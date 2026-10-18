"""Dima stampata 1:1 di una PCB (F5, piano-pcb.md 5): STL della sola scheda, con i fori, nella terna del robot.

Gira con il Python di KiCad (`pcbnew`). Legge `<scheda>/<scheda>.kicad_pcb`, allarga i fori metallizzati di
2 x GIOCO_STAMPA e scrive `cad/stl/attrezzi/Dima_PCB_<Scheda>.stl` con `kicad-cli pcb export stl --board-only`.
Il PCB della repo non cambia: si lavora su una copia in una cartella temporanea.

Perché i fori dei pin si allargano e quelli delle viti no: un foro stampato esce più stretto del disegno di circa il
gioco di stampa per lato (gio_stampa = 0,2, rif_componenti.py), e un pin da 0,64 quadrato (0,9 in diagonale) in un
foro da 1,1 stampato non entrerebbe, dando un falso negativo. I fori Ø2,4 delle viti restano come sulla PCB: se la M2
passa e centra l'inserto nella dima più stretta, passa anche nella scheda vera.
Uso: $KP pcb/script/dima.py carapace [-o file.stl]
"""

import os
import shutil
import subprocess
import sys
import tempfile

import pcbnew

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
from schema_kicad import KICAD_CLI  # noqa: E402

RADICE = os.path.normpath(os.path.join(QUI, '..', '..'))
GIOCO_STAMPA = 0.2   # mm per lato: gio_stampa di cad/script/rif_componenti.py
NOMI = {'carapace': 'Carapace', 'basetta': 'Basetta', 'partitori': 'Partitori'}


def dima(scheda, uscita=None):
    pcb = os.path.join(RADICE, 'pcb', scheda, scheda + '.kicad_pcb')
    uscita = uscita or os.path.join(RADICE, 'cad', 'stl', 'attrezzi', 'Dima_PCB_%s.stl' % NOMI[scheda])
    tmp = tempfile.mkdtemp()
    try:
        copia = os.path.join(tmp, scheda + '.kicad_pcb')
        shutil.copy(pcb, copia)
        board = pcbnew.LoadBoard(copia)
        allargati = 0
        for fp in board.GetFootprints():
            for pad in fp.Pads():
                if pad.GetAttribute() == pcbnew.PAD_ATTRIB_PTH and pad.GetDrillSize().x > 0:
                    d = pad.GetDrillSize()
                    pad.SetDrillSize(pcbnew.VECTOR2I(d.x + pcbnew.FromMM(2 * GIOCO_STAMPA),
                                                     d.y + pcbnew.FromMM(2 * GIOCO_STAMPA)))
                    allargati += 1
        board.Save(copia)
        r = subprocess.run([KICAD_CLI, 'pcb', 'export', 'stl', '--board-only', '--user-origin', '100x100mm',
                            '--force', '-o', uscita, copia], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(uscita):
            raise RuntimeError('kicad-cli non ha scritto la dima (%d): %s%s' % (r.returncode, r.stdout, r.stderr))
    finally:
        shutil.rmtree(tmp)
    return uscita, allargati


if __name__ == '__main__':
    nome = sys.argv[1]
    out = sys.argv[sys.argv.index('-o') + 1] if '-o' in sys.argv else None
    percorso, n = dima(nome, out)
    print('%s: %d fori dei pin allargati di %.1f mm' % (os.path.relpath(percorso, RADICE), n, 2 * GIOCO_STAMPA))
