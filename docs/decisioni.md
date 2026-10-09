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

## D-057 — Muso del coperchio (2026-10-09)

- Il coperchio scende davanti e ai lati di vassoio, torretta e camera con una fascia da 1,6 mm (x da 81 a 101, |y| fino a 20, fino a z −1, sotto il vassoio): ripara ESP32, antenna e camera dagli urti e chiude il corpo davanti. È in PETG come tutto il coperchio (antenna fuori dal carbonio).
- **Finestra della camera** Ø17 centrata sull'asse ottico (z 22,5): il cono di 120° dal centro ottico, a 2,5 mm, ha raggio 4,3; i bordi della finestra, il dorso e i fianchi restano fuori dal campo. Davanti alla lente restano 0,9 mm: il coperchio si sfila verso l'alto senza toccarla.
- Verificato: nessuna interferenza; coxe anteriori libere a ±35°; ciclo a tripode libero a 100/45.

## D-058 — Cavi lungo la zampa (2026-10-09)

- I cavi di femore e ginocchio escono dall'alto delle culle (quello del femore dalla culla della coxa, sull'asse dell'anca; quello del ginocchio dalla culla della tibia, sull'asse del ginocchio), corrono sopra la zampa e sul braccio del ponte fino al mozzo, passano sopra l'asse della coxa (dove l'imbardata cambia meno la lunghezza) ed entrano sotto il coperchio.
- **Ponte**: due feritoie 3 × 1,6 a X 28 e |Y| 5,5 per una fascetta da 2,5 mm, con una gola profonda 1,2 sotto il braccio tra le due: il braccio passa 1,5 mm sopra il servo di coxa e la fascetta, a filo, non ci striscia quando la coxa ruota. La testa della fascetta resta fuori dal coperchio (r 28 dall'asse, il lobo arriva a 22).
- **Femore**: una fascetta da 200 mm attorno a tutto il femore, vicino all'anca (circa 15 mm dall'asse), senza feritoie: vicino al ginocchio la tibia ripiegata a γ 29° passerebbe a pochi millimetri.
- **Anse**: tra la culla della tibia e la fascetta del femore il cavo del ginocchio va da 22 a 40 mm al variare di γ; tra la fascetta del femore e il ponte, da 11 a 56 mm al variare di α. Le anse si lasciano sopra il servo del femore. `calc/cavi_servo.py` ne tiene conto (anse di 10, 17 e 20 mm per imbardata, anca e ginocchio).
- Verificato: ponte rigenerato, giunti e limiti della zampa rifatti, posa di riferimento misurata (0; 90), nessuna interferenza nella zampa e nell'assieme, coxe libere a ±35°, ciclo a tripode libero a 70/70. STL del ponte riesportato.

## D-059 — Risposte dell'utente del 9 ottobre; estetica non ancora applicata

- **Pulsante d'accensione**: approvato il pulsante da pannello Ø12 sul coperchio (voce B3b), collegato ai pin A e B della 2813.
- **Approvate** "se necessarie": 12 viti M3 × 5 (D6), distanziali B18, schiuma D10 al posto delle cinghie, 4 prolunghe C5. Tutte servono al modello. **Tolta C6** (clip delle prolunghe): non serve, le quattro giunzioni si chiudono con il termorestringente B19.
- **Cicalino**: domanda riscritta (BOM, domanda 6). Nella prima versione avevo scritto che dentro il corpo non c'era posto: è sbagliato. Sotto il coperchio in coda, sopra il T-plug, c'è spazio (25 × 40 × 14 mm), il display si vede da una finestra del dorso e lo spinotto di bilanciamento si stacca dal retro come il T-plug.
- **Estetica** ("futuristica ma minimale"): finora **non applicata**. Coperchio, muso, gonne e sportelli sono forme funzionali (piastre, lobi circolari, scatola del muso) e nessuna decisione ne ha tenuto conto; l'unico accenno è nel giudizio sulle architetture della zampa. Va fatta una passata estetica sulle parti non strutturali (coperchio, muso, gonne, sportelli) e sulle facce in vista di zampe e base, prima di considerare chiuso il CAD; pulsante e cicalino si collocano dentro quella passata.
- Aggiornamento dello stesso giorno: l'utente sceglie per il cicalino la (c) e dà le indicazioni sull'estetica, ora in `CLAUDE.md` ("Cosa è deciso dall'utente"): carta bianca sul design, cover delle zampe come placche non strutturali in un altro colore, housing della camera integrato nel frontale.

## D-060 — Passata estetica: scelto "Kabuto" (2026-10-09, da approvare)

- Tre concept indipendenti (Kabuto sfaccettato, Ciottolo levigato, Lamina a pannelli), ognuno con i suoi render schematici (`cad/render/render.py` sulle mesh vere del modello), giudicati da tre revisori che hanno guardato i render e rifatto i conti: estetica, funzione, fattibilità CAD. **Kabuto primo per tutti e tre** (7/7/7; Lamina 6/6/6; Ciottolo 5/4/4). Tutto in `ricerca/estetica.json`, immagini in `ricerca/estetica/`, specifica in `ricerca/estetica-specifica.md`.
- Versione scelta: guscio bianco sfaccettato con sei lobi esagonali sopra le zampe (un lato perpendicolare a ogni zampa), smusso a 45°, fascia nera dalla coda alla visiera della camera (sportellino, pulsante e finestra del cicalino nella fascia), lame bianche su entrambi i lati dei femori con finestre esagonali sui giunti, scudo bianco sul ginocchio, struttura e giunti antracite a vista, piedini in TPU arancio. Innesti da Lamina (coda come porta di servizio, paratie ai lati della testa) e da Ciottolo (lame da giunto a giunto, piedini arancio). Massa +75 g circa (2,8 kg, femore al 49 %).
- **Errori del modello di oggi trovati dai giudici**, da correggere nel primo blocco: (1) le due viti del blocco del femore in (94,5; 7,5) e (94,5; 12,9) distano 5,4 mm e le loro rondelle Ø7 di registro (D-049) si sovrappongono: si spostano gli inserti del blocco; (2) la fascetta attorno al femore di D-058 urta la testa dell'anima della coxa sopra α 74°: va dentro il blocco del femore.
- In attesa del via libera dell'utente e dell'approvazione dei filamenti (PETG bianco, PETG nero non caricato, TPU arancio).
- Risposta dell'utente (9 ottobre): la direzione gli piace; chiede placche **più bombate** ("da placca, non da lamiera piatta") e **più arrotondate**, meno spigolose dove non serve, che accompagnino la struttura; e di valutare a parte una **tibia rastremata** (più larga sopra, più stretta verso la punta, non troppo), con un paio di varianti oltre a quella di base. In corso: due designer con render (placche, tibia) e due revisori; filamenti ancora da approvare.
- **Seconda revisione** (stesso giorno; `ricerca/estetica-v2.json`, render in `ricerca/estetica/5-placche/` e `6-tibia/`): due designer e due revisori indipendenti, tutti con render. **Placche**: consigliata la variante "Piena" (lame bombate con colmo 2,6, estremi R8 concentrici alle teste del femore, gobba fusa con rampe a 30° e 45°, ginocchiera a U, lobi del carapace raccordati R12/R10, dorso piano); da correggere: niente raccordo nei fori delle teste della lama A (presa 2,2–2,6 mm), lame piene (+33 g, femore 49,5 %), toro e raccordi da provare prima su un documento a parte, ripiego sulla "Morbida". Contatto tra zampe vicine a 31,2°, 4,6 mm al limite del firmware. **Tibia**: consigliata "V2 lama ad arco" (dorso dritto, fianco esterno ad arco fino a una punta 8 × 12,4, due fessure tonde, +2 g per tibia), con il fianco che parte a filo della culla e tangente; il lato interno non si allarga perché a γ minimo lo stinco passa a 0,03 mm dalla coxa. Piedino in TPU a U da disegnare. In attesa delle scelte dell'utente.
- Precisazione dell'utente (9 ottobre, con due disegni in `ricerca/estetica/7-guscio/`): scelta la **Piena**, ma le placche vanno **bombate come gusci**, curve in due direzioni e non solo raccordate sugli spigoli, con i bordi morbidi; la tibia **V2** va bene ma deve stringersi **anche nell'altra direzione**, partendo larga quanto il fondo della culla. Render di prova della mia interpretazione nella stessa cartella. Vincoli che restano: le lame del femore non sporgono oltre le teste delle viti (zampe vicine), la ginocchiera può sporgere (faccia esterna della tibia), il lato della tibia verso il corpo non cresce (γ minimo), il piede resta sull'asse della zampa.
- Seconda precisazione (9 ottobre, spunto in `ricerca/estetica/7-guscio/spunto_utente.jpg`: una cover che avvolge un segmento di gamba): placche **più spigolose e meno organiche**, che **avvolgano** la struttura e sembrino parte integrante; tibia: va bene la **V2**, solo **allargata anche lateralmente** e bombata, tipo guscio (la prova a corno era sbagliata). Prova 2 nella stessa cartella.
- Terza precisazione (9 ottobre, seconda foto in `ricerca/estetica/7-guscio/spunto_utente_2.jpg`): niente risvolti sulle lame del femore (restano come la Piena); la placca della tibia diventa un **guscio lungo** che copre gran parte della tibia, sporge verso l'esterno, è più largo in alto e più spigoloso, con una finestra lunga; tibia V2 allargata in alto. Prova 3 nella stessa cartella.

## D-061 — Versione estetica approvata e blocco B1 del CAD (2026-10-09)

- **Approvata dall'utente** ("così mi piace molto"): carapace e lame del femore come la variante **Piena** (lame bombate, estremi R8 attorno alle teste del femore, gobba fusa, senza risvolti); sulla tibia un **guscio lungo** (prova 3: dal ginocchio fin quasi al piede, sporge verso l'esterno da 3 a 6 mm, largo in alto, sezione a C con smussi a 45°, finestra lunga); **tibia V2** (fianco esterno ad arco tangente alla culla) allargata in alto. Resto della specifica di Kabuto corretto (`ricerca/estetica-specifica.md`). L'utente ha detto di passare al CAD e verificare lì.
- **B0, prova delle funzioni dell'API** (`cad/script/prova_api.py`, documento a parte chiuso senza salvare): intersezione con un cilindro (bombatura), raccordo degli spigoli di una faccia curva, smusso a 45° di spigoli scelti per posizione, svuotamento con una faccia tolta dopo lo smusso (sezione a C), rivoluzione e loft: tutto sano, volumi uguali ai conti.
- **B1, femore** (`zampa.py`):
  - inserti del blocco lato ginocchio da Z 7,5 e 12,9 a **6,0 e 13,4**: con 5,4 mm di interasse le rondelle di registro Ø7 si sovrapponevano;
  - **fascetta dei cavi dentro il blocco** (due feritoie dallo smusso alto a X 79,5 e un tunnel a Z 10): sostituisce la fascetta da 200 mm attorno al femore di D-058, che entrava nella testa dell'anima della coxa da α 74°;
  - fascetta del ponte da X 28 a **24** (sotto il lobo del carapace, testa della fascetta di fianco al braccio);
  - fori ciechi Ø3,1 × 3,3 per le spine della lama B in Femore_B (X 81 e 94,5, Z 6);
  - nuovo `Ingombro_Teste_A` (12 teste M3 sul lato A, non si stampa) per le verifiche tra zampe vicine.
- Verificato: zampa senza interferenze, 50 pose della scansione libere (α da −49 a +85, γ al minimo della tabella, γ 180) e le 19 pose di controllo a γ minimo − 2 toccano (tabella invariata); assieme senza interferenze, coxe libere a ±35°, zampe vicine libere a 31° con le teste modellate (contatto a 34°), ciclo a tripode libero a 70/70. Femore_B −0,16 cm³.
- **B2, lame del femore** (`zampa.py` → `cover_femore_a`, `cover_femore_b`; PETG bianco): sagoma Piena (corpo tra i mozzi, estremi esagonali di apotema 14,5 fatti da tre rettangoli, plateau sopra il blocco e rampe a 30° e 45°), raccordi in pianta R8 sugli estremi, R10 sulle rampe, R8 a fine plateau; finestre esagonali di apotema 11 con angoli R4; **bombatura doppia per intersezione con un toro** (cerchio R 148,8 ruotato di 20° attorno a un asse a 1920 mm): 2,6 mm al colmo, 1,6 ai bordi; raccordo 0,8 sulla faccia esterna. Lama A appoggiata sulla piastra con quattro fori Ø5,6 senza raccordo sulle teste del blocco (incastro sui fianchi delle teste); lama B con due spine Ø3 × 3 nei fori ciechi. Lame piene (correzione del revisore: lo svuotamento non reggeva), 3,79 cm³ la A; punte a X 39,49 e 135,51 come nella specifica. Giunti rigidi alle piastre; nelle pose seguono il femore.
- Verificato: 50 pose della scansione libere e i 20 controlli che toccano; nessuna interferenza; zampe vicine libere a 30° e 31°, **contatto tra 31° e 32°** (prima delle lame 34°): il firmware deve tenere 30° e la somma tra vicine entro 60° senza eccezioni; ciclo a tripode 70/70 e 100/45 e rotazione sul posto a 30° liberi.
- **B3, tibia e guscio** (`zampa.py` → `tibia`, `cover_tibia`):
  - **stinco V2 allargato**, costruito prima della culla e da solo: fianco −X da 6 a 4 mm dall'asse (non cresce mai verso la coxa: a γ minimo è il lato critico), fianco +X ad arco R 275 tangente allo zoccolo fino a 4 mm, faccia −Y da 18 a 6 mm (prima 9,45 costante), faccia +Y piana sul piano dell'orlo (sta sul piatto di stampa), punta raccordata R 3,8, due fessure tonde, inserto M3 sulla faccia +X a 88 mm sotto il ginocchio per la vite del guscio. Tibia 31,8 cm³ (prima 25,1), circa 2,3 g in più.
  - **guscio lungo** (PETG bianco): pieno dal centro dello stinco al fronte, fronte convesso per intersezione con un cilindro R 288 (sporgenza massima 7,3 mm a 25 mm sotto il ginocchio, 4,7 in cima e 4,6 sullo stinco in fondo), fianco +Y dritto, fianco −Y dritto fino allo zoccolo e poi rastremato, smussi a 45° da 4 mm tra fronte e fianchi, svuotamento a 1,6 aperto dietro, sopra e sotto. Niente fianco +Y sopra lo zoccolo (lì gira il servo del ginocchio) e niente fianco −Y nei 16 mm sotto il ginocchio (testa del femore). Due tappi a rombo nelle finestre della parete +X della culla e una vite M3 × 10 in basso con un bossolo; finestra lunga 7 × 48. 10,4 cm³, circa 13,5 g per zampa.
  - Con la sporgenza di 5,8 mm prevista, la superficie interna degli smussi toccava gli spigoli della culla in alto e dello stinco in basso (13,6 mm³): portata a 7,3, che sporge di più verso l'esterno come chiesto.
- Verificato: zampa senza interferenze; 54 pose libere (anche γ 150 e 180); 17 controlli su 20 a γ minimo − 2 toccano (gli altri tre ora sono liberi: lo stinco più stretto in basso lascia più aria, la tabella del firmware resta prudente); assieme senza interferenze, coxe libere a ±35°, zampe vicine libere a 30° e 31°, ciclo a tripode 70/70 e 100/45 e rotazione sul posto a 30° liberi.
- Da fare: il piedino in TPU (D9) sulla punta dello stinco; la massa delle cover delle zampe (circa 22 g per zampa) va riguardata con il bilancio completo in B8.

## D-062 — Tibia e guscio simmetrici (2026-10-09)

- **Richiesta dell'utente** (guardando in Fusion la tibia di B3): stinco e guscio simmetrici. Prima lo stinco aveva la faccia +Y piana sul piano dell'orlo e la faccia −Y inclinata (da 18 a 6 mm), e il guscio si stringeva solo sul lato −Y.
- **Soluzione**: fianchi Y simmetrici sul **piano medio dello zoccolo** (`tib_y_c`, Y −7,35), che è anche il piano medio del guscio. Lo stinco parte a filo dello zoccolo sui due lati (33,6 mm, `tib_y_semi_alto`) e si stringe dritto fino a 14 mm alla fine dell'arco (`tib_y_semi_basso` 7). Il guscio ha la rastremazione specchiata, con i fianchi paralleli allo stinco a 0,4 mm d'aria (`cov_tib_y_semi_basso`), e la finestra lunga e la vite in basso sul piano medio. Gli altri fianchi (−X dritto, +X ad arco) non cambiano.
- Scartata la simmetria sul piano Y 0, che avrebbe tenuto la punta sull'asse della zampa: lo stinco sarebbe uscito di 8,5 mm dallo zoccolo sul lato +Y e il guscio avrebbe avuto un gradino sotto lo zoccolo.
- **Conseguenze**:
  - la punta del piede passa da Y +1,7 a **Y −7,35** nella terna della zampa (verso il cuscinetto del ginocchio). Per la cinematica inversa è una costante; i momenti attorno agli assi di femore e ginocchio non cambiano. Il carico si sposta un po' sul lato del cuscinetto e meno sulla squadretta del servo. Supera il vincolo "il piede resta sull'asse della zampa" di D-060;
  - **stampa**: lo stinco non ha più una faccia sul piano dell'orlo. Sdraiato sull'orlo serve un supporto a cuneo sotto la faccia +Y dello stinco (faccia a 8° dal piatto, alto al massimo circa 10 mm alla punta), con interfaccia nell'altro materiale;
  - tibia 33,8 cm³ (circa 2 cm³ e 2 g in più); guscio 10,3 cm³, invariato.
- Verificato in Fusion (versione 23):
  - zampa senza interferenze, 54 pose della scansione libere; 17 controlli su 20 a γ minimo − 2 toccano, come prima;
  - assieme: coxe libere a ±35°, zampe vicine libere a 30° e 31°, ciclo a tripode 70/70 e 100/45 e rotazione sul posto a 30° liberi. L'unica interferenza è tra il vecchio coperchio e il carapace nuovo, che lo sostituisce (B4).
- Punto di ripristino della versione di B3: copia "Hexapod v2 - MG996R - ripristino tibia asimmetrica (v22)" nel progetto Fusion e tag git `ripristino-tibia-asimmetrica`.

## D-063 — Carapace e parti nere costruiti, verifiche e masse (2026-10-09)

- **B4–B6** (`corpo.py` → `carapace`, `carapace_dettagli`, `fascia`, `visiera`, `gonne`, `sportellino`, `sportello`, `togli_coperchio`): carapace, fascia, visiera, gonne, sportellino a ottagono e smusso dello sportello della batteria, come la specifica (`ricerca/estetica-specifica.md`, 2.1–2.7). Il vecchio `Corpo_Coperchio` è cancellato, senza lavorazioni orfane. `Rif_Pulsante_12` nuovo in libreria; cicalino e pulsante sono istanze nel corpo (`assieme.py` → `pose_corpo`).
- **Scarti dalla specifica**, tutti trovati sul modello:
  - **occhio della camera fatto con un loft** fra le due bocche, prolungate di 0,5 mm oltre le facce. Le quattro estrusioni piane della specifica avrebbero tagliato anche fuori dal tronco: un prisma estruso non si ferma agli spigoli delle pareti vicine, e il taglio in alto avrebbe aperto tutta la visiera sopra l'occhio;
  - **guance di coda in due blocchi**: la parte sopra l'attacco dello smusso (z 30) bucava lo smusso del lobo posteriore (un cuneo di 3 mm visibile dal retro) e ora rientra 1 mm dietro la linea della coda;
  - nervature del collare del cicalino a filo nel modello, come quelle dello sportellino (D-056), così il controllo delle interferenze resta pulito;
  - angoli dell'ottagono: i rettangoli dei tagli d'angolo stanno dalla parte interna del lato a 45°. Con i lati in senso antiorario, b = a ruotato di +90° punta fuori, quindi i rettangoli sono a b < 0.
- Volumi: carapace 49,1 cm³ (51,1 dopo lo svuotamento, contro 53 ± 3 stimati), fascia 3,1, visiera 1,5, gonne 3,8, sportellino 2,3, sportello 5,5.
- **Verifiche (B7, Fusion versione 24)**, ognuna con il suo caso di controllo:
  - assieme senza interferenze; coxe libere a ±35°;
  - zampe vicine: libere a 30° e 31°, contatto tra 31° e 32° su tutte e quattro le coppie laterali. Il verso è stato provato: a sinistra AS +, MS −; a destra AD −, MD +; MD −, PD +. Anteriori e posteriori libere a 34°;
  - carapace contro ogni zampa (`assieme.py` → `carapace_zampe`), imbardata −35, 0, +35 con (α, γ) = (85, 90), (85, 29), (60, 90): libero. Distanza minima da femori, lame e teste: 4,6 mm sulle zampe medie, 7,1 sulle altre. Controllo: α 100 tocca il carapace;
  - testa: zampe anteriori a ±35° con α −49, 0, 85 e γ 90 o 180: libere dalla visiera e dal carapace;
  - sfilamento (`sfilamento`): carapace, fascia, visiera, gonne, sportellino, cicalino e pulsante sollevati di 5, 10, 20 e 40 mm: liberi. Controllo: a −2 mm le gonne e il carapace toccano la base;
  - campo della camera (`campo`): tronco di piramide da 7 × 7 sulla lente con 54,2° e 46,1°, lungo 15 mm, libero da visiera, fascia e carapace. Controllo: con +6° tocca visiera e fascia;
  - ciclo a tripode 100/45, 130/25 e 80/60 in 4 fasi, 70/70 in 8; rotazione sul posto di 30° a 100/45 e 70/70: nessun urto;
  - timeline senza avvisi, nessuna posa pendente.
- **Masse** (`progetto-meccanico.md`, tabella aggiornata): totale atteso **circa 2910 g** (2730 prima della passata estetica). Le cover pesano 139 g contro i 49 della specifica, perché le lame sono piene (B2) e il guscio della tibia è lungo (scelta dell'utente); le tibie più larghe 21 g; il carapace 19 g. `calc/statica_tripode.py` con 2910 g: femore al **51 % dello stallo** al punto di progetto 100/45 (48 % con 2750), ginocchio al 47 %. È sopra la soglia del 50 % che ci si era dati, ma dentro quanto l'utente ha accettato ("accetta di superare il 50 % dello stallo"). Massa di progetto del calcolo portata a 2910. Se servirà alleggerire, la prima leva è il guscio della tibia (1,2 mm invece di 1,6: circa 20 g in meno); la base (198 g) va guardata nello slicer.
- **Stampa** (`cad/stl/README.md`, STL riesportati con `cad/script/esporta_stl.py`): il carapace con fascia, visiera e gonne è un pezzo a due colori, capovolto, senza supporti. Aperto: la **lama B** ha le spine sulla faccia interna e non ha una faccia piana da mettere sul piatto. O si stampa con la bombatura in giù e un supporto d'interfaccia sotto i bordi (al massimo 1 mm), o le spine diventano fori e si usano spine separate; si decide con il provino.
- Render a colori della versione attuale in `immagini/assieme-carapace-*.png`; `esporta_mesh.py` ha i gruppi `carapace` e `nero`.

## D-064 — Piedino in TPU (2026-10-09)

- `Piedino` (voce D9, TPU 95A arancio, ancora da approvare come colore: BOM, domanda 7): cappuccio che calza la punta dello stinco da 0,5 mm sotto il bordo del guscio (z 94,5) fino al piede. Si costruisce rifacendo lo stinco con le stesse lavorazioni (`_stinco`), togliendo tutto sopra il bordo e svuotando verso l'esterno con parete e suola da 1,6 (`tib_piede_sp`, quattro perimetri): dentro è lo stinco esatto, quindi segue da solo ogni modifica dello stinco. 1,4 cm³, circa 1,7 g; giunto rigido alla tibia.
- **Lo stinco finisce a 108,4 invece che a 110**, così la suola resta a `zam_Lt` (110) e la cinematica non cambia; `tib_z_arco` segue (104,4).
- Nel modello la stretta sullo stinco è zero; la presa vera (TPU elastico su uno stinco che si stringe verso la punta) si tara sul provino con 0, −0,2 e −0,4 mm. Stampa con la bocca sul piatto e la punta in alto.
- Verificato: zampa senza interferenze, 54 pose libere e 17 controlli su 20 come prima; assieme senza interferenze; ciclo a tripode 100/45 e 70/70 libero. Massa attesa circa 2905 g (i piedini erano già stimati fra le parti non modellate).

## D-065 — Tibia sull'asse del femore, lama B avvitata, materiali e inserti (2026-10-09)

- **Tibia** (richiesta dell'utente: con D-062 il piede era spostato rispetto all'asse del femore; resta simmetrica, eventualmente più larga): stinco e guscio ora sono simmetrici sul **piano della zampa (Y 0)**, il piano medio fra le due piastre del femore. Il piede torna sull'asse.
  - Lo stinco parte largo quanto lo zoccolo (±24,15) e si stringe dritto fino a ±7 alla fine dell'arco. Sul lato −Y è a filo dello zoccolo; sul lato +Y passa sotto le alette del servo, a 0,8 mm dalla loro punta. Le viti delle alette si raggiungono ancora: il loro asse sta 3,6 mm sopra lo stinco. Tibia 39,3 cm³.
  - Il guscio va da −26,15 a +26,15 (12,7 cm³). Il fianco +Y passa fuori dalla cassa del servo del ginocchio, che prima restava scoperta. Come il −Y, è tolto nei 16 mm sotto il ginocchio, dove girano piastre, squadretta e mozzo.
  - Visto da davanti, il ginocchio è centrato fra le due teste del femore.
  - Verificato: zampa senza interferenze; 54 pose della scansione libere e 17 controlli su 20 come prima; quindi lo stinco più largo non tocca la coxa al γ minimo. Assieme senza interferenze; zampe vicine libere a 31° e a contatto a 32°, come prima; carapace contro le zampe libero (distanze minime invariate); cicli 100/45, 70/70 e rotazione a 30° liberi.
  - Stampa: lo stinco ora sporge dal piano dell'orlo. Proposta: fondo della culla sul piatto e supporto a cuneo sotto lo stinco; decide l'utente nello slicer.
- **Lama B avvitata**: le due spine stampate sulla faccia interna (che non lasciavano una faccia piana per il piatto, D-063) diventano due **viti M2 × 6 a testa svasata** in inserti M2 nella piastra di Femore_B, a X 81 e 94,5, Z 6. La faccia interna della lama è piana; le teste stanno a filo nelle svasature (0,9 mm a 90°), quindi il contatto fra zampe vicine non cambia. La lama si smonta senza forzare niente. Voce nuova D8b (12 viti), **da approvare**; gli inserti M2 passano da 16 a 28.
- **Piedino**: resta un cappuccio separato (D-064) invece di una punta in TPU stampata insieme alla tibia con il beam interlocking. Si consuma sul pavimento e si cambia da solo (2 g contro una tibia con la culla). Si possono provare TPU e silicone (D9). La tibia resta di un solo materiale.
- **Materiali** (scelta dell'utente):
  - PETG-CF nero per le parti funzionali; sportello della batteria compreso, perché regge il pacco;
  - PLA per le placche: carapace, lame e gusci, bianco per ora;
  - TPU arancio per i piedini.
  - Proposte mie:
    - fascia, visiera, gonne e sportellino in un secondo PLA (nero): si stampano insieme al carapace e PLA su PLA si attacca senza interlocking. L'intarsio della fascia è di soli 0,6 mm, troppo sottile per l'interlocking con un altro materiale;
    - vassoio dell'ESP32 in PLA, perché sta sotto l'antenna.
  - Attenzione al PLA del carapace: rammollisce verso 55–60 °C. Sotto ci sono i due regolatori, che sotto carico scaldano. Le feritoie sopra le baie anteriori ci sono (D-052); se a robot montato l'interno scalda, il carapace si ristampa in PETG.
- **Inserti in ottone**: il progetto li usa già quasi ovunque. Sono 94 M3 e 28 M2 a caldo; nessun bullone con dado. Le uniche viti in fori pilota sono quelle delle alette dal lato dell'albero (D-049). Dove si monta e smonta (carapace, sportello della batteria, guscio della tibia, ora la lama B) c'è sempre una vite in un inserto, mentre le parti che si aprono spesso senza attrezzi (sportellino, lama A) sono a incastro. L'utente ha un kit di inserti da Temu: se le misure vanno bene sostituisce D4 e D5; i fori si adeguano con `ins_m3_d`, `ins_m3_l`, `ins_m2_d` e `ins_m2_l`. **Misure da avere dall'utente** (il link non si apre da qui).
- Massa attesa circa 2945 g; femore al 51 % dello stallo al punto di progetto (massa del calcolo aggiornata).

## D-066 — Versione 2.1.0: predisposizioni per sensori, luci, audio e computer di bordo (2026-10-09, in corso)

Decisioni dell'utente del 9 ottobre: audio a bordo senza la microSD dell'ESP32, computer di bordo solo predisposto a zaino sul dorso, software approvato (ESP-IDF in C++, repo pubblica), luci del pulsante e dei lobi più la predisposizione nelle tibie (se montarle lo decide dopo). Si lavora sulla copia del design "Hexapod v2.1.0"; la 2.0.0 resta congelata (tag `v2.0.0`, `docs/versioni.md`). Piano in `docs/piano-v2.1.0.md`.

**Blocco A — zampa** (fatto e verificato il 9 ottobre):
- **Punta dello stinco per il sensore di forza** (FSR 400 Short, voce X5): la punta della `Tibia` è piana, finisce a 107,6 (`tib_punta_z` = 110 − 1,6 di suola − 0,3 di FSR − 0,5 di pistoncino) e ha raccordato solo lo spigolo +X (R 1, su cui si piega la coda del sensore); lo spigolo −X resta vivo. Per fare posto alla testa (Ø 7,6) la punta si allarga solo verso +X: `tib_x_piu_basso` da 4 a 6, il raggio dell'arco del fianco passa da 262 a 341. La parte piana è di circa 8,2 mm.
- **Smusso di 1,5** sugli spigoli fra la faccia +X e i fianchi Y dello stinco (`tib_smusso_piu`): con la punta più larga quegli spigoli entravano di circa 0,4 mm nello smusso interno del guscio fra Z 81 e 94 (4,5 mm³). Con lo smusso il gioco torna quello di prima.
- **Tasca** 6 × 9 × 1,2 sulla faccia +X dentro il piedino per linguette e saldature, e **gola** 2 × 2 dei fili a Y 3,5…5,5 dalla tasca al fondo della culla (Z −33), fatta a corde dell'arco, sotto il guscio e fuori dalla finestra. Solo nella `Tibia`, non in `_stinco`: il piedino non le copia.
- **Piedino**: nasce dallo stinco con la punta nuova ma lungo 108,4, così restano 0,8 mm per FSR e pistoncino e la suola resta a 110 (la cinematica non cambia). Pistoncino Ø 4,5 × 0,5 sulla suola sotto il centro della testa; tacca 2 × 2 per i fili nel bordo alto sopra la gola. Fuori i raccordi sono quelli dello svuotamento (1,6 sul lato −X, 2,6 sul +X): più grandi assottiglierebbero la parete sotto 1,2 allo spigolo vivo; la forma del piede si rivede con il provino.
- **Luci nelle tibie, predisposizione** (X31): sede piana larga 5,4 sulla faccia +X dello stinco sotto la finestra del guscio, dal fondo della culla a Z −80, per un tratto di striscia WS2812B-2020 (3 pixel a 60 LED/m); la sede è profonda 0,5 agli estremi e circa 1,3 al centro, perché è piana su una faccia ad arco. Fra la striscia (spessa circa 1,4 con i LED) e il diffusore restano almeno 1,4 mm. **Diffusore** `Cover_Tibia_Diffusore` (PLA bianco, 0,4 cm³): lastra da 0,6 che segue l'interno del fronte del guscio dietro la finestra lunga, con un bordino che entra a incastro nella finestra (0,1 di gioco per lato) e resta 0,6 sotto il fronte. Si monta solo con le luci: senza, la finestra resta aperta come prima e il guscio approvato non cambia. Con le luci spente un diffusore bianco fa vedere la finestra bianca invece che nera; in alternativa si può stampare in PETG traslucido fumé, scuro da spento: da decidere con il provino di luce (X10). I fili della striscia e quelli dell'FSR salgono con il cavo del servo del ginocchio e passano dagli stessi giunti: le anse non cambiano.
- **Inserto del guscio**: il foro parte dalla faccia all'altezza del suo bordo alto; prima la metà alta restava coperta da una pelle di 0,3 mm.
- **Punti con nome** per il software: `P_Asse_coxa`, `P_Asse_femore`, `P_Asse_ginocchio`, `P_Punta_piede` nelle parti della zampa (`zampa.py` → `PUNTI`); `esporta_robot.py` legge la punta del piede da lì. Le facce di riferimento per le dime si decidono con le dime (blocco C).
- Verificato:
  - zampa senza interferenze;
  - scansione ripetibile in `zampa.py` → `pose_scansione`:
    - 81 pose libere (α a passi di 5 da −45 a 85, con γ al minimo, 150 e 180);
    - 17 controlli su 20 toccano, come prima: 14 contro la coxa e 3 fermati dai limiti dei giunti. Restano liberi 0/41, 15/37 e 20/35 (la tabella del firmware resta prudente);
  - assieme senza interferenze;
  - zampe vicine libere a 31° e a contatto a 32° (femori), come prima;
  - cicli a tripode 100/45 (8 fasi) e 70/70 (16 fasi) e rotazione sul posto a 30°: nessun urto;
  - carapace contro la zampa media: distanze minime invariate (4,6 mm).
- Masse: tibia 111,4 g a segmento (+1,2: punta più larga e diffusore); modellato 2591 g, atteso circa 2951. FSR (3 g) e striscia (2 g) per zampa vanno aggiunti quando si comprano: circa 30 g in tutto, meno di mezzo punto di coppia al femore.

**Blocco B — corpo** (fatto e verificato il 9 ottobre):
- **Interruttore 2813** (B3): in piedi nella fessura fra la SSC-32 e il portafusibile (x −58,4, retro del circuito), su due guide con le scanalature per i bordi; sotto restano 5 mm per i fili; vicino a batteria, F1 e pulsante. Così il tetto sotto il vassoio resta per i sensori.
- **IMU e ADC ADS7830** sul tetto del tunnel sotto il vassoio, su bugne alte 4 con inserti M2 (l'inserto resta nella bugna e il tetto sopra il pacco non si buca); freccia dell'asse X stampata accanto all'IMU. Interassi dei fori C. **Asola** 6 × 3 nel vassoio per i fili del bus.
- **Prese dei piedi** (X5): fila di sei spine piegate in piedi in una scanalatura sul tetto (x 48…64, |y| 22–25), accanto all'ADC e fuori dal vassoio: si raggiungono a carapace tolto.
- **Spie dei rail** (X13): due linguette sul tetto dietro il portafusibile con i fori dei LED da 3, rivolti verso la porta di coda.
- **ToF frontale** (X8): la scheda inclinata di 20° sta nella mensola della camera, rifatta come sede; la mensola ora tocca la torretta, così la parte dietro la scheda resta attaccata. Nella visiera c'è la finestra a tronco di piramide sul campo (60° più 0,8 di margine), sotto l'occhio fra z 1 e 11, e un **tappo nero** a incastro finché il sensore manca (`Corpo_Tappo_ToF`). La cima della scheda passa a 0,4 dalla bugna dell'occhio e a 0,2 sotto la testa della camera: posizione del sensore sulla scheda e fori C.
- **INA260** (X7): su due **supporti** separati (`Corpo_Supporto_INA260_S` e `_D`, PETG-CF), appoggiati alla faccia interna della slitta del regolatore con un labbro sul suo bordo e fermati dalla sua vite. La slitta destra è la sinistra ruotata: un prolungamento della slitta sarebbe finito a destra dentro il giro della coxa AD. Morsettiera in basso, sotto i cavi dei servo.
- **Carapace**:
  - **anello di stato** del pulsante, Ø 18–22, bianco a filo nella fascia, assottigliato da sotto a 0,8. Sotto c'è la **camera nera** Ø 28 × 4, stampata con la fascia, con la tacca per i fili dei due pixel;
  - sedi delle **luci dei lobi** (piastrina 5 × 22 con due ganci) sotto ogni lobo, sulla direzione neutra della zampa;
  - **ganci** per il cavo della catena lungo i fianchi;
  - **bugne dello zaino** con inserti M2 messi dall'alto, a 58 × 23 sopra l'ottagono di servizio, lontano dall'antenna dell'ESP32. Lo zaino si avvita con viti M2 nei fori da 2,7 del Radxa: non serve una voce nuova;
  - **microfoni**: fori Ø1 in fascia e carapace con l'anello per la guarnizione e la sede della scheda capovolta;
  - bugne per **scheda del carapace** (X2) e **amplificatore** (X17), appesi al dorso davanti all'ottagono, sopra ESP32 e flat della camera. L'amplificatore sta sopra l'antenna dell'ESP32, a una decina di mm, sotto la plastica: l'effetto sul Wi-Fi è da provare;
  - **altoparlante** su due guide della guancia destra della porta di coda;
  - **ToF posteriore** su un piano inclinato di 35° sulla guancia sinistra. Copre in parte, dall'alto a sinistra, il T-plug visto dalla porta: dal basso si afferra ancora, ma va provato con la mano.
- **Sportellino per lo zaino** (`Corpo_Sportello_Servizio_Zaino`): come quello normale con la tacca per il cavo USB-C. Si stampa solo con lo zaino; quello normale non cambia.
- **FSR** nella zampa (`Rif_FSR_400`, istanza sotto la punta della tibia).
- Non fatti, restano "posto da trovare": INA3221 (X15), sede del CAP1188 (X18), linee di luce della fascia (X22, fuori finché l'utente non le chiede); clip del bus fra SSC-32 e vassoio (bastano le fascette).
- Verificato:
  - istanze del corpo e della zampa al loro posto (scarto 0,000);
  - assieme senza interferenze;
  - coxe libere a ±35° e zampe vicine libere a 31°, a contatto a 32°;
  - carapace contro le zampe AS, MS e PD: distanze invariate;
  - sfilamento del carapace libero da +5 a +40 mm (a −2 tocca, come prima): altoparlante, microfoni, ampli, scheda del carapace, ToF posteriore e tappo salgono con il carapace;
  - campo della camera libero;
  - cicli a tripode 100/45 (8 fasi), 70/70 (16 fasi) e rotazione a 30°: nessun urto;
  - zampa con l'FSR: 81 pose libere e 17 controlli su 20.
- Masse: modellato 2625 g, atteso circa 2985 con tutte le predisposizioni montate. Il femore va al 52,1 % dello stallo a 100/45 (5,73 kgf·cm).

**Blocco C — attrezzi da banco** (fatto e verificato il 10 ottobre, `cad/script/attrezzi.py`, STL in `cad/stl/attrezzi/`):
- **Dime di posa**, due per tutte le zampe, uguali perché le zampe sono la stessa zampa ruotata:
  - `Dima_Posa_1`: imbardata 0°, femore 0°, ginocchio 90°;
  - `Dima_Posa_2`: imbardata +30°, femore +45°, ginocchio 135°.
  Sono le due pose della taratura a due punti di `software.md` 2.7.
- **Come è fatta.** La dima è una piastra che si infila sui due perni del femore dal lato B, con la lama B tolta (due viti), e si appoggia ai mozzi. Ha tre denti:
  - contro la faccia +X della culla della coxa (femore);
  - contro la faccia −X della culla della tibia (ginocchio);
  - con un braccio contro il fianco della cassa del servo di coxa, che sta nel corpo (imbardata).

  Non servono facce nuove sulle parti. Le tre facce sono quasi radiali rispetto al loro asse: ruotando il giunto il punto di contatto si sposta lungo la normale della faccia, circa 0,4 mm per grado.
- **Verificato sulla zampa AS** atteggiata nelle due pose:
  - nessun urto con zampa e corpo;
  - i tre denti a distanza 0,000 dalle loro facce;
  - controllo a ±2°: il dente del femore urta la coxa a −2°, quello del ginocchio la tibia a 88°, quello dell'imbardata la cassa a +2°; dall'altra parte resta libero.

  In taratura quindi si porta il femore giù contro il dente, il ginocchio a chiudere e la coxa in senso antiorario, a passi di 1 e 10 µs. Passa da pochi decimi di millimetro di gioco a contatto: la precisione attesa è quella della stampa più la taratura (±0,5° circa, C).
- **Cavalletto** (`Attrezzo_Cavalletto`, PETG-CF, 222 cm³):
  - culla sotto la chiglia fra x −30 e +30, con labbri sui fianchi alti 8 mm, sotto il ripiano delle baie; resta lontana dallo sportello della batteria e dalle viti;
  - colonna cava 60 × 40 e base 160 × 120. Il tavolo sta a z −170, perché il piede più basso arriva a −159 con femore −49 e ginocchio 139.
  - Verificato: nessun urto con il robot, né con le zampe AS, MS e PS in 18 pose basse e ripiegate (imbardata −35, 0, +35; femore −45 e −49, ginocchio al minimo e a 139).
