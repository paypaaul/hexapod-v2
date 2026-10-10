# BOM — Hexapod v2 (MG996R)

Versione 2.1 (10 ottobre 2026): prezzi e link d'acquisto letti il 10 ottobre 2026, carrelli per negozio e costo totale. Versione 2.0 (8 ottobre 2026) **approvata dall'utente** l'8 ottobre 2026. Le domande in fondo restano aperte: non bloccano il CAD. Nasce dallo studio in `studio-componenti.md`; il perché delle scelte è lì e in `decisioni.md` (D-043, D-045).
La viteria è provvisoria: misure, lunghezze e quantità esatte si ricavano dal modello nella fase 5.

Foto: immagini dei prodotti scelti, collegate dai siti dei negozi e dei produttori (non copiate nella repo: se un negozio cambia pagina, la foto può sparire).
Legenda **dato**: V = verificato su fonte primaria; S = stimato o da fonte secondaria; C = da confermare sul pezzo reale.
Legenda **stato**: P = già in tuo possesso; A = da comprare; ? = dimmi tu; — = non comprare per ora.
Prezzi in euro **IVA inclusa**, letti il 10 ottobre 2026 sulle pagine dei negozi (V) oppure stimati (S: conversione da PLN, SEK, USD o pagina non leggibile). I prezzi di Amazon.it e AliExpress sono letti nelle pagine aperte in Chrome sul Mac dell'utente. Si ricontrollano all'ordine. Criterio di scelta (D-068): il costo consegnato in Italia, spedizioni comprese, con pochi negozi; AliExpress solo per la minuteria, con l'alternativa europea. Il carrello per negozio e il totale sono nella sezione "Carrelli e costo totale".

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

| # | Foto | Componente | Q.tà | Modello / codice | Specifiche chiave | Dato | Stato |
|---|---|---|---|---|---|---|---|
| A1 | <img src="https://www.az-delivery.de/cdn/shop/products/mg996r-micro-digital-servo-motor-mit-metall-getriebe-fur-rc-roboter-hubschrauber-flugzeug-685347.jpg?v=1679399000&width=600" width="56" alt="A1"> | Servo | 18 | AZDelivery MG996R (confezioni da 5) | 55 g; 9,4 kgf·cm a 4,8 V, 11 a 6 V; 4,8–7,2 V; 2,5 A di stallo a 6 V; 40,7 × 19,7 × 42,9 mm; due cuscinetti; squadrette di plastica e viteria incluse | V (datasheet AZDelivery) | P |
| A2 | <img src="https://ae-pic-a1.aliexpress-media.com/kf/S2ac3791edb03436686088fd09a91655cg.png" width="56" alt="A2"> | Scheda di controllo | 1 | UICPAL "ESP32-S3-CAM N16R8 RE1.3" | ESP32-S3 N16R8; 62,6 × 28,3 mm (67,5 con l'antenna); 2 USB-C; nessun foro di fissaggio | S, C | P (da confermare) |
| A3 | <img src="https://ae-pic-a1.aliexpress-media.com/kf/S4006fe28243b4d18a771a8af8e3902a0s.jpg" width="56" alt="A3"> | Camera | 1 | UICPAL "OV3660-75MM", lente 120° "GOOD" | flat da 75 mm; testa 8,5 × 8,5 mm, alta circa 6 mm | S, C | P (da confermare) |
| A4 | <img src="https://ae-pic-a1.aliexpress-media.com/kf/Sda62dddbc24e4e4792b56deb2b49172ds.jpg" width="56" alt="A4"> | Servo controller | 1 | clone "SSC32-V2.5" (AliExpress 1005001888185034) | 32 canali; PCB 72 × 55 mm, fori a 65,5 × 48,5 mm; header a foro passante; VL 6–12 V | S (disegno del venditore) | P |
| A5 | <img src="https://m.media-amazon.com/images/I/71l0wPa2o9L._AC_UL320_.jpg" width="56" alt="A5"> | Batteria | 1 | OVONIC 2S 5200 mAh 50C hardcase, T-plug | 137–139 × 46–47 × 24–25 mm; 245–259 g; 260 A continui; cavi 12 AWG; bilanciamento JST-XH. Autonomia stimata 22–27 minuti in marcia classica | V (pagine del produttore) | P |

## B. Alimentazione

| # | Foto | Componente | Q.tà | Modello / codice | Specifiche chiave | Acquisto (10 ottobre 2026) | Dato | Stato |
|---|---|---|---|---|---|---|---|---|
| B1 | <img src="https://kamami.pl/124942-large_default/6v-11a-step-down-voltage-regulator-d42v110f6.jpg" width="56" alt="B1"> | Regolatore del rail servo, 6,0 V | 2 (uno per lato) | **Pololu D42V110F6 (#5673)** | ingresso fino a 60 V; 11 A tipici dichiarati a 42 V, di più con ingresso basso (circa 13–14 A con la 2S: S); limita la corrente con gradualità; pin di abilitazione e power-good; protezione da inversione; 43,2 × 31,8 × 9 mm; 4 fori M2. Se al banco non basta, al suo posto va il D24V150F6 (#2882), stesso ingombro | Kamami: [D42V110F6](https://kamami.pl/step-down/1201579-6v-11a-step-down-voltage-regulator-d42v110f6-5902186330856.html), 2 × 52,38 € (V, gli ultimi 2 a magazzino). pololu.com 59,95 US$ più IVA e spedizione | V | A |
| B2 | <img src="https://kamami.pl/25991-large_default/pololu-5v-25a-step-down-voltage-regulator-d24v22f5-pololu-2858.jpg" width="56" alt="B2"> | Regolatore 5 V per l'ESP32 | 1 | Pololu D24V22F5 (#2858) | 5 V, 2,5 A; 17,8 × 17,8 mm; 2 fori M2 | Kamami: [D24V22F5](https://kamami.pl/en/step-down/561020-pololu-5v-25a-step-down-voltage-regulator-d24v22f5-pololu-2858-5906623437580.html), 17,84 € (V) | V | A |
| B3 | <img src="https://kamami.pl/26087-large_default/pololu-2813-big-pushbutton-power-switch-with-reverse-voltage-protection-hp.jpg" width="56" alt="B3"> | Interruttore generale (ramo logica) | 1 | Pololu Big Pushbutton Power Switch HP (#2813) | a pulsante; pin OFF per lo spegnimento da firmware; meno di 0,2 µA da spento; 20,3 × 25,4 mm | Kamami: [Pololu 2813](https://kamami.pl/en/digital-switches/561034-pololu-2813-big-pushbutton-power-switch-with-reverse-voltage-protection-hp-5906623477883.html), 7,87 € (V) | V | A |
| B3b | <img src="https://kamami.pl/39512-large_default/momentary-push-button-okragly-przycisk-chwilowy-12mm-zolty.jpg" width="56" alt="B3b"> | Pulsante d'accensione | 1 + 1 | pulsante da pannello Ø12 mm, momentaneo, normalmente aperto, a vite con dado, contatti a saldare | sul coperchio, collegato ai pin A e B della 2813 (in parallelo al suo pulsantino, come indica la pagina Pololu); corpo sotto il pannello circa 20 mm, da confermare sul modello scelto | Kamami: [pulsante 12 mm con dado](https://kamami.pl/przyciski/582435-momentary-push-button-okragly-przycisk-chwilowy-12mm-zolty-5906623460052.html), 2 × 0,58 € (V; giallo, alto 21 mm, NO o NC non dichiarato: C) | S | A (approvato il 9 ottobre 2026) |
| B4 | <img src="https://kamami.pl/130281-large_default/zestaw-bezpiecznikow-ministandard-301szt-yt-83148.jpg" width="56" alt="B4"> | Fusibile principale F1 | assortimento 15 / 20 / 25 / 30 A | lama ATO/ATC, 32 V | 30 A in uso; 15 A per le prime accensioni | Kamami: [set Yato YT-83148](https://kamami.pl/bezpieczniki/1204000-zestaw-bezpiecznikow-ministandard-301szt-yt-83148-5906083091049.html), 301 fusibili ATO e MINI da 2 a 40 A, 7,73 € (V); copre anche i MINI da 2 A di B6 e i 3 e 5 A del banco | S | A |
| B5 | <img src="https://m.media-amazon.com/images/I/71BysLWCWWL._AC_UL320_.jpg" width="56" alt="B5"> | Portafusibile principale | 1 | in linea per lame ATO/ATC, cavi 12 AWG, con coperchio | da fissare al corpo, non appeso ai cavi | Amazon.it: [Gebildet, 4 portafusibili ATO 12 AWG con tappo](https://www.amazon.it/dp/B0BCW47SDY), 8,99 € (V, letto in Chrome) | S | A |
| B6 | <img src="https://kamami.pl/114050-large_default/gniazdo-bezpiecznika-10-mini.jpg" width="56" alt="B6"> | Fusibile del ramo logica F2 | 1 + 1 | portafusibile in linea MINI 18 AWG + fusibile MINI 2 A | il ramo logica usa cavo da 22 AWG: F1 da solo non lo proteggerebbe | Kamami: [portafusibile MINI con cavo 1 mm²](https://kamami.pl/zlacza-inne/1197193-gniazdo-bezpiecznika-10-mini-5900804107170.html), 0,92 € (V); fusibili da 2 A nel set di B4 | S | A |
| B7 | <img src="https://m.media-amazon.com/images/I/71CjacfDkOL._AC_UL320_.jpg" width="56" alt="B7"> | Condensatore sul rail servo | 2 + 2 | elettrolitico 2200 µF 16 V a bassa ESR, es. Panasonic EEUFR1C222 | Ø12,5 × 20 mm; saldato a una spina servo e inserito in un canale libero, uno per lato | Amazon.it: [2200 µF 16 V low ESR 13 × 21, 20 pz](https://www.amazon.it/dp/B0FH27HTJL), 15,00 € (V). Con le voci X: DigiKey [EEU-FR1C222](https://www.digikey.it/en/products/detail/panasonic-electronic-components/EEU-FR1C222/2433536), 4 × 1,79 € (**alto fino a 22 mm**, non 20) | S | A |
| B8 | <img src="https://m.media-amazon.com/images/I/71odu8D-OeL._AC_UL320_.jpg" width="56" alt="B8"> | Condensatore ceramico | 3 | 100 nF 50 V | due in parallelo a B7, uno sull'ingresso dell'ADC | Amazon.it: [BOJACK 100 nF 50 V](https://www.amazon.it/dp/B07Y7PHY91), 8,99 € (V). Con le voci X: DigiKey, 0,18 € l'uno | S | A |
| B9 | <img src="https://kamami.pl/110893-large_default/bx100-tester-napiecia-pakietow-lipo-1-8s.jpg" width="56" alt="B9"> | Allarme di sottotensione | 1 | cicalino LiPo 1–8S tipo "BX100" | sulla presa di bilanciamento; soglia regolabile; assorbe sempre: si stacca a fine uso | Kamami: [BX100](https://kamami.pl/wskazniki-rozladowania/582354-bx100-tester-napiecia-pakietow-lipo-1-8s-5906623459704.html), 3,50 € (V); posizione dei pin da guardare sul pezzo | S | A |
| B10 | <img src="https://kamami.pl/121245-large_default/zestaw-rezystorow-cf-tht-14w-1-1-1-m-820-szt-.jpg" width="56" alt="B10"> | Partitore per la misura di batteria | 1 + 1 | resistenze 100 kΩ e 47 kΩ, 1 % | 8,4 V → 2,69 V su GPIO1 | Kamami: [set resistenze 1 % da 820 pezzi](https://kamami.pl/rezystory-tht-14w/1199442-zestaw-rezystorow-cf-tht-14w-1-1-1-m-820-szt--5902186309630.html), 6,12 € (V): 100 k e 47 k; serve anche per B11 e per le voci X | V (campo ADC) | A |
| B11 | <img src="https://kamami.pl/86574-large_default/dioda-impulsowa-1n4148-tht-500mw-75v-10-szt.jpg" width="56" alt="B11"> | Accensione del rail servo | 1 + 1 | resistenza 47 kΩ (più una da 22 kΩ di riserva) e diodo 1N4148 | pin di abilitazione dei due B1 uniti e tirati a massa; GPIO42 → diodo → abilitazione. La soglia bassa non è pubblicata: valori da provare al banco | Kamami: [1N4148, 10 pz](https://kamami.pl/diody-schottky/1187768-dioda-impulsowa-1n4148-tht-500mw-75v-10-szt-5906623484720.html), 0,58 € (V); 47 k dal set di B10; il 22 k di riserva c'è solo al 5 % (0,01 €) | S, C | A |
| B12 | <img src="https://m.media-amazon.com/images/I/61CK0oMtFUL._AC_UL320_.jpg" width="56" alt="B12"> | Connettore batteria lato robot | 1 conf. | T-plug maschio con codino **12 AWG** | la batteria ha la femmina (dalle immagini del produttore: da guardare sul pacco) | Amazon.it: [Deans T-plug con cavo 12 AWG, 3 coppie](https://www.amazon.it/dp/B07QM1WS2J), 10,99 € (V, 924 recensioni) | S, C | A |
| B13 | <img src="https://kamami.pl/85881-large_default/wago-221-415-zlaczka-instalacyjna-5-przewodow-4mm.jpg" width="56" alt="B13"> | Derivazioni di potenza | 2 | morsetto a leva a 5 vie Wago 221-415 | fino a 4 mm², 32 A: uno per il positivo, uno per il negativo (massa a stella) | Kamami: [Wago 221-415](https://kamami.pl/szybkozlacza/1188363-wago-221-415-zlaczka-instalacyjna-5-przewodow-4mm-5902186324558.html), 2 × 0,81 € (V) | S | A |
| B14 | <img src="https://m.media-amazon.com/images/I/71P4sUoZI-L._AC_UL320_.jpg" width="56" alt="B14"> | Cavo di potenza principale | 0,5 m rosso + 0,5 m nero | siliconico 12 AWG | T-plug → F1 → derivazioni | Amazon.it: [MMOBIEL siliconico 12 AWG rosso e nero](https://www.amazon.it/dp/B0CRVK6Q9C), 14,99 € (V) | S | A |
| B15 | <img src="https://m.media-amazon.com/images/I/61wQ+Fle1EL._AC_UL320_.jpg" width="56" alt="B15"> | Cavi verso i regolatori e la SSC-32 | 0,5 m + 0,5 m di 14 AWG; 0,6 m + 0,6 m di 16 AWG | siliconico | 14 AWG dalle derivazioni agli ingressi dei B1; 16 AWG dalle uscite dei B1 alle file della SSC-32 | Amazon.it: [TUOFENG 14 AWG 1,5 + 1,5 m](https://www.amazon.it/dp/B075M578PB) 9,99 € e [MMOBIEL 16 AWG](https://www.amazon.it/dp/B0CRVMJQJF) 11,99 € (V) | S | A |
| B16 | <img src="https://m.media-amazon.com/images/I/618EHV5B7xL._AC_UL320_.jpg" width="56" alt="B16"> | Barre sulle file degli header | 1 m | filo di rame stagnato rigido Ø1 mm (18 AWG) | saldato sul retro della SSC-32 lungo le file VS e di massa di ogni lato | Amazon.it: [QWORK filo di rame Ø1 mm, 10 m](https://www.amazon.it/dp/B0F6XSTY6Z), 8,34 € (V; rame nudo, si stagna) | — | A |
| B17 | <img src="https://m.media-amazon.com/images/I/61wP1oUDwLL._AC_UL320_.jpg" width="56" alt="B17"> | Cavo logica | circa 2 m | siliconico 22 AWG, più colori | ramo logica, VL, 5 V, partitore, abilitazione | Amazon.it: [siliconico 22 AWG, 6 colori × 10 m](https://www.amazon.it/dp/B0F892PSQK), 15,99 € (V) | S | A |
| B18 | <img src="https://m.media-amazon.com/images/I/61Tnnu1r+hL._AC_UL320_.jpg" width="56" alt="B18"> | Distanziali | 4 | **M3 maschio-femmina da 5 mm** per il vassoio dell'ESP32 (D-051, approvato il 9 ottobre 2026; i regolatori stanno su slitte stampate e la SSC-32 su bugne del corpo) | | Amazon.it: [QUARKZMAN M3 × 5 + 5 maschio-femmina, 12 pz](https://www.amazon.it/dp/B0GGLL9HKK), 9,99 € (V) | — | A |
| B19 | <img src="https://kamami.pl/107093-large_default/cyna-lc60-070mm-100g.jpg" width="56" alt="B19"> | Termorestringente, stagno, flussante | 1 assortimento | — | giunzioni saldate | Kamami: [guaina 4/2 mm 10 × 1 m](https://kamami.pl/rurki-termokurczliwe/569152-rurki-termokurczliwe-czarne-4020-10-szt-x-1-metr-5900804072157.html) 2,99 €, [stagno 0,7 mm 100 g](https://kamami.pl/cyna-olowiowa/549284-cyna-lc60-070mm-100g-5906623404964.html) 7,47 €, [flussante 50 ml](https://kamami.pl/topnik-w-plynie/547791-topnik-tk-83-50ml-oliwiarka-ag-5901764323600.html) 1,98 € (V) | — | A |

Nota su B1: un regolatore serve 9 servo. Corrente stimata per lato: 5–6 A medi nella marcia classica, 8–9 A in quella bassa, picchi di 12–15 A, contro circa 13 A disponibili; oltre, il regolatore limita la corrente e il rail cala, senza spegnersi. Lo stallo contemporaneo di 9 servo (22,5 A) lo impedisce il firmware.

## C. Controllo, segnali, cablaggio dei servo

| # | Foto | Componente | Q.tà | Modello / codice | Specifiche chiave | Acquisto (10 ottobre 2026) | Dato | Stato |
|---|---|---|---|---|---|---|---|---|
| C1 | <img src="https://kamami.pl/113098-large_default/kamod-level-shift-x4-dwukierunkowy-4-kanalowy-konwerter-poziomow-logicznych.jpg" width="56" alt="C1"> | Traslatore di livello 3,3 V ↔ 5 V | 1 | modulo a 4 canali con BSS138 (tipo Adafruit 757) | TX e RX tra ESP32 e SSC-32 | Kamami: [KAmod Level Shift x4](https://kamami.pl/konwertery-napiec/1195428-kamod-level-shift-x4-dwukierunkowy-4-kanalowy-konwerter-poziomow-logicznych-5906623499489.html), 2,51 € (V; il MOSFET non è dichiarato, C). Adafruit 757 vero: [DigiKey](https://www.digikey.it/en/products/detail/adafruit-industries-llc/757/4990756), 4,23 € | S | A |
| C2 | <img src="https://kamami.pl/136652-large_default/kamod-proto-50x70-dwustronna-plytka-uniwersalna-50-x-70-mm.jpg" width="56" alt="C2"> | Basetta di supporto | 1 + 2 + 1 | millefori 50 × 70 mm; 2 strip femmina 1 × 20; 1 strip maschio 1 × 40 | zoccolo per l'ESP32 (che non ha fori) e supporto per B2, C1, B10, B11; si taglia a 56 × 35 (D-053) | Kamami: [millefori 50 × 70](https://kamami.pl/plytki-uniwersalne/1204291-kamod-proto-50x70-dwustronna-plytka-uniwersalna-50-x-70-mm-5902186339903.html) 1,82 € e [strip maschio 1 × 40](https://kamami.pl/zlacza-goldpin/1207864-goldpin-czarny-1x40-szpil-prosty-do-druku-raster-254mm-5906623439881.html) 0,43 € (V); strip femmina: Amazon.it [Ticfox 1 × 40, 5 pz](https://www.amazon.it/dp/B09JP7HT1W), 8,39 € (V) | C | A |
| C3 | <img src="https://m.media-amazon.com/images/I/610vs1ksn-L._AC_UL320_.jpg" width="56" alt="C3"> | Ingresso del 5 V nell'ESP32: alternativa | 1 + 1 | spinotto USB-C maschio a 90° a saldare + diodo Schottky 1N5817 | solo se la scheda non si accende dal pin 5V | spinotto: Amazon.it [USB-C maschio a 90° con 2 fili, 5 pz](https://www.amazon.it/dp/B0D2TN7M5B), 8,98 € (V). Diodo: Kamami [1N5819](https://kamami.pl/diody-schottky/1187767-dioda-schottkiego-1n5819-tht-40v-1a-10-szt-5906623484713.html), 0,46 € per 10 (V; il 1N5817 non c'è, il 1N5819 da 40 V lo sostituisce) | C | A |
| C4 | <img src="https://kamami.pl/42466-large_default/przewody-polaczeniowe-f-f-roznokolorowe-10-cm-40-szt.jpg" width="56" alt="C4"> | Cavetti verso la SSC-32 | 1 conf. | Dupont femmina 10–20 cm | TX, RX, massa, VL | Kamami: [Dupont F-F 10 cm, 40 pz](https://kamami.pl/przewody-f-f/584964-przewody-polaczeniowe-f-f-roznokolorowe-10-cm-40-szt-5906623461738.html), 1,13 € (V) | — | A |
| C5 | <img src="https://kamami.pl/43784-large_default/przedluzacz-do-serw-15cm.jpg" width="56" alt="C5"> | Prolunghe servo | 4 (confezione da 20) | JR maschio-femmina 15 cm, 22 AWG | dal CAD (`calc/cavi_servo.py`): i ginocchi delle zampe d'angolo hanno percorsi di 267–295 mm contro circa 300 utili (32 cm dichiarati), margine 2–11 %; gli altri 14 servo bastano con margine (23–77 %). Con 2,5 A una prolunga da 15 cm in 22 AWG perde circa 40 mV | Kamami: [prolunga JR 15 cm 22 AWG](https://kamami.pl/przewody-do-serw/586760-przedluzacz-do-serw-15cm-5906623462988.html), 4 × 1,34 € (V). Amazon.it B087289HFS, 20 pz circa 9 € (S) | S | A (approvato il 9 ottobre 2026) |
| C6 | — | Clip di blocco delle prolunghe | — | — | non servono: le 4 giunzioni si chiudono con il termorestringente (B19) | — | — | — |
| C7 | <img src="https://ae-pic-a1.aliexpress-media.com/kf/Se49e7214ca17467cae9596d8df4ab098V.jpg" width="56" alt="C7"> | Prolunga di bilanciamento | 1 | JST-XH 3 poli, 10–20 cm | porta la presa di bilanciamento dove si raggiunge senza togliere il pacco | AliExpress: [JST-XH 2S 20 cm 22 AWG, 5 pz](https://it.aliexpress.com/item/1005004996032030.html), 2,32 € (V). Amazon.it [YIXISI 2S, 10 pz](https://www.amazon.it/dp/B08JV8QW3M), 8,99 € | S | ? (dopo il CAD) |
| C8 | — | Antenna esterna | 1 | 2,4 GHz con cavetto IPEX | solo se la portata a guscio montato non basta | Amazon.it | C | — |

## D. Giunti e meccanica

Ogni giunto: il servo è stretto in una culla e appoggia sulle alette; l'albero porta una squadretta metallica avvitata alla parte mobile; sul lato opposto, coassiale, un cuscinetto flangiato e un perno.

| # | Foto | Componente | Q.tà | Modello / codice | Specifiche chiave | Acquisto (10 ottobre 2026) | Dato | Stato |
|---|---|---|---|---|---|---|---|---|
| D1 | <img src="https://m.media-amazon.com/images/I/81-Dhjx3LXL._AC_UL320_.jpg" width="56" alt="D1"> | Cuscinetto del lato opposto all'albero | 18 + 6 | flangiato schermato **5 × 10 × 4** (NMB LF-1050ZZ, venduto come MF105ZZ) | flangia Ø11,6 × 0,8 nella versione NMB (nei generici da 11,2 a 11,7); carico statico 276 N, dinamico 714 N, contro poche decine di newton di lavoro. Ordinare "ZZ" | a tua cura. Riferimento: Amazon.it [METERXITY MF105ZZ 20 pz](https://www.amazon.it/dp/B0F4QWY4XZ) 19,90 € + [4 pz](https://www.amazon.it/dp/B0F4QWG4YM) 10,72 € (V) | V (NMB) | A |
| D2 | <img src="https://m.media-amazon.com/images/I/71IQ-4VR6oL._AC_UL320_.jpg" width="56" alt="D2"> | Perno del cuscinetto | 18 + 6 | spina cilindrica **Ø5 × 12**, tolleranza h8 se si trova (ISO 2338), altrimenti m6 (ISO 8734); lunghezza fissata dal CAD della zampa (D-047) | le m6 entrano forzate nel cuscinetto: provarle su un cuscinetto campione | a tua cura. Riferimento: Amazon.it [QUARKZMAN 5 × 12 inox 316L, 40 pz](https://www.amazon.it/dp/B0FGJKXFY3), 11,69 € (V; tolleranza non dichiarata) | S, C | A |
| D3 | <img src="https://ae-pic-a1.aliexpress-media.com/kf/Hac9e2a1e322f42549b298aedf74f01f6S.jpg" width="56" alt="D3"> | Squadretta lato albero | 18 + 2 | disco in alluminio per servo a **25 denti** con fori M3, dichiarato compatibile MG996R | sostituisce la squadretta di plastica: niente gioco e niente deformazione con 2,6 kg. I 25 denti dell'MG996R sono il dato comune dei servo di questa taglia: prima di ordinarne 20, provarne una su un tuo servo | AliExpress: [disco 25T per MG995/MG996](https://it.aliexpress.com/item/1005002538112794.html), 0,42 € l'uno, 24 pz 10,08 € (V; diametro e fori non dichiarati: si provano 1–2 pezzi). Con le misure del CAD (Ø20, fori M3 filettati a 14 mm): Amazon.it [diymore 25T, 6 pz](https://www.amazon.it/dp/B07G5BTMJB), 10,99 € (V) | S, C | A |
| D4 | — | Inserti a caldo M3 | 94 | **dal kit dell'utente** (Temu, "brass insert nut + screw set" M2/M3, 800 pezzi): M3 × 5 × Ø4,2 e M3 × 6 × Ø4,2, 50 per misura (anche × 3 e × 4) | alette dei servo (72 tra lato coda e corpo), zampe, corpo, coperchi | già in possesso; i fori (`ins_m3_d`, oggi 4,2 per i CNC Kitchen Ø4,6) si tarano sul provino | S | in possesso |
| D5 | — | Inserti a caldo M2 | 28 | **dal kit dell'utente**: M2 × 3 × Ø3,2 (anche × 2, × 4, × 5), 50 per misura | regolatori, SSC-32, basetta, lame B dei femori (D-065) | già in possesso; foro `ins_m2_d` (oggi 3,4) da tarare sul provino | S | in possesso |
| D6 | <img src="https://m.media-amazon.com/images/I/81+LkLd7rkL._SX522_.jpg" width="56" alt="D6"> | Viti M3 | assortimento + 100 | testa cilindrica con esagono incassato (ISO 4762), inox A2, 6–25 mm; **in più 12 × M3 × 5** per le squadrette della coxa (D-049, approvate il 9 ottobre 2026) | alette dei servo, squadrette metalliche, zampe, corpo | Amazon.it: [kit inox M3 da 1320 pz](https://www.amazon.it/dp/B0DZWR53CD) 14,99 € (M3 × 5: 50, × 6: 40, × 8: 40, × 10: 30, × 16: 30; 330 dadi e 330 rondelle), più [M3 × 8 ISO 4762, 100 pz](https://www.amazon.it/dp/B07MCL1LGW) 8,73 € e [M3 × 6 DIN 912 A2, 50 pz](https://www.amazon.it/dp/B0GG6G2RJV) 8,88 € (V). Insieme: M3 × 8 140, M3 × 6 90. Alternativa con le misure esatte: Gedex 27,13 € + 25,90 € di spedizione | — | A |
| D7 | <img src="https://m.media-amazon.com/images/I/81+LkLd7rkL._SX522_.jpg" width="56" alt="D7"> | Dadi e rondelle M3 | 50 + 100 | dadi esagonali DIN 934, rondelle DIN 125 | dove un inserto non entra | nel kit di D6: 330 dadi M3 e 330 rondelle M3 | — | A |
| D8 | <img src="https://m.media-amazon.com/images/I/41VT7NqHlOL._AC_UL320_.jpg" width="56" alt="D8"> | Viti M2 e M2,5 | assortimento | ISO 4762 inox | regolatori (M2), SSC-32 (M2,5: i suoi fori sono circa 3,0 mm) | Amazon.it: [SECCARO M2 × 5 DIN 912 A2, 20 pz](https://www.amazon.it/dp/B0D92Q2KYY), 9,43 € (V) | — | A |
| D8b | <img src="https://ae-pic-a1.aliexpress-media.com/kf/S2e04d5aab94e41f188e15e029ba305c2E.jpg" width="56" alt="D8b"> | Viti M2 × 6 a testa svasata piana | 12 + 4 | ISO 10642 (DIN 7991) inox, esagono incassato; testa Ø4,0 | lame B dei femori, a filo nelle svasature (D-065, al posto delle spine stampate) | AliExpress: [M2 × 6 DIN 7991 inox 304, 50 pz](https://it.aliexpress.com/item/33028389667.html), 1,85 € (V) | — | **da approvare** |
| D9 | — | Piedini antiscivolo | 6 + 2 | stampati in TPU 95A oppure cappucci in silicone | scelta dopo una prova sui tuoi pavimenti | — | — | — |
| D10 | <img src="https://m.media-amazon.com/images/I/71ifR7eRwXL._AC_UL320_.jpg" width="56" alt="D10"> | Fermo batteria | 1 | schiuma EVA adesiva 3–5 mm | le cinghie non servono più: lo sportello preme il pacco con due rebbi e la schiuma (D-051, approvato il 9 ottobre 2026) | Amazon.it: [fogli EVA adesivi 3 mm, 6 pz](https://www.amazon.it/dp/B0DG96T98Z), 12,99 € (V) | — | A |
| D11 | <img src="https://m.media-amazon.com/images/I/61gbdADnIVL._AC_UL320_.jpg" width="56" alt="D11"> | Guaina e fascette | 2 m + 1 conf. | guaina spiralata 6–8 mm, fascette 2,5 mm (tra queste 6 corte nel blocco dei femori, 6 nei ponti e 1 per F1, D-055 e D-061) | fasci dei 3 cavi per zampa, ancoraggi ai giunti | fascette: Kamami [150 × 2,5 mm, 100 pz](https://kamami.pl/opaski-zaciskowe/1191270-vorel-73893-opaski-plastikowe-150x25-100szt-czarne--5906083738937.html), 0,60 € (V); guaina: Amazon.it [GTIWUNG spiralata 6 mm](https://www.amazon.it/dp/B07WDRYFXV), 10,99 € (V) | — | A |

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

| # | Foto | Voce | Q.tà | Uso | Nota | Acquisto (10 ottobre 2026) | Stato |
|---|---|---|---|---|---|---|---|
| E1 | <img src="https://3d.nice-cdn.com/upload/image/product/large/default/esun-epetg-cf-black-175-mm-1000-g-831502-it.jpg" width="56" alt="E1"> | PETG-CF nero | 2 bobine da 1 kg | tutte le parti funzionali: corpo (base, chiglia, slitte, sportello della batteria), zampe (coxa, ponte, femori, tibie) | circa 860 g di pezzi (stima dal modello del 9 ottobre) più provini, supporti e scarti | 3DJake.it: [eSUN PETG-CF nero 1 kg](https://www.3djake.it/esun/petg-cf-black-3), 2 × 29,49 € (V; ugello 240–260 °C) | A (scelta dell'utente, 9 ottobre 2026) |
| E2 | <img src="https://3d.nice-cdn.com/upload/image/product/large/default/esun-pla-basic-white-175-mm-1000-g-espool-775140-it.jpg" width="56" alt="E2"> | PLA colorato (bianco per ora) | 1 bobina | placche: carapace, lame dei femori, gusci delle tibie; vassoio dell'ESP32 (sotto l'antenna niente carbonio) | circa 230 g; il colore può cambiare | 3DJake.it: [eSUN PLA Basic bianco 1 kg](https://www.3djake.it/esun/pla-basic-white), 12,69 € (V) | A (scelta dell'utente) |
| E2b | <img src="https://3d.nice-cdn.com/upload/image/product/large/default/esun-pla-basic-black-175-mm-1000-g-espool-774021-it.jpg" width="56" alt="E2b"> | PLA nero (o un secondo colore) | 1 bobina piccola | fascia, visiera, gonne, sportellino: stampati insieme al carapace, PLA su PLA si attacca senza interlocking | circa 15 g | 3DJake.it: [eSUN PLA Basic nero 1 kg](https://www.3djake.it/esun/pla-basic-black-1), 12,69 € (V; non ci sono bobine più piccole) | proposta (D-065) |
| E3 | <img src="https://3d.nice-cdn.com/upload/image/product/large/default/3djake-tpu-a95-arancione-1207105-it.png" width="56" alt="E3"> | TPU 95A arancio | pochi grammi | piedini (D9) | circa 10 g | 3DJake.it: [3DJAKE TPU A95 arancio 750 g](https://www.3djake.it/3djake/tpu-a95-orange), 30,49 € (V; la confezione più piccola in arancio) | A (scelta dell'utente) |

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

Prezzi delle voci X (10 ottobre 2026, IVA inclusa; facoltativi, niente è approvato). La striscia LED è la WS2812B-2020 a **120 LED/m**, larga 4 mm (D-068).

| Foto | Livello | Voce | Prodotto | Negozio | Costo |
|---|---|---|---|---|---|
| <img src="https://cdn-shop.adafruit.com/480x360/4210-00.jpg" width="48" alt="X1"> | alte | X1 | cavi Qwiic Adafruit 4210 100 mm, 5 pz | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/4210/10230021) | 5,06 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/4210-00.jpg" width="48" alt="X1"> | alte | X1 | cavo Qwiic con prese femmina Adafruit 4397 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/4397/10824270) | 1,01 € (V) |
| <img src="https://kamami.pl/105748-large_default/dc-dc-step-down-converter-module-33v-d24v5f3.jpg" width="48" alt="X3"> | alte | X3 | Pololu D24V5F3 #2842 | [Kamami](https://kamami.pl/en/step-down/558118-pololu-2842-pololu-33v-500ma-step-down-voltage-regulator-d24v5f3.html) | 7,76 € (V) |
| <img src="https://a.pololu-files.com/picture/0J11767.1200x627.jpg?9cec8ded097e97a57913799c94b50cc0" width="48" alt="X4"> | alte | X4 | Pololu LSM6DSO #2798 | [pololu.com](https://www.pololu.com/product/2798) | 22,40 € (S) |
| <img src="https://www.tinytronics.nl/image/cache/catalog/products_2024/interlink-electronics-fsr-400-membrane-pressure-sensor-7.2mm-round-short-soldertabs-600x315w.jpg" width="48" alt="X5"> | alte | X5 | Interlink FSR 400 Short 34-00004, 7 pz | [Tinytronics](https://www.tinytronics.nl/en/sensors/weight-pressure-force/membrane/interlink-electronics-fsr-400-short-tail-membrane-pressure-sensor-7.6mm-round-soldertabs) | 35,00 € (V) |
| <img src="https://www.tinytronics.nl/image/cache/catalog/products_2024/interlink-electronics-fsr-400-membrane-pressure-sensor-7.2mm-round-short-soldertabs-600x315w.jpg" width="48" alt="X5"> | alte | X5 | cavo siliconico 28 AWG, rosso e nero, 3 m ciascuno | [AliExpress](https://it.aliexpress.com/item/1005009017260144.html) | 3,42 € (V) |
| <img src="https://www.tinytronics.nl/image/cache/catalog/products_2024/interlink-electronics-fsr-400-membrane-pressure-sensor-7.2mm-round-short-soldertabs-600x315w.jpg" width="48" alt="X5"> | alte | X5 | partitori: 10 kΩ 1 % × 6, 100 nF × 6 | [DigiKey.it](https://www.digikey.it/en/products/detail/yageo/MFR-25FRF52-10K/14626) | 1,36 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/5836-00.jpg" width="48" alt="X6"> | alte | X6 | Adafruit ADS7830 #5836 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/5836/21839818) | 6,37 € (V) |
| <img src="https://kamami.pl/80509-large_default/vl53l7cx-time-of-flight-8-8-zone-wide-fov-distance-sensor-carrier-with-voltage-regulator-350cm-max.jpg" width="48" alt="X8"> | alte | X8 | Pololu VL53L7CX #3418 | [Kamami](https://kamami.pl/czujniki-odleglosci/1186902-vl53l7cx-time-of-flight-8-8-zone-wide-fov-distance-sensor-carrier-with-voltage-regulator-350cm-max-5906623469284.html) | 19,30 € (V) |
| <img src="https://ae-pic-a1.aliexpress-media.com/kf/S640d105dc5154baab34c8ed3fac068166.jpg" width="48" alt="X9"> | alte | X9 | striscia WS2812B-2020 120 LED/m, FPC 4 mm, 1 m | [AliExpress](https://it.aliexpress.com/item/1005009482531544.html) | 11,79 € (V) |
| <img src="https://ae-pic-a1.aliexpress-media.com/kf/S640d105dc5154baab34c8ed3fac068166.jpg" width="48" alt="X9"> | alte | X9 | SN74AHCT125N DIP-14, 330 Ω × 2, 10 kΩ × 2, PTC Bourns MF-R075 × 2 | [DigiKey.it](https://www.digikey.it/en/products/detail/texas-instruments/SN74AHCT125N/375798) | 2,38 € (V) |
| <img src="https://mm.digikey.com/Volume0/opasdata/d220001/medias/images/667/WP710A10SYD.JPG" width="48" alt="X13"> | alte | X13 | LED 3 mm giallo Kingbright WP710A10SYD × 2, 1 kΩ × 2 | [DigiKey.it](https://www.digikey.it/en/products/detail/kingbright/WP710A10SYD/3084207) | 1,09 € (V) |
| <img src="https://mm.digikey.com/Volume0/opasdata/d220001/medias/images/864/61201623021.jpg" width="48" alt="X2"> | medie | X2 | box header 2 × 8, 2 IDC 16 poli, cavo piatto 61 cm, 470 µF 10 V | [DigiKey.it](https://www.digikey.it/en/products/detail/w%C3%BCrth-elektronik/61201623021/2060599) | 5,26 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/4226-12.jpg" width="48" alt="X7"> | medie | X7 | Adafruit INA260 #4226, 2 pz | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/4226/10130492) | 21,32 € (V) |
| <img src="https://www.buerklin.com/en/images/dae/9163079581726/500x500/ntc-10-k-1-0-06-w-3988-k-0-002-w-k-15-s-tht-b57861s0103f040.webp" width="48" alt="X14"> | medie | X14 | NTC TDK B57861S0103F040, 3 pz | [Bürklin](https://buerklin.com/en/p/epcos/ntc-thermistors/b57861s0103f040/80E6746) | 11,32 € (S) |
| <img src="https://www.buerklin.com/en/images/dae/9163079581726/500x500/ntc-10-k-1-0-06-w-3988-k-0-002-w-k-15-s-tht-b57861s0103f040.webp" width="48" alt="X14"> | medie | X14 | 10 kΩ 1 % × 3 | [DigiKey.it](https://www.digikey.it/en/products/detail/yageo/MFR-25FRF52-10K/14626) | 0,14 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/3421-03.jpg" width="48" alt="X16"> | medie | X16 | Adafruit SPH0645 #3421, 2 pz | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/3421/6691114) | 14,88 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/3006-04.jpg" width="48" alt="X17"> | medie | X17 | Adafruit MAX98357A #3006 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/3006/6058477) | 6,37 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/3006-04.jpg" width="48" alt="X17"> | medie | X17 | altoparlante Same Sky CMS-15113-078SP-67 | [DigiKey.it](https://www.digikey.it/en/products/detail/same-sky-formerly-cui-devices/CMS-15113-078SP-67/9561103) | 3,21 € (V) |
| <img src="https://kamami.pl/31951-large_default/distance-sensor-vl53l1x-4-400-cm-in-tof-technology-with-voltage-regulator.jpg" width="48" alt="X19"> | medie | X19 | Pololu VL53L1X #3415 | [Kamami](https://kamami.pl/en/distance-sensors/571453-distance-sensor-vl53l1x-4-400-cm-in-tof-technology-with-voltage-regulator.html) | 28,78 € (V) |
| <img src="https://www.sparkfun.com/media/catalog/product/cache/6b78ac9ed927a3c2db42a3c84dab4ce5/1/7/17047-SparkFun_Qwiic_GPIO-01.jpg" width="48" alt="X20"> | medie | X20 | SparkFun Qwiic GPIO TCA9534 DEV-17047 (in arrivo il 24 novembre) | [DigiKey.it](https://www.digikey.it/en/products/detail/sparkfun-electronics/17047/13419022) | 7,23 € (V) |
| <img src="https://ae-pic-a1.aliexpress-media.com/kf/Sa63c7c29c9a64cf68382d7b623461fe3N.jpg" width="48" alt="X31"> | medie | X31 | cavo siliconico 30 AWG, 3 colori × 3 m | [AliExpress](https://it.aliexpress.com/item/1005009017260144.html) | 4,77 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/6062-00.jpg" width="48" alt="X15"> | basse | X15 | Adafruit INA3221 #6062, 2 pz | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/6062/25660599) | 23,44 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/1602-00.jpg" width="48" alt="X18"> | basse | X18 | Adafruit CAP1188 #1602 e nastro di rame #3483 | [DigiKey.it](https://www.digikey.it/en/products/result?keywords=1528-1026-ND) | 13,83 € (V) |
| <img src="https://a.pololu-files.com/picture/0J12702.1200x627.jpg?6551b3a74a9f8d833593244ea054a247" width="48" alt="X25"> | basse | X25 | Pololu VL53L4CD #3692 | [pololu.com](https://www.pololu.com/product/3692) | 15,65 € (S) |
| <img src="https://ae-pic-a1.aliexpress-media.com/kf/S32a95c86378c4a3c9017996ccd10a488k.jpg" width="48" alt="X26"> | basse | X26 | Hi-Link HLK-LD2410C | [AliExpress](https://it.aliexpress.com/item/1005008754208019.html) | 3,79 € (S) |
| <img src="https://cdn-shop.adafruit.com/480x360/3595-06.jpg" width="48" alt="X27"> | basse | X27 | Adafruit APDS-9960 #3595 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/3595/7652603) | 8,04 € (V) |
| <img src="https://ae-pic-a1.aliexpress-media.com/kf/Sbb6aa0c9301d4a5589eab94f24c09d30O.jpg" width="48" alt="X28"> | basse | X28 | LDROBOT LD06 | [AliExpress](https://it.aliexpress.com/item/1005010348234406.html) | 36,57 € (S) |
| <img src="https://cdn-shop.adafruit.com/480x360/4469-05.jpg" width="48" alt="X29"> | basse | X29 | Adafruit MLX90640 110° #4469 (in arrivo il 4 novembre) | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/4469/11497511) | 80,29 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/5836-00.jpg" width="48" alt="X32"> | basse | X32 | Adafruit ADS7830 #5836, 2 in più | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/5836/21839818) | 12,74 € (V) |
| <img src="https://cdn-shop.adafruit.com/480x360/5690-00.jpg" width="48" alt="X33"> | basse | X33 | Adafruit seesaw ATtiny1616 #5690 | [DigiKey.it](https://www.digikey.it/en/products/detail/adafruit-industries-llc/5690/18627499) | 5,31 € (V) |
| <img src="https://radxa.com/zero/3w/thumb_zero3w.webp" width="48" alt="Radxa"> | basse | Radxa | Radxa ZERO 3W 4 GB / 32 GB eMMC | [RS Components](https://ie.rs-online.com/web/p/rock-sbc-boards/2564694) | 62,13 € (S) |
| <img src="https://cdn1.botland.store/80780-pdt_540/step-down-voltage-converter-d36v28f5-5v-32a-pololu-3782.jpg" width="48" alt="Reg 5 V"> | basse | Reg 5 V | Pololu D36V28F5 #3782 (Botland: solo clienti B2B?) | [Botland](https://botland.store/converters-step-down/17169-step-down-voltage-converter-d36v28f5-5v-32a-pololu-3782-5903351242837.html) | 17,90 € (S) |
| <img src="https://kamami.pl/74354-large_default/modul-konwertera-usb-uart-na-usb-c-ch340n.jpg" width="48" alt="USB-seriale"> | basse | USB-seriale | modulo CH340N USB-C 3,3/5 V | [Kamami](https://kamami.pl/konwertery-usb---uart--rs232/1183592-modul-konwertera-usb-uart-na-usb-c-ch340n-5906623466696.html) | 1,71 € (V) |

| Insieme | Merce | Spedizioni | Totale |
|---|---|---|---|
| alte | 116,94 € | 52,50 € | 169,44 € |
| medie | 103,28 € | 37,69 € | 140,97 € |
| basse | 281,40 € | 37,50 € | 318,90 € |
| alte e medie | 220,22 € | 40,19 € | 260,41 € |
| tutte | 501,62 € | 57,69 € | 559,31 € |

- **Spedizioni**: quelle di pololu.com (circa 20 €), RS, Bürklin, Botland e Tinytronics sono stime S. pololu.com spedisce da fuori UE, quindi può esserci la dogana. AliExpress spedisce gratis sopra 10 €. DigiKey è gratis sopra 75 €, altrimenti costa 25 €: con alte e medie si arriva a 76 €.
- **Da controllare**:
  - X13: a magazzino c'è solo il LED giallo a 590 nm;
  - X17: l'altoparlante è la variante -67 (IP67);
  - X33: il seesaw attuale è l'ATtiny1616 (#5690);
  - X20 e X29: in arrivo a novembre;
  - X4 e X25: solo su pololu.com;
  - il regolatore 5 V del computer di bordo: Botland dice di vendere solo a clienti B2B;
  - X26 e X28: prezzo letto nell'elenco di ricerca di AliExpress, non nella pagina del prodotto.

Viteria in più se si montano tutte, da contare a robot deciso: inserti M2 (D5) per IMU 2, ADC 2, INA260 4, scheda del carapace 4, amplificatore 2, zaino 4; viti M2 corte per le stesse; viti M3 delle slitte più lunghe di 2,4 mm con i supporti degli INA260.

## Ordine degli acquisti consigliato

1. **Una squadretta metallica** (D3), qualche cuscinetto e perno (D1, D2), inserti e viti M3: servono per il provino stampato della culla e del giunto, che conferma le quote del servo prima di tutto il resto.
2. Alimentazione (B1–B19) e controllo (C1–C4): per la prova al banco della SSC-32 con un lato di servo.
3. Il resto delle squadrette, cuscinetti e perni nella lunghezza decisa dal CAD.
4. Filamento quando si stampano le parti vere; prolunghe e prolunga di bilanciamento dopo il CAD.

## Carrelli e costo totale

Prezzi IVA inclusa del 10 ottobre 2026; V letto sulla pagina, S stimato. Amazon.it e AliExpress sono letti nelle pagine aperte in Chrome (con la consegna in Italia). I prezzi in PLN di Kamami sono convertiti a 0,23 €/PLN: sul sito si può scegliere l'euro, e il totale può cambiare di qualche percento.

### Voci approvate (B, C, D, E con stato A)

| Negozio | Voci | Merce | Spedizione in Italia | Totale |
|---|---|---|---|---|
| Kamami | B1, B2, B3, B3b, B4, B6, B9, B10, B11, B13, B19, C1, C2, C3, C4, C5, D11 | 176,82 € | 8,24 € (FedEx zona 1, 6,70 € + IVA; nessuna soglia gratuita per l'estero, S) | 185,06 € |
| 3DJake.it | E1, E2, E3 | 102,16 € | 0,00 € (gratis sopra 49,90 €, V) | 102,16 € |
| AliExpress | D3 | 10,08 € | 0,00 € (gratis sopra 10 €, V) | 10,08 € |
| Amazon.it | B5, B7, B8, B12, B14, B15, B16, B17, B18, C2, C3, D6, D8, D10, D11 | 198,64 € | 0,00 € (gratis sopra 29 € per gli articoli venduti da Amazon; per i venditori terzi può variare, S) | 198,64 € |
| **Totale** | | **487,70 €** | **8,24 €** | **495,94 €** |

- **Kamami** (Polonia, FedEx 3–7 giorni) porta in un solo pacco i regolatori Pololu e quasi tutta la minuteria, con 20 righe. Le predisposizioni Pololu (X3, X8, X19) si aggiungono senza altra spedizione.
- **Amazon.it**: 18 righe di minuteria, cavi e viti, ciascuna con il suo ASIN. Alcune sono di venditori terzi: la spedizione gratuita sopra 29 € vale per gli articoli venduti o spediti da Amazon, quindi va controllata nel carrello.
- **Viti**: il kit Amazon con le due confezioni in più (32,60 €) costa meno di Gedex con le misure esatte (53,03 € con la spedizione) e porta anche dadi e rondelle.
- **Squadrette** (D3): su AliExpress il disco da 25 denti costa 0,42 €, ma diametro e fori non sono dichiarati. Prima se ne provano 1–2 pezzi (BOM, domanda 4). Con le misure del CAD dichiarate c'è la diymore su Amazon, 6 pezzi a 10,99 €.
- **Con le voci X**: conviene spostare B7 e B8 su DigiKey (9 € di merce), così il carrello DigiKey supera i 75 € e la spedizione è gratuita.

Fuori dal totale:

| Foto | Voci | Stato | Negozio | Costo |
|---|---|---|---|---|
| <img src="https://ae-pic-a1.aliexpress-media.com/kf/S2e04d5aab94e41f188e15e029ba305c2E.jpg" width="48" alt="D8b"> | D8b, M2 × 6 svasate DIN 7991 inox 304, 50 pz | da approvare / ? | [AliExpress](https://it.aliexpress.com/item/33028389667.html) | 1,85 € (V) |
| <img src="https://3d.nice-cdn.com/upload/image/product/large/default/esun-pla-basic-black-175-mm-1000-g-espool-774021-it.jpg" width="48" alt="E2b"> | E2b, eSUN PLA Basic nero 1 kg | da approvare / ? | [3DJake.it](https://www.3djake.it/esun/pla-basic-black-1) | 12,69 € (V) |
| <img src="https://ae-pic-a1.aliexpress-media.com/kf/Se49e7214ca17467cae9596d8df4ab098V.jpg" width="48" alt="C7"> | C7, prolunga bilanciamento JST-XH 2S 20 cm, 5 pz | da approvare / ? | [AliExpress](https://it.aliexpress.com/item/1005004996032030.html) | 2,32 € (V) |
| <img src="https://m.media-amazon.com/images/I/81-Dhjx3LXL._AC_UL320_.jpg" width="48" alt="D1"> | D1, METERXITY MF105ZZ 5 × 10 × 4, 20 + 4 pz | a tua cura | [Amazon.it](https://www.amazon.it/dp/B0F4QWY4XZ) | 30,62 € (V) |
| <img src="https://m.media-amazon.com/images/I/71IQ-4VR6oL._AC_UL320_.jpg" width="48" alt="D2"> | D2, QUARKZMAN spine 5 × 12 inox 316L, 40 pz (tolleranza non dichiarata) | a tua cura | [Amazon.it](https://www.amazon.it/dp/B0FGJKXFY3) | 11,69 € (V) |
| — | A1–A5, D4, D5 | già in possesso | — | 0 € |

Rispetto alla stima della versione 2.0 (circa 380 € di componenti più circa 100 € di filamento): **circa 495,94 €** consegnati. Il filamento costa 102 €, i regolatori 105 €.

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
