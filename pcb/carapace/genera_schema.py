"""PCB-C, scheda del carapace: schema generato da script (piano-pcb.md 4.2; piedinatura di cablaggio.md 3.5).

CE1 in piedi sotto l'ala +Y (sotto c'e' posto per 14 mm, F4); R-MIC tolta (resta R8 al microfono, D-082). Il TCA9534 sulla scheda è stato tolto alla verifica R1: esiste solo in SOIC largo o TSSOP, che non stanno nei
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

# Piazzole dei fili (revisione del 18 ottobre, D-082): una per rete, due fili per foro come la millefori della guida,
# allineate ai poli della testata. P1 accanto ai poli dispari, P2 accanto ai pari, il pulsante a parte nell'ala -Y.
# Fili: 5V catena LED e ampli; GND Qwiic, LED, microfoni, ampli, ToF; 3V3 Qwiic, microfoni, ToF; SDA e SCL Qwiic e ToF;
# BCLK e WS microfoni e ampli; DATA catena LED; MIC microfoni; AMP ampli. La riserva del polo 14 si salda sul pin di J2.
PIAZZOLE = [
    ('P1', 'poli dispari', ['5V', 'GND', 'GND', '3V3', 'GND', 'WS', 'AMP', '3V3']),
    ('P2', 'poli pari', ['5V', 'DATA', 'SCL', 'SDA', 'BCLK', 'MIC']),
    ('P3', 'pulsante', ['BTN_A', 'BTN_B']),   # lontano dalle altre reti (S-10)
]
PROVE = []


def schema():
    s = Schema('carapace', 'HEX2 CARAPACE r1', cartella_simboli=LIBRERIE)
    s.simbolo('hex2_kicad:Conn_02x08_Odd_Even', 'J2', 'Würth 61201621721',
              'hex2:IDC-Header_2x08_P2.54mm_Horizontal_Foro1.1', 76.2, 76.2)
    s.simbolo('hex2_kicad:C_Polarized', 'CE1', '470µ 10V', 'hex2:CP_Radial_D6.3mm_P2.50mm', 139.7, 63.5)
    for i, (rif, gruppo, reti) in enumerate(PIAZZOLE):
        n = len(reti)
        imp = 'hex2:Fili_1x%02d_P2.54mm_D1.7' % n
        s.simbolo('hex2_kicad:Conn_01x%02d' % n, rif, gruppo, imp, 50.8 + 38.1 * (i % 4), 132.08 + 30.48 * (i // 4))
    for i, (rif, rete) in enumerate(PROVE):
        s.simbolo('hex2_kicad:TestPoint', rif, rete, TP, 215.9 + 17.78 * (i % 3), 127 + 22.86 * (i // 3))
    for i, rete in enumerate(['GND', '3V3']):
        s.simbolo('hex2_kicad:PWR_FLAG', '#FLG%02d' % (i + 1), 'PWR_FLAG', '', 266.7 + 17.78 * i, 127)

    for n, rete in POLI.items():
        if rete == 'RISERVA14':
            s.libero('J2', n)   # riserva: il filo verso X25 si salda sul pin
        else:
            s.collega('J2', n, rete)
    s.collega('CE1', 1, '5V')
    s.collega('CE1', 2, 'GND')
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
