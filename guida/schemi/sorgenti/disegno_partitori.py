"""Disegno della striscia dei partitori: partitori.svg (lato componenti) e partitori_saldature.svg (lato saldature,
specchiato da sinistra a destra). Stesso stile di disegno_basetta.py e disegno_scheda.py."""
import os
import partitori_def as d
import svgbase
from svgbase import Svg, CLASSI, legenda
from modello import h
from disegno import classe, stile, OUT

S, GS = d.S, d.GS
P = 2.54
SS = 5.0                       # scala 5:1
SX, SY = 24.0, 57.0            # centro di A-1
COLONNE = 'ABCDEFGHI'
R_PAD, R_FORO = 0.8 * SS, 0.4 * SS
W_SVG, H_SVG = 190, 160
NOMI = {'3v3': '+3,3 V (dal pin VIN dell’ADC)', 'gnd': 'Massa', 'sig3': 'Nodo del canale (ingresso dell’ADC)'}


def pos(f, spec):
    c, r = GS.cr(f)
    x = (d.NCOL - 1 - c) if spec else c
    return SX + x * P * SS, SY + (r - 1) * P * SS


def contorno(svg, spec):
    x0, y0 = SX - P * SS / 2, SY - P * SS / 2
    svg.rect(x0, y0, d.NCOL * P * SS, d.NRIG * P * SS, fill='#f3efe2', col='#000', sw=0.5)


def fori(svg, spec):
    for f in GS.fori():
        X, Y = pos(f, spec)
        if f in S.pin and S.pin[f][2]:
            col = CLASSI[classe(S.pin[f][2])]['col']
            svg.circle(X, Y, R_PAD, fill='#e8d9a8', col=col, sw=0.7)
            svg.circle(X, Y, R_FORO, fill='#fff', col='#7a6a3a', sw=0.2)
        elif f in d.VITI:
            svg.circle(X, Y, 1.2 * SS, fill='#fff', col='#000', sw=0.5)
        else:
            svg.circle(X, Y, R_PAD * 0.9, fill='#efe6c8', col='#c8b88a', sw=0.25)
            svg.circle(X, Y, R_FORO * 0.9, fill='#fff', col='#c8b88a', sw=0.15)


def assi(svg, spec, ytop):
    for c in range(d.NCOL):
        X, _ = pos(COLONNE[c] + '1', spec)
        if ytop is not None:
            svg.text(X, ytop, COLONNE[c], size=3.4, weight=700)
        svg.text(X, SY + 3 * P * SS + P * SS / 2 + 5.0, COLONNE[c], size=3.4, weight=700)
    for r in range(1, 5):
        _, Y = pos('A%d' % r, spec)
        svg.text(SX - P * SS / 2 - 3.2, Y + 1.2, str(r), size=3.4, weight=700)
        svg.text(SX + d.NCOL * P * SS - P * SS / 2 + 3.4, Y + 1.2, str(r), size=3.4, weight=700)


def cerchio_n(svg, x, y, n, col):
    svg.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.0" fill="#fff" stroke="{col}" stroke-width="0.4"/>')
    svg.text(x, y + 1.0, str(n), size=2.7, weight=800, fill=col)


def percorsi_fili(spec):
    """Per ogni filo esterno: punti del tratto disegnato (dal foro in su, fra le colonne) e numero."""
    out = []
    ytop = SY - P * SS / 2 - 11.0
    for (n, f, rete, da, a, nota) in d.FILI:
        X, Y = pos(f, spec)
        c, r = GS.cr(f)
        col = CLASSI[classe(rete)]['col']
        if f in ('A1', 'A4') and rete in ('GND', '3V3') and 'ADC' in da:
            # fili dell'ADC: escono sul bordo sinistro (o destro nel lato saldature)
            sg = 1 if spec else -1
            if r == 1:
                pts = [(X, Y), (X + sg * P * SS * 0.5, Y - 4.0), (X + sg * 17.0, Y - 4.0)]
            else:
                pts = [(X, Y), (X + sg * P * SS * 0.5, Y + 4.0), (X + sg * 17.0, Y + 4.0)]
        elif r == 1:
            pts = [(X, Y), (X, ytop + 1.0)]
        else:
            # riga 2: fili nei canali fra le colonne, a destra l'uscita verso l'ADC, a sinistra il segnale della presa
            lato = 1 if 'ADC' in a else -1
            if spec:
                lato = -lato
            xc = X + lato * (P * SS / 2 - 2.2)
            yend = ytop + 8.0 if 'ADC' in a else ytop - 6.0
            pts = [(X, Y), (xc, Y - P * SS / 2 + 1.0), (xc, yend)]
        out.append((n, pts, col, f, rete))
    return out


def componenti():
    svg = Svg(W_SVG, H_SVG)
    svg.text(4, 6.5, 'Striscia dei partitori (X5, X6, X14) — lato componenti', size=4.4, anchor='start', weight=800)
    svg.text(4, 11, 'Scala 5:1. Vista da sopra. Colonne A–H = canali 0–7 dell’ADS7830; la colonna I porta le due viti M2. '
             'Nel corpo (proposta, S-28): colonne lungo Y con A verso +Y, riga 1 verso la testa.', size=2.6, anchor='start', weight=500)
    svg.text(4, 15, 'POSTO NON DIMOSTRATO (S-28): 22,86 × 10,16 mm non entrano fra ADC, IMU e prese delle luci. '
             'Collegamenti e valori validi.', size=2.6, anchor='start', weight=700, fill='#c92a2a')
    contorno(svg, False)
    fori(svg, False)
    # caldi: viti M2, teste Ø 4 che sfiorano H-1 e H-4
    for f in d.VITI:
        X, Y = pos(f, False)
        svg.circle(X, Y, 2.0 * SS, col='#c92a2a', sw=0.35, dash='1.2 0.8')
        svg.text(X, Y + 1.0, 'M2', size=2.7, weight=800)
    for f in d.LIBERI:
        X, Y = pos(f, False)
        svg.text(X, Y + 1.0, 'libero', size=2.4, weight=500, fill='#868e96')
    # condensatori sul lato saldature (tratteggiati), fra riga 1 e riga 2
    for c in range(8):
        X, Y1 = pos(COLONNE[c] + '1', False)
        _, Y2 = pos(COLONNE[c] + '2', False)
        prop = ('C%d' % (c + 1)) in d.PROPOSTE
        svg.rect(X - 1.0 * SS, Y1 + 0.35 * SS, 2.0 * SS, Y2 - Y1 - 0.7 * SS, fill='#d3f9d8', col='#2b8a3e', sw=0.4,
                 dash='1.4 0.8' if not prop else '0.6 1.0', op=0.55)
        svg.text(X + 0.3, Y1 + 0.5 * (Y2 - Y1) + 0.9, 'C%d%s' % (c + 1, '*' if prop else ''), size=2.5, weight=700, fill='#2b8a3e')
    # resistenze in piedi: corpo sul foro di riga 3, reoforo piegato sul foro di riga 4
    for c in range(8):
        X, Y3 = pos(COLONNE[c] + '3', False)
        _, Y4 = pos(COLONNE[c] + '4', False)
        svg.line(X, Y3, X, Y4, col='#7a4a12', w=0.7)
        svg.circle(X, Y3, 1.2 * SS, fill='#f4d9a6', col='#000', sw=0.4)
        svg.text(X, Y3 + 1.0, 'R%d' % (c + 1), size=2.7, weight=800)
    # fili esterni
    pf = percorsi_fili(False)
    for n, pts, col, f, rete in pf:
        stile(svg, pts, rete, 0.2)
    for n, pts, col, f, rete in pf:
        cerchio_n(svg, pts[-1][0], pts[-1][1] - 3.0, n, col)
    # etichette dei canali sopra i fili
    ytop = SY - P * SS / 2 - 11.0
    for c in range(8):
        X, _ = pos(COLONNE[c] + '1', False)
        svg.text(X, ytop - 17.5, 'canale %d' % c, size=2.5, weight=700)
        svg.text(X, ytop - 14.6, d.CANALI[c], size=2.5, weight=500)
    assi(svg, False, None)
    yb = SY + 3 * P * SS + P * SS / 2 + 12.5
    for i, t in enumerate(['R1–R8: 10 kΩ 1 %, in piedi (corpo sulla riga 3, reoforo piegato sulla riga 4).',
                           'C1–C8: 100 nF SMD sul lato saldature, fra riga 1 e riga 2 (* = proposta, S-30).',
                           'Rosso tratteggiato: testa della M2 (Ø 4), a 0,4 mm dalla piazzola di H-1 e di H-4: isolare (S-29).',
                           'Fori delle viti: Ø 2,4.']):
        svg.text(4, yb + 3.4 * i, t, size=2.6, anchor='start', weight=600)
    yb += 10.4
    # lista dei fili
    y = yb + 6.5
    svg.text(4, y, 'Fili esterni, 30 AWG siliconico (numeri da 201): dal lato componenti, dall’alto, nel foro indicato', size=3.0,
             anchor='start', weight=800)
    y += 4.0
    righe = ['%d  %s  %s → %s' % (n, h(f), da, a) for (n, f, rete, da, a, nota) in d.FILI]
    colw = 62
    per = (len(righe) + 2) // 3
    for i, t in enumerate(righe):
        svg.text(4 + colw * (i // per), y + 2.9 * (i % per), t, size=2.4, anchor='start', weight=600)
    # schema elettrico di un canale
    schema(svg, 140, 24)
    legenda(svg, 140, 104, ['3v3', 'gnd', 'sig3'], titolo='Reti', nomi=NOMI)
    svg.write(os.path.join(OUT, 'partitori.svg'), 'Striscia dei partitori, lato componenti')


def schema(svg, x0, y0):
    """Un canale: 3,3 V – R – nodo – (ADC), nodo – sensore – massa, nodo – C – massa."""
    svg.text(x0, y0, 'Un canale', size=3.2, anchor='start', weight=700)
    xs = x0 + 16
    c3, cg = CLASSI['3v3']['col'], CLASSI['gnd']['col']
    ytop_, ynode, ybot = y0 + 6, y0 + 28, y0 + 50
    svg.line(xs - 8, ytop_, xs + 24, ytop_, col=c3, w=0.9, dash=CLASSI['3v3']['dash'])
    svg.text(xs - 8, ytop_ - 1.2, '+3,3 V', size=2.6, anchor='start', weight=700, fill=c3)
    # R
    svg.line(xs, ytop_, xs, ytop_ + 6, col='#000', w=0.5)
    svg.rect(xs - 1.8, ytop_ + 6, 3.6, 9, fill='#fff', col='#000', sw=0.5)
    svg.line(xs, ytop_ + 15, xs, ynode, col='#000', w=0.5)
    svg.text(xs + 3.0, ytop_ + 11.5, 'R  10 kΩ 1 %', size=2.5, anchor='start', weight=600)
    # nodo e uscita
    svg.circle(xs, ynode, 0.9, fill='#000')
    svg.line(xs, ynode, xs + 26, ynode, col='#000', w=0.5)
    svg.text(xs + 26, ynode - 1.5, 'ADC A0–A7', size=2.5, anchor='end', weight=700)
    # C
    xc = xs + 10
    svg.line(xs, ynode, xc, ynode, col='#000', w=0.5)
    svg.line(xc, ynode, xc, ynode + 8, col='#000', w=0.5)
    svg.line(xc - 3, ynode + 8, xc + 3, ynode + 8, col='#000', w=0.7)
    svg.line(xc - 3, ynode + 10, xc + 3, ynode + 10, col='#000', w=0.7)
    svg.line(xc, ynode + 10, xc, ybot, col='#000', w=0.5)
    svg.text(xc + 4.0, ynode + 10.0, 'C  100 nF', size=2.5, anchor='start', weight=600)
    # sensore
    svg.line(xs, ynode, xs, ynode + 6, col='#000', w=0.5)
    svg.rect(xs - 1.8, ynode + 6, 3.6, 9, fill='#fff', col='#000', sw=0.5, dash='1 0.6')
    svg.line(xs, ynode + 15, xs, ybot, col='#000', w=0.5)
    svg.text(xs - 3.0, ynode + 11.5, 'FSR o NTC', size=2.5, anchor='end', weight=600)
    svg.line(xs - 8, ybot, xs + 24, ybot, col=cg, w=0.9)
    svg.text(xs - 8, ybot + 3.2, 'massa', size=2.6, anchor='start', weight=700, fill=cg)
    for i, t in enumerate(['Lettura invertita: più forza, meno ohm,', 'tensione più bassa. NTC: più caldo,', 'meno ohm, codice più basso.',
                           'Il 3,3 V è quello del pin VIN dell’ADC:', 'riferimento = alimentazione, la lettura', 'è un rapporto e non dipende dal 3,3 V.']):
        svg.text(x0, ybot + 8 + 3.0 * i, t, size=2.4, anchor='start', weight=500)


def saldature():
    svg = Svg(W_SVG, 134)
    svg.text(4, 7.5, 'Striscia dei partitori — LATO SALDATURE (specchiata)', size=5.0, anchor='start', weight=800)
    svg.text(4, 12, 'Scala 5:1. Vista dal lato saldature: la striscia è girata attorno al lato corto, la colonna I a sinistra e la A a destra. '
             'Millefori a doppia faccia, nessuna striscia da tagliare.', size=2.6, anchor='start', weight=500)
    contorno(svg, True)
    fori(svg, True)
    for a, b, rete in S.ponti:
        (x1, y1), (x2, y2) = pos(a, True), pos(b, True)
        svg.line(x1, y1, x2, y2, col='#adb5bd', w=3.2)
        stile(svg, [(x1, y1), (x2, y2)], rete, 0.3)
    for c in range(8):
        X, Y1 = pos(COLONNE[c] + '1', True)
        _, Y2 = pos(COLONNE[c] + '2', True)
        prop = ('C%d' % (c + 1)) in d.PROPOSTE
        svg.rect(X - 1.0 * SS, Y1 + 0.35 * SS, 2.0 * SS, Y2 - Y1 - 0.7 * SS, fill='#d3f9d8', col='#2b8a3e', sw=0.5,
                 dash='0.6 1.0' if prop else None, op=0.9)
        svg.text(X, Y1 + 0.5 * (Y2 - Y1) + 0.9, 'C%d%s' % (c + 1, '*' if prop else ''), size=2.6, weight=800, fill='#14532d')
    # estremi dei fili esterni che escono dai fori (un punto per filo)
    for f, k in d.conteggi().items():
        X, Y = pos(f, True)
        for j in range(k):
            dx = (j - (k - 1) / 2) * 3.0
            svg.circle(X + dx, Y, 1.05, fill='#000', col='#fff', sw=0.3)
    for c in range(8):
        X, Y = pos(COLONNE[c] + '3', True)
        svg.text(X, Y + 7.2, 'R%d' % (c + 1), size=2.4, weight=600, fill='#7a4a12')
    for f in d.VITI:
        X, Y = pos(f, True)
        svg.text(X, Y + 1.0, 'M2', size=2.7, weight=800)
    assi(svg, True, SY - P * SS / 2 - 1.4)
    yb = SY + 3 * P * SS + P * SS / 2 + 12.5
    svg.text(4, yb, 'Ponticelli (22): riga 1 da A a H (massa, un filo nudo teso), riga 4 da A a H (3,3 V, un filo nudo teso), '
             'e 8 piccoli ponti fra riga 2 e riga 3 di ogni colonna (nodo).', size=2.6, anchor='start', weight=600)
    svg.text(4, yb + 3.4, 'Su questo lato non ci sono fili isolati, solo ponticelli e gli 8 condensatori SMD. '
             'I reofori delle R e i fili esterni si tagliano a 1 mm.', size=2.6, anchor='start', weight=600)
    svg.text(4, yb + 6.8, 'Righe 3 e 4: un reoforo di R a testa (R3 sulla riga 3, il reoforo piegato sulla riga 4). '
             'Righe 1 e 2: punti neri = estremi dei fili esterni (1 o 2 per foro).', size=2.6, anchor='start', weight=600)
    yl = yb + 12
    svg.line(30, yl - 1.0, 38, yl - 1.0, col='#adb5bd', w=3.0)
    svg.text(40, yl, 'ponticello di stagno o filo nudo', size=2.6, anchor='start', weight=500)
    svg.rect(88, yl - 3, 8, 3.4, fill='#d3f9d8', col='#2b8a3e', sw=0.5)
    svg.text(98, yl, 'condensatore SMD 100 nF', size=2.6, anchor='start', weight=500)
    svg.circle(142, yl - 1.2, 1.05, fill='#000')
    svg.text(145, yl, 'estremo di un filo esterno', size=2.6, anchor='start', weight=500)
    legenda(svg, 142, 24, ['3v3', 'gnd', 'sig3'], titolo='Reti', nomi=NOMI)
    svg.write(os.path.join(OUT, 'partitori_saldature.svg'), 'Striscia dei partitori, lato saldature')


if __name__ == '__main__':
    componenti()
    saldature()
