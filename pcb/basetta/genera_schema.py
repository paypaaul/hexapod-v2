"""PCB-B, basetta dell'ESP32: schema generato da script (piano-pcb.md 4.1; reti di guida/schemi/schemi.md 1.2).

Le reti si scrivono qui a mano, dal piano e da schemi.md, e `verifica_reti.py` le confronta con basetta_def.py:
derivarle dal _def le renderebbe uguali per costruzione.
"""

import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', 'script'))

from schema_kicad import Schema, scrivi_progetto  # noqa: E402

LIBRERIE = os.path.join(QUI, '..', 'librerie')

R_AX = 'hex2:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal'
TP = 'hex2:TestPoint_THTPad_1.5x1.5mm_Drill0.7mm'

# piazzole dei fili: (riferimento, gruppo, reti dal pin 1); una rete None è un pin senza filo
PIAZZOLE = [
    ('P1', 'batteria (2813)', ['VBAT', 'GND']),
    ('P2', '2813', ['SENSE', 'OFF']),
    ('P3', 'abilitazione (D2 in linea)', ['GPIO42']),
    ('P4', 'seriale SSC-32', ['TX5', 'RX5', 'GND']),  # massa vuota finché S-22 non è misurato
    ('P5', 'bus GND', ['GND'] * 5),                   # quattro rami più uno di riserva, come la guida
    ('P6', 'bus 3V3', ['3V3S'] * 5),
    ('P7', 'bus SDA', ['SDA'] * 5),
    ('P8', 'bus SCL', ['SCL'] * 5),
    ('P9', 'luci delle tibie', ['5V_LED', 'DATA_TIBIE', 'GND']),
    # cavo piatto: poli 1-14 come cablaggio.md 3.5 (polo 14 di riserva, senza rete su questa scheda)
    ('P10', 'cavo piatto', ['5V_LED', '5V_LED', 'GND', 'DATA', 'GND', 'SCL', '3V3S', 'SDA', 'GND',
                            'BCLK', 'WS', 'MIC', 'AMP', None]),
    ('P11', 'uscita di X3', ['3V3_X3', 'GND']),
    ('P12', 'impulso RMT dalla SSC-32', ['RMT_IN', 'GND']),
]

# punti di prova a gruppi (piano 4.1): potenza; 3,3 V e segnali dell'ESP32; uscite del buffer
PROVE = [('TP1', 'VBAT'), ('TP2', '5V_REG'), ('TP3', '5V_LED'), ('TP4', 'GND'),
         ('TP5', '3V3S'), ('TP6', 'SDA'), ('TP7', 'SCL'), ('TP8', 'RX3'), ('TP9', 'LED_IN'), ('TP10', 'SENSE'),
         ('TP11', 'GPIO42'), ('TP12', 'OFF'), ('TP13', 'GND'),
         ('TP14', 'TX5'), ('TP15', 'DATA'), ('TP16', 'DATA_TIBIE'), ('TP17', 'GND')]

# resistenze: (rif, valore, rete del pin 1, rete del pin 2)
RESISTENZE = [
    ('R1', '10k', 'LED_IN', 'GND'),        # tiene basso l'ingresso del buffer all'avvio
    ('R2', '330', 'DATA', 'Y1'),
    ('R4', '4k7', 'SCL', '3V3S'),          # 5,1 kΩ del kit Elegoo o 10 kΩ di B10 (piano 2)
    ('R5', '4k7', '3V3S', 'SDA'),
    ('R7', '47k', 'SENSE', 'GND'),         # partitore con R6 da 100 kΩ sulla 2813
    ('R9', '330', 'DATA2', 'DATA_TIBIE'),  # prima nella guaina, ora sulla scheda
    ('R10', '10k', 'TX3', '3V3_ESP'),      # pull-up di 3A verso il 3V3 dell'ESP32, mai verso il 5 V
    ('R11', '20k', 'RX5', 'RX3'),          # partitore della RX: 3,11 V con 5,0 V
    ('R12', '33k', 'RX3', 'GND'),
    ('R13', '330', 'TX5_3Y', 'TX5'),       # R-TX
    ('R14', '20k', 'RMT_IN', 'RMT'),       # partitore di JP-RMT, come la RX
    ('R15', '33k', 'RMT', 'GND'),
]


def schema():
    s = Schema('basetta', 'HEX2 BASETTA r1', cartella_simboli=LIBRERIE)
    s.simbolo('hex2:ESP32_S3_CAM_RE13', 'U1', 'ESP32-S3-CAM RE1.3', 'hex2:ESP32_S3_CAM_RE13_Strip', 101.6, 101.6)
    s.simbolo('hex2:D24V22F5', 'U2', 'D24V22F5', 'hex2:Pololu_D24V22F5', 190.5, 50.8)
    for u, (x, y) in enumerate([(190.5, 101.6), (190.5, 127), (190.5, 152.4), (190.5, 177.8), (241.3, 101.6)], 1):
        s.simbolo('hex2_kicad:74AHCT125', 'U3', 'SN74AHCT125N', 'hex2:DIP-14_W7.62mm', x, y, unita=u)
    s.simbolo('hex2_kicad:D_Schottky', 'D1', '1N5819', 'hex2:D_DO-41_SOD81_P10.16mm_Horizontal', 241.3, 50.8)
    s.simbolo('hex2_kicad:Polyfuse', 'PTC1', 'MF-R090', 'hex2:Fuse_Bourns_MF-R090_Sdraiato', 279.4, 50.8)
    s.simbolo('hex2_kicad:C', 'CS1', '100n', 'hex2:C_Disc_D3.8mm_W2.6mm_P2.50mm', 279.4, 88.9)
    s.simbolo('hex2_kicad:C', 'CS2', '100n', 'hex2:C_Disc_D3.8mm_W2.6mm_P2.50mm', 304.8, 88.9)
    s.simbolo('hex2_kicad:SolderJumper_3_Bridged12', 'JP1', 'JP-3V3',
              'hex2:SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm', 304.8, 50.8)
    s.simbolo('hex2_kicad:SolderJumper_2_Open', 'JP2', 'JP-RMT',
              'hex2:SolderJumper-2_P1.3mm_Open_RoundedPad1.0x1.5mm', 340.36, 50.8)
    for i, (rif, val, _, _) in enumerate(RESISTENZE):
        s.simbolo('hex2_kicad:R', rif, val, R_AX, 279.4 + 20.32 * (i % 6), 111.76 + 30.48 * (i // 6))
    posti = {'P1': (279.4, 167.64), 'P2': (312.42, 167.64), 'P3': (345.44, 167.64), 'P4': (378.46, 167.64),
             'P5': (279.4, 195.58), 'P6': (312.42, 195.58), 'P7': (345.44, 195.58), 'P8': (378.46, 195.58),
             'P9': (279.4, 228.6), 'P11': (312.42, 228.6), 'P12': (345.44, 228.6), 'P10': (241.3, 210.82)}
    for rif, gruppo, reti in PIAZZOLE:
        n = len(reti)
        x, y = posti[rif]
        s.simbolo('hex2_kicad:Conn_01x%02d' % n, rif, gruppo, 'hex2:PinHeader_1x%02d_P2.54mm_Vertical' % n, x, y)
    for i, (rif, rete) in enumerate(PROVE):
        s.simbolo('hex2_kicad:TestPoint', rif, rete, TP, 30.48 + 17.78 * (i % 6), 190.5 + 22.86 * (i // 6))
    for i, rete in enumerate(['VBAT', 'GND', '5V_ESP']):
        s.simbolo('hex2_kicad:PWR_FLAG', '#FLG%02d' % (i + 1), 'PWR_FLAG', '', 30.48 + 15.24 * i, 266.7)

    # ESP32 (schemi.md 1.2; piano-elettronica-software.md 2.4)
    for nome, rete in {'5V': '5V_ESP', '3V3': '3V3_ESP', 'GND': 'GND', 'GPIO14': 'RX3', 'GPIO21': 'TX3',
                       'GPIO3': 'SCL', 'GPIO47': 'SDA', 'GPIO48': 'LED_IN', 'GPIO38': 'BCLK', 'GPIO39': 'WS',
                       'GPIO40': 'MIC', 'GPIO41': 'OFF', 'GPIO42': 'GPIO42', 'GPIO2': 'AMP',
                       'GPIO1': 'SENSE'}.items():
        s.collega_nome('U1', nome, rete)
    for n in range(1, 41):
        if str(n) not in s.collegamenti['U1']:
            s.libero('U1', n)
    # regolatore: EN e PG liberi (EN ha 270 kΩ interni verso VIN)
    for nome, rete in {'VIN': 'VBAT', 'VOUT': '5V_REG'}.items():
        s.collega_nome('U2', nome, rete)
    s.collega('U2', 4, 'GND')
    s.collega('U2', 6, 'GND')
    s.libero('U2', 1)
    s.libero('U2', 2)
    # buffer: 1 → anello (polo 4), 2 → tibie, 3 → seriale verso la SSC-32 (DU-1), 4 non usato con gli ingressi a massa
    for n, rete in {1: 'GND', 2: 'LED_IN', 3: 'Y1', 4: 'GND', 5: 'LED_IN', 6: 'DATA2', 7: 'GND',
                    8: 'TX5_3Y', 9: 'TX3', 10: 'GND', 12: 'GND', 13: 'GND', 14: '5V_REG'}.items():
        s.collega('U3', n, rete)
    s.libero('U3', 11)
    s.collega('D1', 1, '5V_ESP')   # catodo
    s.collega('D1', 2, '5V_REG')   # anodo
    s.collega('PTC1', 1, '5V_REG')
    s.collega('PTC1', 2, '5V_LED')
    s.collega('CS1', 1, 'SENSE')
    s.collega('CS1', 2, 'GND')
    s.collega('CS2', 1, '5V_REG')
    s.collega('CS2', 2, 'GND')
    s.collega('JP1', 1, '3V3_ESP')  # lato chiuso: 3V3 dell'ESP32
    s.collega('JP1', 2, '3V3S')
    s.collega('JP1', 3, '3V3_X3')   # lato aperto: uscita di X3 (D-076: mai J1 e X3 insieme)
    s.collega('JP2', 1, 'BCLK')     # GPIO38
    s.collega('JP2', 2, 'RMT')
    for rif, _, a, b in RESISTENZE:
        s.collega(rif, 1, a)
        s.collega(rif, 2, b)
    for rif, _, reti in PIAZZOLE:
        for k, rete in enumerate(reti, 1):
            if rete:
                s.collega(rif, k, rete)
            else:
                s.libero(rif, k)
    for rif, rete in PROVE:
        s.collega(rif, 1, rete)
    for i, rete in enumerate(['VBAT', 'GND', '5V_ESP']):
        s.collega('#FLG%02d' % (i + 1), 1, rete)
    return s


if __name__ == '__main__':
    print(schema().salva(QUI))
    scrivi_progetto(QUI, 'basetta')
