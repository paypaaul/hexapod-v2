# Schemi della basetta e della scheda del carapace (F3b)

Fase F3b della guida di montaggio (D-075, `docs/piano-guida.md` riga 150). Proposta da approvare: niente è ancora saldato. Seconda versione, rifatta dopo la verifica elettrica del 12 ottobre 2026: i rilievi applicati sono elencati in fondo (sezione 4), quelli non applicati con il perché nella sezione 5. Gli SVG sono generati da uno script (griglia, reti, zone vietate, instradamento dei fili e controlli in un solo posto) e qui sono elencati per intero.

| Disegno | Contenuto |
|---|---|
| `schemi/basetta.svg` | basetta dell'ESP32, lato componenti, scala 2:1: componenti, pin, fili esterni, teste M3 e colonnine |
| `schemi/basetta_saldature.svg` | basetta, lato saldature (specchiata): zone vietate, ponticelli, fili numerati 1–37 con la sezione, filo della batteria |
| `schemi/scheda_carapace.svg` | scheda del carapace (X2), lato componenti, scala 3:1 |
| `schemi/scheda_carapace_saldature.svg` | scheda del carapace, lato saldature (specchiata): zone delle bugne, fili numerati 101–112, fili dei moduli saldati sui pin |

Convenzioni:
- **fori**: colonna-riga con il trattino (`R-11`), per non confonderli con le sigle dei componenti (`R7`). Colonne a lettere lungo X del robot (A verso la coda), righe a numeri lungo Y;
- **millefori**: la C2 del BOM è una 5 × 7 cm **a doppia faccia, una piazzola per foro** (`docs/BOM.md` riga 70): non ci sono strisce da tagliare. I collegamenti si fanno sul lato saldature con ponticelli di stagno o filo nudo fra fori vicini e con fili isolati. Un filo del lato saldature si salda sulla saldatura del pin, non dentro il foro;
- **fili**: 30 AWG siliconico (X31, 3 colori) per i segnali; 26 AWG (B17) dove la tabella lo dice (masse di ritorno, 5 V, batteria). Nel disegno i fili corrono nei canali fra i fori, mai sopra un foro che non toccano; dove due o tre fili condividono un canale sono disegnati affiancati;
- **stato dei dati**: come nel resto del progetto, V verificato, S stimato, C da confermare sul pezzo. Le piedinature non verificate e le scelte da approvare sono nei problemi (`guida/problemi/schemi.yaml`, S-01 … S-27);
- tutte le quote in mm nella terna del robot (X avanti, Y a sinistra).

Il disegno segue le fonti. Dove le fonti non bastano ho scelto la soluzione più prudente e l'ho scritta in "Scelte" con il perché. Le scelte che cambiano un passo già scritto della guida sono nella sezione 3.

## 1. Basetta dell'ESP32

Millefori C2 tagliata a **56 × 35** (x 22…78, |y| ≤ 17,5; D-053). Griglia di **21 colonne (A–U) × 13 righe**: colonna A a x 23,77 (il primo pin dell'ESP32), riga 1 a y +15,24 (lato sinistro del robot), riga 7 sull'asse. Il bordo di coda sta 1,8 mm dietro la colonna A, quello di testa 3,4 mm davanti alla U.

### 1.0 Zone vietate sotto la basetta

Sotto la basetta ci sono 3,3 mm fino al vassoio (`cad/script/corpo.py:86`, `cor_bas_luce`). In quello spazio ci sono:
- **quattro teste M3** delle viti del vassoio (M3 × 6 sui distanziali B18, `docs/BOM.md:114`), a (30; ±12,5) e (75; ±12,5), alte 3 mm sopra il vassoio (z 2,6–5,6): fra testa e basetta restano **0,3 mm** (`guida/dati/fori.json`, `Corpo_Vassoio` `foro_pa/pb/aa/ab`, z 1,0–2,6; testa DIN 912 Ø 5,5 × 3 [V norma]);
- **quattro colonnine** Ø 5,8 a (29; ±6,8) e (75,5; ±6,5), su cui la basetta appoggia con il lato saldature (`fori.json` `bas_col_pa/pb/aa/ab_ins`, z 1,9–5,9; D-053).

Regole del disegno (le zone sono tratteggiate in `basetta_saldature.svg`, i fori vietati hanno una croce in tutti e due i disegni):
- nessuna saldatura con il centro a meno di 2,75 + 0,9 mm da una testa M3 o di 2,9 + 0,9 mm da una colonnina (raggio di un giunto 0,9 [S]);
- nessun filo né ponticello a meno di 3,35 mm da una testa M3 o di 3,5 mm da una colonnina;
- fori vietati (40): C-1, D-1, C-2, D-2, C-3, D-3, T-2, U-1, U-2, U-3, C-11, D-11, C-12, D-12, C-13, D-13, T-12, U-11, U-12, U-13 (teste M3); B-4, B-5, C-4, C-5, D-4, D-5, B-9, B-10, C-9, C-10, D-9, D-10, T-4, T-5, U-4, U-5, T-9, T-10, U-9, U-10 (colonnine; C-3, C-11, U-3 e U-11 stanno sotto tutte e due).

Tre pin degli strip dell'ESP32 cadono sopra una testa M3 e servono: **T-2 (3V3), D-12 (GPIO21, TX verso la SSC-32)** e, al limite, B-2 (GPIO14, 3,69 mm dal centro). Non si possono spostare: il GPIO21 è deciso (D-012) e non c'è un GPIO libero (`piano-elettronica-software.md` 2.3). Con le teste DIN 912 la basetta non si può montare: **bloccante S-19** (teste basse, o viti del vassoio spostate nel CAD 2.1.7). Lo schema è disegnato in modo da valere con qualunque delle due soluzioni: fuori da quei tre pin, nessun giunto e nessun filo nelle zone. Gli altri pin degli strip nelle zone (C-2, D-2, B-12, C-12, T-12) non sono usati: si tagliano a filo e non si saldano.

### 1.1 Componenti

| Sigla | Cosa (voce del BOM) | Fori | Note |
|---|---|---|---|
| U1 | ESP32-S3-CAM UICPAL (A2) su due strip femmina 1 × 20 (C2) | strip in riga 2 e riga 12, colonne A–T. Pin 1 (3V3 e GPIO43) in colonna T, verso l'antenna | file a 25,4 mm (10 passi): il CAD dice 24,7 [C], S-02. Piedinatura dall'immagine dell'inserzione [S], S-15. Si saldano solo i pin usati (A-2, B-2, I-2, T-2; A-12, D-12, E-12, F-12, L-12…R-12); gli altri si tagliano a filo e restano senza stagno |
| U2 | regolatore 5 V Pololu D24V22F5 (B2) | corpo colonne M–S, righe 4–10; pin in riga 4: N-4 PG, O-4 EN, P-4 VIN, Q-4 GND, R-4 VOUT | ordine dei pin [C] (S-03). Appoggiato su nastro Kapton (S-24), alto 7,2; PG ed EN non collegati (EN ha 270 kΩ interni verso VIN, Pololu 2858). Q-4 è il centro della stella di massa |
| U3 | buffer SN74AHCT125N in DIP-14 (X9) | pin 1–7 in E-8…K-8, pin 8–14 in K-11…E-11 (pin 1 in E-8, tacca verso la coda) | senza zoccolo. **Due canali**: 1A → 1Y per il polo 4, 2A → 2Y per le tibie (rilievo 8); canali 3 e 4 con A e OE a massa |
| U4 | traslatore C1, KAmod Level Shift x4 (15,7 × 10,7, due file da 6) | lato 5 V in E-4…J-4: HV, H1, H2, H3, H4, GND; lato 3,3 V in E-7…J-7: LV, L1, L2, L3, L4, GND | sigle e passo fra le file (7,62) [C], S-04. TX sul canale 1, RX sul canale 3; canali 2 e 4 liberi. Sulle sue strip maschio, pin tagliati a filo sopra il modulo e sotto la basetta (rilievo 10). Sotto il modulo non c'è niente |
| PTC1 | fusibile ripristinabile Bourns MF-R075 (X9) | reofori in L-8 e L-10 | sdraiato **sopra U3, su Kapton** (rilievo 9): 5,1 + 3,0 = 8,1 mm su 8,5 [C] (S-08) |
| D1 | Schottky 1N5819 (C3) | catodo A-6, anodo D-6 | fra il 5 V del regolatore e il pin 5V dell'ESP32 (S-07) |
| R1 | 10 kΩ (X9) | D-8 (LED_IN) – A-8 (massa) | pull-down di GPIO48 all'ingresso del buffer |
| R2 | 330 Ω (X9) | L-7 (1Y) – L-4 (polo 4) | in serie al dato dei LED verso il polo 4 |
| R4 | 4,7 kΩ (B10) | J-3 (SCL) – M-3 (3V3S) | pull-up di SCL. Valore: S-13 |
| R5 | 4,7 kΩ (B10) | N-3 (3V3S) – Q-3 (SDA) | pull-up di SDA |
| R7 | 47 kΩ 1 % (B10) | T-11 (GPIO1) – Q-11 (massa) | partitore della batteria, lato basso. Il lato alto (R6, 100 kΩ 1 %) sta alla 2813 (S-20) |
| CS1 | 100 nF SMD (B8) | fra R-11 e R-10, lato saldature | filtro di GPIO1 (`docs/BOM.md` riga 50) |
| CS2 | 100 nF SMD (kit di B8) | fra E-11 e F-11, lato saldature | disaccoppiamento di U3 (VCC–GND sui pin 14 e 13) |
| J1 | filo 19, T-3 → N-3 | lato saldature | collega il 3V3 dell'ESP32 al 3,3 V dei sensori (3V3S). Con X3 si toglie (S-12) |
| — | cavo piatto a 16 vie (X2) | poli 1–2 in A-13, B-13; poli 3–13 in E-13…O-13 | C-13 e D-13 sono sopra la testa M3: i conduttori 1 e 2 si separano di due fori. Polo 14 tagliato; 15 e 16 vanno alla 2813 |

Non stanno sulla basetta (S-20, S-11, S-12): R6 (100 kΩ) saldata sull'uscita della 2813; D2 (1N4148) in linea nella guaina del filo di abilitazione; R3a e R3b (pull-down dell'abilitazione) saldate sui due D42V110F6; la 100 kΩ di GPIO41 sulla 2813; R9 (330 Ω) in linea sul filo del dato delle tibie; il D24V5F3 (X3), solo se serve.

### 1.2 Reti (netlist)

Pin e fori di ogni rete. I fili e i ponticelli che le realizzano sono in 1.3. Fonti con file e riga (cartella `docs/`, salvo dove è scritto).

| Rete | Pin e fori | Fonte |
|---|---|---|
| VBAT | P-4 (U2 VIN); filo dalla 2813, saldato per ultimo | cablaggio.md:32, :76 (2813 → D24V22F5); un filo da P-4 alla 2813 lungo il bordo (rilievo 6) |
| 5V_REG | E-4 (U4 HV); R-4 (U2 VOUT); D-6 (D1); L-8 (PTC1); E-11 (U3 14 VCC); CS2 verso massa (lato saldature) | cablaggio.md:27–30, :77; BOM.md:43 (B2); predisposizioni.md:109 |
| 5V_ESP | A-2 (ESP32 5V); A-6 (D1) | cablaggio.md:27 (D24V22F5 → pin 5V); D1: scelta S-07, BOM.md:71 (C3) |
| 5V_LED | L-10 (PTC1); A-13 (filo: 1); B-13 (filo: 2) | cablaggio.md:28–29, :77 (PTC → poli 1-2 e tibie); predisposizioni.md:104 |
| 3V3_ESP | T-2 (ESP32 3V3); T-3 (ponticello) | dimensioni-componenti.md:74 (pin 3V3); piano-elettronica-software.md:77 |
| 3V3S | K-1 (filo: 3V3); L-1 (filo: 3V3); M-1 (filo: 3V3); N-1 (filo: 3V3); M-3 (R4); N-3 (R5); E-7 (U4 LV); I-13 (filo: 7); J1 (filo 19) dal 3V3 dell’ESP32 | predisposizioni.md:108 (D24V5F3 o 3V3 della scheda); cablaggio.md:116, :139 (polo 7); LV di U4 (S-04) |
| GND | A-1 (filo: GND); B-1 (filo: GND); E-1 (filo: GND); F-1 (filo: GND); E-3 (filo: massa della seriale (Dupont)); J-4 (U4 GND); Q-4 (U2 GND); J-5 (ponticello); Q-5 (ponticello); J-6 (ponticello); Q-6 (ponticello); J-7 (U4 GND); A-8 (R1); E-8 (U3 1 1OE); H-8 (U3 4 2OE); K-8 (U3 7 GND); E-9 (ponticello); H-9 (ponticello); K-9 (ponticello); E-10 (ponticello); F-10 (ponticello); G-10 (ponticello); H-10 (ponticello); I-10 (ponticello); J-10 (ponticello); K-10 (ponticello); Q-10 (ponticello); R-10 (CS1); F-11 (U3 13 4OE); G-11 (U3 12 4A); I-11 (U3 10 3OE); J-11 (U3 9 3A); Q-11 (R7); A-12 (ESP32 GND); E-13 (filo: 3); G-13 (filo: 5); K-13 (filo: 9); S-13 (filo: massa della 2813) | predisposizioni.md:110 (le masse tornano alla basetta); cablaggio.md:137–140 (poli 3, 5, 9) |
| SCL | G-1 (filo: SCL); H-1 (filo: SCL); I-1 (filo: SCL); J-1 (filo: SCL); I-2 (ESP32 GPIO3); J-3 (R4); H-13 (filo: 6) | piano-elettronica-software.md:88 (GPIO3); cablaggio.md:42, :116, :138 (polo 6) |
| SDA | Q-1 (filo: SDA); R-1 (filo: SDA); S-1 (filo: SDA); T-1 (filo: SDA); Q-3 (R5); E-12 (ESP32 GPIO47); J-13 (filo: 8) | piano-elettronica-software.md:101 (GPIO47); cablaggio.md:42, :116, :139 (polo 8); pull-up :133 |
| LED_IN | D-8 (R1); F-8 (U3 2 1A); I-8 (U3 5 2A); F-12 (ESP32 GPIO48) | cablaggio.md:47 (GPIO48, 10 kΩ a massa, ingresso del buffer); piano-elettronica-software.md:102; 2A per le tibie (rilievo 8) |
| Y1 | L-7 (R2); G-8 (U3 3 1Y) | cablaggio.md:47 (uscita del buffer → 330 Ω) |
| DATA | L-4 (R2); F-13 (filo: 4) | cablaggio.md:47–48, :137 (polo 4); cablaggio.md:108 (luci delle tibie) |
| DATA2 | J-8 (U3 6 2Y); T-13 (filo: dato tibie (330 Ω in linea)) | cablaggio.md:47–48, :108 (ramo delle tibie); secondo canale del buffer (rilievo 8) |
| TX3 | F-7 (U4 L1); D-12 (ESP32 GPIO21) | cablaggio.md:41, :160; piano-elettronica-software.md:93 (GPIO21); BOM.md:69 (C1) |
| RX3 | B-2 (ESP32 GPIO14); H-7 (U4 L3) | cablaggio.md:41, :160; piano-elettronica-software.md:91 (GPIO14) |
| TX5 | F-3 (filo: TX verso la SSC-32 (Dupont)); F-4 (U4 H1) | cablaggio.md:41 (traslatore → RX della SSC-32); 08-elettronica.yaml 8.20 |
| RX5 | H-3 (filo: RX dalla SSC-32 (Dupont)); H-4 (U4 H3) | cablaggio.md:41 (TX della SSC-32 → traslatore); 08-elettronica.yaml 8.20 |
| GPIO42 | P-12 (ESP32 GPIO42); P-13 (filo: GPIO42 → D2 in linea → EN) | cablaggio.md:31, :78; piano-elettronica-software.md:99; D2 in linea e R3 ai regolatori (S-20) |
| OFF | O-12 (ESP32 GPIO41); Q-13 (filo: OFF della 2813) | cablaggio.md:32, :79; piano-elettronica-software.md:98 (GPIO41) |
| SENSE | R-11 (CS1); S-11 (ponticello); T-11 (R7); R-12 (ESP32 GPIO1); R-13 (filo: partitore (100 kΩ alla 2813)); CS1 verso massa (lato saldature) | cablaggio.md:32 (partitore 100 k / 47 k → GPIO1; 100 k alla 2813, S-20); BOM.md:50 (B8), :52 (B10) |
| BCLK | L-12 (ESP32 GPIO38); L-13 (filo: 10) | cablaggio.md:49, :140 (polo 10); piano-elettronica-software.md:95 (GPIO38) |
| WS | M-12 (ESP32 GPIO39); M-13 (filo: 11) | cablaggio.md:49, :141 (polo 11); piano-elettronica-software.md:96 (GPIO39) |
| MIC | N-12 (ESP32 GPIO40); N-13 (filo: 12) | cablaggio.md:49, :141 (polo 12); piano-elettronica-software.md:97 (GPIO40) |
| AMP | Q-12 (ESP32 GPIO2); O-13 (filo: 13) | cablaggio.md:49, :142 (polo 13); piano-elettronica-software.md:87 (GPIO2) |

Pin dell'ESP32 (riga 2, da coda a testa: 5V, 14, 13, 12, 11, 10, 9, 46, 3, 8, 18, 17, 16, 15, 7, 6, 5, 4, RST, 3V3; riga 12: GND, 19, 20, 21, 47, 48, 45, 0, 35, 36, 37, 38, 39, 40, 41, 42, 2, 1, 44, 43; `docs/dimensioni-componenti.md` righe 70–93 [S]). Usati: A-2 5V, B-2 GPIO14, I-2 GPIO3, T-2 3V3, A-12 GND, D-12 GPIO21, E-12 GPIO47, F-12 GPIO48, L-12 GPIO38, M-12 GPIO39, N-12 GPIO40, O-12 GPIO41, P-12 GPIO42, Q-12 GPIO2, R-12 GPIO1. Gli altri restano liberi (camera, PSRAM, USB, strapping) e non si saldano.

**Verifiche fatte sullo schema** (script del progettista, non nella repo):
- ogni rete è chiusa dai suoi fili e ponticelli, nessun filo o ponticello unisce due reti;
- nessun pin, giunto o filo nelle zone vietate di 1.0, salvo i pin T-2, D-12 e B-2 (S-19);
- **VBAT** confina solo con i pin di U2 (O-4 EN, che ha 270 kΩ interni verso VIN, e Q-4 massa) e con fori vuoti (P-3, P-5). Nessun filo passa sugli angoli di P-4, e il filo della batteria non ne incrocia nessun altro;
- **nessuna piazzola a 5 V o a livello 5 V accanto a una a 3,3 V o a un GPIO**, salvo queste coppie, che la disposizione non può evitare e che le prove 5 e 14 controllano: E-11/E-12 (VCC di U3 e GPIO47), F-13/F-12 (polo 4 e GPIO48), G-8/G-7 (1Y e L2 libero, che ha solo il pull-up da 10 kΩ del modulo), I-8/J-8 e F-8/G-8 (ingressi e uscite dello stesso integrato);
- GPIO42 (P-12, P-13) confina con O-13 (AMP), Q-13 (OFF) e con i pin vicini dello strip (O-12, Q-12): prova 13, S-25.

Instradamento: 37 fili sul lato saldature, 44 incroci fra due fili (sempre fili isolati, mai su un giunto) e al più tre fili affiancati nello stesso canale. Sotto restano 3,3 mm: giunto (circa 1 mm) più due strati di filo 30 AWG o un 26 AWG sopra un 30 AWG. Sopra le zone delle colonnine non passa niente: la basetta ci appoggia.

### 1.3 Ponticelli e fili del lato saldature

Ponticelli (stagno o filo nudo fra fori vicini; le catene di fori vuoti, come la barra di massa sotto U3 lungo la riga 10, si fanno con un filo nudo saldato su ogni foro):
P-12–P-13 (GPIO42), J-4–J-5 (GND), J-5–J-6 (GND), J-6–J-7 (GND), F-11–G-11 (GND), I-11–J-11 (GND), E-10–F-10 (GND), F-10–G-10 (GND), G-10–H-10 (GND), H-10–I-10 (GND), I-10–J-10 (GND), J-10–K-10 (GND), E-8–E-9 (GND), E-9–E-10 (GND), H-8–H-9 (GND), H-9–H-10 (GND), K-8–K-9 (GND), K-9–K-10 (GND), F-10–F-11 (GND), I-10–I-11 (GND), M-3–N-3 (3V3S), T-2–T-3 (3V3_ESP), I-1–I-2 (SCL), F-3–F-4 (TX5), H-3–H-4 (RX5), A-1–B-1 (GND), E-1–F-1 (GND), G-1–H-1 (SCL), H-1–I-1 (SCL), I-1–J-1 (SCL), K-1–L-1 (3V3S), L-1–M-1 (3V3S), M-1–N-1 (3V3S), Q-1–R-1 (SDA), R-1–S-1 (SDA), S-1–T-1 (SDA), A-13–B-13 (5V_LED), L-12–L-13 (BCLK), M-12–M-13 (WS), N-12–N-13 (MIC), R-12–R-13 (SENSE), R-12–R-11 (SENSE), R-11–S-11 (SENSE), S-11–T-11 (SENSE), R-10–Q-10 (GND), Q-10–Q-11 (GND), Q-4–Q-5 (GND), Q-5–Q-6 (GND).

Fili isolati, numerati come in `basetta_saldature.svg` (anche in fondo al disegno, con la sezione):

| N. | Da | A | Rete | Sezione | A cosa serve |
|---|---|---|---|---|---|
| 1 | S-13 | Q-4 | GND | 26 AWG | massa della 2813 → stella |
| 2 | E-13 | G-13 | GND | 26 AWG | massa dei LED (poli 3, 5) |
| 3 | G-13 | K-13 | GND | 26 AWG | massa dei LED (poli 5, 9 e tibie) |
| 4 | K-13 | Q-5 | GND | 26 AWG | massa dei LED → stella |
| 5 | K-8 | Q-6 | GND | 26 AWG | massa della logica → stella |
| 6 | Q-10 | Q-6 | GND | 30 AWG | masse di R7 e CS1 → stella |
| 7 | A-12 | A-8 | GND | 26 AWG | massa dell’ESP32 |
| 8 | A-8 | E-8 | GND | 26 AWG | massa dell’ESP32 → U3 |
| 9 | J-7 | K-8 | GND | 26 AWG | masse di U4 |
| 10 | E-3 | J-4 | GND | 30 AWG | massa della seriale e del bus |
| 11 | E-1 | E-3 | GND | 30 AWG | massa del bus (salta E-2) |
| 12 | A-1 | A-8 | GND | 30 AWG | massa del bus |
| 13 | R-4 | L-8 | 5V_REG | 26 AWG | 5 V del regolatore → PTC |
| 14 | L-8 | E-11 | 5V_REG | 26 AWG | 5 V → VCC di U3 |
| 15 | E-11 | E-4 | 5V_REG | 26 AWG | 5 V → HV di U4 |
| 16 | E-4 | D-6 | 5V_REG | 26 AWG | 5 V → D1 |
| 17 | A-6 | A-2 | 5V_ESP | 26 AWG | 5 V dopo D1 → pin 5V dell’ESP32 |
| 18 | L-10 | B-13 | 5V_LED | 26 AWG | 5 V dei LED → poli 1-2 e tibie |
| 19 | T-3 | N-3 | J1 | 30 AWG | J1: 3V3 dell’ESP32 → 3V3S (si toglie con X3) |
| 20 | M-3 | M-1 | 3V3S | 30 AWG | 3V3S → bus (salta M-2) |
| 21 | M-3 | E-7 | 3V3S | 30 AWG | 3V3S → LV di U4 |
| 22 | N-3 | I-13 | 3V3S | 30 AWG | 3V3S → polo 7 |
| 23 | J-3 | J-1 | SCL | 30 AWG | SCL → bus (salta J-2) |
| 24 | J-3 | H-13 | SCL | 30 AWG | SCL → polo 6 |
| 25 | Q-3 | Q-1 | SDA | 30 AWG | SDA → bus (salta Q-2) |
| 26 | E-12 | J-13 | SDA | 30 AWG | SDA (GPIO47) → polo 8 |
| 27 | E-12 | Q-3 | SDA | 30 AWG | SDA → R5 |
| 28 | D-12 | F-7 | TX3 | 30 AWG | TX3 (GPIO21) → L1 |
| 29 | B-2 | H-7 | RX3 | 30 AWG | RX3 (GPIO14) ← L3 |
| 30 | F-12 | F-8 | LED_IN | 30 AWG | GPIO48 → 1A |
| 31 | F-8 | I-8 | LED_IN | 30 AWG | 1A → 2A |
| 32 | D-8 | F-8 | LED_IN | 30 AWG | R1 → 1A |
| 33 | G-8 | L-7 | Y1 | 30 AWG | 1Y → R2 |
| 34 | L-4 | F-13 | DATA | 30 AWG | R2 → polo 4 |
| 35 | J-8 | T-13 | DATA2 | 30 AWG | 2Y → tibie |
| 36 | Q-12 | O-13 | AMP | 30 AWG | GPIO2 → polo 13 |
| 37 | O-12 | Q-13 | OFF | 30 AWG | GPIO41 → OFF |

Filo della batteria (non numerato, disegnato in rosso): **VBAT**, dall'uscita della 2813 a P-4. Arriva al bordo di coda nell'angolo sinistro, corre sul lato saldature lungo il bordo sinistro (fuori dalle piazzole della riga 1 e dalle teste M3), entra fra le colonne O e P passando sopra P-1 e P-3 vuoti e P-2 non saldato, e si salda su P-4. Si posa **per ultimo**, dopo tutte le altre saldature, ed è fermato al bordo con un punto di colla a caldo o con Kapton. Filo siliconico se c'è (S-27), altrimenti 26 AWG di B17.

### 1.4 Ordine di saldatura (dal più basso al più alto)

Al banco (sezione 4), ESP32 fuori, prima di avvitare la basetta. Un componente alla volta, poi continuità.

1. Taglia la millefori a 56 × 35; trapana i quattro fori Ø 2,2 usando il vassoio come dima (D-053). Pulisci le piazzole con alcol. Segna con un pennarello le croci di 1.0 sul lato saldature: lì non va stagno.
2. Prova a secco: strip femmina sull'ESP32, l'insieme appoggiato sulla basetta con U3, PTC1 (su Kapton), U4 sulle sue strip, D1 e le resistenze solo infilati. L'ESP32 deve andare in fondo (S-08).
3. Resistenze e diodo sdraiati, lato componenti: R1, R2, R4, R5, R7, poi D1 (Ø 2,7, fascia verso A-6). Reofori tagliati a 1 mm sotto la basetta.
4. U3 (pin 1 in E-8, tacca verso la coda), saldato senza zoccolo.
5. U4 sulle sue strip maschio, lato 5 V (HV) in riga 4 [C: controlla le sigle prima, S-04]. Taglia i pin a filo sopra il modulo e sotto la basetta prima di saldare.
6. U2 su un quadrato di Kapton, con i pin (o spezzoni di reoforo) nei fori di riga 4 [C: ordine dei pin, S-03].
7. PTC1: Kapton sopra U3, PTC sdraiato, reofori piegati in L-8 e L-10.
8. Strip femmina dell'ESP32: taglia a filo le code dei pin non usati (elenco in 1.1) e quelle di B-2, T-2, D-12; infila le strip sull'ESP32, appoggia l'insieme, salda i pin usati partendo da due ai capi di ogni strip, controlla che le strip siano dritte, togli l'ESP32. B-2, T-2 e D-12 con un giunto piatto, solo dopo la scelta di S-19.
9. Lato saldature: ponticelli e barra di massa sotto U3; poi i fili 1–37 in ordine (masse, 5 V, 3,3 V, bus, segnali), poi CS1 e CS2.
10. Fili verso il resto del robot (1.6), saldati al banco: cavo piatto, bus della riga 1, Dupont della seriale, fili di riga 13 (GPIO42 con D2 in linea, OFF, partitore, massa della 2813, tibie con R9 in linea).
11. **VBAT per ultimo**, come in 1.3.
12. Prove di 1.5, ancora senza ESP32; poi la prima accensione senza ESP32 (1.5, in fondo).

### 1.5 Prove con il multimetro, prima di alimentare

ESP32 fuori dagli strip, nessun filo esterno collegato a batteria o regolatori. Per i pin dell'ESP32 si mette il puntale nella presa della strip. Una lettura di 0 Ω fra due reti diverse è sempre un ponte di stagno.

| N. | Punto | Atteso | Se no |
|---|---|---|---|
| 1 | VBAT (P-4) contro massa (Q-4) | non 0 Ω; sale (condensatori d'ingresso di U2) e resta alta [S] | corto sulla batteria: F2 salterebbe |
| 2 | VBAT (P-4) contro ogni presa delle strip (righe 2 e 12), salvo A-12 (massa, vedi 1) | aperto | ponte: la batteria arriverebbe all'ESP32 |
| 3 | 5V_REG (R-4) contro massa | non 0 Ω; sale (condensatori di U2) [S] | corto sul 5 V |
| 4 | 5V_REG (R-4) contro 3V3 (presa T-2) | oltre 1 kΩ [S] | ponte fra 5 V e 3,3 V: brucia l'ESP32 e i sensori |
| 5 | **ogni piazzola delle righe 1, 3, 11 e 13 contro la presa dello strip accanto**: aperto o qualche kΩ (pull-up), mai 0 Ω, salvo i collegamenti voluti I-1/I-2, L-13/L-12, M-13/M-12, N-13/N-12, P-13/P-12, R-13/R-12, R-11/R-12. Una per una, in particolare: E-11/E-12 (5 V e GPIO47), F-13/F-12 (dato a 5 V e GPIO48), A-13/A-12 (5 V dei LED e massa), A-1/A-2 (massa e 5V), B-1/B-2 (massa e GPIO14), T-1/T-2 (SDA e 3V3: 4,7 kΩ), Q-11/Q-12 (massa e GPIO2), O-13/O-12 (polo 13 e GPIO41), Q-13/Q-12 (OFF e GPIO2) | come a sinistra | ponte fra una piazzola e un pin dell'ESP32; con il 5 V lo brucia |
| 6 | 5V_REG, 5V_LED (A-13) e DATA (F-13) contro ogni presa delle righe 2 e 12 | aperto, salvo A-2 (vedi 7) e A-12 (massa, vedi 3) | ponte fra un 5 V e un GPIO |
| 7 | D1, prova diodi: puntale rosso su D-6, nero su A-6 | 0,15–0,35 V [S]; invertiti: OL | D1 al contrario o in corto |
| 8 | 5V_LED (A-13) contro 5V_REG (R-4) | sotto 1 Ω (PTC freddo) [S] | PTC non saldato |
| 9 | A-13 contro B-13 | 0 Ω | |
| 10 | 3V3S (M-3) contro 3V3 (presa T-2) | 0 Ω con J1 (filo 19); aperto senza | |
| 11 | SDA (Q-1) contro 3V3S (M-3); SCL (G-1) contro 3V3S | 4,7 kΩ ciascuno (solo R4 e R5: moduli non collegati) | |
| 12 | SDA contro SCL | circa 9,4 kΩ (le due pull-up in serie) | ponte fra SDA e SCL |
| 13 | GPIO42 (P-13) contro massa, contro O-13, Q-13, presa O-12, presa Q-12 e contro ogni rete di alimentazione (P-4, R-4, A-13, T-2) | aperto (D2 e le R3 non sono sulla basetta) | un ponte accenderebbe il rail dei servo o spegnerebbe la 2813 |
| 14 | G-8 (1Y) contro G-7 (L2) | non 0 Ω | ponte fra l'uscita a 5 V del buffer e il lato a 3,3 V del traslatore |
| 15 | GPIO1 (presa R-12) contro massa | circa 47 kΩ (R7) [S] | |
| 16 | GPIO48 (presa F-12) contro massa | 10 kΩ (R1) | |
| 17 | OFF (Q-13) contro massa | aperto (la 100 kΩ sta sulla 2813) | |
| 18 | ogni filo della tabella 1.3 e ogni polo del cavo piatto, dal suo capo al pin dell'ESP32 | 0 Ω | |
| 19 | massa: Q-4, S-13, A-12, K-8, E-13, A-1, E-3 fra loro | 0 Ω | |
| 20 | ogni foro con la croce, sul lato saldature | nessuno stagno, nessun filo sopra (salvo B-2, T-2, D-12) | |

**Prima accensione, senza ESP32** (rilievo 5: l'ordine dei pin di U2 non è confermato, S-03). Collega solo il ramo logica (passi 4.07–4.08: 2813, filo VBAT, massa della 2813, R6) e accendi. Misura nelle prese degli strip, contro A-12:

| Punto | Atteso | Se no |
|---|---|---|
| R-4 (uscita di U2) | 5,0 V [V] | spegni: ordine dei pin di U2 sbagliato |
| presa A-2 (5V, dopo D1) | 4,6–5,0 V a vuoto [S] (con l'ESP32 inserito scende a 4,55–4,7) | D1 al contrario |
| presa R-12 (GPIO1) | 0,32 volte il pacco: 2,37 V a 7,4 V, 2,69 V a 8,4 V | R6 o R7 sbagliate |
| tutte le altre prese, T-2 compresa | 0 V (sotto 0,1 V) | spegni: tensione su un pin dell'ESP32 |

Solo dopo: spegni, inserisci l'ESP32 con la USB staccata, riaccendi e misura R-4 (5,0 V), A-2 (4,55–4,7 V) e T-2 (3,3 V).

### 1.6 Collegamenti verso il resto del robot

| Fori | Rete | Va a | Filo e connettore | Fonte |
|---|---|---|---|---|
| P-4 (lato saldature) | VBAT | uscita della 2813 | un filo, siliconico se c'è (S-27), saldato ai due capi; lungo il bordo sinistro, posato per ultimo (1.3) | `cablaggio.md` 76 |
| S-13 | massa | massa della 2813 | 26 AWG nero, saldato | `cablaggio.md` 76; stella su Q-4 (rilievo 7) |
| R-13 | partitore | R6 da 100 kΩ 1 % saldata sull'uscita della 2813, in guaina | 26 AWG; il filo porta al più 2,7 V, attraverso 100 kΩ (S-20) | `cablaggio.md` 32 |
| Q-13 | OFF | pin OFF della 2813; sulla 2813 una 100 kΩ fra OFF e massa | 26 AWG | `cablaggio.md` 79; S-11 |
| P-13 | GPIO42 | D2 (1N4148) in linea nella guaina, **anodo dal lato della basetta**; dopo il diodo il filo si divide e va al pin **ENA** di ciascun D42V110F6. Su ogni regolatore una R3 (22 kΩ, S-05) fra ENA e GND. ENB non si collega | 26 AWG; tre fili dopo il diodo | `cablaggio.md` 31, 78; Pololu 5673; S-20 |
| F-3 | TX5 (uscita H1 del traslatore) | pin RX della SSC-32 | 26 AWG con Dupont femmina (C4), dal bordo di coda | `cablaggio.md` 41, 160 |
| H-3 | RX5 (ingresso H3) | pin TX della SSC-32 | idem | idem |
| E-3 | massa | pin GND della SSC-32 | idem; vedi S-22 (doppia massa con VL−) | idem |
| riga 1: A-1, B-1, E-1, F-1 (massa), G–J (SCL), K–N (3,3 V), Q–T (SDA) | bus I2C0 | ramo 1 INA260 S: A-1, G-1, K-1, Q-1; ramo 2 INA260 D: B-1, H-1, L-1, R-1; ramo 3 ADC e IMU: E-1, I-1, M-1, S-1 (due fili per foro); ramo 4 ToF frontale: F-1, J-1, N-1, T-1 | cavetti Qwiic tagliati (nero massa, rosso 3,3 V, blu SDA, giallo SCL) e i 4 fili di IMU e ToF | `cablaggio.md` 116–124 |
| A-13, B-13, E-13…O-13 | poli 1–13 | scheda del carapace, spina IDC | cavo piatto 16 vie, 15 cm [S], filo rosso = polo 1; conduttori separati per 25 mm, aperti a ventaglio; 1 e 2 saltano C e D | `cablaggio.md` 132–143 |
| — | poli 15 e 16 | pin A e B della 2813 | separati dal cavo piatto per 10 cm e giuntati a due fili 26 AWG (stagno e guaina) | `cablaggio.md` 80 |
| K-13, B-13, T-13 | massa, +5 V, dato dei LED delle tibie | prese delle luci delle tibie (polo marrone, rosso, arancio) | tre fili 26 AWG (dato 30 AWG), saldati al banco e lunghi fino alle prese [S]: massa nel foro del polo 9, +5 V nel foro del polo 2, dato su T-13 con **R9 da 330 Ω in linea** nella guaina vicino alla basetta | `cablaggio.md` 108; passo 8.25; rilievo 8 |

Piedinatura del cavo piatto: 1–2 +5 V (dopo PTC1), 3 massa, 4 dato dei LED a 5 V, 5 massa, 6 SCL, 7 +3,3 V sensori, 8 SDA, 9 massa, 10 BCLK, 11 WS, 12 dati dei microfoni, 13 dati verso l'amplificatore, 14 riserva, 15–16 pulsante (`cablaggio.md` righe 132–143 [V]).

**Misura RMT al banco (P2, rilievo 22).** Il piano usa un canale libero del traslatore per leggere su GPIO38 gli impulsi della SSC-32 (`piano-elettronica-software.md` riga 95). Con questo schema il canale libero è il 4: un Dupont dall'uscita di un canale della SSC-32 a I-4 (H4) e un **filo provvisorio da I-7 (L4) a L-12 (GPIO38)**, sul lato saldature. Si toglie dopo la misura, prima di collegare la scheda del carapace. Il ponticello L-12–L-13 non dà fastidio: a basetta sola il polo 10 non va da nessuna parte.

### 1.7 Scelte e perché

1. **Diodo D1 (1N5819) fra il 5 V e il pin 5V dell'ESP32.** È l'alternativa del BOM C3 messa sempre: senza, con la sola USB collegata, la USB potrebbe alimentare all'indietro il 5 V dei LED, il regolatore e il ramo della batteria (non sappiamo se la scheda ha un diodo, `guida/problemi/banco.yaml`). Costo: 0,3–0,45 V di caduta. S-07.
2. **Due canali del buffer** (rilievo 8): 1A e 2A insieme su GPIO48; 1Y → R2 → polo 4, 2Y → R9 in linea → tibie. Un corto in una tibia non spegne più l'anello e i lobi, e il carico capacitivo delle sei linee lunghe sta su un'uscita sua. `cablaggio.md` riga 47 prevede un canale solo; la prima versione dello schema lo teneva perché sulla basetta non c'era posto per un secondo 330 Ω: R9 sta nella guaina.
3. **Un solo PTC** a monte di poli 1–2 e tibie, come `cablaggio.md` riga 77, **su Kapton** sopra U3 (rilievo 9: a PTC scattato la superficie supera 100 °C). L'alternativa del PTC in linea fuori dalla basetta resta in S-08.
4. **Pull-up 4,7 kΩ** su SDA e SCL: con le tre schede Adafruit (3,3 kΩ) e i pull-up di GY-6500 e ToF (10 kΩ ciascuno, S) l'equivalente viene circa 1,2 kΩ, dentro 1,0–1,4 (`piano-elettronica-software.md` riga 133). Si misura al passo 8.28 (S-13).
5. **100 kΩ di GPIO41 sulla 2813**: il pin OFF scatta sopra 1 V (Pololu 2813) e GPIO41 flotta durante il reset (S-11).
6. **D2 in linea e una R3 su ogni regolatore** (S-20, rilievo 3). Sulla basetta non resta nessuna piazzola dell'abilitazione accanto a una rete alta a riposo, e il pull-down sta all'altro capo del filo: se il filo si stacca, l'ENA resta a massa e il rail resta spento (con la R3 sulla basetta un filo staccato lasciava l'ENA al suo 1 MΩ verso VIN, cioè acceso).
7. **R6 alla 2813** (S-20): sulla basetta VBAT tocca solo U2, e il filo del partitore porta al più 2,7 V attraverso 100 kΩ; un suo corto non può fare danni. Il nodo di misura (R7, CS1, GPIO1) resta vicino all'ESP32, e se il filo si stacca GPIO1 legge 0 V (batteria scarica: il firmware spegne), non un valore a caso.
8. **Massa a stella su Q-4** (rilievo 7): la massa della 2813 (filo 1) e il ritorno dei LED (poli 3, 5, 9 e tibie, fili 2–4) arrivano ciascuno con il suo 26 AWG alla stella Q-4/Q-5/Q-6 sotto U2. La logica (ESP32, U3, U4, bus, seriale) arriva con i fili 5 e 6 come rami. Il ritorno dei LED e dell'ingresso non passa più sui pin di massa della logica.
9. **VBAT lungo il bordo** (rilievo 6), un filo solo dalla 2813 a P-4, posato per ultimo. Gli angoli di P-4 sono riservati: nessun altro filo ci passa.
10. **3,3 V dei sensori e lato LV del traslatore sulla stessa rete (3V3S)**, collegata al 3V3 dell'ESP32 con J1 (filo 19). Con X3 il traslatore prende il 3,3 V del D24V5F3, che si accende insieme all'ESP32 (stessa 2813).
11. **TX sul canale 1 e RX sul canale 3 del traslatore**: L2 (G-7), libero, sta accanto all'uscita 1Y del buffer (G-8); sul canale 2 il GPIO14 avrebbe confinato con un'uscita a 5 V.
12. **Pin degli strip non usati non saldati**: meno giunti accanto alle piazzole delle righe 1, 3, 11 e 13, e niente stagno sopra le teste M3.
13. **Seriale con tre Dupont** dalla riga 3 (E-3, F-3, H-3), con i ponticelli verso H1 e H3, fatti uscire dal bordo di coda sul lato componenti: un connettore in piedi non sta sotto l'ESP32.
14. **Fili dei segnali in 30 AWG siliconico** (X31): nei canali fra i fori ci stanno affiancati e reggono il saldatore. Le masse di ritorno, il 5 V e la batteria in 26 AWG (rilievo 21: con il pacco a 6 V, U2 a 2,5 A chiede circa 2,3 A in ingresso).


## 2. Scheda del carapace (X2)

Striscia di millefori (avanzo della C2, doppia faccia) di **20 × 30**, appesa al dorso davanti all'ottagono: x 29,5…49,5, |y| ≤ 15, faccia alta a z 30,9 sulle quattro bugne Ø 5,5 × 3,5 (`guida/dati/fori.json`, `ins_sch_a…d` a (32; ±12,5) e (47; ±12,5); `cad/script/corpo.py:1085`; `cad/script/rif_componenti.py` righe 184–186). Il lato componenti guarda in basso (verso l'ESP32), il lato saldature guarda il dorso e **appoggia sulle bugne** (3,5 mm d'aria fra le bugne).

Griglia di **7 colonne (A–G) × 11 righe**: colonna A a x 31,88 (lato ottagono), riga 1 a y +12,7. I quattro fori delle viti cadono sui fori d'angolo A-1, G-1, A-11, G-11, spostati di (0,12; 0,2) mm, cioè 0,23 mm, dal CAD: **si allargano a Ø 2,6** (rilievo 17), oppure si trapanano sulle quote misurate. **Zone delle bugne**: nessuna saldatura a meno di 2,75 + 0,9 mm dal centro di un foro d'angolo, nessun filo a meno di 3,35 mm (rilievo 12). Fori vietati: A-1, B-1, A-2, B-2, F-1, G-1, F-2, G-2, A-10, B-10, A-11, B-11, F-10, G-10, F-11, G-11.

**Bloccante (S-01).** La testata 2 × 8 dritta del BOM (X2) con la spina IDC innestata scende di 16–18 mm sotto la scheda (`predisposizioni.md` riga 72: circa 9 + 9 mm); sopra l'ESP32 ne restano circa 10 (il CAD dà 9 mm alla scheda con la spina, S). Lo schema qui sotto vale per i collegamenti; la posizione della testata va decisa con il CAD (2.1.7) prima di saldare. Con le zone delle bugne e la scatola della testata che copre le colonne C–F, sulla scheda restano libere solo le colonne A, B e G: il dato dei LED e i due fili del pulsante si saldano sul pin della testata, dal lato saldature.

### 2.1 Componenti

| Sigla | Cosa (voce del BOM) | Fori | Note |
|---|---|---|---|
| J2 | testata 2 × 8 con chiave, passo 2,54 (X2) | poli dispari in colonna D, pari in colonna E, righe 2–9: polo 1 in D-2, polo 2 in E-2 … polo 15 in D-9, polo 16 in E-9 | **tacca della scatola sul lato della colonna D** (poli dispari): sul disegno della spina Würth 61201623021 (quella del link del BOM) il polo 1 e la sporgenza della chiave stanno sulla stessa fila [V]; la testata va presa compatibile con quella spina (S-26). Il triangolo del polo 1 della spina va verso D-2. Bloccante S-01 |
| CE1 | elettrolitico 470 µF 10 V (X2) | + in A-9, − in B-9 | sdraiato verso la riga 5, Ø ≤ 6,3 [C] (S-18) |
| R8 | 100 kΩ (B10, D-074) | **non sulla scheda**: al microfono, fra SD e GND, nel fascio | pull-down della linea dati dei microfoni (rilievo 13, S-18). Vedi S-21: GPIO40 è anche la linea dati della microSD della scheda |

### 2.2 Reti (netlist)

| Rete | Pin e fori | Fonte |
|---|---|---|
| 5V | D-2 (polo 1); E-2 (polo 2); G-3 (filo: VIN dell’amplificatore); A-9 (CE1 +) | cablaggio.md:136 (poli 1-2), :147 (catena LED), :151 (ampli); predisposizioni.md:66 (470 µF) |
| 3V3 | B-3 (filo: +3,3 V ToF posteriore e Qwiic); D-5 (polo 7); G-5 (filo: +3,3 V dei microfoni) | cablaggio.md:139 (polo 7), :150 (microfoni), :153, :154 |
| GND | A-3 (filo: GND ToF posteriore e Qwiic); D-3 (polo 3); D-4 (polo 5); G-4 (filo: massa dei microfoni e dell’ampli); D-6 (polo 9); B-9 (CE1 −) | cablaggio.md:137–140 (poli 3, 5, 9), :147–153 |
| SCL | B-4 (filo: SCL ToF posteriore e Qwiic); E-4 (polo 6) | cablaggio.md:138 (polo 6), :153 (ToF posteriore), :154 (Qwiic) |
| SDA | A-4 (filo: SDA ToF posteriore e Qwiic); E-5 (polo 8) | cablaggio.md:139 (polo 8), :153, :154 |
| DATA | E-3 (polo 4); filo del modulo sul pin E-3: DIN del primo pixel dell’anello | cablaggio.md:137 (polo 4), :147 (catena: anello, lobi) |
| BCLK | E-6 (polo 10); F-6 (ponticello); G-6 (filo: BCLK microfoni (SCK) e ampli) | cablaggio.md:140 (polo 10), :150, :151 |
| WS | D-7 (polo 11); G-8 (filo: WS microfoni e LRC ampli) | cablaggio.md:141 (polo 11), :150, :151 |
| MIC | E-7 (polo 12); F-7 (ponticello); G-7 (filo: SD dei microfoni (R8 al microfono)) | cablaggio.md:141 (polo 12), :150 (dati uniti, pull-down 100 kΩ); decisioni.md:639 (D-074) |
| AMP | D-8 (polo 13); G-9 (filo: DIN dell’amplificatore) | cablaggio.md:142 (polo 13), :151 |
| BTN_A | D-9 (polo 15); filo del modulo sul pin D-9: pulsante, contatto 1 | cablaggio.md:143 (polo 15), :149; BOM.md:45 (B3b) |
| BTN_B | E-9 (polo 16); filo del modulo sul pin E-9: pulsante, contatto 2 | cablaggio.md:143 (polo 16), :149; BOM.md:45 (B3b) |

Il polo 14 (riserva) non è collegato. Il polo 4 porta il dato già a 5 V e dopo il 330 Ω (buffer sulla basetta, `predisposizioni.md` riga 148).

### 2.3 Ponticelli e fili del lato saldature

Ponticelli: D-2–E-2 (5V), D-3–D-4 (GND), E-6–F-6–G-6 (BCLK, F-6 vuoto), E-7–F-7–G-7 (MIC, F-7 vuoto). Fili isolati 101–112 (anche nel disegno):

| N. | Da | A | Rete | Sezione | A cosa serve |
|---|---|---|---|---|---|
| 101 | D-2 | A-9 | 5V | 26 AWG | +5 V → catena LED e CE1 |
| 102 | E-2 | G-3 | 5V | 30 AWG | +5 V → ampli |
| 103 | D-4 | B-9 | GND | 26 AWG | massa → catena LED e CE1 |
| 104 | D-6 | G-4 | GND | 30 AWG | massa → microfoni e ampli |
| 105 | D-4 | D-6 | GND | 30 AWG | massa: polo 9 con i poli 3 e 5 |
| 106 | D-3 | A-3 | GND | 30 AWG | massa → ToF e Qwiic |
| 107 | D-5 | B-3 | 3V3 | 30 AWG | +3,3 V → ToF e Qwiic |
| 108 | D-5 | G-5 | 3V3 | 30 AWG | +3,3 V → microfoni |
| 109 | E-4 | B-4 | SCL | 30 AWG | SCL |
| 110 | E-5 | A-4 | SDA | 30 AWG | SDA |
| 111 | D-7 | G-8 | WS | 30 AWG | WS |
| 112 | D-8 | G-9 | AMP | 30 AWG | dati verso l’ampli |

Fili dei moduli saldati sul pin della testata, dal lato saldature (non c'è un foro libero fuori dalla scatola): DIN dell'anello sul polo 4 (E-3, 30 AWG); i due contatti del pulsante sui poli 15 e 16 (D-9, E-9, 26 AWG). Corrono nei canali fra i fori fino al bordo verso l'ottagono, come nel disegno.

### 2.4 Piazzole dei moduli

| Foro | Rete | Fili dei moduli |
|---|---|---|
| A-3 | massa | ToF posteriore e cavo Qwiic (2 fili) |
| B-3 | +3,3 V | ToF posteriore (VIN a 3,3 V) e cavo Qwiic |
| A-4 | SDA | ToF posteriore e cavo Qwiic |
| B-4 | SCL | ToF posteriore e cavo Qwiic |
| A-9 | +5 V | catena LED (anello, poi lobi), 30 AWG; + di CE1 |
| B-9 | massa | catena LED; − di CE1 |
| E-3 (pin) | dato dei LED | DIN del primo pixel dell'anello |
| D-9, E-9 (pin) | pulsante | i due contatti del pulsante da 12 mm (B3b), 26 AWG circa 9 cm |
| G-3 | +5 V | VIN dell'amplificatore |
| G-4 | massa | microfoni (un filo, vedi sotto) e amplificatore |
| G-5 | +3,3 V | microfoni |
| G-6 | BCLK | microfoni (SCK) e amplificatore (BCLK) |
| G-7 | dati dei microfoni | SD dei due microfoni |
| G-8 | WS | microfoni (WS) e amplificatore (LRC) |
| G-9 | dati verso l'ampli | DIN dell'amplificatore |

- **Microfoni**: i due MS3625 si collegano fra loro (VDD, GND, SCK, WS, SD in parallelo, fili corti), e un solo gruppo di cinque fili arriva a G-4…G-8: così ogni foro ha al più due fili. **R8 da 100 kΩ fra SD e GND sul microfono** da cui parte il gruppo, con guaina. L/R a massa su quello sinistro e a 3,3 V sul destro, sul microfono (`cablaggio.md` riga 150). Prima, la misura di S-21.
- **Amplificatore** MAX98357A: GAIN e SD non collegati (guadagno e canale di fabbrica) [S].
- **ToF posteriore** (X19): l'XSHUT va direttamente a un I/O dell'espansore TCA9534 (X20), non alla scheda (`cablaggio.md` riga 153).
- **Presa Qwiic** (`predisposizioni.md` riga 75): un connettore SMD da 1 mm non si salda sulla millefori. Si usa un cavo Qwiic tagliato a metà (X1, Adafruit 4210): i quattro fili vanno in A-3, B-3, A-4, B-4 e la spina resta libera, raggiungibile dall'ottagono. L'espansore SparkFun (X20) si innesta lì (S-17).
- Fili interni e dei moduli in 30 AWG siliconico (rilievo 13), salvo i 26 AWG della tabella e del pulsante.

### 2.5 Ordine di saldatura

1. Taglia l'avanzo a 20 × 30 con le righe e le colonne di sopra; allarga a Ø 2,6 i quattro fori d'angolo. Segna le croci: sono le zone che appoggiano sulle bugne.
2. CE1 sdraiato (lato componenti), + in A-9. Se è lungo 11 mm, prima infila e salda i fili dei moduli in A-4 e B-4: il fondo del condensatore arriva a 0,4 mm da quei fori (S-18).
3. J2 (dopo la decisione di S-01), tacca verso la colonna D.
4. Lato saldature: ponticelli D-2–E-2, D-3–D-4, E-6…G-6, E-7…G-7; poi i fili 101–112.
5. Fili dei moduli (13.16), dal lato componenti, uno alla volta con la prova di continuità; DIN e pulsante sui pin E-3, D-9, E-9 dal lato saldature.
6. R8 al microfono, nel fascio, con la guaina.

### 2.6 Prove con il multimetro, prima di collegare la spina

| N. | Punto | Atteso | Se no |
|---|---|---|---|
| 1 | polo 1 (D-2) contro polo 3 (D-3) | non 0 Ω; sale mentre CE1 si carica | corto sul 5 V: fa scattare PTC1 |
| 2 | polo 7 (D-5) contro poli 3, 5, 9 | non 0 Ω | corto sul 3,3 V dei sensori |
| 3 | polo 1 contro polo 7 | aperto | 5 V sul 3,3 V: brucia i sensori e l'ESP32 |
| 4 | poli 1 e 4 (5 V, dato) contro poli 6, 8, 10, 11, 12, 13 | aperto | 5 V su un GPIO |
| 5 | poli 15 e 16 contro tutti gli altri | aperto; fra loro: aperto a riposo, chiuso a pulsante premuto | pulsante normalmente chiuso o filo sbagliato |
| 6 | polo 12 (E-7) contro massa, con i microfoni collegati | 100 kΩ (R8) | R8 mancante |
| 7 | polo 14 (E-8) contro tutti | aperto | |
| 8 | ogni filo 101–112 dal polo alla piazzola, e ogni piazzola al pin del suo modulo | 0 Ω | |
| 9 | i fori con la croce, sul lato saldature | nessuno stagno, nessun filo sopra | la scheda non appoggia sulle bugne |

### 2.7 Scelte e perché

1. **Testata con chiave** come nel BOM, non un pin header senza scatola: girata di 180° la spina porterebbe il +5 V dei poli 1–2 sui poli 15–16 (pulsante della 2813).
2. **Fili dei moduli a due per foro**: tolte le zone delle bugne, la scatola della testata e CE1, restano 13 fori per i moduli; i microfoni si uniscono fra loro e il ToF condivide i fori con il cavo Qwiic. Il dato dei LED e il pulsante vanno sul pin della testata.
3. **R8 al microfono**: sul lato saldature stava sopra i giunti di G-7 e G-8, in 3,5 mm d'aria (rilievo 13).
4. **Pulsante sui poli 15 e 16**, lontano dal 5 V: con la tensione dei pin A e B della 2813 ignota (S-10) si controlla prima di collegare.
5. **CE1 sul +5 V dopo il PTC**, come `predisposizioni.md` riga 66: smorza i picchi della catena LED vicino alla catena.
6. **Alimentazione dell'ampli dai poli 1–2** con un 30 AWG (fino a circa 200 mA, `predisposizioni.md` 4.3); i LED con il 26 AWG (fino a 600 mA).


## 3. Cosa cambia nei passi già scritti

Da riportare nei passi (F3c), con il riferimento a questi disegni (`figura: schemi/basetta.svg` e gli altri):

| Passo | Oggi | Con lo schema |
|---|---|---|
| 4.03 | misura del pin 5V con la sola USB; sigla RE1.3 | in più: **nessuna microSD nella scheda**; a scheda spenta, resistenza fra GPIO40 e 3V3 (pull-up della microSD, S-21); serigrafia di 5V, GND, 3V3 accanto ai pin (S-15) |
| 4.04 | strip a 24,7 mm [C]; "connettore a 3 poli" per la seriale; 100 kΩ su GPIO41 sulla basetta; 47 kΩ e 1N4148 sulla basetta | strip a 25,4 mm (10 passi) dopo la misura di S-02; solo i pin usati saldati; teste M3 basse o CAD (S-19); seriale con tre Dupont (E-3, F-3, H-3); la 100 kΩ si salda sulla 2813, R6 pure (S-20); D2 e R3 non sono sulla basetta |
| 4.05 | buffer e PTC senza posto; pull-up senza valore; un canale del buffer | U3 con due canali, PTC1 su Kapton sopra U3, R4 e R5 da 4,7 kΩ; fili delle tibie saldati qui (K-13, B-13, T-13 con R9 in linea) |
| 4.06 | disposizione assente; presa Qwiic; 100 kΩ sul polo 12 | `scheda_carapace.svg`, dopo S-01; fori d'angolo a Ø 2,6; cavo Qwiic tagliato in A-3…B-4; R8 al microfono; DIN e pulsante sui pin |
| 4.07 | il D24V22F5 sciolto con i Dupont | prima accensione **senza ESP32**, misure di 1.5 nelle prese |
| 4.08 | "uscita del D24V22F5 5,0 V"; LED dell'ESP32 acceso | 5,0 V su R-4; sul pin 5V 4,55–4,7 V con l'ESP32 (D1); ESP32 inserito solo dopo la prima accensione |
| 4.03, 4.08 (avviso) | "Mai la USB con l'ESP32 alimentata dal pin 5V" | con D1 il regolatore non riceve più la USB; resta da sapere se la porta USB riceve il 5 V del pin (S-07): una alimentazione alla volta finché 4.03 non lo dice |
| 4.12 | prova con un regolatore e il 47 kΩ sulla basetta | prova di ogni regolatore con la sua R3 (22 kΩ) fra ENA e GND e il D2 in linea; ENB libero (S-05, S-20) |
| P2 (misura RMT) | "canale libero del traslatore" | Dupont sull'ingresso H4 (I-4) e filo provvisorio I-7 → L-12 (1.6) |
| 8.18 | due fili 26 AWG dalla 2813 alla basetta, saldati sulla basetta | VBAT, massa (S-13), partitore (R-13) e OFF (Q-13) sono già sulla basetta: si saldano sulla 2813, con R6 sull'uscita e la 100 kΩ fra OFF e massa |
| 8.19 | EN e OFF saldati sulla basetta; "pad EN" | il filo GPIO42 (P-13) con D2 in linea arriva al pin **ENA** di ogni D42V110F6; R3 fra ENA e GND su ogni regolatore; ENB libero |
| 8.20 | tre fili saldati sul "connettore di prova" | i tre fili (E-3, F-3, H-3) sono già sulla basetta: si infilano le Dupont. Vedi S-22 per la massa |
| 8.21, 8.22 | "ramo del bus della basetta" | riga 1: un ramo per foro di ogni gruppo (1.6); IMU e ADC nello stesso foro |
| 8.23 | poli 15–16 sulla basetta | poli 15–16 separati dal cavo e giuntati ai fili verso A e B della 2813 |
| 8.25 | tre fili dalla basetta alle prese delle luci, saldati sulla basetta nel robot | già saldati al banco: si saldano sulle prese. R9 in linea sul dato; condensatore delle prese: S-23 |
| 8.28 | SDA e SCL contro 3,3 V: 1,0–1,4 kΩ | valore atteso con tutti i moduli (S-13); prima, a basetta sola, 4,7 kΩ (prova 11 di 1.5) |
| 13.16 | 5 fili per microfono, presa Qwiic | microfoni uniti fra loro con R8 al microfono; cavo Qwiic tagliato in A-3…B-4; DIN e pulsante sui pin della testata; tabella 2.4 |


## 4. Rilievi della verifica elettrica applicati

| Rilievo | Cosa è cambiato |
|---|---|
| 1, bloccante, teste M3 | zone vietate in 1.0 e nel disegno; poli 1–2 spostati in A-13, B-13; massa del bus fuori da C-1, D-1; il +5 V delle tibie non sta più in U-13; nessun filo sopra le teste (i vecchi 14 e 44 sono rifatti). Restano T-2, D-12, B-2: S-19 |
| 2, bloccante, colonnine | zone Ø 7 sul lato saldature; nessun filo né giunto sopra le colonnine; VBAT non entra più da B-9; i fili della seriale non passano più vicino a (29; ±6,8) |
| 3, rete EN | D2 e R3 non stanno più sulla basetta (S-20); prova 13 su GPIO42 e i suoi vicini |
| 4, prove sulle piazzole vicine | prova 5 generale per le righe 1, 3, 11 e 13, con l'elenco delle coppie critiche; pin non usati non saldati |
| 5, prima accensione | prima accensione senza ESP32 con le misure nelle prese (1.5) |
| 6, VBAT | un filo solo, lungo il bordo, posato per ultimo, nessun filo vicino a P-4; frase corretta in 1.2 |
| 7, masse | stella su Q-4/Q-5/Q-6 con fili separati per ingresso, LED e logica (scelta 8) |
| 8, ramo delle tibie | secondo canale del buffer con R9 in linea (scelta 2) |
| 9, PTC | Kapton (S-24); PTC in linea resta l'alternativa di S-08 |
| 10, pin di U4 | pin tagliati a filo sopra e sotto; niente sotto il modulo |
| 11, microfoni e microSD | S-21; avviso in 4.03 |
| 12, bugne della scheda | zone e fori vietati; masse e 3,3 V spostati in A-3, B-3, G-4, G-5 |
| 13, lato saldature della scheda | R8 al microfono; fili in 30 AWG; 12 fili invece di 18 |
| 14, S-15 | testo corretto: con la piedinatura vista dal retro il 5 V e la massa si scambiano |
| 15, ENA | "ENA, ENB libero" in 1.6, 3 e S-05 |
| 16, prova 2 | R6 non è più sulla basetta: VBAT contro ogni presa è aperto, salvo A-12 (prova 1) |
| 17, fori del carapace | Ø 2,6 |
| 18, disegni | fili disegnati nei canali, affiancati dove condividono un canale; etichette lontane dai fori e fra loro |
| 19, doppia massa con la SSC-32 | S-22 |
| 20, passi | righe di 4.03, 4.06, 4.07, 4.08 nella sezione 3 |
| 21, sezione dei fili | colonna "Sezione" nelle tabelle 1.3 e 2.3 |
| 22, misura RMT | filo provvisorio I-7 → L-12 (1.6) |
| 23, chiave di J2 | letta sul disegno Würth della spina: tacca dal lato dei poli dispari (S-26) |
| 24, condensatore delle tibie | S-23, proposta |

In più, rileggendo la pagina Pololu 5673 per il rilievo 15: ENB è tirato a VIN con 1 MΩ ed è collegato a ENA con 10 kΩ, quindi ogni D42V110F6 tira ENA verso VIN con circa 500 kΩ, non 1 MΩ. I numeri di S-05 sono rifatti.


## 5. Rilievi non applicati

- **Rilievo 3, seconda parte** ("spostare D2 e R3 fuori da sotto il traslatore"): applicato in un altro modo. Sulla basetta non c'è un posto per l'abilitazione che non confini con una rete alta a riposo (sotto il traslatore, le righe 3 e 11 accanto agli strip, la coda accanto alla seriale); D2 va in linea e le R3 sui regolatori (S-20). Le prove proposte "EN (A-10) contro A-4, A-5, F-7 e D-12" e "I-5 contro E-4 e I-4" non servono più: quei fori non portano più l'abilitazione.
- **Rilievo 10, seconda parte** ("controllare a secco con D2 e R3 sotto il modulo"): non serve, sotto U4 non c'è più niente. Resta la prova a secco di tutto l'insieme (1.4, passo 2).
- **Rilievo 20, seconda parte** ("con D1 USB e pin 5V insieme non sono più un rischio"): vero per il regolatore, non ancora per la porta USB del Mac, che potrebbe ricevere il 5 V del pin se la scheda non ha un diodo sulla USB (S-07). L'avviso resta, con il motivo cambiato.
- **Rilievo 1, "code degli strip tagliate a filo e Kapton sulle teste"** come correzione sufficiente: non basta. Con 0,3 mm di luce non sta nemmeno una saldatura piatta su T-2 e D-12, che servono. Resta una delle soluzioni di S-19.
