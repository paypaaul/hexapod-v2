import math, os
import basetta_def as d
import fili_b
from modello import LET, h, controlli_vicinanze
from svgbase import Svg, CLASSI, legenda
from disegno import classe, stile, tratteggio_zona, etichette_fili, OUT

B, GB = d.B, d.GB
S = 2.0
BX = 12.0
BY = 30.0


def tb(x, y, spec):
    return BX + S * (x - d.BAS['x0']), BY + S * ((y - d.BAS['y0']) if spec else (d.BAS['y1'] - y))


def fxy(f, spec):
    return tb(*GB.xy(f), spec)


def nxy(n, spec):
    return tb(*GB.cxy(*n), spec)


def assi(svg, spec, by):
    for c in range(21):
        X, _ = fxy(LET[c] + '1', spec)
        svg.text(X, by - 1.6, LET[c], size=2.8, weight=700)
        svg.text(X, by + 70 + 4.2, LET[c], size=2.8, weight=700)
    for r in range(1, 14):
        _, Y = fxy('A%d' % r, spec)
        svg.text(BX - 3.0, Y + 1.0, str(r), size=2.8, weight=700)
        svg.text(BX + 112 + 3.2, Y + 1.0, str(r), size=2.8, weight=700)


def croce(svg, X, Y, r=1.1, col='#868e96'):
    svg.line(X - r, Y - r, X + r, Y + r, col=col, w=0.35)
    svg.line(X - r, Y + r, X + r, Y - r, col=col, w=0.35)


def fori(svg, spec):
    for f in GB.fori():
        X, Y = fxy(f, spec)
        if f in B.pin and f not in B.nosald:
            rete = B.pin[f][2]
            col = CLASSI[classe(rete)]['col'] if rete else '#adb5bd'
            svg.circle(X, Y, 1.55, fill='#e8d9a8', col=col, sw=0.55)
            svg.circle(X, Y, 0.55, fill='#fff', col='#7a6a3a', sw=0.2)
        elif f in B.nosald:
            svg.circle(X, Y, 1.35, fill='#efe6c8', col='#adb5bd', sw=0.3)
            svg.circle(X, Y, 0.5, fill='#adb5bd', col='#868e96', sw=0.15)
        else:
            svg.circle(X, Y, 1.35, fill='#efe6c8', col='#c8b88a', sw=0.25)
            svg.circle(X, Y, 0.5, fill='#fff', col='#c8b88a', sw=0.15)
        if f in B.vietati:
            croce(svg, X, Y, 1.2, '#c92a2a' if f in B.pin else '#868e96')


def contorno(svg, spec):
    X0, Y0 = tb(d.BAS['x0'], d.BAS['y1'], spec); X1, Y1 = tb(d.BAS['x1'], d.BAS['y0'], spec)
    svg.rect(min(X0, X1), min(Y0, Y1), abs(X1 - X0), abs(Y1 - Y0), fill='#f3efe2', col='#000', sw=0.5)


def zone_saldature(svg):
    for x, y in d.TESTE_M3:
        X, Y = tb(x, y, True)
        tratteggio_zona(svg, X, Y, 3.0 * S, col='#c92a2a')
        svg.circle(X, Y, d.R_TESTA * S, col='#c92a2a', sw=0.4, dash='1 0.6')
        svg.text(X, Y + 0.9, 'M3', size=2.6, weight=800, fill='#c92a2a', halo=True)
    for x, y in d.COLONNINE:
        X, Y = tb(x, y, True)
        tratteggio_zona(svg, X, Y, 3.5 * S, col='#495057')
        svg.circle(X, Y, d.R_COL * S, fill='#fff', col='#000', sw=0.4)
        svg.circle(X, Y, 1.1 * S, fill='#fff', col='#000', sw=0.4)
        svg.line(X - 1.0, Y, X + 1.0, Y, w=0.3); svg.line(X, Y - 1.0, X, Y + 1.0, w=0.3)


def percorso_pts(f, R, idx, spec=True):
    from modello import punti_con_corsie
    p = f['perc']
    mid = punti_con_corsie(R, idx, p, lambda n: nxy(n, spec), passo=0.8)
    return [fxy(f['a'], spec)] + mid + [fxy(f['b'], spec)]


def saldature():
    global BY
    BY = 21.0
    import ast
    R, falliti = fili_b.instrada_ordine(ast.literal_eval(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ordine_b.txt')).read()))
    if falliti: print('FALLITI', [(i+1, B.fili[i]['a'], B.fili[i]['b']) for i in falliti])
    svg = Svg(190, 132)
    svg.text(4, 7.5, 'Basetta — LATO SALDATURE (specchiata)', size=5.2, anchor='start', weight=800)
    svg.text(4, 12, 'Scala 2:1. La basetta girata attorno al lato lungo: riga 1 in basso, riga 13 in alto; colonne A–U '
             'sempre da sinistra (coda) a destra (testa).', size=2.6, anchor='start', weight=500)
    contorno(svg, True)
    zone_saldature(svg)
    fori(svg, True)
    for a, b, rete in B.ponti:
        (x1, y1), (x2, y2) = fxy(a, True), fxy(b, True)
        svg.line(x1, y1, x2, y2, col='#adb5bd', w=2.2)
        stile(svg, [(x1, y1), (x2, y2)], rete)
    # VBAT: lungo il bordo sinistro, dal bordo di coda, giu' fra le colonne O e P fino a P-4
    yv = tb(0, 16.95, True)[1]
    xo = nxy((14, 0), True)[0]
    pts = [(BX - 6, yv), (xo, yv)] + [nxy(n, True) for n in [(14, 1), (14, 2), (14, 3)]] + [fxy('P4', True)]
    stile(svg, pts, 'VBAT', 0.3)
    svg.text(BX - 6.5, yv - 1.6, 'VBAT', size=2.6, weight=800, anchor='start', fill='#b00020', halo=True)
    for idx, f in enumerate(B.fili):
        if f['perc'] is None:
            f['pts'] = [fxy(f['a'], True), fxy(f['b'], True)]
            svg.line(*f['pts'][0], *f['pts'][1], col='#ff00ff', w=0.4, dash='1 1')
            continue
        f['pts'] = percorso_pts(f, R, idx)
        stile(svg, f['pts'], f['rete'], 0.15 if f['awg'] == 26 else 0)
    for rif, val, a, b, n1, n2 in d.SMD:
        (x1, y1), (x2, y2) = fxy(a, True), fxy(b, True)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if abs(x1 - x2) < 0.1:
            svg.rect(mx - 1.3, my - 2.0, 2.6, 4.0, fill='#c5a46e', col='#000', sw=0.35)
            svg.text(mx + 2.0, my + 1.0, rif, size=2.6, weight=800, anchor='start', halo=True)
        else:
            svg.rect(mx - 2.0, my - 1.3, 4.0, 2.6, fill='#c5a46e', col='#000', sw=0.35)
            svg.text(mx, my - 2.0, rif, size=2.6, weight=800, halo=True)
    pad_xy = [fxy(f, True) for f in B.pin if f not in B.nosald]
    evita = []
    for rif, val, a, b, n1, n2 in d.SMD:
        (x1, y1), (x2, y2) = fxy(a, True), fxy(b, True)
        evita += [((x1 + x2) / 2, (y1 + y2) / 2), ((x1 + x2) / 2 + 3, (y1 + y2) / 2)]
    etichette_fili(svg, B.fili, None, pad_xy, 0, evita=evita)
    for t, f in (('U2', 'P8'), ('U3', 'H10'), ('U4', 'H6')):
        X, Y = fxy(f, True)
        svg.text(X, Y + 1.0, t, size=3.4, weight=800, fill='#868e96', halo=True)
    assi(svg, True, BY)
    # legenda
    y = legenda(svg, 131, 18, ['vbat', '5v', '3v3', 'gnd', 'i2c', 'sig5', 'sig3', 'cmd'], titolo='Fili (stile per rete)')
    y += 0.4
    svg.line(132, y - 1.0, 140, y - 1.0, col='#adb5bd', w=2.2)
    svg.text(141.5, y, 'ponticello di stagno o filo nudo', size=2.6, anchor='start', weight=500); y += 3.4
    svg.add(f'<rect x="133.5" y="{y - 3.0:.2f}" width="5" height="3.3" rx="1.2" fill="#fff" stroke="#000" stroke-width="0.35"/>')
    svg.text(136, y - 0.4, '12', size=2.9, weight=800)
    svg.text(141.5, y, 'filo isolato n. 12 (tratto spesso: 26 AWG)', size=2.6, anchor='start', weight=500); y += 3.6
    svg.rect(132.5, y - 2.4, 4, 2.6, fill='#c5a46e', col='#000', sw=0.35)
    svg.text(141.5, y, 'condensatore SMD 100 nF fra due fori', size=2.6, anchor='start', weight=500); y += 3.8
    tratteggio_zona(svg, 135, y - 1.2, 2.2, col='#c92a2a')
    svg.text(141.5, y - 1.0, 'testa M3 del vassoio sotto (0,3 mm):', size=2.6, anchor='start', weight=700, fill='#c92a2a')
    svg.text(141.5, y + 2.0, 'niente fili né saldature (S-19)', size=2.6, anchor='start', weight=700, fill='#c92a2a'); y += 6.4
    tratteggio_zona(svg, 135, y - 1.2, 2.2, col='#495057')
    svg.text(141.5, y - 1.0, 'colonnina Ø 5,8: la basetta appoggia', size=2.6, anchor='start', weight=500)
    svg.text(141.5, y + 2.0, 'qui, niente fili né saldature', size=2.6, anchor='start', weight=500); y += 6.2
    croce(svg, 135, y - 1.0, 1.2, '#868e96')
    svg.text(141.5, y, 'foro vietato (rossa: pin dello strip, S-19)', size=2.6, anchor='start', weight=500); y += 3.6
    svg.circle(135, y - 1.0, 1.35, fill='#efe6c8', col='#adb5bd', sw=0.3); svg.circle(135, y - 1.0, 0.5, fill='#adb5bd', col='#868e96', sw=0.15)
    svg.text(141.5, y, 'pin dello strip non usato: tagliato a filo,', size=2.6, anchor='start', weight=500); y += 3.0
    svg.text(141.5, y, 'non saldato', size=2.6, anchor='start', weight=500); y += 3.8
    svg.text(131, y, 'Fili: 30 AWG siliconico (X31), 26 AWG (B17)', size=2.6, anchor='start', weight=600); y += 3.0
    svg.text(131, y, 'dove la tabella lo dice. Sotto restano 3,3 mm.', size=2.6, anchor='start', weight=600); y += 3.6
    svg.text(131, y, 'VBAT: un filo solo dalla 2813, lungo il bordo', size=2.6, anchor='start', weight=700, fill='#b00020'); y += 3.0
    svg.text(131, y, 'di sinistra, saldato per ultimo su P-4.', size=2.6, anchor='start', weight=700, fill='#b00020')
    # elenco dei fili
    yl = BY + 70 + 4.2 + 4.4
    for i, f in enumerate(B.fili, 1):
        col, rig = (i - 1) // 6, (i - 1) % 6
        c = CLASSI[classe(f['rete'])]['col'] if classe(f['rete']) != 'sig3' else '#000'
        svg.text(4 + col * 26.5, yl + rig * 2.8, '%d  %s→%s  %d' % (i, h(f['a']), h(f['b']), f['awg']), size=2.45,
                 anchor='start', weight=600, fill=c)
    svg.text(4, 130.6, 'Elenco: n. del filo, da → a, sezione in AWG. Prima di inserire l’ESP32: prove di schemi.md 1.5; '
             'prima accensione senza ESP32.', size=2.6, anchor='start', weight=700, fill='#c92a2a')
    svg.write(os.path.join(OUT, 'basetta_saldature.svg'), 'Basetta dell’ESP32, lato saldature')
    BY = 30.0
    return R




def assiali(svg, spec=False):
    for rif, val, f1, n1, f2, n2, L, D, tipo in d.ASSIALI:
        if tipo == 'ptc':
            continue
        X1, Y1 = fxy(f1, spec); X2, Y2 = fxy(f2, spec)
        svg.line(X1, Y1, X2, Y2, col='#555', w=0.5)
        mx, my = (X1 + X2) / 2, (Y1 + Y2) / 2
        vert = abs(X1 - X2) < 0.1
        Lb, Db = L * S, D * S
        fill = '#d0ebff' if tipo == 'res' else '#ffe3e3'
        if vert:
            svg.rect(mx - Db / 2, my - Lb / 2, Db, Lb, fill=fill, col='#000', sw=0.35, rx=0.8)
        else:
            svg.rect(mx - Lb / 2, my - Db / 2, Lb, Db, fill=fill, col='#000', sw=0.35, rx=0.8)
        if tipo == 'diodo':      # fascia dal lato del catodo (primo foro)
            if vert:
                yy = my - Lb / 2 + 0.9 if Y1 < Y2 else my + Lb / 2 - 0.9
                svg.line(mx - Db / 2, yy, mx + Db / 2, yy, w=0.9)
            else:
                xx = mx - Lb / 2 + 0.9 if X1 < X2 else mx + Lb / 2 - 0.9
                svg.line(xx, my - Db / 2, xx, my + Db / 2, w=0.9)
        if vert:
            svg.text(mx + 0.9, my, rif + ' ' + val, size=2.4, weight=700, rot=-90, halo=True)
        else:
            svg.text(mx, my + 0.9, rif + ' ' + val, size=2.4, weight=700, halo=True)


def componenti():
    global BY
    BY = 30.0
    svg = Svg(190, 124)
    svg.text(4, 6.5, 'Basetta dell’ESP32 — lato componenti', size=4.4, anchor='start', weight=800)
    svg.text(4, 11, 'Scala 2:1 (1 passo = 5,08 mm sul foglio). Vista dall’alto: testa del robot a destra, '
             'sinistra del robot (+Y) in alto. Millefori C2 tagliata a 56 × 35 (D-053).', size=2.6, anchor='start', weight=500)
    contorno(svg, False)
    # teste M3 del vassoio (sotto la basetta) e colonnine con la vite M2 (sopra)
    for x, y in d.TESTE_M3:
        X, Y = tb(x, y, False)
        svg.circle(X, Y, d.R_TESTA * S, col='#c92a2a', sw=0.4, dash='1 0.6')
    for x, y in d.COLONNINE:
        X, Y = tb(x, y, False)
        svg.circle(X, Y, 1.1 * S, fill='#fff', col='#000', sw=0.4)
        svg.circle(X, Y, 1.9 * S, col='#000', sw=0.3, dash='0.8 0.6')
        svg.line(X - 1.0, Y, X + 1.0, Y, w=0.3); svg.line(X, Y - 1.0, X, Y + 1.0, w=0.3)
    # ESP32 e microSD
    X0, Y0 = tb(22.5, 7.0, False); X1, Y1 = tb(37.5, -7.0, False)
    svg.rect(X0, Y0, X1 - X0, Y1 - Y0, col='#1971c2', sw=0.35, dash='1.2 0.8')
    for yy in (14.15, -14.15):
        Xa, Ya = tb(22.0, yy, False); Xb, Yb = tb(78.0, yy, False)
        svg.line(Xa, Ya, Xb, Yb, col='#1971c2', w=0.35, dash='2 1')
    fori(svg, False)
    for riga, nomi in ((2, d.ESP_L), (12, d.ESP_R)):
        Xa, Ya = tb(22.5, GB.xy('A%d' % riga)[1] + 1.27, False); Xb, Yb = tb(73.3, GB.xy('A%d' % riga)[1] - 1.27, False)
        svg.rect(Xa, Ya, Xb - Xa, Yb - Ya, fill='#343a40', col='#000', sw=0.3, op=0.12)
        for i, n in enumerate(nomi):
            f = LET[i] + str(riga)
            X, Y = fxy(f, False)
            used = d.ESP_NET.get(f)
            svg.text(X, Y + 0.9, n, size=2.5, weight=800 if used else 500, fill='#000' if used else '#868e96', halo=True)
    C = {'U2': (52.98, -8.89, 70.76, 8.89), 'U3': (31.9, -9.52, 51.2, -3.17), 'U4': (33.7, -1.54, 46.9, 9.16),
         'PTC1': (38.0, -10.05, 50.7, -2.65)}
    def box(k, dash=None, fill='#ffffff', op=0.75):
        x0, y0, x1, y1 = C[k]
        Xa, Ya = tb(x0, y1, False); Xb, Yb = tb(x1, y0, False)
        svg.rect(Xa, Ya, Xb - Xa, Yb - Ya, fill=fill, col='#000', sw=0.45, dash=dash, op=op)
        return Xa, Ya, Xb, Yb
    Xa, Ya, Xb, Yb = box('U2')
    cx = (Xa + Xb) / 2
    svg.text(cx, Ya + 13, 'U2  D24V22F5', size=3.0, weight=800)
    svg.text(cx, Ya + 16.5, 'regolatore 5 V (B2)', size=2.6, weight=500)
    svg.text(cx, Ya + 20, 'su nastro isolante, alto 7,2', size=2.5, weight=500)
    svg.text(cx, Ya + 23.5, 'ordine dei pin da leggere [C]', size=2.5, weight=700, fill='#c92a2a')
    Xa, Ya, Xb, Yb = box('U3')
    X, Y = tb(31.9, -6.35, False); svg.path('M %.2f %.2f a 1.4 1.4 0 0 1 0 2.8' % (X, Y - 1.4), col='#000', sw=0.35)
    Xp, Yp, Xq, Yq = box('PTC1', dash='1.4 0.7', fill='#fff3bf', op=0.55)
    svg.text(Xa + 6.5, (Ya + Yb) / 2 + 1.0, 'U3', size=3.0, weight=800, halo=True)
    svg.text((Xp + Xq) / 2, (Ya + Yb) / 2 - 0.6, 'PTC1 sopra U3,', size=2.4, weight=700, halo=True)
    svg.text((Xp + Xq) / 2, (Ya + Yb) / 2 + 2.4, 'su Kapton', size=2.4, weight=700, halo=True)
    Xa, Ya, Xb, Yb = box('U4', fill='#e7f5ff', op=0.45)
    svg.text((Xa + Xb) / 2, Ya + 7.5, 'U4 traslatore C1', size=2.6, weight=800, halo=True)
    svg.text((Xa + Xb) / 2, Ya + 10.5, 'sotto: niente; pin a filo', size=2.4, weight=600, halo=True)
    svg.text((Xa + Xb) / 2, Ya + 13.5, 'sigle e file [C]', size=2.4, weight=700, fill='#c92a2a', halo=True)
    assiali(svg)
    for f, (comp, nome, rete) in B.pin.items():
        if comp not in ('U2', 'U3', 'U4'):
            continue
        X, Y = fxy(f, False)
        corto = nome.split(' ')[-1]
        r = int(f[1:])
        dy = {('U2', 4): 3.8, ('U4', 4): -2.0, ('U4', 7): 3.8, ('U3', 8): 3.8, ('U3', 11): -2.1}[(comp, r)]
        svg.text(X, Y + dy, corto, size=2.4, weight=700, halo=True)
    # fili esterni: coda (lato componenti, verso la coda) e righe 1 e 13 (verso i fianchi)
    for f, e in d.EST.items():
        X, Y = fxy(f, False)
        col = CLASSI[classe(e['rete'])]['col']
        if e['lato'] == 'coda':
            o = {'E3': -1.5, 'F3': 0.0, 'H3': 1.5}.get(f, 0.0)
            svg.add(f'<path d="M {X:.2f} {Y:.2f} L {X - 1.4:.2f} {Y + o:.2f} L {BX - 0.5:.2f} {Y + o:.2f}" fill="none" '
                    f'stroke="{col}" stroke-width="0.5"/>')
            svg.path('M %.2f %.2f l 1.4 -0.8 l 0 1.6 z' % (BX - 1.6, Y + o), fill=col, col='none')
        elif e['lato'] == 'lato':
            svg.line(X, Y, X, BY + 70 + 0.6, col=col, w=0.45)
    for c0, c1, t in (('A', 'F', 'GND'), ('G', 'J', 'SCL'), ('K', 'N', '3,3 V'), ('Q', 'T', 'SDA')):
        Xa, _ = fxy(c0 + '1', False); Xb, _ = fxy(c1 + '1', False)
        svg.line(Xa, BY - 5.2, Xb, BY - 5.2, w=0.4)
        svg.line(Xa, BY - 5.2, Xa, BY - 4.2, w=0.4); svg.line(Xb, BY - 5.2, Xb, BY - 4.2, w=0.4)
        svg.text((Xa + Xb) / 2, BY - 6.2, t + (' (A, B, E, F)' if t == 'GND' else ''), size=2.6, weight=800)
    svg.text(BX + 56, BY - 10.2, 'Riga 1: bus dei sensori, un ramo per foro di ogni gruppo: INA260 S, INA260 D, ADC + IMU, ToF',
             size=2.6, weight=600)
    for f, n, polo in d.CAVO:
        X, Y = fxy(f, False)
        svg.text(X, BY + 70 + 8.0, str(polo), size=2.6, weight=800)
    Xa, _ = fxy('A13', False); Xb, _ = fxy('O13', False)
    svg.line(Xa, BY + 70 + 9.2, Xb, BY + 70 + 9.2, w=0.4)
    svg.text((Xa + Xb) / 2, BY + 70 + 12.4, 'poli 1–13 del cavo piatto (rosso = polo 1; C e D saltate)',
             size=2.5, weight=600)
    for f, t in (('P13', '42'), ('Q13', 'OFF'), ('R13', 'BAT'), ('S13', 'GND'), ('T13', 'TIB')):
        X, _ = fxy(f, False); svg.text(X + 0.9, BY + 70 + 6.0, t, size=2.4, weight=800, rot=-90, anchor='end')
    # legenda
    y = legenda(svg, 131, 18, ['vbat', '5v', '3v3', 'gnd', 'i2c', 'sig5', 'sig3', 'cmd'], titolo='Reti (bordo delle piazzole)')
    y += 0.6
    svg.text(131, y, 'Simboli', size=3.2, anchor='start', weight=700); y += 3.8
    svg.circle(135, y - 0.9, 1.9, col='#000', sw=0.3, dash='0.8 0.6'); svg.circle(135, y - 0.9, 1.1, fill='#fff', col='#000', sw=0.4)
    svg.text(141.5, y, 'vite M2 della colonnina (testa tratteggiata)', size=2.6, anchor='start', weight=500); y += 3.6
    svg.circle(135, y - 0.9, 2.2, col='#c92a2a', sw=0.4, dash='1 0.6')
    svg.text(141.5, y, 'testa M3 del vassoio, sotto la basetta', size=2.6, anchor='start', weight=500); y += 3.6
    croce(svg, 135, y - 1.0, 1.2, '#868e96')
    svg.text(141.5, y, 'foro vietato (testa M3 o colonnina sotto)', size=2.6, anchor='start', weight=500); y += 3.6
    svg.rect(132, y - 2.4, 6, 3.0, fill='#d0ebff', col='#000', sw=0.35, rx=0.8)
    svg.text(141.5, y, 'resistenza sdraiata', size=2.6, anchor='start', weight=500); y += 3.6
    svg.rect(132, y - 2.4, 6, 3.0, fill='#ffe3e3', col='#000', sw=0.35, rx=0.8); svg.line(132.9, y - 2.4, 132.9, y + 0.6, w=0.9)
    svg.text(141.5, y, 'diodo: la fascia è il catodo', size=2.6, anchor='start', weight=500); y += 3.6
    svg.line(132, y - 0.9, 140, y - 0.9, col='#1971c2', w=0.35, dash='2 1')
    svg.text(141.5, y, 'bordo dell’ESP32; riquadro: microSD, ≤ 6,6', size=2.6, anchor='start', weight=500); y += 4.4
    svg.text(131, y, 'Fili esterni (saldati al banco)', size=3.2, anchor='start', weight=700); y += 3.6
    for f in ('E3', 'F3', 'H3', 'P13', 'Q13', 'R13', 'S13', 'T13'):
        e = d.EST[f]
        svg.text(131, y, h(f), size=2.5, anchor='start', weight=800)
        svg.text(138, y, e['testo'], size=2.5, anchor='start', weight=500); y += 2.9
    svg.text(131, y, 'VBAT', size=2.5, anchor='start', weight=800, fill='#b00020')
    svg.text(138, y, 'su P-4, lungo il bordo sinistro (lato saldature)', size=2.5, anchor='start', weight=500); y += 3.6
    svg.text(131, y, '[C] = da confermare sul pezzo.', size=2.6, anchor='start', weight=700, fill='#c92a2a')
    assi(svg, False, BY)
    svg.text(4, 122.4, 'Reti, fili e fonti: guida/schemi/schemi.md. Non saldare prima che i problemi bloccanti di '
             'guida/problemi/schemi.yaml (S-01, S-02, S-19) siano chiusi.', size=2.6, anchor='start', weight=700, fill='#c92a2a')
    svg.write(os.path.join(OUT, 'basetta.svg'), 'Basetta dell’ESP32, lato componenti')


if __name__ == '__main__':
    R = saldature()
    print('incroci', len(R.incroci()))
    componenti()
