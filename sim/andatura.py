"""Generatore del tripode in Python, porting di cad/script/assieme.py -> pose_tripode sulla descrizione unica.

Le pose di cad.json -> cicli_verificati vengono da quella funzione nel CAD (arrotondate a 0,01 gradi): questo modulo le
riproduce entro 0,01 gradi (sim/tests/test_andatura.py). Lo stesso confronto si fara' con il nucleo C++ del firmware.

Andatura: tripode A (robot.yaml -> tripodi[0]) in appoggio nella prima meta' del ciclo, B nella seconda. In appoggio il
piede va in linea retta da +passo/2 a -passo/2 lungo X; in volo torna avanti con un'alzata a mezza sinusoide. Con giro
(gradi di rotazione del corpo a ogni passo, positivo antiorario) i piedi si spostano su archi attorno al centro del
corpo invece che lungo X: rotazione sul posto.
"""
import math


def pose_tripode(descrizione, h, xf0, passo, alzata, fase, giro=0.0):
    """{zampa: (imbardata, alpha, gamma) in gradi, oppure None se il piede e' fuori portata} alla fase 0..1."""
    d = descrizione
    tripode_a = set(d.yaml['tripodi'][0])
    out = {}
    for n in d.zampe:
        x, y, dire = d.coxe[n]
        fx = x + (d.Lc + xf0) * math.cos(math.radians(dire))
        fy = y + (d.Lc + xf0) * math.sin(math.radians(dire))
        u = fase if n in tripode_a else (fase + 0.5) % 1.0
        if u < 0.5:                                   # appoggio: il piede va da +passo/2 a -passo/2
            k, dz = 0.5 - u / 0.5, 0.0
        else:                                         # volo: torna avanti alzandosi
            v = (u - 0.5) / 0.5
            k, dz = -0.5 + v, alzata * math.sin(math.pi * v)
        if giro:                                      # nella terna del corpo il piede gira al contrario del corpo
            r = math.radians(giro * k)
            fx, fy = fx * math.cos(r) - fy * math.sin(r), fx * math.sin(r) + fy * math.cos(r)
            dx = 0.0
        else:
            dx = passo * k
        px, py = fx + dx - x, fy - y
        imb = math.degrees(math.atan2(py, px)) - dire
        imb = (imb + 180) % 360 - 180
        s = d.ik_piano(math.hypot(px, py) - d.Lc, h - dz)
        out[n] = (imb, s[0], s[1]) if s else None
    return out


def in_appoggio(descrizione, zampa, fase):
    """True se alla fase data la zampa e' comandata in appoggio."""
    u = fase if zampa in descrizione.yaml['tripodi'][0] else (fase + 0.5) % 1.0
    return u < 0.5


class Tripode:
    """Tripode nel tempo: periodo in secondi, parametri come pose_tripode (assetto e passo da robot.yaml se mancano).

    Con avvio_s > 0 passo e giro crescono in linea retta da zero nei primi avvio_s secondi: si parte dalla posa neutra
    senza il gradino di velocita' di una partenza a regime.
    """

    def __init__(self, descrizione, periodo_s, h=None, xf0=None, passo=None, alzata=None, giro=0.0, avvio_s=0.0):
        a = descrizione.yaml['andatura']
        self.d = descrizione
        self.periodo_s = periodo_s
        self.h = a['assetto']['h'] if h is None else h
        self.xf0 = a['assetto']['xf0'] if xf0 is None else xf0
        self.passo = a['passo'] if passo is None else passo
        self.alzata = a['alzata'] if alzata is None else alzata
        self.giro = giro
        self.avvio_s = avvio_s

    def fase(self, t):
        return (t / self.periodo_s) % 1.0

    def pose(self, t):
        k = min(1.0, t / self.avvio_s) if self.avvio_s > 0 else 1.0
        return pose_tripode(self.d, self.h, self.xf0, self.passo * k, self.alzata, self.fase(t), self.giro * k)

    def velocita_massima(self, campioni=400):
        """Velocita' angolare massima comandata (gradi/s) su un ciclo, per giunto, per confrontarla con la guardia."""
        dt = self.periodo_s / campioni
        massimo = [0.0, 0.0, 0.0]
        prec = self.pose(0.0)
        for i in range(1, campioni + 1):
            ora = self.pose(i * dt)
            for n in self.d.zampe:
                for k in range(3):
                    massimo[k] = max(massimo[k], abs(ora[n][k] - prec[n][k]) / dt)
            prec = ora
        return tuple(massimo)
