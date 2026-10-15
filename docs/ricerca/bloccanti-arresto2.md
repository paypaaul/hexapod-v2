# Bloccanti dell'arresto 2 della guida: P-002, P-003, P-005

15 ottobre 2026. Risposte dell'utente all'arresto 2 (`guida/problemi.md`, bloccanti):
- P-003 (S-19) e P-005 (S-02): "risolvi in autonomia". Qui sotto la decisione, il perché e le quote. Diventano modifiche della 2.1.7 (`docs/piano-v2.1.0.md`, sezione "Versione 2.1.7").
- P-002 (S-01): "cosa suggerisci?". Qui sotto tre soluzioni con le misure e una raccomandazione; **la scelta resta all'utente**.

Quote in mm nella terna del robot (X avanti, Y a sinistra, z 0 sul piano dei femori). Stato dei dati come nel resto del progetto: V verificato, S stimato, C da confermare sul pezzo. Nessuna quota qui è stata verificata in Fusion: le verifiche sono nel piano della 2.1.7.

## P-003 (S-19): le teste M3 del vassoio sotto la basetta

### Il problema, con le quote di oggi

| Cosa | z | Fonte |
|---|---|---|
| faccia alta del tetto del tunnel | −9,4 | `corpo.py` `cor_tetto` |
| bugne del vassoio sul tetto (Ø7,4, inserto M3) | −9,4 … −4,0 | `corpo.py:417`, `cor_vas_z − 5` |
| distanziali B18, M3 maschio-femmina da 5 | −4,0 … 1,0 | `docs/BOM.md` B18 |
| piano del vassoio (PETG) | 1,0 … 2,6 | `cor_vas_z`, `cor_vas_sp` |
| teste delle M3 × 6 DIN 912 (Ø5,5 × 3) | 2,6 … 5,6 | `fori.json` `foro_pa/pb/aa/ab` a (30; ±12,5), (75; ±12,5) |
| basetta (lato saldature in basso) | 5,9 … 7,5 | D-053, `cor_bas_luce` 3,3 |

Restano 0,3 mm fra testa e basetta. Sotto le teste cadono T-2 (3V3), D-12 (GPIO21) e B-2 (GPIO14), che servono tutti; un giunto è alto 0,5-1.

### Soluzioni guardate

| | Soluzione | Aria sotto la basetta | Pezzi | Perché sì o no |
|---|---|---|---|---|
| a | M3 a testa bassa DIN 7984 (k 2,0) o ISO 7380 (k 1,65) | 1,3 / 1,65 | da comprare se il kit Temu non le ha (Q-20) | con giunti da 0,5-1 restano 0,3-1,1 mm e serve il Kapton: margine piccolo, dipende da un acquisto |
| b | spostare le viti fuori dalla basetta | — | nessuno | non si può: davanti la testa del carapace parte da x 82,6 (`car_testa_x0`) e il tetto finisce a x 81; dietro c'è la SSC-32 fino a x 22. Spostarle fra le file di pin (|y| ≤ 9) o lungo le file cade su fori già usati dallo schema (riga 13 del flat, U3 in riga 11) |
| c | alzare la basetta (`cor_bas_luce` da 3,3 a 5,3) | 2,3 | nessuno | alza l'ESP32 di 2 mm e toglie 2 mm sotto la scheda del carapace, cioè peggiora P-002 |
| d | M3 svasate ISO 10642 a filo, piano del vassoio ispessito | 2,9-3,3 | 4 M3 svasate da comprare | buona, ma è un acquisto, e per avere la svasatura intera il piano va ispessito verso il basso, dove IMU e ADC hanno 1,3 e 1,7 mm d'aria |
| **e** | **colonne stampate con la base al posto dei distanziali, inserti M2 in cima, viti M2 × 5 svasate a filo del vassoio** | **3,3** | **niente da comprare; B18 non serve più** | scelta |

### Decisione

**Soluzione e.** I quattro distanziali B18 e le quattro M3 × 6 si tolgono. Le bugne del vassoio sul tetto diventano colonne della base che arrivano fino al piano del vassoio, con un inserto M2 in cima; il vassoio si avvita con quattro **M2 × 5 a testa svasata** (D8b, già in casa: 50 pezzi, 16 usati) in svasature del piano, con la testa 0,1 sotto la faccia, come la piastrina della GY-6500 (`cor_pimu_svas`).

Perché:
- **tutta la luce torna libera**: sotto la basetta restano 3,3 mm come voleva D-053; con giunti da 0,5-1 restano 2,3-2,8 mm d'aria e non serve Kapton sulle teste;
- **lo schema non cambia**: le viti restano a (30; ±12,5) e (75; ±12,5), quindi zone vietate, fori e fili di `basetta*.svg` valgono così come sono. T-2, D-12 e B-2 si saldano normalmente (giunti piatti come gli altri);
- **niente acquisti**: viti e inserti M2 sono già in casa (D5, D8b); B18 (9,99 €, non ancora ordinato) esce dal BOM;
- **il carico è piccolo**: il vassoio porta ESP32, basetta e camera (decine di grammi); quattro M2 in inserti bastano, come per IMU, ADC e lame B;
- toglie anche l'incongruenza del caso di controllo "distanziali del vassoio: 5 o 10" (il commento di `corpo.py:415` dice 10, il BOM 5).

Quote proposte (da verificare in Fusion, piano della 2.1.7):

| Cosa | Oggi | 2.1.7 |
|---|---|---|
| colonna sul tetto | bugna Ø7,4 da −9,4 a −4,0 | bugna Ø7,4 da −9,4 a −4,0 (com'è) più **colonna Ø6,0** (`cor_vas_col_d`, oggi definito e non usato) da −4,0 a **1,0** |
| inserto in cima | M3 (`ins_m3_d` × `ins_m3_l`) a z −4,0 | **M2** (`ins_m2_d` 3,4 × `ins_m2_l` 4) dall'alto, a z 1,0 |
| foro del vassoio | Ø3,4 passante | Ø2,4 (`vite_m2_pass`) con **svasatura a 90°** profonda 0,9 (nuovo `cor_vas_svas`, valore di `cor_pimu_svas`) |
| testa della vite | z 2,6-5,6 | z 1,6-2,5 (Ø4,0, 0,1 sotto la faccia) |
| filetto nell'inserto | — | M2 × 5 svasata: dalla faccia a z 2,5 la punta arriva a −2,4, cioè 3,4 sotto la cima della colonna: inserto da 3 tutto impegnato, 0,6 di margine sul fondo del foro (4) |

Perché la colonna è Ø6,0 e non Ø7,4: fra z −4 e 1 c'erano i distanziali (esagono da 5,5, Ø6,35 sugli spigoli). Una colonna Ø6,0 non occupa più spazio di loro: il bordo dell'IMU (x 34,5) resta a 1,5 mm dalla colonna di (30; −12,5), come oggi dal distanziale. Parete intorno all'inserto: (6,0 − 3,4) / 2 = 1,3, due perimetri e mezzo con l'ugello da 0,4.

Stampa: la colonna è una prosecuzione verticale della bugna, stampata con la base (che si stampa con il tetto in orizzontale): niente sbalzi. Gli inserti si mettono dall'alto prima del vassoio, con il saldatore verticale.

Resta da provare:
- nel provino degli inserti (P-057) c'è già la riga degli M2 in PETG-CF: vale anche per queste colonne;
- l'altezza della colonna sostituisce un distanziale metallico: la planarità del vassoio dipende dalla stampa (quattro colonne della stessa base, stesso strato: differenze di pochi centesimi).

Le zone vietate dello schema restano come sono (proteggono anche le teste delle M2 e i bordi delle svasature); il testo di schemi.md 1.0, S-19 e il passo 4.04 vanno aggiornati (vedi il piano).

## P-005 (S-02): interasse delle file di pin dell'ESP32

### Fonti

| Fonte | Cosa dice | Stato |
|---|---|---|
| `docs/dimensioni-componenti.md`, scheda UICPAL (inserzione AliExpress 1005008519401021, letta l'8 ottobre) | PCB 62,6 × 28,3; passo 2,54, 2 × 20 pin; una quota "24,7" sul disegno letta come "probabile interasse" | V passo, C la lettura di 24,7 |
| Keyestudio MB0200 "S3 CAM" (stesso modulo ESP32-S3-WROOM-1-N16R8, OV3660, 2 file di pin), [docs.keyestudio.com](https://docs.keyestudio.com/projects/MB0200/en/latest/docs/MB0200%20S3%20CAM.html), letta il 15 ottobre 2026 | "The two rows of pin headers have a spacing of 25.4mm" (scheda 67,2 × 30,8) | V per quella scheda |
| Freenove ESP32-S3-WROOM CAM (la scheda di cui la UICPAL è un clone), repo GitHub `Freenove/Freenove_ESP32_S3_WROOM_Board` | nessuna quota meccanica nel testo; solo foto e piedinatura | — |
| Espressif DevKitC (riferimento dello schema) | file a 25,4 (1 pollice) | V |

### Ragionamento

- Una scheda con due file di pin a passo 2,54 pensata per la breadboard ha le file sulla stessa griglia da 2,54: 25,4 sono 10 passi, 22,86 sarebbero 9. **24,7 non è un multiplo del passo** (9,72 passi): nessuna scheda di questa famiglia ha le file fuori griglia.
- 24,7 torna invece come **distanza fra le facce interne dei pin** di due file a 25,4: 25,4 − 0,64 (pin quadro da 0,64) = 24,76. È la quota più probabile del disegno del venditore, letta male come interasse.
- La larghezza del PCB (28,3) è compatibile: con 25,4 restano 1,45 mm dal centro del pin al bordo, abbastanza per una piazzola da 1,7.
- Le schede uguali con lo stesso modulo e lo stesso schema a 2 × 20 (Keyestudio MB0200) dichiarano 25,4.

### Decisione

**Interasse 25,4 (10 passi), stato S** fino alla prova a secco. Lo schema della basetta (righe 2 e 12) resta valido.

Cosa cambia:
- CAD 2.1.7: `esp_file` da 24,7 a **25,4** in `rif_componenti.py` (riga 99), con il commento "S: 10 passi; 24,7 del disegno = facce interne dei pin". È usato solo da `Rif_ESP32` (`rif_componenti.py:461`): si spostano le file di pin del riferimento da |y| 12,35 a **12,7**. Nessun pezzo stampato dipende da `esp_file` (le colonnine della basetta sono a |y| 6,5-6,8, fra le file con 5,9 mm di margine).
- D-053: "file dei pin a |y| 12,35" diventa **12,7** (nuova decisione D-0xx della 2.1.7, D-053 resta com'è con il rimando).
- `docs/dimensioni-componenti.md`: la riga della quota "24,7" va riscritta (interasse 25,4 S, 24,7 = facce interne) e il PCB resta C.
- Guida: il passo 4.04 dice "file a 24,7 mm [C]": diventa "file a 25,4 (10 passi) [S], prova a secco prima di saldare".

Verifica che resta, sul pezzo vero (**prova a secco**, al banco, prima di tagliare e saldare la basetta):
1. infilare le due strip femmina 1 × 20 sui pin dell'ESP32;
2. appoggiare la scheda con le strip sulla millefori intera, con le gambe nelle righe 2 e 12 (10 passi): devono entrare tutte e quaranta senza forzare né piegarsi;
3. se entrano, si taglia la basetta e si salda come da schema; se no, si misura con il calibro (Q-18) e si passa all'opzione 3 di S-02 (strip su striscioline separate, schema da rifare per la parte degli strip).

La prova a secco sostituisce la misura con il calibro come condizione per saldare: è più sicura (prova tutti i 40 pin insieme e anche il passo lungo le file) e non chiede uno strumento. La misura di Q-18 resta utile ma non blocca più.

## P-002 (S-01): la testata 2 × 8 della scheda del carapace (proposta, decide l'utente)

### Lo spazio sotto la scheda, con le quote di oggi

| Cosa | x | z | Fonte |
|---|---|---|---|
| dorso del carapace (faccia interna) | — | 34,4 | `predisposizioni.md` 2.8 |
| scheda X2 (20 × 30, \|y\| ≤ 15) sulle bugne alte 3,5 | 29,5 … 49,5 | 29,3 … 30,9 | `corpo.py:1082`, `sch_x` 39,5 |
| PCB dell'ESP32 (sulle strip da 8,5 sopra la basetta) | 13,7 … 76,3 | 16,0 … 17,6 | `rif_componenti.py:459-468`, D-053 |
| connettore FPC della camera | 40,75 … 45,25, \|y\| ≤ 7,25 | fino a 19,6 | idem |
| modulo con l'antenna (non sotto la scheda) | da 55,6 | fino a 20,8 | idem |
| USB-C dell'ESP32 (dietro, sotto lo sportellino) | 12,7 … 20,1 | fino a 20,9 | idem |

Sotto la faccia bassa della scheda (z 29,3) restano **11,7 mm** sopra il PCB dell'ESP32 e **9,7** sopra il connettore FPC. Testata dritta con la spina IDC innestata e il cavo piegato: **16-18** [S] (`predisposizioni.md` 2.3). Mancano 4-8 mm: con la testata dritta la scheda non si chiude.

Spostare la scheda dove ci sono 18 mm (opzione 1 di S-01): non ho trovato un posto. Ai lati dell'ottagono restano 3,5 mm di larghezza o 4,2 d'altezza (`predisposizioni.md` 2.3); davanti, sopra modulo e flat, c'è l'amplificatore (x 60,7); sopra la SSC-32 c'è l'ottagono, che deve restare libero. Abbassare l'ESP32 vorrebbe dire strip femmina basse da comprare e basetta senza posto per regolatore (7,2) e PTC (8,1). La scarto.

### Tre soluzioni

| | A. Testata a 90° con chiave sul bordo verso l'ottagono | B. Cavo saldato sulla scheda, giunzione IDC volante nell'ottagono | C. Testata a 90° piegata dalla strip in casa, chiave col polo 14 |
|---|---|---|---|
| Cosa | box header 2 × 8 a 90°, chiave come oggi, sul bordo di coda della scheda (x 29,5); la spina entra ed esce **orizzontale, verso −X**, dentro l'ottagono | niente testata sulla scheda: i 16 conduttori del flat saldati in due file (come sulla basetta, riga 13); a metà cavo una coppia IDC femmina + IDC maschio da cavo piatto che si stacca dall'ottagono | strip maschio 2 × 8 piegata a 90° (senza scatola) sul bordo di coda; polo 14 tolto e foro 14 della spina tappato |
| Altezza sotto la scheda | scatola circa 9 [S]: fondo a circa z 20,3, **2,7 mm** sopra il PCB dell'ESP32; l'FPC (da x 40,75) non è sotto la testata (x 29,5 … 38,5) | solo le saldature: circa 2 | circa 5 [S] di pin e 6,5-9 di spina orizzontale [S]: come A |
| Spina | spina IDC orizzontale lunga circa 10-12 [S], da x 29,5 verso x 17,5, z 20,3 … 29,3: sopra la USB-C (che arriva a z 20,9), raggiungibile dall'ottagono | giunzione di circa 20 × 25 × 10 [S] appoggiata nell'ottagono, sopra la SSC-32: va fermata (fascetta) o sbatte | come A |
| Protezione dal verso | piena (scatola e chiave) | piena (spine con chiave) | solo dal giro di 180°: il tappo del foro 14 cade sul polo 3; uno spostamento di una colonna resta possibile (5 V sulla massa: scatta PTC1) |
| CAD 2.1.7 | scheda più lunga (circa 23 invece di 20) e viti di coda spostate davanti alla testata (x ≥ 41,5, oggi 32), `sch_sp` diventa l'ingombro vero (9 + 1,6); verificare spina e flat contro USB-C, SSC-32 e ottagono | `sch_sp` a 1,6 + 2; nessun altro cambio; un sostegno della giunzione nell'ottagono | come A, senza scatola |
| BOM | nella voce X2 (approvata, non ancora comprata) la testata dritta diventa **a 90° con chiave** compatibile con la spina Würth 61201623021: stesso ordine, prezzo simile [S] | X2: via la testata, in più un **IDC maschio 2 × 8 da cavo piatto** (circa 1-2 € [S]); flat in due pezzi | X2: via la testata (−1 € circa); costo zero |
| Guida | 4.06, 13.16, 13.17 riscritti (testata sul bordo, verso della chiave); scheda: la scatola non copre più le colonne C-F, quindi più fori liberi per i moduli (DIN e pulsante non più sui pin) | 16 conduttori da separare e saldare sulla scheda, a passo 2,54; giunzione da fermare a ogni montaggio | come A, più la prova del verso a ogni innesto |
| Schemi | J2 si sposta sul bordo; reti e prove (2.2, 2.6) restano | J2 diventa una fila di piazzole; reti e prove restano | come A |

Valori [S] da confermare con i disegni della testata e della spina scelte prima del CAD (le quote dei box header a 90° con chiave sono di catalogo, non ancora lette).

### Raccomandazione: A

- **Risolve con il margine più grande e senza pezzi in più**: X2 non è ancora comprata, quindi si cambia solo il tipo di testata nello stesso ordine; la protezione dal verso resta piena come vuole la scelta 1 di schemi.md 2.7 (girata, la spina porterebbe il 5 V sul pulsante della 2813).
- **La spina esce dove deve uscire**: verso l'ottagono, cioè dove la guida già la fa sfilare per togliere il carapace (`predisposizioni.md` 2.3, "si sfila la spina dall'ottagono").
- **Libera la scheda**: la scatola non sta più in mezzo, quindi CE1, le piazzole dei moduli e qualche foro libero in più (chiesto da S-01) entrano senza saldare sui pin della testata.
- B evita la testata ma lascia una giunzione volante sopra la SSC-32 e 16 saldature delicate; C costa zero ma protegge solo in parte. Tengo B come riserva se in CAD la spina orizzontale di A tocca la USB-C o la SSC-32.

Cosa serve dall'utente: la scelta (A, B o C) e, se ce l'ha già, che testata e che millefori ha in casa (Q-02).
