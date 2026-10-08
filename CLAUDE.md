# Hexapod v2

Robot esapode a 18 gradi di libertà (6 zampe × 3 servo), stampato in 3D, che verrà costruito davvero.
Questa repo è la memoria del progetto: una sessione nuova deve poter ripartire leggendo solo questi file.

## Stato attuale

> Aggiornare questa sezione alla fine di ogni fase.

| Fase | Stato |
|---|---|
| 0. Esplorazione connettore Fusion | **fatta** (2026-10-08) — vedi "Connettore Fusion" |
| 1. Studio dei componenti | **fatta** (2026-10-08) — report in `reports/`, note e verifiche in `research_notes/` |
| 2. BOM e revisione | **fatta e approvata** (2026-10-08): BOM v1.2. L'utente ha risposto alle domande, confermato i Pololu e delegato la batteria (D-027) |
| 3. Dimensioni e modelli 3D | **fatta** (2026-10-08): tabella in `docs/dimensioni-componenti.md`; design Fusion "Hexapod v2 - Assieme" con 68 parametri, servo per riferimento, STEP Pololu e ingombri |
| 4. Progettazione CAD | **in corso**. Fatto: zampa v0 modellata, assemblata e verificata con i giunti veri (`docs/progetto-meccanico.md`). Da fare: rifinitura della zampa, corpo (progettato sulla carta), sei zampe sull'assieme, cover |
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
| `cad/script/` | script Fusion: `lib_cad.py` (schizzi vincolati), `zampa.py`, `verifica_zampa.py`, `rif_componenti.py` |
| `docs/revisioni/` | revisioni indipendenti dei documenti (BOM v1: elettrico, meccanico, acquisti) |
| `calc/` | script di calcolo riproducibili (statica, cinematica) |
| `research_notes/<titolo>/` | note grezze dei ricercatori e file `verifica_*.md` (controllo su fonte primaria) |
| `reports/<titolo>.md` | report di sintesi della ricerca |

## Fusion

- Il progetto Fusion si chiama **"Hexabot v2"** (id `202512011021193576`), non `hexapod-v2`. Hub: "Paul's team".
- File esistenti nel progetto (NON modificare né cancellare senza chiedere):
  - `Tower Pro MG90S Micro servo` (f3d importato da STEP, corpo unico) — lineage `urn:adsk.wipprod:dm.lineage:WfZcQDYtQ2mcTssS11zxYw`
- Il lavoro si fa nel design **"Hexapod v2 - Assieme"** dentro "Hexabot v2" (creato l'8 ottobre 2026). Contiene i parametri utente e, in una zona libreria a y ≥ 200 mm, i componenti di riferimento (elenco in fondo a `docs/dimensioni-componenti.md`). L'origine è libera per il robot.
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
- **`Parte.sk_poligono` non funziona ancora**: quotando ogni vertice dall'origine (orizzontale e verticale), Fusion segnala "schizzo ipervincolato" su alcune quote anche se `geometricConstraints` è vuoto. Prova su un esagono con vertici (20,−10), (20,10), (7.66,25), (−20,10), (−20,−10), (0,−25): fallisce la quota x del secondo vertice (stessa x del primo) e la quota y del quinto (stessa y del primo, non collegati da un lato). Ipotesi: Fusion deduce allineamenti tra punti con la stessa coordinata. Da provare: spostare leggermente i punti alla creazione e lasciare che le quote li portino al valore, oppure quote allineate rispetto a linee di costruzione.
- Guida Autodesk (connettore Knowledge): `search_help_content` con `product_code: F360`, `locale: it_IT`.

## Dati già accertati

- Servo MG90S, quote dal modello STEP dell'utente e quote ufficiali Tower Pro: vedi `docs/dimensioni-componenti.md`.
- Scheda ESP32-S3-CAM: identificata dalle immagini dell'inserzione; pinout e quote in `docs/dimensioni-componenti.md`.

## Prossimi passi

Stato all'8 ottobre 2026 (sessione chiusa su richiesta dell'utente, tutto salvato e committato). Design Fusion "Hexapod v2 - Assieme" salvato con: componenti di riferimento in libreria (y ≥ 200 mm), componente `Zampa` all'origine. Leggere **`docs/progetto-meccanico.md`** prima di proseguire: contiene l'architettura della zampa e il piano del corpo.

1. **Chiedere all'utente** se approva la prolunga USB-C da pannello (D-034, voce C9 del BOM): decide dove sta la scheda ESP32 nel corpo.
2. **Corpo**: modellarlo secondo `docs/progetto-meccanico.md`. Prima scegliere come fare le gondole ruotate: sistemare `Parte.sk_poligono` (vedi nota sotto) oppure gondola come componente a sé istanziato sei volte.
3. **Assieme**: corpo fissato alla radice, sei istanze di `Zampa`, giunto di rivoluzione al livello radice tra corpo e `Coxa` di ogni istanza; poi posa di marcia e controllo di interferenze, massa e baricentro.
4. **Rifinitura della zampa**: elenco in `docs/progetto-meccanico.md` ("Da rifinire").
5. Cover non strutturali, poi fasi 5 e 6.
6. Ancora da avere dall'utente: misure del servo (denti, vite centrale, fori alette, squadretta); altezza reale della testa della camera; regolatore, piste e morsetti della SSC-32; prova del pin 5V; pesi.

Come si rigenera la zampa: dentro uno script del connettore, `ns = runpy.run_path('/Users/paul/hexapod-v2/cad/script/zampa.py'); ns['main']([...])` con i passi `parametri`, `coxa`, `femore_b`, `femore_a`, `tibia`, `istanze`, `giunti`, `stato`, `interferenze`. Dopo aver rigenerato una parte vanno rifatti `istanze` e poi `giunti`, in due chiamate separate, e reimpostati i limiti dei giunti (femore da −25° a +70°, ginocchio da −70° a +25° come valori di giunto). Verifica: `cad/script/verifica_zampa.py`.

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
