"""Aspetti (colori) dei pezzi nel design, per materiale (D-065): PETG-CF nero per le parti funzionali, PLA per le placche
(bianco per ora) e per fascia, visiera, gonne e sportellino (nero), TPU arancio per i piedini; colori plausibili per le
parti comprate generate come ingombri. I modelli STEP di terzi (servo, regolatori) tengono i loro colori.

Gli aspetti nuovi si copiano dalla libreria di Fusion con un nome proprio ("Esa ...") e si assegnano ai corpi del
componente, quindi valgono per tutte le istanze. Per cambiare il colore delle placche basta cambiare COLORI['Esa PLA
placche']. Uso dal connettore: runpy.run_path(percorso)['main']()
"""
import json
import os
import runpy
import traceback

import adsk.core
import adsk.fusion

V = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'versione.py'))
LIBRERIA = 'Libreria aspetti di Fusion'
# nome nel design: (aspetto di partenza nella libreria, colore RGB o None per tenere quello della libreria)
COLORI = {
    'Esa PETG-CF nero': ('Plastica - Opaco (nero)', (42, 42, 45)),
    'Esa PLA placche': ('Plastica - Opaco (bianco)', (236, 236, 232)),
    'Esa PLA nero': ('Plastica - Lucido (nero)', (16, 16, 18)),
    'Esa TPU arancio': ('Gomma - Morbido', (255, 98, 16)),
    'Esa acciaio': ('Acciaio inossidabile - Satinato', None),
    'Esa alluminio': ('Alluminio - Satinato', None),
    'Esa scheda verde': ('Plastica - Lucido (verde)', (24, 92, 48)),
    'Esa scheda blu': ('Plastica - Lucido (blu)', (26, 56, 132)),
    'Esa plastica nera': ('Plastica - Lucido (nero)', (30, 30, 32)),
    'Esa batteria': ('Plastica - Lucido (grigio)', (52, 54, 60)),
    'Esa grigio chiaro': ('Plastica - Opaco (grigio)', (192, 194, 197)),
    'Esa rosso': ('Plastica - Lucido (rosso)', (196, 30, 30)),
}
PARTI = {
    # PETG-CF nero: tutte le parti funzionali
    'Coxa': 'Esa PETG-CF nero', 'Coxa_Ponte': 'Esa PETG-CF nero', 'Femore_A': 'Esa PETG-CF nero',
    'Femore_B': 'Esa PETG-CF nero', 'Tibia': 'Esa PETG-CF nero', 'Corpo_Base': 'Esa PETG-CF nero',
    'Corpo_Chiglia': 'Esa PETG-CF nero', 'Corpo_Slitta_Regolatore': 'Esa PETG-CF nero', 'Corpo_Sportello': 'Esa PETG-CF nero',
    # PLA: placche e vassoio (sotto l'antenna), parti nere stampate con il carapace
    'Corpo_Carapace': 'Esa PLA placche', 'Cover_Femore_A': 'Esa PLA placche', 'Cover_Femore_B': 'Esa PLA placche',
    'Cover_Tibia': 'Esa PLA placche', 'Corpo_Vassoio': 'Esa PLA placche', 'Cover_Tibia_Diffusore': 'Esa PLA placche',
    'Corpo_Fascia': 'Esa PLA nero', 'Corpo_Visiera': 'Esa PLA nero', 'Corpo_Gonne': 'Esa PLA nero',
    'Corpo_Sportello_Servizio': 'Esa PLA nero',
    'Piedino': 'Esa TPU arancio',
    'Corpo_Tappo_ToF': 'Esa PLA nero', 'Corpo_Fondo_Anello': 'Esa PLA nero', 'Corpo_Sportello_Servizio_Zaino': 'Esa PLA nero',
    'Corpo_Supporto_INA260_S': 'Esa PETG-CF nero', 'Corpo_Supporto_INA260_D': 'Esa PETG-CF nero',
    'Dima_Posa_1': 'Esa PLA placche', 'Dima_Posa_2': 'Esa PLA placche', 'Attrezzo_Cavalletto': 'Esa PETG-CF nero',
    'Rif_IMU': 'Esa scheda blu', 'Rif_ADC_ADS7830': 'Esa scheda blu', 'Rif_INA260': 'Esa scheda blu', 'Rif_ToF_8x8': 'Esa scheda verde',
    'Rif_ToF_1': 'Esa scheda verde', 'Rif_Ampli_MAX98357A': 'Esa scheda blu', 'Rif_Altoparlante': 'Esa plastica nera',
    'Rif_Microfono_I2S': 'Esa scheda blu', 'Rif_FSR_400': 'Esa grigio chiaro', 'Rif_Scheda_Carapace': 'Esa scheda verde',
    'Rif_Prese_Piedi': 'Esa plastica nera', 'Rif_Computer_Zaino': 'Esa scheda verde',
    # comprati (ingombri generati)
    'Ingombro_Teste_A': 'Esa acciaio', 'Rif_Cuscinetto_LF1050ZZ': 'Esa acciaio', 'Rif_Perno_5': 'Esa acciaio',
    'Rif_Squadretta_25T': 'Esa alluminio', 'Rif_Pulsante_12': 'Esa acciaio',
    'Rif_Batteria_2S5200': 'Esa batteria', 'Rif_SSC32_V25': 'Esa scheda blu', 'Rif_ESP32_S3_CAM': 'Esa plastica nera',
    'Rif_Camera_OV3660_75': 'Esa plastica nera', 'Rif_Basetta_50x70': 'Esa scheda verde',
    'Rif_Interruttore_Pololu_2813': 'Esa scheda verde', 'Rif_Portafusibile_ATO': 'Esa plastica nera',
    'Rif_Wago_221_415': 'Esa grigio chiaro', 'Rif_Tplug': 'Esa rosso', 'Rif_Cicalino_BX100': 'Esa plastica nera',
    'Rif_Condensatore_2200uF': 'Esa plastica nera',
}


def aspetto(des, nome):
    """Aspetto del design con questo nome; se manca lo copia dalla libreria. Il colore si riallinea sempre a COLORI."""
    base, rgb = COLORI[nome]
    a = des.appearances.itemByName(nome)
    if a is None:
        lib = adsk.core.Application.get().materialLibraries.itemByName(LIBRERIA)
        a = des.appearances.addByCopy(lib.appearances.itemByName(base), nome)
    if rgb is not None:
        pr = a.appearanceProperties.itemById('opaque_albedo')
        if pr is None:
            raise RuntimeError('l\'aspetto %s (da %s) non ha la proprieta opaque_albedo' % (nome, base))
        adsk.core.ColorProperty.cast(pr).value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 0)
    return a


def main():
    out = {}
    try:
        V['controlla'](adsk.core.Application.get())
        des = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
        cache = {}
        for comp_nome, a_nome in PARTI.items():
            comp = des.allComponents.itemByName(comp_nome)
            if comp is None:
                out[comp_nome] = 'assente'
                continue
            if a_nome not in cache:
                cache[a_nome] = aspetto(des, a_nome)
            a = cache[a_nome]
            for b in comp.bRepBodies:
                b.appearance = a
            # facce con un aspetto proprio (copiate da import o lavorazioni) che resterebbero dell'altro colore
            diverse = sum(1 for b in comp.bRepBodies for f in b.faces if f.appearance and f.appearance.name != a_nome)
            out[comp_nome] = a_nome if not diverse else '%s (%d facce diverse)' % (a_nome, diverse)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, ensure_ascii=False))
