"""Esporta dal CAD i dati della guida di montaggio (D-075, docs/piano-guida.md), in sola lettura.

Passi, uno o piu' per chiamata del connettore (ognuno si ferma a `budget_s` secondi e dice quanti ne restano):
    manifest   occorrenze del corpo e della zampa con chiavi stabili, trasformate, colori dei corpi -> guida/dati/manifest.json
    mesh       un PLY per componente, nella terna propria, solo se il revisionId e' cambiato -> build/guida/cad/mesh/
    fori       cilindri concavi dei pezzi con il nome della lavorazione -> build/guida/cad/fori/, poi guida/dati/fori.json
    controllo  rilettura: ogni componente del manifest ha la sua mesh e i proxy coincidono con istanza x locale

    import runpy
    def run(_context: str):
        runpy.run_path('/Users/paul/hexapod-v2/cad/script/esporta_guida.py')['main'](['manifest', 'mesh'])

Le zampe sono la stessa zampa ruotata: le parti si scrivono una volta, nella terna della zampa come costruita, piu' le
sei terne delle istanze. Le chiavi del corpo sono quelle di assieme.pose_corpo (Servo_Coxa_AS, SSC32, ...) e il nome
del componente per le parti stampate; quelle della zampa sono il pezzo piu' il giunto (Servo_femore, Perno_coxa, ...).
"""
import array
import fnmatch
import json
import math
import os
import runpy
import time
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
RADICE = os.path.dirname(os.path.dirname(QUI))
V = runpy.run_path(os.path.join(QUI, 'versione.py'))
AS = runpy.run_path(os.path.join(QUI, 'assieme.py'))
DATI = os.path.join(RADICE, 'guida', 'dati')
CACHE = os.path.join(RADICE, 'build', 'guida', 'cad')
SALTA = ('flat', 'linguetta', 'zona_spine_servo', 'zona_barre_retro', 'uscita_cavi')   # ingombri non rigidi o sovrapposti
CORTI = {'Rif_Servo_MG996R': 'Servo', 'Rif_Squadretta_25T': 'Squadretta', 'Rif_Cuscinetto_LF1050ZZ': 'Cuscinetto',
         'Rif_Perno_5': 'Perno'}
# pezzi comprati che nella zampa ci sono una volta sola, lontani dai giunti
SINGOLI = {'Rif_FSR_400': 'FSR_piede'}
# qualita' delle mesh: le parti stampate fini (i fori da 2,4 restano tondi), le comprate dagli STEP grossolane
TOLLERANZA_CM, DEVIAZIONE_RAD = 0.003, math.radians(15)


def _mm(des, expr):
    return des.unitsManager.evaluateExpression(expr, 'mm') * 10.0


def _matrice(m):
    """Le prime tre righe della matrice 4x4, traslazione in mm."""
    d = list(m.asArray())
    out = []
    for r in range(3):
        out += [round(d[4 * r], 9), round(d[4 * r + 1], 9), round(d[4 * r + 2], 9), round(d[4 * r + 3] * 10, 4)]
    return out


def _colore(corpo):
    """(nome dell'aspetto, [r, g, b]) del corpo: opaque_albedo se c'e', altrimenti la prima proprieta' colore."""
    a = corpo.appearance
    if a is None:
        return ('', [180, 180, 180])
    prop = a.appearanceProperties.itemById('opaque_albedo')
    if prop is None:
        for i in range(a.appearanceProperties.count):
            p = a.appearanceProperties.item(i)
            if p.objectType == adsk.core.ColorProperty.classType():
                prop = p
                break
    if prop is None or adsk.core.ColorProperty.cast(prop) is None or adsk.core.ColorProperty.cast(prop).value is None:
        return (a.name, [180, 180, 180])
    c = adsk.core.ColorProperty.cast(prop).value
    return (a.name, [c.red, c.green, c.blue])


def _corpi(comp, m):
    """[(corpo nativo, matrice dalla terna del suo componente alla terna di comp)] con i sotto-componenti."""
    out = [(b, m) for b in comp.bRepBodies if b.name not in SALTA]
    for c in comp.occurrences:
        mc = c.transform2.copy()
        mc.transformBy(m)
        out += _corpi(c.component, mc)
    return out


def _tipo(nome):
    if nome.startswith('Rif_'):
        return 'comprato'
    if nome.startswith('Ingombro_'):
        return 'ingombro'
    return 'stampato'


# ------------------------------------------------------------------------------------------------ manifest
def _chiavi_corpo(des, corpo):
    """{occorrenza nativa dentro Corpo: chiave}: le chiavi di pose_corpo per le Rif_, il nome per le parti stampate."""
    out = {}
    for chiave, o in AS['_istanze_corpo'](corpo).items():
        if o is not None:
            out[o.name] = chiave
    for o in corpo.component.occurrences:
        n = o.component.name
        if o.name in out or n.startswith('Rif_'):
            continue
        if n == 'Corpo_Slitta_Regolatore':
            # la destra e' la sinistra girata attorno a un asse che non passa per l'origine: conta dove finisce la geometria
            bb = o.component.bRepBodies.item(0).boundingBox
            c = adsk.core.Point3D.create((bb.minPoint.x + bb.maxPoint.x) / 2, (bb.minPoint.y + bb.maxPoint.y) / 2, 0)
            c.transformBy(o.transform2)
            out[o.name] = n + ('_S' if c.y > 0 else '_D')
        else:
            out[o.name] = n
    return out


def _chiave_zampa(des, o):
    """Pezzo della zampa piu' il giunto, dalla posizione su x nella terna della zampa come costruita."""
    n = o.component.name
    if n in SINGOLI:
        return SINGOLI[n]
    if n not in CORTI:
        return n
    lc, lf = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lf')
    x = o.transform2.translation.x * 10
    giunto = min((('coxa', 0.0), ('femore', lc), ('ginocchio', lc + lf)), key=lambda g: abs(x - g[1]))[0]
    return CORTI[n] + '_' + giunto


def manifest(des, root):
    corpo = AS['_corpo'](root)
    zampe = AS['mappa_zampe'](des, root)
    zampa = next(iter(zampe.values()))
    componenti, occorrenze = {}, []

    def registra(comp):
        if comp.name in componenti:
            return
        corpi = _corpi(comp, adsk.core.Matrix3D.create())
        aspetti = {}
        lo, hi = [1e9] * 3, [-1e9] * 3
        for b, mb in corpi:
            nome, rgb = _colore(b)
            aspetti.setdefault(nome, rgb)
            bb = b.boundingBox
            for x in (bb.minPoint.x, bb.maxPoint.x):
                for y in (bb.minPoint.y, bb.maxPoint.y):
                    for z in (bb.minPoint.z, bb.maxPoint.z):
                        p = adsk.core.Point3D.create(x, y, z)
                        p.transformBy(mb)
                        for k, v in enumerate((p.x, p.y, p.z)):
                            lo[k], hi[k] = min(lo[k], v * 10), max(hi[k], v * 10)
        componenti[comp.name] = {'tipo': _tipo(comp.name), 'revisione': comp.revisionId, 'mesh': comp.name + '.ply',
                                 'aspetti': [[k, v] for k, v in sorted(aspetti.items())], 'corpi': len(corpi),
                                 'bbox': [[round(v, 3) for v in lo], [round(v, 3) for v in hi]]}

    chiavi = _chiavi_corpo(des, corpo)
    for o in corpo.component.occurrences:
        registra(o.component)
        occorrenze.append({'chiave': 'corpo/' + chiavi[o.name], 'componente': o.component.name, 'assieme': 'corpo',
                           'T': _matrice(o.transform2),
                           **({'alternativa': True} if o.component.name == 'Corpo_Sportello_Servizio_Zaino' else {})})
    viste = set()
    for o in zampa.component.occurrences:
        registra(o.component)
        k = _chiave_zampa(des, o)
        if k in viste:
            raise RuntimeError('chiave della zampa doppia: ' + k)
        viste.add(k)
        occorrenze.append({'chiave': 'zampa/' + k, 'componente': o.component.name, 'assieme': 'zampa',
                           'segmento': AS['_gruppo'](des, o), 'T': _matrice(o.transform2)})
    # attrezzi stampati (dime, cavalletto, provini; cad/script/attrezzi.py): nella terna propria, non si montano
    for o in root.occurrences:
        n = o.component.name
        if n.startswith(('Attrezzo_', 'Dima_')):
            registra(o.component)
            occorrenze.append({'chiave': 'attrezzo/' + n.replace('Attrezzo_', ''), 'componente': n, 'assieme': 'attrezzo',
                               'T': [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]})
    lib = {o.component.name: o for o in root.occurrences if o.component.name.startswith('Rif_')}
    for chiave, (nome_lib, m, togli) in AS['alternative'](des).items():
        registra(lib[nome_lib].component)
        occorrenze.append({'chiave': 'corpo/' + chiave, 'componente': nome_lib, 'assieme': 'corpo', 'virtuale': True,
                           'sostituisce': list(togli), 'T': _matrice(m)})
    doc = adsk.core.Application.get().activeDocument
    out = {'versione': V['VERSIONE'], 'documento': doc.name, 'unita': 'mm',
           'parametri': {k: round(_mm(des, k), 4) for k in ('zam_Lc', 'zam_Lf', 'zam_Lt', 'ins_m3_d', 'ins_m3_l', 'ins_m2_d', 'ins_m2_l')},
           'istanze': {'corpo': _matrice(corpo.transform2), 'zampe': {n: _matrice(z.transform2) for n, z in sorted(zampe.items())}},
           'componenti': dict(sorted(componenti.items())), 'occorrenze': occorrenze}
    os.makedirs(DATI, exist_ok=True)
    with open(os.path.join(DATI, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False, sort_keys=False)
        f.write('\n')
    return {'componenti': len(componenti), 'occorrenze': len(occorrenze)}


# ------------------------------------------------------------------------------------------------ mesh
def _scrivi_ply(percorso, corpi, comprato):
    """PLY binario: vertici in mm con il colore del corpo, facce indicizzate."""
    xyz, rgb, facce = array.array('f'), array.array('B'), array.array('i')
    base = 0
    for b, m in corpi:
        mc = b.meshManager.createMeshCalculator()
        if comprato:
            mc.setQuality(adsk.fusion.TriangleMeshQualityOptions.LowQualityTriangleMesh)
        else:
            mc.surfaceTolerance = TOLLERANZA_CM
            mc.maxNormalDeviation = DEVIAZIONE_RAD
        me = mc.calculate()
        c, idx = me.nodeCoordinatesAsDouble, me.nodeIndices
        col = _colore(b)[1]
        d = list(m.asArray())
        n = len(c) // 3
        for i in range(n):
            x, y, z = c[3 * i], c[3 * i + 1], c[3 * i + 2]
            xyz.extend(((d[0] * x + d[1] * y + d[2] * z + d[3]) * 10, (d[4] * x + d[5] * y + d[6] * z + d[7]) * 10,
                        (d[8] * x + d[9] * y + d[10] * z + d[11]) * 10))
            rgb.extend(col)
        for k in range(0, len(idx), 3):
            facce.extend((3,))
            facce.extend((idx[k] + base, idx[k + 1] + base, idx[k + 2] + base))
        base += n
    nv, nf = base, len(facce) // 4
    intest = ('ply\nformat binary_little_endian 1.0\nelement vertex %d\nproperty float x\nproperty float y\nproperty float z\n'
              'property uchar red\nproperty uchar green\nproperty uchar blue\nelement face %d\n'
              'property list uchar int vertex_indices\nend_header\n' % (nv, nf)).encode('ascii')
    with open(percorso, 'wb') as f:
        f.write(intest)
        for i in range(nv):
            f.write(xyz[3 * i:3 * i + 3].tobytes())
            f.write(rgb[3 * i:3 * i + 3].tobytes())
        for k in range(nf):
            f.write(bytes((3,)))
            f.write(facce[4 * k + 1:4 * k + 4].tobytes())
    return nv, nf


def mesh(des, root, budget_s=25.0, forza=False, solo=None):
    t0 = time.time()
    with open(os.path.join(DATI, 'manifest.json'), encoding='utf-8') as f:
        man = json.load(f)
    cartella = os.path.join(CACHE, 'mesh')
    os.makedirs(cartella, exist_ok=True)
    p_indice = os.path.join(cartella, 'indice.json')
    indice = json.load(open(p_indice, encoding='utf-8')) if os.path.exists(p_indice) else {}
    comp = {}

    def trova(c):
        comp.setdefault(c.name, c)
        for o in c.occurrences:
            trova(o.component)
    trova(root)
    fatti, restano = [], []
    for nome, info in man['componenti'].items():
        if solo and nome not in solo:
            continue
        if not forza and indice.get(nome) == info['revisione'] and os.path.exists(os.path.join(cartella, info['mesh'])):
            continue
        if time.time() - t0 > budget_s:
            restano.append(nome)
            continue
        c = comp[nome]
        nv, nf = _scrivi_ply(os.path.join(cartella, info['mesh']), _corpi(c, adsk.core.Matrix3D.create()), info['tipo'] == 'comprato')
        indice[nome] = info['revisione']
        fatti.append('%s %d' % (nome, nf))
        with open(p_indice, 'w', encoding='utf-8') as f:
            json.dump(indice, f, indent=1, sort_keys=True)
    return {'fatti': fatti, 'restano': len(restano), 's': round(time.time() - t0, 1)}


# ------------------------------------------------------------------------------------------------ fori
def _rifletti(pt, o, n):
    """Punto riflesso sul piano (o, n)."""
    k = math.sqrt(n.x * n.x + n.y * n.y + n.z * n.z)
    nx, ny, nz = n.x / k, n.y / k, n.z / k
    d = (pt.x - o.x) * nx + (pt.y - o.y) * ny + (pt.z - o.z) * nz
    return adsk.core.Point3D.create(pt.x - 2 * d * nx, pt.y - 2 * d * ny, pt.z - 2 * d * nz)


def _firma(fa):
    """Tipo di superficie e raggio: restringe la ricerca della faccia d'origine di una copia specchiata."""
    g = fa.geometry
    return g.surfaceType, round(getattr(g, 'radius', 0.0), 5)


def _sulla_faccia(fa, pt):
    ev = fa.evaluator
    ok, par = ev.getParameterAtPoint(pt)
    if not ok:
        return False
    ok, q = ev.getPointAtParameter(par)
    return ok and q.distanceTo(pt) < 1e-4 and ev.isParameterOnFace(par)


def _lavorazioni_facce(comp):
    """[(faccia, lavorazione, origine)] delle facce create da estrusioni e specchi. Una copia specchiata prende il nome
    della lavorazione d'origine: un punto della copia, riflesso sul piano dello specchio, cade sulla faccia d'origine
    (anche per gli specchi di specchi, nell'ordine in cui sono fatti). Se non la trova resta il nome dello specchio."""
    out, fonti = [], []
    for f in comp.features.extrudeFeatures:
        if f.isSuppressed:
            continue
        for fa in f.faces:
            fonti.append((fa, f.name))
            out.append((fa, f.name, 'estrusione'))
    for f in comp.features.mirrorFeatures:
        if f.isSuppressed:
            continue
        g = f.mirrorPlane.geometry
        per_firma = {}
        for fa, lav in fonti:
            per_firma.setdefault(_firma(fa), []).append((fa, lav))
        nuove = []
        for i in range(f.patternElements.count):
            for fa in f.patternElements.item(i).faces:
                r = _rifletti(fa.pointOnFace, g.origin, g.normal)
                lav = next((nome for c, nome in per_firma.get(_firma(fa), []) if _sulla_faccia(c, r)), None)
                nuove.append((fa, lav or f.name, 'specchio' if lav else 'specchio senza origine'))
        for fa, lav, org in nuove:
            fonti.append((fa, lav))
            out.append((fa, lav, org))
    return out


def _mappa_lavorazioni(comp):
    """{(nome del corpo, tempId della faccia): (lavorazione, origine)}; vince la prima lavorazione che crea la faccia."""
    mappa = {}
    for fa, lav, org in _lavorazioni_facce(comp):
        mappa.setdefault((fa.body.name, fa.tempId), (lav, org))
    return mappa


def _vicina(edge, faccia):
    for f in edge.faces:
        if f.tempId != faccia.tempId or f.body.name != faccia.body.name:
            return f
    return None


def _estremo(faccia, edge, asse, r):
    """Che cosa c'e' oltre lo spigolo circolare: fondo (foro cieco), svasato, gradino (cilindro coassiale) o aperto."""
    v = _vicina(edge, faccia)
    if v is None:
        return 'aperto', None
    st = v.geometry.surfaceType
    if st == adsk.core.SurfaceTypes.ConeSurfaceType:
        return 'svasato', None
    if st == adsk.core.SurfaceTypes.CylinderSurfaceType:
        return 'gradino', round(v.geometry.radius * 20, 3)
    if st == adsk.core.SurfaceTypes.PlaneSurfaceType:
        n = v.geometry.normal
        parallelo = abs(n.x * asse.x + n.y * asse.y + n.z * asse.z) > 0.999
        if parallelo and v.area < math.pi * r * r * 1.05:
            return 'fondo', None
    return 'aperto', None


def _cilindri(comp, m):
    """Cilindri concavi (fori) da 1,5 a 6,5 mm dei corpi del componente e dei sotto-componenti, nella terna di comp."""
    out = []
    for c, mt in [(comp, adsk.core.Matrix3D.create())] + [(o.component, o.transform2) for o in comp.occurrences]:
        mappa = _mappa_lavorazioni(c)
        for b in c.bRepBodies:
            if b.name in SALTA:
                continue
            for fa in b.faces:
                g = fa.geometry
                if g.surfaceType != adsk.core.SurfaceTypes.CylinderSurfaceType:
                    continue
                r = g.radius
                if not 0.075 <= r <= 0.325:
                    continue
                o, a = g.origin, g.axis
                a.normalize()
                p = fa.pointOnFace
                ok, nrm = fa.evaluator.getNormalAtPoint(p)
                w = adsk.core.Vector3D.create(p.x - o.x, p.y - o.y, p.z - o.z)
                ax = w.dotProduct(a)
                w = adsk.core.Vector3D.create(w.x - a.x * ax, w.y - a.y * ax, w.z - a.z * ax)
                if not ok or nrm.dotProduct(w) >= 0:          # la normale guarda fuori dall'asse: e' una bugna
                    continue
                ts = [adsk.core.Vector3D.create(v.geometry.x - o.x, v.geometry.y - o.y, v.geometry.z - o.z).dotProduct(a)
                      for v in fa.vertices]
                if not ts:
                    continue
                t0, t1 = min(ts), max(ts)
                estremi = {}
                for e in fa.edges:
                    if e.geometry.curveType != adsk.core.Curve3DTypes.Circle3DCurveType:
                        continue
                    c3 = e.geometry.center
                    t = adsk.core.Vector3D.create(c3.x - o.x, c3.y - o.y, c3.z - o.z).dotProduct(a)
                    estremi['t0' if abs(t - t0) < abs(t - t1) else 't1'] = _estremo(fa, e, a, r)
                p0 = adsk.core.Point3D.create(o.x + a.x * t0, o.y + a.y * t0, o.z + a.z * t0)
                p1 = adsk.core.Point3D.create(o.x + a.x * t1, o.y + a.y * t1, o.z + a.z * t1)
                p0.transformBy(mt)
                p1.transformBy(mt)
                p0.transformBy(m)
                p1.transformBy(m)
                lav = mappa.get((b.name, fa.tempId), ('', ''))
                out.append({'lav': lav[0], 'origine': lav[1], 'corpo': b.name, 'd': round(r * 20, 3),
                            'p0': [round(p0.x * 10, 3), round(p0.y * 10, 3), round(p0.z * 10, 3)],
                            'p1': [round(p1.x * 10, 3), round(p1.y * 10, 3), round(p1.z * 10, 3)],
                            'e0': list(estremi.get('t0', ('aperto', None))), 'e1': list(estremi.get('t1', ('aperto', None)))})
    return out


def _teste(comp):
    """Cilindri convessi di Ingombro_Teste_A (teste delle viti sul lato A): caso di controllo del piazzamento."""
    out = []
    for b in comp.bRepBodies:
        for fa in b.faces:
            g = fa.geometry
            if g.surfaceType != adsk.core.SurfaceTypes.CylinderSurfaceType:
                continue
            bb = fa.boundingBox
            out.append({'corpo': b.name, 'd': round(g.radius * 20, 3),
                        'centro': [round((bb.minPoint.x + bb.maxPoint.x) * 5, 3), round((bb.minPoint.y + bb.maxPoint.y) * 5, 3),
                                   round((bb.minPoint.z + bb.maxPoint.z) * 5, 3)],
                        'asse': [round(g.axis.x, 6), round(g.axis.y, 6), round(g.axis.z, 6)]})
    return out


def fori(des, root, budget_s=25.0, forza=False):
    t0 = time.time()
    with open(os.path.join(DATI, 'manifest.json'), encoding='utf-8') as f:
        man = json.load(f)
    cartella = os.path.join(CACHE, 'fori')
    os.makedirs(cartella, exist_ok=True)
    comp = {}

    def trova(c):
        comp.setdefault(c.name, c)
        for o in c.occurrences:
            trova(o.component)
    trova(root)
    fatti, restano = [], 0
    for nome, info in man['componenti'].items():
        p = os.path.join(cartella, nome + '.json')
        if not forza and os.path.exists(p) and json.load(open(p, encoding='utf-8')).get('revisione') == info['revisione']:
            continue
        if time.time() - t0 > budget_s:
            restano += 1
            continue
        dati = {'revisione': info['revisione'], 'fori': _cilindri(comp[nome], adsk.core.Matrix3D.create())}
        if nome == 'Ingombro_Teste_A':
            dati['teste'] = _teste(comp[nome])
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(dati, f)
        fatti.append('%s %d' % (nome, len(dati['fori'])))
    if restano == 0:                                   # tutto pronto: il file unico per la guida, deterministico
        tutti = {}
        for nome, info in man['componenti'].items():
            d = json.load(open(os.path.join(cartella, nome + '.json'), encoding='utf-8'))
            if d['fori'] or d.get('teste'):
                tutti[nome] = {'fori': sorted(d['fori'], key=lambda h: (h['lav'], h['p0'], h['p1'])), **({'teste': d['teste']} if d.get('teste') else {})}
        with open(os.path.join(DATI, 'fori.json'), 'w', encoding='utf-8') as f:
            json.dump({'versione': man['versione'], 'documento': man['documento'], 'componenti': tutti}, f, indent=0, sort_keys=True)
            f.write('\n')
    return {'fatti': fatti, 'restano': restano, 's': round(time.time() - t0, 1)}


# ------------------------------------------------------------------------------------------------ zone
def _zone_richieste():
    """{componente: [glob delle lavorazioni]} da guida/catalogo/zone.yaml (formato semplice: una riga per componente)."""
    out = {}
    with open(os.path.join(RADICE, 'guida', 'catalogo', 'zone.yaml'), encoding='utf-8') as f:
        for riga in f:
            riga = riga.split('#')[0].strip()
            if not riga or ':' not in riga:
                continue
            nome, lista = riga.split(':', 1)
            out[nome.strip()] = [x.strip().strip('"') for x in lista.strip().strip('[]').split(',') if x.strip()]
    return out


def _facce_lavorazioni(comp, modelli):
    """{lavorazione: [facce]} delle lavorazioni il cui nome corrisponde a uno dei glob, copie specchiate comprese."""
    out = {}
    for fa, lav, _ in _lavorazioni_facce(comp):
        if any(fnmatch.fnmatchcase(lav, m) for m in modelli):
            out.setdefault(lav, []).append(fa)
    return out


def _ply_facce(percorso, facce):
    """PLY binario delle facce (mm, terna del componente), senza colore."""
    xyz, tri = array.array('f'), array.array('i')
    base = 0
    for fa in facce:
        mc = fa.meshManager.createMeshCalculator()
        mc.surfaceTolerance = TOLLERANZA_CM
        mc.maxNormalDeviation = DEVIAZIONE_RAD
        me = mc.calculate()
        c, idx = me.nodeCoordinatesAsDouble, me.nodeIndices
        xyz.extend(v * 10 for v in c)
        tri.extend(i + base for i in idx)
        base += len(c) // 3
    intest = ('ply\nformat binary_little_endian 1.0\nelement vertex %d\nproperty float x\nproperty float y\nproperty float z\n'
              'element face %d\nproperty list uchar int vertex_indices\nend_header\n' % (base, len(tri) // 3)).encode('ascii')
    with open(percorso, 'wb') as f:
        f.write(intest)
        f.write(xyz.tobytes())
        for k in range(0, len(tri), 3):
            f.write(bytes((3,)))
            f.write(tri[k:k + 3].tobytes())
    return len(tri) // 3


def zone(des, root):
    """Facce delle lavorazioni di guida/catalogo/zone.yaml in build/guida/cad/zone/<componente>__<lavorazione>.ply,
    con l'indice; segnala i glob che non trovano niente."""
    cartella = os.path.join(CACHE, 'zone')
    os.makedirs(cartella, exist_ok=True)
    comp = {}

    def trova(c):
        comp.setdefault(c.name, c)
        for o in c.occurrences:
            trova(o.component)
    trova(root)
    indice, mancano = {}, []
    for nome, modelli in _zone_richieste().items():
        lav = [m for m in modelli if not m.startswith('corpo:')]
        corpi = [m[6:] for m in modelli if m.startswith('corpo:')]
        trovate = _facce_lavorazioni(comp[nome], lav) if lav else {}
        for b in comp[nome].bRepBodies:             # componenti comprati: zone fatte di corpi interi
            if any(fnmatch.fnmatchcase(b.name, m) for m in corpi):
                trovate.setdefault('corpo:' + b.name, []).extend(list(b.faces))
        mancano += ['%s/%s' % (nome, m) for m in modelli if not any(fnmatch.fnmatchcase(k, m) for k in trovate)]
        for lav, facce in sorted(trovate.items()):
            n = _ply_facce(os.path.join(cartella, '%s__%s.ply' % (nome, lav.replace(':', '-'))), facce)
            indice.setdefault(nome, {})[lav] = n
    with open(os.path.join(cartella, 'indice.json'), 'w', encoding='utf-8') as f:
        json.dump(indice, f, indent=1, sort_keys=True)
    return {'zone': sum(len(v) for v in indice.values()), 'mancano': mancano}


# ------------------------------------------------------------------------------------------------ controllo
def controllo(des, root):
    """Ogni componente ha mesh e fori aggiornati; i proxy delle zampe coincidono con istanza x locale (entro 1e-3 mm)."""
    with open(os.path.join(DATI, 'manifest.json'), encoding='utf-8') as f:
        man = json.load(f)
    indice = json.load(open(os.path.join(CACHE, 'mesh', 'indice.json'), encoding='utf-8'))
    senza_mesh = [n for n, i in man['componenti'].items() if indice.get(n) != i['revisione']]
    scarti = []
    locali = {o['chiave'].split('/', 1)[1]: o['T'] for o in man['occorrenze'] if o['assieme'] == 'zampa'}
    for n, z in AS['mappa_zampe'](des, root).items():
        tz = man['istanze']['zampe'][n]
        for o in z.childOccurrences:
            k = _chiave_zampa(des, o.nativeObject)
            a = _componi(tz, locali[k])
            b = _matrice(o.transform2)
            d = max(abs(a[i] - b[i]) for i in range(12))
            if d > 1e-3:
                scarti.append('%s/%s %.4f' % (n, k, d))
    return {'senza_mesh': senza_mesh, 'scarti': scarti}


def _componi(a, b):
    """Prodotto di due matrici 3x4 in mm (prima b, poi a)."""
    out = []
    for r in range(3):
        for c in range(4):
            v = sum(a[4 * r + k] * b[4 * k + c] for k in range(3))
            out.append(v + (a[4 * r + 3] if c == 3 else 0.0))
    return out


# ------------------------------------------------------------------------------------------------ main
def main(passi, **kw):
    out = {'passi': passi}
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        V['controlla'](app)
        if des.snapshots.hasPendingSnapshot:
            raise RuntimeError('posa pendente: ripristinare prima di esportare per la guida')
        root = des.rootComponent
        if 'manifest' in passi:
            out['manifest'] = manifest(des, root)
        if 'mesh' in passi:
            out['mesh'] = mesh(des, root, kw.get('budget_s', 25.0), kw.get('forza', False), kw.get('solo'))
        if 'fori' in passi:
            out['fori'] = fori(des, root, kw.get('budget_s', 25.0), kw.get('forza', False))
        if 'zone' in passi:
            out['zone'] = zone(des, root)
        if 'controllo' in passi:
            out['controllo'] = controllo(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out
