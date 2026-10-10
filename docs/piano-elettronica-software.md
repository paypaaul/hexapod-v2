# Piano: sensori, elettronica e software (backlog)

9 ottobre 2026. Proposta da approvare: niente è approvato né comprato. I dettagli stanno in `predisposizioni.md` (sensori, luci, espansioni) e in `software.md` (firmware, controllo, RL, visione).

Legenda: **V** verificato su fonte primaria; **S** stimato o da fonte secondaria; **C** da confermare sul pezzo reale. In `software.md`, e per le fonti dei ricercatori in `predisposizioni.md` (sezione 8), V vuol dire fonte primaria indicata dai ricercatori e non riletta nella sintesi. Codici X1…X33 come in `predisposizioni.md`; fasi S0…S9 come in `software.md`; fasi P0…P10 di questo piano. Le fasi 1–6 di `CLAUDE.md` restano: P0 prepara il CAD dentro le fasi 4–6, che si chiudono dopo i provini di P1, con i loro valori riportati nel CAD; da P1 in poi si stampa e si costruisce. Quote in mm, terna del robot (X avanti, Y a sinistra, z 0 sugli assi dei femori) o della zampa dove è detto.

## 1. Cosa saprà fare il robot

- **P0**: niente di fisico. Il gemello nel browser e in MuJoCo cammina con le andature di `calc/`; nel CAD ci sono le sedi dei sensori.
- **P1–P2**: al banco l'ESP32 parla con la SSC-32, muove un servo, manda il video e legge IMU, ToF e un piede di prova.
- **P3**: una zampa tarata con le dime si muove nei suoi limiti. L'accensione non dà scatti e ogni guasto spegne il rail.
- **P4**: cammina guidato dal telefono, a coppie e a tripode. Si alza, si siede, si ferma se perde il collegamento. Le luci dicono in che stato è.
- **P5**: tiene il corpo orizzontale, cerca l'appoggio con i piedi, va in posa sicura sul pendio, si accorge di un giunto bloccato.
- **P6**: vede persone e volti a bordo (3–5 fps), li segue, si ferma davanti agli ostacoli e al bordo del tavolo. Se approvati: parla, ascolta, sente il tocco.
- **P7**: con il PC acceso capisce obiettivi in linguaggio naturale e riconosce gli oggetti. I limiti restano nel firmware.
- **P8**: cammina con un'andatura corretta da una politica appresa, più robusta sul terreno irregolare.
- **P9**: va in una stanza e torna, con mappa e marcatori AprilTag. Si decide se serve un computer di bordo.
- **P10**: supera gradini bassi e ostacoli con una politica appresa; senza PC solo se c'è il computer di bordo.

## 2. Architettura unica

### 2.1 Blocchi e collegamenti

Tre livelli. L'ESP32-S3 è il "midollo spinale": andature, cinematica, guardia, sicurezza, sensori e visione leggera, sempre attivi anche senza rete. Il Mac o un PC è il "cervello" facoltativo: percezione pesante, mappa, navigazione, LLM, simulazione e addestramento. Un computer di bordo si predispone ma non si compra.

```
 telefono: app, gamepad, STOP          Mac o PC: ponte, Rerun, percezione, MuJoCo, MCP, LLM
            |  WebSocket                          |  UDP 50 Hz, video MJPEG (porta 81)
            +------------ Wi-Fi 2,4 GHz ----------+
                                 |
 +-------------------------------+---------------------------------------------------+
 | ESP32-S3-CAM N16R8                                                                 |
 | core 1: ctrl 50 Hz (stato, andatura, IK, politica, guardia, UART) | sens 100 Hz    |
 |         | infer 2-7 Hz a priorità bassa                                            |
 | core 0: Wi-Fi, HTTP e WebSocket, camera, telemetria, OTA (e audio, se approvato)   |
 +---+---------+---------+------------+------------+--------+----------+------------+
     |         |         |            |            |        |          |            |
   UART1     SCCB      I2C0          I2S        GPIO48    GPIO1    GPIO42/41    USB OTG
   21/14     4/5       47/3      38/39/40/2       |         |          |         19/20
     |         |         |            |            |        |          |            |
   SSC-32   OV3660   bus dei     microfoni     buffer   partitore   rail 6 V,   Mac al banco
     |               sensori     (X16) e       a 5 V    batteria    OFF della   (flash, HIL);
  18 MG996R          (2.4)       ampli (X17)   catena               2813        poi computer
                                               LED (X9)                         di bordo
```

Il bus dei sensori parte dalla basetta (pull-up, D24V5F3 se serve):

```
 basetta ─┬─ vano sotto il vassoio: IMU (0x6B), ADS7830 (0x48) ← 6 FSR dei piedi, 2 NTC
          ├─ baie anteriori: INA260 sinistro (0x44) e destro (0x45) sulle slitte
          ├─ mensola della camera: ToF frontale VL53L7CX (0x30)
          └─ cavo piatto 16 poli ─ scheda del carapace: presa Qwiic, TCA9534 (0x20), CAP1188 (0x28),
                                   ToF posteriore (0x31), microfoni e ampli (I2S), LED, pulsante
```

Simulatore e prove: il nucleo C++ (IK, andature, guardia, modello dei servo, politica) si compila anche sul Mac. Gira con MuJoCo e con l'emulatore Python della SSC-32 (SIL, anche in CI). Al banco l'ESP32 vero gira con i sensori simulati dal Mac attraverso la USB OTG (HIL). Una sola descrizione del robot, esportata dal CAD in sola lettura (`esporta_robot.py`), genera l'header del firmware, le costanti di `calc/` e i modelli URDF e MJCF.

### 2.2 Alimentazione

```
Batteria 2S ─ T-plug ─ F1 30 A ─ Wago ─┬─ D42V110F6 sinistro 6 V ─ INA260 (X7) ─ VS1, 9 servo ─ spia (X13)
                                       ├─ D42V110F6 destro 6 V   ─ INA260 (X7) ─ VS2, 9 servo ─ spia (X13)
                                       └─ F2 2 A ─ 2813 ─┬─ D24V22F5 5 V ─┬─ ESP32 (pin 5V)
                                                         │                ├─ catena LED (PTC, tetto 600 mA)
                                                         │                └─ amplificatore; radar e LIDAR se approvati
                                                         ├─ D24V5F3 3,3 V ─ bus dei sensori (se la prova del 3V3 fallisce)
                                                         ├─ VL della SSC-32
                                                         ├─ partitore ─ GPIO1
                                                         └─ eventuale 5 V 3 A ─ computer di bordo (Radxa o Pi Zero)
GPIO42 ─ diodo ─ abilitazione dei due D42V110F6 (rail spento di default, D-019)
```

- Gli INA260 stanno all'uscita dei regolatori: misurano i rail a 6 V. La corrente di batteria si stima (rendimento più ramo logica), non si misura.
- Ogni sensore dei piedi ha il suo filo di massa: lungo la zampa passano solo massa e segnale, mai il 3,3 V.
- Lo zaino Pi 5 con AI HAT+ 2 (5 V 5 A) avrebbe un'alimentazione propria, fuori da F2.
- Senza X3 i sensori prendono il 3,3 V dal regolatore della scheda, che lo ricava dal 5 V: i bilanci di 3.2 e 3.3 hanno le due varianti.

### 2.3 GPIO: una sola assegnazione

Piano A: senza microSD (la scatola nera va in LittleFS, le registrazioni sul Mac).

| GPIO | Uso | Stato | Nota |
|---|---|---|---|
| 0, 45, 46 | strapping | non usare | |
| 1 | tensione di batteria (ADC1_CH0, partitore B10) | deciso | |
| 2 | dati I2S verso l'amplificatore (X17) | proposta | porta il LED "ON" della scheda, che lampeggia con il segnale: innocuo (polarità da provare). Mai I2C: il LED carica la linea |
| 3 | SCL del bus dei sensori (I2C0) | proposta | strapping solo con l'eFuse STRAP_JTAG_SEL bruciato; con il pull-up sta alto, la scelta predefinita (V); prova in P2 |
| 4, 5 | SCCB della camera (I2C1), da sola | sulla scheda | |
| 6–13, 15–18 | camera (DVP) | sulla scheda | |
| 14 | UART1 RX ← SSC-32 | deciso (D-012) | |
| 19, 20 | USB OTG: flash, JTAG, HIL; poi l'eventuale computer di bordo | da riservare | non va al LIDAR |
| 21 | UART1 TX → SSC-32 | deciso (D-012) | |
| 35–37 | PSRAM | non usabili | |
| 38 | BCLK I2S | proposta | in P2, prima dell'audio: ingresso RMT per misurare al banco gli impulsi della SSC-32 (canale libero del traslatore C1) |
| 39 | WS I2S | proposta | |
| 40 | dati dei microfoni (X16) | proposta | RX del LIDAR solo rinunciando ai microfoni |
| 41 | OFF della 2813 | deciso | 100 kΩ verso massa se scatta con il GPIO flottante (C, P2) |
| 42 | accensione del rail servo | deciso (D-019) | spento con il GPIO flottante |
| 43, 44 | UART0 (CH340): console | sulla scheda | |
| 47 | SDA del bus dei sensori (I2C0) | proposta | la riserva della RX della SSC-32 (`studio-componenti.md`) sparisce |
| 48 | catena LED, in parallelo al WS2812 della scheda (ripete il primo pixel) | proposta | buffer a 5 V sulla basetta, pull-down 10 kΩ all'ingresso |

- **Nessun GPIO libero.** Niente interrupt: si legge a intervalli. XSHUT dei ToF e uscita del radar passano dall'espansore X20. Ogni funzione nuova passa dal bus I2C o toglie qualcos'altro.
- **Piano B** (con la microSD): 38–40 alla scheda TF, niente microfoni né amplificatore I2S. Resta un audio semplice sul GPIO2 (PAM8302A). La misura RMT al banco si fa prima di montare la TF.

### 2.4 Indirizzi I2C: una sola tabella

Bus dei sensori: I2C0, GPIO47 SDA, GPIO3 SCL, 400 kHz, 3,3 V.

| Indirizzo | Dispositivo | Voce | Priorità | Come si ottiene |
|---|---|---|---|---|
| 0x10 | VEML7700 | X24 | riserva | fisso |
| 0x20 | TCA9534 | X20 | media | piedini A0–A2 (0x20–0x27) |
| 0x28 | CAP1188 | X18 | media | AD a 3,3 V (il predefinito 0x29 è dei ToF) |
| 0x29 | VL53L4CD sotto il mento | X25 | bassa | di fabbrica, l'ultimo acceso |
| 0x30 | VL53L7CX frontale | X8 | alta | dal firmware a ogni accensione, con gli altri ToF spenti |
| 0x31 | VL53L1X posteriore | X19 | media | dal firmware |
| 0x33 | MLX90640 | X29 | bassa | di fabbrica |
| 0x39 | APDS-9960 | X27 | bassa | fisso |
| 0x40, 0x41 | INA3221 sinistro, destro | X15 | media | di fabbrica; ponticello |
| 0x44, 0x45 | INA260 sinistro, destro | X7 | alta | ponticello A1; A0 e A1 |
| 0x48 | ADS7830 | X6 | alta | di fabbrica |
| 0x49…0x4B | ADS7830 in più | X32 | bassa | ponticelli |
| 0x4C | seesaw | X33 | bassa | ponticelli (0x49 se X32 non c'è) |
| 0x6B | LSM6DSO | X4 | alta | di fabbrica (V) |

Bus della camera: I2C1 (SCCB), GPIO4 e GPIO5. Solo la OV3660 (0x3C). All'avvio esp32-camera prova gli indirizzi dei sensori di camera compilati (0x21, 0x30, 0x3C, 0x68 e altri, V): per questo i sensori non stanno su quel bus. Se mai servisse la riserva (bus condiviso), i ToF vanno a indirizzi fuori da quella tabella (per esempio 0x52 e 0x53, da ricontrollare sulla versione del driver).

Nessun conflitto. INA260 e INA3221 nascono tutti a 0x40: i ponticelli si fanno prima di collegarli.

Pull-up: obiettivo 1,0–1,4 kΩ in tutto, minimo 0,97 kΩ (S, specifica NXP non riletta). Schede Adafruit con 10 kΩ ciascuna:
- alta: 3 (INA260 × 2, ADS7830), 3,3 kΩ;
- alta e media: 6 (più INA3221 × 2 e CAP1188), 1,67 kΩ;
- tutto: 11–12 (più APDS-9960, MLX90640, 2–3 ADS7830 di X32, seesaw), 0,83–0,91 kΩ, sotto il minimo.

A questi si aggiungono i pull-up propri dei Pololu (IMU e ToF; valore dal loro schema, C). Regola: le schede di X27, X29, X32 e X33 si montano con i pull-up staccati (ponticello dove c'è, altrimenti resistenze tolte), così l'equivalente resta quello di alta e media. Se con i Pololu la resistenza misurata scende sotto 1,0 kΩ già con alta e media, si staccano anche quelli di INA3221 e CAP1188.

### 2.5 Compiti del firmware che toccano l'hardware

- **UART della SSC-32**: un solo proprietario, `ctrl`. Manda il gruppo dei 18 canali, le domande del battito (`Q`, `QP`) e, se servono, legge gli ingressi A–D allo stesso ritmo. A 115200 baud il gruppo ASCII occupa 11,3–13,1 ms su 20: in P2 si prova cosa accetta il clone (230400, modo binario). Un cambio di baud o di formato modifica D-012 (115200): va registrato in `decisioni.md`.
- **Bus dei sensori**: lo legge `sens` sul core 1 a 100 Hz (IMU dalla FIFO, ADS7830, INA260), il ToF al suo ritmo. Requisito di `software.md` 4.3: contatti con meno di 10 ms di ritardo. Una lettura 8 × 8 del VL53L7CX con tutte le uscite del driver vale circa 1–1,5 KB, cioè 25–35 ms a 400 kHz (S). Proposta: nessuna transazione oltre circa 5 ms, metà del periodo dei contatti. Per stare dentro, il ToF si legge con le sole uscite che servono (distanza e stato). Si misura in P2.
- **Bus a 100 kHz**: porta circa un quarto del traffico. Il carico stimato a 400 kHz con alta e media (30–50 %, `predisposizioni.md` 2.2) varrebbe il 120–200 %, e i requisiti di `software.md` 4.3 non si rispetterebbero. Ripiego a 100 kHz, conto S: IMU a 208 Hz letta dalla FIFO a pacchetti (~3 KB/s), sei FSR a 100 Hz (~2,5 KB/s), INA260 con la media interna e la sola corrente a 50 Hz (~0,5 KB/s), ToF frontale in 4 × 4 a 15 Hz con le letture spezzate sotto i 5 ms (~1,5 KB/s), voci medie a 10 Hz (~0,6 KB/s). Sono circa 8 KB/s, tre quarti del bus: al limite, da misurare. Senza oscilloscopio si parte a 400 kHz contando gli errori del bus (NACK, timeout, valori fuori campo) in prove lunghe; 100 kHz solo se gli errori ci sono.
- **LED**: la catena si comanda con l'RMT su GPIO48. Il tetto dei 600 mA sta nel driver; pull-down e PTC lo coprono durante reset e avvio.
- **Audio** (se approvato): I2S in full-duplex, BCLK e WS condivisi. ESP-SR occupa una parte di un core e della PSRAM (S): si prova in P6 insieme a camera, streaming e inferenza. Se non regge, l'audio va al telefono o al Mac.
- **USB OTG**: debug e HIL durante lo sviluppo. Se arriva il computer di bordo, la porta passa a lui (UVC più CDC) e il debug va sulla CH340 e in OTA.

### 2.6 Scelte dove i due documenti non coincidevano

| Tema | `predisposizioni.md` | `software.md` | Scelta e perché | Allineamento |
|---|---|---|---|---|
| Bus dei sensori | dedicato, I2C0 su 47/3 | da decidere; prova del bus condiviso in S1 | **dedicato su 47/3**. All'avvio esp32-camera scrive agli indirizzi della sua tabella, e un sensore che blocca il bus fermerebbe la camera. Il bus condiviso resta la riserva nel firmware | `software.md` (1, S1, 8) |
| GPIO47 | SDA | un solo uso: riserva RX o I2C | **SDA**. La RX su GPIO14 è decisa (D-012); la riserva sparisce | `software.md` (1); `studio-componenti.md` da aggiornare all'approvazione |
| GPIO38–40 | I2S dell'audio | uno serve al banco per la misura RMT | **tutti e due, in tempi diversi**: misura su GPIO38 in P2, audio da P6 | `software.md` (1, S1, 8); `predisposizioni.md` (4.1) |
| GPIO2 | dati verso l'amplificatore | libero, non per l'I2C | **dati I2S verso l'amplificatore**: è un'uscita, il LED "ON" non la disturba | `software.md` (1) |
| USB OTG | riserva per il LIDAR, rinunciando alla USB | debug e HIL, poi computer di bordo | **USB riservata**: senza USB nativa si perdono l'HIL e il collegamento del computer di bordo. Il LIDAR va su GPIO40 senza microfoni, oppure sul computer di bordo | `predisposizioni.md` (X28, 4.1, domanda 7) |
| microSD | piano A senza, piano B con | non serve: si registra sul Mac | **piano A**, con la conferma dell'utente (domanda 3) | nessuna |
| Ingressi della SSC-32 | per i PG dei regolatori e l'uscita del radar | UART solo a `ctrl` | se servono, **li legge `ctrl` al ritmo del battito**; il radar passa comunque dall'espansore | `predisposizioni.md` (2.7) |
| Posto dell'IMU | tetto del tunnel sotto il vassoio (`Corpo_Base`) | sul vassoio, rigida con la camera | **`Corpo_Base`**: misura il corpo che porta le zampe, e il tetto è più rigido del vassoio in PLA su distanziali (vibrazioni, X23). La calibrazione camera–IMU si rifà dopo ogni smontaggio del vassoio | `software.md` (1, 8); `predisposizioni.md` (2.9) |
| ToF frontale | mensola del vassoio, finestra sotto l'occhio | sede nella visiera, asse vicino alla camera | **mensola e finestra di `predisposizioni.md`**: sullo stesso piano verticale della camera, 11 mm sotto il suo asse | `software.md` (8) |
| Luce di stato | catena LED; il LED della scheda è nascosto | guida di luce dal WS2812 alla visiera | **anello del pulsante (X11) e pixel della catena**; "camera attiva" su un pixel (fessure X21 o anello). La guida di luce solo se la catena non si fa | `software.md` (In breve, 3.3, 8) |
| Vano del computer di bordo | sotto il dorso (z 34,4) restano 9,2 mm sopra le spine della SSC-32 e circa 13,6 sopra l'ESP32; zona contesa da scheda del carapace e amplificatore | 70 × 35 × 15 sopra la SSC-32 | **posto da trovare**: alto 15 sotto il dorso non ci sta. Ripiego: uno zaino esterno sul dorso, come quello del Pi 5 (domanda 6) | `software.md` (In breve, 1, 8); `predisposizioni.md` (2.8) |
| Lettura dei contatti | ADS7830 sullo stesso bus del ToF 8 × 8 | contatti a 100 Hz, meno di 10 ms di ritardo | **limite alla durata delle transazioni** (2.5), misurato in P2 | `predisposizioni.md` (2.2) |
| Massa | +58 / 99 / 189 g | +5 g di stampe; computer di bordo 10–130 g | **un solo bilancio** (3.4) | nessuna |
| 5 V | D24V22F5 per ESP32, LED e audio | secondo regolatore per Radxa o Pi Zero; Pi 5 a parte | **uguale**: il computer di bordo non sta sul D24V22F5 | nessuna |
| Somma fra coxe vicine | — | 56° (proposta, 2.5) | **56°, da approvare**: cambia il limite di 60° di D-050 e D-061. Con ±30° per zampa quel limite non toglie nulla; con 56° restano 3° per zampa, come al ginocchio | `decisioni.md` all'approvazione (10) |

## 3. Bilanci

### 3.1 Corrente a 3,3 V

D24V5F3 da 500 mA, oppure il 3V3 della scheda se la prova in P2 va bene (non cala sotto 3,0 V con ToF e Wi-Fi accesi, nessun riavvio). Il software non aggiunge carichi a 3,3 V.

| Insieme | Tipica (mA) | Picco (mA) | Quota del picco |
|---|---|---|---|
| Alta: IMU, due INA260, ADS7830 con FSR e NTC, ToF frontale, pull-up | ~104 | ~157 | 31 % |
| Alta e media: più INA3221, microfoni, CAP1188, espansore, ToF posteriore | ~127 | ~201 | 40 % |
| Tutto: più ToF del mento, APDS-9960, MLX90640 | ~176 | ~364 | 73 % |

Senza X3 queste correnti passano dal regolatore della scheda, cioè dal 5 V (3.2). La prova di P2 vale solo per le voci alte: si ripete in P6 con le medie (ToF posteriore) e prima delle voci basse (ToF del mento, APDS-9960 con impulsi fino a 100 mA, MLX90640).

### 3.2 Corrente a 5 V

D24V22F5 (B2), 2,5 A.

| Voce | Tipica (mA) | Picco (mA) | Dati |
|---|---|---|---|
| ESP32 con Wi-Fi e camera | ~250 | ~500 | S; si misura in P2, di nuovo con l'inferenza in P6 |
| LED con il tetto del firmware | 50–150 | 600 | S |
| LED spenti, 38–58 pixel (~1 mA ciascuno) | 40–60 | ~60 | S |
| Amplificatore (X17) | pochi | ~200 | S |
| **Alta e media** | | **~1360 (54 %)** | |
| Radar e LIDAR (X26, X28) | ~260 | ~380 | S |
| LED spenti in più (X30, X31), fino a 94 pixel | ~35 | ~35 | S |
| **Tutto** | | **~1780 (71 %)** | |

- Senza X3 il 5 V porta anche i sensori a 3,3 V (3.1): circa 1560 mA (62 %) con alta e media, circa 2140 mA (86 %) con tutto.
- Il PTC dei LED deve tenere il tetto più i pixel spenti: 600 + 38–94 mA, cioè circa 0,7 A.
- Senza protezioni, 58 pixel bianchi chiedono circa 2,1 A: con l'ESP32 si superano i 2,5 A, il 5 V cala, l'ESP32 si riavvia e i LED restano accesi. Per questo pull-down e PTC (o interruttore di carico) fanno parte di X9.
- Il D24V22F5 sta chiuso sotto l'ESP32: in P4 si misura la sua temperatura. Se scalda, un secondo D24V22F5 solo per luci e audio.
- Computer di bordo, fuori dal D24V22F5: Radxa ZERO 3W 2–4 W, Pi Zero 2 W 0,4–1,4 W, con un regolatore 5 V da 3 A proprio; Pi 5 con AI HAT+ 2 5,5–13,5 W (5 V 5 A), con alimentazione propria (S).

### 3.3 Ramo logica: F2 e interruttore

Caso peggiore a 6,6 V: sotto 3,5 V per cella il firmware spegne il rail servo, ma la logica resta accesa fino a 3,3 V per cella (`software.md` 2.6); i cali brevi sotto carico il fusibile non li sente. Rendimento 0,88 sul 5 V e 0,85 sul 3,3 V, VL della SSC-32 circa 0,4 W (S). Due varianti: sensori dal D24V5F3 (X3), oppure dal 3V3 della scheda, cioè dal 5 V.

| Caso | Potenza con X3 | Corrente con X3 | Corrente senza X3 | F2 da 2 A (con / senza X3) | F2 da 3 A (con / senza X3) |
|---|---|---|---|---|---|
| Oggi: ESP32 e VL | ~3,2 W | ~0,49 A | uguale | 25 % | |
| Alta e media | ~8,9 W | ~1,35 A | ~1,40 A | 67 / 70 % | |
| Tutto | ~11,9 W | ~1,81 A | ~1,91 A | 90 / 95 % | 60 / 64 % |
| Alta e media più Radxa (4 W) | ~13,4 W | ~2,04 A | ~2,09 A | oltre | 68 / 70 % |
| Tutto più Radxa | ~16,5 W | ~2,50 A | ~2,60 A | oltre | 83 / 87 % |

- A 7,0 V le correnti sono il 6 % più basse (1,27 A con alta e media e X3). Varrebbero solo se sotto 3,5 V per cella il firmware spegnesse anche LED, audio e computer di bordo, che `software.md` 2.6 oggi non prevede.
- Con le voci basse o con il computer di bordo F2 passa a 3 A: voce B6 da riapprovare. Il BOM dice "ramo logica, meno di 1 A": vale solo senza sensori.
- Interruttore Pololu 2813: circa 16 A continui, 6 A a 55 °C nella tabella del produttore (V, pagina riletta oggi). Basta anche con F2 da 3 A.
- Rail servo: le spie (X13) prendono 4 mA per lato. Lo shunt da 2 mΩ dell'INA260 a 13 A fa cadere 26 mV (calcolo).

### 3.4 Massa ed effetto sulla coppia

`calc/statica_tripode.py` al punto di progetto 100/45, tripode, rail a 6 V, rifatto oggi con le masse della tabella. Il calcolo mette tutta la massa sul corpo; sulle zampe ne vanno 18–39 g, che pesano anche in volo (trascurabile). Circa 57 g valgono un punto di femore.

| Insieme | Corpo | Zampe | Totale | Femore | Ginocchio |
|---|---|---|---|---|---|
| Oggi | — | — | 2945 g | 51,4 % | 47,1 % |
| Stampe in più del software (vano, dettagli) | +5 g | — | 2950 g | 51,5 % | 47,2 % |
| Alta, più le stampe | +45 g | +18 g | 3008 g | 52,5 % | 48,1 % |
| Alta e media, più le stampe | +86 g | +18 g | 3049 g | 53,2 % | 48,8 % |
| Alta e media più Radxa (~40 g, S) | +126 g | +18 g | 3089 g | 53,9 % | 49,4 % |
| Tutto, più le stampe | +155 g | +39 g | 3139 g | 54,8 % | 50,2 % |
| Tutto più Radxa, oppure alta e media più zaino Pi 5 (~130 g) | +195 / +216 g | +39 / +18 g | 3179 g | 55,5 % | 50,9 % |

- La guardia proposta avvisa al 55 % dello stallo, tollera il 60 % per un tempo limitato e rifiuta al 70 % (`software.md` 2.5). Con tutto più un computer di bordo il tripode a 100/45 supera già l'avviso.
- Le altre andature crescono nella stessa proporzione (la coppia statica va con il peso): a coppie a 100/45 dal 41 % al 42 % (alta e media) e al 44 % (3179 g). Il ginocchio in tripode a 130/25 passa dal 58 % al 60 % e al 63 %. Negli assetti alti e bassi si cammina a coppie o a onda.
- Al punto di progetto il piede più carico porta 11,4–12,3 N (2945–3179 g): il 57–62 % dei 20 N dell'FSR. Gli FSR danno il contatto e un carico relativo, non una misura.
- Conclusione: alta e media costano meno di 2 punti e si possono fare. Voci basse e computer di bordo non vanno insieme senza alleggerire: la prima leva è il guscio della tibia a 1,2 mm (circa −20 g, D-063).

## 4. Roadmap

Ogni fase lascia la repo in uno stato da cui ripartire. "Si compra" vuol dire: da approvare voce per voce, salvo dove è scritto "approvato".

**P0 — Decisioni, CAD e software senza hardware**
- Si fa: risposte alle domande 1–10 (sezione 7). CAD della sezione 5, prima della prima stampa di tibie, piedini e carapace, compresi i posti da trovare. In parallelo S0: `robot.yaml`, `esporta_robot.py` in sola lettura, generatori, nucleo C++, vettori di prova dal CAD, gemello nel browser, modello MuJoCo, CI. Prepara la chiusura delle fasi 4–6 di `CLAUDE.md`, che si chiudono dopo P1 con i valori dei provini; nel BOM finale entrano anche gli inserti e le viti dei sensori.
- Si compra: niente. Il software libero si installa sul Mac solo con il permesso (domanda 9).
- Si verifica: zampa con `scansione` (54 pose) e `interferenze`, suola a 110; assieme senza interferenze, `sfilamento`, `campo`, `carapace_zampe`, sentinella dei volumi; T-plug e spinotto di bilanciamento raggiungibili dalla porta di servizio. S0: nucleo uguale a `calc/` entro 0,01° e al CAD entro 0,05 mm; pose verificate accettate dalla guardia, casi d'urto rifiutati; 20 s di tripode in SIL senza cadute.

**P1 — Provini**
- Si fa: provino della culla e del giunto, provino degli inserti (già in programma). Provino del piedino con un FSR (X5). Provino di luce (X10) con tre pixel comandati dall'ESP32 su GPIO48. Poi i valori dei provini tornano nel CAD e si chiudono le fasi 4–6 di `CLAUDE.md`.
- Prima: le domande 1–4 del BOM (sezione 7).
- Si compra: ordine 1 del BOM v2.0 (voci approvate; una sola squadretta di prova prima delle altre 19 è la domanda 4 del BOM). Filamento per i provini: dalla v1 se c'è (domanda 3 del BOM), altrimenti E1, E2 ed E3 già qui, ed E2b se approvata (D-065). Da approvare: 2 FSR 400 Short e un tratto di striscia LED con buffer e resistenze (X9).
- Si verifica: forzamenti di cuscinetti e perni, fori degli inserti, gioco della coxa. FSR: presa del cappuccio, piega della coda, resistenza con pesi noti al multimetro, forza persa per attrito. Luce: spessore di bianco (0,6–0,8) e camere nere, da riportare nel CAD del carapace.

**P2 — Banco dell'elettronica (S1)**
- Si fa: S1 di `software.md` (passi di banco B0–B2 di 6.7): versione dell'IDF, OV3660 con il DVDD a 1,2 V, SSC-32 (baud, `VER`, `Q`, `QP`, `STOP`, `P0`, ingressi `VA`, modo binario, 230400), jitter misurato con l'RMT su GPIO38, un MG996R alimentato senza impulsi, corrente a 5 V di ESP32 e camera con il Wi-Fi, heap interno libero. Per i sensori: bus dedicato su GPIO47/3 (GPIO3 all'avvio), IMU, ADS7830 e ToF frontale; 3V3 della scheda con ToF e Wi-Fi accesi (decide X3); tempo di salita del bus e durata di una lettura del ToF; GPIO41 flottante e 2813.
- Si compra: ordine 2 del BOM v2.0 (alimentazione e controllo, approvato); ESP32-S3-CAM e OV3660 se mancano (domanda 1 del BOM, voci A2 e A3). Da approvare: X1, X4, X6, X8; X3 solo se la prova del 3V3 fallisce; adattatore USB-seriale (facoltativo); fusibili da 3 e 5 A per il banco.
- Si verifica: formato e baud della SSC-32 scelti; fps della camera in JPEG; 3V3 sopra 3,0 V senza riavvii; bus a 400 kHz con salita entro 300 ns (senza oscilloscopio: errori del bus contati, domanda 13), altrimenti 100 kHz con il carico ridotto di 2.5; contatti letti entro 10 ms con il ToF attivo.

**P3 — Corpo e una zampa (S2)**
- Si fa: stampa del corpo e di una zampa con le predisposizioni; dime e cavalletto. Catena di potenza e un lato da 9 servo (passi B3–B5 di `software.md` 6.7; B0–B2 sono in P2). Spie dei rail (X13). Firmware di base S2: macchina a stati, accensione, misura di batteria, watchdog, console, prima app, telemetria, taratura con le dime, OTA con ritorno, HIL sul Mac.
- Si compra: ordine 3 del BOM v2.0 (squadrette, cuscinetti e perni restanti; approvato); il resto dei filamenti: E1, E2, E3 (scelti dall'utente); E2b da approvare (D-065). Da approvare: X13.
- Si verifica: accensione senza scatti; rail spento in ogni guasto provato (SSC-32 staccata, firmware bloccato, batteria simulata bassa); taratura ripetibile entro 1°; escursioni della zampa sul cavalletto contro la tabella del ginocchio minimo; rail a 6 V con power-good; spie accese solo con il rail.

**P4 — Robot completo in guida manuale (S3)**
- Si fa: sei zampe; carapace a due colori con le predisposizioni; scheda e cavo del carapace (X2); catena LED con le protezioni (X9, X11, X12; X21 e X22 se approvate); INA260 sulle slitte (X7); NTC sui regolatori (X14). S3: in piedi, seduto, a coppie e a tripode a 100/45 dal telefono, registrazione MCAP, scatola nera, perdita del collegamento.
- Si compra: da approvare X2, X7, X9 (il resto), X14; un gamepad solo se manca (domanda 16).
- Si verifica: jitter del ciclo sotto 1 ms al 99,9° percentile con il video acceso; uomo morto a 300 ms e seduta a 30 s; latenza e consumo per assetto. Temperatura sotto il carapace (regolatori, D24V22F5; il PLA rammollisce a 55–60 °C): decide PLA o PETG (D-065). LED spenti all'accensione e durante un reset; 5 V stabile con i LED al tetto.

**P5 — Sensori e andature adattive (S4)**
- Si fa: FSR nei sei piedi (X5); IMU per livellamento, caduta e imbardata, poi vibrazioni e urti dalla sua FIFO (X23, solo firmware); ToF frontale per l'arresto e il bordo del tavolo; correnti dei rail per lo stallo. Ricerca dell'appoggio, posa sicura alla soglia dell'assetto, scelta dell'andatura dal budget di coppia, assetti da 130/25 a 70/70. Identificazione dei servo e taratura di MuJoCo sui registri.
- Si compra: il resto di X5.
- Si verifica: tappetini, libri e pendenze senza cadute; contatto letto su ogni piede; giunto bloccato visto dalla corrente; robot e simulatore con tracce di IMU e corrente vicine sulle stesse sequenze.

**P6 — Visione a bordo (S5) e voci di media priorità**
- Si fa: S5 (streaming, persone e volti con ESP-DL, AprilTag, scatto a metà appoggio, "seguimi", "sono bloccato", arresto con il ToF); luce ambiente dalla camera e dal ToF (X24, solo firmware). Audio (X16, X17), tocco (X18), ToF posteriore (X19), espansore (X20). INA3221 (X15) solo se nel CAD si è trovato il posto.
- Si compra: da approvare X16–X20; X15 solo con il posto.
- Si verifica: fps reali con passo, Wi-Fi e camera insieme (attesi 3–5) senza peggiorare il jitter di P4; audio in full-duplex insieme a camera e streaming; ToF posteriore e altoparlante che non ostacolano il T-plug. Senza X3: di nuovo la prova del 3V3 della scheda, con le voci medie accese.

**P7 — Cervello esterno (S6)**
- Si fa: ponte Python, Rerun, protocollo v1 congelato; percezione sul Mac (YOLO26, profondità, ToF); calibrazione fisheye e camera–IMU; server MCP con Claude Code e l'operatore presente; ROS 2 se voluto (domanda 21).
- Si compra: API di un LLM, a consumo (domanda 20).
- Si verifica: latenze e fps della percezione; ogni chiamata dell'LLM registrata e dentro i limiti; STOP sempre efficace.

**P8 — Apprendimento, livello 1 (S7)**
- Si fa: politica PMTG addestrata con ARS sul Mac, con la randomizzazione; poi sul robot in ombra, limitata, piena.
- Si compra: niente.
- Si verifica: contro la sola andatura classica, sullo stesso percorso: cadute, velocità, energia dalle correnti (X7).

**P9 — Autonomia in casa (S8) e decisione sul computer di bordo**
- Si fa: Kalman con odometria delle zampe, IMU e AprilTag; mappa d'ingombro dal ToF e dalla profondità; Nav2 con MPPI; agente per missioni brevi. Decisione sul computer di bordo con il criterio di `software.md` 5.4 e il bilancio di 3.4.
- Si compra: marcatori su carta. Se il criterio lo chiede: Radxa ZERO 3W, regolatore 5 V 3 A, F2 da 3 A (da approvare).
- Si verifica: missioni ripetute con il tasso di riuscita e gli interventi dell'operatore contati. Con il computer: UVC più CDC, NPU misurata, femore sotto la soglia d'avviso.

**P10 — Apprendimento, livelli 2 e 3 (S9) e voci di bassa priorità**
- Si fa: politica maestro-allievo su GPU in cloud, poi con ToF e profondità. Le voci basse scelte dall'utente (X25–X33; X24 solo se serve il VEML7700), ognuna con il suo bilancio di massa e corrente, i pull-up staccati (2.4) e, senza X3, la prova del 3V3 della scheda con i loro picchi.
- Si compra: GPU a consumo (domanda 23); le voci basse approvate.
- Si verifica: prima in SIL, poi HIL, poi sul robot in ombra; confronto con il livello 1 su gradini bassi e ostacoli; femore entro la soglia con la massa nuova.

## 5. Da predisporre subito nel CAD

**Stato al 10 ottobre 2026** (versione 2.1.0, D-066):
- fatte e verificate nel modello:
  - punta dello stinco, piedino, tasca e gola dell'FSR;
  - luci nelle tibie con diffusore, anello del pulsante con camera nera, sedi dei lobi e ganci;
  - 2813, IMU, ADC, prese dei piedi, spie dei rail;
  - ToF frontale con finestra e tappo, ToF posteriore, INA260 su supporti separati;
  - microfoni, altoparlante, amplificatore e scheda del carapace;
  - zaino;
  - punti con nome, dime e cavalletto.
- Restano "posto da trovare": INA3221 (X15), sede del CAP1188 (X18) e linee di luce della fascia (X22). Le fessure dell'occhio (X21) sono fuori finché l'utente non le chiede.
- Le righe qui sotto sono la specifica di partenza: dove differiscono, vale D-066.

Un solo elenco, dalle due ricerche. Parametri nuovi con i prefissi `sen_` (sensori) e `luc_` (luci). Dopo ogni gruppo le verifiche solite: interferenze, sentinella dei volumi, timeline.

Stato: **sicuro** = quote e posto controllati sul modello nella revisione, resta da modellare e verificare; **da verificare** = posto indicato, con un controllo aperto; **posto da trovare** = il volume non è dimostrato; **da decidere** = dipende da una domanda della sezione 7.

| Pezzo (componente Fusion) | Cosa | Quote | Voce | Stato |
|---|---|---|---|---|
| `Tibia` (`fai_tibia`, non `_stinco`) | punta dello stinco piana, spigolo +X raccordato R 1; parametro nuovo per la fine dello stinco, usato solo dalla `Tibia` (non `tib_piede_sp`, che muove l'arco) | fine a ~107,6 (oggi 108,4); `tib_x_piu_basso` da 4 a ~6, parte piana ~8,4 per la testa dell'FSR Ø7,6; `tib_arco_R` da 262 a ~341; lato −X invariato (0,03 mm dalla coxa) | X5 | sicuro; cambiano inserto e bossolo della vite del guscio, si rifanno `scansione` e `interferenze` |
| `Tibia` | tasca per linguette e saldature dell'FSR, faccia +X dentro il piedino | 6 × 9 × 1,2, Z −94,5…−110 | X5 | sicuro |
| `Tibia` | gola per i fili, faccia +X di stinco e zoccolo | 2 × 2 a Y ≈ +5, dal piedino al fondo della culla (Z ≈ −33), non oltre. Sulla culla i fili passano nell'aria sotto il guscio (3,1–5,7) con un fermo, o in una gola profonda al massimo 0,8 | X5 | sicuro |
| `Piedino` | nasce da uno stinco con la punta nuova ma lungo 108,4; pistoncino; tacca; esterno raccordato a parte | suola a 110; cavità 0,8 (FSR 0,3 + pistoncino 0,5); pistoncino Ø4,5 × 0,5; tacca 2 × 2 sul bordo alto lato +X | X5 | sicuro; raggio esterno da scegliere |
| `Cover_Tibia` | niente; tacca 3 × 2 se il bordo schiaccia i fili. Luci nelle tibie: finestra chiusa da 0,6 di bianco | finestra 7 × 48 | X5; X31 | sicuro; X31 da decidere (cambia il guscio di D-061, domanda 2) |
| `Coxa`, `Femore_A`, `Femore_B`, `Tibia` | facce di riferimento libere e tacche per le dime | con le dime | dime | posto da trovare |
| `zampa.py`, `assieme.py` | punti con nome: punta del piede, IMU, assi dei giunti | — | S0 | sicuro (non si stampa) |
| `Corpo_Visiera` | finestra del ToF sotto l'occhio: tronco di piramide sul campo 60° × 60° inclinato di 20° in basso, più 0,8; tappo nero finché il sensore manca | bocca ~10 × 9 sull'asse, z ≈ 3,5…13,5; cima a z ≤ 13,5, ponte ≥ 1 dall'occhio (z 14,56) | X8 | sicuro |
| `Corpo_Visiera` | fessure di luce ai lati dell'occhio, camere nere chiuse verso l'occhio | larghe 1,5 a 60°, da (\|y\| 13; z 16) a (\|y\| 18; z 25); camere x 96,5…100,4, pareti 1,2, fori Ø2 | X21 | sicuro; da decidere (domanda 2) |
| `Corpo_Vassoio` | mensola della camera come plancia del ToF; testa della camera bloccata nella torretta, posizione e orientamento come parametri | mensola x 92,5…98,5, \|y\| ≤ 6, z 1…18,25; sede a 20° per 13 × 18 × 3, lato 13 lungo y, centro del sensore a z ≤ ~11,5; perni Ø1,9 o inserti M2 (C); fessura fino a z ≈ −0,5; canale per 4 fili lungo la torretta | X8; calibrazione | da verificare: posizione del sensore sulla scheda (C, disegno Pololu). La scheda inclinata arriva a z ≈ 16,4 e circa 6 più avanti del piede: prova d'interferenza con la bugna dell'occhio (x ≥ 99,4, z ≥ 15, \|y\| ≤ 11) e con la testa della camera. Fermo della testa da disegnare |
| `Corpo_Vassoio` | asola per il bus verso il vano sotto il vassoio | 6 × 3 a x ≈ 50, y 13…16 | X1 | sicuro |
| `Corpo_Base` | posto della 2813, oggi aperto: decide le due righe sotto | 20,3 × 25,4 × 4,1 | B3 | posto da trovare |
| `Corpo_Base` | IMU sul tetto del tunnel sotto il vassoio, freccia dell'asse X stampata | due bugne Ø5,5 alte 2 (fino a z −7,4), inserti M2 (D5), 1 mm di tetto sopra il pacco; gioco 1 mm attorno a 13 × 23; interasse dal disegno Pololu (C) | X4 | sicuro se la 2813 va altrove |
| `Corpo_Base` | ADS7830 e striscia dei partitori, accanto all'IMU | due bugne con inserti M2 (fori C) | X6 | posto da trovare se la 2813 va sotto il vassoio |
| `Corpo_Base` | sei prese a 3 poli dei piedi, raggiungibili a carapace tolto | — | X5 | posto da trovare |
| `Corpo_Base` | passaggi: 4 fili del bus fra SSC-32 (x 22) e vassoio (x 26) con due clip sul tetto; cavi dei piedi dalle file della SSC-32 alle prese | — | X1, X5 | sicuro le clip; percorsi da tracciare |
| `Corpo_Base` | linguetta delle spie dei rail in coda, sotto il cicalino | due fori Ø3,1 rivolti indietro a \|y\| ≈ 10 | X13 | posto da trovare con F1, T-plug e cavi della batteria |
| `Corpo_Base` | sede dell'INA3221 | 38,6 × 22,9 × 10,5; fuori dalla pianta dei Wago (x −46…−16, \|y\| 27,5–35,8) e sopra il raggio dei cavi | X15 | posto da trovare (sopra i Wago non ci sta) |
| `Corpo_Slitta_Regolatore` | prolungata in alto con due inserti M2 per l'INA260 sulla faccia verso il tunnel, morsettiera in alto | fino a z ≈ 32, x 14…37; ~2 g per lato | X7 | da verificare: smusso del carapace, gonne, cavi anteriori, feritoie a \|y\| 30. Ripiego: scheda in linea nel 16 AWG |
| `Corpo_Carapace`, `Corpo_Fascia` | anello di stato del pulsante | foro anulare Ø18–22 attorno al pulsante (x −40); bianco 0,6–0,8 (dal provino X10); camera nera Ø32 × 6 (z 28,4…34,4) con il fondo e due sedi da 16,7 mm (due pixel ciascuna) a \|y\| 6,5–11,9 | X11 | fatto (D-067); X22 non si fa; dado del pulsante C |
| `Corpo_Carapace` | luce dei lobi | sede 5 × 22 × 0,6 con due ganci per lobo, sulla direzione neutra della zampa, per due pixel di striscia 2020 a 120 LED/m (D-068); cavo lungo i fianchi nei ganci (cablaggio.md) | X12 | fatto |
| `Corpo_Carapace` | ganci passacavo della striscia | alti 3 ogni 40 mm, fuori dalla battuta dello sportellino (x −21…29, \|y\| ≤ 17) e dai pozzetti (x 40 e −56, \|y\| 17,8–27,2) | X9 | sicuro |
| `Corpo_Carapace`, `Corpo_Fascia` | linee di luce lungo la fascia | gola a \|y\| 17–18,5 con 0,6–0,8 di bianco; canali neri a U alti 5, interno ≥ 5,4 centrato su \|y\| 17,75; tre tratti per lato (x −91…−61, −51…35, 45…96); passaggio nelle paratie (x 81…82,6) | X22 | da ridisegnare: con pareti da 0,8 il canale occupa \|y\| 14,25–21,25, z 29,4…34,4, e urta tre cose. (1) La battuta dello sportellino (x −21…29). (2) Il collare del cicalino (\|y\| 20,2–21,4, z 25,4…34,4) per tutto x −87…−62, e il cicalino stesso se è alto più di 12 (D-059 gli lascia 14, fino a z 31,4). (3) La camera nera di X11 fra x ≈ −47 e −33. Tratto posteriore da togliere o spostare, tratto centrale spezzato |
| `Corpo_Carapace` | scheda del carapace con la spina che si sfila dall'ottagono | testata con spina ~9 + 9, 470 µF Ø6,3–8, TCA9534; libero il passaggio dell'USB-C (\|y\| ≤ 13, z 14…24) | X2, X20 | posto da trovare: prima da guardare x 29…50, \|y\| ≤ 16, sopra l'ESP32, prima dell'antenna (da x 55,6) |
| `Corpo_Carapace`, `Corpo_Fascia` | fori dei microfoni con anello per la guarnizione, sedi delle schede a faccia in giù | due fori Ø1 a x ≈ 89; a \|y\| 11 le schede arrivano a 17,35, dentro i canali di X22 | X16 | posto da trovare |
| `Corpo_Carapace` | sede dell'amplificatore | 19,4 × 17,8 × 3 | X17 | posto da trovare |
| `Corpo_Carapace` | guance di coda: ToF posteriore sulla guancia lontana dallo spinotto, inclinato di 35° in basso; altoparlante sull'altra | \|y\| 25,4; il ToF sporge ~13 nella porta larga 50,8 | X19, X17 | da verificare: T-plug e spinotto si afferrano con i due montati, altrimenti sopra il piano del T-plug |
| `Corpo_Carapace` | zone piane per gli elettrodi, sede del CAP1188 | 15 × 25 senza ganci né nervature (viso x 96…101, coda x −91…−83, lobi); modulo 42 × 18 × 3; niente sopra l'antenna (x 55,6…81,1) | X18 | sicuro le zone; sede del modulo da collocare |
| `Corpo_Carapace` | vano del computer di bordo con feritoie, passaggio per un USB-C a 90° | 70 × 35 × 15, bugne M2,5 a 58 × 23; sotto il dorso restano 9,2 sopra le spine della SSC-32 e circa 13,6 sopra l'ESP32 | computer di bordo | posto da trovare; ripiego zaino sul dorso (domanda 6) |
| `Corpo_Carapace`, `Corpo_Fascia` | voci basse, solo se scelte: finestra dei gesti 5 × 4 a x ≈ 40 (X27); sede del radar sotto il dorso, niente viti sopra le antenne (X26); finestra della termocamera (X29); sella del LIDAR fino alle viti a x 40 (X28) | — | X26–X29 | da decidere (domanda 5) |
| visiera o fascia | guida di luce dal WS2812 della scheda | — | stato | solo se la catena LED non si fa |
| parti nuove, non sul robot | dime di taratura generate dai parametri: coxa 0° e +30°, femore 0° e +45°, ginocchio 90° e 135° | — | taratura | da disegnare |
| parti nuove, non sul robot | cavalletto da banco: corpo appoggiato sotto la chiglia, zampe libere su tutta l'escursione; leva di prova facoltativa | — | banco | da disegnare |
| `rif_componenti.py` → `ingombri` | ingombri nuovi in libreria | IMU 13 × 23 × 3; ToF 8 × 8 13 × 18 × 3; ToF semplice 13 × 18 × 2; INA260 22,9 × 22,8 × 2,7 più morsettiera; INA3221 38,6 × 22,9 × 10,5; ADS7830 30,5 × 17,7 × 4,7; D24V5F3 13 × 10 × 3; scheda del carapace con spina IDC; MAX98357A 19,4 × 17,8 × 3; altoparlante 15 × 11 × 3; microfono 16,7 × 12,7 × 1,8; FSR Ø7,6 × 0,3 con coda da 16 | — | sicuro |
| `cad/script/esporta_robot.py` (nuovo) | esportazione in sola lettura per S0 | ogni chiamata sotto i 40 s | S0 | sicuro |

`Corpo_Chiglia`, `Coxa_Ponte` e i femori (salvo le facce per le dime) non cambiano: i fili dei piedi seguono le fascette esistenti.

## 6. Candidati per il BOM

Tutti da approvare. Costi indicativi (S), da ricontrollare all'ordine. Fase = fase del piano in cui servono. Corrente a 3,3 V salvo dove è scritto.

| Voce | Uso | Fase | Massa | Corrente | Costo |
|---|---|---|---|---|---|
| X5 FSR 400 Short × 7, doppino 28 AWG, spine JR dalle C5 avanzate | contatto e carico relativo dei piedi | P1 (2 pezzi), P5 | 18 g (3 a zampa) | ~2 mA | ~40 € |
| X9 catena LED: striscia WS2812B-2020, buffer SN74AHCT1G125, 330 Ω, pull-down 10 kΩ, PTC sul 5 V | base di tutte le luci | P1 (provino), P4 | ~1 g ogni 10 cm | 5 V: tetto 600 mA | ~15 € |
| X1 cavi Qwiic e cavo Adafruit 4209 | bus dei sensori e presa di espansione | P2 | ~5 g | ~2 mA | ~5 € |
| X3 Pololu D24V5F3 | 3,3 V dei sensori, solo se il 3V3 della scheda non regge | P2 | <1 g | 0,2 mA a vuoto | ~9 € |
| X4 Pololu #2798 (LSM6DSO) | assetto, caduta, imbardata, urti, vibrazioni (X23) | P2 | ~2 g | 1 mA | ~20 € |
| X6 Adafruit ADS7830 (#5836) e partitori | sei piedi e due NTC | P2 | ~3 g | <1 mA | ~6 € |
| X8 Pololu #3418 (VL53L7CX) | ostacoli, bordo del tavolo, gradini | P2 | ~3 g | 100, picco 150 mA | ~22 € |
| X13 2 LED ambra Ø3, 2 × 1 kΩ | spia dei rail senza firmware | P3 | <1 g | 6 V: 4 mA per rail | <1 € |
| X2 testata 2 × 8, cavo piatto 16 vie con IDC, 470 µF 10 V | un solo connettore per il carapace | P4 | ~8 g | — | ~6 € |
| X7 2 × Adafruit INA260 | corrente dei rail, giunto bloccato, stima della carica | P4 | ~8 g | 0,6 mA | ~25 € |
| X14 3 NTC TDK B57861S0103F040 e 10 kΩ 1 % | temperatura dei regolatori; decide PLA o PETG del carapace | P4 | ~1 g | 0,34 mA | ~3 € |
| X15 2 × Adafruit INA3221 | corrente di ogni femore | P6, solo con il posto | ~16 g | 0,7 mA | ~24 € |
| X16 2 × Adafruit 3421 (SPH0645, I2S) | comandi a voce, direzione dei suoni | P6 | ~3 g | ~1 mA | ~14 € |
| X17 Adafruit 3006 (MAX98357A) e altoparlante CUI CMS-15113-078SP | voce e avvisi | P6 | ~4 g | 5 V: fino a ~200 mA | ~10 € |
| X18 Adafruit 1602 (CAP1188) e nastro di rame | tocco sul carapace | P6 | ~3,5 g | ~1 mA | ~13 € |
| X19 Pololu #3415 (VL53L1X) | retromarcia e rotazione | P6 | ~3,5 g | 20, picco 40 mA | ~22 € |
| X20 TCA9534 su adattatore | XSHUT dei ToF, uscita del radar | P6 | ~2 g | <1 mA | ~3–6 € |
| X24 Vishay VEML7700 (riserva) | luce ambiente, solo se camera e ToF non bastano (in P6 è solo firmware) | P10 | — | — | da cercare |
| X25 Pololu #3692 (VL53L4CD) | luce sotto il muso, robot sollevato | P10 | ~2,5 g | 25, picco 40 mA | ~15 € |
| X26 Hi-Link HLK-LD2410C | presenza a robot fermo | P10 | ~2 g | 5 V: 79 mA | ~5 € |
| X27 Adafruit 3595 (APDS-9960) | gesti sopra la schiena | P10 | ~2 g | 0,8 mA, impulsi fino a 100 | ~8 € |
| X28 LIDAR LD06 o LD19 con sella | mappa della stanza (via Mac) | P10 | ~50 g | 5 V: 180, 300 all'avvio | ~70–100 € |
| X29 Adafruit 4469 (MLX90640 110°) | persone e animali al buio | P10 | ~3 g | <23 mA | ~75 € |
| X30, X31 pixel in più (fari, tibie) e cavo 3 × 30 AWG | fari bassi; luce nelle tibie | P10 | 2–4 g; 12 g | 5 V: fino a 216; 100–150 | 0 €; ~5 € |
| X32 filo sul cursore e 2–3 ADS7830 | angolo vero dei giunti, prima su un servo di scorta | P10 | ~0,5 g per servo | trascurabile | ~12–18 € |
| X33 Adafruit 5690 (seesaw) | solo se mancano ingressi | P10 | 2–3 g | pochi mA | ~5–7 € |
| Adattatore USB-seriale 3,3 V (CH340 o CP2102) | ascoltare la linea ESP32–SSC-32 | P2, facoltativo | non a bordo | — | ~5 € |
| Fusibili a lama da 3 e 5 A | banco, un servo alla volta | P2 | — | — | pochi euro |
| Gamepad BLE (Xbox con firmware 5 o successivo) | guida senza telefono | P4, solo se manca | — | — | — |
| F2 da 3 A (voce B6 da riapprovare) | ramo logica con le voci basse o il computer di bordo | P9–P10 | — | — | pochi euro |
| Regolatore 5 V 3 A | computer di bordo Radxa o Pi Zero | P9 | — | — | da cercare |
| Radxa ZERO 3W 4 GB | computer di bordo, solo con il criterio di `software.md` 5.4 | P9 | ~40 g | 2–4 W | da cercare |
| API di un LLM | agente | P7 | — | — | a consumo |
| GPU in cloud | RL livelli 2 e 3 | P10 | — | — | a consumo (Colab per le prove) |
| Marcatori AprilTag | localizzazione | P9 | — | — | carta |
| Software libero (ESP-IDF e componenti, MuJoCo, pytest, ruff, Rerun, mcap, three.js, Vite, Node.js, OpenCV) | S0 e oltre | P0 | — | — | 0 € (installazione da approvare) |

Somme indicative (S): voci alte circa 150 €, medie circa 90 €, basse circa 200–230 €. Prezzi e link letti il 10 ottobre 2026 nel BOM, sezione X (D-068): con le spedizioni alte circa 177 €, medie circa 140 €, basse circa 321 €. Dime e cavalletto si stampano dalle bobine già scelte.

## 7. Decisioni che servono dall'utente

In ordine di urgenza. Fra parentesi la fase che bloccano e la domanda dei documenti di dettaglio da cui vengono.

Bloccano P0 (CAD prima della prima stampa di tibie, piedini e carapace):
1. Approvi le priorità e le predisposizioni nel CAD? Cambiano tibia, piedino, visiera, carapace, vassoio, base e slitte; in più dime, cavalletto e punti di riferimento. Sul robot circa 10 g di stampa (S: 5 per vano e dettagli del software, 4 per le slitte di X7, il resto bugne di IMU e ADS7830; le luci a parte, domanda 2), nessun acquisto. (P0; sensori 2, software 11)
2. Luci: quali vuoi fra anello del pulsante, lobi, fessure dell'occhio, linee della fascia e luci nelle tibie? Le luci nelle tibie chiuderebbero con 0,6 di bianco la finestra lunga del guscio approvato in D-061. Che colori? Va bene il tetto di 600 mA con pull-down e PTC? La spia di camera attiva sarebbe un pixel della catena. (P0; sensori 5, software 16)
3. Rinunci alla microSD (piano A, consigliato)? Se no, niente microfoni né altoparlante I2S. (P0; sensori 1)
4. Audio: va bene l'altoparlante in coda, con il suono dalla porta di servizio? I comandi vocali offline sono solo in inglese: vanno bene, o l'audio va al telefono o al Mac? (P0; sensori 3 e 4)
5. Ti interessano il LIDAR sulla schiena (circa 50 g e 80 €; toglie i microfoni, la sella coprirebbe i loro fori) e la termocamera (circa 75 €)? (P0; sensori 7)
6. Computer di bordo: cerco un vano dentro il carapace, sapendo che sotto il dorso restano 9,2 mm sopra la SSC-32 e circa 13,6 sopra l'ESP32, o basta prevedere uno zaino esterno sul dorso? (P0; nuova, dal confronto)

Bloccano S0 (in parallelo al CAD):

7. Approvi l'architettura a tre livelli: ESP32 autonomo, Mac facoltativo, computer di bordo solo predisposto? (software 1)
8. Firmware in ESP-IDF e C++, senza Arduino: va bene? (software 2)
9. Posso installare sul Mac il software libero della sezione 6? (software 3)
10. La repo è pubblica: va bene pubblicare firmware e registrazioni, con le credenziali fuori, o la rendiamo privata? (software 4)

Bloccano P1 e P2 (provini e banco):

Prima di queste, le domande 1–4 del BOM, ancora aperte (`CLAUDE.md`, prossimi passi): 1, ESP32-S3-CAM e OV3660 li hai già? (servono dal provino di luce in P1); 2, quanti MG996R hai, e di scorta?; 3, filamento, inserti, viteria o prolunghe dalla v1? (servono ai provini); 4, una squadretta di prova prima delle altre 19? (ordine 1).

11. Approvi i primi acquisti? Per i provini: 2 FSR e un tratto di striscia LED. Per il banco: IMU, ADS7830, ToF frontale e cavi Qwiic. (P1, P2; nuova)
12. Al banco posso cambiare baud e registri della SSC-32? Sono scritture in EEPROM, reversibili con il pulsante BAUD. La scheda si studia dalle immagini dell'inserzione e il retro si guarda all'arrivo (D-045): allora, se puoi, una foto dal lato delle prese (ingressi A–D, uscite). (P2; sensori 6, software 12)
13. Hai un oscilloscopio? Serve per il tempo di salita del bus; senza, si prova a 400 kHz contando gli errori, e a 100 kHz il robot legge meno (2.5). (P2; nuova)
14. Rimando alla domanda 2 del BOM (quanti MG996R hai): uno di scorta servirebbe al banco per l'identificazione e per la prova del potenziometro (X32), e non tornerebbe sul robot. Il video della leva è facoltativo. (P2; sensori 8, software 13)

Servono in P3 e P4:

15. Confermi che non servono firma degli aggiornamenti e cifratura della flash? Sono irreversibili sull'ESP32. (P3; software 15)
16. Il telefono è un iPhone o un Android? Hai un gamepad Bluetooth, e quale? Sull'S3 vanno solo i BLE. (P3, P4; software 7 e 8)
17. L'app la vuoi in italiano? (P3; software 17)
18. Il robot userà solo il Wi-Fi di casa o anche altre reti, per esempio l'hotspot del telefono? (P4; software 9)
19. Conta di più la robustezza sul terreno irregolare o la velocità su piano? Il tripode arriva a circa 105–115 mm/s con il limite proposto di 250°/s per giunto. (P4; software 14)

Servono più avanti:

20. Per l'LLM va bene un servizio cloud (Claude), a consumo e con le foto della casa inviate al fornitore, o solo modelli locali? (P7; software 6)
21. ROS 2 è un obiettivo in sé o basta il ponte? (P7; software 10)
22. Riconoscimento dei volti dei familiari e marcatori AprilTag su muri o mobili: li vuoi? (P6, P9; software 16)
23. Hai un PC con una GPU NVIDIA? Ti interessa una macchina Linux sempre accesa (acquisto da approvare)? (P10; software 5)

## 8. Rischi principali

| Rischio | Effetto | Contromisura | Quando |
|---|---|---|---|
| Posti non dimostrati nel corpo: scheda del carapace, amplificatore, microfoni, INA3221, prese dei piedi, ADS7830 contro 2813, vano del computer | predisposizioni impossibili, carapace da ristampare | trovarli nel CAD prima della prima stampa del carapace; le voci medie che non entrano scendono di priorità | P0 |
| Punta dello stinco: oggi la testa dell'FSR non ci sta | tibia da cambiare insieme ad arco e vite del guscio | parametro nuovo, `scansione` e `interferenze`, provino del piedino | P0, P1 |
| Margine di coppia: dal 51 % fino al 55,5 % (3.4) | stalli, calore, rail che cala | a coppie di base; voci basse e computer di bordo non insieme; guscio della tibia più leggero | sempre |
| Clone della SSC-32 senza modo binario, `QP`, ingressi o baud oltre 115200 | ciclo senza margine, nessun controllo dei valori | prove in P2 prima del driver; ripiego a 25 Hz con T = 40 ms | P2 |
| Bus I2C lungo 1,1 m a 400 kHz con una decina di schede; ToF 8 × 8 che tiene il bus | errori, contatti in ritardo | pull-up 1,0–1,4 kΩ (staccati sulle schede basse, 2.4), salita misurata o errori contati; 100 kHz solo con il carico ridotto (2.5); ToF con le sole uscite utili; transazioni brevi | P2 |
| LED con dati a caso durante reset e avvio | 5 V oltre 2,5 A, ESP32 che si riavvia con i LED accesi | pull-down all'ingresso del buffer, PTC o interruttore di carico, tetto nel driver | P4 |
| Calore sotto il carapace in PLA (55–60 °C): regolatori, D24V22F5, ESP32, eventuale computer | carapace deformato, spegnimenti | NTC (X14), misura in P4, carapace in PETG se serve, secondo regolatore per i LED | P4 |
| Nessun GPIO libero con il piano A | ogni funzione nuova toglie qualcosa | tutto il nuovo sul bus I2C o sull'espansore; USB OTG riservata | sempre |
| OV3660 con il DVDD a 1,2 V | camera instabile o muta | prima prova di P2 | P2 |
| Taratura sbagliata di più di 3° (coxe: restano 1–2° per zampa) | urti fra zampe vicine o al ginocchio minimo | dime, taratura a due punti, somma tra vicine entro 56° (proposta; D-050 e D-061 dicono 60°, 2.6), hash controllato all'avvio | P3 |
| PSRAM condivisa fra camera, ESP-DL e ciclo; heap interno ridotto | passo irregolare, memoria che manca (pesi del livello 2) | ciclo in RAM interna, heap misurato, pesi int8 o in PSRAM | P2–P6 |
| Audio, camera, streaming e inferenza insieme | core 0 saturo, jitter | prova in P6; audio al telefono o al Mac se non regge | P6 |
| Wi-Fi debole sotto il carapace; radar con il Bluetooth acceso, LIDAR | video e comandi a scatti | comandi che scadono, comportamenti a bordo, antenna C8, prova dell'effetto del LIDAR | P4, P10 |
| ToF posteriore e altoparlante nella porta di servizio | T-plug, sezionamento d'emergenza, difficile da afferrare | verifica nel CAD; ripiego sopra il piano del T-plug | P0 |
| LLM che fraintende la scena; foto della casa a terzi | movimenti sbagliati; privacy | limiti nel firmware, durata massima, STOP, operatore presente; locale per default | P7 |
| Troppo lavoro per una persona, con finestre d'uso limitate | progetto che si arena | fasi piccole, ognuna con la sua verifica e uno stato da cui ripartire | sempre |

## 9. Rimandi ai documenti di dettaglio

| Argomento | `predisposizioni.md` | `software.md` |
|---|---|---|
| Cosa saprà fare | 1 | In breve, 7 |
| Architettura e livelli | 2.1, 2.6 | 1 |
| Bus I2C, connettore del carapace | 2.2, 2.3 | — |
| Audio e luci | 2.4 | 3.3, 5.5 |
| Alimentazione | 2.5 | 8 (Elettronica) |
| SSC-32 | 2.7 | 2.4 |
| Zone del robot | 2.8 | — |
| GPIO | 4.1 | 1 (pin) |
| Indirizzi I2C | 4.2 | — |
| Corrente | 4.3 | 5.4, 8 |
| Massa e coppia | 4.4 | 1 (perché), 4.2, 5.4 |
| Firmware, compiti, guardia, sicurezza, taratura | — | 2 |
| Controllo, protocollo, app, rete, video, LLM | — | 3 |
| Locomozione, RL, simulatore, modello dei servo | X5 (contatti) | 4 |
| Visione e computer di bordo | X8, X29 | 5 |
| Repo, test, CI, gemello, procedure di banco | — | 6 |
| Roadmap | — | 7 |
| CAD | 5 | 8 (CAD) |
| Voci e BOM | 3 | 8 (BOM) |
| Idee scartate | 6 | 2.1, 3.2, 4.5, 5.1 |
| Domande | 7 | 9 (domande) |
| Rischi | 2.4, 2.8 | 9 (rischi) |
| Fonti | 8 | 9 (fonti) |

## 10. Modifiche ai documenti di dettaglio

Allineamenti minimi fatti il 9 ottobre 2026 insieme a questo piano.

`software.md`:
- riga iniziale: i sensori stanno in `predisposizioni.md` (non più "non ancora presente"), con il rimando a questo piano;
- In breve: guida di luce solo senza catena LED; vano del computer di bordo con il posto da trovare;
- schema del capitolo 1: "I2C: SCCB o 2 pin" diventa "I2C0, GPIO47/3";
- tabella dei pin: GPIO 4/5 solo camera; GPIO2 ai dati dell'amplificatore; GPIO3 e GPIO47 al bus dei sensori; GPIO38–40 all'audio, con GPIO38 per la misura RMT prima dell'audio; GPIO48 alla catena LED;
- tabella dei disaccordi: bus dei sensori dedicato; IMU sul tetto del tunnel con la calibrazione camera–IMU rifatta dopo ogni smontaggio del vassoio; vano del computer con il posto da trovare;
- 3.3: il modo si vede dall'anello del pulsante, la guida di luce è il ripiego;
- S1: bus dei sensori dedicato, prova del 3V3 della scheda;
- capitolo 8: righe di IMU, ToF, guida di luce e vano nel CAD; righe del traslatore (GPIO38) e del bus nell'elettronica.

`predisposizioni.md`:
- riga iniziale: rimando a questo piano; i conflitti stanno in 2.9 (il testo diceva 2.8);
- 2.2: requisito dei contatti di `software.md` (meno di 10 ms) e durata delle letture del ToF;
- 2.7: gli ingressi della SSC-32 li legge `ctrl` al ritmo del battito;
- 2.8, zona "Sotto il dorso": il vano del computer di bordo alto 15 non ci sta;
- 2.9, IMU: la calibrazione camera–IMU si rifà dopo ogni smontaggio del vassoio;
- X28: niente LIDAR su GPIO19/20, riservati alla USB OTG; in alternativa sul computer di bordo;
- 4.1: GPIO19/20 riservati alla USB OTG; GPIO38 per la misura RMT prima dell'audio;
- domanda 7: il LIDAR toglie solo i microfoni.

Correzioni della revisione di coerenza (9 ottobre), nei tre file: spazio sotto il dorso (9,2 sopra la SSC-32, circa 13,6 sopra l'ESP32); conflitti di X22 con cicalino e X11; sede del ToF frontale da verificare; pull-up con le voci basse; ripiego a 100 kHz; bilanci a 6,6 V e senza X3; PTC da circa 0,7 A; filamenti e domande 1–4 del BOM nella roadmap; X23 e X24 nelle fasi; ingressi della SSC-32 senza il radar; guida di luce e spia di camera attiva in `software.md`; distanza dell'IMU dal baricentro (circa 50 mm).

Da aggiornare quando il piano sarà approvato (non toccati ora): `decisioni.md` (una D-066 per il piano, con la somma fra coxe vicine a 56° invece dei 60° di D-050 e D-061, e dopo P2 il baud o il formato della SSC-32 se cambia D-012), `studio-componenti.md` (riserva della RX su GPIO47), `BOM.md` (ramo logica "meno di 1 A", voce B6), `CLAUDE.md` (stato e prossimi passi).
