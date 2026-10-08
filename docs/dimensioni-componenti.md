# Dimensioni dei componenti

Quote reali dei componenti, con la fonte. Legenda stato: **V** verificato su fonte primaria o misurato sul modello, **S** stimato / fonte secondaria, **C** da confermare sul pezzo reale.

## Servo Tower Pro MG90S

Fonte: modello STEP dell'utente nel progetto Fusion "Hexabot v2" (`Tower Pro MG90S Micro servo`), misurato via API il 2026-10-08. Il modello è un import STEP di terzi: le quote vanno confrontate con il datasheet e, prima di stampare le sedi, con un calibro su un servo reale (i cloni variano di qualche decimo).

Sistema di riferimento del modello: X = lunghezza, Y = altezza (albero verso +Y), Z = larghezza. Origine al centro della cassa.

| Quota | Valore (mm) | Stato |
|---|---|---|
| Cassa, lunghezza (X) | 22,6 (da −11,3 a +11,3) | V modello, C calibro |
| Cassa, larghezza (Z) | 12,15 (±6,075); 12,3 con l'etichetta | V modello, C calibro |
| Cassa, altezza (Y) fino al piano superiore | 22,55 (da −11,275 a +11,275) | V modello, C calibro |
| Lunghezza totale sulle orecchie | 32,2 (±16,1) | V modello |
| Orecchie: spessore | 2,5 (Y da 7,125 a 9,625) | V modello |
| Orecchie: lato inferiore dal fondo cassa | 18,4 | V modello |
| Orecchie: lato superiore dal fondo cassa | 20,9 | V modello |
| Fori orecchie: diametro | 2,5 (svasatura Ø4,3 profonda 1,05 dal lato inferiore) | V modello |
| Fori orecchie: interasse | 27,5 (X = ±13,75, Z = 0) | V modello |
| Fori orecchie: asola verso l'estremità | larghezza 1,4 | V modello |
| Asse albero d'uscita: posizione | X = +5,375 dal centro cassa, Z = 0 | V modello |
| Torretta riduttore (cilindro grande) | Ø11,8, alta 5,5 (dal piano cassa a 28,05 dal fondo) | V modello |
| Torretta secondaria | Ø5,9 a X = −0,525, stessa altezza | V modello |
| Millerighe: diametro esterno | 4,9 | V modello, C datasheet |
| Millerighe: quota inizio / fine dal fondo cassa | 28,3 / 32,25 | V modello |
| Altezza totale (fondo cassa → cima albero) | 32,25 | V modello |
| Foro vite albero | Ø2,0 (modello) | C |
| Uscita cavo | lato corto X = +11,3 (quello vicino all'albero), a 4,75 dal fondo cassa; 3 fili Ø1 passo 1,02 | V modello |
| Viti fondello | 4 × Ø2 agli angoli (X = ±10, Z = ±4,5) | V modello |

### Confronto con le quote ufficiali Tower Pro

Fonte primaria: pagina prodotto [towerpro.com.tw/product/mg90s-3](https://www.towerpro.com.tw/product/mg90s-3/) e disegno quotato incorporato (lettere A–F), ricontrollati dal verificatore indipendente (`research_notes/.../verifica_servo_mg90s.md`).

| Quota Tower Pro | Significato | Ufficiale (mm) | Modello STEP (mm) | Clone Sky Star (mm) |
|---|---|---|---|---|
| A | altezza totale, fondo → punta dell'albero | 32,5 | 32,25 | 32,9 (con squadretta) |
| B | lunghezza della cassa | 22,8 | 22,6 | 22,4 |
| C | altezza fondo → sommità del coperchio riduttore | 28,4 | 28,05 | — |
| D | larghezza | 12,4 | 12,15 | 12,5 |
| E | lunghezza totale sulle alette | 32,1 | 32,2 | 31,8 |
| F | fondo → lato inferiore dell'aletta | 18,5 | 18,4 | 19,8 |
| — | interasse fori alette | non pubblicato | 27,5 | 27,7 |
| — | altezza cassa | — | 22,55 | 22,8 |

Conseguenze per il CAD:

- Le sedi dei servo si disegnano sulle quote **ufficiali** (le più grandi) più il gioco di stampa, non su quelle dello STEP: lo STEP è più piccolo di 0,2–0,35 mm in lunghezza, larghezza e altezza.
- Sopra l'albero e sopra il coperchio riduttore servono almeno 0,5 mm di gioco.
- I fori delle alette vanno fatti ad asola o maggiorati: l'interasse varia tra 27,5 e 27,7 mm secondo la fonte.
- Restano **da misurare sul pezzo reale** (nessuna fonte primaria li dà): numero di denti del millerighe (20 o 21) e diametro esterno, filetto della vite centrale (M2 o M2,5), diametro dei fori delle alette, quote delle squadrette di serie.

Dati non meccanici (fonte primaria Tower Pro, verificati): peso 13,4 g; tensione operativa dichiarata 4,8 V; coppia 1,8 kgf·cm a 4,8 V e 2,2 kgf·cm a **6,6 V**; velocità 0,10 s/60° a 4,8 V; cavo 25 cm con connettore JR; dead band 1 µs; 0–55 °C. Corrente di stallo: Tower Pro non la pubblica; clone Sky Star 750 mA ±10 % a 4,8 V e 860 mA ±10 % a 6,0 V.

## Scheda UICPAL ESP32-S3-CAM N16R8 RE1.3

Fonte: immagini dell'inserzione AliExpress 1005008519401021 (venditore "Uncle Electronic Tech Store"), lette il 2026-10-08. Fonte primaria del venditore, ma le quote di un'inserzione vanno confermate con il calibro sulla scheda reale.

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

Aggiunte dalla verifica (`verifica_esp32cam_camera.md`): l'antenna del modulo sporge dal PCB di 4,7–4,9 mm (ingombro totale circa 67,5 mm); nessun foro di fissaggio; le due USB-C stanno affiancate sul lato corto opposto all'antenna; il connettore FPC della camera è al centro e il flat esce verso il lato dell'antenna. Spessore del PCB, altezza dei componenti e posizione quotata delle USB-C non sono pubblicati: **da misurare** (nel modello sono parametri con valori tipici: PCB 1,6 mm, USB-C 9 × 7,4 × 3,3 mm).
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

## Batteria OVONIC 2S 2200 mAh 50C

Fonte: pagina del produttore us.ovonicshop.com (confezione da 2), letta l'8 ottobre 2026.

| Quota / dato | Valore | Stato |
|---|---|---|
| Ingombro nominale | 105 × 33 × 14 mm | V |
| Tolleranza dichiarata | ±5 / ±2 / ±2 mm → massimo 110 × 35 × 16 mm | V |
| Massa | 120 g ± 20 | V |
| Connettori | T-plug (Deans), bilanciamento JST-XH 3 poli | V |
| Uscita e lunghezza dei cavi | non dichiarate; nei pacchi di questo tipo escono da un lato corto | C |
| Vano nel corpo | 112 × 37 × 18 mm con schiuma da 3–5 mm e battuta fissa | scelta di progetto |

## Schede di alimentazione Pololu

| Scheda | Ingombro (mm) | Fissaggio | Modello STEP | Stato |
|---|---|---|---|---|
| D42V110F6 (#5673), regolatore servo | 31,8 × 43,2 × 9; 15 g | 4 fori Ø2,18 (vite M2) a 38,86 × 25,40 mm | [pololu.com/file/0J2219](https://www.pololu.com/file/0J2219/d42v110fx-step-down-voltage-regulator.step) (9 MB); disegno [0J2217](https://www.pololu.com/file/0J2217/d42v110fx-step-down-voltage-regulator-dimensions.pdf) | V |
| D24V22F5 (#2858), regolatore 5 V | 17,8 × 17,8 × 8 | 2 fori Ø2,18 (vite M2) in diagonale, a 2,29 mm dai bordi (misurato sullo STEP) | [pololu.com/file/0J1413](https://www.pololu.com/file/0J1413/d24v22fx-step-down-voltage-regulator.step) (4 MB); disegno [0J1031](https://www.pololu.com/file/0J1031/d24v22fx-step-down-voltage-regulator-dimension-diagram.pdf) | V |
| Big Pushbutton Power Switch HP (#2813) | 20,3 × 25,4 × 4,1; 2,7 g | nessun foro dichiarato: sede a guide | da cercare nelle risorse del prodotto | V (ingombro) |

I modelli STEP Pololu si scaricano senza login. Sono in `cad/modelli/` e sono stati importati nel design Fusion; sullo STEP del D42V110F6 i quattro fori di fissaggio risultano a 38,86 × 25,40 mm (come da datasheet) e i quattro fori di potenza a passo 5 mm lungo un lato lungo.

## Giunti, viteria, connettori

| Componente | Quote (mm) | Fonte | Stato |
|---|---|---|---|
| Cuscinetto F683ZZ | foro 3, esterno 7, larghezza 3; flangia Ø8,1 × 0,8; raccordo minimo 0,1 | scheda NMB LF-730ZZ | V |
| Tolleranze del cuscinetto (classe P0) | foro +0/−0,008; esterno +0/−0,008; larghezza +0/−0,12 | tabelle Enduro (ISO 492) | V |
| Perno | Ø3 × 10, h8: 2,986–3,000 | ISO 286 (fascia fino a 3 mm non vista su fonte primaria) | S |
| Inserto a caldo M2 (CNC Kitchen) | Ø3,6 × 3,0; foro 3,2; parete minima 1,3 | negozio del produttore (lunghezza), rivenditore (diametri) | V / S |
| Inserto a caldo M3 (CNC Kitchen) | Ø4,6 × 5,7; foro 4,0; parete minima 1,6 | idem | V / S |
| Spina servo JR femmina | 7,90 × 2,75 × 14,0 (±0,25); passo 2,54 | disegno Pololu 0J9699 | V |
| Collare maschio della prolunga | 10,30 × 4,00 × 18,0 (±0,25) | disegno Pololu 0J9700 | V |
| Asola passacavo | 9 × 4 per una spina; 12 × 7 per tre cavi con un collare | calcolato | S |
| Condensatore 2200 µF 16 V | Ø12,5 × 20, passo 5 | scheda distributore | S |
| Cicalino BX100 | 40 × 25 × 11 | negozio | S |
| Fusibile MINI | 10,9 × 3,6 × 16,3 | standard ATM | S |
| Portafusibile Littelfuse FHM | ingombro non raccolto: da misurare o dal datasheet | — | C |
| Derivazione Wago 221-415 | circa 30 × 19 × 8 | da controllare sulla scheda Wago | C |
| Basetta millefori | 50 × 70, 4 fori agli angoli | generica | C |
| Traslatore di livello (tipo Adafruit 757) | circa 15 × 13 | da misurare | C |

Regole per il CAD che discendono da queste quote:

- foro per inserto: diametro di datasheet più 0,2 mm, profondità pari all'inserto più 1 mm;
- gioco di stampa di partenza 0,15 mm per lato sulle sedi dei servo, da tarare con un provino;
- sede del cuscinetto: Ø7,0 con interferenza leggera da provino, profonda 3 mm più 1 mm di battuta; sull'anello interno appoggia solo un rialzo di Ø ≤ 4,3 mm;
- tutte le quote marcate C sono parametri utente del modello, così la misura sul pezzo reale si inserisce senza ridisegnare.

## Stato dei modelli nel design Fusion "Hexapod v2 - Assieme"

Creati l'8 ottobre 2026 (fase 3). Tutti stanno in una "zona libreria" a y ≥ 200 mm, lontano dall'origine dove verrà costruito il robot.

| Componente nel design | Origine | Contenuto |
|---|---|---|
| `Tower Pro MG90S Micro servo v1` | riferimento esterno al file dell'utente (non modificato) | STEP completo |
| `Rif_Reg_Servo_D42V110F6` | STEP Pololu | modello completo |
| `Rif_Reg_5V_D24V22F5` | STEP Pololu | modello completo |
| `Rif_SSC32_V25` | script `cad/script/rif_componenti.py` | PCB con 4 fori, header servo, morsettiera, header seriale, micro-USB, zoccolo XBee, condensatori, zona libera per le spine dei servo |
| `Rif_ESP32_S3_CAM` | script | PCB, modulo con antenna sporgente, 2 USB-C, connettore FPC, pin header, slot TF |
| `Rif_Camera_OV3660_75` | script | testa, flat disteso, linguetta |
| `Rif_Batteria_2S2200` | script | pacco nominale e uscita dei cavi |
| `Rif_Cuscinetto_F683ZZ`, `Rif_Perno_3x10` | script | geometria esatta |
| `Rif_Interruttore_2813`, `Rif_Condensatore_2200uF`, `Rif_Cicalino_BX100`, `Rif_Basetta_50x70` | script | ingombri |

Gli ingombri generati dallo script leggono le quote dai parametri utente: per aggiornarli si cambia il parametro e si rilancia lo script con `rigenera=True`.
Non modellati (quote non ancora raccolte, poco influenti): portafusibili, derivazioni a leva, traslatore di livello, T-plug.
