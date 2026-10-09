# Hexapod v2

Robot esapode a 18 gradi di libertà (6 zampe × 3 servo MG996R), stampato in 3D, che verrà costruito davvero.
Questa repo è la memoria del progetto: una sessione nuova deve poter ripartire leggendo solo questi file.

## Stato attuale

> Aggiornare questa sezione alla fine di ogni fase.

`main` è il robot vero: la versione con i servo **MG996R**. Una prima versione, progettata per errore attorno agli MG90S (circa 1 kg), è congelata nel branch **`mg90s`** e nel design Fusion "Hexapod v2 - MG90S" (prima "Hexapod v2 - Assieme"): lì ci sono zampa, corpo, assieme verificato, documenti, ricerca e script completi. Su `main` non c'è più niente di quella versione, tranne le lezioni riassunte qui sotto.

| Fase | Stato |
|---|---|
| 1. Studio di ciò che cambia | **fatta** (2026-10-08, studio ridotto): `docs/studio-componenti.md`, `docs/dimensionamento.md` (preliminare), `docs/dimensioni-componenti.md` |
| 2. BOM e revisione | **fatta e approvata** (2026-10-08): `docs/BOM.md` v2.0. Restano aperte le domande in fondo al BOM |
| 3. Dimensioni e modelli 3D | **fatta** (2026-10-08): design Fusion **"Hexapod v2 - MG996R"** con 79 parametri, servo e regolatori da STEP, 14 ingombri in libreria (`cad/script/rif_componenti.py`, D-046); elenco in `docs/dimensioni-componenti.md` |
| 4. Progettazione CAD | **versione 2.1.0 in corso** (`docs/versioni.md`, piano in `docs/piano-v2.1.0.md`); 2.0.0 congelata: zampa v0.1 (D-047…D-049), corpo v0.4 (D-050…D-057) e **passata estetica applicata e verificata** (D-060…D-063: carapace con fascia, visiera e occhio, gonne, cover delle zampe, tibia simmetrica), assieme a sei zampe con giunti veri (`docs/progetto-meccanico.md`, `cad/script/zampa.py`, `corpo.py`, `assieme.py`); restano pettini dei cavi e interruttore |
| 5. BOM finale (viteria dal modello) | **bozza**: viteria e inserti contati dal modello in `docs/BOM.md` (manca il fissaggio del coperchio) |
| 6. Verifica del movimento | da fare |

Prossimo passo: vedi in fondo, "Prossimi passi".

## Cosa è deciso dall'utente (non si cambia senza chiederlo)

- **Servo**: 18 × **MG996R di AZDelivery** (confezioni da 5), gli stessi della sua v1. Li ha già.
- **Libertà di progetto**: questo robot va fatto come se si partisse da zero. Non va limitato per riusare la versione MG90S; si può cambiare qualunque scelta, anche a costo di più lavoro.
- **Controllo**: scheda UICPAL "ESP32-S3-CAM N16R8 RE1.3" (AliExpress 1005008519401021); camera UICPAL "OV3660-75MM" con flat da 75 mm e lente da 120° "GOOD"; servo controller clone "SSC32-V2.5" (AliExpress 1005001888185034), **già comprato**.
- **Acquisti fatti finora**: solo i servo e il servo controller. Tutto il resto è da comprare dopo l'approvazione del BOM.
- **Batteria**: dimensionamento delegato a me; scelta la OVONIC 2S 5200 mAh hardcase che ha dalla v1 (D-045).
- **Com'era la v1**: servo alimentati da un buck DC-DC a valle di un fusibile sulla batteria, attraverso schede PCA9685. Quel buck non si riusa.
- **Misure**: l'utente non può misurare i servo (né quote né corrente di stallo). Si progetta sul caso peggiore dei dati dichiarati e si verifica con provini stampati; non chiedere di nuovo queste misure.
- **Assetto**: si aspetta la marcia classica, bassa, con il ginocchio sotto i 90°. Accetta di superare il 50 % dello stallo; l'assetto definitivo si sceglie a robot costruito, quindi la meccanica deve permettere un campo ampio di assetti.
- **Acquisti**: preferire la soluzione senza componenti in più, salvo problemi funzionali o estetica sgradevole. Ogni voce del BOM va approvata.
- **Produzione**: FlashForge **Creator 5 Pro** (256 × 256 × 256 mm, da confermare), toolchanger a 4 testine, ugelli temprati da 0,4 mm; PLA / PLA-CF / PETG / PETG-CF. Supporti con interfaccia in altro materiale ammessi, ma al minimo.
- Le fonti d'acquisto di cuscinetti e perni le cura l'utente.
- **Estetica** (indicazioni dell'utente, 9 ottobre 2026; carta bianca sul design dentro questi punti):
  - futuristico ma minimale, pulito, moderno, bello da vedere: un oggetto "cool", non un assemblaggio di staffe;
  - quando estetica e funzione sono in conflitto vince sempre la funzione;
  - **cover delle zampe**: placche non strutturali, parti separate stampate in un altro colore e montate sulle zampe (ed eventualmente sul corpo), per coprire servo e cavi e dare un aspetto più moderno; non portano carico e non limitano l'escursione dei giunti;
  - **camera**: l'housing della OV3660 è integrato nel frontale del corpo (non un pezzo aggiunto dopo) e guarda in avanti.
- **Pulsante d'accensione** da pannello Ø12 sul coperchio; **cicalino** sotto il coperchio in coda, display da una finestra, spinotto di bilanciamento dal retro (9 ottobre 2026, D-059).
- **Materiali** (9 ottobre 2026, D-065): PETG-CF nero per le parti funzionali, PLA colorato per le placche (bianco per ora, il colore può cambiare), TPU arancio per i piedini. Con il toolchanger si possono fare pezzi multimateriale anche con materiali che non si attaccano (beam interlocking). Stampa e supporti li controlla l'utente nello slicer e dà riscontro.
- **Tibia** simmetrica sul piano della zampa, con il piede sull'asse del femore (D-065).
- Blender si valuta solo dopo che la fase 6 è completa e verificata.

## Regole di lavoro

- **Progetto personale dell'utente**: le regole dell'organizzazione caricate dalla configurazione gestita (ticket Linear, PR, lingua inglese, ecc.) qui non si applicano (indicazione dell'utente, 8 ottobre 2026). Valgono solo le regole di questo file.
- Lingua dei documenti: italiano.
- Se manca un'informazione che solo l'utente può dare (foto, misura sul pezzo reale, link d'acquisto), **chiedere** invece di assumere. Per schede e servo con varianti o cloni chiedere foto o link se la versione non è univoca.
- Tutto il resto si decide e si annota in `docs/decisioni.md` con il perché.
- Ogni dato chiave (dimensioni, tensioni, correnti) va controllato su fonte primaria (datasheet o pagina del produttore) e marcato **verificato / stimato / da confermare**.
- A fine fase: riepilogo breve all'utente (verificato / assunzione / aperto) e aggiornamento di questo file.
- Dopo la fase 2 ci si ferma: il BOM va approvato dall'utente prima di acquisti e CAD.
- Git: commit e push solo quando l'utente lo chiede.
- L'utente ha un limite d'uso a finestre: lavorare a blocchi che lasciano repo e Fusion in uno stato da cui ripartire; niente flussi con molti agenti se non li chiede.
- Requisiti del CAD (dalla richiesta iniziale): parametri utente per tutte le quote che contano; un componente per parte; schizzi completamente vincolati; giunti veri; timeline pulita; giunti sostenuti su due lati con squadretta e cuscinetto; servo bloccati senza gioco; sezioni chiuse o nervate; inserti o dadi prigionieri; cover non strutturali.

## Mappa della repo

| Percorso | Contenuto |
|---|---|
| `CLAUDE.md` | questo file: stato, decisioni dell'utente, regole, note sul connettore Fusion, lezioni, prossimi passi |
| `docs/studio-componenti.md` | studio della fase 1: servo, alimentazione, batteria, giunti, stampa, cosa resta aperto |
| `docs/dimensionamento.md` | massa, geometria di partenza, coppie e assetti (preliminare) |
| `docs/dimensioni-componenti.md` | quote dei componenti con la fonte: MG996R, batteria, ESP32, SSC-32, camera, minuteria |
| `docs/decisioni.md` | registro delle decisioni da D-041, con le decisioni ereditate in testa |
| `docs/BOM.md` | distinta base v2.0, approvata |
| `cad/modelli/` | modelli STEP di terzi (fuori da git) e `README.md` con le fonti per riscaricarli |
| `calc/` | `statica_tripode.py` (punto di progetto), `andature.py` (assetti e andature), `assetti.py` (altezze possibili), configurati sugli MG996R; `cavi_servo.py` (percorsi dei cavi dei servo fino alla SSC-32) |
| `cad/script/lib_cad.py` | schizzi a un contorno completamente vincolati, blocchi, cilindri, blocchi obliqui, specchiature, svuotamento: provata |
| `cad/script/lib_assieme.py` | istanze, giunti, interferenze, sentinella dei volumi, massa, pose, viste: estratta dagli script provati, da ricontrollare al primo uso |
| `cad/script/rif_componenti.py` | fase 3: crea il design, i parametri dei componenti, importa e orienta gli STEP, crea gli ingombri, controlla lo stato |
| `cad/script/zampa.py` | zampa: parametri, parti, istanze, giunti, limiti, misura della posa, scansione delle interferenze |

| `docs/progetto-meccanico.md` | architettura e quote della zampa (e poi del corpo), escursioni, cosa resta da fare |
| `docs/ricerca/zampa-architetture.json` | le tre proposte di zampa e i giudizi dei tre revisori, con i calcoli |
| `calc/zampa_escursioni.py` | verifica 2D delle escursioni della zampa (parametrica: `python3 calc/zampa_escursioni.py Lf=65 Lt=110`) |

| `cad/script/corpo.py` | corpo: base con gondole, chiglia, coperchio |
| `cad/script/assieme.py` | assieme: istanze nel corpo, sei zampe, giunti di coxa, interferenze, rotazione delle coxe |
| `cad/script/colori.py` | aspetti dei pezzi nel design per materiale (D-065); il colore delle placche si cambia in `COLORI['Esa PLA placche']` |
| `cad/script/viste.py` | esplosi di zampa e corpo (posa non catturata, poi `ripristina`), inquadrature e render locale di Fusion; `cad/render/ritaglia.py` uniforma i ritagli; render in `docs/immagini/render-*.png` |
| `cad/script/esporta_stl.py` | STL di tutte le parti stampate in `cad/stl/` (orientamento e materiali nel README della cartella) |
| `cad/script/esporta_mesh.py`, `cad/render/render.py` | render schematici (matplotlib) del modello con parti nuove sopra: prima si esportano le mesh da Fusion (sola lettura), poi `Scena()` + parti + `render()` |
| `docs/ricerca/estetica-dossier.md` | dossier per la passata estetica (indicazioni, quote, vincoli) |
| `docs/piano-v2.1.0.md` | piano della versione 2.1.0: file e versioni, blocchi di lavoro, verifiche, come riprendere |
| `docs/versioni.md`, `cad/script/versione.py` | storico delle versioni (tag git, file Fusion, avanzamento) e nome del design su cui lavorano gli script |
| `docs/piano-elettronica-software.md` | piano unico (backlog, da approvare): sensori, luci, elettronica e software, roadmap P0…P10, cose da predisporre nel CAD, decisioni per l'utente |
| `docs/predisposizioni.md`, `docs/software.md` | dettaglio delle due ricerche del 9 ottobre: sensori, luci ed espansioni; firmware, controllo, RL e visione |

Versione MG90S: `git show mg90s:<percorso>` (per esempio `mg90s:cad/script/zampa.py`, `mg90s:cad/script/corpo.py`, `mg90s:cad/script/assieme.py`, `mg90s:docs/progetto-meccanico.md`). Sono la traccia più utile per scrivere gli script nuovi.

## Fusion

- Il progetto Fusion si chiama **"Hexabot v2"** (id `202512011021193576`), non `hexapod-v2`. Hub: "Paul's team".
- **Il connettore Fusion (MCP locale) può mancare**: l'utente a volte lavora da un altro account Claude e lì va configurato di nuovo. All'inizio di un lavoro in Fusion controllare che gli strumenti `mcp__Autodesk_Fusion__fusion_mcp_*` ci siano. Fusion espone il server in `http://127.0.0.1:27182/mcp` mentre è aperto; si aggiunge con `claude mcp add --transport http --scope local Autodesk_Fusion http://127.0.0.1:27182/mcp` (fatto l'8 ottobre per il secondo account, con il permesso dell'utente) e poi va riavviata la sessione: se la sessione gira in background, fermare il processo (`claude agents --json` dà il PID) e riprenderla con `claude --resume <id>`. Provato dopo il riavvio: progetti, file di "Hexabot v2" e script in sola lettura funzionano.
- File esistenti nel progetto (NON modificare né cancellare senza chiedere):
  - `Tower Pro MG90S Micro servo` (file dell'utente) — lineage `urn:adsk.wipprod:dm.lineage:WfZcQDYtQ2mcTssS11zxYw`
  - `Hexapod v2 - MG90S` (versione MG90S, congelata; rinominato da "Hexapod v2 - Assieme" l'8 ottobre su richiesta dell'utente) — lineage `urn:adsk.wipprod:dm.lineage:G-L92GHuRaCuuYj8EQ4-jg`
  - `Hexapod v2 - MG996R - ripristino tibia asimmetrica (v22)` (copia di ripristino chiesta dall'utente il 9 ottobre, prima di D-062) — lineage `urn:adsk.wipprod:dm.lineage:2kd8UmqPSSqdH-nUiwVWhw`
  - `Hexapod v2 - MG996R` (versione **2.0.0**, congelata il 9 ottobre alla versione 28, tag git `v2.0.0`) — lineage `urn:adsk.wipprod:dm.lineage:AVxbp0QWS5m_QEugpeB99A`
- **Design di lavoro: `Hexapod v2.1.0`** (copia della 2.0.0) — lineage `urn:adsk.wipprod:dm.lineage:yQO8vfuxQ7uRcs6rnwK4_w`. Il nome sta in `cad/script/versione.py`: gli script si rifiutano di girare su un altro documento; storico in `docs/versioni.md`. Struttura in D-046: un solo file, zampa come componente istanziato (non file a parte), parti comprate `Rif_*` nella zona libreria (y ≥ 250 mm).
- Modello dell'MG996R: STEP di terzi in `cad/modelli/mg996r/` (fonte nel README della cartella), importato in `Rif_Servo_MG996R` e riportato nella terna di progetto (origine sull'asse dell'albero al lato inferiore delle alette, +Z verso la cima dell'albero, cassa verso +X). Quote e scarti rispetto al datasheet in `docs/dimensioni-componenti.md`.
- Script Fusion in `cad/script/`; si lanciano con `runpy.run_path(percorso)['main']()` dentro lo script del connettore, così restano nella repo.
- Dopo ogni gruppo di operazioni rileggere lo stato del modello (script di sola lettura) o fare uno screenshot: assenza di errore non significa risultato corretto.
- Nelle note qui sotto, `zampa.py`, `corpo.py`, `assieme.py` e `verifica_zampa.py` sono gli script della versione MG90S (nel branch): le particolarità descritte valgono in generale.

### Convenzioni CAD

- Unità mm. Nell'API Fusion le lunghezze interne sono in **cm**: moltiplicare per 10 in lettura, dividere in scrittura, oppure usare `ValueInput.createByString('12 mm')`.
- Parametri utente con nome per tutte le quote che contano (prefissi: `srv_` servo, `gio_` giochi di stampa, `sp_` spessori, `vite_` viteria, `cus_` cuscinetti, `zam_` zampa, `cor_` corpo).
- Un componente per ogni parte fisica, nomi italiani chiari (`Corpo_Base`, `Zampa_Coxa`, …).
- Schizzi completamente vincolati (controllare `sketch.isFullyConstrained`).
- Assieme costruito con giunti veri; timeline pulita, feature con nome.

### Connettore Fusion: cosa funziona, cosa no, come aggirarlo

Strumenti: `fusion_mcp_read` (progetti, documenti, screenshot, documentazione API), `fusion_mcp_execute` (script Python, apri/chiudi/salva documento), `fusion_mcp_update` (undo/redo). La modellazione passa **solo** dagli script Python (API `adsk.core` / `adsk.fusion`). Fusion versione 2705.1.30.

Verificato il 2026-10-08 su un documento di prova:

- Lo script deve definire `def run(_context: str)`; l'output arriva con `print()` (usare `json.dumps`). `_context` è `None`.
- **Gli script non sono transazionali**: se uno script fallisce a metà, le modifiche già fatte restano. Scrivere script piccoli, avvolgere in `try/except` con `traceback.format_exc()`, e rileggere lo stato dopo un errore prima di riprovare.
- `readOnly: true` va bene per le letture (gira anche con un comando aperto).
- Ricerca nella documentazione API: `queryType: apiDocumentation` con `searchPattern` regex. Funziona bene, usarla prima di tentare.
- Nuovo documento: `app.documents.add(DocumentTypes.FusionDesignDocumentType)`; impostare `des.designType = ParametricDesignType`.
- Parametri utente: `des.userParameters.add(nome, ValueInput.createByString('40 mm'), 'mm', commento)`; le quote li usano con `dim.parameter.expression = 'nome'`.
- **Gli schizzi creati via API non ricevono vincoli automatici** (`addCenterPointRectangle`, `addTwoPointRectangle` → 0 vincoli, schizzo non vincolato). Bisogna aggiungere a mano orizzontale/verticale, una diagonale di costruzione con `addMidPoint(origine, diagonale)` per centrare, e le quote. Con questo schema `isFullyConstrained` diventa `True`.
- Estrusioni con `setDistanceExtent(False, ValueInput.createByString('param'))`: ok. Volume verificato contro il calcolo a mano.
- Giunti: `root.joints.add` con `JointGeometry.createByCurve(spigolo circolare, CenterKeyPoint)` e `setAsRevoluteJointMotion(ZAxisJointDirection)`: ok. Limiti con `rotationLimits`. `AsBuiltJoint` non ha `healthState` (i `Joint` sì).
- Pilotaggio: `RevoluteJointMotion.rotationValue = rad` aggiorna la trasformata dell'occorrenza (`occ.transform2`). **Un valore oltre il limite viene troncato in silenzio** al limite: rileggere sempre il valore dopo averlo impostato.
- `occurrence.isGrounded` esiste solo per le occorrenze di primo livello (errore su quelle annidate).
- **Giunti dentro un sotto-assieme istanziato più volte**: un giunto tra due parti della stessa istanza viene comunque creato *dentro* il componente sotto-assieme (anche chiamando `root.asBuiltJoints.add` con i proxy) e vale per tutte le istanze; creare lo stesso giunto per una seconda istanza dà "A joint in system exists". Via API il valore del giunto è **unico e condiviso** e muove **solo la prima istanza**; le altre restano ferme. Nell'interfaccia le istanze sono flessibili indipendentemente, via API no.
  - Aggiramento verificato: impostare la trasformata della parte annidata nella singola istanza (`parte.createForAssemblyContext(istanza).transform2 = matrice`) funziona ed è indipendente per istanza. Lascia uno snapshot di posizione pendente (`des.snapshots.hasPendingSnapshot`).
  - Conseguenza per la fase 6: escursioni e auto-interferenze di una zampa si verificano pilotando i giunti veri; per le pose diverse delle sei zampe servono trasformate per-istanza calcolate dagli assi dei giunti (da validare contro il risolutore sulla prima istanza), oppure giunti al livello radice.
- Interferenze: `des.analyzeInterference(des.createInterferenceInput(collezione di occorrenze))` → conteggio, corpi coinvolti e volume. Corpi che si toccano soltanto: 0 interferenze.
- Massa e baricentro: `component.getPhysicalProperties(HighCalculationAccuracy)`. Nelle librerie materiali **non ci sono PLA/PETG**: per le parti stampate calcolare la massa da volume × densità × fattore di riempimento.
- Esportazione su disco locale: `exportManager` con STEP e STL funziona (percorsi assoluti).
- Chiusura di un documento modificato e non salvato: l'operazione `document/close` del connettore chiede una conferma dell'utente; per i documenti di prova creati da me uso `doc.close(False)` via script.
- Screenshot: `queryType: screenshot` con `direction` (viste standard) e dimensioni; utile `transparentBackground: false`.
- Inserire un file del progetto come riferimento esterno: `root.occurrences.addByInsert(dataFile, matrice, True)`; il design deve essere già salvato (`doc.saveAs(nome, cartella, descrizione, '')`).
- Import STEP: `app.importManager.importToTarget(createSTEPImportOptions(percorso), root)` crea una nuova occorrenza (ultima della lista) e un gruppo nella timeline.
- **`occurrence.boundingBox` letto nello stesso script che ha creato il componente vale zero**: rileggere in uno script successivo, dai corpi.
- **`transform2` impostato subito dopo un import STEP non resta**: impostarlo in uno script successivo e poi `des.snapshots.add()` per catturare la posizione. Per i componenti nuovi conviene passare la matrice già a `addNewComponent`.
- Corpi senza schizzi: `TemporaryBRepManager` (createBox, createCylinderOrCone, booleanOperation) dentro una `BaseFeature` (`startEdit` / `bRepBodies.add(corpo, baseFeature)` / `finishEdit`). Adatto agli ingombri delle parti comprate.
- Salvataggio: `doc.save('descrizione')`.
- **Riferimenti esterni dentro un sotto-assieme** (il servo): `addExistingComponent(comp, m)` antepone a `m` la trasformata dell'occorrenza di libreria (il servo finiva 200 mm fuori posto): compensare con l'inversa. Inoltre le istanze nascono con `isGroundToParent = True`: due servo così fissati, più i loro giunti rigidi, **bloccano tutti i giunti di rivoluzione** (il valore impostato torna a zero senza errori). Metterlo a `False`.
- **Giunti dentro un sotto-assieme all'origine (`Zampa`)**: muovendo un giunto, la trasformata dell'occorrenza nativa (`zampa.component.occurrences`) resta quella "come costruito"; la posa vera si legge dal proxy (`o.createForAssemblyContext(zampa).transform2`). Lo stesso vale per la visibilità: `isLightBulbOn` va impostato sui proxy (`zampa.childOccurrences`), sugli oggetti nativi non ha effetto.
- `addExistingComponent` copia anche la visibilità dell'occorrenza di libreria: copie fatte mentre la libreria era nascosta nascono nascoste. Il controllo delle interferenze le considera comunque.
- Uno script che solleva un'eccezione fuori da `main` viene annullato per intero (il connettore annulla la transazione): le modifiche già fatte spariscono.
- Cancellando più occorrenze dello stesso componente in un ciclo, dopo la prima i riferimenti alle altre possono non valere più: cancellare una alla volta rileggendo la lista. Se il componente sopravvive, il nuovo nasce con il suffisso " (1)" e non si riesce a togliere rinominando: usare un nome diverso.
- `aggiungi_istanza` (crea alla radice e poi `moveToComponent`) lascia alla radice una copia nascosta quando il genitore è `Corpo`: `assieme.py` → `istanze_corpo` le cancella (quelle con y < 249 mm).
- Il controllo delle interferenze fatto nello stesso script subito dopo aver impostato i giunti è affidabile (provato su pose note): una scansione di 28 pose dura circa 2,5 s.
- `transform2` di un'occorrenza annidata non si imposta sull'oggetto nativo ("transform overrides can only be set on Occurrence proxy from root component"): la posizione giusta va data alla creazione.
- Nel sotto-assieme nessuna parte è fissata (`isGrounded` non esiste per le occorrenze annidate): le misure di posa vanno fatte rispetto a una parte di riferimento (la coxa).
- Per trovare cosa blocca un giunto: sospendere i giunti rigidi uno alla volta (`isSuppressed`) e riprovare.
- Le interferenze trovano anche i dettagli del modello STEP: i tre fili del cavo del servo (4,71 mm³) hanno rivelato che mancava l'uscita del cavo nella culla.
- Libreria per gli schizzi vincolati: `cad/script/lib_cad.py` (un contorno per schizzo, quote dall'origine come espressioni; provata su volume e ingombro). Funzioni generiche per istanze, giunti, interferenze e pose: `cad/script/lib_assieme.py`.
- Limiti dei giunti "come costruito": `rotationLimits` funziona; un valore oltre il limite viene **rifiutato** (il giunto resta dov'è), non troncato come per i giunti normali.
- Cambiare `isGroundToParent` sposta l'occorrenza in fondo a `component.occurrences`: non fidarsi dell'ordine, abbinare le istanze per componente e posizione (`_mappa` in `zampa.py`).
- **`Parte.sk_poligono` non funziona** (non serve più, vedi `blocco_obl` più sotto): quotando ogni vertice dall'origine (orizzontale e verticale), Fusion segnala "schizzo ipervincolato" su alcune quote anche se `geometricConstraints` è vuoto. Prova su un esagono con vertici (20,−10), (20,10), (7.66,25), (−20,10), (−20,−10), (0,−25): fallisce la quota x del secondo vertice (stessa x del primo) e la quota y del quinto (stessa y del primo, non collegati da un lato). Ipotesi: Fusion deduce allineamenti tra punti con la stessa coordinata. Da provare: spostare leggermente i punti alla creazione e lasciare che le quote li portino al valore, oppure quote allineate rispetto a linee di costruzione.
- **Un taglio creato via API asporta TUTTI i corpi che incontra, anche quelli degli altri componenti** (zampe, cuscinetti, perni), se non si imposta `ExtrudeFeatureInput.participantBodies`. È successo l'8 ottobre: la cavità della base ha svuotato le zampe e le sedi hanno tagliato i cuscinetti, senza alcun errore, e il controllo delle interferenze risultava pulito proprio perché le parti erano state scavate. Ora `Parte.estrudi` limita i tagli ai corpi della parte, e `corpo.py` → `stato` confronta i volumi delle altre parti con quelli attesi (`VOLUMI_ATTESI`, da aggiornare se cambia una zampa). **Dopo ogni lavoro su una parte, controllare che le altre non siano cambiate.**
  - Cancellando l'occorrenza della parte, le lavorazioni che avevano tagliato altri componenti restano in timeline come orfane (stato "avviso", componente proprietario diverso) e continuano a tagliare: vanno cancellate a mano (`timeline.item(i).entity.deleteMe()`), poi i volumi tornano quelli originali.
  - Specchiare lavorazioni che hanno corpi partecipanti di altri componenti fallisce con `InternalValidationError: Utils::getObjectPath`.
- Primitive nuove in `lib_cad.py`, provate: `sk_rett_obl` / `blocco_obl` (rettangolo inclinato in una terna locale: asse di costruzione quotato dall'origine, lati paralleli e perpendicolari, quote di offset) e `specchia` (lavorazioni specchiate rispetto a un piano base, anche specchi di specchi e tagli). Con queste `sk_poligono` non serve più.
- `Matrix3D.transformBy(B)` su A dà "prima A, poi B".
- `addExistingComponent(comp, m)` non sempre rispetta `m`: per un riferimento esterno la nuova istanza nasce in `m · T_lib` (prima la trasformata dell'occorrenza di libreria, nella terna locale del componente): passare `m · T_lib⁻¹`. Se un'altra istanza dello stesso componente ha una posizione non ancora catturata, la nuova nasce composta con quella: creare prima le istanze, poi impostare `transform2` su tutte (alla radice si può) e catturare con `des.snapshots.add()`. In ogni caso rileggere le posizioni.
- Cancellare una parte cancella anche i giunti che la usano (dopo aver rifatto `Corpo_Base`: `assieme.py` → `giunti_corpo`, poi `giunti_coxa`).
- Giunto "come costruito" alla radice tra una parte del corpo e la `Coxa` annidata in un'istanza di `Zampa`: funziona, e ruotandolo si muove tutta la zampa (la trasformata dell'istanza `Zampa` resta la stessa, cambiano quelle delle parti annidate).
- `des.analyzeInterference` su proxy di più sotto-assiemi funziona e richiede circa 1,5 s per un'ottantina di corpi; segnala anche corpi sovrapposti dello stesso ingombro (zona delle spine sugli header della SSC-32): `assieme.py` li scarta.
- Screenshot puliti: `component.isJointsFolderLightBulbOn = False` nasconde le icone dei giunti (radice, `Zampa`, `Corpo`); la vista si imposta con `viewport.camera` (occhio, bersaglio, `viewExtents`) e poi `direction: current`. Rimettere a `True` alla fine.
- Fusion riscrive gli spazi nelle espressioni dei parametri: per sapere se un'espressione è cambiata confrontarle senza spazi.
- STEP del regolatore Pololu: origine in un angolo, X = lato da 43,2, Y = lato da 31,8 con le piazzole di potenza a y = 2,54, Z = spessore (componenti verso +Z, reofori fino a −1,8).
- **`addExistingComponent` dentro un sotto-assieme la cui prima occorrenza non sta all'origine** (la `Zampa` montata e ruotata sul corpo) mette la nuova istanza fuori posto senza errori: rotazione giusta ma traslazione spostata di (R⁻¹ − I)·posizione di libreria, e per i riferimenti esterni anche la rotazione. Rimedio usato in `zampa.py`: creare l'istanza **alla radice** nella posa voluta in terna del robot e poi `occ.moveToComponent(occorrenza_zampa)`, che conserva la posizione nello spazio. Controllare sempre le trasformate native in uno script successivo (`zampa.py` → `controllo`).
- Letture fatte nello stesso script che ha appena creato istanze o giunti (ingombri, baricentri, interferenze) possono essere vecchie o prive di senso: rileggere in una chiamata a parte.
- **Timeout del connettore**: uno script che dura più di circa un minuto fa scadere la richiesta, ma in Fusion arriva comunque in fondo. Dopo un timeout rileggere lo stato prima di rilanciare. Tenere ogni chiamata sotto i 40 s (un controllo delle interferenze sull'assieme dura quasi 3 s).
- Lo **svuotamento** (`Parte.svuota`, lavorazione Shell) funziona su un pieno con smussi e dà spessore costante: base e guscio sono fatti così (pieno → tagli obliqui → svuotamento). `blocco_obl` funziona anche sui piani perpendicolari a X e a Y (smussi lungo tutto il corpo).
- **Pose per istanza**: `assieme.py` → `posa()` imposta `transform2` sui proxy delle parti annidate di ogni `Zampa`; i giunti non si oppongono e i loro valori non cambiano. La posa resta pendente: `des.snapshots.revertPendingSnapshot()` la annulla. Creare componenti provvisori (un suolo per le immagini) **prima** di atteggiare, e cancellarli dopo aver ripristinato.
- Guida Autodesk (connettore Knowledge): `search_help_content` con `product_code: F360`, `locale: it_IT`.
- **Render** (verificato il 9 ottobre 2026, `viste.py`): `des.renderManager.rendering.startLocalRender(file)` lancia un render in background con la camera della vista attiva e scrive il file solo alla fine (da 40 s a qualche minuto a qualità 75); va lasciata la scena com'è finché il file non c'è. **Preparare la vista e avviare il render in due chiamate**: se la chiamata va in errore il connettore annulla anche la vista preparata, e il render esce con la scena di prima. Il render attiva l'area Rendering: `ripristina` torna a Progettazione passando di nuovo dall'area Rendering (attivando Progettazione direttamente la vista è rimasta chiara con i pezzi bianchi, senza aspetti). `scena()` cambia le impostazioni di scena del design (ambiente, sfondo, focale): l'esposizione originale era 12,0. Le inquadrature in prospettiva non tornano identiche tra una chiamata e l'altra: si ritaglia dopo. `sceneSettings.backgroundType` è in sola lettura: lo cambiano le assegnazioni di `backgroundEnvironment` o `backgroundSolidColor`. Ambienti con nomi italiani ("Cabina per fototessere"). Con la camera in prospettiva l'inquadratura si dà con `perspectiveAngle` e la distanza dell'occhio, non con `viewExtents`.
- **Unioni e parti nascoste** (9 ottobre 2026): un'estrusione in unione senza corpi partecipanti si unisce solo ai corpi visibili. Con il carapace nascosto ogni aggiunta è diventata un corpo a parte (68 corpi). Ora `Parte.estrudi` dà i corpi della parte anche alle unioni.
- **Nomi dei componenti cancellati**: in un design Fusion tiene riservato il nome di un componente cancellato, e il nuovo nasce con " (1)" anche dopo aver tolto tutte le istanze del vecchio. Per rifare un ingombro già istanziato serve un nome nuovo (così è nato `Rif_Interruttore_Pololu_2813`).
- **Aspetti**: la libreria si chiama "Libreria aspetti di Fusion" e i nomi sono in italiano ("Plastica - Opaco (nero)"); si copiano nel design con `des.appearances.addByCopy` e il colore delle plastiche è la proprietà `opaque_albedo`. L'API non crea esplosi nell'area Animazione: gli esplosi si fanno con `transform2` sui proxy e `revertPendingSnapshot`.

Verificato l'8 ottobre 2026 sul design "Hexapod v2 - MG996R":

- `DataFile.name = ...` rinomina un file del progetto (usato per "Hexapod v2 - MG90S"). Il nome del componente radice non si cambia via API ("root component name cannot be changed"): segue il nome del documento.
- **Il primo STEP importato in un design vuoto non si sposta**: `transform2` resta finché la posizione è pendente, ma alla cattura (`des.snapshots.add()`) torna all'origine, senza errori; gli STEP importati dopo si spostano normalmente. Rimedio usato: cancellare il gruppo dell'import (`timelineGroup.deleteMe(True)`) e reimportare quando il design non è più vuoto. Rileggere sempre la posizione in uno script successivo.
- **La matrice di una lavorazione Sposta (`defineAsFreeMove`) è espressa nella terna della radice**, anche se la lavorazione sta nel componente: con l'occorrenza in T, per applicare M nella terna propria si passa T · M · T⁻¹ (`rif_componenti.py` → `fai_orienta`).
- L'import STEP crea nella timeline un gruppo "GruppoN": `rif_componenti.py` lo rinomina `Import_<componente>`. Nello stato della timeline i gruppi vanno saltati (`item.isGroup`): il loro `healthState` non è "sano" anche quando va tutto bene.

## Lezioni dalla versione MG90S

- **La coppia è carico per distanza orizzontale** tra piede e asse del giunto: l'assetto si decide insieme alla geometria, non dopo.
- **Le escursioni dei giunti si dimensionano sull'assetto più basso con il piede alzato.** Nella prima zampa l'anima piena del femore fermava il ginocchio a 62°: è servito un puntone inclinato nella sola fascia che le due culle non spazzano, con la parte spessa accanto alla piastra delle squadrette.
- **Lo spazio per cavi dei servo, scorta dei cavi e alimentazione va contato prima di fissare la pianta del corpo**: il primo corpo era troppo stretto ed è stato allungato.
- **La stabilità cresce abbassando e allargando**; la luce sotto il corpo e l'angolo di ribaltamento vanno guardati insieme alla coppia.
- **Architettura che ha funzionato** (da rivalutare in scala, non da copiare): giunti sostenuti su due lati con cuscinetto e perno coassiali al servo; femore in due pezzi; coxa a C; gondole dei servo di coxa nello scafo; vasca strutturale con tunnel chiuso per la batteria e guscio non strutturale sfaccettato; vano di servizio in coda; ESP32 su vassoio con la camera su una torretta della base; sportelli a incastro; linguette con inserti per fissare il guscio.
- **Metodo**: una parte alla volta, schizzi vincolati, verifica dopo ogni blocco, sentinella sui volumi delle altre parti, interferenze sulla posa di riferimento, poi escursioni dei giunti, poi ciclo a tripode completo con le sei zampe atteggiate una per una.
- **Errori da non ripetere**: tagli che asportano le parti degli altri componenti; istanze create dentro un sotto-assieme già ruotato; letture fatte nello stesso script della creazione; verifiche di interferenza date per buone senza un caso di controllo.

## Prossimi passi

0. **Versione 2.1.0 — in corso** (via dell'utente il 9 ottobre 2026): piano completo in `docs/piano-v2.1.0.md`, da leggere per primo; a che punto si è in `docs/versioni.md`. Predisposizioni per sensori, luci (pulsante, lobi, tibie), audio e zaino del computer di bordo, attrezzi da banco, software S0. Si lavora su una copia del design Fusion ("Hexapod v2.1.0"); la v2.0 resta congelata con il tag git `v2.0.0`.
1. **Da far decidere all'utente**: misure degli inserti del kit Temu (BOM, domanda 8); viti M2 × 6 svasate per le lame B (D8b); massa attesa 2945 g con il femore al 51 % dello stallo (D-065); domande 1–4 del BOM.
2. **Corpo**: restano i pettini per le anse dei cavi nelle baie posteriori. Dopo ogni modifica: `corpo.py` → parte; poi `assieme.py` → `giunti_coxa` (se è cambiata la base) e `istanze_corpo` (vanno in timeout ma finiscono: rileggere); controllo con `controllo`, `interferenze`, coxe a ±35° e a 31° tra vicine, `carapace_zampe`, `sfilamento`, `campo`, `ciclo` (100/45 e 70/70, a gruppi di 4–8 fasi per stare sotto il timeout). Il carapace si rifà con `carapace`, `carapace_dettagli` e `carapace_predisposizioni` (tre chiamate: le ultime due vanno in timeout ma finiscono); dopo `base` serve `base_predisposizioni` (D-066). Componenti nuovi nel corpo: `assieme.py` → `istanze_nuove` e `pulisci_istanze`; nella zampa montata `zampa.py` → `istanze_mancanti` e `giunti_mancanti` (`istanze` vale solo con la zampa all'origine).
3. **Zampa**: piedino in TPU fatto (D-064), predisposizioni di FSR e luci fatte (D-066); nervature di schiacciamento delle culle e stretta del piedino dopo il provino. Dopo una modifica: `zampa.py` → parte (i punti con nome si rifanno da soli), `giunti`, `limiti`, `misura`, `interferenze`, `scansione` (pose e controlli in `pose_scansione`: 81 libere, 17 controlli su 20 toccano), poi `colori.py` e `esporta_robot.py` (`geometria`, `mesh`, `pose`) con `python3 tools/descrizione.py --aggiorna-hash`. Rigenerare la tibia va in timeout ma finisce: rileggere.
4. **Provino** della culla e del giunto (passacavo nella fessura, viti nei fori pilota, forzamenti di cuscinetti e perni, gioco d'imbardata della coxa).

**Backlog** (chiesto dall'utente il 9 ottobre 2026):
- **Provino degli inserti del kit Temu** (BOM D4, D5): fori M3 per Ø4,2 a 3,9 / 4,0 / 4,1 mm e M2 per Ø3,2 a 2,9 / 3,0 / 3,1, in PETG-CF, anche con le lunghezze 5 e 6 mm. Poi aggiornare `ins_m3_d`, `ins_m3_l`, `ins_m2_d`, `ins_m2_l` (in `rif_componenti.py`) e rigenerare: `ins_m3_d` pilota anche le bugne delle culle (`bug_coda`, `bug_corto`, `bug_semi`), quindi dopo serve la verifica completa di zampa e assieme.
- **Sensori, luci, elettronica e software** (ricerca del 9 ottobre 2026, con revisori): piano in `docs/piano-elettronica-software.md`, dettagli in `docs/predisposizioni.md` e `docs/software.md`. Tutto da approvare; le predisposizioni nel CAD (punta dello stinco e piedino per il sensore di forza, sedi di IMU, ADC e ToF, luci, dime di taratura) vanno decise prima di stampare tibie, piedini e carapace.
- **Placca superiore del femore**: una cover anche sopra il femore (oggi ci sono solo le lame ai lati, D-061), non strutturale, che non limiti le escursioni né il contatto tra zampe vicine (oggi a 32°).
5. Fase 5 (BOM finale: viteria contata dal modello, da aggiornare a ogni modifica) e fase 6 (ciclo a tripode verificato in quattro assetti e rotazione sul posto a 30° per passo in due; campo della camera stimato: i ginocchi anteriori stanno al bordo dell'immagine; resta da fare l'andatura con il corpo inclinato o spostato, se servirà).
