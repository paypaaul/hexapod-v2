# Registro delle decisioni — versione MG996R

Riparte da D-041. Le decisioni D-001…D-040 della versione MG90S sono nel branch `mg90s` (`git show mg90s:docs/decisioni.md`).

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

## D-043 — Scelte dello studio per la versione MG996R (2026-10-08, proposte: si confermano con il BOM)

Dettagli e fonti in `studio-componenti.md` e `dimensionamento.md`.

- **Rail servo a 6,0 V** regolato: è la tensione della coppia dichiarata e sta dentro i campi di entrambe le fonti (AZDelivery fino a 7,2 V, Tower Pro fino a 6,6 V). Regolatore a tensione selezionabile, per poter provare 6,6–7,2 V al banco.
- **Alimentazione dimensionata su 15 A continui e 30 A di picco**, non sui 45 A di stallo totale: quel caso lo impedisce il firmware. Proposta: tre UBEC da 10 A, uno per coppia di zampe.
- **Potenza fuori dai morsetti della SSC-32**: saldatura sulle file degli header oppure basette di distribuzione; si sceglie con la foto del clone.
- **Fusibile principale da 30 A** (40 A se le misure lo chiedono), cavi da 12 AWG, T-plug. Batteria: la 5200 mAh dell'utente.
- **Punto di progetto preliminare**: 2,6 kg; asse dei femori a 100 mm, piede a 45 mm dall'asse; 50 % dello stallo dichiarato; ginocchio 63–78°. Giunti della zampa da progettare per femore da −30° a +65° e ginocchio da 40° a 150°, così il firmware può scegliere anche assetti più bassi.
- **Giunti**: cuscinetto flangiato con foro da 4 o 5 mm e perno coassiale al servo; squadrette metalliche a 25 denti consigliate (voce d'acquisto da approvare).
- **Nuovo criterio rispetto alla prima versione**: nessun vincolo di riuso. Verso dei servo, forma del corpo e divisione delle parti si decidono da capo nel CAD.

## D-044 — `main` contiene solo ciò che serve alla versione MG996R (2026-10-08, richiesta dell'utente)

Tolti da `main` i documenti, gli script, la ricerca e il report della versione MG90S: restano nel branch `mg90s`, pubblicato sul remoto. Su `main` restano lo studio e il dimensionamento nuovi, le dimensioni dei componenti (con i dati ancora validi di ESP32, SSC-32 e camera), il registro delle decisioni, gli script di calcolo riparametrizzati e due librerie Fusion generiche: `lib_cad.py` (provata) e `lib_assieme.py` (estratta dagli script provati, da ricontrollare al primo uso).

## D-045 — Risposte dell'utente e scelte per il BOM v2.0 (2026-10-08, sera; BOM approvato dall'utente)

Risposte dell'utente: non può misurare i servo (né quote né corrente di stallo); il buck della v1 non si usa; la SSC-32 si studia dalle immagini dell'inserzione; la batteria la dimensiono io; il modello 3D dell'MG996R lo cerco io o faccio un ingombro. Comprati finora: solo i servo e la SSC-32. Conseguenze:

- **Si progetta sul caso peggiore dei dati dichiarati**: 2,5 A di stallo (AZDelivery, contro 1,4 A di Tower Pro); per le quote, sedi che non dipendono da ciò su cui le fonti divergono. Le culle appoggiano il servo sulle alette e lasciano libero il fondo, perché sotto le alette la cassa è alta 26,6 o 28,8 mm secondo la fonte, mentre dalle alette all'albero le fonti concordano entro 0,5 mm. Prima delle parti vere si stampa un provino della culla e del giunto.
- **Modello 3D**: quello di HowToMechatronics (copia su GitHub), in `cad/modelli/mg996r/`. Confrontato con datasheet e tabella Tower Pro in `dimensioni-componenti.md`.
- **Alimentazione: due regolatori Pololu D42V110F6 invece dei tre UBEC proposti in D-043.** La SSC-32 ha due rail; con la potenza portata alle file degli header ognuno è un solo nodo elettrico e regge un solo regolatore. Il D42V110F6 ha il pin di abilitazione (rail spento di default, D-019), limita la corrente senza spegnersi e ha dati e modello del produttore; il D24V150F6 ha lo stesso ingombro e resta il ricambio più forte. Rail fisso a 6,0 V (si rinuncia a provare tensioni più alte).
- **Potenza dal retro della SSC-32**: filo stagnato da 1 mm saldato lungo le file VS e di massa di ogni lato, alimentato a metà fila. Le immagini mostrano header a foro passante; il retro non è fotografato e va guardato all'arrivo. SSC-32 su distanziali da almeno 8 mm.
- **Batteria: la OVONIC 2S 5200 mAh che l'utente ha.** 22–27 minuti di marcia classica stimati, 260 A ammessi, VL della SSC-32 alimentabile direttamente. Scartate una 2S più piccola (1–2 punti di coppia in meno, ma il 25–40 % di autonomia in meno e un acquisto) e una 3S (12,6 V oltre i 12 V del VL e un acquisto).
- **Giunti**: cuscinetto 5 × 10 × 4 (NMB LF-1050ZZ, verificato) e perno Ø5; squadretta in alluminio a 25 denti, da provare su un servo prima di comprarne 20.
