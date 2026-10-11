# Schemi della basetta e della scheda del carapace (F3b)

Fase F3b della guida di montaggio (D-075, `docs/piano-guida.md` riga 150). Proposta da approvare: niente è ancora saldato. Gli SVG sono generati da uno script (griglia, reti e fili in un solo posto) e qui sono elencati per intero.

| Disegno | Contenuto |
|---|---|
| `schemi/basetta.svg` | basetta dell'ESP32, lato componenti, scala 2:1 |
| `schemi/basetta_saldature.svg` | basetta, lato saldature (specchiata), fili numerati 1–48 |
| `schemi/scheda_carapace.svg` | scheda del carapace (X2), lato componenti, scala 3:1 |
| `schemi/scheda_carapace_saldature.svg` | scheda del carapace, lato saldature (specchiata), fili numerati 101–118 |

Convenzioni:
- **fori**: colonna-riga con il trattino (`R-11`), per non confonderli con le sigle dei componenti (`R7`). Colonne a lettere lungo X del robot (A verso la coda), righe a numeri lungo Y;
- **millefori**: la C2 del BOM è una 5 × 7 cm **a doppia faccia, una piazzola per foro** (`docs/BOM.md` riga 70): non ci sono strisce da tagliare. I collegamenti si fanno sul lato saldature con ponticelli di stagno o filo nudo fra fori vicini e con fili isolati (26 AWG, B17; 30 AWG avanzato di X31). Un filo del lato saldature si salda sulla saldatura del pin, non dentro il foro;
- **stato dei dati**: come nel resto del progetto, V verificato, S stimato, C da confermare sul pezzo. Le piedinature non verificate sono nei problemi (`guida/problemi/schemi.yaml`, S-01 … S-18);
- tutte le quote in mm nella terna del robot (X avanti, Y a sinistra).

Il disegno segue le fonti. Dove le fonti non bastano ho scelto la soluzione più prudente e l'ho scritta in "Scelte" con il perché. Le scelte che cambiano un passo già scritto della guida sono in fondo ("Cosa cambia nei passi").

## 1. Basetta dell'ESP32

Millefori C2 tagliata a **56 × 35** (x 22…78, |y| ≤ 17,5; D-053). Griglia di **21 colonne (A–U) × 13 righe**: colonna A a x 23,77 (il primo pin dell'ESP32), riga 1 a y +15,24 (lato sinistro del robot), riga 7 sull'asse. Il bordo di coda sta 1,8 mm dietro la colonna A, quello di testa 3,4 mm davanti alla U: la colonna oltre la U cade sul taglio e non si usa.

Vincoli che hanno deciso la disposizione (D-053, `cad/script/rif_componenti.py` righe 95–111, `guida/dati/fori.json`):
- **sopra la basetta c'è l'ESP32** a 8,5 mm (strip femmina), 6,6 mm sotto la sede della microSD (x 22,5…37,5, |y| ≤ 7, riquadro blu). Il circuito dell'ESP32 copre tutto tranne le righe 1 e 13: sono le sole piazzole raggiungibili con l'ESP32 inserito;
- **quattro colonnine** con viti M2 × 5 dall'alto a (29; ±6,8) e (75,5; ±6,5), fuori griglia: i fori Ø 2,2 si trapanano sul vassoio (D-053). Le piazzole a meno di 3 mm dal centro (sotto la testa Ø 3,8) non si usano (croci): B-4, C-4, C-5, D-4, D-5, B-10, C-9, C-10, D-9, D-10, U-4, U-5, U-9, U-10. Sopra le teste non c'è nessun corpo: le viti si stringono nel passo 8.11 con i componenti già saldati;
- **sotto la basetta** restano 3,3 mm (colonnine): solo saldature, fili adagiati e i due condensatori SMD.

### 1.1 Componenti

| Sigla | Cosa (voce del BOM) | Fori | Note |
|---|---|---|---|
| U1 | ESP32-S3-CAM UICPAL (A2) su due strip femmina 1 × 20 (C2) | strip in riga 2 e riga 12, colonne A–T. Pin 1 (3V3 e GPIO43) in colonna T, verso l'antenna | file a 25,4 mm (10 passi): il CAD dice 24,7 [C], problema S-02. Piedinatura dall'immagine dell'inserzione [S], S-15 |
| U2 | regolatore 5 V Pololu D24V22F5 (B2) | corpo colonne M–S, righe 4–10; pin in riga 4: N-4 PG, O-4 EN, P-4 VIN, Q-4 GND, R-4 VOUT | ordine dei pin [C] (S-03). Appoggiato su nastro isolante, alto 7,2; PG ed EN non collegati (EN ha 270 kΩ interni verso VIN, Pololu 2858) |
| U3 | buffer SN74AHCT125N in DIP-14 (X9) | pin 1–7 in E-8…K-8, pin 8–14 in K-11…E-11 (pin 1 in E-8, tacca verso la coda) | senza zoccolo: con lo zoccolo sarebbe 8 mm. Usato un solo canale (1A → 1Y), come in `cablaggio.md` riga 47 |
| U4 | traslatore C1, KAmod Level Shift x4 (15,7 × 10,7, due file da 6) | lato 5 V in E-4…J-4: HV, H1, H2, H3, H4, GND; lato 3,3 V in E-7…J-7: LV, L1, L2, L3, L4, GND | sigle e passo fra le file (7,62) [C], S-04. Sulle sue strip da 2,5 mm: sotto il modulo passano D2 e R3 |
| PTC1 | fusibile ripristinabile Bourns MF-R075 (X9) | reofori in L-8 e L-10 | sdraiato **sopra U3**, su nastro isolante: 5,1 + 3,0 = 8,1 mm su 8,5 [C] (S-08) |
| D1 | Schottky 1N5819 (C3) | catodo A-6, anodo D-6 | fra il 5 V del regolatore e il pin 5V dell'ESP32 (scelta 1, S-07) |
| D2 | 1N4148 (B11) | catodo F-5, anodo I-5 | abilitazione del rail: anodo a GPIO42 (`cablaggio.md` riga 31). Sotto U4 |
| R1 | 10 kΩ (X9) | B-3 – E-3 | pull-down di GPIO48 all'ingresso del buffer |
| R2 | 330 Ω (X9) | D-8 – A-8 | in serie al dato dei LED, verso il polo 4 e le tibie |
| R3 | 47 kΩ (B11; 22 kΩ se la prova lo chiede) | F-6 – J-6 | EN dei regolatori a massa. Sotto U4. Valore: S-05 |
| R4 | 4,7 kΩ (B10) | I-3 – L-3 | pull-up di SCL verso il 3,3 V dei sensori. Valore: S-13 |
| R5 | 4,7 kΩ (B10) | M-3 – Q-3 | pull-up di SDA |
| R6 | 100 kΩ 1 % (B10) | T-8 – T-11, sdraiata lungo la colonna T | partitore della batteria, lato alto |
| R7 | 47 kΩ 1 % (B10) | R-11 – N-11 | partitore, lato basso |
| CS1 | 100 nF SMD (B8) | fra R-11 e S-11, lato saldature | filtro di GPIO1 (`docs/BOM.md` riga 50) |
| CS2 | 100 nF SMD (kit di B8) | fra E-11 e F-11, lato saldature | disaccoppiamento di U3 (VCC–GND sui pin 14 e 13) |
| J1 | ponticello di filo, lato componenti | T-3 – S-3 | chiuso: i sensori prendono il 3,3 V dell'ESP32. Con X3 si toglie (S-12) |
| — | cavo piatto a 16 vie (X2) | poli 1–13 in C-13…O-13 | polo 14 tagliato; 15 e 16 non passano dalla basetta: vanno alla 2813 |

Non stanno sulla basetta: la 100 kΩ di GPIO41 (si salda sulla 2813, S-11) e il regolatore 3,3 V D24V5F3 (X3, solo se serve: fuori dalla basetta, S-12).

### 1.2 Reti (netlist)

Pin e fori di ogni rete. I fili e i ponticelli che le realizzano sono in 1.3. Fonti con file e riga (cartella `docs/`, salvo dove è scritto).

| Rete | Pin e fori | Fonte |
|---|---|---|
| VBAT | P-4 (U2 VIN); T-8 (R6); B-9 (filo: uscita della 2813) | cablaggio.md:32, :76 (2813 → D24V22F5 e partitore); BOM.md:52 (B10) |
| 5V_ESP | A-2 (ESP32 5V); A-6 (D1) | cablaggio.md:27 (D24V22F5 → pin 5V); diodo D1: scelta S-07, BOM.md:71 (C3) |
| 5V_LED | L-10 (PTC1); C-13 (filo: 1); D-13 (filo: 2); U-13 (filo: +5 V tibie) | cablaggio.md:28–29, :77 (PTC → poli 1-2 e tibie); predisposizioni.md:104 |
| 5V_REG | R-4 (U2 VOUT); E-11 (U3 14 VCC); E-4 (U4 HV); L-8 (PTC1); D-6 (D1); CS2 fra E-11 e F-11 (lato saldature) | cablaggio.md:27–30, :77; BOM.md:43 (B2); predisposizioni.md:109 |
| 3V3S | L-3 (R4); M-3 (R5); S-3 (filo: J1); L-1 (filo: 3V3); M-1 (filo: 3V3); N-1 (filo: 3V3); O-1 (filo: 3V3); I-13 (filo: 7); J1 (ponticello sul lato componenti) T-3–S-3, solo senza X3 | predisposizioni.md:108 (D24V5F3 o 3V3 della scheda); cablaggio.md:116, :139 (polo 7) |
| 3V3_ESP | T-2 (ESP32 3V3); E-7 (U4 LV); T-3 (filo: J1) | dimensioni-componenti.md:74 (pin 3V3); piano-elettronica-software.md:77 |
| GND | A-12 (ESP32 GND); Q-4 (U2 GND); E-8 (U3 1 1OE); H-8 (U3 4 2OE); I-8 (U3 5 2A); K-8 (U3 7 GND); J-11 (U3 9 3A); I-11 (U3 10 3OE); G-11 (U3 12 4A); F-11 (U3 13 4OE); J-4 (U4 GND); J-7 (U4 GND); E-3 (R1); J-6 (R3); N-11 (R7); S-11 (CS1); A-3 (filo: massa: 2813 e SSC-32 (2 fili)); B-1 (filo: GND); C-1 (filo: GND); D-1 (filo: GND); E-1 (filo: GND); E-13 (filo: 3); G-13 (filo: 5); K-13 (filo: 9); S-13 (filo: massa tibie) | predisposizioni.md:110 (le masse tornano alla basetta); cablaggio.md:137–140 (poli 3, 5, 9) |
| SCL | I-2 (ESP32 GPIO3); I-3 (R4); G-1 (filo: SCL); H-1 (filo: SCL); I-1 (filo: SCL); J-1 (filo: SCL); H-13 (filo: 6) | piano-elettronica-software.md:88 (GPIO3); cablaggio.md:42, :116, :138 (polo 6) |
| SDA | E-12 (ESP32 GPIO47); Q-3 (R5); Q-1 (filo: SDA); R-1 (filo: SDA); S-1 (filo: SDA); T-1 (filo: SDA); J-13 (filo: 8) | piano-elettronica-software.md:101 (GPIO47); cablaggio.md:42, :116, :139 (polo 8); pull-up :133 |
| DATA | A-8 (R2); F-13 (filo: 4); T-13 (filo: dato tibie) | cablaggio.md:47–48, :137 (polo 4); cablaggio.md:108 (luci delle tibie) |
| RX5 | G-4 (U4 H2); A-4 (filo: TX della SSC-32 (Dupont)) | cablaggio.md:41 (TX della SSC-32 → traslatore); 08-elettronica.yaml 8.20 |
| TX5 | F-4 (U4 H1); A-5 (filo: RX della SSC-32 (Dupont)) | cablaggio.md:41 (traslatore → RX della SSC-32); 08-elettronica.yaml 8.20 |
| Y1 | G-8 (U3 3 1Y); D-8 (R2) | cablaggio.md:47 (uscita del buffer → 330 Ω) |
| AMP | Q-12 (ESP32 GPIO2); O-13 (filo: 13) | cablaggio.md:49, :142 (polo 13); piano-elettronica-software.md:87 (GPIO2) |
| BCLK | L-12 (ESP32 GPIO38); L-13 (filo: 10) | cablaggio.md:49, :140 (polo 10); piano-elettronica-software.md:95 (GPIO38) |
| LED_IN | F-12 (ESP32 GPIO48); F-8 (U3 2 1A); B-3 (R1) | cablaggio.md:47 (GPIO48, 10 kΩ a massa, ingresso del buffer); piano-elettronica-software.md:102 |
| MIC | N-12 (ESP32 GPIO40); N-13 (filo: 12) | cablaggio.md:49, :141 (polo 12); piano-elettronica-software.md:97 (GPIO40) |
| RX3 | B-2 (ESP32 GPIO14); G-7 (U4 L2) | cablaggio.md:41, :160; piano-elettronica-software.md:91 (GPIO14) |
| TX3 | D-12 (ESP32 GPIO21); F-7 (U4 L1) | cablaggio.md:41, :160; piano-elettronica-software.md:93 (GPIO21); BOM.md:69 (C1) |
| WS | M-12 (ESP32 GPIO39); M-13 (filo: 11) | cablaggio.md:49, :141 (polo 11); piano-elettronica-software.md:96 (GPIO39) |
| EN | F-5 (D2); F-6 (R3); A-10 (filo: EN dei due D42V110F6 (2 fili)) | cablaggio.md:31, :78 (1N4148, 47 kΩ a massa); BOM.md:53 (B11) |
| GPIO42 | P-12 (ESP32 GPIO42); I-5 (D2) | cablaggio.md:31, :78; piano-elettronica-software.md:99; firmware/main/main.cpp:14 |
| OFF | O-12 (ESP32 GPIO41); A-11 (filo: OFF della 2813) | cablaggio.md:32, :79; piano-elettronica-software.md:98 (GPIO41) |
| SENSE | R-12 (ESP32 GPIO1); T-11 (R6); R-11 (R7); CS1 fra R-11 e S-11 (lato saldature) | cablaggio.md:32 (partitore 100 k / 47 k → GPIO1); BOM.md:50 (B8), :52 (B10); piano-elettronica-software.md:86 |

Pin dell'ESP32 usati (riga 2, da coda a testa: 5V, 14, 13, 12, 11, 10, 9, 46, 3, 8, 18, 17, 16, 15, 7, 6, 5, 4, RST, 3V3; riga 12: GND, 19, 20, 21, 47, 48, 45, 0, 35, 36, 37, 38, 39, 40, 41, 42, 2, 1, 44, 43; `docs/dimensioni-componenti.md` righe 70–93 [S]): A-2 5V, B-2 GPIO14, I-2 GPIO3, T-2 3V3, A-12 GND, D-12 GPIO21, E-12 GPIO47, F-12 GPIO48, L-12 GPIO38, M-12 GPIO39, N-12 GPIO40, O-12 GPIO41, P-12 GPIO42, Q-12 GPIO2, R-12 GPIO1. Gli altri restano liberi (camera, PSRAM, USB, strapping).

Verifiche fatte sullo schema (script del progettista, non nella repo): nessun foro usato da due componenti, nessun pin su un foro sotto le viti, nessuna piazzola di VBAT accanto ad altre reti, nessuna piazzola di 5 V accanto a una di 3,3 V. Restano vicine a pin dell'ESP32 le piazzole a 5 V C-13, D-13 (+5 V LED), F-13, T-13 (dato dei LED) ed E-11 (VCC di U3): la prova 5 di 1.5 le controlla una per una (S-09).

### 1.3 Ponticelli e fili del lato saldature

Ponticelli (stagno o filo nudo fra fori vicini): L-3–M-3 (3V3S), L-1–M-1 (3V3S), M-1–N-1 (3V3S), N-1–O-1 (3V3S), T-2–T-3 (3V3_ESP), D-13–C-13 (5V_LED), L-12–L-13 (BCLK), F-5–F-6 (EN), G-11–F-11 (GND), I-11–J-11 (GND), I-8–H-8 (GND), J-7–J-6 (GND), E-1–D-1 (GND), D-1–C-1 (GND), C-1–B-1 (GND), N-12–N-13 (MIC), I-2–I-3 (SCL), I-2–I-1 (SCL), I-1–H-1 (SCL), I-1–J-1 (SCL), H-1–G-1 (SCL), Q-1–R-1 (SDA), R-1–S-1 (SDA), S-1–T-1 (SDA), R-12–R-11 (SENSE), M-12–M-13 (WS).

Fili isolati, numerati come in `basetta_saldature.svg` (anche in fondo al disegno). Si saldano sulla saldatura dei pin, adagiati: VBAT (1, 2) da solo, senza toccare altri fili nudi.

| N. | Da | A | Rete |
|---|---|---|---|
| 1 | P-4 | T-8 | VBAT |
| 2 | P-4 | B-9 | VBAT |
| 3 | A-2 | A-6 | 5V_ESP |
| 4 | L-10 | D-13 | 5V_LED |
| 5 | L-10 | U-13 | 5V_LED |
| 6 | R-4 | L-8 | 5V_REG |
| 7 | L-8 | E-11 | 5V_REG |
| 8 | E-11 | D-6 | 5V_REG |
| 9 | D-6 | E-4 | 5V_REG |
| 10 | L-3 | L-1 | 3V3S |
| 11 | O-1 | S-3 | 3V3S |
| 12 | L-3 | I-13 | 3V3S |
| 13 | T-3 | E-7 | 3V3_ESP |
| 14 | A-12 | E-13 | GND |
| 15 | E-13 | G-13 | GND |
| 16 | G-13 | G-11 | GND |
| 17 | G-11 | I-11 | GND |
| 18 | J-11 | K-13 | GND |
| 19 | I-11 | I-8 | GND |
| 20 | I-8 | J-7 | GND |
| 21 | J-7 | K-8 | GND |
| 22 | J-6 | J-4 | GND |
| 23 | H-8 | E-8 | GND |
| 24 | K-13 | N-11 | GND |
| 25 | N-11 | S-11 | GND |
| 26 | S-11 | S-13 | GND |
| 27 | E-8 | E-3 | GND |
| 28 | E-3 | E-1 | GND |
| 29 | B-1 | A-3 | GND |
| 30 | J-4 | Q-4 | GND |
| 31 | I-3 | H-13 | SCL |
| 32 | E-12 | J-13 | SDA |
| 33 | J-13 | Q-3 | SDA |
| 34 | Q-3 | Q-1 | SDA |
| 35 | A-8 | F-13 | DATA |
| 36 | F-13 | T-13 | DATA |
| 37 | G-4 | A-4 | RX5 |
| 38 | F-4 | A-5 | TX5 |
| 39 | G-8 | D-8 | Y1 |
| 40 | Q-12 | O-13 | AMP |
| 41 | F-12 | F-8 | LED_IN |
| 42 | F-8 | B-3 | LED_IN |
| 43 | B-2 | G-7 | RX3 |
| 44 | D-12 | F-7 | TX3 |
| 45 | F-6 | A-10 | EN |
| 46 | P-12 | I-5 | GPIO42 |
| 47 | O-12 | A-11 | OFF |
| 48 | R-11 | T-11 | SENSE |

### 1.4 Ordine di saldatura (dal più basso al più alto)

Al banco (sezione 4), ESP32 fuori, prima di avvitare la basetta. Un componente alla volta, poi continuità.

1. Taglia la millefori a 56 × 35 come sopra; trapana i quattro fori Ø 2,2 usando il vassoio come dima (D-053). Pulisci le piazzole con alcol.
2. Lato componenti, sotto U4: D2 (fascia verso F-5) e R3. Sono alti 1,9 e 2,3: sotto il modulo restano 2,5 mm.
3. Resistenze sdraiate: R1, R2, R4, R5, R6, R7; poi D1 (Ø 2,7, fascia verso A-6).
4. U3 (pin 1 in E-8, tacca verso la coda), saldato senza zoccolo.
5. U4 sulle sue strip, lato 5 V (HV) in riga 4 [C: controlla le sigle prima, S-04].
6. U2 su un quadrato di nastro isolante, con i pin (o spezzoni di reoforo) nei fori di riga 4 [C: ordine dei pin, S-03].
7. PTC1: nastro isolante sopra U3, PTC sdraiato, reofori piegati in L-8 e L-10.
8. Strip femmina dell'ESP32: infilale sui pin dell'ESP32, appoggia l'insieme, salda i due pin d'angolo di ogni strip, controlla che siano dritte, poi tutti gli altri; togli l'ESP32.
9. Lato saldature: ponticelli, poi i fili 1–48 in ordine (prima VBAT, poi 5 V, 3,3 V, massa, bus, segnali), poi CS1 e CS2.
10. J1 sul lato componenti (senza X3).
11. Fili verso il resto del robot (1.6): fili dal retro, cavo piatto, tibie. Fascetta del cavo piatto sul bordo della basetta.
12. Prove di 1.5, ancora senza ESP32.

### 1.5 Prove con il multimetro, prima di alimentare

ESP32 fuori dagli strip, nessun filo esterno collegato a batteria o regolatori. Per i pin dell'ESP32 si mette il puntale nella presa della strip.

| N. | Punto | Atteso | Se no |
|---|---|---|---|
| 1 | VBAT (B-9) contro massa (A-3) | sale, poi resta sopra 10 kΩ (circa 147 kΩ dal partitore, meno l'ingresso di U2) [S] | corto sul 26 AWG della batteria: F2 salterebbe |
| 2 | VBAT (B-9) contro 5V_REG (R-4), contro 3V3 (T-2), contro ogni pin delle righe 2 e 12 | aperto (oltre 100 kΩ) | ponte di stagno: la batteria arriverebbe all'ESP32 |
| 3 | 5V_REG (R-4) contro massa | non 0 Ω; sale (condensatori di U2) [S] | corto sul 5 V |
| 4 | 5V_REG (R-4) contro 3V3 (T-2) | non 0 Ω, oltre 1 kΩ [S] | ponte fra 5 V e 3,3 V: brucia l'ESP32 e i sensori |
| 5 | 5V_REG, 5V_LED (C-13) e DATA (F-13) contro ogni pin delle righe 2 e 12, in particolare C-13/C-12, D-13/D-12, F-13/F-12, T-13/T-12, E-11/E-12 | aperto, salvo A-2 (vedi 6) e A-12 (massa, vedi 3) | ponte fra un 5 V e un GPIO |
| 6 | D1, prova diodi: puntale rosso su D-6, nero su A-2 | 0,15–0,35 V [S]; invertiti: OL | D1 al contrario o in corto |
| 7 | 5V_LED (C-13) contro 5V_REG (R-4) | sotto 1 Ω (PTC freddo) [S] | PTC non saldato |
| 8 | C-13 contro D-13 e contro U-13 | 0 Ω | |
| 9 | 3V3S (S-3) contro 3V3 (T-2) | 0 Ω con J1; aperto senza | |
| 10 | SDA (Q-1) contro 3V3S (S-3); SCL (G-1) contro 3V3S | 4,7 kΩ ciascuno (solo R4 e R5: moduli non collegati) | |
| 11 | SDA contro SCL | circa 9,4 kΩ (le due pull-up in serie) | ponte fra SDA e SCL |
| 12 | EN (A-10) contro massa | 47 kΩ (o 22 kΩ, S-05) | |
| 13 | EN (A-10) contro ogni rete di alimentazione (B-9, R-4, C-13, T-2) | aperto | un ponte accenderebbe il rail dei servo |
| 14 | D2, prova diodi: rosso su I-5, nero su F-5 | 0,5–0,7 V; invertiti: OL | |
| 15 | GPIO1 (R-12) contro massa | circa 47 kΩ [S] | |
| 16 | GPIO48 (F-12) contro massa | 10 kΩ | |
| 17 | OFF (A-11) contro massa | aperto (la 100 kΩ sta sulla 2813) | |
| 18 | ogni filo della tabella 1.3 e ogni polo del cavo piatto, dal suo capo al pin dell'ESP32 | 0 Ω | |
| 19 | massa: A-3, A-12, Q-4, K-8, E-13, S-13, B-1 fra loro | 0 Ω | |

Con tutte le righe giuste: ESP32 negli strip, USB staccata, e si passa al ramo logica (passo 4.07–4.08). La prima tensione si misura su R-4 (5,0 V), su A-2 (circa 4,6–4,8 V dopo D1) e su T-2 (3,3 V).

### 1.6 Collegamenti verso il resto del robot

| Fori | Rete | Va a | Filo e connettore | Fonte |
|---|---|---|---|---|
| B-9 | VBAT | uscita della 2813 | 26 AWG rosso (B17), saldato ai due capi; da solo nel foro (con X3: anche il VIN di X3) | `cablaggio.md` 76 |
| A-3 | massa | massa della 2813 e GND della SSC-32 | due fili 26 AWG neri nello stesso foro; verso la SSC-32 con Dupont femmina (C4) | `cablaggio.md` 76, 160 |
| A-5 | TX5 (uscita H1 del traslatore) | pin RX della SSC-32 | 26 AWG con Dupont femmina | `cablaggio.md` 41, 160 |
| A-4 | RX5 (ingresso H2) | pin TX della SSC-32 | 26 AWG con Dupont femmina | idem |
| A-10 | EN | pad EN del D42V110F6 sinistro e del destro | due fili 26 AWG nello stesso foro | `cablaggio.md` 78 |
| A-11 | OFF | pin OFF della 2813; sulla 2813 una 100 kΩ fra OFF e massa | 26 AWG | `cablaggio.md` 79 |
| riga 1, gruppi B–E (massa), G–J (SCL), L–O (3,3 V), Q–T (SDA) | bus I2C0 | ramo 1 INA260 S: B-1, G-1, L-1, Q-1; ramo 2 INA260 D: C-1, H-1, M-1, R-1; ramo 3 ADC e IMU: D-1, I-1, N-1, S-1 (due fili per foro); ramo 4 ToF frontale: E-1, J-1, O-1, T-1 | cavetti Qwiic tagliati (nero massa, rosso 3,3 V, blu SDA, giallo SCL) e i 4 fili di IMU e ToF | `cablaggio.md` 116–124 |
| C-13…O-13 | poli 1–13 | scheda del carapace, spina IDC | cavo piatto 16 vie, 15 cm [S], filo rosso = polo 1; conduttori separati per 25 mm e aperti a ventaglio | `cablaggio.md` 132–143 |
| — | poli 15 e 16 | pin A e B della 2813 | separati dal cavo piatto per 10 cm e giuntati a due fili 26 AWG (stagno e guaina) | `cablaggio.md` 80 |
| S-13, T-13, U-13 | massa, dato, +5 V dei LED | prese delle luci delle tibie (polo marrone, arancio, rosso) | tre fili 26 AWG, saldati al banco e lunghi fino alle prese [S] | `cablaggio.md` 108; passo 8.25 |

Piedinatura del cavo piatto: 1–2 +5 V (dopo PTC1), 3 massa, 4 dato dei LED a 5 V, 5 massa, 6 SCL, 7 +3,3 V sensori, 8 SDA, 9 massa, 10 BCLK, 11 WS, 12 dati dei microfoni, 13 dati verso l'amplificatore, 14 riserva, 15–16 pulsante (`cablaggio.md` righe 132–143 [V]).

### 1.7 Scelte e perché

1. **Diodo D1 (1N5819) fra il 5 V e il pin 5V dell'ESP32.** Non è nei documenti: è l'alternativa del BOM C3 messa sempre. Senza, con la sola USB collegata, la USB potrebbe alimentare all'indietro il 5 V dei LED, il regolatore e il ramo della batteria (non sappiamo se la scheda ha un diodo, `guida/problemi/banco.yaml`). Costo: 0,3–0,45 V di caduta. Problema S-07.
2. **Un solo canale del buffer, un solo 330 Ω**, per polo 4 e tibie insieme, come `cablaggio.md` riga 47. Un secondo canale per le tibie sarebbe stato più robusto ma non c'è posto.
3. **Un solo PTC** a monte di poli 1–2 e tibie, come `cablaggio.md` riga 77: così la corrente d'intervento (1,5 A) più l'ESP32 resta sotto i 2,5 A del D24V22F5 (`predisposizioni.md` riga 104). L'amplificatore sta dopo il PTC perché prende il 5 V dai poli 1–2 (S-06).
4. **Pull-up 4,7 kΩ** su SDA e SCL: con le tre schede Adafruit (3,3 kΩ) e i pull-up di GY-6500 e ToF (10 kΩ ciascuno, S) l'equivalente viene circa 1,2 kΩ, dentro 1,0–1,4 (`piano-elettronica-software.md` riga 133). Si misura al passo 8.28 (S-13).
5. **100 kΩ di GPIO41 montata sempre**, sulla 2813 e non sulla basetta (manca il posto): il pin OFF scatta sopra 1 V (Pololu 2813) e GPIO41 flotta durante il reset (S-11).
6. **R3 47 kΩ** come B11, con la nota che con due regolatori in parallelo l'EN sale a 0,72 V: la prova 4.12 va fatta con i due regolatori insieme (S-05).
7. **Fili esterni saldati al banco** e fatti uscire dal bordo di coda (righe 3–11 della colonna A): sotto l'ESP32 non si salda più e nelle righe 1 e 13 le piazzole stanno accanto ai pin dell'ESP32. Nel robot (sezione 8) si salda l'altro capo, sulla 2813, sui regolatori e sulla SSC-32. Solo il bus della riga 1 (3,3 V) si salda anche nel robot.
8. **Seriale verso la SSC-32 con tre fili e Dupont**, non con un connettore sulla basetta: un connettore in piedi non sta sotto l'ESP32. VL arriva dalla 2813 ai morsetti (passo 8.18).
9. **VBAT su un foro isolato** (B-9: intorno solo fori vuoti e sotto le viti), un filo solo sul lato saldature fino a U2 e a R6.
10. **3,3 V dei sensori con un ponticello** (J1): senza X3 dal pin 3V3 dell'ESP32, con X3 dal D24V5F3; mai i due insieme.


## 2. Scheda del carapace (X2)

Striscia di millefori (avanzo della C2, doppia faccia) di **20 × 30**, appesa al dorso davanti all'ottagono: x 29,5…49,5, |y| ≤ 15, faccia alta a z 30,9 sulle quattro bugne (`guida/dati/fori.json`, `ins_sch_a…d` a (32; ±12,5) e (47; ±12,5); `cad/script/rif_componenti.py` righe 184–186). Il lato componenti guarda in basso (verso l'ESP32), il lato saldature guarda il dorso (3,5 mm d'aria).

Griglia di **7 colonne (A–G) × 11 righe**: colonna A a x 31,88 (lato ottagono), riga 1 a y +12,7. I quattro fori delle viti cadono sui fori d'angolo A-1, G-1, A-11, G-11 (spostati di 0,1–0,2 mm dal CAD): si allargano a Ø 2,4. Le otto piazzole accanto (B-1, A-2, F-1, G-2, A-10, B-11, F-11, G-10) toccano la testa della vite: si usano solo per la massa (A-2, G-2) o restano vuote.

**Bloccante (S-01).** La testata 2 × 8 dritta del BOM (X2) con la spina IDC innestata scende di 16–18 mm sotto la scheda (`predisposizioni.md` riga 72: circa 9 + 9 mm); sopra l'ESP32 ne restano circa 10 (il CAD dà 9 mm alla scheda con la spina, S). Una testata a 90° con la spina verso l'ottagono non va meglio: la scatola (27,9 mm) e la spina coprono le due viti di coda e quasi tutta la scheda. Lo schema qui sotto vale per i collegamenti; la posizione della testata va decisa con il CAD (2.1.7) prima di saldare.

### 2.1 Componenti

| Sigla | Cosa (voce del BOM) | Fori | Note |
|---|---|---|---|
| J2 | testata 2 × 8 con chiave, passo 2,54 (X2, Würth 61201623021) | poli dispari in colonna D, pari in colonna E, righe 2–9: polo 1 in D-2, polo 2 in E-2 … polo 15 in D-9, polo 16 in E-9 | tacca della scatola sul lato della colonna E [C]: il triangolo del polo 1 della spina IDC va verso D-2. Bloccante S-01 |
| CE1 | elettrolitico 470 µF 10 V (X2) | + in A-9, − in B-9 | sdraiato verso la riga 5, Ø ≤ 6,3 [C] (S-18) |
| R8 | 100 kΩ (B10, D-074) | G-6 – G-9, **sul lato saldature**, con guaina | pull-down della linea dati dei microfoni (S-18) |

### 2.2 Reti (netlist)

| Rete | Pin e fori | Fonte |
|---|---|---|
| 5V | D-2 (polo 1); E-2 (polo 2); A-9 (filo: +5 V catena LED; + di CE1); G-8 (filo: VIN dell’ampli); CE1 + | cablaggio.md:136 (poli 1-2), :147 (catena LED), :151 (ampli); predisposizioni.md:66 (470 µF) |
| 3V3 | D-5 (polo 7); B-2 (filo: +3,3 V ToF e Qwiic (2 fili)); G-3 (filo: +3,3 V microfoni) | cablaggio.md:139 (polo 7), :150 (microfoni), :153, :154 |
| GND | D-3 (polo 3); D-4 (polo 5); D-6 (polo 9); A-2 (filo: GND ToF e Qwiic (2 fili)); B-9 (filo: massa catena LED; − di CE1); G-2 (filo: massa microfoni e ampli (2 fili)); G-9 (filo: R8 verso massa); R8; CE1 − | cablaggio.md:137–140 (poli 3, 5, 9), :147–153 |
| SCL | E-4 (polo 6); B-3 (filo: SCL ToF e Qwiic (2 fili)) | cablaggio.md:138 (polo 6), :153 (ToF posteriore), :154 (Qwiic) |
| SDA | E-5 (polo 8); A-3 (filo: SDA ToF e Qwiic (2 fili)) | cablaggio.md:139 (polo 8), :153, :154 |
| DATA | E-3 (polo 4); B-10 (filo: DIN catena LED) | cablaggio.md:137 (polo 4), :147 (catena: anello, lobi) |
| AMP | D-8 (polo 13); G-7 (filo: DIN dell’ampli) | cablaggio.md:142 (polo 13), :151 |
| BCLK | E-6 (polo 10); G-4 (filo: BCLK microfoni e ampli (2 fili)) | cablaggio.md:140 (polo 10), :150, :151 |
| MIC | E-7 (polo 12); G-6 (filo: SD dei microfoni; R8); R8 100 kΩ fra G-6 e G-9 (lato saldature) | cablaggio.md:141 (polo 12), :150 (dati uniti, pull-down 100 kΩ); decisioni.md:639 (D-074) |
| WS | D-7 (polo 11); G-5 (filo: WS/LRC microfoni e ampli (2 fili)) | cablaggio.md:141 (polo 11), :150, :151 |
| BTN_A | D-9 (polo 15); A-4 (filo: pulsante, contatto 1) | cablaggio.md:143 (polo 15), :149; BOM.md:45 (B3b) |
| BTN_B | E-9 (polo 16); B-4 (filo: pulsante, contatto 2) | cablaggio.md:143 (polo 16), :149; BOM.md:45 (B3b) |

Il polo 14 (riserva) non è collegato. Il polo 4 porta il dato già a 5 V e dopo il 330 Ω (buffer sulla basetta, `predisposizioni.md` riga 148).

### 2.3 Ponticelli e fili del lato saldature

Ponticelli: D-2–E-2 (5V), D-3–D-4 (GND). Fili isolati 101–118 (anche nel disegno):

| N. | Da | A | Rete |
|---|---|---|---|
| 101 | D-2 | A-9 | 5V |
| 102 | E-2 | G-8 | 5V |
| 103 | D-5 | G-3 | 3V3 |
| 104 | D-5 | B-2 | 3V3 |
| 105 | D-4 | D-6 | GND |
| 106 | D-3 | G-2 | GND |
| 107 | D-3 | A-2 | GND |
| 108 | D-6 | B-9 | GND |
| 109 | D-6 | G-9 | GND |
| 110 | E-4 | B-3 | SCL |
| 111 | E-5 | A-3 | SDA |
| 112 | E-3 | B-10 | DATA |
| 113 | D-8 | G-7 | AMP |
| 114 | E-6 | G-4 | BCLK |
| 115 | E-7 | G-6 | MIC |
| 116 | D-7 | G-5 | WS |
| 117 | D-9 | A-4 | BTN_A |
| 118 | E-9 | B-4 | BTN_B |

### 2.4 Piazzole dei moduli

| Foro | Rete | Fili dei moduli |
|---|---|---|
| A-2 | massa | ToF posteriore e cavo Qwiic (2 fili) |
| B-2 | +3,3 V | ToF posteriore (VIN a 3,3 V) e cavo Qwiic |
| A-3 | SDA | ToF posteriore e cavo Qwiic |
| B-3 | SCL | ToF posteriore e cavo Qwiic |
| A-4, B-4 | pulsante | i due contatti del pulsante da 12 mm (B3b), 26 AWG circa 9 cm |
| A-9 | +5 V | catena LED (anello, poi lobi), 30 AWG; + di CE1 |
| B-9 | massa | catena LED; − di CE1 |
| B-10 | dato dei LED | DIN del primo pixel dell'anello |
| G-2 | massa | microfoni (un filo, vedi sotto) e amplificatore |
| G-3 | +3,3 V | microfoni |
| G-4 | BCLK | microfoni (SCK) e amplificatore (BCLK) |
| G-5 | WS | microfoni (WS) e amplificatore (LRC) |
| G-6 | dati dei microfoni | SD dei due microfoni; R8 |
| G-7 | dati verso l'ampli | DIN dell'amplificatore |
| G-8 | +5 V | VIN dell'amplificatore |
| G-9 | massa | R8 |

- **Microfoni**: i due MS3625 si collegano fra loro (VDD, GND, SCK, WS, SD in parallelo, fili corti), e un solo gruppo di cinque fili arriva a G-2…G-6: così ogni foro ha al più due fili. L/R a massa su quello sinistro e a 3,3 V sul destro, sul microfono (`cablaggio.md` riga 150).
- **Amplificatore** MAX98357A: GAIN e SD non collegati (guadagno e canale di fabbrica) [S].
- **ToF posteriore** (X19): l'XSHUT va direttamente a un I/O dell'espansore TCA9534 (X20), non alla scheda (`cablaggio.md` riga 153).
- **Presa Qwiic** (`predisposizioni.md` riga 75): un connettore SMD da 1 mm non si salda sulla millefori. Si usa un cavo Qwiic tagliato a metà (X1, Adafruit 4210): i quattro fili vanno in A-2, B-2, A-3, B-3 e la spina resta libera, raggiungibile dall'ottagono. L'espansore SparkFun (X20) si innesta lì e porta una seconda presa Qwiic per i moduli futuri (S-17).

### 2.5 Ordine di saldatura

1. Taglia l'avanzo a 20 × 30 con le righe e le colonne di sopra; allarga a Ø 2,4 i quattro fori d'angolo.
2. CE1 sdraiato (lato componenti), + in A-9.
3. J2 (dopo la decisione di S-01), tacca verso la colonna E.
4. Lato saldature: ponticelli D-2–E-2 e D-3–D-4, poi i fili 101–118, poi R8 con la guaina.
5. Fili dei moduli (13.16), dal lato componenti, uno alla volta con la prova di continuità.

### 2.6 Prove con il multimetro, prima di collegare la spina

| N. | Punto | Atteso | Se no |
|---|---|---|---|
| 1 | polo 1 (D-2) contro polo 3 (D-3) | non 0 Ω; sale mentre CE1 si carica | corto sul 5 V: brucia PTC1 e scalda il regolatore |
| 2 | polo 7 (D-5) contro poli 3, 5, 9 | non 0 Ω | corto sul 3,3 V dei sensori |
| 3 | polo 1 contro polo 7 | aperto | 5 V sul 3,3 V: brucia i sensori e l'ESP32 |
| 4 | poli 1 e 4 (5 V, dato) contro poli 6, 8, 10, 11, 12, 13 | aperto | 5 V su un GPIO |
| 5 | poli 15 e 16 contro tutti gli altri | aperto; fra loro: aperto a riposo, chiuso a pulsante premuto | pulsante normalmente chiuso o filo sbagliato |
| 6 | polo 12 (E-7) contro massa | 100 kΩ (R8) | |
| 7 | polo 14 (E-8) contro tutti | aperto | |
| 8 | ogni filo 101–118 dal polo alla piazzola, e ogni piazzola al pin del suo modulo | 0 Ω | |

### 2.7 Scelte e perché

1. **Testata con chiave** come nel BOM, non un pin header senza scatola: girata di 180° la spina porterebbe il +5 V dei poli 1–2 sui poli 15–16 (pulsante della 2813).
2. **Fili dei moduli a due per foro**: la scheda ha 77 fori, di cui 16 per la testata e una decina sotto CE1; i microfoni si uniscono fra loro e il ToF condivide i fori con il cavo Qwiic.
3. **R8 sul lato saldature**: sul lato componenti non c'è un posto libero lungo tre passi fuori dalla testata.
4. **Pulsante lontano dal 5 V**: A-4 e B-4 confinano con SDA, SCL e con fori vuoti. Con la tensione dei pin A e B della 2813 ignota (S-10) si controlla prima di collegare.
5. **CE1 sul +5 V dopo il PTC**, come `predisposizioni.md` riga 66: smorza i picchi della catena LED vicino alla catena.


## 3. Cosa cambia nei passi già scritti

Da riportare nei passi (F3c), con il riferimento a questi disegni (`figura: schemi/basetta.svg` e gli altri):

| Passo | Oggi | Con lo schema |
|---|---|---|
| 4.04 | strip a 24,7 mm [C]; "connettore a 3 poli" per la seriale; 100 kΩ su GPIO41 sulla basetta | strip a 25,4 mm (10 passi) dopo la misura di S-02; seriale con tre fili e Dupont (A-3, A-4, A-5); la 100 kΩ si salda sulla 2813 (8.19) |
| 4.05 | buffer e PTC senza posto; pull-up senza valore | U3, PTC1 sopra U3, R4 e R5 da 4,7 kΩ; fili delle tibie saldati qui (S-13, T-13, U-13) |
| 4.06 | disposizione assente | `scheda_carapace.svg`, dopo S-01 |
| 4.12 | prova con un regolatore | prova con i due regolatori in parallelo (S-05) |
| 8.18 | due fili 26 AWG dalla 2813 alla basetta, saldati sulla basetta | i fili sono già sulla basetta (B-9, A-3): si saldano sulla 2813 |
| 8.19 | EN e OFF saldati sulla basetta | EN (A-10) e OFF (A-11) già sulla basetta: si saldano sui regolatori e sulla 2813, con la 100 kΩ fra OFF e massa della 2813 |
| 8.20 | tre fili saldati sul "connettore di prova" | i tre fili (A-3, A-4, A-5) sono già sulla basetta: si infilano le Dupont |
| 8.21, 8.22 | "ramo del bus della basetta" | riga 1: un ramo per foro di ogni gruppo (1.6); IMU e ADC nello stesso foro |
| 8.23 | poli 15–16 sulla basetta | poli 15–16 separati dal cavo e giuntati ai fili verso A e B della 2813 |
| 8.25 | tre fili dalla basetta alle prese delle luci, saldati sulla basetta nel robot | già saldati al banco: si saldano sulle prese |
| 8.28 | SDA e SCL contro 3,3 V: 1,0–1,4 kΩ | valore atteso con tutti i moduli (S-13); prima, a basetta sola, 4,7 kΩ (prova 10 di 1.5) |
| 13.16 | 5 fili per microfono, presa Qwiic | microfoni uniti fra loro; cavo Qwiic tagliato in A-2…B-3; tabella 2.4 |
