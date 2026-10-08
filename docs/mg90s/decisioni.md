# Registro delle decisioni

Ogni decisione ha una data, il perché e lo stato (**presa** / **proposta, in attesa dell'utente** / **superata**).
Le scelte fissate dall'utente stanno in `CLAUDE.md` e non si ripetono qui.

## D-001 — Il progetto Fusion è "Hexabot v2" (2026-10-08, presa)

L'utente parla di progetto `hexapod-v2`, ma nel hub non esiste: i candidati sono "Hexabot v1" e "Hexabot v2". "Hexabot v2" contiene l'unico file servo (`Tower Pro MG90S Micro servo`), quindi è quello. Segnalato all'utente.

## D-002 — Il servo è il Tower Pro MG90S (2026-10-08, presa)

Identificato dal nome del file e dalle quote del modello (cassa 22,6 × 12,15 × 22,55 mm, 32,2 mm sulle orecchie), coerenti con la tabella ufficiale Tower Pro (22,8 × 12,4, 32,5 sulle alette). Resta da sapere se i 18 pezzi reali sono originali o cloni: cambia coppia, millerighe e affidabilità.

## D-003 — La scheda di controllo è la UICPAL "ESP32-S3-CAM N16R8 RE1.3" (2026-10-08, presa)

Letta dalle immagini dell'inserzione AliExpress indicata dall'utente: serigrafia, pinout e disegno quotato sono univoci, quindi non serve chiedere una foto. Pinout identico alla Freenove ESP32-S3-WROOM CAM.

## D-004 — Coppia di stallo di progetto: 1,8 kgf·cm a 4,8 V, 2,0 kgf·cm a 6,0 V (2026-10-08, presa)

Tower Pro dichiara 2,2 kgf·cm a **6,6 V**, non a 6 V; il "2,2 a 6 V" viene da un PDF non ufficiale. Il datasheet di un clone (Sky Star) dà 2,0 a 6,0 V. Si progetta sul valore prudente. Limite del 50 %: 1,0 kgf·cm con rail a 6,0 V.

## D-005 — Corrente di stallo di progetto: 1,0 A per servo a 6 V (2026-10-08, presa)

Unico dato da datasheet: 860 mA ±10 % a 6,0 V e 750 mA ±10 % a 4,8 V (clone Sky Star). Arrotondato a 1,0 A: 18 A nel caso peggiore con 18 servo in stallo. Tower Pro non pubblica la corrente.

## D-006 — Architettura Fusion: giunti e istanze (2026-10-08, proposta tecnica, da confermare in fase 4)

Via API i giunti interni a un sotto-assieme istanziato più volte hanno un valore unico che muove solo la prima istanza (prova documentata in `CLAUDE.md`). La zampa resta un unico componente istanziato sei volte, come chiesto; per le pose indipendenti della verifica d'andatura si useranno trasformate per-istanza calcolate dagli assi dei giunti e validate contro il risolutore sulla prima istanza, oppure giunti al livello radice. Da decidere quando si costruisce l'assieme.

## D-007 — Rail servo a 6,0 V con due regolatori Pololu, uno per lato della SSC-32 (2026-10-08, presa: confermata dall'utente)

La 2S diretta è esclusa: Tower Pro dichiara 4,8 V di esercizio e una prova di terzi mostra il chip di controllo di un MG90S forato a 8,4 V. Si regola a 6,0 V perché a 5,0 V la coppia al ginocchio supera il 50 % (vedi `dimensionamento.md`). Lo stallo dei 18 servo vale 17 A: un solo Pololu D42V110F6 ne dà circa 14, quindi se ne usano due, ciascuno su un lato della SSC-32 con 9 servo (8,5 A di stallo). Così anche ogni lato della scheda resta sotto i 15 A di picco dichiarati da Lynxmotion. Alternativa: due Hobbywing UBEC 10A (metà costo, +42 g, caduta minima non dichiarata, nessun pin di spegnimento). Scelta finale all'utente.

## D-008 — Logica separata: regolatore 5 V dedicato all'ESP32, VL della SSC-32 dalla batteria (2026-10-08, presa)

L'ESP32 ha un suo buck (Pololu D24V22F5), così i buchi di tensione dei servo non lo resettano. La logica della SSC-32 ha il proprio regolatore a bordo e accetta 6–12 V (venditore del clone) o 5,3–16 V (SSC-32U): la batteria commutata ci rientra. Ponticelli VL=VS e VS1=VS2 tolti. Massa comune a stella vicino ai regolatori.

## D-009 — Interruttore generale a MOSFET Pololu #2815 (2026-10-08, **superata da D-019**)

Piccolo, 2,6 g, protegge dall'inversione di polarità, levetta raggiungibile da una feritoia. Limite: 6 A continui a 55 °C e 16 A a 150 °C. Copre la marcia (circa 4,5 A) e i picchi (11 A); i 17 A dello stallo totale li regge solo per decine di secondi. Va montato staccato dalle pareti, in PETG. Se l'utente preferisce un componente dichiarato per 20 A continui: bilanciere R13-112, foro da 20,2 mm.

## D-010 — Fusibile a lama MINI da 20 A subito dopo la batteria (2026-10-08, presa)

Protegge cavi e connettori dal cortocircuito, non i servo dallo stallo: a 17 A lavora all'86 % e non scatta. Un valore più basso scatterebbe sui picchi legittimi.

## D-011 — Sottotensione su tre livelli indipendenti (2026-10-08, presa)

Cicalino sulla presa di bilanciamento (funziona anche se il firmware è bloccato); partitore 100 kΩ / 47 kΩ su GPIO1 per avviso e arresto ordinato; spegnimento del rail servo dai pin ENA dei regolatori Pololu. Soglie: 3,5 V per cella allarme, 3,3 V arresto. Nota: i pin ENA sono attivi di default, quindi lo spegnimento non è a prova di blocco dell'ESP32; il cicalino sì.

## D-012 — Seriale ESP32 ↔ SSC-32: UART1, TX su GPIO21, RX su GPIO47, 115200 baud, traslatore di livello (2026-10-08, presa)

I GPIO dell'ESP32-S3 non tollerano 5 V (massimo 3,6 V) e l'uscita a 3,3 V non garantisce la soglia alta di un ATmega a 5 V (2,64 V garantiti contro 3,0 V richiesti): serve un traslatore su entrambe le linee. GPIO21 non ha impulsi spuri all'accensione ma resta flottante al reset: le resistenze di pull-up del traslatore lo tengono a riposo. A 115200 baud un comando per 18 servo dura circa 12 ms. Il baud reale della scheda va letto sui LED.

## D-013 — Camera senza prolunghe (2026-10-08, presa, dettaglio dopo la risposta dell'utente)

Le prove pubbliche dicono che un DVP a 24 pin regge 75–90 mm e non 100 mm o più: niente adattatori di prolunga. Con il modulo standard (21 mm, 8 mm di flat libero) la scheda sta in verticale subito dietro il frontale, con la camera appoggiata sulla scheda che guarda avanti e le USB-C verso un fianco. Con un modulo a flat lungo (75 mm) la scheda si può mettere altrove.

## D-014 — Giunti: culla che stringe il servo, cuscinetto F683ZZ coassiale, squadretta di serie in sede stampata (2026-10-08, presa, squadretta con riserva)

Nessun progetto di riferimento sfrutta un rilievo del servo: il perno opposto all'albero sta sempre nel pezzo che avvolge il servo. Cuscinetto F683ZZ (3 × 7 × 3, flangiato: la flangia fa da battuta) su spina da 3 mm h8, che dà al massimo 0,014 mm di gioco; una vite M3 ne darebbe fino a 0,126. Sotto le alette non c'è parete per un inserto M2 (0,6 mm contro 1,3 richiesti): lì vite passante e dado. Squadretta: una metallica verificata per l'MG90S non esiste (Tower Pro ne fa solo per Futaba, Hitec e JR; le fonti non concordano su 20 o 21 denti). Base di progetto: squadretta di plastica di serie chiusa in una sede e avvitata. La metallica "21T" resta una prova da fare su una confezione dopo aver contato i denti.

## D-015 — Geometria della zampa: coxa 36, femore 34, tibia 50 mm, assetto alto (2026-10-08, presa)

Vedi `dimensionamento.md`. Massa di progetto 1,20 kg, asse del femore a 75 mm da terra: 45 % dello stallo al ginocchio. Il femore non si allunga (a 38 mm si perde il margine). Con questa massa il 50 % si rispetta solo tenendo piede e ginocchio vicini alla verticale dell'anca. Segmenti corti riducono anche il gioco in punta.

## D-016 — Materiali: PETG-CF per le parti strutturali, PLA o PETG per le cover (2026-10-08, presa, da confermare con l'ugello dell'utente)

Dati dello stesso laboratorio: PLA-CF 3700 MPa a flessione ma 26 MPa tra gli strati e cedimento a 54–55 °C; PETG-CF 2890 MPa, 38 MPa tra gli strati, 68–74 °C. Culle dei servo e corpo vicino ai regolatori scaldano: PETG-CF. Aperto: ugello di serie temprato (Flashforge) o inox (Tom's Hardware), e 0,4 mm contro lo 0,6–0,8 consigliato dalla guida filamenti per i caricati carbonio.

## D-017 — La batteria resta la OVONIC 5200 mAh (2026-10-08, **superata da D-027**)

È un quarto della massa e nessun esapode documentato con MG90S ne porta una simile, ma il calcolo mostra che il vincolo si rispetta. Alternativa documentata se in prova il margine non basta: 2S 2200 mAh da 126 g.

## D-018 — Sedi dei servo sulle quote ufficiali Tower Pro; ginocchio predisposto per il Savox SH-0255MG+ (2026-10-08, presa)

Lo STEP è 0,2–0,35 mm più piccolo delle quote ufficiali: le sedi si disegnano su 22,8 × 12,4 mm più il gioco e si stringono con le viti. Al ginocchio (il giunto più caricato) asole delle alette da 27,5 a 28,4 mm e spessore removibile di 2,4 mm, così il Savox da 3,9 kgf·cm resta montabile senza ridisegnare.

## D-019 — Nessun interruttore nel percorso dei servo; rail acceso dai pin di abilitazione, spento di default (2026-10-08, presa; sostituisce D-009)

Rilievo bloccante della revisione elettrica: l'interruttore #2815 era l'unico anello sotto la corrente di stallo (18 A contro 16 A a 150 °C) e il fusibile da 20 A non lo proteggeva; la frase "regge per decine di secondi" non aveva fonte. Soluzione: i due regolatori Pololu restano collegati alla batteria dopo il fusibile e si accendono dal pin ENA. I due ENA sono uniti e tirati a massa da 47 kΩ, quindi il rail è spento all'accensione, in reset, in bootloader e a ESP32 bloccata; il GPIO42 li accende attraverso un diodo. La soglia di ENA non è pubblicata: i valori vanno provati al banco. L'interruttore generale passa sul ramo logica (meno di 1 A). Vale solo con i Pololu: con gli Hobbywing servirebbe un sezionatore da almeno 30 A.

## D-020 — Interruttore a pulsante con pin OFF sul ramo logica, e fusibile dedicato da 2 A (2026-10-08, presa)

Rilievo: dopo l'arresto dei servo nulla staccava la logica (circa 0,2 A), e il pacco sarebbe sceso sotto 3,0 V per cella in circa un'ora. Il Pololu #2813 ha un pin OFF: a 3,2 V per cella il firmware spegne il rail e poi sé stesso (GPIO41). Il ramo logica in 22 AWG ha un suo fusibile da 2 A, perché quello da 20 A non lo proteggerebbe. Il cicalino sulla presa di bilanciamento assorbe sempre: a fine uso si staccano T-plug e presa di bilanciamento.

## D-021 — Portata dei lati della SSC-32: da confermare sul clone prima del CAD (2026-10-08, aperta)

9 A di stallo per lato contro 3–5 A continui raccomandati da Lynxmotion; per il clone non c'è alcun dato. Nel tripode i due lati si dividono il carico 2/3 e 1/3 a turno (picco 7,2 A sul lato carico). Si decide dopo foto e misure delle piste: lasciare così con limite di tempo dello sforzo nel firmware, aggiungere un fusibile da 10 A per lato, oppure portare +V e massa dei servo su una barra esterna lasciando alla scheda solo i segnali. L'ultima opzione cambia il cablaggio nel corpo.

## D-022 — Il 5 V entra nell'ESP32 da una porta USB-C con un diodo in serie (2026-10-08, **ridotta ad alternativa da D-028**)

Secondo lo schema del venditore il pin 5V è a valle di un diodo e non alimenta il regolatore della scheda; due segnalazioni su cloni simili lo confermano. Percorso di base: spinotto USB-C nella porta "OTG", con un diodo Schottky che impedisce al 5 V del PC di arrivare all'uscita del regolatore. Il margine è stretto (circa 4,65 V contro 4,4–4,6 V richiesti dal regolatore della scheda): si prova con il Wi-Fi in trasmissione. Se la prova sul pin 5V riesce, si usa quello.

## D-023 — Elettronica sfusa su una basetta con zoccolo per l'ESP32 (2026-10-08, presa)

La scheda ESP32 non ha fori di fissaggio e i ponticelli Dupont su un robot che cammina si sfilano. Una basetta millefori con due strip femmina fa da zoccolo e da supporto: sopra si saldano traslatore, partitore, rete di abilitazione e condensatore dell'ADC, e la basetta ha i fori per fissarla.

## D-024 — Montaggio del giunto: cuscinetto nella culla, perno nella forcella infilato per ultimo (2026-10-08, presa, da confermare con lo schizzo)

Una forcella a U in un pezzo con il perno già piantato non si monta, e un perno piantato in foro cieco non si estrae. Quindi: cuscinetto F683ZZ nel fondo della culla con la flangia a battuta; perno nel braccio della forcella, infilato dall'esterno e bloccato da una vite M2; squadretta in una tasca aperta verso l'esterno con coperchietto. Perni: le spine comuni sono m6 e nel cuscinetto entrano forzate; servono h8 con tolleranza dichiarata o asta rettificata h6, da misurare col micrometro. Fonte d'acquisto ancora da trovare.

## D-025 — Massa di progetto 1,20 kg (2026-10-08, presa)

La revisione ha trovato la somma del bilancio sbagliata (1081 e non 1070 g) e voci mancanti. Bilancio rifatto: 1167 g. Si progetta a 1,20 kg con l'asse del femore a 75 mm.

## D-026 — Ugello da 0,6 mm per i caricati carbonio, finestra non caricata sull'antenna (2026-10-08, ugello **superato da D-029**; la finestra sull'antenna resta)

La guida filamenti Flashforge chiede 0,6–0,8 mm per PLA-CF e PETG-CF; la macchina esce con 0,4. La scelta fissa gli spessori minimi delle pareti, quindi va fatta prima del CAD. Il carbonio scherma il Wi-Fi: sopra l'antenna della scheda va una finestra in materiale non caricato con 15 mm liberi.

## D-027 — Batteria: OVONIC 2S 2200 mAh 50C con T-plug, in coppia (2026-10-08, presa su delega dell'utente e **confermata**)

L'utente aveva scelto la 5200 mAh perché l'aveva in casa dalla v1 e ha chiesto di dimensionarla. Il vincolo che stringe è la coppia, non l'autonomia: 140 g in meno portano il ginocchio dal 51 % al 44 % dello stallo a parità di assetto. Autonomia stimata 25–53 minuti per pacco; la batteria si sfila senza attrezzi e si vende in coppia. Stesso marchio e stessi connettori (T-plug, JST-XH) della batteria esistente, quindi caricabatterie e cavi non cambiano. Una taglia intermedia da 3000–3300 mAh riporterebbe la coppia al 47 %. Dati dalla pagina del produttore: 105 × 33 × 14 mm (±5 / ±2 / ±2), 120 g ± 20, 50C. Vano disegnato su 112 × 37 × 18 mm con schiuma. Dettagli in `dimensionamento.md`.

## D-028 — ESP32 alimentata dal pin 5V, con lo spinotto USB-C come alternativa già prevista (2026-10-08, presa: indicazione dell'utente)

L'utente ritiene che la scheda si accenda dal pin 5V e chiede un'alternativa pronta. Percorso di base: 5 V del regolatore sul pin 5V attraverso la basetta. Alternativa: spinotto USB-C a 90° nella porta "OTG" con diodo Schottky in serie (D-022). Il corpo lascia lo spazio per lo spinotto e la basetta porta entrambe le piazzole, così il cambio non richiede di ristampare nulla.

## D-029 — Stampante Creator 5 Pro, ugelli temprati da 0,4 mm anche per i caricati (2026-10-08, presa: dato dell'utente)

Niente ugello da 0,6 mm. Spessori del CAD in multipli di 0,4 mm; pareti strutturali da almeno 1,6 mm. La Pro è chiusa e scalda la camera fino a 65 °C.

## D-030 — SSC-32 e camera identificate dai link d'acquisto dell'utente (2026-10-08, presa)

SSC-32: è il clone "SSC32-V2.5" con micro-USB e XBee (AliExpress 1005001888185034). Il disegno quotato del venditore dà PCB 72 × 55 mm e fori a 65,5 × 48,5 mm, coerente con la misura fatta dal verificatore sulle foto (65,2 × 48,3). Camera: UICPAL "OV3660-75MM" con flat da 75 mm (AliExpress 1005007456301694): esiste, quindi la scheda ESP32 non deve più stare addosso al frontale. Variante dell'utente: lente da 120° "GOOD", a testa compatta (circa 8,5 × 8,5 × 6 mm), non quella a cupola da 12,4 mm. Il campo visivo libero dalle zampe anteriori si verifica su 120°.

## D-031 — Componenti comprati nel design: STEP dove esiste, altrimenti ingombro generato da script (2026-10-08, presa)

Servo inserito come riferimento esterno al file dell'utente, così l'originale non si tocca e le 18 copie saranno istanze dello stesso componente. Regolatori Pololu importati dallo STEP del produttore. Per SSC-32, ESP32, camera, batteria, cuscinetto, perno e parti minori non esiste un modello: l'ingombro è un corpo in una BaseFeature creato da `cad/script/rif_componenti.py`, che legge le quote dai parametri utente. Niente schizzi per le parti comprate: gli schizzi vincolati restano per le parti progettate. Le quote delle sedi nelle parti progettate dipendono dai parametri, non dalla geometria degli ingombri.

## D-032 — Supporti ammessi dove servono (2026-10-08, indicazione dell'utente)

La Creator 5 Pro è un toolchanger a 4 testine e stampa i supporti con l'interfaccia in un altro materiale, quindi si staccano puliti. Regola: ogni parte ha una faccia d'appoggio naturale e si evita ogni supporto inutile, ma un sottosquadro è accettato quando migliora rigidezza, estetica o semplicità (per esempio raccordi sulle facce inferiori, sedi su due lati opposti, forme chiuse).

## D-033 — Architettura della zampa (2026-10-08, presa; dettagli in `progetto-meccanico.md`)

Servo della coxa nel corpo con la coda verso l'esterno (cavo verso l'interno); coxa a C in un pezzo, infilata di lato; servo del femore con lato lungo verticale e coda in alto; femore in due pezzi avvitati, perché una forcella in un pezzo non si infila sull'albero; tibia con la culla del servo e la coda verso il piede. Finestra del cavo sotto la bugna dell'aletta, larga 9 mm per far passare la spina. Verificata pilotando i giunti veri: libera per femore da −75° a +25° e ginocchio da 62° a 165°.

## D-034 — Porta USB: nessuna prolunga, sportello di servizio sul dorso (2026-10-08, presa su delega dell'utente; sostituisce la proposta della prolunga)

L'utente ha delegato la scelta chiedendo di evitare un acquisto in più, a meno di problemi funzionali o estetici. Con la camera frontale e il flat da 75 mm la scheda ESP32 sta con l'antenna in avanti e le due USB-C a metà corpo, rivolte indietro: questo non si può cambiare. Alternative valutate:

- **Prolunga USB-C da pannello** (circa 8 €, 10 g): porta pulita sul retro, ma è un acquisto, e in coda lo spinotto, la presa da pannello e 15–20 cm di cavo da ripiegare contendono lo spazio a connettore della batteria, cicalino e interruttore.
- **USB sul frontale sotto la camera** (scheda girata): nessun acquisto, ma l'antenna finisce a metà corpo sopra la SSC-32; l'alimentazione di riserva dalla USB-C (D-028) resterebbe con lo spinotto sporgente dal muso; il cavo di prova uscirebbe davanti alle zampe.
- **Sportello di servizio sul dorso** (scelta): un'apertura nel guscio sopra le USB, chiusa da uno sportellino a incastro. Nessun acquisto. Dà accesso anche ai pulsanti BOOT e RST, che una porta da pannello lascerebbe sepolti, e alla seriale della SSC-32. Il cavo USB esce dall'alto, al centro: è la posizione che intralcia meno le zampe in una prova col cavo attaccato.

Costo accettato: per collegare il cavo si toglie lo sportellino, e dietro le porte servono circa 40 mm liberi per lo spinotto (sopra la striscia centrale della SSC-32). La voce C9 del BOM è stata tolta.

## D-035 — Disposizione del corpo: prima proposta a ottagono (2026-10-08, **superata da D-036**)

Scafo a ottagono allungato (±68 × ±48 mm) con batteria sotto un ponte, SSC-32 sopra, ESP32 sopra la SSC-32, regolatori in piedi nei rigonfiamenti laterali. Rifacendo i conti degli ingombri non regge: i regolatori ai lati chiudono le finestre dei cavi delle gondole medie e lasciano 3–4 mm ai cavi che salgono agli header; le alette dei servo delle coxe medie arrivano a 0,7 mm dentro la parete.

## D-036 — Disposizione del corpo: base a vasca con muso e coda, guscio non strutturale (2026-10-08, presa; modellata)

- **Pianta**: tratto centrale ±30 × ±46 mm, fianchi obliqui fino a (±68, ±25), muso e coda larghi 50 mm fino a x = ±82. Gli assi delle coxe non cambiano: (±72, ±40) a 40° e (0, ±58). Muso e coda stanno tra le zampe d'angolo, che non li raggiungono (verificato ruotando le coxe di ±45°).
- **Base** (PETG-CF, strutturale): vasca da z = −17 all'orlo a z = +14, con le sei gondole, il tunnel chiuso della batteria al centro (sezione chiusa lungo tutto il corpo), una paratia anteriore a tutta altezza e il telaio posteriore.
- **Guscio** (non caricato, non strutturale) da z = 14 a 37,5: tutta l'elettronica sopra l'orlo sta dentro plastica trasparente alle onde radio, quindi non serve una finestra apposita per l'antenna.
- **Batteria** nel tunnel, sfilabile dal retro, con i cavi verso la coda; il connettore T si accoppia nel vano di servizio in coda, dove stanno anche cicalino e pulsante. Staccare il T-plug è l'unico sezionamento vero dei servo (D-019): deve essere a portata di mano.
- **Regolatori** in piedi nel muso, di traverso, affacciati con 5 mm d'aria tra loro, piazzole di potenza in alto: uno sulla paratia, uno sulla parete del muso. Lontani dalla batteria, non intralciano i cavi dei servo. Il muso più lungo porta anche la camera più avanti: le ginocchia anteriori escono dall'inquadratura (da confermare in fase 6).
- **SSC-32** sul tetto del tunnel, morsettiera verso la coda, i due bus ai due lati. Gli spazi ai lati del tunnel restano liberi per i cavi dei servo e la loro scorta.
- **ESP32** su un vassoio a sbalzo sopra la striscia centrale della SSC-32, antenna in avanti; **camera** su una torretta della base, così togliendo il guscio non si tira il flat.
- Perché non più corto: con ±68 mm il volume interno (circa 500 cm³) era pari alla somma degli ingombri; 14 mm in più per parte danno il posto ai regolatori e al vano di servizio per circa 15 g di plastica.

## D-037 — Assetto di marcia confermato: femore verso il basso, tibia da 50 mm (2026-10-08, presa dopo la verifica chiesta dall'utente)

L'utente ha chiesto se il corpo non sia troppo basso, pensando al femore inclinato verso l'alto come negli esapodi comuni, e ha notato che il corpo è spesso rispetto alle zampe. Verifica (`calc/assetti.py` e posa nel modello): in marcia l'asse dei femori sta a 72 mm e la luce sotto il corpo è 55 mm; il femore punta verso il basso di 40–52° perché solo così piede e ginocchio restano entro circa 20 mm in orizzontale dai loro assi, cioè entro il 50 % dello stallo. Con il femore orizzontale o verso l'alto questa zampa darebbe 13–33 mm di luce, 50–53 % di coppia e nessuna alzata utile. La posa classica chiederebbe tibie da circa 95 mm e un ginocchio che si chiude molto di più: il doppio del gioco in punta. Resta quindi l'assetto di progetto. La tibia non si allunga per ora (`zam_Lt`: +10 mm alzerebbe il corpo di 10 mm a pari coppia, con il 20 % di gioco in più); si rivaluta dopo la prova di una zampa stampata. Lo spessore del corpo è dato da batteria, SSC-32 con le spine verticali ed ESP32: si alleggerisce il profilo con gli smussi (D-038), non la sostanza.

## D-038 — Guscio sfaccettato da 1,6 mm, fissato con otto viti M2; sportelli a incastro (2026-10-08, presa)

Guscio costruito pieno, smussato e poi svuotato a spessore costante: i fianchi scendono di 14 mm dal dorso piano (largo 60 mm), la coda di 10,5 mm. Da 48 a 35 g. Fissaggio: sei linguette della base che salgono dentro il bordo del guscio, lo centrano e portano gli inserti M2 (viti dai fianchi, visibili ma accessibili senza smontare nulla), più due viti dall'alto nella testa della torretta della camera. Scartati: viti dall'alto in colonnine alte 21 mm (fragili e in mezzo ai cavi) e viti interne raggiungibili solo da fori nel dorso. Sportelli del dorso e della coda senza viti, con dente e scatto: la batteria deve uscire senza attrezzi. Gli incastri vanno tarati in stampa. Anche la base ha uno smusso di 6 mm sul fondo lungo i fianchi; per averlo a spessore costante la vasca è ora uno svuotamento del pieno, e i colli delle gondole d'angolo si rifilano lungo la parete interna.

**Aggiunta a D-037 (stessa sera, in discussione con l'utente).** L'utente si aspettava un'andatura più bassa, con il ginocchio sotto i 90°. Confronto in `calc/andature.py` e in `dimensionamento.md`: l'assetto alto è il migliore per i servo (44 %) ma il peggiore per la stabilità (ribaltamento a 29° contro 37° dell'assetto medio e 49–54° di quelli bassi). L'assetto basso e largo "classico" chiede l'89 % dello stallo a tripode e il 71 % anche con cinque zampe a terra: con MG90S e 1,05 kg non rientra nella regola del 50 %. Punto emerso: la zampa v0 limita gli assetti bassi più della coppia, perché il ginocchio non si chiude sotto i 62° e il piede non si alza. Proposta: tenere le lunghezze dei segmenti, aumentare la chiusura del ginocchio nella rifinitura della zampa e lasciare l'altezza di marcia al firmware (da 58 a 75 mm), da scegliere dopo aver misurato coppia reale e massa. Da decidere con l'utente se la regola del 50 % resta rigida. **Chiusa da D-039.**

## D-039 — Il robot è progettato per due modi di marcia: alto e raccolto, basso e largo (2026-10-08, decisione dell'utente)

L'utente accetta di superare il 50 % dello stallo per camminare più basso; quale assetto usare si decide a robot costruito, misurando coppia reale, massa e temperatura dei servo. La meccanica deve permettere entrambi.

- **Modo alto** (asse dei femori a 72 mm, piede a 12 mm dall'asse): 44 % dello stallo, luce 55 mm, ribaltamento a 29°. La regola del 50 % resta il riferimento per questo modo.
- **Modo basso** (asse a 40 mm, piede a 40 mm): ginocchio tra 66° e 109°, luce 23 mm, ribaltamento a 54°, ma 89 % dello stallo a tripode. In mezzo c'è una gamma continua (per esempio asse a 50 mm e piede a 25 mm: 59 %, ginocchio 72–99°, ribaltamento a 43°): tabella in `dimensionamento.md`.
- **Cosa è cambiato nella meccanica**: il femore. L'anima piena tra le due piastre fermava il ginocchio a 62° e il femore a +25°. Ora tra le due culle passa un puntone inclinato di 35°, sezione 6,2 × 4 mm, dentro la sola fascia che resta libera a ogni angolo utile; l'anima torna spessa, con i due inserti M2, solo negli 8 mm accanto alla piastra delle squadrette, sopra la cassa dei servo. Campo libero verificato: femore da −60° a +55°, ginocchio da 50° a 145°. Il femore pesa 1,6 g in meno.
- **Verifica**: ciclo a tripode completo (dieci fasi, sei zampe) in tutti e due i modi, con passo 40 mm e alzata 20 mm: nessuna interferenza, angoli dentro i limiti con almeno 4° di margine nel modo basso.
- **Rischi accettati**: nel modo basso i servo di femore lavorano vicino allo stallo (scaldano, cedono, durano meno); il puntone è sottile e in PETG-CF può rompersi in montaggio (se succede: sezione piena in PETG non caricato, oppure un tirante metallico M2).
- Nessun cambio per l'elettronica: anche con i giunti carichi all'89 % i due regolatori (11 A dichiarati ciascuno) e il fusibile da 20 A restano sopra il fabbisogno.

## D-040 — Servo sbagliati in partenza: MG996R, non MG90S (2026-10-08, **aperta**: da decidere con l'utente)

L'utente ha detto di aver indicato per errore il file dell'MG90S: i servo che voleva usare sono gli MG996R della sua v1. Li ha entrambi. Conseguenze:

- La versione MG90S progettata fin qui è coerente e verificata, ma è un altro robot: circa 1 kg, corpo da 164 mm. Con gli MG996R (55 g l'uno, 40,7 × 19,7 × 42,9 mm, 11 kgf·cm dichiarati a 6 V: dati tipici **non ancora ricontrollati su fonte primaria**) i soli servo pesano 990 g e il robot supera i 2 kg.
- Stima preliminare con la stessa statica (coxa 50, femore 75, tibia 120 mm, 2,1–2,4 kg, asse a 90 mm e piede a 50 mm dall'asse): 4,7–5,4 kgf·cm, cioè 43–49 % dello stallo dichiarato (52–60 % se lo stallo reale è 9). Con gli MG996R l'assetto classico, basso e con il ginocchio sotto i 90°, sta attorno alla regola del 50 %: quello che con gli MG90S costa l'89 %.
- Non si riusano: quote, disposizione del corpo, bilancio di massa, cuscinetti e perni (troppo piccoli), sezione alimentazione del BOM (stallo dichiarato 2,5 A per servo: 45 A in tutto; i due Pololu da 11 A e i morsetti della SSC-32 non bastano; la batteria da 5200 mAh torna sensata).
- Si riusano: metodo e script (schizzi vincolati, primitive, assieme, interferenze, pose e ciclo a tripode), statica e confronto degli assetti, architettura (giunti su due lati con cuscinetto e perno, femore in due pezzi con puntone, gondole, vasca con tunnel della batteria e guscio non strutturale, vassoio dell'ESP32, torretta della camera, sportelli), ricerca su ESP32, SSC-32 e camera, regole di lavoro.
