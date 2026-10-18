"""PCB-C, scheda del carapace: contorno dal CAD e piazzamento (F4; piano-pcb.md 4.2). Lo sbroglio viene dopo la dima.

Gira con il Python di KiCad. Le quote sono nella terna del robot (X avanti, Y a sinistra) e si portano in KiCad con
genera_contorni.kicad. Tutti i componenti stanno sotto la scheda (lato B); la si guarda dall'alto del robot.
"""

import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', 'script'))

from genera_contorni import kicad  # noqa: E402
from scheda_kicad import Scheda, netlist  # noqa: E402

PASSO = 2.54
# Testata J2: la scatola va dal bordo di coda (x 29,5) a x 38,35; la fila dei poli dispari (lato chiave, S-26) sta
# 4,38 dietro la scatola. Polo 1 a +Y.
J2_X, J2_Y = 29.5 + 8.85 + 4.38, 8.89
# Griglia delle piazzole (Ø1,5) fra le file di J2 e il bordo davanti (x 51): colonne a 2,52 per stare a 0,2 dai pin
# di J2 (Ø1,8) e a 0,5 dal bordo; righe a passo 2,54 da y 8,89. Con Ø1,5 fra due vicine restano 1,02 mm: il pulsante
# (regola di 1 mm, S-10) puo' stare nella griglia
COL = {'A': 44.65, 'B': 47.17, 'C': 49.69}


def riga(i):
    return 8.89 - i * PASSO


# (rif, x, y del pad 1 nel robot, angolo); le piazzole 1 x N scendono verso -Y dal pad 1
PIAZZA = [
    ('P3', COL['A'], riga(0), 0),   # microfoni (5); A5-A7 vuote: A7 starebbe a 0,27 dal pulsante sul polo 15
    ('P1', COL['B'], riga(0), 0),   # Qwiic verso X20 (4)
    ('P7', COL['B'], riga(4), 0),   # riserva del polo 14
    ('P6', COL['B'], riga(5), 0),   # pulsante (2), a 1,02 dalle piazzole vicine; B7 vuota
    ('P4', COL['C'], riga(0), 0),   # amplificatore (5), sul bordo davanti verso di lui
    ('P2', COL['C'], riga(5), 0),   # catena LED (3)
    ('P5', 48.94, 18.54, 0),        # ToF posteriore, 2 x 2 nell'ala +Y, fuori dall'ombra della bugna (48; 12,5)
    ('R1', 48.94, 21.9, 0),         # R-MIC in piedi, non montata
    ('CE1', 49.25, -20.0, 0),       # 470 µF in piedi al centro dell'ala -Y (sotto c'e' posto per 14 mm)
]


def scheda(cartella=QUI):
    s = Scheda(netlist(os.path.join(QUI, 'carapace.kicad_sch'), os.path.join(cartella, 'carapace.net')),
               os.path.join(cartella, 'carapace.kicad_pcb'))
    s.contorni_dal_cad('carapace')
    # sul lato B KiCad ribalta specchiando la Y: con 180 gradi in piu' il risultato e' la X specchiata, cioe' la
    # scheda vista dall'alto con i pin che scendono verso -Y dal pad 1
    s.piazza('J2', *kicad(J2_X, J2_Y), angolo=180, retro=True)
    for rif, x, y, ang in PIAZZA:
        s.piazza(rif, *kicad(x, y), angolo=ang + 180, retro=True)
    return s


if __name__ == '__main__':
    cartella = sys.argv[sys.argv.index('-o') + 1] if '-o' in sys.argv else QUI
    print(scheda(cartella).salva())
