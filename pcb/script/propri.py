"""Simboli e impronte disegnati per il robot: pcb/librerie/hex2.kicad_sym e i .kicad_mod "propri" di hex2.pretty.

Fonti delle quote:
- ESP32-S3-CAM UICPAL RE1.3: due strip 1 × 20 a 25,4 (V, foto della scheda corta e immagine "Pin definitions" della
  RE1.3, piano-pcb.md, esiti di F0); nomi dei pin da guida/schemi/sorgenti/basetta_def.py (ESP_L, ESP_R); PCB del
  modulo da 2,6 oltre il primo pin di testa a 11,6 oltre l'ultimo di coda, largo 28,3 (S, inserzione);
- Pololu D24V22F5: STEP di Pololu in cad/modelli/pololu-d24v22fx (fori Ø1,016 della fila a passo 2,54, primo a 1,27
  dai bordi; secondo GND a (1,27; 11,938); scheda 17,78 × 17,78), ordine PG, EN, VIN, GND, VOUT (S+, piano 5.1);
- Bourns MF-R090: reofori Ø0,51 a passo 5,1 ± 0,7, disco al più 11,7 × 16,7 × 3,1 (V, scheda Bourns);
- 470 µF 10 V in Ø6,3 × 11 sdraiato, passo 2,5 (S, guida/problemi S-18).

Uso: python3 propri.py (rigenera) o python3 propri.py --controlla.
"""

import os
import sys

from sexpr import S, Sym, scrivi

QUI = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(QUI, '..', 'librerie'))
sys.path.insert(0, os.path.normpath(os.path.join(QUI, '..', '..', 'guida', 'schemi', 'sorgenti')))

PASSO = 2.54


# --- simboli

def _font(nascosto=False):
    e = S('effects', S('font', S('size', 1.27, 1.27)))
    if nascosto:
        e.append(S('hide', Sym('yes')))
    return e


def _prop(nome, valore, x=0, y=0, nascosto=True):
    return S('property', nome, valore, S('at', x, y, 0), _font(nascosto))


def _pin(numero, nome, tipo, x, y, angolo, lunghezza=2.54):
    return S('pin', Sym(tipo), Sym('line'), S('at', x, y, angolo), S('length', lunghezza),
             S('name', nome, _font()), S('number', str(numero), _font()))


def simbolo(nome, ref, valore, descrizione, sinistra, destra, larghezza=20.32, impronta=''):
    """Rettangolo con i pin a sinistra e a destra, dall'alto in basso: liste di (numero, nome, tipo)."""
    n = max(len(sinistra), len(destra))
    alto = (n - 1) * PASSO / 2 + PASSO
    # griglia di 1,27: i pin cadono sulla griglia dello schema
    y0 = round(((n - 1) * PASSO / 2) / 1.27) * 1.27
    corpo = [Sym('symbol'), nome + '_0_1',
             S('rectangle', S('start', -larghezza / 2, alto), S('end', larghezza / 2, -alto),
               S('stroke', S('width', 0.254), S('type', Sym('default'))), S('fill', S('type', Sym('background'))))]
    pin = [Sym('symbol'), nome + '_1_1']
    for lato, elenco in ((-1, sinistra), (1, destra)):
        for i, (num, nm, tipo) in enumerate(elenco):
            x = lato * (larghezza / 2 + PASSO)
            pin.append(_pin(num, nm, tipo, x, round(y0 - i * PASSO, 4), 0 if lato < 0 else 180))
    return [Sym('symbol'), nome, S('pin_names', S('offset', 1.016)), S('exclude_from_sim', Sym('no')),
            S('in_bom', Sym('yes')), S('on_board', Sym('yes')),
            _prop('Reference', ref, 0, alto + 1.27, False), _prop('Value', valore, 0, -alto - 1.27, False),
            _prop('Footprint', impronta), _prop('Datasheet', ''), _prop('Description', descrizione),
            corpo, pin]


def _nome_gpio(n):
    return n if n in ('5V', '3V3', 'GND', 'RST') else 'GPIO' + n


def _tipo_esp(n):
    return {'5V': 'power_in', '3V3': 'power_out', 'GND': 'power_in', 'RST': 'input'}.get(n, 'bidirectional')


def simboli():
    import basetta_def as B
    esp = simbolo(
        'ESP32_S3_CAM_RE13', 'U', 'ESP32-S3-CAM RE1.3',
        'UICPAL ESP32-S3-CAM N16R8 RE1.3 su due strip femmina 1 x 20 a 25,4 mm. Pin 1-20 fila ESP_L dalla coda, '
        '21-40 fila ESP_R dalla coda (pcb/README.md)',
        [(i + 1, _nome_gpio(n), _tipo_esp(n)) for i, n in enumerate(B.ESP_L)],
        [(i + 21, _nome_gpio(n), _tipo_esp(n)) for i, n in enumerate(B.ESP_R)],
        larghezza=20.32, impronta='hex2:ESP32_S3_CAM_RE13_Strip')
    reg = simbolo(
        'D24V22F5', 'U', 'D24V22F5', 'Pololu D24V22F5, regolatore 5 V 2,5 A (pagina Pololu 2858)',
        [(3, 'VIN', 'power_in'), (2, 'EN', 'input'), (1, 'PG', 'open_collector')],
        [(5, 'VOUT', 'power_out'), (4, 'GND', 'power_in'), (6, 'GND', 'power_in')],
        larghezza=12.7, impronta='hex2:Pololu_D24V22F5')
    radice = [Sym('kicad_symbol_lib'), S('version', 20251024), S('generator', 'hex2_propri'),
              S('generator_version', '10.0'), esp, reg]
    return scrivi(radice) + '\n'


# --- impronte

def _linea(a, b, strato, spessore=0.12):
    return S('fp_line', S('start', *a), S('end', *b), S('stroke', S('width', spessore), S('type', Sym('solid'))),
             S('layer', strato))


def _rett(x0, y0, x1, y1, strato, spessore):
    return S('fp_rect', S('start', x0, y0), S('end', x1, y1),
             S('stroke', S('width', spessore), S('type', Sym('solid'))), S('fill', Sym('no')), S('layer', strato))


def _testo(tipo, testo, x, y, strato):
    return S('property', tipo, testo, S('at', x, y, 0), S('layer', strato),
             S('effects', S('font', S('size', 1, 1), S('thickness', 0.15))))


def _pad_tht(num, x, y, d=1.7, foro=1.0, quadrato=False):
    return S('pad', str(num), Sym('thru_hole'), Sym('rect' if quadrato else 'circle'), S('at', x, y),
             S('size', d, d), S('drill', foro), S('layers', '*.Cu', '*.Mask'), S('remove_unused_layers', Sym('no')))


def impronta(nome, descrizione, elementi, rif_y=-2, val_y=2):
    return [Sym('footprint'), nome, S('version', 20260206), S('generator', 'hex2_propri'), S('layer', 'F.Cu'),
            S('descr', descrizione), _testo('Reference', 'REF**', 0, rif_y, 'F.SilkS'),
            _testo('Value', nome, 0, val_y, 'F.Fab'), S('attr', Sym('through_hole'))] + elementi + \
        [S('embedded_fonts', Sym('no'))]


# Posti delle strip senza foro: O-2 e P-2 (pin 15 e 16, GPIO7 e GPIO6), varco del VBAT (piano-pcb.md 4.1)
VARCHI_ESP = (15, 16)


def impronta_esp():
    el = []
    x0 = -9.5 * PASSO
    for i in range(20):
        x = round(x0 + i * PASSO, 4)
        if i + 1 not in VARCHI_ESP:
            el.append(_pad_tht(i + 1, x, -12.7, quadrato=(i == 0)))
        el.append(_pad_tht(i + 21, x, 12.7))
    # strip femmina: corpo 2,54 × 50,8 (sagoma e cortile solo sulle strip, i componenti stanno sotto il modulo)
    for y in (-12.7, 12.7):
        el.append(_rett(x0 - 1.27, y - 1.27, -x0 + 1.27, y + 1.27, 'F.SilkS', 0.12))
        el.append(_rett(x0 - 1.52, y - 1.52, -x0 + 1.52, y + 1.52, 'F.CrtYd', 0.05))
    # PCB del modulo e antenna sullo strato Fab
    coda, testa = x0 - 11.6, -x0 + 2.6
    el.append(_rett(coda, -14.15, testa, 14.15, 'F.Fab', 0.1))
    el.append(_rett(testa, -8, testa + 4.8, 8, 'F.Fab', 0.1))
    el.append(_linea((x0 - 2.2, -14.2), (x0 - 2.2, -11.2), 'F.SilkS'))  # segno del pin 1
    return impronta('ESP32_S3_CAM_RE13_Strip',
                    'UICPAL ESP32-S3-CAM N16R8 RE1.3 su due strip femmina 1x20, file a 25,4; posti 15 e 16 senza '
                    'foro (varco del VBAT). Origine al centro delle file', el, rif_y=-16, val_y=16)


def impronta_d24():
    el = [_pad_tht(n, (n - 1) * PASSO, 0, quadrato=(n == 1)) for n in range(1, 6)]
    el.append(_pad_tht(6, 0, -10.668))
    el.append(_rett(-1.27, 1.27, 16.51, -16.51, 'F.Fab', 0.1))
    el.append(_rett(-1.39, 1.39, 16.63, -16.63, 'F.SilkS', 0.12))
    el.append(_rett(-1.52, 1.52, 16.76, -16.76, 'F.CrtYd', 0.05))
    return impronta('Pololu_D24V22F5',
                    'Pololu D24V22F5: fila PG EN VIN GND VOUT a passo 2,54, secondo GND fuori fila; scheda 17,78 '
                    '(STEP Pololu). Origine sul pin 1 (PG)', el, rif_y=-18, val_y=3)


def impronta_ptc():
    el = [_pad_tht(1, 0, 0, 1.6, 0.8, quadrato=True), _pad_tht(2, 5.08, 0, 1.6, 0.8)]
    # disco sdraiato oltre le piazzole (-Y): 11,7 × 16,7, reofori piegati di 1,5
    el.append(_rett(2.54 - 5.85, -1.5, 2.54 + 5.85, -18.2, 'F.Fab', 0.1))
    el.append(_rett(2.54 - 5.97, -1.38, 2.54 + 5.97, -18.32, 'F.SilkS', 0.12))
    el.append(_rett(2.54 - 6.1, 1.1, 2.54 + 6.1, -18.45, 'F.CrtYd', 0.05))
    return impronta('Fuse_Bourns_MF-R090_Sdraiato',
                    'Bourns MF-R075 / MF-R090 sdraiato, reofori a passo 5,08 (5,1 ± 0,7), disco 11,7 x 16,7',
                    el, rif_y=2.2, val_y=-10)


def impronta_ce():
    el = [_pad_tht(1, 0, 0, 1.6, 0.8, quadrato=True), _pad_tht(2, 2.5, 0, 1.6, 0.8)]
    el.append(_rett(1.25 - 3.15, -1.5, 1.25 + 3.15, -12.5, 'F.Fab', 0.1))
    el.append(_rett(1.25 - 3.27, -1.38, 1.25 + 3.27, -12.62, 'F.SilkS', 0.12))
    el.append(_rett(1.25 - 3.4, 1.1, 1.25 + 3.4, -12.75, 'F.CrtYd', 0.05))
    el.append(_linea((-1.6, -2.2), (-0.6, -2.2), 'F.SilkS'))  # segno del +
    el.append(_linea((-1.1, -2.7), (-1.1, -1.7), 'F.SilkS'))
    return impronta('CP_Radial_D6.3mm_P2.50mm_Sdraiato',
                    'Elettrolitico Ø6,3 x 11 sdraiato, passo 2,5; + sul pin 1', el, rif_y=2.2, val_y=-7)


def impronte():
    out = {}
    for f in (impronta_esp, impronta_d24, impronta_ptc, impronta_ce):
        fp = f()
        out[fp[1] + '.kicad_mod'] = scrivi(fp) + '\n'
    return out


def principale(controlla):
    attesi = {os.path.join(LIB, 'hex2.kicad_sym'): simboli()}
    for nome, testo in impronte().items():
        attesi[os.path.join(LIB, 'hex2.pretty', nome)] = testo
    diversi = []
    for percorso, testo in attesi.items():
        if controlla:
            if not os.path.exists(percorso) or open(percorso, encoding='utf-8').read() != testo:
                diversi.append(percorso)
        else:
            with open(percorso, 'w', encoding='utf-8') as f:
                f.write(testo)
    if diversi:
        print('file diversi da quelli che darebbe propri.py:\n  ' + '\n  '.join(diversi))
        return 1
    print('%d file %s' % (len(attesi), 'controllati' if controlla else 'scritti'))
    return 0


if __name__ == '__main__':
    sys.exit(principale('--controlla' in sys.argv))
