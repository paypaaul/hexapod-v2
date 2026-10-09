#!/usr/bin/env python3
"""Concept "Kabuto - armatura sfaccettata": render schematici sul modello attuale (render.py).

Carapace bianco a sei lobi esagonali (raggio 32,3 sugli assi delle coxe) con smusso 6 x 45 (4 x 45 sulla testa),
fascia dorsale nera intarsiata con sportellino ottagonale, pulsante e finestra del cicalino, testa stretta con
l'occhio a tronco di piramide; lame bianche sui due lati del femore (cuscinetto con le teste delle viti sul lato A,
scanalatura sul lato B) e schiniere bianco sulla faccia esterna della tibia. Quote dal concept, terna del robot in mm.

Le facce del modello attuale coperte da una cover (stesso piano) vengono ritagliate, cosi' l'ordinamento per
profondita' di matplotlib non le fa riaffiorare sopra le cover.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica')
from render import Scena, terna_zampa, COXE  # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(QUI, 'sfaccettato')
TITOLO = 'Kabuto — armatura sfaccettata'

BIANCO = '#eef0f2'      # PETG bianco opaco (cover)
ANTRACITE = '#393c41'   # PETG-CF (struttura)
SERVO = '#1c1d20'       # servo neri
NERO = '#141517'        # PETG nero non caricato (interfacce: fascia, sportellino, occhio)
FUGA = '#050505'
OMBRA = '#0e0f11'
INOX = '#b3b8be'
INOX_CHIARO = '#d3d7db'
VETRO = '#1b2638'
CICALINO = '#2a2d31'
DISPLAY = '#1e3a46'


# ---------------------------------------------------------------- geometria piana
def area(p):
    p = np.asarray(p, float)
    return 0.5 * float(np.sum(p[:, 0] * np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1) * p[:, 1]))


def ccw(p):
    p = [(float(a), float(b)) for a, b in p]
    return p if area(p) > 0 else p[::-1]


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def cerchio(c, r, n=32, fase=0.0):
    return [(c[0] + r * math.cos(fase + 2 * math.pi * k / n), c[1] + r * math.sin(fase + 2 * math.pi * k / n)) for k in range(n)]


def due_cerchi(c1, c2, r, n=28):
    """Contorno dell'unione di due cerchi uguali che si sovrappongono (centri sulla stessa verticale o no)."""
    c1, c2 = np.asarray(c1, float), np.asarray(c2, float)
    d = np.linalg.norm(c2 - c1)
    u = (c2 - c1) / d
    a = math.acos(min(d / 2 / r, 1.0))          # semiangolo dell'arco tagliato, visto dal centro
    base = math.atan2(u[1], u[0])
    out = []
    for c, verso in ((c1, base + math.pi), (c2, base)):
        for k in range(n + 1):
            t = verso - (math.pi - a) + 2 * (math.pi - a) * k / n
            out.append((c[0] + r * math.cos(t), c[1] + r * math.sin(t)))
    return pulisci(out, 1e-6)


def rett(u0, v0, u1, v1):
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


def pulisci(p, eps=1e-9):
    out = []
    for q in p:
        if not out or abs(q[0] - out[-1][0]) > eps or abs(q[1] - out[-1][1]) > eps:
            out.append(q)
    while len(out) > 1 and abs(out[0][0] - out[-1][0]) <= eps and abs(out[0][1] - out[-1][1]) <= eps:
        out.pop()
    return out


def taglia(poly, a, b, sinistra=True):
    """Sutherland-Hodgman su un semipiano: tiene la parte a sinistra (o a destra) della retta a -> b."""
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        fp, fq = cross(a, b, P), cross(a, b, Q)
        if not sinistra:
            fp, fq = -fp, -fq
        if fp >= 0:
            out.append(P)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return pulisci(out)


def meno_convesso(poligoni, C):
    """Poligoni convessi meno il poligono convesso C (antiorario): pezzi convessi."""
    out = []
    n = len(C)
    for P in poligoni:
        resto = P
        for k in range(n):
            a, b = C[k], C[(k + 1) % n]
            fuori = taglia(resto, a, b, sinistra=False)
            if len(fuori) >= 3 and abs(area(fuori)) > 1e-6:
                out.append(fuori)
            resto = taglia(resto, a, b, sinistra=True)
            if len(resto) < 3 or abs(area(resto)) < 1e-6:
                break
    return out


def rientra(poly, d):
    """Contorno antiorario spostato verso l'interno di d (uno per lato): vertici = incroci delle rette spostate."""
    P = np.asarray(poly, float)
    n = len(P)
    d = list(d) if hasattr(d, '__len__') else [d] * n
    linee = []
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        u = (b - a) / np.linalg.norm(b - a)
        linee.append((a + d[i] * np.array([-u[1], u[0]]), u))
    out = []
    for i in range(n):
        (p1, u1), (p2, u2) = linee[i - 1], linee[i]
        den = u1[0] * u2[1] - u1[1] * u2[0]
        if abs(den) < 1e-12:
            out.append(tuple(p2))
            continue
        w = p2 - p1
        t = (w[0] * u2[1] - w[1] * u2[0]) / den
        out.append(tuple(p1 + t * u1))
    return out


def incrocio(p1, p2, p3, p4):
    d = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
    t = ((p1[0] - p3[0]) * (p3[1] - p4[1]) - (p1[1] - p3[1]) * (p3[0] - p4[0])) / d
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def _attraversa(p1, p2, p3, p4, e=1e-9):
    d1, d2 = cross(p3, p4, p1), cross(p3, p4, p2)
    d3, d4 = cross(p1, p2, p3), cross(p1, p2, p4)
    return ((d1 > e and d2 < -e) or (d1 < -e and d2 > e)) and ((d3 > e and d4 < -e) or (d3 < -e and d4 > e))


def _sul_segmento(p, a, b, e=1e-7):
    if abs(cross(a, b, p)) > e * max(1.0, math.dist(a, b)):
        return False
    if math.dist(p, a) < 1e-7 or math.dist(p, b) < 1e-7:
        return False
    return min(a[0], b[0]) - e <= p[0] <= max(a[0], b[0]) + e and min(a[1], b[1]) - e <= p[1] <= max(a[1], b[1]) + e


def _dentro_tri(p, a, b, c, e=1e-9):
    return cross(a, b, p) >= -e and cross(b, c, p) >= -e and cross(c, a, p) >= -e


def _orecchie(pts):
    idx = list(range(len(pts)))
    tris = []
    while len(idx) > 3:
        n = len(idx)
        fatto = False
        for k in range(n):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % n]
            a, b, c = pts[i0], pts[i1], pts[i2]
            if cross(a, b, c) <= 1e-10:
                continue
            ok = True
            for m in idx:
                if m in (i0, i1, i2):
                    continue
                p = pts[m]
                if min(math.dist(p, a), math.dist(p, b), math.dist(p, c)) < 1e-7:
                    continue
                if _dentro_tri(p, a, b, c):
                    ok = False
                    break
            if ok:
                tris.append((a, b, c))
                idx.pop(k)
                fatto = True
                break
        if not fatto:
            for k in range(n):        # vertici allineati: si tolgono senza triangolo
                if abs(cross(pts[idx[k - 1]], pts[idx[k]], pts[idx[(k + 1) % n]])) <= 1e-8:
                    idx.pop(k)
                    fatto = True
                    break
        if not fatto:
            raise RuntimeError('triangolazione bloccata con %d vertici' % len(idx))
    if len(idx) == 3 and abs(cross(pts[idx[0]], pts[idx[1]], pts[idx[2]])) > 1e-10:
        tris.append(tuple(pts[i] for i in idx))
    return tris


def triangola(esterno, buchi=()):
    """Poligono semplice con buchi -> triangoli (taglio a orecchie, buchi uniti con ponti)."""
    poly = ccw(esterno)
    hs = [ccw(h)[::-1] for h in buchi]
    hs.sort(key=lambda h: -max(q[0] for q in h))
    for k, h in enumerate(hs):
        j = max(range(len(h)), key=lambda i: h[i][0])
        M = h[j]
        segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
        for h2 in hs[k:]:
            segs += [(h2[i], h2[(i + 1) % len(h2)]) for i in range(len(h2))]
        vertici = [q for s in segs for q in s]
        scelto = None
        for i in sorted(range(len(poly)), key=lambda i: math.dist(poly[i], M)):
            V = poly[i]
            if any(_attraversa(M, V, a, b) for a, b in segs):
                continue
            if any(_sul_segmento(w, M, V) for w in vertici):
                continue
            scelto = i
            break
        if scelto is None:
            raise RuntimeError('ponte per il buco non trovato')
        poly = poly[:scelto + 1] + h[j:] + h[:j + 1] + poly[scelto:]
    return _orecchie(poly)


# ---------------------------------------------------------------- dal piano allo spazio
def a3d(uv, liv, asse):
    """Punti (u, v) del piano a quota liv lungo l'asse: 'z' -> (u, v, liv), 'y' -> (u, liv, v), 'x' -> (liv, u, v)."""
    uv = np.asarray(uv, float)
    l = np.broadcast_to(np.asarray(liv, float), (len(uv),))
    if asse == 'z':
        return np.c_[uv[:, 0], uv[:, 1], l]
    if asse == 'y':
        return np.c_[uv[:, 0], l, uv[:, 1]]
    return np.c_[l, uv[:, 0], uv[:, 1]]


def faccia(esterno, buchi, liv, asse='z'):
    t = np.array(triangola(esterno, buchi))
    return np.stack([a3d(t[:, k, :], liv, asse) for k in range(3)], axis=1)


def pareti(anello, a0, a1, asse='z'):
    out = []
    n = len(anello)
    for i in range(n):
        p, q = anello[i], anello[(i + 1) % n]
        A0, B0, B1, A1 = a3d([p, q, q, p], [a0, a0, a1, a1], asse)
        out += [(A0, B0, B1), (A0, B1, A1)]
    return np.array(out)


def lastra(esterno, buchi, a0, a1, asse='z', sotto=True):
    parti = [faccia(esterno, buchi, a1, asse), pareti(esterno, a0, a1, asse)]
    if sotto:
        parti.append(faccia(esterno, buchi, a0, asse))
    for h in buchi:
        parti.append(pareti(h, a0, a1, asse))
    return np.concatenate(parti)


def quad(a, b, c, d):
    return np.array([(a, b, c), (a, c, d)], float)


def aggiungi(s, tri, colore, **kw):
    tri = np.asarray(tri, float)
    s.mesh(tri.reshape(-1, 3), np.arange(len(tri) * 3).reshape(-1, 3), colore, **kw)


def trasforma(tri, m):
    t = tri.reshape(-1, 3)
    return (t @ m[:3, :3].T + m[:3, 3]).reshape(tri.shape)


# ---------------------------------------------------------------- modello attuale: facce coperte e ricolori
def togli_coperte(s, gruppo, coperture):
    """Toglie da un gruppo le parti di faccia (nella terna di ogni zampa) che stanno sotto una cover.
    coperture: (asse 0/1/2, quota del piano, pezzi convessi nel piano)."""
    T = s.gruppi[gruppo]['tri']
    tieni = np.ones(len(T), bool)
    nuovi = []
    tolti = 0
    for n in COXE:
        M = terna_zampa(n)
        TL = trasforma(T, np.linalg.inv(M))
        reg = (TL[:, :, 0].min(1) > 25) & (TL[:, :, 0].max(1) < 220) & (np.abs(TL[:, :, 1]).max(1) < 45)
        for ax, val, pezzi in coperture:
            m = reg & tieni & (np.abs(TL[:, :, ax] - val).max(1) < 0.02)
            if not m.any():
                continue
            tieni &= ~m
            tolti += int(m.sum())
            uv = [i for i in range(3) if i != ax]
            for t in TL[m]:
                p2 = [tuple(q[uv]) for q in t]
                if abs(area(p2)) < 1e-9:
                    continue
                poligoni = [ccw(p2)]
                for C in pezzi:
                    poligoni = meno_convesso(poligoni, ccw(C))
                for P in poligoni:
                    for k in range(1, len(P) - 1):
                        tri = np.zeros((3, 3))
                        tri[:, ax] = val
                        tri[:, uv] = [P[0], P[k], P[k + 1]]
                        nuovi.append(trasforma(tri[None], M)[0])
    s.gruppi[gruppo]['tri'] = np.concatenate([T[tieni]] + ([np.array(nuovi)] if nuovi else []))
    return tolti, len(nuovi)


def maschera_zampe(s, gruppo, cond):
    """Triangoli del gruppo che, nella terna di una delle sei zampe, soddisfano cond(triangoli in terna zampa)."""
    T = s.gruppi[gruppo]['tri']
    m = np.zeros(len(T), bool)
    for n in COXE:
        TL = trasforma(T, np.linalg.inv(terna_zampa(n)))
        reg = (TL[:, :, 0].min(1) > 25) & (TL[:, :, 0].max(1) < 220) & (np.abs(TL[:, :, 1]).max(1) < 45)
        m |= reg & cond(TL)
    return m


def estrai(s, gruppo, maschera):
    """Toglie dal gruppo i triangoli scelti e li restituisce (per ricolorarli come parti nuove)."""
    T = s.gruppi[gruppo]['tri']
    s.gruppi[gruppo]['tri'] = T[~maschera]
    return T[maschera]


# ---------------------------------------------------------------- carapace
Z_BORDO, Z_TOP, SP = 28.4, 36.0, 1.6
R_LOBO = 32.3


def esagono(c, r=R_LOBO):
    return [(c[0] + r * math.cos(math.radians(60 * k)), c[1] + r * math.sin(math.radians(60 * k))) for k in range(6)]


def contorno_carapace():
    AS, MS, PS = esagono((80, 44)), esagono((0, 48)), esagono((-80, 44))
    y50 = ((0, 50), (1, 50))
    H = incrocio((102, 12), (94, 20), AS[5], AS[0])          # smusso in pianta della testa contro il lobo AS
    L = [H, AS[0], AS[1], AS[2], incrocio(AS[2], AS[3], *y50), incrocio(MS[0], MS[1], *y50), MS[1], MS[2],
         incrocio(MS[2], MS[3], *y50), incrocio(PS[0], PS[1], *y50), PS[1], PS[2], PS[3],
         incrocio(PS[3], PS[4], (-96.2, 0), (-96.2, 1))]
    cont = [(102.0, -12.0), (102.0, 12.0)] + L + [(x, -y) for x, y in reversed(L)]
    d = [6.0] * len(cont)
    d[0] = d[1] = d[-1] = 4.0          # viso e smussi in pianta della testa: visiera 4 x 45
    return cont, d


def fai_carapace(s):
    cont, d = contorno_carapace()
    q = rientra(cont, d)
    n = len(cont)
    print('carapace: area in pianta %.0f mm2, perimetro %.0f mm, ingombro x %.1f..%.1f, y %.1f..%.1f'
          % (area(cont), sum(math.dist(cont[i], cont[(i + 1) % n]) for i in range(n)),
             min(p[0] for p in cont), max(p[0] for p in cont), min(p[1] for p in cont), max(p[1] for p in cont)))
    print('  semicontorno sinistro:', ' '.join('(%.2f; %.2f)' % p for p in cont[1:n // 2 + 1]))

    # bordo verticale e smusso (il bordo del viso e' una parete a parte con il vano dell'occhio)
    bordo = []
    for i in range(n):
        j = (i + 1) % n
        zt = Z_TOP - d[i]
        if i != 0:
            bordo.append(quad((*cont[i], Z_BORDO), (*cont[j], Z_BORDO), (*cont[j], zt), (*cont[i], zt)))
        bordo.append(quad((*cont[i], zt), (*cont[j], zt), (*q[j], Z_TOP), (*q[i], Z_TOP)))
        if d[i - 1] != d[i]:
            bordo.append(np.array([((*cont[i], Z_TOP - d[i - 1]), (*cont[i], Z_TOP - d[i]), (*q[i], Z_TOP))]))
    aggiungi(s, np.concatenate(bordo), BIANCO)

    # faccia piana: due parti bianche ai lati della fascia nera (|y| <= 17)
    sx = taglia(q, (0, 17), (1, 17), sinistra=True)
    x_fer = [18 + i * 7.3 for i in range(5)]
    feritoie = [rett(x, 28.5, x + 6, 31.5) for x in x_fer]
    pozzi = [(40.0, 22.5), (-56.0, 22.5)]
    buchi_sx = [cerchio(c, 3.5, 28) for c in pozzi] + feritoie
    aggiungi(s, faccia(sx, buchi_sx, Z_TOP), BIANCO, specchia_y=True)
    for f in feritoie:                                                      # feritoie: pelle da 1,6 e buio sotto
        aggiungi(s, pareti(f, Z_TOP - SP, Z_TOP), BIANCO, specchia_y=True)
        aggiungi(s, faccia(f, [], Z_TOP - SP), OMBRA, specchia_y=True)
    for c in pozzi:                                                         # pozzetti con la testa della vite
        aggiungi(s, pareti(cerchio(c, 3.5, 28), 30.0, Z_TOP), BIANCO, specchia_y=True)
        aggiungi(s, faccia(cerchio(c, 3.5, 28), [cerchio(c, 2.75, 28)], 30.0), BIANCO, specchia_y=True)
        aggiungi(s, lastra(cerchio(c, 2.75, 28), [], 30.0, 33.4, sotto=False), INOX, specchia_y=True)

    # fascia nera, sportellino ottagonale a filo, pulsante, finestra del cicalino, tacca
    fascia = taglia(taglia(q, (0, 17), (1, 17), sinistra=False), (0, -17), (1, -17), sinistra=True)
    ott = [(-14, -17), (22, -17), (28, -11), (28, 11), (22, 17), (-14, 17), (-20, 11), (-20, -11)]
    dietro = [(-90.2, -17), (-14, -17), (-20, -11), (-20, 11), (-14, 17), (-90.2, 17)]
    davanti = taglia(fascia, (22, 0), (22, 1), sinistra=False)             # x >= 22
    k = min(range(len(davanti)), key=lambda i: math.dist(davanti[i], (22, 17)))
    davanti = davanti[:k + 1] + [(28, 11), (28, -11)] + davanti[k + 1:]
    print('  fascia: dietro x %.1f, davanti fino a x %.2f' % (min(p[0] for p in dietro), max(p[0] for p in davanti)))
    puls, fin, tacca = cerchio((-40, 0), 6.1, 36), rett(-81.5, -12, -67.5, 12), rett(29, -5, 32, 5)
    aggiungi(s, faccia(dietro, [puls, fin], Z_TOP), NERO)
    aggiungi(s, faccia(davanti, [tacca], Z_TOP), NERO)
    porta = rientra(ccw(ott), 0.4)
    aggiungi(s, faccia(porta, [], Z_TOP), NERO)
    aggiungi(s, pareti(porta, Z_TOP - 0.6, Z_TOP), NERO)
    aggiungi(s, faccia(ott, [porta], Z_TOP - 0.6), FUGA)
    aggiungi(s, pareti(tacca, Z_TOP - 0.8, Z_TOP), NERO)
    aggiungi(s, faccia(tacca, [], Z_TOP - 0.8), OMBRA)
    aggiungi(s, pareti(fin, Z_TOP - SP, Z_TOP), NERO)
    # pulsante da pannello: corpo inox con il tasto al centro
    aggiungi(s, pareti(cerchio((-40, 0), 6.0, 36), 34.0, 36.6), INOX)
    aggiungi(s, faccia(cerchio((-40, 0), 6.0, 36), [cerchio((-40, 0), 4.2, 36)], 36.6), INOX)
    aggiungi(s, lastra(cerchio((-40, 0), 4.2, 36), [], 36.6, 36.9, sotto=False), INOX_CHIARO)

    # testa: viso con il vano dell'occhio, smussi in pianta e fianchi fino a z -1
    occhio_e = rett(-9.15, 22.5 - 7.95, 9.15, 22.5 + 7.95)                 # bocca esterna a x 102 (y, z)
    occhio_i = rett(-5.55, 22.5 - 5.25, 5.55, 22.5 + 5.25)                 # bocca interna a x 99,4
    aggiungi(s, faccia(rett(-12, -1, 12, 32), [occhio_e], 102.0, 'x'), BIANCO)
    e3, i3 = a3d(occhio_e, 102.0, 'x'), a3d(occhio_i, 99.4, 'x')
    aggiungi(s, np.concatenate([quad(e3[k], e3[(k + 1) % 4], i3[(k + 1) % 4], i3[k]) for k in range(4)]), NERO)
    aggiungi(s, faccia(rett(-6.2, 15.5, 6.2, 29.5), [], 98.0, 'x'), OMBRA)  # fondo buio della testa
    aggiungi(s, pareti(cerchio((0, 22.5), 3.5, 32), 98.5, 99.1, 'x'), '#26282c')
    aggiungi(s, faccia(cerchio((0, 22.5), 3.5, 32), [cerchio((0, 22.5), 2.4, 32)], 99.1, 'x'), '#26282c')
    aggiungi(s, faccia(cerchio((0, 22.5), 2.4, 32), [], 99.1, 'x'), VETRO)
    aggiungi(s, quad((102, 12, -1), (94, 20, -1), (94, 20, Z_BORDO), (102, 12, Z_BORDO)), BIANCO, specchia_y=True)
    aggiungi(s, quad((94, 20, -1), (81, 20, -1), (81, 20, Z_BORDO), (94, 20, Z_BORDO)), BIANCO, specchia_y=True)

    # gonne sulle pareti delle baie
    for x0, x1 in ((22, 58.8), (-58.8, -22)):
        s.scatola(x0, 48.8, 7.0, x1, 50.0, Z_BORDO, BIANCO, specchia_y=True)


def fai_coda(s):
    # cicalino spostato a x -87...-62, appeso al collare del carapace; display sotto la finestra 14 x 24
    box = rett(-87, -20, -62, 20)
    disp = rett(-81.0, -11.5, -68.0, 11.5)
    aggiungi(s, pareti(box, 17.4, 28.4), CICALINO)
    aggiungi(s, faccia(box, [disp], 28.4), CICALINO)
    aggiungi(s, faccia(disp, [], 28.4), DISPLAY)
    aggiungi(s, faccia(box, [], 17.4), CICALINO)
    # sportello della batteria in PETG bianco (lo smusso da 1 mm e' troppo piccolo per questa scala)
    b = s.gruppi['base']['tri']
    c = b.mean(1)
    m = (b[:, :, 0].max(1) <= -85.39) & (c[:, 0] < -85.45) & (np.abs(c[:, 1]) < 32) & (c[:, 2] < -9.3)
    aggiungi(s, estrai(s, 'base', m), BIANCO)
    print('sportello della batteria: %d triangoli ricolorati' % m.sum())
    # fronte della testa della camera (oggi nel gruppo interni): nera
    t = s.gruppi['interni']['tri']
    m = t[:, :, 0].min(1) >= 98.45
    aggiungi(s, estrai(s, 'interni', m), NERO)


# ---------------------------------------------------------------- cover delle zampe (terna della zampa)
LAMA_ESAG = [(67.2, 0), (74.7, -13), (100.3, -13), (107.8, 0), (100.3, 13), (74.7, 13)]          # (X, Z)
GOBBA = [(76.5, 13), (99, 13), (95, 20), (80.5, 20)]
LAMA = [(67.2, 0), (74.7, -13), (100.3, -13), (107.8, 0), (100.3, 13), (99, 13), (95, 20), (80.5, 20), (76.5, 13),
        (74.7, 13)]
RIQUADRO = [(76.5, 0), (99, 0), (99, 13), (95, 20), (80.5, 20), (76.5, 13)]
LAMA_MENO_RIQ = [(67.2, 0), (74.7, -13), (100.3, -13), (107.8, 0), (100.3, 13), (99, 13), (99, 0), (76.5, 0),
                 (76.5, 13), (74.7, 13)]
VITI_BLOCCO = [(81, 4.5), (81, 12.9), (94.5, 7.5), (94.5, 12.9)]
Y_A, Y_B, SP_COV, Y_CUSC = 30.55, -30.55, 1.2, 33.95
# schiniere, nel piano (Y, Z) della faccia esterna della culla del ginocchio
SCH_PIASTRA = rett(-24.15, -38.35, 19.65, 13.65)
SCH_PIEGA = [(-24.15, -38.35), (19.65, -38.35), (19.65, -42.8), (17.65, -44.8), (-17.65, -44.8)]
SCH_STINCO = [(-17.65, -44.8), (17.65, -44.8), (0.0, -62.45)]


def fai_lame(s):
    kw = dict(zampe=True)
    # lama A: piastra 1,2 + cuscinetto fino a Y 33,95 con le quattro teste M3 incassate di 0,4
    ya1 = Y_A + SP_COV
    aggiungi(s, faccia(LAMA_MENO_RIQ, [], ya1, 'y'), BIANCO, **kw)
    aggiungi(s, pareti(LAMA, Y_A, ya1, 'y'), BIANCO, **kw)
    # le due sedi verso il ginocchio distano 5,4 e hanno diametro 5,6: nel pezzo si fondono in un'asola
    sedi = [cerchio(VITI_BLOCCO[0], 2.8, 28), cerchio(VITI_BLOCCO[1], 2.8, 28), due_cerchi(VITI_BLOCCO[2], VITI_BLOCCO[3], 2.8)]
    aggiungi(s, faccia(RIQUADRO, sedi, Y_CUSC, 'y'), BIANCO, **kw)
    aggiungi(s, pareti(RIQUADRO, ya1, Y_CUSC, 'y'), BIANCO, **kw)
    for h in sedi:
        aggiungi(s, pareti(h, Y_CUSC - 0.4, Y_CUSC, 'y'), BIANCO, **kw)
    for c in VITI_BLOCCO:
        esag = cerchio(c, 1.45, 6, math.pi / 6)
        aggiungi(s, faccia(cerchio(c, 2.75, 28), [esag], Y_CUSC - 0.4, 'y'), INOX, **kw)
        aggiungi(s, pareti(esag, Y_CUSC - 1.6, Y_CUSC - 0.4, 'y'), OMBRA, **kw)
        aggiungi(s, faccia(esag, [], Y_CUSC - 1.6, 'y'), OMBRA, **kw)
    # lama B: piastra 1,2 con il riquadro segnato da una scanalatura a V 0,8 x 0,4
    yb1 = Y_B - SP_COV
    est = [(67.2, 0), (74.7, -13), (100.3, -13), (107.8, 0), (100.3, 13), (99.4, 13), (99.4, -0.4), (76.1, -0.4),
           (76.1, 13), (74.7, 13)]
    inn = [(76.9, 0.4), (98.6, 0.4), (98.6, 13.7), (95, 20), (80.5, 20), (76.9, 13.7)]
    aggiungi(s, faccia(est, [], yb1, 'y'), BIANCO, **kw)
    aggiungi(s, faccia(inn, [], yb1, 'y'), BIANCO, **kw)
    aggiungi(s, pareti(LAMA, Y_B, yb1, 'y'), BIANCO, **kw)
    mezzo = [(76.5, 13), (76.5, 0), (99, 0), (99, 13)]
    bordo_e = [(76.1, 13), (76.1, -0.4), (99.4, -0.4), (99.4, 13)]
    bordo_i = [(76.9, 13.7), (76.9, 0.4), (98.6, 0.4), (98.6, 13.7)]
    v = []
    for bordo in (bordo_e, bordo_i):
        for k in range(3):
            A, B = a3d([bordo[k], bordo[k + 1]], yb1, 'y')
            C, D = a3d([mezzo[k + 1], mezzo[k]], yb1 + 0.4, 'y')
            v.append(quad(A, B, C, D))
    aggiungi(s, np.concatenate(v), BIANCO, **kw)


def fai_teste_mozzi(s):
    """Teste inox delle viti delle squadrette sui mozzi del lato A (il modello non le ha) e teste dei perni sul lato B."""
    kw = dict(zampe=True)
    for xc in (55.0, 120.0):
        for dx, dz in ((-7, 0), (7, 0), (0, 7), (0, -7)):
            c = (xc + dx, dz)
            esag = cerchio(c, 1.45, 6, math.pi / 6)
            aggiungi(s, faccia(cerchio(c, 2.75, 28), [esag], Y_A + 3.0, 'y'), INOX, **kw)
            aggiungi(s, pareti(cerchio(c, 2.75, 28), Y_A, Y_A + 3.0, 'y'), INOX, **kw)
            aggiungi(s, pareti(esag, Y_A + 1.8, Y_A + 3.0, 'y'), OMBRA, **kw)
            aggiungi(s, faccia(esag, [], Y_A + 1.8, 'y'), OMBRA, **kw)
    m = maschera_zampe(s, 'zampe_servo', lambda TL: TL[:, :, 1].max(1) < -30.5)
    aggiungi(s, estrai(s, 'zampe_servo', m), INOX)
    # piedini in TPU nero (la parte sotto Z -95)
    m = maschera_zampe(s, 'zampe_struttura', lambda TL: TL[:, :, 2].max(1) <= -94.9)
    aggiungi(s, estrai(s, 'zampe_struttura', m), '#161719')


def fai_schiniere(s):
    kw = dict(zampe=True)
    s.scatola(132.45, -24.15, -38.35, 133.65, 19.65, 13.65, BIANCO, **kw)       # piastra sulla culla
    s.scatola(130.65, -24.15, 12.45, 133.65, 9.45, 13.65, BIANCO, **kw)         # labbro sopra la parete
    punti = []
    for y, z in SCH_PIEGA:                                                      # piega a 45 verso lo stinco
        xo = 133.65 + (z + 38.35)
        punti += [(xo, y, z), (xo - SP_COV, y, z)]
    s.solido(punti, BIANCO, **kw)
    s.prisma(SCH_STINCO, 126.0, 127.2, BIANCO, asse='x', **kw)                 # punta sullo stinco


def main():
    s = Scena()
    s.nascondi('coperchio')
    s.colore('base', ANTRACITE)
    s.colore('zampe_struttura', ANTRACITE)
    s.colore('servo_coxa', SERVO)
    s.colore('zampe_servo', SERVO)
    tolti = togli_coperte(s, 'zampe_struttura', [
        (1, Y_A, [LAMA_ESAG, GOBBA]),
        (1, Y_B, [LAMA_ESAG, GOBBA]),
        (0, 132.45, [SCH_PIASTRA]),
        (2, 12.45, [rett(130.65, -24.15, 133.65, 9.45)]),
        (0, 126.0, [SCH_STINCO]),
    ])
    print('facce coperte: %d triangoli tolti, %d rimessi fuori dalle cover' % tolti)
    fai_carapace(s)
    fai_coda(s)
    fai_lame(s)
    fai_schiniere(s)
    fai_teste_mozzi(s)
    fatti = s.render(BASE, viste=('iso_ant', 'iso_post', 'fianco', 'alto', 'fronte'), titolo=TITOLO)
    fatti += s.render(BASE, viste=('zampa',), centro=(150, 85, -20), titolo=TITOLO)
    fatti += s.render(BASE, viste=((16, 25, 3.2),), centro=(92, 0, 15), titolo=TITOLO)    # dettaglio della testa
    for f in fatti:
        print(f)


if __name__ == '__main__':
    main()
