"""Lettura e scrittura delle S-espressioni dei file di KiCad (.kicad_sch, .kicad_sym, .kicad_pcb).

Un nodo è una lista; gli atomi sono `Sym` (parola nuda) o `str` (stringa fra virgolette).
Gira con il Python di KiCad (3.9) e con quello di sistema.
"""

import re


class Sym(str):
    """Atomo senza virgolette (parole chiave, numeri, yes/no)."""


_TOKEN = re.compile(r'\s*(?:(\()|(\))|"((?:[^"\\]|\\.)*)"|([^\s()"]+))', re.S)


def leggi(testo):
    """Restituisce il primo nodo del testo."""
    pila, radice, pos = [], None, 0
    while True:
        m = _TOKEN.match(testo, pos)
        if not m or m.end() == pos:
            break
        pos = m.end()
        aperta, chiusa, stringa, parola = m.groups()
        if aperta:
            nodo = []
            if pila:
                pila[-1].append(nodo)
            pila.append(nodo)
        elif chiusa:
            nodo = pila.pop()
            if not pila:
                radice = nodo
                break
        elif stringa is not None:
            pila[-1].append(re.sub(r'\\(.)', lambda c: {'n': '\n', 't': '\t'}.get(c.group(1), c.group(1)), stringa))
        else:
            pila[-1].append(Sym(parola))
    if radice is None:
        raise ValueError('S-espressione incompleta')
    return radice


def _atomo(a):
    if isinstance(a, Sym):
        return str(a)
    if isinstance(a, bool):
        return 'yes' if a else 'no'
    if isinstance(a, (int, float)):
        return num(a)
    s = str(a).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    return '"' + s + '"'


def num(x):
    """Numero come lo scrive KiCad: niente zeri inutili, al più 6 decimali."""
    s = ('%.6f' % x).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def scrivi(nodo, rientro=0):
    """Testo con il rientro a tabulazioni di KiCad: i nodi con figli vanno a capo."""
    if not isinstance(nodo, list):
        return _atomo(nodo)
    if all(not isinstance(x, list) for x in nodo):
        return '(' + ' '.join(_atomo(x) for x in nodo) + ')'
    tab = '\t' * (rientro + 1)
    i = 0
    while not isinstance(nodo[i], list):
        i += 1
    righe = ['(' + ' '.join(_atomo(x) for x in nodo[:i])]
    for x in nodo[i:]:
        righe.append(tab + scrivi(x, rientro + 1))
    righe.append('\t' * rientro + ')')
    return '\n'.join(righe)


def figli(nodo, nome):
    """Sotto-nodi con quel nome in testa."""
    return [x for x in nodo if isinstance(x, list) and x and x[0] == nome]


def figlio(nodo, nome):
    f = figli(nodo, nome)
    return f[0] if f else None


def S(*parole):
    """Comodità: S('at', 1, 2) -> [Sym('at'), 1, 2]."""
    return [Sym(parole[0])] + list(parole[1:])
