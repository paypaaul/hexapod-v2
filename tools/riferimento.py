"""Riferimenti in Python per i test del nucleo C++ (firmware/components/nucleo): andatura a tripode e statica.

L'andatura e' cad/script/assieme.py -> pose_tripode riscritta sulla Descrizione, senza Fusion e senza l'arrotondamento a
0,01 gradi: con gli stessi argomenti da' le pose di cad.json -> cicli_verificati entro l'arrotondamento (test in
tests/test_vettori.py). La statica usa calc/statica_tripode.py cosi' com'e'.

Da spostare in tools/descrizione.py quando lo si tocca (file comune): qui per non modificarlo durante S0.
"""
import math
import os
import runpy

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def statica():
    """Le funzioni di calc/statica_tripode.py (carichi_piedi, ik_piano, valuta, margine_stabilita, CONFIG...)."""
    return runpy.run_path(os.path.join(REPO, 'calc', 'statica_tripode.py'))


def fase_zampa(d, zampa, fase):
    """Fase propria della zampa: il primo tripode di robot.yaml e' in appoggio nella prima meta' del ciclo."""
    return fase if zampa in d.yaml['tripodi'][0] else (fase + 0.5) % 1.0


def in_appoggio(d, zampa, fase):
    return fase_zampa(d, zampa, fase) < 0.5


def piede_tripode(d, zampa, h, xf0, passo, alzata, fase, giro=0.0):
    """Punta del piede nella terna del robot alla fase 0..1, come pose_tripode: in appoggio va da +passo/2 a -passo/2
    in linea retta; in volo torna avanti alzandosi di alzata * sin(pi v). Con giro (gradi a passo) il piede si sposta su
    un arco attorno al centro del corpo e il passo non conta, come in pose_tripode."""
    x, y, dd = d.coxe[zampa]
    fx = x + (d.Lc + xf0) * math.cos(math.radians(dd))
    fy = y + (d.Lc + xf0) * math.sin(math.radians(dd))
    u = fase_zampa(d, zampa, fase)
    if u < 0.5:
        k, dz = 0.5 - u / 0.5, 0.0
    else:
        v = (u - 0.5) / 0.5
        k, dz = -0.5 + v, alzata * math.sin(math.pi * v)
    if giro:
        r = math.radians(giro * k)
        fx, fy = fx * math.cos(r) - fy * math.sin(r), fx * math.sin(r) + fy * math.cos(r)
        dx = 0.0
    else:
        dx = passo * k
    return (fx + dx, fy, dz - h)


def pose_tripode(d, h, xf0, passo, alzata, fase, giro=0.0):
    """{zampa: (imbardata, alpha, gamma)} come assieme.py -> pose_tripode, senza arrotondare; None fuori portata."""
    return {n: d.ik_robot(n, piede_tripode(d, n, h, xf0, passo, alzata, fase, giro)) for n in d.zampe}
