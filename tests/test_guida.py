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


def test_passi_campi_nuovi(dati):
    """Figura che non esiste, tabella con righe storte, terna sbagliata: errori; passo solo testo: ammesso."""
    s = _sez('tibia', [{'id': '1.01', 'titolo': 'testo', 'immagine': False, 'testo': ['Controlla.']},
                       {'id': '1.02', 'titolo': 'figura', 'figura': 'schemi/manca.svg'},
                       {'id': '1.03', 'titolo': 'tabella', 'immagine': False,
                        'tabella': {'intestazione': ['a', 'b'], 'righe': [['1']]}},
                       {'id': '1.04', 'titolo': 'terna', 'terna': 'spazio', 'in_evidenza': ['zampa/Tibia']}])
    errori = C.chiavi_esistenti(_con_sezioni(dati, s))
    assert len(errori) == 3, errori


def test_controlli_solo_le_sezioni_scelte(dati):
    """Con solo, un errore in un'altra sezione non si vede; senza, si'."""
    rotta = _sez('altra', [{'id': '9.01', 'titolo': 'x', 'nuovi': ['zampa/Inesistente']}])
    d = _con_sezioni(dati, BUONA, rotta)
    assert C.chiavi_esistenti(d, solo=['tibia']) == []
    assert C.chiavi_esistenti(d) != []


def test_inserti_dal_parametro(dati):
    """Le regole dei fori per inserti prendono il diametro dal parametro del CAD (cambia con il provino)."""
    regole = {r['tipo']: r['d'] for r in dati.regole_fori if r['tipo'].startswith('inserto')}
    assert regole == {'inserto_m3': dati.manifest['parametri']['ins_m3_d'], 'inserto_m2': dati.manifest['parametri']['ins_m2_d']}


def test_posa_della_zampa(dati):
    """alfa alza il ginocchio, gamma sotto 90 porta il piede verso la coxa, coxa gira in senso antiorario."""
    from guida.lib import geom

    def centro(k):
        lo, hi = dati.componente(k)['bbox']
        return geom.punto(dati.matrice(k), [(lo[i] + hi[i]) / 2 for i in range(3)])
    d = copy.copy(dati)
    g0, p0 = centro('zampa/Servo_ginocchio'), centro('zampa/Piedino')
    try:
        d.posa = d.matrici_posa({'alfa': 20})
        assert geom.punto(d.matrice('zampa/Servo_ginocchio'), [0, 0, 0])[2] > geom.punto(dati.occ['zampa/Servo_ginocchio']['T'], [0, 0, 0])[2]
        d.posa = d.matrici_posa({'gamma': 60})
        lo, hi = d.componente('zampa/Piedino')['bbox']
        piede = geom.punto(d.matrice('zampa/Piedino'), [(lo[i] + hi[i]) / 2 for i in range(3)])
        assert piede[0] < p0[0] - 20
        d.posa = d.matrici_posa({'coxa': 20})
        assert geom.punto(d.matrice('zampa/Servo_ginocchio'), [0, 0, 0])[1] > g0[1] + 20
    finally:
        d.posa = None


def test_viti_spina_verso_il_ponte(dati):
    """Viti-spina della squadretta di coxa (filettato passante, testa sull'ingresso): la testa esce verso il ponte
    (coassiale_con), non dentro il servo. Prima della correzione la testa era sulla faccia di sotto con l'asse in su."""
    from guida.lib import fori as F
    from guida.lib import geom
    presenti = [k for k in dati.basi if k.startswith('zampa/')]
    g = dati.giunzioni['zampa']['squadretta_coxa_spine']
    lo, hi = dati.componente('zampa/Coxa_Ponte')['bbox']
    zp = sorted(geom.punto(dati.matrice('zampa/Coxa_Ponte'), [0, 0, z])[2] for z in (lo[2], hi[2]))
    for v in F.piazza(dati, 'squadretta_coxa_spine', g, presenti, 'zampa'):
        assert v['asse'][2] < -0.99
        assert zp[0] <= v['testa'][2] <= zp[1]


def test_viti_svasate_in_cima_al_cono(dati):
    """Le viti svasate (ISO 10642, lunghezza totale) hanno l'origine sulla faccia alta della testa, come in rendi.py
    mesh_vite: la testa sta in cima al cono, non sul suo fondo dove finisce il cilindro del foro.
    Vassoio, a mano (fori.json): cilindro del foro del vassoio Ø2,4 da z 1,0 a 1,7 con il cono sopra; foro dell'inserto
    della base da z 1,0 (ingresso) a -3,0 (fondo); M2 x 5 svasata con testa Ø4,0.
    Cono a 90°: (4,0 - 2,4) / 2 = 0,8 mm, testa a z 1,7 + 0,8 = 2,5. Presa 5 - (2,5 - 1,0) = 3,5 mm; fondo libero
    (2,5 - (-3,0)) - 5 = 0,5 mm. Prima della correzione: testa a 1,7, presa 4,3, fondo libero -0,3 (vite nel fondo)."""
    from guida.lib import fori as F
    presenti = C._presenti(dati, 'corpo')
    viti = F.piazza(dati, 'vassoio', dati.giunzioni['corpo']['vassoio'], presenti, 'robot')
    assert len(viti) == 4
    for v in viti:
        assert v['asse'][2] < -0.99
        assert v['testa'][2] == pytest.approx(2.5, abs=0.01)
        assert v['presa'] == pytest.approx(3.5, abs=0.01)
        assert v['fondo_libero'] == pytest.approx(0.5, abs=0.01)
