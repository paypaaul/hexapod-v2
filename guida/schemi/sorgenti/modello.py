"""Modello della basetta e della scheda del carapace (F3b, seconda versione dopo la verifica elettrica).
Griglia, componenti, reti, collegamenti, zone vietate, router dei fili sul lato saldature e controlli.
Non fa parte della repo: genera guida/schemi/*.svg e le tabelle di schemi.md."""
import math, heapq

P = 2.54
LET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def h(f):
    return '%s-%s' % (f[0], f[1:])


class Griglia:
    def __init__(s, x0, y0, ncol, nrig):
        s.x0, s.y0, s.ncol, s.nrig = x0, y0, ncol, nrig

    def cr(s, f):
        return LET.index(f[0]), int(f[1:])

    def xy(s, f):
        c, r = s.cr(f)
        return s.x0 + c * P, s.y0 - (r - 1) * P

    def nome(s, c, r):
        return LET[c] + str(r)

    def fori(s):
        return [s.nome(c, r) for r in range(1, s.nrig + 1) for c in range(s.ncol)]

    def dentro(s, c, r):
        return 0 <= c < s.ncol and 1 <= r <= s.nrig

    def vicini(s, f):
        c, r = s.cr(f)
        return [s.nome(c + dc, r + dr) for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)) if s.dentro(c + dc, r + dr)]

    # angoli fra quattro fori: (i, k) con x = x0 + (i + 0,5) P, y = riga k - 1,27 (k = 0 sopra la riga 1)
    def cxy(s, i, k):
        return s.x0 + (i + 0.5) * P, s.y0 - (k - 0.5) * P

    def angoli(s, f):
        c, r = s.cr(f)
        return [(c - 1, r - 1), (c, r - 1), (c - 1, r), (c, r)]


def adiacenti(g, a, b):
    return b in g.vicini(a)


# ------------------------------------------------------------------ livelli delle reti (per i controlli)
def livello(rete):
    if rete is None:
        return None
    if rete == 'VBAT':
        return 'vbat'
    if rete.startswith('5V'):
        return '5v'
    if rete in ('DATA', 'DATA2', 'Y1', 'TX5', 'RX5', 'H_NC'):
        return 's5'
    if rete.startswith('3V3'):
        return '3v3'
    if rete == 'GND' or rete == 'LO':
        return 'gnd'
    if rete in ('EN', 'GPIO42'):
        return 'en'
    return 's3'


ALTI_A_RIPOSO = {'TX3', 'RX3', 'SDA', 'SCL', 'L_NC', 'SENSE', 'ESP'}


class Scheda:
    """Una millefori: fori, pin, ponticelli, fili e zone."""

    def __init__(s, g, nome):
        s.g, s.nome = g, nome
        s.pin = {}          # foro -> (componente, nome del pin, rete)
        s.ponti = []        # (a, b, rete)
        s.fili = []         # dict: a, b, rete, awg, nota, fisso (percorso fissato)
        s.vietati = {}      # foro -> motivo
        s.nosald = set()    # pin degli strip non saldati (tagliati a filo)
        s.zone = []         # (x, y, r_corpo, r_foro, r_filo, testo)
        s.capi_ammessi = set()  # (foro, nodo): capo di filo ammesso dentro una zona

    def metti(s, f, comp, nome, rete):
        assert f not in s.pin, ('foro doppio', f, s.pin.get(f), comp)
        assert f not in s.vietati or comp == 'U1', ('foro vietato', f, comp, s.vietati.get(f))
        s.pin[f] = (comp, nome, rete)

    def rete(s, f):
        return s.pin[f][2] if f in s.pin else None

    def reti(s):
        out = {}
        for f, (c, n, r) in s.pin.items():
            if r and f not in s.nosald:
                out.setdefault(r, []).append(f)
        return out

    def ponte(s, *fori, rete=None):
        rr = set(s.rete(f) for f in fori) - {None}
        if rete: rr.add(rete)
        if not rr:
            # catena di fori vuoti: la rete viene dal ponticello che la tocca dopo
            rr = {None}
        assert len(rr) == 1, ('ponte fra reti', fori, rr)
        r = rr.pop()
        for a, b in zip(fori, fori[1:]):
            assert adiacenti(s.g, a, b), (a, b)
            ra, rb = s.rete(a), s.rete(b)
            assert (ra is None or ra == r) and (rb is None or rb == r), ('ponte fra reti', a, b, ra, rb)
            for f in (a, b):
                if f not in s.pin:
                    s.metti(f, 'ponte', '', r)
            s.ponti.append((a, b, r))

    def filo(s, a, b, awg=30, nota='', fisso=None):
        ra, rb = s.rete(a), s.rete(b)
        assert ra == rb, ('filo fra reti', a, b, ra, rb)
        s.fili.append(dict(a=a, b=b, rete=ra, awg=awg, nota=nota, fisso=fisso))


# ------------------------------------------------------------------ router sul lato saldature
class Router:
    def __init__(s, sch, imin=-1, imax=None, kmin=0, kmax=None, riservati=None):
        s.s, g = sch, sch.g
        s.imin, s.imax = imin, (g.ncol - 1 if imax is None else imax)
        s.kmin, s.kmax = kmin, (g.nrig if kmax is None else kmax)
        s.uso_nodo = {}      # nodo -> lista di (filo, verso) verso in h, v, svolta, capo
        s.uso_arco = {}
        s.riservati = riservati or {}   # nodo -> rete che lo puo' usare
        s.bloccati_archi = set()
        for a, b, r in sch.ponti:
            s.bloccati_archi.add(s.arco_del_ponte(a, b))
        s.smd = []
        s.costo_incrocio = 3.0
        s.costo_parallelo = 2.5
        s.storia = {}
        s.cap_arco = 3
        s.costo_angolo = 2.0
        s.capi_assegnati = set()
        s.domanda = {}
        s.angoli_capo = set()
        for f in sch.fili:
            for p in (f['a'], f['b']):
                if p:
                    s.angoli_capo |= set(sch.g.angoli(p))
        s.cap_nodo = 3

    def arco_del_ponte(s, a, b):
        g = s.s.g
        (ca, ra), (cb, rb) = g.cr(a), g.cr(b)
        if ra == rb:      # ponte orizzontale: blocca l'arco verticale fra (min c, r-1) e (min c, r)
            c = min(ca, cb)
            return frozenset({(c, ra - 1), (c, ra)})
        r = min(ra, rb)
        return frozenset({(ca - 1, r), (ca, r)})

    def nodo_ok(s, n, rete):
        i, k = n
        if not (s.imin <= i <= s.imax and s.kmin <= k <= s.kmax):
            return False
        x, y = s.s.g.cxy(i, k)
        for zx, zy, rc, rf, rw, t in s.s.zone:
            if math.hypot(x - zx, y - zy) < rw:
                return False
        if n in s.riservati and s.riservati[n] != rete:
            return False
        return True

    def nodo_ok_capo(s, n, rete, foro):
        if (foro, n) in s.s.capi_ammessi:
            return True
        return s.nodo_ok(n, rete)

    def arco_ok(s, a, b, rete):
        (xa, ya), (xb, yb) = s.s.g.cxy(*a), s.s.g.cxy(*b)
        xm, ym = (xa + xb) / 2, (ya + yb) / 2
        for zx, zy, rc, rf, rw, t in s.s.zone:
            if math.hypot(xm - zx, ym - zy) < rw:
                return False
        return len(s.uso_arco.get(frozenset({a, b}), [])) < 2

    def costo_arco(s, a, b, rete):
        # fori ai due lati dell'arco: un giunto di un'altra rete accanto costa un poco (il filo isolato ci passa sopra)
        g = s.s.g
        (ia, ka), (ib, kb) = a, b
        if ka == kb:
            c = max(ia, ib); lati = [(c, ka), (c, ka + 1)]
        else:
            r = max(ka, kb); lati = [(ia, r), (ia + 1, r)]
        cst = 1.0
        for c, r in lati:
            if g.dentro(c, r):
                f = g.nome(c, r)
                rr = s.s.rete(f)
                if f in s.s.pin and rr != rete:
                    cst += 0.35
                    if rr == 'VBAT':
                        cst += 50
        return cst

    def instrada(s, filo, idx, forza=False):
        """Percorso piu' corto. Con forza=True passa anche sulle risorse occupate (costo alto) e
        restituisce (percorso, fili in conflitto) senza registrarlo."""
        g = s.s.g
        rete = filo['rete']
        PEN = 25.0
        def capo_ok(n, foro):
            return s.nodo_ok_capo(n, rete, foro)
        if filo.get('dest_nodi'):
            sorg = [n for n in g.angoli(filo['a']) if capo_ok(n, filo['a']) and (forza or s.capo_libero(n))]
            dest = set(n for n in filo['dest_nodi'] if s.nodo_ok(n, rete) and (forza or s.capo_libero(n)))
        elif 'capi' in filo:
            sorg = [filo['capi'][0]]
            dest = {filo['capi'][1]}
        else:
            sorg = [n for n in g.angoli(filo['a']) if capo_ok(n, filo['a']) and (forza or s.capo_libero(n))]
            dest = set(n for n in g.angoli(filo['b']) if capo_ok(n, filo['b']) and (forza or s.capo_libero(n)))
        if not sorg or not dest:
            return (None, set()) if forza else None
        def chi(n):
            return set(u[0] for u in s.uso_nodo.get(n, []))
        pq, best = [], {}
        import itertools
        cnt = itertools.count()
        for n in sorg:
            c0 = 0.6 + s.storia.get(n, 0) + 4.0 * len(s.uso_nodo.get(n, []))
            con = frozenset(chi(n)) if forza else frozenset()
            if con: c0 += PEN
            best[(n, None)] = c0
            heapq.heappush(pq, (c0, next(cnt), n, None, (n,), con))
        perc = None
        while pq:
            c, _, n, d, path, con = heapq.heappop(pq)
            if best.get((n, d), 1e9) < c - 1e-9:
                continue
            if n in dest and len(path) >= 1:
                perc = path
                break
            i, k = n
            occ_n = bool(s.uso_nodo.get(n)) and not (forza and set(chi(n)) <= con)
            for di, dk, dv in ((1, 0, 'h'), (-1, 0, 'h'), (0, 1, 'v'), (0, -1, 'v')):
                m = (i + di, k + dk)
                if m in path or not (s.nodo_ok(m, rete) or m in dest):
                    continue
                if not (s.imin <= m[0] <= s.imax and s.kmin <= m[1] <= s.kmax):
                    continue
                arco = frozenset({n, m})
                if not s.arco_geom_ok(n, m):
                    continue
                cc = c + s.costo_arco(n, m, rete) + s.storia.get(m, 0)
                if m not in dest and m in s.capi_assegnati:
                    cc += 12.0
                if m not in dest:
                    cc += s.domanda.get(m, 0)
                nuovi = set()
                ua = s.uso_arco.get(arco, [])
                if len(ua) >= s.cap_arco:
                    if not forza or 'VBAT' in ua:
                        continue
                    nuovi |= set(ua)
                elif ua:
                    cc += s.costo_parallelo * len(ua)
                if arco in s.bloccati_archi:
                    cc += 1.5
                if d is not None and d != dv:
                    cc += 0.25
                usi = s.uso_nodo.get(m, [])
                if usi:
                    ok = len(usi) < s.cap_nodo
                    if ok:
                        cc += s.costo_incrocio * len(usi)
                    else:
                        if not forza or any(u[0] == 'VBAT' for u in usi):
                            continue
                        nuovi |= set(u[0] for u in usi)
                nuovi -= con
                if nuovi:
                    cc += PEN * len(nuovi)
                if m in dest:
                    cc += 0.6 + 4.0 * len(usi)
                st = (m, dv)
                if cc < best.get(st, 1e9):
                    best[st] = cc
                    heapq.heappush(pq, (cc, next(cnt), m, dv, path + (m,), con | frozenset(nuovi)))
        if perc is None:
            return (None, set()) if forza else None
        if forza:
            return list(perc), set(con) - {idx}
        s.registra(perc, idx)
        return list(perc)

    def arco_geom_ok(s, a, b):
        (xa, ya), (xb, yb) = s.s.g.cxy(*a), s.s.g.cxy(*b)
        xm, ym = (xa + xb) / 2, (ya + yb) / 2
        for zx, zy, rc, rf, rw, t in s.s.zone:
            if math.hypot(xm - zx, ym - zy) < rw:
                return False
        return True

    def registra(s, perc, idx):
        for j, n in enumerate(perc):
            if j == 0 or j == len(perc) - 1:
                v = 'capo'
            else:
                a, b = perc[j - 1], perc[j + 1]
                if a[1] == n[1] == b[1]:
                    v = 'h'
                elif a[0] == n[0] == b[0]:
                    v = 'v'
                else:
                    v = 'svolta'
            s.uso_nodo.setdefault(n, []).append((idx, v))
        for a, b in zip(perc, perc[1:]):
            s.uso_arco.setdefault(frozenset({a, b}), []).append(idx)

    def togli(s, idx):
        for n in list(s.uso_nodo):
            s.uso_nodo[n] = [u for u in s.uso_nodo[n] if u[0] != idx]
            if not s.uso_nodo[n]:
                del s.uso_nodo[n]
        for a in list(s.uso_arco):
            s.uso_arco[a] = [u for u in s.uso_arco[a] if u != idx]
            if not s.uso_arco[a]:
                del s.uso_arco[a]

    def capo_libero(s, n):
        u = s.uso_nodo.get(n, [])
        return len(u) < s.cap_nodo and not any(x[0] == 'VBAT' for x in u)

    def libero_capo(s, n):
        return not s.uso_nodo.get(n)

    def incroci(s):
        return [(n, u) for n, u in s.uso_nodo.items() if len(set(x[1] for x in u)) > 1 or (len(u) > 1 and 'svolta' in [x[1] for x in u])]

    def paralleli(s):
        return [(a, u) for a, u in s.uso_arco.items() if len(u) > 1]


def controlli_vicinanze(sch, eccezioni=()):
    """Coppie di fori vicini, con giunto, di reti diverse. Restituisce (errori, avvisi, tutte)."""
    g = sch.g
    err, avv, tutte = [], [], []
    for f in g.fori():
        if f not in sch.pin:
            continue
        for v in g.vicini(f):
            if v not in sch.pin or v <= f:
                continue
            a, b = sch.pin[f], sch.pin[v]
            ra, rb = a[2], b[2]
            if ra == rb and ra is not None:
                continue
            na = f in sch.nosald
            nb = v in sch.nosald
            la, lb = livello(ra), livello(rb)
            if na: la = 'esp_ns'
            if nb: lb = 'esp_ns'
            if a[0] == 'U1' and ra is None and not na: la = 's3'
            if b[0] == 'U1' and rb is None and not nb: lb = 's3'
            coppia = (f, ra or ('libero' if na else a[1]), v, rb or ('libero' if nb else b[1]))
            tutte.append(coppia)
            if (f, v) in eccezioni or (v, f) in eccezioni:
                continue
            ls = {la, lb}
            if 'vbat' in ls and not (a[0] == 'U2' and b[0] == 'U2'):
                err.append(('VBAT', coppia))
            if ls & {'5v', 's5'} and ls & {'3v3', 's3'}:
                err.append(('5 V accanto a 3,3 V o GPIO', coppia))
            elif ls & {'5v', 's5'} and 'esp_ns' in ls:
                avv.append(('5 V accanto a un pin non saldato', coppia))
            if 'en' in ls:
                altra = lb if la == 'en' else la
                rete_altra = rb if la == 'en' else ra
                if altra in ('5v', 's5', '3v3', 'vbat') or rete_altra in ALTI_A_RIPOSO or altra == 's3':
                    if {ra, rb} != {'EN', 'GPIO42'}:
                        err.append(('EN o GPIO42 accanto a una rete alta', coppia))
    return err, avv, tutte


def assegna_capi(R, fili, riservati=()):
    """Sceglie per ogni capo di filo un angolo del suo foro, verso l'altro capo, senza ripetizioni."""
    g = R.s.g
    presi = set(riservati)
    # prima i fori con piu' fili
    from collections import Counter
    cnt = Counter()
    for f in fili:
        cnt[f['a']] += 1; cnt[f['b']] += 1
    capi = []
    for i, f in enumerate(fili):
        for lato in (0, 1):
            capi.append((-cnt[f['a'] if lato == 0 else f['b']], i, lato))
    capi.sort()
    scelta = {}
    for _, i, lato in capi:
        f = fili[i]
        foro, altro = (f['a'], f['b']) if lato == 0 else (f['b'], f['a'])
        xo, yo = g.xy(altro)
        cand = [n for n in g.angoli(foro) if R.nodo_ok_capo(n, f['rete'], foro) and n not in presi]
        cand.sort(key=lambda n: math.hypot(g.cxy(*n)[0] - xo, g.cxy(*n)[1] - yo))
        if not cand:
            raise RuntimeError('nessun angolo libero per %s (%s-%s)' % (foro, f['a'], f['b']))
        scelta[(i, lato)] = cand[0]
        presi.add(cand[0])
    for i, f in enumerate(fili):
        f['capi'] = (scelta[(i, 0)], scelta[(i, 1)])
    R.capi_assegnati = set(scelta.values())


def aggiorna_domanda(R, fili, in_attesa, peso=8.0):
    """Costo di passaggio sugli angoli dei fori che aspettano ancora un capo di filo."""
    g = R.s.g
    from collections import Counter
    att = Counter()
    for i in in_attesa:
        att[fili[i]['a']] += 1
        if fili[i]['b']:
            att[fili[i]['b']] += 1
    R.domanda = {}
    for foro, n in att.items():
        liberi = [c for c in g.angoli(foro) if not R.uso_nodo.get(c) and R.nodo_ok_capo(c, fili[0]['rete'], foro)]
        if not liberi:
            continue
        q = peso * n / len(liberi)
        for c in liberi:
            R.domanda[c] = R.domanda.get(c, 0) + q


def punti_con_corsie(R, idx, perc, cxy, passo=0.85):
    """Punti della polilinea di un filo, spostati nella sua corsia dove l'arco e' condiviso."""
    def off(a, b):
        u = R.uso_arco.get(frozenset({a, b}), [idx])
        u = [x for x in u if x != 'VBAT'] or [idx]
        n = len(u)
        j = u.index(idx) if idx in u else 0
        o = (j - (n - 1) / 2) * passo
        if a[1] == b[1]:
            return (0.0, o)
        return (o, 0.0)
    pts = []
    for j, nd in enumerate(perc):
        x, y = cxy(nd)
        ins = off(perc[j - 1], nd) if j > 0 else None
        outs = off(nd, perc[j + 1]) if j < len(perc) - 1 else None
        if ins and outs:
            if (ins[0] == 0) == (outs[0] == 0):
                dx, dy = (ins[0] + outs[0]) / 2, (ins[1] + outs[1]) / 2
            else:
                dx, dy = ins[0] + outs[0], ins[1] + outs[1]
        else:
            dx, dy = ins or outs or (0, 0)
        pts.append((x + dx, y + dy))
    return pts
