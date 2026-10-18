# Piano dei circuiti stampati (PCB), prima serie r1

Bozza del 18 ottobre 2026, **da approvare prima di partire**. Parte dallo studio in `docs/ricerca/pcb/`: `studio.md` è la sintesi, `architettura-una-per-una.md` l'architettura scelta. Lo studio è stato scritto sul CAD 2.1.6. Qui i dati sono riletti sulla 2.1.7 chiusa (D-077), e dove lo studio è vecchio è scritto. Il piano è stato verificato da tre agenti (fatti, elettrica, completezza) e corretto (sezione 9).

Stato dei dati come nel resto del progetto: **V** verificato (fonte primaria o modello CAD), **S** stimato, **C** da confermare.

## 1. Scelte dell'utente (18 ottobre 2026)

| Domanda | Scelta | Cosa vuol dire |
|---|---|---|
| Architettura | **una per una** | Tre PCB al posto delle tre millefori, con le stesse reti: **PCB-B** (basetta dell'ESP32 sul vassoio), **PCB-C** (scheda del carapace), **PCB-P** (partitori dei piedi e delle NTC). Stessi moduli, stessi fili verso il resto del robot |
| Montaggio | **a mano** | Schede nude dal produttore, niente chip a passo fine. Basetta e carapace solo con componenti a reoforo; SMD 0805 solo sulla scheda dei partitori, dove lo spazio li impone (scelta delegata all'agente il 18 ottobre, sezione 2) |
| Produttore | **JLCPCB** | Un solo ordine, e un pannello se il preventivo vero lo conviene (5.6) |
| Banco S1 | **sulla r1** | Le millefori non si saldano mai. Le prove di S1 che non hanno bisogno delle schede (IDF, camera, SSC-32 da USB, un servo) si fanno prima, con i moduli sciolti |

Principio della r1: **semplice e verificabile a mano col multimetro**. Ogni rete importante ha un punto di prova. Le scelte ancora aperte hanno un ponticello a saldare o un'impronta vuota, così un errore si corregge con un filo e non con una nuova serie.

## 2. Decisioni che restano all'utente

Le chiedo in F0, prima di F1. Le sigle sono DU-n, per non confonderle con i componenti U1, U2. Per ognuna c'è la mia proposta.

| N. | Domanda | Proposta | Perché |
|---|---|---|---|
| DU-1 | **Togliere il traslatore KAmod** (ritocco b)? La TX verso la SSC-32 esce dal canale 3 del buffer U3, che è già sulla scheda. La RX passa da un partitore 10 kΩ / 15 kΩ | **deciso il 18 ottobre: sì** | Un modulo e una voce in meno (C1, 2,51 €) e 12 giunti in meno. Costa 4 resistenze a reoforo dal set B10 (4.1). Il partitore si monta sempre: con la TX a 5 V dà 3,0 V, sopra la soglia alta di 2,48 V. Se la TX fosse a 3,3 V la seriale non funziona ma non si rompe niente; il ripiego si monta solo dopo averla misurata (4.1) |
| DU-2 | **Presa Qwiic vera sulla PCB-C** (JST SH SM04B-SRSS-TB, ritocco c) al posto del cavo Qwiic tagliato? | **deciso il 18 ottobre: no** | L'utente ha scelto le piazzole: 4 piazzole con il nome (GND, 3V3, SDA, SCL), dove si salda il cavo Qwiic tagliato verso l'espansore TCA9534, come sulla millefori. La presa sarebbe servita solo a innestare l'espansore e moduli futuri senza saldare, e dalla 2.1.7 si raggiunge solo a carapace tolto (la scheda sta a x 29,5…51, l'ottagono finisce a x 28): non vale un componente in più sulla scheda più piena |
| DU-3 | **ERC e DRC di KiCad nella CI**? | **deciso il 18 ottobre: sì**, con KiCad dal PPA e non da Docker Hub | La CI resta verde solo con schemi e PCB puliti. È una dipendenza nuova della CI: un paio di minuti d'installazione, poi la cache (S). Docker Hub è già fallito il 9 ottobre (`ci.yml:58-60`). La CI controlla anche che la versione di KiCad sia quella scritta in `pcb/README.md`: il PPA può dare un'altra 10.0.x |
| DU-4 | **Acquisti di F0**: moduli e piccole parti che servono alla dima e al banco S1, in un ordine Kamami e **un solo** ordine DigiKey | **sì, voce per voce con il prezzo** (5.1) | Le voci B e C (B2 D24V22F5, B3, B6, B10, C3; C1 solo se DU-1 = no) sono già approvate: cambia solo il momento. **Le voci X vanno approvate per l'acquisto** (BOM, sezione X): X1, X6 e il resto di X9 servono al banco; di X2 e X9 sono approvati solo testata, 470 µF, buffer e resistenze. Le piccole voci nuove (10 kΩ 0805, eventuale MF-R090) si approvano qui e non in R1, così DigiKey è un ordine solo: sotto i 75 € la spedizione costa 25 € (`BOM.md`, sezione X) |
| DU-5 | **Posto della PCB-P**: tasca accanto all'IMU (P1) o sotto le prese dei piedi (P2)? Si decide in F2, dopo le prove nel CAD | **da vedere sulle prove** | 4.3: P2 chiuderebbe insieme S-28, S-29 e P-012, come chiede D-076, ma costa la strada B dei partitori e chiede la misura della spina JR |

Scelte che faccio io e annoto nel disegno (le cambio se l'utente vuole):
- **PTC1**: impronta per MF-R075 e MF-R090 (passo 5,08, S su Bourns). Si monta l'MF-R075 già approvato (X9). Il valore si decide con la misura di P4 (S-06). Fino ad allora il firmware limita i LED sotto i 600 mA (R-10, alternativa): va scritto nel piano di S1.
- **Pull-up del bus**: R4 e R5 da 4,7 kΩ, impronte che si possono lasciare vuote. Con tutti i moduli della r1 il conto dà circa 0,97 kΩ, sul minimo di 0,97, perché il modulo SparkFun X20 ha 4,7 kΩ inseriti di fabbrica (V, guida SparkFun). **Si taglia il ponticello I2C di X20**: si torna a circa 1,2 kΩ. Valore atteso al passo 8.28: 1,2–1,6 kΩ, mai sotto 0,97 (S-13; stato S finché non sono letti i pull-up di GY-6500 e dei ToF Pololu).
- **TCA9534**: il modulo X20 esce a **0x27** (V, guida SparkFun), il progetto dice 0x20. Propongo 0x27 nel firmware, così non si tocca il modulo, e l'aggiornamento di `piano-elettronica-software.md` 2.4. L'impronta SOIC-16 vuota sulla PCB-C, se ci sta, va su un indirizzo diverso (0x20).
- **Resistenze in serie sulle uscite di U3**: 330 Ω su 3Y (TX5) e **R9 da 330 Ω sulla scheda**, accanto a 2Y (DATA2). R9 stava nella guaina solo perché sulla millefori non c'era posto (`schemi.md:232`). Senza le 4,7 kΩ del KAmod, un Dupont sul pin sbagliato o una SSC-32 spenta caricherebbero direttamente il buffer, che porta anche le due catene LED. A 115200 baud la resistenza non cambia niente (S).
- **Restano fuori dalle schede**: R3, R6 e la 100 kΩ di OFF (R-12: un filo staccato lascia tutto spento o al sicuro), D2 per scelta, come oggi; R8 perché sta sul microfono.
- **Masse**: un piano intero sul retro, senza piste "a stella". Con il piano la caduta dei ritorni dei LED (0,86 A) è di pochi mV su 1 oz (S). Le piste dedicate non si possono fare: KiCad collega ogni piazzola GND al piano, e U2 sta fra le due file (dubbio 2 di `studio.md`).
- **Polo 14 del cavo piatto**: piazzola di riserva sulla PCB-C (XSHUT del ToF del mento, X25) e piazzola libera sulla PCB-B. Costo zero.
- **Componenti a reoforo su basetta e carapace** (l'utente ha chiesto di poter saldare come sulla millefori e ha lasciato a me la scelta, 18 ottobre): CS1 e CS2 da 100 nF a reoforo; R-TX, R10, R11, R12, il partitore di JP-RMT e il ripiego da 1 kΩ a reoforo dal set B10; R-MIC a reoforo. Gli unici SMD sono gli 8 + 8 0805 della PCB-P: in 0,4 mm per lato (P1) o in 7 mm di larghezza (P2) quelli a reoforo non ci stanno. Si saldano a mano con pinzetta, punta fine e flussante (B19); i componenti segnati "non montare" restano vuoti.
- **Strip dell'ESP32**: saldati tutti i pin, salvo quelli dei varchi (4.1). Nei varchi i contatti si sfilano dalla strip femmina; il ripiego è la strip tagliata a pezzi, con l'impronta fatta per i pezzi.
- **Fori delle viti**: Ø2,4 non metallizzati, come i passanti M2 del CAD (`rif_componenti.py:133`): la tolleranza viene dalla posizione degli inserti nei pezzi stampati. Sulla dima si prova solo che le viti centrano gli inserti.

## 3. Cosa non fa questo piano

- **Non cambia reti né GPIO**: il firmware non se ne accorge (`studio.md` 6.3), salvo l'indirizzo del TCA9534 (2).
- **Non porta connettori nuovi** verso il resto del robot, salvo, con la variante P2, le spine delle prese dei piedi saldate sulla PCB-P. I fili restano saldati sulle piazzole, con il nome in serigrafia. La PCB-B non si toglie senza dissaldare: è il limite della una per una.
- **Non è la serie definitiva**: la r2 si decide dopo la prova della r1 sul robot.
- **Non scrive il programma di banco S1**: oggi non esiste (`04-banco.yaml`, passo 4.05: "non c'è ancora"). È lavoro del software S1, da pianificare a parte. È la condizione per montare la r1 (F7).
- **Non mette gli STEP delle PCB nel design di lavoro**: in F4 gli ingombri si provano con scatole provvisorie. La sostituzione delle scatole `Rif_Basetta_50x70` e `Rif_Scheda_Carapace` con gli STEP chiede codice nuovo in `rif_componenti.py` (oggi `fai_step` è fatto per il servo e i Pololu) ed è la voce di una versione del CAD successiva, con il suo piano.
- **Millefori come alternativa**: la guida tiene la strada con le millefori per la basetta e, con la variante P1, per i partitori. Per la scheda del carapace no: i suoi disegni sono rimasti alla 2.1.6 e il 17 ottobre si è deciso di non rifarli (`piano-guida.md`). La PCB-C è l'unica strada aggiornata per il carapace, e la sezione 13 della guida passa alla PCB già dopo F7.

## 4. Le tre schede (dati riletti sulla 2.1.7)

Quote in mm nella terna del robot: X avanti, Y a sinistra, Z in alto. Due strati, 1,6 mm, rame da 1 oz, HASL senza piombo.

### 4.1 PCB-B, basetta dell'ESP32

| Dato | Valore | Stato, fonte |
|---|---|---|
| Sagoma | 56 × 35, x 22…78, \|y\| ≤ 17,5; faccia componenti in alto, z 5,9…7,5 | V; `rif_componenti.py:111-113`; `corpo.py:86`; `assieme.py:63-64` |
| Fori | (29; ±6,8) e (75,5; ±6,5) sulle colonnine Ø5,8 del vassoio, M2 × 5 | V; `corpo.py:485-488`; `fori.json` `bas_col_*_ins` |
| Senza rame | Ø6 attorno ai fori sulla faccia alta (testa Ø4 più 1 mm) e Ø6,8 sulla faccia bassa (colonnina Ø5,8 più 1 mm); da x 74 al bordo di testa, su tutte e due le facce (antenna) | S; `studio.md` 2.1, correzione 6; R-15 |
| Sotto | 3,3 mm fino al vassoio; teste M2 svasate del vassoio a 3,4 sotto la scheda | V; D-077 |
| Sopra | 8,5 fino al PCB dell'ESP32; 6,6 sotto la sede della microSD (x 22,5…37,5, \|y\| ≤ 7), meno i componenti sul retro dell'ESP32 (S-08) | V modello, C pezzo |
| File dell'ESP32 | due strip femmina 1 × 20 a y ±12,7 (25,4), da x 22,5 a 73,3 | S fino alla prova a secco (P-005) |
| Vicinanze | morsettiera della SSC-32 a 3,1 dal bordo di coda; asola del bus della 2.1.7 a 0,5 oltre il bordo +Y (x 26,5…33,5); colonnina del carapace a 1,3 dal bordo ±Y | V; `rif_componenti.py:483-490`, `corpo.py:51`; `corpo.py:187-191`; `corpo.py:108-110`, `:392-393` |

**Componenti**: U1 ESP32 su strip; U2 D24V22F5; U3 SN74AHCT125N in DIP-14; D1 1N5819; PTC1; R1, R2, R4, R5, R7 come oggi; CS1 e CS2 da 100 nF **a reoforo** (oggi sono SMD del kit B8).
Con DU-1 = sì si aggiungono:
- R10, pull-up da 10 kΩ all'ingresso del canale 3, **verso il 3V3 dell'ESP32** (lato ESP32 di JP-3V3), mai verso il 5 V. GPIO21 non ha pull al reset e resta libero finché il firmware non avvia la UART (scheda Espressif, letta dalla verifica: si riconferma in F0);
- R-TX da 330 Ω in serie su 3Y;
- R11 e R12, partitore 10 kΩ / 15 kΩ della RX.

Con DU-1 = no resta U4 KAmod. R9 da 330 Ω entra sulla scheda in tutti e due i casi.

**Ripiego della RX**: R11 da 1 kΩ al posto della 10 kΩ e R12 non montata, **solo dopo una misura scritta della TX della SSC-32 a non più di 3,6 V**. Con 1 kΩ, se la TX fosse comunque a 5 V, la corrente nel diodo di protezione resta sotto circa 1,5 mA (S). Serigrafia accanto a R11 e R12: "partitore di serie; ripiego solo con TX ≤ 3,6 V misurata". A SSC-32 staccata il partitore tiene GPIO14 bassa: il firmware vede un break, ed è atteso (nota per S1).

**Ponticelli a saldare**:
- **JP-3V3 a tre piazzole**: al centro il 3V3S, da un lato il 3V3 dell'ESP32 (chiuso), dall'altro l'uscita di X3 (aperto). Serigrafia "un lato solo" e prova al multimetro fra le piazzole esterne (D-076: mai J1 e X3 insieme).
- **JP-RMT** per la misura del jitter su GPIO38 al banco, aperto. Ha una piazzola RMT_IN per l'impulso della SSC-32, con una massa accanto e fuori dalle file, e un partitore 10 kΩ / 15 kΩ come la RX (gli impulsi sono a 5 V). Serigrafia "aprire JP-RMT prima del carapace".

**Regole** (`studio.md` 1.4 e 2.5, correzioni della verifica dello studio e di questo piano):
- **VBAT**: pista da 1,5 mm, 1 mm da ogni altro rame. Entra dal bordo +Y e attraversa la fila +Y in un varco di **due posti senza foro**: O-2 e P-2, cioè GPIO7 e GPIO6, non usati (V, `schemi.md:93`). La piazzola d'ingresso ha accanto solo masse e sta **ad almeno 5 mm** dalle piazzole a 3,3 V e dei GPIO: oggi il posto O-1/P-1 è fra le piazzole del bus (`schemi.md:220`), quindi si sposta verso la coda. Niente punto di prova nudo del VBAT accanto ai GPIO: il punto ha solo una massa vicino.
- **5 V e pin dell'ESP32**: nessuna pista **o piazzola** a 5 V a meno di 1 mm da un pin dell'ESP32 senza massa in mezzo (R-09). TX5, DATA, DATA2, il 5 V delle luci e il 5V_REG verso il suo punto di prova attraversano le file solo nei varchi dei posti non usati: fila +Y C…H e J…R; fila −Y B-C, G-H, I-J-K e S-T (`schemi.md:93`). Il partitore della RX sta fuori dalle file.
- **Eccezioni scritte nel file delle regole**: le piazzole di U2 (VIN a 2,54 da EN e GND, e EN si tratta come VBAT perché ha 270 kΩ interni verso VIN, pagina Pololu 2858) e la coppia pin 5V / GPIO14 (0,84 mm, controllata dalla prova 5 della guida). Il pin 5V esce verso l'interno: verso il bordo restano 0,9 mm.
- **Bordo −Y**: le piazzole a 5 V (poli 1-2, polo 4, luci delle tibie) devono stare a 1 mm dalla strip a y −12,7. Con piazzole Ø1,7 e 0,5 mm dal bordo il centro sta solo fra \|y\| 15,4 e 16,15: **una fila sola**, circa 19 posti a passo 2,54. Il cavo piatto va in quella fila: niente "due file sfalsate". I posti si contano prima del piazzamento, insieme a P-140 (strisce del cavo piatto più basse di 1 mm, 2.1.8) e alla verifica `cavo_piatto`.
- **Larghezze**: 5V_REG 1,5; 5V_LED 1,0; 5V_ESP 0,6; 3V3S 0,5; segnali 0,25 (`studio.md` 2.5).
- **PTC1**: il più lontano possibile dal retro dell'ESP32, meglio fuori dalla sua ombra, sdraiato, senza riempimento di rame sotto (R-10: a PTC scattato la superficie passa i 100 °C, S).
- **Punti di prova** fuori dall'ombra dell'ESP32, a gruppi per tensione con una massa in mezzo: VBAT e 5 V (5V_REG, 5V_LED) da una parte; 3V3S, SDA, SCL, RX3, LED_IN, SENSE, ENA, OFF dall'altra; TX5, DATA e DATA2 con le uscite di U3. Il 5V_ESP si misura nella presa del pin 5V, come oggi.
- **Piazzole dei fili**, con il nome: 2813 (VBAT, GND, SENSE, OFF), abilitazione, seriale (TX5, RX5, e la massa vuota finché S-22 non è misurato), bus a 4 rami più uno di riserva, luci delle tibie (3), cavo piatto. Due fori Ø1,5 per le fascette accanto ai fasci.

### 4.2 PCB-C, scheda del carapace

| Dato | Valore | Stato, fonte |
|---|---|---|
| Sagoma | **21,5 × 30**, x 29,5…51,0, \|y\| ≤ 15 (lo studio dice ancora 23 × 30) | V; `rif_componenti.py:186-188`; D-077 |
| Facce | faccia alta a z 31,5 sulle bugne; componenti sotto, faccia bassa a z 29,9; 2,9 d'aria fino al dorso | V; `assieme.py:115`; `corpo.py:240-241` |
| Fori | (41,5; ±12,5) e (48,0; ±12,5), inserti M2, viti M2 × 4, teste Ø3,8 sulla faccia dei componenti | V; `fori.json` `ins_sch_*`; `corpo.py:238-239` |
| Testata J2 | Würth 61201621721, 2 × 8 a 90°, lunga 27,98. Scatola x 29,5…38,35, alta 9 sotto la scheda. File dei pin a 1,84 e 4,38 dietro la scatola, cioè a x ≈ 40,2 e 42,7, per \|y\| ≤ 8,9. Chiave al centro, sul lato lontano dalla scheda. Spina IDC verso la coda | V (disegno Würth, `dimensioni-componenti.md:165`); C solo il polo 1 rispetto alla chiave (S-26) |
| Vicinanze | amplificatore a 0,85 dal bordo anteriore; il flat della camera torna al suo connettore (x 40,75…45,25) passando sotto la parte anteriore della scheda, e le verifiche del CAD oggi lo saltano (`assieme.py:163`, `:353`, `:561`); 10,3 di altezza sotto la scheda sul connettore | V; D-077 |

**Il posto è stretto.** Le file dei pin di J2 arrivano a x 42,7, e le teste delle viti prendono gli angoli. Per CE1, la presa, le piazzole e i punti di prova restano circa **7,4 × 19 mm** al centro (x 43,6…51) (S, conto della verifica). Sopra la scheda ci sono 2,9 mm d'aria fino al dorso, quindi le code dei pin a reoforo si tagliano a meno di 2 mm.

**Componenti**: J2; CE1 470 µF 10 V sdraiato; 4 piazzole per il cavo Qwiic tagliato verso l'espansore (DU-2 = no); l'impronta SOIC-16 vuota del TCA9534, che è la prima a uscire se manca posto; R-MIC a reoforo, vuota (S-21); punti di prova (5V, 3V3, GND, SDA, SCL, DATA).

**Piazzole**: una per filo, raggruppate per modulo: catena LED (3), microfoni (5), amplificatore (5), ToF posteriore (5), pulsante (2), riserva del polo 14. Il pulsante va su piste isolate e lontane dalle altre (S-10). Il gruppo I2S è separato dal bus con una pista di massa.

La PCB-C si piazza per prima, in F4.

### 4.3 PCB-P, partitori

Oggi la striscia dei partitori **non ha un posto nel CAD** (S-28, S-29). Le prese dei piedi e delle luci stanno sul tetto senza supporto (P-012, P-141). La PCB-P è l'unica delle tre schede che cambia forma, e l'unico motivo di cambiare il CAD.

| Variante | Dove | Pro | Contro | Stato |
|---|---|---|---|---|
| **P1, tasca accanto all'IMU** (studio) | x 60,5…71,3, y −20,9…0,75; PCB circa 20 × 10, due fori M2 | sagoma piccola, niente spine sulla scheda; la strada B con la striscia di oggi resta possibile | 0,4 mm per lato in X (non 0,8 come dice lo studio). I 12 fili dei piedi arrivano da +Y: passano sotto l'ADC (circa 3,7 × 4 mm fra le sue bugne) o fra ADC e colonna (1,8 mm sotto z −4). P-012 resta aperto | V tasca; S passaggi |
| **P2, sotto le prese dei piedi** | a +Y, fra l'ADC e il servo di coxa: y circa 19…25,5, x da scegliere fra 44 e 79. Fori M2 oltre i capi della fila. Su bugne da 4, come IMU e ADC (sopra il pacco il tetto resta intero, `corpo.py:179`), quindi la scheda sta a z −5,4…−3,8, alla quota del fondo dell'ADC | chiude S-28, S-29 e P-012 per i piedi in un pezzo solo, come chiede D-076 ("prese progettate con lo schema della striscia dei partitori, con la misura vera della spina JR"); fili corti verso l'ADC | Circa 7 mm di larghezza per la fila delle spine (2,6), 8 R e 8 C in 0805 e le piazzole. Le spine salgono di circa 3,5 mm rispetto a `spine_prese` della 2.1.7. Serve la misura della spina JR. La NTC sinistra non ha spina (va su piazzole, o con una spina nuova da approvare). Le prese delle luci e la NTC destra (a −Y) restano su fili. **La strada B dei partitori diventa una millefori tagliata sulla sagoma della PCB-P** | S, da provare in F2 |

Componenti in tutte e due le varianti: 8 × 10 kΩ 1 % in 0805 (voce nuova), 8 × 100 nF in 0805 dal kit B8, due fori M2, piazzole d'uscita verso A0…A7, VIN e GND dell'ADC (pin del modulo, S-31). Con P2 anche la strip maschio delle sei spine dei piedi (come le prese di oggi, X5).

## 5. Fasi

Ogni fase finisce con **commit, push su `main` e CI `ci` e `sim` verdi**, e lascia la repo in uno stato da cui una sessione nuova riparte. A ogni arresto si aggiornano la riga di stato di `CLAUDE.md` e lo stato in fondo a questo file. Le revisioni R1…R4 sono **punti d'arresto**: si aspetta il via dell'utente.

| Fase | Cosa | Chi | Uscita | Arresto |
|---|---|---|---|---|
| **F0** | dati (5.1), decisioni DU-1…DU-4, acquisti | utente e agente | tabella 5.1 chiusa o con un ripiego scritto; ordini fatti | — |
| **F1** | strumenti e **prova del metodo** (5.2) | agente | `pcb/` con librerie, regole, generatore, controllo delle reti; esito della prova scritto; CI se DU-3 = sì | se la prova fallisce: chi fa schema e sbroglio |
| **F2** | versione 2.1.8 del CAD (5.3) | agente, Fusion | posto della PCB-P provato in due varianti | **DU-5** |
| **F3** | schemi: PCB-B e PCB-C subito dopo F1 (anche mentre si fa F2), PCB-P dopo DU-5 | agente (o utente, secondo F1) | tre schemi, ERC a zero, `verifica_reti.py` verde | **R1**: reti, componenti, conferma delle voci del BOM |
| **F4** | piazzamento, PCB-C per prima; PCB-B dopo P-140 | agente (o utente) | componenti al loro posto; ingombri provati nel CAD con scatole provvisorie (`urti_scatole`, ognuna con il caso di controllo): flat della camera sotto la PCB-C, spine | — |
| **F5** | dima stampata 1:1 | agente (STEP `--board-only`), utente (stampa e prova) | ESP32 con la strip preparata, D24V22F5, buffer, testata, spine e viti provati sulla dima | **R2**: posti, render, dima. Lo sbroglio parte solo dopo |
| **F6** | sbroglio | agente (o utente) | VBAT e potenza, poi masse, poi segnali; DRC a zero con parità dello schema; serigrafia | **R3**: lista 5.4 |
| **F7** | uscite, pannello e ordine (5.6) | agente, poi utente | Gerber controllati, preventivo vero, foglio di montaggio e collaudo della r1, tag `pcb-r1` | **R4**: l'utente ordina e paga |
| **F8** | montaggio per gradi e banco S1 | utente, agente per le prove | prima solo U2 e l'alimentazione, con misure senza ESP32; poi buffer e passivi; poi l'ESP32. Errata in `pcb/README.md`. Entra solo con il programma di banco S1 pronto | — |
| **F9** | robot e guida | agente e utente | PCB nel robot: interferenze vere, poi 30 minuti di marcia quando ci sono il robot completo e il firmware di P4 (S3), cioè mesi dopo. La guida passa alla strada A (5.5) | approvazione del passaggio |

**Durata** (S, rifatta dopo la verifica):

| Tratto | Durata |
|---|---|
| F0 | una sessione, più l'attesa dei pezzi |
| F1 | 1–2 sessioni |
| F2 | come una versione del CAD, 2–3 blocchi |
| F3–F6 | 4–6 sessioni se la prova di F1 riesce; di più se schema e sbroglio passano all'utente nell'editor |
| Fabbricazione e spedizione | 1–3 settimane |
| **Dal via alle schede in mano** | **circa 5–8 settimane di calendario** |

### 5.1 F0: dati, decisioni, acquisti

| Dato | Serve per | Chi | Come, ripiego |
|---|---|---|---|
| Quale delle 4 schede è la RE1.3 (Q-18) | U1 | utente | sigla stampata sulla scheda |
| Piedinatura dell'ESP32 vista dal lato giusto (S-15) e altezze dei componenti sul retro (S-08) | U1, altezze sotto la scheda | utente | foto del retro e della serigrafia |
| Strip con i contatti di O-2 e P-2 sfilati, e prova a secco a 25,4 (P-005, dubbio 11 dello studio) | varchi del VBAT e del 5 V | utente | se lo sfilamento non riesce: strip tagliata a pezzi, impronta per i pezzi |
| Ordine dei pin del D24V22F5 (S-03) | U2 | agente | pagina Pololu 2858 e STEP in `cad/modelli/` |
| Polo 1 della testata Würth rispetto alla chiave (S-26) | J2 | agente | disegno del produttore |
| Schede tecniche: SN74AHCT125 (soglie), ESP32-S3 (stato di GPIO21 al reset), Bourns MF-R (impronte di R075 e R090) | U3, R10, PTC1 | agente | fonte primaria |
| Pull-up e indirizzo del modulo SparkFun X20: 4,7 kΩ inseriti e 0x27 di fabbrica (V, guida SparkFun) | bus, firmware | agente, poi utente sul pezzo | taglio del ponticello I2C; scelta dell'indirizzo (2) |
| Passo e piedinatura del KAmod (S-04), solo se DU-1 = no | U4 | agente, poi utente sul pezzo | pagina Kamami |
| Tensione a riposo della TX della SSC-32 e massa VL− (S-22, Q-19) | ripiego della RX, massa della seriale | utente, multimetro, con la SSC-32 alimentata | se manca, si monta il partitore di serie |
| Misura della spina JR, maschio e femmina: passo, ingombro, altezza (P-012, Q-04) | variante P2, `spine_prese` | utente | calibro; se manca, P2 si scarta e si fa P1 |
| Taglia degli SMD del kit B8 (S-30) | impronte 0805 | utente | calibro |
| Valori nel set di resistenze B10 (15 kΩ, 330 Ω, 1 kΩ) | R11, R12, R-TX, ripiego | utente, alla consegna | se mancano, a reoforo nell'ordine DigiKey |
| Posizione dei pin A0…A7 del modulo ADC (S-31) | PCB-P, fili verso l'ADC | agente su Adafruit, poi utente | `docs/ricerca/dati-moduli.md` |
| Portafusibile Neuftech (Q-23) | P-139 della 2.1.8 | utente | se manca, P-139 passa alla 2.1.9 (5.3) |

I dati dell'agente si leggono su fonte primaria e si marcano V. Quelli che mancano diventano C e hanno un ripiego scritto.

**Acquisti (DU-4)**: in F0 preparo l'elenco voce per voce dal BOM, con prezzo, negozio e stato (B e C già approvate, X da approvare, piccole voci nuove), e il totale dell'ordine DigiKey rispetto ai 75 €. L'utente approva e ordina. Le voci che escono (C1 con DU-1 = sì; le 6 + 3 resistenze e i 6 condensatori a reoforo di X5 e X14, salvo scorte) si tolgono dai carrelli prima dell'ordine.

**All'approvazione di questo piano**, in un commit: decisione D-078 con le scelte del 18 ottobre e le risposte DU-n; `CLAUDE.md` (stato, mappa, prossimi passi); voce PCB di `docs/backlog.md`.

### 5.2 F1: progetto KiCad e prova del metodo

```
pcb/
  README.md                 versione di KiCad, revisioni, errata, comandi, foglio di montaggio della r1
  librerie/hex2.kicad_sym   simboli dei moduli
  librerie/hex2.pretty/     impronte: ESP32 a 25,4 con i varchi, D24V22F5, KAmod (se resta), Würth a 90°, PTC,
                            più una copia di quelle standard usate (strip, DIP-14, DO-41, 0805, ponticelli, punti di prova)
  regole/hex2.kicad_dru     fonte unica delle regole, copiata in ogni progetto da uno script
  script/genera_contorni.py contorni, fori e zone senza rame dalle quote del CAD; modo --controlla
  script/verifica_reti.py   netlist di KiCad contro guida/schemi/sorgenti/*_def.py
  aggiunte.yaml             componenti e reti volute che i *_def.py non hanno
  basetta/  carapace/  partitori/   un progetto per scheda, ciascuno con il suo <nome>.kicad_dru
  ordini/r1/                Gerber, fori e distinta effettivamente inviati
```

**Prova del metodo** (prima di tutto il resto; esito scritto in `pcb/README.md`). L'agente non ha un modo provato per usare l'interfaccia grafica di KiCad, e `kicad-cli` esporta la netlist ma non la importa nel PCB. La prova del 18 ottobre ha generato solo uno schema vuoto. Su una scheda di prova piccola:
1. schema generato da script, con simboli, etichette di rete e fili, che passa l'ERC;
2. PCB con le impronte e le reti assegnate alle piazzole da `pcbnew`;
3. una pista e un riempimento di massa tracciati da script;
4. DRC con `--schematic-parity` a zero, e un caso di controllo che fallisce.

Se riesce, schema, piazzamento e sbroglio li fa l'agente da script, e l'utente rivede nell'editor e nei render. Se non riesce, si prova l'agente con l'automazione dell'interfaccia (strumenti `cmux-cua`). Altrimenti schema e sbroglio nell'editor li fa l'utente, con l'agente che prepara contorni, impronte, piazzamento iniziale, regole e controlli. La colonna "Chi" e le durate si correggono di conseguenza.

**Il resto di F1**:
- KiCad 10.0.7 sul Mac (V). `kicad-cli` fa ERC, DRC, Gerber, fori, posizioni, STEP, render, SVG e PDF (V, provati il 18 ottobre). I messaggi escono in italiano: nella CI si usa `--format json`. I comandi provati vanno in `pcb/README.md` e in `produzione.md` 4.1.
- Niente autorouter: Freerouting sarebbe una dipendenza nuova.
- **Quote del CAD**:
  - `rif_componenti.py` importa le librerie di Fusion e non si carica fuori da Fusion. Quindi `genera_contorni.py` legge le liste `PARAMETRI` di `rif_componenti.py` e `corpo.py` con `ast`, senza importarle, e ne valuta le espressioni.
  - Le pose (basetta con centro in x 50, scheda del carapace) vengono da `guida/dati/manifest.json`, i fori da `fori.json` (`bas_col_*_ins`, `ins_sch_a…d`, V).
  - Lo script genera una volta. Poi `--controlla` legge il `.kicad_pcb` senza riscriverlo e fallisce se contorno o fori si sono staccati dal CAD.
  - Gira in pytest senza KiCad, leggendo il testo del file, quindi anche con DU-3 = no.
- **Regole**: KiCad legge solo `<progetto>.kicad_dru`, accanto al `.kicad_pro`. Uno script copia la fonte unica nei tre progetti e la CI controlla che le copie siano uguali. Un caso di controllo per scheda: una violazione voluta deve far fallire il DRC.
- **`verifica_reti.py`**:
  - per ogni rete dei `*_def.py`, tutti i pin stanno nella stessa rete di KiCad, e nessuna rete di KiCad unisce due reti dei `*_def.py`;
  - una tabella dà il nome del pin → numero (U1, U3, U4, diodi) e gli alias (3V3_ESP / 3V3S con JP-3V3);
  - `pcb/aggiunte.yaml` elenca le differenze volute: canale 3 sulla seriale e R10, R-TX, R11, R12 (DU-1); R9 sulla scheda; JP-RMT, RMT_IN e il suo partitore; polo 14; piazzole del Qwiic; SOIC-16 e R-MIC vuote; punti di prova; spine JR con P2;
  - tutto quello che non è né nei `*_def.py` né in `aggiunte.yaml` è un errore;
  - un caso di controllo: una rete scambiata apposta deve fallire.
- `scheda_def.py` descrive la scheda del carapace della 2.1.6. Per il confronto contano solo le reti, che non sono cambiate. Va scritto nel controllo, non corretto.
- `.gitignore`: `*-backups/`, `.history/`, `*.kicad_prl`, `fp-info-cache`, `*.lck`, uscite di produzione fuori da `ordini/`.
- **STEP**: si esportano con `--user-origin` sull'origine del CAD. Nello STEP di KiCad l'asse Y è rovesciato (V, provato il 18 ottobre). La procedura si prova su un punto noto e si scrive in `cad/CLAUDE.md`.
- **CI** (se DU-3 = sì): job `pcb` con KiCad dal PPA, controllo della versione, ERC, DRC con parità, `verifica_reti.py`, `genera_contorni.py --controlla`. Gli script Python passano anche da `ruff`. I test che chiedono `pcbnew` si saltano se il modulo manca.

### 5.3 F2: versione 2.1.8 del CAD

La 2.1.8 ha già tre voci in attesa (`piano-v2.1.0.md`, "Seguito: versione 2.1.8"):
- P-139, i reofori delle spie: aspetta il portafusibile (Q-23);
- P-140, le strisce del cavo piatto: toccano le piazzole della PCB-B;
- P-141, le prese dei piedi: sono proprio la variante P2.

Proposta: la 2.1.8 contiene P-140, P-141 e la PCB-P. P-139 entra solo se Q-23 arriva in tempo, altrimenti passa alla 2.1.9. Il piano della versione si scrive in `piano-v2.1.0.md` prima di partire, come le altre, e si aspetta il via.

- **Prima di partire**: copia di ripristino "Hexapod v2.1.0 - ripristino 2.1.7 (prima della 2.1.8)", da aggiungere in `CLAUDE.md` fra i file da non toccare. Il tag `v2.1.7` c'è già.
- **Prova delle varianti**: P1 e P2 si provano come scatole provvisorie con `urti_scatole`, come `spine_prese` e `qwiic_adc`, ognuna con il suo caso di controllo. `assieme.py → varianti` lavora solo con `Rif_*` già in libreria e serve dopo.
  - P1: la PCB-P e i due passaggi dei fili dei piedi (sotto l'ADC, fra ADC e colonna).
  - P2: la PCB contro il bordo dell'ADC (y 18,45) e contro il servo di coxa AS a tutta l'escursione; le spine più alte di 3,5 mm contro vassoio e cavi.
- **Variante scelta (DU-5)**: bugne con inserti M2, `Rif_Partitori` in `LIBRERIA` e nel passo `ingombri`, `fori.json` e `manifest.json` rigenerati.
- **A valle**, come ogni versione (`cad/CLAUDE.md`, blocco a valle), così `test_guida` e la CI restano verdi:
  - viteria e inserti nel BOM;
  - catalogo della guida (giunzioni, viteria);
  - `esporta_guida`, poi `guida.costruisci controlla`;
  - passi 7.10, 8.09 e 8.10 alla 2.1.8.
- La basetta e la scheda del carapace **non cambiano** nel CAD.
- **Verifiche di fine versione** come sempre: controllo dell'assieme, sentinella sui volumi, CI verde, decisione D-0xx, `versioni.md`, salvataggio in Fusion, tag `v2.1.8`.

### 5.4 R3: lista di controllo dopo lo sbroglio

- DRC ed ERC a zero, con la parità dello schema; `verifica_reti.py` verde; `genera_contorni.py --controlla` verde.
- Antenna: niente rame per x ≥ 74 sulla PCB-B.
- VBAT isolato, da 1,5 mm, nei due posti senza foro; piazzola e punto di prova a 5 mm dal 3,3 V e dai GPIO.
- Nessun 5 V, pista o piazzola, a meno di 1 mm da un pin dell'ESP32, salvo le eccezioni scritte.
- R10 verso il 3V3 dell'ESP32; partitore della RX montato di serie, con la serigrafia del ripiego.
- Faccia dei componenti: "LATO COMPONENTI" e freccia verso la testa in serigrafia. Controllo nel 3D di KiCad e con lo STEP (PCB-C con i componenti in basso, PCB-B in alto).
- Polarità e pin 1 in serigrafia: D1, CE1, U3, J2 e la sua chiave, PTC1.
- Nome, revisione e data: "HEX2 BASETTA r1", "HEX2 CARAPACE r1", "HEX2 PARTITORI r1".
- Punti di prova raggiungibili con l'ESP32 inserito; nomi delle piazzole uguali a quelli della guida.
- Code dei pin della PCB-C sotto i 2 mm; niente sotto la PCB-B oltre i 3,3 mm.

### 5.5 F8 e F9: montaggio, documenti e guida

- **Foglio di montaggio e collaudo della r1** (in `pcb/README.md`, fatto in F7): ordine dei componenti, punti di prova, valori attesi, prima accensione senza ESP32. Prove in più rispetto alle millefori:
  - portata del Wi-Fi con l'ESP32 sulla basetta (antenna sopra il rame fino a x 74);
  - GPIO21 all'avvio;
  - break atteso sulla RX a SSC-32 staccata;
  - temperatura di U2, che si misura in P4.
- **Decisioni**: D-078 all'approvazione del piano; poi una voce a ogni revisione approvata.
- **BOM**:
  - entrano: PCB, 0805 da 10 kΩ, eventuale MF-R090, strip delle spine con P2, resistenze che mancano in B10, 2 condensatori da 100 nF a reoforo per CS1 e CS2;
  - escono: C1 con DU-1 = sì, i 6 + 3 × 10 kΩ e i 6 × 100 nF a reoforo di X5 e X14 (salvo scorte).
- **Guida**:
  - Sezione 13: passa alla PCB-C dopo F8, perché per il carapace non c'è alternativa.
  - Sezioni 4 e 8: passano alla strada A dopo F9. Le millefori restano la strada B per la basetta e, con P1, per i partitori.
  - Cambiano anche le appendici A.15–A.19 (`architettura-una-per-una.md` 7.2). Spariscono 4.11–4.14 e 4.24.
  - Le stampe di KiCad prendono il posto dei disegni delle millefori. I `*_def.py` restano la fonte delle reti.
- **Altri documenti**: `cablaggio.md`, `predisposizioni.md`, `schemi.md` (nota sulla strada A), `piano-elettronica-software.md` 2.4 (indirizzo del TCA9534), `CLAUDE.md` a ogni arresto.

### 5.6 F7: pannello e ordine

- **Pannello o tre disegni separati**: si confrontano due preventivi veri.
  - Il pannello si fa a mano in KiCad (un quarto progetto `pcb/pannello/`). KiKit sarebbe una dipendenza nuova.
  - Niente linguette sui bordi con gioco sotto 1,5 mm: il fronte della PCB-C (0,85 dall'amplificatore) e i bordi ±Y della PCB-B (1,3 dalle colonnine del carapace).
  - Il pannello passa DRC e Gerber come le schede.
- Gerber aperti in GerbView e nell'anteprima di JLCPCB.
- Preventivo vero sotto i 170 $: oltre, IVA e dazio passano al corriere con la sua commissione. Si controllano anche dazio, voci doganali e cambio (`produzione.md` 6.3).
- Tag `pcb-r1` e file inviati in `pcb/ordini/r1/`.

## 6. Rischi

| Rischio | Come si riduce |
|---|---|
| Schema e sbroglio da script non riescono | prova del metodo in F1, prima di tutto; ripieghi scritti (5.2) |
| Impronta sbagliata (ESP32, D24V22F5, testata, PTC, spine) | dati di F0 su fonte primaria; dima prima dello sbroglio (F5) |
| Rete sbagliata | `verifica_reti.py` con `aggiunte.yaml`; ponticelli e 0805 per correggere con un filo; 4 schede di scorta |
| 5 V su un GPIO | varchi nelle file, VBAT lontano dal bus, punti di prova a gruppi; ripiego della RX solo dopo la misura; prima accensione senza ESP32 |
| Bus con pull-up troppo forti | ponticello di X20 tagliato; R4 e R5 sostituibili; misura al passo 8.28 |
| PCB-P senza posto | due varianti provate in F2 prima dello schema della PCB-P |
| PCB-C troppo piena (7,4 × 19 mm utili) | piazzata per prima; l'impronta del TCA9534 esce per prima |
| Specchiature | serigrafia, 3D di KiCad, STEP con l'asse Y controllato |
| Antenna sopra il rame | niente rame da x 74; prova di portata del Wi-Fi in F8 |
| Calore di U2 e del PTC sotto l'ESP32 | piano di massa; PTC lontano, senza rame sotto; misura in P4; tetto del firmware sotto 600 mA fino ad allora |
| Moduli non arrivati in tempo per la dima | acquisti in F0; se tardano, la dima si fa con le misure dei disegni e il rischio si dichiara in R2 |
| La 2.1.8 aspetta Q-23 | P-139 passa alla 2.1.9 (5.3) |
| Dogana e prezzi | un solo ordine, sotto i 170 $; Aisler se le regole cambiano |

## 7. Uso di agenti e di token

Il disegno lo faccio io nel flusso principale. Ai punti d'arresto, prima di portare il lavoro all'utente, può servire una verifica con pochi agenti (al più tre, effort alto, Sonnet dove basta), sui risultati scritti su file:
- dopo F3 (R1): reti e sicurezza elettrica;
- dopo F6 (R3): regole di 4.1 e lista 5.4;
- dopo F7 (R4): Gerber, pannello e preventivo.

**Ogni verifica si chiede prima all'utente**, con il numero di agenti e i token stimati, e parte solo con il suo via.

Riferimenti di oggi: la raccolta per questo piano ha usato 4 agenti e circa 0,9 milioni di token, la verifica 3 agenti e circa 0,65 milioni. Una verifica costa quindi circa 0,7–1 milione di token. Il flusso principale si aggiunge a parte: circa una finestra d'uso per sessione di disegno (S).

## 8. Per ripartire

Lo stato sta qui sotto, aggiornato a ogni fase: fase corrente, ultimo commit, cosa aspetta l'utente.

**Stato al 18 ottobre 2026**: piano scritto, verificato e corretto. Aspetta l'approvazione dell'utente (decise il 18 ottobre: DU-1 = sì, KAmod tolto; DU-2 = no, piazzole al posto della presa Qwiic; DU-3 = sì, KiCad nella CI). Nessun file KiCad nella repo.

**Acquisti (DU-4, in parte)**: il 18 ottobre, prima di approvare il piano, l'utente ha approvato i pezzi nuovi delle schede: 10 kΩ 0805, 15 kΩ / 330 Ω / 1 kΩ se mancano in B10 (voci PCB1 e PCB3 del BOM; dopo la scelta di basetta a reoforo, PCB3 si compra a reoforo), e X1. Da approvare in F0 con il resto: 2 condensatori da 100 nF a reoforo per CS1 e CS2. La presa JST SH (PCB2) è stata approvata e poi tolta lo stesso giorno, con DU-2 = no. L'ordine DigiKey è **in sospeso**, da unire ad altre voci per superare i 75 €. Le voci che il piano toglierebbe (C1, reoforo di X5 e X14) restano nel BOM finché il piano non è approvato. Restano da approvare per l'acquisto X6 (ADC) e il resto delle voci X del banco.

## 9. Verifica del piano (18 ottobre 2026)

Tre agenti indipendenti, effort alto, con tre lenti: fatti e fonti, elettrica e sicurezza, completezza ed eseguibilità. Hanno trovato 51 rilievi: 1 bloccante, 31 importanti, 19 minori. I dati chiave li ho ricontrollati sulle fonti:
- bugne da 4 mm (`corpo.py:179`);
- file dei pin Würth (`dimensioni-componenti.md:165`);
- ottagono a x −20…28 (`requisiti.md:195`);
- S-13 (`schemi.yaml`);
- guida SparkFun del modulo X20: 0x27, ponticello I2C chiuso con 4,7 kΩ. In S-13 c'era "2,2 kΩ, non letto": sono i pull-up dei ponticelli d'indirizzo.

Correzioni principali:
- **Bloccante**: il metodo per fare schema e sbroglio non era provato. Ora c'è la prova del metodo in F1, con i ripieghi (5.2).
- **Ordine delle fasi**:
  - il CAD della PCB-P viene prima dello schema della PCB-P;
  - la dima viene prima dello sbroglio;
  - la PCB-B aspetta P-140;
  - la 2.1.8 non aspetta Q-23.
- **Acquisti**: le voci X non erano già approvate. Ora ci sono un elenco voce per voce e un solo ordine DigiKey.
- **Elettrica**:
  - partitore della RX sempre montato, con il ripiego da 1 kΩ solo dopo la misura;
  - R10 verso il 3,3 V;
  - resistenze in serie su TX5 e DATA2, con R9 sulla scheda;
  - VBAT lontano dal bus;
  - punti di prova a gruppi;
  - una fila sola al bordo −Y;
  - posto del PTC e tetto del firmware;
  - pull-up con X20 (ponticello da tagliare) e indirizzo 0x27;
  - "stella" delle masse tolta.
- **Geometria**:
  - PCB-C con le file dei pin V e lo spazio vero (7,4 × 19 mm);
  - variante P2 su bugne da 4, con la sua larghezza vera e le spine più alte;
  - due passaggi dei fili in P1.
- **Strumenti**:
  - quote del CAD lette con `ast`;
  - un `.kicad_dru` per progetto;
  - `aggiunte.yaml` per le differenze volute;
  - pannello in F7;
  - nessuno STEP nel design di lavoro in questa serie.
- **Regole di lavoro**:
  - commit, push e CI a ogni fase;
  - copia di ripristino della 2.1.7;
  - D-078 e `CLAUDE.md` all'approvazione;
  - verifiche con agenti chieste prima;
  - durate rifatte.

Non applicato:
- il pull-up da 100 kΩ sulla RX proposto da una verifica: con R12 da 15 kΩ a massa la linea resterebbe comunque bassa (0,43 V). Il break a SSC-32 staccata resta atteso e scritto.
- I rapporti completi dei verificatori non sono nella repo: i rilievi sono riassunti qui e corretti nel testo.
