"""Genera i vettori di prova del nucleo C++ (firmware/test_host/vettori_generati.hpp) dalla Descrizione, da
robot/pose_cad.json, da cad.json -> cicli_verificati e da calc/statica_tripode.py.

    python3 tools/genera_vettori.py              # scrive il file
    python3 tools/genera_vettori.py --controlla  # esce con 1 se il file nel repo non e' aggiornato

Un header e non un file di dati: cosi' gli stessi vettori servono anche ai test sul chip, che non leggono la repo.
Numeri a 6 decimali (1e-6 mm o gradi, molto sotto le tolleranze dei test), con lo zero sempre positivo, perche'
l'uscita sia la stessa su ogni macchina.
"""
import json
import math
import os
import sys

import riferimento
from descrizione import REPO, Descrizione

USCITA = os.path.join(REPO, 'firmware', 'test_host', 'vettori_generati.hpp')

# griglia dei giunti per l'andata e ritorno della cinematica: dentro i limiti della guardia (robot.yaml)
GRIGLIA_IMBARDATA = (-30.0, -12.5, 0.0, 17.5, 30.0)
GRIGLIA_ALPHA = (-45.0, -20.0, 5.0, 35.0, 60.0, 82.0)
GRIGLIA_GAMMA_PUNTI = 5          # da gamma_min(alpha) + margine a gamma_max
R_MINIMO = 20.0                  # mm: con il piede vicino all'asse della coxa l'imbardata non e' definita
# fasi dell'andatura di riferimento: 40 per ciclo, spostate di 0,37/40 per non cadere sulle fasi del CAD (8 o 16)
FASI_RIFERIMENTO = [(i + 0.37) / 40.0 for i in range(40)]


def _n(x):
    x = float(x)
    if abs(x) < 5e-7:
        x = 0.0
    return '%.6ff' % x


def _riga(valori):
    return ', '.join(_n(v) for v in valori)


def _angoli(pose, zampe):
    return '{' + ', '.join('{%s}' % _riga(pose[n]) for n in zampe) + '}'


def griglia(d):
    """[(zampa, imbardata, alpha, gamma, (x, y, z))] con la punta dalla cinematica diretta di tools/descrizione.py."""
    g = d.guardia
    out = []
    for i, n in enumerate(d.zampe):
        for imb in GRIGLIA_IMBARDATA:
            for a in GRIGLIA_ALPHA:
                g0 = d.gamma_min(a) + g['gamma_margine']
                for k in range(GRIGLIA_GAMMA_PUNTI):
                    gm = g0 + (g['gamma_max'] - g0) * k / (GRIGLIA_GAMMA_PUNTI - 1)
                    r = math.hypot(*d.piede_zampa(imb, a, gm)[:2])
                    if r < R_MINIMO:
                        continue
                    out.append((i, imb, a, gm, d.piede_robot(n, imb, a, gm)))
    return out


def righe_statica(d):
    """Righe di calc/statica_tripode.py -> valuta(CONFIG) con la posizione dei piedi: (tripode, d, zampa, piede_x,
    piede_y, carico_kgf, alpha, gamma, imbardata, t_femore, t_ginocchio) e i risultati complessivi."""
    st = riferimento.statica()
    cfg = st['CONFIG']
    ris = st['valuta'](cfg, verbose=False)
    tripodi = [tuple(t) for t in st['TRIPODI']]
    out = []
    for trip, dd, n, fz, _x_f, alpha, gamma, yaw, t_f, t_t in ris['righe']:
        fx, fy = st['piede_neutro'](cfg, n)
        out.append((tripodi.index(tuple(trip)), dd, d.zampe.index(n), fx - dd, fy, fz, alpha, gamma, yaw, t_f, t_t))
    return out, ris, st['margine_stabilita'](cfg), cfg


def genera(d):
    zampe = d.zampe
    with open(os.path.join(d.cartella, 'pose_cad.json')) as f:
        pc = json.load(f)
    out = []
    w = out.append
    w('// GENERATO da tools/genera_vettori.py: non modificare a mano. Vettori di prova del nucleo (firmware/test_host).')
    w('#pragma once')
    w('')
    w('#include <cstdint>')
    w('')
    w('namespace vettori {')
    w('')
    w('inline constexpr const char* cad_sha256 = "%s";' % d.yaml['cad_sha256'])
    w('')
    w('// Punta del piede letta dal CAD con i giunti veri (robot/pose_cad.json): angoli comandati e punta nella terna')
    w('// del robot. imbardata = segno_imbardata * G_coxa.')
    w('struct PosaCad {')
    w('    uint8_t zampa;')
    w('    float angoli[3];')
    w('    float punta[3];')
    w('};')
    w('inline constexpr PosaCad pose_cad[] = {')
    for r in pc['pose']:
        ang = (pc['segno_imbardata'] * r['G_coxa'], r['alpha'], r['gamma'])
        w('    {%d, {%s}, {%s}},' % (zampe.index(r['zampa']), _riga(ang), _riga(r['punta_robot'])))
    w('};')
    w('')
    w('// Griglia dei giunti dentro i limiti della guardia, con la punta da tools/descrizione.py -> piede_robot: la')
    w('// cinematica inversa della punta deve ridare gli angoli (andata e ritorno).')
    w('struct PuntoGriglia {')
    w('    uint8_t zampa;')
    w('    float angoli[3];')
    w('    float punta[3];')
    w('};')
    w('inline constexpr PuntoGriglia griglia[] = {')
    for i, imb, a, gm, p in griglia(d):
        w('    {%d, {%s}, {%s}},' % (i, _riga((imb, a, gm)), _riga(p)))
    w('};')
    w('')
    w('// Cicli a tripode verificati senza urti nel CAD (cad.json -> cicli_verificati): pose di assieme.py ->')
    w('// pose_tripode, arrotondate a 0,01 gradi. pose_cicli[prima .. prima + fasi). Ordine delle zampe di robot.yaml.')
    w('struct Ciclo {')
    w('    float h;')
    w('    float xf0;')
    w('    float passo;')
    w('    float alzata;')
    w('    float giro;')
    w('    uint16_t prima;')
    w('    uint16_t fasi;')
    w('};')
    w('struct PosaCiclo {')
    w('    float fase;')
    w('    float angoli[%d][3];' % len(zampe))
    w('};')
    cicli = d.cad['cicli_verificati']
    righe_c, righe_p, prima = [], [], 0
    for c in cicli:
        righe_c.append('    {%s, %d, %d},' % (_riga((c['h'], c['xf0'], c['passo'], c['alzata'], c['giro'])), prima,
                                             len(c['pose'])))
        for p in c['pose']:
            righe_p.append('    {%s, %s},' % (_n(p['fase']), _angoli(p['zampe'], zampe)))
        prima += len(c['pose'])
    w('inline constexpr Ciclo cicli[] = {')
    out.extend(righe_c)
    w('};')
    w('inline constexpr PosaCiclo pose_cicli[] = {')
    out.extend(righe_p)
    w('};')
    w('')
    w('// Andatura di riferimento in Python (tools/riferimento.py -> pose_tripode, senza arrotondare) a fasi che non')
    w('// sono quelle del CAD, con i parametri di cicli[ciclo].')
    w('struct PosaRiferimento {')
    w('    uint8_t ciclo;')
    w('    float fase;')
    w('    float angoli[%d][3];' % len(zampe))
    w('};')
    w('inline constexpr PosaRiferimento andatura[] = {')
    for k, c in enumerate(cicli):
        for f in FASI_RIFERIMENTO:
            q = riferimento.pose_tripode(d, c['h'], c['xf0'], c['passo'], c['alzata'], f, c['giro'])
            if any(v is None for v in q.values()):
                raise ValueError('ciclo %d: piede fuori portata alla fase %g' % (k, f))
            w('    {%d, %s, %s},' % (k, _n(f), _angoli(q, zampe)))
    w('};')
    w('')
    righe, ris, margine, cfg = righe_statica(d)
    w('// calc/statica_tripode.py -> valuta(CONFIG): per ogni tripode e avanzamento d del corpo, i tre piedi in')
    w('// appoggio con carico, angoli e coppie (kgf, gradi, kgf*cm); in fondo i massimi e il margine di stabilita\'.')
    w('struct RigaStatica {')
    w('    uint8_t tripode;')
    w('    float d;')
    w('    uint8_t zampa;')
    w('    float piede[2];')
    w('    float carico_kgf;')
    w('    float alpha;')
    w('    float gamma;')
    w('    float imbardata;')
    w('    float t_femore;')
    w('    float t_ginocchio;')
    w('};')
    w('inline constexpr RigaStatica statica[] = {')
    for tr, dd, z, px, py, fz, a, gm, yaw, tf, tt in righe:
        w('    {%d, %s, %d, {%s}, %s, %s, %s, %s, %s, %s},'
          % (tr, _n(dd), z, _riga((px, py)), _n(fz), _n(a), _n(gm), _n(yaw), _n(tf), _n(tt)))
    w('};')
    w('inline constexpr float statica_massa_g = %s;' % _n(cfg['massa_g']))
    w('inline constexpr float statica_h = %s;' % _n(cfg['h']))
    w('inline constexpr float statica_xf0 = %s;' % _n(cfg['x_f0']))
    w('inline constexpr float statica_passo = %s;' % _n(cfg['passo']))
    w('inline constexpr float statica_stallo_kgfcm = %s;' % _n(ris['stallo']))
    w('inline constexpr float statica_t_femore = %s;' % _n(ris['t_femore']))
    w('inline constexpr float statica_t_ginocchio = %s;' % _n(ris['t_tibia']))
    w('inline constexpr float statica_margine_mm = %s;' % _n(margine))
    w('')
    w('}  // namespace vettori')
    return '\n'.join(out) + '\n'


def main(argv):
    testo = genera(Descrizione())
    if '--controlla' in argv:
        with open(USCITA) as f:
            if f.read() != testo:
                print('%s non e\' aggiornato: python3 tools/genera_vettori.py' % os.path.relpath(USCITA, REPO))
                return 1
        return 0
    os.makedirs(os.path.dirname(USCITA), exist_ok=True)
    with open(USCITA, 'w') as f:
        f.write(testo)
    print('scritto', os.path.relpath(USCITA, REPO))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
