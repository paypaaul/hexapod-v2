"""Render schematici del concept "Lamina" (angolo: pannelli) sul modello attuale dell'esapode MG996R.

Uso:  python3 concept.py            -> tutte le viste
      python3 concept.py iso_ant    -> solo le viste nominate (per le prove)

Quote dal concept (mm, terna del robot; le parti di zampa nella terna della zampa, posa di riferimento).
Le fughe d'ombra (larghe 0,5-1 mm) sono disegnate con il loro fondo in un colore d'ombra, perche' il render
non calcola ombre portate: senza, una fuga larga 1 px sparirebbe.
"""
import math
import os
import sys

import numpy as np
from matplotlib.path import Path
from scipy.spatial import ConvexHull, Delaunay, cKDTree

sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica')
import render as R  # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(QUI, 'pannelli')

# ----------------------------------------------------------------------------------- colori del concept
NERO = '#27292c'        # PETG-CF nero naturale: struttura del corpo e delle zampe
SERVO = '#18181b'       # servo MG996R, squadrette, cuscinetti, perni
ANTRACITE = '#454c53'   # PETG tipo RAL 7016: carapace (spina, bordo, frontale, gonne, guance), sportelli
GRIGIO = '#c9cdca'      # PETG tipo RAL 7035: lamine delle spalle e cover di zampa
ARANCIO = '#f04e14'     # PETG tipo RAL 2004: anello dell'occhio e del pulsante
OMBRA = '#0e0f11'       # fondo delle fughe d'ombra
DISPLAY = '#d6242b'     # display rosso del cicalino
METALLO = '#a5a9ad'     # testa del pulsante da pannello
VITE = '#1c1d1f'        # teste delle viti (acciaio brunito)
INTERNI = '#4e545b'
CICALINO = '#1f2023'


# ----------------------------------------------------------------------------------- geometria 2D
def _area2(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))


def _cr(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _in_tri(p, a, b, c, eps=1e-9):
    return _cr(a, b, p) >= -eps and _cr(b, c, p) >= -eps and _cr(c, a, p) >= -eps


def _incrocia(p1, p2, q1, q2):
    d1, d2 = _cr(q1, q2, p1), _cr(q1, q2, p2)
    d3, d4 = _cr(p1, p2, q1), _cr(p1, p2, q2)
    return d1 * d2 < 0 and d3 * d4 < 0


def _in_cono(a0, a, a1, b):
    """b e' dentro l'angolo interno del vertice a (poligono antiorario, a0 precedente, a1 successivo)?"""
    if _cr(a, a1, a0) >= 0:                       # vertice convesso
        return _cr(a, b, a0) > 0 and _cr(b, a, a1) > 0
    return not (_cr(a, b, a1) >= 0 and _cr(b, a, a0) >= 0)


def _ponte(poly, foro, altri):
    """Unisce un foro (orario) al contorno (antiorario) con un ponte verso il vertice visibile piu' vicino."""
    j = max(range(len(foro)), key=lambda k: foro[k][0])
    m = foro[j]
    for i in sorted(range(len(poly)), key=lambda i: (poly[i][0] - m[0]) ** 2 + (poly[i][1] - m[1]) ** 2):
        p = poly[i]
        if not _in_cono(poly[i - 1], p, poly[(i + 1) % len(poly)], m):
            continue
        libero = True
        for anello in [poly, foro] + altri:
            n = len(anello)
            if any(_incrocia(m, p, anello[k], anello[(k + 1) % n]) for k in range(n)):
                libero = False
                break
        if libero:
            return poly[:i + 1] + foro[j:] + foro[:j + 1] + poly[i:]
    raise RuntimeError('nessun ponte per il foro in %s' % (m,))


def antiorario(p):
    p = [tuple(map(float, q)) for q in p]
    return p if _area2(p) > 0 else p[::-1]


def triangola(contorno, fori=()):
    """Triangolazione a orecchie di un poligono semplice con fori (contorno e fori in qualunque verso)."""
    poly = antiorario(contorno)
    hs = [antiorario(h)[::-1] for h in fori]
    hs.sort(key=lambda h: -max(q[0] for q in h))
    for k, h in enumerate(hs):
        poly = _ponte(poly, h, hs[k + 1:])
    idx = list(range(len(poly)))
    tris = []
    while len(idx) > 3:
        n = len(idx)
        preso = False
        for k in range(n):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % n]
            a, b, c = poly[i0], poly[i1], poly[i2]
            if _cr(a, b, c) <= 1e-10:
                continue
            if any(_in_tri(poly[m], a, b, c) for m in idx
                   if m not in (i0, i1, i2) and poly[m] not in (a, b, c)):
                continue
            tris.append((a, b, c))
            idx.pop(k)
            preso = True
            break
        if not preso:          # restano solo vertici allineati: si toglie quello piu' piatto
            k = min(range(n), key=lambda k: abs(_cr(poly[idx[k - 1]], poly[idx[k]], poly[idx[(k + 1) % n]])))
            idx.pop(k)
    tris.append(tuple(poly[i] for i in idx))
    return tris


def _campiona(anello, passo):
    out = []
    n = len(anello)
    for k in range(n):
        a, b = anello[k], anello[(k + 1) % n]
        m = max(1, int(math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / passo)))
        out += [(a[0] + (b[0] - a[0]) * j / m, a[1] + (b[1] - a[1]) * j / m) for j in range(m)]
    return out


def triangola_fine(contorno, fori=(), passo=7.5, bordo=0.8):
    """Triangoli quasi equilateri (reticolo interno + bordo fitto, Delaunay filtrato): sulle facce grandi evita i
    ventagli di triangoli lunghi, che nel render a pittore lasciano righe chiare sulle superfici piane."""
    anelli = [antiorario(contorno)] + [antiorario(h) for h in fori]
    bordo_pt = np.array(sum((_campiona(a, bordo) for a in anelli), []))
    out_p, fori_p = Path(np.array(anelli[0])), [Path(np.array(h)) for h in anelli[1:]]
    lo, hi = np.array(anelli[0]).min(0), np.array(anelli[0]).max(0)
    gy = np.arange(lo[1], hi[1], passo * 0.866)
    griglia = np.array([(x + (passo / 2 if i % 2 else 0), y) for i, y in enumerate(gy) for x in np.arange(lo[0], hi[0], passo)])

    def dentro(q):
        ok = out_p.contains_points(q)
        for h in fori_p:
            ok &= ~h.contains_points(q)
        return ok
    if len(griglia):
        griglia = griglia[dentro(griglia)]
    if len(griglia):
        griglia = griglia[cKDTree(bordo_pt).query(griglia)[0] > 0.5 * passo]
    pts = np.vstack([bordo_pt, griglia]) if len(griglia) else bordo_pt
    tri = pts[Delaunay(pts).simplices]
    tri = tri[dentro(tri.mean(1))]
    return [tuple(map(tuple, t)) for t in tri]


def rientro(p, d):
    """Contorno antiorario spostato verso l'interno di d[k] lungo ogni lato k (lato k: p[k] -> p[k+1])."""
    n = len(p)
    linee = []
    for k in range(n):
        a, b = p[k], p[(k + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        lg = math.hypot(dx, dy)
        u = (dx / lg, dy / lg)
        linee.append(((a[0] - u[1] * d[k], a[1] + u[0] * d[k]), u))
    out = []
    for k in range(n):
        (p1, u1), (p2, u2) = linee[k - 1], linee[k]
        den = u1[0] * u2[1] - u1[1] * u2[0]
        if abs(den) < 1e-9:
            out.append(p2)
        else:
            t = ((p2[0] - p1[0]) * u2[1] - (p2[1] - p1[1]) * u2[0]) / den
            out.append((p1[0] + u1[0] * t, p1[1] + u1[1] * t))
    return out


def cerchio(c, r, n=32):
    return [(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def ottagono(c, a, b, t):
    """Ottagono di semiassi a, b con angoli tagliati a 45 gradi di cateto t, centrato in c."""
    x, y = c
    return [(x + a, y - b + t), (x + a, y + b - t), (x + a - t, y + b), (x - a + t, y + b),
            (x - a, y + b - t), (x - a, y - b + t), (x - a + t, y - b), (x + a - t, y - b)]


def rett(u0, v0, u1, v1):
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


# ----------------------------------------------------------------------------------- solidi
def _assi(tri, asse):
    tri = np.asarray(tri, dtype=float)
    if asse == 'x':
        return tri[:, :, [2, 0, 1]]
    if asse == 'y':
        return tri[:, :, [0, 2, 1]]
    return tri


def lastra(contorno, w0, w1, fori=(), smusso=0.0, lati=None, pareti=None, cap0=True, cap1=True, asse='z'):
    """Lastra dal poligono (u, v) estrusa da w0 a w1 lungo l'asse dato, con fori e smusso a 45 gradi sul bordo della
    faccia w1 (solo sui lati indicati in `lati`). Ritorna i triangoli nella terna (x, y, z).
    Asse 'z': (u, v) = (x, y); 'x': (u, v) = (y, z); 'y': (u, v) = (x, z)."""
    p = [tuple(map(float, q)) for q in contorno]
    n = len(p)
    lati = list(lati) if lati is not None else [True] * n
    pareti = list(pareti) if pareti is not None else [True] * n
    if _area2(p) < 0:                         # il lato k del contorno rovesciato e' il lato n-2-k dell'originale
        p = p[::-1]
        lati = [lati[(n - 2 - i) % n] for i in range(n)]
        pareti = [pareti[(n - 2 - i) % n] for i in range(n)]
    s = smusso
    sopra = rientro(p, [s if lati[k] else 0.0 for k in range(n)]) if s > 0 else p
    verso = 1.0 if w1 > w0 else -1.0
    wm = w1 - verso * s
    tri = []
    grande = abs(_area2(p)) / 2 > 300.0
    tri_f = triangola_fine if grande else triangola
    if cap0:
        tri += [[(a[0], a[1], w0), (b[0], b[1], w0), (c[0], c[1], w0)] for a, b, c in tri_f(p, fori)]
    if cap1:
        tri += [[(a[0], a[1], w1), (b[0], b[1], w1), (c[0], c[1], w1)] for a, b, c in tri_f(sopra, fori)]
    for k in range(n):
        if not pareti[k]:
            continue
        a, b = p[k], p[(k + 1) % n]
        ta, tb = sopra[k], sopra[(k + 1) % n]
        tri += [[(a[0], a[1], w0), (b[0], b[1], w0), (b[0], b[1], wm)], [(a[0], a[1], w0), (b[0], b[1], wm), (a[0], a[1], wm)]]
        if s > 0:
            tri += [[(a[0], a[1], wm), (b[0], b[1], wm), (tb[0], tb[1], w1)], [(a[0], a[1], wm), (tb[0], tb[1], w1), (ta[0], ta[1], w1)]]
    for h in fori:
        m = len(h)
        for k in range(m):
            a, b = h[k], h[(k + 1) % m]
            tri += [[(a[0], a[1], w0), (b[0], b[1], w0), (b[0], b[1], w1)], [(a[0], a[1], w0), (b[0], b[1], w1), (a[0], a[1], w1)]]
    return _assi(tri, asse)


def quad(p0, p1, p2, p3):
    return np.array([[p0, p1, p2], [p0, p2, p3]], dtype=float)


def scatola(x0, y0, z0, x1, y1, z1):
    return lastra(rett(x0, y0, x1, y1), z0, z1)


# ----------------------------------------------------------------------------------- scena
class Concept:
    def __init__(self):
        self.s = R.Scena()
        self.n = 0

    def add(self, tri, colore, **kw):
        tri = np.asarray(tri, dtype=float)
        self.n += len(tri)
        self.s._aggiungi(tri, colore, **kw)


def modello_attuale(c):
    s = c.s
    s.nascondi('coperchio')                       # coperchio, muso e sportellino di oggi: sostituiti dal carapace
    s.colore('base', NERO)
    s.colore('zampe_struttura', NERO)
    s.colore('servo_coxa', SERVO)
    s.colore('zampe_servo', SERVO)
    s.colore('interni', INTERNI)
    # lo sportello della batteria esce dal gruppo "base": nel concept e' antracite e smussato (lo si ridisegna)
    t = s.gruppi['base']['tri']
    x, y, z = t[:, :, 0], t[:, :, 1], t[:, :, 2]
    sportello = (x.max(1) <= -85.35) & (x.min(1) >= -87.45) & (np.abs(y).max(1) <= 32.5) & (z.max(1) <= -9.3)
    s.gruppi['base']['tri'] = t[~sportello]
    # facce nascoste sotto le cover, vicine alla loro faccia in vista: nel render a pittore i loro triangoli grandi
    # passerebbero sopra le cover. Fondo delle tasche delle culle (Y -21,35), 1,6 mm dietro gli inserti dei fondi:
    t = s.gruppi['zampe_struttura']['tri']
    tasca = np.zeros(len(t), bool)
    for nome in R.COXE:
        inv = np.linalg.inv(R.terna_zampa(nome))
        loc = t @ inv[:3, :3].T + inv[:3, 3]
        for xc in (55.0, 120.0):
            tasca |= ((np.abs(loc[:, :, 1] + 21.35) < 0.02).all(1) & (np.abs(loc[:, :, 0] - xc) <= 10.5).all(1)
                      & (loc[:, :, 2] >= -31.0).all(1) & (loc[:, :, 2] <= -7.9).all(1))
        # parete esterna della culla della tibia con le sue finestre, dietro la lama dello stinco (1,7 mm piu' indietro)
        tasca |= ((loc[:, :, 0] >= 130.4).all(1) & (loc[:, :, 0] <= 132.5).all(1) & (loc[:, :, 1] >= -24.2).all(1)
                  & (loc[:, :, 1] <= 9.5).all(1) & (loc[:, :, 2] >= -33.0).all(1) & (loc[:, :, 2] <= 8.0).all(1))
    s.gruppi['zampe_struttura']['tri'] = t[~tasca]
    return int(sportello.sum()), int(tasca.sum())


# ----------------------------------------------------------------------------------- carapace
SEMI = [(101, 27), (112.73, 47.31), (99.23, 70.69), (73.78, 56), (26.20, 56), (13.5, 78), (-13.5, 78), (-26.20, 56),
        (-73.78, 56), (-99.23, 70.69), (-112.73, 47.31), (-101, 27)]
CONTORNO = SEMI + [(x, -y) for x, y in reversed(SEMI)]          # 24 vertici, antiorario visto dall'alto
Z_BORDO, Z_PELLE, Z_TOP = 28.4, 31.8, 33.0
SM = 1.2                                                         # smusso del guscio
FUGA = 0.5                                                       # semilarghezza delle fughe sul dorso (1,0 x 0,5)
X_FER = [18 + i * (43.18 - 14) / 4 for i in range(5)]            # feritoie: _x_feritoia di corpo.py
VITI = [(40, 22.5), (40, -22.5), (-56, 22.5), (-56, -22.5)]
PULS = (-52.0, 39.0)


def carapace(c):
    # bordo verticale 1,2 da z 28,4 alla pelle, su tutto il contorno tranne il fronte (lo fa il frontale con la visiera)
    fronte = [abs(a[0] - 101) < 1e-6 and abs(b[0] - 101) < 1e-6 for a, b in zip(CONTORNO, CONTORNO[1:] + CONTORNO[:1])]
    c.add(lastra(CONTORNO, Z_BORDO, Z_PELLE, pareti=[not f for f in fronte], cap0=False, cap1=False), ANTRACITE)

    # spina antracite |y| <= 27 (meno la fuga), smussata davanti e dietro; aperture: sportellino, cicalino, lamature
    fori = [rett(-20, -17, 28, 17), rett(-79.5, -12, -69.5, 12)] + [cerchio(v, 3.25, 24) for v in VITI]
    c.add(lastra(rett(-101, -(27 - FUGA), 101, 27 - FUGA), Z_PELLE, Z_TOP, fori=fori, smusso=SM,
                 lati=[False, True, False, True], cap0=False), ANTRACITE)
    # fondo delle due fughe tra spina e spalle (1,0 x 0,5), con le estremita' sullo smusso
    for sy in (1, -1):
        pts = [(sx * xx, sy * yy, zz) for sx in (1, -1) for yy in (27 - FUGA, 27 + FUGA)
               for xx, zz in ((101, Z_PELLE), (101 - (Z_TOP - FUGA - Z_PELLE), Z_TOP - FUGA))]
        pts = np.asarray(pts, dtype=float)
        c.add(pts[ConvexHull(pts).simplices], OMBRA)

    # lamine grigie delle spalle (pelle fuori dalla spina, compreso lo smusso del bordo)
    x_inizio = 101 + (27 + FUGA - 27) * 11.73 / 20.31
    spalla = [(-x_inizio, 27 + FUGA), (x_inizio, 27 + FUGA)] + SEMI[1:-1]
    lati = [False] + [True] * (len(spalla) - 1)
    feritoie = [rett(x0, 28.5, x0 + 6, 31.5) for x0 in X_FER]
    sin = lastra(spalla, Z_PELLE, Z_TOP, fori=feritoie + [cerchio(PULS, 10.0, 40)], smusso=SM, lati=lati, cap0=False)
    c.add(sin, GRIGIO)
    des = lastra(spalla, Z_PELLE, Z_TOP, fori=feritoie, smusso=SM, lati=lati, cap0=False)
    des[:, :, 1] *= -1
    c.add(des, GRIGIO)

    # pulsante sulla spalla posteriore sinistra: anello arancio a filo, sotto la pelle grigia, testa del pulsante
    c.add(lastra(cerchio(PULS, 10.0, 40), Z_TOP - 0.6, Z_TOP, fori=[cerchio(PULS, 6.1, 32)], cap0=False), ARANCIO)
    c.add(lastra(cerchio(PULS, 10.0, 40), Z_PELLE, Z_TOP - 0.6, fori=[cerchio(PULS, 6.1, 32)], cap1=False), GRIGIO)
    c.add(lastra(cerchio(PULS, 8.0, 40), Z_TOP, Z_TOP + 2.0), METALLO)
    c.add(lastra(cerchio(PULS, 6.0, 32), Z_TOP - 18.0, Z_TOP, cap1=False), METALLO)

    # sportellino a filo con la fuga di 0,5 e la tacca per l'unghia nella fuga anteriore
    sport = [(-19.5, -16.5), (27.5, -16.5), (27.5, -5), (24.5, -5), (24.5, 5), (27.5, 5), (27.5, 16.5), (-19.5, 16.5)]
    c.add(lastra(sport, Z_PELLE, Z_TOP, cap0=False), ANTRACITE)
    for q in (rett(-20, -17, -19.5, 17), rett(27.5, -17, 28, 17), rett(-19.5, 16.5, 27.5, 17), rett(-19.5, -17, 27.5, -16.5),
              rett(24.5, -5, 27.5, 5)):
        c.add(lastra(q, Z_PELLE - 0.2, Z_PELLE, cap0=False), OMBRA)

    # viti del guscio a filo nelle lamature (teste M3 D5,5)
    for v in VITI:
        c.add(lastra(cerchio(v, 2.75, 20), Z_TOP - 3.0, Z_TOP, cap0=False), VITE)

    # culla del cicalino appesa alla pelle e cicalino con il display sotto la finestra
    c.add(scatola(-87.4, 20.2, 23.8, -60.8, 21.4, Z_PELLE), ANTRACITE, specchia_y=True)
    c.add(scatola(-62.0, -21.4, 23.8, -60.8, 21.4, Z_PELLE), ANTRACITE)
    c.add(scatola(-87.0, -20.0, 20.8, -62.0, 20.0, 31.0), CICALINO)
    c.add(scatola(-79.0, -11.5, 31.0, -70.0, 11.5, Z_PELLE), DISPLAY)

    # gonne laterali (a 6 mm dentro il bordo delle baie, da z 7 alla pelle)
    for sx in (1, -1):
        x0, x1 = sorted((sx * 22.0, sx * 58.8))
        c.add(scatola(x0, 48.8, 7.0, x1, 50.0, Z_PELLE), ANTRACITE, specchia_y=True)


def frontale(c):
    """Frontale con visiera, occhio ottagonale e anello arancio; fianchi del muso; paraluce. Lastre lungo X, (u, v) = (y, z)."""
    # parete alta (sopra la cintura) con la visiera: smussi sugli spigoli verticali
    c.add(lastra(rett(-27, 7.0 + 0.5, 27, Z_PELLE), 99.4, 101.0, fori=[rett(-24, 15.0, 24, 30.6)], smusso=SM,
                 lati=[False, True, False, True], asse='x'), ANTRACITE)
    # parete bassa sotto la cintura: smussi sugli spigoli verticali e sul bordo basso
    c.add(lastra(rett(-27, -1.0, 27, 7.0 - 0.5), 99.4, 101.0, smusso=SM, lati=[True, True, False, True], asse='x'), ANTRACITE)
    # fondo della fuga di cintura (1 x 0,5 a z 7)
    yf = 27 - (101.0 - 100.5)
    c.add(quad((100.5, -yf, 6.5), (100.5, yf, 6.5), (100.5, yf, 7.5), (100.5, -yf, 7.5)), OMBRA)
    # fondo della visiera (0,8 dentro) con la sede ottagonale dell'anello
    # l'ottagono esterno dell'anello (16,4 x 15,4 su z 22,5) scende a z 14,8, cioe' 0,2 sotto il fondo della visiera
    # (z 15): sotto z 15 l'anello e' dentro la parete, quindi lo si disegna tagliato a z 15
    occhio = ottagono((0, 22.5), 7.0, 6.5, 2.5)
    anello = [(5.2, 15.0), (8.2, 18.0), (8.2, 27.0), (5.0, 30.2), (-5.0, 30.2), (-8.2, 27.0), (-8.2, 18.0), (-5.2, 15.0)]
    fondo_vis = [(-24, 15.0)] + anello[::-1] + [(24, 15.0), (24, 30.6), (-24, 30.6)]
    c.add(lastra(fondo_vis, 99.4, 100.2, cap0=False, pareti=[False] * len(fondo_vis), asse='x'), ANTRACITE)
    c.add(lastra(anello, 99.4, 100.2, fori=[occhio], asse='x'), ARANCIO)
    # fianchi del muso
    c.add(scatola(81.5, 25.4, -1.0, 99.4, 27.0, Z_PELLE), ANTRACITE, specchia_y=True)
    # paraluce dietro il frontale, ai lati della testa della camera
    c.add(scatola(96.0, 5.5, 19.0, 99.4, 6.7, Z_PELLE), ANTRACITE, specchia_y=True)


def coda(c):
    """Guance di coda con la fuga di cintura e sportello della batteria antracite smussato."""
    for sy in (1, -1):
        c.add(scatola(-101.0, sy * 25.4, -8.4, -87.6, sy * 27.0, 6.5), ANTRACITE)
        c.add(scatola(-101.0, sy * 25.4, 7.5, -87.6, sy * 27.0, Z_PELLE), ANTRACITE)
        c.add(scatola(-100.5, sy * 25.4, 6.5, -87.6, sy * 26.5, 7.5), OMBRA)
    # sportello della batteria (D-054): piastra a T con le orecchie delle viti, smusso 1,2 sugli spigoli esterni
    t = [(-31.7, -41.4), (31.7, -41.4), (31.7, -31.95), (27, -31.95), (27, -9.4), (-27, -9.4), (-27, -31.95), (-31.7, -31.95)]
    fori = [cerchio((sy * 28.5, -36.7), 1.7, 16) for sy in (1, -1)]
    c.add(lastra(t, -85.4, -87.4, fori=fori, smusso=SM, asse='x'), ANTRACITE)
    for sy in (1, -1):
        c.add(lastra(cerchio((sy * 28.5, -36.7), 2.75, 20), -87.4, -90.4, asse='x'), VITE)


# ----------------------------------------------------------------------------------- cover delle zampe (terna della zampa)
def cappuccio(xc):
    contorno = [(xc - 8.2, -37.55), (xc + 8.2, -37.55), (xc + 8.2, -32.95), (xc + 11.65, -29.5), (xc + 11.65, 9.0),
                (xc + 8.2, 12.45), (xc + 8.2, 17.25), (xc - 8.2, 17.25), (xc - 8.2, 12.45), (xc - 11.65, 9.0),
                (xc - 11.65, -29.5), (xc - 8.2, -32.95)]
    tri = [lastra(contorno, 22.0, 23.2, fori=[cerchio((xc, 0.0), 6.0, 32)], smusso=0.6, asse='y')]
    for sx in (1, -1):
        x0, x1 = sorted((xc + sx * 10.45, xc + sx * 11.65))
        tri.append(lastra(rett(x0, -29.5, x1, 9.0), 10.0, 22.0, asse='y'))
    return np.concatenate(tri)


def fondo(xc):
    return lastra(rett(xc - 10.25, -30.75, xc + 10.25, -8.2), -21.35, -22.95, asse='y')


def tegola():
    fori = [cerchio((91.0, sy * 16.0), 2.1, 20) for sy in (1, -1)]
    tri = [lastra(rett(83.0, -27.0, 99.0, 27.0), 22.0, 23.2, fori=fori, smusso=0.6)]
    for sy in (1, -1):
        tri.append(lastra(cerchio((91.0, sy * 16.0), 3.0, 24), 20.0, 22.0, cap1=False))
    return np.concatenate(tri)


def viti_tegola():
    return np.concatenate([lastra(cerchio((91.0, sy * 16.0), 1.9, 20), 21.2, 23.2, cap0=False) for sy in (1, -1)])


def lama():
    """Lama dello stinco: (u, v) = (Y, Z_t), lastra lungo X da 132,95 a 134,15, fuga 0,8 x 0,4 lungo Y 0."""
    contorno = [(-24.15, 8.0), (-24.15, -36.0), (-9.45, -50.7), (-9.45, -87.0), (-6.45, -90.0), (6.45, -90.0),
                (9.45, -87.0), (9.45, 8.0), (5.45, 12.0), (-20.15, 12.0)]
    fuga = rett(-0.4, -88.0, 0.4, -40.0)
    tri = [lastra(contorno, 132.95, 133.75, fori=[fuga], cap1=True, asse='x'),
           lastra(contorno, 133.75, 134.15, fori=[fuga], smusso=0.6, cap0=False, asse='x')]
    grigio = np.concatenate(tri)
    # braccetti dell'aggancio a scatto ai lati dello stinco
    br = np.concatenate([lastra(rett(119.0, sy * 9.65, 132.95, sy * 10.85), -91.0, -83.0) for sy in (1, -1)])
    return np.concatenate([grigio, br]), lastra(fuga, 132.95, 133.75, asse='x')


def rombi_chiusi(x0, x1):
    d = 6 * math.sqrt(2)
    return np.concatenate([lastra([(-5 + d, zc), (-5, zc + d), (-5 - d, zc), (-5, zc - d)], x0, x1, asse='x')
                           for zc in (-1.0, -20.5)])


def zampe(c):
    for xc in (55.0, 120.0):
        c.add(cappuccio(xc), GRIGIO, zampe=True)
        c.add(fondo(xc), GRIGIO, zampe=True)
    c.add(tegola(), GRIGIO, zampe=True)
    c.add(viti_tegola(), VITE, zampe=True)
    grigio, fuga = lama()
    c.add(grigio, GRIGIO, zampe=True)
    c.add(fuga, OMBRA, zampe=True)
    c.s.cilindro((0.0, -56.0), 3.0, 126.1, 132.95, GRIGIO, n=24, asse='x', zampe=True)    # distanziale della lama
    # finestre a rombo chiuse: parete esterna della culla della coxa, parete interna della culla della tibia
    c.add(rombi_chiusi(65.45, 67.45), NERO, zampe=True)
    c.add(rombi_chiusi(107.55, 109.55), NERO, zampe=True)


# ----------------------------------------------------------------------------------- main
R.VISTE.update({'fronte': (6, 0, 1.5), 'muso': (12, 28, 3.6), 'coda': (16, 208, 3.4), 'zampa_b': (12, -35, 3.0)})


def costruisci():
    c = Concept()
    tolti = modello_attuale(c)
    carapace(c)
    frontale(c)
    coda(c)
    zampe(c)
    print('tolti dal modello: %d triangoli dello sportello, %d delle facce nascoste sotto inserti e lama; triangoli nuovi (prima della suddivisione): %d' % (tolti + (c.n,)))
    return c


if __name__ == '__main__':
    scelte = sys.argv[1:]
    c = costruisci()
    s = c.s
    gruppi = [
        (('iso_ant', 'iso_post', 'fianco', 'alto'), {}),
        (('zampa',), {'centro': (150, 85, -20)}),
        (('fronte',), {}),
        (('muso',), {'centro': (88, 0, 14), 'larghezza': 1300, 'altezza': 1300}),
        (('coda',), {'centro': (-92, 0, 4), 'larghezza': 1300, 'altezza': 1300}),
        (('zampa_b',), {'centro': (150, 85, -25), 'larghezza': 1300, 'altezza': 1300}),
    ]
    for viste, kw in gruppi:
        viste = tuple(v for v in viste if not scelte or v in scelte)
        if viste:
            print(s.render(OUT, viste=viste, titolo='Lamina', **kw))
