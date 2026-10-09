"""Geometria comune delle varianti della tibia (terna della zampa, mm) e verifiche di ingombro sulle mesh del modello.

Terna della zampa come in render.py: X verso l'esterno, Y lungo l'asse del femore (verso Femore_A), Z in alto;
posa di riferimento alpha = 0, gamma = 90. Ginocchio in (120, 0). Lo stinco si descrive con un profilo nel piano X-Z
(semilarghezze a sinistra e a destra dell'asse X = 120 in funzione di z) e con la faccia -Y (la +Y resta sul piano
dell'orlo, Y = 9,45, che in stampa sta sul piatto).
"""
import math
import sys

import numpy as np
from scipy.spatial import cKDTree

sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica')
from render import leggi_stl, terna_zampa, _trasforma  # noqa: E402

MESH = '/Users/paul/.claude/jobs/3d86073b/tmp/estetica/mesh/%s.stl'
XK = 120.0
Z_ZOC = -38.35                 # fondo dello zoccolo (bug_coda): qui comincia lo stinco libero
Y_ORLO, Y_FONDO = 9.45, -24.15
LT = 110.0
CUL_X = (107.55, 132.45)

# minimo del ginocchio in funzione del femore (progetto-meccanico.md, gioco zero)
GMIN = {-45: 54, -40: 55, -35: 45, -30: 46, -25: 46, -20: 46, -15: 45, -10: 44, -5: 43, 0: 43, 5: 41, 10: 39, 15: 39,
        20: 37, 25: 35, 30: 33, 35: 31, 40: 29, 45: 29, 50: 29, 55: 29, 60: 29, 65: 29, 70: 29, 75: 29, 80: 29, 85: 29}


def gamba(nome='AS'):
    """Triangoli della zampa nella sua terna, divisi per parte."""
    M = np.linalg.inv(terna_zampa(nome))
    out = {}
    for g in ('tibia', 'coxa', 'coxa_ponte', 'femore_a', 'femore_b'):
        T = _trasforma(leggi_stl(MESH % ('zampe_struttura_' + g)), M)
        reg = (T[:, :, 0].min(1) > -30) & (T[:, :, 0].max(1) < 220) & (np.abs(T[:, :, 1]).max(1) < 45) & (T[:, :, 2].min(1) > -130)
        out[g] = T[reg]
    T = _trasforma(leggi_stl(MESH % 'zampe_servo'), M)
    reg = (T[:, :, 0].min(1) > -30) & (T[:, :, 0].max(1) < 220) & (np.abs(T[:, :, 1]).max(1) < 45) & (T[:, :, 2].min(1) > -130)
    T = T[reg]
    c = T.mean(1)
    # servo e cuscinetto del ginocchio girano con la tibia; squadretta (Y > 21,5) e perno (vicino all'asse) girano con il
    # femore ma sono assialsimmetrici: si tolgono
    r = np.hypot(c[:, 0] - XK, c[:, 2])
    out['servo_ginocchio'] = T[(c[:, 0] > 95) & (c[:, 1] < 21.5) & (r > 6.5)]
    out['servo_femore'] = T[c[:, 0] <= 95]            # servo del femore e minuteria dell'anca (con la coxa)
    for g in ('base', 'servo_coxa'):
        out[g] = _trasforma(leggi_stl(MESH % g), M)
    return out


def campiona(tri, passo=0.35, seme=1):
    """Punti sulla superficie dei triangoli: spigoli a passo costante e interno a caso con densita' 4 / passo^2."""
    rng = np.random.default_rng(seme)
    pts = [tri.reshape(-1, 3)]
    for k in range(3):
        a, b = tri[:, k], tri[:, (k + 1) % 3]
        n = np.ceil(np.linalg.norm(b - a, axis=1) / passo).astype(int)
        idx = np.repeat(np.arange(len(tri)), n)
        t = (np.arange(n.sum()) - np.repeat(np.cumsum(n) - n, n)) / np.repeat(np.maximum(n, 1), n)
        pts.append(a[idx] + t[:, None] * (b - a)[idx])
    area = np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1) / 2
    n = np.ceil(area * 4 / passo ** 2).astype(int)
    idx = np.repeat(np.arange(len(tri)), n)
    u, v = rng.random(len(idx)), rng.random(len(idx))
    f = u + v > 1
    u[f], v[f] = 1 - u[f], 1 - v[f]
    A, B, C = tri[idx, 0], tri[idx, 1], tri[idx, 2]
    pts.append(A + u[:, None] * (B - A) + v[:, None] * (C - A))
    return np.concatenate(pts)


def rot_xz(P, ang, cx, cz):
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    Q = P.copy()
    x, z = P[:, 0] - cx, P[:, 2] - cz
    Q[:, 0] = cx + c * x - s * z
    Q[:, 2] = cz + s * x + c * z
    return Q


def rot_z(P, ang):
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    Q = P.copy()
    Q[:, 0] = c * P[:, 0] - s * P[:, 1]
    Q[:, 1] = s * P[:, 0] + c * P[:, 1]
    return Q


def posa_tibia(P, alpha, gamma):
    return rot_xz(rot_xz(P, gamma - 90.0, XK, 0.0), alpha, 55.0, 0.0)


def _q(albero, P, limite=8.0):
    """Distanza minima dei punti P dall'albero (oltre `limite` vale `limite`) e indice del punto di P piu' vicino."""
    lo, hi = albero.mins - limite, albero.maxes + limite
    idx = np.nonzero(np.all((P > lo) & (P < hi), axis=1))[0]
    if not len(idx):
        return limite, -1
    d = albero.query(P[idx], distance_upper_bound=limite, workers=-1)[0]
    k = int(np.argmin(d))
    return (float(d[k]), int(idx[k])) if d[k] < limite else (limite, -1)


class Ostacoli:
    """Nuvole di punti delle parti che non girano con la tibia: coxa (ferma), femore (alpha), corpo (imbardata)."""

    def __init__(self, G, passo=0.4):
        self.coxa = campiona(np.concatenate([G['coxa'], G['coxa_ponte'], G['servo_femore']]), passo)
        self.femore = campiona(np.concatenate([G['femore_a'], G['femore_b']]), passo)
        corpo = np.concatenate([G['base'], G['servo_coxa']])
        c = corpo.mean(1)
        corpo = corpo[(c[:, 0] > -60) & (np.abs(c[:, 1]) < 80)]           # solo la parte vicina alla zampa
        self.corpo = campiona(corpo, 0.5)
        self.t_coxa = cKDTree(self.coxa)
        self._fem = {}
        self._corpo = {}

    def distanza(self, P, alpha, imbardate=(0.0,)):
        """Distanza minima dei punti P (gia' in posa) da coxa, femore e corpo; ritorna (d, indice del punto di P, parte)."""
        if alpha not in self._fem:
            self._fem[alpha] = cKDTree(rot_xz(self.femore, alpha, 55.0, 0.0))
        best = [(*_q(self.t_coxa, P), 'coxa'), (*_q(self._fem[alpha], P), 'femore')]
        for psi in imbardate:
            if psi not in self._corpo:
                self._corpo[psi] = cKDTree(rot_z(self.corpo, -psi))
            best.append((*_q(self._corpo[psi], P), 'corpo %+g' % psi))
        return min(best)
