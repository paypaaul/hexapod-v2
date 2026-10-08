"""Funzioni generiche per assiemi via API Fusion: istanze, giunti, interferenze, pose, viste.

Estratte dagli script della prima versione del robot (branch `mg90s`: cad/script/zampa.py e assieme.py),
dove la logica e' stata provata sul modello. In questa forma generica NON sono ancora state rieseguite:
al primo uso controllare il risultato rileggendo lo stato del modello in uno script a parte.

Regole imparate (dettagli in CLAUDE.md, "Connettore Fusion"):
  - un'istanza dentro un sotto-assieme si crea alla radice e poi si sposta con moveToComponent;
  - i riferimenti esterni nascono composti con la trasformata dell'occorrenza di libreria e fissati al genitore;
  - letture fatte nello stesso script che ha creato istanze o giunti possono essere vecchie;
  - i giunti dentro un sotto-assieme ripetuto sono condivisi: per atteggiare le singole istanze si impone
    la trasformata delle parti annidate, e la posa resta non catturata.
"""
import math

import adsk.core
import adsk.fusion

P3 = adsk.core.Point3D.create
V3 = adsk.core.Vector3D.create


# ----------------------------------------------------------------------------------- matrici
def matrice(origine_mm, ex, ey, ez):
    """Matrice da origine (mm) e versori degli assi."""
    m = adsk.core.Matrix3D.create()
    m.setWithCoordinateSystem(P3(origine_mm[0] / 10, origine_mm[1] / 10, origine_mm[2] / 10), V3(*ex), V3(*ey), V3(*ez))
    return m


def rotazione(gradi, asse, punto_mm):
    """Rotazione di `gradi` attorno all'asse dato passante per un punto (mm)."""
    m = adsk.core.Matrix3D.create()
    m.setToRotation(math.radians(gradi), V3(*asse), P3(punto_mm[0] / 10, punto_mm[1] / 10, punto_mm[2] / 10))
    return m


def componi(*matrici):
    """Composizione: la prima matrice si applica per prima. (A.transformBy(B) = prima A, poi B.)"""
    m = matrici[0].copy()
    for altra in matrici[1:]:
        m.transformBy(altra)
    return m


# ----------------------------------------------------------------------------------- istanze
def aggiungi_istanza(root, occ_libreria, m_radice, dentro=None):
    """Nuova istanza del componente di `occ_libreria` nella posa `m_radice` (terna della radice).

    Se `dentro` e' un'occorrenza, l'istanza viene spostata nel suo componente conservando la posizione
    nello spazio: aggiungerla direttamente dentro un sotto-assieme non all'origine sbaglia la posa.
    """
    w = m_radice.copy()
    if occ_libreria.isReferencedComponent:
        # un riferimento esterno nasce in w * T_libreria: si passa w * T_libreria^-1
        inv = occ_libreria.transform2.copy()
        inv.invert()
        inv.transformBy(w)
        w = inv
    occ = root.occurrences.addExistingComponent(occ_libreria.component, w)
    if dentro is not None:
        occ = occ.moveToComponent(dentro)
    try:
        if occ.isGroundToParent:        # i riferimenti esterni nascono fissati: bloccherebbero i giunti
            occ.isGroundToParent = False
    except Exception:
        pass
    return occ


def piu_vicina(occorrenze, punto_mm):
    """Occorrenza la cui origine e' piu' vicina al punto dato (mm): l'ordine delle occorrenze non e' affidabile."""
    def distanza(o):
        t = o.transform2.translation
        return math.dist((t.x * 10, t.y * 10, t.z * 10)[:len(punto_mm)], punto_mm)
    return min(occorrenze, key=distanza)


# ----------------------------------------------------------------------------------- giunti
def faccia_cilindrica(occ, raggio_mm, punto_mm, asse):
    """Faccia cilindrica del primo corpo di `occ` con raggio e asse dati, passante per un punto (terna di `occ`)."""
    indice = {'x': 0, 'y': 1, 'z': 2}[asse]
    for f in occ.bRepBodies.item(0).faces:
        g = f.geometry
        if g.surfaceType != adsk.core.SurfaceTypes.CylinderSurfaceType or abs(g.radius * 10 - raggio_mm) > 1e-3:
            continue
        a = g.axis
        if abs(abs((a.x, a.y, a.z)[indice]) - 1) > 1e-4:
            continue
        o = g.origin
        d = [o.x * 10 - punto_mm[0], o.y * 10 - punto_mm[1], o.z * 10 - punto_mm[2]]
        d[indice] = 0
        if math.sqrt(sum(c * c for c in d)) < 1e-3:
            return f
    return None


def giunto_rigido(comp, a, b, nome):
    """Giunto rigido "come costruito" tra due occorrenze, creato nel componente `comp`."""
    inp = comp.asBuiltJoints.createInput(a, b, None)
    inp.setAsRigidJointMotion()
    j = comp.asBuiltJoints.add(inp)
    j.name = nome
    return j


def giunto_rivoluzione(comp, mobile, fisso, faccia, nome, limiti_gradi=None):
    """Giunto di rivoluzione "come costruito" sull'asse di una faccia cilindrica; limiti = (min, max) in gradi.

    Un valore oltre il limite viene rifiutato: verificare le escursioni PRIMA di impostare i limiti.
    """
    geo = adsk.fusion.JointGeometry.createByNonPlanarFace(faccia, adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)
    inp = comp.asBuiltJoints.createInput(mobile, fisso, geo)
    inp.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
    j = comp.asBuiltJoints.add(inp)
    j.name = nome
    if limiti_gradi is not None:
        imposta_limiti(j, *limiti_gradi)
    return j


def imposta_limiti(giunto, minimo_gradi, massimo_gradi):
    lim = adsk.fusion.RevoluteJointMotion.cast(giunto.jointMotion).rotationLimits
    lim.isMinimumValueEnabled = True
    lim.minimumValue = math.radians(minimo_gradi)
    lim.isMaximumValueEnabled = True
    lim.maximumValue = math.radians(massimo_gradi)


def valore_giunto(giunto):
    return math.degrees(adsk.fusion.RevoluteJointMotion.cast(giunto.jointMotion).rotationValue)


# ----------------------------------------------------------------------------------- controlli
def interferenze(des, occorrenze, scarta=None):
    """Interferenze tra le occorrenze date: [(percorso a, percorso b, volume mm3)].

    Scarta le coppie di corpi della stessa occorrenza (ingombri fatti di piu' corpi sovrapposti) e
    quelle per cui `scarta(nome corpo a, nome corpo b, percorso a, percorso b)` e' vero.
    """
    col = adsk.core.ObjectCollection.create()
    for o in occorrenze:
        col.add(o)
    res = des.analyzeInterference(des.createInterferenceInput(col))
    out = []
    for i in range(res.count):
        r = res.item(i)
        nomi = []
        for e in (r.entityOne, r.entityTwo):
            occ = getattr(e, 'assemblyContext', None)
            nomi.append(occ.fullPathName if occ else e.parentComponent.name)
        if nomi[0] == nomi[1]:
            continue
        if scarta and scarta(r.entityOne.name, r.entityTwo.name, nomi[0], nomi[1]):
            continue
        out.append((nomi[0], nomi[1], round(r.interferenceBody.volume * 1000, 2)))
    return out


def sentinella(des, attesi, tolleranza_mm3=0.05):
    """Confronta i volumi (mm3) dei componenti con quelli attesi: {nome componente: volume}.

    Un taglio fatto senza limitare i corpi partecipanti asporta anche le parti degli altri componenti,
    senza errori: questo controllo va fatto dopo ogni lavoro su una parte.
    """
    diversi = {}
    for c in des.allComponents:
        if c.name in attesi:
            vol = round(sum(b.volume for b in c.bRepBodies) * 1000, 2)
            if abs(vol - attesi[c.name]) > tolleranza_mm3 or c.bRepBodies.count != 1:
                diversi[c.name] = {'volume': vol, 'atteso': attesi[c.name], 'corpi': c.bRepBodies.count}
    return diversi or 'invariati'


def massa_e_baricentro(foglie, densita, stampate, comprate):
    """Massa (g) e baricentro (mm) dalle occorrenze foglia.

    stampate = {nome componente: riempimento medio}; massa = volume x densita' (g/cm3) x riempimento.
    comprate = {prefisso del nome: (massa in g, nome del corpo di riferimento o None)}.
    """
    tot, mom, voci = 0.0, [0.0, 0.0, 0.0], {}
    for o in foglie:
        nome = o.component.name
        if nome in stampate:
            b = o.bRepBodies.item(0)
            m, chiave = b.volume * densita * stampate[nome], nome
        else:
            pref = [k for k in comprate if nome.startswith(k)]
            if not pref:
                continue
            m, rif = comprate[pref[0]]
            b = ([x for x in o.bRepBodies if x.name == rif] or [o.bRepBodies.item(0)])[0]
            chiave = pref[0]
        g = b.physicalProperties.centerOfMass
        tot += m
        for i, c in enumerate((g.x, g.y, g.z)):
            mom[i] += m * c * 10
        v = voci.setdefault(chiave, [0, 0.0])
        v[0] += 1
        v[1] += m
    return {'voci': {k: [n, round(m, 1)] for k, (n, m) in voci.items()}, 'totale_g': round(tot, 1),
            'baricentro_mm': [round(c / tot, 2) for c in mom] if tot else None}


# ----------------------------------------------------------------------------------- pose
def ik_piano(x_f, h, lf, lt):
    """Cinematica inversa nel piano della zampa, ginocchio in alto: (alpha, gamma) in gradi.

    x_f = distanza orizzontale del piede dall'asse del femore, h = altezza dell'asse dal piede;
    alpha = femore sopra l'orizzontale, gamma = angolo interno al ginocchio (180 = zampa distesa).
    """
    d = math.hypot(x_f, h)
    alpha = math.atan2(-h, x_f) + math.acos((lf * lf + d * d - lt * lt) / (2 * lf * d))
    gamma = math.acos((lf * lf + lt * lt - d * d) / (2 * lf * lt))
    return math.degrees(alpha), math.degrees(gamma)


def imponi_posa(occ_istanza, parti, catene, riferimento):
    """Impone la posa alle parti annidate di UNA istanza di un sotto-assieme.

    parti = {chiave: occorrenza nativa}; riferimento = {chiave: trasformata nativa a giunti azzerati};
    catene = {chiave: [matrici da applicare in ordine, nella terna del sotto-assieme]}.
    La posa resta non catturata: ripristina() la annulla.
    """
    for chiave, o in parti.items():
        m = riferimento[chiave].copy()
        for r in catene[chiave]:
            m.transformBy(r)
        m.transformBy(occ_istanza.transform2)
        o.createForAssemblyContext(occ_istanza).transform2 = m


def ripristina(des):
    """Annulla le pose non catturate (torna alla posa salvata)."""
    if des.snapshots.hasPendingSnapshot:
        des.snapshots.revertPendingSnapshot()
    return not des.snapshots.hasPendingSnapshot


# ----------------------------------------------------------------------------------- viste
def vista(app, occhio_cm, bersaglio_cm=(0, 0, 0), estensione_cm=30, giunti_visibili=None, componenti=()):
    """Imposta la vista ortogonale per uno screenshot (poi: queryType screenshot, direction current).

    giunti_visibili = True / False mostra o nasconde le icone dei giunti dei componenti dati.
    """
    vp = app.activeViewport
    cam = vp.camera
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    cam.target = P3(*bersaglio_cm)
    cam.eye = P3(*occhio_cm)
    cam.upVector = V3(0, 0, 1) if (occhio_cm[0], occhio_cm[1]) != (bersaglio_cm[0], bersaglio_cm[1]) else V3(0, 1, 0)
    cam.viewExtents = estensione_cm
    cam.isSmoothTransition = False
    vp.camera = cam
    vp.refresh()
    if giunti_visibili is not None:
        for c in componenti:
            c.isJointsFolderLightBulbOn = giunti_visibili
