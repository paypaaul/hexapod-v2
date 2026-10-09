# Predisposizioni per sensori, luci ed espansioni (backlog)

9 ottobre 2026. È un backlog: niente è approvato né comprato, e nel CAD non è ancora modellato niente. Ogni voce nuova del BOM va approvata dall'utente.

Nasce da quattro ricerche indipendenti: stato del robot, percezione dell'ambiente, luci e interazione, integrazione elettrica e meccanica. Qui sono unite: doppioni fusi, conflitti risolti (sezione 2.9). Il piano che unisce questo documento e `software.md` è `piano-elettronica-software.md`.

Legenda dati: **V** verificato su fonte primaria; **S** stimato o da fonte secondaria; **C** da confermare sul pezzo reale. Quote in mm, terna del robot (X avanti, Y a sinistra, z 0 sugli assi dei femori) o terna della zampa dove è detto.

Priorità:
- **alta**: si predispone ora nel CAD; prima tranche di acquisti, se approvata;
- **media**: si predispone solo nei pezzi che si stampano una volta (carapace, visiera); si compra dopo;
- **bassa**: idee tenute in lista; nessuna predisposizione, salvo dove è scritto.

## 1. In breve

- Un secondo bus I2C solo per i sensori (GPIO47 SDA, GPIO3 SCL), separato da quello della camera. Una presa Qwiic per i sensori futuri.
- Un solo connettore a 16 poli fra corpo e carapace: luci, audio, bus e pulsante.
- Alta priorità: IMU, sensori di forza nei piedi, correnti dei due rail, ToF multizona nel viso, catena LED con anello del pulsante e luci dei lobi.
- I piedi vanno predisposti subito: punta dello stinco, piedino e gola per i fili. Dopo vorrebbe dire ristampare sei tibie.
- Visiera e carapace sono un pezzo unico a due colori: finestre, fori e sedi vanno disegnati prima della prima stampa, anche per le voci di media priorità.
- Con le voci alte il robot pesa circa 58 g in più (18 sulle zampe): femore dal 51,4 al 52,4 % dello stallo. Con alte e medie, 53,1 %.
- Alcuni posti nel corpo non stanno in piedi: scheda del carapace, amplificatore, microfoni, INA3221, prese dei piedi. Sono segnati "posto da trovare nel CAD" (revisione del 9 ottobre).

## 2. Architettura proposta

### 2.1 Principi

- I sensori nuovi stanno tutti su un bus I2C a 3,3 V. Nessun I2C lungo le zampe: dai piedi arrivano solo segnali analogici su due fili.
- Ogni scheda I2C si alimenta a 3,3 V. I moduli Pololu e Adafruit tirano SDA e SCL alla loro VIN: a 5 V porterebbero 5 V sull'ESP32.
- La seriale verso la SSC-32 resta solo per i servo.
- Si legge tutto a intervalli (polling): nessuna linea d'interrupt, perché non restano GPIO.
- Nessun microcontrollore ausiliario per ora (2.6).

### 2.2 Bus I2C dei sensori

- Controller I2C0 dell'ESP32-S3 su GPIO47 (SDA) e GPIO3 (SCL), 400 kHz. La camera resta sul suo SCCB (GPIO4/5), da sola; esp32-camera lo mette su I2C1 di default (V, `Kconfig`).
- Perché separato e non condiviso con la camera: all'avvio esp32-camera passa la tabella degli indirizzi dei sensori di camera compilati (0x21, 0x30, 0x3C, 0x68 e altri) e, se qualcuno risponde, prova a riconoscerlo leggendo e scrivendo registri (V, `esp_camera.c`). Un sensore a uno di quegli indirizzi verrebbe scritto; un sensore che blocca il bus fermerebbe anche la camera. Il bus condiviso resta la riserva se servono i due pin (`pin_sccb_sda = -1` e `sccb_i2c_port`, V).
- Nella riserva il ToF frontale non va a 0x30: è l'indirizzo dell'OV2640, che esp32-camera prova all'avvio (supporto attivo di default nel `Kconfig`, V), e dopo un riavvio senza togliere corrente il ToF è ancora lì. Si usano indirizzi fuori dalla tabella della camera (per esempio 0x52 e 0x53, liberi in 4.2; da ricontrollare sulla versione del driver), oppure si tolgono dal `Kconfig` i sensori di camera non usati.
- GPIO3 è un pin di strapping solo se è bruciato l'eFuse STRAP_JTAG_SEL; con il pull-up dell'I2C sta alto, che è comunque la scelta predefinita (V Espressif, da provare al banco). GPIO47 sta a 3,3 V sul modulo N16R8 (V). GPIO47 era la riserva della RX verso la SSC-32: la riserva sparisce.
- GPIO2 non va bene per l'I2C: il LED "ON" della scheda carica la linea.
- Pull-up: ogni modulo Adafruit ne ha 10 kΩ e i Pololu ne hanno di propri. Le sei schede Adafruit delle voci alte e medie da sole danno già 1,67 kΩ. Con le voci basse si arriva a 11–12 schede Adafruit, 0,83–0,91 kΩ, sotto il minimo qui sotto: le schede di X27, X29, X32 e X33 si montano con i pull-up staccati (`piano-elettronica-software.md` 2.4).
  - A 400 kHz il tempo di salita deve stare entro 300 ns: Rp(max) = 300 ns / (0,8473 · Cb). Con circa 1,1 m di cavo e una decina di schede la capacità prevista è 150–250 pF (S): serve 1,0–1,4 kΩ. Il minimo è 0,97 kΩ, per stare entro 3 mA a livello basso a 3,3 V (NXP UM10204, tabella 10 e §7.1; S, non riletta qui).
  - All'arrivo si misurano la resistenza equivalente e, con un oscilloscopio, il tempo di salita. Se supera 300 ns: rami più corti, oppure bus a 100 kHz. A 100 kHz lo stesso traffico vale quattro volte tanto (120–200 % con alte e medie): si riducono le letture (ToF in 4 × 4, IMU a 208 Hz, media negli INA260; conto nel piano, 2.5).
- Cavi: in tutto circa 1,1 m (corpo 0,8, carapace 0,3; S). Almeno 10 mm dai cavi da 12–16 AWG, incroci a 90°.
- Carico stimato a 400 kHz con le voci alte e medie: 30–50 % (S).
- Il software chiede i contatti dei piedi a 100 Hz con meno di 10 ms di ritardo (`software.md` 4.3). Una lettura 8 × 8 del VL53L7CX con tutte le uscite del driver tiene il bus per decine di ms (S): si leggono solo le uscite che servono e si misura la durata al banco.
- Con l'ESP32 alimentata solo dalla USB (al banco) il bus dei sensori è spento: il firmware lo deve tollerare, come un sensore mancante.

### 2.3 Connettore del carapace e presa di espansione

Oggi il carapace si toglie staccando lo spinotto di bilanciamento e il Dupont a 2 vie del pulsante. Con luci, microfoni e sensori sul carapace servono più fili. Proposta: un solo connettore.

- **Scheda del carapace**: una striscia di millefori (avanzo della C2) sotto il dorso, con la spina che si sfila dall'ottagono. Porta una testata 2 × 8 a passo 2,54 con chiave, la presa Qwiic di espansione, l'espansore di I/O (X20), il condensatore da 470 µF dei LED e le derivazioni verso luci, microfoni e pulsante.
- **Posto da trovare nel CAD**. Lungo i lati lunghi dell'ottagono non c'è il volume. Fra x −21 e 29 ci sono:
  - la battuta dello sportellino, a \|y\| 14,5–17 e z 32,8–34,4;
  - i canali di X22, a \|y\| 17,2–21 da z 29,4, e più larghi dopo la correzione (X22);
  - le spine dei servo, a \|y\| ≥ 19,5 fino a z 25,2.

  Restano una fessura larga 3,5 mm (\|y\| 16–19,5, sotto z 29,4) e 4,2 mm d'altezza a \|y\| ≥ 19,5. Non ci stanno la testata con la spina IDC (circa 9 + 9 mm, S), il 470 µF (Ø6,3–8, S) e l'adattatore del TCA9534. Lo stesso vale per l'amplificatore (X17) sul lato −Y. Da guardare per primo, non verificato: davanti all'ottagono sopra l'ESP32 (x 29…50, \|y\| ≤ 16), fuori dal flat della camera e dall'antenna (da x 55,6); oppure i canali di X22 interrotti sopra le schede.
- **Cavo**: piatto a 16 vie con spina IDC, saldato sulla basetta, lungo circa 15 cm.
- **Come si toglie il carapace**: si toglie lo sportellino, si sfila la spina dall'ottagono, si svitano le 4 viti, si stacca lo spinotto di bilanciamento, si solleva.
- **Presa di espansione**: la presa Qwiic (JST SH a 4 poli, GND, 3V3, SDA, SCL) sulla scheda del carapace si raggiunge dall'ottagono. Qualunque modulo STEMMA QT o Qwiic si collega lì senza saldare.

| Polo | Segnale | Polo | Segnale |
|---|---|---|---|
| 1 | +5 V (LED e audio) | 2 | +5 V (LED e audio) |
| 3 | GND | 4 | dato LED a 5 V (dopo il buffer) |
| 5 | GND | 6 | SCL |
| 7 | +3,3 V sensori | 8 | SDA |
| 9 | GND | 10 | BCLK I2S |
| 11 | WS I2S | 12 | dati dei microfoni |
| 13 | dati verso l'amplificatore | 14 | riserva (XSHUT del ToF del mento, X25) |
| 15 | pulsante A (2813) | 16 | pulsante B (2813) |

Nel cavo piatto il conduttore n sta accanto a n + 1. Per questo:
- il dato dei LED (5 V, 800 kHz) sta fra due masse;
- SCL e SDA hanno accanto masse o il 3,3 V;
- il gruppo I2S è separato dal bus da una massa;
- i fili del pulsante stanno lontani dai segnali veloci.

Con 0,8 A sui due poli da 5 V la caduta nel cavo piatto è circa 13 mV all'andata e 8 mV al ritorno sui tre poli di massa: circa 21 mV in tutto (S).

### 2.4 Audio e luci

- **Audio**: un solo controller I2S in full-duplex, con BCLK e WS condivisi fra amplificatore e microfoni (V, ESP-IDF). Due microfoni I2S sulla stessa linea dati, uno a sinistra e uno a destra (pin SEL). Quattro GPIO in tutto: 38 BCLK, 39 WS, 40 dati dei microfoni, 2 dati verso l'amplificatore. Campionamento a 48 kHz, ricampionato a 16 kHz per il riconoscimento vocale (S). Sull'S3 la camera usa la periferica LCD_CAM, non l'I2S (S).
- **Luci**: una catena di LED indirizzabili sul GPIO48, in parallelo al WS2812 della scheda (che ripete il primo pixel). Un buffer a 5 V sulla basetta. Ordine della catena: pixel del corpo (fari, se si fanno), poi il connettore, poi anello del pulsante, lobi, occhio, linee della fascia.
- **Tetto di corrente dei LED**: 600 mA, nel driver del firmware e non nelle animazioni. Da solo non basta:
  - durante il reset e l'avvio GPIO48 non è pilotato (S): se l'ingresso del buffer fluttua, alla catena arrivano dati a caso;
  - i pixel tengono l'ultimo colore anche se l'ESP32 si riavvia;
  - con le voci alte e medie i pixel sono fino a 58: tutto bianco chiede circa 2,1 A (36 mA a pixel, S). Con l'ESP32 si superano i 2,5 A del D24V22F5, il 5 V cala, l'ESP32 si riavvia e i LED restano accesi.
- **Protezioni in hardware** (voci nuove del BOM, da approvare): pull-down da 10 kΩ all'ingresso del buffer; sul 5 V dei LED un PTC (tenuta di almeno circa 0,7 A: i 600 mA del tetto più 38–94 mA dei pixel spenti; intervento sotto quanto il D24V22F5 regge insieme all'ESP32; taglia da scegliere) oppure un interruttore di carico spento all'avvio.

### 2.5 Alimentazione

- **3,3 V dei sensori**: un regolatore proprio, Pololu D24V5F3 (3,3 V, 500 mA), alimentato dal ramo logica dopo l'interruttore. Il 3V3 della scheda UICPAL non ha schema pubblicato e regge già ESP32, Wi-Fi e camera; il ToF frontale da solo chiede 150 mA di picco. Alternativa senza componenti: provare al banco il 3V3 della scheda con ToF e Wi-Fi accesi; se non cala sotto 3,0 V e la scheda non si riavvia, il D24V5F3 non serve.
- **5 V**: LED, amplificatore, radar e LIDAR dal D24V22F5 (B2), presi alla sua uscita e non dal pin 5V dell'ESP32.
- **Masse**: tornano alla basetta e da lì alla massa a stella. Ogni sensore dei piedi ha il proprio filo di massa, non il marrone del servo: lungo la zampa passano solo massa e segnale (X5), mai il 3,3 V.
- Bilanci in 4.3.

### 2.6 Microcontrollore ausiliario: no, per ora

L'ESP32-S3 ha due core; l'RMT genera i dati dei LED e l'I2S l'audio in hardware; i canali analogici li dà l'ADS7830. Un microcontrollore ausiliario conviene solo se servono più di 8 ingressi analogici veloci, più uscite di quelle dell'espansore, o se il firmware in tempo reale non regge insieme a camera e Wi-Fi. Candidato in quel caso: X33.

### 2.7 SSC-32: ingressi e uscite da verificare

La SSC-32 originale ha ingressi A–D (digitali, o analogici a 8 bit con i comandi VA…VD) e uscite discrete (`#nH`, `#nL`) (S: forum RobotShop e manuale Lynxmotion). Sul clone "V2.5" non è verificato. Prova al banco a costo zero: un partitore noto su un ingresso e il comando `VA`. Se ci sono, possono leggere i PG dei due regolatori senza GPIO (l'uscita del radar passa comunque dall'espansore X20); li legge `ctrl`, unico proprietario della UART, al ritmo del battito (`software.md` 2.4). Il piano non dipende da questo: a 115200 baud i soli comandi dei 18 servo (circa 148 byte, 12,8 ms) occupano già il 64 % di un ciclo da 20 ms (S).

### 2.8 Zone del robot

| Zona | Volume utile | Cosa ci va |
|---|---|---|
| Vano sotto il vassoio (x 34…71, \|y\| ≤ 16, z −9,4…+1) | 37 × 32 × 10,4 | IMU (X4), ADS7830 con i partitori (X6). Conteso con l'interruttore 2813, che non ha ancora un posto. Si raggiunge solo togliendo il vassoio: ci va solo ciò che si monta una volta |
| Basetta sotto l'ESP32 (x 22…78, 8,5 di luce) | piena per metà | buffer dei LED, 330 Ω, D24V5F3, cavo piatto del carapace |
| Baie anteriori (regolatori, x 14…57,2) | fuori dal camino \|y\| 27…33,4 | INA260 sulle slitte (X7), NTC (X14) |
| Baie posteriori, parete del tunnel sopra i Wago | 28 cm³ per lato, 5 usati dalle anse; sopra gli ingressi dei Wago lo spazio resta libero per i fili | pettini delle anse (già in programma). L'INA3221 (X15) qui non ci sta (5) |
| Testa: mensola della camera e visiera | dentro \|y\| 7,35 per le parti fisse al corpo | ToF frontale (X8) |
| Sotto il dorso del carapace | dorso da z 34,4: 9,2 mm sopra le spine della SSC-32 (z 25,2), circa 13,6 sopra l'ESP32 (modulo fino a z 20,8); ai lati dell'ottagono (x −21…29) solo 3,5 mm di larghezza o 4,2 di altezza (2.3) | luci, tocco. Scheda del carapace, amplificatore e microfoni: posto da trovare nel CAD. Il vano del computer di bordo (`software.md` 8), alto 15, qui non ci sta |
| Coda: guance della porta di servizio | \|y\| 25,4 verso l'interno | ToF posteriore (X19) su una guancia, altoparlante (X17) sull'altra, spie dei rail (X13) sotto il cicalino. Da qui si raggiungono T-plug e spinotto di bilanciamento: si verifica che si afferrino con ToF e altoparlante montati |
| Zampe | | sensori di forza e loro fili (X5) |

### 2.9 Conflitti fra le proposte e scelte

- **Pin del bus I2C** (proposti 39/40, 47/3, oppure bus della camera): scelti **47/3**. Così 38–40 restano all'audio, e la camera ha il suo bus (2.2).
- **Pin dei LED** (GPIO48 condiviso oppure GPIO2): scelto **GPIO48**. Non costa un pin; il LED della scheda ripete il primo pixel ed è nascosto sotto lo sportellino.
- **Microfoni PDM o I2S**: scelti **I2S**, che condividono BCLK e WS con l'amplificatore: 4 pin invece di 5.
- **Mensola della camera** (ToF frontale e altoparlante volevano lo stesso posto sotto l'occhio, sull'asse): il posto va al **ToF**, che deve guardare avanti. L'altoparlante va in coda e il suono esce dalla porta di servizio aperta. Nel viso non ci sta: sotto l'occhio, fra la parete del mento (\|y\| 7,35) e il fianco della testa restano 4–5 mm; ai lati dell'occhio ci sono le fessure di luce (X21).
- **IMU sotto la SSC-32 o sotto il vassoio**: scelto **sotto il vassoio**, perché sotto la SSC-32 passano il 12 AWG e i fili di potenza delle file. A circa 50 mm dal baricentro (+1,6; 0; −13 nel modello, `progetto-meccanico.md`) l'accelerazione centripeta a 1 rad/s è 0,05 m/s², trascurabile. La camera sta sul vassoio: la calibrazione camera–IMU (`software.md` 5.2) si rifà dopo ogni smontaggio del vassoio.
  - Tutti e due i posti si raggiungono solo smontando: la SSC-32, oppure il vassoio con basetta, ESP32, torretta e mensola della camera (`Corpo_Vassoio`).
  - Vanno bene per IMU e ADC, che si montano una volta. Le prese dei piedi no, perché si staccano a ogni smontaggio di una zampa: vanno dove si raggiungono a carapace tolto (posto da trovare nel CAD).
- **IMU fissata rigida o su schiuma**: **rigida**, con due viti M2: serve anche alle vibrazioni (X23). La schiuma resta il rimedio se il rumore dei servo disturba l'assetto.
- **IMU** (LSM6DSO o BNO085): **LSM6DSO**. Adafruit elenca la BNO085 fra i chip che con ESP32 ed ESP32-S3 danno problemi di clock stretching.
- **ADC dei piedi** (ingressi della SSC-32, due ADS1115 nelle baie, un ADS7830): **un ADS7830**. Una scheda per sei piedi e due NTC, nessun carico sulla seriale, nessuna dipendenza dal clone. Per il contatto bastano 8 bit: gli FSR hanno una ripetibilità di ±6 %. Le ADS1115 erano anche in conflitto d'indirizzo (0x48).
  - Gli FSR danno il contatto e un carico relativo, non una misura. Al punto di progetto il piede più carico porta 11,4–12,2 N, da 2945 a 3134 g (`calc/statica_tripode.py`): già il 57–61 % dei 20 N del campo. All'appoggio i picchi lo saturano.
- **Connettore del carapace** (sul tetto fra SSC-32 e F1, oppure sotto il dorso accanto all'ottagono): **sotto il dorso**. Si stacca dall'ottagono prima di sollevare il carapace, e la presa di espansione sta nello stesso posto. Accanto ai lati dell'ottagono però non ci sta: posto da trovare nel CAD (2.3).
- **Buffer dei LED** (sulla basetta o sulla scheda del carapace): **sulla basetta**. Così anche i pixel del corpo ricevono il dato a 5 V.
- **Tetto di corrente dei LED** (600 o 800 mA): **600 mA**. Lascia margine al D24V22F5, chiuso sotto l'ESP32, e a F2. Vale solo insieme alle protezioni in hardware (2.4).
- **Indirizzi**: il CAP1188 nasce a 0x29 come i ToF: va a **0x28**. I ToF ST nascono tutti a 0x29: il frontale va a 0x30, il posteriore a 0x31, quello del mento resta a 0x29 (4.2).
- **OLED nella fascia e sensore dei gesti** (stesso posto, x 30…56): l'OLED è scartato (sezione 6).
- **Fili del piede** (canale dentro lo stinco o gola sulla faccia +X): **gola sotto il guscio**, sullo stinco e sullo zoccolo; sulla culla i fili passano nell'aria sotto il fronte del guscio (5). Il guscio la copre già da Z 94,5 in su e il piedino sotto; un canale dentro lo stinco non serve.

## 3. Voci per priorità

Codici X1…X33 solo per questo documento (le sigle del BOM sono altre). Costi indicativi (S), da ricontrollare all'ordine. Corrente sul 3,3 V dei sensori, salvo dove è scritto.

### 3.1 Alta

| Voce | A cosa serve | Parte candidata | Interfaccia e indirizzo | Dove nel robot | Cosa predisporre nel CAD | Massa | Corrente | Costo | Dati |
|---|---|---|---|---|---|---|---|---|---|
| X1 Bus I2C dei sensori e presa di espansione | dorsale dei sensori nuovi; la presa accoglie quelli futuri senza saldare | nessun modulo: cavi Qwiic (JST SH 4 poli), cavo Adafruit 4209 | I2C0, 400 kHz, 3,3 V; GPIO47 SDA, GPIO3 SCL | dalla basetta: un ramo nel vano sotto il vassoio e nelle baie, uno nel connettore del carapace | asola nel vassoio, passaggio fra SSC-32 e vassoio, clip sul tetto | ~5 g | ~2 mA (pull-up) | ~5 € | V pin e driver della camera; S carico |
| X2 Connettore e scheda del carapace | un solo connettore porta sul carapace LED, audio, bus e pulsante | striscia di millefori (avanzo C2), testata 2 × 8 con chiave, cavo piatto a 16 vie con spina IDC, 470 µF 10 V | 16 poli (2.3) | sotto il dorso, con la spina raggiungibile dall'ottagono: posto da trovare nel CAD (2.3) | sede della scheda, dopo aver trovato il posto | ~8 g sul carapace | — | ~6 € | C posizione |
| X3 Regolatore 3,3 V dei sensori | stacca i sensori dal 3V3 della scheda, non documentato | Pololu D24V5F3 (#2842): 3,3 V, 500 mA, ingresso 3,4–36 V, 13 × 10 × 3 | ramo logica dopo la 2813 | basetta (o vano sotto il vassoio) | nessuna | <1 g (S) | 0,2 mA a vuoto | ~9 € | V (Pololu) |
| X4 IMU a 6 assi | assetto per tenere il corpo orizzontale; caduta o ribaltamento: impulsi tolti e rail spento (GPIO42); imbardata per la rotazione sul posto e la marcia dritta; urti | Pololu #2798 (ST LSM6DSO): 13 × 23 × 3, 0,6 g, 1,8–5,5 V, due fori M2 | I2C 0x6B | tetto del tunnel sotto il vassoio, sull'asse, asse X verso la testa | due bugne con inserti M2 in Corpo_Base | ~2 g | 1 mA | ~20 € | V (Pololu); C interasse dei fori |
| X5 Sensori di forza nei piedi | contatto e carico relativo di ogni piede (non una misura: 2.9): fine del volo al contatto, piede nel vuoto, peso fra i piedi come stima, scivolamenti | 6 (+1) Interlink FSR 400 Short: area attiva Ø5,6, testa Ø7,6, spessore 0,3, 0,2–20 N; doppino 28 AWG siliconico; spine JR dalle prolunghe C5 avanzate (ne restano 16) | analogica: FSR fra l'ingresso e massa, 10 kΩ 1 % verso il 3,3 V e 100 nF a massa sulla striscia dei partitori (lettura invertita); lungo la zampa solo massa e segnale; ADS7830 canali 0–5 | sotto la punta dello stinco, dentro il piedino; fili sotto il guscio, poi con il cavo del servo del ginocchio | punta dello stinco, piedino, gola (sezione 5) | ~3 g a zampa, 18 in tutto | ~2 mA in tutto | ~40 € | V area attiva e ripetibilità (Interlink); S testa e spessore (rivenditore); C presa del cappuccio, piega della coda |
| X6 ADC a 8 canali | sei piedi e due NTC (X14) senza caricare la seriale dei servo | Adafruit ADS7830 (#5836): 8 canali, 8 bit, 2,7–5,25 V, riferimento = alimentazione, 30,5 × 17,7 × 4,7, 2,1 g | I2C 0x48 | sotto il vassoio, accanto all'IMU; partitori su una striscia di millefori | due bugne con inserti M2 | ~3 g | <1 mA | ~6 € | V (Adafruit); C fori |
| X7 Corrente e tensione dei rail servo | giunto bloccato: rail spento (requisito già scritto nello studio e nel BOM, oggi senza sensore); regolatore in limitazione (13 A); stima della carica (6) | 2 × Adafruit INA260 (#4226): shunt 2 mΩ integrato, 15 A continui, 0–36 V, 16 bit; 22,9 × 22,8 × 2,7, 2 g | I2C 0x44 (ponticello A1) e 0x45 (A0 e A1) | in serie al positivo all'uscita di ogni regolatore, baie anteriori | Corpo_Slitta_Regolatore più alta, due inserti M2 | ~8 g con le slitte | 0,3 mA ciascuno | ~25 € | V (TI, Adafruit); C morsettiera per 13 A, fori |
| X8 ToF multizona frontale | mappa 8 × 8 delle distanze, inclinata di 20° in basso: a 100/45 vede il pavimento sull'asse da x ≈ 191, all'altezza dei piedi anteriori (x 197), e la loro fascia da x ≈ 260 (S): bordo del tavolo, gradino, buco; ostacoli fino a 3,5 m, anche al buio | Pololu #3418 (ST VL53L7CX): 60° × 60°, 3,5 m, 13 × 18 × 3, 0,5 g | I2C 0x29 all'accensione, 0x30 dal firmware; alimentato dal pin VDD a 3,3 V con VIN scollegato (Pololu lo ammette fra 2,5 e 3,6 V; il bus allo stesso livello). Con VIN a 3,3 V il regolatore della scheda lavorerebbe in caduta | nel viso sotto l'occhio, sull'asse: sensore a x ≈ 99,4, centro a z ≤ circa 11,5 (finestra sotto l'occhio, 5) | plancia nella mensola, finestra nella visiera | ~3 g | 100 tipici, 150 di picco | ~22 € | V (Pololu, VDD riletto il 9 ottobre); C frequenza in 8 × 8, posizione del sensore sulla scheda, filtro IR della lente |
| X9 Catena LED | base di tutte le luci, con il tetto di corrente | striscia FPC larga 4–5 con WS2812B-2020, 60–100 LED/m; buffer TI SN74AHCT1G125; 330 Ω in serie al dato; pull-down 10 kΩ all'ingresso del buffer; PTC sul 5 V dei LED (da scegliere) | GPIO48, 800 kHz (RMT), dato a 5 V | buffer sulla basetta, striscia sul carapace | ganci passacavo alti 3 ogni 40 mm sotto il dorso | ~1 g ogni 10 cm | 5 V: tetto 600 mA nel firmware, con le protezioni di 2.4; ~1 mA a pixel spento | ~15 € | V (Worldsemi, TI); S striscia; C GPIO48 dell'header = LED della scheda |
| X10 Provino di luce | misura sul filamento vero quanta luce passa nel PLA bianco e come si sparge, prima di disegnare le sedi | piastrina 60 × 40: gradini di bianco da 0,4 a 1,6, intarsio nero 0,6, camere nere da 2, 4, 6, anello e fessura; 3 pixel | al banco | — | nessuna | — | <110 mA al banco | ~0 € | S (nessun dato pubblicato) |
| X11 Anello di stato del pulsante | spia visibile da fuori: avvio, rete, rail acceso, batteria bassa, errore | 2 pixel di X9 | catena LED | attorno al foro del pulsante (x −40): anello bianco Ø18–22 nella fascia, camera nera Ø32 × 4 sotto la pelle | foro anulare, gola, camera nera | <1 g | 5 V: 10–20, max 72 | 0 € | V posizione; C dado del pulsante (non comprato) |
| X12 Luce sotto i lobi | un bagliore per zampa: tripode visibile in marcia, zampa in errore in rosso; illumina coxe e lame | 12 pixel di X9, 2 per lobo | catena LED | faccia interna dello smusso esterno di ogni lobo, rivolti in basso e in fuori | sede piana con due ganci in ogni lobo | ~4 g sul carapace | 5 V: 60–100, max 430 | 0 € | V geometria; C distanza dalle zampe con la striscia |
| X13 Spia dei rail servo | mostra senza firmware che i servo sono sotto tensione, accanto al sezionamento (T-plug) | 2 LED ambra Ø3, 2 resistenze 1 kΩ | su VS1 e VS2, nessun GPIO | in coda sotto il cicalino, rivolti alla porta di servizio | linguetta con due fori Ø3,1 | <1 g | 6 V: 4 mA per rail | <1 € | V rail a 6 V; S tensione del LED |

### 3.2 Media

| Voce | A cosa serve | Parte candidata | Interfaccia e indirizzo | Dove nel robot | Cosa predisporre nel CAD | Massa | Corrente | Costo | Dati |
|---|---|---|---|---|---|---|---|---|---|
| X14 Temperatura dei regolatori | rallentare prima che un regolatore si spenga o che il carapace in PLA (55–60 °C) si deformi; decide se il carapace va in PETG (D-065) | 2 (+1) NTC 10 kΩ 1 % TDK B57861S0103F040 (Ø2,41), ciascuna con 10 kΩ 1 % | ADS7830 canali 6 e 7 | incollate sulla bobina o sul MOSFET di ogni regolatore, nel camino | nessuna: i fili non devono chiudere il camino | ~1 g | 0,17 mA ciascuna | ~3 € | V (TDK); S risoluzione 0,6 °C a 60 °C |
| X15 Corrente del servo di ogni femore | contatto e carico per zampa senza fili oltre i giunti; stallo di un singolo femore, che gli INA260 non distinguono (vedono 9 servo); modello I²t | 2 × Adafruit INA3221 (#6062): 3 canali, shunt 50 mΩ, ±3,2 A, 38,6 × 22,9 × 10,5, 5,8 g | I2C 0x40 e 0x41 (ponticello) | in serie al filo rosso dei femori; posto da trovare nel CAD. Sopra i Wago non ci sta: la scheda finisce 1,35 mm sopra gli ingressi dei fili, sulla stessa pianta (5). Da dimostrare nel CAD prima di tenerla in media priorità | sede dopo aver trovato il posto | ~16 g | 0,35 mA ciascuno (S) | ~24 € | V (Adafruit); S corrente in appoggio (~1,4 A); C fori; da provare il segnale in marcia |
| X16 Udito stereo | comandi a voce offline (ESP-SR: solo inglese o cinese) e direzione dei suoni: il robot si gira verso chi chiama | 2 × Adafruit 3421 (Knowles SPH0645LM4H, I2S, porta sul fondo), 16,7 × 12,7 × 1,8, 0,4 g | I2S: BCLK 38, WS 39, dati 40; SEL a massa e a 3,3 V | sotto il dorso della testa (x ≈ 83–95), ai lati del flat della camera, dentro la fascia: posto da trovare nel CAD. Centrate su \|y\| 11 le schede arrivano a \|y\| 17,35, dentro i canali di X22 (da 17,2) | due fori Ø1 nella fascia con anello e guarnizione, due sedi | ~3 g | ~1 mA (S) | ~14 € | V dimensioni (Adafruit), full-duplex (ESP-IDF); S rumore dei servo; C spazio |
| X17 Voce | conferme e avvisi a voce (batteria, giunto in errore per nome), personalità | Adafruit 3006 (MAX98357A, I2S, classe D, 19,4 × 17,8 × 3, 1,2 g); altoparlante CUI (Same Sky) CMS-15113-078SP, 8 Ω, 0,7 W, 15 × 11 × 3 | I2S, dati sul GPIO2; 5 V | amplificatore sotto il dorso: posto da trovare nel CAD (lungo il lato −Y dell'ottagono non c'è il volume, 2.3); altoparlante su una guancia di coda, il suono esce dalla porta aperta; T-plug e spinotto devono restare a portata di mano | sede dell'amplificatore, sede dell'altoparlante | ~4 g | 5 V: fino a ~200 mA | ~10 € | V (Adafruit); S altoparlante (estratti CUI); C resa dalla porta |
| X18 Tocco sul carapace | carezza sulla testa; tocco lungo sulla coda = si siede (comodità, non arresto di sicurezza); tocco su un lobo = alza quella zampa | Adafruit 1602 (Microchip CAP1188, 8 ingressi), nastro di rame da 0,05 | I2C 0x28 (AD a 3,3 V) | elettrodi sulla faccia interna: smusso del viso, coda (x −91…−83), piani dei lobi; lontano dall'antenna (x 55,6…81,1) | zone piane 15 × 25 senza nervature; sede del modulo (42 × 18 × 3) | ~3,5 g | ~1 mA (S) | ~13 € | V (Adafruit); S tocco attraverso 1,6 di PLA |
| X19 ToF posteriore | in retromarcia e nella rotazione: pavimento dietro la coda (a 100/45 da 11 a 31 cm) e muro vicino | Pololu #3415 (ST VL53L1X): 27°, fino a 4 m, 13 × 18 × 2, 0,5 g | I2C 0x29 all'accensione, 0x31 dal firmware; XSHUT da X20 | guancia di coda lontana dallo spinotto di bilanciamento, inclinato di 35° in basso. Per guardare indietro la scheda sta di traverso e sporge circa 13 mm nella porta (larga 50,8), da cui si raggiunge il T-plug, sezionamento d'emergenza dei servo: si verifica che T-plug e spinotto si afferrino, oppure ToF e altoparlante vanno sopra il piano del T-plug | supporto sulla guancia, due perni o un inserto M2 | ~3,5 g | 20 tipici, 40 di picco | ~22 € | V (Pololu); C lato dello spinotto (cicalino da scegliere) |
| X20 Espansore di I/O | XSHUT dei ToF e uscita del radar senza GPIO | TI TCA9534: 8 I/O, 1,65–5,5 V, I/O tolleranti a 5 V; su adattatore o modulo pronto | I2C 0x20 (0x20–0x27) | sulla scheda del carapace | nessuna | ~2 g | <1 mA | ~3–6 € | V (TI); S modulo |
| X21 Fessure di luce ai lati dell'occhio | espressione del viso senza toccare il campo della camera | 4 pixel di X9 | catena LED | visiera, fuori dalla bugna: da (\|y\| 13; z 16) a (\|y\| 18; z 25), larghe 1,5, a 60°; camere nere da x 96,5 a 100,4 | due tagli riempiti di bianco, camere chiuse verso l'occhio | <1 g | 5 V: 20–30, max 144 | 0 € | V quote dell'occhio; C riflessi nell'immagine |
| X22 Linee di luce lungo la fascia | il segno più riconoscibile dall'alto; verso di marcia e carica | 2 × 10–20 pixel di X9 | catena LED | bordi della fascia (\|y\| 17–18,5), tre tratti per lato: x −91…−61, −51…35, 45…96 | gola che lascia 0,6–0,8 di bianco; canali neri a U alti 5, con l'interno largo almeno la striscia più 0,4 (≥ 5,4) e centrato sulla gola. Il canale disegnato prima (\|y\| 17,2–21, interno 2,2) non conteneva la striscia. Con pareti da 0,8 il canale occupa \|y\| 14,25–21,25, z 29,4…34,4, e urta: la battuta dello sportellino (x −21…29, \|y\| 14,5–17); il collare del cicalino (\|y\| 20,2–21,4) per tutto x −87…−62, e il cicalino se è alto più di 12; la camera nera di X11 fra x ≈ −47 e −33. Tratti da spezzare o ridisegnare nel CAD (5) | 5–8 g | 5 V: 100–200, max 720 | 0 € | V quote; S spazio sopra la SSC-32 |

### 3.3 Bassa

| Voce | A cosa serve | Parte candidata | Interfaccia e indirizzo | Dove nel robot | Cosa predisporre nel CAD | Massa | Corrente | Costo | Dati |
|---|---|---|---|---|---|---|---|---|---|
| X23 Vibrazioni e urti | viti allentate, giochi e ingranaggi consumati dallo spettro; istante del contatto dei piedi; urti contro ostacoli | nessuna: l'IMU di X4 (FIFO da 9 KB) | come X4 | come X4 | fissaggio rigido dell'IMU | 0 | qualche decimo di mA a raffiche (S) | 0 € | V FIFO (ST); S campionamento fino a 6,66 kHz |
| X24 Luce ambiente | accendere i fari, regolare i LED, scegliere l'esposizione | nessuna: esposizione e guadagno della OV3660, luce ambiente per zona del ToF; riserva Vishay VEML7700 | riserva I2C 0x10 | — | nessuna | 0 | 0 | 0 € | V VEML7700 (Vishay); S registri della camera |
| X25 ToF sotto il mento | luce sotto il muso (28,6 mm a 70/70), robot sollevato. Non salva dal bordo del tavolo: i piedi anteriori arrivano 8–10 cm davanti al mento | Pololu #3692 (ST VL53L4CD): 18°, fino a 1,2 m, 13 × 18 × 2 | I2C 0x29 (l'ultimo con l'indirizzo di fabbrica); XSHUT dal polo 14 | sotto la testa, a faccia in giù, a filo del fondo della chiglia | mensolina in Corpo_Chiglia con foro Ø6 | ~2,5 g | 25 tipici, 40 di picco | ~15 € | V (Pololu); C distanza dalle zampe anteriori |
| X26 Radar di presenza | sentinella: robot fermo, rail spento; si sveglia se qualcuno si avvicina, anche al buio | Hi-Link HLK-LD2410C, 16 × 22 | uscita OUT a 3,3 V su X20; 5 V | sotto il dorso, lato sinistro (x −35…−13, y 26…42), antenne in alto: il PLA lascia passare i 24 GHz, il PETG-CF no | tasca o clip, niente viti sopra le antenne | ~2 g (S) | 5 V: 79 mA medi | ~5 € | S (manuale Hi-Link da copie di terzi); C tensione, Bluetooth acceso di fabbrica |
| X27 Gesti e prossimità | comandare il robot passando la mano sopra la schiena; misura anche luce e colore | Adafruit 3595 (Broadcom APDS-9960) | I2C 0x39 | sotto la fascia, x ≈ 40, prima dell'antenna | finestra 5 × 4 svasata nella fascia: da decidere prima della stampa del carapace | ~2 g (S) | 0,8 mA più impulsi del LED IR fino a 100 mA | ~8 € | V (Broadcom, Adafruit); S portata 10–20 cm |
| X28 LIDAR 360° | mappa della stanza; la scansione va via Wi-Fi a un PC con ROS 2 | LDROBOT LD06 o LD19: 38,6 × 38,6 × 33,5 | UART 230400 in sola ricezione: GPIO40 al posto dei microfoni, oppure attraverso l'eventuale computer di bordo; non su GPIO19/20, riservati alla USB OTG (`software.md`); 5 V | sella sul dorso (x 50…90); piano ottico a z ≈ 60. Le viti anteriori del carapace stanno a x 40 (`cor_col_xa`): sella allungata fino a x 40 o altro fissaggio. Sopra x 83–95 coprirebbe i fori dei microfoni (X16), con il motore sopra | nessuna ora | ~50 g con la sella | 5 V: 180, 300 all'avvio | ~70–100 € | V (wiki Waveshare LD19); S massa e spunto; da provare l'effetto sul Wi-Fi |
| X29 Termocamera 32 × 24 | persone e animali al buio, con la posizione; campo simile a quello della camera | Melexis MLX90640 versione 110° × 75° (Adafruit 4469) | I2C 0x33 | accanto all'occhio, con una finestra aperta (il PLA non lascia passare l'infrarosso lontano): probabilmente va allargata la testa | da decidere con X8 prima della stampa del carapace | ~3 g | <23 mA | ~75 € | V (Melexis, Adafruit); C spazio nella testa |
| X30 Fari bassi e bagliore sotto il corpo | illuminare il pavimento davanti nelle stanze buie; alone attorno al robot | 4–6 + 8–12 pixel di X9, in testa alla catena | catena LED | fari sotto il mento (x 81–83), inclinati di 30° in basso; bagliore da studiare (chiglia o ripiani delle baie) | sede nel fronte o pezzo avvitato alle orecchie della chiglia | 2–4 g | 5 V: fari fino a 216, bagliore 100–200 | 0 € | S; C spazio davanti al tunnel |
| X31 Luce nelle tibie | barra luminosa nella finestra del guscio | 3 pixel per tibia; cavo 3 × 30 AWG siliconico | ramo in parallelo dall'uscita del buffer: ripete i primi pixel, nessun GPIO | faccia frontale dello stinco, dietro la finestra 7 × 48 del guscio; cavo con quello del servo del ginocchio | finestra chiusa da 0,6 di bianco, sede sullo stinco: da decidere prima di stampare i gusci. Cambia il guscio approvato in D-061 (finestra lunga aperta): domanda 5 | ~2 g a zampa, 12 in tutto | 5 V: 100–150, max 650 | ~5 € | V quote del guscio; C durata del cavo piegato nei giunti |
| X32 Retroazione di posizione dei servo | angolo vero dei giunti: giunto bloccato, squadretta slittata, calibrazione, pose insegnate a mano | filo da 30 AWG sul cursore del potenziometro; 2–3 ADS7830 in più | I2C 0x49…0x4B | dentro le casse dei servo; il filo segue il cavo del servo | nessuna | ~0,5 g per servo | trascurabile | ~12–18 € | C tensione del potenziometro; prima un servo di scorta al banco |
| X33 Microcontrollore ausiliario | solo se servono più ingressi analogici o più uscite (2.6) | Adafruit 5690 (ATtiny1616 con seesaw: 9 ADC, uscita NeoPixel) o QT Py SAMD21 (4600) | I2C 0x49 (0x4C se c'è X32) | nel vano sotto il vassoio o in una baia posteriore | nessuna | 2–3 g | pochi mA | ~5–7 € | V (Adafruit) |

## 4. Bilanci

### 4.1 GPIO dell'ESP32-S3-CAM

Piano A: senza microSD. Piano B: con la microSD, se l'utente la vuole.

| GPIO | Oggi | Piano A | Piano B | Nota |
|---|---|---|---|---|
| 0, 45, 46 | strapping | non usare | non usare | |
| 1 | ADC della batteria | invariato | invariato | |
| 2 | libero (LED "ON") | dati verso l'amplificatore (X17) | audio a un pin (PDM) con un amplificatore analogico (Adafruit 2130, PAM8302A), oppure libero | il LED "ON" lampeggia con il segnale: innocuo; polarità da provare |
| 3 | strapping JTAG, non usato | SCL dei sensori | SCL dei sensori | conta solo con l'eFuse STRAP_JTAG_SEL bruciato |
| 4, 5 | SCCB della camera | invariato, bus della camera da solo | invariato | |
| 6–13, 15–18 | camera | invariato | invariato | |
| 14 | RX dalla SSC-32 | invariato | invariato | |
| 19, 20 | USB nativa | invariato | invariato | riservati alla USB OTG: flash, debug, HIL, poi l'eventuale computer di bordo (`software.md`) |
| 21 | TX verso la SSC-32 | invariato | invariato | |
| 35–37 | PSRAM | non usabili | non usabili | |
| 38 | libero senza microSD | BCLK I2S | microSD | possibili pull-up della scheda TF: innocui per l'I2S (C). Al banco, prima dell'audio, ingresso RMT per misurare gli impulsi della SSC-32 (`software.md` S1) |
| 39 | libero senza microSD | WS I2S | microSD | |
| 40 | libero senza microSD | dati dei microfoni | microSD | GPIO40 diventa RX del LIDAR se si rinuncia ai microfoni |
| 41 | spegnimento della 2813 | invariato | invariato | |
| 42 | accensione del rail servo | invariato | invariato | |
| 43, 44 | UART0 (CH340) | invariato | invariato | |
| 47 | libero (riserva RX) | SDA dei sensori | SDA dei sensori | |
| 48 | WS2812 della scheda | catena LED, in parallelo | catena LED | |

Con il piano A non resta nessun GPIO libero. Interrupt: nessuno, si legge a intervalli. XSHUT e uscita del radar passano dall'espansore X20. Con il piano B mancano microfoni e altoparlante I2S; resta un audio semplice sul GPIO2.

### 4.2 Indirizzi I2C

Bus dei sensori (I2C0, GPIO47/3). La camera OV3660 (0x3C) sta sull'altro bus.

| Indirizzo | Dispositivo | Voce | Come si ottiene |
|---|---|---|---|
| 0x10 | VEML7700 (riserva) | X24 | fisso |
| 0x20 | TCA9534 | X20 | piedini A0–A2 (campo 0x20–0x27) |
| 0x28 | CAP1188 | X18 | AD a 3,3 V (il predefinito 0x29 è dei ToF) |
| 0x29 | VL53L4CD sotto il mento | X25 | di fabbrica |
| 0x30 | VL53L7CX frontale | X8 | dal firmware a ogni accensione, mentre gli altri ToF sono tenuti spenti; nella riserva (bus della camera) un indirizzo fuori dalla tabella della camera (2.2) |
| 0x31 | VL53L1X posteriore | X19 | dal firmware, poi si accende quello del mento |
| 0x33 | MLX90640 | X29 | di fabbrica |
| 0x39 | APDS-9960 | X27 | fisso |
| 0x40 | INA3221 sinistro | X15 | di fabbrica |
| 0x41 | INA3221 destro | X15 | ponticello |
| 0x44 | INA260 sinistro | X7 | ponticello A1 |
| 0x45 | INA260 destro | X7 | ponticelli A0 e A1 |
| 0x48 | ADS7830 | X6 | di fabbrica |
| 0x49…0x4B | ADS7830 in più | X32 | ponticelli |
| 0x4C | seesaw | X33 | ponticelli (0x49 se X32 non c'è) |
| 0x6B | LSM6DSO | X4 | di fabbrica (V Pololu) |

Nessun conflitto. Gli INA260 e gli INA3221 nascono tutti a 0x40: i ponticelli vanno fatti prima di collegarli. Il VL53L7CX torna a 0x29 a ogni accensione: dopo un riavvio senza togliere corrente il firmware controlla chi risponde prima di riassegnare. Se il ToF del mento non c'è, il posteriore può restare a 0x29.

### 4.3 Corrente

**3,3 V dei sensori** (D24V5F3, 500 mA):

| Voce | Tipica (mA) | Picco (mA) | Dati |
|---|---|---|---|
| IMU (X4) | 1 | 1 | V |
| INA260 × 2 (X7) | 0,6 | 0,6 | V |
| ADS7830 con 6 FSR e 2 NTC (X5, X6, X14) | 1 | 3 | S |
| ToF frontale (X8) | 100 | 150 | V |
| Pull-up del bus | 1 | 2,5 | S |
| **Alta** | **~104** | **~157** | |
| INA3221 × 2, microfoni, CAP1188, espansore (X15, X16, X18, X20) | 3 | 4 | S |
| ToF posteriore (X19) | 20 | 40 | V |
| **Media** | **~23** | **~44** | |
| ToF del mento, APDS-9960, MLX90640 (X25, X27, X29) | 49 | 163 | V |
| **Totale** | **~176** | **~364** | su 500 mA |

Senza X3 (3V3 della scheda) queste correnti passano dal regolatore della scheda, cioè dal 5 V. La prova al banco con le sole voci alte non basta: si ripete con le medie e prima delle basse.

**5 V** (D24V22F5, B2, 2,5 A):

| Voce | Tipica (mA) | Picco (mA) | Dati |
|---|---|---|---|
| ESP32 con Wi-Fi e camera (attraverso il 3V3 della scheda) | ~250 | ~500 | S |
| LED (X9, X11, X12, X21, X22), tetto del firmware | 50–150 | 600 | S |
| LED a riposo, 38–58 pixel (~1 mA ciascuno) | 40–60 | ~60 | S |
| Amplificatore (X17) | pochi | ~200 | S |
| **Alta e media** | | **~1360 (54 %)** | |
| Radar e LIDAR (X26, X28) | ~260 | ~380 | S |
| LED a riposo in più (X30, X31), fino a 94 pixel | ~35 | ~35 | S |
| **Con la bassa** | | **~1780 (71 %)** | |

Senza X3 il 5 V porta anche i sensori: circa 1560 mA (62 %) con alte e medie, circa 2140 mA (86 %) con la bassa.

Il tetto dei 600 mA vale solo con le protezioni in hardware di 2.4. Il D24V22F5 sta sotto l'ESP32, in uno spazio chiuso: si misura la sua temperatura al banco. Se scalda, un secondo D24V22F5 solo per luci e audio.

**F2** (2 A, ramo logica, dalla batteria), al caso peggiore di 6,6 V (sotto 3,5 V per cella il rail servo si spegne, ma la logica resta accesa fino a 3,3 V per cella, `software.md` 2.6), con rendimento 0,88 sul 5 V e 0,85 sul 3,3 V (S):
- alta e media: 7,7 W (5 V) + 0,8 W (3,3 V) + circa 0,4 W (VL della SSC-32) = 8,9 W, cioè 1,35 A: il 67 % di F2 (1,40 A, 70 %, senza X3);
- con la bassa: circa 11,9 W, cioè 1,8 A: il 90 % di F2 (1,9 A, 95 %, senza X3), poco margine per un fusibile. In quel caso F2 passa a 3 A (voce B6 da riapprovare).
- A 7,0 V le correnti sono il 6 % più basse; varrebbero solo se sotto 3,5 V per cella il firmware spegnesse anche LED e audio.

**Rail servo**: le spie (X13) prendono 4 mA per lato.

### 4.4 Massa e coppia

| Insieme | Massa in più | Di cui sulle zampe | Massa totale | Femore | Ginocchio |
|---|---|---|---|---|---|
| Oggi | — | — | 2945 g | 51,4 % | 47,1 % |
| Alta | ~58 g | 18 g | ~3003 g | 52,4 % | 48,1 % |
| Alta e media | ~99 g | 18 g | ~3044 g | 53,1 % | 48,7 % |
| Tutto | ~189 g | ~39 g | ~3134 g | 54,7 % | 50,2 % |

Coppie da `calc/statica_tripode.py` al punto di progetto 100/45, con la massa cambiata (S: il calcolo mette tutta la massa sul corpo). Il LIDAR da solo vale circa 1 punto. Costo indicativo: alta circa 150 €, media circa 90 €, bassa circa 200–230 € (S).

## 5. Da predisporre subito nel CAD

Solo voci alte, più le medie che toccano carapace e visiera, che si stampano una volta sola. Dopo ogni gruppo: le verifiche solite (interferenze, sentinella dei volumi, timeline). Parametri nuovi con i prefissi `sen_` (sensori) e `luc_` (luci).

**Prima di stampare tibie e piedini** (`zampa.py`):
- `Tibia`, punta dello stinco (X5): piana invece che raccordata R 3,8, con lo spigolo +X raccordato R 1 per la piega della coda, e accorciata da 108,4 a circa 107,6.
  - L'accorciamento passa da un parametro nuovo per la fine dello stinco, usato solo dalla `Tibia`. Non da `tib_piede_sp`, che alimenta `tib_z_arco` e quindi `tib_arco_R`: cambierebbero l'arco e la vite del guscio.
  - **La testa dell'FSR (Ø7,6, S) oggi non ci sta.** Sotto `tib_z_arco` (104,4) l'arco del fianco +X continua a stringere: a 107,6 lo stinco è largo circa 7,0 in X (da −3,9 a +3,15), e con il raccordo R 1 la parte piana resta di circa 6,3.
  - Si allarga la punta solo verso +X. Con `tib_x_piu_basso` da 4 a circa 6 la parte piana diventa circa 8,4, con lo spigolo −X vivo; con 5,5 resta 7,9, cioè 0,15 per lato.
  - Cambiano `tib_arco_R` (da 262 a circa 341), l'inserto e il bossolo della vite del guscio e il piedino: si rifanno `scansione` e `interferenze`.
  - Il lato −X non si tocca: al γ minimo lo stinco passa a 0,03 mm dalla coxa (D-061).
- `Tibia`: tasca 6 × 9 × 1,2 sulla faccia +X, dentro il piedino (Z −94,5…−110), per linguette e saldature dell'FSR.
- `Tibia`: gola 2 × 2 sulla faccia +X dello stinco e dello zoccolo, a Y ≈ +5, dal bordo del piedino al fondo della culla (Z −`cul_coda`, circa −33), non oltre.
  - Sulla culla una gola profonda 2 taglierebbe la parete (`cul_parete` 2) e scoprirebbe il servo; accanto alle finestre a rombo (fino a Y +3,5) resterebbe una lista di 0,5 mm.
  - Lungo la culla i fili passano nell'aria sotto il fronte del guscio, dove restano 3,1–5,7 mm (`cov_tib_sporgenza` meno `cov_tib_sp`), tenuti da un fermo, oppure in una gola profonda al massimo 0,8.
  - Resta sotto il guscio, fuori dalla finestra lunga (\|Y\| ≤ 3,5), dal bossolo della vite a Z 88 e dai tappi a rombo. Mai sul lato −X: al γ minimo lo stinco passa a 0,03 mm dalla coxa.
- `Piedino`: si costruisce da uno stinco con la punta nuova (piana, R 1) ma lungo 108,4, non dallo stinco accorciato.
  - Così fra la punta della tibia e il fondo del piedino restano gli 0,8 mm per FSR (0,3) e pistoncino (0,5), e la suola resta a `zam_Lt` (110): la cinematica non cambia.
  - Costruito dallo stinco a 107,6, la suola andrebbe a 109,2 (zampa più corta di 0,8) e la cavità non ci sarebbe.
  - Dentro: pistoncino Ø4,5 × 0,5 al centro della suola (più piccolo dell'area attiva, come chiede Interlink).
  - Fuori: lo svuotamento verso l'esterno di una punta piana dà una suola piana, non più arrotondata R 5,4. L'esterno si raccorda a parte, con un raggio da scegliere nel CAD.
  - Tacca 2 × 2 nel bordo alto sul lato +X per i fili.
- Attenzione: il piedino nasce da `_stinco` (D-064). Gola e tasca vanno solo nella `Tibia` (`fai_tibia`, non `_stinco`), altrimenti il piedino le copia, il TPU le riempie e schiaccia i fili.
- `Cover_Tibia`: niente. I fili escono dalla cima del guscio, che è aperto sopra, accanto al cavo del servo del ginocchio; se il bordo li schiaccia, una tacca 3 × 2.
- Verifiche: `scansione` (54 pose) e `interferenze` della zampa; suola a 110; poi un provino del piedino con un FSR: presa del cappuccio, scorrimento, piega della coda, quota di forza che il cappuccio si porta via per attrito.

**Prima della prima stampa del carapace** (`corpo.py` → `carapace`, `carapace_dettagli`, `fascia`, `visiera`):
- `Corpo_Visiera` (X8): finestra del ToF sotto l'occhio, a tronco di piramide sul campo di 60° × 60° inclinato di 20° in basso più 0,8; bocca esterna circa 10 × 9, centrata sull'asse fra z ≈ 3,5 e 13,5. Tappo nero a incastro dall'interno finché il sensore manca.
  - La cima sta a z ≤ 13,5: la bocca esterna dell'occhio comincia a z 14,56 (22,5 − `car_occhio_ve` 7,94), la bugna a 15. Così fra le due bocche resta un ponte di almeno 1 mm; con la cima a 14 sarebbe di 0,56, meno di due perimetri con l'ugello da 0,4.
  - Il sensore scende di conseguenza: centro a z ≤ circa 11,5, da ricavare nel CAD dalla sua posizione sulla scheda.
- `Corpo_Visiera` (X21, media): due tagli inclinati a 60°, larghi 1,5, da (\|y\| 13; z 16) a (\|y\| 18; z 25), riempiti di bianco; camere nere da x 96,5 a 100,4 chiuse verso l'occhio con pareti da 1,2, fori Ø2 per i fili.
- `Corpo_Carapace` (X2): sede della scheda del carapace, **posto da trovare nel CAD** (2.3). Lungo il lato +Y dell'ottagono non ci sta. Vincoli:
  - spine dei servo a \|y\| ≥ 19,5 fino a z 25,2;
  - battuta dello sportellino a \|y\| 14,5–17, z 32,8–34,4;
  - canali di X22;
  - passaggio dell'USB-C (\|y\| ≤ 13, z 14…24) libero;
  - spina IDC che si sfila dall'ottagono; testata con spina circa 9 + 9 mm, 470 µF Ø6,3–8, adattatore del TCA9534.
- `Corpo_Carapace` e `Corpo_Fascia` (X11): foro anulare Ø18–22 attorno al foro del pulsante (x −40), riempito dal bianco nella stampa a due colori; gola dall'interno che lascia 0,6–0,8 di bianco (valore dal provino X10); camera nera Ø32 × 4 (z 30,4…34,4) con sede piana per i due pixel a \|y\| 12–16, fuori dal dado del pulsante (circa Ø16, C). Da verificare: la camera arriva a \|y\| 16 e urta il canale di X22 (da \|y\| 14,25) fra x ≈ −47 e −33; camera Ø ≤ 28 oppure canale interrotto sopra il pulsante.
- `Corpo_Carapace` (X12): in ogni lobo una sede 5 × 22 × 0,6 con due ganci sulla faccia interna dello smusso esterno, centrata sulla direzione neutra della zampa; passaggio del cavo da lobo a lobo lungo le valli (y 56).
- `Corpo_Carapace` (X9): ganci passacavo alti 3 ogni 40 mm, fuori dalla battuta dello sportellino (x −21…29, \|y\| ≤ 17) e dai tubi dei pozzetti (x 40 e −56, \|y\| 17,8–27,2).
- `Corpo_Carapace` e `Corpo_Fascia` (X16, media): due fori Ø1 nella fascia sopra la testa, a x ≈ 89, con un anello stampato attorno per la guarnizione; due sedi sotto la pelle per i microfoni (porta sul fondo: scheda a faccia in giù sul foro).
  - \|y\| dei fori: **posto da trovare nel CAD**. Centrate su \|y\| 11, le schede (12,7 lungo y) arrivano a \|y\| 17,35 e entrano nel canale di X22, che parte da 17,2; con il canale allargato (X22) lo spazio fra canale e flat della camera si stringe ancora.
  - Si sceglie se spostare i microfoni o interrompere il canale sopra di loro.
- `Corpo_Carapace` (X17, X19, media): sulle guance di coda (\|y\| 25,4), il supporto del ToF posteriore sulla guancia lontana dallo spinotto di bilanciamento e la sede dell'altoparlante sull'altra. Sede dell'amplificatore: posto da trovare nel CAD (2.3).
- `Corpo_Carapace` (X18, media): zone piane 15 × 25 senza ganci né nervature per gli elettrodi (smusso del viso x 96…101, coda x −91…−83, piano dei lobi) e la sede del modulo CAP1188; niente elettrodi sopra l'antenna.
- `Corpo_Carapace` (X22, media): gola a \|y\| 17–18,5 che lascia 0,6–0,8 di bianco e canali neri a U (pareti 0,8, alti 5), in tre tratti per lato; passaggio nelle paratie dietro la testa (x 81…82,6).
  - L'interno del canale è largo almeno la striscia più 0,4 (≥ 5,4) ed è centrato sulla gola (\|y\| 17,75). A \|y\| 17,2–21 l'interno era di 2,2 mm e la striscia (4–5) non entrava.
  - Con pareti da 0,8 il canale occupa \|y\| 14,25–21,25 e z 29,4…34,4. Lungo l'ottagono (x −21…29) urta la battuta dello sportellino (\|y\| 14,5–17): il tratto centrale si spezza o si ridisegna nel CAD.
  - Nel tratto posteriore urta il collare del cicalino (\|y\| 20,2–21,4, z 25,4…34,4) per tutto x −87…−62, e il cicalino stesso se è alto più di 12 (D-059 gli lascia 14, fino a z 31,4): il tratto si toglie o si sposta.
  - Nel tratto centrale urta la camera nera di X11 fra x ≈ −47 e −33: canale interrotto sopra il pulsante, oppure camera Ø ≤ 28.
  - Poi si ricontrollano le distanze dai pozzetti (\|y\| ≥ 17,8 a x 40 e −56).
- Se si vogliono (bassa): finestra dei gesti 5 × 4 nella fascia a x ≈ 40 (X27); sede del radar sotto il dorso (X26); finestra della termocamera (X29).
- Verifiche: `sfilamento` a 5, 10, 20 e 40 mm con le schede montate; `campo` della camera invariato; `carapace_zampe` con l'ingombro delle strisce nei lobi (oggi 4,6 mm sulle zampe medie); T-plug e spinotto di bilanciamento si afferrano dalla porta di servizio con ToF e altoparlante montati; assieme senza interferenze.

**`Corpo_Vassoio`**:
- Mensola della camera (x 92,5…98,5, \|y\| ≤ 6, z 1…18,25) come plancia del viso (X8): sede inclinata di 20° per la scheda del ToF (13 × 18 × 3), con il sensore a z ≤ circa 11,5 (finestra sotto l'occhio) e il lato da 13 lungo y (\|y\| ≤ 6,5, dentro la parete del mento a \|y\| 7,35); due perni Ø1,9 o due inserti M2 sui fori della scheda (C); fessura nel piede della mensola fino a z ≈ −0,5; canale per 4 fili lungo la torretta. La testa della camera resta appoggiata sopra. Da verificare con il disegno Pololu (posizione del sensore sulla scheda, C): la scheda inclinata arriva a z ≈ 16,4 e circa 6 mm più avanti del piede, vicino alla bugna dell'occhio (x ≥ 99,4, z ≥ 15, \|y\| ≤ 11) e sotto la testa della camera. Verifiche: interferenza con la visiera, rigidità della mensola, `campo`, `sfilamento`.
- Asola 6 × 3 a x ≈ 50, lato +Y (y 13…16), sotto la fascia libera della basetta, per il bus verso il vano sotto il vassoio (X1).

**`Corpo_Base`**:
- Prima va deciso dove sta l'interruttore 2813 (20,3 × 25,4 × 4,1, posto ancora aperto): nel vano sotto il vassoio non ci stanno 2813, IMU e ADS7830 insieme. Se la 2813 va lì, l'ADS7830 va altrove: posto da trovare nel CAD (sopra i Wago non ci sta, vedi INA3221).
- IMU (X4): due bugne Ø5,5 alte 2 sul tetto (fino a z −7,4), con inserti M2 × 2 del kit (D5); il foro lascia 1 mm di tetto sopra il pacco. Interasse dal disegno Pololu (C). Gioco di 1 mm attorno a 13 × 23. Freccia dell'asse X stampata sul tetto.
- ADS7830 (X6): due bugne con inserti M2 (fori C), accanto all'IMU; posto per la striscia dei partitori.
- Le sei prese a 3 poli dei piedi non vanno sotto il vassoio: lì si arriva solo togliendo `Corpo_Vassoio`, con basetta, ESP32, torretta e mensola, e le prese si staccano a ogni smontaggio di una zampa. Vanno dove si raggiungono a carapace tolto: posto da trovare nel CAD.
- Passaggi (X1, X5): 4 fili del bus fra il bordo anteriore della SSC-32 (x 22) e il vassoio (x 26); due clip sul tetto; cavi dei piedi dalle file della SSC-32 alle loro prese, e dalle prese al vano sotto il vassoio.
- Spie dei rail (X13): linguetta sul tetto in coda, sotto il cicalino, con due fori Ø3,1 rivolti all'indietro, a \|y\| ≈ 10; posto da trovare con F1, T-plug e cavi della batteria.
- INA3221 (X15, media): **posto da trovare nel CAD**.
  - Sulla parete del tunnel sopra i Wago (x −50…−12, z −10…+13) non ci sta. La scheda, alta 10,5 con le morsettiere, sporge fino a \|y\| ≈ 37,5. I Wago stanno a x −46…−16, \|y\| 27,5–35,8, con la cima a z −11,35 e i fili che entrano dall'alto (D-055).
  - La scheda finirebbe 1,35 mm sopra gli ingressi, sulla stessa pianta: i cavi da 12–16 AWG non entrerebbero. Lì passano anche le anse dei cavi dei servo.
  - Serve un posto fuori dalla pianta dei Wago e sopra il raggio di curvatura dei cavi, da dimostrare nel CAD prima di tenere X15 in media priorità. Verifiche: leve dei Wago apribili (12 mm d'aria), cavi da 12 e 14 AWG, anse.

**`Corpo_Slitta_Regolatore`** (X7): prolungata verso l'alto fino a circa z 32, con due inserti M2 per l'INA260 sulla faccia verso il tunnel (x 14…37) e la morsettiera in alto. Verifiche: smusso del carapace, gonne, cavi delle zampe anteriori, feritoie a \|y\| 30 aperte. Se non entra: scheda in linea nel 16 AWG, fissata alla parete del tunnel. Circa 2 g in più per lato.

**`Corpo_Chiglia`**, `Coxa`, `Coxa_Ponte`, `Femore_A`, `Femore_B`: niente. I fili dei piedi seguono le fascette esistenti (blocco del femore, ponte).

**Libreria Fusion** (`rif_componenti.py` → `ingombri`): ingombri nuovi per IMU (13 × 23 × 3), ToF 8 × 8 (13 × 18 × 3), ToF semplice (13 × 18 × 2), INA260 (22,9 × 22,8 × 2,7 più la morsettiera), INA3221 (38,6 × 22,9 × 10,5), ADS7830 (30,5 × 17,7 × 4,7), D24V5F3 (13 × 10 × 3), scheda del carapace con la spina IDC, MAX98357A (19,4 × 17,8 × 3), altoparlante (15 × 11 × 3), microfono (16,7 × 12,7 × 1,8), FSR (Ø7,6 × 0,3 con coda da 16).

## 6. Idee scartate

- **Bus I2C condiviso con la camera** come soluzione di base: lo scorrimento degli indirizzi di esp32-camera e il rischio di fermare la camera (2.2). Resta la riserva, con i ToF a indirizzi fuori dalla tabella della camera.
- **I2C sul GPIO2**: il LED "ON" carica la linea.
- **Magnetometro, IMU a 9 assi**: fra 18 motori, cavi da 13 A e un corpo in carbonio la direzione non è affidabile.
- **BNO085**: problemi noti di clock stretching con ESP32-S3 (Adafruit).
- **IMU sotto la SSC-32**: fili di potenza sotto la scheda. Per arrivarci si smonta la SSC-32, come sotto il vassoio si toglie il vassoio (2.9).
- **Misura di corrente sulla batteria**: nessun modulo I2C pronto per 30 A (l'INA228 di Adafruit arriva a 10 A, l'INA780 esiste solo come scheda di valutazione). La corrente di batteria si stima dai due rail, non si misura: gli INA260 stanno all'uscita dei regolatori, a 6 V. Servono il rendimento dei regolatori, che non si misura, e il ramo logica (4.3), da aggiungere a parte.
- **Corrente per zampa tagliando le barre della SSC-32**: fino a 8 A in morsetti da 3,5 e piste senza dati.
- **Celle di carico con HX711, microinterruttori nei piedi**: decine di grammi per zampa, oppure solo sì/no senza posto per la corsa.
- **I2C o collettore rotante lungo le zampe; accelerometri sulle zampe**: fili e disturbi attraverso tre giunti per informazioni che danno piedi e IMU.
- **Due ADS1115 nelle baie posteriori, ingressi della SSC-32 come ADC principale**: 2.9.
- **Sonar HC-SR04**: 8,5 g, cono largo che vede le zampe, eco a 5 V, due GPIO.
- **Sensori IR analogici Sharp**: nessun ingresso ADC libero sull'ESP32 (l'ADC2 è conteso dal Wi-Fi).
- **VL53L5CX**: campo più stretto del VL53L7CX, nessun vantaggio. Il VL53L8CX (65° in diagonale, migliore in luce forte) resta l'alternativa per l'esterno.
- **Sensori laterali, ToF verso il basso ai quattro angoli**: lì girano le zampe; ruotando sul posto il ToF frontale guarda di lato.
- **Grid-EYE AMG8833**: 8 × 8 pixel, troppo poco dettaglio.
- **LIDAR STL-27L**: 46 g e 1,45 W, 25 m inutili in casa.
- **Altoparlante nel viso**: il posto sotto l'occhio va al ToF frontale (2.9).
- **Microfoni PDM**: un pin in più rispetto agli I2S condivisi con l'amplificatore.
- **Microfono sotto lo sportellino**: un solo microfono non dà la direzione, e lo sportellino si toglie.
- **Display OLED nella fascia**: stesso posto del sensore dei gesti, vicino all'antenna; le stesse informazioni arrivano dalla pagina web, dai LED e dalla voce, e il cicalino ha già un display.
- **Display come occhio**: l'occhio è la camera, integrata nel frontale (decisione dell'utente).
- **LED nelle finestre esagonali delle lame del femore**: nessuno spazio fuori dalle piastre (zampe vicine a contatto a 31–32°), le finestre servono a raggiungere le viti, i fili attraverserebbero due giunti. Le luci dei lobi illuminano già le lame.
- **Traslatore BSS138 (C1) per il dato dei LED**: troppo lento con i pull-up da 10 kΩ.
- **LED sul rail a 6 V**: oltre i 5,5 V dei LED, e il rail è spento di default.
- **Pixel RGBW mescolati agli RGB**: protocollo diverso (32 bit per pixel).
- **MPR121 per il tocco**: fuori produzione (NXP). **Moduli TTP223**: un GPIO per tasto.
- **RP2040 o ESP32-C3 come nodo dei piedi**: troppo pochi ingressi analogici.
- **Hub Qwiic sotto lo sportellino**: lì passa la spina USB-C e non c'è appoggio.
- **Sonda di temperatura sulla batteria**: in media circa 2C, scalda poco.
- **Contatto sotto la chiglia**: lo deducono IMU e correnti.

## 7. Domande per l'utente

1. Rinunci alla microSD? Se sì, piano A (microfoni stereo e altoparlante I2S). Se no, piano B: niente microfoni, audio semplice.
2. Approvi le priorità? Le voci alte cambiano tibia, piedino, visiera e carapace prima della loro prima stampa.
3. Va bene l'altoparlante in coda, con il suono che esce dalla porta di servizio, invece che nel viso, che serve al ToF?
4. I comandi vocali offline funzionano solo in inglese (ESP-SR). Vanno bene, o preferisci che l'audio vada al telefono o al PC?
5. Luci: ti interessano anello del pulsante, lobi, fessure dell'occhio, linee della fascia e luci nelle tibie? Le luci nelle tibie (X31) chiuderebbero con 0,6 di bianco la finestra lunga del guscio, approvato in D-061 con la finestra aperta. Che colori? Va bene un tetto di 600 mA, con pull-down e PTC sul 5 V dei LED?
6. All'arrivo della SSC32-V2.5 (D-045: si studia dalle immagini dell'inserzione, il retro si guarda all'arrivo), puoi mandare una foto dal lato delle prese? Si cerca se ha gli ingressi A–D (o A–H) e le uscite; poi una prova al banco con un partitore.
7. Ti interessano il LIDAR sulla schiena (cresta che gira, circa 50 g e 80 €; toglie i microfoni, perché la USB nativa resta al debug e al computer di bordo, e la sella coprirebbe i loro fori) e la termocamera (circa 75 €)?
8. Hai un MG996R di scorta da aprire per la prova del potenziometro (X32)? Non è urgente.

## 8. Fonti

Lette oggi per questo documento:
- [Pololu #2798, LSM6DSO](https://www.pololu.com/product/2798): quote, massa, indirizzo 1101011b (0x6B), 1,8–5,5 V, 1 mA, fori M2.
- [Pololu #2842, D24V5F3](https://www.pololu.com/product/2842): 3,3 V, 500 mA, ingresso 3,4–36 V, 13 × 10 × 3, 200 µA a vuoto, 8,95 US$.
- [esp32-camera, `esp_camera.c`](https://github.com/espressif/esp32-camera/blob/master/driver/esp_camera.c) e [`sccb-ng.c`](https://github.com/espressif/esp32-camera/blob/master/driver/sccb-ng.c): scorrimento della tabella degli indirizzi all'avvio, bus condiviso con `pin_sccb_sda = -1` e `sccb_i2c_port`.
- `calc/statica_tripode.py` con la massa cambiata (4.4) e per il carico massimo su un piede (2.9).
- [Pololu #3418, VL53L7CX](https://www.pololu.com/product/3418), riletta dopo la revisione: VIN 3,3–5,5 V nella piedinatura e 2,5–5,5 V nelle specifiche; pin VDD come ingresso fra 2,5 e 3,6 V con VIN scollegato; SDA e SCL al livello di VIN, o di VDD se si alimenta da VDD.
- [esp32-camera, `Kconfig`](https://raw.githubusercontent.com/espressif/esp32-camera/master/Kconfig): supporto dell'OV2640 attivo di default; SCCB su I2C1 di default.
- [Adafruit #6062, INA3221](https://www.adafruit.com/product/6062): 38,6 × 22,9 × 10,5, 5,8 g, morsettiere da 3,5 mm, 0x40 o 0x41.
- [Interlink FSR 400 Short](https://www.interlinkelectronics.com/fsr-400-short): area attiva Ø5,6; la pagina non dà il diametro della testa (resta S).
- NXP UM10204 (specifica dell'I2C), tabella 10 e §7.1: non riletta, il PDF non si legge da qui. Valori citati dal revisore: S.

Dalle quattro ricerche (fonti primarie lette dai ricercatori, che hanno messo le marcature V; non rilette nella sintesi). Il revisore ne ha ricontrollato un campione il 9 ottobre e corrisponde: Pololu #2798, #2842, #3415; Adafruit #4226, #6062, #5836; indirizzi del CAP1188; FSR 400 (Ø5,6, 0,2–20 N, ±6 % fra pezzi diversi).
- Bus e GPIO: [esp_camera.h](https://github.com/espressif/esp32-camera/blob/master/driver/include/esp_camera.h), [sensor.h](https://github.com/espressif/esp32-camera/blob/master/driver/include/sensor.h), [GPIO dell'ESP32-S3](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/gpio.html), [checklist dello schema ESP32-S3](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html), [I2S dell'ESP32-S3](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/i2s.html), [sensori tattili dell'ESP32-S3](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/cap_touch_sens.html), [ESP-SR](https://components.espressif.com/components/espressif/esp-sr), [indirizzi I2C (Adafruit)](https://learn.adafruit.com/i2c-addresses/the-list), [chip problematici (Adafruit)](https://learn.adafruit.com/i2c-addresses/troublesome-chips), [Qwiic (SparkFun)](https://www.sparkfun.com/qwiic), [cavo Adafruit 4209](https://www.adafruit.com/product/4209).
- Stato del robot: [ST LSM6DSO](https://www.st.com/en/mems-and-sensors/lsm6dso.html), [TI INA260](https://www.ti.com/product/INA260), [Adafruit INA260](https://www.adafruit.com/product/4226) e [piedinatura](https://learn.adafruit.com/adafruit-ina260-current-voltage-power-sensor-breakout/pinouts), [Adafruit INA3221](https://www.adafruit.com/product/6062), [Adafruit ADS7830](https://www.adafruit.com/product/5836), [Interlink FSR 400 Short](https://interlinkelectronics.com/fsr-400-short) e [serie 400](https://www.interlinkelectronics.com/fsr-400-series), [TDK B57861S0103F040 (Arrow)](https://www.arrow.com/en/products/b57861s0103f040/tdk.html), [Pololu D42V110F6](https://www.pololu.com/product/5673) (PG, rendimento), [Adafruit INA228](https://www.adafruit.com/product/5832), [TI INA780B](https://www.ti.com/product/INA780B).
- Ambiente: [Pololu #3418 VL53L7CX](https://www.pololu.com/product/3418), [Pololu #3419 VL53L8CX](https://www.pololu.com/product-info-merged/3419), [ST VL53L7CX](https://www.st.com/en/imaging-and-photonics-solutions/vl53l7cx.html), [Pololu #3415 VL53L1X](https://www.pololu.com/product/3415), [Pololu #3692 VL53L4CD](https://www.pololu.com/product/3692), [Hi-Link HLK-LD2410C (manuale, copia di terzi)](https://www.manualslib.com/manual/3223606/Hi-Link-Hlk-Ld2410c.html), [Broadcom APDS-9960](https://cdn.sparkfun.com/assets/8/9/3/5/1/av02-4191en_ds_apds-9960_2015-11-13.pdf), [Adafruit 3595](https://www.adafruit.com/product/3595), [Vishay VEML7700](https://www.vishay.com/docs/84286/veml7700.pdf), [LIDAR LD19 (Waveshare)](https://www.waveshare.com/wiki/DTOF_LIDAR_LD19), [LD06 (ArduPilot)](https://ardupilot.org/rover/docs/common-ld06.html), [Melexis MLX90640](https://media.melexis.com/-/media/files/documents/datasheets/MLX90640-datasheet-melexis.pdf), [Adafruit 4469](https://www.adafruit.com/product/4469).
- Luci e interazione: [famiglia WS2812 (Worldsemi)](http://www.world-semi.com/ws2812-family/), [SK6812MINI-E (Opsco)](https://akizukidenshi.com/goodsaffix/sk6812mini-e.pdf), [TI SN74AHCT1G125](https://www.ti.com/product/SN74AHCT1G125), [alimentare i NeoPixel (Adafruit)](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels), [Adafruit 757 (BSS138)](https://www.adafruit.com/product/757), [Pololu D24V22F5](https://www.pololu.com/product/2858), [Pololu 2813](https://www.pololu.com/product/2813), [Adafruit 3006 (MAX98357A)](https://www.adafruit.com/product/3006), [CUI CMS-15113-078](https://jp.cuidevices.com/product/resource/cms-15113-078x.pdf), [Adafruit 3421 (SPH0645)](https://www.adafruit.com/product/3421), [Adafruit 1602 (CAP1188)](https://www.adafruit.com/product/1602), [NXP MPR121](https://www.nxp.com/products/MPR121), [prova di diffusione nel PLA](https://newscrewdriver.com/2019/07/18/glow-flow-led-diffusion-test-3d-printed-sheet/), [traslucenza del PLA (MDPI 2024)](https://doi.org/10.3390/polym16202862).
- Integrazione: [SSC-32U (Lynxmotion)](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/servo-erector-set-system/ses-electronics/ses-modules/ssc-32u/), [lettura degli ingressi della SSC-32 (forum RobotShop)](https://community.robotshop.com/forum/t/how-do-i-read-analog-voltages-on-ssc-32/14335), [uscite discrete della SSC-32 (forum RobotShop)](https://community.robotshop.com/forum/t/discrete-output-how-much-current-can-be-gather-from-the-pin/18430), [TI TCA9534](https://www.ti.com/product/TCA9534), [Adafruit PCA9548](https://www.adafruit.com/product/5626), [Adafruit 5690 (seesaw)](https://www.adafruit.com/product/5690), [Adafruit QT Py SAMD21](https://www.adafruit.com/product/4600), [JST PH](https://cdn.sparkfun.com/assets/0/e/f/7/2/ePH.pdf).

Documenti del progetto: `dimensioni-componenti.md` (piedinatura UICPAL, SSC-32), `studio-componenti.md` (GPIO, alimentazione, correnti), `BOM.md` (schema di alimentazione, B2, B6, C1, C2, C5), `progetto-meccanico.md` (corpo, carapace, zampe, cavi, masse), `decisioni.md` (D-050…D-065), `ricerca/estetica-specifica.md` (quote del carapace), `cad/script/corpo.py` e `zampa.py` (parametri).
