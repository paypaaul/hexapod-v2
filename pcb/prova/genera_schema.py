"""Prova del metodo (piano del PCB, 5.2), passo 1: schema della scheda di prova generato da script.

La scheda di prova ha i pezzi che pesano nelle schede vere: un buffer a più unità con l'unità
d'alimentazione, un ponticello a tre piazzole, un reoforo, un 0805, una strip e un punto di prova.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'script'))

from schema_kicad import Schema, scrivi_progetto  # noqa: E402

QUI = os.path.dirname(os.path.abspath(__file__))
LIBRERIE = os.path.join(QUI, '..', 'librerie')


def schema():
    s = Schema('prova', 'HEX2 prova del metodo', cartella_simboli=LIBRERIE)
    s.simbolo('hex2_kicad:Conn_01x04', 'J1', 'Conn_01x04',
              'hex2:PinHeader_1x04_P2.54mm_Vertical', 50.8, 50.8)
    for u, (x, y) in enumerate([(101.6, 50.8), (101.6, 76.2), (101.6, 101.6), (101.6, 127), (152.4, 63.5)], 1):
        s.simbolo('hex2_kicad:74AHCT125', 'U3', 'SN74AHCT125N', 'hex2:DIP-14_W7.62mm', x, y, unita=u)
    s.simbolo('hex2_kicad:R', 'R1', '330', 'hex2:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal', 152.4, 101.6)
    s.simbolo('hex2_kicad:C', 'C1', '100n', 'hex2:C_0805_2012Metric', 190.5, 63.5)
    s.simbolo('hex2_kicad:SolderJumper_3_Bridged12', 'JP1', 'OE',
              'hex2:SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm', 50.8, 101.6)
    s.simbolo('hex2_kicad:TestPoint', 'TP1', 'OUT', 'hex2:TestPoint_THTPad_1.5x1.5mm_Drill0.7mm', 190.5, 101.6)
    s.simbolo('hex2_kicad:PWR_FLAG', '#FLG01', 'PWR_FLAG', '', 50.8, 139.7)
    s.simbolo('hex2_kicad:PWR_FLAG', '#FLG02', 'PWR_FLAG', '', 76.2, 139.7)

    for n, rete in {1: '5V_REG', 2: 'GND', 3: 'IN', 4: 'OUT'}.items():
        s.collega('J1', n, rete)
    for n, rete in {1: 'OE1', 2: 'IN', 3: 'Y1', 14: '5V_REG', 7: 'GND',
                    4: 'GND', 5: 'GND', 9: 'GND', 10: 'GND', 12: 'GND', 13: 'GND'}.items():
        s.collega('U3', n, rete)
    for n in (6, 8, 11):
        s.libero('U3', n)
    s.collega('R1', 1, 'Y1')
    s.collega('R1', 2, 'OUT')
    s.collega('C1', 1, '5V_REG')
    s.collega('C1', 2, 'GND')
    s.collega('JP1', 1, 'GND')
    s.collega('JP1', 2, 'OE1')
    s.collega('JP1', 3, '5V_REG')
    s.collega('TP1', 1, 'OUT')
    s.collega('#FLG01', 1, '5V_REG')
    s.collega('#FLG02', 1, 'GND')
    return s


if __name__ == '__main__':
    print(schema().salva(QUI))
    scrivi_progetto(QUI, 'prova')
