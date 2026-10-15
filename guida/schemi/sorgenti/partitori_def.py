"""Striscia dei partitori (X5, X6, X14): componenti, reti, ponticelli e fili esterni (fonte di verita' dei disegni).
Millefori a doppia faccia, passo 2,54: 9 colonne (A-H canali 0-7, I colonna delle viti) per 4 righe.
Per controllarla: python partitori_def.py"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modello import Griglia, Scheda, controlli_vicinanze, h

NCOL, NRIG = 9, 4
GS = Griglia(0.0, 0.0, NCOL, NRIG)          # origine locale: A-1 in (0, 0); la striscia non ha una terna del robot
S = Scheda(GS, 'partitori')
COL = 'ABCDEFGH'
# canale -> (sigla della zampa o della NTC, descrizione). Ordine delle zampe: robot.yaml, proposta [C]
CANALI = ['AS', 'MS', 'PS', 'AD', 'MD', 'PD', 'NTC S', 'NTC D']
VITI = ['I1', 'I4']                           # fori delle due M2 (allargati a 2,4)
LIBERI = ['I2', 'I3']


def nodo(c):
    return 'N%d' % c


for c, L in enumerate(COL):
    S.metti(L + '4', 'R%d' % (c + 1), '2', '3V3')
    S.metti(L + '3', 'R%d' % (c + 1), '1', nodo(c))
    S.metti(L + '2', 'C%d' % (c + 1), '+', nodo(c))
    S.metti(L + '1', 'C%d' % (c + 1), '−', 'GND')
for f in VITI:
    S.metti(f, 'vite', 'M2', None)

# ponticelli del lato saldature: righe 1 (massa) e 4 (3,3 V) lungo A-H, e fra riga 2 e riga 3 di ogni colonna
S.ponte(*[L + '4' for L in COL])
S.ponte(*[L + '1' for L in COL])
for L in COL:
    S.ponte(L + '2', L + '3')

# fili esterni, 30 AWG siliconico (X31), dal lato componenti, dall'alto; numeri da 201
FILI = []     # (n, foro, rete, da, a, nota)
n = 200
for c, L in enumerate(COL):
    z = CANALI[c]
    if c < 6:
        FILI.append((None, L + '2', nodo(c), 'presa %d, polo del segnale' % (c + 1), 'canale %d' % c, 'segnale della zampa %s' % z))
        FILI.append((None, L + '1', 'GND', 'presa %d, polo di massa' % (c + 1), 'massa', 'massa della zampa %s' % z))
    else:
        FILI.append((None, L + '2', nodo(c), z, 'canale %d' % c, 'filo della %s verso l’ingresso' % z))
        FILI.append((None, L + '1', 'GND', z, 'massa', 'filo della %s verso la massa' % z))
    FILI.append((None, L + '2', nodo(c), 'striscia %s-2' % L, 'ADC, ingresso A%d' % c, 'uscita del canale verso l’ADC'))
FILI.append((None, 'A4', '3V3', 'ADC, pin VIN', 'striscia A-4', '3,3 V dei partitori, dalla stessa alimentazione dell’ADC'))
FILI.append((None, 'A1', 'GND', 'ADC, pin GND', 'striscia A-1', 'massa dell’ADC'))
FILI = [(200 + i + 1,) + f[1:] for i, f in enumerate(FILI)]

# valori. R: 10 kΩ 1 % (BOM X5, X14); C: 100 nF (BOM X5; B8 se SMD). C7 e C8: proposta S-30
VALORI = {'R': '10 kΩ 1 %', 'C': '100 nF'}
PROPOSTE = ['C7', 'C8']


def connessione():
    par = {}

    def f(x):
        par.setdefault(x, x)
        while par[x] != x:
            x = par[x]
        return x
    for a, b, r in S.ponti:
        par[f(a)] = f(b)
    reti = {}
    for p, (c, nm, r) in S.pin.items():
        if r:
            reti.setdefault(r, []).append(p)
    ok = True
    for r, ps in reti.items():
        g = {}
        for p in ps:
            g.setdefault(f(p), []).append(p)
        if len(g) > 1:
            ok = False
            print('RETE NON CONNESSA', r, list(g.values()))
    # due reti diverse nello stesso gruppo
    gruppi = {}
    for r, ps in reti.items():
        for p in ps:
            gruppi.setdefault(f(p), set()).add(r)
    for g, rr in gruppi.items():
        if len(rr) > 1:
            ok = False
            print('CORTO FRA RETI', rr)
    for fl in FILI:
        if S.rete(fl[1]) != fl[2]:
            ok = False
            print('FILO SU UN FORO DI UN’ALTRA RETE', fl)
    return ok


def conteggi():
    per = {}
    for fl in FILI:
        per[fl[1]] = per.get(fl[1], 0) + 1
    return per


if __name__ == '__main__':
    print('connessione', connessione())
    err, avv, tutte = controlli_vicinanze(S)
    print('errori', err, 'avvisi', avv)
    print('fili per foro (massimo 2):', {k: v for k, v in conteggi().items() if v > 1})
    assert max(conteggi().values()) <= 2
    print('fili', len(FILI))
    print('coppie vicine di reti diverse (per le prove):')
    for t in tutte:
        print(' ', h(t[0]), t[1], '/', h(t[2]), t[3])
    w, hh = NCOL * 2.54, NRIG * 2.54
    print('striscia %.2f x %.2f mm' % (w, hh))
