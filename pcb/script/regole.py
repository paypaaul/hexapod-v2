"""Copia la fonte unica delle regole del DRC (pcb/regole/hex2.kicad_dru) in ogni progetto come <nome>.kicad_dru.

Uso: python3 regole.py              copia
     python3 regole.py --controlla  fallisce se una copia manca o è diversa
"""

import glob
import os
import sys

PCB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
FONTE = os.path.join(PCB, 'regole', 'hex2.kicad_dru')


def progetti():
    return sorted(os.path.dirname(p) for p in glob.glob(os.path.join(PCB, '*', '*.kicad_pro')))


def principale(controlla):
    with open(FONTE, encoding='utf-8') as f:
        testo = f.read()
    diversi = []
    for cartella in progetti():
        copia = os.path.join(cartella, os.path.basename(cartella) + '.kicad_dru')
        if controlla:
            if not os.path.exists(copia) or open(copia, encoding='utf-8').read() != testo:
                diversi.append(copia)
        else:
            with open(copia, 'w', encoding='utf-8') as f:
                f.write(testo)
    if diversi:
        print('regole diverse dalla fonte %s:\n  %s' % (FONTE, '\n  '.join(diversi)))
        return 1
    print('%d progetti %s' % (len(progetti()), 'controllati' if controlla else 'aggiornati'))
    return 0


if __name__ == '__main__':
    sys.exit(principale('--controlla' in sys.argv))
