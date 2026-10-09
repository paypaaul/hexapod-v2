"""Render della seconda passata sulle placche: Kabuto corretto (riferimento), Morbida, Piena.

Parte da sintesi/concept.py (testa, visiera, coda, colori) e sostituisce carapace, lame e ginocchiera con quelli di
varianti.py / guscio.py (raccordi in pianta, spalla raccordata, placche bombate con raccordo sul bordo).
Uso: python3 <versione>.py [viste...]  (le viste di default: iso_ant, iso_post, fianco, zampa, punta)
"""
import importlib.util
import math
import os
import sys

import numpy as np
from matplotlib.path import Path

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica')
import render as RD  # noqa: E402
from render import Scena, COXE, terna_zampa, _suddividi  # noqa: E402
import geo  # noqa: E402
import guscio  # noqa: E402
import varianti as VR  # noqa: E402

_spec = importlib.util.spec_from_file_location('sintesi_concept', '/Users/paul/.claude/jobs/3d86073b/tmp/estetica/sintesi/concept.py')
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
K = C.K

BIANCO, ANTRACITE, SERVO, NERO, FUGA, OMBRA = C.BIANCO, C.ANTRACITE, C.SERVO, C.NERO, C.FUGA, C.OMBRA
INOX, INOX_CHIARO, ARANCIO = C.INOX, C.INOX_CHIARO, C.ARANCIO
faccia, pareti, lastra, quad, aggiungi = K.faccia, K.pareti, K.lastra, K.quad, K.aggiungi
cerchio, rett, rientra, taglia, ccw = K.cerchio, K.rett, K.rientra, K.taglia, K.ccw
Z_BORDO, Z_SMUSSO, Z_TOP, SP, FASCIA = C.Z_BORDO, C.Z_SMUSSO, C.Z_TOP, C.SP, C.FASCIA
VISO_X, CODA_X = C.VISO_X, C.CODA_X


# ----------------------------------------------------------------------------- utilita' sui gruppi divisi
def _trasf(tri, m):
    t = tri.reshape(-1, 3)
    return (t @ m[:3, :3].T + m[:3, 3]).reshape(tri.shape)


def togli_sotto(s, prefisso, asse, val, contorno, fori=(), assi_uv=None):
    """Toglie dalle parti del gruppo i pezzi di faccia (piano asse = val, terna della zampa) coperti da una placca:
    suddivide i triangoli del piano e scarta quelli con i tre vertici dentro la sagoma (fuori dalle finestre)."""
    uv = assi_uv or [i for i in range(3) if i != asse]
    pe = Path(np.asarray(contorno))
    pf = [Path(np.asarray(f)) for f in fori]

    def dentro(q):
        m = pe.contains_points(q)
        for p in pf:
            m &= ~p.contains_points(q)
        return m
    for g in [g for g in s.gruppi if g.startswith(prefisso)]:
        T = s.gruppi[g]['tri']
        tieni = np.ones(len(T), bool)
        nuovi = []
        for n in COXE:
            M = terna_zampa(n)
            TL = _trasf(T, np.linalg.inv(M))
            m = (TL[:, :, 0].min(1) > 25) & (TL[:, :, 0].max(1) < 220) & (np.abs(TL[:, :, 1]).max(1) < 45)
            m &= tieni & (np.abs(TL[:, :, asse] - val).max(1) < 0.02)
            if not m.any():
                continue
            tieni &= ~m
            sub = _suddividi(TL[m], 1.2)
            q = sub[:, :, uv].reshape(-1, 2)
            dd = dentro(q).reshape(-1, 3).all(1)
            nuovi.append(_trasf(sub[~dd], M))
        s.gruppi[g]['tri'] = np.concatenate([T[tieni]] + nuovi)


def maschera(s, prefisso, cond):
    out = {}
    for g in [g for g in s.gruppi if g.startswith(prefisso)]:
        T = s.gruppi[g]['tri']
        m = np.zeros(len(T), bool)
        for n in COXE:
            TL = _trasf(T, np.linalg.inv(terna_zampa(n)))
            reg = (TL[:, :, 0].min(1) > 25) & (TL[:, :, 0].max(1) < 220) & (np.abs(TL[:, :, 1]).max(1) < 45)
            m |= reg & cond(TL)
        out[g] = T[m]
        s.gruppi[g]['tri'] = T[~m]
    return np.concatenate(list(out.values()))


# ----------------------------------------------------------------------------- carapace
def faccia_fine(esterno, buchi, z, passo=5.0):
    """Faccia piana triangolata a griglia (Delaunay): niente triangoli a ventaglio lunghi e sottili, che con
    l'ordinamento per profondita' di matplotlib fanno affiorare le parti sotto."""
    p = geo.Placca(esterno, buchi, t_c=0.0, Rb=0.0, q_c=0.0, asse_q=0, r_bordo=0.0, passo=passo)
    t = p.pts[p.tri]
    P = t
    ar = 0.5 * np.abs((P[:, 1, 0] - P[:, 0, 0]) * (P[:, 2, 1] - P[:, 0, 1]) - (P[:, 2, 0] - P[:, 0, 0]) * (P[:, 1, 1] - P[:, 0, 1]))
    lmax = np.max(np.linalg.norm(P - np.roll(P, 1, axis=1), axis=2), axis=1)
    t = t[ar >= 0.02 * lmax ** 2]
    return np.concatenate([t, np.full(t.shape[:2] + (1,), z)], axis=2)


def _spezza(cont):
    """Aggiunge i punti a |y| = FASCIA sui lati diritti di viso e coda (la fascia nera e' una striscia di colore)."""
    out = []
    n = len(cont)
    for i in range(n):
        a, b = cont[i], cont[(i + 1) % n]
        out.append(a)
        for xl in (VISO_X, -CODA_X):
            if abs(a[0] - xl) < 1e-6 and abs(b[0] - xl) < 1e-6:
                for yf in sorted((-FASCIA, FASCIA), key=lambda y: (y - a[1]) * (1 if b[1] > a[1] else -1)):
                    if min(a[1], b[1]) < yf < max(a[1], b[1]):
                        out.append((xl, yf))
    return out


def fai_carapace(s, car):
    cont = _spezza(ccw(guscio.contorno(car)))
    n = len(cont)
    prof = guscio.profilo(car)
    anelli = [rientra(cont, d) for d, _ in prof]
    zz = [z for _, z in prof]
    vivo = {0.0: cont, guscio.CH: rientra(cont, guscio.CH)}
    for i in range(n):
        j = (i + 1) % n
        a, b = cont[i], cont[j]
        viso = abs(a[0] - VISO_X) < 1e-6 and abs(b[0] - VISO_X) < 1e-6
        coda = abs(a[0] + CODA_X) < 1e-6 and abs(b[0] + CODA_X) < 1e-6
        nero = (viso or coda) and abs((a[1] + b[1]) / 2) < FASCIA
        if viso or coda:
            # viso e coda restano a spigolo vivo (li incontrano fascia e visiera nere, pezzi piani)
            for (d0, z0), (d1, z1) in (((0.0, Z_BORDO), (0.0, Z_SMUSSO)), ((0.0, Z_SMUSSO), (guscio.CH, Z_TOP))):
                if viso and z1 <= Z_SMUSSO:
                    continue                               # bordo del viso: e' la visiera (fai_testa)
                pa, pb = vivo[d0][i], vivo[d0][j]
                qa, qb = vivo[d1][i], vivo[d1][j]
                col = NERO if (nero and (coda or z0 >= Z_SMUSSO - 1e-6)) else BIANCO
                aggiungi(s, quad((*pa, z0), (*pb, z0), (*qb, z1), (*qa, z1)), col)
            continue
        for k in range(len(prof) - 1):
            pa, pb, qa, qb = anelli[k][i], anelli[k][j], anelli[k + 1][i], anelli[k + 1][j]
            col = NERO if (nero and (coda or zz[k] >= Z_SMUSSO - 1e-6)) else BIANCO
            aggiungi(s, quad((*pa, zz[k]), (*pb, zz[k]), (*qb, zz[k + 1]), (*qa, zz[k + 1])), col)
    q = anelli[-1]
    # (le facce interne del guscio non si vedono nelle viste dall'alto e sbagliano l'ordinamento per profondita')

    sx = taglia(q, (0, FASCIA), (1, FASCIA), sinistra=True)
    feritoie = [rett(18 + i * 7.295, 28.5, 24 + i * 7.295, 31.5) for i in range(5)]
    pozzi = [(40.0, 22.5), (-56.0, 22.5)]
    aggiungi(s, faccia_fine(sx, [cerchio(c, 3.5, 28) for c in pozzi] + feritoie, Z_TOP), BIANCO, specchia_y=True)
    for f in feritoie:
        aggiungi(s, pareti(f, Z_TOP - SP, Z_TOP), BIANCO, specchia_y=True)
        aggiungi(s, faccia(f, [], Z_TOP - SP), OMBRA, specchia_y=True)
    for c in pozzi:
        aggiungi(s, pareti(cerchio(c, 3.5, 28), 30.0, Z_TOP), BIANCO, specchia_y=True)
        aggiungi(s, faccia(cerchio(c, 3.5, 28), [cerchio(c, 2.75, 28)], 30.0), BIANCO, specchia_y=True)
        aggiungi(s, lastra(cerchio(c, 2.75, 28), [], 30.0, 33.4, sotto=False), INOX, specchia_y=True)
        aggiungi(s, faccia(cerchio(c, 1.3, 6), [], 33.41), OMBRA, specchia_y=True)

    fascia = taglia(taglia(q, (0, FASCIA), (1, FASCIA), sinistra=False), (0, -FASCIA), (1, -FASCIA), sinistra=True)
    ott = [(-14, -16), (22, -16), (28, -10), (28, 10), (22, 16), (-14, 16), (-20, 10), (-20, -10)]
    puls, fin, tacca = cerchio((-40, 0), 6.1, 36), rett(-81.5, -12, -67.5, 12), rett(29, -5, 32, 5)
    dietro = taglia(taglia(fascia, (-20, 0), (-20, 1), sinistra=True), (0, 0), (0, 1), sinistra=True)
    davanti = taglia(fascia, (28, 0), (28, 1), sinistra=False)
    mezzo = taglia(taglia(fascia, (-20, 0), (-20, 1), sinistra=False), (28, 0), (28, 1), sinistra=True)
    aggiungi(s, faccia_fine(dietro, [puls, fin], Z_TOP), NERO)
    aggiungi(s, faccia_fine(davanti, [tacca], Z_TOP), NERO)
    aggiungi(s, faccia_fine(mezzo, [ott], Z_TOP), NERO)
    porta = rientra(ccw(ott), 0.4)
    aggiungi(s, faccia(porta, [], Z_TOP), NERO)
    aggiungi(s, pareti(porta, Z_TOP - 0.6, Z_TOP), NERO)
    aggiungi(s, faccia(ott, [porta], Z_TOP - 0.6), FUGA)
    aggiungi(s, pareti(tacca, Z_TOP - 0.8, Z_TOP), NERO)
    aggiungi(s, faccia(tacca, [], Z_TOP - 0.8), OMBRA)
    aggiungi(s, pareti(fin, Z_TOP - SP, Z_TOP), NERO)
    aggiungi(s, faccia(fin, [], Z_TOP - SP - 0.01), C.DISPLAY)
    aggiungi(s, pareti(cerchio((-40, 0), 6.0, 36), 34.0, 36.6), INOX)
    aggiungi(s, faccia(cerchio((-40, 0), 6.0, 36), [cerchio((-40, 0), 4.2, 36)], 36.6), INOX)
    aggiungi(s, lastra(cerchio((-40, 0), 4.2, 36), [], 36.6, 36.9, sotto=False), INOX_CHIARO)
    for x0, x1 in ((22, 58.8), (-58.8, -22)):
        s.scatola(x0, 48.8, 7.0, x1, 50.0, Z_BORDO, NERO, specchia_y=True)
        s.scatola(x0, 48.8, Z_BORDO, x1, 50.0, Z_TOP - SP, BIANCO, specchia_y=True)


# ----------------------------------------------------------------------------- placche delle zampe
def _lama(p, y0, verso, fondo):
    t = p.triangoli(fondo=fondo)
    out = np.empty_like(t)
    out[:, :, 0] = t[:, :, 0]
    out[:, :, 1] = y0 + verso * t[:, :, 2]
    out[:, :, 2] = t[:, :, 1]
    return out


def _ginocchiera(p):
    t = p.triangoli(fondo=False)
    out = np.empty_like(t)
    out[:, :, 0] = VR.X_CULLA + t[:, :, 2]
    out[:, :, 1] = t[:, :, 0]
    out[:, :, 2] = t[:, :, 1]
    return out


def fai_zampe(s, v):
    kw = dict(zampe=True)
    togli_sotto(s, 'zampe_struttura', 1, VR.Y_FA, v.contorno, v.finestre, [0, 2])
    togli_sotto(s, 'zampe_struttura', 1, VR.Y_FB, v.contorno, v.finestre, [0, 2])
    togli_sotto(s, 'zampe_struttura_tibia', 0, VR.X_CULLA, v.gin_contorno, (), [1, 2])
    aggiungi(s, _lama(v.lama_A, v.y_in_A, 1, fondo=v.tubi), BIANCO, **kw)
    aggiungi(s, _lama(v.lama_B, v.y_in_B, -1, fondo=False), BIANCO, **kw)
    if v.tubi:
        for c in VR.VITI_BLOCCO:
            aggiungi(s, pareti(cerchio(c, VR.TUBO_R, 28), VR.Y_FA, v.y_in_A, 'y'), BIANCO, **kw)
        for c in ((VR.XH + 15.2, 0.0), (VR.XK - 15.2, 0.0)):
            aggiungi(s, pareti(cerchio(c, 1.5, 16), VR.Y_FA, v.y_in_A, 'y'), BIANCO, **kw)
    # teste M3 sul lato A: 8 delle squadrette (nelle finestre) e 4 del blocco (nei fori della lama)
    teste = [(xc + dx, dz) for xc in (VR.XH, VR.XK) for dx, dz in ((-7, 0), (7, 0), (0, 7), (0, -7))] + VR.VITI_BLOCCO
    for c in teste:
        es = cerchio(c, 1.45, 6, math.pi / 6)
        aggiungi(s, faccia(cerchio(c, 2.75, 28), [es], VR.Y_TESTE, 'y'), INOX, **kw)
        aggiungi(s, pareti(cerchio(c, 2.75, 28), VR.Y_FA, VR.Y_TESTE, 'y'), INOX, **kw)
        aggiungi(s, pareti(es, VR.Y_TESTE - 1.2, VR.Y_TESTE, 'y'), OMBRA, **kw)
        aggiungi(s, faccia(es, [], VR.Y_TESTE - 1.2, 'y'), OMBRA, **kw)
    aggiungi(s, maschera(s, 'zampe_servo', lambda TL: TL[:, :, 1].max(1) < -30.5), INOX)
    aggiungi(s, maschera(s, 'zampe_struttura_tibia', lambda TL: TL[:, :, 2].max(1) <= -94.9), ARANCIO)
    # ginocchiera e labbro sulla cima della culla
    aggiungi(s, _ginocchiera(v.gin), BIANCO, **kw)
    s.scatola(130.65, -24.15, 12.45, VR.X_CULLA + 1.2, 9.45, 13.65, BIANCO, **kw)


# ----------------------------------------------------------------------------- scena e viste
VISTE_DEF = ('iso_ant', 'iso_post', 'fianco', 'zampa', 'punta')
EXTRA = {'zampa': ((18, 60, 3.0), (150, 85, -20)), 'punta': ((8, 22, 3.6), (150, 86, -8)),
         'lato_b': ((14, 120, 3.4), (150, 86, -8))}
RD.VISTE.update({k: v[0] for k, v in EXTRA.items()})


def costruisci(v):
    s = Scena()
    s.nascondi('coperchio')
    s.colore('base', ANTRACITE)
    s.colore('zampe_struttura', ANTRACITE)
    s.colore('servo_coxa', SERVO)
    s.colore('interni', '#33363b')
    s.colore('zampe_servo', SERVO)
    fai_carapace(s, v.car)
    C.fai_testa(s)
    C.fai_coda(s)
    fai_zampe(s, v)
    return s


def main(fabbrica, base, titolo):
    v = fabbrica(passo=1.3)
    s = costruisci(v)
    viste = sys.argv[1:] or list(VISTE_DEF)
    fatti = []
    for vv in viste:
        if vv in EXTRA:
            fatti += s.render(base, viste=(vv,), centro=EXTRA[vv][1], titolo=titolo, lato=5.0)
        else:
            fatti += s.render(base, viste=(vv,), titolo=titolo, lato=5.0)
    for f in fatti:
        print(f)
