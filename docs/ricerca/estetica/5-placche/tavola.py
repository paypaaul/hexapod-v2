#!/usr/bin/env python3
"""Tavola di confronto in scala: sagome e sezioni di lame, ginocchiera e spalla del carapace nelle tre versioni."""
import math
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import guscio  # noqa: E402
import varianti as VR  # noqa: E402

COL = {'Kabuto corretto': '#9aa0a8', 'Morbida': '#2f7dd1', 'Piena': '#e0601c'}


def chiudi(p):
    p = np.asarray(p)
    return np.vstack([p, p[:1]])


def sezione(p, q_val, asse_fisso, lo, hi, n=400):
    """Spessore lungo una retta (coordinata asse_fisso = q_val) campionando il campo della placca."""
    t = np.linspace(lo, hi, n)
    q = np.c_[np.full(n, q_val), t] if asse_fisso == 0 else np.c_[t, np.full(n, q_val)]
    m = p.dentro(q)
    from geo import dist_segmenti
    d = dist_segmenti(q, p.segm)
    h = np.where(m, p.spessore(q, d), np.nan)
    return t, h


def main():
    vv = [VR.kabuto(), VR.morbida(), VR.piena()]
    fig = plt.figure(figsize=(16, 11), dpi=100)
    g = fig.add_gridspec(3, 3, height_ratios=[1.1, 1, 1])
    # 1. sagome delle lame
    for k, v in enumerate(vv):
        ax = fig.add_subplot(g[0, k])
        c = COL[v.nome]
        ax.fill(*chiudi(v.contorno).T, color=c, alpha=0.25)
        ax.plot(*chiudi(v.contorno).T, color=c, lw=1.6)
        for f in v.finestre:
            ax.fill(*chiudi(f).T, color='white')
            ax.plot(*chiudi(f).T, color=c, lw=1.0)
        for xc in (55, 120):
            th = np.linspace(0, 2 * math.pi, 100)
            ax.plot(xc + 13 * np.cos(th), 13 * np.sin(th), color='#444', lw=0.6, ls='--')
        ax.plot([76.5, 82.5, 99, 99], [14, 20, 20, 14], color='#444', lw=0.6, ls='--')
        for (x, z) in VR.VITI_BLOCCO:
            ax.add_patch(plt.Circle((x, z), 2.75, color='#777'))
            if v.tubi:
                ax.add_patch(plt.Circle((x, z), VR.TUBO_R, fill=False, color=c, lw=0.6, ls=':'))
        ax.set_aspect('equal')
        ax.set_xlim(35, 140)
        ax.set_ylim(-20, 25)
        ax.set_title('%s: lama del femore (X, Z)\ntratteggio = teste del femore R 13 e blocco' % v.nome, fontsize=10)
        ax.grid(alpha=0.2)
    # 2. sezioni della lama a X 87,5 (sopra il blocco) e a X 120 (mozzo del ginocchio): spessore x 5
    ax = fig.add_subplot(g[1, 0:2])
    for v in vv:
        c = COL[v.nome]
        for xs, ls in ((87.5, '-'), (128.0, ':')):
            t, h = sezione(v.lama_B, xs, 0, -20, 25)
            ax.plot(t, 5 * h, color=c, ls=ls, lw=1.8, label='%s, X %.1f' % (v.nome, xs))
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xlabel('Z della zampa (mm)')
    ax.set_ylabel('spessore della lama x 5 (mm)')
    ax.set_title('Sezione delle lame (spessore esagerato 5 volte): faccia interna piana, cresta cilindrica, raccordo sul bordo', fontsize=10)
    ax.legend(fontsize=8, ncol=3)
    ax.grid(alpha=0.2)
    # 3. ginocchiere
    ax = fig.add_subplot(g[1, 2])
    for v in vv:
        c = COL[v.nome]
        ax.plot(*chiudi(v.gin_contorno).T, color=c, lw=1.6, label=v.nome)
    ax.set_aspect('equal')
    ax.set_title('Ginocchiera (Y, Z) sulla culla del ginocchio', fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    # 4. carapace: lobo anteriore in pianta (contorno e bordo della faccia piana)
    ax = fig.add_subplot(g[2, 0:2])
    for v in vv:
        c = COL[v.nome]
        cont = guscio.contorno(v.car)
        ax.plot(*chiudi(cont).T, color=c, lw=1.6, label='%s: contorno' % v.nome)
        prof = guscio.profilo(v.car)
        from scena import rientra
        q = rientra(geo_ccw(cont), prof[-1][0])
        ax.plot(*chiudi(q).T, color=c, lw=0.8, ls='--')
    ax.set_aspect('equal')
    ax.set_xlim(-10, 120)
    ax.set_ylim(15, 80)
    ax.set_title('Carapace in pianta, meta anteriore sinistra (pieno = contorno a z 28,4; tratteggio = bordo della faccia piana a z 36)', fontsize=10)
    ax.legend(fontsize=8, loc='lower left')
    ax.grid(alpha=0.2)
    # 5. spalla del carapace in sezione
    ax = fig.add_subplot(g[2, 2])
    for v in vv:
        p = np.array(guscio.profilo(v.car))
        ax.plot(-p[:, 0], p[:, 1], color=COL[v.nome], lw=1.8, label=v.nome)
    ax.set_aspect('equal')
    ax.set_title('Spalla del carapace in sezione (rientro, z)', fontsize=10)
    ax.set_xlabel('dal bordo verso il centro (mm)')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    f = os.path.join(QUI, 'tavola_sagome.png')
    fig.savefig(f, facecolor='white')
    print(f)


def geo_ccw(p):
    import geo
    return geo.ccw(p)


if __name__ == '__main__':
    main()
