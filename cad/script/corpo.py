"""Corpo dell'esapode: base strutturale (scafo, gondole dei servo di coxa, tunnel della batteria).

Si esegue dentro Fusion sul design "Hexapod v2 - Assieme":
    ns = runpy.run_path('<repo>/cad/script/corpo.py'); ns['main'](['parametri', 'scafo', ...])

Terna del robot (= terna del sotto-assieme "Corpo" e della parte "Corpo_Base", all'origine):
X in avanti, Y a sinistra, Z in alto, z = 0 all'altezza degli assi dei femori.

Passi, da eseguire in ordine e in chiamate separate (gli script non sono transazionali):
  parametri   parametri utente del corpo
  scafo       cancella e ricrea Corpo_Base: prisma con la pianta dello scafo, smusso del fondo, svuotamento
  gondole     culle dei servo di coxa con il collo che entra nello scafo, rifilato lungo la parete interna
  lavorazioni sedi dei servo, finestre dei cavi, sedi dei cuscinetti, fori delle alette
  interno     tunnel della batteria, paratie, colonnine della SSC-32, bugne dei regolatori, torretta della
              camera, nervature delle gondole, linguette per il guscio, apertura posteriore
  guscio      cancella e ricrea Corpo_Guscio (cover superiore sfaccettata, con aperture e fori delle viti)
  vassoio     cancella e ricrea Vassoio_ESP32 (guide per la basetta dell'ESP32)
  sportelli   cancella e ricrea Sportello_Dorso e Sportello_Coda (cover a incastro)
  stato       sola lettura: corpi, volume, ingombro, schizzi non vincolati

Le gondole e i fianchi si modellano una volta (anteriore sinistra, media sinistra) e si specchiano.
"""
import json
import os
import runpy
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
L = runpy.run_path(os.path.join(QUI, 'lib_cad.py'))
Parte, NUOVO, UNISCI, TAGLIA = L['Parte'], L['NUOVO'], L['UNISCI'], L['TAGLIA']

NOME = 'Corpo_Base'
T0 = {}

PARAMETRI = [
    # --- pianta dello scafo
    ('cor_xn', '82 mm', 'mm', 'Corpo: semilunghezza (muso e coda)'),
    ('cor_yn', '25 mm', 'mm', 'Corpo: semilarghezza di muso e coda'),
    ('cor_xa', '68 mm', 'mm', 'Corpo: X dove il fianco obliquo incontra muso e coda'),
    ('cor_xb', '30 mm', 'mm', 'Corpo: semilunghezza del tratto centrale largo'),
    ('cor_yb', '46 mm', 'mm', 'Corpo: semilarghezza al centro'),
    ('cor_parete', '2 mm', 'mm', 'Corpo: spessore delle pareti'),
    ('cor_fondo', '2 mm', 'mm', 'Corpo: spessore del fondo'),
    ('cor_h_sotto', '17 mm', 'mm', 'Corpo: fondo esterno sotto l asse dei femori'),
    ('cor_orlo', '14 mm', 'mm', 'Base: quota dell orlo sopra l asse dei femori'),
    ('cor_smusso', '6 mm', 'mm', 'Base: smusso del fondo lungo i fianchi (resta sotto le gondole)'),
    ('cor_lato', 'sqrt((cor_xa - cor_xb) * (cor_xa - cor_xb) + (cor_yb - cor_yn) * (cor_yb - cor_yn))', 'mm',
     'Corpo: lunghezza del fianco obliquo'),
    ('cor_k', 'cor_parete * (cor_lato - (cor_xa - cor_xb)) / (cor_yb - cor_yn)', 'mm',
     'Corpo: arretramento in X dei vertici interni del fianco obliquo'),
    ('cor_spalla', '(cor_xa - cor_xb) * (cor_yb - cor_yn) / cor_lato + 0.5 mm', 'mm',
     'Corpo: profondita del riempimento sotto il fianco obliquo'),
    # --- gondole dei servo di coxa
    ('gon_rad_ang', '22 mm', 'mm', 'Gondole d angolo: asse della coxa -> estremita interna del collo (oltre la parete)'),
    ('gon_rad_med', 'cor_coxa_ym - cor_yb + cor_parete', 'mm', 'Gondole medie: asse della coxa -> faccia interna della parete'),
    ('gon_rifilo', '24 mm', 'mm', 'Gondole d angolo: tratto di parete interna lungo cui si rifila il collo'),
    ('ner_l', '8 mm', 'mm', 'Nervature alle radici delle gondole: sporgenza dentro lo scafo'),
    # --- dadi quadri M2 (DIN 562: 4 x 4 x 1,2) sotto le alette dei servo di coxa
    ('dado_m2_l', '4.2 mm', 'mm', 'Tasca del dado quadro M2: lato'),
    ('dado_m2_h', '1.6 mm', 'mm', 'Tasca del dado quadro M2: altezza'),
    ('dado_m2_z', '3 mm', 'mm', 'Tasca del dado quadro M2: plastica tra aletta e dado'),
    # --- feritoie di ventilazione tra i due regolatori (fondo del muso e dorso del guscio)
    ('fer_l', '3 mm', 'mm', 'Feritoie dei regolatori: larghezza'),
    ('fer_y0', '3 mm', 'mm', 'Feritoie del fondo: inizio (dalla mezzeria)'),
    ('fer_y1', '19 mm', 'mm', 'Feritoie: fine'),
    ('fer_dorso_y0', '8 mm', 'mm', 'Feritoie del dorso: inizio (ai lati del flat della camera)'),
    # --- tunnel della batteria
    ('cor_tun', '2 mm', 'mm', 'Tunnel della batteria: spessore di pareti e tetto'),
    ('vano_tetto_x', '10 mm', 'mm', 'Tunnel: il tetto parte a questa distanza dal fondo del vano (risalita dei cavi della batteria)'),
    ('cor_par_semi', 'cor_yn + (cor_xa - (vano_l - cor_xa + cor_tun)) * (cor_yb - cor_yn) / (cor_xa - cor_xb) - 1 mm', 'mm',
     'Paratia anteriore: semilarghezza (finisce dentro la parete obliqua)'),
    # --- SSC-32
    ('ssc_dx', '6 mm', 'mm', 'SSC-32: arretramento del centro rispetto all origine'),
    ('ssc_z', '8 mm', 'mm', 'SSC-32: quota del lato inferiore del PCB'),
    ('ssc_col_semi', '3.7 mm', 'mm', 'Colonnine della SSC-32: semilato'),
    # --- paratia anteriore e regolatori nel muso (in piedi, di traverso, piazzole in alto)
    ('par_asola_y0', 'vano_w / 2 + cor_tun + 2 mm', 'mm', 'Paratia anteriore: inizio dell asola passacavi'),
    ('par_asola_y1', 'cor_par_semi - 3 mm', 'mm', 'Paratia anteriore: fine dell asola passacavi'),
    ('reg_dist', '5 mm', 'mm', 'Regolatori: distanza del PCB dalla parete (lunghezza delle bugne)'),
    ('reg_bugna_d', '5.8 mm', 'mm', 'Regolatori: diametro delle bugne (inserto M2)'),
    ('reg_z_basso', 'cor_h_sotto - cor_fondo - 1 mm', 'mm', 'Regolatori: bordo inferiore sotto l asse dei femori'),
    ('reg_foro_bordo', '2.16 mm', 'mm', 'Regolatori: fori di fissaggio dal bordo lungo opposto alle piazzole (STEP Pololu)'),
    # --- torretta della camera sul muso
    ('cam_z', '29 mm', 'mm', 'Camera: quota dell asse ottico'),
    ('cam_tasca', 'cam_testa + 0.4 mm', 'mm', 'Camera: lato della tasca per la testa'),
    ('cam_tasca_prof', '3.5 mm', 'mm', 'Camera: profondita della tasca'),
    ('cam_foro', 'cam_lente_d + 0.6 mm', 'mm', 'Camera: foro della lente'),
    ('tor_semi', '11 mm', 'mm', 'Torretta della camera: semilarghezza'),
    ('tor_sp', '4 mm', 'mm', 'Torretta della camera: spessore dello stelo'),
    ('tor_testa_sp', '6 mm', 'mm', 'Torretta della camera: tasca + parete della lente'),
    ('tor_testa_z', '19 mm', 'mm', 'Torretta della camera: quota da cui parte la testa (sopra i regolatori)'),
    ('cam_rientro', '4 mm', 'mm', 'Camera: rientro della lente rispetto al muso (protegge la lente, lascia scorta al flat)'),
    ('tor_vis_semi', '9 mm', 'mm', 'Visiera davanti alla lente: semilarghezza (campo orizzontale libero 54 gradi per parte)'),
    ('tor_vis_z', '21 mm', 'mm', 'Visiera davanti alla lente: quota del bordo inferiore'),
    ('cor_tetto', '37.5 mm', 'mm', 'Guscio: quota del dorso sopra l asse dei femori'),
    ('gus_sp', '1.6 mm', 'mm', 'Guscio: spessore'),
    # --- elettronica: posizioni
    ('esp_cx', '19 mm', 'mm', 'ESP32: X del centro del PCB (antenna in avanti)'),
    ('esp_z', '28.6 mm', 'mm', 'ESP32: quota del lato inferiore del PCB'),
    ('bat_gioco_x', '3 mm', 'mm', 'Batteria: schiuma tra il pacco e la battuta anteriore'),
    # --- guscio (cover non strutturale)
    ('gus_k', 'gus_sp * (cor_lato - (cor_xa - cor_xb)) / (cor_yb - cor_yn)', 'mm', 'Guscio: arretramento in X dei vertici interni'),
    ('spo_x0', '2 mm', 'mm', 'Sportello di servizio: bordo anteriore (X negativa, dietro l origine)'),
    ('spo_x1', '58 mm', 'mm', 'Sportello di servizio: bordo posteriore'),
    ('spo_semi', '15 mm', 'mm', 'Sportello di servizio: semilarghezza'),
    ('gus_post_h', '12 mm', 'mm', 'Guscio: altezza dell apertura posteriore sopra l orlo (vano di servizio)'),
    ('gus_sm_y0', '30 mm', 'mm', 'Guscio: semilarghezza del dorso piano (da qui scende lo smusso dei fianchi)'),
    ('gus_sm_h', '14 mm', 'mm', 'Guscio: altezza dello smusso dei fianchi'),
    ('gus_sm_coda_x', '12 mm', 'mm', 'Guscio: lunghezza dello smusso della coda'),
    ('gus_sm_coda_h', '10.5 mm', 'mm', 'Guscio: altezza dello smusso della coda'),
    # --- fissaggio del guscio: linguette della base con inserto M2, viti dai fianchi; due viti sulla torretta
    ('lin_x', '22 mm', 'mm', 'Linguette dei fianchi: X del centro'),
    ('lin_coda_x', '74 mm', 'mm', 'Linguette della coda: X del centro (negativa)'),
    ('lin_larg', '8 mm', 'mm', 'Linguette: larghezza'),
    ('lin_sp', '4 mm', 'mm', 'Linguette: spessore (lunghezza dell inserto M2)'),
    ('lin_z0', '8 mm', 'mm', 'Linguette: quota inferiore'),
    ('lin_z1', '20 mm', 'mm', 'Linguette: quota superiore'),
    ('lin_vite_z', '17 mm', 'mm', 'Linguette: quota della vite'),
    ('tor_ins_y', '8 mm', 'mm', 'Torretta: Y degli inserti M2 per le viti del guscio'),
    ('asola_cavi_l', '10 mm', 'mm', 'Guscio: larghezza delle asole per i cavi di femore e ginocchio'),
    ('asola_cavi_h', '6 mm', 'mm', 'Guscio: altezza delle asole per i cavi di femore e ginocchio'),
    # --- vassoio dell ESP32 (porta la basetta con lo zoccolo)
    ('ssc_sp', '1.6 mm', 'mm', 'SSC-32: spessore del PCB (C)'),
    ('bas_z', 'esp_z - 12.6 mm', 'mm', 'Basetta: quota del lato inferiore (zoccolo 8,5 + distanziale dei pin 2,5 + PCB 1,6)'),
    ('bas_semi', '16.5 mm', 'mm', 'Basetta: semilarghezza dopo il taglio (13 file di fori)'),
    ('vas_sp', '1.6 mm', 'mm', 'Vassoio: spessore delle guide'),
    ('vas_labbro', '1.6 mm', 'mm', 'Vassoio: spessore del labbro laterale'),
    ('vas_semi_int', '14.5 mm', 'mm', 'Vassoio: inizio dell appoggio della basetta (fuori dalle saldature)'),
    ('vas_x0', '8 mm', 'mm', 'Vassoio: estremita posteriore (X negativa)'),
    ('vas_x1', 'vano_l - cor_xa + cor_tun', 'mm', 'Vassoio: estremita anteriore (filo della paratia: oltre ci sono le bugne del regolatore)'),
    ('vas_dist_d', '7 mm', 'mm', 'Vassoio: diametro dei distanziali sulle viti anteriori della SSC-32'),
    # --- sportelli (cover a incastro, da provare in stampa)
    ('spo_bordo', '2 mm', 'mm', 'Sportello del dorso: sormonto sul guscio'),
    ('spo_sp', '1.2 mm', 'mm', 'Sportello del dorso: spessore della piastra'),
    ('spo_tappo', '1.2 mm', 'mm', 'Sportello del dorso: spessore della cornice di centraggio'),
    ('coda_sp', '1.6 mm', 'mm', 'Sportello della coda: spessore della piastra'),
]

# asse della coxa anteriore sinistra e punto che ne da' la direzione radiale
AX = ('cor_coxa_x', 'cor_coxa_y')
DIR = ('cor_coxa_x + 20 mm * cos(cor_coxa_ang)', 'cor_coxa_y + 20 mm * sin(cor_coxa_ang)')
Z_SOTTO = '-(cor_h_sotto)'
H_SCAFO = 'cor_h_sotto + cor_orlo'
Z_INT = '-(cor_h_sotto - cor_fondo)'              # faccia superiore del fondo
H_INT = 'cor_h_sotto - cor_fondo + cor_orlo'
Z_GON = '-(cox_z0 + cul_fondo)'                   # faccia inferiore della gondola
H_GON = 'srv_alette_sotto + cul_fondo'
Z_ORLO_GON = 'srv_alette_sotto - cox_z0'          # orlo della gondola (appoggio delle alette)
Z_BUGNA = 'srv_alette_sotto - cox_z0 - ale_bugna_h'
Z_CAVO = '-(cox_z0 - srv_cavo_alt + 1.5 mm)'      # bordo inferiore della finestra del cavo
Z_DADO = 'srv_alette_sotto - cox_z0 - dado_m2_z - dado_m2_h'   # fondo della tasca del dado
X_VANO1 = 'vano_l - cor_xa'                       # X del fondo anteriore del vano batteria


def _corpo(root):
    """Sotto-assieme "Corpo" alla radice (terna del robot): contiene la base e cio' che vi e' montato."""
    occ = L['trova_occ'](root, 'Corpo')
    if occ:
        return occ[0]
    o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = 'Corpo'
    return o


def _occ(root):
    o = L['trova_occ'](_corpo(root).component, NOME)
    if not o:
        raise RuntimeError('manca %s: eseguire prima il passo "scafo"' % NOME)
    return o[0]


def fai_scafo(des, root):
    corpo = _corpo(root).component
    for o in L['trova_occ'](corpo, NOME):
        o.deleteMe()
    t0 = des.timeline.count
    occ = corpo.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = NOME
    p = Parte(occ.component)
    _pianta_piena(p, Z_SOTTO, H_SCAFO, 'scafo')
    # smusso del fondo lungo i fianchi: profilo piu' leggero, il fondo non si impunta sugli ostacoli
    sm = p.blocco_obl('x', '-(cor_xn)', 'smusso_fondo_sx', ('cor_yb', '-(cor_h_sotto - cor_smusso)'),
                      ('cor_yb - cor_smusso', '-(cor_h_sotto)'), '-(3 mm)', 'cor_smusso * sqrt(2) + 3 mm', '0 mm', '8 mm',
                      '2 * cor_xn', 1, TAGLIA)
    p.specchia([sm], 'y', 'smusso_fondo_dx')
    # vasca a spessore costante, aperta in alto (il fondo viene spesso quanto le pareti)
    p.svuota([_faccia_piana(p.c, 'z', p.val('cor_orlo'), 1)], 'cor_parete', 'svuotamento')
    L['raggruppa'](des, t0, 'Base: scafo')
    return p


def fai_gondole(des, root):
    p = Parte(_occ(root).component)
    t0 = des.timeline.count
    g = p.blocco_obl('z', Z_GON, 'gondola_as', AX, DIR, '-(gon_rad_ang)', 'cul_lungo', '-(cul_semi)', 'cul_semi', H_GON)
    b = p.blocco_obl('z', Z_BUGNA, 'bugna_as', AX, DIR, 'cul_lungo', 'cul_lungo + ale_bugna_l',
                     '-(ale_bugna / 2)', 'ale_bugna / 2', 'ale_bugna_h')
    # il collo d'angolo finisce perpendicolare all'asse della zampa: si rifila lungo la faccia interna della parete
    r = p.blocco_obl('z', Z_GON, 'rifilo_collo_as', ('cor_xa - cor_k', 'cor_yn - cor_parete'),
                     ('cor_xb - cor_k', 'cor_yb - cor_parete'), '0 mm', 'gon_rifilo', '0 mm', '12 mm', H_GON, 1, TAGLIA)
    gm = p.blocco('z', Z_GON, 'gondola_ms', '-(cul_semi)', 'cor_coxa_ym - gon_rad_med', 'cul_semi',
                  'cor_coxa_ym + cul_lungo', H_GON)
    bm = p.blocco('z', Z_BUGNA, 'bugna_ms', '-(ale_bugna / 2)', 'cor_coxa_ym + cul_lungo', 'ale_bugna / 2',
                  'cor_coxa_ym + cul_lungo + ale_bugna_l', 'ale_bugna_h')
    m = p.specchia([g, b, r], 'x', 'gondola_ps')
    p.specchia([g, b, r, gm, bm, m], 'y', 'gondole_dx')
    L['raggruppa'](des, t0, 'Base: gondole')
    return p


def fai_lavorazioni(des, root):
    p = Parte(_occ(root).component)
    t0 = des.timeline.count
    cs, sn = 'cos(cor_coxa_ang)', 'sin(cor_coxa_ang)'
    # --- gondola anteriore sinistra (inclinata)
    a = [
        p.blocco_obl('z', '-(cox_z0)', 'sede_servo_as', AX, DIR, '-(srv_corto + gio_servo)', 'srv_coda + gio_servo',
                     '-(srv_larg / 2 + gio_servo)', 'srv_larg / 2 + gio_servo', 'srv_alette_sotto', 1, TAGLIA),
        p.blocco_obl('z', Z_CAVO, 'finestra_cavo_as', AX, DIR, '-(gon_rad_ang + 3 mm)', '-(srv_corto)',
                     '-(cavo_fin_l / 2)', 'cavo_fin_l / 2', 'cavo_fin_h', 1, TAGLIA),
        p.cilindro('z', Z_GON, 'sede_cuscinetto_as', AX[0], AX[1], 'cus_sede_d', 'cus_sede_prof', 1, TAGLIA),
        p.cilindro('z', Z_GON, 'passaggio_perno_as', AX[0], AX[1], 'perno_passo', 'cul_fondo', 1, TAGLIA),
        p.cilindro('z', Z_ORLO_GON, 'foro_aletta_int_as', 'cor_coxa_x - ale_foro_corto * ' + cs,
                   'cor_coxa_y - ale_foro_corto * ' + sn, 'vite_m2_passante', 'ale_bugna_h', -1, TAGLIA),
        p.cilindro('z', Z_ORLO_GON, 'foro_aletta_est_as', 'cor_coxa_x + ale_foro_coda * ' + cs,
                   'cor_coxa_y + ale_foro_coda * ' + sn, 'vite_m2_passante', 'ale_bugna_h', -1, TAGLIA),
        # tasche dei dadi quadri: quella esterna si apre in punta alla bugna, quella interna sul fianco del collo
        p.blocco_obl('z', Z_DADO, 'tasca_dado_est_as', AX, DIR, 'ale_foro_coda - dado_m2_l / 2', 'cul_lungo + ale_bugna_l',
                     '-(dado_m2_l / 2)', 'dado_m2_l / 2', 'dado_m2_h', 1, TAGLIA),
        p.blocco_obl('z', Z_DADO, 'tasca_dado_int_as', AX, DIR, '-(ale_foro_corto + dado_m2_l / 2)',
                     '-(ale_foro_corto - dado_m2_l / 2)', '-(dado_m2_l / 2)', 'cul_semi', 'dado_m2_h', 1, TAGLIA),
    ]
    # --- gondola media sinistra (allineata agli assi: radiale = +Y)
    ym = 'cor_coxa_ym'
    b = [
        p.blocco('z', '-(cox_z0)', 'sede_servo_ms', '-(srv_larg / 2 + gio_servo)', ym + ' - srv_corto - gio_servo',
                 'srv_larg / 2 + gio_servo', ym + ' + srv_coda + gio_servo', 'srv_alette_sotto', 1, TAGLIA),
        p.blocco('z', Z_CAVO, 'finestra_cavo_ms', '-(cavo_fin_l / 2)', ym + ' - gon_rad_med - 3 mm', 'cavo_fin_l / 2',
                 ym + ' - srv_corto', 'cavo_fin_h', 1, TAGLIA),
        p.cilindro('z', Z_GON, 'sede_cuscinetto_ms', '0 mm', ym, 'cus_sede_d', 'cus_sede_prof', 1, TAGLIA),
        p.cilindro('z', Z_GON, 'passaggio_perno_ms', '0 mm', ym, 'perno_passo', 'cul_fondo', 1, TAGLIA),
        p.cilindro('z', Z_ORLO_GON, 'foro_aletta_int_ms', '0 mm', ym + ' - ale_foro_corto', 'vite_m2_passante',
                   'ale_bugna_h', -1, TAGLIA),
        p.cilindro('z', Z_ORLO_GON, 'foro_aletta_est_ms', '0 mm', ym + ' + ale_foro_coda', 'vite_m2_passante',
                   'ale_bugna_h', -1, TAGLIA),
        p.blocco('z', Z_DADO, 'tasca_dado_est_ms', '-(dado_m2_l / 2)', ym + ' + ale_foro_coda - dado_m2_l / 2', 'dado_m2_l / 2',
                 ym + ' + cul_lungo + ale_bugna_l', 'dado_m2_h', 1, TAGLIA),
        p.blocco('z', Z_DADO, 'tasca_dado_int_ms', '-(cul_semi)', ym + ' - ale_foro_corto - dado_m2_l / 2', 'dado_m2_l / 2',
                 ym + ' - ale_foro_corto + dado_m2_l / 2', 'dado_m2_h', 1, TAGLIA),
    ]
    m = p.specchia(a, 'x', 'lavorazioni_gondola_ps')
    p.specchia(a + b + [m], 'y', 'lavorazioni_gondole_dx')
    L['raggruppa'](des, t0, 'Base: lavorazioni gondole')
    return p


def fai_interno(des, root):
    p = Parte(_occ(root).component)
    t0 = des.timeline.count
    h_tun = 'vano_h + cor_tun'
    # tunnel della batteria: due pareti, tetto, paratia anteriore (fa da battuta)
    for nome, s in (('sx', 1), ('dx', -1)):
        y0, y1 = 'vano_w / 2', 'vano_w / 2 + cor_tun'
        if s < 0:
            y0, y1 = '-(%s)' % y1, '-(%s)' % y0
        p.blocco('z', Z_INT, 'tunnel_' + nome, '-(cor_xa)', y0, X_VANO1 + ' + cor_tun', y1, h_tun)
    p.blocco('z', 'vano_h - cor_h_sotto + cor_fondo', 'tunnel_tetto', '-(cor_xa - vano_tetto_x)', '-(vano_w / 2 + cor_tun)',
             X_VANO1 + ' + cor_tun', 'vano_w / 2 + cor_tun', 'cor_tun')
    # paratia anteriore a tutta altezza: chiude il tunnel, irrigidisce le radici delle gondole anteriori,
    # porta il regolatore posteriore. Due asole in alto per cavi di potenza e cavi delle zampe anteriori.
    p.blocco('z', Z_INT, 'paratia_ant', X_VANO1, '-(cor_par_semi)', X_VANO1 + ' + cor_tun', 'cor_par_semi', H_INT)
    z_tetto = 'vano_h - cor_h_sotto + cor_fondo + cor_tun'
    aso = p.blocco('z', z_tetto, 'asola_paratia_sx', X_VANO1, 'par_asola_y0', X_VANO1 + ' + cor_tun', 'par_asola_y1',
                   'cor_orlo - (%s)' % z_tetto, 1, TAGLIA)
    p.specchia([aso], 'y', 'asola_paratia_dx')
    # telaio posteriore: unisce le pareti del tunnel allo scafo dove inizia la coda
    for nome, s in (('sx', 1), ('dx', -1)):
        y0, y1 = 'vano_w / 2', 'cor_yn - cor_parete / 2'
        if s < 0:
            y0, y1 = '-(%s)' % y1, '-(%s)' % y0
        p.blocco('z', Z_INT, 'telaio_post_' + nome, '-(cor_xa)', y0, '-(cor_xa - cor_tun)', y1, h_tun)
    # colonnine della SSC-32 (inserti M3), appoggiate alle pareti del tunnel
    h_col = 'ssc_z + cor_h_sotto - cor_fondo'
    col = []
    for nome, x in (('ant', 'ssc_fori_x / 2 - ssc_dx'), ('post', '-(ssc_fori_x / 2 + ssc_dx)')):
        col.append(p.blocco('z', Z_INT, 'ssc_colonna_%s_sx' % nome, x + ' - ssc_col_semi', 'vano_w / 2 + cor_tun / 2',
                            x + ' + ssc_col_semi', 'ssc_fori_y / 2 + ssc_col_semi', h_col))
        col.append(p.cilindro('z', 'ssc_z', 'ssc_inserto_%s_sx' % nome, x, 'ssc_fori_y / 2', 'ins_m3_d', 'ins_m3_l', -1, TAGLIA))
    p.specchia(col, 'y', 'ssc_colonne_dx')
    # bugne dei due regolatori (inserti M2): uno sulla paratia, uno sulla parete del muso
    z_lo = '-(reg_z_basso - reg_foro_bordo)'
    z_hi = 'reg_foro_bordo + reg_fori_y - reg_z_basso'
    bug = []
    for nome, q, verso in (('par', X_VANO1 + ' + cor_tun', 1), ('muso', 'cor_xn - cor_parete', -1)):
        for lato, z in (('basso', z_lo), ('alto', z_hi)):
            bug.append(p.cilindro('x', q, 'reg_bugna_%s_%s_sx' % (nome, lato), 'reg_fori_x / 2', z, 'reg_bugna_d', 'reg_dist', verso))
            qf = q + (' + reg_dist' if verso > 0 else ' - reg_dist')
            bug.append(p.cilindro('x', qf, 'reg_inserto_%s_%s_sx' % (nome, lato), 'reg_fori_x / 2', z, 'ins_m2_d', 'ins_m2_l',
                                  -verso, TAGLIA))
    p.specchia(bug, 'y', 'reg_bugne_dx')
    # torretta della camera: stelo sul muso e testa con la tasca (aperta dietro, il flat esce in alto)
    # La lente rientra di cam_rientro dentro una visiera: e' protetta dagli urti e il flat (61,5 mm utili)
    # arriva al connettore dell'ESP32 con circa 5 mm di scorta.
    x_cam = 'cor_xn - cam_rientro - tor_testa_sp'
    p.blocco('z', 'cor_orlo', 'torretta', 'cor_xn - tor_sp', '-(tor_semi)', 'cor_xn', 'tor_semi', 'tor_testa_z - cor_orlo')
    p.blocco('z', 'tor_testa_z', 'torretta_testa', x_cam, '-(tor_semi)', 'cor_xn', 'tor_semi', 'cor_tetto - gus_sp - tor_testa_z')
    p.blocco('z', 'tor_vis_z', 'visiera', 'cor_xn - cam_rientro', '-(tor_vis_semi)', 'cor_xn', 'tor_vis_semi',
             'cor_tetto - gus_sp - tor_vis_z', 1, TAGLIA)
    p.blocco('x', x_cam, 'tasca_camera', '-(cam_tasca / 2)', 'cam_z - cam_tasca / 2', 'cam_tasca / 2',
             'cam_z + cam_tasca / 2', 'cam_tasca_prof', 1, TAGLIA)
    p.cilindro('x', x_cam, 'foro_lente', '0 mm', 'cam_z', 'cam_foro', 'tor_testa_sp', 1, TAGLIA)
    ti = p.cilindro('z', 'cor_tetto - gus_sp', 'inserto_torretta_sx', x_cam + ' + tor_testa_sp / 2', 'tor_ins_y', 'ins_m2_d',
                    'ins_m2_l', -1, TAGLIA)
    p.specchia([ti], 'y', 'inserto_torretta_dx')
    # nervature alle radici delle gondole: prolungano dentro lo scafo i fianchi della culla
    n_as = p.blocco_obl('z', Z_INT, 'nervatura_as', AX, DIR, '-(gon_rad_ang + ner_l)', '-(gon_rad_ang - 2 mm)',
                        'cul_semi - cor_parete', 'cul_semi', h_tun)
    n_ms = p.blocco('z', Z_INT, 'nervatura_ms', 'cul_semi - cor_parete', 'cor_yb - cor_parete - ner_l', 'cul_semi',
                    'cor_yb - cor_parete / 2', Z_ORLO_GON + ' + cor_h_sotto - cor_fondo')
    m1 = p.specchia([n_as], 'x', 'nervatura_ps')
    m2 = p.specchia([n_ms], 'x', 'nervatura_ms_post')
    p.specchia([n_as, n_ms, m1, m2], 'y', 'nervature_dx')
    # linguette per il guscio: salgono dentro il suo bordo, lo centrano e portano gli inserti M2 delle viti
    y1 = 'cor_yb - gus_sp - gio_stampa'
    t1 = p.blocco('z', 'lin_z0', 'linguetta_fianco_as', 'lin_x - lin_larg / 2', y1 + ' - lin_sp', 'lin_x + lin_larg / 2', y1,
                  'lin_z1 - lin_z0')
    i1 = p.cilindro('y', y1, 'inserto_fianco_as', 'lin_x', 'lin_vite_z', 'ins_m2_d', 'ins_m2_l', -1, TAGLIA)
    yc = 'cor_yn - gus_sp - gio_stampa'
    t2 = p.blocco('z', 'lin_z0', 'linguetta_coda_sx', '-(lin_coda_x + lin_larg / 2)', yc + ' - lin_sp',
                  '-(lin_coda_x - lin_larg / 2)', yc, 'lin_z1 - lin_z0')
    i2 = p.cilindro('y', yc, 'inserto_coda_sx', '-(lin_coda_x)', 'lin_vite_z', 'ins_m2_d', 'ins_m2_l', -1, TAGLIA)
    m = p.specchia([t1, i1], 'x', 'linguetta_fianco_ps')
    p.specchia([t1, i1, t2, i2, m], 'y', 'linguette_dx')
    # feritoie nel fondo del muso, sotto il canale d'aria tra i due regolatori
    x_fer = X_VANO1 + ' + cor_tun + (cor_xn - cor_parete - (' + X_VANO1 + ' + cor_tun)) / 2'
    fe = p.blocco('z', Z_SOTTO, 'feritoia_fondo_sx', x_fer + ' - fer_l / 2', 'fer_y0', x_fer + ' + fer_l / 2', 'fer_y1',
                  'cor_fondo', 1, TAGLIA)
    p.specchia([fe], 'y', 'feritoia_fondo_dx')
    # apertura posteriore: uscita della batteria e vano di servizio
    p.blocco('z', Z_INT, 'apertura_post', '-(cor_xn)', '-(vano_w / 2)', '-(cor_xn - cor_parete)', 'vano_w / 2', H_INT, 1, TAGLIA)
    L['raggruppa'](des, t0, 'Base: interno')
    return p


def _parte(root, nome):
    """Crea (cancellando l'esistente) una parte dentro Corpo e ne restituisce il costruttore."""
    corpo = _corpo(root).component
    for o in L['trova_occ'](corpo, nome):
        o.deleteMe()
    T0[nome] = corpo.parentDesign.timeline.count        # dopo la cancellazione: il gruppo parte da qui
    occ = corpo.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = nome
    return Parte(occ.component)


def _pianta_piena(p, q, h, pref):
    """Prisma pieno con la pianta dello scafo, dal piano z = q per l'altezza h."""
    p.blocco('z', q, pref, '-(cor_xn)', '-(cor_yn)', 'cor_xn', 'cor_yn', h, 1, NUOVO)
    p.blocco('z', q, pref + '_ala', '-(cor_xb)', '-(cor_yb)', 'cor_xb', 'cor_yb', h)
    sp = p.blocco_obl('z', q, pref + '_spalla_as', ('cor_xa', 'cor_yn'), ('cor_xb', 'cor_yb'),
                      '0 mm', 'cor_lato', '0 mm', 'cor_spalla', h)
    m = p.specchia([sp], 'x', pref + '_spalla_ps')
    p.specchia([sp, m], 'y', pref + '_spalle_dx')


def _faccia_piana(comp, asse, quota_mm, verso):
    """Faccia piana del corpo con normale lungo `asse` (verso +1 / -1) alla quota data (mm)."""
    for f in comp.bRepBodies.item(0).faces:
        if f.geometry.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType:
            continue
        pt = f.pointOnFace
        ok, n = f.evaluator.getNormalAtPoint(pt)
        if abs({'x': n.x, 'y': n.y, 'z': n.z}[asse] - verso) > 1e-6:
            continue
        if abs({'x': pt.x, 'y': pt.y, 'z': pt.z}[asse] * 10 - quota_mm) < 1e-4:
            return f
    raise RuntimeError('faccia piana non trovata: %s = %s' % (asse, quota_mm))


def fai_guscio(des, root):
    """Guscio superiore, non strutturale: pianta della base, dorso sfaccettato, spessore costante."""
    p = _parte(root, 'Corpo_Guscio')
    t0 = T0['Corpo_Guscio']
    _pianta_piena(p, 'cor_orlo', 'cor_tetto - cor_orlo', 'guscio')
    # smussi: i fianchi scendono dal dorso piano, la coda scende verso il retro
    lung = 'sqrt((cor_yb - gus_sm_y0) * (cor_yb - gus_sm_y0) + gus_sm_h * gus_sm_h)'
    sm = p.blocco_obl('x', '-(cor_xn)', 'smusso_fianco_sx', ('gus_sm_y0', 'cor_tetto'), ('cor_yb', 'cor_tetto - gus_sm_h'),
                      '-(3 mm)', lung + ' + 3 mm', '0 mm', '15 mm', '2 * cor_xn', 1, TAGLIA)
    p.specchia([sm], 'y', 'smusso_fianco_dx')
    lung_c = 'sqrt(gus_sm_coda_x * gus_sm_coda_x + gus_sm_coda_h * gus_sm_coda_h)'
    p.blocco_obl('y', '-(cor_yb)', 'smusso_coda', ('-(cor_xn - gus_sm_coda_x)', 'cor_tetto'),
                 ('-(cor_xn)', 'cor_tetto - gus_sm_coda_h'), '-(3 mm)', lung_c + ' + 3 mm', '-(15 mm)', '0 mm',
                 '2 * cor_yb', 1, TAGLIA)
    p.svuota([_faccia_piana(p.c, 'z', p.val('cor_orlo'), -1)], 'gus_sp', 'svuotamento')
    hi = 'cor_tetto - gus_sp - cor_orlo'
    # aperture: torretta della camera e visiera, sportello di servizio sul dorso, vano di servizio in coda
    p.blocco('z', 'cor_orlo', 'asola_torretta', 'cor_xn - gus_sp', '-(tor_semi + gio_stampa)', 'cor_xn', 'tor_semi + gio_stampa',
             hi, 1, TAGLIA)
    p.blocco('z', 'cor_tetto - gus_sp', 'visiera_guscio', 'cor_xn - cam_rientro', '-(tor_vis_semi)', 'cor_xn', 'tor_vis_semi',
             'gus_sp', 1, TAGLIA)
    p.blocco('z', 'cor_tetto - gus_sp', 'apertura_sportello', '-(spo_x1)', '-(spo_semi)', '-(spo_x0)', 'spo_semi', 'gus_sp', 1, TAGLIA)
    p.blocco('z', 'cor_orlo', 'apertura_post', '-(cor_xn)', '-(vano_w / 2)', '-(cor_xn - gus_sp)', 'vano_w / 2', 'gus_post_h', 1, TAGLIA)
    x_fer = X_VANO1 + ' + cor_tun + (cor_xn - cor_parete - (' + X_VANO1 + ' + cor_tun)) / 2'
    fe = p.blocco('z', 'cor_tetto - gus_sp', 'feritoia_dorso_sx', x_fer + ' - fer_l / 2', 'fer_dorso_y0', x_fer + ' + fer_l / 2',
                  'fer_y1', 'gus_sp', 1, TAGLIA)
    p.specchia([fe], 'y', 'feritoia_dorso_dx')
    # asole sul bordo inferiore per i cavi dei servo di femore e ginocchio, sopra il collo di ogni gondola
    a = p.blocco_obl('z', 'cor_orlo', 'asola_cavi_as', AX, DIR, '-(gon_rad_ang + 3 mm)', '-(cul_corto + 1 mm)',
                     '-(asola_cavi_l / 2)', 'asola_cavi_l / 2', 'asola_cavi_h', 1, TAGLIA)
    b = p.blocco('z', 'cor_orlo', 'asola_cavi_ms', '-(asola_cavi_l / 2)', 'cor_coxa_ym - gon_rad_med - 3 mm', 'asola_cavi_l / 2',
                 'cor_coxa_ym - cul_corto - 1 mm', 'asola_cavi_h', 1, TAGLIA)
    m = p.specchia([a], 'x', 'asola_cavi_ps')
    p.specchia([a, b, m], 'y', 'asole_cavi_dx')
    # fori per le viti M2: quattro sui fianchi e due in coda (nelle linguette della base), due sulla torretta
    f1 = p.cilindro('y', 'cor_yb', 'foro_vite_fianco_as', 'lin_x', 'lin_vite_z', 'vite_m2_passante', 'gus_sp + 1 mm', -1, TAGLIA)
    f2 = p.cilindro('y', 'cor_yn', 'foro_vite_coda_sx', '-(lin_coda_x)', 'lin_vite_z', 'vite_m2_passante', 'gus_sp + 1 mm', -1, TAGLIA)
    f3 = p.cilindro('z', 'cor_tetto', 'foro_vite_torretta_sx', 'cor_xn - cam_rientro - tor_testa_sp / 2', 'tor_ins_y',
                    'vite_m2_passante', 'gus_sp', -1, TAGLIA)
    m = p.specchia([f1], 'x', 'foro_vite_fianco_ps')
    p.specchia([f1, f2, f3, m], 'y', 'fori_viti_dx')
    L['raggruppa'](des, t0, 'Guscio')
    return p


def fai_vassoio(des, root):
    """Vassoio dell'ESP32: due guide con labbro per la basetta, a sbalzo sopra la SSC-32.

    Davanti appoggia sulla paratia; e' stretto dalle due viti anteriori della SSC-32 attraverso
    due alette con distanziale.
    """
    p = _parte(root, 'Vassoio_ESP32')
    t0 = T0['Vassoio_ESP32']
    zg = 'bas_z - vas_sp'
    y_lab0, y_lab1 = 'bas_semi + gio_stampa', 'bas_semi + gio_stampa + vas_labbro'
    xl = 'ssc_fori_x / 2 - ssc_dx'
    primo = True
    for nome, s in (('sx', 1), ('dx', -1)):
        def y(e0, e1):
            return (e0, e1) if s > 0 else ('-(%s)' % e1, '-(%s)' % e0)
        y0, y1 = y('vas_semi_int', y_lab1)
        p.blocco('z', zg, 'guida_' + nome, '-(vas_x0)', y0, 'vas_x1', y1, 'vas_sp', 1, NUOVO if primo else UNISCI)
        if primo:
            # traverse: dietro la basetta e sulla paratia (piede di appoggio)
            p.blocco('z', zg, 'traversa_post', '-(vas_x0)', '-(vas_semi_int)', '-(vas_x0 - 2 mm)', 'vas_semi_int', 'vas_sp')
            p.blocco('z', 'cor_orlo', 'piede_paratia', X_VANO1, '-(%s)' % y_lab1, X_VANO1 + ' + cor_tun', y_lab1,
                     'bas_z - vas_sp - cor_orlo')
            primo = False
        y0, y1 = y(y_lab0, y_lab1)
        p.blocco('z', 'bas_z', 'labbro_' + nome, '-(vas_x0)', y0, 'vas_x1', y1, 'vas_labbro + 1 mm')
        y0, y1 = y(y_lab0, 'ssc_fori_y / 2 + 4 mm')
        p.blocco('z', zg, 'aletta_' + nome, xl + ' - 4 mm', y0, xl + ' + 4 mm', y1, 'vas_sp')
        yc = 'ssc_fori_y / 2' if s > 0 else '-(ssc_fori_y / 2)'
        p.cilindro('z', 'ssc_z + ssc_sp', 'distanziale_' + nome, xl, yc, 'vas_dist_d', 'bas_z - vas_sp - ssc_z - ssc_sp')
        p.cilindro('z', 'bas_z', 'foro_vite_' + nome, xl, yc, 'vite_m3_passante', 'bas_z - ssc_z - ssc_sp', -1, TAGLIA)
    L['raggruppa'](des, t0, 'Vassoio ESP32')
    return p


def fai_sportelli(des, root):
    """Sportello di servizio sul dorso e sportello della coda: cover a incastro, senza viti."""
    # --- dorso: piastra che sormonta l'apertura, cornice di centraggio, dente davanti e scatto dietro
    p = _parte(root, 'Sportello_Dorso')
    t0 = T0['Sportello_Dorso']
    zc, hc = 'cor_tetto - gus_sp - 1 mm', 'gus_sp + 1 mm'
    p.blocco('z', 'cor_tetto', 'piastra', '-(spo_x1 + spo_bordo)', '-(spo_semi + spo_bordo)', '-(spo_x0 - spo_bordo)',
             'spo_semi + spo_bordo', 'spo_sp', 1, NUOVO)
    p.blocco('z', zc, 'cornice', '-(spo_x1 - gio_stampa)', '-(spo_semi - gio_stampa)', '-(spo_x0 + gio_stampa)',
             'spo_semi - gio_stampa', hc)
    p.blocco('z', zc, 'cornice_vuoto', '-(spo_x1 - gio_stampa - spo_tappo)', '-(spo_semi - gio_stampa - spo_tappo)',
             '-(spo_x0 + gio_stampa + spo_tappo)', 'spo_semi - gio_stampa - spo_tappo', hc, 1, TAGLIA)
    p.blocco('z', zc, 'dente_ant', '-(spo_x0 + gio_stampa)', '-(8 mm)', '-(spo_x0 - 1.5 mm)', '8 mm', '0.9 mm')
    p.blocco('z', zc, 'scatto_post', '-(spo_x1 + 0.5 mm)', '-(4 mm)', '-(spo_x1 - gio_stampa)', '4 mm', '0.9 mm')
    L['raggruppa'](des, t0, 'Sportello del dorso')
    # --- coda: piastra esterna, due guide che entrano nell'apertura, dente a scatto dietro la parete
    q = _parte(root, 'Sportello_Coda')
    t0 = T0['Sportello_Coda']
    q.blocco('x', '-(cor_xn + coda_sp)', 'piastra', '-(vano_w / 2 + 3 mm)', '-(cor_h_sotto)', 'vano_w / 2 + 3 mm',
             'cor_orlo + gus_post_h + 1 mm', 'coda_sp', 1, NUOVO)
    for nome, sg in (('sx', 1), ('dx', -1)):
        def y(e0, e1):
            return (e0, e1) if sg > 0 else ('-(%s)' % e1, '-(%s)' % e0)
        y0, y1 = y('vano_w / 2 - gio_stampa - 1.2 mm', 'vano_w / 2 - gio_stampa')
        q.blocco('x', '-(cor_xn)', 'guida_' + nome, y0, '-(cor_h_sotto - cor_fondo - 0.3 mm)', y1,
                 'cor_orlo + gus_post_h - 0.3 mm', '5 mm')
        y0, y1 = y('vano_w / 2 - gio_stampa', 'vano_w / 2 + 0.3 mm')
        q.blocco('x', '-(cor_xn - cor_parete - 0.3 mm)', 'scatto_' + nome, y0, '-(4 mm)', y1, '4 mm', '1.2 mm')
    L['raggruppa'](des, t0, 'Sportello della coda')
    p.n += q.n
    p.non_vincolati += q.non_vincolati
    return p


def stato_parte(des, root, nome):
    occ = L['trova_occ'](_corpo(root).component, nome)
    if not occ:
        return 'assente'
    c = occ[0].component
    rep = {'corpi': c.bRepBodies.count, 'lavorazioni': c.features.count,
           'non_vincolati': [s.name for s in c.sketches if not s.isFullyConstrained]}
    if c.bRepBodies.count:
        b = c.bRepBodies.item(0)
        bb = b.boundingBox
        rep['volume_cm3'] = round(sum(x.volume for x in c.bRepBodies), 2)
        rep['ingombro_mm'] = [round(v * 10, 2) for v in (bb.minPoint.x, bb.minPoint.y, bb.minPoint.z,
                                                          bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z)]
    return rep


def stato(des, root):
    occ = _occ(root)
    c = occ.component
    rep = {'corpi': c.bRepBodies.count, 'lavorazioni': c.features.count, 'schizzi': c.sketches.count,
           'non_vincolati': [s.name for s in c.sketches if not s.isFullyConstrained],
           'timeline': des.timeline.count}
    if c.bRepBodies.count:
        b = c.bRepBodies.item(0)
        bb = b.boundingBox
        rep['volume_cm3'] = round(b.volume, 2)
        rep['ingombro_mm'] = [round(v * 10, 2) for v in (bb.minPoint.x, bb.minPoint.y, bb.minPoint.z,
                                                          bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z)]
        rep['facce'] = b.faces.count
    errori = []
    for f in c.features:
        try:
            if f.healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState:
                errori.append((f.name, f.errorOrWarningMessage))
        except Exception:
            pass
    rep['lavorazioni_non_sane'] = errori
    rep['altri_componenti'] = sentinella(des)
    return rep


# Volumi (mm3) delle parti che NON devono cambiare quando si lavora sul corpo: un taglio fatto senza
# limitare i corpi partecipanti asporta anche le parti degli altri componenti (successo l'8 ottobre 2026).
VOLUMI_ATTESI = {'Coxa': 11771.42, 'Femore_B': 4819.63, 'Femore_A': 1922.56, 'Tibia': 7992.76,
                 'Rif_Cuscinetto_F683ZZ': 104.68, 'Rif_Perno_3x10': 70.69}


def sentinella(des):
    """Confronta i volumi delle parti delle zampe e dei componenti comprati con quelli attesi."""
    diversi = {}
    for c in des.allComponents:
        if c.name in VOLUMI_ATTESI:
            vol = round(sum(b.volume for b in c.bRepBodies) * 1000, 2)
            if abs(vol - VOLUMI_ATTESI[c.name]) > 0.05 or c.bRepBodies.count != 1:
                diversi[c.name] = {'volume': vol, 'atteso': VOLUMI_ATTESI[c.name], 'corpi': c.bRepBodies.count}
    return diversi or 'invariati'


PASSI = {'scafo': fai_scafo, 'gondole': fai_gondole, 'lavorazioni': fai_lavorazioni, 'interno': fai_interno,
         'guscio': fai_guscio, 'vassoio': fai_vassoio, 'sportelli': fai_sportelli}


def main(passi):
    out = {'passi': passi}
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
        if 'parametri' in passi:
            out['parametri'] = L['aggiungi_parametri'](des, PARAMETRI)
            out['controllo'] = {n: round(v(n), 3) for n in ('cor_lato', 'cor_k', 'cor_spalla', 'gon_rad_med', 'cor_par_semi',
                                                              'par_asola_y0', 'par_asola_y1', 'reg_z_basso')}
        for nome, fn in PASSI.items():
            if nome in passi:
                p = fn(des, root)
                out[nome] = {'lavorazioni': p.n, 'schizzi_non_vincolati': p.non_vincolati}
        if 'stato' in passi:
            out['stato'] = stato(des, root)
            out['stato']['Corpo_Guscio'] = stato_parte(des, root, 'Corpo_Guscio')
            out['stato']['Vassoio_ESP32'] = stato_parte(des, root, 'Vassoio_ESP32')
            out['stato']['Sportello_Dorso'] = stato_parte(des, root, 'Sportello_Dorso')
            out['stato']['Sportello_Coda'] = stato_parte(des, root, 'Sportello_Coda')
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1))
