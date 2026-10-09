"""File generati per il firmware (header e vettori di prova) aggiornati, e riferimenti Python contro il CAD."""
import genera_header
import genera_vettori
import riferimento

# le pose di cad.json -> cicli_verificati sono arrotondate a 0,01 gradi da assieme.py -> pose_tripode
ARROTONDAMENTO_CAD = 0.005 + 1e-9


def _leggi(percorso):
    with open(percorso) as f:
        return f.read()


def test_header_aggiornato(d):
    assert genera_header.genera(d) == _leggi(genera_header.USCITA), 'python3 tools/genera_header.py'


def test_vettori_aggiornati(d):
    assert genera_vettori.genera(d) == _leggi(genera_vettori.USCITA), 'python3 tools/genera_vettori.py'


def test_uscita_deterministica(d):
    assert genera_header.genera(d) == genera_header.genera(d)
    assert genera_vettori.genera(d) == genera_vettori.genera(d)


def test_segni_delle_vicine(d):
    """robot.yaml: a sinistra imb_A - imb_M e imb_M - imb_P, a destra il contrario."""
    segni = {(a, b): genera_header._segno_vicine(d, a, b) for a, b in d.yaml['vicine']}
    assert segni == {('AS', 'MS'): 1, ('MS', 'PS'): 1, ('AD', 'MD'): -1, ('MD', 'PD'): -1}


def test_riferimento_uguale_ai_cicli_del_cad(d):
    """tools/riferimento.py -> pose_tripode da' le pose verificate nel CAD (generate da assieme.py -> pose_tripode)."""
    n = 0
    for c in d.cad['cicli_verificati']:
        for p in c['pose']:
            q = riferimento.pose_tripode(d, c['h'], c['xf0'], c['passo'], c['alzata'], p['fase'], c['giro'])
            for z in d.zampe:
                assert q[z] is not None
                for a, b in zip(q[z], p['zampe'][z]):
                    assert abs(a - b) <= ARROTONDAMENTO_CAD, (c['h'], c['xf0'], c['giro'], p['fase'], z)
                n += 1
    assert n == 6 * sum(len(c['pose']) for c in d.cad['cicli_verificati'])


def test_appoggio_meta_ciclo(d):
    for f in (0.0, 0.1, 0.49):
        assert {z for z in d.zampe if riferimento.in_appoggio(d, z, f)} == set(d.yaml['tripodi'][0])
    for f in (0.5, 0.75, 0.99):
        assert {z for z in d.zampe if riferimento.in_appoggio(d, z, f)} == set(d.yaml['tripodi'][1])
