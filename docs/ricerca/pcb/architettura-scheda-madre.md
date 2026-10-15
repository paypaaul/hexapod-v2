# Architettura 2: scheda madre (studio preliminare)

Studio del 16 ottobre 2026. Una sola PCB principale nel corpo, la **scheda madre** (SM), prende il posto della basetta dell'ESP32 e assorbe la striscia dei partitori, l'ADC, il traslatore e quello che oggi è sparso: R9 sulle luci delle tibie e le prese dei piedi e delle luci. La **scheda del carapace** (SC) resta separata e diventa anche lei una PCB, collegata alla SM dal cavo piatto di oggi. Niente è approvato né comprato: ogni voce nuova è una proposta, e il disegno vero si fa con l'utente in una versione successiva (D-076, `docs/decisioni.md:676`).

- Base dello studio: `docs/ricerca/pcb/requisiti.md` (requisiti R-01…R-20, spazi, vincoli) e `docs/ricerca/pcb/produzione.md` (produttori, costi, regole).
- Quote in mm nella terna del robot: X avanti, Y a sinistra, Z in alto, origine al centro del corpo sul piano dei femori. CAD di riferimento: 2.1.6, con le modifiche della 2.1.7 in bozza (`docs/piano-v2.1.0.md:343-566`).
- Stato dei dati: **V** verificato (fonte primaria o modello CAD), **S** stimato (calcolo mio, catalogo non riletto, ingombro di una parte comprata), **C** da confermare (sul pezzo, nel CAD o con il preventivo).

## In breve

- **Due schede**: la SM nel corpo, sul vassoio al posto della basetta, e la SC sotto il dorso. Due è il minimo, perché il carapace si toglie staccando una sola spina (R-02, `requisiti.md:217`).
- **La SM ci sta.** Il corpo resta quello della basetta (56 × 35 alle stesse quote). Si aggiungono due **orecchie** di coda per i fili e due **ali** laterali che portano le prese dei piedi e delle luci. L'inviluppo è 56 × 52, circa 25,6 cm². Sotto l'ESP32 il riempimento è circa 62 % con resistenze e condensatori SMD 0805 [S, sezione 1.3].
- **Spariscono** il traslatore KAmod, il modulo ADS7830 Adafruit, la striscia dei partitori, i 37 fili e la cinquantina di ponticelli della basetta, i 26 fili della striscia, gli 8 fili fra ADC e striscia, il ramo del bus verso l'ADC e le spine piegate senza supporto (P-012).
- **Cambia il CAD**: due colonne nuove della base sotto le ali; tolte le bugne dell'ADC e le sedi delle prese; asola dei fili spostata verso l'IMU, e l'ala del vassoio della 2.1.7 (modifica 8) non serve più; nuovo componente al posto di `Basetta`. ESP32, vassoio, colonnine e quote verticali non si muovono.
- **Costo** per 5 schede nude dei due disegni: circa 13–19 € da JLCPCB e circa 47 € da Aisler [S, da `produzione.md`]. Con gli SMD montati da JLCPCB su 2 schede madri si aggiungono circa 22–25 € [S]. Al netto dei moduli che non si comprano più, il robot costa circa 14–30 € in più di oggi se si monta tutto a mano, 27–36 € con gli SMD montati da JLCPCB [S, sezione 6].
- **Punteggi** (5 = meglio): semplicità per l'utente 4, affidabilità 4, costo 4, impatto sul CAD 3, riparabilità 3, compatibilità con le predisposizioni X 4 (sezione 11).

## 1. Schede

### 1.1 Numero e ruolo

| Scheda | Dove | Cosa fa | Perché separata |
|---|---|---|---|
| **SM, scheda madre** | sul vassoio, al posto della basetta, sotto l'ESP32 | zoccolo dell'ESP32; regolatore 5 V; D1; buffer dei LED, che porta anche la TX verso la SSC-32; partitore della RX; pull-up del bus; partitore della batteria (lato basso); ADS7830 con gli 8 partitori; prese dei 6 piedi, delle 6 luci delle tibie e delle 2 NTC; piazzole per 2813, regolatori, seriale, INA260, ToF frontale, IMU; partenza del cavo piatto | è la logica del corpo: tutto quello che sta nel corpo ci arriva |
| **SC, scheda del carapace** | sotto il dorso, davanti all'ottagono | testata 2 × 8 a 90° (J2), condensatore della catena (CE1), presa Qwiic, piazzole per catena LED, microfoni, amplificatore, ToF posteriore e pulsante; l'espansore TCA9534 si innesta sulla presa Qwiic | il carapace si toglie con una sola spina (R-02; `cablaggio.md:166`) |

La 2813, i due D42V110F6, i due INA260, l'IMU, i ToF, i microfoni, l'amplificatore e il pulsante restano dove sono e come sono (R-01, R-06, R-07; `requisiti.md:124-146`).

### 1.2 Scheda madre: sagoma e posizione

Pianta della SM vista dall'alto (non in scala; X verso destra, +Y in alto):

```
 y +26                    ┌───── ala +Y ─────┐
 y +25   ┌─ orecchia ─┐   │ FSR ×6 + NTC S   │
         │  +Y: fili  │   │ (spine in piedi) │
 y +17,5 ├────────────┴───┴──────────────────┴─────────┐
         │   corpo: come la basetta, sotto l'ESP32     │ zona
         │   (file dei pin a |y| 12,7)                 │ antenna
 y −17,5 ├────────────┬───┬──────────────────┬─────────┘ x ≥ 74
         │ orecchia −Y│   │ luci ×6 + NTC D  │
 y −25   └ cavo piatto┘   │ PTC              │
 y −26                    └───── ala −Y ─────┘
        x 22  22,5  35,5  44,5               68,5      78
```

| Parte della sagoma | Quote | Perché lì | Stato, fonte |
|---|---|---|---|
| Corpo | x 22,0…78,0, \|y\| ≤ 17,5, z 5,9…7,5 (spessore 1,6), come la basetta | inviluppo R-03; bordo di coda a 3,1 dalla morsettiera VS/VL della SSC-32; bordo a 1,3 dalle colonnine del carapace (bordo interno a \|y\| 18,8 fra x 36,3 e 43,7) | V modello (`corpo.py:85-87`; manifest `Basetta`); `requisiti.md:158`, `:165`, `:169` |
| Orecchie di coda | x 22,5…35,5, \|y\| 17,5…25,0 | fra la SSC-32 (fino a x 22) e la colonnina del carapace (da x 36,3); sopra il tetto del tunnel (bordo a \|y\| 27); l'INA260 parte da \|y\| 29 | S: zona senza parti nel manifest, conto mio; C con la verifica d'interferenza |
| Ali | x 44,5…68,5, \|y\| 17,5…26,0 | sopra le sedi di oggi delle prese (x 48,25…63,75, \|y\| 22,1…24,7, che si tolgono); 0,8 dopo la colonnina del carapace (x 43,7); il tetto del tunnel finisce a \|y\| 27, oltre c'è il camino dei regolatori (\|y\| 27…33,4) che resta libero | V prese e colonnine (manifest; `corpo.py:103-105`, `:180-181`); S il resto |
| Zona dell'antenna | x 74…78 sul corpo | niente rame su nessuno strato: solo i fori delle due colonnine anteriori, non metallizzati (R-15). Il modulo dell'antenna va da x 55,6 a 81,1: l'antenna stampata occupa all'incirca gli ultimi 6–7 mm del modulo | S (regola generale dei moduli con antenna stampata, non riletta; `requisiti.md:245`) |
| Fissaggio | 4 M2 × 5 sulle colonnine del vassoio di oggi, a (29; ±6,8) e (75,5; ±6,5); **2 M2 × 5 nuove**, una per ala, su colonne Ø6 della base a (47,5; ±20,5), dal tetto (z −9,4) fino a z 5,9 | le ali portano le spine: si spingono e si tirano a ogni smontaggio della zampa. Colonna a 1,0 dal vassoio (\|y\| 16,5) e a 1,1 dalla colonnina del carapace | V colonnine di oggi (`corpo.py:456-459`); S le nuove, da verificare nel CAD (C) |
| Inviluppo | x 22…78, \|y\| ≤ 26: 56 × 52; area circa 25,6 cm² (1960 + 195 + 408 mm²) | sotto i 100 × 100 del prezzo d'ingresso | S, conto mio |

Gli assi delle file di pin dell'ESP32 restano a \|y\| 12,7 (file a 25,4, D-076) dopo la prova a secco (P-005). Le quote verticali non cambiano: la SM sta a z 5,9…7,5 come la basetta, quindi l'ESP32 resta a z 16,0…17,6 e non si muove niente di quello che c'è sopra (camera, flat, SC).

**Quanto sono vicine le altre parti** (stime mie sul manifest della 2.1.6, da rifare con la verifica d'interferenza del CAD) [S]:
- servo di coxa anteriore: l'angolo interno delle sue alette sta circa a (70,3; ±26,8). Ho fatto il conto da asse (80; ±44), direzione 30°, 20 di larghezza e 17 dall'asse all'estremo interno con le alette (`corpo.py:30-32`). L'angolo dell'ala a (68,5; ±26) resta a circa 1,9 in X, quindi le ali non vanno oltre x 68,5;
- spine sulle ali: in piedi, con la cima a circa z 24,5 (strip maschio: 2,5 di plastica; femmina JR lunga circa 14,5). Il carapace parte da z 28,4 (`corpo.py:110`) e i cavi delle zampe entrano a z 25 (`cablaggio.md:60`): restano circa 4 mm per piegare i fili da 28–30 AWG [C];
- INA260 (x 14,15…37,05, \|y\| 29…40,2): a 4 dalle orecchie in Y.

### 1.3 Zone di montaggio e bilancio delle aree

Le parti alte non vanno sotto l'ESP32. Le parti calde stanno lontane da ESP32 e PLA. Le piazzole che servono a ESP32 inserito stanno fuori dalla sua ombra (\|y\| > 14,15).

| Zona | Quote | Area utile | Altezza libera | Cosa ci va (proposta) |
|---|---|---|---|---|
| Z1, sotto l'ESP32 fra le file | x 22…74, \|y\| ≤ 11,4 | 1186 mm² meno le 2 colonnine di coda (Ø5,8 più 1 di anello): circa 1090 | 8,5 fino all'ESP32; **6,6 sotto la microSD** (x 22,5…37,5, \|y\| ≤ 7); meno i componenti sul retro dell'ESP32, non noti (S-08) | U2 regolatore, U3 buffer, U5 ADS7830 con il suo 100 nF, D1, R1, R2, R4, R5, R7, R9, R10-R12, CS1, CS2, ponticello J1 e piazzole di X3 |
| Z2, strisce di bordo fuori dall'ombra dell'ESP32 | \|y\| 14,2…17,5, x 22…74, due lati | 2 × 3,3 × 52 = 343 mm² | libera in alto, accanto al bordo dell'ESP32 | lato +Y: 8 partitori (R da 10 kΩ in piedi a reoforo, C 0805 sul lato inferiore), piazzole del ToF frontale; lato −Y: piazzole di IMU e INA260 destro; punti di prova (5.4) |
| Z3, orecchie | x 22,5…35,5, \|y\| 17,5…25 | 2 × 97 mm² | libera | +Y: griglia 3 × 5 a passo 2,54 per 2813 (VBAT, massa, partitore, OFF), abilitazione, seriale (TX, RX, massa), INA260 sinistro; −Y: griglia 3 × 5 per i 14 conduttori del cavo piatto (poli 1–14) |
| Z4, ali | x 44,5…68,5, \|y\| 17,5…26 | 2 × 204 mm² | spine in piedi fino a z 24,5 [C] | +Y: foro M2, fila di 7 posti × 3 file (6 FSR, NTC sinistra); −Y: foro M2, PTC, fila di 7 × 3 (6 luci, NTC destra) |
| Z5, antenna | x 74…78 | — | — | solo i fori delle colonnine anteriori, nessun rame |

**Bilancio di Z1** con le parti SMD da 0805 e il regolatore modulo (ingombri di catalogo con le piazzole e un po' di spazio, S):

| Parte | mm² |
|---|---|
| U2 D24V22F5 (17,8 × 17,8 più anello) | 380 |
| U3 SN74AHCT125 in SOIC-14 (in DIP-14: 200) | 60 |
| U5 ADS7830 in TSSOP-16 con 100 nF | 55 |
| 9 resistenze e 4 condensatori 0805 | 130 |
| D1 (SMA o 1N5819 in piedi) | 20 |
| J1, piazzole di X3, prove | 30 |
| **Totale** | **circa 675, cioè 62 % di 1090** (con il DIP-14 circa 815, 75 %) |

Con 2 strati e un riempimento di massa sotto, il 60–65 % lascia spazio alle piste. Sopra il 75 % il disegno diventa difficile [S, regola pratica]. Per questo propongo i partitori nella striscia Z2 +Y, a reoforo: le resistenze di X5 e X14 sono già approvate. In Z1 vanno resistenze 0805, che non sono in casa (S-28): è una voce nuova (sezione 3.5).

### 1.4 Altezze

| Parte | Altezza sopra la SM | Limite | Stato |
|---|---|---|---|
| U2 D24V22F5 appoggiato sulla SM | 7,2 (oggi su Kapton) | 8,5 sotto l'ESP32, fuori dalla microSD | S (`requisiti.md:164`); sulla PCB il Kapton serve solo se sotto il modulo c'è rame scoperto: si lascia senza piazzole |
| SMD 0805, SOIC, TSSOP | ≤ 1,75 | 6,6 sotto la microSD | S catalogo |
| R a reoforo in piedi (solo in Z2) | circa 7 | libera (fuori dall'ombra) | S (`schemi.md:439`) |
| PTC radiale in piedi (ala −Y) | circa 12 [S] | libera; a ≥ 8 dal bordo dell'ESP32 | S |
| Spine JR sulle ali | circa 17 (z 24,5) | carapace da z 28,4 | S, C |
| Strip femmina dell'ESP32 | 8,5 | — | S (D-053) |

Sotto la SM restano 3,3 mm fino al vassoio, liberi con le viti svasate della 2.1.7 (`requisiti.md:160`). Sul lato inferiore vanno solo SMD bassi (i C dei partitori, ≤ 1 mm) lontano dalle quattro colonnine, e le saldature a reoforo devono stare sotto i 3,3.

### 1.5 Scheda del carapace

| Dato | Valore | Stato, fonte |
|---|---|---|
| Sagoma | rettangolo di circa 23 × 30, \|y\| ≤ 15, z 29,3…30,9, lato componenti in basso. **Allungata verso la coda**, x circa 26,5…49,5: allungata in avanti arriverebbe a 52,5 e toccherebbe l'amplificatore, che parte da x 51,85 | S; `requisiti.md:197-198`; `piano-v2.1.0.md:473-489`, `:540` |
| Fissaggio | 4 bugne sotto il dorso, con le due di coda spostate davanti alla testata (x ≥ 41,5) come nella 2.1.7; fori Ø2,6 | S, 2.1.7 in bozza |
| Connettore | J2 testata 2 × 8 a 90° con chiave sul bordo di coda, spina orizzontale verso −X, piedinatura di `cablaggio.md:132-143` | V decisione D-076; C codice Würth (S-26) |
| Area | circa 6,9 cm² | S |

L'inviluppo è quello della 2.1.7 ("le quote della scheda restano le stesse che servirebbero a un PCB", `piano-v2.1.0.md:475`). La SC non cambia il CAD oltre la 2.1.7; restano da chiudere i due conflitti già noti, la spina sulla USB-C (0,6 mm) e il verso dell'allungamento (`requisiti.md:198`).

### 1.6 Posti scartati per la SM

| Variante | Perché no | Fonte |
|---|---|---|
| PCB che fa da vassoio (piano a z 1,0…2,6) | il vassoio porta torretta e mensola della camera (`corpo.py:518-523`); l'ESP32 scenderebbe di circa 5 mm e cambierebbero flat, antenna e luce sotto la SC | V codice; S conseguenze |
| Nel vano sotto il vassoio | 37 × 32 × 10,4 con l'IMU che deve restare sulla base (R-06); si raggiunge solo togliendo il vassoio; l'ESP32 non ci si innesta | `requisiti.md:178`, `:307` |
| Più larga in tutto il corpo | le colonnine del carapace (x 36,3…43,7) e la parete anteriore (\|y\| ≤ 17 a x ≥ 79) fermano il corpo a ±17,5: si allarga solo con orecchie e ali | `requisiti.md:167`, `:169`, `:172` |
| SM e SC in una scheda | contro R-02: un connettore per ogni modulo del carapace | `requisiti.md:217` |
| Ala anteriore oltre x 68,5 | servo di coxa anteriore e zona dell'antenna | 1.2 |

## 2. Schema a blocchi

Fuori dalle cornici restano i pezzi che non cambiano. `[ ]` indica un connettore o una piazzola sul bordo della scheda.

```
 batteria 2S ─ T-plug ─ F1 ─ Wago ─┬─ D42V110F6 S ─ INA260 S ─ VS1 SSC-32 ─ servo 0–15
                                   ├─ D42V110F6 D ─ INA260 D ─ VS2 SSC-32 ─ servo 16–31
                                   └─ F2 2 A ─ 2813 (R6 100 kΩ, 100 kΩ su OFF) ─ VL della SSC-32
                                                │ VBAT, massa, SENSE (dopo R6), OFF
 ┌──────────────────────────── SM, scheda madre ─┼──────────────────────────────────────────────┐
 │ [orecchia +Y] ─ VBAT ─ U2 D24V22F5 ─ 5V_REG ─┬─ D1 ─ 5V_ESP ─ pin 5V ┐                       │
 │                                              ├─ U3 VCC                │  U1 ESP32-S3-CAM      │
 │                                              └─ PTC ─ 5V_LED ─┬─ [cavo piatto poli 1-2]     │
 │                                                                └─ [ala −Y: +5 V delle luci]  │
 │  3V3 dell'ESP32 ─ J1 (ponticello) ─ 3V3S ─┬─ R4, R5 pull-up ─ SDA/SCL                        │
 │                                           ├─ U5 ADS7830 (VDD = REF) ─ 8 partitori 10 kΩ     │
 │                                           │     ├─ [ala +Y: 6 FSR, NTC S]  [ala −Y: NTC D]   │
 │                                           └─ [INA S] [INA D] [ToF frontale] [IMU] [poli 7]   │
 │  GPIO48 ─ R1 ─ U3 canale 1 ─ R2 ─ [polo 4: anello e lobi]                                    │
 │               └ U3 canale 2 ─ R9 ─ [ala −Y: dato delle 6 luci]                               │
 │  GPIO21 TX ─ R10 pull-up ─ U3 canale 3 ─ [orecchia +Y: RX della SSC-32]                      │
 │  GPIO14 RX ─ partitore R11/R12 ─────────── [orecchia +Y: TX della SSC-32]                   │
 │  GPIO1 ─ R7 47 kΩ, CS1 ─ [orecchia +Y: SENSE]     GPIO41 ─ [OFF]   GPIO42 ─ D2 ─ [ENA]      │
 │  GPIO38-40, GPIO2 (I2S) ─ [cavo piatto poli 10-13]   polo 14 ─ [riserva, piazzola libera]    │
 └──────────────────────────────────────────────┬───────────────────────────────────────────────┘
                     cavo piatto 16 vie, 15 cm   │  poli 15-16 separati prima della SM ─ A e B della 2813
 ┌───────────────── SC, scheda del carapace ─────┼───────────────────────────────────────────────┐
 │ J2 2 × 8 a 90° ─ CE1 470 µF ─ 5 V: [catena LED] [amplificatore]                              │
 │                ─ 3,3 V, I2C: [ToF posteriore] [presa Qwiic ─ TCA9534 (X20) ─ XSHUT]          │
 │                ─ I2S: [microfoni (R8 100 kΩ al microfono)] [amplificatore]                  │
 │                ─ poli 15-16: [pulsante]                                                      │
 └───────────────────────────────────────────────────────────────────────────────────────────────┘
 Abilitazione: [ENA] ─ filo ─ R3 22 kΩ su ciascun D42V110F6 (pull-down all'estremo lontano, R-12)
```

Rispetto alla basetta di oggi (`schemi.md:42-60`, `cablaggio.md:40-50`) le reti e i GPIO non cambiano: stessi 15 pin dell'ESP32, stessi indirizzi I2C, stessa piedinatura del cavo piatto. Cambiano tre cose:
1. **TX verso la SSC-32 dal canale 3 del buffer**, al posto del canale 1 del KAmod. L'SN74AHCT125 alimentato a 5 V riconosce i 3,3 V come livello alto (soglia TTL di 2 V) e dà in uscita 5 V pieni [S, scheda TI non riletta per questo studio]. Non serve più la soglia della seriale del clone (C in `requisiti.md:241`). R10, 10 kΩ verso 3V3S all'ingresso, tiene la linea a riposo alta mentre l'ESP32 si avvia [S].
2. **RX dalla SSC-32 con un partitore**: R11 da 10 kΩ verso la SSC-32, R12 da 20 kΩ a massa, quindi 5,0 V × 20/30 = 3,33 V su GPIO14. Con circa 8 pF fra pin e pista, la costante di tempo è 6,7 kΩ × 8 pF ≈ 53 ns; un bit a 230400 baud dura 4,3 µs [S, conto mio]. Se R12 si stacca, il GPIO riceve al più (5,0 − 3,3 − 0,5) / 10 kΩ ≈ 0,12 mA dal diodo di protezione [S]. È il punto più debole del cambio. L'alternativa robusta è un 74LVC1G17 alimentato a 3,3 V, con ingresso che regge 5 V: un chip SOT-23-5 in più.
3. **ADS7830 sulla scheda**: il VDD e il REF prendono il 3V3S, che alimenta anche i partitori. La lettura resta in rapporto (R-05; `schemi.md:433`). Il riferimento esterno si sceglie con i bit PD del comando [S, scheda TI da rileggere: C].

## 3. Componenti

### 3.1 Scheda madre

"Voce" è la riga del BOM. "Stato" dice se la parte c'è già (in casa, comprata o approvata) o se è **nuova**, cioè da approvare. Le altezze sono in 1.4.

| Sigla | Cosa | Contenitore sulla PCB | Voce | Stato | Note |
|---|---|---|---|---|---|
| U1 | ESP32-S3-CAM UICPAL N16R8 RE1.3 su 2 strip femmina 1 × 20 | THT, file a 25,4 | A2, C2 | in casa | resta estraibile (R-01). Prova a secco prima di ordinare la PCB (P-005) |
| U2 | Pololu D24V22F5 | modulo THT, 5 pin in fila | B2 | approvato, da comprare | ordine dei pin dalla pagina Pololu (S-03, C). Resta modulo: un convertitore da 2,5 A disegnato da zero sotto l'ESP32 è il rischio più alto e non toglie acquisti (`requisiti.md:129`) |
| U3 | SN74AHCT125 | **SOIC-14** (consigliato) o DIP-14 | X9 | DIP-14 approvato per il provino 7 | canali: 1 anello e lobi, 2 tibie, **3 TX della SSC-32**, 4 libero con ingresso e OE a massa. Il SOIC è una voce nuova piccola; il DIP-14 riusa quello approvato ma occupa 200 mm² |
| U5 | ADS7830IPW | **TSSOP-16**, passo 0,65 | nuova (sostituisce X6) | nuova | il solo passo fine della scheda: a mano con flussante e trascinamento, oppure montato da JLCPCB (sezione 6) |
| R1 | 10 kΩ, pull-down di GPIO48 | 0805 | kit 0805 (nuovo); oggi X9 a reoforo | — | come oggi |
| R2 | 330 Ω, dato verso il polo 4 | 0805 | kit 0805 (nuovo); oggi X9 a reoforo | — | come oggi |
| R9 | 330 Ω, dato delle tibie | 0805 | kit 0805 (nuovo); oggi X9 a reoforo | — | **entra sulla scheda**; oggi è in linea nella guaina |
| R4, R5 | pull-up di SCL e SDA, **3,3 kΩ** | 0805 | kit 0805 (nuovo); oggi B10 a reoforo | — | senza il modulo ADS7830 sparisce un 10 kΩ dal bus: con 4,7 kΩ l'equivalente salirebbe a circa 1,40–1,63 kΩ, con 3,3 kΩ è circa 1,25–1,42 kΩ, nella finestra 1,0–1,4 (conto con 10 kΩ su INA260 × 2, GY-6500, ToF frontale e ToF posteriore se c'è; S-13) [S] |
| R7 | 47 kΩ 1 %, partitore della batteria, lato basso | 0805 | kit 0805 (nuovo); oggi B10 a reoforo | — | R6 resta alla 2813 (R-12) |
| R10 | 10 kΩ, pull-up della TX | 0805 | kit 0805 | nuova (funzione) | 2.1 |
| R11, R12 | 10 kΩ e 20 kΩ, partitore della RX | 0805 | kit 0805 | nuova (funzione) | 2.2; sostituiscono il KAmod |
| RP1–RP8 | 10 kΩ 1 %, partitori di FSR e NTC | **a reoforo in piedi**, in Z2 +Y | X5, X14 | approvate | come la striscia di oggi (`schemi.md:439-446`) |
| CP1–CP8 | 100 nF, partitori | 0805, lato inferiore in Z2 +Y | B8 | in casa (taglia da guardare: S-30) | C7 e C8 sulle NTC come proposti in `schemi.md:442` |
| CS1, CS2, CU5 | 100 nF: GPIO1, U3, U5 | 0805 | B8 | in casa | CU5 è nuova: disaccoppiamento dell'ADC, che oggi sta sul modulo |
| D1 | Schottky fra 5V_REG e pin 5V | 1N5819 in piedi, o SS14 in SMA | C3 | approvato | S-07 invariato |
| D2 | 1N4148, abilitazione | a reoforo, anodo verso GPIO42 | — (già nello schema) | come oggi | **entra sulla scheda**: niente più giunzione nella guaina. Le R3 restano sui regolatori (R-12), quindi un filo staccato lascia il rail spento |
| PTC1 | fusibile ripristinabile del 5 V dei LED | radiale in piedi, sull'ala −Y | X9 (MF-R075) | approvato | tenuta 0,75 A contro circa 0,86 A del ramo (S-06): l'impronta radiale accetta anche un MF-R090 o un MF-R110 se si decide di salire (R-10) [S catalogo Bourns] |
| J1 | ponticello a saldare 3V3 dell'ESP32 → 3V3S | piazzola sulla PCB | — | — | chiuso di fabbrica con una goccia di stagno; con X3 si apre (R-17) |
| X3 | piazzole per un D24V5F3 | 3 piazzole, non montato | X3 (tolto) | non si compra | R-17: si torna al regolatore senza ridisegnare |
| JF | prese dei piedi e NTC S: 7 posti × 3 file | strip maschio 2,54 in piedi, sull'ala +Y; fila centrale senza pin | come le prese di oggi (X5) | approvate | le femmine JR delle FSR usano 2 poli su 3 (`cablaggio.md:107`) |
| JL | prese delle luci e NTC D: 7 × 3 | strip maschio 2,54 in piedi, sull'ala −Y; sulla NTC niente pin centrale | come oggi (X31) | approvate | ordine massa, +5 V, dato, come un servo |
| TP1–TP12 | punti di prova | piazzole nude Ø1,5 | — | — | 5.4 |
| JR1 | misura RMT al banco | 2 piazzole 0805 non montate più un ponticello a saldare verso GPIO38 | — | — | sostituisce il canale 4 libero del KAmod (`schemi.md:227`) |

Parti attive sulla SM: 1 modulo ESP32, 1 modulo regolatore, 2 integrati (buffer, ADC). Oggi sono 4 moduli (ESP32, regolatore, traslatore, ADC) più 1 integrato (buffer). Parti passive, diodi compresi: 31, contro le 27 di oggi (9 sulla basetta, 16 sulla striscia, R9 e D2 nella guaina). Le quattro in più sono R10, R11, R12 e CU5, che oggi stanno dentro i moduli.

### 3.2 Scheda del carapace

| Sigla | Cosa | Contenitore | Voce | Stato | Note |
|---|---|---|---|---|---|
| J2 | testata 2 × 8 a 90° con chiave | THT | X2 (Würth 61201621721, C) | approvata, non comprata | D-076; S-26 |
| CE1 | 470 µF 10 V, Ø6,3 × 8 | radiale sdraiato | X2 | approvato, non comprato | D-076 |
| JQ | presa Qwiic JST SH 4 poli | SMD, passo 1,0 | **nuova** (al posto del cavo 4210 tagliato) | nuova | sulla PCB si salda, sulla millefori no (`schemi.md:326`) |
| — | TCA9534 | modulo SparkFun DEV-17047 sulla presa JQ, con un cavo Qwiic corto | X20 | in arrivo il 24 novembre | resta modulo: è già comprato. Il posto lo dà la PCB (S-17). Pull-up del modulo tagliati (S-13) |
| — | piazzole: catena LED (3), microfoni (5), amplificatore (5), ToF posteriore (4), XSHUT dal modulo (1), pulsante (2, sui poli 15-16), riserva polo 14 (1) | fori metallizzati 1,0 | — | — | serigrafia con il nome di ogni filo |
| TP | 5 V, 3,3 V, massa, SDA, SCL | piazzole nude | — | — | prove di 13.18 |

R8, il pull-down da 100 kΩ dei microfoni, resta al microfono (`schemi.md:261`).

### 3.3 Cosa sparisce

| Cosa | Voce | Risparmio | Fonte |
|---|---|---|---|
| Traslatore KAmod Level Shift x4 | C1 | 2,51 € (non comprato) | `BOM.md:70`; `requisiti.md:131` |
| Modulo Adafruit ADS7830 #5836 | X6 | 6,37 € (approvato, non comprato) | `BOM.md:170` |
| Striscia dei partitori (millefori, 2 viti M2, fissaggio non risolto) | X5, X14 | S-28 e S-29 chiusi | `schemi.md:433` |
| Bugne dell'ADC sul tetto, sedi delle prese, ala del vassoio della 2.1.7 | — | CAD più semplice (sezione 7) | `corpo.py:960-975`, `:998`; `piano-v2.1.0.md:424-431` |
| 37 fili isolati, circa 50 ponticelli e la barra di massa della basetta | — | il lavoro più lungo della sezione 4 (passi 4.11–4.14) | `schemi.md:102-149` |
| 26 fili della striscia, 8 fili fra striscia e ADC, ramo 3 del bus verso l'ADC | — | sezione 8 (8.09, 8.10, 8.22) | `schemi.md:511-524` |
| Spine JR piegate senza supporto (P-012), fili delle prese verso striscia e basetta | — | spine sulla PCB | `requisiti.md:145` |
| Giunzioni in guaina di R9 e D2 | — | componenti sulla PCB | `schemi.md:60` |
| Nastro Kapton sotto regolatore e PTC (S-24) | — | basta il solder mask, con niente rame scoperto sotto il modulo | `requisiti.md:164` |
| Millefori C2 per basetta e SC | C2 (in casa) | resta in casa | — |
| Problemi aperti dello schema che si chiudono | — | S-04 (KAmod), S-08 (in parte), S-09 e S-25 (vicinanze fra piazzole: le decide il disegno), S-28, S-29, S-31 (piedinatura del modulo ADC) | `guida/problemi/schemi.yaml` |

### 3.4 Cosa resta fuori dalle schede, apposta

Il principio di R-12 resta: un filo staccato lascia tutto spento o al sicuro.
- R6 da 100 kΩ, saldata sull'uscita della 2813: il filo SENSE porta al più 2,7 V attraverso 100 kΩ.
- La 100 kΩ fra OFF e massa, sulla 2813 (S-11).
- R3 da 22 kΩ fra ENA e massa, su ciascun D42V110F6 (S-05, S-20).
- R8 al microfono.
- I poli 15-16 del cavo piatto, separati prima della SM e giuntati ai fili verso A e B della 2813: non passano dalla logica (`requisiti.md:232`, S-10).

### 3.5 Acquisti nuovi (proposte, da approvare)

| Cosa | Per | Quantità | Prezzo | Stato |
|---|---|---|---|---|
| ADS7830IPW (TSSOP-16) | U5 | 1 + 1 di scorta | circa 3–5 € l'uno da Mouser, DigiKey o LCSC | S, catalogo non riletto |
| Kit di resistenze 0805 1 % (o le sole 10 k, 3,3 k, 20 k, 47 k, 330) | R1, R2, R4, R5, R7, R9-R12 | — | circa 5–10 € il kit | S; in alternativa le monta JLCPCB come parti Basic |
| SN74AHCT125 in SOIC-14 | U3 | 1 + 1 | circa 0,5 € | S; facoltativo (il DIP-14 approvato va bene, con meno spazio) |
| JST SH 4 poli SMD orizzontale (tipo SM04B-SRSS-TB) | JQ sulla SC | 2 | circa 0,5 € l'uno | S |
| PCB | SM e SC | 5 + 5 | sezione 6 | S |

Totale delle parti: circa 10–20 € più la spedizione, se non viaggiano con un ordine DigiKey già previsto per le voci X. Si risparmiano C1 e X6 (8,88 €, V dai prezzi del BOM).

## 4. Connettori e cavi

Scelta di base: **fili saldati sulle piazzole** dove oggi si saldano (meno componenti), **spine** dove oggi ci sono già spine. La SM si salda al banco con i suoi fili e si monta poi nel robot, come oggi la basetta (`requisiti.md:255`).

| Collegamento | Fili | Sulla SM | All'altro capo | Lunghezza | Rispetto a oggi |
|---|---|---|---|---|---|
| 2813: VBAT, massa, SENSE (dopo R6), OFF | 4 × 26 AWG (VBAT siliconico se c'è, S-27) | piazzole nell'orecchia +Y; VBAT in un angolo con un posto vuoto accanto | saldati sulla 2813 | circa 25 cm (`BOM.md:59`) | uguale; i fili non passano più sotto l'ESP32 |
| Abilitazione dei regolatori | 1 × 26 AWG, poi 2 dopo la diramazione | piazzola nell'orecchia +Y, dopo D2 | ENA dei due D42V110F6 con le R3 | fino alle baie | D2 non è più nella guaina |
| Seriale della SSC-32: TX, RX, massa | 3 × 26 AWG | piazzole nell'orecchia +Y | Dupont femmina (C4) sui pin della SSC-32 | pochi cm | uguale; la massa resta da decidere (S-22) |
| INA260 sinistro | 4 (cavo Qwiic 4210 tagliato) | piazzole nell'orecchia +Y | presa STEMMA QT dell'INA260 | circa 10 cm | uguale |
| INA260 destro | 4 (idem) | piazzole in Z2 −Y, x 24…34 | idem | circa 10 cm | uguale |
| ToF frontale VL53L7CX | 4 × 30 AWG | piazzole in Z2 +Y, x 66…74 | saldati al ToF (VDD a 3,3 V) | lungo la torretta | uguale |
| IMU GY-6500 | 4 × 30 AWG | fori in Z2 −Y, x 62…72: i fili salgono dall'asola del vassoio | saldati sull'IMU | circa 6 cm [S] | ramo 3 senza l'ADC |
| Scheda del carapace | cavo piatto 16 vie: poli 1–14 sulla SM; 15-16 separati e giuntati ai fili della 2813 | griglia 3 × 5 a passo 2,54 nell'orecchia −Y, conduttori aperti a ventaglio | spina IDC 2 × 8 con chiave sulla J2 della SC | circa 15 cm [S] | griglia sulla PCB al posto della riga 13; poli 1-2 e 4 lontani dai pin dell'ESP32 |
| Pulsante → A e B della 2813 | 2 | non passano dalla SM | giunti a 26 AWG, stagno e guaina | | uguale (`requisiti.md:69`) |
| 6 FSR dei piedi | 2 per zampa (doppino 28 AWG) | **spine sull'ala +Y**, posti 1–6, ordine AS, MS, PS, AD, MD, PD (canali 0–5, C) | sotto la punta dello stinco | 0,4–0,5 m | prima andavano sul tetto e poi alla striscia con altri fili |
| 6 luci delle tibie | 3 per zampa (30 AWG) | **spine sull'ala −Y**, posti 1–6 | capo alto della striscia della tibia | circa 0,5 m | prima andavano sul tetto e poi alla basetta con 3 fili e R9 nella guaina |
| 2 NTC dei regolatori | 2 per NTC (28 AWG) | posto 7 delle due file di spine, senza pin centrale | sulla bobina del regolatore | circa 5 cm dall'ala | prima andavano alla striscia nel vano |
| Misura RMT (solo al banco) | 1 provvisorio | JR1 | uscita di un canale della SSC-32 | | sostituisce il canale 4 del KAmod |

**Sulla SC**: J2 verso la SM. Piazzole saldate per catena LED (3 fili, X31), microfoni (5), amplificatore (5), ToF posteriore (4, più XSHUT dal TCA9534), pulsante (2) e polo 14 di riserva. Presa Qwiic JQ per il modulo TCA9534 e per le espansioni (`requisiti.md:96-104`).

**Spine sulle ali.** Le femmine JR non hanno chiave su una fila di pin nuda. Girate di 180° non fanno danni, eccetto in un caso:
- FSR e NTC sono resistenze: il verso non conta.
- Luci: il +5 V resta al centro, massa e dato si scambiano. Il dato bufferizzato vede allora la striscia attraverso R9 da 330 Ω: con l'uscita bassa ci passano circa (5 − 0,5) / 330 ≈ 14 mA, sopra gli 8 mA della corrente d'uscita nominale dell'AHCT125 ma sotto il massimo assoluto [S, scheda TI non riletta].

Contromisure: serigrafia con il colore del filo di massa e il nome della zampa; prova al multimetro al passo 8.23.

Connettori che si potrebbero aggiungere, **non proposti** per la preferenza "meno componenti": prese JST SH per i due INA260 (i cavi Qwiic non andrebbero tagliati), una testata 2 × 8 con chiave al posto del cavo piatto saldato sulla SM (non sta sotto l'ESP32 e in un'orecchia ci sta a fatica), morsetti per la 2813. Ciascuno rende la SM smontabile senza dissaldare, ma è una voce in più.

## 5. Strati e regole

### 5.1 Strati

**2 strati, 1,6 mm, rame da 1 oz (35 µm), HASL senza piombo**, per tutte e due le schede (`produzione.md:278`). Sopra ci sono i componenti e le piste di potenza; sotto, un riempimento di massa intero, interrotto solo nella zona dell'antenna. Sulla SM non passano le correnti dei servo, che restano su fili, Wago, INA260 e SSC-32 (`produzione.md:19`). Il 4 strati non serve: l'unico segnale veloce è il clock I2S a circa 3 MHz, che attraversa la SM in pochi centimetri (`requisiti.md:55`).

### 5.2 Correnti e larghezze delle piste

Larghezze per lo strato esterno con 1 oz e +10 °C, dalla tabella IPC-2221 di `produzione.md:167-172` [S]:

| Rete | Corrente | Fonte della corrente | Pista proposta | Minimo dalla tabella |
|---|---|---|---|---|
| VBAT (orecchia → VIN di U2) | fino a circa 2,3 A; 3 A se F2 passa a 3 A | `requisiti.md:43`, `:223` | **1,5 mm** | 1,37 a 3 A |
| 5V_REG (U2 → D1, PTC, U3) | fino a 2,5 A (limite di U2) | `requisiti.md:44` | **1,5 mm** o riempimento | 1,37 a 3 A |
| 5V_LED (PTC → poli 1-2, ala −Y) | circa 0,86 A; transitorio fino allo scatto del PTC | S-06 | **1,0 mm** | 0,30 a 1 A, 0,78 a 2 A |
| 5V_ESP (D1 → pin 5V) | 0,25 / 0,5 A | `requisiti.md:45` | 0,6 mm | 0,30 a 1 A |
| 3V3S | circa 0,2 A | `requisiti.md:47` | 0,5 mm | — |
| Masse di ritorno di LED e ingresso | come il loro 5 V | | riempimento sotto, più una pista da 1,5 mm sopra fra la massa di U2, la griglia del cavo piatto e l'ala −Y | |
| Segnali (I2C, seriale, dato LED, I2S, ADC) | mA | | 0,25 mm | — |

### 5.3 Separazione del VBAT

- VBAT sta su un'isola sola: piazzola nell'orecchia +Y, pista da 1,5 mm, piazzola VIN di U2. Non tocca nient'altro (R-08).
- Distanza dal rame delle altre reti almeno **1,0 mm**, contro gli 0,2 della regola generale [S, proposta mia]. A 8,4 V non serve per l'isolamento: serve contro i ponti di stagno e i graffi.
- Per arrivare a U2 il VBAT attraversa la fila +Y dei pin dell'ESP32. Passa nel tratto dei pin non usati C…H (GPIO13…46, `schemi.md:93`), sul lato inferiore, con piste di massa ai due lati. In quel tratto i fori della strip sono **non metallizzati**: i pin non usati si tagliano a filo come oggi.
- Nessuna piazzola VBAT accanto a una piazzola a 3,3 V o a un GPIO. Nell'orecchia, VBAT ha un posto vuoto accanto e confina solo con la massa.

### 5.4 Altre regole

- **5 V lontano dai GPIO** (R-09): nessuna piazzola o pista a 5 V a meno di 1,0 mm da un pin dell'ESP32 senza una massa in mezzo. Le piazzole a 5 V del cavo piatto stanno nell'orecchia −Y, fuori dalla zona dei pin. Sparisce il controllo al multimetro delle vicinanze inevitabili (S-09, S-25).
- **Antenna** (R-15): niente rame su nessuno strato per x ≥ 74 [S]. I fori delle colonnine anteriori sono non metallizzati.
- **Analogico**: ADC e partitori lontani da U2, il convertitore a commutazione. I ritorni dei LED non passano sotto ADC e partitori. Le piste dei partitori verso l'ADC sono corte, sul lato superiore, con la massa sotto (`requisiti.md:244`).
- **Regole del produttore**: pista e spazio 0,20 mm, via 0,3 / 0,6 mm, rame a 0,5 mm dal bordo; fori delle viti M2 da 2,2 mm non metallizzati, con 1 mm senza rame attorno (`produzione.md:179-193`). Le zone vietate di oggi sotto la SM (colonnine, `schemi.md:33-36`) restano senza piazzole sul lato inferiore.
- **Sotto U2**: nessun rame scoperto, così il modulo appoggia sul solder mask senza Kapton.
- **PTC sull'ala −Y**: niente nel raggio di 3 mm; a più di 8 mm dal bordo dell'ESP32 e lontano dal vassoio in PLA (`requisiti.md:227`).
- **Punti di prova** (R-16), fuori dall'ombra dell'ESP32, quindi raggiungibili anche con l'ESP32 inserito:
  - VBAT, 5V_REG, 5V_LED, 3V3S, due masse;
  - SDA, SCL;
  - TX verso la SSC-32, RX dopo il partitore;
  - DATA, DATA2, SENSE, ENA.

  Il 5V_ESP si misura nella presa della strip, come oggi.
- **Serigrafia**: nome, revisione e data ("HEX2 SM r1"); "LATO COMPONENTI"; pin 1 e polarità; nome di ogni piazzola; zampa e canale su ogni spina (`produzione.md:251`, `:260`).
- **Ponticelli e impronte non montate** sulle scelte aperte: J1 (3V3 dell'ESP32 → 3V3S) e JR1 sulla SM; sulla SC un'impronta 0805 vuota fra la linea dei microfoni e la massa, se la decisione su S-21 sposta R8 dal microfono alla scheda.

## 6. Costo stimato per 5 schede

Prezzi, dogana e cambio (1 $ ≈ 0,86 €) da `produzione.md` (righe 7, 27-33, 44-53, 81-92, 264-274). Si fabbricano 5 SM e 5 SC (Aisler a gruppi di 3, quindi 6). Le aree sono l'inviluppo della SM, 56 × 52 = 29,1 cm², e la SC, 23 × 30 = 6,9 cm². Tutti i totali sono **S**, da rifare con il preventivo vero (C).

### 6.1 Schede nude

| Strada | Calcolo | Totale consegnato |
|---|---|---|
| JLCPCB, due disegni separati nello stesso carrello, linea economica | 2 × 2 $ + spedizione 3–6 $ = 7–10 $; con l'IVA al 22 % 8,5–12,2 $, cioè 7,3–10,5 €; dazio 3 € × 2 voci = 6 € (C: quante voci); dal 1° dicembre 2026 più 2 € | **circa 13–19 €** |
| JLCPCB, un pannello con SM e SC | 2–10 $ (sovrapprezzo per i disegni diversi, C) + 3–6 $; con l'IVA 6,1–19,5 $, cioè 5,2–16,8 €; una voce: 3 € (+2 €) | **circa 8–22 €** |
| Aisler, due progetti da 6 | SM: 12 + 29,1 × 0,067 × 6 = 23,71 €; SC: 12 + 6,9 × 0,067 × 6 = 14,77 €; totale 38,48 €, con l'IVA 46,95 €; spedizione gratuita, niente dogana | **circa 47 €** (listino del 2023, C) |
| Aisler, un pannello di circa 40 cm² da 6 | 12 + 40 × 0,402 = 28,08 €, con l'IVA 34,26 € | **circa 34 €** |

### 6.2 Schede montate

| Strada | Calcolo | Totale in più rispetto alle nude |
|---|---|---|
| **A mano** (proposta di `produzione.md:142`, 279) | parti nuove della sezione 3.5: ADS7830 × 2, kit 0805, JST SH × 2, eventuale SOIC; THT e moduli già approvati | **circa 10–20 €** più la spedizione delle parti |
| **JLCPCB Economic, solo SMD, 2 SM montate su 5** (`produzione.md:83-97`) | avvio 8,18 + stencil 1,53 + conferma 0,45 = 10,16 $; caricamento Extended dell'ADS7830 3,07 $ (e del buffer SOIC se non è Basic: altri 3,07, C); giunti circa 120 × 2 × 0,0016 = 0,38 $; parti per 2 schede circa 7 $; totale 20,6–23,7 $, con l'IVA 25–29 $ | **circa 22–25 €** |
| Montaggio THT del produttore (strip, spine, moduli) | non conviene (`produzione.md:144`) | — |

Economic monta **una faccia sola** (`produzione.md:83`). Con JLCPCB quindi i condensatori dei partitori vanno sul lato superiore, e conviene fare 0805 anche le 8 resistenze dei partitori: sono parti Basic. La SC non ha SMD che valga la pena far montare: la presa JST SH si salda a mano.

### 6.3 Quanto costa in più al robot

| Strada | Schede | Montaggio o parti | Si risparmia | Netto |
|---|---|---|---|---|
| JLCPCB separate, tutto a mano | 13–19 € | 10–20 € | C1 e X6: 8,88 € | **circa 14–30 €** |
| JLCPCB separate, SMD montati da loro | 13–19 € | 22–25 € più circa 1 € (JST SH della SC) | 8,88 € | **circa 27–36 €** |
| Aisler in pannello, tutto a mano | 34 € | 10–20 € | 8,88 € | **circa 35–45 €** |

Oggi le millefori costano zero (C2 in casa), ma chiedono circa 6–7 ore di saldature solo nella sezione 4 (`guida/passi/04-banco.yaml:33`).

## 7. Cambi al CAD

Si fanno in una versione dopo la 2.1.7, con il piano in `docs/piano-v2.1.0.md` come per le altre (CLAUDE.md, "Versioni"). Se la SM si sceglie prima di costruire la 2.1.7, la modifica 8 della 2.1.7 (asola del bus con l'ala del vassoio, `piano-v2.1.0.md:424-431`) **non va fatta**. Tutto il resto della 2.1.7 resta: colonne del vassoio, file a 25,4, SC allungata.

| N. | Script e funzione | Cosa cambia | Parametri | Verifica |
|---|---|---|---|---|
| 1 | `corpo.py` → `fai_base` | due colonne Ø6 dal tetto (z −9,4) a z 5,9 sotto le ali, a (47,5; ±20,5), con inserto M2 in cima | nuovi `cor_sm_col_x` 47,5, `cor_sm_col_y` 20,5 [S] | colonna contro vassoio (atteso 1,0), colonnina del carapace (atteso 1,1), freccia dell'asse X dell'IMU (asta a y −16,5…−15,5: atteso 1,0) |
| 2 | `corpo.py` → `fai_base_predisposizioni` (righe 980-1007) | via le bugne dell'ADC (`ins_ads_a/b`) e le due sedi delle prese (`_prese`, righe 960-966); la freccia dell'asse X dell'IMU (righe 1001-1004) resta | `cor_ads_x`, `cor_ads_y`, `cor_pre_x`, `cor_pre_y` non servono più nella base | sentinella sui volumi della base; IMU invariata |
| 3 | `corpo.py` → `fai_vassoio` (righe 524-526) | l'asola del bus diventa una tacca sul bordo −Y del piano, a x circa 62…70, accanto all'IMU, per i 4 fili dell'IMU che salgono ai fori della SM in Z2 −Y; niente ala | `cor_vas_asola_x` circa 66; tacca larga 3 [S] | `vassoio`; i fili non passano sotto i pin dell'ESP32 |
| 4 | `rif_componenti.py` (righe 109-111, 503, 527) e `assieme.py` (righe 63, 94-96) | `Rif_Basetta_50x70` diventa `Rif_Scheda_Madre`: corpo, orecchie e ali dai parametri, più l'**ingombro delle spine** sulle ali (z 7,5…24,5, \|y\| 18,2…25,9); via `Rif_ADC_ADS7830`; `Prese_piedi` e `Prese_luci` si tolgono dall'assieme: ora stanno nell'ingombro della SM | nuovi `sm_ala_x0` 44,5, `sm_ala_x1` 68,5, `sm_ala_y` 26, `sm_ore_x1` 35,5, `sm_ore_y` 25 [S] | `controllo`, `interferenze`: SM contro colonnine del carapace, SSC-32 (morsettiera VS/VL), INA260, servo di coxa anteriori, colonne nuove; spine contro il carapace (`sfilamento`) e contro i cavi dei servo a z 25 |
| 5 | `esporta_robot.py` (riga 58), `viste.py` (riga 56), `colori.py` (riga 55) | masse e viste: via ADC e prese, aggiunta la SM | — | CI `ci` e `sim` verdi |
| 6 | Fusion, dopo il disegno KiCad | lo STEP della PCB (`kicad-cli pcb export step`, origine ausiliaria a (22; 0)) sostituisce l'ingombro a scatola; contorno da Fusion a KiCad in DXF (`produzione.md:238-244`) | — | interferenze con i modelli veri dei moduli |
| 7 | Scheda del carapace | nessuna oltre la 2.1.7 (modifica 12): restano da chiudere spina contro USB-C e verso dell'allungamento | — | come la 2.1.7 |

**Viteria e BOM**:
- viti: +2 M2 × 5 a testa tonda (D8) e +2 inserti M2 (D5) per le ali; −2 viti e −2 inserti M2 dell'ADC; le 2 M2 della striscia (S-29) non servono più;
- BOM: escono C1 e X6, entrano le voci di 3.5.

**Documenti da aggiornare se si sceglie**:
- D-053 (basetta), D-066 (asola) e D-069 (prese sul tetto), con il rimando alla decisione nuova;
- `cablaggio.md` 3.3 e 3.4: prese, ramo 3, NTC;
- `predisposizioni.md` 2.8: vano sotto il vassoio con la sola IMU;
- `BOM.md`;
- `guida/schemi/`: gli schemi delle millefori diventano lo schema KiCad e i suoi disegni.

## 8. Cambi alla guida

La guida resta sulle millefori finché la SM non è ordinata e provata (D-076). Quando si passa, cambiano questi passi (titoli da `guida/passi/*.yaml`):

**Sezione 4, banco dell'elettronica** (oggi circa 12 ore, 6–7 di saldature, `04-banco.yaml:33`):

| Passi di oggi | Con la SM |
|---|---|
| 4.06 taglio, fori e croci | **controllo della PCB**: a vista, serigrafia, continuità fra massa e 5 V, 5 V e VBAT (devono essere aperti) |
| 4.07 prova a secco | resta sulla PCB vera. La prova decisiva si fa prima dell'ordine, sulla dima stampata (sezione 9) |
| 4.08 resistenze, D1 e U3; 4.09 traslatore, regolatore e PTC | **SMD** (0805, SOIC, TSSOP dell'ADC; si salta se li monta JLCPCB), poi **THT**: D1, D2, partitori in piedi, U2, PTC sull'ala −Y. Il traslatore sparisce |
| 4.10 strip dell'ESP32 | strip più spine delle ali (2 file da 7 × 3, senza il pin centrale ai posti delle NTC e delle FSR) |
| 4.11–4.14 ponticelli, barra di massa, fili 1–37, CS1 e CS2 | **spariscono**: le reti sono piste |
| 4.15 cavo piatto | resta: conduttori 1–14 nella griglia dell'orecchia −Y; 15-16 separati |
| 4.16 rami del bus | INA260 sinistro nell'orecchia +Y, destro e IMU in Z2 −Y, ToF in Z2 +Y; ramo 3 senza l'ADC |
| 4.17 seriale e luci delle tibie | solo la seriale: le luci si innestano sull'ala al passo 8.23 |
| 4.18 fili verso 2813 e regolatori; 4.19 filo della batteria | uguali, sulle piazzole dell'orecchia +Y; D2 è già sulla scheda |
| 4.20–4.21 prove 1–20 al multimetro | riscritte sui punti di prova: spariscono le prove delle vicinanze fra piazzole (S-09, S-25) e restano quelle delle reti e delle resistenze verso massa |
| 4.22–4.25 scheda del carapace | taglio → controllo della PCB; CE1, J2, presa Qwiic SMD; fili 101–112 sulle piazzole con il nome; prove sui punti di prova |
| 4.26–4.28 ramo logica, prima accensione senza ESP32, ESP32 negli strip | uguali, misure sui punti di prova |

Stima: le saldature della sezione 4 scendono da 6–7 ore a circa 2,5–3,5 ore [S].

**Sezione 8, elettronica nel corpo**:

| Passi di oggi | Con la SM |
|---|---|
| 8.07 fili del bus nell'asola | solo i 4 fili dell'IMU, nella tacca −Y |
| 8.09 ADC sulle bugne; 8.10 striscia dei partitori | **spariscono** |
| 8.11 vassoio sulle colonne | uguale (2.1.7) |
| 8.12 basetta sulle colonnine | SM con 6 viti: 4 sulle colonnine del vassoio, 2 sulle colonne delle ali |
| 8.17–8.21 2813, abilitazione, seriale, INA260, cavo piatto | uguali nei capi lontani |
| 8.22 prese dei piedi verso l'ADC; 8.23 prese delle luci; 8.24 NTC | si **innestano** le spine sulle ali (zampa, canale, colore della massa); nessuna saldatura |
| 8.25 controllo dei fili; 8.26 prove a freddo | più corti, sui punti di prova |

**Sezione 13, carapace**:

| Passi di oggi | Con la SM |
|---|---|
| 13.16 fili sulla scheda | sulle piazzole della SC con il nome in serigrafia, non più nelle righe della millefori |
| 13.17 scheda sulle bugne | uguale (bugne della 2.1.7) |
| 13.18 prova al banco senza corrente | sui punti di prova della SC |
| 13.19 spina IDC; 13.20 prova con la logica accesa | uguali |
| nuovo | modulo TCA9534 sulla presa Qwiic della SC, con i pull-up tagliati (S-13, S-17) |

Fuori dalle tre sezioni:
- 9.x e 10.x (zampa sul corpo): le spine di FSR e luci vanno sulle ali, raggiungibili a carapace tolto come oggi;
- 15 (smontaggio): per togliere il vassoio si staccano 12 spine e 2 NTC e si tolgono 2 viti in più;
- 90 (appendici): gli schemi delle millefori si sostituiscono con quelli della PCB.

## 9. Rischi

| Rischio | Effetto | Quanto è probabile | Contromisura |
|---|---|---|---|
| Impronte sbagliate: interasse dell'ESP32 (S-02), pin del D24V22F5 (S-03), testata Würth (S-26) | scheda da rifare | media: tre quote non lette sul pezzo | prova a secco dell'ESP32 (P-005); pagina Pololu; disegno Würth; **dima stampata** con i moduli veri prima dell'ordine (`produzione.md:250`) |
| Componenti sul retro dell'ESP32 più alti del previsto (S-08) | SMD o U2 toccano l'ESP32 | bassa con SMD, media con U2 a 7,2 su 8,5 | stessa prova a secco con la SM stampata 1:1; in Z1 solo parti basse |
| TSSOP-16 dell'ADC saldato a mano | ponti fra i pin, ADC muto | media al primo tentativo | flussante e treccia; schede di scorta (5 fabbricate); oppure montaggio JLCPCB (6.2) |
| Spine sulle ali: cima a z 24,5 vicino ai cavi dei servo (z 25) e al carapace (28,4) | fili piegati stretti, carapace che preme sulle spine | media | ingombro delle spine nella verifica del CAD (sezione 7, n. 4); se serve, spine con la parte femmina più corta o fila più bassa |
| Spine senza chiave | luce della tibia girata: circa 14 mA nell'uscita del buffer | bassa | serigrafia, colore della massa, prova al passo 8.23 |
| Una scheda sola per tutta la logica del corpo | un guasto o una pista bruciata fermano tutto; si cambia la scheda, non un modulo | bassa | 4 schede di scorta; ponticelli a saldare e punti di prova; ESP32 e U2 restano moduli |
| Rumore del D24V22F5 sull'ADC a 8 bit | letture dei piedi instabili | bassa (1 LSB = 12,9 mV a 3,3 V) | ADC lontano da U2, massa piena sotto, 100 nF per canale; si misura in P2 |
| Partitore della RX: R12 staccata | circa 0,12 mA nel diodo di protezione di GPIO14 | bassa | serigrafia e prova; in alternativa un 74LVC1G17 a 3,3 V |
| Antenna sopra il rame | portata Wi-Fi più corta | bassa | nessun rame per x ≥ 74; prova di portata in P2 |
| PTC caldo dopo lo scatto (oltre 100 °C) | danno al PLA vicino | bassa | sull'ala −Y, a più di 8 mm dall'ESP32, fuori dal vassoio |
| CAD: colonne delle ali vicino a colonnine del carapace e vassoio; ali vicino al servo di coxa | interferenze | media (margini di 1–2 mm, stimati) | verifica d'interferenza della versione nuova; se non ci sta, ali più corte e 6 posti con le NTC saldate |
| Più lavoro per togliere il vassoio | 12 spine, 2 NTC e 2 viti in più | certa, effetto piccolo | è anche il vantaggio: oggi le prese sono fili fissi verso striscia e basetta |
| Dati non letti: riferimento dell'ADS7830 (bit PD), soglie dell'AHCT125 | scelta sbagliata nel disegno | bassa | scheda TI riletta prima dello schema (R-20) |
| Dogana e prezzi | costo più alto | media | un solo ordine o pannello; Aisler (`produzione.md:259`) |

## 10. Tempi

| Fase | Chi | Durata [S] | Note |
|---|---|---|---|
| Dati mancanti (R-20): RE1.3 e prova a secco, disegno Würth, pin del D24V22F5, schede TI di ADS7830 e AHCT125 | utente e agente | 1–2 giorni di calendario | la prova a secco la fa l'utente |
| Scelte con l'utente (sezione 12) | utente | — | prima di disegnare |
| Versione del CAD (sezione 7) | agente, Fusion | 1–2 blocchi di lavoro | dopo la 2.1.7 o insieme |
| Schema e PCB in KiCad, ERC e DRC, STEP in Fusion | agente e utente | 2–4 blocchi | due schede; KiCad 10 da installare (`produzione.md:206`) |
| Dima 1:1 stampata e prova con i moduli veri | utente | 1 giorno | |
| Ordine e consegna | produttore | 1–3 settimane | `produzione.md:69-75` |
| Montaggio | utente | SM circa 2–3 ore, SC circa 1 ora | contro le 6–7 ore di saldature di oggi |
| **Totale** | | **circa 3–6 settimane di calendario** | il robot si può costruire intanto sulle millefori: le reti e i GPIO non cambiano, il firmware non se ne accorge |

## 11. Punteggio

Da 1 a 5, dove 5 è meglio. Per "impatto sul CAD", 5 vuol dire nessun cambio.

| Criterio | Punti | Perché |
|---|---|---|
| Semplicità per l'utente | **4** | spariscono fili, ponticelli e barre di massa; zampe e NTC si innestano; resta il TSSOP-16 se lo salda lui, e i fili verso 2813, seriale, bus e carapace |
| Affidabilità | **4** | circa 120 fili e ponticelli in meno, nessun filo nelle zone vietate, prese con un supporto vero; un punto singolo di guasto in più (una scheda per tutto) |
| Costo | **4** | 14–30 € netti in più tutto a mano, 27–36 € con gli SMD montati; i moduli che spariscono pagano metà delle parti nuove |
| Impatto sul CAD | **3** | ESP32, vassoio e quote verticali restano; cambiano base (2 colonne in più, bugne e sedi in meno), tacca del vassoio, componente di libreria; margini di 1–2 mm da verificare |
| Riparabilità | **3** | ESP32 e regolatore restano moduli; un chip guasto (buffer, ADC) si cambia solo con l'aria calda o si cambia la scheda (4 di scorta); i fili esterni sono saldati come oggi |
| Compatibilità con le predisposizioni X | **4** | X5, X6, X14 e X31 integrate; X3 con piazzole e J1; X1 e X20 trovano posto sulla SC; polo 14 per X25; X15, X18, X27, X29 e X33 si collegano alla presa Qwiic della SC. Nessun GPIO in più, come oggi. Un secondo ADS7830 per X32 si aggiungerebbe solo con un'impronta non montata, se c'è spazio |

## 12. Aperti e domande per l'utente

1. **Montaggio**: SMD saldati da te (TSSOP-16 compreso) o montati da JLCPCB? Decide la tabella 6.2 e se il buffer va in SOIC (`requisiti.md` sezione 4.3).
2. **Prese sulle ali**: cambiano il posto deciso in D-069 (prese sul tetto). Va bene innestare le spine dei piedi e delle luci sulla scheda?
3. **Kit di resistenze 0805**: voce nuova. In alternativa le monta JLCPCB (punto 1).
4. **Fili o connettori** per 2813, INA260 e carapace sulla SM: la proposta è fili saldati (meno componenti).
5. **Ordine dei lavori**: CAD della SM prima o dopo la 2.1.7. Se prima, la modifica 8 della 2.1.7 si salta.
6. Dati di R-20, invariati: prova a secco della RE1.3, codice e disegno della testata Würth, pin del D24V22F5. In più: la scheda TI dell'ADS7830 per il riferimento esterno.
