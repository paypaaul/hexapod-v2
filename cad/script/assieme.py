"""Assieme dell'esapode: corpo fissato, sei zampe, servo di coxa, giunti delle coxe.

Si esegue dentro Fusion sul design "Hexapod v2 - Assieme":
    ns = runpy.run_path('<repo>/cad/script/assieme.py'); ns['main'](['zampe'])

Passi (in chiamate separate, nell'ordine):
  parametri     parametri utente dell'assetto di marcia
  zampe         porta la Zampa esistente nella posizione AS e aggiunge le altre cinque istanze
  istanze       dentro "Corpo": servo di coxa, cuscinetti ed elettronica (cancella le istanze esistenti e i loro giunti)
  giunti_corpo  dentro "Corpo": giunti rigidi tra le istanze e Corpo_Base
  giunti_coxa   alla radice: Corpo fissato; giunti di rivoluzione G_coxa_* tra Corpo_Base e Coxa
  stato         sola lettura: posizioni delle zampe e valori dei giunti
  interferenze  sola lettura: interferenze tra tutte le parti di corpo e zampe
  massa         sola lettura: volumi delle parti stampate e baricentro dei componenti comprati
  ciclo         atteggia le sei zampe a varie fasi del ciclo a tripode (modo='alto' o 'basso'), cerca
                interferenze e ripristina; quattro fasi per chiamata

Nomi delle zampe: A/M/P = anteriore, media, posteriore; S/D = sinistra (+Y), destra (-Y).
Terna di ogni zampa: origine sull'asse della coxa a z = 0, X radiale verso l'esterno.
"""
import json
import math
import os
import runpy
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
Z = runpy.run_path(os.path.join(QUI, 'zampa.py'))
C = runpy.run_path(os.path.join(QUI, 'corpo.py'))
L = Z['L']
P3 = adsk.core.Point3D.create
RIF_SERVO, RIF_CUS = Z['RIF'][0], Z['RIF'][1]
LIMITE_COXA = 45.0          # gradi, per parte: provvisorio, si chiude con la verifica del movimento

# Assetto di marcia (punto di progetto di docs/dimensionamento.md)
PARAMETRI = [
    ('zam_h', '72 mm', 'mm', 'Assetto di marcia: altezza dell asse del femore da terra'),
    ('zam_xf0', '12 mm', 'mm', 'Assetto di marcia: distanza orizzontale del piede dall asse del femore'),
    ('zam_passo', '40 mm', 'mm', 'Andatura: lunghezza del passo'),
    ('zam_alzata', '20 mm', 'mm', 'Andatura: alzata del piede in volo'),
    ('zam_h_basso', '40 mm', 'mm', 'Assetto basso: altezza dell asse del femore da terra'),
    ('zam_xf0_basso', '40 mm', 'mm', 'Assetto basso: distanza orizzontale del piede dall asse del femore'),
]

# I due modi di camminare per cui il robot e' progettato (D-039): (altezza, distanza del piede) come parametri
MODI = {'alto': ('zam_h', 'zam_xf0'), 'basso': ('zam_h_basso', 'zam_xf0_basso')}
TRIPODI = (('AS', 'PS', 'MD'), ('AD', 'PD', 'MS'))


def _terne(des):
    """{nome: (x, y, angolo in gradi)} delle sei zampe nella terna del robot."""
    v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
    cx, cy, cym = v('cor_coxa_x'), v('cor_coxa_y'), v('cor_coxa_ym')
    a = math.degrees(des.userParameters.itemByName('cor_coxa_ang').value)
    return {'AS': (cx, cy, a), 'MS': (0.0, cym, 90.0), 'PS': (-cx, cy, 180.0 - a),
            'AD': (cx, -cy, -a), 'MD': (0.0, -cym, -90.0), 'PD': (-cx, -cy, a - 180.0)}


def _m_zampa(x, y, ang):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return Z['_matrice']((x, y, 0), (c, s, 0), (-s, c, 0), (0, 0, 1))


def _vicina(occs, x, y, z=None):
    """Occorrenza la cui origine e' piu' vicina al punto dato (mm)."""
    def d(o):
        t = o.transform2.translation
        return math.dist((t.x * 10, t.y * 10) + ((t.z * 10,) if z is not None else ()), (x, y) + ((z,) if z is not None else ()))
    return min(occs, key=d)


def fai_zampe(des, root):
    zs = L['trova_occ'](root, 'Zampa')
    comp = zs[0].component
    terne = _terne(des)
    # addExistingComponent non rispetta la matrice se un'altra istanza ha una posizione non ancora
    # catturata (la nuova nasce composta con quella): prima si creano le istanze mancanti, poi si
    # impostano tutte le posizioni e si cattura. Se le istanze sono appena state create, rilanciare
    # il passo una seconda volta e controllare con "stato".
    for _ in range(len(terne) - len(zs)):
        root.occurrences.addExistingComponent(comp, adsk.core.Matrix3D.create())
    zs = L['trova_occ'](root, 'Zampa')
    for zo, nome in zip(zs, terne):
        zo.transform2 = _m_zampa(*terne[nome])
    if des.snapshots.hasPendingSnapshot:
        des.snapshots.add()
    return {'zampe': len(zs)}


def _attese_corpo(des):
    """Istanze dei componenti comprati dentro Corpo: (chiave, prefisso, matrice nella terna del robot)."""
    v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
    z_orlo = v(C['Z_ORLO_GON'])
    z_cus = v(C['Z_GON']) - v('cus_flangia_sp')
    M = Z['_matrice']
    out = []
    for nome, (x, y, ang) in _terne(des).items():
        mz = _m_zampa(x, y, ang)
        # servo della coxa: albero verso +Z sull'asse, coda verso l'esterno, alette appoggiate sull'orlo
        ms = Z['_matrice']((Z['SERVO_ASSE_X'], 0, z_orlo - Z['SERVO_ALETTE_Y']), (-1, 0, 0), (0, 0, 1), (0, 1, 0))
        ms.transformBy(mz)
        out.append(('servo_' + nome, RIF_SERVO, ms))
        # cuscinetto nel fondo della gondola, flangia sotto
        mc = Z['_matrice']((0, 0, z_cus), (1, 0, 0), (0, 1, 0), (0, 0, 1))
        mc.transformBy(mz)
        out.append(('cus_' + nome, RIF_CUS, mc))
    # --- elettronica (posizioni di progetto, vedi docs/progetto-meccanico.md)
    z_int = v(C['Z_INT'])
    x_batt = v(C['X_VANO1']) - v('bat_gioco_x') - v('bat_l') / 2
    mezzo_giro = ((-1, 0, 0), (0, -1, 0), (0, 0, 1))
    out.append(('batteria', 'Rif_Batteria_2S2200', M((x_batt, 0, z_int), *mezzo_giro)))             # cavi verso la coda
    out.append(('ssc32', 'Rif_SSC32_V25', M((-v('ssc_dx'), 0, v('ssc_z')), *mezzo_giro)))             # morsettiera verso la coda
    out.append(('esp32', 'Rif_ESP32_S3_CAM', M((v('esp_cx'), 0, v('esp_z')), (1, 0, 0), (0, 1, 0), (0, 0, 1))))
    # regolatori in piedi nel muso, di traverso, piazzole di potenza in alto, componenti affacciati
    z_alto = v('reg_w') - v('reg_z_basso')
    x1 = v(C['X_VANO1']) + v('cor_tun') + v('reg_dist')
    x2 = v('cor_xn') - v('cor_parete') - v('reg_dist')
    out.append(('reg_paratia', 'Rif_Reg_Servo', M((x1, v('reg_l') / 2, z_alto), (0, -1, 0), (0, 0, -1), (1, 0, 0))))
    out.append(('reg_muso', 'Rif_Reg_Servo', M((x2, -v('reg_l') / 2, z_alto), (0, 1, 0), (0, 0, -1), (-1, 0, 0))))
    return out


def _istanze_corpo(c):
    return [o for o in c.occurrences if o.component.name.startswith(('Tower Pro', 'Rif_'))]


def _mappa_corpo(des, c):
    libere = _istanze_corpo(c)
    out = {}
    for chiave, pref, m in _attese_corpo(des):
        t = m.translation
        cand = [o for o in libere if o.component.name.startswith(pref)]
        if not cand:
            raise RuntimeError('manca l\'istanza %s' % chiave)
        o = min(cand, key=lambda k: math.dist(k.transform2.translation.asArray(), (t.x, t.y, t.z)))
        libere.remove(o)
        out[chiave] = o
    return out


def fai_istanze(des, root):
    c = C['_corpo'](root).component
    for j in [c.asBuiltJoints.item(i) for i in range(c.asBuiltJoints.count)]:
        j.deleteMe()
    for o in _istanze_corpo(c):
        o.deleteMe()
    lib = lambda pref: [o for o in root.occurrences if o.component.name.startswith(pref)][0]
    t0 = des.timeline.count
    for chiave, pref, m in _attese_corpo(des):
        o_lib = lib(pref)
        if o_lib.isReferencedComponent:
            # Per un riferimento esterno la nuova istanza nasce in m * T_lib (prima la trasformata
            # dell'occorrenza di libreria, nella terna locale, poi m): si passa m * T_lib^-1.
            inv = o_lib.transform2.copy()
            inv.invert()
            inv.transformBy(m)
            m = inv
        occ = c.occurrences.addExistingComponent(o_lib.component, m)
        try:
            if occ.isGroundToParent:
                occ.isGroundToParent = False
        except Exception:
            pass
    L['raggruppa'](des, t0, 'Istanze Corpo')
    return {'istanze': len(_istanze_corpo(c))}


def fai_giunti_corpo(des, root):
    c = C['_corpo'](root).component
    t0 = des.timeline.count
    base = L['trova_occ'](c, 'Corpo_Base')[0]
    for chiave, o in _mappa_corpo(des, c).items():
        inp = c.asBuiltJoints.createInput(o, base, None)
        inp.setAsRigidJointMotion()
        j = c.asBuiltJoints.add(inp)
        j.name = 'R_' + chiave
    L['raggruppa'](des, t0, 'Giunti Corpo')
    return {'giunti': c.asBuiltJoints.count}


def _coxa(zo):
    return [o for o in zo.component.occurrences if o.component.name == 'Coxa'][0].createForAssemblyContext(zo)


def fai_giunti_coxa(des, root):
    v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
    for j in [root.asBuiltJoints.item(i) for i in range(root.asBuiltJoints.count)]:
        if j.name.startswith('G_coxa_'):
            j.deleteMe()
    t0 = des.timeline.count
    corpo = C['_corpo'](root)
    corpo.isGrounded = True
    base = L['trova_occ'](corpo.component, 'Corpo_Base')[0].createForAssemblyContext(corpo)
    zs = L['trova_occ'](root, 'Zampa')
    r = v('cus_sede_d') / 2
    fatti = []
    for nome, (x, y, ang) in _terne(des).items():
        zo = _vicina(zs, x, y)
        faccia = Z['_faccia_cilindrica'](base, r, (x, y, 0), 'z')
        if faccia is None:
            raise RuntimeError('sede del cuscinetto non trovata per ' + nome)
        geo = adsk.fusion.JointGeometry.createByNonPlanarFace(faccia, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)
        inp = root.asBuiltJoints.createInput(_coxa(zo), base, geo)
        inp.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
        j = root.asBuiltJoints.add(inp)
        j.name = 'G_coxa_' + nome
        lim = adsk.fusion.RevoluteJointMotion.cast(j.jointMotion).rotationLimits
        lim.isMinimumValueEnabled = True
        lim.minimumValue = -math.radians(LIMITE_COXA)
        lim.isMaximumValueEnabled = True
        lim.maximumValue = math.radians(LIMITE_COXA)
        fatti.append(j.name)
    L['raggruppa'](des, t0, 'Giunti delle coxe')
    return {'giunti': fatti, 'corpo_fissato': corpo.isGrounded}


def giunti_coxa(root):
    return {j.name[7:]: j for j in [root.asBuiltJoints.item(i) for i in range(root.asBuiltJoints.count)]
            if j.name.startswith('G_coxa_')}


def stato(des, root):
    zs = L['trova_occ'](root, 'Zampa')
    rep = {'zampe': {}, 'giunti': {}}
    for nome, (x, y, ang) in _terne(des).items():
        zo = _vicina(zs, x, y)
        t = zo.transform2
        o, ex, ey, ez = t.getAsCoordinateSystem()
        rep['zampe'][nome] = {'occ': zo.name, 'origine': [round(o.x * 10, 3), round(o.y * 10, 3), round(o.z * 10, 3)],
                              'angolo': round(math.degrees(math.atan2(ex.y, ex.x)), 3), 'atteso': [x, y, ang]}
    for nome, j in giunti_coxa(root).items():
        rep['giunti'][nome] = round(math.degrees(adsk.fusion.RevoluteJointMotion.cast(j.jointMotion).rotationValue), 3)
    corpo = C['_corpo'](root)
    rep['corpo'] = {'fissato': corpo.isGrounded, 'figli': corpo.component.occurrences.count,
                    'giunti': corpo.component.asBuiltJoints.count}
    # scarto (mm) tra posizione attesa e reale di servo e cuscinetti del corpo, e asse reale degli alberi
    attese = {k: m for k, _, m in _attese_corpo(des)}
    scarti = {}
    for chiave, o in _mappa_corpo(des, corpo.component).items():
        px = o.createForAssemblyContext(corpo)
        bb = px.bRepBodies.item(0).boundingBox
        info = {'centro': [round((bb.minPoint.x + bb.maxPoint.x) * 5, 2), round((bb.minPoint.y + bb.maxPoint.y) * 5, 2)],
                'z': [round(bb.minPoint.z * 10, 2), round(bb.maxPoint.z * 10, 2)]}
        if chiave.startswith('servo'):
            for f in px.bRepBodies.item(0).faces:
                g = f.geometry
                if g.surfaceType == adsk.core.SurfaceTypes.CylinderSurfaceType and abs(g.radius * 10 - 5.9) < 1e-3:
                    info['asse_albero'] = [round(g.origin.x * 10, 3), round(g.origin.y * 10, 3)]
        scarti[chiave] = info
    rep['istanze_corpo'] = scarti
    return rep


def interferenze(des, root, solo=None):
    """Interferenze tra le parti di corpo e zampe: [(a, b, volume mm3)]; `solo` limita alle zampe elencate."""
    col = adsk.core.ObjectCollection.create()
    for o in C['_corpo'](root).childOccurrences:
        col.add(o)
    zs = L['trova_occ'](root, 'Zampa')
    for nome, (x, y, ang) in _terne(des).items():
        if solo and nome not in solo:
            continue
        for o in _vicina(zs, x, y).childOccurrences:
            col.add(o)
    res = des.analyzeInterference(des.createInterferenceInput(col))
    out = []
    for i in range(res.count):
        r = res.item(i)
        nomi = []
        for e in (r.entityOne, r.entityTwo):
            occ = getattr(e, 'assemblyContext', None)
            nomi.append(occ.fullPathName if occ else e.parentComponent.name)
        if nomi[0] == nomi[1]:
            continue        # corpi dello stesso ingombro (es. zona delle spine sopra gli header della SSC-32)
        corpi = {r.entityOne.name, r.entityTwo.name}
        if 'uscita_cavi' in corpi and any('Sportello_Coda' in n for n in nomi):
            continue        # il moncone dei cavi della batteria e' simbolico: i cavi veri risalgono nel vano di servizio
        out.append((nomi[0], nomi[1], round(r.interferenceBody.volume * 1000, 2)))
    return out


def scansione_coxe(des, root, zampe=None, angoli=(-45, -30, -15, 15, 30, 45)):
    """Ruota una coxa alla volta (le altre a zero) e cerca interferenze in tutto l'assieme.

    Esito per zampa: una stringa con '.' (libera) o 'X' per ogni angolo, piu' l'elenco delle collisioni.
    Angolo positivo = antiorario visto dall'alto. Alla fine tutti i giunti tornano a zero.
    """
    gj = giunti_coxa(root)
    rep = {'angoli': list(angoli)}
    coll = []
    for nome in (zampe or list(gj)):
        m = adsk.fusion.RevoluteJointMotion.cast(gj[nome].jointMotion)
        riga = ''
        for a in angoli:
            m.rotationValue = math.radians(a)
            if abs(math.degrees(m.rotationValue) - a) > 0.05:
                riga += '?'
                continue
            inter = interferenze(des, root)
            riga += 'X' if inter else '.'
            for i in inter:
                coll.append({'zampa': nome, 'angolo': a, 'tra': [i[0], i[1]], 'mm3': i[2]})
        m.rotationValue = 0
        rep[nome] = riga
    rep['collisioni'] = coll
    return rep


# ----------------------------------------------------------------------------------- pose
# I giunti di femore e ginocchio vivono dentro "Zampa" e via API muovono solo la prima istanza.
# Per atteggiare le sei zampe si impone la trasformata di ogni parte annidata, istanza per istanza,
# calcolata dagli assi dei giunti. La posa resta "non catturata": ripristina() la annulla.
GRUPPO = {'Coxa': 'coxa', 'servo_femore': 'coxa', 'cus_femore': 'coxa', 'perno_coxa': 'coxa',
          'Femore_B': 'femore', 'Femore_A': 'femore', 'perno_anca': 'femore', 'perno_ginocchio': 'femore',
          'Tibia': 'tibia', 'servo_ginocchio': 'tibia', 'cus_ginocchio': 'tibia'}


def ik_zampa(x_f, h, lf, lt):
    """Cinematica inversa nel piano della zampa (come calc/statica_tripode.py): (alpha, gamma) in gradi."""
    d = math.hypot(x_f, h)
    alpha = math.atan2(-h, x_f) + math.acos((lf * lf + d * d - lt * lt) / (2 * lf * d))
    gamma = math.acos((lf * lf + lt * lt - d * d) / (2 * lf * lt))
    return math.degrees(alpha), math.degrees(gamma)


def _rot(gradi, asse, punto_mm):
    m = adsk.core.Matrix3D.create()
    m.setToRotation(math.radians(gradi), adsk.core.Vector3D.create(*asse),
                    P3(punto_mm[0] / 10, punto_mm[1] / 10, punto_mm[2] / 10))
    return m


def _parti_zampa(des, z):
    """{chiave: occorrenza nativa} delle undici parti di Zampa, con la trasformata di riferimento."""
    out = {o.component.name: o for o in z.occurrences if o.component.name in GRUPPO}
    out.update(Z['_mappa'](des, z))
    return out


def posa(des, root, pose, riferimento=None):
    """Atteggia le zampe: pose = {nome: (theta coxa, alpha femore, gamma ginocchio)} in gradi.

    theta positivo = antiorario visto dall'alto; alpha = femore sopra l'orizzontale; gamma = angolo
    interno al ginocchio. `riferimento` = trasformate native a giunti azzerati (se assente si leggono
    ora: i giunti interni devono essere a zero). Ritorna la punta di ogni piede nella terna del robot.
    """
    v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
    lc, lf, lt = v('zam_Lc'), v('zam_Lf'), v('zam_Lt')
    zs = L['trova_occ'](root, 'Zampa')
    parti = _parti_zampa(des, zs[0].component)
    rif = riferimento or {k: o.transform2.copy() for k, o in parti.items()}
    piedi = {}
    for nome, (x, y, ang) in _terne(des).items():
        if nome not in pose:
            continue
        theta, alpha, gamma = pose[nome]
        zo = _vicina(zs, x, y)
        r_coxa = _rot(theta, (0, 0, 1), (0, 0, 0))
        r_anca = _rot(-alpha, (0, 1, 0), (lc, 0, 0))
        r_gin = _rot(-(gamma - 90.0), (0, 1, 0), (lc + lf, 0, 0))
        catene = {'coxa': (r_coxa,), 'femore': (r_anca, r_coxa), 'tibia': (r_gin, r_anca, r_coxa)}
        for chiave, o in parti.items():
            m = rif[chiave].copy()
            for r in catene[GRUPPO[chiave]]:
                m.transformBy(r)
            m.transformBy(zo.transform2)
            o.createForAssemblyContext(zo).transform2 = m
        tib = parti['Tibia'].createForAssemblyContext(zo)
        punta = P3(lt / 10, 0, 0)
        punta.transformBy(tib.transform2)
        piedi[nome] = [round(punta.x * 10, 2), round(punta.y * 10, 2), round(punta.z * 10, 2)]
    return piedi


def ik_piede(des, nome, px, py, pz):
    """(theta, alpha, gamma) in gradi per portare il piede della zampa `nome` nel punto dato (terna del robot, mm)."""
    v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
    cx, cy, ang = _terne(des)[nome]
    theta = (math.degrees(math.atan2(py - cy, px - cx)) - ang + 180.0) % 360.0 - 180.0
    alpha, gamma = ik_zampa(math.hypot(px - cx, py - cy) - v('zam_Lc'), -pz, v('zam_Lf'), v('zam_Lt'))
    return theta, alpha, gamma


def pose_tripode(des, modo, fase):
    """Pose delle sei zampe a una fase (0..1) del ciclo a tripode, nel modo 'alto' o 'basso'.

    Prima meta' del ciclo: tripode A in appoggio (i piedi scorrono all'indietro rispetto al corpo),
    tripode B in volo (i piedi tornano avanti sollevati, con profilo parabolico). Poi i ruoli si scambiano.
    """
    v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
    h, xf0 = v(MODI[modo][0]), v(MODI[modo][1])
    passo, alzata, lc = v('zam_passo'), v('zam_alzata'), v('zam_Lc')
    f = fase % 1.0
    in_appoggio = TRIPODI[0] if f < 0.5 else TRIPODI[1]
    d = -passo / 2 + passo * ((f % 0.5) / 0.5)          # avanzamento del corpo sui piedi in appoggio
    pose = {}
    for nome, (cx, cy, ang) in _terne(des).items():
        r = lc + xf0
        fx, fy = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
        if nome in in_appoggio:
            pose[nome] = ik_piede(des, nome, fx - d, fy, -h)
        else:
            pose[nome] = ik_piede(des, nome, fx + d, fy, -h + alzata * (1 - (2 * d / passo) ** 2))
    return pose


def verifica_ciclo(des, root, modo, fasi):
    """Atteggia il robot alle fasi date del ciclo a tripode e cerca interferenze. Alla fine ripristina."""
    parti = _parti_zampa(des, L['trova_occ'](root, 'Zampa')[0].component)
    rif = {k: o.transform2.copy() for k, o in parti.items()}
    lim = Z['LIMITI']
    rep = {'modo': modo, 'fasi': {}, 'theta': [1e9, -1e9], 'alpha': [1e9, -1e9], 'gamma': [1e9, -1e9]}
    for f in fasi:
        pose = pose_tripode(des, modo, f)
        for th, al, ga in pose.values():
            for k, x in (('theta', th), ('alpha', al), ('gamma', ga)):
                rep[k] = [round(min(rep[k][0], x), 1), round(max(rep[k][1], x), 1)]
        piedi = posa(des, root, pose, rif)
        inter = interferenze(des, root)
        rep['fasi']['%.3f' % f] = {'interferenze': inter, 'z_piedi': sorted({p[2] for p in piedi.values()})}
    rep['dentro_i_limiti'] = (lim['alpha'][0] <= rep['alpha'][0] and rep['alpha'][1] <= lim['alpha'][1]
                              and lim['gamma'][0] <= rep['gamma'][0] and rep['gamma'][1] <= lim['gamma'][1]
                              and -LIMITE_COXA <= rep['theta'][0] and rep['theta'][1] <= LIMITE_COXA)
    ripristina(des)
    return rep


def ripristina(des):
    """Annulla le pose non catturate (torna alla posa salvata)."""
    if des.snapshots.hasPendingSnapshot:
        des.snapshots.revertPendingSnapshot()
    return not des.snapshots.hasPendingSnapshot


def assetto_di_marcia(des):
    """(alpha, gamma) dell'assetto neutro di progetto: piede a x_f0 dall'asse del femore, asse a h da terra."""
    v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
    return ik_zampa(v('zam_xf0'), v('zam_h'), v('zam_Lf'), v('zam_Lt'))


# Massa: le librerie di Fusion non hanno PETG e PLA, quindi parti stampate = volume x densita' x riempimento
# medio (pareti piene, zone massicce con riempimento parziale); componenti comprati = massa a catalogo
# applicata al baricentro geometrico del corpo indicato.
DENSITA = 1.29            # g/cm3, PETG-CF (PETG non caricato 1.27: la differenza e' trascurabile)
STAMPATE = {'Corpo_Base': 0.90, 'Corpo_Guscio': 1.0, 'Vassoio_ESP32': 1.0, 'Sportello_Dorso': 1.0, 'Sportello_Coda': 1.0,
            'Coxa': 0.60, 'Femore_B': 0.70, 'Femore_A': 1.0, 'Tibia': 0.60}
COMPRATE = {'Tower Pro': (13.4, None), 'Rif_Cuscinetto': (0.4, None), 'Rif_Perno': (0.55, None),
            'Rif_Batteria': (120.0, 'pacco'), 'Rif_SSC32': (45.0, 'pcb'), 'Rif_ESP32': (14.0, 'pcb'),
            'Rif_Reg_Servo': (15.0, None)}


def massa(des, root):
    """Massa e baricentro di cio' che e' modellato (mm, g), nella posa corrente."""
    foglie = list(C['_corpo'](root).childOccurrences)
    for zo in L['trova_occ'](root, 'Zampa'):
        foglie += list(zo.childOccurrences)
    voci = {}
    tot = 0.0
    mom = [0.0, 0.0, 0.0]
    for o in foglie:
        nome = o.component.name
        if nome in STAMPATE:
            b = o.bRepBodies.item(0)
            m = b.volume * DENSITA * STAMPATE[nome]
            chiave = nome
        else:
            pref = [k for k in COMPRATE if nome.startswith(k)]
            if not pref:
                continue
            m, corpo_rif = COMPRATE[pref[0]]
            b = ([x for x in o.bRepBodies if x.name == corpo_rif] or [o.bRepBodies.item(0)])[0]
            chiave = pref[0]
        g = b.physicalProperties.centerOfMass
        tot += m
        for i, c in enumerate((g.x, g.y, g.z)):
            mom[i] += m * c * 10
        v = voci.setdefault(chiave, [0, 0.0])
        v[0] += 1
        v[1] += m
    return {'voci': {k: [n, round(m, 1)] for k, (n, m) in voci.items()}, 'totale_g': round(tot, 1),
            'baricentro_mm': [round(c / tot, 2) for c in mom]}


def main(passi, **kw):
    out = {'passi': passi}
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        if 'parametri' in passi:
            out['parametri'] = L['aggiungi_parametri'](des, PARAMETRI)
        if 'zampe' in passi:
            out['zampe'] = fai_zampe(des, root)
        if 'istanze' in passi:
            out['istanze'] = fai_istanze(des, root)
        if 'giunti_corpo' in passi:
            out['giunti_corpo'] = fai_giunti_corpo(des, root)
        if 'giunti_coxa' in passi:
            out['giunti_coxa'] = fai_giunti_coxa(des, root)
        if 'stato' in passi:
            out['stato'] = stato(des, root)
        if 'interferenze' in passi:
            out['interferenze'] = interferenze(des, root, kw.get('solo'))
        if 'massa' in passi:
            out['massa'] = massa(des, root)
        if 'ciclo' in passi:
            out['ciclo'] = verifica_ciclo(des, root, kw.get('modo', 'alto'), kw.get('fasi', (0.0, 0.125, 0.25, 0.375)))
        if 'scansione' in passi:
            out['scansione'] = scansione_coxe(des, root, kw.get('zampe'), kw.get('angoli', (-45, -30, -15, 15, 30, 45)))
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1))
