# Tower Pro MG90S micro servo: limiti elettrici, corrente di stallo, millerighe, squadrette, cavo

Data ricerca: 8 ottobre 2026. Etichette fonte: **[primary]** = produttore (pagina prodotto / datasheet del produttore), **[secondary]** = negozio, blog, wiki, datasheet non ufficiale, **[3rd-meas]** = misura di terzi, **[community]** = forum/opinione, **[computed]** = calcolo mio (formula indicata).

Nota di metodo: i due PDF (datasheet "MG90S_Tower-Pro.pdf" e datasheet Sky Star) sono stati letti integralmente come PDF, non da snippet. Le pagine Amazon / eBay / AliExpress hanno risposto 403/500/503 al fetch: i dati su quei prodotti vengono solo da snippet di ricerca e hanno affidabilita' bassa. "Datasheet Tower Pro" in rete NON e' un documento Tower Pro: e' un foglio di 2 pagine anonimo, ospitato da rivenditori.

Nota di ripresa (stesso giorno, 8 ottobre 2026): il file e' stato ricontrollato contro le domande chiave e integrato con 9 chiamate web aggiuntive mirate ai punti deboli (millerighe, vite squadretta, squadrette metalliche, fori alette, sezione fili, test a 2S). Esito: nuove evidenze solo su millerighe e foro vite (sezione 4); nessuna nuova evidenza su squadrette metalliche, fori alette, AWG, test a 2S. Pagine non raggiungibili anche in ripresa: community.robotshop.com (403), makerworld.com (403), rcgroups.com (402, a pagamento). I dati MakerWorld e RobotShop della sezione 4 vengono quindi dal riassunto del motore di ricerca e NON dalla pagina letta: affidabilita' bassa, da confermare col calibro.

---

## 1. Specifiche ufficiali Tower Pro (pagina prodotto e datasheet PDF)

### Takeaway
La pagina ufficiale towerpro.com.tw dichiara "Operating voltage: 4.8V", coppia 1.8 kg/cm a 4.8 V e 2.2 kg/cm a **6.6 V**, dead band 1 us, cavo 25 cm; il PDF "datasheet" che circola (non ufficiale) dice invece 4.8-6.0 V, 2.2 kgf·cm a 6 V e dead band 5 us. La pagina ufficiale NON riporta angolo di rotazione ne' range di impulso.

### Cited Findings
Pagina ufficiale Tower Pro (citazioni testuali):
- "Weight: 13.4g" — [primary] [towerpro.com.tw/product/mg90s-3](https://www.towerpro.com.tw/product/mg90s-3/)
- "Dimension: 22.8×12.2×28.5mm" — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- "Stall torque: 1.8kg/cm (4.8V); 2.2kg/cm (6.6V)" — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- "Operating speed: 0.10sec/60degree (4.8V); 0.08sec/60degree (6.0V)" — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- "Operating voltage: 4.8V" (un solo valore, nessun range) — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- "Temperature range: 0℃_ 55℃" — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- "Dead band width: 1us" — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- "servo wire length: 25 cm"; "Servo Plug: JR (Fits JR and Futaba)"; "servo arms &screws included" — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- "We have upgraded our servo gear set and shaft to aluminum 6061-T6." / "It is stronger and lighter than copper." — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- "PRODUCT CONFIGURE TABLE": Weight 13.4 g; Torque (4.8 V) 1.8 kg; Speed 0.1 sec/60deg; A 32.5 mm; B 22.8 mm; C 28.4 mm; D 12.4 mm; E 32.1 mm; F 18.5 mm — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- Categoria prodotto: "Mini Servo 11-20g" — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)

Datasheet PDF "MG90S_Tower-Pro.pdf" (2 pagine, anonimo, NON Tower Pro; letto integralmente):
- "Weight: 13.4 g"; "Dimension: 22.5 x 12 x 35.5 mm approx."; "Stall torque: 1.8 kgf·cm (4.8V ), 2.2 kgf·cm (6 V)"; "Operating speed: 0.1 s/60 degree (4.8 V), 0.08 s/60 degree (6 V)"; "Operating voltage: 4.8 V - 6.0 V"; "Dead band width: 5 µs" — [secondary] [electronicoscaldas.com PDF](https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf)
- "Servo can rotate approximately 180 degrees (90 in each direction)"; "It comes with a 3 horns (arms) and hardware"; "Metal gear with one bearing" — [secondary] [PDF](https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf)
- Figura: "20 ms (50 Hz) PWM Period", "1 - 2 ms Duty Cycle", "4.8 - 6 V Power and Signal"; "Position "0" (1.5 ms pulse) is middle, "90" (~2 ms pulse) is all the way to the right, "-90" (~1 ms pulse) is all the way to the left." — [secondary] [PDF](https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf)
- Quote del disegno: 35.5 (altezza con squadretta), 21, 11, 22.5, 32.5, 12 mm — [secondary] [PDF](https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf)

Datasheet di un produttore di cloni (Shenzhen Sky Star Technology, venduto da TinyTronics come "TianKongRC"; letto integralmente):
- Size 22.4*12.1*22.8 mm; Weight 13.5 g ±5%; Limit angle 200° ±5°; Bearing: NO; Case PBT; Motor: carbon brush motor; Operating temperature -25..70 °C — [primary del clone] [Sky Star datasheet PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- Pulse width range 500~2500 usec; Neutral 1500 usec; Running degree 180° ±3° (500~2500 usec); Dead band 5 usec; Amplifier: Analog controller; Rotating direction: Counterclockwise (1000~2000 usec) — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- No load speed 0.12 sec/60° (4.8 V), 0.09 sec/60° (6.0 V); Peak stall torque 1.8 kg.cm (4.8 V), 2.0 kg.cm (6.0 V) — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- Disegno clone: 22.4 (corpo), 27.7 (interasse fori alette), 31.8 (lunghezza sulle alette), 12.5 (larghezza), 22.8 (altezza corpo), 19.8, 32.9 (altezza totale con squadretta) — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)

Altre schede:
- ServoDatabase: Modulation Analog; 2.20 kg-cm @6.0 V, 1.80 kg-cm @4.8 V; 0.08 / 0.10 s/60°; 13.4 g; 22.8×12.2×28.5 mm; range 180°; pulse 1000-2000 us (neutro 1500); JR, filo 250 mm; stall current ≤0.7 A; spline 20 T — [secondary] [servodatabase.com](https://servodatabase.com/servo/towerpro/mg90s)
- Vorpal wiki riporta per il genuino "Voltage: 4.8 V to 6.6 V" — [secondary] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)
- Botland (PL): alimentazione 4.8-6.0 V, 1.8 / 2.2 kg·cm, 22.8×12.2×28.5 mm, 13.4 g, "analogue" — [secondary] [botland.store](https://botland.store/micro-servos/24408-towerpro-mg90s-micro-analogue-servo-with-metal-gear.html)

### Disaccordi tra fonti (non risolti)
- **Tensione massima**: 6.6 V (Tower Pro, come tensione a cui e' data la coppia 2.2 kg/cm; Vorpal) contro 6.0 V (PDF non ufficiale, ServoDatabase, Botland, Sky Star).
- **Dead band**: 1 us (Tower Pro) contro 5 us (PDF non ufficiale, Sky Star).
- **Analogico / digitale**: Vorpal descrive il genuino come digitale (nel testo estratto dalla pagina Tower Pro la parola "digital" non compare; il dead band di 1 us e' coerente con un digitale, ma e' una mia deduzione); ServoDatabase e Botland scrivono "Analog"; i cloni sono analogici.
- **Temperatura**: 0-55 °C (Tower Pro) contro -25..70 °C (Sky Star clone).
- **Range impulso**: 1-2 ms per ±90° (PDF non ufficiale) contro 500-2500 us per 180° (Sky Star). Un utente ServoDatabase ha dovuto usare `attach(9,550,1500)` per avere la corsa completa — [community] [servodatabase.com](https://servodatabase.com/servo/towerpro/mg90s)
- **Cuscinetto**: "one bearing" (PDF non ufficiale, ServoDatabase) contro "Bearing: NO" (Sky Star clone).

### Inferences
- Le lettere A-F della tabella Tower Pro non sono spiegate nel testo (stanno su un disegno non leggibile). Confrontandole col modello STEP dell'utente: A 32.5 ≈ lunghezza sulle alette (STEP 32.2), B 22.8 ≈ lunghezza corpo (STEP 22.6), D 12.4 ≈ larghezza (STEP 12.2), E 32.1 ≈ altezza fino in cima al millerighe (STEP 32.25), F 18.5 ≈ quota sotto-aletta (STEP 18.4). E' una mia attribuzione, non dichiarata da Tower Pro.
- Un servo "MG90S" comprato a caso si comportera' piu' probabilmente come il datasheet Sky Star (analogico, 5 us, 500-2500 us) che come la pagina Tower Pro.

### Gaps
- Angolo di rotazione, range d'impulso e periodo: **NON TROVATO** su fonte Tower Pro ufficiale.
- Un datasheet PDF firmato Tower Pro: **NON TROVATO**.

---

## 2. Un 2S LiPo (7.4 V nominali / 8.4 V carico) e' dentro le specifiche?

### Takeaway
No. 8.4 V e' il 40 % sopra il massimo di 6.0 V e il 27 % sopra il 6.6 V della pagina Tower Pro; anche a batteria scarica (6.4 V) si e' sopra 6.0 V. Nessuna fonte dichiara l'MG90S adatto al 2S diretto: serve un regolatore (BEC / buck) a 5-6 V. Non ho trovato un test documentato con misure di un MG90S a 7.4-8.4 V.

### Cited Findings
- Massimo dichiarato 6.0 V — [secondary] [PDF non ufficiale](https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf); [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- Valore piu' alto mai citato dal produttore: 6.6 V (tensione di riferimento della coppia 2.2 kg/cm) — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- Con 5 pile AA (max stimato 7.2 V, non misurato) due SG90 hanno emesso odore di bruciato "immediately upon applying power"; chip di controllo fuso, case rigonfio. L'autore si era basato su una prova precedente con un MG90S e avverte che l'elettronica varia da lotto a lotto — [3rd-meas, aneddoto senza misure] [newscrewdriver.com](https://newscrewdriver.com/2021/03/21/aftermath-of-exceeding-sg90-micro-servo-six-volt-maximum/)
- Lo stesso autore ha poi scelto un buck MP1584 regolato a 5.4 V alimentato da 2S — [community] [newscrewdriver.com](https://newscrewdriver.com/2021/03/24/configurable-micro-sawppy-servo-power-supply)
- FAQ di un rivenditore: un 2S "will likely burn out the motor", usare un BEC a 6 V — [secondary, non misurato] [probots.co.in](https://probots.co.in/mini-servo-motor-mg90s-metal-gear-for-arduino-rc-planes.html)
- Forum Arduino: "The 7.4V for 2S lipos will be too much" — [community] [forum.arduino.cc](https://forum.arduino.cc/t/how-to-power-mg90s-motors-and-arduino-nano/1001853)

### Calcoli
- 8.4 / 6.0 = 1.40 (+40 %); 7.4 / 6.0 = 1.23 (+23 %); 8.4 / 6.6 = 1.27 (+27 %); 6.4 / 6.0 = 1.07 (+7 %) — [computed]
- Corrente di stallo a 8.4 V se collegato diretto (motore DC, I proporzionale a V): 860 mA × 8.4/6.0 ≈ 1.20 A nominali; potenza dissipata a rotore bloccato × (8.4/6.0)² ≈ ×1.96 — [computed] da [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)

### Inferences
- Con batteria a 6.4 V un buck regolato a 6.0 V ha solo 0.4 V di margine: o si regola a 5.0-5.5 V o si accetta che a fine scarica la tensione servo segua la batteria.

### Gaps
- Test strumentato di un MG90S (genuino o clone) a 7.4 V e 8.4 V con durata e modalita' di guasto: **NON TROVATO**. La frase "ha funzionato a 7.4 V ma non a 8.4 V" compare solo in uno snippet di ricerca attribuito a newscrewdriver e non l'ho ritrovata nel testo delle pagine lette: non usarla come dato.
- Sigla e tensione massima del chip di controllo interno: **NON TROVATO**.
- Discussione RC Groups "TowerPro MG90S Metal Gear Servo? How's it?" (possibile fonte di prove d'uso oltre 6 V, coppia e gioco): pagina a pagamento (HTTP 402), **NON LETTA** — [rcgroups.com](https://www.rcgroups.com/forums/showthread.php?1119040-TowerPro-MG90S-Metal-Gear-Servo-How-s-it)

---

## 3. Corrente di stallo, in movimento e a riposo

### Takeaway
Valore di progetto per lo STALLO: **1.0 A per servo a 6.0 V** (datasheet clone: 860 mA ±10 % = 946 mA max), cioe' 18 A per 18 servo nel caso peggiore; a 4.8-5 V circa 0.83-0.85 A. In movimento sotto carico leggero 0.12-0.25 A per servo. Nessuna misura pubblicata della corrente di un esapode con 18 MG90S in camminata.

### Cited Findings
- Stall current 750 mA ±10 % a 4.8 V; 860 mA ±10 % a 6.0 V — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- Running current (a vuoto) 90 mA a 4.8 V e 90 mA a 6.0 V; riga "Idle current" presente ma vuota — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- Clone generico a 5 V: idle 10 mA (typical), in movimento 120-250 mA (typical), stallo 700 mA "(measured)" — [3rd-meas, metodo non descritto] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/)
- Versione a rotazione continua, stallo 800 mA misurato a 5 V — [3rd-meas] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s-continuous-rotation/)
- ServoDatabase: stall current ≤0.7 A — [secondary] [servodatabase.com](https://servodatabase.com/servo/towerpro/mg90s)
- TinyTronics: "minimum recommended supply current 0.9 A" per servo — [secondary] [tinytronics.nl](https://www.tinytronics.nl/en/mechanics-and-actuators/motors/servomotors/mg90s-mini-servo)
- Makers Portal (clone, a 5.0 V): ~2.7 mA idle, ~70 mA no load, ~400 mA stall — [secondary, non dichiarato come misura; valore di stallo anomalo] [makersportal.com](http://makersportal.com/shop/p/mg90s-micro-servo)
- Blog del produttore Kpower: fino a 1.2-1.6 A a 6 V, "1.5 A or more" — [secondary, nessun metodo, outlier] [kpower.com](https://www.kpower.com/insight_bldc/7870.html)
- Forum Arduino (18 servo): stima 0.25 A × 18 = 4.5 A; consiglio di mettere a budget 0.75-1.0 A per servo — [community] [forum.arduino.cc](https://forum.arduino.cc/t/powering-18-servos-is-there-a-better-way-to-manage-the-power/1184852)
- Forum Arduino: "900ma at 6V" citato di seconda mano — [community] [forum.arduino.cc](https://forum.arduino.cc/t/best-way-to-power-a-19-servo-robot/898353)

### Calcoli
- Stallo massimo a 6.0 V: 860 × 1.10 = 946 mA → arrotondato a 1.0 A — [computed]
- 18 servo tutti in stallo a 6.0 V: 18 × 0.946 = 17.0 A (18 A con 1.0 A) — [computed]
- Stallo a 5.0 V per interpolazione lineare: 750 + (860−750) × (5.0−4.8)/(6.0−4.8) = 768 mA; +10 % = 845 mA; × 18 = 15.2 A — [computed]
- Stallo a 4.8 V: 750 × 1.10 = 825 mA; × 18 = 14.9 A — [computed]
- Camminata, stima: 18 × 0.12 A = 2.2 A; 18 × 0.25 A = 4.5 A — [computed] da [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/)
- Riposo: 18 × 0.010 A = 0.18 A — [computed] da [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/)

### Inferences
- Media realistica in camminata: 2-4.5 A sul rail servo, con picchi brevi verso 8-10 A quando piu' servo partono o sono caricati insieme. E' una stima, non una misura.
- Tutti i dati di corrente sono di cloni. Vorpal sostiene che i cloni consumino piu' dei genuini, senza numeri — [community] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)

### Gaps
- Corrente di stallo / movimento / riposo dichiarata da Tower Pro: **NON TROVATO**.
- Misura con oscilloscopio (picco di spunto) su MG90S genuino a 6 V: **NON TROVATO**.
- Corrente misurata di un esapode 18× MG90S in camminata: **NON TROVATO**.

---

## 4. Millerighe d'uscita, vite dell'albero, squadrette di serie

### Takeaway
Il numero di denti e' controverso: 20T secondo ServoDatabase e il datasheet Sky Star (20T, Ø 4.9 mm), 21T secondo TinyTronics, Pololu (classe SG90/FS90R), una tabella parametrica MakerWorld (MG90S: 21 denti, Ø 4.80 mm) e i modelli 3D. Il peso delle fonti pende verso **21 denti, Ø esterno 4.8-4.9 mm**, ma nessuna fonte e' del produttore e nessuna e' stata verificata su un Tower Pro genuino. Per la vite della squadretta tre fonti deboli indicano 2.5 mm (M2.5) e una M2: non confermata. Le squadrette di lotti diversi di MG90S non sono intercambiabili: contare i denti e misurare sul pezzo reale prima di fissare il CAD.

### Cited Findings
A favore di 20T:
- "Horn gear spline: 20T Diameter:4.9mm"; "Horn type: Plastic, POM" — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- ServoDatabase: 20 T — [secondary] [servodatabase.com](https://servodatabase.com/servo/towerpro/mg90s)
- Adafruit, MG90D (modello fratello, non MG90S): "Spline count: 20" — [secondary] [adafruit.com/product/1143](https://www.adafruit.com/product/1143)
- Forum Adafruit: un MG90S misurato "20 tooth spline with a 4.8mm outer diameter", "no 'standard' for mini and micro servo splines" — [community, solo snippet: pagina 403] [forums.adafruit.com](https://forums.adafruit.com/viewtopic.php?t=95879)

A favore di 21T:
- TinyTronics (stessa pagina che ospita il datasheet 20T): "Shaft type: Spline 21T", "Shaft length: 4 mm" — [secondary] [tinytronics.nl](https://www.tinytronics.nl/en/mechanics-and-actuators/motors/servomotors/mg90s-mini-servo)
- Pololu: ruote per "micro servo splines with 21 teeth and a 4.8 mm diameter" (FEETECH FS90R / FT90R) — [primary Pololu] [pololu.com/product/4911](https://www.pololu.com/product/4911)
- Modelli 3D che dichiarano 21T per SG90 / MG90 / MG90S — [community] [cults3d.com](https://cults3d.com/en/3d-model/gadget/sg90-mg90-mg90s-fs90r-sh0257mg-micro-servo-horns-with-21-output-spline-s), [makerworld.com](https://makerworld.com/en/models/3363955)
- Un autore RobotShop Community contava sempre 20 e ha trovato 21 modellando il millerighe — [community, solo snippet: pagina 403] [community.robotshop.com](https://community.robotshop.com/blog/show/modelling-a-servo-spline)
- Tabella parametri del modello "Customizable Servo Horn" (MakerWorld 777516), colonna MG90S: 21 denti; diametro esterno millerighe 4.80; diametro foro vite ("Spline Screw Diameter") 2.5; altezza sede 4.0; profondita' dente 0.3; larghezza dente alla base 0.8, in punta 0.1 (unita' non indicate, presumibilmente mm) — [community, valori di un modello stampabile; solo riassunto del motore di ricerca: pagina 403] [makerworld.com/models/777516](https://makerworld.com/en/models/777516-customizable-servo-horn)
- Stessa pagina, nota di un utente: per MG90S comprati su AliExpress (marcati "TP" sul fondo) la squadretta stampata in PETG calzava meglio impostando il diametro esterno a 4.6 invece di 4.8 — [community, solo riassunto del motore di ricerca] [makerworld.com/models/777516](https://makerworld.com/en/models/777516-customizable-servo-horn)
- Forum RobotShop: un micro servo 9 g Miuzei misurato a 21 denti, foro centrale circa 2.5 mm, diametro millerighe circa 4.8 mm — [3rd-meas di un utente, non su MG90S Tower Pro; solo riassunto del motore di ricerca: pagina 403] [community.robotshop.com](https://community.robotshop.com/forum/t/circular-servo-arm-for-micro-servos/95203)
- M5Stack, SG90 personalizzato (non MG90S): "Spline: 21T" — [primary M5Stack, solo snippet] [docs.m5stack.com](https://docs.m5stack.com/en/accessory/SG90_Servo)

Terzo valore discordante (altro prodotto con lo stesso nome):
- Il servo "MG90S" a marchio DSSERVO dichiara millerighe 25T — [secondary, solo snippet] [aifitlab.com](https://aifitlab.com/products/dsservo-mg90s-servo-motor). Indica che la sigla "MG90S" su un clone non garantisce il millerighe.

Albero e vite:
- SG90: albero in plastica, vite autofilettante; MG90S: albero in metallo gia' filettato in fabbrica, vite a passo metrico — [3rd-meas, osservazione] [newscrewdriver.com](https://newscrewdriver.com/2020/12/27/notes-on-micro-servo-output-shaft/)
- "the output splines can differ between different batches": due lotti di MG90S con squadrette non intercambiabili (una troppo lasca, l'altra si e' spaccata forzandola); squadrette SG90 e MG90S non intercambiabili — [3rd-meas] [newscrewdriver.com](https://newscrewdriver.com/2020/12/27/notes-on-micro-servo-output-shaft/)
- Vite squadretta MG90S: "M2.5" secondo una guida — [secondary, bassa affidabilita'] [shuntool.com](https://shuntool.com/article/mg90s-screw-size); "M2 x 8 mm" secondo un'altra — [secondary, bassa affidabilita'] [aliexpress.com wiki](https://www.aliexpress.com/s/wiki-ssr/article/mg90s-servo-screw-size). Le due si contraddicono.
- A favore di 2.5 mm: foro vite 2.5 nella tabella MakerWorld (colonna MG90S) — [community, solo riassunto] [makerworld.com/models/777516](https://makerworld.com/en/models/777516-customizable-servo-horn). Attenzione: e' il diametro del foro nella squadretta, non la filettatura dell'albero; un foro da 2.5 mm e' compatibile sia con una vite M2.5 di precisione sia con una M2 con gioco.
- Lunghezza della vite: una guida generica indica 4-8 mm secondo lo spessore da serrare — [secondary, bassa affidabilita', non specifica dell'MG90S; frase riportata dal riassunto di ricerca, attribuzione alla pagina Kpower probabile ma non verificata] [kpower.com](https://www.kpower.com/insight_gearbox/7090.html)
- SG90 (non MG90S): vite squadretta autofilettante ~2 mm sul filetto, foro 1.5 mm — [3rd-meas] [forum.arduino.cc](https://forum.arduino.cc/t/servo-arm-screw-mount-size/696481)

Squadrette di serie:
- 3 squadrette nel sacchetto: a 1, 2 e 4 bracci; due profili di foratura (6 o 7 fori) con interassi leggermente diversi; spessore e rigidezza variabili — [3rd-meas, senza quote] [newscrewdriver.com](https://newscrewdriver.com/2020/12/28/notes-on-micro-servo-horn/)
- Contenuto confezione clone: "1x Accessory mounting screw, 1x Shaft accessories, 2x Mounting screw" — [secondary] [tinytronics.nl](https://www.tinytronics.nl/en/mechanics-and-actuators/motors/servomotors/mg90s-mini-servo)

### Inferences
- Pololu vende oggi come "21T, 4.8mm" ruote che diversi rivenditori elencano ancora come "20T, 4.8mm" (lo slug RobotShop contiene ancora "20t"): e' plausibile che "20T" sia spesso un errore di conteggio dello stesso millerighe a 21 denti. Non e' dimostrato per l'MG90S.
- Il diametro 4.9 mm del datasheet Sky Star coincide con lo STEP dell'utente (~4.9 mm).
- Conteggio delle fonti (nessuna del produttore Tower Pro): per 21T = TinyTronics, tabella MakerWorld, modelli Cults3D/MakerWorld, Pololu e M5Stack (per servo della stessa classe); per 20T = datasheet Sky Star, ServoDatabase, forum Adafruit, Adafruit MG90D. Il datasheet Sky Star (20T) e la scheda TinyTronics (21T) descrivono lo STESSO prodotto: almeno una delle due e' un errore di conteggio. Ipotesi di lavoro piu' probabile: 21 denti; non e' un dato certo.
- La differenza di 0.2 mm tra il diametro "da tabella" (4.8) e quello che calza davvero su un clone (4.6) mostra che un millerighe stampato va tarato con provini sul proprio lotto.
- Soluzione robusta: disegnare nel pezzo stampato una sede che accoglie la squadretta di plastica originale, invece di stampare o comprare il millerighe alla cieca.

### Gaps
- Denti, modulo e diametri del millerighe dichiarati da Tower Pro: **NON TROVATO**.
- Filettatura e lunghezza della vite dell'albero dell'MG90S genuino: **NON TROVATO** (fonti deboli in conflitto: M2.5 x3 contro M2 x1; nessuna misura di filetto con calibro/passo pubblicata).
- Quote delle squadrette di serie (lunghezza, interasse e diametro fori, spessore): **NON TROVATO**.
- Differenza genuino / clone sul millerighe: nessuna misura comparativa trovata.

---

## 5. Squadrette METALLICHE (alluminio) per il millerighe MG90S

### Takeaway
**Non esiste una squadretta metallica verificata per l'MG90S.** Nessun marchio noto (Pololu, ServoCity/goBILDA, Tower Pro) ne vende una; esistono squadrette generiche "21T ~4.9-5 mm" per servo da crawler 1/24, ma nessun venditore dichiara la compatibilita' MG90S e non ho potuto verificare quote ne' disponibilita' su Amazon.it. Comprare un solo pacchetto di prova prima di disegnarci attorno.

### Cited Findings
Candidati (compatibilita' NON verificata, dati da snippet):
- **RampCrab RC Servo Horn, Diameter 4.9mm, 21T, Thread M2.0mm, Aluminium Alloy 7075, 3 pcs** (ASIN B0D6GDBYGS), per FCX24 / FCX18 / CR-18P / Mini LMT. Lunghezza braccio, interasse fori, spessore, serraggio a morsetto o solo vite: non indicati — [secondary] [amazon.com](https://www.amazon.com/RampCrab-Diameter-Aluminium-Upgrade-Accessory/dp/B0D6GDBYGS). Esistono varianti con lo stesso nome ma filetto M2.5 (TRX4M) e M1.4 (SCX24), e varianti 25T: controllare.
- **SERVOMY 21T-5mm Metal RC servo arm, 2 pcs** (ASIN B0DT774531): "21T spline + 5mm shaft, fits 21T mini RC servos". Quote non indicate — [secondary] [amazon.com](https://www.amazon.com/SERVOMY-21T-5mm-Crawlers-Models-Electronics/dp/B0DT774531)
- **TL2366 21T** (Sevender / BQLZR): 23 mm × 4.4 mm (altri annunci ~5 mm), OD 8 mm, ID 5 mm, foro vite Ø 2.3 mm, 2-3 g; dichiarata per servo da 12-18 g (MD922, MD933, CS-929MG, DS-929MG), non per 9 g — [secondary] [amazon.com Sevender](https://www.amazon.com/Sevender-Silver-TL2366-Compatible-12G-18G/dp/B0CM5J5W92), [ebay.de](https://www.ebay.de/itm/125626159464)

Da escludere:
- INJORA per EMax ES08MA II / SCX24: millerighe 15T Ø 3.9 mm, non compatibile — [secondary] [injora.com](https://www.injora.com/products/emax-es08ma-ii-12g-analog-metal-gear-servo-servo-mount-bracket-for-axial-scx24)
- Squadrette alluminio 25T (MG995 / MG996R / Futaba): servo standard, non compatibili — [secondary] [probots.co.in](https://probots.co.in/25t-circular-metal-servo-horn-mg996r-mg995.html)
- Pololu: per il millerighe 21T 4.8 mm vende solo ruote in plastica — [primary Pololu] [pololu.com/product/4911](https://www.pololu.com/product/4911)
- Kyosho, squadretta regolabile in alluminio "17-21T / 23T" (FZD2): per servo standard di automodelli Kyosho, compatibilita' con servo 9 g non dichiarata; da non considerare — [secondary, solo snippet] [store.hobbyetc.com](https://store.hobbyetc.com/parts/view/186288)
- Secraft (alluminio, 21 mm): solo per millerighe JR 23T, Hitec 24T, Futaba 25T — [secondary, solo snippet] [gator-rc.com](https://www.gator-rc.com/products/21mm-jr-servo)

Ricambi in PLASTICA reperibili in UE (non metallici, utili come ripiego o come "calibro" del millerighe):
- Pololu "Wheel for Micro Servo Splines (21T, 4.8mm) - 60×8mm, Red, 2-Pack" (cod. 4911) e' a catalogo presso Robot Italy — [secondary, solo titolo/URL del risultato di ricerca; prezzo e giacenza non verificati] [robot-italy.com](https://robot-italy.com/products/4911-pololu-wheel-for-micro-servo-splines-21t-4-8mm-60x8mm-red-2-pack)
- Adafruit "Micro Servo Arm and Horn Set" (cod. 4251), plastica, per micro servo da 9 g, a catalogo presso Opencircuit (NL); compatibilita' con MG90S non dichiarata — [secondary, solo snippet] [adafruit.com/product/4251](https://www.adafruit.com/product/4251), [opencircuit.shop](https://opencircuit.shop/product/micro-servo-arm-and-horn-set)

Esito delle ricerche di ripresa (8 ottobre 2026):
- Due ricerche ulteriori, una in italiano e una in inglese, limitate anche ad AliExpress / amazon.it / amazon.de, non hanno restituito NESSUN annuncio di squadretta o disco metallico dichiarato per MG90S o per servo 9 g — [ricerca mia, esito negativo; l'assenza nei risultati non prova l'inesistenza su AliExpress, le cui pagine non sono indicizzate/raggiungibili]
- L'autore del modello MakerWorld avverte che le squadrette stampate vanno bene per prototipi e carichi leggeri: sotto carico i denti si consumano in fretta — [community, solo riassunto] [makerworld.com/models/777516](https://makerworld.com/en/models/777516-customizable-servo-horn)

### Inferences
- Il candidato piu' vicino per numeri e' RampCrab (21T, Ø 4.9 mm, fori M2). Se il servo dell'utente ha 20 denti, nessuno dei tre va bene.
- Per un esapode da 18 MG90S la via a rischio minore resta la squadretta di plastica di serie annegata in una sede stampata e bloccata con la vite dell'albero; la squadretta metallica e' un miglioramento facoltativo da validare su un solo pezzo.
- Una squadretta in alluminio 7075 su albero in alluminio 6061 (genuino) o ottone (clone) con accoppiamento lasco rovina il millerighe: va accettata solo se entra senza gioco.

### Gaps
- Disponibilita' e prezzo su Amazon.it / AliExpress al 8 ottobre 2026: **NON VERIFICATO** (pagine non raggiungibili).
- Interasse fori, lunghezza, spessore e tipo di serraggio di RampCrab e SERVOMY: **NON TROVATO**.
- Una conferma d'uso su MG90S di una qualsiasi squadretta metallica: **NON TROVATO**.

---

## 6. Alette di fissaggio: fori e viti

### Takeaway
Nessuna fonte affidabile da' diametro dei fori delle alette o misura delle viti di serie. L'unica quota pubblicata e' l'interasse fori 27.7 mm di un clone (27.5 mm nello STEP dell'utente). Indicazione prudente: vite M2, verificando sul pezzo se passa una M2.5.

### Cited Findings
- Interasse fori 27.7 mm; lunghezza sulle alette 31.8 mm — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- Lunghezza sulle alette 32.5 mm (quota A / disegno) — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/); [secondary] [PDF non ufficiale](https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf)
- Contorno di case e alette quasi identico tra SG90 e MG90S (stessi fori), ma spessore delle alette diverso; il cavo esce sempre dal lato vicino all'albero; 2 punti di fissaggio con viti autofilettanti — [3rd-meas, senza quote] [newscrewdriver.com](https://newscrewdriver.com/2020/12/26/notes-on-micro-servo-enclosure/)
- Nella confezione: 2 viti di fissaggio + 1 vite squadretta — [secondary] [tinytronics.nl](https://www.tinytronics.nl/en/mechanics-and-actuators/motors/servomotors/mg90s-mini-servo)
- Staffa commerciale per SG90/MG90 fornita con viti M2 × 10 mm lato servo — [secondary, da snippet] [protosupplies.com](https://protosupplies.com/product/sg90-mg90-servo-bracket/)
- Blog Kpower: fori "M2 o M2.5" — [secondary, bassa affidabilita'] [kpower.com](https://www.kpower.com/insight_gearbox/7090.html)

- Regola empirica per i fori del corpo servo: foro di circa 2 mm → vite M2, foro di circa 2.5 mm → vite M2.5 — [secondary, bassa affidabilita'; frase riportata dal riassunto di ricerca, attribuzione alla pagina Kpower probabile ma non verificata] [kpower.com](https://www.kpower.com/insight_gearbox/7090.html)

### Calcoli
- Con il foro Ø 2.5 mm dello STEP: gioco diametrale con vite M2 = 2.5 − 2.0 = 0.5 mm; con vite M2.5 = 2.5 − 2.5 = 0 mm (accoppiamento senza gioco, entra solo se il foro reale e' almeno 2.5 mm) — [computed] da quota STEP dell'utente
- Differenza di interasse tra fonti: 27.7 − 27.5 = 0.2 mm — [computed] da [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf) e STEP dell'utente

### Inferences
- L'interasse varia di almeno 0.2 mm tra fonti (27.5 / 27.7): fare asole o fori maggiorati nel pezzo stampato.
- Scelta prudente per il CAD: vite a macchina M2 (passa di sicuro in un foro da 2.5 mm e assorbe 0.2 mm di errore d'interasse); passare a M2.5 solo dopo aver verificato col calibro che il foro reale lo consenta. Le viti di serie nel sacchetto sono autofilettanti per legno/plastica e non servono con dado o inserto.

### Gaps
- Diametro foro aletta su pezzo reale e misura delle viti di serie: **NON TROVATO** (confermato anche da una ricerca mirata in ripresa). Il Ø 2.5 mm dello STEP non e' confermato da nessuna fonte.

---

## 7. Cavo, connettore, colori

### Takeaway
Cavo 250 mm (Tower Pro: 25 cm; clone: 250 ±5 mm; un clone misurato 240 mm), connettore tipo JR femmina a 3 poli passo 2.54 mm, colori marrone = massa, rosso = +V, arancio = segnale. Sezione dei fili non trovata.

### Cited Findings
- "servo wire length: 25 cm"; "Servo Plug: JR (Fits JR and Futaba)" — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- "Connector wire 250mm±5mm" — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- Clone: cavo 24 cm (9.5"), "1×3 Female Connector"; Brown = Ground, Red = 5V, Orange = PWM — [3rd-meas] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/)
- "PWM=Orange, Vcc=Red, Ground=Brown" — [secondary] [PDF non ufficiale](https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf)
- "Pin header female (2.54mm)", cavo 0.25 m, ingresso segnale 3-5 V — [secondary] [tinytronics.nl](https://www.tinytronics.nl/en/mechanics-and-actuators/motors/servomotors/mg90s-mini-servo)

### Inferences
- Ordine sul connettore = ordine della piattina: marrone (GND) - rosso (+V, centrale) - arancio (segnale). Il +V centrale e' la convenzione JR/Futaba; nessuna fonte lo scrive esplicitamente per l'MG90S.
- La custodia JR femmina non ha chiave: si puo' inserire al contrario.

### Gaps
- Sezione dei fili (AWG): **NON TROVATO**, anche dopo una ricerca mirata in ripresa. L'unico valore AWG emerso (26 AWG) riguarda prolunghe servo vendute a parte, non il cavo del servo — [secondary, solo snippet] [zbotic.in](https://zbotic.in/mg90s-metal-gear-servo-installation-specs-robotic-uses-in-india/)
- Lunghezza del cavo sui cloni: il riassunto di una ricerca segnala annunci "MG90S" con cavo da 150 mm e 175 mm invece di 250 mm, senza che io abbia potuto identificare e leggere le pagine. Non usare 250 mm come dato certo per un clone: misurare.

---

## 8. Coppia reale, gioco, modi di guasto

### Takeaway
Non esistono misure indipendenti rigorose di coppia o gioco per l'MG90S. Le sole indicazioni: un rivenditore riporta circa 1.7 kg·cm a 5 V su un clone; Vorpal afferma che i cloni tipici hanno meno di meta' della coppia del genuino (senza dati). I guasti documentati riguardano soprattutto i contraffatti: ingranaggi difettosi, deriva termica, jitter, ingranaggi interni in plastica.

### Cited Findings
Coppia:
- Clone a 5 V: "can lift 3.75lb positioned 1 cm from center of shaft" — [secondary/3rd-meas, metodo non descritto] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/). 3.75 lb × 0.4536 = 1.70 kg·cm — [computed]
- "Typically clones will have less than half the torque, be much more sluggish, and consume more power" — [community] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)
- Clone: 2.0 kg·cm a 6.0 V (non 2.2) — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)

Precisione / gioco:
- Dead band 1 us (genuino digitale), che Vorpal traduce in circa 0.045° — [secondary] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)
- Clone: corsa 180° ±3°, dead band 5 us — [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- 180° / 2000 us = 0.09°/us → 5 us = 0.45°, 1 us = 0.09° (non coincide con lo 0.045° di Vorpal) — [computed]
- Corsa utile spesso inferiore a 180°; a fine corsa rumori, vibrazioni e stallo: limitare a 20-160° — [3rd-meas] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/)

Guasti:
- Contraffatti: 10-15 % dei riduttori difettosi appena tolti dalla confezione; denti deformati, punti duri; deriva dell'albero di 2-90° quando il servo si scalda — [community] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)
- Genuini digitali: "hunting" (tremolio attorno alla posizione) sulle anche dell'esapode; rimedio: O-ring / rondella di gomma sotto la squadretta — [community] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)
- Falsi "metal gear": solo l'albero d'uscita e' metallico, gli stadi interni sono in plastica; quando si sgranano il potenziometro non viene piu' trascinato e il motore gira fino a bruciarsi — [community, teardown] [forum-tuyaopen](https://forum-tuyaopen.discourse.group/t/mg90s/24)
- Stallo: "has the potential of stripping gears and damaging the motor" — [secondary] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/)
- Recensioni: 18 servo per un esapode risultati contraffatti e con forte jitter, ricomprati; 5 pezzi difettosi con jitter (potenziometri?); primo stadio in plastica e controllo analogico su pezzi eBay; un pezzo senza bussola dell'ingranaggio d'uscita — [community] [servodatabase.com](https://servodatabase.com/servo/towerpro/mg90s)

### Gaps
- Coppia misurata con metodo documentato (genuino e clone, 4.8 / 6.0 V): **NON TROVATO**.
- Gioco angolare misurato all'uscita (gradi): **NON TROVATO**.
- Durata in cicli / usura del potenziometro: **NON TROVATO** (solo affermazioni generiche).

---

## 9. Riconoscere un Tower Pro genuino e dove comprarlo

### Takeaway
Il genuino si riconosce da prezzo (sotto ~4.50 USD probabilmente contraffatto), marchio visibile nelle foto, fossette profonde attorno alla staffa e rondella scura all'uscita dell'albero. Non ho trovato un rivenditore autorizzato Tower Pro in Italia; l'unico negozio UE trovato che indica TowerPro come produttore e' Botland (Polonia), da verificare.

### Cited Findings
- "There are many counterfeit servo of TowerPro from China dealers selling on eBay, Amazon and Alibaba websites."; "If the suppliers removed "TowerPro" logo from the photos and the products description, they are selling counterfeits low quality servo." — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- Prezzo: sotto ~4.50 USD probabilmente contraffatto, sotto 2.50 USD quasi certamente — [community] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)
- Vista dall'alto: genuino con fossette profonde attorno alla staffa e rondella scura dove esce l'albero; falso con fossette quasi assenti e rondella color rame chiaro — [community] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)
- Genuino: ingranaggi in alluminio, scorrevoli a mano senza scatti, digitale; la maggior parte dei contraffatti si dichiara digitale ma e' analogica — [community] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)
- Clone buono citato: Turnigy MG90S (HobbyKing) — [community] [Vorpal wiki](https://vorpalrobotics.com/wiki/index.php/Tower_Pro_MG90S_Vs._Clones)
- "this is the most-faked servo ever" — [community] [servodatabase.com](https://servodatabase.com/servo/towerpro/mg90s)
- Botland, codice DNG-24408, produttore indicato TowerPro, 15.50 EUR IVA inclusa; la pagina non dichiara esplicitamente che sia originale e riporta una nota "B2B" — [secondary] [botland.store](https://botland.store/micro-servos/24408-towerpro-mg90s-micro-analogue-servo-with-metal-gear.html)

### Inferences
- Il prezzo Botland (15.50 EUR al pezzo) e' alto rispetto ai ~4.50 USD indicati da Vorpal: verificare se e' per pezzo e se spedisce a privati in Italia. 18 pezzi = 279 EUR — [computed]
- A 18 pezzi conviene comprarne 20-22 e scartare quelli con punti duri o jitter.

### Gaps
- Elenco rivenditori autorizzati Tower Pro per Italia / UE: **NON TROVATO**.
- Etichetta, ologramma o codice di autenticita' descritti a parole: **NON TROVATO** (Vorpal rimanda a foto).

---

## Cose che solo l'utente puo' fornire
1. Contare i denti del millerighe su un servo reale (segnare un dente col pennarello) e misurare il diametro esterno col calibro.
2. Misurare la vite della squadretta: diametro sul filetto (2.0 o 2.5 mm) e lunghezza.
3. Misurare il diametro reale dei fori delle alette e l'interasse (27.5 o 27.7 mm), e lo spessore delle alette.
4. Misurare le squadrette di serie: lunghezza, interasse e diametro dei fori, spessore.
5. Link d'acquisto / foto dei 18 servo (etichetta, vista dall'alto) per capire se sono genuini o cloni.
6. Misurare la corrente di stallo di un pezzo a 5 V e 6 V con un alimentatore da banco (stallo breve).
7. Misurare la lunghezza reale del cavo (250 mm sul genuino; alcuni cloni potrebbero averlo piu' corto) e, se possibile, il diametro del conduttore per ricavare l'AWG.
8. Misurare il gioco angolare all'uscita (squadretta lunga come indice, servo alimentato e fermo) su 2-3 pezzi: nessun dato pubblicato.
9. Dire se si vuole davvero una squadretta metallica: in tal caso comprare UN solo pacchetto di prova (es. RampCrab 21T Ø 4.9 mm M2) e verificare l'accoppiamento prima di disegnare i 18 giunti.
