"""Viste e render del robot con il motore di rendering di Fusion: robot montato ed esplosi di zampa e corpo.

Gli esplosi spostano i pezzi lungo i loro assi di montaggio impostando transform2 sui proxy senza catturare la posizione:
il design non cambia, `ripristina` annulla la posa pendente e rimette la visibilita'. Il render locale gira in
background e scrive il file solo alla fine: la vista va lasciata com'e' finche' il file non c'e', poi `ripristina`.

Uso dal connettore (una chiamata per passo):
    v = runpy.run_path('/Users/paul/hexapod-v2/cad/script/viste.py')
    v['prepara']('esploso_zampa')            # esplode, nasconde il resto, inquadra
    v['avvia']('/percorso/file.png')        # scena e render locale
    ... (aspettare il file)
    v['ripristina']()
"""
import json
import math
import os
import runpy

import adsk.core
import adsk.fusion

V = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'versione.py'))
FOCALE = 50.0         # mm, focale della camera del render

# terna della zampa: X verso l'esterno, Y lungo gli assi di femore e ginocchio verso la piastra A, Z in alto (mm)
LC, LF = 55.0, 65.0


def _spost_zampa(nome, x):
    """Spostamento (mm, terna della zampa) di un pezzo della zampa nell'esploso; x = posizione del pezzo lungo la zampa."""
    coxa = abs(x) < 1
    tab = {'Coxa_Ponte': (0, 0, 35), 'Rif_Servo_MG996R': (0, 25, 0), 'Femore_A': (0, 65, 0), 'Ingombro_Teste_A': (0, 85, 0),
           'Cover_Femore_A': (0, 105, 0), 'Rif_Cuscinetto_LF1050ZZ': (0, -22, 0), 'Femore_B': (0, -48, 0),
           'Cover_Femore_B': (0, -95, 0), 'Cover_Tibia': (30, 0, 0), 'Piedino': (0, 0, -30)}
    if nome == 'Rif_Squadretta_25T':
        return (0, 0, 18) if coxa else (0, 45, 0)
    if nome == 'Rif_Perno_5':
        return (0, 0, -35) if coxa else (0, -75, 0)
    if nome in tab:
        return tab[nome]
    return (0, 0, 0)


SPOST_CORPO = {
    'Corpo_Carapace': (0, 0, 150), 'Corpo_Fascia': (0, 0, 150), 'Corpo_Visiera': (0, 0, 150), 'Corpo_Gonne': (0, 0, 150),
    'Corpo_Sportello_Servizio': (0, 0, 172), 'Rif_Pulsante_12': (0, 0, 190), 'Rif_Cicalino_BX100': (0, 0, 118),
    'Corpo_Vassoio': (0, 0, 72), 'Rif_Basetta_50x70': (0, 0, 86), 'Rif_ESP32_S3_CAM': (0, 0, 100), 'Rif_Camera_OV3660_75': (18, 0, 72),
    'Rif_SSC32_V25': (0, 0, 40), 'Rif_Wago_221_415': (0, 0, 48), 'Rif_Portafusibile_ATO': (0, 0, 32), 'Rif_Tplug': (0, 0, 48),
    'Corpo_Slitta_Regolatore': (0, 0, 52), 'Rif_Reg_Servo_D42V110F6': (0, 0, 74), 'Rif_Servo_MG996R': (0, 0, 32),
    'Rif_Cuscinetto_LF1050ZZ': (0, 0, -30), 'Rif_Batteria_2S5200': (0, 0, -52), 'Corpo_Chiglia': (0, 0, -100),
    'Corpo_Sportello': (-45, 0, -52),
}

# inquadrature: (direzione dell'occhio, terna 'robot' o 'zampa', bersaglio in mm nella stessa terna, ampiezza in cm)
VISTE = {
    'montato_ant': ((1.0, 0.72, 0.62), 'robot', (0, 0, -38), 46.0),
    'montato_post': ((-1.0, -0.72, 0.62), 'robot', (0, 0, -38), 46.0),
    'montato_fianco': ((0.12, 1.0, 0.22), 'robot', (0, 0, -40), 30.0),
    'esploso_zampa': ((0.72, 0.58, 0.36), 'zampa', (70, 5, -75), 36.0),
    'esploso_corpo': ((1.0, 0.85, 0.5), 'robot', (0, 0, 38), 47.0),
}


def _des():
    return adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)


def _zampa(root, n):
    """Istanza di Zampa per nome di coxa (AS, MS, PS, AD, MD, PD), come assieme.py -> mappa_zampe."""
    coxe = {'AS': (80, 44), 'MS': (0, 48), 'PS': (-80, 44), 'AD': (80, -44), 'MD': (0, -48), 'PD': (-80, -44)}
    x, y = coxe[n]
    zampe = [o for o in root.occurrences if o.component.name == 'Zampa']
    return min(zampe, key=lambda o: math.hypot(o.transform2.translation.x * 10 - x, o.transform2.translation.y * 10 - y))


def _sposta(o, v_mm):
    m = o.transform2.copy()
    t = m.translation
    t.add(adsk.core.Vector3D.create(v_mm[0] / 10, v_mm[1] / 10, v_mm[2] / 10))
    m.translation = t
    o.transform2 = m


def _visibili(root, quali):
    """Accende solo le occorrenze di primo livello indicate (Corpo, istanze di Zampa); la libreria resta spenta."""
    for o in root.occurrences:
        o.isLightBulbOn = o in quali


def _flat(root, acceso):
    corpo = [o for o in root.occurrences if o.component.name == 'Corpo'][0]
    for o in corpo.childOccurrences:
        if o.component.name == 'Rif_Camera_OV3660_75':
            for b in o.bRepBodies:
                if b.name in ('flat', 'linguetta'):
                    b.isLightBulbOn = acceso       # striscia dritta nel modello: quella vera si piega sotto il carapace


def _inquadra(nome, zo=None):
    d, terna, bersaglio, ampiezza = VISTE[nome]
    app = adsk.core.Application.get()
    if terna == 'zampa':
        m = zo.transform2
        o, ax = m.getAsCoordinateSystem()[0], m.getAsCoordinateSystem()[1:]
        w = lambda v: [sum(v[i] * (ax[i].x, ax[i].y, ax[i].z)[k] for i in range(3)) for k in range(3)]
        dd = w(d)
        tb = [o.x * 10 + c for c in w(bersaglio)]
    else:
        dd, tb = list(d), list(bersaglio)
    n = math.sqrt(sum(c * c for c in dd))
    # il render usa la focale della scena (FOCALE, pellicola 36 x 24): l'occhio sta alla distanza che fa entrare
    # l'ampiezza in verticale; la vista di Fusion usa lo stesso angolo
    angolo = 2 * math.atan(12.0 / FOCALE)
    dist = ampiezza / 2 / math.tan(angolo / 2)
    vp = app.activeViewport
    cam = vp.camera
    cam.cameraType = adsk.core.CameraTypes.PerspectiveCameraType
    cam.perspectiveAngle = angolo
    cam.target = adsk.core.Point3D.create(tb[0] / 10, tb[1] / 10, tb[2] / 10)
    cam.eye = adsk.core.Point3D.create(tb[0] / 10 + dist * dd[0] / n, tb[1] / 10 + dist * dd[1] / n, tb[2] / 10 + dist * dd[2] / n)
    cam.upVector = adsk.core.Vector3D.create(0, 0, 1)
    cam.isFitView = False
    vp.camera = cam
    vp.refresh()


def prepara(nome, zampa='AS'):
    V['controlla'](adsk.core.Application.get())
    des = _des()
    root = des.rootComponent
    if des.snapshots.hasPendingSnapshot:
        des.snapshots.revertPendingSnapshot()
    for c in [root] + [o.component for o in root.allOccurrences if o.component.name in ('Zampa', 'Corpo')]:
        c.isJointsFolderLightBulbOn = False
    adsk.core.Application.get().userInterface.activeSelections.clear()
    _flat(root, False)
    corpo = [o for o in root.occurrences if o.component.name == 'Corpo'][0]
    zampe = [o for o in root.occurrences if o.component.name == 'Zampa']
    zo = None
    if nome == 'esploso_zampa':
        zo = _zampa(root, zampa)
        _visibili(root, [zo])
        for o in zo.childOccurrences:
            x = o.nativeObject.transform2.translation.x * 10
            v = _spost_zampa(o.component.name, x)
            if any(v):
                ax = zo.transform2.getAsCoordinateSystem()[1:]
                _sposta(o, [sum(v[i] * (ax[i].x, ax[i].y, ax[i].z)[k] for i in range(3)) for k in range(3)])
    elif nome == 'esploso_corpo':
        _visibili(root, [corpo])
        for o in corpo.childOccurrences:
            v = SPOST_CORPO.get(o.component.name)
            if v:
                _sposta(o, v)
    else:
        _visibili(root, [corpo] + zampe)
    _inquadra(nome, zo)
    print(json.dumps({'vista': nome, 'posa_pendente': des.snapshots.hasPendingSnapshot}))


def scena():
    """Scena del render: ambiente da studio, sfondo chiaro a tinta unita, suolo con le ombre, prospettiva."""
    rm = _des().renderManager
    ss = rm.sceneSettings
    env = [e for e in rm.renderEnvironments if e.name == 'Cabina per fototessere']
    # il tipo di sfondo e' in sola lettura: lo cambia l'assegnazione dell'ambiente o del colore (l'ambiente resta
    # come illuminazione anche con lo sfondo a tinta unita)
    if env:
        ss.backgroundEnvironment = env[0]
    ss.backgroundSolidColor = adsk.core.Color.create(244, 245, 247, 255)
    ss.isGroundDisplayed = True
    ss.isGroundReflections = False
    ss.cameraType = adsk.core.CameraTypes.PerspectiveCameraType
    ss.cameraFocalLength = FOCALE


def avvia(file, qualita=75, larghezza=1800, altezza=1200):
    V['controlla'](adsk.core.Application.get())
    scena()
    r = _des().renderManager.rendering
    r.renderQuality = qualita
    r.aspectRatio = adsk.fusion.RenderAspectRatios.CustomRenderAspectRatio
    r.resolution = adsk.fusion.RenderResolutions.CustomRenderResolution
    r.resolutionWidth = larghezza
    r.resolutionHeight = altezza
    r.isBackgroundTransparent = False
    f = r.startLocalRender(file)
    print(json.dumps({'file': f.filename, 'stato': str(f.renderState), 'avanzamento': f.progress}))


def ripristina():
    # tornare a Progettazione passando dall'area Rendering: attivando Progettazione direttamente dopo un render la
    # vista e' rimasta con lo sfondo chiaro e i pezzi bianchi, senza aspetti (9 ottobre 2026)
    app = adsk.core.Application.get()
    _des().renderManager.activateRenderWorkspace()
    app.userInterface.workspaces.itemById('FusionSolidEnvironment').activate()
    des = _des()
    root = des.rootComponent
    if des.snapshots.hasPendingSnapshot:
        des.snapshots.revertPendingSnapshot()
    for o in root.occurrences:
        o.isLightBulbOn = not o.component.name.startswith('Rif_')     # la libreria dei componenti resta spenta
    _flat(root, True)
    for c in [root] + [o.component for o in root.allOccurrences if o.component.name in ('Zampa', 'Corpo')]:
        c.isJointsFolderLightBulbOn = True
    print(json.dumps({'posa_pendente': des.snapshots.hasPendingSnapshot}))
