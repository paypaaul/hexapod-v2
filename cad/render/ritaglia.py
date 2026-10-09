"""Ritaglia i render di Fusion sul contenuto con lo stesso margine e li porta tutti a 1800 x 1200: le inquadrature in
prospettiva della vista di Fusion non tornano identiche tra una chiamata e l'altra (viste.py).

    python3 cad/render/ritaglia.py docs/immagini/render-*.png
"""
import sys

import numpy as np
from PIL import Image

LARGHEZZA, ALTEZZA, MARGINE, SOGLIA = 1800, 1200, 0.07, 22


def ritaglia(percorso):
    im = Image.open(percorso).convert('RGB')
    a = np.asarray(im).astype(int)
    fondo = a[5, 5]
    diverso = (np.abs(a - fondo).max(axis=2) > SOGLIA)
    righe, colonne = np.where(diverso.any(axis=1))[0], np.where(diverso.any(axis=0))[0]
    y0, y1, x0, x1 = righe[0], righe[-1], colonne[0], colonne[-1]
    w, h = x1 - x0, y1 - y0
    # riquadro 3:2 attorno al contenuto, con il margine sul lato che comanda
    scala = max(w / (LARGHEZZA * (1 - 2 * MARGINE)), h / (ALTEZZA * (1 - 2 * MARGINE)))
    W, H = LARGHEZZA * scala, ALTEZZA * scala
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    tela = Image.new('RGB', (int(W), int(H)), tuple(int(c) for c in fondo))
    tela.paste(im, (int(W / 2 - cx), int(H / 2 - cy)))
    tela.resize((LARGHEZZA, ALTEZZA), Image.LANCZOS).save(percorso)
    return percorso, (int(x0), int(y0), int(x1), int(y1)), round(scala, 3)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(ritaglia(p))
