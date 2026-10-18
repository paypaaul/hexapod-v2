"""PCB-C, scheda del carapace: schema generato da script (piano-pcb.md 4.2; piedinatura di cablaggio.md 3.5).

Il TCA9534 sulla scheda è stato tolto alla verifica R1: esiste solo in SOIC largo o TSSOP, che non stanno nei
7,4 × 19 mm utili; l'espansore è il modulo X20. Pad n di J2 = polo n del cavo; poli dispari sulla fila lato chiave.

Le reti si scrivono qui a mano e `verifica_reti.py` le confronta con scheda_def.py. Componenti sotto la scheda.
"""

import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', 'script'))

from schema_kicad import Schema, scrivi_progetto  # noqa: E402

LIBRERIE = os.path.join(QUI, '..', 'librerie')
TP = 'hex2:TestPoint_THTPad_1.5x1.5mm_Drill0.7mm'

# testata 2 × 8 (cablaggio.md 3.5, tabella dei poli)
POLI = {1: '5V', 2: '5V', 3: 'GND', 4: 'DATA', 5: 'GND', 6: 'SCL', 7: '3V3', 8: 'SDA', 9: 'GND', 10: 'BCLK',
        11: 'WS', 12: 'MIC', 13: 'AMP', 14: 'RISERVA14', 15: 'BTN_A', 16: 'BTN_B'}

# piazzole dei fili, una per filo e raggruppate per modulo (piano 4.2)
PIAZZOLE = [
    ('P1', 'Qwiic verso X20', ['GND', '3V3', 'SDA', 'SCL']),            # DU-2 = no: cavo Qwiic tagliato
    ('P2', 'catena LED', ['5V', 'DATA', 'GND']),
    ('P3', 'microfoni', ['3V3', 'GND', 'BCLK', 'WS', 'MIC']),           # R8 da 100 kΩ resta al microfono
    ('P4', 'amplificatore', ['5V', 'GND', 'BCLK', 'WS', 'AMP']),
    ('P5', 'ToF posteriore', ['3V3', 'GND', 'SDA', 'SCL']),  # l'XSHUT va diretto a X20 (schemi.md 2.4)
    ('P6', 'pulsante', ['BTN_A', 'BTN_B']),                             # piste isolate e lontane (S-10)
    ('P7', 'riserva polo 14', ['RISERVA14']),                           # XSHUT del ToF del mento (X25)
]
PROVE = [('TP1', '5V'), ('TP2', '3V3'), ('TP3', 'GND'), ('TP4', 'SDA'), ('TP5', 'SCL'), ('TP6', 'DATA')]


def schema():
    s = Schema('carapace', 'HEX2 CARAPACE r1', cartella_simboli=LIBRERIE)
    s.simbolo('hex2_kicad:Conn_02x08_Odd_Even', 'J2', 'Würth 61201621721',
              'hex2:IDC-Header_2x08_P2.54mm_Horizontal_Foro1.1', 76.2, 76.2)
    s.simbolo('hex2_kicad:C_Polarized', 'CE1', '470µ 10V', 'hex2:CP_Radial_D6.3mm_P2.50mm_Sdraiato', 139.7, 63.5)
    s.simbolo('hex2_kicad:R', 'R1', 'R-MIC', 'hex2:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal',
              165.1, 63.5, campi={'DNP': True})   # pull-down dei microfoni, valore al banco (S-21)
    for i, (rif, gruppo, reti) in enumerate(PIAZZOLE):
        n = len(reti)
        s.simbolo('hex2_kicad:Conn_01x%02d' % n, rif, gruppo, 'hex2:PinHeader_1x%02d_P2.54mm_Vertical' % n,
                  50.8 + 38.1 * (i % 4), 132.08 + 30.48 * (i // 4))
    for i, (rif, rete) in enumerate(PROVE):
        s.simbolo('hex2_kicad:TestPoint', rif, rete, TP, 215.9 + 17.78 * (i % 3), 127 + 22.86 * (i // 3))
    for i, rete in enumerate(['GND', '3V3']):
        s.simbolo('hex2_kicad:PWR_FLAG', '#FLG%02d' % (i + 1), 'PWR_FLAG', '', 266.7 + 17.78 * i, 127)

    for n, rete in POLI.items():
        s.collega('J2', n, rete)
    s.collega('CE1', 1, '5V')
    s.collega('CE1', 2, 'GND')
    s.collega('R1', 1, 'MIC')
    s.collega('R1', 2, 'GND')
    for rif, _, reti in PIAZZOLE:
        for k, rete in enumerate(reti, 1):
            s.collega(rif, k, rete)
    for rif, rete in PROVE:
        s.collega(rif, 1, rete)
    for i, rete in enumerate(['GND', '3V3']):
        s.collega('#FLG%02d' % (i + 1), 1, rete)
    return s


if __name__ == '__main__':
    print(schema().salva(QUI))
    scrivi_progetto(QUI, 'carapace')
