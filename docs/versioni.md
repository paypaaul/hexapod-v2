# Versioni del robot

Ogni gruppo di modifiche è una versione: un tag git e un file Fusion proprio nel progetto "Hexabot v2". Le versioni chiuse restano congelate: i loro file Fusion non si modificano, e gli script lavorano solo sul design indicato in `cad/script/versione.py` (si rifiutano di girare sugli altri).

| Versione | Stato | Tag git | File Fusion (lineage) | Contenuto |
|---|---|---|---|---|
| 2.0.0 | congelata (9 ottobre 2026) | `v2.0.0` | "Hexapod v2 - MG996R", versione 28 (`urn:adsk.wipprod:dm.lineage:AVxbp0QWS5m_QEugpeB99A`) | zampa, corpo, assieme a sei zampe con giunti veri, passata estetica, tibia simmetrica sul piano della zampa, piedino in TPU, colori e render (D-047…D-065) |
| 2.1.0 | fatta (10 ottobre 2026) | `v2.1.0` | "Hexapod v2.1.0" (`urn:adsk.wipprod:dm.lineage:yQO8vfuxQ7uRcs6rnwK4_w`), copia della 2.0.0 versione 28; la 2.1.0 è la versione 5 del file | predisposizioni per sensori, luci, audio e computer di bordo; attrezzi da banco; software senza hardware (S0). Piano in `docs/piano-v2.1.0.md` |
| 2.1.1 | fatta (10 ottobre 2026), design di lavoro | `v2.1.1` | lo stesso "Hexapod v2.1.0" (correzioni piccole, senza copia), versione 7 | camera dell'anello Ø32 × 6 con il fondo e le sedi dei pixel, fermo dei fili sulla tibia, schema del cablaggio; striscia corretta in D-068 (2020 a 120 LED/m) (`docs/cablaggio.md`, D-067) |

Prima della 2.0.0: la versione progettata attorno agli MG90S, nel branch `mg90s` e nel file "Hexapod v2 - MG90S".

## Avanzamento della 2.1.0

| Passo | Stato |
|---|---|
| Tag `v2.0.0`, copia del design Fusion, script legati a `versione.py` | fatto (9 ottobre 2026) |
| Blocco A — zampa | fatto e verificato (9 ottobre 2026, D-066): punta e piedino per l'FSR, gola e tasca dei fili, sede della striscia LED, diffusore, punti con nome |
| Blocco B — corpo | fatto e verificato (9 ottobre 2026, D-066): 2813, IMU, ADC, prese dei piedi, spie, ToF frontale e posteriore, INA260, anello del pulsante, luci dei lobi, zaino, audio |
| Blocco C — attrezzi da banco | fatto e verificato (10 ottobre 2026, D-066): due dime di posa per tutte le zampe e cavalletto |
| Blocco D — software S0 | fatto e verificato (9 ottobre 2026): stato in `docs/software.md` |
| Documenti, STL, render, tag `v2.1.0` | fatto (10 ottobre 2026): D-066, BOM (sezione X), STL con gli attrezzi, cinque render rifatti |
