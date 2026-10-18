"""Sbroglio della PCB-P con script/sbroglio.py (quattro strati; poche reti, niente regole a coppie): in piste.json.

Gira con il Python di KiCad. Le piazzole e i divieti vengono dal PCB generato da genera_pcb.py; la massa si collega con
le piste e poi con i riempimenti delle due facce. Uso: $KP pcb/partitori/sbroglia.py
"""

import json
import os
import subprocess
import sys

import pcbnew

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', 'script'))
sys.path.insert(0, QUI)

import genera_contorni  # noqa: E402
import sbroglio  # noqa: E402

RETI = ['N6', '3V3S', 'N7'] + ['N%d' % c for c in range(5, -1, -1)] + ['GND']
LARGHEZZE = {'3V3S': 0.3, 'GND': 0.3}


def _piazzole(board):
    out = []
    for fp in board.GetFootprints():
        for p in fp.Pads():
            s = p.GetSize()
            sx, sy = pcbnew.ToMM(s.x), pcbnew.ToMM(s.y)
            if abs(p.GetOrientationDegrees() % 180 - 90) < 1:
                sx, sy = sy, sx
            st = 'FB' if p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH else ('F' if p.IsOnLayer(pcbnew.F_Cu) else 'B')
            x, y = pcbnew.ToMM(p.GetPosition().x) - 100, 100 - pcbnew.ToMM(p.GetPosition().y)
            forma = 'c' if p.GetShape() == pcbnew.PAD_SHAPE_CIRCLE else 'r'
            out.append((fp.GetReference(), p.GetNumber(), x, y, sx, sy, forma, st, p.GetNetname().lstrip('/')))
    return out


def _vincoli(board):
    lettera = {pcbnew.F_Cu: 'F', pcbnew.B_Cu: 'B', pcbnew.In1_Cu: '1', pcbnew.In2_Cu: '2'}
    viet = {'F': [], 'B': [], '1': [], '2': []}
    for z in board.Zones():
        if z.GetIsRuleArea() and z.GetDoNotAllowTracks():
            o = z.Outline().Outline(0)
            pts = [(pcbnew.ToMM(o.CPoint(i).x) - 100, 100 - pcbnew.ToMM(o.CPoint(i).y)) for i in range(o.PointCount())]
            for st in z.GetLayerSet().Seq():
                if st in lettera:
                    viet[lettera[st]].append(pts)
    contorno = [(x - 100, 100 - y) for x, y in genera_contorni.geometria('partitori')['contorno']]
    return sbroglio.Vincoli(contorno, [], viet)


def principale():
    piste_file = os.path.join(QUI, 'piste.json')
    if os.path.exists(piste_file):
        os.remove(piste_file)
    subprocess.run([sys.executable, os.path.join(QUI, 'genera_pcb.py')], check=True, capture_output=True)
    board = pcbnew.LoadBoard(os.path.join(QUI, 'partitori.kicad_pcb'))
    R, mancate = sbroglio.sbroglia(_piazzole(board), _vincoli(board), LARGHEZZE, (44.2, 18.6, 78.0, 27.2), RETI,
                                   strati='F12B',
                                   fisse=('N6', '3V3S', 'N7'), giri=6,
                                   # il 3,3 V tocca tutte le R: sugli strati interni non chiude le altre reti
                                   costi={'3V3S': {'F': 4.0, 'B': 4.0}})
    nome = {'F': 'F.Cu', 'B': 'B.Cu', '1': 'In1.Cu', '2': 'In2.Cu'}
    piste = [[rete, nome[st], w, list(a), list(b)] for rete, st, w, xy in R.piste for a, b in zip(xy, xy[1:])]
    vie = [[rete, x, y, sbroglio.VIA_D, sbroglio.VIA_FORO] for rete, x, y in R.vie]
    with open(piste_file, 'w', encoding='utf-8') as f:
        json.dump({'origine': 'script/sbroglio.py', 'piste': piste, 'vie': vie}, f)
        f.write('\n')
    subprocess.run([sys.executable, os.path.join(QUI, 'genera_pcb.py')], check=True, capture_output=True)
    return mancate


if __name__ == '__main__':
    print('reti non riuscite:', principale())
