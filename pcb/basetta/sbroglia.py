"""Sbroglio della PCB-B (F6, provato in F4): reti speciali con script/sbroglio.py, il resto con Freerouting.

Gira con il Python di KiCad. Passi, ognuno rigenera il PCB con genera_pcb.py:
1. senza piste.json: piazzole e divieti dal PCB, poi potenza e segnali a 5 V con le regole del .kicad_dru
   (VBAT a 1 mm, 5 V a 1 mm dai pin dell'ESP32, larghezze), salvati in piste.json;
2. Freerouting per le altre reti attorno a quelle (script/freerouting.py), che riscrive piste.json con tutto.
Uso: $KP pcb/basetta/sbroglia.py [--solo-speciali]
"""

import json
import os
import subprocess
import sys

import pcbnew

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', 'script'))

import freerouting  # noqa: E402
import genera_contorni  # noqa: E402
import sbroglio  # noqa: E402

# reti con regole a coppie che Freerouting non conosce, nell'ordine (prima la potenza)
SPECIALI = ['VBAT', '5V_REG', '5V_LED', '5V_ESP', 'DATA_TIBIE', 'DATA', 'TX5', 'TX5_3Y', 'Y1', 'DATA2', 'RX5']
FISSE = ('VBAT', '5V_REG', '5V_LED', '5V_ESP')
# segnali a livello 5 V: a 1 mm dai pin dell'ESP32 (piano-pcb.md 4.1, R-09)
CINQUE_VOLT = set(SPECIALI)
LARGHEZZE = {'VBAT': 1.5, '5V_REG': 1.5, '5V_LED': 1.0, '5V_ESP': 0.6, '3V3S': 0.3, '3V3_ESP': 0.3, '3V3_X3': 0.3}
KP = sys.executable


def _rigenera():
    r = subprocess.run([KP, os.path.join(QUI, 'genera_pcb.py')], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stdout + r.stderr)


def _piazzole(board):
    out = []
    for fp in board.GetFootprints():
        for p in fp.Pads():
            s = p.GetSize()
            sx, sy = pcbnew.ToMM(s.x), pcbnew.ToMM(s.y)
            if abs(p.GetOrientationDegrees() % 180 - 90) < 1:
                sx, sy = sy, sx
            if p.GetShape() == pcbnew.PAD_SHAPE_CUSTOM:
                sx, sy = max(sx, 1.0), max(sy, 1.5)    # ponticelli a saldare: mezzaluna 1,0 x 1,5
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
    g = genera_contorni.geometria('basetta')
    robot = [(x - 100, 100 - y) for x, y in g['contorno']]
    aperture = [[(x - 100, 100 - y) for x, y in a] for a in g['aperture']]

    def distanza(a, b, rif):
        if 'VBAT' in (a, b):
            return 0.5 if rif == 'U2' or (rif == 'P1' and 'GND' in (a, b)) else 1.0
        if a in CINQUE_VOLT and rif == 'U1':
            return 1.0
        return 0.2
    return sbroglio.Vincoli(robot, aperture, viet, distanza=distanza)


def speciali(giri=4):
    pcb = os.path.join(QUI, 'basetta.kicad_pcb')
    board = pcbnew.LoadBoard(pcb)
    R, mancate = sbroglio.sbroglia(_piazzole(board), _vincoli(board), LARGHEZZE, (22, -17.5, 78, 17.5), SPECIALI,
                                   fisse=FISSE, giri=giri)
    if mancate:
        raise RuntimeError('reti speciali non sbrogliate: %s' % mancate)
    piste = [[rete, st + '.Cu', w, list(a), list(b)] for rete, st, w, xy in R.piste for a, b in zip(xy, xy[1:])]
    vie = [[rete, x, y, sbroglio.VIA_D, sbroglio.VIA_FORO] for rete, x, y in R.vie]
    with open(os.path.join(QUI, 'piste.json'), 'w', encoding='utf-8') as f:
        json.dump({'origine': 'script/sbroglio.py, reti speciali', 'piste': piste, 'vie': vie}, f)
        f.write('\n')
    return len(piste), len(vie)


def _aperte():
    """Reti con connessioni aperte secondo il DRC di KiCad (massa compresa)."""
    import re
    out = os.path.join(QUI, '..', '..', 'build', 'pcb', 'basetta-aperte.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([os.environ.get('KICAD_CLI', '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'), 'pcb', 'drc',
                    '--format', 'json', '-o', out, os.path.join(QUI, 'basetta.kicad_pcb')], capture_output=True)
    with open(out, encoding='utf-8') as f:
        d = json.load(f)
    reti = set()
    # anche le reti con un errore di distanza o di larghezza (di solito una pista di Freerouting ristretta e poi
    # riportata alla larghezza della regola): si rifanno da capo
    for v in d.get('unconnected_items', []) + [v for v in d.get('violations', [])
                                                if v['type'] in ('clearance', 'track_width')]:
        for i in v['items']:
            m = re.search(r'\[/([^\]]+)\]', i['description'])
            if m:
                reti.add(m.group(1))
    return sorted(reti)


def rifinitura(reti):
    """Le reti che Freerouting lascia aperte, con script/sbroglio.py sui quattro strati, sopra le piste posate."""
    board = pcbnew.LoadBoard(os.path.join(QUI, 'basetta.kicad_pcb'))
    with open(os.path.join(QUI, 'piste.json'), encoding='utf-8') as f:
        d = json.load(f)
    piste = [p for p in d['piste'] if p[0] not in reti]
    vie = [v for v in d['vie'] if v[0] not in reti]
    R = sbroglio.Instradatore(_piazzole(board), _vincoli(board), LARGHEZZE, 22, -17.5, 78, 17.5, strati='F12B')
    R.posate(piste, vie)
    mancate = [r for r in reti if R.instrada(r)]
    nome = {'F': 'F.Cu', 'B': 'B.Cu', '1': 'In1.Cu', '2': 'In2.Cu'}
    piste += [[rete, nome[st], w, list(a), list(b)] for rete, st, w, xy in R.piste for a, b in zip(xy, xy[1:])]
    vie += [[rete, x, y, sbroglio.VIA_D, sbroglio.VIA_FORO] for rete, x, y in R.vie]
    d.update(piste=piste, vie=vie, origine=d['origine'] + '; rifinitura con script/sbroglio.py: ' + ', '.join(reti))
    with open(os.path.join(QUI, 'piste.json'), 'w', encoding='utf-8') as f:
        json.dump(d, f)
        f.write('\n')
    return mancate


def principale(argv):
    if '--rifinitura' in argv:
        aperte = [r for r in _aperte() if r != 'GND']
        if aperte:
            print('rifinitura', aperte, 'non riuscite:', rifinitura(aperte))
            _rigenera()
        return
    if os.path.exists(os.path.join(QUI, 'piste.json')):
        os.remove(os.path.join(QUI, 'piste.json'))
    _rigenera()
    print('speciali', speciali())
    _rigenera()
    if '--solo-speciali' in argv:
        return
    print(freerouting.sbroglia(QUI, int(os.environ.get('PASSATE', '80')), LARGHEZZE))
    _rigenera()
    # dopo ImportSpecctraSES pcbnew non si legge piu' da questo processo: la rifinitura gira in uno nuovo
    subprocess.run([KP, os.path.abspath(__file__), '--rifinitura'], check=True)


if __name__ == '__main__':
    principale(sys.argv[1:])
