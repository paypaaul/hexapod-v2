# Scheda UICPAL ESP32-S3-CAM N16R8 RE1.3 e moduli camera OV3660: GPIO liberi, alimentazione, meccanica, flat e prolunghe

> Note di ricerca, versione finale dell'8 ottobre 2026 (ripresa di un tentativo interrotto).
>
> Da dove vengono i dati: (1) PDF letti per intero in locale: datasheet ESP32-S3 v2.2, datasheet ESP32-S3-WROOM-1 v1.8, datasheet OmniVision OV3660 v1.3, pinout Freenove, disegno quotato del modulo OV3660 distribuito da Freenove; (2) immagini dell'inserzione AliExpress del venditore UICPAL (pin, hardware, schema elettrico, dimensioni) guardate direttamente; (3) documentazione online Freenove FNK0085; (4) ricerche web e inserzioni viste l'8/10/2026.
>
> Etichette delle fonti: **primary** (datasheet, manuale o pagina del produttore), **secondary** (inserzione, blog, wiki), **third_party_measurement**, **community** (forum), **computed** (calcolo mio, con formula).
>
> Due avvertenze sulla qualita delle evidenze:
> - Lo schema elettrico del venditore e un'immagine da 1000 x 1000 px: le letture fatte li sopra sono marcate "(immagine a bassa risoluzione)" e vanno confermate sulla scheda reale prima di usarle in un progetto.
> - Il forum esp32.com blocca la lettura automatica con un controllo anti-bot che non ho aggirato: delle due discussioni citate ho solo gli estratti del motore di ricerca.

## 1. Identita della scheda, equivalenti e mappa pin completa

### Takeaway
La UICPAL "ESP32-S3-CAM N16R8 RE1.3" ha la stessa disposizione di pin della Freenove ESP32-S3-WROOM CAM (FNK0085): il venditore riusa il disegno di pinout Freenove e il suo schema conferma camera, TF, USB e WS2812 sugli stessi GPIO. Non e una copia identica: monta un CH340 (Freenove: CH343), un modulo marchiato UICPAL con antenna su PCB piu connettore IPEX, e lo schema mostra solo i LED "power" e "TX" (la Freenove ha anche un LED su GPIO2).

### Cited Findings
**Identita ed equivalenti**
- Serigrafia sulla scheda in vendita: "ESP32-S3-CAM N16R8 RE1.3"; modulo marchiato "UICPAL WiFi ESP32-S3-N16R8" con loghi CE/FCC; etichette del venditore: "OTG", "TTL", "CH340", "W2812B", "TX Lamp", "Power Lamp", "IPEX Interface", "Reduce" (pulsante di reset), "BOOT", "TF Card Holder" sul retro, "Support OV2640/OV7725/OV3660 Camera Module DVP 24PIN" (secondary, immagini viste l'8/10/2026) — [foto hardware del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S2c384f8e0b554165953e7e000af34dc5M.jpg); [foto principale](https://ae-pic-a1.aliexpress-media.com/kf/S2ac3791edb03436686088fd09a91655cg.png)
- Inserzione: "Scheda di Sviluppo ESP32-S3 con Modulo WiFi 2.4G per Modulo Fotocamera OV2640, 8MB PSRAM, 16MB FLASH, ESP32-S3 N16R8 CAM Type-C", 17,29 EUR (14,59 EUR da 2 pezzi), 26 recensioni, 287 venduti: disponibile l'8/10/2026 (secondary) — [AliExpress 1005008519401021](https://it.aliexpress.com/item/1005008519401021.html)
- L'immagine "PIN DEFINITIONS" del venditore e il disegno di pinout Freenove (stessa legenda, stessi colori, stesse etichette) con la foto della UICPAL al posto della Freenove (secondary) — [pin definitions del venditore](https://ae-pic-a1.aliexpress-media.com/kf/Sf2f69e5578d14d9ba5780c9c26d0186dO.jpg); originale (primary) — [Freenove ESP32-S3 Pinout.pdf](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/ESP32-S3%20Pinout.pdf)
- Il repository Freenove della scheda dichiara "Apply to FNK0085" (primary) — [GitHub Freenove](https://github.com/Freenove/Freenove_ESP32_S3_WROOM_Board)
- Freenove: modulo ESP32-S3-WROOM-1 Espressif con antenna su PCB, varianti N8R8 e N16R8, USB-seriale CH343, due porte USB-C (primary) — [Freenove docs, Preface](https://docs.freenove.com/projects/fnk0085/en/latest/fnk0085/codes/C/Preface.html); [foto Freenove Board.jpg](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Board.jpg)
- Cloni della famiglia "ESP32-S3-CAM N16R8 con due Type-C": Keyestudio MB0184 (CH340C su una Type-C, OTG sull'altra, stessa mappa camera e SD, dichiara 67 x 29 mm) (secondary) — [Keyestudio MB0184](https://docs.keyestudio.com/projects/MB0184/en/latest/_sources/docs/MB0184%20ESP32-S3%20CAM%20Development%20Board.md.txt); Aideepen ESP32-S3-CAM N16R8 (circa 67 x 28 mm, circa 12 mm di altezza con i componenti) (secondary, solo estratto di ricerca: la pagina risponde 403) — [manuals.plus](https://manuals.plus/asin/B0GDFCCP2G); stessa descrizione sotto i marchi DIYables e FORIOT (secondary) — [Amazon DIYables](https://www.amazon.com/DIYables-ESP32-S3-Development-Bluetooth-Presoldered/dp/B0GQXW2L9G)

**Ordine dei pin sulle due file da 20 (dal lato antenna verso le USB)**
- Fila P1 (lato porta "OTG"): 3V3, EN/RST, GPIO4, 5, 6, 7, 15, 16, 17, 18, 8, 3, 46, 9, 10, 11, 12, 13, 14, 5V (primary Freenove; confermato dalla serigrafia "3V3 EN G4 G5 G6 G7 G15 G16 G17 G18 G8 G3 G46 G9 G10 G11 G12 G13 G14 5V" nel disegno del venditore e dal connettore P1 del suo schema) — [Freenove Pinout.pdf](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/ESP32-S3%20Pinout.pdf); [disegno dimensioni del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S5368b2d9401947d38b09768366c08657l.jpg); [schema del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S42d6e2d5910d49db98b3d85fca29a4d6b.jpg)
- Fila P2 (lato porta "TTL"): TX (GPIO43), RX (GPIO44), GPIO1, 2, 42, 41, 40, 39, 38, 37, 36, 35, 0, 45, 48, 47, 21, 20, 19, GND (stesse tre fonti)

**GPIO occupati**
- Camera DVP, 14 pin: SIOD=4, SIOC=5, VSYNC=6, HREF=7, XCLK=15, Y9=16, Y8=17, Y7=18, Y6=12, Y5=10, Y4=8, Y3=9, Y2=11, PCLK=13 (primary) — [Freenove docs, Preface](https://docs.freenove.com/projects/fnk0085/en/latest/fnk0085/codes/C/Preface.html); identica al profilo `CAMERA_MODEL_ESP32S3_EYE`, con PWDN=-1 e RESET=-1 (primary) — [arduino-esp32 camera_pins.h](https://raw.githubusercontent.com/espressif/arduino-esp32/master/libraries/ESP32/examples/Camera/CameraWebServer/camera_pins.h)
- Lo schema del venditore riporta la stessa mappa camera; il RESET della camera (pin 6 del connettore) e sulla rete EN della scheda; i pin 1, 23 e 24 del connettore non sono collegati (secondary, immagine a bassa risoluzione) — [schema del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S42d6e2d5910d49db98b3d85fca29a4d6b.jpg)
- TF card: CMD=38, CLK=39, D0=40, SDMMC a 1 bit (primary) — [Freenove docs, SD card](https://docs.freenove.com/projects/fnk0085/en/latest/fnk0085/codes/C/28_Read_and_Write_the_SDcard.html); lo schema del venditore mostra tre pull-up da 10 kOhm verso 3.3 V su SD_DATA, SD_CMD, SD_CLK (secondary, immagine a bassa risoluzione) — [schema del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S42d6e2d5910d49db98b3d85fca29a4d6b.jpg)
- PSRAM octal: "pins IO35, IO36, and IO37 are connected to the Octal SPI PSRAM and are not available for other uses" (primary, letto dal PDF) — [ESP32-S3-WROOM-1 datasheet v1.8, nota b della tabella pin](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
- USB nativa: GPIO19 = USB_D-, GPIO20 = USB_D+ (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, Table 2-1](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf); nello schema del venditore vanno al connettore "ESP32S3-OTG" (secondary)
- UART0: GPIO43 = U0TXD, GPIO44 = U0RXD (primary) — [Freenove Pinout.pdf](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/ESP32-S3%20Pinout.pdf); nello schema del venditore vanno al CH340 attraverso resistenze in serie da 470 Ohm, con LED "TX" tra TXD0 e 3.3 V (secondary, immagine a bassa risoluzione) — [schema del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S42d6e2d5910d49db98b3d85fca29a4d6b.jpg)
- All'accensione la ROM stampa i suoi messaggi su UART0 e sul controller USB Serial/JTAG ("(Default) UART0 and USB Serial/JTAG controller") (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, par. 3.3](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- WS2812: GPIO48 (primary) — [Freenove Pinout.pdf](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/ESP32-S3%20Pinout.pdf); nello schema del venditore "W2812B" con DI=GPIO48 e VDD=USB_5V (secondary, immagine a bassa risoluzione)
- LED on-board Freenove: quattro LED "ON, RX, TX, IO2" (TX su GPIO43, RX su GPIO44, LED utente su GPIO2) (primary) — [Freenove Pinout.pdf](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/ESP32-S3%20Pinout.pdf); lo schema UICPAL mostra solo D1 (TX) e D2 (alimentazione, sempre acceso) (secondary, immagine a bassa risoluzione) — [schema del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S42d6e2d5910d49db98b3d85fca29a4d6b.jpg)
- Strapping: GPIO0 (pull-up debole, default 1), GPIO3 (flottante), GPIO45 (pull-down debole, 0), GPIO46 (pull-down debole, 0); sono campionati al reset e poi "freed up to be used as regular IO pins" (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, Table 3-1](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- GPIO0 e anche collegato al pulsante BOOT e al circuito di auto-programmazione DTR/RTS del CH340 (due NPN con 12 kOhm) (secondary, immagine a bassa risoluzione) — [schema del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S42d6e2d5910d49db98b3d85fca29a4d6b.jpg)

### Inferences
- Il modulo radio non e un ESP32-S3-WROOM-1 Espressif: il WROOM-1 ha solo l'antenna su PCB e il WROOM-1U solo il connettore, mentre il modulo UICPAL nelle foto ha entrambi. Quale antenna sia attiva di fabbrica non e documentato.
- La mappa pin dichiarata dall'utente e confermata da tre fonti indipendenti (Freenove, arduino-esp32, schema del venditore): rischio basso.
- La SSC-32 non va collegata a UART0 (GPIO43/44): al reset riceverebbe i messaggi della ROM e i log, e le linee sono condivise con il CH340.

### Gaps
- LED su GPIO2 sulla UICPAL: lo schema dice di no, il disegno "pin definitions" (copiato da Freenove) dice "LED ON". Da guardare sulla scheda.
- Valore di DOVDD e collegamento del pin PWDN della camera: non leggibili nello schema.
- Antenna attiva di default (PCB o IPEX): NON TROVATO.

## 2. GPIO davvero liberi con camera in uso: UART per SSC-32, ADC1 per la batteria, I/O di scorta

### Takeaway
Con camera, PSRAM, USB e UART0 occupati restano liberi senza riserve GPIO1, GPIO2, GPIO14, GPIO21, GPIO41, GPIO42, GPIO47 (piu 38/39/40 se non si usa la TF). Raccomandazione: UART1 con TX su GPIO21 e RX su GPIO47, batteria su GPIO1 (ADC1_CH0), scorta su GPIO41 e GPIO42.

### Cited Findings
- ADC1_CH0..CH9 = GPIO1..GPIO10; ADC2_CH0..CH9 = GPIO11..GPIO20 (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, Table 2-1](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- "the ADC2_CH... analog functions cannot be used with Wi-Fi simultaneously" (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, par. 4.2.2](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- ADC con attenuazione massima (ATTEN3): campo utile 0-2900 mV, errore totale dopo calibrazione +/-50 mV; le misure di datasheet sono fatte con un condensatore esterno da 100 nF sul pin (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, Table 5-5 e 5-6](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- Glitch all'accensione: livello basso per circa 60 us su GPIO1-GPIO14, XTAL_32K_P/N (GPIO15/16) e GPIO17; GPIO18 glitch basso e alto; GPIO19/20 glitch alti. GPIO21, 41, 42 e 47 non sono in tabella (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, Table 2-2](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- "Signals of UART0, UART1, SPI0/1, and SPI2 interfaces can be mapped to any GPIO pins through the GPIO Matrix"; UART2 "can be assigned to any GPIO pins" (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, nota 2 Table 2-4 e par. 2.3.5](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- GPIO47 e GPIO48 lavorano a 1.8 V solo sui chip ESP32-S3R8V e ESP32-S3R16V; sugli altri sono a 3.3 V (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, note Table 2-1](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- GPIO39, 40, 41, 42 sono i pin JTAG MTCK, MTDO, MTDI, MTMS (primary) — [Freenove Pinout.pdf](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/ESP32-S3%20Pinout.pdf)

### Inferences (raccomandazioni)
- Dei dieci pin ADC1, GPIO4-GPIO10 sono della camera e GPIO3 e uno strapping pin: per la batteria restano GPIO1 e GPIO2 (computed, incrocio tra mappa camera e tabella ADC).

| GPIO | Posizione (dall'antenna) | Stato | Note |
|---|---|---|---|
| 1 | fila P2, 3a | LIBERO | ADC1_CH0: scelta per la batteria |
| 2 | fila P2, 4a | LIBERO, da verificare | ADC1_CH1; sulla Freenove pilota un LED |
| 14 | fila P1, 19a | LIBERO | ADC2_CH3: solo uso digitale con Wi-Fi acceso |
| 21 | fila P2, 17a | LIBERO | nessun glitch all'accensione: scelta per UART TX |
| 47 | fila P2, 16a | LIBERO | 3.3 V su chip R8: scelta per UART RX |
| 41 | fila P2, 6a | LIBERO | JTAG MTDI, usabile come GPIO |
| 42 | fila P2, 5a | LIBERO | JTAG MTMS, usabile come GPIO |
| 38, 39, 40 | fila P2, 9a, 8a, 7a | liberi solo senza TF card | pull-up 10 kOhm sulla scheda |
| 0, 3, 45, 46 | varie | strapping: evitare | GPIO0 = pulsante BOOT |
| 43, 44 | fila P2, 1a e 2a | UART0 e CH340 | tenerli per log e programmazione |
| 48 | fila P2, 15a | WS2812 on-board | LED di stato senza hardware in piu |
| 19, 20 | fila P2, 19a e 18a | USB nativa | liberi solo rinunciando alla porta OTG |
| 35, 36, 37 | fila P2, 12a, 11a, 10a | PSRAM | NON usare |

- **(a) UART verso SSC-32**: UART1 con TX = GPIO21 e RX = GPIO47, pin adiacenti in 17a e 16a posizione della fila P2, con GND in 20a. Motivi: sono liberi, non hanno funzioni di boot e non compaiono nella tabella dei glitch. Un glitch basso di 60 us sulla linea TX dura circa 7 bit a 115200 baud (computed: 60e-6 s x 115200 = 6.9) e la SSC-32 lo leggerebbe come un carattere spurio. Alternativa equivalente: TX = GPIO42, RX = GPIO41.
- **(b) Tensione batteria**: GPIO1 (ADC1_CH0) con partitore 100 kOhm (verso batteria) + 47 kOhm (verso massa) e 100 nF tra GPIO1 e GND. Rapporto 47/147 = 0.3197: 8.4 V danno 2.69 V e 6.4 V danno 2.05 V, entro il campo 0-2900 mV (computed: Vadc = Vbat x 47/(100+47)). I +/-50 mV dell'ADC equivalgono a circa +/-0.16 V sulla batteria (computed: 0.050/0.3197): conviene tarare con un multimetro.
- **(c) Scorta**: GPIO41 e GPIO42 (adiacenti), poi GPIO2 e GPIO14; GPIO48 pilota gia il WS2812.

### Gaps
- Se sul modulo UICPAL (non Espressif) ci sia davvero un chip ESP32-S3R8 a 3.3 V: non verificabile da remoto. Indizio a favore: il WS2812 su GPIO48 funziona a 3.3 V sulla stessa scheda.

## 3. Dati meccanici

### Takeaway
Il disegno del venditore da PCB 62.6 x 28.3 mm, passo 2.54 mm, nessun foro di fissaggio e le due USB-C affiancate sul lato corto opposto all'antenna. L'antenna del modulo sporge dal PCB di circa 5 mm, quindi l'ingombro reale in lunghezza e circa 67-68 mm (i cloni dichiarano infatti 67 mm). Il flat della camera esce dal connettore verso il lato antenna e, con il modulo standard da 21 mm, la testa della camera si appoggia sullo schermo metallico del modulo radio. Spessore del PCB, altezze dei componenti e modello STEP: NON TROVATI.

### Cited Findings
- PCB 62.6 mm x 28.3 mm, passo header 2.54 mm, quota aggiuntiva 24.7 mm sul lato corto delle USB (secondary, disegno quotato del venditore) — [disegno dimensioni del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S5368b2d9401947d38b09768366c08657l.jpg)
- Nello stesso disegno il contorno del modulo radio esce dal bordo superiore del PCB e la quota 62.6 parte dal bordo del PCB, non dalla punta dell'antenna; la sporgenza si vede anche nella foto (secondary) — stessa fonte e [foto principale](https://ae-pic-a1.aliexpress-media.com/kf/S2ac3791edb03436686088fd09a91655cg.png)
- Nessun foro di fissaggio ne nel disegno ne nelle foto (secondary) — stesse fonti
- Le due USB-C sono sul lato corto opposto all'antenna, affiancate: "OTG" dal lato della fila che finisce con il pin 5V, "TTL" dal lato della fila che finisce con GND (secondary) — [disegno dimensioni del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S5368b2d9401947d38b09768366c08657l.jpg)
- Slot TF sul lato inferiore del PCB (secondary) — [foto hardware del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S2c384f8e0b554165953e7e000af34dc5M.jpg)
- Connettore FPC camera al centro della scheda, tra modulo radio e pulsanti, con l'asse lungo parallelo al lato corto del PCB (secondary) — stesse immagini
- Sulla Freenove (stesso layout) il flat entra nel connettore dal lato del modulo radio e la testa della camera sta sopra lo schermo metallico del modulo, lente verso l'alto (primary, illustrazione del manuale) — [Freenove docs, figura Chapter32_00](https://docs.freenove.com/projects/fnk0085/en/latest/_images/Chapter32_00.png); pagina [Camera Web Server](https://docs.freenove.com/projects/fnk0085/en/latest/fnk0085/codes/C/32_Camera_Web_Server.html)
- Cloni: Keyestudio MB0184 "67mm x 29mm" e "The two rows of pin headers have a spacing of 25.4mm" (secondary) — [Keyestudio MB0184](https://docs.keyestudio.com/projects/MB0184/en/latest/_sources/docs/MB0184%20ESP32-S3%20CAM%20Development%20Board.md.txt); Aideepen circa 67 x 28 mm e circa 12 mm di altezza con componenti (secondary, estratto) — [manuals.plus](https://manuals.plus/asin/B0GDFCCP2G)
- Modulo Espressif di riferimento ESP32-S3-WROOM-1: 18.0 x 25.5 x 3.1 mm (primary, letto dal PDF) — [WROOM-1 datasheet v1.8, Table 1-1](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
- Il repository Freenove contiene pinout, datasheet e tutorial ma nessun modello STEP e nessun disegno quotato (primary, elenco dei file) — [GitHub Freenove](https://github.com/Freenove/Freenove_ESP32_S3_WROOM_Board)
- Esiste un modello stampabile di custodia per la Freenove ESP32-S3 WROOM con camera; la pagina risponde 403 e non l'ho potuta leggere (secondary, solo titolo da ricerca) — [Printables 1201384](https://printables.com/model/1201384-freemove-esp32-s3-wroom-camera-case-and-prusa-moun)

### Inferences (ricavate dal disegno del venditore: da verificare col calibro)
- Sporgenza dell'antenna oltre il PCB: circa 5 mm (computed: 28 px di sporgenza con scala 5.86 px/mm, ottenuta da 62.6 mm = 367 px). Ingombro in lunghezza circa 62.6 + 5 = 67.6 mm, coerente con i 67 mm dei cloni.
- Interasse tra le due file di header: circa 25.4 mm (computed: 417 px / 16.43 px/mm, scala da 28.3 mm = 465 px; e lo stesso valore dichiarato da Keyestudio). Distanza tra primo e ultimo pin di una fila: 19 x 2.54 = 48.26 mm (computed).
- Interasse tra le due USB-C: circa 11 mm, cioe circa 5.5 mm per parte rispetto alla mezzeria (computed: 181 px / 16.43 px/mm; incertezza +/-0.5 mm).
- La quota 24.7 mm e probabilmente il tratto rettilineo del lato corto tra i due angoli raccordati; in quel caso il raggio degli angoli e circa 1.8 mm (computed: (28.3 - 24.7)/2). E una mia interpretazione.
- Con la camera standard appoggiata sul modulo radio la sommita della lente arriva a circa 3.1 + 5.35 = 8.5 mm sopra il PCB (computed, con modulo alto 3.1 mm come l'Espressif e testa camera da 5.35 mm).
- Senza fori, il fissaggio va fatto con una culla stampata che trattiene i bordi del PCB oppure con uno zoccolo femmina a due file distanti 25.4 mm.
- Orientamento utile per l'esapode: lato USB contro la parete esterna (porte raggiungibili), lato antenna verso l'interno, da cui esce anche il flat della camera. Attorno ai 5 mm di antenna sporgente evitare metallo; l'effetto dei filamenti caricati carbonio sull'antenna non e stato verificato in questa ricerca.

### Gaps
- Spessore del PCB: NON TROVATO.
- Altezze dei componenti (USB-C, connettore FPC, slot TF, modulo UICPAL): NON TROVATO per questa scheda.
- Posizione quotata delle USB-C e loro sporgenza dal bordo: NON TROVATO (solo stima dal disegno).
- Modello STEP della scheda: NON TROVATO (Freenove non lo pubblica; GrabCAD e Printables rispondono 403).
- Tipo esatto del connettore FPC (contatti superiori o inferiori, verso della levetta): non dichiarato.

## 4. Alimentazione

### Takeaway
Secondo lo schema del venditore il regolatore AMS1117-3.3 e alimentato dalla rete USB_5V, e il pin "5V" dell'header sta a valle di un diodo (anodo su USB_5V): il pin 5V sarebbe quindi una USCITA, e alimentare la scheda da li non funzionerebbe. Un caso identico e riportato sul forum Espressif per una ESP32-S3 CAM a due USB. E il punto piu critico di tutta la ricerca e va verificato sulla scheda prima di disegnare il cablaggio. Budget di corrente sul 5 V: almeno 0.5 A continui, meglio 1 A.

### Cited Findings
**Topologia (schema del venditore)** — [schema del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S42d6e2d5910d49db98b3d85fca29a4d6b.jpg) (secondary, immagine a bassa risoluzione)
- Regolatore 3.3 V "AMS1117-3.3": ingresso disegnato sulla rete USB_5V, uscita VCC3.3V; 10 uF + 100 nF in ingresso, 100 uF + 100 nF in uscita
- Diodo D3 (simbolo Schottky) con anodo su USB_5V e catodo su VCC5V; VCC5V e il pin 1 del connettore P1, cioe il pin "5V" dell'header
- I VBUS di entrambe le USB-C sono sulla stessa rete USB_5V, senza diodi tra una porta e l'altra; resistenze da 5.1 kOhm sui CC di entrambe
- CH340 e WS2812 sono alimentati da USB_5V
- Camera: due LDO "XC6206" alimentati dai 3.3 V, uno con uscita VCC1.2V e uno con uscita VCC2.8V

**Conferme e smentite esterne**
- Discussione "ESP32S3 does not work when powered on 5V pin": una ESP32-S3 CAM con due connettori USB e convertitore CH343P (lo stesso chip della Freenove) resta spenta alimentandola a 5 V dal pin 5V con un regolatore su LiPo 2S: LED spento, niente 3.3 V; da USB funziona. La causa non risulta chiarita negli estratti (community, solo estratti di ricerca) — [esp32.com](https://esp32.com/viewtopic.php?p=152000)
- Un rivenditore della Freenove elenca invece tre modi di alimentarla (USB, pin 5V/GND, pin 3V3/GND) indicando USB come preferito (secondary, estratto) — [Bits and Parts](https://www.bitsandparts.nl/en/esp32-s3-wroom-esp32-cam-development-board-wifi-buetooth-p1926701)
- Sulle DevKitC originali Espressif c'e un diodo di protezione dalla corrente inversa e USB piu 5 V esterno insieme "should just work" (community, risposta dello staff Espressif, estratto) — [esp32.com](https://esp32.com/viewtopic.php?p=135762)

**Regolatore**
- AMS1117: fino a 1 A, dropout garantito massimo 1.3 V a pieno carico, minore a correnti piu basse (secondary, scheda del distributore per il componente Advanced Monolithic Systems) — [LCSC C6186](https://www.lcsc.com/product-detail/C6186.html)
- Una copia non verificata del datasheet indica per il contenitore SOT-223 dissipazione massima 600 mW e 150 C/W (secondary, non verificato sull'originale) — [copia su DigiKey](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8122/AMS11173.3SOT223.pdf)

**Correnti**
- Modulo: alimentazione 3.0-3.6 V; "Current delivered by external power supply" minimo 0.5 A (primary, letto dal PDF) — [WROOM-1 datasheet v1.8, Table 6-2](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
- Picchi a 3.3 V e 25 C: TX 802.11b 1 Mbps a 20.5 dBm 355 mA; 802.11g 54 Mbps 297 mA; 802.11n HT20 286 mA; HT40 285 mA; RX 95-97 mA (primary, letto dal PDF) — [WROOM-1 datasheet v1.8, Table 6-4](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
- Solo CPU con radio spenta (modem-sleep), chip senza PSRAM: 27.6-81.1 mA a 160 MHz secondo il carico; con PSRAM "might be higher" (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, Table 5-9](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- Sensore OV3660: 98 mA attivi a piena risoluzione e velocita massima, "about half" a 720p o meno; standby 20 uA (primary, letto dal PDF) — [OV3660 datasheet v1.3, Table 8-3](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/OV3660/OV3660_CSP3_DS_1.3_sida.pdf)
- Clone Keyestudio MB0184: ingresso 3.3-5 V, corrente di lavoro media circa 120 mA (secondary) — [Keyestudio MB0184](https://docs.keyestudio.com/projects/MB0184/en/latest/_sources/docs/MB0184%20ESP32-S3%20CAM%20Development%20Board.md.txt)
- Hardware simile, Seeed XIAO ESP32S3 Sense (ESP32-S3R8 + OV2640), dati del produttore: applicazione webcam 5 V / 138 mA di media, 5 V / 341 mA all'istante dello scatto; Wi-Fi attivo circa 100-110 mA (secondary, estratto di scheda prodotto) — [Elektor](https://elektor.nl/products/seeed-studio-xiao-esp32s3-sense)

**Temperatura**
- Modulo N16R8: temperatura ambiente di funzionamento -40..65 C (primary, letto dal PDF) — [WROOM-1 datasheet v1.8, Table 1-1](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
- OV3660: giunzione -20..+70 C in funzionamento, immagine stabile tra 0 e +50 C (primary, letto dal PDF) — [OV3660 datasheet v1.3, Table 8-2](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/OV3660/OV3660_CSP3_DS_1.3_sida.pdf)

### Inferences
- Stima del picco sul ramo 3.3 V in streaming: 355 mA (TX) + 50-98 mA (camera) = circa 400-450 mA, piu LED ed eventuale TF. Con un regolatore lineare la stessa corrente arriva dal 5 V: prevedere 0.5 A continui e un BEC da almeno 1 A (computed, somma dei massimi di datasheet: non e una misura). La media attesa in streaming e dell'ordine di 150-250 mA, per analogia con i 138 mA dichiarati da Seeed con OV2640.
- Dissipazione sull'AMS1117: (5.0 - 3.3) V x 0.2 A = 0.34 W in media e (5.0 - 3.3) x 0.45 A = 0.77 W nei picchi (computed). Il regolatore scalda: lasciargli aria e non chiuderlo contro la plastica.
- Margine di dropout: entrando direttamente su USB_5V con 5.0 V restano 1.7 V sul regolatore; con un diodo Schottky in serie (circa 0.35 V) ne restano circa 1.35 V, appena sopra il massimo di 1.3 V dichiarato a 1 A (computed). Se si mette un diodo in serie conviene un BEC regolato a 5.2-5.3 V.
- Se lo schema e fedele: (1) il pin 5V da solo i 5 V della USB meno la caduta del diodo e non alimenta la scheda; (2) il BEC deve entrare sulla rete USB_5V, cioe da una delle porte USB-C oppure con un filo saldato sull'ingresso dell'AMS1117; (3) le due porte USB-C hanno i VBUS in comune, quindi BEC su una porta e PC sull'altra mettono in parallelo diretto i due 5 V senza alcuna protezione.
- Regola pratica in ogni caso: prevedere un ponticello o interruttore sul 5 V che va alla scheda, da aprire quando si collega il PC, oppure un diodo Schottky in serie al BEC.
- Se invece lo schema e disegnato male e il regolatore sta a valle del diodo (disposizione delle DevKitC), il pin 5V e un ingresso valido e D3 impedisce il ritorno verso la USB. Le due ipotesi si distinguono con la misura descritta in fondo.

### Gaps
- Conferma della topologia D3 / AMS1117 sulla scheda reale: serve la misura dell'utente.
- Sigla e corrente del diodo D3: non leggibili.
- Consumo misurato in streaming su questa scheda con OV3660: NON TROVATO.
- Soglia di brown-out dell'ESP32-S3 e sensibilita di questa scheda: NON TROVATO in una fonte primaria durante la ricerca.
- Resistenza termica reale dell'AMS1117 su questo PCB: NON TROVATO.

## 5. Tolleranza ai 5 V dei GPIO, rimappatura UART e baud rate

### Takeaway
I GPIO dell'ESP32-S3 non tollerano 5 V: il massimo e VDD + 0.3 V, cioe 3.6 V. Le UART sono rimappabili su qualsiasi GPIO e arrivano a 5 Mbps, quindi qualunque baud rate della SSC-32 va bene.

### Cited Findings
- VIH massimo = VDD + 0.3 V; VIH minimo = 0.75 x VDD; VIL massimo = 0.25 x VDD; VOH minimo = 0.8 x VDD (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, Table 5-4](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- "The voltage tolerance of GPIO is 3.6 V", con il consiglio di un partitore oltre quel valore (primary) — [Espressif ESP-FAQ, hardware design](https://docs.espressif.com/projects/esp-faq/en/latest/hardware-related/hardware-design.html)
- Massimo assoluto sui pin di alimentazione: 3.6 V (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, Table 5-1](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- Tre controller UART (UART0, UART1, UART2) "at a speed of up to 5 Mbps" (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, par. 4.2.1.1](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- Segnali UART instradabili su qualsiasi GPIO tramite GPIO Matrix (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, nota 2 Table 2-4](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)
- Drive di default 20 mA (10 mA per GPIO17/18, 40 mA per GPIO19/20); corrente tipica al massimo drive 40 mA in source e 28 mA in sink (primary, letto dal PDF) — [ESP32-S3 datasheet v2.2, par. 2.2 e Table 5-4](https://documentation.espressif.com/esp32-s3_datasheet_en.pdf)

### Inferences
- SSC-32 TX (5 V) verso ESP32 RX: partitore 10 kOhm in serie + 20 kOhm verso massa, che porta 5 V a 3.33 V (computed: 5 x 20/(10+20)). Con soglia VIH = 0.75 x 3.3 = 2.48 V il margine e 0.85 V (computed).
- ESP32 TX (3.3 V) verso SSC-32 RX: livello alto minimo 0.8 x 3.3 = 2.64 V (computed). Se basti dipende dal microcontrollore della SSC-32: tema del ricercatore SSC-32.

## 6. Moduli OV3660 per ESP32 (DVP 24 pin, passo 0.5 mm)

### Takeaway
Il modulo OV3660 standard e lungo 21 mm in tutto, con testa 8 x 8 x 5.35 mm e soli 8 mm di flat libero: la camera puo stare solo sopra la scheda. Per un alloggiamento camera separato serve la variante a flat lungo: su AliExpress Italia ci sono moduli OV3660 "75MM" con lenti 68, 80, 120 e 160 gradi a 4-8 EUR. Il driver esp32-camera supporta l'OV3660 e la piedinatura coincide con il connettore della scheda.

### Cited Findings
**Disegno quotato del modulo OV3660 68 gradi (distribuito da Freenove; cartiglio del produttore del modulo in cinese)** (primary, letto dal disegno) — [OV3660-Model 68.pdf](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/OV3660/OV3660-Model%2068%C2%B0.pdf)
- Lunghezza totale 21 +/-0.1 mm, dall'estremita della linguetta dei contatti al bordo esterno della testa
- Testa 8 +/-0.2 x 8 +/-0.2 mm in pianta; altezza totale 5.35 +/-0.2 mm; gradini intermedi quotati 2.1 mm e 4 mm
- Linguetta dei contatti: larga 12.5 mm, lunga 5 +/-0.1 mm con rinforzo in poliimmide; zona dei contatti dorati 4.5 +/-0.1 mm
- Tratto flessibile: largo 6 mm
- Spessori: flat 0.15 mm; linguetta con rinforzo 0.3 mm; lamierino d'acciaio sotto il sensore 0.2 mm; biadesivo 0.1 mm sul retro della testa
- 24 contatti, passo 0.5 mm, larghezza del contatto 0.3 mm
- Lato dei contatti: i contatti dorati compaiono nella "BOTTOM VIEW", cioe sulla faccia opposta alla lente; il rinforzo e sul lato della lente
- Flat con film schermante EMI sui due lati
- Ottica: lente formato 1/4", focale 3.4 mm, F/2.4, angolo di campo 68 gradi, distorsione <1%
- Elettrico: sensore OV3660 1/5", 2048 x 1536, AVDD 2.8 V, DOVDD 1.8-2.8 V, DVDD 1.5 V
- Piedinatura dal pin 1 al 24: NC, AGND, SDA, AVDD, SCL, RESET, VS, PWDN, HS, DVDD 1.5V, DOVDD 2.8V, D9, MCLK, D8, DGND, D7, PCLK, D6, D2, D5, D3, D4, D1, D0

**Sensore (datasheet OmniVision OV3660 v1.3, copia nel repository Freenove)** (primary, letto dal PDF) — [OV3660 datasheet](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/OV3660/OV3660_CSP3_DS_1.3_sida.pdf)
- Formato 1/5", 2048 x 1536, pixel 1.4 x 1.4 um, area immagine 2912 x 2167.2 um, package 5010 x 4960 um
- Clock di ingresso 6-27 MHz
- Alimentazioni: core 1.5 V +/-5% (regolatore interno), analogica 2.6-3.0 V, I/O 1.71-3.0 V
- Corrente attiva 98 mA, standby 20 uA; con DVDD interno e DOVDD a 1.8 V: IDD-A 28 mA + IDD-IO 70 mA
- Massimi assoluti: VDD-A 4.5 V, VDD-D 3 V, VDD-IO 4.5 V
- Frame rate massimi: 2048x1536 15 fps, 1080p 20 fps, 720p 45 fps, XGA 45 fps, VGA 60 fps, QVGA 120 fps

**Compatibilita e driver**
- Il driver Espressif esp32-camera elenca l'OV3660 tra i sensori supportati (2048 x 1536, formato 1/5") e l'ESP32-S3 tra i SoC supportati; "Except when using CIF or lower resolution with JPEG, the driver requires PSRAM to be installed and activated"; l'esempio usa `xclk_freq_hz = 20000000` (primary) — [esp32-camera README](https://raw.githubusercontent.com/espressif/esp32-camera/master/README.md)
- L'esempio Freenove per questa scheda gestisce `OV3660_PID` (hmirror=1, vflip=0), usa il profilo `CAMERA_MODEL_ESP32S3_EYE` e `xclk_freq_hz = 10000000` (primary) — [Freenove docs, Camera Web Server](https://docs.freenove.com/projects/fnk0085/en/latest/fnk0085/codes/C/32_Camera_Web_Server.html)
- La piedinatura del modulo coincide con il connettore camera dello schema del venditore: 3 SDA, 5 SCL, 7 VSYNC, 9 HREF, 12 D9=Y9, 13 XCLK, 14 D8=Y8, 16 D7=Y7, 17 PCLK, 18 D6=Y6, 19 D2=Y2, 20 D5=Y5, 21 D3=Y3, 22 D4=Y4; D1 e D0 non collegati (secondary, immagine a bassa risoluzione) — [schema del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S42d6e2d5910d49db98b3d85fca29a4d6b.jpg)
- "OV2640, OV5640, and OV3660 share the same 24-pin ribbon connector"; nessuna variante NoIR per l'OV3660 secondo l'autore (secondary, blog senza riferimenti a datasheet) — [espboards.dev](https://www.espboards.dev/blog/esp32-camera-modules-compared/)

**Varianti acquistabili dall'Italia (AliExpress Italia, viste l'8/10/2026)**
- "Modulo fotocamera OV3660 da 75MM per scheda di sviluppo ESP32 CAM ESP32 S3 68 80 120 160 gradi interfaccia YUV RGB HD 3MP DVP 24pin": 3,92 EUR nella variante 68 gradi, valutazione 4.9, 274 recensioni, oltre 5000 venduti; varianti "68 Degrees", "80 Degrees", "120 Degrees GOOD", "120 Degrees", "160 Degrees" (secondary) — [AliExpress 1005008406404365](https://it.aliexpress.com/item/1005008406404365.html); foto delle quattro teste: [immagine](https://ae-pic-a1.aliexpress-media.com/kf/S4006fe28243b4d18a771a8af8e3902a0s.jpg)
- "Modulo Fotocamera OV3660 3 Milioni di Pixel 68 120 160 Gradi Interfaccia DVP Uscita YUV 21/75mm": 5,21 EUR, 5229 venduti (secondary) — [AliExpress 1005012282236942](https://it.aliexpress.com/item/1005012282236942.html)
- "Modulo Fotocamera OV3660 Aggiornato per Scheda di Sviluppo ESP32-CAM ESP32-S3, 68 120 160 Gradi, Anti-interferenza": 7,55 EUR, 5493 venduti (secondary) — [AliExpress 1005009344582623](https://it.aliexpress.com/item/1005009344582623.html)
- "Modulo telecamera OV3660 da 75 mm per ESP32 CAM ESP32 S3 ... 68 80 120 160 gradi": 4,49 EUR, 540 venduti (secondary) — [AliExpress 1005008694638876](https://it.aliexpress.com/item/1005008694638876.html)
- Recensione di un acquirente della variante 120 gradi: compatibile con il software OV3660 per ESP32, gamma dinamica inferiore all'originale (community) — [AliExpress 1005008406404365](https://it.aliexpress.com/item/1005008406404365.html)
- Taidacent vende OV3660 con flat da 21 mm e da 80 mm (secondary, estratto di ricerca) — [Carrefour UAE / Taidacent](https://www.carrefouruae.com/mafuae/ar/web-cameras/taidacent-esp32-cam-esp32cam-esp32-cam-wifi-ip-timer-webcam-camera-module-3mp-ov3660-160-degree-yuv-rgb-21mm-80mm-fpc-cable-dvp-interface-80mm-fpc-68-degree/p/3233002608237)

### Inferences
- Flat libero sul modulo da 21 mm: 21 - 5 (linguetta) - 8 (testa) = 8 mm (computed). Distanza tra estremita della linguetta e asse ottico: 21 - 4 = 17 mm (computed).
- Flat libero atteso su un modulo "75MM", se 75 mm e la lunghezza totale come nel disegno da 21 mm: 75 - 5 - 8 = 62 mm (computed; la definizione di "75MM" non e verificata).
- Il campo reale e minore dei 68 gradi nominali: la lente e data per il formato 1/4", il sensore e 1/5" con diagonale sqrt(2912^2 + 2167.2^2) = 3630 um. Con focale 3.4 mm: diagonale 2 x atan(1.815/3.4) = 56 gradi, orizzontale 2 x atan(1.456/3.4) = 46 gradi, verticale 2 x atan(1.084/3.4) = 35 gradi (computed, ottica ideale). Per vedere il terreno davanti al robot conviene una lente da 120 o 160 gradi nominali, il cui campo reale sara a sua volta inferiore al nominale.
- Nella foto dell'inserzione la lente da 160 gradi e piu larga della base da 8 x 8 mm: l'alloggiamento va disegnato sul pezzo reale.
- Contatti sul lato opposto alla lente: con la camera appoggiata lente in alto i contatti guardano il PCB, quindi il connettore della scheda prende i contatti dal basso. E una deduzione dal disegno del modulo e dall'illustrazione Freenove.
- La scheda fornisce 1.2 V sul pin 10 (rail pensato per l'OV2640) mentre il disegno del modulo OV3660 indica DVDD 1.5 V. Venditore e Freenove dichiarano comunque il supporto e i moduli OV3660 per ESP32-CAM si vendono a migliaia; non ho trovato una fonte che spieghi il dettaglio elettrico.

### Gaps
- Raggio minimo di piega del flat: NON TROVATO.
- Disegni quotati delle varianti da 75 mm e delle teste da 120 e 160 gradi: NON TROVATI.
- Presenza del filtro IR-cut nelle singole varianti: NON TROVATO.
- Riscaldamento misurato dell'OV3660: NON TROVATO (solo corrente da datasheet: 98 mA massimi).
- Disponibilita su Amazon.it di un OV3660 a flat lungo: non verificata.

## 7. Prolunghe e adattatori FPC DVP 24 pin

### Takeaway
Le prolunghe esistono (Adafruit 4524 piu cavi da 250 mm), ma le poche prove pubbliche dicono che un DVP a 24 pin funziona fino a 75-90 mm e non funziona a 100 mm o piu. Meglio comprare un OV3660 con flat da 75 mm che prolungarne uno corto: la prolunga aggiunge un connettore, inverte l'ordine dei pin se si sbaglia tipo di cavo e porta la lunghezza oltre la soglia.

### Cited Findings
- OV2640 con flat di lunghezze diverse: 10 mm OK, 63 mm OK, 75 mm OK, 100 mm non riconosciuta, 200 mm non riconosciuta; scheda host non indicata, nessuna risposta dello staff (community) — [Arducam forum, dicembre 2023](https://forum.arducam.com/t/omni-vision-camera-extension/6131)
- OV2640 su ESP32-S3 con cavo FFC da 90 mm e scheda di prolunga Adafruit a 24 pin: "didn't work right out of the box", ha funzionato dopo aver sistemato l'impedenza; frequenza XCLK non indicata (community) — [Hackaday.io, Prism laser scanner](https://hackaday.io/project/21933-prism-laser-scanner/log/249686-extending-dvp-running-an-ov2640-on-the-esp32-s3-over-an-ffc-cable)
- Adafruit 4524 "24-pin 0.5mm FFC / FPC Extender": unisce due cavi a 24 pin passo 0.5 mm, per FPC spessi 0.3 mm; "pin 1 of one cable is connected to pin 24 of the other", quindi serve un cavo con i contatti sullo stesso lato (tipo A) (primary) — [Adafruit 4524](https://www.adafruit.com/product/4524); a catalogo DigiKey (secondary) — [DigiKey](https://punchouttest.digikey.es/en/products/detail/adafruit-industries-llc/4524/12323567)
- Cavi: Adafruit 4230 "24-pin eInk / ePaper Extension Cable 0.5mm Pitch - 25cm Long" (250 x 12 x 0.1 mm); Adafruit 6386 "24-pin 0.5mm pitch FPC Flex A-B (D) type Cable - 250mm long" (secondary, rivenditore) — [Core Electronics 4230](https://core-electronics.com.au/24-pin-eink-epaper-extension-cable-0-5mm-pitch-25cm-long.html.plain.md); [Core Electronics 6386](https://core-electronics.com.au/adafruit-24-pin-0-5mm-pitch-fpc-flex-cable-250mm.html)
- Moduli OV2640 con flat da 75 mm sono venduti come ricambio per ESP32-CAM (secondary) — [Kunkune UK](https://kunkune.co.uk/shop/esp32-esp8266/ov2640-camera-upgrade-2mp-length-75mm/)
- Clock: l'OV3660 accetta 6-27 MHz (primary) — [OV3660 datasheet](https://raw.githubusercontent.com/Freenove/Freenove_ESP32_S3_WROOM_Board/main/Datasheet/OV3660/OV3660_CSP3_DS_1.3_sida.pdf); Freenove usa 10 MHz (primary) — [Freenove docs](https://docs.freenove.com/projects/fnk0085/en/latest/fnk0085/codes/C/32_Camera_Web_Server.html); l'esempio Espressif usa 20 MHz (primary) — [esp32-camera README](https://raw.githubusercontent.com/espressif/esp32-camera/master/README.md)

### Inferences
- Lunghezza totale ragionevole: fino a circa 75 mm con il flat originale schermato del modulo. Oltre i 90 mm non c'e nessuna prova positiva tra quelle trovate.
- Con flat lungo partire da XCLK a 10 MHz (valore Freenove), che lascia piu margine dei 20 MHz dell'esempio Espressif.
- Una prolunga con il cavo del tipo sbagliato scambia il pin 1 con il 24 e porta le alimentazioni sui pin dati: rischio concreto di distruggere la camera.
- Il riassunto del log Hackaday indica "prodotto 4523" per la scheda di prolunga Adafruit; sul sito Adafruit la scheda a 24 pin e il 4524. Probabile refuso.

### Gaps
- Nessuna prova specifica con OV3660 e nessuna prova con la frequenza XCLK dichiarata.
- Discussione "Required long cable for ESP32-CAM Module" sul forum Espressif: non letta per il controllo anti-bot — [esp32.com](https://esp32.com/viewtopic.php?p=72377)
- Prolunghe FPC a 24 pin su Amazon.it o AliExpress: non cercate in questa ripresa.

## Solo l'utente puo rispondere (misure e foto sulla scheda reale)

### Takeaway
Otto verifiche sulla scheda fisica chiudono le incertezze rimaste; la prima (pin 5V) condiziona tutto il cablaggio di potenza.

### Cited Findings
- Nessuna fonte nuova: l'elenco deriva dai Gaps delle sezioni precedenti; la topologia da verificare e quella letta sullo [schema del venditore](https://ae-pic-a1.aliexpress-media.com/kf/S42d6e2d5910d49db98b3d85fca29a4d6b.jpg).

### Inferences
1. **Pin 5V, ingresso o uscita?** Scheda scollegata, multimetro in prova diodi: puntale rosso sul pin 3 dell'AMS1117 (ingresso) e nero sul pin 5V dell'header, poi a puntali invertiti. Se si legge 0.2-0.4 V in un solo verso, il regolatore sta a monte del diodo e il pin 5V e solo uscita. Se c'e continuita (circa 0 Ohm) nei due versi, il regolatore e sul pin 5V e il pin e un ingresso valido. Controprova: 5 V da alimentatore sul pin 5V con USB staccata: si accende il LED di alimentazione?
2. **Calibro sul PCB**: lunghezza del solo PCB e lunghezza con l'antenna sporgente, larghezza, spessore del PCB, interasse tra le file di header, distanza del centro di ciascuna USB-C dai bordi lunghi e sporgenza dei connettori dal bordo corto.
3. **Altezze**: modulo radio, USB-C, connettore FPC e pulsanti sopra il PCB; slot TF e plastica degli header sotto il PCB.
4. **Foto ravvicinata del connettore FPC** con levetta aperta, per confermare da che lato entra il flat (atteso: dal lato antenna) e dove sono i contatti.
5. **GPIO2**: caricando un blink su GPIO2 si accende un LED on-board?
6. **Antenna**: foto della zona del connettore IPEX, per vedere la resistenza da 0 Ohm che seleziona antenna su PCB o connettore.
7. **Camera**: quale OV3660 e stato comprato o verra comprato (lunghezza del flat, angolo della lente, link), con misura della testa (lato, altezza, diametro della lente).
8. **TF card**: si usera? Se no, GPIO38, 39 e 40 diventano I/O di scorta.

### Gaps
- La tensione logica reale della SSC-32 in possesso dell'utente dipende dalla variante esatta: tema del ricercatore SSC-32.
