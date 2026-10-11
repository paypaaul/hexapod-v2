"""Placche del femore, quarta passata (11 ottobre 2026): l'utente sceglie le lame con la feritoia e scarta la linguetta
singola sull'anca ("piuttosto mettiamola più in avanti, altrimenti togliamola del tutto").
Verifiche sulle mesh (zampa MS, coxa a -35, 0, +35 gradi, alfa da -49 a 85), contro i 4,6 mm di oggi dal carapace (D-063):
- bordo superiore delle lame che sale verso il ginocchio: 1,4 mm dal carapace a alfa 85 e coxa a +-35; bordo dritto a
  z 20 con il rialzo a 45 gradi solo sul ginocchio (da x 105): 4,2 mm;
- striscia da lama a lama verso l'anca: tocca il ponte della coxa fino a x 78; da x 86 resta a 9,1 mm dal ponte e, se
  sta fra le lame (|y| <= 31, interno a z 20,2) invece che sopra, a 4,1-4,8 mm dal carapace; a x 82 scende a 2,6.
Due varianti: striscia a meta' femore (x 86-100) piu' quella del ginocchio, oppure solo quella del ginocchio."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from concept3 import BIANCO, OUT, Y0, YE, SP, lastra, Scena, terna_piano


def lame(s, meta):
    for lato in (1, -1):
        lastra(s, [(52, -14.5), (129, -14.5), (135.5, -8), (135.5, 20), (48, 20), (40, 12), (40, -3.5)], lato)
        lastra(s, [(97, -10), (135.5, -10), (135.5, 23), (131, 27.6), (113, 27.6), (97, 11.6)], lato)    # rialzo del ginocchio
        p = [(74 + 3.5 * math.cos(math.radians(a)), 3 + 3.5 * math.sin(math.radians(a))) for a in range(90, 271, 15)]
        p += [(104 + 3.5 * math.cos(math.radians(a)), 3 + 3.5 * math.sin(math.radians(a))) for a in range(-90, 91, 15)]
        y0, y1 = sorted((lato * (YE - 0.3), lato * (YE + 0.6)))
        s.prisma(p, y0, y1, '#1e1f22', asse='y', zampe=True)
    T = terna_piano((113.0, -YE + 1.0, 25.0), (1, 0, 0), (0, 1, 0))
    s.piastra([(0, 0), (14, 0), (14, 2 * YE - 2.0), (0, 2 * YE - 2.0)], T, spessore=SP, colore=BIANCO, bombatura=1.0, raggio_bordo=1.5, zampe=True)
    if meta:                                   # fra i bordi delle lame, non sopra: tiene il carapace a oltre 4 mm
        T = terna_piano((86.0, -Y0, 20.2), (1, 0, 0), (0, 1, 0))
        s.piastra([(0, 0), (14, 0), (14, 2 * Y0), (0, 2 * Y0)], T, spessore=SP, colore=BIANCO, bombatura=0.6, raggio_bordo=1.5, zampe=True)


if __name__ == '__main__':
    varianti = (('4-due-strisce', True), ('4-solo-ginocchio', False))
    for nome, meta in [v for v in varianti if len(sys.argv) < 2 or v[0] == sys.argv[1]]:
        s = Scena()
        s.nascondi('zampe_struttura_cover_tibia_diffusore', 'zampe_struttura_cover_femore')
        lame(s, meta)
        s.render(OUT + nome + '_zampa', viste=[(28, 55, 4.2), (10, 100, 4.2), (60, 100, 4.0)], centro=(0, 136, 0), larghezza=1100, altezza=800, lato=2.5)
        s.render(OUT + nome, viste=('iso_ant',), larghezza=1500, altezza=1000, lato=4.0)
        print('fatto', nome)
