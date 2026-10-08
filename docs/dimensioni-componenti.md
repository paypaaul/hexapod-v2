# Dimensioni dei componenti — versione MG996R

Quote reali dei componenti, con la fonte. Legenda stato: **V** verificato su fonte primaria, **S** stimato o da fonte secondaria, **C** da confermare sul pezzo reale. Tutte le quote marcate C diventano parametri utente del modello.

## Servo MG996R (AZDelivery)

Fonti, lette l'8 ottobre 2026: datasheet AZDelivery [Servo_MG996R_Datenblatt.pdf](https://cdn.shopify.com/s/files/1/1509/1638/files/Servo_MG996R_Datenblatt.pdf) (pagina 3: dati e disegno quotato), pagina prodotto [AZDelivery](https://www.az-delivery.de/products/az-delivery-servo-mg996r), pagina [Tower Pro](https://www.towerpro.com.tw/product/mg996r/). I servo dell'utente sono AZDelivery: dove le fonti divergono vale la misura sul pezzo.

L'utente non può misurare i servo: le quote vengono dal datasheet, dalla tabella Tower Pro e da un modello STEP di terzi, e le sedi si progettano in modo che le differenze tra le fonti non contino (vedi in fondo alla sezione). Prima delle parti vere si stampa un provino della culla.

Modello 3D: "Servo Motor MG996R 3D Model.step" di Dejan Nedelkovski (HowToMechatronics, 2020), scaricato dalla copia nel repository GitHub [Matthew-Garcia/SCARA-Robot](https://github.com/Matthew-Garcia/SCARA-Robot/tree/main/3D_Models) insieme alla squadretta di plastica ("Servo MG996R Horn.step"). Sta in `cad/modelli/mg996r/` (fuori da git). Unità mm; Y = altezza dal fondo, X = lunghezza, origine al centro della cassa in pianta. Quote lette dalla geometria del file l'8 ottobre 2026.

| Quota | AZDelivery (disegno) | Tower Pro (tabella) | Modello STEP | Stato |
|---|---|---|---|---|
| Lunghezza della cassa | 40,3 | B = 40,9 | 41,0 | V, divergono di 0,7 |
| Larghezza | 20 | D = 20 | 20,5 | V |
| Fondo → sommità della cassa | 36,6 | C = 37 | 37,0 | V |
| Fondo → lato inferiore delle alette | 26,6 | F = 26,8 | **28,8** | V, **divergono di 2,2** |
| Spessore delle alette | — | — | 2,4 | S |
| Lunghezza totale sulle alette | 53,6 | E = 54 | 54,6 | V |
| Fondo → cima dell'albero | 42,9 (ingombro) | A = 42,7 | **45,2** | V, divergono di 2,5 |
| Lato inferiore delle alette → cima dell'albero | 16,3 | 15,9 | 16,4 | V: **concordano entro 0,5** |
| Asse dell'albero dall'estremità vicina | — | — | 10,25 | S |
| Fori delle alette | — | — | 4 × Ø4,2, interasse 48,0 × 10,0, aperti verso l'estremità con un'asola da 2,5 | S |
| Millerighe | — | — | Ø6,0, lungo 4,0 (atteso 25 denti: da contare) | S |
| Torretta del riduttore | — | — | Ø20,5 fino a 39,3; Ø13 fino a 40,6; Ø10,7 fino a 41,2 | S |
| Uscita del cavo | — | — | sul lato corto vicino all'albero, centro a 5,3 dal fondo; fermacavo 7 × 4,2 sporgente 1 mm | S |
| Lunghezza del cavo | — | 32 cm (JR) | — | S |
| Peso | 55 g | 55 g | — | V |

Conseguenze per il CAD:

- **Il riferimento è il lato inferiore delle alette.** Da lì all'albero le tre fonti concordano entro 0,5 mm; sotto le alette la cassa è alta 26,6 o 28,8 mm a seconda della fonte. Le culle quindi appoggiano il servo sulle alette, lasciano libero il fondo (tasca profonda almeno 29,5 mm, oppure aperta) e il gioco residuo sull'asse dell'albero si assorbe con spessori o con un'asola.
- Sedi in pianta disegnate sulla cassa più grande (41,0 × 20,5) più il gioco di stampa; nervature di schiacciamento per stringere il servo più piccolo.
- Fori delle alette ad asola lungo l'asse del servo (interasse 48,0 nel modello; non pubblicato dai produttori). I gommini si tolgono: il servo si avvita rigido.
- Tutte le quote di questa tabella sono parametri utente (prefisso `srv_`): se un giorno arriva una misura si cambia il numero.

Dati non meccanici (datasheet AZDelivery, V): coppia di stallo 9,4 kgf·cm a 4,8 V e 11 kgf·cm a 6 V; velocità 0,17 s/60° a 4,8 V e 0,14 s/60° a 6 V; tensione 4,8–7,2 V (Tower Pro: 4,8–6,6 V); corrente in movimento 500–900 mA a 6 V; **corrente di stallo 2,5 A a 6 V** (Tower Pro dichiara 1,4 A: da misurare); banda morta 5 µs; due cuscinetti a sfere; 0–55 °C; fili arancio = segnale, rosso = positivo, marrone = massa; periodo 20 ms. Corsa circa 180° (pagina AZDelivery).

## Batteria OVONIC 2S 5200 mAh 50C hardcase (quella che l'utente ha)

Fonti primarie lette l'8 ottobre 2026 (us.ovonicshop.com e ampow.com, più inserzioni): le schede ufficiali non concordano tra loro.

| Quota / dato | Valore | Stato |
|---|---|---|
| Ingombro | 137–139 × 46–47,3 × 24–25,4 mm | V (più schede), C calibro sul pacco |
| Tolleranza dichiarata | ±5 / ±2 / ±2 mm → inviluppo massimo 144 × 49,3 × 27,4 mm | V |
| Massa | 245–259 g ± 20 | V, da pesare |
| Scarica | 50C continui (260 A), 100C di picco | V |
| Cavi | 12 AWG; escono tutti da un lato corto; lunghezza non dichiarata (circa 120 mm dalle immagini) | V sezione, S il resto |
| Connettori | T-plug (dalle immagini femmina sul pacco: C), bilanciamento JST-XH 3 poli | V tipo, C genere |

Il vano si disegna sull'inviluppo massimo con battuta, schiuma e fermo; le quote definitive si prendono con il calibro sul pacco reale.

## Scheda UICPAL ESP32-S3-CAM N16R8 RE1.3

Fonte: immagini dell'inserzione AliExpress 1005008519401021 (venditore "Uncle Electronic Tech Store"), lette l'8 ottobre 2026. Fonte primaria del venditore, ma le quote di un'inserzione vanno confermate con il calibro sulla scheda reale.

| Quota / dato | Valore | Stato |
|---|---|---|
| PCB | 62,6 × 28,3 mm | V inserzione, C calibro |
| Quota "24,7" sul disegno | probabile interasse tra le due file di pin (da confermare; lo standard DevKitC è 25,4) | C |
| Passo pin | 2,54 mm, 2 × 20 pin | V inserzione |
| USB | 2 × USB-C sul lato corto opposto all'antenna: "OTG" (USB nativa, GPIO19/20) e "TTL" (CH340, GPIO43/44) | V inserzione |
| Modulo | ESP32-S3-N16R8 (16 MB flash, 8 MB PSRAM), connettore antenna IPEX | V inserzione |
| Camera | connettore FPC 24 pin DVP al centro della scheda; dichiarato compatibile OV2640 / OV7725 / OV3660 | V inserzione |
| Altro | slot TF sul retro, LED WS2812 (GPIO48), pulsanti RST e BOOT | V inserzione |
| Fori di fissaggio | da verificare sulla scheda reale | C |

Pinout (dall'immagine "Pin definitions" dell'inserzione), antenna in alto:

| Sinistra (dall'alto) | Funzione | Destra (dall'alto) | Funzione |
|---|---|---|---|
| 3V3 | alimentazione | GPIO43 | U0TXD (CH340), LED TX |
| RST | reset | GPIO44 | U0RXD (CH340), LED RX |
| GPIO4 | CAM_SIOD | GPIO1 | ADC1_CH0 — **libero** |
| GPIO5 | CAM_SIOC | GPIO2 | ADC1_CH1, LED "ON" |
| GPIO6 | CAM_VSYNC | GPIO42 | MTMS — libero se non si usa JTAG |
| GPIO7 | CAM_HREF | GPIO41 | MTDI — libero se non si usa JTAG |
| GPIO15 | CAM_XCLK | GPIO40 | SD_DATA |
| GPIO16 | CAM_Y9 | GPIO39 | SD_CLK |
| GPIO17 | CAM_Y8 | GPIO38 | SD_CMD |
| GPIO18 | CAM_Y7 | GPIO37 | PSRAM (non usabile) |
| GPIO8 | CAM_Y4 | GPIO36 | PSRAM (non usabile) |
| GPIO3 | strapping (JTAG) | GPIO35 | PSRAM (non usabile) |
| GPIO46 | strapping (LOG) | GPIO0 | strapping (BOOT) |
| GPIO9 | CAM_Y3 | GPIO45 | strapping (VSPI) |
| GPIO10 | CAM_Y5 | GPIO48 | WS2812 |
| GPIO11 | CAM_Y2 | GPIO47 | **libero** |
| GPIO12 | CAM_Y6 | GPIO21 | **libero** |
| GPIO13 | CAM_PCLK | GPIO20 | USB D+ (porta OTG) |
| GPIO14 | **libero** | GPIO19 | USB D− (porta OTG) |
| 5V | alimentazione | GND | massa |

Aggiunte dalla verifica (ricerca della prima versione, nel branch `mg90s`): l'antenna del modulo sporge dal PCB di 4,7–4,9 mm (ingombro totale circa 67,5 mm); nessun foro di fissaggio; le due USB-C stanno affiancate sul lato corto opposto all'antenna; il connettore FPC della camera è al centro e il flat esce verso il lato dell'antenna. Spessore del PCB, altezza dei componenti e posizione quotata delle USB-C non sono pubblicati: **da misurare** (nel modello sono parametri con valori tipici: PCB 1,6 mm, USB-C 9 × 7,4 × 3,3 mm).
Modello 3D: non trovato. Si modella un ingombro semplificato.

## Servo controller "SSC32-V2.5"

Fonte: disegno quotato e foto dell'inserzione AliExpress 1005001888185034 (quella da cui l'utente ha comprato), letti l'8 ottobre 2026. Coerente con la misura indipendente fatta sulle foto di un'altra inserzione (PCB 71,6 × 54,6 mm, fori 65,2 × 48,3 mm).

| Quota / dato | Valore | Stato |
|---|---|---|
| PCB | 72 × 55 mm | S (disegno del venditore), C calibro |
| Fori di fissaggio | 4, interasse 65,5 × 48,5 mm, cioè a 3,25 mm dai bordi; Ø circa 3 mm | S, C |
| Header servo, lato lungo "alto" | canali 15…0 in 4 gruppi da 4; dal bordo verso l'interno: massa, VS1, segnale | S (serigrafia nel disegno) |
| Header servo, lato lungo "basso" | canali 31…16; dal bordo verso l'interno: massa, VS2, segnale | S |
| Morsettiera | 6 poli sul lato corto vicino ai canali 0 e 16; dall'angolo del canale 0: VS1−, VS1+, VL−, VL+, VS2−, VS2+. Dal disegno il passo è circa 3,5 mm: morsetti piccoli, che di solito portano 8–10 A e accettano al massimo 1–1,5 mm² | S, C sulla serigrafia reale |
| Ponticelli | "VS VL" vicino al canale 0; "VS1 VS2" vicino al canale 16: da togliere | S |
| Seriale TTL | tre pin RX, TX, GND accanto alla morsettiera, lato canali 0–15 | S |
| Micro-USB | sul lato corto opposto alla morsettiera, verso i canali 16–31; sporge di poco dal bordo | S |
| Altro | zoccolo XBee, pulsante BAUD, quarzo 14,7456 MHz, due elettrolitici da 220 µF, regolatore in contenitore DPAK | S |
| Altezza | non pubblicata. Con le spine dei servo inserite servono circa 25 mm liberi sopra il PCB lungo i due lati lunghi (spina 14 mm più la curva del cavo) | C |

Riletto l'8 ottobre 2026 (sera) sulle cinque immagini della galleria, per decidere come portare la potenza ai servo:

- gli header dei servo sono **a foro passante** (i pin si vedono attraversare la scheda): le loro saldature stanno sul retro, quindi si possono alimentare le file dal lato saldature;
- su ogni lato lungo le tre file sono, dal bordo verso l'interno: massa, VS (VS1 per i canali 0–15, VS2 per i 16–31), segnale; quattro gruppi da quattro canali;
- i ponticelli "VS1 VS2" (due, vicino al canale 16) uniscono i due rail: si tolgono; il ponticello "VS VL" (vicino al canale 0) si toglie;
- morsettiera a sei poli lunga circa 21,4 mm sul disegno quotato: passo 3,5 mm (S);
- il retro della scheda non è fotografato: che non ci siano componenti sotto gli header è un'assunzione da controllare all'arrivo.

Modello 3D: non esiste. Si modella un ingombro semplificato con fori, header, morsettiera e micro-USB.

## Camera UICPAL "OV3660-75MM"

Fonte: disegni quotati dell'inserzione AliExpress 1005007456301694 (quella da cui l'utente ha comprato), letti l'8 ottobre 2026.

| Quota / dato | Valore | Stato |
|---|---|---|
| Lunghezza totale | 75 mm | S (disegno del venditore), C |
| Testa | 8,5 × 8,5 mm (±0,2) in pianta; retro metallico 8 × 8 mm | S |
| Variante dell'utente | lente da 120° "GOOD": testa compatta, come quella da 68° (la "120°" semplice e la "160°" hanno invece la cupola grande) | dato dell'utente + foto dell'inserzione |
| Altezza della testa | circa 6 mm per la testa compatta (modulo standard: 5,35); 12,4 ± 0,3 mm solo per le lenti a cupola | S, C: misurare all'arrivo |
| Campo visivo | 120° dichiarati; un acquirente riporta circa 90° utili nel video. Per la verifica delle zampe anteriori si usa 120° | S |
| Flat | largo 6 mm, spesso 0,15 mm | S |
| Linguetta di contatto | 12,5 × 5 mm con rinforzo; 24 contatti passo 0,5 mm sul lato **opposto** alla lente | S |
| Tensioni del modulo | DVDD 1,5 V, DOVDD 1,8–2,8 V, AVDD 2,8 V (la scheda UICPAL dà 1,2 V sul pin DVDD: da provare) | S |

Modello 3D: non trovato. Ingombro semplificato con altezza della testa e diametro della lente come parametri.

## Regolatori e minuteria

| Componente | Quote (mm) | Fonte | Stato |
|---|---|---|---|
| Pololu D42V110F6 (#5673) | 43,2 × 31,8 × 11,4 (reofori compresi); 15 g; 4 fori M2 a 38,86 × 25,40; piazzole di potenza a 2,54 dal bordo lungo | Pololu, STEP in `cad/modelli/` misurato nella prima versione | V |
| Pololu D24V150F6 (#2882), alternativa a parità di ingombro | 43,2 × 31,8 × 11; stessi fori e stessa disposizione dei pin secondo Pololu | Pololu | V |
| Pololu D24V22F5 (5 V logica) | 17,8 × 17,8 × 8; 2 fori M2 | Pololu | V |
| Interruttore Pololu #2813 | 20,3 × 25,4 × 4,1 | Pololu | V |
| Inserto a caldo M2 (CNC Kitchen) | Ø3,6 × 3,0; foro 3,2; parete minima 1,3 | produttore / rivenditore | V / S |
| Inserto a caldo M3 (CNC Kitchen) | Ø4,6 × 5,7; foro 4,0; parete minima 1,6 | idem | V / S |
| Spina servo JR femmina | 7,90 × 2,75 × 14,0; passo 2,54 | disegno Pololu 0J9699 | V |
| Collare maschio della prolunga | 10,30 × 4,00 × 18,0 | disegno Pololu 0J9700 | V |
| Cuscinetto flangiato NMB LF-1050ZZ (= MF105ZZ) | 5 × 10 × 4; flangia Ø11,6 × 0,8; carico dinamico 714 N, statico 276 N | [scheda MinebeaMitsumi](https://product.minebeamitsumi.com/en/product/category/bearing/miniature_small/parts/LF1050ZZ.html) | V; i MF105ZZ generici hanno flange da 11,2 a 11,7: la sede della flangia è un parametro |
| Squadretta metallica a disco, 25 denti | Ø circa 20; fori M3 | varia da prodotto a prodotto | C: si quota sul prodotto scelto |
| Fusibile a lama standard (ATO) | 19,1 × 5,1 × 18,5 | standard | S |

Regole per il CAD ereditate dalla prima versione: foro per inserto = diametro di datasheet + 0,2 mm, profondità = inserto + 1 mm; gioco di stampa di partenza 0,15–0,2 mm per lato sulle sedi dei servo, da tarare con un provino; sedi dei cuscinetti nominali, forzamento da provino; sull'anello interno appoggia solo un rialzo.

## Volume di stampa

FlashForge Creator 5 Pro: 256 × 256 × 256 mm secondo più schede di rivenditori (S: da confermare sulla pagina del produttore o sulla macchina). Un pezzo lungo fino a circa 250 mm sta dritto; fino a circa 330 mm in diagonale se stretto.
