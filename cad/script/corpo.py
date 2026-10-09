"""Corpo dell'esapode MG996R (fase 4, D-050): base strutturale, chiglia, coperchio.

Si esegue dentro Fusion sul design "Hexapod v2 - MG996R", un passo per chiamata:
    import runpy
    def run(_context: str):
        runpy.run_path('/Users/paul/hexapod-v2/cad/script/corpo.py')['main'](['parametri', 'base'])

Terna del robot (componente "Corpo", all'origine della radice): X in avanti, Y a sinistra, Z in alto,
z = 0 sul piano degli assi dei femori. Assi delle coxe: d'angolo (+-cor_ang_x, +-cor_ang_y) a +-cor_ang_dir
dall'asse X (posteriori a 180 - cor_ang_dir), medie (0, +-cor_med_y) a +-90 gradi.
Le gondole sono culle uguali a quelle della zampa (parametri cul_*), con l'albero in alto, la coda verso
l'esterno lungo la direzione neutra della zampa e il lato corto (fessura del passacavo) verso il centro.
Si modellano la gondola anteriore sinistra (inclinata) e la media sinistra; le altre sono specchiature.
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

PARAMETRI = [
    # --- assi delle coxe (D-050)
    ('cor_ang_x', '80 mm', 'mm', 'Corpo: X degli assi delle coxe d angolo'),
    ('cor_ang_y', '44 mm', 'mm', 'Corpo: Y degli assi delle coxe d angolo'),
    ('cor_ang_dir', '30 deg', 'deg', 'Corpo: direzione neutra delle zampe anteriori dall asse X'),
    ('cor_med_y', '48 mm', 'mm', 'Corpo: Y degli assi delle coxe medie'),
    # --- quote in altezza (valori assoluti; z negative dove indicato)
    ('cor_fondo', 'srv_sotto + cul_gio_fondo + cul_fondo - cz_alette_coxa', 'mm', 'Corpo: fondo della base e delle gondole sotto il piano dei femori'),
    ('cor_ripiano', '2 mm', 'mm', 'Corpo: spessore del ripiano delle baie'),
    ('cor_tetto', '9.4 mm', 'mm', 'Corpo: faccia superiore del tetto del tunnel sotto il piano dei femori'),
    ('cor_tetto_sp', '2 mm', 'mm', 'Corpo: spessore del tetto del tunnel'),
    ('cor_orlo', '7 mm', 'mm', 'Corpo: orlo della base sopra il piano dei femori (sotto la testa dell anima della coxa, +8,05)'),
    ('cor_chiglia', '41.4 mm', 'mm', 'Corpo: fondo della chiglia sotto il piano dei femori (quota della nervatura della coxa)'),
    ('cor_chiglia_sp', '2 mm', 'mm', 'Corpo: fondo della chiglia'),
    # --- pianta
    ('cor_tun_x0', '85.4 mm', 'mm', 'Corpo: coda del tunnel (X negativa)'),
    ('cor_tun_x1', '81 mm', 'mm', 'Corpo: fronte del tunnel'),
    ('cor_tun_semi', '27 mm', 'mm', 'Corpo: semilarghezza esterna del tunnel (interno 50)'),
    ('cor_parete', '2 mm', 'mm', 'Corpo: pareti'),
    ('cor_baia_x', '65.5 mm', 'mm', 'Corpo: estremo delle baie lungo X'),
    ('cor_baia_y', '50 mm', 'mm', 'Corpo: parete esterna delle baie'),
    ('cor_fronte_semi', '17 mm', 'mm', 'Corpo: apertura della parete anteriore sopra il tetto (vassoio e basetta)'),
    # --- SSC-32 su bugne del tetto (viti M2,5 in fori pilota, niente distanziali)
    ('cor_ssc_x', '-14 mm', 'mm', 'Corpo: X del centro della SSC-32'),
    ('cor_ssc_bugna_d', '7 mm', 'mm', 'Corpo: diametro delle bugne della SSC-32'),
    ('vite_m25_pilota', '2.1 mm', 'mm', 'Foro pilota per vite M2,5 autofilettante'),
    # --- regolatori dei servo in piedi nelle baie anteriori, su bugne della parete esterna della baia (inserti M2),
    #     componenti verso il tunnel: la parete esterna e' alta fino all'orlo, il fianco del tunnel no
    ('cor_reg_x0', '14 mm', 'mm', 'Regolatori: X del bordo posteriore del circuito'),
    ('cor_reg_ztop', '2.5 mm', 'mm', 'Regolatori: Z del bordo superiore del circuito (la vite della slitta passa sopra; bugne basse 0,26 sopra il ripiano)'),
    ('cor_reg_dist', '5 mm', 'mm', 'Regolatori: dal retro del circuito alla parete della baia (slitta 2,4 + distanziali 2,6; reofori 1,8)'),
    ('cor_slitta_sp', '2.4 mm', 'mm', 'Slitta dei regolatori: spessore della piastra'),
    ('reg_foro_x0', '2.159 mm', 'mm', 'Pololu D42V110F6: foro dal lato corto (STEP) V'),
    ('reg_foro_y0', '4.191 mm', 'mm', 'Pololu D42V110F6: foro dal lato lungo delle piazzole (STEP; i fori non sono centrati) V'),
    ('cor_reg_bugna_d', '5.2 mm', 'mm', 'Regolatori: diametro delle bugne (un reoforo del regolatore passa a circa 2,7 dal foro)'),
    ('reg_l', '43.18 mm', 'mm', 'Pololu D42V110F6: lunghezza (STEP) V'),
    ('reg_w', '31.75 mm', 'mm', 'Pololu D42V110F6: larghezza (STEP) V'),
    ('reg_fori_x', '38.86 mm', 'mm', 'Pololu D42V110F6: interasse dei fori lungo il lato lungo V'),
    ('reg_fori_y', '25.4 mm', 'mm', 'Pololu D42V110F6: interasse dei fori lungo il lato corto V'),
    # --- viti della chiglia (M3 in inserti della base): due davanti fuori dal tunnel, due dietro nella zona dei cavi
    ('cor_chi_vite_y', '15 mm', 'mm', 'Chiglia: Y delle viti anteriori'),
    ('cor_chi_vite_xa', '3 mm', 'mm', 'Chiglia: viti anteriori davanti alla parete del tunnel (centro dalla faccia esterna; la bugna entra 0,7 nella parete)'),
    ('cor_chi_vite_xp', '52 mm', 'mm', 'Chiglia: X delle viti posteriori, sotto le baie posteriori (fuori dal percorso del pacco)'),
    ('cor_chi_vite_yp', '31 mm', 'mm', 'Chiglia: Y delle viti posteriori'),
    ('cor_chi_bugna_d', '7.4 mm', 'mm', 'Chiglia: diametro delle bugne degli inserti M3'),
    ('cor_chi_orecchia', '3 mm', 'mm', 'Chiglia: spessore delle orecchie anteriori'),
    # --- vassoio dell'ESP32 e torretta della camera (PETG)
    ('cor_vas_z', '1 mm', 'mm', 'Vassoio: lato inferiore del piano'),
    ('cor_vas_sp', '1.6 mm', 'mm', 'Vassoio: spessore del piano'),
    ('cor_vas_x0', '26 mm', 'mm', 'Vassoio: estremo posteriore (davanti alla SSC-32)'),
    ('cor_vas_x1', '82 mm', 'mm', 'Vassoio: estremo anteriore'),
    ('cor_vas_col_d', '6 mm', 'mm', 'Vassoio: diametro delle colonnine'),
    # --- Wago in piedi sul ripiano delle baie posteriori, portafusibile F1 sul tetto in coda
    ('cor_wago_x', '31 mm', 'mm', 'Wago: X (negativa) del centro, sul ripiano della baia posteriore'),
    ('cor_wago_luce', '0.5 mm', 'mm', 'Wago: aria tra il dorso e il fianco del tunnel'),
    ('cor_sede_gio', '0.2 mm', 'mm', 'Sedi di Wago e F1: gioco per lato'),
    ('cor_sede_h', '6 mm', 'mm', 'Sede dei Wago: altezza delle pareti'),
    ('cor_bas_x0', '22 mm', 'mm', 'Basetta: bordo posteriore (file dei pin dell ESP32 da 22,5; SSC-32 fino a 22)'),
    ('cor_bas_luce', '3.3 mm', 'mm', 'Basetta: luce sopra il vassoio (sotto ci sono le teste M3 alte 3 e le saldature)'),
    ('cor_bas_col_d', '5.8 mm', 'mm', 'Basetta: diametro delle colonnine del vassoio con inserto M2'),
    ('cor_cam_x', '92.5 mm', 'mm', 'Camera: X del retro della testa'),
    ('cor_cam_z', '22.5 mm', 'mm', 'Camera: Z dell asse ottico'),
    # --- vano di coda e sportello della batteria
    ('cor_cavi_x', '13 mm', 'mm', 'Tetto: fessure per i cavi della batteria, lunghezza dalla coda'),
    ('cor_cavi_y0', '20.5 mm', 'mm', 'Tetto: fessure dei cavi accanto ai capi del portafusibile F1 (|y| da 20,5 a 25)'),
    ('cor_sport_sp', '2 mm', 'mm', 'Sportello della batteria: spessore'),
    ('cor_sport_rebbio', '17 mm', 'mm', 'Sportello: lunghezza dei rebbi che premono il pacco (con schiuma) contro la battuta'),
    ('cor_sport_vite_y', '28.5 mm', 'mm', 'Sportello: Y delle due viti in basso, nei blocchetti della chiglia (2,3 mm dal mozzo della coxa posteriore)'),
    ('cor_sport_vite_z', '36.7 mm', 'mm', 'Sportello: Z (negativa) delle viti, a meta altezza della chiglia'),
    ('cor_sport_blocco', '8 mm', 'mm', 'Chiglia: lunghezza lungo X dei blocchetti delle viti dello sportello'),
    ('cor_sport_ling', '6 mm', 'mm', 'Sportello: profondita della linguetta sotto il tetto (0,4 dal tetto, 1,0 sopra il pacco)'),
    ('cor_gonna_sp', '1.2 mm', 'mm', 'Coperchio: spessore della gonna'),
    ('cor_gonna_x0', '22 mm', 'mm', 'Coperchio: gonna laterale da qui (22 mm dall asse della coxa media)'),
    ('cor_gonna_x1', '58.8 mm', 'mm', 'Coperchio: gonna laterale fino a qui (22 mm dall asse della coxa d angolo)'),
    # --- colonnine del coperchio sul tetto del tunnel, feritoie delle baie anteriori
    ('cor_col_xa', '40 mm', 'mm', 'Coperchio: X delle colonnine anteriori (accanto al vassoio, dietro le pareti di prua)'),
    ('cor_col_xp', '56 mm', 'mm', 'Coperchio: X (negativa) delle colonnine posteriori (tra F1 a -61,4 e la SSC-32 a -50,8)'),
    ('cor_col_y', '22.5 mm', 'mm', 'Coperchio: Y delle colonnine (vassoio fino a 16,5, fianco del tunnel a 27)'),
    ('cor_fer_l', '6 mm', 'mm', 'Feritoie: lunghezza lungo X'),
    ('cor_fer_w', '3 mm', 'mm', 'Feritoie: larghezza'),
    ('cor_fer_y', '30 mm', 'mm', 'Feritoie: Y del centro (camino tra i componenti dei regolatori e il tunnel)'),
    # --- coperchio
    ('cor_cop_z', '28.4 mm', 'mm', 'Coperchio: lato inferiore del dorso'),
    ('cor_serv_x0', '-20 mm', 'mm', 'Coperchio: apertura di servizio sopra USB e pulsanti dell ESP32, inizio'),
    ('cor_serv_x1', '28 mm', 'mm', 'Coperchio: apertura di servizio, fine'),
    ('cor_serv_semi', '17 mm', 'mm', 'Coperchio: apertura di servizio, semilarghezza'),
    ('cor_cop_sp', '1.6 mm', 'mm', 'Coperchio: spessore del dorso'),
    ('cor_cop_lobo', '22 mm', 'mm', 'Coperchio: raggio dei lobi sopra gli assi delle coxe'),
    ('cor_muso_x', '101 mm', 'mm', 'Coperchio: punta del muso'),
    ('cor_muso_semi', '20 mm', 'mm', 'Coperchio: semilarghezza del muso'),
    ('cor_muso_giu', '-1 mm', 'mm', 'Muso: bordo inferiore della fascia (sotto il vassoio, che finisce a z +1)'),
    ('cor_muso_finestra_d', '17 mm', 'mm', 'Muso: finestra della camera (cono di 120 gradi dal centro ottico a 2,5 mm, piu la lente Ø8)'),
    # --- carapace "Piena" (D-060, D-061): sostituisce il coperchio
    ('car_top', 'cor_cop_z + 7.6 mm', 'mm', 'Carapace: cima (6 mm d aria in piu sopra regolatori, cicalino e flat)'),
    ('car_sp', 'cor_cop_sp', 'mm', 'Carapace: pareti'),
    ('car_smusso', '6 mm', 'mm', 'Carapace: smusso unico a 45 gradi del contorno superiore'),
    ('car_lobo_R', '32.3 mm', 'mm', 'Carapace: lobi esagonali sugli assi delle coxe, raggio ai vertici (un lato perpendicolare a ogni zampa)'),
    ('car_lobo_a', 'car_lobo_R * cos(30 deg)', 'mm', 'Carapace: apotema dei lobi'),
    ('car_valle_y', '56 mm', 'mm', 'Carapace: fondo delle valli tra i lobi (copre le bugne delle slitte, y 50-55,7)'),
    ('car_viso_x', '102 mm', 'mm', 'Carapace: viso, tra le punte dei lobi anteriori'),
    ('car_coda_x', 'cor_ang_x + car_lobo_R / 2 + 1 mm', 'mm', 'Carapace: coda, 1 mm oltre il vertice del lobo posteriore'),
    ('car_testa_y', '30 mm', 'mm', 'Carapace: semilarghezza del nucleo di testa e coda'),
    ('car_r_conv', '12 mm', 'mm', 'Carapace: raccordo in pianta dei vertici convessi (Piena; piu del doppio dello smusso)'),
    ('car_r_conc', '10 mm', 'mm', 'Carapace: raccordo in pianta dei vertici concavi'),
    ('car_mento_z', 'cor_muso_giu', 'mm', 'Testa: fondo, sotto il vassoio'),
    ('car_mento_semi', '9.2 mm', 'mm', 'Testa: semilarghezza del mento (fuori da mensola e torretta, |y| 6)'),
    ('car_testa_semi', '25.2 mm', 'mm', 'Testa: fianchi verticali sotto il carapace'),
    ('car_testa_x0', 'cor_vas_x1 + 0.6 mm', 'mm', 'Testa: retro della parte bassa (il vassoio arriva a x 82)'),
    ('car_rastr', '60 deg', 'deg', 'Testa: inclinazione dei fianchi rastremati'),
    ('car_paratia_y0', '15 mm', 'mm', 'Paratie dietro la testa: da qui (ESP32 fino a |y| 14,15)'),
    ('car_paratia_y1', '28.5 mm', 'mm', 'Paratie dietro la testa: fino a qui'),
    ('car_fascia_semi', '17 mm', 'mm', 'Fascia nera: semilarghezza'),
    ('car_fascia_h', '0.6 mm', 'mm', 'Fascia nera: intarsio (3 strati da 0,2)'),
    ('car_pozzo_d', '7 mm', 'mm', 'Carapace: pozzetti delle viti'),
    ('car_pozzo_D', '9.4 mm', 'mm', 'Carapace: tubo dei pozzetti'),
    ('car_serv_semi', '16 mm', 'mm', 'Carapace: apertura di servizio |y| <= 16 (la fascia resta larga 1 mm ai lati)'),
    ('car_serv_smusso', '6 mm', 'mm', 'Carapace: angoli a 45 gradi dell apertura (ottagono)'),
    ('car_battuta', '1.5 mm', 'mm', 'Carapace: battuta dello sportellino sotto la pelle'),
    ('car_puls_x', '-40 mm', 'mm', 'Pulsante d accensione sull asse, sopra lo zoccolo XBee della SSC-32'),
    ('car_puls_d', '12.2 mm', 'mm', 'Foro del pulsante da pannello Ø12 (B3b)'),
    ('cic_x0', '-87 mm', 'mm', 'Cicalino: estremo posteriore (pin verso la coda)'),
    ('cic_x1', '-62 mm', 'mm', 'Cicalino: estremo anteriore'),
    ('cic_semi', '20 mm', 'mm', 'Cicalino: semilarghezza (lato da 40 lungo Y)'),
    ('cic_z0', '17.4 mm', 'mm', 'Cicalino: fondo (sopra il T-plug a 14,1)'),
    ('car_fin_l', '14 mm', 'mm', 'Finestra del display del cicalino: lunghezza'),
    ('car_fin_semi', '12 mm', 'mm', 'Finestra del display: semilarghezza'),
    ('car_guancia_x0', 'car_coda_x + 3.35 mm', 'mm', 'Guance di coda: retro (1 mm dentro il lato del lobo posteriore)'),
    ('car_guancia_x1', 'cor_tun_x0 + cor_sport_sp + 0.2 mm', 'mm', 'Guance di coda: fronte (0,2 dietro lo sportello della batteria)'),
    ('car_guancia_y0', '25.4 mm', 'mm', 'Guance di coda: da qui'),
    ('car_guancia_y1', 'cor_tun_semi', 'mm', 'Guance di coda: fino a qui'),
    ('car_guancia_giu', 'cor_tetto - 1 mm', 'mm', 'Guance di coda: fondo (1 mm sopra lo sportello, che si sfila sotto)'),
    ('car_occhio_x0', 'cor_cam_x + cam_alt + 0.9 mm', 'mm', 'Occhio: bocca interna, 0,9 davanti alla lente'),
    ('cam_fov_h', '54.2 deg', 'deg', 'Camera: semicampo orizzontale (120 gradi in diagonale su 4:3, caso peggiore)'),
    ('cam_fov_v', '46.1 deg', 'deg', 'Camera: semicampo verticale'),
    ('car_occhio_marg', '0.8 mm', 'mm', 'Occhio: margine sul campo'),
    ('car_occhio_si', 'cam_lente_d / 2 + (car_occhio_x0 - cor_cam_x - cam_alt) * tan(cam_fov_h) + car_occhio_marg', 'mm', 'Occhio: semilarghezza della bocca interna'),
    ('car_occhio_vi', 'cam_lente_d / 2 + (car_occhio_x0 - cor_cam_x - cam_alt) * tan(cam_fov_v) + car_occhio_marg', 'mm', 'Occhio: semialtezza della bocca interna'),
    ('car_occhio_se', 'cam_lente_d / 2 + (car_viso_x - cor_cam_x - cam_alt) * tan(cam_fov_h) + car_occhio_marg', 'mm', 'Occhio: semilarghezza della bocca esterna'),
    ('car_occhio_ve', 'cam_lente_d / 2 + (car_viso_x - cor_cam_x - cam_alt) * tan(cam_fov_v) + car_occhio_marg', 'mm', 'Occhio: semialtezza della bocca esterna'),
    ('car_bugna_semi', '11 mm', 'mm', 'Visiera: bugna dell occhio dietro la visiera, semilarghezza'),
    ('car_bugna_z0', 'cor_cam_z - 7.5 mm', 'mm', 'Visiera: fondo della bugna dell occhio'),
]

T0 = {}
N_FER = 5          # feritoie per baia anteriore, distribuite sulla lunghezza del regolatore


def _x_feritoia(i):
    return 'cor_reg_x0 + 4 mm + %d * (reg_l - 8 mm - cor_fer_l) / %d' % (i, N_FER - 1)


def _corpo(root):
    occ = L['trova_occ'](root, 'Corpo')
    if occ:
        return occ[0]
    o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = 'Corpo'
    return o


def _nuovo_comp(corpo, nome):
    genitore = corpo.component
    # una alla volta: dopo la prima cancellazione i riferimenti alle altre occorrenze possono non valere piu'
    while L['trova_occ'](genitore, nome):
        L['trova_occ'](genitore, nome)[0].deleteMe()
    T0[nome] = genitore.parentDesign.timeline.count
    occ = genitore.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = nome
    return occ


def _chiudi(des, nome, p):
    if nome not in T0:                     # Fusion ha aggiunto un suffisso al nome del componente
        nome = [k for k in T0 if nome.startswith(k)][-1]
    L['raggruppa'](des, T0[nome], nome)
    return {'lavorazioni': p.n, 'schizzi_non_vincolati': p.non_vincolati}


# ----------------------------------------------------------------------------------- gondole
def _punto(d, e):
    """Punto (x, y) a distanza d lungo la direzione della coxa d'angolo anteriore sinistra e e di traverso."""
    return ('cor_ang_x + (%s) * cos(cor_ang_dir) - (%s) * sin(cor_ang_dir)' % (d, e),
            'cor_ang_y + (%s) * sin(cor_ang_dir) + (%s) * cos(cor_ang_dir)' % (d, e))


def _asse_ang():
    return (('cor_ang_x', 'cor_ang_y'), ('cor_ang_x + 10 mm * cos(cor_ang_dir)', 'cor_ang_y + 10 mm * sin(cor_ang_dir)'))


def _rett_ang(p, q, nome, a0, a1, b0, b1, h, verso=1, op=UNISCI):
    p0, p1 = _asse_ang()
    return p.blocco_obl('z', q, nome, p0, p1, a0, a1, b0, b1, h, verso, op)


def _rett_med(p, q, nome, a0, a1, b0, b1, h, verso=1, op=UNISCI):
    """Gondola media sinistra: asse in (0, cor_med_y), coda verso +Y; a lungo Y, b verso -X."""
    return p.blocco('z', q, nome, '-(%s)' % b1, 'cor_med_y + (%s)' % a0, '-(%s)' % b0, 'cor_med_y + (%s)' % a1, h, verso, op)


def gondola(p, quale):
    """Gondola anteriore sinistra ('ang') o media sinistra ('med'). Ritorna la lista delle lavorazioni."""
    if quale == 'ang':
        def rett(q, nome, a0, a1, b0, b1, h, verso=1, op=UNISCI):
            return _rett_ang(p, q, nome + '_ang', a0, a1, b0, b1, h, verso, op)

        def cil(q, nome, d, e, diam, h, verso=1, op=TAGLIA):
            x, y = _punto(d, e)
            return p.cilindro('z', q, nome + '_ang', x, y, diam, h, verso, op)
    else:
        def rett(q, nome, a0, a1, b0, b1, h, verso=1, op=UNISCI):
            return _rett_med(p, q, nome + '_med', a0, a1, b0, b1, h, verso, op)

        def cil(q, nome, d, e, diam, h, verso=1, op=TAGLIA):
            return p.cilindro('z', q, nome + '_med', '-(%s)' % e, 'cor_med_y + (%s)' % d, diam, h, verso, op)
    f = []
    # pieni: culla, bugne sotto le alette
    f.append(rett('-(cor_fondo)', 'culla', '-(cul_corto)', 'cul_coda', '-(cul_semi)', 'cul_semi', 'cor_fondo + cz_alette_coxa'))
    f.append(rett('cz_alette_coxa - cul_bugna_h', 'bugna_corto', '-(bug_corto)', '-(cul_corto)', '-(bug_semi)', 'bug_semi',
                  'cul_bugna_h'))
    f.append(rett('cz_alette_coxa - cul_bugna_h', 'bugna_coda', 'cul_coda', 'bug_coda', '-(bug_semi)', 'bug_semi', 'cul_bugna_h'))
    # sede del servo, passacavo, cuscinetto, viti delle alette (come nella zampa, D-049)
    f.append(rett('cz_alette_coxa - srv_sotto - cul_gio_fondo', 'sede', '-(cul_sede_corto)', 'cul_sede_coda',
                  '-(cul_sede_semi)', 'cul_sede_semi', 'srv_sotto + cul_gio_fondo + 1 mm', 1, TAGLIA))
    f.append(rett('cz_alette_coxa - cav_fin_alto', 'gola', '-(cul_sede_corto + cav_gola_p)', '-(cul_sede_corto - 0.5 mm)',
                  '-(cav_gola_w / 2)', 'cav_gola_w / 2', 'cav_fin_alto + 1 mm', 1, TAGLIA))
    f.append(rett('cz_alette_coxa - cav_fin_basso', 'finestra', '-(cul_corto + 0.5 mm)', '-(cul_sede_corto - 0.5 mm)',
                  '-(cav_fin_w / 2)', 'cav_fin_w / 2', 'cav_fin_basso - cav_fin_alto', 1, TAGLIA))
    f.append(rett('cz_alette_coxa - cav_fin_alto', 'fessura', '-(bug_corto + 0.5 mm)', '-(cul_sede_corto - 0.5 mm)',
                  '-(cav_fes_semi)', 'cav_fes_semi', 'cav_fin_alto + 1 mm', 1, TAGLIA))
    f.append(cil('-(cor_fondo)', 'sede_cuscinetto', '0 mm', '0 mm', 'cus_sede_d', 'cus_sede_prof'))
    f.append(cil('-(cor_fondo)', 'passaggio_perno', '0 mm', '0 mm', 'cus_passo_d', 'cul_fondo'))
    for nome, e in (('ins_coda_a', '-(ins_y)'), ('ins_coda_b', 'ins_y')):
        f.append(cil('cz_alette_coxa', nome, 'ins_coda', e, 'ins_m3_d', 'ins_m3_l', -1))
    for nome, e in (('pilota_a', '-(ins_y + ale_vite_sposta)'), ('pilota_b', 'ins_y + ale_vite_sposta')):
        f.append(cil('cz_alette_coxa', nome, '-(ale_foro_corto)', e, 'vite_m3_pilota', 'ins_m3_l', -1))
    return f


# ----------------------------------------------------------------------------------- parti
def fai_base(corpo):
    occ = _nuovo_comp(corpo, 'Corpo_Base')
    p = Parte(occ.component)
    # tunnel della batteria (parte alta: la chiglia chiude sotto), ripiano e pareti delle baie
    p.blocco('z', '-(cor_fondo)', 'tunnel', '-(cor_tun_x0)', '-(cor_tun_semi)', 'cor_tun_x1', 'cor_tun_semi',
             'cor_fondo - cor_tetto', 1, NUOVO)
    sx = [p.blocco('z', '-(cor_fondo)', 'ripiano_s', '-(cor_baia_x)', 'cor_tun_semi', 'cor_baia_x', 'cor_baia_y', 'cor_ripiano'),
          # pareti esterne delle baie interrotte sulla gondola media (sopra l'orlo ci sono alette e cassa del servo di coxa)
          p.blocco('z', '-(cor_fondo)', 'parete_baia_as', 'cul_semi', 'cor_baia_y - cor_parete', 'cor_baia_x', 'cor_baia_y',
                   'cor_fondo + cor_orlo'),
          p.blocco('z', '-(cor_fondo)', 'parete_baia_ps', '-(cor_baia_x)', 'cor_baia_y - cor_parete', '-(cul_semi)', 'cor_baia_y',
                   'cor_fondo + cor_orlo'),
          p.blocco('z', '-(cor_tetto)', 'fronte_s', 'cor_tun_x1 - cor_parete', 'cor_fronte_semi', 'cor_tun_x1', 'cor_tun_semi',
                   'cor_tetto + cor_orlo')]
    # pareti di collegamento tra gondole, baie e tunnel, fino al tetto (portano il momento delle coxe allo scafo)
    h_par = 'cor_fondo - cor_tetto'
    sx.append(p.blocco('z', '-(cor_fondo)', 'collo_med_a', 'cul_sede_semi', 'cor_tun_semi', 'cul_semi', 'cor_med_y - cul_corto', h_par))
    sx.append(p.blocco('z', '-(cor_fondo)', 'collo_med_p', '-(cul_semi)', 'cor_tun_semi', '-(cul_sede_semi)', 'cor_med_y - cul_corto', h_par))
    sx.append(p.blocco('z', '-(cor_fondo)', 'paratia_ang_a', 'cor_baia_x - 7.3 mm', 'cor_tun_semi', 'cor_baia_x - 5.3 mm',
                       'cor_baia_y - cor_parete', h_par))
    sx.append(p.blocco('z', '-(cor_fondo)', 'paratia_ang_p', '-(cor_baia_x - 5.3 mm)', 'cor_tun_semi', '-(cor_baia_x - 7.3 mm)',
                       'cor_baia_y - cor_parete', h_par))
    # guide della slitta del regolatore sulla parete della baia anteriore, e bugna esterna per la sua vite
    # le guide trattengono i bordi della slitta nella fascia libera tra i distanziali alti e quelli bassi
    z_g0 = 'cor_reg_ztop - (reg_foro_y0 + reg_fori_y) + cor_reg_bugna_d / 2 + 0.5 mm'
    h_g = 'reg_fori_y - cor_reg_bugna_d - 1 mm'
    y_g0, y_g1 = 'cor_baia_y - cor_parete - cor_slitta_sp - 1.4 mm', 'cor_baia_y - cor_parete - cor_slitta_sp - 0.2 mm'
    for nome, xa, xb, xl0, xl1 in (('guida_p', 'cor_reg_x0 - 1.5 mm', 'cor_reg_x0 - 0.5 mm', 'cor_reg_x0 - 1.5 mm', 'cor_reg_x0 + 0.6 mm'),
                                   ('guida_a', 'cor_reg_x0 + reg_l + 0.5 mm', 'cor_reg_x0 + reg_l + 1.5 mm',
                                    'cor_reg_x0 + reg_l - 0.6 mm', 'cor_reg_x0 + reg_l + 1.5 mm')):
        sx.append(p.blocco('z', z_g0, nome, xa, y_g0, xb, 'cor_baia_y - cor_parete', h_g))          # gamba fino alla parete
        sx.append(p.blocco('z', z_g0, nome + '_labbro', xl0, y_g0, xl1, y_g1, h_g))              # labbro davanti al bordo
    x_v = 'cor_reg_x0 + reg_l / 2'
    sx.append(p.cilindro('y', 'cor_baia_y', 'slitta_bugna', x_v, 'cor_orlo - 1 mm', 'cor_chi_bugna_d', 'ins_m3_l - cor_parete + 1 mm'))
    sx.append(p.cilindro('y', 'cor_baia_y - cor_parete', 'slitta_ins', x_v, 'cor_orlo - 1 mm', 'ins_m3_d', 'ins_m3_l', 1, TAGLIA))
    for nome, x in (('colonnina_a', 'cor_col_xa'), ('colonnina_p', '-(cor_col_xp)')):
        sx.append(p.cilindro('z', '-(cor_tetto)', nome, x, 'cor_col_y', 'cor_chi_bugna_d', 'cor_tetto + cor_cop_z'))
        sx.append(p.cilindro('z', 'cor_cop_z', nome + '_ins', x, 'cor_col_y', 'ins_m3_d', 'ins_m3_l', -1, TAGLIA))
    # sede del Wago in piedi (ingressi dei fili in alto, leve verso la parete della baia): due spalle e due labbri
    # sulle estremita' della faccia delle leve (1 mm sul corpo, fuori dalle leve)
    zr = '-(cor_fondo) + cor_ripiano'
    yf = 'cor_tun_semi + cor_wago_luce + wago_h + cor_sede_gio'          # davanti alla faccia delle leve
    xe, xi = 'cor_wago_x + wago_l / 2 + cor_sede_gio', 'cor_wago_x - wago_l / 2 - cor_sede_gio'
    for nome, x0, x1, xl0, xl1 in (('wago_spalla_p', '-(%s + 1.6 mm)' % xe, '-(%s)' % xe, '-(%s + 1.6 mm)' % xe, '-(cor_wago_x + wago_l / 2 - 1 mm)'),
                                   ('wago_spalla_a', '-(%s)' % xi, '-(%s - 1.6 mm)' % xi, '-(cor_wago_x - wago_l / 2 + 1 mm)', '-(%s - 1.6 mm)' % xi)):
        sx.append(p.blocco('z', zr, nome, x0, 'cor_tun_semi - 1 mm', x1, yf + ' + 1.6 mm', 'cor_sede_h'))
        sx.append(p.blocco('z', zr, nome + '_labbro', xl0, yf, xl1, yf + ' + 1.6 mm', 'cor_sede_h'))
    for i in range(N_FER):
        x = _x_feritoia(i)
        sx.append(p.blocco('z', '-(cor_fondo)', 'feritoia_%d' % i, x, 'cor_fer_y - cor_fer_w / 2', x + ' + cor_fer_l',
                           'cor_fer_y + cor_fer_w / 2', 'cor_ripiano', 1, TAGLIA))
    sx.append(p.cilindro('z', '-(cor_fondo)', 'chi_bugna_p', '-(cor_chi_vite_xp)', 'cor_chi_vite_yp', 'cor_chi_bugna_d', 'ins_m3_l + 1 mm'))
    sx.append(p.cilindro('z', '-(cor_fondo)', 'chi_ins_p', '-(cor_chi_vite_xp)', 'cor_chi_vite_yp', 'ins_m3_d', 'ins_m3_l', 1, TAGLIA))
    sx.append(p.cilindro('z', '-(cor_fondo)', 'chi_bugna_a', 'cor_tun_x1 + cor_chi_vite_xa', 'cor_chi_vite_y', 'cor_chi_bugna_d',
                         'ins_m3_l + 1 mm'))
    sx.append(p.cilindro('z', '-(cor_fondo)', 'chi_ins_a', 'cor_tun_x1 + cor_chi_vite_xa', 'cor_chi_vite_y', 'ins_m3_d',
                         'ins_m3_l', 1, TAGLIA))
    gond = gondola(p, 'ang')
    gond_p = p.specchia(gond, 'x', 'gondola_posteriore_s')
    med = gondola(p, 'med')
    # bugne della SSC-32 sul tetto
    bug = []
    for nome, sx_, sy_ in (('ssc_bugna_aa', 1, 1), ('ssc_bugna_ab', 1, -1), ('ssc_bugna_pa', -1, 1), ('ssc_bugna_pb', -1, -1)):
        x = 'cor_ssc_x %s ssc_fori_x / 2' % ('+' if sx_ > 0 else '-')
        y = ('ssc_fori_y / 2') if sy_ > 0 else '-(ssc_fori_y / 2)'
        bug.append(p.cilindro('z', '-(cor_tetto)', nome, x, y, 'cor_ssc_bugna_d', 'ssc_dist'))
        bug.append(p.cilindro('z', '-(cor_tetto) + ssc_dist', nome + '_ins', x, y, 'ins_m2_d', 'ins_m2_l', -1, TAGLIA))
    # specchiatura del lato sinistro sul destro
    p.specchia(sx + gond + [gond_p] + med, 'y', 'lato_destro')
    # interno del tunnel (aperto sotto, verso la chiglia, e dietro, per la batteria)
    p.blocco('z', '-(cor_fondo)', 'interno_tunnel', '-(cor_tun_x0)', '-(cor_tun_semi - cor_parete)', 'cor_tun_x1 - cor_parete',
             'cor_tun_semi - cor_parete', 'cor_fondo - cor_tetto - cor_tetto_sp', 1, TAGLIA)
    for lato, y0, y1 in (('s', 'cor_cavi_y0', 'cor_tun_semi - cor_parete'), ('d', '-(cor_tun_semi - cor_parete)', '-(cor_cavi_y0)')):
        p.blocco('z', '-(cor_tetto) - cor_tetto_sp', 'fessura_cavi_' + lato, '-(cor_tun_x0 - cor_parete)', y0,
                 '-(cor_tun_x0 - cor_parete - cor_cavi_x)', y1, 'cor_tetto_sp', 1, TAGLIA)
    # costole che fermano il portafusibile F1 lungo X sul tetto (lo stringe una fascetta che passa nelle fessure dei cavi)
    for nome, x0, x1 in (('costola_f1_p', '-(cor_tun_x0 - cor_parete + cor_sede_gio + 1.2 mm)', '-(cor_tun_x0 - cor_parete + cor_sede_gio)'),
                         ('costola_f1_a', '-(cor_tun_x0 - cor_parete - fus_w - cor_sede_gio)', '-(cor_tun_x0 - cor_parete - fus_w - cor_sede_gio - 1.2 mm)')):
        p.blocco('z', '-(cor_tetto)', nome, x0, '-(12 mm)', x1, '12 mm', '3 mm')
    # bugne del vassoio (distanziali M3 maschio-femmina da 10, voce B18) sul tetto, con inserti M3
    for nome, x, y in _vassoio_fori():
        p.cilindro('z', '-(cor_tetto)', nome, x, y, 'cor_chi_bugna_d', 'cor_tetto + cor_vas_z - 5 mm')
        p.cilindro('z', 'cor_vas_z - 5 mm', nome + '_ins', x, y, 'ins_m3_d', 'ins_m3_l', -1, TAGLIA)
    return occ, p


def fai_chiglia(corpo):
    occ = _nuovo_comp(corpo, 'Corpo_Chiglia')
    p = Parte(occ.component)
    p.blocco('z', '-(cor_chiglia)', 'vasca', '-(cor_tun_x0)', '-(cor_tun_semi)', 'cor_tun_x1', 'cor_tun_semi',
             'cor_chiglia - cor_fondo', 1, NUOVO)
    p.blocco('z', '-(cor_chiglia) + cor_chiglia_sp', 'interno', '-(cor_tun_x0)', '-(cor_tun_semi - cor_parete)',
             'cor_tun_x1 - cor_parete', 'cor_tun_semi - cor_parete', 'cor_chiglia - cor_fondo', 1, TAGLIA)
    for lato, y in (('s', 'cor_chi_vite_y'), ('d', '-(cor_chi_vite_y)')):
        p.blocco('z', '-(cor_chiglia)', 'orecchia_a' + lato, 'cor_tun_x1 - cor_parete', y + ' - cor_chi_bugna_d / 2',
                 'cor_tun_x1 + cor_chi_vite_xa + cor_chi_bugna_d / 2', y + ' + cor_chi_bugna_d / 2', 'cor_chiglia - cor_fondo')
        p.cilindro('z', '-(cor_chiglia)', 'foro_orecchia_a' + lato, 'cor_tun_x1 + cor_chi_vite_xa', y, 'vite_m3_pass',
                   'cor_chiglia - cor_fondo', 1, TAGLIA)
    for lato, y in (('s', 'cor_chi_vite_yp'), ('d', '-(cor_chi_vite_yp)')):
        yy0, yy1 = ('cor_tun_semi - 1 mm', y + ' + cor_chi_bugna_d / 2') if lato == 's' else (y + ' - cor_chi_bugna_d / 2', '-(cor_tun_semi - 1 mm)')
        p.blocco('z', '-(cor_fondo) - cor_chi_orecchia', 'orecchia_p' + lato, '-(cor_chi_vite_xp) - cor_chi_bugna_d / 2', yy0,
                 '-(cor_chi_vite_xp) + cor_chi_bugna_d / 2', yy1, 'cor_chi_orecchia')
        p.cilindro('z', '-(cor_fondo) - cor_chi_orecchia', 'foro_orecchia_p' + lato, '-(cor_chi_vite_xp)', y, 'vite_m3_pass',
                   'cor_chi_orecchia', 1, TAGLIA)
    # blocchetti in coda, fuori dal tunnel (sotto le gondole posteriori), con gli inserti delle viti dello sportello
    for lato, y in (('s', 'cor_sport_vite_y'), ('d', '-(cor_sport_vite_y)')):
        yy0, yy1 = ('cor_tun_semi - 1 mm', y + ' + cor_chi_bugna_d / 2') if lato == 's' else (y + ' - cor_chi_bugna_d / 2', '-(cor_tun_semi - 1 mm)')
        p.blocco('z', '-(cor_chiglia)', 'blocco_sport_' + lato, '-(cor_tun_x0)', yy0, '-(cor_tun_x0) + cor_sport_blocco', yy1,
                 'cor_chiglia - cor_fondo')
        p.cilindro('x', '-(cor_tun_x0)', 'ins_sport_' + lato, y, '-(cor_sport_vite_z)', 'ins_m3_d', 'ins_m3_l', 1, TAGLIA)
    return occ, p


def _vassoio_fori():
    """Quattro distanziali M3 tra tetto e vassoio, fuori dagli ingombri di SSC-32, Wago ed ESP32."""
    y = 'cor_fronte_semi - 4.5 mm'
    return [('vas_bugna_pa', 'cor_vas_x0 + 4 mm', y), ('vas_bugna_pb', 'cor_vas_x0 + 4 mm', '-(%s)' % y),
            ('vas_bugna_aa', 'cor_tun_x1 - cor_parete - 4 mm', y), ('vas_bugna_ab', 'cor_tun_x1 - cor_parete - 4 mm', '-(%s)' % y)]


def _basetta_fori():
    """Colonnine M2 della basetta: tra le due file di pin dell'ESP32 (|y| da 11,1), fuori dalle teste M3 del vassoio."""
    xp, xa = 'cor_bas_x0 + 7 mm', 'cor_bas_x0 + bas_l - 2.5 mm'          # le posteriori restano sul vassoio (da x 26)
    return [('bas_col_pa', xp, '6.8 mm'), ('bas_col_pb', xp, '-(6.8 mm)'), ('bas_col_aa', xa, '6.5 mm'), ('bas_col_ab', xa, '-(6.5 mm)')]


def fai_slitta(corpo):
    """Slitta del regolatore anteriore sinistro (per il destro serve la specchiata: stessa parte capovolta)."""
    occ = _nuovo_comp(corpo, 'Corpo_Slitta_Regolatore')
    p = Parte(occ.component)
    yp = 'cor_baia_y - cor_parete'
    p.blocco('y', yp, 'piastra', 'cor_reg_x0 - 0.2 mm', '-(cor_fondo) + cor_ripiano + 0.2 mm', 'cor_reg_x0 + reg_l + 0.2 mm',
             'cor_orlo + 2 mm', 'cor_slitta_sp', -1, NUOVO)
    for nome, dx, dz in (('a', 'reg_l - reg_foro_x0', 'reg_foro_y0'), ('b', 'reg_foro_x0', 'reg_foro_y0'),
                         ('c', 'reg_l - reg_foro_x0', 'reg_foro_y0 + reg_fori_y'), ('d', 'reg_foro_x0', 'reg_foro_y0 + reg_fori_y')):
        x, z = 'cor_reg_x0 + ' + dx, 'cor_reg_ztop - (%s)' % dz
        p.cilindro('y', yp + ' - cor_slitta_sp', 'distanziale_' + nome, x, z, 'cor_reg_bugna_d', 'cor_reg_dist - cor_slitta_sp', -1)
        p.cilindro('y', yp + ' - cor_reg_dist', 'ins_' + nome, x, z, 'ins_m2_d', 'ins_m2_l', 1, TAGLIA)
    p.cilindro('y', yp, 'foro_vite', 'cor_reg_x0 + reg_l / 2', 'cor_orlo - 1 mm', 'vite_m3_pass', 'cor_slitta_sp', -1, TAGLIA)
    return occ, p


def fai_sportello(corpo):
    occ = _nuovo_comp(corpo, 'Corpo_Sportello')
    p = Parte(occ.component)
    zt = '-(cor_tetto) - cor_tetto_sp'
    # piastra fino al fondo della chiglia, con le orecchie delle due viti in basso
    p.blocco('x', '-(cor_tun_x0)', 'piastra', '-(cor_tun_semi)', '-(cor_chiglia)', 'cor_tun_semi', '-(cor_tetto)', 'cor_sport_sp', -1, NUOVO)
    for lato, y0, y1, y in (('s', 'cor_tun_semi - 1 mm', 'cor_sport_vite_y + 3.2 mm', 'cor_sport_vite_y'),
                            ('d', '-(cor_sport_vite_y + 3.2 mm)', '-(cor_tun_semi - 1 mm)', '-(cor_sport_vite_y)')):
        p.blocco('x', '-(cor_tun_x0)', 'orecchia_' + lato, y0, '-(cor_chiglia)', y1, '-(cor_fondo)', 'cor_sport_sp', -1)
        p.cilindro('x', '-(cor_tun_x0)', 'foro_' + lato, y, '-(cor_sport_vite_z)', 'vite_m3_pass', 'cor_sport_sp', -1, TAGLIA)
    # linguetta sotto il tetto: impedisce alla parte alta di aprirsi (lo sportello si infila e si sfila lungo X)
    p.blocco('z', zt + ' - 1.6 mm', 'linguetta', '-(cor_tun_x0)', '-(8 mm)', '-(cor_tun_x0) + cor_sport_ling', '8 mm', '1.2 mm')
    # rebbi che premono il pacco (con la schiuma) contro la battuta anteriore; tra i due passano i cavi della batteria
    for lato, y in (('s', '12 mm'), ('d', '-(12 mm)')):
        p.blocco('x', '-(cor_tun_x0)', 'rebbio_' + lato, y + ' - 2 mm', '-(29 mm)', y + ' + 2 mm', zt + ' - 4 mm',
                 'cor_sport_rebbio', 1)
    # smusso 1 x 45 sul contorno della faccia esterna: con le guance del carapace fa la cornice della porta (D-061)
    xe = -(p.val('cor_tun_x0') + p.val('cor_sport_sp'))
    corpo_b = occ.component.bRepBodies.item(0)
    fe = [fa for fa in corpo_b.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType
          and abs(fa.pointOnFace.x * 10 - xe) < 0.01]
    _smussa(p, [e for fa in fe for e in fa.edges if e.geometry.curveType == adsk.core.Curve3DTypes.Line3DCurveType],
            '1 mm', 'smusso_cornice', False)
    p.info = {'facce_esterne': len(fe), 'volume_cm3': round(corpo_b.volume, 2)}
    return occ, p


def fai_vassoio(corpo):
    occ = _nuovo_comp(corpo, 'Corpo_Vassoio')
    p = Parte(occ.component)
    p.blocco('z', 'cor_vas_z', 'piano', 'cor_vas_x0', '-(cor_fronte_semi - 0.5 mm)', 'cor_vas_x1', 'cor_fronte_semi - 0.5 mm',
             'cor_vas_sp', 1, NUOVO)
    for nome, x, y in _vassoio_fori():
        p.cilindro('z', 'cor_vas_z', nome.replace('vas_bugna', 'foro'), x, y, 'vite_m3_pass', 'cor_vas_sp', 1, TAGLIA)
    # colonnine della basetta con inserti M2 (viti M2 x 5 dall'alto)
    for nome, x, y in _basetta_fori():
        p.cilindro('z', 'cor_vas_z + cor_vas_sp', nome, x, y, 'cor_bas_col_d', 'cor_bas_luce')
        p.cilindro('z', 'cor_vas_z + cor_vas_sp + cor_bas_luce', nome + '_ins', x, y, 'ins_m2_d', 'ins_m2_l', -1, TAGLIA)
    # torretta della camera: piastra dietro la testa fino all'asse ottico (il flat esce dall'alto della testa e torna
    # indietro sopra la torretta e sopra il modulo dell'antenna) e mensola sotto la testa
    p.blocco('z', 'cor_vas_z + cor_vas_sp', 'torretta', 'cor_vas_x1', '-(6 mm)', 'cor_cam_x - 0.2 mm', '6 mm',
             'cor_cam_z - cor_vas_z - cor_vas_sp')
    p.blocco('z', 'cor_vas_z', 'mensola', 'cor_cam_x', '-(6 mm)', 'cor_cam_x + cam_alt', '6 mm',
             'cor_cam_z - cam_testa / 2 - cor_vas_z')
    p.blocco('z', 'cor_vas_z', 'piede_mensola', 'cor_vas_x1 - 1 mm', '-(6 mm)', 'cor_cam_x + cam_alt', '6 mm', 'cor_vas_sp')
    return occ, p


def _ottagono(p, q, nome, rientro, h, verso, op):
    """Apertura di servizio a ottagono (angoli a 45 gradi da car_serv_smusso), rientrata di `rientro` per lato."""
    x0, x1 = 'cor_serv_x0 + ' + rientro, 'cor_serv_x1 - ' + rientro
    ys, c = 'car_serv_semi - ' + rientro, 'car_serv_smusso'
    f = [p.blocco('z', q, nome + '_a', x0, '-(%s - %s)' % (ys, c), x1, '%s - %s' % (ys, c), h, verso, op)]
    op2 = UNISCI if op == NUOVO else op
    f.append(p.blocco('z', q, nome + '_b', '%s + %s' % (x0, c), '-(%s)' % ys, '%s - %s' % (x1, c), ys, h, verso, op2))
    for k, (xa, ya, xb, yb) in enumerate((((x1 + ' - ' + c), ys, x1, '%s - %s' % (ys, c)),
                                          (x1, '-(%s - %s)' % (ys, c), x1 + ' - ' + c, '-(%s)' % ys),
                                          ('%s + %s' % (x0, c), '-(%s)' % ys, x0, '-(%s - %s)' % (ys, c)),
                                          (x0, '%s - %s' % (ys, c), '%s + %s' % (x0, c), ys))):
        # triangolo d'angolo: rettangolo sul lato a 45 gradi verso l'interno (i lati vanno in senso antiorario e
        # b = a ruotato di +90 gradi punta fuori, quindi b < 0)
        f.append(p.blocco_obl('z', q, '%s_angolo_%d' % (nome, k), (xa, ya), (xb, yb), '0 mm', '%s * sqrt(2)' % c,
                              '-(%s * sqrt(2) / 2)' % c, '0 mm', h, verso, op2))
    return f


def fai_sportellino(corpo):
    """Sportellino di servizio (PETG nero): lastra a filo nell'apertura a ottagono, appoggiata sulla battuta, con
    nervature di schiacciamento sui lati lunghi (a filo dell'apertura nel modello: la stretta la da' la stampa, D-056)."""
    occ = _nuovo_comp(corpo, 'Corpo_Sportello_Servizio')
    p = Parte(occ.component)
    _ottagono(p, 'car_top - car_sp', 'piastra', '0.2 mm', 'car_sp', 1, NUOVO)
    for nome, x in (('a', '16 mm'), ('p', '-(8 mm)')):
        for lato, y0, y1 in (('s', 'car_serv_semi - 0.2 mm', 'car_serv_semi'), ('d', '-(car_serv_semi)', '-(car_serv_semi - 0.2 mm)')):
            p.blocco('z', 'car_top - car_sp', 'nervatura_%s%s' % (nome, lato), x + ' - 0.5 mm', y0, x + ' + 0.5 mm', y1, 'car_sp')
    return occ, p


# ----------------------------------------------------------------------------------- carapace (D-060, D-061)
def _collezione(oggetti):
    c = adsk.core.ObjectCollection.create()
    for o in oggetti:
        c.add(o)
    return c


def _spigoli_z(corpo, punti, tol=0.05):
    """Spigoli rettilinei paralleli a Z che passano (in X, Y, mm) per i punti: [(x, y, chiave)] -> {chiave: [spigoli]}."""
    out = {}
    for e in corpo.edges:
        if e.geometry.curveType != adsk.core.Curve3DTypes.Line3DCurveType:
            continue
        a, b = e.startVertex.geometry, e.endVertex.geometry
        if abs(a.x - b.x) > 1e-5 or abs(a.y - b.y) > 1e-5:
            continue
        for x, y, k in punti:
            if abs(a.x * 10 - x) < tol and abs(a.y * 10 - y) < tol:
                out.setdefault(k, []).append(e)
    return out


def _raccorda(p, gruppi, nome):
    fil = p.c.features.filletFeatures
    inp = fil.createInput()
    for r, spigoli in gruppi:
        if spigoli:
            inp.edgeSetInputs.addConstantRadiusEdgeSet(_collezione(spigoli), adsk.core.ValueInput.createByString(r), False)
    f = fil.add(inp)
    f.name = nome
    p.n += 1
    return f


def _smussa(p, spigoli, dist_expr, nome, catena=True):
    ch = p.c.features.chamferFeatures
    ci = ch.createInput2()
    ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(_collezione(spigoli), adsk.core.ValueInput.createByString(dist_expr), catena)
    f = ch.add(ci)
    f.name = nome
    p.n += 1
    return f


def _lobo(p, nome, cx, cy):
    """Lobo esagonale (vertici a 0, 60, ... gradi) come unione di tre rettangoli, da cor_cop_z a car_top."""
    h = 'car_top - cor_cop_z'
    f = [p.blocco('z', 'cor_cop_z', nome + '_0', cx + ' - car_lobo_R / 2', cy + ' - car_lobo_a', cx + ' + car_lobo_R / 2',
                  cy + ' + car_lobo_a', h)]
    for ang in (60, 120):
        f.append(p.blocco_obl('z', 'cor_cop_z', '%s_%d' % (nome, ang), (cx, cy),
                              ('%s + 10 mm * cos(%d deg)' % (cx, ang), '%s + 10 mm * sin(%d deg)' % (cy, ang)),
                              '-(car_lobo_R / 2)', 'car_lobo_R / 2', '-(car_lobo_a)', 'car_lobo_a', h))
    return f


def _vertici_pianta(p):
    """Vertici del contorno del carapace in pianta (meta' sinistra e specchio): (x, y, 'v' convesso | 'c' concavo)."""
    v = p.val
    R, a = v('car_lobo_R'), v('car_lobo_a')
    ax, ay, my, vy, vx, cx = v('cor_ang_x'), v('cor_ang_y'), v('cor_med_y'), v('car_valle_y'), v('car_viso_x'), v('car_coda_x')
    pts = []
    # viso: la linea x = viso incontra il lato basso-anteriore del lobo AS (da (ax + R, ay) a (ax + R/2, ay - a))
    t = (ax + R - vx) / (R / 2)
    pts.append((vx, ay - t * a, 'c'))
    pts += [(ax + R, ay, 'v'), (ax + R / 2, ay + a, 'v'), (ax - R / 2, ay + a, 'v')]
    # valle tra AS e MS: lato basso-posteriore del lobo AS e lato basso-anteriore del lobo MS incontrano y = valle
    t = (ay + a - vy) / a            # dal vertice (ax - R/2, ay + a) verso (ax - R, ay)
    pts.append((ax - R / 2 - t * R / 2, vy, 'c'))
    t = (my + a - vy) / a
    pts.append((R / 2 + t * R / 2, vy, 'c'))
    pts += [(R / 2, my + a, 'v'), (-R / 2, my + a, 'v')]
    pts.append((-(R / 2 + t * R / 2), vy, 'c'))
    t = (ay + a - vy) / a
    pts.append((-(ax - R / 2 - t * R / 2), vy, 'c'))
    pts += [(-(ax - R / 2), ay + a, 'v'), (-(ax + R / 2), ay + a, 'v'), (-(ax + R), ay, 'v')]
    # coda: la linea x = -coda incontra il lato basso-posteriore del lobo PS
    t = (ax + R - cx) / (R / 2)
    pts.append((-cx, ay - t * a, 'c'))
    return pts + [(x, -y, k) for x, y, k in pts]


def fai_carapace(corpo):
    """Carapace bianco (PETG): testa rastremata, pieno da nucleo, baie e sei lobi, raccordi in pianta, smusso 6 x 45,
    svuotamento 1,6. I dettagli (unioni e tagli) sono in fai_carapace_dettagli."""
    occ = _nuovo_comp(corpo, 'Corpo_Carapace')
    p = Parte(occ.component)
    info = {}
    # A. testa piena con i fianchi rastremati a 60 gradi (prima del carapace, cosi' i tagli non toccano i lobi)
    p.blocco('z', 'car_mento_z', 'testa', 'car_testa_x0', '-(car_testa_semi)', 'car_viso_x', 'car_testa_semi', 'cor_cop_z - car_mento_z', 1, NUOVO)
    r = p.blocco_obl('x', 'car_testa_x0 - 1 mm', 'rastremazione_s', ('car_mento_semi', 'car_mento_z'),
                     ('car_mento_semi + 10 mm * cos(car_rastr)', 'car_mento_z + 10 mm * sin(car_rastr)'), '-(5 mm)', '50 mm', '-(30 mm)', '0 mm',
                     'car_viso_x - car_testa_x0 + 2 mm', 1, TAGLIA)
    p.specchia([r], 'y', 'rastremazione_d')
    # B. pieno del carapace
    h = 'car_top - cor_cop_z'
    p.blocco('z', 'cor_cop_z', 'nucleo', '-(car_coda_x)', '-(car_testa_y)', 'car_viso_x', 'car_testa_y', h)
    p.blocco('z', 'cor_cop_z', 'baie', '-(cor_ang_x)', '-(car_valle_y)', 'cor_ang_x', 'car_valle_y', h)
    las = _lobo(p, 'lobo_as', 'cor_ang_x', 'cor_ang_y')
    lms = _lobo(p, 'lobo_ms', '0 mm', 'cor_med_y')
    lps = p.specchia(las, 'x', 'lobi_ps')
    p.specchia(las + lms + [lps], 'y', 'lobi_destri')
    corpo_b = occ.component.bRepBodies.item(0)
    zt = p.val('car_top')
    cima = [fa for fa in corpo_b.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType and abs(fa.pointOnFace.z * 10 - zt) < 0.01]
    info['area_cima_mm2'] = round(sum(fa.area for fa in cima) * 100, 1)
    # C. raccordi in pianta sui vertici del contorno (R12 convessi, R10 concavi)
    vert = _vertici_pianta(p)
    sp = _spigoli_z(corpo_b, vert)
    info['spigoli_pianta'] = {k: len(v_) for k, v_ in sp.items()}
    _raccorda(p, [('car_r_conv', sp.get('v', [])), ('car_r_conc', sp.get('c', []))], 'raccordi_pianta')
    # D. smusso del contorno superiore e svuotamento
    corpo_b = occ.component.bRepBodies.item(0)
    cima = [fa for fa in corpo_b.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType and abs(fa.pointOnFace.z * 10 - zt) < 0.01][0]
    _smussa(p, [e for e in cima.edges], 'car_smusso', 'smusso')
    corpo_b = occ.component.bRepBodies.item(0)
    cima = [fa for fa in corpo_b.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType and abs(fa.pointOnFace.z * 10 - zt) < 0.01]
    info['area_piano_mm2'] = round(sum(fa.area for fa in cima) * 100, 1)
    zc, zm, xt = p.val('cor_cop_z'), p.val('car_mento_z'), p.val('car_testa_x0')
    sotto = []
    for fa in corpo_b.faces:
        if fa.geometry.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType:
            continue
        q = fa.pointOnFace
        ok, n = fa.evaluator.getNormalAtPoint(q)
        if (abs(q.z * 10 - zc) < 0.01 and n.z < -0.9) or (abs(q.z * 10 - zm) < 0.01 and n.z < -0.9) or (abs(q.x * 10 - xt) < 0.01 and n.x < -0.9):
            sotto.append(fa)
    info['facce_aperte'] = len(sotto)
    p.svuota(sotto, 'car_sp', 'guscio')
    info['volume_cm3'] = round(sum(b.volume for b in occ.component.bRepBodies), 2)
    info['corpi'] = occ.component.bRepBodies.count
    p.info = info
    return occ, p


def _sedi_fascia(p, op, b_viso, b_coda, h_bordo_viso, h_bordo_coda):
    """Fascia nera sulla schiena, sullo smusso e sul bordo del viso e della coda: sedi nel carapace (TAGLIA) o pezzi
    della fascia (NUOVO/UNISCI) con le stesse espressioni."""
    op1 = op
    op2 = UNISCI if op == NUOVO else op
    f = [p.blocco('z', 'car_top - car_fascia_h', 'fascia_piano', '-(car_coda_x - car_smusso)', '-(car_fascia_semi)',
                  'car_viso_x - car_smusso', 'car_fascia_semi', 'car_fascia_h', 1, op1)]
    f.append(p.blocco_obl('y', '-(car_fascia_semi)', 'fascia_smusso_viso', ('car_viso_x', 'car_top - car_smusso'),
                          ('car_viso_x - car_smusso', 'car_top'), b_viso[0], b_viso[1], b_viso[2], b_viso[3], '2 * car_fascia_semi', 1, op2))
    f.append(p.blocco('x', 'car_viso_x - car_sp', 'fascia_bordo_viso', '-(car_fascia_semi)', 'cor_cop_z', 'car_fascia_semi',
                      'car_top - car_smusso', h_bordo_viso, 1, op2))
    f.append(p.blocco_obl('y', '-(car_fascia_semi)', 'fascia_smusso_coda', ('-(car_coda_x)', 'car_top - car_smusso'),
                          ('-(car_coda_x - car_smusso)', 'car_top'), b_coda[0], b_coda[1], b_coda[2], b_coda[3], '2 * car_fascia_semi', 1, op2))
    f.append(p.blocco('x', '-(car_coda_x)', 'fascia_bordo_coda', '-(car_fascia_semi)', 'cor_cop_z', 'car_fascia_semi',
                      'car_top - car_smusso', h_bordo_coda, 1, op2))
    return f


def _fori_dorso(p):
    """Fori del dorso che attraversano carapace e fascia: ottagono di servizio, pulsante, finestra del display, tacca."""
    _ottagono(p, 'car_top - car_sp', 'apertura', '0 mm', 'car_sp', 1, TAGLIA)
    p.cilindro('z', 'car_top - car_sp', 'foro_pulsante', 'car_puls_x', '0 mm', 'car_puls_d', 'car_sp', 1, TAGLIA)
    p.blocco('z', 'car_top - car_sp', 'finestra_cicalino', '(cic_x0 + cic_x1) / 2 - car_fin_l / 2', '-(car_fin_semi)',
             '(cic_x0 + cic_x1) / 2 + car_fin_l / 2', 'car_fin_semi', 'car_sp', 1, TAGLIA)
    p.blocco('z', 'car_top', 'tacca', 'cor_serv_x1 + 1 mm', '-(5 mm)', 'cor_serv_x1 + 4 mm', '5 mm', '0.8 mm', -1, TAGLIA)


def _occhio(p):
    """Occhio della camera: tronco di piramide sul campo di 120 gradi piu' il margine, tagliato con un loft fra le due
    bocche prolungate di 0,5 mm oltre le facce (le quattro estrusioni piane della specifica tagliavano anche fuori dal
    tronco: un prisma estruso non si ferma agli spigoli delle pareti vicine)."""
    k = '0.5 mm / (car_viso_x - car_occhio_x0)'
    s_in, v_in = 'car_occhio_si - (car_occhio_se - car_occhio_si) * ' + k, 'car_occhio_vi - (car_occhio_ve - car_occhio_vi) * ' + k
    s_ex, v_ex = 'car_occhio_se + (car_occhio_se - car_occhio_si) * ' + k, 'car_occhio_ve + (car_occhio_ve - car_occhio_vi) * ' + k
    a = p.sk_rett('x', 'car_occhio_x0 - 0.5 mm', 'occhio_bocca_interna', '-(%s)' % s_in, 'cor_cam_z - (%s)' % v_in, s_in,
                  'cor_cam_z + %s' % v_in)
    b = p.sk_rett('x', 'car_viso_x + 0.5 mm', 'occhio_bocca_esterna', '-(%s)' % s_ex, 'cor_cam_z - (%s)' % v_ex, s_ex,
                  'cor_cam_z + %s' % v_ex)
    lo = p.c.features.loftFeatures
    li = lo.createInput(adsk.fusion.FeatureOperations.CutFeatureOperation)
    li.loftSections.add(a.profiles.item(0))
    li.loftSections.add(b.profiles.item(0))
    li.isSolid = True
    li.participantBodies = list(p.c.bRepBodies)
    f = lo.add(li)
    f.name = 'occhio'
    p.n += 1
    return f


def fai_carapace_dettagli(corpo):
    """Unioni e tagli del carapace (seconda chiamata): gonne alte, paratie, guance di coda, pozzetti, collare del
    cicalino, battuta dello sportellino; sedi di fascia e visiera, apertura, feritoie, pozzetti, fori."""
    occ = L['trova_occ'](corpo.component, 'Corpo_Carapace')[0]
    T0['Corpo_Carapace_dettagli'] = corpo.component.parentDesign.timeline.count
    p = Parte(occ.component)
    p.gruppo = 'Corpo_Carapace_dettagli'
    # E. unioni
    g = [p.blocco('z', 'cor_cop_z', 'gonna_alta_as', 'cor_gonna_x0', 'cor_baia_y - cor_gonna_sp', 'cor_gonna_x1', 'cor_baia_y',
                  'car_top - car_sp - cor_cop_z')]
    g.append(p.specchia(g, 'x', 'gonna_alta_ps'))
    p.specchia(g, 'y', 'gonne_alte_destre')
    pa = p.blocco('z', 'cor_orlo', 'paratia_s', 'cor_tun_x1', 'car_paratia_y0', 'car_testa_x0', 'car_paratia_y1', 'car_top - car_sp - cor_orlo')
    p.specchia([pa], 'y', 'paratia_d')
    # sopra l'attacco dello smusso la guancia rientra dietro la linea della coda: a filo del lobo bucava lo smusso
    gu = [p.blocco('z', '-(car_guancia_giu)', 'guancia_s', '-(car_guancia_x0)', 'car_guancia_y0', '-(car_guancia_x1)', 'car_guancia_y1',
                   'car_top - car_smusso + car_guancia_giu'),
          p.blocco('z', 'car_top - car_smusso', 'guancia_alta_s', '-(car_coda_x) + 1 mm', 'car_guancia_y0', '-(car_guancia_x1)',
                   'car_guancia_y1', 'car_smusso - car_sp')]
    p.specchia(gu, 'y', 'guance_d')
    tubi = [p.cilindro('z', 'cor_cop_z', 'pozzo_tubo_a', 'cor_col_xa', 'cor_col_y', 'car_pozzo_D', 'car_top - car_sp - cor_cop_z'),
            p.cilindro('z', 'cor_cop_z', 'pozzo_tubo_p', '-(cor_col_xp)', 'cor_col_y', 'car_pozzo_D', 'car_top - car_sp - cor_cop_z')]
    p.specchia(tubi, 'y', 'pozzi_tubi_destri')
    hc = 'car_top - car_sp - cic_z0 - 8 mm'
    cs = p.blocco('z', 'cic_z0 + 8 mm', 'collare_s', 'cic_x0 - 0.2 mm', 'cic_semi + 0.2 mm', 'cic_x1 + 0.2 mm', 'cic_semi + 1.4 mm', hc)
    p.specchia([cs], 'y', 'collare_d')
    p.blocco('z', 'cic_z0 + 8 mm', 'collare_fronte', 'cic_x1 + 0.2 mm', '-(14 mm)', 'cic_x1 + 1.4 mm', '14 mm', hc)
    for x in ('-(80 mm)', '-(68 mm)'):
        # a filo del cicalino nel modello, come le nervature dello sportellino (D-056): la stretta la da' la stampa
        for lato, y0, y1 in (('s', 'cic_semi', 'cic_semi + 0.2 mm'), ('d', '-(cic_semi + 0.2 mm)', '-(cic_semi)')):
            p.blocco('z', 'cic_z0 + 8 mm', 'collare_nervatura_%s%s' % (lato, x[3:5]), x + ' - 0.5 mm', y0, x + ' + 0.5 mm', y1, hc)
    p.blocco('z', 'car_top - 2 * car_sp', 'battuta', 'cor_serv_x0 - 1 mm', '-(car_serv_semi + 1 mm)', 'cor_serv_x1 + 1 mm',
             'car_serv_semi + 1 mm', 'car_sp')
    p.blocco('z', 'car_top - 2 * car_sp', 'battuta_vuoto', 'cor_serv_x0 + car_battuta', '-(car_serv_semi - car_battuta)',
             'cor_serv_x1 - car_battuta', 'car_serv_semi - car_battuta', 'car_sp', 1, TAGLIA)
    # F. tagli: sedi della fascia (intarsio da 0,6 sul piano e sugli smussi, a piena parete sui bordi di viso e coda)
    _sedi_fascia(p, TAGLIA, ('-(0.6 mm)', 'car_smusso * sqrt(2) + 0.6 mm', '-(1 mm)', 'car_fascia_h'),
                 ('-(0.6 mm)', 'car_smusso * sqrt(2) + 0.6 mm', '-(car_fascia_h)', '1 mm'), 'car_sp + 0.1 mm', 'car_fascia_h')
    p.blocco('x', 'car_viso_x - car_sp', 'sede_visiera', '-(car_testa_semi + 1 mm)', 'car_mento_z - 1 mm', 'car_testa_semi + 1 mm',
             'cor_cop_z', 'car_sp + 0.1 mm', 1, TAGLIA)
    _fori_dorso(p)
    for lato, ys in (('s', 1), ('d', -1)):
        y0, y1 = ('cor_fer_y - cor_fer_w / 2', 'cor_fer_y + cor_fer_w / 2') if ys > 0 else ('-(cor_fer_y + cor_fer_w / 2)', '-(cor_fer_y - cor_fer_w / 2)')
        for i in range(N_FER):
            x = _x_feritoia(i)
            p.blocco('z', 'car_top - car_sp', 'feritoia_%s%d' % (lato, i), x, y0, x + ' + cor_fer_l', y1, 'car_sp', 1, TAGLIA)
    for nome, x, y in (('as', 'cor_col_xa', 'cor_col_y'), ('ps', '-(cor_col_xp)', 'cor_col_y'),
                       ('ad', 'cor_col_xa', '-(cor_col_y)'), ('pd', '-(cor_col_xp)', '-(cor_col_y)')):
        p.cilindro('z', 'cor_cop_z + cor_cop_sp', 'pozzo_vano_' + nome, x, y, 'car_pozzo_d', 'car_top - cor_cop_z - cor_cop_sp', 1, TAGLIA)
        p.cilindro('z', 'cor_cop_z', 'pozzo_foro_' + nome, x, y, 'vite_m3_pass', 'cor_cop_sp', 1, TAGLIA)
    p.info = {'corpi': occ.component.bRepBodies.count, 'volume_cm3': round(sum(b.volume for b in occ.component.bRepBodies), 2)}
    return occ, p


def fai_fascia(corpo):
    """Fascia nera (PETG non caricato) a filo nelle sedi del carapace, con i fori del dorso e l'occhio."""
    occ = _nuovo_comp(corpo, 'Corpo_Fascia')
    p = Parte(occ.component)
    _sedi_fascia(p, NUOVO, ('0 mm', 'car_smusso * sqrt(2)', '0 mm', 'car_fascia_h'), ('0 mm', 'car_smusso * sqrt(2)', '-(car_fascia_h)', '0 mm'),
                 'car_sp', 'car_fascia_h')
    _fori_dorso(p)
    _occhio(p)
    p.info = {'corpi': occ.component.bRepBodies.count, 'volume_cm3': round(sum(b.volume for b in occ.component.bRepBodies), 2)}
    return occ, p


def fai_visiera(corpo):
    """Visiera nera: parete del viso sotto il carapace, fianchi rastremati come la testa, bugna e occhio della camera."""
    occ = _nuovo_comp(corpo, 'Corpo_Visiera')
    p = Parte(occ.component)
    p.blocco('x', 'car_viso_x - car_sp', 'visiera', '-(car_testa_semi)', 'car_mento_z', 'car_testa_semi', 'cor_cop_z', 'car_sp', 1, NUOVO)
    r = p.blocco_obl('x', 'car_viso_x - car_sp - 1 mm', 'rastremazione_s', ('car_mento_semi', 'car_mento_z'),
                     ('car_mento_semi + 10 mm * cos(car_rastr)', 'car_mento_z + 10 mm * sin(car_rastr)'), '-(5 mm)', '50 mm', '-(30 mm)', '0 mm',
                     'car_sp + 2 mm', 1, TAGLIA)
    p.specchia([r], 'y', 'rastremazione_d')
    p.blocco('x', 'car_occhio_x0', 'bugna_occhio', '-(car_bugna_semi)', 'car_bugna_z0', 'car_bugna_semi', 'cor_cop_z',
             'car_viso_x - car_sp - car_occhio_x0')
    _occhio(p)
    p.info = {'corpi': occ.component.bRepBodies.count, 'volume_cm3': round(sum(b.volume for b in occ.component.bRepBodies), 2)}
    return occ, p


def fai_gonne(corpo):
    """Gonne nere sulle pareti delle baie, da z 7 al carapace: quattro corpi."""
    occ = _nuovo_comp(corpo, 'Corpo_Gonne')
    p = Parte(occ.component)
    for verso, x0, x1 in (('a', 'cor_gonna_x0', 'cor_gonna_x1'), ('p', '-(cor_gonna_x1)', '-(cor_gonna_x0)')):
        for lato, y0, y1 in (('s', 'cor_baia_y - cor_gonna_sp', 'cor_baia_y'), ('d', '-(cor_baia_y)', '-(cor_baia_y - cor_gonna_sp)')):
            p.blocco('z', 'cor_orlo', 'gonna_%s%s' % (verso, lato), x0, y0, x1, y1, 'cor_cop_z - cor_orlo', 1, NUOVO)
    p.info = {'corpi': occ.component.bRepBodies.count, 'volume_cm3': round(sum(b.volume for b in occ.component.bRepBodies), 2)}
    return occ, p


def togli_coperchio(corpo):
    """Cancella il coperchio di D-052...D-057, sostituito da carapace, fascia, visiera e gonne."""
    tolti = []
    while L['trova_occ'](corpo.component, 'Corpo_Coperchio'):
        L['trova_occ'](corpo.component, 'Corpo_Coperchio')[0].deleteMe()
        tolti.append('Corpo_Coperchio')
    return tolti


def fai_coperchio(corpo):
    occ = _nuovo_comp(corpo, 'Corpo_Coperchio')
    p = Parte(occ.component)
    p.blocco('z', 'cor_cop_z', 'dorso_nucleo', '-(cor_tun_x0)', '-(cor_tun_semi)', 'cor_tun_x1', 'cor_tun_semi', 'cor_cop_sp', 1, NUOVO)
    p.blocco('z', 'cor_cop_z', 'dorso_baie', '-(cor_baia_x)', '-(cor_baia_y)', 'cor_baia_x', 'cor_baia_y', 'cor_cop_sp')
    p.blocco('z', 'cor_cop_z', 'muso', 'cor_tun_x1', '-(cor_muso_semi)', 'cor_muso_x', 'cor_muso_semi', 'cor_cop_sp')
    for lato, y0, y1 in (('s', 'cor_baia_y - cor_gonna_sp', 'cor_baia_y'), ('d', '-(cor_baia_y)', '-(cor_baia_y - cor_gonna_sp)')):
        for verso, x0, x1 in (('a', 'cor_gonna_x0', 'cor_gonna_x1'), ('p', '-(cor_gonna_x1)', '-(cor_gonna_x0)')):
            p.blocco('z', 'cor_orlo', 'gonna_%s%s' % (verso, lato), x0, y0, x1, y1, 'cor_cop_z - cor_orlo')
    p.blocco('z', 'cor_cop_z', 'apertura_servizio', 'cor_serv_x0', '-(cor_serv_semi)', 'cor_serv_x1', 'cor_serv_semi', 'cor_cop_sp',
             1, TAGLIA)
    for nome, x, y in (('lobo_as', 'cor_ang_x', 'cor_ang_y'), ('lobo_ad', 'cor_ang_x', '-(cor_ang_y)'),
                       ('lobo_ps', '-(cor_ang_x)', 'cor_ang_y'), ('lobo_pd', '-(cor_ang_x)', '-(cor_ang_y)'),
                       ('lobo_ms', '0 mm', 'cor_med_y'), ('lobo_md', '0 mm', '-(cor_med_y)')):
        p.cilindro('z', 'cor_cop_z', nome, x, y, '2 * cor_cop_lobo', 'cor_cop_sp')
    # muso: fascia davanti e ai lati di vassoio, torretta e camera, con la finestra della camera (in PETG come il coperchio)
    p.blocco('x', 'cor_muso_x', 'muso_fronte', '-(cor_muso_semi)', 'cor_muso_giu', 'cor_muso_semi', 'cor_cop_z', 'cor_cop_sp', -1)
    p.blocco('y', 'cor_muso_semi', 'muso_fianco_s', 'cor_tun_x1', 'cor_muso_giu', 'cor_muso_x', 'cor_cop_z', 'cor_cop_sp', -1)
    p.blocco('y', '-(cor_muso_semi)', 'muso_fianco_d', 'cor_tun_x1', 'cor_muso_giu', 'cor_muso_x', 'cor_cop_z', 'cor_cop_sp', 1)
    p.cilindro('x', 'cor_muso_x', 'finestra_camera', '0 mm', 'cor_cam_z', 'cor_muso_finestra_d', 'cor_cop_sp', -1, TAGLIA)
    # tacca per l'unghia sotto il bordo anteriore dello sportellino di servizio
    p.blocco('z', 'cor_cop_z + cor_cop_sp', 'tacca_sportellino', 'cor_serv_x1 + 1 mm', '-(5 mm)', 'cor_serv_x1 + 4 mm', '5 mm', '0.8 mm', -1,
             TAGLIA)
    # fori delle viti delle colonnine e feritoie sopra i regolatori (dopo i lobi, che altrimenti li richiuderebbero)
    for nome, x, y in (('foro_as', 'cor_col_xa', 'cor_col_y'), ('foro_ps', '-(cor_col_xp)', 'cor_col_y'),
                       ('foro_ad', 'cor_col_xa', '-(cor_col_y)'), ('foro_pd', '-(cor_col_xp)', '-(cor_col_y)')):
        p.cilindro('z', 'cor_cop_z', nome, x, y, 'vite_m3_pass', 'cor_cop_sp', 1, TAGLIA)
    for lato, y0, y1 in (('s', 'cor_fer_y - cor_fer_w / 2', 'cor_fer_y + cor_fer_w / 2'),
                         ('d', '-(cor_fer_y + cor_fer_w / 2)', '-(cor_fer_y - cor_fer_w / 2)')):
        for i in range(N_FER):
            x = _x_feritoia(i)
            p.blocco('z', 'cor_cop_z', 'feritoia_%s%d' % (lato, i), x, y0, x + ' + cor_fer_l', y1, 'cor_cop_sp', 1, TAGLIA)
    return occ, p


def stato(des, root):
    out = {}
    c = L['trova_occ'](root, 'Corpo')
    if not c:
        return 'Corpo assente'
    for o in c[0].childOccurrences:
        comp = o.component
        if not comp.name.startswith('Corpo_'):
            continue
        bb = None
        for b in comp.bRepBodies:
            if bb is None:
                bb = b.boundingBox.copy()
            else:
                bb.combine(b.boundingBox)
        riga = {'corpi': comp.bRepBodies.count, 'volume_cm3': round(sum(b.volume for b in comp.bRepBodies), 2)}
        if bb is not None:
            riga['ingombro'] = [round(v * 10, 2) for v in (bb.minPoint.x, bb.minPoint.y, bb.minPoint.z,
                                                           bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z)]
        nv = [s.name for s in comp.sketches if not s.isFullyConstrained]
        if nv:
            riga['schizzi_non_vincolati'] = nv
        out[comp.name] = riga
    tl = des.timeline
    out['_timeline_problemi'] = [(tl.item(i).name, tl.item(i).errorOrWarningMessage) for i in range(tl.count)
                                 if not tl.item(i).isGroup and tl.item(i).healthState !=
                                 adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
    return out


def main(passi, **kw):
    out = {'passi': passi}
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        if not app.activeDocument.name.startswith('Hexapod v2 - MG996R'):
            raise RuntimeError('documento attivo "%s": attivare Hexapod v2 - MG996R' % app.activeDocument.name)
        root = des.rootComponent
        if 'parametri' in passi:
            out['parametri'] = L['aggiungi_parametri'](des, PARAMETRI)
        corpo = _corpo(root)
        if 'togli_coperchio' in passi:
            out['togli_coperchio'] = togli_coperchio(corpo)
        for nome, f in (('base', fai_base), ('chiglia', fai_chiglia), ('sportello', fai_sportello), ('vassoio', fai_vassoio),
                        ('slitta', fai_slitta), ('coperchio', fai_coperchio), ('sportellino', fai_sportellino),
                        ('carapace', fai_carapace), ('carapace_dettagli', fai_carapace_dettagli), ('fascia', fai_fascia),
                        ('visiera', fai_visiera), ('gonne', fai_gonne)):
            if nome in passi:
                occ, p = f(corpo)
                out[nome] = _chiudi(des, getattr(p, 'gruppo', occ.component.name), p)
                out[nome].update(getattr(p, 'info', {}))
        if 'stato' in passi:
            out['stato'] = stato(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
