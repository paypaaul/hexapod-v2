"""Emulatore della SSC-32 (sim/ssc32_emu.py): protocollo ASCII, gruppi interpolati, impulsi ogni 20 ms, canali."""
import pytest

from sim.ssc32_emu import SSC32, Canali


def fotogrammi(s, n):
    return [s.fotogramma() for _ in range(n)]


def test_primo_comando_senza_t_salta_subito():
    s = SSC32()
    s.scrivi(b'#0P1500#1P1200T1000\r')            # S e T ignorati: la posizione di partenza non e' nota
    assert s.fotogramma()[:2] == [1500.0, 1200.0]
    assert s.scrivi(b'Q\r') is None and s.leggi() == b'.'


def test_gruppo_arriva_insieme_dopo_t():
    s = SSC32()
    s.scrivi(b'#0P1000#5P2000\r')
    s.fotogramma()
    s.scrivi(b'#0P1100 #5P1800 T100\r')          # 5 fotogrammi da 20 ms
    uscite = [(p[0], p[5]) for p in fotogrammi(s, 6)]
    assert uscite[0] == pytest.approx((1020.0, 1960.0))
    assert uscite[3] == pytest.approx((1080.0, 1840.0))
    assert uscite[4] == uscite[5] == (1100.0, 1800.0)


def test_velocita_s_allunga_il_gruppo():
    s = SSC32()
    s.scrivi(b'#3P1000\r')
    s.fotogramma()
    s.scrivi(b'#3P1500S1000T100\r')              # 500 us a 1000 us/s = 500 ms, piu' lungo di T
    p = [x[3] for x in fotogrammi(s, 26)]
    assert p[0] == pytest.approx(1020.0)
    assert p[23] < 1500.0 and p[24] == 1500.0
    s.leggi()
    s.scrivi(b'Q\r')
    assert s.leggi() == b'.'


def test_q_durante_il_movimento():
    s = SSC32()
    s.scrivi(b'#0P1500\r')
    s.fotogramma()
    s.scrivi(b'#0P2000T200\rQ\r')
    assert s.leggi() == b'+'


def test_qp_un_byte_per_canale():
    s = SSC32()
    s.scrivi(b'#2P1503#4P2500\r')
    s.fotogramma()
    s.scrivi(b'QP 2 QP 4 QP 7\r')
    assert s.leggi() == bytes([150, 250, 0])


def test_stop_ferma_dove_si_trova():
    for comando in (b'STOP 0\r', b'#0STOP\r'):
        s = SSC32()
        s.scrivi(b'#0P1000\r')
        s.fotogramma()
        s.scrivi(b'#0P2000T1000\r')
        fotogrammi(s, 5)
        s.scrivi(comando)
        p = [x[0] for x in fotogrammi(s, 3)]
        assert p[0] == p[2] == pytest.approx(1100.0)


def test_p0_libera_il_servo():
    s = SSC32()
    s.scrivi(b'#7P1500\r')
    s.fotogramma()
    s.scrivi(b'#7P0\r')
    assert s.fotogramma()[7] is None
    s.scrivi(b'#7P1600T500\r')                   # dopo P0 la posizione non e' nota: salta
    assert s.fotogramma()[7] == 1600.0


def test_ver_esc_minuscole_spazi_e_fuori_campo():
    s = SSC32(versione='SSC32-PROVA')
    s.scrivi(b'ver\r')
    assert s.leggi() == b'SSC32-PROVA\r'
    s.scrivi(b'#0P1700\x1b#0P1300\r')            # ESC annulla la riga in corso
    assert s.fotogramma()[0] == 1300.0
    s.scrivi(b' # 1 p 2700 \r')
    assert s.fotogramma()[1] == 2500.0 and len(s.avvisi) == 1


def test_errori_registrati():
    s = SSC32()
    s.scrivi(b'#0X1500\r#40P1500\rZ\r')
    assert len(s.errori) == 3
    assert s.fotogramma()[0] is None


def test_canali_da_robot_yaml(descrizione):
    c = Canali(descrizione)
    assert len(c.canale) == 18 and len(set(c.canale.values())) == 18
    for z, giunti in descrizione.yaml['canali'].items():
        for g, ch in giunti.items():
            assert c.canale[(z, g)] == ch
    s = descrizione.yaml['servo']
    for g, a in (('coxa', 'imbardata'), ('femore', 'alpha'), ('ginocchio', 'gamma')):
        assert c.us(g, s['calettamento'][a]) == s['centro_us']
        assert c.angolo(g, c.us(g, 12.3)) == pytest.approx(12.3)
        # verso: un impulso piu' lungo muove il giunto nel verso di robot.yaml
        assert (c.angolo(g, 1600) - c.angolo(g, 1500)) * s['verso'][g] > 0


def test_gruppo_e_ritorno_agli_angoli(descrizione):
    c = Canali(descrizione)
    pose = {z: (10.0, 25.0, 80.0) for z in descrizione.zampe}
    testo = c.gruppo(pose)
    assert testo.endswith(b'T20\r') and testo.count(b'#') == 18
    s = SSC32()
    s.scrivi(testo)
    ang = c.angoli(s.fotogramma())
    passo = 0.5 / descrizione.yaml['servo']['us_per_grado']     # arrotondamento a 1 us
    for z in descrizione.zampe:
        assert ang[z] == pytest.approx([10.0, 25.0, 80.0], abs=passo + 1e-9)
