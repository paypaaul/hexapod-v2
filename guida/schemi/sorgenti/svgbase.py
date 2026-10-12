import math, os
from xml.sax.saxutils import escape
FONT = "'Barlow Condensed','Arial Narrow','Helvetica Neue',Arial,sans-serif"
# ---------------------------------------------------------------- stili delle reti
CLASSI = {
    'vbat': dict(nome='Batteria dopo la 2813 (6,0–8,4 V)', col='#b00020', w=1.5, dash=None, doppia=True),
    '5v':   dict(nome='5 V (regolatore, ESP32, LED)', col='#e8590c', w=1.1, dash='2.6 1.3'),
    '3v3':  dict(nome='3,3 V', col='#1971c2', w=0.9, dash='0.9 0.9'),
    'gnd':  dict(nome='Massa', col='#212529', w=0.9, dash=None),
    'i2c':  dict(nome='SDA e SCL (bus dei sensori)', col='#2b8a3e', w=0.7, dash='3.2 1 0.9 1'),
    'sig5': dict(nome='Segnali a 5 V (dati LED, seriale lato SSC-32)', col='#862e9c', w=0.7, dash='1.8 0.9'),
    'sig3': dict(nome='Segnali a 3,3 V (GPIO, I2S)', col='#495057', w=0.5, dash=None),
    'cmd':  dict(nome='Comandi: abilitazione rail, OFF, misura batteria', col='#c2255c', w=0.8, dash='0.3 1.0'),
    'btn':  dict(nome='Pulsante (pin A e B della 2813)', col='#5c940d', w=0.8, dash='4 1.2'),
}

def classe(net):
    n = net.upper()
    if n.startswith('VBAT'): return 'vbat'
    if n.startswith('5V'): return '5v'
    if n.startswith('3V3'): return '3v3'
    if n.startswith('GND'): return 'gnd'
    if n in ('SDA', 'SCL'): return 'i2c'
    if n in ('DATA', 'Y1', 'TX5', 'RX5', 'RMT5'): return 'sig5'
    if n in ('EN', 'OFF', 'SENSE', 'GPIO42'): return 'cmd'
    if n.startswith('BTN'): return 'btn'
    return 'sig3'

# ---------------------------------------------------------------- utilita' SVG
class Svg:
    def __init__(s, w, h):
        s.w, s.h, s.el = w, h, []
    def add(s, x): s.el.append(x)
    def text(s, x, y, t, size=2.6, anchor='middle', weight=600, fill='#111', rot=None, halo=False, italic=False):
        tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ''
        h = ' stroke="#fff" stroke-width="0.7" paint-order="stroke" stroke-linejoin="round"' if halo else ''
        st = ' font-style="italic"' if italic else ''
        s.add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
              f'fill="{fill}"{h}{st}{tr}>{escape(t)}</text>')
    def line(s, x1, y1, x2, y2, col='#000', w=0.3, dash=None, cap='round', op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        s.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" stroke-width="{w}"'
              f' stroke-linecap="{cap}"{d} opacity="{op}"/>')
    def rect(s, x, y, w, h, fill='none', col='#000', sw=0.3, dash=None, rx=0, op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        s.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}" stroke="{col}"'
              f' stroke-width="{sw}"{d} fill-opacity="{op}"/>')
    def circle(s, x, y, r, fill='none', col='#000', sw=0.3, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        s.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}" stroke="{col}" stroke-width="{sw}"{d}/>')
    def path(s, d, fill='none', col='#000', sw=0.3, dash=None):
        dd = f' stroke-dasharray="{dash}"' if dash else ''
        s.add(f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{sw}"{dd}/>')
    def write(s, path, title):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w}mm" height="{s.h}mm" viewBox="0 0 {s.w} {s.h}" '
                f'font-family="{FONT}">\n<title>{escape(title)}</title>\n'
                f'<rect x="0" y="0" width="{s.w}" height="{s.h}" fill="#fff"/>\n')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(head + '\n'.join(s.el) + '\n</svg>\n')

def stile_rete(svg, x1, y1, x2, y2, net, extra_w=0, cl=None):
    c = CLASSI[cl or classe(net)]
    w = c['w'] + extra_w
    svg.line(x1, y1, x2, y2, col=c['col'], w=w, dash=c['dash'])
    if c.get('doppia'):
        svg.line(x1, y1, x2, y2, col='#fff', w=w * 0.33)

def legenda(svg, x, y, classi, extra=(), larg=56, titolo='Legenda', nomi=None):
    svg.text(x, y, titolo, size=3.2, anchor='start', weight=700)
    y += 4.2
    for k in classi:
        c = CLASSI[k]
        stile_rete(svg, x, y - 0.9, x + 9, y - 0.9, k, cl=k)
        svg.text(x + 10.5, y, (nomi or {}).get(k, c['nome']), size=2.6, anchor='start', weight=500)
        y += 3.7
    for disegna, testo in extra:
        disegna(x, y - 0.9)
        righe = testo.split('\n')
        for i, r in enumerate(righe):
            svg.text(x + 10.5, y + i * 3.0, r, size=2.6, anchor='start', weight=500)
        y += 3.7 + 3.0 * (len(righe) - 1)
    return y

