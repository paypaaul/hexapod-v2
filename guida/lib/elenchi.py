"""Pezzi necessari per passo e per sezione (D-075): si calcolano dai passi e dal catalogo, non si scrivono a mano.

Le quantita' di una sezione ripetuta (la zampa, ripeti: 6) sono per una ripetizione; il totale si moltiplica.
"""
import fnmatch
from collections import Counter

from . import fori as F
from . import scena as S


def _attrezzo_vite(dati, tipo):
    return dati.viteria['viti'][tipo].get('attrezzo')


def passo(dati, sez, p, presenti):
    """{'pezzi': [(componente, qta)], 'viti': Counter, 'rondelle': Counter, 'distanziali': Counter, 'inserti': Counter,
    'extra': [...], 'attrezzi': [chiavi]} del passo, con i pezzi nell'ordine in cui il passo li cita."""
    s = sez['sezione']
    terna, istanza = s.get('terna', 'zampa'), s.get('istanza', 'AS')
    nuovi, assiemi = S.entrano(dati, p)
    nuovi = [c for c in nuovi if c not in presenti]
    pezzi = Counter()
    for k in nuovi:
        pezzi[dati.occ[k]['componente']] += 1
    viti, rondelle, distanziali, inserti = Counter(), Counter(), Counter(), Counter()
    attrezzi = []
    tutti = list(dict.fromkeys(list(presenti) + nuovi + assiemi))
    for gj in p.get('giunzioni', []):
        nome = gj['id'] if isinstance(gj, dict) else gj
        assieme = 'zampa' if nome in dati.giunzioni['zampa'] else 'corpo'
        for v in F.piazza(dati, nome, dati.giunzioni[assieme][nome], tutti, terna, istanza):
            viti[v['vite']] += 1
            rondelle.update({'R_M3': len(v['rondelle'])} if v['rondelle'] else {})
            if v.get('distanziale'):
                distanziali[v['distanziale']['tipo']] += 1
            attrezzi.append(_attrezzo_vite(dati, v['vite']))
    for sel in p.get('inserti', []):
        for k in dati.chiavi(sel['chiave']):
            for f in F.fori_di(dati, k, terna, istanza):
                if f['tipo'].startswith('inserto') and fnmatch.fnmatchcase(f['lav'] or '', sel.get('lav', '*')):
                    inserti['INS_M3' if f['tipo'] == 'inserto_m3' else 'INS_M2'] += 1
    if inserti:
        attrezzi.append('saldatore_inserti')
    attrezzi += p.get('attrezzi', [])
    extra = [{'nome': a['nome'], 'qta': 1} for a in p.get('assiemi', [])] + p.get('extra', [])
    return {'pezzi': list(pezzi.items()), 'viti': viti, 'rondelle': rondelle, 'distanziali': distanziali,
            'inserti': inserti, 'extra': extra, 'attrezzi': [a for a in dict.fromkeys(attrezzi) if a]}


def sezione(dati, sez, per_passo):
    """Somma dei passi della sezione (per una ripetizione) e attrezzi in ordine di comparsa."""
    tot = {'pezzi': Counter(), 'viti': Counter(), 'rondelle': Counter(), 'distanziali': Counter(), 'inserti': Counter(),
           'extra': [], 'attrezzi': []}
    for e in per_passo:
        for c, n in e['pezzi']:
            tot['pezzi'][c] += n
        for k in ('viti', 'rondelle', 'distanziali', 'inserti'):
            tot[k].update(e[k])
        tot['extra'] += e['extra']
        tot['attrezzi'] += [a for a in e['attrezzi'] if a not in tot['attrezzi']]
    tot['attrezzi'] += [a for a in sez['sezione'].get('attrezzi', []) if a not in tot['attrezzi']]
    return tot
