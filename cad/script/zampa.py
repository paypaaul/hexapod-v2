"""Zampa dell'esapode MG996R: parti progettate, istanze dei componenti comprati, giunti (fase 4, D-047, D-048).

Si esegue dentro Fusion sul design di lavoro (`versione.py`), un passo per chiamata:
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
V = runpy.run_path(os.path.join(QUI, 'versione.py'))
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
    ('ins_sposta_corto', '0.6 mm', 'mm', 'Inserti lato albero spostati verso l estremita: al massimo 0,6 (foro dell aletta 4,2, vite 3, asola 2,5)'),
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
    ('cul_fin_lato', '12 mm', 'mm', 'Culla: lato delle finestre a rombo nelle pareti (45 gradi, senza supporti)'),
    ('cul_fin_y', '-5 mm', 'mm', 'Culla: Y del centro delle finestre nelle pareti'),
    ('cul_fin_z1', '1 mm', 'mm', 'Culla: centro della finestra vicina all albero, sotto l asse (valore assoluto)'),
    ('cul_fin_z2', '20.5 mm', 'mm', 'Culla: centro della finestra verso la coda, sotto l asse (valore assoluto)'),
    # --- uscita del cavo (lato corto, vicino all'albero)
    ('cav_fin_w', '9 mm', 'mm', 'Finestra del cavo: larghezza (passa la spina JR 7,9 x 2,75)'),
    ('cav_fin_alto', '9 mm', 'mm', 'Finestra del cavo: bordo verso l orlo, sotto le alette'),
    ('cav_fin_basso', '26.1 mm', 'mm', 'Finestra del cavo: bordo verso il fondo, sotto le alette'),
    ('cav_gola_w', '7.6 mm', 'mm', 'Gola del fermacavo: larghezza (fermacavo 7)'),
    ('cav_gola_p', '1.0 mm', 'mm', 'Gola del fermacavo: profondita (sporgenza 1,0; con il gioco 0,2 della sede resta 0,2)'),
    ('cav_fes_semi', '3.35 mm', 'mm', 'Fessura del passacavo dall orlo alla finestra: semilarghezza (passacavo 6,3 dallo STEP + 0,2)'),
    ('vite_m3_pilota', '2.5 mm', 'mm', 'Foro pilota per vite M3 autofilettante nella plastica (alette lato albero, D-049)'),
    ('ale_vite_sposta', '0.6 mm', 'mm', 'Viti delle alette lato albero spostate verso l esterno nel foro 4,2 (massimo 0,6)'),
    # --- giunto lato cuscinetto
    ('cus_rialzo_h', '0.4 mm', 'mm', 'Rialzo che tocca solo l anello interno del cuscinetto'),
    ('cus_rialzo_d', '6.2 mm', 'mm', 'Rialzo: diametro (diametro interno di riferimento LF-1050ZZ 6,40)'),
    ('cus_sede_d', 'cus_D', 'mm', 'Sede del cuscinetto: diametro nominale (forzamento da provino)'),
    ('cus_sede_prof', 'cus_B - cus_flangia_sp', 'mm', 'Sede del cuscinetto: profondita'),
    ('cus_passo_d', '7.2 mm', 'mm', 'Foro dietro il cuscinetto: piu grande dell anello interno (6,4), la spalla tocca solo l anello esterno'),
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
    ('cox_anima_sp', '4 mm', 'mm', 'Coxa: spessore dell anima (gioco dalla gondola 1,2)'),
    ('cx_anima', 'zam_Lc - cul_sede_semi - cox_anima_sp', 'mm', 'Coxa: X della faccia interna dell anima (gondola raggio 39,32 + 0,8)'),
    ('cox_braccio_sp', '5.2 mm', 'mm', 'Coxa: spessore del braccio inferiore (perno forzato)'),
    ('cox_nerv_h', '3 mm', 'mm', 'Coxa: nervatura sotto il braccio, altezza alla radice'),
    ('cox_nerv_semi', '3 mm', 'mm', 'Coxa: nervatura, semilarghezza'),
    ('cox_nerv_x0', '10 mm', 'mm', 'Coxa: X dove la nervatura si annulla'),
    ('cz_braccio_su', 'bug_coda - cox_braccio_sp', 'mm', 'Coxa: faccia superiore del braccio inferiore, sotto l asse (valore assoluto)'),
    ('cox_tasca_lato', '18 mm', 'mm', 'Coxa: lato della tasca a rombo nell anima'),
    ('cox_tasca_y', '-7.35 mm', 'mm', 'Coxa: Y del centro della tasca nell anima'),
    ('cox_tasca_z', '14 mm', 'mm', 'Coxa: centro della tasca nell anima, sotto l asse (valore assoluto)'),
    ('cz_alette_coxa', 'srv_sotto + cul_gio_fondo + cul_fondo + cus_flangia_sp + cus_rialzo_h - cz_braccio_su', 'mm',
     'Z delle alette del servo di coxa (orlo della gondola)'),
    ('cox_gondola_luce', '1 mm', 'mm', 'Coxa: luce tra la testa dell anima e le teste delle viti delle alette del servo di coxa'),
    ('vite_m3_testa_h', '3 mm', 'mm', 'Vite M3 ISO 4762: altezza della testa'),
    ('cz_mensola', 'cz_alette_coxa + srv_alette_sp + vite_m3_testa_h + cox_gondola_luce', 'mm',
     'Coxa: Z del lato inferiore della testa dell anima (a raggio 34-40 dalla coxa passa sopra le alette e le viti lato coda del servo di coxa)'),
    ('cx_testa', '34 mm', 'mm', 'Coxa: X dell estremo interno della testa dell anima (fuori dalla cassa del servo di coxa, raggio 32,4)'),
    ('cz_ponte_giu', 'cz_alette_coxa + srv_albero_h - srv_spline_l + sq_h - sq_sp', 'mm', 'Ponte: Z del lato inferiore del disco della squadretta di coxa'),
    ('cox_ponte_sopra', '3.95 mm', 'mm', 'Ponte: altezza sopra il disco (teste delle viti M3 x 5 alte 3, senza rondella, D-049)'),
    ('cz_ponte_su', 'cz_ponte_giu + sq_sp + cox_ponte_sopra', 'mm', 'Ponte: Z della faccia superiore'),
    ('cox_ponte_braccio', '3.9 mm', 'mm', 'Ponte: spessore del braccio'),
    ('cz_ponte_app', 'cz_ponte_su - cox_ponte_braccio', 'mm', 'Ponte: Z dell appoggio sulla testa dell anima'),
    ('cox_ponte_r', '12 mm', 'mm', 'Ponte: raggio del mozzo'),
    ('cox_fascetta_x', '24 mm', 'mm', 'Ponte: X delle feritoie della fascetta dei cavi (sotto il lobo del carapace; testa della fascetta di fianco al braccio, D-060)'),
    ('cox_fascetta_y', '5.5 mm', 'mm', 'Ponte: Y delle feritoie (fuori dai due cavi piatti affiancati, 7,6 mm)'),
    ('fascetta_w', '3 mm', 'mm', 'Feritoia per fascetta da 2,5 mm: larghezza'),
    ('fascetta_sp', '1.6 mm', 'mm', 'Feritoia per fascetta: spessore (fascetta 1,0)'),
    ('cox_fascetta_gola', '1.2 mm', 'mm', 'Ponte: gola sotto il braccio tra le feritoie (la fascetta non striscia sul servo di coxa)'),
    # --- passata estetica (D-060): teste delle viti, fascetta del femore nel blocco, spine della lama B
    ('vite_m3_testa_d', '5.5 mm', 'mm', 'Vite M3 ISO 4762: diametro della testa (dk 5,32-5,5)'),
    ('fem_fascetta_u', '24.5 mm', 'mm', 'Femore: X dall anca della fascetta dei cavi dentro il blocco (sullo smusso alto)'),
    ('fem_fascetta_fondo', '10 mm', 'mm', 'Femore: Z del tunnel della fascetta nel blocco'),
    ('cov_vite_b_z', '6 mm', 'mm', 'Lama B: Z delle due viti M2 svasate in inserti di Femore_B (al posto delle spine, D-065)'),
    ('cov_svasatura', '0.9 mm', 'mm', 'Lama B: svasatura a 90 gradi sul foro da 2,4 (testa M2 da 4,0: resta 0,1 sotto la superficie)'),
    # --- lame del femore "Piena" (D-061): bombate, estremi esagonali raccordati attorno alle teste del femore
    ('cov_ap', '14.5 mm', 'mm', 'Lame: semialtezza e apotema degli estremi esagonali (teste del femore R13)'),
    ('cov_tc', '2.6 mm', 'mm', 'Lame: spessore al colmo (1,6 ai bordi alti e bassi)'),
    ('cov_Rb', '148.8 mm', 'mm', 'Lame: raggio della bombatura trasversale (1,0 mm su 17,25)'),
    ('cov_Rb2', '1920 mm', 'mm', 'Lame: raggio della bombatura longitudinale (0,6 mm su 48)'),
    ('cov_zc', '2.75 mm', 'mm', 'Lame: Z del colmo'),
    ('cov_xc', '32.5 mm', 'mm', 'Lame: X del colmo dall asse dell anca'),
    ('cov_r', '0.8 mm', 'mm', 'Lame: raccordo degli spigoli della faccia esterna'),
    ('cov_r_estremo', '8 mm', 'mm', 'Lame: raccordo in pianta degli estremi esagonali'),
    ('cov_r_rampa', '10 mm', 'mm', 'Lame: raccordo in pianta alla base e in cima alla rampa dell anca, alla base di quella del ginocchio'),
    ('cov_r_plateau', '8 mm', 'mm', 'Lame: raccordo in pianta della fine del plateau'),
    ('cov_x_plateau0', '26 mm', 'mm', 'Lame: inizio del plateau sopra il blocco, dall asse dell anca (X 81)'),
    ('cov_x_plateau1', '41 mm', 'mm', 'Lame: fine del plateau (X 96)'),
    ('cov_gobba_z', 'fem_blocco_su', 'mm', 'Lame: cima della gobba sopra il blocco'),
    ('cov_fin_ap', '11 mm', 'mm', 'Lame: apotema delle finestre sui mozzi (teste delle squadrette fino a r 9,75)'),
    ('cov_r_fin', '4 mm', 'mm', 'Lame: raccordo degli angoli delle finestre'),
    ('cov_testa_d', '5.6 mm', 'mm', 'Lama A: fori sulle teste M3 del blocco (incastro sui fianchi, da tarare 5,4-5,7)'),
    ('cox_disco_luce', '0.3 mm', 'mm', 'Ponte: luce sopra il disco (gioco verticale della coxa, D-048)'),
    ('cox_testa_vite_d', '5.6 mm', 'mm', 'Ponte: fori che calzano le teste delle viti M3 della squadretta (gioco d imbardata: tarare sul provino)'),
    ('cox_smusso_ponte', '2.5 mm', 'mm', 'Ponte: smusso dello spigolo esterno alto'),
    ('cx_ins_ponte', 'cx_testa + 4.6 mm', 'mm', 'Coxa: X degli inserti del ponte (teste delle viti fuori dallo smusso)'),
    ('cox_ins_ponte_y', '5.5 mm', 'mm', 'Coxa: Y degli inserti del ponte'),
    ('cox_ling_l', '6 mm', 'mm', 'Ponte: linguetta di centraggio, lunghezza'),
    ('cox_ling_semi', '1.5 mm', 'mm', 'Ponte: linguetta, semilarghezza'),
    ('cox_ling_h', '1.6 mm', 'mm', 'Ponte: linguetta, altezza'),
    # --- tibia
    # --- stinco V2 allargato (D-061): fianco esterno ad arco tangente allo zoccolo, interno appena rastremato (al gamma
    #     minimo e' il lato che passa a pochi centesimi dalla coxa: non cresce); fianchi Y simmetrici sul piano della
    #     zampa, Y 0, cosi' il piede sta sull'asse del femore (D-065; in D-062 erano sul piano medio dello zoccolo, Y -7,35)
    ('tib_x_meno_alto', '6 mm', 'mm', 'Stinco: semilarghezza verso -X sotto lo zoccolo (come oggi)'),
    ('tib_x_meno_basso', '4 mm', 'mm', 'Stinco: semilarghezza verso -X alla punta'),
    ('tib_x_piu_basso', '6 mm', 'mm', 'Stinco: semilarghezza verso +X alla fine dell arco (in alto e cul_semi, a filo dello zoccolo); 6 per la testa dell FSR (D-066, prima 4)'),
    ('tib_piede_sp', '1.6 mm', 'mm', 'Piedino in TPU (D9): parete e suola (4 perimetri); lo stinco finisce a zam_Lt - tib_piede_sp, la suola a zam_Lt'),
    ('tib_piede_z0', 'cov_tib_z1 + 0.5 mm', 'mm', 'Piedino: bordo alto, 0,5 sotto il guscio della tibia'),
    ('tib_z_arco', 'zam_Lt - tib_piede_sp - 4 mm', 'mm', 'Stinco: fine dell arco e dei fianchi dritti, sotto l asse del ginocchio'),
    ('tib_arco_R', '((cul_semi - tib_x_piu_basso) ^ 2 + (tib_z_arco - bug_coda) ^ 2) / (2 * (cul_semi - tib_x_piu_basso))',
     'mm', 'Stinco: raggio dell arco del fianco +X (tangente allo zoccolo, 275 mm)'),
    ('tib_y_c', '0 mm', 'mm', 'Stinco: piano medio dei fianchi Y (piano della zampa: il piede sta sull asse del femore)'),
    ('tib_y_semi_alto', '-(zy_fondo_est)', 'mm', 'Stinco: semilarghezza in Y sotto lo zoccolo (a filo dello zoccolo sul -Y, sul +Y sotto le alette del servo)'),
    ('tib_y_semi_basso', '7 mm', 'mm', 'Stinco: semilarghezza in Y alla fine dei fianchi dritti (punta 8 x 14)'),
    # --- predisposizioni della versione 2.1.0 (D-066): sensore di forza nel piede (X5) e luci nelle tibie (X31)
    ('sen_fsr_sp', '0.3 mm', 'mm', 'FSR 400 Short: spessore (S, rivenditore)'),
    ('sen_fsr_testa_d', '7.6 mm', 'mm', 'FSR 400 Short: diametro della testa (S); area attiva 5,6 (V, Interlink)'),
    ('sen_fsr_dx', '0.2 mm', 'mm', 'FSR: X del centro della testa dall asse del ginocchio (centro della parte piana della punta)'),
    ('tib_pistone_sp', '0.5 mm', 'mm', 'Piedino: altezza del pistoncino sulla suola, che spinge sull area attiva dell FSR'),
    ('tib_pistone_d', '4.5 mm', 'mm', 'Piedino: diametro del pistoncino (piu piccolo dell area attiva, come chiede Interlink)'),
    ('tib_punta_z', 'zam_Lt - tib_piede_sp - sen_fsr_sp - tib_pistone_sp', 'mm', 'Tibia: fine dello stinco, punta piana per l FSR; il piedino nasce dallo stinco lungo zam_Lt - tib_piede_sp'),
    ('tib_smusso_piu', '1.5 mm', 'mm', 'Stinco: smusso degli spigoli fra la faccia +X ad arco e i fianchi Y (con la punta larga 6 toccavano lo smusso interno del guscio fra Z 81 e 94; 1,5 ridà circa 0,4 di gioco)'),
    ('tib_punta_r_piu', '1 mm', 'mm', 'Punta dello stinco: raccordo dello spigolo +X, su cui si piega la coda dell FSR (lo spigolo -X resta vivo)'),
    ('tib_tasca_w', '6 mm', 'mm', 'Tibia: tasca per linguette e saldature dell FSR sulla faccia +X, larghezza in Y'),
    ('tib_tasca_h', '9 mm', 'mm', 'Tibia: tasca dell FSR, altezza'),
    ('tib_tasca_p', '1.2 mm', 'mm', 'Tibia: tasca dell FSR, profondita'),
    ('tib_tasca_y', '0.5 mm', 'mm', 'Tibia: centro in Y della tasca dell FSR (tocca la gola dei fili)'),
    ('tib_tasca_z0', 'tib_punta_z - 1.5 mm', 'mm', 'Tibia: fondo della tasca dell FSR, sopra il raccordo della punta'),
    ('tib_gola_w', '2 mm', 'mm', 'Tibia: gola dei fili dell FSR sulla faccia +X, larghezza'),
    ('tib_gola_p', '2 mm', 'mm', 'Tibia: gola dei fili dell FSR, profondita (si ferma al fondo della culla: la parete e di 2)'),
    ('tib_gola_y', '4.5 mm', 'mm', 'Tibia: centro in Y della gola, fuori dalla finestra del guscio (|Y| <= 3,5)'),
    ('pied_tacca', '2 mm', 'mm', 'Piedino: tacca per i fili nel bordo alto sul lato +X, sopra la gola'),
    ('luc_tib_w', '5.4 mm', 'mm', 'Tibia: sede piana della striscia LED WS2812B-2020 larga 5 (C), sotto la finestra del guscio'),
    ('luc_tib_p', '0.5 mm', 'mm', 'Tibia: profondita della sede della striscia alle estremita (al centro circa 1,3: sede piana su faccia ad arco)'),
    ('luc_tib_z0', 'cul_coda', 'mm', 'Tibia: inizio della sede della striscia, al fondo della culla'),
    ('luc_tib_z1', 'cov_tib_fin_z1', 'mm', 'Tibia: fine della sede della striscia, con la finestra del guscio'),
    ('luc_dif_sp', '0.6 mm', 'mm', 'Diffusore della tibia: spessore della lastra (0,6-0,8 dal provino di luce X10)'),
    ('luc_dif_bordo', '2 mm', 'mm', 'Diffusore: lastra oltre il bordo della finestra'),
    ('luc_dif_h', '1 mm', 'mm', 'Diffusore: altezza del bordino a incastro dentro la finestra (resta 0,6 sotto il fronte)'),
    ('luc_dif_parete', '0.6 mm', 'mm', 'Diffusore: parete del bordino'),
    ('luc_dif_gio', '0.1 mm', 'mm', 'Diffusore: gioco per lato del bordino nella finestra (incastro, da tarare sul provino)'),
    # --- guscio lungo della tibia (D-061, prova 3): fronte convesso che sporge verso l'esterno, sezione a C sfaccettata
    ('cov_tib_sporgenza', '7.3 mm', 'mm', 'Guscio della tibia: sporgenza massima del fronte oltre la faccia +X dello zoccolo (con 5,8 lo smusso interno toccava gli spigoli di culla e stinco)'),
    ('cov_tib_zmax', '25 mm', 'mm', 'Guscio della tibia: quota (sotto il ginocchio) della sporgenza massima'),
    ('cov_tib_R', '288 mm', 'mm', 'Guscio della tibia: raggio del fronte (4,7 mm di sporgenza in cima, 4,6 sullo stinco in fondo)'),
    ('cov_tib_z0', 'cul_corto + 1.2 mm', 'mm', 'Guscio della tibia: bordo alto sopra il ginocchio'),
    ('cov_tib_z1', '94 mm', 'mm', 'Guscio della tibia: bordo basso sotto il ginocchio (sopra il piedino)'),
    ('cov_tib_sp', '1.6 mm', 'mm', 'Guscio della tibia: spessore'),
    ('cov_tib_gio', '0.4 mm', 'mm', 'Guscio della tibia: aria sui fianchi della culla e dello stinco'),
    ('cov_tib_smusso', '4 mm', 'mm', 'Guscio della tibia: smussi a 45 gradi tra fronte e fianchi'),
    ('cov_tib_y_semi_basso', 'tib_y_semi_alto - (tib_y_semi_alto - tib_y_semi_basso) * (cov_tib_z1 - bug_coda) / (tib_z_arco - bug_coda)'
     ' + cov_tib_gio + cov_tib_sp', 'mm', 'Guscio della tibia: semilarghezza in Y in fondo (stinco + aria + spessore, fianchi paralleli allo stinco)'),
    ('cov_tib_fin_w', '7 mm', 'mm', 'Guscio della tibia: larghezza della finestra lunga'),
    ('cov_tib_fin_y', '-(tib_y_c)', 'mm', 'Guscio della tibia: centro della finestra verso -Y (sul piano medio dello stinco)'),
    ('cov_tib_fin_z0', '32 mm', 'mm', 'Guscio della tibia: inizio della finestra sotto il ginocchio (sotto i tappi)'),
    ('cov_tib_fin_z1', '80 mm', 'mm', 'Guscio della tibia: fine della finestra'),
    ('cov_tib_vite_z', '88 mm', 'mm', 'Guscio della tibia: vite M3 in basso nello stinco, sotto la finestra'),
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
    # una alla volta: dopo la prima cancellazione i riferimenti alle altre occorrenze possono non valere piu'
    while L['trova_occ'](genitore, nome):
        L['trova_occ'](genitore, nome)[0].deleteMe()
    T0[nome] = genitore.parentDesign.timeline.count
    occ = genitore.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = nome
    return occ


# punti con nome per il software e le dime (D-066): componente -> [(nome, x, z)] sul piano Y 0 della zampa
PUNTI = {
    'Coxa': [('Asse_coxa', '0 mm', '0 mm'), ('Asse_femore', 'zam_Lc', '0 mm')],
    'Femore_B': [('Asse_femore', 'zam_Lc', '0 mm'), ('Asse_ginocchio', 'zam_Lc + zam_Lf', '0 mm')],
    'Tibia': [('Asse_ginocchio', 'zam_Lc + zam_Lf', '0 mm'), ('Punta_piede', 'zam_Lc + zam_Lf', '-(zam_Lt)')],
}


def _punti(comp):
    """Punti di costruzione P_<nome> nella terna della zampa, su uno schizzo vincolato dall'origine (si rifanno)."""
    for cp in [c for c in comp.constructionPoints if c.name.startswith('P_')]:
        cp.deleteMe()
    for sk in [x for x in comp.sketches if x.name == 'sk_punti']:
        sk.deleteMe()
    p = Parte(comp)
    sk = p._schizzo(comp.xZConstructionPlane, 'punti')
    ex, o = sk.sketchToModelSpace(P3(1, 0, 0)), sk.sketchToModelSpace(P3(0, 0, 0))
    u_lungo_x = abs(ex.x - o.x) > abs(ex.z - o.z)          # l'asse x dello schizzo e' la X del modello?
    fatti = []
    for nome, x, z in PUNTI[comp.name]:
        vx, vz = p.val(x), p.val(z)
        if abs(vx) < 1e-6 and abs(vz) < 1e-6:
            pt = sk.originPoint
        else:
            # creato un po' fuori posto: con la stessa coordinata dell'origine Fusion deduce un allineamento e la quota
            # diventa ipervincolata (CLAUDE.md, sk_poligono); le quote lo portano al valore
            q = sk.modelToSketchSpace(P3(vx / 10, 0, vz / 10))
            pt = sk.sketchPoints.add(P3(q.x + 0.031, q.y + 0.027, 0))
            p._quota_da_origine(sk, pt, True, x if u_lungo_x else z)
            p._quota_da_origine(sk, pt, False, z if u_lungo_x else x)
        inp = comp.constructionPoints.createInput()
        inp.setByPoint(pt)
        cp = comp.constructionPoints.add(inp)
        cp.name = 'P_' + nome
        fatti.append(cp.name)
    if not sk.isFullyConstrained:
        raise RuntimeError('%s: schizzo dei punti non vincolato' % comp.name)
    # servono agli script, non alla vista: spenti come gli altri schizzi
    comp.isSketchFolderLightBulbOn = False
    comp.isConstructionFolderLightBulbOn = False
    return fatti


def _chiudi(des, nome, p):
    if nome not in T0:                     # Fusion ha aggiunto un suffisso al nome del componente
        nome = [k for k in T0 if nome.startswith(k)][-1]
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
    # zoccolo sotto la coda: lega pareti, fondo e bugne (porta il braccio della coxa e lo stinco)
    p.blocco('y', 'zy_fondo_est', 'zoccolo', xc + ' - cul_semi', '-(bug_coda)', xc + ' + cul_semi', '-(cul_coda)',
             'zy_orlo - zy_fondo_est')


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
    # il passacavo rigido (sporge 5 mm dalla testata) scende dall'orlo alla finestra in questa fessura (D-049)
    p.blocco('y', 'zy_orlo - cav_fin_alto', 'fessura_cavo', xc + ' - cav_fes_semi', 'cul_sede_corto - 0.5 mm',
             xc + ' + cav_fes_semi', 'bug_corto + 0.5 mm', 'cav_fin_alto + 0.5 mm', 1, TAGLIA)
    for nome, dx in (('pilota_corto_a', ' - ins_y - ale_vite_sposta'), ('pilota_corto_b', ' + ins_y + ale_vite_sposta')):
        p.cilindro('y', 'zy_orlo', nome, xc + dx, 'ale_foro_corto', 'vite_m3_pilota', 'ins_m3_l', -1, TAGLIA)
    for nome, dx in (('ins_coda_a', ' - ins_y'), ('ins_coda_b', ' + ins_y')):
        p.cilindro('y', 'zy_orlo', nome, xc + dx, '-(ins_coda)', 'ins_m3_d', 'ins_m3_l', -1, TAGLIA)


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
             '-(bug_coda)', 'cox_nerv_semi + zy_orlo')
    p.blocco_obl('y', '-(cox_nerv_semi + 1 mm)', 'nervatura_rastremata', ('cx_anima', '-(bug_coda + cox_nerv_h)'),
                 ('cox_nerv_x0', '-(bug_coda)'), '-(6 mm)', 'sqrt((cx_anima - cox_nerv_x0) ^ 2 + cox_nerv_h ^ 2)',
                 '0 mm', '20 mm', 'cox_nerv_semi + zy_orlo + 2 mm', 1, TAGLIA)
    p.cilindro('z', '-(cz_braccio_su)', 'rialzo', '0 mm', '0 mm', 'cus_rialzo_d', 'cus_rialzo_h')
    # lavorazioni
    _sede(p, 'zam_Lc')
    _alleggerisci_culla(p, 'zam_Lc', (1,))
    p.blocco_obl('x', 'cx_anima', 'tasca_anima', ('cox_tasca_y', '-(cox_tasca_z)'), ('cox_tasca_y + 1 mm', '1 mm - cox_tasca_z'),
                 '-(cox_tasca_lato / 2)', 'cox_tasca_lato / 2', '-(cox_tasca_lato / 2)', 'cox_tasca_lato / 2',
                 'cox_anima_sp - cul_parete', 1, TAGLIA)
    p.cilindro('z', '-(bug_coda)', 'foro_perno', '0 mm', '0 mm', 'perno_foro', 'cox_braccio_sp + cus_rialzo_h', 1, TAGLIA)
    for nome, y in (('ins_ponte_a', '-(cox_ins_ponte_y)'), ('ins_ponte_b', 'cox_ins_ponte_y')):
        p.cilindro('z', 'cz_ponte_app', nome, 'cx_ins_ponte', y, 'ins_m3_d', 'ins_m3_l', -1, TAGLIA)
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
    # fascetta dei cavi di femore e ginocchio, che corrono sul braccio verso il mozzo: due feritoie e una gola sotto
    x0, x1 = 'cox_fascetta_x - fascetta_w / 2', 'cox_fascetta_x + fascetta_w / 2'
    for nome, y0, y1 in (('feritoia_fascetta_a', 'cox_fascetta_y - fascetta_sp / 2', 'cox_fascetta_y + fascetta_sp / 2'),
                         ('feritoia_fascetta_b', '-(cox_fascetta_y + fascetta_sp / 2)', '-(cox_fascetta_y - fascetta_sp / 2)')):
        p.blocco('z', 'cz_ponte_app', nome, x0, y0, x1, y1, 'cox_ponte_braccio', 1, TAGLIA)
    p.blocco('z', 'cz_ponte_app', 'gola_fascetta', x0, '-(cox_fascetta_y + fascetta_sp / 2)', x1, 'cox_fascetta_y + fascetta_sp / 2',
             'cox_fascetta_gola', 1, TAGLIA)
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
    # inserti M2 per le due viti della lama B (D-065; prima fori ciechi per due spine stampate sulla lama)
    for nome, x in (('ins_lama_a', 'zam_Lc + fem_blocco_x0 + fem_ins_dx'), ('ins_lama_g', 'zam_Lc + zam_Lf - fem_blocco_dk - fem_ins_dx')):
        p.cilindro('y', 'zy_B_est', nome, x, 'cov_vite_b_z', 'ins_m2_d', 'ins_m2_l', 1, TAGLIA)
    # fascetta dei cavi dentro il blocco: due feritoie dallo smusso alto e un tunnel tra le due (la fascetta attorno al
    # femore di D-058 entrava nella testa dell'anima della coxa da alfa 74 gradi)
    xf0, xf1 = 'zam_Lc + fem_fascetta_u - fascetta_w / 2', 'zam_Lc + fem_fascetta_u + fascetta_w / 2'
    for nome, y0, y1 in (('feritoia_femore_a', 'cox_fascetta_y - fascetta_sp / 2', 'cox_fascetta_y + fascetta_sp / 2'),
                         ('feritoia_femore_b', '-(cox_fascetta_y + fascetta_sp / 2)', '-(cox_fascetta_y - fascetta_sp / 2)')):
        p.blocco('z', 'fem_fascetta_fondo', nome, xf0, y0, xf1, y1, 'fem_blocco_su - fem_fascetta_fondo', 1, TAGLIA)
    p.blocco('z', 'fem_fascetta_fondo', 'tunnel_fascetta', xf0, '-(cox_fascetta_y + fascetta_sp / 2)', xf1,
             'cox_fascetta_y + fascetta_sp / 2', 'fascetta_sp', 1, TAGLIA)
    return occ, p


# ----------------------------------------------------------------------------------- lame del femore (D-061)
COS30, SIN30 = math.cos(math.radians(30)), math.sin(math.radians(30))


def _esagono(p, q, nome, xc, ap, h, verso, op):
    """Esagono con i vertici lungo X (apotema ap) come unione o taglio di tre rettangoli a 0, 60 e 120 gradi."""
    f = []
    for k, ang in enumerate((0, 60, 120)):
        c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        p1 = ('%s + %.6f mm' % (xc, 10 * c), '%.6f mm' % (10 * s_))
        f.append(p.blocco_obl('y', q, '%s_%d' % (nome, k), (xc, '0 mm'), p1, '-(%s / cos(30 deg) / 2)' % ap,
                              '%s / cos(30 deg) / 2' % ap, '-(%s)' % ap, ap, h, verso, op if k == 0 or op != NUOVO else UNISCI))
    return f


def _spigoli_y(corpo, punti):
    """Spigoli rettilinei paralleli a Y che passano (in X, Z, mm) per i punti dati: [(x, z, chiave)] -> {chiave: [spigoli]}."""
    out = {}
    for e in corpo.edges:
        if e.geometry.curveType != adsk.core.Curve3DTypes.Line3DCurveType:
            continue
        a, b = e.startVertex.geometry, e.endVertex.geometry
        if abs(a.x - b.x) > 1e-5 or abs(a.z - b.z) > 1e-5:
            continue
        for x, z, k in punti:
            if abs(a.x * 10 - x) < 0.05 and abs(a.z * 10 - z) < 0.05:
                out.setdefault(k, []).append(e)
    return out


def _raccorda(comp, gruppi, nome):
    """Un raccordo con un gruppo di spigoli per raggio: gruppi = [(espressione del raggio, [spigoli])]."""
    fil = comp.features.filletFeatures
    inp = fil.createInput()
    for r, spigoli in gruppi:
        if spigoli:
            inp.edgeSetInputs.addConstantRadiusEdgeSet(_collezione(spigoli), adsk.core.ValueInput.createByString(r), False)
    f = fil.add(inp)
    f.name = nome
    return f


def _collezione(oggetti):
    c = adsk.core.ObjectCollection.create()
    for o in oggetti:
        c.add(o)
    return c


def _bombatura(p, nome, y_top, verso):
    """Intersezione con un toro: cerchio di raggio cov_Rb nel piano X = colmo, centro (y_top - verso*cov_Rb; cov_zc),
    ruotato di 20 gradi attorno a una retta parallela a Z a y_top - verso*cov_Rb2 (bombatura doppia della lama)."""
    comp = p.c
    xq = 'zam_Lc + cov_xc'
    yc = '%s - (%d) * cov_Rb' % (y_top, verso)
    sk = p.sk_cerchio('x', xq, nome, yc, 'cov_zc', '2 * cov_Rb')
    # asse di rivoluzione nello stesso schizzo, di costruzione, vincolato come i punti di lib_cad
    ya = '%s - (%d) * cov_Rb2' % (y_top, verso)
    q = p.val(xq)
    a = sk.modelToSketchSpace(p._modello('x', p.val(ya), -60.0, q))
    b = sk.modelToSketchSpace(p._modello('x', p.val(ya), 60.0, q))
    ln = sk.sketchCurves.sketchLines.addByTwoPoints(adsk.core.Point3D.create(a.x, a.y, 0), adsk.core.Point3D.create(b.x, b.y, 0))
    ln.isConstruction = True
    ex, o = sk.sketchToModelSpace(adsk.core.Point3D.create(1, 0, 0)), sk.sketchToModelSpace(adsk.core.Point3D.create(0, 0, 0))
    du, dv = p._uv('x', adsk.core.Point3D.create(ex.x - o.x, ex.y - o.y, ex.z - o.z))
    y_lungo_x = abs(du) > abs(dv)
    if y_lungo_x:
        sk.geometricConstraints.addVertical(ln)
    else:
        sk.geometricConstraints.addHorizontal(ln)
    p._quota_da_origine(sk, ln.startSketchPoint, y_lungo_x, ya)
    p._quota_da_origine(sk, ln.startSketchPoint, not y_lungo_x, '-60 mm')
    p._quota_da_origine(sk, ln.endSketchPoint, not y_lungo_x, '60 mm')
    if not sk.isFullyConstrained and sk.name not in p.non_vincolati:
        p.non_vincolati.append(sk.name)
    rev = comp.features.revolveFeatures
    inp = rev.createInput(sk.profiles.item(0), ln, adsk.fusion.FeatureOperations.IntersectFeatureOperation)
    inp.setAngleExtent(True, adsk.core.ValueInput.createByString('20 deg'))
    inp.participantBodies = [b_ for b_ in comp.bRepBodies]
    f = rev.add(inp)
    f.name = nome
    p.n += 1
    return f


def _cover_femore(zampa, nome, lato):
    """Lama del femore, lato 'A' (+Y, sulla piastra delle squadrette) o 'B' (-Y, sulla piastra dei perni)."""
    occ = _nuovo_comp(zampa, nome)
    p = Parte(occ.component)
    comp = occ.component
    y0, verso = ('zy_A_est', 1) if lato == 'A' else ('zy_B_est', -1)
    y_top = '%s + (%d) * cov_tc' % (y0, verso)
    xh, xk = 'zam_Lc', 'zam_Lc + zam_Lf'
    # sagoma: corpo tra i mozzi, estremi esagonali, plateau sopra il blocco e due rampe (30 gradi anca, 45 ginocchio)
    p.blocco('y', y0, 'corpo', xh, '-(cov_ap)', xk, 'cov_ap', 'cov_tc', verso, NUOVO)
    _esagono(p, y0, 'estremo_anca', xh, 'cov_ap', 'cov_tc', verso, UNISCI)
    _esagono(p, y0, 'estremo_ginocchio', xk, 'cov_ap', 'cov_tc', verso, UNISCI)
    xp0, xp1 = 'zam_Lc + cov_x_plateau0', 'zam_Lc + cov_x_plateau1'
    p.blocco('y', y0, 'plateau', xp0, 'cov_ap - 1 mm', xp1, 'cov_gobba_z', 'cov_tc', verso)
    dz = '(cov_gobba_z - cov_ap)'
    # i rettangoli delle rampe si allungano di 1 mm solo dalla parte della base, dentro il corpo: in cima al plateau
    # devono finire esattamente sullo spigolo, altrimenti lasciano una punta
    p.blocco_obl('y', y0, 'rampa_anca', (xp0 + ' - %s / tan(30 deg)' % dz, 'cov_ap'), (xp0, 'cov_gobba_z'),
                 '-(1 mm)', '%s / sin(30 deg)' % dz, '-(6 mm)', '0 mm', 'cov_tc', verso)
    p.blocco_obl('y', y0, 'rampa_ginocchio', (xp1, 'cov_gobba_z'), (xp1 + ' + %s' % dz, 'cov_ap'),
                 '0 mm', '%s * sqrt(2) + 1 mm' % dz, '-(6 mm)', '0 mm', 'cov_tc', verso)
    corpo = comp.bRepBodies.item(0)
    v = p.val
    ap, R = v('cov_ap'), v('cov_ap') / COS30
    XH, XK, X0, X1, ZG = v(xh), v(xk), v(xp0), v(xp1), v('cov_gobba_z')
    punti = [(XH - R, 0, 'e'), (XH - R / 2, ap, 'e'), (XH - R / 2, -ap, 'e'), (XK + R, 0, 'e'), (XK + R / 2, ap, 'e'),
             (XK + R / 2, -ap, 'e'), (X0 - (ZG - ap) / math.tan(math.radians(30)), ap, 'r'), (X0, ZG, 'r'), (X1, ZG, 'p'),
             (X1 + (ZG - ap), ap, 'r')]
    sp = _spigoli_y(corpo, punti)
    _raccorda(comp, [('cov_r_estremo', sp.get('e', [])), ('cov_r_rampa', sp.get('r', [])), ('cov_r_plateau', sp.get('p', []))],
              'raccordi_sagoma')
    n_sagoma = sum(len(x) for x in sp.values())
    # finestre sui mozzi, angoli raccordati
    for nome_f, xc in (('finestra_anca', xh), ('finestra_ginocchio', xk)):
        _esagono(p, y0, nome_f, xc, 'cov_fin_ap', 'cov_tc', verso, TAGLIA)
    corpo = comp.bRepBodies.item(0)
    rf = v('cov_fin_ap') / COS30
    pf = [(xc + rf * math.cos(math.radians(a)), rf * math.sin(math.radians(a)), 'f') for xc in (XH, XK) for a in range(0, 360, 60)]
    spf = _spigoli_y(corpo, pf).get('f', [])
    _raccorda(comp, [('cov_r_fin', spf)], 'raccordi_finestre')
    # bombatura doppia e raccordo della faccia esterna
    _bombatura(p, 'bombatura', y_top, verso)
    corpo = comp.bRepBodies.item(0)
    tori = [fa for fa in corpo.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.TorusSurfaceType]
    _raccorda(comp, [('cov_r', [e for fa in tori for e in fa.edges])], 'raccordo_esterno')
    # fissaggio: lama A sulle teste M3 del blocco (fori senza raccordo: l'incastro sta sui fianchi delle teste);
    # lama B con due viti M2 svasate negli inserti di Femore_B (D-065): faccia interna piana per la stampa, smontabile
    svasati = 0
    if lato == 'A':
        for nome_t, x, z in _inserti_blocco():
            p.cilindro('y', y0, nome_t.replace('ins_blocco', 'sede_testa'), x, z, 'cov_testa_d', 'cov_tc', verso, TAGLIA)
    else:
        for nome_s, x in (('vite_a', 'zam_Lc + fem_blocco_x0 + fem_ins_dx'), ('vite_g', 'zam_Lc + zam_Lf - fem_blocco_dk - fem_ins_dx')):
            p.cilindro('y', y0, 'foro_' + nome_s, x, 'cov_vite_b_z', 'vite_m2_pass', 'cov_tc + 1 mm', verso, TAGLIA)
        corpo = comp.bRepBodies.item(0)
        r_foro, yb = v('vite_m2_pass') / 2, abs(v(y0))
        bordi = []
        for fa in corpo.faces:
            g = fa.geometry
            if g.surfaceType == adsk.core.SurfaceTypes.CylinderSurfaceType and abs(g.radius * 10 - r_foro) < 0.01:
                # bordo sulla faccia esterna bombata (non e' un cerchio), non quello sulla faccia interna piana
                bordi += [e for e in fa.edges if abs(e.pointOnEdge.y * 10) > yb + 0.5]
        if bordi:
            ch = comp.features.chamferFeatures
            ci = ch.createInput2()
            ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(_collezione(bordi), adsk.core.ValueInput.createByString('cov_svasatura'), False)
            cf = ch.add(ci)
            cf.name = 'svasature'
            p.n += 1
        svasati = len(bordi)
    p.info = {'svasature': svasati, 'spigoli_sagoma': n_sagoma, 'spigoli_finestre': len(spf), 'facce_toro': len(tori)}
    return occ, p


def fai_cover_femore_a(zampa):
    return _cover_femore(zampa, 'Cover_Femore_A', 'A')


def fai_cover_femore_b(zampa):
    return _cover_femore(zampa, 'Cover_Femore_B', 'B')


def fai_teste_a(zampa):
    """Ingombro delle teste M3 sul lato A (non si stampa): 8 sulle squadrette, 4 sul blocco. Serve alle verifiche tra
    zampe vicine e alle sedi della lama A (D-060)."""
    occ = _nuovo_comp(zampa, 'Ingombro_Teste_A')
    p = Parte(occ.component)
    teste = []
    for xc in ('zam_Lc', 'zam_Lc + zam_Lf'):
        teste += [(xc + ' + sq_fori_pcd / 2', '0 mm'), (xc + ' - sq_fori_pcd / 2', '0 mm'), (xc, 'sq_fori_pcd / 2'), (xc, '-(sq_fori_pcd / 2)')]
    teste += [(x, z) for _, x, z in _inserti_blocco()]
    for k, (x, z) in enumerate(teste):
        p.cilindro('y', 'zy_A_est', 'testa_%02d' % k, x, z, 'vite_m3_testa_d', 'vite_m3_testa_h', 1, NUOVO)
    return occ, p


def _inserti_blocco():
    """Quattro inserti M3 per la piastra A, negli angoli del blocco lontani dagli smussi."""
    x0, x1 = 'zam_Lc + fem_blocco_x0 + fem_ins_dx', 'zam_Lc + zam_Lf - fem_blocco_dk - fem_ins_dx'
    z0, z1 = 'fem_ins_dx - fem_blocco_giu + 2 mm', 'fem_blocco_su - fem_ins_dx - 2.6 mm'
    # lato ginocchio a Z 6,0 e 13,4: con 5,4 di interasse le rondelle di registro (Ø7) si sovrapponevano (D-060)
    return [('ins_blocco_ab', x0, z0), ('ins_blocco_aa', x0, z1), ('ins_blocco_gb', x1, z0 + ' + 1.5 mm'),
            ('ins_blocco_ga', x1, z1 + ' + 0.5 mm')]


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


def _interseca(p, sk, asse, dist_expr, verso, nome, corpi=None):
    """Estrusione in intersezione dell'unico profilo dello schizzo, limitata ai corpi della parte (o a quelli dati)."""
    ext = p.c.features.extrudeFeatures
    inp = ext.createInput(sk.profiles.item(0), adsk.fusion.FeatureOperations.IntersectFeatureOperation)
    nrm = sk.xDirection.crossProduct(sk.yDirection)
    positivo = ({'x': nrm.x, 'y': nrm.y, 'z': nrm.z}[asse] > 0) == (verso > 0)
    inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString(dist_expr)),
                         adsk.fusion.ExtentDirections.PositiveExtentDirection if positivo
                         else adsk.fusion.ExtentDirections.NegativeExtentDirection)
    inp.participantBodies = corpi if corpi is not None else [b for b in p.c.bRepBodies]
    f = ext.add(inp)
    f.name = nome
    p.n += 1
    return f


def _stinco(p, xk, fine='zam_Lt - tib_piede_sp'):
    """Stinco V2 allargato (D-061), costruito per primo e da solo: i tagli e le intersezioni toccano solo lui."""
    yq = 'tib_y_c - tib_y_semi_alto - 1 mm'
    largo = '2 * tib_y_semi_alto + 2 mm'
    p.blocco('y', 'tib_y_c - tib_y_semi_alto', 'stinco', xk + ' - tib_x_meno_alto', '-(%s)' % fine, xk + ' + cul_semi',
             '-(bug_coda)', '2 * tib_y_semi_alto', 1, NUOVO)
    # fianco -X: da 6 a 4 dall'asse, dritto
    p.blocco_obl('y', yq, 'fianco_meno_x', (xk + ' - tib_x_meno_alto', '-(bug_coda)'), (xk + ' - tib_x_meno_basso', '-(tib_z_arco)'),
                 '-(20 mm)', '100 mm', '-(20 mm)', '0 mm', largo, 1, TAGLIA)
    # fianco +X: arco tangente alla faccia dello zoccolo, fino a 4 dall'asse alla fine dell'arco
    sk = p.sk_cerchio('y', yq, 'arco_piu_x', xk + ' + cul_semi - tib_arco_R', '-(bug_coda)', '2 * tib_arco_R')
    _interseca(p, sk, 'y', largo, 1, 'arco_piu_x')
    # fianchi Y simmetrici sul piano medio dello zoccolo, a filo dello zoccolo in alto e dritti fino alla punta (nel piano
    # 'x' (u, v) = (y, z); b = a ruotato di +90 gradi: sul fianco -Y punta dentro, sul fianco +Y fuori)
    p.blocco_obl('x', xk + ' - 20 mm', 'rastremazione_y_meno', ('tib_y_c - tib_y_semi_alto', '-(bug_coda)'),
                 ('tib_y_c - tib_y_semi_basso', '-(tib_z_arco)'), '-(20 mm)', '100 mm', '-(20 mm)', '0 mm', '40 mm', 1, TAGLIA)
    p.blocco_obl('x', xk + ' - 20 mm', 'rastremazione_y_piu', ('tib_y_c + tib_y_semi_alto', '-(bug_coda)'),
                 ('tib_y_c + tib_y_semi_basso', '-(tib_z_arco)'), '-(20 mm)', '100 mm', '0 mm', '20 mm', '40 mm', 1, TAGLIA)
    corpo = p.c.bRepBodies.item(0)
    arco = [fa for fa in corpo.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.CylinderSurfaceType][0]
    lati = [e for e in arco.edges if abs(e.startVertex.geometry.z - e.endVertex.geometry.z) * 10 > 10]
    ch = p.c.features.chamferFeatures
    ci = ch.createInput2()
    ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(_collezione(lati), adsk.core.ValueInput.createByString('tib_smusso_piu'), False)
    cf = ch.add(ci)
    cf.name = 'smussi_piu_x'
    p.n += 1
    # punta piana per l'FSR (D-066): raccordato solo lo spigolo +X, dove si piega la coda del sensore
    corpo = p.c.bRepBodies.item(0)
    zt, xr = p.val(fine), p.val(xk)
    fondo = [e for e in corpo.edges if e.geometry.curveType == adsk.core.Curve3DTypes.Line3DCurveType
             and abs(e.startVertex.geometry.z * 10 + zt) < 0.05 and abs(e.endVertex.geometry.z * 10 + zt) < 0.05
             and abs(e.startVertex.geometry.x - e.endVertex.geometry.x) < 1e-5 and e.startVertex.geometry.x * 10 > xr]
    _raccorda(p.c, [('tib_punta_r_piu', fondo)], 'punta')
    return len(fondo), len(lati)


def _x_faccia(xk, z):
    """X della faccia +X dello stinco (arco del fianco) alla quota -z, per z da bug_coda alla punta."""
    return '(%s + cul_semi - tib_arco_R + sqrt(tib_arco_R ^ 2 - ((%s) - bug_coda) ^ 2))' % (xk, z)


def _taglio_faccia(p, xk, nome, z0, z1, y0, larghezza, prof, est0='0.5 mm', est1='0.5 mm', xa=None):
    """Taglio lungo la faccia +X ad arco dello stinco fra le quote -z0 e -z1 (z0 < z1): fondo sulla corda, profondo
    `prof` agli estremi (al centro in piu' la freccia dell'arco), da Y = y0 per `larghezza`; est0 ed est1 allungano la
    corda oltre gli estremi, cosi' i tratti di una gola fatta a corde si sovrappongono."""
    xa = xa or _x_faccia(xk, z0)
    xb = _x_faccia(xk, z1)
    corda = 'sqrt((%s - %s) ^ 2 + ((%s) - (%s)) ^ 2)' % (xa, xb, z1, z0)
    a0 = '-(%s)' % est0 if est0 != '0 mm' else '0 mm'
    # nel piano 'y' (u, v) = (x, z); la corda scende verso -Z e b (a ruotato di +90 gradi) punta verso +X, fuori
    return p.blocco_obl('y', y0, nome, ('%s - %s' % (xa, prof), '-(%s)' % z0), ('%s - %s' % (xb, prof), '-(%s)' % z1),
                        a0, '%s + %s' % (corda, est1), '0 mm', '%s + 3 mm' % prof, larghezza, 1, TAGLIA)


def fai_tibia(zampa):
    occ = _nuovo_comp(zampa, 'Tibia')
    p = Parte(occ.component)
    xk = 'zam_Lc + zam_Lf'
    n_punta, n_smussi = _stinco(p, xk, 'tib_punta_z')
    _culla(p, xk)
    _sede(p, xk)
    _alleggerisci_culla(p, xk, (1, -1))
    # due fessure tonde attraverso lo stinco, al centro tra i fianchi a meta' fessura (V2: X +3,2 e +2,5 dall'asse)
    for nome, z0, z1, w, dx in (('fessura_alta', '44 mm', '62 mm', '3.6 mm', '3.2 mm'), ('fessura_bassa', '67 mm', '83 mm', '2.8 mm', '2.5 mm')):
        xc = xk + ' + ' + dx
        p.blocco('y', 'tib_y_c - tib_y_semi_alto - 1 mm', nome, xc + ' - ' + w, '-(%s - %s)' % (z1, w), xc + ' + ' + w,
                 '-(%s + %s)' % (z0, w), '2 * tib_y_semi_alto + 2 mm', 1, TAGLIA)
        for k, z in (('a', '-(%s + %s)' % (z0, w)), ('b', '-(%s - %s)' % (z1, w))):
            p.cilindro('y', 'tib_y_c - tib_y_semi_alto - 1 mm', '%s_%s' % (nome, k), xc, z, '2 * ' + w, '2 * tib_y_semi_alto + 2 mm', 1, TAGLIA)
    # inserto M3 per la vite in basso del guscio, dalla faccia +X dello stinco (sull'arco) verso -X; parte dalla faccia
    # all'altezza del bordo alto del foro: dal centro, la meta' alta restava coperta da una pelle di 0,3 mm
    xv = _x_faccia(xk, 'cov_tib_vite_z - ins_m3_d / 2')
    p.cilindro('x', xv, 'ins_guscio', 'tib_y_c', '-(cov_tib_vite_z)', 'ins_m3_d', 'ins_m3_l', -1, TAGLIA)
    # FSR (X5, D-066): tasca per linguette e saldature dentro il piedino, poi gola dei fili fino al fondo della culla
    # (non oltre: la parete della culla e' di 2), fatta a corde dell'arco; solo nella Tibia, non in _stinco, altrimenti
    # il piedino le copierebbe e il TPU schiaccerebbe i fili
    _taglio_faccia(p, xk, 'tasca_fsr', 'tib_tasca_z0 - tib_tasca_h', 'tib_tasca_z0', 'tib_tasca_y - tib_tasca_w / 2',
                   'tib_tasca_w', 'tib_tasca_p', '0 mm', '0 mm')
    yg = 'tib_gola_y - tib_gola_w / 2'
    quote = ['tib_tasca_z0', '(bug_coda + (tib_tasca_z0 - bug_coda) * 2 / 3)', '(bug_coda + (tib_tasca_z0 - bug_coda) / 3)', 'bug_coda']
    for k in range(3):
        _taglio_faccia(p, xk, 'gola_fsr_%d' % k, quote[k + 1], quote[k], yg, 'tib_gola_w', 'tib_gola_p')
    p.blocco('y', yg, 'gola_fsr_zoccolo', xk + ' + cul_semi - tib_gola_p', '-(bug_coda)', xk + ' + cul_semi + 1 mm', '-(cul_coda)',
             'tib_gola_w', 1, TAGLIA)
    # luci (X31, predisposizione): sede piana per la striscia sotto la finestra del guscio, dal fondo della culla
    _taglio_faccia(p, xk, 'sede_luce', 'luc_tib_z0', 'luc_tib_z1', 'tib_y_c - luc_tib_w / 2', 'luc_tib_w', 'luc_tib_p',
                   '0 mm', '0.5 mm', xa=xk + ' + cul_semi')
    p.info = {'spigoli_punta': n_punta, 'spigoli_smussati': n_smussi, 'corpi': occ.component.bRepBodies.count}
    return occ, p


def fai_cover_tibia(zampa):
    """Guscio lungo della tibia (PETG bianco): dal ginocchio fin quasi al piede, fronte convesso, sezione a C con smussi
    a 45 gradi, aperto dietro; due tappi a rombo nelle finestre della parete +X della culla e una vite M3 in basso."""
    occ = _nuovo_comp(zampa, 'Cover_Tibia')
    p = Parte(occ.component)
    comp = occ.component
    xk = 'zam_Lc + zam_Lf'
    xmax = xk + ' + cul_semi + cov_tib_sporgenza'
    # simmetrico sul piano della zampa come lo stinco (D-065): il fianco +Y passa fuori dalla cassa del servo
    y0, y1 = '(zy_fondo_est - cov_tib_gio - cov_tib_sp)', '-(zy_fondo_est - cov_tib_gio - cov_tib_sp)'
    # profilo laterale: blocco dal centro dello stinco al fronte, intersecato con il cilindro del fronte convesso
    p.blocco('y', y0 + ' - 1 mm', 'pieno', xk, '-(cov_tib_z1)', xmax + ' + 2 mm', 'cov_tib_z0', y1 + ' - (' + y0 + ') + 2 mm', 1, NUOVO)
    sk = p.sk_cerchio('y', y0 + ' - 2 mm', 'fronte', xmax + ' - cov_tib_R', '-(cov_tib_zmax)', '2 * cov_tib_R')
    _interseca(p, sk, 'y', y1 + ' - (' + y0 + ') + 4 mm', 1, 'fronte_convesso')
    # sagoma frontale simmetrica sul piano medio dello zoccolo: fianchi dritti fino allo zoccolo, poi rastremati come lo stinco
    p.blocco('x', xk + ' - 1 mm', 'taglio_y_piu', y1, '-(cov_tib_z1) - 1 mm', y1 + ' + 10 mm', 'cov_tib_z0 + 1 mm', '30 mm', 1, TAGLIA)
    p.blocco('x', xk + ' - 1 mm', 'taglio_y_meno', y0 + ' - 10 mm', '-(cov_tib_z1) - 1 mm', y0, 'cov_tib_z0 + 1 mm', '30 mm', 1, TAGLIA)
    p.blocco_obl('x', xk + ' - 1 mm', 'rastremazione_meno', (y0, '-(bug_coda)'), ('tib_y_c - cov_tib_y_semi_basso', '-(cov_tib_z1)'),
                 '-(20 mm)', '100 mm', '-(20 mm)', '0 mm', '30 mm', 1, TAGLIA)
    p.blocco_obl('x', xk + ' - 1 mm', 'rastremazione_piu', (y1, '-(bug_coda)'), ('tib_y_c + cov_tib_y_semi_basso', '-(cov_tib_z1)'),
                 '-(20 mm)', '100 mm', '0 mm', '20 mm', '30 mm', 1, TAGLIA)
    corpo = comp.bRepBodies.item(0)
    fronte = [fa for fa in corpo.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.CylinderSurfaceType][0]
    z0v, z1v = p.val('cov_tib_z0'), -p.val('cov_tib_z1')
    lunghi = []
    for e in fronte.edges:
        a, b = e.startVertex.geometry, e.endVertex.geometry
        if abs(a.z - b.z) * 10 > 5:                        # gli spigoli lungo la tibia, non quelli in cima e in fondo
            lunghi.append(e)
    ch = comp.features.chamferFeatures
    ci = ch.createInput2()
    ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(_collezione(lunghi), adsk.core.ValueInput.createByString('cov_tib_smusso'), True)
    cf = ch.add(ci)
    cf.name = 'smussi_fronte'
    p.n += 1
    corpo = comp.bRepBodies.item(0)
    xr = p.val(xk)
    togli = [fa for fa in corpo.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType and
             (abs(fa.pointOnFace.x * 10 - xr) < 0.01 or abs(fa.pointOnFace.z * 10 - z0v) < 0.01 or abs(fa.pointOnFace.z * 10 - z1v) < 0.01)]
    p.svuota(togli, 'cov_tib_sp', 'guscio')
    # niente fianchi vicino alle teste del femore (piastre, squadretta e mozzo girano attorno all'asse del ginocchio)
    p.blocco('y', y1 + ' - 2 mm', 'via_fianco_piu', xk + ' - 20 mm', '-(16 mm)', xk + ' + cul_semi + 1.5 mm', 'cov_tib_z0 + 1 mm',
             '3 mm', 1, TAGLIA)
    p.blocco('y', y0 + ' - 1 mm', 'via_fianco_meno', xk + ' - 20 mm', '-(16 mm)', xk + ' + cul_semi + 1.5 mm', 'cov_tib_z0 + 1 mm',
             '3 mm', 1, TAGLIA)
    # tappi a rombo nelle finestre della parete +X della culla (dentro la parete del fronte, fino a 1,6 nella finestra)
    # la cima dei tappi sta dentro lo spessore del fronte (piu' in basso il fronte e' piu' sporgente): segue la sporgenza
    for k, (zc, xt) in enumerate((('-(cul_fin_z1)', xmax + ' - 2.5 mm'), ('-(cul_fin_z2)', xmax + ' - 1.2 mm'))):
        p.blocco_obl('x', xt, 'tappo_%d' % k, ('cul_fin_y', zc), ('cul_fin_y + 1 mm', zc + ' + 1 mm'),
                     '-(cul_fin_lato / 2 - 0.2 mm)', 'cul_fin_lato / 2 - 0.2 mm', '-(cul_fin_lato / 2 - 0.2 mm)', 'cul_fin_lato / 2 - 0.2 mm',
                     '(%s) - (%s + cul_semi - cul_parete + 0.4 mm)' % (xt, xk), -1)
    # vite in basso: bossolo dallo stinco al fronte e foro passante. Lo stinco e' ad arco: il bossolo parte dal punto
    # piu' sporgente della faccia sotto di lui (3,5 mm sopra la vite), cosi' non entra nello stinco
    xs = xk + ' + cul_semi - tib_arco_R + sqrt(tib_arco_R ^ 2 - (cov_tib_vite_z - 3.5 mm - bug_coda) ^ 2) + 0.05 mm'
    p.cilindro('x', xs, 'bossolo_vite', 'tib_y_c', '-(cov_tib_vite_z)', '7 mm', '2.5 mm', 1)        # finisce dentro la parete del fronte
    p.cilindro('x', xs, 'foro_vite', 'tib_y_c', '-(cov_tib_vite_z)', 'vite_m3_pass', '12 mm', 1, TAGLIA)
    # finestra lunga sul fronte
    yc = '-(cov_tib_fin_y)'
    xf = xk + ' + 8 mm'
    p.blocco('x', xf, 'finestra', yc + ' - cov_tib_fin_w / 2', '-(cov_tib_fin_z1 - cov_tib_fin_w / 2)', yc + ' + cov_tib_fin_w / 2',
             '-(cov_tib_fin_z0 + cov_tib_fin_w / 2)', '30 mm', 1, TAGLIA)
    for k, z in (('a', '-(cov_tib_fin_z0 + cov_tib_fin_w / 2)'), ('b', '-(cov_tib_fin_z1 - cov_tib_fin_w / 2)')):
        p.cilindro('x', xf, 'finestra_' + k, yc, z, 'cov_tib_fin_w', '30 mm', 1, TAGLIA)
    p.info = {'spigoli_smussati': len(lunghi), 'facce_tolte': len(togli), 'corpi': comp.bRepBodies.count}
    return occ, p


def fai_piedino(zampa):
    """Piedino in TPU 95A arancio (D9): calza la punta dello stinco dal bordo del guscio in giu'. Si rifa' lo stinco con le
    stesse lavorazioni, si toglie tutto sopra il bordo e si svuota verso l'esterno: dentro e' lo stinco esatto (stretta da
    tarare sul provino), fuori una parete uniforme che porta la suola a zam_Lt."""
    occ = _nuovo_comp(zampa, 'Piedino')
    p = Parte(occ.component)
    xk = 'zam_Lc + zam_Lf'
    _stinco(p, xk)
    p.blocco('z', '-(tib_piede_z0)', 'taglio_alto', xk + ' - 30 mm', '-(40 mm)', xk + ' + 30 mm', '40 mm', '60 mm', 1, TAGLIA)
    corpo = occ.component.bRepBodies.item(0)
    z0 = -p.val('tib_piede_z0')
    bocca = [fa for fa in corpo.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType
             and abs(fa.pointOnFace.z * 10 - z0) < 0.01]
    sh = occ.component.features.shellFeatures
    inp = sh.createInput(_collezione(bocca), False)
    inp.insideThickness = adsk.core.ValueInput.createByString('0 mm')
    inp.outsideThickness = adsk.core.ValueInput.createByString('tib_piede_sp')
    f = sh.add(inp)
    f.name = 'calza'
    p.n += 1
    # FSR (D-066): la punta della tibia finisce 0,8 sopra il fondo (FSR 0,3 + pistoncino 0,5); il pistoncino sta sulla
    # suola sotto il centro della testa. Fuori i raccordi sono quelli dello svuotamento (1,6 sul lato -X, 2,6 sul +X):
    # piu' grandi assottiglierebbero la parete sotto 1,2 allo spigolo vivo -X della punta
    p.cilindro('z', '-(zam_Lt - tib_piede_sp)', 'pistoncino', xk + ' + sen_fsr_dx', 'tib_y_c', 'tib_pistone_d', 'tib_pistone_sp', 1)
    p.blocco('y', 'tib_gola_y - pied_tacca / 2', 'tacca_fili', xk, '-(tib_piede_z0 + pied_tacca)', xk + ' + 20 mm',
             '-(tib_piede_z0) + 1 mm', 'pied_tacca', 1, TAGLIA)
    corpo = occ.component.bRepBodies.item(0)
    bb = corpo.boundingBox
    p.info = {'bocca': len(bocca), 'corpi': occ.component.bRepBodies.count, 'volume_cm3': round(corpo.volume, 3),
              'z_min': round(bb.minPoint.z * 10, 2), 'z_max': round(bb.maxPoint.z * 10, 2)}
    return occ, p


def fai_cover_tibia_diffusore(zampa):
    """Diffusore delle luci della tibia (X31, D-066): lastra sottile che segue l'interno del fronte del guscio dietro la
    finestra lunga, con un bordino che entra a incastro nella finestra. Si monta solo con le luci: senza, la finestra
    resta aperta come prima. Si costruiscono due corpi (bordino e lastra) sui cilindri del fronte e poi si uniscono."""
    occ = _nuovo_comp(zampa, 'Cover_Tibia_Diffusore')
    p = Parte(occ.component)
    comp = occ.component
    xk = 'zam_Lc + zam_Lf'
    cx = xk + ' + cul_semi + cov_tib_sporgenza - cov_tib_R'          # centro del fronte convesso (fai_cover_tibia)
    cz = '-(cov_tib_zmax)'
    r_int = '(cov_tib_R - cov_tib_sp)'                                # faccia interna del fronte
    yc, w = '-(cov_tib_fin_y)', 'cov_tib_fin_w'
    za, zb = 'cov_tib_fin_z0 + %s / 2' % w, 'cov_tib_fin_z1 - %s / 2' % w   # centri delle estremita' tonde
    ys = '(%s / 2 - luc_dif_gio)' % w                                 # semilarghezza del bordino
    yi = '(%s / 2 - luc_dif_gio - luc_dif_parete)' % w
    # bordino: asola esterna, tagliata fra la faccia interna del fronte e 0,6 sotto quella esterna, poi svuotata
    p.blocco('x', xk, 'bordino', '%s - %s' % (yc, ys), '-(%s)' % zb, '%s + %s' % (yc, ys), '-(%s)' % za, '30 mm', 1, NUOVO)
    for k, z in (('a', '-(%s)' % za), ('b', '-(%s)' % zb)):
        p.cilindro('x', xk, 'bordino_' + k, yc, z, '2 * ' + ys, '30 mm', 1)
    sk = p.sk_cerchio('y', '%s - 10 mm' % yc, 'bordino_cima', cx, cz, '2 * (%s + luc_dif_h)' % r_int)
    _interseca(p, sk, 'y', '20 mm', 1, 'bordino_cima')
    p.cilindro('y', '%s - 10 mm' % yc, 'bordino_fondo', cx, cz, '2 * ' + r_int, '20 mm', 1, TAGLIA)
    p.blocco('x', xk, 'bordino_vuoto', '%s - %s' % (yc, yi), '-(%s)' % zb, '%s + %s' % (yc, yi), '-(%s)' % za, '30 mm', 1, TAGLIA)
    for k, z in (('a', '-(%s)' % za), ('b', '-(%s)' % zb)):
        p.cilindro('x', xk, 'bordino_vuoto_' + k, yc, z, '2 * ' + yi, '30 mm', 1, TAGLIA)
    bordino = comp.bRepBodies.item(0)
    # lastra contro la faccia interna del fronte, oltre il bordo della finestra
    p.blocco('y', '%s - %s / 2 - luc_dif_bordo' % (yc, w), 'lastra', xk, '-(cov_tib_fin_z1 + luc_dif_bordo)', xk + ' + 30 mm',
             '-(cov_tib_fin_z0 - luc_dif_bordo)', '%s + 2 * luc_dif_bordo' % w, 1, NUOVO)
    lastra = [b for b in comp.bRepBodies if b != bordino][0]
    sk = p.sk_cerchio('y', '%s - 10 mm' % yc, 'lastra_fuori', cx, cz, '2 * ' + r_int)
    _interseca(p, sk, 'y', '20 mm', 1, 'lastra_fuori', corpi=[lastra])
    p.cilindro('y', '%s - 10 mm' % yc, 'lastra_dentro', cx, cz, '2 * (%s - luc_dif_sp)' % r_int, '20 mm', 1, TAGLIA)
    corpi = list(comp.bRepBodies)
    cb = comp.features.combineFeatures
    inp = cb.createInput(corpi[0], _collezione(corpi[1:]))
    inp.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    f = cb.add(inp)
    f.name = 'unione'
    p.n += 1
    corpo = comp.bRepBodies.item(0)
    p.info = {'corpi': comp.bRepBodies.count, 'volume_cm3': round(corpo.volume, 4)}
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
    ('FSR', 'Rif_FSR_400', ('zam_Lc + zam_Lf + sen_fsr_dx', '0 mm', '-(tib_punta_z + sen_fsr_sp)'), ((1, 0, 0), (0, 1, 0), (0, 0, 1))),
]
# (nome del giunto, parte che si muove, parte fissa)
RIGIDI = [
    ('R_ponte', 'Coxa_Ponte', 'Coxa'), ('R_servo_femore', 'Servo_Femore', 'Coxa'),
    ('R_cuscinetto_femore', 'Cuscinetto_Femore', 'Coxa'), ('R_perno_coxa', 'Perno_Coxa', 'Coxa'),
    ('R_squadretta_coxa', 'Squadretta_Coxa', 'Coxa_Ponte'), ('R_femore_a', 'Femore_A', 'Femore_B'),
    ('R_squadretta_femore', 'Squadretta_Femore', 'Femore_A'), ('R_squadretta_ginocchio', 'Squadretta_Ginocchio', 'Femore_A'),
    ('R_perno_femore', 'Perno_Femore', 'Femore_B'), ('R_perno_ginocchio', 'Perno_Ginocchio', 'Femore_B'),
    ('R_servo_ginocchio', 'Servo_Ginocchio', 'Tibia'), ('R_cuscinetto_ginocchio', 'Cuscinetto_Ginocchio', 'Tibia'),
    ('R_teste_a', 'Ingombro_Teste_A', 'Femore_A'),
    ('R_cover_femore_a', 'Cover_Femore_A', 'Femore_A'), ('R_cover_femore_b', 'Cover_Femore_B', 'Femore_B'),
    ('R_cover_tibia', 'Cover_Tibia', 'Tibia'),
    ('R_piedino', 'Piedino', 'Tibia'),
    ('R_diffusore', 'Cover_Tibia_Diffusore', 'Cover_Tibia'),
    ('R_fsr', 'FSR', 'Tibia'),
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
    # vale solo con la prima Zampa all'origine (prima dell'assieme): con le zampe montate usare istanze_mancanti
    lib = {o.component.name: o for o in root.occurrences if o.component.name.startswith('Rif_')}
    gia = [o for o in zampa.component.occurrences if o.component.name.startswith('Rif_')]
    for o in gia:
        o.deleteMe()
    fatte = []
    for chiave, (nome_lib, m) in _pose(des).items():
        A['aggiungi_istanza'](root, lib[nome_lib], m, dentro=zampa)
        fatte.append(chiave)
    return {'cancellate': len(gia), 'create': fatte}


def fai_istanze_mancanti(des, root, zampa):
    """Crea solo le istanze di ISTANZE che mancano, senza toccare le altre: alla radice nella posa in terna del robot
    (posa nella zampa composta con la prima istanza di Zampa, montata e ruotata sul corpo) e poi spostate nella Zampa,
    che conserva la posizione. Creandole direttamente nella zampa nascono fuori posto (CLAUDE.md)."""
    lib = {o.component.name: o for o in root.occurrences if o.component.name.startswith('Rif_')}
    presenti = _istanze(zampa)
    fatte = []
    for chiave, (nome_lib, m) in _pose(des).items():
        o = presenti.get(chiave)
        if o is not None:
            t, a = o.transform2.translation, m.translation
            if math.dist((t.x, t.y, t.z), (a.x, a.y, a.z)) * 10 < 1.0:
                continue
        mr = m.copy()
        mr.transformBy(zampa.transform2)
        A['aggiungi_istanza'](root, lib[nome_lib], mr, dentro=zampa)
        fatte.append(chiave)
    return fatte


def fai_giunti_mancanti(des, zampa):
    """Aggiunge solo i giunti rigidi di RIGIDI che mancano (fai_giunti li rifa' tutti)."""
    comp = zampa.component
    nomi = {j.name for j in comp.asBuiltJoints}
    occ = _istanze(zampa)
    fatti = []
    for nome, a, b in RIGIDI:
        if nome not in nomi:
            A['giunto_rigido'](comp, occ[a], occ[b], nome)
            fatti.append(nome)
    return fatti


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


# Campo libero misurato con i giunti veri il 9 ottobre 2026, dopo la revisione (senza corpo): femore da -49 a +85,
# ginocchio fino a 180. Il minimo del ginocchio dipende dal femore (GAMMA_MIN, gioco zero): lo limita il firmware.
LIMITI = {'alpha': (-49.0, 85.0), 'gamma': (29.0, 180.0)}
GAMMA_MIN = {-45: 54, -40: 55, -35: 45, -30: 46, -25: 46, -20: 46, -15: 45, -10: 44, -5: 43, 0: 43, 5: 41, 10: 39,
             15: 39, 20: 37, 25: 35, 30: 33, 35: 31, 40: 29, 85: 29}


def gamma_min(alpha):
    """Ginocchio minimo della tabella per il femore ad alpha: fra due righe il massimo dei due (la tabella non e' monotona)."""
    k = sorted(GAMMA_MIN)
    for a0, a1 in zip(k, k[1:]):
        if alpha == a0:
            return GAMMA_MIN[a0]
        if a0 < alpha < a1:
            return max(GAMMA_MIN[a0], GAMMA_MIN[a1])
    return GAMMA_MIN[k[-1]]


def pose_scansione():
    """(pose che devono essere libere, controlli che devono toccare). Pose: alpha a passi di 5 da -45 a 85 con gamma
    al minimo della tabella, a 150 e a 180. Controlli: gamma minimo - 2 a ogni riga della tabella e il femore a -50."""
    pose = [(float(a), float(g)) for a in range(-45, 90, 5) for g in (gamma_min(a), 150, 180)]
    controlli = [(float(a), float(g) - 2.0) for a, g in sorted(GAMMA_MIN.items())] + [(-50.0, 90.0)]
    return pose, controlli


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
        V['controlla'](app)
        root = des.rootComponent
        if 'parametri' in passi:
            out['parametri'] = L['aggiungi_parametri'](des, PARAMETRI)
        zampa = _zampa(root)
        for nome, f in (('coxa', fai_coxa), ('ponte', fai_ponte), ('femore_b', fai_femore_b), ('femore_a', fai_femore_a),
                        ('tibia', fai_tibia), ('teste_a', fai_teste_a), ('cover_femore_a', fai_cover_femore_a),
                        ('cover_femore_b', fai_cover_femore_b), ('cover_tibia', fai_cover_tibia), ('piedino', fai_piedino),
                        ('diffusore', fai_cover_tibia_diffusore)):
            if nome in passi:
                occ, p = f(zampa)
                if occ.component.name in PUNTI:
                    p.info = dict(getattr(p, 'info', {}), punti=_punti(occ.component))
                out[nome] = _chiudi(des, occ.component.name, p)
                out[nome].update(getattr(p, 'info', {}))
        if 'punti' in passi:
            out['punti'] = {o.component.name: _punti(o.component) for o in zampa.component.occurrences if o.component.name in PUNTI}
        if 'istanze' in passi:
            out['istanze'] = fai_istanze(des, root, zampa)
        if 'istanze_mancanti' in passi:
            out['istanze_mancanti'] = fai_istanze_mancanti(des, root, zampa)
        if 'giunti_mancanti' in passi:
            out['giunti_mancanti'] = fai_giunti_mancanti(des, zampa)
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
            libere, controlli = pose_scansione()
            pose = kw.get('pose') or (libere if kw.get('quali') == 'libere' else controlli if kw.get('quali') == 'controlli'
                                      else libere + controlli)
            r = scansione(des, zampa, pose)
            esito = {'libere': [k for k, v in r.items() if v == 'libera'], 'urti': {k: v for k, v in r.items() if v != 'libera'}}
            if not kw.get('pose'):
                chiavi_c = {'%g/%g' % pc for pc in controlli}
                esito['riassunto'] = {'pose_libere': sum(1 for p in libere if '%g/%g' % p in esito['libere']),
                                      'pose': len(libere) if kw.get('quali') != 'controlli' else 0,
                                      'controlli_che_toccano': sum(1 for k in esito['urti'] if k in chiavi_c),
                                      'controlli': len(controlli) if kw.get('quali') != 'libere' else 0}
            out['scansione'] = esito
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
    return out
