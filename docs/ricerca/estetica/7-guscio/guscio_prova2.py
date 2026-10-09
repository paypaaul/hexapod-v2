"""Prova 2 (dopo lo spunto dell'utente): placche piu' tese e avvolgenti, tibia V2 allargata anche di lato e bombata."""
import math
import os
import sys

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import scena as SC  # noqa: E402
import varianti as VR  # noqa: E402
import geo  # noqa: E402
from render import Scena, terna_piano  # noqa: E402

B, AN, AR, NERO = SC.BIANCO, SC.ANTRACITE, SC.ARANCIO, SC.NERO
v = VR.piena(passo=1.3)
SP = 1.4


def striscia(poly, verso, y0, y1, col, s, sp=SP):
    """Parete sottile che segue una spezzata (x, z) nella terna della zampa, spostata di sp verso `verso` (+1 in alto),
    estesa in Y da y0 a y1: e' il risvolto della placca sopra o sotto il bordo del femore."""
    p = np.asarray(poly, float)
    for k in range(len(p) - 1):
        a, b = p[k], p[k + 1]
        quad = [(a[0], a[1]), (b[0], b[1]), (b[0], b[1] + verso * sp), (a[0], a[1] + verso * sp)]
        s.prisma(quad, y0, y1, col, asse='y', zampe=True)


def bordo(cont, alto, x0, x1):
    pts = [(x, z) for x, z in cont if x0 <= x <= x1 and ((z > 0) if alto else (z < 0))]
    return sorted(pts)


def tibia_v4(n_z=70, n_t=64, esp=4.0):
    """V2 (fianco esterno ad arco, tangente alla culla) allargata anche lungo Y, sezione a superellisse con facce bombate."""
    z0, zr = -38.35, -105.0
    sez = []
    zs = list(np.linspace(z0, zr, n_z)) + list(zr - 5 * np.sin(np.linspace(0, math.pi / 2, 10))[1:])
    for z in zs:
        t = max(0.0, (z - zr) / (z0 - zr))
        f = 1.0 if z >= zr else math.sqrt(max(1 - ((zr - z) / 5.0) ** 2, 0.0))
        xmin = 120 - (4 + 2 * t)
        xmax = 120 + 4 + 8.45 * (1 - (1 - t) ** 2)
        ymax = 6 + 3.45 * t
        ymin = -6 - 10.0 * t
        xc, ax = (xmin + xmax) / 2, (xmax - xmin) / 2 * f
        yc, ay = (ymin + ymax) / 2, (ymax - ymin) / 2 * f
        th = np.linspace(0, 2 * math.pi, n_t, endpoint=False)
        c, s_ = np.cos(th), np.sin(th)
        sez.append(np.c_[xc + ax * np.sign(c) * np.abs(c) ** (2 / esp), yc + ay * np.sign(s_) * np.abs(s_) ** (2 / esp), np.full(n_t, z)])
    tn, ta = [], []
    for k in range(len(sez) - 1):
        a, b = sez[k], sez[k + 1]
        dest = ta if a[0, 2] < -94 else tn
        for i in range(n_t):
            j = (i + 1) % n_t
            dest += [[a[i], a[j], b[j]], [a[i], b[j], b[i]]]
    return np.array(tn), np.array(ta)


def scudo():
    """Ginocchiera tesa: fianchi dritti fino a Z -12, poi due lati a 60 gradi verso una punta corta, angoli raccordati."""
    p = [(-24.15, 13.65), (9.45, 13.65), (9.45, -12.0), (-4.35, -32.0), (-10.35, -32.0), (-24.15, -12.0)]
    return geo.raccorda(p, [1.5, 1.5, 3.0, 2.5, 2.5, 3.0])


s = Scena()
s.nascondi('coperchio')
s.colore('base', AN); s.colore('zampe_struttura', AN); s.colore('servo_coxa', SC.SERVO)
s.colore('interni', '#33363b'); s.colore('zampe_servo', SC.SERVO)
SC.fai_carapace(s, v.car)
SC.C.fai_testa(s)
SC.C.fai_coda(s)
SC.togli_sotto(s, 'zampe_struttura', 1, VR.Y_FA, v.contorno, v.finestre, [0, 2])
SC.togli_sotto(s, 'zampe_struttura', 1, VR.Y_FB, v.contorno, v.finestre, [0, 2])
SC.maschera(s, 'zampe_struttura_tibia', lambda TL: TL[:, :, 2].max(1) < -38.3)

# lame: faccia esterna appena bombata e spigoli quasi vivi (r 1), colmo a filo delle teste; risvolti sopra e sotto il
# bordo del femore tra le due teste, verso l'interno fino a |Y| 26
sedi = [geo.cerchio(c, VR.SEDE_R, 36) for c in VR.VITI_BLOCCO]
cont_A = [(x, -z) for x, z in v.contorno]
fori_A = [[(x, -z) for x, z in f] for f in v.finestre + sedi]
s.piastra(cont_A, terna_piano((0, VR.Y_FA, 0), (1, 0, 0), (0, 0, -1)), 2.2, B, bombatura=0.8, raggio_bordo=1.0, fori=fori_A, zampe=True)
s.piastra(v.contorno, terna_piano((0, VR.Y_FB, 0), (1, 0, 0), (0, 0, 1)), 2.2, B, bombatura=0.8, raggio_bordo=1.0, fori=v.finestre, zampe=True)
for c in VR.VITI_BLOCCO:
    s.cilindro((c[0], c[1]), 2.75, VR.Y_FA, VR.Y_TESTE, SC.INOX, asse='y', zampe=True)
alto, basso = bordo(v.contorno, True, 66, 110), bordo(v.contorno, False, 66, 110)
for y0, y1 in ((26.0, VR.Y_FA + 1.6), (-(VR.Y_FA + 1.6), -26.0)):
    striscia(alto, 1, y0, y1, B, s)
    striscia(basso, -1, y0, y1, B, s)

# ginocchiera tesa sulla faccia +X della culla, risvolto sul fianco -Y della culla sotto la testa del femore
sc = scudo()
s.piastra(sc, terna_piano((VR.X_CULLA, 0, 0), (0, 1, 0), (0, 0, 1)), 1.6, B, bombatura=1.6, raggio_bordo=0.8, zampe=True)
fianco = [(z, x) for x, z in []]
s.prisma([(126.0, -14.0), (VR.X_CULLA + 1.6, -14.0), (VR.X_CULLA + 1.6, -12.0 - 0.0), (126.0, -12.0)], -25.55, -24.15, B, asse='y', zampe=True) if False else None
lato = [(126.0, -14.0), (VR.X_CULLA + 1.0, -14.0), (VR.X_CULLA + 1.0, -27.0), (128.0, -31.0), (126.0, -31.0)]
s.prisma(lato, -25.55, -24.15, B, asse='y', zampe=True)

tn, ta = tibia_v4()
s._aggiungi(tn, AN, zampe=True)
s._aggiungi(ta, AR, zampe=True)
base = os.path.join(QUI, 'guscio_prova2')
for vv in ('zampa', 'punta', 'iso_ant'):
    kw = dict(centro=SC.EXTRA[vv][1]) if vv in SC.EXTRA else {}
    print(s.render(base, viste=(vv,), titolo='Prova 2: placche tese e avvolgenti, tibia V2 allargata', lato=5.0, **kw))
