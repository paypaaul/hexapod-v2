"""Zampa dell'esapode MG996R: parti progettate, istanze dei componenti comprati, giunti (fase 4, D-047, D-048).

Si esegue dentro Fusion sul design "Hexapod v2 - MG996R", un passo per chiamata:
    import runpy
    def run(_context: str):
        runpy.run_path('/Users/paul/hexapod-v2/cad/script/zampa.py')['main'](['parametri', 'coxa'])

Terna della zampa (componente "Zampa", all'origine della radice): origine sull'asse della coxa all'altezza
dell'asse del femore; X verso l'esterno, Y lungo l'asse del femore verso la piastra delle squadrette, Z in alto.
Posa di riferimento: femore orizzontale (alpha = 0), tibia verticale (gamma = 90).
Tutte le parti hanno la terna della zampa (trasformata identita'): le quote sono espressioni con zam_Lc,
zam_Lf, zam_Lt, quindi la zampa si riadatta cambiando i parametri e rigenerando le parti.

Servo del femore e del ginocchio: albero lungo +Y, coda verso -Z, alette sul piano Y = zy_orlo
(terna del servo -> zampa: x_s -> -Z, y_s -> -X, z_s -> +Y).
Le parti sono piene: alleggerimento e rigidezza li danno pareti e riempimento dello slicer
(la massa si calcola con il fattore di riempimento).
"""
import json
import math
import os
import runpy
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
L = runpy.run_path(os.path.join(QUI, 'lib_cad.py'))
A = runpy.run_path(os.path.join(QUI, 'lib_assieme.py'))
Parte, NUOVO, UNISCI, TAGLIA = L['Parte'], L['NUOVO'], L['UNISCI'], L['TAGLIA']

P3 = adsk.core.Point3D.create
V3 = adsk.core.Vector3D.create

PARAMETRI = [
    # --- lunghezze (D-047)
    ('zam_Lc', '55 mm', 'mm', 'Zampa: asse coxa -> asse femore'),
    ('zam_Lf', '65 mm', 'mm', 'Zampa: asse femore -> asse ginocchio'),
    ('zam_Lt', '110 mm', 'mm', 'Zampa: asse ginocchio -> punta del piede'),
    # --- culla dei servo di femore e ginocchio (terna del servo, quote dall'asse dell'albero)
    ('cul_parete', '2 mm', 'mm', 'Culla: parete'),
    ('cul_gio_fondo', '0.4 mm', 'mm', 'Culla: luce sotto il fondo del servo piu lungo (28,8)'),
    ('cul_fondo', '4.4 mm', 'mm', 'Culla: fondo (sede del cuscinetto 3,2 + 1,2)'),
    ('cul_bugna_h', '8 mm', 'mm', 'Culla: profondita delle bugne degli inserti sotto le alette'),
    ('cul_ins_parete', '1.6 mm', 'mm', 'Culla: parete attorno ai fori degli inserti'),
    ('ins_sposta_corto', '1.0 mm', 'mm', 'Inserti lato albero spostati lungo l asola dell aletta: distanza dalla gola del fermacavo'),
    ('ins_sposta_coda', '0.4 mm', 'mm', 'Inserti lato coda spostati lungo l asola: 1,6 mm di parete verso la sede'),
    ('ale_foro_corto', 'srv_fori_x / 2 - (srv_cassa_l / 2 - srv_asse_x)', 'mm', 'Servo: foro dell aletta lato albero, dall asse'),
    ('ale_foro_coda', 'srv_fori_x / 2 + (srv_cassa_l / 2 - srv_asse_x)', 'mm', 'Servo: foro dell aletta lato coda, dall asse'),
    ('cul_sede_corto', 'srv_asse_x + gio_servo', 'mm', 'Culla: sede dall asse verso il lato corto'),
    ('cul_sede_coda', 'srv_cassa_l - srv_asse_x + gio_servo', 'mm', 'Culla: sede dall asse verso la coda'),
    ('cul_sede_semi', 'srv_cassa_w / 2 + gio_servo', 'mm', 'Culla: semilarghezza della sede'),
    ('cul_corto', 'cul_sede_corto + cul_parete', 'mm', 'Culla: esterno lato corto'),
    ('cul_coda', 'cul_sede_coda + cul_parete', 'mm', 'Culla: esterno lato coda'),
    ('cul_semi', 'cul_sede_semi + cul_parete', 'mm', 'Culla: semilarghezza esterna'),
    ('ins_corto', 'ale_foro_corto + ins_sposta_corto', 'mm', 'Inserti lato albero: distanza dall asse'),
    ('ins_coda', 'ale_foro_coda + ins_sposta_coda', 'mm', 'Inserti lato coda: distanza dall asse'),
    ('ins_y', 'srv_fori_y / 2', 'mm', 'Inserti: semi-interasse di traverso'),
    ('bug_corto', 'ins_corto + ins_m3_d / 2 + cul_ins_parete', 'mm', 'Bugna lato albero: estremo'),
    ('bug_coda', 'ins_coda + ins_m3_d / 2 + cul_ins_parete', 'mm', 'Bugna lato coda: estremo'),
    ('bug_semi', 'ins_y + ins_m3_d / 2 + cul_ins_parete', 'mm', 'Bugne: semilarghezza'),
    ('cul_mozzo_d', '16 mm', 'mm', 'Culla: mozzo attorno al cuscinetto nel fondo alleggerito'),
    ('cul_fondo_min', '1.6 mm', 'mm', 'Culla: fondo nelle tasche di alleggerimento'),
    ('cul_fin_lato', '13 mm', 'mm', 'Culla: lato delle finestre a rombo nelle pareti (45 gradi, senza supporti)'),
    ('cul_fin_y', '-5 mm', 'mm', 'Culla: Y del centro delle finestre nelle pareti'),
    ('cul_fin_z1', '1 mm', 'mm', 'Culla: centro della finestra vicina all albero, sotto l asse (valore assoluto)'),
    ('cul_fin_z2', '20.5 mm', 'mm', 'Culla: centro della finestra verso la coda, sotto l asse (valore assoluto)'),
    # --- uscita del cavo (lato corto, vicino all'albero)
    ('cav_fin_w', '9 mm', 'mm', 'Finestra del cavo: larghezza (passa la spina JR 7,9 x 2,75)'),
    ('cav_fin_alto', '9 mm', 'mm', 'Finestra del cavo: bordo verso l orlo, sotto le alette'),
    ('cav_fin_basso', '26.1 mm', 'mm', 'Finestra del cavo: bordo verso il fondo, sotto le alette'),
    ('cav_gola_w', '7.6 mm', 'mm', 'Gola del fermacavo: larghezza (fermacavo 7)'),
    ('cav_gola_p', '0.8 mm', 'mm', 'Gola del fermacavo: profondita (sporgenza 1,0 meno il gioco 0,2)'),
    # --- giunto lato cuscinetto
    ('cus_rialzo_h', '0.4 mm', 'mm', 'Rialzo che tocca solo l anello interno del cuscinetto'),
    ('cus_rialzo_d', '6.2 mm', 'mm', 'Rialzo: diametro (diametro interno di riferimento LF-1050ZZ 6,40)'),
    ('cus_sede_d', 'cus_D', 'mm', 'Sede del cuscinetto: diametro nominale (forzamento da provino)'),
    ('cus_sede_prof', 'cus_B - cus_flangia_sp', 'mm', 'Sede del cuscinetto: profondita'),
    ('cus_passo_d', '6 mm', 'mm', 'Foro dietro il cuscinetto: passaggio del perno ed estrazione'),
    ('perno_foro', 'perno_d', 'mm', 'Foro del perno nella parte che lo porta: nominale (forzamento da provino)'),
    ('perno_sporge', '1.4 mm', 'mm', 'Perno: sporgenza esterna per estrarlo'),
    # --- femore
    ('fem_B_mozzo', '5.2 mm', 'mm', 'Femore B: spessore dei mozzi dei perni'),
    ('fem_piastra', '2.4 mm', 'mm', 'Femore: spessore delle piastre fuori dai mozzi'),
    ('fem_A_dietro', '3.2 mm', 'mm', 'Femore A: plastica dietro il disco della squadretta'),
    ('fem_testa_r', '13 mm', 'mm', 'Femore: raggio delle teste attorno ad anca e ginocchio'),
    ('fem_blocco_x0', '21.5 mm', 'mm', 'Blocco del femore: inizio dall asse dell anca'),
    ('fem_blocco_dk', '21 mm', 'mm', 'Blocco del femore: distanza minima dall asse del ginocchio'),
    ('fem_blocco_giu', '2 mm', 'mm', 'Blocco del femore: lato basso sotto l asse'),
    ('fem_blocco_su', '20 mm', 'mm', 'Blocco del femore: lato alto sopra l asse'),
    ('fem_smusso_bx', '9.5 mm', 'mm', 'Blocco: smusso basso verso il ginocchio, lungo X'),
    ('fem_smusso_bz', '5.5 mm', 'mm', 'Blocco: smusso basso verso il ginocchio, lungo Z'),
    ('fem_smusso_alto', '6 mm', 'mm', 'Blocco: smusso alto verso l anca'),
    ('fem_luce_A', '1.0 mm', 'mm', 'Registro tra blocco e piastra A: due rondelle M3 DIN 125 da 0,5'),
    ('fem_ins_dx', '4.5 mm', 'mm', 'Blocco: inserti M3 per la piastra A, distanza dai bordi'),
    ('sq_accesso_d', '6 mm', 'mm', 'Foro in asse per la vite centrale della squadretta'),
    # --- pila lungo Y nella terna della zampa (D-047): piano medio a meta' tra le facce esterne delle piastre
    ('zy_orlo', '(srv_sotto + cul_gio_fondo + cul_fondo + cus_flangia_sp + cus_rialzo_h + fem_B_mozzo'
                ' - (srv_albero_h - srv_spline_l + sq_h + fem_A_dietro)) / 2', 'mm', 'Y del piano delle alette = orlo delle culle'),
    ('zy_fondo_int', 'zy_orlo - srv_sotto - cul_gio_fondo', 'mm', 'Y della faccia interna del fondo delle culle'),
    ('zy_fondo_est', 'zy_fondo_int - cul_fondo', 'mm', 'Y della faccia esterna del fondo delle culle'),
    ('zy_B_int', 'zy_fondo_est - cus_flangia_sp - cus_rialzo_h', 'mm', 'Y della faccia interna dei mozzi di Femore_B'),
    ('zy_B_est', 'zy_B_int - fem_B_mozzo', 'mm', 'Y della faccia esterna di Femore_B'),
    ('zy_disco', 'zy_orlo + srv_albero_h - srv_spline_l + sq_h - sq_sp', 'mm', 'Y del lato inferiore del disco delle squadrette'),
    ('zy_A_est', 'zy_disco + sq_sp + fem_A_dietro', 'mm', 'Y della faccia esterna di Femore_A'),
    # --- coxa (D-048)
    ('cox_anima_sp', '4.4 mm', 'mm', 'Coxa: spessore dell anima'),
    ('cx_anima', 'zam_Lc - cul_sede_semi - cox_anima_sp', 'mm', 'Coxa: X della faccia interna dell anima (gondola raggio 39,32 + 0,8)'),
    ('cox_braccio_sp', '5.2 mm', 'mm', 'Coxa: spessore del braccio inferiore (perno forzato)'),
    ('cox_nerv_h', '5 mm', 'mm', 'Coxa: nervatura sotto il braccio, altezza alla radice'),
    ('cox_nerv_semi', '3 mm', 'mm', 'Coxa: nervatura, semilarghezza'),
    ('cox_nerv_x0', '10 mm', 'mm', 'Coxa: X dove la nervatura si annulla'),
    ('cz_braccio_su', 'bug_coda - cox_braccio_sp', 'mm', 'Coxa: faccia superiore del braccio inferiore, sotto l asse (valore assoluto)'),
    ('cox_tasca_lato', '18 mm', 'mm', 'Coxa: lato della tasca a rombo nell anima'),
    ('cox_tasca_y', '-7.35 mm', 'mm', 'Coxa: Y del centro della tasca nell anima'),
    ('cox_tasca_z', '14 mm', 'mm', 'Coxa: centro della tasca nell anima, sotto l asse (valore assoluto)'),
    ('cz_alette_coxa', 'srv_sotto + cul_gio_fondo + cul_fondo + cus_flangia_sp + cus_rialzo_h - cz_braccio_su', 'mm',
     'Z delle alette del servo di coxa (orlo della gondola)'),
    ('cox_gondola_luce', '1.2 mm', 'mm', 'Coxa: luce tra la testa dell anima e la cassa del servo di coxa'),
    ('cz_mensola', 'cz_alette_coxa + srv_sopra + cox_gondola_luce', 'mm', 'Coxa: Z del lato inferiore della testa dell anima sopra la gondola'),
    ('cx_testa', '36 mm', 'mm', 'Coxa: X dell estremo interno della testa dell anima'),
    ('cz_ponte_giu', 'cz_alette_coxa + srv_albero_h - srv_spline_l + sq_h - sq_sp', 'mm', 'Ponte: Z del lato inferiore del disco della squadretta di coxa'),
    ('cox_ponte_sopra', '3.95 mm', 'mm', 'Ponte: altezza sopra il disco (teste delle viti 3 + rondella 0,5)'),
    ('cz_ponte_su', 'cz_ponte_giu + sq_sp + cox_ponte_sopra', 'mm', 'Ponte: Z della faccia superiore'),
    ('cox_ponte_braccio', '3.9 mm', 'mm', 'Ponte: spessore del braccio'),
    ('cz_ponte_app', 'cz_ponte_su - cox_ponte_braccio', 'mm', 'Ponte: Z dell appoggio sulla testa dell anima'),
    ('cox_ponte_r', '12 mm', 'mm', 'Ponte: raggio del mozzo'),
    ('cox_disco_luce', '0.3 mm', 'mm', 'Ponte: luce sopra il disco (gioco verticale della coxa, D-048)'),
    ('cox_testa_vite_d', '5.7 mm', 'mm', 'Ponte: fori che calzano le teste delle viti M3 della squadretta'),
    ('cox_smusso_ponte', '3 mm', 'mm', 'Ponte: smusso dello spigolo esterno alto'),
    ('cx_ins_ponte', '(cx_testa + zam_Lc - cul_sede_semi) / 2', 'mm', 'Coxa: X degli inserti del ponte'),
    ('cox_ins_ponte_y', '5.5 mm', 'mm', 'Coxa: Y degli inserti del ponte'),
    ('cox_ling_l', '6 mm', 'mm', 'Ponte: linguetta di centraggio, lunghezza'),
    ('cox_ling_semi', '1.5 mm', 'mm', 'Ponte: linguetta, semilarghezza'),
    ('cox_ling_h', '1.6 mm', 'mm', 'Ponte: linguetta, altezza'),
    # --- tibia
    ('tib_stinco_semi', '6 mm', 'mm', 'Tibia: semilarghezza dello stinco nel piano della zampa'),
    ('tib_fin_semi', '3 mm', 'mm', 'Tibia: semilarghezza delle finestre dello stinco'),
    ('tib_fin_l', '15 mm', 'mm', 'Tibia: lunghezza delle finestre dello stinco'),
    ('tib_fin_passo', '21 mm', 'mm', 'Tibia: passo delle finestre dello stinco'),
    ('tib_fin_z0', '38 mm', 'mm', 'Tibia: inizio della prima finestra sotto l asse del ginocchio'),
    ('tib_piede_r', '6 mm', 'mm', 'Tibia: raggio del piede'),
]


# ----------------------------------------------------------------------------------- utilita'
T0 = {}


def _zampa(root):
    occ = L['trova_occ'](root, 'Zampa')
    if occ:
        return occ[0]
    o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = 'Zampa'
    return o


def _nuovo_comp(zampa, nome):
    """Crea il componente dentro la Zampa (cancellando quello con lo stesso nome), con la terna della zampa."""
    genitore = zampa.component
    for o in L['trova_occ'](genitore, nome):
        o.deleteMe()
    T0[nome] = genitore.parentDesign.timeline.count
    occ = genitore.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = nome
    return occ


def _chiudi(des, nome, p):
    L['raggruppa'](des, T0[nome], nome)
    return {'lavorazioni': p.n, 'schizzi_non_vincolati': p.non_vincolati}


def _culla(p, xc):
    """Culla di un servo con l'albero lungo +Y in (xc, z = 0), coda verso -Z. Ritorna le lavorazioni."""
    p.blocco('y', 'zy_fondo_est', 'culla', xc + ' - cul_semi', '-(cul_coda)', xc + ' + cul_semi', 'cul_corto',
             'zy_orlo - zy_fondo_est', 1, NUOVO if p.c.bRepBodies.count == 0 else UNISCI)
    p.blocco('y', 'zy_orlo - cul_bugna_h', 'bugna_corto', xc + ' - bug_semi', 'cul_corto', xc + ' + bug_semi', 'bug_corto',
             'cul_bugna_h')
    p.blocco('y', 'zy_orlo - cul_bugna_h', 'bugna_coda', xc + ' - bug_semi', '-(bug_coda)', xc + ' + bug_semi', '-(cul_coda)',
             'cul_bugna_h')


def _alleggerisci_culla(p, xc, lati):
    """Tasca nel fondo (attorno al mozzo del cuscinetto) e finestre a rombo nelle pareti laterali indicate (+1, -1)."""
    p.blocco('y', 'zy_fondo_est', 'tasca_fondo', xc + ' - cul_sede_semi', '-(cul_sede_coda)', xc + ' + cul_sede_semi',
             '-(cul_mozzo_d / 2)', 'cul_fondo - cul_fondo_min', 1, TAGLIA)
    for lato in lati:
        q = (xc + ' + cul_sede_semi - 0.5 mm') if lato > 0 else (xc + ' - cul_sede_semi + 0.5 mm')
        for i, zc in ((1, '-(cul_fin_z1)'), (2, '-(cul_fin_z2)')):
            p.blocco_obl('x', q, 'finestra_%s%d' % ('p' if lato > 0 else 'm', i), ('cul_fin_y', zc),
                         ('cul_fin_y + 1 mm', zc + ' + 1 mm'), '-(cul_fin_lato / 2)', 'cul_fin_lato / 2',
                         '-(cul_fin_lato / 2)', 'cul_fin_lato / 2', 'cul_parete + 1 mm', lato, TAGLIA)


def _sede(p, xc):
    """Lavorazioni della culla: sede del servo, cavo, cuscinetto, inserti delle alette."""
    p.blocco('y', 'zy_fondo_int', 'sede_servo', xc + ' - cul_sede_semi', '-(cul_sede_coda)', xc + ' + cul_sede_semi',
             'cul_sede_corto', 'zy_orlo - zy_fondo_int', 1, TAGLIA)
    p.blocco('y', 'zy_orlo - cav_fin_alto', 'gola_cavo', xc + ' - cav_gola_w / 2', 'cul_sede_corto - 0.5 mm',
             xc + ' + cav_gola_w / 2', 'cul_sede_corto + cav_gola_p', 'cav_fin_alto', 1, TAGLIA)
    p.blocco('y', 'zy_orlo - cav_fin_basso', 'finestra_cavo', xc + ' - cav_fin_w / 2', 'cul_sede_corto - 0.5 mm',
             xc + ' + cav_fin_w / 2', 'cul_corto + 0.5 mm', 'cav_fin_basso - cav_fin_alto', 1, TAGLIA)
    p.cilindro('y', 'zy_fondo_est', 'sede_cuscinetto', xc, '0 mm', 'cus_sede_d', 'cus_sede_prof', 1, TAGLIA)
    p.cilindro('y', 'zy_fondo_est', 'passaggio_perno', xc, '0 mm', 'cus_passo_d', 'cul_fondo', 1, TAGLIA)
    for nome, dx, z in (('ins_corto_a', ' - ins_y', 'ins_corto'), ('ins_corto_b', ' + ins_y', 'ins_corto'),
                        ('ins_coda_a', ' - ins_y', '-(ins_coda)'), ('ins_coda_b', ' + ins_y', '-(ins_coda)')):
        p.cilindro('y', 'zy_orlo', nome, xc + dx, z, 'ins_m3_d', 'ins_m3_l', -1, TAGLIA)


# ----------------------------------------------------------------------------------- parti
def fai_coxa(zampa):
    occ = _nuovo_comp(zampa, 'Coxa')
    p = Parte(occ.component)
    _culla(p, 'zam_Lc')
    # anima verso il corpo (faccia interna fuori dalla gondola) e testa sopra la gondola per il ponte
    p.blocco('y', 'zy_fondo_est', 'anima', 'cx_anima', '-(bug_coda)', 'zam_Lc - cul_semi', 'cul_corto',
             'zy_orlo - zy_fondo_est')
    p.blocco('z', 'cul_corto', 'testa_anima_bassa', 'cx_anima', '-(zy_orlo)', 'zam_Lc - bug_semi', 'zy_orlo',
             'cz_ponte_giu - cul_corto')
    p.blocco('z', 'cz_mensola', 'testa_anima_alta', 'cx_testa', '-(zy_orlo)', 'zam_Lc - cul_sede_semi', 'zy_orlo',
             'cz_ponte_app - cz_mensola')
    # braccio inferiore sotto la gondola, con il perno della coxa, e nervatura rastremata sotto
    p.blocco('z', '-(bug_coda)', 'braccio', '0 mm', '-(zy_orlo)', 'zam_Lc - cul_semi', 'zy_orlo', 'cox_braccio_sp')
    p.cilindro('z', '-(bug_coda)', 'braccio_testa', '0 mm', '0 mm', '2 * zy_orlo', 'cox_braccio_sp')
    p.blocco('y', '-(cox_nerv_semi)', 'nervatura', 'cox_nerv_x0', '-(bug_coda + cox_nerv_h)', 'cx_anima + cox_anima_sp / 2',
             '-(bug_coda)', '2 * cox_nerv_semi')
    p.blocco_obl('y', '-(cox_nerv_semi + 1 mm)', 'nervatura_rastremata', ('cx_anima', '-(bug_coda + cox_nerv_h)'),
                 ('cox_nerv_x0', '-(bug_coda)'), '-(6 mm)', 'sqrt((cx_anima - cox_nerv_x0) ^ 2 + cox_nerv_h ^ 2)',
                 '0 mm', '20 mm', '2 * cox_nerv_semi + 2 mm', 1, TAGLIA)
    p.cilindro('z', '-(cz_braccio_su)', 'rialzo', '0 mm', '0 mm', 'cus_rialzo_d', 'cus_rialzo_h')
    # lavorazioni
    _sede(p, 'zam_Lc')
    _alleggerisci_culla(p, 'zam_Lc', (1,))
    p.blocco_obl('x', 'cx_anima', 'tasca_anima', ('cox_tasca_y', '-(cox_tasca_z)'), ('cox_tasca_y + 1 mm', '1 mm - cox_tasca_z'),
                 '-(cox_tasca_lato / 2)', 'cox_tasca_lato / 2', '-(cox_tasca_lato / 2)', 'cox_tasca_lato / 2',
                 'cox_anima_sp - cul_parete', 1, TAGLIA)
    p.cilindro('z', '-(bug_coda)', 'foro_perno', '0 mm', '0 mm', 'perno_foro', 'cox_braccio_sp + cus_rialzo_h', 1, TAGLIA)
    for nome, y in (('ins_ponte_a', '-(cox_ins_ponte_y)'), ('ins_ponte_b', 'cox_ins_ponte_y')):
        p.cilindro('z', 'cz_ponte_app', nome, 'cx_ins_ponte', y, 'ins_m3_d', 'ins_m3_l - 0.7 mm', -1, TAGLIA)
    p.blocco('z', 'cz_ponte_app', 'sede_linguetta', 'cx_ins_ponte - cox_ling_l / 2 - gio_stampa', '-(cox_ling_semi + gio_stampa)',
             'cx_ins_ponte + cox_ling_l / 2 + gio_stampa', 'cox_ling_semi + gio_stampa', 'cox_ling_h + 0.4 mm', -1, TAGLIA)
    return occ, p


def fai_ponte(zampa):
    occ = _nuovo_comp(zampa, 'Coxa_Ponte')
    p = Parte(occ.component)
    p.cilindro('z', 'cz_ponte_giu', 'mozzo', '0 mm', '0 mm', '2 * cox_ponte_r', 'cz_ponte_su - cz_ponte_giu', 1, NUOVO)
    p.blocco('z', 'cz_ponte_app', 'braccio', '0 mm', '-(zy_orlo)', 'zam_Lc - cul_sede_semi', 'zy_orlo', 'cox_ponte_braccio')
    p.blocco('z', 'cz_ponte_app', 'linguetta', 'cx_ins_ponte - cox_ling_l / 2', '-(cox_ling_semi)', 'cx_ins_ponte + cox_ling_l / 2',
             'cox_ling_semi', 'cox_ling_h', -1)
    p.blocco_obl('y', '-(zy_orlo + 1 mm)', 'smusso', ('zam_Lc - cul_sede_semi - cox_smusso_ponte', 'cz_ponte_su'),
                 ('zam_Lc - cul_sede_semi', 'cz_ponte_su - cox_smusso_ponte'), '-(2 mm)', 'cox_smusso_ponte * 1.415 + 2 mm',
                 '0 mm', '10 mm', '2 * zy_orlo + 2 mm', 1, TAGLIA)
    p.cilindro('z', 'cz_ponte_giu', 'sede_disco', '0 mm', '0 mm', 'sq_d + 2 * gio_stampa', 'sq_sp + cox_disco_luce', 1, TAGLIA)
    p.cilindro('z', 'cz_ponte_giu', 'foro_centrale', '0 mm', '0 mm', 'sq_accesso_d', 'cz_ponte_su - cz_ponte_giu', 1, TAGLIA)
    for nome, y in (('foro_testa_a', '-(sq_fori_pcd / 2)'), ('foro_testa_b', 'sq_fori_pcd / 2')):
        p.cilindro('z', 'cz_ponte_giu', nome, '0 mm', y, 'cox_testa_vite_d', 'cz_ponte_su - cz_ponte_giu', 1, TAGLIA)
    for nome, y in (('foro_vite_a', '-(cox_ins_ponte_y)'), ('foro_vite_b', 'cox_ins_ponte_y')):
        p.cilindro('z', 'cz_ponte_app', nome, 'cx_ins_ponte', y, 'vite_m3_pass', 'cox_ponte_braccio', 1, TAGLIA)
    return occ, p


def _sagoma_femore(p, piano, spessore, prima):
    """Sagoma delle piastre del femore: teste attorno ad anca e ginocchio, fascia centrale, rialzo sotto il blocco."""
    p.cilindro('y', piano, 'testa_anca', 'zam_Lc', '0 mm', '2 * fem_testa_r', spessore, 1, prima)
    p.cilindro('y', piano, 'testa_ginocchio', 'zam_Lc + zam_Lf', '0 mm', '2 * fem_testa_r', spessore)


def fai_femore_b(zampa):
    occ = _nuovo_comp(zampa, 'Femore_B')
    p = Parte(occ.component)
    _sagoma_femore(p, 'zy_B_est', 'fem_B_mozzo', NUOVO)
    p.blocco('y', 'zy_B_est', 'piastra', 'zam_Lc', '-(fem_testa_r)', 'zam_Lc + zam_Lf', 'fem_testa_r', 'fem_piastra')
    p.blocco('y', 'zy_B_est', 'piastra_alta', 'zam_Lc + fem_blocco_x0', 'fem_testa_r - 1 mm', 'zam_Lc + zam_Lf - fem_blocco_dk',
             'fem_blocco_su', 'fem_piastra')
    p.cilindro('y', 'zy_B_int', 'rialzo_anca', 'zam_Lc', '0 mm', 'cus_rialzo_d', 'cus_rialzo_h')
    p.cilindro('y', 'zy_B_int', 'rialzo_ginocchio', 'zam_Lc + zam_Lf', '0 mm', 'cus_rialzo_d', 'cus_rialzo_h')
    # blocco pieno tra le piastre (lo slicer lo stampa a pareti e riempimento)
    p.blocco('y', 'zy_B_est + fem_piastra', 'blocco', 'zam_Lc + fem_blocco_x0', '-(fem_blocco_giu)',
             'zam_Lc + zam_Lf - fem_blocco_dk', 'fem_blocco_su',
             'zy_A_est - fem_piastra - fem_luce_A - zy_B_est - fem_piastra')
    lung_b = 'sqrt(fem_smusso_bx ^ 2 + fem_smusso_bz ^ 2)'
    p.blocco_obl('y', 'zy_B_est + fem_piastra', 'smusso_basso',
                 ('zam_Lc + zam_Lf - fem_blocco_dk - fem_smusso_bx', '-(fem_blocco_giu)'),
                 ('zam_Lc + zam_Lf - fem_blocco_dk', 'fem_smusso_bz - fem_blocco_giu'),
                 '-(5 mm)', lung_b + ' + 5 mm', '-(10 mm)', '0 mm', 'zy_A_est - zy_B_est - 2 * fem_piastra', 1, TAGLIA)
    p.blocco_obl('y', 'zy_B_est + fem_piastra', 'smusso_alto',
                 ('zam_Lc + fem_blocco_x0', 'fem_blocco_su - fem_smusso_alto'),
                 ('zam_Lc + fem_blocco_x0 + fem_smusso_alto', 'fem_blocco_su'),
                 '-(5 mm)', 'fem_smusso_alto * 1.415 + 5 mm', '0 mm', '10 mm', 'zy_A_est - zy_B_est - 2 * fem_piastra', 1, TAGLIA)
    p.cilindro('y', 'zy_B_est', 'foro_perno_anca', 'zam_Lc', '0 mm', 'perno_foro', 'fem_B_mozzo + cus_rialzo_h', 1, TAGLIA)
    p.cilindro('y', 'zy_B_est', 'foro_perno_ginocchio', 'zam_Lc + zam_Lf', '0 mm', 'perno_foro', 'fem_B_mozzo + cus_rialzo_h', 1, TAGLIA)
    y_rim = 'zy_A_est - fem_piastra - fem_luce_A'
    for nome, x, z in _inserti_blocco():
        p.cilindro('y', y_rim, nome, x, z, 'ins_m3_d', 'ins_m3_l', -1, TAGLIA)
    return occ, p


def _inserti_blocco():
    """Quattro inserti M3 per la piastra A, negli angoli del blocco lontani dagli smussi."""
    x0, x1 = 'zam_Lc + fem_blocco_x0 + fem_ins_dx', 'zam_Lc + zam_Lf - fem_blocco_dk - fem_ins_dx'
    z0, z1 = 'fem_ins_dx - fem_blocco_giu + 2 mm', 'fem_blocco_su - fem_ins_dx - 2 mm'
    return [('ins_blocco_ab', x0, z0), ('ins_blocco_aa', x0, z1), ('ins_blocco_gb', x1, z0 + ' + 3 mm'), ('ins_blocco_ga', x1, z1)]


def fai_femore_a(zampa):
    occ = _nuovo_comp(zampa, 'Femore_A')
    p = Parte(occ.component)
    _sagoma_femore(p, 'zy_disco', 'zy_A_est - zy_disco', NUOVO)
    p.blocco('y', 'zy_A_est - fem_piastra', 'piastra', 'zam_Lc', '-(fem_testa_r)', 'zam_Lc + zam_Lf', 'fem_testa_r', 'fem_piastra')
    p.blocco('y', 'zy_A_est - fem_piastra', 'piastra_alta', 'zam_Lc + fem_blocco_x0', 'fem_testa_r - 1 mm',
             'zam_Lc + zam_Lf - fem_blocco_dk', 'fem_blocco_su', 'fem_piastra')
    for giunto, x in (('anca', 'zam_Lc'), ('ginocchio', 'zam_Lc + zam_Lf')):
        p.cilindro('y', 'zy_disco', 'sede_disco_' + giunto, x, '0 mm', 'sq_d + 2 * gio_stampa', 'sq_sp', 1, TAGLIA)
        p.cilindro('y', 'zy_disco', 'foro_centrale_' + giunto, x, '0 mm', 'sq_accesso_d', 'zy_A_est - zy_disco', 1, TAGLIA)
        for nome, dx, dz in (('a', ' + sq_fori_pcd / 2', '0 mm'), ('b', ' - sq_fori_pcd / 2', '0 mm'),
                             ('c', '', 'sq_fori_pcd / 2'), ('d', '', '-(sq_fori_pcd / 2)')):
            p.cilindro('y', 'zy_disco', 'foro_sq_%s_%s' % (giunto, nome), x + dx, dz, 'vite_m3_pass', 'zy_A_est - zy_disco', 1, TAGLIA)
    for nome, x, z in _inserti_blocco():
        p.cilindro('y', 'zy_A_est - fem_piastra', nome.replace('ins', 'foro'), x, z, 'vite_m3_pass', 'fem_piastra', 1, TAGLIA)
    return occ, p


def fai_tibia(zampa):
    occ = _nuovo_comp(zampa, 'Tibia')
    p = Parte(occ.component)
    xk = 'zam_Lc + zam_Lf'
    _culla(p, xk)
    p.blocco('y', '-(zy_orlo)', 'stinco', xk + ' - tib_stinco_semi', '-(zam_Lt - tib_piede_r)', xk + ' + tib_stinco_semi',
             '-(cul_coda)', '2 * zy_orlo')
    p.cilindro('y', '-(zy_orlo)', 'piede', xk, '-(zam_Lt - tib_piede_r)', '2 * tib_piede_r', '2 * zy_orlo')
    _sede(p, xk)
    _alleggerisci_culla(p, xk, (1, -1))
    for i in range(3):
        z0 = 'tib_fin_z0 + %d * tib_fin_passo' % i
        p.blocco('y', '-(zy_orlo)', 'finestra_stinco_%d' % (i + 1), xk + ' - tib_fin_semi', '-(%s + tib_fin_l)' % z0,
                 xk + ' + tib_fin_semi', '-(%s)' % z0, '2 * zy_orlo', 1, TAGLIA)
    return occ, p


# ----------------------------------------------------------------------------------- istanze e giunti
# (chiave, componente di libreria, origine come espressioni, versori degli assi del componente nella terna della zampa)
ASSI_Y = ((1, 0, 0), (0, 0, -1), (0, 1, 0))           # asse z del componente lungo +Y
ASSI_SERVO = ((0, 0, -1), (-1, 0, 0), (0, 1, 0))       # x_s -> -Z (coda in basso), z_s -> +Y (albero)
ISTANZE = [
    ('Servo_Femore', 'Rif_Servo_MG996R', ('zam_Lc', 'zy_orlo', '0 mm'), ASSI_SERVO),
    ('Servo_Ginocchio', 'Rif_Servo_MG996R', ('zam_Lc + zam_Lf', 'zy_orlo', '0 mm'), ASSI_SERVO),
    ('Squadretta_Femore', 'Rif_Squadretta_25T', ('zam_Lc', 'zy_disco + sq_sp', '0 mm'), ASSI_Y),
    ('Squadretta_Ginocchio', 'Rif_Squadretta_25T', ('zam_Lc + zam_Lf', 'zy_disco + sq_sp', '0 mm'), ASSI_Y),
    ('Squadretta_Coxa', 'Rif_Squadretta_25T', ('0 mm', '0 mm', 'cz_ponte_giu + sq_sp'), ((1, 0, 0), (0, 1, 0), (0, 0, 1))),
    ('Cuscinetto_Femore', 'Rif_Cuscinetto_LF1050ZZ', ('zam_Lc', 'zy_fondo_est - cus_flangia_sp', '0 mm'), ASSI_Y),
    ('Cuscinetto_Ginocchio', 'Rif_Cuscinetto_LF1050ZZ', ('zam_Lc + zam_Lf', 'zy_fondo_est - cus_flangia_sp', '0 mm'), ASSI_Y),
    ('Perno_Femore', 'Rif_Perno_5', ('zam_Lc', 'zy_B_est - perno_sporge', '0 mm'), ASSI_Y),
    ('Perno_Ginocchio', 'Rif_Perno_5', ('zam_Lc + zam_Lf', 'zy_B_est - perno_sporge', '0 mm'), ASSI_Y),
    ('Perno_Coxa', 'Rif_Perno_5', ('0 mm', '0 mm', '-(bug_coda + perno_sporge)'), ((1, 0, 0), (0, 1, 0), (0, 0, 1))),
]
# (nome del giunto, parte che si muove, parte fissa)
RIGIDI = [
    ('R_ponte', 'Coxa_Ponte', 'Coxa'), ('R_servo_femore', 'Servo_Femore', 'Coxa'),
    ('R_cuscinetto_femore', 'Cuscinetto_Femore', 'Coxa'), ('R_perno_coxa', 'Perno_Coxa', 'Coxa'),
    ('R_squadretta_coxa', 'Squadretta_Coxa', 'Coxa_Ponte'), ('R_femore_a', 'Femore_A', 'Femore_B'),
    ('R_squadretta_femore', 'Squadretta_Femore', 'Femore_A'), ('R_squadretta_ginocchio', 'Squadretta_Ginocchio', 'Femore_A'),
    ('R_perno_femore', 'Perno_Femore', 'Femore_B'), ('R_perno_ginocchio', 'Perno_Ginocchio', 'Femore_B'),
    ('R_servo_ginocchio', 'Servo_Ginocchio', 'Tibia'), ('R_cuscinetto_ginocchio', 'Cuscinetto_Ginocchio', 'Tibia'),
]


def _mm(des, expr):
    return des.unitsManager.evaluateExpression(expr, 'mm') * 10.0


def _pose(des):
    """{chiave: (componente di libreria, matrice nella terna della zampa)}."""
    out = {}
    for chiave, lib, origine, assi in ISTANZE:
        out[chiave] = (lib, A['matrice']([_mm(des, e) for e in origine], *assi))
    return out


def _istanze(zampa):
    """Occorrenze native dentro la Zampa abbinate alle chiavi per componente e posizione (l'ordine non e' affidabile)."""
    des = zampa.component.parentDesign
    occ = {o.component.name: o for o in zampa.component.occurrences if not o.component.name.startswith('Rif_')}
    rif = [o for o in zampa.component.occurrences if o.component.name.startswith('Rif_')]
    for chiave, (lib, m) in _pose(des).items():
        cand = [o for o in rif if o.component.name == lib]
        if cand:
            t = m.translation
            occ[chiave] = A['piu_vicina'](cand, (t.x * 10, t.y * 10, t.z * 10))
    return occ


def fai_istanze(des, root, zampa):
    lib = {o.component.name: o for o in root.occurrences if o.component.name.startswith('Rif_')}
    gia = [o for o in zampa.component.occurrences if o.component.name.startswith('Rif_')]
    for o in gia:
        o.deleteMe()
    fatte = []
    for chiave, (nome_lib, m) in _pose(des).items():
        A['aggiungi_istanza'](root, lib[nome_lib], m, dentro=zampa)
        fatte.append(chiave)
    return {'cancellate': len(gia), 'create': fatte}


def controlla_istanze(des, zampa):
    """Scarto (mm e radianti) tra la trasformata reale di ogni istanza e quella attesa."""
    occ = _istanze(zampa)
    out = {}
    for chiave, (lib, m) in _pose(des).items():
        o = occ.get(chiave)
        if o is None:
            out[chiave] = 'assente'
            continue
        t = o.transform2
        a, b = t.asArray(), m.asArray()
        out[chiave] = round(max(abs(x - y) * (10 if i % 4 == 3 else 1) for i, (x, y) in enumerate(zip(a, b))), 4)
    return out


def fai_giunti(des, zampa):
    comp = zampa.component
    for j in list(comp.asBuiltJoints):
        j.deleteMe()
    occ = _istanze(zampa)
    fatti = []
    for nome, a, b in RIGIDI:
        A['giunto_rigido'](comp, occ[a], occ[b], nome)
        fatti.append(nome)
    lc, lf = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lf')
    r = _mm(des, 'perno_foro') / 2
    f_anca = A['faccia_cilindrica'](occ['Femore_B'], r, (lc, 0, 0), 'y')
    f_ginocchio = A['faccia_cilindrica'](occ['Femore_B'], r, (lc + lf, 0, 0), 'y')
    if f_anca is None or f_ginocchio is None:
        raise RuntimeError('fori dei perni di Femore_B non trovati')
    A['giunto_rivoluzione'](comp, occ['Femore_B'], occ['Coxa'], f_anca, 'G_femore')
    A['giunto_rivoluzione'](comp, occ['Tibia'], occ['Femore_B'], f_ginocchio, 'G_ginocchio')
    return fatti + ['G_femore', 'G_ginocchio']


# ----------------------------------------------------------------------------------- controlli
# Stima della massa delle parti stampate: PETG-CF 1,3 g/cm3, pareti e fondi 1,2 mm, riempimento 25 % (stima S)
RHO, GUSCIO_CM, RIEMPIMENTO = 1.3, 0.12, 0.25


def stato(des, root):
    out = {}
    z = L['trova_occ'](root, 'Zampa')
    if not z:
        return 'Zampa assente'
    for o in z[0].childOccurrences:
        c = o.component
        bb = None
        for b in c.bRepBodies:
            if bb is None:
                bb = b.boundingBox.copy()
            else:
                bb.combine(b.boundingBox)
        v = sum(b.volume for b in c.bRepBodies)
        area = sum(b.area for b in c.bRepBodies)
        pareti = min(v, area * GUSCIO_CM)
        riga = {'corpi': c.bRepBodies.count, 'volume_cm3': round(v, 3),
                'massa_g': round(RHO * (pareti + (v - pareti) * RIEMPIMENTO), 1)}
        if bb is not None:
            riga['ingombro'] = [round(v * 10, 2) for v in (bb.minPoint.x, bb.minPoint.y, bb.minPoint.z,
                                                           bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z)]
        nv = [s.name for s in c.sketches if not s.isFullyConstrained]
        if nv:
            riga['schizzi_non_vincolati'] = nv
        out[c.name] = riga
    tl = des.timeline
    out['_timeline_problemi'] = [(tl.item(i).name, tl.item(i).errorOrWarningMessage) for i in range(tl.count)
                                 if not tl.item(i).isGroup and tl.item(i).healthState !=
                                 adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
    return out


# Convenzione dei giunti, misurata (passo "calibra"): alpha = SF * valore di G_femore,
# gamma = 90 + SG * valore di G_ginocchio. Da rimisurare se si rifanno i giunti.
SF, SG = -1.0, -1.0       # misurati il 9 ottobre 2026: +10 su G_femore -> alpha -10; +10 su G_ginocchio -> gamma 80


def _giunto(zampa, nome):
    return [j for j in zampa.component.asBuiltJoints if j.name == nome][0]


def _rev(j):
    return adsk.fusion.RevoluteJointMotion.cast(j.jointMotion)


def misura(zampa):
    """(alpha, gamma) in gradi dalle trasformate reali, rispetto alla coxa (nella zampa nessuna parte e' fissa)."""
    # le trasformate delle occorrenze native restano quelle "come costruito": la posa vera e' nei proxy
    occ = {k: o.createForAssemblyContext(zampa) for k, o in _istanze(zampa).items()}
    inv = occ['Coxa'].transform2.copy()
    inv.invert()

    def rel(o):
        m = o.transform2.copy()
        m.transformBy(inv)
        return m
    fb, tb = rel(occ['Femore_B']), rel(occ['Tibia'])
    dx = V3(1, 0, 0)
    dx.transformBy(fb)
    alpha = math.degrees(math.atan2(dx.z, dx.x))
    dp = V3(0, 0, -1)
    dp.transformBy(tb)
    beta = math.degrees(math.atan2(dp.z, dp.x))
    gamma = (beta - alpha - 180.0) % 360.0
    return round(alpha, 3), round(gamma, 3)


def calibra(zampa):
    jf, jg = _giunto(zampa, 'G_femore'), _giunto(zampa, 'G_ginocchio')
    _rev(jf).rotationValue = 0
    _rev(jg).rotationValue = 0
    zero = misura(zampa)
    _rev(jf).rotationValue = math.radians(10)
    a10 = misura(zampa)
    _rev(jf).rotationValue = 0
    _rev(jg).rotationValue = math.radians(10)
    g10 = misura(zampa)
    _rev(jg).rotationValue = 0
    return {'zero': zero, 'femore_10': a10, 'ginocchio_10': g10,
            'valori_letti': [A['valore_giunto'](jf), A['valore_giunto'](jg)]}


def imposta(zampa, alpha, gamma):
    """Porta la zampa in (alpha, gamma) con i giunti veri; ritorna la posa misurata."""
    _rev(_giunto(zampa, 'G_femore')).rotationValue = math.radians(SF * alpha)
    _rev(_giunto(zampa, 'G_ginocchio')).rotationValue = math.radians(SG * (gamma - 90.0))
    return misura(zampa)


def scansione(des, zampa, pose):
    """Interferenze con i giunti veri per ogni posa [(alpha, gamma)]; alla fine torna alla posa di riferimento."""
    out = {}
    for a, g in pose:
        mis = imposta(zampa, a, g)
        urti = interferenze(des, zampa)
        chiave = '%g/%g' % (a, g)
        out[chiave] = [(_corto(x), _corto(y), v) for x, y, v in urti] if urti else 'libera'
        if abs(mis[0] - a) > 0.01 or abs(mis[1] - g) > 0.01:
            out[chiave] = {'posa_misurata': mis, 'urti': out[chiave]}
    imposta(zampa, 0.0, 90.0)
    return out


def _corto(percorso):
    return percorso.split('+')[-1].split(':')[0]


# Campo libero misurato con la scansione 3D del 9 ottobre 2026 (senza corpo): femore da -45 a +85, ginocchio da 30 a 175.
# Il minimo del ginocchio dipende dal femore (45-55 con il femore sotto -15): lo limita il firmware.
LIMITI = {'alpha': (-45.0, 85.0), 'gamma': (30.0, 175.0)}


def fai_limiti(zampa):
    """Limiti dei giunti nei valori propri dei giunti (alpha = -valore, gamma = 90 - valore)."""
    a0, a1 = LIMITI['alpha']
    g0, g1 = LIMITI['gamma']
    A['imposta_limiti'](_giunto(zampa, 'G_femore'), -a1, -a0)
    A['imposta_limiti'](_giunto(zampa, 'G_ginocchio'), 90.0 - g1, 90.0 - g0)
    return LIMITI


def interferenze(des, zampa, extra=()):
    """Interferenze tra le parti della zampa (e le occorrenze extra della radice) nella posa attuale."""
    occ = [o.createForAssemblyContext(zampa) for o in zampa.component.occurrences] + list(extra)
    return A['interferenze'](des, occ, scarta=_voluta)


def _voluta(corpo_a, corpo_b, a, b):
    """Sovrapposizioni volute: il mozzo della squadretta (ingombro pieno) calza il millerighe del servo."""
    coppia = {a.split(':')[0].split('+')[-1], b.split(':')[0].split('+')[-1]}
    return coppia == {'Rif_Servo_MG996R', 'Rif_Squadretta_25T'}


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
        zampa = _zampa(root)
        for nome, f in (('coxa', fai_coxa), ('ponte', fai_ponte), ('femore_b', fai_femore_b), ('femore_a', fai_femore_a),
                        ('tibia', fai_tibia)):
            if nome in passi:
                occ, p = f(zampa)
                out[nome] = _chiudi(des, occ.component.name, p)
        if 'istanze' in passi:
            out['istanze'] = fai_istanze(des, root, zampa)
        if 'controllo' in passi:
            out['controllo'] = controlla_istanze(des, zampa)
        if 'giunti' in passi:
            out['giunti'] = fai_giunti(des, zampa)
        if 'calibra' in passi:
            out['calibra'] = calibra(zampa)
        if 'misura' in passi:
            out['misura'] = misura(zampa)
        if 'interferenze' in passi:
            out['interferenze'] = interferenze(des, zampa)
        if 'scansione' in passi:
            out['scansione'] = scansione(des, zampa, kw['pose'])
        if 'limiti' in passi:
            out['limiti'] = fai_limiti(zampa)
        if 'riferimento' in passi:
            out['riferimento'] = imposta(zampa, 0.0, 90.0)
        if 'stato' in passi:
            out['stato'] = stato(des, root)
            out['snapshot_pendente'] = des.snapshots.hasPendingSnapshot
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
