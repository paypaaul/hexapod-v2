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
   - **Base** in PETG-CF: blocchetto 24 × 16 × 8 con una vite M3 × 6 ISO 4762 in un foro pilota Ø2,5 autofilettante, come le alette lato albero (D-049, D-072): niente dado né trappola; vite dal kit D6 (testo corretto il 16 ottobre 2026, P-092).
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
- **Esito (16 ottobre 2026, blocco corpo)**: fatta. Base: bugna Ø7,4 fino a z −4 più colonna Ø6 (`cor_vas_col_d`) fino a z 1, inserto M2 in cima; vassoio: fori Ø2,4 con svasatura 0,9 (`cor_vas_svas`, quattro spigoli trovati). Volumi: base +743,92 mm³ e vassoio (con la modifica 8) +109,89 mm³, uguali al calcolo a mano. Giochi misurati per bisezione (il caso di controllo è il contatto al gioco + passo): colonna di (30; −12,5) a 1,50 dalla piastrina e dalla GY-6500, colonna di (75; 12,5) a 2,50 dall'ADC, le altre due a 4,96-4,99 (SSC-32, carapace). Testa M2 a z 2,5, basetta da 5,9: 3,4 mm. Il controllo "lunghezze" della guida resta alle verifiche a valle (`esporta_guida.py`).

### 2. P-005 (S-02): interasse delle file di pin dell'ESP32 a 25,4

Decisione e fonti: `docs/ricerca/bloccanti-arresto2.md`, P-005.
- **Script**: `rif_componenti.py`, parametro `esp_file` (riga 99) da 24,7 a **25,4**, commento "S: 10 passi da 2,54; il 24,7 del disegno è fra le facce interne dei pin". Usato solo da `Rif_ESP32_S3_CAM` (`pin_header`, riga 461).
- **Parametri**: `esp_file` 25,4 (S fino alla prova a secco).
- **Verifica**: `rif_componenti` (ingombri), `istanze_corpo`; `interferenze` delle strip contro colonnine della basetta (|y| 6,5-6,8: restano 5,9 mm) e contro il bordo della basetta (|y| 17,5); `esporta_robot.py` (`esp_file` è in `robot/cad.json`), hash e generatori.
- **BOM**: nessun impatto.
- **Guida**: passo 4.04 ("file a 24,7 mm [C]" diventa "file a 25,4, 10 passi [S]") con la **prova a secco** prima di tagliare e saldare: strip infilate sui pin, gambe nelle righe 2 e 12 della millefori intera, tutte e quaranta senza forzare; se no, misura (Q-18) e opzione 3 di S-02. Q-18 non blocca più. S-02 chiuso con la prova come condizione.
- **Documenti**: D-053 (|y| 12,35 diventa 12,7, rimando alla D-076), `docs/dimensioni-componenti.md` (riga della quota 24,7).
- **Esito (16 ottobre 2026, blocco corpo)**: fatta. `esp_file` 25,4 (S); il riferimento si cambia senza cancellarlo (`rif_componenti.py` → `ingombri`, `solo=[...]`, `sostituisci=True`: corpi aggiornati nella BaseFeature, le istanze restano). Strip a |y| 11,43…13,97, `controllo` 0, nessuna interferenza. `esporta_robot.py`, hash e generatori restano alle verifiche a valle.

### 3. P-009: ganci della catena LED fra i lobi; README del fondo dell'anello

- **Script**: `corpo.py` → `fai_carapace_predisposizioni`, ciclo "ganci del cavo della catena" (righe 1056-1062): alle x −40, 0, 40 si aggiungono **x ±75** (fra l'ultimo gancio e i lobi d'angolo a x ±94,7, oggi 55 mm senza ganci) e i ganci del **passaggio davanti**, sul percorso di `docs/cablaggio.md` 3.5; stessa sezione dei ganci di oggi (denti 1,2 × 2 alti 3 a y 41,8-43 e 46-47,2), posizione esatta scelta nel modello fuori da lobi, colonnine e pozzetti.
- **Parametri**: nessuno nuovo (le x restano nel ciclo, come oggi).
- **Verifica**: `carapace`, `carapace_dettagli`, `carapace_predisposizioni` (le ultime due vanno in timeout ma finiscono: rileggere); `controllo`, `interferenze`, `carapace_zampe`, `sfilamento`, `campo`; tratti in linea retta della catena (oggi 76-105 mm) misurati di nuovo per la lunghezza da tagliare.
- **BOM**: nessun impatto (stessa striscia).
- **Guida**: 13.04, 13.08 (ganci in più, niente nastro dove ora ci sono i ganci; lunghezza da tagliare ricalcolata), 2.19.
- **Documenti**: `cad/stl/README.md`, riga di `Corpo_Fondo_Anello`: "due pixel per sede" (D-068, 120 LED/m; quattro in tutto come X11); `docs/cablaggio.md` 3.5.
- **Esito (16 ottobre 2026, blocco corpo)**: fatta. Ganci dei fianchi anche a x ±75 (stessi denti); passaggio davanti a x 75, cavo lungo Y, con tre ganci a y −24, 0, 24 (denti a x 71,5-72,7 e 75,7-76,9), fra l'ampli (fino a x 69,6) e le paratie della testa (da x 81). Carapace +200,08 mm³ insieme alle modifiche 12 e 15, uguale al calcolo a mano. Gioco dei ganci nuovi 1,95 mm (dall'ampli; contatto al passo successivo). Tratti in linea retta della catena, in pianta, dai centri dei ganci: al più 40 mm sui fianchi (prima 76-105), circa 10 dal gancio a x ±75 alla luce del lobo d'angolo, circa 25 per tratto davanti; le lunghezze da tagliare vanno in `cablaggio.md` 3.5 con i documenti.

### 4. P-014: lamatura piana sotto la testa della vite del guscio della tibia

- **Script**: `zampa.py` → `fai_cover_tibia` (righe 868-870, `bossolo_vite` e `foro_vite`): nuovo taglio `lamatura_vite`, cilindro coassiale alla vite, piano e perpendicolare all'asse, dal fronte fino al punto più basso della faccia inclinata sotto la testa (oggi 1,23 mm sotto il bordo alto).
- **Parametri**: nuovo `cov_tib_lam_d` = 6,0 mm (testa DIN 912 Ø5,5 + 0,25 per lato).
- **Verifica**: procedura della zampa (`giunti`, `limiti`, `misura`, `interferenze`, `scansione`); parete residua del bossolo sotto la lamatura (bossolo Ø7 × 2,5); controllo "lunghezze" della guida con la testa sul piano nuovo: oggi la punta della M3 × 10 è 0,03 oltre il fondo con la testa nominale, quindi con la testa 1,23 più in basso **va controllato che non tocchi il fondo**. Se tocca: **M3 × 8** (BOM: M3 × 8 da 106 a 112, M3 × 10 da 18 a 12, opzione 2 di P-014) oppure foro più profondo nella tibia, se c'è materiale.
- **BOM**: forse M3 × 10 → M3 × 8 (sopra), dentro gli assortimenti già previsti.
- **Guida**: 6.23 (togliere "stringi piano"; vite giusta).
- **Documenti**: `docs/progetto-meccanico.md` (guscio della tibia), riga di viteria del BOM se cambia la vite.
- **Esito (16 ottobre 2026, blocco zampa)**: fatta, con il foro più profondo e non con la M3 × 8.
  - Lamatura Ø6 (`cov_tib_lam_d`) con il fondo piano a X 132,09, dove il fronte è più basso sotto la lamatura (bordo verso il piede, Z −91): la testa ora appoggia su tutta la corona (19,2 mm², Ø6 − Ø3,4); la parete asportata arriva a 1,34 sul bordo alto. Sotto il piano restano 2,72 mm di fronte e bossolo (da X 129,37). Funzione `_lamatura_vite`, usata da `fai_cover_tibia`; sul modello aggiunta con il passo `lamatura` (gruppo `Cover_Tibia_lamatura`).
  - Con la testa sul piano la punta della M3 × 10 andava 0,34 oltre il fondo del foro dell'inserto (calcolo e prova). Il foro dell'inserto nella tibia passa da `ins_m3_l` (6,7) a `tib_ins_guscio_l` = `ins_m3_l` + 1 (7,7; dietro restano 5,85 mm di stinco, 2,9 dalla fessura bassa, 2,39 dalla sede delle luci): punta 0,66 sopra il fondo, presa 7,04 (l'inserto da 5,7 è preso tutto). Così vite, BOM e viteria non cambiano.
  - Volumi: guscio −13,06 mm³ (differenza booleana fra prima e dopo; calcolo a mano 13,13; il `volume` dei corpi dà 14,77, è meno preciso), tibia −13,85 (calcolo 13,85).
  - Vite provata con corpi temporanei (testa Ø5,5 × 3 sul piano, gambo Ø3): M3 × 10 libera; lunga 10,65 libera, 10,68 tocca il fondo (0,12 mm³): il gioco è 0,66. Controlli: testa abbassata di 0,1 tocca il guscio (1,47 mm³, come la corona × 0,1), testa Ø6,2 tocca la parete della lamatura.
  - Resta alle verifiche a valle il controllo "lunghezze" della guida (`esporta_guida.py` → `fori`).

### 5. P-015: dima del calettamento (α +20°, γ 100°)

- **Script**: `attrezzi.py`: in `POSE` una terza posa `'Dima_Calettamento': (0.0, 20.0, 100.0)` (imbardata, femore, ginocchio) e il suo posto in `LIBRERIA`; si costruisce con `fai_dima` e si controlla con `verifica_dime`, come `Dima_Posa_1` e `_2`.
- **Parametri**: nessuno nuovo (la posa viene dal calettamento di `robot/robot.yaml`: se cambia lì, cambia qui).
- **Verifica**: `verifica_dime` (i tre contatti toccano, niente altro); sentinella sui volumi; in più, come chiede P-015, il **margine del ginocchio a 180°** con un errore di calettamento di ±7,2° (mezzo dente su 25): `limiti` e `scansione` con γ fino a 180° e i limiti del firmware (177°); se il margine resta 0°, proposta di correzione in `robot.yaml` da approvare.
- **BOM**: nessun impatto (stampa).
- **Guida**: 6.16, 6.17 (calettamento con la dima, non più a occhio [C]); elenco delle stampe degli attrezzi.
- **Documenti**: `cad/stl/README.md` (nuovo `Dima_Calettamento.stl`), `docs/software.md` se cambia il calettamento.
- **Esito (16 ottobre 2026, blocco attrezzi)**: fatta. `POSE['Dima_Calettamento']` legge il calettamento da `robot/robot.yaml` (`calettamento()`: (0, 20, 100); se cambia lì, cambia la dima rifacendola), posto in libreria (0; 1000; 0), nascosta; costruita con `dime` e `solo=['Dima_Calettamento']` (rifare le altre due dime ne cancellerebbe i componenti). 9 lavorazioni, schizzi vincolati, 9702,57 mm³ (Posa_1 9676,07).
  - `verifica_dime` (nuovo argomento `solo`) sulla zampa AS: i tre denti toccano coxa, tibia e cassa del servo di coxa (distanze 0,0); unici urti con la lama B e la sua feritoia, che si tolgono per montare la dima (come per Dima_Posa_1 e _2, rifatte per confronto: stessi urti). Casi di controllo, zampa a 1° dalla posa: femore +1 libero a 0,33 dalla coxa, −1 interseca la coxa (12,62 mm³); ginocchio +1 libero a 0,33, −1 interseca la tibia (12,62); imbardata +1 interseca il servo (4,41), −1 libero a 0,31. La dima ferma ogni giunto da un lato e lo lascia andare dall'altro.
  - Margine del ginocchio (P-015). Il campo libero arriva a γ 180 a ogni α (scansione del blocco zampa: le pose a 180 sono libere). La corsa del servo è il calettamento ± 80 (`guardia.corsa_servo`): con il dente più vicino resta un errore e entro ±7,2°, quindi la corsa del ginocchio va da 20 + e a 180 + e. Con e = −7,2 finisce a 172,8: il limite del firmware (177) non si raggiunge, mancano 4,2°. Con e = +7,2 comincia a 27,2, sotto il minimo del firmware (γmin + 3 ≥ 32): va bene. Il femore ha margine da tutte e due le parti (−67,2…−52,8 contro −45, 92,8…107,2 contro 82).
  - **Proposta da approvare** (non applicata, `robot.yaml` non toccato): (1) `calettamento.gamma` da 100 a **104,5**. Con ±7,2 la corsa va da 31,7 a 177,3 nel caso peggiore, cioè 0,3° di margine sopra (177) e sotto (32, a α ≥ 40; sotto α 40 γmin è più alto e il margine cresce). La dima si rifà da sola dal valore, ma cambiano anche la tabella di `software.md` 2.5, i generatori e la posa della guida 6.16-6.17. (2) In alternativa il calettamento resta a 100 e la guardia prende `gamma_max` = min(177, γ di calettamento misurato + 80) dopo la taratura a due punti: il ginocchio perde al più 4,2° di distensione, senza cambiare nulla nella meccanica. Consiglio la (2): tocca solo il firmware. Prima di scegliere va controllato il γ massimo delle andature e delle pose di oggi (non l'ho guardato).
  - **Scelta dell'utente (16 ottobre 2026)**: la (2). Calettamento a 100 come oggi; dopo la taratura `gamma_max = min(177, γ misurato + 80)`, scritto in `software.md` 2.5 (con la nota per il firmware S2) e come commento su `guardia.gamma_max` in `robot.yaml` (nessun campo nuovo). Le andature dei quattro assetti arrivano al più a γ 103,3 in appoggio: il limite non le tocca.

### 6. P-016: stretta del piedino come parametro, tre varianti

- **Script**: `zampa.py` → `fai_piedino`: lo svuotamento `calza` usa `insideThickness` = `pied_stretta` invece di 0 (spessore verso l'interno: la calza si stringe sullo stinco). `esporta_stl.py`: tre file del piedino con `pied_stretta` 0 / 0,2 / 0,4 (il parametro si rimette a 0 alla fine).
- **Parametri**: nuovo `pied_stretta` = 0 mm (D-064: si tara sul provino 6).
- **Verifica**: procedura della zampa; con 0,2 e 0,4 l'interferenza piedino-stinco deve valere esattamente la stretta (caso di controllo: a 0 deve toccare senza compenetrare); pistoncino dell'FSR e suola invariati; sentinella sui volumi.
- **BOM**: nessun impatto (TPU di qualche provino in più).
- **Guida**: 1.14 (provino 6 con tre piedini), 2.12; dopo la prova, il valore scelto in `pied_stretta`.
- **Documenti**: `cad/stl/README.md` (tre STL del provino, uno solo per le zampe), D-064 (rimando).
- **Esito (16 ottobre 2026, blocco zampa)**: fatta. `pied_stretta` = 0 (spessore interno dello svuotamento `calza`; fuori resta `tib_piede_sp`). Con un valore nullo Fusion non tiene il parametro nello svuotamento: `_collega_stretta` lo collega con 0,2 provvisorio e poi rimette il valore (lo usano il passo `calza` sul modello e `fai_piedino`, quest'ultimo non provato perché rifare il piedino cancellerebbe il giunto). Verifiche con sonde 1 × 1 mm attraverso la compenetrazione piedino-stinco: a 0,2 spessore 0,2001 sul fianco −X (0,2066 sui fianchi Y, inclinati di 14,6°: 0,2 / cos), compenetrazione 117,7 mm³; a 0,4 spessore 0,4002 (0,4133), 231,9 mm³; a 0 nessuna compenetrazione (il caso di controllo: toccano). Esterno, suola (Z −110) e pistoncino (Z −108,4…−107,9) invariati; con la stretta la suola interna sale e il pistoncino sporge di meno. A 0 il piedino ha il volume della 2.1.6. `esporta_stl.py` → `varianti_piedino`: `cad/stl/attrezzi/Piedino_stretta_0.stl`, `_0.2.stl`, `_0.4.stl` (provati in una cartella di prova: volumi degli STL 1554,4, 1710,8 e 1860,3 mm³, come il modello), poi rimette `pied_stretta`; `Piedino.stl` resta quello del valore del modello. README degli STL con i documenti.

### 7. P-057: blocco del provino degli inserti

- **Script**: `attrezzi.py`: nuova `fai_provino_inserti` (con il suo posto in `LIBRERIA` e il passo in `main`): blocchetto in PETG-CF con otto fori ciechi e i valori incisi accanto: **M3 Ø3,9 / 4,0 / 4,1** più **4,2** (oggi) profondi `ins_m3_l`; **M2 Ø2,9 / 3,0 / 3,1** più **3,4** (oggi) profondi `ins_m2_l`. Pareti fra i fori come nelle bugne del corpo (almeno 1,6 attorno al foro più grande). Esporta `cad/stl/attrezzi/Attrezzo_Provino_Inserti.stl`.
- **Parametri**: nessuno nuovo nel modello; i diametri del provino stanno nella funzione (sono i valori di `CLAUDE.md`, "Provini da stampare").
- **Verifica**: sentinella sui volumi; le profondità leggono i parametri di oggi. **Dopo la prova** (non in questa versione): valori in `ins_m3_d`, `ins_m3_l`, `ins_m2_d`, `ins_m2_l` e verifica completa, perché `ins_m3_d` muove le bugne delle culle.
- **BOM**: nessun impatto (inserti del kit, D4 e D5).
- **Guida**: 1.02, 1.03 (il provino ha un pezzo), 3.01, 3.02; i passi non scrivono il diametro.
- **Documenti**: `cad/stl/README.md`; vale anche per le colonne M2 del vassoio (modifica 1).
- **Esito (16 ottobre 2026, blocco attrezzi)**: fatta. `attrezzi.py` → `fai_provino_inserti` (passo `provino_inserti`), componente `Attrezzo_Provino_Inserti` in libreria (200; 1000; 0), nascosto. Blocchetto 37 × 23,8 × 8,7 (`ins_m3_l` + 2 di fondo); riga dietro M3 Ø3,9 / 4,0 / 4,1 / 4,2 profondi `ins_m3_l` (6,7), riga davanti M2 Ø2,9 / 3,0 / 3,1 / 3,4 profondi `ins_m2_l` (4,0), passo 9 (fra due fori da 4,2 restano 4,8); bordo a 1,6 (`cul_ins_parete`) dal foro M2 più grande, come nelle bugne. Sopra ogni foro il diametro inciso ("3.9" …), grassetto alto 4, profondo 0,6. Letti sul modello: otto facce cilindriche con diametro, centro e profondità giusti; volume 7137,64 mm³ = blocco 7661,22 − fori M3 345,51 − fori M2 121,20 − scritte 56,87. I diametri stanno nella funzione (`PROV_INS_M3`, `PROV_INS_M2`), non nel modello. Gli schizzi delle scritte hanno riquadro, lati e punti tutti vincolati, ma Fusion li dà comunque non vincolati (con una scritta `isFullyConstrained` resta falso): la funzione controlla i lati del riquadro. In `esporta_stl.py` (`ATTREZZI`) e `colori.py` (PETG-CF nero); l'STL si fa con la chiusura.

### 8. P-019: asola del bus fuori dalla basetta, 7 × 4

- **Script**: `corpo.py` → `fai_vassoio`, taglio `asola_bus` (righe 525-526). Oggi a x 47-53, y 13-16, cioè 1,5 mm sotto il bordo della basetta (y 17,5). Nella 2.1.7 l'asola va **fuori dall'ingombro della basetta, a y 18-22** (lato +Y, verso IMU e ADC), larga 7 lungo X: il piano del vassoio oggi finisce a y 16,5, quindi si aggiunge un'**ala** del piano attorno all'asola (fino a circa y 23,5, spessore `cor_vas_sp`), oppure, se l'ala non ci sta, una tacca aperta sul bordo.
- **Parametri**: `cor_vas_asola_x` 50 resta; nuovi `cor_vas_asola_y0` = 18 mm, `cor_vas_asola_l` = 7 mm (lungo X), `cor_vas_asola_w` = 4 mm (lungo Y).
- **Verifica**: `vassoio`; `controllo`, `interferenze` dell'ala con base, fili dei regolatori e del bus, carapace (`sfilamento`); passaggio della spina Qwiic dell'ADC (JST SH 4 poli, circa 6 × 4,3 × 2,9 [S]) nell'asola 7 × 4; i fili del ramo 3 non passano più sotto la basetta.
- **Esito (16 ottobre 2026, blocco corpo)**: fatta. Ala del piano x 45-55, y 16-23,5 (bordo 1,5, `cor_vas_ala_bordo`), asola 7 × 4 a x 46,5-53,5, y 18-22. Gioco dell'ala 1,30 mm (dalla colonnina del carapace sulla base, x 43,7; contatto al passo successivo). La spina Qwiic (6 × 2,9 in pianta) passa nell'asola; controllo: una spina 7,2 × 4,2 tocca il vassoio. **Corretta dopo la verifica** (18, punto 1): ala e asola a x 25–35 / 26,5–33,5.
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
- **Esito (16 ottobre 2026, blocco zampa)**: fatta. `luc_tib_z1` = `cov_tib_fin_z1` + 3: sede da Z −32,95 a −83,53 (il fondo sulla corda cambia pendenza con la quota d'arrivo). Tibia −36,03 mm³ (calcolo 36,03). Fra la sede e il foro dell'inserto del guscio 2,39 mm (atteso 2,4), dalla fessura bassa 3,87. I sei LED (passo 8,33) stanno fra Z −37,1 e −78,8 nella finestra (fino a −80); il diffusore segue la finestra e non cambia. Parametro aggiornato senza rifare la tibia (rifarla cancella i giunti).

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
- **Esito (16 ottobre 2026, blocco attrezzi)**: fatta, con la bussola appoggiata al mozzo invece che al rialzo.
  - `fai_bussola_perno` (passo `bussola`), `Attrezzo_Bussola_Perno` in libreria (260; 1000; 0), nascosta: cilindro Ø20 (`att_bus_D`, sta nella testa del femore, raggio 13) alto 8,4. La faccia in alto appoggia sulla faccia interna del mozzo (`zy_B_int`), con una tasca Ø6,8 × 0,7 per il rialzo (`att_bus_gio` 0,3), così la morsa non schiaccia il rialzo da 0,4, che fissa il gioco del cuscinetto. Foro cieco Ø5,5 (`att_bus_d`), con il fondo a `att_bus_prof` = `perno_l − perno_sporge − fem_B_mozzo` = 5,4 dal mozzo, cioè 5,0 dalla faccia del rialzo come chiedeva il piano. Fondo da 3 (`att_bus_fondo`). Vale anche per il braccio della coxa (stesso spessore, 5,2 + 0,4), ma lì non è verificata.
  - `fai_estrattore` (passo `estrattore`), due componenti in libreria, nascosti. `Attrezzo_Estrattore_Asta` (300; 1000; 0), lunga 53,2, si stampa in piedi sulla testa: punta Ø4,6 × 6,0 (`att_estr_pilota_*`: centra l'asta nel foro del cuscinetto e spinge fuori i perni, più lunga dei 5,6 del foro), spalla Ø6,2 × 10 (`att_estr_d` = `cus_rialzo_d`: tocca solo l'anello interno, come il rialzo), gambo Ø8 × 32,2 (`att_estr_gambo_*`: si ferma sul fondo della culla con la testa 3 mm sopra l'orlo) e testa Ø20 × 5. `Attrezzo_Estrattore_Tubo` (340; 1000; 0): Ø16 (`cul_mozzo_d`) / Ø12,4 (flangia + 0,4 per lato) × 15 (perno + 3). Volumi uguali al calcolo a mano: bussola 2501,85 (2501,86), asta 3590,97 (3591,0), tubo 1204,49 (1204,5).
  - Nuove verifiche con corpi temporanei, in sola lettura: `verifica_bussola` e `verifica_estrattore` sulla zampa AS (le parti si riconoscono con `_parti_zampa`, i corpi degli attrezzi si portano nella terna della parte con `_terna`).
  - Bussola, su anca e ginocchio: nessuna intersezione con il femore B né con il perno; la bussola tocca il mozzo, il perno tocca il fondo (gioco 0,000), quindi la **sporgenza è 1,40**. Controlli: bussola 0,05 più su interseca il femore B per 13,89 mm³, cioè 277,8 mm² (la corona Ø6,8…Ø20 sul mozzo, non il rialzo); perno 0,05 più dentro tocca il fondo per 0,982 mm³ (la faccia Ø5). Fra il rialzo e il fondo della sua tasca: 0,3.
  - Estrattore, su culla della coxa e della tibia: asta e tubo senza intersezioni. Gioco della spalla nel foro Ø7,2: 0,501 (≥ 0,2); della punta nel foro del cuscinetto: 0,199. Il tubo resta a 0,4 dalla flangia. Controlli: asta 0,05 più avanti interseca il cuscinetto per 0,528 mm³, cioè 10,56 mm², quanto la corona Ø5…Ø6,2 (la spalla spinge solo l'anello interno, Ø6,4); tubo 0,05 più su tocca il mozzo su 80,3 mm² (tutta la sua corona). A fine corsa (8,8 mm, il gambo sul bordo del foro Ø7,2: controllo 0,478 mm³ = corona Ø7,2…Ø8), il cuscinetto è tutto fuori dalla sede e sta nel tubo senza toccarlo.
  - Perno del femore B spinto fuori dal lato del rialzo, con il tubo sulla faccia esterna: la punta tocca il perno (controllo 0,831 mm³ = Ø4,6); a fine corsa (11,0, la spalla sul rialzo, controllo 10,56 mm²) il perno è fuori dal foro di 0,4 e sta nel tubo senza toccarlo.
  - Non verificati: i cuscinetti delle coxe nella base (P-013, fuori dal gruppo 4) e il perno della coxa. In `esporta_stl.py` (`ATTREZZI`) e `colori.py` (PETG-CF nero); gli STL si fanno con la chiusura.

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
- **Esito (16 ottobre 2026, blocco corpo)**: fatta, con una correzione in più.
  - Il ponte era il tetto fra x −85,4 e −83,4: le fessure ora arrivano alla coda (taglio fino a x −86,4). Il "dentino" è fatto come **due tacche** sui bordi della lingua, larghe 2,9 lungo X (fascetta da 2,5 più 0,2 per lato, `cor_fes_dente_w`), profonde 1 (`cor_fes_dente_h`), a x −76 (`cor_fes_dente_x`): un dente dentro la fessura fermerebbe i cavi che escono, uno sotto il tetto starebbe nei 2,6 mm sopra il pacco.
  - **Correzione**: le linguette delle spie dei rail (X13) erano a |y| 16-22 sul bordo di coda del tetto e fermavano i cavi del pacco che escono dalle fessure (urto trovato dalla prova di sfilamento). Ora sono a |y| 14-20 (LED a |y| 17), stesse misure; fuori dalle costole di F1 (|y| 12). Da riportare in `cablaggio.md` e `predisposizioni.md` (X13).
  - Nuova verifica `assieme.py` → `sfilamento_pacco` (corpi temporanei, sportello tolto, carapace montato): pacco, due cavi Ø4 nella fessura sinistra e il bilanciamento Ø3 nella destra, meta' femmina del T-plug (15 × 16 × 8,5) e JST-XH (9,9 × 5,75 × 6, S). Pacco e cavi, con le spine già fuori dalla porta: liberi da 0 a 20 mm (e oltre). Con la spina sul lato destro (−Y): libero da 0 a 165 mm. Con la spina sul lato sinistro tocca il ToF posteriore fra 10 e 20 mm (è l'angolo già noto in `cablaggio.md` 4): la spina si porta fuori dal lato dell'altoparlante o si inclina. Spina alta 1 mm in più: libera (sotto il cicalino restano 3,3). Casi di controllo: spina alta 4,3 in più tocca il cicalino; cavi Ø5 toccano le pareti della fessura da 4,5.
  - Tetto: la lingua (41 × 15, spessa 2) è a sbalzo dalla parte di testa, irrigidita dalla costola posteriore di F1 e dalle linguette delle spie sul bordo libero; la linguetta dello sportello (|y| ≤ 8) resta sotto la lingua, a 0,4 (controllo: sportello alzato di 0,5 tocca la base). Cavi contro lo sportello chiuso: liberi.
  - Volume della base come atteso (+743,92 mm³ con la modifica 1). Resta la prova a mano con la spina vera (11.03).

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
- **Esito (16 ottobre 2026, blocco corpo)**: fatta. Disegni letti: testata Würth 61201621721 (L 27,98, scatola 8,85 dal bordo, alta 9,0, file dei pin a 1,84 e 4,38 dietro la scatola, chiave al centro sul lato lontano dalla scheda) e spina 61201623021 (L 25, spessa 6,0, 7,0 con la chiave larga 3,7; 11,4 con il fermacavo, S letto sul disegno). `Rif_Scheda_Carapace` ora ha quattro corpi: millefori 30 × 21,5 × 1,6, testata, spina (sporgenza 10 verso la coda, `sch_spina_fuori`, S) e chiave. Scheda da x 29,5 (`sch_x0`, bordo della testata) a 51,0: **21,5 e non 23**, perché l'ampli comincia a x 51,85 (resta 0,85). Viti di coda a x 41,5 (`sch_vite_xp`: testa Ø3,8 a 1,25 dalla scatola, le file dei pin sono a |y| ≤ 8,9), anteriori a 48,0 (`sch_vite_xa`, bugna Ø5,5 fino a 50,75). `sch_sp` = 1,6 + 9 = 10,6. Giochi: spina 0,94 dalla USB-C dell'ESP32 (fondo a z 21,8 contro 20,86), chiave 0,28 di fianco alla USB-C (non sopra), testata 2,39 dal connettore FPC (che resta fuori, da x 40,75) e 2,7 sopra il PCB. Caso di controllo: spina 2 mm più bassa tocca la USB-C (10,9 mm³). `sfilamento` del carapace (con la spina innestata, che sale con lui) libero a 5, 10, 20 e 40; `campo` libero (controllo a +8° tocca visiera e fascia). Spina staccata: è un sottoinsieme del caso innestato. Lato della chiave e polo 1 sulla millefori: negli schemi. **Corretta dopo la verifica** (18, punto 2): scheda alzata di 0,6 e percorso del cavo piatto.

### 13. Testi rimandati qui da altre voci

- P-092: in questo piano (versione 2.1.5) la base del provino delle tasche è descritta diversamente dal CAD: correggere il testo come il CAD (foro pilota Ø2,5 autofilettante, D-072).
- P-099 e P-100: `cad/stl/README.md`, orientamento delle slitte (faccia piana sul piatto, bugne in alto [C]) e "le due slitte sono lo stesso pezzo, la destra ruotata". Nessuna modifica al CAD.
- **Esito (16 ottobre 2026, blocco a valle)**: fatta. P-092 corretto qui sopra (2.1.5, base del provino con foro pilota Ø2,5, come D-072); P-099 e P-100 nella riga di `Corpo_Slitta_Regolatore.stl` del README degli STL.

### 14. P-063: gola del fermo dei fili della tibia da 4,5

L'utente non può misurare i fili (Q-24): si progetta sulle specifiche stando larghi (D-076).
- **Script**: `zampa.py` → `fai_tibia`, gola del fermo dei fili (oggi 4,0 con 1,1 mm sotto i ponticelli): larghezza da 4,0 a **4,5**.
- **Parametri**: la larghezza della gola (nome da leggere nello script); il valore 4,5 viene da P-063 (doppino FSR 2 × 28 AWG e tre fili da 30 AWG occupano 3,3-4,05 mm; 0,45 mm di margine).
- **Verifica**: procedura della zampa; parete residua accanto alla gola e ponticelli; sentinella sui volumi della tibia.
- **BOM**: nessun impatto. **Guida**: 6.08. **Documenti**: `docs/predisposizioni.md` (X5, X31) se riporta la larghezza.
- **Esito (16 ottobre 2026, blocco zampa)**: fatta. `tib_fermo_w` 4,5 (centro `tib_fermo_y` 6,4 invariato): gola da Y 4,15 a 8,65, profonda 0,8 (sotto restano 1,2 di parete); dalle punte dei rombi (Y 3,49) 0,66; verso l'orlo (Y 9,45) resta una fascia di 0,8. I ponticelli vanno da Y 3,35 a 9,45, a filo dell'orlo, e sotto hanno ancora 1,1. Tibia −15,76 mm³ (gola 0,5 × 0,8 × 45,4 = 18,16, ponticelli più larghi +2,4). Parametro aggiornato senza rifare la tibia.

### 15. P-008: ToF posteriore avvitato, ritegno dell'altoparlante

Decisione (D-076, Q-09): il ToF posteriore si avvita (non essenziale, ma meglio); microfoni con colla a caldo fuori dal percorso del suono.
- **Script**: `corpo.py` → `fai_carapace_predisposizioni`, piano del ToF posteriore a 35°: **due fori pilota Ø1,7** per viti M2 (come la piastrina IMU), nelle posizioni dei fori della Pololu VL53L1X #3415, **da leggere sul disegno del produttore** prima del CAD (le quote di Q-33 sono del VL53L7CX, un'altra scheda). Dietro la guancia dell'altoparlante (sporge 3,3 mm): una linguetta o due costole di ritegno, senza chiudere il corridoio di 25 mm con cui si infila da dietro (D-074).
- **Parametri**: interasse e diametro dei fori del ToF; spessore della linguetta.
- **Verifica**: `carapace_predisposizioni`, `interferenze` (ToF, vite, altoparlante, ritegno), `sfilamento`; la testa della vite M2 e la sede del ToF non toccano la feritoia né il fascio; sentinella sui volumi del carapace.
- **BOM**: viti M2 dal kit (D8); nessun acquisto. **Guida**: 13.09, 13.11-13.13 (viti del ToF; colla solo per i microfoni).
- **Documenti**: `docs/predisposizioni.md` (X19: "due perni o un inserto M2" diventa "due fori pilota per M2").
- **Esito (16 ottobre 2026, blocco corpo)**: fatta. Disegno Pololu del #3415 (VL53L0X/L1X carrier, vista dal basso): scheda 0,5 × 0,7 pollici, due fori Ø2,18 a 0,5 pollici sul lato opposto ai pin, a circa 2,54 dai bordi (letti sul disegno, S). Due fori pilota Ø1,7 (`cor_tofp_pilota`) perpendicolari al piano inclinato, a ±6,35 lungo la scheda e a y 22,21 (pin verso il centro), fatti con una primitiva nuova di `lib_cad.py` (`foro_obl`: mezza sezione e rivoluzione attorno all'asse). Viti M2 × 5 dal kit: teste (Ø4 × 1,6) e punte (1,4 oltre il piano) libere; la testa resta più bassa del sensore e a 5,5 mm dal suo bordo, fuori dal fascio. Controllo: un gambo Ø2 nel foro tocca (1,31 mm³, quanto vale un foro tondo Ø1,7), Ø1,6 no. Altoparlante: le guide si allungano fino alla faccia interna e due costole di ritegno (1,2 × 2,5, `aud_rit_sp`, `aud_rit_h`) coprono il bordo a filo (la stretta la dà la stampa, D-056): l'altoparlante si infila ancora da dietro (spostato di 3, 8, 15 e 25 mm verso la coda non tocca nulla); controllo: spostato di 0,1 verso il centro tocca le costole. Lo spessore dell'altoparlante resta C (`aud_altt_sp` 4).

### 16. P-007: rebbi dello sportello più lunghi sul pacco misurato

Il pacco misura 139,65 mm (Q-17): fra la battuta anteriore del tunnel (X 79) e la punta dei rebbi (X −68,4) ci sono 147,4 mm, quindi 7,75 mm di corsa.
- **Script**: `corpo.py` → `fai_sportellino`, `cor_sport_rebbio` da 17 a circa **22**: per un solo strato di schiuma EVA da 3 mm (D10) sulla faccia anteriore del pacco restano 147,4 − 5 = 142,4 mm contro 142,65 con la schiuma (compressione richiesta 0,25 mm [S]; il valore esatto si sceglie nel modello).
- **Verifica**: `sportello`, `controllo`, `interferenze`; che i rebbi allungati non tocchino T-plug e F1 (x −83…−61) né i cavi del pacco nelle tacche aperte della modifica 11; sfilamento dello sportello con il pacco dentro.
- **BOM**: D10 resta (un solo strato). **Guida**: 11.02, 11.05. **Documenti**: D-051.
- **Esito (16 ottobre 2026, blocco corpo)**: fatta. Il valore è il parametro: `cor_sport_rebbio` 22,5 (non 22: con il pacco misurato e la schiuma la compressione è 0,75 mm invece di 0,25, che sta dentro la tolleranza di stampa). Punta dei rebbi a x −62,9: 2,9 mm dal pacco del modello (139), 2,25 dal pacco vero (139,65) con 3 di schiuma. Sportello +598,40 mm³ (due rebbi 4 × 13,6 × 5,5 in più), sfilamento dello sportello libero a 5, 10, 20 e 25 mm; nessuna interferenza con T-plug, F1 e cavi (i rebbi stanno sotto il tetto, a |y| 10-14). **Corretta dopo la verifica** (18, punti 3 e 4): rebbi fino a z −19,9, pacco da 139,65 con la schiuma nel modello.

### 17. Documenti da correggere con la 2.1.7 (dalle risposte)

- `docs/progetto-meccanico.md`: vassoio in PLA (oggi "in PETG", P-088); T-plug come in P-089 (già in `decisioni-arresto2.md`); colonne del vassoio (modifica 1).
- `docs/software.md` 6.7: assetto di partenza 100/45 a coppie, poi tripode lento (P-046); soglia del cicalino a 3,3 V per cella (P-066).
- `cad/stl/README.md`: lunette dei microfoni in PLA, colore libero.
- `docs/dimensioni-componenti.md`: dati misurati della batteria (139,65 mm, cavo 110 mm, T-plug femmina, positivo sul lato verticale) e inserti del kit (zigrinatura Ø4,2 e invito Ø4,0 per l'M3, Ø3,2 e Ø3,0 per l'M2).
- `CLAUDE.md`: stato e aperti alla chiusura della versione (voci già risolte dall'utente tolte da "Aperti": carica, scheda del carapace, lunghezza del pacco, sesso del T-plug, inserti, squadretta di prova).
- **Esito (16 ottobre 2026, blocco a valle)**: fatta, tranne `CLAUDE.md` (chiusura).
  - `docs/progetto-meccanico.md`: vassoio in PLA su colonne con asola e ala, fessure aperte e rebbi da 22,5, elenco dei cambiamenti del corpo, lamatura e foro da 7,7 del guscio, sede luci 50,5, gola 4,5, stretta del piedino, massa 3047,2 g. T-plug come in P-089: la riga di `Corpo_Sportello` e il vano di coda lo dicevano già.
  - `docs/software.md`: B6 con l'assetto di partenza 100/45 a coppie e poi il tripode lento (P-046); riga del cicalino a 3,3 V per cella (P-066). Il testo non aveva una sezione 6.7 con quell'assetto: l'ho messo nella tabella delle procedure di banco, che è `6.7`.
  - `cad/stl/README.md`: lunette in PLA colore libero, i tre STL del piedino, la dima, il provino degli inserti, bussola ed estrattore, slitte (P-099, P-100), fondo dell'anello a due pixel per sede.
  - `docs/dimensioni-componenti.md`: batteria misurata (139,65 mm, cavo 110, T-plug femmina, positivo sul lato verticale), inserti del kit (Ø4,2 / 4,0 e Ø3,2 / 3,0), 25,4 dei pin, testata e spina Würth, Pololu #3415.
  - Rimandi a D-076 in D-051, D-053, D-054, D-055, D-064, D-066 e D-074; `docs/cablaggio.md` (3.4, 3.5, 4: scheda, catena con le lunghezze dei tratti, ToF, sfilamento del pacco), `docs/predisposizioni.md` (2.3, 2.8, X2, X13, X19, X31 e i punti del CAD), `docs/BOM.md` (B18 già tolto; viteria e inserti riconteggiati: M3 × 6 48, M2 svasate 16, inserti M3 90 e M2 32).

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
- **Esito (16 ottobre 2026)**: testi e immagini rifatti da quattro estrattori in parallelo, poi riconciliati (`controlla` completo verde, `pytest tests`, build completa). Chi ha chiuso cosa (in `guida/problemi.md` lo Stato delle voci dice "chiuso" o "in parte nei testi"):
  - **banco ed elettronica** (sezioni 4, 5, 8, A.15-A.19): P-003 (con le sezioni 0 e 3 da zampa e stampa), P-005, P-072, P-085, P-050 per 5 e 8, P-019 (testi dell'asola), P-073; in parte P-002 (A.17, A.18 e `schemi.md` 2 restano della 2.1.6: disegno della scheda da rifare), P-140 (4.15; il CAD resta alla 2.1.8), P-026 / S-07 (manca la misura sulla scheda vera).
  - **batteria e accensione** (sezioni 11, 12, 15 e 0.06): P-001, P-007, P-031, P-050 per la 12, P-066 (12.04); in parte P-041 (i valori di carica non sono ancora in `docs/dimensioni-componenti.md`). Dubbi dell'arresto 2 su 0.06, 11.01 e 15.04 chiusi.
  - **carapace e collaudo** (sezioni 13, 14): P-008, P-010, P-046, P-066 (13.14), P-117, P-002 e P-140 per 13.16, 13.17, 13.19; dubbio del palmo in 14.09 chiuso (NTC dei regolatori e PLA a 55-60 °C, D-065).
  - **zampa e stampa** (sezioni 0, 1, 2, 3, 6, 9): P-014, P-015, P-016, P-050 per 0 e 9, P-057, P-058, P-062, P-063, P-065, P-077, P-078, P-088, P-111; dubbio dell'alimentazione del tester (9.08) chiuso con una fonte a parte [C], domanda all'utente in `guida/problemi/zampa_corpo.yaml`.
  - **riconciliazione**: 13.17 rimanda ai fori Ø 2,2 trapanati in 4.22 invece di farli ritrapanare a Ø 2,6.
  - Dubbio della modifica 12 chiuso: i testi seguono il CAD (scheda da x 29,5 a 51,0, larga 21,5 lungo X dal bordo della testata, testata sotto sul bordo di coda); in `rif_componenti.py` `sch_sp` = `sch_pcb` + `sch_test_h` = 1,6 + 9. Problemi nuovi nei file `guida/problemi/{banco,batteria,accensione,carapace,zampa_corpo,prima}.yaml`.

### Verifiche a valle (una volta, alla fine)

- Corpo (modifiche 1, 3, 8, 11, 12, 15, 16): `controllo`, `interferenze`; coxe a ±35° e a 30,5° fra vicine; `carapace_zampe`, `sfilamento`, `campo`; `ciclo` a 100/45 e 70/70 a gruppi di fasi.
  - **Esito (16 ottobre 2026, blocco corpo)**: copia di ripristino "Hexapod v2.1.0 - ripristino 2.1.6 (prima della 2.1.7)" (lineage `urn:adsk.wipprod:dm.lineage:o79LLOHlSzmXdBn2HiYE1A`, versione 1, copia della 14). `controllo` 0 su tutte le istanze; nessuna interferenza; timeline senza problemi, schizzi vincolati. Coxe libere a ±35° una alla volta; fra vicine libere a 30,5° su tutte e quattro le coppie e **a contatto a 31° su tutte e quattro** (D-071 diceva AD–MD libere a 31°: le zampe non sono cambiate, da guardare con la zampa). `carapace_zampe` come nella 2.1.6: 3,96 mm sulle medie a +35°, 4,76 a −35°, 7,1 sulle altre. `sfilamento` e `campo` liberi. `ciclo` libero a 100/45 (8 fasi) e a 70/70 (16 fasi). Sentinella: cambiano solo base (+743,92 mm³), vassoio (+109,89), carapace (+200,08), sportello (+598,40) e `Rif_Scheda_Carapace` (4797,61, quattro corpi), tutti uguali al calcolo a mano; zampe, attrezzi e le altre parti invariate. Il documento non è salvato (lo salva la chiusura).
- Zampa (modifiche 4, 6, 9, 14): `giunti`, `limiti`, `misura`, `interferenze`, `scansione` (81 libere, 17 controlli su 20 che toccano).
  - **Esito (16 ottobre 2026, blocco zampa)**: nessuna parte rifatta, quindi i giunti sono quelli di prima: `giunti_mancanti` vuoto, 23 giunti nella zampa (21 rigidi, 2 di rotazione), `calibra` come prima (+10 sul femore dà α −10, sul ginocchio γ 80), limiti rimessi, `misura` 0/90, `controllo` 0 su tutte le istanze. Interferenze: nessuna nella zampa e nessuna nell'assieme (`controllo` 0 sulle 39 istanze del corpo). `scansione`: 81 pose libere su 81; 17 controlli su 20 toccano (14 contro la coxa, 3 fermati dai limiti), liberi 0/41, 15/37 e 20/35, come prima. Sentinella: cambiano solo la tibia (−65,65 mm³ = 36,03 + 13,85 + 15,76) e il guscio (−13,06 per differenza booleana); piedino a stretta zero uguale alla 2.1.6; il resto invariato; timeline senza problemi, schizzi vincolati, nessuno snapshot pendente. Massa: nel modello (`cad.json`, stima con pareti e riempimento) il guscio passa da 15,70 a 15,68 g e la tibia da 36,50 a 36,52 g a zampa, cioè nessuna variazione sul segmento (111,9 g); il calo di volume del guscio (−13 mm³) e della tibia (−66 mm³) è sotto la precisione di quella stima. Documento non salvato.
- Attrezzi (5, 7, 10): `verifica_dime` e verifiche dei pezzi nuovi; tutti in libreria e nascosti.
  - **Esito (16 ottobre 2026, blocco attrezzi)**: cinque componenti nuovi in libreria (y 1000), tutti nascosti, quattro gruppi nella timeline (343 voci, nessun problema, nessuno snapshot pendente): `Attrezzo_Provino_Inserti`, `Dima_Calettamento`, `Attrezzo_Bussola_Perno`, `Attrezzo_Estrattore_Asta` e `_Tubo`. 18 parametri nuovi `att_bus_*`, `att_estr_*`, `att_tubo_*`. `verifica_dime` per le tre dime (urti solo con la lama B, che si toglie), `verifica_bussola`, `verifica_estrattore`, con i casi di controllo nelle modifiche 5, 7 e 10. Sentinella: rispetto alla fine del blocco zampa cambiano solo i cinque componenti nuovi; il resto è invariato. Documento non salvato.
- Sentinella sui volumi delle parti non toccate; caso di controllo per ogni interferenza nuova.
- A valle: `colori.py`, `esporta_stl.py` (con le varianti del piedino), `esporta_mesh.py`, `esporta_robot.py` (`geometria`, `mesh`, `pose`), `tools/descrizione.py --aggiorna-hash`, generatori; ruff, pytest, ctest, `npm test`.
  - **Esito (16 ottobre 2026, blocco a valle)**: fatto sul documento "Hexapod v2.1.0 v14" non salvato (nessun giunto mosso: coxe a 0, snapshot non pendente, `pied_stretta` a 0, timeline di 343 voci senza problemi).
    - `colori.py`: tutti i componenti, compresi i cinque attrezzi nuovi e i quattro corpi della scheda del carapace.
    - `esporta_stl.py`: 41 file fra parti e attrezzi più i tre del piedino (`Piedino_stretta_0.stl`, `_0.2.stl`, `_0.4.stl`: volumi calcolati dagli STL 1554,4 / 1710,8 / 1860,3 mm³, come il modello; `Piedino.stl` uguale al primo). Cambiano `Corpo_Base`, `Corpo_Carapace`, `Corpo_Sportello`, `Corpo_Vassoio`, `Cover_Tibia`, `Tibia`; nuovi i cinque attrezzi e i tre piedini.
    - `esporta_mesh.py`, `esporta_robot.py` (`geometria`: 74 parti, `mesh`, `pose`: 75 pose, l'unica differenza è il nome del documento) e hash `aab061b55d73`; generatori rifatti dopo l'aggiornamento di `robot.yaml`.
    - Test: `ruff` pulito, `pytest tests sim/tests` 72 passati, `ctest` 4 su 4, `npm test` 3 su 3.
- Massa: cambia di pochi grammi (via 4 distanziali da 5 e 4 M3, più 4 colonne di PETG-CF e 4 M2): aggiornare `calc/statica_tripode.py` e `robot.yaml` (`massa.attesa_g`, `regressione_statica`) solo se la differenza si vede nel totale.
  - **Esito (16 ottobre 2026, blocco a valle)**: il modellato passa da 2685,0 a 2687,2 g (solo il segmento del corpo: 1069,4 → 1071,5; le zampe non cambiano: guscio 15,70 → 15,68 g e tibia 36,50 → 36,52 g, segmento della tibia 111,9 g invariato; il +2,2 del totale è il corpo +2,1 e l'arrotondamento) e il totale atteso da 3045,0 a **3047,2 g**: +2,2 g, come le 1,5 g di D-071 → D-074 che si erano riportate. Aggiornati `calc/statica_tripode.py` (`CONFIG['massa_g']`) e `robot.yaml` (`massa.attesa_g`, `femore_kgfcm` 5,84 → 5,85; la frazione resta al 53 %, dentro 52,5–54,5 %); i generatori ne hanno preso la massa. La regressione passa (`test_statica`).
- Guida: `esporta_guida.py` (`manifest`, `mesh`, `fori`, `zone`, `controllo`), poi `.venv/bin/python -m guida.costruisci controlla`; registro dei problemi aggiornato dall'utente (non da qui).
  - **Esito (16 ottobre 2026, blocco a valle)**: `manifest` (71 componenti, 96 occorrenze), `mesh` (tutti, compresi i cinque attrezzi nuovi), `fori`, `zone` (246, nessuna mancante) e `controllo` (nessuna mesh mancante, nessuno scarto) fatti. Con i dati nuovi `controlla` e due test di `tests/test_guida.py` davano rosso, come previsto: la guida seguiva ancora i distanziali. Corretti **solo i dati** che il CAD ha cambiato, senza rifare i testi della guida (che restano al punto "Testi della guida dopo la 2.1.7"):
    - catalogo: `giunzioni.yaml` (`vassoio`: M2 × 5 svasata nell'inserto M2 della colonna, foro passante M2 nel vassoio, niente distanziale) e `viteria.yaml` (M3 × 6 48, M2 × 5 svasate 16, inserti M3 90 e M2 32, come `docs/BOM.md`);
    - passi: 8.11 (colonne e M2 svasate, senza l'avviso bloccante di S-19), tabella e note di 3.12 e 3.x degli inserti, appendici A.12 e A.13 (la riga delle bugne M3 del vassoio esce), inventario di 0.17 (B18 e i totali), 7.0x (lettera E), 15 (tabella dello smontaggio), glossario ("vassoio").
    - `controlla`: tutti i controlli verdi (giunzioni complete, totali viti e inserti, teste del lato A con il caso negativo, montaggio unico, giunzioni usate, decisioni). **Controllo lunghezze**: `guscio_tibia` presa 7,04 e fondo libero 0,66, come atteso. Vassoio: l'avviso "vite a −0,30 dal fondo" è un artefatto della convenzione della guida, che mette la testa delle svasate sul fondo del cono (0,9 più in basso della testa vera): con la testa a 0,1 sotto la faccia la punta resta 0,5 sopra il fondo del foro (4,0) e la presa è 3,5 (3,4 e 0,6 con la testa a filo, come nel piano). Stessa convenzione per `piastrina_imu` e `lama_b`: da correggere nella pipeline quando si rifanno i testi.
    - Restano da rifare i testi e le immagini di 4.04 e delle altre voci dell'elenco "Testi della guida dopo la 2.1.7" (le note di S-19 in 04-banco parlano ancora delle teste M3 del vassoio).

### 18. Correzioni della verifica geometrica (16 ottobre 2026)

La verifica geometrica della 2.1.7 (file Fusion salvato come versione 15, "2.1.7 in corso") ha dato 3 rilievi importanti e 8 minori; l'utente ha dato il via alle correzioni. Verifiche nuove in `assieme.py`, tutte con corpi o scatole provvisorie e in sola lettura: `spine_prese`, `qwiic_adc`, `qwiic_asola`, `spina_staccata`, `cavo_piatto`, `cavi_rebbi`, `led_spie`, `urti_scatole`.
1. **Ala del vassoio sopra la fila delle prese dei piedi** (modifica 8). Prima: con l'ala a x 45–55 le spine JR infilate dall'alto toccavano il vassoio (`spine_prese`: 18,36 mm³, il caso di controllo). La proposta (asola a x ≈ 70) non va: la spina Qwiic dell'ADC nella presa di testa (x 69,5) tocca la colonna del vassoio a (75; 12,5) anche senza fili (1,78 mm³ con Ø6, 3,65 con Ø6,6). Scelta: **asola a x 30** (`cor_vas_asola_x`; asola 26,5–33,5, ala 25–35), dietro la colonnina del carapace (da x 36,3), e cavetto nella presa di coda dell'ADC (x 39), libera con 2 mm di fili dritti (a 0,7 dalla colonna di (30; 12,5)); il percorso dall'asola alla presa è di circa 9 mm invece di 31. Esiti: spine libere su tutte e due le file; ala libera, gioco 1,30 dalla colonnina (1,25 libero, 1,35 tocca); spina Qwiic 6 × 2,9 libera nell'asola, 7,2 × 4,2 tocca il vassoio (3,58 mm³). Vassoio +0,8 mm³ (l'ala sporge 1 mm dietro il piano). Nella guida cambiano solo i dati: etichetta dell'asola in 8.07 e presa di coda dell'ADC in 8.09; il resto dei testi di P-019 resta ai "Testi della guida dopo la 2.1.7".
2. **Chiave della spina IDC e cavo piatto** (modifica 12). Scheda alzata di 0,6: bugne alte 2,9 (`sch_bugna_h`), foro dell'inserto profondo 3,4 (`sch_ins_l` = bugna + dorso − fascia − 0,5: sotto la fascia restano 0,5 come prima; un primo 3,7 lasciava 0,2 e l'ho corretto), viti della scheda **M2 × 4**. Chiave a z 21,4, 0,54 sopra le USB-C. `spina_staccata` (2, 4, 6, 8 mm verso la coda): libera con scarto di fianco 0, ±0,3 e ±0,5; controllo: con la scheda all'altezza di prima e 0,3 di fianco tocca la USB-C a ogni corsa (come trovato dalla verifica). **Cavo piatto**: il nastro intero non ha un percorso libero (sotto le USB-C, davanti la testata, dietro la zona delle spine dei servo; una piega a 45° larga 20,3 non sta fra spina e testata); `cavo_piatto` ne trova uno con il nastro diviso in due strisce da 8 dopo il fermacavo (`cablaggio.md` 3.5bis): libero; controlli: 0,4 più in alto tocca la battuta dell'ottagono (z 32,8), 0,3 verso il centro tocca il PCB dell'ESP32. Le pieghe sono S: vanno provate sul pezzo; la riserva è la soluzione B di P-002, da far scegliere all'utente. Carapace −35,24 mm³ (bugne più basse, calcolo 4 × 0,6 × 14,68).
3. **Rebbi dello sportello** (modifica 16): cima dei rebbi a z −19,9 (`cor_sport_rebbio_luce` 8,5: due cavi Ø4 uno sull'altro più 0,5, invece della proposta −19,5 che lasciava i due cavi a contatto). `cavi_rebbi` (cavi piegati dal centro alla fessura, sotto la linguetta dello sportello e poi sotto il tetto): liberi; controllo: 0,5 più in basso il secondo cavo tocca i rebbi (1,60 mm³); con i rebbi di prima toccavano. Sportello −810 mm³ (4 × 4,5 × 22,5 × 2).
4. **Batteria**: `bat_l` 139,65 e corpo `schiuma` da 2,25 (`bat_schiuma`) davanti, pacco da x −62,9 a 76,75. Pacco, schiuma, battuta e rebbi si toccano: pacco 0,05 più indietro interseca i rebbi (3,64 mm³ = 72,8 mm² × 0,05), schiuma 0,05 più avanti interseca base e chiglia; gioco dei rebbi 0, con la schiuma compressa di 0,75. `sfilamento_pacco`: spina a destra libera da 0 a 165 mm; spine già fuori libere; spina a destra alta 1 mm in più libera; controlli come prima (spina alta 4,3 in più tocca il cicalino, cavi Ø5 toccano la fessura).
5. **T-plug a sinistra**: confermato, fra 10 e 20 mm tocca il ToF posteriore (13,85–20,61 mm³) e il carapace (16,69). Scritto in `cablaggio.md` 4 e nella guida 11.03 (metà femmina fuori dal lato destro).
6. **LED delle spie e F1**: l'ingombro di F1 è 40 × 22 × 15 stimato (S), e la forma vera del Neuftech non è pubblicata (cercata il 16 ottobre: nessun disegno). Corretto sul caso peggiore: lamatura del colletto Ø4,2 × 1 sulla faccia interna delle linguette (`luc_spia_col_d`, `luc_spia_col_h`; passo `lamature_spie`, una volta, e in `fai_base_predisposizioni` per i rifacimenti): il LED (Ø3 × 5,3 col colletto Ø3,8 × 1, S) sporge verso la porta e resta a 0,6 da F1. `led_spie` libero; controllo: LED senza lamatura (colletto contro la faccia) tocca F1 (4,54 mm³ per LED). Restano i reofori, da guardare sul portafusibile in casa (`cablaggio.md` 5, punto 8). Base: −12,61 mm³ per le lamature. La guida classifica la lamatura come foro del LED (`catalogo/fori.yaml`): ha il diametro dell'inserto M3.
7. **Colonne Ø6,6** (`cor_vas_col_d`): parete 1,6 attorno all'inserto. Giochi per bisezione con un cilindro provvisorio: IMU e piastrina 1,2 (1,15 libero, 1,25 tocca), ADC 2,2 (2,15 / 2,25), carapace 4,65, le altre oltre 4,7. Base +118,75 mm³ (4 × 5 × π/4 × (6,6² − 6²)), con le lamature +106,14, come misurato.
8. **Viteria del BOM** (riga delle predisposizioni): due M2 × 5 del ToF posteriore nei fori pilota; viti della scheda del carapace M2 × 4.
9. **Estrattore**: la guida 15.10 e 15.11 dice di controllare o sostituire il cuscinetto estratto (l'asta spinge sull'anello interno).
10. **D-071**: nota datata (vicine a 31° a contatto su quattro coppie su quattro, AD–MD 18,94 + 13,55 = 32,49 mm³; a 30,5° libere), rifatta qui sul modello: stessi numeri della verifica. Procedura di `cad/CLAUDE.md` corretta.
11. **P-015**: vedi la modifica 5, "Scelta dell'utente".
- **Carapace rifatto**: dopo lo spostamento di due istanze nel corpo (batteria e scheda, con `pulisci_istanze` e `istanze_nuove` a tolleranza 0,1) il ricalcolo della timeline ha lasciato in avviso i raccordi in pianta e lo smusso del carapace: il lobo PD è diventato uno spigolo vivo (x −112,3, +677 mm³), senza errori. Rifatto con `carapace`, `carapace_dettagli`, `carapace_predisposizioni`: ingombro di nuovo ±110,44, timeline senza problemi, `carapace_zampe` come prima (3,96 / 4,76 / 4,79 / 6,17 sulle medie), `sfilamento` libero a 5–40 mm, `campo` libero (controllo a +8° tocca visiera e fascia).
- **Assieme**: `controllo` 0 su 39 istanze, nessuna interferenza, coxe a 0, nessuno snapshot pendente, timeline senza problemi, schizzi vincolati. Sentinella rispetto all'inizio: cambiano solo base (+106,14), carapace (−35,24), sportello (−810,00), vassoio (+0,80) e `Rif_Batteria_2S5200` (tre corpi); il resto invariato.
- **A valle**: `colori.py`; `esporta_stl.py` (cambiano solo base, carapace, sportello e vassoio); `esporta_mesh.py`; `esporta_robot.py` (`geometria`, `mesh`, `pose`); massa attesa da 3047,2 a **3046,2 g** (corpo 1071,5 → 1070,6; femore sempre 5,85 kgf·cm, 53 %) in `calc/statica_tripode.py` e `robot.yaml`; hash e generatori; `esporta_guida.py` (`manifest`, `mesh`, `fori`, `zone` 246, `controllo` senza scarti) e `guida.costruisci controlla` verde (resta l'avviso noto della vite svasata del vassoio); ruff, pytest (72), ctest (4 su 4), `npm test` (3 su 3).

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
- **Esito (16 ottobre 2026)**: fatta. File Fusion salvato come versione 16 ("2.1.7: correzioni dalla guida di montaggio (D-076, D-077)"); `VERSIONE` e `robot.yaml` a 2.1.7; `geometria` riletta (`cad.json`: "Hexapod v2.1.0 v16", cambia solo l'intestazione), hash e generatori; ruff, pytest (72), ctest (4 su 4), `npm test` (3 su 3), `guida.costruisci controlla` verde con l'avviso noto del vassoio. D-077, `docs/versioni.md`, `CLAUDE.md`, tag `v2.1.7`.

## Seguito: versione 2.1.8 (proposte, 16 ottobre 2026)

> Proposte: non si parte senza il via dell'utente. Il piano dettagliato si scrive qui prima di partire.

**Minori della seconda verifica geometrica della 2.1.7** (D-077, registro `guida/problemi.md`):
1. **P-139, reofori dei LED delle spie (X13) a 0,6 mm da F1**: spostare F1, la coppia di T-plug e le costole di +2,5 verso la testa (oggi 3,0 mm dal 2813), oppure leggere prima il portafusibile Neuftech vero (Q-23). Il ripiego di `cablaggio.md` 5, punto 8 ("si piegano lungo la linguetta") non è fattibile: va corretto.
2. **P-140, cavo piatto in due strisce a 0,25 mm dal PCB dell'ESP32 e a 0,3 dalla battuta dell'ottagono**: far scendere le strisce 1,0 mm più verso l'esterno, con `cavo_piatto` e i suoi casi di controllo; nei testi della guida (4.15, 13.19) la divisione in due strisce e la crimpatura.
3. **P-141 (P-012), prese dei piedi**: quando si disegnano, l'ingombro delle spine JR (circa 7,6 × 2,5) resta a y ≥ 17,6; verifica con `spine_prese`.
4. **ESP32 RE1.3 col retro giusto** (immagini dell'inserzione e foto dell'utente, 18 ottobre 2026, `docs/immagini/scheda2/`; dettagli in `piano-pcb.md`, esiti di F0): in `Rif_ESP32_S3_CAM` la sede della microSD va verso l'antenna (x ≈ 57…73 nel robot), non verso la coda; vanno aggiunti AMS1117 e tantalio verso le USB (x ≈ 20…28); le file dei pin vanno circa 1,6 mm più verso la testa rispetto al PCB (primo pin a circa 2,6 dal bordo di testa). Da ripetere le verifiche che lo toccano: spina della scheda del carapace sulle USB-C, cavo piatto, regolatore e PTC sotto l'ESP32 (S-08). **Prima**: misure col calibro sulla RE1.3 (lunghezze, distanza dei pin dai bordi, altezze del retro).

**Testi della guida dopo la 2.1.7**: fatti il 16 ottobre 2026 (esito nella sezione 2.1.7; restano le parti "in parte" di P-002, P-026, P-041, P-140). Era: tutto l'elenco della sezione 2.1.7 ("Testi della guida dopo la 2.1.7": P-003, P-005, P-002, P-001, P-007, P-008, P-031, P-050, P-088, P-078, P-072, P-066, P-046, P-085, P-077, P-111, P-010, P-058, P-117 e i dubbi della revisione dell'arresto 2), con le immagini rifatte sulla 2.1.7. Nella 2.1.7 sono cambiati solo i dati che seguono il CAD (catalogo, totali, 8.07, 8.09, 8.11, 11.03, 15.10, 15.11). In più la convenzione della guida per le viti svasate (testa sul fondo del cono: avviso del vassoio, `piastrina_imu`, `lama_b`), da correggere nella pipeline con i testi.

### Piano della 2.1.8 (18 ottobre 2026, approvato dall'utente la sera stessa; **fatta**, D-081, tag `v2.1.8`)

Contiene le voci 2, 3 e 4 qui sopra e la PCB-P (`piano-pcb.md` 5.3, fase F2). La voce 1 (P-139) entra solo se arriva la forma del portafusibile Neuftech (Q-23), altrimenti passa alla 2.1.9. La basetta e la scheda del carapace **non cambiano** nel CAD: le PCB si provano con scatole provvisorie in F4.

**Prima di partire**: copia di ripristino "Hexapod v2.1.0 - ripristino 2.1.7 (prima della 2.1.8)" (`DataFile.copy`, rinominata subito: `cad/CLAUDE.md`), aggiunta in `CLAUDE.md` fra i file da non toccare. Il tag `v2.1.7` c'è già.

| Blocco | Voce | Cosa | Dati dell'utente | Uscita |
|---|---|---|---|---|
| A | P-140 | strisce del cavo piatto 1,0 mm più verso l'esterno e più in basso, con `cavo_piatto` e i suoi casi di controllo. **Fatto**: 1 mm verso −Y, 1,25 dal PCB dell'ESP32; più in basso non si può (tocca la spina) | nessuno | gioco dal PCB dell'ESP32 e dalla battuta dell'ottagono sopra 1 mm |
| B | PCB-P, P-141 | due varianti come scatole provvisorie con `urti_scatole`, ognuna con il caso di controllo: **P1** tasca accanto all'IMU (PCB circa 20 × 10, due M2; passaggi dei fili sotto l'ADC e fra ADC e colonna); **P2** sotto le prese dei piedi (y circa 19…25,5, bugne da 4, spine 3,5 mm più alte contro vassoio, cavi e servo di coxa AS a tutta l'escursione) | misura della spina JR (Q-04): senza, P2 si scarta e si fa P1 | esito delle due prove; **arresto DU-5**: l'utente sceglie. **Prove fatte** (`assieme.py` → `partitori_varianti`, 18 ottobre): P1 libera (scheda 10 × 20 nella tasca, fili sotto l'ADC a x 57…61); controlli: scheda da 11,6 urta la piastrina dell'IMU, fili a x 64…68 urtano la bugna dell'ADC. P2 libera con la scheda a x 44,2…72, y 19…26,5 e le spine JR innestate (y 18,6…26,6, fino a z 12,7), anche contro le zampe nella posa di riferimento; controlli: scheda da x 43 urta la colonnina del carapace, spine a y 21 urtano basetta e ADC |
| C | PCB-P | **Fatto (D-080, P2)**: `Rif_Partitori`, bugne M2, sede delle prese dei piedi tolta, istanza nel corpo, nessuna interferenza; Fusion salvato. Variante scelta: bugne con inserti M2, `Rif_Partitori` in `LIBRERIA` e nel passo `ingombri`, `fori.json` e `manifest.json` rigenerati; con P2 le prese dei piedi su `spine_prese` | — | `genera_contorni.py` con la scheda `partitori` |
| D | voce 4 | **Fatto** con le quote in pianta del disegno dell'inserzione e le altezze massime dei datasheet (S; l'utente ha detto che le immagini bastano): PCB a x 12,03…74,63, antenna fino a 79,43, pin fermi; nessun urto; spina staccata libera (controllo a −1,6 tocca le USB-C), cavo piatto libero; Fusion salvato. Era: `Rif_ESP32_S3_CAM` con il retro della RE1.3: microSD verso l'antenna, AMS1117 e tantalio verso le USB, file dei pin 1,6 mm più verso la testa; poi spina del carapace sulle USB-C, cavo piatto e posto del regolatore sotto l'ESP32 (S-08) | **misure col calibro della RE1.3** (cose da guardare in `CLAUDE.md`) | quote del retro V; posto di U2 sulla PCB-B deciso |
| F | PCB-C | la scheda del carapace non contiene CE1, 24 piazzole, 6 punti di prova e R-MIC in 7,4 × 19 mm utili (F4 del PCB). Due strade provate come scatole provvisorie, con il caso di controllo: **ali** nel tratto davanti (x 45…51) fino a circa \|y\| 24, dove le mesh del CAD sono libere (le colonnine del coperchio occupano x 35…45, \|y\| 17,5…27,5); oppure scheda com'è, due fili per foro e CE1 sui fili della catena LED. Scelta delegata all'agente (18 ottobre). **Fatto**: ali fino a \|y\| 24, profonde 6 (`sch_ala_y`, `sch_ala_x`); libere fino a \|y\| 28 con 8 mm sotto, caso di controllo da x 40 che urta; nessun urto della scheda nuova; Fusion salvato | — | sagoma della PCB-C; `Rif_Scheda_Carapace` e `genera_contorni.py` aggiornati |
| E | a valle | viteria e inserti nel BOM; catalogo della guida; `esporta_guida`, `guida.costruisci controlla`; passi 7.10, 8.09, 8.10 | — | CI verde |

**Ordine e arresti**: A e F subito; B (la spina JR è misurata: 8 × 3 × 14), poi l'arresto DU-5; C dopo la scelta; D quando arrivano le misure della RE1.3 (se tardano, la 2.1.8 si chiude senza D e la voce passa alla 2.1.9, ma il piazzamento della PCB-B aspetta D); E e la chiusura alla fine. Ogni blocco lascia Fusion salvato e la repo committata.

**Verifiche di fine versione**: controllo dell'assieme e sentinella sui volumi, interferenze sulla posa di riferimento, `cavo_piatto`, `spine_prese`, `urti_scatole` delle schede; CI verde; decisione D-0xx; `versioni.md`; salvataggio in Fusion; tag `v2.1.8`.

**Durata** (S): 2–3 blocchi di lavoro in Fusion, più l'attesa delle misure.

### Proposta della 2.1.9 (18 ottobre 2026, da approvare)

Dalla revisione indipendente (D-082). La 2.1.8 è chiusa con il tag `v2.1.8`; in Fusion la 2.1.9 è già cominciata con una correzione piccola.

| Voce | Cosa | Stato |
|---|---|---|
| Ali della scheda del carapace | `sch_ala_x` da 6 a 5,5: il bordo resta a 0,8 dal tubo dei pozzetti (bisezione; a 0,9 tocca) | fatta (Fusion salvato, guida riesportata) |
| Scheda dei partitori più grande | La sagoma della PCB-P (27,8 × 7,5) non contiene i partitori: si allunga verso la testa fino a circa x 78 (foro di testa oltre i componenti, circa x 76) e si allarga ad almeno 8,6 (y 18,6…27,2). Prima un piazzamento di prova in KiCad, come per la PCB-C, per fissare la sagoma minima. Poi bugne, `Rif_Partitori`, verifiche con le coxe AS a ±35° e a 30,5° fra le vicine, gioco misurato per bisezione, a valle | da approvare |
| P-139 | reofori delle spie | aspetta il portafusibile (Q-23) |

**Arresti**: approvazione di questa proposta; poi la sagoma della PCB-P, prima di toccare Fusion.

**Prova dello spazio (19 ottobre 2026, notte, scatole provvisorie contro il corpo, z −5,9…−3,3)**:
- x 72…78 a y 18,6…27,2: tocca appena la base (0,45 mm³);
- x 78…84: urta la base (43,7 mm³);
- x 38…44,2 (coda): urta la base (93 mm³);
- y 27,2…29: urta la base;
- y 17…18,6: urta l'ADC.

La sagoma utile è circa **x 44,2…77 × y 18,6…27,2** (circa 33 × 8,6), e il pettine 6 × 3 ne prende circa 14,4 × 8,6. Fuori dal pettine restano circa 130 mm² per faccia (coda con il foro, testa con il foro). Servono 8 R e 8 C in 0805 e 14 piazzole per i fili (10 verso l'ADC, 4 delle NTC). Con gli 0805 su tutte e due le facce le piazzole a foro da sole prendono circa 90 mm²: **a passo 2,54 non ci stanno**.

Strade possibili, da scegliere con l'utente (S):
- piazzole per i fili a saldare in superficie (una faccia sola) a passo 2,0;
- 100 nF delle NTC (C7, C8) fuori dalla scheda;
- la striscia di millefori della strada B, tagliata sulla sagoma di oggi;
- reti di resistenze e di condensatori al posto degli 0805: voci nuove, e passo fine per il montaggio a mano.
