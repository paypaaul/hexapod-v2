import os
"""Fili isolati della basetta e instradamento."""
import basetta_def as d
from modello import Router, h
B = d.B
F = B.filo
# massa: stella su Q-4/Q-5 (D24V22F5). Ingresso, LED e logica arrivano con fili separati.
F('S13', 'Q4', 26, 'massa della 2813 → stella')
F('E13', 'G13', 26, 'massa dei LED (poli 3, 5)')
F('G13', 'K13', 26, 'massa dei LED (poli 5, 9 e tibie)')
F('K13', 'Q5', 26, 'massa dei LED → stella')
F('K8', 'Q6', 26, 'massa della logica → stella')
F('Q10', 'Q6', 30, 'masse di R7 e CS1 → stella')
F('A12', 'A8', 26, 'massa dell’ESP32')
F('A8', 'E8', 26, 'massa dell’ESP32 → U3')
F('J7', 'K8', 26, 'masse di U4')
F('E3', 'J4', 30, 'massa della seriale e del bus')
F('E1', 'E3', 30, 'massa del bus (salta E-2)')
F('A1', 'A8', 30, 'massa del bus')
# 5 V
F('R4', 'L8', 26, '5 V del regolatore → PTC')
F('L8', 'E11', 26, '5 V → VCC di U3')
F('E11', 'E4', 26, '5 V → HV di U4')
F('E4', 'D6', 26, '5 V → D1')
F('A6', 'A2', 26, '5 V dopo D1 → pin 5V dell’ESP32')
F('L10', 'B13', 26, '5 V dei LED → poli 1-2 e tibie')
# 3,3 V
B.fili.append(dict(a='T3', b='N3', rete='J1', awg=30, nota='J1: 3V3 dell’ESP32 → 3V3S (si toglie con X3)', fisso=None))
F('M3', 'M1', 30, '3V3S → bus (salta M-2)')
F('M3', 'E7', 30, '3V3S → LV di U4')
F('N3', 'I13', 30, '3V3S → polo 7')
# bus
F('J3', 'J1', 30, 'SCL → bus (salta J-2)')
F('J3', 'H13', 30, 'SCL → polo 6')
F('Q3', 'Q1', 30, 'SDA → bus (salta Q-2)')
F('E12', 'J13', 30, 'SDA (GPIO47) → polo 8')
F('E12', 'Q3', 30, 'SDA → R5')
# segnali
F('D12', 'F7', 30, 'TX3 (GPIO21) → L1')
F('B2', 'H7', 30, 'RX3 (GPIO14) ← L3')
F('F12', 'F8', 30, 'GPIO48 → 1A')
F('F8', 'I8', 30, '1A → 2A')
F('D8', 'F8', 30, 'R1 → 1A')
F('G8', 'L7', 30, '1Y → R2')
F('L4', 'F13', 30, 'R2 → polo 4')
F('J8', 'T13', 30, '2Y → tibie')
F('Q12', 'O13', 30, 'GPIO2 → polo 13')
F('O12', 'Q13', 30, 'GPIO41 → OFF')

def vbat_percorso():
    return [(-1, 0)] + [(i, 0) for i in range(0, 15)] + [(14, 1), (14, 2), (14, 3)]

def instrada_ordine(ordine):
    from modello import aggiorna_domanda
    R = nuovo_router(); falliti = []
    for j, i in enumerate(ordine):
        aggiorna_domanda(R, B.fili, ordine[j + 1:], peso=3.0)
        p = R.instrada(B.fili[i], i)
        B.fili[i]['perc'] = p
        if p is None: falliti.append(i)
    return R, falliti


def instrada(ordine=None):
    ris = {}
    for n in vbat_percorso(): ris[n] = 'VBAT'
    for n in ((15, 3), (15, 4)): ris[n] = 'VBAT'     # angoli di P-4: nessun altro filo
    R = Router(B, imin=-1, imax=20, kmin=0, kmax=13, riservati=ris)
    perc = R.vbat = vbat_percorso()
    for j, n in enumerate(perc):
        R.uso_nodo.setdefault(n, []).append(('VBAT', 'capo' if j in (0, len(perc) - 1) else 'h'))
    for a, b in zip(perc, perc[1:]): R.uso_arco[frozenset({a, b})] = ['VBAT', 'VBAT', 'VBAT']
    idx = list(range(len(B.fili)))
    if ordine: idx = ordine
    falliti = []
    for i in idx:
        f = B.fili[i]
        p = R.instrada(f, i)
        f['perc'] = p
        if p is None: falliti.append(i)
    return R, falliti

def nuovo_router():
    ris = {}
    for n in vbat_percorso(): ris[n] = 'VBAT'
    for n in ((15, 3), (15, 4)): ris[n] = 'VBAT'     # angoli di P-4: nessun altro filo
    R = Router(B, imin=-1, imax=20, kmin=0, kmax=13, riservati=ris)
    perc = R.vbat = vbat_percorso()
    for j, n in enumerate(perc):
        R.uso_nodo.setdefault(n, []).append(('VBAT', 'capo' if j in (0, len(perc) - 1) else 'h'))
    for a, b in zip(perc, perc[1:]): R.uso_arco[frozenset({a, b})] = ['VBAT', 'VBAT', 'VBAT']
    return R


def instrada_rr(giri=3000, seme=1, verbose=False, hist=0.7):
    """Instradamento con strappo e reinstradamento (la storia dei nodi contesi cresce)."""
    import random
    rnd = random.Random(seme)
    g = B.g
    def lung(i):
        (xa, ya), (xb, yb) = g.xy(B.fili[i]['a']), g.xy(B.fili[i]['b'])
        return abs(xa - xb) + abs(ya - yb)
    R = nuovo_router()
    from modello import assegna_capi
    assegna_capi(R, B.fili, riservati=[n for n in R.uso_nodo])
    capi = [f['capi'] for f in B.fili]
    coda = sorted(range(len(B.fili)), key=lung)
    perc = {}
    n = 0
    meglio = None
    import copy
    while coda and n < giri:
        n += 1
        i = coda.pop(0)
        p = R.instrada(B.fili[i], i)
        if p is not None:
            perc[i] = p
        else:
            p, con = R.instrada(B.fili[i], i, forza=True)
            if p is None:
                print('impossibile', i + 1); continue
            for j in con:
                R.togli(j); perc.pop(j, None); coda.append(j)
            for nd in p:
                if R.uso_nodo.get(nd):
                    R.storia[nd] = R.storia.get(nd, 0) + hist
            R.registra(p, i); perc[i] = p
        if meglio is None or len(coda) < meglio[0]:
            meglio = (len(coda), dict(perc), list(coda))
    if coda:
        # riparte dalla situazione migliore e prova i rimasti senza strappare
        _, perc, coda = meglio
        R = nuovo_router()
        R.capi_assegnati = set(n for c in capi for n in c)
        for i, p in perc.items(): R.registra(p, i)
        rimasti = []
        for i in coda:
            p = R.instrada(B.fili[i], i)
            if p is None: rimasti.append(i)
            else: perc[i] = p
        coda = rimasti
    for i, f in enumerate(B.fili):
        f['perc'] = perc.get(i)
    return R, coda, n

def cerca(n=150, seme=1):
    import random, copy
    rnd = random.Random(seme)
    g = B.g
    def lung(i):
        (xa, ya), (xb, yb) = g.xy(B.fili[i]['a']), g.xy(B.fili[i]['b'])
        return abs(xa - xb) + abs(ya - yb)
    base = sorted(range(len(B.fili)), key=lung)
    best = None
    for it in range(n):
        if it == 0: ordine = base
        elif it == 1: ordine = base[::-1]
        else:
            ordine = base[:]
            # mescola un poco l'ordine per lunghezza
            for _ in range(rnd.randint(3, 25)):
                a, b = rnd.randrange(len(ordine)), rnd.randrange(len(ordine))
                ordine[a], ordine[b] = ordine[b], ordine[a]
        R, falliti = instrada(ordine)
        tot = sum(len(f['perc']) for f in B.fili if f['perc'])
        sc = 1000 * len(falliti) + 4 * len(R.incroci()) + 3 * len(R.paralleli()) + tot
        if best is None or sc < best[0]:
            best = (sc, ordine[:], len(falliti), len(R.incroci()), tot, len(R.paralleli()))
    return best

if __name__ == '__main__' and 'rr' in __import__('sys').argv:
    import time
    t = time.time()
    R, coda, n = instrada_rr()
    print('giri', n, 'rimasti', [(i + 1, B.fili[i]['a'], B.fili[i]['b']) for i in coda], 'incroci', len(R.incroci()),
          'paralleli', len(R.paralleli()), 'lung', sum(len(f['perc'] or []) for f in B.fili), time.time() - t)
elif __name__ == '__main__':
    import time, sys
    t = time.time()
    best = cerca(int(sys.argv[1]) if len(sys.argv) > 1 else 60)
    print('migliore', best[0], 'falliti', best[2], 'incroci', best[3], 'lung', best[4], 'paralleli', best[5], 'tempo', time.time() - t)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ordine_b.txt'), 'w').write(repr(best[1]))
    R, falliti = instrada(best[1])
    for i in falliti: print('FALLITO', i + 1, B.fili[i]['a'], B.fili[i]['b'], B.fili[i]['rete'])
