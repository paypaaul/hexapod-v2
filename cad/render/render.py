"""Render schematici (matplotlib) del robot attuale con le parti di un concept estetico.

Uso tipico (script dell'agente, lanciato con python3 dalla cartella del concept):

    import sys; sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica')
    from render import Scena, terna_zampa
    s = Scena()                                  # robot attuale: base, interni, servo, zampe, coperchio attuale
    s.nascondi('coperchio')                      # gruppi: base, coperchio, interni, servo_coxa, zampe_struttura, zampe_servo
    s.colore('zampe_struttura', '#3a3d42')
    s.prisma([(x, y), ...], 28.4, 30, '#f2f2f2')               # poligono nel piano XY estruso lungo Z
    s.solido([(x, y, z), ...], '#f2f2f2')                       # inviluppo convesso dei punti: comodo per forme sfaccettate
    s.scatola(x0, y0, z0, x1, y1, z1, '#ff6a13')
    s.cilindro((x, y), r, z0, z1, '#222222')
    s.solido(punti_in_terna_zampa, '#ff6a13', zampe=True)     # replicato sulle sei zampe (terna della zampa)
    s.solido(punti, '#f2f2f2', specchia_y=True)                # anche specchiato rispetto a y = 0
    s.render('/percorso/nome')                                   # scrive nome_iso_ant.png, nome_iso_post.png, nome_fianco.png, nome_alto.png

Unita' mm, terna del robot: X avanti, Y a sinistra, Z in alto, z = 0 sugli assi dei femori (posa di riferimento).
Terna della zampa: origine sull'asse della coxa a z 0, X verso l'esterno lungo la zampa, Y = Z x X (lungo l'asse del femore,
verso la piastra delle squadrette Femore_A), Z in alto. Le parti con zampe=True sono date in questa terna.
"""
import math
import os
import struct

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull

QUI = os.path.dirname(os.path.abspath(__file__))
MESH = os.path.join(QUI, 'mesh')
COLORI = {'base': '#5d636b', 'coperchio': '#6a7079', 'interni': '#6f7c8c', 'servo_coxa': '#2a2a2d',
          'zampe_struttura': '#5d636b', 'zampe_servo': '#2a2a2d'}
# assi delle coxe: (x, y, direzione in gradi), D-050
COXE = {'AS': (80, 44, 30), 'MS': (0, 48, 90), 'PS': (-80, 44, 150), 'AD': (80, -44, -30), 'MD': (0, -48, -90), 'PD': (-80, -44, -150)}
VISTE = {  # elevazione, azimut (gradi), zoom
    'iso_ant': (24, 35, 1.45), 'iso_post': (24, 215, 1.45), 'fianco': (4, 90, 1.5), 'alto': (88, 270, 1.3),
    'fronte': (6, 0, 1.5), 'zampa': (18, 60, 3.0)}


def terna_zampa(nome):
    """Matrice 4x4 dalla terna della zampa alla terna del robot (posa di riferimento)."""
    x, y, d = COXE[nome]
    c, s = math.cos(math.radians(d)), math.sin(math.radians(d))
    X, Z = np.array([c, s, 0.0]), np.array([0.0, 0.0, 1.0])
    Y = np.cross(Z, X)
    m = np.eye(4)
    m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = X, Y, Z, (x, y, 0.0)
    return m


def leggi_stl(percorso):
    with open(percorso, 'rb') as f:
        dati = f.read()
    n = struct.unpack('<I', dati[80:84])[0]
    a = np.frombuffer(dati[84:84 + n * 50], dtype=np.dtype([('n', '<3f4'), ('v', '<9f4'), ('a', '<u2')]))
    return a['v'].reshape(n, 3, 3).astype(float)


class Scena:
    def __init__(self, mesh=MESH):
        self.gruppi = {}
        for f in sorted(os.listdir(mesh)):
            if f.endswith('.stl'):
                g = f[:-4]
                self.gruppi[g] = {'tri': leggi_stl(os.path.join(mesh, f)), 'colore': COLORI.get(g, '#777777'), 'visibile': True}
        self.extra = []

    # --- gruppi del modello attuale
    def nascondi(self, *gruppi):
        for g in gruppi:
            self.gruppi[g]['visibile'] = False

    def colore(self, gruppo, c):
        self.gruppi[gruppo]['colore'] = c

    # --- parti nuove
    def _aggiungi(self, tri, colore, zampe=False, specchia_y=False, terna=None):
        tri = np.asarray(tri, dtype=float)
        if terna is not None:
            tri = _trasforma(tri, terna)
        if zampe:
            for n in COXE:
                self.extra.append((_trasforma(tri, terna_zampa(n)), colore))
            return
        self.extra.append((tri, colore))
        if specchia_y:
            m = tri.copy()
            m[:, :, 1] *= -1
            self.extra.append((m, colore))

    def mesh(self, vertici, facce, colore, **kw):
        v = np.asarray(vertici, dtype=float)
        self._aggiungi(v[np.asarray(facce)], colore, **kw)

    def solido(self, punti, colore, **kw):
        """Inviluppo convesso dei punti (forme sfaccettate). Per forme concave unire piu' solidi."""
        p = np.asarray(punti, dtype=float)
        h = ConvexHull(p)
        self._aggiungi(p[h.simplices], colore, **kw)

    def prisma(self, poligono, z0, z1, colore, asse='z', **kw):
        """Poligono (anche concavo, vertici in ordine) estruso tra z0 e z1 lungo l'asse dato ('x', 'y' o 'z').
        Per asse 'x' il poligono e' in (y, z); per 'y' in (x, z)."""
        p = np.asarray(poligono, dtype=float)
        n = len(p)
        tri = []
        for k in range(1, n - 1):                      # coperchi a ventaglio: vanno bene per poligoni convessi o a stella
            tri.append([(*p[0], z0), (*p[k], z0), (*p[k + 1], z0)])
            tri.append([(*p[0], z1), (*p[k], z1), (*p[k + 1], z1)])
        for k in range(n):
            a, b = p[k], p[(k + 1) % n]
            tri.append([(*a, z0), (*b, z0), (*b, z1)])
            tri.append([(*a, z0), (*b, z1), (*a, z1)])
        tri = np.array(tri)
        if asse == 'x':
            tri = tri[:, :, [2, 0, 1]]
        elif asse == 'y':
            tri = tri[:, :, [0, 2, 1]]
        self._aggiungi(tri, colore, **kw)

    def scatola(self, x0, y0, z0, x1, y1, z1, colore, **kw):
        self.solido([(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], colore, **kw)

    def cilindro(self, centro, r, z0, z1, colore, n=40, asse='z', **kw):
        pts = [(centro[0] + r * math.cos(2 * math.pi * k / n), centro[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
        self.prisma(pts, z0, z1, colore, asse=asse, **kw)

    # --- render
    def render(self, base, viste=('iso_ant', 'iso_post', 'fianco', 'alto'), larghezza=1500, altezza=1000, titolo=None, centro=None,
               lato=8.0):
        tri, col = [], []
        for g in self.gruppi.values():
            if g['visibile']:
                t = _suddividi(g['tri'], lato)
                tri.append(t)
                col += [g['colore']] * len(t)
        for t, c in self.extra:
            t = _suddividi(t, lato)
            tri.append(t)
            col += [c] * len(t)
        tri = np.concatenate(tri)
        rgb = np.array([matplotlib.colors.to_rgb(c) for c in col])
        lo, hi = tri.reshape(-1, 3).min(0), tri.reshape(-1, 3).max(0)
        c0 = np.array(centro) if centro is not None else (lo + hi) / 2
        r = max(hi - lo) / 2
        fatti = []
        for v in viste:
            el, az, zoom = VISTE[v] if isinstance(v, str) else v
            nome = v if isinstance(v, str) else 'vista_%d_%d' % (el, az)
            fig = plt.figure(figsize=(larghezza / 100, altezza / 100), dpi=100)
            ax = fig.add_subplot(111, projection='3d')
            ax.set_proj_type('ortho')
            # luce: dall'alto, un po' da sinistra rispetto all'osservatore
            ea, aa = math.radians(el), math.radians(az)
            vista = np.array([math.cos(ea) * math.cos(aa), math.cos(ea) * math.sin(aa), math.sin(ea)])
            luce = vista + np.array([0, 0, 1.2]) + 0.6 * np.array([-math.sin(aa), math.cos(aa), 0])
            luce /= np.linalg.norm(luce)
            nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
            nrm /= np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-9)
            nrm *= np.where((nrm @ vista) < 0, -1.0, 1.0)[:, None]          # facce sempre verso l'osservatore
            k = 0.45 + 0.65 * np.clip(nrm @ luce, 0, 1)
            spec = 0.18 * np.clip(nrm @ ((luce + vista) / np.linalg.norm(luce + vista)), 0, 1) ** 24
            fc = np.clip(rgb * k[:, None] + spec[:, None], 0, 1)
            pc = Poly3DCollection(tri, facecolors=fc, edgecolors=fc, linewidths=0.15)
            pc.set_zsort('average')
            ax.add_collection3d(pc)
            rr = r
            ax.set_xlim(c0[0] - rr, c0[0] + rr); ax.set_ylim(c0[1] - rr, c0[1] + rr); ax.set_zlim(c0[2] - rr, c0[2] + rr)
            ax.set_box_aspect((1, 1, 1), zoom=zoom)
            ax.view_init(elev=el, azim=az)
            ax.set_axis_off()
            fig.patch.set_facecolor('#e9ebee')
            ax.set_facecolor('#e9ebee')
            if titolo:
                fig.suptitle('%s - %s' % (titolo, nome), fontsize=14, color='#333333')
            plt.subplots_adjust(0, 0, 1, 1)
            f = '%s_%s.png' % (base, nome)
            fig.savefig(f, dpi=100, facecolor=fig.get_facecolor())
            plt.close(fig)
            fatti.append(f)
        return fatti


def _suddividi(tri, lato):
    """Spezza i triangoli con un lato piu' lungo di `lato` in quattro, finche' serve: l'ordinamento per profondita'
    di matplotlib e' per triangolo e sbaglia con triangoli grandi accanto a triangoli piccoli."""
    for _ in range(6):
        e = np.max(np.linalg.norm(tri - np.roll(tri, 1, axis=1), axis=2), axis=1)
        grandi = e > lato
        if not grandi.any():
            break
        t = tri[grandi]
        a, b, c = t[:, 0], t[:, 1], t[:, 2]
        ab, bc, ca = (a + b) / 2, (b + c) / 2, (c + a) / 2
        nuovi = np.concatenate([np.stack(x, axis=1) for x in ((a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca))])
        tri = np.concatenate([tri[~grandi], nuovi])
    return tri


def _trasforma(tri, m):
    t = tri.reshape(-1, 3)
    return (t @ m[:3, :3].T + m[:3, 3]).reshape(tri.shape)


if __name__ == '__main__':
    s = Scena()
    print(s.render(os.path.join(QUI, 'attuale'), titolo='Modello attuale'))
