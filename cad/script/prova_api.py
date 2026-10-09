"""Blocco B0 della passata estetica: prova su un documento a parte delle funzioni dell'API che servono a lame,
guscio della tibia e carapace e che negli script non erano mai state usate.

Prove: intersezione con un cilindro (bombatura delle lame), raccordo degli spigoli di una faccia cilindrica,
smusso a 45 gradi di due spigoli scelti per posizione, svuotamento con una faccia tolta dopo lo smusso (sezione a C),
rivoluzione di un cerchio (toro), loft tra due rettangoli. Il documento di prova si chiude senza salvare e si torna
al design di lavoro. Uso dal connettore: runpy.run_path(percorso)['main']()
"""
import json
import math
import os
import runpy
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__))
VI = adsk.core.ValueInput
P3 = adsk.core.Point3D.create
OP = adsk.fusion.FeatureOperations


def _coll(oggetti):
    c = adsk.core.ObjectCollection.create()
    for o in oggetti:
        c.add(o)
    return c


def _spigoli_dritti(corpo, cond):
    """Spigoli rettilinei del corpo i cui estremi (mm) soddisfano cond(p0, p1)."""
    out = []
    for e in corpo.edges:
        if e.geometry.curveType != adsk.core.Curve3DTypes.Line3DCurveType:
            continue
        a, b = e.startVertex.geometry, e.endVertex.geometry
        if cond((a.x * 10, a.y * 10, a.z * 10), (b.x * 10, b.y * 10, b.z * 10)):
            out.append(e)
    return out


def prova_lama(p, comp):
    """Lastra 90 x 28 x 4 intersecata con un cilindro di raggio 149 (colmo 1 mm), poi raccordo 0,8 sulla faccia curva."""
    L = p.L
    lastra = p.blocco('y', '0 mm', 'lastra', '0 mm', '-14 mm', '90 mm', '14 mm', '4 mm', 1, L['NUOVO'])
    corpo = lastra.bodies.item(0)
    R = 14.0 ** 2 / 2.0 / 1.0 + 0.5
    sk = p.sk_cerchio('x', '-1 mm', 'cresta', '%.3f mm' % (3.0 - R), '0 mm', '%.3f mm' % (2 * R))
    ext = comp.features.extrudeFeatures
    inp = ext.createInput(sk.profiles.item(0), OP.IntersectFeatureOperation)
    inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI.createByString('100 mm')),
                         adsk.fusion.ExtentDirections.PositiveExtentDirection)
    inp.participantBodies = [corpo]
    f = ext.add(inp)
    f.name = 'bombatura'
    corpo = comp.bRepBodies.item(0)
    curve = [fa for fa in corpo.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.CylinderSurfaceType]
    fil = comp.features.filletFeatures
    fi = fil.createInput()
    fi.edgeSetInputs.addConstantRadiusEdgeSet(_coll([e for fa in curve for e in fa.edges]), VI.createByString('0.8 mm'), False)
    ff = fil.add(fi)
    ff.name = 'raccordo'
    corpo = comp.bRepBodies.item(0)
    bb = corpo.boundingBox
    return {'volume_mm3': round(corpo.volume * 1000, 1), 'facce_curve': len(curve),
            'y_max': round(bb.maxPoint.y * 10, 3), 'salute': [f.healthState == 0, ff.healthState == 0]}


def prova_guscio(p, comp):
    """Blocco 12 x 24 x 60, fronte convesso (cilindro R 300), smusso 4 a 45 gradi sui due spigoli del fronte,
    svuotamento 1,6 togliendo il retro: deve uscire una sezione a C sfaccettata."""
    L = p.L
    b = p.blocco('z', '-60 mm', 'pieno', '100 mm', '-12 mm', '114 mm', '12 mm', '60 mm', 1, L['NUOVO'])
    corpo = b.bodies.item(0)
    R = 300.0
    sk = p.sk_cerchio('y', '-13 mm', 'fronte', '%.3f mm' % (114.0 - R), '-30 mm', '%.3f mm' % (2 * R))
    ext = comp.features.extrudeFeatures
    inp = ext.createInput(sk.profiles.item(0), OP.IntersectFeatureOperation)
    inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI.createByString('26 mm')),
                         adsk.fusion.ExtentDirections.PositiveExtentDirection)
    inp.participantBodies = [corpo]
    fr = ext.add(inp)
    fr.name = 'fronte_convesso'
    corpo = [c for c in comp.bRepBodies if c.boundingBox.minPoint.x > 9.0][0]
    # spigoli del fronte: dove la faccia cilindrica incontra i fianchi y = +-12
    fronte = [fa for fa in corpo.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.CylinderSurfaceType][0]
    sp = []
    for e in fronte.edges:
        ys, ye = e.startVertex.geometry.y * 10, e.endVertex.geometry.y * 10
        if abs(abs(ys) - 12) < 0.01 and abs(abs(ye) - 12) < 0.01 and ys * ye > 0:     # spigoli verticali del fronte
            sp.append(e)
    ch = comp.features.chamferFeatures
    ci = ch.createInput2()
    ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(_coll(sp), VI.createByString('4 mm'), False)
    cf = ch.add(ci)
    cf.name = 'smussi_fronte'
    corpo = [c for c in comp.bRepBodies if c.boundingBox.minPoint.x > 9.0][0]
    retro = [fa for fa in corpo.faces if fa.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType
             and abs(fa.pointOnFace.x * 10 - 100) < 0.01]
    sv = p.svuota(retro, '1.6 mm', 'guscio')
    corpo = [c for c in comp.bRepBodies if c.boundingBox.minPoint.x > 9.0][0]
    return {'spigoli_smussati': len(sp), 'volume_mm3': round(corpo.volume * 1000, 1), 'facce': corpo.faces.count,
            'salute': [fr.healthState == 0, cf.healthState == 0, sv.healthState == 0]}


def prova_rivoluzione_loft(p, comp):
    sk = p.sk_cerchio('y', '0 mm', 'sezione_toro', '230 mm', '0 mm', '8 mm')
    rev = comp.features.revolveFeatures
    ri = rev.createInput(sk.profiles.item(0), comp.zConstructionAxis, OP.NewBodyFeatureOperation)
    ri.setAngleExtent(False, VI.createByString('360 deg'))
    rf = rev.add(ri)
    rf.name = 'toro'
    v_toro = rf.bodies.item(0).volume * 1000
    a = p.sk_rett('z', '0 mm', 'loft_alto', '300 mm', '-10 mm', '320 mm', '10 mm')
    b = p.sk_rett('z', '-50 mm', 'loft_basso', '305 mm', '-4 mm', '315 mm', '4 mm')
    lo = comp.features.loftFeatures
    li = lo.createInput(OP.NewBodyFeatureOperation)
    li.loftSections.add(a.profiles.item(0))
    li.loftSections.add(b.profiles.item(0))
    li.isSolid = True
    lf = lo.add(li)
    lf.name = 'loft'
    v_loft = lf.bodies.item(0).volume * 1000
    atteso_toro = math.pi * 4 ** 2 * 2 * math.pi * 230
    atteso_loft = 50 / 3 * (400 + 80 + math.sqrt(400 * 80))
    return {'toro_mm3': round(v_toro, 1), 'toro_atteso': round(atteso_toro, 1), 'loft_mm3': round(v_loft, 1),
            'loft_tronco_di_piramide': round(atteso_loft, 1), 'salute': [rf.healthState == 0, lf.healthState == 0]}


def main():
    out = {}
    app = adsk.core.Application.get()
    lavoro = app.activeDocument
    prova = None
    try:
        prova = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        des = adsk.fusion.Design.cast(app.activeProduct)
        des.designType = adsk.fusion.DesignTypes.ParametricDesignType
        L = runpy.run_path(os.path.join(QUI, 'lib_cad.py'))
        root = des.rootComponent
        for nome, f in (('lama', prova_lama), ('guscio', prova_guscio), ('rivoluzione_loft', prova_rivoluzione_loft)):
            try:
                occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
                occ.component.name = nome
                p = L['Parte'](occ.component)
                p.L = L
                out[nome] = f(p, occ.component)
                out[nome]['schizzi_non_vincolati'] = p.non_vincolati
            except Exception:
                out[nome] = {'errore': traceback.format_exc()[-1500:]}
    finally:
        if prova is not None:
            prova.close(False)
        lavoro.activate()
        out['documento_attivo'] = app.activeDocument.name
    print(json.dumps(out, indent=1, ensure_ascii=False))
