# Architettura di alimentazione: 18 servo MG90S + logica da LiPo 2S

> Stato del file: VERSIONE 2 (8 ottobre 2026). Scritta dal digest del tentativo interrotto e completata con ~20 nuove chiamate web mirate.
>
> Legenda etichette: **[primary]** = datasheet / manuale / pagina prodotto del costruttore; **[secondary]** = negozio, blog, wiki; **[3rd-meas]** = misura di terzi (third_party_measurement); **[community]** = forum; **[computed]** = calcolo mio con formula.
>
> Nota sul metodo. Molte pagine sono state lette tramite WebFetch/WebSearch, cioe' riassunte da un modello piccolo. Dove ho letto io stesso il testo estratto dal PDF, il testo grezzo della pagina o il grafico, lo scrivo ("letto direttamente"). I numeri critici non visti in citazione testuale sono segnalati con "(non visto in citazione)".

## 0. Sintesi del progetto proposto (schema a blocchi e lista acquisti)

### Takeaway
Batteria 2S -> T-plug -> fusibile mini-lama 20 A vicino alla batteria -> interruttore generale -> nodo a stella. Dal nodo partono: (a) regolatore buck servo a 6.0 V (prima scelta Pololu D42V110F6 #5673; ripiego 2x Hobbywing UBEC 10A, uno per bus VS1/VS2), (b) buck piccolo 5 V per la ESP32-S3 (Pololu D24V22F5 #2858 oppure Hobbywing UBEC 3A), (c) VL della SSC-32 direttamente dalla batteria commutata (6.4-8.4 V rientra nel campo 6-9 V), (d) partitore 100k/47k verso un pin ADC1 della ESP32-S3. Massa comune a stella. I 18 servo vanno divisi 9 + 9 sui due bus della SSC-32.

### Cited Findings
- Tutti i numeri e le fonti sono nelle sezioni 1-9.

### Inferences
- Schema (inferenza mia, costruita sui dati delle sezioni seguenti):

```
LiPo 2S OVONIC (T-plug FEMMINA sulla batteria, cavi 12 AWG)
  |
[T-plug MASCHIO lato robot]  cavo siliconico 14 AWG
  |
[Fusibile mini-lama 20 A in portafusibile in linea]   <- a pochi cm dalla batteria, PRIMA dell'interruttore
  |
[Interruttore generale: Pololu Big MOSFET Slide Switch HP #2815, oppure bilanciere 20 A DC]
  |
  +-- NODO A STELLA (+) -----------------------------------------------------+
  |                |                         |                               |
[Buck servo 6.0 V]            [Buck logica 5 V]            SSC-32 VL (6-9 V)     partitore 100k / 47k + 100 nF
 Pololu D42V110F6 #5673        Pololu D24V22F5 #2858       jumper VL=VS TOLTO    -> GPIO1 o GPIO2 (ADC1)
  |  2 coppie di fili 16 AWG         |
  +--> SSC-32 VS1 (ch 0-15: 9 servo, 3 zampe)   +--> pin 5V della ESP32-S3-CAM
  +--> SSC-32 VS2 (ch 16-31: 9 servo, 3 zampe)
       2200 uF 16 V low-ESR su ciascun morsetto VS
GND: tutte le masse tornano a un solo nodo a stella (-) accanto al regolatore servo.
Presa di bilanciamento JST-XH: cicalino 1-8S (soglia 3.5 V/cella), da scollegare a riposo.
```

- Due "carrelli" coerenti (inferenza):
  - Carrello A (Pololu, tutto documentato; spedizione dagli USA o via DigiKey Marketplace): #5673 D42V110F6 (US$59.95) + #2858 D24V22F5 (US$18.95) + #2815 Big MOSFET Slide Switch HP (US$8.49).
  - Carrello B (negozio RC nell'UE): 2x Hobbywing UBEC 10A V2 Car HW30603003 (27.90-32.90 EUR l'uno da Robitronic) + Hobbywing UBEC 3A (2-6S) 86010010 per la logica + interruttore a bilanciere 20 A / 12-14 V DC.
- Comuni ai due carrelli: fusibile MINI 20 A + portafusibile Littelfuse FHM (0FHM0002ZXJ 12 AWG oppure 0FHM0001ZXJ 14 AWG), 2x elettrolitico 2200 uF 16 V low-ESR (Panasonic EEUFR1C222 o EEUFM1C222), cicalino BX100 1-8S (3.99 EUR; spesso gia' incluso nelle confezioni OVONIC da 2 pacchi), resistenze 100 kOhm e 47 kOhm 1 %, ceramico 100 nF, T-plug maschio, cavo siliconico 14 / 16 / 22 AWG.

### Gaps
- Prezzo in EUR del Pololu #5673 presso un rivenditore UE: NON TROVATO.
- Hobbywing UBEC 10A cod. 30603000 (quello col manuale verificato): presso toemen.nl risulta "Op aanvraag" / "Binnenkort leverbaar" (prezzo su richiesta, non a magazzino) -> disponibilita' UE incerta; a magazzino in UE ho trovato solo la variante V2 Car 30603003.

## 1. Architettura del rail servo da 2S: uno o due regolatori, e quale tensione (5.0 / 5.5 / 6.0 V)

### Takeaway
Collegamento diretto dei servo alla 2S escluso (8.4 V contro 6.0 V massimi). Tensione consigliata: 6.0 V regolati. Con il Pololu D42V110F6 il dropout tipico pubblicato e' ~0.20 V a 6 A e ~0.34 V a 10 A: il rail resta regolato finche' l'ingresso del regolatore e' sopra ~6.2-6.35 V; sotto, l'uscita cala di poco restando nel campo 4.8-6.0 V. Indipendentemente dal numero di regolatori, alimentare VS1 e VS2 con due coppie di fili separate e 9 servo per bus: la SSC-32 e' data per 15 A di picco e 3-5 A continui per lato.

### Cited Findings
- MG90S: pagina Tower Pro "Operating voltage: 4.8V", coppia "1.8kg/cm (4.8V); 2.2kg/cm (6.6V)" (sic), nessun dato di corrente — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/). Altre schede: "4.8-6 VDC (5V Typical)" — [secondary] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/).
- Manuale SSC-32 Ver 2.0 (testo letto direttamente dal PDF): VS1 = canali 0-15, VS2 = canali 16-31; "Apply 4.8vdc to 7.2vdc for normal servos. Apply 4.8vdc to 6.0vdc when using micro servos." — [primary, copia del manuale Lynxmotion ospitata da terzi] [hobbielektronika.hu](https://hobbielektronika.hu/forum/getfile.php?id=81561)
- Stesso manuale: i jumper VS1=VS2 "are used to connect VS1 to VS2. Use this option when you are powering all servos from the same battery. Use both jumpers." — [primary, copia] [hobbielektronika.hu](https://hobbielektronika.hu/forum/getfile.php?id=81561)
- Guida SSC-32U (letta direttamente): "There are two jumpers (rather than just one) because of the current involved"; con i jumper inseriti "you can power EITHER VS1 or VS2, but not both"; toglierli quando "A second battery is needed because of high current" — [primary] [Lynxmotion SSC-32U user guide PDF](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf)
- Corrente ammessa dalla scheda SSC-32: picco VS fino a 15 A per lato (wiki Lynxmotion); RobotShop raccomanda non oltre 3-5 A continui per lato; un venditore su forum cita "15 amps per side, 30 amps max"; assorbimento logica 31 mA — [secondary; valori presi dal riassunto di una ricerca fatta dal ricercatore "ssc32": le pagine originali hanno risposto 403 / verifica Cloudflare, quindi NON visti in citazione] [wiki.lynxmotion.com SSC-32](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/servo-erector-set-system/ses-electronics/ses-modules/ssc-32/), [robotshop.com SSC-32](https://www.robotshop.com/products/lynxmotion-ssc-32-servo-controller)
- Dropout tipico Pololu D42V110Fx, curva Vout = 6 V (grafico del costruttore, letto direttamente a occhio, incertezza +/-15 mV): ~75 mV a 2 A, ~135 mV a 4 A, ~200 mV a 6 A, ~270 mV a 8 A, ~335 mV a 10 A. Curva Vout = 5 V: ~150 mV a 6 A, ~235 mV a 8 A, ~290 mV a 10 A — [primary, grafico] [Pololu: Typical dropout voltage D42V110Fx](https://a.pololu-files.com/picture/0J13895.1200.jpg) (dalla pagina [pololu.com/product/5673](https://www.pololu.com/product/5673))
- Pololu: "the effective lower limit of VIN is VOUT plus the regulator's dropout voltage"; campo d'ingresso D42V110F6 6 V - 60 V con nota "Minimum input voltage is subject to dropout voltage considerations" — [primary] [pololu.com/product/5673](https://www.pololu.com/product/5673)
- Hobbywing UBEC 10A (2-6S), manuale letto direttamente: "Input Voltage 6V-25.2V (2-6S LiPo)", "Output Voltage 5.0V/6.0V/7.4V/8.4V". Nessun dato di dropout ne' di tensione minima per l'uscita a 6.0 V — [primary] [Hobbywing UBEC10A2-6S.pdf](https://oss.hobbywing.com/pdf/pdfen/UBEC10A2-6S.pdf)

### Inferences
- Margine di regolazione a 6.0 V con D42V110F6: Vin minima = Vout + dropout = 6.0 + 0.335 = 6.34 V a 10 A; 6.0 + 0.20 = 6.20 V a 6 A — [computed] dal grafico Pololu.
- Bilancio delle cadute a monte del regolatore con 10.9 A lato batteria (vedi sezione 2): cavo 14 AWG 0.4 m totali = 36 mV; interruttore MOSFET Pololu HP 8.6-13 mOhm max = 94-142 mV; fusibile e connettori: non quantificati (dato non trovato). Totale stimato ~0.15-0.2 V + fusibile — [computed] da [powerstream.com](https://www.powerstream.com/Wire_Size.htm) e [pololu.com/product/2815](https://www.pololu.com/product/2815).
- Quindi: con pacco a 6.6 V sotto carico (3.3 V/cella) il regolatore vede ~6.4 V e a 10 A e' al limite della regolazione (6.34 V); con pacco a 7.0 V (3.5 V/cella) restano ~0.45 V di margine. Sotto il limite l'uscita segue circa Vin - dropout (es. 6.2 V in -> ~5.9 V out): innocuo per i servo — [computed/inferenza; il comportamento in dropout non e' descritto testualmente da Pololu].
- A 5.0 V (D42V110F5, #5671) la regolazione regge fino a Vin = 5.0 + 0.29 = 5.29 V a 10 A, cioe' per tutta la scarica, ma la coppia scende da 2.2 a ~1.8 kg·cm (-18 %) — [computed] da [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/).
- Compromessi intermedi: Pololu D42V110F5.3 a 5.3 V (#5672, [pololu.com/product/5672](https://www.pololu.com/product/5672), dettagli non verificati); 5.5 V via jumper sul YPG 20A HV SBEC (sezione 3); Castle BEC 2.0 esce di fabbrica a 5.25 V (sezione 3).
- Tolleranza del D42V110F6: 3 % -> 5.82-6.18 V; il limite alto supera di 0.18 V i 6.0 V nominali dell'MG90S — [computed] da [pololu.com/product/5673](https://www.pololu.com/product/5673). Misurare l'uscita a vuoto prima di collegare i servo.
- Uno o due regolatori: (A) un regolatore, due coppie di fili verso VS1 e VS2 (i jumper VS1=VS2 possono restare: sono in parallelo ai fili); (B) due regolatori, uno per bus, con i jumper VS1=VS2 RIMOSSI (mai mettere in parallelo le uscite di due switching). In entrambi i casi 3 zampe (9 servo) per bus.
- Verifica dei limiti della SSC-32 con 9 servo per lato: camminata 9 x 0.12-0.25 A = 1.1-2.3 A (< 3-5 A continui raccomandati); stallo di tutti e 9: 9 x 0.86-0.95 A = 7.7-8.5 A (< 15 A di picco). Con 18 servo su un solo lato lo stallo (15.5-17 A) supererebbe i 15 A — [computed] dai valori Lynxmotion/RobotShop citati sopra.

### Gaps
- Dropout reale del Hobbywing UBEC 10A a 6.0 V con ingresso 6.4-7.0 V: NON TROVATO (il costruttore non lo pubblica). Da misurare al banco.
- Tolleranza della tensione di uscita dei Hobbywing UBEC: NON TROVATO.
- Resistenza interna del pacco OVONIC 2S 5200 mAh 50C: NON TROVATO.
- Portata per lato della SSC-32 da una pagina del costruttore letta direttamente: non ottenuta (403 / Cloudflare).

## 2. Dimensionamento sulla corrente di stallo

### Takeaway
Stallo per servo: 0.68-0.86 A secondo le fonti (0.95 A con tolleranza +10 % a 6.0 V). Caso peggiore 18 servo in stallo a 6.0 V: 15.5 A nominali, 17 A con tolleranza. Picco realistico con 6-9 servo molto caricati: ~8-11 A. Il regolatore servo deve dare almeno 10-11 A continui a 6.6-8.4 V in ingresso e sopportare (o limitare senza danni) picchi di 17 A per frazioni di secondo.

### Cited Findings
- Stallo "700mA (measured)", tensione di prova non dichiarata; idle "10mA (typical)"; in movimento "120-250mA" — [3rd-meas, metodo non descritto] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/)
- Versione a rotazione continua: stallo 800 mA "(measured)" — [3rd-meas] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s-continuous-rotation/)
- TowerPro MG90S con alimentatore da banco Wanptek NPS306W a 4.9 V: riposo 0.00 A, rotazione ~0.13 A, pieno carico/blocco ~0.68 A — [3rd-meas; modalita' di carico non descritta] [Fab Academy 2022 HKISPACE](https://fabacademy.org/2022/labs/hkispace/assignments/10/)
- Datasheet del clone Sky Star: stallo 750 mA +/-10 % a 4.8 V; 860 mA +/-10 % a 6.0 V — [primary del clone; dato ripreso dalle note del ricercatore "servo_mg90s", PDF non riaperto da me] [Sky Star MG90S datasheet PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- Articolo Kpower (luglio 2026): lo stallo "can spike sharply to 1.5 A or more", senza metodo; blog Kpower: 650 mA da scheda tecnica — [secondary, non verificato] [kpower.com](https://www.kpower.com/insight_bldc/7870.html), [blog.kpower.com](https://blog.kpower.com/servo/630.html)
- Tower Pro non pubblica correnti — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/)
- Adafruit: "Even micro servos will draw several hundred mA when moving" — [secondary] [learn.adafruit.com](https://learn.adafruit.com/16-channel-pwm-servo-driver/hooking-it-up)
- Manuale SSC-32 v2 (letto direttamente): alimentazione singola "generally safe" con "VS of 6.0vdc 1600mAh NiCad or NiMH battery packs for up to 18 servos" e "6.0vdc 2.0amp wall pack for up to 8 servos"; "99% of customers problems with the SSC-32 are power supply related" — [primary, copia] [hobbielektronika.hu](https://hobbielektronika.hu/forum/getfile.php?id=81561)

### Inferences
- Le fonti NON concordano: 0.65 A (Kpower blog), 0.68 A a 4.9 V (Fab Academy), 0.70 A (Protosupplies), 0.80 A (Protosupplies CR), 0.75 / 0.86 A a 4.8 / 6.0 V (Sky Star), "1.5 A o piu'" (Kpower, senza metodo). Valore di progetto: 0.86 A nominali e 0.95 A massimi a 6.0 V.
- 18 servo in stallo a 6.0 V: 18 x 0.86 = 15.5 A; con +10 %: 18 x 0.946 = 17.0 A — [computed].
- 18 servo in stallo a ~5 V: 18 x 0.70 = 12.6 A — [computed] dalle misure Protosupplies / Fab Academy.
- Picco realistico a 6.0 V, 6 in stallo + 12 in movimento a 0.25 A: 6 x 0.86 + 12 x 0.25 = 8.2 A (8.7 A con +10 %) — [computed].
- Picco realistico a 6.0 V, 9 in stallo + 9 in movimento: 9 x 0.86 + 9 x 0.25 = 10.0 A (10.8 A con +10 %) — [computed].
- Camminata normale: 18 x 0.12-0.25 A = 2.2-4.5 A — [computed] dai valori "in movimento" di Protosupplies (a ~5 V, carico non dichiarato: stima, non misura sull'esapode).
- Corrente lato batteria: I_batt = Vout x Iout / (eta x Vbatt). Con eta = 0.90: 10.8 A x 6 V / (0.9 x 6.6 V) = 10.9 A; stallo totale 17 A x 6 / (0.9 x 6.6) = 17.2 A — [computed]; eta da "Typical efficiency of 85% to 95%" [pololu.com/product/5673](https://www.pololu.com/product/5673) e "conversion efficiency exceeds 90%" [manuale Hobbywing](https://oss.hobbywing.com/pdf/pdfen/UBEC10A2-6S.pdf).
- Requisito del regolatore servo: continuo >= 10-11 A con Vin 6.6-8.4 V; burst 17 A per < 1 s oppure limitazione di corrente senza danni. Con due regolatori (uno per bus): continuo >= 5.5 A, burst 8.5 A ciascuno (9 x 0.946).
- Evento critico tipico: all'accensione tutti i servo partono insieme verso la posizione comandata. Mitigazione software: inviare il primo comando una zampa alla volta, a distanza di 100-200 ms — inferenza.
- Autonomia indicativa: 4 A medi x 6 V / 0.9 = 26.7 W + ~2.5 W logica = ~29 W; energia utile 5.2 Ah x 7.4 V x 0.8 = 30.8 Wh -> circa 1 h — [computed, stima].

### Gaps
- Corrente di stallo dichiarata da Tower Pro per l'MG90S originale: NON TROVATO.
- Misura con oscilloscopio del picco di spunto di un MG90S: NON TROVATO.
- Corrente misurata di un esapode con 18 MG90S in camminata: NON TROVATO.

## 3. Regolatori acquistabili: verifica sui dati del costruttore, prima scelta e ripiego

### Takeaway
Prima scelta: Pololu D42V110F6 (#5673), 6 V: corrente continua tipica ~13.5-15.5 A con ingresso 7-12 V (letta dal grafico del costruttore), dropout documentato, protezione da inversione, pin di enable, quiescente < 0.3 mA, fori M2, 31.8 x 43.2 x 9 mm, US$59.95; si compra da pololu.com o via DigiKey Marketplace (spedizione dagli USA), prezzo UE non trovato. Ripiego: 2x Hobbywing UBEC 10A impostati a 6.0 V, uno per bus: versione V2 Car HW30603003 a magazzino in UE (27.90-32.90 EUR, 10 A continui / 15 A picco, 45 x 20 x 16.2 mm, 34 g) oppure versione 30603000 (10 A / 20 A picco, 43.1 x 32.3 x 12.5 mm, 36 g, manuale verificato ma disponibilita' UE incerta). Esclusi per la 2S: Matek BEC12S-PRO (ingresso minimo 9 V), Hobbywing UBEC 25A HV e 10A HV (ingresso da 3S), moduli XL4016 (ingresso minimo 8 V).

### Cited Findings
Tabella comparativa (fonte di ogni riga nell'ultima colonna).

| Regolatore | Ingresso | Uscite | Corrente | Dimensioni / peso | Prezzo | Funziona da 2S? | Fonte |
|---|---|---|---|---|---|---|---|
| Pololu D42V110F6 (#5673) | 6-60 V (minimo soggetto a dropout) | 6 V fisso, 3 % | 11 A tip. "At 42 V in"; famiglia 8-15 A | 31.8 x 43.2 x 9 mm; peso non indicato | US$59.95 (1 pz), 55.15 (5 pz) | Si': dropout ~0.34 V a 10 A (grafico) | [primary] [pololu.com/product/5673](https://www.pololu.com/product/5673) |
| Pololu D42V110F5 (#5671) / F5.3 (#5672) | idem famiglia | 5 V / 5.3 V | 11 A tip. | idem | non verificato | Si' | [primary, solo titoli] [pololu.com/product/5671](https://www.pololu.com/product/5671), [5672](https://www.pololu.com/product/5672) |
| Pololu D24V150F6 (#2882) | 4.5-40 V (minimo = Vout + dropout) | 6 V, 4 % | 15 A tip.; limite istantaneo ~32 A | 43.2 x 31.8 x 11 mm | US$79.95 | Si'; dropout solo su grafico non letto; quiescente ~100 mA | [primary] [pololu.com/product/2882](https://www.pololu.com/product/2882) |
| Pololu D36V50F6 (#4092) | 6.5-50 V | 6 V | 5.5 A tip. (a 36 V in) | 25.4 x 25.4 x 9.5 mm | US$39.95 (prezzo letto sulle versioni F5/F7) | Solo con Vin >= 6.5 V + dropout; da solo e' troppo piccolo | [primary] [pololu.com/product/4093 (tabella di famiglia)](https://www.pololu.com/product/4093) |
| Pololu D24V90F5 (#2866) | 5-38 V | 5 V, 4 % | 4-8 A continui tip. ("as high as 9 A") | 40.6 x 20.3 x 7.6 mm | US$36.82 | Si' a 5 V; dropout 0.5-1.5 V | [primary] [pololu.com/product/2866](https://www.pololu.com/product/2866) |
| Hobbywing UBEC 10A (2-6S) cod. 30603000 | 6-25.2 V (2-6S) | 5.0/6.0/7.4/8.4 V, 3 dip switch | 10 A continui, 20 A picco | 43.1 x 32.3 x 12.5 mm, 36 g | toemen.nl: "Op aanvraag", "Binnenkort leverbaar" | Dichiarato si'; dropout non pubblicato | [primary] [manuale](https://oss.hobbywing.com/pdf/pdfen/UBEC10A2-6S.pdf), [pagina prodotto](https://www.hobbywing.com/en/products/ubec-10a-2-6s152.html); [secondary] [toemen.nl](https://toemen.nl/product/hobbywing-ubec-10a-6s) |
| Hobbywing UBEC 10A V2 Car cod. HW30603003 | 2-6S LiPo | 6.0/7.4/8.4 V (niente 5.0 V) | 10 A continui, 15 A brevi | 45 x 20 x 16.2 mm, 34 g, IP67, interruttore esterno, LED | 27.90 EUR IVA incl., ">20 pcs" (lettura pagina 8/10/2026); un riassunto di ricerca riporta 32.90 EUR; htmodel.sk 33.20 EUR | Dichiarato si'; dropout non pubblicato | [secondary] [shop.robitronic.com](https://shop.robitronic.com/en/hobbywing-bec-10a-v2-car-hw30603003), [htmodel.sk](https://www.htmodel.sk/en/hobbywing-ubec-10a-v2-car/); [primary, non visto in citazione] [hobbywing.com UBEC 10A-Car](https://www.hobbywing.com/en/products/ubec-10a-car79) |
| Hobbywing UBEC 8A (2-3S) cod. 86010030 | 6-12.6 V (2-3S) | 5 V / 6 V con selettore | 8 A continui, 15 A picco; quiescente 60 mA | 42 x 39 x 9 mm, 36 g | NON TROVATO | Dichiarato si' | [primary] [hobbywing.com UBEC 8A](https://www.hobbywing.com/en/products/ubec-8a-2-3s100) |
| Hobbywing UBEC 25A HV cod. 30606000 | 3S-18S (ingresso ausiliario 1S-2S solo di backup) | 5.2 (altrove 5.0)/6.0/7.4/8.4 V | 25 A, 50 A picco | 55 x 40.2 x 17.6 mm, 74 g | — | NO (ingresso principale minimo 3S) | [primary via riassunto di ricerca] [hobbywing.com UBEC 25A HV](https://www.hobbywing.com/en/products/ubec-25a-hv95.html) |
| Hobbywing UBEC 10A HV cod. 30608000 | 3-14S | 6.0/7.4/8.4 V | 10 A, 25 A istantanei | 55 x 25 x 12 mm, 35 g | — | NO (minimo 3S) | [primary via riassunto di ricerca] [hobbywing.com UBEC 10A HV](https://www.hobbywing.com/en/products/ubec-10a-hv289.html) |
| Castle Creations CC BEC 2.0 (010-0154-00) | max 12S/14S; minimo numerico NON TROVATO | 4.75-12 V programmabile con Castle Link USB (non incluso); default 5.25 V | 9 A continui fino a 7.0 V di uscita; picco 14 A | — | US$46.95, "Sold out" sul sito Castle | Non verificato | [primary] [castlecreations.com](https://castlecreations.com/collections/voltage-regulators-becs); specifiche: [secondary, riassunto di ricerca] [holmeshobbies.com](https://holmeshobbies.com/castle-creations-bec-2-0.html), [ozrc.com.au](https://ozrc.com.au/products/castle-creations-14a-4-75-12-0v-bec-2-0-010-0154-00) |
| Castle CC BEC 2.0 WP (010-0153-00) | un rivenditore indica 2S-14S "6V-58.8V" | programmabile | 15 A picco | — | US$56.95, disponibile sul sito Castle | Non verificato | [primary] [castlecreations.com](https://castlecreations.com/collections/voltage-regulators-becs); [secondary] [classicrcshop.com](https://classicrcshop.com/products/cc-bec-2-0-15a-max-output-14s-waterproof-cse010015300) |
| Castle CC BEC PRO | max 12S (50.4 V) | 4.8-12.5 V (rivenditore) | 20 A picco | 1.69" x 1.3" x 0.94" (rivenditore) | US$54.95 | Non verificato | [primary] [castlecreations.com](https://castlecreations.com/collections/voltage-regulators-becs) |
| Matek BEC12S-PRO | 9-55 V | 5.2 (default)/8/12 V | 5 A | — | — | NO (minimo 9 V; nessuna uscita a 6 V; nessuna protezione da inversione) | [secondary, schede rivenditori] [racedayquads.com](https://www.racedayquads.com/products/matek-bec12s-pro-9-55v-to-5-8-12v-5a) |
| YPG (ex YEP) 20A HV SBEC | 2-12S, 6-50 V | 5 / 5.5 / 6 / 7 / 9 V via jumper | 20 A dichiarati (non e' chiaro se in ingresso o in uscita) | PCB 57 x 26 mm, 42 g | NON TROVATO | Dichiarato si'; nessun datasheet | [secondary] [flyingtech.co.uk](https://www.flyingtech.co.uk/product/ypg-20a-hv-2-12s-ubec-with-selectable-voltage-output-5-0v-5-5v-6-0v-7-0v-9-0v/) |
| UBEC 8A generico "6-36V" (tipo HENGE) | 6-36 V | 5.2/6/7.4/8.4 V | 8 A | — | — | Dichiarato si'; nessun dato di dropout | [secondary] [flyingtech.co.uk](https://www.flyingtech.co.uk/product/8a-6-36v-input-ubec-with-5-2-6-7-4-8-4v-output/) |
| Modulo generico XL4016 "300 W" | chip: "Recommended operating voltage range 8V~36V" | regolabile 1.25-32 V | chip 12 A; con Vin 8-20 V l'applicazione tipica da' 5 V / 9 A; limite interruttore 14 A; quiescente 5 mA | — | — | NO: minimo 8 V, la 2S scende a 6.4 V | [primary, datasheet letto direttamente] [XLSEMI XL4016](https://www.xlsemi.com/datasheet/XL4016-EN.pdf) |
| DFRobot DFR0831 "DC-DC Buck Converter 6~14V to 5V/8A" | 6-14 V | 5 V | 8 A | — | — | Solo 5 V; dettagli non verificati | [primary, solo titolo] [wiki.dfrobot.com/dfr0831](https://wiki.dfrobot.com/dfr0831/) |

Altri dati verificati:
- Corrente continua massima tipica D42V110Fx in funzione dell'ingresso (grafico del costruttore, letto direttamente): curva Vout = 5 V ~14.2 A a Vin ~5.2 V e ~15.5 A fra 8 e 12 V; curva Vout = 8.4 V ~13.5 A fra 8.6 e 12 V. La curva a 6 V non e' tracciata — [primary, grafico] [Pololu: Typical maximum continuous output current D42V110Fx](https://a.pololu-files.com/picture/0J13892.1200.png)
- D42V110F6: "< 0.3 mA typical no-load quiescent current"; in shutdown "approximately 100 µA plus 2 µA per volt on VIN"; ENA "pulled up to VIN ... through a 1 MΩ resistor to enable the regulator by default"; fori grandi "sized to accommodate 14 AWG wires or 2-pin 5mm-pitch terminal blocks"; fori di fissaggio 0.086" (M2) "separated by 1.53″ horizontally and 1″ vertically" (38.9 x 25.4 mm); protezione da inversione integrata; ~800 kHz; "gracefully limits the output current" ma "this limiting is insufficient to cover all possible combinations", con raccomandazione di fusibili esterni — [primary] [pololu.com/product/5673](https://www.pololu.com/product/5673)
- Distributori del #5673: quasi tutti "DigiKey Marketplace (ships from the USA, direct from Pololu)", Italia compresa; in Europa compaiono EXP GmbH (Germania) e Kamami (Polonia); stato "Rationed (Active and Preferred)" — [primary] [pololu.com/product/5673/distributors](https://www.pololu.com/product/5673/distributors). La ricerca sul sito exp-tech.de non ha mostrato il prodotto — [secondary] [exp-tech.de](https://exp-tech.de/search?q=D42V110F6)
- Hobbywing UBEC 10A 30603000, manuale (letto direttamente): 6.0 V = "Dip switch #1 = Off, #2 = Off, #3 = On"; 5.0 V = tutti Off; 7.4 V = #2 On; 8.4 V = #1 On; "2 cables are connected in parallel at the output end"; interruttore esterno on/off; custodia in alluminio; protezioni di sovracorrente, cortocircuito in uscita, termica; polarita' errata: "the UBEC will be seriously damaged" — [primary] [Hobbywing UBEC10A2-6S.pdf](https://oss.hobbywing.com/pdf/pdfen/UBEC10A2-6S.pdf)
- Pololu D24V150F6: "Typical no-load quiescent current of 100 mA"; Pololu stessa indirizza alla famiglia piu' nuova D42V110Fx — [primary] [pololu.com/product/2881](https://www.pololu.com/product/2881)

### Inferences
- D42V110F6 con Vin 6.6-8.4 V: la corrente continua tipica sta fra le curve 5 V (~15.5 A) e 8.4 V (~13.5 A), quindi ~14 A — [computed, interpolazione dal grafico; valore tipico in aria libera, da declassare dentro una scocca chiusa]. Copre il picco realistico di 10-11 A con ~30 % di margine; NON copre in continuo lo stallo totale di 17 A (caso di guasto: limitazione del regolatore e condensatori, poi fusibile).
- Calore: a 10 A e 6 V (60 W) con rendimento ~0.90-0.92 il regolatore dissipa ~5-6 W di picco, ~2 W a 4 A medi — [computed]. Montarlo su distanziali con feritoie; vicino al regolatore preferire PETG / PETG-CF al PLA.
- Perche' il Pololu come prima scelta: unico candidato con dropout e corrente massima documentati a bassa tensione d'ingresso; protezione da inversione; ENA per spegnere i servo da firmware; quiescente < 0.3 mA; fori M2 a interasse noto (CAD); 9 mm di altezza.
- Perche' 2x Hobbywing UBEC 10A come ripiego: a magazzino in UE (V2 Car), 20 A continui complessivi (30-40 A di picco), copre lo stallo totale, dimezza la corrente per morsetto VS. Contro: dropout e tolleranza non pubblicati, nessuna protezione da inversione (30603000), nessun foro di fissaggio, 68-72 g in due, costo totale simile al Pololu, e una selezione sbagliata (7.4 o 8.4 V) brucia i servo: misurare l'uscita col tester PRIMA di collegare la SSC-32.
- Attenzione ai due codici Hobbywing: 30603000 (5.0/6.0/7.4/8.4 V, picco 20 A, dip switch) e 30603003 "V2 Car" (6.0/7.4/8.4 V, picco 15 A, IP67). Per questo progetto servono solo i 6.0 V, quindi vanno bene entrambi.
- D24V150F6 scartato: quiescente ~100 mA, US$79.95, e il costruttore stesso consiglia la famiglia D42V110Fx.
- Castle BEC 2.0: 9 A continui non bastano da solo; per cambiare tensione serve il Castle Link USB (software Windows); utile solo perche' esce gia' a 5.25 V.

### Gaps
- Prezzo in EUR / rivenditore UE con il #5673 a magazzino: NON TROVATO. Dazi e IVA di un ordine diretto pololu.com o DigiKey Marketplace verso l'Italia: non verificati.
- Peso del D42V110F6: non indicato. Valore numerico del suo limite di corrente: non dichiarato.
- Metodo di selezione della tensione e valore di fabbrica del Hobbywing V2 Car 30603003: non riportati dal negozio; manuale non letto.
- Tensione minima d'ingresso e dropout dei Castle BEC 2.0 / BEC Pro: NON TROVATO su fonte del costruttore.
- Turnigy 8-15 A SBEC: nessun prodotto attuale trovato.

## 4. Capacita' bulk sul rail servo vicino alla SSC-32

### Takeaway
Regola pratica documentata: ~100 uF per servo, quindi ~1800 uF per 18 servo. Proposta: un elettrolitico low-ESR 2200 uF 16 V su ciascun morsetto VS (4400 uF totali) + 100 nF ceramico in parallelo. Candidati: Panasonic FR EEUFR1C222 (12.5 x 20 mm) o Panasonic FM EEUFM1C222 (12.5 x 25 mm, 15 mOhm).

### Cited Findings
- Adafruit: punto di partenza "n * 100uF" con n = numero di servo, esempio "470uF or more for 5 servos"; serve quando l'alimentazione "dips a lot when the servos move"; "there is no 'one magic capacitor value'"; nessuna indicazione sulla tensione nominale — [secondary] [learn.adafruit.com](https://learn.adafruit.com/16-channel-pwm-servo-driver/hooking-it-up)
- Panasonic FR, EEUFR1C222: 2200 uF, 16 V, diametro 12.5 mm, altezza 20 mm, passo reofori 5 mm, 10 000 h a 105 °C, corrente di ripple 2.6 A (frequenza non indicata) — [secondary, scheda distributore; non visto in citazione] [RS Components](https://uk.rs-online.com/web/p/aluminium-capacitors/1084633)
- Panasonic FM, EEU-FM1C222: 2200 uF, 16 V, 12.5 x 25 mm, passo 5 mm, ripple 3190 mA, impedenza 0.015 Ohm, 7000 h a 105 °C — [secondary, scheda distributore; non visto in citazione] [octopart.com](https://octopart.com/part/panasonic/EEUFM1C222)
- Pololu (interruttori di potenza): per limitare i picchi di tensione, "placing capacitors at the power switch", cavi corti, diodo Schottky sull'uscita, TVS sull'ingresso — [primary, letto direttamente] [pololu.com/product/2815](https://www.pololu.com/product/2815)

### Inferences
- 18 x 100 uF = 1800 uF -> valore commerciale 2200 uF; con due bus 9 x 100 = 900 uF per bus -> 1000-2200 uF per bus — [computed] dalla regola Adafruit.
- Tensione nominale 16 V su rail a 6 V: fattore 2.7; regge anche un errore di selezione a 8.4 V. 10 V sarebbe il minimo accettabile — inferenza.
- Montaggio: reofori corti direttamente sui morsetti a vite VS1 e VS2 (polarita'!). Altezza 20-25 mm: prevedere lo spazio nel CAD o coricare il condensatore.

### Gaps
- Impedenza a 100 kHz del EEUFR1C222 dal datasheet Panasonic: NON TROVATO (solo ripple 2.6 A da distributore).
- Capacita' massima in uscita tollerata all'avvio dal D42V110F6 e dai Hobbywing UBEC: NON TROVATO.

## 5. Alimentazione della logica (SSC-32 VL ed ESP32-S3-CAM)

### Takeaway
La SSC-32 non va alimentata con 5 V regolati su VL: la versione classica ha un regolatore che richiede almeno 5.5 V (morsetto marcato "6vdc thru 9vdc only"), la SSC-32U richiede 5.3 V minimi (nominale 6-12 V). La 2S (6.4-8.4 V) rientra in entrambi i campi: VL va preso dalla batteria dopo fusibile e interruttore, con il jumper VL=VS tolto. La ESP32-S3-CAM va alimentata sul pin 5V da un buck dedicato: il chip ha picchi TX di 340 mA a 3.3 V e Espressif chiede un'alimentazione da almeno 0.5 A; una scheda S3 con camera paragonabile assorbe ~138 mA medi e ~341 mA di picco a 5 V.

### Cited Findings
- Manuale SSC-32 v2 (letto direttamente): morsetto VL "Apply Logic power 6vdc thru 9vdc only"; "The Low Dropout regulator will provide 5vdc out with as little as 5.5vdc coming in ... It can accept a maximum of 9vdc in. The regulator is rated for 500mA, but we are de-rating it to 250mA to prevent the regulator from getting too hot." — [primary, copia] [hobbielektronika.hu](https://hobbielektronika.hu/forum/getfile.php?id=81561)
- Stesso manuale: VL "is used to isolate the logic from the Servo Power Input"; jumper VL=VS: "This requires at least 6vdc to operate correctly. If the microcontroller resets when many servos are moving it may be necessary to power the microcontroller separately using the VL input."; "The onboard regulator can provide 250mA total" — [primary, copia] [hobbielektronika.hu](https://hobbielektronika.hu/forum/getfile.php?id=81561)
- SSC-32U, guida letta direttamente: VL "Nominal: 6-12V; Absolute: 5.3~16V"; la tensione logica e' scelta automaticamente fra VL e VS1 (la piu' alta); "So long as VS1 is above 5.3V (not counting temporary drops in voltage), it is sufficient to power the logic voltage"; V_logic = "MAX(VL, VS1) minus roughly 0.7V"; VS1/VS2 "Absolute: 0~16V"; scheda 3.00" x 2.30" — [primary] [Lynxmotion SSC-32U user guide PDF](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf)
- Indizio sulla scheda dell'utente: un annuncio AliExpress intitolato "SSC32-V2.5 32ch Servo Controller multicanale con interfaccia USB XBEE ..." (USB e XBee sono caratteristiche della SSC-32U) — [secondary, solo titolo visto in una scheda del browser aperta da un altro ricercatore; non e' detto che sia l'articolo dell'utente] [it.aliexpress.com/item/1005001887832328](https://it.aliexpress.com/item/1005001887832328.html)
- ESP32-S3 datasheet v2.2 (letto direttamente), Tabella 5-7, a 3.3 V e 25 °C, TX al 100 % di duty: 802.11b 1 Mbps @21 dBm 340 mA di picco; 802.11g 54 Mbps @19 dBm 291 mA; 802.11n HT20 MCS7 283 mA; HT40 MCS7 286 mA; RX 88-91 mA — [primary] [ESP32-S3 Series Datasheet](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- Stesso datasheet, Tabella 5-2: VDD3P3 3.0 / 3.3 / 3.6 V; "Cumulative input current" minimo 0.5 A — [primary] [ESP32-S3 Series Datasheet](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- Scheda paragonabile (Seeed XIAO ESP32S3 Sense, OV2640), modalita' webcam: a 5 V ~138 mA medi e ~341 mA al momento dello scatto; a riposo ~38 mA; Wi-Fi attivo ~110 mA — [secondary, dati del venditore riportati da un negozio; risoluzione e frame rate non dichiarati; scheda e sensore diversi da quelli dell'utente] [elektor.nl](https://elektor.nl/products/seeed-studio-xiao-esp32s3-sense)
- Pololu D24V22F5 (#2858): ingresso 5.3-36 V; 5 V "with 4% accuracy"; 2.5 A tipici (a 24 V in); quiescente ~1 mA; 17.8 x 17.8 x 8 mm; US$18.95; protezione da inversione; EN con pull-up 270 kOhm — [primary] [pololu.com/product/2858](https://www.pololu.com/product/2858)
- Dropout tipico D24V22F5 (grafico del costruttore, letto direttamente a occhio): ~0.25 V a vuoto, ~0.33 V a 0.5 A, ~0.44 V a 1 A, ~0.62 V a 2 A, ~0.73 V a 2.5 A — [primary, grafico] [Pololu: Typical dropout voltage D24V22F5](https://a.pololu-files.com/picture/0J6871.1200.png)
- Alternativa da negozio RC: Hobbywing UBEC 3A (2-6S) cod. 86010010: ingresso 5.5-26 V, uscita "5V@3A / 6V@3A (adjust via jumper cap)", 43 x 17 x 7 mm, 11 g, ripple < 50 mVp-p a 2 A con 12 V in, protezione da inversione di polarita' — [primary via riassunto di ricerca, non visto in citazione] [hobbywing.com UBEC 3A](https://www.hobbywing.com/en/products/ubec-3a-2-6s99.html)

### Inferences
- VL dalla batteria, SSC-32 classica: 8.4 V (piena) < 9 V massimi; 6.4 V (scarica) > 5.5 V minimi: 0.9 V di margine — [computed]. SSC-32U: V_logic = 8.4 - 0.7 = 7.7 V ... 6.4 - 0.7 = 5.7 V, entro 5.3-16 V — [computed].
- Su una scheda tipo SSC-32U con rail servo a 6.0 V e VL scollegato: V_logic = 6.0 - 0.7 = 5.3 V, cioe' esattamente il minimo: ogni buco di tensione dei servo resetterebbe il micro. Quindi VL dalla batteria anche in quel caso — [computed] dalla guida SSC-32U.
- Dissipazione del regolatore lineare SSC-32 a batteria piena: (8.4 - 5.0) V x I: 0.11 W a 31 mA, 0.85 W a 250 mA — [computed]. Non alimentare la ESP32 dal 5 V della SSC-32.
- 5 V regolati su VL: sotto i minimi dichiarati (5.5 V classica, 5.3 V "U") -> sconsigliato.
- Budget ESP32-S3-CAM sul pin 5V: ~0.15 A medi, ~0.35 A di picco per analogia con la XIAO; progettare per 0.5 A continui e 1 A di picco -> D24V22F5 (2.5 A) o UBEC 3A hanno margine ampio — inferenza; il regolatore 3.3 V di bordo della scheda UICPAL non e' noto.
- D24V22F5 a 0.5 A: Vin minima = 5.0 + 0.33 = 5.33 V -> regola per tutta la scarica della 2S — [computed] dal grafico.
- Separazione dai disturbi servo: (1) buck logica separato, preso dal nodo a stella a monte del regolatore servo; (2) VL separato da VS (jumper VL=VS tolto), come prescrive il manuale; (3) massa unica a stella: il filo GND del collegamento seriale ESP32 <-> SSC-32 non deve portare corrente dei servo; (4) bulk sui morsetti VS; (5) opzionale: diodo Schottky + 470 uF sul ramo VL per superare buchi brevi — inferenze di buona pratica coerenti col manuale SSC-32.

### Gaps
- Variante esatta della scheda "SSC-32 V2.5" (classica o tipo "U", sigla del regolatore 5 V): non nota; il campo di VL va confermato sulla scheda reale.
- Corrente misurata sul pin 5V della scheda UICPAL ESP32-S3-CAM con OV3660 in streaming: NON TROVATO (solo il dato della XIAO con OV2640).
- Tipo e corrente massima del regolatore 3.3 V della scheda UICPAL: NON TROVATO.
- Prezzo e negozio UE per il Hobbywing UBEC 3A: NON TROVATO.

## 6. Interruttore generale

### Takeaway
Prima scelta: Pololu Big MOSFET Slide Switch with Reverse Voltage Protection HP (#2815): 4.5-32 V consigliati, resistenza massima 8.6-13 mOhm, 6 A continui a 55 °C e 16 A a 150 °C, picco 90 A, ~20 x 25 x 4 mm, 2.7 g, US$8.49; la corrente non passa dall'interruttore meccanico, quindi sul pannello basta un qualsiasi interruttorino. Ripiego: bilanciere tondo serie R13-112 con valore DC dichiarato (20 A a 12-14 V DC), foro pannello 20.2 mm, ma resistenza di contatto massima 50 mOhm. Terza via: chiave a ponticello XT60 (30 A continui).

### Cited Findings
- Pololu #2815, testo della pagina letto direttamente: "a pair of P-channel MOSFETs configured as a high-side switch with reverse voltage protection"; tensione massima assoluta 40 V, consigliata 4.5-32 V; "MOSFET combined on resistance (max)" 13 mOhm @ 4.5 V e 8.6 mOhm @ 10 V; corrente continua 6.0 A a 55 °C e 16 A a 150 °C ("At 12 V with ambient temperature of 22°C in still air"); corrente massima 90 A; dimensioni 0.8″ × 1.0″ × 0.16″; peso 2.7 g; corrente in stato ON ~65 µA/V per le versioni Big (attribuzione di colonna dedotta dalla tabella); prezzo US$8.49, 255 pezzi a magazzino — [primary] [pololu.com/product/2815](https://www.pololu.com/product/2815)
- Stessa pagina: per usare un interruttore esterno, slide di bordo su off e SPST "between ground and the switch control terminal"; pin "ON" attivo sopra ~1 V, massimo 30 V; "For applications drawing more than 5 A, you should either use the large holes or both 0.1″-spaced holes"; "the terminal blocks are only rated for 16 A"; "Do not use this switch as an emergency cutoff or similar safety disconnect" — [primary] [pololu.com/product/2815](https://www.pololu.com/product/2815)
- Scheda specifiche #2815: 0.8″ × 0.9″ × 0.16″ senza connettori (la levetta sporge ~1 mm), 2.6 g, 16 A "Continuous at 12 V, without exceeding 150°C", minimo 4.5 V, massimo 40 V ("Recommended maximum is 32 V") — [primary] [pololu.com/product/2815/specs](https://www.pololu.com/product/2815/specs)
- Bilanciere SCI R13-112LP-02-BBRR-0D-L-1 (SPST ON-OFF, LED rosso): 20 A / 12 V DC, foro 20.2 mm, resistenza di contatto max 50 mOhm, 6000 cicli elettrici, -20...85 °C, pannello fino a 3 mm — [secondary, scheda distributore; non visto in citazione] [tme.eu (catalogo SCI)](https://www.tme.eu/html/EN/switch-rocker-sci/ramka_13903_EN_pelny.html)
- R13-112L-02 / B-02 / B2-02 illuminati: "Rating: 20A 14VDC", "Panel Cut Out 20.2mm", "Panel Thickness 0.7-3mm", faston 4.8 mm — [secondary] [pro.maplin.co.uk](https://pro.maplin.co.uk/products/red-led-12v-20mm-round-rocker-switch-spst-20a-r13-112l-02)
- Multicomp Pro R13-112A8: "20A 14VDC, 10A 28VDC", IP65 — [secondary, riassunto del datasheet] [farnell.com datasheet 4552620](https://www.farnell.com/datasheets/4552620.pdf), [Farnell R13-112A8-02-BB-2A](https://ie.farnell.com/multicomp-pro/r13-112a8-02-bb-2a/switch-spst-20a-125v-black-i-0/dp/1634655)
- R13-112A non illuminato: 10 A 250 V AC / 16 A 125 V AC; campo "Contact Current DC Max" vuoto sulla scheda Farnell — [secondary] [Farnell R13-112A](https://pt.farnell.com/en-PT/arcolectric/r13-112a/switch-spst-10a-250vac-black-i/dp/186764)
- XT60 Amass su cavo 12 AWG: 30 A continui (4 ore, sovratemperatura < 60 °C), 60 A per 1 minuto — [secondary, tabella Holybro "Genuine AMASS Connector Rating"] [docs.holybro.com](https://docs.holybro.com/power-module-and-pdb/power-module/connector-and-wire-rating). XT60E-M da pannello: un negozio lo intitola "30A 500V", un altro "20A" — [secondary; le fonti non concordano] [jameco.com](https://www.jameco.com/z/XT60E-M-Amass-XT60-Socket-Male-Terminals-30A-500V-2-Pin-Flanged-for-Panel-Mount_2844431.html), [pro.maplin.co.uk](https://pro.maplin.co.uk/products/male-xt60e-panel-mount-gold-plated-connector-20a-amass)
- Hobbywing UBEC: "The external switch can turn on/off the UBEC easily" — [primary] [manuale Hobbywing](https://oss.hobbywing.com/pdf/pdfen/UBEC10A2-6S.pdf)

### Inferences
- Discrepanza nelle fonti Pololu sulle dimensioni: 0.8″ × 1.0″ (pagina) contro 0.8″ × 0.9″ (scheda specifiche) = 20.3 x 25.4 mm contro 20.3 x 22.9 mm; spessore 4.1 mm — [computed, conversione]. Per il CAD prevedere 21 x 26 x 5 mm e controllare il disegno quotato.
- Caduta e calore sull'interruttore MOSFET con 2S (gate a 6.4-8.4 V, quindi Ron fra 8.6 e 13 mOhm max): a 10.9 A 94-142 mV e 1.0-1.5 W; a 4.5 A medi 39-59 mV e 0.17-0.26 W — [computed: V = R x I, P = R x I²]. La corrente media dell'esapode (4-5 A) sta sotto i 6 A "tiepidi" (55 °C).
- Bilanciere: 50 mOhm e' il massimo di specifica; a 10.9 A varrebbe fino a 0.55 V e 5.9 W — [computed]. Anche se il valore tipico da nuovo e' piu' basso, e' il componente che consuma piu' margine di dropout: per questo e' il ripiego.
- Variante senza interruttore di potenza: lasciare la potenza sempre collegata e comandare con un interruttorino a bassa corrente il pin ENA del Pololu (o l'interruttore esterno dei Hobbywing) piu' il ramo logica (< 1 A). Assorbimento residuo del D42V110F6 spento: 100 µA + 2 µA/V x 8.4 V = ~117 µA — [computed]. Richiede di scollegare comunque la batteria a fine sessione.
- Il vero sezionatore per il rimessaggio resta il T-plug della batteria.

### Gaps
- Datasheet SCI ufficiale della serie R13-112 con il valore DC: NON TROVATO (solo schede distributore).
- Dima di foratura dell'XT60E-M: NON TROVATO.
- Interruttori anti-scintilla dedicati: trovati solo prodotti per skateboard elettrici (es. [tindie.com](https://www.tindie.com/products/makerboy777/xt60-anti-spark-electronic-switch)), specifiche non verificate; a 8.4 V e con pochi mF in ingresso non sono necessari (inferenza).

## 7. Fusibile

### Takeaway
Fusibile automobilistico mini-lama Littelfuse MINI 297 (32 V) da 20 A in portafusibile in linea Littelfuse FHM (IP67), sul positivo, il piu' vicino possibile alla batteria e PRIMA dell'interruttore. 20 A lascia passare lo stallo totale lato batteria (~17 A, 86 %) e i picchi realistici (~11 A, 55 %), e apre in 0.15-5 s a 40 A; protegge cavi e connettori da un cortocircuito, non i servo dallo stallo.

### Cited Findings
- Littelfuse MINI 297 (32 V), tempi di apertura: 110 % minimo 360 000 s (100 h); 135 % 0.75-600 s; 200 % 0.15-5 s; 350 % 0.08-0.5 s (un catalogo piu' vecchio riporta 0.25 s); 600 % 0.03-0.1 s — [primary via estratto di ricerca del datasheet ufficiale; il PDF ha risposto 403, quindi NON visto in citazione] [Littelfuse MINI 297 datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-297-mini32v?assetguid=42c9dd21-a88e-4328-8e67-2f832444faf1)
- MINI 297: 32 V, "fast acting", 10.9 x 3.8 x 8.8 mm; codici del tipo 0297025.WXNV (25 A), 029707.5WXNV (7.5 A) — [secondary, schede distributori] [Farnell 0297002.L](https://de.farnell.com/en-DE/littelfuse/0297002-l/blade-fuse-2a-32vdc-fast-acting/dp/2762034), [element14 0297025.WXNV](https://sg.element14.com/littelfuse/0297025-wxnv/fuse-mini-blade-25a/dp/9943897)
- Portafusibile Littelfuse FHM "In-Line MINI Splashproof Fuse Holder" (datasheet letto direttamente): "Max Operating Voltage: 58V DC", "Fuse Rating Range: 2A - 30A", "Operating Temp: -40 to +125 °C", "Integral cover seals product to IP67 rating"; 0FHM0002ZXJ = cavo 12 AWG arancione, code da 94 mm; 0FHM0001ZXJ = cavo 14 AWG nero, code da 94 mm (abbinamento codice/colonna ricostruito dall'ordine del testo estratto) — [primary, copia LCSC del datasheet Littelfuse] [LCSC PDF 0FHM0002ZXJ](https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2401291424_Littelfuse-0FHM0002ZXJ_C3205323.pdf); pagina prodotto: [littelfuse.com FHM](https://www.littelfuse.com/products/fuses-overcurrent-protection/fuse-holders-fuse-blocks-accessories/fuse-holders/in-line-fuse-holders/mini-fhm/0fhm0001zxj)
- 0FHM0002ZXJ: "30 A, 32 VAC 32 VDC, MINI, wire leaded" — [secondary, titolo scheda] [tanotis.com](https://www.tanotis.com/collections/circuit-protection/products/littelfuse-0fhm0002zxj-fuseholder-automotive-blade-1-fuse-30-a-32-vac-32-vdc-mini-wire-leaded)
- Pololu, sul D42V110F6: la limitazione interna non copre tutti i casi; raccomandati fusibili o interruttori automatici esterni — [primary] [pololu.com/product/5673](https://www.pololu.com/product/5673)
- Portate "chassis wiring": 12 AWG 41 A, 14 AWG 32 A, 16 AWG 22 A — [secondary] [powerstream.com](https://www.powerstream.com/Wire_Size.htm)

### Inferences
- Carico del fusibile da 20 A: picco realistico 10.9 / 20 = 55 %; stallo totale 17.2 / 20 = 86 % (sotto il 110 % che deve reggere 100 h); media 4-5 A = 20-25 % — [computed].
- Tempi di intervento del 20 A: 27 A (135 %) -> 0.75-600 s; 40 A (200 %) -> 0.15-5 s; 70 A (350 %) -> 0.08-0.5 s; cortocircuito franco (centinaia di A) -> < 0.1 s — [computed] dai dati Littelfuse.
- Perche' non 15 A: lo stallo totale (17.2 A) sarebbe al 115 %, zona indefinita fra "regge 100 h" e "apre in 0.75-600 s": interventi casuali senza una protezione reale dei servo. Perche' non 25-30 A: nessun vantaggio e protezione peggiore dei cavi 14-16 AWG.
- Il pacco 5200 mAh 50C puo' erogare nominalmente 5.2 x 50 = 260 A: senza fusibile un cortocircuito fonde cavi e connettori — [computed].
- Codice del fusibile da 20 A secondo lo schema Littelfuse: 0297020.WXNV — inferenza dallo schema dei codici visti, da confermare all'ordine. Un qualsiasi fusibile "MINI" automobilistico da 20 A e' equivalente.
- Portafusibile: scegliere 0FHM0002ZXJ (12 AWG) per avere code di sezione almeno pari al resto del cablaggio; giuntare con saldatura + termorestringente.

### Gaps
- Caduta di tensione / resistenza a freddo del MINI 20 A: NON TROVATO (datasheet 403); manca quindi questo termine nel bilancio del dropout.
- Corrente massima specifica dei singoli codici FHM (oltre al campo 2-30 A della serie): non leggibile nel testo estratto.

## 8. Protezione da sottotensione della LiPo

### Takeaway
Soglie: allarme a 3.5 V/cella (7.0 V), spegnimento dei servo a 3.3 V/cella (6.6 V) sotto carico, mai sotto 3.0 V/cella (6.0 V). Tre livelli indipendenti: (1) cicalino 1-8S "BX100" sulla presa di bilanciamento JST-XH (soglia regolabile OFF / 2.7-3.8 V per cella); (2) partitore 100 kOhm / 47 kOhm + 100 nF su GPIO1 o GPIO2 (ADC1) della ESP32-S3 per avviso e arresto ordinato; (3) spegnimento del rail servo dal pin ENA del regolatore Pololu.

### Cited Findings
- Grepow (costruttore di batterie LiPo): "The absolute minimum voltage for discharging a LiPo cell is typically 3.0 volts per cell"; "Set the cutoff voltage to around 3.3 to 3.5 volts per cell to avoid over-discharging"; conservazione "approximately 3.7 to 3.85 volts per cell"; sotto 3.0 V "permanent damage" — [primary di un costruttore di batterie (non OVONIC), blog aziendale] [grepow.com](https://www.grepow.com/blog/how-to-discharge-a-lipo-battery)
- Altre indicazioni: non scendere sotto 3.0 V/cella (dispensa di sicurezza universitaria); un rivenditore europeo consiglia di non scendere sotto ~3.5 V/cella e di usare ~80 % della capacita'; hobbisti usano 3.2-3.4 V — [secondary / community, da riassunto di ricerca] [uvm.edu PDF](https://www.uvm.edu/d10-files/documents/2024-12/lipo_battery_safety.pdf), [elfa.nl FAQ](https://www.elfa.nl/en/faq/how-far-discharging-lipo), [rctech.net](https://www.rctech.net/forum/radio-electronics/927696-lowest-voltage-per-cell-lipo-printthread.html)
- Cicalino BX100 1-8S: "Alarm set value range per cell: OFF~2.7~3.8V", regolazione a pulsante; precisione di lettura +/-0.01 V; per prese di bilanciamento JST-XH; 40 x 25 x 11 mm; ~8 g; doppio cicalino; 3.99 EUR; assorbimento NON dichiarato — [secondary] [originhobbies.com](https://originhobbies.com/shop/charging/battery-monitors/1-8s-lipo-battery-voltage-tester-low-voltage-buzzer-alarm/)
- Batteria OVONIC 2S 5200 mAh 50C: presa di bilanciamento "JST-XHR-3P", cavi 12 AWG, T-plug; la confezione da 2 pacchi include "1× Lipo Voltage Checker Buzzer Alarm"; carica fino a "4.2V per cell" — [primary/secondary, pagine OVONIC e Amazon lette dal ricercatore "batteria_cablaggio"] [us.ovonicshop.com](https://us.ovonicshop.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-2pcs-lipo-battery)
- ESP-IDF v4.4, ESP32-S3: campo misurabile per attenuazione: 0 dB 0-950 mV; 2.5 dB 0-1250 mV; 6 dB 0-1750 mV; 11 dB 0-3100 mV; ADC1 = "10 channels: GPIO1 - GPIO10"; ADC2 condiviso col Wi-Fi: la lettura "may fail between esp_wifi_start() and esp_wifi_stop()"; "a bypass capacitor (e.g. a 100 nF ceramic capacitor) to the ADC input pad in use, to minimize noise"; multisampling consigliato — [primary] [docs.espressif.com ESP-IDF v4.4 ADC](https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32s3/api-reference/peripherals/adc.html)
- D42V110F6: ENA con pull-up 1 MOhm a VIN; in shutdown "approximately 100 µA plus 2 µA per volt on VIN" — [primary] [pololu.com/product/5673](https://www.pololu.com/product/5673)
- D36V50Fx: EN con soglia precisa: sotto ~1.2 V sleep, sopra ~1.35 V riattivazione; pull-up 100 kOhm a VIN — [primary] [pololu.com/product/4091](https://www.pololu.com/product/4091)

### Inferences
- Soglie di pacco 2S: allarme 2 x 3.5 = 7.0 V; stacco servo 2 x 3.3 = 6.6 V; limite assoluto 2 x 3.0 = 6.0 V — [computed] da Grepow. Sotto carico la tensione si abbassa e poi risale: filtrare in firmware (media mobile di 2-5 s) prima di spegnere.
- La soglia a 7.0 V lascia anche ~0.45 V di margine di dropout al regolatore a 6 V (sezione 1): le due esigenze coincidono.
- Pin ADC: la camera occupa GPIO4-13 e 15-18, quindi dei canali ADC1 (GPIO1-10) restano GPIO1, GPIO2, GPIO3; GPIO3 e' pin di strapping -> usare GPIO1 (ADC1_CH0) o GPIO2 (ADC1_CH1). GPIO14 e' ADC2 (conflitto col Wi-Fi) — inferenza da [ESP-IDF ADC](https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32s3/api-reference/peripherals/adc.html) + mappa pin del progetto.
- Partitore del pacco: R1 = 100 kOhm (verso +batt), R2 = 47 kOhm (verso GND), 100 nF fra pin ADC e GND. V_adc = V_batt x 47 / 147 = 0.3197 x V_batt: 8.4 V -> 2.686 V; 7.0 V -> 2.238 V; 6.6 V -> 2.110 V; 6.0 V -> 1.918 V, tutto entro 3100 mV con attenuazione 11 dB — [computed].
- Corrente nel partitore: 8.4 V / 147 kOhm = 57 µA — [computed]. Collegarlo DOPO l'interruttore generale.
- Errore: resistenze 1 % + ADC non calibrato possono dare > 0.1 V sul pacco: calibrare a due punti con un multimetro (es. 8.4 V e 6.6 V).
- Misura per cella (opzionale): secondo partitore sul filo centrale della presa di bilanciamento (cella 1, max 4.2 V): R1 = 47 kOhm, R2 = 100 kOhm -> 4.2 x 100 / 147 = 2.857 V; cella 2 = pacco - cella 1 — [computed].
- Stacco hardware con soglia precisa (solo famiglia D36V50Fx): resistenza R fra EN e GND con il pull-up interno da 100 kOhm: V_off = 1.2 x (100k + R) / R. R = 22 kOhm -> stacco 6.65 V, riattivazione 1.35 x 122 / 22 = 7.49 V; R = 24 kOhm -> 6.20 V / 6.98 V — [computed] dai dati Pololu.
- Con il D42V110F6 la soglia di ENA non e' pubblicata: lo stacco va comandato dalla ESP32 (transistor NPN / MOSFET che porta ENA a massa). Con i Hobbywing non c'e' un ingresso di enable documentato: resta solo l'arresto software dei servo (comando di rilascio alla SSC-32) piu' il cicalino.
- Il cicalino sulla presa di bilanciamento assorbe corrente in permanenza (display e micro): va staccato quando il robot non e' in uso.

### Gaps
- Tensione minima di scarica dichiarata da OVONIC per questo pacco: NON TROVATO.
- Assorbimento del cicalino BX100: NON TROVATO.
- Moduli di stacco hardware pronti per 2S con soglia regolabile e >= 15 A, con il loro assorbimento a riposo: NON TROVATO.

## 9. Sezioni dei cavi, connettori, morsetti

### Takeaway
Cavo siliconico 14 AWG dalla batteria al regolatore (32 A "chassis", 8.3 mOhm/m), due coppie 16 AWG dal regolatore a VS1 e VS2 (22 A ciascuna, <= 8.5 A reali), 22-24 AWG per logica e segnali. Convenzione T-plug: femmina sulla batteria (sorgente), maschio sul robot. I morsetti a vite da PCB passo 5 mm sono tipicamente da 16-17.5 A e accettano fino a ~1.5-2.5 mm² (16-14 AWG): un altro motivo per non far passare 17 A da un solo morsetto della SSC-32.

### Cited Findings
- Tabella AWG (diametro, resistenza, portata "chassis wiring" / "power transmission"): 12 AWG 2.05 mm, 5.21 Ohm/km, 41 / 9.3 A; 14 AWG 1.63 mm, 8.28 Ohm/km, 32 / 5.9 A; 16 AWG 1.29 mm, 13.17 Ohm/km, 22 / 3.7 A; 18 AWG 1.02 mm, 20.94 Ohm/km, 16 / 2.3 A; 20 AWG 0.81 mm, 33.29 Ohm/km, 11 / 1.5 A; 22 AWG 0.65 mm, 52.94 Ohm/km, 7 / 0.92 A; 24 AWG 0.51 mm, 84.2 Ohm/km, 3.5 / 0.577 A. La pagina cita come fonte l'Handbook of Electronic Tables and Formulas; valori "just a rule of thumb"; colonna chassis "meant for wiring in air, and not in a bundle" — [secondary] [powerstream.com/Wire_Size.htm](https://www.powerstream.com/Wire_Size.htm)
- Cavo siliconico: regola empirica 25 A per mm² di rame (es. 0.5 mm² -> ~12 A); isolamento "usually like 200 degrees C" — [secondary] [sparks.gogo.co.nz](https://sparks.gogo.co.nz/silicone-wire-current-capacity.html)
- Batteria OVONIC: cavi "12 AWG", "Deans(T) Plug"; il genere del connettore non e' dichiarato nelle schede — [primary/secondary, pagina OVONIC] [us.ovonicshop.com](https://us.ovonicshop.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-2pcs-lipo-battery)
- T-plug, convenzione di genere: "A Female (source) and Male (device) Deans Ultra Connector Set"; portata "rated for 60 Amps of continuous load, up to 75 Amp & higher bursts"; i cloni "will not fit well with other copies or even the originals" — [secondary, sito hobbistico] [rchelicopterfun.com](https://www.rchelicopterfun.com/deans-connector.html)
- W.S. Deans Ultra Plug (costruttore): resistenza 0.10 mOhm, peso 4.73 g, corpo 0.650" (16.5 mm), lunghezza totale 1.030" (26.2 mm), altezza 0.650", larghezza 0.300" (7.6 mm); corrente nominale NON dichiarata; coppia maschio + femmina P.N. 1313 — [primary] [wsdeans.com](https://www.wsdeans.com/collections/ultra-plug)
- XT60 Amass su 12 AWG: 30 A continui, 60 A per 1 minuto — [secondary] [docs.holybro.com](https://docs.holybro.com/power-module-and-pdb/power-module/connector-and-wire-rating)
- D42V110F6: fori di potenza per cavo 14 AWG o morsetti passo 5 mm — [primary] [pololu.com/product/5673](https://www.pololu.com/product/5673)
- Morsetti a vite passo 5 mm forniti da Pololu: "only rated for 16 A"; pin header 0.1": "rated for 3 A" ciascuno — [primary] [pololu.com/product/2815](https://www.pololu.com/product/2815), [pololu.com/product/4091](https://www.pololu.com/product/4091)
- Morsetti da PCB di marca, 2 poli passo 5.08 mm: Phoenix Contact MKDS 1.5/2-5.08 17.5 A (250 V, da 0.14 mm²); SMKDS 2.5/2-5.08 20 A con sezione nominale 2.5 mm²; MKDS 2.5 (5 poli) 24 A, 26-14 AWG — [secondary, schede distributori ed estratti di catalogo; non visto in citazione] [RS MKDS 1.5/2-5.08](https://ph.rs-online.com/web/p/products/8044991), [RS MKDS 2.5/5-5.08](https://sg.rs-online.com/web/p/pluggable-terminal-blocks/8818650)
- Manuale SSC-32 v2: "If the wires carrying the current are too small, or connections are made with stripped and twisted wire ... the same problem may occur" — [primary, copia] [hobbielektronika.hu](https://hobbielektronika.hu/forum/getfile.php?id=81561)

### Inferences
- Sezioni di rame dai diametri: 12 AWG 3.31 mm², 14 AWG 2.08 mm², 16 AWG 1.31 mm², 18 AWG 0.82 mm², 20 AWG 0.52 mm², 22 AWG 0.33 mm² (A = pi/4 x d²) — [computed]. Con la regola 25 A/mm²: 14 AWG ~52 A, 16 AWG ~33 A, 18 AWG ~20 A, 20 AWG ~13 A, 22 AWG ~8 A — [computed]: piu' ottimista della colonna "chassis"; usare quest'ultima.
- Caduta batteria -> regolatore: 0.4 m totali (andata + ritorno) di 14 AWG = 0.4 x 8.28 = 3.3 mOhm -> 36 mV a 10.9 A, 57 mV a 17.2 A — [computed].
- Caduta regolatore -> SSC-32: 0.3 m totali di 16 AWG per bus = 0.3 x 13.17 = 4.0 mOhm -> 34 mV a 8.5 A — [computed].
- Il criterio che decide e' la caduta di tensione, non il riscaldamento: ogni 10 mOhm in piu' a 10 A costa 0.1 V sul margine di dropout.
- Se i morsetti della SSC-32 non accettano il 16 AWG (1.31 mm²), usare 18 AWG (16 A "chassis", 20.9 mOhm/m: 0.3 m -> 6.3 mOhm -> 53 mV a 8.5 A) e tenere i fili cortissimi — [computed].
- Trefoli nei morsetti a vite: usare puntalini a bussola anziche' stagnare (buona pratica; non verificata su fonte del costruttore).
- T-plug cloni: saldare sul robot un maschio dello stesso lotto/marca della femmina del pacco oppure provarne l'accoppiamento prima di saldare.

### Gaps
- Passo, sezione massima e corrente nominale dei morsetti montati sulla SSC-32 dell'utente: NON TROVATO nel manuale; da misurare sul pezzo.
- Corrente nominale del T-plug da fonte del costruttore: non dichiarata da W.S. Deans; il valore 60 A viene da un sito hobbistico e non vale per i cloni.
- Genere del T-plug sul pacco OVONIC: non dichiarato nelle schede (atteso femmina per convenzione).

## 10. Domande a cui puo' rispondere solo l'utente

### Takeaway
Servono alcune verifiche sul pezzo reale prima dell'ordine.

### Cited Findings
- (nessuna: elenco di richieste)

### Inferences
- Foto fronte/retro della scheda "SSC-32 V2.5" e link d'acquisto: sigla del regolatore 5 V vicino al morsetto VL, presenza dei jumper VS1=VS2 e VL=VS, presenza di USB / zoccolo XBee (tipo "U"), passo dei morsetti a vite (3.5 o 5.0/5.08 mm) e diametro del foro per il filo.
- Genere del T-plug montato sulla batteria OVONIC (atteso: femmina) e sezione stampata sui cavi (attesa: 12 AWG). La confezione comprendeva il cicalino "Lipo Voltage Checker"?
- Misura al banco della corrente di stallo di un MG90S del lotto acquistato, a 5.0 e a 6.0 V (stallo di 1-2 s, alimentatore con limite di corrente).
- Spazio nel corpo del robot per il regolatore (Pololu 31.8 x 43.2 x 9 mm con fori M2 a 38.9 x 25.4 mm; Hobbywing V2 Car 45 x 20 x 16.2 mm ciascuno) e per i due condensatori (12.5 x 20-25 mm); il pannello puo' ospitare un foro tondo da 20.2 mm (bilanciere) o basta un interruttorino per il MOSFET switch?
- Preferenza fra 6.0 V (piu' coppia) e 5.0-5.3 V (piu' margine, servo piu' freddi), e fra ordine dagli USA (Pololu, documentato) e negozio RC nell'UE (Hobbywing).

### Gaps
- —
