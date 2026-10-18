# Architettura 1: una PCB per ogni millefori

Studio preliminare del 16 ottobre 2026. Ogni millefori di oggi diventa un circuito stampato con la stessa sagoma, gli stessi fori e gli stessi collegamenti verso il resto del robot. Il CAD e la guida cambiano il meno possibile. È una proposta: niente è approvato né comprato, e il disegno vero della PCB si fa con l'utente in una versione successiva (D-076, `docs/decisioni.md:681-686`).

- Requisiti di partenza: `docs/ricerca/pcb/requisiti.md` (sigla R-01…R-20, righe 302-321). Produzione e costi: `docs/ricerca/pcb/produzione.md`.
- Quote in mm nella terna del robot: X avanti, Y a sinistra, Z in alto.
- Stato di ogni dato: **V** verificato (fonte primaria o modello CAD), **S** stimato (calcolo, catalogo non riletto, proposta mia), **C** da confermare (sul pezzo, sul disegno del produttore o con l'utente).
- Il CAD di oggi è la 2.1.6. Le modifiche della 2.1.7 che toccano le schede sono in bozza (`docs/piano-v2.1.0.md:351-367`, `:473-489`) e sono indicate a parte.

## 0. L'idea in breve

| Cosa resta | Cosa cambia |
|---|---|
| Tre schede, negli stessi posti: basetta sotto l'ESP32, scheda del carapace sotto il dorso, partitori accanto all'ADC | il supporto: rame e solder mask al posto di piazzole sciolte, ponticelli e fili |
| Stessi moduli: ESP32 su strip femmina, D24V22F5, buffer SN74AHCT125N in DIP-14, traslatore KAmod, PTC, D1, resistenze a reoforo | **spariscono i fili e i ponticelli interni**: 37 fili isolati, 44 incroci e circa 50 ponticelli sulla basetta (`guida/schemi/schemi.md:102`, `:106-107`); 12 fili e 4 ponticelli sulla scheda del carapace (`:282-299`); 22 ponticelli sui partitori (`:460-467`) |
| Stessi collegamenti verso il resto: circa 47 fili saldati dalla basetta, Dupont della seriale, cavo piatto saldato sulla basetta, spina IDC sul carapace, fili dei moduli saldati sulla scheda del carapace, 26 fili sui partitori | piazzole con il nome stampato in serigrafia, al posto delle coordinate colonna-riga |
| Stesse reti e stessa piedinatura del cavo a 16 poli (`docs/cablaggio.md:132-143`) | punti di prova, ponticelli a saldare per le scelte aperte (J1, X3, misura RMT) |

Che cosa **non** risolve: i fili verso il resto del robot restano saldati, quindi la basetta non si toglie senza dissaldare (oggi è così, `guida/schemi/schemi.md:166-167`). Le architetture con i connettori o con una scheda unica sono studiate a parte.

## 1. Le schede

Tre disegni, ciascuno ordinato in 5 pezzi (minimo di JLCPCB, `produzione.md:29`). Spessore 1,6 come la millefori, così le quote verticali del CAD non cambiano (`requisiti.md:260`; `cad/script/rif_componenti.py:111`, `bas_sp` 1,6 S).

### 1.1 PCB-B, la basetta dell'ESP32

| Dato | Valore | Stato, fonte |
|---|---|---|
| Sagoma | rettangolo 56 × 35, angoli arrotondati R 1 (S) | V; `rif_componenti.py:109-110` (`bas_l`, `bas_w`); D-053 |
| Posizione | x 22…78, \|y\| ≤ 17,5, z 5,9…7,5; lato componenti in alto, verso l'ESP32 | V; `guida/schemi/schemi.md:25`; `requisiti.md:158` |
| Fori | 4 × Ø 2,2 non metallizzati, a (29; ±6,8) e (75,5; ±6,5), con un anello senza rame di 1 mm attorno alla testa M2 Ø 4 su tutte e due le facce | V posizioni (`cad/script/corpo.py:449-459`, `:512-515`; `guida/dati/fori.json` `bas_col_*_ins`); S anello (`produzione.md:190`) |
| Sotto la scheda | 3,3 mm fino al vassoio; nella 2.1.7 le teste M2 svasate a filo li lasciano liberi, salvo le quattro colonnine Ø 5,8 | V 2.1.6; bozza 2.1.7 (`docs/piano-v2.1.0.md:351-367`) |
| Sopra la scheda | 8,5 mm fino al PCB dell'ESP32 (strip femmina); 6,6 sotto la sede della microSD (x 22,5…37,5, \|y\| ≤ 7) | S; D-053; `requisiti.md:161-162` |
| Strip dell'ESP32 | due file da 20 a passo 2,54, a y ±12,7 (25,4 di interasse), da x 22,5 a 73,3; polo 1 (3V3 e GPIO43) verso la testa | S fino alla prova a secco (P-005, D-076); `schemi.md:44` |
| Antenna | modulo dell'ESP32 da x 55,6 a 81,1; la parte con l'antenna stampata è l'ultimo tratto del modulo, oltre la fine delle strip (x 73,3) | S; `requisiti.md:168`, `:245` |
| Zona senza rame | da x 74 al bordo di testa (x 78), su tutte e due le facce: niente piste, niente riempimento, niente piazzole | S, regola generale dei moduli con antenna stampata, non riletta su Espressif (R-15) |

Disposizione proposta (S, da fare nel disegno), che ricalca quella della millefori per non cambiare i passi della guida:

| Fascia | y | Cosa c'è |
|---|---|---|
| bordo sinistro (+Y), fuori dall'ombra dell'ESP32 | 13,9…17,5 | piazzole del bus a 4 rami come la riga 1 di oggi (`schemi.md:220`), più un **quinto gruppo di riserva** (4 piazzole) per X15 o altro; piazzola d'ingresso del VBAT nel posto di O-1/P-1, oggi libero |
| strip sinistra | +12,7 | 20 fori della strip; il foro di P-2 (GPIO6, non usato) **non metallizzato**: ci passa accanto la pista del VBAT, come oggi passa il filo (`schemi.md:151`) |
| interno, sotto l'ESP32 | \|y\| ≤ 11,4 | U2 a destra verso la testa (come oggi, colonne M–S, x 54…70), U3, U4, D1, PTC1, resistenze; sotto la microSD solo parti basse (resistenze sdraiate, SMD) |
| strip destra | −12,7 | 20 fori della strip |
| bordo destro (−Y) | −13,9…−17,5 | piazzole del cavo piatto, dei fili verso 2813 e regolatori e del ramo delle tibie, come la riga 13 di oggi (`schemi.md:213-216`, `:221-223`) |
| bordo di coda (x 22) | — | i tre fili Dupont della seriale escono come oggi (`schemi.md:217-219`); la morsettiera VS/VL della SSC-32 è a 3,1 mm (`requisiti.md:165`) |

### 1.2 PCB-C, la scheda del carapace

| Dato | Valore | Stato, fonte |
|---|---|---|
| Sagoma oggi (2.1.6) | 20 × 30, x 29,5…49,5, \|y\| ≤ 15, faccia alta a z 30,9, lato componenti in basso | V; `schemi.md:249`; `corpo.py:225`, `:1082-1086` |
| Sagoma con la 2.1.7 | circa 23 × 30: testata 2 × 8 a 90° sul bordo di coda (x 29,5), spina orizzontale verso −X; viti di coda spostate davanti alla testata (x ≥ 41,5) | S, bozza; `piano-v2.1.0.md:473-489`; D-076 |
| Fori | 4 fori sulle bugne Ø 5,5 del dorso (inserti M2 messi da sotto), **nelle quote del CAD**: sulla PCB non c'è la griglia da 2,54, quindi niente fori allargati a Ø 2,6 per recuperare gli 0,23 mm di oggi (`schemi.md:251`) | V oggi (`fori.json` `ins_sch_a…d`); C posizioni della 2.1.7 |
| Sopra | 3,5 mm d'aria fra la scheda e il dorso (z 34,4) | V; `corpo.py:110`, `:121` |
| Sotto | 11,7 mm fino al PCB dell'ESP32; 9,7 fino al connettore del flat della camera (x 40,75…45,25, \|y\| ≤ 7,25) | S; `requisiti.md:193` |
| Davanti | amplificatore da x 51,85: se la 2.1.7 allunga la scheda in avanti (fino a 52,5) la PCB può avere un **dente** che lo scansa, cosa che la millefori non permette | S; `requisiti.md:198` |

La PCB-C non decide niente della 2.1.7: prende sagoma e fori dal CAD, come chiede `piano-v2.1.0.md:475` ("J2 al bordo e le quote della scheda restano le stesse che servirebbero a un PCB").

### 1.3 PCB-P, i partitori

| Dato | Valore | Stato, fonte |
|---|---|---|
| Sagoma di partenza | 22,86 × 10,16 (9 × 4 fori), due M2 in colonna I | V; `schemi.md:437`, `:535` |
| Posto | **non dimostrato** nel CAD (S-28, S-29): la tasca libera accanto all'IMU è x 60,5…71,3 (10,8) × y −20,9…0,75 (21,65), sul tetto del tunnel (z −9,4) | S; `schemi.md:553-566`; `requisiti.md:182` |
| Problema di oggi | la striscia è 1,2 mm più lunga della tasca, e le resistenze in piedi lasciano 0,3–0,8 mm sotto il vassoio | S; `schemi.md:566` |

Con la PCB le due difficoltà si allentano (S, da verificare nel disegno e poi nel CAD):
- **altezza**: resistenze sdraiate a reoforo (o SMD 0805 dal kit B8) al posto di quelle in piedi: la scheda sale di circa 1 mm sopra la sua faccia invece di 6,5–7;
- **lunghezza**: le piazzole dei fili non devono stare sulla griglia da 2,54. Con le piazzole a passo 2,0 (foro 0,8, piazzola 1,5 per il 30 AWG [S]) gli otto canali stanno in 16 mm, e i due fori M2 ai capi portano la scheda a circa **20 × 10**, dentro la tasca con circa 0,8 mm per lato.

È l'unica delle tre schede che cambia sagoma. Lo dichiaro come eccezione: la sagoma di oggi non ha un posto, e la PCB è l'occasione per darglielo.

## 2. Schema a blocchi

```
                     BATTERIA 2S -> T-plug -> F1 -> Wago -> F2 (2 A) -> Pololu 2813 (R6 100k, 100k su OFF)
                                                                          |  VBAT, GND, SENSE, OFF  (4 fili saldati)
 D42V110F6 x2 <- ENA (D2 in linea, R3 sul regolatore) ---------+         |
 SSC-32 <- TX5/RX5/GND (3 Dupont) ---------------+              |         |
 INA260 S, INA260 D, IMU+ADC, ToF frontale <- bus I2C (4 rami + 1 di riserva, fili saldati)
 prese delle luci delle tibie <- 5V_LED, GND, DATA2 (R9 in linea)    |         |
                                                  |              |         |
 +------------------------------- PCB-B (basetta, 56 x 35) ------------------------------------+
 |  VBAT -> U2 D24V22F5 -> 5V_REG -+-> D1 -> 5V_ESP -> strip -> ESP32-S3-CAM (U1)            |
 |                                 +-> PTC1 -> 5V_LED -> poli 1-2, tibie                       |
 |                                 +-> U3 VCC, U4 HV                                            |
 |  ESP32 3V3 -> JP1 (oggi J1) -> 3V3S -> pull-up R4 R5, U4 LV, polo 7, bus  [JP2: X3 esterno]  |
 |  GPIO48 -> R1 pull-down -> U3 1A/2A -> 1Y -> R2 330 -> polo 4 ; 2Y -> DATA2                 |
 |  GPIO21/14 <-> U4 KAmod <-> TX5/RX5          [JP3: canale 4 -> GPIO38, misura RMT al banco] |
 |  GPIO1 <- SENSE (R7 47k, CS1)   GPIO42 -> EN    GPIO41 -> OFF   GPIO38-40, GPIO2 -> I2S     |
 |  punti di prova; massa: riempimento sul retro, ritorni dei LED con piste loro fino a U2      |
 +---------------------------------------------+-----------------------------------------------+
                                               | cavo piatto 16 vie, saldato sulla basetta
                                               | (poli 15-16 separati verso i pin A e B della 2813)
                                               v
 +---------------- PCB-C (carapace, circa 23 x 30) ----------------+
 |  J2 testata 2 x 8 a 90 gradi con chiave  <- spina IDC            |
 |  5V -> CE1 470 uF -> catena LED (anello, lobi)  ; 5V -> ampli    |
 |  3V3 -> microfoni, ToF posteriore, presa Qwiic -> TCA9534 (X20)  |
 |  I2S -> microfoni (R8 al microfono) e ampli ; DATA -> anello     |
 |  poli 15-16 -> pulsante ; polo 14 -> piazzola di riserva (X25)   |
 +------------------------------------------------------------------+

 +---- PCB-P (partitori, circa 20 x 10) ----+
 |  3V3 (VIN dell'ADC) -> 8 x 10k 1 %       |  <- 6 FSR (segnale + massa), 2 NTC (segnale + massa)
 |  8 x 100 nF verso massa                  |  -> 8 fili verso A0...A7 dell'ADS7830 (40-60 mm)
 +------------------------------------------+
```

Fonti delle reti: `guida/schemi/schemi.md` 1.2 (righe 62-91), 2.2 (`:263-280`), 6.2 (`:448-458`); catena delle protezioni `requisiti.md:223`.

## 3. Componenti

### 3.1 Da montare (le parti di oggi, sulla PCB)

Le sigle sono quelle di `guida/schemi/schemi.md` (1.1, 2.1, 6.1), così passi, prove e disegni restano riconoscibili.

| Scheda | Sigla | Cosa | Voce, stato | Sulla PCB | Note |
|---|---|---|---|---|---|
| B | U1 | ESP32-S3-CAM UICPAL N16R8 su 2 strip femmina 1 × 20 | A2, C2: in casa | THT, 40 fori | sulla PCB si saldano **tutti** i 40 pin (tengono meglio la strip): i fori dei pin non usati non hanno rete. Eccezione: P-2 non metallizzato (1.1). R-01 |
| B | U2 | Pololu D24V22F5, 5 V 2,5 A | B2: da comprare (BOM approvato) | THT, 5 pin in fila | ordine dei pin da leggere sulla pagina Pololu 2858 prima del disegno (S-03, C). Senza Kapton: sotto il modulo solo solder mask, niente via né piazzole scoperte [S] |
| B | U3 | SN74AHCT125N, DIP-14 | X9: approvato per il provino 7 | THT | due canali per i LED come oggi; canali 3 e 4 a massa (o il 3 per la seriale, variante 3.3) |
| B | U4 | KAmod Level Shift x4 | C1: da comprare, 2,51 € (`docs/BOM.md:70`) | THT, due file da 6 a 7,62 | sigle e passo da confermare sul pezzo (S-04, C); niente sotto il modulo |
| B | PTC1 | fusibile ripristinabile sul 5 V dei LED | X9: MF-R075 approvato | THT radiale, **sdraiato sulla PCB, non più sopra U3**; riempimento di rame tolto sotto | S-06: il ramo arriva a circa 0,86 A contro 0,75 di tenuta. Proposta in 3.3 |
| B | D1 | Schottky 1N5819 | C3 | THT assiale | come oggi (S-07) |
| B | R1, R2, R4, R5, R7 | 10 kΩ, 330 Ω, 4,7 kΩ × 2, 47 kΩ 1 % | X9, B10: in casa (B10) o approvati | THT assiali sdraiati | valori come oggi; R4 e R5 da rivedere con S-13 |
| B | CS1, CS2 | 100 nF | B8: kit SMD in casa | SMD 0805 sul lato componenti | taglia del kit da confermare (S-30) |
| B | JP1 | ponticello a saldare 3V3 dell'ESP32 → 3V3S (oggi J1, filo 19) | — | due piazzole, chiuso con una goccia di stagno | si apre solo se arriva X3; mai JP1 e JP2 chiusi insieme (D-076) |
| B | JP2 | ponticello a saldare uscita di X3 → 3V3S | — | due piazzole, **aperto** | con tre piazzole VIN, GND, VOUT per i fili di un D24V5F3 nel vano sotto il vassoio: X3 resta reversibile senza comprarlo (R-17; S-12) |
| B | JP3 | ponticello a saldare L4 (canale 4 del KAmod) → GPIO38 | — | aperto | sostituisce il filo provvisorio I-7 → L-12 della misura RMT al banco (`schemi.md:227`); si riapre prima di collegare il carapace |
| C | J2 | testata 2 × 8 a 90° con chiave | X2: approvata, non comprata | THT sul bordo di coda | Würth 61201621721 da confermare sul disegno (S-26, C); chiave dal lato dei poli dispari |
| C | CE1 | 470 µF 10 V, Ø 6,3 × al più 8 | X2 | THT radiale sdraiato | D-076 |
| C | — | presa Qwiic | X1: cavo Adafruit 4210 tagliato | 4 piazzole come oggi | variante con presa JST SH in 3.3 |
| C | — | espansore TCA9534 SparkFun DEV-17047 | X20: in arrivo il 24 novembre | non sulla PCB: si innesta sulla presa Qwiic | il suo posto resta aperto (S-17) |
| P | R1–R8 | 10 kΩ 1 % | X5, X14 | **SMD 0805** (proposta) | le assiali in piedi non stanno nella tasca (1.3); le assiali sdraiate a passo 2,54 si toccano [S]. Cambio di codice da approvare (3.2) |
| P | C1–C8 | 100 nF | B8: kit SMD in casa | SMD 0805 | i 6 a reoforo di X5 non servono più (S-30) |

Restano **fuori dalle schede**, come oggi e per la stessa ragione (un filo staccato lascia tutto spento o al sicuro, R-12): R6 da 100 kΩ sulla 2813, la 100 kΩ fra OFF e massa sulla 2813, D2 in linea sul filo dell'abilitazione, R3 su ciascun D42V110F6, R9 in linea sul dato delle tibie, R8 al microfono (`schemi.md:60`, `:236-237`; S-11, S-20).

### 3.2 Che cosa sparisce e che cosa si compra

| Sparisce | Dove oggi | Stato, fonte |
|---|---|---|
| taglio e foratura delle tre millefori, croci a pennarello, fori allargati a Ø 2,6 | passi 4.06, 4.22; `schemi.md:251` | V |
| 37 fili isolati, 44 incroci e circa 50 ponticelli della basetta | `schemi.md:102`, `:106-107` | V |
| 12 fili (101–112) e 4 ponticelli della scheda del carapace; fili di DIN e pulsante saldati sui pin della testata | `schemi.md:282-299`, `:301` | V |
| 22 ponticelli e i due fili nudi della striscia dei partitori | `schemi.md:460-467` | V |
| nastro Kapton sotto U2 e sopra U3 (non nel BOM, S-24) | passo 4.07 | S: con la solder mask sotto U2 non serve [S]; il PTC non è più sopra U3 |
| 6 condensatori a reoforo di X5; 8 resistenze assiali di X5 e X14 (se passano a 0805) | `docs/BOM.md:169`, `:178` | S |
| le tre millefori C2 (in casa: nessun risparmio di soldi) | `docs/BOM.md:71` | V |

| Si compra (proposta, da approvare) | Quanto | Costo | Stato, fonte |
|---|---|---|---|
| tre PCB, 5 pezzi per disegno | — | capitolo 6 | S |
| 10 resistenze 10 kΩ 1 % 0805 (al posto delle 8 assiali di X5 e X14) | 10 | pochi centesimi l'una; meno di 1 € in tutto | S |
| eventuale PTC più grande (3.3) | 1–2 | meno di 1 € | S, C prezzo |

### 3.3 Ritocchi possibili dentro la stessa architettura

Ognuno è una scelta separata da approvare. Nessuno cambia il CAD.

| Ritocco | Cosa cambia | Pro | Contro | Stato |
|---|---|---|---|---|
| **a. PTC con tenuta più alta** | MF-R075 → Bourns MF-R090 (tenuta 0,90 A, intervento 1,80 A) | chiude S-06 con R-10: tenuta sopra 0,86 A, intervento sotto i 2,5 A del regolatore | sotto l'ESP32 fa caldo e la tenuta cala con la temperatura: a 40 °C 0,90 A può non bastare. In alternativa si lascia l'MF-R075 e si abbassa il tetto del firmware sotto i 600 mA (R-10) | S, catalogo Bourns MF-R non riletto per questo studio; C prezzo |
| **b. Seriale senza KAmod** | TX: canale 3 del buffer U3 (GPIO21 → 3A, 3Y → RX della SSC-32), con 10 kΩ di pull-up all'ingresso per tenere la linea alta durante il reset; RX: partitore 10 kΩ / 15 kΩ (5 V → 3,0 V) verso GPIO14 | un modulo e una voce in meno (C1, 2,51 €), 12 giunti delle sue strip in meno. Con l'uscita AHCT a 5 V la soglia d'ingresso della SSC-32 non conta più | tre resistenze in più (dal set B10, in casa), più due da montare solo per la misura RMT (JP3 dal canale 4 non c'è più). Stato di GPIO21 durante il reset da leggere (C). La guida perde il passo del traslatore ma cambia le prove della seriale | S; buffer `schemi.md:46`; `requisiti.md:131` |
| **c. Presa JST SH sulla PCB-C** | al posto del cavo Qwiic tagliato, una presa SM04B-SRSS-TB a 1 mm | la presa vera, raggiungibile dall'ottagono; il cavo intero resta per il TCA9534 | una voce nuova (meno di 1 € [S]); passo da 1 mm, si salda a mano con il flussante | S; `schemi.md:326`; `produzione.md:136` |
| **d. Polo 14 portato a una piazzola** su B e su C | oggi il conduttore 14 si taglia (`schemi.md:58`) | XSHUT del ToF del mento (X25) senza rifare il cavo | nessuno | S |

Nel punteggio del capitolo 10 conto **a**, **c** e **d**; **b** è da decidere con l'utente perché aggiunge parti mentre toglie un modulo.

## 4. Connettori e cavi

Gli stessi di oggi: nessun connettore nuovo, salvo il ritocco **c**. Cambia solo il modo in cui il filo arriva alla scheda: una piazzola metallizzata con il nome in serigrafia, un filo per piazzola (sulla scheda del carapace oggi sono due per foro, `schemi.md:355`).

| Da | Verso | Fili | Connettore | Sulla PCB | Stato, fonte |
|---|---|---|---|---|---|
| B | uscita della 2813: VBAT, massa, partitore (R6 alla 2813), OFF | 4 | saldati ai due capi, 26 AWG (VBAT siliconico se c'è, S-27) | VBAT al bordo +Y (posto di O-1/P-1); massa, SENSE e OFF al bordo −Y come oggi (S-13, R-13, Q-13). VBAT si posa per ultimo | V; `schemi.md:212-215` |
| B | ENA dei due D42V110F6 (D2 in linea, R3 sui regolatori) | 1, poi 3 | saldato, 26 AWG | una piazzola al bordo −Y, lontana da OFF e dal polo 13 (oggi P-13 confina con O-13 e Q-13, S-25) | V; `schemi.md:216` |
| B | SSC-32: TX, RX, massa | 3 | Dupont femmina (C4) | tre piazzole verso il bordo di coda, fili sul lato componenti | V; `schemi.md:217-219`; S-22 per la massa |
| B | bus I2C: INA260 S, INA260 D, IMU e ADC, ToF frontale | 4 × 4 | cavi Qwiic tagliati o 30 AWG, saldati | 4 gruppi da 4 piazzole al bordo +Y (massa, SCL, 3,3 V, SDA) **più un gruppo di riserva**; il ramo 3 con due piazzole per rete invece di due fili per foro | V; `schemi.md:220` |
| B | scheda del carapace | 14 dei 16 conduttori | cavo piatto saldato sulla basetta | 14 piazzole al bordo −Y nell'ordine dei poli. Proposta: due file sfalsate a passo 2,54 (1,27 fra una fila e l'altra), così i conduttori si separano solo di pochi millimetri invece di 25 [S] | V oggi; `schemi.md:221` |
| B | pulsante (pin A e B della 2813) | 2 (poli 15-16) | separati dal cavo piatto e giuntati a 26 AWG | non arrivano alla basetta, come oggi | V; `schemi.md:222` |
| B | prese delle luci delle tibie | 3 | saldati, R9 in linea sul dato | tre piazzole dedicate (oggi i fili condividono i fori dei poli 2 e 9) | V; `schemi.md:223` |
| C | basetta | 16 | spina IDC Würth 61201623021 con chiave | J2 a 90° sul bordo di coda (D-076) | V; `docs/BOM.md:175` |
| C | catena LED, microfoni, ampli, ToF posteriore, pulsante, Qwiic | 3 + 5 + 5 + 4 + 2 + 4 | saldati, 30 AWG (pulsante 26 AWG) | una piazzola per filo, raggruppate per modulo e con il nome; DIN e pulsante su piazzole loro, non più sui pin della testata | V; `schemi.md:305-321` |
| P | 6 prese dei piedi, 2 NTC | 16 | saldati, 30 AWG (NTC 28 AWG) | segnale e massa per ogni canale, nel loro ordine (AS, MS, PS, AD, MD, PD, NTC sinistra, NTC destra) | V; `schemi.md:513-516` |
| P | ADS7830: A0…A7, VIN, GND | 10 | saldati, 30 AWG, 40-60 mm | otto piazzole d'uscita in fila, VIN e GND ai capi | V; `schemi.md:517-519`; posizione dei pin dell'ADC da leggere (S-31) |

Per i fasci che escono dalla basetta (cavo piatto, bus) due fori Ø 1,5 accanto alle piazzole per una fascetta (D11) che tolga la trazione dal giunto [S]: sulla millefori non c'era il posto.

## 5. Strati e regole

Riprendo le regole di `produzione.md` (capitolo 3) e le applico alle tre schede. Tutto S fino al disegno.

| Voce | Scelta | Perché | Fonte |
|---|---|---|---|
| Strati | **2**, 1,6 mm, rame da 1 oz (35 µm), HASL senza piombo | le correnti dei servo non passano sulle schede; il ramo più carico è il 5 V del regolatore, 2,5 A | `produzione.md:19`, `:278` |
| Faccia superiore | componenti, piste di segnale e di potenza | i componenti THT si saldano dal retro | — |
| Faccia inferiore | riempimento di massa intero, salvo la zona dell'antenna e gli anelli delle viti | piano di ritorno per I2C, I2S e dato dei LED; dissipa il calore di U2 | `produzione.md:175` |
| VBAT | piazzola d'ingresso al bordo +Y, pista **1,5 mm** sul retro fino al VIN di U2 (circa 2,3 A con il pacco a 6 V), nel varco del foro non metallizzato di P-2; 1 mm di distanza da ogni altro rame, riempimento di massa compreso | R-08; con 1 oz e +10 °C 1,37 mm portano 3 A | `requisiti.md:224`; `produzione.md:171` |
| 5V_REG | pista da 1,5 mm o area di rame da VOUT di U2 a D1, PTC1, U3, U4 | fino a 2,5 A | `produzione.md:175` |
| 5V_LED | 1,0 mm da PTC1 alle piazzole dei poli 1-2 e delle tibie | 0,86 A di esercizio, fino all'intervento del PTC (1,5-1,8 A) per pochi secondi | S-06 |
| 3V3S | 0,5 mm | 0,2 A al più | `requisiti.md:47` |
| Segnali | 0,25 mm; spazio minimo 0,20 | | `produzione.md:185-186` |
| Masse | un solo piano; i ritorni dei LED (poli 3, 5, 9, massa delle tibie) arrivano con piste da 1 mm fino alla massa di U2, dove entrano nel piano: è la stella di oggi (Q-4) fatta in rame | `schemi.md:238` (scelta 8) | S |
| 5 V vicino all'ESP32 | nessuna piazzola o pista a 5 V adiacente a un foro della strip: in mezzo una pista di massa o almeno un passo (2,54) | R-09; oggi sono coppie che la disposizione non può evitare e che le prove controllano (`schemi.md:99`, S-09) | S |
| Antenna | niente rame da x 74 al bordo di testa | R-15 | S |
| Fori delle viti | non metallizzati, Ø 2,2 sulla basetta, quote del CAD sulle altre; 1 mm senza rame attorno alla testa | la vite non tocca le piste | `produzione.md:190` |
| Via | 0,3 / 0,6 mm | sopra i minimi di tutti i produttori | `produzione.md:188` |
| Rame dal bordo | 0,5 mm | | `produzione.md:191` |
| Serigrafia | sigle di `schemi.md`, nome di ogni piazzola esterna, polo 1, chiave, polarità di D1, CE1, PTC1; nome, revisione e data ("HEX2 BASETTA r1") | la guida chiama i punti per nome; revisioni riconoscibili | `produzione.md:260` |
| Punti di prova | piazzole nude da 1,5 mm: B: VBAT, 5V_REG, 5V_ESP, 5V_LED, 3V3S, due masse, SDA, SCL, TX5, RX5, LED_IN, DATA, DATA2, SENSE, EN, OFF. C: 5V, 3V3, GND, DATA. P: le piazzole dei fili bastano | R-16; le prove della guida si rifanno sui punti di prova | `produzione.md:256` |

La massa a stella di oggi esisteva perché i ritorni passavano su fili sottili e sui pin di massa della logica. Su un piano di rame la caduta è di pochi millivolt [S]: tengo le piste dedicate per i ritorni dei LED solo per non far passare 0,86 A sotto i pin dell'ESP32.

## 6. Costo stimato per 5 schede

Cinque pezzi per ciascuno dei tre disegni (minimo di JLCPCB); se ne monta uno, gli altri sono ricambi o seconda prova. Aree: B 56 × 35 = 19,6 cm²; C circa 23 × 30 = 6,9 cm² (C, misura della 2.1.7); P circa 20 × 10 = 2 cm² (S). `produzione.md` ha fatto i conti con C a 8 cm² e P a 2,3 cm²: la differenza sposta i totali di Aisler di meno di 1 €, quelli di JLCPCB per nulla (prezzo a gradino fino a 100 × 100, `produzione.md:36`).

| Strada | Totale consegnato in Italia | Fonte | Stato |
|---|---|---|---|
| **Nude, JLCPCB, un pannello con le tre schede**, linea economica, una voce doganale | **circa 8–18 €** | `produzione.md:271` | S; C sovrapprezzo per i disegni diversi |
| Nude, JLCPCB, tre ordini separati | circa 20–24 € (9 € sono il dazio di 3 € per voce) | `produzione.md:270` | S; C numero di voci |
| Nude, Aisler (UE, niente dogana), un pannello, 6 pezzi | circa 30 € | `produzione.md:273` | S, listino del 2023 |
| Nude, Aisler, tre progetti, 6 pezzi l'uno | circa 59 € | `produzione.md:272` | S |
| **Montate solo negli SMD da JLCPCB Economic** (CS1, CS2 sulla B; 16 parti 0805 sulla P), un pannello | pannello nudo + circa 18–20 $ (messa in macchina 8,18, stencil 1,53, conferma 0,45, pannello di più disegni 8,21, componenti Basic circa 1 $) = **circa 25–35 €** | voci in `produzione.md:85-92`; somma mia | S; C che 10 kΩ 1 % e 100 nF in 0805 siano Basic |
| Montaggio THT del produttore (strip, testata, moduli) | non conviene: 3,58 $ a ordine più 0,0164 $ a giunto, e il tempo risparmiato è poco | `produzione.md:126`, `:144` | S |

Componenti in più (capitolo 3.2): meno di 2 € (S). Con il ritocco **b** si risparmiano 2,51 € del KAmod (C1). Oggi le millefori sono in casa e costano 0 €: l'architettura costa **circa 10–20 €** in più nella strada consigliata (pannello JLCPCB, montaggio a mano), o circa 30 € con Aisler.

Il montaggio del produttore qui serve poco: le parti SMD sono 18, tutte 0805, e l'utente salda già gli 0805 sulla millefori (`schemi.md:55-56`). Lo terrei solo se l'utente preferisce non saldare la PCB-P.

## 7. Cambi al CAD e alla guida

### 7.1 CAD

Quasi niente: è il punto forte di questa architettura.

| Parte | Cambio | Stato, fonte |
|---|---|---|
| `Rif_Basetta_50x70` (`rif_componenti.py:503`), parametri `bas_l`, `bas_w`, `bas_sp` (`:109-111`) | nessuno. In più, quando la PCB è disegnata, il suo STEP (`kicad-cli pcb export step`) entra in libreria come i `Rif_*` (D-046) per la verifica d'interferenza; la scatola resta come riferimento | V; `produzione.md:240-244` |
| Vassoio, colonnine della basetta, `cor_bas_luce` 3,3 | nessuno: stessi fori, stesso spessore | V; `corpo.py:86`, `:512-515` |
| `Rif_Scheda_Carapace` (`rif_componenti.py:526`), `sch_*`, bugne `sch_a…d` (`corpo.py:1082-1086`) | nessuno oltre la modifica 12 della 2.1.7. La PCB prende sagoma e fori dal CAD; se la 2.1.7 allunga la scheda in avanti, il dente che scansa l'amplificatore si disegna nella PCB, non nel corpo | S; `piano-v2.1.0.md:473-489` |
| PCB-P | **due bugne con inserto M2 nella tasca accanto all'IMU** (x 60,5…71,3, y −20,9…0,75): servono anche con la millefori (S-28, S-29), ma con la PCB bassa e corta ci stanno con margine. Nuovo componente `Rif_Partitori` con le quote della PCB | S; `schemi.md:553-568` |
| Esportazioni | `guida/dati/fori.json` e `manifest.json` rigenerati (fori delle bugne nuove); STEP delle tre PCB come riferimento | S |

### 7.2 Guida

Sezione 4 (banco, `guida/passi/04-banco.yaml`), oggi "circa 12 ore la prima volta, 6–7 di saldature" (`:33`):

| Passo | Oggi | Con le PCB |
|---|---|---|
| 4.06 Basetta, taglio, fori e croci | taglio a 56 × 35, foratura con il vassoio come dima, croci a pennarello | diventa "Basetta, controllo della PCB": revisione in serigrafia, nessun taglio, nessun foro |
| 4.07 prova a secco | con Kapton sotto U2 e sopra U3 | resta (è la prova delle strip a 25,4, P-005), senza Kapton |
| 4.08–4.10 componenti e strip | posizioni per colonna-riga (E-8, A-6…) | restano; le posizioni diventano le sigle in serigrafia; CS1 e CS2 entrano qui (sono sul lato componenti); tutti i 40 pin delle strip si saldano, salvo P-2 |
| **4.11 ponticelli e barra di massa** | | **sparisce** |
| **4.12–4.14 fili 1–37, CS1 e CS2** | tre passi | **spariscono**; al loro posto un passo breve per JP1 (chiuso) e JP2, JP3 (aperti) |
| 4.15–4.19 cavo piatto, bus, seriale, tibie, 2813, VBAT | | restano, con i nomi delle piazzole; cavo piatto nelle due file sfalsate; fascette sui fori di ancoraggio |
| 4.20–4.21 prove 1–20 | sulle piazzole e nelle prese delle strip | restano, rifatte sui punti di prova; le prove dei ponti fra piazzole vicine (prova 5, 14, 20) diventano un controllo a vista, perché le reti non stanno più su fori adiacenti per forza |
| 4.22 Scheda del carapace, taglio e CE1 | | solo CE1 |
| 4.23 testata | | resta (testata a 90°, già cambiata dalla 2.1.7) |
| **4.24 ponticelli e fili 101–112** | | **sparisce** |
| 4.25 prove | | resta, sui punti di prova |
| nuovo, dopo 4.30 (già proposto in `schemi.md:543`) | | "Scheda dei partitori al banco": 16 SMD 0805 e prove 1–6 di `schemi.md` 6.5 |
| 4.26–4.28 ramo logica, prima accensione | misure su R-4, A-2, R-12, T-2 | stesse misure sui punti di prova 5V_REG, 5V_ESP, SENSE, 3V3S |

Sezione 8 (`08-elettronica.yaml`, circa 5 ore, `:45`): 8.10 "Striscia dei partitori" diventa il fissaggio della PCB-P sulle due bugne nuove con due M2 (l'avviso "nel CAD non ha un posto" sparisce); 8.22 e 8.24 cambiano i nomi delle piazzole (canale e zampa in serigrafia); 8.26 usa i punti di prova. 8.12 (basetta sulle colonnine) e i passi dei fili 8.17–8.21, 8.23 non cambiano nella sostanza.

Sezione 13 (`13-carapace.yaml`, circa 2 ore e mezza, `:74`): 13.16 "Fili sulla scheda" si semplifica (una piazzola per filo con il nome, DIN e pulsante su piazzole loro, niente più due fili per foro né saldature sui pin della testata; con il ritocco **c** niente cavo Qwiic tagliato); 13.17 senza fori da allargare; 13.18 sui punti di prova; 13.19–13.21 invariati. Appendici A.17 e A.18 (`90-appendici.yaml:389`, `:405`): un disegno della PCB al posto dei due della millefori.

Disegni e generatori: `basetta*.svg`, `scheda_carapace*.svg`, `partitori*.svg` lasciano il posto alle stampe di KiCad (serigrafia e lato rame). Le netlist di `guida/schemi/sorgenti/*_def.py` restano la fonte delle reti: proposta, un controllo che confronti la netlist di KiCad con quella dei `*_def.py`, nello stesso stile di `verifica.py` [S]. Le sezioni 1.0, 1.3, 2.3, 6.3 di `schemi.md` (zone vietate, ponticelli, fili) non servono più.

Problemi del registro che la PCB chiude o allenta (`guida/problemi/schemi.yaml`): S-08 (basetta piena, PTC sopra il buffer), S-09 (5 V accanto ai pin), S-17 in parte (posto della presa Qwiic, non dell'espansore), S-24 (Kapton), S-25 (piazzole vicine in riga 13), S-28 e S-29 (posto e altezza dei partitori). Restano aperti S-02, S-03, S-04, S-26 (impronte), S-06 (PTC), S-10, S-13, S-21, S-22, S-31.

## 8. Rischi

| Rischio | Dove | Come si riduce | Stato |
|---|---|---|---|
| **Impronta sbagliata** | interasse delle strip (25,4 o 24,7, S-02), ordine dei pin del D24V22F5 (S-03), passo del KAmod (S-04), chiave e polo 1 della testata a 90° (S-26) | dati sul pezzo o sul disegno del produttore prima di disegnare (R-20); stampa 1:1 e **dima stampata in 3D** con i moduli veri infilati, prima di ordinare | S; `produzione.md:250` |
| PCB-C disegnata prima che la 2.1.7 fissi la scheda | sagoma, fori, verso dell'allungamento, spina sopra la USB-C (0,6 mm, `requisiti.md:198`) | ordinare solo dopo la 2.1.7 chiusa in Fusion, con lo STEP della PCB provato nelle interferenze | S |
| Antenna disturbata | basetta fino a x 78, sotto il tratto finale del modulo | zona senza rame da x 74; prova del Wi-Fi al banco (portata) prima di montare | S |
| Calore di U2 chiuso sotto l'ESP32 | come oggi | il riempimento di massa aiuta a disperdere [S]; la misura di P4 resta (`docs/piano-elettronica-software.md:201`) | S |
| PTC che scatta o non protegge | S-06; la tenuta cala con il caldo | ritocco **a** oppure tetto del firmware; PTC sdraiato lontano dalla plastica | S, C |
| **Fili esterni saldati** | circa 47 fili dalla basetta, 23 dalla scheda del carapace, 26 dai partitori: restano il lavoro lungo nel corpo e il punto debole (fatica sul giunto) | fori per le fascette accanto ai fasci; la basetta resta non smontabile senza dissaldare: è il limite di questa architettura | S |
| Ritocco **b**: impulsi spuri sulla seriale durante il reset | GPIO21 flottante prima del firmware | pull-up da 10 kΩ all'ingresso del buffer; il rail dei servo è spento di default (D-019), quindi un comando sbagliato non muove niente | S, C stato di GPIO21 |
| Specchiature e versi | la PCB-C ha il lato componenti verso il basso; la PCB-B verso l'alto | "LATO COMPONENTI" e la freccia della testa del robot in serigrafia; controllo nel 3D di KiCad e nello STEP in Fusion | S; `produzione.md:251` |
| Partitori: tasca al limite | circa 0,8 mm per lato | bugne disegnate nel CAD sulla misura della PCB, non il contrario | S |
| Errore scoperto dopo la fabbricazione | una rete sbagliata | ponticelli a saldare sulle scelte aperte, SMD 0805 per tagliare una pista e mettere un filo, 4 schede di ricambio | S; `produzione.md:257` |
| Dogana e tempi | tre disegni extra UE | pannello unico, oppure Aisler | V regola; `produzione.md:65` |

## 9. Tempi

| Fase | Durata | Stato, fonte |
|---|---|---|
| Dati prima del disegno: prova a secco dell'ESP32, pagina Pololu del D24V22F5, disegno della testata Würth, scheda del carapace e bugne dei partitori nel CAD della 2.1.7 | secondo la 2.1.7 e i pezzi in casa | C; R-20 |
| Disegno con l'utente: schema da `schemi.md` 1.2, 2.2, 6.2 (le reti ci sono già); impronte dei moduli; tre layout; DRC, STEP in Fusion, dima | circa 5–6 sessioni di lavoro; la basetta è metà del lavoro | S, mia stima |
| Fabbricazione e spedizione | JLCPCB 24 ore più 8–15 giorni con la linea economica; Aisler 5–16 giorni lavorativi | `produzione.md:71`, `:73` |
| Dal via alle schede in mano | **circa 3–5 settimane** | S |
| Montaggio per l'utente, sezione 4 | da circa 12 ore (6–7 di saldature) a circa 8–9 ore (3–4 di saldature): spariscono 4.11–4.14 e 4.24 e il taglio | S, mia stima; `04-banco.yaml:33` |
| Sezioni 8 e 13 | 15–30 minuti in meno ciascuna (fili dei moduli una piazzola per filo, partitori avvitati invece che legati) | S; `08-elettronica.yaml:45`, `13-carapace.yaml:74` |

## 10. Punteggio

Da 1 (male) a 5 (bene), con i ritocchi **a**, **c** e **d** e senza **b**.

| Criterio | Voto | Perché |
|---|---|---|
| Semplicità per l'utente | **4** | spariscono fili, ponticelli, tagli e croci (circa metà delle saldature della sezione 4); restano parti THT e 0805 che salda già. Non 5 perché i circa 96 fili esterni restano tutti da saldare, nel corpo e al banco |
| Affidabilità | **4** | niente fili interni e incroci, solder mask, reti controllate da ERC e DRC, punti di prova. Non 5 perché i giunti dei fili esterni restano il punto debole e la basetta non si stacca senza dissaldare |
| Costo | **4** | circa 10–20 € in più (pannello JLCPCB, montaggio a mano), meno di 2 € di parti; nessun modulo nuovo. Le millefori di oggi costano 0 € |
| Impatto sul CAD | **5** | nessun cambio oltre la 2.1.7, salvo le due bugne dei partitori che servono comunque (S-28) |
| Riparabilità | **3** | parti THT e 0805 sostituibili, ponticelli a saldare, 4 schede di ricambio; ma una modifica alle reti vuol dire tagliare piste o rifare la PCB (sulla millefori si rifà un filo), e la basetta si toglie solo dissaldando i fili esterni |
| Compatibilità con le predisposizioni X | **4** | X3 reversibile con JP2 senza comprarlo; gruppo di riserva sul bus (X15, X32, X33); polo 14 portato a una piazzola (X25); canale 4 del buffer libero; X18, X26, X27, X29 passano dalla presa Qwiic del carapace. Non 5 perché la sagoma resta quella di oggi: nessun posto per connettori o moduli nuovi |

Media 4,0.

## 11. Da chiedere all'utente

1. Le PCB le salda lui (THT e 0805, come oggi) o vuole gli SMD montati dal produttore? Questa architettura funziona bene a mano.
2. Ritocco **b**: togliere il traslatore KAmod (una voce e un modulo in meno, tre resistenze in più)?
3. PTC (S-06): MF-R090 oppure MF-R075 con il tetto del firmware più basso?
4. Produttore: un pannello JLCPCB (8–18 €, dogana) o Aisler (circa 30 €, nell'UE)?
5. Ordinare dopo la 2.1.7 chiusa: d'accordo?
6. Aggiornare KiCad dalla 9.0.6 alla 10.0.x prima del disegno (`produzione.md:206`)? Fatto il 18 ottobre 2026 (10.0.7).
