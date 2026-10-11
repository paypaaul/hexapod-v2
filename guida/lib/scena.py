"""Dal passo YAML al lavoro per Blender (D-075): pezzi presenti e nuovi, esplosi, viti, inserti, frecce.

Il lavoro e' un dizionario JSON senza riferimenti al catalogo: Blender non legge YAML. Le misure sono in mm, nella
terna della sezione ('zampa' come costruita, oppure 'robot').
"""
import fnmatch
import os

import yaml

from . import fori as F
from . import geom


def _viste(dati):
    with open(os.path.join(dati.radice, 'catalogo', 'viste.yaml'), encoding='utf-8') as f:
        return yaml.safe_load(f)


def _stile(dati):
    with open(os.path.join(dati.radice, 'catalogo', 'stile.yaml'), encoding='utf-8') as f:
        return yaml.safe_load(f)


def stati(dati, sez):
    """[(passo, presenti prima del passo)] lungo la sezione: i pezzi nuovi restano montati nei passi dopo."""
    presenti = list(sez['sezione'].get('presenti_iniziali', []))
    out = []
    for p in sez['passi']:
        out.append((p, list(presenti)))
        for k in p.get('nuovi', []):
            for c in dati.chiavi(k):
                if c not in presenti:
                    presenti.append(c)
    return out


def _colore(dati, stile, chiave):
    nome, rgb = dati.componente(chiave)['aspetti'][0]
    return stile['colori'].get(nome, rgb)


def _esploso(passo, chiave):
    e = passo.get('esploso') or {}
    per = e.get('pezzi', {})
    for modello, v in per.items():
        if fnmatch.fnmatchcase(chiave, modello):
            return v
    if 'asse' in e:
        return geom.scala(geom.unit(e['asse']), e.get('distanza', 40))
    return [0.0, 0.0, 0.0]


def _centro(dati, chiave, terna, istanza):
    lo, hi = dati.componente(chiave)['bbox']
    return geom.punto(dati.matrice(chiave, terna, istanza), [(lo[i] + hi[i]) / 2 for i in range(3)])


def lavoro(dati, sez, passo, presenti, uscita):
    s = sez['sezione']
    terna, istanza = s.get('terna', 'zampa'), s.get('istanza', 'AS')
    stile, viste = _stile(dati), _viste(dati)
    nuovi = [c for k in passo.get('nuovi', []) for c in dati.chiavi(k)]
    visibili = list(presenti) + [k for k in nuovi if k not in presenti]
    if 'mostra' in passo:
        visibili = [c for k in passo['mostra'] for c in dati.chiavi(k)] + nuovi
    nascosti = {c for k in passo.get('nascondi', []) for c in dati.chiavi(k)}
    oggetti, frecce = [], []
    for k in visibili:
        if k in nascosti or dati.occ[k]['componente'].startswith('Ingombro_'):
            continue
        nuovo = k in nuovi
        d = _esploso(passo, k) if nuovo else [0.0, 0.0, 0.0]
        m = dati.matrice(k, terna, istanza)
        oggetti.append({'chiave': k, 'mesh': dati.componente(k)['mesh'], 'matrice': geom.componi(geom.traslazione(d), m),
                        'ruolo': 'nuovo' if nuovo else 'vecchio', 'colore': _colore(dati, stile, k)})
        if nuovo and geom.norma(d) > 1:
            c = _centro(dati, k, terna, istanza)
            frecce.append({'da': geom.add(c, d), 'a': c})
    viti = []
    tutti = list(dict.fromkeys(visibili))
    for gj in passo.get('giunzioni', []):
        nome = gj['id'] if isinstance(gj, dict) else gj
        assieme = 'zampa' if nome in dati.giunzioni['zampa'] else 'corpo'
        for v in F.piazza(dati, nome, dati.giunzioni[assieme][nome], tutti, terna, istanza):
            spec = dati.viteria['viti'][v['vite']]
            dist = (gj.get('esploso', 1.5 * spec['l'] + 6) if isinstance(gj, dict) else 1.5 * spec['l'] + 6)
            spost = geom.scala(v['asse'], -dist)
            if v['chiave_testa'] in nuovi:          # la vite segue il pezzo esploso su cui sta la testa
                spost = geom.add(spost, _esploso(passo, v['chiave_testa']))
            viti.append({'tipo': v['vite'], 'testa': geom.add(v['testa'], spost), 'asse': v['asse'], 'l': spec['l'],
                         'd': spec['d'], 'testa_d': spec['testa_d'], 'testa_k': spec['testa_k'], 'forma': spec['testa'],
                         'rondelle': [{'centro': geom.add(r['centro'], geom.scala(spost, 0.5)), 'asse': v['asse']}
                                      for r in v['rondelle']]})
            arrivo = geom.add(v['testa'], _esploso(passo, v['chiave_testa'])) if v['chiave_testa'] in nuovi else v['testa']
            frecce.append({'da': geom.add(v['testa'], spost), 'a': arrivo, 'vite': True})
    inserti = []
    for sel in passo.get('inserti', []):
        for k in dati.chiavi(sel['chiave']):
            for f in F.fori_di(dati, k, terna, istanza):
                if f['tipo'].startswith('inserto') and fnmatch.fnmatchcase(f['lav'] or '', sel.get('lav', '*')):
                    spec = dati.viteria['inserti']['INS_M3' if f['tipo'] == 'inserto_m3' else 'INS_M2']
                    ingresso = f['p0'] if f['e1'] == 'fondo' else f['p1']
                    asse = geom.unit(geom.sub(f['p1'], f['p0']) if f['e1'] == 'fondo' else geom.sub(f['p0'], f['p1']))
                    inserti.append({'centro': geom.add(ingresso, geom.scala(asse, -8)), 'asse': asse, 'd': spec['d'], 'l': spec['l']})
                    frecce.append({'da': geom.add(ingresso, geom.scala(asse, -8)), 'a': ingresso, 'vite': True})
    vista = passo.get('vista', 'zampa_A' if terna == 'zampa' else 'corpo_alto')
    vista = viste[vista] if isinstance(vista, str) else vista
    return {'id': passo['id'], 'uscita': uscita, 'oggetti': oggetti, 'viti': viti, 'inserti': inserti, 'frecce': frecce,
            'camera': vista, 'colori': {k: stile[k] for k in ('viti', 'inserti', 'rondelle', 'distanziali')},
            'attenuato': stile['attenuato']}
