"""Reti di KiCad contro le reti della guida (guida/schemi/sorgenti/*_def.py), piano-pcb.md 5.2.

I `*_def.py` restano la fonte delle reti: descrivono le millefori, con fori, ponticelli e fili. Da lì si
prendono solo i pin dei componenti e la loro rete. Le differenze volute della PCB (componenti tolti o aggiunti,
pin spostati su un'altra rete, nomi diversi) stanno in `pcb/aggiunte.yaml`; tutto il resto è un errore:
- un pin di un componente dei `*_def.py` che manca nello schema di KiCad;
- una rete dei `*_def.py` divisa in più reti di KiCad, o con un nome diverso;
- una rete di KiCad che unisce due reti dei `*_def.py`;
- un pin collegato in KiCad che i `*_def.py` lasciano libero;
- un componente di KiCad che non è né nei `*_def.py` né fra gli aggiunti.

Uso: python3 verifica_reti.py basetta pcb/basetta/basetta.net
"""

import fnmatch
import os
import re
import runpy
import sys

import yaml

from schema_kicad import leggi_netlist

RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SORGENTI = os.path.join(RADICE, 'guida', 'schemi', 'sorgenti')
AGGIUNTE = os.path.join(RADICE, 'pcb', 'aggiunte.yaml')
NON_COMPONENTI = ('ponte', 'filo', 'vite')
DEF = {'basetta': 'basetta', 'carapace': 'scheda', 'partitori': 'partitori'}  # progetto KiCad -> *_def.py

# Nome del pin nei *_def.py -> numero del pin del simbolo di KiCad
PIN_U2 = {'PG': '1', 'EN': '2', 'VIN': '3', 'GND': '4', 'VOUT': '5'}  # D24V22F5, ordine della pagina Pololu 2858
POLI = {'+': '1', '−': '2', '-': '2'}                                  # condensatori: pin 1 positivo


def _pin_u1(def_mod):
    """ESP32: pin 1-20 la fila ESP_L dalla coda alla testa, 21-40 la fila ESP_R nello stesso verso (piano 5.2)."""
    out = {n: str(i + 1) for i, n in enumerate(def_mod['ESP_L'])}
    out.update({n: str(i + 21) for i, n in enumerate(def_mod['ESP_R'])})
    return out


def carica_def(scheda):
    """{(ref, pin): rete} dei componenti della scheda nei *_def.py (pin liberi con rete None)."""
    sys.path.insert(0, SORGENTI)
    try:
        mod = runpy.run_path(os.path.join(SORGENTI, DEF[scheda] + '_def.py'))
    finally:
        sys.path.remove(SORGENTI)
    sch = next(v for v in mod.values() if type(v).__name__ == 'Scheda')
    pin_u1 = _pin_u1(mod) if 'ESP_L' in mod else {}
    ordine = {}
    nodi = {}
    for foro, (comp, nome, rete) in sch.pin.items():
        if comp in NON_COMPONENTI or foro in sch.nosald:
            continue
        m = re.match(r'^(\d+)\b', nome)
        if comp == 'U1' and pin_u1:
            pin = pin_u1[nome]
        elif comp == 'U2':
            pin = PIN_U2[nome]
        elif m:
            pin = m.group(1)
        elif nome in POLI:
            pin = POLI[nome]
        elif nome == '':
            # resistenze, diodi e condensatori a due fori: il primo foro è il pin 1 (per i diodi il catodo)
            ordine[comp] = ordine.get(comp, 0) + 1
            pin = str(ordine[comp])
        else:
            pin = nome
        k = 2
        base = pin
        while (comp, pin) in nodi:  # pin con lo stesso nome (le due masse del KAmod): GND, GND#2
            pin, k = '%s#%d' % (base, k), k + 1
        nodi[(comp, pin)] = rete
    return nodi


def carica_aggiunte(scheda, percorso=AGGIUNTE):
    with open(percorso, encoding='utf-8') as f:
        tutte = yaml.safe_load(f) or {}
    a = tutte.get(scheda) or {}
    return {
        'tolti': set(a.get('tolti') or []),
        'aggiunti': set(a.get('aggiunti') or []),
        'pin': {tuple(k.split('.', 1)): v for k, v in (a.get('pin') or {}).items()},
        'rinominate': dict(a.get('rinominate') or {}),
    }


def _nome(rete):
    return rete[1:] if rete.startswith('/') else rete


def verifica(scheda, net, nodi_def=None, aggiunte=None):
    """Elenco degli errori (vuoto se le reti tornano). `net` è il risultato di `leggi_netlist`."""
    nodi_def = carica_def(scheda) if nodi_def is None else nodi_def
    agg = carica_aggiunte(scheda) if aggiunte is None else aggiunte
    errori = []
    rete_kicad = {}
    for nome, nodi in net['reti'].items():
        for n in nodi:
            rete_kicad[n] = _nome(nome)
    libero = {n for n, r in rete_kicad.items() if r.startswith('unconnected-')}

    # rete attesa per ogni pin: dai *_def.py, poi le modifiche volute; '+NOME' è una rete solo della PCB
    attese = {}
    for (ref, pin), rete in nodi_def.items():
        if ref in agg['tolti']:
            continue
        attese[(ref, pin)] = rete
    for chiave, rete in agg['pin'].items():
        attese[chiave] = rete

    componenti_def = {ref for ref, _ in nodi_def} - agg['tolti']
    nuovi = {r for r in set(net['componenti']) - componenti_def
             if not any(fnmatch.fnmatchcase(r, m) for m in agg['aggiunti'])}
    for ref in sorted(nuovi):
        errori.append('%s è nello schema di KiCad ma né nei *_def.py né fra gli aggiunti' % ref)
    for ref in sorted(componenti_def - set(net['componenti'])):
        errori.append('%s dei *_def.py manca nello schema di KiCad' % ref)

    gruppi = {}  # rete attesa -> reti di KiCad
    for (ref, pin), rete in sorted(attese.items()):
        if ref not in net['componenti']:
            continue
        k = rete_kicad.get((ref, pin))
        if rete is None:
            if k is not None and (ref, pin) not in libero:
                errori.append('%s.%s è libero nei *_def.py ma in KiCad sta sulla rete %s' % (ref, pin, k))
            continue
        if k is None:
            errori.append('%s.%s (rete %s) non esiste nello schema di KiCad' % (ref, pin, rete))
            continue
        gruppi.setdefault(rete, set()).add(k)
    for rete, ks in sorted(gruppi.items()):
        nuova = rete.startswith('+')
        atteso = rete[1:] if nuova else agg['rinominate'].get(rete, rete)
        if len(ks) > 1:
            errori.append('la rete %s è divisa in KiCad: %s' % (rete, ', '.join(sorted(ks))))
        elif ks != {atteso}:
            errori.append('la rete %s in KiCad si chiama %s invece di %s' % (rete, next(iter(ks)), atteso))
    unite = {}
    for rete, ks in gruppi.items():
        for k in ks:
            unite.setdefault(k, set()).add(rete)
    for k, rr in sorted(unite.items()):
        if len(rr) > 1:
            errori.append('la rete %s di KiCad unisce le reti %s' % (k, ', '.join(sorted(rr))))
    # pin dei componenti dei *_def.py collegati in KiCad ma assenti dai *_def.py
    for (ref, pin), k in sorted(rete_kicad.items()):
        if ref in componenti_def and (ref, pin) not in attese and (ref, pin) not in libero:
            errori.append('%s.%s sta sulla rete %s in KiCad, ma nei *_def.py non c\'è' % (ref, pin, k))
    return errori


def principale(argv):
    scheda, file_net = argv[0], argv[1]
    errori = verifica(scheda, leggi_netlist(file_net))
    print('%s: %s' % (scheda, 'reti come la guida' if not errori else '%d errori' % len(errori)))
    for e in errori:
        print('  ' + e)
    return 1 if errori else 0


if __name__ == '__main__':
    sys.exit(principale(sys.argv[1:]))
