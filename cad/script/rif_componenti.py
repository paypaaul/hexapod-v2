"""Parametri utente e componenti di riferimento (parti comprate) del design di lavoro (`versione.py`; fase 3).

Si esegue dentro Fusion, un passo per chiamata (gli script del connettore non sono transazionali):
    import runpy
    def run(_context: str):
        runpy.run_path('/Users/paul/hexapod-v2/cad/script/rif_componenti.py')['main'](['parametri'])

Passi:
  documento   crea il design, lo rende parametrico e lo salva in "Hexabot v2" (solo se non e' gia' aperto)
  parametri   aggiunge o aggiorna i parametri utente di PARAMETRI
  step        importa i modelli STEP (servo, regolatori Pololu) e rinomina i componenti
  orienta     riporta il servo nella terna di progetto con una lavorazione Sposta (vedi TERNA_SERVO)
  posiziona   mette i componenti STEP nella zona "libreria" e cattura la posizione
  ingombri    crea gli ingombri semplificati in una BaseFeature (rigenera=True li cancella e ricrea)
  stato       rilegge componenti, corpi, ingombri nella terna propria e li confronta con ATTESI

Le quote vengono da docs/dimensioni-componenti.md (fonte e stato di ogni quota sono li').
Tutti i componenti "Rif_*" stanno nella zona libreria (y >= 250 mm): le istanze nell'assieme si creano dalle
loro copie. Unita' nello script: mm, convertiti in cm per l'API.
"""
import json
import os
import runpy
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
MODELLI = os.path.join(os.path.dirname(QUI), 'modelli')
V = runpy.run_path(os.path.join(QUI, 'versione.py'))
NOME_DESIGN, PROGETTO = V['NOME_DESIGN'], V['PROGETTO']

P3 = adsk.core.Point3D.create
V3 = adsk.core.Vector3D.create

# (nome, espressione, unita', commento). Stato delle quote: V verificato, S stimato, C da confermare.
PARAMETRI = [
    # --- servo MG996R. Terna del servo: origine sull'asse dell'albero al lato inferiore delle alette,
    #     +Z verso la cima dell'albero, cassa verso +X (l'albero sta vicino all'estremita' -X), Y = larghezza.
    ('srv_cassa_l', '41.0 mm', 'mm', 'Servo: lunghezza della cassa, la maggiore delle fonti (STEP 41,0; AZDelivery 40,3; Tower Pro 40,9) V'),
    ('srv_cassa_w', '20.5 mm', 'mm', 'Servo: larghezza della cassa (STEP 20,5; AZDelivery e Tower Pro 20) V'),
    ('srv_sotto', '28.8 mm', 'mm', 'Servo: cassa sotto il lato inferiore delle alette, la maggiore (STEP 28,8; AZDelivery 26,6) V'),
    ('srv_sopra', '10.2 mm', 'mm', 'Servo: sommita della cassa sopra le alette, la maggiore (Tower Pro 10,2; AZDelivery 10,0; STEP 8,2) V'),
    ('srv_albero_h', '16.4 mm', 'mm', 'Servo: cima dell albero sopra le alette (STEP 16,4; AZDelivery 16,3; Tower Pro 15,9) V'),
    ('srv_asse_x', '10.25 mm', 'mm', 'Servo: asse dell albero dall estremita vicina della cassa (STEP) S'),
    ('srv_alette_sp', '2.4 mm', 'mm', 'Servo: spessore delle alette (STEP) S'),
    ('srv_alette_l', '54.6 mm', 'mm', 'Servo: lunghezza sulle alette (STEP 54,6; AZDelivery 53,6; Tower Pro 54) V'),
    ('srv_alette_w', '18.5 mm', 'mm', 'Servo: larghezza delle alette (STEP) S'),
    ('srv_fori_x', '48.0 mm', 'mm', 'Servo: interasse dei fori delle alette lungo la cassa (STEP) S'),
    ('srv_fori_y', '10.0 mm', 'mm', 'Servo: interasse dei fori delle alette di traverso (STEP) S'),
    ('srv_fori_d', '4.2 mm', 'mm', 'Servo: diametro dei fori delle alette (STEP) S'),
    ('srv_torre_d', '20.5 mm', 'mm', 'Servo: diametro della torretta del riduttore (STEP) S'),
    ('srv_torre_h', '10.5 mm', 'mm', 'Servo: altezza della torretta sopra le alette (STEP) S'),
    ('srv_spline_d', '6.0 mm', 'mm', 'Servo: diametro del millerighe, 25 denti attesi (STEP) S'),
    ('srv_spline_l', '4.0 mm', 'mm', 'Servo: lunghezza del millerighe (STEP) S'),
    ('srv_cavo_z', '23.5 mm', 'mm', 'Servo: centro dell uscita del cavo sotto le alette, lato albero (STEP) S'),
    ('srv_cavo_w', '7.0 mm', 'mm', 'Servo: larghezza del fermacavo (STEP) S'),
    ('srv_cavo_h', '4.2 mm', 'mm', 'Servo: altezza del fermacavo (STEP) S'),
    # --- squadretta metallica a disco 25 denti (prodotto non ancora scelto). Origine sull'asse alla faccia
    #     superiore del disco, mozzo verso -Z (verso il servo).
    ('sq_d', '20 mm', 'mm', 'Squadretta metallica: diametro del disco (rivenditori) C'),
    ('sq_sp', '2.5 mm', 'mm', 'Squadretta metallica: spessore del disco (rivenditori, discordanti) C'),
    ('sq_h', '5.5 mm', 'mm', 'Squadretta metallica: altezza totale con il mozzo (rivenditori, discordanti) C'),
    ('sq_mozzo_d', '9 mm', 'mm', 'Squadretta metallica: diametro del mozzo (rivenditori) C'),
    ('sq_fori_pcd', '14 mm', 'mm', 'Squadretta metallica: interasse dei fori M3 opposti (rivenditori) C'),
    ('sq_fori_d', '3 mm', 'mm', 'Squadretta metallica: fori filettati M3 C'),
    # --- giunto lato opposto: cuscinetto NMB LF-1050ZZ e perno
    ('cus_d', '5 mm', 'mm', 'Cuscinetto LF-1050ZZ: foro V'),
    ('cus_D', '10 mm', 'mm', 'Cuscinetto LF-1050ZZ: diametro esterno V'),
    ('cus_B', '4 mm', 'mm', 'Cuscinetto LF-1050ZZ: larghezza V'),
    ('cus_flangia_d', '11.6 mm', 'mm', 'Cuscinetto LF-1050ZZ: diametro della flangia (generici da 11,2 a 11,7) V'),
    ('cus_flangia_sp', '0.8 mm', 'mm', 'Cuscinetto LF-1050ZZ: spessore della flangia V'),
    ('perno_d', '5 mm', 'mm', 'Perno: diametro'),
    ('perno_l', '12 mm', 'mm', 'Perno: lunghezza (D-047: 5,2 nella piastra, 0,4 rialzo, 4 cuscinetto, 1 nel fondo, 1,4 sporgente)'),
    # --- batteria OVONIC 2S 5200 mAh hardcase. Origine al centro del fondo, cavi verso +X.
    ('bat_l', '139 mm', 'mm', 'Batteria: lunghezza, la maggiore delle schede (137-139) V'),
    ('bat_w', '47.3 mm', 'mm', 'Batteria: larghezza, la maggiore delle schede (46-47,3) V'),
    ('bat_h', '25.4 mm', 'mm', 'Batteria: altezza, la maggiore delle schede (24-25,4) V'),
    ('bat_tol_l', '5 mm', 'mm', 'Batteria: tolleranza dichiarata sulla lunghezza V'),
    ('bat_tol_w', '2 mm', 'mm', 'Batteria: tolleranza dichiarata sulla larghezza V'),
    ('bat_tol_h', '2 mm', 'mm', 'Batteria: tolleranza dichiarata sull altezza V'),
    ('bat_cavi_l', '25 mm', 'mm', 'Batteria: spazio per la curva dei cavi 12 AWG e del bilanciamento S'),
    # --- SSC32-V2.5. Origine al centro, lato inferiore del PCB a z = 0, lato lungo lungo X, morsettiera a +X.
    ('ssc_l', '72 mm', 'mm', 'SSC-32: lunghezza del PCB (disegno del venditore) S'),
    ('ssc_w', '55 mm', 'mm', 'SSC-32: larghezza del PCB (disegno del venditore) S'),
    ('ssc_sp', '1.6 mm', 'mm', 'SSC-32: spessore del PCB C'),
    ('ssc_fori_x', '65.5 mm', 'mm', 'SSC-32: interasse dei fori lungo X (disegno del venditore) S'),
    ('ssc_fori_y', '48.5 mm', 'mm', 'SSC-32: interasse dei fori lungo Y (disegno del venditore) S'),
    ('ssc_fori_d', '3.0 mm', 'mm', 'SSC-32: diametro dei fori C'),
    ('ssc_alt_libera', '25 mm', 'mm', 'SSC-32: spazio sopra il PCB lungo i lati lunghi per spine e curva dei cavi S'),
    ('ssc_retro_h', '6 mm', 'mm', 'SSC-32: spazio sotto il PCB per le barre di potenza e i cavi 16 AWG saldati S'),
    ('ssc_dist', '8 mm', 'mm', 'SSC-32: altezza dei distanziali (BOM B18)'),
    # --- ESP32-S3-CAM UICPAL. Origine al centro del PCB, lato inferiore a z = 0, antenna a +X, USB a -X.
    ('esp_l', '62.6 mm', 'mm', 'ESP32: lunghezza del PCB (inserzione) S'),
    ('esp_w', '28.3 mm', 'mm', 'ESP32: larghezza del PCB (inserzione) S'),
    ('esp_sp', '1.6 mm', 'mm', 'ESP32: spessore del PCB C'),
    ('esp_antenna', '4.8 mm', 'mm', 'ESP32: sporgenza del modulo con l antenna oltre il PCB (4,7-4,9) S'),
    ('esp_file', '24.7 mm', 'mm', 'ESP32: interasse delle due file di pin C'),
    # --- camera OV3660-75MM. Origine sull'asse ottico al retro della testa, asse ottico +Z, flat verso -X.
    ('cam_testa', '8.5 mm', 'mm', 'Camera: lato della testa (disegno del venditore) S'),
    ('cam_alt', '6 mm', 'mm', 'Camera: altezza della testa compatta con lente 120 GOOD C'),
    ('cam_lente_d', '7 mm', 'mm', 'Camera: diametro del barilotto della lente C'),
    ('cam_flat_l', '75 mm', 'mm', 'Camera: lunghezza totale testa + flat + linguetta (disegno) S'),
    ('cam_flat_w', '6 mm', 'mm', 'Camera: larghezza del flat S'),
    ('cam_ling_l', '12.5 mm', 'mm', 'Camera: lunghezza della linguetta di contatto S'),
    ('cam_ling_w', '5 mm', 'mm', 'Camera: larghezza della linguetta di contatto S'),
    # --- minuteria elettrica (ingombri)
    ('bas_l', '56 mm', 'mm', 'Basetta millefori 50 x 70 tagliata: lunghezza (sotto l ESP32, D-053)'),
    ('bas_w', '35 mm', 'mm', 'Basetta tagliata: larghezza (colonnine del coperchio a 18,8 dall asse)'),
    ('bas_sp', '1.6 mm', 'mm', 'Basetta: spessore S'),
    ('int_l', '25.4 mm', 'mm', 'Interruttore Pololu 2813: lunghezza V'),
    ('int_w', '20.3 mm', 'mm', 'Interruttore Pololu 2813: larghezza V'),
    ('int_h', '4.1 mm', 'mm', 'Interruttore Pololu 2813: altezza con il pulsante V'),
    ('cond_d', '12.5 mm', 'mm', 'Condensatore 2200 uF 16 V: diametro (Panasonic EEUFR1C222) S'),
    ('cond_h', '20 mm', 'mm', 'Condensatore 2200 uF 16 V: altezza S'),
    ('fus_l', '40 mm', 'mm', 'Portafusibile ATO in linea con coperchio: lunghezza S'),
    ('fus_w', '22 mm', 'mm', 'Portafusibile ATO in linea: larghezza S'),
    ('fus_h', '15 mm', 'mm', 'Portafusibile ATO in linea: altezza S'),
    ('wago_l', '29.9 mm', 'mm', 'Wago 221-415: larghezza sulle 5 leve S'),
    ('wago_w', '18.6 mm', 'mm', 'Wago 221-415: profondita (ingresso dei fili) S'),
    ('wago_h', '8.3 mm', 'mm', 'Wago 221-415: altezza S'),
    # --- regole di stampa e inserti (docs/dimensioni-componenti.md, regole per il CAD)
    ('gio_stampa', '0.2 mm', 'mm', 'Gioco di stampa per lato sulle sedi, da tarare con un provino'),
    ('gio_servo', '0.2 mm', 'mm', 'Gioco per lato sulle sedi dei servo, da tarare con il provino della culla'),
    ('ins_m3_d', '4.2 mm', 'mm', 'Foro per inserto M3 CNC Kitchen (4,0 consigliato + 0,2)'),
    ('ins_m3_l', '6.7 mm', 'mm', 'Profondita del foro per inserto M3 (5,7 + 1)'),
    ('ins_m2_d', '3.4 mm', 'mm', 'Foro per inserto M2 CNC Kitchen (3,2 consigliato + 0,2)'),
    ('ins_m2_l', '4 mm', 'mm', 'Profondita del foro per inserto M2 (3 + 1)'),
    ('vite_m3_pass', '3.4 mm', 'mm', 'Foro passante per vite M3'),
    ('vite_m2_pass', '2.4 mm', 'mm', 'Foro passante per vite M2'),
    # --- predisposizioni della versione 2.1.0 (D-066): sensori, luci, audio e computer di bordo. Quote dalle pagine dei
    #     produttori lette nella ricerca del 9 ottobre (docs/predisposizioni.md); fori e posizione dei chip C, da
    #     ricontrollare sulle schede vere prima di stampare
    ('sen_imu_l', '23 mm', 'mm', 'IMU Pololu (X4): lunghezza S'),
    ('sen_imu_w', '13 mm', 'mm', 'IMU: larghezza S'),
    ('sen_imu_sp', '3 mm', 'mm', 'IMU: spessore con i componenti S'),
    ('sen_imu_fori', '18 mm', 'mm', 'IMU: interasse dei due fori sul lato lungo C'),
    ('sen_ads_l', '30.5 mm', 'mm', 'ADC ADS7830 (X6): lunghezza S'),
    ('sen_ads_w', '17.7 mm', 'mm', 'ADC ADS7830: larghezza S'),
    ('sen_ads_sp', '4.7 mm', 'mm', 'ADC ADS7830: spessore con i connettori STEMMA QT S'),
    ('sen_ads_fori', '25.4 mm', 'mm', 'ADC ADS7830: interasse dei due fori sul lato lungo C'),
    ('sen_tof_l', '18 mm', 'mm', 'ToF Pololu #3418 e #3415 (X8, X19): lunghezza della scheda S'),
    ('sen_tof_w', '13 mm', 'mm', 'ToF: larghezza della scheda S'),
    ('sen_tof_pcb', '1.6 mm', 'mm', 'ToF: spessore del circuito S'),
    ('sen_tof_chip_l', '6.4 mm', 'mm', 'ToF: lato lungo del sensore (VL53L7CX 6,4 x 3,0 x 1,75), al centro della scheda C'),
    ('sen_tof_chip_w', '3 mm', 'mm', 'ToF: lato corto del sensore C'),
    ('sen_tof_chip_h', '1.4 mm', 'mm', 'ToF: altezza del sensore sopra il circuito C'),
    ('sen_ina_l', '22.9 mm', 'mm', 'INA260 Adafruit (X7): lato S'),
    ('sen_ina_w', '22.8 mm', 'mm', 'INA260: altro lato S'),
    ('sen_ina_sp', '2.7 mm', 'mm', 'INA260: spessore senza morsettiera S'),
    ('sen_ina_mors_h', '8.5 mm', 'mm', 'INA260: morsettiera, altezza sopra il circuito C'),
    ('sen_ina_fori', '17.8 mm', 'mm', 'INA260: interasse dei due fori su un lato C'),
    ('aud_amp_l', '19.4 mm', 'mm', 'Amplificatore MAX98357A Adafruit 3006 (X17): lunghezza S'),
    ('aud_amp_w', '17.8 mm', 'mm', 'Amplificatore: larghezza S'),
    ('aud_amp_sp', '3 mm', 'mm', 'Amplificatore: spessore S'),
    ('aud_alt_l', '15 mm', 'mm', 'Altoparlante CMS-15113-078SP (X17): lunghezza S'),
    ('aud_alt_w', '11 mm', 'mm', 'Altoparlante: larghezza S'),
    ('aud_alt_sp', '3 mm', 'mm', 'Altoparlante: spessore S'),
    ('aud_mic_l', '16.7 mm', 'mm', 'Microfono I2S Adafruit 3421 (X16): lunghezza V'),
    ('aud_mic_w', '12.7 mm', 'mm', 'Microfono: larghezza V'),
    ('aud_mic_sp', '1.8 mm', 'mm', 'Microfono: spessore V'),
    ('zai_l', '65 mm', 'mm', 'Computer di bordo a zaino (Radxa ZERO 3W): lunghezza V'),
    ('zai_w', '30 mm', 'mm', 'Computer di bordo: larghezza V'),
    ('zai_sp', '5 mm', 'mm', 'Computer di bordo: spessore con i componenti S'),
    ('zai_fori_l', '58 mm', 'mm', 'Computer di bordo: interasse dei fori sul lato lungo (formato Raspberry Pi Zero) V'),
    ('zai_fori_w', '23 mm', 'mm', 'Computer di bordo: interasse dei fori sul lato corto V'),
    ('sch_l', '30 mm', 'mm', 'Scheda del carapace (X2): lunghezza S'),
    ('sch_w', '20 mm', 'mm', 'Scheda del carapace: larghezza S'),
    ('sch_sp', '9 mm', 'mm', 'Scheda del carapace: spessore con la spina IDC S'),
    ('pre_l', '15.5 mm', 'mm', 'Prese dei piedi: sei spine JR a 3 poli piegate, passo 2,54 S'),
    ('pre_w', '2.6 mm', 'mm', 'Prese dei piedi: spessore della fila S'),
    ('pre_h', '8.5 mm', 'mm', 'Prese dei piedi: altezza del circuito con le spine S'),
]

# Modelli STEP: nome del componente -> percorso relativo a cad/modelli
STEP = {
    'Rif_Servo_MG996R': 'mg996r/Servo Motor MG996R 3D Model.step',
    'Rif_Reg_Servo_D42V110F6': 'pololu-d42v110fx/d42v110fx.step',
    'Rif_Reg_5V_D24V22F5': 'pololu-d24v22fx/d24v22fx.step',
}

# Terna del modello STEP del servo: X = lunghezza, Y = altezza dal fondo, Z = larghezza, origine al centro
# della cassa in pianta, sul fondo. Albero a x = -10,25, lato inferiore delle alette a y = 28,8.
# Terna di progetto (parametri srv_): (x, y, z)_step -> (x + 10,25, -z, y - 28,8).
TERNA_SERVO = {'origine': (10.25, 0.0, -28.8), 'ex': (1, 0, 0), 'ey': (0, 0, 1), 'ez': (0, -1, 0)}

# Posizioni nella zona libreria (mm, alla radice)
LIBRERIA = {
    'Rif_Servo_MG996R': (0, 250, 0),
    'Rif_Squadretta_25T': (60, 250, 0),
    'Rif_Cuscinetto_LF1050ZZ': (90, 250, 0),
    'Rif_Perno_5': (110, 250, 0),
    'Rif_Reg_Servo_D42V110F6': (140, 250, 0),
    'Rif_Reg_5V_D24V22F5': (200, 250, 0),
    'Rif_SSC32_V25': (0, 350, 0),
    'Rif_ESP32_S3_CAM': (100, 350, 0),
    'Rif_Camera_OV3660_75': (200, 350, 0),
    'Rif_Batteria_2S5200': (0, 450, 0),
    'Rif_Interruttore_Pololu_2813': (120, 450, 0),
    'Rif_Condensatore_2200uF': (160, 450, 0),
    'Rif_Basetta_50x70': (230, 450, 0),
    'Rif_Portafusibile_ATO': (0, 550, 0),
    'Rif_Wago_221_415': (60, 550, 0),
    'Rif_Cicalino_BX100': (110, 550, 0),
    'Rif_Tplug': (170, 550, 0),
    'Rif_Pulsante_12': (230, 550, 0),
    'Rif_IMU': (0, 650, 0),
    'Rif_ADC_ADS7830': (50, 650, 0),
    'Rif_INA260': (100, 650, 0),
    'Rif_ToF_8x8': (150, 650, 0),
    'Rif_ToF_1': (190, 650, 0),
    'Rif_Ampli_MAX98357A': (230, 650, 0),
    'Rif_Altoparlante': (0, 710, 0),
    'Rif_Microfono_I2S': (40, 710, 0),
    'Rif_FSR_400': (80, 710, 0),
    'Rif_Scheda_Carapace': (120, 710, 0),
    'Rif_Prese_Piedi': (170, 710, 0),
    'Rif_Computer_Zaino': (0, 780, 0),
}

GENERATI = [n for n in LIBRERIA if n not in STEP]

# Ingombri attesi nella terna propria del componente (mm): [xmin, ymin, zmin, xmax, ymax, zmax]
ATTESI = {
    'Rif_Servo_MG996R': [-18.25, -10.25, -28.8, 37.55, 10.25, 16.4],
    'Rif_Reg_Servo_D42V110F6': [0.0, 0.0, None, 43.18, 31.75, None],
    'Rif_Reg_5V_D24V22F5': [0.0, 0.0, None, 17.78, 17.78, None],
    'Rif_Batteria_2S5200': [-69.5, -23.65, 0.0, 94.5, 23.65, 25.4],
    'Rif_Squadretta_25T': [-10.0, -10.0, -5.5, 10.0, 10.0, 0.0],
    'Rif_Cuscinetto_LF1050ZZ': [-5.8, -5.8, 0.0, 5.8, 5.8, 4.0],
    'Rif_Perno_5': [-2.5, -2.5, 0.0, 2.5, 2.5, 12.0],
}


def _tmp():
    return adsk.fusion.TemporaryBRepManager.get()


def box(cx, cy, z0, lx, ly, lz):
    """Parallelepipedo: centro (cx, cy) in pianta, base a z0, dimensioni lx, ly, lz (mm)."""
    obb = adsk.core.OrientedBoundingBox3D.create(
        P3(cx / 10, cy / 10, (z0 + lz / 2) / 10), V3(1, 0, 0), V3(0, 1, 0), lx / 10, ly / 10, lz / 10)
    return _tmp().createBox(obb)


def cyl(cx, cy, z0, d, h):
    """Cilindro di asse Z, diametro d e altezza h, con base in (cx, cy, z0)."""
    return _tmp().createCylinderOrCone(P3(cx / 10, cy / 10, z0 / 10), d / 20, P3(cx / 10, cy / 10, (z0 + h) / 10), d / 20)


def unisci(a, *altri):
    for b in altri:
        _tmp().booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)
    return a


def sottrai(a, *altri):
    for b in altri:
        _tmp().booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return a


def traslazione(pos_mm):
    t = adsk.core.Matrix3D.create()
    t.translation = V3(pos_mm[0] / 10, pos_mm[1] / 10, pos_mm[2] / 10)
    return t


SOLO = []


def componente(root, nome, corpi):
    """Componente con i corpi dati [(nome, brep)] in una sola BaseFeature, nella posizione di libreria.

    Se SOLO non e' vuota crea soltanto i componenti elencati (i corpi temporanei degli altri si scartano).
    """
    if SOLO and nome not in SOLO:
        return None
    occ = root.occurrences.addNewComponent(traslazione(LIBRERIA[nome]))
    comp = occ.component
    comp.name = nome
    bf = comp.features.baseFeatures.add()
    bf.name = 'Ingombro'
    bf.startEdit()
    for nome_corpo, brep in corpi:
        b = comp.bRepBodies.add(brep, bf)
        b.name = nome_corpo
    bf.finishEdit()
    return occ


def occorrenze_per_nome(root):
    return {o.component.name: o for o in root.occurrences}


# ------------------------------------------------------------------------------------------- passi
def fai_documento(app):
    for d in app.documents:
        if d.name.startswith(NOME_DESIGN):
            d.activate()
            return 'gia aperto: %s' % d.name
    prog = [p for p in app.data.dataProjects if p.name == PROGETTO][0]
    if any(f.name == NOME_DESIGN for f in prog.rootFolder.dataFiles):
        return 'ERRORE: %s esiste gia nel progetto ma non e aperto: aprirlo invece di crearne un altro' % NOME_DESIGN
    doc = app.activeDocument
    des = adsk.fusion.Design.cast(app.activeProduct)
    vuoto = (des is not None and not doc.isSaved and des.timeline.count == 0
             and des.rootComponent.occurrences.count == 0 and des.rootComponent.bRepBodies.count == 0)
    if not vuoto:                       # si riusa un documento nuovo e vuoto, altrimenti se ne crea uno
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        des = adsk.fusion.Design.cast(app.activeProduct)
    des.designType = adsk.fusion.DesignTypes.ParametricDesignType
    doc.saveAs(NOME_DESIGN, prog.rootFolder, 'Fase 3: design vuoto', '')
    return 'creato e salvato: %s' % NOME_DESIGN


def fai_step(app, des, root):
    fatti = {}
    presenti = occorrenze_per_nome(root)
    for nome, rel in STEP.items():
        if nome in presenti:
            fatti[nome] = 'gia presente'
            continue
        prima = set(o.entityToken for o in root.occurrences)
        opz = app.importManager.createSTEPImportOptions(os.path.join(MODELLI, rel))
        if not app.importManager.importToTarget(opz, root):
            raise RuntimeError('import fallito: %s' % rel)
        nuove = [o for o in root.occurrences if o.entityToken not in prima]
        if len(nuove) != 1:
            raise RuntimeError('import di %s: attesa 1 occorrenza nuova, trovate %d' % (rel, len(nuove)))
        occ = nuove[0]
        nome_step = occ.component.name
        occ.component.name = nome
        tl = des.timeline
        if tl.timelineGroups.count:                     # l'import crea un gruppo nella timeline: gli si da' un nome
            tl.timelineGroups.item(tl.timelineGroups.count - 1).name = 'Import_' + nome
        fatti[nome] = {'da': nome_step, 'corpi': occ.component.bRepBodies.count,
                       'sotto_occorrenze': occ.component.occurrences.count}
    return fatti


def fai_orienta(des, root):
    occ = occorrenze_per_nome(root).get('Rif_Servo_MG996R')
    if occ is None:
        return 'servo assente: eseguire prima il passo step'
    comp = occ.component
    for mv in list(comp.features.moveFeatures):           # si rifa' da capo: un'eventuale versione sbagliata si cancella
        if mv.name == 'Terna_di_progetto':
            mv.deleteMe()
    corpi = adsk.core.ObjectCollection.create()
    for b in comp.bRepBodies:
        corpi.add(b)
    t = TERNA_SERVO
    m = adsk.core.Matrix3D.create()
    o = t['origine']
    m.setWithCoordinateSystem(P3(o[0] / 10, o[1] / 10, o[2] / 10), V3(*t['ex']), V3(*t['ey']), V3(*t['ez']))
    # La matrice di uno Sposta si applica nella terna della radice, non in quella del componente: con
    # l'occorrenza in T, per ottenere M nella terna propria si passa T * M * T^-1 (provato l'8 ottobre).
    T = occ.transform2
    x = T.copy()
    x.invert()
    x.transformBy(m)
    x.transformBy(T)
    inp = comp.features.moveFeatures.createInput2(corpi)
    inp.defineAsFreeMove(x)
    mv = comp.features.moveFeatures.add(inp)
    mv.name = 'Terna_di_progetto'
    return {'corpi_spostati': corpi.count, 'nomi': nomina_corpi_servo(comp)}


def nomina_corpi_servo(comp):
    """Il modello ha la cassa (circa 33 cm3) e i tre fili del cavo (5 mm3 l'uno)."""
    fili = 0
    for b in sorted(comp.bRepBodies, key=lambda c: -c.volume):
        if b.volume * 1000 > 1000:
            b.name = 'cassa'
        else:
            fili += 1
            b.name = 'filo_%d' % fili
    return [b.name for b in comp.bRepBodies]


def fai_posiziona(des, root):
    fatti = {}
    presenti = occorrenze_per_nome(root)
    for nome in STEP:
        occ = presenti.get(nome)
        if occ is None:
            fatti[nome] = 'assente'
            continue
        occ.transform2 = traslazione(LIBRERIA[nome])
        fatti[nome] = 'posizionato'
    if des.snapshots.hasPendingSnapshot:
        des.snapshots.add()
        fatti['snapshot'] = 'catturato'
    return fatti


def fai_ingombri(des, root, rigenera, solo=None):
    """Crea gli ingombri; con solo = [nomi] cancella e ricrea soltanto quelli."""
    def p(nome):
        return des.userParameters.itemByName(nome).value * 10.0

    presenti = occorrenze_per_nome(root)
    nomi = list(solo) if solo else GENERATI
    if solo:
        rigenera = True
    if rigenera:
        for n in nomi:
            if n in presenti:
                presenti[n].deleteMe()
    else:
        gia = [n for n in nomi if n in presenti]
        if gia:
            return 'componenti gia presenti: %s (usare rigenera=True)' % gia

    fatti = []

    # SSC32-V2.5: posizioni interne dal disegno quotato del venditore (docs/dimensioni-componenti.md)
    L, W, sp = p('ssc_l'), p('ssc_w'), p('ssc_sp')
    fx, fy, fd = p('ssc_fori_x') / 2, p('ssc_fori_y') / 2, p('ssc_fori_d')
    pcb = box(0, 0, 0, L, W, sp)
    sottrai(pcb, *[cyl(sx * fx, sy * fy, -1, fd, sp + 2) for sx in (-1, 1) for sy in (-1, 1)])
    hdr = unisci(*[box(cx, sy * (W / 2 - 4.0), sp, 10.2, 7.7, 8.5) for sy in (1, -1) for cx in (-20.3, -7.2, 6.0, 19.2)])
    mors = box(L / 2 - 6.6, 0.0, sp, 7.0, 21.5, 8.5)
    ser = box(14.3, 3.2, sp, 7.7, 18.0, 8.5)
    usb = box(-L / 2 + 2.0, -12.5, sp, 5.6, 7.5, 2.7)
    xb = unisci(box(-25.7, 15.1, sp, 20.0, 2.0, 4.5), box(-25.7, -5.8, sp, 20.0, 2.0, 4.5))
    cap = unisci(cyl(22.3, 10.7, sp, 6.3, 7.7), cyl(22.3, 2.6, sp, 6.3, 7.7))
    alt, rh = p('ssc_alt_libera'), p('ssc_retro_h')
    zona = unisci(box(0, W / 2 - 4.0, sp, 56.0, 8.0, alt), box(0, -(W / 2 - 4.0), sp, 56.0, 8.0, alt))
    retro = unisci(box(0, W / 2 - 4.0, -rh, 56.0, 8.0, rh), box(0, -(W / 2 - 4.0), -rh, 56.0, 8.0, rh))
    fatti.append(componente(root, 'Rif_SSC32_V25', [
        ('pcb', pcb), ('header_servo', hdr), ('morsettiera', mors), ('header_seriale', ser), ('micro_usb', usb),
        ('zoccolo_xbee', xb), ('condensatori', cap), ('zona_spine_servo', zona), ('zona_barre_retro', retro)]))

    # ESP32-S3-CAM
    L, W, sp = p('esp_l'), p('esp_w'), p('esp_sp')
    ant = p('esp_antenna')
    fr = p('esp_file') / 2
    fatti.append(componente(root, 'Rif_ESP32_S3_CAM', [
        ('pcb', box(0, 0, 0, L, W, sp)),
        ('modulo_antenna', box(L / 2 + ant - 25.5 / 2, 0, sp, 25.5, 18.0, 3.2)),
        ('usb_c', unisci(box(-L / 2 + 2.7, 6.6, sp, 7.35, 8.94, 3.26), box(-L / 2 + 2.7, -6.6, sp, 7.35, 8.94, 3.26))),
        ('connettore_fpc', box(-2.0, 0, sp, 4.5, 14.5, 2.0)),
        ('pin_header', unisci(box(2.9, fr, -8.5, 50.8, 2.54, 8.5), box(2.9, -fr, -8.5, 50.8, 2.54, 8.5))),
        ('slot_tf', box(-15.0, 0, -1.9, 15.0, 14.0, 1.9))]))

    # Camera OV3660-75MM
    t, h, ld = p('cam_testa'), p('cam_alt'), p('cam_lente_d')
    lung_flat = p('cam_flat_l') - t - p('cam_ling_l')
    fatti.append(componente(root, 'Rif_Camera_OV3660_75', [
        ('testa', unisci(box(0, 0, 0, t, t, h * 0.55), cyl(0, 0, h * 0.55, ld, h * 0.45))),
        ('flat', box(-t / 2 - lung_flat / 2, 0, 0, lung_flat, p('cam_flat_w'), 0.15)),
        ('linguetta', box(-t / 2 - lung_flat - p('cam_ling_l') / 2, 0, 0, p('cam_ling_l'), p('cam_ling_w'), 0.3))]))

    # Batteria OVONIC 2S 5200 hardcase (quote massime delle schede, senza tolleranza)
    bl, bw, bh, cl = p('bat_l'), p('bat_w'), p('bat_h'), p('bat_cavi_l')
    fatti.append(componente(root, 'Rif_Batteria_2S5200', [
        ('pacco', box(0, 0, 0, bl, bw, bh)),
        ('uscita_cavi', box(bl / 2 + cl / 2, 0, bh / 2 - 6, cl, 24, 12))]))

    # Squadretta metallica a disco: disco sotto la faccia superiore, mozzo verso -Z
    sq = unisci(cyl(0, 0, -p('sq_sp'), p('sq_d'), p('sq_sp')), cyl(0, 0, -p('sq_h'), p('sq_mozzo_d'), p('sq_h')))
    r = p('sq_fori_pcd') / 2
    sottrai(sq, cyl(0, 0, -p('sq_h') - 1, 3.2, p('sq_h') + 2),
            *[cyl(x, y, -p('sq_sp') - 1, p('sq_fori_d'), p('sq_sp') + 2) for x, y in ((r, 0), (-r, 0), (0, r), (0, -r))])
    fatti.append(componente(root, 'Rif_Squadretta_25T', [('squadretta', sq)]))

    # Cuscinetto: origine al centro della faccia lato flangia, corpo verso +Z
    cus = unisci(cyl(0, 0, 0, p('cus_D'), p('cus_B')), cyl(0, 0, 0, p('cus_flangia_d'), p('cus_flangia_sp')))
    sottrai(cus, cyl(0, 0, -1, p('cus_d'), p('cus_B') + 2))
    fatti.append(componente(root, 'Rif_Cuscinetto_LF1050ZZ', [('cuscinetto', cus)]))
    fatti.append(componente(root, 'Rif_Perno_5', [('perno', cyl(0, 0, 0, p('perno_d'), p('perno_l')))]))

    # Minuteria
    # 2813: circuito intero e componenti rientrati di 1,5 mm dai bordi, che entrano nelle guide del corpo (S)
    fatti.append(componente(root, 'Rif_Interruttore_Pololu_2813', [('circuito', box(0, 0, 0, p('int_l'), p('int_w'), 1.6)),
                                                            ('componenti', box(0, 0, 1.6, p('int_l') - 3.0, p('int_w') - 3.0, p('int_h') - 1.6))]))
    fatti.append(componente(root, 'Rif_Condensatore_2200uF', [('condensatore', cyl(0, 0, 0, p('cond_d'), p('cond_h')))]))
    # basetta 50 x 70 tagliata a misura (D-053): i fori si trapanano sulle colonnine del vassoio
    fatti.append(componente(root, 'Rif_Basetta_50x70', [('basetta', box(0, 0, 0, p('bas_l'), p('bas_w'), p('bas_sp')))]))
    fatti.append(componente(root, 'Rif_Portafusibile_ATO', [('portafusibile', box(0, 0, 0, p('fus_l'), p('fus_w'), p('fus_h')))]))
    fatti.append(componente(root, 'Rif_Wago_221_415', [('morsetto', box(0, 0, 0, p('wago_l'), p('wago_w'), p('wago_h')))]))
    fatti.append(componente(root, 'Rif_Cicalino_BX100', [('cicalino', box(0, 0, 0, 40.0, 25.0, 11.0))]))
    fatti.append(componente(root, 'Rif_Tplug', [('coppia_tplug', box(0, 0, 0, 30.0, 16.0, 8.5))]))
    # pulsante da pannello Ø12 (B3b): origine al centro della faccia superiore del pannello, +Z in alto
    fatti.append(componente(root, 'Rif_Pulsante_12', [('pulsante', unisci(cyl(0, 0, 0, 15.0, 2.0), cyl(0, 0, -21.6, 12.0, 21.6),
                                                                       cyl(0, 0, -3.6, 17.3, 2.0)))]))
    # Predisposizioni 2.1.0 (D-066): circuiti con l'origine al centro del lato inferiore, +Z verso i componenti
    fatti.append(componente(root, 'Rif_IMU', [('scheda', box(0, 0, 0, p('sen_imu_l'), p('sen_imu_w'), p('sen_imu_sp')))]))
    fatti.append(componente(root, 'Rif_ADC_ADS7830', [('scheda', box(0, 0, 0, p('sen_ads_l'), p('sen_ads_w'), p('sen_ads_sp')))]))
    il, iw = p('sen_ina_l'), p('sen_ina_w')
    fatti.append(componente(root, 'Rif_INA260', [('scheda', box(0, 0, 0, il, iw, p('sen_ina_sp'))),
                                                 ('morsettiera', box(0, -iw / 2 + 4.0, p('sen_ina_sp'), 10.0, 8.0, p('sen_ina_mors_h')))]))
    tl, tw, tp = p('sen_tof_l'), p('sen_tof_w'), p('sen_tof_pcb')
    for nome in ('Rif_ToF_8x8', 'Rif_ToF_1'):
        fatti.append(componente(root, nome, [('scheda', box(0, 0, 0, tl, tw, tp)),
                                             ('sensore', box(0, 0, tp, p('sen_tof_chip_l'), p('sen_tof_chip_w'), p('sen_tof_chip_h')))]))
    fatti.append(componente(root, 'Rif_Ampli_MAX98357A', [('scheda', box(0, 0, 0, p('aud_amp_l'), p('aud_amp_w'), p('aud_amp_sp')))]))
    fatti.append(componente(root, 'Rif_Altoparlante', [('altoparlante', box(0, 0, 0, p('aud_alt_l'), p('aud_alt_w'), p('aud_alt_sp')))]))
    fatti.append(componente(root, 'Rif_Microfono_I2S', [('scheda', box(0, 0, 0, p('aud_mic_l'), p('aud_mic_w'), p('aud_mic_sp')))]))
    # FSR: solo la testa, sotto la punta della tibia (la coda si piega nella tasca sulla faccia +X)
    fatti.append(componente(root, 'Rif_FSR_400', [('testa', cyl(0, 0, 0, p('sen_fsr_testa_d'), p('sen_fsr_sp')))]))
    fatti.append(componente(root, 'Rif_Scheda_Carapace', [('scheda', box(0, 0, 0, p('sch_l'), p('sch_w'), p('sch_sp')))]))
    fatti.append(componente(root, 'Rif_Prese_Piedi', [('prese', box(0, 0, 0, p('pre_l'), p('pre_w'), p('pre_h')))]))
    fatti.append(componente(root, 'Rif_Computer_Zaino', [('scheda', box(0, 0, 0, p('zai_l'), p('zai_w'), p('zai_sp')))]))
    return [o.component.name for o in fatti if o is not None]


def stato(des, root):
    out = {}
    for o in root.occurrences:
        c = o.component
        bb = None
        for b in c.bRepBodies:
            bbb = b.boundingBox
            if bb is None:
                bb = bbb.copy()
            else:
                bb.combine(bbb)
        riga = {'corpi': c.bRepBodies.count,
                'posizione': [round(o.transform2.translation.x * 10, 2), round(o.transform2.translation.y * 10, 2),
                              round(o.transform2.translation.z * 10, 2)]}
        if bb is not None:
            ing = [bb.minPoint.x, bb.minPoint.y, bb.minPoint.z, bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z]
            riga['ingombro_proprio'] = [round(v * 10, 2) for v in ing]
            att = ATTESI.get(c.name)
            if att:
                scarti = [abs(a - round(v * 10, 2)) for a, v in zip(att, ing) if a is not None]
                riga['scarto_max'] = round(max(scarti), 2)
        out[c.name] = riga
    tl = des.timeline
    out['_timeline'] = {'voci': tl.count, 'problemi': [
        (tl.item(i).name, tl.item(i).errorOrWarningMessage) for i in range(tl.count)
        if not tl.item(i).isGroup
        and tl.item(i).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState],
        'gruppi': [g.name for g in tl.timelineGroups]}
    out['_parametri'] = des.userParameters.count
    out['_snapshot_pendente'] = des.snapshots.hasPendingSnapshot
    return out


def main(passi, rigenera=False, solo=None):
    out = {'passi': passi}
    try:
        app = adsk.core.Application.get()
        if 'documento' in passi:
            out['documento'] = fai_documento(app)
        des = adsk.fusion.Design.cast(app.activeProduct)
        V['controlla'](app)
        root = des.rootComponent
        L = runpy.run_path(os.path.join(QUI, 'lib_cad.py'))
        if 'parametri' in passi:
            out['parametri'] = L['aggiungi_parametri'](des, PARAMETRI)
        if 'step' in passi:
            out['step'] = fai_step(app, des, root)
        if 'orienta' in passi:
            out['orienta'] = fai_orienta(des, root)
        if 'posiziona' in passi:
            out['posiziona'] = fai_posiziona(des, root)
        if 'ingombri' in passi:
            SOLO[:] = list(solo or [])
            out['ingombri'] = fai_ingombri(des, root, rigenera, solo)
        if 'stato' in passi:
            out['stato'] = stato(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
