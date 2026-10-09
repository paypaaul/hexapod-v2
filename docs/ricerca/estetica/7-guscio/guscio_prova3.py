"""Prova 3: lame del femore come la Piena; ginocchiera che diventa un guscio lungo sulla tibia (come lo spunto
dell'utente: sporge verso l'esterno, avvolge davanti e sui fianchi, larga in alto, finestra lunga, spigoli tesi);
tibia V2 allargata in alto, sezione squadrata."""
import math
import os
import sys

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import scena as SC  # noqa: E402
import varianti as VR  # noqa: E402
from render import Scena  # noqa: E402

B, AN, AR, NERO = SC.BIANCO, SC.ANTRACITE, SC.ARANCIO, '#151618'
v = VR.piena(passo=1.3)
Z_CUL, Z_TOP, Z_FINE, ZR = -38.35, 13.65, -94.0, -105.0


def stinco(z):
    """Ingombro dello stinco V2 allargato a quota z: (xmin, xmax, ymin, ymax)."""
    t = max(0.0, min(1.0, (z - ZR) / (Z_CUL - ZR)))
    return 120 - (4 + 2 * t), 120 + 4 + 8.45 * (1 - (1 - t) ** 2), -6 - 12.0 * t, 6 + 3.45 * t


def loft(sezioni, chiuso=True):
    tri = []
    for a, b in zip(sezioni[:-1], sezioni[1:]):
        n = len(a)
        for i in range(n if chiuso else n - 1):
            j = (i + 1) % n
            tri += [[a[i], a[j], b[j]], [a[i], b[j], b[i]]]
    return np.array(tri)


def tibia(n_t=64, esp=6.0):
    zs = list(np.linspace(Z_CUL, ZR, 70)) + list(ZR - 5 * np.sin(np.linspace(0, math.pi / 2, 10))[1:])
    sez = []
    for z in zs:
        x0, x1, y0, y1 = stinco(z)
        f = 1.0 if z >= ZR else math.sqrt(max(1 - ((ZR - z) / 5.0) ** 2, 0.0))
        xc, ax, yc, ay = (x0 + x1) / 2, (x1 - x0) / 2 * f, (y0 + y1) / 2, (y1 - y0) / 2 * f
        th = np.linspace(0, 2 * math.pi, n_t, endpoint=False)
        c, s_ = np.cos(th), np.sin(th)
        sez.append(np.c_[xc + ax * np.sign(c) * np.abs(c) ** (2 / esp), yc + ay * np.sign(s_) * np.abs(s_) ** (2 / esp), np.full(n_t, z)])
    tn = loft([q for q in sez if q[0, 2] >= Z_FINE])
    ta = loft([q for q in sez if q[0, 2] <= Z_FINE + 1.0])
    return tn, ta


def _lerp(z, za, va, zb, vb):
    t = min(1.0, max(0.0, (z - za) / (zb - za)))
    t = t * t * (3 - 2 * t)                          # passaggio morbido
    return va + (vb - va) * t


def dims(z, sp=1.6, gio=0.5):
    """Fronte, fianchi e profondita' dei risvolti del guscio a quota z (continui su culla e stinco)."""
    x0, x1, ya, yb = stinco(z) if z < Z_CUL else (114.0, VR.X_CULLA, -24.15, 9.45)
    u = (z - Z_FINE) / (Z_TOP - Z_FINE)
    xf = x1 + 3.2 + 2.6 * math.sin(math.pi * u)                      # sporge verso l'esterno, di piu' a meta'
    y0 = min(-24.15, ya - gio - sp) if z >= -38.35 else ya - gio - sp
    y0 = _lerp(z, -20.0, -24.15, -60.0, ya - gio - sp) if z < -20.0 else -24.15
    giro_p = _lerp(z, -38.35, 0.0, -55.0, 1.0)                       # risvolto +Y solo sotto la culla (sopra c'e' il servo)
    y1 = yb + giro_p * (gio + sp)
    giro_m = _lerp(z, -12.0, 0.0, -20.0, 1.0)                        # risvolto -Y sotto la testa del femore
    xb_m = xf - sp - giro_m * (xf - sp - (x0 + x1) / 2 - 2.0)
    xb_p = xf - sp - giro_p * (xf - sp - (x0 + x1) / 2 - 2.0)
    return xf, y0, y1, xb_m, xb_p


def cover_sezione(z, sp=1.6, c=4.0):
    """Sezione a C sfaccettata: fronte, due smussi a 45 gradi, fianchi fino a xb (anello esterno + interno)."""
    xf, y0, y1, xbm, xbp = dims(z, sp)
    k = sp * math.tan(math.radians(22.5))
    est = [(xbm, y0), (xf - c, y0), (xf, y0 + c), (xf, y1 - c), (xf - c, y1), (xbp, y1)]
    inn = [(xbp, y1 - sp), (xf - c - k, y1 - sp), (xf - sp, y1 - c + k), (xf - sp, y0 + c - k), (xf - c - k, y0 + sp), (xbm, y0 + sp)]
    return [(x, y, z) for x, y in est + inn]


def finestra(z0=-26.0, z1=-82.0, w=3.8):
    """Finestra lunga sul fronte, come lastra scura poco davanti al fronte (si stringe verso il basso)."""
    zs = np.linspace(z0, z1, 50)
    sx, dx = [], []
    for z in zs:
        xf, y0, y1, _, _ = dims(z)
        yc = (y0 + y1) / 2
        hw = w * (0.6 + 0.4 * (z - z1) / (z0 - z1))
        sx.append((xf + 0.06, yc - hw, z)); dx.append((xf + 0.06, yc + hw, z))
    tri = []
    for i in range(len(zs) - 1):
        tri += [[sx[i], dx[i], dx[i + 1]], [sx[i], dx[i + 1], sx[i + 1]]]
    return np.array(tri)


s = Scena()
s.nascondi('coperchio')
s.colore('base', AN); s.colore('zampe_struttura', AN); s.colore('servo_coxa', SC.SERVO)
s.colore('interni', '#33363b'); s.colore('zampe_servo', SC.SERVO)
SC.fai_carapace(s, v.car)
SC.C.fai_testa(s)
SC.C.fai_coda(s)
kw = dict(zampe=True)
SC.togli_sotto(s, 'zampe_struttura', 1, VR.Y_FA, v.contorno, v.finestre, [0, 2])
SC.togli_sotto(s, 'zampe_struttura', 1, VR.Y_FB, v.contorno, v.finestre, [0, 2])
SC.aggiungi(s, SC._lama(v.lama_A, v.y_in_A, 1, fondo=v.tubi), B, **kw)
SC.aggiungi(s, SC._lama(v.lama_B, v.y_in_B, -1, fondo=False), B, **kw)
for c in VR.VITI_BLOCCO:
    s.cilindro((c[0], c[1]), 2.75, VR.Y_FA, VR.Y_TESTE, SC.INOX, asse='y', **kw)
SC.maschera(s, 'zampe_struttura_tibia', lambda TL: TL[:, :, 2].max(1) < -38.3)
tn, ta = tibia()
s._aggiungi(tn, AN, **kw)
s._aggiungi(ta, AR, **kw)
zs = list(np.linspace(Z_TOP, Z_FINE, 90))
anelli = [cover_sezione(z) for z in zs]
# guscio: superfici tra anelli (anello aperto: 12 punti, il lato xb chiude esterno e interno)
s._aggiungi(loft(anelli, chiuso=True), B, **kw)
s.prisma([(p[0], p[1]) for p in anelli[0]], Z_TOP, Z_TOP + 0.01, B, **kw)          # bordo alto
s.prisma([(p[0], p[1]) for p in anelli[-1]], Z_FINE - 0.01, Z_FINE, B, **kw)       # bordo basso
s._aggiungi(finestra(), NERO, **kw)
base = os.path.join(QUI, 'guscio_prova3')
for vv in ('zampa', 'punta', 'iso_ant', 'lato_b'):
    k2 = dict(centro=SC.EXTRA[vv][1]) if vv in SC.EXTRA else {}
    print(s.render(base, viste=(vv,), titolo='Prova 3: guscio lungo sulla tibia', lato=5.0, **k2))
