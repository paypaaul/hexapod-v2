# Hexapod v2

Robot esapode a 18 gradi di libertà (6 zampe × 3 servo), stampato in 3D, che verrà costruito davvero.
Questa repo è la memoria del progetto: una sessione nuova deve poter ripartire leggendo solo questi file.

## Stato attuale

> Aggiornare questa sezione alla fine di ogni fase.

**Dall'8 ottobre 2026 (notte) `main` è la versione con i servo MG996R.** La prima versione, progettata per errore attorno agli MG90S, è congelata nel branch **`mg90s`** (commit `5001f71`): modello Fusion "Hexapod v2 - Assieme", zampa e corpo verificati, due modi di marcia. Su `main` i suoi documenti e script restano solo come consultazione in `docs/mg90s/` e `cad/script/mg90s/`: **non vanno aggiornati qui**; se un giorno si riprende quel robot si lavora sul branch.

| Fase (versione MG996R) | Stato |
|---|---|
| 0. Riorganizzazione della repo | **fatta** (2026-10-08): branch `mg90s`, archivio su `main`, questo file riscritto |
| 1. Studio di ciò che cambia | **da fare**: servo MG996R di AZDelivery (dati su fonte primaria, squadrette, corrente reale), alimentazione per circa 25–45 A di stallo, giunti più grandi, dimensionamento, volume di stampa |
| 2. BOM e revisione | da fare; poi **fermarsi per l'approvazione dell'utente** |
| 3. Dimensioni e modelli 3D | da fare, in un **nuovo design Fusion** |
| 4. Progettazione CAD | da fare |
| 5. BOM finale (viteria dal modello) | da fare |
| 6. Verifica del movimento | da fare |

Prossimo passo: vedi in fondo, "Prossimi passi".

## Cosa è deciso dall'utente (non si cambia senza chiederlo)

- **Servo**: 18 × **MG996R di AZDelivery** (confezioni da 5, Amazon), gli stessi della sua v1. Li ha già. Gli MG90S non si usano in questo robot.
- **Si costruisce solo la versione MG996R.** La versione MG90S resta congelata nel branch `mg90s`; forse più avanti verrà rifinita.
- **Libertà di progetto** (8 ottobre 2026): la versione grande va fatta come se si partisse da zero. Non va limitata per riusare il più possibile la versione piccola; si può cambiare qualunque scelta, anche a costo di più lavoro.
- **Controllo**: scheda UICPAL "ESP32-S3-CAM N16R8 RE1.3" (AliExpress 1005008519401021); camera UICPAL "OV3660-75MM" con flat da 75 mm e lente da 120° "GOOD"; servo controller clone "SSC32-V2.5" (AliExpress 1005001888185034). Dati in `docs/mg90s/dimensioni-componenti.md`, da riportare nel nuovo documento delle dimensioni.
- **Batteria**: la OVONIC 2S 5200 mAh hardcase che ha già (137–139 × 46–47 × 24–25 mm, 245–259 g) torna la candidata naturale; da confermare nel dimensionamento.
- **Assetto**: l'utente si aspetta la marcia classica, bassa, con il ginocchio sotto i 90°. Accetta di superare il 50 % dello stallo, ma l'assetto definitivo si sceglie a robot costruito: la meccanica deve permettere un campo ampio di assetti.
- **Acquisti**: preferire la soluzione senza componenti in più, salvo problemi funzionali o estetica sgradevole. Ogni voce nuova del BOM va approvata.
- **Produzione**: FlashForge **Creator 5 Pro**, toolchanger a 4 testine, ugelli temprati da 0,4 mm; PLA / PLA-CF / PETG / PETG-CF. Supporti con interfaccia in altro materiale ammessi, ma al minimo.
- Le fonti d'acquisto di cuscinetti e perni le cura l'utente.
- Blender si valuta solo dopo che la fase 6 è completa e verificata.

## Regole di lavoro

- Lingua dei documenti: italiano.
- Se manca un'informazione che solo l'utente può dare (foto, misura sul pezzo reale, link d'acquisto), **chiedere** invece di assumere. Per schede e servo con varianti o cloni chiedere foto o link se la versione non è univoca.
- Tutto il resto si decide e si annota in `docs/decisioni.md` con il perché.
- Ogni dato chiave (dimensioni, tensioni, correnti) va controllato su fonte primaria (datasheet o pagina del produttore) e marcato **verificato / stimato / da confermare**.
- A fine fase: riepilogo breve all'utente (verificato / assunzione / aperto) e aggiornamento di questo file.
- Dopo la fase 2 ci si ferma: il BOM va approvato dall'utente prima di acquisti e CAD.
- Git: commit solo quando l'utente lo chiede (eccezione fatta l'8 ottobre per la riorganizzazione dei branch, chiesta da lui). Mai push se non lo chiede.
- L'utente ha un limite d'uso a finestre: lavorare a blocchi che lasciano repo e Fusion in uno stato da cui ripartire; niente flussi con molti agenti se non li chiede.

## Mappa della repo

| Percorso | Contenuto |
|---|---|
| `CLAUDE.md` | questo file: stato, decisioni dell'utente, regole, note sul connettore Fusion, prossimi passi |
| `docs/decisioni.md` | registro delle decisioni della versione MG996R (riparte da D-041; quelle ereditate sono riassunte in testa) |
| `docs/` (da creare man mano) | `BOM.md`, `dimensioni-componenti.md`, `dimensionamento.md`, `progetto-meccanico.md` della versione MG996R |
| `docs/mg90s/` | **archivio di sola consultazione** della versione MG90S: BOM, decisioni D-001…D-040, dimensionamento, dimensioni, progetto meccanico, revisioni, immagini |
| `cad/script/lib_cad.py` | libreria per gli schizzi vincolati via API: generica, si riusa |
| `cad/script/mg90s/` | **archivio**: `zampa.py`, `corpo.py`, `assieme.py`, `verifica_zampa.py`, `rif_componenti.py` della versione MG90S. Sono la base da cui scrivere gli script nuovi, non si eseguono da qui |
| `calc/` | `statica_tripode.py`, `assetti.py`, `andature.py`: motore di calcolo generico, ancora configurato sugli MG90S (da riparametrizzare nella fase 1) |
| `research_notes/`, `reports/` | ricerca della prima versione: valida per ESP32, SSC-32, camera e cablaggio; superata per servo, alimentazione e dimensionamento |

## Fusion

- Il progetto Fusion si chiama **"Hexabot v2"** (id `202512011021193576`), non `hexapod-v2`. Hub: "Paul's team".
- File esistenti nel progetto (NON modificare né cancellare senza chiedere):
  - `Tower Pro MG90S Micro servo` (file dell'utente) — lineage `urn:adsk.wipprod:dm.lineage:WfZcQDYtQ2mcTssS11zxYw`
  - `Hexapod v2 - Assieme` (versione MG90S, congelata: 216 parametri, timeline 81). Da non toccare più; chiesto all'utente se rinominarlo "Hexapod v2 - MG90S".
- **La versione MG996R si modella in un design nuovo** (deciso con l'utente l'8 ottobre 2026): parametri e timeline dei due robot non si mescolano. Da creare all'inizio della fase 3. Da valutare lì se tenere la zampa in un file a parte, inserita per riferimento come il servo.
- Serve un modello dell'MG996R: chiedere all'utente se ne ha uno (magari dalla v1); altrimenti ingombro dalle quote ufficiali.
- Script Fusion in `cad/script/`; si lanciano con `runpy.run_path(percorso)['main']()` dentro lo script del connettore, così restano nella repo.
- Dopo ogni gruppo di operazioni rileggere lo stato del modello (script di sola lettura) o fare uno screenshot: assenza di errore non significa risultato corretto.
- Nelle note sul connettore qui sotto, i nomi `zampa.py`, `corpo.py`, `assieme.py` si riferiscono agli script della versione MG90S (`cad/script/mg90s/`): le particolarità descritte valgono in generale.

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

## Dati già accertati per la versione MG996R

Servo MG996R. Fonti lette l'8 ottobre 2026: pagina Tower Pro [towerpro.com.tw/product/mg996r](https://www.towerpro.com.tw/product/mg996r/) e pagina AZDelivery [az-delivery.de/products/az-delivery-servo-mg996r](https://www.az-delivery.de/products/az-delivery-servo-mg996r). I servo dell'utente sono AZDelivery: dove le due fonti divergono vale la misura sul pezzo.

| Dato | Tower Pro | AZDelivery | Stato |
|---|---|---|---|
| Peso | 55 g | non dichiarato | da pesare |
| Ingombro | 40,7 × 19,7 × 42,9 mm | 40 × 19 × 43 mm | da misurare |
| Quote del disegno (stesse lettere dell'MG90S) | A 42,7 · B 40,9 · C 37 · D 20 · E 54 · F 26,8 mm | — | da misurare |
| Coppia di stallo | 9,4 kgf·cm a 4,8 V; 11 a 6,0 V | 11 a 6,0 V | dichiarata; reale da misurare |
| Tensione operativa | 4,8–6,6 V | 4,8–7,2 V | **divergono** |
| Corrente | 10 mA a riposo, 170 mA a vuoto, **1,4 A di stallo** | non dichiarata | molti rivenditori dichiarano 2,5 A di stallo a 6 V: **da misurare** |
| Velocità | 0,19 s/60° a 4,8 V; 0,15 a 6 V | 0,17 e 0,13 | — |
| Cavo e connettore | 32 cm, JR | — | — |
| Corsa | — | circa 180° | da misurare |

AZDelivery pubblica un datasheet PDF ([Servo_MG996R_Datenblatt.pdf](https://cdn.shopify.com/s/files/1/1509/1638/files/Servo_MG996R_Datenblatt.pdf)) e un eBook. Il PDF è fatto di sole immagini: letta la copertina (il servo arriva con squadrette di plastica a croce, a due bracci e a disco, quattro viti autofilettanti con gommini e boccole di ottone, vite della squadretta; l'albero è un millerighe in ottone), **la tabella dei dati è ancora da leggere** (estrarre le pagine o chiedere all'utente una foto).

Stima preliminare (stessa statica della versione piccola; coxa 50, femore 75, tibia 120 mm; 2,1–2,4 kg; asse dei femori a 90 mm, piede a 50 mm dall'asse; passo 70 mm): 4,7–5,4 kgf·cm, cioè 43–49 % degli 11 kgf·cm dichiarati (52–60 % se lo stallo reale è 9). L'assetto classico sta attorno al 50 %. Sono numeri d'ordine di grandezza: la geometria è tutta da progettare.

## Cosa resta valido dalla versione MG90S

- **Metodo**: schizzi a un contorno completamente vincolati con quote da parametri (`lib_cad.py`), un componente per parte, giunti veri, verifica dopo ogni blocco, sentinella sui volumi delle altre parti, interferenze, pose per istanza e ciclo a tripode (`cad/script/mg90s/assieme.py`).
- **Calcolo**: statica a tripode e confronto degli assetti (`calc/`), da riparametrizzare.
- **Idee di architettura** che hanno funzionato (da rivalutare in scala, non da copiare): giunti sostenuti su due lati con cuscinetto e perno coassiali al servo; femore in due pezzi con le culle che gli girano attorno; coxa a C; gondole dei servo di coxa nello scafo; vasca strutturale con tunnel chiuso per la batteria e guscio non strutturale; vano di servizio in coda; ESP32 su vassoio con la camera su una torretta della base; sportelli a incastro; viti con inserti a caldo e dadi quadri.
- **Lezioni**: la coppia è carico per distanza orizzontale, quindi l'assetto si decide insieme alle lunghezze dei segmenti; le escursioni dei giunti vanno dimensionate sull'assetto più basso con il piede alzato; lo spazio per cavi dei servo e alimentazione va contato prima di fissare la pianta; la stabilità cresce abbassando e allargando.
- **Elettronica di controllo**: ESP32, camera e SSC-32 sono le stesse (pinout, UART1 su GPIO21/14 a 115200 baud con traslatore di livello, interruttore a pulsante sul ramo logica, misura di batteria su GPIO1). Dettagli in `docs/mg90s/BOM.md` e `docs/mg90s/dimensioni-componenti.md`.
- **Da rifare**: quote, disposizione del corpo, bilancio di massa, cuscinetti e perni, tutta l'alimentazione dei servo (i due Pololu da 11 A e i morsetti della SSC-32 non reggono 18 MG996R: la potenza va distribuita fuori dalla SSC-32).

## Prossimi passi

1. **Avere dall'utente** (chiesto l'8 ottobre): cosa ha già comprato del vecchio BOM; come alimentava i servo nella v1, se ha file o foto della v1 e cosa non andava; se ha un modello 3D dell'MG996R; se vuole rinominare il vecchio design Fusion.
2. **Fase 1 ridotta**, senza flussi con molti agenti:
   - MG996R: datasheet AZDelivery, corrente di stallo reale (misura su un pezzo), millerighe a 25 denti e squadrette metalliche, quote reali;
   - alimentazione: tensione del rail (6,0–7,2 V), regolatori o BEC per la corrente che serve, distribuzione separata dalla SSC-32, fusibili, sezioni dei cavi;
   - giunti: cuscinetti e perni adeguati a oltre 2 kg;
   - dimensionamento: masse, lunghezze dei segmenti, assetto classico attorno al 50 %, escursioni dei giunti, autonomia con la 5200 mAh;
   - stampa: volume utile della Creator 5 Pro e divisione del corpo.
3. **Fase 2**: nuovo `docs/BOM.md`, poi fermarsi per l'approvazione.
4. Fasi 3–6 come per la prima versione, nel nuovo design Fusion.
