# Circuiti stampati (PCB)

Progetti KiCad delle schede del robot. Piano, scelte e fasi: `docs/piano-pcb.md` (D-078).

## Versione di KiCad

**KiCad 10.0.7**. Gli script e la CI usano questa; un'altra 10.0.x va provata prima (formato dei file, DRC).
Sul Mac: `/Applications/KiCad/KiCad.app`, con `kicad-cli` in `Contents/MacOS/` e il Python di KiCad (3.9, con `pcbnew`) in `Contents/Frameworks/Python.framework/Versions/Current/bin/python3`. I percorsi si cambiano con le variabili `KICAD_CLI`, `KICAD10_SYMBOL_DIR` e `KICAD10_FOOTPRINT_DIR`.

## Come sono fatti i progetti

Schema e PCB **si generano da script**, e i file di KiCad sono il risultato. Una modifica si fa nello script e si rigenera: una modifica fatta solo nell'editor si perde alla rigenerazione. L'editor serve per guardare (schema, PCB, 3D) e per provare; quello che si vuole tenere torna nello script.

| Passo | Script | Python |
|---|---|---|
| copie dei simboli e delle impronte standard in `librerie/` | `script/librerie.py` (`--controlla`; vuole le librerie di KiCad installate) | qualunque |
| simboli e impronte disegnati per il robot (ESP32 RE1.3, D24V22F5, PTC e 470 µF sdraiati) in `librerie/hex2.*` | `script/propri.py` (`--controlla`) | qualunque |
| schema: simboli, fili, etichette, segni di non collegato | `<scheda>/genera_schema.py`, con `script/schema_kicad.py` | qualunque, con `kicad-cli` |
| PCB: impronte con le reti della netlist, contorno, piste, vie, riempimenti | `<scheda>/genera_pcb.py`, con `script/scheda_kicad.py` | di KiCad (`pcbnew`) |
| ERC, DRC con la parità dello schema (se c'è già il PCB) e reti contro la guida | `script/controlla.py <cartella>` | qualunque, con `kicad-cli` |
| regole del DRC: fonte unica `regole/hex2.kicad_dru`, copiata in ogni progetto come `<nome>.kicad_dru` | `script/regole.py` (`--controlla`) | qualunque |
| contorno, fori Ø2,4 e zone senza rame dalle quote del CAD | `script/genera_contorni.py` (`--controlla <file>.kicad_pcb`); nel PCB `Scheda.contorni_dal_cad` | qualunque |
| reti di KiCad contro `guida/schemi/sorgenti/*_def.py`, con le differenze volute in `aggiunte.yaml` | `script/verifica_reti.py <scheda> <file>.net` | qualunque, con PyYAML |

Piazzamento sul lato B: KiCad ribalta l'impronta specchiando la Y; con 180 gradi in più la scheda si guarda dall'alto del robot (X specchiata). `pcb/stato.yaml` dice in che fase è ogni scheda: in "piazzamento" `controlla.py` conta a parte le connessioni da sbrogliare e gli avvisi di serigrafia.

Regole degli script:
- lo schema ha un tratto di filo e un'etichetta su ogni pin collegato, e il segno di non collegato sui pin liberi. Un pin senza né l'uno né l'altro, o una rete su un pin che non esiste, fermano il generatore prima di KiCad;
- gli identificativi sono ripetibili (uuid derivati dai nomi nello schema, generatore con il seme nel PCB): rigenerare senza modifiche dà gli stessi file;
- lo schema passa da `kicad-cli sch upgrade --force`, così è nel formato in cui lo salverebbe KiCad;
- il PCB copia nelle impronte quello che copierebbe "Aggiorna PCB dallo schema": percorso del simbolo, foglio, campi, esclusione dalla distinta, non montare;
- `controlla.py` fallisce su qualunque rilievo, anche sugli avvisi.

Terna: x = X del robot + 100, y = 100 − Y del robot (KiCad ha la Y verso il basso). Le schede si guardano dall'alto del robot; i componenti della scheda del carapace stanno sul retro (B.Cu). Lo STEP con `--user-origin 100x100mm` torna nella terna del robot (`cad/CLAUDE.md`, STEP delle PCB).

Numeri dei pin per `verifica_reti.py`: ESP32 (U1) da 1 a 20 la fila `ESP_L` dalla coda alla testa, da 21 a 40 la fila `ESP_R` nello stesso verso; D24V22F5 (U2) PG 1, EN 2, VIN 3, GND 4, VOUT 5; condensatori con il + sul pin 1; resistenze e diodi a due fori con il primo foro dei `*_def.py` sul pin 1 (per i diodi il catodo). Le impronte di U1 e U2 si fanno con questa numerazione.

Testata J2 del carapace: pad n = polo n del cavo piatto; poli dispari sulla fila lato chiave, a 4,38 dalla scatola (S-26). Da provare sulla dima con la spina (F5).

**Regole del DRC**: se una sola regola di `regole/hex2.kicad_dru` è scritta male, KiCad ignora tutto il file senza avvisi e il DRC esce a zero. Ogni modifica alle regole passa da `tests/test_pcb.py` (il caso della pista stretta usa la copia vera delle regole) e una regola nuova ha il suo caso di controllo.

Librerie: `librerie/hex2_kicad.kicad_sym` (simboli copiati da KiCad 10, appiattiti) e `librerie/hex2.pretty` (impronte copiate e, più avanti, quelle disegnate per il robot). Le tabelle `sym-lib-table` e `fp-lib-table` di ogni progetto puntano solo lì.

## Schede

| Cartella | Scheda | Stato |
|---|---|---|
| `prova/` | scheda di prova del metodo, caso di riferimento della CI | schema e PCB |
| `basetta/` | PCB-B, basetta dell'ESP32 (piano 4.1), **quattro strati** | schema (R1, D-079, ritocchi di F4 in D-083); piazzamento e sbroglio da script con DRC a zero (D-083); dima e stampe per R2; serigrafia da fare |
| `carapace/` | PCB-C, scheda del carapace (piano 4.2) | schema (R1, D-079), piazzamento e sbroglio da script con DRC a zero (D-082); dima, render e stampa 1:1 per R2 (F5) |
| `partitori/` | PCB-P, scheda dei partitori, **quattro strati** (sullo stesso pannello della basetta) | schema, piazzamento e sbroglio da script con DRC a zero (D-084), sagoma di prova fino alla 2.1.9 del CAD; dima e stampe |

## Prova del metodo (F1, 18 ottobre 2026)

Scheda di prova in `prova/`: buffer SN74AHCT125N a cinque unità (quattro porte e l'alimentazione) in DIP-14, ponticello a tre piazzole, resistenza a reoforo, condensatore 0805, strip 1 × 4, punto di prova, due PWR_FLAG.

| Passo del piano (5.2) | Esito |
|---|---|
| 1. schema da script, con simboli, etichette e fili, che passa l'ERC | **riuscito**: ERC a zero rilievi. La netlist di KiCad è uguale alle reti dello script. Caso di controllo: un pin scollegato e un'alimentazione senza PWR_FLAG danno 3 errori (`pin_not_connected`, `pin_not_driven`, `power_pin_not_driven`) |
| 2. PCB con le impronte e le reti assegnate alle piazzole da `pcbnew` | **riuscito**: impronte dalla libreria del progetto, percorso del simbolo, reti della netlist |
| 3. piste e riempimento di massa da script | **riuscito**: piste su F.Cu, due vie, riempimento su B.Cu riempito da `ZONE_FILLER` |
| 4. DRC con `--schematic-parity` a zero, e un caso di controllo che fallisce | **riuscito**: zero violazioni, zero connessioni mancanti, zero rilievi di parità. Controlli: una pista tolta dà 2 `unconnected_items`; una piazzola con la rete sbagliata dà corto, ponte di maschera, connessione mancante e `net_conflict` di parità |

**Esito: schema, piazzamento e sbroglio li fa l'agente da script**, e l'utente rivede nell'editor e nei render. La colonna "Chi" del piano resta com'è.

Cose imparate nella prova, che il codice già tiene in conto:
- `board.GetLayerID('F.SilkS')` dà UNDEFINED (vuole i nomi utente): si usano le costanti `pcbnew.F_SilkS`;
- `pcbnew.NewBoard(percorso)` apre il `.kicad_pro` accanto e lo completa con i valori predefiniti, senza togliere quelli scritti prima;
- le istanze dei simboli non devono portare `ki_keywords` e `ki_fp_filters`: KiCad le tiene solo nella libreria, e copiate nelle impronte danno avvisi di parità e scritte sulla serigrafia;
- ogni unità di un simbolo a più unità elenca tutti i pin del simbolo, altrimenti KiCad dà ai mancanti un uuid a caso;
- con `--exit-code-violations` il DRC esce con 5 solo per gli errori: i rilievi di parità sono avvisi. Per questo `controlla.py` legge il JSON.

## Sbroglio

Lo sbroglio della basetta si rifà con `$KP pcb/basetta/sbroglia.py` (circa 3 minuti) e scrive `basetta/piste.json`, che `genera_pcb.py` rimette nel PCB: la CI non ha bisogno di strumenti esterni. Passi:
1. `script/sbroglio.py`, instradatore a griglia del progetto (Python puro, A*, 0,1 mm, tratti a 45°), per le reti con le regole a coppie del `.kicad_dru`: potenza, VBAT a 1 mm, segnali a 5 V a 1 mm dai pin dell'ESP32;
2. `script/freerouting.py` con **Freerouting 2.5.0** (`~/tools/freerouting/freerouting-2.5.0.jar`, da github.com/freerouting/freerouting) e **OpenJDK di Homebrew** (`brew install openjdk`, Java 25 o successivo) per le altre reti. Telemetria spenta da riga di comando e in `~/Library/Application Support/freerouting/freerouting.json`; niente piste ristrette ai pin. La versione nativa `freerouting-cli` si blocca allo sbroglio (errore di serializzazione di GraalVM): non si usa;
3. di nuovo `sbroglio.py`, sui quattro strati, per le reti che Freerouting lascia aperte o con un errore.

Dopo `ImportSpecctraSES` gli oggetti di `pcbnew` di quel processo non si leggono più dal Python: la lettura e la rifinitura girano in un processo nuovo. Le classi di rete (larghezze, VBAT a 1 mm) stanno nel `.kicad_pro`, scritte da `genera_pcb.py`, perché Freerouting non legge il `.kicad_dru`.

## Dime (F5)

Prima di ordinare, ogni scheda si prova con una **dima stampata 1:1**: la sola scheda, senza rame, con la sagoma e i fori del PCB, nella terna del robot (`cad/stl/attrezzi/Dima_PCB_<Scheda>.stl`, da `script/dima.py`, Python di KiCad). I fori dei pin sono allargati di 0,4 mm (`gio_stampa` per lato), quelli Ø2,4 delle viti no: se la M2 passa e centra l'inserto nella dima, passa anche nella scheda. La dima è spessa 1,5 (la scheda 1,6). Con la dima ci sono i render e la stampa 1:1 (`script/stampe.py`, in `docs/immagini/pcb/`): la stampa va fatta al 100 % e controllata col righello sulla sagoma (PCB-C: 21,5 mm da coda a testa, 48 fra le punte delle ali).

**PCB-C** (`Dima_PCB_Carapace.stl`), cosa provare e cosa riportare:
1. **J2 Würth** infilata dal lato dei componenti (sotto, come nel robot): i 16 pin entrano senza forzare e la scatola arriva a filo del bordo di coda.
2. **Polo 1 di J2 (S-26)**: si innesta la spina IDC del cavo piatto (la chiave la fa entrare in un verso solo). Il polo 1 dell'impronta è il foro quadrato, sulla fila lontana dalla scatola, verso +Y. Col multimetro in continuità fra il filo rosso del cavo (polo 1) e i pin che escono dalla dima: il filo rosso deve dare continuità con il pin del foro quadrato. Se la dà con il pin accanto, sulla fila vicina alla scatola, l'impronta va rovesciata prima dell'ordine.
3. **CE1** (470 µF) in piedi sotto l'ala +Y, con il + sulla piazzola quadrata, e i due fili del pulsante nelle piazzole dell'ala −Y.
4. **Nel carapace** (quando è stampato, con gli inserti M2): quattro M2 × 4 sugli inserti; le viti centrano gli inserti, le ali non toccano, J2 sta nella sua sede, CE1 non tocca il dorso.

**PCB-B** (`Dima_PCB_Basetta.stl`):
1. **strip femmina** dell'ESP32 a 25,4 (P-005), con i contatti dei pin 27, 28, 30 e 40 sfilati (varchi, D-083); l'ESP32 RE1.3 innestato: si misurano i 8,5 mm e si guarda che U2, U3, il fusibile, D1 e le sei resistenze in piedi passino sotto il suo retro;
2. **D24V22F5** appoggiato sulla dima con i pin senza il distanziale: i componenti di sotto entrano nell'apertura e il modulo sta piano;
3. **U3** (DIP-14), PTC1 sdraiato, D1, le resistenze in piedi (alte non più di 7,5 dalla scheda) e R11, R12;
4. sul vassoio: quattro M2 × 5 nelle colonne, la dima appoggia piana e le code dei reofori non toccano.

Esito: una riga per prova (va / non va, con la misura se non va) in fondo a `docs/piano-pcb.md`.

## Comandi

```
KP=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
python3 pcb/script/librerie.py
python3 pcb/prova/genera_schema.py
$KP pcb/prova/genera_pcb.py
python3 pcb/script/controlla.py pcb/prova
$KP pcb/basetta/sbroglia.py
$KP pcb/script/dima.py carapace
python3 pcb/script/stampe.py carapace
python3 pcb/script/regole.py --controlla
.venv/bin/python -m pytest tests/test_pcb.py -q
```

Nella CI il job `pcb` installa KiCad dal PPA (`ppa:kicad/kicad-10.0-releases`, senza le librerie), controlla che la versione sia quella scritta qui sopra e fa regole, ERC e DRC di ogni progetto, contorni e `tests/test_pcb.py`. I rapporti JSON restano fra gli artefatti (`pcb-rapporti`).
