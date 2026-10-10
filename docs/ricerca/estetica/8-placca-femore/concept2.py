"""Placca superiore del femore, variante 1 rifinita (scelta dell'utente del 10 ottobre 2026): finestra larga aperta verso
l'anca, ginocchiera sfaccettata come il guscio della tibia (piano in cima, smussi a 45 gradi da 4 mm, fianchi che scendono
sulle lame). Terna della zampa: anca a x 55, ginocchio a x 120, z 0 sugli assi, femore orizzontale.
Vincoli: interno della ginocchiera ad almeno 25 dall'asse del ginocchio (il guscio della tibia arriva a 24 in tutta la meta'
superiore); sopra l'anca solo |y| >= 25 (ponte della coxa |y| <= 12, culla della coxa fino a y -24,2)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'cad', 'render'))
from render import Scena

BIANCO = '#f2f2f2'
OUT = os.path.dirname(os.path.abspath(__file__)) + '/'
YB, SM, SP = 33.2, 4.0, 1.6           # esterno delle lame, smusso a 45 gradi, spessore
Z0 = 20.2                             # appoggio sulle lame e sul nero del femore (cima a z 20)
ZT = Z0 + SP                          # cima della cornice
ZK = 26.6                             # cima della ginocchiera: interno a 25 dall'asse del ginocchio
ZFIANCO = 16.0                        # i fianchi scendono sulle lame

def sezione(x, zt, yi, lati=(1, -1), giu=ZFIANCO):
    """Punti della sezione a C smussata alla stazione x: da |y| = yi all'esterno YB, cima zt, smusso SM a 45 gradi."""
    p = []
    for s in lati:
        p += [(x, s * yi, zt - SP), (x, s * yi, zt), (x, s * (YB - SM), zt), (x, s * YB, zt - SM), (x, s * YB, min(giu, zt - SM))]
    return p

def placca(s, anca_alta=False):
    # ginocchiera: rampa a 45 gradi dalla cornice, piano, smusso davanti; dentro a >= 25 dall'asse del ginocchio
    st = [(104.4, ZT), (109.2, ZK), (131.0, ZK), (135.6, ZK - 4.6)]
    s.solido([q for x, zt in st for q in sezione(x, zt, 0.0)], BIANCO, zampe=True)
    for lato in (1, -1):
        # binari ai lati della finestra (|y| 21..33,2), fino alla ginocchiera
        s.solido(sezione(62.0, ZT, 21.0, (lato,)) + sezione(104.4, ZT, 21.0, (lato,)), BIANCO, zampe=True)
        # anca: solo sopra piastre e lame (|y| >= 25), punta smussata a 45 gradi
        zt = ZK - 2.0 if anca_alta else ZT
        st = [(44.0, zt - SM), (48.0, zt), (62.0 if not anca_alta else 58.0, zt)]
        pts = [q for x, z in st for q in sezione(x, z, 25.0, (lato,))]
        if anca_alta:
            pts += sezione(62.0, ZT, 25.0, (lato,))
        s.solido(pts, BIANCO, zampe=True)

if __name__ == '__main__':
    for nome, alta in (('1r-anca-bassa', False), ('1r-anca-alta', True)):
        s = Scena(); s.nascondi('zampe_struttura_cover_tibia_diffusore')
        placca(s, alta)
        s.render(OUT + nome + '_zampa', viste=[(28, 55, 4.2), (6, 0, 4.2), (60, 100, 4.0)], centro=(0, 136, 0), larghezza=1100, altezza=800)
        if not alta:
            s.render(OUT + nome, viste=('iso_ant', 'fianco'), larghezza=1500, altezza=1000)
        print('fatto', nome)
