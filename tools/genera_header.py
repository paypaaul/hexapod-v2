"""Genera l'header constexpr del firmware dalla descrizione del robot (robot/robot.yaml + robot/cad.json).

    python3 tools/genera_header.py              # scrive firmware/components/nucleo/include/nucleo/robot_generato.hpp
    python3 tools/genera_header.py --controlla  # esce con 1 se il file nel repo non e' aggiornato

L'uscita e' deterministica (ordine fisso, numeri con repr di Python): il CI la rigenera e controlla con git diff che
coincida con quella nel commit.
"""
import math
import os
import sys

from descrizione import REPO, Descrizione

USCITA = os.path.join(REPO, 'firmware', 'components', 'nucleo', 'include', 'nucleo', 'robot_generato.hpp')
GIUNTI = ('coxa', 'femore', 'ginocchio')
ANGOLI = ('imbardata', 'alpha', 'gamma')   # angolo di ciascun giunto, come in robot.yaml -> servo.calettamento


def _f(x):
    """Letterale float C++: repr di Python e' la forma piu' corta che torna allo stesso double, quindi stabile."""
    return repr(float(x)) + 'f'


def _lista(valori, fmt=_f):
    return ', '.join(fmt(v) for v in valori)


def _segno_vicine(d, a, b):
    """+1 se la zampa a, ruotando in verso positivo (antiorario), va verso b. Cosi' segno * (imb_a - imb_b) e' positivo
    quando le due vicine ruotano una verso l'altra: a sinistra imb_A - imb_M, a destra il contrario (robot.yaml)."""
    delta = (d.coxe[b][2] - d.coxe[a][2] + 180.0) % 360.0 - 180.0
    if delta == 0.0:
        raise ValueError('vicine %s e %s con la stessa direzione neutra' % (a, b))
    return 1 if delta > 0 else -1


def _valore_a_tensione(tabella, tensione, nome):
    for k, v in tabella.items():
        if math.isclose(float(k), float(tensione)):
            return float(v)
    raise ValueError('robot.yaml -> servo.%s non ha un valore a %s V (tensione_rail)' % (nome, tensione))


def genera(d):
    """Testo dell'header per la Descrizione d."""
    y, cad = d.yaml, d.cad
    zampe = d.zampe
    if sorted(zampe) != sorted(cad['coxe']):
        raise ValueError('robot.yaml -> zampe e cad.json -> coxe non hanno le stesse zampe')
    g, srv, lim, andat = y['guardia'], y['servo'], cad['limiti_meccanici'], y['andatura']
    if g.get('gamma_min_interpolazione') != 'massimo':
        raise ValueError('il nucleo applica solo gamma_min_interpolazione: massimo')
    tensione = srv['tensione_rail']
    out = []
    w = out.append
    w('// GENERATO da tools/genera_header.py a partire da robot/robot.yaml e robot/cad.json: non modificare a mano.')
    w('// Si cambia robot.yaml (o si riesporta cad.json dal CAD) e si rigenera con: python3 tools/genera_header.py')
    w('// Unita\': mm, g, gradi, microsecondi, secondi. Terne e angoli come in robot.yaml.')
    w('#pragma once')
    w('')
    w('#include <array>')
    w('#include <cstdint>')
    w('')
    w('namespace nucleo::robot {')
    w('')
    w('// Origine dei dati')
    w('inline constexpr const char* versione = "%s";' % y['versione'])
    w('inline constexpr const char* documento_cad = "%s";' % cad['documento'])
    w('inline constexpr const char* cad_sha256 = "%s";' % y['cad_sha256'])
    w('')
    w('// Zampe nell\'ordine di robot.yaml -> zampe')
    w('inline constexpr int N_ZAMPE = %d;' % len(zampe))
    w('inline constexpr int N_GIUNTI = 3;  // coxa (imbardata), femore (alpha), ginocchio (gamma)')
    w('enum IndiceZampa : uint8_t { %s };' % ', '.join('%s = %d' % (n, i) for i, n in enumerate(zampe)))
    w('inline constexpr std::array<const char*, N_ZAMPE> nomi_zampe = {%s};' % ', '.join('"%s"' % n for n in zampe))
    w('')
    w('// Geometria della zampa (cad.json -> zampa)')
    w('inline constexpr float Lc = %s;  // asse della coxa -> asse del femore' % _f(d.Lc))
    w('inline constexpr float Lf = %s;  // asse del femore -> asse del ginocchio' % _f(d.Lf))
    w('inline constexpr float Lt = %s;  // asse del ginocchio -> punta del piede' % _f(d.Lt))
    w('')
    w('// Assi delle coxe nella terna del robot (cad.json -> coxe): x, y e direzione neutra in gradi da +X')
    w('struct Coxa {')
    w('    float x;')
    w('    float y;')
    w('    float direzione;')
    w('};')
    w('inline constexpr std::array<Coxa, N_ZAMPE> coxe = {{')
    for n in zampe:
        x, yy, dd = d.coxe[n]
        w('    {%s},  // %s' % (_lista((x, yy, dd)), n))
    w('}};')
    w('')
    w('// Limiti meccanici (cad.json -> limiti_meccanici): campo libero misurato nel CAD, a gioco zero')
    w('namespace meccanici {')
    for a in ANGOLI:
        w('inline constexpr float %s_min = %s;' % (a, _f(lim[a][0])))
        w('inline constexpr float %s_max = %s;' % (a, _f(lim[a][1])))
    w('}  // namespace meccanici')
    w('')
    w('// Ginocchio minimo meccanico in funzione del femore (cad.json -> limiti_meccanici.gamma_min), per alpha')
    w('// crescente. Fra due righe vale il massimo dei due valori (robot.yaml -> guardia.gamma_min_interpolazione).')
    w('struct RigaGammaMin {')
    w('    float alpha;')
    w('    float gamma;')
    w('};')
    tab = d.tabella_gamma_min
    w('inline constexpr std::array<RigaGammaMin, %d> tabella_gamma_min = {{' % len(tab))
    for a, gm in tab:
        w('    {%s},' % _lista((a, gm)))
    w('}};')
    w('')
    w('// Limiti della guardia del firmware (robot.yaml -> guardia, software.md 2.5)')
    w('namespace guardia {')
    w('inline constexpr float imbardata_min = %s;' % _f(g['imbardata'][0]))
    w('inline constexpr float imbardata_max = %s;' % _f(g['imbardata'][1]))
    w('inline constexpr float somma_vicine = %s;  // massimo avvicinamento tra due vicine' % _f(g['somma_vicine']))
    w('inline constexpr float alpha_min = %s;' % _f(g['alpha'][0]))
    w('inline constexpr float alpha_max = %s;' % _f(g['alpha'][1]))
    w('inline constexpr float gamma_max = %s;' % _f(g['gamma_max']))
    w('inline constexpr float gamma_margine = %s;  // sopra tabella_gamma_min' % _f(g['gamma_margine']))
    w('inline constexpr float corsa_servo = %s;  // +- attorno al calettamento' % _f(g['corsa_servo']))
    w('inline constexpr float velocita_gradi_s = %s;  // per giunto' % _f(g['velocita_gradi_s']))
    w('inline constexpr float coppia_avviso = %s;  // frazioni dello stallo' % _f(g['coppia_avviso']))
    w('inline constexpr float coppia_tempo_limitato = %s;' % _f(g['coppia_tempo_limitato']))
    w('inline constexpr float coppia_rifiuto = %s;' % _f(g['coppia_rifiuto']))
    w('inline constexpr float stabilita_mm = %s;  // baricentro dai lati del poligono d\'appoggio' % _f(g['stabilita_mm']))
    w('}  // namespace guardia')
    w('')
    w('// Zampe vicine (robot.yaml -> vicine). avvicinamento = segno * (imbardata_a - imbardata_b): positivo quando le')
    w('// due zampe ruotano una verso l\'altra; segno = +1 se a, ruotando in verso antiorario, va verso b.')
    w('struct Vicine {')
    w('    uint8_t a;')
    w('    uint8_t b;')
    w('    int8_t segno;')
    w('};')
    w('inline constexpr std::array<Vicine, %d> vicine = {{' % len(y['vicine']))
    for a, b in y['vicine']:
        w('    {%s, %s, %d},' % (a, b, _segno_vicine(d, a, b)))
    w('}};')
    w('')
    w('// Tripodi (robot.yaml -> tripodi): il primo e\' in appoggio nella prima meta\' del ciclo')
    w('inline constexpr std::array<std::array<uint8_t, 3>, %d> tripodi = {{' % len(y['tripodi']))
    for t in y['tripodi']:
        w('    {%s},' % ', '.join(t))
    w('}};')
    w('')
    w('// Servo (robot.yaml -> servo). Angolo del giunto -> impulso:')
    w('//     us = centro_us + verso[giunto] * us_per_grado * (angolo - calettamento[giunto])')
    w('namespace servo {')
    w('inline constexpr const char* modello = "%s";' % srv['modello'])
    w('// canali della SSC-32 per zampa: coxa, femore, ginocchio')
    w('inline constexpr std::array<std::array<uint8_t, N_GIUNTI>, N_ZAMPE> canali = {{')
    for n in zampe:
        c = y['canali'][n]
        w('    {%s},  // %s' % (', '.join(str(int(c[j])) for j in GIUNTI), n))
    w('}};')
    w('inline constexpr std::array<int8_t, N_GIUNTI> verso = {%s};' % ', '.join(str(int(srv['verso'][j])) for j in GIUNTI))
    w('inline constexpr std::array<float, N_GIUNTI> calettamento = {%s};'
      % _lista(srv['calettamento'][a] for a in ANGOLI))
    w('inline constexpr float centro_us = %s;' % _f(srv['centro_us']))
    w('inline constexpr float us_per_grado = %s;' % _f(srv['us_per_grado']))
    w('inline constexpr float banda_morta_us = %s;' % _f(srv['banda_morta_us']))
    w('inline constexpr float periodo_ms = %s;' % _f(srv['periodo_ms']))
    w('inline constexpr float corsa_gradi = %s;' % _f(srv['corsa_gradi']))
    w('inline constexpr float tensione_rail = %s;' % _f(tensione))
    w('// a tensione_rail')
    w('inline constexpr float stallo_kgfcm = %s;' % _f(_valore_a_tensione(srv['stallo_kgfcm'], tensione, 'stallo_kgfcm')))
    w('inline constexpr float velocita_s_60 = %s;  // secondi per 60 gradi, a vuoto'
      % _f(_valore_a_tensione(srv['velocita_s_60'], tensione, 'velocita_s_60')))
    w('}  // namespace servo')
    w('')
    w('// Andatura (robot.yaml -> andatura)')
    w('namespace andatura {')
    w('inline constexpr float frequenza_hz = %s;  // ciclo di controllo' % _f(andat['frequenza_hz']))
    w('inline constexpr float h = %s;  // altezza dell\'asse dei femori dal suolo' % _f(andat['assetto']['h']))
    w('inline constexpr float xf0 = %s;  // piede neutro dall\'asse del femore' % _f(andat['assetto']['xf0']))
    w('inline constexpr float passo = %s;' % _f(andat['passo']))
    w('inline constexpr float alzata = %s;' % _f(andat['alzata']))
    w('inline constexpr float giro_max = %s;  // gradi a passo nella rotazione sul posto' % _f(andat['giro_max']))
    w('struct Assetto {')
    w('    float h;')
    w('    float xf0;')
    w('};')
    av = andat['assetti_verificati']
    w('inline constexpr std::array<Assetto, %d> assetti_verificati = {{%s}};'
      % (len(av), ', '.join('{%s}' % _lista(a) for a in av)))
    w('}  // namespace andatura')
    w('')
    w('// Masse (robot.yaml -> massa, cad.json -> masse)')
    w('namespace masse {')
    w('inline constexpr float attesa_g = %s;  // usata per le coppie stimate, come calc/statica_tripode.py'
      % _f(y['massa']['attesa_g']))
    m = cad['masse']
    w('inline constexpr float modellato_g = %s;' % _f(m['modellato_g']))
    w('inline constexpr float non_modellato_g = %s;' % _f(m['non_modellato_g']))
    for s in ('corpo', 'coxa', 'femore', 'tibia'):
        w('inline constexpr float %s_g = %s;' % (s, _f(m['segmenti_g'][s])))
    w('}  // namespace masse')
    w('')
    w('}  // namespace nucleo::robot')
    return '\n'.join(out) + '\n'


def main(argv):
    testo = genera(Descrizione())
    if '--controlla' in argv:
        with open(USCITA) as f:
            if f.read() != testo:
                print('%s non e\' aggiornato: python3 tools/genera_header.py' % os.path.relpath(USCITA, REPO))
                return 1
        return 0
    os.makedirs(os.path.dirname(USCITA), exist_ok=True)
    with open(USCITA, 'w') as f:
        f.write(testo)
    print('scritto', os.path.relpath(USCITA, REPO))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
