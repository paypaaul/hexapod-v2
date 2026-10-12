import os
"""Scheda del carapace (X2), seconda versione."""
import math
from modello import Griglia, Scheda, Router, h

GS = Griglia(31.88, 12.7, 7, 11)
SCH = dict(x0=29.5, x1=49.5, y0=-15.0, y1=15.0)
VITI = [(32.0, 12.5), (47.0, 12.5), (32.0, -12.5), (47.0, -12.5)]   # fori.json ins_sch_a..d
R_BUGNA = 2.75     # bugne Ø 5,5 (cad/script/corpo.py:1085)
S = Scheda(GS, 'carapace')
for x, y in VITI:
    S.zone.append((x, y, R_BUGNA, R_BUGNA + 0.9, R_BUGNA + 0.6, 'bugna'))
for f in GS.fori():
    x, y = GS.xy(f)
    for zx, zy, rc, rf, rw, t in S.zone:
        if math.hypot(x - zx, y - zy) < rf:
            S.vietati[f] = t

NOMI_POLI = {1: '+5 V', 2: '+5 V', 3: 'GND', 4: 'DATO LED', 5: 'GND', 6: 'SCL', 7: '+3,3 V', 8: 'SDA', 9: 'GND',
             10: 'BCLK', 11: 'WS', 12: 'MIC', 13: 'AMP', 14: 'riserva', 15: 'PULS A', 16: 'PULS B'}
RETE_POLO = {1: '5V', 2: '5V', 3: 'GND', 4: 'DATA', 5: 'GND', 6: 'SCL', 7: '3V3', 8: 'SDA', 9: 'GND', 10: 'BCLK',
             11: 'WS', 12: 'MIC', 13: 'AMP', 14: None, 15: 'BTN_A', 16: 'BTN_B'}
TESTATA = {}
for polo in range(1, 17):
    f = ('D' if polo % 2 else 'E') + str(2 + (polo - 1) // 2)
    S.metti(f, 'J2', str(polo), RETE_POLO[polo]); TESTATA[polo] = f

CE1 = ('CE1', '470 µF 10 V', 'A9', 'B9')
S.metti('A9', 'CE1', '+', '5V'); S.metti('B9', 'CE1', '−', 'GND')
CE1_BOX = (30.0, -6.3, 36.3, 4.7)

MOD = {}
def mod(f, rete, testo, n):
    if f in S.pin:
        c, nm, r = S.pin[f]
        assert r == rete
    else:
        S.metti(f, 'filo', testo, rete)
    MOD[f] = (rete, testo, n)

mod('A3', 'GND', 'GND ToF posteriore e Qwiic', 2)
mod('B3', '3V3', '+3,3 V ToF posteriore e Qwiic', 2)
mod('A4', 'SDA', 'SDA ToF posteriore e Qwiic', 2)
mod('B4', 'SCL', 'SCL ToF posteriore e Qwiic', 2)
mod('A9', '5V', '+5 V catena LED (con il + di CE1)', 1)
mod('B9', 'GND', 'massa catena LED (con il − di CE1)', 1)
mod('G3', '5V', 'VIN dell’amplificatore', 1)
mod('G4', 'GND', 'massa dei microfoni e dell’ampli', 2)
mod('G5', '3V3', '+3,3 V dei microfoni', 1)
mod('G6', 'BCLK', 'BCLK microfoni (SCK) e ampli', 2)
mod('G7', 'MIC', 'SD dei microfoni (R8 al microfono)', 1)
mod('G8', 'WS', 'WS microfoni e LRC ampli', 2)
mod('G9', 'AMP', 'DIN dell’amplificatore', 1)

# fili saldati sul lato saldature, direttamente sul pin della testata (sotto la scatola non ci sono fori liberi)
DIRETTI = {'E3': ('DATA', 'DIN del primo pixel dell’anello', 30), 'D9': ('BTN_A', 'pulsante, contatto 1', 26),
           'E9': ('BTN_B', 'pulsante, contatto 2', 26)}
S.ponte('D2', 'E2')                      # +5 V, poli 1 e 2
S.ponte('D3', 'D4')                      # massa, poli 3 e 5
S.ponte('E6', 'F6', 'G6')                # BCLK, polo 10
S.ponte('E7', 'F7', 'G7')                # MIC, polo 12

F = S.filo
F('D2', 'A9', 26, '+5 V → catena LED e CE1')
F('E2', 'G3', 30, '+5 V → ampli')
F('D4', 'B9', 26, 'massa → catena LED e CE1')
F('D6', 'G4', 30, 'massa → microfoni e ampli')
F('D4', 'D6', 30, 'massa: polo 9 con i poli 3 e 5')
F('D3', 'A3', 30, 'massa → ToF e Qwiic')
F('D5', 'B3', 30, '+3,3 V → ToF e Qwiic')
F('D5', 'G5', 30, '+3,3 V → microfoni')
F('E4', 'B4', 30, 'SCL')
F('E5', 'A4', 30, 'SDA')
F('D7', 'G8', 30, 'WS')
F('D8', 'G9', 30, 'dati verso l’ampli')
# fili dei moduli saldati sul pin della testata: escono dal bordo verso l'ottagono (colonna di angoli i = -1)
for f, (r, t, awg) in DIRETTI.items():
    S.fili.append(dict(a=f, b=None, rete=r, awg=awg, nota=t, fisso=None, diretto=True,
                       dest_nodi=[(-1, k) for k in range(2, 10)]))


def nuovo_router():
    return Router(S, imin=-1, imax=6, kmin=0, kmax=11)


def instrada_ordine(ordine):
    from modello import aggiorna_domanda
    R = nuovo_router(); falliti = []
    for j, i in enumerate(ordine):
        aggiorna_domanda(R, S.fili, ordine[j + 1:], peso=3.0)
        p = R.instrada(S.fili[i], i)
        S.fili[i]['perc'] = p
        if p is None:
            falliti.append(i)
    return R, falliti


def cerca(n=300, seme=5):
    import random
    rnd = random.Random(seme)
    base = list(range(len(S.fili)))
    best = None
    for it in range(n):
        o = base[:]
        rnd.shuffle(o)
        R, fail = instrada_ordine(o)
        tot = sum(len(f['perc']) for f in S.fili if f['perc'])
        sc = 1000 * len(fail) + 6 * len(R.incroci()) + 3 * len(R.paralleli()) + tot
        if best is None or sc < best[0]:
            best = (sc, o, len(fail), len(R.incroci()), len(R.paralleli()), tot)
    return best


if __name__ == '__main__':
    from modello import controlli_vicinanze
    print('vietati', sorted(S.vietati))
    e, a, t = controlli_vicinanze(S)
    for x in e:
        if S.pin[x[1][0]][0] != S.pin[x[1][2]][0]:
            print('ERR', x)
    for x in t: print(x)
    b = cerca()
    print(b[0], b[2:])
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ordine_s.txt'), 'w').write(repr(b[1]))
