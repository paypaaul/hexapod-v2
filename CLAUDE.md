# Hexapod v2

Robot esapode a 18 gradi di libertà (6 zampe × 3 servo MG996R), stampato in 3D, che verrà costruito davvero. Questa repo è la memoria del progetto: una sessione nuova deve poter ripartire leggendo solo questi file. **Prima di usare Fusion leggere `cad/CLAUDE.md`** (connettore, procedure, lezioni).

## Stato attuale

> Aggiornare alla fine di ogni versione o fase.

`main` è il robot vero, con i servo MG996R. La prima versione, progettata per errore attorno agli MG90S, è congelata nel branch `mg90s` e nel file Fusion "Hexapod v2 - MG90S" (`git show mg90s:<percorso>`).

| Fase | Stato |
|---|---|
| 1. Studio | fatta (8 ottobre 2026): `docs/studio-componenti.md`, `docs/dimensionamento.md`, `docs/dimensioni-componenti.md` |
| 2. BOM | v2.0 approvata; v2.1 con prezzi, link e foto (D-068) in `docs/BOM.md` |
| 3. Modelli 3D | fatta: parametri, STEP e ingombri in libreria (`cad/script/rif_componenti.py`, D-046) |
| 4. CAD | **versione 2.1.7** (16 ottobre 2026, D-077, file Fusion versione 16): correzioni dalla guida di montaggio (arresto 2, D-076). Cosa contiene ogni versione: `docs/versioni.md`. Meccanica, verifiche e masse: `docs/progetto-meccanico.md` |
| 5. BOM finale | v2.4: circa 365 € consegnati per le voci approvate, tolto quello che l'utente ha già in casa (D-073, D-076, D-078); predisposizioni X a parte (D-068) |
| 6. Verifica del movimento | da fare |

Numeri di oggi:
- massa attesa 3046,2 g, con il femore al 53 % dello stallo a 100/45;
- carapace a 3,96 mm dalle zampe medie a +35° e 4,76 a −35° (D-074: il 4,58 di D-071 non si ritrova), 7,1 dalle altre;
- zampe vicine libere a 30,5° e a contatto a 31° su quattro coppie su quattro (D-077);
- ginocchio calettato a γ 100; dopo la taratura `gamma_max` = min(177, γ misurato + 80) (P-015, D-077);
- il firmware limita la coxa a ±30° e la somma fra vicine a 56°. Il valore sta in `robot.yaml` ed è ancora una proposta da approvare: D-050 e D-061 dicono 60°.

## Cosa è deciso dall'utente (non si cambia senza chiederlo)

- **Servo**: 18 MG996R di AZDelivery, gli stessi della sua v1. Li ha già.
- **Libertà di progetto**: si fa come da zero, senza limitarsi per riusare la versione MG90S.
- **Controllo**:
  - scheda UICPAL "ESP32-S3-CAM N16R8 RE1.3" (AliExpress 1005008519401021);
  - camera UICPAL "OV3660-75MM" con flat da 75 mm e lente da 120° "GOOD";
  - servo controller clone "SSC32-V2.5" (AliExpress 1005001888185034), già comprato.
- **Acquisti fatti**: solo servo e servo controller. Ogni voce del BOM va approvata. Preferire la soluzione senza componenti in più, salvo problemi funzionali o estetica sgradevole. Cuscinetti e perni li procura l'utente.
- **Batteria**: OVONIC 2S 5200 mAh hardcase della v1 (D-045). Nella v1 c'era un buck dopo il fusibile, con schede PCA9685: non si riusa.
- **Misure**: l'utente non può misurare i servo, né quote né corrente di stallo. Si progetta sul caso peggiore dei dati dichiarati e si verifica con provini stampati; non chiedere di nuovo queste misure.
- **Assetto**: marcia classica, bassa, ginocchio sotto i 90°. Accetta di superare il 50 % dello stallo; l'assetto si sceglie a robot costruito, quindi la meccanica deve permettere un campo ampio.
- **Produzione**:
  - FlashForge Creator 5 Pro (256 × 256 × 256, da confermare), toolchanger a 4 testine, ugelli temprati da 0,4;
  - materiali PLA, PLA-CF, PETG, PETG-CF; supporti al minimo;
  - stampa e supporti li controlla l'utente nello slicer.
- **Materiali** (D-065):
  - PETG-CF nero per le parti funzionali;
  - PLA per le placche, bianco per ora;
  - TPU arancio per i piedini.
  - Fascia, visiera, gonne, sportellino e intarsi delle feritoie in PLA nero: è una mia proposta, applicata nel modello ma non confermata dall'utente (D-065, BOM domanda 7).
  - Multimateriale ammesso con il toolchanger.
- **Estetica**:
  - futuristico ma minimale, un oggetto "cool" e non un assemblaggio di staffe; se c'è conflitto vince la funzione;
  - cover delle zampe: placche non strutturali in un altro colore, che non limitano i giunti e seguono la forma del pezzo sotto (D-071);
  - housing della camera integrato nel frontale.
- **Corpo**: pulsante Ø12 sul coperchio, cicalino in coda sotto il coperchio (D-059); tibia simmetrica con il piede sull'asse del femore (D-065).
- **Blender** si valuta solo dopo la fase 6, salvo le immagini della guida di montaggio (D-075).

## Regole di lavoro

- **Progetto personale**: le regole dell'organizzazione della configurazione gestita (Linear, PR, inglese) qui non valgono. Valgono solo queste.
- **Lingua**: documenti in italiano.
- **Chiedere** quello che solo l'utente sa (foto, misure sul pezzo vero, link). Per schede e servo con varianti o cloni chiedere foto o link.
- **Decisioni**: il resto si decide e si annota in `docs/decisioni.md` con il perché.
- **Riepilogo**: a fine fase o versione, breve, all'utente, diviso in verificato / assunzione / aperto.
- **Dati chiave**: si controllano su fonte primaria e si marcano verificato / stimato / da confermare.
- **Versioni**: ogni gruppo di modifiche è una versione (2.1.x sul design di lavoro).
  - Prima di partire, il piano va in `docs/piano-v2.1.0.md`.
  - Alla fine: decisione D-0xx, `docs/versioni.md`, salvataggio in Fusion, tag git.
  - Commit e push su `main` a ogni gruppo di modifiche (indicazione dell'utente).
  - La CI (`ci`, `sim`) deve restare verde.
- **Limite d'uso a finestre**: lavorare a blocchi che lasciano repo e Fusion in uno stato da cui ripartire.
- **Agenti**: flussi con più agenti solo se l'utente li chiede. Modello ed effort secondo il compito: Sonnet per ricerche e report, verificatori con effort alto.
- **Requisiti del CAD**:
  - parametri utente per le quote che contano;
  - un componente per parte;
  - schizzi completamente vincolati, giunti veri, timeline pulita;
  - giunti sostenuti su due lati con squadretta e cuscinetto;
  - servo bloccati senza gioco;
  - sezioni chiuse o nervate;
  - inserti o dadi prigionieri;
  - cover non strutturali.

## Mappa della repo

| Percorso | Contenuto |
|---|---|
| `cad/CLAUDE.md` | connettore Fusion (cosa funziona e come aggirare i problemi), convenzioni, procedure dopo una modifica, render |
| `cad/script/` | script Fusion: `lib_cad.py`, `lib_assieme.py`, `rif_componenti.py`, `zampa.py`, `corpo.py`, `assieme.py`, `attrezzi.py` (dime, cavalletto, provini), `colori.py`, `viste.py` (render, anche notturni), `esporta_stl.py`, `esporta_mesh.py`, `esporta_robot.py`, `versione.py` |
| `cad/stl/` | STL da stampare, con orientamento e materiali nel README; `cad/modelli/`: STEP di terzi (fuori da git) |
| `cad/render/` | render schematici con matplotlib (`render.py`) e ritaglio dei render di Fusion |
| `guida/` | guida di montaggio illustrata (D-075, piano in `docs/piano-guida.md`): passi in YAML, catalogo, immagini con Blender, PDF con Chrome; output in `build/guida/` |
| `docs/decisioni.md` | registro delle decisioni (D-041 e successive) |
| `docs/backlog.md` | lavori decisi o studiati ma non ancora in una versione |
| `docs/piano-pcb.md`, `docs/ricerca/pcb/` | piano dei circuiti stampati (prima serie r1) e studio da cui parte |
| `pcb/` | progetti KiCad generati da script, librerie, regole, controlli (`pcb/README.md`) |
| `docs/versioni.md`, `docs/piano-v2.1.0.md` | storico delle versioni e piani dalla 2.1.0 alla 2.1.7 |
| `docs/progetto-meccanico.md` | architettura, quote, verifiche, masse e render |
| `docs/BOM.md` | distinta base con prezzi, carrelli, foto e domande aperte |
| `docs/cablaggio.md` | tutti i cavi, connettori, piedinature e punti aperti |
| `docs/piano-elettronica-software.md`, `docs/predisposizioni.md`, `docs/software.md` | sensori, luci, elettronica, firmware, controllo, roadmap |
| `docs/ricerca/` | ricerche, concept e giudizi (zampa, estetica, placche del femore) |
| `calc/` | statica del tripode, andature, assetti, escursioni della zampa, cavi dei servo |
| `robot/`, `tools/`, `firmware/`, `sim/`, `app/` | software S0: descrizione del robot dal CAD, nucleo e firmware ESP-IDF, simulazione MuJoCo, gemello nel browser |

## Fusion

- **Progetto**: "Hexabot v2" (id `202512011021193576`), hub "Paul's team".
- **Il connettore MCP può mancare** (l'utente usa a volte un altro account): controllare che ci siano gli strumenti `mcp__Autodesk_Fusion__fusion_mcp_*`. Se mancano:
  - aggiungerlo con `claude mcp add --transport http --scope local Autodesk_Fusion http://127.0.0.1:27182/mcp`;
  - riavviare la sessione: in background `claude agents --json` dà il PID, poi `claude --resume <id>`.
- **File da non modificare né cancellare** senza chiedere:
  - `Tower Pro MG90S Micro servo` (dell'utente), lineage `WfZcQDYtQ2mcTssS11zxYw`;
  - `Hexapod v2 - MG90S`, lineage `G-L92GHuRaCuuYj8EQ4-jg`;
  - `Hexapod v2 - MG996R - ripristino tibia asimmetrica (v22)`, lineage `2kd8UmqPSSqdH-nUiwVWhw`;
  - `Hexapod v2 - MG996R` (versione 2.0.0, congelata, tag `v2.0.0`), lineage `AVxbp0QWS5m_QEugpeB99A`.
  - `Hexapod v2.1.0 - ripristino 2.1.6 (prima della 2.1.7)`, lineage `o79LLOHlSzmXdBn2HiYE1A`.
  - `Hexapod v2.1.0 - ripristino 2.1.7 (prima della 2.1.8)`, lineage `lqTyF-0xTpm2y77ASTO6Tg`.
  - I lineage hanno tutti il prefisso `urn:adsk.wipprod:dm.lineage:`.
- **Design di lavoro**: "Hexapod v2.1.0", lineage `urn:adsk.wipprod:dm.lineage:yQO8vfuxQ7uRcs6rnwK4_w`. Ha le versioni dalla 2.1.0 alla 2.1.7 (versione 16 del file).
  - Struttura (D-046): un solo file; la zampa è un componente istanziato sei volte; le parti comprate `Rif_*` stanno in libreria (y ≥ 250 mm).
  - Gli attrezzi stanno anche loro in libreria e sono nascosti.

## Lezioni dalla versione MG90S

- La coppia è carico per distanza orizzontale tra piede e asse: l'assetto si decide insieme alla geometria.
- Le escursioni dei giunti si dimensionano sull'assetto più basso con il piede alzato.
- Lo spazio per cavi, scorte e alimentazione va contato prima di fissare la pianta del corpo.
- La stabilità cresce abbassando e allargando: luce sotto il corpo e angolo di ribaltamento vanno guardati insieme alla coppia.
- **Architettura della v1 che ha funzionato** (da rivalutare in scala, non da copiare):
  - giunti su due lati con cuscinetto e perno coassiali al servo;
  - femore in due pezzi, coxa a C;
  - gondole dei servo di coxa nello scafo;
  - vasca strutturale con tunnel per la batteria e guscio non strutturale;
  - sportelli a incastro.
- Nella prima zampa l'anima piena del femore fermava il ginocchio a 62°: è servito un puntone nella fascia che le culle non spazzano.
- **Metodo**:
  - una parte alla volta;
  - verifica dopo ogni blocco, con la sentinella sui volumi delle altre parti;
  - interferenze sulla posa di riferimento, poi escursioni, poi ciclo a tripode con le sei zampe.
- **Errori da non ripetere**:
  - tagli che asportano le parti degli altri componenti;
  - istanze create in un sotto-assieme ruotato;
  - letture nello stesso script della creazione;
  - verifiche di interferenza senza un caso di controllo.

## Aperti e prossimi passi

1. **Da far decidere all'utente**:
   - voci X da comprare (luci delle tibie opzionali con il diffusore bianco, niente zaino per ora: D-076);
   - somma fra vicine a 56° invece di 60° (proposta in `docs/software.md`);
   - eventuali viti DIN 7984 a testa bassa sotto la lama A: la lama passa da 4,0 a 3,0 mm, il contatto fra vicine sale verso 31,25° e la massa cala di pochi grammi. Cambiano 72 viti del BOM (D-070).
2. **Aperti tecnici**:
   - coppia a 70/70 oltre la soglia della guardia (`docs/software.md`);
   - fori e chip dei circuiti marcati C;
   - cablaggio, sezione 5: ramo delle tibie e tetto di corrente;
   - T-plug da provare a mano sul primo carapace, con il ToF posteriore montato; spina vera nelle tacche aperte del tetto prima di stampare la base (guida 11.03);
   - cavo piatto del carapace in due strisce: pieghe da provare sul pezzo prima di saldare la basetta (`cablaggio.md` 3.5bis); la riserva è la soluzione B di P-002, da far scegliere all'utente.
3. **Da guardare sui pezzi in casa** (D-073): chiederli all'utente quando servono, non sono misure dei servo.
   - ESP32 RE1.3: nel CAD dalla 2.1.8 con le quote del disegno e le altezze dei datasheet (S); si confermano sulla dima (F5). Basta sapere l'altezza delle strip femmina che si useranno sulla basetta (standard 8,5).
   - Diametro e altezza dei condensatori da 2200 µF (B7). Previsti 12,5–13 × 20–22 mm.
   - Kit Temu da 918 viti M2–M5: tipo di testa e lunghezze delle M3. Se ci sono M3 × 6 e × 8 a testa cilindrica, D6 si riduce.
   - Lega dello stagno "a bassa temperatura": se non è al bismuto, B19 perde anche lo stagno.
   - Quanto resta della bobina FlashForge di PETG-CF nero: se è quasi intera, E1 scende a una bobina.
   - Portafusibile Neuftech di F1 (Q-23): forma delle estremità, per i reofori delle spie (2.1.8).
   - Quote dei moduli della 2.1.6 (D-074), prese dalle foto dei venditori; prima di stampare base, piastrina e carapace:
     - GY-6500: 26 × 15,5, fori Ø3 a 20,6 di interasse e 2,3 dal bordo (`sen_mpu_*`);
     - MS3625: Ø13,5 con i lati piatti a 12,6 (`aud_ms_*`);
     - MAX98357A generico: fori a 13 di interasse, 2,2 dal bordo della morsettiera (`aud_amp_fori*`);
     - altoparlante da 15: spessore (`aud_altt_sp`, oggi 4).
4. **Provini da stampare prima dei pezzi**:
   - culla e giunto: passacavo, fori pilota, forzamenti di cuscinetti e perni, gioco d'imbardata;
   - luce (X10, D-069);
   - tasche della lama A (D-072): il risultato va in `cov_testa_d` o si passa alle costole;
   - inserti del kit Temu con `Attrezzo_Provino_Inserti` (M3 Ø3,9…4,2, M2 Ø2,9…3,4, in PETG-CF). Poi `ins_m3_d`, `ins_m3_l`, `ins_m2_d`, `ins_m2_l` in `rif_componenti.py` e verifica completa, perché `ins_m3_d` muove anche le bugne delle culle.
   - piedino con le tre strette (0 / 0,2 / 0,4): il valore scelto va in `pied_stretta`.
   - Dopo i provini: nervature di schiacciamento delle culle.
5. **Guida di montaggio** (D-075): bozza avanzata allineata alla 2.1.7, aggiornata a ogni versione; la passata finale (immagini, verifica avversaria, release) a progetto stabile. Prossimi passi e decisione del 17 ottobre in `docs/piano-guida.md` (in fondo).
6. **PCB** (D-078): piano `docs/piano-pcb.md` approvato il 18 ottobre; F1 fatta (metodo da script, strumenti e CI in `pcb/`); schemi di basetta e carapace approvati all'arresto R1 (D-079); prossimo F4 della PCB-C; piano della 2.1.8 (F2) approvato, in corso (in fondo a `piano-v2.1.0.md`). Stato in fondo al piano.
7. **Fase 5**: viteria dal modello, da aggiornare a ogni modifica. **Fase 6**: ciclo a tripode verificato in quattro assetti e rotazione sul posto; resta l'andatura con il corpo inclinato o spostato, se servirà.
8. **Software**: prossimo S1, banco dell'elettronica (`docs/piano-elettronica-software.md`).

**Backlog**: `docs/backlog.md` (PCB al posto delle millefori, studio fatto il 16 ottobre 2026; pettini dei cavi dei servo; predisposizioni in attesa).
