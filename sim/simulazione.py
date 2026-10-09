"""Simulazione in MuJoCo comandata come il robot vero: comandi ASCII -> emulatore della SSC-32 -> impulsi ogni 20 ms
-> angoli dei giunti (robot.yaml) -> servo (sim/servo.py) -> fisica a passi di 2 ms.

    sim = Simulazione()
    sim.posa_iniziale(pose)                    # giunti e altezza del corpo con i piedi a terra
    sim.ssc.scrivi(b'#0P1500...T20\\r')        # come farebbe il firmware
    sim.fotogramma(osserva)                    # 20 ms di fisica; osserva(sim) dopo ogni passo
"""
import math
import os
import sys

import mujoco
import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(QUI)
for p in (REPO, os.path.join(REPO, 'tools')):
    if p not in sys.path:
        sys.path.insert(0, p)

from descrizione import Descrizione  # noqa: E402

from sim.servo import Servi  # noqa: E402
from sim.ssc32_emu import GIUNTI, PERIODO_MS, SSC32, Canali  # noqa: E402

MJCF = os.path.join(QUI, 'modello', 'esapode.xml')


def q_da_angoli(imbardata, alpha, gamma):
    """Angoli della descrizione (gradi) -> q dei giunti del modello (rad): coxa, femore, ginocchio."""
    return math.radians(imbardata), math.radians(alpha), math.radians(gamma - 90.0)


class Simulazione:
    def __init__(self, descrizione=None, modello=MJCF):
        self.descrizione = descrizione or Descrizione()
        self.m = mujoco.MjModel.from_xml_path(modello)
        self.d = mujoco.MjData(self.m)
        self.ssc = SSC32()
        self.canali = Canali(self.descrizione)
        self.servi = Servi(self.m)
        self.passi = int(round(PERIODO_MS / 1000.0 / self.m.opt.timestep))
        # attuatore i -> (zampa, giunto); i nomi degli attuatori sono <giunto>_<zampa>
        self.attuatori = []
        for i in range(self.m.nu):
            g, z = self.m.actuator(i).name.split('_')
            self.attuatori.append((z, g))
        self.obiettivo = np.full(self.m.nu, np.nan)
        self.tempo = 0.0
        self.pavimento = self.m.geom('pavimento').id
        self.piedi = {z: self.m.geom('piede_' + z).id for z in self.descrizione.zampe}

    def posa_iniziale(self, pose):
        """Giunti alle pose {zampa: (imb, alpha, gamma)}, corpo orizzontale con il piede piu' basso a terra, fermo."""
        mujoco.mj_resetData(self.m, self.d)
        for i, (z, g) in enumerate(self.attuatori):
            self.d.qpos[self.servi.qadr[i]] = q_da_angoli(*pose[z])[GIUNTI.index(g)]
        self.d.qpos[0:3] = 0.0
        self.d.qpos[3:7] = (1.0, 0.0, 0.0, 0.0)
        mujoco.mj_kinematics(self.m, self.d)
        r = self.m.geom_size[list(self.piedi.values())[0]][0]
        basso = min(self.d.geom_xpos[g][2] - r for g in self.piedi.values())
        self.d.qpos[2] = -basso
        self.obiettivo[:] = self.d.qpos[self.servi.qadr]
        mujoco.mj_forward(self.m, self.d)

    def fotogramma(self, osserva=None):
        """Un fotogramma della SSC-32 (20 ms): nuovi impulsi, poi i passi di fisica."""
        ang = self.canali.angoli(self.ssc.fotogramma())
        for i, (z, g) in enumerate(self.attuatori):
            k = GIUNTI.index(g)
            a = ang[z][k]
            if a is None:
                self.obiettivo[i] = np.nan
            else:
                trio = [0.0, 0.0, 90.0]
                trio[k] = a
                self.obiettivo[i] = q_da_angoli(*trio)[k]
        for _ in range(self.passi):
            self.servi.applica(self.d, self.obiettivo)
            mujoco.mj_step(self.m, self.d)
            self.tempo += self.m.opt.timestep
            if osserva:
                osserva(self)

    # ---------------------------------------------------------------------------------------------- letture
    def altezza_mm(self):
        """Quota dell'origine del corpo (asse dei femori) sul pavimento."""
        return self.d.qpos[2] * 1000.0

    def inclinazione_gradi(self):
        """Angolo fra l'asse Z del corpo e la verticale."""
        zz = self.d.xmat[self.m.body('corpo').id].reshape(3, 3)[2, 2]
        return math.degrees(math.acos(max(-1.0, min(1.0, zz))))

    def nome_geom(self, g):
        return mujoco.mj_id2name(self.m, mujoco.mjtObj.mjOBJ_GEOM, g)
