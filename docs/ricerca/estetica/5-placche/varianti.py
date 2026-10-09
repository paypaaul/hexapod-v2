"""Quote delle tre versioni delle placche: Kabuto corretto (riferimento, piano), Morbida, Piena.

Terna della zampa: X verso l'esterno (anca X 55, ginocchio X 120), Y verso Femore_A, Z in alto. Lame nel piano (X, Z),
ginocchiera nel piano (Y, Z) sulla faccia +X della culla del ginocchio (X 132,45). Carapace in pianta nella terna del
robot. Tutte le quote in mm.
"""
import math

from geo import Placca, raccorda, esagono, cerchio

XH, XK = 55.0, 120.0
Y_FA, Y_FB = 30.55, -30.55                 # facce esterne di Femore_A e Femore_B (lette in Fusion, 9 ottobre)
Y_TESTE = 33.55                            # cima delle teste M3 sul lato A (30,55 + 3)
X_CULLA = 132.45                           # faccia +X della culla del ginocchio
VITI_BLOCCO = [(81, 4.5), (81, 12.9), (94.5, 6.0), (94.5, 13.4)]
SPINE_B = [(81, 6.0), (94.5, 6.0)]
TUBO_R, SEDE_R = 3.8, 2.8                  # tubi della lama A (D 7,6) e sedi delle teste (D 5,6)
T60 = math.tan(math.radians(60))


def _sagoma_kabuto(ap=14.0):
    ve = ap / math.cos(math.radians(30))
    gobba = [(75.58, ap), (99.92, ap), (96.46, 20.0), (79.04, 20.0)]
    return [(XH - ve, 0), (XH - ve / 2, -ap), (XK + ve / 2, -ap), (XK + ve, 0), (XK + ve / 2, ap),
            gobba[1], gobba[2], gobba[3], gobba[0], (XH - ve / 2, ap)]


def _sagoma_piena(ap=14.5):
    """Estremi esagonali (apotema 14,5) e gobba integrata: rampa a 30 gradi verso l'anca, plateau Z 20 da X 81 a 96,
    rampa a 45 gradi verso il ginocchio."""
    ve = ap / math.cos(math.radians(30))
    x1a = 81.0 - (20.0 - ap) / math.tan(math.radians(30))
    x1b = 96.0 + (20.0 - ap)
    return [(XH - ve, 0), (XH - ve / 2, -ap), (XK + ve / 2, -ap), (XK + ve, 0), (XK + ve / 2, ap),
            (x1b, ap), (96.0, 20.0), (81.0, 20.0), (x1a, ap), (XH - ve / 2, ap)]


GIN_K = [(-24.15, 13.65), (9.45, 13.65), (9.45, -9.25), (-7.35, -38.35), (-24.15, -9.25)]   # ginocchiera (Y, Z)


class Versione:
    def __init__(self, nome, sagoma, r_sagoma, ap_fin, r_fin, t_c, Rb, z_c, r_bordo, y_in_A,
                 gin_r, gin_tc, gin_Rb, gin_rb, car_r_conv, car_r_conc, car_r_top, car_r_rim, Rb2=0.0, x_c2=87.5,
                 gin_Rb2=0.0, gin_z_c2=0.0, tubi=True, passo=0.8):
        self.nome = nome
        self.contorno = raccorda(sagoma, r_sagoma) if any(r_sagoma) else sagoma
        self.sagoma = sagoma
        self.finestre = [raccorda(esagono((xc, 0), ap_fin), r_fin) if r_fin else esagono((xc, 0), ap_fin) for xc in (XH, XK)]
        self.ap_fin = ap_fin
        sedi = [cerchio(c, SEDE_R, 36, 0.07 * k) for k, c in enumerate(VITI_BLOCCO)]
        kw = dict(t_c=t_c, Rb=Rb, q_c=z_c, asse_q=1, r_bordo=r_bordo, Rb2=Rb2, q_c2=x_c2, passo=passo)
        self.tubi = tubi                           # lama A sospesa sui tubi (Kabuto, Morbida) o appoggiata (Piena)
        self.lama_A = Placca(self.contorno, self.finestre + sedi, **kw)
        self.lama_B = Placca(self.contorno, self.finestre, **kw)
        self.y_in_A = y_in_A                       # faccia interna della lama A
        self.y_in_B = Y_FB                         # la lama B appoggia sulla piastra
        self.gin_contorno = raccorda(GIN_K, gin_r) if any(gin_r) else GIN_K
        self.gin = Placca(self.gin_contorno, [], t_c=gin_tc, Rb=gin_Rb, q_c=-7.35, asse_q=0, r_bordo=gin_rb,
                          Rb2=gin_Rb2, q_c2=gin_z_c2, passo=passo)
        self.car = dict(conv=car_r_conv, conc=car_r_conc, top=car_r_top, rim=car_r_rim)
        self.par = dict(t_c=t_c, Rb=Rb, z_c=z_c, r_bordo=r_bordo, Rb2=Rb2, x_c2=x_c2, r_sagoma=r_sagoma, ap_fin=ap_fin, r_fin=r_fin,
                        gin_r=gin_r, gin_tc=gin_tc, gin_Rb=gin_Rb, gin_rb=gin_rb)

    def y_out_A(self):
        return self.y_in_A + self.lama_A.massimo()

    def y_out_B(self):
        return self.y_in_B - self.lama_B.massimo()

    def x_out_gin(self):
        return X_CULLA + self.gin.massimo()


def kabuto(**kw):
    return Versione('Kabuto corretto', _sagoma_kabuto(), [0] * 10, 11.0, 0, 1.2, 0, 3.0, 0.0, 32.35,
                    [0] * 5, 1.2, 0, 0.0, 0, 0, 0, 0, **kw)


def morbida(**kw):
    # tips R4, spalle R3, base della gobba (concava) R4, cima della gobba R3; finestre R1,5
    r = [4, 3, 3, 4, 3, 4, 3, 3, 4, 3]
    return Versione('Morbida', _sagoma_kabuto(), r, 11.0, 1.5,
                    t_c=2.0, Rb=180.0, z_c=3.0, r_bordo=0.6, y_in_A=Y_TESTE - 2.0,
                    gin_r=[2, 2, 8, 4, 8], gin_tc=2.0, gin_Rb=176.0, gin_rb=0.6,
                    car_r_conv=7.0, car_r_conc=5.0, car_r_top=0.0, car_r_rim=2.0, **kw)


def piena(**kw):
    # estremi a esagono quasi tondo (R8 su apotema 14,5: segue le teste del femore R13), rampe raccordate
    ap = 14.5
    sag = _sagoma_piena(ap)
    # bombatura doppia: 1,0 di traverso (Z da -14,5 a 20, cresta a Z 2,75) e 0,6 per lungo (cresta a X 87,5,
    # estremi a 48 mm): la lama scende verso i mozzi e accompagna le teste tonde del femore
    r = [8, 8, 8, 8, 8, 10, 8, 10, 10, 8]
    return Versione('Piena', sag, r, 11.0, 4.0,
                    t_c=2.6, Rb=17.25 ** 2 / 2.0, z_c=2.75, r_bordo=0.8, y_in_A=Y_FA,
                    Rb2=48.0 ** 2 / 1.2, x_c2=87.5, tubi=False,
                    gin_r=[4, 4, 14, 10, 14], gin_tc=2.4, gin_Rb=16.8 ** 2 / 2.0, gin_rb=0.8,
                    gin_Rb2=52.0 ** 2 / 1.0, gin_z_c2=-12.35,
                    car_r_conv=12.0, car_r_conc=10.0, car_r_top=0.0, car_r_rim=3.8, **kw)


VERSIONI = {'kabuto': kabuto, 'morbida': morbida, 'piena': piena}
