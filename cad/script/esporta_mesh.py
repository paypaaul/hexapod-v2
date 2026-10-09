"""Esporta le mesh del modello (posa attuale, terna del robot) per i render schematici di `cad/render/render.py`.

Gruppi: base, coperchio, interni, servo_coxa (corpo); zampe_struttura, zampe_servo (sei zampe). STL binari in mm,
qualita' bassa (circa 70 000 triangoli in tutto). Si lancia in sola lettura dal connettore:
    runpy.run_path('/Users/paul/hexapod-v2/cad/script/esporta_mesh.py')['main']()
"""
import json
import os
import struct
import time

import adsk.core
import adsk.fusion

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'render', 'mesh')
SALTA = ('flat', 'linguetta', 'zona_spine_servo', 'zona_barre_retro', 'uscita_cavi')   # ingombri non rigidi o sovrapposti


def _corpi(o):
    r = list(o.bRepBodies)
    for c in o.childOccurrences:
        r += _corpi(c)
    return r


def _gruppi(root):
    gruppi = {}
    corpo = [o for o in root.occurrences if o.component.name == 'Corpo'][0]
    for o in corpo.childOccurrences:
        n = o.component.name
        if n in ('Corpo_Coperchio', 'Corpo_Sportello_Servizio'):
            g = 'coperchio'
        elif n.startswith('Corpo_'):
            g = 'base'
        elif n in ('Rif_Servo_MG996R', 'Rif_Cuscinetto_LF1050ZZ'):
            g = 'servo_coxa'
        else:
            g = 'interni'
        gruppi.setdefault(g, []).extend(b for b in _corpi(o) if b.name not in SALTA)
    for z in [o for o in root.occurrences if o.component.name == 'Zampa']:
        for o in z.childOccurrences:
            g = 'zampe_servo' if o.component.name.startswith('Rif_') else 'zampe_struttura'
            gruppi.setdefault(g, []).extend(_corpi(o))
    return gruppi


def _scrivi_stl(percorso, nome, corpi):
    tri = []
    for b in corpi:
        mc = b.meshManager.createMeshCalculator()
        mc.setQuality(adsk.fusion.TriangleMeshQualityOptions.LowQualityTriangleMesh)
        m = mc.calculate()
        c, idx = m.nodeCoordinatesAsDouble, m.nodeIndices
        for i in range(0, len(idx), 3):
            tri.append([c[3 * k + j] * 10 for k in idx[i:i + 3] for j in range(3)])
    with open(percorso, 'wb') as f:
        f.write(('esapode ' + nome).encode()[:80].ljust(80, b' '))
        f.write(struct.pack('<I', len(tri)))
        for t in tri:
            f.write(struct.pack('<3f', 0, 0, 0) + struct.pack('<9f', *t) + b'\x00\x00')
    return len(tri)


def main(out=OUT):
    t0 = time.time()
    os.makedirs(out, exist_ok=True)
    root = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct).rootComponent
    esito = {g: _scrivi_stl(os.path.join(out, g + '.stl'), g, c) for g, c in _gruppi(root).items()}
    esito['s'] = round(time.time() - t0, 1)
    print(json.dumps(esito))
