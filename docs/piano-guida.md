# Piano della guida di montaggio illustrata (stile LEGO), approvato l'11 ottobre 2026

## Contesto

L'utente vuole una guida dettagliata, passo passo, per montare tutto il robot nell'ordine giusto:
- immagini CAD pezzo per pezzo;
- sezioni con l'elenco completo dei componenti e degli attrezzi;
- ispirata alle istruzioni LEGO;
- in PDF.

Con le predisposizioni e le versioni 2.1.x "ci si perde", e scrivere la guida serve anche a **riguardare tutto il progetto**. I problemi di montaggio che emergono si raccolgono e si portano all'utente; non si correggono in silenzio.

Cosa c'è oggi (esplorazione dell'11 ottobre 2026):
- **Procedura di montaggio**: nessuna scritta in `docs/`, solo vincoli sparsi. Ci sono due sequenze nella ricerca (`docs/ricerca/zampa-architetture.json`, `corpo-disposizioni.json`), in parte superate da D-048, D-049 e D-051.
- **Viti**: nel modello non ci sono, ci sono solo i fori.
- **Incoerenze già trovate** (8):
  - viti della squadretta di coxa: M3 × 6 con rondella o M3 × 5 senza;
  - viti della SSC-32: pilota M2,5 o inserti M2;
  - distanziali del vassoio: 5 o 10;
  - inserti M3 del corpo: 28 o 30;
  - pulsante: Dupont o IDC;
  - vassoio: PETG o PLA;
  - perno della coxa;
  - viti lato coda del servo di coxa: la procedura sta solo nella ricerca.
- **Candidati problema**:
  - vite d'aletta del servo del femore sotto Femore_A;
  - calettamento a α +20° e γ 100° senza riferimento;
  - mancano i provini di inserti, piedino e giunto;
  - mancano gli schemi della basetta e della scheda del carapace;
  - slitta destra: specchiata o la stessa.

## Decisioni dell'utente (11 ottobre 2026)

- **Parti ripetute descritte una volta sola**:
  - **una zampa pilota completa** segnata "×6"; per le altre cinque una scheda a spunta per zampa (servo usati, calettamento, viti strette, prolunga sulle zampe d'angolo);
  - nel corpo un solo passo "×N" (6 servo di coxa, 2 slitte), con le differenze fra destra e sinistra segnate.
- **Strumenti**: liberi, si installa quello che serve. Scelti:
  - **Blender** senza interfaccia per le immagini;
  - **Chrome** per il PDF.
  - "Blender dopo la fase 6" resta valido solo per gli altri usi. Si annota in D-075 e in `CLAUDE.md`.
- **Schemi dell'elettronica**: la disposizione della basetta e della scheda del carapace sulle millefori si **progetta** durante la guida e passa dall'utente come i problemi.
- **PDF**: allegato alla release del tag su GitHub (`gh release upload`). In git restano i sorgenti.
- **Formato**: A4 orizzontale.
- **Agenti**: ammessi, workflow compresi, con modello ed effort scelti per compito.

## Architettura

```
Fusion (sola lettura)  cad/script/esporta_guida.py ─► guida/dati/manifest.json + fori.json (git) ─► build/guida/cad/mesh/*.ply
repo                   guida/costruisci.py  controlla | scene | rendi | verifica | impagina | pdf | tutto
Blender -b             guida/blender/rendi.py (lotto JSON → PNG + JSON frecce)
Chrome                 HTML di stampa → PDF (Playwright con channel="chrome", ripiego --print-to-pdf)
```

- **`cad/script/esporta_guida.py`**: script nuovo, solo lettura, a lotti con un budget di 25 s per chiamata e stato salvato su disco.
  - **`manifest`**: occorrenze con chiavi stabili.
    - Corpo: chiavi di `assieme.pose_corpo`, trovate con `_istanze_corpo`.
    - Zampa: `Servo_femore`, `Squadretta_coxa` e simili, dalla posizione su x (0, `zam_Lc`, `zam_Lc+zam_Lf`) e da `_gruppo`.
    - Trasformate: quelle native della zampa più le sei terne delle istanze.
    - Colori letti dai corpi.
    - Alternative di `assieme.alternative()` segnate come virtuali.
  - **`mesh`**: un PLY per componente, ridotto ai componenti diversi (`TriangleMeshCalculator`, tolleranza 0,03 mm). Si rifà solo se il `revisionId` è cambiato.
  - **`fori`**: cilindri concavi con
    - il nome della lavorazione (da `ExtrudeFeature.sideFaces`, e dagli specchi tramite `patternElements`);
    - asse, profondità ed estremi (fondo, svasato, aperto).

    La classificazione si fa fuori da Fusion, con le regole di `guida/catalogo/fori.yaml`. Il diametro da solo non basta: 3,4 mm vale sia per il passante M3 sia per l'inserto M2, 4,2 mm sia per l'inserto M3 sia per l'aletta del servo.
  - **`controllo`**: verifica che il proxy coincida con `T_istanza · T_locale`.
- **`guida/lib/`**, Python puro testabile:
  - `manifest`;
  - `fori` (pile coassiali, piazzamento della vite: testa sul passante esterno, punta verso l'inserto o il pilota);
  - `scena` (stato del montaggio dopo ogni passo, esploso lungo l'asse);
  - `elenchi`: pezzi per passo, per sezione e generali; si calcolano, non si scrivono a mano;
  - `controlli`, `immagini`, `impagina`, `righello`, `pdf`.
- **Blender** (`guida/blender/rendi.py`, `viti_bmesh.py`):
  - **Stile**: EEVEE + Freestyle con colori piatti, `view_transform` Standard e sfondo trasparente.
    - Pezzi nuovi con il contorno spesso; pezzi già montati attenuati con il contorno grigio.
    - PETG-CF schiarito, perché nero su nero non si legge.
  - **Viti procedurali**: ISO 4762, svasate, a croce, più rondelle, inserti e distanziali. Il filetto si vede solo nei disegni 1:1.
  - **Camere**: ortografiche, con preset da `viste.py`, inquadratura automatica e scala fissa per sezione; riquadri di dettaglio.
  - **Frecce** in SVG sopra l'immagine, dai punti proiettati.
  - **Velocità**: 3 processi in parallelo con cache per hash; circa 5–7 minuti da zero, meno di 1 minuto dopo una modifica.
  - **Ripieghi**: Cycles + Freestyle, oppure Workbench + Line Art.
- **Impaginazione** (`guida/modelli/*.html.j2`, `guida/css/guida.css`, font OFL):
  - pagine fisse A4 orizzontali, con numeri e indice assegnati dal generatore;
  - fascia del colore della sezione;
  - riquadro "pezzi necessari" con miniature e viti **1:1** in SVG, più un righello e una barra di controllo da 100 mm;
  - riquadri ATTENZIONE, IMPORTANTE, NOTA, OPZIONALE Xn ("solo ora" o "anche dopo") e PROVA;
  - pagina "punto di controllo" a fine sezione;
  - uscite: `index.html` navigabile e PDF con i segnalibri;
  - immagini quantizzate e senza perdite, 15–30 MB in tutto.
- **Dipendenze**: nella `.venv` vanno `Jinja2`, `playwright` (usa il Chrome già installato) ed eventualmente `pikepdf`, elencate in `guida/requirements.txt`. Gli output finiscono in `build/guida/`, già ignorata da git.
- **Controlli**: `guida/lib/controlli.py` più `tests/test_guida.py`, in Python puro, così girano in CI.

| Controllo | Cosa garantisce |
|---|---|
| montaggio unico | ogni parte montabile entra una volta sola (zampa × 6) |
| chiavi esistenti | nessun passo cita pezzi, viti o attrezzi che non esistono |
| viti BOM | per giunzione e per tipo, i totali coincidono con la riga "Totale viti" di `docs/BOM.md`: M3 × 5 12, × 6 52, × 8 106, × 10 18, × 16 2; M2 × 5 16, svasate 12; rondelle 48; inserti M3 94 e M2 28 |
| fori coperti | ogni foro riceve qualcosa, oppure è dichiarato libero con il motivo |
| ordine | ogni giunzione usa pezzi già montati |
| lunghezze | presa contro profondità dell'inserto |
| teste A (caso di controllo) | le viti piazzate su Femore_A coincidono con i 12 `testa_NN` di `Ingombro_Teste_A` |
| decisioni | ogni D-0xx citato esiste |
| versione | solo un avviso |

  In più, come avvisi, il controllo del percorso di montaggio con `BVHTree.overlap` in Blender.

## Struttura della guida

Circa 220 passi, 140 pagine e 200 immagini. Ogni sezione si apre con un "sacchetto": obiettivo, prerequisiti, tempo, pezzi stampati e comprati, viti 1:1, consumabili, attrezzi, opzionali, stato elettrico.

| # | Sezione | Contenuto |
|---|---|---|
| 0 | Prima di cominciare | come si legge; sicurezza (LiPo, saldatore, servo); scheda delle opzioni X; nomi delle zampe e lati A/B; terne; inventario; foglio delle viti 1:1 |
| 1 | Provini | culla (Tibia), giunto con la squadretta di prova, tasche della lama A, luce, inserti. I valori trovati tornano nel CAD prima di stampare il resto |
| 2 | Stampa e controllo dei pezzi | orientamento, supporti, carapace a due colori, controlli col calibro, S/D marcati |
| 3 | Inserti a caldo | generata da `fori.json`: una figura per pezzo con gli inserti; avvertenza: mai inserti nei fori pilota |
| 4 | Banco dell'elettronica (B0–B1) | SSC-32 (ponticelli, micro-USB *prima*, barre); **basetta e scheda del carapace secondo gli schemi progettati**; regolatori sulle slitte; ramo logica; ponticelli degli INA260 |
| 5 | Servo | prova, numero, metà corsa (B2) |
| 6 | Zampa pilota (×6) | tibia (opzionali FSR e luci "solo ora", guscio, piedino) → coxa → Femore_B e perni → calettamento → Femore_A con le rondelle di registro → alette strette per ultime → cavi → lama A. La lama B dopo la taratura |
| 7 | Corpo | cuscinetti, chiglia, 6 servo di coxa (×6), sedi: Wago, F1, 2813, prese, spie |
| 8 | Elettronica nel corpo e cablaggio (B3) | slitte, SSC-32, IMU su piastrina e ADC **prima** del vassoio, vassoio **prima** della basetta, camera, ToF; potenza, logica, bus |
| 9 | Zampa pilota sul corpo | vite centrale della squadretta, viti-spina, coxa, ponte, viti lato coda; prova B5; misura dei fili |
| 10 | Le altre cinque zampe | una pagina di lotti e la scheda a spunta, con rimando alle sezioni 6 e 9 |
| 11 | Batteria e sportello | |
| 12 | Prima accensione e taratura | cavalletto, F1 da 15 A, B4, dime 1 e 2 con la lama B tolta, poi lame B e F1 da 30 A |
| 13 | Carapace | pulsante e fondo dell'anello, lobi, scheda del carapace, ampli e altoparlante, microfoni con lunette, ToF posteriore, cicalino; prova al banco; montaggio |
| 14 | Collaudo (B6) | |
| 15 | Smontaggio e manutenzione | |
| App. | | viteria, viti 1:1, canali della SSC-32, registro delle misure, opzionali, glossario, problemi noti, schemi elettrici |

**Stile dei testi** (`guida/stile.md`):
- imperativo con il tu, un'azione per riga;
- verbi con un significato fisso: Accosta e Stringi, Infila e Premi, Posa, Cala, Controlla, Misura e annota;
- dati marcati V, S o C;
- glifo con la freccia "testa" in ogni immagine;
- glossario in `guida/glossario.yaml`.

## Lavoro con gli agenti

Fasi e punti di arresto. I modelli seguono la regola del progetto: Sonnet per ricerche e report, verificatori con effort alto. Opus solo dove contano l'ordine nello spazio e la sicurezza elettrica. Ogni workflow sta sotto i 10 agenti.

| Fase | Chi | Modello ed effort | Cosa produce |
|---|---|---|---|
| F0 prova di fattibilità | sessione principale | — | coxa e servo in Blender con lo stile; 3 pagine PDF; righello misurato. Si sceglie il motore |
| F1 infrastruttura | sessione principale | — | `esporta_guida.py`, `guida/lib`, schema YAML e catalogo (`viteria`, `giunzioni` dalla tabella del BOM, `fori`, `pezzi`, `attrezzi`, `viste`, `stile`), controlli e test, Blender, impaginazione. I controlli sul BOM funzionano già prima di qualsiasi immagine |
| F2 pilota (zampa, tibia, circa 12 passi) | 1 estrattore + 2 verificatori (ordine; coerenza) | Opus high; Opus high e Sonnet high | formato e prompt fissati, 4–6 pagine vere. **ARRESTO 1**: l'utente vede le pagine campione e i primi problemi |
| F3 estrazione (workflow) | 9 estrattori, uno per gruppo di sezioni | Sonnet high ×7, Opus high ×2 (zampa; zampa sul corpo) | bozze YAML con la fonte per ogni passo e un file dei problemi per sezione. Non scelgono fra fonti in disaccordo: le segnalano |
| F3b schemi elettronici (workflow piccolo) | 1 progettista + 1 verificatore elettrico | Opus high ×2 | disposizione di basetta (56 × 35) e scheda del carapace su griglia da 2,54 in SVG, dalle piedinature di `cablaggio.md` e `piano-elettronica-software.md` |
| F4 verifica avversaria (workflow) | V1 ordine fattibile; V2 accessi; V3 conteggi (script + agente); V4a/b coerenza meccanica e elettronica; V5 elettrica e sicurezza | V1 Opus xhigh; V2 Opus high; V3 Sonnet medium; V4 Sonnet high ×2; V5 Opus high | rilievi con prova e gravità. Caso di controllo: le 8 incongruenze note non sono nei prompt e devono uscire |
| F5 sintesi e registro | sessione principale | — | `guida/problemi.md` (P-001…), presentato all'utente a gruppi, prima i bloccanti, con opzioni e consiglio. **ARRESTO 2**: l'utente decide |
| F6 versione 2.1.7 | sessione principale | — | correzioni decise (CAD e documenti) come versione 2.1.7: piano, D-075 e successive raggruppate per tema, procedura solita. **Le immagini si fanno solo sulla 2.1.7** |
| F7 immagini e impaginazione | sessione principale + controlli immagine–testo | Sonnet medium ×3 | foglio di miniature campione. **ARRESTO 3**, poi tutte le immagini e il PDF |
| F8 revisione finale (workflow) | principiante letterale; maker scettico; simulatore dello stato (inventario passo per passo) | Sonnet high; Opus high; Opus xhigh | rilievi corretti. **ARRESTO 4**: l'utente approva |

Tempo stimato: circa 10–13 giorni di lavoro in più sessioni, fra pipeline (5–7) e contenuti e verifiche (4–6). Una prima zampa in PDF arriva dopo circa 4 giorni.

## Regole del progetto da rispettare

- **Prima di partire**:
  - piano della guida in `docs/piano-guida.md`;
  - puntatore in `CLAUDE.md`;
  - D-075: Blender per la guida, PDF allegato al tag, schemi delle schede da progettare.
- **Durante**:
  - commit e push su `main` a ogni gruppo di modifiche;
  - CI (`ci`, `sim`) verde, con `tests/test_guida.py`.
- **Fusion**: solo lettura per l'esportazione; gli eventuali cambi del modello stanno solo nella 2.1.7, con la procedura di `cad/CLAUDE.md`.
- **`cad/CLAUDE.md`**, "A valle di ogni modifica": aggiungere `esporta_guida.py` + `costruisci.py controlla`.
- **Mappa di `CLAUDE.md`**: aggiungere `guida/`.
- **Chiusura**:
  - tag `guida-2.1.7`;
  - `gh release create guida-2.1.7` con il PDF allegato;
  - riepilogo all'utente diviso in verificato / assunzione / aperto.

## Verifica

- `guida/costruisci.py controlla` e `pytest tests/test_guida.py`:
  - montaggio unico;
  - viti e inserti contro il BOM;
  - fori coperti, ordine, lunghezze;
  - caso di controllo `teste_a`;
  - decisioni esistenti.
- **Immagini** (`costruisci.py verifica`): non vuote, non tagliate, pezzi nuovi visibili (passata Workbench con un colore per oggetto), frecce dentro l'immagine; foglio dei provini da guardare.
- **PDF**:
  - nessuna pagina che deborda (misurata con Playwright);
  - segnalibri presenti;
  - righello 1:1 misurato su una stampa al 100 %;
  - peso sotto i 30 MB.
- **Revisione F8** dei tre lettori: con rilievi bloccanti a zero il PDF va alla release.
- **Dopo la zampa costruita davvero**: guida 1.1 con le misure reali, le foto ed eventuali correzioni.

## Stato e ripresa (12 ottobre 2026, pausa chiesta dall'utente per l'uso settimanale)

**Fatto** (tutto su `main`, ultimo commit della guida `a910620`, CI verde):
- F0, F1: pipeline completa. Catalogo, controlli e test (33), Blender, impaginazione, PDF.
- F2: tibia pilota, approvata all'arresto 1. L'utente ha approvato anche le soluzioni dei problemi della tibia (campo `esito` in `guida/problemi/zampa.yaml`).
- F3: bozze di tutte le sezioni (0-15 e appendici), riconciliate (`guida/problemi/riconciliazione.yaml`).
- F3b: schemi della basetta e della scheda del carapace (`guida/schemi/`, generatori in `guida/schemi/sorgenti/`), verificati e corretti.
- F3c: passata di qualita' su tutte le sezioni (zone in giallo, pose della zampa, etichette, attrezzi), saldature tutte al banco.
- Risultato: 306 pagine, nessun avviso sulle immagini, nessun testo che deborda; `controlla` verde, salvo l'avviso noto della vite del guscio.
- Problemi: 207 in `guida/problemi/*.yaml`, di cui 9 bloccanti, 81 importanti, 117 minori. Alcuni hanno `domanda` per l'utente.

**Per ripartire**:
- `build/` non e' in git. Servono:
  - Fusion aperto sul design di lavoro;
  - `esporta_guida.py` con i passi `manifest`, `mesh`, `fori`, `zone`, `controllo` (sola lettura; `cad/CLAUDE.md`);
  - poi `.venv/bin/python -m guida.costruisci tutto -j 3`. Circa mezz'ora di render la prima volta, poi la cache.
- Dipendenze: `guida/requirements.txt` nella `.venv`, Blender 4.5 in `/Applications`, Chrome.

**Ordine cambiato il 15 ottobre 2026** (utente): prima la F5 con il registro unico dei problemi (`guida/problemi.md`,
fatto: 138 voci da 207 problemi) e l'**arresto 2**; poi le correzioni (2.1.7, documenti, testi); la verifica avversaria
(F4) si fa dopo, sulla guida corretta, insieme alla revisione finale (F8), cosi' non si rifa' due volte.
- L'uso pesa:
  - F3: circa 4,8 milioni di token di agenti;
  - F3b: 1,4 milioni;
  - F3c: 2,9 milioni.
- La F4 va dimensionata con l'utente prima di partire: meno agenti (per dimensione, non per sezione), Sonnet dove basta, Opus solo per ordine e accessi e per la sicurezza.
- Caso di controllo della F4: le 8 incongruenze note di "Contesto" non vanno nei prompt.

**15 ottobre 2026**: PDF completo da 98 a 25,4 MB. Le immagini si appiattiscono con gli ottetti a 64 colori (errore medio
1 su 255) e il PDF di Chrome si riscrive con pikepdf, con le immagini indicizzate esatte (`impagina.comprimi`).

**Difetti della pipeline ancora aperti** (dai rapporti degli agenti, da sistemare prima della F7):
- Le etichette su un punto non seguono l'esploso del pezzo e non evitano le altre etichette.
- Un extra con `qta` in un passo con `volte` si moltiplica due volte se l'autore ha gia' scritto il totale. Va deciso e scritto in `schema.md` che `qta` e' per una volta.
- `assiemi` entrano sempre con quantita' 1.
- L'apertura di una sezione con molti extra deborda: serve una seconda pagina del sacchetto.
- Il controllo delle immagini non vede le zone gialle coperte da altri pezzi; manca una vista in sezione o la trasparenza.
- I rimandi "N.xx" scritti a mano sono fragili: servono rimandi simbolici risolti dall'impaginatore.
- Passi con figura e tabella insieme: la colonna e' stretta.
- Gli attrezzi non seguono la posa della zampa (dima 2 sul femore).
- Le giunzioni M2 delle predisposizioni (ADC, INA260, scheda del carapace, ampli) non si possono disegnare finche' le schede nel CAD sono blocchi senza fori.
