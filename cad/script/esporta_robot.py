"""Descrizione del robot dal modello Fusion, per il software (S0): scrive `robot/cad.json`, le mesh dei segmenti e le
pose di controllo della cinematica. Lo legge `tools/genera_robot.py`.

Uso dal connettore, un passo per chiamata (ognuno sotto i 40 s):
    runpy.run_path('/Users/paul/hexapod-v2/cad/script/esporta_robot.py')['main'](['geometria'])

Passi:
  geometria  (sola lettura) parametri utente, assi delle coxe, lunghezze e assi della zampa, limiti meccanici dei giunti,
             tabella del ginocchio minimo, massa, baricentro e inerzia di ogni parte nella terna del suo segmento,
             pose dei cicli verificati nel CAD -> robot/cad.json
  mesh       (sola lettura) robot/mesh/<segmento>.stl: corpo nella terna del robot; coxa, femore e tibia nella terna della
             zampa "come costruita" (imbardata 0, alpha 0, gamma 90)
  pose       muove i giunti veri (coxa, femore e ginocchio di una zampa) su una griglia di pose, legge la punta del piede
             nella terna del robot e scrive robot/pose_cad.json; alla fine rimette i giunti a zero. kw: imbardate=[...]
             per farne una parte (una chiamata per imbardata se si supera il tempo)

Terne (mm, gradi):
  robot   X avanti, Y a sinistra, Z in alto; origine al centro del corpo, all'altezza degli assi dei femori
  zampa   origine sull'asse della coxa all'altezza dell'asse del femore, X verso l'esterno lungo la direzione neutra,
          Y lungo gli assi di femore e ginocchio verso Femore_A, Z in alto. Le sei zampe sono la stessa zampa ruotata
          attorno a Z (non specchiata)
  angoli  imbardata attorno a +Z dalla direzione neutra; alpha del femore sopra l'orizzontale; gamma angolo interno al
          ginocchio (180 = zampa distesa), come calc/statica_tripode.py -> ik_piano
"""
import datetime
import hashlib
import json
import math
import os
import runpy
import struct
import time

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
REPO = os.path.dirname(os.path.dirname(QUI))
OUT = os.path.join(REPO, 'robot')
V = runpy.run_path(os.path.join(QUI, 'versione.py'))
AS = runpy.run_path(os.path.join(QUI, 'assieme.py'))
ZA = runpy.run_path(os.path.join(QUI, 'zampa.py'))

# Masse delle parti stampate come in docs/progetto-meccanico.md: pareti e fondi 1,2 mm pieni, il resto al 25 %;
# densita' PETG-CF 1,3, PLA 1,24, TPU 1,21 g/cm3 (piedino pieno). Materiali per parte da colori.py (D-065).
RHO = {'PETG-CF': 1.3, 'PLA': 1.24, 'TPU': 1.21}
GUSCIO_CM, RIEMPIMENTO = 0.12, 0.25
PLA = ('Corpo_Carapace', 'Cover_Femore_A', 'Cover_Femore_B', 'Cover_Tibia', 'Corpo_Vassoio', 'Corpo_Fascia',
       'Corpo_Visiera', 'Corpo_Gonne', 'Corpo_Sportello_Servizio')
TPU = ('Piedino',)
# parti comprate: massa dichiarata in g (servo: datasheet AZDelivery, V; batteria 245-259 +-20, arrotondata per eccesso;
# le altre stimate dalle pagine dei venditori: sono i valori usati per i 2583 g di progetto-meccanico.md)
COMPRATE = {'Rif_Servo_MG996R': 55.0, 'Rif_Squadretta_25T': 4.0, 'Rif_Cuscinetto_LF1050ZZ': 2.0, 'Rif_Perno_5': 2.0,
            'Rif_Batteria_2S5200': 260.0, 'Rif_SSC32_V25': 30.0, 'Rif_ESP32_S3_CAM': 12.0, 'Rif_Camera_OV3660_75': 4.0,
            'Rif_Reg_Servo_D42V110F6': 17.0, 'Rif_Pulsante_12': 8.0, 'Rif_Cicalino_BX100': 10.0}
NON_MODELLATO_G = 360.0       # cavi, viteria, inserti, logica, fusibili, Wago, T-plug, interruttore (progetto-meccanico.md)
SALTA = ('flat', 'linguetta', 'zona_spine_servo', 'zona_barre_retro', 'uscita_cavi')   # ingombri non rigidi o sovrapposti
# cicli a tripode verificati senza urti nel CAD (progetto-meccanico.md, 9 ottobre 2026): passo 60, alzata 30
CICLI = [{'h': 100, 'xf0': 45, 'fasi': 8, 'giro': 0}, {'h': 130, 'xf0': 25, 'fasi': 8, 'giro': 0},
         {'h': 80, 'xf0': 60, 'fasi': 16, 'giro': 0}, {'h': 70, 'xf0': 70, 'fasi': 16, 'giro': 0},
         {'h': 100, 'xf0': 45, 'fasi': 8, 'giro': 30}, {'h': 70, 'xf0': 70, 'fasi': 8, 'giro': 30}]
PASSO, ALZATA = 60.0, 30.0
# griglia dell'oracolo: dentro i limiti meccanici dei giunti (alpha -49...85, gamma 29...180), urti esclusi
POSE_ALPHA = (-45.0, -15.0, 20.0, 50.0, 80.0)
POSE_GAMMA = (40.0, 75.0, 110.0, 150.0, 178.0)
POSE_IMBARDATA = (-30.0, 0.0, 25.0)


def _mm(des, expr):
    return des.unitsManager.evaluateExpression(expr, 'mm') * 10.0


def _pt(m, p):
    q = adsk.core.Point3D.create(p[0] / 10, p[1] / 10, p[2] / 10)
    q.transformBy(m)
    return [q.x * 10, q.y * 10, q.z * 10]


def _rot(m):
    a = m.asArray()
    return [[a[0], a[1], a[2]], [a[4], a[5], a[6]], [a[8], a[9], a[10]]]


def _matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def _trasp(a):
    return [[a[j][i] for j in range(3)] for i in range(3)]


def _corpi(comp, m):
    """[(corpo nativo, matrice dalla terna del suo componente alla terna di m)] con i sotto-componenti."""
    out = [(b, m) for b in comp.bRepBodies if b.name not in SALTA]
    for c in comp.occurrences:
        mc = c.transform2.copy()
        mc.transformBy(m)
        out += _corpi(c.component, mc)
    return out


def _proprieta(corpi, massa_g):
    """Massa, baricentro (mm) e tensore d'inerzia attorno al baricentro (g mm2) nella terna di arrivo, con densita'
    uniforme scalata alla massa data. Fusion da' i momenti attorno all'origine del componente, in kg cm2, e i termini
    fuori diagonale gia' come elementi del tensore (verificato il 9 ottobre 2026 sulla batteria: xz = -m cx cz)."""
    elementi = []
    mf_tot = 0.0
    for b, m in corpi:
        pp = b.physicalProperties
        mf = pp.mass * 1000.0                         # g, con il materiale assegnato in Fusion
        if mf <= 0:
            continue
        c = pp.centerOfMass
        c = [c.x * 10, c.y * 10, c.z * 10]
        _, xx, yy, zz, xy, yz, xz = pp.getXYZMomentsOfInertia()
        io = [[xx, xy, xz], [xy, yy, yz], [xz, yz, zz]]
        io = [[v * 1e5 for v in r] for r in io]      # kg cm2 -> g mm2
        d2 = sum(v * v for v in c)
        ic = [[io[i][j] - mf * ((d2 if i == j else 0.0) - c[i] * c[j]) for j in range(3)] for i in range(3)]
        r = _rot(m)
        elementi.append((mf, _pt(m, c), _matmul(_matmul(r, ic), _trasp(r))))
        mf_tot += mf
    if not elementi:
        return None
    k = massa_g / mf_tot
    g = [sum(mf * c[i] for mf, c, _ in elementi) / mf_tot for i in range(3)]
    tot = [[0.0] * 3 for _ in range(3)]
    for mf, c, ic in elementi:
        d = [c[i] - g[i] for i in range(3)]
        d2 = sum(v * v for v in d)
        for i in range(3):
            for j in range(3):
                tot[i][j] += k * (ic[i][j] + mf * ((d2 if i == j else 0.0) - d[i] * d[j]))
    return {'massa_g': round(massa_g, 2), 'baricentro_mm': [round(v, 3) for v in g],
            'inerzia_gmm2': [[round(v, 1) for v in r] for r in tot]}


def _massa_stampata(nome, corpi):
    v = sum(b.volume for b, _ in corpi)
    a = sum(b.area for b, _ in corpi)
    if nome in TPU:
        return 'TPU', RHO['TPU'] * v
    mat = 'PLA' if nome in PLA else 'PETG-CF'
    pareti = min(v, a * GUSCIO_CM)
    return mat, RHO[mat] * (pareti + (v - pareti) * RIEMPIMENTO)


def _parte(nome, corpi):
    if nome in COMPRATE:
        mat, m = 'comprato', COMPRATE[nome]
    elif nome.startswith('Rif_') or nome.startswith('Ingombro_'):
        return None                                   # ingombri senza massa propria: nel non modellato
    else:
        mat, m = _massa_stampata(nome, corpi)
    p = _proprieta(corpi, m)
    if p is None:
        return None
    p['materiale'] = mat
    return p


def _corpo_occ(root):
    return [o for o in root.occurrences if o.component.name == 'Corpo'][0]


def _prima_zampa(root):
    return [o for o in root.occurrences if o.component.name == 'Zampa'][0]


def _segmenti(des, root):
    """{segmento: [(nome della parte, [(corpo, matrice)])]}: corpo nella terna del robot, la zampa nella sua terna."""
    seg = {'corpo': [], 'coxa': [], 'femore': [], 'tibia': []}
    corpo = _corpo_occ(root)
    for o in corpo.component.occurrences:
        seg['corpo'].append((o.component.name, _corpi(o.component, o.transform2)))
    for o in _prima_zampa(root).component.occurrences:
        seg[AS['_gruppo'](des, o)].append((o.component.name, _corpi(o.component, o.transform2)))
    return seg


def _parametri(des):
    out = {}
    for p in des.userParameters:
        if p.unit == 'mm':
            v = p.value * 10
        elif p.unit == 'deg':
            v = math.degrees(p.value)
        else:
            v = p.value
        out[p.name] = {'valore': round(v, 6), 'unita': p.unit, 'espressione': p.expression, 'commento': p.comment}
    return out


def _limiti_giunti(root):
    out = {}
    giunti = list(_prima_zampa(root).component.asBuiltJoints) + list(root.asBuiltJoints)
    for j in giunti:
        mot = adsk.fusion.RevoluteJointMotion.cast(j.jointMotion)
        if mot is None:
            continue
        lim = mot.rotationLimits
        out[j.name] = [round(math.degrees(lim.minimumValue), 3) if lim.isMinimumValueEnabled else None,
                       round(math.degrees(lim.maximumValue), 3) if lim.isMaximumValueEnabled else None]
    return out


def geometria(des, root):
    t0 = time.time()
    lc, lf, lt = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lf'), _mm(des, 'zam_Lt')
    coxe = {n: {'x': round(x, 3), 'y': round(y, 3), 'direzione': round(d, 3)} for n, (x, y, d) in AS['coxe'](des).items()}
    giunti = _limiti_giunti(root)
    sf, sg = ZA['SF'], ZA['SG']
    a0, a1 = ZA['LIMITI']['alpha']
    g0, g1 = ZA['LIMITI']['gamma']
    parti = {}
    massa = {}
    for s, voci in _segmenti(des, root).items():
        for nome, corpi in voci:
            p = _parte(nome, corpi)
            if p is None:
                continue
            p['segmento'] = s
            chiave = nome
            i = 2
            while chiave in parti:
                chiave = '%s_%d' % (nome, i)
                i += 1
            parti[chiave] = p
            massa[s] = massa.get(s, 0.0) + p['massa_g']
    totale = massa['corpo'] + 6 * (massa['coxa'] + massa['femore'] + massa['tibia'])
    cicli = []
    for c in CICLI:
        pose = []
        for k in range(c['fasi']):
            f = k / float(c['fasi'])
            pose.append({'fase': round(f, 6), 'zampe': AS['pose_tripode'](des, c['h'], c['xf0'], PASSO, ALZATA, f, c['giro'])})
        cicli.append(dict(c, passo=PASSO, alzata=ALZATA, pose=pose))
    doc = adsk.core.Application.get().activeDocument
    out = {
        'versione': V['VERSIONE'], 'documento': doc.name, 'esportato': datetime.datetime.now().isoformat(timespec='seconds'),
        'unita': 'mm, g, gradi; inerzie in g mm2 attorno al baricentro della parte, nella terna del segmento',
        'terne': {'robot': 'X avanti, Y a sinistra, Z in alto; origine al centro del corpo, all\'altezza degli assi dei femori',
                  'zampa': 'origine sull\'asse della coxa all\'altezza del femore; X verso l\'esterno, Y verso Femore_A, Z in alto; '
                           'parti nella posa come costruita (imbardata 0, alpha 0, gamma 90)'},
        'coxe': coxe,
        'zampa': {
            'Lc': lc, 'Lf': lf, 'Lt': lt,
            'asse_coxa': {'punto': [0.0, 0.0, 0.0], 'direzione': [0.0, 0.0, 1.0]},
            'asse_femore': {'punto': [lc, 0.0, 0.0], 'direzione': [0.0, 1.0, 0.0]},
            'asse_ginocchio': {'punto': [lc + lf, 0.0, 0.0], 'direzione': [0.0, 1.0, 0.0]},
            'punta_piede': [lc + lf, 0.0, -lt],
            'nota_punta': 'punto piu\' basso della suola del piedino nella posa come costruita (z -110 nel modello)',
        },
        'convenzioni': {
            'alpha': 'alpha = %g * valore di G_femore' % sf, 'gamma': 'gamma = 90 + %g * valore di G_ginocchio' % sg,
            'imbardata': 'imbardata = valore di G_coxa_<zampa> (segno misurato dal passo pose, in pose_cad.json)',
        },
        'limiti_meccanici': {
            'giunti_fusion': giunti,
            'alpha': [a0, a1], 'gamma': [g0, g1], 'imbardata': [-AS['LIMITE_COXA'], AS['LIMITE_COXA']],
            'gamma_min': {str(k): v for k, v in sorted(ZA['GAMMA_MIN'].items())},
            'nota': 'campo libero misurato con i giunti veri senza corpo (zampa.py); gamma_min(alpha) a gioco zero, '
                    'contatto tra zampe vicine tra 31 e 32 gradi ciascuna (D-061, D-063): i margini del firmware stanno in robot.yaml',
        },
        'masse': {'segmenti_g': {k: round(v, 1) for k, v in massa.items()}, 'modellato_g': round(totale, 1),
                  'non_modellato_g': NON_MODELLATO_G, 'atteso_g': round(totale + NON_MODELLATO_G, 1),
                  'nota': 'stampate con pareti 1,2 mm e riempimento 25 %, comprate con la massa dichiarata; il non '
                          'modellato (cavi, viteria) va distribuito sul corpo'},
        'parti': parti,
        'cicli_verificati': cicli,
        'parametri': _parametri(des),
    }
    os.makedirs(OUT, exist_ok=True)
    testo = json.dumps(out, indent=1, ensure_ascii=False, sort_keys=False)
    with open(os.path.join(OUT, 'cad.json'), 'w') as f:
        f.write(testo + '\n')
    return {'file': 'robot/cad.json', 'parti': len(parti), 'masse': out['masse'],
            'sha256': hashlib.sha256(testo.encode()).hexdigest()[:12], 's': round(time.time() - t0, 1)}


def _scrivi_stl(percorso, nome, corpi):
    tri = []
    for b, m in corpi:
        mc = b.meshManager.createMeshCalculator()
        mc.setQuality(adsk.fusion.TriangleMeshQualityOptions.LowQualityTriangleMesh)
        me = mc.calculate()
        c, idx = me.nodeCoordinatesAsDouble, me.nodeIndices
        pts = [_pt(m, (c[3 * k] * 10, c[3 * k + 1] * 10, c[3 * k + 2] * 10)) for k in range(len(c) // 3)]
        for i in range(0, len(idx), 3):
            tri.append(pts[idx[i]] + pts[idx[i + 1]] + pts[idx[i + 2]])
    with open(percorso, 'wb') as f:
        f.write(('esapode ' + nome).encode()[:80].ljust(80, b' '))
        f.write(struct.pack('<I', len(tri)))
        for t in tri:
            f.write(struct.pack('<3f', 0, 0, 0) + struct.pack('<9f', *t) + b'\x00\x00')
    return len(tri)


def mesh(des, root):
    t0 = time.time()
    d = os.path.join(OUT, 'mesh')
    os.makedirs(d, exist_ok=True)
    out = {}
    for s, voci in _segmenti(des, root).items():
        corpi = [x for _, cs in voci for x in cs]
        out[s] = _scrivi_stl(os.path.join(d, s + '.stl'), s, corpi)
    out['s'] = round(time.time() - t0, 1)
    return out


def _rev(j):
    return adsk.fusion.RevoluteJointMotion.cast(j.jointMotion)


def _punta_robot(des, zo, punta):
    """Punta del piede di un'istanza di Zampa nella terna del robot: dalla posa del proxy della tibia."""
    tib = [o for o in zo.component.occurrences if o.component.name == 'Tibia'][0]
    inv = tib.transform2.copy()                       # nativa = come costruita, nella terna della zampa
    inv.invert()
    m = inv.copy()
    m.transformBy(tib.createForAssemblyContext(zo).transform2)
    return _pt(m, punta)


def pose(des, root, imbardate=POSE_IMBARDATA):
    t0 = time.time()
    lc, lf, lt = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lf'), _mm(des, 'zam_Lt')
    punta = (lc + lf, 0.0, -lt)
    zampe = AS['mappa_zampe'](des, root)
    coxe = AS['coxe'](des)
    jz = {j.name: j for j in _prima_zampa(root).component.asBuiltJoints}
    jf, jg = jz['G_femore'], jz['G_ginocchio']
    jc = {j.name[len('G_coxa_'):]: j for j in root.asBuiltJoints if j.name.startswith('G_coxa_')}
    for j in [jf, jg] + list(jc.values()):
        _rev(j).rotationValue = 0.0
    riposo = {n: _punta_robot(des, zo, punta) for n, zo in zampe.items()}
    # quale istanza muovono i giunti di femore e ginocchio (sono condivisi e muovono solo la prima)
    _rev(jf).rotationValue = math.radians(ZA['SF'] * 20.0)
    mossa = [n for n, zo in zampe.items() if max(abs(a - b) for a, b in zip(_punta_robot(des, zo, punta), riposo[n])) > 0.5]
    _rev(jf).rotationValue = 0.0
    if len(mossa) != 1:
        raise RuntimeError('i giunti del femore muovono %s, attesa una sola zampa' % mossa)
    n = mossa[0]
    zo = zampe[n]
    x0, y0, d0 = coxe[n]
    righe = []
    try:
        for yaw in imbardate:
            _rev(jc[n]).rotationValue = math.radians(yaw)
            letto_yaw = math.degrees(_rev(jc[n]).rotationValue)
            for a in POSE_ALPHA:
                for g in POSE_GAMMA:
                    _rev(jf).rotationValue = math.radians(ZA['SF'] * a)
                    _rev(jg).rotationValue = math.radians(ZA['SG'] * (g - 90.0))
                    mis = ZA['misura'](zo)
                    p = _punta_robot(des, zo, punta)
                    righe.append({'zampa': n, 'G_coxa': round(letto_yaw, 4), 'alpha': mis[0], 'gamma': mis[1],
                                  'comandati': [yaw, a, g], 'punta_robot': [round(v, 4) for v in p]})
    finally:
        for j in [jf, jg] + list(jc.values()):
            _rev(j).rotationValue = 0.0
    # segno dell'imbardata: direzione della punta nel piano rispetto all'asse della coxa, meno la direzione neutra
    # (solo con il piede ben fuori dall'asse: vicino all'asse la direzione nel piano non ha senso)
    segni = []
    for r in righe:
        px, py = r['punta_robot'][0] - x0, r['punta_robot'][1] - y0
        if abs(r['G_coxa']) > 1 and math.hypot(px, py) > 30:
            yaw = (math.degrees(math.atan2(py, px)) - d0 + 180) % 360 - 180
            segni.append(round(yaw / r['G_coxa'], 4))
    percorso = os.path.join(OUT, 'pose_cad.json')
    vecchie = []
    if os.path.exists(percorso):
        with open(percorso) as f:
            vecchie = [r for r in json.load(f)['pose'] if r['comandati'][0] not in imbardate]
    doc = adsk.core.Application.get().activeDocument
    tutte = sorted(vecchie + righe, key=lambda r: tuple(r['comandati']))
    with open(percorso, 'w') as f:
        json.dump({'versione': V['VERSIONE'], 'documento': doc.name,
                   'nota': 'punta del piede (punto zampa.punta_piede di cad.json) letta dal modello con i giunti veri; '
                           'imbardata = segno_imbardata * valore di G_coxa', 'zampa': n,
                   'riposo_robot': {k: [round(v, 4) for v in p] for k, p in riposo.items()},
                   'segno_imbardata': segni[0] if segni else None, 'pose': tutte}, f, indent=1)
        f.write('\n')
    return {'file': 'robot/pose_cad.json', 'zampa': n, 'pose': len(righe), 'totale': len(tutte),
            'segno_imbardata': sorted(set(segni)), 's': round(time.time() - t0, 1)}


def main(passi, **kw):
    out = {'passi': passi}
    app = adsk.core.Application.get()
    V['controlla'](app)
    des = adsk.fusion.Design.cast(app.activeProduct)
    root = des.rootComponent
    if des.snapshots.hasPendingSnapshot:
        raise RuntimeError('posa pendente nel design: annullarla (revertPendingSnapshot) prima di esportare')
    if 'geometria' in passi:
        out['geometria'] = geometria(des, root)
    if 'mesh' in passi:
        out['mesh'] = mesh(des, root)
    if 'pose' in passi:
        out['pose'] = pose(des, root, tuple(kw.get('imbardate', POSE_IMBARDATA)))
    print(json.dumps(out, ensure_ascii=False))
    return out
