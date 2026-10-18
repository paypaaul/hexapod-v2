# Versioni del robot

Ogni gruppo di modifiche è una versione: un tag git e un file Fusion proprio nel progetto "Hexabot v2". Le versioni chiuse restano congelate: i loro file Fusion non si modificano, e gli script lavorano solo sul design indicato in `cad/script/versione.py` (si rifiutano di girare sugli altri).

| Versione | Stato | Tag git | File Fusion (lineage) | Contenuto |
|---|---|---|---|---|
| 2.0.0 | congelata (9 ottobre 2026) | `v2.0.0` | "Hexapod v2 - MG996R", versione 28 (`urn:adsk.wipprod:dm.lineage:AVxbp0QWS5m_QEugpeB99A`) | zampa, corpo, assieme a sei zampe con giunti veri, passata estetica, tibia simmetrica sul piano della zampa, piedino in TPU, colori e render (D-047…D-065) |
| 2.1.0 | fatta (10 ottobre 2026) | `v2.1.0` | "Hexapod v2.1.0" (`urn:adsk.wipprod:dm.lineage:yQO8vfuxQ7uRcs6rnwK4_w`), copia della 2.0.0 versione 28; la 2.1.0 è la versione 5 del file | predisposizioni per sensori, luci, audio e computer di bordo; attrezzi da banco; software senza hardware (S0). Piano in `docs/piano-v2.1.0.md` |
| 2.1.1 | fatta (10 ottobre 2026) | `v2.1.1` | lo stesso "Hexapod v2.1.0" (correzioni piccole, senza copia), versione 7 | camera dell'anello Ø32 × 6 con il fondo e le sedi dei pixel, fermo dei fili sulla tibia, schema del cablaggio; striscia corretta in D-068 (2020 a 120 LED/m) (`docs/cablaggio.md`, D-067) |
| 2.1.2 | fatta (10 ottobre 2026) | `v2.1.2` | lo stesso "Hexapod v2.1.0", versione 10 | scelta delle predisposizioni (D-069: approvate e backlog), prese delle luci delle tibie, provino di luce, presa del T-plug verificata, tocco dai sensori esistenti (`software.md` 4.3b) |
| 2.1.3 | fatta (11 ottobre 2026) | `v2.1.3` | lo stesso "Hexapod v2.1.0", versione 11 | lame del femore come il guscio della tibia, chiuse su teste e mozzi, con la feritoia a intarsio nero; nessuna copertura superiore (D-070). Contatto fra vicine a 31°, massa attesa 3060,6 g, femore al 53 % |
| 2.1.4 | fatta (11 ottobre 2026) | `v2.1.4` | lo stesso "Hexapod v2.1.0", versione 12 | lame del femore con la sagoma del femore (teste esagonali e rialzo, come D-061) e l'estetica della 2.1.3; feritoia e viti della lama B a Z 1,5 (D-071). Carapace a 4,58 mm, massa attesa 3043,5 g |
| 2.1.5 | fatta (11 ottobre 2026) | `v2.1.5` | lo stesso "Hexapod v2.1.0", versione 13 | provino delle tasche della lama A (attrezzi) e render notturno con le luci accese (D-072); il robot non cambia |
| 2.1.6 | fatta (11 ottobre 2026) | `v2.1.6` | lo stesso "Hexapod v2.1.0", versione 14 | predisposizioni con i pezzi già in casa (D-074): GY-6500 su una piastrina sopra le bugne della Pololu, MS3625 con le lunette nella sede della Adafruit (doppia predisposizione), amplificatore generico con le bugne corrette, altoparlante tondo da 15 con il fermo; massa attesa 3045,0 g; carapace a 3,96 mm dalle zampe medie |
| 2.1.7 | fatta (16 ottobre 2026) | `v2.1.7` | lo stesso "Hexapod v2.1.0", versione 16 (la 15 è "2.1.7 in corso"); copia di ripristino della 2.1.6 in "Hexapod v2.1.0 - ripristino 2.1.6 (prima della 2.1.7)" (`urn:adsk.wipprod:dm.lineage:o79LLOHlSzmXdBn2HiYE1A`) | correzioni dalla guida di montaggio (D-076, D-077): vassoio su colonne con M2 svasate, fessure del tetto aperte, testata a 90° della scheda del carapace, ToF posteriore avvitato, rebbi sul pacco misurato, asola del bus a x 30, ESP32 a 25,4; lamatura e foro più profondo del guscio della tibia, sede luci da 50,5, gola da 4,5, stretta del piedino; dima del calettamento, provino degli inserti, bussola ed estrattore; correzioni della verifica geometrica. Vicine a contatto a 31° su quattro coppie, massa attesa 3046,2 g; calettamento a 100 con `gamma_max` dopo la taratura (P-015) |
| 2.1.8 | fatta (18 ottobre 2026) | `v2.1.8` | lo stesso "Hexapod v2.1.0", versione 20; copia di ripristino della 2.1.7 in "Hexapod v2.1.0 - ripristino 2.1.7 (prima della 2.1.8)" (`urn:adsk.wipprod:dm.lineage:lqTyF-0xTpm2y77ASTO6Tg`) | fase F2 del PCB (D-081): strisce del cavo piatto 1 mm più fuori (P-140); ali davanti della scheda del carapace fino a \|y\| 24; scheda dei partitori sotto le prese dei piedi con il pettine delle spine, sede delle prese tolta (D-080); ESP32 RE1.3 con il retro vero (microSD verso l'antenna, regolatore verso le USB). Massa attesa 3048,2 g. P-139 passa alla 2.1.9 |
| 2.1.9 | fatta (19 ottobre 2026), design di lavoro | `v2.1.9` | lo stesso "Hexapod v2.1.0", versione 23; copia di ripristino in "Hexapod v2.1.0 - ripristino 2.1.8 (prima della 2.1.9)" (`urn:adsk.wipprod:dm.lineage:Apmswd3aTvaSp-kx9JGvNg`, la versione 21) | ali della scheda del carapace da 5,5 (D-082); scheda dei partitori 33,8 × 8,6 (x 44,2…78, y 18,6…27,2) con l'angolo di testa smussato per uno spigolo della base, foro di testa a x 76,2, pettine a due file, 0805 e code dei pin sotto (D-084, D-085). Massa attesa 3048,2 g. P-139 passa alla versione dopo |

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
