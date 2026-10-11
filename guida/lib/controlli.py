"""Controlli della guida (D-075), in Python puro perche' girino in CI. Ognuno torna una lista di errori (stringhe);
gli avvisi sono a parte. Il caso di controllo teste_a verifica che il piazzamento delle viti sia giusto."""
import fnmatch

from . import fori as F
from . import geom

ZAMPE = 6


def _presenti(dati, assieme):
    return [k for k in dati.occ if k.startswith(assieme + '/') and not dati.occ[k].get('virtuale')]


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
    for k, o in dati.occ.items():
        if o.get('virtuale') or o.get('alternativa'):
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


def tutti(dati):
    return {'giunzioni_complete': giunzioni_complete(dati), 'totali_viti': totali_viti(dati),
            'totali_inserti': totali_inserti(dati), 'teste_a': teste_a(dati)}
