# Circuiti stampati al posto delle millefori: requisiti

Studio preliminare del 16 ottobre 2026 (D-076: "l'utente prevede di far stampare un PCB al posto delle millefori e lo disegneremo insieme in una versione successiva"). Questo file raccoglie **cosa devono fare e dove devono stare** le schede: non sceglie quante schede fare né come disegnarle. Niente è approvato né comprato.

- Quote in mm nella terna del robot: X avanti, Y a sinistra, Z in alto, origine al centro del corpo sul piano dei femori.
- Stato dei dati: **V** verificato (fonte primaria, oppure il modello CAD per le parti stampate), **S** stimato (fonte indiretta, quota di catalogo non riletta, ingombro di una parte comprata nel CAD), **C** da confermare sul pezzo o sul disegno del produttore.
- Fonti con file e riga. Gli ingombri "dal manifest" sono calcolati da `guida/dati/manifest.json` (CAD 2.1.6, "Hexapod v2.1.0 v14"): trasformata di ogni occorrenza applicata al `bbox` del suo componente. Sono V per le parti stampate e S per le parti comprate, che nel CAD sono scatole con le quote dei venditori.
- Il CAD di oggi è la 2.1.6. Le modifiche della 2.1.7 che toccano le schede (vassoio sulle colonne della base, asola del bus, scheda del carapace allungata) sono in bozza (`docs/piano-v2.1.0.md` righe 343-566): qui sono indicate a parte.

## 1. Le tre millefori di oggi

### 1.1 Basetta dell'ESP32

**Funzione.** Zoccolo dell'ESP32, che non ha fori (`docs/BOM.md:33`), e nodo di tutta la logica: regolatore 5 V, protezione del 5 V dell'ESP32 dalla USB, traslatore della seriale verso la SSC-32, buffer a 5 V della catena LED, pull-up del bus I2C, metà bassa del partitore della batteria, partenza di tutti i fili verso il resto del robot (`guida/schemi/schemi.md:23-245`; D-053, `docs/decisioni.md:153-157`).

**Forma.** Millefori C2 a doppia faccia tagliata a 56 × 35 (x 22…78, |y| ≤ 17,5, z 5,9…7,5), griglia di 21 colonne × 13 righe; 4 fori Ø2,2 su colonnine del vassoio con M2 × 5 (`schemi.md:25`, `:157`; D-053).

**Componenti** (`schemi.md:42-58`):

| Sigla | Cosa | Voce del BOM | Contenitore oggi | Note |
|---|---|---|---|---|
| U1 | ESP32-S3-CAM UICPAL N16R8 RE1.3, su due strip femmina 1 × 20 | A2, C2 | modulo, strip a passo 2,54; file a 25,4 (10 passi) [S] | resta (preferenza dell'utente). Pin saldati: 15 su 40 (`schemi.md:93`) |
| U2 | regolatore 5 V Pololu D24V22F5 | B2 | modulo 17,8 × 17,8, alto 7,2 su Kapton; 5 pin in fila | 2,5 A [V Pololu 2858, `BOM.md:43`]; ordine dei pin [C] (S-03) |
| U3 | buffer SN74AHCT125N | X9 | DIP-14 senza zoccolo | 2 canali usati (anello e lobi; tibie), 2 a massa |
| U4 | traslatore KAmod Level Shift x4 | C1 | modulo 15,7 × 10,7, due file da 6 a 7,62 [S] | canale 1 TX, canale 3 RX; ha già 4,7 kΩ verso HV e verso LV su ogni canale [V, `docs/ricerca/dati-moduli.md:37`] |
| PTC1 | Bourns MF-R075 | X9 | radiale, sdraiato sopra U3 (8,1 mm su 8,5) | tenuta 0,75 A a 23 °C; il ramo dopo il PTC arriva a circa 0,86 A (S-06) |
| D1 | Schottky 1N5819 | C3 | assiale | fra 5 V del regolatore e pin 5V dell'ESP32 (S-07): il pin 5V della scheda è legato alla VBUS della USB da un PTC, senza diodo [V Freenove, S UICPAL; `dati-moduli.md:176-177`] |
| R1 | 10 kΩ, pull-down di GPIO48 | X9 | assiale | dati a caso durante il reset |
| R2 | 330 Ω in serie al dato dei LED | X9 | assiale | polo 4 del cavo del carapace |
| R4, R5 | 4,7 kΩ, pull-up di SCL e SDA | B10 | assiale | valore S-13 |
| R7 | 47 kΩ 1 %, partitore della batteria, lato basso | B10 | assiale | il lato alto (R6) sta alla 2813 |
| CS1 | 100 nF, filtro di GPIO1 | B8 | SMD 0805 [S] sul lato saldature | |
| CS2 | 100 nF, disaccoppiamento di U3 | B8 | SMD 0805 [S] | |
| J1 | ponticello 3V3 dell'ESP32 → 3,3 V dei sensori | — | filo 19 | si toglie solo se arriva X3 (D-076: mai J1 e X3 insieme) |
| — | cavo piatto a 16 vie verso il carapace | X2 | saldato in riga 13 | |

**Restano fuori dalla basetta, per scelta di sicurezza** (`schemi.md:60`, `:236-237`; S-11, S-20): R6 da 100 kΩ saldata sull'uscita della 2813 (il filo del partitore porta al più 2,7 V attraverso 100 kΩ); D2 (1N4148) in linea nella guaina dell'abilitazione; R3 da 22 kΩ fra ENA e GND **su ciascun D42V110F6** (se il filo si stacca il rail resta spento); 100 kΩ fra OFF e massa **sulla 2813**; R9 da 330 Ω in linea sul dato delle tibie. Una PCB deve conservare il principio (pull-down all'estremo lontano del filo), non necessariamente il posto.

**Reti** (netlist in `schemi.md:66-91`; correnti dai bilanci):

| Rete | Tensione | Corrente | Fonte | Note |
|---|---|---|---|---|
| VBAT (logica) | 6,0…8,4 V (2S); il firmware tiene la logica fino a 3,3 V per cella, 6,6 V | fino a circa 2,3 A in ingresso a U2 con il pacco a 6 V [S]; a monte F2 da 2 A | `schemi.md:244`; `piano-elettronica-software.md:206` | tocca solo il VIN di U2; arriva con un filo dalla 2813, posato per ultimo (`schemi.md:151`) |
| 5V_REG | 5,0 V | U2 2,5 A max: ESP32 ~250/500 mA (tipica/picco), LED fino a 600 mA (tetto del firmware), ampli ~200 mA picco; con alta e media priorità ~1,36 A di picco [S] | `piano-elettronica-software.md:187-198` | senza X3 porta anche i 3,3 V dei sensori: ~1,56 A |
| 5V_ESP | 4,55…4,7 V dopo D1 [S] | ESP32 ~250/500 mA [S] | `schemi.md:202` | |
| 5V_LED | 5 V dopo PTC1 | tetto 600 mA + pixel spenti 16…94 mA + ampli 200 mA ≈ 0,86 A [S] | S-06; `predisposizioni.md:104` | poli 1-2 del cavo del carapace e ramo delle tibie |
| 3V3_ESP / 3V3S | 3,3 V dal regolatore della scheda (AMS1117 [V Freenove, S UICPAL], `dati-moduli.md:180`) | sensori 104/157 mA (alta), 127/201 mA (alta e media) [S] | `piano-elettronica-software.md:175-179` | X3 solo se la prova in P2 cala sotto 3,0 V (D-076) |
| GND | — | ritorno del 5 V e della logica; stella su U2 (Q-4) | `schemi.md:238` | il ritorno dei LED arriva con fili suoi, non sui pin di massa della logica |
| SDA, SCL | 3,3 V, I2C0 su GPIO47 e GPIO3, 400 kHz | pull-up equivalente obiettivo 1,0…1,4 kΩ, minimo 0,97 kΩ [S] | `piano-elettronica-software.md:109`, `:133-138` | quattro rami dalla riga 1 più il polo 6/8 del cavo |
| TX3, RX3 / TX5, RX5 | 3,3 V lato ESP32, 5 V lato SSC-32 | UART1 GPIO21 TX, GPIO14 RX, 115200 baud (D-012) | `piano-elettronica-software.md:91`, `:93`, `:142` | in P2 si prova 230400 |
| LED_IN, Y1, DATA, DATA2 | 3,3 V in ingresso al buffer, 5 V in uscita | 800 kHz (RMT su GPIO48) | `predisposizioni.md:170` | due uscite separate: carapace e tibie |
| GPIO42 (abilitazione) | 3,3 V | ~0,25 mA nelle due R3 [S] | S-05 | rail spento a GPIO flottante (D-019) |
| OFF | 3,3 V | impulso | `cablaggio.md:79` | la 2813 spegne sopra 1 V (S-11) |
| SENSE | 0,32 × VBAT: 2,37 V a 7,4 V, 2,69 V a 8,4 V | circa 57 µA a 8,4 V (147 kΩ) | `schemi.md:203` | GPIO1, ADC1_CH0 |
| BCLK, WS, MIC, AMP | 3,3 V, I2S | BCLK circa 3,07 MHz (48 kHz × 64 fronti) [S, calcolo], WS 48 kHz | `predisposizioni.md:98` | GPIO38, 39, 40, 2: solo passano dalla riga 12 alla riga 13 |

**Collegamenti verso il resto** (`schemi.md:210-225`; `cablaggio.md:65-154`):

| Verso | Fili | Sezione | Connettore oggi | Lunghezza |
|---|---|---|---|---|
| uscita della 2813 (VBAT) | 1 | 26 AWG di B17, siliconico se c'è (S-27) | saldato ai due capi | circa 25 cm (`BOM.md:59`) |
| massa della 2813 | 1 | 26 AWG | saldato | idem |
| R6 alla 2813 (partitore) | 1 | 26 AWG | saldato | idem |
| OFF della 2813 | 1 | 26 AWG | saldato | idem |
| ENA dei due D42V110F6 (D2 in linea) | 1, poi 3 dopo il diodo | 26 AWG | saldato | dalla basetta alle due baie |
| SSC-32: TX, RX, massa | 3 | 26 AWG | Dupont femmina (C4) sul connettore seriale | pochi cm; S-22: forse la massa non serve |
| bus I2C, 4 rami (INA260 S, INA260 D, IMU + ADC, ToF frontale) | 4 per ramo; il ramo 3 ha due fili per foro | Qwiic tagliati (28 AWG [S]) o 30 AWG | saldati in riga 1 | bus in tutto circa 1,1 m [S] |
| scheda del carapace | 16 | cavo piatto IDC (passo 1,27) | saldato sulla basetta, spina IDC sull'altro capo | circa 15 cm [S] |
| pulsante → pin A e B della 2813 | 2 (poli 15-16 separati dal cavo piatto) | giuntati a 26 AWG | stagno e guaina | |
| prese delle luci delle tibie | 3 (massa, +5 V, dato con R9 in linea) | 26 AWG, dato 30 AWG | saldati | fino alle prese a x 48…64, y −25…−22 |

In tutto circa 47 fili esterni saldati, più 37 fili isolati e una cinquantina di ponticelli sul lato saldature (`schemi.md:102-149`).

### 1.2 Scheda del carapace (X2)

**Funzione.** Unico punto di passaggio fra il corpo e tutto quello che sta sul carapace: 5 V, 3,3 V, I2C, I2S, dato dei LED e pulsante arrivano dal cavo a 16 vie e si dividono verso catena LED, microfoni, amplificatore, ToF posteriore, espansione Qwiic e pulsante. Porta il condensatore della catena LED. Si stacca con la spina IDC quando si toglie il carapace (`cablaggio.md:128-130`, `:166`; `predisposizioni.md:66`).

**Forma.** Avanzo di C2 da 20 × 30 (x 29,5…49,5, |y| ≤ 15), appeso al dorso su quattro bugne Ø5,5 × 3,5 a (32; ±12,5) e (47; ±12,5), lato componenti verso il basso, faccia alta a z 30,9 (`schemi.md:249-251`; `guida/dati/fori.json`, `Corpo_Carapace` `ins_sch_a…d`). Nella 2.1.7 si allunga a circa 23 per la testata a 90° (sezione 3.3).

**Componenti** (`schemi.md:257-261`):

| Sigla | Cosa | Voce | Contenitore | Note |
|---|---|---|---|---|
| J2 | testata 2 × 8, passo 2,54, con chiave; **a 90° sul bordo posteriore** (D-076) | X2 | THT, Würth 61201621721 [C: codice da confermare sul disegno] | accoppiata alla spina IDC Würth 61201623021; la tacca va dal lato dei poli dispari [V sul disegno della spina, S-26] |
| CE1 | elettrolitico 470 µF 10 V, **basso: Ø6,3, alto al più 8** | X2 | radiale, sdraiato | D-076 (`decisioni.md:698`) |
| R8 | 100 kΩ, pull-down dei dati dei microfoni | B10 | assiale | **al microfono, nel fascio**, non sulla scheda (`schemi.md:261`) |
| — | presa Qwiic | X1 | oggi un cavo Qwiic tagliato a metà (Adafruit 4210) | un JST SH SMD da 1 mm non si salda sulla millefori (`schemi.md:326`) |
| — | espansore TCA9534 | X20 | modulo SparkFun DEV-17047, innestato sulla presa Qwiic | posto da decidere (P-067, S-17) |

**Reti** (`schemi.md:265-280`): 5V (poli 1-2; catena LED fino a 600 mA, ampli fino a ~200 mA), 3V3 (polo 7; microfoni ~2,8 mA, ToF posteriore 20/40 mA, TCA9534 < 1 mA, espansione), GND (poli 3, 5, 9), SCL (polo 6), SDA (polo 8), DATA (polo 4: dato a 5 V già bufferizzato e dopo 330 Ω), BCLK (10), WS (11), MIC (12), AMP (13), BTN_A e BTN_B (15, 16, tensione dei pin A e B della 2813 sconosciuta: S-10), polo 14 di riserva (XSHUT del ToF del mento, X25).

Piedinatura della testata, da non cambiare (`cablaggio.md:132-143`, `predisposizioni.md:77-92`): 1-2 +5 V, 3 massa, 4 dato LED, 5 massa, 6 SCL, 7 +3,3 V, 8 SDA, 9 massa, 10 BCLK, 11 WS, 12 dati dei microfoni, 13 dati verso l'ampli, 14 riserva, 15-16 pulsante. È ordinata perché nel cavo piatto il dato dei LED stia fra due masse, SCL e SDA accanto a masse o al 3,3 V, l'I2S separato dal bus da una massa, il pulsante lontano dai segnali veloci. Caduta nel cavo con 0,8 A: circa 21 mV [S].

**Collegamenti verso il resto** (`cablaggio.md:145-154`; `schemi.md:305-327`):

| Verso | Fili | Sezione | Connettore | Lunghezza |
|---|---|---|---|---|
| basetta | 16 | cavo piatto | spina IDC 2 × 8 con chiave, si sfila dall'ottagono | circa 15 cm [S] |
| catena LED: anello del pulsante (x −40), poi i 6 lobi | 3 (5 V, dato, massa) | 30 AWG (X31) | saldati | lungo il fianco sinistro, nei ganci sotto il dorso |
| due microfoni MS3625 (x 83…96, \|y\| 3…19) | 5 (3,3 V, massa, BCLK, WS, dati), i due microfoni uniti fra loro | 30 AWG | saldati | circa 8 cm [S] |
| amplificatore MAX98357A (x 51,85…69,55) | 5 (5 V, massa, BCLK, WS/LRC, DIN) | 30 AWG | saldati | pochi cm |
| ToF posteriore VL53L1X (guancia sinistra di coda) | 4 (3,3 V, massa, SDA, SCL) più XSHUT dal TCA9534 | 30 AWG | saldati | circa 20 cm [S] |
| pulsante Ø12 (x −40) | 2 | 26 AWG | saldati sui pin 15-16 | circa 9 cm [S] |
| espansione | 4 | Qwiic | JST SH 4 poli | raggiungibile dall'ottagono |

L'altoparlante si collega all'ampli, non alla scheda (2 fili, circa 17 cm).

### 1.3 Striscia dei partitori (X5, X6, X14)

**Funzione.** Otto partitori fra 3,3 V e massa verso gli otto ingressi dell'ADS7830: sei FSR dei piedi (canali 0-5) e due NTC dei regolatori (canali 6-7). Ogni canale: 10 kΩ 1 % verso il 3,3 V, sensore verso massa, 100 nF in parallelo al sensore; lettura invertita e in rapporto, perché il 3,3 V dei partitori è il VIN dell'ADC, che ne è anche il riferimento (`schemi.md:427-433`, `:528`).

**Forma.** Millefori 9 × 4 fori = 22,86 × 10,16, R in piedi (circa 7 mm), C sul lato saldature, due viti M2 sulla colonna I. **Posto nel corpo non dimostrato** (S-28, S-29; `schemi.md:433`, `:553-568`).

**Componenti** (`schemi.md:437-446`): R1-R8 10 kΩ 1 % (Yageo MFR-25FRF52-10K, X5 e X14), C1-C6 100 nF (X5: a reoforo o SMD, S-30), C7-C8 100 nF SMD (proposta, kit B8). FSR e NTC arrivano con i fili.

**Reti** (`schemi.md:450-458`): 3V3 dal VIN dell'ADC (carico totale circa 2 mA [S]); GND con una massa per presa; nodi N0…N7 verso A0…A7.

**Collegamenti** (`schemi.md:511-524`): 26 fili da 30 AWG (sei segnali e sei masse dalle prese dei piedi; due segnali e due masse dalle NTC, 28 AWG; otto fili verso A0…A7, consigliati 40-60 mm; VIN e GND dell'ADC). Lungo la zampa solo segnale e massa, mai il 3,3 V (`predisposizioni.md:110`).

## 2. Moduli che parlano con queste schede

Per ciascuno: dove sta, come si collega e se potrebbe diventare un chip sulla PCB. "Chip sulla PCB" vuol dire comprare il circuito integrato e i suoi pochi passivi al posto della scheda già fatta: **è sempre una voce nuova, da approvare**, e toglie un modulo che in alcuni casi l'utente ha già in casa (D-073, D-074). I contenitori dei chip sono di catalogo, non riletti per questo studio [S].

| Modulo | Voce, stato | Dove (manifest 2.1.6) | Collegamento | Chip sulla PCB? | Perché |
|---|---|---|---|---|---|
| ESP32-S3-CAM UICPAL N16R8 | A2, in casa | sopra la basetta: x 12,7…81,1, \|y\| ≤ 14,15, PCB a z 16,0…17,6 | 2 strip 1 × 20, 15 pin usati | **no**, resta | decisione dell'utente (CLAUDE.md, "Controllo") |
| SSC-32 clone V2.5 | A4, comprata | x −50,8…22, \|y\| ≤ 27,5, PCB a z −1,4 | seriale: 3 Dupont; VL dalla 2813 | **no**, resta | decisione dell'utente |
| D42V110F6 × 2 | B1 | baie anteriori, x 14…57,2, \|y\| 33,4…44,8 | ENA (dalla basetta con D2), NTC sulla bobina | **no**, restano | decisione dell'utente; 13-14 A per lato [S] |
| D24V22F5 (5 V, 2,5 A) | B2, da comprare | sulla basetta, U2 | VIN, GND, VOUT (PG, EN liberi) | forse | un convertitore da 2,5 A sulla PCB chiede un disegno attento (anello di commutazione, induttore, termica sotto l'ESP32); tenerlo come modulo saldato sulla PCB è la via con meno rischi. P4 misura se scalda chiuso sotto l'ESP32 (`piano-elettronica-software.md:201`) |
| Pololu 2813 (interruttore, protezione dall'inversione) | B3, da comprare | in coda, in piedi: x −58,4…−54,3, \|y\| ≤ 12,7, z −4,4…15,9 | VIN da F2, VOUT, OFF, A e B | no | sta a 8 cm dalla basetta, sul ramo da 2 A che parte dai Wago; porta R6 e la 100 kΩ di OFF; integrarla vuol dire disegnare un interruttore di potenza con protezione |
| KAmod Level Shift x4 | C1, da comprare (2,51 €) | sulla basetta, U4 | TX canale 1, RX canale 3 | **sì, o sparisce** | due canali del SN74AHCT125 restano liberi (`schemi.md:46`): il TX a 3,3 V → 5 V può passare da uno di questi (ingressi TTL [S]); il RX a 5 V → 3,3 V con un partitore o un traslatore a MOSFET. Da sapere prima: soglia d'ingresso della seriale del clone [C] |
| SN74AHCT125N | X9, approvato per il provino 7 | sulla basetta, U3 | GPIO48 → 1A e 2A; 1Y → polo 4, 2Y → tibie | **sì** | DIP-14 → SOIC-14 o TSSOP-14, oppure due SN74AHCT1G125 SOT-23-5 (la parte che `predisposizioni.md:170` indicava prima della millefori) |
| PTC MF-R075 | X9 | sulla basetta, PTC1 | sul 5 V dei LED | **sì** | equivalente SMD (1206 o 1812) [S]; taglia da rivedere con S-06 (0,86 A contro 0,75) |
| ADS7830 Adafruit #5836 + striscia dei partitori | X6, X5, X14 | vano sotto il vassoio: x 39…69,5, y 0,75…18,45, z −5,4…−0,7 | I2C 0x48; 8 ingressi dai partitori | **sì** | ADS7830 in TSSOP-16 [S] con gli 8 partitori sulla stessa PCB: spariscono la striscia, 8 fili ADC-striscia e un ramo del bus. Da tenere: riferimento uguale all'alimentazione dei partitori (lettura in rapporto, `schemi.md:528`) |
| INA260 Adafruit #4226 × 2 | X7 | baie anteriori sopra le slitte: x 14,15…37,05, \|y\| 29…40,2, z 8,6…31,4 | I2C 0x44, 0x45; in serie al rail da 13 A, morsettiera a vite 5,08 | no, non sulla scheda della logica | il chip va dove passa la corrente del rail (13-14 A [S], shunt di 2 mΩ integrato, 15 A continui [V, `dati-moduli.md:141`]): sulla PCB della logica porterebbe il rail sotto l'ESP32. Solo una schedina di potenza per lato, con rame spesso, potrebbe sostituire il modulo: fuori dal perimetro di queste millefori |
| IMU GY-6500 (MPU-6500), Pololu LSM6DSO predisposta | X4, in casa | sotto il vassoio sul tetto del tunnel: x 34,5…60,5, y −15,35…0,15, z −2,9…−0,3, su `Corpo_Piastrina_IMU` | I2C 0x68 (0x6B la Pololu), 4 fili saldati | no | la scelta 2.9 vuole l'IMU **fissata rigida sul `Corpo_Base`**, che porta le zampe, non sul vassoio in PLA (`predisposizioni.md:140`, `:143`; `piano-elettronica-software.md:160`). Un chip sulla PCB della logica cambierebbe questa decisione: va chiesto all'utente |
| ToF frontale VL53L7CX Pololu #3418 | X8 | mensola della camera a 20°: x 91,3…100,3, \|y\| ≤ 6,5, z 0…18 | I2C 0x30 (dal firmware), alimentato dal VDD a 3,3 V con VIN scollegato | no | deve guardare dalla finestra della visiera; 4 fili lungo la torretta |
| ToF posteriore VL53L1X Pololu #3415 | X19 | guancia sinistra di coda a 35°: x −101,1…−88,3, y 11,9…24,9 | I2C 0x31, XSHUT dal TCA9534 | no | deve guardare dalla porta di coda |
| TCA9534 SparkFun DEV-17047 | X20, in arrivo il 24 novembre | sulla scheda del carapace (posto da decidere, S-17) | I2C 0x20, Qwiic | **sì** | TSSOP-16 o SOIC-16 [S] sulla PCB del carapace; l'XSHUT del ToF posteriore esce da un suo I/O |
| MAX98357A generico | X17, in casa (10 pezzi) | sotto il dorso, bugne a (67,35; ±6,5): x 51,85…69,55, \|y\| ≤ 8,75, z 27,9…30,9 | I2S + 5 V, 5 fili; altoparlante alla morsettiera | forse | il chip è TQFN-16 da 3 × 3 o WLP [S], non saldabile a mano senza aria calda: solo con il montaggio fatto dal produttore. In più il modulo c'è già |
| Microfoni MS3625 × 2 (Adafruit 3421 predisposte) | X16, in casa | sotto i fori della fascia (89,3; ±11): x 83…95,6, \|y\| 4,25…17,75, z 31,8…33,8 | I2S, 5 fili, uniti fra loro | no | la porta del microfono deve stare sul foro della fascia, con l'anello e la guarnizione: a 40 mm dalla scheda del carapace di oggi. Un microfono MEMS su una PCB lunga fino alla testa è possibile solo se la PCB arriva sopra i fori (sezione 3.4) |
| Catena LED, CE1 470 µF | X9, X11, X12, X2 | anello a x −40, lobi | 3 fili | il condensatore sì | CE1 sulla PCB del carapace com'è oggi (D-076: basso, Ø6,3 × 8) |
| Pulsante Ø12 | B3b, da comprare (2) | sul carapace a x −40, corpo z 14,4…38 | 2 fili ai poli 15-16 | no | è un pezzo da pannello |
| Cavo Qwiic, presa di espansione | X1 | scheda del carapace | JST SH 4 poli | **sì** | sulla PCB la presa JST SH SMD si salda (sulla millefori no, `schemi.md:326`) |
| Prese dei piedi e delle luci delle tibie (6 + 6 spine JR) | X5, X31 | sul tetto del tunnel: x 48,25…63,75, \|y\| 22,1…24,7, z −8,9…−0,4 | 2 poli (FSR) e 3 poli (luci) per zampa | forse | oggi spine piegate senza un supporto disegnato (P-012: "progettate con lo schema della striscia dei partitori, con la misura vera della spina JR", non nella 2.1.7). Una fila di pin su una PCB è il loro supporto naturale |
| Cicalino BX100, spie dei rail X13 | B9, X13 | in coda | presa di bilanciamento; file VS della SSC-32 | no | non toccano la logica |

**Quote delle schede comprate già verificate** (per le impronte): ADS7830 30,48 × 17,78, fori Ø2,5 a 25,4 × 12,7, file di 8 pin a 12,7 [V, `dati-moduli.md:58-62`]; INA260 22,86 × 22,86, fori Ø2,5 a 17,78 [V, `:142-145`]; VL53L7CX 12,7 × 17,78, fori Ø2,18 a 12,7 [V, `:87-90`]; KAmod 15,7 × 10,7, file a 7,62 [S, `:30-32`]; ESP32 UICPAL: file a 25,4 [S, prova a secco prima di saldare, D-076], piedinatura uguale a Freenove e Keyestudio [V su quelle, S sulla UICPAL, `dati-moduli.md:170`].

## 3. Spazi nel CAD

Inviluppi di oggi (2.1.6) con le modifiche della 2.1.7 indicate a parte. Le altezze delle parti comprate sono quelle del CAD (S); le parti stampate sono V nel modello.

### 3.1 Basetta: sul vassoio, sotto l'ESP32

| Cosa | Quote | Stato, fonte |
|---|---|---|
| Ingombro di oggi | x 22…78, \|y\| ≤ 17,5, z 5,9…7,5 (spessore 1,6) | V modello; D-053; manifest `Basetta` |
| Fissaggio | 4 colonnine Ø5,8 del vassoio, alte 3,3 (z 2,6…5,9), inserto M2 Ø3,4 × 4, a (29; ±6,8) e (75,5; ±6,5); viti M2 × 5 dall'alto; fori Ø2,2 nella basetta | V; `corpo.py:449-459`, `:512-515`; `fori.json` `bas_col_*_ins` |
| Sotto la basetta | 3,3 mm fino al piano del vassoio (z 2,6). Oggi le teste M3 del vassoio (z 2,6…5,6) a (30; ±12,5) e (75; ±12,5) lasciano 0,3 mm. **Nella 2.1.7** il vassoio si avvita su colonne della base con M2 × 5 svasate a filo (testa a z 1,6…2,5): i 3,3 mm tornano liberi, salvo le quattro colonnine | V 2.1.6 (`fori.json` `foro_pa/pb/aa/ab`); 2.1.7 in bozza (`piano-v2.1.0.md:351-367`, D-076) |
| Sopra la basetta | strip femmina alte 8,5: PCB dell'ESP32 a z 16,0…17,6 | S; D-053 |
| Sotto l'ESP32 | sede della microSD x 22,5…37,5, \|y\| ≤ 7, alta 1,9: lì restano **6,6** sopra la basetta. Altri componenti sul retro della scheda (AMS1117 SOT-223 circa 1,7, tantalio da 100 µF circa 2,8 vicino alle USB, decine di SMD) sono nelle gemelle Freenove e Keyestudio; le altezze non sono pubblicate | S, C; `rif_componenti.py:468`; `dati-moduli.md:181`; S-08 |
| File dei pin dell'ESP32 | x 22,5…73,3; \|y\| 12,35 nel CAD 2.1.6, **12,7 nella 2.1.7** (file a 25,4) | C → S; `rif_componenti.py:99`; D-076 |
| Altezze dei componenti di oggi | U2 7,2 su Kapton; PTC sopra U3 8,1 su 8,5 | S; S-08 |
| Bordo di coda (x 22) | SSC-32 fino a x 22; la sua morsettiera VS/VL (x 11,9…18,9, alta fino a z 8,7) a 3,1 mm | V modello (S il pezzo); D-053; `rif_componenti.py:446` |
| Sopra, verso la coda | USB-C dell'ESP32 x 12,7…20,1, fino a z 20,9, sotto lo sportellino dell'ottagono | S; `bloccanti-arresto2.md:111` |
| Bordo di testa (x 78) | vassoio fino a x 82, poi torretta della camera (x 82…92,3, \|y\| ≤ 6, fino a z 22,5) e mensola del ToF; la parete anteriore della base lascia passare solo \|y\| ≤ 17 sopra il tetto (`cor_fronte_semi`) | V; `corpo.py:49`, `:516-522` |
| Antenna dell'ESP32 | modulo x 55,6…81,1, z 17,6…20,8: il vassoio è in PLA perché "sotto l'antenna niente carbonio" | S; `BOM.md:134` |
| Fianchi | colonnine del coperchio Ø7,4 a (40; ±22,5), dal tetto a z 28,4: bordo interno a \|y\| 18,8 fra x 36,3 e 43,7 (è il motivo dei 35 di larghezza); prese dei piedi e delle luci da \|y\| 22,1; fianco del tunnel a \|y\| 27 | V; `corpo.py:45`, `:103-105`, `:371-373`; `rif_componenti.py:110` |
| Fili che escono oggi | riga 1 (bus, verso +Y), riga 13 (cavo piatto, 2813, abilitazione, tibie, verso −Y), bordo di coda (seriale, VBAT lungo il bordo sinistro) | V; `schemi.md:210-225` |

Una PCB più larga di 35 sarebbe possibile solo lontano dalle colonnine del coperchio (fuori da x 36,3…43,7) e sopra le prese, che oggi si raggiungono dall'alto a carapace tolto (`corpo.py:180`): da verificare nel CAD [C].

### 3.2 Vano sotto il vassoio (striscia dei partitori, ADC, IMU)

| Cosa | Quote | Stato, fonte |
|---|---|---|
| Vano | x 34…71, \|y\| ≤ 16, z −9,4 (tetto del tunnel) … +1,0 (lato inferiore del vassoio): 37 × 32 × 10,4. Si raggiunge solo togliendo il vassoio | V; `predisposizioni.md:125` |
| ADC | x 39…69,5, y 0,75…18,45, z −5,4…−0,7; bugne Ø5,5 alte 4 con inserto M2 a (41,55; 9,6) e (66,95; 9,6) | V bugne (`fori.json` `ins_ads_*`), S scheda |
| IMU | piastrina x 34,5…60,5, y −15,35…−4,25, z −5,4…−2,9; GY-6500 fino a z −0,3 (1,3 sotto il vassoio); bugne a (38,5; −7,5) e (56,5; −7,5) | V; D-074; `fori.json` `ins_imu_*` |
| Colonne del vassoio | oggi bugne Ø7,4 fino a z −4,0 più distanziali; **2.1.7**: colonne Ø6,0 fino a z 1,0 a (30; ±12,5) e (75; ±12,5) | V 2.1.6; `bloccanti-arresto2.md:49` |
| Tasca libera accanto all'IMU | x 60,5…71,3 (10,8) × y −20,9…0,75 (21,65); la striscia di 22,86 × 10,16 non ci sta con la colonna delle viti (mancano circa 1,2) | S (quote dei disegni); `schemi.md:557-566`; S-28 |
| Prese dei piedi e delle luci | x 48,25…63,75, \|y\| 22,1…24,7, z −8,9…−0,4 | V sede, S spine; manifest |
| Asola dei fili del bus | oggi x 47…53, y 13…16 (sotto la basetta); **2.1.7**: x 46,5…53,5, y 18…22, con un'ala del vassoio | `corpo.py:525`; `piano-v2.1.0.md:424-431` |

### 3.3 Sotto il dorso del carapace (scheda del carapace)

| Cosa | Quote | Stato, fonte |
|---|---|---|
| Scheda di oggi | x 29,5…49,5, \|y\| ≤ 15, z 29,3…30,9 | V modello; `corpo.py:225`, `:1082-1086` |
| Fissaggio | 4 bugne Ø5,5 alte 3,5 sotto il dorso a (32; ±12,5) e (47; ±12,5), inserto M2 (Ø3,4 × 4) messo da sotto; fori della scheda da allargare a Ø2,6 | V; `fori.json` `ins_sch_*`; `schemi.md:251` |
| Dorso | faccia interna a z 34,4 (`car_top` 36,0 meno 1,6): fra scheda e dorso 3,5 di aria fra le bugne | V; `corpo.py:110`, `:121` |
| Sotto la scheda | PCB dell'ESP32 a z 17,6: **11,7**; connettore del flat x 40,75…45,25, \|y\| ≤ 7,25, fino a z 19,6: **9,7**; modulo dell'antenna da x 55,6 fino a z 20,8 | S; `bloccanti-arresto2.md:104-113` |
| Davanti | amplificatore da x 51,85 (2,35 dal bordo), fino a 69,55 | V bugne, S scheda; manifest `Ampli` |
| Dietro | ottagono, cioè l'apertura di servizio del carapace, x −20…28, \|y\| ≤ 16 con angoli a 45°, chiusa dallo sportellino (z 34,4…36,0): deve restare libera (USB-C, pulsanti dell'ESP32, spina, presa di espansione) | V; `corpo.py:111-113`, `:143-144`; `cablaggio.md:162` |
| Ai lati | pozzetti delle viti del carapace Ø9,4 a (40; ±22,5), da z 28,4 al dorso: \|y\| libero fino a 17,8 fra x 35,3 e 44,7 | V; `corpo.py:141-142`, `:773` |
| **2.1.7** (D-076, modifica 12) | testata 2 × 8 a 90° sul bordo di coda; `sch_w` da 20 a circa 23; viti di coda spostate davanti alla testata (x ≥ 41,5); scatola della testata circa 9 sotto la scheda (fondo a circa z 20,3), spina orizzontale verso −X lunga 10-12, da x 29,5 a circa 17,5 | S; `piano-v2.1.0.md:473-489`; `bloccanti-arresto2.md:119-126` |
| Punti aperti della 2.1.7 | il fondo della spina (z 20,3) sta **0,6 sotto la cima della USB-C** nel tratto x 17,5…20,1: primo controllo nel CAD. Il verso in cui la scheda si allunga è tra i dubbi della revisione (`piano-v2.1.0.md:540`): allungata in avanti di 3 arriverebbe a x 52,5 e toccherebbe l'amplificatore (da x 51,85; conto mio, S) | S |

La 2.1.7 dice esplicitamente che "J2 al bordo e le quote della scheda restano le stesse che servirebbero a un PCB" (`piano-v2.1.0.md:475`): la PCB del carapace deve entrare nello stesso inviluppo.

### 3.4 Altre zone guardate per una scheda unica o più grande

| Zona | Quote | Cosa c'è, perché sì o no | Stato |
|---|---|---|---|
| Basetta, come in 3.1 | 56 × 35, 8,5 sopra e 3,3 sotto | è il posto naturale della logica: l'ESP32 ci si innesta | V |
| Vano sotto il vassoio, tasca accanto all'IMU | 10,8 × 21,65 × circa 10 | partitori o ADC; separato dalla basetta dal vassoio (i fili passano dall'asola) | S |
| Sotto il dorso, 3.3 | 20 (23 nella 2.1.7) × 30, 3,5 sopra e 9,7-11,7 sotto | scheda del carapace: deve restare sul carapace, che si toglie (sotto) | V/S |
| Sotto il dorso, fra amplificatore e paratie della testa | x 69,6…81, \|y\| ≤ 15 (le paratie stanno a \|y\| 15…28,5 da x 81 a 82,6), z circa 21…34,4 | sotto c'è il modulo dell'antenna (fino a x 81,1, z 20,8) e passa il flat della camera, che torna sopra la torretta e l'antenna: una PCB con rame qui starebbe sopra l'antenna | C (antenna: S, regola generale non riletta) |
| Sotto il dorso, sopra i microfoni | x 83…95,6, \|y\| 4,25…17,75, z 31,8…33,8 | microfoni sui fori a (89,3; ±11); una PCB del carapace lunga fino a qui li porterebbe sopra i fori, ma passa sopra l'antenna (riga sopra) | C |
| Lati dell'ottagono | 3,5 di larghezza (\|y\| 16…19,5, sotto z 29,4) o 4,2 d'altezza a \|y\| ≥ 19,5 | non ci sta nulla | V; `predisposizioni.md:72` |
| Sopra la SSC-32, fuori dall'ottagono | dorso a 9,2 sopra le spine dei servo (z 25,2); al centro pulsante (x −48,65…−31,35, z 14,4…38) e camera dell'anello (x −56,85…−23,15, z 27,2…29,6) | occupato | V |
| Baie anteriori | regolatori e INA260; camino d'aria \|y\| 27…33,4 da lasciare aperto | occupato | V; `predisposizioni.md:127` |
| Coda | 2813, F1, T-plug, cicalino, ToF posteriore, altoparlante | occupata; la porta di coda deve lasciare afferrare T-plug e presa di bilanciamento | V; `cablaggio.md:13`, `:167` |
| Zaino sul dorso | 4 bugne a (−9,5/13,5; ±29) | predisposizione per il computer di bordo; "niente zaino per ora" (D-076) | V |

Fatto che vincola il numero delle schede: **il carapace si toglie staccando una sola spina** e tutto quello che sta sul carapace (anello, lobi, microfoni, amplificatore, altoparlante, ToF posteriore, pulsante) resta sul carapace con i suoi fili (`cablaggio.md:166`). Una scheda unica per corpo e carapace vorrebbe un connettore per ogni modulo del carapace, oppure cambiare questa regola.

## 4. Vincoli

### 4.1 Sicurezza: batteria, fusibili, 5 V sui GPIO

- **Catena delle protezioni** (`cablaggio.md:25-33`; `BOM.md:46-48`): batteria 2S → T-plug → F1 30 A (15 A nelle prime accensioni) → Wago → **F2 2 A** (MINI, in linea) → 2813 (con protezione dall'inversione) → logica. Tutte le schede di questo studio stanno a valle di F2: sul loro VBAT passano al più 2 A continui; il regolatore a 2,5 A con il pacco a 6 V ne chiede circa 2,3 [S, `schemi.md:244`], quindi F2 è già al limite con tutto acceso (`piano-elettronica-software.md:208-217`: con le voci basse F2 passa a 3 A, da riapprovare).
- **VBAT sulla scheda**: 6,0…8,4 V. Oggi tocca solo il VIN del regolatore 5 V e arriva con un filo posato per ultimo, lontano da ogni altro filo (`schemi.md:151`, `:239`). Su una PCB: pista e piazzola del VBAT lontane dai pin dell'ESP32 e dalle reti a 3,3 V; larghezza da calcolare per 2,5-3 A (con rame da 35 µm e 10 °C di sovratemperatura circa 1,1-1,4 mm, IPC-2221 [S, conto mio]).
- **Nessun 5 V accanto a un GPIO**: l'ESP32-S3 non regge 5 V sui pin [S]. Sulla basetta restano vicinanze inevitabili controllate con il multimetro (S-09, `schemi.md:99`, prove 5 e 6). Sulla PCB: nessuna piazzola o pista a 5 V adiacente a un pin dell'ESP32 senza una massa o una distanza in mezzo.
- **Ritorno della USB**: il pin 5V della scheda è legato alla VBUS da un PTC da 0,5 A, senza diodo [V Freenove, S UICPAL] (`dati-moduli.md:176-177`). D1 impedisce alla USB di alimentare regolatore, LED e ramo della batteria, ma non impedisce al 5 V del pin di arrivare alla porta del Mac: "una alimentazione alla volta" resta la regola (`schemi.md:374`, S-07).
- **5 V dei LED**: PTC con tenuta sopra la corrente vera del ramo (0,86 A con ampli e LED al tetto, contro 0,75 del MF-R075: S-06) e intervento sotto quello che il D24V22F5 regge insieme all'ESP32 (2,5 A). A PTC scattato la superficie supera 100 °C [S]: non a contatto con l'ESP32 né con il PLA (`schemi.md:233`).
- **LED all'accensione**: pull-down da 10 kΩ all'ingresso del buffer, tetto di 600 mA nel driver; senza, 58 pixel bianchi chiedono circa 2,1 A e l'ESP32 si riavvia con i LED accesi (`predisposizioni.md:100-104`).
- **Rail dei servo spento di default** (D-019): GPIO42 → diodo → ENA, con il pull-down **su ogni regolatore**: se il filo si stacca il rail resta spento (S-05, S-20). Con GPIO42 alto l'ENA sta a circa 2,6 V, sopra i 2 V chiesti [S].
- **Spegnimento**: 100 kΩ fra OFF e massa sulla 2813 (spegne sopra 1 V, GPIO41 flotta nel reset; S-11).
- **Partitore della batteria**: R6 da 100 kΩ sulla 2813, così il filo porta al più 2,7 V attraverso 100 kΩ; se si stacca GPIO1 legge 0 V e il firmware spegne (`schemi.md:237`).
- **Connettore del carapace con chiave**: girata di 180° la spina porterebbe il +5 V dei poli 1-2 sui poli 15-16, cioè sui pin A e B della 2813 (`schemi.md:354`). La tensione di A e B non è nota (S-10): i poli 15-16 non passano dalla logica.
- **Masse**: stella sotto il regolatore 5 V, con fili separati per ingresso, LED e logica (`schemi.md:238`); Wago − come stella di tutti i rami (`cablaggio.md:177`). Doppia massa possibile fra SSC-32 e logica (S-22): da misurare prima di decidere il Dupont di massa della seriale.
- **Lungo la zampa mai il 3,3 V**: solo segnale e massa dell'FSR, una massa per presa; il 5 V delle luci ha la sua massa (`cablaggio.md:112`; `predisposizioni.md:110`).
- **Temperatura**: il D24V22F5 sta chiuso sotto l'ESP32 su un vassoio in PLA; in P4 si misura, e se scalda un secondo regolatore per luci e audio (`piano-elettronica-software.md:201`). Il carapace in PLA tiene 55-60 °C (`predisposizioni.md:180`).

### 4.2 Segnali delicati

- **I2C0** (GPIO47 SDA, GPIO3 SCL, 3,3 V, 400 kHz): bus di circa 1,1 m con una decina di schede, 150-250 pF [S]; pull-up equivalente 1,0-1,4 kΩ, mai sotto 0,97 kΩ; oggi 4,7 kΩ sulla basetta in parallelo a 3,3 kΩ delle tre Adafruit e ai 10 kΩ di GY-6500 e ToF (circa 1,2 kΩ, S-13); ripiego a 100 kHz solo se si contano errori (`piano-elettronica-software.md:133-144`; `predisposizioni.md:55-59`). Almeno 10 mm dai cavi da 12-16 AWG, incroci a 90° (`cablaggio.md:126`). GPIO3 è di strapping: il pull-up lo tiene al valore predefinito [V, `piano-elettronica-software.md:88`]. Ogni transazione sotto circa 5 ms (`:143`).
- **I2S** (GPIO38 BCLK, 39 WS, 40 dati dei microfoni, 2 dati verso l'ampli): full-duplex con BCLK e WS condivisi; BCLK circa 3,07 MHz [S]. Sulla linea dei microfoni un pull-down da 100 kΩ (D-074), ma sulla scheda c'è un pull-up da 10 kΩ verso 3V3 su GPIO40 (linea della microSD) [V Freenove, S UICPAL]: i due insieme tengono la linea alta, e il pull-down non conta (S-21, `dati-moduli.md:178`). Nel cavo piatto il gruppo I2S è separato dal bus da una massa (`predisposizioni.md:91`).
- **Seriale della SSC-32** (UART1, GPIO21 TX, GPIO14 RX, 115200 baud, D-012; 230400 da provare in P2): livelli 3,3 V ↔ 5 V; il traslatore di oggi ha già 4,7 kΩ verso HV e LV su ogni canale [V]; la soglia d'ingresso della seriale del clone non è nota [C].
- **Dato dei LED** (GPIO48, RMT, 800 kHz, 5 V dopo il buffer): 330 Ω in serie vicino al buffer, uscite separate per carapace e tibie (le tibie sono sei linee lunghe in parallelo con R9 330 Ω, `schemi.md:232`); nel cavo piatto fra due masse. GPIO48 pilota anche il WS2812 della scheda, che ripete il primo pixel (`piano-elettronica-software.md:102`).
- **GPIO2**: porta il LED "ON" della scheda con 1 kΩ a massa [V Freenove, S UICPAL]: va bene per un'uscita (dati dell'ampli), mai per l'I2C (`piano-elettronica-software.md:87`).
- **Ingressi analogici**: GPIO1 con 100 nF (CS1); partitori con 100 nF per canale; fili fra partitori e ADC corti (40-60 mm) e lontani dai rail; le NTC arrivano dalle baie, nel rumore dei convertitori (`schemi.md:442`, `:521`).
- **Antenna dell'ESP32** (modulo x 55,6…81,1): niente fibra di carbonio sotto (il vassoio è in PLA per questo, `BOM.md:134`). Per una PCB vale la regola generale dei moduli con antenna stampata: niente rame né piano di massa sotto e attorno all'antenna [S, regola Espressif non riletta per questo studio]. La basetta di oggi arriva a x 78, sotto la parte anteriore del modulo.
- **Flat della camera** (24 poli, levetta a ribalta sul lato dell'antenna): parte dal connettore a x 40,75…45,25 e torna verso la camera sopra la torretta e il modulo dell'antenna (`corpo.py:516-517`; `dati-moduli.md:182-183`). Non passa dalle schede, ma una scheda sopra l'ESP32 deve lasciargli il posto (9,7 mm sotto la scheda del carapace di oggi).
- **Camera sul suo bus** (GPIO4, GPIO5): nessun sensore su quel bus; l'indirizzo 0x68 dell'IMU non va mai lì (`piano-elettronica-software.md:129`; D-074).

### 4.3 Montaggio e smontaggio

- **Chi salda**: l'utente, a mano, al banco (guida di montaggio, D-075). Sulla basetta di oggi ci sono già SMD da 0805 saldati a mano (`schemi.md:55-56`, `:467`). Chip a passo fine (TQFN, WLP, LGA) solo se la PCB arriva montata dal produttore: da chiedere all'utente (la produzione è un altro file di questo studio).
- **ESP32 estraibile** sulle strip femmina: impronta 2 × 20 a 25,4, antenna verso +X e USB verso −X; condizione per saldare: la prova a secco con tutte e 40 le gambe (D-076, P-005).
- **Prove con il multimetro prima di alimentare**: la guida le ha per ogni scheda (`schemi.md:170-206`, `:338-350`, `:479-495`), e la prima accensione si fa senza ESP32, misurando nelle prese delle strip. Una PCB deve lasciare raggiungibili i punti di misura: VBAT, 5 V del regolatore, 5 V dei LED, 3,3 V dei sensori, SDA, SCL, GPIO1, masse.
- **Misura RMT al banco** (P2): un canale libero del traslatore verso GPIO38 con un filo provvisorio (`schemi.md:227`): sulla PCB un punto o un ponticello apribile.
- **Basetta saldata al banco e poi montata**: oggi tutti i fili verso il robot si saldano sulla basetta al banco, VBAT per ultimo, e all'altro capo nel robot (`schemi.md:166-167`). Connettori sulla PCB renderebbero la scheda smontabile senza dissaldare, ma sono componenti in più: è una scelta da fare con l'utente.
- **Vassoio**: si toglie con basetta, ESP32, torretta e camera; IMU e ADC sotto il vassoio si montano una volta (`predisposizioni.md:141-142`).
- **Carapace**: si toglie lo sportellino, si sfila la spina IDC dall'ottagono, si svitano le 4 viti, si stacca il cicalino, si solleva (`cablaggio.md:166`). Nella 2.1.7 la spina esce orizzontale verso −X.
- **Zampa**: si staccano 3 spine dalla SSC-32, la spina dell'FSR e quella delle luci dalle prese sul tetto, raggiungibili a carapace tolto (`cablaggio.md:168`).
- **Viti e inserti**: M2 × 5 a testa tonda Ø4 (D8) nelle colonnine e nelle bugne; inserti M2 del kit con zigrinatura Ø3,2 (D-076); fori della scheda Ø2,2 (basetta) e Ø2,6 (carapace). Sulle facce della PCB, attorno ai fori, niente piazzole sotto la testa né sopra la colonnina (le zone vietate di `schemi.md:33-36` restano, `piano-v2.1.0.md:366`).
- **Spessore**: 1,6 come la millefori (`bas_sp` S): le quote verticali di 3.1 e 3.3 contano su questo valore.

### 4.4 Scelte già prese

| Scelta | Cosa vincola | Fonte |
|---|---|---|
| PCB in una versione successiva, non nella 2.1.7; la guida resta sulle millefori | lo studio non cambia CAD né guida | D-076 (`decisioni.md:681-686`) |
| Testata 2 × 8 a 90° con chiave sul bordo posteriore della scheda del carapace, spina IDC Würth 61201623021, piedinatura dei 16 poli | connettore, posizione e ordine dei poli della PCB del carapace; cavo piatto saldato sulla basetta | D-076; `cablaggio.md:132-143` |
| Le quote della scheda del carapace della 2.1.7 "restano le stesse che servirebbero a un PCB" | inviluppo della PCB del carapace | `piano-v2.1.0.md:475` |
| X3 (regolatore 3,3 V dei sensori) tolto: 3,3 V dei sensori dal 3V3 dell'ESP32 con J1; X3 solo se la prova del 3,3 V lo chiede; mai J1 e X3 insieme | la PCB deve poter tornare a un regolatore proprio senza comprarlo ora | D-076 (`decisioni.md:701`); S-12 |
| Vassoio su colonne della base con M2 × 5 svasate a filo; colonnine della basetta a (29; ±6,8) e (75,5; ±6,5) | 3,3 mm liberi sotto la basetta, fori nelle posizioni di oggi | D-076, D-053 |
| File dei pin dell'ESP32 a 25,4, con la prova a secco | impronta delle strip | D-076 (P-005) |
| 470 µF basso (Ø6,3 × 8, 10 V) e testata a 90° nell'ordine di X2, **non ancora comprati** | con una PCB l'ordine di X2 si può rivedere | D-076; `BOM.md:175` |
| UART1 su GPIO21/14 a 115200; rail spento di default con GPIO42; OFF su GPIO41; batteria su GPIO1 | assegnazione dei pin fissa, nessun GPIO libero | D-012, D-019; `piano-elettronica-software.md:79-105` |
| Piano A: niente microSD | GPIO38-40 all'I2S | `piano-elettronica-software.md:81`, `:158` |
| Indirizzi I2C (0x20, 0x30, 0x31, 0x44, 0x45, 0x48, 0x68/0x6B) | nessun conflitto da introdurre | `piano-elettronica-software.md:111-131` |
| IMU rigida sul `Corpo_Base`, non sul vassoio; un solo ADS7830; buffer dei LED sulla basetta; connettore del carapace sotto il dorso; tetto LED a 600 mA | posto di IMU e buffer | `predisposizioni.md:140-149` |
| Moduli in casa: GY-6500, 2 MS3625, MAX98357A, altoparlante | sostituirli con chip è un acquisto in più | D-074 |
| Preferenze dell'utente: meno componenti possibile; nessun acquisto senza approvazione; restano ESP32-S3-CAM UICPAL N16R8, SSC-32 clone, D42V110F6 sulle slitte e batteria 2S | perimetro dello studio | richiesta dell'utente; `CLAUDE.md`, "Cosa è deciso dall'utente" |

Le scelte di `schemi.md` (D1, due canali del buffer, un PTC, pull-up da 4,7 kΩ, stella su U2, R6/D2/R3/100 kΩ fuori dalla basetta) sono dello schema, "proposta da approvare" (`schemi.md:3`): una PCB può cambiarle se ne tiene lo scopo, scritto in `schemi.md` 1.7 e 2.7.

### 4.5 Dati che mancano per disegnare una PCB

| Dato | Serve per | Stato, dove |
|---|---|---|
| Interasse e piedinatura della UICPAL RE1.3; quale delle 4 schede è la RE1.3 | impronta delle strip | S; prova a secco (P-005), S-15, `CLAUDE.md` |
| Componenti e altezze sul retro dell'ESP32 | altezza dei componenti sotto l'ESP32 | C; S-08 |
| Ordine dei pin del D24V22F5 | impronta del regolatore | C nello schema (S-03); pagina Pololu 2858 da rileggere |
| Soglia d'ingresso della seriale del clone; VL− comune alle masse dei servo? | traslatore, masse | C; S-22 |
| Tensione dei pin A e B della 2813 | pulsante, poli 15-16 | C; S-10 |
| Disegno della testata a 90° (Würth 61201621721): altezza della scatola, chiave, polo 1 | impronta e posizione sulla PCB del carapace | C; S-26, `piano-v2.1.0.md:480` |
| Pull-up da 10 kΩ su GPIO40 sulla UICPAL | pull-down dei microfoni | V Freenove, C UICPAL; S-21 |
| Misura della spina JR | prese dei piedi e delle luci | C; P-012 |
| Fori della GY-6500, del MAX98357A generico, quote delle MS3625 | impronte o supporti | C; `CLAUDE.md`, "Da guardare sui pezzi" |
| Taglia degli SMD del kit B8; condensatori di X5 a reoforo o SMD | impronte dei passivi | C; S-30 |
| Lunghezze dei fili | connettori e cavi | S; `cablaggio.md:175` (si misurano sulla prima zampa) |

## 5. Requisiti in breve

Numerati per i passi successivi dello studio. Fra parentesi la sezione che li giustifica.

- **R-01** Restano ESP32-S3-CAM UICPAL (su strip, estraibile), SSC-32 clone, D42V110F6 sulle slitte e batteria 2S (4.4).
- **R-02** Il carapace si toglie con una sola spina: tutto quello che sta sul carapace passa da un connettore 2 × 8 con chiave, piedinatura di `cablaggio.md:132-143`; quindi almeno una scheda sul carapace e una nel corpo (3.4, 4.4).
- **R-03** La scheda della logica sta nell'inviluppo della basetta: x 22…78, \|y\| ≤ 17,5, sotto 3,3 mm liberi (2.1.7), sopra 8,5 mm all'ESP32 meno i componenti sul suo retro (6,6 sotto la microSD), 4 fori M2 nelle posizioni delle colonnine (3.1).
- **R-04** La scheda del carapace sta nell'inviluppo della 2.1.7 (circa 23 × 30, \|y\| ≤ 15, sotto il dorso a z 34,4, 3,5 di aria sopra), con la testata a 90° sul bordo di coda e la spina verso l'ottagono; non deve toccare l'amplificatore (da x 51,85) né la USB-C (fino a z 20,9) (3.3).
- **R-05** I partitori possono stare sulla scheda della logica solo con l'ADC: lettura in rapporto, riferimento uguale all'alimentazione dei partitori (1.3, 2).
- **R-06** L'IMU resta fissata rigida al `Corpo_Base`, salvo decisione diversa dell'utente (2, 4.4).
- **R-07** INA260, ToF, microfoni e pulsante restano dove sono: la loro posizione è funzionale (2).
- **R-08** Tutte le schede stanno a valle di F2 (2 A); VBAT tocca solo l'ingresso del regolatore, con pista per 2,5-3 A e lontano dai GPIO (4.1).
- **R-09** Nessun 5 V adiacente a un pin dell'ESP32; buffer a 5 V per i LED con pull-down in ingresso e 330 Ω in uscita, due uscite separate (4.1, 4.2).
- **R-10** Protezione del 5 V dei LED con tenuta di almeno 0,86 A e intervento sotto 2,5 A, lontana da ESP32 e PLA, oppure tetto del firmware rivisto (4.1, S-06).
- **R-11** Il 5 V del regolatore non arriva alla USB attraverso il pin 5V senza una scelta esplicita (oggi D1, S-07) (4.1).
- **R-12** Pull-down dell'abilitazione del rail e della 2813 all'estremo lontano del filo; partitore della batteria con il lato alto alla 2813, o una soluzione con la stessa proprietà: un filo staccato lascia tutto spento o in sicurezza (4.1).
- **R-13** Bus I2C: pull-up rivisti con tutti i moduli (equivalente 1,0-1,4 kΩ), presa Qwiic sulla scheda del carapace, rami lontani dai cavi di potenza (4.2).
- **R-14** I2S con massa fra il gruppo I2S e il bus nel cavo; pull-down dei microfoni da decidere con il pull-up della scheda su GPIO40 (4.2, S-21).
- **R-15** Niente rame sotto e attorno all'antenna dell'ESP32; spazio per il flat della camera (4.2).
- **R-16** Punti di misura per le prove con il multimetro e per la prima accensione senza ESP32; punto per la misura RMT al banco (4.3).
- **R-17** La scelta fra 3V3 della scheda e regolatore proprio dei sensori resta reversibile senza comprare X3 (4.4).
- **R-18** Meno componenti: ogni modulo sostituito da un chip, ogni connettore in più e ogni voce nuova è una proposta da approvare; i moduli già in casa contano come costo zero (2, 4.4).
- **R-19** Saldabile a mano dall'utente, salvo che l'utente scelga il montaggio del produttore (4.3).
- **R-20** Prima di disegnare servono i dati di 4.5; i più urgenti sono la prova a secco dell'ESP32, il disegno della testata a 90° e l'ordine dei pin del regolatore.
