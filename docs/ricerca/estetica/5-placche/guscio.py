"""Contorno del carapace di Kabuto corretto con i raccordi in pianta e profilo della spalla (sezione).

Pianta: raccordo `conv` sui vertici convessi (punte dei lobi, corna, spigoli di viso e coda), `conc` sui vertici
concavi (valli). Sezione dal bordo (z 28,4) alla faccia piana (z 36): bordo verticale fino a z 30, smusso 6 x 45,
raccordo `rim` fra smusso e bordo, raccordo `top` fra faccia piana e smusso.
"""
import math

import numpy as np

import geo

Z_BORDO, Z_SMUSSO, Z_TOP, CH = 28.4, 30.0, 36.0, 6.0
R = 32.3
VISO_X = 102.0
CODA_X = 80 + R / 2 + 1.0
VALLE_Y = 56.0
TESTA_SEMI = 25.2
T225 = math.tan(math.radians(22.5))


def _esagono(c):
    return [(c[0] + R * math.cos(math.radians(60 * k)), c[1] + R * math.sin(math.radians(60 * k))) for k in range(6)]


def _x_lato(p, q, y):
    return p[0] + (y - p[1]) * (q[0] - p[0]) / (q[1] - p[1])


def _y_lato(p, q, x):
    return p[1] + (x - p[0]) * (q[1] - p[1]) / (q[0] - p[0])


AS, MS, PS = _esagono((80, 44)), _esagono((0, 48)), _esagono((-80, 44))
Y_VISO = _y_lato(AS[5], AS[0], VISO_X)
Y_CODA = _y_lato(PS[3], PS[4], -CODA_X)


def contorno_vivo():
    L = [(VISO_X, Y_VISO), AS[0], AS[1], AS[2], (_x_lato(AS[2], AS[3], VALLE_Y), VALLE_Y),
         (_x_lato(MS[0], MS[1], VALLE_Y), VALLE_Y), MS[1], MS[2], (_x_lato(MS[2], MS[3], VALLE_Y), VALLE_Y),
         (_x_lato(PS[0], PS[1], VALLE_Y), VALLE_Y), PS[1], PS[2], PS[3], (-CODA_X, Y_CODA)]
    return geo.ccw([(VISO_X, -Y_VISO)] + L + [(x, -y) for x, y in reversed(L[1:])])


def raggi(car, P=None):
    P = P or contorno_vivo()
    n = len(P)
    out = []
    for i in range(n):
        a, b, c = np.array(P[i - 1]), np.array(P[i]), np.array(P[(i + 1) % n])
        cr = (b - a)[0] * (c - b)[1] - (b - a)[1] * (c - b)[0]
        out.append(car['conv'] if cr > 1e-9 else (car['conc'] if cr < -1e-9 else 0.0))
    return out


def contorno(car):
    P = contorno_vivo()
    if not (car['conv'] or car['conc']):
        return P
    return geo.raccorda(P, raggi(car, P), passo_ang=5.0)


def profilo(car):
    """Sezione della spalla: lista (rientro dal contorno, z) dal bordo basso alla faccia piana."""
    rr, rt = car['rim'], car['top']
    pts = [(0.0, Z_BORDO)]
    # raccordo fra bordo verticale e smusso (angolo di 45 gradi): tangenti a rr * tan(22,5)
    t = rr * T225
    if rr > 0:
        c = (rr, Z_SMUSSO - t)                           # centro, a rr dentro il bordo
        for k in range(7):
            f = math.radians(180 - 45 * k / 6)            # da 180 (sul bordo) a 135 (sullo smusso)
            pts.append((c[0] + rr * math.cos(f), c[1] + rr * math.sin(f)))
    else:
        pts.append((0.0, Z_SMUSSO))
    t2 = rt * T225
    if rt > 0:
        e = (CH - t2 / math.sqrt(2), Z_TOP - t2 / math.sqrt(2))
        c = (CH + t2, Z_TOP - rt)
        for k in range(7):
            f = math.radians(135 - 45 * k / 6)
            pts.append((c[0] + rt * math.cos(f), c[1] + rt * math.sin(f)))
    else:
        pts.append((CH, Z_TOP))
    return pts


def area_perimetro(p):
    return abs(geo.area(p)), geo.perimetro(p)


def controlli(car):
    P = contorno(car)
    print('  carapace: raccordi in pianta convessi R %.1f, concavi R %.1f; spalla: raccordo smusso-bordo R %.1f, faccia-smusso R %.1f'
          % (car['conv'], car['conc'], car['rim'], car['top']))
    if car['conv']:
        print('    raggio dei vertici convessi sulla faccia piana (R - 6): %.1f (deve restare > 0 perche lo smusso da 6 non si incroci)'
              % (car['conv'] - CH))
    if car['rim']:
        print('    raccordo smusso-bordo: tangente a %.2f mm sul bordo alto 1,6 e sullo smusso lungo 8,49' % (car['rim'] * T225))
    if car['top']:
        r = car['top']
        print('    raccordo faccia-smusso (stampa capovolta, primo strato da 0,2 sul PEI): sbalzo del primo strato %.2f mm, '
              'sbalzo oltre 45 gradi per %.2f mm di altezza' % (math.sqrt(2 * r * 0.2 - 0.04), r * (1 - math.cos(math.radians(45)))))
    # visiera: x del contorno alla quota y = TESTA_SEMI (gli spigoli della visiera stanno a x 102)
    Q = np.array(P)
    xs = []
    for i in range(len(Q)):
        a, b = Q[i], Q[(i + 1) % len(Q)]
        if (a[1] - TESTA_SEMI) * (b[1] - TESTA_SEMI) <= 0 and a[0] > 90 and b[0] > 90 and abs(b[1] - a[1]) > 1e-9:
            xs.append(a[0] + (TESTA_SEMI - a[1]) * (b[0] - a[0]) / (b[1] - a[1]))
    print('    bordo del viso a y %.1f: x %.2f (spigolo alto della visiera a x 102: sporge %.2f)' % (TESTA_SEMI, max(xs), 102 - max(xs)))
    ar, pe = area_perimetro(P)
    xs_ = Q[:, 0]
    print('    pianta: area %.0f mm2, perimetro %.0f, ingombro x %.2f..%.2f, y +-%.2f' % (ar, pe, xs_.min(), xs_.max(), Q[:, 1].max()))
