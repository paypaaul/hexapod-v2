# Revisione del BOM v1 — catena elettrica

Revisore indipendente, 8 ottobre 2026. Documento rivisto: `docs/BOM.md` versione 1.
Lente: la catena elettrica dal pacco 2S fino a ogni utilizzatore.
Gravità: **bloccante** = così com'è si rompe o non funziona; **importante** = rilavorazione probabile, parte mancante, numero diverso da quello verificato; **minore** = chiarezza.
Sigle delle fonti (cartella `research_notes/Studio componenti esapode MG90S/`): `VA` = `verifica_alimentazione.md`, `VS` = `verifica_ssc32.md`, `VE` = `verifica_esp32cam_camera.md`, `VM` = `verifica_servo_mg90s.md`, `VB` = `verifica_batteria_cablaggio.md`.
Chiamate web usate: 3 su 6 (pagine Pololu #5673, #2815, #2813, rilette l'8/10/2026).

Stato del file: **completo**.

## Risposta breve alle sei domande

| Domanda | Esito |
|---|---|
| 1. Tensioni a ogni salto | Tornano sulla carta fino a 6,6 V di batteria, con circa 0,1 V di margine all'ingresso di B1. Non dimostrato: la logica della SSC-32 clone a fine scarica (E6) e il 5 V dell'ESP32 con due sorgenti in parallelo (E7). |
| 2. Correnti nei tre casi | Marcia e picchi: ok ovunque. Stallo: reggono batteria, T-plug, cavi e i due regolatori Pololu; **non** reggono l'interruttore B3 (E1) e, sulla carta, i morsetti della SSC-32 (E2). La frase "dimensionamento sullo stallo rispettato con margine" vale solo per i regolatori. Fusibile da 20 A: posto giusto, valore da confermare dopo la misura dello stallo (E3). |
| 3. Sottotensione | Stacca solo il rail servo, solo con i Pololu, solo se il firmware è vivo, e parte acceso all'avvio (E4). Niente stacca la logica: robot dimenticato acceso = pacco scarico a fondo (E5). |
| 4. Masse e disturbi | Manca il nodo di distribuzione e il ramo logica non ha protezione propria (E10). L'ESP32 su B2 non va in sottotensione; il rischio è la logica della SSC-32 (E6). |
| 5. GPIO | 21, 47, 1, 42 sono coerenti con la mappa dei pin. Osservazioni minori in E13. |
| 6. Cosa manca | Alimentazioni del traslatore (E8), protezione contro il ritorno di corrente verso l'USB (E7), nodo di distribuzione e fusibile del ramo logica (E10), resistenza e diodo per l'abilitazione a prova di guasto (E4), interruttore che si possa spegnere da firmware (E5). |

## Rilievi

### E1 — bloccante rispetto al requisito "dimensionato sullo stallo" (in marcia normale funziona) — B3, interruttore Pololu #2815

- BOM, tabella "Catena elettrica", riga "Interruttore B3": "17,2 A ... 6 A continui a 55 °C; 16 A a 150 °C ... lo stallo totale è sopportato solo per decine di secondi".
- VA riga 5 (fonte Pololu): "Continuous current at 150°C 16 A", nota "At 12 V with ambient temperature of 22°C in still air"; Ron massima 13 mΩ a 4,5 V e 8,6 mΩ a 10 V. Pagina Pololu riletta: "With adequate cooling, or for brief periods if the MOSFETs are not hot to begin with, currents up to the listed maximums are attainable" (nessuna durata) e "Do not use this switch as an emergency cutoff or similar safety disconnect".
- Calcolo, P = R × I²: lo stallo totale (17,2 A; 18,7 A con i numeri di E3) supera la corrente che porta la scheda a 150 °C (16 A), e quel dato vale a 12 V, dove la Ron è 8,6 mΩ. Con la 2S a 6,6 V la Ron sta fra 8,6 e 13 mΩ: 0,0086 × 17,2² = 2,5 W fino a 0,013 × 17,2² = 3,8 W, contro 0,0086 × 16² = 2,2 W del punto "150 °C". Le "decine di secondi" non compaiono in nessuna fonte.
- Il fusibile da 20 A non interviene a 17,2 A (86 %): l'interruttore è l'anello più debole e nulla lo protegge.
- Sul picco realistico (11 A): 0,0086–0,013 × 11² = 1,0–1,6 W su 20 × 23 mm, fra il punto "55 °C" (6 A) e il punto "150 °C" (16 A). In marcia (4,5–5 A) è sotto i 6 A: ok. Dentro un corpo chiuso in PETG-CF (68–74 °C) la scheda non va appoggiata alla plastica.
- B3-alt non risolve così com'è scritto: "contatto fino a 50 mΩ" significa, al massimo dichiarato, 0,05 × 17,2 = 0,86 V e 0,05 × 17,2² = 14,8 W in stallo, e 0,05 × 11 = 0,55 V sul picco: a batteria a 6,6 V il regolatore B1 (gli servono 6,2–6,3 V) andrebbe in caduta. Serve il valore tipico da datasheet prima di proporlo.
- Correzione, in ordine di preferenza:
  1. Togliere l'interruttore dal percorso dei servo: batteria → fusibile → nodo di distribuzione → ingressi dei due B1 sempre collegati; il rail servo si accende e si spegne dai pin ENA (regolatore disabilitato: "approximately 100 µA plus 2 µA per volt on VIN", pagina Pololu #5673: circa 0,115 mA l'uno a 7,4 V). L'interruttore Pololu resta sul solo ramo logica (B2 + VL + partitore), dove passa meno di 1 A. Vale solo con i Pololu B1 e richiede la correzione E4. Toglie anche 8,6–13 mΩ dal percorso dei servo.
  2. Oppure un sezionatore meccanico da almeno 30 A (ponticello estraibile) al posto dell'interruttore.
  3. In ogni caso togliere "decine di secondi" o sostituirlo con una prova al banco (17 A per 60 s, temperatura misurata sulla scheda).

### E2 — importante — Morsetti VS della SSC-32: lo stallo per lato supera la corrente continua raccomandata

- BOM, riga "Morsetto VS della SSC-32, per lato": "8,5 A ... 15 A di picco, 3–5 A continui (dato Lynxmotion; per il clone non esiste) ... ok sulla carta". Nota sotto la sezione B: "il dimensionamento sullo stallo è rispettato con margine".
- VS riga 3: "VS peak current: max 15 amps per side"; "VS steady current: max 3-5 amps per side recommended"; "senza condizioni di prova"; "Per il clone non esiste alcun dato". VA punto 3: "Il dimensionamento ... poggia quindi su un limite non verificato".
- Calcolo: 8,5 A di stallo per lato = 1,7–2,8 volte i 3–5 A continui (8,5 / 5 e 8,5 / 3). Anche il picco realistico (5,5 A) è sopra i 3–5 A. "Ok sulla carta" è vero solo se lo stallo dura quanto un "picco", durata che Lynxmotion non dichiara.
- La ripartizione per lato in marcia non è 50/50: nel tripode un lato ha due zampe in appoggio e l'altro una, a turno. Il picco sul lato carico può arrivare a 2/3 del totale: 10,8 × 2/3 = 7,2 A, non 5,5 A. La media sul ciclo resta metà (1,5–2,3 A), sotto i 3 A.
- Correzione: (a) riscrivere l'esito come "da confermare" e la nota come "rispettato per i regolatori; non dimostrato per SSC-32 e interruttore"; (b) aggiungere alla domanda 2 la larghezza delle piste VS e il passo dei morsetti del clone; (c) un fusibile MINI da 10 A per lato fra l'uscita di ogni B1 e il morsetto VS (stallo 8,5–9 A = 85–90 %: limita un guasto sotto i 15 A di picco); (d) nel firmware, togliere gli impulsi ai servo fermi sotto sforzo dopo pochi secondi; (e) alternativa da decidere prima del CAD: barra di alimentazione esterna per +V e massa dei servo, con solo segnale e massa verso la SSC-32.

### E3 — importante — Corrente di stallo: il BOM usa 0,946 A, il registro delle decisioni 1,0 A; la logica non è sommata

- BOM: "17 A dei 18 servo in stallo", "8,5 A" per lato, "17,2 A" lato batteria, fusibile "86 %".
- `docs/decisioni.md` D-005: "Corrente di stallo di progetto: 1,0 A per servo a 6 V ... 18 A nel caso peggiore". VM riga 13: "1.0 A non è un limite superiore garantito" (il dato è di un clone analogico; Tower Pro non pubblica correnti).
- Ricalcolo con D-005, I_batt = I_out × 6,0 / (0,9 × 6,6): 18 × 6 / 5,94 = 18,2 A; più B2 (0,5 A × 5 V / 5,94 = 0,42 A) e logica SSC-32 (0,1 A) = **18,7 A = 94 % del fusibile**; 9,0 A per lato. Con 0,946 A: 17,2 + 0,5 = 17,7 A = 89 %.
- Sensibilità: con 1,1 A misurati, 18 × 1,1 × 6 / 5,94 = 20,0 A, più la logica 20,5 A = 103 %: "non scatta in stallo" non sarebbe più vero.
- Anche la media in marcia (4,5 A) non comprende la logica: 4,6 A × 6 / 5,94 = 4,65 A più 0,2–0,5 A = circa 5 A.
- Correzione: allineare BOM e D-005 su un solo valore; rifare le tre colonne sommando la logica; scrivere che il valore del fusibile (20 o 25 A; il T-plug si ferma a 25 A) si fissa dopo la misura dello stallo su un servo reale (già prevista: domanda 1); comprare un assortimento 15 / 20 / 25 A.

### E4 — importante — B10: lo spegnimento del rail servo non è a prova di guasto e la resistenza da 10 kΩ non ha una funzione dichiarata

- BOM B10: "MOSFET N a segnale, es. 2N7000 (+ 1 resistenza 10 kΩ) — porta a massa i pin ENA dei due regolatori B1 su comando dell'ESP32"; GPIO42.
- VA punto 5: "Il pin ENA del D42V110F6 è abilitato di default (pull-up 1 MOhm a VIN): se la ESP32 è spenta, in reset o in bootloader, il rail servo resta ACCESO. Lo stacco per sottotensione comandato dalla ESP32 non è quindi fail-safe". Pagina Pololu riletta: "This pin is pulled up to VIN by through a 1 MΩ resistor to enable the regulator by default"; nessuna soglia pubblicata.
- Conseguenze: (a) all'accensione i servo sono alimentati prima che il firmware parta, insieme all'avvio di SSC-32 e B2; (b) con l'ESP32 bloccata, in reset, in bootloader o durante il caricamento del firmware il rail resta acceso e l'arresto a 3,3 V per cella non esiste; (c) se la 10 kΩ venisse montata fra ENA e massa, ENA resterebbe a 8,4 × 10 / (1000 + 10) = 0,08 V e il MOSFET N, che può solo tirare verso massa, non potrebbe mai accendere il rail.
- Correzione: logica invertita, spento di default. ENA dei due regolatori uniti; resistenza verso massa di 47 kΩ (con i due pull-up da 1 MΩ in parallelo: 8,4 × 47 / (500 + 47) = 0,72 V a riposo; 22 kΩ danno 0,35 V); GPIO → diodo in serie (anodo sul GPIO) → ENA, così il livello alto vale 3,3 − 0,3…0,6 = 2,7–3,0 V e il pull-up verso VIN non arriva al GPIO (VA riga 1: mai un GPIO in presa diretta su ENA). La soglia di ENA non è pubblicata: i due livelli vanno provati al banco prima di fissare i valori. Aggiungere il watchdog dell'ESP32 e, se si vuole, il pin PG dei regolatori su un GPIO libero ("An external pull-up resistor ... is required", 100 kΩ consigliati; "drives low during soft start and while the regulator is disabled").
- Se si resta sullo schema attuale: dichiarare nel BOM che il rail parte acceso e che la 10 kΩ va fra gate e massa; il 2N7000 ha soglia fino a 3,0 V (datasheet, non ricontrollato) e con 3,3 V di gate lavora al limite: meglio un BSS138.

### E5 — importante — Niente stacca la logica: robot dimenticato acceso o cicalino lasciato inserito scaricano il pacco a fondo

- BOM: "Soglie LiPo: allarme a 3,5 V per cella, arresto dei servo a 3,3 V per cella, mai sotto 3,0 V". Gli unici attuatori sono B10 (solo rail servo) e B8 (solo suono).
- Calcolo del carico che resta dopo l'arresto dei servo, a 6,6 V: ESP32 0,14 A × 5 V / (0,9 × 6,6 V) = 0,118 A; logica SSC-32 fino a 0,1 A (BOM); due B1 disabilitati 2 × (100 + 2 × 6,6) µA = 0,23 mA; LED dell'interruttore 65 µA/V × 6,6 V = 0,43 mA (VA riga 5); partitore 6,6 / 147 kΩ = 0,045 mA. Totale circa **0,17–0,22 A**. Se sotto 3,3 V per cella restano 260 mAh (5 %, stima), bastano 260 / 200 = 1,3 ore per scendere sotto 3,0 V per cella. Dal pieno, con i servo spenti: 5200 / 200 = 26 ore.
- "Mai sotto 3,0 V" non è quindi garantito da nessun componente.
- Cicalino B8: sta sulla presa di bilanciamento, a monte dell'interruttore. Le note di ricerca dicono "assorbe corrente in permanenza ... va staccato quando il robot non è in uso" e "Assorbimento del cicalino BX100: NON TROVATO" (`alimentazione.md`, righe 294 e 298). Il BOM non riporta l'avviso e con la prolunga C6 il cicalino diventa fisso. Con 10 mA ipotetici: 5200 / 10 = 520 ore, 22 giorni dal pieno.
- Correzione: (a) sul ramo logica (vedi E1) usare il **Pololu Big Pushbutton Power Switch with Reverse Voltage Protection, HP (#2813)** al posto del #2815: stesse portate (6 A a 55 °C, 16 A a 150 °C), pin OFF: "A high pulse (> 1 V) on this pin turns off the switch (e.g. allowing the target device to shut off its own power)", consumo da spento "< 0.2 μA" (pagina Pololu #2813). A 3,2 V per cella il firmware spegne il rail servo e poi toglie alimentazione a sé stesso e alla SSC-32. Serve un GPIO libero (41). Avvertenza Pololu: "Switch can lose its state when power is disconnected". (b) Scrivere nel BOM: a fine uso si staccano T-plug e presa di bilanciamento. (c) Misurare l'assorbimento del cicalino.

### E6 — importante — Logica della SSC-32 clone alimentata da VL: l'esito "ok" non è dimostrato a fine scarica

- BOM, riga "Logica SSC-32 (VL)": "6,4–8,4 V dalla batteria ... 6–12 V (venditore del clone) ... ok; regolatore del clone non identificato".
- VS riga 8c: "Il regolatore del clone è un componente DPAK a 3 terminali non identificato: se fosse un 78M05 (dropout tipico circa 2 V) a batteria scarica (6.4 V) la logica scenderebbe sotto 5 V". VA riga 7, punto 6: i limiti Lynxmotion "per il clone ... NON è garantito".
- Calcolo: resistenza fra batteria e nodo dopo l'interruttore circa 20 mΩ (interruttore 8,6–13 mΩ, verificato; 0,6 m di 14 AWG a 8,28 mΩ/m = 5 mΩ; fusibile e contatti circa 5 mΩ, stimati). Sul picco da 11 A la caduta è 0,22 V: alla soglia di arresto VL = 6,6 − 0,22 = 6,4 V; a 6,4 V di batteria 6,2 V. Con un regolatore da 2 V di caduta la logica starebbe a 4,2–4,4 V, con uno da 1,2 V a 5,0 V senza margine; un eventuale diodo di selezione in serie (sulla Lynxmotion "MAX(VL, VS1) minus roughly 0.7V") toglie altri 0,7 V. Un reset del micro della SSC-32 ferma gli impulsi di tutti i 18 servo proprio a batteria bassa.
- Il BOM non mette fra le domande aperte la prova che VA chiede all'utente: "Misura col tester della tensione minima a cui il micro della scheda resta acceso (alimentatore da banco su VL, scendere da 8 V)".
- Correzione: esito "da confermare"; aggiungere alle domande aperte la sigla del regolatore e la prova con alimentatore da banco (VL da 8 V in giù, leggere il pin 5 V). Se il clone chiede più di 6,3 V: alzare la soglia di arresto, oppure alimentare la logica dal 5 V di B2 (2,5 A, ne usa 0,5) dopo aver capito lo schema del clone.

### E7 — importante — 5 V dell'ESP32: la via USB-C va trattata come quella di base, e con il PC collegato ci sono due sorgenti in parallelo

- BOM C3: spinotto USB-C "solo se il pin 5V della scheda non la alimenta", stato "A (condizionale)". Tabella dei connettori: "PC | porta USB-C "TTL" della scheda | resta accessibile dall'esterno".
- VE riga 7: nello schema del venditore l'AMS1117 è alimentato dalla rete USB_5V e il pin 5V sta a valle del diodo D3, "quindi sarebbe solo un'USCITA"; due segnalazioni dello stesso sintomo su cloni simili; "Scelta prudente per il cablaggio: portare il 5 V del BEC su una porta USB-C ... e NON sul pin 5V, finché la misura non dice il contrario".
- Problema 1: il BOM rovescia la scelta prudente. Lo spinotto costa pochi euro: va comprato comunque e il percorso del 5 V in tabella va disegnato via USB-C.
- Problema 2: con B2 su una porta USB-C e il PC sull'altra (situazione normale mentre si mette a punto l'andatura a batteria inserita) l'uscita di B2 (5 V ±4 %: 4,8–5,2 V) e il VBUS del PC finiscono sulla stessa rete USB_5V. A robot spento il 5 V del PC arriva all'uscita di B2. Nessuna fonte dice che sia ammesso e nel BOM non c'è nulla che lo impedisca. Se le due porte abbiano diodi separati non è noto.
- Correzione, una delle tre: (a) diodo Schottky da almeno 1 A in serie all'uscita di B2: con 0,3–0,45 V di caduta l'AMS1117 riceve 4,35–4,9 V contro i 3,3 + 1,1…1,3 = 4,4–4,6 V che gli servono (caduta dell'AMS1117 non ricontrollata, VE): margine nullo nel caso peggiore, da provare al banco con il Wi-Fi in trasmissione; (b) cavo o adattatore USB-C con il VBUS interrotto per il PC; (c) ingresso dal pin 5V, se la misura della domanda 4 dice che è un ingresso.
- Numero da correggere: riga "ESP32-S3-CAM ... picco 0,36 A" conta solo il modulo (355 mA, VE riga 7). La OV3660 assorbe 98 mA da attiva ed è sempre attiva (PWDN a massa con 1 kΩ, VE): 0,355 + 0,098 = 0,45 A, più scheda TF e LED. B2 (2,5 A) basta comunque.

### E8 — importante — C1, traslatore di livello: nel cablaggio mancano le due alimentazioni di riferimento

- BOM C1: "le resistenze di pull-up tengono la linea a riposo durante il reset". Tabella dei connettori: "ESP32 (pin 2,54 mm) | C1, SSC-32 (TX, RX, GND) | Dupont femmina".
- VE punto 1: GPIO21 al reset è in alta impedenza, serve un pull-up verso 3,3 V. VS riga 7: ingresso dell'ATmega al massimo VCC + 0,5 V.
- Un modulo a BSS138 funziona solo con LV e HV alimentati: senza, non ci sono pull-up e la linea TX non sta a riposo. La tabella non elenca né il 3,3 V né il 5 V, e non dice da dove prendere HV.
- Correzione: LV dal pin 3V3 dell'ESP32; HV dal pin 5 V della logica della SSC-32, non da B2, così il pull-up alto segue l'alimentazione del micro che lo riceve. Prima di collegare: misurare la tensione a riposo sul pin TX del clone (VS, domanda 5). Aggiungere le due righe alla tabella dei connettori.
- Nota: quando il PC è collegato alla micro-USB della SSC-32, il convertitore USB della scheda e l'ESP32 pilotano lo stesso RX. Sulla SSC-32 originale i ponticelli del DB9 vanno tolti per usare la seriale TTL (`ssc32.md`, riga 178); per il clone non è documentato: scollegare TX durante la configurazione da PC.

### E9 — importante — B1-alt (Hobbywing) non è equivalente a B1 e il BOM non lo dice

- BOM, nota sotto la sezione B: "La scelta fra B1 e B1-alt è tua: i Pololu pesano 42 g in meno, hanno caduta documentata e il pin per spegnere il rail; gli Hobbywing costano circa la metà."
- Mancano quattro conseguenze:
  1. Margine sullo stallo: 10 A continui contro 8,5–9 A per lato = 85–90 %. "Con margine" vale per i Pololu.
  2. Nessun pin di abilitazione (`alimentazione.md`, riga 293: "resta solo l'arresto software dei servo ... più il cicalino"): B10, GPIO42 e l'"arresto dei servo a 3,3 V" restano senza attuatore, e la correzione 1 di E1 non si applica.
  3. Uscita su cavetti con spinotto servo, sezione non dichiarata, da tagliare e mettere in parallelo sul morsetto VS (VA righe 3–4 e punto 6).
  4. Il 30603000 non ha protezione da inversione ("the UBEC will be seriously damaged", VA riga 3) e nessuno dei due dichiara la caduta minima ("The output voltage will reduce with the battery voltage", VA riga 4): a 6,6 V di batteria i 6,0 V non sono garantiti.
- Correzione: riportare questi punti nella riga B1-alt e nella domanda 6; aggiungere "misurare l'uscita col tester prima di collegare la SSC-32" (VA, "Gap chiusi").

### E10 — importante — Manca il nodo di distribuzione; il ramo logica in 22 AWG è protetto solo dal fusibile da 20 A

- BOM B12–B14 e tabella dei connettori: "B5, B3, B1, B2 | cavi 14 / 16 / 22 AWG | saldatura"; B14: 22 AWG per "VL, 5 V, partitore, ENA"; un solo fusibile (B4, 20 A).
- Un cavo 14 AWG deve dividersi in tre: B1 sinistro, B1 destro, ramo logica. I fori di potenza del D42V110F6 sono "sized to accommodate 14 AWG wires" (uno per foro): il BOM non ha né un componente né una giunzione per la derivazione, e non indica dove sta il punto unico di massa.
- Ramo logica: il 22 AWG vale 53 mΩ/m (VB, calcoli). Un guasto parziale da 15 A, sotto la soglia del fusibile, dissipa 0,053 × 15² = 12 W per metro di cavo senza che nulla intervenga.
- Correzione: (a) aggiungere due derivazioni da almeno 20 A (una per il positivo, una per il negativo) o una giunzione saldata descritta; il negativo è il punto a stella: batteria −, massa dei due B1, massa di B2; (b) fusibile da 1–2 A all'inizio del ramo logica; (c) la resistenza da 100 kΩ del partitore va montata sul lato del nodo, così il filo verso l'ADC porta al massimo 8,4 / 100 kΩ = 84 µA; (d) verificare col tester che sulla SSC-32 clone VS1−, VS2− e VL− siano la stessa massa: se sì, il filo VL− e la massa della seriale stanno in parallelo ai ritorni dei servo (con 0,3 m: 16 mΩ contro 4 + 4 mΩ, circa l'11 %, 1,9 A in stallo totale): accettabile, ma va disegnato così.

### E11 — minore — B1: "circa 14 A" è marcato V ma è un'interpolazione; calore nel corpo chiuso

- BOM B1: "corrente continua tipica circa 14 A con ingresso 7–8,4 V (letta dal grafico, in aria libera)", dato "V".
- VA riga 2: "NESSUNA curva a 6 V"; "il valore ~14 A a 6 V resta un'interpolazione, non un dato del costruttore"; fra 10 e 14 A la caduta "NON è documentata"; in una scocca stampata "va declassata". Dati del costruttore: famiglia 8–15 A; 11 A a 42 V d'ingresso.
- Stallo per lato 8,5–9 A = 61–64 % di 14 A, 77–82 % di 11 A: il dimensionamento regge, ma l'etichetta giusta è S. Con rendimento 0,9–0,95 ogni regolatore dissipa in stallo 54 W × 5–11 % = 3–6 W: nel CAD servono aperture d'aria vicino ai due B1.
- Le due uscite sono indipendenti al ±3 % (5,82–6,18 V): fra zampe sinistre e destre possono esserci fino a 0,36 V di differenza. Misurarle e, se serve, compensare nel firmware.

### E12 — minore — Misura di batteria: errore non tarato pari a metà della distanza fra le soglie

- BOM B9 e "Soglie LiPo" (7,0 V e 6,6 V).
- VE riga 4: campo 0–2900 mV, errore ±50 mV. Riportato alla batteria: 50 × 147 / 47 = ±156 mV. Resistenze all'1 %: errore sul rapporto fino a 0,68 × 2 % = 1,36 %, cioè ±90 mV a 6,6 V. Totale fino a ±0,25 V contro 0,4 V fra allarme e arresto.
- Correzione: taratura a un punto contro il multimetro; media su 1–2 s, perché i picchi abbassano il nodo di 0,2–0,4 V; dichiarare che le soglie valgono sotto carico (la ricerca lo dice, il BOM no); prendere il partitore sul nodo d'ingresso dei regolatori. A 6,6 V su quel nodo il margine di B1 è 6,6 − 6,3 = 0,3 V; a 6,6 V sulla batteria, tolta la caduta di E6, resta circa 0,1 V.

### E13 — minore — Assegnazione dei GPIO: corretta, con tre precisazioni

- BOM: "tutti verificati sul datasheet Espressif come liberi con camera, PSRAM e USB in uso".
- Il datasheet Espressif dice quali pin sono presi da PSRAM e USB e quali hanno impulsi all'accensione (VE righe 3 e 5). Che 21, 47, 1 e 42 siano liberi su questa scheda viene dall'inserzione del venditore e dal disegno Freenove (VE riga 2; `dimensioni-componenti.md`): l'etichetta giusta è S/C.
- RX su GPIO47: VE riga 3 lo indica come pin particolare (dominio VDD_SPI / VDD3P3_CPU), "da provare a banco prima di affidargli la RX". GPIO14 è un pin ordinario (l'impulso basso di 60 µs all'accensione non conta per un ingresso): usarlo come RX da subito e tenere 47 di riserva.
- Lo stato di GPIO42 al reset non è nei file di verifica: la rete su ENA deve dare "spento" anche con GPIO42 flottante (vedi E4).
- Con E4 ed E5 servono fino a due pin in più (OFF dell'interruttore, PG): 2, 41 e 47 bastano.

### E14 — minore — Montaggio dei condensatori B6 e messa in servizio della seriale

- BOM B6: "uno su ciascun morsetto VS"; B15: "sotto i morsetti a vite: puntalini". Un puntalino per 16 AWG non accoglie anche il reoforo del condensatore: indicare un puntalino doppio, oppure saldare il condensatore su un connettore a 3 poli da inserire in un canale libero di ciascun banco (15 e 31; +V al centro, massa verso il bordo, VS riga 4). Il componente è polarizzato: segnare il verso.
- BOM: "Seriale: 115200 baud". VS riga 5: la Lynxmotion esce a 9600; il 115200 del clone è una dichiarazione del venditore non verificata (VS riga 8a). Aggiungere: tenere premuto BAUD, leggere i LED, inviare "VER".

## Parti da aggiungere o cambiare (riassunto per l'autore)

| Voce | Modifica | Rilievo |
|---|---|---|
| B3 | fuori dal percorso dei servo; sul ramo logica Pololu #2813 al posto del #2815 | E1, E5 |
| B4 | assortimento MINI 15 / 20 / 25 A; valore dopo la misura dello stallo | E3 |
| nuovo | 2 portafusibili + 2 fusibili MINI 10 A, uno per lato VS (facoltativo) | E2 |
| nuovo | fusibile 1–2 A per il ramo logica | E10 |
| nuovo | 2 derivazioni da almeno 20 A (positivo e negativo) | E10 |
| B10 | resistenza verso massa 22–47 kΩ + diodo in serie al GPIO; valori dopo la prova al banco | E4 |
| C3 | da comprare comunque; più diodo Schottky da almeno 1 A oppure cavo USB senza VBUS | E7 |
| C1 | due cavetti in più: LV (3V3 ESP32) e HV (5 V SSC-32) | E8 |
| Domande aperte | sigla del regolatore e tensione minima di VL del clone; piste VS e passo dei morsetti; assorbimento del cicalino | E2, E5, E6 |

## Controllato e trovato corretto

- Partitore: 8,4 × 47 / 147 = 2,686 V, dentro 0–2,9 V; satura a 2,9 × 147 / 47 = 9,07 V; GPIO1 è ADC1_CH0 (VE riga 4).
- Correnti lato batteria con la formula del BOM: 10,8 × 6 / (0,9 × 6,6) = 10,9 A; 17,03 × 6 / 5,94 = 17,2 A; percentuali del fusibile 22,5 / 55 / 86 % coerenti con quei dati di partenza.
- B1: ingresso ≥ 6,3 V per 6,0 V pieni (6,0 + 0,27 = 6,27 V a 8 A; 6,34 V a 10 A, VA riga 2). I due Pololu reggono lo stallo per lato (8,5–9 A) dentro il campo in cui la caduta è documentata (fino a 10 A).
- B2: minimo 5,3 V contro 6,0–8,4 V; 2,5 A contro 0,5 A.
- VL: 6,4–8,4 V dentro il 6–12 V del venditore e il nominale 6–12 V della SSC-32U.
- Livelli logici: 0,8 × 3,3 = 2,64 V < 0,6 × 5 = 3,0 V, quindi il TX va traslato; 5 V > 3,6 V, quindi anche l'RX. C1 copre entrambi i versi e i suoi pull-up tengono TX a riposo con GPIO21 in alta impedenza, purché LV sia alimentato (E8).
- GPIO 21, 47, 1, 42: nessuno è di strapping (0, 3, 45, 46), della PSRAM (35–37), della camera o dell'USB (19, 20); 21, 42, 47 non sono nella tabella degli impulsi all'accensione; ADC1 funziona con il Wi-Fi.
- Canali 0–8 su VS1 e 16–24 su VS2, ponticelli VS1=VS2 e VL=VS tolti: coerente con la guida SSC-32U (VA riga 7, VS riga 2). Ordine dei morsetti del clone e verso delle spine servo come in VS righe 4 e 8c.
- Batteria 50 × 5,2 = 260 A; T-plug 25 A; 14 AWG e 16 AWG: adeguati a 17–19 A e 9 A (portate dei cavi da fonte secondaria).
- Fusibile sul positivo subito dopo la batteria, prima di ogni derivazione: posizione corretta. Portafusibile FHM adatto a MINI 2–30 A, 58 V (VA riga 8).
- Condensatori da 16 V su un rail da 6 V; tempo del comando di gruppo: 9 × 7 + 9 × 8 + 5 = 140 caratteri × 10 bit / 115200 = 12,2 ms.
- Servo a 6,0 V +3 % = 6,18 V: sotto i 6,6 V della prova di coppia Tower Pro e lontano dagli 8,4 V che hanno bruciato un clone (VM riga 9).

## Non controllato

- Schema reale della SSC-32 clone: regolatore, diodi di selezione, masse comuni, larghezza delle piste, passo e sezione dei morsetti, tensione del pin TX.
- Assorbimento del cicalino BX100 (non dichiarato in nessuna fonte).
- Curva tempo-corrente, resistenza a freddo e declassamento in temperatura del fusibile MINI da 20 A (sito Littelfuse non raggiungibile, VA).
- Portate dei cavi siliconici (32 A, 22 A) e del T-plug (25 A): fonti secondarie non riaperte.
- Caduta dell'AMS1117; soglia del 2N7000; stato di GPIO42 al reset sul datasheet Espressif.
- Soglia di ENA e valore del limite di corrente del D42V110F6 (non pubblicati); comportamento con una tensione applicata all'uscita di B2.
- Collegamento fra le due porte USB-C sulla scheda UICPAL.
- Diametro dei fori grandi dell'interruttore Pololu rispetto a un cavo 14 AWG.
- Rendimento 0,9 dei regolatori (assunto dal BOM, non letto sui grafici).
- Effetto del PETG-CF sull'antenna Wi-Fi; prezzi, disponibilità, meccanica.
