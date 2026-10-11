"""Pezzi necessari per passo e per sezione (D-075): si calcolano dai passi e dal catalogo, non si scrivono a mano.

Le quantita' di una sezione ripetuta (la zampa, ripeti: 6) sono per una ripetizione; il totale si moltiplica.
"""
from collections import Counter

from . import fori as F
from . import scena as S


def _attrezzo_vite(dati, tipo):
    return dati.viteria['viti'][tipo].get('attrezzo')


def passo(dati, sez, p, presenti):
    """{'pezzi': [(componente, qta)], 'viti': Counter, 'rondelle': Counter, 'distanziali': Counter, 'inserti': Counter,
    'extra': [...], 'attrezzi': [chiavi]} del passo, con i pezzi nell'ordine in cui il passo li cita."""
    terna, istanza = S.terna_di(sez, p)
    nuovi, assiemi = S.entrano(dati, p)
    nuovi = [c for c in nuovi if c not in presenti]
    pezzi = Counter()
    for k in nuovi:
        pezzi[dati.occ[k]['componente']] += 1
    viti, rondelle, distanziali, inserti = Counter(), Counter(), Counter(), Counter()
    attrezzi = []
    pieni = [c for k in p.get('in_evidenza', []) for c in dati.chiavi(k)]
    tutti = list(dict.fromkeys(list(presenti) + nuovi + assiemi + pieni))
    for gj in p.get('giunzioni', []):
        nome = gj['id'] if isinstance(gj, dict) else gj
        assieme = 'zampa' if nome in dati.giunzioni['zampa'] else 'corpo'
        for v in F.piazza(dati, nome, dati.giunzioni[assieme][nome], tutti, terna, istanza):
            attrezzi.append(_attrezzo_vite(dati, v['vite']))
            if isinstance(gj, dict) and gj.get('stringi'):      # viti gia' contate dove sono state messe
                continue
            viti[v['vite']] += 1
            rondelle.update({'R_M3': len(v['rondelle'])} if v['rondelle'] else {})
            if v.get('distanziale'):
                distanziali[v['distanziale']['tipo']] += 1
    for sel in p.get('inserti', []):
        for f in F.inserti_scelti(dati, sel, terna, istanza):
            inserti['INS_M3' if f['tipo'] == 'inserto_m3' else 'INS_M2'] += 1
    if inserti:
        attrezzi.append('saldatore_inserti')
    attrezzi += p.get('attrezzi', [])
    extra = [{'nome': a['nome'], 'qta': 1} for a in p.get('assiemi', [])] + p.get('extra', [])
    return {'pezzi': list(pezzi.items()), 'viti': viti, 'rondelle': rondelle, 'distanziali': distanziali,
            'inserti': inserti, 'extra': extra, 'attrezzi': [a for a in dict.fromkeys(attrezzi) if a]}


def sezione(dati, sez, per_passo):
    """Somma dei passi della sezione (per una ripetizione) e attrezzi in ordine di comparsa. Un passo con volte: N
    conta N volte (il riquadro del passo mostra le quantita' di una volta, il totale della sezione tutte)."""
    tot = {'pezzi': Counter(), 'viti': Counter(), 'rondelle': Counter(), 'distanziali': Counter(), 'inserti': Counter(),
           'extra': [], 'attrezzi': []}
    for p, e in zip(sez['passi'], per_passo):
        v = p.get('volte') or 1
        for c, n in e['pezzi']:
            tot['pezzi'][c] += n * v
        for k in ('viti', 'rondelle', 'distanziali', 'inserti'):
            for t, n in e[k].items():
                tot[k][t] += n * v
        for x in e['extra']:                        # la stessa cosa in piu' passi: una riga sola, quantita' sommate
            q = x.get('qta', 1)
            q = q * v if isinstance(q, (int, float)) else q
            gia = next((y for y in tot['extra'] if y['nome'] == x['nome']), None)
            if gia and isinstance(gia.get('qta', 1), (int, float)) and isinstance(q, (int, float)):
                gia['qta'] = gia.get('qta', 1) + q
            elif not gia:
                tot['extra'].append(dict(x, qta=q))
        tot['attrezzi'] += [a for a in e['attrezzi'] if a not in tot['attrezzi']]
    tot['attrezzi'] += [a for a in sez['sezione'].get('attrezzi', []) if a not in tot['attrezzi']]
    return tot
