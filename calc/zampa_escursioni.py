#!/usr/bin/env python3
"""Verifica geometrica delle escursioni della zampa MG996R (modello 2D a strati).

Nasce dallo script della proposta "scalata" (docs/ricerca/zampa-architetture.json), reso parametrico
per provare le varianti prima di modellarle in Fusion. Il CAD resta la verifica finale: questo
modello non ha raccordi, teste delle viti reali, cavi.

Terna della zampa: origine sull'asse del femore nel piano medio (a meta' tra le facce esterne delle
due piastre del femore), X orizzontale verso l'esterno, Y lungo l'asse del femore (verso la piastra
delle squadrette), Z in alto. Posa di riferimento alpha = 0 (femore orizzontale), gamma = 90.
Ogni parte e' un insieme di poligoni convessi nel piano XZ della propria terna, ciascuno con il suo
intervallo lungo Y: due poligoni possono toccarsi solo se gli intervalli Y si sovrappongono.
Servo nella terna di progetto (parametri srv_): origine sull'asse dell'albero al lato inferiore delle
alette, x_s verso la coda, z_s verso la cima dell'albero (qui z_s = +Y per femore e ginocchio).
Il corpo e' rappresentato dalla gondola del servo di coxa (raggio massimo dall'asse, quindi vale per
qualunque angolo di coxa) e da un fianco 15 mm dietro l'asse.

Uso (dalla radice della repo):
    python3 calc/zampa_escursioni.py                      # configurazione di progetto (CONFIG)
    python3 calc/zampa_escursioni.py Lf=65 Lt=110         # variante: qualunque chiave di CONFIG
"""
import math
import os
import sys

CONFIG = {
    'gioco': 1.0,          # gioco minimo richiesto tra parti in moto relativo (mm)
    'Lf': 70.0, 'Lt': 115.0,
    # servo MG996R (docs/dimensioni-componenti.md): cassa 41,0 x 20,5, sotto le alette 28,8 (caso peggiore)
    'cassa_x0': -10.25, 'cassa_x1': 30.75, 'cassa_semi': 10.25, 'sotto': 28.8, 'sopra': 10.2,
    'alette_x0': -17.05, 'alette_x1': 37.55, 'alette_semi': 9.25, 'alette_sp': 2.4,
    'fori_x': (-13.75, 34.25), 'fori_y': 5.0, 'torre_r': 10.25, 'torre_h': 10.5,
    'sq_disco_basso': 15.4, 'sq_disco_alto': 17.9,     # squadretta a disco (C): mozzo 12,4..15,4, disco 2,5
    # culla e giunto
    'gio': 0.2, 'parete': 2.0, 'gio_fondo': 0.4, 'fondo': 4.4,
    'ins_r': 2.1, 'ins_par': 1.6, 'ins_sposta': 0.4, 'bugna_h': 8.0,
    'cus_fl': 0.8, 'rialzo': 0.4,
    'pB': 5.2,             # piastra dei perni: spessore al mozzo
    'pA_sopra': 3.2,       # piastra delle squadrette: plastica dietro il disco
    # coxa
    'sp_anima': 4.0, 'sp_ponte_extra': 0.0,
    # femore: blocco cavo tra le piastre; x0 e la distanza dal ginocchio fissano la zona libera
    'blocco_x0': 21.5, 'blocco_dk': 21.0, 'blocco_z0': -2.0, 'blocco_z1': 20.0,
    'smusso_blocco_basso': (9.5, 5.5),   # smusso dello spigolo basso verso il ginocchio (dx, dz)
    'smusso_blocco_alto': 0.0,           # smusso dello spigolo alto verso l'anca (lato del triangolo)
    'smusso_ponte': 0.0,                 # smusso dello spigolo esterno alto del ponte
    'r_testa': 13.0,
    'stinco_semi': 9.0, 'stinco_y': 9.45, 'piede_r': 6.0,
}


def rett(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def cerchio(cx, cz, r, n=24):
    return [(cx + r * math.cos(2 * math.pi * k / n), cz + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def inviluppo(pts):
    pts = sorted(set(pts))

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


class Zampa:
    """Geometria derivata da una configurazione."""

    def __init__(self, **kw):
        c = dict(CONFIG, **kw)
        self.c = c
        self.LF, self.LT, self.GIOCO = c['Lf'], c['Lt'], c['gioco']
        self.zs_fondo_int = -(c['sotto'] + c['gio_fondo'])
        self.zs_fondo_est = self.zs_fondo_int - c['fondo']
        self.zs_pB_int = self.zs_fondo_est - c['cus_fl'] - c['rialzo']
        self.zs_pB_est = self.zs_pB_int - c['pB']
        self.zs_pA_int, self.zs_pA_est = c['sq_disco_basso'], c['sq_disco_alto'] + c['pA_sopra']
        self.Y0 = -(self.zs_pA_est + self.zs_pB_est) / 2
        self.larghezza = self.zs_pA_est - self.zs_pB_est
        self.cul_x0, self.cul_x1 = c['cassa_x0'] - c['gio'] - c['parete'], c['cassa_x1'] + c['gio'] + c['parete']
        self.cul_semi = c['cassa_semi'] + c['gio'] + c['parete']
        self.ins_x = (c['fori_x'][0] - c['ins_sposta'], c['fori_x'][1] + c['ins_sposta'])
        self.bug_x0 = self.ins_x[0] - c['ins_r'] - c['ins_par']
        self.bug_x1 = self.ins_x[1] + c['ins_r'] + c['ins_par']
        self.bug_semi = c['fori_y'] + c['ins_r'] + c['ins_par']
        # coxa: servo di coxa nel corpo, albero in alto, coda verso l'esterno; anima oltre la gondola
        self.r_gondola = max(math.hypot(self.bug_x1, self.bug_semi), math.hypot(c['alette_x1'], c['alette_semi']))
        self.r_anima = self.r_gondola + self.GIOCO
        self.LC = math.ceil(self.r_anima + c['sp_anima'] + c['cassa_semi'] + c['gio'])
        self.x_anima_int = -self.LC + self.r_anima
        self.x_sede = -(c['cassa_semi'] + c['gio'])
        self.pila_sotto = c['sotto'] + c['gio_fondo'] + c['fondo'] + c['cus_fl'] + c['rialzo']
        self.H = -self.bug_x1 + self.pila_sotto + c['pB']
        self.z_braccio = (self.H - self.pila_sotto - c['pB'], self.H - self.pila_sotto)
        self.z_ponte = (self.H + c['sq_disco_basso'], self.H + c['sq_disco_alto'] + c['pA_sopra'] + c['sp_ponte_extra'])
        self.z_gondola = (self.H - c['sotto'] - c['gio_fondo'] - c['fondo'], self.H + c['sopra'])
        self._parti()

    def Y(self, zs):
        return zs + self.Y0

    def servo_e_culla(self, nome, ang):
        c = self.c
        co, si = math.cos(math.radians(ang)), math.sin(math.radians(ang))

        def m(poly):
            return [(co * x - si * y, si * x + co * y) for x, y in poly]
        Y = self.Y
        out = [(nome + ' culla', m(rett(self.cul_x0, self.cul_x1, -self.cul_semi, self.cul_semi)), (Y(self.zs_fondo_est), Y(0.0)))]
        out += [(nome + ' bugna', m(rett(self.bug_x0, self.cul_x0, -self.bug_semi, self.bug_semi)), (Y(-c['bugna_h']), Y(0.0))),
                (nome + ' bugna', m(rett(self.cul_x1, self.bug_x1, -self.bug_semi, self.bug_semi)), (Y(-c['bugna_h']), Y(0.0)))]
        out += [(nome + ' cassa', m(rett(c['cassa_x0'], c['cassa_x1'], -c['cassa_semi'], c['cassa_semi'])),
                 (Y(self.zs_fondo_int + 0.4), Y(c['sopra'])))]
        out += [(nome + ' alette', m(rett(c['alette_x0'], c['alette_x1'], -c['alette_semi'], c['alette_semi'])), (Y(0.0), Y(c['alette_sp'])))]
        out += [(nome + ' teste viti', m(rett(self.ins_x[0] - 2.75, self.ins_x[1] + 2.75, -(c['fori_y'] + 2.75), c['fori_y'] + 2.75)),
                 (Y(c['alette_sp']), Y(c['alette_sp'] + 3.0)))]
        out += [(nome + ' torretta', cerchio(0, 0, c['torre_r']), (Y(c['sopra']), Y(c['torre_h'] + 1.9)))]
        return out

    def _parti(self):
        c, Y = self.c, self.Y
        tutto_y = (-1e3, 1e3)
        yc = (Y(self.zs_fondo_est), Y(0.0))
        sp = c['smusso_ponte']
        x0p, x1p, z0p, z1p = -self.LC - 12.0, self.x_sede, self.z_ponte[0], self.z_ponte[1]
        ponte = [(x0p, z0p), (x1p, z0p), (x1p, z1p - sp), (x1p - sp, z1p), (x0p, z1p)] if sp > 0 else rett(x0p, x1p, z0p, z1p)
        self.COXA = self.servo_e_culla('coxa: culla femore', -90.0) + [
            ('coxa: anima', rett(self.x_anima_int, self.x_sede, self.z_braccio[0], self.z_ponte[0]), yc),
            ('coxa: bugna inserti anima', rett(self.x_anima_int, self.x_sede + 3.2, self.cul_semi, self.z_ponte[0]), (yc[0], Y(-c['bugna_h']))),
            ('coxa: braccio inferiore', rett(-self.LC - 10.0, self.x_sede, self.z_braccio[0], self.z_braccio[1]), yc),
            ('coxa_ponte', ponte, (-12.0, 12.0)),
            ('corpo: gondola e servo coxa', rett(-self.LC - 25.0, -self.LC + self.r_gondola, self.z_gondola[0], self.z_gondola[1]), tutto_y),
            ('corpo: fondo e fianco', rett(-self.LC - 120.0, -self.LC - 15.0, self.z_gondola[0], z1p), tutto_y),
        ]
        bx0, bx1 = c['blocco_x0'], self.LF - c['blocco_dk']
        bz0, bz1 = c['blocco_z0'], c['blocco_z1']
        sdx, sdz = c['smusso_blocco_basso']
        sa = c['smusso_blocco_alto']
        blocco = [(bx0, bz0), (bx1 - sdx, bz0), (bx1, bz0 + sdz), (bx1, bz1)]
        blocco += [(bx0 + sa, bz1), (bx0, bz1 - sa)] if sa > 0 else [(bx0, bz1)]
        self.blocco = blocco
        sagoma = inviluppo(cerchio(0, 0, c['r_testa']) + cerchio(self.LF, 0, c['r_testa']) + [(bx0, bz1), (bx1, bz1)])
        self.FEMORE = [
            ('femore_B: piastra', sagoma, (Y(self.zs_pB_est), Y(self.zs_pB_int))),
            ('femore_A: piastra', sagoma, (Y(self.zs_pA_int), Y(self.zs_pA_est))),
            ('femore_B: blocco', blocco, (Y(self.zs_pB_int), Y(self.zs_pA_int))),
        ]
        stinco = inviluppo([(self.cul_x1, -c['stinco_semi']), (self.cul_x1, c['stinco_semi'])]
                           + cerchio(self.LT - c['piede_r'], 0.0, c['piede_r']))
        self.TIBIA = self.servo_e_culla('tibia: culla ginocchio', 0.0) + [('tibia: stinco', stinco, (-c['stinco_y'], c['stinco_y']))]

    # ------------------------------------------------------------------ contatti
    @staticmethod
    def trasforma(poly, ang_deg, ox, oz):
        co, si = math.cos(math.radians(ang_deg)), math.sin(math.radians(ang_deg))
        return [(ox + co * x - si * z, oz + si * x + co * z) for x, z in poly]

    def posa(self, alpha, gamma):
        kx, kz = self.LF * math.cos(math.radians(alpha)), self.LF * math.sin(math.radians(alpha))
        fem = [(n, self.trasforma(p, alpha, 0, 0), y) for n, p, y in self.FEMORE]
        tib = [(n, self.trasforma(p, alpha + 180.0 + gamma, kx, kz), y) for n, p, y in self.TIBIA]
        return self.COXA, fem, tib

    def coppie(self, alpha, gamma):
        cox, fem, tib = self.posa(alpha, gamma)
        for g1, g2 in ((fem, cox), (tib, fem), (tib, cox)):
            for n1, p1, y1 in g1:
                for n2, p2, y2 in g2:
                    if min(y1[1], y2[1]) - max(y1[0], y2[0]) > -self.GIOCO:
                        yield distanza(p1, p2), n1 + ' / ' + n2

    def contatti(self, alpha, gamma):
        return [(n, round(d, 2)) for d, n in self.coppie(alpha, gamma) if d < self.GIOCO]

    def gioco_minimo(self, alpha, gamma):
        return min(self.coppie(alpha, gamma))

    def pose_di_marcia(self, h, xf0, alzata=30.0, passi=9):
        """Pose (alpha, gamma) di tutte le zampe su appoggio + volo, come calc/statica_tripode.py."""
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import statica_tripode as st
        cfg = dict(st.CONFIG, Lc=float(self.LC), Lf=self.LF, Lt=self.LT, h=float(h), x_f0=float(xf0))
        out = []
        for n in cfg['coxa']:
            cx, cy, _ = cfg['coxa'][n]
            fx, fy = st.piede_neutro(cfg, n)
            for i in range(passi):
                d = -cfg['passo'] / 2 + cfg['passo'] * i / (passi - 1)
                x_f = math.hypot(fx - d - cx, fy - cy) - cfg['Lc']
                for dz in (0.0, alzata / 2, alzata):
                    s = st.ik_piano(x_f, h - dz, self.LF, self.LT)
                    if s is not None:
                        out.append((s[0], s[3]))
        return out


def _sep(a, b):
    for poly in (a, b):
        n = len(poly)
        for i in range(n):
            p, q = poly[i], poly[(i + 1) % n]
            nx, nz = q[1] - p[1], p[0] - q[0]
            pa = [nx * x + nz * z for x, z in a]
            pb = [nx * x + nz * z for x, z in b]
            if max(pa) < min(pb) or max(pb) < min(pa):
                return True
    return False


def _d_ps(p, a, b):
    ex, ez = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * ex + (p[1] - a[1]) * ez) / (ex * ex + ez * ez)))
    return math.hypot(p[0] - a[0] - t * ex, p[1] - a[1] - t * ez)


def distanza(a, b):
    if not _sep(a, b):
        return 0.0
    return min(_d_ps(p, Q[i], Q[(i + 1) % len(Q)]) for P, Q in ((a, b), (b, a)) for p in P for i in range(len(Q)))


def rapporto(z, mappa=True):
    c = z.c
    print('Lf %g, Lt %g, Lc %d; larghezza della zampa lungo Y %.1f mm' % (z.LF, z.LT, z.LC, z.larghezza))
    print('Coxa: alette del servo di coxa Z %.2f; braccio inferiore Z %.2f..%.2f; ponte Z %.2f..%.2f; gondola Z %.2f..%.2f'
          % (z.H, z.z_braccio[0], z.z_braccio[1], z.z_ponte[0], z.z_ponte[1], z.z_gondola[0], z.z_gondola[1]))
    print('Blocco del femore: X %.1f..%.1f; posa di riferimento: gioco minimo %.2f mm (%s)'
          % (c['blocco_x0'], z.LF - c['blocco_dk'], *z.gioco_minimo(0, 90)))
    A = list(range(-40, 81, 5))
    G = list(range(30, 161, 5))
    libero = {(a, g): not z.contatti(a, g) for a in A for g in G}
    if mappa:
        print('Mappa: righe alpha da -40 a +80, colonne gamma da 30 a 160 ogni 5; . libero, # contatto')
        for a in A:
            print('%+5d   ' % a + ''.join('.' if libero[(a, g)] else '#' for g in G))
    rich = [(a, g) for a in A if -30 <= a <= 65 for g in G if 40 <= g <= 150]
    occ = [p for p in rich if not libero[p]]
    print('Rettangolo richiesto alpha -30..+65 x gamma 40..150: %d pose, %d con contatto %s' % (len(rich), len(occ), occ))
    for g0 in (40, 90, 150):
        al = [a for a in range(-90, 121) if not z.contatti(a, g0)]
        print('  gamma %3d: alpha %+d..%+d   sopra: %s' % (g0, al[0], al[-1], z.contatti(al[-1] + 1, g0)[0][0]))
    for a0 in (-40, -30, 0, 17.5, 40, 65, 75):
        gl = [g for g in range(0, 181) if not z.contatti(a0, g)]
        print('  alpha %+5.1f: gamma %d..%d   chiuso da: %s' % (a0, gl[0], gl[-1], z.contatti(a0, gl[0] - 1)[0][0]))
    print('Pose di marcia (6 zampe, passo 60, appoggio + volo con alzata 30)')
    for h, xf0 in ((130, 25), (110, 40), (100, 45), (90, 55), (80, 60), (70, 70)):
        pose = z.pose_di_marcia(h, xf0)
        if not pose:
            print('  h %3d / x_f0 %2d: fuori portata' % (h, xf0))
            continue
        urti = sorted({(round(a), round(g)) for a, g in pose if z.contatti(a, g)})
        d, n = min(z.gioco_minimo(a, g) for a, g in pose)
        print('  h %3d / x_f0 %2d: alpha %+4.0f..%+4.0f, gamma %3.0f..%3.0f; gioco minimo %4.1f mm (%s) -> %s'
              % (h, xf0, min(p[0] for p in pose), max(p[0] for p in pose), min(p[1] for p in pose),
                 max(p[1] for p in pose), d, n, 'libero' if not urti else 'CONTATTO %s' % urti))


if __name__ == '__main__':
    kw = {}
    for a in sys.argv[1:]:
        k, v = a.split('=')
        kw[k] = eval(v)      # numeri o tuple, scritti a mano da chi lancia lo script
    rapporto(Zampa(**kw))
