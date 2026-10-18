"""PCB-B, basetta dell'ESP32: contorno dal CAD, apertura sotto U2 e piazzamento (F4, piano-pcb.md 4.1).

Gira con il Python di KiCad. Le quote sono nella terna del robot (X avanti, Y a sinistra) e si portano in KiCad con
genera_contorni.kicad; la scheda si guarda dall'alto, componenti sopra (lato F).

Vincoli che decidono la disposizione (quote lette dal CAD, 2.1.8):
- sopra la scheda (z 7,5) ci sono 8,5 mm fino al PCB dell'ESP32, meno il suo retro: x 20…33 |y| ≤ 9 alto 2,1 (restano
  6,4), x 33…57 |y| ≤ 9 alto 0,6 (7,9), microSD x 57…73 |y| ≤ 7 alta 2,0 (6,5); fuori da queste scatole 8,5;
- U2 (D24V22F5, 7,12 dalla faccia bassa del suo PCB, STEP Pololu) entra solo nella fascia x 33…57, e solo con
  l'apertura sotto i suoi componenti inferiori (1,1 mm): appoggiato sulla scheda arriva a z 14,62 contro 15,4;
- fuori dall'ombra dell'ESP32 restano solo le due fasce di bordo (|y| 14,15…17,5): una fila di piazzole per lato;
- VBAT: la piazzola d'ingresso sta accanto al VIN di U2, con accanto solo masse e a 5 mm da 3,3 V e GPIO (piano 4.1);
  il filo arriva da sotto la scheda, come sulla millefori (sotto ci sono 3,3 mm fino al vassoio).
"""

import json
import math
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', 'script'))

from genera_contorni import kicad  # noqa: E402
from scheda_kicad import Scheda, classi_di_rete, netlist  # noqa: E402

PASSO = 2.54
X_ESP0 = 23.77                      # primo pin delle file dell'ESP32 (coda), V: Rif_ESP32_S3_CAM, pin_header
Y_ESP = 12.7
Y_FILA = 15.8                       # file di piazzole dei bordi: 1,4 dalla strip, 0,85 dal bordo
# U2 con la fila dei pin verso la testa: modulo x U2_X…U2_X+17,78, y U2_YB…U2_YB+17,78 (STEP Pololu, scheda 17,78)
U2_X, U2_YB = 34.0, -9.58
U2_LATO = 17.78


def x_esp(k):
    return round(X_ESP0 + k * PASSO, 3)


def u2(mx, my):
    """Punto della terna dello STEP Pololu (mx lungo la fila dei pin da PG, my verso l'interno) nella terna del robot."""
    return (round(U2_X + U2_LATO - my, 3), round(U2_YB + mx, 3))


def apertura_u2():
    """Apertura sotto i componenti inferiori di U2: STEP Pololu, scatola mx 1,44…15,49, my 3,02…15,44, piu' 0,5 per
    lato, e una tacca attorno al secondo GND (mx 1,27, my 11,94); verso la fila dei pin 0,4 (rame dal bordo 0,5)."""
    return [u2(0.94, 2.62), u2(15.99, 2.62), u2(15.99, 15.94), u2(2.62, 15.94), u2(2.62, 9.5), u2(0.94, 9.5)]


# classi di rete per il DRC e per Freerouting: larghezze del .kicad_dru; VBAT e l'EN di U2 a 1 mm da tutto
CLASSI = {
    'VBAT': (1.5, 1.0, ['VBAT', 'unconnected-(U2-EN-Pad2)']),
    '5V_REG': (1.5, 0.2, ['5V_REG']),
    '5V_LED': (1.0, 0.2, ['5V_LED']),
    '5V_ESP': (0.6, 0.2, ['5V_ESP']),
    '3V3': (0.3, 0.2, ['3V3S', '3V3_ESP', '3V3_X3']),
}
PISTE = os.path.join(QUI, 'piste.json')
# quattro strati (scelta dell'utente del 18 ottobre, F4): a due la basetta non si sbroglia con le regole del piano
# (9 connessioni di segnale aperte e 8 isole di massa, con script/sbroglio.py e con Freerouting)
STRATI = 4


def scheda(cartella=QUI):
    classi_di_rete(os.path.join(cartella, 'basetta.kicad_pro'), CLASSI)
    s = Scheda(netlist(os.path.join(QUI, 'basetta.kicad_sch'), os.path.join(cartella, 'basetta.net')),
               os.path.join(cartella, 'basetta.kicad_pcb'), strati=STRATI)
    g = s.contorni_dal_cad('basetta')
    # l'apertura e' scritta in genera_contorni (che controlla il PCB): deve seguire U2
    attesa = [kicad(*p) for p in apertura_u2()]
    if sorted(attesa) != sorted(tuple(p) for p in g['aperture'][0]):
        raise ValueError('apertura di genera_contorni %s diversa da quella di U2 %s' % (g['aperture'][0], attesa))

    def piazza(rif, x, y, angolo=0):
        s.piazza(rif, *kicad(x, y), angolo=angolo)

    # U1: centro delle file
    piazza('U1', X_ESP0 + 9.5 * PASSO, 0)
    # U2: pin 1 (PG) in alto sulla fila di coda; l'impronta ha la fila lungo la sua x e il modulo verso la sua -y
    piazza('U2', *u2(1.27, 1.27), angolo=90)
    for rif, (x, y, a) in POSTI.items():
        piazza(rif, x, y, a)
    for rif, (x, y, a) in SOTTO.items():
        s.piazza(rif, *kicad(x, y), angolo=a, retro=True)
    # sotto il modulo U2, che appoggia sulla scheda, niente piste ne' vie sopra; sotto il disco di PTC1 niente
    # riempimento (a PTC scattato la superficie passa i 100 °C, R-10)
    s.area_senza_rame('sotto_U2', ['F.Cu'], [kicad(x, y) for x, y in
                      [(U2_X, U2_YB), (U2_X + U2_LATO, U2_YB), (U2_X + U2_LATO, U2_YB + U2_LATO), (U2_X, U2_YB + U2_LATO)]],
                      'piste')
    px, py = POSTI['PTC1'][:2]
    s.area_senza_rame('sotto_PTC1', ['F.Cu', 'B.Cu'], [kicad(x, y) for x, y in
                      [(px - 13.7, py - 1.2), (px - 1.5, py - 1.2), (px - 1.5, py + 6.3), (px - 13.7, py + 6.3)]],
                      'riempimento')
    if STRATI == 4:
        # strati interni: il rame dal bordo (0,5) anche attorno ai fori e all'apertura, come aree vietate, perche'
        # Freerouting le veda (ai fori sulle facce esterne pensano gia' gli anelli di genera_contorni)
        for _, x, y, d in g['fori']:
            s.area_senza_rame('foro_%.1f_%.1f' % (x, y), ['In1.Cu', 'In2.Cu'],
                              [(x + (d / 2 + 0.5) * math.cos(a * math.pi / 16), y + (d / 2 + 0.5) * math.sin(a * math.pi / 16))
                               for a in range(32)])
        s.area_senza_rame('bordo_apertura', ['F.Cu', 'In1.Cu', 'In2.Cu', 'B.Cu'], s.gonfia(g['aperture'][0], 0.5))
    if os.path.exists(PISTE):
        d = s.piste_da_file(PISTE, kicad)
        if 'Freerouting' in d.get('origine', ''):
            for strato in ('B.Cu', 'F.Cu') + (('In1.Cu',) if STRATI == 4 else ()):
                s.riempimento('GND', s.contorno_rientrato(0.5), strato, 0.3)
    return s


# fila del bordo -Y (y -15,8), posti alle x dei pin. In coda GPIO42 e i fili della 2813; poi il cavo piatto, poli 1-13,
# con i poli 1-2 (5V_LED) e 4 (DATA) sui varchi dei pin 27, 28 e 30; in testa il dato delle tibie sul varco del pin 40
# fila del bordo +Y (y +15,8): bus a 5 rami, GND, SDA, SCL, 3V3S
VIN = u2(6.35, 1.27)
X_PIEDI = [54.2 + 2.9 * k for k in range(6)]    # resistenze in piedi nella fascia +Y della testa (8,5 mm liberi)
POSTI = {
    'P3': (x_esp(0), -Y_FILA, 0),
    'P9': (x_esp(19), -Y_FILA, 0),
    'P2': (x_esp(3), -Y_FILA, 90),
    'P10': (x_esp(6), -Y_FILA, 90),
    'P5': (x_esp(0), Y_FILA, 90),
    'P7': (x_esp(5), Y_FILA, 90),
    'P8': (x_esp(10), Y_FILA, 90),
    'P6': (x_esp(15), Y_FILA, 90),
    # testa: VBAT accanto al VIN di U2 (pin 1 VBAT, pin 2 GND verso +Y), D1 sopra il modulo, U3 coricato con VCC verso
    # PTC1, che sta sotto con il disco verso la coda
    'P1': (VIN[0] + PASSO, VIN[1], 180),
    'D1': (37.7, 9.75, 0),
    'U3': (70.99, 5.6, -90),
    'PTC1': (70.7, -9.24, 90),
    'JP1': (72.1, 10.4, 0),
    'P11': (52.9, 5.5, 0),
    'TP2': (50.7, 9.9, 0),
    'TP4': (53.4, -6.6, 0),
    'R5': (X_PIEDI[0], 10.0, -90),
    'R4': (X_PIEDI[1], 10.0, -90),
    'R2': (X_PIEDI[2], 10.0, -90),
    'R9': (X_PIEDI[3], 10.0, -90),
    'R7': (X_PIEDI[4], 10.0, -90),
    'R13': (X_PIEDI[5], 10.0, -90),
    # coda: seriale verso la SSC-32, partitore della RX, punti di prova
    'P4': (23.9, -5.4, 0),
    'R11': (31.12, 0.0, 180),
    'TP8': (24.2, 5.3, 0),
    'TP9': (24.6, -2.9, 0),
    'TP12': (27.2, -2.6, 0),
    'TP13': (31.2, -2.6, 0),
}

# lato sotto: R12 sdraiata in coda; 0805 dove sopra non c'e' niente
SOTTO = {
    'R12': (24.0, 2.3, 0),       # corpo a 0,35 dalla colonnina del vassoio (29; 6,8), Ø5,8
    'R16': (33.4, -10.4, 0),
    'CS1': (36.4, -8.3, 0),
    'CS2': (69.47, 0.9, 0),
    'R1': (62.0, 3.0, 0),
    'R10': (58.0, 3.0, 0),
}


# Ingombri dei corpi per la prova nel CAD (cad/script/assieme.py -> ingombri_pcb): scatole nella terna del robot.
# Faccia alta della basetta a z 7,5, bassa a 5,9 (assieme.py, Rif_Basetta_50x70). Altezze: U2 7,12 dalla faccia bassa
# del suo PCB (STEP Pololu, V); U3 5,08 (TI SCLS264R, package N, altezza massima, V); PTC1 3,0 (scheda Bourns, V); D1
# Ø2,7 x 5,2 (DO-41, S); resistenze in piedi 7,5 (corpo 6,3 piu' la curva del reoforo, S); sdraiate Ø2,5 (S); code dei
# reofori sotto la scheda 1,5 (tagliate, S)
Z_SU, Z_GIU = 7.5, 5.9
CODE = 1.5


def ingombri():
    out = []
    u3x = (POSTI['U3'][0] + POSTI['U3'][0] - 6 * PASSO) / 2
    u3y = (POSTI['U3'][1] + POSTI['U3'][1] - 3 * PASSO) / 2
    out.append(('U2', U2_X, U2_YB, Z_SU, U2_X + U2_LATO, U2_YB + U2_LATO, Z_SU + 7.12))
    out.append(('U3', u3x - 9.53, u3y - 3.18, Z_SU, u3x + 9.53, u3y + 3.18, Z_SU + 5.08))
    px, py = POSTI['PTC1'][:2]
    out.append(('PTC1', px - 1.5 - 12.2, py + 2.54 - 3.7, Z_SU, px - 1.5, py + 2.54 + 3.7, Z_SU + 3.0))
    dx, dy = POSTI['D1'][:2]
    out.append(('D1', dx + 5.08 - 2.6, dy - 1.35, Z_SU, dx + 5.08 + 2.6, dy + 1.35, Z_SU + 2.7))
    for rif in ('R2', 'R4', 'R5', 'R7', 'R9', 'R13'):
        x, y = POSTI[rif][:2]
        out.append((rif, x - 1.25, y - 1.25, Z_SU, x + 1.25, y + 1.25, Z_SU + 7.5))
    x, y = POSTI['R11'][:2]
    out.append(('R11', x - 3.81 - 3.15, y - 1.25, Z_SU, x - 3.81 + 3.15, y + 1.25, Z_SU + 2.5))
    x, y = SOTTO['R12'][:2]
    out.append(('R12', x + 3.81 - 3.15, y - 1.25, Z_GIU - 2.5, x + 3.81 + 3.15, y + 1.25, Z_GIU))
    return out


def scrivi_ingombri(scheda, percorso=os.path.join(QUI, 'ingombri.json')):
    """Scatole dei corpi e, per ogni piazzola a foro, quella della coda del reoforo sotto la scheda (Ø1,2)."""
    import pcbnew
    corpi = ingombri()
    for fp in sorted(scheda.board.GetFootprints(), key=lambda f: f.GetReference()):
        for p in fp.Pads():
            if p.GetAttribute() != pcbnew.PAD_ATTRIB_PTH:
                continue
            x, y = pcbnew.ToMM(p.GetPosition().x) - 100, 100 - pcbnew.ToMM(p.GetPosition().y)
            corpi.append(('code_%s.%s' % (fp.GetReference(), p.GetNumber()), x - 0.6, y - 0.6, Z_GIU - CODE,
                          x + 0.6, y + 0.6, Z_GIU))
    with open(percorso, 'w', encoding='utf-8') as f:
        json.dump({'scatole': [[n] + [round(v, 3) for v in q] for n, *q in corpi]}, f)
        f.write('\n')
    return percorso


if __name__ == '__main__':
    cartella = sys.argv[sys.argv.index('-o') + 1] if '-o' in sys.argv else QUI
    s = scheda(cartella)
    print(s.salva())
    if cartella == QUI:
        print(scrivi_ingombri(s))
