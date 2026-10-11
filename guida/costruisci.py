"""Costruzione della guida di montaggio (D-075, docs/piano-guida.md).

    .venv/bin/python -m guida.costruisci controlla      controlli contro il BOM e sui passi
    .venv/bin/python -m guida.costruisci scene [-s ID]  lotti JSON per Blender in build/guida/lotti/
    .venv/bin/python -m guida.costruisci rendi [-s ID] [-j 3]
    .venv/bin/python -m guida.costruisci tutto
"""
import argparse
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


def controlla(dati):
    esito = C.tutti(dati)
    for k, v in esito.items():
        print('%-20s %s' % (k, 'ok' if not v else '\n  ' + '\n  '.join(v)))
    avvisi = C.lunghezze(dati)
    if avvisi:
        print('avvisi\n  ' + '\n  '.join(avvisi))
    return all(not v for v in esito.values())


def scene(dati, solo=None):
    os.makedirs(os.path.join(BUILD, 'lotti'), exist_ok=True)
    lotti = []
    for sez in dati.sezioni:
        sid = sez['sezione']['id']
        if solo and sid not in solo:
            continue
        cartella = os.path.join(BUILD, 'img', sid)
        os.makedirs(cartella, exist_ok=True)
        lavori = [S.lavoro(dati, sez, p, presenti, os.path.join(cartella, p['id'] + '.png')) for p, presenti in S.stati(dati, sez)]
        p = os.path.join(BUILD, 'lotti', sid + '.json')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump({'mesh': os.path.join(BUILD, 'cad', 'mesh'), 'risoluzione': [2000, 1400], 'lavori': lavori}, f)
        lotti.append(p)
    return lotti


def rendi(lotti, paralleli=3):
    def uno(p):
        r = subprocess.run([BLENDER, '-b', '--factory-startup', '-noaudio', '--python-exit-code', '1', '-P',
                            os.path.join(D.GUIDA, 'blender', 'rendi.py'), '--', p], capture_output=True, text=True)
        righe = [x for x in r.stdout.splitlines() if x.startswith('SCRITTO') or 'Error' in x]
        return p, r.returncode, righe + ([r.stderr[-2000:]] if r.returncode else [])
    with ThreadPoolExecutor(paralleli) as ex:
        for p, rc, righe in ex.map(uno, lotti):
            print(os.path.basename(p), 'ok' if rc == 0 else 'ERRORE', len([x for x in righe if x.startswith('SCRITTO')]), 'immagini')
            if rc:
                print('\n'.join(righe))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('comando', choices=['controlla', 'scene', 'rendi', 'tutto'])
    ap.add_argument('-s', '--sezione', action='append')
    ap.add_argument('-j', type=int, default=3)
    a = ap.parse_args()
    dati = D.Dati()
    if a.comando in ('controlla', 'tutto') and not controlla(dati):
        sys.exit(1)
    if a.comando in ('scene', 'rendi', 'tutto'):
        lotti = scene(dati, a.sezione)
        if a.comando in ('rendi', 'tutto'):
            rendi(lotti, a.j)


if __name__ == '__main__':
    main()
