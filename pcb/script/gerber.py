"""Gerber e forature di una PCB per JLCPCB, in uno zip (F7, piano-pcb.md 5.6).

Strati di rame secondo la scheda (2 o 4), maschere, serigrafie e contorno; forature Excellon in mm, fori metallizzati
e non metallizzati in due file. Estensioni Protel (quelle che il sito di JLCPCB riconosce da solo). Lo zip va in
build/gerber/: si copia in pcb/ordini/r1/ solo quello che si manda davvero.
Uso: python3 pcb/script/gerber.py basetta [partitori ...]
"""

import os
import shutil
import subprocess
import sys
import tempfile

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
from schema_kicad import KICAD_CLI  # noqa: E402

RADICE = os.path.normpath(os.path.join(QUI, '..', '..'))
USCITA = os.path.join(RADICE, 'build', 'gerber')


def strati_di_rame(pcb):
    with open(pcb, encoding='utf-8') as f:
        testo = f.read()
    return ['F.Cu'] + [s for s in ('In1.Cu', 'In2.Cu') if '"%s"' % s in testo.split('(setup')[0]] + ['B.Cu']


def gerber(scheda):
    pcb = os.path.join(RADICE, 'pcb', scheda, scheda + '.kicad_pcb')
    strati = strati_di_rame(pcb) + ['F.Mask', 'B.Mask', 'F.Silkscreen', 'B.Silkscreen', 'Edge.Cuts']
    tmp = tempfile.mkdtemp()
    try:
        for argomenti in (['pcb', 'export', 'gerbers', '--check-zones', '-l', ','.join(strati), '-o', tmp, pcb],
                          ['pcb', 'export', 'drill', '--excellon-separate-th', '-u', 'mm', '-o', tmp, pcb]):
            r = subprocess.run([KICAD_CLI] + argomenti, capture_output=True, text=True)
            if r.returncode:
                raise RuntimeError('kicad-cli %s: %s%s' % (argomenti[2], r.stdout, r.stderr))
        os.makedirs(USCITA, exist_ok=True)
        zip_ = shutil.make_archive(os.path.join(USCITA, 'HEX2-%s-r1-gerber' % scheda), 'zip', tmp)
        return zip_, sorted(os.listdir(tmp))
    finally:
        shutil.rmtree(tmp)


if __name__ == '__main__':
    for nome in sys.argv[1:]:
        z, file = gerber(nome)
        print(os.path.relpath(z, RADICE), len(file), 'file:', ', '.join(file))
