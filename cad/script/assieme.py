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
    out['ESP32'] = ('Rif_ESP32_S3_CAM', _rz(54.0, 0, 16.0, 0.0))                         # antenna in avanti
    out['Camera'] = ('Rif_Camera_OV3660_75', A['matrice']((92.5, 0, 22.5), (0, 0, 1), (0, -1, 0), (1, 0, 0)))
    out['Regolatore_S'] = ('Rif_Reg_Servo_D42V110F6', A['matrice']((14.0, 32.0, 3.8), (1, 0, 0), (0, 0, -1), (0, 1, 0)))
    out['Regolatore_D'] = ('Rif_Reg_Servo_D42V110F6', A['matrice']((57.2, -32.0, 3.8), (-1, 0, 0), (0, 0, -1), (0, -1, 0)))
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
    if corpo_a in ('flat', 'linguetta') or corpo_b in ('flat', 'linguetta'):
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
        if 'stato' in passi:
            out['stato'] = stato(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
