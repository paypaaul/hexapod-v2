"""Zampa dell'esapode: parti progettate, istanze dei componenti comprati, giunti.

Si esegue dentro Fusion sul design "Hexapod v2 - Assieme":
    ns = runpy.run_path('<repo>/cad/script/zampa.py'); ns['main'](['parametri', 'coxa', ...])

Terna della zampa (componente "Zampa"): origine sull'asse della coxa, all'altezza dell'asse
del femore; X radiale verso l'esterno, Z in alto, Y lungo gli assi di femore e ginocchio.
Posa di riferimento del modello: femore orizzontale, tibia verticale verso il basso.

Parti (ognuna nella propria terna, tutte si stampano con la faccia -Y sul piano):
  Coxa       forcella attorno al servo della coxa + culla del servo del femore
  Femore_B   piastra lato perni + anima           (terna: origine sull'asse dell'anca, X lungo il femore)
  Femore_A   piastra lato squadrette, avvitata all'anima
  Tibia      culla del servo del ginocchio + piede (terna: origine sull'asse del ginocchio, X verso il piede)
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
Parte, NUOVO, UNISCI, TAGLIA = L['Parte'], L['NUOVO'], L['UNISCI'], L['TAGLIA']
P3 = adsk.core.Point3D.create
V3 = adsk.core.Vector3D.create

PARAMETRI = [
    # --- culla del servo
    ('cul_parete', '2 mm', 'mm', 'Culla: parete attorno al servo'),
    ('cul_fondo', '3.4 mm', 'mm', 'Culla: fondo sotto il servo (sede cuscinetto 2.2 + 1.2)'),
    ('srv_corto', 'srv_lung / 2 - srv_asse_offset', 'mm', 'Servo: asse albero -> estremita vicina (lato cavo)'),
    ('srv_coda', 'srv_lung / 2 + srv_asse_offset', 'mm', 'Servo: asse albero -> estremita lontana (coda)'),
    ('cul_semi', 'srv_larg / 2 + gio_servo + cul_parete', 'mm', 'Culla: semilarghezza esterna'),
    ('cul_corto', 'srv_corto + gio_servo + cul_parete', 'mm', 'Culla: asse -> esterno lato corto'),
    ('cul_lungo', 'srv_coda + gio_servo + cul_parete', 'mm', 'Culla: asse -> esterno lato coda'),
    ('ale_foro_corto', 'srv_fori_interasse / 2 - srv_asse_offset', 'mm', 'Asse -> foro aletta lato corto'),
    ('ale_foro_coda', 'srv_fori_interasse / 2 + srv_asse_offset', 'mm', 'Asse -> foro aletta lato coda'),
    ('ale_bugna', '6 mm', 'mm', 'Bugna sotto le alette: larghezza'),
    ('ale_bugna_l', '4.2 mm', 'mm', 'Bugna sotto le alette: sporgenza oltre la culla'),
    ('ale_bugna_h', '8 mm', 'mm', 'Bugna sotto le alette: altezza'),
    ('cavo_fin_l', '9 mm', 'mm', 'Finestra del cavo: larghezza (ci passa la spina JR da 7,9 mm)'),
    ('cavo_fin_y0', 'zy_srv + srv_cavo_alt - 1.5 mm', 'mm', 'Finestra del cavo: Y del bordo inferiore'),
    ('cavo_fin_h', 'zy_orlo - ale_bugna_h - cavo_fin_y0', 'mm', 'Finestra del cavo: altezza, fino sotto la bugna'),
    # --- cuscinetto e perno
    ('cus_sede_d', 'cus_D', 'mm', 'Sede cuscinetto: diametro nominale (interferenza da provino)'),
    ('cus_sede_prof', 'cus_B - cus_flangia_sp', 'mm', 'Sede cuscinetto: profondita (la flangia resta fuori)'),
    ('perno_foro', 'perno_d', 'mm', 'Foro del perno nella plastica: nominale (forzamento da provino)'),
    ('perno_passo', '3.4 mm', 'mm', 'Foro di passaggio del perno dietro il cuscinetto'),
    ('perno_sporge', '1.5 mm', 'mm', 'Sporgenza esterna del perno, per estrarlo'),
    # --- bracci della forcella
    ('arm_sp_perno', '4.8 mm', 'mm', 'Braccio lato perno: spessore'),
    ('arm_sp_sq', '3.2 mm', 'mm', 'Braccio lato squadretta: spessore'),
    ('arm_rialzo_d', '4.2 mm', 'mm', 'Rialzo che tocca solo l anello interno del cuscinetto: diametro'),
    ('arm_rialzo_h', 'gio_mobile', 'mm', 'Rialzo: altezza = gioco tra braccio e flangia'),
    # --- squadretta di serie (C: da misurare)
    ('sq_alt_sotto', '31 mm', 'mm', 'Squadretta: fondo servo -> lato inferiore del braccio (C)'),
    ('sq_sp', '1.6 mm', 'mm', 'Squadretta: spessore del braccio (C)'),
    ('sq_larg', '5.8 mm', 'mm', 'Squadretta: larghezza della sede (C)'),
    ('sq_braccio_l', '16.5 mm', 'mm', 'Squadretta: asse -> punta del braccio (C)'),
    ('sq_mozzo_d', '7.2 mm', 'mm', 'Squadretta: diametro del mozzo (C)'),
    ('sq_mozzo_sede', 'sq_mozzo_d + 0.2 mm', 'mm', 'Sede del mozzo: diametro'),
    ('sq_accesso_d', '4.5 mm', 'mm', 'Foro di accesso alla vite centrale'),
    # --- quote lungo Y della zampa (derivate, con segno)
    ('zam_semi_larg', '(sq_alt_sotto + arm_sp_sq + cul_fondo + cus_flangia_sp + arm_rialzo_h + arm_sp_perno) / 2', 'mm', 'Zampa: semilarghezza'),
    ('zy_sq_int', 'zam_semi_larg - arm_sp_sq', 'mm', 'Y faccia interna della piastra lato squadrette'),
    ('zy_srv', 'zy_sq_int - sq_alt_sotto', 'mm', 'Y fondo dei servo di femore e ginocchio'),
    ('zy_orlo', 'zy_srv + srv_alette_sotto', 'mm', 'Y orlo della culla (appoggio alette)'),
    ('zy_fondo', 'zy_srv - cul_fondo', 'mm', 'Y faccia esterna del fondo della culla'),
    ('zy_pn_int', 'zy_fondo - cus_flangia_sp - arm_rialzo_h', 'mm', 'Y faccia interna della piastra lato perni'),
    ('zy_pn_est', '-(zam_semi_larg)', 'mm', 'Y faccia esterna della piastra lato perni'),
    # --- coxa
    ('cox_z0', '7 mm', 'mm', 'Coxa: fondo del servo della coxa sotto l asse del femore'),
    ('cz_inf_su', '-(cox_z0 + cul_fondo + cus_flangia_sp + arm_rialzo_h)', 'mm', 'Z faccia superiore del braccio inferiore'),
    ('cz_inf_giu', 'cz_inf_su - arm_sp_perno', 'mm', 'Z faccia inferiore del braccio inferiore'),
    ('cz_sup_giu', 'sq_alt_sotto - cox_z0', 'mm', 'Z faccia inferiore del braccio superiore'),
    ('cz_sup_su', 'cz_sup_giu + arm_sp_sq', 'mm', 'Z faccia superiore del braccio superiore'),
    ('cox_web_x', '24.2 mm', 'mm', 'Coxa: X della faccia interna dell anima (oltre le alette del servo coxa)'),
    ('cox_arm_semi', '8 mm', 'mm', 'Coxa: semilarghezza dei bracci'),
    # --- femore
    ('fem_semi', '8 mm', 'mm', 'Femore: semilarghezza delle piastre'),
    ('fem_web_x0', '14 mm', 'mm', 'Femore: asse anca -> faccia vicina dell anima'),
    ('fem_web_sp', '6 mm', 'mm', 'Femore: spessore dell anima'),
    ('fem_web_semi', '7.5 mm', 'mm', 'Femore: semialtezza dell anima'),
    ('fem_vite_dz', '4.5 mm', 'mm', 'Femore: viti dell anima, distanza dalla mezzeria'),
    # L'anima piena fermava il ginocchio a 62 gradi e il femore a +25. Ora tra le due culle passa solo un
    # puntone inclinato, dentro la fascia che resta libera con il femore fino a +55 e il ginocchio fino a 50;
    # torna spessa (testa con gli inserti) solo accanto alla piastra delle squadrette, sopra la cassa dei servo.
    ('fem_testa_y0', 'zy_srv + srv_alt_cassa + 0.6 mm', 'mm', 'Femore: Y da cui parte la testa dell anima (sopra la cassa dei servo)'),
    ('fem_pun_ang', '35 deg', 'deg', 'Femore: inclinazione del puntone sull asse del femore'),
    ('fem_pun_cz', '1.46 mm', 'mm', 'Femore: centro del puntone sotto la mezzeria'),
    ('fem_pun_semi_l', '3.1 mm', 'mm', 'Femore: semilunghezza della sezione del puntone'),
    ('fem_pun_semi_sp', '2 mm', 'mm', 'Femore: semispessore della sezione del puntone'),
    # --- tibia
    ('tib_piede_semi', '5 mm', 'mm', 'Tibia: semilarghezza dello stinco'),
    ('tib_piede_d', '10 mm', 'mm', 'Tibia: diametro del piede'),
    ('tib_piede_semi_y', '6 mm', 'mm', 'Tibia: semispessore dello stinco lungo Y'),
]


T0 = {}


def _nuovo_comp(genitore, nome, matrice=None):
    """Crea il componente (cancellando quello esistente con lo stesso nome) e annota l'indice di timeline."""
    for o in L['trova_occ'](genitore, nome):
        o.deleteMe()
    T0[nome] = genitore.parentDesign.timeline.count
    occ = genitore.occurrences.addNewComponent(matrice or adsk.core.Matrix3D.create())
    occ.component.name = nome
    return occ


def _matrice(origine_mm, ex, ey, ez):
    m = adsk.core.Matrix3D.create()
    m.setWithCoordinateSystem(P3(origine_mm[0] / 10, origine_mm[1] / 10, origine_mm[2] / 10), V3(*ex), V3(*ey), V3(*ez))
    return m


def _zampa(root):
    occ = L['trova_occ'](root, 'Zampa')
    if occ:
        return occ[0]
    o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = 'Zampa'
    return o


# ----------------------------------------------------------------------------------- parti
def fai_coxa(zampa):
    occ = _nuovo_comp(zampa, 'Coxa')
    p = Parte(occ.component)
    # culla del servo del femore (asse lungo Y, lato lungo verticale, coda in alto)
    p.blocco('y', 'zy_fondo', 'culla', 'zam_Lc - cul_semi', '-(cul_corto)', 'zam_Lc + cul_semi', 'cul_lungo',
             'zy_orlo - zy_fondo', 1, NUOVO)
    p.blocco('y', 'zy_orlo - ale_bugna_h', 'bugna_bassa', 'zam_Lc - ale_bugna / 2', '-(cul_corto + ale_bugna_l)',
             'zam_Lc + ale_bugna / 2', '-(cul_corto)', 'ale_bugna_h')
    p.blocco('y', 'zy_orlo - ale_bugna_h', 'bugna_alta', 'zam_Lc - ale_bugna / 2', 'cul_lungo',
             'zam_Lc + ale_bugna / 2', 'cul_lungo + ale_bugna_l', 'ale_bugna_h')
    # anima verticale e bracci della forcella attorno al servo della coxa
    p.blocco('z', 'cz_inf_giu', 'anima', 'cox_web_x', 'zy_fondo', 'zam_Lc - cul_semi', 'cox_arm_semi',
             'cz_sup_su - cz_inf_giu')
    p.blocco('z', 'cz_inf_giu', 'braccio_inf', '0 mm', '-(cox_arm_semi)', 'cox_web_x', 'cox_arm_semi', 'arm_sp_perno')
    p.cilindro('z', 'cz_inf_giu', 'braccio_inf_testa', '0 mm', '0 mm', '2 * cox_arm_semi', 'arm_sp_perno')
    p.blocco('z', 'cz_sup_giu', 'braccio_sup', '0 mm', '-(cox_arm_semi)', 'cox_web_x', 'cox_arm_semi', 'arm_sp_sq')
    p.cilindro('z', 'cz_sup_giu', 'braccio_sup_testa', '0 mm', '0 mm', '2 * cox_arm_semi', 'arm_sp_sq')
    p.cilindro('z', 'cz_inf_su', 'rialzo_perno', '0 mm', '0 mm', 'arm_rialzo_d', 'arm_rialzo_h')
    # lavorazioni del giunto della coxa
    p.cilindro('z', 'cz_inf_giu', 'foro_perno', '0 mm', '0 mm', 'perno_foro', 'arm_sp_perno + arm_rialzo_h', 1, TAGLIA)
    p.blocco('z', 'cz_sup_giu', 'sede_squadretta', '-(cox_arm_semi)', '-(sq_larg / 2)', 'sq_braccio_l', 'sq_larg / 2',
             'sq_sp', 1, TAGLIA)
    p.blocco('z', 'cz_sup_giu', 'ingresso_squadretta', '-(cox_arm_semi)', '-(sq_mozzo_sede / 2)', '0 mm', 'sq_mozzo_sede / 2',
             'sq_sp', 1, TAGLIA)
    p.cilindro('z', 'cz_sup_giu', 'sede_mozzo', '0 mm', '0 mm', 'sq_mozzo_sede', 'sq_sp', 1, TAGLIA)
    p.cilindro('z', 'cz_sup_giu', 'foro_vite_centrale', '0 mm', '0 mm', 'sq_accesso_d', 'arm_sp_sq', 1, TAGLIA)
    # sede del servo del femore, cuscinetto, viti delle alette
    p.blocco('y', 'zy_srv', 'sede_servo', 'zam_Lc - srv_larg / 2 - gio_servo', '-(srv_corto + gio_servo)',
             'zam_Lc + srv_larg / 2 + gio_servo', 'srv_coda + gio_servo', 'zy_orlo - zy_srv', 1, TAGLIA)
    p.blocco('y', 'cavo_fin_y0', 'finestra_cavo', 'zam_Lc - cavo_fin_l / 2', '-(cul_corto)', 'zam_Lc + cavo_fin_l / 2', '-(srv_corto)',
             'cavo_fin_h', 1, TAGLIA)
    p.cilindro('y', 'zy_fondo', 'sede_cuscinetto', 'zam_Lc', '0 mm', 'cus_sede_d', 'cus_sede_prof', 1, TAGLIA)
    p.cilindro('y', 'zy_fondo', 'passaggio_perno', 'zam_Lc', '0 mm', 'perno_passo', 'cul_fondo', 1, TAGLIA)
    p.cilindro('y', 'zy_orlo', 'foro_aletta_basso', 'zam_Lc', '-(ale_foro_corto)', 'vite_m2_passante', 'ale_bugna_h', -1, TAGLIA)
    p.cilindro('y', 'zy_orlo', 'foro_aletta_alto', 'zam_Lc', 'ale_foro_coda', 'vite_m2_passante', 'ale_bugna_h', -1, TAGLIA)
    return occ, p


def fai_femore_b(zampa, m):
    occ = _nuovo_comp(zampa, 'Femore_B', m)
    p = Parte(occ.component)
    p.blocco('y', 'zy_pn_est', 'piastra', '0 mm', '-(fem_semi)', 'zam_Lf', 'fem_semi', 'arm_sp_perno', 1, NUOVO)
    p.cilindro('y', 'zy_pn_est', 'testa_anca', '0 mm', '0 mm', '2 * fem_semi', 'arm_sp_perno')
    p.cilindro('y', 'zy_pn_est', 'testa_ginocchio', 'zam_Lf', '0 mm', '2 * fem_semi', 'arm_sp_perno')
    p.cilindro('y', 'zy_pn_int', 'rialzo_anca', '0 mm', '0 mm', 'arm_rialzo_d', 'arm_rialzo_h')
    p.cilindro('y', 'zy_pn_int', 'rialzo_ginocchio', 'zam_Lf', '0 mm', 'arm_rialzo_d', 'arm_rialzo_h')
    centro = ('zam_Lf / 2', '-(fem_pun_cz)')
    verso = ('zam_Lf / 2 + 10 mm * cos(fem_pun_ang)', '10 mm * sin(fem_pun_ang) - fem_pun_cz')
    p.blocco_obl('y', 'zy_pn_int', 'puntone', centro, verso, '-(fem_pun_semi_l)', 'fem_pun_semi_l', '-(fem_pun_semi_sp)',
                 'fem_pun_semi_sp', 'fem_testa_y0 - zy_pn_int')
    p.blocco('y', 'fem_testa_y0', 'testa_anima', 'fem_web_x0', '-(fem_web_semi)', 'fem_web_x0 + fem_web_sp', 'fem_web_semi',
             'zy_sq_int - fem_testa_y0')
    p.cilindro('y', 'zy_pn_est', 'foro_perno_anca', '0 mm', '0 mm', 'perno_foro', 'arm_sp_perno + arm_rialzo_h', 1, TAGLIA)
    p.cilindro('y', 'zy_pn_est', 'foro_perno_ginocchio', 'zam_Lf', '0 mm', 'perno_foro', 'arm_sp_perno + arm_rialzo_h', 1, TAGLIA)
    p.cilindro('y', 'zy_sq_int', 'inserto_su', 'fem_web_x0 + fem_web_sp / 2', 'fem_vite_dz', 'ins_m2_d', 'ins_m2_l', -1, TAGLIA)
    p.cilindro('y', 'zy_sq_int', 'inserto_giu', 'fem_web_x0 + fem_web_sp / 2', '-(fem_vite_dz)', 'ins_m2_d', 'ins_m2_l', -1, TAGLIA)
    return occ, p


def fai_femore_a(zampa, m):
    occ = _nuovo_comp(zampa, 'Femore_A', m)
    p = Parte(occ.component)
    p.blocco('y', 'zy_sq_int', 'piastra', '0 mm', '-(fem_semi)', 'zam_Lf', 'fem_semi', 'arm_sp_sq', 1, NUOVO)
    p.cilindro('y', 'zy_sq_int', 'testa_anca', '0 mm', '0 mm', '2 * fem_semi', 'arm_sp_sq')
    p.cilindro('y', 'zy_sq_int', 'testa_ginocchio', 'zam_Lf', '0 mm', '2 * fem_semi', 'arm_sp_sq')
    p.blocco('y', 'zy_sq_int', 'sede_sq_anca', '-(sq_larg / 2)', '-(sq_larg / 2)', 'sq_braccio_l', 'sq_larg / 2', 'sq_sp', 1, TAGLIA)
    p.blocco('y', 'zy_sq_int', 'sede_sq_ginocchio', 'zam_Lf - sq_braccio_l', '-(sq_larg / 2)', 'zam_Lf + sq_larg / 2',
             'sq_larg / 2', 'sq_sp', 1, TAGLIA)
    p.cilindro('y', 'zy_sq_int', 'sede_mozzo_anca', '0 mm', '0 mm', 'sq_mozzo_sede', 'sq_sp', 1, TAGLIA)
    p.cilindro('y', 'zy_sq_int', 'sede_mozzo_ginocchio', 'zam_Lf', '0 mm', 'sq_mozzo_sede', 'sq_sp', 1, TAGLIA)
    p.cilindro('y', 'zy_sq_int', 'foro_vite_anca', '0 mm', '0 mm', 'sq_accesso_d', 'arm_sp_sq', 1, TAGLIA)
    p.cilindro('y', 'zy_sq_int', 'foro_vite_ginocchio', 'zam_Lf', '0 mm', 'sq_accesso_d', 'arm_sp_sq', 1, TAGLIA)
    p.cilindro('y', 'zy_sq_int', 'foro_vite_anima_su', 'fem_web_x0 + fem_web_sp / 2', 'fem_vite_dz', 'vite_m2_passante', 'arm_sp_sq', 1, TAGLIA)
    p.cilindro('y', 'zy_sq_int', 'foro_vite_anima_giu', 'fem_web_x0 + fem_web_sp / 2', '-(fem_vite_dz)', 'vite_m2_passante', 'arm_sp_sq', 1, TAGLIA)
    return occ, p


def fai_tibia(zampa, m):
    occ = _nuovo_comp(zampa, 'Tibia', m)
    p = Parte(occ.component)
    p.blocco('y', 'zy_fondo', 'culla', '-(cul_corto)', '-(cul_semi)', 'cul_lungo', 'cul_semi', 'zy_orlo - zy_fondo', 1, NUOVO)
    p.blocco('y', 'zy_orlo - ale_bugna_h', 'bugna_ginocchio', '-(cul_corto + ale_bugna_l)', '-(ale_bugna / 2)', '-(cul_corto)',
             'ale_bugna / 2', 'ale_bugna_h')
    p.blocco('y', 'zy_orlo - ale_bugna_h', 'bugna_piede', 'cul_lungo', '-(ale_bugna / 2)', 'cul_lungo + ale_bugna_l',
             'ale_bugna / 2', 'ale_bugna_h')
    p.blocco('y', '-(tib_piede_semi_y)', 'stinco', 'cul_lungo', '-(tib_piede_semi)', 'zam_Lt - tib_piede_d / 2', 'tib_piede_semi',
             '2 * tib_piede_semi_y')
    p.cilindro('y', '-(tib_piede_semi_y)', 'piede', 'zam_Lt - tib_piede_d / 2', '0 mm', 'tib_piede_d', '2 * tib_piede_semi_y')
    p.blocco('y', 'zy_srv', 'sede_servo', '-(srv_corto + gio_servo)', '-(srv_larg / 2 + gio_servo)', 'srv_coda + gio_servo',
             'srv_larg / 2 + gio_servo', 'zy_orlo - zy_srv', 1, TAGLIA)
    p.blocco('y', 'cavo_fin_y0', 'finestra_cavo', '-(cul_corto)', '-(cavo_fin_l / 2)', '-(srv_corto)', 'cavo_fin_l / 2',
             'cavo_fin_h', 1, TAGLIA)
    p.cilindro('y', 'zy_fondo', 'sede_cuscinetto', '0 mm', '0 mm', 'cus_sede_d', 'cus_sede_prof', 1, TAGLIA)
    p.cilindro('y', 'zy_fondo', 'passaggio_perno', '0 mm', '0 mm', 'perno_passo', 'cul_fondo', 1, TAGLIA)
    p.cilindro('y', 'zy_orlo', 'foro_aletta_ginocchio', '-(ale_foro_corto)', '0 mm', 'vite_m2_passante', 'ale_bugna_h', -1, TAGLIA)
    p.cilindro('y', 'zy_orlo', 'foro_aletta_piede', 'ale_foro_coda', '0 mm', 'vite_m2_passante', 'ale_bugna_h', -1, TAGLIA)
    return occ, p


# ----------------------------------------------------------------------------------- assieme
# Nel modello STEP del servo (mm): X dell'asse dell'albero, Y del fondo della cassa, Y del lato inferiore
# delle alette. Il servo appoggia sull'orlo della culla con le alette, quindi si posiziona su quel riferimento:
# nello STEP il sotto-aletta e' a 18,4 mm dal fondo, la quota ufficiale e' 18,5.
SERVO_ASSE_X, SERVO_FONDO_Y, SERVO_ALETTE_Y = 5.375, -11.275, 7.125
RIF = ('Tower Pro MG90S', 'Rif_Cuscinetto_F683ZZ', 'Rif_Perno_3x10')


def _faccia_cilindrica(occ, raggio_mm, punto_mm, asse):
    """Faccia cilindrica di un'occorrenza con raggio e asse dati, passante per un punto (terna della zampa)."""
    for f in occ.bRepBodies.item(0).faces:
        g = f.geometry
        if g.surfaceType != adsk.core.SurfaceTypes.CylinderSurfaceType or abs(g.radius * 10 - raggio_mm) > 1e-3:
            continue
        a = g.axis
        if abs(abs({'x': a.x, 'y': a.y, 'z': a.z}[asse]) - 1) > 1e-4:
            continue
        o = g.origin
        d = [o.x * 10 - punto_mm[0], o.y * 10 - punto_mm[1], o.z * 10 - punto_mm[2]]
        d[{'x': 0, 'y': 1, 'z': 2}[asse]] = 0
        if math.sqrt(sum(c * c for c in d)) < 1e-3:
            return f
    return None


def _attese(des):
    """Istanze dei componenti comprati dentro la zampa: (chiave, prefisso del componente, matrice)."""
    v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
    lc, lf = v('zam_Lc'), v('zam_Lf')
    ty = v('zy_orlo') - SERVO_ALETTE_Y          # alette del servo appoggiate sull'orlo
    ycus = v('zy_fondo') - v('cus_flangia_sp')
    ypn = v('zy_pn_est') - v('perno_sporge')
    asse_y = ((1, 0, 0), (0, 0, -1), (0, 1, 0))     # Z del componente -> +Y della zampa
    return [
        # servo del femore: albero verso +Y, coda in alto
        ('servo_femore', RIF[0], _matrice((lc, ty, SERVO_ASSE_X), (0, 0, -1), (0, 1, 0), (1, 0, 0))),
        # servo del ginocchio: albero verso +Y, coda verso il piede
        ('servo_ginocchio', RIF[0], _matrice((lc + lf, ty, -SERVO_ASSE_X), (0, 0, 1), (0, 1, 0), (-1, 0, 0))),
        ('cus_femore', RIF[1], _matrice((lc, ycus, 0), *asse_y)),
        ('cus_ginocchio', RIF[1], _matrice((lc + lf, ycus, 0), *asse_y)),
        ('perno_anca', RIF[2], _matrice((lc, ypn, 0), *asse_y)),
        ('perno_ginocchio', RIF[2], _matrice((lc + lf, ypn, 0), *asse_y)),
        ('perno_coxa', RIF[2], _matrice((0, 0, v('cz_inf_giu') - v('perno_sporge')), (1, 0, 0), (0, 1, 0), (0, 0, 1))),
    ]


def _istanze(z):
    """Occorrenze dei componenti comprati dentro la zampa."""
    return [o for o in z.occurrences if o.component.name.startswith(RIF)]


def _mappa(des, z):
    """{chiave: occorrenza} abbinando ogni istanza attesa a quella reale piu' vicina.

    L'ordine di z.occurrences non e' affidabile: cambiare isGroundToParent sposta le occorrenze
    in fondo all'elenco. Si abbina per componente e posizione.
    """
    libere = _istanze(z)
    out = {}
    for chiave, pref, m in _attese(des):
        t = m.translation
        cand = [o for o in libere if o.component.name.startswith(pref)]
        if not cand:
            raise RuntimeError('manca l\'istanza %s' % chiave)
        o = min(cand, key=lambda c: math.dist(c.transform2.translation.asArray(), (t.x, t.y, t.z)))
        libere.remove(o)
        out[chiave] = o
    return out


def fai_istanze(des, root, zo):
    """Passo 1: cancella giunti e istanze precedenti e crea le istanze.

    Le istanze si creano alla radice, nella posa voluta in terna del robot, e poi si spostano dentro la
    zampa con moveToComponent, che conserva la posizione nello spazio. Aggiungerle direttamente dentro
    "Zampa" funziona solo finche' la zampa sta all'origine: con la zampa ruotata addExistingComponent
    sbaglia la traslazione (e per i riferimenti esterni anche la rotazione) senza dare errori.
    """
    z = zo.component
    for j in [z.asBuiltJoints.item(i) for i in range(z.asBuiltJoints.count)]:
        j.deleteMe()
    for o in _istanze(z):
        o.deleteMe()
    lib = lambda pref: [o for o in root.occurrences if o.component.name.startswith(pref)][0]
    for chiave, pref, m in _attese(des):
        o_lib = lib(pref)
        w = m.copy()
        w.transformBy(zo.transform2)            # dalla terna della zampa alla terna del robot
        if o_lib.isReferencedComponent:
            # Per un riferimento esterno la nuova istanza nasce in w * T_lib: si passa w * T_lib^-1.
            inv = o_lib.transform2.copy()
            inv.invert()
            inv.transformBy(w)
            w = inv
        occ = root.occurrences.addExistingComponent(o_lib.component, w)
        occ = occ.moveToComponent(zo)
        # I riferimenti esterni nascono "fissati al genitore": cosi' bloccherebbero i giunti della zampa.
        try:
            if occ.isGroundToParent:
                occ.isGroundToParent = False
        except Exception:
            pass
    return {'istanze': len(_istanze(z))}


def controlla_istanze(des, zo):
    """Scarto (mm) tra la posizione nativa attesa e quella reale di ogni istanza: da leggere in uno script a parte."""
    z = zo.component
    inv = zo.transform2.copy()
    inv.invert()
    rep = {}
    for chiave, o in _mappa(des, z).items():
        px = o.createForAssemblyContext(zo)
        c = px.bRepBodies.item(0).physicalProperties.centerOfMass
        c.transformBy(inv)
        rep[chiave] = [round(c.x * 10, 2), round(c.y * 10, 2), round(c.z * 10, 2)]
    return rep


def fai_giunti(des, root, zo):
    """Passo 3: giunti rigidi per le parti solidali, di rivoluzione per femore e ginocchio."""
    z = zo.component
    v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
    t0 = des.timeline.count
    ist = _mappa(des, z)
    parti = {o.component.name: o for o in z.occurrences}
    coxa, fem_b, fem_a, tibia = parti['Coxa'], parti['Femore_B'], parti['Femore_A'], parti['Tibia']
    lc, lf = v('zam_Lc'), v('zam_Lf')

    def rigido(a, b, nome):
        inp = z.asBuiltJoints.createInput(a, b, None)
        inp.setAsRigidJointMotion()
        j = z.asBuiltJoints.add(inp)
        j.name = nome
        return j

    def rivoluzione(mobile, fisso, faccia, nome):
        geo = adsk.fusion.JointGeometry.createByNonPlanarFace(faccia, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)
        inp = z.asBuiltJoints.createInput(mobile, fisso, geo)
        inp.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
        j = z.asBuiltJoints.add(inp)
        j.name = nome
        return j

    rigido(ist['servo_femore'], coxa, 'R_servo_femore')
    rigido(ist['cus_femore'], coxa, 'R_cuscinetto_femore')
    rigido(ist['perno_coxa'], coxa, 'R_perno_coxa')
    rigido(fem_a, fem_b, 'R_femore_A_B')
    rigido(ist['perno_anca'], fem_b, 'R_perno_anca')
    rigido(ist['perno_ginocchio'], fem_b, 'R_perno_ginocchio')
    rigido(ist['servo_ginocchio'], tibia, 'R_servo_ginocchio')
    rigido(ist['cus_ginocchio'], tibia, 'R_cuscinetto_ginocchio')
    r = v('cus_sede_d') / 2
    f_anca = _faccia_cilindrica(coxa, r, (lc, 0, 0), 'y')
    f_gin = _faccia_cilindrica(tibia, r, (lc + lf, 0, 0), 'y')
    rivoluzione(fem_b, coxa, f_anca, 'G_femore')
    rivoluzione(tibia, fem_b, f_gin, 'G_ginocchio')
    L['raggruppa'](des, t0, 'Giunti Zampa')
    return {'giunti': [z.asBuiltJoints.item(i).name for i in range(z.asBuiltJoints.count)]}


# Limiti dei giunti, in angoli fisici: alpha = femore sopra l'orizzontale, gamma = angolo interno al ginocchio.
# Valori di giunto: G_femore = -alpha, G_ginocchio = 90 - gamma (misurato con verifica_zampa.py).
# Campo verificato libero da interferenze l'8 ottobre 2026 (femore con il puntone): contatti a alpha = +60,
# a gamma = 40 e, solo con il femore oltre -52, a gamma = 45.
LIMITI = {'alpha': (-60.0, 55.0), 'gamma': (50.0, 145.0)}


def fai_limiti(des, zo):
    z = zo.component
    g = {z.asBuiltJoints.item(i).name: z.asBuiltJoints.item(i) for i in range(z.asBuiltJoints.count)}
    campi = {'G_femore': (-LIMITI['alpha'][1], -LIMITI['alpha'][0]),
             'G_ginocchio': (90.0 - LIMITI['gamma'][1], 90.0 - LIMITI['gamma'][0])}
    for nome, (lo, hi) in campi.items():
        lim = adsk.fusion.RevoluteJointMotion.cast(g[nome].jointMotion).rotationLimits
        lim.isMinimumValueEnabled = True
        lim.minimumValue = math.radians(lo)
        lim.isMaximumValueEnabled = True
        lim.maximumValue = math.radians(hi)
    return campi


def stato_istanze(des, zo):
    """Posizione reale di ogni istanza: ingombro nella terna della zampa e, per i servo, asse dell'albero."""
    rep = {}
    for chiave, o in _mappa(des, zo.component).items():
        px = o.createForAssemblyContext(zo)
        b = px.bRepBodies.item(0)
        bb = b.boundingBox
        info = {'min': [round(bb.minPoint.x * 10, 2), round(bb.minPoint.y * 10, 2), round(bb.minPoint.z * 10, 2)],
                'max': [round(bb.maxPoint.x * 10, 2), round(bb.maxPoint.y * 10, 2), round(bb.maxPoint.z * 10, 2)]}
        if chiave.startswith('servo'):
            for f in b.faces:
                g = f.geometry
                if g.surfaceType == adsk.core.SurfaceTypes.CylinderSurfaceType and abs(g.radius * 10 - 5.9) < 1e-3:
                    info['asse_albero'] = [round(g.origin.x * 10, 3), round(g.origin.z * 10, 3)]
        rep[chiave] = info
    return rep


def interferenze(des, zo):
    """Interferenze tra le occorrenze figlie della zampa: [(a, b, volume mm3)]."""
    col = adsk.core.ObjectCollection.create()
    for o in zo.childOccurrences:
        col.add(o)
    res = des.analyzeInterference(des.createInterferenceInput(col))
    out = []
    for i in range(res.count):
        r = res.item(i)
        nomi = []
        for e in (r.entityOne, r.entityTwo):
            occ = getattr(e, 'assemblyContext', None)
            nomi.append(occ.name if occ else e.parentComponent.name)
        out.append((nomi[0], nomi[1], round(r.interferenceBody.volume * 1000, 2)))
    return out


# ----------------------------------------------------------------------------------- script
def main(passi):
    out = {'passi': passi}
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0

        if 'parametri' in passi:
            out['parametri'] = L['aggiungi_parametri'](des, PARAMETRI)
            out['controllo'] = {n: round(v(n), 3) for n in ('zam_semi_larg', 'zy_sq_int', 'zy_srv', 'zy_orlo', 'zy_fondo',
                                                              'zy_pn_int', 'cz_inf_giu', 'cz_inf_su', 'cz_sup_giu', 'cz_sup_su',
                                                              'cul_semi', 'cul_corto', 'cul_lungo', 'ale_foro_corto', 'ale_foro_coda')}
        zo = _zampa(root)
        z = zo.component
        lc, lf = v('zam_Lc'), v('zam_Lf')
        m_fem = _matrice((lc, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
        m_tib = _matrice((lc + lf, 0, 0), (0, 0, -1), (0, 1, 0), (1, 0, 0))
        costruttori = {
            'coxa': lambda: fai_coxa(z),
            'femore_b': lambda: fai_femore_b(z, m_fem),
            'femore_a': lambda: fai_femore_a(z, m_fem),
            'tibia': lambda: fai_tibia(z, m_tib),
        }
        for nome, fn in costruttori.items():
            if nome not in passi:
                continue
            occ, p = fn()
            L['raggruppa'](des, T0[occ.component.name], 'Parte ' + occ.component.name)
            out[nome] = {'lavorazioni': p.n, 'schizzi_non_vincolati': p.non_vincolati,
                         'corpi': occ.component.bRepBodies.count}
        if 'istanze' in passi:
            out['istanze'] = fai_istanze(des, root, zo)
        if 'giunti' in passi:
            out['giunti'] = fai_giunti(des, root, zo)
        if 'limiti' in passi:
            out['limiti'] = fai_limiti(des, zo)
        if 'stato' in passi:
            out['stato'] = stato_istanze(des, zo)
        if 'controllo' in passi:
            out['controllo_istanze'] = controlla_istanze(des, zo)
        if 'interferenze' in passi:
            out['interferenze'] = interferenze(des, zo)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1))
