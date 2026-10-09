#!/usr/bin/env python3
"""Render delle varianti della tibia sulla sintesi "Kabuto corretto" (sintesi/concept.py, render.py).

La scena e' quella della sintesi (carapace, testa, coda, lame dei femori, ginocchiera) con i gruppi delle mesh di oggi
(zampe_struttura_<parte>). La tibia di oggi si nasconde: se ne ridisegna la culla (le facce del modello sopra il fondo
dello zoccolo, z -38,35) e si aggiungono lo stinco e il piedino della variante (stinco.py), nella terna della zampa.
"""
import importlib.util
import os
import sys

import numpy as np

sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica')
sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica/v2_tibia')
from render import Scena  # noqa: E402
import stinco as ST  # noqa: E402
from varianti import VARIANTI, Z0  # noqa: E402

_spec = importlib.util.spec_from_file_location('sintesi', '/Users/paul/.claude/jobs/3d86073b/tmp/estetica/sintesi/concept.py')
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
K = C.K

QUI = os.path.dirname(os.path.abspath(__file__))
STRUTTURA = C.ANTRACITE
ARANCIO = C.ARANCIO
# tibia della zampa anteriore sinistra (AS): ginocchio in (183,9; 104; 0) nella terna del robot
CENTRO_TIBIA = (178.0, 100.0, -42.0)
VISTE_DETTAGLIO = {'zampa': (18, 60, 3.3), 'profilo': (8, 125, 3.3)}


def fai_lame(s):
    """Come sintesi/concept.py -> fai_lame, senza la punta arancio (il piedino lo disegna la variante)."""
    kw = dict(zampe=True)
    sag, fin = C.sagoma_lama(), [C.finestra(C.XH), C.finestra(C.XK)]
    sedi = [K.cerchio(c, 2.8, 28, 0.07 * k) for k, c in enumerate(C.VITI_BLOCCO)]
    K.aggiungi(s, K.lastra(sag, fin + sedi, C.YA0, C.YA1, 'y'), C.BIANCO, **kw)
    for c in C.VITI_BLOCCO:
        K.aggiungi(s, K.pareti(K.cerchio(c, 3.8, 28), C.Y_A, C.YA0, 'y'), C.BIANCO, **kw)
    for c in ((C.XH + 15.2, 0.0), (C.XK - 15.2, 0.0)):
        K.aggiungi(s, K.pareti(K.cerchio(c, 1.5, 16), C.Y_A, C.YA0, 'y'), C.BIANCO, **kw)
    K.aggiungi(s, K.lastra(sag, fin, C.YB1, C.YB0, 'y'), C.BIANCO, **kw)
    teste = [(xc + dx, dz) for xc in (C.XH, C.XK) for dx, dz in ((-7, 0), (7, 0), (0, 7), (0, -7))] + C.VITI_BLOCCO
    for c in teste:
        es = K.cerchio(c, 1.45, 6, np.pi / 6)
        K.aggiungi(s, K.faccia(K.cerchio(c, 2.75, 28), [es], C.Y_A + 3.0, 'y'), C.INOX, **kw)
        K.aggiungi(s, K.pareti(K.cerchio(c, 2.75, 28), C.Y_A, C.Y_A + 3.0, 'y'), C.INOX, **kw)
        K.aggiungi(s, K.pareti(es, C.Y_A + 1.8, C.Y_A + 3.0, 'y'), C.OMBRA, **kw)
        K.aggiungi(s, K.faccia(es, [], C.Y_A + 1.8, 'y'), C.OMBRA, **kw)
    m = K.maschera_zampe(s, 'zampe_servo', lambda TL: TL[:, :, 1].max(1) < -30.5)
    K.aggiungi(s, K.estrai(s, 'zampe_servo', m), C.INOX)


def fai_tibia(s, nome):
    """Culla di oggi (sopra lo zoccolo) come gruppo nuovo, poi stinco e piedino della variante."""
    m = K.maschera_zampe(s, 'zampe_struttura_tibia', lambda TL: TL[:, :, 2].min(1) >= Z0 - 0.01)
    s.gruppi['variante_culla'] = {'tri': s.gruppi['zampe_struttura_tibia']['tri'][m], 'colore': STRUTTURA, 'visibile': True}
    s.nascondi('zampe_struttura_tibia')
    tolti = K.togli_coperte(s, 'variante_culla', [(0, 132.45, [C.GIN]), (2, 12.45, [K.rett(130.65, -24.15, 133.65, 9.45)])])
    # fondo dello zoccolo intero (nel modello ha il buco dello stinco di oggi)
    K.aggiungi(s, K.faccia(K.rett(107.55, -24.15, 132.45, 9.45), [], Z0, 'z'), STRUTTURA, zampe=True)
    strutt, piede = ST.mesh(nome)
    K.aggiungi(s, strutt, STRUTTURA, zampe=True)
    K.aggiungi(s, piede, ARANCIO, zampe=True)
    return tolti


def scena(nome):
    s = Scena()
    s.nascondi('coperchio')
    s.colore('base', C.ANTRACITE)
    s.colore('zampe_struttura', C.ANTRACITE)
    s.colore('servo_coxa', C.SERVO)
    s.colore('interni', '#33363b')
    s.colore('zampe_servo', C.SERVO)
    K.togli_coperte(s, 'zampe_struttura_femore_a', [(1, C.Y_A, C.pezzi_coperti())])
    K.togli_coperte(s, 'zampe_struttura_femore_b', [(1, C.Y_B, C.pezzi_coperti())])
    C.fai_carapace(s)
    C.fai_testa(s)
    C.fai_coda(s)
    fai_lame(s)
    C.fai_ginocchiera(s)
    fai_tibia(s, nome)
    return s


def main(nome, argv=()):
    v = VARIANTI[nome]
    s = scena(nome)
    base = os.path.join(QUI, 'tibia_' + v['breve'])
    viste = list(argv) or ['tutte']
    fatti = []
    if 'tutte' in viste or 'robot' in viste:
        fatti += s.render(base, viste=('iso_ant', 'fianco'), titolo=v['titolo'], lato=5.0)
    if 'tutte' in viste or 'zampa' in viste:
        for k, vv in VISTE_DETTAGLIO.items():
            f = s.render(base, viste=(vv,), centro=CENTRO_TIBIA, titolo=v['titolo'], lato=4.0)[0]
            nuovo = '%s_%s.png' % (base, k)
            os.replace(f, nuovo)
            fatti.append(nuovo)
    for f in fatti:
        print(f)
    return fatti
