"""Concept estetico "Ciottolo" (angolo levigato): render schematici sul modello attuale dell'esapode.

Lanciare con:  python3 /Users/paul/.claude/jobs/3d86073b/tmp/estetica/levigato/concept.py [--dettagli]
Scrive levigato_*.png in questa cartella (iso_ant, iso_post, fianco, alto, zampa; con --dettagli anche fronte, muso
vista_14_28, coda vista_16_205, vita vista_22_110). Circa 5 minuti con --dettagli.

Quote dal concept (terna del robot: X avanti, Y a sinistra, Z in alto, z 0 sugli assi dei femori; terna della zampa: X verso
l'esterno, Y verso Femore_A, Z in alto). Parti nuove come mesh triangolate qui: lastre con fori (Delaunay filtrata),
guscio del dorso come pila di contorni sfalsati (raccordo R 7), frontale a cuscino (R 8 / R 4 / R 1).
"""
import math
import os
import sys

import numpy as np
from matplotlib.path import Path
from scipy.spatial import Delaunay, cKDTree

sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica')
import render  # noqa: E402
from render import Scena  # noqa: E402

# Solo in questo processo: bordi dei triangoli piu' spessi (0,15 -> 0,6). Con 0,15 le fughe d'antialiasing tra i triangoli
# lasciano vedere gli interni neri attraverso le parti bianche (reticolo grigio sul dorso e sul frontale nel primo giro).
_P3D = render.Poly3DCollection


def _p3d(*a, **k):
    k['linewidths'] = 0.6
    return _P3D(*a, **k)


render.Poly3DCollection = _p3d
LATO = 5.0      # suddivisione piu' fine (default 8): meno errori d'ordinamento tra lastre sottili e parti dietro

QUI = os.path.dirname(os.path.abspath(__file__))
BASE_PNG = os.path.join(QUI, 'levigato')

BIANCO = '#ebebe7'      # PETG bianco opaco
NERO = '#37393d'        # PETG-CF nero (schiarito quanto basta per leggere le forme)
SERVO = '#1f2023'       # casse dei servo
IRIDE = '#111111'
ARANCIO = '#ff6a13'     # piedini in TPU
INOX = '#c6cacf'        # teste delle viti
METALLO = '#b3b7bc'     # pulsante
OMBRA = '#6d6e70'       # fondo delle fessure da 0,3-0,5 mm (ombra)


# ----------------------------------------------------------------------------------------- geometria 2D
def arco(c, r, a0, a1, n):
    a = np.radians(np.linspace(a0, a1, n))
    return np.c_[c[0] + r * np.cos(a), c[1] + r * np.sin(a)]


def cerchio(c, r, n=48):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.c_[c[0] + r * np.cos(a), c[1] + r * np.sin(a)]


def rett(u0, v0, u1, v1):
    return np.array([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], dtype=float)


def rett_r(u0, v0, u1, v1, r, n=8):
    if r <= 0:
        return rett(u0, v0, u1, v1)
    return np.vstack([arco((u1 - r, v0 + r), r, -90, 0, n), arco((u1 - r, v1 - r), r, 0, 90, n),
                      arco((u0 + r, v1 - r), r, 90, 180, n), arco((u0 + r, v0 + r), r, 180, 270, n)])


def stadio(u0, v0, u1, v1, n=16):
    return rett_r(u0, v0, u1, v1, min(u1 - u0, v1 - v0) / 2, n)


def pulisci(p):
    p = np.asarray(p, dtype=float)
    keep = np.linalg.norm(p - np.roll(p, -1, axis=0), axis=1) > 1e-6
    return p[keep]


def densifica(p, passo):
    p = pulisci(p)
    out = []
    for i in range(len(p)):
        a, b = p[i], p[(i + 1) % len(p)]
        k = max(1, int(math.ceil(np.hypot(*(b - a)) / passo)))
        for j in range(k):
            out.append(a + (b - a) * j / k)
    return np.array(out)


def triangola(est, buchi=(), passo=2.0, griglia=4.0):
    """Triangoli 2D di un poligono (anche concavo) con fori: Delaunay di bordo + griglia, filtrata sui baricentri."""
    est = pulisci(est)
    buchi = [pulisci(b) for b in buchi]
    pe, pb = Path(est), [Path(b) for b in buchi]
    bordo = np.vstack([densifica(est, passo)] + [densifica(b, min(passo, 1.0)) for b in buchi])
    lo, hi = bordo.min(0), bordo.max(0)
    gx, gy = np.meshgrid(np.arange(lo[0] + griglia / 2, hi[0], griglia), np.arange(lo[1] + griglia / 2, hi[1], griglia))
    g = np.c_[gx.ravel(), gy.ravel()]
    ok = pe.contains_points(g)
    for p in pb:
        ok &= ~p.contains_points(g)
    g = g[ok]
    if len(g):
        d, _ = cKDTree(bordo).query(g)
        g = g[d > 0.45 * griglia]
    pts = np.vstack([bordo, g]) if len(g) else bordo
    tri = Delaunay(pts).simplices
    c = pts[tri].mean(1)
    ok = pe.contains_points(c)
    for p in pb:
        ok &= ~p.contains_points(c)
    return pts[tri[ok]]


def mappa(uv, a, asse):
    uv = np.asarray(uv, dtype=float)
    u, v = uv[..., 0], uv[..., 1]
    A = np.broadcast_to(np.asarray(a, dtype=float), u.shape)
    if asse == 'z':
        return np.stack([u, v, A], -1)
    if asse == 'x':
        return np.stack([A, u, v], -1)
    return np.stack([u, A, v], -1)


def pareti(anello, a0, a1, asse, passo=2.0):
    r = densifica(anello, passo)
    b = np.roll(r, -1, axis=0)
    q0, q1, q2, q3 = mappa(r, a0, asse), mappa(b, a0, asse), mappa(b, a1, asse), mappa(r, a1, asse)
    return np.concatenate([np.stack([q0, q1, q2], 1), np.stack([q0, q2, q3], 1)])


def faccia(est, buchi, a, asse, passo=2.0, griglia=4.0):
    return mappa(triangola(est, buchi, passo, griglia), a, asse)


def lastra(est, buchi, a0, a1, asse='z', passo=2.0, griglia=4.0):
    t2 = triangola(est, buchi, passo, griglia)
    parti = [mappa(t2, a0, asse), mappa(t2, a1, asse), pareti(est, a0, a1, asse, passo)]
    parti += [pareti(b, a0, a1, asse, min(passo, 1.0)) for b in buchi]
    return np.concatenate(parti)


def fascia(anello_a, anello_b, chiuso=True, salta=None):
    """Quadrilateri tra due anelli 3D con lo stesso numero di punti (salta(i) -> True per non farne uno)."""
    n = len(anello_a)
    tri = []
    for i in range(n if chiuso else n - 1):
        j = (i + 1) % n
        if salta is not None and salta(i):
            continue
        a, b, c, d = anello_a[i], anello_a[j], anello_b[j], anello_b[i]
        tri += [(a, b, c), (a, c, d)]
    return np.array(tri)


def aggiungi(s, tri, colore, **kw):
    tri = np.asarray(tri, dtype=float)
    s.mesh(tri.reshape(-1, 3), np.arange(len(tri) * 3).reshape(-1, 3), colore, **kw)


# ----------------------------------------------------------------------------------------- guscio (dorso)
R_CAL = 32.0
CA, CM, CP = np.array([80.0, 44.0]), np.array([0.0, 48.0]), np.array([-80.0, 44.0])
X_CODA, Y_NUC, X_CIGLIO = -95.0, 50.0, 101.2
R_VITA, R_CODA, R_BORDO = 8.0, 6.0, 7.0
Z_SU, Z_BORDO, SP = 36.0, 28.0, 1.6


def _ang(v):
    return math.degrees(math.atan2(v[1], v[0]))


def primitive_guscio():
    """Mezzo contorno sinistro in pianta, dal centro del sopracciglio al centro della coda (senso antiorario).
    ('L', p0, p1, normale esterna) | ('A', centro, raggio, a0, a1, convesso)."""
    F1 = np.array([X_CIGLIO + R_VITA, CA[1] - math.sqrt((R_CAL + R_VITA) ** 2 - (X_CIGLIO + R_VITA - CA[0]) ** 2)])
    F2 = np.array([CA[0] - math.sqrt((R_CAL + R_VITA) ** 2 - (Y_NUC + R_VITA - CA[1]) ** 2), Y_NUC + R_VITA])
    F3 = np.array([CM[0] + math.sqrt((R_CAL + R_VITA) ** 2 - (Y_NUC + R_VITA - CM[1]) ** 2), Y_NUC + R_VITA])
    F4, F5 = F3 * [-1, 1], F2 * [-1, 1]
    F6 = np.array([X_CODA - R_CODA, CP[1] - math.sqrt((R_CAL + R_CODA) ** 2 - (X_CODA - R_CODA - CP[0]) ** 2)])
    a = lambda c, p: _ang(p - c)  # noqa: E731
    return [
        ('L', (X_CIGLIO, 0.0), (X_CIGLIO, F1[1]), (1, 0)),
        ('A', F1, R_VITA, 180.0, a(F1, CA), False),
        ('A', CA, R_CAL, a(CA, F1), a(CA, F2), True),
        ('A', F2, R_VITA, a(F2, CA), -90.0, False),
        ('L', (F2[0], Y_NUC), (F3[0], Y_NUC), (0, 1)),
        ('A', F3, R_VITA, -90.0, a(F3, CM), False),
        ('A', CM, R_CAL, a(CM, F3), a(CM, F4), True),
        ('A', F4, R_VITA, a(F4, CM), -90.0, False),
        ('L', (F4[0], Y_NUC), (F5[0], Y_NUC), (0, 1)),
        ('A', F5, R_VITA, -90.0, a(F5, CP), False),
        ('A', CP, R_CAL, a(CP, F5), a(CP, F6) + 360.0, True),
        ('A', F6, R_CODA, a(F6, CP), 0.0, False),
        ('L', (X_CODA, F6[1]), (X_CODA, 0.0), (-1, 0)),
    ], (F1, F2, F3, F6)


PRIM, FILLETS = primitive_guscio()


def contorno(d, passo=1.5):
    """Contorno del guscio sfalsato verso l'interno di d (stesso numero di punti per ogni d)."""
    meta = []
    for pr in PRIM:
        if pr[0] == 'L':
            p0, p1, n = np.array(pr[1]), np.array(pr[2]), np.array(pr[3], dtype=float)
            k = max(2, int(math.ceil(np.hypot(*(p1 - p0)) / passo)))
            for j in range(k):
                meta.append(p0 + (p1 - p0) * j / k - d * n)
        else:
            _, c, r, a0, a1, convesso = pr
            k = max(3, int(math.ceil(r * math.radians(abs(a1 - a0)) / passo)))
            rr = r - d if convesso else r + d
            for j in range(k):
                t = math.radians(a0 + (a1 - a0) * j / k)
                meta.append(c + rr * np.array([math.cos(t), math.sin(t)]))
    meta.append(np.array([X_CODA + d, 0.0]))
    meta = np.array(meta)
    dx = meta[1:-1][::-1] * [1, -1]
    return np.vstack([meta, dx])


def quota_dorso(xy, cont0):
    """Z della superficie esterna del guscio sopra il punto (x, y) interno alla pianta."""
    seg_a, seg_b = cont0, np.roll(cont0, -1, axis=0)
    out = []
    for p in np.atleast_2d(xy):
        ab = seg_b - seg_a
        t = np.clip(((p - seg_a) * ab).sum(1) / np.maximum((ab * ab).sum(1), 1e-9), 0, 1)
        d = np.min(np.linalg.norm(seg_a + ab * t[:, None] - p, axis=1))
        out.append(Z_SU if d >= R_BORDO else Z_BORDO + 1 + math.sqrt(max(R_BORDO ** 2 - (R_BORDO - d) ** 2, 0)))
    return np.array(out)


def x_feritoia(i):
    # corpo.py: cor_reg_x0 + 4 + i * (reg_l - 8 - cor_fer_l) / 4, con le feritoie da x 18 (dossier) -> cor_reg_x0 = 14
    return 14.0 + 4.0 + i * (43.18 - 8.0 - 6.0) / 4


def guscio(s):
    cont0 = contorno(0.0)
    livelli = [(Z_BORDO, 0.0), (Z_BORDO + 1, 0.0)]
    for phi in np.linspace(0, 90, 12)[1:]:
        f = math.radians(phi)
        livelli.append((Z_BORDO + 1 + R_BORDO * math.sin(f), R_BORDO - R_BORDO * math.cos(f)))
    anelli = [np.c_[contorno(d), np.full(len(cont0), z)] for z, d in livelli]

    # aperture del dorso
    apertura = np.vstack([arco((-16, -13), 4, 180, 270, 8), arco((24, -13), 4, -90, 0, 8),
                          [(28, -5), (31, -5), (31, 5), (28, 5)],
                          arco((24, 13), 4, 0, 90, 8), arco((-16, 13), 4, 90, 180, 8)])   # sportellino + tacca
    feritoie = [rett(x_feritoia(i), sy * 28.5 if sy > 0 else -31.5, x_feritoia(i) + 6, 31.5 if sy > 0 else -28.5)
                for i in range(5) for sy in (1, -1)]
    pulsante = cerchio((-58, 0), 6.1, 40)
    display = stadio(-92.5, -5, -68.5, 5)
    viti = [(40, 22.5), (40, -22.5), (-56, 22.5), (-56, -22.5)]
    lamature = [cerchio(c, 3.1, 24) for c in viti]
    buchi = [apertura, pulsante, display] + feritoie + lamature

    # superficie esterna: bordo verticale z 28-29 e raccordo R 7; il display taglia il raccordo di coda
    p_disp = Path(display)
    tri = []
    for k in range(len(anelli) - 1):
        A, B = anelli[k], anelli[k + 1]
        cen = (A[:, :2] + np.roll(A[:, :2], -1, axis=0) + B[:, :2] + np.roll(B[:, :2], -1, axis=0)) / 4
        dentro = p_disp.contains_points(cen)
        tri.append(fascia(A, B, salta=lambda i, dd=dentro: dd[i]))
    tri.append(faccia(contorno(R_BORDO), buchi, Z_SU, 'z', passo=1.5, griglia=4.0))
    tri.append(faccia(contorno(R_BORDO), [apertura, pulsante, display] + feritoie, Z_SU - SP, 'z', passo=1.7, griglia=3.6))
    # orlo inferiore a z 28 (spessore 1,6)
    tri.append(fascia(np.c_[cont0, np.full(len(cont0), Z_BORDO)], np.c_[contorno(SP), np.full(len(cont0), Z_BORDO)]))
    # pareti delle aperture (spessore del dorso)
    for b in [apertura] + feritoie + [pulsante]:
        tri.append(pareti(b, Z_SU - SP, Z_SU, 'z', 1.0))
    for b in lamature:
        tri.append(pareti(b, Z_SU - 0.2, Z_SU, 'z', 1.0))
    r = densifica(display, 1.0)
    zt = quota_dorso(r, cont0)
    r1 = np.roll(r, -1, axis=0)
    zt1 = np.roll(zt, -1)
    q0, q1 = np.c_[r, zt - SP], np.c_[r1, zt1 - SP]
    q2, q3 = np.c_[r1, zt1], np.c_[r, zt]
    tri.append(np.concatenate([np.stack([q0, q1, q2], 1), np.stack([q0, q2, q3], 1)]))
    aggiungi(s, np.concatenate(tri), BIANCO)

    # tappi delle viti (0,2 sotto il piano), fondo della tacca, battuta dello sportellino (vista solo nella fessura)
    for c in viti:
        aggiungi(s, lastra(cerchio(c, 3.1, 24), [], Z_SU - 1.0, Z_SU - 0.2), BIANCO)
    aggiungi(s, lastra(rett(28, -5, 31, 5), [], Z_SU - 0.9, Z_SU - 0.8), BIANCO)
    aggiungi(s, lastra(rett_r(-20, -17, 28, 17, 4), [rett_r(-18, -15, 26, 15, 2)], 33.2, 34.4), OMBRA)

    # sportellino a filo (0,3 di fessura)
    aggiungi(s, lastra(rett_r(-19.7, -16.7, 27.7, 16.7, 3.7), [], 34.4, Z_SU), BIANCO)

    # gonne (y 48,4-50, x +-(22-58,8), da z 7 al sotto del dorso 34,4), come da concept
    for sx in (1, -1):
        x0, x1 = (22.0, 58.8) if sx > 0 else (-58.8, -22.0)
        s.scatola(x0, 48.4, 7.0, x1, 50.0, Z_SU - SP, BIANCO, specchia_y=True)
    # grembiule di coda con la porta di servizio (|y| <= 20, z -8...29, angoli alti R 6, aperta in basso)
    gremb = np.vstack([[(-24, -8), (-20, -8)], arco((-14, 23), 6, 180, 90, 8), arco((14, 23), 6, 90, 0, 8),
                       [(20, -8), (24, -8), (24, Z_SU - SP), (-24, Z_SU - SP)]])
    aggiungi(s, lastra(gremb, [], X_CODA, X_CODA + 1.6, asse='x', passo=1.5, griglia=3.0), BIANCO)
    # culla del cicalino: guide e labbri
    s.scatola(-93, 20.2, 21.2, -68, 21.4, Z_SU - SP, BIANCO, specchia_y=True)
    s.scatola(-93, 18.7, 21.2, -68, 20.2, 22.0, BIANCO, specchia_y=True)


# ----------------------------------------------------------------------------------------- frontale con l'occhio
def frontale(s):
    X0, X1, SEMI, ZG, ZS = 84.5, 100.2, 20.0, -9.4, 27.5
    RV, RB, RT = 8.0, 4.0, 1.0
    zb, zt = ZG + RB, ZS - RT          # inizio del raccordo basso e di quello alto

    def sezione(d):
        lato_s = np.linspace((X0, SEMI - d), (X1 - RV, SEMI - d), 4)
        arco_s = arco((X1 - RV, SEMI - RV), RV - d, 90, 0, 9)[1:]
        fronte = np.linspace((X1 - d, SEMI - RV), (X1 - d, -(SEMI - RV)), 9)[1:]
        arco_d = arco((X1 - RV, -(SEMI - RV)), RV - d, 0, -90, 9)[1:]
        lato_d = np.linspace((X1 - RV, -(SEMI - d)), (X0, -(SEMI - d)), 4)[1:]
        p = np.vstack([lato_s, arco_s, fronte, arco_d, lato_d])
        i0 = len(lato_s) + len(arco_s) - 1          # primo punto del fronte piano (y = +12)
        return p, i0, i0 + len(fronte)               # quad del fronte: i0 ... i0 + 8 - 1

    p0, i0, i1 = sezione(0)
    livelli = []
    for phi in np.linspace(0, 90, 7):
        f = math.radians(phi)
        livelli.append((zb - RB * math.cos(f), RB - RB * math.sin(f)))
    livelli.append((zt, 0.0))
    for phi in np.linspace(0, 90, 4)[1:]:
        f = math.radians(phi)
        livelli.append((zt + RT * math.sin(f), RT - RT * math.cos(f)))
    anelli = [np.c_[sezione(d)[0], np.full(len(p0), z)] for z, d in livelli]
    tri = []
    for k in range(len(anelli) - 1):
        piano = math.isclose(livelli[k][0], zb, abs_tol=1e-6) and math.isclose(livelli[k + 1][0], zt, abs_tol=1e-6)
        tri.append(fascia(anelli[k], anelli[k + 1], chiuso=False,
                          salta=(lambda i: i0 <= i < i1) if piano else None))
    tri.append(faccia(sezione(RB)[0], [], ZG, 'z'))
    tri.append(faccia(sezione(RT)[0], [], ZS, 'z'))
    # faccia piana con il foro dell'occhio (D 16, centro z 18)
    tri.append(faccia(rett(-(SEMI - RV), zb, SEMI - RV, zt), [cerchio((0, 18), 8.0, 48)], X1, 'x', passo=1.0, griglia=3.0))
    tri.append(faccia(rett(-(SEMI - RV), zb, SEMI - RV, zt), [cerchio((0, 18), 3.7, 32)], X1 - 1.6, 'x', passo=1.3, griglia=2.7))
    aggiungi(s, np.concatenate(tri), BIANCO)
    # iride nera: corona tra D 13 e D 16 sulla faccia, cono fino a D 7,4 a x 98,6
    aggiungi(s, lastra(cerchio((0, 18), 8.0, 48), [cerchio((0, 18), 6.5, 48)], X1 - 0.3, X1, asse='x', passo=1.0, griglia=2.0),
             IRIDE)
    a = np.linspace(0, 2 * np.pi, 48, endpoint=False)
    est = np.c_[np.full(48, X1), 6.5 * np.cos(a), 18 + 6.5 * np.sin(a)]
    inn = np.c_[np.full(48, 98.6), 3.7 * np.cos(a), 18 + 3.7 * np.sin(a)]
    aggiungi(s, fascia(est, inn), IRIDE)
    # lente della camera (D 7, faccia a x 98,5) sull'asse a z 18
    aggiungi(s, lastra(cerchio((0, 18), 3.5, 32), [], 98.4, 98.5, asse='x', passo=1.0, griglia=2.0), '#16202c')
    aggiungi(s, lastra(cerchio((-1.0, 19.2), 0.9, 16), [], 98.5, 98.52, asse='x', passo=0.5, griglia=1.0), '#5d6f84')


# ----------------------------------------------------------------------------------------- cover delle zampe (terna della zampa)
XA, XK = 55.0, 120.0


def sagoma_femore():
    """Sagoma del femore + 1,5 nel piano (X, Z): teste R 14,5, fascia +-14,5, gobba 75-100,5 fino a Z 21,5.
    Fianco della gobba alto 7: R 6 concavo e R 4 convesso non ci stanno con un tratto verticale, diventano una S."""
    rc, rv, zf, zg = 6.0, 4.0, 14.5, 21.5
    dx = math.sqrt((rc + rv) ** 2 - ((zf + rc) - (zg - rv)) ** 2)        # 9,54 tra i centri
    cl, vl = 75.0 - rc / (rc + rv) * dx, 75.0 + rv / (rc + rv) * dx       # sinistra: concavo, convesso
    vr, cr = 100.5 - rv / (rc + rv) * dx, 100.5 + rc / (rc + rv) * dx     # destra: convesso, concavo
    a_c = _ang(np.array([vr - cr, (zg - rv) - (zf + rc)]))                # da centro concavo destro a centro convesso
    b = a_c + 180.0                                                       # 17,5 gradi
    p = [np.array([(XA, -zf), (XK, -zf)]),
         arco((XK, 0), 14.5, -90, 90, 25)[1:],
         np.array([(cr, zf)]),
         arco((cr, zf + rc), rc, -90, a_c, 8)[1:],
         arco((vr, zg - rv), rv, b, 90, 8)[1:],
         arco((vl, zg - rv), rv, 90, 180 - b, 8),
         arco((cl, zf + rc), rc, -b, -90, 8)[1:],
         arco((XA, 0), 14.5, 90, 270, 25)]
    return np.vstack(p)


def cover_zampe(s):
    sag = sagoma_femore()
    finestre = [cerchio((XA, 0), 11, 40), cerchio((XK, 0), 11, 40), stadio(77.75, 1.2, 97.75, 16.2)]
    # Cover_Femore_A (Y 32,35-33,55) e Cover_Femore_B (Y -32,95 / -31,75)
    aggiungi(s, lastra(sag, finestre, 32.35, 33.55, asse='y', passo=1.2, griglia=3.0), BIANCO, zampe=True)
    aggiungi(s, lastra(sag, [], -32.95, -31.75, asse='y', passo=1.2, griglia=3.0), BIANCO, zampe=True)
    # teste M3 inox (D 5,5 x 3, da Y 30,55): 4 per squadretta (PCD 14) e 4 del blocco
    teste = [(xc + dx, dz) for xc in (XA, XK) for dx, dz in ((7, 0), (-7, 0), (0, 7), (0, -7))]
    teste += [(81, 4.5), (81, 12.9), (94.5, 7.5), (94.5, 12.9)]
    for c in teste:
        s.cilindro(c, 2.75, 30.55, 33.55, INOX, n=20, asse='y', zampe=True)
        s.cilindro(c, 1.3, 33.55, 33.6, '#55585c', n=6, asse='y', zampe=True)       # impronta esagonale
    # cuffie dei servo di femore e ginocchio (piastra Y 20,3-21,5, foro D 14, pareti da 1,0)
    for xc in (XA, XK):
        pl = np.vstack([[(xc - 12.15, -38.35), (xc + 12.15, -38.35)], arco((xc, 8), 12.15, 0, 180, 24)])
        aggiungi(s, lastra(pl, [cerchio((xc, 0), 7.0, 32)], 20.3, 21.5, asse='y', passo=1.2, griglia=3.0), BIANCO, zampe=True)
        for x0 in (xc + 11.15, xc - 12.15):
            s.scatola(x0, 9.8, -38.35, x0 + 1.0, 20.3, 8.0, BIANCO, zampe=True)
    # schiniere: lama X 133,0-134,2 e fianchi a U attorno allo stinco
    lama = np.vstack([arco((-24 + 6, 10 - 6), 6, 180, 90, 7), arco((21.5 - 6, 10 - 6), 6, 90, 0, 7),
                      [(21.5, -33), (10.95, -45)], arco((10.95 - 5.5, -98 + 5.5), 5.5, 0, -90, 7),
                      arco((-10.95 + 5.5, -98 + 5.5), 5.5, -90, -180, 7), [(-10.95, -45), (-24, -33)]])
    aggiungi(s, lastra(lama, [], 133.0, 134.2, asse='x', passo=1.5, griglia=3.0), BIANCO, zampe=True)
    for y0 in (9.75, -10.95):
        s.scatola(117, y0, -98, 134.2, y0 + 1.2, -45, BIANCO, zampe=True)
    # piedino in TPU arancio: cappuccio sulla punta tonda dello stinco (R 6 a Z -104), 1,5 di parete, alto fino a Z -100
    pieno = np.vstack([[(XK - 7.5, -100)], arco((XK, -104), 7.5, 180, 360, 24), [(XK + 7.5, -100)]])
    u = np.vstack([pieno, [(XK + 6, -100)], arco((XK, -104), 6, 0, -180, 20), [(XK - 6, -100)]])
    aggiungi(s, lastra(u, [], -9.45, 9.45, asse='y', passo=1.0, griglia=1.5), ARANCIO, zampe=True)
    for y0, y1 in ((9.45, 10.95), (-10.95, -9.45)):
        aggiungi(s, lastra(pieno, [], y0, y1, asse='y', passo=1.0, griglia=1.5), ARANCIO, zampe=True)


# ----------------------------------------------------------------------------------------- scena
def scena():
    s = Scena()
    s.nascondi('coperchio')
    for g, c in (('base', NERO), ('zampe_struttura', NERO), ('servo_coxa', SERVO), ('zampe_servo', SERVO)):
        s.colore(g, c)
    # interni: camera abbassata a z 18 (asse), T-plug, F1, il resto scuro
    t = s.gruppi['interni']['tri']
    c = t.mean(1)
    cam = (c[:, 0] > 92) & (np.abs(c[:, 1]) < 5) & (c[:, 2] > 17)
    tpl = (c[:, 0] > -81) & (c[:, 0] < -64) & (c[:, 2] > 5.5) & (c[:, 2] < 14.2) & (np.abs(c[:, 1]) <= 15.1)
    f1 = (c[:, 0] > -84) & (c[:, 0] < -61) & (c[:, 2] < 5.7) & (c[:, 2] > -9.5) & (np.abs(c[:, 1]) <= 20.1)
    tcam = t[cam].copy()
    tcam[:, :, 2] -= 4.5
    resto = ~(cam | tpl | f1)
    s.gruppi['interni']['tri'] = t[resto]
    s.colore('interni', '#33363b')
    s.gruppi['camera'] = {'tri': tcam, 'colore': '#24262a', 'visibile': True}
    s.gruppi['tplug'] = {'tri': t[tpl], 'colore': '#b3322a', 'visibile': True}
    s.gruppi['f1'] = {'tri': t[f1], 'colore': '#2b2c2f', 'visibile': True}
    # cicalino (40 x 25 x 11 stimato) con il display sotto la finestra del dorso
    s.scatola(-93, -20, 22, -68, 20, 33, '#2a2a2d')
    s.scatola(-91.5, -4.5, 33, -69.5, 4.5, 33.15, '#3c1515')
    # pulsante metallico D 12 a (-58; 0): flangia D 15 sporgente 2 mm
    s.cilindro((-58, 0), 7.5, Z_SU, Z_SU + 1.4, METALLO, n=40)
    s.cilindro((-58, 0), 4.5, Z_SU + 1.4, Z_SU + 2.0, '#d4d7db', n=32)
    guscio(s)
    frontale(s)
    cover_zampe(s)
    return s


if __name__ == '__main__':
    s = scena()
    print(s.render(BASE_PNG, viste=('iso_ant', 'iso_post', 'fianco', 'alto'), titolo='Ciottolo', lato=LATO))
    print(s.render(BASE_PNG, viste=('zampa',), centro=(150, 85, -20), titolo='Ciottolo', lato=LATO))
    if '--dettagli' in sys.argv:
        print(s.render(BASE_PNG, viste=('fronte', (14, 28, 3.2)), centro=(95, 0, 10), titolo='Ciottolo', lato=LATO))
        print(s.render(BASE_PNG, viste=((16, 205, 3.0),), centro=(-95, 0, 8), titolo='Ciottolo', lato=LATO))
        print(s.render(BASE_PNG, viste=((22, 110, 6.0),), centro=(40, 50, 26), titolo='Ciottolo', lato=LATO))
