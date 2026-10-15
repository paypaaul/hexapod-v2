# Generatori degli schemi delle schede (F3b, D-075)

Gli SVG di `guida/schemi/` vengono da questi script, scritti dal progettista degli schemi il 12 ottobre 2026. Rigenerano
gli stessi file:

```
cd guida/schemi/sorgenti
../../../.venv/bin/python disegno_basetta.py      # basetta.svg e basetta_saldature.svg
../../../.venv/bin/python disegno_scheda.py       # scheda_carapace.svg e scheda_carapace_saldature.svg
../../../.venv/bin/python disegno_partitori.py    # partitori.svg e partitori_saldature.svg (P-006, 15 ottobre 2026)
../../../.venv/bin/python verifica.py             # reti chiuse, niente corti, zone vietate libere
../../../.venv/bin/python tabelle.py              # tabelle delle reti e dei fili per schemi.md
../../../.venv/bin/python png.py basetta          # PNG da guardare, nella cartella temporanea
```

- `basetta_def.py`, `scheda_def.py` e `partitori_def.py`: componenti, reti, fili e ponticelli delle tre schede (la fonte
  di verita').
- `modello.py`: griglia, instradamento dei fili, controlli di vicinanza.
- `fili_b.py`, `cerca_b.py`: ricerca dell'ordine dei fili della basetta; il risultato e' in `ordine_b.txt` e `ordine_s.txt`.
- `svgbase.py`, `disegno*.py`: disegno in mm, scala nei titoli degli SVG.
- `md.py`, `check_md.py`: fonti delle reti e controllo che `schemi.md` concordi con i disegni.
