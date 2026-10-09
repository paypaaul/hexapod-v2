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


def fai_sportellino(corpo):
    """Sportellino di servizio nel dorso del coperchio: piastra che sormonta l'apertura e cornice di centraggio."""
    occ = _nuovo_comp(corpo, 'Corpo_Sportello_Servizio')
    p = Parte(occ.component)
    p.blocco('z', 'cor_cop_z + cor_cop_sp', 'piastra', 'cor_serv_x0 - 2 mm', '-(cor_serv_semi + 2 mm)', 'cor_serv_x1 + 2 mm',
             'cor_serv_semi + 2 mm', 'cor_cop_sp', 1, NUOVO)
    p.blocco('z', 'cor_cop_z', 'cornice', 'cor_serv_x0 + 0.3 mm', '-(cor_serv_semi - 0.3 mm)', 'cor_serv_x1 - 0.3 mm',
             'cor_serv_semi - 0.3 mm', 'cor_cop_sp')
    p.blocco('z', 'cor_cop_z', 'vuoto', 'cor_serv_x0 + 1.5 mm', '-(cor_serv_semi - 1.5 mm)', 'cor_serv_x1 - 1.5 mm',
             'cor_serv_semi - 1.5 mm', 'cor_cop_sp', 1, TAGLIA)
    return occ, p


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
        for nome, f in (('base', fai_base), ('chiglia', fai_chiglia), ('sportello', fai_sportello), ('vassoio', fai_vassoio),
                        ('slitta', fai_slitta), ('coperchio', fai_coperchio), ('sportellino', fai_sportellino)):
            if nome in passi:
                occ, p = f(corpo)
                out[nome] = _chiudi(des, occ.component.name, p)
        if 'stato' in passi:
            out['stato'] = stato(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
