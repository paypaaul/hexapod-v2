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
| `basetta/` | PCB-B, basetta dell'ESP32 (piano 4.1) | schema approvato all'arresto R1 (D-079) |
| `carapace/` | PCB-C, scheda del carapace (piano 4.2) | schema approvato all'arresto R1 (D-079) |
| `partitori/` | PCB-P | dopo DU-5 (F2) |

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

## Comandi

```
KP=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
python3 pcb/script/librerie.py
python3 pcb/prova/genera_schema.py
$KP pcb/prova/genera_pcb.py
python3 pcb/script/controlla.py pcb/prova
python3 pcb/script/regole.py --controlla
.venv/bin/python -m pytest tests/test_pcb.py -q
```

Nella CI il job `pcb` installa KiCad dal PPA (`ppa:kicad/kicad-10.0-releases`, senza le librerie), controlla che la versione sia quella scritta qui sopra e fa regole, ERC e DRC di ogni progetto, contorni e `tests/test_pcb.py`. I rapporti JSON restano fra gli artefatti (`pcb-rapporti`).
