"""Esporta gli STL delle parti stampate in `cad/stl/`, ognuna nella terna del suo componente (terna della zampa per le
parti della zampa, terna del robot per quelle del corpo: carapace, fascia, visiera e gonne restano allineati e si
caricano insieme nello slicer come un pezzo a due colori). Si lancia dal connettore (accende per un momento i pezzi spenti):
    runpy.run_path('/Users/paul/hexapod-v2/cad/script/esporta_stl.py')['main']()
"""
import json
import os
import runpy
import time

import adsk.core
import adsk.fusion

V = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'versione.py'))
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'stl')
PARTI = ('Coxa', 'Coxa_Ponte', 'Femore_A', 'Femore_B', 'Tibia', 'Cover_Femore_A', 'Cover_Femore_B', 'Cover_Tibia', 'Piedino', 'Cover_Tibia_Diffusore',
         'Corpo_Base', 'Corpo_Chiglia', 'Corpo_Vassoio', 'Corpo_Slitta_Regolatore', 'Corpo_Sportello', 'Corpo_Carapace',
         'Corpo_Fascia', 'Corpo_Visiera', 'Corpo_Gonne', 'Corpo_Sportello_Servizio', 'Corpo_Tappo_ToF',
         'Corpo_Supporto_INA260_S', 'Corpo_Supporto_INA260_D', 'Corpo_Sportello_Servizio_Zaino', 'Corpo_Fondo_Anello')
# attrezzi da banco (attrezzi.py): in cad/stl/attrezzi/
ATTREZZI = ('Dima_Posa_1', 'Dima_Posa_2', 'Attrezzo_Cavalletto')


def main(out=OUT):
    V['controlla'](adsk.core.Application.get())
    t0 = time.time()
    des = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    em = des.exportManager
    esito = {}
    os.makedirs(os.path.join(out, 'attrezzi'), exist_ok=True)
    # Fusion non esporta i corpi nascosti: sportellino dello zaino e attrezzi stanno spenti, si accendono solo qui
    spenti = [o for o in des.rootComponent.allOccurrences
              if o.component.name in PARTI + ATTREZZI and not o.isLightBulbOn]
    for o in spenti:
        o.isLightBulbOn = True
    for nome in PARTI + ATTREZZI:
        comp = des.allComponents.itemByName(nome)
        if comp is None or comp.bRepBodies.count == 0:
            esito[nome] = 'assente'
            continue
        f = os.path.join(out, 'attrezzi' if nome in ATTREZZI else '', nome + '.stl')
        op = em.createSTLExportOptions(comp, f)
        op.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
        op.isOneFilePerBody = False
        op.sendToPrintUtility = False
        em.execute(op)
        esito[nome] = round(os.path.getsize(f) / 1024)
    for o in spenti:
        o.isLightBulbOn = False
    esito['s'] = round(time.time() - t0, 1)
    print(json.dumps(esito))
