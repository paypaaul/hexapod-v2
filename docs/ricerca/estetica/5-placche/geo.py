"""Geometria delle placche bombate (seconda passata sulle cover di Kabuto corretto). Unita' mm.

- raccorda(): contorno con raccordi in pianta (convessi e concavi), come un raccordo di schizzo o un raccordo sugli
  spigoli perpendicolari alla lastra in Fusion;
- Placca: lastra con faccia interna piana e faccia esterna = bombatura cilindrica (intersezione con un cilindro di
  raggio Rb, asse nel piano della lastra; facoltativo un secondo cilindro Rb2 con l'asse perpendicolare) e raccordo r
  su tutti gli spigoli della faccia esterna (contorno, finestre, fori). E' la sequenza CAD estrudi -> interseca con
  il cilindro (o i due cilindri) -> raccorda, quindi lo spessore e':
      h(u, v) = t_c - (q - q_c)^2 / (2 Rb) [- (p - p_c)^2 / (2 Rb2)]   q trasversale, p longitudinale
      vicino al bordo (distanza d < r): h - r + sqrt(r^2 - (r - d)^2)
  Restituisce triangoli (u, v, h), volume, ingombro dello spessore per fasce (per i conti in pianta).
"""
import math

import numpy as np
from matplotlib.path import Path
from scipy.spatial import Delaunay


# ----------------------------------------------------------------------------- contorni
def area(p):
    p = np.asarray(p, float)
    return 0.5 * float(np.sum(p[:, 0] * np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1) * p[:, 1]))


def perimetro(p):
    p = np.asarray(p, float)
    return float(np.sum(np.linalg.norm(np.roll(p, -1, 0) - p, axis=1)))


def ccw(p):
    p = [tuple(map(float, q)) for q in p]
    return p if area(p) > 0 else p[::-1]


def raccorda(poly, raggi, passo_ang=6.0):
    """Raccordi d'arco ai vertici (raggio per vertice, 0 = spigolo vivo). Errore se due raccordi non ci stanno sul lato."""
    P = [np.asarray(q, float) for q in poly]
    n = len(P)
    raggi = list(raggi) if hasattr(raggi, '__len__') else [raggi] * n
    tang = []
    for i in range(n):
        a = P[i] - P[i - 1]
        b = P[(i + 1) % n] - P[i]
        a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
        th = math.acos(max(-1.0, min(1.0, float(a @ b))))
        tang.append((a, b, th, raggi[i] * math.tan(th / 2)))
    for i in range(n):
        L = np.linalg.norm(P[(i + 1) % n] - P[i])
        if tang[i][3] + tang[(i + 1) % n][3] > L + 1e-6:
            raise ValueError('raccordi ai vertici %d e %d non stanno sul lato lungo %.2f (%.2f + %.2f)'
                             % (i, (i + 1) % n, L, tang[i][3], tang[(i + 1) % n][3]))
    out = []
    for i in range(n):
        a, b, th, t = tang[i]
        r = raggi[i]
        if r <= 0 or th < 1e-6:
            out.append(tuple(P[i]))
            continue
        T1, T2 = P[i] - a * t, P[i] + b * t
        sx = 1.0 if (a[0] * b[1] - a[1] * b[0]) > 0 else -1.0          # svolta a sinistra = centro a sinistra
        nrm = sx * np.array([-a[1], a[0]])
        C = T1 + nrm * r
        f0 = math.atan2(*(T1 - C)[::-1])
        f1 = math.atan2(*(T2 - C)[::-1])
        df = (f1 - f0 + math.pi) % (2 * math.pi) - math.pi
        k = max(2, int(math.ceil(abs(math.degrees(df)) / passo_ang)))
        for j in range(k + 1):
            f = f0 + df * j / k
            out.append((C[0] + r * math.cos(f), C[1] + r * math.sin(f)))
    return out


def esagono(c, ap, fase=0.0):
    """Esagono di apotema ap, vertici a fase, fase+60... (fase 0: vertici lungo u)."""
    R = ap / math.cos(math.radians(30))
    return [(c[0] + R * math.cos(math.radians(fase + 60 * k)), c[1] + R * math.sin(math.radians(fase + 60 * k))) for k in range(6)]


def cerchio(c, r, n=40, fase=0.0):
    return [(c[0] + r * math.cos(fase + 2 * math.pi * k / n), c[1] + r * math.sin(fase + 2 * math.pi * k / n)) for k in range(n)]


def ricampiona(a, h):
    a = np.asarray(a, float)
    pts = []
    for k in range(len(a)):
        p0, p1 = a[k], a[(k + 1) % len(a)]
        n = max(1, int(math.ceil(np.linalg.norm(p1 - p0) / h)))
        pts += [p0 + (p1 - p0) * t / n for t in range(n)]
    return np.array(pts)


def dist_segmenti(q, segm):
    a, b = segm[:, 0], segm[:, 1]
    ab = b - a
    out = np.empty(len(q))
    for i0 in range(0, len(q), 2000):
        qq = q[i0:i0 + 2000]
        t = np.clip(((qq[:, None, :] - a) * ab).sum(2) / np.maximum((ab * ab).sum(1), 1e-12), 0, 1)
        out[i0:i0 + 2000] = np.linalg.norm(qq[:, None, :] - (a + t[..., None] * ab), axis=2).min(1)
    return out


def dist_poligono_cerchio(poly, c, r):
    """Distanza minima tra il contorno di un poligono e una circonferenza interna (gioco della parete attorno a un tubo)."""
    P = np.asarray(poly, float)
    segm = np.stack([P, np.roll(P, -1, 0)], 1)
    return float(dist_segmenti(np.array([c], float), segm)[0] - r)


# ----------------------------------------------------------------------------- placca
class Placca:
    def __init__(self, contorno, fori, t_c, Rb, q_c, asse_q, r_bordo, passo=0.8, Rb2=0.0, q_c2=0.0):
        """contorno e fori in (u, v); asse_q = 0 se la bombatura varia con u, 1 se con v; q_c: coordinata della cresta."""
        self.contorno = ccw(contorno)
        self.fori = [ccw(f) for f in fori]
        self.t_c, self.Rb, self.q_c, self.asse_q, self.r = t_c, Rb, q_c, asse_q, r_bordo
        self.Rb2, self.q_c2 = Rb2, q_c2          # seconda bombatura (cilindro con l'asse perpendicolare al primo)
        anelli = [self.contorno] + self.fori
        self.paths = [Path(np.asarray(a)) for a in anelli]
        bordi = [ricampiona(a, passo * 0.5) for a in anelli]
        self.segm = np.concatenate([np.stack([b, np.roll(b, -1, 0)], 1) for b in bordi])
        # punti: bordo, anelli interni alle distanze del raccordo (lungo la normale), griglia
        extra = []
        for b in bordi:
            tng = np.roll(b, -1, 0) - np.roll(b, 1, 0)
            tng /= np.maximum(np.linalg.norm(tng, axis=1, keepdims=True), 1e-12)
            nrm = np.c_[-tng[:, 1], tng[:, 0]]
            for d in (0.15, 0.4, 0.7, 1.0, 1.4):
                for sgn in (1, -1):
                    extra.append(b + sgn * nrm * d * max(self.r, 0.3))
        lo, hi = np.min(anelli[0], 0), np.max(anelli[0], 0)
        gu, gv = np.meshgrid(np.arange(lo[0] + passo / 2, hi[0], passo), np.arange(lo[1] + passo / 2, hi[1], passo))
        griglia = np.c_[gu.ravel(), gv.ravel()]
        cand = np.concatenate(extra + [griglia])
        cand = cand[self.dentro(cand)]
        dc = dist_segmenti(cand, self.segm)
        cand = cand[dc > passo * 0.12]
        nb = sum(len(b) for b in bordi)
        self.pts = np.concatenate(bordi + [cand])
        self.d = dist_segmenti(self.pts, self.segm)
        self.d[:nb] = 0.0
        self.nb = nb
        self.bordi = bordi
        tri = Delaunay(self.pts).simplices
        cen = self.pts[tri].mean(1)
        tri = tri[self.dentro(cen)]
        P = self.pts[tri]
        ar = 0.5 * np.abs((P[:, 1, 0] - P[:, 0, 0]) * (P[:, 2, 1] - P[:, 0, 1]) - (P[:, 2, 0] - P[:, 0, 0]) * (P[:, 1, 1] - P[:, 0, 1]))
        lmax = np.max(np.linalg.norm(P - np.roll(P, 1, axis=1), axis=2), axis=1)
        self.buoni = ar >= 0.02 * lmax ** 2                 # i triangoli schiacciati hanno normale instabile nei render
        self.tri = tri
        self.h = self.spessore(self.pts, self.d)

    def dentro(self, q):
        m = self.paths[0].contains_points(q)
        for p in self.paths[1:]:
            m &= ~p.contains_points(q)
        return m

    def cresta(self, q):
        h = self.t_c - (q[:, self.asse_q] - self.q_c) ** 2 / (2 * self.Rb) if self.Rb else np.full(len(q), self.t_c)
        if self.Rb2:
            h = h - (q[:, 1 - self.asse_q] - self.q_c2) ** 2 / (2 * self.Rb2)
        return h

    def spessore(self, q, d):
        h = self.cresta(q)
        r = self.r
        if r > 0:
            dd = np.minimum(d, r)
            h = h - r + np.sqrt(np.clip(r * r - (r - dd) ** 2, 0, None))
        return h

    def triangoli(self, fondo=False):
        """Triangoli in (u, v, h): faccia esterna, pareti del bordo (da 0 allo spessore al bordo), fondo se richiesto."""
        sopra = np.c_[self.pts, self.h][self.tri[self.buoni]]
        parti = [sopra]
        if fondo:
            parti.append(np.c_[self.pts, np.zeros(len(self.pts))][self.tri])
        off = 0
        for b in self.bordi:
            m = len(b)
            hb = self.h[off:off + m]
            for k in range(m):
                k1 = (k + 1) % m
                a0, a1 = b[k], b[k1]
                parti.append(np.array([[(*a0, 0), (*a1, 0), (*a1, hb[k1])], [(*a0, 0), (*a1, hb[k1]), (*a0, hb[k])]]))
            off += m
        return np.concatenate(parti)

    def volume(self):
        P = self.pts[self.tri]
        a = 0.5 * np.abs((P[:, 1, 0] - P[:, 0, 0]) * (P[:, 2, 1] - P[:, 0, 1]) - (P[:, 2, 0] - P[:, 0, 0]) * (P[:, 1, 1] - P[:, 0, 1]))
        return float(np.sum(a * self.h[self.tri].mean(1)))

    def area(self):
        return area(self.contorno) - sum(area(f) for f in self.fori)

    def massimo(self):
        return float(self.h.max())

    def minimo_bordo(self):
        """Spessore minimo del bordo (parete verticale sotto il raccordo)."""
        return float(self.h[:self.nb].min())

    def profilo(self, asse=0, passo=1.0):
        """Spessore massimo per fasce lungo l'asse dato (u se 0): [(c0, c1, hmax)] per i conti in pianta."""
        c = self.pts[:, asse]
        lo, hi = c.min(), c.max()
        out = []
        x = lo
        while x < hi - 1e-9:
            m = (c >= x - 1e-9) & (c <= x + passo + 1e-9)
            if m.any():
                out.append((x, min(x + passo, hi), float(self.h[m].max())))
            x += passo
        return out
