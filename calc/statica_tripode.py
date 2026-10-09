#!/usr/bin/env python3
"""Statica dell'esapode in andatura a tripode.

Calcola, per una geometria data:
  - il carico verticale sui 3 piedi in appoggio (equilibrio statico, 3 incognite);
  - la cinematica inversa della zampa nel suo piano verticale;
  - la coppia statica all'asse del femore e all'asse della tibia (ginocchio);
  - il confronto con il limite "coppia richiesta <= 50 % della coppia di stallo".

Convenzioni
  Terna corpo: x in avanti, y a sinistra, z in alto. Lunghezze in mm, masse in g.
  Zampa: asse coxa verticale in P; asse femore orizzontale a distanza Lc dall'asse
  coxa; ginocchio a Lf dall'asse femore; punta del piede a Lt dal ginocchio.
  alpha = angolo del femore sopra l'orizzontale (positivo = ginocchio in alto).
  x_f = distanza orizzontale del piede dall'asse femore, nel piano della zampa.
  h   = altezza dell'asse femore dal suolo.

Ipotesi (conservative dove possibile)
  - suolo piano, corpo orizzontale, nessuna accelerazione (il margine del 50 % copre la dinamica);
  - il peso proprio dei segmenti della zampa in appoggio non viene sottratto (conservativo);
  - forza al piede puramente verticale: la coppia statica alla coxa (asse verticale) e' nulla;
    la coppia alla coxa dovuta a forze orizzontali e' stimata a parte.

Uso:  python3 calc/statica_tripode.py            # valuta la configurazione CONFIG
      python3 calc/statica_tripode.py --scan     # esplora lunghezze e assetto
"""
import math
import sys

G = 9.80665  # m/s^2

# ----------------------------------------------------------------------------
# Servo MG996R (AZDelivery): coppia di stallo (kgf*cm) in funzione della tensione.
#   Datasheet AZDelivery e pagina Tower Pro: 9.4 a 4.8 V, 11 a 6.0 V (dichiarati; il reale va misurato).
#   Fonti in docs/studio-componenti.md
STALLO = {4.8: 9.4, 6.0: 11.0}


def stallo_kgfcm(v):
    """Interpolazione lineare tra i due punti (nessuna estrapolazione oltre 6.0 V)."""
    v = max(4.8, min(6.0, v))
    return STALLO[4.8] + (STALLO[6.0] - STALLO[4.8]) * (v - 4.8) / (6.0 - 4.8)


# ----------------------------------------------------------------------------
# Configurazione di riferimento = punto di progetto PRELIMINARE (vedi docs/dimensionamento.md).
# Lunghezze e posizioni degli assi sono stime da confermare con il CAD.
CONFIG = {
    "massa_g": 2910.0,          # massa attesa dopo la passata estetica (D-063: 2537 g modellati + 375 stimati); prima 2750
    "com_xy": (0.0, 0.0),       # baricentro nel piano, terna corpo
    "v_servo": 6.0,             # tensione del rail servo
    # assi coxa: nome -> (x, y, direzione neutra della zampa in gradi dall'asse longitudinale +x)
    "coxa": {    # D-050: disposizione del corpo "compatto"
        "AS": (80.0, 44.0, 30.0),     # anteriore sinistra
        "MS": (0.0, 48.0, 90.0),      # media sinistra
        "PS": (-80.0, 44.0, 150.0),   # posteriore sinistra
        "AD": (80.0, -44.0, -30.0),
        "MD": (0.0, -48.0, -90.0),
        "PD": (-80.0, -44.0, -150.0),
    },
    "Lc": 55.0,     # asse coxa -> asse femore (zampa D-047: anima della coxa fuori dalla gondola)
    "Lf": 65.0,     # asse femore -> asse ginocchio (D-047, verificato con calc/zampa_escursioni.py)
    "Lt": 110.0,    # asse ginocchio -> punta del piede (D-047)
    "x_f0": 45.0,   # piede neutro: distanza orizzontale dall'asse femore
    "h": 100.0,     # altezza asse femore dal suolo (assetto di marcia classico)
    "passo": 60.0,  # corsa del piede in appoggio (mm), simmetrica attorno al neutro
    "alzata": 30.0, # sollevamento del piede in volo (mm)
    "gamma_min": 36.0,  # ginocchio minimo: tabella GAMMA_MIN della zampa (33 a femore +30) piu 3 di margine
    "corsa_servo": 160.0,  # escursione utile di un servo (gradi), su 180 nominali
}

TRIPODI = (("AS", "PS", "MD"), ("AD", "PD", "MS"))


# ----------------------------------------------------------------------------
def risolvi3(a, b):
    """Risolve un sistema lineare 3x3 con la regola di Cramer."""
    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    d = det(a)
    if abs(d) < 1e-9:
        raise ValueError("piedi allineati: sistema singolare")
    out = []
    for k in range(3):
        m = [row[:] for row in a]
        for i in range(3):
            m[i][k] = b[i]
        out.append(det(m) / d)
    return out


def carichi_piedi(piedi, com, peso):
    """Carico verticale su 3 piedi (stessa unita' di `peso`). piedi: 3 tuple (x, y)."""
    a = [[1.0, 1.0, 1.0],
         [p[0] - com[0] for p in piedi],
         [p[1] - com[1] for p in piedi]]
    return risolvi3(a, [peso, 0.0, 0.0])


def ik_piano(x_f, h, lf, lt):
    """Cinematica inversa nel piano della zampa, soluzione a ginocchio alto.

    Ritorna (alpha_deg, x_ginocchio, z_ginocchio, gamma_deg) oppure None se fuori portata.
    gamma = angolo interno al ginocchio tra femore e tibia (180 = zampa distesa).
    """
    d = math.hypot(x_f, h)
    if d > lf + lt or d < abs(lf - lt) or d == 0:
        return None
    c = (lf * lf + d * d - lt * lt) / (2 * lf * d)
    c = max(-1.0, min(1.0, c))
    alpha = math.atan2(-h, x_f) + math.acos(c)
    xk, zk = lf * math.cos(alpha), lf * math.sin(alpha)
    cg = (lf * lf + lt * lt - d * d) / (2 * lf * lt)
    gamma = math.degrees(math.acos(max(-1.0, min(1.0, cg))))
    return math.degrees(alpha), xk, zk, gamma


def piede_neutro(cfg, nome):
    x, y, phi = cfg["coxa"][nome]
    r = cfg["Lc"] + cfg["x_f0"]
    return (x + r * math.cos(math.radians(phi)), y + r * math.sin(math.radians(phi)))


def valuta(cfg, passi=21, verbose=True):
    """Scorre la fase di appoggio dei due tripodi e riporta le coppie massime."""
    peso = cfg["massa_g"] / 1000.0  # kgf
    stallo = stallo_kgfcm(cfg["v_servo"])
    limite = 0.5 * stallo
    peggio = {"femore": 0.0, "tibia": 0.0, "carico": 0.0}
    ang = {"coxa": [1e9, -1e9], "alpha": [1e9, -1e9], "gamma": [1e9, -1e9]}
    righe = []
    for trip in TRIPODI:
        for i in range(passi):
            # d = avanzamento del corpo rispetto ai piedi fermi a terra
            d = -cfg["passo"] / 2 + cfg["passo"] * i / (passi - 1)
            piedi = []
            for n in trip:
                fx, fy = piede_neutro(cfg, n)
                piedi.append((fx - d, fy))
            try:
                f = carichi_piedi(piedi, cfg["com_xy"], peso)
            except ValueError:
                return None
            if min(f) < 0:
                return None  # baricentro fuori dal triangolo d'appoggio
            for n, p, fz in zip(trip, piedi, f):
                cx, cy, phi = cfg["coxa"][n]
                vx, vy = p[0] - cx, p[1] - cy
                r = math.hypot(vx, vy)
                yaw = math.degrees(math.atan2(vy, vx)) - phi
                yaw = (yaw + 180) % 360 - 180
                x_f = r - cfg["Lc"]
                sol = ik_piano(x_f, cfg["h"], cfg["Lf"], cfg["Lt"])
                if sol is None:
                    return None
                alpha, xk, zk, gamma = sol
                t_f = abs(fz * x_f) / 10.0          # kgf*cm
                t_t = abs(fz * (x_f - xk)) / 10.0   # kgf*cm
                peggio["femore"] = max(peggio["femore"], t_f)
                peggio["tibia"] = max(peggio["tibia"], t_t)
                peggio["carico"] = max(peggio["carico"], fz)
                for k, v in (("coxa", yaw), ("alpha", alpha), ("gamma", gamma)):
                    ang[k][0] = min(ang[k][0], v)
                    ang[k][1] = max(ang[k][1], v)
                righe.append((trip, d, n, fz, x_f, alpha, gamma, yaw, t_f, t_t))
    ris = {
        "stallo": stallo, "limite": limite,
        "t_femore": peggio["femore"], "t_tibia": peggio["tibia"],
        "carico_max_kgf": peggio["carico"], "carico_max_frazione": peggio["carico"] / peso,
        "angoli": ang, "righe": righe,
        "ok": max(peggio["femore"], peggio["tibia"]) <= limite,
    }
    if verbose:
        stampa(cfg, ris)
    return ris


def stampa(cfg, ris):
    print(f"Massa {cfg['massa_g']:.0f} g  |  rail servo {cfg['v_servo']:.1f} V  |  "
          f"stallo {ris['stallo']:.2f} kgf*cm  |  limite 50 % = {ris['limite']:.2f} kgf*cm")
    print(f"Lc {cfg['Lc']:.0f}  Lf {cfg['Lf']:.0f}  Lt {cfg['Lt']:.0f}  x_f0 {cfg['x_f0']:.0f}  "
          f"h {cfg['h']:.0f}  passo {cfg['passo']:.0f} mm")
    print(f"Carico massimo su un piede: {ris['carico_max_kgf']*1000:.0f} gf "
          f"({ris['carico_max_frazione']*100:.0f} % del peso)")
    for nome, t in (("femore", ris["t_femore"]), ("tibia ", ris["t_tibia"])):
        print(f"Coppia max {nome}: {t:.2f} kgf*cm = {t*G/100*1000:.0f} mN*m "
              f"= {t/ris['stallo']*100:.0f} % dello stallo  "
              f"[{'OK' if t <= ris['limite'] else 'OLTRE IL LIMITE'}]")
    a = ris["angoli"]
    print(f"Escursioni in appoggio: coxa {a['coxa'][0]:+.0f}..{a['coxa'][1]:+.0f} gradi, "
          f"femore {a['alpha'][0]:+.0f}..{a['alpha'][1]:+.0f}, ginocchio (interno) "
          f"{a['gamma'][0]:.0f}..{a['gamma'][1]:.0f}")
    volo = verifica_volo(cfg)
    if volo is None:
        print("Fase di volo: NON FATTIBILE (piede non raggiungibile, ginocchio troppo chiuso o corsa servo insufficiente)")
    else:
        print(f"Appoggio + volo (alzata {cfg['alzata']:.0f} mm): femore {volo['alpha'][0]:+.0f}..{volo['alpha'][1]:+.0f} gradi "
              f"(corsa {volo['alpha'][1]-volo['alpha'][0]:.0f}), ginocchio {volo['gamma'][0]:.0f}..{volo['gamma'][1]:.0f} "
              f"(corsa {volo['gamma'][1]-volo['gamma'][0]:.0f})")
    xf_max = max(abs(r[4]) for r in ris["righe"])
    m_coxa = ris["carico_max_kgf"] * (cfg["Lc"] + xf_max) / 10.0
    print(f"Momento flettente sul perno coxa (portato dai cuscinetti, non dal servo): fino a {m_coxa:.1f} kgf*cm")
    # raggio d'appoggio e margine di stabilita' del triangolo
    for trip in TRIPODI[:1]:
        pts = [piede_neutro(cfg, n) for n in trip]
        print("Piedi tripode A (neutro):", ", ".join(f"{n}=({p[0]:.0f},{p[1]:.0f})" for n, p in zip(trip, pts)))
        print(f"Margine di stabilita' minimo (distanza baricentro-lato del triangolo, su tutta la corsa): "
              f"{margine_stabilita(cfg):.0f} mm")


def margine_stabilita(cfg, passi=21):
    """Distanza minima del baricentro dai lati del triangolo d'appoggio lungo la corsa."""
    m = 1e9
    com = cfg["com_xy"]
    for trip in TRIPODI:
        for i in range(passi):
            d = -cfg["passo"] / 2 + cfg["passo"] * i / (passi - 1)
            p = [(piede_neutro(cfg, n)[0] - d, piede_neutro(cfg, n)[1]) for n in trip]
            for k in range(3):
                a, b, c = p[k], p[(k + 1) % 3], p[(k + 2) % 3]
                ex, ey = b[0] - a[0], b[1] - a[1]
                ln = math.hypot(ex, ey)
                # distanza con segno, positiva dal lato del terzo vertice
                s = ((com[0] - a[0]) * ey - (com[1] - a[1]) * ex) / ln
                sc = ((c[0] - a[0]) * ey - (c[1] - a[1]) * ex) / ln
                m = min(m, s if sc > 0 else -s)
    return m


def verifica_volo(cfg, passi=9):
    """Fase di volo: il piede percorre la stessa corsa sollevato di `alzata`.

    Ritorna None se un punto non e' raggiungibile o viola gamma_min, altrimenti
    le escursioni (alpha, gamma) su appoggio + volo, da confrontare con la corsa del servo.
    """
    amin, amax, gmin, gmax = 1e9, -1e9, 1e9, -1e9
    for n in cfg["coxa"]:
        cx, cy, phi = cfg["coxa"][n]
        fx, fy = piede_neutro(cfg, n)
        for i in range(passi):
            d = -cfg["passo"] / 2 + cfg["passo"] * i / (passi - 1)
            x_f = math.hypot(fx - d - cx, fy - cy) - cfg["Lc"]
            for dz in (0.0, cfg["alzata"]):
                sol = ik_piano(x_f, cfg["h"] - dz, cfg["Lf"], cfg["Lt"])
                if sol is None:
                    return None
                alpha, _, _, gamma = sol
                if gamma < cfg["gamma_min"]:
                    return None
                amin, amax = min(amin, alpha), max(amax, alpha)
                gmin, gmax = min(gmin, gamma), max(gmax, gamma)
    if amax - amin > cfg["corsa_servo"] or gmax - gmin > cfg["corsa_servo"]:
        return None
    return {"alpha": (amin, amax), "gamma": (gmin, gmax)}


def sollevamento(cfg, m_fuori_g, d_com_mm):
    """Coppia al femore per tenere sollevata una zampa in volo (massa a valle x braccio)."""
    return m_fuori_g / 1000.0 * d_com_mm / 10.0


def con_layout(base, xc, yc, ym, phi):
    """Esagono allungato: zampe d'angolo in (+-xc, +-yc) orientate a phi da x, medie in (0, +-ym)."""
    c = {"AS": (xc, yc, phi), "MS": (0.0, ym, 90.0), "PS": (-xc, yc, 180.0 - phi),
         "AD": (xc, -yc, -phi), "MD": (0.0, -ym, -90.0), "PD": (-xc, -yc, -(180.0 - phi))}
    return dict(base, coxa=c)


def scan(base, lc_list=(40, 50, 60), stampa_n=20):
    """Esplora Lc, Lf, Lt, x_f0, h; scarta cio' che non cammina; ordina per coppia massima."""
    out = []
    for lc in lc_list:
        for lf in range(55, 91, 5):
            for lt in range(90, 141, 10):
                for xf0 in range(20, 81, 10):
                    for h in range(60, 131, 10):
                        cfg = dict(base, Lc=float(lc), Lf=float(lf), Lt=float(lt), x_f0=float(xf0), h=float(h))
                        r = valuta(cfg, passi=7, verbose=False)
                        if r is None:
                            continue
                        volo = verifica_volo(cfg, passi=5)
                        if volo is None:
                            continue
                        out.append((max(r["t_femore"], r["t_tibia"]), lc, lf, lt, xf0, h, r, volo))
    out.sort(key=lambda t: (round(t[0], 2), t[5]))
    print(f"{len(out)} configurazioni che camminano. Migliori {stampa_n}:")
    print("  tmax   Lc   Lf   Lt  x_f0   h   t_fem  t_tib   femore(min..max)  ginocchio(min..max)  carico")
    for t, lc, lf, lt, xf0, h, r, v in out[:stampa_n]:
        print(f"  {t:4.2f}  {lc:3d}  {lf:3d}  {lt:3d}  {xf0:3d}  {h:3d}   {r['t_femore']:4.2f}   {r['t_tibia']:4.2f}"
              f"    {v['alpha'][0]:+4.0f}..{v['alpha'][1]:+4.0f}       {v['gamma'][0]:4.0f}..{v['gamma'][1]:4.0f}"
              f"        {r['carico_max_frazione']*100:3.0f} %")
    return out


if __name__ == "__main__":
    if "--scan" in sys.argv:
        scan(CONFIG)
    else:
        valuta(CONFIG)
