"""Controlli della guida (D-075), in Python puro perche' girino in CI. Ognuno torna una lista di errori (stringhe);
gli avvisi sono a parte. Il caso di controllo teste_a verifica che il piazzamento delle viti sia giusto."""
import fnmatch
import os
import re

import yaml

from . import fori as F
from . import geom
from . import scena as S

ZAMPE = 6


def _presenti(dati, assieme):
    return [k for k in dati.basi if k.startswith(assieme + '/') and not dati.occ[k].get('virtuale')]


def giunzioni_complete(dati):
    """Con tutti i pezzi presenti, ogni giunzione trova esattamente le viti attese."""
    errori = []
    for assieme, terna in (('zampa', 'zampa'), ('corpo', 'robot')):
        presenti = _presenti(dati, assieme)
        for nome, g in dati.giunzioni[assieme].items():
            n = len(F.piazza(dati, nome, g, presenti, terna))
            if n != g['attesi']:
                errori.append('%s/%s: %d viti trovate, %d attese' % (assieme, nome, n, g['attesi']))
    return errori


def totali_viti(dati):
    """Somma delle giunzioni (zampa x 6, senza le predisposizioni) contro la riga "Totale viti" del BOM."""
    viti, rondelle = {}, {}
    for assieme, molt in (('zampa', ZAMPE), ('corpo', 1)):
        for g in dati.giunzioni[assieme].values():
            if g.get('predisposizione'):
                continue
            viti[g['vite']] = viti.get(g['vite'], 0) + g['attesi'] * molt
            if 'rondelle' in g:
                t = g['rondelle']['tipo']
                rondelle[t] = rondelle.get(t, 0) + g['attesi'] * g['rondelle']['n'] * molt
    attesi = dati.viteria['totali_bom']
    errori = ['viti %s: %d dalle giunzioni, %d nel BOM' % (k, viti.get(k, 0), attesi['viti'].get(k, 0))
              for k in sorted(set(viti) | set(attesi['viti'])) if viti.get(k, 0) != attesi['viti'].get(k, 0)]
    errori += ['rondelle %s: %d dalle giunzioni, %d nel BOM' % (k, rondelle.get(k, 0), attesi['rondelle'].get(k, 0))
               for k in sorted(set(rondelle) | set(attesi['rondelle'])) if rondelle.get(k, 0) != attesi['rondelle'].get(k, 0)]
    return errori


def totali_inserti(dati):
    """Fori per inserti nei pezzi (zampa x 6), tolti quelli delle predisposizioni, contro il BOM."""
    conta = {'inserto_m3': 0, 'inserto_m2': 0}
    predisp = dati.viteria['inserti_predisposizioni']
    for k in dati.basi:
        o = dati.occ[k]
        if o.get('virtuale') or o.get('alternativa') or o['assieme'] == 'attrezzo':
            continue
        molt = ZAMPE if o['assieme'] == 'zampa' else 1
        terna = 'zampa' if o['assieme'] == 'zampa' else 'robot'
        for f in F.fori_di(dati, k, terna, 'AS'):
            if f['tipo'] not in conta:
                continue
            if any(fnmatch.fnmatchcase(k, p['chiave']) and fnmatch.fnmatchcase(f['lav'] or '', p['lav']) for p in predisp):
                continue
            conta[f['tipo']] += molt
    attesi = dati.viteria['totali_bom']['inserti']
    errori = []
    for tipo, chiave in (('inserto_m3', 'INS_M3'), ('inserto_m2', 'INS_M2')):
        if conta[tipo] != attesi[chiave]:
            errori.append('inserti %s: %d fori nei pezzi, %d nel BOM' % (chiave, conta[tipo], attesi[chiave]))
    return errori


def teste_a(dati):
    """Caso di controllo: le teste delle 12 viti del lato A (8 sulle squadrette, 4 sul blocco) cadono sui cilindri
    testa_NN di Ingombro_Teste_A (entro 0,05 mm di traverso, il centro a meta' altezza della testa)."""
    presenti = _presenti(dati, 'zampa')
    viti = []
    for nome in ('femore_a_squadrette', 'femore_a_blocco'):
        viti += F.piazza(dati, nome, dati.giunzioni['zampa'][nome], presenti, 'zampa')
    m = dati.matrice('zampa/Ingombro_Teste_A', 'zampa')
    teste = [geom.punto(m, t['centro']) for t in dati.fori_grezzi['Ingombro_Teste_A']['teste']]
    errori = []
    if len(teste) != 12 or len(viti) != 12:
        return ['teste_a: %d teste nel CAD, %d viti piazzate (attese 12 e 12)' % (len(teste), len(viti))]
    for v in viti:
        k = dati.viteria['viti'][v['vite']]['testa_k']
        c = geom.add(v['testa'], geom.scala(v['asse'], -k / 2))
        d = min(geom.norma(geom.sub(c, t)) for t in teste)
        if d > 0.05:
            errori.append('teste_a: vite %s con la testa a %.3f mm dalla testa del CAD' % (v['giunzione'], d))
    return errori


def lunghezze(dati):
    """Avvisi: presa corta (meno di 2 mm, o di 3 per le M3 negli inserti) o vite che tocca il fondo del foro."""
    avvisi = []
    for assieme, terna in (('zampa', 'zampa'), ('corpo', 'robot')):
        presenti = _presenti(dati, assieme)
        for nome, g in dati.giunzioni[assieme].items():
            for v in F.piazza(dati, nome, g, presenti, terna):
                minima = 3.0 if g['vite'].startswith('M3') and 'inserto' in g['punta'].get('tipo', '') else 2.0
                if v['presa'] < minima:
                    avvisi.append('%s/%s: presa %.2f mm (minimo %.1f)' % (assieme, nome, v['presa'], minima))
                if v['fondo_libero'] is not None and v['fondo_libero'] < 0.1:
                    avvisi.append('%s/%s: la vite arriva a %.2f mm dal fondo del foro' % (assieme, nome, v['fondo_libero']))
    return sorted(set(avvisi))


# ------------------------------------------------------------------------------------------ controlli sui passi
TIPI_AVVISO = {'attenzione', 'importante', 'nota', 'opzionale', 'prova'}
SEZIONI_DI_PROVA = {'prova'}          # guida/passi/99-prova.yaml: solo per la pipeline, fuori dai conteggi


def _sezioni(dati, anche_prova=False, solo=None):
    return [z for z in dati.sezioni if (anche_prova or z['sezione']['id'] not in SEZIONI_DI_PROVA)
            and (not solo or z['sezione']['id'] in solo)]


def _giunzione(dati, nome):
    for assieme in ('zampa', 'corpo'):
        if nome in dati.giunzioni[assieme]:
            return assieme, dati.giunzioni[assieme][nome]
    return None, None


def chiavi_esistenti(dati, solo=None):
    """Nessun passo cita pezzi, giunzioni, attrezzi, viste, figure o tipi di avviso che non esistono; id unici."""
    errori, visti = [], set()
    with open(os.path.join(dati.radice, 'catalogo', 'viste.yaml'), encoding='utf-8') as f:
        viste = yaml.safe_load(f)
    for z in _sezioni(dati, anche_prova=True, solo=solo):
        s = z['sezione']
        for k in s.get('presenti_iniziali', []):
            if not dati.chiavi(k):
                errori.append('%s: presenti_iniziali %s non esiste' % (s['id'], k))
        for p in z['passi']:
            pid = p.get('id', '?')
            if pid in visti:
                errori.append('%s: id ripetuto' % pid)
            visti.add(pid)
            if p.get('terna', 'zampa') not in ('zampa', 'robot'):
                errori.append('%s: terna %s' % (pid, p['terna']))
            if 'figura' in p and not os.path.exists(os.path.join(dati.radice, p['figura'])):
                errori.append('%s: figura %s non esiste (percorso da guida/)' % (pid, p['figura']))
            t = p.get('tabella')
            if t is not None and (not t.get('righe') or any(len(r) != len(t.get('intestazione', r)) for r in t['righe'])):
                errori.append('%s: tabella senza righe o con righe di lunghezza diversa dall\'intestazione' % pid)
            for campo in ('nuovi', 'mostra', 'nascondi', 'in_evidenza'):
                for k in p.get(campo, []):
                    if not dati.chiavi(k):
                        errori.append('%s: %s %s non esiste' % (pid, campo, k))
            for a in p.get('assiemi', []):
                if not S.chiavi_assieme(dati, a):
                    errori.append('%s: assieme %s vuoto' % (pid, a.get('chiavi')))
            for gj in p.get('giunzioni', []):
                nome = gj['id'] if isinstance(gj, dict) else gj
                if _giunzione(dati, nome)[0] is None:
                    errori.append('%s: giunzione %s non esiste' % (pid, nome))
            for sel in p.get('inserti', []):
                if not dati.chiavi(sel['chiave']):
                    errori.append('%s: inserti in %s, che non esiste' % (pid, sel['chiave']))
            for t in p.get('attrezzi', []):
                if t not in dati.attrezzi:
                    errori.append('%s: attrezzo %s non e\' in attrezzi.yaml' % (pid, t))
            v = p.get('vista')
            if isinstance(v, str) and v not in viste:
                errori.append('%s: vista %s non e\' in viste.yaml' % (pid, v))
            for a in p.get('avvisi', []):
                if a.get('tipo') not in TIPI_AVVISO:
                    errori.append('%s: avviso di tipo %s' % (pid, a.get('tipo')))
                elif a['tipo'] == 'opzionale' and not a.get('x'):
                    errori.append('%s: avviso opzionale senza la predisposizione (x)' % pid)
                elif a.get('quando') not in (None, 'solo_ora', 'meglio_ora', 'anche_dopo'):
                    errori.append('%s: quando = %s' % (pid, a['quando']))
    return errori


def montaggio_unico(dati, solo=None):
    """Ogni pezzo si monta una volta sola in tutta la guida (la zampa una volta, ripetuta sei: 'zampa/Coxa' e
    'zampa/Coxa@AS' sono lo stesso pezzo) e mai se e' gia' presente nel passo."""
    errori, dove = [], {}
    for z in _sezioni(dati, solo=solo):
        for p, presenti in S.stati(dati, z):
            for c in S.entrano(dati, p)[0]:
                if c in presenti:
                    errori.append('%s: %s e\' gia\' montato' % (p['id'], c))
                b = dati.base(c)
                if b in dove and dove[b] != p['id']:
                    errori.append('%s: %s montato anche al passo %s' % (p['id'], b, dove[b]))
                dove.setdefault(b, p['id'])
    return errori


def giunzioni_usate(dati, solo=None):
    """Ogni giunzione si usa una volta sola, e nel passo che la usa trova tutte le viti attese: se ne mancano, un
    pezzo della giunzione non e' ancora montato (ordine sbagliato)."""
    errori, dove = [], {}
    for z in _sezioni(dati, anche_prova=True, solo=solo):
        s = z['sezione']
        for p, presenti in S.stati(dati, z):
            terna, istanza = S.terna_di(z, p)
            nuovi, assiemi = S.entrano(dati, p)
            pieni = [c for k in p.get('in_evidenza', []) for c in dati.chiavi(k)]
            tutti = list(dict.fromkeys(presenti + nuovi + assiemi + pieni))
            for gj in p.get('giunzioni', []):
                nome = gj['id'] if isinstance(gj, dict) else gj
                assieme, g = _giunzione(dati, nome)
                if g is None:
                    continue
                stringi = isinstance(gj, dict) and gj.get('stringi')
                if stringi and s['id'] not in SEZIONI_DI_PROVA and nome not in dove:
                    errori.append('%s: giunzione %s stretta prima di essere messa' % (p['id'], nome))
                elif not stringi and s['id'] not in SEZIONI_DI_PROVA:
                    if nome in dove:
                        errori.append('%s: giunzione %s gia\' usata al passo %s' % (p['id'], nome, dove[nome]))
                    dove.setdefault(nome, p['id'])
                n = len(F.piazza(dati, nome, g, tutti, terna, istanza))
                if n != g['attesi']:
                    errori.append('%s: giunzione %s con %d viti su %d: manca un pezzo nel passo' % (p['id'], nome, n, g['attesi']))
    return errori


def decisioni(dati, solo=None):
    """Ogni D-0xx citato nei passi esiste in docs/decisioni.md."""
    with open(os.path.join(os.path.dirname(dati.radice), 'docs', 'decisioni.md'), encoding='utf-8') as f:
        esistono = set(re.findall(r'^##+ (D-0\d\d[a-z]?)\b', f.read(), re.M))
    errori = []
    for z in _sezioni(dati, anche_prova=True, solo=solo):
        citate = set(re.findall(r'\bD-0\d\d[a-z]?\b', str(z['sezione'])))
        errori += ['sezione %s: %s non esiste in docs/decisioni.md' % (z['sezione']['id'], d) for d in sorted(citate - esistono)]
        for p in z['passi'] + z.get('rinviati', []):
            citate = set(re.findall(r'\bD-0\d\d[a-z]?\b', str(p)))
            errori += ['%s: %s non esiste in docs/decisioni.md' % (p['id'], d) for d in sorted(citate - esistono)]
    return errori


def mancanti(dati):
    """Avvisi finche' la guida non e' completa: pezzi mai montati, giunzioni mai usate, fori per inserti senza
    inserto in nessun passo (zampa contata una volta)."""
    montati, usate, inseriti = set(), set(), set()
    for z in _sezioni(dati):
        for p, _ in S.stati(dati, z):
            montati.update(dati.base(c) for c in S.entrano(dati, p)[0])
            usate.update(g['id'] if isinstance(g, dict) else g for g in p.get('giunzioni', []))
            terna, istanza = S.terna_di(z, p)
            for sel in p.get('inserti', []):
                for f in F.inserti_scelti(dati, sel, terna, istanza):
                    inseriti.add((dati.base(f['chiave']), f['lav'], tuple(round(x, 1) for x in f['p0'])))
    pezzi = [k for k in dati.basi if not dati.occ[k].get('virtuale') and not dati.occ[k]['componente'].startswith('Ingombro_')
             and dati.occ[k]['assieme'] != 'attrezzo']
    out = ['pezzo mai montato: %s' % k for k in pezzi if k not in montati]
    out += ['giunzione mai usata: %s' % n for a in ('zampa', 'corpo') for n in dati.giunzioni[a] if n not in usate]
    for k in dati.basi:
        o = dati.occ[k]
        if o.get('virtuale') or o['componente'].startswith('Ingombro_') or o['assieme'] == 'attrezzo':
            continue
        terna = 'zampa' if o['assieme'] == 'zampa' else 'robot'
        for f in F.fori_di(dati, k, terna, 'AS'):
            if f['tipo'].startswith('inserto') and (k, f['lav'], tuple(round(x, 1) for x in f['p0'])) not in inseriti:
                out.append('inserto mai messo: %s %s' % (k, f['lav']))
    return out


def tutti(dati, solo=None):
    """Tutti i controlli. Con solo (id di sezioni) quelli sui passi guardano solo quelle sezioni: serve quando piu'
    estrattori lavorano insieme; gli incroci fra sezioni li vede il controllo completo."""
    return {'file_leggibili': [] if solo else list(dati.errori_yaml),
            'giunzioni_complete': giunzioni_complete(dati), 'totali_viti': totali_viti(dati),
            'totali_inserti': totali_inserti(dati), 'teste_a': teste_a(dati),
            'chiavi_esistenti': chiavi_esistenti(dati, solo), 'montaggio_unico': montaggio_unico(dati, solo),
            'giunzioni_usate': giunzioni_usate(dati, solo), 'decisioni': decisioni(dati, solo)}
