"""Prova SIL: 20 s di tripode a comandi aperti a 100/45 attraverso l'emulatore della SSC-32 (software.md 6.5).

Soglie, con il perche':
- non cade: l'asse dei femori non scende sotto h - alzata/2 (con un cedimento maggiore il piede in volo si alzerebbe
  meno della meta' di quanto comandato) e il corpo non si inclina oltre la soglia della posa sicura a 100/45 (25 gradi,
  software.md 2.6); nessuna parte diversa dai piedi tocca terra;
- nessun urto fra parti del robot (primitive di collisione del modello generato);
- scivolamento dei piedi in appoggio, come spostamento netto sul pavimento del punto che tocca terra:
  * dopo l'atterraggio (sim/sil.py -> FRAZIONE_ATTERRAGGIO) non oltre lo spostamento del piede che la banda morta dei
    tre servo lascia libero (meta' banda per giunto per la distanza dall'asse al piede): oltre, i piedi in appoggio si
    contendono il corpo piu' di quanto i servo sappiano correggere;
  * sull'appoggio intero, atterraggio compreso, non oltre il 10 % del passo. Il volo di pose_tripode atterra in moto
    (240 mm/s sul pavimento) e il piede striscia qualche millimetro: e' il limite di quel volo, che il generatore del
    firmware supera con una Bezier che arriva a velocita' zero (software.md 4.2);
  * il robot avanza (o ruota) quanto comandato entro il 10 %: controlla anche versi e canali di tutta la catena;
- coppia all'uscita dei servo sotto il 60 % dello stallo per tutta la prova (robot.yaml -> guardia: sopra il 60 % solo
  per un tempo limitato). La prova parte con una rampa di un ciclo (sim/sil.py -> AVVIO_S).
"""
import math

import pytest

from sim.sil import FRAZIONE_ATTERRAGGIO, prova_tripode

DURATA_S, PERIODO_S, AVVIO_S = 20.0, 1.0, 1.0


def soglie(descrizione):
    a = descrizione.yaml['andatura']
    s = descrizione.yaml['servo']
    h, xf0 = a['assetto']['h'], a['assetto']['xf0']
    semibanda = math.radians(s['banda_morta_us'] / 2.0 / s['us_per_grado'])
    bracci = descrizione.Lc + xf0 + math.hypot(xf0, h) + descrizione.Lt     # coxa, femore e ginocchio fino al piede
    return {
        'altezza_min_mm': h - a['alzata'] / 2.0,
        'inclinazione_max_gradi': 25.0,
        'scivolamento_caricato_mm': semibanda * bracci,
        'scivolamento_netto_mm': 0.10 * a['passo'],
        'avanzamento': 0.10,
        'coppia': descrizione.guardia['coppia_tempo_limitato'],
    }


@pytest.fixture(scope='module', params=[0.0, 30.0], ids=['dritto', 'giro_30'])
def prova(request, descrizione):
    return request.param, prova_tripode(DURATA_S, PERIODO_S, giro=request.param, avvio_s=AVVIO_S)


def test_dura_venti_secondi(prova):
    assert prova[1]['durata_s'] == pytest.approx(DURATA_S)
    assert prova[1]['appoggi'] == 6 * DURATA_S / PERIODO_S


def test_non_cade(prova, descrizione):
    r, s = prova[1], soglie(descrizione)
    assert r['altezza_mm'][0] >= s['altezza_min_mm']
    assert r['inclinazione_max_gradi'] <= s['inclinazione_max_gradi']
    assert r['a_terra'] == {}


def test_nessun_urto(prova):
    assert prova[1]['urti'] == {}


def test_piedi_in_appoggio_non_scivolano(prova, descrizione):
    r, s = prova[1], soglie(descrizione)
    assert FRAZIONE_ATTERRAGGIO <= 0.1
    assert r['scivolamento_caricato_mm'][1] <= s['scivolamento_caricato_mm']
    assert r['scivolamento_netto_mm'][1] <= s['scivolamento_netto_mm']


def test_avanza_quanto_comandato(prova, descrizione):
    giro, r = prova
    a = descrizione.yaml['andatura']
    # due passi a ciclo; durante la rampa di avvio la velocita' cresce in linea retta da zero
    cicli = (DURATA_S - AVVIO_S / 2.0) / PERIODO_S
    if giro:
        assert r['rotazione_gradi'] == pytest.approx(2 * giro * cicli, rel=soglie(descrizione)['avanzamento'])
        assert abs(r['avanzamento_mm']) < a['passo']
    else:
        assert r['avanzamento_mm'] == pytest.approx(2 * a['passo'] * cicli, rel=soglie(descrizione)['avanzamento'])
        assert abs(r['rotazione_gradi']) < 5.0


def test_coppia_sotto_il_60_per_cento(prova, descrizione):
    for g, v in prova[1]['coppia_max_frazione'].items():
        assert v < soglie(descrizione)['coppia'], g
