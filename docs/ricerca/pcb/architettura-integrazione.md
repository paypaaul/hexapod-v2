# Architettura 3, "massima integrazione": PCB montate dal produttore

Studio preliminare del 16 ottobre 2026. Fa parte dello studio sulle PCB al posto delle millefori (D-076): i requisiti stanno in `requisiti.md` (R-01…R-20), produzione e costi in `produzione.md`. Qui si descrive **una** delle architetture possibili, quella che integra di più: schede montate dal produttore (PCBA), chip al posto dei moduli comprati dove conviene, connettori con chiave per tutti i cavi, punti di prova. Il disegno vero si fa con l'utente in una versione successiva. **Niente è approvato né comprato**: ogni voce nuova è una proposta.

- Quote in mm nella terna del robot (X avanti, Y a sinistra, Z in alto, origine al centro del corpo sul piano dei femori), come in `requisiti.md:5`.
- Stato: **V** verificato (fonte primaria o modello CAD), **S** stimato (calcolo, catalogo non riletto, fonte di terzi), **C** da confermare (sul pezzo, nel CAD, nel preventivo).
- Prezzi dei chip letti il 16 ottobre 2026 sulle pagine di JLCPCB e LCSC (link nel testo); cambiano ogni giorno e vanno rifatti il giorno dell'ordine.

## 0. In breve

Tre PCB al posto delle tre millefori, con una scheda in più di sostanza: la striscia dei partitori diventa una vera **scheda dei sensori del corpo** che porta anche l'ADC e, se l'utente lo approva, l'IMU.

| Scheda | Sostituisce | Misura | Dove |
|---|---|---|---|
| **PCB-L**, logica | basetta dell'ESP32 e traslatore KAmod | 56 × 35, come oggi | sul vassoio, sotto l'ESP32 |
| **PCB-S**, sensori del corpo | striscia dei partitori, ADS7830 Adafruit, piastrina e GY-6500 (opzione) | circa 35 × 30 | vano sotto il vassoio, sulle quattro bugne di ADC e IMU |
| **PCB-C**, carapace | scheda del carapace, SparkFun TCA9534, modulo MAX98357A | circa 43,5 × 30 | sotto il dorso, dalla testata al posto dell'amplificatore |

Le PCB arrivano con tutti gli SMD già saldati da JLCPCB (montaggio Economic, una faccia). L'utente salda solo il regolatore D24V22F5 e i codini dei cavi all'estremo lontano (2813, regolatori, prese, moduli), poi innesta. Costo stimato consegnato: **circa 140–175 €** con 5 serie montate, **circa 100–110 €** con un pannello e 2 serie montate su 5 (S, capitolo 7), contro 8–24 € delle sole schede nude (`produzione.md:270-271`).

## 1. Schede: numero, sagome, posizione

Il numero minimo è due, una nel corpo e una sul carapace, perché il carapace si toglie staccando una sola spina (R-02, `requisiti.md:217`, `:303`). Questa architettura ne usa tre perché nel corpo ci sono due piani separati dal vassoio, raggiungibili in momenti diversi del montaggio (`requisiti.md:178`, `:256`): la logica sopra il vassoio, i sensori sotto.

### 1.1 PCB-L, scheda della logica

| Dato | Valore | Stato, fonte |
|---|---|---|
| Sagoma | rettangolo 56 × 35, x 22…78, \|y\| ≤ 17,5, spessore 1,6 (z 5,9…7,5) | V, inviluppo di oggi (`requisiti.md:16`, `:158`); R-03 |
| Fissaggio | 4 fori Ø2,2 non metallizzati a (29; ±6,8) e (75,5; ±6,5), sulle colonnine del vassoio, M2 × 5; anello senza rame di 1 mm attorno alla testa | V posizioni (`requisiti.md:159`); regola da `produzione.md:190` |
| Sopra | 8,5 fino alla PCB dell'ESP32 (z 16,0), 6,6 sotto la sede della microSD (x 22,5…37,5, \|y\| ≤ 7) | S (`requisiti.md:161-162`) |
| Sotto | 3,3 liberi fino al vassoio nella 2.1.7 (oggi 0,3 sulle teste M3) | V 2.1.6, bozza 2.1.7 (`requisiti.md:160`) |
| Faccia dei componenti | tutti gli SMD **sopra**, verso l'ESP32 (montaggio a una faccia, `produzione.md:83`); sotto solo i reofori dei THT, tagliati a 1,5 | S |
| Zona senza rame | x ≥ 74 su entrambe le facce, sotto l'antenna stampata del modulo (modulo x 55,6…81,1; l'antenna occupa l'estremo anteriore) | S: regola Espressif non riletta (`requisiti.md:245`); C la quota 74 |
| Bordi | coda (x 22) a 3,1 dalla morsettiera VS/VL della SSC-32; fianchi liberi fino alle colonnine del coperchio (\|y\| 18,8 fra x 36,3 e 43,7) e alle prese (\|y\| 22,1, ma sotto, a z ≤ −0,4) | V (`requisiti.md:165`, `:169`) |

La sagoma non cambia: la PCB-L entra nel CAD al posto del componente `Basetta` con le stesse colonnine. Cambiano solo i corpi dei connettori sui bordi (capitolo 4), che sporgono dal rettangolo e vanno provati nel CAD [C].

### 1.2 PCB-S, scheda dei sensori del corpo

| Dato | Valore | Stato, fonte |
|---|---|---|
| Vano | x 34…71, \|y\| ≤ 16, z −9,4 (tetto del tunnel) … +1,0 (vassoio) | V (`requisiti.md:178`) |
| Sagoma proposta | x 35…70, \|y\| ≤ 15: **35 × 30**, angoli smussati | S, da provare nel CAD |
| Fissaggio | le **quattro bugne esistenti**, tutte con la cima a z −5,4: ADC a (41,55; 9,6) e (66,95; 9,6), IMU a (38,5; −7,5) e (56,5; −7,5), inserti M2 | V posizioni (`requisiti.md:179-180`, `fori.json` `ins_ads_*`, `ins_imu_*`); la quota comune −5,4 si ricava da "ADC z −5,4…−0,7" e "piastrina z −5,4…−2,9": S finché non si rilegge nel modello |
| Piano della scheda | z −5,4…−3,8 | S |
| Sopra | 4,8 fino al vassoio (z +1,0, colonne della 2.1.7) | S |
| Sotto | 4,0 fino al tetto del tunnel, fra le bugne | S |
| Ingombri vicini | colonne del vassoio della 2.1.7 a (30; ±12,5) e (75; ±12,5): fuori sagoma; asola del bus della 2.1.7 x 46,5…53,5, y 18…22: fuori sagoma, ci passano i cavi | V (`requisiti.md:181`, `:184`) |

La PCB-S è avvitata al `Corpo_Base` (il tetto del tunnel), che porta le zampe: per questo può portare l'IMU senza tradire la scelta "IMU rigida sul `Corpo_Base`" (`predisposizioni.md:143`, R-06). Resta una decisione dell'utente (capitolo 3.2).

### 1.3 PCB-C, scheda del carapace

| Dato | Valore | Stato, fonte |
|---|---|---|
| Sagoma proposta | x 26,5…70, \|y\| ≤ 15: **43,5 × 30**. Parte di coda come la scheda della 2.1.7 (circa 23 di lunghezza, testata sul bordo posteriore); parte di testa al posto del modulo dell'amplificatore (x 51,85…69,55, \|y\| ≤ 8,75) | S; 2.1.7 in bozza (`requisiti.md:197`); il verso dell'allungamento della 2.1.7 è fra i dubbi della revisione (`requisiti.md:198`): C |
| Piano | come oggi, faccia alta a z 30,9, componenti sotto (z 29,3 e in giù) | V oggi (`requisiti.md:190`) |
| Fissaggio | due bugne Ø5,5 di testa della 2.1.7 (x ≥ 41,5, \|y\| 12,5) più le due bugne dell'amplificatore a (67,35; ±6,5); quelle di coda a x 32 tolte se la testata le occupa | V bugne dell'amplificatore (`requisiti.md:140`); S la scelta |
| Sopra | 3,5 di aria fino al dorso (z 34,4) fra le bugne | V (`requisiti.md:192`) |
| Sotto | 11,7 fino alla PCB dell'ESP32, 9,7 sul connettore del flat (x 40,75…45,25), e oltre x 55,6 il modulo dell'antenna fino a z 20,8: **8,5** | S (`requisiti.md:193`) |
| Ai lati | pozzetti delle viti del carapace a (40; ±22,5): \|y\| libero fino a 17,8 | V (`requisiti.md:196`) |
| Davanti | si ferma a x 70: oltre (x 69,6…81) starebbe sopra l'antenna (`requisiti.md:209`) | S |

Rame sopra l'antenna: la PCB-C arriva a x 70, dove oggi c'è già il circuito del modulo dell'amplificatore con il suo piano di massa, e resta a 8,5 sopra il modulo; non peggiora la situazione di oggi [S]. I microfoni restano moduli: per portarli sulla PCB-C bisognerebbe arrivare a x 96, sopra l'antenna (`requisiti.md:141`, `:210`).

## 2. Schema a blocchi

```
                         CORPO                                              CARAPACE
 2813 (coda) ── XH4: VBAT, GND, OFF, SENSE ──┐                    ┌──────────── PCB-C (sotto il dorso) ───────────┐
   R6 100k, 100k su OFF restano alla 2813    │                    │ J2 2x8 a 90° ─┬─ CE1 470 µF ── GH3: catena LED │
 2813 A, B ── XH2: pulsante ─────────────────┤                    │  (chiave)     ├─ TCA9534 0x20 ─ GH5: ToF post. │
                                             │                    │               │   (XSHUT, 7 I/O su piazzole)   │
 ┌──────────────── PCB-L (sul vassoio) ──────┴─────────────┐      │               ├─ MAX98357A ─── GH2: altoparl.  │
 │ VBAT ─ D24V22F5 (modulo) ─ 5V_REG ─┬─ SS34 ─ 5V ESP32   │      │               ├─ GH5: microfoni MS3625 x2      │
 │                                    ├─ PTC 1812 ─ 5V_LED │      │               ├─ SH4: Qwiic di espansione      │
 │                                    └─ (LDO 3,3 V, DNP)  │      │               └─ GH2: pulsante ─┐ (poli 15-16) │
 │ 3V3 ESP32 ─ ponticello a 3 vie ─ 3V3S                   │      └─────────────────────────────────┼──────────────┘
 │ GPIO48 ─ 10k↓ ─ AHCT125 ch1 ─ 330 ─┐ DATA carapace      │  cavo piatto 16 vie, IDC ai due capi │
 │                AHCT125 ch2 ─ 330 ─── XH3: luci tibie ───┼──► 6 prese delle luci (R9 sulla PCB) │
 │ GPIO21 ─ AHCT125 ch3 ─ 5 V ─┐                           │                                      │
 │ GPIO14 ◄─ partitore 2k2/3k3 ┴─ XH3: seriale ────────────┼──► SSC-32 (Dupont lato SSC)         │
 │ GPIO38 ◄─ AHCT125 ch4 / piazzola (misura RMT, P2)       │                                      │
 │ GPIO42 ─ 1N4148W ─ XH3: ENA S, ENA D, GND ──────────────┼──► D42V110F6 x2 (R3 22k su ognuno)  │
 │ GPIO41 ─ OFF; GPIO1 ◄─ R7 47k ─ SENSE (100 nF)          │                                      │
 │ GPIO47/3 ─ pull-up ─ SH4 x4: INA260 S, INA260 D, PCB-S, ToF frontale                           │
 │ J-CAR 2x8 a 90° (chiave) ───────────────────────────────┼──────────────────────────────────────┘
 │ GPIO38, 39, 40, 2 (I2S) e 5V_LED, 3V3S, DATA, SDA, SCL ─┘ verso J-CAR, piedinatura di cablaggio.md:132-143
 └─────────────────────────────────────────────────────────┘
        │ SH4 Qwiic (3V3S, GND, SDA, SCL), dall'asola del bus
 ┌──── PCB-S (vano sotto il vassoio, su Corpo_Base) ───────┐
 │ ADS7830 0x48, REF = 3V3S filtrato                        │
 │ 8 partitori 10k 1 % + 100 nF ─ A0…A7                     │
 │ LSM6DSO 0x6B (opzione) o strip per la GY-6500 (0x68)    │
 │ SH4 Qwiic passante (X15, X32, X33)                       │
 │ GH8 sinistra: FSR AS, MS, PS + NTC S, con le masse       │
 │ GH8 destra:   FSR AD, MD, PD + NTC D, con le masse       │
 └──────────────────────────────────────────────────────────┘
```

Note [S]:
- Le correnti dei servo non toccano nessuna scheda: restano su fili, Wago, INA260 e SSC-32 (`produzione.md:19`).
- I quattro canali dell'SN74AHCT125 diventano tutti utili: due per i LED (come oggi, `requisiti.md:24`), uno per il TX verso la SSC-32 (ingressi TTL a 5 V: 3,3 V bastano [S]), uno libero per la misura RMT al banco (`requisiti.md:254`). Il KAmod sparisce (`requisiti.md:131`).
- Il ricevitore (SSC-32 → GPIO14) passa da un partitore 2,2 kΩ / 3,3 kΩ: 5 V diventano 3,0 V, sopra la soglia alta dell'ESP32-S3 (0,75 × 3,3 = 2,5 V [S, datasheet non riletto]). Due resistenze di libreria Basic invece di un modulo. Se la SSC-32 trasmette a 3,3 V il partitore dà 2,0 V, troppo poco: la tensione d'uscita del clone va misurata prima del disegno (C, S-22, `requisiti.md:289`).
- Il pulsante (poli 15-16) attraversa la PCB-L su due piste isolate verso la XH2, lontane da ogni rete della logica: la tensione dei pin A e B della 2813 resta sconosciuta (S-10, `requisiti.md:232`).

## 3. Componenti

### 3.1 Chip al posto dei moduli: cosa si fa e cosa no

| Funzione | Oggi | Architettura 3 | Contenitore, codice | Prezzo per pezzo | Perché | Stato |
|---|---|---|---|---|---|---|
| Buffer dei LED e TX | SN74AHCT125N DIP-14 (X9) + KAmod (C1) | **SN74AHCT125PW** sulla PCB-L, 4 canali usati | TSSOP-14, LCSC [C36365](https://www.lcsc.com/product-detail/C36365.html); in SOIC-14 se ce n'è uno Basic | circa 0,3 $ | toglie il KAmod (2,51 €, da comprare, `BOM.md:70`) | S prezzo; C categoria JLCPCB |
| Protezione del 5 V dei LED | PTC MF-R075 radiale, 0,75 A (X9) | **PTC 1812 da 1,1 A di tenuta, intervento 2,2 A** (per esempio Bourns MF-MSMF110) | 1812 | circa 0,3 $ | chiude S-06: il ramo arriva a 0,86 A (`requisiti.md:26`, `:311`) | S |
| Diodo del 5 V dell'ESP32 | 1N5819 assiale (C3) | **SS34** o simile | SMA | < 0,1 $ | R-11 come oggi | S, Basic da controllare |
| Diodo dell'abilitazione | 1N4148 in linea nella guaina (B11) | **1N4148W** sulla PCB-L | SOD-123 | < 0,05 $ | il pull-down R3 resta su ogni regolatore (R-12): il diodo può stare dove si vuole | S |
| ADC dei piedi | Adafruit ADS7830 #5836 (X6) + striscia | **ADS7830IPWR** sulla PCB-S con gli 8 partitori | TSSOP-16, [JLCPCB C161747](https://jlcpcb.com/partdetail/ADS7830IPWR/C161747), Extended | 1,65–1,72 $ ([LCSC](https://www.lcsc.com/product-image/C161747.html)) | spariscono striscia, 8 fili ADC-striscia, un ramo del bus | V codice e categoria; S prezzo |
| Espansore | SparkFun DEV-17047 (X20, in arrivo il 24 novembre) | **TCA9534PWR** sulla PCB-C, indirizzo 0x20 come oggi | TSSOP-16, [JLCPCB C783615](https://jlcpcb.com/partdetail/TCA9534PWR/C783615), Extended | circa 0,4–0,6 $ | toglie l'adattatore che non trovava posto (S-17, `requisiti.md:139`); **non** la variante "A" (0x38) | V codice; S prezzo |
| Amplificatore | modulo MAX98357A generico (X17, in casa) | **MAX98357AETE+T** sulla PCB-C | TQFN-16 3 × 3 con piazzola termica, [JLCPCB C910544](https://jlcpcb.com/partdetail/MAX98357AETE+T/C910544), Extended | 1,40 $ (circa 10 000 a magazzino) | il modulo e le sue bugne spariscono, 5 fili in meno; si salda solo a macchina (`requisiti.md:140`) | S (pagina letta da una ricerca) |
| IMU | GY-6500 su `Corpo_Piastrina_IMU` (X4, in casa) | **opzione**: LSM6DSO sulla PCB-S (0x6B, già predisposta nel firmware come Pololu #2798) **più** una fila di 4 fori per innestare la GY-6500 se il chip non si monta | LGA-14 2,5 × 3, LCSC C2655100, Extended | circa 4,2 $ (1100 a magazzino, istantanea non datata) | spariscono piastrina e 4 fili; la scheda è avvitata al `Corpo_Base` (R-06) | S; decisione dell'utente |
| Presa di espansione | cavo Qwiic tagliato (X1) | **JST SH 4 poli SMD** (SM04B-SRSS-TB) | [JLCPCB C160404](https://jlcpcb.com/partdetail/Jst-SM04B_SRSS_TB_LF_SN/C160404), Extended | circa 0,3 $ | sulla millefori non si saldava (`requisiti.md:144`) | V codice; S prezzo |
| Regolatore 5 V | Pololu D24V22F5 (B2) | **resta modulo**, saldato sulla PCB-L | 5 pin a passo 2,54 | 17,84 € (`BOM.md:43`) | un convertitore da 2,5 A sotto l'ESP32 è il pezzo più delicato da disegnare (`requisiti.md:129`); variante in 3.3 | V prezzo |
| INA260 | Adafruit #4226 × 2 (X7) | **restano moduli** | — | 21,32 € la coppia (`BOM.md:176`) | portano 13–14 A: servirebbero due schedine di potenza con rame spesso; il chip INA260AIPW su LCSC ha [0 pezzi a magazzino](https://www.lcsc.com/product-image/C181331.html) | V scelta (R-07); S magazzino |
| ToF frontale e posteriore, microfoni, pulsante, 2813 | moduli | **restano moduli** | — | — | posizione funzionale (R-07, `requisiti.md:137-143`) | V |

Il chip SN74AHCT125PW non ha una pagina JLCPCB trovata in questa ricerca: la categoria (Basic, Preferred, Extended) va letta il giorno del disegno [C]. Per gli altri la categoria Extended costa 3,07 $ di caricamento per codice (`produzione.md:90`).

### 3.2 Decisioni che restano all'utente

1. **IMU sulla PCB-S**: cambia D-074 (GY-6500 in casa su piastrina). Proposta: impronta del LSM6DSO e fila di fori per la GY-6500 sulla stessa scheda; alla prima serie si monta il chip su 2 schede e si lasciano le altre senza, così la GY-6500 resta il ripiego. Il fissaggio rigido è quello di oggi (bugne del `Corpo_Base`, 4 viti invece di 2), quindi X23 (vibrazioni) non perde nulla [S].
2. **Amplificatore sulla PCB-C**: il modulo è in casa (costo zero, 10 pezzi). Il chip costa circa 1,4 $ più 3,07 $ di caricamento, ma toglie un modulo, 5 fili e due bugne dal carapace. Il modulo in casa resta un ripiego **solo con un ponticello** (piazzole per 5 fili verso un modulo esterno).
3. **Chi salda le schede**: questa architettura presuppone il montaggio del produttore (TSSOP, TQFN, LGA). Se l'utente preferisce saldare tutto a mano, vale `produzione.md:278-279` e un'altra architettura.

### 3.3 Variante non proposta: regolatore 5 V integrato

Un convertitore sincrono da 3 A in SOT-23-6 con induttore SMD sostituirebbe il D24V22F5 (17,84 €, non ancora comprato) con circa 2 € di parti, e abbasserebbe l'ingombro da 7,2 a circa 4–5 mm [S]. Non la propongo per la prima serie: anello di commutazione accanto ai pin dell'ESP32 e sotto la camera, calore chiuso sotto l'ESP32 da misurare in P4 (`requisiti.md:235`), e se sbaglia il disegno si ferma tutta la logica. Da rivalutare in una seconda serie, dopo la misura di P4.

### 3.4 Elenco dei componenti per scheda

| Scheda | Montati dal produttore (SMD) | Montati dall'utente | Non montati (DNP), per scelte aperte |
|---|---|---|---|
| PCB-L | SN74AHCT125PW, PTC 1812, SS34, 1N4148W; resistenze 0603: R1 10k (GPIO48), R2 e R9 330, R7 47k 1 %, pull-up SDA/SCL, partitore 2k2/3k3 della seriale; condensatori 0603: CS1 e CS2 100 nF, 10 µF sul 5V_REG; 4 prese SH4 | strip femmina 2 × 20 (o dal produttore, capitolo 7), D24V22F5, J-CAR 2 × 8 a 90°, XH4, XH2, XH3 × 3 | LDO 3,3 V da 600 mA (al posto di X3, `requisiti.md:269`); pull-up di riserva; ponticello per GPIO38 |
| PCB-S | ADS7830IPWR, 8 × 10 kΩ 1 %, 8 × 100 nF, 100 nF e 1 µF sull'ADC, LSM6DSO con 100 nF (opzione), 2 prese SH4, 2 prese GH8 | niente (oppure la strip 1 × 4 della GY-6500) | LSM6DSO sulle schede di ripiego; pull-up I2C (mai montati: stanno sulla PCB-L) |
| PCB-C | TCA9534PWR, MAX98357AETE+T con 10 µF e 100 nF, CE1 470 µF 10 V SMD (Ø6,3 × 7,7 [S]), prese GH2 × 2, GH3, GH5 × 2, SH4 | J2 2 × 8 a 90° (THT) | pull-down di GPIO40 (S-21, `requisiti.md:240`): impronta 0603 vuota, valore da decidere al banco; piazzole per un modulo amplificatore esterno |

## 4. Connettori e cavi

Regola: **ogni cavo si innesta con una chiave**, e la saldatura si sposta all'estremo lontano, dove oggi c'è già (2813, regolatori, prese, moduli). Lo scopo è che la PCB si tolga e si rimetta senza saldatore, e che una spina girata non entri.

Famiglie proposte (portate di catalogo JST, non rilette per questo studio [S]):

| Famiglia | Passo | Corrente per contatto | Ritenuta | Dove | Perché |
|---|---|---|---|---|---|
| JST XH | 2,5 | circa 3 A | per attrito, con chiave | PCB-L: 2813, pulsante, seriale, abilitazione, luci delle tibie | il kit di codini XH da 2 a 5 poli con 26 AWG da 200 mm è **già in casa** (C7, `BOM.md:76`); regge il VBAT da 2,3 A (`requisiti.md:43`) |
| JST GH | 1,25 | circa 1 A | **con aggancio** | PCB-S e PCB-C: sensori, microfoni, ToF, altoparlante, LED, pulsante | il robot vibra camminando: la spina deve agganciarsi; cavi da 28–30 AWG come oggi |
| JST SH (Qwiic) | 1,0 | circa 1 A | per attrito | rami del bus | è lo standard di INA260 e dei moduli Adafruit/SparkFun (X1, `requisiti.md:144`) |
| Box header 2 × 8 a 90° + IDC | 2,54 | — | chiave e alette | cavo del carapace, ai due capi | piedinatura e chiave di D-076 (`cablaggio.md:132-143`, `requisiti.md:267`) |

### 4.1 PCB-L

| Connettore | Poli, nell'ordine | Verso | Lunghezza | Note | Stato |
|---|---|---|---|---|---|
| XH4 a 90°, bordo di coda o fianco +Y | VBAT, GND, OFF, SENSE | uscita e pin della 2813 | circa 25 cm (`requisiti.md:61`) | la massa fra VBAT e i segnali: un corto sul connettore non porta 8,4 V su OFF o su GPIO1. R6 e il 100 kΩ di OFF restano saldati alla 2813 (R-12) | S |
| XH2 | BTN_A, BTN_B | pin A e B della 2813 | idem, nello stesso fascio | arriva dai poli 15-16 di J-CAR su piste isolate | S |
| XH3 | TX (5 V), RX, GND | connettore seriale della SSC-32, Dupont femmina all'altro capo (C4) | pochi cm | S-22: il polo di massa si lascia vuoto se la misura dice che crea una doppia massa | S |
| XH3 | ENA_S, ENA_D, GND | pin ENA dei due D42V110F6, con R3 22 kΩ saldata su ognuno | fino alle baie | spina staccata = rail spento (D-019) | S |
| XH3 | 5V_LED, DATA2 (dopo R9 330 Ω), GND | prese delle luci delle tibie (x 48…64, y −25…−22) | circa 10 cm [S] | una sola uscita, poi il fascio si divide verso le 6 prese come oggi | S |
| SH4 × 4, bordo +Y verso l'asola | 3V3S, GND, SDA, SCL (ordine Qwiic) | INA260 S, INA260 D (sono STEMMA QT: cavo X1 intero), PCB-S, ToF frontale (cavo X1 tagliato e saldato sul VL53L7CX) | bus in tutto circa 1,1 m (`requisiti.md:67`) | oggi i rami sono saldati in riga 1 con due fili per foro | S |
| J-CAR, box header 2 × 8 a 90°, bordo −Y | piedinatura di `cablaggio.md:132-143` | PCB-C | circa 15 cm (`requisiti.md:68`) | il cavo piatto oggi è saldato sulla basetta: con due IDC si stacca ai due capi; X2 ha già due spine IDC (`BOM.md:175`) | S; ingombro C |

I connettori della PCB-L sono **a 90° sui bordi**: sopra la scheda ci sono 8,5 mm fino all'ESP32 e solo 3,35 mm di striscia fra il bordo della scheda (\|y\| 17,5) e quello dell'ESP32 (\|y\| 14,15) (`requisiti.md:126`, `:161`), quindi una presa verticale non si innesterebbe con l'ESP32 al suo posto. Le spine entrano di lato, da fuori del rettangolo. Gli ingombri delle spine innestate (circa 6–9 mm oltre il bordo [S]) vanno provati nel CAD contro le colonnine del coperchio (x 36,3…43,7), la morsettiera della SSC-32 e le pareti del corpo [C].

### 4.2 PCB-S

| Connettore | Poli | Verso | Note |
|---|---|---|---|
| SH4 | 3V3S, GND, SDA, SCL | PCB-L, dall'asola del bus | cavo X1 intero |
| SH4 passante | idem | moduli futuri sul bus (X15, X32, X33) | vuoto finché non servono |
| GH8 sinistra | FSR AS, GND, FSR MS, GND, FSR PS, GND, NTC S, GND | prese dei piedi a y +22…+25 e NTC del regolatore sinistro | una massa per sensore, mai il 3,3 V lungo la zampa (`requisiti.md:234`) |
| GH8 destra | idem per le zampe destre | prese a y −25…−22 e NTC destra | |

Le prese dei piedi e delle luci (spine JR sul tetto del tunnel) restano come sono: il loro supporto è ancora da disegnare (P-012, `requisiti.md:145`) e sta fuori dal vano (\|y\| 22,1…24,7). Una PCB con le ali fino alle prese le sosterrebbe, ma non è dimostrato che passi fra vano e prese: da guardare nel CAD [C].

### 4.3 PCB-C

| Connettore | Poli | Verso | Lunghezza (`requisiti.md:99-104`) |
|---|---|---|---|
| J2, box header 2 × 8 a 90°, bordo di coda | piedinatura di D-076 | PCB-L, spina orizzontale verso l'ottagono | circa 15 cm |
| GH3 | 5V_LED, DATA, GND | catena LED: anello del pulsante, poi i lobi | lungo il fianco sinistro |
| GH5 | 3V3, GND, BCLK, WS, DATA | due microfoni MS3625, uniti fra loro | circa 8 cm |
| GH2 | OUT+, OUT− | altoparlante in coda | circa 17 cm, come oggi dall'amplificatore |
| GH5 | 3V3, GND, SDA, SCL, XSHUT | ToF posteriore VL53L1X | circa 20 cm |
| GH2 | BTN_A, BTN_B | pulsante Ø12 | circa 9 cm |
| SH4 | Qwiic | espansione, raggiungibile dall'ottagono | — |

Tutte le prese della PCB-C stanno sulla faccia di sotto (sotto ci sono 8,5–11,7 mm) e guardano verso ±Y o verso la coda; le prese GH a 90° sono alte circa 4,3 mm [S].

### 4.4 Cavi

- **Codini XH**: dal kit in casa (C7). Per i connettori della scheda servono le prese XH **a 90°** (S…B-XH-A), che il kit probabilmente non ha (C: guardare il kit).
- **Codini GH**: da comprare già crimpati (proposta, non nel BOM). Crimpare GH e SH a mano chiede una pinza dedicata: la si evita.
- **Cavi Qwiic**: X1, già approvati (`BOM.md:163-164`).
- **Cavo piatto**: quello di X2, con la seconda spina IDC al posto della saldatura sulla basetta. Serve **una seconda testata 2 × 8 a 90°** (voce nuova, prezzo simile alla prima, S).

## 5. Strati e regole

### 5.1 Strati e finitura

- **Due strati, 1,6 mm, rame da 1 oz** su tutte e tre le schede: le correnti più alte sono 2,3–2,5 A sul ramo del regolatore 5 V (`produzione.md:175-177`, `:278`). Il quattro strati non serve [S].
- **Finitura**: HASL senza piombo sulla PCB-L; **ENIG** consigliato su PCB-S (LGA da 0,5) e PCB-C (TQFN da 0,5), perché è piana [S]; il sovrapprezzo per 5 pezzi va letto nel preventivo [C].
- **Montaggio a una faccia** (Economic, `produzione.md:83`): sulla PCB-L gli SMD sopra, sulla PCB-C sotto (la faccia che guarda l'ESP32), sulla PCB-S sopra.
- Regole di disegno di `produzione.md:181-193`: pista e spazio 0,20 / 0,20, via 0,3 / 0,6, rame a 0,5 dal bordo. Le piazzole a passo 0,5 di TQFN e LGA si fanno con le impronte di libreria, con piste da 0,2 [S].

### 5.2 Correnti e piste di potenza

| Rete | Corrente di progetto | Pista (1 oz, strato esterno) | Fonte |
|---|---|---|---|
| VBAT, da XH4 al VIN del D24V22F5 | 3 A (F2 da 2 A, regolatore fino a 2,3 A con il pacco a 6 V) | **1,5 mm** (1,37 per +10 °C) | `requisiti.md:43`; `produzione.md:171` |
| 5V_REG, dal VOUT al diodo e al PTC | 2,5 A (massimo del regolatore) | 1,5 mm o riempimento | `requisiti.md:44` |
| 5V_LED, dopo il PTC, fino a J-CAR e XH3 | 2,2 A (intervento del PTC), 0,86 A in uso | 1,0 mm (0,9 per 3 A a +20 °C) | S-06 |
| 5V_ESP, dopo SS34 | 0,5 A | 0,5 mm | `requisiti.md:45` |
| 3V3S | 0,2 A | 0,4 mm | `requisiti.md:47` |
| 5 V della PCB-C (LED e ampli) | 0,86 A | 1,0 mm | `requisiti.md:46` |
| Segnali | — | 0,25 mm | `produzione.md:186` |

Sul cavo piatto il 5 V passa già su due poli (1-2) e la massa su tre (`requisiti.md:92`): la PCB non cambia il cavo.

### 5.3 Separazione del VBAT e del 5 V

- **VBAT in un'isola**: la pista corta fra XH4 e il VIN del regolatore, su un solo strato, lungo il bordo e lontana dalle file dei pin dell'ESP32 (\|y\| 12,7), con almeno 0,5 mm di spazio e una pista di massa di guardia verso il resto [S; per tensioni sotto 15 V l'IPC-2221 chiede molto meno, il margine serve contro le gocce di stagno]. Nessun via VBAT sotto l'ESP32, nessun VBAT sul cavo del carapace. Serigrafia "VBAT 8,4 V".
- **5 V lontano dai GPIO** (R-09): sulla UICPAL il pin 5V è l'ultimo della fila sinistra, accanto al GPIO14 (RX della SSC-32) (`dati-moduli.md`, piedinatura Freenove: V sul Freenove, S sulla UICPAL). La pista del 5 V esce dal pin dal lato opposto al GPIO14; fra le piazzole una massa o almeno 0,5 mm.
- **Il 5 V del regolatore non torna verso la USB** senza la scelta esplicita di oggi: SS34 in serie (R-11, S-07).
- **Masse**: riempimento di massa sulla faccia senza componenti; punto a stella sotto il GND del regolatore; ritorno dei LED con una sua pista larga verso J-CAR e XH3, unita al piano solo al punto a stella (`requisiti.md:48`, `:233`).
- **Antenna**: niente rame sulle due facce della PCB-L per x ≥ 74 (C la quota), PCB-C ferma a x 70 (capitolo 1).

### 5.4 Segnali

- **I2C**: pull-up solo sulla PCB-L, dimensionati nel disegno per un equivalente di 1,0–1,4 kΩ con i moduli che restano (spariscono le resistenze della Adafruit ADS7830, della GY-6500 e della SparkFun TCA9534) (R-13, `requisiti.md:239`). Impronte di pull-up vuote sulle altre due schede.
- **I2S** sulla PCB-C: BCLK, WS e i due dati lontani dal bus, con una massa in mezzo come nel cavo (`requisiti.md:240`). Uscite dell'amplificatore corte e affiancate fino alla GH2, lontane dalla linea dei microfoni.
- **ADC** sulla PCB-S: riferimento REF e partitori dallo stesso 3V3S filtrato (per esempio 10 Ω e 1 µF), così la lettura resta in rapporto (R-05, `requisiti.md:134`); il funzionamento del pin REF dell'ADS7830 va riletto sul datasheet [C].
- **IMU** sulla PCB-S: vicino a una vite, lontana dalle prese (le spine tirano), assi stampati in serigrafia con X verso la testa; niente via sotto l'LGA [S].
- **Dato dei LED**: 330 Ω vicino al buffer, uscite separate per carapace e tibie, pull-down da 10 kΩ all'ingresso (R-09, `requisiti.md:228`, `:242`).

### 5.5 Punti di prova

Una piazzola nuda Ø1,5 o un foro da 1 mm per il puntale, con la sigla in serigrafia (R-16, `produzione.md:256`):
- PCB-L: VBAT, 5V_REG, 5V_ESP, 5V_LED, 3V3S, due GND, SDA, SCL, TX3, TX5, RX5, RX3, LED_IN, DATA, DATA2, SENSE, ENA, OFF; piazzola per il filo provvisorio verso GPIO38 (misura RMT, P2);
- PCB-S: 3V3S, GND, REF, A0…A7 (sulle piazzole dei condensatori), SDA, SCL;
- PCB-C: 5V, 3V3, GND, DATA, BCLK, WS, MIC, AMP, XSHUT.

La prima accensione senza ESP32 (`guida/passi/04-banco.yaml:705`) si fa sui punti di prova invece che nelle prese delle strip.

## 6. Cosa sparisce, cosa si compra

### 6.1 Spariscono

| Voce | Oggi | Costo evitato | Stato, fonte |
|---|---|---|---|
| C1 KAmod Level Shift x4 | da comprare | 2,51 € | V (`BOM.md:70`) |
| X6 Adafruit ADS7830 | approvata | 6,37 € se non è ancora comprata | V (`BOM.md:170`) |
| X5 e X14, resistenze e condensatori dei partitori a reoforo | approvate | circa 1,50 € | V (`BOM.md`, righe X5 e X14) |
| C2 millefori e strip | in casa | 0 € (restano per i provini) | V (`BOM.md:71`) |
| X20 SparkFun TCA9534 | in arrivo il 24 novembre | 0 €: diventa una scheda per il banco | V (`BOM.md:184`) |
| X17 modulo MAX98357A, X4 GY-6500 | in casa | 0 €: ripieghi e ricambi | V (D-074) |
| X9 buffer DIP e PTC radiale | approvati per il provino 7 | 0 €: servono comunque al provino | V (`BOM.md:173`) |
| `Corpo_Piastrina_IMU`, bugne dell'amplificatore come supporto del modulo | parti stampate | stampa | se l'IMU va sulla PCB-S |
| Fili saldati | circa 47 fili esterni, 37 fili isolati e una cinquantina di ponticelli sulla basetta; 26 fili della striscia; i fili della scheda del carapace | ore di lavoro e il rischio vero delle millefori | `requisiti.md:72`, `:118` |

### 6.2 Da comprare (proposte, niente è approvato)

| Voce | Quantità | Costo stimato | Stato |
|---|---|---|---|
| Ordine JLCPCB: 3 schede × 5, montaggio Economic | 1 ordine | capitolo 7 | S, C preventivo |
| Seconda testata 2 × 8 a 90° (Würth 61201621721 o uguale), per J-CAR sulla PCB-L | 1 + 1 | circa 2–3 € [S] | S |
| Prese XH a 90° (2, 3 e 4 poli) per la PCB-L, se il kit in casa non le ha | 5 + scorte | < 1 € [S] | C (guardare il kit C7) |
| Codini JST GH già crimpati (2, 3, 5, 8 poli) | circa 9 + scorte | circa 5–10 € [S] | S |
| Strip femmina 1 × 20 | 2 | in casa (C2) | V |
| D24V22F5 (B2) | 1 | 17,84 € (già nel BOM) | V |

I componenti montati da JLCPCB non si possono far spedire sciolti (restano nella libreria dell'utente da JLCPCB, [pagina JLCPCB della TCA9534](https://jlcpcb.com/partdetail/TCA9534PWR/C783615)) [V]: testate e prese a reoforo vanno nel carrello Kamami o DigiKey del resto del BOM, oppure le monta JLCPCB (capitolo 7).

## 7. Costo stimato per 5 schede

Voci del montaggio dal listino JLCPCB Economic del 9 settembre 2026 (`produzione.md:81-92`) [V]; quantità e prezzi dei componenti miei [S]. Cambio 1 $ ≈ 0,86 € (`produzione.md:7`) [S].

### 7.1 Voci

| Voce | PCB-L | PCB-S | PCB-C | Fonte |
|---|---|---|---|---|
| Schede nude, 5 pezzi, 2 strati, ≤ 100 × 100 | 2 $ | 2 $ | 2 $ | `produzione.md:29` |
| Messa in macchina, stencil, conferma della posizione | 10,16 $ | 10,16 $ | 10,16 $ | `produzione.md:85-91` |
| Codici Extended (3,07 $ l'uno) | 3: buffer, PTC, SH4 = 9,21 $ | 4: ADS7830, LSM6DSO, SH4, GH8 = 12,28 $ | 7: TCA9534, MAX98357A, SH4, GH2, GH3, GH5, CE1 = 21,49 $ | S: categorie da rileggere |
| Componenti per 5 schede (con le quantità minime) | circa 12 $ | circa 35 $ con l'IMU, 14 $ senza | circa 19 $ | S, prezzi del capitolo 3.1 |
| Giunti SMD (circa 225 a serie × 5 × 0,0016 $) | | 1,8 $ in tutto | | S |

### 7.2 Totali consegnati in Italia

| Strada | Calcolo | Totale | Stato |
|---|---|---|---|
| **Schede nude**, per confronto (montaggio a mano, altra architettura) | `produzione.md:270-271` | **8–24 €** | S |
| **3 ordini separati, 5 schede montate ciascuno, IMU su tutte** | 6 + 30,48 + 42,98 + 66 + 1,8 + spedizione 3–6 = 150–153 $, sotto i 170 $ dell'IOSS; IVA 22 % alla cassa → 183–187 $ ≈ 158–161 €; dazio 3 € per voce (1–3 voci) e 2 € dal 1° dicembre 2026 | **circa 165–175 €** | S; C voci doganali (`produzione.md:65`) |
| **Un pannello con le tre schede, 5 pannelli montati** | schede 2–10 $; montaggio una volta 10,16 $ + pannello 8,21 $; 12 codici Extended diversi = 36,84 $; componenti 66 $; giunti 1,8 $; spedizione 3–6 $ → 128–139 $; con l'IVA 156–170 $ ≈ 134–146 €; un dazio da 3 € e 2 € | **circa 140–150 €** | S; C sovrapprezzo dei disegni diversi e conteggio dei codici nel pannello |
| **Un pannello, 5 fabbricati, 2 montati** (uno in uso, uno di scorta) | come sopra con i componenti al 40 % (26,4 $): 87–98 $, con l'IVA 106–120 $ ≈ 91–103 €; un dazio e 2 € | **circa 100–110 €** | S |
| In più: strip, testate e prese XH montate da JLCPCB | 3,58 $ a ordine + circa 435 giunti × 0,0164 $ + parti circa 8 $ ≈ 18–22 $ | **+ 20–25 €**, e l'ordine supera i 170 $: IVA e dazio passano al corriere con la sua commissione (10–20 €, S) | S (`produzione.md:47`, `:51`) |
| In più: ENIG su PCB-S e PCB-C | — | da leggere nel preventivo | C |

Proposta: **un pannello, 2 serie montate su 5**, testate e prese saldate dall'utente. Il costo netto rispetto alle millefori (in casa, costo zero) è di circa **100–110 €** meno i 10 € circa di moduli non più da comprare (6.1), più 10–15 € di codini e testate (6.2). Una seconda serie, se la prima ha un errore, costa di nuovo circa la stessa cifra.

## 8. Cambi al CAD e alla guida

Niente di questo si fa ora: D-076 tiene la 2.1.7 e la guida sulle millefori (`requisiti.md:266`). È l'elenco di cosa toccherebbe la versione con le PCB.

### 8.1 CAD

| Parte | Cambio | Peso |
|---|---|---|
| `Basetta` | sostituita dallo STEP della PCB-L, stessa sagoma e stesse colonnine; origine ausiliaria di KiCad nel punto (22; 0) del CAD (`produzione.md:242`) | piccolo |
| Spine della PCB-L | corpi delle spine innestate sui bordi da provare contro colonnine del coperchio, morsettiera della SSC-32, pareti e prese; l'asola del bus della 2.1.7 deve far passare 4 cavi Qwiic e le due spine GH8 (oggi fili sciolti) | medio, C |
| Vano sotto il vassoio | via `Rif` dell'ADC, la striscia (mai posata, S-28) e, con l'IMU sulla PCB-S, `Corpo_Piastrina_IMU`; dentro lo STEP della PCB-S sulle 4 bugne. Le bugne restano; si controlla che abbiano davvero la stessa cima (z −5,4) | medio |
| Carapace | scheda allungata da circa 23 × 30 a 43,5 × 30; le bugne dell'amplificatore (67,35; ±6,5) diventano bugne della PCB-C; il fermo del modulo e la sua morsettiera spariscono. Si ricontrolla lo spazio del flat della camera sotto la scheda (9,7 a x 40,75…45,25) e l'aria sopra l'antenna (8,5) | medio |
| 2.1.7 | i due punti aperti restano: spina orizzontale 0,6 sotto la cima della USB-C, e verso in cui si allunga la scheda (`requisiti.md:198`); con la PCB-C allungata in avanti il secondo si chiude da sé | — |
| `rif_componenti.py`, `fori.json`, manifest | quote di PCB-L, PCB-S, PCB-C e delle spine; via le quote dei moduli integrati | piccolo |

Il CAD non cambia nelle parti strutturali: base, vassoio, coperchio e carapace restano, con fori e bugne già esistenti. È il motivo del punteggio 3 sull'impatto.

### 8.2 Guida, sezione 4 (banco dell'elettronica)

| Passi di oggi | Diventano |
|---|---|
| 4.06–4.07 basetta: taglio, fori, croci, prova a secco (`04-banco.yaml:209-251`) | ricevimento della PCB-L: controllo visivo (ponti, polarità di SS34, PTC e CE1), prova a secco dell'ESP32 nelle strip. La prova a secco vera si fa **prima di ordinare**, con la dima stampata (`produzione.md:250`) |
| 4.08–4.11 resistenze, D1, U3, traslatore, regolatore, PTC, strip, ponticelli e barra di massa (`:252-344`) | un passo: strip femmina e D24V22F5 saldati a mano |
| 4.12–4.19 fili 1–37, cavo piatto, rami del bus, seriale, luci, fili verso 2813 e regolatori, filo della batteria (`:345-548`) | spariscono: al loro posto i codini XH e GH saldati all'estremo lontano (2813, regolatori con R3, prese, NTC, moduli), un passo per gruppo |
| 4.20–4.21 prove 1–20 al multimetro (`:549-601`) | le stesse prove sui punti di prova, con la lista in serigrafia |
| 4.22–4.25 scheda del carapace: taglio e CE1, testata, ponticelli e fili 101–112, prove (`:602-682`) | ricevimento della PCB-C e prove sui punti di prova; resta da saldare solo J2 |
| 4.26–4.28 ramo logica sul tavolo, prima accensione senza ESP32, ESP32 negli strip (`:683-754`) | restano, con le spine al posto dei fili |

Da circa 20 passi di saldatura fine a circa 6 [S].

### 8.3 Guida, sezione 8 (elettronica nel corpo)

| Passi di oggi | Diventano |
|---|---|
| 8.06 piastrina dell'IMU, 8.08 IMU sulla piastrina, 8.09 ADC sulle bugne, 8.10 striscia dei partitori (`08-elettronica.yaml:219-345`) | un passo: PCB-S sulle 4 bugne, 4 viti M2 |
| 8.07 fili del bus nell'asola (`:242-266`) | 4 cavi Qwiic e 2 spine GH8 nell'asola |
| 8.12 basetta sulle colonnine (`:373-398`) | uguale, con la PCB-L |
| 8.17–8.24: uscita della 2813, abilitazione e spegnimento, seriale, bus agli INA260, cavo piatto e pulsante, prese dei piedi verso l'ADC, prese delle luci, NTC (`:525-772`) | i fili si saldano al banco all'estremo lontano come codini; nel corpo si innestano. Restano saldati solo i lati della 2813, dei regolatori e delle prese |
| 8.25–8.26 controllo dei fili e prove a freddo (`:773-818`) | controllo delle spine e prove sui punti di prova |

### 8.4 Guida, sezione 13 (carapace)

| Passi di oggi | Diventano |
|---|---|
| 13.09 altoparlante, 13.10 amplificatore (`13-carapace.yaml:284-333`) | l'altoparlante finisce in una spina GH2; il passo dell'amplificatore sparisce |
| 13.12 microfoni, 13.13 ToF posteriore (`:353-402`) | i fili finiscono in spine GH5 |
| 13.16 fili sulla scheda, 13.17 scheda sulle bugne (`:439-486`) | PCB-C sulle 4 bugne, poi le spine; niente saldature nel carapace |
| 13.18 prova al banco senza corrente, 13.19 spina IDC e cicalino, 13.20 prova con la logica accesa (`:487-592`) | restano, sui punti di prova |

## 9. Rischi

| Rischio | Quanto pesa qui | Come si riduce | Stato |
|---|---|---|---|
| **Impronta sbagliata** (interasse dell'ESP32 25,4 o 24,7, pin del D24V22F5, testata 2 × 8, spine) | una serie montata costa circa 100–150 € invece di 2–10 € | prova a secco (P-005) e dima stampata 1:1 prima dell'ordine; montare 2 serie su 5 | S (S-02, S-03, S-26; `produzione.md:250`) |
| **Circuito non ancora provato al banco** | lo schema è "proposta da approvare" (`requisiti.md:280`); restano aperti S-06, S-10, S-21, S-22, il 3,3 V (X3), il calore del regolatore (P4), i 230400 baud | fare la PCBA **dopo** il banco S1 (`docs/piano-elettronica-software.md`), con la millefori o con una prima PCB nuda; impronte vuote e ponticelli per le scelte aperte | S |
| **Riparabilità** | TSSOP, TQFN e LGA non si cambiano con il saldatore a punta: un chip guasto vuol dire cambiare la scheda | una scheda montata di scorta; ripieghi ai moduli in casa (GY-6500 nella fila di fori, piazzole per un amplificatore esterno) | S |
| **Componenti esauriti** | l'INA260 su LCSC ha 0 pezzi; LSM6DSO 1100 in una istantanea non datata | parti Basic o Preferred dove c'è scelta; controllo del magazzino il giorno dell'ordine; niente "Global Sourcing" (`produzione.md:97`) | V INA260 (escluso), S gli altri |
| **Spine sotto vibrazione** | un SH o un XH per attrito può sfilarsi camminando | GH con aggancio per tutto quello che si muove; XH e SH fermati dalla guida dei cavi; prova di 30 minuti di marcia | S |
| **Disegno più lungo** | tre schede, due chip con piazzola termica o LGA, un amplificatore in classe D vicino ai microfoni; è la prima PCB del progetto | ERC e DRC nella CI, STEP in Fusion (`produzione.md:228-244`); revisione dello schema prima del layout | S |
| **Dogana** | oltre i 170 $ l'IVA passa al corriere con la sua commissione | un pannello, 2 serie montate, THT a mano | V regola (`produzione.md:47`) |
| **Disturbi** | amplificatore in classe D a 8,5 mm sopra l'antenna e accanto ai microfoni; I2S a 3 MHz | come oggi con il modulo; layout del capitolo 5.4; prova di ricezione Wi-Fi a carapace chiuso (C8 è il ripiego, `BOM.md:77`) | S |

## 10. Tempi

| Fase | Durata | Stato |
|---|---|---|
| Dati che mancano (`requisiti.md:282-296`): prova a secco dell'ESP32, disegno della testata, pin del D24V22F5, tensione d'uscita della seriale della SSC-32, pin A e B della 2813 | quando arrivano i pezzi | C |
| Banco S1 con le millefori, per chiudere gli aperti dello schema | secondo `docs/piano-elettronica-software.md` | S |
| Schemi in KiCad delle tre schede, scelta dei codici LCSC | 2–3 sessioni di lavoro | S |
| Layout, DRC, STEP in Fusion e verifica degli ingombri, dima stampata | 3–4 sessioni | S |
| Fabbricazione e montaggio JLCPCB Economic | 1–2 giorni + 1–3 giorni (`produzione.md:71`, `:96`) | V |
| Spedizione con la linea economica | 7–15 giorni lavorativi (`produzione.md:59`) | S |
| **Dall'ordine a casa** | **circa 2–3 settimane** | S |
| Montaggio dell'utente: D24V22F5, strip, testate, prese XH, codini | circa 2–3 ore invece di 2–3 giorni di millefori [S] | S |
| Una seconda serie se la prima ha un errore | altre 3–4 settimane | S |

## 11. Cosa si guadagna e cosa si perde

**Si guadagna**:
- affidabilità: spariscono i giunti a filo volante e i ponticelli delle millefori, i fili restano solo agli estremi lontani, ogni spina ha la chiave;
- spazio: la PCB-C si prende il posto dell'amplificatore e chiude il dubbio sul verso della 2.1.7; la striscia senza posto (S-28, S-29) sparisce dentro la PCB-S; nel vano si libera la piastrina dell'IMU;
- montaggio e smontaggio: le tre schede si tolgono senza saldatore; la scheda della logica si cambia in pochi minuti;
- misure: punti di prova con la sigla invece di fori contati sulla millefori;
- il PTC giusto (S-06) e un TCA9534 che trova posto (S-17).

**Si perde**:
- **ricambi**: i moduli in casa (MAX98357A × 10, GY-6500, TCA9534 SparkFun) diventano ripieghi da banco; un chip guasto sulla PCB vuol dire una scheda nuova;
- **riparabilità**: solo i THT e gli SMD grandi si rifanno a mano;
- **flessibilità**: ogni cambio dello schema dopo l'ordine è una nuova serie; le scelte ancora aperte si coprono con impronte vuote e ponticelli, non tutte;
- **predisposizioni X**: quasi tutte restano, alcune a una condizione (tabella sotto).

| Predisposizione | Con questa architettura | Stato |
|---|---|---|
| X1 bus e presa di espansione | SH4 su PCB-C, PCB-S (passante) e 4 rami sulla PCB-L | resta |
| X3 regolatore 3,3 V | LDO non montato sulla PCB-L e ponticello a tre vie: per costruzione **mai J1 e X3 insieme** (D-076) | resta, senza comprare X3 |
| X4 IMU, X23 vibrazioni | LSM6DSO sulla PCB-S o GY-6500 nella fila di fori; la Pololu #2798 non ha più un posto suo | resta, con un cambio |
| X5, X14 FSR e NTC | sulla PCB-S | resta |
| X7 INA260, X8 ToF frontale, X19 ToF posteriore | moduli sulle spine | resta |
| X9, X11, X12, X21, X22, X30, X31 luci | catena dalla PCB-C, luci delle tibie dalla PCB-L | resta |
| X15 INA3221, X32 ADC in più, X33 seesaw, X18, X27, X29 | sul bus, dalle prese Qwiic | resta |
| X16 microfoni (MS3625 o Adafruit 3421) | GH5 sulla PCB-C | resta |
| X17 amplificatore | chip sulla PCB-C; il modulo solo dalle piazzole di ripiego | cambia |
| X20 espansore, X25 XSHUT dal polo 14, X26 uscita del radar | TCA9534 sulla PCB-C con i 7 I/O liberi su piazzole; polo 14 di J2 invariato | resta |
| X28 LIDAR su GPIO40 | serve un ponticello sulla PCB-C che stacca i microfoni | resta, con un ponticello |
| Piano B con la microSD e PAM8302A su GPIO2 | l'amplificatore I2S è saldato: si lascia vuoto | peggiora |
| Computer di bordo a zaino | il suo 5 V da 3 A non passa dalle schede (`piano-elettronica-software.md:202`); la USB OTG è sull'ESP32 | indifferente |

## 12. Punteggio

Da 1 a 5, dove 5 è il meglio per l'utente. Giudizio mio [S], per confrontare questa architettura con le altre dello studio.

| Criterio | Voto | Perché |
|---|---|---|
| Semplicità per l'utente | **4** | arrivano schede finite: si saldano solo regolatore, strip, testate, prese XH e codini; da circa 20 passi di millefori a circa 6. Non è 5 perché restano da saldare i codini agli estremi lontani e il disegno insieme è il più lungo |
| Affidabilità | **4** | niente fili volanti né ponticelli, spine con chiave e aggancio, punti di prova. Non è 5 perché lo schema non è ancora provato al banco e le prime serie di una PCB hanno spesso un errore |
| Costo | **2** | circa 100–110 € con un pannello e 2 serie montate, 140–175 € con 5 serie montate, contro 8–24 € delle schede nude e 0 € delle millefori; un errore raddoppia la spesa |
| Impatto sul CAD | **3** | base, vassoio, coperchio e carapace restano; si riusano colonnine e bugne. Cambiano il contenuto del vano, la scheda del carapace (più lunga, al posto dell'amplificatore) e gli ingombri delle spine sui bordi della PCB-L |
| Riparabilità | **2** | i chip a passo fine non si cambiano a mano; la riparazione è una scheda di scorta. Restano riparabili i THT, i codini e i moduli esterni |
| Compatibilità con le predisposizioni X | **4** | il bus Qwiic arriva a tutte le schede, X3 resta reversibile senza comprarlo, l'espansore porta i suoi I/O su piazzole. Perdono qualcosa la Pololu #2798, il modulo X17 e il piano B con la microSD |

Somma 19 su 30.

## 13. Proposta e aperti

Proposta [S]: l'architettura 3 è la più comoda da montare e la più affidabile a robot finito, ma è la più cara e la meno perdonante agli errori. Ha senso **dopo** il banco S1, quando lo schema è provato, come seconda serie: prima la millefori (o una PCB nuda saldata a mano), poi un pannello JLCPCB con 2 serie montate su 5.

Da chiedere all'utente:
1. Se accetta il montaggio del produttore (chip a passo fine) e la spesa di circa 100–110 € per la prima serie.
2. Se l'IMU può passare dalla GY-6500 sulla piastrina a un LSM6DSO sulla PCB-S (D-074, R-06).
3. Se l'amplificatore può passare dal modulo in casa al chip sulla PCB-C (X17).
4. Se le spine si saldano a mano (THT dall'utente) o le monta JLCPCB (circa 20–25 € in più e l'ordine oltre i 170 $).

Aperti tecnici:
- tensione d'uscita della seriale della SSC-32 (partitore della RX) e massa comune (S-22) [C];
- categoria JLCPCB del buffer, del PTC 1812, del CE1 SMD e delle prese GH [C];
- funzionamento del pin REF dell'ADS7830 per la lettura in rapporto [C];
- ingombri delle spine innestate sui bordi della PCB-L e passaggio dei cavi nell'asola della 2.1.7 [C, CAD];
- cima comune delle quattro bugne del vano a z −5,4 [S, CAD];
- zona senza rame sotto l'antenna (x ≥ 74) dal datasheet del modulo ESP32-S3-WROOM [C];
- prezzi e dogana dal preventivo vero (`produzione.md:284-291`) [C].
