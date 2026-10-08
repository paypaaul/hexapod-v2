# Servo controller SSC-32 ("SSC-32 V2.5"): varianti e cloni, meccanica, alimentazione, seriale, livelli logici, baud rate

Data della ricerca: 8 ottobre 2026.

Legenda etichette: [primary] = manuale / datasheet / pagina prodotto del costruttore; [secondary] = negozio, blog, wiki, documentazione del venditore di un clone; [3rd-meas] = misura di terzi; [community] = forum; [computed] = calcolo o misura mia (formula indicata).

Come sono stati letti i documenti. I PDF (manuale SSC-32 Ver 2.0, guida SSC-32U V1.1, scheda RB-LYN-850, datasheet ATmega48/88/168, datasheet ATmega328P, datasheet ESP32-S3 v2.2) sono stati scaricati e il testo estratto in locale: i numeri attribuiti a questi documenti li ho visti scritti nel testo originale. Le inserzioni Amazon.it e AliExpress del clone sono state aperte nel browser e lette direttamente (testo e immagini). I siti robotshop.com, community.robotshop.com e wiki.lynxmotion.com rispondono 403 ai robot: tutto cio' che viene da li' e' passato attraverso il riassunto del motore di ricerca ed e' marcato "NON VISTO SULLA FONTE".

---

## 1. Che cos'e' una "SSC-32 V2.5"? Quali schede si vendono con il nome SSC-32 e come distinguerle

### Takeaway
"V2.5" NON e' una revisione hardware Lynxmotion: e' la serigrafia di un clone cinese della Lynxmotion SSC-32U (micro-USB + zoccolo XBee, micro SMD), venduto come "SSC32-V2.5 32ch Multi-Channel Servo Controller with USB XBEE Interface"; il "2.5" coincide con il firmware ufficiale "2.50USB" della SSC-32U. Il clone e' piu' piccolo della Lynxmotion (circa 72 x 55 mm contro 76.2 x 58.4 mm), quindi anche la dima di foratura e' diversa. La variante esatta in mano all'utente NON si puo' stabilire con certezza senza una foto o il link d'acquisto: l'ipotesi di gran lunga piu' probabile e' il clone USB/XBee.

### Cited Findings

**A) Lynxmotion SSC-32 originale (manuale "SSC-32 Ver 2.0")**
- Il manuale ufficiale si intitola "Users Manual SSC-32 Ver 2.0", "Manual written for firmware version SSC32-1.06XE", "Copyright © 2005 by Lynxmotion, Inc." — [primary, copia ospitata da terzi] [manuale SSC-32 Ver 2.0, pag. 1 e 15](https://hobbielektronika.hu/forum/getfile.php?id=81561). URL ufficiale del PDF: [lynxmotion.com/images/data/ssc-32.pdf](http://www.lynxmotion.com/images/data/ssc-32.pdf) (reindirizza al wiki Lynxmotion, 403 ai robot: non letto da li').
- Una seconda copia dello stesso manuale porta in copertina il firmware "SSC32-1.03XE" con lo stesso testo hardware: quindi "Ver 2.0" e' la versione della scheda/manuale, non del firmware — [primary, copia ospitata da INFN Roma1] [28_ssc-32v2.pdf](https://www.roma1.infn.it/~meddif/LabElRob_MaterialeDidattico/28_ssc-32v2.pdf).
- Nel disegno del manuale si vedono: connettore DB9 ("DB9 Port, True RS232 level serial connector"), zoccolo DIP per "Atmel IC", zoccolo EEPROM a 8 pin, tre morsetti a vite separati a 2 poli (VS2, VL, VS1), ponticelli BAUD + ingressi A B C D, LED D1, connettore "TTL Serial Port" (TX RX + massa), serigrafia "SSC-32" e "lynxmotion.com" — [primary, osservazione mia del disegno] [manuale SSC-32 Ver 2.0, pag. 2](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Il microcontrollore e' un ATmega168: la guida SSC-32U, che riusa il testo dei registri, parla di "EEPROM in the ATMega168 processor" — [primary] [guida SSC-32U V1.1, pag. 38-39](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Specifiche secondo inserzione RobotShop e wiki Lynxmotion: "ATMEGA168-20PU", velocita' "14.75 MHz", "Current requirements: 31mA", 32 uscite, 4 ingressi, porta DB9, "PC board size: 3.0" x 2.3"", firmware di riferimento 2.01XE; prodotto fuori produzione, sostituito dalla SSC-32U — [secondary, riassunto del motore di ricerca: NON VISTO SULLA FONTE] [RobotShop SSC-32](https://www.robotshop.com/products/lynxmotion-ssc-32-servo-controller), [wiki Lynxmotion SSC-32](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/servo-erector-set-system/ses-electronics/ses-modules/ssc-32/).

**B) Lynxmotion SSC-32U (USB)**
- "The Lynxmotion SSC-32U is a versatile and easy to use R/C servo controller, the core of which is an Atmel ATmega328p"; ingressi "USB, serial or XBee" — [primary] [guida SSC-32U V1.1 (agosto 2015), pag. 3](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- "Firmware: 2.50USB"; "Microcontroller: Atmel ATmega328P"; "External EEPROM: 512 kbit"; "Serial input: USB, 3.3V Xbee, TTL UART, N81"; "PC interface: USB Mini B (cable included)"; "Microcontroller interface: 0.1" Header" — [primary] [scheda prodotto RB-LYN-850, pag. 3](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf).
- Convertitore USB-seriale: "an FTDI chip (the area highlighted next to the USB port)" — [primary] [guida SSC-32U, pag. 11](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Nella foto del manuale: un solo blocco morsetti verde a 6 poli (VS2, VL, VS1), connettore mini-USB, zoccolo XBee, pulsante "Baud", LED A e B, due condensatori elettrolitici, serigrafia "SSC-32U lynxmotion.com" — [primary, osservazione mia della figura] [guida SSC-32U, pag. 7-8](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).

**C) Clone cinese "SSC-32 V2.5" (micro-USB + XBee)**
- Inserzione AliExpress (letta nel browser l'8/10/2026): "SSC32-V2.5 32ch Servo Controller multicanale con interfaccia USB XBEE Fit PC MAC LINUX per Hexapod Spider e robot Biped", venditore "superior RC parts", 28,19 EUR IVA inclusa, "47 disponibili", consegna stimata 18-26 ottobre, 12 venduti — [secondary] [it.aliexpress.com/item/1005001887832328](https://it.aliexpress.com/item/1005001887832328.html).
- Descrizione del venditore (traduzione automatica AliExpress): "Rispetto al servo controller a 32 canali, ha un volume inferiore"; "integra una interfaccia USB"; "Viene aggiunta una interfaccia XBEE"; modalita' di controllo "completamente compatibili con il software di controllo di LYNXMOTION" — [secondary] [it.aliexpress.com/item/1005001887832328](https://it.aliexpress.com/item/1005001887832328.html).
- Immagini della descrizione del venditore (testo in inglese dentro le immagini, lette da me): disegno della scheda con etichette "XBee", "Baud", "RX TX GND", "ICSP A B C D", "V G", morsetti "+VS1− / +VL− / +VS2−", ponticelli "VS VL" e "VS1 VS2", e la didascalia "No.0-31 pins are for servo, black pin for GND, red pin for positive and white pin for servo signal." — [secondary] [immagine layout](https://ae-pic-a1.aliexpress-media.com/kf/H3ffa527f479b4b848dc8d326b0d79583M.jpg).
- "The onboard memory chip can store 3,200 actions and can be run offline. Comes with supporting PC software." — [secondary] [immagine USB](https://ae-pic-a1.aliexpress-media.com/kf/H09d24d3dfbdd4155ac4d56eb4f0c827ew.jpg). (Frase che non corrisponde a nessuna funzione descritta nei manuali Lynxmotion: possibile testo riciclato da un altro prodotto o firmware diverso.)
- Riepilogo "generato da IA" della stessa pagina AliExpress: "dimensioni di 72x55 mm e peso di soli 0,071 kg" (la pagina avverte che non rappresenta l'opinione del venditore) — [secondary, bassa affidabilita' presa da sola] [it.aliexpress.com/item/1005001887832328](https://it.aliexpress.com/item/1005001887832328.html).
- Inserzione Amazon.it: "Glayent SSC32-V2.5 32ch Multi-Channel Servo Controller con interfaccia USB XBEE ...", ASIN B0FM8S6W59, "Non disponibile. Non sappiamo se o quando l'articolo sara' di nuovo disponibile."; "peso articolo 61 Grammi"; "Volume/peso dell'unita' di vendita 71.0 Grammi"; "Dimensioni dell'articolo 9 x 7 x 3 cm" — [secondary] [amazon.it/dp/B0FM8S6W59](https://www.amazon.it/dp/B0FM8S6W59).
- Foto principale Amazon (osservazione mia): PCB verde con serigrafia "SSC-32" e sotto "V2.5"; nessuna scritta "lynxmotion"; connettore micro-USB; due strisce femmina per XBee; pulsante BAUD; LED "A" e "B"; blocco morsetti verde a 6 poli; due elettrolitici; microcontrollore SMD a 32 pin; quarzo HC-49S; 4 integrati SMD; 4 fori agli angoli — [secondary, foto del venditore] [immagine](https://m.media-amazon.com/images/I/61z4KjfDqpL._AC_SL1001_.jpg).
- Stesso prodotto con altri marchi: "MVOSJFIE SSC32-V2.5 ..." su [Amazon.co.uk B0F63D2QZY](https://www.amazon.co.uk/MVOSJFIE-SSC32-V2-5-Multi-Channel-Controller-Interface/dp/B0F63D2QZY) e su [Walmart](https://www.walmart.com/ip/SSC32-V2-5-32ch-Multi-Channel-Servo-Controller-with-USB-XBEE-Interface-Fit-PC-LINUX-for-Hexapod-Spider-Biped-Robots/15678665779) — [secondary, solo titoli dai risultati di ricerca].

**D) Altre schede vendute con il nome SSC-32**
- Tra gli "articoli correlati" della pagina AliExpress compaiono due prodotti diversi: "32 Scheda di controllo servo SSC-32 Scheda di controllo servo Sensore modulo scheda di controllo servo" (12,19 EUR) e "Scheda Controllo Servo PWM a 32 Canali, Interfaccia UART/TTL, Compatibile con Protocollo SSC-32, per Arduino e Braccio Robotico" (12,49 EUR) — [secondary, solo titoli e prezzi; pagine non aperte] [it.aliexpress.com/item/1005001887832328](https://it.aliexpress.com/item/1005001887832328.html).
- Cloni della SSC-32 originale venduti come "SSC-32 32Ch Servo Controller Lynxmotion Compatible" e "32 Servo Control Board SSC-32" — [secondary, solo titoli dai risultati di ricerca: NON VISTO SULLA FONTE] [dishantech.com](https://dishantech.com/product/ssc-32-32ch-servo-controller-lynxmotion-compatible/), [eBay 154510202797](https://www.ebay.com/itm/154510202797).
- Sul forum RobotShop esistono discussioni su altri cloni ("SSC-32U clone called QSC-32E?") — [community, solo titolo] [community.robotshop.com](https://community.robotshop.com/forum/t/ssc-32u-clone-called-qsc-32e/25951).

**Come distinguerle da una foto**

| Caratteristica | Lynxmotion SSC-32 (orig.) | Lynxmotion SSC-32U | Clone "SSC-32 V2.5" |
|---|---|---|---|
| Connettore PC | DB9 RS-232 | mini-USB B | micro-USB |
| Microcontrollore | ATmega168 DIP su zoccolo | ATmega328P SMD | SMD 32 pin (sigla da leggere) |
| Morsetti | 3 morsetti separati a 2 poli | 1 blocco a 6 poli | 1 blocco a 6 poli |
| Baud | ponticelli BAUD | pulsante + LED A/B | pulsante + LED A/B |
| Zoccolo XBee | no | si' | si' |
| Serigrafia | "SSC-32" + "lynxmotion.com" | "SSC-32U" + "lynxmotion.com" | "SSC-32" + "V2.5", niente "lynxmotion" |
| PCB | 76.2 x 58.4 mm | 76.2 x 58.4 mm | circa 72 x 55 mm (stima) |

Fonti della tabella: [manuale SSC-32 Ver 2.0 pag. 2](https://hobbielektronika.hu/forum/getfile.php?id=81561) [primary]; [guida SSC-32U pag. 7-13](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf) [primary]; [foto Amazon.it](https://www.amazon.it/dp/B0FM8S6W59) e [AliExpress](https://it.aliexpress.com/item/1005001887832328.html) [secondary]; dimensioni vedi sezione 2.

### Inferences
- Nessuna fonte Lynxmotion trovata usa "V2.5" come revisione della scheda: le versioni ufficiali incontrate sono "SSC-32 Ver 2.0" (scheda/manuale) e i firmware 1.03XE, 1.06XE, 2.01XE (SSC-32) e 2.50USB (SSC-32U). "V2.5" compare invece stampato sul PCB del clone. Conclusione: "SSC-32 V2.5" identifica in pratica il clone micro-USB/XBee.
- Il clone copia l'architettura della SSC-32U (blocco morsetti a 6 poli, pulsante baud, LED A/B, XBee, ponticelli VS1=VS2 e VS/VL): il riferimento funzionale e' la guida SSC-32U, non il manuale della SSC-32 originale. NON e' garantito che regolatore, selezione automatica dell'alimentazione logica, chip USB e firmware siano identici.
- "V2.5" da solo non basta a identificare la scheda senza ambiguita': va confermato con una foto (connettore micro-USB + serigrafia "V2.5" = clone).

### Gaps
- Scheda tecnica del clone (microcontrollore, chip USB, regolatore, quarzo, correnti ammesse): NON TROVATO; il venditore pubblica solo le immagini citate.
- Stringa restituita dal clone al comando VER: NON TROVATO.

---

## 2. Meccanica: dimensioni PCB, fori di fissaggio, altezza, peso, modello 3D

### Takeaway
Lynxmotion SSC-32U (e, per dichiarazione del costruttore, SSC-32 originale): PCB 3.00" x 2.30" = 76.20 x 58.42 mm, 4 fori da 0.125" = 3.175 mm con centro a 0.15" = 3.81 mm dai bordi, interasse 68.58 x 50.80 mm. Clone "V2.5": circa 72 x 55 mm con interasse fori stimato circa 65.4 x 48.4 mm (misura mia su due immagini del venditore, incertezza circa ±1 mm): la dima Lynxmotion NON va bene per il clone. Altezza, peso della scheda nuda e modello STEP: NON TROVATI. Nessuna quota va congelata nel CAD prima della misura col calibro sul pezzo.

### Cited Findings

**Lynxmotion**
- "The SSC-32U is 3.00" x 2.30" with 0.125" holes set in 0.15" from each edge. It was designed to the same dimensions as the Lynxmotion BotBoarduino, the Lynxmotion SSC-32 (its predecessor), the Lynxmotion Bot Board and Bot Board 2 so they could be stacked." Disegno quotato "SSC-32U Board Dimensions (inches)": 3.000, 2.300, 0.150 (dal bordo al centro foro, su entrambi gli assi), ⌀0.125 — [primary] [guida SSC-32U V1.1, pag. 7](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- "PC board size: 3.0" x 2.3" (mounting holes set 0.15" from each edge)" — [primary] [scheda RB-LYN-850, pag. 3](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf).
- Conversioni — [computed]: 3.00 x 25.4 = 76.20 mm; 2.30 x 25.4 = 58.42 mm; 0.125 x 25.4 = 3.175 mm; 0.15 x 25.4 = 3.81 mm; interasse fori = (3.00 − 2 x 0.15) x 25.4 = 68.58 mm e (2.30 − 2 x 0.15) x 25.4 = 50.80 mm.
- Il manuale della SSC-32 originale (Ver 2.0) NON riporta dimensioni ne' fori nel testo — [primary, verificato sull'intero testo estratto] [manuale SSC-32 Ver 2.0](https://hobbielektronika.hu/forum/getfile.php?id=81561). Le dimensioni della originale vengono dalla frase della guida SSC-32U ("same dimensions as ... SSC-32") e dall'inserzione RobotShop ("3.0" x 2.3"", NON VISTO SULLA FONTE) — [secondary] [RobotShop SSC-32](https://www.robotshop.com/products/lynxmotion-ssc-32-servo-controller).

**Clone V2.5: misura mia sulle immagini del venditore**
- Metodo — [computed]: uso come righello il passo degli header servo (2.54 mm). Sul disegno del venditore ([immagine layout](https://ae-pic-a1.aliexpress-media.com/kf/H3ffa527f479b4b848dc8d326b0d79583M.jpg), vista a 800x600 px) i 4 pin di un gruppo distano 19.0 px l'uno dall'altro → 7.48 px/mm; il PCB misura 539 x 417 px → 539/7.48 = 72.1 mm e 417/7.48 = 55.7 mm.
- Controllo incrociato sulla foto dall'alto di Amazon ([immagine](https://m.media-amazon.com/images/I/61z4KjfDqpL._AC_SL1001_.jpg)): passo pin 22.9 px → 9.02 px/mm; PCB 649 x 496 px → 72.0 x 55.0 mm — [computed].
- Fori — [computed, stesse immagini]: centri a circa 3.1-3.4 mm dai bordi; interasse 65.5 x 48.0-48.5 mm (disegno) e 65.3-65.4 x 48.4 mm (foto); diametro apparente 2.8-2.9 mm sulla foto (limite inferiore: il bordo sfumato riduce l'area misurata; compatibile con un foro da circa 3 mm).
- Se la scheda fosse 76.2 x 58.42 mm, alla scala del disegno dovrebbe misurare 570 x 437 px invece di 539 x 417 px: la differenza (31 px = 4 mm) e' ben oltre l'errore di misura (circa ±3 px) — [computed].
- Coerenza con il venditore: "ha un volume inferiore" rispetto al controller a 32 canali, e "72x55 mm" nel riepilogo automatico — [secondary] [AliExpress](https://it.aliexpress.com/item/1005001887832328.html).

**Disposizione dei connettori sui bordi**
- SSC-32U (figura con canali 16-31 in alto): header servo lungo i due lati lunghi (3.00"); blocco morsetti a 6 poli sul lato corto sinistro; mini-USB sul lato corto opposto, sporgente dal bordo; pin TX RX G accanto al chip FTDI, verso il lato USB; zoccolo XBee nella meta' destra — [primary, osservazione mia] [guida SSC-32U, pag. 7-12](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- SSC-32 originale (disegno con canali 16-31 in alto): morsetti VS2, VL, VS1 (dall'alto in basso) sul lato corto sinistro, con i ponticelli VS1=VS2 e VL=VS in mezzo; DB9 sul lato corto destro, sporgente; header TTL (TX RX + massa) in basso a destra sotto il DB9; ponticelli BAUD al centro in alto — [primary, osservazione mia] [manuale SSC-32 Ver 2.0, pag. 2](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Clone V2.5 (disegno del venditore, micro-USB a sinistra): canali 0-15 lungo un lato lungo e 16-31 lungo l'altro; blocco morsetti a 6 poli sul lato corto destro (VS1, VL, VS2 dall'alto in basso); micro-USB sul lato corto sinistro vicino all'angolo dei canali 28-31; header "RX TX GND" al centro-destra sopra l'header A-D, accanto ai due elettrolitici; zoccolo XBee nella meta' sinistra; ponticello "VS VL" nell'angolo accanto al canale 0, ponticello "VS1 VS2" nell'angolo accanto al canale 16; 4 fori agli angoli — [secondary] [immagine layout](https://ae-pic-a1.aliexpress-media.com/kf/H3ffa527f479b4b848dc8d326b0d79583M.jpg).

**Peso**
- SSC-32U: "Item weight 0,08 kg", "Shipping weight 0,20 kg" — [secondary, riassunto automatico della pagina; valore arrotondato] [mybotshop.de](https://www.mybotshop.de/Lynxmotion-SSC-32U-Servocontrollerboard_1).
- Clone: "peso articolo 61 Grammi" e "unita' di vendita 71.0 Grammi" (Amazon.it); "0,071 kg" (riepilogo AliExpress) — [secondary, dati di catalogo] [amazon.it/dp/B0FM8S6W59](https://www.amazon.it/dp/B0FM8S6W59), [AliExpress](https://it.aliexpress.com/item/1005001887832328.html).

### Inferences
- Due dime di foratura possibili: Lynxmotion 68.58 x 50.80 mm (fori 3.175 mm, vite M3 con 0.17 mm di gioco diametrale) oppure clone circa 65.4 x 48.4 mm (fori circa 3 mm). La differenza e' di circa 3.2 mm e 2.4 mm: un supporto stampato per una non monta l'altra.
- I valori del clone sono una stima da immagini (una e' un disegno, l'altra una foto con possibile prospettiva): buoni per l'ingombro di massima, NON per forare. In attesa della misura conviene prevedere asole nel supporto.
- Ingombro oltre il PCB: le spine dei servo escono verso l'esterno dai due lati lunghi (massa sul bordo), i cavi di potenza da un lato corto e il cavo USB dal lato corto opposto.
- I pesi di catalogo (61-80 g) includono con ogni probabilita' imballo o accessori: usarli solo come limite superiore nel bilancio di massa.

### Gaps
- Altezza complessiva (componente piu' alto; altezza con spine servo inserite) e spessore del PCB: NON TROVATO in nessun manuale ne' inserzione. Da misurare sul pezzo.
- Peso della sola scheda misurato su bilancia: NON TROVATO.
- Modello STEP / 3D della SSC-32, della SSC-32U o del clone: NON TROVATO (tre ricerche su GrabCAD / Thingiverse / wiki Lynxmotion senza esito; la pagina di ricerca GrabCAD e il wiki Lynxmotion rispondono 403 ai robot, quindi non posso escludere che esista).
- Quote ufficiali del clone (venditore o costruttore): NON TROVATO.

---

## 3. Architettura di alimentazione: morsetti VS1, VS2, VL, ponticelli, tensioni ammesse, regolatore, correnti, header servo

### Takeaway
VS1 alimenta direttamente i servo 0-15, VS2 i servo 16-31, VL la logica attraverso un regolatore a 5 V. Con la batteria 2S (6.4-8.4 V) la batteria NON va sui morsetti VS (micro servo: 4.8-6.0 V): VS va alimentato a 5-6 V da un regolatore, la logica VL direttamente dalla batteria, che rientra nei limiti di tutte e tre le schede (SSC-32: 6-9 V; SSC-32U: 5.3-16 V; clone: 6-12 V secondo il venditore, che consiglia proprio "7.4V or 8.4V battery"). Portata dichiarata Lynxmotion: 15 A di picco per lato, 3-5 A continui per lato raccomandati. Sugli header servo la massa e' sempre la fila sul bordo, poi V+, poi il segnale verso il centro.

### Cited Findings

**SSC-32 originale (manuale Ver 2.0)**
- Regolatore logica: "5vdc 500mA Low Dropout V Reg."; "The Low Dropout regulator will provide 5vdc out with as little as 5.5vdc coming in ... It can accept a maximum of 9vdc in. The regulator is rated for 500mA, but we are de-rating it to 250mA to prevent the regulator from getting too hot." — [primary] [manuale SSC-32 Ver 2.0, pag. 2, voce 1](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- "Caution! The onboard regulator can provide 250mA total. This includes the microcontroller chip, the onboard LEDs, and any attached peripherals." — [primary] [stesso, pag. 2](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- VL: "VL Terminal: Apply Logic power 6vdc thru 9vdc only."; "This input is used to isolate the logic from the Servo Power Input." — [primary] [stesso, pag. 2, voce 4](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- VS2: "This terminal connects power to servo channels 16 thru 31. Apply 4.8vdc to 7.2vdc for normal servos. Apply 4.8vdc to 6.0vdc when using micro servos." VS1: stesso testo per "servo channels 0 thru 15" — [primary] [stesso, pag. 2, voci 2 e 6](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Ponticello VS1=VS2: "Use this option when you are powering all servos from the same battery. Use both jumpers." — [primary] [stesso, voce 3](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Ponticello VL=VS: "This jumper allows powering the microcontroller and support circuitry from the servo power supply. This requires at least 6vdc to operate correctly. If the microcontroller resets when many servos are moving it may be necessary to power the microcontroller separately using the VL input." — [primary] [stesso, voce 5](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Reset per cali di tensione: "if it does drop, the voltage to the microcontroller is interrupted and the SSC-32 resets. To fix this you remove the VS1=VL jumper and connect a 9vdc battery clip to the VL input." — [primary] [stesso, pag. 12](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Alimentazione singola "generally safe": "VS of 7.2vdc 2800mAh NiCad or NiMH battery packs for up to 24 servos. VS of 7.4vdc 2800mAh LiPo battery packs for up to 24 servos. VS of 6.0vdc 1600mAh NiCad or NiMH battery packs for up to 18 servos. VS of 6.0vdc 2.0amp wall pack for up to 8 servos."; "99% of customers problems with the SSC-32 are power supply related." — [primary] [stesso, pag. 12](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Portata: "VS peak current: max 15 amps per side", "VS steady current = max 3-5 amps per side recommended" (inserzione RobotShop e wiki); un post di vendita sul forum riporta "15 amps per side, 30 amps max" — [secondary/community, riassunto del motore di ricerca: NON VISTO SULLA FONTE] [RobotShop SSC-32](https://www.robotshop.com/products/lynxmotion-ssc-32-servo-controller), [forum RobotShop](https://community.robotshop.com/forum/t/ssc-32-sequencer-software-sold/20154).
- DISACCORDO sul campo di VL della SSC-32 originale: il manuale dice "6vdc thru 9vdc only" e "maximum of 9vdc in" ([primary] [manuale Ver 2.0 pag. 2](https://hobbielektronika.hu/forum/getfile.php?id=81561)); una guida RobotShop direbbe che VL "can generally accept 6-26 V", consigliando di non superare di molto 12 V ([secondary, riassunto del motore di ricerca: NON VISTO SULLA FONTE] [Guide to the Power Supply Options for Lynxmotion Controllers](https://community.robotshop.com/blog/show/guide-to-the-power-supply-options-for-lynxmotion-controllers)). Per il progetto vale il limite piu' restrittivo (9 V), che la 2S a piena carica (8.4 V) rispetta.

**SSC-32U (guida V1.1)**
- "VS1 provides power directly to pins 0 to 15 (ideally 4.8V to 6V for standard RC servos); VS2 provides power directly to pins 16 to 31 ...; VL provides power to the logic controller" — [primary] [guida SSC-32U, pag. 9](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- VL: "The logic voltage is automatically selected between VL and VS1 (whichever has highest voltage). So long as VS1 is above 5.3V (not counting temporary drops in voltage), it is sufficient to power the logic voltage ... Ideal: Nothing connected; Nominal: 6-12V; Absolute: 5.3~16V" — [primary] [stesso, pag. 15](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Quando serve una sorgente separata su VL: "You are using 4.8V for your VS1, which isn't enough for VL"; "You want to ensure the logic is still powered even if the servo battery is depleted" — [primary] [stesso, pag. 15](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- VS1: "connects directly to the power and GND lines of servo pins 0 to 15 ... Using a 7.4V LiPo with a normal R/C servo is discouraged ... Nominal: 6V (standard R/C servos); Absolute: 0~16V" — [primary] [stesso, pag. 15](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Tensione logica interna: "V_logic which is the equivalent of MAX(VL, VS1) minus roughly 0.7V. It's the voltage that's then regulated to 5V for powering the logic circuits." — [primary] [stesso, pag. 14](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- USB: "The USB does not however power the main ATmega chip, so it must be powered separately through VS1 or VL." — [primary] [stesso, pag. 15](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- VS1=VS2: "There are two jumpers (rather than just one) because of the current involved ... If you have the two VS1 = VS2 terminals in place, you can power EITHER VS1 or VS2, but not both."; scheda spedita con i due ponticelli inseriti — [primary] [stesso, pag. 10 e 16](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- VL=VS: "Unless you are having unusual problems with the auto power select, this jumper should not be used. This jumper is not installed nor included in the package. Do not use the VL screw terminals if you install this jumper." — [primary] [stesso, pag. 16](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Portata: "VS peak current: max 15 amps per side"; "VS steady current: max 3-5 amps per side recommended"; "Logic power: auto select between VS1 and VL" — [primary] [scheda RB-LYN-850, pag. 3-4](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf).
- Uscite: "The outputs can sink or source up to 20mA per output pin, but a max of 70mA per bank must be observed." — [primary] [guida SSC-32U, pag. 32](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- "The SSC-32U board does not read the battery's voltage, and will continue to function even if a battery is being deeply discharged." — [primary] [stesso, pag. 17](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).

**Clone V2.5 (documentazione del venditore)**
- "VL is the logic power input terminal of the control board, and the input voltage is 6-12V. It is recommended to use a 7.4V or 8.4V battery or a switching power supply with sufficient power, and make sure that the power supply cannot be reversed when using it." — [secondary] [immagine alimentazione](https://ae-pic-a1.aliexpress-media.com/kf/Ha46454e5bac543578df26442fdabaa8bB.jpg).
- "VS1VS2 is the power input terminal of the [servo]. The default 6V servo is used. 6V battery or full power switching power supply is used. When the VS1 and VS2 jumper caps are shorted, only one input can be connected." Lo schema mostra "Servo BAT 6.0V DC" sui morsetti VS1, "Logic BAT 6.0~12V DC" sui morsetti VL e "Jumper cap shorted" sul ponticello VS1/VS2 — [secondary] [immagine alimentazione](https://ae-pic-a1.aliexpress-media.com/kf/Ha46454e5bac543578df26442fdabaa8bB.jpg).

**Header servo (ordine dei pin)**
- SSC-32U: "The outermost pin (farthest from the center of the board) is the ground pin (normally the black wire ...). The center pin corresponds to the voltage (normally the red wire) ... The last pin is the signal pin" (vale per entrambe le file) — [primary] [guida SSC-32U, pag. 8](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- SSC-32 originale: "Ground row (Black) / Power row (Red) / Servo Pulse (Yellow)"; nel disegno la fila con il simbolo di massa e' sul bordo, poi VS, poi PULSE verso il centro, su entrambe le file — [primary] [manuale SSC-32 Ver 2.0, pag. 2](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Clone V2.5: serigrafia massa / VS1 / PULSE dal bordo verso il centro (e PULSE / VS2 / massa sull'altro lato); "black pin for GND, red pin for positive and white pin for servo signal" — [secondary] [immagine layout](https://ae-pic-a1.aliexpress-media.com/kf/H3ffa527f479b4b848dc8d326b0d79583M.jpg).
- Numerazione Lynxmotion (vista con 16-31 in alto): gruppi di 4; 0-15 da sinistra a destra in basso, 16-31 da sinistra a destra in alto — [primary] [manuale SSC-32 Ver 2.0 pag. 2](https://hobbielektronika.hu/forum/getfile.php?id=81561); [guida SSC-32U pag. 7](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Passo tra i gruppi da 4 sul clone: circa 13 mm tra pin omologhi di gruppi adiacenti (97.4 px / 7.48 px/mm), cioe' non un multiplo esatto di 2.54 mm — [computed dal disegno del venditore].

### Inferences
- Batteria 2S (6.4-8.4 V) su VL: ammessa su SSC-32 originale (6-9 V; a 6.4 V restano 0.9 V sopra il minimo di 5.5 V del regolatore), su SSC-32U (5.3-16 V) e, secondo il venditore, sul clone (6-12 V). Batteria 2S sui morsetti VS: NO con gli MG90S.
- Se VS e' a 5.0 V, sulla SSC-32U la logica non puo' essere presa da VS1 (servono piu' di 5.3 V); a 6.0 V il margine e' 0.7 V e i picchi dei servo possono far resettare il micro. In entrambi i casi: VL direttamente dalla batteria. Sulla SSC-32 originale va TOLTO il ponticello VL=VS quando VL e' alimentato a parte; sulla SSC-32U e sul clone il ponticello VS/VL deve restare aperto.
- Il regolatore del clone non e' identificato: il "6-12 V" viene solo dal venditore. Prima di dare 8.4 V a VL leggere la sigla del regolatore (componente a 3 terminali accanto al blocco morsetti) e controllare la polarita' sulla serigrafia reale del blocco morsetti: dalle immagini l'ordine di + e − non e' leggibile con certezza.

### Gaps
- Sigla del regolatore a 5 V (Lynxmotion e clone): NON TROVATO.
- Portata nominale del blocco morsetti e larghezza/spessore delle piste VS: NON TROVATO.
- Protezione contro l'inversione di polarita' su VS/VL: nessuna menzione nei manuali; il manuale SSC-32 avverte "Never reverse the power coming into the board" ([primary] [pag. 2](https://hobbielektronika.hu/forum/getfile.php?id=81561)).

---

## 4. Seriale: DB9 / TTL, ponticelli, baud rate, protocollo, impulso

### Takeaway
SSC-32 originale: DB9 RS-232 oppure header TTL a 5 V (si tolgono i due ponticelli "DB9 enable" e si collegano TX, RX, GND); baud da due ponticelli: 2400 / 9600 / 38400 / 115200. SSC-32U e clone V2.5: tre pin TX RX GND, baud scelto con il pulsante tra 9600 / 38400 / 115200 e salvato in EEPROM; la Lynxmotion esce di fabbrica a 9600, il venditore del clone indica 115200 come predefinito. Protocollo ASCII: "#<ch>P<pw>S<spd>T<time><cr>", impulso 500-2500 us, risoluzione 1 us.

### Cited Findings

**SSC-32 originale**
- "DB9 Port: True RS232 level serial connector"; "TTL Serial Port: For connecting to Atom, Stamp etc. and DB9 enable" — [primary] [manuale SSC-32 Ver 2.0, pag. 2](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- "This is the TTL serial port or DB9 serial port enable. Install two jumpers as illustrated below to enable the DB9 port. Install wire connectors to utilize TTL serial communication from a host microcontroller." — [primary] [stesso, pag. 3, voce 13](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Ponticelli BAUD: "0 0 = 2400; 0 1 = 9600; 1 0 = 38.4k; 1 1 = 115.2k"; "Baud rate 38.4k for Basic Atom use", "Baud rate 115.2k for PC use" (serigrafia: "00:2400 01:9600 10:38.4 11:115.2") — [primary] [stesso, pag. 2-3](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- LED: acceso fisso all'accensione, si spegne al primo comando valido, poi lampeggia in ricezione: "The green LED is not a power indicator, but a status indicator." — [primary] [stesso, pag. 3 e 12](https://hobbielektronika.hu/forum/getfile.php?id=81561).

**SSC-32U**
- "There are three ways to communicate with the SSC-32U board: USB, TTL UART, and XBee socket. We recommend only using one, but USB will have priority if multiple are used." — [primary] [guida SSC-32U, pag. 19](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- "The three pins behind the FTDI chip are Tx, Rx and GND ... connect the Tx pin on the microcontroller to the Rx pin on the SSC-32U, the Rx pin on the microcontroller to the Tx pin on the SSC-32 and GND to GND." — [primary] [stesso, pag. 12](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- "The SSC-32U is shipped with a default Baud rate of 9600." Pulsante: tenendolo premuto i LED mostrano il baud corrente: "9600 (green); 38400 (red); 115200 (both green and red); Non-standard Baud rate (no LEDs)"; dopo 2 s i LED si alternano; rilasciare; premere per scorrere; dopo 5 s "the new baud rate will be written to EEPROM" — [primary] [stesso, pag. 34](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Baud via registro: "Register R4 now holds the Baud rate ... it stores the value divided by 10 ... to set to 2400 Baud, issue the command R4=240"; lettura con "R4<cr>" — [primary] [stesso, pag. 34-35](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- "Baud speeds: 9600, 38.4k, and 115.2k selectable via push button; other speeds through register configuration"; formato "N81" — [primary] [scheda RB-LYN-850, pag. 3](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf).
- LED A/B: "Both ON at power-up before a byte is received. Green flashes when a valid byte is received. Red flashes when an invalid byte is received (framing error)." — [primary] [guida SSC-32U, pag. 13](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Ritardi di risposta: registro 1 "Transmit Delay" predefinito 600 us; registro 2 "Transmit Pacing" predefinito 70 us tra i byte — [primary] [stesso, pag. 36](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).

**Clone V2.5 (venditore)**
- Procedura baud identica alla SSC-32U; LED: "Una luce [A] su significa 9600; B luce su significa 38400; Le luci A e B sono on allo stesso tempo 115200 (di base)" (traduzione automatica; "di base" = predefinito) — [secondary] [AliExpress](https://it.aliexpress.com/item/1005001887832328.html).
- "Quando si collega ad ARDUINO, il TX della scheda di controllo servo e' collegato al numero 0; RX e' collegato al numero 1; GND e' collegato"; esempio con Serial a 115200 e comandi "#0P750T500" / "#0P2200T500" — [secondary] [AliExpress](https://it.aliexpress.com/item/1005001887832328.html).
- DISACCORDO: baud di fabbrica 9600 sulla SSC-32U Lynxmotion ([primary] [guida pag. 34](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf)) contro 115200 dichiarato dal venditore del clone ([secondary] [AliExpress](https://it.aliexpress.com/item/1005001887832328.html)): il valore reale va letto sul pezzo tenendo premuto il pulsante BAUD.

**Protocollo (uguale nei due manuali Lynxmotion)**
- "With the exception of MiniSSC-II mode, all SSC-32 commands must end with a carriage return character (ASCII 13) ... Commands of different types cannot be mixed in the same command group ... numeric arguments ... must be ASCII strings of decimal numbers ... ASCII format is not case sensitive ... Spaces, tabs, and line feeds are ignored." — [primary] [manuale SSC-32 Ver 2.0, pag. 5](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Movimento: "# <ch> P <pw> S <spd> ... # <ch> P <pw> S <spd> T <time> <cr>"; "<ch> = Channel number in decimal, 0 - 31"; "<pw> = Pulse width in microseconds, 500 - 2500"; "<spd> = Movement speed in uS per second for one channel (Optional)"; "<time> = Time in mS for the entire move, affects all channels, 65535 max (Optional)"; "<esc> = Cancel the current command, ASCII 27" — [primary] [stesso, pag. 5](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Group move: "#5 P1600 #10 P750 T2500 <cr>" — "The servos will both start and stop moving at the same time." — [primary] [stesso, pag. 5](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Primo comando: "Don't issue a speed or time command to the servo controller as the first instruction. It will assume it needs to start at 500uS and will zip there as quickly as possible. The first positioning command should be a normal '# <ch> P <pw>' command." — [primary] [stesso, pag. 6](https://hobbielektronika.hu/forum/getfile.php?id=81561). Sulla SSC-32U: "it will ignore speed and time commands until the first normal command has been received" — [primary] [guida SSC-32U, pag. 25](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Risoluzione: "A position value of 500 corresponds to 0.50mS pulse, and a position value of 2500 corresponds to a 2.50mS pulse. A one unit change in position value produces a 1uS (microsecond) change in pulse width. The positioning resolution is 0.09°/unit (180°/2000)."; impulsi "repeated 50 times a second (every 20mS)" — [primary] [manuale SSC-32 Ver 2.0, pag. 4](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- "Generally, micro servos are not able to move the entire 180° range." — [primary] [stesso, pag. 4](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Offset: "# <ch> PO <offset value>", da −100 a 100 us; sulla SSC-32U si perde allo spegnimento salvo usare i registri 32-63 — [primary] [manuale SSC-32 pag. 6](https://hobbielektronika.hu/forum/getfile.php?id=81561); [guida SSC-32U pag. 26 e 36](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Query: "Q <cr> — This will return a '.' if the previous move is complete, or a '+' if it is still in progress. There will be a delay of 50uS to 5mS before the response is sent."; "QP <arg> <cr> — return a single byte (in binary format) indicating the pulse width of the selected servo with a resolution of 10uS"; "VER <cr> — Returns the software version number as an ASCII string." — [primary] [manuale SSC-32 Ver 2.0, pag. 7 e 10](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Altri comandi: uscite discrete "#<ch>H / #<ch>L", byte "#<bank>:<value>", ingressi digitali "A B C D AL BL CL DL", analogici "VA VB VC VD" (8 bit, 255 = 4.98 V), sequencer esapode a 12 servo (canali 0-5 e 16-21), "GOBOOT", emulazione MiniSSC-II binaria a 3 byte — [primary] [stesso, pag. 6-10](https://hobbielektronika.hu/forum/getfile.php?id=81561). Solo SSC-32U: ingressi A-H, "STOP <n>", registri "R<r>=<n>", "RDFLT", stringa di avvio "SSCAT / SSDEL / SS", registri 64-95 "Initial Pulse Width" — [primary] [guida SSC-32U, pag. 33-40](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- DISACCORDO interno alla guida SSC-32U sull'unita' di T: a pag. 24 "<time>: time in microseconds", ma l'esempio a pag. 25 dice "T2500 ... 2500 milliseconds (2.5 seconds)" e il manuale SSC-32 dice "Time in mS". L'unita' corretta e' il millisecondo — [primary] [guida SSC-32U pag. 24-25](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf) contro [manuale SSC-32 pag. 5](https://hobbielektronika.hu/forum/getfile.php?id=81561).

### Inferences
- Un esapode a 18 GDL non puo' usare il sequencer integrato (12 servo, 2 GDL per zampa): servono group move calcolati dall'ESP32.
- La scheda non emette impulsi finche' non riceve il primo comando di posizione: il firmware ESP32 deve mandare per primo un "#chPpw" senza T ne' S per ogni canale, altrimenti i servo scattano (SSC-32) o il comando viene ignorato (SSC-32U).
- Con USB collegato a un PC la SSC-32U da' priorita' all'USB: durante l'uso con l'ESP32 sui pin TTL il cavo USB della scheda servo va scollegato.

### Gaps
- Frequenza reale del quarzo e quindi errore di baud a 115200 (SSC-32: "14.75 MHz" da inserzione, NON VISTO SULLA FONTE; clone: sconosciuta): NON TROVATO da fonte primaria.
- Dimensione del buffer di ricezione seriale: NON TROVATO.
- Conferma che il firmware del clone accetti tutti i comandi Lynxmotion (Q, QP, VER, registri R): NON TROVATO; il venditore mostra solo "#0P750T500".

---

## 5. Compatibilita' dei livelli con ESP32-S3 (I/O a 3.3 V, non tolleranti 5 V)

### Takeaway
ESP TX (3.3 V) → SSC RX (ATmega a 5 V): NON garantito dai datasheet (VOH minimo ESP 2.64 V < VIH minimo ATmega 3.0 V), anche se un'uscita CMOS a vuoto sta a circa 3.3 V e in pratica di solito funziona con circa 0.3 V di margine. SSC TX (5 V) → ESP RX: collegamento diretto NON ammesso (VIH massimo ESP = 3.6 V): serve un partitore (10 kΩ in serie + 20 kΩ verso massa → 3.33 V) oppure un traslatore di livello. Soluzione robusta: modulo traslatore a 4 canali su entrambe le linee; in alternativa collegare solo ESP TX → SSC RX se non si usano le query.

### Cited Findings
- ATmega48/88/168, Tabella 33-2: "VIH Input High Voltage, except XTAL1 and RESET pins: VCC = 2.4V - 5.5V → Min 0.6 VCC, Max VCC + 0.5"; "VIL ...: VCC = 2.4V - 5.5V → Max 0.3 VCC"; "VOH ... IOH = -20mA, VCC = 5V → Min 4.2 V"; "VOL ... IOL = 20mA, VCC = 5V → Max 0.9 V"; massimi assoluti "Voltage on any Pin except RESET with respect to Ground: -0.5V to VCC+0.5V" — [primary] [datasheet Atmel-2545W ATmega48/V/88/V/168/V, pag. 383-384](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2545-8-bit-AVR-Microcontroller-ATmega48-88-168_Datasheet.pdf).
- ATmega328P (micro della SSC-32U), Tabella 28.2 (VCC = 2.7-5.5 V): "Input high voltage, except XTAL1 and RESET pins: Min 0.6 VCC, Max VCC + 0.5"; "Input low voltage: Max 0.3 VCC"; "Output high voltage: IOH = −20mA, VCC = 5V → Min 4.1 V"; "Output low voltage: IOL = 20mA, VCC = 5V → Max 0.8 V"; nota 2: ""Min" means the lowest value where the pin is guaranteed to be read as high" — [primary; datasheet della versione automotive 7810D, l'unica di dimensione scaricabile: stessa soglia 0.6 VCC dell'ATmega168] [ATmega328P datasheet 7810D-AVR-01/15, pag. 258-259](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf).
- ESP32-S3, Tabella 5-4 "DC Characteristics (3.3 V, 25 °C)": "VIH High-level input voltage: Min 0.75 × VDD, Max VDD + 0.3 V"; "VIL: Max 0.25 × VDD"; "VOH High-level output voltage: Min 0.8 × VDD"; "VOL: Max 0.1 × VDD"; "IOH ... 40 mA (typ)"; nota 2: "VOH and VOL are measured using high-impedance load"; "CIN Pin capacitance 2 pF (typ)" — [primary] [ESP32-S3 Series Datasheet v2.2, pag. 65](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf).
- ESP32-S3, Tabella 5-1 "Absolute Maximum Ratings": "Input power pins: Allowed input voltage −0.3 ... 3.6 V" (la tabella non da' un massimo separato per i GPIO) — [primary] [stesso, pag. 64](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf).
- La SSC-32U ha uno zoccolo XBee dichiarato a 3.3 V: "Serial input: USB, 3.3V Xbee, TTL UART, N81" — [primary] [scheda RB-LYN-850, pag. 3](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf).
- Le uscite logiche della scheda sono a 5 V: "output a High (+5v) on channel 3" — [primary] [manuale SSC-32 Ver 2.0, pag. 6](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Forum RobotShop, SSC-32U ↔ Raspberry Pi: "The 5.0 V DC output (TX) from the SSC-32U can (and most certainly will/already has) damage the RPi's RX pin since it cannot accept more than 3.3 V DC" — [community, citazione riportata dal motore di ricerca; thread non leggibile direttamente (403), autore non verificato] [community.robotshop.com](https://community.robotshop.com/forum/t/ssc32u-to-raspbian-communication-uart/68610).
- Un progetto Hackaday collega una SSC-32U a un Raspberry Pi attraverso un traslatore di livello SparkFun — [community, riassunto del motore di ricerca: NON VISTO SULLA FONTE] [hackaday.io/project/10344](https://hackaday.io/project/10344/instructions).
- Calcoli — [computed]:
  - VIH minimo ATmega a VCC = 5.00 V: 0.6 × 5.00 = 3.00 V (a 5.25 V: 3.15 V; a 4.75 V: 2.85 V).
  - VOH minimo ESP32-S3 a VDD = 3.3 V: 0.8 × 3.3 = 2.64 V.
  - Margine garantito sul livello alto = 2.64 − 3.00 = −0.36 V → NON garantito. Margine tipico con uscita a vuoto ≈ 3.3 − 3.0 = +0.3 V.
  - Livello basso: VOL max ESP = 0.1 × 3.3 = 0.33 V < VIL max ATmega = 0.3 × 5 = 1.5 V → garantito, margine 1.17 V.
  - SSC TX alto ≈ 5 V contro VIH massimo ESP = 3.3 + 0.3 = 3.6 V → circa 1.4 V di troppo: diretto NON ammesso.
  - Partitore R1 = 10 kΩ (in serie, dal TX della SSC), R2 = 20 kΩ (verso massa): Vout = 5.00 × 20/(10+20) = 3.33 V; con 5.25 V → 3.50 V (< 3.6 V); soglia alta ESP = 0.75 × 3.3 = 2.475 V → margine 0.86 V.
  - Variante con valori E12: R1 = 10 kΩ, R2 = 18 kΩ → 5.00 × 18/28 = 3.21 V (con 5.25 V → 3.375 V).
  - Velocita': 10k∥20k = 6.67 kΩ; con 50 pF (pin + cavo, valore assunto) τ = 6.67e3 × 50e-12 = 0.33 us; un bit a 115200 dura 1/115200 = 8.68 us → τ ≈ 4 % del bit.

**Traslatore di livello acquistabile dall'Italia**
- Adafruit "4-channel I2C-safe Bi-directional Logic Level Converter - BSS138", codice 757 — [primary] [adafruit.com/product/757](https://www.adafruit.com/product/757). Rivenditori UE/IT comparsi nei risultati (prezzi e giacenze NON VISTI SULLA FONTE): [Melopero (Italia)](https://www.melopero.com/?p=8086); [Farnell, codice 2301651](https://ie.farnell.com/adafruit/757/logic-level-converter-4ch-arm/dp/2301651) "€3.90" IVA esclusa; [buyzero.de](https://buyzero.de/en/products/4-channel-i2c-safe-bi-directional-logic-level-converter-bss138) "5,69 €" IVA inclusa; RS/Distrelec codice 300-91-221 "temporarily out of stock" — [secondary, riassunto del motore di ricerca].

### Inferences
- "Garantito?" No. "Funziona di solito?" Si', ma con circa 0.3 V di margine su un robot con 18 servo che sporcano le alimentazioni: per un progetto che deve funzionare al primo colpo e' giustificato un traslatore (lato alto alimentato dai 5 V della scheda servo, lato basso dai 3.3 V dell'ESP32).
- Le query (Q, QP, VER) sono l'unico motivo per collegare SSC TX → ESP RX. Con MG90S senza feedback si puo' temporizzare lato ESP32 e lasciare quel filo scollegato: sparisce il rischio dei 5 V sull'ESP32.
- Zoccolo XBee a 3.3 V della SSC-32U: indica che la scheda Lynxmotion prevede gia' una seriale a 3.3 V su quei pin e potrebbe essere un punto di collegamento senza traslatore; lo schema elettrico pero' non e' stato letto e sul clone non c'e' alcuna garanzia. Da considerare solo dopo verifica con il tester.
- Livelli del clone: dipendono dalla tensione a cui gira il suo microcontrollore (5 V se copia la Lynxmotion; il venditore lo collega direttamente a un Arduino a 5 V). Misurare la tensione a riposo sul pin TX prima di collegarlo all'ESP32.

### Gaps
- Schema elettrico della SSC-32U (percorso del pin RX, eventuali resistenze serie, traslatore sullo zoccolo XBee): NON LETTO (wiki 403).
- Dichiarazione ufficiale Lynxmotion sulla compatibilita' a 3.3 V del pin RX: NON TROVATA.
- Tensione logica reale del clone: NON TROVATO.

---

## 6. Baud rate consigliato e tempo di invio di un group move a 18 servo

### Takeaway
Consigliato 115200 baud, 8N1: un group move da 18 servo e' una stringa di circa 140 byte, cioe' circa 12 ms a 115200 (meno di un periodo servo da 20 ms) contro circa 36.5 ms a 38400 (quasi due periodi) e circa 146 ms a 9600 (valore di fabbrica della SSC-32U Lynxmotion, da cambiare).

### Cited Findings
- Formato del comando e terminatore — [primary] [manuale SSC-32 Ver 2.0, pag. 5](https://hobbielektronika.hu/forum/getfile.php?id=81561). Formato "N81" (1 start + 8 dati + 1 stop = 10 bit per byte) — [primary] [scheda RB-LYN-850, pag. 3](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf).
- Lunghezza della stringa — [computed]: senza spazi, canali 0-8 (9 servo su VS1) e 16-24 (9 servo su VS2), impulsi a 4 cifre:
  - "#0P1500" = 7 byte × 9 = 63; "#16P1500" = 8 byte × 9 = 72; "T100" = 4 byte (fino a "T65535" = 6); CR = 1.
  - Totale = 63 + 72 + 4 + 1 = 140 byte (142 con T a 5 cifre; caso peggiore con tutti i canali a 2 cifre: 18 × 8 + 6 + 1 = 151 byte).
- Tempo = byte × 10 bit / baud — [computed]:
  - 9600: 140 × 10 / 9600 = 145.8 ms
  - 38400: 140 × 10 / 38400 = 36.5 ms (151 byte → 39.3 ms)
  - 115200: 140 × 10 / 115200 = 12.2 ms (151 byte → 13.1 ms)
- Frequenza massima = 1 / tempo — [computed]: 38400 → circa 27 comandi/s; 115200 → circa 82 comandi/s; il periodo servo e' 20 ms = 50 Hz ([manuale SSC-32 pag. 4](https://hobbielektronika.hu/forum/getfile.php?id=81561)).
- 115200 e' un baud standard su tutte le schede: ponticelli "1 1" sulla SSC-32; LED verde + rosso sulla SSC-32U; LED A + B sul clone, dove sarebbe il valore predefinito — [primary] [manuale SSC-32 pag. 3](https://hobbielektronika.hu/forum/getfile.php?id=81561); [primary] [guida SSC-32U pag. 34](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf); [secondary] [AliExpress](https://it.aliexpress.com/item/1005001887832328.html).

### Inferences
- A 38400 la stringa occupa quasi due periodi servo: funziona ma limita il ciclo di controllo a circa 25 Hz; a 115200 si arriva a 50 Hz con margine.
- Il group move parte solo alla ricezione del CR: il tempo di trasmissione e' un ritardo puro, uguale per tutti i servo, non uno sfasamento tra zampe.
- Se a 115200 compaiono errori (LED rosso "framing error" sulla SSC-32U), ripiegare su 38400.

### Gaps
- Errore di baud reale a 115200 delle tre schede: NON TROVATO.

---

## 7. I morsetti e le piste reggono picchi di circa 15 A? Pratica comune per 18 servo

### Takeaway
Lynxmotion dichiara 15 A di picco PER LATO (VS1 e VS2 separatamente) e raccomanda 3-5 A continui per lato; per il clone non esiste alcun dato di corrente. Con 18 MG90S: 9 servo per banco (canali 0-8 su VS1, 16-24 su VS2), alimentazione servo portata a ENTRAMBI i morsetti con due coppie di fili dalla stessa sorgente, logica su VL. Cosi' il caso peggiore (tutti in stallo) e' circa 8.5 A per lato.

### Cited Findings
- "VS peak current: max 15 amps per side"; "VS steady current: max 3-5 amps per side recommended" — [primary] [scheda RB-LYN-850, pag. 3-4](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf).
- "There are two jumpers (rather than just one) because of the current involved." — [primary] [guida SSC-32U, pag. 16](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- Quando togliere i ponticelli VS1=VS2: "A second battery is needed because of high current; Second set of servos operate at a different voltage; Want to use two separate packs for power" — [primary] [stesso, pag. 16](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf).
- "If the wires carrying the current are too small, or connections are made with stripped and twisted wire, or cheap plastic battery holders are used, the same problem may occur." — [primary] [manuale SSC-32 Ver 2.0, pag. 12](https://hobbielektronika.hu/forum/getfile.php?id=81561).
- Clone: "When the VS1 and VS2 jumper caps are shorted, only one input can be connected." — [secondary] [immagine alimentazione](https://ae-pic-a1.aliexpress-media.com/kf/Ha46454e5bac543578df26442fdabaa8bB.jpg).
- Stallo MG90S (dalla ricerca parallela sui servo, file servo_mg90s.md): 860 mA ±10 % a 6.0 V per servo (datasheet di un clone), 18 × 0.946 = 17.0 A con tutti in stallo; in movimento 0.12-0.25 A per servo — [secondary] [datasheet Sky Star MG90S](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf).
- Ripartizione 9 + 9 — [computed]: stallo simultaneo per lato = 9 × 0.946 = 8.5 A (< 15 A di picco per lato); camminata tipica per lato = 9 × 0.12...0.25 = 1.1...2.3 A (< 3-5 A continui per lato). Tutti i 18 su un solo morsetto: 17.0 A di picco (> 15 A).
- Pratica riportata su forum/blog RobotShop — [community; citazioni restituite dal motore di ricerca, NON VISTE SULLA FONTE]:
  - meta' dei servo sui canali 0-15 e meta' sui canali 16-31 — [Guide to the Power Supply Options for Lynxmotion Controllers](https://community.robotshop.com/blog/show/guide-to-the-power-supply-options-for-lynxmotion-controllers);
  - limite "about 15A per side (VS1 and VS2)" — [Max amp draw from ssc-32](https://community.robotshop.com/forum/t/max-amp-draw-from-ssc-32/18267);
  - per carichi pesanti "two pair of wires from the supply into VS1 and VS2 individually"; i cavetti jumper comuni non reggono circa 2 A continui — [SSC-32 Powering Options](https://community.robotshop.com/forum/t/ssc-32-powering-options/15869/59);
  - un esapode a 18 servo (taglia standard, non micro) assorbe "around 6-8 amps when walking" — [Max number of servos that can be run simultaneously on SSC](https://community.robotshop.com/forum/t/max-number-of-servos-that-can-be-run-simultaneously-on-ssc/17305);
  - con due sorgenti distinte togliere i ponticelli VS1=VS2 PRIMA di collegare la seconda ("Not doing so will most likely kill the weakest of the two supplies") e alimentare VL a parte contro i brownout — [Power jumpers for SSC-32](https://community.robotshop.com/forum/t/power-jumpers-for-ssc-32/18510);
  - alimentare la logica dal BEC di un controller motori e' sconsigliato — [SSC32 and BEC from motor-controller](https://community.robotshop.com/forum/t/q-ssc32-and-bec-from-motor-controller/17165).

### Inferences
- Su una Lynxmotion vera, 9 + 9 servo con due alimentazioni ai morsetti restano dentro i dati dichiarati sia in stallo (8.5 A contro 15 A di picco per lato) sia in camminata (1-2.3 A contro 3-5 A continui).
- Con VS1 e VS2 alimentati dalla STESSA sorgente i ponticelli VS1=VS2 sono elettricamente superflui; i divieti dei manuali riguardano due sorgenti diverse in parallelo. Con due regolatori separati (uno per lato) i ponticelli vanno obbligatoriamente tolti.
- Per il clone, senza dati su piste e morsetti, e' prudente trattare 3-5 A continui per lato come limite e non contare sui 15 A di picco. Alternativa conservativa: distribuzione di potenza esterna (V+ e massa dei servo su una barra separata, alla scheda solo segnale e massa di riferimento).

### Gaps
- Portata nominale del blocco morsetti a vite, dei ponticelli e delle piste VS: NON TROVATO.
- Prove di terzi sulla corrente sopportata dal clone V2.5: NON TROVATO.
- Misure di corrente di un esapode a 18 micro servo alimentato attraverso una SSC-32: NON TROVATO.

---

## 8. Disponibilita' e acquisto dall'Italia (ottobre 2026)

### Takeaway
La SSC-32 originale e' fuori produzione. La SSC-32U (RB-Lyn-850) risulta ancora in vendita da RobotShop EU; il clone "SSC32-V2.5" e' disponibile su AliExpress a 28,19 EUR e non disponibile su Amazon.it.

### Cited Findings
- Clone su AliExpress: 28,19 EUR IVA inclusa, "47 disponibili", spedizione gratuita, consegna 18-26 ottobre, venditore "superior RC parts" (92.0 % recensioni positive) — [secondary, letto nel browser l'8/10/2026] [it.aliexpress.com/item/1005001887832328](https://it.aliexpress.com/item/1005001887832328.html).
- Clone su Amazon.it: "Non disponibile" — [secondary, letto nel browser l'8/10/2026] [amazon.it/dp/B0FM8S6W59](https://www.amazon.it/dp/B0FM8S6W59).
- SSC-32U su RobotShop EU (RB-Lyn-850): "€51.80" tasse incluse, 12 pezzi disponibili — [secondary, riassunto del motore di ricerca con data di rilevazione ignota: NON VISTO SULLA FONTE (sito 403)] [eu.robotshop.com](https://eu.robotshop.com/products/lynxmotion-ssc-32u-usb-servo-controller).
- SSC-32U da mybotshop.de: "€ 64,95" IVA 19 % inclusa, "Must be ordered. Ready for shipment in 21 days after order", articolo MBS-SSC32, GTIN 0756832455524 — [secondary, riassunto automatico della pagina, 8/10/2026] [mybotshop.de](https://www.mybotshop.de/Lynxmotion-SSC-32U-Servocontrollerboard_1).
- SSC-32 originale: fuori produzione, sostituita dalla SSC-32U — [secondary, NON VISTO SULLA FONTE] [RobotShop SSC-32](https://www.robotshop.com/products/lynxmotion-ssc-32-servo-controller).

### Gaps
- Prezzo e giacenza RobotShop EU verificati direttamente: NON TROVATO (sito non leggibile dai robot).

---

## Solo l'utente puo' rispondere
1. Foto nitida di entrambe le facce della scheda, oppure il link d'acquisto: stabilisce se e' Lynxmotion SSC-32, SSC-32U o clone "V2.5".
2. Misure col calibro: lati del PCB, interasse dei 4 fori nei due sensi, diametro dei fori, spessore del PCB, altezza del componente piu' alto, sporgenza del connettore USB dal bordo, posizione e ingombro del blocco morsetti.
3. Sigle stampate su: microcontrollore, regolatore a 5 V, chip USB-seriale, quarzo.
4. Ordine di + e − sulla serigrafia del blocco morsetti (VS1, VL, VS2).
5. Tensione a riposo sul pin TX della scheda rispetto a GND con la sola logica alimentata: 5 V o 3.3 V?
6. Baud impostato (tenere premuto il pulsante BAUD e leggere i LED A/B) e risposta ai comandi "VER" e "R4" seguiti da invio.
7. Peso della scheda sulla bilancia.
