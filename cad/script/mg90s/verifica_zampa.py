"""Verifica cinematica di una zampa pilotando i giunti veri (G_femore, G_ginocchio).

Si esegue dentro Fusion:  runpy.run_path('<repo>/cad/script/verifica_zampa.py')['main']()

Convenzioni dell'esito:
  alpha = angolo del femore sopra l'orizzontale (negativo = ginocchio piu' basso dell'anca);
  gamma = angolo interno al ginocchio tra femore e tibia (180 = zampa distesa).
Posa di riferimento del modello: alpha = 0, gamma = 90.
Lo script misura alpha e gamma dalle trasformate reali delle parti, non li assume dal valore del giunto.
"""
import json
import math
import os
import runpy
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
P3 = adsk.core.Point3D.create


def _pt(occ, x_mm, rif):
    """Punto (x, 0, 0) della terna di una parte, espresso nella terna della parte di riferimento.

    Nel sotto-assieme nessuna parte e' fissata: pilotando un giunto Fusion puo' muovere l'una o
    l'altra. Per questo si misura tutto rispetto alla coxa.
    """
    p = P3(x_mm / 10, 0, 0)
    p.transformBy(occ.transform2)
    inv = rif.transform2.copy()
    inv.invert()
    p.transformBy(inv)
    return p.x * 10, p.y * 10, p.z * 10


def main(alphas=(-75, -60, -52, -40, -28, -16, -4, 10, 25), gammas=(55, 62, 68, 74, 90, 105, 120, 134, 150, 165)):
    out = {}
    try:
        Z = runpy.run_path(os.path.join(QUI, 'zampa.py'))
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent
        v = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10.0
        zo = [o for o in root.occurrences if o.component.name == 'Zampa'][0]
        z = zo.component
        giunti = {z.asBuiltJoints.item(i).name: z.asBuiltJoints.item(i) for i in range(z.asBuiltJoints.count)}
        gf = adsk.fusion.RevoluteJointMotion.cast(giunti['G_femore'].jointMotion)
        gg = adsk.fusion.RevoluteJointMotion.cast(giunti['G_ginocchio'].jointMotion)
        parti = {o.component.name: o.createForAssemblyContext(zo) for o in z.occurrences
                 if o.component.name in ('Coxa', 'Femore_B', 'Tibia')}
        lc, lf, lt = v('zam_Lc'), v('zam_Lf'), v('zam_Lt')

        def posa():
            cx = parti['Coxa']
            anca = _pt(parti['Femore_B'], 0, cx)
            gin = _pt(parti['Femore_B'], lf, cx)
            gin_t = _pt(parti['Tibia'], 0, cx)
            piede = _pt(parti['Tibia'], lt, cx)
            alpha = math.degrees(math.atan2(gin[2] - anca[2], gin[0] - anca[0]))
            a = (anca[0] - gin[0], anca[2] - gin[2])
            b = (piede[0] - gin_t[0], piede[2] - gin_t[2])
            cg = (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))
            gamma = math.degrees(math.acos(max(-1, min(1, cg))))
            scarto = math.dist(gin, gin_t)       # il ginocchio del femore e quello della tibia devono coincidere
            return alpha, gamma, piede, scarto

        gf.rotationValue = 0
        gg.rotationValue = 0
        a0, g0, piede0, s0 = posa()
        out['riferimento'] = {'alpha': round(a0, 2), 'gamma': round(g0, 2), 'piede': [round(c, 2) for c in piede0],
                              'scarto_ginocchio_mm': round(s0, 4), 'interferenze': Z['interferenze'](des, zo)}
        # verso dei giunti: +10 gradi su ciascuno
        gf.rotationValue = math.radians(10)
        a1, g1, _, _ = posa()
        gf.rotationValue = 0
        gg.rotationValue = math.radians(10)
        a2, g2, _, _ = posa()
        gg.rotationValue = 0
        kf = (a1 - a0) / 10.0      # gradi di alpha per grado di giunto
        kg = (g2 - g0) / 10.0      # gradi di gamma per grado di giunto
        if abs(kf) < 0.5 or abs(kg) < 0.5:
            out['verso'] = {'kf': kf, 'kg': kg, 'nota': 'i giunti non muovono le parti'}
            print(json.dumps(out, indent=1))
            return
        out['verso'] = {'d_alpha_per_grado_G_femore': round(kf, 3), 'd_gamma_per_grado_G_ginocchio': round(kg, 3),
                        'alpha_non_cambia_gamma': round(g1 - g0, 3)}
        # scansione
        griglia = {}
        peggiori = []
        for al in alphas:
            riga = ''
            for ga in gammas:
                gf.rotationValue = math.radians((al - a0) / kf)
                gg.rotationValue = math.radians((ga - g0) / kg)
                am, gm, piede, sc = posa()
                if abs(am - al) > 0.2 or abs(gm - ga) > 0.2:
                    riga += '?'
                    continue
                inter = Z['interferenze'](des, zo)
                riga += '.' if not inter else 'X'
                if inter:
                    peggiori.append({'alpha': al, 'gamma': ga, 'chi': sorted({'%s/%s' % (i[0].split(':')[0], i[1].split(':')[0]) for i in inter}),
                                     'vol_mm3': round(sum(i[2] for i in inter), 1)})
            griglia['alpha %+4d' % al] = riga
        gf.rotationValue = 0
        gg.rotationValue = 0
        out['gammas'] = list(gammas)
        out['griglia'] = griglia
        out['collisioni'] = peggiori
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1))
