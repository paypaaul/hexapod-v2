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


# ------------------------------------------------------------------------------------------ controlli sui passi
def _con_sezioni(dati, *sezioni):
    d = copy.copy(dati)
    d.sezioni = list(sezioni)
    return d


def _sez(sid, passi, **kw):
    s = {'id': sid, 'numero': 1, 'titolo': sid, 'terna': 'zampa'}
    s.update(kw)
    return {'sezione': s, 'passi': passi}


BUONA = _sez('tibia', [
    {'id': '1.01', 'titolo': 'tibia', 'nuovi': ['zampa/Tibia']},
    {'id': '1.02', 'titolo': 'servo', 'nuovi': ['zampa/Servo_ginocchio'],
     'giunzioni': ['alette_ginocchio_coda', 'alette_ginocchio_albero'], 'fonti': ['D-049']},
])


def test_passi_buoni(dati):
    d = _con_sezioni(dati, BUONA)
    for controllo in (C.chiavi_esistenti, C.montaggio_unico, C.giunzioni_usate, C.decisioni):
        assert controllo(d) == [], controllo.__name__


def test_passi_pezzo_montato_due_volte(dati):
    """La tibia montata nella sezione della zampa e di nuovo, con l'istanza, in una sezione del robot."""
    altra = _sez('corpo', [{'id': '2.01', 'titolo': 'di nuovo', 'nuovi': ['zampa/Tibia@AS']}], terna='robot')
    assert C.montaggio_unico(_con_sezioni(dati, BUONA, altra)) != []


def test_passi_giunzione_prima_dei_pezzi(dati):
    """Le viti delle alette prima che ci sia la tibia: il controllo dell'ordine deve accorgersene."""
    s = _sez('tibia', [{'id': '1.01', 'titolo': 'servo', 'nuovi': ['zampa/Servo_ginocchio'], 'giunzioni': ['alette_ginocchio_coda']}])
    assert C.giunzioni_usate(_con_sezioni(dati, s)) != []


def test_passi_chiavi_e_decisioni_inesistenti(dati):
    s = _sez('tibia', [{'id': '1.01', 'titolo': 'x', 'nuovi': ['zampa/Tibbia'], 'giunzioni': ['alette_tibia'],
                        'avvisi': [{'tipo': 'opzionale', 'testo': 'senza x'}], 'fonti': ['D-099']}])
    d = _con_sezioni(dati, s)
    assert len(C.chiavi_esistenti(d)) == 3
    assert C.decisioni(d) == ['1.01: D-099 non esiste in docs/decisioni.md']


def test_passi_viti_strette_dopo(dati):
    """Viti accostate in un passo e strette in un altro: ammesso; strette senza essere state messe: errore."""
    s = _sez('tibia', BUONA['passi'] + [{'id': '1.03', 'titolo': 'stringi',
                                          'giunzioni': [{'id': 'alette_ginocchio_coda', 'stringi': True}]}])
    assert C.giunzioni_usate(_con_sezioni(dati, s)) == []
    prima = _sez('tibia', [BUONA['passi'][0], {'id': '1.02', 'titolo': 'stringi', 'nuovi': ['zampa/Servo_ginocchio'],
                                               'giunzioni': [{'id': 'alette_ginocchio_coda', 'stringi': True}]}])
    assert C.giunzioni_usate(_con_sezioni(dati, prima)) != []
