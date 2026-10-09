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
    # --- coperchio
    ('cor_cop_z', '28.4 mm', 'mm', 'Coperchio: lato inferiore del dorso'),
    ('cor_cop_sp', '1.6 mm', 'mm', 'Coperchio: spessore del dorso'),
    ('cor_cop_lobo', '22 mm', 'mm', 'Coperchio: raggio dei lobi sopra gli assi delle coxe'),
    ('cor_muso_x', '101 mm', 'mm', 'Coperchio: punta del muso'),
    ('cor_muso_semi', '20 mm', 'mm', 'Coperchio: semilarghezza del muso'),
]

T0 = {}


def _corpo(root):
    occ = L['trova_occ'](root, 'Corpo')
    if occ:
        return occ[0]
    o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name = 'Corpo'
    return o


def _nuovo_comp(corpo, nome):
    genitore = corpo.component
    for o in L['trova_occ'](genitore, nome):
        o.deleteMe()
    T0[nome] = genitore.parentDesign.timeline.count
    occ = genitore.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = nome
    return occ


def _chiudi(des, nome, p):
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
    gond = gondola(p, 'ang')
    gond_p = p.specchia(gond, 'x', 'gondola_posteriore_s')
    med = gondola(p, 'med')
    # bugne della SSC-32 sul tetto
    bug = []
    for nome, sx_, sy_ in (('ssc_bugna_aa', 1, 1), ('ssc_bugna_ab', 1, -1), ('ssc_bugna_pa', -1, 1), ('ssc_bugna_pb', -1, -1)):
        x = 'cor_ssc_x %s ssc_fori_x / 2' % ('+' if sx_ > 0 else '-')
        y = ('ssc_fori_y / 2') if sy_ > 0 else '-(ssc_fori_y / 2)'
        bug.append(p.cilindro('z', '-(cor_tetto)', nome, x, y, 'cor_ssc_bugna_d', 'ssc_dist'))
        bug.append(p.cilindro('z', '-(cor_tetto) + ssc_dist', nome + '_pilota', x, y, 'vite_m25_pilota', 'ssc_dist - 1 mm', -1, TAGLIA))
    # specchiatura del lato sinistro sul destro
    p.specchia(sx + gond + [gond_p] + med, 'y', 'lato_destro')
    # interno del tunnel (aperto sotto, verso la chiglia, e dietro, per la batteria)
    p.blocco('z', '-(cor_fondo)', 'interno_tunnel', '-(cor_tun_x0)', '-(cor_tun_semi - cor_parete)', 'cor_tun_x1 - cor_parete',
             'cor_tun_semi - cor_parete', 'cor_fondo - cor_tetto - cor_tetto_sp', 1, TAGLIA)
    return occ, p


def fai_chiglia(corpo):
    occ = _nuovo_comp(corpo, 'Corpo_Chiglia')
    p = Parte(occ.component)
    p.blocco('z', '-(cor_chiglia)', 'vasca', '-(cor_tun_x0)', '-(cor_tun_semi)', 'cor_tun_x1', 'cor_tun_semi',
             'cor_chiglia - cor_fondo', 1, NUOVO)
    p.blocco('z', '-(cor_chiglia) + cor_chiglia_sp', 'interno', '-(cor_tun_x0)', '-(cor_tun_semi - cor_parete)',
             'cor_tun_x1 - cor_parete', 'cor_tun_semi - cor_parete', 'cor_chiglia - cor_fondo', 1, TAGLIA)
    return occ, p


def fai_coperchio(corpo):
    occ = _nuovo_comp(corpo, 'Corpo_Coperchio')
    p = Parte(occ.component)
    p.blocco('z', 'cor_cop_z', 'dorso_nucleo', '-(cor_tun_x0)', '-(cor_tun_semi)', 'cor_tun_x1', 'cor_tun_semi', 'cor_cop_sp', 1, NUOVO)
    p.blocco('z', 'cor_cop_z', 'dorso_baie', '-(cor_baia_x)', '-(cor_baia_y)', 'cor_baia_x', 'cor_baia_y', 'cor_cop_sp')
    p.blocco('z', 'cor_cop_z', 'muso', 'cor_tun_x1', '-(cor_muso_semi)', 'cor_muso_x', 'cor_muso_semi', 'cor_cop_sp')
    for nome, x, y in (('lobo_as', 'cor_ang_x', 'cor_ang_y'), ('lobo_ad', 'cor_ang_x', '-(cor_ang_y)'),
                       ('lobo_ps', '-(cor_ang_x)', 'cor_ang_y'), ('lobo_pd', '-(cor_ang_x)', '-(cor_ang_y)'),
                       ('lobo_ms', '0 mm', 'cor_med_y'), ('lobo_md', '0 mm', '-(cor_med_y)')):
        p.cilindro('z', 'cor_cop_z', nome, x, y, '2 * cor_cop_lobo', 'cor_cop_sp')
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
        for nome, f in (('base', fai_base), ('chiglia', fai_chiglia), ('coperchio', fai_coperchio)):
            if nome in passi:
                occ, p = f(corpo)
                out[nome] = _chiudi(des, occ.component.name, p)
        if 'stato' in passi:
            out['stato'] = stato(des, root)
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
