"""Gamma minimo equivalente delle varianti: il gamma a cui lo stinco della variante ha lo stesso gioco che lo stinco di
oggi ha al gamma minimo della tabella (dove il limite e' lo stinco contro la coxa)."""
import sys
sys.path.insert(0, '/Users/paul/.claude/jobs/3d86073b/tmp/estetica/v2_tibia')
import numpy as np
import geom as G
import stinco as S
from varianti import Z0
gam = G.gamba()
O = G.Ostacoli(gam)
oggi = G.campiona(np.concatenate(S.mesh('base')), 0.4)
for n in sys.argv[1:]:
    P = G.campiona(np.concatenate(S.mesh(n)), 0.4)
    for al in (-35, -25, -10, 0, 10, 25, 40):
        g0 = G.GMIN[al]
        d0 = O.distanza(G.posa_tibia(oggi, al, g0), al, (0,))[0]
        g = g0
        while g > 15:
            d = O.distanza(G.posa_tibia(P, al, g - 0.5), al, (0,))
            if d[0] < d0:
                break
            g -= 0.5
        print('%s alfa %+d: tabella %d (gioco di oggi %.2f) -> variante %.1f' % (n, al, g0, d0, g), flush=True)
