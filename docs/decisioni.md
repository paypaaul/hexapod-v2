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

## D-049 — Correzioni della zampa dopo la revisione (2026-10-09)

Quattro revisori indipendenti (montaggio, stampa e struttura, quote, sistema) hanno controllato la zampa v0 sul modello; i rilievi completi sono in `ricerca/zampa-v0-revisione.json`. Corretti nel modello:

- **Il servo non entrava nella culla** (bloccante, trovato da due revisori): il passacavo rigido dell'MG996R sporge 5 mm dalla testata e non passava tra l'orlo e la finestra del cavo; per lo stesso motivo un servo rotto non sarebbe uscito. Ora una **fessura larga 6,7 mm** scende dall'orlo alla finestra attraverso la testata lato albero. Gli inserti M3 di quel lato non ci stavano più: le due viti delle alette lato albero sono **M3 avvitate in fori pilota Ø2,5** (autofilettanti nella plastica), spostate di 0,6 mm verso l'esterno dentro il foro Ø4,2 dell'aletta; lato coda restano gli inserti. Nessuna voce nuova.
- **La rondella sotto le teste delle viti della squadretta di coxa** (D-048) impediva al ponte di scendere nella sua sede (bloccante): **niente rondella, viti M3 × 5**. Con M3 × 6 la punta arriverebbe a 0,1 mm dalla torretta del servo. Il BOM elencava viti M3 da 6 a 25 mm: servono 12 viti M3 × 5 (da confermare con l'utente).
- **Collo di 2,4 mm tra braccio e culla della coxa** (alta): sotto la coda di ogni culla c'è ora uno **zoccolo pieno** che lega pareti, fondo, bugne e braccio; nella tibia lega anche lo stinco, che prima si attaccava alla sola parete di coda.
- **La spalla della sede del cuscinetto toccava l'anello interno** (il foro dietro era Ø6, l'anello interno arriva a 6,4): foro portato a Ø7,2.
- **Nervatura della coxa sospesa in stampa**: ora va dal piano medio fino al piano di stampa, alta 3 mm (non serve più per la ripartizione del carico, D-048).
- **Inserti del ponte con fondo di 0,55 mm**: la testa dell'anima scende fino a 1 mm sopra le teste delle viti lato coda del servo di coxa (dove la cassa del servo non c'è, a raggio 34–40 dalla coxa) e gli inserti hanno la profondità piena; spostati in modo che le teste delle viti non cadano sullo smusso del ponte.
- **Inserto del blocco del femore a 1,4 mm dallo smusso**: abbassato di 0,6 mm (parete 1,9).
- Anima della coxa da 4,0 mm (gioco dalla gondola 1,2 invece di 0,8); finestre a rombo più piccole (ponte di 2,5 mm tra le due).
- **Assi fuori asse** (alta, probabile): la sede centra la cassa, non l'albero, e il giunto è sostenuto su due lati. Rimedio di montaggio: le viti delle alette si stringono **per ultime**, a femore montato, così il servo si allinea al cuscinetto dentro i giochi della sede (0,2 mm per lato) e dei fori delle alette.
- Restano aperti, da chiudere con il provino o con il corpo: gioco d'imbardata della coxa tra teste delle viti e fori Ø5,6 (da tarare), perni forzati senza ritegno assiale (perni h8 scorrevoli nei cuscinetti; m6 solo se provati), parete di 1,15 mm nel ponte tra foro centrale e fori delle teste, lunghezza del cavo del ginocchio delle zampe d'angolo, massa reale (circa 2,75 kg con la viteria: femore al 52 %).

## D-050 — Disposizione del corpo (2026-10-09, fase 4)

Tre disposizioni indipendenti ("compatto", "accessibile", "stabile") giudicate da tre revisori (ingombri e interferenze, struttura e manutenzione, sistema); tutto in `ricerca/corpo-disposizioni.json`. **Base: "compatto"**, scelto all'unanimità (7/10 per tutti e tre): unica con margine vero sul piatto (base 235 × 173), cavi dei servo più corti, T-plug e USB a portata, massa realistica. "Accessibile" ha il cambio batteria che non funziona come descritto; "stabile" ha zampe d'angolo che si toccano a 26,6° e la SSC-32 sepolta sotto 20 viti.

- **Assi delle coxe**: d'angolo (±80, ±44) a ±30° e ±150° dall'asse longitudinale; medie (0, ±48) a ±90°. Coppia al femore 48 % a 2,75 kg (52 % con le posizioni provvisorie), ginocchio 44 %, margine di stabilità 59 mm. Zampe vicine a contatto a 32,5° ciascuna verso l'altra: limite nel firmware (somma delle imbardate di due vicine entro 60°).
- **Struttura**: tunnel chiuso della batteria al centro (interno 162 × 50 × 28), gondole attaccate ai fianchi, quattro baie laterali tra le gondole. `Corpo_Base` in PETG-CF stampato con il fondo sul piatto (da z −31,95 a +7), `Corpo_Chiglia` sotto il tunnel (fino a −41,4, quota della nervatura della coxa: la luce resta quella della zampa), coperchio non strutturale in PETG fino a +30, vassoio dell'ESP32 e muso in PETG (antenna e camera fuori dal carbonio), sportello della batteria a scatto sul retro.
- **Pila in altezza**: batteria da −39,4 a −12; tetto del tunnel −11,4…−9,4; SSC-32 su bugne alte 8 sul tetto; vassoio a +1…+2,6; basetta a +5,9; ESP32 a +16; camera con asse a +22,5; coperchio da +28,4 a +30.
- **Correzioni dei revisori da applicare nel modello**: viti della chiglia fuori dagli ingombri di regolatori e fusibile; F1 nel vano di coda accanto al T-plug (raggiungibile senza togliere il coperchio); parete anteriore del tunnel aperta dove passano vassoio e basetta; regolatori su bugne esterne o slitte, non con viti nel vano della batteria; finestra della gonna del coperchio ad almeno 22 mm dagli assi delle coxe; ingressi dei Wago verso l'esterno; baie anteriori libere come camino d'aria dei regolatori (scorte di cavo nelle baie posteriori); 12 AWG sotto la SSC-32 dal lato posteriore; giochi sotto 1 mm come parametri; labbro di centraggio tra chiglia e base; viti della SSC-32 M2 con rondella oppure M2,5.
- **Firmware**: imbardata assoluta entro ±30°, somma tra vicine entro 60°, γ minimo dalla tabella della zampa più 3°, piede neutro delle zampe d'angolo 5 mm più fuori negli assetti 80/60 e 70/70.
- **Da confermare**: area utile della Creator 5 Pro con zona di spurgo; misure col calibro di batteria, SSC-32 e camera prima di stampare la base; 4 prolunghe dei servo per i ginocchi (voce C5).

## D-051 — Correzioni del corpo dopo la revisione (2026-10-09)

Quattro revisori (montaggio, stampa e struttura, quote, sistema) hanno controllato il corpo v0.2 sul modello: 39 rilievi in `ricerca/corpo-v0-revisione.json`. Corretti nel modello (corpo v0.3):

- **La batteria non si sfilava dal retro** (bloccante): le viti posteriori della chiglia stavano dentro il tunnel. Ora sono sotto le baie posteriori (orecchie della chiglia a x −52, |y| 31, inserti in bugne sul ripiano). Verificato facendo scorrere il pacco fino a 160 mm fuori: nessun urto.
- **Gondole legate al tunnel solo dal ripiano da 2 mm** (bloccante): pareti di collegamento fino al tetto (le fiancate delle gondole medie prolungate fino al tunnel, una paratia per ogni gondola d'angolo). Formano celle chiuse con tunnel, ripiano e parete della baia.
- **F1 copriva la fessura dei cavi**: due fessure nel tetto accanto ai capi del portafusibile (|y| da 20,5 a 25). La coppia di T-plug sta sopra F1, nel vano di coda: si raggiunge dal retro senza aprire nulla.
- **Regolatori**: gli inserti non si potevano posare e le viti non si raggiungevano, e le bugne erano 1,016 mm fuori asse (i fori del Pololu non sono centrati: a 4,191 mm dal lato delle piazzole, letti dallo STEP). Ora ogni regolatore sta su una **slitta stampata** (inserti M2 posati al banco), che scende tra due guide sulla parete della baia e si ferma con una vite M3 orizzontale sopra il circuito. Componenti verso il tunnel, 4,8 mm d'aria.
- **Flat della camera senza percorso**: camera girata di 180° sull'asse ottico, il flat esce dall'alto della testa e torna verso l'ESP32 sopra la torretta (abbassata all'asse ottico) e sopra il modulo dell'antenna.
- **Vassoio non fissato**: quattro distanziali M3 maschio-femmina da 5 mm (voce B18, che non serviva più per la SSC-32) su bugne del tetto con inserti.
- **Wago sotto il vassoio** (leve inaccessibili): spostati sul ripiano delle baie posteriori.
- **USB-C e pulsanti dell'ESP32 non raggiungibili**: apertura di servizio nel dorso del coperchio con uno sportellino a cornice.
- **SSC-32**: inserti M2 nelle bugne del tetto al posto dei fori pilota (la scheda si smonta spesso); viti M2 con testa da 3,8 sui fori da 3,0.
- **Orecchie anteriori della chiglia** a tutta altezza (prima erano a sbalzo); niente teste di vite sotto il fondo.
- **Copie nascoste** lasciate alla radice da ogni lancio di `istanze_corpo`: ora si cancellano.
- **Da fare o da provare**, non corretti: smussi o supporti sotto le 12 bugne delle gondole (le bugne sono sbalzi piatti a 25,6 mm dal piatto: supporti con interfaccia), chiglia avvitata solo in quattro punti (sezione chiusa del tunnel solo dove le viti la stringono), denti a scatto di sportello e sportellino, fermagli di F1, T-plug e Wago, feritoie, percorso dei cavi; micro-USB della SSC-32 non raggiungibile a corpo montato (la scheda si configura al banco, come previsto); ginocchi anteriori nel campo della camera (fase 6); viteria nella stima di massa probabilmente bassa.
- **BOM**: B18 diventa "4 distanziali M3 maschio-femmina da 5 mm" per il vassoio; D10 (cinghie a strappo) non serve più (lo sportello tiene il pacco con i rebbi e la schiuma).

## D-052 — Dettagli del corpo (v0.4, 2026-10-09)

- **Fissaggio del coperchio**: quattro colonnine Ø7,4 sul tetto del tunnel, alte fino al lato inferiore del dorso, con inserto M3 in testa; il coperchio si avvita con 4 viti M3 × 8 (1,6 di dorso + 6,4 nell'inserto da 6,7). Posizioni scelte negli unici corridoi liberi del tetto: davanti a x 40 e |y| 22,5, tra il vassoio (|y| fino a 16,5) e il fianco del tunnel; dietro a x −56, tra il portafusibile F1 (fino a −61,4) e la SSC-32 (da −50,8), con 1,5–2,3 mm d'aria. Scartata la prima idea, colonnine accanto alle gondole medie: a x 14 toccavano le alette dei servo di coxa medi (ingombro fino a |x| 10,3) ed entravano nell'ingombro dei regolatori. Il coperchio appoggia anche con le gonne sull'orlo delle pareti delle baie. Al posto delle "linguette e 2 viti" previste: niente parti in più e nessun aggancio da provare.
- **Ventilazione dei regolatori**: cinque feritoie 6 × 3 per lato nel ripiano delle baie anteriori e cinque sopra, nel dorso del coperchio, allineate sul corridoio d'aria tra i componenti dei regolatori (|y| da 33,4) e il fianco del tunnel (|y| 27): l'aria entra da sotto e sale lungo i componenti. Nel coperchio i fori sono tagliati dopo i lobi, che altrimenti li richiuderebbero.
- Verificato sul modello: colonnine piene, inserti e fori del dorso allineati (prova a punti), feritoie aperte in base e coperchio, nessuna interferenza nella posa di riferimento, coxe libere a ±35° e tra vicine a 31°, ciclo a tripode libero a 70/70. Massa in più circa 5 g.

## D-053 — Basetta dell'ESP32 (2026-10-09)

- La millefori 50 × 70 (voce C2) si **taglia a 56 × 35** e sta sul vassoio da x 22 a 78, |y| fino a 17,5, da z 5,9 a 7,5: intera non entra (le colonnine del coperchio sono a 18,8 dall'asse). Porta i due strip femmina dell'ESP32 (file dei pin da x 22,5 a 73,3, a |y| 12,35) e, tra le due file, sotto il circuito dell'ESP32, regolatore 5 V (B2), traslatore (C1), partitore (B10) e accensione del rail (B11): 8,5 mm d'altezza (6,6 sotto la sede della microSD, da x 22,5 a 37,5).
- Si fissa con **4 viti M2 × 5** in inserti M2 su quattro colonnine del vassoio (Ø5,8, alte 3,3: la luce copre le teste delle viti M3 del vassoio e le saldature). Colonnine tra le due file di pin, a (29, ±6,8) e (75,5, ±6,5), fuori dalle teste M3 del vassoio; i quattro fori nella basetta si trapanano a Ø2,2 sulle colonnine.
- Verificato sul modello: nessuna interferenza; 3,1 mm dalla morsettiera della SSC-32, 1,0 dalla base, appoggio sulle colonnine e sotto gli strip dell'ESP32.

## D-054 — Fissaggio dello sportello della batteria (2026-10-09)

- Lo sportello si infila e si sfila **lungo X** (i rebbi entrano per 17 mm dietro il pacco: una cerniera o un aggancio in alto che ruota non li lascerebbe uscire). Si ferma con **due viti M3 × 8** in basso, in inserti di due blocchetti della chiglia fuori dal tunnel (x da −85,4 a −77,4, |y| da 26 a 32,2, tutta l'altezza della chiglia: stampa senza sbalzi), e con una **linguetta** in alto, larga 16 e profonda 6, che entra sotto il tetto (0,4 mm dal tetto, 1,0 sopra il pacco): se la parte alta prova ad aprirsi, la linguetta sale contro il tetto dopo circa 1 mm.
- Scartate: guide verticali con lo sportello che scende dall'alto (a robot capovolto si sfila da solo), aggancio nelle fessure dei cavi più viti in basso (i rebbi non escono ruotando), viti in alto (nessun posto: tetto da 2 mm, F1 a 2 mm dalla coda, sedi dei servo posteriori accanto al tunnel), denti a scatto (forza di sgancio da tarare, nessuna leva raggiungibile).
- Cambio della batteria: due viti, si sfila lo sportello, si sfila il pacco. T-plug e F1 restano raggiungibili dal retro senza togliere lo sportello.
- Verificato: nessuna interferenza; distanza minima dalla coxa posteriore che ruota: chiglia 2,35 mm (1,83 a +35°), sportello 3,98 mm (2,16 a +35°): per questo le viti sono a |y| 28,5 e non 29. Coxe libere a ±35° e tra vicine a 31°, ciclo a tripode libero a 70/70.

## D-055 — Wago in piedi, fissaggio di F1 (2026-10-09)

- **Errore trovato**: i due Wago 221-415 sdraiati sul ripiano delle baie posteriori (D-051) avevano gli ingressi dei fili a 1,4 mm dalla parete della baia (la baia è larga 21 mm, il Wago è profondo 18,6): i cavi da 12–16 AWG non sarebbero entrati. Ora stanno **in piedi**, con gli ingressi in alto (fili dall'alto, sotto il coperchio) e le leve verso la parete della baia (12 mm d'aria per aprirle), il dorso a 0,5 mm dal fianco del tunnel; x da −46 a −16, z da −29,95 a −11,35.
- **Sede dei Wago** stampata con la base: due spalle alle estremità (alte 6, gioco 0,2) e due labbri da 1,6 che coprono 1 mm delle estremità della faccia delle leve, fuori dalle leve. Il Wago entra dall'alto e resta fermo tra spalle, labbri e fianco del tunnel; se al banco balla, una goccia di colla a caldo.
- **F1**: due costole sul tetto (alte 3, larghe 24, gioco 0,2) lo fermano lungo X; lo stringe al tetto una fascetta da 2,5 mm (voce D11) che passa nelle due fessure dei cavi a x ≈ −76, fuori dalla linguetta dello sportello e dalle uscite dei fili del portafusibile. La coppia di T-plug resta appoggiata sopra F1, tenuta dai suoi cavi.
- Verificato: nessuna interferenza; coxe libere a ±35° e tra vicine a 31°, ciclo a tripode libero a 70/70.

## D-056 — Sportellino di servizio e note di stampa del corpo (2026-10-09)

- **Sportellino** (sopra USB-C e pulsanti dell'ESP32): resta su per attrito, con quattro nervature larghe 1 mm sui lati lunghi della cornice, a filo dell'apertura nel modello (i fori stampati vengono più stretti di 0,1–0,2 mm: l'interferenza viene dalla stampa e si tara sul pezzo). Una tacca nel dorso sotto il bordo anteriore (3 × 10, profonda 0,8) per sollevarlo con l'unghia. Scartati i denti a scatto: con 1,6 mm di dorso il dente sarebbe lungo 3 mm e non fletterebbe senza rompersi.
- **Chiglia**: niente labbro di centraggio. Un labbro interno toglierebbe 2,8 mm al tunnel, dove il pacco ha 1,3 mm d'aria per lato; uno esterno urterebbe il ripiano delle baie. La centrano le quattro viti M3 nei fori da 3,4 (±0,2 mm).
- **Stampa della base** (con il fondo sul piatto): il tetto del tunnel è un ponte di 50 mm lungo 162, e le 12 bugne sotto le alette dei servo di coxa sono sbalzi piatti a 25,6 mm dal piatto: supporti con interfaccia nell'altro materiale (toolchanger), sotto il tetto solo nella parte interna del tunnel. Un tetto a falde non ci sta: tra pacco e tetto ci sono 2,6 mm.
