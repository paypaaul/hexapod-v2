# Formato dei passi della guida (D-075)

Una sezione è un file `guida/passi/NN-nome.yaml`. I pezzi, le viti e le immagini vengono dal CAD (`guida/dati/`) e dal catalogo (`guida/catalogo/`). Nel file si scrive solo l'ordine, l'inquadratura e il testo. Le quantità non si scrivono a mano: si calcolano.

## Sezione

```yaml
sezione:
  id: zampa                 # unico, minuscolo; nomi di file e immagini
  numero: 6
  titolo: La zampa
  colore: "#ff6a13"         # fascia della sezione
  terna: zampa              # zampa: la zampa come costruita (Coxa nell'origine); robot: il robot intero
  istanza: AS               # solo terna robot: la zampa di riferimento (AD AS MD MS PD PS)
  ripeti: 6                 # la sezione si rifà N volte (zampa); quantità mostrate per una volta e in totale
  unita: una zampa          # "pezzi per una zampa"
  ripeti_testo: "6× — una zampa alla volta"
  presenti_iniziali: []     # pezzi già montati all'inizio (glob)
  obiettivo: ...            # testo dell'apertura
  prima: [..., ...]         # cosa deve essere già fatto (con il numero di sezione)
  tempo: circa 2 ore la prima volta [S]
  stato_elettrico: T-plug staccato
  note: ...
  attrezzi: [calibro]       # in più rispetto a quelli dei passi
  controllo: [..., ...]     # punto di controllo a fine sezione: frasi da spuntare
  scheda: [..., ...]        # solo con ripeti: righe della tabella a spunta per le sei zampe
  vista_finale: zampa_A
passi: [...]
rinviati: [...]             # passi gia' scritti che vanno piu' avanti (stesso formato); la pipeline li ignora
```

## Passo

```yaml
- id: "6.01"                # sezione.passo, a due cifre
  titolo: Cuscinetto nella culla della tibia      # breve, senza verbo
  formato: grande           # grande (una pagina) o mezzo (due passi mezzo consecutivi stanno in una pagina)
  nuovi: [zampa/Cuscinetto_ginocchio]             # pezzi montati in questo passo (glob di chiavi del manifest)
  assiemi:                  # sottoassiemi già fatti che entrano interi (non contano come pezzi montati)
    - {chiavi: "zampa/*@AS", esclusi: ["zampa/Coxa_Ponte@AS"], nome: Zampa montata (sezione 6)}
  giunzioni: [alette_ginocchio_coda]              # nomi di guida/catalogo/giunzioni.yaml; oppure {id: ..., esploso: 12}
  # viti messe (accostate) in un passo prima e strette ora: {id: alette_ginocchio_coda, stringi: true}; si disegnano
  # al loro posto e non si contano di nuovo
  inserti: [{chiave: zampa/Tibia, lav: "ins_*"}]  # inserti a caldo da mettere in questo passo (fori del CAD)
  esploso: {asse: [0, -1, 0], distanza: 30}       # spostamento dei pezzi nuovi, nella terna della sezione (mm)
  # oppure per pezzo: esploso: {pezzi: {"zampa/Perno_*": [0, 0, -25], "zampa/Femore_B": [0, -40, 0]}}
  vista: zampa_B            # nome di guida/catalogo/viste.yaml, oppure {direzione: [x, y, z], su: [0, 0, 1]}
  mostra: [...]             # solo questi pezzi già montati (più i nuovi); di solito non serve
  nascondi: [...]           # pezzi montati da non disegnare (coprono la vista)
  evidenzia: [{chiave: zampa/Tibia, lav: sede_luce}]   # facce di lavorazioni in giallo (guida/catalogo/zone.yaml):
                            # dove va quello che il CAD non ha (striscia, fili); si esportano con esporta_guida.py zone
  volte: 2                  # riquadro "2×" nell'immagine: il passo si fa due volte uguale (es. i due lati)
  testo:                    # un'azione per riga, imperativo, verbo all'inizio (guida/stile.md)
    - Premi il cuscinetto nella sede del lato B fino in battuta.
  avvisi:
    - {tipo: attenzione, testo: ...}              # pericolo o danno
    - {tipo: importante, testo: ...}              # errore facile che costa smontare
    - {tipo: nota, testo: ...}
    - {tipo: opzionale, x: X31, quando: solo_ora, testo: ...}   # quando: solo_ora | meglio_ora | anche_dopo
    - {tipo: prova, testo: ...}                   # prova da fare prima di andare avanti
  attrezzi: [calibro]       # chiavi di guida/catalogo/attrezzi.yaml (quelli delle viti e degli inserti si aggiungono da soli)
  extra: [{nome: "fascetta 2,5 × 100", qta: 2, bom: D11}]   # cose che non sono nel CAD
  fonti: [D-049, docs/progetto-meccanico.md "Zampa"]        # da dove viene il passo; i D-0xx devono esistere
```

## Chiavi dei pezzi

- Le chiavi stanno in `guida/dati/manifest.json` (`occorrenze[].chiave`):
  - zampa: `zampa/Coxa`, `zampa/Servo_femore`, `zampa/Squadretta_coxa`, …;
  - corpo: `corpo/Corpo_Base`, `corpo/Servo_Coxa_AS`, ….
- Nelle sezioni con `terna: robot` i pezzi della zampa si citano con l'istanza: `zampa/Coxa@AS`.
- Le alternative virtuali (`corpo/IMU_Pololu`, `corpo/Microfono_Adafruit_*`) non si montano; si citano negli avvisi.
- I nomi da usare nel testo stanno in `guida/catalogo/pezzi.yaml`.

## Come si prova

```
.venv/bin/python -m guida.costruisci controlla          # deve dire ok ovunque
.venv/bin/python -m guida.costruisci rendi -s zampa     # immagini in build/guida/img/zampa/ (pochi secondi a passo)
.venv/bin/python -m guida.costruisci pdf -s zampa       # build/guida/guida.pdf; righe "immagine:" e "deborda:" da correggere
.venv/bin/python -c "from guida.lib import impagina as I; I.anteprime('build/guida/sito/index.html', 'build/guida/anteprima')"
```

- "esploso di scorcio": l'asse dell'esploso è quasi lungo la vista. Cambia la vista o l'asse.
- "poco visibile": un pezzo nuovo o una vite è coperto. Cambia la vista, oppure usa `nascondi` per i pezzi davanti.
- "tagliata": non dovrebbe succedere, l'inquadratura è automatica. Segnalalo.
- "deborda": il testo non sta nella colonna. Accorcia il testo o usa `formato: grande`.

## Problemi

Quello che non torna (fonti in disaccordo, un pezzo che non entra, un dato mancante) non si risolve nel passo: si scrive in `guida/problemi/<id sezione>.yaml` e la guida dice la cosa più prudente, con un avviso.

```yaml
- titolo: Vite d'aletta del servo del femore coperta da Femore_A
  gravita: bloccante        # bloccante | importante | minore
  dove: "6.12"
  cosa: ...                 # il fatto, con i numeri
  prove: [...]              # fonti, misure, file:riga, immagini
  opzioni: [...]
  consiglio: ...
```
