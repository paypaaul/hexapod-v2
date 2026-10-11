"""Controlli della guida di montaggio (D-075, docs/piano-guida.md): viti e inserti contro il BOM, caso di controllo
delle teste del lato A, con un caso negativo che deve fallire."""
import copy

import pytest

from guida.lib import controlli as C
from guida.lib import dati as D


@pytest.fixture(scope='module')
def dati():
    return D.Dati()


def test_giunzioni_complete(dati):
    assert C.giunzioni_complete(dati) == []


def test_totali_viti_come_il_bom(dati):
    assert C.totali_viti(dati) == []


def test_totali_inserti_come_il_bom(dati):
    assert C.totali_inserti(dati) == []


def test_teste_a(dati):
    assert C.teste_a(dati) == []


def test_teste_a_caso_negativo(dati):
    """Femore_A spostato di 1 mm di traverso: le viti piazzate non cadono piu' sulle teste del CAD."""
    falsi = copy.copy(dati)
    falsi.occ = copy.deepcopy(dati.occ)
    falsi.occ['zampa/Femore_A']['T'][3] += 1.0
    assert C.teste_a(falsi) != []
