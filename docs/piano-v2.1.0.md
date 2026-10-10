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
