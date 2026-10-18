"""ERC e DRC (con la parità dello schema) di un progetto KiCad; fallisce su qualunque rilievo, anche gli avvisi.

Uso: python3 controlla.py pcb/prova [pcb/basetta ...]
Il progetto è la cartella con <nome>.kicad_sch e <nome>.kicad_pcb, dove <nome> è il nome della cartella.
I rapporti JSON vanno in build/pcb/<nome>-erc.json e -drc.json.
"""

import json
import os
import subprocess
import sys

KICAD_CLI = os.environ.get('KICAD_CLI', '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
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
    _kicad(['pcb', 'drc', '--schematic-parity', '--severity-all', '--format', 'json', '-o', drc,
            os.path.join(cartella, nome + '.kicad_pcb')])
    out = []
    with open(erc, encoding='utf-8') as f:
        for foglio in json.load(f)['sheets']:
            for v in foglio['violations']:
                out.append(('ERC', v['severity'], v['type'], v['description'], [i['description'] for i in v['items']]))
    with open(drc, encoding='utf-8') as f:
        d = json.load(f)
    for chiave in ('violations', 'unconnected_items', 'schematic_parity'):
        for v in d.get(chiave, []):
            out.append(('DRC ' + chiave, v['severity'], v['type'], v['description'],
                        [i['description'] for i in v['items']]))
    return out


def principale(cartelle):
    errori = 0
    for c in cartelle:
        r = rilievi(c)
        print('%s: %d rilievi' % (c, len(r)))
        for controllo, grav, tipo, descr, elementi in r:
            print('  %s %s %s: %s %s' % (controllo, grav, tipo, descr, elementi))
        errori += len(r)
    return 1 if errori else 0


if __name__ == '__main__':
    sys.exit(principale(sys.argv[1:]))
