import os
import sys, ast
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def connessione(S, alias=None):
    par = {}
    def f(x):
        par.setdefault(x, x)
        while par[x] != x: x = par[x]
        return x
    def u(a, b): par[f(a)] = f(b)
    for a, b, r in S.ponti: u(a, b)
    for w in S.fili:
        if w['b']: u(w['a'], w['b'])
    reti = {}
    for p, (c, n, r) in S.pin.items():
        if r and p not in S.nosald and r not in ('H_NC', 'L_NC', 'LO'):
            reti.setdefault((alias or {}).get(r, r), []).append(p)
    ok = True
    for r, ps in reti.items():
        g = {}
        for p in ps: g.setdefault(f(p), []).append(p)
        if len(g) > 1:
            ok = False; print('RETE NON CONNESSA', r, list(g.values()))
    # archi fra reti diverse
    for w in S.fili:
        if w['b'] and S.rete(w['a']) != S.rete(w['b']) and w['rete'] != 'J1':
            ok = False; print('FILO FRA RETI', w)
    for a, b, r in S.ponti:
        if S.rete(a) != S.rete(b): ok = False; print('PONTE FRA RETI', a, b)
    return ok
import basetta_def, scheda_def, fili_b
print('basetta', connessione(basetta_def.B, {'3V3_ESP': '3V3S'}))
print('scheda', connessione(scheda_def.S))
