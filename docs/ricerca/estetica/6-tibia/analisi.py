#!/usr/bin/env python3
"""Conti delle varianti della tibia: volumi e masse, sezioni e sforzi, rigidezza, ingombri al ginocchio minimo e a 180,
appoggio negli assetti di marcia. Terna della zampa, mm, N.

Uso: python3 analisi.py [strutt] [masse] [escursioni] [appoggio]   (senza argomenti: tutto)
"""
import math
import sys

import numpy as np

sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica/v2_tibia')
sys.path.insert(0, '/Users/paul/hexapod-v2/calc')
from varianti import VARIANTI, Z0, ZP, Y_ORLO  # noqa: E402
import stinco as S  # noqa: E402

LT = 110.0
# ---------------------------------------------------------------- materiali (stimati, da schede tipiche: da confermare)
E_CF = 3500.0          # MPa, PETG-CF nel piano degli strati (schede tipiche 3,0..4,5 GPa)
R_CF = 40.0            # MPa, resistenza a trazione nel piano degli strati (schede tipiche 35..55)
RHO_EFF = 28.3 / 25.087      # g/cm3: massa / volume della tibia di oggi (progetto-meccanico.md: 25,1 cm3 -> 28,3 g)
RHO_TPU = 1.21         # g/cm3, TPU 95A pieno (schede tipiche 1,20..1,23)

# ---------------------------------------------------------------- carichi sul piede
STALLO = 11.0 * 9.80665 * 10       # N mm (11 kgf cm a 6 V, calc/statica_tripode.py)
T_STAT = 475.0                     # N mm: coppia massima del ginocchio al punto di progetto (statica_tripode.py)
F_PIEDE = 1089 * 9.80665 / 1000    # N: carico massimo su un piede (40 % del peso, statica_tripode.py)
T_CAD = 2 * STALLO                 # N mm: in caduta il servo cede (ritorno degli ingranaggi) a circa 2 volte lo stallo (stimato)
XF = 45.0                          # mm: distanza orizzontale piede - asse del femore al punto di progetto
F_CAD_V = T_CAD / XF               # N: carico lungo lo stinco in caduta, limitato dal servo del femore che cede
MU = 0.8                           # attrito TPU - pavimento (stimato)
CASI = {
    'statica (punto di progetto)': dict(T=T_STAT, Fy=0.0, N=F_PIEDE),
    'stallo del ginocchio (11 kgf cm)': dict(T=STALLO, Fy=0.0, N=F_PIEDE),
    'caduta: nel piano (2 x stallo)': dict(T=T_CAD, Fy=0.0, N=F_CAD_V),
    'caduta: di fianco (attrito 0,8)': dict(T=0.0, Fy=MU * F_CAD_V, N=F_CAD_V),
}


def struttura(nome, stampa=True):
    v = VARIANTI[nome]
    sez = [s for s in S.sezioni(nome, 0.25) if s['z'] > v['zc']]
    out = {}
    for caso, c in CASI.items():
        Fp = c['T'] / LT
        peggio = (0, None)
        for s in sez:
            a = s['z'] + LT                      # braccio dalla punta del piede
            sig = Fp * a * s['cx'] / s['Iy'] + c['Fy'] * a * s['cy'] / s['Ix'] + c['N'] / s['A']
            if sig > peggio[0]:
                peggio = (sig, s)
        out[caso] = peggio
    # rigidezza: freccia della punta per 1 N perpendicolare allo stinco (nel piano) e 1 N di fianco, zoccolo rigido
    dz = 0.25
    f_in = sum((s['z'] + LT) ** 2 / (E_CF * s['Iy']) * dz for s in sez)
    f_out = sum((s['z'] + LT) ** 2 / (E_CF * s['Ix']) * dz for s in sez)
    rad = sez[0]
    if stampa:
        print('%s: sotto lo zoccolo %.1f x %.1f (X x Y), alla punta %.1f x %.1f, rotaia minima %.2f, A radice %.0f mm2'
              % (v['titolo'], rad['wx'], rad['wy'], 2 * v['r'], Y_ORLO - v['ym'](v['zc']), min(s['rotaia'] for s in sez), rad['A']))
        for caso, (sig, s) in out.items():
            a = s['z'] + LT
            print('   %-34s sforzo massimo %5.1f MPa a z %6.1f (braccio %4.1f, sezione %.1f x %.1f%s), coeff. %.0f'
                  % (caso, sig, s['z'], a, s['wx'], s['wy'], ', finestra' if s['rotaia'] < s['wx'] - 0.01 else '', R_CF / sig))
        print('   freccia della punta per 1 N: nel piano %.4f mm, di fianco %.4f mm; al punto di progetto (%.1f N) %.3f mm'
              % (f_in, f_out, T_STAT / LT, f_in * T_STAT / LT))
    return out, f_in, f_out


def cappuccio(nome):
    """Volume del piedino (guscio: parete sui fianchi e suola sulla punta) e del nucleo della struttura che ci entra."""
    v = VARIANTI[nome]
    p = v['piedino']
    if p['parete'] == 0:
        # base: cappuccio sopra la punta di oggi (non disegnato): parete 1,2 sui fianchi per 15 mm e suola 2
        L, wx, wy = 15.0, 12.0, 18.9
        vol = (2 * (wx + 2.4) * 1.2 + 2 * wy * 1.2) * L + (math.pi * (6 + 2) ** 2 / 2 - math.pi * 36 / 2) * (wy + 2.4)
        return vol, 0.0
    zs = np.arange(p['z'], v['zc'] - v['r'], -0.05)
    est = nuc = 0.0
    for z in zs:
        xl, xr = S.semilarghezze(v, z)
        y0 = v['ym'](max(z, v['zc'] - v['r']))
        est += (xr - xl) * (Y_ORLO - y0) * 0.05
        # nucleo: fianchi rientrati della parete, punta rialzata della suola
        zz = z - p['suola'] * max(0.0, 1 - (z - (v['zc'] - v['r'])) / v['r'])
        if zz < v['zc'] - v['r'] + p['suola']:
            continue
        xl2, xr2 = S.semilarghezze(v, z + p['suola'] * 0) if z >= v['zc'] else S.semilarghezze(v, z)
        w = max(0.0, (xr2 - xl2) - 2 * p['parete'])
        if z < v['zc']:
            # sotto il centro dell'arco: nucleo = arco di raggio r - parete, alzato della suola meno la parete
            rc = v['r'] - p['parete']
            zc2 = v['zc'] + (p['suola'] - p['parete'])
            w = 2 * math.sqrt(max(rc * rc - (z - zc2) ** 2, 0.0)) if z < zc2 else w
        nuc += w * max(0.0, Y_ORLO - y0 - 2 * p['parete']) * 0.05
    return est - nuc, nuc


def masse(stampa=True):
    vb = S.volume('base')
    cb, _ = cappuccio('base')
    out = {}
    for n in VARIANTI:
        V = S.volume(n)
        cap, nuc = cappuccio(n)
        if VARIANTI[n]['piedino']['parete'] == 0:
            strutt = V
        else:
            strutt = V - cap
        dm = (strutt - vb) * RHO_EFF / 1000 + (cap - cb) * RHO_TPU / 1000
        out[n] = dict(V=V, strutt=strutt, cap=cap, dm=dm)
        if stampa:
            print('%-26s sagoma sotto lo zoccolo %.2f cm3, struttura %.2f cm3 (%.1f g), piedino %.2f cm3 (%.1f g TPU); '
                  'differenza da oggi (stinco + piedino) %+.1f g per tibia, %+.0f g sul robot'
                  % (VARIANTI[n]['titolo'], V / 1000, strutt / 1000, strutt * RHO_EFF / 1000, cap / 1000, cap * RHO_TPU / 1000,
                     dm, 6 * dm))
    return out


# ---------------------------------------------------------------- escursioni
def escursioni(nomi=None, stampa=True):
    import geom as G
    from geom import GMIN, posa_tibia, campiona
    gam = G.gamba()
    O = G.Ostacoli(gam)
    base_stl = campiona(gam['tibia'][gam['tibia'][:, :, 2].max(1) <= Z0 + 0.01], 0.4)
    nuvole = {'oggi (STL)': base_stl}
    for n in (nomi or VARIANTI):
        a, b = S.mesh(n)
        nuvole[n] = campiona(np.concatenate([a, b]), 0.4)
    ris = {}
    for n, P in nuvole.items():
        righe = []
        for al, g in GMIN.items():
            d, i, parte = O.distanza(posa_tibia(P, al, g), al, (-35, 0, 35))
            # gamma minimo della variante con lo stesso criterio (prima posa con gioco >= quello di oggi meno 0,1): scansione
            righe.append((al, g, d, parte, P[i] if i >= 0 else None))
        # ginocchio a 180 con il femore a 0 e a +85, -49
        d180 = min(O.distanza(posa_tibia(P, al, 180.0), al)[0] for al in (-49, 0, 85))
        ris[n] = (righe, d180)
    if stampa:
        print('Gioco dello stinco (mm) al gamma minimo della tabella, femore da -45 a +85 (coxa, femore, corpo a imbardata -35/0/+35):')
        print('  alfa gmin ' + ' '.join('%12s' % k[:12] for k in ris))
        for k in range(len(GMIN)):
            al, g = list(GMIN.items())[k]
            print('  %+4d %4d ' % (al, g) + ' '.join('%7.2f %-4s' % (ris[n][0][k][2], ris[n][0][k][3][:4]) for n in ris))
        print('  ginocchio a 180 (femore -49, 0, +85): ' + ', '.join('%s %.2f' % (n, ris[n][1]) for n in ris))
    return ris, O, nuvole


def gamma_min(O, P, al, g0, d_rif):
    """Gamma minimo con lo stesso gioco di riferimento: scende da g0 + 15 finche' il gioco resta >= d_rif."""
    from geom import posa_tibia
    g = g0 + 15.0
    while g > 15:
        d = O.distanza(posa_tibia(P, al, g - 0.5), al, (-35, 0, 35))[0]
        if d < d_rif:
            return g
        g -= 0.5
    return g


# ---------------------------------------------------------------- appoggio
def appoggio(stampa=True):
    import statica_tripode as st
    import andature as an
    out = []
    for h, xf in ((130, 25), (115, 35), (100, 45), (90, 50), (80, 60), (70, 70)):
        r = st.ik_piano(xf, h, 65.0, LT)
        out.append((h, xf, r))
    if stampa:
        for h, xf, r in out:
            print('assetto %d/%d: ik %s' % (h, xf, r))
    return out


if __name__ == '__main__':
    cosa = sys.argv[1:] or ['strutt', 'masse', 'escursioni', 'appoggio']
    if 'strutt' in cosa:
        print('Carichi: piede %.1f N, ginocchio %.0f N mm (statica), stallo %.0f N mm, caduta %.0f N mm e %.0f N lungo lo stinco, '
              'di fianco %.0f N' % (F_PIEDE, T_STAT, STALLO, T_CAD, F_CAD_V, MU * F_CAD_V))
        for n in VARIANTI:
            struttura(n)
    if 'masse' in cosa:
        masse()
    if 'escursioni' in cosa:
        escursioni()
    if 'appoggio' in cosa:
        appoggio()
