# Stile dei testi della guida (D-075)

La guida si legge con le mani occupate: poche parole, sempre le stesse, una cosa alla volta. Prima l'immagine, il testo dice solo quello che l'immagine non può dire.

## Frasi

- Imperativo con il tu, verbo all'inizio: "Premi il cuscinetto nella sede".
- Un'azione per riga, da tre a sei righe per passo. Se ne servono di più, il passo va diviso.
- Niente "ora", "quindi", "a questo punto": l'ordine lo danno i numeri.
- Niente spiegazioni nel testo. Il perché, quando serve, va in un avviso NOTA con il riferimento (D-0xx).
- Italiano: "vite", "foro", "sede", non "screw" o "slot". Sigle solo quelle del BOM e della scheda (SSC-32, ESP32, T-plug).

## Verbi con un significato fisso

| Verbo | Significa |
|---|---|
| Accosta | avvita finché la testa tocca, senza stringere |
| Stringi | stringi a fondo, senza forzare la plastica |
| Infila | fai scorrere un pezzo in una sede, senza forza |
| Premi | forzamento: con il pollice o con una morsa a ganasce morbide |
| Posa | appoggia nella posizione finale, senza fissare |
| Cala | fai scendere dall'alto in una sede o in una culla |
| Ruota | gira fino alla posizione indicata (angolo o riferimento) |
| Collega | innesta un connettore (verso indicato) |
| Salda | saldatura a stagno |
| Controlla | verifica senza attrezzi; se non va, fermati |
| Misura e annota | misura con l'attrezzo e scrivi il valore nel registro delle misure (appendice) |

## Numeri e nomi

- Virgola decimale, spazio prima dell'unità: "0,5 mm", "5,2 V", "30 A".
- Viti come nel BOM: "M3 × 8", "M2 × 5 svasata".
- Nomi dei pezzi da `guida/catalogo/pezzi.yaml`. Lati della zampa A e B come nel CAD (il lato di Femore_A e quello di Femore_B): la sezione 0 li mostra con un disegno. Zampe AS, AD, MS, MD, PS, PD.
- I dati si marcano dopo il numero: [V] verificato su fonte primaria o nel CAD, [S] stimato, [C] da confermare (di solito con un provino o con il pezzo vero).

## Avvisi

- ATTENZIONE: pericolo per le persone o danno a un pezzo (batteria, saldatore, servo sotto carico, polarità).
- IMPORTANTE: errore facile che costringe a smontare.
- NOTA: il perché, un trucco, un riferimento.
- OPZIONALE Xn — solo ora / anche dopo: una predisposizione; "solo ora" se dopo non si può più.
- PROVA: una prova da fare prima di andare avanti, con il risultato atteso.
