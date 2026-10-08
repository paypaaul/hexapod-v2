#!/usr/bin/env python3
"""Assetti possibili della zampa: altezza da terra, inclinazione del femore, coppia.

Risponde alla domanda "il corpo non e' troppo basso? e se il femore punta verso l'alto?".
Per ogni altezza h dell'asse del femore cerca la distanza neutra del piede x_f0 che minimizza
la coppia massima sul ciclo a tripode (stesso modello di statica_tripode.py) e riporta
l'inclinazione del femore in appoggio, la luce sotto il corpo e la coppia in % dello stallo.

Uso:  python3 calc/assetti.py            # zampa di progetto (femore 34, tibia 50)
      python3 calc/assetti.py 60 70 95   # anche con altre lunghezze di tibia
"""
import sys

from statica_tripode import CONFIG, valuta, verifica_volo

FONDO = 17.0        # fondo esterno del corpo sotto l'asse dei femori (parametro cor_h_sotto)


def migliore(cfg, h):
    """(coppia max % stallo, x_f0, ris) con la x_f0 che minimizza la coppia massima a questa altezza."""
    best = None
    for x10 in range(-100, 601, 5):
        c = dict(cfg, h=h, x_f0=x10 / 10.0)
        r = valuta(c, verbose=False)
        if r is None:
            continue
        t = max(r["t_femore"], r["t_tibia"]) / r["stallo"] * 100
        if best is None or t < best[0]:
            best = (t, c["x_f0"], r)
    return best


def tabella(lt):
    cfg = dict(CONFIG, Lt=float(lt))
    print("\nFemore %g mm, tibia %g mm, massa %g g, passo %g mm" % (cfg["Lf"], cfg["Lt"], cfg["massa_g"], cfg["passo"]))
    print("   h   luce  x_f0   femore in appoggio      coppia max   esito")
    for h in range(30, int(cfg["Lf"] + cfg["Lt"]) + 1, 4):
        b = migliore(cfg, float(h))
        if b is None:
            print("%4d  %4d    -    fuori portata" % (h, h - FONDO))
            continue
        t, x0, r = b
        a0, a1 = r["angoli"]["alpha"]
        verso = "in alto" if a0 > 5 else ("in basso" if a1 < -5 else "circa orizzontale")
        volo = verifica_volo(dict(cfg, h=float(h), x_f0=x0))
        nota = "" if volo else "  (alzata di %g mm non raggiungibile)" % cfg["alzata"]
        print("%4d  %4d  %4.1f   da %+4.0f a %+4.0f  %-18s  %3.0f %%   %s%s"
              % (h, h - FONDO, x0, a0, a1, verso, t, "ok" if t <= 50 else ("oltre il 50 %" if t < 100 else "OLTRE LO STALLO"), nota))


if __name__ == "__main__":
    for lt in ([CONFIG["Lt"]] + [float(a) for a in sys.argv[1:]]):
        tabella(lt)
