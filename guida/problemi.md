# Registro dei problemi della guida (F5, arresto 2)

Registro unico dei problemi trovati scrivendo la guida di montaggio (D-075, `docs/piano-guida.md`). Unisce i 207 problemi dei file `guida/problemi/*.yaml` (fasi F3, F3b, F3c): lo stesso fatto registrato in più sezioni è una voce sola, con tutte le origini. Le prove complete stanno nei file d'origine, citati come `file#n` (n = posizione nel file, da 0) con il titolo.

Serve all'utente per decidere cosa correggere: CAD nella versione 2.1.7, documenti in `docs/`, testi della guida, acquisti, firmware, provini.

Stato di ogni voce:
- **aperto**: consiglio da approvare;
- **deciso**: c'è già un esito (campo `esito` del file d'origine), resta solo da fare o da verificare sul pezzo;
- **domanda**: serve una risposta dell'utente prima di decidere.

## Riepilogo

207 problemi registrati, 138 voci dopo l'unione dei doppioni.

| Tema | Bloccanti | Importanti | Minori | Totale |
|---|---:|---:|---:|---:|
| CAD (2.1.7) | 3 | 13 | 7 | 23 |
| BOM e acquisti | 1 | 2 | 12 | 15 |
| Elettronica e schemi | 2 | 19 | 6 | 27 |
| Documenti in `docs/` | 0 | 6 | 15 | 21 |
| Testi della guida (con immagini e impaginatore) | 0 | 8 | 25 | 33 |
| Firmware | 0 | 2 | 3 | 5 |
| Provini e misure | 0 | 5 | 9 | 14 |
| **Totale** | **6** | **55** | **77** | **138** |

Per stato: 74 aperte, 47 in attesa di una domanda, 17 decise (esito già approvato o applicato; 3 di queste hanno ancora una domanda). In tutto 50 voci contengono una domanda, riunite qui sotto in 37 domande.

I bloccanti:
- P-001: le spine del pacco non passano dalle fessure del tetto (CAD).
- P-002: la testata 2 × 8 non sta sotto la scheda del carapace, S-01 (CAD).
- P-003: le teste M3 del vassoio stanno 0,3 mm sotto la basetta, S-19 (CAD o viti a testa bassa).
- P-004: la squadretta di prova non è comprata (acquisto).
- P-005: interasse delle file dell'ESP32, 24,7 o 25,4, S-02 (misura).
- P-006: gli schemi mancavano; superato, resta la striscia dei partitori.

## Domande per l'utente

Ogni domanda dice quali voci sblocca. Sono cose da scegliere o da guardare sui pezzi, mai misure dei servo.

**Scelte**
- **Q-01** Va bene comprare ora una squadretta di prova (D3, domanda 4 del BOM)? AliExpress da 0,42 €, diymore da 10,99 € (6 pezzi, misure dichiarate) o tutte e due? Sblocca P-004, P-059, P-069, P-136.
- **Q-02** Scheda del carapace: preferisci spostarla (18 mm liberi sotto) o passare a una testata a 90° da comprare? Hai già una millefori tagliata e una testata 2 × 8? Sblocca P-002, P-067, P-075.
- **Q-03** Se il kit Temu non ha M3 × 6 a testa bassa, preferisci comprarle o spostare le viti del vassoio nel CAD? Sblocca P-003.
- **Q-04** Prese dei piedi e delle luci: un pettine a 3 poli per zampa o un connettore diverso? Hai già qualcosa in casa? Sblocca P-012, P-006, P-017.
- **Q-05** Approvi l'acquisto di 2 FSR 400 Short (X5) e di un tratto di striscia a 120 LED/m con buffer e resistenze (X9) per i provini 6 e 7? Sblocca P-021.
- **Q-06** Monti le luci nelle tibie? Se sì, diffusore bianco o fumé (dopo il provino di luce)? Sblocca P-077, P-062, P-063, P-064, P-138.
- **Q-07** Aggiungiamo un condensatore sulle prese delle luci delle tibie (voce nuova, pochi centesimi)? Sblocca P-074.
- **Q-08** Monti lo zaino con il computer di bordo? Se sì, da dove lo alimenti? Sblocca P-027.
- **Q-09** Il ToF posteriore lo preferisci avvitato (due fori nel carapace) o incollato? Sblocca P-008.
- **Q-10** Il vassoio dell'ESP32 va in PLA bianco (BOM E2) o in PETG? Sblocca P-088.
- **Q-11** Le lunette dei microfoni vanno in PLA nero o bianco? Sblocca P-078.
- **Q-12** Soglia del cicalino a 3,3 V per cella (ultimo livello) o a 3,5 V (come il firmware)? Sblocca P-066.
- **Q-13** Da quale assetto parte il robot a terra: 100/45 (punto di progetto) o più alto? Sblocca P-046.
- **Q-14** La prima prova della zampa sul corpo può aspettare la sezione 12 (batteria nel robot), o la vuoi prima con la batteria appoggiata fuori o con un alimentatore? Sblocca P-050.
- **Q-15** Vuoi una scorta di pezzi stampati (carapace, tibia, femore, piedini) o ristampi quando serve? Sblocca P-080.
- **Q-16** Il totale delle durate (0.23) va portato a circa 48 ore, o le durate delle sezioni 4 e 13 sono da rivedere? Sblocca P-111.

**Pezzi già in casa: da guardare o misurare**
- **Q-17** Batteria OVONIC: lunghezza del pacco con il calibro; il T-plug del pacco è femmina e quale lato è il +; che caricatore usavi con la v1 (carica bilanciata 2S, modalità storage), e caricavi il pacco fuori dal robot ogni volta? Hai un sacchetto per LiPo? Sblocca P-001, P-007, P-029, P-041.
- **Q-18** Scheda ESP32: con il calibro, distanza fra le due file di pin da centro a centro (prima di tutto); la sigla stampata (è la RE1.3?) e la serigrafia accanto ai pin 5V, GND, 3V3; con la sola USB collegata, i volt fra pin 5V e GND; a scheda spenta, la resistenza fra GPIO40 e 3V3; componenti sul lato inferiore oltre alla microSD; il connettore FPC ha la levetta e come stanno i contatti del flat (foto). Sblocca P-005, P-026, P-035, P-039, P-040, P-079, P-086.
- **Q-19** SSC-32: foto dei due lati con le scritte di ponticelli, morsetti e pin accanto alla morsettiera leggibili; i ponticelli sono a spina o saldati? Con il multimetro, VL− è collegato alle file di massa dei servo? Sblocca P-022, P-023, P-082.
- **Q-20** Kit Temu: misure degli inserti (diametro esterno e lunghezza di ogni misura), quanti per misura e se il kit è da 800 o da 500 pezzi; nel kit da 918 viti ci sono M3 × 6 a testa bassa (DIN 7984) o bombata (ISO 7380)? Che chiave serve alle M2 svasate nere? Sblocca P-003, P-057, P-058, P-112.
- **Q-21** Saldatore e stagno: hai una punta per inserti a temperatura regolabile? Che lega è lo stagno "a bassa temperatura"? Che temperatura consigliano le istruzioni per il 14 AWG? Sblocca P-058, P-079.
- **Q-22** Pulsante da 12 mm: ce l'hai? Diametro massimo dei contatti a saldare, ed è aperto a riposo? Sblocca P-010.
- **Q-23** Portafusibile impermeabile: lunghezza, larghezza, altezza e lati da cui escono i cavi. Sblocca P-011.
- **Q-24** Fili siliconici: diametro esterno del 14 AWG (previsto 3,3 mm) e dei 28 e 30 AWG di FSR e luci. Sblocca P-028, P-063.
- **Q-25** Hai in casa nastro Kapton, colla a caldo o biadesivo sottile? Sblocca P-072, P-008.
- **Q-26** Attrezzi: hai un tester dei servo a manopola, un alimentatore da banco regolabile con limite di corrente, una bilancia da almeno 5 kg e un termometro a infrarossi? Sblocca P-070, P-071, P-117, P-050.
- **Q-27** Nel set di resistenze B10 c'è il 22 kΩ? Sblocca P-024.
- **Q-28** Su un MG996R appena aperto: i gommini sono già nelle alette? Ci sono tubetti di ottone dentro? Sblocca P-134.
- **Q-29** Con la v1, ogni quanto dovevi stringere le viti o sostituire un servo? Sblocca P-101.

**Quando arrivano i pezzi o al banco**
- **Q-30** INA260: il 14 AWG entra nella morsettiera? Sblocca P-025.
- **Q-31** Traslatore KAmod: foto dei due lati con le scritte dei pin. Sblocca P-033.
- **Q-32** ADS7830: quote dei due fori di fissaggio e altezza dei pin. Sblocca P-017.
- **Q-33** Pololu VL53L7CX: diametro e posizione dei fori. Sblocca P-018.
- **Q-34** Cicalino BX100: lunghezza, larghezza, altezza, lato dei pin della presa di bilanciamento, posizione del display. Sblocca P-066, P-132.
- **Q-35** Al banco, con la 2813 accesa: volt fra il pin A e la massa, e fra il B e la massa. Sblocca P-037.
- **Q-36** Striscia LED e FSR: hanno l'adesivo sul retro? Sblocca P-138.
- **Q-37** Dopo il provino delle tasche: quanta forza serve per togliere la lama A, e si impugna bene? Sblocca P-135.

## Decisioni in blocco

Gruppi di consigli che si possono approvare con un sì solo. Le domande delle voci restano valide; ogni voce sta in un solo gruppo. Le voci fuori dai gruppi (i bloccanti e quelle con una scelta vera) vanno decise una per una.

1. **Correzioni di testo ai documenti in `docs/`** (nessuna scelta di progetto): P-043, P-087, P-089, P-090, P-091, P-092, P-093, P-094, P-096, P-099, P-100, P-102.
2. **Testi della guida già cambiati dalla riconciliazione F3c** (approvazione a posteriori): P-047, P-051, P-052, P-053, P-084, P-104, P-107, P-109, P-110, P-114.
3. **Altre correzioni di testo della guida**: P-026 (regola "mai USB e batteria" e 12.07), P-031, P-036, P-045, P-048, P-054, P-103, P-105, P-106, P-108, P-113, P-115, P-116, P-118, P-123, P-124.
4. **Modifiche CAD della 2.1.7 senza scelte aperte**: P-009, P-014, P-015, P-016, P-019, P-057 (blocco del provino degli inserti), P-062, P-065.
5. **Catalogo delle giunzioni e BOM (viteria, conteggi, codici)**: P-020, P-068, P-069, P-073, P-075, P-076, P-085.
6. **Scelte degli schemi elettrici, come proposte**: P-024, P-028, P-030, P-032, P-034, P-035, P-038, P-039.
7. **Firmware e strumenti, nella roadmap S1-S3**: P-055, P-056, P-127, P-128, P-129.
8. **Impaginatore e immagini (F7)**: P-119, P-120, P-121, P-122, P-125, P-126.
9. **Provini e misure sul primo esemplare**: P-042, P-059, P-060, P-061, P-095, P-130, P-131, P-132, P-133, P-136, P-137.

## Caso di controllo

`docs/piano-guida.md`, "Contesto", elenca 8 incongruenze note prima della guida. Risultato: 4 trovate, 1 in parte, 3 non trovate.

| Incongruenza nota | Nel registro |
|---|---|
| Viti della squadretta di coxa: M3 × 6 con rondella o M3 × 5 senza | sì, P-069 (D-048 contro D-049, riga 107 del BOM) |
| Viti della SSC-32: pilota M2,5 o inserti M2 | no |
| Distanziali del vassoio: 5 o 10 | no (P-003 parla delle viti sui distanziali, non della loro altezza) |
| Inserti M3 del corpo: 28 o 30 | sì, P-087 |
| Pulsante: Dupont o IDC | no (P-010 e P-037 riguardano il pulsante, non il connettore) |
| Vassoio: PETG o PLA | sì, P-088 |
| Perno della coxa | in parte: P-044 (montaggio della coxa con il perno che sporge 5 mm) e P-059 (forzamento del perno); la lista non dice quale fosse l'incongruenza |
| Viti lato coda del servo di coxa: procedura solo nella ricerca | sì, P-047 |

Anche i 5 candidati problema della stessa sezione sono nel registro: vite d'aletta del femore sotto Femore_A (P-048), calettamento senza riferimento (P-015), provini di inserti, piedino e giunto (P-057, P-016, P-059), schemi di basetta e carapace (P-006), slitta destra (P-100).

---

## Bloccanti

### P-001 Le spine del pacco non passano dalle fessure del tetto: il pacco non si toglie per la carica
- **Gravità e tema**: bloccante · CAD (2.1.7)
- **Dove**: 11.03, 11.04, 15.04, 15.05, ogni cambio della batteria. `batteria#0` «Le spine del pacco non passano dalle fessure del tetto...»; `smontaggio#1` «Il cambio della batteria dipende dal problema bloccante di 11.03...».
- **Cosa**: i cavi del pacco salgono al T-plug (sopra F1) solo dalle due fessure del tetto, 13 × 4,5 mm, chiuse verso la coda da un ponte di 2 mm. La spina T-plug (circa 30 × 16 × 8,5 la coppia) e la JST-XH di bilanciamento (circa 10 × 5,8) non passano da 4,5 mm: il pacco non si sfila per caricarlo come dice D-054. La verifica di D-051 riguardava solo la scatola, senza cavi.
- **Opzioni**: (1) fessure aperte verso la coda, togliendo il ponte da 2 mm (da verificare con la fascetta di F1, D-055, e la rigidezza del tetto); (2) una fessura larga quanto la spina (circa 17 × 9) accanto a F1; (3) caricare il pacco dentro il robot, nessuna modifica; (4) prolunga di bilanciamento infilata prima di saldare (solo il bilanciamento).
- **Consiglio**: fessure aperte verso la coda nella 2.1.7, provate con la spina vera. Intanto 11.03 fa provare a secco e fermare se la spina non passa; la sezione 15 (cambio batteria) segue la stessa scelta.
- **Stato**: domanda.
- **Domanda**: con la v1 caricavi il pacco fuori dal robot, ogni volta?

### P-002 La testata 2 × 8 con la spina IDC non sta sotto la scheda del carapace (S-01)
- **Gravità e tema**: bloccante · CAD (2.1.7)
- **Dove**: 4.06, 4.22-4.25, 13.16, 13.17, 13.19, A.17, A.18; `guida/schemi/scheda_carapace.svg`. `schemi#0` (S-01) «La testata 2 x 8 con la spina IDC non sta sotto la scheda del carapace»; `carapace#0` «La posizione della testata 2 x 8 ... è bloccata da S-01»; `banco#14` «Scheda del carapace: anche ponticelli e fili 101-112 aspettano S-01...».
- **Cosa**: sotto la scheda (faccia alta a z 30,9) c'è l'ESP32 fino a z 20,8: restano circa 10 mm. Testata dritta più spina IDC fanno 16-18 mm; il CAD le dà 9 (sch_sp, S). Una testata a 90° copre le viti di coda o quasi tutta la scheda. I collegamenti dello schema valgono, la posizione della testata no; ponticelli e fili 101-112 si saldano sui pin di J2, quindi al banco si fanno solo taglio, fori e CE1 (anche il taglio dipende da S-01).
- **Opzioni**: (1) CAD 2.1.7: scheda fuori dall'ingombro dell'ESP32 o cose sotto più basse, 18 mm liberi; (2) CAD 2.1.7: testata a 90° con chiave (da comprare) sul bordo verso l'ottagono, viti di coda a |y| ≥ 15, scheda allargata; (3) testata piegata dalla strip in casa, chiave togliendo il pin 14 (costo zero, protezione parziale).
- **Consiglio**: opzione 1 o 2 nel CAD prima di stampare il carapace; nel CAD anche qualche foro libero in più. Fino ad allora 4.06 e 13.16-13.17 non fanno saldare J2 (marcati [C]); 13.16 deve riportare le prove 6 e 8 di schemi.md 2.6.
- **Stato**: domanda.
- **Domanda**: preferisci spostare la scheda del carapace (più spazio sotto) o passare a una testata a 90° da comprare? Hai già una millefori tagliata per la scheda e una testata 2 × 8 dritta o a 90°?

### P-003 Le teste M3 del vassoio stanno 0,3 mm sotto la basetta, sotto tre pin dell'ESP32 (S-19)
- **Gravità e tema**: bloccante · CAD (2.1.7)
- **Dove**: 4.04; schemi.md 1.0; `basetta_saldature.svg` (zone rosse). `schemi#18` (S-19).
- **Cosa**: quattro M3 × 6 DIN 912 (testa 5,5 × 3) a (30; ±12,5) e (75; ±12,5): teste a z 5,6, basetta da z 5,9. Sotto le teste cadono T-2 (3V3), D-12 (GPIO21, TX verso la SSC-32) e al limite B-2 (GPIO14), tutti necessari; una saldatura è alta 0,5-1 mm e una testa sotto C-12 e D-12 li unirebbe.
- **Opzioni**: (1) teste basse: DIN 7984 (lascia 1,3 mm) o ISO 7380 (1,65 mm), più Kapton sulle teste, code tagliate a filo, giunti piatti; (2) CAD 2.1.7: viti del vassoio fuori dalla basetta (|y| > 17,5 o x fuori da 22-78) o colonnine più alte (cor_bas_luce).
- **Consiglio**: opzione 1 se il kit Temu ha M3 a testa bassa (già fra le cose da guardare in `CLAUDE.md`), altrimenti opzione 2. Le zone vietate dello schema valgono in tutti e due i casi.
- **Stato**: domanda.
- **Domanda**: nel kit Temu da 918 viti ci sono M3 × 6 a testa bassa (DIN 7984) o bombata (ISO 7380)? Se no, preferisci comprarle o spostare le viti del vassoio nel CAD?

### P-004 La squadretta di prova non è comprata: senza le sue quote non si prova il giunto né si stampa la zampa
- **Gravità e tema**: bloccante · BOM e acquisti
- **Dove**: 1.04, 1.09, 1.10, 1.18. `provini#1`.
- **Cosa**: la squadretta a 25 denti (D3) è da comprare (domanda 4 del BOM aperta). Le sue quote (sq_d 20, sq_sp 2,5, sq_h 5,5, sq_mozzo_d 9, sq_fori_pcd 14, sq_fori_d 3) sono tutte C, da rivenditori discordanti; sq_h e sq_sp spostano lungo Y tutti i pezzi della zampa (zy_orlo, zy_disco, zy_A_est). Il provino 4 e la chiusura della sezione 1 aspettano la misura.
- **Opzioni**: (1) 1-2 squadrette AliExpress da 0,42 € (misure non dichiarate); (2) diymore 10,99 € per 6, con Ø20 e fori M3 a 14 dichiarati; (3) tutte e due.
- **Consiglio**: una AliExpress e una confezione diymore; si misura la prima che arriva e le quote vanno nel CAD prima della zampa.
- **Stato**: domanda.
- **Domanda**: va bene comprare ora una squadretta di prova (D3, domanda 4 del BOM)? Quale: AliExpress da 0,42 € o diymore da 10,99 €?

### P-005 Interasse delle due file di pin dell'ESP32: 24,7 nel CAD, 25,4 sulla millefori (S-02)
- **Gravità e tema**: bloccante · elettronica e schemi
- **Dove**: 4.04; `basetta.svg` righe 2 e 12. `schemi#1` (S-02).
- **Cosa**: sulla millefori le strip femmina stanno solo a multipli di 2,54: lo schema le mette a 25,4 (standard DevKitC). Il CAD usa 24,7 (esp_file, C, letto sul disegno del venditore). Se la scheda vera è a 24,7 non entra (0,7 mm di troppo) e lo schema della basetta va rifatto.
- **Opzioni**: (1) misurare centro-centro sui pin prima di tagliare la basetta; (2) se 25,4: schema valido, esp_file a 25,4 nella 2.1.7 e D-053 corretta (|y| 12,7); (3) se 24,7: strip su due striscioline separate, collegate con fili, schema da rifare.
- **Consiglio**: misurare per prima cosa: è la quota da cui dipende tutta la basetta.
- **Stato**: domanda.
- **Domanda**: con il calibro, quanto misura la distanza fra le due file di pin dell'ESP32, da centro a centro?

### P-006 Gli schemi della basetta e della scheda del carapace non esistevano (resta la striscia dei partitori)
- **Gravità e tema**: bloccante (in origine) · elettronica e schemi
- **Dove**: 4.04-4.25, 8.10-8.26, 13.16, appendici. `banco#0` «Gli schemi della basetta e della scheda del carapace non esistono»; `elettronica#0` «Gli schemi della basetta, della striscia dei partitori e della scheda del carapace non esistono»; `riconciliazione#13` «Gli schemi elettrici non esistono: l'appendice non ha i passi con le figure».
- **Cosa**: la prima F3b non aveva prodotto niente e le sezioni 4, 8 e 13 davano solo tabelle di collegamento [C]. Gli schemi F3b del 12 ottobre (`guida/schemi/schemi.md`, `basetta*.svg`, `scheda_carapace*.svg`) e le pagine A.15-A.19 li hanno sostituiti. Resta senza schema la **striscia dei partitori** dei sei FSR e delle due NTC (8.10, X5), che nel CAD non ha un posto (vedi P-017 e P-012).
- **Opzioni**: (1) schema della striscia dei partitori con il prossimo giro degli schemi; (2) fissare i punti sul primo esemplare costruito e disegnarli dopo.
- **Consiglio**: opzione 1, insieme alle prese dei piedi (P-012).
- **Stato**: deciso per basetta e scheda del carapace (esito: superato dagli schemi F3b; restano S-01, S-02, S-19 = P-002, P-005, P-003); aperto per la striscia dei partitori.

---

## Importanti

### P-007 La schiuma dello sportello non basta a premere il pacco, e le fonti non dicono dove va
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 11.02, 11.05. `batteria#1`.
- **Cosa**: fra la battuta anteriore del tunnel (X 79) e la punta dei rebbi (X -68,4) ci sono 147,4 mm; il pacco è lungo 137-139 (V): restano 8,4-10,4 mm. La schiuma EVA del BOM (D10) è da 3 mm: con uno strato il pacco scorre di 5-7 mm. D-051 e corpo.py non dicono dove va la schiuma; la bozza mette 3-4 strati sulla faccia anteriore del pacco [C].
- **Opzioni**: (1) strati sulla faccia anteriore, CAD invariato; (2) rebbi più lunghi nella 2.1.7 (cor_sport_rebbio da 17 a circa 22) sul pacco misurato, per un solo strato; (3) tasselli di schiuma sulle punte dei rebbi (poco stabili).
- **Consiglio**: misurare il pacco e allungare i rebbi nella 2.1.7; intanto gli strati sulla faccia anteriore.
- **Stato**: domanda.
- **Domanda**: quanto è lungo il tuo pacco OVONIC, misurato con il calibro?

### P-008 Altoparlante, microfoni e ToF posteriore non hanno un fissaggio definito
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 13.09, 13.11-13.13. `carapace#1`.
- **Cosa**: l'altoparlante Ø15 sta fra due guide e un fermo davanti, dietro niente (sporge 3,3 mm); i microfoni poggiano sull'anello attorno al foro Ø1 senza ritegno verso il dorso, e la guarnizione di D-066 non ha materiale né voce del BOM; il ToF posteriore ha solo il piano inclinato a 35°, senza fori né perni (predisposizioni.md diceva "due perni o un inserto M2"). La bozza dice colla a caldo o biadesivo [C], fuori dal percorso del suono.
- **Opzioni**: (1) colla a caldo o biadesivo, reversibili; (2) due fori Ø1,7 per viti M2 (o perni) sul piano del ToF, nella 2.1.7; (3) linguetta o due costole dietro l'altoparlante, nella 2.1.7.
- **Consiglio**: ora colla o nastro, un punto solo fuori dal suono; nella 2.1.7 viti del ToF e ritegno dell'altoparlante.
- **Stato**: domanda.
- **Domanda**: hai colla a caldo o biadesivo sottile in casa? Il ToF posteriore lo preferisci avvitato (due fori nel carapace) o incollato?

### P-009 La catena LED non ha un percorso disegnato fra i lobi; il README dice un pixel per sede del fondo dell'anello
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 13.04, 13.08, 2.19. `carapace#4` «La catena LED non ha un percorso disegnato fra i lobi...»; `stampa#4` «Il README dice un pixel nelle sedi del fondo dell'anello, D-068 ne mette due».
- **Cosa**: cablaggio.md 3.5 fa correre la catena nei ganci sotto il dorso (x -40, 0, 40), ma fra l'ultimo gancio e un lobo d'angolo (x ±94,7) ci sono circa 55 mm senza ganci e il passaggio davanti non ne ha. Tratti in linea retta 76-105 mm; la bozza fa tagliare 20 mm in più [S]. `cad/stl/README.md` (Corpo_Fondo_Anello) dice ancora un pixel per sede (D-067, 60 LED/m); D-068 (120 LED/m) ne mette due, quattro in tutto come X11.
- **Opzioni**: (1) cavo con un'ansa a ogni lobo, nastro dove mancano i ganci (bozza); (2) ganci in più nel carapace (x ±75 e davanti), 2.1.7; (3) README corretto in "due pixel per sede".
- **Consiglio**: bozza per ora; ganci in più e README corretto nella 2.1.7.
- **Stato**: aperto.

### P-010 I contatti del pulsante potrebbero non passare dal foro del fondo, e il pulsante può essere normalmente chiuso
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 13.02, 13.05, 13.06. `carapace#3`.
- **Cosa**: il fondo dell'anello ha un foro Ø12,2 e si infila dal basso sul corpo del pulsante; se le linguette a saldare sporgono oltre Ø12,2 il fondo non passa. Il BOM (B3b) dice "NO o NC non dichiarato": la 2813 vuole un contatto aperto a riposo. La bozza fa misurare il pulsante in 13.02.
- **Opzioni**: (1) misurare il pulsante vero prima di stampare il fondo; (2) fondo diviso o con foro a chiave nella 2.1.7; (3) saldare i fili prima del fondo e infilarlo da sopra (cambia l'ordine).
- **Consiglio**: misurare adesso; se le linguette passano la bozza resta.
- **Stato**: domanda.
- **Domanda**: hai già il pulsante da 12 mm? Diametro massimo dei contatti a saldare, ed è aperto a riposo?

### P-011 Sedi di Wago e portafusibile costruite su misure stimate, con 0,2 mm di gioco
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 7.07, 7.11. `corpo#2`.
- **Cosa**: le sedi dei Wago 221-415 (29,9 × 18,6 × 8,3, S, scheda di terzi) e le costole del portafusibile (luce 22,4 = 22 + 2 × 0,2; ATO in linea 40 × 22 × 15, "stima") sono tagliate su misure non verificate. Il portafusibile in casa è un impermeabile 30 A con cavo 14 AWG (D-073, B5), senza misure; i Wago non sono comprati. Più largo di 22,4 non entra; più lungo di 40 finisce su fessure e spie.
- **Opzioni**: (1) misurare portafusibile e un Wago prima di stampare la base e correggere i parametri; (2) provino della sola zona; (3) portafusibile solo con la fascetta, senza costole.
- **Consiglio**: misurare prima di stampare la base; nel passo c'è una prova a secco con il calibro. Il portafusibile va aggiunto ai pezzi in casa da guardare in `CLAUDE.md`.
- **Stato**: domanda.
- **Domanda**: puoi misurare con il calibro il portafusibile impermeabile in casa (lunghezza, larghezza, altezza) e dire da quali lati escono i cavi?

### P-012 Prese dei piedi e delle luci: forma, fissaggio, poli e ordine non definiti
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 7.10, 9.09, 10.02. `corpo#3` «Prese dei piedi e delle luci, file da sei spine JR...»; `zampa_corpo#4` «Spine di FSR e luci dalle prolunghe avanzate, ordine delle prese e poli non scritti».
- **Cosa**: nel CAD due file da sei spine JR a passo 2,54 (Rif_Prese_Piedi, 15,5 × 2,6 × 8,5, S), ma una spina JR è spessa 2,75: sei affiancate non stanno in 15,5. Nessun pezzo nel BOM (X5 elenca le spine femmina dalle prolunghe C5), niente su come la fila si tiene nella scanalatura, né su come i contatti vanno a partitori, ADS7830 e 5 V dei LED. Servono 12 contatti per gli FSR e 18 per le luci. cablaggio.md 3.3 non dice quale polo resta libero sulla presa dei piedi né da che capo parte l'ordine AS...PD (C); le prolunghe avanzate sono 16 per 12 spine.
- **Opzioni**: (1) progettare le prese come un pezzo (millefori con pettine 6 × 3 e fili), insieme agli schemi; (2) spine JR sciolte sul tetto finché le zampe non sono montate; (3) togliere le prese e portare gli FSR alla basetta con un connettore piccolo.
- **Consiglio**: progettarle con il prossimo giro degli schemi, insieme alla striscia dei partitori (P-006, P-017), con la misura vera della spina JR; poli e ordine in cablaggio.md. Fino ad allora 7.10 le posa senza fissarle ("anche dopo").
- **Stato**: domanda.
- **Domanda**: come vuoi fare le prese dei piedi e delle luci: un pettine a 3 poli per zampa o un connettore diverso? Hai già qualcosa in casa?

### P-013 Come si premono i cuscinetti nella culla del ginocchio e nelle gondole, e come si tiene la base
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 6.02, 7.03, 7.04. `zampa#2` «Come si preme il cuscinetto del ginocchio»; `corpo#1` «Come si tiene la base per premere i cuscinetti e avvitare la chiglia».
- **Cosa**: il cuscinetto LF-1050ZZ entra forzato (cus_sede_d dal provino). Nella tibia una morsa piana non va (lato A aperto, lato B preme flangia e anello interno insieme). Nella base la flangia sporge 0,8 sotto il fondo: sul piano la base poggia sulle sei flange e nessuna fonte dice come tenerla sollevata; dopo la chiglia restano 8,65 mm e il cuscinetto non si preme più. Le viti della chiglia entrano da sotto, con la base capovolta sulle colonnine del tetto.
- **Opzioni**: (1) sede tarata sul provino per il pollice; (2) tubetto sulla sola flangia (Ø est. ≤ 11,5, int. ≥ 8) e distanziale; (3) attrezzo stampato nella 2.1.7 (bussola e distanziale), lo stesso per tibie e corpo; (4) base su due listelli di circa 20 mm, capovolta su un panno per la chiglia.
- **Consiglio**: sede tarata per il pollice; se non basta, l'attrezzo stampato della 2.1.7. Listelli e panno nel passo, marcati [C].
- **Stato**: deciso per la tibia (esito di `zampa#2`: consiglio approvato l'11 ottobre 2026, modifiche nella 2.1.7); aperto per la base.

### P-014 La testa della vite del guscio appoggia su una faccia inclinata di circa 12,6°
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 6.23. `zampa#3`.
- **Cosa**: la M3 × 10 del guscio entra dal fronte; sotto la testa Ø5,5 il fronte scende di 1,23 mm (pendenza 0,22-0,23), senza lamatura: la testa tocca solo sul bordo alto. Il controllo "lunghezze" trova la punta 0,03 mm oltre il fondo, ma con l'appoggio vero resta circa 0,95 mm sopra; se il PLA cede di 1 mm la vite tocca. È l'unico ritegno lungo +X.
- **Opzioni**: (1) lamatura piana Ø6 sul fronte; (2) vite M3 × 8 (BOM: M3 × 8 da 106 a 112, M3 × 10 da 18 a 12); (3) testa svasata o rondella sagomata.
- **Consiglio**: lamatura piana nella 2.1.7; intanto "stringi piano".
- **Stato**: deciso (esito: consiglio approvato l'11 ottobre 2026, modifiche nella 2.1.7).

### P-015 Il calettamento a α +20° e γ 100° non ha un riferimento sul pezzo
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 6.16, 6.17. `zampa#15`.
- **Cosa**: le fonti fissano il calettamento (1500 µs con α +20°, γ 100°) ma non come si riconoscono gli angoli: la guida li fa tenere a occhio [C]. Con 25 denti si resta entro ±7,2° se la posa è giusta, fino a circa ±12° se si sbaglia. Con −7,2° sul ginocchio la corsa arriva a 172,8°, sotto i 177° del limite del firmware; margine del ginocchio a 180°: 0°.
- **Opzioni**: (1) dima del calettamento stampata nella 2.1.7, come Dima_Posa_1 ma con i denti a α +20°, γ 100°; (2) goniometro di carta 1:1 in appendice; (3) calettare con Dima_Posa_1 (α 0°, γ 90°) e cambiare il calettamento in robot.yaml.
- **Consiglio**: dima del calettamento nella 2.1.7; intanto a occhio [C]. Guardare anche il margine del ginocchio a 180°.
- **Stato**: aperto.

### P-016 La stretta del piedino non ha un parametro né le varianti da provare
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 1.14, 2.12. `provini#3`.
- **Cosa**: D-064 e il README chiedono di tarare la stretta con 0, −0,2 e −0,4 mm, ma nel CAD non c'è un parametro (solo pied_tacca) e c'è un solo Piedino.stl, a stretta zero: il provino 6 ha un solo valore.
- **Opzioni**: (1) parametro pied_stretta e tre STL nella 2.1.7; (2) variare la correzione dei fori nello slicer; (3) solo il valore zero, scelta dopo la prova dell'FSR.
- **Consiglio**: opzione 1: la stretta decisa deve stare nel CAD.
- **Stato**: aperto.

### P-017 L'ADC non ha giunzione né viti, e la striscia dei partitori non ha un posto
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 8.09, 8.10, 8.22. `elettronica#4`.
- **Cosa**: la base ha due bugne con inserti M2 per l'ADS7830, ma il catalogo non ha la giunzione e il BOM dice "viti M2 corte" senza lunghezza; i fori dell'ADS7830 sono C (X6). La striscia dei partitori non ha posto nel CAD: il vano sotto il vassoio (37 × 32 × 10,4) è contato per IMU e ADC. Nell'immagine 8.08 l'ADC è senza viti.
- **Opzioni**: (1) giunzione `adc` (M2 × 5) quando i fori sono noti; (2) partitori in una sede nel vassoio o sul bordo della basetta, nella 2.1.7.
- **Consiglio**: aspettare il pezzo, poi la giunzione; la striscia si disegna con il suo schema (P-006).
- **Stato**: domanda.
- **Domanda**: hai già l'ADS7830? Servono le quote dei due fori di fissaggio e l'altezza dei pin.

### P-018 ToF e camera senza ritegno modellato
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 8.13, 8.28. `elettronica#5`.
- **Cosa**: il ToF sta in una sede inclinata con 0,2 mm di gioco, senza perni né viti (la predisposizione diceva "due perni Ø1,9 o due inserti M2", C). La testa della camera è solo posata fra torretta e mensola; davanti la ferma la visiera, a 0,9 mm dalla lente. La cima del ToF passa 0,2 mm sotto la testa della camera: la guida monta il ToF prima.
- **Opzioni**: (1) posati come nel CAD; (2) goccia di colla a caldo dal lato non ottico; (3) perni o inserti M2 nella mensola, nella 2.1.7.
- **Consiglio**: prova a secco sul primo vassoio; se balla, colla a caldo.
- **Stato**: domanda.
- **Domanda**: come sono i fori del Pololu VL53L7CX (diametro e posizione)?

### P-019 L'asola del bus sta sotto il bordo della basetta, e la spina Qwiic dell'ADC deve passarci
- **Gravità e tema**: importante · CAD (2.1.7)
- **Dove**: 4.16, 8.07, 8.09, 8.11, 8.12. `elettronica#13`.
- **Cosa**: l'asola del vassoio (x 47-53, y 13-16) sta 1,5 mm sotto il bordo della basetta (y 17,5). I fili del ramo 3 passano sotto la basetta nei 3,3 mm dove stanno saldature e teste M3 (P-003); una spina JST SH a 4 poli in un'asola 6 × 3 non è verificata.
- **Opzioni**: (1) provare la spina sul vassoio stampato, altrimenti cavetto saldato sull'ADC; (2) asola spostata a |y| ≥ 18 e allargata a 7 × 4 nella 2.1.7.
- **Consiglio**: opzione 2 nella 2.1.7; fino ad allora la 1.
- **Stato**: aperto.

### P-020 Vite della slitta con il supporto dell'INA260: lunghezza e accesso
- **Gravità e tema**: importante · BOM e acquisti
- **Dove**: 4.14, 4.34, 8.01, 8.03. `banco#4` «Con i supporti degli INA260 la vite M3 della slitta deve essere più lunga...»; `elettronica#1` «Vite delle slitte con il supporto dell'INA260, lunghezza e accesso»; `riconciliazione#3` «INA260: il supporto si posa sulla slitta al banco (4.14), l'INA260 si avvita nel corpo (8.03)».
- **Cosa**: con il supporto la testa della M3 si alza di 2,4 mm: M3 × 8 ha 3,2 mm di presa, M3 × 10 ne ha 5,2 (senza supporto M3 × 8: 5,6). Il catalogo disegna sempre M3 × 8 e il BOM non conta le due M3 × 10 in più. Con l'INA260 avvitato sopra la vite non si raggiunge (fessura di 6,1 mm). La riconciliazione ha già spostato l'INA260 in 8.03: in 4.14 si posa solo il supporto.
- **Opzioni**: (1) M3 × 10 con X7 e M3 × 8 senza, giunzione per variante (BOM: M3 × 8 104, M3 × 10 20); (2) M3 × 8 con 3,2 mm di presa; (3) seconda vite o foro d'accesso nel supporto (2.1.7).
- **Consiglio**: opzione 1, con l'ordine già applicato (vite stretta prima dell'INA260); catalogo e BOM da aggiornare.
- **Stato**: aperto (la domanda di `elettronica#1` sull'ordine è superata dalla riconciliazione).

### P-021 I provini di luce e del piedino chiedono un programma di banco e pezzi non approvati
- **Gravità e tema**: importante · BOM e acquisti
- **Dove**: 1.15, 1.17. `provini#4`.
- **Cosa**: il provino 7 vuole 3 pixel comandati dall'ESP32 su GPIO48 e il 6 un FSR 400 Short con il doppino. Il firmware non ha codice per i pixel (vedi P-055); FSR (X5) e striscia a 120 LED/m (X9) sono predisposizioni approvate nel CAD ma non per l'acquisto.
- **Opzioni**: (1) programma di banco S1 con un comando per N pixel; (2) tester di strisce WS2812 comprato; (3) un pixel diretto da un pin senza buffer (livello a 3,3 V da valutare).
- **Consiglio**: programma S1 prima del provino 7; acquisti X5 e X9 approvati con il BOM.
- **Stato**: domanda.
- **Domanda**: approvi l'acquisto di 2 FSR 400 Short (X5) e di un tratto di striscia a 120 LED/m con buffer e resistenze (X9) per i provini 6 e 7?

### P-022 La SSC-32 clone non è mai stata vista: ponticelli, micro-USB, retro e lato dei canali dal disegno del venditore
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.01, 4.02, 4.29. `banco#2`.
- **Cosa**: posizioni dei ponticelli "VS VL" e "VS1 VS2", della micro-USB, dei morsetti e delle file vengono dal disegno quotato del venditore [S]; il retro non è fotografato. Non si sa se la micro-USB alimenta la logica, se il clone risponde a VER, Q, QP e a 115200, se i ponticelli sono a spina o saldati. Le etichette "Canali 0-15 / 16-31" di 4.01 sono quelle del CAD, non verificate (vedi P-081).
- **Opzioni**: (1) foto della scheda dai due lati e guida corretta; (2) guida com'è, con [S] e [C].
- **Consiglio**: chiedere le foto prima di portare la sezione all'utente; se la micro-USB non alimenta la logica, VL dalla 2813 (già in 4.09).
- **Stato**: domanda.
- **Domanda**: puoi fotografare la SSC-32 dal lato componenti e dal retro, con le scritte dei ponticelli, dei morsetti e dei pin accanto alla morsettiera leggibili, e dire se i ponticelli sono a spina o saldati?

### P-023 Seriale della SSC-32: tre o quattro fili, e dove va VL
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 8.17, 8.19. `elettronica#6`.
- **Cosa**: cablaggio.md 3.6 dice "4: TX, RX, massa, VL" con Dupont, e 3.1 "VL con un Dupont (C4)". VL è l'alimentazione della logica (6-8,4 V) e non viaggia su un pin di segnale; il disegno del venditore dà tre pin RX, TX, GND e i morsetti VL+ e VL- (S, C). Non è scritto da dove il traslatore prende il 5 V del lato alto. La guida scrive tre fili sui pin e VL ai morsetti [C].
- **Opzioni**: (1) leggere le sigle sul clone e confermare tre pin più i morsetti VL; (2) se il clone ha un pin 5 V, prendere da lì il lato alto del traslatore.
- **Consiglio**: verificare al banco e aggiornare cablaggio.md 3.6 a tre fili.
- **Stato**: domanda (la stessa foto di P-022).

### P-024 Abilitazione dei D42V110F6: ENA tirato a VIN, R3 da 22 kΩ su ogni regolatore
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.12, 4.18, 4.31, 4.32, 8.19, 12. `banco#3` «Il pin di abilitazione dei regolatori può avere un pull-up interno...»; `schemi#4` (S-05) «Abilitazione dei D42V110F6: ENA tirato a VIN con circa 500 kOhm...».
- **Cosa**: il progetto tirava EN a massa con 47 kΩ per avere il rail spento di default. La pagina Pololu (riletta il 12 ottobre) dice ENA tirato a VIN con 1 MΩ, più ENB con 1 MΩ e 10 kΩ verso ENA: circa 500 kΩ. Con una R3 da 22 kΩ per regolatore l'ENA sta a 0,35 V a batteria piena (47 kΩ: 0,72 V; una R3 sola per due regolatori: 1,3 V). Con GPIO42 alto l'ENA è a 2,6 V, sopra i 2 V chiesti. La soglia bassa non è pubblicata.
- **Opzioni**: (1) R3 da 22 kΩ su ogni regolatore; (2) 47 kΩ solo se la prova 4.32 lo permette.
- **Consiglio**: 22 kΩ su tutti e due; prova 4.32 con ogni regolatore, R3 e D2 in linea: con GPIO42 basso o staccato l'uscita è a 0 V.
- **Stato**: deciso (esito di `banco#3`: ripreso dagli schemi, R3 da 22 kΩ in 4.31, D2 in 4.18, prova in 4.32); resta la domanda.
- **Domanda**: nel set di resistenze B10 c'è il valore 22 kΩ? Serve una seconda R3.

### P-025 La morsettiera dell'INA260 potrebbe non prendere il 14 AWG del rail dei servo
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.11, 4.31, 4.34, 8.03. `banco#6` «La morsettiera dell'INA260 potrebbe non prendere il 14 AWG del rail dei servo»; `elettronica#3` «La morsettiera dell'INA260 potrebbe non prendere il 14 AWG».
- **Cosa**: il rail porta fino a 13 A su 14 AWG (D-073); la morsettiera da 3,5 mm dell'INA260 potrebbe prendere al massimo 16 AWG, e allora "l'ultimo tratto si salda". Al banco (4.31) i fili d'uscita si saldano sul regolatore da 0,6 m (S): se poi passano dall'INA260 vanno tagliati e rifatti. Non è scelto chi taglia né dove si salda; non è noto se i pad dell'INA260 reggono 13 A.
- **Opzioni**: (1) fili d'uscita lunghi al banco, e nella sezione 8 con X7 un tratto da 16 AWG sulla morsettiera; (2) INA260 in linea già al banco; (3) fili sempre saldati sui pad.
- **Consiglio**: fili lunghi al banco; provare la morsettiera con un 14 AWG appena arriva l'INA260 e decidere nella sezione 8. La guida dice cosa fare nei due casi.
- **Stato**: domanda.
- **Domanda**: quando arriva l'INA260, il 14 AWG entra nella morsettiera?

### P-026 ESP32 su USB e sul pin 5V insieme: diodo D1 (1N5819) e misura del pin 5V
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.03-4.08, 4.26, 4.28, 4.32, 12.07. `banco#7` «ESP32 su USB e sul pin 5V insieme...»; `schemi#6` (S-07) «Diodo 1N5819 fra il 5 V del regolatore e il pin 5V dell'ESP32».
- **Cosa**: non è scritto se la UICPAL ha un diodo fra VBUS e il pin 5V. Senza, USB e D24V22F5 si spingono uno contro l'altro (e il Mac riceverebbe il 5 V), oppure la sola USB alimenta all'indietro la basetta. Lo schema mette sempre D1 (catodo verso l'ESP32): caduta 0,3-0,45 V, il pin riceve 4,55-4,7 V e il regolatore della scheda (non documentato) deve dare ancora 3,3 V con Wi-Fi e camera. La guida tiene "mai USB e batteria insieme", ma 12.07 collega la USB con la batteria.
- **Opzioni**: (1) misurare il pin 5V con la sola USB (riga in 4.03): 0 V vuol dire diodo già presente, D1 diventa un ponticello; (2) tenere D1 e misurare il 3V3 sotto carico in P2 (sotto 3,0 V: X3 per i sensori); (3) console con la batteria solo dall'adattatore USB-seriale CH340N.
- **Consiglio**: tenere D1 finché la misura di 4.03 non dice il contrario; fino ad allora mai USB e batteria insieme; correggere 12.07.
- **Stato**: domanda.
- **Domanda**: con l'ESP32 collegata solo alla USB, quanti volt ci sono fra il pin 5V e GND?

### P-027 F2 da 2 A, ma con lo zaino il piano chiede 3 A, e il cavo della logica è da 26 AWG
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 0.08. `prima#1`.
- **Cosa**: F2 da 2 A protegge il ramo logica in 26 AWG (D-073). Il piano elettronico calcola 1,35 A (voci alte e medie), 1,81 A (tutto) e 2,04 A con la Radxa ZERO 3W dello zaino: oltre 2 A, e scrive "F2 da 3 A (da approvare)". Un 3 A sul 26 AWG non protegge il cavo. Nessun documento dice da dove prende corrente il regolatore dello zaino.
- **Opzioni**: (1) ramo proprio per lo zaino dai Wago, con fusibile e cavo suoi; (2) F2 da 3 A e tratto logica in 22 AWG (B6 e B17 da riapprovare); (3) niente zaino.
- **Consiglio**: F2 da 2 A finché lo zaino non si compra; se si compra, opzione 1.
- **Stato**: domanda.
- **Domanda**: monti lo zaino con il computer di bordo? Se sì, da dove lo alimenti?

### P-028 Percorso e ordine dei cavi di potenza intorno alla SSC-32
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 8.02-8.05. `elettronica#2`.
- **Cosa**: il Wago + sta a sinistra e il − a destra: un filo per rail attraversa il tunnel. Le fonti dicono solo "sotto la SSC-32 dal lato posteriore" (D-050), con 6 mm sotto la scheda per barre e cavi. Non è scritto se le barre si saldano prima o dopo aver avvitato la scheda; con la scheda sulle bugne il 14 AWG (circa 3,3 mm, S) entra solo di fianco.
- **Opzioni**: (1) fili e barre saldati con la SSC-32 fuori, poi avvitarla (la guida, 8.02-8.05); (2) saldare dal fianco a scheda avvitata, non verificato; (3) fessure o canale per i cavi nel tetto (2.1.7).
- **Consiglio**: opzione 1, confermata alla prima prova; se il 14 AWG non passa, opzione 3.
- **Stato**: domanda.
- **Domanda**: hai già il filo 14 AWG siliconico per misurarne il diametro (previsto circa 3,3 mm)?

### P-029 Fra T-plug e F1 non c'è un connettore, e F2 non ha una sede
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 8.14, 8.16. `elettronica#7`.
- **Cosa**: cablaggio.md dice "T-plug → F1 → Wago +" senza dire come si uniscono (entrambi con codino 14 AWG, D-073); la guida scrive saldatura e termorestringente [S]. F2 (MINI) è in linea fra Wago e 2813 senza sede nel CAD. Sesso e polarità del T-plug sul pacco sono C (BOM B12).
- **Opzioni**: (1) saldatura e termorestringente; (2) un connettore fra T-plug e F1 (non nel BOM); (3) F2 fermato con una fascetta D11 sul fianco del tunnel.
- **Consiglio**: saldatura per T-plug e F1, fascetta per F2; leggere sesso e polarità sul pacco prima di saldare.
- **Stato**: domanda.
- **Domanda**: sul pacco OVONIC il T-plug è femmina? Quale lato è il +?

### P-030 Sulla 2813, nel corpo, si saldano nove fili; piazzole e pulsantino non sono nel CAD
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 7.08, 8.16-8.18, 8.21. `elettronica#15` «Sulla 2813, nel corpo, si saldano nove fili»; `corpo#4` «Fili e pulsantino della 2813 con la scheda in piedi nelle guide».
- **Cosa**: sulla 2813, in piedi nelle guide in coda, arrivano ingresso da F2, massa, P-4, R6, S-13, VL+ e VL−, OFF, A e B: tre fili sull'uscita e tre sulla massa. Le piazzole non sono pubblicate (C): non si sa se stanno sul bordo basso (5 mm liberi) né se si raggiungono con il saldatore fra SSC-32 e T-plug. Anche la posizione del pulsantino (usato nella sezione 12) non è nel CAD.
- **Opzioni**: (1) unire al banco i tre fili dell'uscita e i tre della massa, due fili per pin; (2) saldare prima di calare la 2813 nelle guide, con i fili lunghi; (3) se il pulsantino è coperto, cacciavite da orologiaio o 2813 spostata di 5 mm (2.1.7).
- **Consiglio**: guardare la 2813 quando arriva (ordine ancora da fare) e provare sul corpo stampato; se non si arriva, opzione 1.
- **Stato**: aperto.

### P-031 Senza carapace non c'è il pulsante, che è anche l'arresto d'emergenza
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 12.01, 12.07, 12.13. `accensione#1`.
- **Cosa**: il pulsante Ø12 sta sul carapace (sezione 13); nella 12 la bozza accende con il pulsantino della 2813, che non si sa se si raggiunge [C]. Il pulsante è anche l'arresto (software.md 2.6): finché manca resta solo il T-plug.
- **Opzioni**: (1) pulsantino della 2813, se si raggiunge; (2) pulsante provvisorio sui pin A e B, il B3b di scorta, fuori dal robot; (3) pulsante del carapace collegato al banco con il cavo piatto.
- **Consiglio**: opzione 2.
- **Stato**: aperto.

### P-032 Ordine dei pin del D24V22F5 (e del D24V5F3) non letto (S-03)
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.04; `basetta.svg` U2 riga 4. `schemi#2` (S-03).
- **Cosa**: la pagina Pololu elenca PG, EN, VIN, GND, VOUT ma non l'ordine fisico; lo schema assume N-4 PG ... R-4 VOUT [C]. Un ordine sbagliato porta fino a 8,4 V sull'uscita a 5 V e sull'ESP32. EN ha 270 kΩ interni verso VIN: si lascia libero.
- **Opzioni**: (1) leggere la serigrafia prima di saldare; (2) leggerlo dallo STEP Pololu in `cad/modelli/`.
- **Consiglio**: fissare l'ordine dallo STEP o dalla serigrafia prima della guida finale; la prima accensione resta senza ESP32.
- **Stato**: aperto.

### P-033 Piedinatura e passo fra le file del traslatore KAmod (C1) non noti (S-04)
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.04; `basetta.svg` U4 righe 4 e 7. `schemi#3` (S-04).
- **Cosa**: la pagina Kamami dà solo 15,7 × 10,7 mm e due strip da 6 pin: niente sigle, ordine né distanza fra le file. Lo schema assume V, 1, 2, 3, 4, GND e file a 7,62 mm [C]. Non si sa se il modulo ha i pull-up da 10 kΩ sui due lati (contano per le prove 5 e 14).
- **Opzioni**: (1) foto del modulo dai due lati e schema corretto; (2) Adafruit 757 (alternativa del BOM), con piedinatura dal produttore.
- **Consiglio**: foto all'arrivo, prima di saldare la basetta.
- **Stato**: domanda.
- **Domanda**: quando arriva il KAmod, puoi fotografarlo dai due lati con le scritte dei pin leggibili?

### P-034 Il PTC MF-R075 regge 0,75 A, il ramo 5 V dopo il PTC arriva a circa 0,86 A (S-06)
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.05, 13; `basetta.svg` PTC1. `schemi#5` (S-06).
- **Cosa**: dopo il PTC: LED al tetto del firmware 600 mA, LED spenti fino a 94 mA, amplificatore fino a circa 200 mA; in tutto circa 0,86 A contro 0,75 A a 23 °C, meno al caldo sotto il carapace (derating non riletto, C). Il PTC potrebbe intervenire con LED al tetto e audio forte. cablaggio.md è ambiguo sul ramo dell'ampli.
- **Opzioni**: (1) tetto dei LED a 450 mA con l'audio acceso, nel firmware; (2) PTC più grosso (MF-R090); (3) ampli prima del PTC con un filo suo (serve un polo in più).
- **Consiglio**: opzione 1, scritta in software.md; misura in P4 con LED e audio al massimo.
- **Stato**: aperto.

### P-035 Sotto l'ESP32 la basetta è piena: PTC sopra il buffer a 8,1 mm su 8,5 (S-08)
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.04, 4.05; `basetta.svg`. `schemi#7` (S-08).
- **Cosa**: fra le file restano 9 × 20 fori con otto zone vietate e il regolatore. Lo schema sdraia il PTC sopra il buffer (8,1 mm con 8,5 all'ESP32) su Kapton (scattato supera 100 °C, S) e porta fuori R6, D2, R3, R9, la 100 kΩ di GPIO41 e X3. Il lato inferiore dell'ESP32 è modellato solo con la microSD: altri componenti lo terrebbero sollevato.
- **Opzioni**: (1) guardare il lato inferiore e provare a secco prima di saldare; (2) PTC in linea fuori dalla basetta, nella guaina.
- **Consiglio**: prova a secco al banco; se l'ESP32 non va in fondo, PTC in linea.
- **Stato**: domanda.
- **Domanda**: sotto l'ESP32 (lato senza modulo) ci sono componenti oltre alla sede della microSD? Basta una foto.

### P-036 Piazzole vicine sulla basetta: 5 V accanto ai GPIO, e GPIO42, OFF e polo 13 nella riga 13 (S-09, S-25)
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.04, 4.05; schemi.md 1.5, prove 5, 6 e 13. `schemi#8` (S-09) «Piazzole a 5 V accanto ai pin dell'ESP32»; `schemi#24` (S-25) «Piazzole di GPIO42, OFF e polo 13 vicine nella riga 13».
- **Cosa**: restano due vicinanze a 5 V: dato del polo 4 (F-13) accanto a GPIO48 (F-12) e VCC del buffer (E-11) accanto a GPIO47 (E-12); un ponte di stagno porta 5 V su un GPIO, che non lo regge. Nella riga 13 GPIO42 (P-13) sta fra il polo 13 (O-13, audio) e OFF (Q-13): un ponte accenderebbe il rail con l'audio (contro D-019) o spegnerebbe il robot. Non ci sono altre uscite per questi fili.
- **Opzioni**: (1) prove 5, 6 e 13 obbligatorie con l'ESP32 fuori, foro per foro; (2) nastro isolante sulle piazzole libere della riga 12.
- **Consiglio**: prove 5, 6 e 13 come passo con tabella, prima di inserire l'ESP32.
- **Stato**: aperto.

### P-037 Tensione dei pin A e B della 2813 sconosciuta (S-10)
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 8.23, 13.16; `scheda_carapace_saldature.svg` D-9, E-9. `schemi#9` (S-10).
- **Cosa**: il pulsante va ai pin A e B attraverso i poli 15-16; la pagina Pololu non dice a che tensione stanno e potrebbe essere vicina a quella della batteria. Per questo i poli 15-16 non passano dalla basetta; sulla scheda del carapace stanno accanto al polo 13 (audio) e al 14.
- **Opzioni**: (1) misurare A e B contro massa con la 2813 accesa e spenta (4.27); (2) se oltre 3,6 V: Kapton sul polo 13 e prova 4 di schemi.md 2.6 ripetuta.
- **Consiglio**: misurare al banco e scrivere il valore in cablaggio.md.
- **Stato**: domanda.
- **Domanda**: al banco, con la 2813 accesa, quanti volt ci sono fra il pin A e la massa, e fra il B e la massa?

### P-038 Pull-up del bus a 4,7 kΩ sulla basetta, con i pull-up dei moduli non tutti noti (S-13)
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.05, 8.28; `basetta.svg` R4, R5. `schemi#12` (S-13).
- **Cosa**: obiettivo 1,0-1,4 kΩ in tutto, minimo 0,97. Le tre schede Adafruit danno 3,3 kΩ; GY-6500 e ToF hanno pull-up di valore non noto. Con 4,7 kΩ sulla basetta circa 1,2-1,4 kΩ; l'espansore TCA9534 (X20), con i suoi 2,2 kΩ, porterebbe a circa 0,8, sotto il minimo. La misura fra SDA e 3,3 V non vede i pull-up del GY-6500.
- **Opzioni**: (1) 4,7 kΩ, ponticello dei pull-up dell'espansore tagliato; (2) R4 e R5 non montate fino alla misura con i moduli.
- **Consiglio**: 4,7 kΩ; in 8.28 valore atteso "circa 1,2-1,6 kΩ, mai sotto 0,97".
- **Stato**: aperto.

### P-039 Piedinatura dell'ESP32 presa dall'immagine dell'inserzione (S-15)
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.03, 4.04; `basetta.svg` righe 2 e 12. `schemi#14` (S-15).
- **Cosa**: l'ordine dei 40 pin viene dall'immagine "Pin definitions" del venditore, senza dire da che lato è vista. Se fosse vista dal retro le file si scambierebbero: il 5 V andrebbe sul GND della scheda (inversione di polarità) e tutti i GPIO al posto sbagliato. La prima accensione senza ESP32 non lo scopre.
- **Opzioni**: (1) leggere la serigrafia accanto ai pin (5V, GND, 3V3) prima di saldare le strip.
- **Consiglio**: controllo con la serigrafia al passo 4.03, insieme alla sigla RE1.3 (P-079).
- **Stato**: aperto.

### P-040 GPIO38-40 sono anche le linee della microSD: il pull-down dei microfoni potrebbe non contare (S-21)
- **Gravità e tema**: importante · elettronica e schemi
- **Dove**: 4.03, 13.16; schemi.md 2.1 (R8), 2.4. `schemi#20` (S-21).
- **Cosa**: sulla UICPAL GPIO38, 39, 40 sono SD_CMD, SD_CLK, SD_DATA. Con i soliti pull-up da 10 kΩ, la R8 da 100 kΩ (D-074) tiene GPIO40 a circa 3,0 V invece che a 0: nessun danno, ma R8 non fa quello che D-074 chiede. Con una microSD inserita le linee sarebbero condivise.
- **Opzioni**: (1) misurare a scheda spenta la resistenza fra GPIO40 e 3V3: se è circa 10 kΩ R8 si toglie o si annota inutile, e il firmware tiene conto del livello alto; (2) avviso in 4.03: nessuna microSD.
- **Consiglio**: tutte e due; il risultato in cablaggio.md 3.5.
- **Stato**: domanda.
- **Domanda**: quando arriva la scheda, puoi misurare con il multimetro la resistenza fra GPIO40 e 3V3, a scheda spenta?

### P-041 Sicurezza e carica della batteria senza fonte primaria
- **Gravità e tema**: importante · documenti in docs/
- **Dove**: 0.05-0.07, 4 (prima), 11.01, 12.01. `prima#0` «La pagina di sicurezza della batteria non ha una fonte primaria...»; `batteria#2` «Nessuna fonte del progetto dice come si carica la batteria»; `accensione#7` «Procedura d'emergenza per la batteria (calore, fumo, gonfiore) senza fonte»; `riconciliazione#8` «Carica della batteria: regole nel passo 0.06, richiamate da 4, 11.01 e 0.07».
- **Cosa**: il BOM descrive l'OVONIC solo per la scarica (50C) e i connettori: nessun caricatore, corrente di carica, tensione di conservazione, né cosa fare se il pacco scalda, fuma o si gonfia. La bozza scrive 8,4 V e 4,20 V per cella [V] e regole generali LiPo [S]; nulla su come spegnere un incendio. La riconciliazione ha già messo le regole solo in 0.06-0.07, richiamate da 4, 11.01 e 12.01.
- **Opzioni**: (1) leggere il manuale OVONIC e scrivere carica e conservazione in `docs/dimensioni-componenti.md`, poi la guida le copia; (2) sacchetto ignifugo per LiPo nel BOM (voce nuova); (3) regole generali [S] senza fonte.
- **Consiglio**: opzione 1 prima della guida 2.1.7; il sacchetto se l'utente non ne ha uno.
- **Stato**: domanda.
- **Domanda**: che caricatore usavi con la v1? Ha la carica bilanciata 2S e la modalità storage? Hai un sacchetto o contenitore per LiPo?

### P-042 Nessun documento fissa i criteri di accettazione (tolleranze delle tensioni, soglie di corrente e temperatura)
- **Gravità e tema**: importante · documenti in docs/
- **Dove**: 12.06-12.10, 14.03-14.05, 14.08, 14.09. `collaudo#1` «Nessun documento fissa i criteri di accettazione...»; `accensione#5` «Mancano le tolleranze delle tensioni da misurare».
- **Cosa**: le fonti danno i nominali (6,0 V dei rail, 5 V, 8,4 V, 2,69 V sul partitore, 53 % dello stallo, 10-12 A in marcia) ma non lo scostamento accettato: mancano tolleranza dei rail, corrente attesa a zampe ferme, soglia di temperatura dei regolatori (le NTC di X14 non hanno soglia nel firmware), temperatura dei servo, inclinazione del corpo, errore dei sensori. La bozza dice "lontano da 6,0 V, fermati" e "annota".
- **Opzioni**: (1) leggere i fogli Pololu del D42V110F6 e del D24V22F5 e scrivere il campo ammesso; (2) fissare le altre soglie con le prime misure, nel registro, e riportarle nella guida 1.1.
- **Consiglio**: tutte e due; fino ad allora "annota".
- **Stato**: aperto.

### P-043 Partitore, diodo e pull-down dell'abilitazione fuori dalla basetta: cablaggio.md da aggiornare (S-20)
- **Gravità e tema**: importante · documenti in docs/
- **Dove**: 4.04, 4.12, 8.18, 8.19, 8.25; schemi.md 1.6, 1.7. `schemi#19` (S-20).
- **Cosa**: sulla basetta non c'è un posto per la rete EN che non confini con una rete alta. Lo schema porta fuori R6 (sull'uscita della 2813), D2 (in linea nel filo di GPIO42), una R3 per regolatore (fra ENA e GND, P-024) e R9 (in linea sul dato delle tibie). Con la R3 sul regolatore un filo staccato lascia il rail spento.
- **Opzioni**: (1) come lo schema, componenti in linea con la guaina C6; (2) R3 unica sulla basetta come in cablaggio.md (non c'è un foro adatto).
- **Consiglio**: come lo schema; aggiornare cablaggio.md 3.1.
- **Stato**: aperto.

### P-044 La coxa non si monta più alzandola di 5 mm in linea con la gondola: va avvicinata ruotata di circa 40°
- **Gravità e tema**: importante · documenti in docs/
- **Dove**: 9.04. `zampa_corpo#0`.
- **Cosa**: il perno sporge 5,0 mm sopra il rialzo; dopo D-049 la testa dell'anima sta 1,0 mm sopra le teste lato coda, e scendendo di 5-6 mm in linea 22 vertici dell'aletta del servo entrano nella coxa. La procedura "alzata di 5 mm" della revisione v0 non vale più, e nessun documento di main la aggiorna. A ±40°, 6 mm più in basso, la coxa con il perno non tocca niente (a 30° tocca il servo); le zampe vicine montate a 0 non danno fastidio.
- **Opzioni**: (1) procedura a 40° della bozza, corpo sul cavalletto; (2) perno infilato da sotto a coxa in posizione (sconsigliato); (3) perno più corto o sede più alta nella 2.1.7 (tocca giunto ed escursioni).
- **Consiglio**: procedura a 40°, provata sulla prima zampa e scritta in `progetto-meccanico.md` con la 2.1.7.
- **Stato**: aperto.

### P-045 Nessun documento descrive la sostituzione di un servo, e 15.11 mescola due procedure
- **Gravità e tema**: importante · documenti in docs/
- **Dove**: 15.01, 15.10, 15.11. `smontaggio#0` «Nessun documento descrive la sostituzione di un servo di femore, di ginocchio o di coxa»; `smontaggio#7` «15.11 toglie la zampa dal corpo e poi fa ruotare la coxa sul perno...».
- **Cosa**: per il servo di coxa c'è solo una proposta della ricerca sul corpo v0 (togliere il ponte, coxa a circa 33°); per femore e ginocchio niente, salvo gli esiti dei problemi della zampa. 15.11 dice prima di togliere la zampa dal corpo e poi di ruotare la coxa sul perno, che a zampa tolta è vuoto: è la proposta v0 mescolata con 15.09.
- **Opzioni**: (1) scrivere la procedura in `progetto-meccanico.md` dopo averla provata sul primo servo; (2) provarla prima nel CAD con i giunti veri; per 15.11: via a zampa tolta (viti scoperte) o via con il solo ponte tolto (coxa a 33° [C]).
- **Consiglio**: 15.11 descrive le due vie (già nella bozza, immagine a zampa tolta); procedura provata sul primo servo e scritta in `progetto-meccanico.md`, la guida 1.1 la copia.
- **Stato**: aperto.

### P-046 "Assetto basso" della prova B6 non dice quale assetto né quale andatura per prima
- **Gravità e tema**: importante · documenti in docs/
- **Dove**: 14.07, 14.08, 14.12. `collaudo#2`.
- **Cosa**: software.md 6.7 dice "a terra in assetto basso". Gli assetti sono 130/25, 110/40, 100/45, 80/60, 70/70; a 70/70 il tripode porta il femore al 75 % dello stallo, oltre il rifiuto al 70 %. L'andatura di base è a coppie (41 % a 100/45). La bozza usa 100/45, a coppie e poi in tripode lento [C].
- **Opzioni**: (1) 100/45 a coppie, poi tripode; (2) 130/25, il più alto, e poi scendere.
- **Consiglio**: 100/45 a coppie per la prima camminata; correggere software.md 6.7.
- **Stato**: domanda.
- **Domanda**: da quale assetto vuoi far partire il robot a terra: 100/45 (punto di progetto) o più alto?

### P-047 Viti lato coda del servo di coxa: accostate in 7.05, strette in 9.08
- **Gravità e tema**: importante · testi della guida
- **Dove**: 7.05, 9.04, 9.08. `corpo#0` «Viti lato coda del servo di coxa: alette_coxa_coda va accostata nella sezione 7 e stretta nella 9»; `zampa_corpo#1` «Viti lato coda del servo di coxa: dove si accostano e come si stringono»; `riconciliazione#0` «Viti delle alette dei servo di coxa: tutte e quattro accostate nel passo 7.05, strette nel 9.08».
- **Cosa**: la procedura stava solo nella ricerca e il piano metteva le 12 viti lato coda nella sezione 9, dopo la coxa. Con la coxa montata la testa dell'anima le copre (1,0 mm sopra le teste): si liberano da ±30° (una già a +20°). La coxa si gira solo con il servo alimentato. Le due sezioni proponevano angoli diversi per il serraggio: ±20° una vite per volta (sezione 7) o 30° una posa sola (sezione 9).
- **Opzioni**: (1) accostare tutte e quattro in 7.05, stringere in 9.08 (applicato); (2) tutto in 9.08 dopo la coxa; (3) foro d'accesso nella testa dell'anima (2.1.7).
- **Consiglio**: opzione 1, già applicata dalla riconciliazione (controlli verdi); serraggio a coxa 30° (una posa sola).
- **Stato**: aperto (applicato nella bozza, da approvare).

### P-048 Viti delle alette dei servo di femore e ginocchio: raggiungibili solo in una posa, lama A tolta, cacciavite dritto
- **Gravità e tema**: importante · testi della guida
- **Dove**: 6.04, 6.20, 6.21. `zampa#14` «Le viti delle alette del servo del femore si raggiungono solo con il femore fra −8° e −49°»; `zampa#1` «Le viti delle alette del ginocchio si raggiungono solo con la lama A tolta, il ginocchio fra 45 e 75 gradi e un cacciavite a brugola dritto».
- **Cosa**: femore: la vite lato albero a X 60,6 è coperta da Femore_A per α ≥ −7° (anche nella posa come costruita); le quattro sono libere per α da −49° a −8°. Ginocchio: libere fra γ 45° e 75°, con la lama A tolta. Nella posa α −25°, γ 60° le otto viti si raggiungono con una chiave dritta lungo +Y, a lama A e guscio non montati. La chiave a L da 2,5 urta Femore_A: serve un cacciavite a brugola dritto. Le pose si portano con il servo alimentato.
- **Opzioni**: (1) posa per le alette in 6.20 (α circa −25°, γ circa 60°) con il banco dei servo, CAD invariato; (2) foro d'accesso Ø3 in Femore_A (la lama A lo copre comunque); (3) chiave a testa sferica inclinata.
- **Consiglio**: opzione 1; cacciavite dritto da 2,5 nel catalogo degli attrezzi.
- **Stato**: deciso per il ginocchio (esito di `zampa#1`: approvato l'11 ottobre 2026); aperto per la posa del femore.

### P-049 Il guscio della tibia copre una vite delle alette, che D-049 vuole stretta per ultima
- **Gravità e tema**: importante · testi della guida
- **Dove**: 6.04, 6.21-6.23. `zampa#0`.
- **Cosa**: il fianco +Y del guscio sta sopra la vite lato coda verso il fronte (X 125, Z −34,65): un fascio Ø2,8 incontra il fianco a 9,6 mm. D-049 vuole le alette strette per ultime, a femore montato; il piano metteva il guscio prima. Il guscio si monta anche a femore montato.
- **Opzioni**: (1) guscio dopo le alette strette, CAD invariato; (2) foro Ø3 nel fianco del guscio; (3) alette strette prima del femore (contro D-049).
- **Consiglio**: guscio dopo le alette; il diffusore si mette nel guscio sciolto.
- **Stato**: deciso (esito: consiglio approvato l'11 ottobre 2026).

### P-050 Prove con il rail acceso prima della batteria: B3 e B5 nelle sezioni 8 e 9 o tutto nella 12
- **Gravità e tema**: importante · testi della guida
- **Dove**: 8, 9.08, 9 (rinviati), 10.01, 10.03, 12.06-12.13. `accensione#2` «Prove con la corrente previste nelle sezioni 8 e 9, prima che la batteria arrivi nella 11»; `zampa_corpo#2` «La prova B5 nella sezione 9 viene prima della batteria e della prima accensione della sezione 12»; `riconciliazione#1` «La prova B5 e il rail acceso tolti dalla sezione 9: il servo di coxa si muove con il tester».
- **Cosa**: il piano mette B3 nella 8 e B5 (una zampa sul cavalletto, taratura con le dime) nella 9, ma la batteria entra nella 11 e la prima accensione per gradi è la 12; `tools/hexa banco` non esiste. Le sezioni proponevano cose diverse: la 12 voleva tutto il rail nella 12; la 9 voleva B5 sulla prima zampa con batteria fuori o alimentatore. La riconciliazione ha applicato la prima: B5 è nei rinviati della 9, e 9.08 gira la coxa con il tester dei servo (P-070), staccando la spina dalla SSC-32.
- **Opzioni**: (1) tutto ciò che accende il rail nella 12, nelle 8 e 9 solo prove a freddo e tester (applicato); (2) B5 sulla prima zampa nella 9, con la prima parte di B3 nella 8 e batteria fuori o alimentatore; (3) B3 e B5 nelle 8 e 9 con l'alimentatore limitato, la 12 controlla soltanto.
- **Consiglio**: opzione 1 (già nella bozza); l'opzione 2 solo se l'utente vuole provare una zampa intera prima di montare le altre e ha un alimentatore.
- **Stato**: domanda.
- **Domanda**: per la prima prova della zampa sul corpo, ti va bene aspettare la sezione 12 (batteria nel robot), o vuoi provarla prima con la batteria appoggiata fuori o con un alimentatore da banco?

### P-051 Le sei zampe si montano tutte nella sezione 6, prima del corpo
- **Gravità e tema**: importante · testi della guida
- **Dove**: 6 (ripeti_testo), 10.01, sezione 10. `riconciliazione#2`.
- **Cosa**: la sezione 10 diceva di ripetere "sezione 6, poi sezione 9" per ogni zampa, cioè dopo il corpo; ma la 6 usa il banco dei servo della sezione 5 (regolatore sulla slitta, SSC-32 dal Mac), che nella sezione 8 entra nel corpo.
- **Opzioni**: (1) tutte e sei le zampe nella 6, la 10 ripete solo la 9 (applicato); (2) ordine di prima, e la 6 usa il tester dei servo con un alimentatore.
- **Consiglio**: opzione 1.
- **Stato**: aperto (applicato nella bozza, da approvare).

### P-052 Fili della basetta, cavo piatto e collegamenti degli schemi: saldature spostate al banco
- **Gravità e tema**: importante · testi della guida
- **Dove**: 4.03-4.19, 8.07-8.25, 8.28, 13.16. `elettronica#12` «Fili saldati sulla basetta già avvitata: spostati al banco»; `riconciliazione#6` «Fili saldati sulla basetta già avvitata: 8.18 e 8.25 saldano dal lato componenti»; `riconciliazione#5` «Cavo piatto saldato sulla basetta al banco (4.05), non nel corpo (8.23)»; `schemi#15` (S-16) «Collegamenti diversi dai passi scritti...».
- **Cosa**: dopo 8.11 la basetta sta sulle colonnine con il lato rame in basso, a 3,3 mm dal vassoio: 8.18, 8.21, 8.23 e 8.25 saldavano fili che non si raggiungono più. Gli schemi hanno spostato al banco tutti i fili della basetta (cavo piatto, bus, seriale con tre Dupont, riga 13, batteria su P-4, fili delle tibie); nel corpo si salda solo l'altro capo. Cambiano anche: R6, D2, R3, R9 fuori dalla basetta, poli 15-16 separati dal cavo piatto, prima accensione senza ESP32, R8 al microfono, cavo Qwiic tagliato.
- **Opzioni**: nessuna: applicato nella F3c.
- **Consiglio**: nessuna azione.
- **Stato**: deciso (esito di `elettronica#12`: applicato nella F3c).

### P-053 Rinumerazioni e rimandi fra le sezioni dopo la F3c
- **Gravità e tema**: importante · testi della guida
- **Dove**: sezioni 0, 4, 8, 9, 11, 12, 13, appendici. `banco#10` «Sezione 4 rinumerata: i rimandi delle altre sezioni ai passi 4.xx vanno aggiornati»; `riconciliazione#16` «F3c: rimandi alle sezioni 4, 8 e alle appendici riallineati alla nuova numerazione»; `elettronica#14` «Prove a freddo con l'ESP32 fuori, ma il flat della camera era già innestato»; `riconciliazione#11` «Rimandi corretti fra le sezioni»; `appendici#3` «Le pagine delle appendici prendono il numero dalla posizione...».
- **Cosa**: la sezione 4 è passata da 14 a 34 passi; nella 8 le prove a freddo sono ora 8.26, prima di ESP32 (8.27) e camera (8.28), perché per togliere l'ESP32 si doveva staccare il flat; le appendici hanno A.15-A.19 (schemi), glossario A.20-A.25, viti A.26. L'impaginatore numera le pagine dalla posizione, non dall'id. Tutti i rimandi sono stati riallineati (415 controllati a mano), compresa la tabella di 0.24. Restano con i numeri vecchi le righe "sezione 3, riga 4.xx" di `guida/schemi/schemi.md`.
- **Opzioni**: (1) nessuna per i passi; (2) leggere i numeri dall'impaginatore invece di scriverli a mano.
- **Consiglio**: nessuna azione sui testi; l'opzione 2 come lavoro dell'impaginatore (F7).
- **Stato**: aperto (applicato nella bozza).

### P-054 Il centro del servo si perde fra il banco e il calettamento della squadretta
- **Gravità e tema**: importante · testi della guida
- **Dove**: 5.07, sezione 6 (prima del calettamento), sezione 9. `servo#0`.
- **Cosa**: il calettamento assume il servo a 1500 µs, ma spento il servo non tiene la posizione: fra la sezione 5 e la squadretta passano ore o giorni, e il riduttore trascinato a mano si sfasa. Nessun documento dice come si riporta a 1500 µs; B4 chiede il residuo entro ±7,2° senza dire a che impulso.
- **Opzioni**: (1) banco tenuto montato e P1500 subito prima della squadretta (bozza); (2) dima di centro stampata; (3) calettare dopo la taratura, a robot acceso.
- **Consiglio**: opzione 1, CAD invariato.
- **Stato**: aperto.

### P-055 Il programma di prova del banco (S1) non esiste, e lo scheletro del firmware non è mai girato sul chip
- **Gravità e tema**: importante · firmware
- **Dove**: 4.05, 4.28, 4.29, A.19. `banco#1` «Il programma di prova del banco non esiste...»; `riconciliazione#18` «La misura RMT al banco è solo nell'appendice A.19...».
- **Cosa**: software.md 6.7 prevede `tools/hexa banco` per B0 (LED, ADC su GPIO1, GPIO42): non c'è, e `firmware/main/main.cpp` tiene solo GPIO42 basso; il README dice "non provato sul chip". Al banco restano multimetro, flash dello scheletro e terminale seriale a mano. A.19 chiede la misura RMT (filo provvisorio I-7 → L-12) che nessun passo della sezione 4 fa, e la colloca prima della scheda del carapace, che viene prima di ESP32 e SSC-32.
- **Opzioni**: (1) scrivere S1 (LED, ADC, scansione I2C, comandi alla SSC-32, pixel) prima della guida finale e usarlo in 4.03, 4.08 e nei provini; (2) restare con multimetro e terminale.
- **Consiglio**: multimetro e terminale nella bozza; S1 quando c'è (è già nella roadmap); poi un passo dopo 4.29 per la misura RMT e l'avviso di A.19 riformulato.
- **Stato**: aperto.

### P-056 Le sezioni 12, 13.20 e 14 dipendono da un firmware che non c'è (S2-S6)
- **Gravità e tema**: importante · firmware
- **Dove**: 12.07-12.13, 13.20, 14.03-14.11. `accensione#0` «La sezione dipende da un firmware che non c'è ancora (console, rail, stato di taratura)»; `carapace#2` «La prova del carapace con la logica accesa dipende dal firmware...»; `collaudo#0` «La sezione dipende dal firmware S2-S6...».
- **Cosa**: console (ssc, rail, stato, cal), stato CALIBRAZIONE, salvataggio della taratura, sequenza d'accensione, modi, andature, macchina a stati, driver LED, I2S e ToF sono progetto (S2-S6); il firmware ha solo gli scheletri. software.md 2.6-2.7 tiene il rail spento senza taratura valida, ma per tarare servono i servo alimentati: serve un modo di accendere il rail con la taratura di partenza. I colori dell'anello non sono definiti. Tutte le righe sono [C].
- **Opzioni**: (1) S2 prima della sezione 12 (con un comando che accende il rail con la taratura di robot.yaml), S3 prima del collaudo, poi comandi veri nella guida; (2) tenere le sezioni come elenco di prove e valori, da rifare dopo.
- **Consiglio**: la guida si chiude dopo S2 (sezione 12) e S3 (sezione 14); 13.20 si rifà dopo S3-S6. La bozza resta valida come elenco delle prove.
- **Stato**: aperto.

### P-057 I fori per gli inserti del CAD sono tarati su inserti più grossi, e il provino degli inserti non ha un pezzo
- **Gravità e tema**: importante · provini e misure
- **Dove**: 1.02, 1.03, 3.01, 3.02 e tutti i passi con inserti. `inserti#0` «Il foro per l'inserto M3 del CAD (Ø4,2) è grande come l'inserto del kit (Ø4,2)...»; `provini#0` «Il provino degli inserti non ha un pezzo nel CAD».
- **Cosa**: `ins_m3_d` 4,2 e `ins_m2_d` 3,4 sono i fori degli inserti CNC Kitchen; gli inserti del kit Temu sono M3 Ø4,2 e M2 Ø3,2: un foro grande quanto l'inserto non dà interferenza. Il provino di `CLAUDE.md` (M3 3,9/4,0/4,1, M2 2,9/3,0/3,1) non ha un pezzo in `cad/stl/attrezzi/` né in `attrezzi.py`. I valori trovati vanno in `ins_m3_d`, `ins_m3_l`, `ins_m2_d`, `ins_m2_l`, e `ins_m3_d` muove le bugne delle culle: serve la verifica completa.
- **Opzioni**: (1) blocco del provino nella 2.1.7 con i sei fori di `CLAUDE.md` più i due valori di oggi come controllo; (2) provare direttamente su tibie e coxe (più filamento); (3) tenere i fori di oggi (rischio: inserti che girano).
- **Consiglio**: opzione 1, poi i valori nel CAD con la verifica completa; nei passi la guida non scrive il diametro.
- **Stato**: domanda.
- **Domanda**: che misure hanno gli inserti del kit Temu (diametro esterno e lunghezza di ogni misura)?

### P-058 I 94 inserti M3 non stanno in una sola lunghezza del kit, e nessuna fonte dice quale foro prende quale
- **Gravità e tema**: importante · provini e misure
- **Dove**: 0.17, 0.21, 1.03, 3.01, 3.04, A.12, A.13. `inserti#1` «I 94 inserti M3 non stanno in una sola lunghezza del kit...»; `appendici#0` «Due proposte diverse per la lunghezza dei 94 inserti M3...»; `provini#5` «I 94 inserti M3 chiedono due lunghezze del kit...»; `prima#4` «Il set di inserti del kit Temu è da 800 o da 500 pezzi?»; `provini#11` «Nessuna fonte dice temperatura e tempo di posa degli inserti nel PETG-CF».
- **Cosa**: il kit ha 50 inserti per misura (BOM D4, D5): per 94 M3 servono due lunghezze (gli M2, 28, stanno tutti in M2 × 3). Fori profondi 6,7: con M3 × 5 restano 1,7 mm di fondo, con × 6 0,7. Catalogo (INS_M3 l 5,0) e CAD contano tutti da 5. Due divisioni proposte: sezione 3, M3 × 6 ad alette e ponte (48) e × 5 agli altri (46); appendici, per presa, × 6 a guscio, ponte, chiglia davanti, colonnine, sportello e blocco del femore (50) e × 5 agli altri (44). Il BOM dice kit da 800 pezzi, `CLAUDE.md` "da 500". Mancano anche temperatura della punta e tempo di posa (più bassa per il PLA).
- **Opzioni**: (1) divisione della sezione 3; (2) divisione per presa; (3) comprare altri M3 e usare una sola lunghezza (contro "niente acquisti in più").
- **Consiglio**: provino 1.03 con M3 × 5 e × 6 sul foro più sottile (ponte, fondo 0,55) e temperatura per PETG-CF e PLA; poi una divisione scritta una sola volta in 3.01 (le appendici la copiano) e in `ins_m3_l`.
- **Stato**: domanda.
- **Domanda**: quanti inserti M3 e M2 ha davvero ogni misura del kit (50 per misura?), e il kit è da 800 o da 500 pezzi? Hai già un saldatore con punta per inserti a temperatura regolabile?

### P-059 Il provino del giunto non ha pezzi dedicati
- **Gravità e tema**: importante · provini e misure
- **Dove**: 1.09-1.11. `provini#2`.
- **Cosa**: il README parla di un "provino del giunto completo (ponte, squadretta, perni)", ma nessuno STL lo è. La bozza usa Coxa.stl con un perno e Coxa_Ponte.stl con la squadretta; restano fuori la sede del disco in Femore_A e i perni in Femore_B (stessi parametri). Non c'è un criterio per il forzamento del perno: la bozza dice "con la morsa, non col martello" [C].
- **Opzioni**: (1) pezzi veri come nella bozza; (2) attrezzo di prova piccolo (2.1.7); (3) Femore_B e Femore_A come primi pezzi del lotto.
- **Consiglio**: pezzi veri più Femore_B come primo pezzo del lotto; nessun attrezzo nuovo.
- **Stato**: aperto.

### P-060 L'ansa del cavo del ginocchio di D-058 vale per la fascetta di prima, non per quella nel blocco
- **Gravità e tema**: importante · provini e misure
- **Dove**: 6.24, 6.25. `zampa#16`.
- **Cosa**: D-058 dà 22-40 mm fra culla della tibia e fascetta vicino all'anca; D-061 ha portato la fascetta nel blocco (X 79,5) e cablaggio.md 3.2 ripete ancora 22-40 mm. Dall'uscita del cavo alla fascetta: 57,4 mm a γ 29, 40,5 a 90, 27,2 a 150 [S]. La guida dice 60 mm [C] con una prova in 6.25. La stessa misura serve ai pettini.
- **Opzioni**: (1) misurare l'ansa sulla prima zampa e scriverla in guida e cablaggio.md; (2) rifare il percorso con `calc/cavi_servo.py`.
- **Consiglio**: tutte e due nella 2.1.7; il numero vero viene dalla prima zampa.
- **Stato**: aperto.

### P-061 Con 3045 g il femore è al 53 %, l'avviso scatta al 55 %: bastano circa 105 g in più
- **Gravità e tema**: importante · provini e misure
- **Dove**: 14.02, 14.07, 14.08. `collaudo#3`.
- **Cosa**: 5,84 kgf·cm su 11 a 100/45; la coppia è proporzionale alla massa, quindi il 55 % arriva a circa 3150 g. I 3045 g contano anche cavi e viteria stimati: colla, nastro, fascette e fili in più possono superarli. Il margine non è scritto in nessun passo; la bozza fa pesare il robot in 14.02.
- **Opzioni**: (1) pesare prima di camminare; oltre 3150 g alleggerire (guscio della tibia più sottile, circa 20 g, D-063); (2) soglia d'avviso al 57 % per il primo collaudo (firmware).
- **Consiglio**: pesare e annotare; oltre 3150 g decidere con l'utente.
- **Stato**: aperto.

---

## Minori

### P-062 La striscia delle luci della tibia (50 mm) è più lunga della sede (47,5 mm), e D-066 dice Z −80 invece di −80,5
- **Gravità e tema**: minore · CAD (2.1.7)
- **Dove**: 6.05. `zampa#4` «La striscia delle luci (6 pixel, 50 mm) è più lunga della sua sede (47,5 mm)»; `zampa#5` «D-066 dice sede delle luci fino a Z -80, il taglio arriva a -80,5».
- **Cosa**: 6 pixel a 120 LED/m fanno 50 mm (S); la sede va da Z −33,0 a −80,5 (il taglio è allungato di 0,5 oltre luc_tib_z1, D-066 dice −80): il capo basso sporge 2,5 mm. I sei LED stanno nella finestra.
- **Opzioni**: (1) sede più lunga di 3 mm (luc_tib_z1 = cov_tib_fin_z1 + 3) e testo di D-066 corretto; (2) lasciare; (3) 5 pixel (cambia il firmware).
- **Consiglio**: opzione 1 nella 2.1.7.
- **Stato**: deciso (esito: approvato l'11 ottobre 2026, modifiche nella 2.1.7).

### P-063 Nella gola del fermo della tibia i fili stanno a filo (3,3-4,05 mm in 4)
- **Gravità e tema**: minore · CAD (2.1.7)
- **Dove**: 6.08. `zampa#6`.
- **Cosa**: la gola è larga 4,0 con 1,1 mm sotto i ponticelli; doppino FSR (2 × 28 AWG) e tre fili da 30 AWG occupano 3,3-4,05 mm: con i 30 AWG più grossi non entrano.
- **Opzioni**: misurare i fili comprati e, se serve, ponticelli 0,4 più alti o gola da 4,5 nella 2.1.7.
- **Consiglio**: misurare i fili prima di stampare le tibie.
- **Stato**: deciso (esito: approvato l'11 ottobre 2026); resta la domanda.
- **Domanda**: che diametro esterno hanno i fili siliconici da 28 e 30 AWG per FSR e luci?

### P-064 Linguette e tasca dell'FSR: le linguette finirebbero fuori dal piedino, e le quote della tasca differiscono fra documenti e CAD
- **Gravità e tema**: minore · CAD (2.1.7)
- **Dove**: 6.06, 6.07. `zampa#8` «Le linguette dell'FSR finirebbero sopra la tasca e fuori dal piedino»; `zampa#9` «La tasca dell'FSR ha quote diverse fra documenti e CAD».
- **Cosa**: con la coda da 16 mm della libreria, piegata sul fronte, le linguette arrivano a Z circa −93, sopra la tasca (Z −106,1…−97,1) e fuori dal piedino (−94,5). predisposizioni.md e il piano elettronico mettono la tasca 6 × 9 × 1,2 a Z −94,5…−110; il CAD a −97,1…−106,1.
- **Opzioni**: guardare la coda sull'FSR vero; se serve tasca più alta; poi allineare documenti e CAD.
- **Consiglio**: provino del piedino con un FSR vero, poi documenti e CAD allineati.
- **Stato**: deciso (esito: approvato l'11 ottobre 2026, modifiche nella 2.1.7).

### P-065 Attrezzi per premere i perni e per estrarre cuscinetti e perni
- **Gravità e tema**: minore · CAD (2.1.7)
- **Dove**: 6.14, 9, 15.10, 15.11. `zampa#17` «I perni si premono a 1,4 mm dalla faccia senza un attrezzo»; `smontaggio#3` «Come si estrae un cuscinetto o un perno forzato non è scritto».
- **Cosa**: il perno Ø5 × 12 deve sporgere 1,4 mm: premendolo esce di 5,0 dal lato del blocco, serve un appoggio forato e la sporgenza va misurata. Per estrarre, un'asta nel foro Ø7,2 spinge sull'anello interno e sulle sfere, non sulla flangia.
- **Opzioni**: (1) bussola di battuta stampata (foro cieco Ø5,5 profondo 5,0) e attrezzo d'estrazione nella 2.1.7, con l'attrezzo di P-013; (2) distanziale di recupero e calibro; per estrarre, sostituire il pezzo stampato intero.
- **Consiglio**: bussola stampata con l'attrezzo del cuscinetto; per estrarre, l'attrezzo solo se il forzamento non è leggero.
- **Stato**: aperto.

### P-066 Cicalino BX100: ingombro stimato, verso dei pin non scritto, soglia da scegliere
- **Gravità e tema**: minore · CAD (2.1.7)
- **Dove**: 12.04, 13.14, 13.19. `carapace#5` «Il collare del cicalino segue un ingombro stimato, e il verso dei pin del BX100 non è scritto»; `accensione#4` «Soglia del cicalino BX100 e verso dei suoi pin non scritti».
- **Cosa**: il collare è tagliato su 40 × 25 × 11 mm stimati (cic_*), aperto in coda; il BOM (B9) dice "posizione dei pin da guardare sul pezzo". Se i pin stanno sul lato lungo, la spina di bilanciamento non arriva alla prolunga. La bozza imposta la soglia a 3,5 V per cella [C], che sotto carico può suonare a ogni passo.
- **Opzioni**: (1) misurare il BX100 e stampare un provino del collare; (2) quote cic_* corrette nella 2.1.7; soglia: 3,5 V (come il firmware) o 3,3 V (ultimo livello indipendente).
- **Consiglio**: misurare prima di stampare il carapace; soglia a 3,3 V per cella.
- **Stato**: domanda.
- **Domanda**: lunghezza, larghezza e altezza del BX100, da che lato stanno i pin della presa di bilanciamento e dove sta il display? Soglia del cicalino a 3,3 o 3,5 V per cella?

### P-067 Presa Qwiic ed espansore TCA9534 senza posto sulla scheda del carapace (S-17)
- **Gravità e tema**: minore · CAD (2.1.7)
- **Dove**: 13.16; `scheda_carapace.svg` A-3...B-4. `schemi#16` (S-17).
- **Cosa**: il connettore JST SH è SMD e non si salda sulla millefori; lo schema usa un cavo Qwiic tagliato (X1). Dove appoggiare l'espansore (X20) sotto il dorso non è deciso.
- **Opzioni**: espansore con biadesivo sotto il dorso; posto nel CAD 2.1.7.
- **Consiglio**: insieme a S-01 (P-002).
- **Stato**: aperto.

### P-068 Viti M2 di INA260, scheda del carapace e amplificatore senza giunzione né lunghezza
- **Gravità e tema**: minore · CAD (2.1.7)
- **Dove**: 4.34, 8.03, 13.10, 13.17. `banco#5` «Gli INA260 non hanno fori di fissaggio nel CAD e nessuna giunzione»; `carapace#6` «Le viti M2 della scheda e dell'amplificatore non sono giunzioni del catalogo...».
- **Cosa**: il supporto dell'INA260 ha due inserti M2 a 17,8 mm, ma Rif_INA260 non ha fori: niente giunzione (fori C). Scheda del carapace (4 viti) e amplificatore (2) non sono nel catalogo né nei totali del BOM ("viti M2 corte"). La guida dice M2 × 5 [C]: con un circuito da 1,6 restano 3,4 mm di presa.
- **Opzioni**: (1) fori dell'INA260 nel CAD e giunzioni `ina260`, `scheda_carapace`, `ampli` nel catalogo; (2) provare con i pezzi veri e scrivere le viti nei passi; lunghezza nel BOM.
- **Consiglio**: giunzioni e lunghezza nel BOM dopo la prova sui pezzi veri; M2 × 5 fino ad allora.
- **Stato**: aperto.

### P-069 Squadretta: vite centrale, dente e viti-spina
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 6.17, 6.18, 9.01, 9.02. `zampa#19` «La testa della vite centrale della squadretta non è nota e sta nel foro Ø6 di Femore_A»; `zampa_corpo#3` «Squadretta di coxa: dente, vite centrale e viti-spina».
- **Cosa**: la vite centrale in dotazione (D3) non ha misure: il catalogo la stima M3 con testa Ø5,5; con una testa oltre circa 6 mm Femore_A non appoggia. Nessun documento dice su che dente va la squadretta di coxa: con 25 denti e quattro fori a 90° si arriva entro 1,8° [S], se il disco ha davvero quattro fori. Viti-spina: D-048 diceva M3 × 6 con rondella, D-049 M3 × 5 senza; la riga 107 del BOM dice ancora "da approvare", la D6 "approvate il 9 ottobre 2026".
- **Opzioni**: (1) guardare vite e disco sulla squadretta di prova (P-004), e se serve allargare il foro centrale nella 2.1.7; (2) regola dei fori di traverso, scarto controllato con la dima 1; (3) riga 107 del BOM corretta.
- **Consiglio**: tutte e tre.
- **Stato**: aperto (dipende da P-004).

### P-070 Tester dei servo e alimentatore da banco non sono nel BOM
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 5.01, 6.16, 6.20, 6.21, 6.25, 9.08, 15. `zampa#20` «Il tester dei servo non è nel BOM»; `riconciliazione#14` «Il banco dei servo (sezione 5) usa un regolatore che poi entra nel corpo; le sezioni 9 e 15 chiedono un tester».
- **Cosa**: la sezione 6 può usare il banco della sezione 5 (SSC-32 dal Mac), ma dopo la sezione 8 il regolatore e la SSC-32 sono nel corpo: 9.08 (P-050) e la 15 muovono un servo solo con un tester, che non è nel BOM, più un alimentatore a 6 V o un pacco a parte.
- **Opzioni**: (1) tester a manopola nel BOM (pochi euro); (2) banco della sezione 5 per la 6, e in 0.20 l'alimentatore regolabile fra gli attrezzi.
- **Consiglio**: tester a manopola nel BOM, salvo che l'utente l'abbia già.
- **Stato**: domanda.
- **Domanda**: hai un tester dei servo a manopola e un alimentatore da banco regolabile con limite di corrente?

### P-071 Attrezzi del collaudo non nel BOM, e la massa attesa vale con tutte le predisposizioni
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 14.02, 14.09. `collaudo#6`.
- **Cosa**: la guida chiede bilancia da 5 kg, termometro a infrarossi o a termocoppia e alimentatore regolabile: nessuno è nel BOM. I 3045 g contano tutte le predisposizioni (circa 45 g, D-066); il CAD non dà la massa per configurazione.
- **Opzioni**: (1) usare quelli dell'utente; (2) massa per configurazione da `esporta_robot.py`.
- **Consiglio**: chiedere cosa c'è in casa; massa per configurazione se il robot non le monta tutte.
- **Stato**: domanda.
- **Domanda**: hai una bilancia da cucina da almeno 5 kg e un termometro a infrarossi?

### P-072 Il nastro Kapton non è nel BOM, e disegno e testo degli schemi discordano per U2
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 4.04-4.09; schemi.md 1.4; `basetta.svg` U2. `schemi#23` (S-24) «Il nastro Kapton non è nel BOM»; `banco#13` «Il disegno della basetta dice U2 su nastro isolante, schemi.md 1.4 dice Kapton».
- **Cosa**: lo schema mette Kapton sotto il PTC (oltre 100 °C scattato), sotto U2 e sulle teste M3 basse (P-003); non è nel BOM né fra le cose in casa. `basetta.svg` scrive U2 "su nastro isolante", schemi.md 1.4 "su Kapton": la guida segue il disegno per U2 e usa il Kapton sotto il PTC.
- **Opzioni**: (1) un rotolo di Kapton da 10-20 mm (voce nuova); (2) nastro in PVC sotto U2 e sulle teste, PTC in linea fuori dalla basetta (P-035); disegno e testo allineati nella prossima versione degli schemi.
- **Consiglio**: Kapton, se non c'è già; allineare disegno e testo.
- **Stato**: domanda.
- **Domanda**: hai del nastro Kapton in casa?

### P-073 Il 470 µF della scheda del carapace: diametro, altezza e fili di A-4 e B-4 (S-18)
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 4.06, 4.22-4.25, 13.16; `scheda_carapace.svg` CE1, R8. `schemi#17` (S-18) «Diametro del 470 uF; la 100 kOhm dei microfoni va al microfono»; `carapace#9` «CE1 da 11 mm copre A-4 e B-4...».
- **Cosa**: CE1 sdraiato sta con Ø6,3, non con Ø8. Con 6,3 × 11 il fondo arriva a 0,4 mm dai fori A-4 e B-4 (SDA e SCL), i cui fili si saldano in 13.16, molto dopo CE1. La 100 kΩ dei microfoni (R8) non sta sulla scheda: si salda al microfono, in guaina.
- **Opzioni**: (1) saldare i quattro fili Qwiic (A-3...B-4) al banco, prima di CE1; (2) ordinare il 470 µF 10 V in Ø6,3 alto al più 8 mm.
- **Consiglio**: Ø6,3 all'ordine di X2 (corto, se si trova); fili Qwiic prima di CE1 quando si riscrive il passo della scheda.
- **Stato**: aperto.

### P-074 Nessun condensatore sul ramo delle luci delle tibie (S-23)
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 8.25; X31. `schemi#22` (S-23).
- **Cosa**: 36 pixel su fili sottili di circa 0,5 m, dal 5 V dopo il PTC, senza condensatore vicino alle prese (il 470 µF sta sul carapace).
- **Opzioni**: (1) elettrolitico 220-470 µF 10 V sulla fila delle prese delle luci (voce nuova di X31); (2) niente, e prova al massimo in P4.
- **Consiglio**: prova in P4; condensatore solo se i pixel sfarfallano.
- **Stato**: domanda.
- **Domanda**: vuoi aggiungere un condensatore sulle prese delle luci delle tibie (voce nuova, pochi centesimi)?

### P-075 La testata 2 × 8 del BOM non è identificata; il verso della chiave viene dalla spina (S-26)
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 4.06; `scheda_carapace.svg` (tacca). `schemi#25` (S-26).
- **Cosa**: il link di X2 (Würth 61201623021) è la spina IDC con fermacavo, non la testata. Sul disegno della spina polo 1 e chiave stanno sulla stessa fila: la tacca della testata va dal lato dei poli dispari (colonna D) [V].
- **Opzioni**: controllare il verso con la spina in mano prima di saldare J2.
- **Consiglio**: codice della testata nel BOM insieme alla decisione di S-01 (P-002).
- **Stato**: aperto.

### P-076 Filo della batteria verso la basetta: siliconico, non nel BOM in 26 AWG (S-27)
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 4.04, 8.18; schemi.md 1.3. `schemi#26` (S-27).
- **Cosa**: il filo VBAT si salda per ultimo accanto a saldature fatte: conviene un isolamento siliconico. B17 è 26 AWG con isolamento non dichiarato; i siliconici del BOM sono 28, 30 e 14 AWG. L'ingresso chiede fino a circa 2,3 A: troppo per 28-30 AWG su 20 cm.
- **Opzioni**: (1) 26 AWG di B17 con guaina siliconica sul tratto lungo la basetta; (2) un Dupont in silicone di C4, se è almeno 26 AWG [C].
- **Consiglio**: opzione 1.
- **Stato**: aperto.

### P-077 Luci nelle tibie e colore del diffusore non ancora decisi
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 6.05, 6.08, 6.22. `zampa#13`.
- **Cosa**: X31 è approvata come predisposizione (D-069) ma l'utente non ha deciso se montare le luci né il colore del diffusore (PLA bianco o PETG fumé, provino X10). La bozza le tratta come "meglio ora" (striscia e fili) e "anche dopo" (diffusore).
- **Opzioni**: decidere prima di montare la prima zampa.
- **Consiglio**: decidere prima della sezione 6; il colore dopo il provino di luce. È già fra gli aperti di `CLAUDE.md`.
- **Stato**: domanda (consiglio approvato l'11 ottobre 2026: decidere prima della sezione 6).
- **Domanda**: monti le luci nelle tibie? Se sì, diffusore bianco o fumé (dopo il provino di luce)?

### P-078 Il colore delle lunette dei microfoni non è dato
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 2.03, 2.20. `stampa#5`.
- **Cosa**: il README dice solo "PLA"; il BOM non le elenca in E2b (nero); nel CAD hanno l'aspetto "Esa PLA nero". La bozza scrive PLA nero [S].
- **Opzioni**: PLA nero (come il CAD) o bianco (stanno sotto il carapace).
- **Consiglio**: PLA nero; lunette aggiunte alla riga E2b del BOM.
- **Stato**: domanda.
- **Domanda**: le lunette dei microfoni vanno in PLA nero o bianco?

### P-079 Quale scheda è la RE1.3, la lega dello stagno e la temperatura del saldatore
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 4.02, 4.03, 4.06-4.25, 4.31, 4.33. `banco#8`.
- **Cosa**: già fra le cose da guardare in `CLAUDE.md`: la sigla RE1.3 serve prima del vassoio; lo stagno "a bassa temperatura" potrebbe non essere al bismuto (allora B19 perde anche lo stagno). Nessun documento dà la temperatura di saldatura: per 14 AWG e barre da 1 mm serve una punta più grossa e calda.
- **Opzioni**: l'utente legge sigla e lega e le scrive nel BOM; guida con [C].
- **Consiglio**: chiederle quando si arriva al banco.
- **Stato**: domanda.
- **Domanda**: che sigla è stampata sulla scheda ESP32 (è la RE1.3)? Che lega è lo stagno "a bassa temperatura"? Che temperatura consigliano le istruzioni del saldatore per il 14 AWG?

### P-080 Ricambi e scorte di pezzi stampati e di inserti non sono nel BOM
- **Gravità e tema**: minore · BOM e acquisti
- **Dove**: 15.14. `smontaggio#6`.
- **Cosa**: il BOM dà le scorte di servo, squadrette, cuscinetti e perni, FSR, piedini, prolunghe, fusibili; non quanti pezzi stampati o filamento tenere, né quanti inserti restano (P-058). La striscia LED comprata (1 m) è circa il doppio del necessario (0,43 m, S).
- **Opzioni**: (1) ristampare quando serve; (2) stampare subito un carapace, una tibia e un femore di scorta.
- **Consiglio**: ristampare quando serve; tenere in casa PETG-CF, PLA e TPU per un ricambio.
- **Stato**: domanda.
- **Domanda**: vuoi una scorta di pezzi stampati (carapace, tibia, femore, piedini) o ristampi quando serve?

### P-081 Canali della SSC-32, lato di VS1 e VS2 e ordine delle prese sono ancora una proposta
- **Gravità e tema**: minore · elettronica e schemi
- **Dove**: 9.07, 9.09, 10.02, A.01, A.02. `altre_zampe#1` «Canali della SSC-32 e ordine delle prese sono ancora una proposta»; `appendici#1` «I canali della SSC-32 e il lato delle file VS1 e VS2 sono una proposta...».
- **Cosa**: robot.yaml marca i canali "C, proposta" (sinistro 0-15, destro 16-31) e chiede di controllare il lato al banco (B1); VS1 sui canali 0-15 viene dal disegno del venditore [S]; l'ordine degli FSR sull'ADS7830 è [C] e quello delle prese delle luci non c'è (vedi P-012).
- **Opzioni**: (1) provare al banco un servo alla volta e correggere robot.yaml e le tabelle; (2) ordine delle prese fissato nel CAD.
- **Consiglio**: confermare in B1 e togliere la [C] prima della stampa della guida.
- **Stato**: aperto.

### P-082 Doppia massa fra la SSC-32 e la logica (S-22)
- **Gravità e tema**: minore · elettronica e schemi
- **Dove**: 8.18, 8.20; schemi.md 1.6 (E-3). `schemi#21` (S-22).
- **Cosa**: la massa della seriale va dalla SSC-32 alla basetta, quella di VL alla massa della 2813, e la basetta è collegata alla 2813. Se sul clone VL− e la massa dei servo sono comuni, parte del ritorno dei servo passa sui 26 AWG della logica; il Dupont di massa della seriale aggiunge un secondo giro.
- **Opzioni**: (1) misurare VL− contro le file di massa a scheda scollegata; se uniti, togliere il Dupont di massa della seriale; (2) tenerlo e misurare in P4 la caduta sulla massa della basetta.
- **Consiglio**: misurare prima di 8.20; se uniti, senza il Dupont di massa.
- **Stato**: domanda.
- **Domanda**: sulla SSC-32, con il multimetro, il morsetto VL− è collegato alle file di massa dei servo?

### P-083 Per provare un servo al banco serve l'EN dei regolatori comandato a mano
- **Gravità e tema**: minore · elettronica e schemi
- **Dove**: 5.01, 5.04, 5.07. `servo#4`.
- **Cosa**: B2 vuole il rail a 6 V con l'impulso prima del rail; al banco l'EN del regolatore è tenuto a massa e la bozza lo alzava con il filo del diodo sul 3V3 dell'ESP32. Non era in nessun documento.
- **Opzioni**: nessuna dopo gli schemi.
- **Consiglio**: nessuna azione.
- **Stato**: deciso (esito: R3 da 22 kΩ sul regolatore, rail acceso toccando l'ENA con un Dupont dal 3V3 dell'ESP32 sulla sola USB, 5.01, 5.04, 5.07). La domanda sull'alimentatore è in P-070.

### P-084 La 100 kΩ di GPIO41 si salda sulla 2813, sempre (S-11)
- **Gravità e tema**: minore · elettronica e schemi
- **Dove**: 4.04, 4.26, 8.19. `schemi#10` (S-11).
- **Cosa**: cablaggio.md la mette "se scatta da sola" e il passo 4.04 sulla basetta, dove non c'è posto. Il pin OFF spegne sopra 1 V: con GPIO41 flottante durante il reset un disturbo spegnerebbe il robot. Lo schema la mette sempre fra OFF e massa della 2813 (al banco, 4.26).
- **Opzioni**: come lo schema.
- **Consiglio**: come lo schema; aggiornare cablaggio.md.
- **Stato**: aperto (applicato nella bozza).

### P-085 Il regolatore 3,3 V dei sensori (X3) non sta sulla basetta (S-12)
- **Gravità e tema**: minore · elettronica e schemi
- **Dove**: 4.05; `basetta_saldature.svg` filo 19. `schemi#11` (S-12).
- **Cosa**: il D24V5F3 (13 × 10) non trova posto sotto l'ESP32. Lo schema prepara J1 (filo 19): con J1 i sensori prendono il 3,3 V dell'ESP32; con X3, J1 si toglie e il regolatore va nel vano sotto il vassoio o in linea. Mai J1 e X3 insieme.
- **Opzioni**: X3 solo se la prova del 3,3 V fallisce; posto da trovare allora.
- **Consiglio**: come lo schema; X3 non si compra finché la prova non lo chiede.
- **Stato**: aperto.

### P-086 Verso del flat e connettore FPC dell'ESP32 non documentati
- **Gravità e tema**: minore · elettronica e schemi
- **Dove**: 8.28. `elettronica#8`.
- **Cosa**: le fonti dicono solo che il connettore FPC a 24 pin sta al centro e il flat esce verso l'antenna; non se c'è una levetta né da che lato guardano i contatti. La guida dice di guardare il pezzo [C].
- **Opzioni**: guardare la scheda vera prima di stampare il vassoio.
- **Consiglio**: come le opzioni.
- **Stato**: domanda.
- **Domanda**: il connettore FPC della tua ESP32-S3-CAM ha la levetta? Come sono messi i contatti del flat (foto)?

### P-087 Voce degli inserti del BOM (D4): "30 nel corpo" invece di 28, "72" alette invece di 36
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 2.25, 3.04, 7.02, 9 (prima). `corpo#6` «Il BOM conta 30 inserti M3 nel corpo, il CAD ne ha 28»; `inserti#2` «Il BOM scrive "30 inserti M3 nel corpo", ma il modello ne ha 28»; `stampa#3` «Gli inserti M3 del corpo sono 28 nel CAD e 30 nel BOM, e la somma del BOM fa 96»; `zampa_corpo#6` «BOM D4: 'alette dei servo (72 tra lato coda e corpo)' conta le viti, non gli inserti».
- **Cosa**: il BOM dice 94 M3 = 30 nel corpo + 24 + 18 + 24, che fa 96. Il CAD ha 28 nel corpo (base 26, chiglia 2) e 66 nelle zampe (11 × 6): 94, come il totale e il controllo `totali_inserti`. In D4 "alette dei servo (72 ...)" conta le viti: gli inserti delle alette lato coda sono 36.
- **Opzioni**: correggere il testo del BOM: "28 nel corpo", "36 nelle alette lato coda".
- **Consiglio**: correggerlo con la 2.1.7; la guida usa già i numeri del CAD.
- **Stato**: deciso (esito di `stampa#3`: il totale 94 è giusto, "30 nel corpo" è un errore di testo).

### P-088 Il vassoio dell'ESP32 è in PETG per un documento e in PLA per gli altri
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 2.03, 2.18. `stampa#0`.
- **Cosa**: `progetto-meccanico.md` dice "in PETG"; README, D-065, BOM E2 e il CAD dicono PLA bianco ("sotto l'antenna: niente carbonio"). D-065 segna il PLA fra le proposte non confermate. La bozza scrive PLA [S].
- **Opzioni**: PLA bianco; PETG-CF nero (il carbonio può schermare l'antenna); PETG senza carbonio.
- **Consiglio**: PLA bianco; correggere `progetto-meccanico.md` nella 2.1.7.
- **Stato**: domanda.
- **Domanda**: il vassoio dell'ESP32 va in PLA bianco (BOM E2) o in PETG?

### P-089 progetto-meccanico.md descrive ancora il T-plug dietro il pacco, sotto i rebbi
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 11.03. `batteria#4`.
- **Cosa**: due righe della tabella del corpo mettono la coppia di T-plug dietro il pacco, raggiungibile aprendo lo sportello; D-051, D-054, D-055 e il CAD la mettono sopra F1, raggiungibile dal retro. La bozza segue D-051.
- **Opzioni**: aggiornare le due righe.
- **Consiglio**: con la 2.1.7, insieme a P-001.
- **Stato**: aperto.

### P-090 Il piano della guida usa "B4" e "B6" in un senso diverso dal BOM
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 12.04, 12.05, 12.11; titolo della sezione 14. `accensione#3` «Il piano dice "B4" nella sezione 12, ma B4 è il fusibile nel BOM e il calettamento nelle prove di banco»; `collaudo#5` «Il piano chiama "B6" la fase del collaudo, ma B6 è anche il fusibile F2 del BOM».
- **Cosa**: nel BOM B4 è l'assortimento di fusibili di F1 e B6 il portafusibile di F2; in software.md B4 è il calettamento e B6 il collaudo; il cicalino è B9. `docs/piano-guida.md` scrive "B4" nella riga della sezione 12 e "Collaudo (B6)".
- **Opzioni**: riga della 12 corretta in "F1 da 15 A (B4), cicalino (B9)"; nella 14 "prova B6 di software.md".
- **Consiglio**: correggere il piano; la bozza della 14 lo dice già.
- **Stato**: aperto.

### P-091 D-012 non ha una voce in decisioni.md
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 8.19. `elettronica#11`.
- **Cosa**: cablaggio.md e il piano elettronico citano D-012 per la seriale (115200, GPIO21 e 14), ma il registro comincia da D-041; il controllo `decisioni` della guida non la accetta, e i passi citano studio-componenti.md.
- **Opzioni**: una voce D-012 (o nuova D-0xx) in `decisioni.md`.
- **Consiglio**: come le opzioni.
- **Stato**: aperto.

### P-092 Il piano della 2.1.5 descrive la base del provino delle tasche in modo diverso dal CAD
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 1.12. `provini#8`.
- **Cosa**: `docs/piano-v2.1.0.md` (2.1.5) dice foro passante per M3 × 6 con trappola del dado; D-072 e `attrezzi.py` hanno un foro pilota Ø2,5 autofilettante. La guida segue D-072.
- **Opzioni**: correggere il piano, o lasciarlo (D-072 vale su di esso).
- **Consiglio**: correggerlo nella 2.1.7.
- **Stato**: aperto.

### P-093 predisposizioni.md descrive ancora la finestra del guscio chiusa da 0,6 di bianco
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 6.22. `zampa#11`.
- **Cosa**: la riga di X31 parla della finestra chiusa da 0,6 di bianco e della domanda 5; D-066 ha scelto il diffusore separato a incastro e D-069 ha approvato X31.
- **Opzioni**: aggiornare la riga di X31.
- **Consiglio**: con la 2.1.7.
- **Stato**: deciso (esito: approvato l'11 ottobre 2026).

### P-094 Fascette dei cavi della zampa: quote e riferimenti diversi fra cablaggio.md e D-061
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 6.24. `zampa#12`.
- **Cosa**: cablaggio.md 3.2 mette la fascetta del ponte a X 28 (D-058) e cita D-060 per quella nel blocco; D-061 l'ha spostata a X 24 (cox_fascetta_x) e ha introdotto quella nel blocco.
- **Opzioni**: correggere cablaggio.md (X 24, D-061).
- **Consiglio**: con la 2.1.7; la guida usa X 24.
- **Stato**: deciso (esito: approvato l'11 ottobre 2026).

### P-095 I fili dei microfoni (5 cm) e del ToF posteriore (15 cm) non arrivano alla scheda con la scorta
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 13.12, 13.13, 13.16. `carapace#8`.
- **Cosa**: cablaggio.md 3.5 dice circa 5 e 15 cm; dal CAD i microfoni stanno a 42,6-45,1 mm in linea retta dai fori, il ToF a circa 126-129 mm in pianta più 12 di quota, con il cavo che gira fuori dall'ottagono. La guida scrive 8 e 20 cm [S].
- **Opzioni**: tagliare a misura sul primo carapace; correggere cablaggio.md con le misure.
- **Consiglio**: misurare sul primo carapace e correggere cablaggio.md; intanto 8 e 20 cm.
- **Stato**: aperto.

### P-096 Spie dei rail: vanno prima del portafusibile; LED giallo nel BOM e "ambra" nel cablaggio
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 7.09, 7.11. `corpo#5`.
- **Cosa**: il portafusibile sta 0,6 mm davanti alle linguette delle spie: il LED si infila dal davanti e dopo F1 non c'è spazio, quindi l'ordine "F1, poi le spie" del piano non si può fare. X13 compra un LED giallo 590 nm (D-068), il cablaggio dice "ambra": è lo stesso LED. predisposizioni.md scrive ancora |y| circa 10 e "posto da trovare"; il CAD le ha a |y| 19 (D-066).
- **Opzioni**: (1) spie prima del portafusibile (7.09, poi 7.11); (2) linguette 6 mm più avanti nel CAD (2.1.7).
- **Consiglio**: opzione 1, CAD invariato; correggere cablaggio.md ("giallo") e predisposizioni.md (|y| 19).
- **Stato**: aperto.

### P-097 Il tetto del tunnel misura 164 mm nel CAD, il testo dice 162
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 2.13. `stampa#8`.
- **Cosa**: la zona interno_tunnel va da X −85,4 a 79,0 (164,4 mm); 2.13, da D-056, dice "un ponte di 50 mm lungo 162". Il valore non cambia l'azione (supporti sotto il tetto).
- **Opzioni**: verificare in Fusion la luce libera del tetto, o lasciare il testo di D-056.
- **Consiglio**: lasciare il testo; verificare quando si stampa la base.
- **Stato**: aperto.

### P-098 Parametri di stampa dati solo per il PETG-CF e il piedino
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 2.01, 2.23. `stampa#6`.
- **Cosa**: il README dà perimetri, strati e riempimento per il PETG-CF, D-064 i perimetri del piedino; niente per PLA, PETG fumé e TPU, né tolleranze dei pezzi (solo 0,1-0,2 mm sui fori, D-056).
- **Opzioni**: lasciare allo slicer (decisione dell'utente); registrare i valori dopo i provini.
- **Consiglio**: lasciare allo slicer; dopo i provini scrivere nel README valori e tolleranze che funzionano.
- **Stato**: aperto.

### P-099 Slitte e supporti degli INA260: l'orientamento sul piatto non è dato
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 2.16, 2.17. `stampa#1`.
- **Cosa**: il README dice "due copie" per le slitte e "piastra sul piatto" per i supporti, senza la faccia. La bozza mette la faccia piana della slitta sul piatto e le bugne in alto [C].
- **Opzioni**: faccia piana sul piatto (bozza) o bugne sul piatto con supporti (peggio).
- **Consiglio**: faccia piana sul piatto, scritta nel README; l'utente la conferma nello slicer.
- **Stato**: aperto.

### P-100 La slitta destra è la sinistra ruotata, non specchiata; i supporti degli INA260 invece sono speculari
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 2.02, 2.16, 2.22, 4.30, 4.34. `banco#9` «La slitta destra è la sinistra ruotata; i supporti degli INA260 sono due pezzi diversi»; `stampa#2` «La slitta destra è la stessa della sinistra, non uno specchio».
- **Cosa**: era un candidato del piano ("slitta destra: specchiata o la stessa"). Nel CAD e nel manifest la slitta D è la S ruotata di 180° attorno a Z (determinante +1); i due supporti sono speculari su Y (vertici coincidenti a 0,01 mm).
- **Opzioni**: nessuna.
- **Consiglio**: scrivere nel README degli STL che le slitte sono due copie dello stesso pezzo, la destra ruotata.
- **Stato**: deciso (esito: confermato nel CAD e nel manifest, nessuna modifica).

### P-101 Gli intervalli di manutenzione non hanno fonte
- **Gravità e tema**: minore · documenti in docs/
- **Dove**: 15.13. `smontaggio#4`.
- **Cosa**: la tabella dei controlli usa fatti dei documenti (PLA a 55-60 °C, budget termico dei servo, taratura dopo ogni smontaggio) e intervalli a eventi proposti dalla guida; nessuna coppia di serraggio per le viti dei giunti.
- **Opzioni**: (1) intervalli a eventi, numeri dopo le prime ore; (2) una pagina "Manutenzione" in `progetto-meccanico.md`.
- **Consiglio**: bozza; numeri dall'usura vera.
- **Stato**: domanda.
- **Domanda**: con la v1, ogni quanto dovevi stringere le viti o sostituire un servo?

### P-102 Il verso della coxa contro il braccio della dima ("antiorario") non diceva da dove si guarda
- **Gravità e tema**: minore · testi della guida
- **Dove**: 12.11. `accensione#6`.
- **Cosa**: D-066 e software.md 2.7 dicono "antiorario" senza "visto dall'alto". Controllato sulla geometria di `attrezzi.py` (12 ottobre): imbardata positiva, antioraria vista dall'alto, porta la coxa contro il braccio; 12.11 ora lo dice [V dallo script].
- **Opzioni**: nessuna in più.
- **Consiglio**: controllarlo sul pezzo vero; aggiungere "visto dall'alto" a D-066 e software.md.
- **Stato**: aperto (verificato sulla geometria dello script).

### P-103 L'ordine dei lotti di zampe (prima il lato sinistro) è una proposta della guida
- **Gravità e tema**: minore · testi della guida
- **Dove**: 10.01. `altre_zampe#0`.
- **Cosa**: nessun documento dice l'ordine. La bozza finisce il lato sinistro (canali 0-15 su VS1, regolatore S) prima del destro, così ogni lato si prova da solo; le zampe non si ostacolano.
- **Opzioni**: ordine per lati o libero.
- **Consiglio**: per lati.
- **Stato**: aperto.

### P-104 La prolunga di bilanciamento C7 non aveva una sezione che la preparasse
- **Gravità e tema**: minore · testi della guida
- **Dove**: 11.04, 11 (prima). `batteria#3` «La prolunga di bilanciamento non ha una sezione che la prepari»; `riconciliazione#7` «Prolunga di bilanciamento C7 preparata nel passo 11.04».
- **Cosa**: nessuna sezione saldava i due codini JST-XH; ora li salda 11.04 [S]. Se le fessure del tetto restano chiuse (P-001) vanno saldati dopo averli infilati, nella sezione 8.
- **Opzioni**: 11.04 (applicato) o sezione 8 se le fessure restano chiuse.
- **Consiglio**: segue la decisione di P-001.
- **Stato**: aperto (applicato nella bozza).

### P-105 Al banco la 2813 si collega alla basetta con i coccodrilli; le saldature sulla 2813 si fanno nel corpo
- **Gravità e tema**: minore · testi della guida
- **Dove**: 4.26-4.28, 4.32, 8.17. `banco#11`.
- **Cosa**: la prima accensione della basetta vuole la 2813, che si monta nel corpo nella sezione 7: saldata al banco la basetta resterebbe appesa. La guida usa cavetti a coccodrillo (attrezzo nuovo, non nel BOM) e salda nel corpo; la 100 kΩ fra OFF e massa si salda subito (4.26).
- **Opzioni**: coccodrilli al banco (bozza) o 2813 saldata al banco con la basetta appesa.
- **Consiglio**: coccodrilli; aggiungerli agli attrezzi della sezione 0.
- **Stato**: aperto.

### P-106 Lunghezze dei fili della basetta stimate dal CAD, prima che il corpo esista
- **Gravità e tema**: minore · testi della guida
- **Dove**: 4.16-4.19. `banco#12`.
- **Cosa**: le lunghezze sono la distanza in linea d'aria per 1,5 più 3 cm (2813 25 cm, ENA 10 e 15 cm, luci 10 cm, bus 9-15 cm, seriale Dupont 10 cm); si accorciano nel corpo. I Qwiic tagliati (circa 9 cm) potrebbero essere corti per l'INA260 destro [C].
- **Opzioni**: lunghezze stimate con margine (bozza) o fili saldati dopo la sezione 7 (la 4 si divide).
- **Consiglio**: bozza; le lunghezze vere nella guida 1.1.
- **Stato**: aperto.

### P-107 Le NTC dei regolatori si incollano al banco, non nel corpo
- **Gravità e tema**: minore · testi della guida
- **Dove**: 4.10, 8.24, 8.26. `elettronica#9` «Le NTC dei regolatori si incollano al banco, non nel corpo»; `riconciliazione#4` «NTC dei regolatori incollate al banco (4.10); nel corpo solo i fili (8.26)».
- **Cosa**: nel corpo la bobina sta sotto l'INA260 con 4,8 mm d'aria. Ora 4.10 incolla e salda (opzionale X14) e 8.26 porta solo i fili ai canali 6 e 7.
- **Opzioni**: nessuna: applicato.
- **Consiglio**: nessuna azione.
- **Stato**: aperto (applicato nella bozza).

### P-108 Nessuna sezione dice dove si infilano le spine dei servo di coxa sulla SSC-32
- **Gravità e tema**: minore · testi della guida
- **Dove**: 7.12, 8.05, 12. `elettronica#10`.
- **Cosa**: 7.12 porta i cavi verso la SSC-32 senza collegarli, la 8 monta la SSC-32 e non collega niente, la 12 parte con "spine dei 18 servo sui loro canali (sezioni 9 e 10)".
- **Opzioni**: spine di coxa nella sezione 9 con la zampa, o un passo nuovo nella 8.
- **Consiglio**: sezione 9, con le altre due spine di ogni zampa.
- **Stato**: aperto.

### P-109 Gli inserti della chiglia (dal basso) non si vedevano nelle immagini della base dall'alto
- **Gravità e tema**: minore · testi della guida
- **Dove**: 3.10, 3.11, 3.22. `inserti#3`.
- **Cosa**: i 4 inserti della chiglia entrano dal fondo ed erano coperti nelle viste dall'alto; il testo diceva "capovolgi la base" in un passo con l'immagine dall'alto. È stato aggiunto il passo 3.22 (base capovolta); i numeri citati da altre sezioni non cambiano.
- **Opzioni**: nessuna in più.
- **Consiglio**: tenere 3.22.
- **Stato**: aperto (applicato nella bozza).

### P-110 Il "quando" delle opzioni X (solo ora, meglio ora, anche dopo) è dedotto dalla guida
- **Gravità e tema**: minore · testi della guida
- **Dove**: 0.15, 0.16, 3.20, 13.01, A.10, A.11, A.14. `prima#2` «Il "quando" delle opzioni X ... non è scritto in nessun documento»; `riconciliazione#10` «Tabelle delle opzioni X (0.15, 0.16, A.10, A.11) riallineate alle sezioni scritte»; `riconciliazione#9` «Inserti M2 di scheda e amplificatore del carapace: 'meglio ora' anche nella sezione 3».
- **Cosa**: le fonti dicono quali predisposizioni sono approvate e dove stanno, non quando si possono ancora aggiungere. La guida lo ricava da cosa bisogna smontare [S]; solo X10 è "solo ora". La riconciliazione ha riallineato colonne "Sez." e "Quando" alle sezioni scritte (anche gli inserti M2 del carapace "meglio ora" in 3.20 e A.14).
- **Opzioni**: tenere il "quando" dedotto [S], o farlo decidere all'utente voce per voce.
- **Consiglio**: tenerlo [S].
- **Stato**: aperto (applicato nella bozza).

### P-111 Tempi delle sezioni non misurati, e il totale di 0.23 non è ricalcolato
- **Gravità e tema**: minore · testi della guida
- **Dove**: 0.15, 0.16, 0.22, 0.23. `prima#3` «I tempi delle sezioni non sono misurati e non tornano con quelli scritti nelle sezioni»; `riconciliazione#17` «F3c: tabelle della sezione 0 (opzioni X, durate) riallineate alle sezioni».
- **Cosa**: nessun documento dà il tempo di montaggio; le durate sono [S] (5 minuti a passo dove la sezione non dice niente). La F3c ha copiato in 0.22-0.23 le durate scritte nelle aperture delle sezioni 4, 8, 13 e 14 (e allineato X2 e X31 in 0.15-0.16), ma il totale "circa 45 ore" non è ricalcolato: con le durate nuove viene circa 48 [S].
- **Opzioni**: totale a circa 48 ore, o rivedere le durate delle sezioni 4 e 13; i tempi veri dalla guida 1.1.
- **Consiglio**: totale a circa 48 ore [S]; i tempi veri dopo la prima zampa.
- **Stato**: domanda.
- **Domanda**: il totale di 0.23 va portato a circa 48 ore, o le durate delle sezioni 4 e 13 sono da rivedere?

### P-112 La chiave per le M2 svasate è da 1,5 mm nel BOM e da 1,3 mm nel catalogo della guida
- **Gravità e tema**: minore · testi della guida
- **Dove**: 0.03, 0.17 e tutti i passi con le lame B. `prima#5`.
- **Cosa**: il catalogo (brugola_1_3) dice 1,3 mm per le M2 svasate delle lame B (D8b); il BOM elenca chiavi da 1,5, 2 e 2,5. Per una M2 svasata a esagono incassato la chiave normale è da 1,5 (ISO 10642, a memoria [S]).
- **Opzioni**: catalogo corretto a 1,5, o guardare la chiave in dotazione con le viti.
- **Consiglio**: guardare la chiave del kit e correggere il catalogo.
- **Stato**: domanda.
- **Domanda**: che chiave a brugola serve alle tue viti M2 svasate nere?

### P-113 Gli MG995 in più hanno lo stesso ingombro del MG996R ma non vanno sul robot
- **Gravità e tema**: minore · testi della guida
- **Dove**: 5.01 (prima), 5.08. `servo#5`.
- **Cosa**: il BOM ha 18 + 2 MG996R e 4 MG995 "dello stesso ingombro"; nel registro hanno solo 20 righe. Nella culla non si distinguono.
- **Opzioni**: tenerli separati e senza numero (bozza), o usarli solo per le prove del banco.
- **Consiglio**: come la bozza.
- **Stato**: aperto.

### P-114 Il registro dei servo nel sacchetto della sezione 5 contava 400 servo
- **Gravità e tema**: minore · testi della guida
- **Dove**: 5.02, 5.08, apertura della sezione 5. `servo#6`.
- **Cosa**: volte 20 per qta 20 dava 400; corretto con qta 1, e la tabella del registro ora ha 10 righe con due servo per riga.
- **Opzioni**: nessuna.
- **Consiglio**: nessuna azione.
- **Stato**: deciso (esito: corretto nella F3c).

### P-115 Lo sfilamento della zampa con la lama B montata non è verificato nel CAD
- **Gravità e tema**: minore · testi della guida
- **Dove**: 15.09. `smontaggio#5`.
- **Cosa**: i 40° e i 6 mm di 9.04 sono misurati senza Cover_Femore_B (la lama B si monta nella 12). La bozza fa togliere la lama B prima (15.06).
- **Opzioni**: togliere sempre la lama B, o provare lo sfilamento con la lama nel CAD.
- **Consiglio**: togliere la lama B.
- **Stato**: aperto.

### P-116 Anse dei cavi di coxa libere nelle baie posteriori, e misure per i pettini non definite
- **Gravità e tema**: minore · testi della guida
- **Dove**: 7.12, 9.10. `corpo#7` «Anse dei cavi di coxa: restano libere nelle baie posteriori fino ai pettini»; `zampa_corpo#5` «Le misure per i pettini dei cavi non sono definite».
- **Cosa**: i cavi di coxa hanno il 57-77 % di margine e il resto va in anse sopra i Wago (D-050), dove entrano i fili di potenza e le leve vogliono 12 mm d'aria; i pettini sono in backlog. La bozza chiede, per ogni cavo, lunghezza dall'ingresso nel corpo alla spina e ansa che avanza a coxa 0, con la prova a ±30°.
- **Opzioni**: anse libere con una fascetta lenta (D11) fino ai pettini, o pettini disegnati subito con `calc/cavi_servo.py`.
- **Consiglio**: anse libere con fascetta lenta; confermare le misure quando si disegnano i pettini.
- **Stato**: aperto.

### P-117 Le prove sui guasti possono far cadere il robot; la batteria bassa vuole un alimentatore regolabile
- **Gravità e tema**: minore · testi della guida
- **Dove**: 14.06. `collaudo#4`.
- **Cosa**: pulsante, T-plug, perdita del collegamento e batteria bassa si provano sul cavalletto; caduta, inclinazione oltre 50° e capovolgimento non hanno una prova sicura. La soglia di batteria vuole un alimentatore regolabile ("utile ma non indispensabile"); il "firmware bloccato" di P3 non ha procedura.
- **Opzioni**: solo i guasti elencati sul cavalletto, caduta e inclinazione al simulatore; prestare o comprare un alimentatore.
- **Consiglio**: bozza; alimentatore solo se si vuole provare la soglia di batteria.
- **Stato**: domanda.
- **Domanda**: hai un alimentatore regolabile con limite di corrente (vedi P-070), o ti basta provare le soglie di batteria in simulazione?

### P-118 La sezione 2 ha due passi in più per dima 2 e cavalletto
- **Gravità e tema**: minore · testi della guida
- **Dove**: 2.26-2.28. `stampa#12`.
- **Cosa**: per mostrare ogni attrezzo nella sua terna, 2.26 (dima 1), 2.27 (dima 2) e 2.28 (cavalletto); nessun rimando cambia.
- **Opzioni**: tornare a un passo solo.
- **Consiglio**: lasciare com'è.
- **Stato**: aperto.

### P-119 Zone mancanti nell'esportazione per le immagini
- **Gravità e tema**: minore · testi della guida (immagini)
- **Dove**: 1.05, 1.08, 1.12, 1.13, 1.16, 1.17, 2.07, 2.10, 2.13, 2.14, 2.18, 2.19, 2.24, 6.05, 6.06, 6.08, 7.11. Voce che raccoglie sei problemi dello stesso tipo: `provini#12` «Il provino delle tasche e quello della luce non hanno zone...»; `provini#15` «Le immagini dei passi 1.05 e 1.08 non mostrano la sede del servo»; `stampa#9` «Le bugne dei servo di coxa della base si vedono solo dall'alto...»; `stampa#11` «Mancano zone per i controlli di 2.07, 2.10, 2.14, 2.18 e 2.19»; `zampa#10` «Le immagini della striscia e dei fili non mostrano striscia e fili»; `corpo#9` «La zona fessura_cavi_* esportata ha facce della parete di coda...».
- **Cosa**: `guida/catalogo/zone.yaml` non ha zone per gli attrezzi (tasche, camere, canali), per la faccia inferiore delle bugne, per i fori di Femore_A, guscio, chiglia, vassoio, sportello e fondo dell'anello, per sede della striscia, gole e tasca dell'FSR; la zona sede_servo copre le zone piccole; la zona fessura_cavi contiene facce della parete di coda (cuneo giallo in 7.11). Oggi le immagini usano etichette a punto.
- **Opzioni**: aggiungere o dividere le zone ed esportarle (`esporta_guida.py zone`); lasciare le etichette.
- **Consiglio**: rifare la zona fessura_cavi e aggiungere le zone di stampa e della tibia alla prossima esportazione; quelle dei provini solo se i numeri non bastano.
- **Stato**: aperto.

### P-120 Gli attrezzi non seguono la posa della zampa nelle immagini (dima 2)
- **Gravità e tema**: minore · testi della guida (immagini)
- **Dove**: 2.27, 12.12. `accensione#8` «Immagine della dima 2 senza la coxa: gli attrezzi non seguono la posa della zampa»; `stampa#7` «La dima di posa 2 non si vede sulla zampa in posa».
- **Cosa**: la pipeline disegna gli attrezzi sempre nella loro terna; nella posa 2 (imbardata +30, femore +45, ginocchio 135) il femore si muove e la dima no. 2.27 mostra la dima con il solo femore B; 12.12 tiene fermo il femore e toglie coxa e servo di coxa, con una nota.
- **Opzioni**: un attrezzo legato a un segmento ne segue la posa; lasciare con la nota.
- **Consiglio**: far seguire alle dime la posa del femore e rifare 12.12 con la zampa intera.
- **Stato**: aperto.

### P-121 Avvisi della costruzione: falso "poco visibile" oltre 26 oggetti, aperture che debordano
- **Gravità e tema**: minore · testi della guida (immagini)
- **Dove**: aperture delle sezioni 6 e 8, 7.05, 9.02. `corpo#8` «7.05: vite20-vite23 'poco visibili' è un falso allarme del controllo...»; `riconciliazione#15` «Avvisi rimasti dopo la costruzione completa...».
- **Cosa**: il controllo dei pixel visibili ha 26 colori e lascia neri gli oggetti dal ventisettesimo: in 7.05 (30 oggetti) le ultime quattro viti risultano a 0 px, ma nell'immagine si vedono tutte. Restano anche l'apertura della 6 e della 8 che debordano e "9.02: vite0/vite1" (difetto di piazza). La dimensione del PDF segnalata allora (69 MB) è stata poi ridotta a 25,4 MB.
- **Opzioni**: più colori o due passate nel controllo di `rendi.py`; seconda pagina per il sacchetto; 7.05 in due passi (cambia la numerazione).
- **Consiglio**: correggere nell'impaginatore e in `rendi.py` (F7), non nei testi.
- **Stato**: aperto.

### P-122 Nei passi di prova i pezzi esplosi non hanno la freccia, e spina, viti e doppino non sono disegnati
- **Gravità e tema**: minore · testi della guida (immagini)
- **Dove**: 1.06-1.08, 1.10, 1.11, 1.15. `provini#13` «Nei passi di prova i pezzi esplosi non hanno la freccia...»; `provini#14` «In 1.08 e 1.15 la spina, le viti e il doppino non sono disegnati».
- **Cosa**: un pezzo in in_evidenza si sposta con l'esploso ma non riceve la freccia; con assiemi la freccia c'è ma la vista finale disegna pezzi sparsi. In 1.08 le quattro viti non hanno giunzione (giunzioni_usate non permette di riusare quella della sezione 6); doppino e linguette dell'FSR non sono nel CAD.
- **Opzioni**: freccia anche per i pezzi in evidenza con esploso; campo che escluda i pezzi di prova dalla vista finale; giunzione di prova con id diverso.
- **Consiglio**: correggere la pipeline; intanto zone gialle ed etichette.
- **Stato**: aperto.

### P-123 I supporti a cuneo e i supporti piccoli non sono nel CAD: le etichette SUPPORTO sono a stima
- **Gravità e tema**: minore · testi della guida (immagini)
- **Dove**: 2.04, 2.10. `stampa#10`.
- **Cosa**: il cuneo sotto lo stinco e i supporti del guscio non sono pezzi né zone; l'etichetta di 2.04 sta in un punto stimato.
- **Opzioni**: lasciare l'etichetta o toglierla.
- **Consiglio**: lasciarla; i supporti li decide lo slicer.
- **Stato**: aperto.

### P-124 Le prese delle luci sono contate come "Prese dei piedi (X5)" nel sacchetto della sezione 7
- **Gravità e tema**: minore · testi della guida
- **Dove**: apertura della sezione 7, 7.10. `corpo#10`.
- **Cosa**: Prese_piedi e Prese_luci sono lo stesso componente e il catalogo ha una sola voce (X5): il riquadro mostra "2x Prese dei piedi X5", senza X31. Testo ed etichette distinguono le due file.
- **Opzioni**: una voce di catalogo per occorrenza; lasciare così.
- **Consiglio**: lasciare finché il catalogo non conosce le occorrenze (F7).
- **Stato**: aperto.

### P-125 Il registro delle misure è una copia delle tabelle dei passi
- **Gravità e tema**: minore · testi della guida
- **Dove**: A.03-A.05. `appendici#2`.
- **Cosa**: A.03-A.05 riassumono le colonne "Misurato" dei passi; se un passo cambia un valore atteso il registro resta indietro.
- **Opzioni**: generare il registro dalle tabelle con l'impaginatore; tenere la copia a mano e rivederla.
- **Consiglio**: generarlo; almeno rivederlo a ogni riconciliazione.
- **Stato**: aperto.

### P-126 Il glossario è generato da uno script fuori dalla repo
- **Gravità e tema**: minore · testi della guida
- **Dove**: `guida/glossario.yaml`, A.20-A.25, 0.24. `riconciliazione#12`.
- **Cosa**: i 14 file di `guida/glossario.d/` sono stati uniti in `guida/glossario.yaml` (122 termini) e l'appendice è stata generata con `/tmp/guida_tools/genera_glossario.py`, che non è nella repo.
- **Opzioni**: un comando `glossario` dell'impaginatore.
- **Consiglio**: come le opzioni.
- **Stato**: aperto.

### P-127 Il verso del servo è un'ipotesi del firmware, e la prova decide il segno di tutta la zampa
- **Gravità e tema**: minore · firmware
- **Dove**: 5.05. `servo#1`.
- **Cosa**: robot.yaml presume il servo antiorario quando l'impulso cresce e ne ricava i segni dei giunti (coxa +1, femore −1, ginocchio +1). La guida fa provare 1400 e 1600 µs e annotare.
- **Opzioni**: annotare e correggere robot.yaml, regressione e simulatore se il verso è opposto; due servo opposti fra loro: scartare.
- **Consiglio**: come la bozza.
- **Stato**: aperto.

### P-128 L'escursione provata al banco (±72°) è più stretta di quella del firmware (±80°)
- **Gravità e tema**: minore · firmware
- **Dove**: 5.06. `servo#2`.
- **Cosa**: robot.yaml usa ±80° a 11,1 µs/grado (612-2388 µs, S); la guida si ferma a 700-2300 µs per non cercare il fermo meccanico. Gli ultimi 8° per lato restano non provati fino alla taratura con le dime.
- **Opzioni**: provare fino a 612-2388 µs ascoltando se ronza; fermarsi a 700-2300 (bozza).
- **Consiglio**: come la bozza; il limite vero viene dalla taratura e la guardia lo contiene.
- **Stato**: aperto.

### P-129 robot.yaml non contiene i pin dell'ESP32 (S-14)
- **Gravità e tema**: minore · firmware
- **Dove**: schemi.md 1.2. `schemi#13` (S-14).
- **Cosa**: le assegnazioni dei GPIO stanno nel piano elettronico (2.3) e, per GPIO42, in `firmware/main/main.cpp`; robot.yaml ha solo canali, guardia, andatura e massa.
- **Opzioni**: sezione pin in robot.yaml, generata nell'header.
- **Consiglio**: nella fase S1.
- **Stato**: aperto.

### P-130 La tibia del provino della culla ha i fori per gli inserti da 4,2, prima che il provino 1 dica il valore giusto
- **Gravità e tema**: minore · provini e misure
- **Dove**: 1.05, 1.08. `provini#6`.
- **Cosa**: Tibia.stl ha `ins_m3_d` = 4,2: se il valore buono è 4,0 la tenuta degli inserti nella prova della culla è falsata; da `ins_m3_d` dipendono anche le bugne della culla.
- **Opzioni**: provino 1 per primo e Tibia.stl riesportata se il valore cambia; oppure contare solo le misure, non la tenuta.
- **Consiglio**: provino 1 per primo (la guida lo dice in 1.01 e 1.05).
- **Stato**: aperto.

### P-131 Il provino di luce non prova l'incastro del diffusore né quello del fondo dell'anello
- **Gravità e tema**: minore · provini e misure
- **Dove**: 1.16, 1.17. `provini#7`.
- **Cosa**: luc_dif_gio (0,1) e luc_fondo_gio (0,05) sono "da tarare sul provino", ma il provino ha solo camere, strisce di bianco e un anello senza fondo né diffusore.
- **Opzioni**: provarli sui pezzi veri alla prima stampa; bordino e gonna nel provino (2.1.7).
- **Consiglio**: pezzi veri alla prima stampa.
- **Stato**: aperto.

### P-132 Tre provini citati nel README non hanno né un pezzo né un passo
- **Gravità e tema**: minore · provini e misure
- **Dove**: 1.01. `provini#9`.
- **Cosa**: il README elenca tappo a rombo, nervature dello sportellino e collare del cicalino fra i provini della passata estetica; nessuno ha un attrezzo né è fra i provini di `CLAUDE.md`.
- **Opzioni**: provarli sui pezzi veri; aggiungerli a un provino (2.1.7).
- **Consiglio**: pezzi veri alla prima stampa; il collare, prima del carapace, con la misura del BX100 (P-066).
- **Stato**: aperto.

### P-133 "Servo fermo, senza gioco" dipende dal servo vero, e le nervature di schiacciamento non esistono
- **Gravità e tema**: minore · provini e misure
- **Dove**: 1.08. `provini#10`.
- **Cosa**: sede 41,4 × 20,9 sul caso peggiore; con le casse dichiarate il gioco va da 0,4 a 1,1 mm in lunghezza e fino a 0,9 in larghezza. Le nervature sono "da decidere sul provino" (già in `CLAUDE.md`).
- **Opzioni**: misurare il gioco nel provino e disegnare le nervature; nessuna nervatura.
- **Consiglio**: misurare nel provino 3 e disegnare le nervature nella 2.1.7.
- **Stato**: aperto.

### P-134 Non si sa se i servo AZDelivery hanno i gommini montati né i collari di ottone
- **Gravità e tema**: minore · provini e misure
- **Dove**: 5.02, 6.03. `servo#3`.
- **Cosa**: il progetto toglie i gommini; nessun documento dice se sono già nelle alette né se ci sono collari di ottone che cambiano il gioco della M3 nel foro da 4,2. È una cosa da guardare, non una misura.
- **Opzioni**: l'utente guarda un servo; "se ci sono" [C] nella bozza.
- **Consiglio**: come la bozza finché l'utente non ha guardato.
- **Stato**: domanda.
- **Domanda**: su un MG996R appena aperto, i gommini sono già nelle alette o nel sacchetto? Ci sono tubetti di ottone dentro i gommini?

### P-135 Come si sfila la lama A e quanta forza serve
- **Gravità e tema**: minore · provini e misure
- **Dove**: 15.07. `smontaggio#2`.
- **Cosa**: la lama A si calza sulle teste M3 senza viti; la tenuta (tasche lisce o costole) la decide il provino D-072. Nessun documento dice dove si impugna; la bozza dice "tira dritto lungo Y, non forzare" [C].
- **Opzioni**: annotare forza e verso dopo il provino; tacca per l'unghia nella 2.1.7.
- **Consiglio**: provino prima, poi la procedura.
- **Stato**: domanda.
- **Domanda**: dopo il provino delle tasche, quanta forza serve per togliere la lama? Si impugna bene?

### P-136 Il numero di rondelle di registro dipende dalla squadretta vera
- **Gravità e tema**: minore · provini e misure
- **Dove**: 6.18. `zampa#18`.
- **Cosa**: il CAD lascia 1,0 mm fra blocco di Femore_B e Femore_A (due DIN 125 da 0,5 per vite, 48 nel BOM), ma dipende dallo spessore del disco (sq_sp 2,5, C). Il kit ne ha 330.
- **Opzioni**: misurare la luce sul provino del giunto e scrivere il numero nel passo.
- **Consiglio**: come le opzioni (dopo P-004).
- **Stato**: aperto.

### P-137 Il T-plug a carapace montato è stretto fra cicalino, ToF e altoparlante
- **Gravità e tema**: minore · provini e misure
- **Dove**: 13.23. `carapace#7`.
- **Cosa**: il T-plug sta 7 mm dentro la porta di coda, con 3,3 mm sotto il cicalino; è il sezionamento d'emergenza. D-069 e `CLAUDE.md` lo danno "da provare a mano sul primo carapace", con il ripiego di una linguetta di nastro.
- **Opzioni**: prova a mano (bozza); ToF e altoparlante più in alto (2.1.7).
- **Consiglio**: prova a mano, come previsto.
- **Stato**: aperto.

### P-138 Mancano i dati per saldare e fissare FSR e striscia nella tibia
- **Gravità e tema**: minore · provini e misure
- **Dove**: 6.05, 6.06. `zampa#7`.
- **Cosa**: non sono scritti temperatura e tempo di saldatura delle linguette dell'FSR, il raggio minimo di piega della coda, se FSR e striscia hanno l'adesivo, i colori dei tre fili delle luci (la bozza propone nero, rosso, dato [S]); le lunghezze 0,4-0,5 m sono S.
- **Opzioni**: guida d'integrazione Interlink e scheda della striscia; prova di piega e saldatura sul provino del piedino.
- **Consiglio**: provino del piedino con un FSR vero prima delle sei tibie.
- **Stato**: deciso (esito: approvato l'11 ottobre 2026); resta la domanda.
- **Domanda**: la striscia e gli FSR che hai (o comprerai) hanno l'adesivo sul retro?
