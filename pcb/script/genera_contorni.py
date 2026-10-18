"""Contorni, fori e zone senza rame delle schede, dalle quote del CAD (piano-pcb.md 5.2).

Fonti:
- parametri (`PARAMETRI` di `cad/script/rif_componenti.py` e `corpo.py`), letti con `ast` senza importare i file,
  che vogliono le librerie di Fusion;
- pose delle schede nel corpo da `guida/dati/manifest.json`, fori degli inserti da `guida/dati/fori.json`
  (li scrive `esporta_guida.py` dal modello di Fusion).

Terna di KiCad: x = X del robot + 100, y = 100 − Y del robot (KiCad ha la Y verso il basso). Le schede si guardano
dall'alto del robot; i componenti della scheda del carapace stanno sotto, sul retro (B.Cu).

Uso: python3 genera_contorni.py                  stampa la geometria delle schede
     python3 genera_contorni.py --controlla F...  fallisce se un .kicad_pcb si è staccato dal CAD
Gira con il Python di sistema e con quello di KiCad, senza `pcbnew`.
"""

import ast
import json
import math
import os
import re
import sys

from sexpr import figli, figlio, leggi

RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ORIGINE = (100.0, 100.0)  # punto di KiCad dove cade l'origine del robot
TOLLERANZA = 0.01
LATI_CERCHIO = 32

# Una scheda: istanza nel manifest, parametri della sagoma (lunghezza lungo la X locale, larghezza lungo la Y
# locale, scatola centrata), fori degli inserti, zone senza rame attorno ai fori per faccia, zone senza rame a rettangolo.
SCHEDE = {
    'basetta': {
        'istanza': 'corpo/Basetta',
        'sagoma': ('bas_l', 'bas_w'),
        'fori': ['bas_col_pa_ins', 'bas_col_pb_ins', 'bas_col_aa_ins', 'bas_col_ab_ins'],
        # faccia dei componenti in alto: testa M2 Ø4 più 1 mm per lato; sotto, colonnina più 1 mm (piano 4.1, S)
        'anelli': {'F.Cu': '4 mm + 2 mm', 'B.Cu': 'cor_bas_col_d + 1 mm'},
        # antenna dell'ESP32: niente rame da x 74 al bordo di testa, sulle due facce (studio.md 2.1, R-15; S)
        'rettangoli': [(('F.Cu', 'B.Cu'), 'antenna', '74 mm', None)],
        # apertura sotto i componenti inferiori di U2 (D24V22F5), nella terna del robot: non viene dal CAD ma dal
        # piazzamento di U2 e dallo STEP Pololu (pcb/basetta/genera_pcb.py, apertura_u2, che la controlla)
        'aperture': [[(49.16, -8.64), (49.16, 6.41), (35.84, 6.41), (35.84, -6.96), (42.28, -6.96), (42.28, -8.64)]],
    },
    'carapace': {
        'istanza': 'corpo/Scheda_carapace',
        'sagoma': ('sch_l', 'sch_w'),
        # ali davanti (2.1.8, blocco F): lungo la X locale fino a ±sch_ala_y, profonde sch_ala_x dal bordo a -Y locale
        'ali': ('sch_ala_y', 'sch_ala_x'),
        'fori': ['ins_sch_a', 'ins_sch_b', 'ins_sch_c', 'ins_sch_d'],
        # componenti sotto: testa M2 Ø3,8 (corpo.py, sch_vite_xp) più 0,5 per lato; sopra, la bugna Ø5,5 (corpo.py,
        # cilindro 'bugna_sch_*', non parametrica) senza margine: la plastica puo' toccare il rame, ma nessuna piazzola
        # le sta sotto (con 0,5 di margine coprivano i pin 1, 2, 15 e 16 della testata, F4)
        # sopra vieta solo le piazzole: sotto la plastica una pista con la sua maschera ci puo' stare (revisione)
        'anelli': {'B.Cu': '3.8 mm + 1 mm', 'F.Cu': ('5.5 mm', 'piazzole')},
        'rettangoli': [],
    },
    'partitori': {
        # variante P2 (D-080): sotto le prese dei piedi, su due bugne come IMU e ADC
        'istanza': 'corpo/Partitori',
        'sagoma': ('par_l', 'par_w'),
        # 2.1.9 (D-084): centro della scheda spostato di par_dy rispetto alla posa (fila dei fori), angolo di testa a +Y
        # smussato di par_smusso
        'centro_y': 'par_dy',
        'smusso': 'par_smusso',
        'fori': ['ins_par_a', 'ins_par_b'],
        # sopra la testa M2 × 5 (Ø4) più 0,5 per lato; sotto la bugna Ø5,5 più 0,5 per lato (S)
        'anelli': {'F.Cu': '4 mm + 1 mm', 'B.Cu': 'cor_sen_bugna_d + 1 mm'},
        'rettangoli': [],
    },
}


# --- parametri del CAD

def _leggi_parametri(percorso):
    with open(percorso, encoding='utf-8') as f:
        albero = ast.parse(f.read())
    for nodo in albero.body:
        if isinstance(nodo, ast.Assign) and getattr(nodo.targets[0], 'id', None) == 'PARAMETRI':
            return {t.elts[0].value: t.elts[1].value for t in nodo.value.elts}
    raise ValueError('PARAMETRI non trovato in %s' % percorso)


class Parametri(dict):
    """Espressioni dei parametri di Fusion valutate in mm, con i nomi risolti a richiesta."""

    def __init__(self, espressioni):
        super().__init__()
        self.espressioni = espressioni

    def __missing__(self, nome):
        if nome not in self.espressioni:
            raise KeyError('parametro %s non definito nel CAD' % nome)
        self[nome] = self.valuta(self.espressioni[nome])
        return self[nome]

    def valuta(self, espressione):
        testo = re.sub(r'(\d+(?:\.\d+)?)\s*mm\b', r'\1', espressione)
        if re.search(r'\b(deg|rad|cm|in)\b', testo):
            raise ValueError('unità non gestita in %r' % espressione)
        return float(eval(testo, {'__builtins__': {}}, self))


def parametri():
    esp = {}
    for f in ('cad/script/rif_componenti.py', 'cad/script/corpo.py'):
        esp.update(_leggi_parametri(os.path.join(RADICE, f)))
    return Parametri(esp)


# --- geometria

def kicad(x, y):
    return (round(ORIGINE[0] + x, 4), round(ORIGINE[1] - y, 4))


def _posa(chiave):
    with open(os.path.join(RADICE, 'guida', 'dati', 'manifest.json'), encoding='utf-8') as f:
        man = json.load(f)
    for i in man['occorrenze']:
        if i['chiave'] == chiave:
            t = i['T']
            return (t[0], t[1], t[3]), (t[4], t[5], t[7])
    raise KeyError('istanza %s non trovata nel manifest' % chiave)


def _fori_cad():
    with open(os.path.join(RADICE, 'guida', 'dati', 'fori.json'), encoding='utf-8') as f:
        dati = json.load(f)
    out = {}
    for fori in dati['componenti'].values():
        for h in (fori if isinstance(fori, list) else fori.get('fori', [])):
            if isinstance(h, dict) and 'lav' in h:
                out.setdefault(h['lav'], h)
    return out


def _cerchio(cx, cy, d):
    return [(round(cx + d / 2 * math.cos(2 * math.pi * k / LATI_CERCHIO), 4),
             round(cy + d / 2 * math.sin(2 * math.pi * k / LATI_CERCHIO), 4)) for k in range(LATI_CERCHIO)]


def geometria(nome, par=None):
    """{'contorno': [(x, y)], 'fori': [(nome, x, y, d)], 'senza_rame': [(nome, (strati), [(x, y)], cosa)]} in mm di
    KiCad; cosa = 'tutto' (niente rame) o 'piazzole' (niente piazzole, le piste si')."""
    par = parametri() if par is None else par
    s = SCHEDE[nome]
    (a, b, tx), (c, d, ty) = _posa(s['istanza'])
    lx, ly = par[s['sagoma'][0]] / 2, par[s['sagoma'][1]] / 2
    dy = par[s['centro_y']] if 'centro_y' in s else 0.0
    locale = [(-lx, -ly + dy), (lx, -ly + dy), (lx, ly + dy), (-lx, ly + dy)]
    if 'smusso' in s:
        sm = par[s['smusso']]
        locale = [(-lx, -ly + dy), (lx, -ly + dy), (lx, ly + dy - sm), (lx - sm, ly + dy), (-lx, ly + dy)]
    if 'ali' in s:
        ay, ax = par[s['ali'][0]], par[s['ali'][1]]
        ya = -ly + ax
        locale = [(-ay, -ly), (ay, -ly), (ay, ya), (lx, ya), (lx, ly), (-lx, ly), (-lx, ya), (-ay, ya)]
    robot = [(a * x + b * y + tx, c * x + d * y + ty) for x, y in locale]
    contorno = [kicad(x, y) for x, y in robot]
    xs, ys = [p[0] for p in robot], [p[1] for p in robot]
    fori_cad = _fori_cad()
    fori, senza = [], []
    d_vite = par['vite_m2_pass']
    for lav in s['fori']:
        x, y = fori_cad[lav]['p0'][:2]
        if not (min(xs) < x < max(xs) and min(ys) < y < max(ys)):
            raise ValueError('foro %s (%.2f; %.2f) fuori dalla sagoma di %s' % (lav, x, y, nome))
        kx, ky = kicad(x, y)
        fori.append((lav, kx, ky, d_vite))
        for strato, espr in sorted(s['anelli'].items()):
            espr, cosa = espr if isinstance(espr, tuple) else (espr, 'tutto')
            senza.append(('%s_%s' % (lav, strato), (strato,), _cerchio(kx, ky, par.valuta(espr)), cosa))
    for strati, nome_r, x0, x1 in s['rettangoli']:
        rx0 = par.valuta(x0) if x0 else min(xs)
        rx1 = par.valuta(x1) if x1 else max(xs)
        senza.append((nome_r, tuple(strati), [kicad(rx0, max(ys)), kicad(rx1, max(ys)),
                                              kicad(rx1, min(ys)), kicad(rx0, min(ys))], 'tutto'))
    aperture = [[kicad(x, y) for x, y in a] for a in s.get('aperture', [])]
    return {'contorno': contorno, 'fori': fori, 'senza_rame': senza, 'aperture': aperture}


# --- controllo di un .kicad_pcb (lettura del testo, senza KiCad)

def _xy(n):
    return (float(n[1]), float(n[2]))


def leggi_pcb(percorso):
    """Segmenti e cerchi su Edge.Cuts, aree senza rame con nome, dal file di KiCad."""
    with open(percorso, encoding='utf-8') as f:
        pcb = leggi(f.read())
    segmenti, cerchi, aree = [], [], {}
    for g in figli(pcb, 'gr_line'):
        if figlio(g, 'layer')[1] == 'Edge.Cuts':
            segmenti.append((_xy(figlio(g, 'start')), _xy(figlio(g, 'end'))))
    for g in figli(pcb, 'gr_circle'):
        if figlio(g, 'layer')[1] == 'Edge.Cuts':
            c, e = _xy(figlio(g, 'center')), _xy(figlio(g, 'end'))
            cerchi.append((c[0], c[1], 2 * math.hypot(e[0] - c[0], e[1] - c[1])))
    altre = [g[0] for tipo in ('gr_rect', 'gr_arc', 'gr_poly', 'gr_curve')
             for g in figli(pcb, tipo) if figlio(g, 'layer')[1] == 'Edge.Cuts']
    segmenti.extend(('altra forma', 'altra forma') for _ in altre)
    for z in figli(pcb, 'zone'):
        if figlio(z, 'keepout') is None:
            continue
        nome = (figlio(z, 'name') or [None, ''])[1]
        strati = figlio(z, 'layers') or figlio(z, 'layer')
        punti = [_xy(p) for p in figli(figlio(figlio(z, 'polygon'), 'pts'), 'xy')]
        piste = figlio(figlio(z, 'keepout'), 'tracks')
        cosa = 'piazzole' if piste is not None and piste[1] == 'allowed' else 'tutto'
        aree[nome] = (tuple(sorted(str(x) for x in strati[1:])), punti, cosa)
    return segmenti, cerchi, aree


def _vicini(a, b):
    return all(abs(p - q) <= TOLLERANZA for p, q in zip(a, b))


def controlla(nome, percorso, par=None):
    """Elenco delle differenze fra il .kicad_pcb e il CAD (vuoto se va tutto bene)."""
    g = geometria(nome, par)
    segmenti, cerchi, aree = leggi_pcb(percorso)
    errori = []
    attesi = list(zip(g['contorno'], g['contorno'][1:] + g['contorno'][:1]))
    for a in g['aperture']:
        attesi += list(zip(a, a[1:] + a[:1]))
    for a, b in attesi:
        if not any((_vicini(a, s) and _vicini(b, e)) or (_vicini(a, e) and _vicini(b, s)) for s, e in segmenti):
            errori.append('lato del contorno %s-%s mancante' % (a, b))
    if len(segmenti) != len(attesi):
        errori.append('contorno con %d lati, il CAD ne ha %d' % (len(segmenti), len(attesi)))
    for lav, x, y, d in g['fori']:
        if not any(_vicini((x, y, d), c) for c in cerchi):
            errori.append('foro %s (%.3f; %.3f) Ø%.2f mancante' % (lav, x, y, d))
    if len(cerchi) != len(g['fori']):
        errori.append('%d fori sul contorno, il CAD ne ha %d' % (len(cerchi), len(g['fori'])))
    for nome_a, strati, punti, cosa in g['senza_rame']:
        if nome_a not in aree:
            errori.append('zona senza rame %s mancante' % nome_a)
            continue
        s_pcb, p_pcb, c_pcb = aree[nome_a]
        if c_pcb != cosa:
            errori.append('zona senza rame %s vieta "%s" invece di "%s"' % (nome_a, c_pcb, cosa))
        if s_pcb != tuple(sorted(strati)):
            errori.append('zona senza rame %s sugli strati %s invece di %s' % (nome_a, s_pcb, strati))
        if len(p_pcb) != len(punti) or not all(any(_vicini(p, q) for q in p_pcb) for p in punti):
            errori.append('zona senza rame %s con una forma diversa dal CAD' % nome_a)
    return errori


def principale(argv):
    if '--controlla' in argv:
        file_pcb = [a for a in argv if a.endswith('.kicad_pcb')]
        errori = 0
        for f in file_pcb:
            nome = os.path.splitext(os.path.basename(f))[0]
            e = controlla(nome, f)
            print('%s: %s' % (f, 'come il CAD' if not e else '%d differenze' % len(e)))
            for x in e:
                print('  ' + x)
            errori += len(e)
        return 1 if errori else 0
    par = parametri()
    for nome in SCHEDE:
        print(nome, json.dumps(geometria(nome, par), indent=1)[:2000])
    return 0


if __name__ == '__main__':
    sys.exit(principale(sys.argv[1:]))
