"""PCB-C, scheda del carapace: contorno dal CAD, piazzamento (F4) e sbroglio da script (piano-pcb.md 4.2; D-082).

Gira con il Python di KiCad. Le quote sono nella terna del robot (X avanti, Y a sinistra) e si portano in KiCad con
genera_contorni.kicad. I componenti stanno sotto la scheda (lato B); la si guarda dall'alto del robot.

Disposizione (revisione del 18 ottobre: la prima non si sbrogliava):
- J2 sul bordo di coda: poli dispari a x 42,73 (fila lato chiave, S-26), pari a x 40,19, polo 1 a +Y;
- P1, una piazzola per polo dispari a x 45,6, alla stessa altezza: piste dritte;
- P2, una piazzola per polo pari a x 49,0, mezzo passo piu' in basso: la pista passa fra due poli dispari;
- CE1 nell'ala +Y (5V a destra del foro della vite, massa dal riempimento), pulsante nell'ala -Y, raggiunto passando
  sopra e sotto i fori delle viti (S-10).
"""

import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', 'script'))

from genera_contorni import kicad  # noqa: E402
from scheda_kicad import Scheda, netlist  # noqa: E402

PASSO = 2.54
J2_DISPARI, J2_PARI, J2_Y1 = 29.5 + 8.85 + 4.38, 29.5 + 8.85 + 4.38 - PASSO, 8.89
X_P1, X_P2 = 45.6, 49.0
LARGHEZZE = {'5V': 0.6, '3V3': 0.5, 'GND': 0.4}
ANGOLO_P3 = 270


def y_polo(n):
    """Y del polo n di J2 (righe da 8,89 verso -Y, dispari e pari sulla stessa riga)."""
    return J2_Y1 - ((n - 1) // 2) * PASSO


def scheda(cartella=QUI):
    s = Scheda(netlist(os.path.join(QUI, 'carapace.kicad_sch'), os.path.join(cartella, 'carapace.net')),
               os.path.join(cartella, 'carapace.kicad_pcb'))
    s.contorni_dal_cad('carapace')

    def piazza(rif, x, y, angolo=0):
        # sul lato B KiCad ribalta specchiando la Y: con 180 gradi in piu' la X e' specchiata, cioe' la scheda vista
        # dall'alto del robot con le file che scendono verso -Y dal pad 1
        s.piazza(rif, *kicad(x, y), angolo=angolo + 180, retro=True)

    piazza('J2', J2_DISPARI, J2_Y1)
    piazza('P1', X_P1, y_polo(1))
    piazza('P2', X_P2, y_polo(2) - PASSO / 2)
    piazza('P3', 49.54, -17.0, ANGOLO_P3)   # pulsante: BTN_A a destra (x 49,54), BTN_B a sinistra (x 47,0)
    piazza('CE1', 49.5, 19.5)             # + a destra (x 49,5), massa a sinistra (x 47,0)

    def pista(rete, punti, strato='F.Cu'):
        nome = s.rete(rete).GetNetname().lstrip('/')
        s.pista(rete, [p if isinstance(p[0], str) else kicad(*p) for p in punti],
                LARGHEZZE.get(nome, 0.25), strato)

    # poli dispari -> P1, dritti (il polo 15 e' il pulsante: va nell'ala -Y)
    for k, polo in enumerate((1, 3, 5, 7, 9, 11, 13), 1):
        pista(s.impronte['J2'].FindPadByNumber(str(polo)).GetNetname(), [('J2', polo), ('P1', k)])
    # 5V: il polo 2 sul polo 1, poi la seconda piazzola del 5V
    pista('5V', [('J2', 2), ('J2', 1)])
    pista('5V', [('P1', 1), ('P2', 1)])
    # poli pari -> P2: fra i poli dispari, mezzo passo sotto
    for k, polo in enumerate((4, 6, 8, 10, 12), 2):
        y = y_polo(polo) - PASSO / 2
        pista(s.impronte['J2'].FindPadByNumber(str(polo)).GetNetname(),
              [('J2', polo), (J2_PARI + PASSO / 2, y), ('P2', k)])
    # seconda piazzola del 3V3 (P1.8) sotto, sul lato B, fra le due colonne
    pista('3V3', [('P1', 4), (47.3, y_polo(7) - 0.6), (47.3, y_polo(15) + 0.6), ('P1', 8)], 'B.Cu')
    # 5V a CE1: a destra del foro della vite (48; 12,5)
    pista('5V', [('P2', 1), (50.0, y_polo(2) - PASSO / 2 + 1.0), (50.0, 18.3), ('CE1', 1)])
    # pulsante: sopra e sotto i fori delle viti (41,5; -12,5) e (48; -12,5)
    pista('BTN_A', [('J2', 15), (J2_DISPARI, -10.5), (49.9, -10.5), (49.9, -16.0), ('P3', 1)])
    pista('BTN_B', [('J2', 16), (39.4, -9.7), (39.4, -14.35), (47.0, -14.35), ('P3', 2)])
    # massa: riempimento sul lato B; le masse dei poli sono gia' collegate dalle piste, CE1 con una pista verso il
    # riempimento (sul lato F il riempimento restava a isole fra le piste)
    pista('GND', [('CE1', 2), (47.0, 16.3)], 'B.Cu')
    s.riempimento('GND', s.contorno_rientrato(0.5), 'B.Cu', 0.3)
    # serigrafia: i contorni di J2 e CE1 escono dal bordo e i riferimenti delle piazzole non servono (vanno su Fab)
    for rif in ('J2', 'CE1', 'P1', 'P2', 'P3'):
        s.togli_serigrafia(rif)
    # legenda sul lato F (dove si saldano i fili), sopra la scatola di J2, allineata alle righe delle piazzole
    s.testo('P1', *kicad(31.6, J2_Y1 + 1.5), altezza=0.8)
    s.testo('P2', *kicad(35.6, J2_Y1 + 1.5), altezza=0.8)
    for k, rete in enumerate(['5V', 'GND', 'GND', '3V3', 'GND', 'WS', 'AMP', '3V3'], 1):
        s.testo(rete, *kicad(31.6, y_polo(2 * k - 1)), altezza=0.8)
    for k, rete in enumerate(['5V', 'DATA', 'SCL', 'SDA', 'BCLK', 'MIC'], 1):
        s.testo(rete, *kicad(35.6, y_polo(2) - PASSO / 2 - (k - 1) * PASSO), altezza=0.8)
    s.testo('HEX2 CARAPACE r1 - fili da sotto', *kicad(38.6, 0.0), altezza=0.8, angolo=90)
    s.testo('B   A', *kicad(48.27, -19.2), altezza=0.8)
    s.testo('+', *kicad(49.5, 21.5), altezza=1.0)
    return s


if __name__ == '__main__':
    cartella = sys.argv[sys.argv.index('-o') + 1] if '-o' in sys.argv else QUI
    print(scheda(cartella).salva())
