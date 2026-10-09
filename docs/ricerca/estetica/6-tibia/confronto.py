#!/usr/bin/env python3
"""Tavole di confronto: le quattro tibie affiancate (ritagli delle viste di dettaglio)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

QUI = os.path.dirname(os.path.abspath(__file__))
NOMI = [('base', 'Base (oggi)'), ('v1', 'V1 rastremata dritta'), ('v2', 'V2 lama ad arco'), ('v3', 'V3 sagoma unica')]
RITAGLI = {'zampa': (560, 920, 120, 830), 'profilo': (600, 860, 180, 830)}

for vista, (x0, x1, y0, y1) in RITAGLI.items():
    fig, axs = plt.subplots(1, 4, figsize=(4 * (x1 - x0) / 100, (y1 - y0) / 100 + 0.6), dpi=100)
    for ax, (n, t) in zip(axs, NOMI):
        im = mpimg.imread(os.path.join(QUI, 'tibia_%s_%s.png' % (n, vista)))
        ax.imshow(im[y0:y1, x0:x1])
        ax.set_title(t, fontsize=12, color='#333333')
        ax.set_axis_off()
    fig.patch.set_facecolor('#e9ebee')
    plt.subplots_adjust(0, 0, 1, 0.94, 0.02, 0)
    f = os.path.join(QUI, 'confronto_%s.png' % vista)
    fig.savefig(f, facecolor=fig.get_facecolor())
    print(f)
