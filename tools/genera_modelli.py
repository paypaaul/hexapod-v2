"""Modelli del robot generati dalla descrizione unica (tools/descrizione.py: robot.yaml + cad.json + mesh):

- robot/generati/esapode.urdf, per il gemello nel browser (app/), Rerun ed eventualmente ROS 2;
- sim/modello/esapode.xml, MJCF per MuJoCo (sim/).

Un link per il corpo e tre per zampa (coxa, femore, tibia), piu' la punta del piede e l'IMU come terne fisse. Giunti
con lo zero nella posa "come costruita" del CAD (imbardata 0, alpha 0, gamma 90):

    g_coxa_<z>      q = imbardata       asse +Z della zampa
    g_femore_<z>    q = alpha           asse -Y: alpha positivo alza il femore
    g_ginocchio_<z> q = gamma - 90      asse -Y: gamma che cresce apre la tibia verso l'esterno

Unita' SI nei modelli (m, kg, kg m2, rad); la descrizione e' in mm, g, gradi. Le sei zampe sono la stessa zampa ruotata
attorno a Z della direzione della coxa, come nel CAD (cad.json -> terne).

Il ginocchio minimo che dipende dal femore (cad.json -> limiti_meccanici.gamma_min) non sta nei modelli: lo applica la
guardia, uguale nel firmware e nel simulatore (software.md 6.2). Nei modelli ci sono solo i fine corsa meccanici.

    python3 tools/genera_modelli.py              # scrive i due file
    python3 tools/genera_modelli.py --controlla  # esce con 1 se i file della repo non sono quelli generati

L'uscita e' deterministica: stessi ingressi, stessi byte (numeri arrotondati, nessuna data).
"""
import math
import os
import sys
import xml.etree.ElementTree as ET

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
from descrizione import REPO, Descrizione  # noqa: E402

USCITA_URDF = os.path.join('robot', 'generati', 'esapode.urdf')
USCITA_MJCF = os.path.join('sim', 'modello', 'esapode.xml')
SEGMENTI = ('corpo', 'coxa', 'femore', 'tibia')
G = 9.80665                      # m/s2, per kgf -> N

# Saturazione del servo: errore di posizione al quale l'amplificatore da' la coppia di stallo. Il datasheet non da' il
# guadagno: 5 gradi e' un valore di partenza (S), da sostituire con l'identificazione (software.md 4.6). Con il femore
# al 51 % dello stallo (punto di progetto 100/45) il servo cede circa 2,5 gradi.
SATURAZIONE_GRADI = 5.0

# Attrito del piedino in TPU sul pavimento: centro del campo di randomizzazione 0,4-1,2 (software.md 4.4), S.
ATTRITO = 0.8

# Rigidezza dei contatti (solref: costante di tempo, smorzamento critico). Con il valore di MuJoCo (0,02 s) il robot da
# 2,9 kg affonda di qualche millimetro nel pavimento e i piedi in appoggio strisciano (prova del 9 ottobre 2026: 12 mm a
# passo invece di 5). 5 ms e' 2,5 volte il passo di 2 ms, sopra il minimo di 2 passi indicato da MuJoCo: il contatto
# piu' rigido che resta stabile, adatto a un piedino in TPU di 1,6 mm su un pavimento duro (S).
CONTATTO_SOLREF = '0.005 1'

# IMU (predisposizioni.md, X4): sul tetto del tunnel, nel vano sotto il vassoio (x 34...71, sull'asse), su due bugne
# alte 2 mm, scheda Pololu spessa 3 mm. La x esatta non e' ancora fissata nel CAD (C): centro del vano.
IMU_X_MM = (34.0 + 71.0) / 2
IMU_SOPRA_TETTO_MM = 2.0 + 3.0 / 2


# ------------------------------------------------------------------------------------------------ numeri e matrici
def num(x, cifre=6):
    """Numero in testo a cifre decimali fisse, senza zeri in coda e senza "-0": stessa uscita su ogni piattaforma."""
    s = '%.*f' % (cifre, x)
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def sig(x, cifre=6):
    """Numero con cifre significative (inerzie, che vanno da 1e-9 a 1e-2)."""
    if abs(x) < 1e-12:
        return '0'
    return '%.*g' % (cifre, x)


def vet(v, cifre=6):
    return ' '.join(num(x, cifre) for x in v)


def _somma_inerzie(parti):
    """Massa, baricentro e inerzia attorno al baricentro di un insieme di parti [(m, c, I)], con il trasporto (Huygens-
    Steiner). Python puro e somme in ordine fisso: stessi bit su ogni piattaforma."""
    M = 0.0
    s = [0.0, 0.0, 0.0]
    for m, c, _ in parti:
        M += m
        for k in range(3):
            s[k] += m * c[k]
    C = [s[k] / M for k in range(3)]
    J = [[0.0] * 3 for _ in range(3)]
    for m, c, inerzia in parti:
        r = [c[k] - C[k] for k in range(3)]
        r2 = r[0] * r[0] + r[1] * r[1] + r[2] * r[2]
        for i in range(3):
            for j in range(3):
                J[i][j] += inerzia[i][j] + m * ((r2 if i == j else 0.0) - r[i] * r[j])
    return M, C, J


# ------------------------------------------------------------------------------------------------ dalla descrizione
def origini_segmenti(d):
    """Origine di ogni link nella terna in cui cad.json da' le parti (robot per il corpo, zampa per gli altri)."""
    return {'corpo': (0.0, 0.0, 0.0), 'coxa': (0.0, 0.0, 0.0), 'femore': (d.Lc, 0.0, 0.0),
            'tibia': (d.Lc + d.Lf, 0.0, 0.0)}


def segmenti(d):
    """{segmento: (massa g, baricentro mm nella terna del link, inerzia g mm2 attorno al baricentro)}.

    Somma le parti di cad.json -> parti per segmento. Il non modellato (cavi, viteria: cad.json -> masse) va sul corpo
    distribuito come il corpo: massa e inerzia scalate dello stesso fattore, baricentro invariato.
    """
    origini = origini_segmenti(d)
    per = {s: [] for s in SEGMENTI}
    for nome in sorted(d.cad['parti']):
        p = d.cad['parti'][nome]
        per[p['segmento']].append((p['massa_g'], p['baricentro_mm'], p['inerzia_gmm2']))
    out = {}
    for s in SEGMENTI:
        M, C, J = _somma_inerzie(per[s])
        atteso = d.cad['masse']['segmenti_g'][s]
        if abs(M - atteso) > 0.15:
            raise ValueError('massa del segmento %s: somma delle parti %.2f g, cad.json -> masse %.2f g'
                             % (s, M, atteso))
        o = origini[s]
        out[s] = (M, [C[k] - o[k] for k in range(3)], J)
    if d.yaml['massa'].get('non_modellato_sul_corpo'):
        M, C, J = out['corpo']
        f = (M + d.cad['masse']['non_modellato_g']) / M
        out['corpo'] = (M * f, C, [[x * f for x in r] for r in J])
    return out


def leggi_stl(percorso):
    """Vertici (n, 3, 3) di un STL binario, in mm."""
    with open(percorso, 'rb') as f:
        f.read(80)
        n = int(np.frombuffer(f.read(4), '<u4')[0])
        tipo = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
        return np.frombuffer(f.read(n * 50), tipo)['v'].astype(np.float64)


def _scatola(v):
    """(centro, semilati) del parallelepipedo che contiene i vertici v (n, 3)."""
    lo, hi = v.min(0), v.max(0)
    return [float(x) for x in (lo + hi) / 2], [float(x) for x in (hi - lo) / 2]


def urti(d):
    """Primitive di collisione per segmento, in mm nella terna del link. Quote dai parametri di cad.json e dalle mesh.

    Le primitive stanno dentro o a filo della forma vera dove una zampa puo' avvicinarsi (un urto finto fermerebbe la
    prova) e la coprono dove conta per le cadute (chiglia). Restano fuori le gondole e le alette dei servo di coxa, che
    stanno sotto la coxa: li' i contatti li esclude il CAD con i limiti della guardia.
    """
    p = {k: v['valore'] for k, v in d.cad['parametri'].items()}
    mesh = {s: leggi_stl(os.path.join(d.cartella, 'mesh', s + '.stl')).reshape(-1, 3) for s in SEGMENTI}
    o = origini_segmenti(d)
    out = {s: [] for s in SEGMENTI}

    # corpo: chiglia (sotto il fondo della base e le flange dei cuscinetti di coxa), scafo fra le coxe, carapace con i
    # lobi esagonali sulle coxe
    c = mesh['corpo']
    chi = c[c[:, 2] < -p['cor_fondo'] - p['cus_flangia_sp'] - 0.05]
    x0, x1 = float(chi[:, 0].min()), float(chi[:, 0].max())
    y1 = float(np.abs(chi[:, 1]).max())
    z0, z1 = -p['cor_chiglia'], -p['cor_fondo']
    out['corpo'].append(('chiglia', 'box', [(x0 + x1) / 2, 0.0, (z0 + z1) / 2], [(x1 - x0) / 2, y1, (z1 - z0) / 2]))
    z0, z1 = -p['cor_fondo'], p['cor_orlo']
    out['corpo'].append(('scafo', 'box', [(x0 + x1) / 2, 0.0, (z0 + z1) / 2],
                         [(x1 - x0) / 2, p['cor_med_y'], (z1 - z0) / 2]))
    z0, z1 = p['cor_orlo'], p['car_top']
    x0, x1 = -p['car_coda_x'], p['car_viso_x']
    out['corpo'].append(('carapace', 'box', [(x0 + x1) / 2, 0.0, (z0 + z1) / 2],
                         [(x1 - x0) / 2, p['car_valle_y'], (z1 - z0) / 2]))
    for n in d.zampe:
        x, y, _ = d.coxe[n]
        out['corpo'].append(('lobo_' + n, 'cylinder', [x, y, (z0 + z1) / 2], [p['car_lobo_R'], (z1 - z0) / 2]))

    # coxa: la culla del servo del femore, la sola parte larga piu' di +-15 mm (il braccio verso il corpo e' +-9,4)
    cx = mesh['coxa']
    culla = cx[np.abs(cx[:, 1]) > 15.0]
    centro, semi = _scatola(culla)
    out['coxa'].append(('coxa_culla', 'box', centro, semi))
    z_culla = centro[2] - semi[2]

    # femore: due capsule, una per fianco (Femore_A/B con le placche); raggio = semialtezza delle teste sugli assi
    f = mesh['femore']
    teste = f[(np.abs(f[:, 0] - d.Lc) < 1.0) | (np.abs(f[:, 0] - d.Lc - d.Lf) < 1.0)]
    r_f = float(np.abs(teste[:, 2]).max())
    y_c = float(np.abs(f[:, 1]).max()) - r_f
    for lato, s in (('A', 1.0), ('B', -1.0)):
        out['femore'].append(('femore_' + lato, 'capsule', [[0.0, s * y_c, 0.0], [d.Lf, s * y_c, 0.0]], r_f))

    # tibia: culla del servo del ginocchio (stessa culla della coxa, fino alla stessa quota), stinco e piede
    t = mesh['tibia']
    centro, semi = _scatola(t[t[:, 2] >= z_culla])
    ot = o['tibia']
    centro = [centro[k] - ot[k] for k in range(3)]
    out['tibia'].append(('tibia_culla', 'box', centro, semi))
    r_p = p['tib_x_meno_basso'] + p['tib_piede_sp']        # meta' della suola lungo X: stinco 8 mm + TPU 1,6 per lato
    z_p = -d.Lt + r_p
    # lo stinco finisce al bordo basso del guscio, sopra il piedino: con la tibia inclinata fino a circa 50 gradi tocca
    # terra prima la sfera del piede
    out['tibia'].append(('tibia_stinco', 'capsule', [[centro[0], 0.0, z_culla], [0.0, 0.0, -p['cov_tib_z1']]],
                         p['cov_tib_y_semi_basso']))
    out['tibia'].append(('piede', 'sphere', [0.0, 0.0, z_p], r_p))
    return out


def servo(d):
    """Parametri dell'attuatore di posizione, in SI, con la loro origine."""
    s = d.yaml['servo']
    v = s['tensione_rail']
    stallo = s['stallo_kgfcm'][v] * G / 100.0                 # N m
    w0 = math.radians(60.0) / s['velocita_s_60'][v]           # rad/s a vuoto
    return {
        'stallo_nm': stallo,
        'velocita_rad_s': w0,
        # retta coppia-velocita' del motore a piena tensione: stallo a velocita' zero, zero alla velocita' a vuoto
        'smorzamento': stallo / w0,
        'kp': stallo / math.radians(SATURAZIONE_GRADI),
        # il datasheet da' la larghezza della banda morta (5 us): il servo non reagisce entro meta' banda per parte
        'semibanda_morta_rad': math.radians(s['banda_morta_us'] / 2.0 / s['us_per_grado']),
    }


def campi_comando(d):
    """Campo del comando di ogni giunto (gradi, in q): la corsa che l'SSC-32 puo' comandare, 500-2500 us."""
    s = d.yaml['servo']
    semi = 1000.0 / s['us_per_grado']
    cal = s['calettamento']
    return {'coxa': (cal['imbardata'] - semi, cal['imbardata'] + semi),
            'femore': (cal['alpha'] - semi, cal['alpha'] + semi),
            'ginocchio': (cal['gamma'] - 90.0 - semi, cal['gamma'] - 90.0 + semi)}


def limiti_giunti(d):
    """Fine corsa meccanici in q (gradi), da cad.json -> limiti_meccanici."""
    lim = d.cad['limiti_meccanici']
    g = lim['gamma']
    return {'coxa': tuple(lim['imbardata']), 'femore': tuple(lim['alpha']), 'ginocchio': (g[0] - 90.0, g[1] - 90.0)}


def posa_in_piedi(d):
    """Angoli (imbardata, alpha, gamma) della posa neutra all'assetto di robot.yaml -> andatura, per tutte le zampe."""
    a = d.yaml['andatura']['assetto']
    s = d.ik_piano(a['xf0'], a['h'])
    return 0.0, s[0], s[1]


def altezza_appoggio(d, alpha, gamma, r_piede):
    """Quota dell'origine del corpo (mm) con la sfera del piede che tocca il suolo, per una posa della zampa."""
    a = math.radians(alpha)
    b = a - math.pi + math.radians(gamma)
    # centro della sfera: sull'asse della tibia, r_piede sopra la punta
    zc = d.Lf * math.sin(a) + (d.Lt - r_piede) * math.sin(b)
    return -(zc - r_piede)


# ------------------------------------------------------------------------------------------------ URDF
def _quat_z(gradi):
    h = math.radians(gradi) / 2
    return (math.cos(h), 0.0, 0.0, math.sin(h))


def _urdf_inerziale(el, M, C, J):
    i = ET.SubElement(el, 'inertial')
    ET.SubElement(i, 'origin', xyz=vet([x / 1000 for x in C]), rpy='0 0 0')
    ET.SubElement(i, 'mass', value=num(M / 1000))
    k = 1e-9                                             # g mm2 -> kg m2
    ET.SubElement(i, 'inertia', ixx=sig(J[0][0] * k), ixy=sig(J[0][1] * k), ixz=sig(J[0][2] * k),
                  iyy=sig(J[1][1] * k), iyz=sig(J[1][2] * k), izz=sig(J[2][2] * k))


def _urdf_urti(el, primitive):
    """Capsule come cilindro piu' due sfere: l'URDF non ha la capsula."""
    for nome, tipo, a, b in primitive:
        if tipo == 'box':
            c = ET.SubElement(el, 'collision', name=nome)
            ET.SubElement(c, 'origin', xyz=vet([x / 1000 for x in a]), rpy='0 0 0')
            ET.SubElement(ET.SubElement(c, 'geometry'), 'box', size=vet([2 * x / 1000 for x in b]))
        elif tipo == 'cylinder':
            c = ET.SubElement(el, 'collision', name=nome)
            ET.SubElement(c, 'origin', xyz=vet([x / 1000 for x in a]), rpy='0 0 0')
            ET.SubElement(ET.SubElement(c, 'geometry'), 'cylinder', radius=num(b[0] / 1000),
                          length=num(2 * b[1] / 1000))
        elif tipo == 'sphere':
            c = ET.SubElement(el, 'collision', name=nome)
            ET.SubElement(c, 'origin', xyz=vet([x / 1000 for x in a]), rpy='0 0 0')
            ET.SubElement(ET.SubElement(c, 'geometry'), 'sphere', radius=num(b / 1000))
        elif tipo == 'capsule':
            p0, p1 = a
            dx, dy, dz = (p1[k] - p0[k] for k in range(3))
            lung = math.sqrt(dx * dx + dy * dy + dz * dz)
            # il cilindro dell'URDF e' lungo Z: ruotato attorno a Y (le capsule stanno in piani XZ)
            beccheggio = math.atan2(dx, dz)
            mezzo = [(p0[k] + p1[k]) / 2 / 1000 for k in range(3)]
            c = ET.SubElement(el, 'collision', name=nome)
            ET.SubElement(c, 'origin', xyz=vet(mezzo), rpy='0 %s 0' % num(beccheggio, 9))
            ET.SubElement(ET.SubElement(c, 'geometry'), 'cylinder', radius=num(b / 1000), length=num(lung / 1000))
            for k, pk in enumerate((p0, p1)):
                c = ET.SubElement(el, 'collision', name='%s_%d' % (nome, k))
                ET.SubElement(c, 'origin', xyz=vet([x / 1000 for x in pk]), rpy='0 0 0')
                ET.SubElement(ET.SubElement(c, 'geometry'), 'sphere', radius=num(b / 1000))


def urdf(d):
    seg, prim, sv, lim = segmenti(d), urti(d), servo(d), limiti_giunti(d)
    o = origini_segmenti(d)
    r = ET.Element('robot', name='esapode')
    r.append(ET.Comment(' Generato da tools/genera_modelli.py (versione %s, %s): non modificare a mano. '
                        % (d.yaml['versione'], d.cad['documento'])))
    ET.SubElement(ET.SubElement(r, 'material', name='scuro'), 'color', rgba='0.18 0.18 0.2 1')

    def link(nome, segmento, mesh_xyz=None):
        el = ET.SubElement(r, 'link', name=nome)
        if segmento:
            v = ET.SubElement(el, 'visual')
            ET.SubElement(v, 'origin', xyz=vet([x / 1000 for x in mesh_xyz]), rpy='0 0 0')
            ET.SubElement(ET.SubElement(v, 'geometry'), 'mesh', filename='../mesh/%s.stl' % segmento,
                          scale='0.001 0.001 0.001')
            ET.SubElement(v, 'material', name='scuro')
            _urdf_inerziale(el, *seg[segmento])
            _urdf_urti(el, prim[segmento])
        return el

    def giunto(nome, tipo, padre, figlio, xyz, rpy='0 0 0', asse=None, campo=None):
        j = ET.SubElement(r, 'joint', name=nome, type=tipo)
        ET.SubElement(j, 'parent', link=padre)
        ET.SubElement(j, 'child', link=figlio)
        ET.SubElement(j, 'origin', xyz=vet([x / 1000 for x in xyz]), rpy=rpy)
        if asse:
            ET.SubElement(j, 'axis', xyz=asse)
            ET.SubElement(j, 'limit', lower=num(math.radians(campo[0]), 6), upper=num(math.radians(campo[1]), 6),
                          effort=num(sv['stallo_nm'], 4), velocity=num(sv['velocita_rad_s'], 4))
            ET.SubElement(j, 'dynamics', damping=num(sv['smorzamento'], 6))

    link('corpo', 'corpo', (0, 0, 0))
    link('imu', None)
    giunto('imu', 'fixed', 'corpo', 'imu', imu_mm(d))
    for n in d.zampe:
        x, y, dire = d.coxe[n]
        link('coxa_' + n, 'coxa', (0, 0, 0))
        link('femore_' + n, 'femore', [-c for c in o['femore']])
        link('tibia_' + n, 'tibia', [-c for c in o['tibia']])
        link('piede_' + n, None)
        giunto('g_coxa_' + n, 'revolute', 'corpo', 'coxa_' + n, (x, y, 0.0), '0 0 %s' % num(math.radians(dire), 9),
               '0 0 1', lim['coxa'])
        giunto('g_femore_' + n, 'revolute', 'coxa_' + n, 'femore_' + n, o['femore'], asse='0 -1 0', campo=lim['femore'])
        giunto('g_ginocchio_' + n, 'revolute', 'femore_' + n, 'tibia_' + n, (d.Lf, 0.0, 0.0), asse='0 -1 0',
               campo=lim['ginocchio'])
        giunto('punta_' + n, 'fixed', 'tibia_' + n, 'piede_' + n, (0.0, 0.0, -d.Lt))
    ET.indent(r, space='  ')
    return '<?xml version="1.0"?>\n' + ET.tostring(r, encoding='unicode') + '\n'


def imu_mm(d):
    return (IMU_X_MM, 0.0, -d.cad['parametri']['cor_tetto']['valore'] + IMU_SOPRA_TETTO_MM)


# ------------------------------------------------------------------------------------------------ MJCF
def _mjcf_urti(corpo, primitive, classe='urto'):
    for nome, tipo, a, b in primitive:
        if tipo == 'box':
            ET.SubElement(corpo, 'geom', name=nome, **{'class': classe}, type='box',
                          pos=vet([x / 1000 for x in a]), size=vet([x / 1000 for x in b]))
        elif tipo == 'cylinder':
            ET.SubElement(corpo, 'geom', name=nome, **{'class': classe}, type='cylinder',
                          pos=vet([x / 1000 for x in a]), size=vet([x / 1000 for x in b]))
        elif tipo == 'capsule':
            ET.SubElement(corpo, 'geom', name=nome, **{'class': classe}, type='capsule',
                          fromto=vet([x / 1000 for x in a[0] + a[1]]), size=num(b / 1000))
        elif tipo == 'sphere':
            ET.SubElement(corpo, 'geom', name=nome, **{'class': 'piede'}, type='sphere',
                          pos=vet([x / 1000 for x in a]), size=num(b / 1000))


def _mjcf_inerziale(corpo, M, C, J):
    k = 1e-9
    ET.SubElement(corpo, 'inertial', pos=vet([x / 1000 for x in C]), mass=num(M / 1000),
                  fullinertia=' '.join(sig(x * k) for x in (J[0][0], J[1][1], J[2][2], J[0][1], J[0][2], J[1][2])))


def mjcf(d):
    seg, prim, sv, lim, cmd = segmenti(d), urti(d), servo(d), limiti_giunti(d), campi_comando(d)
    o = origini_segmenti(d)
    r_piede = [b for _, t, _, b in prim['tibia'] if t == 'sphere'][0]
    m = ET.Element('mujoco', model='esapode')
    m.append(ET.Comment(' Generato da tools/genera_modelli.py (versione %s, %s): non modificare a mano. '
                        % (d.yaml['versione'], d.cad['documento'])))
    ET.SubElement(m, 'compiler', angle='radian', meshdir='../../robot/mesh', autolimits='true')
    # passo di 2 ms (software.md 4.5); implicitfast integra in modo implicito lo smorzamento dei giunti
    ET.SubElement(m, 'option', timestep='0.002', integrator='implicitfast', cone='elliptic', impratio='100')
    vis = ET.SubElement(m, 'visual')
    ET.SubElement(vis, 'global', offwidth='1280', offheight='720')

    # parametri del servo che l'MJCF non sa esprimere (la banda morta) o che servono al simulatore: sim/servo.py
    cu = ET.SubElement(m, 'custom')
    for k in ('stallo_nm', 'velocita_rad_s', 'smorzamento', 'kp', 'semibanda_morta_rad'):
        ET.SubElement(cu, 'numeric', name='servo_' + k, data=sig(sv[k], 8))
    ET.SubElement(cu, 'numeric', name='servo_saturazione_gradi', data=num(SATURAZIONE_GRADI))

    df = ET.SubElement(ET.SubElement(m, 'default'), 'default', **{'class': 'esapode'})
    df.append(ET.Comment(' smorzamento = stallo / velocita a vuoto: la retta coppia-velocita del motore a piena '
                         'tensione; kp = stallo / %g gradi (saturazione, S); forcerange = stallo a %g V; banda morta '
                         'in sim/servo.py ' % (SATURAZIONE_GRADI, d.yaml['servo']['tensione_rail'])))
    ET.SubElement(df, 'joint', type='hinge', damping=sig(sv['smorzamento'], 6), armature='0')
    ET.SubElement(df, 'position', kp=sig(sv['kp'], 6),
                  forcerange='%s %s' % (num(-sv['stallo_nm'], 5), num(sv['stallo_nm'], 5)))
    ET.SubElement(df, 'geom', friction='%s 0.005 0.0001' % num(ATTRITO), solref=CONTATTO_SOLREF)
    ET.SubElement(ET.SubElement(df, 'default', **{'class': 'visivo'}), 'geom', type='mesh', contype='0',
                  conaffinity='0', group='2', density='0', material='scuro')
    ET.SubElement(ET.SubElement(df, 'default', **{'class': 'urto'}), 'geom', group='3', rgba='0.9 0.5 0.1 0.4')
    ET.SubElement(ET.SubElement(df, 'default', **{'class': 'piede'}), 'geom', group='3', rgba='1 0.4 0 1')

    asset = ET.SubElement(m, 'asset')
    for s in SEGMENTI:
        ET.SubElement(asset, 'mesh', name=s, file=s + '.stl', scale='0.001 0.001 0.001')
    ET.SubElement(asset, 'material', name='scuro', rgba='0.18 0.18 0.2 1')
    ET.SubElement(asset, 'texture', name='griglia', type='2d', builtin='checker', rgb1='0.32 0.34 0.36',
                  rgb2='0.42 0.44 0.46', width='512', height='512')
    ET.SubElement(asset, 'material', name='pavimento', texture='griglia', texrepeat='10 10', reflectance='0')

    wb = ET.SubElement(m, 'worldbody')
    ET.SubElement(wb, 'light', name='sole', pos='0 0 2', dir='0 0 -1', directional='true')
    ET.SubElement(wb, 'geom', name='pavimento', type='plane', size='0 0 0.05', material='pavimento',
                  friction='%s 0.005 0.0001' % num(ATTRITO), solref=CONTATTO_SOLREF)

    imb, alpha, gamma = posa_in_piedi(d)
    z0 = altezza_appoggio(d, 0.0, 90.0, r_piede)           # posa come costruita: piedi a terra
    corpo = ET.SubElement(wb, 'body', name='corpo', pos='0 0 %s' % num(z0 / 1000), childclass='esapode')
    ET.SubElement(corpo, 'freejoint', name='corpo')
    _mjcf_inerziale(corpo, *seg['corpo'])
    ET.SubElement(corpo, 'geom', name='mesh_corpo', **{'class': 'visivo'}, mesh='corpo')
    _mjcf_urti(corpo, prim['corpo'])
    ET.SubElement(corpo, 'site', name='imu', pos=vet([x / 1000 for x in imu_mm(d)]), size='0.005', rgba='0 0.6 1 1')

    for n in d.zampe:
        x, y, dire = d.coxe[n]
        coxa = ET.SubElement(corpo, 'body', name='coxa_' + n, pos=vet([x / 1000, y / 1000, 0.0]),
                             quat=vet(_quat_z(dire), 9))
        _mjcf_inerziale(coxa, *seg['coxa'])
        ET.SubElement(coxa, 'joint', name='g_coxa_' + n, axis='0 0 1',
                      range='%s %s' % tuple(num(math.radians(v)) for v in lim['coxa']))
        ET.SubElement(coxa, 'geom', name='mesh_coxa_' + n, **{'class': 'visivo'}, mesh='coxa')
        _mjcf_urti(coxa, [(a + '_' + n, t, p, b) for a, t, p, b in prim['coxa']])

        fem = ET.SubElement(coxa, 'body', name='femore_' + n, pos=vet([c / 1000 for c in o['femore']]))
        _mjcf_inerziale(fem, *seg['femore'])
        ET.SubElement(fem, 'joint', name='g_femore_' + n, axis='0 -1 0',
                      range='%s %s' % tuple(num(math.radians(v)) for v in lim['femore']))
        ET.SubElement(fem, 'geom', name='mesh_femore_' + n, **{'class': 'visivo'}, mesh='femore',
                      pos=vet([-c / 1000 for c in o['femore']]))
        _mjcf_urti(fem, [(a + '_' + n, t, p, b) for a, t, p, b in prim['femore']])

        tib = ET.SubElement(fem, 'body', name='tibia_' + n, pos=vet([d.Lf / 1000, 0.0, 0.0]))
        _mjcf_inerziale(tib, *seg['tibia'])
        ET.SubElement(tib, 'joint', name='g_ginocchio_' + n, axis='0 -1 0',
                      range='%s %s' % tuple(num(math.radians(v)) for v in lim['ginocchio']))
        ET.SubElement(tib, 'geom', name='mesh_tibia_' + n, **{'class': 'visivo'}, mesh='tibia',
                      pos=vet([-c / 1000 for c in o['tibia']]))
        _mjcf_urti(tib, [(a + '_' + n, t, p, b) for a, t, p, b in prim['tibia']])
        ET.SubElement(tib, 'site', name='punta_' + n, pos=vet([0.0, 0.0, -d.Lt / 1000]), size='0.002')
        ET.SubElement(tib, 'site', name='contatto_' + n, type='sphere', size=num((r_piede + 1.0) / 1000),
                      pos=vet([0.0, 0.0, (-d.Lt + r_piede) / 1000]), rgba='0 1 0 0.3')

    att = ET.SubElement(m, 'actuator')
    for n in d.zampe:
        for g in ('coxa', 'femore', 'ginocchio'):
            ET.SubElement(att, 'position', name='%s_%s' % (g, n), joint='g_%s_%s' % (g, n), **{'class': 'esapode'},
                          ctrlrange='%s %s' % tuple(num(math.radians(v)) for v in cmd[g]))

    sen = ET.SubElement(m, 'sensor')
    for n in d.zampe:
        ET.SubElement(sen, 'touch', name='contatto_' + n, site='contatto_' + n)
    ET.SubElement(sen, 'accelerometer', name='imu_acc', site='imu')
    ET.SubElement(sen, 'gyro', name='imu_gyro', site='imu')
    ET.SubElement(sen, 'framequat', name='imu_quat', objtype='site', objname='imu')

    # posa neutra all'assetto di robot.yaml, piedi a terra
    q = [math.radians(imb), math.radians(alpha), math.radians(gamma - 90.0)]
    zp = altezza_appoggio(d, alpha, gamma, r_piede)
    kf = ET.SubElement(m, 'keyframe')
    ET.SubElement(kf, 'key', name='in_piedi', qpos=vet([0.0, 0.0, zp / 1000, 1.0, 0.0, 0.0, 0.0] + q * len(d.zampe), 9),
                  ctrl=vet(q * len(d.zampe), 9))
    ET.indent(m, space='  ')
    return ET.tostring(m, encoding='unicode') + '\n'


# ------------------------------------------------------------------------------------------------ uscita
def genera(descrizione):
    """{percorso relativo alla repo: testo} dei modelli generati."""
    return {USCITA_URDF: urdf(descrizione), USCITA_MJCF: mjcf(descrizione)}


def main(argv):
    d = Descrizione()
    file = genera(d)
    if '--controlla' in argv:
        diversi = []
        for rel, testo in file.items():
            p = os.path.join(REPO, rel)
            if not os.path.exists(p) or open(p, encoding='utf-8').read() != testo:
                diversi.append(rel)
        if diversi:
            print('modelli non aggiornati: %s. Rigenerare con "python3 tools/genera_modelli.py" e fare il commit.'
                  % ', '.join(diversi))
            return 1
        print('modelli aggiornati')
        return 0
    for rel, testo in file.items():
        p = os.path.join(REPO, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(testo)
        print('scritto', rel)
    seg = segmenti(d)
    print('massa del modello %.1f g (robot.yaml -> massa.attesa_g %.1f)'
          % (seg['corpo'][0] + len(d.zampe) * sum(seg[s][0] for s in SEGMENTI[1:]), d.yaml['massa']['attesa_g']))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
