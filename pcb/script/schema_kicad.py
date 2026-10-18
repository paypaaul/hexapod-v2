"""Schema di KiCad 10 generato da script.

Ogni pin collegato riceve un tratto di filo verso l'esterno e un'etichetta con il nome della rete;
i pin non usati ricevono il segno di non collegato. Non ci sono fili fra un simbolo e l'altro: le reti
le fanno le etichette, così lo schema si legge per simbolo e il generatore non deve sbrogliare niente.
Gli identificativi (uuid) sono derivati dai nomi: rigenerare lo stesso schema dà lo stesso file.
"""

import copy
import math
import os
import subprocess
import uuid

from sexpr import S, Sym, figli, figlio, leggi, scrivi

LIBRERIE_SIMBOLI = os.environ.get(
    'KICAD10_SYMBOL_DIR', '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols')
VERSIONE_SCH = 20260306
KICAD_CLI = os.environ.get('KICAD_CLI', '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
PASSO = 2.54
TRATTO = 2.54  # filo fra il pin e l'etichetta

_NS = uuid.UUID('6b1d2f0e-6e0c-4d0a-9a51-4865786132a0')  # spazio dei nomi del progetto "Hex2"
_cache_lib = {}


def uid(*parti):
    return str(uuid.uuid5(_NS, '/'.join(str(p) for p in parti)))


def _libreria(nome, cartella=None):
    percorso = os.path.join(cartella or LIBRERIE_SIMBOLI, nome + '.kicad_sym')
    if percorso not in _cache_lib:
        with open(percorso, encoding='utf-8') as f:
            _cache_lib[percorso] = leggi(f.read())
    return _cache_lib[percorso]


def simbolo_libreria(lib_id, cartella=None):
    """Simbolo appiattito (senza `extends`), con il nome 'Lib:Nome' come lo vuole lo schema."""
    lib, nome = lib_id.split(':')
    radice = _libreria(lib, cartella)
    trovati = {x[1]: x for x in figli(radice, 'symbol')}
    if nome not in trovati:
        raise KeyError('simbolo %s non trovato nella libreria %s' % (nome, lib))
    sim = copy.deepcopy(trovati[nome])
    padre = figlio(sim, 'extends')
    if padre:
        base = copy.deepcopy(trovati[padre[1]])
        proprieta = figli(sim, 'property')
        nuovo = [Sym('symbol'), nome]
        for x in base[2:]:
            if isinstance(x, list) and x[0] == 'property':
                continue
            if isinstance(x, list) and x[0] == 'symbol':
                x[1] = nome + x[1][len(padre[1]):]
            nuovo.append(x)
        # le proprietà del figlio vanno prima dei sotto-simboli, come nel file di KiCad
        i = next(i for i, x in enumerate(nuovo) if isinstance(x, list) and x[0] == 'symbol')
        sim = nuovo[:i] + proprieta + nuovo[i:]
    sim[1] = lib_id
    return sim


def pin_del_simbolo(sim):
    """{(unità, numero): (x, y, angolo, tipo)} in coordinate della libreria (Y in alto); unità 0 = comune."""
    nome = sim[1].split(':')[-1]
    pin = {}
    for sotto in figli(sim, 'symbol'):
        unita, stile = (int(v) for v in sotto[1][len(nome) + 1:].split('_'))
        if stile not in (0, 1):
            continue
        for p in figli(sotto, 'pin'):
            at = figlio(p, 'at')
            numero = figlio(p, 'number')[1]
            pin[(unita, numero)] = (float(at[1]), float(at[2]), float(at[3]) if len(at) > 3 else 0.0, str(p[1]))
    return pin


def _font():
    return S('effects', S('font', S('size', 1.27, 1.27)))


class Schema:
    def __init__(self, progetto, titolo, carta='A3', cartella_simboli=None):
        self.progetto = progetto
        self.titolo = titolo
        self.carta = carta
        self.cartella = cartella_simboli
        self.uuid = uid(progetto, 'foglio')
        self.lib = {}        # lib_id -> simbolo appiattito
        self.istanze = []    # (lib_id, ref, unità, x, y, campi)
        self.collegamenti = {}  # (ref, unità) -> {numero: rete}
        self.non_collegati = set()  # (ref, numero)

    def simbolo(self, lib_id, ref, valore, impronta, x, y, unita=1, campi=None):
        if lib_id not in self.lib:
            self.lib[lib_id] = simbolo_libreria(lib_id, self.cartella)
        campi = dict(campi or {})
        campi.update({'Reference': ref, 'Value': valore, 'Footprint': impronta})
        self.istanze.append((lib_id, ref, unita, x, y, campi))

    def collega(self, ref, numero, rete):
        self.collegamenti.setdefault(ref, {})[str(numero)] = rete

    def libero(self, ref, numero):
        self.non_collegati.add((ref, str(numero)))

    # --- costruzione del file ---

    def _pin_istanza(self, lib_id, unita):
        tutti = pin_del_simbolo(self.lib[lib_id])
        return {n: v for (u, n), v in tutti.items() if u in (0, unita)}

    def reti(self):
        """{rete: [(ref, numero)]}: per il controllo, uguale a quello che leggerà KiCad."""
        out = {}
        for ref, pins in self.collegamenti.items():
            for n, r in pins.items():
                out.setdefault(r, []).append((ref, n))
        return out

    def _controlla(self):
        """Ogni pin di ogni unità piazzata è collegato o dichiarato libero, e niente di più."""
        visti = set()
        errori = []
        for lib_id, ref, unita, _, _, _ in self.istanze:
            for n in self._pin_istanza(lib_id, unita):
                visti.add((ref, n))
                c = n in self.collegamenti.get(ref, {})
                libero = (ref, n) in self.non_collegati
                if c == libero:
                    errori.append('%s pin %s: %s' % (ref, n, 'collegato e libero' if c else 'senza rete'))
        for ref, pins in self.collegamenti.items():
            for n in pins:
                if (ref, n) not in visti:
                    errori.append('%s pin %s: rete %s su un pin che non esiste' % (ref, n, pins[n]))
        if errori:
            raise ValueError('schema incoerente:\n  ' + '\n  '.join(errori))

    def testo(self):
        self._controlla()
        corpo = [Sym('kicad_sch'), S('version', VERSIONE_SCH), S('generator', 'hex2_schema'),
                 S('generator_version', '10.0'), S('uuid', self.uuid), S('paper', self.carta),
                 S('title_block', S('title', self.titolo), S('rev', 'r1'),
                   S('comment', 1, 'Generato da pcb/script: non modificare a mano'))]
        corpo.append([Sym('lib_symbols')] + [self.lib[k] for k in sorted(self.lib)])
        elementi = []
        for lib_id, ref, unita, x, y, campi in self.istanze:
            elementi += self._istanza(lib_id, ref, unita, x, y, campi)
        corpo += elementi
        corpo.append(S('sheet_instances', S('path', '/', S('page', '1'))))
        corpo.append(S('embedded_fonts', Sym('no')))
        return scrivi(corpo) + '\n'

    def _istanza(self, lib_id, ref, unita, x, y, campi):
        sim = self.lib[lib_id]
        u = uid(self.progetto, 'simbolo', ref, unita)
        nodo = [Sym('symbol'), S('lib_id', lib_id), S('at', x, y, 0), S('unit', unita),
                S('exclude_from_sim', Sym('no')), S('in_bom', Sym('yes')), S('on_board', Sym('yes')),
                S('dnp', Sym('yes' if campi.pop('DNP', False) else 'no')), S('uuid', u)]
        dy = 0
        for p in figli(sim, 'property'):
            nome = p[1]
            if nome.startswith('ki_'):  # parole chiave e filtri restano nella libreria, come negli schemi di KiCad
                continue
            valore = campi.pop(nome, p[2])
            nascosto = nome not in ('Reference', 'Value')
            at = S('at', x + 2.54, y - 2.54 - dy, 0) if not nascosto else S('at', x, y, 0)
            if not nascosto:
                dy -= 2.54
            eff = _font()
            if nascosto:
                eff.append(S('hide', Sym('yes')))
            else:
                eff.append(S('justify', Sym('left')))
            nodo.append(S('property', nome, valore, at, eff))
        for nome, valore in campi.items():
            nodo.append(S('property', nome, valore, S('at', x, y, 0), _font() + [S('hide', Sym('yes'))]))
        pins = self._pin_istanza(lib_id, unita)
        # KiCad tiene in ogni unità l'elenco di tutti i pin del simbolo: se ne manca uno gli dà un uuid a caso
        for n in sorted({n for (_, n) in pin_del_simbolo(sim)}, key=_ordine_pin):
            nodo.append(S('pin', n, S('uuid', uid(self.progetto, 'pin', ref, unita, n))))
        nodo.append(S('instances', S('project', self.progetto,
                                     S('path', '/' + self.uuid, S('reference', ref), S('unit', unita)))))
        out = [nodo]
        reti = self.collegamenti.get(ref, {})
        for n, (px, py, ang, _) in pins.items():
            cx, cy = x + px, y - py
            if n in reti:
                dx, dy_ = -math.cos(math.radians(ang)), math.sin(math.radians(ang))
                ex, ey = round(cx + dx * TRATTO, 4), round(cy + dy_ * TRATTO, 4)
                out.append(S('wire', S('pts', S('xy', cx, cy), S('xy', ex, ey)),
                             S('stroke', S('width', 0), S('type', Sym('solid'))),
                             S('uuid', uid(self.progetto, 'filo', ref, n))))
                ang_et = {0: 180, 180: 0, 90: 270, 270: 90}[int(ang) % 360]
                giust = {0: 'left', 180: 'right', 90: 'left', 270: 'right'}[ang_et]
                out.append(S('label', reti[n], S('at', ex, ey, ang_et),
                             _font() + [S('justify', Sym(giust), Sym('bottom'))],
                             S('uuid', uid(self.progetto, 'etichetta', ref, n))))
            elif (ref, n) in self.non_collegati:
                out.append(S('no_connect', S('at', cx, cy), S('uuid', uid(self.progetto, 'nc', ref, n))))
        return out

    def salva(self, cartella):
        percorso = os.path.join(cartella, self.progetto + '.kicad_sch')
        with open(percorso, 'w', encoding='utf-8') as f:
            f.write(self.testo())
        # KiCad riscrive il file nel suo formato: così una modifica fatta poi nell'editor dà un diff piccolo
        subprocess.run([KICAD_CLI, 'sch', 'upgrade', '--force', percorso], check=True, capture_output=True)
        return percorso


def _ordine_pin(n):
    return (0, int(n)) if n.isdigit() else (1, n)


_TABELLA = '(%s\n\t(version 7)\n%s)\n'
_RIGA = '\t(lib (name "%s") (type "KiCad") (uri "${KIPRJMOD}/../librerie/%s") (options "") (descr "%s"))\n'


def scrivi_progetto(cartella, nome):
    """File di progetto e tabelle delle librerie del progetto (solo pcb/librerie, niente librerie di sistema)."""
    modello = os.path.join(os.path.dirname(LIBRERIE_SIMBOLI), 'template', 'kicad.kicad_pro')
    pro = os.path.join(cartella, nome + '.kicad_pro')
    if not os.path.exists(pro):
        with open(modello, encoding='utf-8') as f:
            testo = f.read()
        with open(pro, 'w', encoding='utf-8') as f:
            f.write(testo.replace('"filename": "kicad.kicad_pro"', '"filename": "%s.kicad_pro"' % nome))
    with open(os.path.join(cartella, 'sym-lib-table'), 'w', encoding='utf-8') as f:
        f.write(_TABELLA % ('sym_lib_table',
                            _RIGA % ('hex2_kicad', 'hex2_kicad.kicad_sym', 'copie dalle librerie di KiCad 10')))
    with open(os.path.join(cartella, 'fp-lib-table'), 'w', encoding='utf-8') as f:
        f.write(_TABELLA % ('fp_lib_table', _RIGA % ('hex2', 'hex2.pretty', 'impronte del progetto e copie')))


def netlist(sch, uscita):
    """Netlist dello schema: {'componenti': {ref: {...}}, 'reti': {nome: [(ref, pin)]}}."""
    subprocess.run([KICAD_CLI, 'sch', 'export', 'netlist', '--format', 'kicadsexpr', '-o', uscita, sch],
                   check=True, capture_output=True)
    return leggi_netlist(uscita)


def leggi_netlist(uscita):
    """Netlist di KiCad (formato kicadsexpr) già esportata."""
    with open(uscita, encoding='utf-8') as f:
        n = leggi(f.read())
    comp = {}
    for c in figli(figlio(n, 'components'), 'comp'):
        ref = figlio(c, 'ref')[1]
        foglio = figlio(c, 'sheetpath')
        prop = {figlio(p, 'name')[1]: (figlio(p, 'value') or [None, ''])[1] for p in figli(c, 'property')}
        campi = {figlio(f, 'name')[1]: (f[2] if len(f) > 2 else '') for f in figli(figlio(c, 'fields'), 'field')}
        comp[ref] = {
            'valore': figlio(c, 'value')[1],
            'impronta': figlio(c, 'footprint')[1],
            # le unità di un simbolo a più unità hanno un tstamp l'una: KiCad usa il primo
            'percorso': figlio(foglio, 'tstamps')[1] + figlio(c, 'tstamps')[1],
            'foglio': prop.get('Sheetname', ''),
            'file_foglio': prop.get('Sheetfile', ''),
            'campi': campi,
            'fuori_distinta': 'exclude_from_bom' in prop,
            'non_montare': 'dnp' in prop,
        }
    reti = {}
    for r in figli(figlio(n, 'nets'), 'net'):
        reti[figlio(r, 'name')[1]] = [(figlio(x, 'ref')[1], figlio(x, 'pin')[1]) for x in figli(r, 'node')]
    return {'componenti': comp, 'reti': reti}
