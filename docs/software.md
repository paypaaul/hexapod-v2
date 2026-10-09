# Stack software: firmware, controllo e AI (ricerca, backlog)

9 ottobre 2026. Approvato dall'utente lo stesso giorno (repo pubblica, ESP-IDF senza Arduino, software libero sul Mac). La fase S0 è fatta nella versione 2.1.0: stato qui sotto.

## Stato di S0 (9 ottobre 2026, versione 2.1.0)

Fatto e verificato sul Mac. I dettagli e le prove stanno in `firmware/README.md`, `sim/README.md` e `app/README.md`.

- **Descrizione unica**:
  - `cad/script/esporta_robot.py` legge il modello Fusion e scrive `robot/cad.json`: geometria, punti con nome, limiti meccanici, tabella del ginocchio, masse e inerzie per parte, cicli verificati. Scrive anche le mesh dei segmenti e `robot/pose_cad.json`, 75 pose lette con i giunti veri;
  - `robot/robot.yaml` è la parte scritta a mano: canali, versi, calettamento e limiti della guardia;
  - `tools/descrizione.py` unisce i due file e controlla l'impronta di `cad.json`.
- **Nucleo C++17** (`firmware/components/nucleo`), con le stesse formule di `calc/` e di `pose_tripode`:
  - contiene cinematica, guardia del fotogramma intero, statica, tripode a fase continua e modello del servo;
  - scarti: diretta contro il CAD 0,0001 mm; inversa contro Python 0,0004°; andatura contro Python 0,00003°;
  - regressione a 100/45: femore al 51,4 % dello stallo, margine 59 mm;
  - i casi d'urto del CAD sono rifiutati.
- **Firmware ESP-IDF v6.1** per esp32s3: compila (174 KB, 4 % dello slot OTA). Il compito `ctrl` gira a 50 Hz in modo OMBRA, con il rail spento; il resto è scheletro. Non è ancora provato sul chip.
- **Simulazione MuJoCo** (`sim/`), con emulatore della SSC-32 e modello generato da `tools/genera_modelli.py`. Prova di 20 s di tripode a 100/45 comandata attraverso l'emulatore, superata anche con la rotazione di 30°:
  - corpo fra 97,7 e 99,2 mm, inclinazione 0,2°;
  - nessun urto;
  - scivolamento 0,5 mm all'atterraggio;
  - femore al 51 % dello stallo.
- **Gemello digitale nel browser** (`app/`, three.js): riproduce tripode e rotazione con i cursori di assetto e avvisa che le pose sono comandate, non misurate.
- **CI su GitHub** (`ci.yml`, `sim.yml`): ruff e pytest, nucleo con gcc e clang e i sanitizer, firmware, file generati, simulazione, app.

Aperti:
- **Coppia agli assetti bassi.** A 70/70 il ciclo a tripode porta il femore al 75 % dello stallo: è sopra la soglia di rifiuto proposta (70 %), quindi la guardia lo rifiuta. In MuJoCo arriva all'81 %. Nel CAD l'assetto 70/70 è libero da urti, ma per andarci servono un'andatura con più piedi a terra (a coppie o a onda) o una soglia diversa: decide l'utente quando si sceglie l'assetto, a robot costruito.
- **Contatti in MuJoCo.** La rigidezza dei contatti (0,005 s) è una stima: con il valore standard il femore sale all'83 % e la prova non passa. Va tarata sui registri del robot (S4).
- **Atterraggio del piede.** Con il volo di `pose_tripode` il piede tocca terra a 240 mm/s e striscia di 2–3 mm. Il generatore del firmware userà una curva che arriva a velocità zero.
- **Nel CI** il job del firmware dipende dall'immagine Docker di Espressif: i primi giri sono falliti per i limiti di Docker Hub, non per la compilazione. Ora l'immagine si scarica con tre tentativi.

Nasce da cinque ricerche indipendenti: architettura del firmware, controllo e interfacce, locomozione e reinforcement learning, visione e AI, strumenti e test. Qui sono unite. Dove i ricercatori non erano d'accordo la scelta è spiegata (tabella in fondo al capitolo 1). I sensori (IMU, contatti dei piedi, corrente, ToF frontale, LED) li sceglie la ricerca parallela, in `docs/predisposizioni.md`; il piano che unisce le due ricerche è `docs/piano-elettronica-software.md`. Qui sono trattati come probabili e il firmware è pensato per funzionare anche senza.

Legenda: **V** dato da fonte primaria indicata dai ricercatori (non riletta in questa sintesi); **S** stima o fonte secondaria; **C** da confermare al banco o sul robot; *calcolo* = rifatto oggi sui file della repo.

## In breve

- **Tre livelli.** L'ESP32-S3 è il "midollo spinale": andature, cinematica, sicurezza e una visione leggera, sempre attivi anche senza rete. Il Mac o un PC è il "cervello" facoltativo: visione pesante, mappa, navigazione, LLM, simulazione e addestramento. Un computer di bordo si **predispone** nel CAD ma non si compra.
- **Firmware** in C++ su ESP-IDF. Ciclo fisso a 50 Hz sul core 1, uguale al periodo degli impulsi della SSC-32. Ogni comando, da qualunque sorgente, passa da **una guardia unica** che applica i limiti verificati nel CAD.
- **Dall'esterno arrivano solo comandi che scadono** (velocità, assetto, andatura). Gli angoli dei giunti non viaggiano in Wi-Fi, salvo nel modo laboratorio.
- **Una sola descrizione del robot** esportata dal CAD genera l'header del firmware, le costanti di `calc/` e i modelli URDF e MJCF. Oggi le stesse costanti stanno in quattro posti e già divergono.
- **Locomozione**: oscillatori di fase con andatura **a coppie** di base (giunto più caricato al 41 % dello stallo a 100/45), tripode per andare veloci, a onda per gli assetti bassi. Poi una **politica appresa che modula l'andatura** (PMTG), addestrata in MuJoCo sul Mac ed **eseguita sull'ESP32**.
- **Visione**: a bordo persone, volti e AprilTag (persone a 3–5 fps con lo streaming, al massimo 6,8; da misurare); fuori bordo YOLO, profondità monoculare, localizzazione e Nav2; sopra, un agente LLM che usa il robot attraverso un server MCP con abilità limitate.
- **Niente da comprare adesso.** Da predisporre nel CAD: dime di taratura, cavalletto da banco, sedi di IMU e ToF (quelle di `predisposizioni.md`), vano del computer di bordo (posto da trovare); la guida di luce del LED solo se non si fa la catena LED.
- **Primo passo, senza hardware** (fase S0): descrizione unica del robot, nucleo C++ provato contro `calc/` e contro le pose del CAD, gemello nel browser e in MuJoCo, integrazione continua.

## 1. Architettura

```
  telefono o browser                      PC / Mac: "cervello", facoltativo
 +---------------------------+     +------------------------------------------------------+
 | app: joystick, gamepad,   |     | ponte Python: Rerun o Foxglove, MCAP, ROS 2, MCP     |
 | video, gemello 3D, STOP   |     | percezione: YOLO26, profondità, AprilTag, Nav2       |
 +-------------+-------------+     | MuJoCo: gemello fisico, SIL, addestramento RL        |
               |                   +----------+-------------------+----------------+------+
               | WebSocket:                   | UDP: telemetria   | HTTP :81:      | API
               | comandi che scadono,         | 50 Hz, comandi    | video MJPEG    v
               | telemetria 10-20 Hz          | che scadono       |         LLM in cloud o locale
               |                              |                   |
 ==============|======== Wi-Fi 2,4 GHz =======|===================|=====
               |                              |                   |
 +-------------+------------------------------+-------------------+-----------------------------+
 | ESP32-S3: "midollo spinale", autonomo anche senza rete                                       |
 | core 1  ciclo 50 Hz: stato > andatura > IK > politica RL > GUARDIA > gruppo di 18 canali     |
 |         sensori a 100 Hz; visione leggera (ESP-DL) a priorità bassa                          |
 | core 0  Wi-Fi, HTTP e WebSocket, camera, telemetria, NVS, OTA                                |
 +----+-------------+---------------+------------------+-------------+-------------+------------+
      |             |               |                  |             |             |
  UART1 21/14  DVP, SCCB 4/5   I2C0, GPIO47/3      ADC GPIO1     GPIO42, 41    USB OTG 19/20
      v             v               v                  v             v             v
  SSC-32 clone  OV3660 120°    IMU, contatti,      batteria 2S   rail 6 V,     predisposto:
  impulsi 20 ms in avanti      corrente, ToF       (partitore)   interruttore  computer di bordo
      |                        (ricerca sensori)                 2813          formato Zero
      v 18 PWM                                                                 (UVC + CDC)
  18 MG996R senza retroazione di posizione
```

### Cosa gira dove

| Livello | Dove | Cosa | Frequenza |
|---|---|---|---|
| Passo e sicurezza | ESP32, core 1 | macchina a stati, andatura, IK, politica, guardia, invio alla SSC-32 | 50 Hz |
| Sensori | ESP32, core 1 | IMU (FIFO a 200–400 Hz), ADC, contatti | 100 Hz |
| Visione leggera | ESP32, core 1, priorità bassa | persone, volti, AprilTag, "sono bloccato" | 2–7 Hz |
| Rete e video | ESP32, core 0 | Wi-Fi, app, WebSocket, UDP, MJPEG | — |
| Percezione | PC | rilevamento, profondità, marcatori | 10–30 Hz |
| Navigazione | PC | stima della posizione, mappa, Nav2 | 5–20 Hz |
| Agente | PC più LLM | obiettivi in linguaggio naturale | 0,2–1 Hz |
| Addestramento | Mac, GPU in cloud | MuJoCo | fuori linea |

### Perché

- **Il Wi-Fi ha ritardi variabili e buchi.** Un'andatura calcolata sul PC si fermerebbe a ogni buco. Per questo il ciclo e i limiti stanno a bordo, e il robot resta sicuro se la rete cade.
- **Il margine di coppia è scarso.** Il femore lavora al 51,4 % dello stallo a 100/45 con 2945 g (*calcolo*, `calc/statica_tripode.py`). Ogni 57 g in più costano circa un punto. Un computer di bordo oggi non si giustifica: la potenza di calcolo sta sul PC, che non pesa.
- **I servo non dicono dove sono.** Il firmware è l'unica difesa contro gli urti tra zampe e contro lo stallo. Per questo c'è una guardia unica, e ogni comportamento nuovo si prova prima nel gemello, poi al banco, poi a terra.
- **La SSC-32 genera da sola gli impulsi.** Un ritardo dell'ESP32 rallenta l'aggiornamento della traiettoria ma non sposta gli impulsi dei servo. Basta un ciclo a 50 Hz con poco jitter, non un tempo reale al microsecondo.
- **Una sola fonte dei dati.** Firmware, calcoli e simulatore leggono gli stessi numeri, generati dal CAD. Oggi il ginocchio minimo vale 36 in `calc/statica_tripode.py`, 45 in `calc/andature.py` ed è una tabella in `cad/script/zampa.py` (riga 973); il limite della coxa sta in `assieme.py` (*verificato oggi*).
- **Lo stesso codice sul robot e nel simulatore.** Il nucleo (IK, andature, guardia, politica) è C++ senza dipendenze dall'ESP-IDF: si compila anche sul Mac, per i test e per MuJoCo.

### Pin dell'ESP32 per il software

| GPIO | Uso | Stato |
|---|---|---|
| 21 / 14 | UART1 verso la SSC-32 (TX / RX), con il ritorno collegato | deciso (D-012) |
| 1 | tensione di batteria (ADC1) | deciso |
| 42 | accensione del rail servo (spento se flottante) | deciso (D-019) |
| 41 | spegnimento dell'interruttore 2813 | deciso |
| 48 | catena LED in parallelo al WS2812 della scheda, che ripete il primo pixel (`predisposizioni.md` X9) | proposta |
| 19 / 20 | USB OTG: flash, JTAG, prove HIL; poi l'eventuale computer di bordo | **da riservare** |
| 43 / 44 | UART0 (CH340): console | sulla scheda |
| 4 / 5 | SCCB della camera, da sola; riserva per i sensori se il bus dedicato non va | sulla scheda |
| 2 | dati I2S verso l'amplificatore (`predisposizioni.md`, piano A). Porta il LED "ON" della scheda (`dimensioni-componenti.md`): per l'I2C no, il LED carica la linea | proposta |
| 47 / 3 | SDA / SCL del bus dei sensori, I2C0 (`predisposizioni.md` 2.2). GPIO47 ha un solo uso: la riserva della RX della SSC-32 (`studio-componenti.md`) sparisce | proposta |
| 38 / 39 / 40 | I2S dell'audio senza scheda TF (la TF non serve: si registra sul PC). Al banco, prima dell'audio, GPIO38 misura gli impulsi con l'RMT | proposta |

### Dove le ricerche non erano d'accordo

| Tema | Proposte | Scelta e perché |
|---|---|---|
| Versione di ESP-IDF | v6.1 (firmware); v6.0 perché micro-ROS è provato lì (strumenti); ≥ 5.3 (locomozione) | **v6.1**, ripiego su v6.0 e poi v5.5 se esp32-camera o esp-dl non compilano (prova in S1). L'argomento di micro-ROS non vale: micro-ROS non è nel piano. Versione fissata dall'immagine Docker e da `dependencies.lock` |
| Dove gira l'inferenza della visione | core 1 a priorità bassa (firmware); core 0 con il Wi-Fi (visione) | **core 1, priorità bassa**: il ciclo la interrompe sempre, in modo deterministico; il core 0 è già occupato da Wi-Fi, camera e server. Se il jitter supera l'obiettivo si sposta sul core 0 o si rallenta |
| Linguaggio del nucleo | C (locomozione); C++17 (firmware, strumenti) | **C++17** con un'interfaccia C per Python (ctypes): stesso codice in firmware, test e simulatore |
| Bus dei sensori | SCCB della camera condiviso (firmware, visione); bus dedicato su 2 pin liberi (locomozione) | **bus dedicato su GPIO47/3**, scelto in `predisposizioni.md` 2.2: all'avvio esp32-camera scrive agli indirizzi della sua tabella, e un sensore che blocca il bus fermerebbe la camera. Il firmware tiene il bus condiviso come riserva (la OV3660 risponde a 0x3C, S) |
| Andatura di base | scelta automatica (firmware); a coppie di base (locomozione) | **a coppie di base**, tripode per la velocità, a onda per gli assetti bassi; il passaggio lo decide il budget di coppia |
| Collegamento perso | 0,5 s e 30 s (firmware); 300 ms, 3 s e 30 s (interfacce) | **a gradini**: 300 ms si ferma in piedi; 30 s si siede e solo dopo spegne il rail. Mai rail spento con il robot in piedi per colpa della rete |
| Inclinazione | posa sicura oltre 25–30° (locomozione); rail spento oltre 50° (firmware) | **entrambe**, come due soglie; la prima dipende dall'assetto, perché a 130/25 il robot si ribalta già a 21° (2.6) |
| Taratura dei servo | un punto (locomozione); due punti con dime (firmware, strumenti) | **due punti con dime**, salvata in NVS e in git con un hash |
| Gamepad | BLE sull'ESP32 (firmware, locomozione); dal browser (interfacce) | **dal browser prima** (niente radio condivisa, niente RAM), Bluepad32 dopo, se serve guidare senza telefono |
| Visualizzatore | Foxglove (interfacce, visione); Rerun, perché l'edizione libera di Foxglove è chiusa (strumenti) | **formato MCAP**, visualizzatore Rerun di base (libero, funziona senza rete); Foxglove facoltativo |
| Identificazione dei servo | video al rallentatore di una leva (strumenti); prove automatiche con IMU e corrente (locomozione, firmware) | **prove automatiche**: l'utente non misura i servo (sua indicazione). Il video resta facoltativo |
| Forma della politica | residuo sui piedi (firmware); modulazione dell'andatura, PMTG (locomozione) | **PMTG**, che comprende il residuo: ±10 mm all'inizio, al massimo ±15 |
| Esecuzione della politica | ESP-DL o TFLite Micro (firmware); codice generato dai pesi (locomozione) | **codice generato**, nessuna libreria; ESP-DL solo se la rete cresce |
| Telemetria | 50 Hz (firmware); 100 Hz (strumenti) | **50 Hz**, il ritmo del ciclo; l'IMU grezza, se serve alla VIO, a parte e a pacchetti |
| Scatola nera | 30 s (firmware); 60 s (strumenti) | **60 s**, circa 0,6 MB di PSRAM su 8 MB |
| Computer di bordo | non serve (locomozione); da predisporre (visione) | **predisporre ora** vano, 5 V e USB (circa 5 g di stampa; il posto del vano è da trovare, 8), **comprare solo** se le fasi con il PC lo dimostrano |
| Porta USB OTG | debug e HIL (strumenti); collegamento del computer di bordo (visione) | **debug e HIL durante lo sviluppo**; se arriva il computer di bordo la porta passa a lui e il debug va sulla CH340 e in OTA |
| Servo nel simulatore | attuatore di posizione (strumenti); PID con limite di velocità e ritardo (locomozione) | **PID con limite di velocità e ritardo** (MuJoCo ≥ 3.12); ripiego: posizione più ritardo scritto nell'ambiente |
| Posizione dell'IMU | vicino al baricentro (locomozione); rigida con la camera (visione) | **sul tetto del tunnel sotto il vassoio** (`Corpo_Base`, `predisposizioni.md` X4): misura il corpo che porta le zampe, e il tetto è più rigido del vassoio; per l'assetto i circa 50 mm dal baricentro non contano. La calibrazione camera–IMU (5.2) si rifà dopo ogni smontaggio del vassoio |
| Partizioni | LittleFS da 6 a 7,8 MB secondo il ricercatore | **tabella del firmware** (capitolo 2.8) |

## 2. Firmware

### 2.1 Piattaforma

- **ESP-IDF in C++17**, versione bloccata nella repo. Componenti ufficiali: esp32-camera (OV3660, frame buffer in PSRAM), esp-dl (inferenza con le istruzioni vettoriali dell'S3), esp-dsp, led_strip. Dall'IDF: server HTTP con WebSocket, NVS, OTA con ritorno alla versione precedente, core dump, USB Serial/JTAG.
- Perché non Arduino: è uno strato sopra l'IDF che nasconde proprio le leve che servono (compiti fissati a un core, priorità, partizioni, sdkconfig). Va bene solo per prove rapide.
- Scartati: MicroPython (garbage collector, niente ciclo deterministico), Rust con esp-hal 1.0 (camera instabile, niente equivalente di ESP-DL), Zephyr (OV3660 ed ESP-DL non integrati, S).
- **Float a precisione singola ovunque**: l'FPU dell'S3 non fa il double, che è emulato (V). Niente float nelle interruzioni.
- Ogni versione dell'IDF ha 12 mesi di servizio e 30 di supporto (V). L'IDF 6 toglie i driver vecchi e tratta gli avvisi come errori: per codice nuovo va bene, per qualche componente esterno no (S).

### 2.2 Compiti, core e frequenze

| Compito | Core | Priorità | Ritmo | Cosa fa |
|---|---|---|---|---|
| `ctrl` | 1 | 22 | 50 Hz, da un timer hardware con l'interruzione sul core 1 | legge l'ultimo comando e l'ultimo campione dei sensori; stato, andatura, IK, politica, guardia, conversione in µs, invio alla SSC-32 |
| `sens` | 1 | 20 | 100 Hz | FIFO dell'IMU, ADC di batteria e corrente, contatti |
| `infer` | 1 | 3 | 2–7 Hz | ESP-DL; sempre interrotto da `ctrl` |
| Wi-Fi, esp_timer, eventi, lwIP | 0 | 23, 22, 20, 18 | — | di sistema, lwIP fissato al core 0 |
| `comm` | 0 | 15 | a evento | WebSocket, UDP, gamepad facoltativo |
| `cam` | 0 | 10 | 10–20 Hz | acquisizione e streaming |
| `telem` | 0 | 8 | 50 Hz | fotogrammi di telemetria, scatola nera |
| `servizio` | 0 | 3 | a evento | NVS, LittleFS, OTA |

Regole:

- Scambio tra compiti con caselle a doppio buffer e numero di sequenza: `ctrl` non aspetta mai un mutex tenuto da un compito lento.
- **La UART della SSC-32 ha un solo proprietario, `ctrl`**: manda il gruppo, le domande del battito e legge le risposte (2.4). Nessun altro compito ci scrive, così non serve un blocco condiviso.
- Codice, stack e dati del ciclo in RAM interna, mai in PSRAM: la PSRAM è condivisa con il DMA della camera e con ESP-DL, e quando la CPU la usa insieme al DMA la banda crolla (V).
- **Nessuna scrittura in flash con il robot in piedi**: durante una scrittura le cache si spengono e i compiti fuori dalla IRAM si fermano (V).
- Budget del ciclo: al massimo 2 ms. Jitter obiettivo: sotto 1 ms al 99,9° percentile, misurato e mandato in telemetria come istogramma. Stime dei costi: IK dei 18 giunti circa 50 µs, andatura e guardia qualche centinaio di µs, politica sotto 0,2 ms (S, da misurare).
- RAM interna: 512 KB di SRAM in tutto (V), ma è molto meno quella libera. Il codice in IRAM e i dati statici la riducono ("the available heap memory at runtime is reduced by the total static IRAM and DRAM usage", V, ESP-IDF), poi cache, stack, buffer DMA della camera, server HTTP, Wi-Fi e lwIP (circa 100–150 KB, S) ed eventualmente il BLE. Il dato da usare è l'heap interno libero misurato (`heap_caps_get_free_size(MALLOC_CAP_INTERNAL)`) con Wi-Fi, camera, server e streaming attivi, in S1 e in S3 (C).

### 2.3 Moduli

| Modulo | Compito |
|---|---|
| `nucleo` (C++ puro) | geometria generata, IK e cinematica diretta, andature, assetto e coppie stimate, guardia, modello dei servo, mappa dei canali, politica |
| `ssc32` | UART, gruppi ASCII o binari, Q e QP, ingressi |
| `potenza` | rail (GPIO42), spegnimento (GPIO41), ADC, soglie |
| `sicurezza` | macchina a stati, watchdog, eventi |
| `sensori` | bus I2C, IMU, contatti, ToF, corrente; backend vero o simulato |
| `camera`, `visione` | acquisizione e streaming; ESP-DL |
| `comandi` | schema dei messaggi, arbitraggio, caselle verso `ctrl` |
| `rete` | Wi-Fi, mDNS, HTTP, WebSocket, UDP, BLE facoltativo |
| `telemetria` | fotogrammi, scatola nera |
| `config`, `ota` | NVS, taratura, esportazione JSON; aggiornamenti |

Ogni modulo ha un'interfaccia piccola: si cambia il driver della SSC-32 o si aggiunge un sensore senza toccare il controllo. Il livello hardware ha sempre due backend, vero e simulato, per le prove SIL e HIL (capitolo 6).

### 2.4 Protocollo con la SSC-32

- UART1 (TX GPIO21, RX GPIO14), **con il filo di ritorno collegato**: servono le risposte.
- All'avvio: lettura di `VER` e del registro del baud; un primo comando senza S né T per ogni canale (la SSC-32U ignora S e T finché non ne ha ricevuto uno normale, V).
- A ogni ciclo: **un gruppo con i 18 canali e T pari al periodo** (`#cP<µs>…T20<cr>`). Oltre 50 Hz non si guadagna nulla: la scheda rinnova gli impulsi ogni 20 ms (V).
- Battito: `Q` (la SSC-32 risponde) e `QP` a rotazione su due canali, per controllare che il valore arrivato sia plausibile (risoluzione 10 µs). `QP` restituisce l'impulso che la scheda sta mandando in quel momento: con T a ogni ciclo è un valore interpolato, non quello mandato, quindi si accetta se sta tra il comando precedente e quello nuovo, con una tolleranza (S, forum RobotShop). La risposta può arrivare fino a 5 ms dopo la domanda (S): questo ritardo entra nel conto del tempo della linea. A 115200 baud si fanno ogni 5 cicli; con il modo binario o a 230400 a ogni ciclo.
- Gli ingressi della SSC-32, se servono, si leggono allo stesso ritmo del battito, sempre da `ctrl`. Per i piedi non servono (4.3).
- Per liberare i servo: `P0` sui canali (lo fa il codice Phoenix) oppure rail spento.
- Mai scrivere registri nel ciclo: la EEPROM regge circa 100 000 scritture (S).

| Formato del gruppo | Byte | a 115200 baud | a 230400 baud |
|---|---|---|---|
| ASCII, 18 canali più T | 130–151 | 11,3–13,1 ms | 5,6–6,6 ms |
| binario del codice Phoenix (3 byte a servo, chiusura 0xA1 con il tempo) | 57 | 4,9 ms | 2,5 ms |

*Calcolo*: byte × 10 bit / baud. A 115200 il gruppo ASCII occupa due terzi del ciclo: con battito e letture si resta senza margine. Il quarzo del clone (14,7456 MHz) divide esattamente 230400 e 460800 (S). **In S1 si prova cosa accetta il clone** (baud più alti, modo binario, Q, QP, STOP, ingressi) e si tiene il formato più veloce che funziona senza errori. Ripiego: fotogrammi chiave a 25 Hz con T = 40 ms, interpolati dalla SSC-32, come fa il codice Phoenix.

Il protocollo ASCII non ha checksum: un byte rovinato può spostare un servo. Contromisure: cavi corti, massa comune, `QP` di controllo, limite di velocità `S` per servo se la banda lo consente.

### 2.5 Guardia

Un modulo unico, attraversato da ogni sorgente (andatura, PC, politica), controlla **il fotogramma intero** prima dell'invio.

| Limite | Valore nel firmware | Da dove viene |
|---|---|---|
| Imbardata di coxa | ±30° | fine corsa ±35°, contatto tra vicine tra 31° e 32° ciascuna (D-061, D-063) |
| Due vicine una verso l'altra | somma entro 56° (proposta) | D-050, D-061; a sinistra imb_A − imb_M e imb_M − imb_P, a destra il contrario. D-061 dice 60°, ma con ogni zampa entro ±30° la somma non supera mai 60°: quel limite non toglie nulla. Con 56° restano 3° per zampa, come al ginocchio; la rotazione sul posto di 30° arriva a 50° (`progetto-meccanico.md`). Se approvata, cambia D-050 e D-061: va registrata in `decisioni.md` |
| Femore | da −45° a +82° | campo libero −49…+85 meno 3°; in basso −45, perché la tabella del ginocchio minimo parte da lì (`GAMMA_MIN` in `zampa.py`) |
| Ginocchio | da γmin(α) + 3° a 177° | tabella del ginocchio minimo (`progetto-meccanico.md`); fra due righe vale **il massimo** dei due valori, perché la tabella non è monotona (−40 → 55, −35 → 45) |
| Corsa dei servo | ±80° attorno al calettamento | calettamento a α +20°, γ 100° |
| Velocità per giunto | 250°/s (proposta) | a vuoto 0,14 s/60° = 429°/s (V). Con 250°/s il tripode arriva a circa 105–115 mm/s (4.2); per andare più veloci si alza dopo l'identificazione dei servo, sempre sotto 429°/s |
| Coppia stimata | avviso al 55 % dello stallo, sopra il 60 % solo per un tempo limitato, rifiuto al 70 % (proposte) | ripartizione statica dei carichi sui piedi a terra, come in `calc/` |
| Stabilità | baricentro ad almeno 20 mm dai lati del poligono d'appoggio (proposta) | `calc/statica_tripode.py` |

- Se un fotogramma viola un limite **non si tronca il singolo giunto**, perché il piede striscerebbe: si riduce il comando (corsa, velocità, assetto) e si ricalcola. Se non basta si tiene il fotogramma precedente e si registra l'evento.
- I limiti rigidi sono generati dalla repo e non si cambiano dalla rete. I limiti morbidi (in NVS) possono solo stringere quelli rigidi.
- Il margine di 3° sul ginocchio vale solo se la taratura sbaglia di meno: per questo le dime sono necessarie. Lo stesso vale per le coxe: con ±30° e 60° resterebbero 1–2° per zampa prima del contatto, meno dell'errore di taratura (±2° nella randomizzazione del 4.4) e del gioco (0,5–1,5°).
- Il contatto tra vicine a 31–32° è verificato nelle pose provate nel CAD, con le due zampe ruotate dello stesso angolo. Le coppie con angoli diversi (per esempio 30° e 26°) sono da provare con `assieme.py` prima di fissare il limite.
- Se cambia una parte della zampa si rifà la scansione con `zampa.py`; il generatore riporta la nuova tabella nel firmware.

### 2.6 Sicurezza e macchina a stati

Stati: AVVIO → RIPOSO → RISVEGLIO → IN PIEDI ⇄ CAMMINO → SEDUTA → RIPOSO; in più OMBRA (firmware completo con il rail spento), CALIBRAZIONE, GUASTO, SPEGNIMENTO.

Accensione:

1. GPIO42 basso dal primo istante: rail spento finché la SSC-32 non risponde, la taratura non è valida e la batteria non è sopra soglia.
2. Impulsi della posa di parcheggio su tutti i canali, poi rail acceso (ordine di D-019).
3. Controllo del calo di tensione, poi alzata lenta con T lungo.

Spegnimento: seduta sulla chiglia, parcheggio, rail spento, impulso su GPIO41.

| Evento | Soglia (proposta, da tarare) | Azione |
|---|---|---|
| Batteria bassa | sotto 3,6 V/cella, filtrata sotto carico | avviso, velocità ridotta |
| Batteria scarica | sotto 3,5 V/cella per 5 s (soglia dello studio dei componenti; più livelli come in D-011) | seduta, parcheggio, rail spento |
| Batteria critica | sotto 3,3 V/cella | rail spento e spegnimento |
| Nessun comando | 300 ms | decelera e si ferma in piedi |
| Nessun collegamento | 30 s | seduta sulla chiglia, poi rail spento |
| Inclinazione del piano dei piedi (IMU meno l'inclinazione comandata al corpo) | dipende dall'assetto: angolo di ribaltamento, atan(margine di stabilità / altezza del baricentro), meno 6°. Circa 15° a 130/25, 21° a 110/40, 25° a 100/45 | posa sicura |
| Caduta | oltre 50° o capovolto | rail spento subito |
| SSC-32 muta | 3 `Q` senza risposta | GUASTO, rail spento |
| Corrente (se c'è il sensore) | sopra soglia | seduta o rail spento |
| Sforzo prolungato | budget termico per giunto, dalla coppia stimata integrata nel tempo | seduta forzata |
| Blocco del firmware | watchdog dei compiti a 1 s su `ctrl`, `comm`, `servizio` | riavvio; durante il reset GPIO42 è flottante e il rail si spegne |

- Angolo di ribaltamento (*calcolo* con le funzioni di `calc/andature.py`, margine minimo su tutto il passo): 21° a 130/25, 27° a 110/40, 31° a 100/45, 40° a 80/60, 46° a 70/70, con il baricentro all'asse dei femori. Con il baricentro del modello, 13 mm più in basso (`progetto-meccanico.md`), 23°, 30°, 34°, 45° e 52°. Una soglia fissa di 25–30° arriverebbe dopo il ribaltamento negli assetti alti. Il margine di 6° è una proposta, da tarare a robot costruito.
- Il budget termico segue l'indicazione Lynxmotion: circa 10 minuti di sforzo continuo, poi circa 30 di riposo (S).
- Dopo un riavvio non voluto (`esp_reset_reason`) la posa è ignota: si riparte una zampa alla volta.
- Dopo un crash il robot cade sulla chiglia: circa 59 mm a 100/45 (*calcolo*: asse a 100, chiglia 41,4 sotto). La chiglia deve reggerlo.
- Il pulsante d'accensione è anche l'arresto d'emergenza: spegne la logica, GPIO42 resta flottante e il rail si spegne. Il T-plug resta il sezionamento dei servo.
- Da controllare: che GPIO41 e GPIO42 non abbiano pull-up interni all'avvio (dal testo del datasheet sembra di no, C) e che il pin OFF della 2813 non scatti con GPIO41 flottante (eventuale 100 kΩ verso massa, C). Da provare al banco come reagisce un MG996R alimentato senza impulsi.

### 2.7 Taratura dei servo

- Per ogni giunto: canale, verso, impulso a due angoli noti (da cui offset e guadagno), impulso minimo e massimo.
- Valori di partenza generati dalla repo: servo a metà corsa con α +20°, γ 100° e coxa in direzione neutra. Le sei zampe sono la stessa zampa ruotata, non specchiata: lo stesso verso vale per tutte (`robot/robot.yaml` → `servo.verso`, ipotesi da provare al banco).
- Procedura dalla web app, nello stato CALIBRAZIONE: un servo alla volta, passi di ±1 e ±10 µs, **due pose fissate da dime stampate**: coxa a 0° e +30°, femore a 0° e +45°, ginocchio a 90° e 135°. Circa un'ora per il robot (S).
- Salvataggio: blob con versione e CRC in una partizione NVS dedicata, copia in `robot/calib/<robot>.yaml` nella repo. All'avvio il firmware manda l'hash in telemetria e gli strumenti avvisano se non coincide. **Senza taratura valida il rail non si accende.**
- Le correzioni le applica l'ESP32, non il comando `PO` della SSC-32: copre solo ±100 µs e non resta allo spegnimento (V).
- Perché due punti: la squadretta a 25 denti si cala a passi di 14,4°, quindi l'errore di montaggio arriva a ±7,2°, circa ±80 µs (*calcolo*). Il guadagno dell'MG996R non è pubblicato: circa 11 µs/° sul campo 500–2500 µs (S). Se femore e ginocchio risultano non lineari si aggiunge un terzo punto.

### 2.8 OTA, partizioni, configurazione

| Partizione | Dimensione | Uso |
|---|---|---|
| `nvs` | 24 KB | configurazione, assetti, limiti morbidi, credenziali Wi-Fi |
| `nvs_cal` | 16 KB | taratura |
| `otadata`, `phy_init` | 8 + 4 KB | |
| `ota_0`, `ota_1` | 4 MB ciascuna | firmware (immagine prevista sotto 4 MB, S) |
| `coredump` | 64 KB | |
| `storage` (LittleFS) | circa 7,8 MB | web app, modelli ESP-DL, pesi della politica, scatola nera |

- OTA dalla web app o da `hexa` sul Mac, **solo in RIPOSO con il rail spento**. La nuova versione si dichiara valida solo dopo un autotest (SSC-32 risponde, taratura valida, batteria plausibile, sensori presenti), altrimenti si torna alla precedente.
- Wi-Fi con le credenziali in NVS ma configurato in RAM, per non scrivere in flash durante l'uso.
- **Secure Boot e cifratura della flash non si attivano**: bruciano eFuse in modo irreversibile (domanda 15).
- La USB-C OTG resta raggiungibile dallo sportellino per il recupero (D-034).

### 2.9 Telemetria e diagnostica

- Fotogramma binario a 50 Hz, circa 200 byte: stato e sorgente attiva, comando, fase dell'andatura, 18 angoli e µs comandati, angoli stimati dal modello dei servo, coppie stimate, tensione e corrente, IMU, contatti, durata e ritardo del ciclo, errori UART, RSSI, memoria libera. Circa 10 KB/s (*calcolo*).
- Ogni fotogramma porta il tempo del robot in µs: video, IMU e telemetria si allineano sullo stesso orologio.
- Scatola nera: ultimi 60 s in PSRAM, scritti su LittleFS dopo un guasto, a rail già spento.
- Console a comandi sulla porta CH340 per il banco (`ssc`, `servo`, `rail`, `cal`, `stato`), core dump in flash, LED WS2812 per lo stato (ombra, banco, attivo, errore, camera attiva).

## 3. Controllo e interfacce

### 3.1 Principio

Tre livelli di comando:

1. **Moto**: velocità del corpo (vx, vy in mm/s, imbardata in °/s), altezza, rollio, beccheggio e imbardata del corpo, andatura, alzata, in piedi, seduto, STOP. È il solo che arriva da fuori nell'uso normale.
2. **Piedi**: posizioni dei sei piedi.
3. **Giunti**: angoli dei 18 giunti.

Piedi e giunti valgono solo nel modo LABORATORIO, con il robot sul cavalletto, e passano comunque dalla guardia.

Arbitraggio: sicurezza di bordo > operatore (app, gamepad) > autonomia del PC > LLM. Uno STOP da qualunque sorgente vale sempre. Muovere lo stick dell'operatore riprende il comando. Vale l'ultimo comando valido entro la sua scadenza: un pacchetto perso non si ritrasmette.

### 3.2 Protocollo

Un solo schema in Protocol Buffers (`proto/hexapod.proto`), compilato con nanopb per l'ESP32 (solo memoria statica) e con i generatori standard per Python e TypeScript. Ogni messaggio porta versione, numero di sequenza e tempo del robot. Regola: i campi si aggiungono, non si rinumerano.

| Messaggio | Da → a | Ritmo | Scadenza |
|---|---|---|---|
| `ComandoMoto` | app, gamepad, PC → robot | 20–50 Hz | 300 ms |
| `ComandoPiedi`, `ComandoGiunti` | PC → robot, solo LABORATORIO | 50 Hz | 100 ms |
| Richiesta e risposta | qualunque client ↔ robot | a richiesta | — |
| `Telemetria` | robot → PC (UDP) e app (WebSocket) | 50 Hz e 10–20 Hz | — |
| `Evento` | robot → tutti | quando succede | — |

Le richieste coprono cambio di modo, presa e rilascio del controllo, rail, parametri, taratura, pose, foto, OTA. Gli eventi: limite raggiunto, caduta, batteria bassa, collegamento perso.

Trasporti: WebSocket binario per l'app, UDP per il PC, seriale USB per il banco. Il WebSocket viaggia su TCP: con perdite un comando può arrivare in ritardo. Le scadenze brevi limitano il danno; se non basta, WebRTC con canale non affidabile (3.7). Scartati MAVLink (pensato per droni e rover) e JSON (senza schema; resta come vista di debug nel ponte).

### 3.3 Modi

| Modo | Chi comanda | Cosa aggiunge il firmware |
|---|---|---|
| MANUALE | operatore | — |
| ASSISTITO | operatore | frena davanti agli ostacoli (ToF), livella il corpo (IMU), adatta l'alzata (contatti), rallenta con la batteria bassa |
| AUTONOMO | PC (visione, navigazione, LLM) | l'operatore vede e può scavalcare |
| LABORATORIO | PC, comandi di piedi e giunti | robot sul cavalletto: taratura, identificazione, prove di politiche |
| OMBRA | qualunque | firmware completo con il rail spento: il gemello mostra cosa farebbe il robot |

Il modo si vede da fuori: anello del pulsante (`predisposizioni.md` X11). Se la catena LED non si fa, il LED della scheda portato alla visiera con una guida di luce.

### 3.4 Rete

- Wi-Fi 2,4 GHz sulla rete di casa; access point del robot (WPA2) come riserva. Nome `hexapod.local` via mDNS, più indirizzo IP e QR code nell'app (su Android i nomi `.local` non sempre si risolvono, S).
- Risparmio energetico del Wi-Fi spento durante la guida: con quello di default la ricezione può ritardare fino a un intervallo DTIM (V). Con il Bluetooth acceso (3.6) non basta: in coesistenza il Wi-Fi resta attivo solo nella sua fetta di tempo (V), e secondo un forum l'IDF rifiuta di spegnere il risparmio ("Should enable WiFi modem sleep when both WiFi and Bluetooth are enabled", S). Quindi con il BLE si accetta il ritardo, oppure niente Bluetooth durante la guida in Wi-Fi. Da provare in S1.
- Un solo pilota alla volta, gli altri client in sola lettura; token controllato prima dell'apertura del WebSocket.
- Ritardo atteso dal comando all'inizio del movimento: 35–60 ms (S): rete, attesa del ciclo, UART, fotogramma della SSC-32, servo.
- Banda: telemetria circa 10 KB/s, video VGA 0,5–1 MB/s (S). L'S3 fa decine di Mbit/s in laboratorio (V); in casa, sotto il carapace, si misura in S3. Se non basta c'è l'antenna esterna C8.

### 3.5 App web

- Servita dall'ESP32 (LittleFS, compressa): niente da installare, funziona su iPhone, Android e PC, anche senza PC acceso e senza Internet.
- Contenuti: video a tutto schermo, joystick virtuale a due stick, HUD (batteria, modo, assetto, ToF, coppia stimata, RSSI, avvisi), selettori di andatura e assetto, **STOP grande sempre visibile**. Pagina tecnica: parametri, taratura, registro eventi, OTA. Gemello 3D (6.6).
- Gamepad collegato al telefono o al PC, letto dal browser (Gamepad API). Mappa come il codice Phoenix: stick sinistro avanti e di lato, destro imbardata, croce per l'altezza, un tasto per l'assetto, Select per l'andatura.
- Limite da provare: in http la Gamepad API non funziona su Firefox (vuole HTTPS dalla versione 81) e una pagina in http non si installa come app (V). Su Chrome e Safari del telefono: C. Se non va: HTTPS sul robot con certificato autofirmato, oppure app servita in https dal ponte sul PC, oppure gamepad BLE sull'ESP32.

### 3.6 Gamepad Bluetooth sull'ESP32

Dopo l'app, facoltativo: Bluepad32, che produce lo stesso `ComandoMoto` dentro il firmware. Serve per guidare senza telefono e senza rete. L'S3 parla solo BLE: vanno i controller Xbox con firmware 5 o successivo, non DualShock, DualSense e Switch Pro (V). Costi: Wi-Fi e Bluetooth si dividono la radio, quindi meno banda per il video e il risparmio del Wi-Fi forse non si spegne (3.4), e lo stack occupa decine di KB (S). Bluepad32 può impiegare 20 s ad accorgersi che il gamepad è sparito: serve un uomo morto proprio, a 0,5 s.

### 3.7 Video

- Fase 1: **MJPEG su HTTP da un secondo server sulla porta 81**, come l'esempio CameraWebServer di Espressif: uno stream bloccato non ferma i comandi. JPEG prodotto dal sensore, 2–3 buffer in PSRAM, si prende l'ultimo fotogramma, tempo del robot nell'intestazione di ogni fotogramma.
- `/foto`: istantanea fino a 2048 × 1536 per la visione e per l'LLM.
- Obiettivo: VGA a 10–20 fps con il robot in marcia (C). La OV3660 arriva a 2048 × 1536 a 15 fps (V). Latenza dalla scena allo schermo 100–250 ms (S): si misura inquadrando un cronometro.
- Dopo, solo se la latenza non basta: WebRTC con esp_peer (MJPEG su un canale dati, lo stesso collegamento porta i comandi in modo non affidabile). RTSP per VLC o ffmpeg. H.264 sull'S3 è solo software: scartato.

### 3.8 Ponte sul PC, ROS 2, registrazione

Un processo Python sul PC parla il protocollo del robot (UDP e WebSocket) ed è **l'unico punto di traduzione** verso:

- **Rerun** (libero) per vedere e riavvolgere i dati con il modello 3D; **Foxglove** facoltativo per i cruscotti dal vivo;
- **registrazioni MCAP** con i metadati (versione del firmware, hash della descrizione del robot e della taratura, scenario);
- **ROS 2**, quando servirà: `/cmd_vel`, `JointState`, `Imu`, `BatteryState`, `CompressedImage`, poi Nav2. Sul Mac ROS 2 non è supportato di prima classe: si usa RoboStack (Jazzy via pixi) o una macchina Ubuntu con Lyrical (S);
- il **server MCP** per l'LLM (3.9) e la visione pesante (capitolo 5).

micro-ROS sull'ESP32 resta un'opzione futura: servirebbe comunque l'agente sul PC, cresce la RAM, il video non ci passa e il WebSocket per l'app resterebbe. MQTT non per il controllo: più avanti, facoltativo, per mandare stato e notifiche a un sistema domotico, in sola lettura.

### 3.9 LLM

- **Server MCP nel ponte**, con strumenti di alto livello e limiti nello schema: `stato()`, `foto()`, `cammina(vx, vy, ωz, durata ≤ 5 s)`, `ruota(gradi)`, `assetto(preset, rollio, beccheggio)`, `alzati()`, `siediti()`, `fermati()`, `guarda_intorno()`; poi `vai_a(punto o stanza)`, `segui(persona)`, `esplora()`, `torna_alla_base()`, che delegano alla navigazione del PC.
- Un LLM risponde in secondi: decide obiettivi, non passi. Velocità, imbardata, ginocchio minimo e arresto restano nel firmware, quindi un suo errore non diventa una caduta.
- Primo client: Claude Code o Claude Desktop sul Mac, con il server aggiunto come MCP http (lo stesso meccanismo del connettore di Fusion), l'operatore presente e l'app aperta come uomo morto. Poi un agente proprio con l'SDK Anthropic per missioni brevi ("trova le chiavi", "controlla il corridoio"): foto, decisione, al massimo 1 m di movimento, nuova foto.
- Modello: Claude in cloud; in alternativa Gemini Robotics-ER per il ragionamento spaziale o un modello locale con Ollama sul Mac. Costo a consumo: una foto ridotta vale una frazione di centesimo (S, prezzi da ricontrollare). Le foto della casa vanno al fornitore: si decide con l'utente (domanda 6).
- Ogni chiamata si registra. Più avanti, MCP direttamente sull'ESP32 (mcp-c-sdk di Espressif) per un robot che parla con l'LLM senza PC, attraverso un proxy di casa che tiene la chiave.

## 4. Locomozione

### 4.1 Cinematica

- Zampa: forma chiusa portata da `calc/statica_tripode.py` (`ik_piano`, soluzione a ginocchio alto), con le stesse convenzioni. Terna del corpo X avanti, Y sinistra, Z su. Imbardata = direzione del piede dall'asse della coxa meno la direzione neutra (±30°, ±90°, ±150°). α sopra l'orizzontale, γ angolo interno al ginocchio. Versi del CAD: α = −G_femore, γ = 90° − G_ginocchio.
- Corpo: i piedi in terna mondo si riportano in terna corpo applicando altezza, spostamento e rotazioni del corpo. Serve per inclinarsi, abbassarsi, spostare il baricentro nel poligono d'appoggio e livellare con l'IMU.
- Cinematica diretta per i controlli. Conversione angolo → µs con la taratura.
- Le formule sono quelle di `calc/` e di `assieme.py` → `pose_tripode`: gli angoli si confrontano 1:1 nei test.

### 4.2 Generatore d'andatura

- Sei oscillatori di fase accoppiati, uno per zampa: tripode (2 gruppi, piede a terra metà ciclo), a coppie (3 coppie, 2/3), a onda (6 fasi, 5/6). Si passa da un'andatura all'altra cambiando gli sfasamenti con continuità, con i piedi a terra.
- Piede in appoggio in linea retta (o su un arco nella rotazione sul posto); in volo una curva di Bézier che parte e arriva a velocità nulla, alzata 20–30 mm. La fase si azzera quando il piede tocca terra (con i contatti).
- Assetti come preimpostazioni modificabili a caldo: 130/25, 110/40, 100/45, 80/60, 70/70 (altezza dell'asse dei femori / distanza del piede, in mm). L'assetto definitivo si sceglie a robot costruito (D-039).
- Frequenza, ampiezza e sfasamenti sono parametri esposti: è lì che agirà la politica appresa.

Coppia massima tra femore e ginocchio in % dello stallo, con 2945 g (*calcolo*: `calc/andature.py` riporta il massimo dei due giunti; femore e ginocchio separati, 100/45 e 80/60 rifatti oggi con le sue funzioni):

| Assetto | Tripode | A coppie | A onda | Giunto più caricato |
|---|---|---|---|---|
| 130/25 | 58 | 51 | 52 | ginocchio (femore 32 / 28 / 30) |
| 110/40 | 51 | 44 | 45 | ginocchio (femore 47 / 37 / 40) |
| 100/45 | 51 | **41** | 43 | femore (ginocchio 47 / 41 / 42) |
| 90/55 | 61 | 48 | 50 | femore |
| 80/60 | 66 | 52 | 54 | femore |
| 70/70 | 75 | 59 | 62 | femore |

Quindi: **andatura a coppie di base**, al meglio a 100/45; tripode per andare veloci, a 100/45 e 110/40; a onda per gli assetti bassi e i terreni difficili. Il firmware passa da solo a un'andatura con più piedi a terra quando l'assetto si abbassa o la batteria cala.

Velocità stimata in tripode a 100/45, passo 60, alzata 30 (S, conto di un ricercatore fuori dalla repo, da portare in `calc/`): 120 mm/s con un ciclo di 1,0 s (femore e ginocchio a circa 215°/s in volo); 150 mm/s con 0,8 s (circa 270°/s); con 0,6 s servirebbero 350–470°/s, più della velocità a vuoto dichiarata. Con la Bézier i picchi crescono del 20–30 %: circa 260–280°/s a 120 mm/s e 320–350°/s a 150 mm/s. **Con il limite proposto di 250°/s (2.5) il tripode arriva a circa 105–115 mm/s**; 120–150 mm/s solo se l'identificazione dei servo permette di alzarlo. A parte il limite della guardia, il vincolo vero è la coppia.

### 4.3 Adattamento al terreno

Servono IMU e contatti dei piedi (ricerca sensori).

- **Ricerca dell'appoggio**: se il piede non tocca alla quota nominale continua a scendere fino a −40 mm; se tocca prima si ferma lì. In entrambi i casi la fase si azzera. La discesa è limitata dalla coppia stimata.
- **Livellamento**: un PI su rollio e beccheggio dell'IMU agisce sull'IK del corpo e lo tiene orizzontale o parallelo al pendio.
- **Altezza** regolata sulla media delle quote d'appoggio.
- **Posa sicura** oltre la soglia d'inclinazione dell'assetto (2.6): circa 15° a 130/25, 25° a 100/45.

Sono i riflessi di Walknet e la modalità "balance" del codice Phoenix. Senza la posizione dei servo sono l'unico modo di chiudere l'anello: il contatto dice dove sta davvero il piede. Gli stessi segnali diventano ingressi della politica. Requisiti per la ricerca sensori: IMU a 6 assi a 200–400 Hz con filtro d'assetto a 50–100 Hz; 6 contatti letti ad almeno 100 Hz con latenza sotto 10 ms; corrente ad almeno 50 Hz. I 4 ingressi della SSC-32 non bastano per sei piedi.

### 4.4 Apprendimento per rinforzo

| Livello | Cosa | Dove si addestra | Dove gira |
|---|---|---|---|
| 0 | andatura classica (4.2) e riflessi (4.3) | — | ESP32 |
| 1, PMTG | politica lineare o MLP 2 × 64 che a 50 Hz modula il generatore (frequenza, alzata, altezza e inclinazione del corpo) e corregge i piedi di ±10 mm (al massimo ±15) | ARS sul Mac, 10 core | ESP32, nel ciclo |
| 2, end-to-end | MLP con due strati da 128 o GRU piccola con 0,5–1 s di storia; schema maestro-allievo (il maestro vede terreno, angoli veri e forze, l'allievo solo i sensori di bordo) | PPO in MuJoCo Playground su GPU NVIDIA in cloud | ESP32 |
| 3, percezione | ToF frontale e, se la visione la dà, una mappa d'altezza: gradini bassi, ostacoli | GPU in cloud | ESP32 più PC |

Perché si comincia dal livello 1: i servo non danno la posizione, il femore è già al 51 % e tra calcolo e movimento passano 15–50 ms (S). In queste condizioni una politica end-to-end da zero è la più difficile da portare sul robot. Le politiche che modulano un'andatura hanno già funzionato: PMTG con una politica lineare, sul Minitaur (V); Rahme et al. (2021) su OpenQuadruped, un quadrupede stampato con servo da hobby e un processore di bordo (V). Il Minitaur però ha motori brushless a presa diretta con encoder (S) e un PD sui giunti (V): per PMTG vale il metodo, non l'hardware. Un esapode da 600 $ senza retroazione dei giunti (SpiderPi di Hiwonder) ha salito le scale con lo schema maestro-allievo, ma con un Raspberry Pi a bordo, una camera di profondità Intel L515 e una camera di tracciamento T265, e la politica guardava le immagini di profondità (V): non dimostra un livello 2 che gira sull'ESP32 senza profondità. Da un robot con servo da hobby ci si aspetta più robustezza sul terreno irregolare, non più velocità.

Osservazioni: gravità proiettata e velocità angolare dall'IMU, contatti, fase dell'andatura (seno e coseno), comando, ultime 2–3 azioni, angoli stimati dall'osservatore del servo, tensione di batteria.

Ricompense: premio per l'inseguimento della velocità e dell'imbardata e per il tempo di volo dei piedi; penalità per coppia oltre il 50 % dello stallo, energia, variazioni brusche delle azioni (i servo sono lenti), rollio e beccheggio, piedi che scivolano, vicinanza ai limiti, corpo a terra. L'episodio finisce se il corpo tocca terra o l'inclinazione supera la soglia della posa sicura dell'assetto (2.6), non un valore fisso.

Randomizzazione (valori di partenza):

| Grandezza | Campo |
|---|---|
| Massa, baricentro | 2,65–3,25 kg; ±15 mm |
| Attrito | 0,4–1,2 |
| Coppia massima del servo | 80–100 % di 1,08 N·m (11 kgf·cm a 6 V), che scende verso 9,4 kgf·cm con il rail a 4,8 V |
| Velocità massima | 250–430°/s |
| Ritardo | 20–80 ms, fino a 100 (Mini Pupper 2 ne misura 76 con i suoi servo, V) |
| Banda morta, gioco | 0,1–0,5°; 0,5–1,5° (C) |
| Offset di taratura | ±2° per giunto |
| IMU, contatti | rumore e deriva; 0–20 ms di ritardo e falsi contatti |
| Terreno | rilievi fino a 20–30 mm, spinte |

Sul robot la politica ha tre modi: **ombra** (calcola e registra senza applicare), **limitato**, **pieno**. Guardia, budget di coppia e budget termico restano attivi in tutti e tre.

### 4.5 Simulatore

- **MuJoCo** (gratuito, `pip install mujoco`) sul Mac M2 Pro con 10 core e 16 GB (*verificato oggi*; MuJoCo non è ancora installato). Passo di simulazione 2 ms, politica a 50 Hz.
- Perché MuJoCo: gira nativo su macOS; dalla 3.5 gli attuatori hanno un ritardo, dalla 3.12 c'è un attuatore PID con un limite di velocità del riferimento (`slewmax`), dalla 3.7 c'è un attuatore per motori a corrente continua (`dcmotor`), riprogettato nella 3.12 (V). Insieme fanno un servo da hobby. È lo stesso motore di MuJoCo Playground e di Open Duck Mini.
- Scartati sul Mac: Isaac Lab (vuole Linux o Windows e una RTX 4080), Genesis (backend Metal senza prove di locomozione, S), Webots (non addestra in parallelo), PyBullet (poco mantenuto).
- Limite: MJX su JAX non supporta il PID né il ritardo (V). Per l'addestramento su GPU il modello del servo si scrive nell'ambiente in JAX, oppure si usa MuJoCo Warp (solo NVIDIA).
- Le funzioni nuove (PID, motore) hanno pochi mesi: si provano per prime in S0.

### 4.6 Modello dei servo senza retroazione

- In simulazione ogni servo è un attuatore PID di MuJoCo (proporzionale più smorzamento) con coppia, velocità, ritardo, banda morta e gioco randomizzati come nella tabella del 4.4.
- **Lo stesso modello gira nel firmware come "osservatore del servo"**: stima l'angolo reale dal comando e lo passa alla politica, uguale in simulazione e sul robot. Il gemello lo mostra accanto al comando.
- Perché conta: su Mini Pupper 2 (luglio 2026) un modello del servo identificato porta l'errore di previsione da 0,1–1,8 rad a 0,003–0,03 rad (V). Quei servo però restituiscono la posizione ("position-only feedback") e l'identificazione usa le posizioni misurate, che l'MG996R non dà: qui il modello si identifica da IMU, contatti e corrente (sotto), con meno precisione da aspettarsi. Il ritardo misurato lì è 76 ms (V). Open Duck Mini lo definisce il punto critico del passaggio al robot vero.
- **Identificazione senza misure dell'utente**: il robot, sul cavalletto e poi a terra, esegue gradini e sweep su un giunto alla volta e registra IMU, contatti e corrente. Le stesse sequenze girano nel simulatore; i parametri si stimano confrontando le tracce, con CMA-ES.
- Facoltativi, solo se l'utente li vuole: video al rallentatore di una leva stampata con pesi noti; un servo di scorta con un filo sul cursore del potenziometro, letto da un ADC, **solo al banco** (non torna sul robot). Una retroazione su tutti i 18 servo richiederebbe di aprirli e 18 ingressi analogici: non proposta.

### 4.7 Dove gira la politica

- **Sull'ESP32, dentro il ciclo a 50 Hz del core 1**, come codice C++ in float32 generato dai pesi: solo prodotti matrice-vettore, nessuna libreria. Vettori di prova controllano che dia gli stessi numeri dell'addestramento.
- Dimensioni (*calcolo*): MLP 60 → 64 → 64 → 18, circa 9 100 moltiplicazioni-somme; con due strati da 128, circa 26 000 parametri, 104 KB in float32: troppi per la RAM interna senza averne misurato la parte libera (2.2). Per il livello 2 i pesi vanno quantizzati in int8 (circa 26 KB) oppure in PSRAM, misurando l'effetto sul jitter. Tempo stimato da decine a centinaia di µs (S, da misurare).
- Pesi su LittleFS, identificati da un hash, caricati via HTTP; la sorgente attiva (andatura classica o politica) è un modo del firmware.
- ESP-DL o TFLite Micro solo se la rete cresce. Le GRU vanno scritte a mano (ESP-DL non le elenca, S).
- Il PC non chiude mai il ciclo dei servo, salvo nel modo LABORATORIO per provare in fretta una politica con il robot sollevato.

## 5. Visione e AI

### 5.1 A bordo dell'ESP32

| Funzione | Modello | Tempo sull'S3 | Dato |
|---|---|---|---|
| Volti | MSR + MNP, 160 × 120 | circa 43 ms, 15–20 fps sul modello | V |
| Persone | pedestrian_detect pico, 224 × 224 | 9,2 + 118,3 + 2,4 = 130 ms, più circa 16 ms di decodifica JPEG QVGA: al massimo 6,8 fps con il core tutto per sé; con `ctrl`, `sens`, streaming e PSRAM condivisa realisticamente 3–5 (S, da misurare in S5) | V tempi, S fps |
| Persona sì o no | TFLite Micro con ESP-NN, 96 × 96 | 54 ms | V |
| AprilTag e QR | apriltag-esp32 | circa 150 ms in VGA sul vecchio ESP32; sull'S3 C | S |
| Oggetti propri (per esempio una futura base di ricarica) | ESPDet-Pico addestrato con esp-detection, o FOMO | circa 100–140 ms | S |
| Decodifica JPEG → RGB565 | esp_new_jpeg | QVGA 59–66 fps, VGA 18–20 fps | V |
| Rilevatore generico (YOLO11n) | coco_detect | circa 6,2 s a 320 × 320 (15,2 + 6161,8 + 19,3 ms): **escluso** (l'S3 non ha NPU) | V |

Comportamenti a bordo, senza PC: seguire una persona, fermarsi davanti a una persona, guardare chi entra, leggere un marcatore, accorgersi di essere bloccato (marcia comandata ma immagine ferma). Sono anche il ripiego quando il Wi-Fi manca. Il rilevatore manda eventi (riquadri con classe e confidenza) al livello dei comportamenti.

Acquisizione:

- JPEG dal sensore (in RGB o YUV in PSRAM si perdono fotogrammi con il Wi-Fi attivo, V); 2 buffer; QVGA per l'uso a bordo, VGA per lo streaming; per l'inferenza si decodifica una copia ridotta (QVGA a metà scala = 160 × 120, l'ingresso del rilevatore di volti).
- **Scatto a metà appoggio**: il firmware conosce la fase del passo e scatta quando il corpo oscilla meno; scarta i fotogrammi con velocità angolare alta (IMU). Meno mosso e meno rolling shutter senza hardware in più.
- Maschera fissa per i ginocchi anteriori, che stanno al bordo dell'immagine (`progetto-meccanico.md`).
- La lente da 120° distorce molto e i modelli sono addestrati su ottiche normali: si usa il centro o si raddrizza dopo la calibrazione.
- **Prima di tutto si prova la camera**: la scheda UICPAL dà 1,2 V sul pin DVDD della OV3660, che ne dichiara 1,5 (C).
- Due modi: "streaming" senza modelli pesanti e "autonomo" con i modelli e lo streaming ridotto.

### 5.2 Fuori bordo (Mac o PC)

- **Percezione**: YOLO26 per rilevamento, segmentazione e posa; Depth Anything V2 Small metrica per interni (Apache 2.0, 24,8 milioni di parametri, V) sull'immagine raddrizzata; fusione con il ToF per dare scala e controllo (la profondità monoculare sbaglia su vetri e specchi). Latenza totale 150–300 ms (S): adatta a decidere, non ai riflessi. L'arresto davanti agli ostacoli resta a bordo, sul ToF.
- **Localizzazione**: filtro di Kalman esteso con odometria delle zampe (dal ciclo del passo), imbardata dell'IMU e correzioni assolute da marcatori AprilTag in casa. Mappa d'ingombro 2D dal ToF multizona e dalla profondità.
- **Navigazione**: Nav2 con il controllore MPPI in modello omnidirezionale, perché l'esapode va anche di lato.
- **Esperimento**: ORB-SLAM3 monoculare-inerziale con il modello fisheye (GPLv3, poco mantenuto). Lo SLAM monoculare su un robot che cammina, con rolling shutter e 120° di campo, è fragile: per questo prima i marcatori.
- **Calibrazione**: fisheye con una scacchiera ChArUco stampata; camera–IMU con Kalibr, che stima anche lo sfasamento temporale. Serve la testa della camera bloccata nella torretta: se si muove, la calibrazione va rifatta.
- Lo stesso codice girerà sull'eventuale computer di bordo: YOLO26 si esporta per le NPU Rockchip.

### 5.3 Agente

È il livello più alto (3.9): compiti in linguaggio naturale, una mappa semantica di stanze e oggetti, il recupero dagli errori, a 0,2–1 decisioni al secondo. Si cambia modello senza toccare il robot. I modelli visione-linguaggio-azione end-to-end (per esempio Gemini Robotics 1.5) non sono adatti ora: chiedono un controllo a basso livello appreso e hanno accesso limitato.

### 5.4 Computer di bordo: sì o no

Femore al punto 100/45 calcolato oggi con `calc/statica_tripode.py` aggiungendo la massa; masse e potenze da fonti dei ricercatori (S).

| Opzione | Massa in più | Potenza | Femore | Esito |
|---|---|---|---|---|
| Nessuno (oggi) | 0 | 0 | 51,4 % | **scelta per ora** |
| Radxa ZERO 3W 4 GB (RK3566, NPU 0,8 TOPS, formato 65 × 30) | circa 40 g | 2–4 W | 52,1 % | **predisporre, comprare solo se serve** |
| Raspberry Pi Zero 2 W | circa 10–20 g | 0,4–1,4 W | circa 51,7 % | senza NPU e con 512 MB: solo inoltro dei dati |
| Pi 5 con AI HAT+ 2 (Hailo-10H) | circa 130 g | 5,5–13,5 W, alimentazione 5 V 5 A | 53,6 % | solo come zaino sperimentale |
| Jetson Orin Nano Super | circa 210 g | 7–25 W, ingresso 9–19 V | 55,0 % | **scartato** |

- Energia: 2–4 W contro 69–82 W in marcia, circa 1–2 minuti di autonomia in meno (S). Il Pi 5 con l'acceleratore ne toglie il 10–15 % (S).
- Collegamento: un cavo USB corto dalla porta OTG dell'ESP32, che si presenta come webcam UVC (la OV3660) e come seriale CDC (comandi e telemetria). Il dispositivo composto UVC più CDC è da provare (C). Banda della USB full speed: circa 0,5–1 MB/s, cioè VGA MJPEG a 12–25 fps (S).
- **Il computer di bordo non comanda mai la SSC-32**: l'ESP32 resta il controllore in tempo reale e la guardia resta lì.
- Spegnimento: l'ESP32 chiede l'arresto via CDC e aspetta la conferma prima di spegnere l'interruttore. Sistema su eMMC o con radice in sola lettura, contro la corruzione quando si stacca la batteria.
- Prestazioni della NPU RK3566 molto variabili nei forum (2–15 fps su YOLOv5s, S): si misurano prima di contarci. Piano B: schede RK3588S (6 TOPS, 5–10 W, 50–70 g, S).
- **Criterio per comprarlo** (dopo S6): il Wi-Fi di casa non regge video e latenza per i comportamenti voluti, oppure si vuole autonomia senza PC acceso, e il budget di coppia lo consente (per esempio dopo aver alleggerito il guscio della tibia, circa −20 g, D-063).

### 5.5 Privacy

- Locale per default: nessuna registrazione salvata senza un comando; streaming solo nella rete di casa, con token, nessuna porta aperta su Internet (da fuori, una VPN).
- Cloud solo su richiesta, con fotogrammi ridotti e volti sfocati a bordo dal rilevatore dell'ESP32.
- LED di camera attiva acceso quando il sensore manda immagini.
- Eventuali impronte dei volti dei familiari (dati biometrici): solo sul robot o sul PC, cifrate e cancellabili.
- Perché: per il Garante le telecamere usate in casa a fini personali sono fuori dal GDPR finché le immagini restano negli spazi propri e non vanno a terzi; restano esclusi aree comuni, bagni, e vanno informati colf e babysitter (V). L'AI Act non si applica agli usi personali (art. 2, par. 10, V). Mandare immagini a un servizio cloud è comunicazione a terzi: deve essere una scelta esplicita.

## 6. Strumenti, struttura della repo, test e gemello digitale

### 6.1 Struttura della repo

Tutto in questa repo: un commit lega CAD, firmware, taratura e registrazioni.

```
robot/              robot.yaml (unica fonte: geometria, limiti, tabella del ginocchio, canali, versi, masse)
                    cad.json (esportato da Fusion), mesh/ per segmento, calib/<robot>.yaml
proto/              hexapod.proto (unico schema dei messaggi)
firmware/           progetto ESP-IDF: main/, components/nucleo (C++ puro), ssc32, potenza, sicurezza,
                    sensori, camera, visione, politica, comandi, rete, telemetria, config, ota;
                    test_host/, test_target/, partitions.csv, sdkconfig.defaults
app/                web app (TypeScript, three.js), copiata nell'immagine LittleFS
sim/                modello MJCF generato, ambienti MuJoCo, emulatore della SSC-32, ponte SIL e HIL
tools/              genera_robot.py; hexa (banco, taratura, flash e OTA, registra, riproduci, sysid);
                    ponte (Rerun, MCAP, ROS 2, MCP)
tests/              pytest; dati/ con i vettori esportati dal CAD
calc/               resta; legge i numeri da robot/robot.yaml
cad/script/         in più esporta_robot.py (sola lettura)
.github/workflows/  ci.yml
```

Linguaggi: C++17 per il firmware, Python 3.12 per strumenti, generatori, simulazione e test (già sul Mac con numpy), TypeScript per l'app. Mancano ESP-IDF, MuJoCo e Node.js (*verificato oggi*).

La repo è **pubblica** su GitHub (*verificato oggi*): credenziali Wi-Fi e chiavi mai in git (stanno in NVS; `sdkconfig` locale ignorato); registrazioni e video fuori da git (cartella locale ignorata o allegati alle release).

### 6.2 Una sola descrizione del robot

- `cad/script/esporta_robot.py`, script Fusion **in sola lettura** sullo schema di `esporta_mesh.py`, scrive `robot/cad.json`: parametri utente (`zam_Lc`, `zam_Lf`, `zam_Lt`, `cor_ang_x`, `cor_ang_y`, `cor_med_y`, `cor_ang_dir`), origini, assi e limiti dei giunti (`G_coxa_*`, `G_femore`, `G_ginocchio`), massa, baricentro e inerzia di ogni segmento (parti stampate con il fattore di riempimento del progetto meccanico, comprate con la massa dichiarata), mesh di una zampa e del corpo nella terna di ogni segmento, tabella del ginocchio minimo. Ogni chiamata sotto i 40 s.
- `tools/genera_robot.py` produce:
  - l'header `constexpr` del firmware e il modulo Python per `calc/`;
  - **URDF** per il gemello nel browser e per Rerun (e ROS 2);
  - **MJCF** per MuJoCo: collisioni con primitive (scatola e cilindri per il corpo, capsule per femore e tibia, sfera per il piede), mesh solo visive, attuatori dei servo, un punto per l'IMU, sensori di contatto ai piedi.
- I generatori generici non si usano: fusion2urdf modifica il design e vuole componenti non annidati; qui la zampa è un sotto-assieme istanziato sei volte con i giunti di coxa alla radice (limiti dell'API in `CLAUDE.md`). ACDC4Robot resta un controllo incrociato.
- Il ginocchio minimo che dipende dal femore non si scrive in URDF: resta una tabella, applicata dalla guardia identica in simulazione, più una penalità nella ricompensa.
- Massa da distribuire: 2583 g modellati più circa 360 non modellati (cavi e viteria). Le masse delle parti stampate si sostituiscono con quelle dello slicer e con la pesata.
- Il CI rigenera tutto e fallisce se i file generati differiscono da quelli nel commit, o se l'hash di `robot.yaml` non corrisponde a quello di `cad.json`.

### 6.3 Test

1. **IK e cinematica diretta**, andata e ritorno su una griglia dello spazio dei giunti.
2. **CAD come oracolo**: `esporta_robot.py --pose` muove i giunti veri su circa 50 pose e legge la punta del piede. Cinematica diretta in Python e in C++ entro 0,05 mm (tolleranza da tarare).
3. **Pose verificate in Fusion** (ciclo a tripode 100/45, 130/25, 80/60, 70/70; rotazione sul posto di 30°): devono passare la guardia.
4. **Casi d'urto del CAD** (femore a −60°, vicine a 40°, ginocchio sotto la tabella): la guardia li deve rifiutare.
5. **Regole del firmware**: imbardata, somma tra vicine, ginocchio minimo più 3° con l'interpolazione prudente, velocità.
6. **Regressione della statica**: femore al 51 % ± 1 a 100/45 (oggi 5,65 kgf·cm) e margine di stabilità 59 mm (*verificato oggi*).
7. **Andature**: niente salti tra fasi e transizioni, piedi in appoggio fermi entro 0,5 mm, nucleo C++ uguale al Python entro 0,01° sugli stessi vettori.

L'esportazione delle pose da Fusion si rifà a ogni cambio di zampa o corpo: è un passo in più nella procedura del CAD.

### 6.4 Integrazione continua (GitHub Actions)

| Job | Cosa fa |
|---|---|
| `python` | ruff e pytest (`calc/`, descrizione del robot, cinematica, statica) |
| `nucleo` | CMake e ctest del nucleo sul PC con controlli di memoria; framework Unity, lo stesso dei test sul chip |
| `firmware` | build con l'azione ufficiale di Espressif (versione fissata, target esp32s3), controllo della dimensione, binari allegati |
| `qemu` | una configurazione dedicata del firmware, con camera, rete e sensori simulati, si avvia in QEMU, stampa la versione e in uno scenario scritto emette i comandi attesi per la SSC-32. Prova la macchina a stati e il nucleo, non lo stack completo |
| `sim` | rigenera l'MJCF e fa 20 s di andatura in SIL con asserzioni |
| `app` | build e controllo della dimensione |
| `generati` | i file generati devono coincidere con quelli nel commit |

Gratuito per le repo pubbliche (V). Le prove HIL **non** girano in Actions: GitHub sconsiglia i runner sul proprio computer per le repo pubbliche, perché una PR da un fork potrebbe eseguire codice sul Mac con il robot collegato (V). Si lanciano in locale e l'esito si registra nella repo. Un job non bloccante con la versione successiva dell'IDF avvisa in anticipo delle migrazioni. Il QEMU di Espressif per l'S3 emula la UART ma non Wi-Fi, Bluetooth, USB, I2C, RMT né la matrice dei GPIO (V): il firmware vero, con camera (SCCB su I2C), Wi-Fi e UART1 instradata sui GPIO 21/14, lì non si avvia così com'è. La UART1 è da verificare: se manca, la prova d'avvio usa la console.

### 6.5 Prove SIL e HIL attorno alla SSC-32

- **Emulatore Python della SSC-32** (`sim/ssc32_emu.py`): comandi ASCII e binari, `Q`, `QP`, interpolazione dei gruppi, impulsi ogni 20 ms, uscita verso MuJoCo. Le risposte vere del clone, registrate in S1, diventano i suoi dati di prova.
- **SIL in CI**: il nucleo compilato per il PC comanda emulatore e MuJoCo. 20 s di tripode: non cade, nessun urto, piedi che non scivolano, coppia simulata sotto il 60 % dello stallo.
- **HIL al banco**: ESP32 vero con il firmware vero compilato con `HIL=1`; i comandi della SSC-32 escono sulla USB nativa, i sensori arrivano dal PC tramite il backend simulato, la console resta sulla CH340. Si provano sul silicio tempi dei compiti, Wi-Fi, app e telemetria, senza rischiare i servo.

### 6.6 Gemello digitale

Un solo modello generato, in tre forme:

- **Cinematico nel browser**, dentro l'app servita dal robot: three.js con urdf-loader. Mostra la posa comandata, la posa prevista dal modello del servo e, quando ci sarà, l'assetto dall'IMU. Con il modo OMBRA il firmware gira completo a rail spento e si vede cosa farebbe il robot. L'app deve dire chiaramente che sono pose comandate o previste, non misurate.
- **Fisico in MuJoCo**: SIL, regressione, identificazione dei servo, RL.
- **Rerun** per rivedere le registrazioni con il modello 3D.

Servire l'app dal robot evita anche un blocco dei browser: una pagina https (per esempio su GitHub Pages) non può aprire un WebSocket non cifrato verso il robot (S, da MDN). Modelli 3D compressi sotto 1–2 MB (S).

### 6.7 Procedure di banco

Script `tools/hexa banco` più una lista di controllo, un elemento nuovo alla volta, così un guasto ha una sola causa possibile.

| Passo | Cosa | Si controlla |
|---|---|---|
| B0 | solo ESP32 su USB, regolatori scollegati | flash, LED, ADC su GPIO1 con il partitore, GPIO42 con il multimetro |
| B1 | SSC-32 comandata dal PC, logica da 2S attraverso F2, ponticello VS-VL tolto | versione, baud, comandi ASCII e binari; risposte registrate per l'emulatore |
| B2 | un servo alla volta, senza carico, rail a 6 V con fusibile da 3 A o alimentatore limitato a 1 A | verso, escursione da 1500 ± 100 µs poi più ampia, mai contro il fermo; servo etichettati, difettosi scartati |
| B3 | catena di potenza | abilitazione bassa = 0 V; GPIO42 alto = 6,0 V e power-good; poi un lato con 9 servo, F1 da 15 A |
| B4 | calettamento delle squadrette | servo a metà corsa, dente più vicino all'angolo di progetto, residuo entro ±7,2° |
| B5 | una zampa sul cavalletto | limiti, tabella del ginocchio, taratura con le dime |
| B6 | robot sul cavalletto con le zampe in aria, poi a terra in assetto basso | andatura in aria, poi alzarsi e sedersi |

Sempre attivi: limite di velocità, tempo massimo di sforzo, battito dal PC (300 ms), arresto da app, pulsante e T-plug.

## 7. Roadmap

Fasi software S0…S9 (S per non confonderle con le fasi meccaniche di `CLAUDE.md`). S0 non chiede hardware e può partire subito, in parallelo con il CAD.

0. **S0 — Fondamenta senza hardware.** Scheletro della repo; `robot.yaml`, `esporta_robot.py` e generatori; nucleo C++ (IK, guardia, oscillatori, modello del servo); vettori di prova dal CAD; gemello nel browser che riproduce le andature di `calc/`; modello MuJoCo con l'andatura a comandi aperti; CI.
   *Si verifica*: nucleo uguale a `calc/` entro 0,01° e al CAD entro 0,05 mm; le pose del ciclo verificate in Fusion passano la guardia, i casi d'urto no; 20 s di tripode in SIL senza cadute; file generati allineati.
1. **S1 — Banco dell'elettronica.** Versione dell'IDF (camera ed ESP-DL compilano?); OV3660 con il DVDD a 1,2 V; SSC-32: baud, `VER`, `Q`, `QP`, `STOP`, `P0`, ingressi, modo binario, 230400; tempi e jitter letti con l'RMT su GPIO38, prima dell'audio; un MG996R alimentato senza impulsi; corrente a 5 V di ESP32, camera e Wi-Fi; bus dei sensori dedicato (GPIO47/3) con i primi sensori, se arrivano; 3V3 della scheda con ToF e Wi-Fi accesi.
   *Si verifica*: formato e baud scelti; fps della camera in JPEG; campo reale della lente e ginocchi nell'immagine.
2. **S2 — Firmware di base e una zampa.** Macchina a stati, rail e sequenza d'accensione, misura di batteria, watchdog, console, prima app, telemetria, taratura con le dime, OTA con ritorno; HIL sul Mac senza servo.
   *Si verifica*: accensione senza scatti; rail spento in ogni guasto provato (SSC-32 staccata, firmware bloccato, batteria simulata bassa); taratura ripetibile entro 1°.
3. **S3 — Robot completo in guida manuale.** In piedi, seduto, andatura a coppie e tripode a 100/45 dal telefono; registrazione MCAP; scatola nera; perdita del collegamento; jitter del ciclo con il video acceso.
   *Si verifica*: jitter sotto 1 ms al 99,9° percentile con camera e streaming; uomo morto a 300 ms e seduta a 30 s; latenza del comando misurata; velocità e consumo per assetto.
4. **S4 — Sensori e andature adattive.** IMU (livellamento, caduta), contatti (ricerca dell'appoggio, azzeramento della fase), corrente; scelta dell'andatura dal budget di coppia; transizioni; assetti da 130/25 a 70/70; budget termico; identificazione dei servo e taratura di MuJoCo sui registri.
   *Si verifica*: tappetini, libri e pendenze senza cadute; robot e simulatore sulle stesse sequenze con tracce di IMU e corrente vicine (criterio da fissare sui primi dati).
5. **S5 — Visione a bordo.** Streaming al PC; persone e volti con ESP-DL; AprilTag; scatto a metà appoggio; "seguimi", "fermati davanti a una persona", "sono bloccato"; arresto davanti agli ostacoli con il ToF.
   *Si verifica*: fps reali con passo, Wi-Fi e camera insieme, senza superare il jitter di S3.
6. **S6 — Cervello esterno.** Ponte Python, Rerun, protocollo v1 congelato; percezione sul PC (YOLO26, profondità, ToF); calibrazione fisheye e camera–IMU; ponte ROS 2 se voluto; server MCP con Claude Code e l'operatore presente.
   *Si verifica*: latenze e fps della percezione; ogni chiamata dell'LLM registrata e contenuta dai limiti; STOP sempre efficace.
7. **S7 — Apprendimento, livello 1 (PMTG).** Politica addestrata con ARS sul Mac con la randomizzazione; esportata in C++; ombra, poi limitato, poi pieno.
   *Si verifica*: contro la sola andatura classica, a parità di percorso, cadute, velocità ed energia (dalla corrente).
8. **S8 — Autonomia in casa.** Kalman con odometria delle zampe, IMU e AprilTag; mappa d'ingombro; Nav2 con MPPI; mappa semantica; agente con l'SDK Anthropic (o locale) per missioni brevi; decisione sul computer di bordo con il criterio del 5.4.
   *Si verifica*: missioni ripetute (andare in una stanza, tornare) con il tasso di riuscita e gli interventi dell'operatore contati.
9. **S9 — Apprendimento, livelli 2 e 3.** Politica end-to-end maestro-allievo su GPU in cloud, poi con il ToF e la profondità; eventuale computer di bordo nel vano predisposto (UVC più CDC, YOLO sulla NPU, ROS 2 a bordo).
   *Si verifica*: prima in SIL, poi HIL, poi sul robot in ombra; confronto con il livello 1 su gradini bassi e ostacoli; autonomia senza PC se c'è il computer di bordo.

## 8. Impatto su CAD, elettronica e BOM

### CAD (da predisporre ora)

| Cosa | Dove | Perché |
|---|---|---|
| Dime di taratura generate dai parametri: coxa 0° e +30°, femore 0° e +45°, ginocchio 90° e 135° | parti nuove | taratura a due punti; seguono le modifiche della zampa |
| Facce di riferimento libere per le dime, tacche | coxa, femori, tibia | appoggio ripetibile delle dime |
| Cavalletto da banco: corpo appoggiato sotto la chiglia, zampe libere su tutta l'escursione | parte nuova | B5, B6, identificazione, modo LABORATORIO |
| Punti di riferimento con nome: punta del piede, IMU, assi dei giunti | `zampa.py`, `assieme.py` | esportazione senza dedurre nulla |
| `esporta_robot.py` | `cad/script/` | sola lettura, nessuna modifica al design |
| Testa della camera bloccata nella torretta, posizione e orientamento come parametri | vassoio | calibrazione stabile, VIO |
| Sede dell'IMU, terna nota | tetto del tunnel sotto il vassoio, `Corpo_Base` (`predisposizioni.md` X4) | rigida con la base; camera–IMU si ricalibra dopo ogni smontaggio del vassoio |
| Sede del ToF sotto l'occhio, sullo stesso piano verticale della camera | mensola del vassoio e finestra nella visiera (`predisposizioni.md` X8) | abbinare distanze e rilevamenti |
| Guida di luce dal WS2812 della scheda (GPIO48) verso la visiera | visiera o fascia | solo se la catena LED (`predisposizioni.md` X9, X11) non si fa: modo del robot e "camera attiva" |
| Vano del computer di bordo circa 70 × 35 × 15 mm, bugne M2,5 sul passo 58 × 23, feritoie nel carapace, passaggio per un cavo USB-C a 90° | **posto da trovare**: sotto il dorso restano 9,2 mm sopra le spine della SSC-32 e circa 13,6 sopra l'ESP32 (`predisposizioni.md` 2.8), e la zona è contesa da scheda del carapace e amplificatore | predisposizione; ripiego: zaino esterno sul dorso, come quello del Pi 5 |
| Leva di prova (facoltativa) | parte nuova | identificazione con il video, solo se l'utente la vuole |

Circa 5 g di stampa in più sul robot (S); dime, cavalletto e leva non stanno sul robot. Farle dopo vorrebbe dire ristampare base, vassoio o carapace.

### Elettronica

| Cosa | Perché |
|---|---|
| Filo RX dalla SSC-32 collegato (già in D-012) e un connettore di prova con TX, RX e massa sulla basetta | risposte della SSC-32; ascolto della linea con un adattatore |
| Canale libero del traslatore C1 verso GPIO38, solo al banco e prima dell'audio | misura con l'RMT dell'impulso di un canale libero della SSC-32; GPIO47 resta a un solo uso, il bus dei sensori (capitolo 1) |
| 100 kΩ verso massa su GPIO41, se il pin OFF della 2813 scatta con il GPIO flottante (C) | spegnimenti non voluti all'avvio |
| GPIO19 e 20 riservati alla USB OTG | debug, HIL, poi computer di bordo |
| Bus I2C dei sensori dedicato su GPIO47/3 | scelto in `predisposizioni.md` 2.2; il firmware tiene il bus condiviso come riserva |
| Margine sul 5 V: il D24V22F5 (2,5 A) basta per ESP32 e LED; con la Radxa o la Pi Zero serve un secondo regolatore 5 V da 3 A e F2 va rivisto. Lo "zaino" Pi 5 con AI HAT+ 2 (fino a 13,5 W, alimentazione dichiarata 5 V 5 A) chiede un'alimentazione propria | predisporre lo spazio, non comprare |
| Antenna: controllare sulla scheda quale antenna è attiva (spesso un resistore da 0 Ω) | se servirà la C8 |

### BOM

**Niente da comprare adesso.** Voci candidate, ciascuna da approvare:

| Voce | Stato proposto | Costo indicativo |
|---|---|---|
| Adattatore USB-seriale a 3,3 V (CH340 o CP2102) per ascoltare la linea ESP32–SSC-32 | da approvare, facoltativo | circa 5 € (S) |
| Fusibili a lama da 3 A e 5 A per il banco | da aggiungere all'assortimento B4 | pochi euro |
| Alimentatore da banco con limite di corrente | già "utile, non indispensabile" negli attrezzi | — |
| Gamepad BLE (Xbox con firmware 5 o successivo) | ? solo se non ne hai uno e lo vuoi | — |
| Regolatore 5 V da 3 A per il computer di bordo (Radxa o Pi Zero, non il Pi 5) | — non comprare per ora | — |
| Radxa ZERO 3W 4 GB | — non comprare per ora | — |
| GPU in cloud per l'addestramento end-to-end | a consumo: Colab gratuito per le prove, noleggio per le corse lunghe | da approvare |
| API di un LLM | a consumo | da approvare |
| Marcatori AprilTag | stampati su carta | — |

Software gratuito e libero da installare (da approvare): ESP-IDF con esp32-camera, esp-dl, esp-dsp, led_strip, nanopb; MuJoCo; pytest e ruff; Rerun e mcap; three.js con urdf-loader, Vite e Node.js; OpenCV; più avanti Bluepad32, ROS 2 via RoboStack, l'SDK MCP e l'SDK Anthropic.

## 9. Rischi, domande, fonti

### Rischi principali

| Rischio | Effetto | Contromisura |
|---|---|---|
| Il clone della SSC-32 non ha modo binario, `QP`, ingressi o baud diversi da 115200 | ciclo a 115200 senza margine, niente controllo dei valori | prova in S1 prima di scrivere il driver; ripiego a 25 Hz con T = 40 ms |
| Servo senza retroazione | posa reale diversa dal comando sotto carico; politica che fallisce sul robot | guardia, osservatore del servo, contatti e IMU, identificazione, PMTG prima dell'end-to-end |
| Margine di coppia scarso (51 %) | stalli, calore, cali del rail | andatura a coppie di base, budget di coppia e termico, niente massa in più a bordo |
| Jitter da PSRAM condivisa tra camera, ESP-DL e ciclo | passo irregolare | ciclo in RAM interna, misura in S3, inferenza rallentata o spostata |
| Wi-Fi di casa debole sotto il carapace | video e comandi a scatti | comandi che scadono, comportamenti a bordo, antenna C8, computer di bordo come ultima strada |
| OV3660 con il DVDD a 1,2 V | camera instabile o muta | prova in S1 prima di tutto il resto della visione |
| Taratura sbagliata di più di 3° | il margine sul ginocchio minimo e tra le coxe vicine non basta | dime, taratura a due punti, hash controllato all'avvio |
| ESP-IDF 6 e componenti esterni | build che non compila | prova in S1, ripiego su 6.0 o 5.5 |
| Funzioni nuove di MuJoCo (PID, ritardo) | modello del servo non usabile | prova in S0, ripiego sul modello scritto nell'ambiente |
| Calore sotto il carapace in PLA (rammollisce verso 55–60 °C) | ESP32 o computer di bordo surriscaldati | misura in S3 con Wi-Fi, camera e inferenza; feritoie |
| LLM che fraintende scena o distanze | movimenti sbagliati | limiti nel firmware, durata massima, STOP, operatore presente all'inizio |
| Privacy | immagini di casa a terzi | locale per default, cloud solo su richiesta con volti sfocati |
| Troppo lavoro per una persona sola, con finestre d'uso limitate | progetto che si arena | fasi piccole che lasciano la repo in uno stato da cui ripartire; ogni fase ha la sua verifica |

### Domande per l'utente

Le prime quattro servono per partire con S0.

1. Approvi l'architettura a tre livelli (ESP32 autonomo, PC facoltativo, computer di bordo solo predisposto)?
2. Firmware in ESP-IDF e C++, senza Arduino: va bene? Costa più lavoro all'inizio, ma rende più semplici camera, AI e tempi del ciclo.
3. Posso installare sul Mac il software gratuito elencato nel capitolo 8 (ESP-IDF, MuJoCo, Rerun, Node.js e il resto)?
4. La repo è pubblica: va bene pubblicare anche firmware e registrazioni (le credenziali restano fuori), oppure la rendiamo privata? Da privata Actions dà 2000 minuti al mese (S).
5. Oltre al Mac M2 Pro hai un PC con una GPU NVIDIA? Ti interessa una macchina Linux sempre accesa (un acquisto da approvare)?
6. Per l'LLM va bene un servizio cloud (Claude), a consumo e con le foto della casa inviate al fornitore, o preferisci solo modelli locali?
7. Il telefono è un iPhone o un Android? Cambiano gamepad nel browser e nomi `.local`.
8. Hai un gamepad Bluetooth, e quale? Sull'ESP32-S3 vanno solo i BLE (Xbox con firmware aggiornato sì, PlayStation e Switch no).
9. Il robot userà solo il Wi-Fi di casa o anche fuori (per esempio con l'hotspot del telefono)?
10. ROS 2 è un obiettivo in sé (imparare, RViz, Nav2) o basta il ponte finché non serve?
11. Predispongo nel CAD il vano del computer di bordo, le dime di taratura, il cavalletto e le sedi di IMU e ToF? La guida di luce solo se la catena LED non si fa. Circa 5 g sul robot, nessun acquisto.
12. Al banco posso cambiare baud e registri della SSC-32? Sono scritture in EEPROM, reversibili con il pulsante BAUD.
13. Hai servo di scorta? Uno potrebbe servire per l'identificazione al banco (con un filo sul potenziometro non tornerebbe sul robot). Il video della leva è facoltativo e non è una misura che ti chiedo.
14. Cosa conta di più: robustezza sul terreno irregolare (contatti, andatura a coppie) o velocità su piano (tripode: circa 105–115 mm/s con il limite proposto di 250°/s per giunto, 120–150 mm/s solo alzandolo dopo l'identificazione dei servo)?
15. Confermi che non servono firma degli aggiornamenti e cifratura della flash? Sono irreversibili sull'ESP32.
16. Riconoscimento dei volti dei familiari, marcatori AprilTag su muri o mobili, spia di camera attiva (un pixel della catena LED, `piano-elettronica-software.md` 2.6): quali vuoi?
17. L'app la vuoi in italiano?

### Fonti

Indicate dai ricercatori il 9 ottobre 2026; i numeri marcati V vengono da queste pagine.

Espressif:

- [ESP-IDF v6.1: versioni e supporto](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/versions.html), [politica di supporto](https://github.com/espressif/esp-idf/blob/master/SUPPORT_POLICY.md), [annuncio della v6.0](https://developer.espressif.com/blog/2026/03/idf-v6-0-release/)
- [FreeRTOS nell'IDF (FPU, core)](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-reference/system/freertos_idf.html), [prestazioni e priorità](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-guides/performance/speed.html), [flash e cache](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-reference/peripherals/spi_flash/spi_flash_concurrency.html), [RAM esterna](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/external-ram.html)
- [OTA](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-reference/system/ota.html), [core dump](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-guides/core_dump.html), [watchdog](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-reference/system/wdts.html), [calibrazione dell'ADC](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-reference/peripherals/adc_calibration.html), [NVS](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-reference/storage/nvs_flash.html)
- [Wi-Fi: prestazioni e risparmio](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32s3/api-guides/wifi-driver/wifi-performance-and-power-save.html), [coesistenza Wi-Fi e Bluetooth](https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32s3/api-guides/coexist.html), [forum: risparmio del Wi-Fi con il Bluetooth](https://esp32.com/viewtopic.php?p=99823), [server HTTP](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/protocols/esp_http_server.html), [QEMU](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-guides/tools/qemu.html), [QEMU di Espressif, periferiche emulate](https://github.com/espressif/esp-toolchain-docs/blob/main/qemu/README.md), [tipi di memoria dell'S3](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/memory-types.html)
- [Datasheet ESP32-S3](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)
- [esp32-camera](https://github.com/espressif/esp32-camera), [esp_cam_sensor](https://components.espressif.com/components/espressif/esp_cam_sensor), [esp-webrtc-solution](https://github.com/espressif/esp-webrtc-solution), [soluzioni camera](https://docs.espressif.com/projects/esp-techpedia/en/latest/esp-friends/solution-introduction/camera/dvp-mipi-csi-camera-solution.html)
- [esp-dl](https://github.com/espressif/esp-dl), [pedestrian_detect](https://components.espressif.com/components/espressif/pedestrian_detect), [human_face_detect](https://components.espressif.com/components/espressif/human_face_detect), [coco_detect](https://components.espressif.com/components/espressif/coco_detect/versions/0.4.0/readme), [esp-detection](https://github.com/espressif/esp-detection), [esp-who](https://github.com/espressif/esp-who), [esp_new_jpeg](https://components.espressif.com/components/espressif/esp_new_jpeg/versions/1.0.2/readme), [esp-tflite-micro](https://github.com/espressif/esp-tflite-micro), [esp-nn](https://components.espressif.com/components/espressif/esp-nn), [esp-dsp](https://github.com/espressif/esp-dsp)
- [usb_device_uvc](https://components.espressif.com/components/espressif/usb_device_uvc), [mcp-c-sdk](https://components.espressif.com/components/espressif/mcp-c-sdk), [micro-ROS per ESP-IDF](https://components.espressif.com/components/micro-ros/micro_ros_espidf_component), [esp-idf-ci-action](https://github.com/espressif/esp-idf-ci-action), [pytest-embedded](https://github.com/espressif/pytest-embedded)

SSC-32, servo, codice Phoenix:

- [Guida della SSC-32U (PDF)](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf), [comandi binari della SSC-32](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/servo-erector-set-system/ses-electronics/ses-modules/ssc-32/ssc-32-binary-commands), [forum: Q e QP](https://community.robotshop.com/forum/t/ssc32-query-commands/16113), [forum: QP durante un movimento](https://community.robotshop.com/forum/t/pulse-width-query-in-real-time/14411), [forum: ritardo della risposta a Q](https://community.robotshop.com/forum/t/q-command-problem/15884), [forum: offset PO](https://community.robotshop.com/forum/t/pulse-width-offset/16638)
- [Codice Phoenix (KurtE)](https://github.com/KurtE/Arduino_Phoenix_Parts), [Phoenix di Lynxmotion](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-v1/ses-v1-robots/ses-v1-3-4-dof-hexapods/phoenix/)
- [Datasheet AZDelivery MG996R](https://cdn.shopify.com/s/files/1/1509/1638/files/Servo_MG996R_Datenblatt.pdf), [Tower Pro MG996R](https://www.towerpro.com.tw/product/mg996r/), [Adafruit 757 (BSS138)](https://www.adafruit.com/product/757)

Locomozione, simulazione, apprendimento:

- [MuJoCo: riferimento XML](https://mujoco.readthedocs.io/en/stable/XMLreference.html), [novità](https://mujoco.readthedocs.io/en/stable/changelog.html), [MJX](https://mujoco.readthedocs.io/en/stable/mjx.html), [MuJoCo Playground](https://github.com/google-deepmind/mujoco_playground) e [articolo](https://arxiv.org/abs/2502.08844)
- [Ijspeert 2008, CPG](https://doi.org/10.1016/j.neunet.2008.03.014), [CPG-RL](https://arxiv.org/abs/2211.00458), [Walknet](https://link.springer.com/article/10.1007/s00422-013-0563-5), [PMTG](https://arxiv.org/abs/1910.02812), [Rahme et al., politiche lineari su un quadrupede economico](https://robotics.northwestern.edu/research/publications/linear-policies-are-sufficient-to-enable-low-cost-quadrupedal-robots-to-traverse-rough-terrain.html), [esapode con schema maestro-allievo](https://arxiv.org/abs/2412.10628), [addestramento parallelo massivo](https://arxiv.org/abs/2109.11978)
- [Hwangbo et al., rete dell'attuatore](https://arxiv.org/abs/1901.08652), [Residual Policy Learning](https://arxiv.org/abs/1812.06298), [Mini Pupper 2, modello dei servo](https://arxiv.org/abs/2607.26434), [BAM](https://github.com/Rhoban/bam) e [articolo](https://arxiv.org/abs/2410.08650), [Open Duck Mini, dalla simulazione al robot](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/sim2real.md), [SpotMicroAI](https://spotmicroai.readthedocs.io/en/next/gettingStarted/)
- [Isaac Lab](https://isaac-sim.github.io/IsaacLab/release/3.0.0/source/setup/installation/index.html), [requisiti di Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html), [Genesis](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/what_is_genesis.html), [spot_mini_mini](https://github.com/OpenQuadruped/spot_mini_mini), [fusion2urdf](https://github.com/syuntoku14/fusion2urdf), [ACDC4Robot](https://github.com/ACDC4Robot/Fusion360)

Visione, navigazione, computer di bordo, agente:

- [Ultralytics e NPU Rockchip](https://docs.ultralytics.com/integrations/rockchip-rknn), [Depth Anything V2 metrica per interni](https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-Indoor-Small-hf), [Depth Anything 3](https://blog.roboflow.com/depth-anything-3/), [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3), [Nav2 MPPI](https://docs.nav2.org/rolling/configuration_and_development/configuration_guide/controller_plugins/mppi_controller/configuring_mppic/), [Kalibr](https://github.com/ethz-asl/kalibr), [apriltag-esp32](https://github.com/raspiduino/apriltag-esp32), [VL53L5CX](https://www.st.com/en/imaging-and-photonics-solutions/vl53l5cx.html)
- [Radxa ZERO 3](https://docs.radxa.com/en/zero/zero3), [YOLOv5 sulla NPU (Q-engineering)](https://github.com/Qengineering/YoloV5-NPU), [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/), [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/), [AI HAT+ 2 (heise)](https://heise.de/-11136612), [Jetson Orin Nano Super](https://www.kiwi-electronics.com/en/single-board-computers-390/nvidia-jetson-orin-nano-super-developer-kit-11461)
- [Claude, visione](https://platform.claude.com/docs/en/build-with-claude/vision), [specifica MCP, strumenti](https://modelcontextprotocol.io/specification/2025-11-25/server/tools), [Gemini Robotics-ER 1.5](https://developers.googleblog.com/en/building-the-next-generation-of-physical-agents-with-gemini-robotics-er-1-5/), [Ollama, modelli di visione](https://ollama.com/search?c=vision), [ros-mcp-server](https://github.com/robotmcp/ros-mcp-server)

Interfacce e strumenti:

- [nanopb](https://github.com/nanopb/nanopb), [Bluepad32 FAQ](https://bluepad32.readthedocs.io/en/latest/FAQ/), [Gamepad API e HTTPS (Mozilla)](https://hacks.mozilla.org/2020/07/securing-gamepad-api/), [specifica Gamepad](https://w3c.github.io/gamepad/), [contenuto misto (MDN)](https://developer.mozilla.org/en-US/docs/Web/Security/Mixed_content)
- [MCAP](https://mcap.dev/), [Rerun](https://github.com/rerun-io/rerun) e [URDF in Rerun](https://rerun.io/docs/howto/urdf), [Foxglove SDK](https://foxglove.dev/blog/announcing-the-foxglove-sdk), [Foxglove 2.0 e codice aperto](https://discourse.openrobotics.org/t/foxglove-2-0-integrated-ui-new-pricing-and-open-source-changes/36583), [urdf-loaders](https://github.com/gkjohnson/urdf-loaders)
- [ROS 2 Lyrical](https://discourse.openrobotics.org/t/ros-2-lyrical-luth-released/55021) e [piattaforme](https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html), [RoboStack con pixi](https://pixi.prefix.dev/latest/build/ros/)
- [GitHub Actions, costi](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [runner sul proprio computer](https://docs.github.com/en/enterprise-server@3.21/actions/how-tos/manage-runners/self-hosted-runners/add-runners), [Wokwi CI](https://docs.wokwi.com/wokwi-ci/getting-started)

Privacy:

- [Garante: videosorveglianza, domande frequenti](https://www.garanteprivacy.it/faq/videosorveglianza), [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)

Nella repo: `calc/statica_tripode.py`, `calc/andature.py`, `cad/script/assieme.py` (`pose_tripode`, `posa_zampa`), `cad/script/zampa.py` (`GAMMA_MIN`), `cad/script/esporta_mesh.py`, `docs/progetto-meccanico.md`, `docs/studio-componenti.md`, `docs/dimensioni-componenti.md`, `docs/BOM.md`, `docs/decisioni.md` (D-011, D-012, D-019, D-034, D-039, D-050, D-061, D-063).
