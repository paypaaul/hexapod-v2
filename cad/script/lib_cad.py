"""Funzioni di base per modellare le parti progettate via API Fusion.

Regole che la libreria fa rispettare:
  - ogni schizzo contiene UN solo contorno chiuso ed e' completamente vincolato
    (vincoli orizzontale/verticale + quote dall'origine legate a espressioni);
  - tutte le quote sono espressioni: parametri utente o loro combinazioni;
  - ogni piano, schizzo e lavorazione ha un nome.

Le espressioni di posizione hanno il segno (es. '-(cul_parete)'): la libreria le valuta
per piazzare la geometria e usa il valore assoluto nella quota. Se un parametro cambia
al punto da invertire il segno di una posizione, lo schizzo va rigenerato.
"""
import math

import adsk.core
import adsk.fusion

P3 = adsk.core.Point3D.create
VI = adsk.core.ValueInput
EPS = 1e-6

NUOVO = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
UNISCI = adsk.fusion.FeatureOperations.JoinFeatureOperation
TAGLIA = adsk.fusion.FeatureOperations.CutFeatureOperation


class Parte:
    """Costruttore di una parte dentro un componente."""

    def __init__(self, comp):
        self.c = comp
        self.des = comp.parentDesign
        self.non_vincolati = []
        self.n = 0
        self.piani = {}

    # ------------------------------------------------------------------ utilita'
    def val(self, expr):
        """Valore numerico in mm di un'espressione di lunghezza."""
        return self.des.unitsManager.evaluateExpression(expr, 'mm') * 10.0

    def _base(self, asse):
        return {'x': self.c.yZConstructionPlane, 'y': self.c.xZConstructionPlane,
                'z': self.c.xYConstructionPlane}[asse]

    def _segno(self, asse):
        n = self._base(asse).geometry.normal
        return 1.0 if {'x': n.x, 'y': n.y, 'z': n.z}[asse] > 0 else -1.0

    def piano(self, asse, expr, nome):
        """Piano perpendicolare a un asse del componente, alla quota `expr` (con segno)."""
        if abs(self.val(expr)) < EPS:
            return self._base(asse)
        if (asse, expr) in self.piani:          # stesso piano gia' creato da questa Parte: si riusa
            return self.piani[(asse, expr)]
        e = expr if self._segno(asse) > 0 else '-(%s)' % expr
        inp = self.c.constructionPlanes.createInput()
        inp.setByOffset(self._base(asse), VI.createByString(e))
        pl = self.c.constructionPlanes.add(inp)
        pl.name = 'pn_' + nome
        self.piani[(asse, expr)] = pl
        return pl

    def _schizzo(self, piano, nome):
        sk = self.c.sketches.add(piano)
        sk.name = 'sk_' + nome
        return sk

    @staticmethod
    def _uv(asse, m):
        """Coordinate nel piano (mm) di un punto modello (cm)."""
        if asse == 'y':
            return m.x * 10, m.z * 10
        if asse == 'z':
            return m.x * 10, m.y * 10
        return m.y * 10, m.z * 10

    @staticmethod
    def _modello(asse, u, v, q):
        if asse == 'y':
            return P3(u / 10, q / 10, v / 10)
        if asse == 'z':
            return P3(u / 10, v / 10, q / 10)
        return P3(q / 10, u / 10, v / 10)

    def _quota_da_origine(self, sk, punto, lungo_x, expr):
        """Vincola la distanza di `punto` dall'origine lungo x o y dello schizzo."""
        gc, dims = sk.geometricConstraints, sk.sketchDimensions
        v = self.val(expr)
        if abs(v) < EPS:
            if lungo_x:
                gc.addVerticalPoints(sk.originPoint, punto)      # stessa x dell'origine
            else:
                gc.addHorizontalPoints(sk.originPoint, punto)    # stessa y dell'origine
            return
        g = punto.geometry
        if lungo_x:
            d = dims.addDistanceDimension(sk.originPoint, punto,
                                          adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                                          P3(g.x / 2, g.y + 0.3, 0))
        else:
            d = dims.addDistanceDimension(sk.originPoint, punto,
                                          adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                                          P3(g.x + 0.3, g.y / 2, 0))
        d.parameter.expression = expr if v > 0 else '-(%s)' % expr

    def _controlla(self, sk):
        if not sk.isFullyConstrained:
            self.non_vincolati.append(sk.name)
        if sk.profiles.count != 1:
            raise RuntimeError('%s: attesi 1 profilo, trovati %d' % (sk.name, sk.profiles.count))

    # ------------------------------------------------------------------ primitive 2D
    def sk_rett(self, asse, q_expr, nome, u0, v0, u1, v1):
        """Schizzo con un rettangolo: lati alle quote u0, u1 e v0, v1 (espressioni con segno)."""
        piano = self.piano(asse, q_expr, nome)
        sk = self._schizzo(piano, nome)
        q = self.val(q_expr)
        a = sk.modelToSketchSpace(self._modello(asse, self.val(u0), self.val(v0), q))
        b = sk.modelToSketchSpace(self._modello(asse, self.val(u1), self.val(v1), q))
        linee = sk.sketchCurves.sketchLines.addTwoPointRectangle(P3(a.x, a.y, 0), P3(b.x, b.y, 0))
        gc = sk.geometricConstraints
        attese = {'u': [(self.val(u0), u0), (self.val(u1), u1)], 'v': [(self.val(v0), v0), (self.val(v1), v1)]}
        for i in range(linee.count):
            ln = linee.item(i)
            s, e = ln.startSketchPoint.geometry, ln.endSketchPoint.geometry
            verticale = abs(s.x - e.x) < EPS
            if verticale:
                gc.addVertical(ln)
            else:
                gc.addHorizontal(ln)
            # a quale lato del rettangolo (in coordinate modello) corrisponde questa linea?
            mid = sk.sketchToModelSpace(P3((s.x + e.x) / 2, (s.y + e.y) / 2, 0))
            ms, me = sk.sketchToModelSpace(s), sk.sketchToModelSpace(e)
            us, vs = self._uv(asse, ms)
            ue, ve = self._uv(asse, me)
            um, vm = self._uv(asse, mid)
            if abs(us - ue) < 1e-4:          # linea a u costante
                expr = min(attese['u'], key=lambda t: abs(t[0] - um))[1]
            else:
                expr = min(attese['v'], key=lambda t: abs(t[0] - vm))[1]
            self._quota_da_origine(sk, ln.startSketchPoint, verticale, expr)
        self._controlla(sk)
        return sk

    def sk_cerchio(self, asse, q_expr, nome, cu, cv, d_expr):
        """Schizzo con un cerchio: centro (cu, cv) e diametro come espressioni."""
        piano = self.piano(asse, q_expr, nome)
        sk = self._schizzo(piano, nome)
        q = self.val(q_expr)
        c = sk.modelToSketchSpace(self._modello(asse, self.val(cu), self.val(cv), q))
        cer = sk.sketchCurves.sketchCircles.addByCenterRadius(P3(c.x, c.y, 0), self.val(d_expr) / 20)
        # quale coordinata modello corre lungo x dello schizzo?
        ex = sk.sketchToModelSpace(P3(1, 0, 0))
        o = sk.sketchToModelSpace(P3(0, 0, 0))
        du, dv = self._uv(asse, P3(ex.x - o.x, ex.y - o.y, ex.z - o.z))
        u_lungo_x = abs(du) > abs(dv)
        centro = cer.centerSketchPoint
        if abs(self.val(cu)) < EPS and abs(self.val(cv)) < EPS:
            sk.geometricConstraints.addCoincident(centro, sk.originPoint)
        else:
            self._quota_da_origine(sk, centro, True, cu if u_lungo_x else cv)
            self._quota_da_origine(sk, centro, False, cv if u_lungo_x else cu)
        g = centro.geometry
        dd = sk.sketchDimensions.addDiameterDimension(cer, P3(g.x + 0.3, g.y + 0.3, 0))
        dd.parameter.expression = d_expr
        self._controlla(sk)
        return sk

    def sk_poligono(self, asse, q_expr, nome, vertici):
        """Schizzo con un poligono chiuso: vertici = [(u_expr, v_expr), ...] con segno.

        Ogni vertice e' quotato dall'origine lungo le due direzioni dello schizzo, quindi i lati
        possono avere qualunque inclinazione e le espressioni possono contenere seno e coseno.
        """
        piano = self.piano(asse, q_expr, nome)
        sk = self._schizzo(piano, nome)
        q = self.val(q_expr)
        pts = []
        for ue, ve in vertici:
            m = sk.modelToSketchSpace(self._modello(asse, self.val(ue), self.val(ve), q))
            pts.append(P3(m.x, m.y, 0))
        linee = sk.sketchCurves.sketchLines
        prima = linee.addByTwoPoints(pts[0], pts[1])
        ultima = prima
        segmenti = [prima]
        for i in range(2, len(pts)):
            ultima = linee.addByTwoPoints(ultima.endSketchPoint, pts[i])
            segmenti.append(ultima)
        segmenti.append(linee.addByTwoPoints(ultima.endSketchPoint, prima.startSketchPoint))
        # Fusion aggiunge da solo "orizzontale"/"verticale" ai lati che nascono allineati agli assi:
        # con i vertici quotati uno per uno lo schizzo diventerebbe ipervincolato, e i due estremi
        # resterebbero legati anche se le loro espressioni un giorno divergessero. Si tolgono.
        gc = sk.geometricConstraints
        for i in range(gc.count - 1, -1, -1):
            v = gc.item(i)
            if v.objectType in (adsk.fusion.HorizontalConstraint.classType(), adsk.fusion.VerticalConstraint.classType()):
                v.deleteMe()
        ex = sk.sketchToModelSpace(P3(1, 0, 0))
        o = sk.sketchToModelSpace(P3(0, 0, 0))
        du, dv = self._uv(asse, P3(ex.x - o.x, ex.y - o.y, ex.z - o.z))
        u_lungo_x = abs(du) > abs(dv)
        for seg, (ue, ve) in zip(segmenti, vertici):
            p0 = seg.startSketchPoint
            self._quota_da_origine(sk, p0, True, ue if u_lungo_x else ve)
            self._quota_da_origine(sk, p0, False, ve if u_lungo_x else ue)
        self._controlla(sk)
        return sk

    def sk_rett_obl(self, asse, q_expr, nome, p0, p1, a0, a1, b0, b1):
        """Schizzo con un rettangolo inclinato, definito in una terna locale.

        p0 = (u, v) origine locale, p1 = (u, v) punto che da' la direzione +a (espressioni con segno);
        b e' a ruotato di +90 gradi nel piano (u, v). I lati stanno ad a = a0, a1 e b = b0, b1
        (espressioni con segno). Vincoli: un asse di costruzione p0-p1 quotato dall'origine, lati
        paralleli o perpendicolari all'asse, distanze dall'asse e da p0. Nessun vertice e' quotato
        dall'origine: cosi' si evita lo "schizzo ipervincolato" del poligono.
        L'asse non deve essere parallelo agli assi dello schizzo (in quel caso si usa sk_rett).
        """
        piano = self.piano(asse, q_expr, nome)
        sk = self._schizzo(piano, nome)
        q = self.val(q_expr)
        u0, v0, u1, v1 = self.val(p0[0]), self.val(p0[1]), self.val(p1[0]), self.val(p1[1])
        lung = math.hypot(u1 - u0, v1 - v0)
        ea = ((u1 - u0) / lung, (v1 - v0) / lung)
        eb = (-ea[1], ea[0])

        def sp(u, v):
            m = sk.modelToSketchSpace(self._modello(asse, u, v, q))
            return P3(m.x, m.y, 0)

        def loc(a, b):
            return sp(u0 + a * ea[0] + b * eb[0], v0 + a * ea[1] + b * eb[1])

        linee = sk.sketchCurves.sketchLines
        gc, dims = sk.geometricConstraints, sk.sketchDimensions
        ax = linee.addByTwoPoints(sp(u0, v0), sp(u1, v1))
        ax.isConstruction = True
        ex = sk.sketchToModelSpace(P3(1, 0, 0))
        o = sk.sketchToModelSpace(P3(0, 0, 0))
        du, dv = self._uv(asse, P3(ex.x - o.x, ex.y - o.y, ex.z - o.z))
        u_lungo_x = abs(du) > abs(dv)
        for punto, (ue, ve) in ((ax.startSketchPoint, p0), (ax.endSketchPoint, p1)):
            self._quota_da_origine(sk, punto, True, ue if u_lungo_x else ve)
            self._quota_da_origine(sk, punto, False, ve if u_lungo_x else ue)
        va0, va1, vb0, vb1 = self.val(a0), self.val(a1), self.val(b0), self.val(b1)
        l1 = linee.addByTwoPoints(loc(va0, vb0), loc(va1, vb0))          # b = b0
        l2 = linee.addByTwoPoints(l1.endSketchPoint, loc(va1, vb1))      # a = a1
        l3 = linee.addByTwoPoints(l2.endSketchPoint, loc(va0, vb1))      # b = b1
        l4 = linee.addByTwoPoints(l3.endSketchPoint, l1.startSketchPoint)  # a = a0
        gc.addParallel(l1, ax)
        gc.addParallel(l3, ax)
        gc.addPerpendicular(l2, ax)
        gc.addPerpendicular(l4, ax)

        def medio(ln):
            s, e = ln.startSketchPoint.geometry, ln.endSketchPoint.geometry
            return P3((s.x + e.x) / 2, (s.y + e.y) / 2, 0)

        for ln, expr, val in ((l1, b0, vb0), (l3, b1, vb1)):
            if abs(val) < EPS:
                gc.addCollinear(ln, ax)
            else:
                d = dims.addOffsetDimension(ax, ln, medio(ln))
                d.parameter.expression = expr if val > 0 else '-(%s)' % expr
        for ln, expr, val in ((l2, a1, va1), (l4, a0, va0)):
            if abs(val) < EPS:
                gc.addCoincident(ax.startSketchPoint, ln)
            else:
                d = dims.addOffsetDimension(ln, ax.startSketchPoint, medio(ln))
                d.parameter.expression = expr if val > 0 else '-(%s)' % expr
        self._controlla(sk)
        return sk

    def blocco_obl(self, asse, q_expr, nome, p0, p1, a0, a1, b0, b1, dist_expr, verso=1, op=UNISCI):
        """Parallelepipedo inclinato: rettangolo in terna locale sul piano `asse = q`, estruso di `dist`."""
        sk = self.sk_rett_obl(asse, q_expr, nome, p0, p1, a0, a1, b0, b1)
        return self.estrudi(sk, asse, dist_expr, verso, op, nome)

    def specchia(self, lavorazioni, asse, nome):
        """Specchia un gruppo di lavorazioni rispetto al piano base perpendicolare a `asse`."""
        col = adsk.core.ObjectCollection.create()
        for f in lavorazioni:
            col.add(f)
        inp = self.c.features.mirrorFeatures.createInput(col, self._base(asse))
        inp.patternComputeOption = adsk.fusion.PatternComputeOptions.AdjustPatternCompute
        f = self.c.features.mirrorFeatures.add(inp)
        f.name = nome
        self.n += 1
        return f

    def prisma(self, asse, q_expr, nome, vertici, dist_expr, verso=1, op=UNISCI):
        """Prisma: poligono sul piano `asse = q` estruso di `dist` nel verso dato."""
        sk = self.sk_poligono(asse, q_expr, nome, vertici)
        return self.estrudi(sk, asse, dist_expr, verso, op, nome)

    def svuota(self, facce, spessore_expr, nome):
        """Svuotamento (shell) verso l'interno togliendo le facce date."""
        col = adsk.core.ObjectCollection.create()
        for f in facce:
            col.add(f)
        inp = self.c.features.shellFeatures.createInput(col, False)
        inp.insideThickness = VI.createByString(spessore_expr)
        f = self.c.features.shellFeatures.add(inp)
        f.name = nome
        self.n += 1
        return f

    # ------------------------------------------------------------------ lavorazioni 3D
    def estrudi(self, sk, asse, dist_expr, verso, op, nome):
        """Estrude l'unico profilo dello schizzo di `dist_expr` nel verso +1 / -1 dell'asse."""
        ext = self.c.features.extrudeFeatures
        inp = ext.createInput(sk.profiles.item(0), op)
        nx, ny = sk.xDirection, sk.yDirection
        nrm = nx.crossProduct(ny)
        comp_n = {'x': nrm.x, 'y': nrm.y, 'z': nrm.z}[asse]
        positivo = (comp_n > 0) == (verso > 0)
        d = adsk.fusion.DistanceExtentDefinition.create(VI.createByString(dist_expr))
        inp.setOneSideExtent(d, adsk.fusion.ExtentDirections.PositiveExtentDirection if positivo
                             else adsk.fusion.ExtentDirections.NegativeExtentDirection)
        if op == TAGLIA:
            # Senza questo un taglio asporta TUTTI i corpi che incontra, anche quelli degli altri
            # componenti dell'assieme (zampe, cuscinetti...): si limita ai corpi di questa parte.
            inp.participantBodies = [b for b in self.c.bRepBodies]
        f = ext.add(inp)
        f.name = nome
        self.n += 1
        return f

    def blocco(self, asse, q_expr, nome, u0, v0, u1, v1, dist_expr, verso=1, op=UNISCI):
        """Parallelepipedo: rettangolo sul piano `asse = q` estruso di `dist` nel verso dato."""
        sk = self.sk_rett(asse, q_expr, nome, u0, v0, u1, v1)
        return self.estrudi(sk, asse, dist_expr, verso, op, nome)

    def cilindro(self, asse, q_expr, nome, cu, cv, d_expr, dist_expr, verso=1, op=UNISCI):
        """Cilindro: cerchio sul piano `asse = q` estruso di `dist` nel verso dato."""
        sk = self.sk_cerchio(asse, q_expr, nome, cu, cv, d_expr)
        return self.estrudi(sk, asse, dist_expr, verso, op, nome)


def aggiungi_parametri(des, lista):
    """Aggiunge (o aggiorna) parametri utente: lista di (nome, espressione, unita', commento)."""
    up = des.userParameters
    fatti = []
    for nome, expr, unita, commento in lista:
        p = up.itemByName(nome)
        if p is None:
            up.add(nome, VI.createByString(expr), unita, commento)
            fatti.append(nome)
        elif p.expression.replace(' ', '') != expr.replace(' ', ''):      # Fusion riscrive gli spazi
            p.expression = expr
            p.comment = commento
            fatti.append(nome + '*')
    return fatti


def trova_occ(genitore, nome_comp):
    """Occorrenze figlie dirette di `genitore` il cui componente ha il nome dato."""
    return [o for o in genitore.occurrences if o.component.name == nome_comp]


def raggruppa(des, da, nome):
    """Raggruppa nella timeline le voci create a partire dall'indice `da`."""
    tl = des.timeline
    if tl.count - da < 2:
        return None
    g = tl.timelineGroups.add(da, tl.count - 1)
    g.name = nome
    return g
