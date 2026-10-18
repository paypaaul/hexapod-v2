"""Instradatore a griglia per le PCB del robot (algoritmo di Lee con A*, due strati, vie), in Python puro.

Serve a provare e a fare lo sbroglio da script senza un autorouter esterno (Freerouting sarebbe una dipendenza nuova,
piano-pcb.md 5.2). Lavora nella terna del robot, in mm. Il risultato e' un elenco di piste e vie che il generatore della
scheda (`<scheda>/genera_pcb.py`) aggiunge al PCB; il giudice resta il DRC di KiCad (`controlla.py`).

Ingresso: `piazzole` [(rif, numero, x, y, larghezza, altezza, forma 'c'|'r', strati 'F'|'B'|'FB', rete)], i vincoli
della scheda (`Vincoli`) e le reti da sbrogliare nell'ordine voluto. Ogni rete ha la sua larghezza; la distanza fra
due reti e' quella minima del produttore, salvo le coppie di `Vincoli.distanza`. Le celle sono libere per una rete se
la pista, centrata sulla cella, rispetta le distanze da tutto il rame delle altre reti e dai bordi.
"""

import heapq
import math

_CACHE = {}           # distanze dai bordi per strato, condivise fra le prove sullo stesso vincolo
PASSO = 0.1           # mm per cella
MARGINE = 0.05        # in piu' sulle distanze: le diagonali fra due centri di cella tagliano gli angoli
VIA_D, VIA_FORO = 0.6, 0.3
COSTO_VIA = 25        # in celle
COSTO_DIAG = math.sqrt(2)


def _d_rett(px, py, cx, cy, hx, hy):
    dx, dy = max(abs(px - cx) - hx, 0.0), max(abs(py - cy) - hy, 0.0)
    return math.hypot(dx, dy)


def _d_seg(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    l2 = vx * vx + vy * vy
    t = 0.0 if l2 == 0 else max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / l2))
    return math.hypot(px - ax - t * vx, py - ay - t * vy)


def _in_poligono(px, py, pts):
    dentro = False
    for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
        if (ay > py) != (by > py) and px < ax + (py - ay) * (bx - ax) / (by - ay):
            dentro = not dentro
    return dentro


def _distanza(tipo, g, px, py):
    """Distanza dal bordo del rame: piazzola ('p', rettangolo o cerchio), pista ('s'), via ('v')."""
    if tipo == 'p':
        x, y, hx, hy, forma = g
        return math.hypot(px - x, py - y) - hx if forma == 'c' else _d_rett(px, py, x, y, hx, hy)
    if tipo == 's':
        (ax, ay), (bx, by), w = g
        return _d_seg(px, py, ax, ay, bx, by) - w / 2
    x, y, rv = g
    return math.hypot(px - x, py - y) - rv


def _scatola(tipo, g, d):
    if tipo == 'p':
        x, y, hx, hy, _ = g
        e = max(hx, hy) + d
        return x - e, y - e, x + e, y + e
    if tipo == 's':
        (ax, ay), (bx, by), w = g
        e = w / 2 + d
        return min(ax, bx) - e, min(ay, by) - e, max(ax, bx) + e, max(ay, by) + e
    x, y, rv = g
    return x - rv - d, y - rv - d, x + rv + d, y + rv + d


class Vincoli:
    """Bordi e divieti della scheda. `contorno` e `aperture` sono poligoni; `vietati[strato]` sono poligoni o cerchi
    (x, y, r) dove le piste non entrano; `distanza(rete_a, rete_b, rif_b)` da' la distanza minima fra due reti."""

    def __init__(self, contorno, aperture=(), vietati=None, bordo=0.5, minimo=0.2, distanza=None):
        self.contorno, self.aperture = contorno, list(aperture)
        self.vietati = vietati or {'F': [], 'B': []}
        self.bordo, self.minimo = bordo, minimo
        self.distanza = distanza or (lambda a, b, rif: minimo)


class Instradatore:
    def __init__(self, piazzole, vincoli, larghezze, x0, y0, x1, y1, strati='FB'):
        """strati: lettere degli strati di rame, dall'alto ('FB', oppure 'F12B' con In1 e In2); le piazzole a foro
        ('FB') stanno su tutti."""
        self.v = vincoli
        self.strati = strati
        self.larghezze = larghezze
        self.x0, self.y0 = x0, y0
        self.nx, self.ny = int(round((x1 - x0) / PASSO)) + 1, int(round((y1 - y0) / PASSO)) + 1
        self.piazzole = piazzole
        # rame posato: [(strato, tipo, geometria, rete, rif)]; tipo 'p' piazzola (rett o cerchio), 's' pista, 'v' via
        self.rame = []
        for rif, num, x, y, w, h, forma, st_p, rete in piazzole:
            for st in (self.strati if st_p == 'FB' else st_p):
                self.rame.append((st, 'p', (x, y, w / 2, h / 2, forma), rete, rif))
        self.piste, self.vie = [], []
        self._fisso = _CACHE.setdefault((id(vincoli), x0, y0, x1, y1), {})

    # --- celle
    def xy(self, i, j):
        return self.x0 + i * PASSO, self.y0 + j * PASSO

    def ij(self, x, y):
        return int(round((x - self.x0) / PASSO)), int(round((y - self.y0) / PASSO))

    def _distanze(self, st):
        """Per ogni cella: distanza dal bordo della scheda (0 fuori) e dai divieti dello strato (0 dentro), calcolate
        una volta per strato; le mappe di ogni larghezza sono soglie su queste."""
        if st in self._fisso:
            return self._fisso[st]
        v = self.v
        lati = [(a, b) for poli in [v.contorno] + v.aperture for a, b in zip(poli, poli[1:] + poli[:1])]
        db, dz = [0.0] * (self.nx * self.ny), [1e9] * (self.nx * self.ny)
        for j in range(self.ny):
            for i in range(self.nx):
                x, y = self.xy(i, j)
                k = j * self.nx + i
                if _in_poligono(x, y, v.contorno) and not any(_in_poligono(x, y, a) for a in v.aperture):
                    db[k] = min(_d_seg(x, y, *a, *b) for a, b in lati)
                m = 1e9
                for z in v.vietati[st]:
                    if len(z) == 3:
                        m = min(m, max(math.hypot(x - z[0], y - z[1]) - z[2], 0.0))
                    elif _in_poligono(x, y, z):
                        m = 0.0
                    else:
                        m = min(m, min(_d_seg(x, y, *a, *b) for a, b in zip(z, z[1:] + z[:1])))
                    if m == 0.0:
                        break
                dz[k] = m
        self._fisso[st] = (db, dz)
        return db, dz

    def _bordi(self, st, h):
        """Celle vietate dai bordi e dai divieti della scheda per una pista di mezza larghezza h."""
        db, dz = self._distanze(st)
        lim = self.v.bordo + h + MARGINE
        lz = h + MARGINE
        return bytearray(1 if (a < lim or b < lz) else 0 for a, b in zip(db, dz))

    def _mappa(self, rete, st, h):
        """Celle vietate su uno strato per una pista della rete con mezza larghezza h."""
        no = bytearray(self._bordi(st, h))
        for s, tipo, g, r, rif in self.rame:
            if s != st or r == rete:
                continue
            d = self.v.distanza(rete, r, rif) + h + MARGINE
            box = _scatola(tipo, g, d)
            i0, j0 = self.ij(box[0], box[1])
            i1, j1 = self.ij(box[2], box[3])
            for j in range(max(j0, 0), min(j1, self.ny - 1) + 1):
                for i in range(max(i0, 0), min(i1, self.nx - 1) + 1):
                    if not no[j * self.nx + i]:
                        px, py = self.xy(i, j)
                        if _distanza(tipo, g, px, py) < d:
                            no[j * self.nx + i] = 1
        return no

    # --- ricerca
    def posate(self, piste, vie):
        """Rame gia' posato come ostacolo: piste [rete, strato 'F.Cu'|'In1.Cu'|..., larghezza, (x, y), (x, y)] e vie
        [rete, x, y, diametro, foro] (passano tutti gli strati)."""
        lettera = {'F.Cu': 'F', 'B.Cu': 'B', 'In1.Cu': '1', 'In2.Cu': '2'}
        for rete, st, w, a, b in piste:
            self.rame.append((lettera[st], 's', (tuple(a), tuple(b), w), rete, None))
        for rete, x, y, d, _ in vie:
            self.rame += [(st, 'v', (x, y, d / 2), rete, None) for st in self.strati]

    def instrada(self, rete, strati=None, vie=True, costi=None):
        strati = strati or self.strati
        """Collega tutte le piazzole della rete; restituisce le connessioni non riuscite."""
        w = self.larghezze.get(rete, 0.25)
        h = w / 2
        pz = [p for p in self.piazzole if p[8] == rete]
        if len(pz) < 2:
            return []
        mappe = {st: self._mappa(rete, st, h) for st in strati}
        mappe_via = None
        if vie:
            hv = VIA_D / 2
            mv = [self._mappa(rete, st, hv) for st in self.strati]
            mappe_via = bytearray(max(c) for c in zip(*mv))
        costi = dict(costi or {})
        zone = costi.pop('zone', [])
        if zone:
            # zone da evitare: [(x0, y0, x1, y1, fattore)]; il costo di un passo dentro la zona si moltiplica
            pes = bytearray(self.nx * self.ny)
            fattori = {}
            for k, (x0, y0, x1, y1, fat) in enumerate(zone, 1):
                fattori[k] = fat
                i0, j0 = self.ij(x0, y0)
                i1, j1 = self.ij(x1, y1)
                for j in range(max(j0, 0), min(j1, self.ny - 1) + 1):
                    for i in range(max(i0, 0), min(i1, self.nx - 1) + 1):
                        pes[j * self.nx + i] = k
            costi['_zone'] = (pes, fattori)

        def celle(p):
            # centro della piazzola e celle dentro la piazzola (si entra da qualunque punto del rame)
            x, y, w2, h2 = p[2], p[3], p[4] / 2, p[5] / 2
            out = []
            i0, j0 = self.ij(x - w2 + 0.05, y - h2 + 0.05)
            i1, j1 = self.ij(x + w2 - 0.05, y + h2 - 0.05)
            for j in range(j0, j1 + 1):
                for i in range(i0, i1 + 1):
                    cx, cy = self.xy(i, j)
                    if p[6] == 'c' and math.hypot(cx - x, cy - y) > w2 - 0.1:
                        continue        # piazzola tonda: solo le celle dentro il cerchio
                    for st in (self.strati if p[7] == 'FB' else p[7]):
                        if st in strati:
                            out.append((st, i, j))
            return out

        albero = set(celle(pz[0]))
        fatti, mancati = [pz[0]], []
        resto = pz[1:]
        while resto:
            # la piazzola piu' vicina all'albero
            resto.sort(key=lambda p: min(math.hypot(p[2] - q[2], p[3] - q[3]) for q in fatti))
            p = resto.pop(0)
            arrivi = set(celle(p))
            cammino = self._a_stella(albero, arrivi, mappe, mappe_via, strati, (p[2], p[3]), costi)
            if cammino is None:
                mancati.append('%s %s.%s' % (rete, p[0], p[1]))
                continue
            self._posa(rete, w, cammino, mappe)
            albero |= set(cammino) | arrivi
            fatti.append(p)
        return mancati

    def _a_stella(self, partenze, arrivi, mappe, mappe_via, strati, meta, costi):
        nx = self.nx
        mx, my = self.ij(*meta)
        aperti, dist, prima = [], {}, {}
        for n in partenze:
            dist[n] = 0.0
            heapq.heappush(aperti, (math.hypot(n[1] - mx, n[2] - my), 0.0, n))
        passi = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
                 (1, 1, COSTO_DIAG), (1, -1, COSTO_DIAG), (-1, 1, COSTO_DIAG), (-1, -1, COSTO_DIAG)]
        while aperti:
            _, g, n = heapq.heappop(aperti)
            if g > dist.get(n, 1e18):
                continue
            if n in arrivi:
                cam = [n]
                while cam[-1] in prima:
                    cam.append(prima[cam[-1]])
                return cam[::-1]
            st, i, j = n
            vicini = []
            for di, dj, c in passi:
                a, b = i + di, j + dj
                if 0 <= a < nx and 0 <= b < self.ny:
                    m = (st, a, b)
                    if not mappe[st][b * nx + a] or m in arrivi:
                        f = costi.get(st, 1.0)
                        if '_zone' in costi:
                            k = costi['_zone'][0][b * nx + a]
                            if k:
                                f *= costi['_zone'][1][k]
                        vicini.append((m, c * f))
            if mappe_via is not None and not mappe_via[j * nx + i]:
                for altro in strati:
                    if altro != st:
                        vicini.append(((altro, i, j), COSTO_VIA))
            for m, c in vicini:
                ng = g + c
                if ng < dist.get(m, 1e18):
                    dist[m] = ng
                    prima[m] = n
                    heapq.heappush(aperti, (ng + math.hypot(m[1] - mx, m[2] - my), ng, m))
        return None

    def _vista(self, mappa, a, b):
        """Il segmento fra i centri delle celle a e b passa solo su celle libere (campionato ogni mezza cella)."""
        n = int(max(abs(b[1] - a[1]), abs(b[2] - a[2])) * 2) + 1
        for k in range(n + 1):
            i = int(round(a[1] + (b[1] - a[1]) * k / n))
            j = int(round(a[2] + (b[2] - a[2]) * k / n))
            if mappa[j * self.nx + i]:
                return False
        return True

    @staticmethod
    def _a45(a, b):
        """Tratti a 0, 45 o 90 gradi: Freerouting e i controlli di KiCad li trattano senza ritocchi."""
        di, dj = abs(b[1] - a[1]), abs(b[2] - a[2])
        return di == 0 or dj == 0 or di == dj

    def _liscia(self, mappa, t):
        """Accorcia una scala di celle sullo stesso strato con tratti dritti dove la vista e' libera."""
        out, k = [t[0]], 0
        while k < len(t) - 1:
            m = len(t) - 1
            while m > k + 1 and not (self._a45(t[k], t[m]) and self._vista(mappa, t[k], t[m])):
                m -= 1
            out.append(t[m])
            k = m
        return out

    def _posa(self, rete, w, cammino, mappe=None):
        """Celle del cammino -> segmenti dritti per strato e vie dove cambia strato."""
        tratti, corrente = [], [cammino[0]]
        for n in cammino[1:]:
            if n[0] != corrente[-1][0]:
                tratti.append(corrente)
                x, y = self.xy(n[1], n[2])
                self.vie.append((rete, round(x, 3), round(y, 3)))
                self.rame += [(st, 'v', (x, y, VIA_D / 2), rete, None) for st in self.strati]
                corrente = [n]
            else:
                corrente.append(n)
        tratti.append(corrente)
        for t in tratti:
            if len(t) < 2:
                continue
            st = t[0][0]
            if mappe is not None:
                punti = self._liscia(mappe[st], t)
            else:
                # un vertice dove cambia la direzione del passo: i tratti dritti restano interi
                punti = [t[0]]
                for k in range(1, len(t) - 1):
                    d0 = (t[k][1] - t[k - 1][1], t[k][2] - t[k - 1][2])
                    d1 = (t[k + 1][1] - t[k][1], t[k + 1][2] - t[k][2])
                    if d0 != d1:
                        punti.append(t[k])
                punti.append(t[-1])
            xy = [tuple(round(v, 3) for v in self.xy(i, j)) for _, i, j in punti]
            self.piste.append((rete, st, w, xy))
            for p, q in zip(xy, xy[1:]):
                self.rame.append((st, 's', (p, q, w), rete, None))


def sbroglia(piazzole, vincoli, larghezze, finestra, ordine, fisse=(), giri=12, registro=print, costi=None):
    """Instrada le reti nell'ordine dato; quelle che non riescono passano in testa (dopo le `fisse`, che restano prime)
    e si ricomincia, fino a `giri` volte. Restituisce l'instradatore dell'ultimo giro e le reti non riuscite."""
    ordine = list(ordine)
    for g in range(giri):
        R = Instradatore(piazzole, vincoli, larghezze, *finestra)
        mancate = [r for r in ordine if R.instrada(r, costi=(costi or {}).get(r))]
        registro('giro %d: %d reti non riuscite %s' % (g + 1, len(mancate), mancate))
        if not mancate:
            return R, []
        resto = [r for r in ordine if r not in mancate and r not in fisse]
        ordine = [r for r in fisse] + [r for r in mancate if r not in fisse] + resto
    return R, mancate
