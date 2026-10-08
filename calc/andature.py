#!/usr/bin/env python3
"""Confronto tra assetti (alto e raccolto, basso e largo) e andature (tripode, a coppie, a onda).

Domanda: conviene camminare "accucciati", con il ginocchio chiuso sotto i 90 gradi, o alti e raccolti?
Per ogni assetto e andatura lo script riporta: coppia statica massima in % dello stallo, angoli di
femore e ginocchio, alzata del piede che la zampa riesce a dare, margine di stabilita' e angolo di
ribaltamento.

Modello: come statica_tripode.py. Con piu' di tre piedi a terra il carico e' staticamente
indeterminato: si usa la ripartizione piana (corpo rigido su appoggi di uguale cedevolezza).
Semplificazione: tutti i piedi in appoggio alla stessa fase della corsa (si prende il caso peggiore).

Uso:  python3 calc/andature.py
"""
import math

from statica_tripode import CONFIG, ik_piano, piede_neutro, stallo_kgfcm

FONDO = 17.0          # fondo del corpo sotto l'asse dei femori (cor_h_sotto)
COM_SOTTO = 3.0       # baricentro sotto l'asse dei femori nell'assetto di marcia (dal modello)
GAMMA_MIN = 50.0      # angolo interno minimo al ginocchio (zampa con il puntone al posto dell'anima piena; era 62)
ALPHA_MAX = 55.0      # femore sopra l'orizzontale (era 25)
ZAMPE = ("AS", "MS", "PS", "AD", "MD", "PD")
ANDATURE = {
    "tripode (3 a terra)": [("AD", "MS", "PD"), ("AS", "MD", "PS")],                  # zampe sollevate
    "a coppie (4 a terra)": [("AS", "PD"), ("AD", "PS"), ("MS", "MD")],
    "a onda (5 a terra)": [(n,) for n in ZAMPE],
}
ASSETTI = [
    ("alto e raccolto (progetto)", 72.0, 12.0),
    ("medio", 58.0, 20.0),
    ("basso e largo (classico)", 40.0, 40.0),
    ("basso e raccolto", 40.0, 20.0),
]


def carichi(piedi, com, peso):
    """Carichi verticali su n >= 3 piedi: f_i = a + b x_i + c y_i con equilibrio di forze e momenti."""
    n = len(piedi)
    sx = sum(p[0] for p in piedi); sy = sum(p[1] for p in piedi)
    sxx = sum(p[0] ** 2 for p in piedi); syy = sum(p[1] ** 2 for p in piedi); sxy = sum(p[0] * p[1] for p in piedi)
    m = [[n, sx, sy], [sx, sxx, sxy], [sy, sxy, syy]]
    r = [peso, peso * com[0], peso * com[1]]
    for i in range(3):                       # eliminazione di Gauss con pivot
        piv = max(range(i, 3), key=lambda k: abs(m[k][i]))
        m[i], m[piv], r[i], r[piv] = m[piv], m[i], r[piv], r[i]
        for k in range(i + 1, 3):
            f = m[k][i] / m[i][i]
            m[k] = [a - f * b for a, b in zip(m[k], m[i])]
            r[k] -= f * r[i]
    x = [0.0] * 3
    for i in (2, 1, 0):
        x[i] = (r[i] - sum(m[i][k] * x[k] for k in range(i + 1, 3))) / m[i][i]
    return [x[0] + x[1] * p[0] + x[2] * p[1] for p in piedi]


def margine(piedi, com):
    """Distanza minima del baricentro dai lati dell'inviluppo convesso dei piedi (negativa = fuori)."""
    pts = sorted(set(piedi))
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    inf, sup = [], []
    for p in pts:
        while len(inf) >= 2 and cross(inf[-2], inf[-1], p) <= 0:
            inf.pop()
        inf.append(p)
    for p in reversed(pts):
        while len(sup) >= 2 and cross(sup[-2], sup[-1], p) <= 0:
            sup.pop()
        sup.append(p)
    hull = inf[:-1] + sup[:-1]
    m = 1e9
    for a, b in zip(hull, hull[1:] + hull[:1]):
        ln = math.hypot(b[0] - a[0], b[1] - a[1])
        m = min(m, cross(a, b, com) / ln)
    return m


def alzata_possibile(cfg):
    """Alzata massima del piede al neutro, restando dentro i limiti di ginocchio e femore della zampa."""
    best = 0.0
    for dz10 in range(0, 400):
        dz = dz10 / 10.0
        sol = ik_piano(cfg["x_f0"], cfg["h"] - dz, cfg["Lf"], cfg["Lt"])
        if sol is None or sol[3] < GAMMA_MIN or sol[0] > ALPHA_MAX:
            break
        best = dz
    return best


def valuta(cfg, sollevate_set, passi=21):
    peso = cfg["massa_g"] / 1000.0
    stallo = stallo_kgfcm(cfg["v_servo"])
    t_max, m_min, a_rng, g_rng, negativo = 0.0, 1e9, [1e9, -1e9], [1e9, -1e9], False
    for sollevate in sollevate_set:
        a_terra = [n for n in ZAMPE if n not in sollevate]
        for i in range(passi):
            d = -cfg["passo"] / 2 + cfg["passo"] * i / (passi - 1)
            piedi = [(piede_neutro(cfg, n)[0] - d, piede_neutro(cfg, n)[1]) for n in a_terra]
            f = carichi(piedi, cfg["com_xy"], peso)
            negativo = negativo or min(f) < -1e-9
            m_min = min(m_min, margine(piedi, cfg["com_xy"]))
            for n, p, fz in zip(a_terra, piedi, f):
                cx, cy, _ = cfg["coxa"][n]
                x_f = math.hypot(p[0] - cx, p[1] - cy) - cfg["Lc"]
                sol = ik_piano(x_f, cfg["h"], cfg["Lf"], cfg["Lt"])
                if sol is None:
                    return None
                alpha, xk, _, gamma = sol
                t_max = max(t_max, abs(fz * x_f) / 10.0, abs(fz * (x_f - xk)) / 10.0)
                a_rng = [min(a_rng[0], alpha), max(a_rng[1], alpha)]
                g_rng = [min(g_rng[0], gamma), max(g_rng[1], gamma)]
    return {"pct": t_max / stallo * 100, "margine": m_min, "alpha": a_rng, "gamma": g_rng, "negativo": negativo}


if __name__ == "__main__":
    print("Massa %g g, stallo %.1f kgf*cm, femore %g, tibia %g, passo %g mm"
          % (CONFIG["massa_g"], stallo_kgfcm(CONFIG["v_servo"]), CONFIG["Lf"], CONFIG["Lt"], CONFIG["passo"]))
    for nome, h, xf in ASSETTI:
        cfg = dict(CONFIG, h=h, x_f0=xf)
        r0 = valuta(cfg, ANDATURE["tripode (3 a terra)"])
        if r0 is None:
            print("\n%s: fuori portata" % nome)
            continue
        print("\n%s: asse a %g mm, luce %g mm, piede a %g mm dall'asse del femore" % (nome, h, h - FONDO, xf))
        print("  femore da %+.0f a %+.0f gradi, ginocchio da %.0f a %.0f gradi, alzata possibile %.0f mm"
              % (r0["alpha"][0], r0["alpha"][1], r0["gamma"][0], r0["gamma"][1], alzata_possibile(cfg)))
        for and_nome, sollevate in ANDATURE.items():
            r = valuta(cfg, sollevate)
            rib = math.degrees(math.atan2(r["margine"], h - COM_SOTTO))
            print("  %-22s coppia max %3.0f %%   margine %3.0f mm   ribaltamento a %2.0f gradi%s"
                  % (and_nome, r["pct"], r["margine"], rib, "   (un piede si scarica)" if r["negativo"] else ""))
