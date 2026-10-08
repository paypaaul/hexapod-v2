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

## D-046 — Struttura del design Fusion "Hexapod v2 - MG996R" (2026-10-08, fase 3)

- **Un solo file** per tutto il robot, nel progetto "Hexabot v2"; il vecchio "Hexapod v2 - Assieme" è stato rinominato "Hexapod v2 - MG90S" (richiesta dell'utente). La zampa **non** va in un file a parte: nella prima versione i riferimenti esterni hanno dato quasi tutti i problemi di posizione e di giunti bloccati (CLAUDE.md, note sul connettore). Sarà un componente `Zampa` istanziato sei volte, come nella prima versione.
- **Servo e regolatori importati da STEP dentro il design**, non come riferimenti esterni. Il servo è riportato nella **terna di progetto** con una lavorazione Sposta (`Terna_di_progetto`): origine sull'asse dell'albero al lato inferiore delle alette, +Z verso la cima dell'albero, cassa verso +X. Il lato inferiore delle alette è il riferimento perché dalle alette all'albero le tre fonti concordano entro 0,5 mm (D-045).
- **Le parti comprate sono componenti `Rif_*` nella zona libreria** (y ≥ 250 mm), fuori dall'ingombro del robot; nell'assieme se ne creano copie. Gli ingombri semplificati stanno in una BaseFeature, con le quote prese dai parametri utente: si rigenerano con `rif_componenti.py` → `ingombri` e `rigenera=True`.
- **Squadretta metallica**: il prodotto non è ancora scelto, quindi l'ingombro usa valori tipici dei rivenditori (disco Ø20, spessore 2,5, altezza con il mozzo 5,5, fori M3 a 14 mm), tutti C. Prima di stampare il provino si sostituiscono con le quote del prodotto comprato.
- **Batteria**: l'ingombro usa le quote massime delle schede (139 × 47,3 × 25,4) senza tolleranza; la tolleranza dichiarata (±5 / ±2 / ±2) è in parametri a parte e si aggiunge nel vano.

## D-047 — Architettura della zampa (2026-10-09, fase 4)

Scelta con un confronto tra tre architetture indipendenti ("scalata", "compatta", "robusta"), giudicate da tre revisori (verifica geometrica, struttura e montaggio, sistema). Tutto il materiale, compresi i calcoli dei revisori, è in `docs/ricerca/zampa-architetture.json`; il riassunto è in `progetto-meccanico.md`.

- **Base: "scalata"**, cioè l'architettura della prima versione portata sugli MG996R. Due revisori su tre la indicano come base; il terzo (struttura) la mette seconda dopo "robusta", che però pesa 117 g a zampa e porta femore e ginocchio oltre il 50 % per architettura. "Compatta" ha la coxa in un pezzo senza registro assiale e il femore chiuso da due sole viti.
- **Servo di coxa** nella gondola del corpo, albero in alto, coda verso l'esterno: il cavo esce già dentro lo scafo. Costa Lc = 55 (l'anima della coxa deve girare fuori dalla gondola, raggio 39,3 mm).
- **Servo del femore** nella coxa con la **coda in basso** (nella prima versione era in alto): con la coda in alto le culle lasciavano al femore una fascia di 8–10 mm; con la coda in basso resta libero un blocco cavo che chiude la sezione del femore.
- **Servo del ginocchio** nella tibia con la coda verso il piede.
- **Femore** in due piastre (squadrette da un lato, perni dall'altro) unite da un blocco cavo integrale con la piastra dei perni e avvitato all'altra con 4 viti M3.
- **Ponte della coxa** separato (braccio superiore della C): la squadretta a disco si avvita dall'alto e la sua altezza non è nota. Centrato sull'anima con una linguetta, non solo con le viti.
- **Lunghezze: coxa 55, femore 65, tibia 110** (prima 45 / 70 / 115). Con femore e tibia più corti le pose di tutte e sei le andature restano libere (gioco minimo 1,6 mm contro 1,1) e il ginocchio scende dal 39 al 34 % dello stallo; il femore resta al 49 % (non dipende dalle lunghezze). Femore da 60 scartato: urti nelle andature basse (`calc/zampa_escursioni.py`).
- **Smussi** sul ponte (3 mm) e in testa al blocco verso l'anca (6 mm): il femore sale fino a +80°.
- **Eccezione all'obiettivo delle escursioni**: con il femore tra −30° e 0° il ginocchio non chiude sotto 42–49° (lo stinco tocca le bugne della culla del femore, cioè il piede finirebbe sotto il corpo). Nessuna andatura usa quelle pose; il firmware limita γ in funzione di α. Il resto dell'obiettivo (femore da −30° a +65°, ginocchio fino a 150°) è libero.
- **Correzioni dei revisori adottate**:
  - braccio inferiore della coxa irrigidito con una nervatura sotto (prima portava al cuscinetto solo il 40–66 % del peso; il resto tirava l'albero del servo) e ponte sottile in verticale ma largo, così il peso del corpo passa quasi tutto dal cuscinetto;
  - registro assiale con rondelle M3 DIN 125 già nel BOM (voce D7) tra ponte e anima e tra piastra delle squadrette e blocco: nessuna voce nuova da comprare;
  - inserti delle alette spostati verso le estremità per lasciare almeno 1 mm verso la gola del fermacavo e 1,6 verso la sede del servo: al massimo 0,6 mm, perché la vite M3 deve restare dentro il foro Ø4,2 dell'aletta (l'asola è larga 2,5);
  - rialzo sull'anello interno Ø6,2 (diametro di riferimento interno dell'LF-1050ZZ 6,40);
  - spessori in multipli di 0,4; piastre del femore da 2,4 fuori dai mozzi;
  - perni Ø5 × 12 (la voce D2 del BOM diceva 16–20: si aggiorna la lunghezza, non è una voce nuova).
- **Vincoli per il corpo**: fondo della gondola 31,95 mm sotto l'asse dei femori, braccio della coxa fino a 38,35 (più la nervatura); ponte a 17–23 mm sopra l'asse; zampe vicine a contatto se ruotano entrambe di 30° una verso l'altra (in marcia ±17°): limite d'imbardata nel firmware o coxe più distanziate.

## D-048 — Giunto della coxa: il peso passa tutto dal cuscinetto (2026-10-09)

Il revisore della struttura ha trovato che nella proposta "scalata" il peso del corpo si divide tra il cuscinetto (braccio inferiore) e l'albero del servo di coxa (ponte avvitato alla squadretta), in proporzione alle rigidezze: al cuscinetto arrivava solo il 40–66 %, il resto tirava l'albero.

Soluzione: **il ponte non è avvitato alla squadretta**. Due viti M3 × 6 avvitate dall'alto nella squadretta a disco (con una rondella sotto la testa) sporgono con la testa; il ponte ha due fori Ø5,7 che calzano le teste e una sede per il disco con una luce di 0,3 mm sopra. La coppia passa dalle teste delle viti; in senso assiale il ponte è libero.

- In appoggio la zampa spinge in su: tutto il carico va dal braccio inferiore all'anello interno del cuscinetto e alla gondola; la luce sopra il disco si apre e l'albero non è tirato.
- In volo il peso della zampa (circa 2,6 N) appoggia il ponte sul disco: l'albero è spinto verso il servo, non tirato. Il gioco verticale della coxa è la luce sopra il disco (0,3 mm), regolabile con rondelle M3 sotto il ponte o ristampando il ponte (parametro `cox_disco_luce`).
- L'altezza della squadretta (non nota) non vincola più la pila: la recupera la luce.
- Il braccio inferiore porta tutto il peso: ha una nervatura sotto (freccia stimata sotto 0,1 mm con 11 N).
- Le forze orizzontali del momento ribaltante (circa 29 N) restano divise tra cuscinetto e albero: carico radiale sull'albero da provare sul provino.
- Il ponte si avvita all'anima con 2 M3 in inserti in una testa dell'anima che sta sopra la gondola (1,2 mm sopra la cassa del servo di coxa) ed è centrato da una linguetta.
