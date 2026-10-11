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

**Piano, da fare dopo il via dell'utente.** Sullo stesso design "Hexapod v2.1.0", tag `v2.1.6`, decisione D-074.

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
5. **Firmware e documenti**:
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
