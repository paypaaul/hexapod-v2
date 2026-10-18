"""PCB-P, scheda dei partitori: schema generato da script (piano-pcb.md 4.3; reti di partitori_def.py).

Variante P2 (D-080) sotto le prese dei piedi, rivista nella 2.1.9 (piano-v2.1.0.md): il pettine porta solo i due poli
esterni delle spine JR (segnale e massa: il piede ha 2 fili su 3, cablaggio.md); l'FSR e' una resistenza, quindi una
spina girata funziona lo stesso. Canali 0-5 i piedi nell'ordine di robot.yaml, 6 e 7 le NTC.
I fili verso l'ADC dei canali 0-5 e le masse delle NTC si saldano sulle code dei pin del pettine, sotto la scheda; le
NTC, il 3,3 V e la massa dell'ADC hanno quattro piazzole (due fili per foro).
"""

import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', 'script'))

from schema_kicad import Schema, scrivi_progetto  # noqa: E402

LIBRERIE = os.path.join(QUI, '..', 'librerie')
R_0805 = 'hex2:R_0805_2012Metric'
C_0805 = 'hex2:C_0805_2012Metric'


def nodo(c):
    return 'N%d' % c


# piazzole dei fili: NTC sinistra (canale 6, con il filo verso A6), NTC destra (7, con A7), VIN e GND dell'ADC
PIAZZOLE = ['N6', '3V3S', 'N7', 'GND']   # 2 x 2: N6 e 3V3S in alto, N7 e GND in basso, accanto alle loro R


def schema():
    s = Schema('partitori', 'HEX2 PARTITORI r1', cartella_simboli=LIBRERIE)
    s.simbolo('hex2_kicad:Conn_01x12', 'J1', 'pettine dei piedi', 'hex2:Pettine_JR_2x06_P2.54_File5.08', 50.8, 76.2)
    s.simbolo('hex2_kicad:Conn_01x04', 'P1', 'NTC e ADC', 'hex2:Fili_2x02_P2.54mm_D1.7', 50.8, 127.0)
    for c in range(8):
        s.simbolo('hex2_kicad:R', 'R%d' % (c + 1), '10k', R_0805, 101.6 + 15.24 * c, 76.2)
        s.simbolo('hex2_kicad:C', 'C%d' % (c + 1), '100n', C_0805, 101.6 + 15.24 * c, 106.68)
    for c in range(8):
        s.collega('R%d' % (c + 1), 1, nodo(c))   # come partitori_def.py: pin 1 sul nodo, pin 2 sul 3,3 V
        s.collega('R%d' % (c + 1), 2, '3V3S')    # il 3V3 della guida: e' il ramo del 3V3S che alimenta l'ADC
        s.collega('C%d' % (c + 1), 1, nodo(c))
        s.collega('C%d' % (c + 1), 2, 'GND')
    for c in range(6):
        s.collega('J1', c + 1, 'GND')            # fila della massa (verso +Y, lontana dall'ADC)
        s.collega('J1', c + 7, nodo(c))          # fila del segnale (verso -Y, dalla parte dell'ADC)
    for k, rete in enumerate(PIAZZOLE, 1):
        s.collega('P1', k, rete)
    return s


if __name__ == '__main__':
    print(schema().salva(QUI))
    scrivi_progetto(QUI, 'partitori')
