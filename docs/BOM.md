# BOM — Hexapod v2 (MG996R)

Versione 2.1 (10 ottobre 2026): prezzi e link d'acquisto letti il 10 ottobre 2026, carrelli per negozio e costo totale. Versione 2.0 (8 ottobre 2026) **approvata dall'utente** l'8 ottobre 2026. Le domande in fondo restano aperte: non bloccano il CAD. Nasce dallo studio in `studio-componenti.md`; il perché delle scelte è lì e in `decisioni.md` (D-043, D-045).
La viteria è provvisoria: misure, lunghezze e quantità esatte si ricavano dal modello nella fase 5.

Legenda **dato**: V = verificato su fonte primaria; S = stimato o da fonte secondaria; C = da confermare sul pezzo reale.
Legenda **stato**: P = già in tuo possesso; A = da comprare; ? = dimmi tu; — = non comprare per ora.
Prezzi in euro **IVA inclusa**, letti il 10 ottobre 2026 sulle pagine dei negozi (V) oppure stimati (S: negozio non leggibile dagli strumenti, come Amazon.it e AliExpress, o conversione da PLN, SEK, USD). Si ricontrollano all'ordine. Criterio di scelta (D-068): il costo consegnato in Italia, spedizioni comprese, con pochi negozi; AliExpress solo per la minuteria, con l'alternativa europea. Il carrello per negozio e il totale sono nella sezione "Carrelli e costo totale".

## Schema di alimentazione

```
Batteria 2S ── T-plug ── F1 (30 A) ── derivazione + ──┬── regolatore 6 V sinistro ── file VS1 e massa della SSC-32, dal retro (9 servo)
                                                      ├── regolatore 6 V destro   ── file VS2 e massa della SSC-32, dal retro (9 servo)
                                                      └── F2 (2 A) ── interruttore ──┬── regolatore 5 V ── ESP32
                                                                                     ├── VL della SSC-32 (logica)
                                                                                     └── partitore ── GPIO1
GPIO42 ── diodo ── pin di abilitazione dei due regolatori 6 V (tirati a massa: rail spento di default)
Presa di bilanciamento ── cicalino di sottotensione
```

- I due regolatori servo sono sempre collegati alla batteria ma **spenti di default**: li accende l'ESP32 quando la SSC-32 sta già mandando impulsi. Nel percorso dei servo non c'è nessun interruttore.
- La potenza dei servo entra nelle file degli header **dal retro della SSC-32**, con un filo stagnato saldato lungo i pin: i morsetti e le piste della scheda non la portano. Ponticelli "VS1 VS2" e "VS VL" tolti.
- L'interruttore sta sul ramo logica (meno di 1 A). **A fine uso si staccano T-plug e presa di bilanciamento**: il T-plug è anche il sezionamento d'emergenza dei servo.
- I negativi si uniscono in un solo punto (massa a stella) accanto ai regolatori.

## A. Già in possesso

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Dato | Stato |
|---|---|---|---|---|---|---|
| A1 | Servo | 18 | AZDelivery MG996R (confezioni da 5) | 55 g; 9,4 kgf·cm a 4,8 V, 11 a 6 V; 4,8–7,2 V; 2,5 A di stallo a 6 V; 40,7 × 19,7 × 42,9 mm; due cuscinetti; squadrette di plastica e viteria incluse | V (datasheet AZDelivery) | P |
| A2 | Scheda di controllo | 1 | UICPAL "ESP32-S3-CAM N16R8 RE1.3" | ESP32-S3 N16R8; 62,6 × 28,3 mm (67,5 con l'antenna); 2 USB-C; nessun foro di fissaggio | S, C | P (da confermare) |
| A3 | Camera | 1 | UICPAL "OV3660-75MM", lente 120° "GOOD" | flat da 75 mm; testa 8,5 × 8,5 mm, alta circa 6 mm | S, C | P (da confermare) |
| A4 | Servo controller | 1 | clone "SSC32-V2.5" (AliExpress 1005001888185034) | 32 canali; PCB 72 × 55 mm, fori a 65,5 × 48,5 mm; header a foro passante; VL 6–12 V | S (disegno del venditore) | P |
| A5 | Batteria | 1 | OVONIC 2S 5200 mAh 50C hardcase, T-plug | 137–139 × 46–47 × 24–25 mm; 245–259 g; 260 A continui; cavi 12 AWG; bilanciamento JST-XH. Autonomia stimata 22–27 minuti in marcia classica | V (pagine del produttore) | P |

## B. Alimentazione

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Acquisto (10 ottobre 2026) | Dato | Stato |
|---|---|---|---|---|---|---|---|
| B1 | Regolatore del rail servo, 6,0 V | 2 (uno per lato) | **Pololu D42V110F6 (#5673)** | ingresso fino a 60 V; 11 A tipici dichiarati a 42 V, di più con ingresso basso (circa 13–14 A con la 2S: S); limita la corrente con gradualità; pin di abilitazione e power-good; protezione da inversione; 43,2 × 31,8 × 9 mm; 4 fori M2. Se al banco non basta, al suo posto va il D24V150F6 (#2882), stesso ingombro | Kamami: [D42V110F6](https://kamami.pl/step-down/1201579-6v-11a-step-down-voltage-regulator-d42v110f6-5902186330856.html), 2 × 52,38 € (V, gli ultimi 2 a magazzino). pololu.com 59,95 US$ più IVA e spedizione | V | A |
| B2 | Regolatore 5 V per l'ESP32 | 1 | Pololu D24V22F5 (#2858) | 5 V, 2,5 A; 17,8 × 17,8 mm; 2 fori M2 | Kamami: [D24V22F5](https://kamami.pl/en/step-down/561020-pololu-5v-25a-step-down-voltage-regulator-d24v22f5-pololu-2858-5906623437580.html), 17,84 € (V) | V | A |
| B3 | Interruttore generale (ramo logica) | 1 | Pololu Big Pushbutton Power Switch HP (#2813) | a pulsante; pin OFF per lo spegnimento da firmware; meno di 0,2 µA da spento; 20,3 × 25,4 mm | Kamami: [Pololu 2813](https://kamami.pl/en/digital-switches/561034-pololu-2813-big-pushbutton-power-switch-with-reverse-voltage-protection-hp-5906623477883.html), 7,87 € (V) | V | A |
| B3b | Pulsante d'accensione | 1 + 1 | pulsante da pannello Ø12 mm, momentaneo, normalmente aperto, a vite con dado, contatti a saldare | sul coperchio, collegato ai pin A e B della 2813 (in parallelo al suo pulsantino, come indica la pagina Pololu); corpo sotto il pannello circa 20 mm, da confermare sul modello scelto | Kamami: [pulsante 12 mm con dado](https://kamami.pl/przyciski/582435-momentary-push-button-okragly-przycisk-chwilowy-12mm-zolty-5906623460052.html), 2 × 0,58 € (V; giallo, alto 21 mm, NO o NC non dichiarato: C) | S | A (approvato il 9 ottobre 2026) |
| B4 | Fusibile principale F1 | assortimento 15 / 20 / 25 / 30 A | lama ATO/ATC, 32 V | 30 A in uso; 15 A per le prime accensioni | Kamami: [set Yato YT-83148](https://kamami.pl/bezpieczniki/1204000-zestaw-bezpiecznikow-ministandard-301szt-yt-83148-5906083091049.html), 301 fusibili ATO e MINI da 2 a 40 A, 7,73 € (V); copre anche i MINI da 2 A di B6 e i 3 e 5 A del banco | S | A |
| B5 | Portafusibile principale | 1 | in linea per lame ATO/ATC, cavi 12 AWG, con coperchio | da fissare al corpo, non appeso ai cavi | Amazon.it, circa 10 € (S: Amazon non è leggibile dagli strumenti; cercare "portafusibile lama ATO 12 AWG coperchio") | S | A |
| B6 | Fusibile del ramo logica F2 | 1 + 1 | portafusibile in linea MINI 18 AWG + fusibile MINI 2 A | il ramo logica usa cavo da 22 AWG: F1 da solo non lo proteggerebbe | Kamami: [portafusibile MINI con cavo 1 mm²](https://kamami.pl/zlacza-inne/1197193-gniazdo-bezpiecznika-10-mini-5900804107170.html), 0,92 € (V); fusibili da 2 A nel set di B4 | S | A |
| B7 | Condensatore sul rail servo | 2 + 2 | elettrolitico 2200 µF 16 V a bassa ESR, es. Panasonic EEUFR1C222 | Ø12,5 × 20 mm; saldato a una spina servo e inserito in un canale libero, uno per lato | Amazon.it, circa 8 € per 4 (S). Con le voci X: DigiKey [EEU-FR1C222](https://www.digikey.it/en/products/detail/panasonic-electronic-components/EEU-FR1C222/2433536), 4 × 1,79 € (V; **alto fino a 22 mm**, non 20) | S | A |
| B8 | Condensatore ceramico | 3 | 100 nF 50 V | due in parallelo a B7, uno sull'ingresso dell'ADC | Amazon.it, assortimento circa 6 € (S). Con le voci X: DigiKey Vishay K104K15X7RF5TL2, 0,18 € l'uno (V) | S | A |
| B9 | Allarme di sottotensione | 1 | cicalino LiPo 1–8S tipo "BX100" | sulla presa di bilanciamento; soglia regolabile; assorbe sempre: si stacca a fine uso | Kamami: [BX100](https://kamami.pl/wskazniki-rozladowania/582354-bx100-tester-napiecia-pakietow-lipo-1-8s-5906623459704.html), 3,50 € (V); posizione dei pin da guardare sul pezzo | S | A |
| B10 | Partitore per la misura di batteria | 1 + 1 | resistenze 100 kΩ e 47 kΩ, 1 % | 8,4 V → 2,69 V su GPIO1 | Kamami: [set resistenze 1 % da 820 pezzi](https://kamami.pl/rezystory-tht-14w/1199442-zestaw-rezystorow-cf-tht-14w-1-1-1-m-820-szt--5902186309630.html), 6,12 € (V): 100 k e 47 k; serve anche per B11 e per le voci X | V (campo ADC) | A |
| B11 | Accensione del rail servo | 1 + 1 | resistenza 47 kΩ (più una da 22 kΩ di riserva) e diodo 1N4148 | pin di abilitazione dei due B1 uniti e tirati a massa; GPIO42 → diodo → abilitazione. La soglia bassa non è pubblicata: valori da provare al banco | Kamami: [1N4148, 10 pz](https://kamami.pl/diody-schottky/1187768-dioda-impulsowa-1n4148-tht-500mw-75v-10-szt-5906623484720.html), 0,58 € (V); 47 k dal set di B10; il 22 k di riserva c'è solo al 5 % (0,01 €) | S, C | A |
| B12 | Connettore batteria lato robot | 1 conf. | T-plug maschio con codino **12 AWG** | la batteria ha la femmina (dalle immagini del produttore: da guardare sul pacco) | Amazon.it, circa 9 € (S: cercare "T-plug Deans maschio 12 AWG"). Il solo connettore da saldare: Electrokit 0,57 € (spedizione in Italia non confermata) | S, C | A |
| B13 | Derivazioni di potenza | 2 | morsetto a leva a 5 vie Wago 221-415 | fino a 4 mm², 32 A: uno per il positivo, uno per il negativo (massa a stella) | Kamami: [Wago 221-415](https://kamami.pl/szybkozlacza/1188363-wago-221-415-zlaczka-instalacyjna-5-przewodow-4mm-5902186324558.html), 2 × 0,81 € (V) | S | A |
| B14 | Cavo di potenza principale | 0,5 m rosso + 0,5 m nero | siliconico 12 AWG | T-plug → F1 → derivazioni | Amazon.it, circa 10 € (S). Leggibile: [Bits and Parts](https://www.bitsandparts.nl/en/silicone-wire-set-multi-core-12awg-3.3mm²-1-meter-red-+-black-p1905600), 9,95 € per 1 m + 1 m (V, spedizione in Italia non indicata) | S | A |
| B15 | Cavi verso i regolatori e la SSC-32 | 0,5 m + 0,5 m di 14 AWG; 0,6 m + 0,6 m di 16 AWG | siliconico | 14 AWG dalle derivazioni agli ingressi dei B1; 16 AWG dalle uscite dei B1 alle file della SSC-32 | Amazon.it, circa 20 € (S). Leggibile: Bits and Parts [14 AWG](https://www.bitsandparts.nl/en/silicone-wire-set-multi-core-14awg-2.08mm²-1-meter-red-+-black-p1905601) e [16 AWG](https://www.bitsandparts.nl/en/silicone-wire-set-multi-core-16awg-1.31mm²-1-meter-red-+-black-p1905602), 9,95 € l'uno (V) | S | A |
| B16 | Barre sulle file degli header | 1 m | filo di rame stagnato rigido Ø1 mm (18 AWG) | saldato sul retro della SSC-32 lungo le file VS e di massa di ogni lato | Amazon.it, circa 7 € la bobina (S) | — | A |
| B17 | Cavo logica | circa 2 m | siliconico 22 AWG, più colori | ramo logica, VL, 5 V, partitore, abilitazione | Amazon.it, kit di colori circa 14 € (S). Kamami ha il set 22 AWG 6 × 4 m a 20,67 € (V, caro per 2 m) | S | A |
| B18 | Distanziali | 4 | **M3 maschio-femmina da 5 mm** per il vassoio dell'ESP32 (D-051, approvato il 9 ottobre 2026; i regolatori stanno su slitte stampate e la SSC-32 su bugne del corpo) | | Amazon.it, kit circa 9 € (S). Leggibile: [Grobotronics](https://grobotronics.com/standoff-m3-metal-m-f-l5mm.html?sl=en), 0,20 € l'uno (spedizione non letta) | — | A |
| B19 | Termorestringente, stagno, flussante | 1 assortimento | — | giunzioni saldate | Kamami: [guaina 4/2 mm 10 × 1 m](https://kamami.pl/rurki-termokurczliwe/569152-rurki-termokurczliwe-czarne-4020-10-szt-x-1-metr-5900804072157.html) 2,99 €, [stagno 0,7 mm 100 g](https://kamami.pl/cyna-olowiowa/549284-cyna-lc60-070mm-100g-5906623404964.html) 7,47 €, [flussante 50 ml](https://kamami.pl/topnik-w-plynie/547791-topnik-tk-83-50ml-oliwiarka-ag-5901764323600.html) 1,98 € (V) | — | A |

Nota su B1: un regolatore serve 9 servo. Corrente stimata per lato: 5–6 A medi nella marcia classica, 8–9 A in quella bassa, picchi di 12–15 A, contro circa 13 A disponibili; oltre, il regolatore limita la corrente e il rail cala, senza spegnersi. Lo stallo contemporaneo di 9 servo (22,5 A) lo impedisce il firmware.

## C. Controllo, segnali, cablaggio dei servo

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Acquisto (10 ottobre 2026) | Dato | Stato |
|---|---|---|---|---|---|---|---|
| C1 | Traslatore di livello 3,3 V ↔ 5 V | 1 | modulo a 4 canali con BSS138 (tipo Adafruit 757) | TX e RX tra ESP32 e SSC-32 | Kamami: [KAmod Level Shift x4](https://kamami.pl/konwertery-napiec/1195428-kamod-level-shift-x4-dwukierunkowy-4-kanalowy-konwerter-poziomow-logicznych-5906623499489.html), 2,51 € (V; il MOSFET non è dichiarato, C). Adafruit 757 vero: [DigiKey](https://www.digikey.it/en/products/detail/adafruit-industries-llc/757/4990756), 4,23 € | S | A |
| C2 | Basetta di supporto | 1 + 2 + 1 | millefori 50 × 70 mm; 2 strip femmina 1 × 20; 1 strip maschio 1 × 40 | zoccolo per l'ESP32 (che non ha fori) e supporto per B2, C1, B10, B11; si taglia a 56 × 35 (D-053) | Kamami: [millefori 50 × 70](https://kamami.pl/plytki-uniwersalne/1204291-kamod-proto-50x70-dwustronna-plytka-uniwersalna-50-x-70-mm-5902186339903.html) 1,82 € e [strip maschio 1 × 40](https://kamami.pl/zlacza-goldpin/1207864-goldpin-czarny-1x40-szpil-prosty-do-druku-raster-254mm-5906623439881.html) 0,43 € (V); strip femmina 1 × 20 su Amazon.it, circa 5 € (S) | C | A |
| C3 | Ingresso del 5 V nell'ESP32: alternativa | 1 + 1 | spinotto USB-C maschio a 90° a saldare + diodo Schottky 1N5817 | solo se la scheda non si accende dal pin 5V | spinotto: Amazon.it circa 8 € per una confezione (S; AliExpress circa 2 €). Diodo: Kamami [1N5819](https://kamami.pl/diody-schottky/1187767-dioda-schottkiego-1n5819-tht-40v-1a-10-szt-5906623484713.html), 0,46 € per 10 (V; il 1N5817 non c'è, il 1N5819 da 40 V lo sostituisce) | C | A |
| C4 | Cavetti verso la SSC-32 | 1 conf. | Dupont femmina 10–20 cm | TX, RX, massa, VL | Kamami: [Dupont F-F 10 cm, 40 pz](https://kamami.pl/przewody-f-f/584964-przewody-polaczeniowe-f-f-roznokolorowe-10-cm-40-szt-5906623461738.html), 1,13 € (V) | — | A |
| C5 | Prolunghe servo | 4 (confezione da 20) | JR maschio-femmina 15 cm, 22 AWG | dal CAD (`calc/cavi_servo.py`): i ginocchi delle zampe d'angolo hanno percorsi di 267–295 mm contro circa 300 utili (32 cm dichiarati), margine 2–11 %; gli altri 14 servo bastano con margine (23–77 %). Con 2,5 A una prolunga da 15 cm in 22 AWG perde circa 40 mV | Kamami: [prolunga JR 15 cm 22 AWG](https://kamami.pl/przewody-do-serw/586760-przedluzacz-do-serw-15cm-5906623462988.html), 4 × 1,34 € (V). Amazon.it B087289HFS, 20 pz circa 9 € (S) | S | A (approvato il 9 ottobre 2026) |
| C6 | Clip di blocco delle prolunghe | — | — | non servono: le 4 giunzioni si chiudono con il termorestringente (B19) | — | — | — |
| C7 | Prolunga di bilanciamento | 1 | JST-XH 3 poli, 10–20 cm | porta la presa di bilanciamento dove si raggiunge senza togliere il pacco | AliExpress circa 2,50 € (S): nei negozi UE leggibili non c'è una prolunga XH a 3 poli | S | ? (dopo il CAD) |
| C8 | Antenna esterna | 1 | 2,4 GHz con cavetto IPEX | solo se la portata a guscio montato non basta | Amazon.it | C | — |

## D. Giunti e meccanica

Ogni giunto: il servo è stretto in una culla e appoggia sulle alette; l'albero porta una squadretta metallica avvitata alla parte mobile; sul lato opposto, coassiale, un cuscinetto flangiato e un perno.

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Acquisto (10 ottobre 2026) | Dato | Stato |
|---|---|---|---|---|---|---|---|
| D1 | Cuscinetto del lato opposto all'albero | 18 + 6 | flangiato schermato **5 × 10 × 4** (NMB LF-1050ZZ, venduto come MF105ZZ) | flangia Ø11,6 × 0,8 nella versione NMB (nei generici da 11,2 a 11,7); carico statico 276 N, dinamico 714 N, contro poche decine di newton di lavoro. Ordinare "ZZ" | a tua cura. Riferimento: eBay.de [MF105ZZ, 10 pz](https://www.ebay.de/itm/317047658010) circa 8 € più circa 4 € di spedizione (S) | V (NMB) | A |
| D2 | Perno del cuscinetto | 18 + 6 | spina cilindrica **Ø5 × 12**, tolleranza h8 se si trova (ISO 2338), altrimenti m6 (ISO 8734); lunghezza fissata dal CAD della zampa (D-047) | le m6 entrano forzate nel cuscinetto: provarle su un cuscinetto campione | a tua cura. Riferimento: [SFS 331664](https://www.sfs.ch/CH/en/dl/p/331664), ISO 2338 5 h8 × 12 inox, 100 pz 13,90 CHF (S, Svizzera: dogana) | S, C | A |
| D3 | Squadretta lato albero | 18 + 2 | disco in alluminio per servo a **25 denti** con fori M3, dichiarato compatibile MG996R | sostituisce la squadretta di plastica: niente gioco e niente deformazione con 2,6 kg. I 25 denti dell'MG996R sono il dato comune dei servo di questa taglia: prima di ordinarne 20, provarne una su un tuo servo | AliExpress circa 1,25 € l'uno, 20 pz circa 25 € (S). Leggibile: [Botland GRL-12539](https://botland.store/servo-horns-hooks/12539-aluminum-servo-horn-35mm-6mm-5904422319540.html), 1,20 € (V, ma il negozio dice "solo clienti B2B registrati"); [AZ-Delivery](https://www.az-delivery.de/en/products/aluminium-25t-servoarm) 5 pz 6,39 €, esaurito | S, C | A |
| D4 | Inserti a caldo M3 | 94 | **dal kit dell'utente** (Temu, "brass insert nut + screw set" M2/M3, 800 pezzi): M3 × 5 × Ø4,2 e M3 × 6 × Ø4,2, 50 per misura (anche × 3 e × 4) | alette dei servo (72 tra lato coda e corpo), zampe, corpo, coperchi | già in possesso; i fori (`ins_m3_d`, oggi 4,2 per i CNC Kitchen Ø4,6) si tarano sul provino | S | in possesso |
| D5 | Inserti a caldo M2 | 28 | **dal kit dell'utente**: M2 × 3 × Ø3,2 (anche × 2, × 4, × 5), 50 per misura | regolatori, SSC-32, basetta, lame B dei femori (D-065) | già in possesso; foro `ins_m2_d` (oggi 3,4) da tarare sul provino | S | in possesso |
| D6 | Viti M3 | assortimento + 100 | testa cilindrica con esagono incassato (ISO 4762), inox A2, 6–25 mm; **in più 12 × M3 × 5** per le squadrette della coxa (D-049, approvate il 9 ottobre 2026) | alette dei servo, squadrette metalliche, zampe, corpo | Gedex: DIN 912 A2 [M3 × 5](https://www.gedex-shop.de/de/schrauben/INNENSECHKANT/Zylinderkopf-DIN-912/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2-635/) 50 pz 2,49 €, [M3 × 6](https://www.gedex-shop.de/de/schrauben/INNENSECHKANT/Zylinderkopf-DIN-912/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2-636/) 100 pz 3,67 €, [M3 × 8](https://www.gedex-shop.de/de/schrauben/INNENSECHKANT/Zylinderkopf-DIN-912/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2-637/) 100 + 50 pz 6,02 €, [M3 × 10](https://www.gedex-shop.de/de/schrauben/INNENSECHKANT/Zylinderkopf-DIN-912/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2-640/) 50 pz 2,99 €, [M3 × 16](https://www.gedex-shop.de/de/schrauben/INNENSECHKANT/Zylinderkopf-DIN-912/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2/DIN-912-M3-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2-642/) 50 pz 2,89 € (V) | — | A |
| D7 | Dadi e rondelle M3 | 50 + 100 | dadi esagonali DIN 934, rondelle DIN 125 | dove un inserto non entra | Gedex: [dadi DIN 934 A2 M3](https://www.gedex-shop.de/de/MUTTERN/Sechskantmuttern-FORM-B--NIEDRIG--MIT-FASE--DIN-5206/Sechskantmuttern-DIN-934/Sechskantmuttern-DIN-934-M3/) 100 pz 2,89 € (S: codice della confezione da ricontrollare), [rondelle DIN 125 A2 3,2 mm](https://www.gedex-shop.de/de/SCHEIBEN/Fluegelschrauben--geschmiedete--amerikanische-Form-5362/Unterlegscheiben-Form-A-ohne-Fase-Edelstahl-V2A-DIN-125/Unterlegscheiben-Form-A-ohne-Fase-Edelstahl-V2A-DIN-125-M2-5/) 100 pz 3,19 € (V; scegliere la variante 125-2-3-100) | — | A |
| D8 | Viti M2 e M2,5 | assortimento | ISO 4762 inox | regolatori (M2), SSC-32 (M2,5: i suoi fori sono circa 3,0 mm) | Gedex: [DIN 912 A2 M2 × 5](https://www.gedex-shop.de/de/schrauben/INNENSECHKANT/Zylinderkopf-DIN-912/DIN-912---ISO-4762-M2-Zylinderschrauben-mit-Innensechskant/DIN-912-M2-Innensechskantschrauben-mit-Zylinderkopf-Edelstahl-rostfrei-A2-613/) 50 pz 2,99 € (V). Le M2,5 non servono più: la SSC-32 va su M2 × 5 | — | A |
| D8b | Viti M2 × 6 a testa svasata piana | 12 + 4 | ISO 10642 (DIN 7991) inox, esagono incassato; testa Ø4,0 | lame B dei femori, a filo nelle svasature (D-065, al posto delle spine stampate) | AliExpress circa 3 € per 50 (S): Gedex non ha M2 svasate | — | **da approvare** |
| D9 | Piedini antiscivolo | 6 + 2 | stampati in TPU 95A oppure cappucci in silicone | scelta dopo una prova sui tuoi pavimenti | — | — | — |
| D10 | Fermo batteria | 1 | schiuma EVA adesiva 3–5 mm | le cinghie non servono più: lo sportello preme il pacco con due rebbi e la schiuma (D-051, approvato il 9 ottobre 2026) | Amazon.it circa 8 € (S) | — | A |
| D11 | Guaina e fascette | 2 m + 1 conf. | guaina spiralata 6–8 mm, fascette 2,5 mm (tra queste 6 corte nel blocco dei femori, 6 nei ponti e 1 per F1, D-055 e D-061) | fasci dei 3 cavi per zampa, ancoraggi ai giunti | fascette: Kamami [150 × 2,5 mm, 100 pz](https://kamami.pl/opaski-zaciskowe/1191270-vorel-73893-opaski-plastikowe-150x25-100szt-czarne--5906083738937.html), 0,60 € (V); guaina spiralata su Amazon.it, circa 7 € (S) | — | A |

## Viteria e inserti contati dal modello (fase 5, bozza del 9 ottobre 2026)

Conteggio fatto in Fusion sulle lavorazioni del modello (inserti, fori pilota, fori passanti) moltiplicate per il numero di copie di ogni parte, comprese le specchiature del corpo. Lunghezze delle viti dalla pila di ogni giunto. Comprende il fissaggio del coperchio (D-052).

| Dove | Cosa | Quantità |
|---|---|---|
| Alette dei 18 servo | M3 × 8 ISO 4762: lato coda in inserti, lato albero in fori pilota Ø2,5 (D-049) | 72 |
| Femore_A → squadrette di femore e ginocchio | M3 × 6 | 48 |
| Femore_A → blocco di Femore_B | M3 × 8 con 2 rondelle M3 DIN 125 di registro ciascuna | 24 viti, 48 rondelle |
| Ponte → anima della coxa | M3 × 10 | 12 |
| Squadretta di coxa (teste che fanno da spine, D-048) | **M3 × 5**, senza rondella (D-049, da approvare) | 12 |
| Viti centrali delle squadrette | in dotazione con le squadrette | 18 |
| Chiglia → base | M3 × 16 davanti (orecchie a tutta altezza), M3 × 8 dietro | 2 + 2 |
| Slitte dei regolatori → parete della baia | M3 × 8 | 2 |
| Regolatori → slitte | M2 × 5 in inserti M2 | 8 |
| SSC-32 → bugne del tetto | M2 × 5 in inserti M2 (testa Ø3,8 sui fori da 3,0) | 4 |
| Basetta → colonnine del vassoio | M2 × 5 in inserti M2 (D-053) | 4 |
| Vassoio → distanziali | M3 × 6 sui 4 distanziali M3 maschio-femmina da 5 mm (B18) | 4 |
| Coperchio → colonnine del tetto | M3 × 8 in inserti M3 (D-052) | 4 |
| Sportello della batteria → blocchetti della chiglia | M3 × 8 in inserti M3 (D-054) | 2 |
| Guscio della tibia → stinco | M3 × 10 in inserti M3 (D-061) | 6 |
| Lama B → Femore_B | M2 × 6 a testa svasata in inserti M2 (D-065) | 12 |
| **Totale viti** | M3 × 5: 12; M3 × 6: 52; M3 × 8: 106; M3 × 10: 18; M3 × 16: 2; M2 × 5: 16; M2 × 6 svasate: 12 | |
| **Inserti a caldo** | M3: 94 (30 nel corpo, nelle gondole e nella chiglia, 24 nelle coxe, 18 nelle tibie, 24 nei femori); M2: 28 | dentro le confezioni da 200 e 50 (D4, D5) |
| Fori pilota per viti M3 autofilettanti | 36 (alette lato albero dei 18 servo) | |

Le voci D6 (viti M3 in assortimento più 100) e D8 (M2) vanno ordinate con queste quantità: in particolare servono circa 106 M3 × 8 e 52 M3 × 6, più dei pezzi di un assortimento normale.

## E. Materiali di stampa

| # | Voce | Q.tà | Uso | Nota | Acquisto (10 ottobre 2026) | Stato |
|---|---|---|---|---|---|---|
| E1 | PETG-CF nero | 2 bobine da 1 kg | tutte le parti funzionali: corpo (base, chiglia, slitte, sportello della batteria), zampe (coxa, ponte, femori, tibie) | circa 860 g di pezzi (stima dal modello del 9 ottobre) più provini, supporti e scarti | 3DJake.it: [eSUN PETG-CF nero 1 kg](https://www.3djake.it/esun/petg-cf-black-3), 2 × 29,49 € (V; ugello 240–260 °C) | A (scelta dell'utente, 9 ottobre 2026) |
| E2 | PLA colorato (bianco per ora) | 1 bobina | placche: carapace, lame dei femori, gusci delle tibie; vassoio dell'ESP32 (sotto l'antenna niente carbonio) | circa 230 g; il colore può cambiare | 3DJake.it: [eSUN PLA Basic bianco 1 kg](https://www.3djake.it/esun/pla-basic-white), 12,69 € (V) | A (scelta dell'utente) |
| E2b | PLA nero (o un secondo colore) | 1 bobina piccola | fascia, visiera, gonne, sportellino: stampati insieme al carapace, PLA su PLA si attacca senza interlocking | circa 15 g | 3DJake.it: [eSUN PLA Basic nero 1 kg](https://www.3djake.it/esun/pla-basic-black-1), 12,69 € (V; non ci sono bobine più piccole) | proposta (D-065) |
| E3 | TPU 95A arancio | pochi grammi | piedini (D9) | circa 10 g | 3DJake.it: [3DJAKE TPU A95 arancio 750 g](https://www.3djake.it/3djake/tpu-a95-orange), 30,49 € (V; la confezione più piccola in arancio) | A (scelta dell'utente) |

## Attrezzi necessari

Saldatore con punta per inserti a caldo (o kit di punte dedicate), multimetro, pinza spelafili, termosoffiatore o accendino per il termorestringente, chiavi a brugola da 1,5 / 2 / 2,5 mm, calibro per controllare i pezzi stampati. Al banco, per le prime accensioni: un alimentatore regolabile con limite di corrente sarebbe utile ma non indispensabile (si parte con F1 da 15 A).

## X. Predisposizioni della versione 2.1.0 (candidati, da approvare)

Nel CAD della 2.1.0 (D-066) ci sono le sedi per queste voci; **niente è approvato né da comprare**. L'elenco completo, con fasi, masse, correnti e costi indicativi, è in `docs/piano-elettronica-software.md`, sezione 6. Dove il posto è nel modello:

| Voce | Posto nel modello (D-066) |
|---|---|
| X5 FSR 400 Short (6 + 1) | punta della tibia, piedino con pistoncino, tasca e gola dei fili, prese dei piedi accanto all'ADC |
| X4 IMU Pololu #2798 | bugne sul tetto del tunnel sotto il vassoio |
| X6 ADS7830 | bugne accanto all'IMU |
| X7 2 × INA260 | supporti sopra le slitte dei regolatori |
| X8 ToF VL53L7CX | mensola della camera, finestra nella visiera, tappo |
| X9, X11, X12, X31 luci (striscia WS2812B-2020 a 120 LED/m, D-068) | anello del pulsante con camera nera Ø32 × 6 e fondo con due sedi da 16,7 mm (2 pixel ciascuna); sedi dei lobi da 2 pixel; sedi nelle tibie con il fermo dei fili, diffusore. Cablaggio in `cablaggio.md` |
| X13 spie dei rail | linguette in coda |
| X2 scheda del carapace, X17 amplificatore e altoparlante, X16 microfoni, X19 ToF posteriore | bugne sotto il dorso, guide e piano sulle guance di coda, fori con anello |
| Computer a zaino (Radxa ZERO 3W) | quattro bugne M2 sopra l'ottagono, sportellino con la tacca dell'USB-C |

Prezzi delle voci X (10 ottobre 2026, IVA inclusa; facoltativi, niente è approvato). La striscia LED cambia in D-068: WS2812B-2020 a **120 LED/m**, larga 4 mm, perché la 2020 a 60 LED/m su 4–5 mm non è in commercio.

| Livello | Voce | Prodotto | Negozio | Costo |
|---|---|---|---|---|
| alte | X1 | cavi Qwiic Adafruit 4210 100 mm, 5 pz | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/4210/10230021) | 5,06 € (V) |
| alte | X1 | cavo Qwiic con prese femmina Adafruit 4397 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/4397/10824270) | 1,01 € (V) |
| alte | X3 | Pololu D24V5F3 #2842 | [Kamami](https://kamami.pl/en/step-down/558118-pololu-2842-pololu-33v-500ma-step-down-voltage-regulator-d24v5f3.html) | 7,76 € (V) |
| alte | X4 | Pololu LSM6DSO #2798 | [pololu.com](https://www.pololu.com/product/2798) | 22,40 € (S) |
| alte | X5 | Interlink FSR 400 Short 34-00004, 7 pz | [Tinytronics](https://www.tinytronics.nl/en/sensors/weight-pressure-force/membrane/interlink-electronics-fsr-400-short-tail-membrane-pressure-sensor-7.6mm-round-soldertabs) | 35,00 € (V) |
| alte | X5 | cavo siliconico 28 AWG, 2 colori, 4 m | AliExpress | 3,00 € (S) |
| alte | X5 | partitori: 10 kΩ 1 % × 6, 100 nF × 6 | [DigiKey.it](https://www.digikey.it/en/products/detail/yageo/MFR-25FRF52-10K/14626) | 1,36 € (V) |
| alte | X6 | Adafruit ADS7830 #5836 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/5836/21839818) | 6,37 € (V) |
| alte | X8 | Pololu VL53L7CX #3418 | [Kamami](https://kamami.pl/czujniki-odleglosci/1186902-vl53l7cx-time-of-flight-8-8-zone-wide-fov-distance-sensor-carrier-with-voltage-regulator-350cm-max-5906623469284.html) | 19,30 € (V) |
| alte | X9 | striscia WS2812B-2020 120 LED/m, FPC 4 mm, 1 m | [Superlighting](https://www.superlightingled.com/4mm-ws2812c-individually-addressable-rgb-led-strip-light-120ledsm-328ft1m-p-4003.html) | 12,32 € (S) |
| alte | X9 | SN74AHCT125N DIP-14, 330 Ω × 2, 10 kΩ × 2, PTC Bourns MF-R075 × 2 | [DigiKey.it](https://www.digikey.it/en/products/detail/texas-instruments/SN74AHCT125N/375798) | 2,38 € (V) |
| alte | X13 | LED 3 mm giallo Kingbright WP710A10SYD × 2, 1 kΩ × 2 | [DigiKey.it](https://www.digikey.it/en/products/detail/kingbright/WP710A10SYD/3084207) | 1,09 € (V) |
| medie | X2 | box header 2 × 8, 2 IDC 16 poli, cavo piatto 61 cm, 470 µF 10 V | [DigiKey.it](https://www.digikey.it/en/products/detail/w%C3%BCrth-elektronik/61201623021/2060599) | 5,26 € (V) |
| medie | X7 | Adafruit INA260 #4226, 2 pz | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/4226/10130492) | 21,32 € (V) |
| medie | X14 | NTC TDK B57861S0103F040, 3 pz | [Bürklin](https://buerklin.com/en/p/epcos/ntc-thermistors/b57861s0103f040/80E6746) | 11,32 € (S) |
| medie | X14 | 10 kΩ 1 % × 3 | [DigiKey.it](https://www.digikey.it/en/products/detail/yageo/MFR-25FRF52-10K/14626) | 0,14 € (V) |
| medie | X16 | Adafruit SPH0645 #3421, 2 pz | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/3421/6691114) | 14,88 € (V) |
| medie | X17 | Adafruit MAX98357A #3006 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/3006/6058477) | 6,37 € (V) |
| medie | X17 | altoparlante Same Sky CMS-15113-078SP-67 | [DigiKey.it](https://www.digikey.it/en/products/detail/same-sky-formerly-cui-devices/CMS-15113-078SP-67/9561103) | 3,21 € (V) |
| medie | X19 | Pololu VL53L1X #3415 | [Kamami](https://kamami.pl/en/distance-sensors/571453-distance-sensor-vl53l1x-4-400-cm-in-tof-technology-with-voltage-regulator.html) | 28,78 € (V) |
| medie | X20 | SparkFun Qwiic GPIO TCA9534 DEV-17047 (in arrivo il 24 novembre) | [DigiKey.it](https://www.digikey.it/en/products/detail/sparkfun-electronics/17047/13419022) | 7,23 € (V) |
| medie | X31 | cavo siliconico 30 AWG, 3 colori, 6 m | AliExpress | 4,00 € (S) |
| basse | X15 | Adafruit INA3221 #6062, 2 pz | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/6062/25660599) | 23,44 € (V) |
| basse | X18 | Adafruit CAP1188 #1602 e nastro di rame #3483 | [DigiKey.it](https://www.digikey.it/en/products/result?keywords=1528-1026-ND) | 13,83 € (V) |
| basse | X25 | Pololu VL53L4CD #3692 | [pololu.com](https://www.pololu.com/product/3692) | 15,65 € (S) |
| basse | X26 | Hi-Link HLK-LD2410C | [Electrokit](https://www.electrokit.com/en/ld2410c-human-presence-sensor-24ghz-radar) | 8,00 € (S) |
| basse | X27 | Adafruit APDS-9960 #3595 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/3595/7652603) | 8,04 € (V) |
| basse | X28 | LDROBOT LD06 | [eBay (UK)](https://www.ebay.de/itm/405260556470) | 14,91 € (S) |
| basse | X29 | Adafruit MLX90640 110° #4469 (in arrivo il 4 novembre) | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/4469/11497511) | 80,29 € (V) |
| basse | X32 | Adafruit ADS7830 #5836, 2 in più | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/5836/21839818) | 12,74 € (V) |
| basse | X33 | Adafruit seesaw ATtiny1616 #5690 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/5690/18627499) | 5,31 € (V) |
| basse | Radxa | Radxa ZERO 3W 4 GB / 32 GB eMMC | [RS Components](https://ie.rs-online.com/web/p/rock-sbc-boards/2564694) | 62,13 € (S) |
| basse | Reg 5 V | Pololu D36V28F5 #3782 (Botland: solo clienti B2B?) | [Botland](https://botland.store/converters-step-down/17169-step-down-voltage-converter-d36v28f5-5v-32a-pololu-3782-5903351242837.html) | 17,90 € (S) |
| basse | USB-seriale | modulo CH340N USB-C 3,3/5 V | [Kamami](https://kamami.pl/konwertery-usb---uart--rs232/1183592-modul-konwertera-usb-uart-na-usb-c-ch340n-5906623466696.html) | 1,71 € (V) |

| Insieme | Merce | Spedizioni | Totale |
|---|---|---|---|
| alte | 117,05 € | 59,86 € | 176,91 € |
| medie | 102,51 € | 37,69 € | 140,20 € |
| basse | 263,95 € | 57,50 € | 321,45 € |
| alte e medie | 219,56 € | 47,55 € | 267,11 € |
| tutte | 483,51 € | 85,05 € | 568,56 € |

- **Spedizioni**: quelle di pololu.com (circa 20 €), Electrokit, eBay, RS, Bürklin e Superlighting sono stime S. Superlighting e pololu.com spediscono da fuori UE, quindi possono esserci dogana e IVA all'importazione. DigiKey è gratuito sopra 75 €, altrimenti costa 25 €: con le sole alte non si arriva, con alte e medie si sta al limite (76 € IVA inclusa).
- **Da controllare**:
  - X13: a magazzino c'è solo il LED giallo a 590 nm, non ambra;
  - X17: l'altoparlante disponibile è la variante -67 (IP67), con le stesse misure;
  - X33: il seesaw attuale è l'ATtiny1616 (#5690);
  - X20 e X29: in arrivo a novembre;
  - X4 e X25: si trovano solo su pololu.com;
  - il regolatore da 5 V del computer di bordo: Botland dice di vendere solo a clienti B2B;
  - X28: c'è solo un'offerta eBay dal Regno Unito.

Viteria in più se si montano tutte, da contare a robot deciso: inserti M2 (D5) per IMU 2, ADC 2, INA260 4, scheda del carapace 4, amplificatore 2, zaino 4; viti M2 corte per le stesse; viti M3 delle slitte più lunghe di 2,4 mm con i supporti degli INA260.

## Ordine degli acquisti consigliato

1. **Una squadretta metallica** (D3), qualche cuscinetto e perno (D1, D2), inserti e viti M3: servono per il provino stampato della culla e del giunto, che conferma le quote del servo prima di tutto il resto.
2. Alimentazione (B1–B19) e controllo (C1–C4): per la prova al banco della SSC-32 con un lato di servo.
3. Il resto delle squadrette, cuscinetti e perni nella lunghezza decisa dal CAD.
4. Filamento quando si stampano le parti vere; prolunghe e prolunga di bilanciamento dopo il CAD.

## Carrelli e costo totale

Prezzi IVA inclusa del 10 ottobre 2026; V letto sulla pagina, S stimato. I prezzi in PLN di Kamami sono convertiti a 0,23 €/PLN: sul sito si può scegliere l'euro, e il totale può cambiare di qualche percento. Le spedizioni sono quelle lette sulle pagine dei negozi, salvo dove è scritto S.

### Voci approvate (B, C, D, E con stato A)

| Negozio | Voci | Merce | Spedizione in Italia | Totale |
|---|---|---|---|---|
| Kamami | B1, B2, B3, B3b, B4, B6, B9, B10, B11, B13, B19, C1, C2, C3, C4, C5, D11 | 176,82 € | 8,24 € (FedEx zona 1, 6,70 € + IVA; nessuna soglia gratuita per l'estero, S) | 185,06 € |
| 3DJake.it | E1, E2, E3 | 102,16 € | 0,00 € (gratis sopra 49,90 €, V) | 102,16 € |
| Gedex | D6, D7, D8 | 27,13 € | 25,90 € (forfait Italia, nessuna soglia, V) | 53,03 € |
| AliExpress | D3 | 25,00 € | 0,00 € (di solito compresa, S) | 25,00 € |
| Amazon.it | B5, B7, B8, B12, B14, B15, B16, B17, B18, C2, C3, D10, D11 | 121,00 € | 0,00 € (gratis sopra 29 €, S) | 121,00 € |
| **Totale** | | **452,11 €** | **34,14 €** | **486,25 €** |

- **Kamami** (Polonia, FedEx 3–7 giorni) porta in un solo pacco i regolatori Pololu e quasi tutta la minuteria: 20 righe con link e prezzo letto. Le predisposizioni Pololu (X3, X8, X19) si aggiungono senza altra spedizione.
- **Amazon.it**: 13 voci di minuteria e cavi (B5, B7, B8, B12, B14–B18, C2 strip femmina, C3 spinotto, D10, D11 guaina) che non sono su Kamami. Amazon non è leggibile dagli strumenti: i prezzi sono stime e i prodotti si scelgono all'ordine con le specifiche della tabella. Sopra 29 € la spedizione è gratuita.
- **Viti** (Gedex, Germania): le quantità esatte in inox A2 costano 27,13 €, ma la spedizione in Italia è 25,90 €. Un kit M3 su Amazon.it costa circa 15 € e farebbe risparmiare circa 30 €, se contiene almeno 106 viti M3 × 8 e 52 M3 × 6: va controllato all'ordine.
- **Squadrette** (D3): prima 1–2 pezzi di prova (BOM, domanda 4). Su AliExpress circa 1,25 € l'una; Botland le ha a 1,20 € ma il negozio dice di vendere solo a clienti B2B registrati: si prova a registrarsi da privato.
- **Con le voci X** conviene spostare B7 e B8 su DigiKey (9 € di merce): il carrello DigiKey supera i 75 € e la spedizione è gratuita.

Fuori dal totale:

| Voci | Stato | Negozio | Costo |
|---|---|---|---|
| D8b, M2 × 6 svasate ISO 10642 A2, 50 pz | da approvare / ? | AliExpress | 3,00 € (S) |
| E2b, eSUN PLA Basic nero 1 kg | da approvare / ? | [3DJake.it](https://www.3djake.it/esun/pla-basic-black-1) | 12,69 € (V) |
| C7, prolunga bilanciamento JST-XH 3 poli | da approvare / ? | AliExpress | 2,50 € (S) |
| D1, MF105ZZ 5 × 10 × 4, 30 pz | a tua cura | [eBay.de](https://www.ebay.de/itm/317047658010) | 28,00 € (S) |
| D2, spina ISO 2338 5 h8 × 12 inox A1, 100 pz | a tua cura | [SFS (CH)](https://www.sfs.ch/CH/en/dl/p/331664) | 14,90 € (S) |
| A1–A5, D4, D5 | già in possesso | — | 0 € |

Rispetto alla stima della versione 2.0 (circa 380 € di componenti più circa 100 € di filamento): **circa 486,25 €** consegnati. Il filamento costa 102 €; i regolatori costano 105 €, meno dei 110 € stimati.

## Aperto: serve una tua risposta

| # | Domanda | Cosa decide |
|---|---|---|
| 1 | ESP32-S3-CAM e camera OV3660: le hai già? (prima avevi detto di sì; ora hai scritto che hai comprato solo servo e SSC-32) | voci A2, A3 |
| 2 | Quanti MG996R hai? Ne servono 18; qualcuno di scorta aiuta | voce A1 |
| 3 | Hai già prolunghe servo, inserti, viteria, filamento o attrezzi dalla v1? | si tolgono dal BOM |
| 4 | Squadrette metalliche: va bene comprarne una per prova prima delle altre 19? | voce D3 |
| 5 | Pulsante d'accensione | **Risposto il 9 ottobre 2026**: pulsante da pannello Ø12 sul coperchio, voce B3b |
| 6 | Cicalino di sottotensione | **Risposto il 9 ottobre 2026**: (c), sotto il coperchio in coda sopra il T-plug, display da una finestra del dorso, spinotto di bilanciamento dal retro; serve un modello con i pin sul lato lungo (da scegliere all'ordine) | voci B9, C7, coperchio |
| 7 | Filamenti e colori della passata estetica | **Risposto il 9 ottobre 2026**: PETG-CF nero per le parti funzionali, PLA colorato (bianco per ora) per le placche, TPU arancio per i piedini; proposto PLA nero per fascia, visiera, gonne e sportellino | voci E1, E2, E2b, E3 |
| 8 | Inserti in ottone del kit Temu | **Risposto il 9 ottobre 2026** (foto del kit): M3 Ø4,2 lunghi 3/4/5/6, M2 Ø3,2 lunghi 2/3/4/5, 50 per misura, più viti a testa tonda con impronta a croce (M2 × 5/6/8, M3 × 6/8/10/12). Si usano gli inserti; le viti del kit solo dove la testa non conta. Fori da tarare sul provino | voci D4, D5, fori `ins_m3_*`, `ins_m2_*` |
