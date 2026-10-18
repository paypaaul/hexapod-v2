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

## D-012 — Seriale ESP32 ↔ SSC-32: UART1, TX su GPIO21, RX su GPIO14, 115200 baud, traslatore di livello (ereditata dalla versione MG90S, registrata qui il 15 ottobre 2026)

Presa il 8 ottobre 2026 nel registro della versione MG90S (`git show mg90s:docs/decisioni.md`, D-012), che usava GPIO47 per la RX. Qui vale con una differenza: la RX è su GPIO14, perché GPIO47 è la SDA del bus dei sensori (`piano-elettronica-software.md`, tabella dei GPIO). I GPIO dell'ESP32-S3 non tollerano 5 V e la sua uscita a 3,3 V non garantisce la soglia alta di un ATmega a 5 V: serve un traslatore su entrambe le linee, con le resistenze di pull-up che tengono a riposo la linea al reset. A 115200 baud un comando per 18 servo dura circa 12 ms. Il baud reale della scheda si legge sui LED. La voce esiste perché `cablaggio.md`, il piano elettronico e la guida la citano (P-091).

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
- **Aggiornato dalla 2.1.7 (D-076)**: il vassoio non sta più su distanziali M3 ma su quattro colonne della base con inserti M2 e M2 × 5 svasate (P-003, B18 tolto); le fessure del tetto sono aperte verso la coda, così il pacco si sfila con T-plug e JST-XH attaccati (P-001); i rebbi dello sportello sono da 22,5 per il pacco misurato di 139,65 mm (P-007).

## D-052 — Dettagli del corpo (v0.4, 2026-10-09)

- **Fissaggio del coperchio**: quattro colonnine Ø7,4 sul tetto del tunnel, alte fino al lato inferiore del dorso, con inserto M3 in testa; il coperchio si avvita con 4 viti M3 × 8 (1,6 di dorso + 6,4 nell'inserto da 6,7). Posizioni scelte negli unici corridoi liberi del tetto: davanti a x 40 e |y| 22,5, tra il vassoio (|y| fino a 16,5) e il fianco del tunnel; dietro a x −56, tra il portafusibile F1 (fino a −61,4) e la SSC-32 (da −50,8), con 1,5–2,3 mm d'aria. Scartata la prima idea, colonnine accanto alle gondole medie: a x 14 toccavano le alette dei servo di coxa medi (ingombro fino a |x| 10,3) ed entravano nell'ingombro dei regolatori. Il coperchio appoggia anche con le gonne sull'orlo delle pareti delle baie. Al posto delle "linguette e 2 viti" previste: niente parti in più e nessun aggancio da provare.
- **Ventilazione dei regolatori**: cinque feritoie 6 × 3 per lato nel ripiano delle baie anteriori e cinque sopra, nel dorso del coperchio, allineate sul corridoio d'aria tra i componenti dei regolatori (|y| da 33,4) e il fianco del tunnel (|y| 27): l'aria entra da sotto e sale lungo i componenti. Nel coperchio i fori sono tagliati dopo i lobi, che altrimenti li richiuderebbero.
- Verificato sul modello: colonnine piene, inserti e fori del dorso allineati (prova a punti), feritoie aperte in base e coperchio, nessuna interferenza nella posa di riferimento, coxe libere a ±35° e tra vicine a 31°, ciclo a tripode libero a 70/70. Massa in più circa 5 g.

## D-053 — Basetta dell'ESP32 (2026-10-09)

- La millefori 50 × 70 (voce C2) si **taglia a 56 × 35** e sta sul vassoio da x 22 a 78, |y| fino a 17,5, da z 5,9 a 7,5: intera non entra (le colonnine del coperchio sono a 18,8 dall'asse). Porta i due strip femmina dell'ESP32 (file dei pin da x 22,5 a 73,3, a |y| 12,35) e, tra le due file, sotto il circuito dell'ESP32, regolatore 5 V (B2), traslatore (C1), partitore (B10) e accensione del rail (B11): 8,5 mm d'altezza (6,6 sotto la sede della microSD, da x 22,5 a 37,5).
- Si fissa con **4 viti M2 × 5** in inserti M2 su quattro colonnine del vassoio (Ø5,8, alte 3,3: la luce copre le teste delle viti M3 del vassoio e le saldature). Colonnine tra le due file di pin, a (29, ±6,8) e (75,5, ±6,5), fuori dalle teste M3 del vassoio; i quattro fori nella basetta si trapanano a Ø2,2 sulle colonnine.
- Verificato sul modello: nessuna interferenza; 3,1 mm dalla morsettiera della SSC-32, 1,0 dalla base, appoggio sulle colonnine e sotto gli strip dell'ESP32.
- **Aggiornato dalla 2.1.7 (D-076)**: l'interasse delle file di pin dell'ESP32 è 25,4 (10 passi, P-005), quindi le file stanno a \|y\| 12,7; il vassoio sta su colonne della base e le teste delle viti svasate restano a 3,4 mm sotto la basetta; l'asola del bus è fuori dalla basetta (P-019).

## D-054 — Fissaggio dello sportello della batteria (2026-10-09)

- Lo sportello si infila e si sfila **lungo X** (i rebbi entrano per 17 mm dietro il pacco: una cerniera o un aggancio in alto che ruota non li lascerebbe uscire). Si ferma con **due viti M3 × 8** in basso, in inserti di due blocchetti della chiglia fuori dal tunnel (x da −85,4 a −77,4, |y| da 26 a 32,2, tutta l'altezza della chiglia: stampa senza sbalzi), e con una **linguetta** in alto, larga 16 e profonda 6, che entra sotto il tetto (0,4 mm dal tetto, 1,0 sopra il pacco): se la parte alta prova ad aprirsi, la linguetta sale contro il tetto dopo circa 1 mm.
- Scartate: guide verticali con lo sportello che scende dall'alto (a robot capovolto si sfila da solo), aggancio nelle fessure dei cavi più viti in basso (i rebbi non escono ruotando), viti in alto (nessun posto: tetto da 2 mm, F1 a 2 mm dalla coda, sedi dei servo posteriori accanto al tunnel), denti a scatto (forza di sgancio da tarare, nessuna leva raggiungibile).
- Cambio della batteria: due viti, si sfila lo sportello, si sfila il pacco. T-plug e F1 restano raggiungibili dal retro senza togliere lo sportello.
- Verificato: nessuna interferenza; distanza minima dalla coxa posteriore che ruota: chiglia 2,35 mm (1,83 a +35°), sportello 3,98 mm (2,16 a +35°): per questo le viti sono a |y| 28,5 e non 29. Coxe libere a ±35° e tra vicine a 31°, ciclo a tripode libero a 70/70.
- **Aggiornato dalla 2.1.7 (D-076)**: il pacco si sfila dalle tacche aperte del tetto con le spine attaccate (P-001); rebbi da 22,5 (P-007); la linguetta resta a 0,4 mm dal tetto.

## D-055 — Wago in piedi, fissaggio di F1 (2026-10-09)

- **Errore trovato**: i due Wago 221-415 sdraiati sul ripiano delle baie posteriori (D-051) avevano gli ingressi dei fili a 1,4 mm dalla parete della baia (la baia è larga 21 mm, il Wago è profondo 18,6): i cavi da 12–16 AWG non sarebbero entrati. Ora stanno **in piedi**, con gli ingressi in alto (fili dall'alto, sotto il coperchio) e le leve verso la parete della baia (12 mm d'aria per aprirle), il dorso a 0,5 mm dal fianco del tunnel; x da −46 a −16, z da −29,95 a −11,35.
- **Sede dei Wago** stampata con la base: due spalle alle estremità (alte 6, gioco 0,2) e due labbri da 1,6 che coprono 1 mm delle estremità della faccia delle leve, fuori dalle leve. Il Wago entra dall'alto e resta fermo tra spalle, labbri e fianco del tunnel; se al banco balla, una goccia di colla a caldo.
- **F1**: due costole sul tetto (alte 3, larghe 24, gioco 0,2) lo fermano lungo X; lo stringe al tetto una fascetta da 2,5 mm (voce D11) che passa nelle due fessure dei cavi a x ≈ −76, fuori dalla linguetta dello sportello e dalle uscite dei fili del portafusibile. La coppia di T-plug resta appoggiata sopra F1, tenuta dai suoi cavi.
- Verificato: nessuna interferenza; coxe libere a ±35° e tra vicine a 31°, ciclo a tripode libero a 70/70.
- **Aggiornato dalla 2.1.7 (D-076)**: il dentino per la fascetta di F1 è fatto come due tacche sui bordi della lingua (2,9 lungo X, profonde 1, a x −76), perché un dente nella fessura fermerebbe i cavi in uscita.

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
- **Aggiornato dalla 2.1.7 (D-076)**: la stretta del piedino sullo stinco è il parametro `pied_stretta` (oggi 0) e il provino 6 stampa tre piedini, 0 / 0,2 / 0,4 (`cad/stl/attrezzi/Piedino_stretta_*.stl`, P-016).

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

## D-066 — Versione 2.1.0: predisposizioni per sensori, luci, audio e computer di bordo, attrezzi, software S0 (2026-10-09…10)

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

  In taratura quindi si porta il femore giù contro il dente, il ginocchio a chiudere e la coxa in senso antiorario visto dall'alto, a passi di 1 e 10 µs. Passa da pochi decimi di millimetro di gioco a contatto: la precisione attesa è quella della stampa più la taratura (±0,5° circa, C).
- **Cavalletto** (`Attrezzo_Cavalletto`, PETG-CF, 222 cm³):
  - culla sotto la chiglia fra x −30 e +30, con labbri sui fianchi alti 8 mm, sotto il ripiano delle baie; resta lontana dallo sportello della batteria e dalle viti;
  - colonna cava 60 × 40 e base 160 × 120. Il tavolo sta a z −170, perché il piede più basso arriva a −159 con femore −49 e ginocchio 139.
  - Verificato: nessun urto con il robot, né con le zampe AS, MS e PS in 18 pose basse e ripiegate (imbardata −35, 0, +35; femore −45 e −49, ginocchio al minimo e a 139).
- **Aggiornato dalla 2.1.7 (D-076)**: la sede delle luci della tibia arriva a Z −83,5 (50,5 di lunghezza, P-062); la gola del fermo dei fili è larga 4,5 (P-063); l'asola del bus è 7 × 4 fuori dalla basetta, in un'ala del vassoio (P-019); le linguette delle spie dei rail (X13) stanno a \|y\| 14–20.

## D-067 — Versione 2.1.1: camera dell'anello, fermo dei fili della tibia, cablaggio (2026-10-10)

Correzioni chieste dall'utente il 10 ottobre, sullo stesso design "Hexapod v2.1.0" (nessuna copia del file Fusion), tag `v2.1.1`. Piano in `piano-v2.1.0.md`, ultima sezione.

- **Striscia LED** (X9): WS2812B-2020 a **60 LED/m**, larga 4 o 5 mm. È la densità che il produttore Superlighting elenca per le strisce 2020 da 4 e 5 mm; a 100 LED/m ho trovato solo un'inserzione esaurita, e 120 e 160 LED/m solo da rivenditori senza scheda tecnica. Un solo tipo di striscia per tutte le luci: un pixel misura 16,7 mm. **Corretto in D-068**: la 2020 a 60 LED/m su 4–5 mm non esiste; si usa quella a 120 LED/m.
- **Camera nera dell'anello del pulsante** (X11): da Ø28 × 4 a **Ø32 × 6**. Con Ø28 fra il dado del pulsante (r 8,65) e la parete restavano 4,15 mm, e un pezzo di striscia largo 5 non entrava. Il limite di 28 veniva dalle linee di luce della fascia (X22), che non si fanno.
  - **Fondo** nuovo, `Corpo_Fondo_Anello` (PLA nero, 0,96 cm³): disco con una gonna che calza da sotto la parete della camera (0,05 di gioco per lato, forzamento leggero da tarare), con il foro per il corpo del pulsante e **due sedi da un pixel** (17,1 × 5,4 × 0,4) ai lati del pulsante, a Y ±(6,5…11,9). I LED stanno a r 9,2, sotto l'anello (r 9–11).
  - I pixel passano **sotto il dado** del pulsante: per questo la camera è alta 6. Dal pezzo di striscia al dado restano 3 mm con il dado alto 2 dell'ingombro (C). Due pezzi da un pixel e non un pezzo da due, che a 60 LED/m è lungo 33,3 e chiederebbe una camera di circa Ø43. Il ponticello di 3 fili fra i due pezzi gira attorno al corpo del pulsante sul lato della testa. Con la striscia di D-068 ogni sede porta 2 pixel: l'anello ne ha 4.
  - La **tacca** dei fili nella parete, verso la coda, passa da 3 × 2 a 4 × 3: due fili da 3 a 30 AWG, in entrata e in uscita, sopra la gonna.
  - Verificato: assieme senza interferenze; il fondo tocca solo la camera (appoggio), con 0,1 mm dal corpo del pulsante, 3,3 dalla zona delle spine della SSC-32, 3,8 dal carapace e 5,9 dallo sportellino. Sfilamento del carapace libero da +5 a +40 con il fondo che sale insieme a lui. Il volume della camera (682 mm³) e quello del fondo (955 mm³) coincidono con il calcolo a mano.
- **Luci dei lobi** (X12): **un pixel per lobo** invece di due. La sede 5 × 22 della 2.1.0 era stata pensata per due pixel a 100 LED/m. A 60 LED/m due pixel sono lunghi 33,3. Sotto il dorso piano del lobo, nella fascia della sede (17 ± 2,5 mm dall'asse della coxa), la larghezza è di 27–32 mm (calcolo dai parametri del lobo, S), e con i ganci ne servirebbero 36. Un pixel da 16,7 entra nella sede di oggi. La catena del carapace ha così 8 pixel: 2 dell'anello e 6 dei lobi. **Corretto in D-068**: con la striscia a 120 LED/m due pixel sono lunghi 16,7 e i lobi tornano a 2 pixel.
- **Fermo dei fili della tibia**: gola larga 4 e profonda 0,8 sulla parete +X della culla, da Z −33 a +12,45 (la testata), a Y 4,4…8,4.
  - Sta fuori dalle finestre a rombo e dai tappi del guscio, che arrivano a Y 3,5. Tiene il doppino dell'FSR (28 AWG siliconico, circa Ø0,9, S) e i 3 fili della striscia da 30 AWG.
  - Tre **ponticelli** a Z −28, −10 e +6, staccati 0,3 dalla parete: sotto restano 1,1 mm. Sporgono 1,1, dove il guscio è a 4–5,7 dalla parete. La tibia si stampa sul fondo della culla, quindi i ponticelli crescono come pareti in piedi, senza supporti.
  - Una prima versione larga 3,2, con i ponticelli a filo, era pensata per fili da 30 AWG. Il doppino dell'FSR è da 28 AWG (X5) e lì non passava: è stata rifatta prima delle verifiche finali.
  - Verificato: tibia un solo corpo, volume −115,5 mm³ come da calcolo; zampa senza interferenze; 81 pose libere e 17 controlli su 20 che toccano, come prima. Assieme senza interferenze, dime con i denti a contatto, cavalletto libero nelle 18 pose.
- **Cablaggio**: schema e tabelle di tutti i cavi in `cablaggio.md`. Restano aperti:
  - le prese delle luci delle tibie, non ancora nel CAD;
  - il ramo delle tibie, che ripete i primi tre pixel della catena, cioè l'anello e il primo lobo;
  - il tetto di corrente, che deve contare sei volte i pixel delle tibie;
  - i pettini delle anse.
- **Esportazione**: `esporta_robot.py` scrive i JSON in UTF-8 esplicito. Il 10 ottobre il Python di Fusion aveva l'ASCII come codifica predefinita, e la "Ø" di un commento ha interrotto la scrittura di `cad.json`.
- Masse: tibia 111,9 g a segmento, corpo 1064,7; modellato 2627 g, atteso circa 2987.

## D-068 — BOM con prezzi e link; striscia LED a 120 LED/m (2026-10-10)

Chiesto dall'utente il 10 ottobre: BOM con prezzi e link d'acquisto al prezzo migliore e stima del totale. Scelte dell'utente:
- prezzi per le voci approvate, con il loro totale, e un totale a parte per le predisposizioni X;
- "prezzo migliore" vuol dire costo consegnato in Italia, spedizioni comprese, con pochi negozi;
- AliExpress va bene per la minuteria, sempre con l'alternativa europea.

- **Come**: due giri di ricerca con 10 ricercatori e 10 verificatori (Sonnet). I verificatori hanno riaperto ogni link e corretto prezzi, spedizioni e codici. I totali sono calcolati da uno script sulle righe, non a mano.
- **Carrelli delle voci approvate** (BOM, "Carrelli e costo totale"): circa **486 €** consegnati (496 € dopo i prezzi letti in Chrome, vedi sotto), contro i circa 480 stimati nella v2.0.
  - **Kamami**: regolatori Pololu e quasi tutta la minuteria, 185 €. Le spedizioni lette sono 8,24 € (Kamami) e 25,90 € (Gedex); quelle di Amazon e AliExpress sono stime.
  - **3DJake.it**: filamenti, 102 €.
  - **Gedex**: viti DIN 912 inox nelle quantità esatte, 53 € con 25,90 di spedizione.
  - **AliExpress**: squadrette, circa 25 €.
  - **Amazon.it**: 13 voci di minuteria, circa 121 €. Amazon non è leggibile dagli strumenti, quindi queste sono stime S.
- **Fuori dal totale**: D1 e D2 (le procura l'utente) e le voci da approvare (D8b, E2b, C7).
- **Predisposizioni X**: alte circa 177 €, alte e medie circa 267 €, tutte circa 569 €, con le spedizioni.
- **Sostituzioni trovate nei negozi**:
  - C1: modulo KAmod a 4 canali al posto dell'Adafruit 757; il tipo di MOSFET va confermato;
  - C3: diodo 1N5819 al posto del 1N5817;
  - X9: buffer SN74AHCT125N in DIP-14 per la millefori;
  - X13: LED giallo 590 nm, perché l'ambra non c'è a magazzino;
  - X17: altoparlante CMS-15113-078SP-67 (IP67);
  - X33: seesaw ATtiny1616 (#5690).
  - Il condensatore EEU-FR1C222 è alto fino a 22 mm, non 20.
- **Striscia LED**: corregge D-067. Sulle pagine del produttore Superlighting la WS2812B-2020 a 60 LED/m su FPC da 4–5 mm **non esiste**: la 60 LED/m da 4 mm usa LED 3535, alti 2,5 mm. La 2020 esiste a 90, 96, 120, 160 e 200 LED/m. Si sceglie la **2020 a 120 LED/m, FPC 4 mm, spessa circa 1 mm** (Superlighting p-4003), con un pixel ogni 8,33 mm e taglio a ogni LED.
  - Le sedi del CAD non cambiano. Erano fatte per 16,7 × 5 mm e ora portano 2 pixel ciascuna; lo spessore di 1 mm sta sotto l'1,4 previsto.
  - **Anello**: 4 pixel, 2 per sede. I LED stanno a r 10,1, proprio sotto l'anello (r 9–11).
  - **Lobi**: tornano a **2 pixel**, 16,7 mm nella sede da 22.
  - **Tibie**: 6 pixel per tibia, 50 mm.
  - La catena del carapace ha 16 pixel. Il ramo delle tibie ripete i primi 6 e porta 36 pixel reali: il tetto di corrente del firmware deve contarli.
  - La striscia viene da fuori UE: dogana possibile.
  - Cambiano solo i commenti dei parametri `luc_pix_*`; `cablaggio.md`, `predisposizioni.md` e il BOM sono aggiornati.
  - **Correzione, stesso giorno**: cercando in Chrome, su AliExpress un'inserzione ([1005009482531544](https://it.aliexpress.com/item/1005009482531544.html)) vende la 2020 su FPC da 4 mm a 60, 90, 120 e 200 LED/m. Quindi la 60 LED/m esiste; è il produttore Superlighting a non elencarla. Si resta a 120 LED/m, che dà 2 pixel per sede e i lobi a 2 pixel, e la si compra lì: 11,79 € al metro con la spedizione gratuita, invece di Superlighting.
- **Prezzi Amazon.it e AliExpress letti in Chrome** (10 ottobre, su richiesta dell'utente): sul Mac dell'utente, con una scheda comandata via AppleScript, che apre le pagine di ricerca e di prodotto e legge prezzi, varianti, ASIN e foto. Le stime S di quei negozi sono diventate prezzi letti. Le viti passano da Gedex ad Amazon: kit inox più due confezioni, 42,03 € contro 53,03. Il totale delle approvate è circa **496 €**. Nel BOM c'è una colonna con la foto di ogni voce: sono link alle immagini dei negozi e dei produttori, non copie nella repo.

## D-069 — Versione 2.1.2: scelta delle predisposizioni, prese delle luci, provino di luce (2026-10-10)

L'utente ha chiesto di fare chiarezza sulle predisposizioni con sei classi: importanza (importante, good-to-have, superfluo) per posto nel CAD (c'è o no). Dove c'è il posto la predisposizione si approva; dove manca, l'importante cerca opzioni e il resto va in backlog. Tre giudici indipendenti hanno classificato le voci, ognuno da un punto di vista: camminata e sicurezza, esperienza d'uso, costo e complessità. Ha deciso la maggioranza. Il posto nel CAD viene dal modello. L'utente ha approvato tutto il 10 ottobre.

- **Importante, con posto** → approvata: X1, X2, X4, X5, X6, X7, X8, X9, X11, X13. Circa 45 g e 135 €, meno di un punto di coppia al femore.
- **Importante senza posto**: nessuna voce.
- **Good-to-have, con posto o senza CAD** → approvata: X3 (si compra solo se il 3,3 V della scheda non regge), X10, X12, X14 (2 NTC, non 3: l'ADC ha 8 canali e 6 sono dei piedi), X19 con X20, X23, X24, computer di bordo a zaino.
- **Good-to-have senza posto** → backlog: X15 (correnti dei femori: ridondanti con X5 e X7, 16 g, sopra i Wago non ci sta), X32 (angolo vero dei servo: va aperto ogni servo, servono ADC in più).
- **Superfluo, con posto** → approvata: X16, X17 (scelta dell'utente del 9 ottobre), X31 (sede e fermo già fatti, il guscio non cambia).
- **Superfluo senza posto o con costo d'aspetto** → backlog: X18, X21 (le fessure si vedrebbero anche spente), X22, X25, X26, X27, X28, X29, X30, X33. Nessuna di queste ha sedi nel modello: non c'è niente da togliere.
- **Tocco senza X18**: colpetto e doppio colpetto dall'IMU, pressione localizzata dal centro di pressione degli FSR, molleggio con controllo di ammettenza e passo di recupero, lenti e morbidi con gli MG996R (`software.md` 4.3b). La carezza leggera resta solo con X18.
- **"Predisposizione approvata" vale per CAD e documenti**: l'acquisto di ogni voce resta da approvare nel BOM.

Modifiche al CAD (stesso design "Hexapod v2.1.0", versione 10 del file, tag `v2.1.2`):
- **Prese delle luci delle tibie**: seconda fila di sei spine JR sul tetto del tunnel, speculare a quella dei piedi, x 48…64, y −25…−22.
  - `corpo.py` → `_prese`, fatta anche da `fai_base_predisposizioni`; il passo `prese_luci` è servito una volta sola. Istanza `Prese_luci` in `assieme.py`.
  - Volume +0,150 cm³ come da calcolo, base di un solo corpo, istanze al loro posto, assieme senza interferenze.
- **T-plug con il ToF posteriore**: visto da dietro il ToF copre solo l'angolo in alto a sinistra del T-plug (3 × 3 mm) e sta 8 mm più indietro. Lo spazio stretto viene dalla porta, larga 50,8:
  - aria attorno al T-plug: 3,3 mm sotto il cicalino, 7 mm verso l'altoparlante, 10,4 mm verso la guancia sinistra;
  - sotto c'è il portafusibile.
  Alzare il ToF non aiuta, e a z 19 c'era stato messo per non toccare il bordo della fascia. Si prova a mano sul primo carapace; il ripiego è una linguetta di nastro sulla metà lato batteria.
- **Provino di luce** (X10): `Attrezzo_Provino_Luce_Nero` e `_Bianco`, da stampare insieme in due colori con il fondo sul piatto (`attrezzi.py` → `provino_luce`).
  - Tre camere profonde 2, 4 e 6 mm, ciascuna con quattro strisce di bianco da 0,4, 0,8, 1,2 e 1,6.
  - L'anello del pulsante come sul carapace: camera Ø29,6 × 6, bianco 1,6 con l'intarsio nero da 0,6, anello assottigliato a 0,8.
  - Canali sotto per uno spezzone di striscia da 120 LED/m.
  - Volumi del bianco come da calcolo (288 mm³ per camera, 663 per l'anello).
- **Cablaggio**: chiusi gli aperti 1 (prese delle luci) e 6 (Wago positivo a sinistra, negativo a destra).
- **Masse**: corpo 1067,9 g a segmento; modellato 2630 g, atteso circa 2990.


## D-070 — Versione 2.1.3: lame del femore come il guscio della tibia (2026-10-11)

L'utente voleva una cover anche sopra il femore (backlog del 9 ottobre). Le prove sono in `docs/ricerca/estetica/8-placca-femore/`:
- tre concept: finestra larga, feritoia come la tibia, due cappucci;
- la finestra larga rifinita;
- lame come la tibia con strisce strette da lama a lama.

Alla fine ha scelto così:
- **lame laterali nello stile del guscio della tibia, con la feritoia, chiuse anche sulle teste dei bulloni**;
- **nessuna copertura superiore**.

Le strisce hanno vincoli che le verifiche sulle mesh hanno mostrato (`concept4.py`):
- sopra l'anca una striscia da lama a lama urta il ponte della coxa fino a X 78;
- da X 86 in avanti si può fare, ma non copre più l'uscita del cavo;
- una linguetta della sola lama B all'utente non piaceva.

Lame (`zampa.py` → `_cover_femore`, parametri `cov_fem_*`; tolti i 15 parametri delle lame bombate di D-061):
- **Sagoma**:
  - da X 40 a 135,5 e da Z −14,5 a 20, con tre angoli smussati: in alto e in basso verso l'anca, in basso oltre il ginocchio;
  - si stringe verso l'anca come la tibia verso il piede.
  - Il bordo alto è dritto. Un bordo che sale verso il ginocchio (provato nei concept) porta la lama a 1,4 mm dal carapace con α 85 e coxa a ±35.
- **Faccia esterna** piana con lo smusso 3 × 2 tutt'attorno (3 in pianta, 2 nello spessore). Uno smusso a 45° da 3 mm non ci stava sulla lama B senza lasciare un bordo a lama di coltello.
- **Lama A**:
  - spessa 4,0 mm, da \|y\| 30,55 a 34,55;
  - tasche cieche per le 12 teste M3: teste da 3,0, gioco 0,2, pelle 0,8;
  - resta a incastro sulle 4 teste del blocco (Ø5,6 come prima); le 8 teste delle squadrette stanno libere in tasche Ø6,2.
- **Lama B**:
  - spessa 2,6 come prima, fino a 33,15;
  - tasche Ø5,6 sulle punte dei perni, che sporgono 1,4;
  - restano le due viti M2 × 6 svasate (D-065).
- **Feritoia**: intarsio di PLA nero (`Cover_Femore_A_Feritoia`, `_B_Feritoia`), a filo della faccia, stampato insieme alla lama come la fascia del carapace (D-063).
  - Asola 37 × 7 con gli estremi tondi, a metà fra gli assi (X 87,5), a Z 6.
  - Sulla lama A è profonda 0,6. Copre le tasche delle due teste basse del blocco, e sopra resta 0,2 di bianco.
  - Sulla lama B è profonda 1,0: contiene tutta la svasatura delle due viti, che stanno nere dentro il nero.
  - Una feritoia passante avrebbe lasciato a vista due teste.
- **Stampa**: faccia interna sul piatto; le tasche sono fori ciechi che partono dal piatto.
- **Dime di posa**: si usano con la lama B smontata, come prima.

Verifiche nel CAD (design "Hexapod v2.1.0"):
- **Lame**: un corpo ciascuna, smusso dalla parte giusta al primo colpo, faccia piana da X 43 a 132,5 e da Z −11,5 a 17. Volumi:
  - lama A 10,752 cm³, lama B 7,196;
  - intarsi 0,149 e 0,232 cm³, come il calcolo dell'asola.
- **Sentinella**: le altre parti della zampa hanno gli stessi volumi di prima.
- **Zampa**: nessuna interferenza; 81 pose libere su 81; 17 controlli su 20 toccano, come prima.
- **Assieme**:
  - nessuna interferenza; coxe libere a ±20 e ±35;
  - **zampe vicine libere a 30,5° e a contatto a 31°** su tutte e quattro le coppie laterali, lama A contro lama B; prima tra 31° e 32°;
  - gioco a 30° di 3,58 mm, prima 4,6; anteriori e posteriori libere a 34°;
  - il firmware resta a ±30° e a 56° di somma (`software.md`): restano 3° per zampa.
- **Carapace** con (85, 90), (85, 29), (60, 90) a imbardata −35, 0, +35: nessun urto.
  - Distanza minima 3,96 mm sulle zampe medie (prima 4,6), 7,1 sulle altre.
- **Cicli**: 100/45 e 70/70 e rotazione sul posto a 30° (a 100/45 e 70/70) liberi, otto fasi ciascuno.
- **Masse**:
  - il femore passa da 54,4 a 66,2 g a segmento (lama A 12,0 g, B 8,9, intarsi 0,5);
  - modellato 2700,6 g, atteso **3060,6 g**, prima 2990; aggiornato in `calc/statica_tripode.py` e `robot.yaml`;
  - al punto di progetto 100/45 il femore sale dal 51 % al **53 % dello stallo** (5,87 kgf·cm), la tibia al 49 %;
  - regressioni di Python e del nucleo aggiornate; nella simulazione il contatto fra vicine è a 31°, come nel CAD.
- **Se servisse togliere peso** (corretto l'11 ottobre 2026): la testa bombata ISO 7380 non va, perché la lama A si incastra sui fianchi cilindrici delle teste del blocco e una testa a cupola non la terrebbe. La testa svasata non va sulle viti del blocco, perché passano la piastra di Femore_A da 2,4 e la svasatura (1,86) lascerebbe 0,5 mm. Va la **testa cilindrica bassa DIN 7984** (alta 2,0, Ø5,5 come la ISO 4762) sulle 12 viti per zampa sotto la lama A: la lama scende a 3,0, il contatto tra vicine torna verso 31,25°, la massa cala di pochi grammi. Cambiano 72 viti del BOM: va approvato dall'utente.

## D-071 — Versione 2.1.4: lame del femore con la sagoma del femore, feritoia al centro (2026-10-11)

Sulle lame della 2.1.3 (D-070) l'utente ha detto che escono troppo dalla forma del femore senza avvolgerla, "una placca un po' buttata lì". Ha chiesto la sagoma delle lame di prima (D-061), che seguono il femore, con l'estetica nuova. Poi ha chiesto di abbassare la feritoia, che stava troppo in alto.

- **Sagoma** come D-061:
  - fascia fra i mozzi a Z ±14,5;
  - teste esagonali con l'apotema 14,5 attorno ad anca e ginocchio;
  - rialzo fino a Z 20 sopra il blocco, con le rampe a 30° verso l'anca e a 45° verso il ginocchio.
  - Il rialzo va da X 80 a 97, prima da 81 a 96: così la tasca della testa alta del blocco lato anca resta sotto la faccia piana, a 0,85 mm dallo smusso invece che dentro.
  - Niente raccordi in pianta: spigoli vivi con lo smusso 3 × 2, sfaccettati come la tibia.
  - Parametri `cov_fem_ap`, `cov_fem_plateau0` e `cov_fem_plateau1`; tolti quelli della sagoma rettangolare.
- **Feritoia a Z 1,5**, quasi al centro della faccia: il baricentro della faccia piana sta a Z 1 circa, per il rialzo. Prima era a Z 6.
  - Le due viti M2 della lama B la seguono, perché devono restare nel nero: passano a Z 1,5 (`cov_vite_b_z`) e quella lato ginocchio da X 94,5 a **X 89** (`cov_vite_b_xg`).
  - A Z 1,5 e X 94,5 il foro dell'inserto avrebbe bucato il taglio basso del blocco, che comincia a X 89,5. A X 89 restano 1,6 mm di parete, e 1,8 sopra il fondo del blocco.
  - In `Femore_B` è cambiata solo la quota dello schizzo dell'inserto, senza rifare il pezzo. I due fori degli inserti sono cilindri interi (42,73 mm² come da calcolo).
- **Resta come in D-070**:
  - lama A spessa 4,0 con le 12 tasche; lama B spessa 2,6 con le tasche dei perni;
  - intarsio nero a filo, 0,6 sulla A e 1,0 sulla B con le svasature;
  - stampa con la faccia interna sul piatto.

Verifiche nel CAD:
- **Lame**: un corpo ciascuna, smusso dalla parte giusta, faccia piana da X 41,72 a 133,28 come da calcolo. Volumi: lama A 9,074 cm³, lama B 6,117; intarsi 0,149 e 0,232.
- **Sentinella**: le altre parti hanno gli stessi volumi di prima; `Femore_B` resta 32,858 perché i fori si spostano soltanto.
- **Zampa**: nessuna interferenza, 81 pose libere su 81, 17 controlli su 20 toccano.
- **Assieme**:
  - nessuna interferenza; coxe libere a ±20 e ±35;
  - vicine libere a 30,5° e a contatto a 31° su AS–MS, MS–PS e MD–PD; AD–MD libere anche a 31°;
  - gioco a 30° di 3,58 mm; anteriori e posteriori libere a 34°.
- **Carapace**: distanza minima **4,58 mm** sulle zampe medie (3,96 nella 2.1.3, 4,6 con le lame bombate), 7,1 sulle altre.
- **Cicli**: 100/45, 70/70 e rotazione a 30° liberi.
- **Masse**:
  - femore 63,3 g a segmento: 66,2 nella 2.1.3, 54,4 con le lame bombate;
  - atteso **3043,5 g**;
  - femore al 53 % dello stallo a 100/45 (5,84 kgf·cm).

> **Nota del 16 ottobre 2026** (verifica della 2.1.7): rifacendo la prova delle coxe vicine sul modello della 2.1.7, con le zampe uguali a quelle di questa versione, a 31° toccano **tutte e quattro le coppie**, anche AD–MD: lama B contro lama A per 18,94 mm³ e feritoia della B contro la lama A per 13,55 mm³ (32,49 in tutto), come MS–PS; AS–MS e MD–PD toccano per 19,06 + 15,56. A 30,5° sono libere tutte e quattro. La riga "AD–MD libere anche a 31°" qui sopra non si ritrova; i versi provati sono quelli di `cad/CLAUDE.md` (a destra AD −, MD +). Il limite del firmware (somma 56° o 60° fra vicine, ±30° a coxa) non cambia.

## D-072 — Versione 2.1.5: provino delle tasche della lama A e render notturno (2026-10-11)

Richieste dell'utente:
- un provino per tarare l'incastro della lama A sulle teste delle viti, da stampare con gli altri provini prima dei pezzi;
- un render "più cinematografico, al buio, con le luci accese".

Il modello del robot non cambia.

- **Provino delle tasche** (`attrezzi.py` → `provino_tasche`, componenti `Attrezzo_Provino_Tasche_Base` e `_Lama` nella zona libreria):
  - **base** in PETG-CF, 24 × 16 × 8, con una vite M3 × 6 ISO 4762 in un foro pilota Ø2,5 come le alette lato albero (D-049). Così non servono dadi né inserti ancora da tarare;
  - **lamina** in PLA bianco spessa come la lama A (4,0), stampata come lei con le tasche sul piatto, sei tasche profonde 3,2:
    - lisce da Ø5,4, 5,5, 5,6 e 5,7 (`cov_testa_d` oggi è 5,6; la testa va da 5,32 a 5,5);
    - due da Ø6,0 con tre costole di schiacciamento che stringono a 5,3 e 5,4: danno una stretta che dipende meno dalla stampante.
  - Da 1 a 6 puntini sulla faccia in alto per riconoscere le tasche.
  - Verificato sul modello: un corpo per pezzo, 4 tasche lisce e 2 con le costole, 21 puntini; volume della lamina 2,867 cm³ contro 2,876 dal calcolo a mano.
  - STL in `cad/stl/attrezzi/`.
- **Render notturno** (`viste.py`: viste `notte_ant` e `notte_alto`, `avvia(..., notte=True)`):
  - ambiente "Evidenziazioni del bordo" quasi spento (luminosità 10 invece di 1000), esposizione 6 EV, sfondo nero, suolo lucido con i riflessi;
  - solo durante il render, il PLA bianco (`Esa PLA placche`) diventa traslucido, così la luce passa attraverso il carapace e i gusci come nel pezzo vero.
  - Le luci sono aspetti emissivi copiati da "LED (blu)" della libreria di Fusion, color ciano. Le WS2812B fanno qualunque colore: per il render ne basta uno, e si cambia in `LUCE`.
    - **Anello del pulsante**: emette la faccia sotto l'anello assottigliato.
    - **Lobi**: due pixel provvisori sotto ogni piastrina delle luci, rivolti verso l'alto, in un componente che `ripristina` cancella. Hanno un aspetto più luminoso, perché la luce attraversa 2,2 mm di PLA.
    - **Diffusori delle tibie**: emettono loro.
    - Spie dei rail non accese: stanno in coda e da queste viste non si vedono.
  - `ripristina` toglie colori delle facce, pixel e traslucenza, rimette i colori di `colori.py` e la scena di giorno. Verificato dopo ogni render: nessun colore sulle facce, PLA opaco, timeline com'era.
  - Ogni render notturno dura 8–9 minuti, contro meno di un minuto per quelli di giorno.
  - Immagini in `docs/immagini/render-notte-ant.png` e `render-notte-alto.png`.

## D-073 — BOM 2.2: quello che c'è già in casa, linea principale in 14 AWG, logica in 26 AWG (2026-10-11)

L'utente ha chiesto di cercare nei suoi ordini Amazon, AliExpress e Temu i pezzi che sostituiscono voci del BOM. Ha approvato le sostituzioni che non cambiano niente in pratica, comprese due sezioni di cavo più piccole ("erano comunque sovrastimate"). Il modello del robot non cambia.

- **Voci tolte dagli acquisti** (stato P nel BOM):
  - B5 portafusibile, B12 T-plug, B14 e B15 cavi di potenza;
  - B7 condensatori da 2200 µF, B8 ceramici da 100 nF (SMD, saldati sui reofori);
  - B17 cavo della logica, guaina di B19;
  - C2 basetta e strip, C4 cavetti Dupont, C7 prolunga di bilanciamento (due codini JST-XH a 3 poli saldati);
  - D8 viti M2 × 5 (a croce, dal kit degli inserti), D8b viti svasate;
  - E2 PLA bianco, E2b PLA nero.
- **Linea principale in 14 AWG** invece che 12: T-plug, portafusibile e cavo arrivano già in 14 AWG. Il tratto è sotto 0,5 m e F1 da 30 A protegge il siliconico da 2,08 mm². Caduta circa 0,1 V a 15 A. Anche le uscite dei regolatori passano da 16 a 14 AWG. Il codino della batteria resta il suo, da 12 AWG.
- **Logica in 26 AWG** invece che 22: il ramo logica sta sotto 1 A, e F2 da 2 A protegge anche il 26 AWG.
- **D8b**: viti M2 × 5 svasate invece di M2 × 6, perché sono quelle in casa. Su 2,6 mm di lama ne restano 2,4 nell'inserto da 3, invece di 3,4: basta per una lama non strutturale. Sono nere e stanno nell'intarsio nero.
- **Risposte alle domande del BOM**: 20 MG996R (domanda 2); 4 schede ESP32-S3 N16R8 CAM e la camera OV3660 da 75 mm (domanda 1).
- **Costo**: da 495,94 € a circa 362,13 € consegnati; circa 332,64 € se basta una bobina di PETG-CF.
- **Non vanno**:
  - per B2, la scheda di distribuzione NISHZHU (7,2 V minimi) e il buck Jadeshay (8 V minimi): la 2S scende sotto;
  - per B1, il buck da 20 A: non ha il pin di abilitazione;
  - i cuscinetti in casa: nessuno è il 5 × 10 × 4 flangiato;
  - il 26 AWG per i fili delle tibie (X5, X31): la gola è larga 4 mm e sotto i ponticelli restano 1,1 mm.
- **Da guardare sui pezzi** (elenco in `CLAUDE.md`, da richiedere all'utente):
  - quale scheda è la RE1.3;
  - diametro e altezza dei condensatori da 2200 µF;
  - testa e lunghezze delle M3 nel kit da 918 viti;
  - misure del set da 500 inserti;
  - lega dello stagno "a bassa temperatura";
  - quanto resta del PETG-CF nero FlashForge.
- **Predisposizioni** (IMU, microfoni, amplificatore e altoparlante in casa): ancora da decidere con l'utente.

## D-074 — Versione 2.1.6: predisposizioni con i pezzi già in casa, IMU e microfoni doppi (2026-10-11)

L'utente ha scelto i moduli che ha già (D-073):
- l'MPU-6500 (GY-6500) al posto della Pololu LSM6DSO, con **doppia predisposizione**: per tornare alla Pololu basta smontare;
- lo stesso per i microfoni: MS3625 montati, Adafruit 3421 predisposti;
- l'amplificatore MAX98357A generico e l'altoparlante tondo da 15 mm.

Piano in `docs/piano-v2.1.0.md`, sezione 2.1.6. Prima del via sono stati controllati i collegamenti.

- **Quote dei moduli**: S, ricavate dalle foto dei venditori con il passo dei pin da 2,54 come scala; C, da guardare sui pezzi (elenco in `CLAUDE.md`).
  - **GY-6500** ("MPU-9250/6500" blu): 26 × 15,5 × 1,6 mm, componenti alti circa 1 mm; 10 pin su un lato lungo; due fori Ø3 sul lato opposto, a 20,6 di interasse e 2,3 dal bordo; asse X del chip sul lato corto.
  - **MS3625**: tonda, Ø13,5, con due lati piatti a 12,6 lungo le file dei pin. La porta è al centro della faccia senza componenti, come la porta sul fondo della Adafruit.
  - **MAX98357A generico**: 17,5 × 17,7 mm; due fori Ø2,4 sul lato della morsettiera, a 13 di interasse e 2,2 dai bordi.
  - **Altoparlante**: Ø15, spessore non dichiarato (4, C).
- **IMU** (`Corpo_Piastrina_IMU`, PETG-CF, 26 × 11,1 × 2,5):
  - la base non cambia, la Pololu si avvita ancora sulle sue bugne;
  - la piastrina va sulle stesse bugne con due M2 × 5 svasate a filo, e porta la GY-6500 con due M2 × 6 in fori pilota Ø1,7;
  - pin verso +Y, scheda a 0,6 dal bordo della scheda dell'ADC e a 0,65 dalla parete del vano; in Z da −2,9 a −0,3, sotto il vassoio a +1;
  - fili saldati sulle piazzole, senza pin.
- **Microfoni**:
  - stesso foro e stesso telaio della Adafruit: la MS3625 ci sta con i lati piatti lungo i lati lunghi, a 0,25 dalle pareti;
  - lungo il telaio la centrano due lunette per microfono (`Corpo_Lunette_Microfoni`, PLA, quattro pezzi simmetrici), che si tolgono per montare la Adafruit;
  - le lunette sono larghe 12 invece di 12,9, perché a 12,9 toccavano per 0,49 mm³ lo smusso del viso.
- **Amplificatore**: le bugne passano sul lato della morsettiera (verso +X), a 13 di interasse. **Quelle in diagonale della 2.1.0 erano sbagliate anche per la Adafruit**, che ha i fori nello stesso punto.
- **Altoparlante**:
  - la guancia è lunga 12,9 e il tondo è Ø15: si centra a x −96,3 contro un fermo nuovo da 1 mm all'estremo anteriore della guancia, e sporge 3,3 mm dietro;
  - le guide restano quelle di prima (15,4 fra le facce interne);
  - lo spazio dietro la guancia è libero, compreso un corridoio di 25 mm per infilarlo da dietro (verificato nel CAD).
- **Collegamenti**:
  - l'IMU usa gli stessi 4 fili (NCS, AD0 e FSYNC già tirati sulla scheda, S) e l'indirizzo 0x68, che non va mai sul bus della camera;
  - i microfoni usano gli stessi sei segnali e GPIO, con **in più un pull-down da 100 kΩ sulla linea dati** (datasheet ADMP441/INMP441), che valeva anche per le Adafruit;
  - l'amplificatore ha gli stessi pin;
  - il volume dell'altoparlante da 1 W va limitato nel firmware;
  - il driver dell'IMU riconoscerà la scheda dall'indirizzo e ruoterà gli assi (`software.md`). I colpetti si riconoscono in software, perché l'MPU-6500 non li fa in hardware.
- **Verifiche nel CAD**:
  - ingombri nuovi con i volumi del calcolo a mano;
  - schizzi vincolati, timeline senza problemi;
  - **sentinella**: cambia solo il carapace, +0,020 cm³ (il fermo); baricentro spostato di 0,01–0,02 mm, quanto danno fermo e bugne;
  - **assieme**: nessuna interferenza; coxe libere a ±35°;
  - **varianti**: la Pololu e le Adafruit montate al posto di GY-6500 e MS3625 non toccano niente; i casi di controllo (senza togliere la variante montata) trovano piastrina, scheda e lunette;
  - **carapace**: sfilamento libero a 5, 10, 20 e 40 mm; campo della camera libero;
  - carapace contro le zampe senza urti: **3,96 mm** sulle zampe medie a +35° (lama A), 4,76 a −35°, 7,1 sulle altre. Il 4,58 scritto in D-071 non si ritrova con carapace e lame identici a quelli della 2.1.5: probabilmente era stato misurato prima di un ritocco alle lame. Il valore buono è 3,96;
  - cicli non rifatti: i pezzi nuovi sono dentro il corpo e il carapace, la forma esterna non cambia.
- **Massa**: attesa **3045,0 g** (+1,5 g); femore sempre al 53 % dello stallo a 100/45 (5,84 kgf·cm), margine di stabilità 59 mm.
- **BOM**:
  - X4, X16 e X17 sono in possesso;
  - le predisposizioni approvate costano circa 42 € in meno (220,26 € invece di 262,12, senza il computer di bordo);
  - il carrello DigiKey scende a 51,22 € e paga 25 € di spedizione, mentre sparisce l'ordine da pololu.com.
- **Aggiornato dalla 2.1.7 (D-076)**: la scheda del carapace ha la testata 2 × 8 a 90° sul bordo di coda e misura 21,5 × 30 da x 29,5 (P-002); il ToF posteriore è avvitato con due fori pilota Ø1,7 e l'altoparlante ha due costole di ritegno a filo (P-008); restano da confermare lo spessore dell'altoparlante (`aud_altt_sp`) e la posizione dei fori del #3415 dai bordi.

## D-075 — Guida di montaggio illustrata: strumenti, formato e regole (2026-10-11)

L'utente ha chiesto una guida di montaggio passo passo, sullo stile delle istruzioni LEGO, in PDF. Scriverla serve anche a riguardare tutto il progetto. Il piano approvato è in `docs/piano-guida.md`.

- **Strumenti**: l'utente lascia libera la scelta, anche di installare.
  - Immagini con **Blender** senza interfaccia, da mesh esportate dal CAD in sola lettura (`cad/script/esporta_guida.py`).
  - PDF con **Chrome** senza interfaccia.
  - La regola "Blender si valuta solo dopo la fase 6" resta valida per gli altri usi (animazioni, simulazione).
- **Parti ripetute descritte una volta sola**: una zampa pilota segnata ×6, e per le altre cinque una scheda a spunta. Nel corpo i passi ripetuti sono uno solo, ×N.
- **Formato**: A4 orizzontale, con l'HTML navigabile accanto.
- **PDF**: allegato alla release del tag su GitHub. In git restano i sorgenti (`guida/`).
- **Schemi della basetta e della scheda del carapace**: non erano mai stati progettati. Si progettano durante la guida e passano dall'utente.
- **Problemi trovati scrivendo**: vanno in `guida/problemi.md`, si portano all'utente e diventano la versione 2.1.7. Le immagini si fanno solo sulla 2.1.7.

## D-076 — Arresto 2 della guida di montaggio (2026-10-15)

L'utente ha letto il registro dei problemi (`guida/problemi.md`: 138 voci, 6 bloccanti, 37 domande) e il 15 ottobre 2026 ha deciso i bloccanti, gli acquisti e le risposte alle domande. Qui sono le decisioni, con il perché; le modifiche al CAD stanno nel piano della 2.1.7 (`docs/piano-v2.1.0.md`, "Versione 2.1.7"), il riepilogo voce per voce in `guida/decisioni-arresto2.md`. Ricerche: `docs/ricerca/bloccanti-arresto2.md`, `docs/ricerca/carica-usbc.md`. Le decisioni in blocco applicate prima (gruppi 1, 2, 3, 5, 9 di `decisioni-arresto2.md`) non sono ripetute.

**Bloccanti**
- **P-002, testata della scheda del carapace**: soluzione A, testata 2 × 8 a 90° con chiave sul bordo posteriore della scheda, comprata con X2.
  - Perché: sotto la scheda restano 11,7 mm contro i 16-18 della testata dritta con la spina; A è l'unica che risolve senza una giunzione volante sopra la SSC-32 e tiene la protezione dal verso intera (la spina girata porterebbe il 5 V sul pulsante della 2813). La spina esce verso l'ottagono, dove la guida la fa già sfilare. Spostare la scheda (la scelta del Q-02 "se c'è spazio") non è possibile: ai lati dell'ottagono restano 3,5 mm di larghezza, davanti c'è l'amplificatore.
  - Nel CAD la scheda si allunga. La testata va identificata sul catalogo con la chiave sul lato giusto; il codice trovato, da confermare sul disegno, è Würth 61201621721 (WR-BHD a 90°, 2 × 8, 2,54 mm), accoppiabile alla spina IDC 61201623021 già in X2 (S, C).
  - La guida resta sulle millefori. L'utente prevede di far stampare un PCB al posto delle millefori e lo disegneremo insieme in una versione successiva: la guida avrà una nota che l'alternativa arriverà, senza dettagli. Il PCB non è nella 2.1.7. L'utente ha già due connettori 1 × 8 maschio-femmina (Q-02), che non entrano nella scelta.
- **P-001, carica e fessure del tetto**: nella 2.1.7 si aprono le fessure del tetto verso la coda (si toglie il ponte da 2 mm), con un dentino sulla lingua centrale per la fascetta di F1 (D-055), così il pacco si sfila con le spine attaccate.
  - Perché: senza, il pacco non esce dal robot: non si carica nel sacchetto, non si sostituisce, un pacco gonfio resta nel corpo. È la regola dei produttori ("mai caricare nel modello", `carica-usbc.md`, sezione 2) e non costa niente.
  - **Niente caricatore integrato** (opzione 1 della ricerca, USB-C 15 W): 4-6 ore, bilanciamento passivo, nessun programma di conservazione, e invita a lasciar caricare da solo. La carica si fa con il **caricatore USB per 2S, lento, che l'utente ha già** (usato con la v1), collegato alle spine in coda (T-plug lato robot e presa di bilanciamento dietro il cicalino), a robot spento. Il pacco si sfila e si carica nel sacchetto quando si può; dentro il robot l'utente carica anche, sorvegliato, su una superficie che non brucia (le regole di sicurezza restano quelle della guida, 0.06 e 0.07).
  - Da provare con la spina vera prima di stampare la base (passo 11.03): che T-plug e JST-XH scorrano nelle tacche, e che il cavo del caricatore esca dalla porta di coda senza tirare il pacco.
- **P-003, teste M3 del vassoio sotto la basetta**: soluzione e di `bloccanti-arresto2.md`. Su S-19 l'utente aveva detto "risolvi in autonomia" (Q-03: "è uguale"): la scelta è dell'agente, il 15 ottobre l'utente l'ha confermata. Le quattro M3 × 6 e i quattro distanziali B18 escono: il vassoio si avvita su quattro colonne della base (inserto M2 in cima) con M2 × 5 svasate a filo. Perché: sotto la basetta tornano 3,3 mm come voleva D-053, lo schema della basetta non cambia, non si compra niente (B18 esce dal BOM) e il carico è di decine di grammi.
- **P-005, interasse delle file di pin dell'ESP32**: 25,4 mm (10 passi), stato S, come in `bloccanti-arresto2.md` (su S-02 l'utente aveva detto "risolvi in autonomia": scelta dell'agente, confermata il 15 ottobre): 24,7 non è un multiplo di 2,54 e torna come distanza fra le facce interne dei pin; Keyestudio MB0200, stesso modulo, dichiara 25,4. La condizione per saldare è la **prova a secco** (le strip infilate sui pin entrano nelle righe 2 e 12 della millefori), non il calibro: Q-18 resta aperta ma non blocca più.
- **P-004**: squadretta di prova approvata (Q-01), già nel BOM (domanda 4, voce D3): AliExpress da 0,42 € oppure diymore da 10,99 € (6 pezzi, misure dichiarate), alternative (risposta dell'utente del 16 ottobre).
- **Carica** (16 ottobre): il caricatore USB 2S dell'utente si attacca solo alla presa di bilanciamento JST-XH, non al T-plug: nessun adattatore; nella guida la carica passa dalla presa di bilanciamento.

**Acquisti approvati** (voci nel BOM)
- **Tester dei servo a manopola**, circa 5 €. Perché: senza alimentatore da banco (l'utente ha solo la bilancia, Q-26) il tester è l'unico modo di portare un giunto in posa a servo alimentato (6.16, 6.20, 9.08, 15); P-070.
- **Pulsanti da 12 mm, due** (B3b, già "1 + 1" nel BOM): l'utente non ne ha (Q-22). Il secondo serve per la prima accensione al banco, come pulsante provvisorio sui pin A e B della 2813 (opzione 2 di P-031: il pulsante è anche l'arresto d'emergenza, quindi non si lascia al pulsantino della 2813, che forse non si raggiunge).
- **Sacchetto per LiPo**, circa 10 €: l'utente non lo ha (Q-17); serve per caricare e conservare il pacco sfilato (P-041, P-001). Il pacco è da 38,5 Wh: molti sacchetti dichiarano 30 Wh, quindi se ne sceglie uno più grande (formato 23 × 30 cm, portata dichiarata sopra i 40 Wh).
- **Condensatore da 470 µF basso** (Ø6,3, alto al più 8 mm, 10 V) nell'ordine di X2 (P-073): con 6,3 × 11 il fondo arriva a 0,4 mm dai fori A-4 e B-4 e i fili Qwiic andrebbero saldati prima.
- **Testata 2 × 8 a 90° con chiave** (P-075, P-002), nell'ordine di X2 al posto di una testata dritta.
- Già approvati nelle risposte: la squadretta di prova (Q-01) e, per i provini 6 e 7, due FSR 400 Short e un tratto di striscia a 120 LED/m con buffer e resistenze (Q-05, X5 e X9).
- **Esce dal BOM**: B18, i distanziali (P-003); X3, il regolatore 3,3 V dei sensori (P-085): X3 non si compra finché la prova del 3,3 V non lo chiede. Negli schemi resta il ponticello J1 (filo 19) come ritorno possibile; mai J1 e X3 insieme.
- Consumabili generici (colla a caldo, biadesivo, nastro): non vanno nel BOM, sono cose che si hanno in casa (Q-25; P-008, P-072).

**Altre decisioni dalle risposte** (le non elencate sono nel registro)
- **Luci delle tibie** (P-077, Q-06): opzionali, con il diffusore **bianco**; se si cambia colore si modifica dopo. Condensatore sulle prese delle luci (P-074, Q-07): solo se serve, e con quelli che l'utente ha già (ceramici o elettrolitici di B7 e B8); prima si guarda in P4 se i pixel sfarfallano. Niente zaino per ora (P-027, Q-08): F2 resta da 2 A e il ramo logica non cambia; la predisposizione nel CAD resta com'è.
- **ToF posteriore avvitato** (P-008, Q-09): due fori per viti M2 sul piano del ToF; per l'altoparlante un ritegno dietro la guancia (linguetta o due costole); i microfoni con colla a caldo, fuori dal percorso del suono.
- **Materiali** (P-088, P-078, Q-10, Q-11): vassoio e lunette dei microfoni in PLA, colore libero (bianco e nero oggi nel CAD e nel BOM). `progetto-meccanico.md` ("in PETG") va corretto in PLA.
- **Prima prova della zampa con la batteria** (P-050, Q-14): niente alimentatore da banco. Il rail si accende solo nella sezione 12, con la batteria nel robot (opzione 1, già nella guida); chi vuole provare una zampa prima lo fa con la batteria appoggiata fuori e F1 da 15 A. Le sezioni 8 e 9 restano prove a freddo e tester.
- **Ristampa quando serve** (P-080, Q-15): nessuna scorta di pezzi stampati nel BOM; si tengono in casa PETG-CF, PLA e TPU.
- **Durate** (P-111, Q-16): non importano; il totale di ore della sezione 0.23 si toglie, restano le durate dei passi come stima.
- **Batteria, dati misurati** (Q-17; P-007, P-029): pacco lungo 139,65 mm (oltre i 137-139 dichiarati), cavo 110 mm, T-plug **femmina**, positivo sul lato verticale. Quindi (P-029) T-plug e F1 si uniscono con saldatura e termorestringente e F2 si ferma con una fascetta (opzione 1, consiglio del registro: la scelta è dell'agente, l'utente non si è espresso); il robot porta il maschio (B12) e la polarità si controlla con il multimetro prima di saldare. P-007: con 139,65 mm restano 7,75 mm fra pacco e rebbi; nella 2.1.7 i rebbi si allungano (`cor_sport_rebbio` da 17 a circa 22) per un solo strato di schiuma da 3 mm.
- **Inserti del kit** (Q-20; P-057, P-058): zigrinatura Ø4,2 e invito liscio Ø4,0 per l'M3, Ø3,2 e Ø3,0 per l'M2. Quindi il foro nel PETG-CF non può essere 4,2 (come l'inserto, senza interferenza): il provino di P-057 resta (M3 Ø3,9 / 4,0 / 4,1 più 4,2 di controllo, M2 Ø2,9 / 3,0 / 3,1 più 3,4) e il valore si sceglie sul pezzo. Divisione delle lunghezze M3 (× 5 e × 6) scritta una sola volta in 3.01, dopo il provino 1.03 con temperatura e tempo per PETG-CF e PLA (P-058). Temperatura e tempo di posa (Q-21) li decide l'agente, dal provino: l'utente ha detto "mi arrangio, risolvi in autonomia".
- **Servo con gommini e tubetti di ottone a parte** (Q-28, P-134): non si montano. Deciso dall'agente: l'utente ha risposto solo che gommini e tubetti sono a parte; il progetto li toglie già e il consiglio del registro era di restare alla bozza. Il servo si avvita rigido sulle alette nude, come da progetto. La guida non dice più "togli i gommini".
- **Attrezzi** (Q-26; P-070, P-071, P-117, P-050): l'utente ha solo la bilancia. La guida non richiede alimentatore da banco né termometro a infrarossi: per il collaudo (14) la temperatura si legge dalle NTC dei regolatori (X14) e al tatto con una regola fissa, le soglie di batteria si provano in simulazione, la corrente massima si limita con F1 da 15 A per le prime accensioni.
- **Cicalino** (P-066, Q-12): soglia a 3,3 V per cella (ultimo livello, indipendente dal firmware). Deciso dall'agente (l'utente: "risolvi in autonomia"), come da consiglio del registro: a 3,5 V sotto carico suonerebbe a ogni passo; le quote del BX100 si leggono sul pezzo.
- **Assetto di partenza** (P-046, Q-13): 100/45 a coppie per la prima camminata, poi il tripode lento. Deciso dall'agente (l'utente: "risolvi in autonomia"), come da consiglio del registro: è il punto di progetto, con il femore al 41 % dello stallo contro il 75 % di 70/70; `software.md` 6.7 va corretto.
- **Fili** (P-028, P-063, Q-24): l'utente non può misurare i diametri. Si progetta sulle specifiche stando larghi: 14 AWG siliconico 3,3 mm con margine (opzione 1 di P-028, consiglio del registro scelto dall'agente; si ripiega sui canali nel tetto solo se alla prima prova il filo non passa); gola del fermo della tibia da 4,5 invece di 4,0 per i fili da 28 e 30 AWG (P-063).
- **Prese dei piedi e delle luci** (P-012, Q-04 "non lo so"): si segue il registro: progettate con lo schema della striscia dei partitori, con la misura vera della spina JR; fino ad allora 7.10 le posa senza fissarle. Non nella 2.1.7.
- **Manutenzione** (P-101, Q-29): intervalli a eventi, numeri dall'usura vera dopo le prime ore. Deciso dall'agente: l'utente non ricorda gli intervalli della v1 (stringeva le viti con i dadi dall'altra parte), quindi si resta al consiglio del registro.
- **Kapton** (P-072): non nel BOM (consumabile generico): sotto il PTC e U2 va bene anche nastro in PVC; con le colonne di P-003 non serve più sulle teste delle viti.

**Aperte** (da chiedere quando arrivano i pezzi): Q-18 (scheda ESP32: sigla e misure; la prova a secco di P-005 sostituisce il calibro), Q-19 (foto della SSC-32), Q-23 (portafusibile), Q-27 (22 kΩ nel set B10), Q-30 … Q-37.

**Cosa cambia**: BOM (B18 e X3 tolti, due voci nuove (B20, C9), X2 con testata a 90° e 470 µF basso, totale circa 367,14 €); piano della 2.1.7 (modifiche 11, 12, 14-17); testi della guida per gommini, alimentatore da banco, termometro, tester, carica, zaino e diffusore. I testi che dipendono dal CAD 2.1.7 si fanno dopo la 2.1.7 (elenco nel piano, "Testi della guida dopo la 2.1.7").

## D-077 — Versione 2.1.7: correzioni dalla guida di montaggio (2026-10-16)

La 2.1.7 applica al CAD le scelte dell'arresto 2 della guida (D-076) e le decisioni in blocco approvate (P-009, P-014, P-015, P-016, P-019, P-057, P-062, P-065). Piano ed esiti modifica per modifica in `docs/piano-v2.1.0.md`, sezione 2.1.7; qui i risultati, le deviazioni dal piano con il perché e le verifiche. File Fusion "Hexapod v2.1.0", versione 16 ("2.1.7: correzioni dalla guida di montaggio (D-076, D-077)"); copia di ripristino della 2.1.6 in "Hexapod v2.1.0 - ripristino 2.1.6 (prima della 2.1.7)" (lineage `urn:adsk.wipprod:dm.lineage:o79LLOHlSzmXdBn2HiYE1A`).

**Cosa è stato fatto** (numeri del piano)
- **Corpo**:
  - 1, P-003: vassoio su quattro colonne della base con inserto M2 in cima e M2 × 5 svasate a filo; B18 (distanziali) esce. Testa a 3,4 mm sotto la basetta, come voleva D-053.
  - 3, P-009: ganci della catena LED anche a x ±75 e tre ganci nel passaggio davanti (x 75, y −24 / 0 / 24): tratti liberi della catena al più 40 mm (prima 76-105).
  - 8, P-019: asola del bus 7 × 4 fuori dalla basetta, su un'ala del vassoio.
  - 11, P-001: fessure del tetto aperte verso la coda (via il ponte da 2 mm), il pacco si sfila con T-plug e JST-XH attaccati.
  - 12, P-002: scheda del carapace con la testata Würth 61201621721 a 90° sul bordo di coda (x 29,5) e la spina 61201623021 orizzontale verso la coda; `Rif_Scheda_Carapace` con quattro corpi (millefori, testata, spina, chiave).
  - 15, P-008: ToF posteriore (Pololu #3415) con due fori pilota Ø1,7 per M2 × 5, perpendicolari al piano a 35°; due costole di ritegno dell'altoparlante a filo, che si infila ancora da dietro.
  - 16, P-007: rebbi dello sportello lunghi 22,5 sul pacco misurato (139,65) con 3 mm di schiuma.
- **Riferimenti**: 2, P-005: file di pin dell'ESP32 a 25,4 (S, con la prova a secco prima di saldare).
- **Zampa**:
  - 4, P-014: lamatura piana Ø6 sotto la testa della vite del guscio della tibia (la testa appoggia su tutta la corona).
  - 6, P-016: stretta del piedino come parametro (`pied_stretta`, 0) e tre STL del provino (0 / 0,2 / 0,4).
  - 9, P-062: sede delle luci della tibia lunga 50,5 (Z −32,95…−83,53) per la striscia da 50.
  - 14, P-063: gola del fermo dei fili della tibia da 4,5.
- **Attrezzi** (in libreria, nascosti): 7, P-057: provino degli inserti con otto fori e i diametri incisi; 5, P-015: `Dima_Calettamento` (α +20°, γ 100°, letta da `robot.yaml`); 10, P-065: bussola di battuta dei perni ed estrattore (asta e tubo d'appoggio).
- **Documenti** (13, 17): P-092, P-099, P-100; `progetto-meccanico.md`, `software.md`, README degli STL, `dimensioni-componenti.md` (batteria misurata, inserti del kit, Würth, Pololu #3415), `cablaggio.md`, `predisposizioni.md`, BOM (viteria e inserti: M3 × 6 48, M2 × 5 svasate 16, inserti M3 90 e M2 32; M2 × 4 per la scheda del carapace, due M2 × 5 per il ToF posteriore) e rimandi a questa versione in D-051, D-053, D-054, D-055, D-064, D-066, D-071 e D-074. Nella guida sono cambiati solo i dati che seguono il CAD (catalogo, totali, 8.07, 8.09, 8.11, 11.03, 15.10, 15.11, inventario); i testi restano a "Testi della guida dopo la 2.1.7" nel piano.
- **Correzioni della verifica geometrica** (sezione 18 del piano: 3 rilievi importanti e 8 minori, tutti corretti):
  - ala e asola del vassoio a x 25–35 / 26,5–33,5, fuori dalle prese dei piedi; la spina Qwiic va nella presa di coda dell'ADC (x 39);
  - scheda del carapace alzata di 0,6 (bugne da 2,9, `sch_bugna_h`), inserti in fori da 3,4, viti M2 × 4; chiave della spina 0,54 sopra le USB-C;
  - percorso del cavo piatto in due strisce (`cablaggio.md` 3.5bis);
  - rebbi fino a z −19,9 (`cor_sport_rebbio_luce` 8,5) per due cavi Ø4 uno sull'altro;
  - pacco da 139,65 con la schiuma da 2,25 nel modello;
  - lamatura Ø4,2 × 1 dei LED delle spie, fuori da F1;
  - colonne del vassoio Ø6,6;
  - carapace rifatto: il ricalcolo dopo lo spostamento di due istanze aveva tolto raccordi e smusso (lobo PD a spigolo vivo, +677 mm³) senza errori.

**Deviazioni dal piano** (e perché)
- **Dentino della fascetta di F1 fatto come due tacche** sui bordi della lingua (2,9 × 1 a x −76): un dente dentro la fessura fermerebbe i cavi che escono, uno sotto il tetto starebbe nei 2,6 mm sopra il pacco.
- **Linguette delle spie (X13) a |y| 14–20** invece di 16–22: fermavano i cavi del pacco che escono dalle fessure aperte (trovato dalla prova di sfilamento). Poi la lamatura dei LED (Ø4,2 × 1) per stare fuori dall'ingombro di F1.
- **Scheda del carapace larga 21,5 e non 23**: l'amplificatore comincia a x 51,85 (resta 0,85). Viti di coda a x 41,5 e anteriori a 48,0; `sch_sp` = 10,6.
- **Asola del bus a x 30** invece di 50: a x 45–55 l'ala copriva la fila delle prese dei piedi (le spine JR infilate dall'alto toccavano il vassoio); a x ≈ 70, la proposta della verifica, la spina Qwiic nella presa di testa dell'ADC tocca la colonna (75; 12,5). A x 30 il cavetto va nella presa di coda dell'ADC, a circa 9 mm invece di 31.
- **Cavo piatto in due strisce da 8** dopo il fermacavo: il nastro intero (20,3) non ha un percorso libero fra USB-C, testata e spine dei servo. Le pieghe sono S, da provare sul pezzo; la riserva è la soluzione B di P-002, da far scegliere all'utente.
- **Viti della scheda del carapace M2 × 4**: con la scheda alzata di 0,6 il foro dell'inserto è profondo 3,4 e la M2 × 5 arriverebbe sul fondo.
- **Rebbi da 22,5** (non 22: compressione della schiuma 0,75 invece di 0,25, dentro la tolleranza di stampa) e **cima a z −19,9** invece di −19,5, che lasciava i due cavi a contatto.
- **Colonne del vassoio Ø6,6** invece di 6,0: 1,6 di parete attorno all'inserto M2, come nelle bugne. I giochi scendono a 1,2 (IMU e piastrina) e 2,2 (ADC).
- **Bussola appoggiata al mozzo** e non al rialzo: una tasca Ø6,8 × 0,7 lascia libero il rialzo da 0,4, che fissa il gioco del cuscinetto e non va schiacciato dalla morsa. La sporgenza resta 1,40.
- **Foro dell'inserto del guscio della tibia più profondo di 1** (`tib_ins_guscio_l` 7,7) invece della M3 × 8: con la testa sul piano della lamatura la M3 × 10 andava 0,34 oltre il fondo; così vite, BOM e viteria non cambiano (dietro restano 5,85 mm di stinco).
- **Ganci del passaggio davanti a x 75**, cavo lungo Y, fra l'ampli e le paratie della testa: il piano lasciava la posizione al modello.
- **Dima del calettamento costruita con `solo`**: rifare le altre due dime ne avrebbe cancellato i componenti.

**Verifiche** (a fine versione, sul file salvato come versione 15 con le correzioni)
- **Assieme**: `controllo` 0 su 39 istanze del corpo, nessuna interferenza, coxe a 0, nessuno snapshot pendente, timeline senza problemi, schizzi vincolati.
- **Coxe**: libere a ±35° una alla volta; fra vicine libere a 30,5° e **a contatto a 31° su quattro coppie su quattro** (AS–MS e MD–PD 19,06 + 15,56 mm³, MS–PS e AD–MD 18,94 + 13,55). La riga "AD–MD libere anche a 31°" di D-071 non si ritrova (nota in D-071).
- **Carapace contro le zampe**: 3,96 mm sulle medie a +35°, 4,76 a −35°, 7,1 sulle altre, come nella 2.1.6. Sfilamento del carapace libero a 5, 10, 20 e 40 mm, anche con la spina IDC innestata; campo della camera libero (controllo a +8° tocca visiera e fascia).
- **Ciclo a tripode** libero a 100/45 (8 fasi) e a 70/70 (16 fasi).
- **Zampa**: 23 giunti (21 rigidi, 2 di rotazione), `misura` 0/90; `scansione` 81 pose libere su 81, 17 controlli su 20 toccano.
- **Verifiche nuove con corpi o scatole provvisorie** (`assieme.py`), ognuna con il suo caso di controllo:
  - `sfilamento_pacco`: pacco e cavi liberi; con la spina a destra libero da 0 a 165 mm, a sinistra tocca il ToF posteriore fra 10 e 20 mm (si esce dal lato destro, `cablaggio.md` 4);
  - `spine_prese`, `qwiic_adc`, `qwiic_asola`: spine JR e Qwiic libere; spina 7,2 × 4,2 tocca il vassoio;
  - `spina_staccata`: spina sfilata 2–8 mm libera con 0 / ±0,3 / ±0,5 di scarto; con la scheda all'altezza di prima tocca la USB-C;
  - `cavo_piatto`: libero; 0,4 più in alto tocca l'ottagono, 0,3 verso il centro il PCB dell'ESP32;
  - `cavi_rebbi`: liberi; 0,5 più in basso il secondo cavo tocca i rebbi (1,60 mm³);
  - `led_spie`: libero; LED senza lamatura tocca F1 (4,54 mm³);
  - bussola: sporgenza del perno 1,40; estrattore: spalla a 0,501 dal foro Ø7,2, punta a 0,199 dal cuscinetto;
  - `verifica_dime` (tre dime): urti solo con la lama B, che si toglie per montarle.
- **Sentinella sui volumi**: cambiano solo base, vassoio, carapace, sportello, tibia, guscio della tibia, `Rif_Scheda_Carapace`, `Rif_Batteria_2S5200` e i cinque attrezzi nuovi, ognuno con il volume del calcolo a mano; il resto è invariato.
- **A valle**: STL (41 file più tre piedini), mesh, `cad.json` (74 parti), pose, hash e generatori; `guida.costruisci controlla` verde (resta l'avviso noto della vite svasata del vassoio, un artefatto della convenzione della guida); ruff, pytest (72), ctest (4 su 4), `npm test` (3 su 3).
- La seconda verifica geometrica, sulle correzioni, non ha trovato rilievi bloccanti né importanti; i 3 minori sono qui sotto.

**Massa**: attesa **3046,2 g** (2.1.6: 3045,0; corpo 1070,6 g, modellato 2686,2 + non modellato 360,0); femore a 5,85 kgf·cm, sempre al 53 % dello stallo a 100/45. Aggiornati `calc/statica_tripode.py` e `robot.yaml`, la regressione passa.

**P-015, calettamento del ginocchio** (scelta dell'utente del 16 ottobre 2026): il calettamento resta a **γ 100**. Con il dente più vicino resta un errore fino a ±7,2°, e nel caso peggiore il ginocchio arriva a 172,8 invece di 177. Dopo la taratura a due punti la guardia prende `gamma_max = min(177, γ di calettamento misurato + 80)` (`software.md` 2.5, nota per il firmware S2; commento su `guardia.gamma_max` in `robot.yaml`). Il ginocchio perde al più 4,2° di distensione; le andature dei quattro assetti arrivano al più a γ 103,3 in appoggio. La proposta di portare il calettamento a 104,5 non è stata scelta: avrebbe cambiato la dima, la tabella di `software.md`, i generatori e la guida.

**Aperti per la 2.1.8** (minori della seconda verifica; l'utente li porta alla versione successiva, registro `guida/problemi.md` P-139…P-141):
- **Reofori dei LED delle spie (X13) a 0,6 mm da F1**: con la lamatura il corpo del LED è fuori dall'ingombro di F1 (40 × 22 × 15, S), i reofori no. Proposta: spostare F1, la coppia di T-plug e le costole di +2,5 verso la testa (oggi ci sono 3,0 mm dal 2813), oppure prima leggere il portafusibile Neuftech vero. Il ripiego di `cablaggio.md` 5, punto 8 ("si piegano lungo la linguetta") non è fattibile.
- **Cavo piatto in due strisce a 0,25 mm dal PCB dell'ESP32 e a 0,3 dalla battuta dell'ottagono**: proposta di far scendere le strisce 1,0 mm più verso l'esterno; nei testi della guida vanno la divisione in due strisce e la crimpatura.
- **P-012, prese dei piedi**: quando si disegnano le prese, l'ingombro delle spine JR (circa 7,6 × 2,5) deve restare a y ≥ 17,6.

## D-078 — Circuiti stampati al posto delle millefori: piano della prima serie (2026-10-18)

L'utente ha scelto il 18 ottobre 2026, sullo studio di `docs/ricerca/pcb/`, e ha approvato il piano `docs/piano-pcb.md` (verificato da tre agenti, 51 rilievi corretti, sezione 9 del piano).

**Scelte dell'utente**
- **Architettura "una per una"**: tre PCB al posto delle tre millefori, con le stesse reti: basetta dell'ESP32 (PCB-B), scheda del carapace (PCB-C), partitori (PCB-P). Perché: è la strada più semplice, verificabile a mano col multimetro, e il CAD cambia solo per dare un posto ai partitori. La scheda madre consigliata dallo studio chiedeva colonne nuove e due varianti della base.
- **Montaggio a mano**, schede nude; **JLCPCB**, un solo ordine; **banco S1 sulla prima serie** (r1): le millefori non si saldano mai.
- **DU-1, KAmod tolto**: la TX verso la SSC-32 esce dal terzo canale del buffer SN74AHCT125 (già sulla basetta), con 330 Ω in serie e 10 kΩ di pull-up verso il 3,3 V dell'ESP32; la RX passa da un partitore 20 kΩ / 33 kΩ (in F0, perché il set B10 non ha il 15 kΩ), montato sempre (ripiego da 1 kΩ solo dopo aver misurato la TX a non più di 3,6 V). Un modulo e un'impronta incerta (S-04) in meno.
- **DU-2, niente presa Qwiic** sulla scheda del carapace: quattro piazzole per il cavo tagliato verso il TCA9534. Dalla 2.1.7 la scheda si raggiunge solo a carapace tolto, e sulla scheda più piena un componente in più non vale.
- **DU-3, ERC e DRC di KiCad nella CI**, con KiCad dal PPA e il controllo della versione.
- **Componenti** (scelta lasciata all'agente): basetta e carapace solo a reoforo, come sulla millefori; SMD 0805 solo sulla PCB-P (8 resistenze e 8 condensatori), dove lo spazio li impone.

**Scelte dell'agente scritte nel piano** (sezione 2): PTC MF-R075 con impronta anche per MF-R090 e tetto dei LED sotto 600 mA fino a P4; pull-up del bus da 4,7 kΩ e ponticello I2C del modulo SparkFun X20 da tagliare; R9 sulla basetta; masse su un piano unico; fori Ø2,4.

**Dati letti** (V): il modulo SparkFun Qwiic GPIO X20 esce di fabbrica a **0x27** con i pull-up da 4,7 kΩ inseriti (guida SparkFun); il progetto diceva 0x20. Proposta da decidere con S1: 0x27 nel firmware.

**Acquisti** (18 ottobre): approvati 10 kΩ 0805 (PCB1), X1 e X6 (scelta lasciata all'agente); PTC di X9 passato a MF-R090 (a 40 °C tiene 0,73 A contro 0,61); ordine DigiKey in sospeso finché non supera i 75 €. Non si comprano: 100 nF a reoforo e pull-up (kit dell'utente: ceramici e resistenze Elegoo, 5,1 kΩ o 10 kΩ al posto del 4,7 kΩ che il set B10 non ha); 330 Ω e 1 kΩ dal set B10; partitori a 20 kΩ / 33 kΩ dal set. BOM 2.4: escono C1 e i partitori a reoforo di X5 e X14, circa 364,63 €.

**Scheda ESP32** (18 ottobre, dopo le foto): l'utente ha 2 UICPAL RE1.3 e 2 schede "corte" da 57 mm (`dimensioni-componenti.md`). Resta la **RE1.3**, confermata dall'utente: oltre al CAD già fatto, sotto ha un tratto di circa 23 mm con soli componenti bassi dove sta il regolatore 5 V, ha la presa IPEX per un'antenna esterna (il corpo in PETG-CF può attenuare il Wi-Fi), lo schema pubblicato e due fori. Le schede corte restano per il banco. Nel CAD la microSD della RE1.3 è dal lato sbagliato: voce 4 della 2.1.8.

**Cosa resta**: DU-5, il posto della PCB-P (tasca accanto all'IMU o sotto le prese dei piedi), si decide nella 2.1.8 dopo le prove nel CAD. Fasi, arresti e rischi nel piano.

## D-079 — PCB, arresto R1: schemi di basetta e carapace approvati, con le correzioni della verifica (2026-10-18)

L'utente ha approvato gli schemi r1 della basetta (PCB-B) e della scheda del carapace (PCB-C), generati da script in `pcb/basetta` e `pcb/carapace` (F3 di `docs/piano-pcb.md`), e ha chiesto la verifica con agenti. Due revisori indipendenti (reti e pin; sicurezza elettrica), circa 0,38 milioni di token, 10 rilievi: nessuno bloccante. Li ho ricontrollati sulle fonti e corretti così:
- **TCA9534 tolto dalla scheda del carapace**: TI lo vende solo in SOIC largo (DW, 10,3 × 10,3) e TSSOP (PW, passo 0,65) (ti.com, letto il 18 ottobre), non nel SOIC stretto dell'impronta; un DW non sta nei 7,4 × 19 mm utili e il TSSOP va contro "niente chip a passo fine". L'espansore resta il modulo X20; la piazzola XSHUT del ToF posteriore esce (il filo va diretto a X20, `schemi.md` 2.4).
- **R16 da 10 kΩ in serie fra GPIO41 e la piazzola OFF della 2813**, dal set B10: un corto a 8,4 V sul filo o sulla 2813 non arriva al GPIO.
- **Regole del DRC** per le reti che mancavano: 5V e 3V3 del carapace, 3V3_ESP e 3V3_X3, 1 mm attorno a EN di U2 (come il VBAT) e al pulsante (BTN_A, BTN_B, S-10), con l'eccezione dentro J2.
- **Testata J2 con fori da 1,1** e piazzole da 1,8, come il disegno Würth; pad n = polo n del cavo, poli dispari sulla fila lato chiave (S-26). La riga di F0 che diceva il contrario è segnata: si prova sulla dima con la spina (F5).
- **CS1 e CS2 su un'impronta a due passi** (2,5 e 5,0): il passo dei 100 nF del kit dell'utente non è noto.
- **Tetto dei LED**: il ramo dopo PTC1 porta anche l'amplificatore e i pixel spenti; fino alla misura di P4 il firmware tiene i LED sotto 450 mA con l'audio acceso (S-06), non sotto 600 mA. Corretti anche il ripiego della RX (al posto della 20 kΩ) e le righe del piano.

**Lezione**: se una sola regola del `.kicad_dru` è scritta male, KiCad ignora tutto il file senza avvisi (DRC a zero anche con piste strette, provato). La copre il test che restringe il 5V_REG della scheda di prova con la copia vera delle regole.

**Cosa resta**: polo 1 di J2 sul pezzo (F5); prove sui pezzi di dima; regole nuove provate con i loro casi di controllo quando ci sono i PCB (F4, F6).

## D-080 — Scheda dei partitori sotto le prese dei piedi (DU-5 = P2) (2026-10-18)

L'utente ha lasciato la scelta all'agente, con un criterio: "l'interno il più ordinato possibile e facile per il montaggio e la manutenzione". Le due varianti del piano del PCB (4.3) sono state provate nel CAD come scatole provvisorie, con i casi di controllo (`assieme.py` → `partitori_varianti`): libere tutte e due.

**Scelta: P2.** La scheda dei partitori (PCB-P) sta sotto le prese dei piedi, a x 44,2…72 e y 19…26,5, su due bugne da 4 con inserti M2 come IMU e ADC. Porta il pettine 6 × 3 delle spine dei piedi (centro a x 56,6, `cor_par_pet_x`): le spine JR (8 × 3 × 14, misurate dall'utente) si innestano dall'alto a carapace tolto. Perché:
- un pezzo solo chiude le prese dei piedi (P-012, oggi una fila sciolta in una scanalatura), il vincolo P-141 (spine a y ≥ 18,75) e il posto dei partitori (S-28, S-29);
- i fili dei piedi non attraversano il corpo: dalla presa al partitore c'è la scheda, e dal partitore all'ADC, che sta accanto, pochi centimetri;
- per smontare una zampa si sfila la spina dall'alto, come prima.

**Nel CAD (2.1.8, blocco C)**: `Rif_Partitori` (scheda 27,8 × 7,5 con pettine e pin); bugne `bugna_par_a/b` sul tetto; tolta la sede delle prese dei piedi (le code dei pin l'avrebbero toccata); le prese delle luci restano dov'erano, su fili. Saldature della prima colonna a 0,45 dalla bugna di coda; caso di controllo 0,5 più in là tocca. Nessuna interferenza nell'assieme.

**Cosa resta**: la NTC sinistra non ha una spina (piazzola o spina nuova, da decidere con lo schema della PCB-P); partitori 0805 anche sul lato sotto (4 mm d'aria fino al tetto); la strada B con la millefori tagliata sulla stessa sagoma.
