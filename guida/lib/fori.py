"""Fori e viti: classificazione dei fori esportati dal CAD e piazzamento delle viti di una giunzione (D-075).

Una vite sta sull'asse di un foro di presa (punta: inserto, pilota, filettato). La testa va sul foro coassiale piu'
lontano dal fondo della punta fra i pezzi presenti (testa), oppure sulla faccia lontana di un pezzo comprato senza
fori modellati (sopra), oppure resta sull'ingresso della punta (sulla_punta).
"""
import fnmatch

from . import geom

TOLL_D = 0.05            # mm, sul diametro
TOLL_ASSE = 0.3          # mm, distanza fra gli assi di due fori coassiali
TOLL_PARALLELO = 0.9998  # coseno fra gli assi


def classifica(nome_comp, foro, regole):
    cieco = 'fondo' in (foro['e0'][0], foro['e1'][0])
    for r in regole:
        if 'componente' in r and not fnmatch.fnmatchcase(nome_comp, r['componente']):
            continue
        if 'd' in r and abs(foro['d'] - r['d']) > TOLL_D:
            continue
        if 'lav' in r and not fnmatch.fnmatchcase(foro['lav'] or '', r['lav']):
            continue
        if 'cieco' in r and r['cieco'] != cieco:
            continue
        return r['tipo']
    return 'ignora'


def fori_di(dati, chiave, terna, istanza):
    """Fori dell'occorrenza nella terna data: [{tipo, lav, d, p0, p1, e0, e1, asse, chiave}]."""
    nome = dati.occ[chiave]['componente']
    m = dati.matrice(chiave, terna, istanza)
    out = []
    for f in dati.fori_grezzi.get(nome, {}).get('fori', []):
        t = classifica(nome, f, dati.regole_fori)
        if t == 'ignora':
            continue
        p0, p1 = geom.punto(m, f['p0']), geom.punto(m, f['p1'])
        out.append({'tipo': t, 'lav': f['lav'], 'd': f['d'], 'p0': p0, 'p1': p1, 'e0': f['e0'][0], 'e1': f['e1'][0],
                    'asse': geom.unit(geom.sub(p1, p0)), 'chiave': chiave})
    return out


def _sceglie(foro, sel):
    if 'tipo' in sel and foro['tipo'] != sel['tipo']:
        return False
    if 'lav' in sel and not fnmatch.fnmatchcase(foro['lav'] or '', sel['lav']):
        return False
    return True


def coassiali(a, b, d_vite=None):
    """Assi paralleli e vicini. Con il diametro della vite, la vite sull'asse di a deve passare nel foro b: la
    distanza ammessa e' il gioco radiale (le viti delle alette stanno spostate fino a 0,6 nel foro da 4,2, D-049)."""
    toll = TOLL_ASSE if d_vite is None else max(TOLL_ASSE, (b['d'] - d_vite) / 2 + 0.05)
    return abs(geom.dot(a['asse'], b['asse'])) > TOLL_PARALLELO and geom.distanza_retta(b['p0'], a['p0'], a['asse']) < toll


def _fondo_e_ingresso(f):
    """(fondo, ingresso) della punta: il fondo e' l'estremo cieco; se non ce n'e', decide la testa."""
    if f['e1'] == 'fondo':
        return f['p1'], f['p0']
    if f['e0'] == 'fondo':
        return f['p0'], f['p1']
    return None, None


def _lontano_su_asse(chiave_bbox, dati, terna, istanza, origine, asse):
    """Coordinata lungo l'asse della faccia del riquadro d'ingombro del pezzo piu' lontana dall'origine."""
    lo, hi = dati.componente(chiave_bbox)['bbox']
    m = dati.matrice(chiave_bbox, terna, istanza)
    ts = []
    for x in (lo[0], hi[0]):
        for y in (lo[1], hi[1]):
            for z in (lo[2], hi[2]):
                ts.append(geom.dot(geom.sub(geom.punto(m, [x, y, z]), origine), asse))
    return min(ts)


def piazza(dati, nome_g, g, presenti, terna='zampa', istanza='AS'):
    """Viti della giunzione fra i pezzi presenti: [{vite, testa, asse, punta, presa, rondelle, distanziale}].
    asse: unitario, dalla testa verso la punta. presa: mm di vite oltre l'ingresso della punta."""
    v = dati.viteria['viti'][g['vite']]
    punte = [f for k in presenti if dati.corrisponde(k, g['punta']['chiave'])
             for f in fori_di(dati, k, terna, istanza) if _sceglie(f, g['punta'])]
    teste = []
    if 'chiave' in g['testa']:
        teste = [f for k in presenti if dati.corrisponde(k, g['testa']['chiave'])
                 for f in fori_di(dati, k, terna, istanza) if _sceglie(f, g['testa'])]
    vincoli = []
    if 'coassiale_con' in g:
        vincoli = [f for k in presenti if dati.corrisponde(k, g['coassiale_con']['chiave'])
                   for f in fori_di(dati, k, terna, istanza) if _sceglie(f, g['coassiale_con'])]
    out = []
    for p in punte:
        if vincoli and not any(coassiali(p, c) for c in vincoli):
            continue
        fondo, ingresso = _fondo_e_ingresso(p)
        passante = fondo is None
        if 'chiave' in g['testa']:
            compagne = [t for t in teste if coassiali(p, t, v['d'])]
            if not compagne:
                continue
            # il foro della testa piu' vicino alla punta: un foro coassiale dall'altra parte del robot non conta
            vic = min(compagne, key=lambda t: min(geom.norma(geom.sub(t['p0'], e)) for e in (p['p0'], p['p1'])) +
                      min(geom.norma(geom.sub(t['p1'], e)) for e in (p['p0'], p['p1'])))
            if passante:                            # punta passante (filettato): il fondo e' l'estremo lontano dalla testa
                c = vic['p0']
                d0, d1 = geom.norma(geom.sub(p['p0'], c)), geom.norma(geom.sub(p['p1'], c))
                fondo, ingresso = (p['p1'], p['p0']) if d0 < d1 else (p['p0'], p['p1'])
            asse = geom.unit(geom.sub(fondo, ingresso))
            testa = min((vic['p0'], vic['p1']), key=lambda e: geom.dot(geom.sub(e, fondo), asse))
            chiave_testa = vic['chiave']
            vicino = max((vic['p0'], vic['p1']), key=lambda e: geom.dot(geom.sub(e, fondo), asse))
        else:
            if passante:                            # la testa sta dalla parte del pezzo sopra (o dell'ingresso)
                fondo, ingresso = p['p1'], p['p0']
                if 'sopra' in g['testa']:
                    lo, hi = dati.componente(g['testa']['sopra'])['bbox']
                    c = geom.punto(dati.matrice(g['testa']['sopra'], terna, istanza), [(lo[i] + hi[i]) / 2 for i in range(3)])
                    if geom.norma(geom.sub(c, p['p1'])) < geom.norma(geom.sub(c, p['p0'])):
                        fondo, ingresso = p['p0'], p['p1']
            asse = geom.unit(geom.sub(fondo, ingresso))
            chiave_testa = p['chiave'] if g['testa'].get('sulla_punta') else g['testa']['sopra']
            if g['testa'].get('sulla_punta'):
                testa = ingresso
            else:
                s = _lontano_su_asse(g['testa']['sopra'], dati, terna, istanza, fondo, asse)
                testa = geom.add(fondo, geom.scala(asse, s))
            vicino = testa
        presa = v['l'] - geom.dot(geom.sub(vicino if 'distanziale' in g else ingresso, testa), asse)
        fondo_libero = None if passante else round(geom.dot(geom.sub(fondo, testa), asse) - v['l'], 2)
        rondelle = []
        if 'rondelle' in g:
            r = dati.viteria['rondelle'][g['rondelle']['tipo']]
            for i in range(g['rondelle']['n']):
                rondelle.append({'tipo': g['rondelle']['tipo'], 'centro': geom.add(ingresso, geom.scala(asse, -(i + 0.5) * r['sp']))})
        distanziale = None
        if 'distanziale' in g:
            distanziale = {'tipo': g['distanziale'], 'da': ingresso, 'a': vicino}
        out.append({'giunzione': nome_g, 'vite': g['vite'], 'testa': testa, 'asse': asse, 'punta': p['chiave'], 'chiave_testa': chiave_testa,
                    'presa': round(presa, 2), 'fondo_libero': fondo_libero, 'rondelle': rondelle,
                    'distanziale': distanziale})
    return out
