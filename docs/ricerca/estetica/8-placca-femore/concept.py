"""Concept della placca superiore del femore: tre varianti nel renderer schematico (terna della zampa)."""
import math, sys
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', '..', '..', 'cad', 'render'))
import numpy as np
from render import Scena, terna_piano

BIANCO = '#f2f2f2'
OUT = '/Users/paul/hexapod-v2/docs/ricerca/estetica/8-placca-femore/'
KNEE, HIP = 120.0, 55.0
YB = 33.2                                    # esterno delle lame laterali

def arco(s, cx, r0, r1, t0, t1, y0, y1, n=14):
    """Fascia ad arco attorno all'asse (cx, z 0) parallelo a Y: inviluppo dei punti (solido pieno sotto l'arco)."""
    pts = []
    for k in range(n + 1):
        t = math.radians(t0 + (t1 - t0) * k / n)
        for r in (r0, r1):
            for y in (y0, y1):
                pts.append((cx + r * math.cos(t), y, r * math.sin(t)))
    s.solido(pts, BIANCO, zampe=True)

def ginocchiera(s, fessura=0.0):
    # raggio interno 25: il guscio della tibia, ruotando, arriva a 24 dall'asse del ginocchio
    if fessura:
        arco(s, KNEE, 25.0, 26.6, 52, 120, fessura / 2, YB)
        arco(s, KNEE, 25.0, 26.6, 52, 120, -YB, -fessura / 2)
        arco(s, KNEE, 25.0, 26.6, 52, 82, -fessura / 2 - 0.1, fessura / 2 + 0.1)   # davanti alla fessura e' chiusa
    else:
        arco(s, KNEE, 25.0, 26.6, 52, 120, -YB, YB)

def alette_anca(s):
    # solo fuori dal ponte della coxa (|y| <= 12): il centro resta aperto per ponte e cavi
    arco(s, HIP, 22.6, 24.2, 62, 100, 13.0, YB)
    arco(s, HIP, 22.6, 24.2, 62, 100, -YB, -13.0)

def rett_tondo(x0, x1, y0, y1, r, n=8):
    p = []
    for cx, cy, a0 in ((x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            p.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return p

def dorso(s, foro):
    T = terna_piano((0, 0, 20.2), (1, 0, 0), (0, 1, 0))
    s.piastra(rett_tondo(64.5, 110.5, -YB, YB, 3.0), T, spessore=1.6, colore=BIANCO, bombatura=0.8, raggio_bordo=2.0,
              fori=[foro], zampe=True)

def scena():
    s = Scena()
    s.nascondi('zampe_struttura_cover_tibia_diffusore')
    return s

VARIANTI = {
    '1-finestra-larga': lambda s: (dorso(s, rett_tondo(70, 105, -21, 21, 6)), ginocchiera(s), alette_anca(s)),
    '2-feritoia-tibia': lambda s: (dorso(s, rett_tondo(68, 107, -3.5, 3.5, 3.49)), ginocchiera(s), alette_anca(s)),
    '3-due-cappucci': lambda s: (ginocchiera(s, fessura=9.0), alette_anca(s)),
}
VICINO = [(28, 55, 4.2), (6, 0, 4.2)]                 # zampa media sinistra: dall'esterno-davanti, e di lato
if __name__ == '__main__':
    for nome, f in VARIANTI.items():
        s = scena(); f(s)
        s.render(OUT + nome + '_zampa', viste=VICINO, centro=(0, 136, 0), larghezza=1100, altezza=800)
        s.render(OUT + nome, viste=('iso_ant',), larghezza=1500, altezza=1000)
        print('fatto', nome)
