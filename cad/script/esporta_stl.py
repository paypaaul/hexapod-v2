"""Esporta gli STL delle parti stampate in `cad/stl/`, ognuna nella terna del suo componente (terna della zampa per le
parti della zampa, terna del robot per quelle del corpo: carapace, fascia, visiera e gonne restano allineati e si
caricano insieme nello slicer come un pezzo a due colori). Si lancia in sola lettura dal connettore:
    runpy.run_path('/Users/paul/hexapod-v2/cad/script/esporta_stl.py')['main']()
"""
import json
import os
import time

import adsk.core
import adsk.fusion

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'stl')
PARTI = ('Coxa', 'Coxa_Ponte', 'Femore_A', 'Femore_B', 'Tibia', 'Cover_Femore_A', 'Cover_Femore_B', 'Cover_Tibia', 'Piedino',
         'Corpo_Base', 'Corpo_Chiglia', 'Corpo_Vassoio', 'Corpo_Slitta_Regolatore', 'Corpo_Sportello', 'Corpo_Carapace',
         'Corpo_Fascia', 'Corpo_Visiera', 'Corpo_Gonne', 'Corpo_Sportello_Servizio')


def main(out=OUT):
    t0 = time.time()
    des = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    em = des.exportManager
    esito = {}
    for nome in PARTI:
        comp = des.allComponents.itemByName(nome)
        if comp is None or comp.bRepBodies.count == 0:
            esito[nome] = 'assente'
            continue
        f = os.path.join(out, nome + '.stl')
        op = em.createSTLExportOptions(comp, f)
        op.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
        op.isOneFilePerBody = False
        op.sendToPrintUtility = False
        em.execute(op)
        esito[nome] = round(os.path.getsize(f) / 1024)
    esito['s'] = round(time.time() - t0, 1)
    print(json.dumps(esito))
