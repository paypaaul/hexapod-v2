"""Assieme dell'esapode MG996R (fase 4, D-050): corpo, sei zampe, giunti di coxa, componenti nel corpo.

Si esegue dentro Fusion sul design "Hexapod v2 - MG996R", un passo per chiamata:
    import runpy
    def run(_context: str):
        runpy.run_path('/Users/paul/hexapod-v2/cad/script/assieme.py')['main'](['istanze_corpo'])

Passi: istanze_corpo (servo e cuscinetti di coxa, elettronica dentro "Corpo"), zampe (sei istanze di "Zampa"
alla radice), posiziona_zampe (in uno script successivo: trasformate e cattura), giunti_coxa (giunti di
rivoluzione alla radice tra Corpo_Base e la Coxa di ogni istanza), controllo, interferenze, coxe (scansione
dell'imbardata), stato.
Terna del robot: X avanti, Y a sinistra, Z in alto, z = 0 sul piano dei femori.
"""
import json
import math
import os
import runpy
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
L = runpy.run_path(os.path.join(QUI, 'lib_cad.py'))
A = runpy.run_path(os.path.join(QUI, 'lib_assieme.py'))

ZAMPE = ('AS', 'MS', 'PS', 'AD', 'MD', 'PD')
LIMITE_COXA = 35.0          # gradi; il firmware resta entro +-30 e entro 60 di somma tra vicine (D-050)


def _mm(des, expr):
    return des.unitsManager.evaluateExpression(expr, 'mm') * 10.0


def coxe(des):
    """{zampa: (x, y, direzione in gradi)} dai parametri del corpo."""
    ax, ay, my = _mm(des, 'cor_ang_x'), _mm(des, 'cor_ang_y'), _mm(des, 'cor_med_y')
    d = math.degrees(des.unitsManager.evaluateExpression('cor_ang_dir', 'rad'))
    return {'AS': (ax, ay, d), 'MS': (0.0, my, 90.0), 'PS': (-ax, ay, 180.0 - d),
            'AD': (ax, -ay, -d), 'MD': (0.0, -my, -90.0), 'PD': (-ax, -ay, d - 180.0)}


def _rz(x, y, z, gradi):
    c, s = math.cos(math.radians(gradi)), math.sin(math.radians(gradi))
    return A['matrice']((x, y, z), (c, s, 0), (-s, c, 0), (0, 0, 1))


def pose_corpo(des):
    """{chiave: (componente di libreria, matrice nella terna del robot)} per le istanze dentro Corpo."""
    out = {}
    z_al = _mm(des, 'cz_alette_coxa')
    z_cus = -_mm(des, 'cor_fondo') - _mm(des, 'cus_flangia_sp')
    for n, (x, y, d) in coxe(des).items():
        out['Servo_Coxa_' + n] = ('Rif_Servo_MG996R', _rz(x, y, z_al, d))
        out['Cuscinetto_Coxa_' + n] = ('Rif_Cuscinetto_LF1050ZZ', _rz(x, y, z_cus, 0.0))
    fondo_int = -_mm(des, 'cor_chiglia') + _mm(des, 'cor_chiglia_sp')
    x_bat = _mm(des, 'cor_tun_x1') - _mm(des, 'cor_parete') - _mm(des, 'bat_l') / 2
    out['Batteria'] = ('Rif_Batteria_2S5200', _rz(x_bat, 0, fondo_int, 180.0))           # cavi verso la coda
    z_ssc = -_mm(des, 'cor_tetto') + _mm(des, 'ssc_dist')
    out['SSC32'] = ('Rif_SSC32_V25', _rz(_mm(des, 'cor_ssc_x'), 0, z_ssc, 0.0))          # morsettiera in avanti
    z_bas = _mm(des, 'cor_vas_z') + _mm(des, 'cor_vas_sp') + _mm(des, 'cor_bas_luce')
    out['Basetta'] = ('Rif_Basetta_50x70', _rz(_mm(des, 'cor_bas_x0') + _mm(des, 'bas_l') / 2, 0, z_bas, 0.0))
    out['ESP32'] = ('Rif_ESP32_S3_CAM', _rz(45.0, 0, 16.0, 0.0))                         # antenna in avanti, punta a x 81 (torretta della camera da x 82)
    # camera girata di 180 gradi sull'asse ottico: il flat esce dall'alto della testa e torna verso l'ESP32 sopra la torretta
    out['Camera'] = ('Rif_Camera_OV3660_75', A['matrice']((_mm(des, 'cor_cam_x'), 0, _mm(des, 'cor_cam_z')), (0, 0, -1), (0, 1, 0), (1, 0, 0)))
    # vano di coda sul tetto: fusibile F1 di traverso dietro, T-plug davanti a lui; Wago sotto il vassoio, ingressi verso l'esterno
    zt = -_mm(des, 'cor_tetto')
    x_coda = -_mm(des, 'cor_tun_x0')
    out['Portafusibile_F1'] = ('Rif_Portafusibile_ATO', _rz(x_coda + 2 + _mm(des, 'fus_w') / 2, 0, zt, 90.0))
    # la coppia di T-plug sta nella zona dei cavi dietro il pacco: si stacca aprendo lo sportello della batteria
    # coppia di T-plug sopra il portafusibile, nel vano di coda: si raggiunge dal retro
    out['Tplug'] = ('Rif_Tplug', _rz(x_coda + 2 + _mm(des, 'fus_w') / 2, 0, zt + _mm(des, 'fus_h'), 90.0))
    # Wago in piedi sul ripiano delle baie posteriori: ingressi dei fili in alto, leve verso la parete della baia
    # (sdraiati avevano gli ingressi a 1,4 mm dalla parete); si raggiungono togliendo il coperchio
    z_w = -_mm(des, 'cor_fondo') + _mm(des, 'cor_ripiano') + _mm(des, 'wago_w') / 2
    y_w, x_w = _mm(des, 'cor_tun_semi') + _mm(des, 'cor_wago_luce'), -_mm(des, 'cor_wago_x')
    out['Wago_piu'] = ('Rif_Wago_221_415', A['matrice']((x_w, y_w, z_w), (-1, 0, 0), (0, 0, 1), (0, 1, 0)))
    out['Wago_meno'] = ('Rif_Wago_221_415', A['matrice']((x_w, -y_w, z_w), (1, 0, 0), (0, 0, 1), (0, -1, 0)))
    # regolatori sulla parete esterna della baia, componenti verso il tunnel, piazzole in alto
    y_reg = _mm(des, 'cor_baia_y') - _mm(des, 'cor_parete') - _mm(des, 'cor_reg_dist')
    x0, z1, lr = _mm(des, 'cor_reg_x0'), _mm(des, 'cor_reg_ztop'), _mm(des, 'reg_l')
    out['Regolatore_S'] = ('Rif_Reg_Servo_D42V110F6', A['matrice']((x0 + lr, y_reg, z1), (-1, 0, 0), (0, 0, -1), (0, -1, 0)))
    out['Regolatore_D'] = ('Rif_Reg_Servo_D42V110F6', A['matrice']((x0, -y_reg, z1), (1, 0, 0), (0, 0, -1), (0, 1, 0)))
    # cicalino sotto il carapace in coda (lato da 40 lungo Y, pin verso la coda) e pulsante sull'asse del dorso
    out['Cicalino'] = ('Rif_Cicalino_BX100', _rz((_mm(des, 'cic_x0') + _mm(des, 'cic_x1')) / 2, 0, _mm(des, 'cic_z0'), 90.0))
    out['Pulsante'] = ('Rif_Pulsante_12', _rz(_mm(des, 'car_puls_x'), 0, _mm(des, 'car_top'), 0.0))
    return out


def _corpo(root):
    return L['trova_occ'](root, 'Corpo')[0]


def _istanze_corpo(corpo):
    des = corpo.component.parentDesign
    occ = {}
    rif = [o for o in corpo.component.occurrences if o.component.name.startswith('Rif_')]
    for chiave, (lib, m) in pose_corpo(des).items():
        cand = [o for o in rif if o.component.name == lib]
        t = m.translation
        occ[chiave] = A['piu_vicina'](cand, (t.x * 10, t.y * 10, t.z * 10)) if cand else None
    return occ


def fai_istanze_corpo(des, root):
    corpo = _corpo(root)
    lib = {o.component.name: o for o in root.occurrences if o.component.name.startswith('Rif_')}
    for o in [o for o in corpo.component.occurrences if o.component.name.startswith('Rif_')]:
        o.deleteMe()
    fatte = []
    for chiave, (nome_lib, m) in pose_corpo(des).items():
        o = A['aggiungi_istanza'](root, lib[nome_lib], m, dentro=corpo)
        fatte.append(chiave)
    # aggiungi_istanza lascia alla radice copie nascoste dei componenti di libreria: si cancellano
    for o in [o for o in root.occurrences if o.component.name.startswith('Rif_') and o.transform2.translation.y * 10 < 249]:
        o.deleteMe()
    # slitta del regolatore destro: copia della sinistra girata di 180 gradi attorno all'asse verticale del suo centro
    sl = [o for o in corpo.component.occurrences if o.component.name == 'Corpo_Slitta_Regolatore']
    for o in sl[1:]:
        o.deleteMe()
    if sl:
        xc = _mm(des, 'cor_reg_x0') + _mm(des, 'reg_l') / 2
        m = adsk.core.Matrix3D.create()
        m.setToRotation(math.pi, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(xc / 10, 0, 0))
        corpo.component.occurrences.addExistingComponent(sl[0].component, m)
        fatte.append('Slitta_Reg_D')
    for o in corpo.childOccurrences:
        o.isLightBulbOn = True
    return fatte


def controllo_corpo(des, root):
    corpo = _corpo(root)
    occ = _istanze_corpo(corpo)
    out = {}
    for chiave, (lib, m) in pose_corpo(des).items():
        o = occ.get(chiave)
        if o is None:
            out[chiave] = 'assente'
            continue
        a, b = o.transform2.asArray(), m.asArray()
        out[chiave] = round(max(abs(x - y) * (10 if i % 4 == 3 else 1) for i, (x, y) in enumerate(zip(a, b))), 4)
    return out


# ----------------------------------------------------------------------------------- zampe
def _zampe(root):
    return [o for o in root.occurrences if o.component.name == 'Zampa']


def fai_zampe(des, root):
    """Porta a sei le istanze di Zampa alla radice (la prima e' quella gia' esistente)."""
    z = _zampe(root)
    comp = z[0].component
    while len(z) < 6:
        root.occurrences.addExistingComponent(comp, adsk.core.Matrix3D.create())
        z = _zampe(root)
    return len(z)


def posiziona_zampe(des, root):
    """Assegna le istanze alle zampe nell'ordine di root.occurrences e ne imposta la posa; cattura la posizione."""
    z = _zampe(root)
    for o, (n, (x, y, d)) in zip(z, coxe(des).items()):
        o.transform2 = _rz(x, y, 0.0, d)
        o.isLightBulbOn = True
    if des.snapshots.hasPendingSnapshot:
        des.snapshots.add()
    return [o.name for o in z]


def mappa_zampe(des, root):
    """{zampa: occorrenza} abbinando ogni istanza all'asse di coxa piu' vicino."""
    out = {}
    z = _zampe(root)
    for n, (x, y, d) in coxe(des).items():
        out[n] = A['piu_vicina'](z, (x, y, 0.0))
    return out


def fai_giunti_coxa(des, root):
    base = [o for o in _corpo(root).childOccurrences if o.component.name == 'Corpo_Base'][0]
    for j in list(root.asBuiltJoints):
        if j.name.startswith('G_coxa_'):
            j.deleteMe()
    fatti = []
    r = _mm(des, 'perno_foro') / 2
    for n, zo in mappa_zampe(des, root).items():
        x, y, d = coxe(des)[n]
        coxa = [o for o in zo.childOccurrences if o.component.name == 'Coxa'][0]
        f = A['faccia_cilindrica'](coxa, r, (x, y, 0.0), 'z')
        if f is None:
            raise RuntimeError('foro del perno della coxa non trovato per %s' % n)
        A['giunto_rivoluzione'](root, coxa, base, f, 'G_coxa_' + n, (-LIMITE_COXA, LIMITE_COXA))
        fatti.append('G_coxa_' + n)
    corpo = _corpo(root)
    corpo.isGrounded = True
    return fatti


def imposta_coxe(root, angoli):
    """angoli = {zampa: gradi}; ritorna i valori letti."""
    out = {}
    for j in root.asBuiltJoints:
        if j.name.startswith('G_coxa_'):
            n = j.name[len('G_coxa_'):]
            if n in angoli:
                adsk.fusion.RevoluteJointMotion.cast(j.jointMotion).rotationValue = math.radians(angoli[n])
            out[n] = round(A['valore_giunto'](j), 2)
    return out


# ----------------------------------------------------------------------------------- controlli
def _voluta(corpo_a, corpo_b, a, b):
    """Sovrapposizioni volute o fittizie: squadretta piena sul millerighe, ingombri di spine e flat della camera."""
    nomi = {a.split('+')[-1].split(':')[0], b.split('+')[-1].split(':')[0]}
    if nomi == {'Rif_Servo_MG996R', 'Rif_Squadretta_25T'}:
        return True
    if corpo_a in ('flat', 'linguetta', 'uscita_cavi') or corpo_b in ('flat', 'linguetta', 'uscita_cavi'):
        return True
    return False


def interferenze(des, root):
    occ = [o for o in root.occurrences if not o.component.name.startswith('Rif_')]
    res = A['interferenze'](des, occ, scarta=_voluta)
    return [(a.split('+')[-2:] and '+'.join(a.split('+')[-2:]), '+'.join(b.split('+')[-2:]), v) for a, b, v in res]


def scansione_coxe(des, root, zampe, angoli):
    """Una zampa alla volta (le altre a zero) a ciascun angolo; poi coppie di vicine verso l'altra."""
    out = {}
    for n in zampe:
        for a in angoli:
            imposta_coxe(root, {n: a})
            r = interferenze(des, root)
            out['%s %+g' % (n, a)] = r if r else 'libera'
            imposta_coxe(root, {n: 0.0})
    return out


# ----------------------------------------------------------------------------------- ciclo a tripode
SEGUONO_FEMORE = ('Femore_B', 'Femore_A', 'Ingombro_Teste_A', 'Cover_Femore_A', 'Cover_Femore_B')   # piu' le copie con origine sul femore (squadrette, perni)
SEGUONO_TIBIA = ('Tibia', 'Cover_Tibia')


def _gruppo(des, o):
    """'coxa', 'femore' o 'tibia': a quale segmento appartiene una parte annidata nella Zampa (terna della zampa)."""
    n = o.component.name
    if n in SEGUONO_FEMORE:
        return 'femore'
    if n in SEGUONO_TIBIA:
        return 'tibia'
    lc, lf = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lf')
    t = o.transform2.translation
    x, y = t.x * 10, t.y * 10
    if n == 'Rif_Servo_MG996R' or n == 'Rif_Cuscinetto_LF1050ZZ':
        return 'tibia' if abs(x - (lc + lf)) < 1 else 'coxa'
    if n in ('Rif_Squadretta_25T', 'Rif_Perno_5'):
        if abs(x) < 1:
            return 'coxa'
        return 'femore'
    return 'coxa'


def _rot_y(gradi, x0):
    m = adsk.core.Matrix3D.create()
    m.setToRotation(math.radians(gradi), adsk.core.Vector3D.create(0, 1, 0), adsk.core.Point3D.create(x0 / 10, 0, 0))
    return m


def _rot_z(gradi):
    m = adsk.core.Matrix3D.create()
    m.setToRotation(math.radians(gradi), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
    return m


def posa_zampa(des, zo, imbardata, alpha, gamma):
    """Atteggia UNA istanza di Zampa imponendo le trasformate delle parti annidate (la posa resta non catturata)."""
    lc, lf = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lf')
    for o in zo.component.occurrences:
        g = _gruppo(des, o)
        m = o.transform2.copy()                       # nativa = posa "come costruito" nella terna della zampa
        if g == 'tibia':
            m.transformBy(_rot_y(90.0 - gamma, lc + lf))
        if g in ('tibia', 'femore'):
            m.transformBy(_rot_y(-alpha, lc))
        m.transformBy(_rot_z(imbardata))
        m.transformBy(zo.transform2)
        o.createForAssemblyContext(zo).transform2 = m


def pose_tripode(des, h, xf0, passo, alzata, fase, giro=0.0):
    """{zampa: (imbardata, alpha, gamma)} alla fase 0..1 del ciclo; tripode A (AS, PS, MD) in appoggio nella prima meta'.

    Con giro (gradi di rotazione del corpo a ogni passo, positivo antiorario) i piedi si spostano su archi attorno al
    centro del corpo invece che lungo X: rotazione sul posto.
    """
    st = runpy.run_path(os.path.join(os.path.dirname(QUI), '..', 'calc', 'statica_tripode.py'))
    lc, lf, lt = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lf'), _mm(des, 'zam_Lt')
    out = {}
    for n, (x, y, d) in coxe(des).items():
        fx = x + (lc + xf0) * math.cos(math.radians(d))
        fy = y + (lc + xf0) * math.sin(math.radians(d))
        a_tripode = n in ('AS', 'PS', 'MD')
        u = fase if a_tripode else (fase + 0.5) % 1.0
        if u < 0.5:                                   # appoggio: il piede va da +passo/2 a -passo/2
            k, dz = 0.5 - u / 0.5, 0.0
        else:                                         # volo: torna avanti alzandosi
            v = (u - 0.5) / 0.5
            k, dz = -0.5 + v, alzata * math.sin(math.pi * v)
        if giro:                                      # nella terna del corpo il piede in appoggio gira in senso opposto al corpo
            r = math.radians(giro * k)
            fx, fy = fx * math.cos(r) - fy * math.sin(r), fx * math.sin(r) + fy * math.cos(r)
            dx = 0.0
        else:
            dx = passo * k
        px, py = fx + dx - x, fy - y
        yaw = math.degrees(math.atan2(py, px)) - d
        yaw = (yaw + 180) % 360 - 180
        x_f = math.hypot(px, py) - lc
        s = st['ik_piano'](x_f, h - dz, lf, lt)
        out[n] = (round(yaw, 2), round(s[0], 2), round(s[3], 2)) if s else None
    return out


def verifica_ciclo(des, root, h, xf0, passo, alzata, fasi, giro=0.0):
    out = {}
    zampe = mappa_zampe(des, root)
    for f in fasi:
        pose = pose_tripode(des, h, xf0, passo, alzata, f, giro)
        if any(v is None for v in pose.values()):
            out['%g' % f] = {'pose': pose, 'esito': 'piede non raggiungibile'}
            continue
        for n, (yaw, a, g) in pose.items():
            posa_zampa(des, zampe[n], yaw, a, g)
        r = interferenze(des, root)
        out['%g' % f] = {'pose': pose, 'urti': r if r else 'nessuno'}
        A['ripristina'](des)
    return out


# ----------------------------------------------------------------------------------- carapace (D-061, specifica 5.4-5.8)
GRUPPO_CARAPACE = ('Corpo_Carapace', 'Corpo_Fascia', 'Corpo_Visiera', 'Corpo_Gonne', 'Corpo_Sportello_Servizio')
SALGONO_COL_CARAPACE = GRUPPO_CARAPACE + ('Rif_Cicalino_BX100', 'Rif_Pulsante_12')


def _occ_carapace(root, nomi=GRUPPO_CARAPACE):
    return [o for o in _corpo(root).childOccurrences if o.component.name in nomi]


def carapace_zampe(des, root, zampe, imbardate, pose):
    """Una zampa atteggiata alla volta contro il gruppo del carapace: interferenze e distanza minima del carapace da
    femore e lame. Le altre zampe restano nella posa di riferimento."""
    out = {}
    mz = mappa_zampe(des, root)
    car = _occ_carapace(root)
    guscio = [b for o in car if o.component.name == 'Corpo_Carapace' for b in o.bRepBodies]
    mm = adsk.core.Application.get().measureManager
    for n in zampe:
        zo = mz[n]
        for yaw in imbardate:
            for a, g in pose:
                posa_zampa(des, zo, yaw, a, g)
                r = A['interferenze'](des, car + [zo], scarta=_voluta)
                urti = sorted(set('%s/%s' % (x[0].split('+')[-1], x[1].split('+')[-1]) for x in r))
                dmin = None
                for o in zo.childOccurrences:
                    if o.component.name in ('Femore_A', 'Femore_B', 'Cover_Femore_A', 'Cover_Femore_B', 'Ingombro_Teste_A'):
                        for b in o.bRepBodies:
                            for cb in guscio:
                                d = mm.measureMinimumDistance(b, cb).value * 10
                                dmin = d if dmin is None else min(dmin, d)
                out['%s %+g %g/%g' % (n, yaw, a, g)] = {'urti': urti or 'nessuno', 'dmin_mm': round(dmin, 2)}
                A['ripristina'](des)
    return out


def sfilamento(des, root, quote):
    """Il carapace (con fascia, visiera, gonne, sportellino, cicalino e pulsante) sollevato di dz mm: interferenze."""
    out = {}
    occ = _occ_carapace(root, SALGONO_COL_CARAPACE)
    for dz in quote:
        for o in occ:
            m = o.transform2.copy()
            t = adsk.core.Matrix3D.create()
            t.translation = adsk.core.Vector3D.create(0, 0, dz / 10)
            m.transformBy(t)
            o.transform2 = m
        r = interferenze(des, root)
        out['%+g' % dz] = r if r else 'nessuna'
        A['ripristina'](des)
    return out


def campo(des, root, piu_gradi=0.0):
    """Campo della camera: tronco di piramide da un quadrato 7 x 7 sulla lente, con le semiaperture 54,2 e 46,1 gradi
    (piu' piu_gradi), lungo 15 mm, in un componente provvisorio; interferenze con il gruppo del carapace, poi lo cancella."""
    lib = runpy.run_path(os.path.join(QUI, 'lib_cad.py'))
    x0 = _mm(des, 'cor_cam_x') + _mm(des, 'cam_alt')
    zc = _mm(des, 'cor_cam_z')
    th, tv = (math.radians(des.userParameters.itemByName(n).value * 180 / math.pi + piu_gradi) for n in ('cam_fov_h', 'cam_fov_v'))
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = 'Prova_Campo'
    try:
        p = lib['Parte'](occ.component)
        a = p.sk_rett('x', '%.4f mm' % x0, 'bocca', '-3.5 mm', '%.4f mm' % (zc - 3.5), '3.5 mm', '%.4f mm' % (zc + 3.5))
        sy, sz = 3.5 + 15 * math.tan(th), 3.5 + 15 * math.tan(tv)
        b = p.sk_rett('x', '%.4f mm' % (x0 + 15), 'fondo', '%.4f mm' % -sy, '%.4f mm' % (zc - sz), '%.4f mm' % sy, '%.4f mm' % (zc + sz))
        lo = occ.component.features.loftFeatures
        li = lo.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        li.loftSections.add(a.profiles.item(0))
        li.loftSections.add(b.profiles.item(0))
        li.isSolid = True
        lo.add(li)
        r = A['interferenze'](des, _occ_carapace(root) + [occ])
        return {'piu_gradi': piu_gradi, 'urti': [(x[0].split('+')[-1], x[1].split('+')[-1], x[2]) for x in r] or 'nessuno'}
    finally:
        occ.deleteMe()


def stato(des, root):
    out = {'zampe': {n: o.name for n, o in mappa_zampe(des, root).items()},
           'giunti_coxa': {j.name: round(A['valore_giunto'](j), 2) for j in root.asBuiltJoints if j.name.startswith('G_coxa_')},
           'snapshot_pendente': des.snapshots.hasPendingSnapshot}
    return out


def main(passi, **kw):
    out = {'passi': passi}
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        if not app.activeDocument.name.startswith('Hexapod v2 - MG996R'):
            raise RuntimeError('documento attivo "%s"' % app.activeDocument.name)
        root = des.rootComponent
        if 'istanze_corpo' in passi:
            out['istanze_corpo'] = fai_istanze_corpo(des, root)
        if 'controllo' in passi:
            out['controllo'] = controllo_corpo(des, root)
        if 'zampe' in passi:
            out['zampe'] = fai_zampe(des, root)
        if 'posiziona_zampe' in passi:
            out['posiziona_zampe'] = posiziona_zampe(des, root)
        if 'giunti_coxa' in passi:
            out['giunti_coxa'] = fai_giunti_coxa(des, root)
        if 'interferenze' in passi:
            out['interferenze'] = interferenze(des, root)
        if 'coxe' in passi:
            out['coxe'] = scansione_coxe(des, root, kw.get('zampe', ZAMPE), kw.get('angoli', (-35, -20, 20, 35)))
        if 'ciclo' in passi:
            out['ciclo'] = verifica_ciclo(des, root, kw.get('h', 100.0), kw.get('xf0', 45.0), kw.get('passo', 60.0),
                                          kw.get('alzata', 30.0), kw.get('fasi', (0.0, 0.25)), kw.get('giro', 0.0))
        if 'carapace_zampe' in passi:
            out['carapace_zampe'] = carapace_zampe(des, root, kw['zampe'], kw.get('imbardate', (-35.0, 0.0, 35.0)),
                                                   kw.get('pose', ((85.0, 90.0), (85.0, 29.0), (60.0, 90.0))))
        if 'sfilamento' in passi:
            out['sfilamento'] = sfilamento(des, root, kw.get('quote', (5.0, 10.0, 20.0, 40.0)))
        if 'campo' in passi:
            out['campo'] = campo(des, root, kw.get('piu_gradi', 0.0))
        if 'ripristina' in passi:
            out['ripristina'] = A['ripristina'](des)
        if 'stato' in passi:
            out['stato'] = stato(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
