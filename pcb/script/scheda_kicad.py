"""Circuito stampato di KiCad 10 costruito da script con `pcbnew` (Python di KiCad, 3.9).

`kicad-cli` esporta la netlist ma non la porta nel PCB: lo fa questo modulo. Legge la netlist dello
schema, carica le impronte da pcb/librerie/hex2.pretty, dà a ogni impronta il percorso del simbolo
(così il DRC con --schematic-parity le riconosce) e a ogni piazzola la sua rete. Poi piste, vie,
riempimenti e contorno si aggiungono con le funzioni qui sotto, in mm.
"""

import os
import zlib

import pcbnew

import genera_contorni
from schema_kicad import netlist  # noqa: F401 (la usano i generatori delle schede)

IMPRONTE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'librerie', 'hex2.pretty'))


def mm(x):
    return pcbnew.FromMM(float(x))


def _strato(nome):
    """'F.Cu' -> pcbnew.F_Cu: GetLayerID vuole i nomi utente ('F.Silkscreen') e con gli altri dà UNDEFINED."""
    return getattr(pcbnew, nome.replace('.', '_'))


def punto(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


class Scheda:
    def __init__(self, net, percorso):
        """`net` è la netlist di `netlist()`; None per una scheda senza componenti (prove dei contorni)."""
        net = net or {'componenti': {}, 'reti': {}}
        # NewBoard apre il progetto accanto (.kicad_pro, con regole e classi di rete) e lo completa con i default
        self.percorso = percorso
        # identificativi ripetibili: rigenerare la stessa scheda dà lo stesso file, e il diff mostra solo le modifiche
        pcbnew.KIID.SeedGenerator(zlib.crc32(os.path.basename(percorso).encode()))
        self.board = pcbnew.NewBoard(percorso)
        self.board.SetCopperLayerCount(2)
        self.net = net
        self.reti = {}
        for nome in sorted(net['reti']):
            r = pcbnew.NETINFO_ITEM(self.board, nome)
            self.board.Add(r)
            self.reti[nome] = r
        self.impronte = {}
        rete_di = {(ref, pin): nome for nome, nodi in net['reti'].items() for ref, pin in nodi}
        for ref, c in sorted(net['componenti'].items()):
            lib, nome = c['impronta'].split(':')
            fp = pcbnew.FootprintLoad(IMPRONTE, nome)
            if fp is None:
                raise KeyError('impronta %s non trovata in %s' % (nome, IMPRONTE))
            # FootprintLoad legge tutta la libreria e consuma identificativi: si riparte da un seme per impronta, così
            # il file non cambia quando cambia il contenuto di hex2.pretty
            pcbnew.KIID.SeedGenerator(zlib.crc32(('%s/%s' % (os.path.basename(percorso), ref)).encode()))
            for el in [fp] + [x for g in (fp.Pads(), fp.GraphicalItems(), fp.GetFields(), fp.Zones(), fp.Groups()) for x in g]:
                el.ResetUuid()
            fp.SetFPID(pcbnew.LIB_ID(lib, nome))
            fp.SetReference(ref)
            fp.SetValue(c['valore'])
            fp.SetPath(pcbnew.KIID_PATH(c['percorso']))
            fp.SetSheetname(c['foglio'])
            fp.SetSheetfile(c['file_foglio'])
            # come "Aggiorna PCB dallo schema": campi e attributi del simbolo passano all'impronta
            for nome_campo, valore in c['campi'].items():
                if nome_campo not in ('Reference', 'Value', 'Footprint'):
                    fp.SetField(nome_campo, valore)
            fp.SetExcludedFromBOM(c['fuori_distinta'])
            fp.SetDNP(c['non_montare'])
            self.board.Add(fp)
            for pad in fp.Pads():
                nome_rete = rete_di.get((ref, pad.GetNumber()))
                if nome_rete:
                    pad.SetNet(self.reti[nome_rete])
            self.impronte[ref] = fp

    def rete(self, nome):
        """Rete per nome; le etichette locali del foglio radice si chiamano '/NOME'."""
        return self.reti.get(nome) or self.reti['/' + nome]

    def piazza(self, ref, x, y, angolo=0, retro=False, specchio='tb'):
        """Impronta in (x, y) di KiCad; con retro=True va sul lato B, specchiata sopra-sotto ('tb') o destra-sinistra ('lr')."""
        fp = self.impronte[ref]
        if retro and not fp.IsFlipped():
            fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT if specchio == 'lr' else
                    pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
        fp.SetPosition(punto(x, y))
        fp.SetOrientationDegrees(angolo)

    def pad(self, ref, numero):
        """Centro della piazzola in mm."""
        for p in self.impronte[ref].Pads():
            if p.GetNumber() == str(numero):
                c = p.GetPosition()
                return (pcbnew.ToMM(c.x), pcbnew.ToMM(c.y))
        raise KeyError('%s non ha la piazzola %s' % (ref, numero))

    def pista(self, rete, punti, larghezza=0.25, strato='F.Cu'):
        """Piste fra punti consecutivi; un punto può essere (x, y) o ('U1', '14')."""
        pp = [self.pad(*p) if isinstance(p[0], str) else p for p in punti]
        for a, b in zip(pp, pp[1:]):
            t = pcbnew.PCB_TRACK(self.board)
            t.SetStart(punto(*a))
            t.SetEnd(punto(*b))
            t.SetWidth(mm(larghezza))
            t.SetLayer(_strato(strato))
            t.SetNet(self.rete(rete))
            self.board.Add(t)

    def via(self, rete, x, y, diametro=0.8, foro=0.4):
        v = pcbnew.PCB_VIA(self.board)
        v.SetPosition(punto(x, y))
        v.SetWidth(mm(diametro))
        v.SetDrill(mm(foro))
        v.SetNet(self.rete(rete))
        self.board.Add(v)

    def contorno(self, punti):
        for a, b in zip(punti, punti[1:] + punti[:1]):
            s = pcbnew.PCB_SHAPE(self.board)
            s.SetShape(pcbnew.SHAPE_T_SEGMENT)
            s.SetStart(punto(*a))
            s.SetEnd(punto(*b))
            s.SetLayer(pcbnew.Edge_Cuts)
            s.SetWidth(mm(0.1))
            self.board.Add(s)

    def foro(self, x, y, diametro):
        """Foro non metallizzato, come cerchio sul contorno (Edge.Cuts)."""
        s = pcbnew.PCB_SHAPE(self.board)
        s.SetShape(pcbnew.SHAPE_T_CIRCLE)
        s.SetCenter(punto(x, y))
        s.SetEnd(punto(x + diametro / 2, y))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(mm(0.1))
        self.board.Add(s)

    def area_senza_rame(self, nome, strati, punti):
        """Area vietata a piste, vie, piazzole e riempimenti sugli strati dati."""
        z = pcbnew.ZONE(self.board)
        z.SetIsRuleArea(True)
        z.SetZoneName(nome)
        ls = pcbnew.LSET()
        for st in strati:
            ls.AddLayer(_strato(st))
        z.SetLayerSet(ls)
        z.SetDoNotAllowZoneFills(True)
        z.SetDoNotAllowTracks(True)
        z.SetDoNotAllowVias(True)
        z.SetDoNotAllowPads(True)
        z.SetDoNotAllowFootprints(False)
        contorno = z.Outline()
        contorno.NewOutline()
        for x, y in punti:
            contorno.Append(mm(x), mm(y))
        self.board.Add(z)
        return z

    def contorni_dal_cad(self, nome):
        """Contorno, fori Ø2,4 non metallizzati e zone senza rame della scheda, da genera_contorni."""
        g = genera_contorni.geometria(nome)
        self.contorno(g['contorno'])
        for _, x, y, d in g['fori']:
            self.foro(x, y, d)
        for nome_a, strati, punti in g['senza_rame']:
            self.area_senza_rame(nome_a, strati, punti)
        return g

    def riempimento(self, rete, punti, strato='B.Cu', distanza=0.3):
        z = pcbnew.ZONE(self.board)
        z.SetLayer(_strato(strato))
        z.SetNet(self.rete(rete))
        z.SetLocalClearance(mm(distanza))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        contorno = z.Outline()
        contorno.NewOutline()
        for x, y in punti:
            contorno.Append(mm(x), mm(y))
        self.board.Add(z)
        return z

    def testo(self, testo, x, y, strato='F.SilkS', altezza=1.0):
        t = pcbnew.PCB_TEXT(self.board)
        t.SetText(testo)
        t.SetPosition(punto(x, y))
        t.SetLayer(_strato(strato))
        t.SetTextSize(pcbnew.VECTOR2I(mm(altezza), mm(altezza)))
        t.SetTextThickness(mm(altezza * 0.15))
        if strato.startswith('B.'):
            t.SetMirrored(True)
        self.board.Add(t)

    def salva(self):
        filler = pcbnew.ZONE_FILLER(self.board)
        filler.Fill(self.board.Zones())
        self.board.Save(self.percorso)
        return self.percorso
