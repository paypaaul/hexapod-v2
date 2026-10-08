# Hexapod v2

Robot esapode a 18 gradi di libertà (6 zampe × 3 servo), stampato in 3D, che verrà costruito davvero.
Questa repo è la memoria del progetto: una sessione nuova deve poter ripartire leggendo solo questi file.

## Stato attuale

> **In sospeso dall'8 ottobre 2026, notte (D-040).** L'utente ha detto di aver sbagliato servo: voleva usare gli **MG996R** della sua v1, non gli MG90S del file Fusion. Ha entrambi. Tutto ciò che segue descrive la versione MG90S, che è coerente e verificata ma è un robot diverso (circa 1 kg invece di oltre 2 kg). **Non proseguire con i dettagli della versione MG90S finché l'utente non ha deciso come procedere.**

> Aggiornare questa sezione alla fine di ogni fase.

| Fase | Stato |
|---|---|
| 0. Esplorazione connettore Fusion | **fatta** (2026-10-08) — vedi "Connettore Fusion" |
| 1. Studio dei componenti | **fatta** (2026-10-08) — report in `reports/`, note e verifiche in `research_notes/` |
| 2. BOM e revisione | **fatta e approvata** (2026-10-08): BOM v1.2. L'utente ha risposto alle domande, confermato i Pololu e delegato la batteria (D-027) |
| 3. Dimensioni e modelli 3D | **fatta** (2026-10-08): tabella in `docs/dimensioni-componenti.md`; design Fusion "Hexapod v2 - Assieme" con 68 parametri, servo per riferimento, STEP Pololu e ingombri |
| 4. Progettazione CAD | **in corso**. Fatto: zampa v0 con il femore a puntone (ginocchio 50–145°, femore da −60° a +55°); corpo v0 (base, guscio sfaccettato fissato con 8 viti M2, vassoio ESP32, due sportelli a incastro); assieme con sei zampe, servo di coxa, elettronica e giunti delle coxe; ciclo a tripode verificato senza interferenze nei due modi di marcia, alto e basso (`docs/progetto-meccanico.md`). Da fare: vano di servizio, rifiniture di zampa e corpo, estetica |
| 5. BOM finale (viteria dal modello) | da fare |
| 6. Verifica del movimento | da fare |

Prossimo passo: vedi in fondo, "Prossimi passi".

## Cosa è deciso dall'utente (non si cambia senza chiederlo)

- **Servo**: 18 × Tower Pro MG90S (identificato dal file nel progetto Fusion).
- **Controllo**: scheda UICPAL "ESP32-S3-CAM N16R8 RE1.3" (AliExpress 1005008519401021). Si alimenta dal pin 5V; alternativa prevista: spinotto USB-C (D-028).
- **Camera**: UICPAL "OV3660-75MM", flat da 75 mm (AliExpress 1005007456301694), lente da 120° "GOOD" a testa compatta.
- **Servo controller**: clone "SSC32-V2.5" con micro-USB e XBee (AliExpress 1005001888185034), PCB 72 × 55 mm, fori 65,5 × 48,5 mm.
- **Regolatori servo**: due Pololu D42V110F6 (confermati l'8 ottobre 2026).
- **Batteria**: OVONIC 2S 2200 mAh 50C T-plug (D-027), confermata dall'utente. La 5200 mAh hardcase che ha in casa resta per il banco.
- **Produzione**: FlashForge **Creator 5 Pro**, ugelli temprati da 0,4 mm anche per i caricati; materiali PLA / PLA-CF / PETG / PETG-CF. È un toolchanger a 4 testine: i supporti con interfaccia in un altro materiale sono ammessi quando migliorano funzione, estetica o semplicità; restano da ridurre al minimo per non sprecare materiale.
- Le fonti d'acquisto di cuscinetti e perni le cura l'utente.
- **Due modi di marcia** (D-039, 8 ottobre 2026): l'utente accetta di superare il 50 % dello stallo per camminare più basso, con il ginocchio sotto i 90° come negli esapodi comuni; quale assetto usare si decide a robot costruito. La meccanica deve permettere sia il modo alto (asse a 72 mm, 44 %) sia il modo basso (asse a 40 mm, piede a 40 mm, 89 %). La regola del 50 % resta il riferimento solo per il modo alto.
- **Porta USB**: l'utente ha delegato la scelta chiedendo di evitare acquisti in più se non creano problemi funzionali o estetici. Scelto: nessuna prolunga, sportello di servizio sul dorso (D-034). Vale come criterio generale: prima la soluzione senza componenti aggiuntivi.
- Blender si valuta solo dopo che la fase 6 è completa e verificata.

## Regole di lavoro

- Lingua dei documenti: italiano.
- Se manca un'informazione che solo l'utente può dare (foto, misura sul pezzo reale, link d'acquisto), **chiedere** invece di assumere. Per schede con varianti/cloni (ESP32-S3-CAM, SSC-32) chiedere foto o link se la versione non è univoca.
- Tutto il resto si decide e si annota in `docs/decisioni.md` con il perché.
- Ogni dato chiave (dimensioni, tensioni, correnti) va controllato su fonte primaria (datasheet o pagina del produttore) e marcato **verificato / stimato / da confermare**.
- A fine fase: riepilogo breve all'utente (verificato / assunzione / aperto) e aggiornamento di questo file.
- Dopo la fase 2 ci si ferma: il BOM va approvato dall'utente prima di acquisti e CAD.
- Git: non fare commit se l'utente non lo chiede. Primo commit fatto l'8 ottobre 2026 su sua richiesta.

## Mappa della repo

| Percorso | Contenuto |
|---|---|
| `CLAUDE.md` | questo file: convenzioni, stato, prossimi passi, note sul connettore Fusion |
| `docs/BOM.md` | distinta base (componente, quantità, codice, specifiche, dove comprare, stato) |
| `docs/dimensioni-componenti.md` | tabella delle dimensioni reali dei componenti, con fonte |
| `docs/decisioni.md` | registro delle decisioni con il perché |
| `docs/dimensionamento.md` | massa, geometria delle zampe, coppie ai giunti |
| `docs/progetto-meccanico.md` | architettura della zampa (modellata e verificata) e piano del corpo (da modellare) |
| `cad/script/` | script Fusion: `lib_cad.py` (schizzi vincolati), `zampa.py`, `verifica_zampa.py`, `corpo.py` (base, guscio, vassoio), `assieme.py` (zampe, istanze, giunti, interferenze, massa), `rif_componenti.py` |
| `docs/immagini/` | screenshot dell'assieme |
| `docs/revisioni/` | revisioni indipendenti dei documenti (BOM v1: elettrico, meccanico, acquisti) |
| `calc/` | script di calcolo riproducibili: `statica_tripode.py` (modo alto), `assetti.py` (altezze e inclinazioni possibili), `andature.py` (assetti e andature a confronto: coppia, stabilità, alzata) |
| `research_notes/<titolo>/` | note grezze dei ricercatori e file `verifica_*.md` (controllo su fonte primaria) |
| `reports/<titolo>.md` | report di sintesi della ricerca |

## Fusion

- Il progetto Fusion si chiama **"Hexabot v2"** (id `202512011021193576`), non `hexapod-v2`. Hub: "Paul's team".
- File esistenti nel progetto (NON modificare né cancellare senza chiedere):
  - `Tower Pro MG90S Micro servo` (f3d importato da STEP, corpo unico) — lineage `urn:adsk.wipprod:dm.lineage:WfZcQDYtQ2mcTssS11zxYw`
- Il lavoro si fa nel design **"Hexapod v2 - Assieme"** dentro "Hexabot v2" (creato l'8 ottobre 2026). Contiene 216 parametri utente; in una zona libreria a y ≥ 200 mm i componenti di riferimento (elenco in fondo a `docs/dimensioni-componenti.md`); all'origine il robot: sotto-assieme `Corpo` (fissato) e sei istanze di `Zampa`.
- Script Fusion riutilizzabili in `cad/script/`; si lanciano con `runpy.run_path(percorso)['main']()` dentro lo script del connettore, così restano nella repo.
- Modelli scaricati in `cad/modelli/`, uno per cartella.
- Dopo ogni gruppo di operazioni rileggere lo stato del modello (script di sola lettura) o fare uno screenshot: assenza di errore non significa risultato corretto.

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
- `transform2` di un'occorrenza annidata non si imposta sull'oggetto nativo ("transform overrides can only be set on Occurrence proxy from root component"): la posizione giusta va data alla creazione.
- Nel sotto-assieme nessuna parte è fissata (`isGrounded` non esiste per le occorrenze annidate): le misure di posa vanno fatte rispetto a una parte di riferimento (la coxa).
- Per trovare cosa blocca un giunto: sospendere i giunti rigidi uno alla volta (`isSuppressed`) e riprovare.
- Le interferenze trovano anche i dettagli del modello STEP: i tre fili del cavo del servo (4,71 mm³) hanno rivelato che mancava l'uscita del cavo nella culla.
- Libreria per gli schizzi vincolati: `cad/script/lib_cad.py` (un contorno per schizzo, quote dall'origine come espressioni; provata su volume e ingombro).
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

## Dati già accertati

- Servo MG90S, quote dal modello STEP dell'utente e quote ufficiali Tower Pro: vedi `docs/dimensioni-componenti.md`.
- Scheda ESP32-S3-CAM: identificata dalle immagini dell'inserzione; pinout e quote in `docs/dimensioni-componenti.md`.

## Prossimi passi

Stato all'8 ottobre 2026, notte. Design Fusion "Hexapod v2 - Assieme" salvato (timeline 81, 216 parametri): libreria a y ≥ 200 mm; all'origine `Corpo` (fissato: `Corpo_Base`, `Corpo_Guscio`, `Vassoio_ESP32`, `Sportello_Dorso`, `Sportello_Coda`, 6 servo di coxa, 6 cuscinetti, batteria, SSC-32, ESP32, 2 regolatori) e sei `Zampa` con i giunti `G_coxa_*`. Nessuna interferenza, né nella posa di riferimento né nell'assetto di marcia. Leggere **`docs/progetto-meccanico.md`** prima di proseguire.

L'utente ha visto l'assieme, ha chiesto di verificare altezza da terra e proporzioni (D-037) e poi di progettare il robot per camminare sia alto sia basso (D-039: fatto, femore modificato e ciclo verificato nei due modi). Il lavoro prosegue con i dettagli.

1. **Corpo, resto della fase 4** (elenco in `docs/progetto-meccanico.md`, "Da fare nel corpo"): sedi nel vano di servizio in coda (servono gli ingombri reali di T-plug e portafusibili); alleggerimento dei colli d'angolo; guide dei cavi; muso del guscio. Già fatti: tasche dei dadi M2 nelle gondole, feritoie dei regolatori, nervature, linguette.
2. **Rifinitura della zampa**: elenco in `docs/progetto-meccanico.md` ("Da rifinire nella zampa"). Il femore è già stato rifatto con il puntone (D-039); resta da provarlo in stampa. Dopo aver cambiato una parte della zampa aggiornare `VOLUMI_ATTESI` in `corpo.py`.
3. **Estetica**: raccordi e linee; solo dopo che la funzione è chiusa.
4. **Fase 5**: BOM finale con la viteria ricavata dal modello (inserti M2 e M3, viti delle alette, viti del femore, 8 viti del guscio, viti della SSC-32 che stringono anche il vassoio).
5. **Fase 6**: il ciclo a tripode nei due modi è già verificato per le interferenze (`assieme.py` → `ciclo`). Restano: rotazione sul posto e marcia laterale, baricentro nel poligono d'appoggio fase per fase, campo visivo della camera nelle pose reali, corsa dei servo con la squadretta a metà.
6. Ancora da avere dall'utente: misure del servo (denti, vite centrale, fori alette, squadretta); altezza reale della testa della camera; altezza dello zoccolo XBee, regolatore, piste e morsetti della SSC-32; prova del pin 5V; posizione dei pulsanti BOOT e RST sull'ESP32; pesi.

Come si rigenerano corpo e assieme: vedi "Come si rigenera" in `docs/progetto-meccanico.md`. In breve: `corpo.py` → `main(['parametri', 'scafo', 'gondole', 'lavorazioni', 'interno', 'stato'])`, poi in chiamate separate `guscio`, `vassoio`, `sportelli`; poi `assieme.py` → `giunti_corpo` e, in una chiamata separata, `giunti_coxa`; controllo con `interferenze`, `massa` e `scansione` (due zampe per chiamata).

Come si rigenera la zampa: dentro uno script del connettore, `ns = runpy.run_path('/Users/paul/hexapod-v2/cad/script/zampa.py'); ns['main']([...])` con i passi `parametri`, `coxa`, `femore_b`, `femore_a`, `tibia`, `istanze`, `giunti`, `stato`, `interferenze`. Dopo aver rigenerato una parte vanno rifatti `istanze`, `giunti` e `limiti`, in chiamate separate (limiti attuali: femore da −60° a +55°, ginocchio da 50° a 145°, in `LIMITI`); `controllo` rilegge le posizioni native delle istanze. Rifare la `Coxa` cancella anche i giunti `G_coxa_*`. Verifica: `cad/script/verifica_zampa.py`.

## Risultati chiave della fase 1 (dettagli nei documenti)

- Servo: 2S diretta esclusa; rail a 6,0 V; stallo 0,95 A per servo, 17 A in tutto. Coppia di progetto 2,0 kgf·cm a 6,0 V.
- "SSC-32 V2.5" = clone cinese della SSC-32U (micro-USB + XBee), 72 × 55 mm, fori 65,5 × 48,5 mm dal disegno del venditore: non usare la dima Lynxmotion.
- ESP32: il pin 5V potrebbe essere solo un'uscita (schema del venditore): **da provare** prima di decidere come alimentarla.
- Camera: l'utente ha il modulo con flat da 75 mm; niente prolunghe FPC.
- Squadretta metallica per MG90S: non ne esiste una verificata; denti 20 o 21 **da contare**.
- Il vincolo del 50 % regge con assetto alto e raccolto: 44 % a 1,05 kg con la batteria da 2200 mAh; dipende da massa e coppia reali.
- Alimentazione: nessun interruttore nel percorso dei servo; rail servo spento di default e acceso dai pin ENA dei due regolatori Pololu (D-019).
- Domande ancora aperte: in fondo a `docs/BOM.md`.
- Limite d'uso della sessione: i workflow con molti agenti lo esauriscono (tre interruzioni l'8 ottobre). Far scrivere agli agenti i risultati su file man mano, e preferire pochi agenti con compiti stretti.
