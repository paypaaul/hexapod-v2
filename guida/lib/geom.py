"""Geometria minima in Python puro (la CI non ha numpy): matrici 3x4 a righe, traslazione in mm."""
import math

IDENTITA = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]


def componi(a, b):
    """a . b: prima b, poi a."""
    out = []
    for r in range(3):
        for c in range(4):
            v = sum(a[4 * r + k] * b[4 * k + c] for k in range(3))
            out.append(v + (a[4 * r + 3] if c == 3 else 0.0))
    return out


def inversa(m):
    """Inversa di una trasformata rigida (rotazione e traslazione)."""
    r = [[m[4 * i + j] for j in range(3)] for i in range(3)]
    t = [m[3], m[7], m[11]]
    out = []
    for i in range(3):
        out += [r[0][i], r[1][i], r[2][i], -(r[0][i] * t[0] + r[1][i] * t[1] + r[2][i] * t[2])]
    return out


def punto(m, p):
    return [m[4 * r] * p[0] + m[4 * r + 1] * p[1] + m[4 * r + 2] * p[2] + m[4 * r + 3] for r in range(3)]


def direzione(m, v):
    return [m[4 * r] * v[0] + m[4 * r + 1] * v[1] + m[4 * r + 2] * v[2] for r in range(3)]


def traslazione(v):
    return [1.0, 0.0, 0.0, v[0], 0.0, 1.0, 0.0, v[1], 0.0, 0.0, 1.0, v[2]]


def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def scala(a, k):
    return [a[0] * k, a[1] * k, a[2] * k]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def norma(a):
    return math.sqrt(dot(a, a))


def unit(a):
    n = norma(a)
    return [a[0] / n, a[1] / n, a[2] / n]


def distanza_retta(p, o, d):
    """Distanza del punto p dalla retta per o con direzione unitaria d."""
    w = sub(p, o)
    return norma(sub(w, scala(d, dot(w, d))))


def base_da_asse(z):
    """Matrice di rotazione 3x4 (senza traslazione) che porta l'asse Z locale su z."""
    z = unit(z)
    t = [1.0, 0.0, 0.0] if abs(z[0]) < 0.9 else [0.0, 1.0, 0.0]
    x = unit(cross(t, z))
    y = cross(z, x)
    return [x[0], y[0], z[0], 0.0, x[1], y[1], z[1], 0.0, x[2], y[2], z[2], 0.0]


def con_origine(m, o):
    out = list(m)
    out[3], out[7], out[11] = o[0], o[1], o[2]
    return out


def rotazione(punto_asse, asse, gradi):
    """Rotazione di 'gradi' attorno alla retta (punto_asse, asse), regola della mano destra."""
    u = unit(asse)
    a = math.radians(gradi)
    c, s_, t = math.cos(a), math.sin(a), 1 - math.cos(a)
    x, y, z = u
    r = [[t * x * x + c, t * x * y - s_ * z, t * x * z + s_ * y],
         [t * x * y + s_ * z, t * y * y + c, t * y * z - s_ * x],
         [t * x * z - s_ * y, t * y * z + s_ * x, t * z * z + c]]
    p = punto_asse
    out = []
    for i in range(3):
        out += [r[i][0], r[i][1], r[i][2], p[i] - (r[i][0] * p[0] + r[i][1] * p[1] + r[i][2] * p[2])]
    return out
