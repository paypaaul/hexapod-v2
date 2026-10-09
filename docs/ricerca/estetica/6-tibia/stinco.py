"""Mesh e sezioni dello stinco di una variante (terna della zampa, mm)."""
import importlib.util
import math

import numpy as np

from varianti import VARIANTI, Z0, Y_ORLO

_spec = importlib.util.spec_from_file_location('kabuto', '/Users/paul/.claude/jobs/3d86073b/tmp/estetica/sfaccettato/concept.py')
K = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(K)

XK = 120.0
PASSO_Z = 0.5


def profilo(v, z_basso=None):
    """Contorno (x, z) della sagoma esterna, da z0 alla punta, in senso antiorario."""
    zc, r = v['zc'], v['r']
    zs = list(np.arange(Z0, zc, -PASSO_Z)) + [zc]
    sin = [(XK - v['sx'](z), z) for z in zs]
    arco = [(XK - r * math.cos(t), zc - r * math.sin(t)) for t in np.linspace(0, math.pi, 37)[1:-1]]
    des = [(XK + v['dx'](z), z) for z in reversed(zs)]
    return K.pulisci(sin + arco + des, 1e-6)


def finestra(v, f, n=12):
    z1, z2, w, tonda = f
    zm = (z1 + z2) / 2
    xc = XK + (v['dx'](zm) - v['sx'](zm)) / 2          # al centro tra i due fianchi
    if not tonda:
        return [(xc - w, z1), (xc - w, z2), (xc + w, z2), (xc + w, z1)]
    out = [(xc - w * math.cos(t), z2 + w - w * math.sin(t)) for t in np.linspace(0, math.pi, n)]
    out += [(xc + w * math.cos(t), z1 - w + w * math.sin(t)) for t in np.linspace(0, math.pi, n)]
    return out


def semilarghezze(v, z):
    """(xl, xr) della sagoma a quota z (arco della punta compreso)."""
    zc, r = v['zc'], v['r']
    if z >= zc:
        return XK - v['sx'](z), XK + v['dx'](z)
    h = math.sqrt(max(r * r - (z - zc) ** 2, 0.0))
    return XK - h, XK + h


def intervallo_finestra(h, z):
    inter = []
    for i in range(len(h)):
        p, q = h[i], h[(i + 1) % len(h)]
        if (p[1] - z) * (q[1] - z) <= 0 and p[1] != q[1]:
            inter.append(p[0] + (z - p[1]) * (q[0] - p[0]) / (q[1] - p[1]))
    return (min(inter), max(inter)) if len(inter) >= 2 else None


def segmenti(v, buchi, z):
    xl, xr = semilarghezze(v, z)
    segs = [(xl, xr)]
    for h in buchi:
        iv = intervallo_finestra(h, z)
        if iv is None or iv[1] - iv[0] < 1e-9:
            continue
        a, c = iv
        nuovi = []
        for s0, s1 in segs:
            if c <= s0 or a >= s1:
                nuovi.append((s0, s1))
            else:
                if a > s0:
                    nuovi.append((s0, a))
                if c < s1:
                    nuovi.append((c, s1))
        segs = nuovi
    return segs


def livelli(v, buchi, z_alto, z_basso):
    zc, r = v['zc'], v['r']
    zs = set(np.round(np.arange(z_alto, z_basso, -PASSO_Z), 6)) | {z_alto, z_basso}
    zs |= {round(zc - r * math.sin(t), 6) for t in np.linspace(0, math.pi / 2, 19)}
    for h in buchi:
        zmax, zmin = max(p[1] for p in h), min(p[1] for p in h)
        zs |= {zmax - 1e-4, zmin + 1e-4}
        zs |= {round(p[1], 6) for p in h}
    return sorted([z for z in zs if z_basso - 1e-9 <= z <= z_alto + 1e-9], reverse=True)


def solido(v, buchi, z_alto, z_basso, pareti_buchi=True):
    """Stinco tra due quote: facce +Y (piana, Y_ORLO) e -Y (y = ym(z)) a strisce, pareti esterne e delle finestre."""
    ym = v['ym']
    zs = livelli(v, buchi, z_alto, z_basso)
    facce = []
    for za, zb in zip(zs[:-1], zs[1:]):
        zm = (za + zb) / 2
        sm = segmenti(v, buchi, zm)
        sa, sb = segmenti(v, buchi, za - 1e-7), segmenti(v, buchi, zb + 1e-7)
        if not (len(sa) == len(sb) == len(sm)):
            sa = sb = sm
        for (a0, a1), (b0, b1) in zip(sa, sb):
            for y in (Y_ORLO, None):
                ya, yb = (Y_ORLO, Y_ORLO) if y is not None else (ym(za), ym(zb))
                P = [(a0, ya, za), (a1, ya, za), (b1, yb, zb), (b0, yb, zb)]
                facce += [(P[0], P[1], P[2]), (P[0], P[2], P[3])]
        # pareti esterne (fianchi -X e +X) e delle finestre
        bordi = [x for s in sa for x in s], [x for s in sb for x in s]
        for xa, xb in zip(*bordi):
            A0, B0 = (xa, ym(za), za), (xb, ym(zb), zb)
            A1, B1 = (xa, Y_ORLO, za), (xb, Y_ORLO, zb)
            facce += [(A0, B0, B1), (A0, B1, A1)]
    # chiusure orizzontali in alto e in basso (in alto e' nascosta nello zoccolo; in basso serve al taglio del piedino)
    for z in (z_alto, z_basso):
        for s0, s1 in segmenti(v, buchi, z):
            if s1 - s0 > 1e-6:
                P = [(s0, ym(z), z), (s1, ym(z), z), (s1, Y_ORLO, z), (s0, Y_ORLO, z)]
                facce += [(P[0], P[1], P[2]), (P[0], P[2], P[3])]
    # bordi orizzontali delle finestre (estremi piani, solo per le finestre squadrate)
    for h in buchi:
        for z in (max(p[1] for p in h), min(p[1] for p in h)):
            iv = intervallo_finestra(h, z)
            if iv and iv[1] - iv[0] > 1e-6:
                P = [(iv[0], ym(z), z), (iv[1], ym(z), z), (iv[1], Y_ORLO, z), (iv[0], Y_ORLO, z)]
                facce += [(P[0], P[1], P[2]), (P[0], P[2], P[3])]
    return np.array(facce, float)


def mesh(nome):
    """(struttura, piedino): triangoli dello stinco (antracite) e del piedino (arancio) nella terna della zampa."""
    v = VARIANTI[nome]
    buchi = [finestra(v, f) for f in v['finestre']]
    zp, zt = v['piedino']['z'], v['zc'] - v['r']
    return solido(v, buchi, Z0, zp), solido(v, [], zp, zt)


def sezioni(nome, passo=0.25):
    """Per ogni z: larghezza X, larghezza Y, area, I attorno a Y (flessione nel piano della zampa) e attorno a X
    (flessione fuori dal piano), distanze delle fibre estreme; finestre comprese."""
    v = VARIANTI[nome]
    out = []
    zs = np.arange(Z0 - passo / 2, v['zc'], -passo)
    for z in zs:
        xl, xr = XK - v['sx'](z), XK + v['dx'](z)
        y0, y1 = v['ym'](z), Y_ORLO
        b = y1 - y0
        segs = [(xl, xr)]
        for f in v['finestre']:
            h = finestra(v, f, 24)
            xs = [p[0] for p in h if True]
            # intervallo della finestra a quota z (poligono convesso): intersezione con la retta orizzontale
            inter = []
            for i in range(len(h)):
                p, q = h[i], h[(i + 1) % len(h)]
                if (p[1] - z) * (q[1] - z) <= 0 and p[1] != q[1]:
                    inter.append(p[0] + (z - p[1]) * (q[0] - p[0]) / (q[1] - p[1]))
            if len(inter) >= 2:
                a, c = min(inter), max(inter)
                nuovi = []
                for s0, s1 in segs:
                    if c <= s0 or a >= s1:
                        nuovi.append((s0, s1))
                    else:
                        if a > s0:
                            nuovi.append((s0, a))
                        if c < s1:
                            nuovi.append((c, s1))
                segs = nuovi
        A = sum((s1 - s0) * b for s0, s1 in segs)
        xg = sum((s1 - s0) * b * (s0 + s1) / 2 for s0, s1 in segs) / A
        Iy = sum(b * (s1 - s0) ** 3 / 12 + (s1 - s0) * b * ((s0 + s1) / 2 - xg) ** 2 for s0, s1 in segs)
        Ix = sum((s1 - s0) * b ** 3 / 12 for s0, s1 in segs)
        cx = max(xr - xg, xg - xl)
        out.append(dict(z=z, wx=xr - xl, wy=b, A=A, Iy=Iy, Ix=Ix, cx=cx, cy=b / 2, rotaia=min(s1 - s0 for s0, s1 in segs)))
    return out


def volume(nome):
    """Volume dello stinco sotto lo zoccolo (mm3), punta compresa, finestre tolte (sagoma esterna, piedino compreso)."""
    v = VARIANTI[nome]
    S = sezioni(nome, 0.1)
    V = sum(s['A'] for s in S) * 0.1
    r = v['r']
    V += math.pi * r * r / 2 * (Y_ORLO - v['ym'](v['zc'] - r / 2))
    return V
