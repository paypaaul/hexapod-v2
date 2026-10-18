"""Copia nella libreria del progetto (pcb/librerie/hex2.*) i simboli e le impronte standard di KiCad usati.

Così i progetti non dipendono dalle librerie installate: la CI e un'altra versione 10.0.x di KiCad
leggono gli stessi pezzi. I pezzi disegnati da noi (ESP32, D24V22F5, Würth a 90°) stanno in
`hex2_propri.kicad_sym` e nei file `.kicad_mod` scritti a mano: questo script non li tocca.

Uso: python3 librerie.py            rigenera le copie
     python3 librerie.py --controlla  fallisce se le copie non sono uguali a quelle che darebbe la libreria installata
"""

import os
import sys

from schema_kicad import LIBRERIE_SIMBOLI, simbolo_libreria
from sexpr import S, Sym, scrivi

QUI = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(QUI, '..', 'librerie'))
IMPRONTE_KICAD = os.environ.get(
    'KICAD10_FOOTPRINT_DIR', os.path.join(os.path.dirname(LIBRERIE_SIMBOLI), 'footprints'))

SIMBOLI = [
    '74xx:74AHCT125',
    'Device:R',
    'Device:C',
    'Device:C_Polarized',
    'Device:D_Schottky',
    'Device:Polyfuse',
    'Connector_Generic:Conn_01x01',
    'Connector_Generic:Conn_01x02',
    'Connector_Generic:Conn_01x03',
    'Connector_Generic:Conn_01x04',
    'Connector_Generic:Conn_01x05',
    'Connector_Generic:Conn_01x14',
    'Connector_Generic:Conn_02x08_Odd_Even',
    'Connector:TestPoint',
    'Jumper:SolderJumper_2_Open',
    'Jumper:SolderJumper_3_Bridged12',
    'power:PWR_FLAG',
    'power:GND',
    'Interface_Expansion:TCA9534',
]

IMPRONTE = [
    'Package_DIP:DIP-14_W7.62mm',
    'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal',
    'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal',
    'Resistor_SMD:R_0805_2012Metric',
    'Capacitor_SMD:C_0805_2012Metric',
    'Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm',
    'Connector_PinHeader_2.54mm:PinHeader_1x01_P2.54mm_Vertical',
    'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
    'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical',
    'Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical',
    'Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical',
    'Connector_PinHeader_2.54mm:PinHeader_1x14_P2.54mm_Vertical',
    'Connector_IDC:IDC-Header_2x08_P2.54mm_Horizontal',
    'Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal',
    'Capacitor_THT:C_Disc_D3.8mm_W2.6mm_P2.50mm',
    'Package_SO:SOIC-16_3.9x9.9mm_P1.27mm',
    'TestPoint:TestPoint_THTPad_1.5x1.5mm_Drill0.7mm',
    'Jumper:SolderJumper-2_P1.3mm_Open_RoundedPad1.0x1.5mm',
    'Jumper:SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm',
]


def testo_simboli():
    radice = [Sym('kicad_symbol_lib'), S('version', 20251024), S('generator', 'hex2_librerie'),
              S('generator_version', '10.0')]
    for lib_id in SIMBOLI:
        sim = simbolo_libreria(lib_id)
        sim[1] = lib_id.split(':')[1]
        radice.append(sim)
    return scrivi(radice) + '\n'


def impronte():
    out = {}
    for lib_id in IMPRONTE:
        lib, nome = lib_id.split(':')
        with open(os.path.join(IMPRONTE_KICAD, lib + '.pretty', nome + '.kicad_mod'), encoding='utf-8') as f:
            out[nome + '.kicad_mod'] = f.read()
    return out


def principale(controlla):
    attesi = {os.path.join(LIB, 'hex2_kicad.kicad_sym'): testo_simboli()}
    for nome, testo in impronte().items():
        attesi[os.path.join(LIB, 'hex2.pretty', nome)] = testo
    diversi = []
    for percorso, testo in attesi.items():
        if controlla:
            if not os.path.exists(percorso) or open(percorso, encoding='utf-8').read() != testo:
                diversi.append(percorso)
        else:
            os.makedirs(os.path.dirname(percorso), exist_ok=True)
            with open(percorso, 'w', encoding='utf-8') as f:
                f.write(testo)
    if diversi:
        print('copie diverse dalla libreria installata:\n  ' + '\n  '.join(diversi))
        return 1
    print('%d file %s' % (len(attesi), 'controllati' if controlla else 'scritti'))
    return 0


if __name__ == '__main__':
    sys.exit(principale('--controlla' in sys.argv))
