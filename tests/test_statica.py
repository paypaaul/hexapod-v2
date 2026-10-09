"""Regressione della statica (software.md 6.3, test 6) con calc/statica_tripode.py usato com'e', e coerenza delle
sue costanti con la descrizione del robot (oggi stanno in due posti)."""
import math

import pytest
import riferimento


@pytest.fixture(scope='module')
def st():
    return riferimento.statica()


def test_regressione_a_100_45(d, st):
    """Femore al 51 % +- 1 dello stallo a 100/45 (5,65 kgf*cm) e margine di stabilita' 59 mm, come robot.yaml ->
    regressione_statica."""
    attesi = d.yaml['regressione_statica']
    ris = st['valuta'](st['CONFIG'], verbose=False)
    frazione = ris['t_femore'] / ris['stallo']
    lo, hi = attesi['femore_frazione_stallo']
    assert lo <= frazione <= hi, 'femore al %.1f %% dello stallo' % (100 * frazione)
    assert round(ris['t_femore'], 2) == attesi['femore_kgfcm']
    assert ris['t_femore'] >= ris['t_tibia']   # a 100/45 il giunto piu' caricato e' il femore (software.md 4.2)
    assert round(st['margine_stabilita'](st['CONFIG'])) == attesi['margine_stabilita_mm']


def test_calc_usa_la_descrizione(d, st):
    """Le costanti di calc/statica_tripode.py -> CONFIG coincidono con robot.yaml e cad.json: se una cambia, la
    regressione qui sopra non direbbe piu' nulla sul robot vero."""
    cfg, y = st['CONFIG'], d.yaml
    assert (cfg['Lc'], cfg['Lf'], cfg['Lt']) == (d.Lc, d.Lf, d.Lt)
    for n, (x, yy, dd) in cfg['coxa'].items():
        assert all(math.isclose(a, b) for a, b in zip((x, yy, dd), d.coxe[n])), n
    assert cfg['massa_g'] == y['massa']['attesa_g']
    assert cfg['v_servo'] == y['servo']['tensione_rail']
    assert st['stallo_kgfcm'](cfg['v_servo']) == y['servo']['stallo_kgfcm'][cfg['v_servo']]
    assert (cfg['h'], cfg['x_f0']) == (y['andatura']['assetto']['h'], y['andatura']['assetto']['xf0'])
    assert (cfg['passo'], cfg['alzata']) == (y['andatura']['passo'], y['andatura']['alzata'])
    assert [list(t) for t in st['TRIPODI']] == y['tripodi']
    assert cfg['com_xy'] == (0.0, 0.0)  # come LimitiGuardia::rigidi() nel nucleo


def test_carichi_in_equilibrio(st):
    piedi = [(167.0, 94.0), (-167.0, 94.0), (0.0, -148.0)]
    f = st['carichi_piedi'](piedi, (0.0, 0.0), 2.945)
    assert math.isclose(sum(f), 2.945)
    assert abs(sum(fi * p[0] for fi, p in zip(f, piedi))) < 1e-9
    assert abs(sum(fi * p[1] for fi, p in zip(f, piedi))) < 1e-9
