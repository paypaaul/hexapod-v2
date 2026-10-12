"""Basetta dell'ESP32, seconda versione (dopo la verifica elettrica degli schemi F3b)."""
import math
from modello import Griglia, Scheda, P, h

GB = Griglia(23.77, 15.24, 21, 13)
BAS = dict(x0=22.0, x1=78.0, y0=-17.5, y1=17.5)
# viti M3 x 6 del vassoio (teste DIN 912 Ø 5,5 x 3 sotto la basetta): guida/dati/fori.json Corpo_Vassoio foro_aa/ab/pa/pb
TESTE_M3 = [(30.0, 12.5), (30.0, -12.5), (75.0, 12.5), (75.0, -12.5)]
# colonnine Ø 5,8 del vassoio con le viti M2 (D-053; fori.json bas_col_pa/pb/aa/ab_ins)
COLONNINE = [(29.0, 6.8), (29.0, -6.8), (75.5, 6.5), (75.5, -6.5)]
R_TESTA, R_COL = 2.75, 2.9
GIUNTO = 0.9     # raggio di una saldatura sul lato saldature [S]
FILO = 0.6       # mezzo diametro del filo piu' margine

ESP_L = ['5V', '14', '13', '12', '11', '10', '9', '46', '3', '8', '18', '17', '16', '15', '7', '6', '5', '4', 'RST', '3V3']
ESP_R = ['GND', '19', '20', '21', '47', '48', '45', '0', '35', '36', '37', '38', '39', '40', '41', '42', '2', '1', '44', '43']
ESP_NET = {'A2': '5V_ESP', 'B2': 'RX3', 'I2': 'SCL', 'T2': '3V3_ESP',
           'A12': 'GND', 'D12': 'TX3', 'E12': 'SDA', 'F12': 'LED_IN', 'L12': 'BCLK', 'M12': 'WS', 'N12': 'MIC',
           'O12': 'OFF', 'P12': 'GPIO42', 'Q12': 'AMP', 'R12': 'SENSE'}

B = Scheda(GB, 'basetta')
for x, y in TESTE_M3:
    B.zone.append((x, y, R_TESTA, R_TESTA + GIUNTO, R_TESTA + FILO, 'testa M3'))
for x, y in COLONNINE:
    B.zone.append((x, y, R_COL, R_COL + GIUNTO, R_COL + FILO, 'colonnina'))
for f in GB.fori():
    x, y = GB.xy(f)
    for zx, zy, rc, rf, rw, t in B.zone:
        if math.hypot(x - zx, y - zy) < rf:
            B.vietati[f] = t

# ---------------------------------------------------------------- U1: strip dell'ESP32
for i, n in enumerate(ESP_L):
    f = GB.nome(i, 2); B.pin[f] = ('U1', n, ESP_NET.get(f))
for i, n in enumerate(ESP_R):
    f = GB.nome(i, 12); B.pin[f] = ('U1', n, ESP_NET.get(f))
# pin non usati: tagliati a filo e non saldati (meno giunti accanto alle piazzole delle righe 1, 3 e 13)
for f, (c, n, r) in list(B.pin.items()):
    if c == 'U1' and r is None:
        B.nosald.add(f)
# P-2 (GPIO6, camera) non si salda comunque: ci passa sotto il filo della batteria
STRIP_IN_ZONA = sorted(f for f in B.pin if B.pin[f][0] == 'U1' and f in B.vietati)

# ---------------------------------------------------------------- U2 regolatore 5 V (ordine dei pin [C], S-03)
for f, n, r in (('N4', 'PG', None), ('O4', 'EN', None), ('P4', 'VIN', 'VBAT'), ('Q4', 'GND', 'GND'), ('R4', 'VOUT', '5V_REG')):
    B.metti(f, 'U2', n, r)
# ---------------------------------------------------------------- U3 SN74AHCT125N: canale 1 al polo 4, canale 2 alle tibie
for f, n, r in (('E8', '1 1OE', 'GND'), ('F8', '2 1A', 'LED_IN'), ('G8', '3 1Y', 'Y1'), ('H8', '4 2OE', 'GND'),
                ('I8', '5 2A', 'LED_IN'), ('J8', '6 2Y', 'DATA2'), ('K8', '7 GND', 'GND'), ('K11', '8 3Y', 'LO'),
                ('J11', '9 3A', 'GND'), ('I11', '10 3OE', 'GND'), ('H11', '11 4Y', 'LO'), ('G11', '12 4A', 'GND'),
                ('F11', '13 4OE', 'GND'), ('E11', '14 VCC', '5V_REG')):
    B.metti(f, 'U3', n, r)
# ---------------------------------------------------------------- U4 traslatore (sigle e passo [C], S-04)
# TX3 sul canale 1, RX3 sul canale 3: il canale 2 (L2 in G-7) resta libero accanto all'uscita 1Y (G-8)
for f, n, r in (('E4', 'HV', '5V_REG'), ('F4', 'H1', 'TX5'), ('G4', 'H2', 'H_NC'), ('H4', 'H3', 'RX5'),
                ('I4', 'H4', 'H_NC'), ('J4', 'GND', 'GND'), ('E7', 'LV', '3V3S'), ('F7', 'L1', 'TX3'),
                ('G7', 'L2', 'L_NC'), ('H7', 'L3', 'RX3'), ('I7', 'L4', 'L_NC'), ('J7', 'GND', 'GND')):
    B.metti(f, 'U4', n, r)

# ---------------------------------------------------------------- componenti assiali (catodo sul primo foro per i diodi)
# (rif, valore, foro1, rete1, foro2, rete2, lunghezza, diametro, tipo)
ASSIALI = [
    ('PTC1', 'MF-R075', 'L8', '5V_REG', 'L10', '5V_LED', None, None, 'ptc'),
    ('D1', '1N5819', 'A6', '5V_ESP', 'D6', '5V_REG', 5.2, 2.7, 'diodo'),
    ('R2', '330 Ω', 'L4', 'DATA', 'L7', 'Y1', 6.0, 2.3, 'res'),
    ('R1', '10 kΩ', 'D8', 'LED_IN', 'A8', 'GND', 6.0, 2.3, 'res'),
    ('R7', '47 kΩ', 'T11', 'SENSE', 'Q11', 'GND', 6.0, 2.3, 'res'),
    ('R4', '4,7 kΩ', 'J3', 'SCL', 'M3', '3V3S', 6.0, 2.3, 'res'),
    ('R5', '4,7 kΩ', 'N3', '3V3S', 'Q3', 'SDA', 6.0, 2.3, 'res'),
]
for rif, val, f1, n1, f2, n2, *_ in ASSIALI:
    B.metti(f1, rif, '', n1); B.metti(f2, rif, '', n2)
SMD = [('CS1', '100 nF', 'R11', 'R10', 'SENSE', 'GND'), ('CS2', '100 nF', 'E11', 'F11', '5V_REG', 'GND')]
B.metti('R11', 'CS1', '', 'SENSE'); B.metti('R10', 'CS1', '', 'GND')

# ---------------------------------------------------------------- piazzole dei fili esterni
EST = {}
def est(f, rete, testo, lato, awg, va):
    B.metti(f, 'filo', testo, rete); EST[f] = dict(rete=rete, testo=testo, lato=lato, awg=awg, va=va)

est('E3', 'GND', 'massa della seriale (Dupont)', 'coda', 26, 'pin GND della SSC-32')
est('F3', 'TX5', 'TX verso la SSC-32 (Dupont)', 'coda', 26, 'pin RX della SSC-32')
est('H3', 'RX5', 'RX dalla SSC-32 (Dupont)', 'coda', 26, 'pin TX della SSC-32')
# riga 1: bus dei sensori, un ramo per foro
for c in 'ABEF': est(c + '1', 'GND', 'GND', 'bus', 30, '')
for c in 'GHIJ': est(c + '1', 'SCL', 'SCL', 'bus', 30, '')
for c in 'KLMN': est(c + '1', '3V3S', '3V3', 'bus', 30, '')
for c in 'QRST': est(c + '1', 'SDA', 'SDA', 'bus', 30, '')
# riga 13: cavo piatto e fili verso il retro del corpo
CAVO = [('A13', '5V_LED', 1), ('B13', '5V_LED', 2), ('E13', 'GND', 3), ('F13', 'DATA', 4), ('G13', 'GND', 5),
        ('H13', 'SCL', 6), ('I13', '3V3S', 7), ('J13', 'SDA', 8), ('K13', 'GND', 9), ('L13', 'BCLK', 10),
        ('M13', 'WS', 11), ('N13', 'MIC', 12), ('O13', 'AMP', 13)]
for f, n, polo in CAVO:
    est(f, n, str(polo), 'cavo', 28, 'polo %d della spina IDC' % polo)
EST['B13']['testo'] = '2 + 5 V tibie'
EST['K13']['testo'] = '9 + massa tibie'
est('P13', 'GPIO42', 'GPIO42 → D2 in linea → EN', 'lato', 26, 'D2 (1N4148) nella guaina, poi ENA dei due D42V110F6, ognuno con R3 verso massa')
est('Q13', 'OFF', 'OFF della 2813', 'lato', 26, 'pin OFF della 2813 (100 kΩ verso massa sulla 2813)')
est('R13', 'SENSE', 'partitore (100 kΩ alla 2813)', 'lato', 26, 'R6 da 100 kΩ saldata sull’uscita della 2813')
est('S13', 'GND', 'massa della 2813', 'lato', 26, 'massa della 2813')
est('T13', 'DATA2', 'dato tibie (330 Ω in linea)', 'lato', 30, 'polo arancio delle prese delle luci, con R9 da 330 Ω nella guaina')
# VBAT: un filo solo, dalla 2813 lungo il bordo sinistro, saldato per ultimo su P-4 (nessuna piazzola a parte)

# ---------------------------------------------------------------- ponticelli (stagno o filo nudo)
B.ponte('P12', 'P13')                                                    # GPIO42 verso il filo esterno
B.ponte('J4', 'J5', 'J6', 'J7')                                          # masse di U4
B.ponte('F11', 'G11'); B.ponte('I11', 'J11')                             # masse di U3
# barra di massa sotto U3: filo nudo lungo la riga 10 (fori vuoti fra le file del DIP) e ponticelli verso i pin
B.ponte('E10', 'F10', 'G10', 'H10', 'I10', 'J10', 'K10', rete='GND')
B.ponte('E8', 'E9', 'E10'); B.ponte('H8', 'H9', 'H10'); B.ponte('K8', 'K9', 'K10'); B.ponte('F10', 'F11'); B.ponte('I10', 'I11')
B.ponte('M3', 'N3')                                                      # 3V3S fra R4 e R5
B.ponte('T2', 'T3')                                                      # 3V3 dell'ESP32
B.ponte('I1', 'I2')                                                      # SCL
B.ponte('F3', 'F4'); B.ponte('H3', 'H4')                                 # seriale lato 5 V
B.ponte('A1', 'B1'); B.ponte('E1', 'F1'); B.ponte('G1', 'H1', 'I1'); B.ponte('I1', 'J1')
B.ponte('K1', 'L1', 'M1', 'N1'); B.ponte('Q1', 'R1', 'S1', 'T1')
B.ponte('A13', 'B13'); B.ponte('L12', 'L13'); B.ponte('M12', 'M13'); B.ponte('N12', 'N13'); B.ponte('R12', 'R13')
B.ponte('R12', 'R11'); B.ponte('R11', 'S11'); B.ponte('S11', 'T11')       # SENSE fino a R7
B.ponte('R10', 'Q10'); B.ponte('Q10', 'Q11')                             # massa di CS1
B.ponte('Q4', 'Q5', 'Q6')                                                # stella di massa sotto U2

# il GPIO21 (D-12) sta sopra la testa M3: il suo filo esce verso E-11 sopra il bordo della testa (solo con teste basse, S-19)
B.capi_ammessi.add(('D12', (3, 11)))
