"""Generatore del tripode (sim/andatura.py): uguale alle pose verificate nel CAD e dentro i limiti della guardia."""
import pytest

from sim.andatura import Tripode, in_appoggio, pose_tripode

TOLLERANZA_GRADI = 0.01          # software.md 6.3, test 7 (il CAD arrotonda a 0,01: lo scarto vero e' entro 0,005)


def test_uguale_ai_cicli_verificati(descrizione):
    n = 0
    for c in descrizione.cad['cicli_verificati']:
        for p in c['pose']:
            calc = pose_tripode(descrizione, c['h'], c['xf0'], c['passo'], c['alzata'], p['fase'], c['giro'])
            for z, atteso in p['zampe'].items():
                caso = (c['h'], c['xf0'], c['giro'], p['fase'], z)
                assert calc[z] == pytest.approx(atteso, abs=TOLLERANZA_GRADI), caso
                n += 1
    assert n == 6 * sum(len(c['pose']) for c in descrizione.cad['cicli_verificati'])


def test_fasi_dei_tripodi(descrizione):
    a, b = descrizione.yaml['tripodi']
    assert all(in_appoggio(descrizione, z, 0.1) for z in a)
    assert not any(in_appoggio(descrizione, z, 0.1) for z in b)
    assert all(in_appoggio(descrizione, z, 0.6) for z in b)


@pytest.mark.parametrize('giro', [0.0, 30.0])
def test_dentro_la_guardia_a_100_45(descrizione, giro):
    """Il tripode della prova SIL (100/45, periodo 1,0 s) resta nei limiti di robot.yaml -> guardia."""
    g = descrizione.guardia
    t = Tripode(descrizione, 1.0, giro=giro)
    assert max(t.velocita_massima()) <= g['velocita_gradi_s']
    for i in range(200):
        for imb, alpha, gamma in t.pose(i / 200).values():
            assert g['imbardata'][0] <= imb <= g['imbardata'][1]
            assert g['alpha'][0] <= alpha <= g['alpha'][1]
            assert descrizione.gamma_min(alpha) + g['gamma_margine'] <= gamma <= g['gamma_max']


def test_rampa_di_avvio(descrizione):
    t = Tripode(descrizione, 1.0, avvio_s=1.0)
    a = descrizione.yaml['andatura']['assetto']
    neutra = descrizione.ik_piano(a['xf0'], a['h'])
    for imb, alpha, gamma in t.pose(0.0).values():
        assert (imb, alpha, gamma) == pytest.approx((0.0, neutra[0], neutra[1]), abs=1e-9)
    assert t.pose(1.5) == Tripode(descrizione, 1.0).pose(1.5)
