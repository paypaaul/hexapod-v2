import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import basetta_def as db, scheda_def as ds, fili_b
from modello import h
from md import FONTI_B, FONTI_S
FONTI_B = dict(FONTI_B)
FONTI_B['VBAT'] = 'cablaggio.md:32, :76 (2813 → D24V22F5); un filo da P-4 alla 2813 lungo il bordo (rilievo 6)'
FONTI_B['5V_ESP'] = 'cablaggio.md:27 (D24V22F5 → pin 5V); D1: scelta S-07, BOM.md:71 (C3)'
FONTI_B['DATA2'] = 'cablaggio.md:47–48, :108 (ramo delle tibie); secondo canale del buffer (rilievo 8)'
FONTI_B['GPIO42'] = 'cablaggio.md:31, :78; piano-elettronica-software.md:99; D2 in linea e R3 ai regolatori (S-20)'
FONTI_B['SENSE'] = 'cablaggio.md:32 (partitore 100 k / 47 k → GPIO1; 100 k alla 2813, S-20); BOM.md:50 (B8), :52 (B10)'
FONTI_B['3V3S'] = 'predisposizioni.md:108 (D24V5F3 o 3V3 della scheda); cablaggio.md:116, :139 (polo 7); LV di U4 (S-04)'
FONTI_B['3V3_ESP'] = 'dimensioni-componenti.md:74 (pin 3V3); piano-elettronica-software.md:77'
FONTI_B['LED_IN'] = 'cablaggio.md:47 (GPIO48, 10 kΩ a massa, ingresso del buffer); piano-elettronica-software.md:102; 2A per le tibie (rilievo 8)'
FONTI_B['TX5'] = 'cablaggio.md:41 (traslatore → RX della SSC-32); 08-elettronica.yaml 8.20'
FONTI_B['RX5'] = 'cablaggio.md:41 (TX della SSC-32 → traslatore); 08-elettronica.yaml 8.20'
FONTI_B['OFF'] = 'cablaggio.md:32, :79; piano-elettronica-software.md:98 (GPIO41)'
ORD = ['VBAT', '5V_REG', '5V_ESP', '5V_LED', '3V3_ESP', '3V3S', 'GND', 'SCL', 'SDA', 'LED_IN', 'Y1', 'DATA', 'DATA2',
       'TX3', 'RX3', 'TX5', 'RX5', 'GPIO42', 'OFF', 'SENSE', 'BCLK', 'WS', 'MIC', 'AMP']

def desc(S, f):
    c, n, r = S.pin[f]
    if c == 'U1':
        return '%s (ESP32 %s)' % (h(f), n if n in ('5V', 'GND', '3V3') else 'GPIO' + n)
    if c == 'filo':
        return '%s (filo: %s)' % (h(f), n)
    if c == 'ponte':
        return '%s (ponticello)' % h(f)
    if c == 'J2':
        return '%s (polo %s)' % (h(f), n)
    return '%s (%s%s)' % (h(f), c, (' ' + n) if n else '')

def netlist_b():
    B = db.B
    righe = ['| Rete | Pin e fori | Fonte |', '|---|---|---|']
    reti = {}
    for f, (c, n, r) in B.pin.items():
        if r and f not in B.nosald and r not in ('H_NC', 'L_NC', 'LO'):
            reti.setdefault(r, []).append(f)
    extra = {'SENSE': ['CS1 verso massa (lato saldature)'], '5V_REG': ['CS2 verso massa (lato saldature)'],
             'VBAT': ['filo dalla 2813, saldato per ultimo'], '3V3S': ['J1 (filo 19) dal 3V3 dell’ESP32']}
    for r in ORD:
        ps = sorted(reti.get(r, []), key=lambda f: (int(f[1:]), f[0]))
        p = [desc(B, f) for f in ps] + extra.get(r, [])
        righe.append('| %s | %s | %s |' % (r, '; '.join(p), FONTI_B.get(r, '—')))
    return '\n'.join(righe)

def netlist_s():
    S = ds.S
    righe = ['| Rete | Pin e fori | Fonte |', '|---|---|---|']
    reti = {}
    for f, (c, n, r) in S.pin.items():
        if r: reti.setdefault(r, []).append(f)
    for r in ['5V', '3V3', 'GND', 'SCL', 'SDA', 'DATA', 'BCLK', 'WS', 'MIC', 'AMP', 'BTN_A', 'BTN_B']:
        ps = sorted(reti.get(r, []), key=lambda f: (int(f[1:]), f[0]))
        p = [desc(S, f) for f in ps]
        if r in ds.DIRETTI.values():
            pass
        for f, (rr, t, awg) in ds.DIRETTI.items():
            if rr == r: p.append('filo del modulo sul pin %s: %s' % (h(f), t))
        righe.append('| %s | %s | %s |' % (r, '; '.join(p), FONTI_S.get(r, '—')))
    return '\n'.join(righe)

def fili_tab(fili, base, nota_awg=True):
    righe = ['| N. | Da | A | Rete | Sezione | A cosa serve |', '|---|---|---|---|---|---|']
    i = base
    for f in fili:
        if not f['b']: continue
        i += 1
        righe.append('| %d | %s | %s | %s | %d AWG | %s |' % (i, h(f['a']), h(f['b']), f['rete'], f['awg'], f['nota']))
    return '\n'.join(righe)

def ponti(S):
    return ', '.join('%s–%s (%s)' % (h(a), h(b), r) for a, b, r in S.ponti)

if __name__ == '__main__':
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_net_b.md'), 'w').write(netlist_b())
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_net_s.md'), 'w').write(netlist_s())
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_fili_b.md'), 'w').write(fili_tab(db.B.fili, 0))
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_fili_s.md'), 'w').write(fili_tab(ds.S.fili, 100))
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_ponti.md'), 'w').write('BASETTA: ' + ponti(db.B) + '\n\nSCHEDA: ' + ponti(ds.S))
    print(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_net_b.md')).read()); print(); print(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_fili_b.md')).read())
    print(); print(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_ponti.md')).read()); print(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_net_s.md')).read()); print(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 't_fili_s.md')).read())
