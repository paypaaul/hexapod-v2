"""Lunghezza dei percorsi dei cavi dei servo fino ai canali della SSC-32 (corpo v0.4).

Posizioni dei servo lette dal modello Fusion nella posa di riferimento (9 ottobre 2026): origine sull'asse
dell'albero al lato inferiore delle alette, asse x verso la cassa, asse z lungo l'albero. Il cavo esce dalla
cassa a (-15,25; 0; -23,5) nella terna del servo (STEP, fili compresi).

Percorso: il cavo del servo di coxa sale dalla culla nella baia e va sotto il coperchio fino al canale; quelli
di femore e ginocchio risalgono sopra la zampa, seguono femore e coxa a z 25, passano sopra l'asse della coxa
(dove l'imbardata cambia meno la lunghezza), entrano sotto il coperchio e arrivano al canale. Spine in alto,
file degli header a |y| 23,5 da x 10,3 a -39,4, sedici canali per lato.

Uso: python3 calc/cavi_servo.py [cavo_mm=300]
"""
import math
import sys

# zampa: servo -> (origine, asse x, asse z), asse della coxa
SERVO = {
    'AS': {'coxa': ((80, 44, 1.6), (0.866, 0.5, 0), (0, 0, 1)), 'femore': ((122.9, 79.7, 0), (0, 0, -1), (-0.5, 0.866, 0)),
           'ginocchio': ((179.2, 112.2, 0), (0, 0, -1), (-0.5, 0.866, 0)), 'asse': (80, 44)},
    'MS': {'coxa': ((0, 48, 1.6), (0, 1, 0), (0, 0, 1)), 'femore': ((-9.4, 103, 0), (0, 0, -1), (-1, 0, 0)),
           'ginocchio': ((-9.4, 168, 0), (0, 0, -1), (-1, 0, 0)), 'asse': (0, 48)},
    'PS': {'coxa': ((-80, 44, 1.6), (-0.866, 0.5, 0), (0, 0, 1)), 'femore': ((-132.4, 63.3, 0), (0, 0, -1), (-0.5, -0.866, 0)),
           'ginocchio': ((-188.6, 95.8, 0), (0, 0, -1), (-0.5, -0.866, 0)), 'asse': (-80, 44)},
    'AD': {'coxa': ((80, -44, 1.6), (0.866, -0.5, 0), (0, 0, 1)), 'femore': ((132.4, -63.3, 0), (0, 0, -1), (0.5, 0.866, 0)),
           'ginocchio': ((188.6, -95.8, 0), (0, 0, -1), (0.5, 0.866, 0)), 'asse': (80, -44)},
    'MD': {'coxa': ((0, -48, 1.6), (0, -1, 0), (0, 0, 1)), 'femore': ((9.5, -103, 0), (0, 0, -1), (1, 0, 0)),
           'ginocchio': ((9.5, -168, 0), (0, 0, -1), (1, 0, 0)), 'asse': (0, -48)},
    'PD': {'coxa': ((-80, -44, 1.6), (-0.866, -0.5, 0), (0, 0, 1)), 'femore': ((-122.9, -79.7, 0), (0, 0, -1), (0.5, -0.866, 0)),
           'ginocchio': ((-179.2, -112.2, 0), (0, 0, -1), (0.5, -0.866, 0)), 'asse': (-80, -44)},
}
CANALI = [10.3 - 1.27 - 2.54 * i for i in range(16)]          # x dei 16 canali di un lato
ASSEGNA = {'A': (0, 1, 2), 'M': (6, 7, 8), 'P': (13, 14, 15)}  # coxa, femore, ginocchio: zampe anteriori sui canali davanti
Z_CAVI = 25.0          # quota dei cavi sotto il coperchio (lato inferiore a 28,4)
CURVE = 1.15           # curve, fascette e scostamenti dalla linea retta (stima)
SCORTA = {'coxa': 0.0, 'femore': 20.0, 'ginocchio': 40.0}   # anse per imbardata (10), femore (10), ginocchio (20)


def _somma(a, b, k=1.0):
    return tuple(x + k * y for x, y in zip(a, b))


def uscita(t):
    o, x, z = t
    return _somma(_somma(o, x, -15.25), z, -23.5)


def percorso(zampa, servo):
    s = SERVO[zampa]
    lato = 1 if zampa[1] == 'S' else -1
    e = uscita(s[servo])
    ch = (CANALI[ASSEGNA[zampa[0]][('coxa', 'femore', 'ginocchio').index(servo)]], lato * 23.5, 22.7)
    sopra = (ch[0], lato * 30.0, Z_CAVI)
    p = [e, (e[0], e[1], Z_CAVI)]
    if servo == 'ginocchio':
        f = uscita(s['femore'])
        p.append((f[0], f[1], Z_CAVI))
    if servo != 'coxa':
        p.append((s['asse'][0], s['asse'][1], Z_CAVI))
    p += [sopra, ch]
    return sum(math.dist(a, b) for a, b in zip(p, p[1:])) * CURVE + SCORTA[servo], e


def main(cavo=300.0):
    print('cavo utile %.0f mm (32 cm dichiarati meno la spina)' % cavo)
    for zampa in SERVO:
        for servo in ('coxa', 'femore', 'ginocchio'):
            L, e = percorso(zampa, servo)
            print('%s %-9s uscita (%6.1f %6.1f %5.1f)  percorso %4.0f mm  margine %+4.0f mm (%+3.0f %%)'
                  % (zampa, servo, *e, L, cavo - L, 100 * (cavo - L) / cavo))


if __name__ == '__main__':
    kw = dict(a.split('=') for a in sys.argv[1:])
    main(float(kw.get('cavo_mm', 300)))
