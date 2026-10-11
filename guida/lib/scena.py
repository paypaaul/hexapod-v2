"""Dal passo YAML al lavoro per Blender (D-075): pezzi presenti e nuovi, esplosi, viti, inserti, frecce.

Il lavoro e' un dizionario JSON senza riferimenti al catalogo: Blender non legge YAML. Le misure sono in mm, nella
terna della sezione ('zampa' come costruita, oppure 'robot').
"""
import fnmatch
import json
import os
import sys

import yaml

from . import fori as F
from . import geom


# Spazio dell'immagine nella pagina A4 orizzontale (mm) per formato del passo, e densita' del render: 9 px/mm sono
# circa 230 dpi, abbastanza per i contorni Freestyle da 1,2 px senza file enormi (prova F0: 96 colori, PNG piatti).
FORMATI = {'grande': (196, 172), 'mezzo': (131, 104), 'finale': (196, 150)}
PX_MM = 9
MINIATURA = (480, 400)


def risoluzione(formato):
    w, h = FORMATI[formato]
    return [w * PX_MM, h * PX_MM]


def _zone(dati):
    """Indice delle zone esportate da esporta_guida.py: {componente: {lavorazione: triangoli}}."""
    p = os.path.join(os.path.dirname(dati.radice), 'build', 'guida', 'cad', 'zone', 'indice.json')
    if not os.path.exists(p):
        return {}
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def _viste(dati):
    with open(os.path.join(dati.radice, 'catalogo', 'viste.yaml'), encoding='utf-8') as f:
        return yaml.safe_load(f)


def _stile(dati):
    with open(os.path.join(dati.radice, 'catalogo', 'stile.yaml'), encoding='utf-8') as f:
        return yaml.safe_load(f)


def chiavi_assieme(dati, a):
    """Pezzi di un sottoassieme gia' montato che entra nel passo: {chiavi: glob, esclusi: [glob], nome}."""
    fuori = {c for k in a.get('esclusi', []) for c in dati.chiavi(k)}
    return [c for c in dati.chiavi(a['chiavi']) if c not in fuori and not dati.occ[c]['componente'].startswith('Ingombro_')]


def entrano(dati, passo):
    """(pezzi nuovi, pezzi dei sottoassiemi) del passo, in ordine."""
    nuovi = [c for k in passo.get('nuovi', []) for c in dati.chiavi(k)]
    assiemi = [c for a in passo.get('assiemi', []) for c in chiavi_assieme(dati, a)]
    return nuovi, assiemi


def stati(dati, sez):
    """[(passo, presenti prima del passo)] lungo la sezione: i pezzi nuovi restano montati nei passi dopo."""
    presenti = [c for k in sez['sezione'].get('presenti_iniziali', []) for c in dati.chiavi(k)]
    out = []
    for p in sez['passi']:
        out.append((p, list(presenti)))
        nuovi, assiemi = entrano(dati, p)
        for c in nuovi + assiemi:
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


def terna_di(sez, passo):
    """(terna, istanza) del passo: quelle della sezione, salvo che il passo le dia (es. gli inserti, pezzo per pezzo)."""
    s = sez['sezione']
    return passo.get('terna', s.get('terna', 'zampa')), passo.get('istanza', s.get('istanza', 'AS'))


def ha_render(passo):
    """Il passo ha un'immagine del CAD: no se e' solo testo (immagine: false) o se la figura viene da un file."""
    return passo.get('immagine', True) is not False and 'figura' not in passo and 'genera' not in passo


def lavoro(dati, sez, passo, presenti, uscita):
    """Il lavoro per Blender di un passo; con posa: {alfa, gamma, coxa} la zampa e' disegnata in quella posa."""
    dati.posa = dati.matrici_posa(passo.get('posa'))
    try:
        return _lavoro(dati, sez, passo, presenti, uscita)
    finally:
        dati.posa = None


def _lavoro(dati, sez, passo, presenti, uscita):
    terna, istanza = terna_di(sez, passo)
    stile, viste = _stile(dati), _viste(dati)
    nuovi, assiemi = entrano(dati, passo)
    pieni = [c for k in passo.get('in_evidenza', []) for c in dati.chiavi(k)]   # a colori pieni, ma non si montano
    nuovi = nuovi + assiemi + [c for c in pieni if c not in nuovi]
    visibili = list(presenti) + [k for k in nuovi if k not in presenti]
    if 'mostra' in passo:
        visibili = [c for k in passo['mostra'] for c in dati.chiavi(k)] + [c for c in nuovi]
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
        if nuovo and geom.norma(d) > 1 and k not in assiemi and k not in pieni:
            c = _centro(dati, k, terna, istanza)
            frecce.append({'da': geom.add(c, d), 'a': c, 'tipo': 'pezzo', 'chiavi': [k]})
    for a in passo.get('assiemi', []):                 # una freccia sola per sottoassieme
        gruppo = [k for k in chiavi_assieme(dati, a) if k not in nascosti]
        d = _esploso(passo, gruppo[0]) if gruppo else [0.0, 0.0, 0.0]
        if gruppo and geom.norma(d) > 1:
            centri = [_centro(dati, k, terna, istanza) for k in gruppo]
            c = geom.scala([sum(x[i] for x in centri) for i in range(3)], 1 / len(centri))
            frecce.append({'da': geom.add(c, d), 'a': c, 'tipo': 'pezzo', 'chiavi': gruppo})
    for z in passo.get('evidenzia', []):            # sedi e percorsi di quello che il CAD non ha (striscia, fili)
        trovate = 0
        for k in dati.chiavi(z['chiave']):
            comp = dati.occ[k]['componente']
            for lav in sorted((_zone(dati).get(comp) or {})):
                if fnmatch.fnmatchcase(lav, z['lav']):
                    d = _esploso(passo, k) if k in nuovi else [0.0, 0.0, 0.0]
                    oggetti.append({'chiave': '%s:%s' % (k, lav), 'mesh': '../zone/%s__%s.ply' % (comp, lav.replace(':', '-')),
                                    'matrice': geom.componi(geom.traslazione(d), dati.matrice(k, terna, istanza)),
                                    'ruolo': 'zona', 'colore': stile['evidenzia']})
                    trovate += 1
        if not trovate:                             # la zona si aggiunge in zone.yaml e si esporta da Fusion
            print('avviso: %s: evidenzia %s %s non trova zone esportate (guida/catalogo/zone.yaml, esporta_guida.py '
                  'zone)' % (passo['id'], z['chiave'], z['lav']), file=sys.stderr)
    viti = []
    tutti = list(dict.fromkeys(visibili))
    for gj in passo.get('giunzioni', []):
        nome = gj['id'] if isinstance(gj, dict) else gj
        assieme = 'zampa' if nome in dati.giunzioni['zampa'] else 'corpo'
        stringi = isinstance(gj, dict) and gj.get('stringi')
        for v in F.piazza(dati, nome, dati.giunzioni[assieme][nome], tutti, terna, istanza):
            spec = dati.viteria['viti'][v['vite']]
            dist = (gj.get('esploso', 1.5 * spec['l'] + 6) if isinstance(gj, dict) else 1.5 * spec['l'] + 6)
            if stringi:                             # viti gia' messe in un passo prima: al loro posto, senza freccia
                dist = 0
            spost = geom.scala(v['asse'], -dist)
            if v['chiave_testa'] in nuovi:          # la vite segue il pezzo esploso su cui sta la testa
                spost = geom.add(spost, _esploso(passo, v['chiave_testa']))
            viti.append({'tipo': v['vite'], 'testa': geom.add(v['testa'], spost), 'asse': v['asse'], 'l': spec['l'],
                         'd': spec['d'], 'testa_d': spec['testa_d'], 'testa_k': spec['testa_k'], 'forma': spec['testa'],
                         'rondelle': [{'centro': geom.add(r['centro'], geom.scala(spost, 0.5)), 'asse': v['asse']}
                                      for r in v['rondelle']]})
            arrivo = geom.add(v['testa'], _esploso(passo, v['chiave_testa'])) if v['chiave_testa'] in nuovi else v['testa']
            punta = geom.add(geom.add(v['testa'], spost), geom.scala(v['asse'], spec['l']))
            if not stringi:
                frecce.append({'da': punta, 'a': arrivo, 'tipo': 'vite'})
    inserti = []
    for sel in passo.get('inserti', []):
        for f in F.inserti_scelti(dati, sel, terna, istanza):
            spec = dati.viteria['inserti']['INS_M3' if f['tipo'] == 'inserto_m3' else 'INS_M2']
            ingresso = f['p0'] if f['e1'] == 'fondo' else f['p1']
            asse = geom.unit(geom.sub(f['p1'], f['p0']) if f['e1'] == 'fondo' else geom.sub(f['p0'], f['p1']))
            via = spec['l'] + 8
            inserti.append({'centro': geom.add(ingresso, geom.scala(asse, -via)), 'asse': asse, 'd': spec['d'], 'l': spec['l']})
            frecce.append({'da': geom.add(ingresso, geom.scala(asse, spec['l'] - via)), 'a': ingresso, 'tipo': 'inserto'})
    etichette = []
    for e in passo.get('etichette', []):            # nomi sull'immagine: su un punto o al centro di un pezzo
        if 'punto' in e:
            etichette.append({'testo': str(e['testo']), 'punto': e['punto']})
        else:
            for k in dati.chiavi(e['chiave']):
                c = _centro(dati, k, terna, istanza)
                if k in nuovi:
                    c = geom.add(c, _esploso(passo, k))
                etichette.append({'testo': str(e['testo']), 'punto': c})
    vista = passo.get('vista', 'zampa_A' if terna == 'zampa' else 'corpo_alto')
    vista = viste[vista] if isinstance(vista, str) else vista
    return {'id': passo['id'], 'uscita': uscita, 'risoluzione': risoluzione(passo.get('formato', 'grande')),
            'etichette': etichette,
            'oggetti': oggetti, 'viti': viti, 'inserti': inserti, 'frecce': frecce, 'camera': vista,
            'colori': {k: stile[k] for k in ('viti', 'inserti', 'rondelle', 'distanziali')}, 'attenuato': stile['attenuato']}


def miniatura(dati, componente, uscita):
    """Il pezzo da solo, nella sua terna, per il riquadro dei pezzi necessari."""
    stile, viste = _stile(dati), _viste(dati)
    c = dati.manifest['componenti'][componente]
    nome, rgb = c['aspetti'][0]
    vista = (dati.pezzi.get(componente) or {}).get('vista', 'parte')
    return {'id': componente, 'uscita': uscita, 'risoluzione': list(MINIATURA), 'verifica': False,
            'oggetti': [{'chiave': componente, 'mesh': c['mesh'], 'matrice': [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                         'ruolo': 'nuovo', 'colore': stile['colori'].get(nome, rgb)}],
            'viti': [], 'inserti': [], 'frecce': [], 'camera': viste[vista] if isinstance(vista, str) else vista,
            'colori': {k: stile[k] for k in ('viti', 'inserti', 'rondelle', 'distanziali')}, 'attenuato': stile['attenuato']}


def finale(dati, sez, presenti, uscita):
    """Il punto di controllo a fine sezione: tutto quello che e' montato, a colori pieni."""
    s = sez['sezione']
    passo = {'id': s['id'] + '.fine', 'nuovi': presenti, 'mostra': [], 'vista': s.get('vista_finale', 'zampa_A' if s.get('terna', 'zampa') == 'zampa' else 'corpo_alto'),
             'formato': 'finale'}
    lav = lavoro(dati, sez, passo, [], uscita)
    lav['frecce'], lav['verifica'] = [], False
    return lav
