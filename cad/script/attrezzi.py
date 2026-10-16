"""Attrezzi da banco della versione 2.1.0 (D-066): dime di taratura e cavalletto. Componenti nella zona libreria
(y >= 250, spenti); STL in cad/stl/attrezzi/ con esporta_stl.py.

Dime di posa (software.md 2.7: due pose note per giunto, taratura a due punti):
  Dima_Posa_1  imbardata 0, femore 0, ginocchio 90
  Dima_Posa_2  imbardata +30, femore +45, ginocchio 135
Valgono per tutte e sei le zampe (sono la stessa zampa ruotata). La dima e' una piastra che si infila sui due perni del
femore dal lato B, con la lama B tolta, appoggiata ai mozzi, con tre denti:
  - femore: contro la faccia +X della culla della coxa, sotto la testa del femore;
  - ginocchio: contro la faccia -X della culla della tibia, sotto la testa del femore;
  - imbardata: un braccio con una punta contro il fianco della cassa del servo di coxa, che sta nel corpo.
Le tre facce sono quasi radiali rispetto al loro asse: ruotando il giunto il punto di contatto si sposta lungo la normale
della faccia (circa 0,4 mm per grado), quindi il dente ferma davvero il giunto. Si porta un giunto alla volta contro il
suo dente con passi di 1 e 10 us dall'app (stato CALIBRAZIONE).

Dima_Calettamento (P-015, 2.1.7): stessa dima nella posa del calettamento di robot/robot.yaml (imbardata 0, femore +20,
ginocchio 100): si calettano le squadrette con il servo a meta' corsa e il giunto contro i denti.

Cavalletto: culla sotto la chiglia (lontana da sportello della batteria e viti), colonna cava e base; le zampe restano
libere su tutta l'escursione (piede piu' basso a z -159 con femore -49 e ginocchio 139, tavolo a z -170).

Provino degli inserti (P-057, 2.1.7): blocchetto con otto fori ciechi e il diametro inciso accanto a ciascuno.
Bussola del perno e estrattore (P-065, 2.1.7): la bussola ferma il perno premuto con la sporgenza giusta; l'asta passa
nel foro dietro il cuscinetto e lo spinge fuori nel tubo d'appoggio (o spinge fuori un perno).

Uso dal connettore, un passo per chiamata:
    runpy.run_path('/Users/paul/hexapod-v2/cad/script/attrezzi.py')['main'](['parametri', 'dime'])
Passi: parametri, dime (kw solo=[...]), cavalletto, provino_luce, provino_tasche, provino_inserti, bussola,
estrattore, verifica_dime (kw zampa='AS', solo=[...]), verifica_cavalletto, verifica_bussola, verifica_estrattore.
"""
import json
import math
import os
import re
import runpy
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
L = runpy.run_path(os.path.join(QUI, 'lib_cad.py'))
V = runpy.run_path(os.path.join(QUI, 'versione.py'))
A = runpy.run_path(os.path.join(QUI, 'lib_assieme.py'))
Parte, NUOVO, UNISCI, TAGLIA = L['Parte'], L['NUOVO'], L['UNISCI'], L['TAGLIA']
P3, V3 = adsk.core.Point3D.create, adsk.core.Vector3D.create

PARAMETRI = [
    ('att_sp', '3 mm', 'mm', 'Dime: spessore della piastra sui mozzi del femore'),
    ('att_gio_perno', '0.15 mm', 'mm', 'Dime: gioco per lato dei fori sui perni del femore'),
    ('att_dente', '4 mm', 'mm', 'Dime: spessore dei denti'),
    ('att_dente_l', '10 mm', 'mm', 'Dime: lunghezza dei denti lungo la faccia di contatto'),
    ('att_entra', '3 mm', 'mm', 'Dime: quanto i denti entrano oltre il fondo delle culle (lato B)'),
    ('att_z_contatto', '24 mm', 'mm', 'Dime: distanza sotto l asse dei contatti sulle culle (sotto le teste del femore, R13)'),
    ('att_punta_d', '4 mm', 'mm', 'Dime: diametro della punta del braccio dell imbardata'),
    ('att_punta_a', '20 mm', 'mm', 'Dime: punto di contatto sulla cassa del servo di coxa, distanza dall asse lungo la cassa'),
    ('att_punta_z', '4.5 mm', 'mm', 'Dime: punto di contatto sulla cassa del servo di coxa, sopra il lato inferiore delle alette'),
    ('att_braccio_w', '6 mm', 'mm', 'Dime: larghezza dei bracci nel piano della piastra'),
    ('cav_z_tavolo', '-(170 mm)', 'mm', 'Cavalletto: quota del tavolo (piede piu basso a z -159)'),
    ('cav_culla_x', '30 mm', 'mm', 'Cavalletto: semilunghezza della culla sotto la chiglia (lontana da sportello e viti a x 84 e -52)'),
    ('cav_gio', '0.3 mm', 'mm', 'Cavalletto: gioco per lato della chiglia nella culla'),
    ('cav_labbro', '8 mm', 'mm', 'Cavalletto: altezza dei labbri sui fianchi della chiglia (sotto il ripiano delle baie a z -31,95)'),
    ('cav_parete', '4 mm', 'mm', 'Cavalletto: parete della culla e della colonna'),
    # bussola del perno (P-065): il femore B appoggia la faccia interna del mozzo (zy_B_int) sulla bussola, il perno
    # premuto da fuori si ferma sul fondo del foro cieco; il rialzo da 0,4 resta libero nella sua tasca, cosi' non lo
    # schiaccia la morsa (fissa il gioco del cuscinetto). Fondo a perno_l - perno_sporge - fem_B_mozzo = 5,4 dalla
    # faccia del mozzo, cioe' 5,0 dalla faccia del rialzo come in P-065.
    ('att_bus_d', '5.5 mm', 'mm', 'Bussola del perno: foro cieco (perno 5, gioco 0,25 per lato, P-065)'),
    ('att_bus_prof', 'perno_l - perno_sporge - fem_B_mozzo', 'mm', 'Bussola del perno: fondo del foro dalla faccia del mozzo (sporgenza perno_sporge fuori)'),
    ('att_bus_D', '20 mm', 'mm', 'Bussola del perno: diametro (dentro la testa del femore, raggio fem_testa_r 13)'),
    ('att_bus_fondo', '3 mm', 'mm', 'Bussola del perno: fondo sotto il foro'),
    ('att_bus_gio', '0.3 mm', 'mm', 'Bussola del perno: gioco radiale e assiale della tasca del rialzo'),
    # estrattore (P-065): asta che entra dalla sede del servo, passa nel foro cus_passo_d dietro il cuscinetto e spinge
    # l'anello interno (spalla come il rialzo, cus_rialzo_d); la punta centra l'asta nel foro del cuscinetto e spinge
    # fuori i perni forzati (piu' lunga dei 5,6 del foro). Il tubo appoggia attorno alla flangia e la raccoglie.
    ('att_estr_pilota_gio', '0.2 mm', 'mm', 'Estrattore: gioco per lato della punta nel foro del cuscinetto (cus_d) e del perno (perno_foro)'),
    ('att_estr_pilota_d', 'cus_d - 2 * att_estr_pilota_gio', 'mm', 'Estrattore: diametro della punta'),
    ('att_estr_pilota_l', 'fem_B_mozzo + cus_rialzo_h + 0.4 mm', 'mm', 'Estrattore: lunghezza della punta (oltre il foro del perno da 5,6)'),
    ('att_estr_d', 'cus_rialzo_d', 'mm', 'Estrattore: spalla che spinge solo l anello interno (come il rialzo; passa nel foro cus_passo_d)'),
    ('att_estr_spalla_l', '10 mm', 'mm', 'Estrattore: lunghezza della spalla (attraversa i 1,2 dietro la sede e entra nella sede del servo)'),
    ('att_estr_gambo_d', '8 mm', 'mm', 'Estrattore: gambo nella sede del servo (semilarghezza cul_sede_semi 10,45); si ferma sul fondo della culla'),
    ('att_estr_gambo_l', 'zy_orlo - zy_fondo_int + 3 mm', 'mm', 'Estrattore: gambo; a fine corsa la testa resta 3 mm sopra l orlo della culla'),
    ('att_estr_testa_d', '20 mm', 'mm', 'Estrattore: testa su cui si preme'),
    ('att_estr_testa_h', '5 mm', 'mm', 'Estrattore: spessore della testa'),
    ('att_tubo_gio', '0.4 mm', 'mm', 'Estrattore: gioco per lato fra tubo e flangia del cuscinetto (cus_flangia_d, generici fino a 11,7)'),
    ('att_tubo_d', 'cus_flangia_d + 2 * att_tubo_gio', 'mm', 'Estrattore: diametro interno del tubo d appoggio'),
    ('att_tubo_D', 'cul_mozzo_d', 'mm', 'Estrattore: diametro esterno del tubo (il mozzo piano attorno al cuscinetto nella culla)'),
    ('att_tubo_h', 'perno_l + 3 mm', 'mm', 'Estrattore: altezza del tubo (dentro ci cade un perno intero)'),
]

ROBOT_YAML = os.path.join(os.path.dirname(os.path.dirname(QUI)), 'robot', 'robot.yaml')


def calettamento():
    """(imbardata, femore, ginocchio) del calettamento in robot/robot.yaml (servo -> calettamento): la dima lo segue.
    Il Python di Fusion non ha yaml: si legge la riga con un'espressione regolare."""
    with open(ROBOT_YAML, encoding='utf-8') as f:
        testo = f.read()
    m = re.search(r'calettamento:\s*\{imbardata:\s*([-\d.]+),\s*alpha:\s*([-\d.]+),\s*gamma:\s*([-\d.]+)\}', testo)
    if not m:
        raise RuntimeError('calettamento non trovato in %s: attesa la riga "calettamento: {imbardata: .., alpha: .., '
                           'gamma: ..}"' % ROBOT_YAML)
    return tuple(float(v) for v in m.groups())


# (imbardata, femore, ginocchio) in gradi delle due pose (software.md 2.7) e del calettamento (P-015)
POSE = {'Dima_Posa_1': (0.0, 0.0, 90.0), 'Dima_Posa_2': (30.0, 45.0, 135.0), 'Dima_Calettamento': calettamento()}
LIBRERIA = {'Dima_Posa_1': (0, 850, 0), 'Dima_Posa_2': (100, 850, 0), 'Attrezzo_Cavalletto': (260, 850, 0),
            'Attrezzo_Provino_Luce_Nero': (420, 850, 0), 'Attrezzo_Provino_Luce_Bianco': (420, 850, 0),
            'Attrezzo_Provino_Tasche_Base': (520, 850, 0), 'Attrezzo_Provino_Tasche_Lama': (520, 880, 0),
            'Dima_Calettamento': (0, 1000, 0), 'Attrezzo_Provino_Inserti': (200, 1000, 0),
            'Attrezzo_Bussola_Perno': (260, 1000, 0), 'Attrezzo_Estrattore_Asta': (300, 1000, 0),
            'Attrezzo_Estrattore_Tubo': (340, 1000, 0)}
# provino di luce (X10, D-069): profondita' delle camere sopra la striscia e spessori del bianco da provare
PROV_CAMERE = (2.0, 4.0, 6.0)
PROV_BIANCO = (0.4, 0.8, 1.2, 1.6)
# provino delle tasche della lama A (D-072): diametri lisci attorno a cov_testa_d (5,6; testa ISO 4762 da 5,32 a 5,5) e
# tasche da 6,0 con tre costole di schiacciamento che stringono al diametro dato
PROV_TASCHE = (5.4, 5.5, 5.6, 5.7)
PROV_COSTOLE = (5.3, 5.4)
PROV_COSTOLA_D, PROV_FORO_COSTOLE, PROV_PASSO = 1.0, 6.0, 10.0
# provino degli inserti (P-057, D-076): inserti del kit con zigrinatura 4,2 e invito 4,0 (M3), 3,2 e 3,0 (M2), quindi
# fori attorno all'invito; l'ultimo di ogni riga e' il valore di oggi (ins_m3_d, ins_m2_d), di controllo
PROV_INS_M3 = (3.9, 4.0, 4.1, 4.2)
PROV_INS_M2 = (2.9, 3.0, 3.1, 3.4)
# passo fra i fori 9: fra due fori da 4,2 restano 4,8 (piu' di due pareti cul_ins_parete da 1,6); il bordo del blocco
# sta a cul_ins_parete dal foro piu' grande, come nelle bugne; fondo sotto i fori M3 da 2
PROV_INS_PASSO, PROV_INS_FONDO = 9.0, 2.0
# scritte: alte 4 in grassetto (tratto di circa 0,6, una passata dell'ugello da 0,4), incise 0,6 (tre strati da 0,2)
PROV_INS_TESTO_H, PROV_INS_TESTO_P = 4.0, 0.6


def _mm(des, expr):
    return des.unitsManager.evaluateExpression(expr, 'mm') * 10.0


def _f(v):
    return '%.4f mm' % v if v >= 0 else '-(%.4f mm)' % -v


def _rot(p, c, ang):
    """Rotazione antioraria di ang gradi nel piano (x, z) attorno a c."""
    a = math.radians(ang)
    x, z = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - z * math.sin(a), c[1] + x * math.sin(a) + z * math.cos(a))


def _rett(p, nome, pa, pb, a0, a1, b0, b1, y, h, op=UNISCI):
    """Rettangolo nel piano 'y' (u, v) = (x, z) in una terna locale (a da pa verso pb, b = a ruotato di +90 gradi),
    estruso verso +Y: inclinato con blocco_obl, dritto con blocco se la direzione e' parallela a X o a Z (sk_rett_obl
    non accetta un asse parallelo agli assi dello schizzo)."""
    ux, uz = pb[0] - pa[0], pb[1] - pa[1]
    n = math.hypot(ux, uz)
    ux, uz = ux / n, uz / n
    if abs(ux) > 1e-9 and abs(uz) > 1e-9:
        return p.blocco_obl('y', _f(y), nome, (_f(pa[0]), _f(pa[1])), (_f(pb[0]), _f(pb[1])), _f(a0), _f(a1), _f(b0), _f(b1), _f(h), 1, op)
    bx, bz = -uz, ux
    xs = [pa[0] + a * ux + b * bx for a in (a0, a1) for b in (b0, b1)]
    zs = [pa[1] + a * uz + b * bz for a in (a0, a1) for b in (b0, b1)]
    return p.blocco('y', _f(y), nome, _f(min(xs)), _f(min(zs)), _f(max(xs)), _f(max(zs)), _f(h), 1, op)


def _comp(root, nome):
    """Componente nuovo alla radice nella posizione di libreria (cancella quello con lo stesso nome)."""
    while L['trova_occ'](root, nome):
        L['trova_occ'](root, nome)[0].deleteMe()
    t = adsk.core.Matrix3D.create()
    x, y, z = LIBRERIA[nome]
    t.translation = adsk.core.Vector3D.create(x / 10, y / 10, z / 10)
    occ = root.occurrences.addNewComponent(t)
    occ.component.name = nome
    return occ


def geometria_dima(des, posa):
    """Punti (terna della zampa come costruita, piano x-z; il femore e' la terna della dima) dei tre contatti."""
    yaw, alfa, gamma = posa
    lc, lf = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lf')
    H, K = (lc, 0.0), (lc + lf, 0.0)
    cs, zc = _mm(des, 'cul_semi'), _mm(des, 'att_z_contatto')
    out = {'H': H, 'K': K}
    # femore: faccia +X della culla della coxa; nella terna del femore la coxa e' ruotata di -alfa attorno all'anca
    out['femore'] = (_rot((lc + cs, -zc), H, -alfa), _rot((lc + cs, -zc - 10), H, -alfa))
    # ginocchio: faccia -X della culla della tibia, ruotata di gamma - 90 attorno al ginocchio
    out['ginocchio'] = (_rot((lc + lf - cs, -zc), K, gamma - 90), _rot((lc + lf - cs, -zc - 10), K, gamma - 90))
    # imbardata: fianco -Y della cassa del servo di coxa (fisso nel corpo); nella terna della zampa il corpo e' ruotato
    # di -yaw attorno all'asse della coxa, poi nella terna del femore di -alfa attorno all'anca
    a, b = _mm(des, 'att_punta_a'), -_mm(des, 'srv_cassa_w') / 2
    z = _mm(des, 'cz_alette_coxa') + _mm(des, 'att_punta_z')
    t = math.radians(-yaw)
    px, py = a * math.cos(t) - b * math.sin(t), a * math.sin(t) + b * math.cos(t)
    nx, ny = math.sin(t), -math.cos(t)                         # normale del fianco, verso la punta
    pf = _rot((px, z), H, -alfa)
    nxf, nzf = _rot((nx, 0.0), (0.0, 0.0), -alfa)
    r = _mm(des, 'att_punta_d') / 2
    # la punta e' un cilindro lungo Y sul punto di contatto: finisce dove il suo bordo tocca il piano del fianco
    y_fine = py + r * math.hypot(nxf, nzf) / ny
    out['imbardata'] = {'xz': pf, 'y_contatto': py, 'y_fine': y_fine}
    return out


def fai_dima(des, root, nome):
    posa = POSE[nome]
    g = geometria_dima(des, posa)
    occ = _comp(root, nome)
    p = Parte(occ.component)
    y0 = _mm(des, 'zy_B_est')                                    # faccia esterna dei mozzi di Femore_B
    sp = _mm(des, 'att_sp')
    yb = y0 - sp                                                 # retro della piastra
    ye = _mm(des, 'zy_fondo_est') + _mm(des, 'att_entra')        # fine dei denti, oltre il fondo delle culle
    (hx, hz), kx = g['H'], g['K'][0]
    # piastra sui due mozzi, con i fori sui perni
    p.blocco('y', _f(yb), 'piastra', _f(hx - 14), _f(-14), _f(kx + 14), _f(14), _f(sp), 1, NUOVO)
    dl, dt = _mm(des, 'att_dente_l'), _mm(des, 'att_dente')
    bw = _mm(des, 'att_braccio_w')
    for k, ((ax, az), (bx, bz)), lato, centro in (('femore', g['femore'], 1, g['H']), ('ginocchio', g['ginocchio'], -1, g['K'])):
        # dente: la faccia di contatto passa per il punto a; b = a ruotato di +90 gradi (verso +X sulla culla della coxa,
        # dentro la culla della tibia), quindi il dente sta a b > 0 per il femore e a b < 0 per il ginocchio
        b0, b1 = (0.0, dt) if lato > 0 else (-dt, 0.0)
        _rett(p, 'dente_' + k, (ax, az), (bx, bz), -dl / 2, dl / 2, b0, b1, yb, ye - yb)
        # braccio nel piano della piastra dal dente al mozzo
        ux, uz = bx - ax, bz - az
        n = math.hypot(ux, uz)
        mx, mz = ax + lato * (-uz / n) * dt / 2, az + lato * (ux / n) * dt / 2      # centro del dente
        lung = math.hypot(centro[0] - mx, centro[1] - mz)
        _rett(p, 'braccio_' + k, (mx, mz), centro, 0, lung, -bw / 2, bw / 2, yb, sp)
    # imbardata: braccio nel piano della piastra fino sopra il punto di contatto, poi punta lungo Y
    (cx, cz), yf = g['imbardata']['xz'], g['imbardata']['y_fine']
    lung = math.hypot(hx - cx, hz - cz)
    _rett(p, 'braccio_imbardata', (cx, cz), (hx, hz), -bw / 2, lung, -bw / 2, bw / 2, yb, sp)
    p.cilindro('y', _f(yb), 'punta_imbardata', _f(cx), _f(cz), 'att_punta_d', _f(yf - yb), 1)
    # fori sui perni per ultimi: i bracci arrivano al centro dei mozzi
    for k, (x, z) in (('anca', g['H']), ('ginocchio', g['K'])):
        p.cilindro('y', _f(yb), 'foro_perno_' + k, _f(x), _f(z), 'perno_d + 2 * att_gio_perno', _f(sp), 1, TAGLIA)
    corpo = occ.component.bRepBodies
    p.info = {'corpi': corpo.count, 'volume_cm3': round(sum(b.volume for b in corpo), 2), 'posa': posa,
              'contatti': {k: [round(v, 2) for v in g[k][0]] for k in ('femore', 'ginocchio')},
              'imbardata': {k: (round(v, 2) if isinstance(v, float) else [round(w, 2) for w in v]) for k, v in g['imbardata'].items()}}
    return occ, p


def fai_cavalletto(des, root):
    """Cavalletto nella terna del robot (la posizione di libreria si toglie per le verifiche)."""
    occ = _comp(root, 'Attrezzo_Cavalletto')
    p = Parte(occ.component)
    zk = -_mm(des, 'cor_chiglia')                               # fondo della chiglia
    ys = _mm(des, 'cor_tun_semi') + _mm(des, 'cav_gio')
    pw, cx = _mm(des, 'cav_parete'), _mm(des, 'cav_culla_x')
    zt = _mm(des, 'cav_z_tavolo')
    zc = zk - 6.0                                                # fondo della culla
    lab = _mm(des, 'cav_labbro')
    p.blocco('z', _f(zc), 'culla', _f(-cx), _f(-(ys + pw)), _f(cx), _f(ys + pw), _f(zk - zc + lab), 1, NUOVO)
    p.blocco('z', _f(zk), 'culla_vuoto', _f(-cx - 1), _f(-ys), _f(cx + 1), _f(ys), _f(lab + 1), 1, TAGLIA)
    p.blocco('z', _f(zt + 5), 'colonna', _f(-30), _f(-20), _f(30), _f(20), _f(zc - zt - 5))
    p.blocco('z', _f(zt + 5 + pw), 'colonna_vuoto', _f(-30 + pw), _f(-20 + pw), _f(30 - pw), _f(20 - pw), _f(zc - zt - 5 - 2 * pw), 1, TAGLIA)
    p.blocco('z', _f(zt), 'base', _f(-80), _f(-60), _f(80), _f(60), _f(5))
    corpo = occ.component.bRepBodies
    p.info = {'corpi': corpo.count, 'volume_cm3': round(sum(b.volume for b in corpo), 2), 'altezza_mm': round(zk + lab - zt, 1)}
    return occ, p


def fai_provino_luce(des, root):
    """Provino di luce (X10, D-069) in due componenti, nero e bianco, da stampare insieme in due colori con il fondo sul
    piatto. Uno spezzone di striscia a 120 LED/m si infila nel canale sotto (alto 1,6): sotto ogni camera cade sempre un
    LED. Riga 1: tre camere profonde PROV_CAMERE (dal canale al bianco da 1,6), ciascuna coperta da quattro strisce di
    bianco spesse PROV_BIANCO. Riga 2: l'anello del pulsante come sul carapace (camera nera luc_camera_D x luc_camera_h,
    bianco car_sp con l'intarsio nero car_fascia_h, anello luc_anello_r0..r1 assottigliato da sotto a luc_bianco)."""
    nero, bianco = _comp(root, 'Attrezzo_Provino_Luce_Nero'), _comp(root, 'Attrezzo_Provino_Luce_Bianco')
    pn, pb = Parte(nero.component), Parte(bianco.component)
    can, cav, w = 1.6, 16.0, 2.0                                    # canale, lato delle camere, pareti
    sp, fa, bi = _mm(des, 'car_sp'), _mm(des, 'car_fascia_h'), _mm(des, 'luc_bianco')
    r0, r1 = _mm(des, 'luc_anello_r0'), _mm(des, 'luc_anello_r1')
    dc, hc = _mm(des, 'luc_camera_D') - 2 * _mm(des, 'luc_camera_sp'), _mm(des, 'luc_camera_h')
    xs = [-(cav + w), 0.0, cav + w]
    y0, y1 = 0.0, cav + 2                                           # cavita' della riga 1 in y
    zt = [can + d + max(PROV_BIANCO) for d in PROV_CAMERE]
    op = NUOVO
    for i, (xc, z) in enumerate(zip(xs, zt)):
        pn.blocco('z', _f(0), 'blocco_%d' % i, _f(xc - cav / 2 - w), _f(y0 - w), _f(xc + cav / 2 + w), _f(y1 + w), _f(z), 1, op)
        op = UNISCI
    yr, zr = -(dc / 2 + w + 2), can + hc + sp                       # centro e cima dell'anello
    pn.blocco('z', _f(0), 'blocco_anello', _f(-(dc / 2 + w)), _f(yr - dc / 2 - w), _f(dc / 2 + w), _f(y0 - w), _f(zr), 1, UNISCI)
    for i, (xc, z) in enumerate(zip(xs, zt)):
        pn.blocco('z', _f(can), 'camera_%d' % i, _f(xc - cav / 2), _f(y0), _f(xc + cav / 2), _f(y1), _f(z - can), 1, TAGLIA)
    pn.cilindro('z', _f(can), 'camera_anello', _f(0), _f(yr), _f(dc), _f(zr - can), 1, TAGLIA)
    pn.blocco('z', _f(0), 'canale', _f(xs[0] - cav), _f((y0 + y1) / 2 - 2.3), _f(xs[2] + cav), _f((y0 + y1) / 2 + 2.3), _f(can), 1, TAGLIA)
    yl = yr + (r0 + r1) / 2                                         # i pixel stanno sotto l'anello, come nel fondo vero
    pn.blocco('z', _f(0), 'canale_anello', _f(-(dc / 2 + w + 1)), _f(yl - 2.3), _f(dc / 2 + w + 1), _f(yl + 2.3), _f(can), 1, TAGLIA)
    # intarsio nero sopra il bianco dell'anello, aperto sull'anello
    pn.cilindro('z', _f(zr - fa), 'intarsio', _f(0), _f(yr), _f(dc), _f(fa), 1, UNISCI)
    pn.cilindro('z', _f(zr - fa), 'intarsio_anello', _f(0), _f(yr), _f(2 * r1), _f(fa), 1, TAGLIA)
    pn.cilindro('z', _f(zr - fa), 'intarsio_dentro', _f(0), _f(yr), _f(2 * r0), _f(fa), 1, UNISCI)
    # bianco: strisce sulle tre camere e pelle dell'anello
    for i, (xc, z) in enumerate(zip(xs, zt)):
        for k, t in enumerate(PROV_BIANCO):                         # le strisce di una camera si toccano: un corpo
            xa = xc - cav / 2 + k * cav / len(PROV_BIANCO)
            pb.blocco('z', _f(z - t), 'bianco_%d_%d' % (i, k), _f(xa), _f(y0), _f(xa + cav / len(PROV_BIANCO)), _f(y1), _f(t), 1,
                      NUOVO if k == 0 else UNISCI)
    pb.cilindro('z', _f(zr - sp), 'pelle_anello', _f(0), _f(yr), _f(dc), _f(sp - fa), 1, NUOVO)
    pb.cilindro('z', _f(zr - fa), 'anello', _f(0), _f(yr), _f(2 * r1), _f(fa), 1, UNISCI)
    pb.cilindro('z', _f(zr - fa), 'anello_dentro', _f(0), _f(yr), _f(2 * r0), _f(fa), 1, TAGLIA)
    pb.cilindro('z', _f(zr - sp), 'gola', _f(0), _f(yr), _f(2 * r1), _f(sp - bi), 1, TAGLIA)
    pb.cilindro('z', _f(zr - sp), 'gola_dentro', _f(0), _f(yr), _f(2 * r0), _f(sp - bi), 1, UNISCI)
    for o, p in ((nero, pn), (bianco, pb)):
        c = o.component.bRepBodies
        p.info = {'corpi': c.count, 'volume_cm3': round(sum(b.volume for b in c), 3)}
    return nero, pn, bianco, pb


def fai_provino_tasche(des, root):
    """Provino delle tasche della lama A (D-072). Base in PETG-CF con una vite M3 x 6 ISO 4762 in un foro pilota (come le
    alette lato albero, D-049): la testa sta in piedi come quelle del blocco del femore. Lamina in PLA spessa come la lama
    A (cov_fem_sp_a) e stampata come lei, con le tasche sul piatto: quattro lisce PROV_TASCHE e due da PROV_FORO_COSTOLE
    con tre costole che stringono a PROV_COSTOLE, profonde come nella lama (testa piu' cov_fem_tasca_gio). Accanto alla
    tasca i-esima, sulla faccia in alto, i puntini (da 1 a 6) per riconoscerla."""
    base, lama = _comp(root, 'Attrezzo_Provino_Tasche_Base'), _comp(root, 'Attrezzo_Provino_Tasche_Lama')
    pb, pl = Parte(base.component), Parte(lama.component)
    pb.blocco('z', _f(0), 'base', _f(-12), _f(-8), _f(12), _f(8), _f(8), 1, NUOVO)
    pb.cilindro('z', _f(8), 'pilota', _f(0), _f(0), 'vite_m3_pilota', _f(7), -1, TAGLIA)
    sp, prof = _mm(des, 'cov_fem_sp_a'), _mm(des, 'vite_m3_testa_h') + _mm(des, 'cov_fem_tasca_gio')
    tasche = [(d, None) for d in PROV_TASCHE] + [(PROV_FORO_COSTOLE, d) for d in PROV_COSTOLE]
    n = len(tasche)
    x0 = -(n - 1) * PROV_PASSO / 2
    pl.blocco('z', _f(0), 'lamina', _f(x0 - PROV_PASSO / 2), _f(-7), _f(-x0 + PROV_PASSO / 2), _f(7), _f(sp), 1, NUOVO)
    for i, (d, stretta) in enumerate(tasche):
        xc = x0 + i * PROV_PASSO
        pl.cilindro('z', _f(0), 'tasca_%d' % (i + 1), _f(xc), _f(0), _f(d), _f(prof), 1, TAGLIA)
        if stretta is not None:                    # costole: cilindri lungo la tasca, tangenti al cerchio della stretta
            rc = stretta / 2 + PROV_COSTOLA_D / 2
            for k in range(3):
                a = math.radians(90 + 120 * k)
                pl.cilindro('z', _f(0), 'costola_%d_%d' % (i + 1, k), _f(xc + rc * math.cos(a)), _f(rc * math.sin(a)),
                            _f(PROV_COSTOLA_D), _f(prof), 1, UNISCI)
        for k in range(i + 1):                     # puntini sulla faccia in alto, verso +Y
            pl.cilindro('z', _f(sp), 'puntino_%d_%d' % (i + 1, k), _f(xc - 3.75 + 1.5 * k), _f(5.2), _f(1.0), _f(0.4), -1, TAGLIA)
    for o, p in ((base, pb), (lama, pl)):
        c = o.component.bRepBodies
        p.info = {'corpi': c.count, 'volume_cm3': round(sum(b.volume for b in c), 3)}
    pl.info['tasche'] = [('%.1f' % d) if s_ is None else 'costole %.1f in %.1f' % (s_, d) for d, s_ in tasche]
    return base, pb, lama, pl


def _incidi(p, nome, testo, x, y, z_expr):
    """Scritta incisa sulla faccia z = z_expr, centrata in (x, y): testo in grassetto alto PROV_INS_TESTO_H, profondo
    PROV_INS_TESTO_P, tagliato solo nei corpi della parte."""
    piano = p.piano('z', z_expr, nome)
    sk = p._schizzo(piano, nome)
    z = p.val(z_expr)
    h = PROV_INS_TESTO_H
    a = sk.modelToSketchSpace(P3((x - PROV_INS_PASSO / 2) / 10, (y - h / 2 - 0.5) / 10, z / 10))
    b = sk.modelToSketchSpace(P3((x + PROV_INS_PASSO / 2) / 10, (y + h / 2 + 0.5) / 10, z / 10))
    ti = sk.sketchTexts.createInput2(testo, h / 10)
    ti.setAsMultiLine(P3(min(a.x, b.x), min(a.y, b.y), 0), P3(max(a.x, b.x), max(a.y, b.y), 0),
                      adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
                      adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    ti.textStyle = adsk.fusion.TextStyles.TextStyleBold
    t = sk.sketchTexts.add(ti)
    # il riquadro della scritta e' un rettangolo libero di muoversi e ruotare (i lati restano perpendicolari: un secondo
    # vincolo orizzontale o verticale lo rende ipervincolato): un lato orizzontale e due angoli quotati dall'origine
    linee = adsk.fusion.MultiLineTextDefinition.cast(t.definition).rectangleLines
    s_, e_ = linee[0].startSketchPoint.geometry, linee[0].endSketchPoint.geometry
    if abs(s_.y - e_.y) < abs(s_.x - e_.x):
        sk.geometricConstraints.addHorizontal(linee[0])
    else:
        sk.geometricConstraints.addVertical(linee[0])
    for ln in (linee[0], linee[2]):
        g = ln.startSketchPoint.geometry                     # coordinate dello schizzo (cm)
        p._quota_da_origine(sk, ln.startSketchPoint, True, _f(g.x * 10))
        p._quota_da_origine(sk, ln.startSketchPoint, False, _f(g.y * 10))
    # con una scritta Fusion da' isFullyConstrained falso anche con riquadro, lati e punti tutti vincolati (provato il
    # 16 ottobre 2026 sul provino degli inserti): si controllano i lati del riquadro
    if not all(ln.isFullyConstrained for ln in linee):
        p.non_vincolati.append(sk.name)
    ext = p.c.features.extrudeFeatures
    inp = ext.createInput(t, TAGLIA)
    nrm = sk.xDirection.crossProduct(sk.yDirection)
    inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString('%g mm' % PROV_INS_TESTO_P)),
                         adsk.fusion.ExtentDirections.NegativeExtentDirection if nrm.z > 0
                         else adsk.fusion.ExtentDirections.PositiveExtentDirection)
    inp.participantBodies = [bd for bd in p.c.bRepBodies]
    f = ext.add(inp)
    f.name = nome
    p.n += 1
    return f


def fai_provino_inserti(des, root):
    """Provino degli inserti (P-057), PETG-CF, stampato con la faccia dei fori in alto. Riga dietro: fori M3 PROV_INS_M3
    profondi ins_m3_l; riga davanti: fori M2 PROV_INS_M2 profondi ins_m2_l; sopra ogni foro il diametro inciso. Il
    valore scelto va in ins_m3_d / ins_m2_d (CLAUDE.md, provini)."""
    occ = _comp(root, 'Attrezzo_Provino_Inserti')
    p = Parte(occ.component)
    par = _mm(des, 'cul_ins_parete')
    n = len(PROV_INS_M3)
    xs = [(i - (n - 1) / 2) * PROV_INS_PASSO for i in range(n)]
    y3, y2 = 4.0, -8.0                                 # centri delle due righe; le scritte stanno 5,5 sopra ciascuna
    dm3, dm2 = max(PROV_INS_M3), max(PROV_INS_M2)
    x1 = max(xs[-1] + dm3 / 2 + par, xs[-1] + PROV_INS_PASSO / 2 + 0.5)    # scritte larghe circa 7,4: 1,3 dal bordo
    y0 = y2 - dm2 / 2 - par
    y1 = y3 + 5.5 + PROV_INS_TESTO_H / 2 + 1.0
    alto = 'ins_m3_l + %g mm' % PROV_INS_FONDO
    p.blocco('z', '0 mm', 'blocco', _f(-x1), _f(y0), _f(x1), _f(y1), alto, 1, NUOVO)
    for riga, y, diametri, prof in (('m3', y3, PROV_INS_M3, 'ins_m3_l'), ('m2', y2, PROV_INS_M2, 'ins_m2_l')):
        for x, d in zip(xs, diametri):
            k = ('%.1f' % d).replace('.', '_')
            p.cilindro('z', alto, 'foro_%s_%s' % (riga, k), _f(x), _f(y), _f(d), prof, -1, TAGLIA)
            _incidi(p, 'testo_%s_%s' % (riga, k), '%.1f' % d, x, y + 5.5, alto)
    c = occ.component.bRepBodies
    p.info = {'corpi': c.count, 'volume_cm3': round(sum(b.volume for b in c), 3),
              'ingombro_mm': [round(2 * x1, 2), round(y1 - y0, 2), round(_mm(des, alto), 2)],
              'fori': {'m3': list(PROV_INS_M3), 'm2': list(PROV_INS_M2)}}
    return occ, p


def fai_bussola_perno(des, root):
    """Bussola di battuta del perno (P-065): cilindro con la faccia in alto contro il mozzo del femore B (o il braccio
    della coxa, stesso spessore), la tasca del rialzo e il foro cieco att_bus_d profondo att_bus_prof."""
    occ = _comp(root, 'Attrezzo_Bussola_Perno')
    p = Parte(occ.component)
    alto = 'att_bus_fondo + att_bus_prof'
    p.cilindro('z', '0 mm', 'corpo', '0 mm', '0 mm', 'att_bus_D', alto, 1, NUOVO)
    p.cilindro('z', alto, 'tasca_rialzo', '0 mm', '0 mm', 'cus_rialzo_d + 2 * att_bus_gio', 'cus_rialzo_h + att_bus_gio', -1, TAGLIA)
    p.cilindro('z', alto, 'foro', '0 mm', '0 mm', 'att_bus_d', 'att_bus_prof', -1, TAGLIA)
    c = occ.component.bRepBodies
    p.info = {'corpi': c.count, 'volume_cm3': round(sum(b.volume for b in c), 3), 'alto_mm': round(_mm(des, alto), 3),
              'prof_mm': round(_mm(des, 'att_bus_prof'), 3)}
    return occ, p


def fai_estrattore(des, root):
    """Estrattore (P-065): asta (punta, spalla, gambo, testa; asse z, punta a z 0, si stampa in piedi sulla testa) e
    tubo d'appoggio (asse z, da z 0 a att_tubo_h)."""
    asta, tubo = _comp(root, 'Attrezzo_Estrattore_Asta'), _comp(root, 'Attrezzo_Estrattore_Tubo')
    pa, pt = Parte(asta.component), Parte(tubo.component)
    z1 = 'att_estr_pilota_l'
    z2 = z1 + ' + att_estr_spalla_l'
    z3 = z2 + ' + att_estr_gambo_l'
    pa.cilindro('z', '0 mm', 'punta', '0 mm', '0 mm', 'att_estr_pilota_d', 'att_estr_pilota_l', 1, NUOVO)
    pa.cilindro('z', z1, 'spalla', '0 mm', '0 mm', 'att_estr_d', 'att_estr_spalla_l', 1, UNISCI)
    pa.cilindro('z', z2, 'gambo', '0 mm', '0 mm', 'att_estr_gambo_d', 'att_estr_gambo_l', 1, UNISCI)
    pa.cilindro('z', z3, 'testa', '0 mm', '0 mm', 'att_estr_testa_d', 'att_estr_testa_h', 1, UNISCI)
    pt.cilindro('z', '0 mm', 'tubo', '0 mm', '0 mm', 'att_tubo_D', 'att_tubo_h', 1, NUOVO)
    pt.cilindro('z', '0 mm', 'vuoto', '0 mm', '0 mm', 'att_tubo_d', 'att_tubo_h', 1, TAGLIA)
    for o, p in ((asta, pa), (tubo, pt)):
        c = o.component.bRepBodies
        p.info = {'corpi': c.count, 'volume_cm3': round(sum(b.volume for b in c), 3)}
    pa.info['lungo_mm'] = round(_mm(des, z3 + ' + att_estr_testa_h'), 3)
    return asta, pa, tubo, pt


def _chiudi(des, t0, nome, p):
    L['raggruppa'](des, t0, nome)
    return dict({'lavorazioni': p.n, 'schizzi_non_vincolati': p.non_vincolati}, **getattr(p, 'info', {}))


def _copia(root, nome, m):
    """Occorrenza provvisoria alla radice del componente di libreria `nome` nella matrice m (terna del robot)."""
    lib = [o for o in root.occurrences if o.component.name == nome][0]
    o = root.occurrences.addExistingComponent(lib.component, m)
    o.isLightBulbOn = True
    return o


def verifica_dime(des, root, zampa, solo=None):
    """Ogni dima (o quelle in `solo`) su una zampa atteggiata nella sua posa: interferenze con zampa e corpo (attese:
    nessuna) e distanza dei tre denti dalle loro facce (attesa: zero, contatto)."""
    AS = runpy.run_path(os.path.join(QUI, 'assieme.py'))
    out = {}
    zo = AS['mappa_zampe'](des, root)[zampa]
    corpo = AS['_corpo'](root)
    fb = [o for o in zo.component.occurrences if o.component.name == 'Femore_B'][0]
    nomi = list(solo or POSE)
    copie = {n: _copia(root, n, adsk.core.Matrix3D.create()) for n in nomi}
    try:
        for nome in nomi:
            yaw, alfa, gamma = POSE[nome]
            AS['posa_zampa'](des, zo, yaw, alfa, gamma)
            # terna della dima = terna della zampa come costruita portata con il femore: nativa^-1, poi proxy
            m = fb.transform2.copy()
            m.invert()
            m.transformBy(fb.createForAssemblyContext(zo).transform2)
            copie[nome].transform2 = m
            r = A['interferenze'](des, [copie[nome], zo, corpo])
            urti = sorted(set('%s/%s %.2f' % (a.split('+')[-1].split(':')[0], b.split('+')[-1].split(':')[0], v) for a, b, v in r
                              if nome in a or nome in b))
            mm = adsk.core.Application.get().measureManager
            dist = {}
            for parte in ('Coxa', 'Tibia'):
                po = [o for o in zo.childOccurrences if o.component.name == parte][0]
                dist[parte] = round(min(mm.measureMinimumDistance(b, c).value * 10 for b in copie[nome].bRepBodies
                                        for c in po.bRepBodies), 3)
            serv = [o for o in corpo.childOccurrences if o.component.name == 'Rif_Servo_MG996R'
                    and abs(o.transform2.translation.x * 10 - AS['coxe'](des)[zampa][0]) < 1
                    and abs(o.transform2.translation.y * 10 - AS['coxe'](des)[zampa][1]) < 1][0]
            dist['servo_coxa'] = round(min(mm.measureMinimumDistance(b, c).value * 10 for b in copie[nome].bRepBodies
                                           for c in serv.bRepBodies), 3)
            out[nome] = {'urti': urti or 'nessuno', 'distanze_mm': dist}
            A['ripristina'](des)
    finally:
        if des.snapshots.hasPendingSnapshot:
            des.snapshots.revertPendingSnapshot()
        for o in copie.values():
            o.deleteMe()
    return out


def verifica_cavalletto(des, root):
    """Cavalletto sotto il robot: interferenze nella posa di riferimento e con ogni zampa nelle pose piu' basse e
    ripiegate sotto il corpo (femore -45/-49, ginocchio al minimo e a 139, imbardata -35, 0, +35)."""
    AS = runpy.run_path(os.path.join(QUI, 'assieme.py'))
    out = {}
    cav = _copia(root, 'Attrezzo_Cavalletto', adsk.core.Matrix3D.create())
    try:
        occ = [o for o in root.occurrences if o.component.name in ('Corpo', 'Zampa')]
        r = A['interferenze'](des, [cav] + occ)
        out['riferimento'] = sorted(set('%s/%s' % (a.split('+')[-1].split(':')[0], b.split('+')[-1].split(':')[0]) for a, b, v in r
                                        if 'Attrezzo' in a or 'Attrezzo' in b)) or 'nessuno'
        mz = AS['mappa_zampe'](des, root)
        for n in ('AS', 'MS', 'PS'):
            for yaw in (-35.0, 0.0, 35.0):
                for alfa, gamma in ((-45.0, 54.0), (-49.0, 139.0)):
                    AS['posa_zampa'](des, mz[n], yaw, alfa, gamma)
                    r = [x for x in A['interferenze'](des, [cav, mz[n]]) if 'Attrezzo' in x[0] or 'Attrezzo' in x[1]]
                    if r:
                        out.setdefault('urti', []).append('%s %+g %g/%g' % (n, yaw, alfa, gamma))
                    A['ripristina'](des)
        out.setdefault('urti', 'nessuno nelle 18 pose')
    finally:
        if des.snapshots.hasPendingSnapshot:
            des.snapshots.revertPendingSnapshot()
        cav.deleteMe()
    return out


# ---------------------------------------------------------------- verifiche di bussola ed estrattore (corpi temporanei)
def _terna(proxy):
    """Matrice dalla terna della zampa come costruita al mondo per la parte annidata `proxy` (nativa^-1, poi proxy)."""
    m = proxy.nativeObject.transform2.copy()
    m.invert()
    m.transformBy(proxy.transform2)
    return m


def _assi(xc, y, verso_y):
    """Terna dell'attrezzo nella zampa: asse z dell'attrezzo lungo Y della zampa (verso_y +1 o -1), x lungo X, origine
    sull'asse del giunto (xc, y, 0) in mm."""
    m = adsk.core.Matrix3D.create()
    m.setWithCoordinateSystem(P3(xc / 10, y / 10, 0), V3(1, 0, 0), V3(0, 0, -verso_y), V3(0, verso_y, 0))
    return m


def _sposta(m, dx=0.0, dz=0.0):
    """m preceduta da uno spostamento (mm) lungo x e z dell'attrezzo."""
    s = adsk.core.Matrix3D.create()
    s.translation = V3(dx / 10, 0, dz / 10)
    s.transformBy(m)
    return s


def _corpi_attrezzo(root, nome, m):
    tbm = adsk.fusion.TemporaryBRepManager.get()
    comp = [o for o in root.occurrences if o.component.name == nome][0].component
    out = []
    for b in comp.bRepBodies:
        t = tbm.copy(b)
        tbm.transform(t, m)
        out.append((nome, t))
    return out


def _corpi_spostati(corpi, v_mondo):
    """Copie temporanee di corpi del modello [(nome, corpo)] traslate di v_mondo (cm)."""
    tbm = adsk.fusion.TemporaryBRepManager.get()
    s = adsk.core.Matrix3D.create()
    s.translation = v_mondo
    out = []
    for n, b in corpi:
        t = tbm.copy(b)
        tbm.transform(t, s)
        out.append((n, t))
    return out


def _vol(mobili, fissi):
    """Volume (mm3) delle intersezioni fra corpi temporanei e corpi (del modello o temporanei)."""
    tbm = adsk.fusion.TemporaryBRepManager.get()
    v = 0.0
    for _, a in mobili:
        for _, b in fissi:
            c = tbm.copy(a)
            if tbm.booleanOperation(c, tbm.copy(b), adsk.fusion.BooleanTypes.IntersectionBooleanType):
                v += c.volume * 1000
    return round(v, 3)


def _gioco(fab, fissi, hi=2.0, it=10):
    """Gioco per bisezione: fab(g) da' i corpi spostati di g; contatto al primo g con intersezione (caso di controllo)."""
    if _vol(fab(0.0), fissi) > 1e-4:
        return 0.0
    if _vol(fab(hi), fissi) <= 1e-4:
        return '>%g' % hi
    lo = 0.0
    for _ in range(it):
        mid = (lo + hi) / 2
        if _vol(fab(mid), fissi) > 1e-4:
            hi = mid
        else:
            lo = mid
    return round(lo, 3)


def _parti_zampa(des, root, zampa):
    """Proxy delle parti della zampa: per nome del componente e, per perni e cuscinetti (stesso componente), con i nomi
    di zampa.py (ISTANZE) riconosciuti dalla X nella terna della zampa come costruita."""
    AS = runpy.run_path(os.path.join(QUI, 'assieme.py'))
    zo = AS['mappa_zampe'](des, root)[zampa]
    lc, lk = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lc + zam_Lf')
    ruoli = {'Rif_Perno_5': {0.0: 'Perno_Coxa', lc: 'Perno_Femore', lk: 'Perno_Ginocchio'},
             'Rif_Cuscinetto_LF1050ZZ': {lc: 'Cuscinetto_Femore', lk: 'Cuscinetto_Ginocchio'}}
    out = {}
    for o in zo.childOccurrences:
        n = o.component.name
        if n in ruoli:
            x = o.nativeObject.transform2.translation.x * 10
            for xr, nome in ruoli[n].items():
                if abs(x - xr) < 0.5:
                    out[nome] = o
        else:
            out[n] = o
    return out


def verifica_bussola(des, root, zampa):
    """Bussola sotto i due mozzi del femore B della zampa, con i perni dove li mette il modello (sporgenza perno_sporge).
    Attesi: nessuna intersezione; la bussola tocca il mozzo (0,05 piu' in su interseca il femore B) e il perno tocca il
    fondo (0,05 piu' in giu' interseca la bussola); rialzo libero nella tasca."""
    po = _parti_zampa(des, root, zampa)
    fb = po['Femore_B']
    m_f = _terna(fb)
    alto = _mm(des, 'att_bus_fondo + att_bus_prof')
    yi = _mm(des, 'zy_B_int')
    out = {}
    for giunto, xc, perno in (('anca', _mm(des, 'zam_Lc'), 'Perno_Femore'), ('ginocchio', _mm(des, 'zam_Lc + zam_Lf'), 'Perno_Ginocchio')):
        m0 = _assi(xc, yi + alto, -1)                     # z della bussola verso -Y: la faccia in alto sta a zy_B_int
        def bus(dz=0.0):
            return _corpi_attrezzo(root, 'Attrezzo_Bussola_Perno', _mondo(_sposta(m0, dz=dz), m_f))
        fem = [('Femore_B', b) for b in fb.bRepBodies]
        pe = [(perno, b) for b in po[perno].bRepBodies]
        # direzione +Y della zampa nel mondo (verso il fondo del foro della bussola)
        vy = _dir_mondo(m_f, 0, 1, 0)
        r = {'bussola_femore_mm3': _vol(bus(), fem), 'bussola_perno_mm3': _vol(bus(), pe),
             'controllo_bussola_su_0.05_mm3': _vol(bus(0.05), fem),
             'controllo_perno_giu_0.05_mm3': _vol(_corpi_spostati(pe, _scala(vy, 0.005)), bus()),
             'gioco_perno_fondo_mm': _gioco(lambda g: _corpi_spostati(pe, _scala(vy, g / 10)), bus(), hi=1.0),
             'gioco_bussola_mozzo_mm': _gioco(lambda g: bus(g), fem, hi=1.0)}
        # sporgenza del perno fuori dalla faccia esterna con il perno sul fondo: perno_sporge meno il gioco
        g = r['gioco_perno_fondo_mm']
        r['sporgenza_mm'] = round(_mm(des, 'perno_sporge') - (g if isinstance(g, float) else 99), 3)
        # tasca del rialzo: la bussola alzata fino a toccare il rialzo (se non tocca prima il mozzo) non deve servire:
        # il rialzo da solo dista dal fondo della tasca
        rialzo = _tmp_cil_y(m_f, xc, yi, yi + _mm(des, 'cus_rialzo_h'), _mm(des, 'cus_rialzo_d'))
        r['gioco_tasca_rialzo_mm'] = _gioco(lambda gg: _corpi_spostati(rialzo, _scala(vy, gg / 10)), bus(), hi=1.0)
        out[giunto] = r
    return out


def _mondo(m_att, m_zampa):
    m = m_att.copy()
    m.transformBy(m_zampa)
    return m


def _dir_mondo(m, x, y, z):
    v = V3(x, y, z)
    v.transformBy(m)
    v.normalize()
    return v


def _scala(v, k):
    """Vettore v (unitario) per k cm."""
    return V3(v.x * k, v.y * k, v.z * k)


def _tmp_cil_y(m_zampa, xc, y0, y1, d):
    """Cilindro temporaneo lungo Y della zampa (mm) portato nel mondo."""
    tbm = adsk.fusion.TemporaryBRepManager.get()
    c = tbm.createCylinderOrCone(P3(xc / 10, y0 / 10, 0), d / 20, P3(xc / 10, y1 / 10, 0), d / 20)
    tbm.transform(c, m_zampa)
    return [('rialzo', c)]


def verifica_estrattore(des, root, zampa):
    """Estrattore sulla culla della coxa (cuscinetto del femore) e della tibia (cuscinetto del ginocchio), e sul perno
    del femore B. Attesi: asta e tubo senza intersezioni; l'asta tocca l'anello interno (0,05 piu' avanti interseca,
    area di contatto = corona fra cus_d e att_estr_d); gioco della spalla nel foro cus_passo_d >= 0,2; tubo che tocca il
    mozzo della culla e lontano dalla flangia; a fine corsa (gambo sul fondo della culla) il cuscinetto e' tutto fuori,
    dentro il tubo. Per il perno: punta sul perno, a fine corsa (spalla sul rialzo) il perno e' fuori dal mozzo, nel tubo."""
    po = _parti_zampa(des, root, zampa)
    out = {}
    yfe, sede = _mm(des, 'zy_fondo_est'), _mm(des, 'cus_sede_prof')
    yb = yfe + sede                                       # faccia del cuscinetto verso la sede del servo
    pl, sl = _mm(des, 'att_estr_pilota_l'), _mm(des, 'att_estr_spalla_l')
    corsa = (yb + sl) - _mm(des, 'zy_fondo_int')         # il gambo si ferma sul fondo interno della culla
    corona = math.pi / 4 * (_mm(des, 'att_estr_d') ** 2 - _mm(des, 'cus_d') ** 2)
    for nome, parte, cus, xc in (('coxa', 'Coxa', 'Cuscinetto_Femore', _mm(des, 'zam_Lc')),
                                 ('tibia', 'Tibia', 'Cuscinetto_Ginocchio', _mm(des, 'zam_Lc + zam_Lf'))):
        m_p = _terna(po[parte])
        culla = [(parte, b) for b in po[parte].bRepBodies]
        cu = [(cus, b) for b in po[cus].bRepBodies]
        ma = _assi(xc, yb - pl, 1)                        # asta: z verso +Y, la spalla sulla faccia del cuscinetto
        mt = _assi(xc, yfe, -1)                           # tubo: z verso -Y, appoggiato sulla faccia esterna del fondo
        def asta(dz=0.0, dx=0.0):
            return _corpi_attrezzo(root, 'Attrezzo_Estrattore_Asta', _mondo(_sposta(ma, dx=dx, dz=dz), m_p))
        def tubo(dz=0.0, dx=0.0):
            return _corpi_attrezzo(root, 'Attrezzo_Estrattore_Tubo', _mondo(_sposta(mt, dx=dx, dz=dz), m_p))
        vy = _dir_mondo(m_p, 0, 1, 0)
        c_avanti = _vol(asta(-0.05), cu)
        r = {'asta_culla_mm3': _vol(asta(), culla), 'asta_cuscinetto_mm3': _vol(asta(), cu),
             'controllo_asta_avanti_0.05_mm3': c_avanti,
             'area_contatto_mm2': round(c_avanti / 0.05, 2), 'corona_anello_interno_mm2': round(corona, 2),
             'gioco_spalla_foro_mm': _gioco(lambda g: asta(dx=g), culla, hi=1.5),
             'gioco_punta_cuscinetto_mm': _gioco(lambda g: asta(dx=g), cu, hi=1.5),
             'tubo_culla_mm3': _vol(tubo(), culla), 'tubo_cuscinetto_mm3': _vol(tubo(), cu),
             'controllo_tubo_su_0.05_mm3': _vol(tubo(-0.05), culla),
             'gioco_tubo_flangia_mm': _gioco(lambda g: tubo(dx=g), cu, hi=1.5),
             'corsa_mm': round(corsa, 3)}
        fuori = _corpi_spostati(cu, _scala(vy, -corsa / 10))
        r['fine_corsa'] = {'asta_culla_mm3': _vol(asta(-corsa), culla),
                           'controllo_asta_oltre_0.05_mm3': _vol(asta(-corsa - 0.05), culla),
                           'cuscinetto_culla_mm3': _vol(fuori, culla), 'cuscinetto_tubo_mm3': _vol(fuori, tubo()),
                           'asta_tubo_mm3': _vol(asta(-corsa), tubo())}
        out[nome] = r
    # perno del femore B spinto fuori dal lato del rialzo verso il tubo appoggiato alla faccia esterna
    fb = po['Femore_B']
    m_f = _terna(fb)
    fem = [('Femore_B', b) for b in fb.bRepBodies]
    ype = _mm(des, 'zy_B_est - perno_sporge + perno_l')   # punta lunga del perno
    corsa_p = (ype + pl) - _mm(des, 'zy_B_int + cus_rialzo_h')   # la spalla si ferma sul rialzo
    vy = _dir_mondo(m_f, 0, 1, 0)
    for giunto, xc, perno in (('perno_anca', _mm(des, 'zam_Lc'), 'Perno_Femore'),):
        pe = [(perno, b) for b in po[perno].bRepBodies]
        ma = _assi(xc, ype, 1)
        mt = _assi(xc, _mm(des, 'zy_B_est'), -1)
        def asta(dz=0.0):
            return _corpi_attrezzo(root, 'Attrezzo_Estrattore_Asta', _mondo(_sposta(ma, dz=dz), m_f))
        def tubo(dz=0.0):
            return _corpi_attrezzo(root, 'Attrezzo_Estrattore_Tubo', _mondo(_sposta(mt, dz=dz), m_f))
        fuori = _corpi_spostati(pe, _scala(vy, -corsa_p / 10))
        out[giunto] = {'asta_perno_mm3': _vol(asta(), pe), 'controllo_asta_avanti_0.05_mm3': _vol(asta(-0.05), pe),
                       'tubo_femore_mm3': _vol(tubo(), fem), 'controllo_tubo_su_0.05_mm3': _vol(tubo(-0.05), fem),
                       'corsa_mm': round(corsa_p, 3),
                       'fine_corsa': {'asta_femore_mm3': _vol(asta(-corsa_p), fem),
                                      'controllo_asta_oltre_0.05_mm3': _vol(asta(-corsa_p - 0.05), fem),
                                      'perno_femore_mm3': _vol(fuori, fem), 'perno_tubo_mm3': _vol(fuori, tubo()),
                                      # perno e foro hanno lo stesso diametro: il gioco si calcola, non si misura
                                      'perno_oltre_la_faccia_mm': round(_mm(des, 'zy_B_est') - (ype - corsa_p), 3)}}
    return out


def main(passi, **kw):
    out = {'passi': passi}
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        V['controlla'](app)
        root = des.rootComponent
        if 'parametri' in passi:
            out['parametri'] = L['aggiungi_parametri'](des, PARAMETRI)
        if 'dime' in passi:
            # solo=[...] rifa' solo quelle dime: rifarne una cancella e ricrea il componente (D-066)
            for nome in kw.get('solo', list(POSE)):
                t0 = des.timeline.count
                occ, p = fai_dima(des, root, nome)
                occ.isLightBulbOn = False
                out[nome] = _chiudi(des, t0, nome, p)
        if 'cavalletto' in passi:
            t0 = des.timeline.count
            occ, p = fai_cavalletto(des, root)
            occ.isLightBulbOn = False
            out['cavalletto'] = _chiudi(des, t0, 'Attrezzo_Cavalletto', p)
        if 'provino_luce' in passi:
            t0 = des.timeline.count
            nero, pn, bianco, pb = fai_provino_luce(des, root)
            nero.isLightBulbOn = bianco.isLightBulbOn = False
            out['provino_luce'] = {'nero': dict(pn.info), 'bianco': dict(pb.info)}
            L['raggruppa'](des, t0, 'Attrezzo_Provino_Luce')
        if 'provino_tasche' in passi:
            t0 = des.timeline.count
            base, pb, lama, pl = fai_provino_tasche(des, root)
            base.isLightBulbOn = lama.isLightBulbOn = False
            out['provino_tasche'] = {'base': dict(pb.info), 'lama': dict(pl.info)}
            L['raggruppa'](des, t0, 'Attrezzo_Provino_Tasche')
        if 'provino_inserti' in passi:
            t0 = des.timeline.count
            occ, p = fai_provino_inserti(des, root)
            occ.isLightBulbOn = False
            out['provino_inserti'] = _chiudi(des, t0, 'Attrezzo_Provino_Inserti', p)
        if 'bussola' in passi:
            t0 = des.timeline.count
            occ, p = fai_bussola_perno(des, root)
            occ.isLightBulbOn = False
            out['bussola'] = _chiudi(des, t0, 'Attrezzo_Bussola_Perno', p)
        if 'estrattore' in passi:
            t0 = des.timeline.count
            asta, pa, tubo, pt = fai_estrattore(des, root)
            asta.isLightBulbOn = tubo.isLightBulbOn = False
            out['estrattore'] = {'asta': dict({'lavorazioni': pa.n, 'schizzi_non_vincolati': pa.non_vincolati}, **pa.info),
                                 'tubo': dict({'lavorazioni': pt.n, 'schizzi_non_vincolati': pt.non_vincolati}, **pt.info)}
            L['raggruppa'](des, t0, 'Attrezzo_Estrattore')
        if 'verifica_dime' in passi:
            out['verifica_dime'] = verifica_dime(des, root, kw.get('zampa', 'AS'), kw.get('solo'))
        if 'verifica_bussola' in passi:
            out['verifica_bussola'] = verifica_bussola(des, root, kw.get('zampa', 'AS'))
        if 'verifica_estrattore' in passi:
            out['verifica_estrattore'] = verifica_estrattore(des, root, kw.get('zampa', 'AS'))
        if 'verifica_cavalletto' in passi:
            out['verifica_cavalletto'] = verifica_cavalletto(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out
