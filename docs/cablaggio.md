# Cablaggio

Tutti i cavi del robot nella versione 2.1.1 (D-067): da dove a dove, percorso (giunti attraversati, fascette, ganci), connettore, numero di fili e sezione.

- Quote in mm nella terna del robot: X avanti, Y a sinistra, Z in alto, origine al centro del corpo all'altezza degli assi dei femori.
- Le posizioni dei pezzi sono lette dal modello Fusion "Hexapod v2.1.0" (ingombri della libreria). Sezioni e connettori vengono dal BOM, segnali e pin da `piano-elettronica-software.md` (2.1–2.5) e da `predisposizioni.md`.
- Stato: **V** verificato, **S** stimato, **C** da confermare. Le voci X sono predisposizioni: il CAD c'è, l'acquisto va approvato (BOM, sezione X).

## 1. Dove stanno i pezzi

| Zona | Pezzi | Posizione (x; \|y\|; z) |
|---|---|---|
| Coda, porta di servizio | T-plug; portafusibile F1; cicalino BX100 sulla presa di bilanciamento; spie dei rail sotto il cicalino (X13); ToF posteriore sulla guancia sinistra (X19); altoparlante sulla guancia destra (X17) | T-plug −80…−64; F1 −83…−61; cicalino −87…−62, z 17…28; ToF y 12…25, altoparlante y −25…−22, tutti e due a x −100…−88 |
| Centro | SSC-32; interruttore 2813 in piedi fra SSC-32 e F1; due morsetti Wago, uno per lato | SSC-32 −51…22, \|y\| ≤ 28, z −7…25 (spine in alto, file degli header a \|y\| 23,5 da x 10,3 a −39,4); 2813 −58…−54; Wago −46…−16, \|y\| 28…36, z −30…−11 |
| Baie anteriori | regolatori D42V110F6 sulle slitte; INA260 sui supporti sopra (X7) | regolatori 14…57, \|y\| 33…45, z −29…2; INA260 14…37, \|y\| 29…40, z 9…31 |
| Davanti, vassoio | basetta con ESP32, D24V22F5, traslatore C1, buffer dei LED, partitore e abilitazione; sotto il vassoio IMU (X4) e ADC (X6); prese dei piedi sul tetto del tunnel; ToF frontale nella mensola della camera (X8) | basetta 22…78, z 6…8; IMU 36…59; ADC 39…70, y 1…18; prese 48…64, y 22…25; ToF 91…99 |
| Sotto il dorso (carapace) | scheda del carapace con la spina IDC (X2); amplificatore (X17); microfoni (X16); pulsante e camera dell'anello (X11); luci dei lobi (X12) | scheda 29…49, \|y\| ≤ 15, z 22…31; ampli 51…70; microfoni 83…96, \|y\| 3…19; pulsante x −40 |
| Tunnel | batteria | −85…79, z −39…−14 |

## 2. Schemi

**Potenza.** Sezioni dal BOM (B5, B6, B12, B14–B17).

```
Batteria 2S ─12 AWG─ T-plug ─14 AWG─ F1 30 A ─14 AWG─ Wago + ─┬─14 AWG─ D42V110F6 S ─14 AWG─ INA260 S ─14 AWG─ VS1 ─ 9 servo
   │                                  (Wago − : massa a stella) ├─14 AWG─ D42V110F6 D ─14 AWG─ INA260 D ─14 AWG─ VS2 ─ 9 servo
   │                                                            └─18/26 AWG─ F2 2 A ─ 2813 ─┬─ D24V22F5 5 V ─┬─ ESP32, pin 5V
   └─ bilanciamento JST-XH 3 poli ─ prolunga C7 ─ cicalino BX100                            │                ├─ PTC ─ LED: poli 1-2 del
                                                                                            │                │   connettore e ramo delle tibie
   VS1, VS2 ─ 1 kΩ ─ LED giallo ─ massa (spie, X13)                                          │                └─ amplificatore (poli 1-2)
   GPIO42 ─ 1N4148 in linea ─ ENA dei due D42V110F6 (R3 22 kΩ ENA–massa su ognuno)                                   ├─ VL della SSC-32
   GPIO41 ─ OFF della 2813;  pulsante ─ A e B della 2813                                     ├─ partitore 100 k / 47 k ─ GPIO1
                                                                                            └─ D24V5F3 3,3 V sensori (X3, se serve)
```

Sulla SSC-32 le barre di rame da 1 mm (B16) corrono lungo le file VS e di massa di ogni lato.

**Segnali.**

```
ESP32-S3 ─ GPIO21 TX / GPIO14 RX ─ traslatore C1 ─ RX / TX della SSC-32 ─ 18 servo, canali in robot.yaml
         ─ GPIO47 SDA, GPIO3 SCL (I2C0, pull-up sulla basetta) ─┬─ IMU 0x68 e ADC 0x48 sotto il vassoio ─ 6 FSR, 2 NTC
                                                                ├─ INA260 0x44 e 0x45 nelle baie
                                                                ├─ ToF frontale 0x30 nella mensola
                                                                └─ connettore a 16 poli ─ scheda del carapace: Qwiic,
                                                                   TCA9534 0x20, ToF posteriore 0x31
         ─ GPIO48 ─ 10 kΩ a massa ─ SN74AHCT125N ── 330 Ω ─┬─ polo 4 ─ anello (4 pixel) ─ 6 lobi (2 pixel ciascuno)
                                                           └─ secondo canale ─ R9 330 Ω in linea ─ ramo delle tibie: 6 × 6 pixel in parallelo (ripetono i primi 6)
         ─ GPIO38 BCLK, 39 WS, 40 dati dei microfoni, 2 dati dell'ampli ─ poli 10-13 ─ 2 microfoni, ampli ─ altoparlante
         ─ camera OV3660: flat da 75 mm (SCCB su GPIO4 e 5, da sola)
```

**Zampa.** I fili della tibia salgono con il cavo del servo del ginocchio (D-058, D-067).

```
punta della tibia: FSR ─ tasca ─ gola 2 × 2 sullo stinco ──┐
striscia LED (6 pixel) ─ capo in alto a z −33 ─────────────┴─ gola del fermo sulla parete +X della culla,
   sotto tre ponticelli ─ testata della culla ─ si unisce al cavo del servo del ginocchio
   ─ ansa del ginocchio ─ fascetta nel blocco del femore ─ ansa dell'anca ─ fascetta del ponte (+ cavo del servo del femore)
   ─ sopra l'asse della coxa (ansa dell'imbardata) ─ sotto il coperchio a z 25 ─┬─ servo: canali della SSC-32
                                                                               ├─ FSR: prese dei piedi
                                                                               └─ LED: prese delle luci (lato −Y, D-069)
```

## 3. Cavi uno per uno

### 3.1 Potenza

| Cavo | Da → a | Percorso | Connettore | Fili e sezione | Stato |
|---|---|---|---|---|---|
| Batteria | pacco → T-plug | codino della batteria, dal tunnel alla coda | T-plug (la batteria ha la femmina) | 2 × 12 AWG | C sesso del T-plug |
| Principale | T-plug → F1 → Wago + ; T-plug → Wago − | in coda, poi lungo il fondo fino ai Wago sotto la SSC-32 | portafusibile in linea ATO con coperchio, fissato al corpo | 14 AWG siliconico, 0,5 m rosso + 0,5 m nero (D-073; anche i codini di T-plug e portafusibile sono 14 AWG) | S |
| Ingresso dei regolatori | Wago → D42V110F6 S e D | dai Wago (x −46…−16) alle baie anteriori (x 14…57), uno per lato | saldati | 14 AWG siliconico, 0,5 + 0,5 m | S |
| Rail servo | D42V110F6 → INA260 → file VS della SSC-32 | INA260 in serie sul positivo all'uscita di ogni regolatore; poi alla fila VS del suo lato | morsettiera dell'INA260 (C: deve reggere 13 A); barre B16 sulla SSC-32 | 14 AWG siliconico, 0,6 + 0,6 m (D-073) | S, C morsettiera: quella da 3,5 mm dell'INA260 potrebbe prendere al massimo 16 AWG, e allora l'ultimo tratto si salda |
| Ramo logica | Wago + → F2 → 2813 | in coda: F2 in linea fra i Wago e la 2813 | portafusibile MINI | codini 18 AWG del portafusibile, poi 26 AWG (D-073: regge i 2 A di F2) | S |
| 5 V e VL | 2813 → D24V22F5 (basetta) → ESP32; 2813 → VL della SSC-32; 2813 → R6 (100 kΩ, saldata sull'uscita della 2813, in guaina) → partitore → GPIO1 | dalla 2813 (x −56) alla basetta lungo il fianco del tunnel | saldati; VL con un Dupont (C4) | 26 AWG, più colori (circa 2 m in tutto) | S |
| 5 V dei LED | D24V22F5 → PTC → poli 1-2 del connettore del carapace; → ramo delle tibie | sulla basetta | saldati | 26 AWG fino alla basetta | S |
| Abilitazione del rail | GPIO42 → D2 (1N4148) in linea nella guaina, anodo dal lato della basetta → ENA dei due regolatori; R3 da 22 kΩ fra ENA e massa su ogni regolatore | dalla basetta alle due baie | saldati; D2 e R3 non stanno sulla basetta (`guida/schemi/schemi.md`, S-20: con la R3 sul regolatore un filo staccato lascia il rail spento) | 26 AWG, tre fili dopo il diodo | S, valori da provare al banco |
| Spegnimento | GPIO41 → OFF della 2813 | dalla basetta alla 2813 | saldato; 100 kΩ a massa se scatta da sola (C) | 26 AWG | S |
| Pulsante | pulsante (x −40) → scheda del carapace → poli 15-16 → basetta → A e B della 2813 | sotto il dorso, poi nel cavo piatto | contatti a saldare sul pulsante; spina IDC | 2 fili | S |
| Spie dei rail (X13) | file VS1 e VS2 della SSC-32 → 1 kΩ → LED giallo → massa | dalla SSC-32 alla linguetta in coda sotto il cicalino; il LED si infila da dentro con il colletto nella lamatura Ø4,2 × 1 della linguetta e la cupola sporge di circa 4 verso la porta (dalla verifica della 2.1.7: prima entrava di 3,3 mm nell'ingombro di F1). I reofori si piegano subito verso l'esterno (\|y\| > 17): fra la linguetta e l'ingombro di F1 restano 0,6 mm | saldati | 2 + 2 fili, 26 AWG | S; C reofori contro F1 vero |
| Bilanciamento | presa JST-XH del pacco → prolunga C7 → cicalino BX100 | dal tunnel alla coda | JST-XH 3 poli | 3 fili | S; si stacca a fine uso |

### 3.2 Servo

Ogni servo ha il suo cavo a 3 fili (massa, +6 V, segnale), lungo 32 cm dichiarati: 30 utili tolta la spina. I percorsi sono quelli di `calc/cavi_servo.py`, con le anse di imbardata (10), anca (17) e ginocchio (20) e il 15 % in più per curve e fascette. Le spine vanno sui canali in alto della SSC-32; i canali sono in `robot.yaml` (C, proposta: lato sinistro 0–15, destro 16–31).

| Zampa | Canali coxa / femore / ginocchio | Percorso coxa | Percorso femore | Percorso ginocchio, margine | Prolunga |
|---|---|---|---|---|---|
| AS | 0 / 1 / 2 | 129 | 180 | 295, +5 mm (2 %) | sì, sul ginocchio |
| MS | 6 / 7 / 8 | 70 | 117 | 231, +69 mm (23 %) | no |
| PS | 13 / 14 / 15 | 112 | 158 | 267, +33 mm (11 %) | sì, sul ginocchio |
| AD | 16 / 17 / 18 | 129 | 181 | 295, +5 mm (2 %) | sì, sul ginocchio |
| MD | 22 / 23 / 24 | 70 | 117 | 231, +69 mm (23 %) | no |
| PD | 29 / 30 / 31 | 112 | 158 | 267, +33 mm (11 %) | sì, sul ginocchio |

- **Coxa**: il cavo sale dalla culla nella baia e va sotto il coperchio fino al canale. Non attraversa giunti.
- **Femore**: esce dall'alto della culla della coxa, sull'asse dell'anca. Passa sul braccio del ponte (fascetta da 2,5 mm nelle feritoie a X 24, \|Y\| 5,5: `cox_fascetta_x`, D-061; era a X 28 in D-058) e sopra l'asse della coxa, dove l'imbardata cambia meno la lunghezza. Entra sotto il coperchio a z 25. Attraversa un giunto, l'imbardata.
- **Ginocchio**: esce dalla finestra del cavo nella testata della culla della tibia, sull'asse del ginocchio. Fa l'ansa del ginocchio e passa nella fascetta dentro il blocco del femore (feritoie a X 79,5, tunnel a Z 10, D-061). I 22–40 mm di D-058 valgono per la fascetta di prima, vicino all'anca: dall'uscita del cavo alla fascetta nel blocco sono 57,4 mm a γ 29°, 40,5 a 90° e 27,2 a 150° [S]; il valore vero si misura sulla prima zampa (P-060). Segue l'ansa dell'anca, 11–56 mm al variare di α, poi ponte, imbardata e canale come il femore. Attraversa tre giunti.
- **Prolunghe** (BOM C5): 4 JR maschio-femmina da 15 cm, 22 AWG, sui ginocchi delle zampe d'angolo. Le giunzioni si chiudono con il termorestringente (C6).
- I pettini per le anse dei cavi nelle baie posteriori sono in backlog: pezzi separati, da disegnare con le lunghezze misurate (`CLAUDE.md`, Backlog).

### 3.3 Zampa: sensore di forza e luci della tibia

| Cavo | Da → a | Percorso | Connettore | Fili e sezione | Stato |
|---|---|---|---|---|---|
| Sensore di forza (X5) | FSR sotto la punta dello stinco → prese dei piedi → partitore (10 kΩ 1 % al 3,3 V, 100 nF a massa) → ADS7830, canali 0–5 | coda dell'FSR piegata sul raccordo della punta, saldature nella tasca 6 × 9. Poi gola 2 × 2 sullo stinco fino al fondo della culla, gola del fermo sulla parete +X della culla sotto tre ponticelli, testata. Infine con il cavo del servo del ginocchio (3.2) fino alla fila delle prese | spina JR femmina (dalle prolunghe C5 avanzate, 2 poli su 3: segnale e massa) sulle prese dei piedi (x 48…64, y 22…25) | doppino 28 AWG siliconico, circa 0,4–0,5 m | S lunghezza; C canali: proposta nell'ordine di `robot.yaml` (AS, MS, PS, AD, MD, PD = 0…5) |
| Luci della tibia (X31) | capo alto della striscia (z −33) → prese delle luci (x 48…64, y −25…−22) → 5 V dopo il PTC, massa, dato dal buffer con R9 (330 Ω) in linea nella guaina vicino alla basetta | dal capo della striscia alla gola del fermo, poi come l'FSR | spina JR a 3 poli: massa, +5 V, dato, come un servo | 3 × 30 AWG siliconico | prese nel CAD dalla 2.1.2 (D-069) |

- **Fili che attraversano i giunti**, per zampa: 8 al ginocchio e all'anca (servo del ginocchio, 2 dell'FSR, 3 delle luci). All'imbardata sono 11, con i 3 del servo del femore.
- **Gola del fermo** (D-067): larga 4 e profonda 0,8 sulla parete +X della culla, da z −33 a +12,45, a Y 4,4…8,4. Sta fuori dalle finestre a rombo e dai tappi del guscio. I tre ponticelli a z −28, −10 e +6 lasciano 1,1 mm sotto di sé. Si infilano i fili prima di saldarli all'altro capo.
- **Lungo la zampa passano solo massa e segnale dell'FSR, mai il 3,3 V** (`piano-elettronica-software.md` 2.2). Il 5 V delle luci ha la sua massa.

### 3.4 Bus dei sensori (X1) e ToF frontale

Bus I2C0: GPIO47 SDA, GPIO3 SCL, 3,3 V, 400 kHz. Ogni ramo ha 4 fili: massa, 3,3 V, SDA, SCL. Si usano cavetti Qwiic (JST SH 4 poli) dove la scheda ha la presa, altrimenti fili saldati.

| Ramo | Da → a | Percorso | Stato |
|---|---|---|---|
| Vano sotto il vassoio | basetta → IMU (GY-6500 a 0x68, oppure la Pololu predisposta a 0x6B; 4 fili saldati sulle piazzole, senza pin: sotto il vassoio non c'è altezza, D-074) e ADS7830 (0x48) | dall'asola del vassoio (dalla 2.1.7 7 × 4, fuori dalla basetta a x 26,5–33,5, y 18–22: la spina Qwiic 6 × 2,9 passa; i fili non passano più sotto la basetta, D-076). Il cavetto dell'ADC va nella presa STEMMA QT di coda (x 39): quella di testa è chiusa dalla colonna del vassoio a (75; 12,5). La spina con 2 mm di fili dritti resta a 0,7 dalla colonna di (30; 12,5) (verifica della 2.1.7) | S |
| Baie anteriori | basetta → INA260 sinistro (0x44) e destro (0x45) | passaggio fra SSC-32 e vassoio, clip sul tetto | S |
| ToF frontale (X8) | basetta → VL53L7CX nella mensola della camera | lungo la torretta. Alimentato dal pin VDD a 3,3 V con VIN scollegato. Prende 0x30 a ogni accensione mentre il posteriore è tenuto spento | V alimentazione; S percorso |
| Carapace | basetta → poli 5–8 del connettore → scheda del carapace | cavo piatto (percorso in 3.5bis) | S |
| NTC dei regolatori (X14) | NTC sulla bobina di ogni regolatore → partitore (10 kΩ 1 %) → ADS7830, canali 6 e 7 | dalle baie al vano sotto il vassoio, fuori dal camino dei regolatori | S |

Il bus misura in tutto circa 1,1 m: 0,8 nel corpo e 0,3 nel carapace (S). Sta almeno 10 mm lontano dai cavi da 12–16 AWG e li incrocia a 90°.

### 3.5 Carapace

Tutto quello che sta sul carapace passa dalla **scheda del carapace** (X2): una striscia di millefori sotto il dorso, 21,5 × 30 a x 29,5…51 (dalla 2.1.7, D-076: la testata 2 × 8 sta a 90° sul bordo di coda e la spina esce orizzontale verso la coda, dentro l'ottagono; la chiave è sul lato lontano dalla scheda; la scheda finisce prima dell'amplificatore, che comincia a x 51,85). La collega alla basetta un **cavo piatto a 16 vie**, lungo circa 15 cm, saldato sulla basetta e con la spina IDC sulla scheda; la spina si sfila dall'ottagono.

**3.5bis Percorso del cavo piatto** (verifica della 2.1.7, `assieme.py` → `cavo_piatto`, scatole provvisorie, misure S). Il nastro intero (20,3 × 1,3) dalla spina non arriva alla basetta: sotto ci sono le USB-C dell'ESP32, davanti la testata, dietro le spine dei servo della SSC-32, e una piega a 45 gradi larga 20,3 non sta fra la spina e la testata. Funziona così:
1. dopo il fermacavo il nastro sale sul dorso della spina (x 18,2…19,5) e piega in avanti sopra la spina (z 28,5…29,8);
2. subito dopo il fermacavo si divide in **due strisce da 8 conduttori** (10,16), tagliando fra i conduttori 8 e 9;
3. ogni striscia gira a 45 gradi verso destra (−Y) davanti alla testata (x 19,2…29,4). La striscia destra resta sotto, la sinistra passa sopra la piega della destra (z 31,2…32,5, a 0,3 sotto la battuta dell'ottagono, z 32,8);
4. le due strisce scendono una dietro l'altra di fianco all'ESP32 (y −14,4…−17,0; il PCB finisce a y −14,15) fino alla basetta;
5. in basso i conduttori si aprono a ventaglio verso i fori della riga 13 (x 23,8…59,3).
Nessun urto con il modello; casi di controllo: tutto 0,4 più in alto tocca la battuta dell'ottagono, 0,3 verso il centro tocca il PCB dell'ESP32. Le pieghe, lo spessore del fermacavo e il raggio di curva vanno provati sul pezzo (C).

**Scheda alzata di 0,6** (verifica della 2.1.7): bugne della scheda alte 2,9 (`sch_bugna_h`, erano 3,5 come quelle dell'ampli), faccia bassa della millefori a z 29,9. Così la chiave della spina (fondo a z 21,4) passa 0,54 sopra le USB-C (z 20,86): sfilando la spina verso la coda per 2–8 mm con 0,3 o 0,5 di scarto di fianco non tocca (prima, a 0,3 di fianco, toccava). Il foro dell'inserto M2 è profondo 3,4 (`sch_ins_l`: inserto da 3 più 0,4) e sotto la fascia restano 0,5 di dorso come prima: le viti della scheda diventano **M2 × 4** (2,4 nell'inserto; con la M2 × 5 la punta arriverebbe sul fondo).

Piedinatura della testata 2 × 8, la stessa di `predisposizioni.md` 2.3:

| Polo | Segnale | Polo | Segnale |
|---|---|---|---|
| 1 | +5 V (LED e audio) | 2 | +5 V (LED e audio) |
| 3 | massa | 4 | dato dei LED a 5 V (dopo il buffer) |
| 5 | massa | 6 | SCL |
| 7 | +3,3 V sensori | 8 | SDA |
| 9 | massa | 10 | BCLK I2S |
| 11 | WS I2S | 12 | dati dei microfoni |
| 13 | dati verso l'amplificatore | 14 | riserva (XSHUT del ToF del mento, X25) |
| 15 | pulsante A (2813) | 16 | pulsante B (2813) |

| Cavo | Da → a | Percorso | Connettore | Fili | Stato |
|---|---|---|---|---|---|
| Catena LED (X9, X11, X12) | scheda → anello del pulsante → lobi PS, MS, AS, AD, MD, PD | dalla scheda lungo il lato sinistro dell'ottagono fino alla camera dell'anello. Entra dalla tacca verso la coda ed esce dalla stessa tacca. Poi lungo i fianchi nei ganci sotto il dorso (x −40, 0, 40 e, dalla 2.1.7, ±75, \|y\| 41,8–47,2), con il passaggio da sinistra a destra davanti, lungo Y a x 75, in tre ganci (y −24, 0, 24) fra l'amplificatore e le paratie della testa. Tratti dritti dal CAD (dai centri dei ganci, in pianta): al più 40 mm sui fianchi, circa 10 dal gancio a x ±75 alla luce del lobo d'angolo, circa 25 per tratto davanti: la striscia si taglia sommando questi tratti più le scorte, sul primo carapace | saldati sulle piazzole della striscia | 3 × 30 AWG (5 V, dato, massa) | S percorso; 16 pixel in tutto (D-068) |
| Dentro la camera dell'anello | due pezzi da due pixel (16,7 mm a 120 LED/m, D-068) nelle sedi del fondo, a Y ±(6,5…11,9) | entra al capo DIN del pezzo +Y, dalla parte della coda. Dal capo DOUT un ponticello di 3 fili gira attorno al corpo del pulsante sul lato della testa e va al capo DIN del pezzo −Y. Dal capo DOUT del pezzo −Y esce verso la tacca | saldati | 3 + 3 + 3 fili da 30 AWG | V spazio nel CAD (camera Ø32 × 6, D-067) |
| Pulsante | pulsante → scheda → poli 15-16 | sotto il dorso, circa 9 cm | saldati | 2 fili | S |
| Microfoni (X16) | due schede (x 83…96, \|y\| 3…19) → scheda | sotto il dorso, circa 8 cm [S]: dal CAD 42,6–45,1 mm in linea retta, più la scorta; si taglia a misura sul primo carapace | saldati | 5 per scheda: 3,3 V, massa, BCLK, WS, dati. I dati dei due microfoni sono uniti sul polo 12, con un pull-down da 100 kΩ verso massa sulla scheda del carapace (D-074); L/R (SEL sulla Adafruit) a massa su uno e a 3,3 V sull'altro. MS3625: VDD, GND, SCK, WS, SD, L/R | S |
| Amplificatore (X17) | scheda → ampli generico (x 51…70, pin verso la scheda, D-074) | sotto il dorso | saldati | 5: 5 V, massa, BCLK, WS, dati | S |
| Altoparlante | ampli → altoparlante tondo da 15 mm sulla guancia destra di coda | sotto il dorso, dalla testa alla coda, circa 17 cm | il cavetto dell'altoparlante si taglia (connettore da 1,25) e si allunga; nella morsettiera o saldato | 2 | S |
| ToF posteriore (X19) | scheda → VL53L1X sulla guancia sinistra di coda, avvitato con due viti M2 × 5 in fori pilota Ø1,7 (dalla 2.1.7) | sotto il dorso, circa 20 cm [S]: dal CAD circa 126–129 mm in pianta più 12 di quota, con il cavo che gira fuori dall'ottagono; si taglia a misura sul primo carapace | saldati | 5: 3,3 V, massa, SDA, SCL, XSHUT (dal TCA9534) | S |
| Espansione | cavo Qwiic tagliato, saldato su quattro piazzole della scheda (niente presa, `piano-pcb.md` DU-2) | a carapace tolto: dalla 2.1.7 la scheda sta a x 29,5…51, l'ottagono finisce a x 28 | saldato | 4 | V standard Qwiic |

### 3.6 Comandi dei servo e camera

| Cavo | Da → a | Connettore | Fili | Stato |
|---|---|---|---|---|
| Seriale della SSC-32 | ESP32 GPIO21 TX e GPIO14 RX → traslatore C1 → SSC-32 | Dupont femmina (C4) | 4: TX, RX, massa, VL | V pin (D-012) |
| Camera | OV3660 → ESP32 | flat da 75 mm | — | V |
| USB | ESP32 → Mac al banco, poi l'eventuale computer di bordo | USB-C della scheda, sotto l'ottagono (con lo zaino il cavo esce dalla tacca del suo sportellino) | — | — |

## 4. Smontaggio

- **Carapace**: si toglie lo sportellino, si sfila la spina IDC dall'ottagono, si svitano le 4 viti, si stacca il cicalino dalla presa di bilanciamento e si solleva. Anello, fondo, lobi, microfoni, ampli, altoparlante e ToF posteriore restano sul carapace con i loro fili.
- **T-plug** (sezionamento d'emergenza): sta 7 mm dentro la porta di coda, appoggiato al portafusibile, con 3,3 mm sotto il cicalino. Si prende con la punta delle dita sul retro e sui fianchi: 7 mm d'aria verso l'altoparlante, 10,4 mm verso la guancia sinistra. Il ToF posteriore copre solo l'angolo in alto a sinistra (3 × 3 mm) visto da dietro e sta 8 mm più indietro (verifica della 2.1.2). Dalla 2.1.7 le fessure del tetto sono aperte verso la coda e il pacco si sfila con T-plug e JST-XH attaccati (prova con corpi temporanei, sportello tolto, carapace montato: libero da 0 a 165 mm con la metà femmina del T-plug sul lato destro; **con la spina sul lato sinistro tocca fra 10 e 20 mm il ToF posteriore (fino a 20,6 mm³) e anche il carapace (16,7 mm³)**, quindi la metà femmina si porta fuori dal lato destro, quello dell'altoparlante; con la spina 1 mm più alta, a destra, passa. Rifatta con le correzioni della verifica della 2.1.7: pacco da 139,65 con la schiuma da 2,25 davanti). Si prova a mano sul primo carapace (guida 11.03); se è scomodo, una linguetta di nastro sulla metà lato batteria.
- **Zampa**: si staccano dalla SSC-32 le tre spine dei servo, poi la spina dell'FSR dalle prese dei piedi e quella delle luci dalle sue prese. Tutti questi fili restano sulla zampa.

## 5. Aperti

1. **Prese delle luci delle tibie**: fatte nella 2.1.2 (D-069). Seconda fila di sei spine JR a 3 poli (massa, +5 V, dato, l'ordine dei servo) speculare a quella dei piedi, sul tetto del tunnel a x 48…64, y −25…−22, nessuna interferenza.
2. **Il ramo delle tibie ripete i primi sei pixel della catena**. Oggi sono i quattro dell'anello e i due del primo lobo, quindi le tibie avrebbero gli stessi colori. Per tenerle indipendenti servono sei pixel nascosti in testa alla catena, per esempio 5 cm di striscia sulla basetta. Da decidere con X31.
3. **Tetto di corrente**: i 600 mA del firmware devono contare ogni pixel delle tibie sei volte (36 pixel reali per 6 indirizzi).
4. **Lunghezze dei fili** (S): si misurano sulla prima zampa montata, prima di tagliare gli altri cinque.
5. **Pettini delle anse** nelle baie posteriori: in backlog, come pezzi separati sulla parete del tunnel, da disegnare dopo il montaggio di una zampa con le lunghezze misurate (`CLAUDE.md`, Backlog).
6. **Wago**: il positivo sta sul lato sinistro (+Y), il negativo, massa a stella di tutti i rami, sul destro (−Y), come nell'assieme (`assieme.py` → `Wago_piu`, `Wago_meno`).
7. **Cavo piatto del carapace** (verifica della 2.1.7, 3.5bis): il percorso libero c'è solo con il nastro diviso in due strisce da 8 dopo il fermacavo. Va provato sul pezzo prima di saldare la basetta (pieghe, fermacavo, raggio); se non va, la riserva è la soluzione B di P-002 (cavo saldato sulla scheda e giunzione IDC volante nell'ottagono), da far scegliere all'utente.
8. **Reofori delle spie (X13) e F1**: con la lamatura il corpo del LED resta fuori dall'ingombro di F1 (40 × 22 × 15, S), i reofori no. Da guardare sul portafusibile Neuftech in casa: se le estremità verso i cavi sono più strette dell'ingombro, i reofori passano; se no, piegarli lungo la linguetta non basta (verifica del 16 ottobre: resterebbero a filo del corpo del LED, senza posto per saldatura e guaina) e si spostano F1, la coppia di T-plug e le costole di 2,5 mm verso la testa (P-139, 2.1.8).
