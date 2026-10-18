"""PCB-P, scheda dei partitori: piazzamento (2.1.9, piano-v2.1.0.md) con la sagoma di prova.

Gira con il Python di KiCad. Terna del robot. La sagoma non viene ancora dal CAD: e' quella della prova dello spazio
del 19 ottobre (x 44,2…78, y 18,6…27,2, piano-v2.1.0.md), da portare nel CAD con la 2.1.9; poi il contorno torna a
genera_contorni ('partitori') come per le altre schede.

Disposizione:
- pettine J1 a due file (massa a y 25,29, segnale a 20,21; colonne da x 50,25 come cor_par_pet_x 56,6 del CAD);
- fra le due file, sotto, i 100 nF dei canali 0-5 (ognuno fra il suo pin del segnale e il suo pin di massa) e, sopra,
  i 10 kΩ dei canali 0-3 sdraiati (sotto le spine, che appoggiano sulle plastiche delle strip a 2,5 mm);
- verso la testa i 10 kΩ dei canali 4-7, i 100 nF delle NTC sotto e le quattro piazzole P1.
"""

import math
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', 'script'))

from genera_contorni import kicad  # noqa: E402
from scheda_kicad import Scheda, netlist  # noqa: E402

PASSO = 2.54
# quattro strati, come la basetta: a due resta sempre una rete aperta (prova del 19 ottobre); le due schede si ordinano
# insieme sullo stesso pannello (F7)
STRATI = 4
# sagoma di prova (robot): angolo di testa a +Y smussato per lo spigolo della base a x 75...76, y > 24,5
SAGOMA = [(44.2, 18.6), (78.0, 18.6), (78.0, 25.7), (76.5, 27.2), (44.2, 27.2)]
FORI = [(46.2, 22.75), (76.2, 22.75)]
X_J1, Y_MASSA, Y_SEGNALE = 50.25, 25.29, 20.21

POSTI = {
    'J1': (X_J1, Y_MASSA, 0),
    'R1': (51.0, 22.75, 0), 'R2': (54.4, 22.75, 0), 'R3': (57.8, 22.75, 0), 'R4': (61.2, 22.75, 0),
    'R5': (65.3, 21.0, 90), 'R6': (65.3, 24.5, 90), 'R7': (67.3, 24.5, 90), 'R8': (67.3, 21.0, 90),
    'P1': (69.4, 24.02, 0),
}
SOTTO = {**{'C%d' % (c + 1): (X_J1 + c * PASSO, 22.75, 90) for c in range(6)},
         'C7': (67.3, 22.75, 90), 'C8': (65.3, 22.75, 90)}


def scheda(cartella=QUI):
    s = Scheda(netlist(os.path.join(QUI, 'partitori.kicad_sch'), os.path.join(cartella, 'partitori.net')),
               os.path.join(cartella, 'partitori.kicad_pcb'), strati=STRATI)
    s.contorno([kicad(*p) for p in SAGOMA])
    for x, y in FORI:
        kx, ky = kicad(x, y)
        s.foro(kx, ky, 2.4)
        # sopra la testa M2 (Ø4) piu' 0,5 per lato; sotto la bugna Ø5,5 piu' 0,5 per lato (come genera_contorni)
        for strato, d in (('F.Cu', 5.0), ('B.Cu', 6.5), ('In1.Cu', 3.4), ('In2.Cu', 3.4)):
            s.area_senza_rame('foro_%s_%s' % (x, strato), [strato],
                              [kicad(x + d / 2 * math.cos(a * math.pi / 16), y + d / 2 * math.sin(a * math.pi / 16))
                               for a in range(32)])
    for rif, (x, y, a) in POSTI.items():
        s.piazza(rif, *kicad(x, y), angolo=a)
    for rif, (x, y, a) in SOTTO.items():
        s.piazza(rif, *kicad(x, y), angolo=a, retro=True)
    # serigrafia: sulla scheda c'e' posto solo per il nome, nel tratto di coda accanto al foro; la tabella delle
    # piazzole e dei canali sta nella guida
    for rif in list(s.impronte):
        s.togli_serigrafia(rif)
    s.testo('PARTITORI', *kicad(48.4, 22.9), altezza=0.8, angolo=90)
    s.testo('HEX2 r1', *kicad(48.4, 22.9), strato='B.SilkS', altezza=0.8, angolo=90)
    piste = os.path.join(QUI, 'piste.json')
    if os.path.exists(piste):
        s.piste_da_file(piste, kicad)
        for strato in ('B.Cu', 'F.Cu', 'In1.Cu', 'In2.Cu'):
            s.riempimento('GND', s.contorno_rientrato(0.5), strato, 0.3)
    return s


if __name__ == '__main__':
    cartella = sys.argv[sys.argv.index('-o') + 1] if '-o' in sys.argv else QUI
    print(scheda(cartella).salva())
