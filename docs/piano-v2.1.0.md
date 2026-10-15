# Versione 2.1.0 — piano di progettazione

Stato: **fatto** (9–10 ottobre 2026, D-066, tag `v2.1.0`; avanzamento e risultati in `docs/versioni.md` e `docs/decisioni.md`). Questo file serve a riprendere il lavoro dopo una compattazione del contesto o una sessione nuova: da qui si sa cosa fare, in che ordine e come verificarlo.

## Cos'è la 2.1.0

- **v2.0.0** è il robot com'è oggi: commit `5a3a0fc` (più i commit di questo piano), design Fusion "Hexapod v2 - MG996R" all'ultima versione salvata il 9 ottobre 2026. Comprende zampa, corpo, passata estetica e tibia simmetrica sul piano della zampa (D-047…D-065).
- **v2.1.0** aggiunge le **predisposizioni** per sensori, luci, audio e computer di bordo, gli **attrezzi da banco** e il **software senza hardware (S0)**. È la fase P0 di `docs/piano-elettronica-software.md`. Non si compra niente: le voci nuove del BOM restano da approvare.

## Come si lavora (file e versioni)

Primo passo, al via dell'utente:
1. **Git**: tag `v2.0.0` sull'ultimo commit prima delle modifiche, con push del tag. Si lavora su `main` come sempre: progetto personale, commit e push a fine di ogni blocco.
2. **Fusion**: si copia "Hexapod v2 - MG996R" nel progetto "Hexabot v2" con `DataFile.copy`, e la copia si rinomina **"Hexapod v2.1.0"**. Il file vecchio resta la v2.0 congelata: va aggiunto in `CLAUDE.md` ai file da non modificare, con il lineage. Il lineage della copia va scritto in `CLAUDE.md` come nuovo design di lavoro.
3. **Script**: il controllo sul nome del documento oggi è `startswith('Hexapod v2 - MG996R')`, in `corpo.py`, `zampa.py`, `assieme.py` e `NOME_DESIGN` di `rif_componenti.py`. Va portato a una sola costante con il nome della 2.1.0 ("Hexapod v2.1.0"). Così gli script si rifiutano di girare sulla v2.0 per errore. Lo stesso vale per `viste.py`, `colori.py`, `esporta_*.py` e `esploso`, se lo usano.
4. **Storico delle versioni**: file nuovo `docs/versioni.md`, una riga per versione, con il tag git e il file Fusion. A fine lavoro: tag `v2.1.0` e una decisione riassuntiva in `docs/decisioni.md`.

## Decisioni dell'utente (9 ottobre 2026)

- **Audio a bordo**: si rinuncia alla microSD dell'ESP32. Microfoni I2S e altoparlante (MAX98357A) usano i GPIO 38/39/40/2; altoparlante in coda, con il suono dalla porta di servizio.
- **Computer di bordo**: solo **predisposizione a zaino sul dorso**, cioè una sella con 4 fori sul carapace per un modulo esterno (Radxa ZERO 3W o simile). Niente vano interno. Non si compra.
- **Software approvato**: l'ESP32 è autonomo, il Mac è facoltativo, il computer di bordo è solo predisposto. Firmware in ESP-IDF e C++ senza Arduino. Si può installare sul Mac il software libero (ESP-IDF, MuJoCo, Python con pytest e ruff, Node.js, Rerun…). La repo resta pubblica, con le credenziali fuori.
- **Luci**: predisposizione per l'anello del pulsante e per la luce dei lobi. In più, **predisposizione per le luci nelle tibie**: se montarle o no lo decide l'utente dopo, in base ai componenti e alla difficoltà di montaggio, quindi niente nel guscio approvato deve cambiare in modo irreversibile. Fessure dell'occhio e linee della fascia restano fuori finché l'utente non le chiede.
- **Non ora**: LIDAR, termocamera e le altre voci basse.
- Materiali (D-065): PETG-CF nero per le parti funzionali, PLA per le placche (bianco per ora), TPU arancio per i piedini.

## Blocco A — Zampa (`cad/script/zampa.py`)

1. **Punta dello stinco per il sensore di forza (FSR 400 Short, voce X5)**, solo in `fai_tibia` e non in `_stinco`:
   - parametro nuovo per la fine dello stinco, circa 107,6 (oggi 108,4);
   - `tib_x_piu_basso` da 4 a circa 6, così la parte piana è circa 8,4 per la testa Ø7,6; `tib_arco_R` passa da circa 262 a circa 341;
   - punta piana con lo spigolo +X raccordato R 1; lato −X invariato (a γ minimo passa a 0,03 mm dalla coxa);
   - tasca 6 × 9 × 1,2 per linguette e saldature, sulla faccia +X dentro il piedino;
   - gola 2 × 2 per i fili a Y circa +5, dal piedino fino al fondo della culla (z circa −33), non oltre: la parete della culla è di 2 mm.
2. **Piedino** (`fai_piedino`): nasce da uno stinco con la punta nuova ma lungo 108,4, così restano la cavità di 0,8 (FSR 0,3 + pistoncino 0,5) e la suola a 110. Pistoncino Ø4,5 × 0,5; tacca 2 × 2 per i fili sul bordo alto lato +X; esterno raccordato a parte.
3. **Luci nelle tibie (predisposizione, X31)** senza toccare il guscio approvato:
   - sulla faccia +X dello stinco, sotto la finestra lunga del guscio (7 × 48, centrata su Y 0), una sede piatta per un tratto di striscia WS2812B-2020 (larga 4–5 mm). Fra stinco e fronte del guscio ci sono 3,1–5,7 mm d'aria: da verificare con la striscia e i suoi fili;
   - un diffusore separato `Cover_Tibia_Diffusore` in PLA bianco da 0,6 mm che chiude la finestra da dentro a incastro. Si monta solo se si mettono le luci; senza, la finestra resta aperta come oggi;
   - percorso dei 3 fili della striscia insieme a quelli dell'FSR (gola, fascette esistenti). Da ricontrollare la scorta dei cavi ai giunti con `calc/cavi_servo.py`;
   - massa da contare: circa 2 g a zampa.
4. **Guscio** (`fai_cover_tibia`): inserto e bossolo della vite seguono l'arco nuovo; tacca 3 × 2 solo se il bordo schiaccia i fili.
5. **Punti con nome** per il software (punta del piede, assi dei giunti) e **facce di riferimento** per le dime su coxa, femori e tibia.
6. **Verifiche**:
   - zampa: `giunti`, `limiti`, `misura`, `interferenze`; scansione delle 54 pose con i 20 controlli (17 toccano, come oggi); suola a 110;
   - assieme: `interferenze`, zampe vicine libere a 31° e a contatto a 32°, `carapace_zampe`, `ciclo` 100/45 e 70/70.

## Blocco B — Corpo (`corpo.py`, `assieme.py`, `rif_componenti.py`)

1. **Ingombri nuovi in libreria** (`rif_componenti.py` → `ingombri`), con le pose in `assieme.py` → `pose_corpo`:
   - sensori: IMU Pololu #2798, ToF 8 × 8 Pololu #3418, ToF semplice #3415, ADS7830;
   - correnti e alimentazione: INA260, D24V5F3;
   - scheda del carapace con spina IDC;
   - audio: MAX98357A, altoparlante, due microfoni;
   - FSR; Radxa ZERO 3W per lo zaino.

   Quote nella sezione 5 del piano unico.
2. **Prima: posto della scheda 2813** (interruttore B3, oggi senza posto). Decide se il tetto del tunnel sotto il vassoio resta libero per IMU e ADS7830.
3. **IMU e ADS7830** sul tetto del tunnel sotto il vassoio: bugne Ø5,5 con inserti M2, freccia dell'asse X stampata. In più asola 6 × 3 nel vassoio e clip per il bus fra SSC-32 e vassoio.
4. **Visiera e vassoio**: finestra del ToF frontale sotto l'occhio (piramide sul campo 60° × 60° inclinata di 20° in basso, più 0,8; tappo nero finché il sensore manca). La mensola della camera diventa la sede del ToF; fermo della testa della camera. Da verificare l'interferenza con la bugna dell'occhio e il `campo` della camera.
5. **Carapace e fascia**:
   - anello di stato attorno al pulsante (x −40), con la camera nera di diametro 28 o meno per non urtare altro;
   - sedi 5 × 22 × 0,6 della luce nei lobi, con i ganci; ganci passacavo della striscia fuori dalla battuta dello sportellino e dai pozzetti;
   - sella dello zaino: 4 fori M2,5 a 58 × 23 e un passaggio per un USB-C, fuori dall'ottagono, dai pozzetti e dalle luci;
   - audio: altoparlante su una guancia di coda, ToF posteriore sull'altra (da verificare: T-plug e spinotto raggiungibili); fori dei microfoni con anello per la guarnizione;
   - scheda del carapace con la spina che si sfila dall'ottagono, e amplificatore: posto da trovare, prima da guardare la zona x 29…50, |y| ≤ 16, sopra l'ESP32 e prima dell'antenna (x 55,6). Se il posto non c'è, si scrive.
6. **Slitte dei regolatori** prolungate per l'INA260, se passano sotto smusso, gonne e cavi; altrimenti scheda in linea sul 16 AWG.
7. **Posti ancora da trovare** (prese dei piedi, INA3221, spie dei rail): si cercano. Dove non si dimostrano, restano "posto da trovare" nel piano unico.
8. **Verifiche**: `interferenze`, `sfilamento`, `campo`, `carapace_zampe`, coxe ±35, zampe vicine, cicli; timeline senza avvisi; volumi delle altre parti invariati.

## Blocco C — Attrezzi da banco (script nuovo `cad/script/attrezzi.py`)

- Dime di taratura generate dai parametri: coxa 0° e +30°, femore 0° e +45°, ginocchio 90° e 135°.
- Cavalletto che regge il corpo sotto la chiglia con le zampe libere su tutta l'escursione.
- Componenti nella zona libreria del design (y ≥ 250, spenti), STL in `cad/stl/attrezzi/`.

## Blocco D — Software S0 (con agenti, in parallelo al CAD; senza toccare `cad/` e `calc/`)

- `cad/script/esporta_robot.py`: legge da Fusion in sola lettura (ogni chiamata sotto i 40 s) e genera `robot.yaml`, la descrizione unica del robot: geometria, limiti, tabella del ginocchio minimo, masse, punti con nome.
- `firmware/`: progetto ESP-IDF per esp32s3. Il nucleo C++ (cinematica, guardia dei limiti, andature) si compila anche sul Mac per i test.
- `sim/`: modello MuJoCo generato da `robot.yaml`, tripode in simulazione.
- `tools/` e `app/`: gemello digitale nel browser (three.js) che mostra le pose.
- CI su GitHub Actions: test Python e C++, build del firmware.
- Da riusare: `calc/statica_tripode.py` (`ik_piano`), `assieme.py` → `pose_tripode`, `GAMMA_MIN` di `zampa.py`.
- Dettaglio dell'architettura in `docs/software.md`; i limiti della guardia vanno corretti come in quel file (somma d'imbardata tra vicine 56°, soglia d'inclinazione per assetto, 250°/s per giunto).

## Documenti a fine lavoro

- `docs/decisioni.md`: D-066 con le decisioni di oggi e il riassunto della 2.1.0.
- `docs/BOM.md`: le voci X come candidati da approvare.
- `docs/progetto-meccanico.md`, `docs/piano-elettronica-software.md` (stato di P0), `docs/versioni.md`, `CLAUDE.md` (stato, design di lavoro, prossimi passi).
- STL (`esporta_stl.py`) e render (`viste.py`, `cad/render/ritaglia.py`) aggiornati.
- Commit e push a fine di ogni blocco; Fusion salvato dopo ogni blocco.

## Ordine e punti di arresto

Copia del file Fusion e tag git, poi A, B, C. D gira con agenti in parallelo dal blocco A in poi; `esporta_robot.py` lo lancio io, perché usa Fusion. Mi fermo solo per scelte che spettano all'utente, per esempio quando un posto non c'è e serve rinunciare a una voce.

## Come riprendere dopo una compattazione o una sessione nuova

1. Leggere `CLAUDE.md`, poi questo file, poi la sezione 5 (CAD) e la 2.3 (GPIO) di `docs/piano-elettronica-software.md`.
2. Controllare che ci siano gli strumenti del connettore Fusion e quale file è aperto: la v2.1.0, non la v2.0.
3. `git log --oneline -5` e `docs/versioni.md` dicono a che blocco si è arrivati.

## Seguito: tre correzioni (versione 2.1.1, chieste dall'utente il 10 ottobre 2026)

**Fatta il 10 ottobre 2026** (D-067, tag `v2.1.1`): camera Ø32 × 6 con il fondo e due sedi da un pixel, fermo dei fili sulla culla della tibia, `cablaggio.md`. In più la striscia LED, poi corretta in D-068: WS2812B-2020 a 120 LED/m, due pixel per sede.

Sullo stesso design "Hexapod v2.1.0" (correzioni piccole: niente copia del file Fusion), tag `v2.1.1` a fine lavoro, decisione D-067.

1. **Camera nera dell'anello del pulsante da Ø28 a Ø32** (`luc_camera_D`).
   - Con Ø28 fra il dado del pulsante (r 8,65) e la parete (r 12,8) restano 4 mm e un pezzo di striscia WS2812B-2020 largo 5 non entra. Il limite di 28 veniva dai canali delle linee della fascia (X22), che non si fanno.
   - Aggiungere la **sede dei due pixel**: un fondo o una piastrina che chiude la camera in basso, con il pezzo di striscia incollato rivolto verso l'anello, e la tacca per i fili verso la coda.
   - Ricontrollare pozzetti (−56, ±22,5), battuta dello sportellino, SSC-32 e cavi dei servo sotto (z ≤ 25), sfilamento del carapace.
2. **Fermo dei fili della tibia** (FSR: 2 fili; LED: 3 fili da 30 AWG) sulla parete +X della culla della tibia, sotto il guscio: oggi dalla gola in su e dalla cima della striscia corrono nell'aria fino alla cima del guscio.
   - Un gancio o una scanalatura poco profonda (≤ 0,8, la parete è di 2), fuori dalle finestre a rombo e dai tappi del guscio.
   - Poi le verifiche della zampa (interferenze, scansione, cicli).
3. **Schema del cablaggio**: documento nuovo `docs/cablaggio.md`, con uno schema e una tabella.
   - Per ogni cavo: da dove a dove, percorso (giunti attraversati, fascette, ganci), connettore, numero di fili e sezione.
   - Cavi da coprire: servo, FSR, LED delle tibie, catena LED del carapace (anello, lobi) attraverso la scheda del carapace con la spina IDC, bus I2C dei sensori, ToF, microfoni e amplificatore, INA260, spie, alimentazione.
   - Partire da `docs/piano-elettronica-software.md` (sezioni 2.1–2.5), `docs/predisposizioni.md`, `calc/cavi_servo.py` e D-066.

## Seguito: versione 2.1.2 — scelta delle predisposizioni (approvata dall'utente il 10 ottobre 2026)

**Fatta il 10 ottobre 2026** (D-069, tag `v2.1.2`).

Sullo stesso design "Hexapod v2.1.0", tag `v2.1.2`, decisione D-069. L'utente ha approvato la classificazione delle voci X in sei classi (importante, good-to-have, superfluo; ha posto o no).

- **Confermate come predisposizione**:
  - sensori e loro infrastruttura: X1, X2, X3, X4, X5, X6, X7, X8, X14 (2 NTC), X19, X20, X23, X24;
  - luci: X9, X10, X11, X12, X13, X31;
  - audio: X16, X17;
  - computer di bordo a zaino.
- **Backlog, senza predisposizione**: X15, X18, X21, X22, X25, X26, X27, X28, X29, X30, X32, X33.
- **Tocco senza sensore nuovo**: colpetto e doppio colpetto dall'IMU, pressione localizzata dal centro di pressione degli FSR, molleggio con controllo di ammettenza, passo di recupero. Va in `software.md`; il tocco capacitivo X18 resta in backlog.

Lavori:
1. **Prese delle luci delle tibie**: seconda fila di 6 spine JR, speculare a quella dei piedi sul lato −Y del tetto del tunnel. Va verificato il posto: IMU, cavi e asola.
2. **Presa di T-plug e spinotto con il ToF posteriore montato**: ingombro di due dita nella porta di coda e controllo delle interferenze. Se non passa, il ToF si sposta sopra il piano del T-plug.
3. **Provino di luce** (X10): piastrina 60 × 40 in `attrezzi.py`, con:
   - gradini di bianco da 0,4 a 1,6;
   - intarsio nero da 0,6;
   - camere nere da 2, 4 e 6;
   - anello e fessura;
   - sedi per 3 pixel.
   STL in `cad/stl/attrezzi/`.
4. **Documenti**: D-069; classificazione in `predisposizioni.md`, nel piano elettronico, nella sezione X del BOM e in `CLAUDE.md`; NTC da 3 a 2; tocco dai sensori esistenti in `software.md`.
5. **Chiusura**: verifiche, salvataggio in Fusion, STL, esportazione del robot, commit, tag `v2.1.2`.

## Seguito: versione 2.1.3 — lame del femore come la tibia (scelta dell'utente dell'11 ottobre 2026)

**Fatta l'11 ottobre 2026** (D-070, tag `v2.1.3`). Verificato in CAD: contatto fra vicine a 31° (libere a 30,5°, gioco a 30° di 3,58 mm), carapace a 3,96 mm. Massa attesa 3060,6 g, con il femore al 53 % dello stallo.

Sullo stesso design "Hexapod v2.1.0", tag `v2.1.3`, decisione D-070. Concept e verifiche sulle mesh in `docs/ricerca/estetica/8-placca-femore/` (`concept3.py`, `concept4.py`, `confronto_strisce.png`).

Scelte dell'utente:
- lame laterali nello stile del guscio della tibia: faccia piana, smussi tutt'attorno, chiuse anche sulle teste dei bulloni e sui mozzi;
- con la feritoia;
- **nessuna copertura superiore**. Scartate: finestra larga, cappucci, strisce da lama a lama, linguetta sull'anca.

Geometria (dalle verifiche sulle mesh; si riverifica in CAD):
- **Sagoma**:
  - da X 40 a 135,5 (anca a 55, ginocchio a 120), da Z −14,5 a 20;
  - verso l'anca si stringe con due smussi, (48; 20)–(40; 12) in alto e (40; −3,5)–(52; −14,5) in basso; sotto il ginocchio uno smusso (129; −14,5)–(135,5; −8);
  - il bordo alto resta dritto a Z 20. Un bordo che sale verso il ginocchio porta la lama a 1,4 mm dal carapace con α 85 e coxa a ±35.
- **Faccia esterna** piana, con lo smusso 3 × 2 tutt'attorno: 3 in pianta, 2 nello spessore.
- **Lama A**:
  - da \|y\| 30,6 a 34,6, quindi 4,0 di spessore;
  - tasche cieche per le 12 teste M3: teste da 3,0, 0,2 di gioco, pelle 0,8;
  - si incastra sulle 4 teste del blocco con tasche Ø5,6 (`cov_testa_d`, come oggi); le 8 teste delle squadrette stanno in tasche libere Ø6,2.
- **Lama B**:
  - da 30,6 a 33,2: 2,6 di spessore, come oggi;
  - tasche per le punte dei perni (sporgono 1,4; la tasca è profonda 1,7);
  - restano le due viti M2 svasate a X 81 e 94,5, Z 6 (D-065).
- **Feritoia**:
  - intarsio di PLA nero a filo della faccia, profondo 0,6 come la fascia del carapace (D-063);
  - 37 × 7 con gli estremi tondi, centrata fra gli assi (X 87,5) e all'altezza delle viti della lama B (Z 6);
  - sul lato A copre le tasche delle due teste basse del blocco; sul lato B le viti nere stanno dentro l'intarsio nero;
  - componenti nuovi `Cover_Femore_A_Feritoia` e `Cover_Femore_B_Feritoia`, stampati insieme alla lama (PLA su PLA).
- **Stampa**: faccia interna sul piatto. Le tasche sono fori ciechi che partono dal piatto; la faccia esterna e l'intarsio stanno in cima.
- **Stime sulle mesh**:
  - contatto fra zampe vicine a 30,75° (oggi 31,25°); gioco a 30° di 3,5 mm (oggi 4,6). Il firmware resta a 30° per zampa e 60° di somma;
  - distanza dal carapace con α 85 e coxa a ±35: 4,0–4,8 mm (oggi 4,6).
- **Dime di posa**: si usano con la lama B smontata, come oggi.

Lavori:
1. **`zampa.py`**:
   - parametri `cov_fem_*` nuovi;
   - `_cover_femore` riscritta, più `fai_cover_femore_feritoia` per i due intarsi;
   - tolti i parametri delle lame bombate che non servono più (bombatura, esagoni, plateau, finestre).
2. **Rifare nel CAD**:
   - `Cover_Femore_A` e `_B`, poi i due intarsi con le istanze e i giunti rigidi nella zampa montata;
   - controllo delle trasformate e dei volumi delle altre parti (sentinella).
3. **Verifiche**:
   - zampa: interferenze, scansione delle pose (le 81 libere e i controlli), misura;
   - assieme:
     - interferenze;
     - coxe a ±35;
     - zampe vicine libere a 30°, con il contatto atteso fra 30,5° e 31°;
     - carapace contro le zampe con (85, 90), (85, 29) e (60, 90), a imbardata −35, 0 e +35;
     - cicli 100/45 e 70/70, rotazione a 30°;
   - massa delle lame.
4. **A valle**:
   - `colori.py`: intarsi in PLA nero;
   - `esporta_stl.py` e `cad/stl/README.md`: orientamento e materiali;
   - `viste.py` (esploso), `esporta_robot.py` (geometria, mesh, pose), `tools/descrizione.py --aggiorna-hash`, `genera_header.py`, `genera_vettori.py`, `genera_modelli.py`;
   - mesh del renderer e render della zampa in `docs/immagini/`.
5. **Documenti**:
   - D-070 in `decisioni.md`;
   - `versioni.md`;
   - `progetto-meccanico.md` (lame del femore e contatto fra vicine);
   - `CLAUDE.md`: stato, e la placca superiore del femore tolta dal backlog perché scartata;
   - `software.md`, se cambia il margine del contatto fra vicine.
6. **Chiusura**: `versione.py` a 2.1.3, salvataggio in Fusion, commit, tag `v2.1.3`, CI verde.

## Seguito: versione 2.1.4 — lame del femore che seguono la sagoma del femore (richiesta dell'utente dell'11 ottobre 2026)

**Fatta l'11 ottobre 2026** (D-071, tag `v2.1.4`). In più, su richiesta dell'utente, la feritoia è scesa a Z 1,5, con le viti della lama B (quella lato ginocchio a X 89). Verificato in CAD: contatto fra vicine a 31°, carapace a 4,58 mm, massa attesa 3043,5 g.

Sullo stesso design "Hexapod v2.1.0", tag `v2.1.4`, decisione D-071.

**Richiesta dell'utente**: le lame della 2.1.3 escono troppo dalla forma del femore e "sembrano una placca buttata lì". Vuole la sagoma che aderisce al femore come le lame bombate di prima (D-061), con l'estetica nuova.

**Lavori**:
- **Sagoma** come le lame di D-061:
  - fascia fra i mozzi a Z ±14,5;
  - teste esagonali con l'apotema 14,5 attorno ad anca e ginocchio (teste del femore R13);
  - rialzo sopra il blocco fino a Z 20, con le rampe a 30° verso l'anca e a 45° verso il ginocchio.
  - Il rialzo va da X 80 a 97, prima da 81 a 96: così le tasche delle teste alte del blocco restano sotto la faccia piana, non nello smusso.
  - Niente raccordi in pianta: spigoli vivi e smussati, come le sfaccettature della tibia.
- **Come la 2.1.3** (D-070):
  - faccia piana con lo smusso 3 × 2;
  - lama A spessa 4,0 con le 12 tasche, lama B spessa 2,6 con le tasche dei perni e le due viti M2;
  - feritoia a intarsio nero a X 87,5, Z 6.
- **Parametri**: tolti `cov_fem_x0`, `x1`, `giu`, `anca_*` e `gin_giu`; nuovi `cov_fem_ap`, `cov_fem_plateau0` e `cov_fem_plateau1`.

**Verifiche e chiusura**, come nella 2.1.3:
- sentinella dei volumi;
- zampa: interferenze e scansione;
- assieme: coxe a ±35, vicine a 30, 30,5 e 31°, carapace, cicli e rotazione;
- colori, STL, esportazione del robot e generatori, mesh del renderer, render delle zampe;
- documenti, salvataggio in Fusion, tag `v2.1.4`, CI.

## Seguito: versione 2.1.5 — provino delle tasche della lama A e render notturno (richiesta dell'utente dell'11 ottobre 2026)

**Fatta l'11 ottobre 2026** (D-072, tag `v2.1.5`).

Sullo stesso design "Hexapod v2.1.0", tag `v2.1.5`, decisione D-072. Il modello del robot non cambia.

1. **Provino delle tasche** (`attrezzi.py` → `provino_tasche`), da stampare con gli altri provini prima dei pezzi.
   - Serve a tarare l'incastro della lama A sulle teste M3 del blocco (`cov_testa_d`, oggi 5,6, D-063).
   - **Base** in PETG-CF: blocchetto con un foro passante per una vite M3 × 6 ISO 4762 e la trappola del dado sotto; viti e dadi dal kit D6/D7.
   - **Lamina** in PLA bianco, spessa come la lama A (4,0), stampata come la lama con le tasche sul piatto:
     - sei tasche profonde 3,2;
     - quattro lisce da Ø5,4, 5,5, 5,6 e 5,7;
     - due da Ø6,0 con tre costole di schiacciamento, che stringono a Ø5,3 e 5,4;
     - da 1 a 6 puntini accanto a ogni tasca per riconoscerla.
   - Si preme ogni tasca sulla testa e si sceglie quella che tiene senza forzare troppo. Il valore va in `cov_testa_d`, oppure si passa alle costole.
   - STL in `cad/stl/attrezzi/`.
2. **Render notturno** (`viste.py` → scena `notte`), accanto ai render normali.
   - Ambiente scuro, luci accese con aspetti emissivi messi solo per il render e tolti da `ripristina`: anello del pulsante, luci dei lobi, diffusori delle tibie, spie dei rail.
   - Una o due inquadrature in `docs/immagini/render-notte-*.png`.
   - Il colore delle luci è uno solo per ora: si può cambiare.
3. **Documenti e chiusura**: D-072, `versioni.md`, `CLAUDE.md` (provini da stampare), `cad/stl/README.md`; salvataggio in Fusion, tag, CI.

## Seguito: versione 2.1.6 — predisposizioni con i pezzi già in casa (scelta dell'utente dell'11 ottobre 2026)

**Fatta l'11 ottobre 2026** (D-074, tag `v2.1.6`). Sullo stesso design "Hexapod v2.1.0", versione 14 del file. Rispetto al piano:
- le guide dell'altoparlante non si alzano: la guancia è lunga 12,9, e il tondo si centra a x −96,3 contro il fermo e sporge 3,3 dietro, nello spazio libero;
- le lunette sono larghe 12, non 12,9: più larghe toccavano lo smusso del viso;
- la distanza del carapace dalle zampe medie è 3,96 mm, non 4,58 come in D-071, con carapace e lame identici a quelli della 2.1.5.

L'utente ha scelto i moduli che ha già (D-073):
- **X4**: MPU-6500 (GY-6500) al posto della Pololu LSM6DSO, con **doppia predisposizione**: si deve poter tornare alla Pololu smontando e basta;
- **X16**: microfoni MS3625, anche qui con doppia predisposizione (MS3625 e Adafruit 3421);
- **X17**: amplificatore MAX98357A generico e altoparlante tondo da 15 mm.

**Quote dei moduli** (S: dalle foto dei venditori, con il passo dei pin da 2,54 come scala; C: da guardare sul pezzo prima di stampare, nell'elenco delle cose da guardare in `CLAUDE.md`):
- **GY-6500**, la scheda blu "MPU-9250/6500":
  - 26 × 15,5 × 1,6 mm, componenti alti circa 1 mm;
  - 10 pin su un lato lungo, due fori Ø3 agli angoli del lato opposto, a circa 20,6 di interasse e circa 2,3 dal bordo;
  - asse X del chip sul lato corto; indirizzo I2C 0x68.
- **MS3625**: tonda, Ø13,5 circa, con due lati piatti a 12,6 lungo le due file di 3 pin. La porta del microfono è al centro della faccia senza componenti.
- **MAX98357A generico**, copia della Adafruit 3006:
  - 17,5 × 17,7 mm;
  - due fori Ø2,4 sul lato della morsettiera, a circa 13 di interasse e circa 2,2 dai bordi.
  - Anche la Adafruit ha i fori lì: **le bugne in diagonale di oggi sono sbagliate** e si correggono comunque.
- **Altoparlante tondo da 15 mm** (8 Ω, 1 W): anello bianco e cavetto con connettore da 1,25; lo spessore non è dichiarato (circa 4, C).

**Modifiche**:
1. **IMU** (`corpo.py`, nuovo pezzo `Corpo_Piastrina_IMU`, PETG-CF):
   - la base non cambia: restano le due bugne con gli inserti M2 a 18 di interasse, dove si avvita direttamente la Pololu;
   - la GY-6500 si monta su una piastrina di circa 26 × 11 × 2,5, che si avvita sulle stesse bugne con due M2 × 5 svasate a filo (la scheda ci passa sopra);
   - la scheda si fissa alla piastrina con due M2 × 6 in fori pilota Ø1,7, con i pin verso +Y, da dove arriva il bus;
   - fili saldati sulle piazzole, senza pin: sotto il vassoio non c'è altezza;
   - in Z: tetto a −9,4, bugne fino a −5,4, piastrina fino a −2,9, scheda fino a circa −0,3; il vassoio è a +1;
   - nuovo ingombro `Rif_IMU_MPU6500` in `rif_componenti.py`;
   - si cambia IMU svitando due viti: se la piastrina va corretta, si ristampa solo lei.
2. **Microfoni** (`Corpo_Carapace`):
   - stesso foro e stesso telaio 16,7 × 12,7: la MS3625 ci sta con i lati piatti lungo i lati lunghi, a 0,25 dalle pareti;
   - lungo il telaio la centrano due lunette stampate per microfono (`Corpo_Lunette_Microfoni`, PLA, quattro pezzi), che si tolgono per montare la Adafruit;
   - nuovo ingombro `Rif_Microfono_MS3625`.
3. **Amplificatore** (`Corpo_Carapace`): bugne spostate sul lato della morsettiera, a 13 di interasse (vale per la generica e per la Adafruit); ingombro aggiornato a 17,7 × 17,5.
4. **Altoparlante** (`Corpo_Carapace`):
   - le due guide sulla guancia restano a 15,4 di distanza, perché il tondo da 15 scorre fra le stesse guide;
   - le guide si alzano per uno spessore di circa 4 e prendono un fermo in fondo;
   - ingombro tondo Ø15 × 4 (C).
5. **Collegamenti** (verificati l'11 ottobre 2026, prima del via):
   - **IMU**:
     - stesso bus I2C0 (GPIO47 e GPIO3) e stessi 4 fili (VCC a 3,3 V, massa, SCL, SDA);
     - NCS, AD0 e FSYNC hanno già pull-up e pull-down sulla scheda (S, dalle schede dei venditori), quindi restano scollegati;
     - indirizzo 0x68. Su I2C0 non ci sono conflitti; 0x68 è fra gli indirizzi che il driver della camera prova sul suo bus, quindi l'IMU non va mai sul bus della camera;
     - la GY ha un suo regolatore a 3,3 V e i suoi pull-up, come la Pololu: il bilancio dei pull-up non cambia, si misura al banco.
   - **Firmware dell'IMU**:
     - driver dell'MPU-6500 (registri e scale diversi; WHO_AM_I 0x70, oppure 0x71 se è un MPU-9250);
     - riconoscimento automatico: 0x68 → MPU-6500, 0x6B → LSM6DSO. Così il cambio di scheda non chiede di ricompilare;
     - rotazione degli assi per scheda nella configurazione. Oggi il driver non esiste ancora: non c'è codice da rifare.
   - **Microfoni**:
     - gli stessi sei segnali con altri nomi: 3V = VDD, BCLK = SCK, LRCL = WS, DOUT = SD, SEL = L/R;
     - stessi GPIO 38, 39 e 40, L/R a massa su uno e a 3,3 V sull'altro;
     - formato I2S standard a 24 bit in slot da 32: è più semplice della SPH0645, che dà 18 bit e chiede di spostare i bit e togliere l'offset;
     - **in più, per tutti e due i tipi**: un pull-down da 100 kΩ sulla linea dati comune, sulla scheda del carapace (datasheet ADMP441/INMP441: la linea resta flottante quando nessun microfono la pilota). La resistenza c'è già nel set di B10;
     - l'MS3625 non ha un datasheet: si prova al banco prima di montarla.
   - **Amplificatore**:
     - stessi pin e stesso ordine (LRC, BCLK, DIN, GAIN, SD, GND, Vin), stesse impostazioni di fabbrica (9 dB, (L+R)/2): è una copia della Adafruit;
     - per l'altoparlante si taglia il connettore da 1,25 e i fili vanno nella morsettiera;
     - a 5 V su 8 Ω l'amplificatore arriva a circa 1,4 W: il volume va limitato nel firmware per l'altoparlante da 1 W, come lo sarebbe stato per quello da 0,7 W.
6. **Firmware e documenti**:
   - IMU a 0x68 nella tabella degli indirizzi (0x6B resta per la Pololu) e assi della GY-6500 da rimappare;
   - BOM: X4, X16 e X17 in possesso;
   - `predisposizioni.md`, `piano-elettronica-software.md` §6, `cablaggio.md`, `cad/stl/README.md`, D-074, `versioni.md`, `CLAUDE.md`.

**Verifiche**:
- sentinella sui volumi;
- `stato` e interferenze dell'assieme con gli ingombri nuovi, provando le due varianti di IMU e di microfono una alla volta;
- per il carapace: `carapace_zampe`, `sfilamento` e `campo`;
- distanza della GY-6500 dalla scheda dell'ADC (il suo bordo è a y 0,75) e dalle pareti del vano (|y| ≤ 16);
- spazio delle lunette accanto alle paratie della testa (x 82,6);
- massa aggiornata se cambia (pochi grammi);
- colori, STL, mesh, `esporta_robot` e generatori, test e CI.

**Chiusura**: salvataggio in Fusion, `geometria` riletta con la versione nuova del file, tag `v2.1.6`, push, CI verde.

## Seguito: versione 2.1.7 — correzioni dalla guida di montaggio (BOZZA, 15 ottobre 2026)

> Bozza: non si parte senza il via dell'utente. Le scelte di P-001 e P-002 sono arrivate il 15 ottobre 2026 (D-076) e sono nelle modifiche 11 e 12; dalle risposte dell'arresto 2 nascono anche le modifiche 14-16, i documenti della 17 e l'elenco dei testi della guida da rifare dopo la 2.1.7.

Origine: arresto 2 della guida (`guida/problemi.md`). Decisioni prese in autonomia su richiesta dell'utente per P-003 e P-005, con il ragionamento in `docs/ricerca/bloccanti-arresto2.md`; modifiche CAD del gruppo 4 delle decisioni in blocco (P-009, P-014, P-015, P-016, P-019, P-057, P-062, P-065), approvate dall'utente. Le scelte dell'utente sono in D-076; la chiusura della versione aggiunge D-077 con i risultati e le verifiche.

Ogni modifica dice: script e funzione, parametri, verifica dopo la modifica (procedure di `cad/CLAUDE.md`), impatto su BOM, guida e documenti. Le verifiche comuni a tutte sono in fondo ("Verifiche a valle").

### 1. P-003 (S-19): vassoio su colonne della base, viti M2 svasate a filo

Decisione e quote: `docs/ricerca/bloccanti-arresto2.md`, P-003.
- **Script**:
  - `corpo.py` → `fai_base`, blocco "bugne del vassoio" (righe 415-418): bugna Ø7,4 com'è fino a z −4,0, più una colonna Ø`cor_vas_col_d` (6,0) fino a `cor_vas_z` (1,0); in cima l'inserto M2 (`ins_m2_d` × `ins_m2_l`) al posto dell'M3. Commento corretto (oggi dice "distanziali da 10").
  - `corpo.py` → `fai_vassoio`: i quattro `foro_*` passano da `vite_m3_pass` a `vite_m2_pass` con la svasatura a 90° dall'alto, come `fai_piastrina_imu` (righe 1117-1125).
  - `corpo.py` → `_vassoio_fori`: posizioni invariate (30; ±12,5), (75; ±12,5); docstring da aggiornare.
- **Parametri**: nuovo `cor_vas_svas` = 0,9 mm (testa M2 Ø4,0 a 0,1 sotto la faccia, come `cor_pimu_svas`); `cor_vas_col_d` 6 mm finalmente usato; `cor_bas_luce` resta 3,3.
- **Verifica**:
  - `base` e poi `base_predisposizioni`, `giunti_coxa`, `istanze_corpo`; `vassoio`;
  - `controllo`, `interferenze`; in particolare colonne contro IMU (bordo a x 34,5: atteso 1,5 mm dalla colonna di (30; −12,5)), ADC (bordo a x 69,5: atteso 2,5), fili del bus e asola (modifica 8);
  - distanza testa-basetta: atteso 3,4 (testa a z 2,5, basetta a 5,9); misura nel modello con la vite svasata (catalogo della guida);
  - controllo "lunghezze" della guida: M2 × 5 svasata, punta a 3,4 sotto la cima della colonna, fondo del foro a 4,0;
  - sentinella sui volumi di base e vassoio.
- **BOM**: B18 (distanziali, 9,99 €, non ordinato) esce; riga "Vassoio → distanziali" della viteria diventa "Vassoio → colonne della base: M2 × 5 svasate (D8b), 4"; totali: M3 × 6 da 52 a 48, M2 × 5 svasate da 12 a 16 (+2 della piastrina IMU già contate a parte); inserti M2 (D5) +4, inserti M3 (D4) −4; ordine Amazon senza B18.
- **Guida**: catalogo `giunzioni.yaml` (`vassoio`: vite M2x5 svasata, punta `inserto_m2`, niente distanziale), `viteria.yaml` (`DIST_M3_5` non usato), glossario ("vassoio"), passi con i distanziali (03 inserti: quattro M2 in più sulle colonne; 08 elettronica); `basetta*.svg` e schemi.md 1.0: teste a filo del vassoio, i tre pin T-2, D-12, B-2 si saldano normalmente; S-19 chiuso. Le zone vietate restano.
- **Documenti**: D-051 e D-053 (rimando alla D-076), `docs/progetto-meccanico.md` (vassoio), `docs/predisposizioni.md` 2.8 (vano sotto il vassoio: le colonne), `docs/BOM.md`.

### 2. P-005 (S-02): interasse delle file di pin dell'ESP32 a 25,4

Decisione e fonti: `docs/ricerca/bloccanti-arresto2.md`, P-005.
- **Script**: `rif_componenti.py`, parametro `esp_file` (riga 99) da 24,7 a **25,4**, commento "S: 10 passi da 2,54; il 24,7 del disegno è fra le facce interne dei pin". Usato solo da `Rif_ESP32_S3_CAM` (`pin_header`, riga 461).
- **Parametri**: `esp_file` 25,4 (S fino alla prova a secco).
- **Verifica**: `rif_componenti` (ingombri), `istanze_corpo`; `interferenze` delle strip contro colonnine della basetta (|y| 6,5-6,8: restano 5,9 mm) e contro il bordo della basetta (|y| 17,5); `esporta_robot.py` (`esp_file` è in `robot/cad.json`), hash e generatori.
- **BOM**: nessun impatto.
- **Guida**: passo 4.04 ("file a 24,7 mm [C]" diventa "file a 25,4, 10 passi [S]") con la **prova a secco** prima di tagliare e saldare: strip infilate sui pin, gambe nelle righe 2 e 12 della millefori intera, tutte e quaranta senza forzare; se no, misura (Q-18) e opzione 3 di S-02. Q-18 non blocca più. S-02 chiuso con la prova come condizione.
- **Documenti**: D-053 (|y| 12,35 diventa 12,7, rimando alla D-076), `docs/dimensioni-componenti.md` (riga della quota 24,7).

### 3. P-009: ganci della catena LED fra i lobi; README del fondo dell'anello

- **Script**: `corpo.py` → `fai_carapace_predisposizioni`, ciclo "ganci del cavo della catena" (righe 1056-1062): alle x −40, 0, 40 si aggiungono **x ±75** (fra l'ultimo gancio e i lobi d'angolo a x ±94,7, oggi 55 mm senza ganci) e i ganci del **passaggio davanti**, sul percorso di `docs/cablaggio.md` 3.5; stessa sezione dei ganci di oggi (denti 1,2 × 2 alti 3 a y 41,8-43 e 46-47,2), posizione esatta scelta nel modello fuori da lobi, colonnine e pozzetti.
- **Parametri**: nessuno nuovo (le x restano nel ciclo, come oggi).
- **Verifica**: `carapace`, `carapace_dettagli`, `carapace_predisposizioni` (le ultime due vanno in timeout ma finiscono: rileggere); `controllo`, `interferenze`, `carapace_zampe`, `sfilamento`, `campo`; tratti in linea retta della catena (oggi 76-105 mm) misurati di nuovo per la lunghezza da tagliare.
- **BOM**: nessun impatto (stessa striscia).
- **Guida**: 13.04, 13.08 (ganci in più, niente nastro dove ora ci sono i ganci; lunghezza da tagliare ricalcolata), 2.19.
- **Documenti**: `cad/stl/README.md`, riga di `Corpo_Fondo_Anello`: "due pixel per sede" (D-068, 120 LED/m; quattro in tutto come X11); `docs/cablaggio.md` 3.5.

### 4. P-014: lamatura piana sotto la testa della vite del guscio della tibia

- **Script**: `zampa.py` → `fai_cover_tibia` (righe 868-870, `bossolo_vite` e `foro_vite`): nuovo taglio `lamatura_vite`, cilindro coassiale alla vite, piano e perpendicolare all'asse, dal fronte fino al punto più basso della faccia inclinata sotto la testa (oggi 1,23 mm sotto il bordo alto).
- **Parametri**: nuovo `cov_tib_lam_d` = 6,0 mm (testa DIN 912 Ø5,5 + 0,25 per lato).
- **Verifica**: procedura della zampa (`giunti`, `limiti`, `misura`, `interferenze`, `scansione`); parete residua del bossolo sotto la lamatura (bossolo Ø7 × 2,5); controllo "lunghezze" della guida con la testa sul piano nuovo: oggi la punta della M3 × 10 è 0,03 oltre il fondo con la testa nominale, quindi con la testa 1,23 più in basso **va controllato che non tocchi il fondo**. Se tocca: **M3 × 8** (BOM: M3 × 8 da 106 a 112, M3 × 10 da 18 a 12, opzione 2 di P-014) oppure foro più profondo nella tibia, se c'è materiale.
- **BOM**: forse M3 × 10 → M3 × 8 (sopra), dentro gli assortimenti già previsti.
- **Guida**: 6.23 (togliere "stringi piano"; vite giusta).
- **Documenti**: `docs/progetto-meccanico.md` (guscio della tibia), riga di viteria del BOM se cambia la vite.

### 5. P-015: dima del calettamento (α +20°, γ 100°)

- **Script**: `attrezzi.py`: in `POSE` una terza posa `'Dima_Calettamento': (0.0, 20.0, 100.0)` (imbardata, femore, ginocchio) e il suo posto in `LIBRERIA`; si costruisce con `fai_dima` e si controlla con `verifica_dime`, come `Dima_Posa_1` e `_2`.
- **Parametri**: nessuno nuovo (la posa viene dal calettamento di `robot/robot.yaml`: se cambia lì, cambia qui).
- **Verifica**: `verifica_dime` (i tre contatti toccano, niente altro); sentinella sui volumi; in più, come chiede P-015, il **margine del ginocchio a 180°** con un errore di calettamento di ±7,2° (mezzo dente su 25): `limiti` e `scansione` con γ fino a 180° e i limiti del firmware (177°); se il margine resta 0°, proposta di correzione in `robot.yaml` da approvare.
- **BOM**: nessun impatto (stampa).
- **Guida**: 6.16, 6.17 (calettamento con la dima, non più a occhio [C]); elenco delle stampe degli attrezzi.
- **Documenti**: `cad/stl/README.md` (nuovo `Dima_Calettamento.stl`), `docs/software.md` se cambia il calettamento.

### 6. P-016: stretta del piedino come parametro, tre varianti

- **Script**: `zampa.py` → `fai_piedino`: lo svuotamento `calza` usa `insideThickness` = `pied_stretta` invece di 0 (spessore verso l'interno: la calza si stringe sullo stinco). `esporta_stl.py`: tre file del piedino con `pied_stretta` 0 / 0,2 / 0,4 (il parametro si rimette a 0 alla fine).
- **Parametri**: nuovo `pied_stretta` = 0 mm (D-064: si tara sul provino 6).
- **Verifica**: procedura della zampa; con 0,2 e 0,4 l'interferenza piedino-stinco deve valere esattamente la stretta (caso di controllo: a 0 deve toccare senza compenetrare); pistoncino dell'FSR e suola invariati; sentinella sui volumi.
- **BOM**: nessun impatto (TPU di qualche provino in più).
- **Guida**: 1.14 (provino 6 con tre piedini), 2.12; dopo la prova, il valore scelto in `pied_stretta`.
- **Documenti**: `cad/stl/README.md` (tre STL del provino, uno solo per le zampe), D-064 (rimando).

### 7. P-057: blocco del provino degli inserti

- **Script**: `attrezzi.py`: nuova `fai_provino_inserti` (con il suo posto in `LIBRERIA` e il passo in `main`): blocchetto in PETG-CF con otto fori ciechi e i valori incisi accanto: **M3 Ø3,9 / 4,0 / 4,1** più **4,2** (oggi) profondi `ins_m3_l`; **M2 Ø2,9 / 3,0 / 3,1** più **3,4** (oggi) profondi `ins_m2_l`. Pareti fra i fori come nelle bugne del corpo (almeno 1,6 attorno al foro più grande). Esporta `cad/stl/attrezzi/Attrezzo_Provino_Inserti.stl`.
- **Parametri**: nessuno nuovo nel modello; i diametri del provino stanno nella funzione (sono i valori di `CLAUDE.md`, "Provini da stampare").
- **Verifica**: sentinella sui volumi; le profondità leggono i parametri di oggi. **Dopo la prova** (non in questa versione): valori in `ins_m3_d`, `ins_m3_l`, `ins_m2_d`, `ins_m2_l` e verifica completa, perché `ins_m3_d` muove le bugne delle culle.
- **BOM**: nessun impatto (inserti del kit, D4 e D5).
- **Guida**: 1.02, 1.03 (il provino ha un pezzo), 3.01, 3.02; i passi non scrivono il diametro.
- **Documenti**: `cad/stl/README.md`; vale anche per le colonne M2 del vassoio (modifica 1).

### 8. P-019: asola del bus fuori dalla basetta, 7 × 4

- **Script**: `corpo.py` → `fai_vassoio`, taglio `asola_bus` (righe 525-526). Oggi a x 47-53, y 13-16, cioè 1,5 mm sotto il bordo della basetta (y 17,5). Nella 2.1.7 l'asola va **fuori dall'ingombro della basetta, a y 18-22** (lato +Y, verso IMU e ADC), larga 7 lungo X: il piano del vassoio oggi finisce a y 16,5, quindi si aggiunge un'**ala** del piano attorno all'asola (fino a circa y 23,5, spessore `cor_vas_sp`), oppure, se l'ala non ci sta, una tacca aperta sul bordo.
- **Parametri**: `cor_vas_asola_x` 50 resta; nuovi `cor_vas_asola_y0` = 18 mm, `cor_vas_asola_l` = 7 mm (lungo X), `cor_vas_asola_w` = 4 mm (lungo Y).
- **Verifica**: `vassoio`; `controllo`, `interferenze` dell'ala con base, fili dei regolatori e del bus, carapace (`sfilamento`); passaggio della spina Qwiic dell'ADC (JST SH 4 poli, circa 6 × 4,3 × 2,9 [S]) nell'asola 7 × 4; i fili del ramo 3 non passano più sotto la basetta.
- **BOM**: nessun impatto.
- **Guida**: 4.16, 8.07, 8.09, 8.11, 8.12 (percorso dei fili fuori dalla basetta; niente più "prova la spina, altrimenti cavetto saldato").
- **Documenti**: D-066 (rimando), `docs/cablaggio.md` (ramo 3), `docs/predisposizioni.md` 2.8.

### 9. P-062: sede delle luci della tibia lunga quanto la striscia

- **Script**: `zampa.py`, parametro `luc_tib_z1` (riga 218) da `cov_tib_fin_z1` a **`cov_tib_fin_z1 + 3 mm`**; lo usa `fai_tibia` (`sede_luce`, riga 808) e, se lo segue, `fai_cover_tibia_diffusore`. Sede da z −33,0 a −83,5 (con lo 0,5 del taglio): 50,5 per la striscia da 50.
- **Parametri**: `luc_tib_z1`.
- **Verifica**: rigenerare la tibia (va in timeout ma finisce: rileggere), poi procedura della zampa; materiale fra il fondo della sede (z −83,5) e il foro dell'inserto del guscio (z −88, Ø4,2: bordo a −85,9): atteso 2,4 mm, da misurare; diffusore e finestra del guscio (la finestra finisce a −80: i sei LED restano nella finestra).
- **BOM**: nessun impatto.
- **Guida**: 6.05 (la striscia entra tutta nella sede).
- **Documenti**: testo di D-066 ("fino a Z −80" diventa la quota vera) con rimando dalla D-076.

### 10. P-065: bussola di battuta dei perni e attrezzo d'estrazione

- **Script**: `attrezzi.py`:
  - nuova `fai_bussola_perno`: appoggio forato con un **foro cieco Ø5,5 profondo 5,0**, così premendo il perno Ø5 × 12 si ferma con la sporgenza giusta di 1,4 dall'altra faccia senza misurarla; la profondità si calcola dai parametri (`perno_l`, spessore del blocco, sporgenza) invece di scriverla;
  - nuova `fai_estrattore`: asta che passa nel foro Ø7,2 e spinge sull'anello interno del cuscinetto o sul perno, con un tubo d'appoggio; secondo il consiglio di P-065 si stampa solo se il forzamento del provino non è leggero.
  - Tutti e due in `LIBRERIA`, nascosti, STL in `cad/stl/attrezzi/`.
- **Parametri**: nuovi `att_bus_d` = 5,5 mm; la profondità è un'espressione.
- **Verifica**: `verifica` sul perno di riferimento (`Rif_Perno_5`) dentro la bussola: sporgenza 1,4 ± 0,05; asta dell'estrattore contro il foro Ø7,2 (gioco ≥ 0,2) e contro la flangia (non deve toccarla); sentinella sui volumi.
- **BOM**: nessun impatto.
- **Guida**: 6.14 (perni con la bussola), sezione 9, 15.10, 15.11 (estrazione).
- **Documenti**: `cad/stl/README.md`. L'attrezzo dei cuscinetti di P-013 non è nel gruppo 4: resta fuori, a meno che l'utente lo chieda (P-013 dice "solo se il pollice non basta").

### 11. P-001: fessure del tetto aperte verso la coda, con il dentino per la fascetta di F1

Decisione (D-076): fessure aperte, nessun caricatore integrato; si carica con il caricatore USB 2S lento che l'utente ha già, collegato alle spine in coda. Ricerca: `docs/ricerca/carica-usbc.md`, sezioni 5 e 9. Il pacco si deve poter sfilare con T-plug e JST-XH attaccati.
- **Script**: `corpo.py` → `fai_base`, `fessura_cavi_*` (righe 408-410, da rileggere: il piano cita i numeri di riga della 2.1.6):
  - si toglie il ponte da 2 mm che chiude verso la coda le due fessure 13 × 4,5 (|y| 20,5…25) accanto a F1: diventano due tacche aperte verso la coda;
  - sulla lingua centrale fra le due tacche, dove passa la fascetta di F1 (D-055, x circa −76), un **dentino** (o una tacca) che impedisce alla fascetta di scivolare via dall'estremità aperta. Il dentino è largo quanto la fascetta da 2,5 mm (D11) più il gioco; l'altezza e la posizione si scelgono nel modello, non sono fissate qui.
- **Parametri**: il parametro del ponte (nome da leggere nello script) va a 0 o sparisce; nuovo `cor_fes_dente_*` (larghezza, altezza) con la misura della fascetta e il gioco usati, scritti accanto al valore.
- **Verifica**:
  - `base`, `base_predisposizioni`, `giunti_coxa`, `istanze_corpo`; `controllo`, `interferenze`;
  - **sfilamento del pacco con le spine e i cavi** (la prova di D-051 era senza cavi): T-plug (coppia circa 30 × 16 × 8,5), JST-XH (circa 10 × 5,8), cavi 12 AWG (Ø circa 3,5-4) nelle tacche, corsa di 140 mm; caso di controllo con la spina più alta di un millimetro;
  - tetto senza il ponte (2 mm): sezione chiusa o nervata, e la lingua centrale a sbalzo con il dentino;
  - costole di F1 e sua fascetta; linguetta dello sportello (D-054, 0,4 mm dal tetto) e sportello che non pizzica i cavi;
  - sentinella sui volumi: cambia solo la base.
- **Da provare** con la spina vera prima di stampare la base (11.03): T-plug e JST-XH scorrono nelle tacche; il cavo del caricatore esce dalla porta di coda senza tirare il pacco.
- **BOM**: nessun impatto sul modello; sacchetto LiPo (B20) già in D-076.
- **Guida**: 11.01 (carica con il caricatore dell'utente, sorvegliata), 11.03, 11.04, 11.05, 15.04, 15.05; apertura della sezione 11; 0.06 e 0.07 (la riga "il caricabatterie non è nel BOM" diventa "il caricatore USB 2S dell'utente; corrente e conservazione dal manuale");  passo nuovo "Carica" con le regole della ricerca (sezione 2: superficie che non brucia, presenza, pacco a temperatura ambiente, robot spento, corrente al massimo 1C, mai pacco gonfio o caldo).
- **Documenti**: D-051 e D-054 (rimando a D-076: il pacco si sfila dalle tacche aperte); D-055 (dentino); `docs/cablaggio.md` sezione 4 (porta di coda come porta di carica); `docs/progetto-meccanico.md`; `docs/dimensioni-componenti.md`: carica e conservazione dell'OVONIC (P-041, opzione 1: corrente 0,5C = 2,6 A consigliata, 1C = 5,2 A al massimo, conservazione a 3,85 V per cella: valori da leggere sull'etichetta del pacco [C], i divieti dai manuali ElectriFly / Great Planes e Flyzone citati nella ricerca).
- Collegati: P-007 (modifica 16), P-029 (saldatura e termorestringente fra T-plug e F1, fascetta per F2: solo guida), P-041.

### 12. P-002: testata 2 × 8 a 90° con chiave sul bordo posteriore della scheda del carapace

Decisione (D-076): soluzione A. Quote e confronto con B e C: `docs/ricerca/bloccanti-arresto2.md`, P-002. La spina entra ed esce orizzontale verso −X, dentro l'ottagono. In una versione futura l'utente vorrà un PCB stampato al posto della millefori: non è in questa versione; per ora J2 al bordo e le quote della scheda restano le stesse che servirebbero a un PCB.
- **Script**:
  - `rif_componenti.py`: `sch_w` (lato lungo X, oggi 20) a circa 23, `sch_l` (lungo Y, oggi 30) invariato; `sch_sp` (oggi 9 "con la spina IDC S") diventa l'ingombro vero (testata a 90° circa 9 [S] + scheda 1,6): da rileggere nello script che cosa conta oggi il 9, perché la ricerca parla di 1,6 + 2;
  - `corpo.py` → `fai_carapace_predisposizioni` (bugne `sch_a…d`, righe 1080-1086, e `sch_x` 39,5): le viti di coda si spostano davanti alla testata (x ≥ 41,5, oggi 32), la scheda si allunga verso la coda fino a x 29,5, bordo della testata.
- **Parametri**: `sch_l`, `sch_sp`, `sch_x`, posizioni delle bugne; nuovo parametro per l'ingombro della testata e della spina (misure dal disegno del pezzo scelto, non stime).
- **Prima del CAD**: leggere il disegno della testata scelta (Würth 61201621721 o equivalente, codice da confermare) e della spina IDC 61201623021: altezza della scatola, posizione della chiave e del polo 1, lunghezza della spina con il cavo piegato. I valori della ricerca (scatola circa 9, spina 10-12) sono [S].
- **Verifica**:
  - `carapace_predisposizioni`, `carapace`, `interferenze`: spina e testata contro il PCB dell'ESP32 (z 16,0…17,6; atteso 2,7 mm sopra il PCB sotto la testata), contro la **USB-C dell'ESP32 (x 12,7…20,1, fino a z 20,9)** e contro SSC-32 e ottagono. Attenzione: il fondo della spina orizzontale sta a circa z 20,3 [S], cioè 0,6 mm sotto la cima della USB-C nel tratto x 17,5…20,1: è il primo punto da verificare; se tocca, si alza la scheda, si accorcia la spina o si passa a B (riserva dichiarata nella ricerca);
  - connettore FPC della camera (x da 40,75, fino a z 19,6): non sotto la testata (x 29,5…38,5);
  - `sfilamento` del carapace con la spina innestata e con la spina staccata; `campo`;
  - caso di controllo: spina alta 2 mm in più, deve toccare.
- **BOM**: X2 (fatto in D-076): testata a 90° con chiave e 470 µF basso, stesso ordine.
- **Guida**: 4.06, 4.22-4.25, 13.16, 13.17, 13.19, A.17, A.18 (testata sul bordo, verso della chiave, fori liberi in più perché la scatola non copre più le colonne C-F); nota che l'alternativa PCB stampato arriverà in una versione successiva; Q-02 e P-075 chiusi.
- **Schemi**: `scheda_carapace*.svg`: J2 si sposta sul bordo, reti e prove (schemi.md 2.2, 2.6) restano; con i fori liberi in più si decide il posto dell'espansore TCA9534 e della presa Qwiic (P-067).
- **Documenti**: `docs/predisposizioni.md` 2.3 e 2.8; D-074 (scheda).

### 13. Testi rimandati qui da altre voci

- P-092: in questo piano (versione 2.1.5) la base del provino delle tasche è descritta diversamente dal CAD: correggere il testo come il CAD (foro pilota Ø2,5 autofilettante, D-072).
- P-099 e P-100: `cad/stl/README.md`, orientamento delle slitte (faccia piana sul piatto, bugne in alto [C]) e "le due slitte sono lo stesso pezzo, la destra ruotata". Nessuna modifica al CAD.

### 14. P-063: gola del fermo dei fili della tibia da 4,5

L'utente non può misurare i fili (Q-24): si progetta sulle specifiche stando larghi (D-076).
- **Script**: `zampa.py` → `fai_tibia`, gola del fermo dei fili (oggi 4,0 con 1,1 mm sotto i ponticelli): larghezza da 4,0 a **4,5**.
- **Parametri**: la larghezza della gola (nome da leggere nello script); il valore 4,5 viene da P-063 (doppino FSR 2 × 28 AWG e tre fili da 30 AWG occupano 3,3-4,05 mm; 0,45 mm di margine).
- **Verifica**: procedura della zampa; parete residua accanto alla gola e ponticelli; sentinella sui volumi della tibia.
- **BOM**: nessun impatto. **Guida**: 6.08. **Documenti**: `docs/predisposizioni.md` (X5, X31) se riporta la larghezza.

### 15. P-008: ToF posteriore avvitato, ritegno dell'altoparlante

Decisione (D-076, Q-09): il ToF posteriore si avvita (non essenziale, ma meglio); microfoni con colla a caldo fuori dal percorso del suono.
- **Script**: `corpo.py` → `fai_carapace_predisposizioni`, piano del ToF posteriore a 35°: **due fori pilota Ø1,7** per viti M2 (come la piastrina IMU), nelle posizioni dei fori della Pololu VL53L1X #3415, **da leggere sul disegno del produttore** prima del CAD (le quote di Q-33 sono del VL53L7CX, un'altra scheda). Dietro la guancia dell'altoparlante (sporge 3,3 mm): una linguetta o due costole di ritegno, senza chiudere il corridoio di 25 mm con cui si infila da dietro (D-074).
- **Parametri**: interasse e diametro dei fori del ToF; spessore della linguetta.
- **Verifica**: `carapace_predisposizioni`, `interferenze` (ToF, vite, altoparlante, ritegno), `sfilamento`; la testa della vite M2 e la sede del ToF non toccano la feritoia né il fascio; sentinella sui volumi del carapace.
- **BOM**: viti M2 dal kit (D8); nessun acquisto. **Guida**: 13.09, 13.11-13.13 (viti del ToF; colla solo per i microfoni).
- **Documenti**: `docs/predisposizioni.md` (X19: "due perni o un inserto M2" diventa "due fori pilota per M2").

### 16. P-007: rebbi dello sportello più lunghi sul pacco misurato

Il pacco misura 139,65 mm (Q-17): fra la battuta anteriore del tunnel (X 79) e la punta dei rebbi (X −68,4) ci sono 147,4 mm, quindi 7,75 mm di corsa.
- **Script**: `corpo.py` → `fai_sportellino`, `cor_sport_rebbio` da 17 a circa **22**: per un solo strato di schiuma EVA da 3 mm (D10) sulla faccia anteriore del pacco restano 147,4 − 5 = 142,4 mm contro 142,65 con la schiuma (compressione richiesta 0,25 mm [S]; il valore esatto si sceglie nel modello).
- **Verifica**: `sportello`, `controllo`, `interferenze`; che i rebbi allungati non tocchino T-plug e F1 (x −83…−61) né i cavi del pacco nelle tacche aperte della modifica 11; sfilamento dello sportello con il pacco dentro.
- **BOM**: D10 resta (un solo strato). **Guida**: 11.02, 11.05. **Documenti**: D-051.

### 17. Documenti da correggere con la 2.1.7 (dalle risposte)

- `docs/progetto-meccanico.md`: vassoio in PLA (oggi "in PETG", P-088); T-plug come in P-089 (già in `decisioni-arresto2.md`); colonne del vassoio (modifica 1).
- `docs/software.md` 6.7: assetto di partenza 100/45 a coppie, poi tripode lento (P-046); soglia del cicalino a 3,3 V per cella (P-066).
- `cad/stl/README.md`: lunette dei microfoni in PLA, colore libero.
- `docs/dimensioni-componenti.md`: dati misurati della batteria (139,65 mm, cavo 110 mm, T-plug femmina, positivo sul lato verticale) e inserti del kit (zigrinatura Ø4,2 e invito Ø4,0 per l'M3, Ø3,2 e Ø3,0 per l'M2).
- `CLAUDE.md`: stato e aperti alla chiusura della versione (voci già risolte dall'utente tolte da "Aperti": carica, scheda del carapace, lunghezza del pacco, sesso del T-plug, inserti, squadretta di prova).

### Testi della guida dopo la 2.1.7

Fatti con le immagini nuove e solo dopo il CAD (la guida segue ancora i distanziali, la testata dritta e le fessure chiuse):
- **P-003**: 4.04 (colonne e M2 svasate, niente M3 e distanziali, giunti piatti anche sotto T-2, D-12, B-2), catalogo `giunzioni.yaml` (`vassoio`: vite M2x5 svasata, punta `inserto_m2`) e `viteria.yaml` (`DIST_M3_5` non usato; totali M3 × 6 48, M2 × 5 svasate 16, inserti M3 90 e M2 32), 03-inserti (quattro M2 in più sulle colonne), 08 elettronica, riga B18 dell'inventario in 00-prima 0.17, glossario "vassoio".
- **P-005**: 4.04 ("file a 24,7 [C]" diventa "25,4, 10 passi [S]" con la prova a secco prima di tagliare e saldare).
- **P-002**: 4.06, 4.22-4.25, 13.16, 13.17, 13.19, A.17, A.18, con la nota sul PCB stampato futuro.
- **P-001, P-007**: sezione 11 e 15 come nella modifica 11 e nella 16.
- **P-008**: 13.09, 13.11-13.13.
- **P-031**: 12.01 e 12.07, con il secondo pulsante B3b come pulsante provvisorio sui pin A e B (arresto d'emergenza prima del carapace).
- **P-050**: 8, 9 e 12 come in D-076: rail acceso solo nella 12, con la batteria nel robot; la sezione 9.08 dice come si alimenta il tester dei servo (6,0 V dal regolatore del banco o dal rail, da decidere: oggi "alimentato a 6 V [C]").
- **P-088, P-078**: 02-stampa (vassoio e lunette in PLA, colore libero). **P-072**: 4.04-4.09 (Kapton o nastro in PVC, non nel BOM). **P-066**: 12.04, 13.14 (soglia 3,3 V). **P-046**: 14.07, 14.08. **P-085**: 4.05 (J1; X3 non si compra). **P-077**: 6.05, 6.08, 6.22 (luci opzionali, diffusore bianco). **P-111**: durate dei passi senza totale. **P-010**: 13.02 (misura il pulsante all'arrivo). **P-058**: 3.01 (divisione M3 × 5 e × 6 dopo il provino 1.03). **P-117**: 14.06 (soglie di batteria in simulazione).
- **Gommini**: niente nel CAD; nella guida è già fatto con D-076 (5.02).
- Dubbi della revisione dell'arresto 2 (15 ottobre 2026), da chiudere con i testi: 0.06, 11.01 e 15.04 danno gia' per aperte le fessure del tetto; sezione 9, alimentazione del tester dei servo (batteria fuori, F1 da 3 A) in contrasto con "T-plug staccato"; 14.09, regola del palmo per i 55 °C senza fonte; modifica 12, verso in cui si allunga la scheda del carapace e valore di `sch_sp` da rileggere nel codice. Dati dei moduli trovati sulle fonti pubbliche (Q-18, Q-21, Q-30...Q-34) in `docs/ricerca/dati-moduli.md`: da usare nella 2.1.7 per i fori di ADS7830 e VL53L7CX, la morsettiera dell'INA260 e la prova 1.5 degli schemi (GPIO40 con 10 kOhm a bordo); il pin 5V dell'ESP32 e' legato alla VBUS della USB da un PTC, senza diodo (S-07). Il registro di riferimento dei problemi e' `guida/problemi.md` (i file `guida/problemi/*.yaml` sono le origini e non si rigenerano).

### Verifiche a valle (una volta, alla fine)

- Corpo (modifiche 1, 3, 8, 11, 12, 15, 16): `controllo`, `interferenze`; coxe a ±35° e a 30,5° fra vicine; `carapace_zampe`, `sfilamento`, `campo`; `ciclo` a 100/45 e 70/70 a gruppi di fasi.
- Zampa (modifiche 4, 6, 9, 14): `giunti`, `limiti`, `misura`, `interferenze`, `scansione` (81 libere, 17 controlli su 20 che toccano).
- Attrezzi (5, 7, 10): `verifica_dime` e verifiche dei pezzi nuovi; tutti in libreria e nascosti.
- Sentinella sui volumi delle parti non toccate; caso di controllo per ogni interferenza nuova.
- A valle: `colori.py`, `esporta_stl.py` (con le varianti del piedino), `esporta_mesh.py`, `esporta_robot.py` (`geometria`, `mesh`, `pose`), `tools/descrizione.py --aggiorna-hash`, generatori; ruff, pytest, ctest, `npm test`.
- Massa: cambia di pochi grammi (via 4 distanziali da 5 e 4 M3, più 4 colonne di PETG-CF e 4 M2): aggiornare `calc/statica_tripode.py` e `robot.yaml` (`massa.attesa_g`, `regressione_statica`) solo se la differenza si vede nel totale.
- Guida: `esporta_guida.py` (`manifest`, `mesh`, `fori`, `zone`, `controllo`), poi `.venv/bin/python -m guida.costruisci controlla`; registro dei problemi aggiornato dall'utente (non da qui).

### Ordine e arresti

1. Via dell'utente su questo piano (le scelte di P-001 e P-002 ci sono: D-076).
2. Copia del file Fusion di lavoro per la versione (regola delle versioni).
3. Corpo: 1, 8, 3, 11, 12, 15, 16; verifiche del corpo.
4. Zampa: 9, 4, 6, 14; verifiche della zampa.
5. Attrezzi: 7, 5, 10.
6. Riferimenti: 2.
7. Verifiche a valle, documenti, BOM, guida.

Blocchi che lasciano repo e Fusion in uno stato da cui ripartire: un commit e un push per ogni punto, CI verde.

### Chiusura

D-077 (risultati e verifiche; le scelte di P-001, P-002, P-003, P-005 e le risposte dell'arresto 2 sono in D-076), `docs/versioni.md`, `CLAUDE.md` ("Stato attuale" e "Aperti"), `VERSIONE` in `versione.py` e `versione` in `robot.yaml` a 2.1.7, salvataggio in Fusion, `geometria` riletta, hash e generatori, tag `v2.1.7`, push, CI verde. Riepilogo all'utente diviso in verificato / assunzione / aperto.
