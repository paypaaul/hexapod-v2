#!/usr/bin/env python3
"""Sintesi "Kabuto corretto": render schematici della versione finale sul modello attuale (render.py).

Base Kabuto (carapace bianco a sei lobi esagonali, smusso 6 x 45, fascia nera) con le correzioni dei giudici:
- testa: viso nero (visiera) tra le corna, con i fianchi rastremati a 60 gradi fino al mento, occhio nella visiera;
- valli del carapace a y 56 (nascondono le slitte dei regolatori), coda a x -97,15 (non degenere), gonne nere;
- coda: guance bianche ai lati della porta di servizio, fascia nera che scende sulla coda, sportello bianco;
- femore: lame lunghe da mozzo a mozzo con finestre esagonali; lato A sospeso a filo delle teste, lato B appoggiato;
- tibia: ginocchiera a scudo solo sulla culla del ginocchio (niente piega sullo stinco);
- piedini arancio, unico accento.
Quote nella specifica (StructuredOutput); terna del robot e della zampa come in render.py, mm.
"""
import importlib.util
import math
import os
import sys

import numpy as np

sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica')
from render import Scena, COXE  # noqa: E402

_spec = importlib.util.spec_from_file_location('kabuto', '/Users/paul/.claude/jobs/3d86073b/tmp/estetica/sfaccettato/concept.py')
K = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(K)

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(QUI, 'sintesi')
TITOLO = 'Sintesi — Kabuto corretto'

BIANCO = '#eef0f2'
ANTRACITE = '#393c41'
SERVO = '#1c1d20'
NERO = '#141517'
FUGA = '#050505'
OMBRA = '#0e0f11'
INOX = '#b3b8be'
INOX_CHIARO = '#d3d7db'
VETRO = '#1b2638'
CICALINO = '#2a2d31'
DISPLAY = '#1e3a46'
ARANCIO = '#f04e14'

faccia, pareti, lastra, quad, aggiungi = K.faccia, K.pareti, K.lastra, K.quad, K.aggiungi
cerchio, rett, rientra, taglia, ccw, area = K.cerchio, K.rett, K.rientra, K.taglia, K.ccw, K.area
a3d = K.a3d

# ---------------------------------------------------------------- quote del corpo
Z_BORDO, Z_SMUSSO, Z_TOP, SP = 28.4, 30.0, 36.0, 1.6
CH = Z_TOP - Z_SMUSSO                      # smusso unico 6 x 45
R = 32.3
VISO_X = 102.0
CODA_X = 80 + R / 2 + 1.0                  # 97,15
VALLE_Y = 56.0
FASCIA = 17.0                              # semilarghezza della fascia nera
MENTO_Z, MENTO_SEMI = -1.0, 9.2            # mento della testa
TESTA_SEMI = 25.2                          # fianchi della testa sotto il carapace (1 mm dentro lo spigolo del viso)
TESTA_X0 = 82.6                            # retro della parte bassa della testa (vassoio fino a x 82)
T60 = math.tan(math.radians(60))
Z_RASTR = MENTO_Z + (TESTA_SEMI - MENTO_SEMI) * T60      # dove finisce la rastremazione (26,7)


def esagono(c):
    return [(c[0] + R * math.cos(math.radians(60 * k)), c[1] + R * math.sin(math.radians(60 * k))) for k in range(6)]


def x_lato(p, q, y):
    return p[0] + (y - p[1]) * (q[0] - p[0]) / (q[1] - p[1])


def y_lato(p, q, x):
    return p[1] + (x - p[0]) * (q[1] - p[1]) / (q[0] - p[0])


AS, MS, PS = esagono((80, 44)), esagono((0, 48)), esagono((-80, 44))
Y_VISO = y_lato(AS[5], AS[0], VISO_X)       # 26,16
Y_CODA = y_lato(PS[3], PS[4], -CODA_X)      # 17,76


def contorno():
    L = [(VISO_X, Y_VISO), AS[0], AS[1], AS[2], (x_lato(AS[2], AS[3], VALLE_Y), VALLE_Y),
         (x_lato(MS[0], MS[1], VALLE_Y), VALLE_Y), MS[1], MS[2], (x_lato(MS[2], MS[3], VALLE_Y), VALLE_Y),
         (x_lato(PS[0], PS[1], VALLE_Y), VALLE_Y), PS[1], PS[2], PS[3], (-CODA_X, Y_CODA)]
    return [(VISO_X, -Y_VISO)] + L + [(x, -y) for x, y in reversed(L[1:])]


def larghezza_testa(z):
    """Semilarghezza della parte bassa della testa alla quota z."""
    if z >= Z_RASTR:
        return TESTA_SEMI
    return MENTO_SEMI + (z - MENTO_Z) / T60


def sagoma_viso():
    """Visiera nera a x = VISO_X nel piano (y, z): dal mento al bordo del carapace (z 28,4), con la tacca dell'occhio."""
    return [(-TESTA_SEMI, Z_BORDO), (-TESTA_SEMI, Z_RASTR), (-MENTO_SEMI, MENTO_Z), (MENTO_SEMI, MENTO_Z),
            (TESTA_SEMI, Z_RASTR), (TESTA_SEMI, Z_BORDO), (9.15, Z_BORDO), (9.15, 22.5 - 7.94), (-9.15, 22.5 - 7.94),
            (-9.15, Z_BORDO)]


def fai_carapace(s):
    cont = contorno()
    n = len(cont)
    q = rientra(cont, CH)
    print('carapace: area %.0f mm2, ingombro x %.2f..%.2f, y +-%.2f; viso +-%.2f, coda +-%.2f'
          % (area(cont), min(p[0] for p in cont), max(p[0] for p in cont), max(p[1] for p in cont), Y_VISO, Y_CODA))
    # bordo verticale e smusso; sul viso e sulla coda la striscia |y| <= FASCIA e' nera
    for i in range(n):
        j = (i + 1) % n
        a, b, qa, qb = cont[i], cont[j], q[i], q[j]
        viso = abs(a[0] - VISO_X) < 1e-6 and abs(b[0] - VISO_X) < 1e-6
        coda = abs(a[0] + CODA_X) < 1e-6 and abs(b[0] + CODA_X) < 1e-6
        if viso:
            # bordo verticale del viso: fa parte della visiera (sotto); smusso: bianco ai lati, fascia nera al centro
            for y0, y1, col in ((a[1], -FASCIA, BIANCO), (-FASCIA, FASCIA, NERO), (FASCIA, b[1], BIANCO)):
                ya0 = qa[1] if y0 == a[1] else y0
                ya1 = qb[1] if y1 == b[1] else y1
                aggiungi(s, quad((VISO_X, y0, Z_SMUSSO), (VISO_X, y1, Z_SMUSSO), (qa[0], ya1, Z_TOP), (qa[0], ya0, Z_TOP)), col)
            continue
        if coda:
            for y0, y1, col in ((a[1], FASCIA, BIANCO), (FASCIA, -FASCIA, NERO), (-FASCIA, b[1], BIANCO)):
                ya0 = qa[1] if y0 == a[1] else y0
                ya1 = qb[1] if y1 == b[1] else y1
                aggiungi(s, quad((-CODA_X, y0, Z_BORDO), (-CODA_X, y1, Z_BORDO), (-CODA_X, y1, Z_SMUSSO), (-CODA_X, y0, Z_SMUSSO)), col)
                aggiungi(s, quad((-CODA_X, y0, Z_SMUSSO), (-CODA_X, y1, Z_SMUSSO), (qa[0], ya1, Z_TOP), (qa[0], ya0, Z_TOP)), col)
            continue
        aggiungi(s, quad((*a, Z_BORDO), (*b, Z_BORDO), (*b, Z_SMUSSO), (*a, Z_SMUSSO)), BIANCO)
        aggiungi(s, quad((*a, Z_SMUSSO), (*b, Z_SMUSSO), (*qb, Z_TOP), (*qa, Z_TOP)), BIANCO)
    # sotto della pelle (z 34,4) e del bordo, per non vedere attraverso il guscio
    aggiungi(s, faccia(rientra(cont, SP), [q], Z_TOP - SP), BIANCO)      # sotto dello smusso
    aggiungi(s, faccia(cont, [rientra(cont, SP)], Z_BORDO), BIANCO)

    # faccia piana: bianca fuori dalla fascia, con pozzetti e feritoie
    sx = taglia(q, (0, FASCIA), (1, FASCIA), sinistra=True)
    feritoie = [rett(18 + i * 7.295, 28.5, 24 + i * 7.295, 31.5) for i in range(5)]
    pozzi = [(40.0, 22.5), (-56.0, 22.5)]
    aggiungi(s, faccia(sx, [cerchio(c, 3.5, 28) for c in pozzi] + feritoie, Z_TOP), BIANCO, specchia_y=True)
    aggiungi(s, faccia(sx, [cerchio(c, 4.7, 28) for c in pozzi] + feritoie, Z_TOP - SP), BIANCO, specchia_y=True)
    for f in feritoie:
        aggiungi(s, pareti(f, Z_TOP - SP, Z_TOP), BIANCO, specchia_y=True)
        aggiungi(s, faccia(f, [], Z_TOP - SP), OMBRA, specchia_y=True)
    for c in pozzi:
        aggiungi(s, pareti(cerchio(c, 3.5, 28), 30.0, Z_TOP), BIANCO, specchia_y=True)
        aggiungi(s, faccia(cerchio(c, 3.5, 28), [cerchio(c, 2.75, 28)], 30.0), BIANCO, specchia_y=True)
        aggiungi(s, lastra(cerchio(c, 2.75, 28), [], 30.0, 33.4, sotto=False), INOX, specchia_y=True)
        aggiungi(s, faccia(cerchio(c, 1.3, 6), [], 33.41), OMBRA, specchia_y=True)

    # fascia nera: sportellino ottagonale a filo (|y| <= 16), pulsante, finestra del cicalino, tacca
    fascia = taglia(taglia(q, (0, FASCIA), (1, FASCIA), sinistra=False), (0, -FASCIA), (1, -FASCIA), sinistra=True)
    ott = [(-14, -16), (22, -16), (28, -10), (28, 10), (22, 16), (-14, 16), (-20, 10), (-20, -10)]
    puls, fin, tacca = cerchio((-40, 0), 6.1, 36), rett(-81.5, -12, -67.5, 12), rett(29, -5, 32, 5)
    dietro = taglia(fascia, (-20, 0), (-20, 1), sinistra=True)          # x <= -20
    dietro = taglia(dietro, (0, 0), (0, 1), sinistra=True)
    davanti = taglia(fascia, (28, 0), (28, 1), sinistra=False)          # x >= 28
    mezzo = taglia(taglia(fascia, (-20, 0), (-20, 1), sinistra=False), (28, 0), (28, 1), sinistra=True)
    aggiungi(s, faccia(dietro, [puls, fin], Z_TOP), NERO)
    aggiungi(s, faccia(davanti, [tacca], Z_TOP), NERO)
    aggiungi(s, faccia(mezzo, [ott], Z_TOP), NERO)
    for pz, bb in ((dietro, [puls, fin]), (davanti, []), (mezzo, [ott])):
        aggiungi(s, faccia(pz, bb, Z_TOP - SP), BIANCO)
    porta = rientra(ccw(ott), 0.4)
    aggiungi(s, faccia(porta, [], Z_TOP), NERO)
    aggiungi(s, pareti(porta, Z_TOP - 0.6, Z_TOP), NERO)
    aggiungi(s, faccia(ott, [porta], Z_TOP - 0.6), FUGA)
    aggiungi(s, pareti(tacca, Z_TOP - 0.8, Z_TOP), NERO)
    aggiungi(s, faccia(tacca, [], Z_TOP - 0.8), OMBRA)
    aggiungi(s, pareti(fin, Z_TOP - SP, Z_TOP), NERO)
    aggiungi(s, pareti(cerchio((-40, 0), 6.0, 36), 34.0, 36.6), INOX)
    aggiungi(s, faccia(cerchio((-40, 0), 6.0, 36), [cerchio((-40, 0), 4.2, 36)], 36.6), INOX)
    aggiungi(s, lastra(cerchio((-40, 0), 4.2, 36), [], 36.6, 36.9, sotto=False), INOX_CHIARO)

    # gonne: nere sotto il bordo (z 7..28,4), bianche sopra (nascoste dal bordo delle valli)
    for x0, x1 in ((22, 58.8), (-58.8, -22)):
        s.scatola(x0, 48.8, 7.0, x1, 50.0, Z_BORDO, NERO, specchia_y=True)
        s.scatola(x0, 48.8, Z_BORDO, x1, 50.0, Z_TOP - SP, BIANCO, specchia_y=True)


def fai_testa(s):
    """Parte bassa della testa (x 82,6..102) con i fianchi rastremati e la visiera nera (x 100,4..102)."""
    vis = sagoma_viso()
    occhio_e = rett(-9.15, 22.5 - 7.94, 9.15, 29.8)                   # bocca esterna a x 102 (lo smusso la intacca in cima)
    occhio_i = rett(-5.55, 22.5 - 5.24, 5.55, 22.5 + 5.24)            # bocca interna a x 99,4
    aggiungi(s, faccia(vis, [], VISO_X, 'x'), NERO)
    # fascia verticale del bordo sul viso (z 28,4..30): bianca ai lati, nera nella striscia della fascia, occhio aperto
    for y0, y1, z0, col in ((-Y_VISO, -FASCIA, Z_BORDO, BIANCO), (FASCIA, Y_VISO, Z_BORDO, BIANCO),
                            (-FASCIA, -9.15, Z_BORDO, NERO), (9.15, FASCIA, Z_BORDO, NERO), (-9.15, 9.15, 29.8, NERO)):
        aggiungi(s, faccia(rett(y0, z0, y1, Z_SMUSSO), [], VISO_X, 'x'), col)
    e3, i3 = a3d(occhio_e, VISO_X, 'x'), a3d(occhio_i, 99.4, 'x')
    aggiungi(s, np.concatenate([quad(e3[k], e3[(k + 1) % 4], i3[(k + 1) % 4], i3[k]) for k in range(4)]), NERO)
    aggiungi(s, faccia(rett(-6.2, 15.5, 6.2, 29.5), [], 98.0, 'x'), OMBRA)
    aggiungi(s, pareti(cerchio((0, 22.5), 3.5, 32), 98.5, 99.1, 'x'), '#26282c')
    aggiungi(s, faccia(cerchio((0, 22.5), 3.5, 32), [cerchio((0, 22.5), 2.4, 32)], 99.1, 'x'), '#26282c')
    aggiungi(s, faccia(cerchio((0, 22.5), 2.4, 32), [], 99.1, 'x'), VETRO)
    # fianchi della testa: lato rastremato e lato verticale, bianchi fino a x 100,4, poi lo spessore della visiera
    prof = [(MENTO_SEMI, MENTO_Z), (TESTA_SEMI, Z_RASTR), (TESTA_SEMI, Z_BORDO)]
    for sgn in (1, -1):
        for (y0, z0), (y1, z1) in zip(prof[:-1], prof[1:]):
            for xa, xb, col in ((TESTA_X0, VISO_X - SP, BIANCO), (VISO_X - SP, VISO_X, NERO)):
                aggiungi(s, quad((xa, sgn * y0, z0), (xb, sgn * y0, z0), (xb, sgn * y1, z1), (xa, sgn * y1, z1)), col)
        # gradino tra il fianco della testa e lo spigolo del viso, sotto il bordo
        aggiungi(s, quad((VISO_X - SP, sgn * TESTA_SEMI, Z_BORDO), (VISO_X, sgn * TESTA_SEMI, Z_BORDO),
                         (VISO_X, sgn * Y_VISO, Z_BORDO), (VISO_X - SP, sgn * Y_VISO, Z_BORDO)), BIANCO)
    # mento (bordo inferiore aperto: si vede lo spessore)
    aggiungi(s, quad((TESTA_X0, -MENTO_SEMI, MENTO_Z), (VISO_X, -MENTO_SEMI, MENTO_Z), (VISO_X, MENTO_SEMI, MENTO_Z),
                     (TESTA_X0, MENTO_SEMI, MENTO_Z)), BIANCO)
    # paratie dietro la testa (chiudono il fronte del corpo sopra l'orlo, |y| 15..28,5)
    s.scatola(81.0, 15.0, 7.0, TESTA_X0, 28.5, Z_TOP - SP, BIANCO, specchia_y=True)


def fai_coda(s):
    # guance bianche ai lati della porta di servizio
    s.scatola(-100.5, 25.4, -8.4, -87.6, 27.0, Z_TOP - SP, BIANCO, specchia_y=True)
    # cicalino a x -87..-62, appeso al collare del carapace; display sotto la finestra 14 x 24
    box = rett(-87, -20, -62, 20)
    disp = rett(-81.0, -11.5, -68.0, 11.5)
    aggiungi(s, pareti(box, 17.4, 28.4), CICALINO)
    aggiungi(s, faccia(box, [disp], 28.4), CICALINO)
    aggiungi(s, faccia(disp, [], 28.4), DISPLAY)
    aggiungi(s, faccia(box, [], 17.4), CICALINO)
    # sportello della batteria bianco
    b = s.gruppi['base']['tri']
    c = b.mean(1)
    m = (b[:, :, 0].max(1) <= -85.39) & (c[:, 0] < -85.45) & (np.abs(c[:, 1]) < 32) & (c[:, 2] < -9.3)
    aggiungi(s, K.estrai(s, 'base', m), BIANCO)
    t = s.gruppi['interni']['tri']
    m = t[:, :, 0].min(1) >= 98.45
    aggiungi(s, K.estrai(s, 'interni', m), NERO)


# ---------------------------------------------------------------- cover delle zampe (terna della zampa)
XH, XK = 55.0, 120.0
AP_E, AP_F = 14.0, 11.0                       # apotema della punta esagonale e della finestra
VE, VF = AP_E / math.cos(math.radians(30)), AP_F / math.cos(math.radians(30))
GOBBA = [(75.58, 14.0), (99.92, 14.0), (96.46, 20.0), (79.04, 20.0)]


def sagoma_lama():
    return [(XH - VE, 0), (XH - VE / 2, -AP_E), (XK + VE / 2, -AP_E), (XK + VE, 0), (XK + VE / 2, AP_E),
            GOBBA[1], GOBBA[2], GOBBA[3], GOBBA[0], (XH - VE / 2, AP_E)]


def finestra(xc):
    return [(xc + VF * math.cos(math.radians(60 * k)), VF * math.sin(math.radians(60 * k))) for k in range(6)]


def pezzi_coperti():
    """Pezzi convessi coperti dalla lama (sagoma meno finestre) per ritagliare le facce del femore."""
    out = []
    for xc in (XH, XK):
        fo = [(xc + VE * math.cos(math.radians(60 * k)), AP_E / math.sin(math.radians(60)) * math.sin(math.radians(60 * k)))
              for k in range(6)]
        fi = finestra(xc)
        for k in range(6):
            out.append([fi[k], fi[(k + 1) % 6], fo[(k + 1) % 6], fo[k]])
    out.append([(XH + VE, 0), (XK - VE, 0), (XK - VE / 2, AP_E), (XH + VE / 2, AP_E)])
    out.append([(XH + VE, 0), (XH + VE / 2, -AP_E), (XK - VE / 2, -AP_E), (XK - VE, 0)])
    out.append(GOBBA)
    return out


VITI_BLOCCO = [(81, 4.5), (81, 12.9), (94.5, 6.0), (94.5, 13.4)]
Y_A, Y_B = 30.55, -30.55
YA0, YA1 = 32.35, 33.55                        # lama A sospesa, faccia a filo delle teste M3
YB0, YB1 = -30.55, -31.75                      # lama B appoggiata
GIN = [(-24.15, 13.65), (9.45, 13.65), (9.45, -9.25), (-7.35, -38.35), (-24.15, -9.25)]


def fai_lame(s):
    kw = dict(zampe=True)
    sag, fin = sagoma_lama(), [finestra(XH), finestra(XK)]
    sedi = [cerchio(c, 2.8, 28, 0.07 * k) for k, c in enumerate(VITI_BLOCCO)]     # fasi diverse: la triangolazione non regge vertici allineati
    # lama A: lastra sospesa con quattro tubi sulle teste del blocco e due distanziali
    aggiungi(s, lastra(sag, fin + sedi, YA0, YA1, 'y'), BIANCO, **kw)
    for c in VITI_BLOCCO:
        aggiungi(s, pareti(cerchio(c, 3.8, 28), Y_A, YA0, 'y'), BIANCO, **kw)
    for c in ((XH + 15.2, 0.0), (XK - 15.2, 0.0)):
        aggiungi(s, pareti(cerchio(c, 1.5, 16), Y_A, YA0, 'y'), BIANCO, **kw)
    # lama B: lastra appoggiata, stessa sagoma e stesse finestre
    aggiungi(s, lastra(sag, fin, YB1, YB0, 'y'), BIANCO, **kw)
    # teste M3 sul lato A: 8 delle squadrette e 4 del blocco (a filo della lama)
    teste = [(xc + dx, dz) for xc in (XH, XK) for dx, dz in ((-7, 0), (7, 0), (0, 7), (0, -7))] + VITI_BLOCCO
    for c in teste:
        es = cerchio(c, 1.45, 6, math.pi / 6)
        aggiungi(s, faccia(cerchio(c, 2.75, 28), [es], Y_A + 3.0, 'y'), INOX, **kw)
        aggiungi(s, pareti(cerchio(c, 2.75, 28), Y_A, Y_A + 3.0, 'y'), INOX, **kw)
        aggiungi(s, pareti(es, Y_A + 1.8, Y_A + 3.0, 'y'), OMBRA, **kw)
        aggiungi(s, faccia(es, [], Y_A + 1.8, 'y'), OMBRA, **kw)
    m = K.maschera_zampe(s, 'zampe_servo', lambda TL: TL[:, :, 1].max(1) < -30.5)
    aggiungi(s, K.estrai(s, 'zampe_servo', m), INOX)
    m = K.maschera_zampe(s, 'zampe_struttura', lambda TL: TL[:, :, 2].max(1) <= -94.9)
    aggiungi(s, K.estrai(s, 'zampe_struttura', m), ARANCIO)


def fai_ginocchiera(s):
    kw = dict(zampe=True)
    aggiungi(s, lastra(GIN, [], 132.45, 133.65, 'x'), BIANCO, **kw)
    s.scatola(130.65, -24.15, 12.45, 133.65, 9.45, 13.65, BIANCO, **kw)


def main():
    s = Scena()
    s.nascondi('coperchio')
    s.colore('base', ANTRACITE)
    s.colore('zampe_struttura', ANTRACITE)
    s.colore('servo_coxa', SERVO)
    s.colore('interni', '#33363b')
    s.colore('zampe_servo', SERVO)
    tolti = K.togli_coperte(s, 'zampe_struttura', [
        (1, Y_A, pezzi_coperti()),
        (1, Y_B, pezzi_coperti()),
        (0, 132.45, [GIN]),
        (2, 12.45, [rett(130.65, -24.15, 133.65, 9.45)]),
    ])
    print('facce coperte: %d triangoli tolti, %d rimessi' % tolti)
    fai_carapace(s)
    fai_testa(s)
    fai_coda(s)
    fai_lame(s)
    fai_ginocchiera(s)
    viste = sys.argv[1:] or ['tutte']
    fatti = []
    if 'tutte' in viste or 'base' in viste:
        fatti += s.render(BASE, viste=('iso_ant', 'iso_post', 'fianco', 'alto'), titolo=TITOLO, lato=5.0)
    if 'tutte' in viste or 'zampa' in viste:
        fatti += s.render(BASE, viste=('zampa',), centro=(150, 85, -20), titolo=TITOLO, lato=5.0)
    if 'tutte' in viste or 'extra' in viste:
        fatti += s.render(BASE, viste=('fronte',), titolo=TITOLO, lato=5.0)
        fatti += s.render(BASE, viste=((16, 25, 3.2),), centro=(92, 0, 12), titolo=TITOLO, lato=5.0)
        fatti += s.render(BASE, viste=((16, 205, 3.0),), centro=(-90, 0, 5), titolo=TITOLO, lato=5.0)
    for f in fatti:
        print(f)


if __name__ == '__main__':
    main()
