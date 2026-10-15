"""Impaginazione della guida (D-075): pagine A4 orizzontali in HTML da Jinja2, immagini piatte, frecce e viti 1:1 in SVG.

Le pagine si numerano qui, non nel browser: indice e rimandi restano giusti anche nell'HTML navigabile. Le misure delle
viti in SVG sono in mm con viewBox in mm: stampate al 100 % sono a grandezza vera (barra di controllo da 100 mm).
"""
import html
import json
import math
import os
import re
import shutil

import jinja2
import yaml
from PIL import Image

from . import elenchi as E
from . import scena as S

# zampe dalla testa alla coda, sinistra prima di destra
ORDINE_ZAMPE = ['AS', 'AD', 'MS', 'MD', 'PS', 'PD']
ETICHETTE = {'attenzione': 'Attenzione', 'importante': 'Importante', 'nota': 'Nota', 'opzionale': 'Opzionale', 'prova': 'Prova'}
QUANDO = {'solo_ora': 'solo ora', 'meglio_ora': 'meglio ora', 'anche_dopo': 'anche dopo'}
# Frecce in pixel del render (9 px/mm, scena.PX_MM): pezzi 1,6 mm, viti e inserti 0,9 mm, bordo bianco 0,5 mm.
LARGHEZZA_FRECCIA = {'pezzo': 14, 'vite': 8, 'inserto': 8}
BORDO_FRECCIA = 4.5


# ---------------------------------------------------------------------------------------------- disegni 1:1
def _filetto(x0, y0, lung, d):
    passo = 0.5 if d >= 3 else 0.4
    return ''.join('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (x0 + i * passo, y0, x0 + i * passo + passo / 2, y0 + d)
                   for i in range(int(lung / passo)))


def svg_vite(v):
    """Vite vista di fianco, testa a sinistra, in mm: cilindrica (ISO 4762), tonda (ISO 7045), svasata (ISO 10642)."""
    d, lung, td, tk = v['d'], v['l'], v['testa_d'], v['testa_k']
    m = 0.4
    h = td + 2 * m
    yc = h / 2
    if v['testa'] == 'svasata':
        kc = (td - d) / 2
        w = lung + 2 * m
        testa = '<path class="testa" d="M%.2f %.2f L%.2f %.2f L%.2f %.2f L%.2f %.2f Z"/>' % (
            m, yc - td / 2, m + kc, yc - d / 2, m + kc, yc + d / 2, m, yc + td / 2)
        x_gambo, l_gambo = m + kc, lung - kc
    elif v['testa'] == 'tonda':
        w = tk + lung + 2 * m
        testa = '<path class="testa" d="M%.2f %.2f A%.2f %.2f 0 0 0 %.2f %.2f Z"/>' % (m + tk, yc - td / 2, tk, td / 2, m + tk, yc + td / 2)
        x_gambo, l_gambo = m + tk, lung
    else:
        w = tk + lung + 2 * m
        testa = '<rect class="testa" x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="0.35"/>' % (m, yc - td / 2, tk, td)
        x_gambo, l_gambo = m + tk, lung
    return ('<svg class="v11" width="%.2fmm" height="%.2fmm" viewBox="0 0 %.2f %.2f">%s'
            '<rect class="gambo" x="%.2f" y="%.2f" width="%.2f" height="%.2f"/><g class="filetto">%s</g></svg>'
            % (w, h, w, h, testa, x_gambo, yc - d / 2, l_gambo, d, _filetto(x_gambo, yc - d / 2, l_gambo, d)))


def svg_rondella(r):
    """Rondella di fianco e di fronte, in mm."""
    de, di, sp = r['d_est'], r['d_int'], r['sp']
    m = 0.4
    w, h = sp + de + 3 + 2 * m, de + 2 * m
    return ('<svg class="v11" width="%.2fmm" height="%.2fmm" viewBox="0 0 %.2f %.2f">'
            '<rect class="testa" x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>'
            '<circle class="testa" cx="%.2f" cy="%.2f" r="%.2f"/><circle cx="%.2f" cy="%.2f" r="%.2f" fill="#fff" stroke="#1d2026" stroke-width=".12"/></svg>'
            % (w, h, w, h, m, m, sp, de, m + sp + 3 + de / 2, h / 2, de / 2, m + sp + 3 + de / 2, h / 2, di / 2))


def svg_inserto(s):
    d, lung = s['d'], s['l']
    m = 0.4
    w, h = lung + 2 * m, d + 2 * m
    zig = ''.join('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (m + i * 0.7, m, m + i * 0.7 + 0.5, m + d) for i in range(int(lung / 0.7)))
    return ('<svg class="v11" width="%.2fmm" height="%.2fmm" viewBox="0 0 %.2f %.2f"><rect class="ottone" x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx=".3"/>'
            '<g class="filetto">%s</g></svg>' % (w, h, w, h, m, m, lung, d, zig))


def svg_distanziale(s):
    d, lung = s['d'], s['l']
    m = 0.4
    w, h = lung + 6 + 2 * m, d + 2 * m
    return ('<svg class="v11" width="%.2fmm" height="%.2fmm" viewBox="0 0 %.2f %.2f"><rect class="ottone" x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>'
            '<rect class="gambo" x="%.2f" y="%.2f" width="6" height="3"/></svg>' % (w, h, w, h, m, m, lung, d, m + lung, h / 2 - 1.5))


def righello(mm):
    """Righello 1:1 in mm, tacche ogni millimetro e numeri ogni 10."""
    tacche = ''.join('<line x1="%d" y1="0" x2="%d" y2="%s"/>' % (i, i, '3' if i % 10 == 0 else ('2' if i % 5 == 0 else '1.2'))
                     for i in range(mm + 1))
    numeri = ''.join('<text x="%d" y="5.6">%d</text>' % (i, i) for i in range(0, mm + 1, 10))
    return ('<svg class="righello" width="%dmm" height="6mm" viewBox="-0.5 0 %d 6"><g class="tacche">%s</g>%s</svg>'
            % (mm + 1, mm + 1, tacche, numeri))


def nome_vite(tipo, v):
    return 'M%g × %g%s' % (v['d'], v['l'], ' svasata' if v['testa'] == 'svasata' else '')


# ---------------------------------------------------------------------------------------------- testo
_VERBO = re.compile(r'^([A-ZÀ-Ý][a-zà-ÿ\']+)(\b)')


def testo(riga, verbo=True):
    """Riga di istruzione: escape, verbo iniziale in neretto, **neretto**, dati marcati [V] [S] [C], rimandi D-0xx."""
    t = html.escape(str(riga), quote=False)
    if verbo:
        t = _VERBO.sub(r'<b class="verbo">\1</b>', t, count=1)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\[([VSC])\]', r'<span class="dato \1">\1</span>', t)
    t = re.sub(r'\b(D-0\d\d[a-z]?)\b', r'<span class="rif">\1</span>', t)
    return t


def avviso(a):
    tipo = a['tipo']
    et = ETICHETTE[tipo]
    if tipo == 'opzionale':
        et = ' '.join(x for x in (et, a.get('x', ''), '— ' + QUANDO[a['quando']] if a.get('quando') else '') if x)
    return {'tipo': tipo, 'etichetta': et, 'testo': testo(a['testo'], verbo=False)}


def _tabella(t):
    """Tabella di un passo: {intestazione: [...], righe: [[...]]}, celle con lo stesso trattamento del testo. Le righe
    con celle vuote sono da compilare a mano: piu' alte."""
    if not t:
        return None
    return {'intestazione': [testo(c, verbo=False) for c in t.get('intestazione', [])],
            'righe': [{'celle': [testo(c, verbo=False) for c in r], 'da_compilare': any(str(c).strip() == '' for c in r)}
                      for r in t['righe']]}


# ---------------------------------------------------------------------------------------------- frecce
def freccia_path(da, a, larg):
    (x0, y0), (x1, y1) = da, a
    lung = math.hypot(x1 - x0, y1 - y0)
    if lung < 1:
        return ''
    ux, uy = (x1 - x0) / lung, (y1 - y0) / lung
    nx, ny = -uy, ux
    hl, hw, sw = min(3.0 * larg, 0.55 * lung), 1.45 * larg, larg / 2
    bx, by = x1 - ux * hl, y1 - uy * hl
    pts = [(x0 + nx * sw, y0 + ny * sw), (bx + nx * sw, by + ny * sw), (bx + nx * hw, by + ny * hw), (x1, y1),
           (bx - nx * hw, by - ny * hw), (bx - nx * sw, by - ny * sw), (x0 - nx * sw, y0 - ny * sw)]
    return 'M' + ' L'.join('%.1f %.1f' % p for p in pts) + ' Z'


# ---------------------------------------------------------------------------------------------- immagini
def piatta(src, dst, colori=64):
    """Alfa su bianco e colori quantizzati senza dithering: i colori piatti si comprimono bene (prova F0). Con gli
    ottetti (15 ottobre 2026, 8 render della guida): 40 KB a immagine contro 183 del taglio mediano a 96 colori, errore
    medio 1 su 255 e massimo 14, invisibile; da 96 a 32 colori il peso non cambia."""
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src).convert('RGBA')
    fondo = Image.new('RGBA', im.size, (255, 255, 255, 255))
    fondo.alpha_composite(im)
    fondo.convert('RGB').quantize(colors=colori, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(dst, optimize=True)


def verifica(png, info, nuovi, bordo=3):
    """Problemi dell'immagine: vuota, tagliata ai bordi, pezzi nuovi o viti poco visibili (passata Workbench)."""
    out = []
    im = Image.open(png).getchannel('A')
    w, h = im.size
    if not im.getbbox():
        return ['vuota']
    for nome, box in (('sinistra', (0, 0, bordo, h)), ('destra', (w - bordo, 0, w, h)), ('alto', (0, 0, w, bordo)),
                      ('basso', (0, h - bordo, w, h))):
        if im.crop(box).getbbox():
            out.append('tagliata a ' + nome)
    vis = info.get('visibili', {})
    for k in nuovi:
        if k in vis and vis[k] < 400:
            out.append('%s poco visibile (%d px)' % (k, vis[k]))
    for k, n in vis.items():
        if not k.startswith(('vite', 'inserto')) or n >= 40:
            continue
        out.append('%s poco visibile (%d px)' % (k, n))
    for e in info.get('etichette', []):
        x, y = e['xy']
        if not (0 <= x <= w and 0 <= y <= h):
            out.append('etichetta %s fuori dall\'immagine' % e['testo'])
    for f in info.get('frecce', []):
        # sotto il 40 % lo spostamento e' quasi lungo la vista: la freccia non dice dove va il pezzo
        if f.get('scorcio', 1) < 0.4:
            out.append('esploso di scorcio (%s, %d %%): cambiare vista o asse' % (f['tipo'], 100 * f['scorcio']))
        for x, y in (f['da'], f['a']):
            if not (0 <= x <= w and 0 <= y <= h):
                out.append('freccia fuori dall\'immagine')
                break
    return out


# ---------------------------------------------------------------------------------------------- pagine
def voce(**kw):
    """Voce di un elenco di pezzi con tutti i campi (il modello usa StrictUndefined per trovare i refusi)."""
    v = {'img': None, 'svg': None, 'qta': 1, 'tot': None, 'nome': '', 'x': None, 'bom': ''}
    v.update(kw)
    return v


class Impaginatore:
    def __init__(self, dati, build, sito):
        self.dati, self.build, self.sito = dati, build, sito
        self.problemi = []
        self.totali = {'viti': {}, 'rondelle': {}, 'inserti': {}, 'distanziali': {}}

    def _img(self, src_rel):
        """Copia piatta del render nel sito; torna il percorso relativo per l'HTML."""
        src = os.path.join(self.build, 'img', src_rel)
        piatta(src, os.path.join(self.sito, 'img', src_rel))
        return 'img/' + src_rel

    def _miniatura(self, comp):
        return self._img('miniature/%s.png' % comp)

    def _voci_viteria(self, e, per=1):
        V = self.dati.viteria
        voci = []
        for tipo, n in sorted(e['viti'].items()):
            v = V['viti'][tipo]
            voci.append(voce(svg=svg_vite(v), qta=n, tot=n * per if per > 1 else None, nome=nome_vite(tipo, v)))
        for tipo, n in e['rondelle'].items():
            voci.append(voce(svg=svg_rondella(V['rondelle'][tipo]), qta=n, tot=n * per if per > 1 else None, nome='rondella M3'))
        for tipo, n in sorted(e['inserti'].items()):
            s = V['inserti'][tipo]
            voci.append(voce(svg=svg_inserto(s), qta=n, tot=n * per if per > 1 else None, nome='inserto %s' % s['filetto']))
        for tipo, n in e['distanziali'].items():
            voci.append(voce(svg=svg_distanziale(V['distanziali'][tipo]), qta=n, tot=n * per if per > 1 else None,
                             nome='distanziale M3 × %g' % V['distanziali'][tipo]['l']))
        return voci

    def _attrezzi(self, chiavi):
        out = []
        for k in chiavi:
            a = self.dati.attrezzi.get(k)
            if a is None:
                self.problemi.append('attrezzo sconosciuto: %s' % k)
                continue
            out.append({'nome': a['nome'], 'icona': a.get('icona', '')})
        return out

    def _pezzo(self, comp):
        return self.dati.pezzi.get(comp) or {'nome': comp}

    def _figura_file(self, rel):
        """Figura che non viene dal CAD (schemi delle schede, foto): copiata nel sito, percorso per l'HTML."""
        src = os.path.join(self.dati.radice, rel)
        dst = os.path.join(self.sito, 'img', 'figure', rel.replace('/', '__'))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        return 'img/figure/' + os.path.basename(dst)

    def passo(self, sez, n, p, el):
        s = sez['sezione']
        sid = s['id']
        img, info = None, {'larghezza': 1, 'altezza': 1, 'frecce': []}
        if S.ha_render(p):
            info = json.load(open(os.path.join(self.build, 'img', sid, p['id'] + '.json'), encoding='utf-8'))
            nuovi = S.entrano(self.dati, p)[0]
            for prob in verifica(os.path.join(self.build, 'img', sid, p['id'] + '.png'), info, nuovi):
                self.problemi.append('%s: %s' % (p['id'], prob))
            img = self._img('%s/%s.png' % (sid, p['id']))
        elif 'figura' in p:
            img = self._figura_file(p['figura'])
        voci = [voce(img=self._miniatura(c), qta=q, nome=self._pezzo(c)['nome'], x=self._pezzo(c).get('x'))
                for c, q in el['pezzi']]
        voci += self._voci_viteria(el)
        voci += [voce(qta=x.get('qta', 1), nome=x['nome'], bom=x.get('bom', '')) for x in el['extra']]
        frecce = [{'tipo': f['tipo'], 'd': freccia_path(f['da'], f['a'], LARGHEZZA_FRECCIA[f['tipo']]), 'bordo': BORDO_FRECCIA}
                  for f in info['frecce']]
        return {'id': p['id'], 'sez': s['numero'], 'n': n, 'titolo': p['titolo'], 'formato': p.get('formato', 'grande'),
                'voci': voci, 'righe': [testo(r) for r in p.get('testo', [])], 'avvisi': [avviso(a) for a in p.get('avvisi', [])],
                'attrezzi': self._attrezzi(el['attrezzi']), 'img': img, 'da_file': 'figura' in p,
                'larghezza': info['larghezza'], 'altezza': info['altezza'], 'frecce': frecce, 'volte': p.get('volte'),
                'etichette': info.get('etichette', []),
                'tabella': _tabella(p.get('tabella')), 'html': None, 'fonti': p.get('fonti', [])}

    def _genera(self, sez, p, n0):
        """Passi generati: glossario (da guida/glossario.yaml, a pagine di 22 termini) e foglio delle viti 1:1 (tutta
        la viteria della guida, con la barra di controllo da 100 mm)."""
        s = sez['sezione']
        base = {'sez': s['numero'], 'formato': 'grande', 'voci': [], 'avvisi': [], 'attrezzi': [], 'img': None,
                'da_file': False, 'larghezza': 1, 'altezza': 1, 'frecce': [], 'etichette': [], 'volte': None,
                'tabella': None, 'html': None, 'fonti': p.get('fonti', []), 'righe': []}
        if p['genera'] == 'glossario':
            with open(os.path.join(self.dati.radice, 'glossario.yaml'), encoding='utf-8') as f:
                g = yaml.safe_load(f) or {}
            voci = sorted(g.items(), key=lambda kv: kv[0].lower())
            out = []
            for i in range(0, len(voci), 22):
                parte = voci[i:i + 22]
                righe = [{'celle': [testo(k, verbo=False), testo(v['definizione'] if isinstance(v, dict) else v, verbo=False)],
                          'da_compilare': False} for k, v in parte]
                out.append(dict(base, id='%s.%d' % (p['id'], len(out) + 1), n=n0 + len(out),
                                titolo='%s, %s–%s' % (p['titolo'], parte[0][0][:1].upper(), parte[-1][0][:1].upper()),
                                tabella={'intestazione': ['Termine', 'Significato'], 'righe': righe}))
            return out
        if p['genera'] == 'viti':
            V = self.dati.viteria
            h = ['<div class="foglio-viti"><div class="controllo"></div><div class="nota">Questa barra deve misurare '
                 '100 mm: se no, ristampa al 100 % senza adattamento alla pagina.</div>', righello(100), '<div class="viteria">']
            for tipo, n in sorted(self.totali['viti'].items()):
                h.append('<div class="voce">%s<span><span class="q">%d×</span> %s</span></div>'
                         % (svg_vite(V['viti'][tipo]), n, nome_vite(tipo, V['viti'][tipo])))
            for tipo, n in sorted(self.totali['rondelle'].items()):
                h.append('<div class="voce">%s<span><span class="q">%d×</span> rondella M3</span></div>' % (svg_rondella(V['rondelle'][tipo]), n))
            for tipo, n in sorted(self.totali['inserti'].items()):
                h.append('<div class="voce">%s<span><span class="q">%d×</span> inserto %s</span></div>'
                         % (svg_inserto(V['inserti'][tipo]), n, V['inserti'][tipo]['filetto']))
            for tipo, n in sorted(self.totali['distanziali'].items()):
                h.append('<div class="voce">%s<span><span class="q">%d×</span> distanziale</span></div>' % (svg_distanziale(V['distanziali'][tipo]), n))
            h.append('</div></div>')
            return [dict(base, id=p['id'], n=n0, titolo=p['titolo'], html=''.join(h),
                         righe=[testo('Appoggia ogni vite sul suo disegno: lunghezza e testa devono coincidere.'),
                                testo('Conta le viti per tipo prima di cominciare una sezione.')])]
        raise ValueError('%s: genera %s sconosciuto (glossario, viti)' % (p['id'], p['genera']))

    def sezione(self, sez):
        s = dict(sez['sezione'])
        s.setdefault('ripeti', 1)
        s.setdefault('unita', 'una')
        s['ripeti_testo'] = s.get('ripeti_testo', '%d×' % s['ripeti'])
        stati = S.stati(self.dati, sez)
        per_passo = [E.passo(self.dati, sez, p, presenti) for p, presenti in stati]
        tot = E.sezione(self.dati, sez, per_passo)
        per = s['ripeti']
        blocchi = []
        for chiave, titolo in (('obiettivo', 'Obiettivo'), ('prima', 'Prima di cominciare'), ('tempo', 'Tempo'),
                               ('stato_elettrico', 'Stato elettrico'), ('note', 'Note')):
            v = s.get(chiave)
            if not v:
                continue
            if isinstance(v, list):
                h = '<ol class="spunte">' + ''.join('<li><span>%s</span></li>' % testo(x, verbo=False) for x in v) + '</ol>'
            else:
                h = '<div>%s</div>' % testo(v, verbo=False)
            blocchi.append({'titolo': titolo, 'html': h})
        apertura = {'tipo': 'apertura', 'sezione': s, 'blocchi': blocchi, 'attrezzi': self._attrezzi(tot['attrezzi']),
                    'molti': len(tot['pezzi']) > 12,
                    'pezzi': [voce(img=self._miniatura(c), qta=q, tot=q * per if per > 1 else None, nome=self._pezzo(c)['nome'],
                                   bom=self._pezzo(c).get('bom', ''), x=self._pezzo(c).get('x')) for c, q in tot['pezzi'].items()],
                    'viteria': self._voci_viteria(tot, per), 'extra': [voce(qta=x.get('qta', 1), nome=x['nome'], bom=x.get('bom', ''))
                                                                       for x in tot['extra']],
                    'fonti': sorted(set(re.findall(r'\bD-0\d\d[a-z]?\b', str(s.get('fonti', [])))))}
        pagine = [apertura]
        for k in ('viti', 'rondelle', 'inserti', 'distanziali'):      # totali della guida per il foglio delle viti
            for t, q in tot[k].items():
                self.totali[k][t] = self.totali[k].get(t, 0) + q * per
        passi = []
        for (p, _), el in zip(stati, per_passo):
            if 'genera' in p:
                passi += self._genera(sez, p, len(passi) + 1)
            else:
                passi.append(self.passo(sez, len(passi) + 1, p, el))
        i = 0
        while i < len(passi):
            e = passi[i]
            if e['formato'] == 'mezzo' and i + 1 < len(passi) and passi[i + 1]['formato'] == 'mezzo':
                gruppo = [e, passi[i + 1]]
            else:
                gruppo = [e]
            i += len(gruppo)
            # a pie' di pagina solo le decisioni: i file e le sezioni citate restano nel YAML per chi verifica
            fonti = list(dict.fromkeys(d for g in gruppo for f in g['fonti'] for d in re.findall(r'\bD-0\d\d[a-z]?\b', str(f))))
            pagine.append({'tipo': 'passi', 'sezione': s, 'passi': gruppo, 'fonti': fonti})
        # la vista finale solo se la sezione ha pezzi montati: una fine.png rimasta da prove vecchie non conta
        monta = s.get('presenti_iniziali') or any(sum(S.entrano(self.dati, p), []) for p, _ in stati)
        fine = os.path.exists(os.path.join(self.build, 'img', s['id'], 'fine.png')) and bool(monta)
        if fine or s.get('controllo'):
            pagine.append({'tipo': 'controllo', 'sezione': s, 'img': self._img('%s/fine.png' % s['id']) if fine else None,
                           'spunte': [testo(x, verbo=False) for x in s.get('controllo', [])],
                           'zampe': ORDINE_ZAMPE if s.get('scheda') else [],
                           'tabella': s.get('scheda', []), 'fonti': []})
        return pagine

    def pagine(self, solo=None):
        corpo = []
        for sez in self.dati.sezioni:
            if solo and sez['sezione']['id'] not in solo:
                continue
            corpo.append((sez['sezione'], self.sezione(sez)))
        pagine = [{'tipo': 'copertina', 'sezione': None, 'img': None, 'fonti': [],
                   'sottotitolo': 'Versione %s · bozza' % self.dati.manifest['versione']},
                  {'tipo': 'indice', 'sezione': None, 'voci': [], 'fonti': []}]
        for _, ps in corpo:
            pagine += ps
        for i, p in enumerate(pagine):
            p['numero'] = i + 1
        k = 2
        for s, ps in corpo:
            k += 1
            pagine[1]['voci'].append({'numero': s['numero'], 'titolo': s['titolo'], 'colore': s.get('colore', '#888'), 'pagina': k})
            k += len(ps) - 1
        return pagine

    def scrivi(self, solo=None):
        os.makedirs(self.sito, exist_ok=True)
        guida = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for cartella in ('css', 'font'):
            shutil.copytree(os.path.join(guida, cartella), os.path.join(self.sito, cartella), dirs_exist_ok=True)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(guida, 'modelli')), autoescape=True,
                                 trim_blocks=True, lstrip_blocks=True, undefined=jinja2.StrictUndefined)
        pagine = self.pagine(solo)
        out = env.get_template('guida.html.j2').render(
            titolo='Hexapod v2 — guida di montaggio', pagine=pagine,
            piede_testo='Hexapod v%s · guida di montaggio · bozza' % self.dati.manifest['versione'])
        p = os.path.join(self.sito, 'index.html')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(out)
        return p, len(pagine)


def comprimi(pdf_path):
    """Riscrive le immagini del PDF come indicizzate (palette), senza perdite. Chrome reincapsula le PNG a palette come
    RGB pieno: sulla guida completa del 12 ottobre 2026 le immagini erano 60 MB e il PDF 98 MB. Le immagini della guida
    hanno al massimo 96 colori (piatta()), quindi la palette le rappresenta esattamente; quelle con piu' colori restano."""
    import zlib

    import numpy as np
    import pikepdf
    with pikepdf.open(pdf_path, allow_overwriting_input=True) as doc:
        # tutti gli oggetti immagine: Chrome le richiama da pattern e form, che page.images non vede
        for img in [o for o in doc.objects if isinstance(o, pikepdf.Stream) and o.get('/Subtype') == '/Image']:
            if img.get('/SMask') is not None:
                continue
            if '/Indexed' in str(img.get('/ColorSpace')):
                continue
            pil = pikepdf.PdfImage(img).as_pil_image()
            if pil.mode != 'RGB':
                continue
            # palette esatta: i colori unici dell'immagine e il loro indice (una quantizzazione li sposterebbe)
            px = np.asarray(pil).reshape(-1, 3)
            colori, indici = np.unique(px, axis=0, return_inverse=True)
            if len(colori) > 256:
                continue                            # piu' di 256 colori: resta com'e'
            img.write(zlib.compress(indici.astype(np.uint8).tobytes(), 9), filter=pikepdf.Name.FlateDecode)
            img.ColorSpace = pikepdf.Array([pikepdf.Name.Indexed, pikepdf.Name.DeviceRGB, len(colori) - 1,
                                            pikepdf.String(colori.astype(np.uint8).tobytes())])
            img.BitsPerComponent = 8
            for k in ('/DecodeParms', '/Decode'):
                if k in img:
                    del img[k]
        doc.save(pdf_path, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)


def pdf(html_path, pdf_path):
    """Stampa con Chrome via Playwright; torna i contenitori che debordano (testo che non sta nella pagina)."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome')
        pagina = browser.new_page()
        pagina.goto('file://' + html_path)
        pagina.wait_for_load_state('networkidle')
        pagina.emulate_media(media='print')
        deborda = pagina.evaluate("""() => [...document.querySelectorAll('[data-controlla]')]
            .filter(e => e.scrollHeight > e.clientHeight + 1 || e.scrollWidth > e.clientWidth + 1)
            .map(e => 'pagina ' + e.closest('.pagina').dataset.numero + ': ' + e.dataset.controlla)
            .concat([...document.querySelectorAll('.pagina table')]
            .filter(t => t.getBoundingClientRect().right > t.closest('[data-controlla], .pagina').getBoundingClientRect().right + 1)
            .map(t => 'pagina ' + t.closest('.pagina').dataset.numero + ": tabella piu' larga della colonna"))""")
        pagina.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True, outline=True, tagged=True)
        browser.close()
    comprimi(pdf_path)
    return deborda


def anteprime(html_path, cartella, pagine=None, px_mm=3.0):
    """PNG di ogni pagina (come stampata) per guardarle senza aprire il PDF; pagine: numeri da 1, None per tutte."""
    from playwright.sync_api import sync_playwright
    os.makedirs(cartella, exist_ok=True)
    if not pagine:                                  # le pagine di prima non devono restare a confondere
        for f in os.listdir(cartella):
            if f.startswith('p') and f.endswith('.png'):
                os.remove(os.path.join(cartella, f))
    fatti = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='chrome')
        pagina = browser.new_page(viewport={'width': 1200, 'height': 900}, device_scale_factor=px_mm * 25.4 / 96)
        pagina.goto('file://' + html_path)
        pagina.emulate_media(media='print')
        pagina.wait_for_load_state('networkidle')
        for el in pagina.query_selector_all('section.pagina'):
            n = int(el.get_attribute('data-numero'))
            if pagine and n not in pagine:
                continue
            p = os.path.join(cartella, 'p%03d.png' % n)
            el.screenshot(path=p)
            fatti.append(p)
        browser.close()
    return fatti
