"""Strumenti dei circuiti stampati (docs/piano-pcb.md 5.2, pcb/README.md).

I test senza KiCad girano sempre: contorni dal CAD, regole, generatore dello schema. Quelli che chiedono
`kicad-cli` o il Python di KiCad si saltano se mancano; nella CI li esegue il job `pcb`.
Ogni controllo ha il suo caso che deve fallire.
"""
import os
import shutil
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PCB = os.path.join(REPO, 'pcb')
sys.path.insert(0, os.path.join(PCB, 'script'))

import genera_contorni as GC  # noqa: E402
import regole  # noqa: E402
from schema_kicad import Schema  # noqa: E402

KICAD_CLI = os.environ.get('KICAD_CLI', '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
KICAD_PY = os.environ.get('KICAD_PYTHON',
                          '/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3')
con_kicad = pytest.mark.skipif(not os.path.exists(KICAD_CLI), reason='kicad-cli non installato')
con_pcbnew = pytest.mark.skipif(
    not os.path.exists(KICAD_PY) or subprocess.run([KICAD_PY, '-c', 'import pcbnew'], capture_output=True).returncode,
    reason='Python di KiCad con pcbnew non disponibile')


# --- contorni dal CAD

def test_contorni_come_il_piano():
    """Quote scritte nel piano (4.1, 4.2), in terna di KiCad (x + 100, 100 − y)."""
    b = GC.geometria('basetta')
    assert sorted(b['contorno']) == [(122.0, 82.5), (122.0, 117.5), (178.0, 82.5), (178.0, 117.5)]
    assert sorted((x, y) for _, x, y, _ in b['fori']) == [(129.0, 93.2), (129.0, 106.8), (175.5, 93.5), (175.5, 106.5)]
    c = GC.geometria('carapace')
    # con le ali davanti della 2.1.8 (x 45…51 fino a |y| 24)
    assert sorted(c['contorno']) == [(129.5, 85.0), (129.5, 115.0), (145.0, 76.0), (145.0, 85.0), (145.0, 115.0),
                                     (145.0, 124.0), (151.0, 76.0), (151.0, 124.0)]
    assert sorted((x, y) for _, x, y, _ in c['fori']) == [(141.5, 87.5), (141.5, 112.5), (148.0, 87.5), (148.0, 112.5)]
    p = GC.geometria('partitori')
    assert sorted(p['contorno']) == [(144.2, 73.5), (144.2, 81.0), (172.0, 73.5), (172.0, 81.0)]
    assert sorted((x, y) for _, x, y, _ in p['fori']) == [(146.2, 77.25), (169.6, 77.25)]
    assert all(d == 2.4 for g in (b, c, p) for _, _, _, d in g['fori'])


def _pcb_finto(g):
    """Testo di un .kicad_pcb con contorno, fori e zone senza rame come li scrive KiCad 10."""
    righe = ['(kicad_pcb (version 20260206)']
    pts = g['contorno']
    for a, b in zip(pts, pts[1:] + pts[:1]):
        righe.append('(gr_line (start %s %s) (end %s %s) (layer "Edge.Cuts"))' % (a + b))
    for _, x, y, d in g['fori']:
        righe.append('(gr_circle (center %s %s) (end %s %s) (layer "Edge.Cuts"))' % (x, y, x + d / 2, y))
    for nome, strati, punti in g['senza_rame']:
        st = ('(layer "%s")' % strati[0]) if len(strati) == 1 else '(layers %s)' % ' '.join('"%s"' % s for s in strati)
        xy = ' '.join('(xy %s %s)' % p for p in punti)
        righe.append('(zone %s (name "%s") (keepout (tracks not_allowed)) (polygon (pts %s)))' % (st, nome, xy))
    return '\n'.join(righe) + ')\n'


@pytest.mark.parametrize('nome', sorted(GC.SCHEDE))
def test_controllo_contorni_e_casi_di_controllo(tmp_path, nome):
    g = GC.geometria(nome)
    f = tmp_path / (nome + '.kicad_pcb')
    f.write_text(_pcb_finto(g))
    assert GC.controlla(nome, str(f)) == []
    # foro spostato di 0,1
    lav, x, y, d = g['fori'][0]
    spostato = dict(g, fori=[(lav, x + 0.1, y, d)] + g['fori'][1:])
    f.write_text(_pcb_finto(spostato))
    assert any(lav in e for e in GC.controlla(nome, str(f)))
    # zona senza rame mancante
    f.write_text(_pcb_finto(dict(g, senza_rame=g['senza_rame'][1:])))
    assert any('mancante' in e for e in GC.controlla(nome, str(f)))
    # CAD cambiato dopo la scheda: sagoma più larga di 0,5
    f.write_text(_pcb_finto(g))
    par = GC.parametri()
    chiave = GC.SCHEDE[nome]['sagoma'][1]
    par.espressioni[chiave] = '%s + 0.5 mm' % par.espressioni[chiave]
    assert any('contorno' in e for e in GC.controlla(nome, str(f), par))


# --- regole e schema

def test_regole_copiate_in_ogni_progetto():
    assert regole.progetti(), 'nessun progetto KiCad in pcb/'
    assert regole.principale(controlla=True) == 0


def test_schema_ferma_i_pin_senza_rete():
    s = Schema('t', 't', cartella_simboli=os.path.join(PCB, 'librerie'))
    s.simbolo('hex2_kicad:R', 'R1', '1k', 'hex2:R_0805_2012Metric', 50.8, 50.8)
    s.collega('R1', 1, 'A')
    with pytest.raises(ValueError, match='R1 pin 2: senza rete'):
        s.testo()
    s.collega('R1', 2, 'B')
    s.collega('R1', 3, 'C')
    with pytest.raises(ValueError, match='pin che non esiste'):
        s.testo()


# --- con KiCad

def _copia_prova(tmp_path):
    """Copia della scheda di prova con le tabelle delle librerie che puntano a pcb/librerie."""
    d = tmp_path / 'prova'
    shutil.copytree(os.path.join(PCB, 'prova'), d, ignore=shutil.ignore_patterns('__pycache__', '*.net', '*.py'))
    for t in ('sym-lib-table', 'fp-lib-table'):
        p = d / t
        p.write_text(p.read_text().replace('${KIPRJMOD}/../librerie', os.path.join(PCB, 'librerie')))
    return d


@con_kicad
def test_prova_senza_rilievi():
    import controlla
    assert controlla.rilievi(os.path.join(PCB, 'prova')) == []


@con_kicad
def test_erc_trova_pin_scollegato(tmp_path):
    sys.path.insert(0, os.path.join(PCB, 'prova'))
    import controlla
    import genera_schema
    s = genera_schema.schema()
    del s.collegamenti['U3']['2']
    s.libero('U3', 2)  # dichiarato libero ma l'ingresso resta aperto: l'ERC lo segnala
    d = _copia_prova(tmp_path)
    (d / 'prova.kicad_sch').write_text(s.testo())
    tipi = {r[2] for r in controlla.rilievi(str(d), str(tmp_path)) if r[0] == 'ERC'}
    assert 'pin_not_driven' in tipi or 'isolated_pin_label' in tipi


@con_pcbnew
@con_kicad
def test_drc_trova_pista_mancante_e_pista_stretta(tmp_path):
    import controlla
    d = _copia_prova(tmp_path)
    script = (
        'import sys; sys.path[:0] = [%r, %r]\n'
        'import genera_pcb, pcbnew\n'
        's = genera_pcb.scheda(guasto=True, cartella=%r)\n'
        'for t in s.board.GetTracks():\n'
        '    if t.GetNetname() == "/5V_REG" and t.GetClass() == "PCB_TRACK": t.SetWidth(pcbnew.FromMM(1.0))\n'
        's.salva()\n') % (os.path.join(PCB, 'prova'), os.path.join(PCB, 'script'), str(d))
    subprocess.run([KICAD_PY, '-c', script], check=True, capture_output=True)
    r = controlla.rilievi(str(d), str(tmp_path))
    tipi = {x[2] for x in r}
    assert 'unconnected_items' in tipi
    assert any(x[2] == 'track_width' and '5V_REG' in x[3] for x in r)


@con_pcbnew
def test_pcb_ripetibile(tmp_path):
    """Rigenerare la prova dà lo stesso file che è nella repo."""
    d = _copia_prova(tmp_path)
    script = ('import sys; sys.path[:0] = [%r, %r]\nimport genera_pcb\ngenera_pcb.scheda(cartella=%r).salva()\n'
              % (os.path.join(PCB, 'prova'), os.path.join(PCB, 'script'), str(d)))
    subprocess.run([KICAD_PY, '-c', script], check=True, capture_output=True)
    with open(os.path.join(PCB, 'prova', 'prova.kicad_pcb'), encoding='utf-8') as f:
        assert (d / 'prova.kicad_pcb').read_text() == f.read()


@con_kicad
@pytest.mark.parametrize('scheda', ['prova', 'basetta', 'carapace'])
def test_schema_ripetibile(tmp_path, scheda):
    """Rigenerare lo schema dà lo stesso file che è nella repo."""
    import runpy
    mod = runpy.run_path(os.path.join(PCB, scheda, 'genera_schema.py'))
    d = tmp_path / scheda
    d.mkdir()
    # il progetto della repo: il modello di KiCad sta in un posto diverso su Linux
    shutil.copy(os.path.join(PCB, scheda, scheda + '.kicad_pro'), d)
    mod['schema']().salva(str(d))
    with open(os.path.join(PCB, scheda, scheda + '.kicad_sch'), encoding='utf-8') as f:
        assert (d / (scheda + '.kicad_sch')).read_text() == f.read()


@con_kicad
@pytest.mark.parametrize('scheda', ['basetta', 'carapace'])
def test_schemi_senza_rilievi_e_reti_come_la_guida(scheda):
    import controlla
    assert controlla.rilievi(os.path.join(PCB, scheda)) == []


def test_simboli_e_impronte_proprie_aggiornati():
    import propri
    assert propri.principale(controlla=True) == 0


# --- reti di KiCad contro i *_def.py della guida

def _netlist_attesa(scheda):
    """Netlist come la darebbe uno schema di KiCad fatto giusto: reti dei *_def.py con le modifiche di aggiunte.yaml."""
    import verifica_reti as VR
    agg = VR.carica_aggiunte(scheda)
    nodi = {k: r for k, r in VR.carica_def(scheda).items() if k[0] not in agg['tolti']}
    nodi.update(agg['pin'])
    reti = {}
    for (ref, pin), rete in nodi.items():
        nome = ('unconnected-(%s-Pad%s)' % (ref, pin)) if rete is None else '/' + rete.lstrip('+')
        reti.setdefault(nome, []).append((ref, pin))
    return {'componenti': {ref: {} for ref, _ in nodi}, 'reti': reti}


@pytest.mark.parametrize('scheda', ['basetta', 'carapace', 'partitori'])
def test_verifica_reti_e_casi_di_controllo(scheda):
    import copy

    import verifica_reti as VR
    net = _netlist_attesa(scheda)
    assert VR.verifica(scheda, net) == []
    # due pin scambiati fra reti diverse
    guasta = copy.deepcopy(net)
    a, b = [n for n in sorted(guasta['reti']) if not n.startswith('unconnected')][:2]
    guasta['reti'][a][0], guasta['reti'][b][0] = guasta['reti'][b][0], guasta['reti'][a][0]
    assert any('unisce' in e or 'divisa' in e or 'si chiama' in e for e in VR.verifica(scheda, guasta))
    # due reti unite
    guasta = copy.deepcopy(net)
    guasta['reti'][a] += guasta['reti'].pop(b)
    assert any('unisce' in e for e in VR.verifica(scheda, guasta))
    # componente non previsto
    guasta = copy.deepcopy(net)
    guasta['componenti']['Q1'] = {}
    assert any('Q1' in e for e in VR.verifica(scheda, guasta))
    # pin mancante
    guasta = copy.deepcopy(net)
    guasta['reti'][a] = guasta['reti'][a][1:]
    assert any('non esiste' in e for e in VR.verifica(scheda, guasta))


def test_basetta_senza_kamod_e_canale_3_sulla_seriale():
    """DU-1 = sì: TX3 entra in 3A (pin 9 di U3) e arriva all'ESP32 sul GPIO21 (pin 24 della strip)."""
    net = _netlist_attesa('basetta')
    tx3 = set(net['reti']['/TX3'])
    assert tx3 == {('U1', '24'), ('U3', '9')}
    assert 'U4' not in net['componenti']


@con_pcbnew
@con_kicad
def test_step_nella_terna_del_robot(tmp_path):
    """Un foro solo a (40; +10) del robot finisce a (40; +10) nello STEP con --user-origin 100x100mm (cad/CLAUDE.md)."""
    import re
    pcb = tmp_path / 'basetta.kicad_pcb'
    script = ('import sys; sys.path.insert(0, %r)\nfrom scheda_kicad import Scheda\nfrom genera_contorni import kicad\n'
              's = Scheda(None, %r)\ns.contorni_dal_cad("basetta")\ns.foro(*kicad(40, 10), 3.0)\ns.salva()\n'
              % (os.path.join(PCB, 'script'), str(pcb)))
    subprocess.run([KICAD_PY, '-c', script], check=True, capture_output=True)
    step = tmp_path / 'b.step'
    subprocess.run([KICAD_CLI, 'pcb', 'export', 'step', '--board-only', '--user-origin', '100x100mm',
                    '-o', str(step), str(pcb)], check=True, capture_output=True)
    pts = [tuple(map(float, m.groups())) for m in re.finditer(
        r"CARTESIAN_POINT\('[^']*',\(\s*([-\d.E+]+),\s*([-\d.E+]+),\s*([-\d.E+]+)\)\)", step.read_text())]

    def sul_foro(cx, cy):
        return sum(1 for x, y, _ in pts if abs(((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 - 1.5) < 1e-3)
    assert sul_foro(40, 10) > 0
    assert sul_foro(40, -10) == 0
