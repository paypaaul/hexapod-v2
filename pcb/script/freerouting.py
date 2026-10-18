"""Sbroglio con Freerouting delle reti non ancora tracciate di una PCB, attorno alle piste gia' posate e bloccate.

Strumento di progetto, non della CI: le piste che trova si salvano in `<scheda>/piste.json` (terna del robot) e il
generatore della scheda le rimette nel PCB a ogni rigenerazione, cosi' la CI non ha bisogno di Freerouting.
Gira con il Python di KiCad (`pcbnew`: ExportSpecctraDSN e ImportSpecctraSES).

Freerouting 2.5.0 (github.com/freerouting/freerouting, rilascio v2.5.0, freerouting-2.5.0.jar), fuori dalla repo,
con OpenJDK di Homebrew (`brew install openjdk`); i percorsi si cambiano con FREEROUTING e JAVA. Freerouting conosce
larghezze e distanze delle classi di rete del progetto, non le regole a coppie del .kicad_dru: le reti con regole speciali (VBAT, segnali a 5 V vicino ai pin dell'ESP32) si
tracciano prima con script/sbroglio.py e si bloccano. Il giudice resta il DRC (controlla.py).

Uso: $KP pcb/script/freerouting.py <cartella della scheda> [passate]
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

import pcbnew

# il jar (la versione nativa a riga di comando si blocca allo sbroglio: errore di serializzazione di GraalVM) con Java
# 25 o successivo (classi versione 69); telemetria spenta e niente piste ristrette ai pin
JAVA = os.environ.get('JAVA', '/opt/homebrew/opt/openjdk/bin/java')
FREEROUTING = os.environ.get('FREEROUTING', os.path.expanduser('~/tools/freerouting/freerouting-2.5.0.jar'))
COMANDO = [JAVA, '-jar', FREEROUTING, '-l', 'en', '--router.automatic_neckdown=false',
           '--router.copper_to_edge_clearance_um=500',
           '--usage_and_diagnostic_data.disable_analytics=true', '--profile.allow_telemetry=false']
# a due strati la massa la fanno i riempimenti delle due facce; a quattro la sbroglia anche Freerouting (connessa per
# costruzione), poi i riempimenti si aggiungono sopra
SENZA_A_2_STRATI = ('GND',)


def _senza_reti(dsn, reti):
    """Toglie le reti dalla rete del file Specctra: le loro piazzole restano come ostacoli."""
    with open(dsn, encoding='utf-8') as f:
        s = f.read()
    for rete in reti:
        i = s.index('(net /%s' % rete)
        livello = 0
        for k in range(i, len(s)):
            livello += {'(': 1, ')': -1}.get(s[k], 0)
            if livello == 0:
                break
        s = s[:i] + s[k + 1:]
        s = s.replace(' /%s ' % rete, ' ').replace(' /%s)' % rete, ')')
    with open(dsn, 'w', encoding='utf-8') as f:
        f.write(s)


def _robot(p):
    return [round(pcbnew.ToMM(p.x) - 100, 4), round(100 - pcbnew.ToMM(p.y), 4)]


def piste_della_scheda(board):
    piste, vie = [], []
    for t in board.GetTracks():
        rete = t.GetNetname().lstrip('/')
        if isinstance(t, pcbnew.PCB_VIA):
            vie.append([rete, *_robot(t.GetPosition()), round(pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu)), 3),
                        round(pcbnew.ToMM(t.GetDrill()), 3)])
        else:
            piste.append([rete, t.GetLayerName(), round(pcbnew.ToMM(t.GetWidth()), 3), _robot(t.GetStart()),
                          _robot(t.GetEnd())])
    return piste, vie


def sbroglia(cartella, passate=30, minimi=None):
    """minimi = {rete: larghezza}: le piste di Freerouting piu' strette (le restringe vicino a certe piazzole anche con
    automatic_neckdown spento) si riportano alla larghezza della regola; il DRC dice se ci stanno."""
    minimi = minimi or {}
    nome = os.path.basename(os.path.abspath(cartella))
    pcb = os.path.join(cartella, nome + '.kicad_pcb')
    tmp = tempfile.mkdtemp()
    try:
        board = pcbnew.LoadBoard(pcb)
        fisse = piste_della_scheda(board)
        reti_fisse = {p[0] for p in fisse[0]}
        for t in board.GetTracks():
            t.SetLocked(True)
        # le aree che vietano solo il riempimento (sotto PTC1) nell'esportazione diventerebbero divieti per le piste
        for z in list(board.Zones()):
            if z.GetIsRuleArea() and not z.GetDoNotAllowTracks():
                board.Remove(z)
        dsn, ses = os.path.join(tmp, nome + '.dsn'), os.path.join(tmp, nome + '.ses')
        if not pcbnew.ExportSpecctraDSN(board, dsn):
            raise RuntimeError('esportazione Specctra non riuscita per %s' % pcb)
        _senza_reti(dsn, SENZA_A_2_STRATI if board.GetCopperLayerCount() == 2 else ())
        r = subprocess.run(COMANDO + ['-de', dsn, '-do', ses, '--router.autorouter.max_passes=%d' % passate],
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(ses):
            raise RuntimeError('Freerouting non ha scritto la sessione (%d):\n%s%s' % (r.returncode, r.stdout[-3000:],
                                                                                      r.stderr[-3000:]))
        if not pcbnew.ImportSpecctraSES(board, ses):
            raise RuntimeError('importazione della sessione di Freerouting non riuscita')
        # dopo ImportSpecctraSES gli oggetti di pcbnew di questo processo non si leggono piu' dal Python (SwigPyObject
        # senza tipo, anche con un LoadBoard nuovo): si salva e si legge in un processo a parte
        copia = os.path.join(tmp, nome + '_sbrogliata.kicad_pcb')
        board.Save(copia)
        letto = os.path.join(tmp, 'piste.json')
        subprocess.run([sys.executable, os.path.abspath(__file__), '--leggi', copia, letto], check=True,
                       capture_output=True)
        with open(letto, encoding='utf-8') as f:
            nuove, vie_nuove = json.load(f)
        # delle reti gia' posate si tengono le piste originali (Freerouting le riscrive sulla sua griglia)
        for p in nuove:
            p[2] = max(p[2], minimi.get(p[0], 0.0))
        piste = fisse[0] + [p for p in nuove if p[0] not in reti_fisse]
        vie = fisse[1] + [v for v in vie_nuove if v[0] not in reti_fisse]
        uscita = os.path.join(cartella, 'piste.json')
        with open(uscita, 'w', encoding='utf-8') as f:
            json.dump({'origine': 'script/sbroglio.py (reti speciali, bloccate) e Freerouting 2.5.0 (%d passate)'
                       % passate, 'piste': piste, 'vie': vie}, f)
            f.write('\n')
        righe = [x for x in r.stdout.splitlines() if 'unrouted' in x.lower() or 'completed' in x.lower()]
        return uscita, len(piste), len(vie), righe[-5:]
    finally:
        shutil.rmtree(tmp)


if __name__ == '__main__':
    if sys.argv[1] == '--leggi':
        with open(sys.argv[3], 'w', encoding='utf-8') as f:
            json.dump(piste_della_scheda(pcbnew.LoadBoard(sys.argv[2])), f)
        sys.exit(0)
    print(sbroglia(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 30))
