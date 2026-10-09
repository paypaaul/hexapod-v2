"""Varianti della tibia: profilo dello stinco, finestre e piedino (terna della zampa, mm).

Lo stinco libero va dal fondo dello zoccolo (z -38,35) alla punta del piede (z -110, con il piedino). Ogni variante e':
- 'sx', 'dx': semilarghezza verso -X (lato corpo a gamma 90: e' il lato che tocca la coxa al gamma minimo) e verso +X;
- 'ym': Y della faccia -Y (la faccia +Y resta sul piano dell'orlo, Y 9,45, che in stampa sta sul piatto);
- 'r', 'zc': raggio e centro dell'arco della punta esterna (sagoma vista, piedino compreso): zc - r = -110;
- 'finestre': fessure passanti lungo Y (z alto, z basso, semilarghezza, estremi tondi);
- 'piedino': cappuccio in TPU, z dell'orlo, parete e suola.
Le funzioni valgono da z0 a zc; a zc le due semilarghezze valgono r (la punta e' un mezzo cerchio).
"""
import math

Z0 = -38.35          # fondo dello zoccolo (bug_coda)
ZP = -110.0          # punta del piede (zam_Lt)
Y_ORLO = 9.45


def retta(a, b, z0, z1):
    """Da a (a z0) a b (a z1), lineare; costante fuori dall'intervallo."""
    def f(z):
        t = min(max((z0 - z) / (z0 - z1), 0.0), 1.0)
        return a + (b - a) * t
    return f


def arco_convesso(w0, w1, z0, z1):
    """Arco di cerchio per (z0, w0) tangente alla verticale e per (z1, w1): fianco bombato (lama)."""
    d, h = w0 - w1, abs(z1 - z0)
    R = (d * d + h * h) / (2 * d)
    def f(z):
        dz = min(abs(z - z0), h)
        return w0 - R + math.sqrt(max(R * R - dz * dz, 0.0))
    f.R = R
    return f


def raccordo_concavo(q, z0, retta_w, R):
    """Arco concavo di raggio R che parte dallo spigolo dello zoccolo (w = q a z0) e finisce tangente alla retta
    w = retta_w(z) dello stinco; sotto la tangenza segue la retta. Ritorna f con f.centro, f.zt, f.angolo (inclinazione
    dell'arco allo spigolo, dalla verticale)."""
    # retta per due punti
    za, zb = z0, z0 - 60.0
    wa, wb = retta_w(za), retta_w(zb)
    # versore della retta e normale verso l'esterno (w crescente)
    t = (wb - wa, zb - za)
    L = math.hypot(*t)
    t = (t[0] / L, t[1] / L)
    n = (t[1], -t[0]) if t[1] < 0 else (-t[1], t[0])
    if n[0] < 0:
        n = (-n[0], -n[1])
    # centro C = P + R n con P sulla retta; |C - Q| = R, Q = (q, z0): si risolve per il parametro s lungo la retta
    best = None
    for k in range(200001):
        s = k * 0.0005
        P = (wa + t[0] * s, za + t[1] * s)
        C = (P[0] + R * n[0], P[1] + R * n[1])
        e = math.hypot(C[0] - q, C[1] - z0) - R
        if best is None or abs(e) < abs(best[0]):
            best = (e, s, C, P)
    e, s, C, P = best
    zt = P[1]
    def f(z):
        if z <= zt:
            return retta_w(z)
        dz = z - C[1]
        return C[0] - math.sqrt(max(R * R - dz * dz, 0.0))
    f.centro, f.zt, f.R = C, zt, R
    f.angolo = math.degrees(math.atan2(abs(C[1] - z0), abs(C[0] - q)))      # tangente allo spigolo dalla verticale
    return f


VARIANTI = {}

# ---------------------------------------------------------------- 0. base: lo stinco di oggi (zampa.py, fai_tibia)
VARIANTI['base'] = dict(
    titolo='Tibia di base (oggi)', breve='base',
    sx=lambda z: 6.0, dx=lambda z: 6.0, ym=lambda z: -9.45,
    r=6.0, zc=-104.0,
    finestre=[(min(-38.0 - 21 * i, Z0 - 0.4), -53.0 - 21 * i, 3.0, False) for i in range(3)],     # la prima entra 0,35 nello zoccolo: qui parte 0,4 sotto
    piedino=dict(z=-95.5, parete=0.0, suola=0.0),      # come nella sintesi: punta in arancio sotto l'ultima finestra, cappuccio non disegnato
)

# ---------------------------------------------------------------- 1. rastremata dritta, lieve
# 14 x 18,9 sotto lo zoccolo -> 9 x 13 alla punta. Il lato -X (quello che tocca la coxa al gamma minimo) si stringe
# appena (6 -> 4,5), il lato +X di piu' (8 -> 4,5).
VARIANTI['v1'] = dict(
    titolo='V1 - rastremata dritta', breve='v1',
    sx=retta(6.0, 4.5, Z0, -105.5), dx=retta(8.0, 4.5, Z0, -105.5), ym=retta(-9.45, -3.55, Z0, ZP),
    r=4.5, zc=-105.5,
    finestre=[(-43.0, -58.0, 3.6, True), (-63.0, -76.0, 3.0, True), (-81.0, -91.0, 2.4, True)],
    piedino=dict(z=-94.0, parete=1.2, suola=2.0),
)

# ---------------------------------------------------------------- 2. lama: fianco +X ad arco (trave di uguale resistenza)
VARIANTI['v2'] = dict(
    titolo='V2 - lama ad arco', breve='v2',
    sx=retta(6.0, 4.0, Z0, -106.0), dx=arco_convesso(10.0, 4.0, Z0, -106.0), ym=retta(-9.45, -2.55, Z0, ZP),
    r=4.0, zc=-106.0,
    finestre=[(-44.0, -62.0, 3.6, True), (-67.0, -83.0, 2.8, True)],
    piedino=dict(z=-94.0, parete=1.2, suola=2.0),
)

# ---------------------------------------------------------------- 3. sagoma unica: lo zoccolo scende nello stinco con
# raccordi concavi sul lato +X (sotto la ginocchiera) e sul lato -Y (sotto il fondo della culla); il lato -X resta
# dritto con lo spigolo vivo (li' tocca la coxa al gamma minimo)
_dx3 = retta(7.0, 4.5, Z0, -105.5)
_y3 = retta(9.45, 3.55, Z0, ZP)          # semilarghezza "verso -Y" come numero positivo
VARIANTI['v3'] = dict(
    titolo='V3 - sagoma unica', breve='v3',
    sx=retta(6.0, 4.5, Z0, -105.5),
    dx=raccordo_concavo(12.45, Z0, _dx3, 40.0),
    ym=None,                              # impostata sotto
    r=4.5, zc=-105.5,
    finestre=[(-58.0, -73.0, 3.0, True), (-78.0, -90.0, 2.5, True)],
    piedino=dict(z=-94.0, parete=1.2, suola=2.0),
)
_ry3 = raccordo_concavo(24.15, Z0, _y3, 70.0)
VARIANTI['v3']['ym'] = lambda z: -_ry3(z)
VARIANTI['v3']['_raccordi'] = (VARIANTI['v3']['dx'], _ry3)
