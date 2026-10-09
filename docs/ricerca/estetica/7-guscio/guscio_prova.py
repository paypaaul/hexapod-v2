"""Prova: placche a guscio (bombate in due direzioni) e tibia a corno (rastremata in X e in Y), dai disegni dell'utente."""
import math
import os
import sys

import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import scena as SC  # noqa: E402
import varianti as VR  # noqa: E402
from render import Scena, terna_piano  # noqa: E402
import geo  # noqa: E402

B, AN, AR = SC.BIANCO, SC.ANTRACITE, SC.ARANCIO
v = VR.piena(passo=1.3)


def corno(n_z=70, n_t=56, esp=3.0):
    """Stinco a corno nella terna della zampa: sezioni a superellisse da Z -38,35 alla punta Z -110."""
    z0, zr, zt = -38.35, -105.0, -110.0
    sezioni, colori = [], []
    zs = list(np.linspace(z0, zr, n_z)) + list(zr - 5 * np.sin(np.linspace(0, math.pi / 2, 10))[1:])
    for z in zs:
        t = max(0.0, (z - zr) / (z0 - zr))
        f = 1.0 if z >= zr else math.sqrt(max(1 - ((zr - z) / 5.0) ** 2, 0.0))
        xmin = 120 - (4 + 2 * t)
        xmax = 120 + 4 + 8.45 * t ** 1.6
        ymax = 4 + 5.45 * t ** 1.8
        ymin = -4 - 20.15 * t ** 2.4
        xc, ax = (xmin + xmax) / 2, (xmax - xmin) / 2 * f
        yc, ay = (ymin + ymax) / 2, (ymax - ymin) / 2 * f
        th = np.linspace(0, 2 * math.pi, n_t, endpoint=False)
        c, s = np.cos(th), np.sin(th)
        x = xc + ax * np.sign(c) * np.abs(c) ** (2 / esp)
        y = yc + ay * np.sign(s) * np.abs(s) ** (2 / esp)
        sezioni.append(np.c_[x, y, np.full(n_t, z)])
    tri_n, tri_a = [], []
    for k in range(len(sezioni) - 1):
        a, b = sezioni[k], sezioni[k + 1]
        dest = tri_a if sezioni[k][0, 2] < -94 else tri_n
        for i in range(n_t):
            j = (i + 1) % n_t
            dest += [[a[i], a[j], b[j]], [a[i], b[j], b[i]]]
    return np.array(tri_n), np.array(tri_a)


def scudo():
    """Ginocchiera a guscio dal disegno: larga in alto, fianchi che convergono appena, fondo a U."""
    pts = [(-24.15, 13.65), (9.45, 13.65), (8.6, -6.0)]
    for a in np.linspace(0, math.pi, 25)[1:-1]:
        pts.append((-7.35 + 15.9 * math.cos(a), -6.0 - 24.0 * math.sin(a)))
    pts.append((-23.3, -6.0))
    return pts


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
# lame a guscio: base sulla piastra, colmo a 3,0 (a filo delle teste: la zampa non si allarga), bordi che tornano giu'
sedi = [geo.cerchio(c, VR.SEDE_R, 36) for c in VR.VITI_BLOCCO]
cont_A = [(x, -z) for x, z in v.contorno]
fori_A = [[(x, -z) for x, z in f] for f in v.finestre + sedi]
s.piastra(cont_A, terna_piano((0, VR.Y_FA, 0), (1, 0, 0), (0, 0, -1)), 1.0, B, bombatura=2.0, raggio_bordo=2.5, fori=fori_A, zampe=True)
s.piastra(v.contorno, terna_piano((0, VR.Y_FB, 0), (1, 0, 0), (0, 0, 1)), 1.0, B, bombatura=2.0, raggio_bordo=2.5, fori=v.finestre, zampe=True)
for c in VR.VITI_BLOCCO:                                    # teste delle viti del blocco
    s.cilindro((c[0], c[1]), 2.75, VR.Y_FA, VR.Y_TESTE, SC.INOX, asse='y', zampe=True)
# ginocchiera a guscio: colmo 6,9 mm fuori dalla culla
s.piastra(scudo(), terna_piano((VR.X_CULLA, 0, 0), (0, 1, 0), (0, 0, 1)), 1.4, B, bombatura=5.5, raggio_bordo=2.0, zampe=True)
tn, ta = corno()
s._aggiungi(tn, AN, zampe=True)
s._aggiungi(ta, AR, zampe=True)
base = os.path.join(QUI, 'guscio_prova')
for vv in ('zampa', 'punta', 'iso_ant'):
    if vv in SC.EXTRA:
        print(s.render(base, viste=(vv,), centro=SC.EXTRA[vv][1], titolo='Prova: placche a guscio, tibia a corno', lato=5.0))
    else:
        print(s.render(base, viste=(vv,), titolo='Prova: placche a guscio, tibia a corno', lato=5.0))
