"""tools/descrizione.py contro il CAD (robot/pose_cad.json) e coerenza di robot.yaml con cad.json."""
import json
import math
import os

import genera_vettori
from descrizione import impronta

# software.md 6.3 chiede la diretta entro 0,05 mm dal CAD; in double la Descrizione arriva all'arrotondamento delle
# punte esportate (1e-4 mm), quindi qui si chiede di piu'.
TOLLERANZA_CAD_MM = 1e-3


def _pose_cad(d):
    with open(os.path.join(d.cartella, 'pose_cad.json')) as f:
        return json.load(f)


def test_impronta_di_cad_json(d):
    assert d.yaml['cad_sha256'] == impronta(d.percorso_cad)


def test_diretta_uguale_al_cad(d):
    pc = _pose_cad(d)
    assert len(pc['pose']) >= 50
    scarti = []
    for r in pc['pose']:
        imb = pc['segno_imbardata'] * r['G_coxa']
        p = d.piede_robot(r['zampa'], imb, r['alpha'], r['gamma'])
        scarti.append(max(abs(a - b) for a, b in zip(p, r['punta_robot'])))
    assert max(scarti) <= TOLLERANZA_CAD_MM, 'scarto massimo %.6f mm' % max(scarti)


def test_riposo_uguale_al_cad(d):
    for n, punta in _pose_cad(d)['riposo_robot'].items():
        p = d.piede_robot(n, 0.0, 0.0, 90.0)
        assert max(abs(a - b) for a, b in zip(p, punta)) <= TOLLERANZA_CAD_MM


def test_inversa_andata_e_ritorno(d):
    punti = genera_vettori.griglia(d)
    assert len(punti) > 500
    for i, imb, a, g, punta in punti:
        s = d.ik_robot(d.zampe[i], punta)
        assert s is not None
        assert abs((s[0] - imb + 180) % 360 - 180) < 1e-9
        assert abs(s[1] - a) < 1e-9 and abs(s[2] - g) < 1e-9


def test_gamma_min_interpolazione_massimo(d):
    assert d.yaml['guardia']['gamma_min_interpolazione'] == 'massimo'
    assert d.gamma_min(-37.5) == 55       # max(55, 45): la tabella non e' monotona
    assert d.gamma_min(-35.0) == 45       # sulla riga
    assert d.gamma_min(2.5) == 43
    assert d.gamma_min(-46.0) is None and d.gamma_min(86.0) is None


def test_limiti_della_guardia_dentro_quelli_meccanici(d):
    g, m = d.guardia, d.cad['limiti_meccanici']
    assert m['imbardata'][0] < g['imbardata'][0] < g['imbardata'][1] < m['imbardata'][1]
    assert m['alpha'][0] < g['alpha'][0] < g['alpha'][1] < m['alpha'][1]
    assert g['gamma_max'] < m['gamma'][1]
    # la tabella del ginocchio copre tutto il campo del femore della guardia
    assert d.tabella_gamma_min[0][0] <= g['alpha'][0] and d.tabella_gamma_min[-1][0] >= g['alpha'][1]
    # la corsa della guardia sta nella corsa utile del servo, attorno al calettamento
    assert g['corsa_servo'] <= d.yaml['servo']['corsa_gradi'] / 2
    # la somma tra vicine stringe davvero: con ogni zampa al limite si supererebbe
    assert g['somma_vicine'] < 2 * g['imbardata'][1]


def test_zampe_tripodi_vicine_canali(d):
    y = d.yaml
    zampe = set(d.zampe)
    assert zampe == set(d.cad['coxe'])
    assert sorted(n for t in y['tripodi'] for n in t) == sorted(zampe)
    assert all(a in zampe and b in zampe for a, b in y['vicine'])
    canali = [c for n in d.zampe for c in y['canali'][n].values()]
    assert len(set(canali)) == 18 and all(0 <= c <= 31 for c in canali)


def test_cicli_verificati_negli_assetti(d):
    assetti = {tuple(a) for a in d.yaml['andatura']['assetti_verificati']}
    cicli = {(c['h'], c['xf0']) for c in d.cad['cicli_verificati']}
    assert cicli == assetti


def test_coxe_simmetriche(d):
    # sinistra e destra speculari rispetto a XZ: serve alla guardia (segni delle vicine) e alla statica
    for s, dd in (('AS', 'AD'), ('MS', 'MD'), ('PS', 'PD')):
        xs, ys, ds = d.coxe[s]
        xd, yd, dd_ = d.coxe[dd]
        assert math.isclose(xs, xd) and math.isclose(ys, -yd) and math.isclose(ds, -dd_)
