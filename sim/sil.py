"""Prova SIL del tripode a comandi aperti (software.md 6.5): un "firmware" Python manda ogni 20 ms un gruppo ASCII con
i 18 canali e T20 all'emulatore della SSC-32, che pilota i servo del modello MuJoCo. Nessuna retroazione.

    python3 sim/sil.py                    # 20 s a 100/45, periodo 1,0 s
    python3 sim/sil.py --h 70 --xf0 70    # altri assetti
    python3 sim/sil.py --giro 30          # rotazione sul posto
    python3 sim/sil.py --avvio 0          # partenza a regime, senza rampa

Misure (le soglie delle asserzioni sono in sim/tests/test_sil.py, con il perche'):
- altezza dell'origine del corpo (asse dei femori) e inclinazione dell'asse Z del corpo;
- urti: contatti fra due parti del robot, e parti del robot diverse dai piedi sul pavimento;
- scivolamento: spostamento netto sul pavimento del punto del piede che tocca terra, per ogni appoggio comandato, intero
  e senza l'atterraggio (i primi FRAZIONE_ATTERRAGGIO dell'appoggio);
- coppia all'uscita dei servo (sim/servo.py), in frazione dello stallo.
"""
import argparse
import math
import os
import sys

import mujoco
import numpy as np

if __package__ in (None, ''):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim.andatura import Tripode  # noqa: E402
from sim.simulazione import Simulazione  # noqa: E402

# Periodo del ciclo: 1,0 s da' 120 mm/s con passo 60 e, a 100/45, velocita' comandate fino a 215 gradi/s, sotto i 250
# della guardia (robot.yaml -> guardia.velocita_gradi_s; software.md 4.2).
PERIODO_S = 1.0
ASSESTAMENTO_S = 1.0             # posa iniziale tenuta prima di partire: il corpo si assesta sui servo
# Rampa di passo e giro su un ciclo: partendo a regime il tripode d'appoggio passa da fermo a 120 mm/s in un
# fotogramma e il ginocchio posteriore arriva al 68 % dello stallo per 42 ms (prova del 9 ottobre 2026). Il firmware
# non partira' mai con un gradino di velocita'.
AVVIO_S = 1.0
# Atterraggio: il primo 10 % dell'appoggio (50 ms a 1,0 s di periodo). Il volo di pose_tripode torna avanti a velocita'
# costante e il piede arriva a terra ancora in moto (240 mm/s rispetto al pavimento); con il ritardo del servo (circa
# smorzamento / kp = 12 ms) e un periodo degli impulsi (20 ms) il piede si ferma entro questa finestra.
FRAZIONE_ATTERRAGGIO = 0.1


class Misure:
    """Raccoglie a ogni passo di fisica altezza, inclinazione, urti, scivolamento dei piedi in appoggio e coppie."""

    def __init__(self, sim, tripode):
        self.sim = sim
        self.tripode = tripode
        self.tripode_a = set(sim.descrizione.yaml['tripodi'][0])
        self.id_piede = {g: z for z, g in sim.piedi.items()}
        self.t_comando = 0.0
        self.attiva = False
        self.altezza, self.inclinazione, self.coppie, self.x, self.y, self.imbardata = [], [], [], [], [], []
        self.urti = {}               # (geom, geom) -> passi in contatto
        self.a_terra = {}            # parte del robot (non piede) sul pavimento -> passi in contatto
        self.finestre = {}           # (zampa, ciclo) -> [spostamento netto (x, y) mm, idem dopo l'atterraggio]
        self._vel = np.zeros(6)

    def __call__(self, sim):
        if not self.attiva:
            return
        m, d = sim.m, sim.d
        dt = m.opt.timestep
        self.altezza.append(sim.altezza_mm())
        self.inclinazione.append(sim.inclinazione_gradi())
        self.coppie.append(sim.servi.coppia(d) / sim.servi.stallo)
        self.x.append(d.qpos[0] * 1000.0)
        self.y.append(d.qpos[1] * 1000.0)
        r = d.xmat[m.body('corpo').id]
        self.imbardata.append(math.atan2(r[3], r[0]))
        fase = self.tripode.fase(self.t_comando)
        ciclo = int(self.t_comando // self.tripode.periodo_s)
        for c in d.contact[:d.ncon]:
            g1, g2 = int(c.geom1), int(c.geom2)
            if sim.pavimento not in (g1, g2):
                coppia = tuple(sorted((sim.nome_geom(g1), sim.nome_geom(g2))))
                self.urti[coppia] = self.urti.get(coppia, 0) + 1
                continue
            g = g2 if g1 == sim.pavimento else g1
            z = self.id_piede.get(g)
            if z is None:
                n = sim.nome_geom(g)
                self.a_terra[n] = self.a_terra.get(n, 0) + 1
                continue
            u = fase if z in self.tripode_a else (fase + 0.5) % 1.0
            if u >= 0.5:                              # piede comandato in volo
                continue
            # velocita' del punto del piede che tocca terra: centro della sfera piu' omega per il braccio
            mujoco.mj_objectVelocity(m, d, mujoco.mjtObj.mjOBJ_GEOM, g, self._vel, 0)
            v = self._vel[3:] + np.cross(self._vel[:3], c.pos - d.geom_xpos[g])
            f = self.finestre.setdefault((z, ciclo), [np.zeros(2), np.zeros(2)])
            f[0] += v[:2] * dt * 1000.0
            if u >= 0.5 * FRAZIONE_ATTERRAGGIO:       # l'appoggio occupa u da 0 a 0,5
                f[1] += v[:2] * dt * 1000.0

    def riassunto(self):
        s = self.sim
        tau = np.abs(np.array(self.coppie))
        netto = [float(np.hypot(*f[0])) for f in self.finestre.values()]
        caricato = [float(np.hypot(*f[1])) for f in self.finestre.values()]
        coppie = {}
        for g in ('coxa', 'femore', 'ginocchio'):
            idx = [i for i, (_, gg) in enumerate(s.attuatori) if gg == g]
            coppie[g] = float(tau[:, idx].max())
        return {
            'durata_s': len(self.altezza) * s.m.opt.timestep,
            'altezza_mm': (min(self.altezza), max(self.altezza)),
            'inclinazione_max_gradi': max(self.inclinazione),
            'urti': dict(self.urti),
            'a_terra': dict(self.a_terra),
            'appoggi': len(self.finestre),
            'scivolamento_netto_mm': (float(np.mean(netto)), max(netto)),
            'scivolamento_caricato_mm': (float(np.mean(caricato)), max(caricato)),
            'coppia_max_frazione': coppie,
            'avanzamento_mm': self.x[-1] - self.x[0],
            'deriva_laterale_mm': self.y[-1] - self.y[0],
            'rotazione_gradi': math.degrees(float(np.unwrap(self.imbardata)[-1] - self.imbardata[0])),
        }


def prova_tripode(durata_s=20.0, periodo_s=PERIODO_S, h=None, xf0=None, giro=0.0, avvio_s=AVVIO_S,
                  assestamento_s=ASSESTAMENTO_S, sim=None):
    """Tripode a comandi aperti attraverso l'emulatore; restituisce le misure (Misure.riassunto)."""
    sim = sim or Simulazione()
    trip = Tripode(sim.descrizione, periodo_s, h=h, xf0=xf0, giro=giro, avvio_s=avvio_s)
    pose0 = trip.pose(0.0)
    if any(v is None for v in pose0.values()):
        raise ValueError('assetto fuori portata: %s' % pose0)
    sim.posa_iniziale(pose0)
    sim.ssc.scrivi(sim.canali.gruppo(pose0, tempo_ms=None))     # primo comando senza T (software.md 2.4)
    misure = Misure(sim, trip)
    for _ in range(int(round(assestamento_s * 1000 / 20))):
        sim.fotogramma()
    misure.attiva = True
    for k in range(int(round(durata_s * 1000 / 20))):
        t = k * 0.020
        misure.t_comando = t
        sim.ssc.scrivi(sim.canali.gruppo(trip.pose(t)))
        sim.fotogramma(misure)
    if sim.ssc.errori or sim.ssc.avvisi:
        raise RuntimeError('emulatore della SSC-32: errori %s, avvisi %s' % (sim.ssc.errori, sim.ssc.avvisi))
    return misure.riassunto()


def stampa(r):
    print('durata %.1f s' % r['durata_s'])
    print('altezza del corpo %.1f...%.1f mm, inclinazione massima %.2f gradi'
          % (*r['altezza_mm'], r['inclinazione_max_gradi']))
    print('urti fra parti del robot: %s' % (r['urti'] or 'nessuno'))
    print('parti del robot a terra oltre ai piedi: %s' % (r['a_terra'] or 'nessuna'))
    print('scivolamento netto per appoggio (%d appoggi): medio %.2f mm, massimo %.2f; dopo l\'atterraggio medio %.2f, '
          'massimo %.2f' % (r['appoggi'], *r['scivolamento_netto_mm'], *r['scivolamento_caricato_mm']))
    print('coppia massima in frazione dello stallo: %s'
          % ', '.join('%s %.3f' % (g, v) for g, v in r['coppia_max_frazione'].items()))
    print('avanzamento %.0f mm, deriva laterale %.0f mm, rotazione %.1f gradi'
          % (r['avanzamento_mm'], r['deriva_laterale_mm'], r['rotazione_gradi']))


if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    a.add_argument('--durata', type=float, default=20.0)
    a.add_argument('--periodo', type=float, default=PERIODO_S)
    a.add_argument('--h', type=float)
    a.add_argument('--xf0', type=float)
    a.add_argument('--giro', type=float, default=0.0)
    a.add_argument('--avvio', type=float, default=AVVIO_S, help='rampa di partenza in s (0 = parte a regime)')
    x = a.parse_args()
    stampa(prova_tripode(x.durata, x.periodo, x.h, x.xf0, x.giro, x.avvio))
