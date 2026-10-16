# CAD dell'esapode: note per lavorare in Fusion

Si carica quando si lavora in `cad/`. Il `CLAUDE.md` della radice rimanda qui: va letto prima di usare Fusion.

## Regole di base

- Script Fusion in `cad/script/`, lanciati con `runpy.run_path(percorso)` dentro lo script del connettore, così restano nella repo:
  - con passi, `['main'](passi, **kw)`: `corpo`, `zampa`, `assieme`, `attrezzi`, `esporta_robot`, `rif_componenti`;
  - senza argomenti, `['main']()`: `colori`, `esporta_stl`, `esporta_mesh`;
  - `viste.py` non ha `main`: si usano le sue funzioni (`prepara`, `avvia`, `ripristina`).
- Gli script controllano di girare sul design di lavoro (`cad/script/versione.py`).
- Dopo ogni gruppo di operazioni rileggere lo stato del modello (script di sola lettura) o fare uno screenshot: assenza di errore non significa risultato corretto.
- Modello dell'MG996R: STEP di terzi in `cad/modelli/mg996r/` (fonte nel README della cartella), importato in `Rif_Servo_MG996R` e riportato nella terna di progetto (origine sull'asse dell'albero al lato inferiore delle alette, +Z verso la cima dell'albero, cassa verso +X). Quote e scarti rispetto al datasheet in `docs/dimensioni-componenti.md`.
- Nelle note sul connettore, `zampa.py`, `corpo.py`, `assieme.py` e `verifica_zampa.py` sono a volte gli script della versione MG90S (nel branch): le particolarità descritte valgono in generale.

## Procedure dopo una modifica

- **Corpo**:
  - `corpo.py` → parte;
  - poi `assieme.py` → `giunti_coxa` (se è cambiata la base) e `istanze_corpo` (vanno in timeout ma finiscono: rileggere);
  - controllo:
    - `controllo`, `interferenze`;
    - coxe a ±35° e a 30,5° tra vicine (contatto a 31° su tre coppie su quattro, D-071);
    - `carapace_zampe`, `sfilamento`, `campo`;
    - `ciclo` (100/45 e 70/70, a gruppi di 4–8 fasi per stare sotto il timeout).
  - Il carapace si rifà con `carapace`, `carapace_dettagli` e `carapace_predisposizioni`: tre chiamate, le ultime due vanno in timeout ma finiscono.
  - Dopo `base` serve `base_predisposizioni` (D-066); il fondo dell'anello è un pezzo a sé, `fondo_anello` (D-067).
  - Componenti nuovi nel corpo: `assieme.py` → `istanze_nuove` e `pulisci_istanze`.
- **Zampa**:
  - `zampa.py` → parte (i punti con nome si rifanno da soli);
  - poi `giunti`, `limiti`, `misura`, `interferenze`, `scansione` (pose e controlli in `pose_scansione`: 81 libere, 17 controlli su 20 toccano);
  - componenti nuovi nella zampa montata: `istanze_mancanti` e `giunti_mancanti` (`istanze` vale solo con la zampa all'origine).
  - Rigenerare la tibia va in timeout ma finisce: rileggere. `fai_tibia` fa anche il fermo dei fili (D-067).
  - Lame del femore (D-070, D-071): `cover_femore_a`, `cover_femore_b`, `feritoia_a`, `feritoia_b`, poi `giunti_mancanti`. Le prime due vanno in timeout ma finiscono: rileggere.
  - Le pose per istanza le fa `assieme.py` → `posa_zampa` (usata da `pose_tripode` e `verifica_ciclo`), con `imponi_posa` di `lib_assieme.py`. Le parti che seguono il femore e la tibia stanno in `SEGUONO_FEMORE` e `SEGUONO_TIBIA`: un pezzo nuovo della zampa va aggiunto lì, altrimenti resta fermo e dà falsi urti.
  - `carapace_zampe` vuole `zampe=(...)` fra gli argomenti.
- **Coppie di zampe vicine**: `assieme.py` → `imposta_coxe(root, {'AS': +a, 'MS': -a})` e `interferenze`. Versi provati: a sinistra AS +, MS − e MS +, PS −; a destra AD −, MD + e MD −, PD +.
- **A valle di ogni modifica**:
  - `colori.py`;
  - `esporta_stl.py`;
  - `esporta_mesh.py` (mesh del renderer schematico);
  - `esporta_robot.py` (`geometria`, `mesh`, `pose`), poi `python3 tools/descrizione.py --aggiorna-hash` e tutti i generatori: `genera_header.py`, `genera_vettori.py`, `genera_modelli.py` (la CI `sim` li controlla).
  - Test locali con `.venv/bin/ruff check .`, `.venv/bin/python -m pytest tests sim/tests -q`, il nucleo con cmake e ctest su `firmware/test_host`, e `npm test` in `app/`.
  - Se cambia la massa: `calc/statica_tripode.py` → `CONFIG['massa_g']` e `robot.yaml` → `massa.attesa_g` (devono coincidere), con la regressione `robot.yaml` → `regressione_statica`.
  - Guida di montaggio (D-075): `esporta_guida.py` (`manifest`, `mesh`, `fori`, `zone`, `controllo`, in sola lettura), poi `.venv/bin/python -m guida.costruisci controlla`; formato dei passi in `guida/schema.md`.
- **Chiusura di una versione**:
  - aggiornare a mano `VERSIONE` in `cad/script/versione.py` e `versione` in `robot/robot.yaml`;
  - salvare in Fusion con `doc.save(descrizione)` e aspettare che il nome del documento passi alla versione nuova;
  - poi rifare `esporta_robot.py` → `geometria`, così il campo `documento` di `cad.json` riporta la versione nuova del file; l'hash e i generatori vanno rifatti dopo;
  - commit, tag, push e CI.
- **Render** (`viste.py`):
  - `prepara(vista)` e `avvia(file)` in due chiamate;
  - aspettare il file;
  - `ripristina`. Se la vista resta chiara con i pezzi bianchi (12 ottobre 2026: `ripristina` in una chiamata non e' bastato), attivare l'area Rendering (`renderManager.activateRenderWorkspace()`) e poi Progettazione (`FusionSolidEnvironment`) in **due chiamate separate**;
  - `cad/render/ritaglia.py` per i render di giorno.
  - Di notte (D-072): viste `notte_ant` e `notte_alto`, `avvia(file, notte=True)`, circa 9 minuti. `ripristina` toglie luci, pixel provvisori e traslucenza.

## Convenzioni CAD

- Unità mm. Nell'API Fusion le lunghezze interne sono in **cm**: moltiplicare per 10 in lettura, dividere in scrittura, oppure usare `ValueInput.createByString('12 mm')`.
- Parametri utente con nome per tutte le quote che contano (prefissi: `srv_` servo, `gio_` giochi di stampa, `sp_` spessori, `vite_` viteria, `cus_` cuscinetti, `zam_` zampa, `cor_` corpo).
- Un componente per ogni parte fisica, nomi italiani chiari (`Corpo_Base`, `Zampa_Coxa`, …).
- Schizzi completamente vincolati (controllare `sketch.isFullyConstrained`).
- Assieme costruito con giunti veri; timeline pulita, feature con nome.

## Connettore Fusion: cosa funziona, cosa no, come aggirarlo

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
- **Pose per istanza**: `assieme.py` → `posa_zampa` (con `imponi_posa` di `lib_assieme.py`) imposta `transform2` sui proxy delle parti annidate di ogni `Zampa`; i giunti non si oppongono e i loro valori non cambiano. La posa resta pendente: `des.snapshots.revertPendingSnapshot()` la annulla. Creare componenti provvisori (un suolo per le immagini) **prima** di atteggiare, e cancellarli dopo aver ripristinato.
- Guida Autodesk (connettore Knowledge): `search_help_content` con `product_code: F360`, `locale: it_IT`.
- **Render** (verificato il 9 ottobre 2026, `viste.py`): `des.renderManager.rendering.startLocalRender(file)` lancia un render in background con la camera della vista attiva e scrive il file solo alla fine (da 40 s a qualche minuto a qualità 75); va lasciata la scena com'è finché il file non c'è. **Preparare la vista e avviare il render in due chiamate**: se la chiamata va in errore il connettore annulla anche la vista preparata, e il render esce con la scena di prima. Il render attiva l'area Rendering: `ripristina` torna a Progettazione passando di nuovo dall'area Rendering (attivando Progettazione direttamente la vista è rimasta chiara con i pezzi bianchi, senza aspetti). `scena()` cambia le impostazioni di scena del design (ambiente, sfondo, focale): l'esposizione originale era 12,0. Le inquadrature in prospettiva non tornano identiche tra una chiamata e l'altra: si ritaglia dopo. `sceneSettings.backgroundType` è in sola lettura: lo cambiano le assegnazioni di `backgroundEnvironment` o `backgroundSolidColor`. Ambienti con nomi italiani ("Cabina per fototessere"). Con la camera in prospettiva l'inquadratura si dà con `perspectiveAngle` e la distanza dell'occhio, non con `viewExtents`.
- **`print` in ricorsione** (12 ottobre 2026): dopo alcune chiamate il connettore ha dato `RecursionError` nel suo `write` a ogni `print`, anche negli script piu' semplici. Si aggira scrivendo l'esito in un file JSON (in sola lettura) e leggendolo dalla shell.
- **Codifica dei file scritti da Fusion** (10 ottobre 2026): la codifica predefinita del Python di Fusion cambia da una sessione all'altra (una volta ascii): i file di testo si aprono con `encoding='utf-8'`. Un `open(..., 'w')` che fallisce a metà lascia il file vuoto.
- **Unioni e parti nascoste** (9 ottobre 2026): un'estrusione in unione senza corpi partecipanti si unisce solo ai corpi visibili. Con il carapace nascosto ogni aggiunta è diventata un corpo a parte (68 corpi). Ora `Parte.estrudi` dà i corpi della parte anche alle unioni.
- **Nomi dei componenti cancellati**: in un design Fusion tiene riservato il nome di un componente cancellato, e il nuovo nasce con " (1)" anche dopo aver tolto tutte le istanze del vecchio. Per rifare un ingombro già istanziato serve un nome nuovo (così è nato `Rif_Interruttore_Pololu_2813`).
- **Aspetti**: la libreria si chiama "Libreria aspetti di Fusion" e i nomi sono in italiano ("Plastica - Opaco (nero)"); si copiano nel design con `des.appearances.addByCopy` e il colore delle plastiche è la proprietà `opaque_albedo`. L'API non crea esplosi nell'area Animazione: gli esplosi si fanno con `transform2` sui proxy e `revertPendingSnapshot`.

Verificato l'8 ottobre 2026 sul design "Hexapod v2 - MG996R":

- `DataFile.name = ...` rinomina un file del progetto (usato per "Hexapod v2 - MG90S"). Il nome del componente radice non si cambia via API ("root component name cannot be changed"): segue il nome del documento.
- **Il primo STEP importato in un design vuoto non si sposta**: `transform2` resta finché la posizione è pendente, ma alla cattura (`des.snapshots.add()`) torna all'origine, senza errori; gli STEP importati dopo si spostano normalmente. Rimedio usato: cancellare il gruppo dell'import (`timelineGroup.deleteMe(True)`) e reimportare quando il design non è più vuoto. Rileggere sempre la posizione in uno script successivo.
- **La matrice di una lavorazione Sposta (`defineAsFreeMove`) è espressa nella terna della radice**, anche se la lavorazione sta nel componente: con l'occorrenza in T, per applicare M nella terna propria si passa T · M · T⁻¹ (`rif_componenti.py` → `fai_orienta`).
- L'import STEP crea nella timeline un gruppo "GruppoN": `rif_componenti.py` lo rinomina `Import_<componente>`. Nello stato della timeline i gruppi vanno saltati (`item.isGroup`): il loro `healthState` non è "sano" anche quando va tutto bene.

## Lezioni dell'11 ottobre 2026 (versioni 2.1.3–2.1.5)

- **Salvataggio asincrono**: dopo `doc.save` il nome del documento e `dataFile.versionNumber` si aggiornano dopo qualche secondo. Rileggerli prima di esportare `geometria`, che scrive il nome in `cad.json`.
- **Ruvidità del suolo**: `sceneSettings.groundRoughness` si imposta solo con `isGroundReflections` a vero, altrimenti è un errore. Un errore fuori da `main` annulla tutto lo script, compreso quello che era già andato a buon fine.
- **Camera**: `ripristina` e `prepara` nella stessa chiamata hanno lasciato la camera con un'inquadratura sbagliata. `prepara` va in una chiamata a sé, e l'inquadratura va controllata con uno screenshot prima di avviare un render lungo. Il campo di `VISTE` (in cm) non scala in modo lineare con la vista: si tara guardando.
- **Aspetti emissivi**: nella libreria ci sono "LED (blu)", "LED (rosso)", "LED (verde)" e "LED - SMD … (bianco)" (letti in Fusion l'11 ottobre; `viste.py` copia "LED (blu)"). Proprietà usate: `opaque_luminance`, `opaque_luminance_modifier` (colore della luce), `opaque_albedo`. La copia ha già `opaque_emission` a vero.
  - Il PLA diventa traslucido con `opaque_translucency`.
  - Un colore assegnato a una faccia (`BRepFace.appearance`) risulta `FaceAppearanceSource` e si toglie con `appearance = None`.
  - Una faccia emissiva emette verso l'esterno del corpo: per far passare la luce attraverso il PLA serve un corpo emissivo che guarda verso il pezzo.
- **Modificare senza rifare il pezzo**: per spostare un elemento si cambia l'espressione della quota nello schizzo (`sketchDimensions` → `parameter.expression`). Lo si è fatto per l'inserto della lama B in `Femore_B`: rifare il pezzo avrebbe cancellato i giunti.
- **Smusso a due distanze** (`addTwoDistancesChamferEdgeSet`): Fusion sceglie lui quale distanza va su quale faccia. Si controlla la faccia che resta e, se è sbagliato, si rifà con `isFlipped`. Così fa `_cover_femore`.
- **Parametri utente non più usati**: si cancellano con `deleteMe()` dopo aver controllato `dependentParameters`.

## Lezioni del 16 ottobre 2026 (versione 2.1.7, blocco corpo)

- **`DataFile.copy(cartella)` nella stessa cartella dà alla copia lo stesso nome** dell'originale ("Hexapod v2.1.0"): rinominarla subito (`DataFile.name`, in una chiamata a parte, cercandola per `id`), altrimenti due file hanno il nome che controlla `versione.py`.
- **Cambiare un ingombro già istanziato**: `rif_componenti.py` → `ingombri` con `solo=[...]` e `sostituisci=True` aggiorna i corpi nella BaseFeature (`updateBody`, `bRepBodies.add`, `deleteMe` in modo modifica): le istanze nel corpo restano e il nome non prende " (1)".
- **Istanza spostata da un parametro**: `istanze_nuove` con la vecchia istanza ancora presente ha creato la nuova fuori posto (88,5; −11; 35,4 invece di 40,25; 0; 20,3), e `pulisci_istanze` le ha tolte tutte e due. Rifatto `istanze_nuove` senza la vecchia: posto giusto. Ordine: `pulisci_istanze`, poi `istanze_nuove`, poi `controllo`.
- **Fori di asse inclinato**: `Parte.foro_obl` (mezza sezione con `sk_rett_obl` e rivoluzione di 360° attorno all'asse di costruzione). Provato sui fori del ToF posteriore: un gambo Ø2 nel foro Ø1,7 interseca 1,31 mm³, come un foro tondo.
- **Verifiche con corpi temporanei** (`assieme.py` → `_urti_temporanei`, `_corpi_mondo`, `sfilamento_pacco`): non toccano il modello e girano in sola lettura. I giochi si misurano per bisezione ingrandendo il corpo provvisorio; il contatto al passo dopo il gioco è il caso di controllo. `_corpi_mondo` con `salta_comp` contenente "Corpo" salta tutto (errore del 16 ottobre: prova passata senza corpi fissi).
- Dopo `base` le chiamate di sola lettura successive sono andate in timeout per alcuni minuti (Fusion al 100 %): aspettare che il file JSON dell'esito compaia (`until [ -f ... ]` in background) invece di rilanciare.

## Lezioni del 16 ottobre 2026 (versione 2.1.7, blocco zampa)

- **Modificare una lavorazione senza rifare la parte** (rifarla cancella i giunti): `zampa.py` → `aggiorna_217`.
  - Il verso di un'estrusione sta nel segno della distanza (`-( ins_m3_l )`): una espressione positiva gira il taglio nel vuoto ("Nessun corpo di destinazione", il foro sparisce). Tenere il segno.
  - Lo svuotamento con spessore interno nullo non tiene il parametro (`insideThickness` è None): `setThicknesses` con un valore provvisorio non nullo, poi il parametro torna a zero e resta collegato (`_collega_stretta`). `setThicknesses` e `participantBodies` vogliono la timeline subito prima della lavorazione.
  - Dentro un gruppo chiuso della timeline `rollTo` dà "Associated feature is invalid": aprire il gruppo (`isCollapsed = False`), lavorare, `moveToEnd`, richiuderlo.
- **Precisione dei volumi**: `BRepBody.volume` sbaglia di 1-2 mm³ su 12 cm³ (lamatura: 14,77 contro 13,06). Per le differenze piccole usare la differenza booleana fra il corpo prima e dopo (`markerPosition` indietro, `TemporaryBRepManager.copy`, `moveToEnd`) o `getPhysicalProperties(VeryHighCalculationAccuracy)`.
- `measureManager.measureMinimumDistance` sulle facce di un componente annidato vuole i proxy (`createForAssemblyContext`), altrimenti "invalid argument geometryOne".
- Uno spessore di compenetrazione si misura con una sonda 1 × 1 mm intersecata con l'intersezione dei due corpi: il volume in mm³ è lo spessore.

## Lezioni del 16 ottobre 2026 (versione 2.1.7, blocco attrezzi)

- **Scritte incise** (`attrezzi.py` → `_incidi`): `sketchTexts.createInput2` con `setAsMultiLine`, poi la scritta stessa come profilo di `extrudeFeatures.createInput`, con `participantBodies`. Il riquadro nasce libero ma rettangolo: basta un vincolo orizzontale su un lato (il secondo dà "schizzo ipervincolato") e due angoli quotati dall'origine. Anche così `sketch.isFullyConstrained` resta falso: si controllano i lati del riquadro (`rectangleLines`).
- **Undo di uno script intero**: uno script che finisce (anche con l'errore preso in `main`) è una sola transazione; `fusion_mcp_update` → `undo` lo toglie tutto, parametri compresi, e il nome del componente non resta riservato. Rileggere la sentinella dopo.
- **Verifiche di attrezzi su una zampa** (`verifica_bussola`, `verifica_estrattore`): i corpi dell'attrezzo si copiano dal componente di libreria e si portano nel mondo con terna dell'attrezzo → terna della zampa → `nativa⁻¹ · proxy` della parte (`_terna`). Perni e cuscinetti sono istanze dello stesso componente: si riconoscono dalla X nativa (`_parti_zampa`). Un perno nel suo foro dello stesso diametro non dà intersezione: quel gioco si calcola.
