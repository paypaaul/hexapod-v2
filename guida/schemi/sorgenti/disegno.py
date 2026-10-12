"""Disegno degli SVG (seconda versione)."""
import math, os
import svgbase
_classe0 = svgbase.classe
from svgbase import Svg, CLASSI, legenda
from modello import LET, h

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def classe(net):
    n = (net or '').upper()
    if n in ('J1',):
        return '3v3'
    if n in ('DATA2', 'H_NC'):
        return 'sig5'
    if n in ('L_NC', 'LO'):
        return 'sig3'
    return _classe0(net)


svgbase.classe = classe


def stile(svg, pts, net, extra_w=0):
    c = CLASSI[classe(net)]
    w = c['w'] + extra_w
    d = 'M ' + ' L '.join('%.2f %.2f' % p for p in pts)
    dash = f' stroke-dasharray="{c["dash"]}"' if c['dash'] else ''
    svg.add(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w + 0.9:.2f}" stroke-linejoin="round" stroke-linecap="round"/>')
    svg.add(f'<path d="{d}" fill="none" stroke="{c["col"]}" stroke-width="{w:.2f}" stroke-linejoin="round" stroke-linecap="round"{dash}/>')
    if c.get('doppia'):
        svg.add(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w * 0.33:.2f}" stroke-linejoin="round"/>')


def tratteggio_zona(svg, X, Y, r, col='#868e96'):
    """Cerchio pieno a righe: zona vietata sul lato saldature."""
    pid = 'z%d%d' % (int(X * 10), int(Y * 10))
    svg.add(f'<clipPath id="{pid}"><circle cx="{X:.2f}" cy="{Y:.2f}" r="{r:.2f}"/></clipPath>')
    svg.add(f'<circle cx="{X:.2f}" cy="{Y:.2f}" r="{r:.2f}" fill="#e9ecef" stroke="{col}" stroke-width="0.35"/>')
    for k in range(-6, 7):
        o = k * r / 3.2
        svg.add(f'<line x1="{X - r + o:.2f}" y1="{Y + r:.2f}" x2="{X + r + o:.2f}" y2="{Y - r:.2f}" stroke="{col}" '
                f'stroke-width="0.3" clip-path="url(#{pid})"/>')


def etichette_fili(svg, fili, nodo_xy, pad_xy, base, size=2.9, evita=()):
    """Numero di ogni filo sul tratto piu' lungo, lontano dalle altre etichette e dai fori."""
    messe = list(evita)
    out = []
    for i, f in enumerate(fili, base + 1):
        p = f.get('pts')
        if not p:
            continue
        cand = []
        for a, b in zip(p, p[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            for t in (0.5, 0.3, 0.7):
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                dmin = min([math.hypot(x - u, y - v) for u, v in messe] + [99])
                dp = min([math.hypot(x - u, y - v) for u, v in pad_xy] + [99])
                cand.append((min(dmin, 6) * 2 + min(dp, 3.2) * 3 + min(L, 8) * 0.3, x, y))
        cand.sort(reverse=True)
        _, x, y = cand[0]
        messe.append((x, y))
        n = str(i)
        w = 1.25 * len(n) + 0.9
        col = CLASSI[classe(f['rete'])]['col']
        svg.add(f'<rect x="{x - w / 2:.2f}" y="{y - 1.75:.2f}" width="{w:.2f}" height="3.3" rx="1.2" fill="#fff" '
                f'stroke="{col}" stroke-width="0.35"/>')
        svg.text(x, y + 1.0, n, size=size, weight=800, fill=col)
        out.append((x, y))
    return out
