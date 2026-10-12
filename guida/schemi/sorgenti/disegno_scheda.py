import math, os, ast
import scheda_def as d
from modello import LET, h, punti_con_corsie
from svgbase import Svg, CLASSI, legenda
from disegno import classe, stile, tratteggio_zona, etichette_fili, OUT

S, GS = d.S, d.GS
SS = 3.0
SX, SY = 12.0, 22.0
NOMI = {'5v': '+5 V (poli 1 e 2)', '3v3': '+3,3 V (polo 7)', 'gnd': 'Massa', 'i2c': 'SDA e SCL', 'sig5': 'Dato dei LED a 5 V',
        'sig3': 'I2S (BCLK, WS, MIC, AMP)', 'btn': 'Pulsante (A e B della 2813)'}


def ts(x, y, spec):
    return SX + SS * (x - d.SCH['x0']), SY + SS * ((d.SCH['y1'] - y) if spec else (y - d.SCH['y0']))


def fxy(f, spec):
    return ts(*GS.xy(f), spec)


def contorno(svg, spec):
    X0, Y0 = ts(d.SCH['x0'], d.SCH['y0'], spec); X1, Y1 = ts(d.SCH['x1'], d.SCH['y1'], spec)
    svg.rect(min(X0, X1), min(Y0, Y1), abs(X1 - X0), abs(Y1 - Y0), fill='#f3efe2', col='#000', sw=0.5)


def viti(svg, spec):
    for vx, vy in d.VITI:
        X, Y = ts(vx, vy, spec)
        if spec:
            tratteggio_zona(svg, X, Y, (d.R_BUGNA + 0.6) * SS, col='#495057')
            svg.circle(X, Y, d.R_BUGNA * SS, fill='#fff', col='#000', sw=0.4)
        svg.circle(X, Y, 1.3 * SS, fill='#fff', col='#000', sw=0.4)
        if not spec:
            svg.circle(X, Y, 1.9 * SS, col='#000', sw=0.3, dash='0.8 0.6')


def fori(svg, spec):
    for f in GS.fori():
        X, Y = fxy(f, spec)
        if f in S.pin:
            rete = S.pin[f][2]
            col = CLASSI[classe(rete)]['col'] if rete else '#adb5bd'
            svg.circle(X, Y, 2.3, fill='#e8d9a8', col=col, sw=0.7)
            svg.circle(X, Y, 0.8, fill='#fff', col='#7a6a3a', sw=0.2)
        else:
            svg.circle(X, Y, 2.0, fill='#efe6c8', col='#c8b88a', sw=0.25)
            svg.circle(X, Y, 0.7, fill='#fff', col='#c8b88a', sw=0.15)
        if f in S.vietati:
            svg.line(X - 1.6, Y - 1.6, X + 1.6, Y + 1.6, col='#868e96', w=0.4)
            svg.line(X - 1.6, Y + 1.6, X + 1.6, Y - 1.6, col='#868e96', w=0.4)


def assi(svg, spec):
    yt, yb = ts(0, d.SCH['y0'] if spec else d.SCH['y1'], spec)[1], ts(0, d.SCH['y1'] if spec else d.SCH['y0'], spec)[1]
    top, bot = min(yt, yb), max(yt, yb)
    for c in range(7):
        X, _ = fxy(LET[c] + '1', spec)
        dt, db_ = (4.6, 7.2) if spec else (1.8, 4.4)
        svg.text(X, top - dt, LET[c], size=3.0, weight=700); svg.text(X, bot + db_, LET[c], size=3.0, weight=700)
    for r in range(1, 12):
        _, Y = fxy('A%d' % r, spec)
        svg.text(SX - 3.2, Y + 1.1, str(r), size=3.0, weight=700); svg.text(SX + 60 + 3.4, Y + 1.1, str(r), size=3.0, weight=700)


def componenti():
    svg = Svg(190, 124)
    svg.text(4, 6.5, 'Scheda del carapace (X2) — lato componenti', size=4.4, anchor='start', weight=800)
    svg.text(4, 11, 'Scala 3:1. Vista da sotto, come pende dal dorso: ottagono (coda) a sinistra, testa a destra, '
             'sinistra del robot (+Y) in basso.', size=2.6, anchor='start', weight=500)
    svg.text(4, 15, 'BLOCCANTE (S-01): con la testata dritta e la spina servono 16–18 mm sotto la scheda, ne restano circa 10. '
             'Collegamenti validi, posto da rifare nel CAD.', size=2.6, anchor='start', weight=700, fill='#c92a2a')
    contorno(svg, False)
    viti(svg, False)
    fori(svg, False)
    # testata 2 x 8: tacca dal lato dei poli dispari (colonna D), come la sporgenza della spina Wurth 61201623021
    Xa, Ya = ts(36.35, -12.7, False); Xb, Yb = ts(45.19, 15.24, False)
    svg.rect(Xa, min(Ya, Yb), Xb - Xa, abs(Yb - Ya), fill='#495057', col='#000', sw=0.5, op=0.18)
    Xk, Yk = ts(36.35, 1.27, False)
    svg.rect(Xk - 1.2, Yk - 6.0, 1.6, 12.0, fill='#fff', col='#000', sw=0.4)
    svg.text(Xk + 2.2, Yk, 'tacca', size=2.6, weight=800, rot=-90, halo=True)
    for polo, f in d.TESTATA.items():
        X, Y = fxy(f, False)
        dx = -4.0 if polo % 2 else 4.0
        svg.text(X + dx, Y + 1.0, str(polo), size=2.8, weight=800, anchor='end' if polo % 2 else 'start', halo=True)
    X1, Y1 = fxy('D2', False)
    svg.path('M %.2f %.2f l -1.6 -2.6 l 3.2 0 z' % (X1, Y1 - 2.6), fill='#000')
    x0, y0, x1, y1 = d.CE1_BOX
    Xa, Ya = ts(x0, y0, False); Xb, Yb = ts(x1, y1, False)
    svg.rect(Xa, min(Ya, Yb), Xb - Xa, abs(Yb - Ya), fill='#d3f9d8', col='#000', sw=0.45, rx=2.5, op=0.8)
    cx, cy = (Xa + Xb) / 2, (Ya + Yb) / 2
    svg.text(cx + 1.0, cy, 'CE1 470 µF 10 V', size=2.6, weight=800, rot=-90, halo=True)
    svg.text(cx - 2.4, cy, 'sdraiato, Ø ≤ 6,3', size=2.5, weight=500, rot=-90, halo=True)
    for f, sgn in (('A9', '+'), ('B9', '−')):
        X, Y = fxy(f, False); svg.text(X, Y + 5.6, sgn, size=3.4, weight=800)
    for f, (r, t, n) in d.MOD.items():
        X, Y = fxy(f, False)
        if f.startswith('G'):
            svg.line(X + 2.3, Y, SX + 60 + 6.2, Y, col='#868e96', w=0.25)
            svg.text(SX + 60 + 7, Y + 1.0, '%s  %s' % (h(f), t), size=2.5, anchor='start', weight=600)
    y = legenda(svg, 134, 22, ['5v', '3v3', 'gnd', 'i2c', 'sig5', 'sig3', 'btn'], titolo='Reti', nomi=NOMI)
    y += 1
    svg.text(134, y, 'Piazzole dei moduli (lato ottagono e sotto)', size=3.0, anchor='start', weight=800); y += 3.5
    for f in ('A3', 'B3', 'A4', 'B4', 'A9', 'B9'):
        svg.text(134, y, h(f), size=2.5, anchor='start', weight=800)
        svg.text(141.5, y, d.MOD[f][1], size=2.5, anchor='start', weight=600); y += 2.9
    for f, (r, t, awg) in d.DIRETTI.items():
        svg.text(134, y, h(f), size=2.5, anchor='start', weight=800)
        svg.text(141.5, y, t + ' (sul pin)', size=2.5, anchor='start', weight=600); y += 2.9
    y += 1
    svg.text(134, y, 'Poli della testata', size=3.0, anchor='start', weight=800); y += 3.4
    for polo in range(1, 17, 2):
        svg.text(134, y, '%d %s' % (polo, d.NOMI_POLI[polo]), size=2.5, anchor='start', weight=600)
        svg.text(158, y, '%d %s' % (polo + 1, d.NOMI_POLI[polo + 1]), size=2.5, anchor='start', weight=600); y += 2.8
    yy = 104
    for t in ('Grigio: testata 2 × 8 con chiave (BOM X2).', '×: sopra la bugna Ø 5,5: vuoto.',
              'Triangolo: polo 1 (filo rosso).', 'R8 100 kΩ sta al microfono, nel fascio.'):
        svg.text(80, yy, t, size=2.6, anchor='start', weight=600); yy += 3.0
    assi(svg, False)
    svg.text(4, 122.4, 'Fori delle viti: Ø 2,6 sul foro d’angolo della griglia, spostato di 0,23 mm dal CAD (o trapanati sulle quote misurate).',
             size=2.6, anchor='start', weight=600)
    svg.write(os.path.join(OUT, 'scheda_carapace.svg'), 'Scheda del carapace, lato componenti')


def saldature():
    R, falliti = d.instrada_ordine(ast.literal_eval(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ordine_s.txt')).read()))
    assert not falliti
    svg = Svg(190, 124)
    svg.text(4, 7.5, 'Scheda del carapace — LATO SALDATURE (specchiata)', size=5.0, anchor='start', weight=800)
    svg.text(4, 12, 'Scala 3:1. Vista da sopra (il lato che guarda il dorso): ottagono a sinistra, +Y in alto. '
             'Millefori a doppia faccia, nessuna striscia da tagliare.', size=2.6, anchor='start', weight=500)
    contorno(svg, True)
    viti(svg, True)
    fori(svg, True)
    for a, b, rete in S.ponti:
        (x1, y1), (x2, y2) = fxy(a, True), fxy(b, True)
        svg.line(x1, y1, x2, y2, col='#adb5bd', w=3.2)
        stile(svg, [(x1, y1), (x2, y2)], rete, 0.3)
    for i, f in enumerate(S.fili):
        mid = punti_con_corsie(R, i, f['perc'], lambda n: ts(*GS.cxy(*n), True), passo=1.2)
        if f.get('diretto'):
            xe = SX - 3.0
            f['pts'] = [fxy(f['a'], True)] + mid + [(xe, mid[-1][1])]
            stile(svg, f['pts'], f['rete'], 0.3 if f['awg'] == 30 else 0.6)
            svg.path('M %.2f %.2f l 1.4 -0.8 l 0 1.6 z' % (xe - 1.2, mid[-1][1]), fill=CLASSI[classe(f['rete'])]['col'], col='none')
            continue
        f['pts'] = [fxy(f['a'], True)] + mid + [fxy(f['b'], True)]
        stile(svg, f['pts'], f['rete'], 0.3 if f['awg'] == 30 else 0.6)
    poli_xy = []
    for polo, f in d.TESTATA.items():
        X, Y = fxy(f, True)
        poli_xy.append((X + (-3.9 if polo % 2 else 3.9), Y))
    pad_xy = [fxy(f, True) for f in S.pin]
    etichette_fili(svg, [f for f in S.fili if not f.get('diretto')], None, pad_xy, 100, size=3.0, evita=poli_xy)
    for polo, f in d.TESTATA.items():
        X, Y = fxy(f, True)
        svg.text(X + (-3.9 if polo % 2 else 3.9), Y + 1.0, str(polo), size=2.6, weight=800,
                 anchor='end' if polo % 2 else 'start', halo=True)
    assi(svg, True)
    y = legenda(svg, 112, 22, ['5v', '3v3', 'gnd', 'i2c', 'sig5', 'sig3', 'btn'], titolo='Fili (stile per rete)', nomi=NOMI)
    y += 1
    svg.line(113, y - 1.0, 121, y - 1.0, col='#adb5bd', w=3.0)
    svg.text(122.5, y, 'ponticello di stagno o filo nudo', size=2.6, anchor='start', weight=500); y += 4.2
    tratteggio_zona(svg, 117, y - 1.2, 2.4, col='#495057')
    svg.text(122.5, y - 1.0, 'bugna Ø 5,5: la scheda appoggia qui,', size=2.6, anchor='start', weight=500)
    svg.text(122.5, y + 2.0, 'niente saldature né fili', size=2.6, anchor='start', weight=500); y += 7.0
    svg.text(112, y, 'Fili isolati (numeri da 101 in schemi.md)', size=3.0, anchor='start', weight=800); y += 3.6
    for i, f in enumerate([f for f in S.fili if not f.get('diretto')], 101):
        svg.text(112, y, '%d  %s → %s  %s, %d AWG' % (i, h(f['a']), h(f['b']), f['rete'], f['awg']), size=2.5,
                 anchor='start', weight=600)
        y += 2.85
    y += 1.5
    svg.text(112, y, 'Fili dei moduli saldati qui, sul pin:', size=2.8, anchor='start', weight=800); y += 3.2
    for f, (r, t, awg) in d.DIRETTI.items():
        svg.text(112, y, '%s (polo %s)  %s, %d AWG' % (h(f), d.S.pin[f][1], t, awg), size=2.5, anchor='start', weight=600); y += 2.85
    svg.text(4, 122.4, 'I fili dei moduli entrano dal lato componenti e si saldano qui (DIN e pulsante sul pin della testata), prima di avvitare '
             'la scheda (13.16). Sotto il dorso: 3,5 mm.', size=2.6, anchor='start', weight=700, fill='#c92a2a')
    svg.write(os.path.join(OUT, 'scheda_carapace_saldature.svg'), 'Scheda del carapace, lato saldature')
    return R


if __name__ == '__main__':
    R = saldature()
    print('incroci', len(R.incroci()), 'paralleli', len(R.paralleli()))
    componenti()
