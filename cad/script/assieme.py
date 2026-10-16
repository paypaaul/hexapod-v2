"""Assieme dell'esapode MG996R (fase 4, D-050): corpo, sei zampe, giunti di coxa, componenti nel corpo.

Si esegue dentro Fusion sul design di lavoro (`versione.py`), un passo per chiamata:
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
V = runpy.run_path(os.path.join(QUI, 'versione.py'))
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
    # predisposizioni 2.1.0 (D-066): posti in corpo.py -> PARAMETRI
    out['Interruttore'] = ('Rif_Interruttore_Pololu_2813', A['matrice']((_mm(des, 'cor_int_x'), 0, _mm(des, 'cor_int_z0') + _mm(des, 'int_w') / 2),
                                                                 (0, 1, 0), (0, 0, 1), (1, 0, 0)))
    zb = zt + _mm(des, 'cor_sen_bugna_h')
    # IMU montata: GY-6500 sulla sua piastrina (D-074); la Pololu sulle bugne e' in alternative()
    out['IMU'] = ('Rif_IMU_MPU6500', _rz(_mm(des, 'cor_imu_x'), _mm(des, 'cor_mpu_y'), zb + _mm(des, 'cor_pimu_sp'), 0.0))
    out['ADC'] = ('Rif_ADC_ADS7830', _rz(_mm(des, 'cor_ads_x'), _mm(des, 'cor_ads_y'), zb, 0.0))
    out['Prese_piedi'] = ('Rif_Prese_Piedi', _rz(_mm(des, 'cor_pre_x'), _mm(des, 'cor_pre_y'), zt + 0.5, 0.0))
    out['Prese_luci'] = ('Rif_Prese_Piedi', _rz(_mm(des, 'cor_pre_x'), -_mm(des, 'cor_pre_y'), zt + 0.5, 0.0))
    a = des.unitsManager.evaluateExpression('cor_tof_ang', 'rad')
    out['ToF_frontale'] = ('Rif_ToF_8x8', A['matrice']((_mm(des, 'cor_tof_x'), 0, _mm(des, 'cor_tof_z')),
                                                       (math.sin(a), 0, math.cos(a)), (0, -1, 0), (math.cos(a), 0, -math.sin(a))))
    b = des.unitsManager.evaluateExpression('cor_tofp_ang', 'rad')
    yp = _mm(des, 'car_guancia_y0') - 0.5 - _mm(des, 'sen_tof_w') / 2
    out['ToF_posteriore'] = ('Rif_ToF_1', A['matrice']((_mm(des, 'cor_tofp_x'), yp, _mm(des, 'cor_tofp_z')),
                                                       (-math.sin(b), 0, math.cos(b)), (0, 1, 0), (-math.cos(b), 0, -math.sin(b))))
    yi = _mm(des, 'cor_baia_y') - _mm(des, 'cor_parete') - _mm(des, 'cor_slitta_sp') - _mm(des, 'cor_sup_sp') - _mm(des, 'cor_ina_dist')
    xi, zi = _mm(des, 'cor_ina_x'), _mm(des, 'cor_ina_z')
    out['INA260_S'] = ('Rif_INA260', A['matrice']((xi, yi, zi), (1, 0, 0), (0, 0, 1), (0, -1, 0)))
    out['INA260_D'] = ('Rif_INA260', A['matrice']((xi, -yi, zi), (-1, 0, 0), (0, 0, 1), (0, 1, 0)))
    # altoparlante tondo (D-074): fra le guide, contro il fermo all'estremo anteriore della guancia
    out['Altoparlante'] = ('Rif_Altoparlante_Tondo', A['matrice']((-_mm(des, 'aud_altt_x'), -_mm(des, 'car_guancia_y0'), _mm(des, 'aud_alt_z')),
                                                                  (0, 0, 1), (1, 0, 0), (0, 1, 0)))
    zs = _mm(des, 'car_top') - _mm(des, 'car_sp')
    # amplificatore generico (D-074): morsettiera e fori verso +X, pin verso la scheda del carapace
    out['Ampli'] = ('Rif_Ampli_Generico', _rz(_mm(des, 'aud_amp_x'), 0, zs - 3.5 - _mm(des, 'aud_amp_sp'), -90.0))
    out['Scheda_carapace'] = ('Rif_Scheda_Carapace', _rz(_mm(des, 'sch_x'), 0, zs - 3.5 - _mm(des, 'sch_sp'), 90.0))
    for lato, s in (('S', 1), ('D', -1)):
        # scheda capovolta: la porta del microfono (sul fondo) guarda il foro, appoggiata all'anello della guarnizione
        # MS3625 montate (D-074): lati piatti lungo Y, centrate dalle lunette nel telaio della Adafruit 3421
        out['Microfono_' + lato] = ('Rif_Microfono_MS3625', _pose_microfono(des, s))
    return out


def _pose_microfono(des, s):
    zs = _mm(des, 'car_top') - _mm(des, 'car_sp')
    return A['matrice']((_mm(des, 'aud_mic_x'), s * _mm(des, 'aud_mic_y'), zs - 0.6), (0, 1, 0), (1, 0, 0), (0, 0, -1))


def alternative(des):
    """Moduli predisposti ma non montati (D-074): {chiave: (componente di libreria, matrice, parti da togliere)}. Le
    parti da togliere sono quelle della variante montata, che si smontano per far posto a questa."""
    zb = -_mm(des, 'cor_tetto') + _mm(des, 'cor_sen_bugna_h')
    out = {'IMU_Pololu': ('Rif_IMU', _rz(_mm(des, 'cor_imu_x'), _mm(des, 'cor_imu_y'), zb, 0.0),
                          ('Corpo_Piastrina_IMU', 'Rif_IMU_MPU6500'))}
    for lato, s in (('S', 1), ('D', -1)):
        out['Microfono_Adafruit_' + lato] = ('Rif_Microfono_I2S', _pose_microfono(des, s), ('Corpo_Lunette_Microfoni', 'Rif_Microfono_MS3625'))
    return out


def varianti(des, root):
    """Ogni modulo alternativo nella sua posa, contro tutti i corpi del robot tranne la variante montata: volumi di
    intersezione (mm3). Caso di controllo: lo stesso conto senza togliere la variante montata deve trovare un urto."""
    tbm = adsk.fusion.TemporaryBRepManager.get()
    lib = {o.component.name: o for o in root.occurrences if o.component.name.startswith('Rif_')}
    corpi = []
    def raccogli(o):
        for b in o.bRepBodies:
            corpi.append((o.component.name, b))
        for c in o.childOccurrences:
            raccogli(c)
    for o in root.occurrences:
        if not o.component.name.startswith('Rif_') and not o.component.name.startswith('Attrezzo'):
            raccogli(o)
    out = {}
    for chiave, (nome_lib, m, togli) in alternative(des).items():
        prove = {'variante': [c for c in corpi if c[0] not in togli], 'controllo': corpi}
        for k, insieme in prove.items():
            urti = []
            for b in lib[nome_lib].component.bRepBodies:
                t = tbm.copy(b)
                tbm.transform(t, m)
                bb = t.boundingBox
                for nome, cb in insieme:
                    if cb.name in ('flat', 'linguetta', 'uscita_cavi'):     # ingombri non rigidi, come in _voluta
                        continue
                    q = cb.boundingBox
                    if (q.maxPoint.x < bb.minPoint.x or q.minPoint.x > bb.maxPoint.x or q.maxPoint.y < bb.minPoint.y or
                            q.minPoint.y > bb.maxPoint.y or q.maxPoint.z < bb.minPoint.z or q.minPoint.z > bb.maxPoint.z):
                        continue
                    c1 = tbm.copy(t)
                    if tbm.booleanOperation(c1, tbm.copy(cb), adsk.fusion.BooleanTypes.IntersectionBooleanType) and c1.volume > 1e-6:
                        urti.append('%s %.2f' % (nome, c1.volume * 1000))
            out['%s %s' % (chiave, k)] = urti or 'nessuno'
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


def fai_istanze_nuove(des, root):
    """Crea solo le istanze di pose_corpo che mancano (nessuna istanza dello stesso componente entro 1 mm): per i
    componenti aggiunti dopo, senza rifare le altre (fai_istanze_corpo va in timeout)."""
    corpo = _corpo(root)
    lib = {o.component.name: o for o in root.occurrences if o.component.name.startswith('Rif_')}
    fatte = []
    for chiave, (nome_lib, m) in pose_corpo(des).items():
        t = m.translation
        cand = [o for o in corpo.component.occurrences if o.component.name == nome_lib]
        if cand and math.dist([v * 10 for v in (t.x, t.y, t.z)],
                              [v * 10 for v in (lambda q: (q.x, q.y, q.z))(A['piu_vicina'](cand, (t.x * 10, t.y * 10, t.z * 10)).transform2.translation)]) < 1.0:
            continue
        o = A['aggiungi_istanza'](root, lib[nome_lib], m, dentro=corpo)
        o.isLightBulbOn = True
        fatte.append(chiave)
    for o in [o for o in root.occurrences if o.component.name.startswith('Rif_') and o.transform2.translation.y * 10 < 249]:
        o.deleteMe()
    return fatte


def pulisci_istanze(des, root):
    """Cancella le istanze Rif_ dentro Corpo che non stanno entro 1 mm da una posa di pose_corpo per lo stesso
    componente (restano dopo aver spostato un posto con i parametri e rifatto istanze_nuove)."""
    corpo = _corpo(root)
    attese = {}
    for nome_lib, m in pose_corpo(des).values():
        t = m.translation
        attese.setdefault(nome_lib, []).append((t.x * 10, t.y * 10, t.z * 10))
    tolte = []
    while True:
        for o in corpo.component.occurrences:
            n = o.component.name
            if not n.startswith('Rif_'):
                continue
            t = o.transform2.translation
            p = (t.x * 10, t.y * 10, t.z * 10)
            if not any(math.dist(p, q) < 1.0 for q in attese.get(n, [])):
                tolte.append('%s %s' % (n, [round(v, 1) for v in p]))
                o.deleteMe()
                break
        else:
            return tolte


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
    # i due sportellini di servizio sono alternativi: quello con la tacca dell'USB-C si monta solo con lo zaino
    if nomi == {'Corpo_Sportello_Servizio', 'Corpo_Sportello_Servizio_Zaino'}:
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
SEGUONO_FEMORE = ('Femore_B', 'Femore_A', 'Ingombro_Teste_A', 'Cover_Femore_A', 'Cover_Femore_B', 'Cover_Femore_A_Feritoia',
                  'Cover_Femore_B_Feritoia')   # piu' le copie con origine sul femore (squadrette, perni)
SEGUONO_TIBIA = ('Tibia', 'Cover_Tibia', 'Piedino', 'Cover_Tibia_Diffusore', 'Rif_FSR_400')


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
# montati sul carapace o sulla visiera: si tolgono con loro (D-066)
SALGONO_COL_CARAPACE = GRUPPO_CARAPACE + ('Rif_Cicalino_BX100', 'Rif_Pulsante_12', 'Corpo_Fondo_Anello', 'Corpo_Tappo_ToF',
                                          'Corpo_Sportello_Servizio_Zaino',
                                          'Rif_Altoparlante_Tondo', 'Rif_Microfono_MS3625', 'Corpo_Lunette_Microfoni', 'Rif_Ampli_Generico',
                                          'Rif_Scheda_Carapace', 'Rif_ToF_1')


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
                    if o.component.name in SEGUONO_FEMORE:
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


def _corpi_mondo(occorrenze, salta_comp=(), salta_corpi=('flat', 'linguetta', 'uscita_cavi')):
    """[(componente, corpo proxy)] delle occorrenze e dei loro figli, nella terna del robot."""
    out = []
    def raccogli(o):
        if o.component.name in salta_comp:
            return
        for b in o.bRepBodies:
            if b.name not in salta_corpi:
                out.append((o.component.name, b))
        for c in o.childOccurrences:
            raccogli(c)
    for o in occorrenze:
        raccogli(o)
    return out


def _urti_temporanei(mobili, fissi):
    """Intersezioni (mm3) fra corpi temporanei [(nome, brep)] e corpi del modello [(componente, corpo)]."""
    tbm = adsk.fusion.TemporaryBRepManager.get()
    urti = []
    for nm, t in mobili:
        bb = t.boundingBox
        for nome, cb in fissi:
            q = cb.boundingBox
            if (q.maxPoint.x < bb.minPoint.x or q.minPoint.x > bb.maxPoint.x or q.maxPoint.y < bb.minPoint.y or
                    q.minPoint.y > bb.maxPoint.y or q.maxPoint.z < bb.minPoint.z or q.minPoint.z > bb.maxPoint.z):
                continue
            c1 = tbm.copy(t)
            if tbm.booleanOperation(c1, tbm.copy(cb), adsk.fusion.BooleanTypes.IntersectionBooleanType) and c1.volume > 1e-6:
                urti.append('%s/%s:%s %.2f' % (nm, nome, cb.name, c1.volume * 1000))
    return urti


def _box_mm(x0, y0, z0, x1, y1, z1):
    tbm = adsk.fusion.TemporaryBRepManager.get()
    c = adsk.core.Point3D.create((x0 + x1) / 20, (y0 + y1) / 20, (z0 + z1) / 20)
    obb = adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                 (x1 - x0) / 10, (y1 - y0) / 10, (z1 - z0) / 10)
    return tbm.createBox(obb)


def _cil_z_mm(x, y, z0, z1, d):
    tbm = adsk.fusion.TemporaryBRepManager.get()
    return tbm.createCylinderOrCone(adsk.core.Point3D.create(x / 10, y / 10, z0 / 10), d / 20,
                                    adsk.core.Point3D.create(x / 10, y / 10, z1 / 10), d / 20)


def pacco_mobile(des, root, lato_spina=-1, cavo_d=4.0, piu_alta=0.0):
    """Pacco con quello che si sfila con lui (P-001, D-076), come corpi temporanei: il pacco, due cavi da 12 AWG (Ø cavo_d)
    nella fessura sinistra e il bilanciamento (Ø3) nella destra, dal pacco a 3 mm sopra il tetto; con lato_spina (+1 / -1)
    anche la meta' femmina del T-plug (15 x 16 x 8,5, staccata, sopra F1 da quella parte) e la JST-XH a 3 poli
    (9,9 x 5,75 x 6 S) appesa nella porta di coda. Con lato_spina = 0 le spine sono gia' fuori dalla porta di coda e si sfilano
    solo pacco e cavi. piu_alta alza la cima della spina (caso di controllo)."""
    tbm = adsk.fusion.TemporaryBRepManager.get()
    corpo = _corpo(root)
    bat = _istanze_corpo(corpo)['Batteria']
    mob = [('pacco', tbm.copy(b)) for b in bat.bRepBodies if b.name == 'pacco']
    zt, zp = -_mm(des, 'cor_tetto'), max(b.boundingBox.maxPoint.z for _, b in mob) * 10
    yc = _mm(des, 'cor_cavi_y0') + (_mm(des, 'cor_tun_semi') - _mm(des, 'cor_parete') - _mm(des, 'cor_cavi_y0')) / 2
    for k, x in (('cavo_piu', -79.0), ('cavo_meno', -74.0)):
        mob.append((k, _cil_z_mm(x, yc, zp, zt + 3.0, cavo_d)))
    mob.append(('bilanciamento', _cil_z_mm(-79.0, -yc, zp, zt + 3.0, 3.0)))
    x_f = -_mm(des, 'cor_tun_x0') + 2 + _mm(des, 'fus_w') / 2
    z_f = zt + _mm(des, 'fus_h')
    if lato_spina:
        y0, y1 = (0.5, 15.5) if lato_spina > 0 else (-15.5, -0.5)
        mob.append(('tplug_femmina', _box_mm(x_f - 8, y0, z_f, x_f + 8, y1, z_f + 8.5 + piu_alta)))
        # JST-XH staccata dalla prolunga del cicalino, appesa nella porta di coda dietro il tetto (fra F1 e la guancia
        # restano 5,4 mm, sopra il T-plug 3,3 sotto il cicalino: li' non ci sta)
        ya, yb = sorted((-lato_spina * 2.0, -lato_spina * 7.75))
        xc = -_mm(des, 'cor_tun_x0') - 0.5
        mob.append(('jst_xh', _box_mm(xc - 9.9, ya, zt + 2.0, xc, yb, zt + 8.0)))
    return mob


def sfilamento_pacco(des, root, corse, lato_spina=-1, cavo_d=4.0, piu_alta=0.0):
    """Il pacco sfilato verso la coda di d mm (sportello tolto, carapace montato) con cavi e spine attaccati: urti con
    tutti i pezzi del corpo tranne la coppia di T-plug (la meta' maschio resta su F1 come corpo a parte)."""
    corpo = _corpo(root)
    fissi = _corpi_mondo([corpo], salta_comp=('Corpo_Sportello', 'Rif_Batteria_2S5200', 'Rif_Tplug'))
    x_f = -_mm(des, 'cor_tun_x0') + 2 + _mm(des, 'fus_w') / 2
    z_f = -_mm(des, 'cor_tetto') + _mm(des, 'fus_h')
    y0, y1 = (-15.5, -0.5) if lato_spina > 0 else (0.5, 15.5)
    maschio = ('tplug_maschio', _box_mm(x_f - 8, y0, z_f, x_f + 8, y1, z_f + 8.5))      # resta su F1, saldato
    tbm = adsk.fusion.TemporaryBRepManager.get()
    out = {}
    for d in corse:
        mob = pacco_mobile(des, root, lato_spina, cavo_d, piu_alta)
        m = adsk.core.Matrix3D.create()
        m.translation = adsk.core.Vector3D.create(-d / 10, 0, 0)
        for _, t in mob:
            tbm.transform(t, m)
        out['%g' % d] = _urti_temporanei(mob, fissi + [('T-plug', maschio[1])]) or 'nessuno'
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
        V['controlla'](app)
        root = des.rootComponent
        if 'istanze_corpo' in passi:
            out['istanze_corpo'] = fai_istanze_corpo(des, root)
        if 'pulisci_istanze' in passi:
            out['pulisci_istanze'] = pulisci_istanze(des, root)
        if 'istanze_nuove' in passi:
            out['istanze_nuove'] = fai_istanze_nuove(des, root)
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
        if 'varianti' in passi:
            out['varianti'] = varianti(des, root)
        if 'sfilamento_pacco' in passi:
            out['sfilamento_pacco'] = sfilamento_pacco(des, root, kw.get('corse', (0.0, 10.0, 20.0)), kw.get('lato_spina', -1),
                                                       kw.get('cavo_d', 4.0), kw.get('piu_alta', 0.0))
        if 'stato' in passi:
            out['stato'] = stato(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out
