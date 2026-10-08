# Registro delle decisioni — versione MG996R

Riparte da D-041. Le decisioni D-001…D-040 della versione MG90S sono in `docs/mg90s/decisioni.md` (e nel branch `mg90s`).

## Decisioni ereditate che restano valide

Riassunto; il perché è nel registro vecchio al numero indicato.

- **Controllo**: ESP32-S3-CAM UICPAL N16R8 RE1.3; camera OV3660 con flat da 75 mm, senza prolunghe (D-013, D-030); SSC-32 clone "V2.5" identificata dal link d'acquisto (D-030).
- **Seriale** ESP32 ↔ SSC-32 su UART1, TX GPIO21, RX GPIO14, 115200 baud, con traslatore di livello (D-012).
- **Logica separata dai servo**: regolatore da 5 V dedicato all'ESP32, interruttore a pulsante con pin OFF sul ramo logica e fusibile dedicato (D-008, D-020); ESP32 alimentata dal pin 5V con la USB-C come alternativa (D-028); elettronica sfusa su una basetta con zoccolo (D-023).
- **Nessun interruttore nel percorso di potenza dei servo**: rail spento di default e acceso dal firmware (D-019). Il principio resta; i componenti vanno ridimensionati.
- **Sottotensione su più livelli indipendenti** (D-011).
- **Materiali e stampa**: PETG-CF per le parti strutturali, non caricato per le cover; Creator 5 Pro con ugelli temprati da 0,4 mm; supporti ammessi dove servono (D-016, D-029, D-032).
- **Modellazione**: componenti comprati come STEP o ingombro da script, parti progettate con schizzi vincolati e parametri (D-031).
- **Porta USB** raggiungibile da uno sportello di servizio, senza prolunghe (D-034): vale il criterio, la soluzione si rivaluta sul corpo nuovo.
- **Assetto scelto a robot costruito**, meccanica che permette un campo ampio (D-039).

Non valgono più: tutto ciò che riguarda servo MG90S, regolatori Pololu da 11 A, batteria da 2200 mAh, cuscinetti F683ZZ, geometria delle zampe e del corpo (D-007, D-014, D-015, D-018, D-021, D-024…D-027, D-033, D-035…D-038).

## D-041 — Si costruisce la versione con gli MG996R; la versione MG90S è congelata (2026-10-08, decisione dell'utente)

L'utente aveva indicato per errore il file dell'MG90S: i servo voluti sono gli MG996R (AZDelivery) della sua v1. Si costruisce solo questa versione. La versione MG90S, coerente e verificata fino al ciclo a tripode, resta nel branch `mg90s` e nel design Fusion "Hexapod v2 - Assieme"; `main` diventa la versione grande. Indicazione esplicita: non limitare la versione grande per riusare la piccola; progettarla come si farebbe partendo da zero, cambiando qualunque scelta se serve.

## D-042 — Nuovo design Fusion per la versione MG996R (2026-10-08, concordata con l'utente)

Il vecchio design non è pesante (216 parametri, 81 voci di timeline), ma contiene parametri, componenti e storia di un altro robot. Un file nuovo tiene separati i due progetti e lascia intatta la versione congelata. Si crea all'inizio della fase 3. Da valutare lì: zampa in un file proprio, inserita per riferimento nell'assieme.
