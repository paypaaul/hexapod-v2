"""Render e stampa 1:1 di una PCB per le revisioni (R2, piano-pcb.md 5): in `docs/immagini/pcb/`.

- `<scheda>-sopra.png`, `<scheda>-sotto.png`: render 3D di KiCad dall'alto e dal basso del robot;
- `<scheda>-1a1.pdf`: contorno, rame, serigrafia e Fab in scala 1:1 su A4, da stampare al 100 % e controllare con il
  righello (il bordo della scheda è nelle misure del piano) prima di posarci sopra i pezzi veri.
Uso: python3 pcb/script/stampe.py carapace
"""

import os
import subprocess
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
from schema_kicad import KICAD_CLI  # noqa: E402

RADICE = os.path.normpath(os.path.join(QUI, '..', '..'))
USCITA = os.path.join(RADICE, 'docs', 'immagini', 'pcb')


def _kicad(*argomenti):
    r = subprocess.run([KICAD_CLI, *argomenti], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError('kicad-cli %s: %s%s' % (argomenti[:3], r.stdout, r.stderr))


def stampe(scheda):
    pcb = os.path.join(RADICE, 'pcb', scheda, scheda + '.kicad_pcb')
    os.makedirs(USCITA, exist_ok=True)
    fatti = []
    for lato in ('top', 'bottom'):
        out = os.path.join(USCITA, '%s-%s.png' % (scheda, {'top': 'sopra', 'bottom': 'sotto'}[lato]))
        _kicad('pcb', 'render', '--side', lato, '--width', '1600', '--height', '1200', '--quality', 'high',
               '--background', 'opaque', '--zoom', '0.9', '-o', out, pcb)
        fatti.append(out)
    out = os.path.join(USCITA, '%s-1a1.pdf' % scheda)
    _kicad('pcb', 'export', 'pdf', '--mode-single', '--scale', '1', '--ibt', '--sp',
           '--layers', 'Edge.Cuts,F.Cu,B.Cu,F.Silkscreen,B.Silkscreen,F.Fab,B.Fab', '-o', out, pcb)
    fatti.append(out)
    return fatti


if __name__ == '__main__':
    for f in stampe(sys.argv[1]):
        print(os.path.relpath(f, RADICE))
