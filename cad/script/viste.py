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
           'Cover_Femore_B': (0, -95, 0), 'Cover_Femore_A_Feritoia': (0, 105, 0), 'Cover_Femore_B_Feritoia': (0, -95, 0),
           'Cover_Tibia': (34, 0, 0), 'Cover_Tibia_Diffusore': (17, 0, 0),
           'Piedino': (0, 0, -30)}
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
    # predisposizioni 2.1.0 (D-066)
    'Corpo_Supporto_INA260_S': (0, 0, 52), 'Corpo_Supporto_INA260_D': (0, 0, 52), 'Rif_INA260': (0, 0, 74),
    'Rif_Interruttore_Pololu_2813': (0, 0, 40), 'Rif_IMU': (0, 0, 40), 'Rif_ADC_ADS7830': (0, 0, 40), 'Rif_Prese_Piedi': (0, 0, 40), 'Rif_Partitori': (0, 0, 40),
    'Rif_ToF_8x8': (18, 0, 72), 'Corpo_Tappo_ToF': (14, 0, 150), 'Rif_ToF_1': (-12, 0, 150), 'Rif_Altoparlante': (-12, 0, 150),
    'Rif_Microfono_I2S': (0, 0, 132), 'Corpo_Fondo_Anello': (0, 0, 132), 'Rif_Ampli_MAX98357A': (0, 0, 132), 'Rif_Scheda_Carapace': (0, 0, 132),
    # moduli e pezzi della 2.1.6 (D-074)
    'Rif_IMU_MPU6500': (0, 0, 40), 'Corpo_Piastrina_IMU': (0, 0, 40), 'Rif_Altoparlante_Tondo': (-12, 0, 150),
    'Rif_Microfono_MS3625': (0, 0, 132), 'Corpo_Lunette_Microfoni': (0, 0, 132), 'Rif_Ampli_Generico': (0, 0, 132),
}

# inquadrature: (direzione dell'occhio, terna 'robot' o 'zampa', bersaglio in mm nella stessa terna, ampiezza in cm)
VISTE = {
    'montato_ant': ((1.0, 0.72, 0.62), 'robot', (0, 0, -38), 54.0),
    'montato_post': ((-1.0, -0.72, 0.62), 'robot', (0, 0, -38), 54.0),
    'montato_fianco': ((0.12, 1.0, 0.22), 'robot', (0, 0, -40), 46.0),
    'esploso_zampa': ((0.72, 0.58, 0.36), 'zampa', (70, 5, -75), 36.0),
    'esploso_corpo': ((1.0, 0.85, 0.5), 'robot', (0, 0, 38), 54.0),
    # render notturni (D-072): piu' bassi e piu' stretti, con le luci accese
    'notte_ant': ((1.0, 0.62, 0.34), 'robot', (0, 0, -40), 42.0),
    'notte_alto': ((0.75, 0.55, 0.95), 'robot', (0, 0, -25), 36.0),
}
# luci del render notturno: le WS2812B fanno qualunque colore, nel render uno solo (ciano). Aspetto emissivo copiato da
# "LED (blu)" della libreria; la luminanza e l'esposizione sono tarate a occhio sul render
# i pixel dei lobi stanno sotto 2,2 mm di PLA (piastrina e pelle): hanno un aspetto piu' luminoso
LUCE = {'nome': 'Esa luce notte', 'colore': (70, 210, 255), 'luminanza': 400.0, 'nome_pixel': 'Esa luce notte pixel',
        'luminanza_pixel': 6000.0}
NOTTE = {'ambiente': 'Evidenziazioni del bordo', 'luminosita': 10.0, 'esposizione': 6.0, 'sfondo': (4, 5, 8)}
GIORNO = {'luminosita': 1000.0, 'esposizione': 12.0}     # valori originali della scena del design


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
    n_luci = luci(True) if nome.startswith('notte') else 0
    print(json.dumps({'vista': nome, 'posa_pendente': des.snapshots.hasPendingSnapshot, 'luci': n_luci}))


def scena(notte=False):
    """Scena del render: ambiente da studio, sfondo chiaro a tinta unita, suolo con le ombre, prospettiva. Di notte
    (D-072): ambiente quasi spento che lascia solo le luci di bordo, sfondo nero, suolo lucido che riflette le luci."""
    rm = _des().renderManager
    ss = rm.sceneSettings
    env = [e for e in rm.renderEnvironments if e.name == (NOTTE['ambiente'] if notte else 'Cabina per fototessere')]
    # il tipo di sfondo e' in sola lettura: lo cambia l'assegnazione dell'ambiente o del colore (l'ambiente resta
    # come illuminazione anche con lo sfondo a tinta unita)
    if env:
        ss.backgroundEnvironment = env[0]
    ss.backgroundSolidColor = adsk.core.Color.create(*(NOTTE['sfondo'] if notte else (244, 245, 247)), 255)
    ss.brightness = NOTTE['luminosita'] if notte else GIORNO['luminosita']
    ss.cameraExposure = NOTTE['esposizione'] if notte else GIORNO['esposizione']
    ss.isGroundDisplayed = True
    ss.isGroundReflections = notte
    if notte:                                  # la ruvidita' si imposta solo con i riflessi accesi
        ss.groundRoughness = 0.25
    ss.cameraType = adsk.core.CameraTypes.PerspectiveCameraType
    ss.cameraFocalLength = FOCALE


def _aspetto_luce(des, nome, luminanza):
    """Aspetto emissivo del design per le luci accese (copia di "LED (blu)" con il colore di LUCE e la luminanza data)."""
    a = des.appearances.itemByName(nome)
    if a is None:
        lib = [m for m in adsk.core.Application.get().materialLibraries if m.name == 'Libreria aspetti di Fusion'][0]
        a = des.appearances.addByCopy(lib.appearances.itemByName('LED (blu)'), nome)
    a.appearanceProperties.itemById('opaque_luminance_modifier').value = adsk.core.Color.create(*LUCE['colore'], 255)
    a.appearanceProperties.itemById('opaque_albedo').value = adsk.core.Color.create(*LUCE['colore'], 255)
    a.appearanceProperties.itemById('opaque_luminance').value = luminanza
    return a


def _facce_luci(des):
    """Facce del carapace da cui esce la luce: sotto dell'anello del pulsante assottigliato e piastrine delle luci dei lobi."""
    comp = [c for c in des.allComponents if c.name == 'Corpo_Carapace'][0]
    mm = lambda e: des.unitsManager.evaluateExpression(e, 'mm') * 10
    z_anello, z_lobi = mm('car_top - luc_bianco'), mm('car_top - car_sp - 0.6 mm')
    xp, r1 = mm('car_puls_x'), mm('luc_anello_r1')
    out = []
    for b in comp.bRepBodies:
        for fa in b.faces:
            g = fa.geometry
            if g.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType or abs(abs(g.normal.z) - 1) > 1e-6:
                continue
            p, area = fa.pointOnFace, fa.area * 100
            if abs(p.z * 10 - z_anello) < 0.01 and abs(p.x * 10 - xp) < r1 + 0.1 and abs(p.y * 10) < r1 + 0.1:
                out.append(fa)
            elif abs(p.z * 10 - z_lobi) < 0.01 and 60 < area < 160:
                out.append(fa)
    return out


PIXEL = 'Luci_Notte_Provvisorie'


def _pixel_lobi(des, led):
    """Due pixel emissivi rivolti in alto sotto ogni piastrina delle luci dei lobi, in un componente provvisorio alla
    radice (lo cancella luci(False)): la faccia della piastrina emette verso il basso e non illumina il bianco sopra."""
    root = des.rootComponent
    car = [o for o in root.allOccurrences if o.component.name == 'Corpo_Carapace'][0]
    z_lobi = des.unitsManager.evaluateExpression('car_top - car_sp - 0.6 mm', 'mm')     # cm, terna del carapace
    passo = 25.4 / 3 / 10                                       # due pixel a 120 LED/m, in cm
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = PIXEL
    comp = occ.component
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    tbm = adsk.fusion.TemporaryBRepManager.get()
    n = 0
    for b in car.bRepBodies:
        for fa in b.faces:
            g = fa.geometry
            if g.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType or abs(abs(g.normal.z) - 1) > 1e-6:
                continue
            if abs(fa.nativeObject.pointOnFace.z - z_lobi) > 0.001 or not 0.6 < fa.area < 1.6:
                continue
            lati = [e for e in fa.edges if e.geometry.curveType == adsk.core.Curve3DTypes.Line3DCurveType]
            e = max(lati, key=lambda x: x.length)
            a, z = e.startVertex.geometry, e.endVertex.geometry
            u = adsk.core.Vector3D.create(z.x - a.x, z.y - a.y, 0)
            u.normalize()
            w = adsk.core.Vector3D.create(-u.y, u.x, 0)
            bb = fa.boundingBox
            c = [(bb.minPoint.x + bb.maxPoint.x) / 2, (bb.minPoint.y + bb.maxPoint.y) / 2, bb.minPoint.z - 0.025]
            for k in (-0.5, 0.5):
                centro = adsk.core.Point3D.create(c[0] + k * passo * u.x, c[1] + k * passo * u.y, c[2])
                obb = adsk.core.OrientedBoundingBox3D.create(centro, u, w, 0.25, 0.25, 0.04)
                comp.bRepBodies.add(tbm.createBox(obb), bf)
                n += 1
    bf.finishEdit()
    for corpo in comp.bRepBodies:
        corpo.appearance = led
    return n


def luci(accese):
    """Accende o spegne le luci per il render notturno (D-072): PLA bianco traslucido, facce delle luci del carapace e
    diffusori delle tibie emissivi. Spente: niente override sulle facce, PLA opaco, aspetti dei pezzi da colori.py."""
    des = _des()
    pla = des.appearances.itemByName('Esa PLA placche')
    pla.appearanceProperties.itemById('opaque_translucency').value = bool(accese)
    car = [c for c in des.allComponents if c.name == 'Corpo_Carapace'][0]
    n = 0
    if accese:
        led = _aspetto_luce(des, LUCE['nome'], LUCE['luminanza'])
        for fa in _facce_luci(des):
            fa.appearance = led
            n += 1
        for c in [c for c in des.allComponents if c.name == 'Cover_Tibia_Diffusore']:
            for b in c.bRepBodies:
                b.appearance = led
                n += 1
        n += _pixel_lobi(des, _aspetto_luce(des, LUCE['nome_pixel'], LUCE['luminanza_pixel']))
    else:
        for o in [o for o in des.rootComponent.occurrences if o.component.name == PIXEL]:
            o.deleteMe()
        for b in car.bRepBodies:
            for fa in b.faces:
                if fa.appearanceSourceType in (adsk.core.AppearanceSourceTypes.FaceAppearanceSource,
                                               adsk.core.AppearanceSourceTypes.OverrideAppearanceSource):
                    fa.appearance = None
                    n += 1
        import io
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'colori.py'))['main']()
    return n


def avvia(file, qualita=75, larghezza=1800, altezza=1200, notte=False):
    V['controlla'](adsk.core.Application.get())
    scena(notte)
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
        o.isLightBulbOn = not o.component.name.startswith(('Rif_', 'Dima_', 'Attrezzo_'))     # libreria e attrezzi restano spenti
    _flat(root, True)
    for c in [root] + [o.component for o in root.allOccurrences if o.component.name in ('Zampa', 'Corpo')]:
        c.isJointsFolderLightBulbOn = True
    spente = luci(False)
    scena()
    print(json.dumps({'posa_pendente': des.snapshots.hasPendingSnapshot, 'override_tolti': spente}))
