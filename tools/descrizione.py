"""Descrizione del robot per strumenti, generatori e test: unisce robot/robot.yaml (scritto a mano) e robot/cad.json
(esportato dal modello Fusion con cad/script/esporta_robot.py) e da' la cinematica di riferimento in Python.

La cinematica e' quella di calc/statica_tripode.py -> ik_piano e di cad/script/assieme.py -> pose_tripode; la diretta
coincide con le pose lette dal CAD (robot/pose_cad.json) entro 0,001 mm (9 ottobre 2026).

    python3 tools/descrizione.py                 # controlla l'impronta di cad.json e stampa un riassunto
    python3 tools/descrizione.py --aggiorna-hash # dopo una nuova esportazione dal CAD
"""
import hashlib
import math
import os
import sys

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROBOT = os.path.join(REPO, 'robot')


def impronta(percorso):
    with open(percorso, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


class Descrizione:
    """robot.yaml + cad.json. Lunghezze in mm, angoli in gradi (vedi le terne in robot.yaml)."""

    def __init__(self, cartella=ROBOT, controlla=True):
        import json
        self.cartella = cartella
        with open(os.path.join(cartella, 'robot.yaml')) as f:
            self.yaml = yaml.safe_load(f)
        self.percorso_cad = os.path.join(cartella, self.yaml['cad'])
        with open(self.percorso_cad) as f:
            self.cad = json.load(f)
        if controlla and self.yaml.get('cad_sha256') != impronta(self.percorso_cad):
            raise ValueError('robot.yaml -> cad_sha256 non corrisponde a %s: dopo un\'esportazione dal CAD lanciare '
                             '"python3 tools/descrizione.py --aggiorna-hash" e rigenerare' % self.percorso_cad)
        z = self.cad['zampa']
        self.Lc, self.Lf, self.Lt = z['Lc'], z['Lf'], z['Lt']
        self.zampe = list(self.yaml['zampe'])
        self.coxe = {n: (c['x'], c['y'], c['direzione']) for n, c in self.cad['coxe'].items()}
        self.tabella_gamma_min = sorted((float(k), float(v)) for k, v in self.cad['limiti_meccanici']['gamma_min'].items())
        self.guardia = self.yaml['guardia']

    # ------------------------------------------------------------------------------------------- limiti
    def gamma_min(self, alpha):
        """Ginocchio minimo meccanico (gioco zero) per il femore ad alpha; None fuori dalla tabella. Fra due righe
        vale il massimo dei due valori, perche' la tabella non e' monotona (robot.yaml -> gamma_min_interpolazione)."""
        t = self.tabella_gamma_min
        if alpha < t[0][0] or alpha > t[-1][0]:
            return None
        for (a0, g0), (a1, g1) in zip(t, t[1:]):
            if alpha == a0:
                return g0
            if a0 < alpha < a1:
                return max(g0, g1)
        return t[-1][1]

    # ------------------------------------------------------------------------------------------- cinematica
    def piede_zampa(self, imbardata, alpha, gamma):
        """Punta del piede nella terna della zampa (ruotata dell'imbardata attorno a Z)."""
        a = math.radians(alpha)
        b = a - math.pi + math.radians(gamma)       # direzione della tibia: alpha - (180 - gamma)
        r = self.Lc + self.Lf * math.cos(a) + self.Lt * math.cos(b)
        z = self.Lf * math.sin(a) + self.Lt * math.sin(b)
        y = math.radians(imbardata)
        return (r * math.cos(y), r * math.sin(y), z)

    def piede_robot(self, zampa, imbardata, alpha, gamma):
        """Cinematica diretta: punta del piede nella terna del robot."""
        x0, y0, d = self.coxe[zampa]
        px, py, pz = self.piede_zampa(imbardata, alpha, gamma)
        c, s = math.cos(math.radians(d)), math.sin(math.radians(d))
        return (x0 + c * px - s * py, y0 + s * px + c * py, pz)

    def ik_piano(self, x_f, h):
        """Come calc/statica_tripode.py -> ik_piano: (alpha, gamma) con il piede a x_f dall'asse del femore e h sotto,
        soluzione a ginocchio alto; None fuori portata."""
        lf, lt = self.Lf, self.Lt
        d = math.hypot(x_f, h)
        if d > lf + lt or d < abs(lf - lt) or d == 0:
            return None
        c = max(-1.0, min(1.0, (lf * lf + d * d - lt * lt) / (2 * lf * d)))
        alpha = math.atan2(-h, x_f) + math.acos(c)
        cg = (lf * lf + lt * lt - d * d) / (2 * lf * lt)
        return math.degrees(alpha), math.degrees(math.acos(max(-1.0, min(1.0, cg))))

    def ik_robot(self, zampa, p):
        """Cinematica inversa: (imbardata, alpha, gamma) per portare la punta in p (terna del robot); None fuori portata."""
        x0, y0, d = self.coxe[zampa]
        px, py = p[0] - x0, p[1] - y0
        imb = (math.degrees(math.atan2(py, px)) - d + 180.0) % 360.0 - 180.0
        s = self.ik_piano(math.hypot(px, py) - self.Lc, -p[2])
        return None if s is None else (imb, s[0], s[1])

    # ------------------------------------------------------------------------------------------- giunti del CAD
    @staticmethod
    def giunti_cad(imbardata, alpha, gamma):
        """Valori dei giunti di Fusion (G_coxa_*, G_femore, G_ginocchio) per gli angoli dati (zampa.py: SF = SG = -1)."""
        return imbardata, -alpha, -(gamma - 90.0)


def aggiorna_hash(cartella=ROBOT):
    p = os.path.join(cartella, 'robot.yaml')
    d = Descrizione(cartella, controlla=False)
    nuovo = impronta(d.percorso_cad)
    with open(p) as f:
        righe = f.readlines()
    for i, r in enumerate(righe):
        if r.startswith('cad_sha256:'):
            commento = r[r.index('#'):] if '#' in r else '\n'
            righe[i] = 'cad_sha256: %s  %s' % (nuovo, commento)
            break
    else:
        raise ValueError('cad_sha256 non trovato in %s' % p)
    with open(p, 'w') as f:
        f.writelines(righe)
    return nuovo


if __name__ == '__main__':
    if '--aggiorna-hash' in sys.argv:
        print('cad_sha256 =', aggiorna_hash())
    d = Descrizione()
    print('versione', d.yaml['versione'], '| documento', d.cad['documento'], '| Lc Lf Lt', d.Lc, d.Lf, d.Lt,
          '| massa attesa', d.cad['masse']['atteso_g'], 'g')
