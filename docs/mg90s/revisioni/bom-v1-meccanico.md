# Revisione del BOM v1 — meccanica, montaggio, completezza

Data: 8 ottobre 2026. Revisore indipendente. Documento rivisto: `docs/BOM.md` (versione 1), con `docs/dimensionamento.md` e `docs/dimensioni-componenti.md`.
Fonti di confronto: `research_notes/Studio componenti esapode MG90S/verifica_*.md` (giunti_stampa, servo_mg90s, dimensionamento, batteria_cablaggio, esp32cam_camera, ssc32), le note lunghe solo per dettagli puntuali, il report `reports/Studio componenti esapode MG90S.md`, lo script `calc/statica_tripode.py` (rieseguito: stessi numeri del documento).

Gravità: **bloccante** = costruendo o comprando come scritto qualcosa non funziona o si danneggia; **importante** = rilavorazione probabile, quantità sbagliata, numero in disaccordo con il valore verificato; **minore** = chiarezza o miglioria.
Etichette: [calcolo] = conto mio con formula; [stima] = valore mio non da fonte, da confermare.

## Esito in breve

- Nessun bloccante. 13 rilievi importanti, 4 minori.
- I tre punti da chiudere **prima di aprire il CAD**: come si monta e si smonta il giunto (M-01), in quale segmento sta ogni servo (M-05), dove stanno batteria e cavi rispetto alle coxe (M-06).
- Il bilancio di massa è sommato male e incompleto: il totale realistico è circa 1,15 kg, non 1,07 (M-07). Con quella massa il punto di progetto sta al 49–50 % dello stallo, cioè sul limite.
- Mancano dal BOM: ugello da 0,6 mm per i caricati carbonio, basetta e zoccolo per l'elettronica sfusa, viti M2 lunghe, rondelle M2, fermo del perno, micrometro.

## Rilievi

### M-01 — importante — Giunto: perno "forzato nella plastica" senza fermo; ordine di montaggio non definito

Voci: D1, D2, D3.

Problema. Il BOM dice solo "spina forzata nella plastica" e "squadretta chiusa in una sede stampata". Non dice quale pezzo porta il cuscinetto, quale il perno, come si infila il servo fra i due bracci e come si toglie.

Evidenza.
- Corsa assiale per calzare la squadretta sul millerighe: 32,25 − 28,3 = 3,95 mm (`dimensioni-componenti.md`, quote di inizio e fine millerighe). Corsa per infilare il perno nel cuscinetto: 3 mm (larghezza F683ZZ). Una staffa a U in un solo pezzo, con squadretta già in tasca e perno già piantato, dovrebbe aprirsi di 3,95 + 3 ≈ 7 mm [calcolo]: con bracci stampati lunghi circa 20 mm non si monta.
- Il report di progetto prescrive altro: "Il cuscinetto va nel guscio fisso, il perno nella staffa mobile" e "spina rettificata da 3 mm bloccata nella staffa da una vite di fermo" (report, sezione "Giunto senza gioco"). Il progetto di riferimento SmallpTsai ha 18 viti M2×10 "pin locks" (`giunti_stampa.md`, sezione 1). Nel BOM la vite di fermo non c'è.
- Le note si contraddicono: `giunti_stampa.md` sezione 1, Inferences, dice prima "il cuscinetto va nel guscio fisso e il perno nella staffa mobile; non il contrario", e alla riga dopo "il perno coassiale va quindi creato nella culla stampata".
- Un perno piantato a pressione in foro cieco non si estrae: sostituire un servo guasto vorrebbe dire rompere la culla. È contro il requisito "smontabile ovunque".

Correzione. Scrivere nel BOM la scelta, prima del CAD:
1. Cuscinetto nel fondo della culla (fondo ≥ 3 mm di sede + 1 mm di battuta), flangia verso l'esterno; perno nel braccio mobile.
2. Perno **infilato per ultimo dall'esterno**, scorrevole a mano nel foro del braccio e bloccato da una vite di fermo M2 trasversale (18 viti M2×6–8 + 18 inserti o dadi in più), oppure braccio lato cuscinetto smontabile con 2 viti M2 su inserti. Mai a pressione in foro cieco.
3. Squadretta inserita in una tasca aperta verso l'esterno e chiusa da un coperchietto avvitato, così il braccio lato albero si monta dopo aver calzato la squadretta.
4. Lunghezza del perno: 3 (cuscinetto) + 0,5 (rialzo sull'anello interno) + spessore del braccio; 10 mm va bene con braccio da 5–6 mm.
5. Rialzo stampato Ø ≤ 4,3 mm attorno al perno, che tocchi solo l'anello interno: senza, la culla striscia sullo schermo del cuscinetto.
6. Giunto di coxa: albero in alto e cuscinetto in basso, così il peso del corpo scarica sulla flangia e non tira la squadretta fuori dal millerighe.

### M-02 — importante — Spina Ø3 h8: accoppiamento descritto a metà, reperibilità non verificata

Voce: D2.

Problema. Il BOM scrive "gioco nel cuscinetto ≤ 0,014 mm" e "ferramenta, Amazon.it". Con h8 l'accoppiamento va da 0,008 mm di interferenza a 0,014 mm di gioco; le spine che si trovano normalmente (DIN 6325 / ISO 8734 temprate, DIN 7 comuni) sono m6, che nel cuscinetto entra sempre forzata.

Evidenza.
- `verifica_giunti_stampa.md` riga 7: foro P0 2,992–3,000 mm; h8 = 0/−0,014; m6 = +0,002/+0,008 "sempre interferenza 0,002–0,016 mm". Spina h8 al massimo (3,000) in foro al minimo (2,992): 0,008 mm di interferenza [calcolo].
- Stessa riga: verdetto "non verificabile su fonte primaria"; "all'acquisto farsi dare dal venditore la tolleranza in mm e misurare le spine col micrometro".

Correzione. Ordinare "ISO 2338 h8" con tolleranza dichiarata dal venditore, non "spina 3×10" generica. Confezione da 50: misurare col micrometro e scegliere le 18 fra 2,986 e 2,992 mm. Se arrivano m6: si piantano nell'anello interno con una pressa appoggiando l'anello interno (mai spingendo sull'esterno) e si lascia scorrevole il lato plastica con vite di fermo (vedi M-01). Aggiungere il micrometro 0–25 mm agli attrezzi.

### M-03 — importante — Serraggio dei servo: il BOM copre solo le due viti delle alette

Voci: D7, D8.

Problema. Il requisito è "servo serrati nelle sedi". Il BOM elenca viti M2 da 4 a 20 mm e "circa 50" dadi, cioè le sole alette. Il report stesso dice che non basta.

Evidenza.
- Report, sezione "La cassa si stringe in una culla": "Due viti nelle alette stanno su una sola retta e lasciano il servo libero di oscillare"; sede "in due metà che le viti chiudono sulla cassa".
- Progetto di riferimento: 2 viti M2×30 passanti + 2 dadi per servo (`giunti_stampa.md`, sezioni 1 e 4). M2×30 non rientra nell'assortimento 4–20 mm.
- Conteggio dadi: alette 18 × 2 = 36; ne restano 14 su 50. Se la culla si chiude con altre 2 viti per servo servono 36 + 36 = 72 dadi [calcolo].
- Aletta nello STEP: foro Ø2,5 con svasatura Ø4,3 profonda 1,05 dal lato inferiore, spessore 2,5: sotto la testa della vite restano 2,5 − 1,05 = 1,45 mm di plastica, con asola aperta verso l'estremità (`dimensioni-componenti.md`). Le viti di serie sono flangiate (`verifica_servo_mg90s.md` riga 21). Una testa ISO 4762 M2 (Ø3,8) senza rondella appoggia su una corona di (3,8 − 2,5)/2 = 0,65 mm [calcolo].
- Sede del dado: centro foro a (27,5 − 22,6)/2 = 2,45 mm dalla cassa; tasca esagonale M2 da 4,2 mm (`giunti_stampa.md`, sezione 5): 2,45 − 2,1 − 0,15 = 0,2 mm di parete [calcolo]. Non si stampa.

Correzione.
- D8: 100 dadi M2 DIN 934 più 50 dadi quadri DIN 562 M2 (4 × 4 × 1,2), da infilare di fianco.
- D7: aggiungere M2×25 e M2×30 (40 pezzi l'una) finché il CAD non dice che non servono.
- Nuova voce: 50 rondelle M2 DIN 433 (Ø4,5): stanno tra foro e cassa con 2,45 − 2,25 = 0,2 mm [calcolo]; la DIN 125 (Ø5) non ci sta.
- Nel CAD la tasca del dado sotto l'aletta va aperta verso la cavità del servo: è la cassa a impedire la rotazione.

### M-04 — importante — Squadretta di serie: quote ignote, viti non definite, domanda mancante

Voci: D3, D7, D12, domanda 5.

Problema. La tasca della squadretta è il pezzo che trasmette la coppia in tutti i 18 giunti, ma nessuna quota delle squadrette è nota e il BOM non la chiede. D7 assegna viti M2 alle "squadrette" senza sapere il diametro dei loro fori.

Evidenza.
- `verifica_servo_mg90s.md` riga 21: squadrette di serie, "Quote (lunghezza, interasse e Ø fori, spessore): NON TROVATO".
- Report, tabella finale, domanda 5: chiede "quote delle tre squadrette" e "sporgenza delle viti del fondo". La domanda 5 del BOM le ha perse entrambe.
- `giunti_stampa.md` sezione 3: "due viti passanti nei fori della squadretta". I fori delle squadrette dei micro servo sono fatti per viti autofilettanti sottili, di norma ben sotto i 2 mm [stima, non verificata]: una M2 non passa senza forare.
- Fra lotti diversi di cloni le squadrette non sono intercambiabili (`verifica_servo_mg90s.md` riga 19).

Correzione.
- Domanda 5: aggiungere, per la squadretta che si intende usare, lunghezza, larghezza e spessore del braccio, Ø e altezza del mozzo, Ø e passo dei fori; e la sporgenza delle 4 viti del fondello (cadono a 6,45 mm dall'asse dell'albero, la sede della flangia arriva a 4,15: con teste da Ø3 restano circa 0,8 mm [calcolo da X = ±10, Z = ±4,5 e asse a X = 5,375; Ø della testa stimato]).
- Decidere dopo la misura: tasca a forma con coperchietto (nessuna vite nella squadretta) oppure fori allargati a 2,1 mm.
- Comprare i 18 servo più le scorte in un unico lotto; le scorte portano anche le squadrette e le viti centrali di ricambio, che altrimenti non esistono.
- D12 (frenafiletti): vedi M-16.

### M-05 — importante — Geometria 36 / 34 / 50: entra in una sola disposizione, che il documento non dichiara

Voce: `dimensionamento.md`, "Punto di progetto".

Problema. Le lunghezze vengono dalla sola statica. Non c'è alcuna verifica d'ingombro contro la cassa del servo, e non è scritto in quale segmento sta ciascun servo.

Quote usate (ufficiali Tower Pro e STEP): cassa 22,8 × 12,4; asse albero a 5,925 mm dalla faccia corta lato cavo e a 22,8 − 5,925 = 16,9 mm dall'altra; aletta lunga (32,2 − 22,6)/2 = 4,8 mm, quindi punta dell'aletta a 10,7 mm e a 21,5 mm dall'asse. Raggi spazzati attorno all'albero [calcolo]: spigolo vicino della cassa √(5,925² + 6,2²) = 8,6; spigolo vicino dell'aletta √(10,7² + 6,2²) = 12,4; spigolo lontano dell'aletta √(21,5² + 6,2²) = 22,4 mm.

Aritmetica.
- **Due casse sul femore, in linea, code verso l'interno**: 2 × 16,9 = 33,8 mm di cassa su 34 mm di interasse. Restano 0,2 mm, senza pareti; le alette sommano 2 × 21,5 = 43 mm > 34. **Non entra.** Servirebbero almeno 2 × 16,9 + 2 × 2 (pareti) + giochi ≈ 39 mm e alette sfalsate.
- **Due casse sul femore, code verso l'esterno**: fra le facce 34 − 2 × 5,925 = 22,2 mm, fra le alette 34 − 2 × 10,7 = 12,6 mm: entra. Ma il pezzo è lungo 34 + 2 × 21,5 = 77 mm e la coda del servo d'anca spazza un raggio di 22,4 mm: arriva a 36 − 22,4 = 13,6 mm dall'asse della coxa, dove la staffa della coxa ha la sua anima. Spigolo della culla del servo di coxa a √(8,1² + 8,4²) = 11,6 mm dall'asse (cassa più 2 mm di parete e 0,15 di gioco); più 1 mm di gioco e 3 mm di anima: faccia esterna a 15,6 mm. Interferenza di circa 2 mm.
- **Disposizione classica** (servo del femore nella coxa, femore passivo, servo del ginocchio nella tibia):
  - femore: fra i due raggi spazzati delle alette vicine restano 34 − 2 × 12,4 = 9,2 mm; tolti i giochi (2 × 0,7) e i bordi delle culle restano 6–7,5 mm per l'anima del femore **e** per i cavi. Entra, di misura.
  - coxa: con la coda del servo del femore rivolta verso l'asse della coxa, 36 − 21,5 − 2,15 = 12,4 mm contro 15,6 necessari: non entra (−3,2 mm). Con il lato lungo del servo in verticale, 36 − 6,2 − 2,15 = 27,7 mm: entra con 12 mm.
  - coda in alto o in basso: in basso la coda si avvicina al ginocchio quando il femore scende a −52° (lo spigolo dell'aletta resta a √(34² + 22,4² − 2 × 34 × 22,4 × cos 21,9°) = 15,6 mm dall'asse del ginocchio, contro 12,4 mm spazzati dal servo di tibia più due pareti): solo la coda in alto funziona.
  - tibia: servo con coda verso il piede, 21,5 + 2,15 = 23,6 mm dall'asse del ginocchio; per fusto e piedino restano 50 − 23,6 = 26,4 mm. Entra.
- Ginocchio chiuso a 74°: lo spigolo più vicino del servo di tibia resta a 29 mm dall'asse del femore [calcolo: punto a 22,4 mm e 57,9° dalla linea ginocchio–anca]. Nessun urto.

Conseguenza. 36 / 34 / 50 è costruibile solo così: servo del femore nella coxa con il lato lungo verticale e la coda in alto; femore passivo a due piastre con anima da circa 6 mm; servo del ginocchio nella tibia con la coda verso il piede. Ogni altra disposizione chiede femore ≥ 39–40 mm o coxa ≥ 40 mm.

Correzione. Scrivere la disposizione in `dimensionamento.md`. Prima del CAD fare uno schizzo 2D del piano della zampa con le casse a quote ufficiali più 2 mm di parete, a femore −52° e −4° e ginocchio 74° e 134°. Tenere `zam_femore` come parametro: portarlo a 38 mm cambia poco la coppia (dipende dalle distanze orizzontali, non dalle lunghezze) e toglie il problema dell'anima. Il cavo del servo di tibia esce dalla faccia corta rivolta proprio verso quei 6 mm: prevedere lì il canale.

### M-06 — importante — Corpo: batteria e cavi contro la posizione delle coxe

Voci: A5, D11; `dimensionamento.md` (assi coxa agli angoli (±72, ±40) mm).

Problema. Gli assi delle coxe d'angolo distano 144 mm in lunghezza e 80 mm in larghezza. Il pacco, alla tolleranza massima, misura proprio 144 × 49,3 × 27,4 mm, più 50–60 mm per i cavi. Nessun documento controlla che il tutto conviva.

Evidenza.
- `verifica_batteria_cablaggio.md` riga 4: inviluppo massimo 144 × 49,3 × 27,4 mm. `batteria_cablaggio.md` sezione 1: "Prevedere almeno 50-60 mm liberi oltre la testata oppure far risalire i cavi sopra il pacco".
- Lunghezza: 144 + 55 ≈ 200 mm contro 144 mm fra le coxe [calcolo]: il corpo sporge di circa 55 mm da una parte, oppure i cavi 12 AWG (Ø4,5) e la coppia di T-plug risalgono sopra il pacco e aggiungono circa 8–10 mm in altezza.
- Larghezza: vano 50 + 2 × 2 = 54 mm. Servo di coxa con il lato lungo parallelo alla batteria: 80 − 2 × (6,2 + 2,15) = 63,3 mm liberi, cioè 4,6 mm per parte [calcolo]. I 9 cavi per lato non passano allo stesso livello: vanno sopra.
- Servo di coxa d'angolo orientato lungo la zampa (40° dall'asse longitudinale), coda verso il centro: fondo cassa a (72 − 16,7 × 0,766; 40 − 16,7 × 0,643) = (59,2; 29,3); spigolo interno a y = 29,3 − 6,2 × 0,766 = 24,5 mm [calcolo]. La parete del vano sta a 27 mm e il pacco, al massimo, a 24,65: il servo entra nel vano.
- La scheda ESP32 è larga 67,5 mm con l'antenna e va dietro il frontale (vedi M-08): fra le culle delle due coxe anteriori ci sono 63 mm.

Correzione. Fissare nel BOM o in `decisioni.md`: livello della batteria rispetto ai servo di coxa (stesso piano oppure sotto), lato di uscita dei cavi, verso di estrazione. Servo di coxa con il lato lungo parallelo alla batteria (la squadretta si calza a passi di 17–18° e il resto si corregge via software). Rivedere la stima di 290 g di parti stampate con un corpo da circa 200 mm.

### M-07 — importante — Bilancio di massa: somma sbagliata, voci basse, voci mancanti

Voce: `dimensionamento.md`, "Bilancio di massa".

Somma delle righe come scritte: 241 + 260 + 45 + 14 + 30 + 3 + 3 + 12 + 8 + 30 + 30 + 8 + 12 + 50 + 290 + 45 = **1081 g**, non "≈ 1070" [calcolo]. Il margine sulla massa di progetto (1100 g) è 19 g, non 30.

Voci in disaccordo con i dati o chiaramente basse:

| Voce | Nel bilancio | Rilievo | Correzione |
|---|---|---|---|
| 18 cuscinetti e spine | 12 g | spina Ø3 × 10 acciaio: π × 0,15² × 1,0 × 7,85 = 0,555 g; × 18 = 10,0 g [calcolo]. Cuscinetto circa 0,4 g [stima]; × 18 = 7 g | 17 g (+5) |
| SSC-32 | 45 g | unico dato pubblicato: "peso articolo 61 g" su Amazon (`verifica_ssc32.md` riga 8a, dato di catalogo); il report usava 60 g | 45–61 g: pesare (+0…16) |
| Batteria | 260 g | caso peggiore 259 + 20 = 279 g (`verifica_batteria_cablaggio.md`, osservazione 3) | 260–279 g (+0…19) |
| Prolunghe, cavetti, traslatore | 30 g | 10 prolunghe da 15 cm a circa 3,2 g = 32 g da sole [stima]; mancano clip C5, guaina e fascette D13, cavo 22 AWG B14, prolunga C6 | circa 50 g (+20) |
| Viteria e inserti | 50 g | solo alette: 36 viti + 36 dadi ≈ 15 g; inserti e viti M3 del corpo, M2 dei gusci: 60–80 g [stima]. Il report usava 40 g | 65 g (+15) |

Voci assenti: piedini (6 × 1,5 g), cinghie (2 × 3 g), 18 squadrette con vite (18 × 0,5 g), basetta e zoccolo (M-12, circa 8 g), spinotto USB-C C3, eventuale antenna esterna: circa **+30 g** [stima].

Totale realistico: 1081 + 5 + 20 + 15 + 30 ≈ **1150 g**, fino a circa 1185 g con batteria e SSC-32 al caso peggiore [calcolo]. È sopra la massa di progetto. Dalla tabella di sensibilità dello stesso documento: 1,15 kg, h = 72, passo 40 → **49 %**; ogni 50 g valgono circa 2 punti, quindi a 1,185 kg si è al 50–51 %.

Va notato che il report di ricerca diceva che lo script usa 1150 g, "che è prudente"; lo script oggi parte da 1100 g.

Correzione. Correggere la somma; aggiungere le voci mancanti e una riga di margine del 5 %; riportare la massa di progetto a 1150 g e rifare la tabella dei risultati. Con 1150 g il punto di progetto è al 49 %: il vincolo regge con un solo punto di margine. Per riavere il margine di oggi servono passo 30 mm (42 %) o h = 75 mm (43 %): dirlo nel "Risultato in breve". Non comprare la batteria da 5200 mAh prima di aver pesato schede e una zampa di prova.

### M-08 — importante — Camera: il modulo OV3660 "75MM" non è verificato; con quello da 21 mm la scheda è obbligata

Voce: A3, domanda 3.

Problema. Il BOM propone come acquisto la "versione a flat lungo 75MM" e marca la riga "V (modulo standard)". Il V vale solo per il modulo da 21 mm.

Evidenza.
- `verifica_esp32cam_camera.md`, tabella delle lacune: esistenza dell'OV3660 con flat da 75 mm "NON VERIFICABILE"; la ricerca indipendente ha trovato OV3660 da 21 e da 80 mm e "moduli da 75 mm solo con sensore OV2640".
- Stesso file, riga 8: lunghezza totale 21 mm, flat libero 21 − 5 − 8 = 8 mm, asse ottico a 21 − 4 = 17 mm dall'estremità della linguetta. Il connettore FPC è al centro della scheda e il flat esce verso l'antenna (`esp32cam_camera.md`, sezione ingombri).
- Conseguenza [calcolo]: con il modulo da 21 mm l'obiettivo guarda perpendicolare alla scheda da circa metà scheda. Per guardare avanti la scheda sta in piedi dietro il frontale, larga 62,6 mm (67,5 con l'antenna) e alta 28,3 mm, con le USB su un fianco e l'antenna sull'altro.
- Stesso file: lo schema porta 1,2 V sul pin DVDD del sensore, che chiede 1,425–1,575 V: "Provare la camera sulla scheda prima di congelare il progetto".

Correzione. Marcare A3 "C" per la versione lunga e non ordinarla senza la lunghezza scritta dal venditore. Disegnare il frontale per il modulo da 21 mm. La testa 8 × 8 × 5,35 mm non ha fori: sede stampata con coperchietto, da aggiungere alle parti. Provare la camera sulla scheda prima del CAD del frontale.

### M-09 — importante — Antenna Wi-Fi: nessuna voce e nessuna domanda

Voci: A2, E1.

Problema. L'antenna su PCB sporge di 4,7–4,9 mm dalla scheda; il corpo è previsto in PETG-CF; accanto ci sono batteria e cavi di potenza. Il BOM non ne parla.

Evidenza.
- `verifica_esp32cam_camera.md`: sporgenza 4,7–4,9 mm. `esp32cam_camera.md`: "Antenna attiva di default (PCB o IPEX): NON TROVATO"; "l'effetto dei filamenti caricati carbonio sull'antenna non è stato verificato in questa ricerca".
- Con la scheda dietro il frontale (M-08) l'antenna finisce su uno spigolo anteriore, dentro il guscio.
- Linee guida Espressif per l'ESP32-S3, sezione sul posizionamento del modulo: "please consider the impact of the housing on the antenna during end-product design"; "A clearance of at least 15 mm is recommended in all directions." [fonte primaria, letta tramite estrazione automatica] https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html

Correzione. Attorno all'antenna una finestra o un coperchio in materiale non caricato (E2), con 15 mm liberi in ogni direzione: nessun metallo, cavo, batteria o parete in PETG-CF dentro quel raggio. Aggiungere la domanda: foto della zona del connettore IPEX (resistenza da 0 Ω che sceglie l'antenna). Voce opzionale: antenna 2,4 GHz con cavetto IPEX, da montare fuori dal guscio se la prova di portata va male. Prova di portata con il guscio montato prima di stampare i pezzi definitivi.

### M-10 — importante — Calore vicino alla plastica: interruttore senza fori, regolatori senza distanziali né feritoie

Voci: B1, B3; tabella "Catena elettrica".

Evidenza.
- B3: "6 A continui a 55 °C; 16 A a 150 °C", misurati a 12 V, 22 °C, aria ferma (`verifica_alimentazione.md` riga 5); PCB senza fori di fissaggio.
- Interpolazione fra i due punti [calcolo]: ΔT = 33 K a 6 A e 128 K a 16 A, esponente ln(128/33)/ln(16/6) = 1,38. A 4,5 A: 33 × 0,75^1,38 = 22 K → circa 44 °C. A 11 A ("picco realistico"): 33 × (11/6)^1,38 = 76 K → circa **98 °C**. A 17,2 A: circa 163 °C. In aria libera a 22 °C; dentro un guscio chiuso di più.
- PETG-CF: 68–74 °C (BOM, sezione E). Una sede stampata che stringe il PCB cede se il picco dura.
- B1: `alimentazione.md`, sezione regolatore: "dissipa ~5-6 W di picco, ~2 W a 4 A medi. Montarlo su distanziali con feritoie". Nel BOM distanziali e feritoie non compaiono.
- La batteria LiPo è a pochi millimetri (M-06).

Correzione. B3 tenuto per i bordi del PCB da due guide con aria sopra e sotto, mai una tasca chiusa; oppure il bilanciere B3-alt, che ha il suo foro da pannello e non scalda il guscio. Regolatori su distanziali da almeno 5 mm (ottone o nylon M2, voce nuova: 8 pezzi) con feritoie sopra e sotto, ad almeno 10 mm dalla batteria. Scrivere nel BOM che i 10 inserti delle schede Pololu sono M2 (vedi M-13).

### M-11 — importante — Materiali e ugello: manca l'ugello da 0,6 mm; i dati sono di un'altra marca

Voci: E1, E2, domanda 7.

Evidenza.
- `giunti_stampa.md`, guida filamenti Flashforge: "Nozzle Size 0.6/0.8mm" per PLA CF e PETG CF. Riletto da me sul PDF del produttore (una pagina, 11 colonne da "PLA" a "PLA CF" e "Petg CF"): la riga del diametro ugello dà "All Size" per le prime nove colonne e "0.6/0.8mm" per le ultime due. La riga "Hardened Nozzle Required" è fatta di simboli grafici e non l'ho potuta leggere. [fonte primaria] https://en.fss.flashforge.com/10000/software/9d9a24cd6d47443d428166b4b1e23dfb.pdf . Conclusione delle note: "conviene prevedere un ugello da 0.6 mm sulla testina dedicata ai caricati (ricambio ufficiale a 39,90 US$)". La Creator 5 esce con 0,4 mm; l'ugello fa corpo con il riscaldatore e si cambia con attrezzi (`verifica_giunti_stampa.md` riga 2). Materiale dell'ugello di serie in disaccordo fra produttore (temprato) e recensione (inox), riga 3: "usare i caricati carbonio su una sola testina sacrificabile".
- Con 0,6 mm "pareti sottili, tasche per dadi M2 e dettagli fini vanno ridisegnati" (`giunti_stampa.md`): la scelta dell'ugello viene **prima** del CAD, non è una domanda da lasciare aperta.
- I numeri della sezione E (68–74 °C, +35 %, "migliore adesione") sono delle schede Bambu Lab. Il verificatore non li ha ricontrollati (`verifica_giunti_stampa.md`, "Non ricontrollato": "Schede Bambu Lab (moduli, HDT, trazione Z)") e le note dicono che "i numeri non sono trasferibili da una marca all'altra". La sezione E non ha la colonna "dato".
- "Rigidezza pari al PLA normale" vale nel piano: 2890 contro 2750 MPa. Fra gli strati il PETG-CF è il **meno** rigido dei quattro: 1680 MPa contro 2370 del PLA, cioè −29 % [calcolo dalla tabella delle note].
- "Il PLA-CF ha la peggiore adesione tra strati": nella stessa tabella la trazione Z è 26 ± 2 MPa per il PLA-CF e 23 ± 4 per il PETG non caricato. Il peggiore è il PETG, entro l'incertezza.
- E1 "circa 350 g" e E2 "circa 150 g" contro 290 g e 45 g del bilancio di massa: va detto che la differenza è scarto, supporti e provini.

Correzione. Nuova voce: "Nozzle Assembly Creator 5, 0,6 mm" (1 pezzo, più 1 di scorta se quello di serie è inox). Colonna "dato" in sezione E con S e la marca. Correggere le due frasi. Regola per il CAD: bracci delle staffe stampati coricati. I provini (sede cuscinetto, inserti, culla, dado M2) si stampano con l'ugello e il filamento definitivi.

### M-12 — importante — Elettronica sfusa senza supporto: mancano basetta e zoccolo

Voci: A2, B7, B9, B10, C1, C2.

Problema. Due resistenze del partitore, il MOSFET con la sua resistenza, un ceramico e il traslatore di livello non hanno un posto dove stare. La scheda ESP32 non ha fori. Il collegamento è previsto con ponticelli Dupont, che su un robot che cammina si sfilano.

Evidenza. BOM A2 "nessun foro di fissaggio"; C2 "Dupont femmina-femmina". Report, sezione sulla scheda: "serve una culla che trattenga i bordi oppure uno zoccolo a due file distanti circa 25,4 mm". Gli header dei servo sulla SSC-32 non hanno chiave né ritegno (BOM, tabella connettori).

Correzione. Voci nuove: 1 basetta millefori circa 50 × 70 mm con 4 fori; 2 strip femmina 1 × 20 passo 2,54 mm (zoccolo dell'ESP32, interasse da misurare: 24,7 o 25,4 mm); 1 strip maschio. Sulla basetta: zoccolo, C1, B9, B10, ceramico dell'ADC, saldati. La basetta dà alla scheda il fissaggio che non ha; sopra, un fermo stampato che la tenga nello zoccolo. Nel CAD: una barra stampata che trattenga le 18 spine dei servo sulla SSC-32, e un appoggio per i due elettrolitici da Ø12,5 × 20 (non appesi ai reofori nei morsetti).

### M-13 — minore — Quantità e scorte

| Voce | Nel BOM | Riconteggio | Correzione |
|---|---|---|---|
| D5 inserti M2,5 | 70, "fissaggio delle schede" | l'unica scheda con fori da M2,5 è la SSC-32: 4 viti. I Pololu B1 e B2 hanno fori M2 (BOM stesso): 2 × 4 + 2 = 10 inserti M2 | D5 serve per 4 pezzi; aggiungere a D4 "schede Pololu: 10" |
| D1 cuscinetti | 18, confezione da 20 | 2 di scorta su 18, senza marca e da piantare in sedi stampate, più i provini | 30 |
| A1 servo | 18 + 2–4 | le scorte danno anche squadrette e viti centrali (1 per servo); lotti diversi non sono intercambiabili | 22, stesso lotto |
| C4 prolunghe | 20, "ne servono circa 10" | dipende dal cavo reale: 250 mm (genuino) o 175 mm (alcuni cloni), `verifica_batteria_cablaggio.md` riga 11. Con 175 mm servono anche i femori centrali e le coxe d'angolo: fino a 16 | 20 bastano; aggiungere la domanda "lunghezza del cavo su 3 servo", che il report aveva e il BOM ha perso |
| D11 cinghie | 2 × 200 mm | giro del pacco più fondo del vano: 2 × (49,3 + 27,4 + 3) = 159 mm; sovrapposizione 41 mm [calcolo] | 20 × 250–300 mm |
| D6 inserti M3 | 100 | non è chiaro se 100 in tutto o 100 per tipo | precisare |
| A4 ingombro SSC-32 | "circa 72 × 55 mm" | `verifica_ssc32.md` riga 8b: PCB 71,5–74 × 54,5–56,5 mm, fori 65–67,5 × 48–50 mm, dima Lynxmotion 68,58 × 50,80 non esclusa | scrivere l'intervallo; nel CAD asole 65–69 × 48–51 mm; sopra la scheda circa 25–30 mm per le spine dei servo in piedi [stima] |

### M-14 — minore — Batteria: manca il fermo in lunghezza

Voce: D11. Le due cinghie tengono il pacco contro il fondo ma non lo fermano in lunghezza: il guscio rigido è liscio e la tolleranza è ±5 mm. Le note chiedevano "fermo regolabile, spessori e cinghia" (`batteria_cablaggio.md`, sezione 1). Aggiungere: battuta fissa da un lato, spessore in schiuma adesiva (EVA 3–5 mm) dall'altro, un foglio antiscivolo sul fondo. La presa di bilanciamento deve restare raggiungibile per il cicalino B8 senza togliere il pacco.

### M-15 — minore — Piedini, cavi, scarico di trazione

- D10: la scelta è rimandata, ma la punta della tibia (Ø e forma) va fissata con il piedino. Il TPU 95A è duro: su pavimento liscio tiene poco. Prevedere in alternativa il tubo o il cappuccio in silicone e stamparne 8, non 6.
- D13: la guaina va solo sui tratti rigidi; ai giunti il fascio resta libero con un'ansa (`batteria_cablaggio.md`, sezione 5). Servono due punti di ancoraggio per giunto: 6 zampe × 3 giunti × 2 = 36 fascette più quelle del corpo [calcolo]; una confezione da 100 basta.
- Asole passacavo: spina JR 8,15 × 3,0 mm al massimo → asola 9 × 4; collare della prolunga 10,55 × 4,25 → asola 11,5 × 5 (`verifica_batteria_cablaggio.md` righe 25–26). Le culle hanno l'asola del cavo sulla stessa faccia corta vicino alla quale cade il cuscinetto (asse a 5,925 mm, cavo a 4,75 mm dal fondo): l'asola deve essere aperta verso l'alto per far scendere il cavo quando si infila il servo.
- Il cavo esce a 5,9 mm dall'asse del giunto, nella zona spazzata dalla staffa: va piegato subito lungo la parete in un canale, non lasciato libero.

### M-16 — importante — Frenafiletti sulla vite di una squadretta di plastica

Voce: D12 (con D3).

Problema. Il BOM destina il Loctite 243 alla "vite centrale delle squadrette" con la nota "solo vite su metallo". La vite entra sì nell'albero metallico, ma attraversa la squadretta scelta in D3, che è di plastica, e la testa appoggia sul suo mozzo. Il prodotto in eccesso finisce sulla squadretta e sul coperchio del servo.

Evidenza. Scheda tecnica Henkel del LOCTITE 243, letta da me: "This product is not normally recommended for use on plastics (particularly thermoplastic materials where stress cracking of the plastic could result). Users are recommended to confirm compatibility of the product with such substrates." [fonte primaria] https://datasheets.tdx.henkel.com/LOCTITE-243-en_GL.pdf . Le squadrette sono il pezzo che porta la coppia in tutti i 18 giunti e non hanno ricambi fuori dalle confezioni dei servo (M-04).

Correzione. Con la squadretta di plastica niente frenafiletti: la vite si controlla a ogni manutenzione, e il foro d'accesso nel braccio serve anche a questo. D12 resta in lista solo per la prova con la squadretta metallica D3-opz, una goccia sul filetto dell'albero e non sulla vite.

### M-17 — minore — Attrezzi e ordine degli acquisti

- Attrezzi mancanti: micrometro 0–25 mm (M-02); punte per inserti M2 / M2,5 / M3 per il saldatore; cacciavite a croce PH00 (viti di serie dei servo); punta o alesatore da 3,0 mm per ripassare i fori del perno; una morsa piccola per piantare cuscinetti e spine; bilancia da cucina (domanda 8 e M-07).
- Acquisto in due tempi: il report consiglia di "costruire una sola zampa completa" prima di tutto il resto. Comprare prima il necessario per una zampa (3 cuscinetti, spine, inserti, un regolatore) e ordinare il resto dopo la prova.

## Controllato e trovato corretto

- D1: F683ZZ 3 × 7 × 3 mm, flangia Ø8,1 × 0,8, carico statico 108–129 N, avviso sulla versione aperta da 2 mm: coincidono con `verifica_giunti_stampa.md` righe 4 e 5 (scheda NMB LF-730ZZ).
- Il cuscinetto sta dentro l'impronta della cassa: 5,925 − 4,05 = 1,875 mm di margine alla flangia, 2,425 mm all'anello esterno.
- Carico sul cuscinetto: momento di coxa 2,8 kgf·cm su appoggi distanti circa 37 mm → 0,275 N·m / 0,037 m = 7,4 N, più 4,3 N di carico della zampa; contro 108 N statici il margine è almeno 9.
- Niente inserto M2 sotto le alette (0,60 mm di parete contro 1,3): giusta la scelta di vite passante e dado.
- Inserti D4, D5, D6: lunghezze e confezioni coincidono con `verifica_giunti_stampa.md` riga 8; diametri marcati correttamente come stimati.
- Conteggi di base: 18 servo = 6 × 3; 18 cuscinetti, 18 spine, 18 squadrette (una per tipo in ogni confezione); 36 dadi per le alette ≤ 50; 2 regolatori, 2 elettrolitici e 2 coppie di cavi per i 2 lati della SSC-32; canali 0–8 e 16–24 = 9 + 9.
- A2: 62,6 × 28,3 mm, 67,5 con l'antenna, nessun foro: coincide con `verifica_esp32cam_camera.md`.
- A5: dimensioni e peso del pacco coincidono con `verifica_batteria_cablaggio.md`; 260 g nel bilancio è il valore raccomandato.
- B3: PCB 20,3 × 22,9 × 4,1 mm senza fori: coincide con `verifica_alimentazione.md`.
- D9: viti M2,5 per la SSC-32 (fori circa 2,9–3,0 mm): coerente con `verifica_ssc32.md` riga 8b; la domanda 2 chiede le misure giuste.
- Quote del servo in `dimensioni-componenti.md`: coerenti con la tabella A–F di Tower Pro; corretta la regola di disegnare le sedi sulle quote ufficiali.
- Statica: script rieseguito, 441 gf, 0,71 e 0,93 kgf·cm, escursioni 49° e 60°: come nel documento. Angolo interno del ginocchio in posa neutra 119,5° (da √(12² + 72²) = 73,0 mm, 34 e 50 mm), dentro il campo dichiarato.
- Escursioni usate (±23°, 49°, 60°) dentro i circa 90° che un servo dà con 1000–2000 µs e dentro i 145° del Savox.
- Tibia da 50 mm: servo più culla occupano 23,6 mm, restano 26,4 mm per il piedino.
- Creator 5: 256 mm di lato, PETG-CF, PLA-CF e TPU 95A fra i filamenti consigliati: coincide con `verifica_giunti_stampa.md`.
- Chiavi esagonali 1,5 / 2 / 2,5 mm: corrette per M2, M2,5 e M3 a testa cilindrica.
- Masse: 18 × 13,4 = 241 g; 2 × 15 = 30 g; differenza con gli Hobbywing 2 × 36 − 30 = 42 g.

## Non controllato

- Catena elettrica, fusibile, regolatori, livelli logici, pin dell'ESP32: fuori dalla lente meccanica.
- Prezzi, disponibilità, codici Amazon e AliExpress.
- Quote reali di squadrette, millerighe, vite centrale, fori delle alette: servono le misure dell'utente.
- Massa delle parti stampate (290 + 45 g): non verificabile prima del CAD.
- Peso e fori delle schede Pololu su fonte primaria: presi dal BOM e da `verifica_alimentazione.md`.
- Urti fra zampe vicine e fra tibia e corpo durante il passo: da fare nel CAD.
- Creep del PETG-CF sotto il precarico delle viti: nessun dato nelle note.
- Diametro dei fori delle squadrette di serie e massa del cuscinetto: valori miei di stima, non da fonte.

## Chiamate web

3 su 4 consentite.
1. Scheda tecnica Henkel LOCTITE 243 (PDF scaricato, testo estratto in locale e letto da me): avvertenza sulle plastiche, usata in M-16.
2. Linee guida hardware Espressif per l'ESP32-S3 (lette tramite estrazione automatica, citazioni non viste da me nel sorgente): 15 mm liberi attorno all'antenna dentro l'involucro, usate in M-09.
3. Guida filamenti Flashforge (PDF scaricato; i font sono incorporati senza testo, decodificati in locale con le loro tabelle: intestazioni di colonna e riga "Nozzle Size" leggibili, alcune lettere mancanti): ugello 0,6 / 0,8 mm per PLA CF e PETG CF, usata in M-11.
