"""Modello dei servo MG996R attorno agli attuatori di posizione dell'MJCF (sim/modello/esapode.xml).

Nell'MJCF ogni giunto ha:
- un attuatore di posizione con kp e la coppia limitata allo stallo (11 kgf cm a 6 V, V): coppia = kp * errore fino alla
  saturazione;
- uno smorzamento del giunto pari a stallo / velocita' a vuoto (0,14 s/60 gradi, V): a piena tensione il motore segue
  la retta coppia-velocita' (stallo da fermo, zero alla velocita' a vuoto), cioe' la forza controelettromotrice.

Qui si aggiunge quello che l'MJCF non sa esprimere:
- la banda morta (larga 5 us, V, convertita in gradi con robot.yaml -> servo.us_per_grado): finche' l'errore resta
  entro meta' banda per parte il servo non spinge. Si ottiene comandando all'attuatore q + bm(errore), dove bm toglie la
  semibanda all'errore;
- il servo libero (P0 sulla SSC-32, nessun impulso): comando uguale alla posizione, nessuna spinta.

I parametri si leggono dall'MJCF (<custom>), cosi' restano quelli generati da tools/genera_modelli.py. Ritardo, gioco e
offset di taratura (software.md 4.4) non ci sono ancora: entrano con l'identificazione dei servo.
"""
import numpy as np


class Servi:
    def __init__(self, modello):
        m = modello

        def valore(nome):
            return float(m.numeric(nome).data[0])

        self.kp = valore('servo_kp')
        self.semibanda = valore('servo_semibanda_morta_rad')
        self.stallo = valore('servo_stallo_nm')
        self.smorzamento = valore('servo_smorzamento')
        giunti = m.actuator_trnid[:, 0]
        self.qadr = np.array([m.jnt_qposadr[j] for j in giunti])
        self.dadr = np.array([m.jnt_dofadr[j] for j in giunti])

    def applica(self, dati, obiettivo):
        """Imposta i comandi degli attuatori. obiettivo: angoli dei giunti in rad (NaN = servo libero)."""
        q = dati.qpos[self.qadr]
        e = obiettivo - q
        bm = np.sign(e) * np.maximum(np.abs(e) - self.semibanda, 0.0)
        dati.ctrl[:] = np.where(np.isnan(obiettivo), q, q + np.nan_to_num(bm))

    def coppia(self, dati):
        """Coppia all'uscita di ogni servo (N m): spinta dell'attuatore meno la forza controelettromotrice."""
        return dati.actuator_force - self.smorzamento * dati.qvel[self.dadr]
