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

Cavalletto: culla sotto la chiglia (lontana da sportello della batteria e viti), colonna cava e base; le zampe restano
libere su tutta l'escursione (piede piu' basso a z -159 con femore -49 e ginocchio 139, tavolo a z -170).

Uso dal connettore, un passo per chiamata:
    runpy.run_path('/Users/paul/hexapod-v2/cad/script/attrezzi.py')['main'](['parametri', 'dime'])
Passi: parametri, dime, cavalletto, verifica_dime (kw zampa='AS'), verifica_cavalletto.
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
Parte, NUOVO, UNISCI, TAGLIA = L['Parte'], L['NUOVO'], L['UNISCI'], L['TAGLIA']

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
]

# (imbardata, femore, ginocchio) in gradi delle due pose (software.md 2.7)
POSE = {'Dima_Posa_1': (0.0, 0.0, 90.0), 'Dima_Posa_2': (30.0, 45.0, 135.0)}
LIBRERIA = {'Dima_Posa_1': (0, 850, 0), 'Dima_Posa_2': (100, 850, 0), 'Attrezzo_Cavalletto': (260, 850, 0),
            'Attrezzo_Provino_Luce_Nero': (420, 850, 0), 'Attrezzo_Provino_Luce_Bianco': (420, 850, 0)}
# provino di luce (X10, D-069): profondita' delle camere sopra la striscia e spessori del bianco da provare
PROV_CAMERE = (2.0, 4.0, 6.0)
PROV_BIANCO = (0.4, 0.8, 1.2, 1.6)


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


def _chiudi(des, t0, nome, p):
    L['raggruppa'](des, t0, nome)
    return dict({'lavorazioni': p.n, 'schizzi_non_vincolati': p.non_vincolati}, **getattr(p, 'info', {}))


def _copia(root, nome, m):
    """Occorrenza provvisoria alla radice del componente di libreria `nome` nella matrice m (terna del robot)."""
    lib = [o for o in root.occurrences if o.component.name == nome][0]
    o = root.occurrences.addExistingComponent(lib.component, m)
    o.isLightBulbOn = True
    return o


def verifica_dime(des, root, zampa):
    """Ogni dima su una zampa atteggiata nella sua posa: interferenze con zampa e corpo (attese: nessuna) e distanza
    dei tre denti dalle loro facce (attesa: zero, contatto)."""
    AS = runpy.run_path(os.path.join(QUI, 'assieme.py'))
    out = {}
    zo = AS['mappa_zampe'](des, root)[zampa]
    corpo = AS['_corpo'](root)
    fb = [o for o in zo.component.occurrences if o.component.name == 'Femore_B'][0]
    copie = {n: _copia(root, n, adsk.core.Matrix3D.create()) for n in POSE}
    try:
        for nome, (yaw, alfa, gamma) in POSE.items():
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
            for nome in POSE:
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
        if 'verifica_dime' in passi:
            out['verifica_dime'] = verifica_dime(des, root, kw.get('zampa', 'AS'))
        if 'verifica_cavalletto' in passi:
            out['verifica_cavalletto'] = verifica_cavalletto(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out
