"""Prova del metodo (piano del PCB, 5.2), passi 2 e 3: PCB della scheda di prova da script.

Gira con il Python di KiCad:
  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 genera_pcb.py
Con --guasto toglie una pista apposta: il DRC deve trovare la connessione mancante (caso di controllo).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'script'))

from scheda_kicad import Scheda, netlist  # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
L, H = 30.0, 29.0


def scheda(guasto=False, cartella=QUI):
    s = Scheda(netlist(os.path.join(QUI, 'prova.kicad_sch'), os.path.join(cartella, 'prova.net')),
               os.path.join(cartella, 'prova.kicad_pcb'))
    s.contorno([(0, 0), (L, 0), (L, H), (0, H)])
    s.piazza('J1', 5, 5)
    s.piazza('U3', 13, 7.54)
    s.piazza('C1', 24, 3)
    s.piazza('JP1', 9.6, 5.5, 90)
    s.piazza('R1', 16.81, 26, 180)
    s.piazza('TP1', 5, 19)

    s.pista('5V_REG', [('J1', 1), (5, 3), (20.62, 3), ('U3', 14)], 1.5)
    s.pista('5V_REG', [(20.62, 3), ('C1', 1)], 1.5)
    # la pista larga si ferma prima del centro della piazzola: le piazzole del ponticello sono a 1,3
    s.pista('5V_REG', [(9.6, 3), (9.6, 3.9)], 1.5)
    s.pista('IN', [('J1', 3), ('U3', 2)])
    s.pista('OE1', [('JP1', 2), (11, 5.5), ('U3', 1)])
    s.pista('Y1', [('U3', 3), (16.81, 12.62), ('R1', 1)])
    if not guasto:
        s.pista('OUT', [('R1', 2), (5, 24.35), ('TP1', 1), ('J1', 4)])
    s.pista('GND', [('JP1', 1), (9.6, 8.5)])
    s.via('GND', 9.6, 8.5)
    s.pista('GND', [('C1', 2), (26.5, 3)])
    s.via('GND', 26.5, 3)
    s.riempimento('GND', [(0.5, 0.5), (L - 0.5, 0.5), (L - 0.5, H - 0.5), (0.5, H - 0.5)])
    s.testo('HEX2 PROVA r1', 24, 27.5, altezza=0.8)
    return s


if __name__ == '__main__':
    guasto = '--guasto' in sys.argv
    cartella = sys.argv[sys.argv.index('-o') + 1] if '-o' in sys.argv else QUI
    print(scheda(guasto, cartella).salva())
