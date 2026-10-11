"""Esporta dal CAD i dati della guida di montaggio (D-075, docs/piano-guida.md), in sola lettura.

Passi, uno o piu' per chiamata del connettore (ognuno si ferma a `budget_s` secondi e dice quanti ne restano):
    manifest   occorrenze del corpo e della zampa con chiavi stabili, trasformate, colori dei corpi -> guida/dati/manifest.json
    mesh       un PLY per componente, nella terna propria, solo se il revisionId e' cambiato -> build/guida/cad/mesh/
    fori       cilindri concavi dei pezzi con il nome della lavorazione -> build/guida/cad/fori/, poi guida/dati/fori.json
    controllo  rilettura: ogni componente del manifest ha la sua mesh e i proxy coincidono con istanza x locale

    import runpy
    def run(_context: str):
        runpy.run_path('/Users/paul/hexapod-v2/cad/script/esporta_guida.py')['main'](['manifest', 'mesh'])

Le zampe sono la stessa zampa ruotata: le parti si scrivono una volta, nella terna della zampa come costruita, piu' le
sei terne delle istanze. Le chiavi del corpo sono quelle di assieme.pose_corpo (Servo_Coxa_AS, SSC32, ...) e il nome
del componente per le parti stampate; quelle della zampa sono il pezzo piu' il giunto (Servo_femore, Perno_coxa, ...).
"""
import array
import json
import math
import os
import runpy
import time
import traceback

import adsk.core
import adsk.fusion

QUI = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '/Users/paul/hexapod-v2/cad/script'
RADICE = os.path.dirname(os.path.dirname(QUI))
V = runpy.run_path(os.path.join(QUI, 'versione.py'))
AS = runpy.run_path(os.path.join(QUI, 'assieme.py'))
DATI = os.path.join(RADICE, 'guida', 'dati')
CACHE = os.path.join(RADICE, 'build', 'guida', 'cad')
SALTA = ('flat', 'linguetta', 'zona_spine_servo', 'zona_barre_retro', 'uscita_cavi')   # ingombri non rigidi o sovrapposti
CORTI = {'Rif_Servo_MG996R': 'Servo', 'Rif_Squadretta_25T': 'Squadretta', 'Rif_Cuscinetto_LF1050ZZ': 'Cuscinetto',
         'Rif_Perno_5': 'Perno', 'Rif_FSR_400': 'FSR'}
# qualita' delle mesh: le parti stampate fini (i fori da 2,4 restano tondi), le comprate dagli STEP grossolane
TOLLERANZA_CM, DEVIAZIONE_RAD = 0.003, math.radians(15)


def _mm(des, expr):
    return des.unitsManager.evaluateExpression(expr, 'mm') * 10.0


def _matrice(m):
    """Le prime tre righe della matrice 4x4, traslazione in mm."""
    d = list(m.asArray())
    out = []
    for r in range(3):
        out += [round(d[4 * r], 9), round(d[4 * r + 1], 9), round(d[4 * r + 2], 9), round(d[4 * r + 3] * 10, 4)]
    return out


def _colore(corpo):
    """(nome dell'aspetto, [r, g, b]) del corpo: opaque_albedo se c'e', altrimenti la prima proprieta' colore."""
    a = corpo.appearance
    if a is None:
        return ('', [180, 180, 180])
    prop = a.appearanceProperties.itemById('opaque_albedo')
    if prop is None:
        for i in range(a.appearanceProperties.count):
            p = a.appearanceProperties.item(i)
            if p.objectType == adsk.core.ColorProperty.classType():
                prop = p
                break
    if prop is None or adsk.core.ColorProperty.cast(prop) is None or adsk.core.ColorProperty.cast(prop).value is None:
        return (a.name, [180, 180, 180])
    c = adsk.core.ColorProperty.cast(prop).value
    return (a.name, [c.red, c.green, c.blue])


def _corpi(comp, m):
    """[(corpo nativo, matrice dalla terna del suo componente alla terna di comp)] con i sotto-componenti."""
    out = [(b, m) for b in comp.bRepBodies if b.name not in SALTA]
    for c in comp.occurrences:
        mc = c.transform2.copy()
        mc.transformBy(m)
        out += _corpi(c.component, mc)
    return out


def _tipo(nome):
    if nome.startswith('Rif_'):
        return 'comprato'
    if nome.startswith('Ingombro_'):
        return 'ingombro'
    return 'stampato'


# ------------------------------------------------------------------------------------------------ manifest
def _chiavi_corpo(des, corpo):
    """{occorrenza nativa dentro Corpo: chiave}: le chiavi di pose_corpo per le Rif_, il nome per le parti stampate."""
    out = {}
    for chiave, o in AS['_istanze_corpo'](corpo).items():
        if o is not None:
            out[o.name] = chiave
    for o in corpo.component.occurrences:
        n = o.component.name
        if o.name in out or n.startswith('Rif_'):
            continue
        if n == 'Corpo_Slitta_Regolatore':
            # la destra e' la sinistra girata attorno a un asse che non passa per l'origine: conta dove finisce la geometria
            bb = o.component.bRepBodies.item(0).boundingBox
            c = adsk.core.Point3D.create((bb.minPoint.x + bb.maxPoint.x) / 2, (bb.minPoint.y + bb.maxPoint.y) / 2, 0)
            c.transformBy(o.transform2)
            out[o.name] = n + ('_S' if c.y > 0 else '_D')
        else:
            out[o.name] = n
    return out


def _chiave_zampa(des, o):
    """Pezzo della zampa piu' il giunto, dalla posizione su x nella terna della zampa come costruita."""
    n = o.component.name
    if n not in CORTI:
        return n
    lc, lf = _mm(des, 'zam_Lc'), _mm(des, 'zam_Lf')
    x = o.transform2.translation.x * 10
    giunto = min((('coxa', 0.0), ('femore', lc), ('ginocchio', lc + lf)), key=lambda g: abs(x - g[1]))[0]
    return CORTI[n] + '_' + giunto


def manifest(des, root):
    corpo = AS['_corpo'](root)
    zampe = AS['mappa_zampe'](des, root)
    zampa = next(iter(zampe.values()))
    componenti, occorrenze = {}, []

    def registra(comp):
        if comp.name in componenti:
            return
        corpi = _corpi(comp, adsk.core.Matrix3D.create())
        aspetti = {}
        for b, _ in corpi:
            nome, rgb = _colore(b)
            aspetti.setdefault(nome, rgb)
        componenti[comp.name] = {'tipo': _tipo(comp.name), 'revisione': comp.revisionId, 'mesh': comp.name + '.ply',
                                 'aspetti': [[k, v] for k, v in sorted(aspetti.items())], 'corpi': len(corpi)}

    chiavi = _chiavi_corpo(des, corpo)
    for o in corpo.component.occurrences:
        registra(o.component)
        occorrenze.append({'chiave': 'corpo/' + chiavi[o.name], 'componente': o.component.name, 'assieme': 'corpo',
                           'T': _matrice(o.transform2),
                           **({'alternativa': True} if o.component.name == 'Corpo_Sportello_Servizio_Zaino' else {})})
    viste = set()
    for o in zampa.component.occurrences:
        registra(o.component)
        k = _chiave_zampa(des, o)
        if k in viste:
            raise RuntimeError('chiave della zampa doppia: ' + k)
        viste.add(k)
        occorrenze.append({'chiave': 'zampa/' + k, 'componente': o.component.name, 'assieme': 'zampa',
                           'segmento': AS['_gruppo'](des, o), 'T': _matrice(o.transform2)})
    lib = {o.component.name: o for o in root.occurrences if o.component.name.startswith('Rif_')}
    for chiave, (nome_lib, m, togli) in AS['alternative'](des).items():
        registra(lib[nome_lib].component)
        occorrenze.append({'chiave': 'corpo/' + chiave, 'componente': nome_lib, 'assieme': 'corpo', 'virtuale': True,
                           'sostituisce': list(togli), 'T': _matrice(m)})
    doc = adsk.core.Application.get().activeDocument
    out = {'versione': V['VERSIONE'], 'documento': doc.name, 'unita': 'mm',
           'parametri': {k: round(_mm(des, k), 4) for k in ('zam_Lc', 'zam_Lf', 'zam_Lt')},
           'istanze': {'corpo': _matrice(corpo.transform2), 'zampe': {n: _matrice(z.transform2) for n, z in sorted(zampe.items())}},
           'componenti': dict(sorted(componenti.items())), 'occorrenze': occorrenze}
    os.makedirs(DATI, exist_ok=True)
    with open(os.path.join(DATI, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False, sort_keys=False)
        f.write('\n')
    return {'componenti': len(componenti), 'occorrenze': len(occorrenze)}


# ------------------------------------------------------------------------------------------------ mesh
def _scrivi_ply(percorso, corpi, comprato):
    """PLY binario: vertici in mm con il colore del corpo, facce indicizzate."""
    xyz, rgb, facce = array.array('f'), array.array('B'), array.array('i')
    base = 0
    for b, m in corpi:
        mc = b.meshManager.createMeshCalculator()
        if comprato:
            mc.setQuality(adsk.fusion.TriangleMeshQualityOptions.LowQualityTriangleMesh)
        else:
            mc.surfaceTolerance = TOLLERANZA_CM
            mc.maxNormalDeviation = DEVIAZIONE_RAD
        me = mc.calculate()
        c, idx = me.nodeCoordinatesAsDouble, me.nodeIndices
        col = _colore(b)[1]
        d = list(m.asArray())
        n = len(c) // 3
        for i in range(n):
            x, y, z = c[3 * i], c[3 * i + 1], c[3 * i + 2]
            xyz.extend(((d[0] * x + d[1] * y + d[2] * z + d[3]) * 10, (d[4] * x + d[5] * y + d[6] * z + d[7]) * 10,
                        (d[8] * x + d[9] * y + d[10] * z + d[11]) * 10))
            rgb.extend(col)
        for k in range(0, len(idx), 3):
            facce.extend((3,))
            facce.extend((idx[k] + base, idx[k + 1] + base, idx[k + 2] + base))
        base += n
    nv, nf = base, len(facce) // 4
    intest = ('ply\nformat binary_little_endian 1.0\nelement vertex %d\nproperty float x\nproperty float y\nproperty float z\n'
              'property uchar red\nproperty uchar green\nproperty uchar blue\nelement face %d\n'
              'property list uchar int vertex_indices\nend_header\n' % (nv, nf)).encode('ascii')
    with open(percorso, 'wb') as f:
        f.write(intest)
        for i in range(nv):
            f.write(xyz[3 * i:3 * i + 3].tobytes())
            f.write(rgb[3 * i:3 * i + 3].tobytes())
        for k in range(nf):
            f.write(bytes((3,)))
            f.write(facce[4 * k + 1:4 * k + 4].tobytes())
    return nv, nf


def mesh(des, root, budget_s=25.0, forza=False, solo=None):
    t0 = time.time()
    with open(os.path.join(DATI, 'manifest.json'), encoding='utf-8') as f:
        man = json.load(f)
    cartella = os.path.join(CACHE, 'mesh')
    os.makedirs(cartella, exist_ok=True)
    p_indice = os.path.join(cartella, 'indice.json')
    indice = json.load(open(p_indice, encoding='utf-8')) if os.path.exists(p_indice) else {}
    comp = {}

    def trova(c):
        comp.setdefault(c.name, c)
        for o in c.occurrences:
            trova(o.component)
    trova(root)
    fatti, restano = [], []
    for nome, info in man['componenti'].items():
        if solo and nome not in solo:
            continue
        if not forza and indice.get(nome) == info['revisione'] and os.path.exists(os.path.join(cartella, info['mesh'])):
            continue
        if time.time() - t0 > budget_s:
            restano.append(nome)
            continue
        c = comp[nome]
        nv, nf = _scrivi_ply(os.path.join(cartella, info['mesh']), _corpi(c, adsk.core.Matrix3D.create()), info['tipo'] == 'comprato')
        indice[nome] = info['revisione']
        fatti.append('%s %d' % (nome, nf))
        with open(p_indice, 'w', encoding='utf-8') as f:
            json.dump(indice, f, indent=1, sort_keys=True)
    return {'fatti': fatti, 'restano': len(restano), 's': round(time.time() - t0, 1)}


# ------------------------------------------------------------------------------------------------ main
def main(passi, **kw):
    out = {'passi': passi}
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        V['controlla'](app)
        if des.snapshots.hasPendingSnapshot:
            raise RuntimeError('posa pendente: ripristinare prima di esportare per la guida')
        root = des.rootComponent
        if 'manifest' in passi:
            out['manifest'] = manifest(des, root)
        if 'mesh' in passi:
            out['mesh'] = mesh(des, root, kw.get('budget_s', 25.0), kw.get('forza', False), kw.get('solo'))
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out
