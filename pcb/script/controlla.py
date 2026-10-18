"""ERC, DRC con la parità dello schema e reti contro la guida di un progetto KiCad; fallisce su qualunque rilievo.

Senza .kicad_pcb (schema fatto, PCB non ancora) il DRC si salta e lo si scrive.

Uso: python3 controlla.py pcb/prova [pcb/basetta ...]
Il progetto è la cartella con <nome>.kicad_sch e <nome>.kicad_pcb, dove <nome> è il nome della cartella.
I rapporti JSON vanno in build/pcb/<nome>-erc.json e -drc.json.
"""

import json
import os
import subprocess
import sys

import verifica_reti
import yaml

KICAD_CLI = os.environ.get('KICAD_CLI', '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
NON_SBROGLIATE = {}
SERIGRAFIA = {}
RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def _kicad(args):
    r = subprocess.run([KICAD_CLI] + args, capture_output=True, text=True)
    if r.returncode not in (0, 5):  # 5 = rilievi trovati, li legge il JSON
        raise RuntimeError('kicad-cli %s: uscita %d\n%s%s' % (' '.join(args), r.returncode, r.stdout, r.stderr))


def rilievi(cartella, uscite=None):
    """[(controllo, gravità, tipo, descrizione, elementi)] di ERC e DRC del progetto."""
    nome = os.path.basename(os.path.abspath(cartella))
    uscite = uscite or os.path.join(RADICE, 'build', 'pcb')
    os.makedirs(uscite, exist_ok=True)
    erc = os.path.join(uscite, nome + '-erc.json')
    drc = os.path.join(uscite, nome + '-drc.json')
    _kicad(['sch', 'erc', '--severity-all', '--format', 'json', '-o', erc,
            os.path.join(cartella, nome + '.kicad_sch')])
    out = []
    pcb = os.path.join(cartella, nome + '.kicad_pcb')
    if os.path.exists(pcb):
        _kicad(['pcb', 'drc', '--schematic-parity', '--severity-all', '--format', 'json', '-o', drc, pcb])
    # reti contro la guida, per le schede che hanno un *_def.py
    if nome in verifica_reti.DEF:
        net = os.path.join(uscite, nome + '.net')
        _kicad(['sch', 'export', 'netlist', '--format', 'kicadsexpr', '-o', net,
                os.path.join(cartella, nome + '.kicad_sch')])
        for e in verifica_reti.verifica(nome, verifica_reti.leggi_netlist(net)):
            out.append(('reti', 'error', 'verifica_reti', e, []))
    with open(erc, encoding='utf-8') as f:
        for foglio in json.load(f)['sheets']:
            for v in foglio['violations']:
                out.append(('ERC', v['severity'], v['type'], v['description'], [i['description'] for i in v['items']]))
    if not os.path.exists(pcb):
        return out
    with open(drc, encoding='utf-8') as f:
        d = json.load(f)
    # prima dello sbroglio (pcb/stato.yaml: piazzamento) le connessioni mancanti sono attese: si contano a parte
    with open(os.path.join(RADICE, 'pcb', 'stato.yaml'), encoding='utf-8') as f:
        fase = (yaml.safe_load(f) or {}).get(nome, 'sbroglio')
    for chiave in ('violations', 'unconnected_items', 'schematic_parity'):
        if chiave == 'unconnected_items' and fase == 'piazzamento':
            NON_SBROGLIATE[nome] = len(d.get(chiave, []))
            continue
        for v in d.get(chiave, []):
            if fase == 'piazzamento' and v['type'].startswith('silk_'):
                SERIGRAFIA[nome] = SERIGRAFIA.get(nome, 0) + 1
                continue
            out.append(('DRC ' + chiave, v['severity'], v['type'], v['description'],
                        [i['description'] for i in v['items']]))
    return out


def principale(cartelle):
    errori = 0
    for c in cartelle:
        r = rilievi(c)
        nome = os.path.basename(os.path.abspath(c))
        senza = '' if os.path.exists(os.path.join(c, nome + '.kicad_pcb')) else ' (PCB non ancora: solo ERC e reti)'
        if nome in NON_SBROGLIATE:
            senza = (' (piazzamento: %d connessioni da sbrogliare e %d avvisi di serigrafia, non contati)'
                     % (NON_SBROGLIATE[nome], SERIGRAFIA.get(nome, 0)))
        print('%s: %d rilievi%s' % (c, len(r), senza))
        for controllo, grav, tipo, descr, elementi in r:
            print('  %s %s %s: %s %s' % (controllo, grav, tipo, descr, elementi))
        errori += len(r)
    return 1 if errori else 0


if __name__ == '__main__':
    sys.exit(principale(sys.argv[1:]))
