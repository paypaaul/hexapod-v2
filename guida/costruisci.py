"""Costruzione della guida di montaggio (D-075, docs/piano-guida.md).

    .venv/bin/python -m guida.costruisci controlla      controlli contro il BOM e sui passi
    .venv/bin/python -m guida.costruisci scene [-s ID]  lotti JSON per Blender in build/guida/lotti/
    .venv/bin/python -m guida.costruisci rendi [-s ID] [-j 3] [--forza]
    .venv/bin/python -m guida.costruisci impagina [-s ID]   HTML e verifica delle immagini
    .venv/bin/python -m guida.costruisci pdf [-s ID]        PDF, con i contenitori che debordano
    .venv/bin/python -m guida.costruisci anteprime [-s ID]  PNG di ogni pagina
    .venv/bin/python -m guida.costruisci tutto [-s ID]

Senza -s l'uscita e' build/guida/ (sito/, guida.pdf, anteprima/); con -s e' build/guida/sezioni/<id>/, cosi' piu'
estrattori lavorano insieme senza scriversi addosso. Con -s anche i controlli sui passi guardano solo quelle sezioni.

Le dipendenze in piu' stanno in guida/requirements.txt; Blender 4.5 e Chrome sono installati a parte.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from guida.lib import controlli as C
from guida.lib import dati as D
from guida.lib import scena as S

BUILD = os.path.join(D.RADICE, 'build', 'guida')
BLENDER = '/Applications/Blender.app/Contents/MacOS/Blender'


def uscita(solo):
    return os.path.join(BUILD, 'sezioni', '-'.join(sorted(solo))) if solo else BUILD


def controlla(dati, solo=None):
    esito = C.tutti(dati, solo)
    if solo and dati.errori_yaml:                   # con -s non sono errori (puo' essere il file a meta' di un altro),
        print('file illeggibili, saltati:\n  ' + '\n  '.join(dati.errori_yaml))   # ma si vedono sempre
    for k, v in esito.items():
        print('%-20s %s' % (k, 'ok' if not v else '\n  ' + '\n  '.join(v)))
    avvisi = C.lunghezze(dati)
    if avvisi:
        print('avvisi\n  ' + '\n  '.join(avvisi))
    return all(not v for v in esito.values())


def _impronta(lav, mesh):
    """Hash del lavoro e delle mesh che usa: se non cambia, il render in cache vale ancora."""
    h = hashlib.sha1(json.dumps(lav, sort_keys=True).encode())
    h.update(open(os.path.join(D.GUIDA, 'blender', 'rendi.py'), 'rb').read())
    for o in lav['oggetti']:
        h.update(str(os.path.getmtime(os.path.join(mesh, o['mesh']))).encode())
    return h.hexdigest()


def scene(dati, solo=None, forza=False):
    """Lotti per Blender: passi, punto di controllo di fine sezione, miniature dei pezzi nuovi. Salta i lavori in cache."""
    mesh = os.path.join(BUILD, 'cad', 'mesh')
    os.makedirs(os.path.join(BUILD, 'lotti'), exist_ok=True)
    lotti, componenti = {}, set()
    for sez in dati.sezioni:
        sid = sez['sezione']['id']
        if solo and sid not in solo:
            continue
        cartella = os.path.join(BUILD, 'img', sid)
        os.makedirs(cartella, exist_ok=True)
        lavori, presenti = [], []
        for p, presenti in S.stati(dati, sez):
            if S.ha_render(p):
                lavori.append(S.lavoro(dati, sez, p, presenti, os.path.join(cartella, p['id'] + '.png')))
            componenti.update(dati.occ[c]['componente'] for k in p.get('nuovi', []) for c in dati.chiavi(k))
        tutti = list(presenti) + [c for c in sum(S.entrano(dati, sez['passi'][-1]), []) if c not in presenti]
        if tutti:                                   # sezioni senza pezzi montati (procedure): niente vista finale
            lavori.append(S.finale(dati, sez, tutti, os.path.join(cartella, 'fine.png')))
        lotti[sid] = lavori
    cartella = os.path.join(BUILD, 'img', 'miniature')
    os.makedirs(cartella, exist_ok=True)
    lotti['miniature-' + ('-'.join(sorted(solo)) if solo else 'tutte')] = [
        S.miniatura(dati, c, os.path.join(cartella, c + '.png')) for c in sorted(componenti) if not c.startswith('Ingombro_')]
    percorsi, saltati = [], 0
    for nome, lavori in lotti.items():
        da_fare = []
        for lav in lavori:
            lav['impronta'] = _impronta(lav, mesh)
            j = os.path.splitext(lav['uscita'])[0] + '.impronta'
            if not forza and os.path.exists(lav['uscita']) and os.path.exists(j) and open(j).read() == lav['impronta']:
                saltati += 1
                continue
            da_fare.append(lav)
        if not da_fare:
            continue
        p = os.path.join(BUILD, 'lotti', nome + '.json')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump({'mesh': mesh, 'lavori': da_fare}, f)
        percorsi.append((p, da_fare))
    print('lavori in cache:', saltati)
    return percorsi


def rendi(lotti, paralleli=3):
    def uno(voce):
        p, lavori = voce
        r = subprocess.run([BLENDER, '-b', '--factory-startup', '-noaudio', '--python-exit-code', '1', '-P',
                            os.path.join(D.GUIDA, 'blender', 'rendi.py'), '--', p], capture_output=True, text=True)
        righe = [x for x in r.stdout.splitlines() if x.startswith('SCRITTO') or 'Error' in x]
        if r.returncode == 0:
            for lav in lavori:
                with open(os.path.splitext(lav['uscita'])[0] + '.impronta', 'w') as f:
                    f.write(lav['impronta'])
        return p, r.returncode, righe + ([r.stderr[-2000:], r.stdout[-2000:]] if r.returncode else [])
    ok = True
    with ThreadPoolExecutor(paralleli) as ex:
        for p, rc, righe in ex.map(uno, lotti):
            print(os.path.basename(p), 'ok' if rc == 0 else 'ERRORE', len([x for x in righe if x.startswith('SCRITTO')]), 'immagini')
            if rc:
                ok = False
                print('\n'.join(righe))
    return ok


def impagina(dati, solo=None):
    from guida.lib import impagina as I
    imp = I.Impaginatore(dati, BUILD, os.path.join(uscita(solo), 'sito'))
    p, n = imp.scrivi(solo)
    print('HTML', p, n, 'pagine')
    for x in imp.problemi:
        print('  immagine:', x)
    return p


def pdf(html_path, solo=None):
    from guida.lib import impagina as I
    p = os.path.join(uscita(solo), 'guida.pdf')
    deborda = I.pdf(html_path, p)
    print('PDF', p, '%.1f MB' % (os.path.getsize(p) / 1e6))
    for x in deborda:
        print('  deborda:', x)
    return not deborda


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('comando', choices=['controlla', 'scene', 'rendi', 'impagina', 'pdf', 'anteprime', 'tutto'])
    ap.add_argument('-s', '--sezione', action='append')
    ap.add_argument('-j', type=int, default=3)
    ap.add_argument('--forza', action='store_true')
    a = ap.parse_args()
    dati = D.Dati()
    if a.comando in ('controlla', 'tutto') and not controlla(dati, a.sezione):
        sys.exit(1)
    if a.comando in ('scene', 'rendi', 'tutto'):
        lotti = scene(dati, a.sezione, a.forza)
        if a.comando in ('rendi', 'tutto') and not rendi(lotti, a.j):
            sys.exit(1)
    if a.comando in ('impagina', 'pdf', 'anteprime', 'tutto'):
        p = impagina(dati, a.sezione)
        if a.comando in ('pdf', 'tutto') and not pdf(p, a.sezione):
            sys.exit(1)
        if a.comando == 'anteprime':
            from guida.lib import impagina as I
            fatti = I.anteprime(p, os.path.join(uscita(a.sezione), 'anteprima'))
            print('anteprime', os.path.dirname(fatti[0]) if fatti else '-', len(fatti))


if __name__ == '__main__':
    main()
