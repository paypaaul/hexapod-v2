"""Modelli generati (tools/genera_modelli.py): allineati alla descrizione, cinematica uguale al CAD, masse, urti."""
import json
import math
import os
import xml.etree.ElementTree as ET

import genera_modelli as gm
import mujoco
import numpy as np
import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TOLLERANZA_MM = 0.05            # software.md 6.3, test 2


@pytest.fixture(scope='module')
def modello():
    return mujoco.MjModel.from_xml_path(os.path.join(REPO, gm.USCITA_MJCF))


def _posa(m, d, pose, z=0.5):
    """Giunti alle pose {zampa: (imb, alpha, gamma)}, corpo fermo all'origine in orizzontale, alto z metri."""
    d.qpos[:] = 0.0
    d.qpos[2] = z
    d.qpos[3] = 1.0
    for n, (imb, a, g) in pose.items():
        for k, v in (('coxa', imb), ('femore', a), ('ginocchio', g - 90.0)):
            d.qpos[m.jnt_qposadr[m.joint('g_%s_%s' % (k, n)).id]] = math.radians(v)


def _urti_interni(m, d):
    pav = m.geom('pavimento').id
    return [(m.geom(c.geom1).name, m.geom(c.geom2).name) for c in d.contact[:d.ncon] if pav not in (c.geom1, c.geom2)]


def test_file_generati_aggiornati(descrizione):
    for rel, testo in gm.genera(descrizione).items():
        with open(os.path.join(REPO, rel), encoding='utf-8') as f:
            assert f.read() == testo, '%s non e\' aggiornato: python3 tools/genera_modelli.py' % rel


def test_uscita_deterministica(descrizione):
    assert gm.genera(descrizione) == gm.genera(descrizione)


def test_masse(descrizione, modello):
    atteso = descrizione.cad['masse']['atteso_g']
    assert sum(modello.body_mass) * 1000 == pytest.approx(atteso, abs=0.1)
    seg = gm.segmenti(descrizione)
    for s in gm.SEGMENTI[1:]:
        assert seg[s][0] == pytest.approx(descrizione.cad['masse']['segmenti_g'][s], abs=0.15)
        J = np.array(seg[s][2])
        assert np.allclose(J, J.T) and np.all(np.linalg.eigvalsh(J) > 0)


def test_cinematica_mujoco_uguale_al_cad(descrizione, modello):
    with open(os.path.join(REPO, 'robot', 'pose_cad.json')) as f:
        pc = json.load(f)
    d = mujoco.MjData(modello)
    peggio_cad = peggio_descr = 0.0
    for p in pc['pose']:
        n, imb = p['zampa'], pc['segno_imbardata'] * p['G_coxa']
        _posa(modello, d, {n: (imb, p['alpha'], p['gamma'])}, z=0.0)
        mujoco.mj_kinematics(modello, d)
        punta = d.site('punta_' + n).xpos * 1000
        peggio_cad = max(peggio_cad, np.abs(punta - p['punta_robot']).max())
        peggio_descr = max(peggio_descr, np.abs(punta - descrizione.piede_robot(n, imb, p['alpha'], p['gamma'])).max())
    assert len(pc['pose']) >= 50
    assert peggio_cad < TOLLERANZA_MM
    assert peggio_descr < TOLLERANZA_MM


def test_cinematica_sei_zampe(descrizione, modello):
    d = mujoco.MjData(modello)
    rng = np.random.default_rng(0)
    lim = descrizione.cad['limiti_meccanici']
    for _ in range(500):
        n = descrizione.zampe[rng.integers(6)]
        imb, a, g = rng.uniform(*lim['imbardata']), rng.uniform(*lim['alpha']), rng.uniform(*lim['gamma'])
        _posa(modello, d, {n: (imb, a, g)}, z=0.0)
        mujoco.mj_kinematics(modello, d)
        assert np.abs(d.site('punta_' + n).xpos * 1000 - descrizione.piede_robot(n, imb, a, g)).max() < TOLLERANZA_MM


def _urdf_punte(testo, giunti):
    """Cinematica diretta dell'URDF (catena di trasformate), punte dei piedi in mm."""
    r = ET.fromstring(testo)
    per_figlio = {j.find('child').get('link'): j for j in r.findall('joint')}

    def trasformata(link):
        if link not in per_figlio:
            return np.eye(4)
        j = per_figlio[link]
        o = j.find('origin')
        xyz = [float(x) for x in o.get('xyz').split()]
        rr, pp, yy = [float(x) for x in o.get('rpy').split()]
        T = np.eye(4)
        cz, sz, cy, sy, cx, sx = math.cos(yy), math.sin(yy), math.cos(pp), math.sin(pp), math.cos(rr), math.sin(rr)
        rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
        ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
        rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
        T[:3, :3] = rz @ ry @ rx
        T[:3, 3] = xyz
        if j.get('type') == 'revolute':
            a = np.array([float(x) for x in j.find('axis').get('xyz').split()])
            q = giunti.get(j.get('name'), 0.0)
            K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
            R = np.eye(4)
            R[:3, :3] = np.eye(3) + math.sin(q) * K + (1 - math.cos(q)) * K @ K
            T = T @ R
        return trasformata(j.find('parent').get('link')) @ T

    return {link[6:]: trasformata(link)[:3, 3] * 1000 for link in per_figlio if link.startswith('piede_')}


def test_cinematica_urdf(descrizione):
    testo = gm.urdf(descrizione)
    rng = np.random.default_rng(1)
    for _ in range(50):
        pose = {n: (rng.uniform(-35, 35), rng.uniform(-49, 85), rng.uniform(29, 180)) for n in descrizione.zampe}
        q = {}
        for n, (imb, a, g) in pose.items():
            q.update({'g_coxa_' + n: math.radians(imb), 'g_femore_' + n: math.radians(a),
                      'g_ginocchio_' + n: math.radians(g - 90.0)})
        punte = _urdf_punte(testo, q)
        for n, p in pose.items():
            assert np.abs(punte[n] - descrizione.piede_robot(n, *p)).max() < TOLLERANZA_MM


def test_limiti_giunti(descrizione, modello):
    lim = descrizione.cad['limiti_meccanici']
    for n in descrizione.zampe:
        for g, (lo, hi) in (('coxa', lim['imbardata']), ('femore', lim['alpha']),
                            ('ginocchio', (lim['gamma'][0] - 90, lim['gamma'][1] - 90))):
            r = modello.jnt_range[modello.joint('g_%s_%s' % (g, n)).id]
            assert np.degrees(r) == pytest.approx((lo, hi), abs=1e-4)


def test_sensori_e_attuatori(descrizione, modello):
    for n in descrizione.zampe:
        assert modello.sensor('contatto_' + n).type == mujoco.mjtSensor.mjSENS_TOUCH
    for s in ('imu_acc', 'imu_gyro', 'imu_quat'):
        assert modello.sensor(s).objid == modello.site('imu').id
    assert modello.nu == 18
    sv = gm.servo(descrizione)
    assert modello.actuator_forcerange[0][1] == pytest.approx(sv['stallo_nm'], rel=1e-4)
    assert sv['stallo_nm'] == pytest.approx(11.0 * 0.0980665, rel=1e-9)        # 11 kgf cm a 6 V


def test_nessun_urto_nelle_pose_verificate(descrizione, modello):
    """Le pose dei cicli verificati nel CAD sono senza urti: le primitive non devono vederne."""
    d = mujoco.MjData(modello)
    n = 0
    for c in descrizione.cad['cicli_verificati']:
        for p in c['pose']:
            _posa(modello, d, {z: tuple(v) for z, v in p['zampe'].items()})
            mujoco.mj_forward(modello, d)
            assert _urti_interni(modello, d) == [], (c['h'], c['xf0'], c['giro'], p['fase'])
            n += 1
    assert n == sum(len(c['pose']) for c in descrizione.cad['cicli_verificati'])


def test_contatto_fra_vicine_come_nel_cad(descrizione, modello):
    """Nel CAD due vicine ruotate una verso l'altra si toccano fra 31 e 32 gradi ciascuna (D-061, D-063)."""
    d = mujoco.MjData(modello)
    neutra = {n: (0.0, 0.0, 90.0) for n in descrizione.zampe}
    for ang, atteso in ((30.0, False), (31.0, False), (32.0, True)):
        _posa(modello, d, {**neutra, 'AS': (ang, 0.0, 90.0), 'MS': (-ang, 0.0, 90.0)})
        mujoco.mj_forward(modello, d)
        assert bool(_urti_interni(modello, d)) == atteso, ang


def test_ginocchio_minimo_come_nel_cad(descrizione, modello):
    """Il ginocchio piu' chiuso senza urti nel modello sta vicino alla tabella del CAD (cad.json -> gamma_min): da 1
    grado sotto a 4 sopra, perche' le primitive sono un po' piu' grosse delle parti vere. Sopra alpha 40 la tabella
    vale il fine corsa meccanico, che nel modello e' il limite del giunto."""
    d = mujoco.MjData(modello)
    neutra = {n: (0.0, 0.0, 90.0) for n in descrizione.zampe}
    for a, gmin in descrizione.tabella_gamma_min:
        if a > 40:
            continue
        g = 180.0
        while True:
            _posa(modello, d, {**neutra, 'AS': (0.0, a, g - 0.5)})
            mujoco.mj_forward(modello, d)
            if _urti_interni(modello, d):
                break
            g -= 0.5
        assert gmin - 1.0 <= g <= gmin + 4.0, (a, gmin, g)
