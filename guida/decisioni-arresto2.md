# Decisioni dell'arresto 2 (15 ottobre 2026)

Una riga per voce: P-xxx, decisione, file cambiati. Fonte: `guida/problemi.md`, sezione "Decisioni in blocco"; l'utente ha detto "risolvi in autonomia, se non ci sono scelte importanti" e ha approvato P-004. Le voci con una scelta vera non sono applicate: "da decidere".

## Bloccanti

- P-004: approvato dall'utente; squadretta di prova (una AliExpress e una confezione diymore) approvata, domanda 4 del BOM risposta, voce D3 e ordine degli acquisti aggiornati; il costo extra (10,99 €) è scritto fuori dal totale di 362,13 €. File: `docs/BOM.md`.

## Gruppo 1: correzioni di testo ai documenti in docs/

- P-043: applicato come lo schema: D2 (1N4148) in linea e R3 da 22 kΩ ENA-massa su ogni regolatore, R6 (100 kΩ) alla 2813, R9 in linea sul dato delle tibie. File: `docs/cablaggio.md` (schema di potenza, schema dei segnali, 3.1, 3.3).
- P-087: applicato: "28 nel corpo" (base 26, chiglia 2), 66 nelle zampe, 36 inserti nelle alette lato coda (le 72 sono viti). File: `docs/BOM.md` (D4 e riga "Inserti a caldo"). I totali (94 M3, 28 M2) non cambiano.
- P-089: applicato: la coppia di T-plug sta sopra F1, raggiungibile dal retro (D-051, D-054, D-055). File: `docs/progetto-meccanico.md` (riga di `Corpo_Sportello` e vano di coda).
- P-090: applicato: riga 12 del piano "F1 da 15 A (B4 del BOM), cicalino (B9)"; riga 14 "prova B6 di `software.md`". File: `docs/piano-guida.md`.
- P-091: applicato: voce D-012 in `docs/decisioni.md` (ereditata dal registro MG90S, con RX su GPIO14 invece di GPIO47). File: `docs/decisioni.md`.
- P-092: rimandato alla 2.1.7: `docs/piano-v2.1.0.md` è riservato ad altri agenti in questa passata; la guida segue già D-072 (foro pilota Ø2,5 autofilettante).
- P-093: applicato: riga di X31 aggiornata (diffusore separato a incastro, D-066; sede approvata in D-069). File: `docs/predisposizioni.md`.
- P-094: applicato: fascetta del ponte a X 24 (`cox_fascetta_x`, D-061), fascetta nel blocco D-061 al posto di D-060. File: `docs/cablaggio.md` 3.2.
- P-096: applicato per i documenti: LED "giallo" (cablaggio.md, predisposizioni.md X13), spie a |y| 19 (predisposizioni.md). I passi hanno già l'ordine giusto (spie in 7.09, portafusibile in 7.11): nessuna modifica. File: `docs/cablaggio.md`, `docs/predisposizioni.md`.
- P-099: rimandato alla 2.1.7: la riga sull'orientamento va nel README degli STL (`cad/stl/README.md`, cartella riservata ad altri agenti): faccia piana della slitta sul piatto, bugne in alto [C].
- P-100: rimandato alla 2.1.7, stesso motivo: scrivere nel README degli STL che le slitte sono due copie dello stesso pezzo, la destra ruotata. Nessuna modifica al CAD (esito già deciso).
- P-102: applicato: "visto dall'alto" dopo "antiorario" nella taratura. File: `docs/decisioni.md` (D-066), `docs/software.md` 2.7.

## Gruppo 2: testi della guida già cambiati dalla riconciliazione F3c

Approvati a posteriori, nessuna modifica.

- P-047: approvato, nessuna modifica.
- P-051: approvato, nessuna modifica.
- P-052: approvato, nessuna modifica.
- P-053: approvato, nessuna modifica.
- P-084: approvato, nessuna modifica.
- P-104: approvato, nessuna modifica.
- P-107: approvato, nessuna modifica.
- P-109: approvato, nessuna modifica.
- P-110: approvato, nessuna modifica.
- P-114: approvato, nessuna modifica.

## Gruppo 4: CAD

Non trattato qui: lo prepara un altro agente nel piano della 2.1.7 (P-009, P-014, P-015, P-016, P-019, P-057, P-062, P-065).

## Gruppo 6: scelte degli schemi elettrici

Accettate come proposte; gli schemi sono già fatti (`guida/schemi/`). Nessuna modifica qui.

- P-024: accettato, rimandato (schema già fatto: ENA a R3 da 22 kΩ su ogni regolatore).
- P-028: accettato, rimandato (schema già fatto).
- P-030: accettato, rimandato (schema già fatto).
- P-032: accettato, rimandato (schema già fatto; l'ordine dei pin resta da leggere sul pezzo, S-03).
- P-034: accettato, rimandato (schema già fatto; la misura del ramo 5 V resta al banco).
- P-035: accettato, rimandato (schema già fatto).
- P-038: accettato, rimandato (schema già fatto).
- P-039: accettato, rimandato (schema già fatto; la piedinatura si controlla sul pezzo, S-15).

## Gruppo 7: firmware e strumenti

Accettati e rimandati alla roadmap S1-S3 (`docs/piano-elettronica-software.md`). Nessuna modifica.

- P-055: rimandato a S1-S3.
- P-056: rimandato a S1-S3.
- P-127: rimandato a S1-S3.
- P-128: rimandato a S1-S3.
- P-129: rimandato a S1-S3.

## Gruppo 8: impaginatore e immagini

Accettati e rimandati alla fase F7 della guida (`docs/piano-guida.md`). Nessuna modifica.

- P-119: rimandato a F7.
- P-120: rimandato a F7.
- P-121: rimandato a F7.
- P-122: rimandato a F7.
- P-125: rimandato a F7.
- P-126: rimandato a F7.

## Gruppo 3: altre correzioni di testo della guida

- P-026: applicato: finché il pin 5V con la sola USB non dice che la scheda ha un diodo (passo 4.05), mai USB e batteria insieme; 12.07 collega la USB solo se il pin ha dato 0 V, altrimenti la console passa dall'adattatore USB-seriale CH340N (già approvato nel BOM); D1 resta. File: `guida/passi/12-accensione.yaml` (12.07), `guida/passi/04-banco.yaml` (stato elettrico).
- P-031: da decidere: il consiglio (pulsante provvisorio sui pin A e B della 2813, il B3b di scorta) riguarda l'arresto d'emergenza (sicurezza) e richiede un secondo pulsante B3b (acquisto). Nessuna modifica; la bozza di 12.01-12.07 resta con il pulsantino della 2813.
- P-036: già nella guida: i passi 4.20 e 4.21 hanno le prove 5, 6 e 13 in tabella, con l'ESP32 ancora fuori. Nessuna modifica.
- P-045: già nella guida: 15.11 descrive le due vie (zampa tolta, oppure ponte tolto e coxa a circa 33° [C]) e dice che la procedura non è provata. Rimandato: scrivere la procedura in `docs/progetto-meccanico.md` dopo averla provata sul primo servo, poi copiarla nella guida 1.1.
- P-048: già nella guida: posa per le alette in 6.20 (α circa −25°, γ circa 60°) e cacciavite dritto 2,5 (`brugola_dritta_2_5`) nel catalogo. Nessuna modifica.
- P-054: già nella guida: 5.07 tiene il banco montato e prima della squadretta (6.16) riporta il servo a 1500 µs. Nessuna modifica.
- P-103: già nella guida: 10.01 fa prima il lato sinistro, poi il destro. Nessuna modifica.
- P-105: applicato: i cavetti a coccodrillo (già nel catalogo, sezione 4) entrano nell'elenco degli attrezzi della sezione 0 (apertura e inventario 0.20). Il BOM non cambia: nessun acquisto aggiunto. File: `guida/passi/00-prima.yaml`.
- P-106: già nella guida: lunghezze stimate con margine, da accorciare nel corpo. Nessuna modifica.
- P-108: già nella guida: 9.07 collega le spine di coxa, femore e ginocchio ai loro canali. Nessuna modifica.
- P-113: già nella guida: gli MG995 restano separati e senza numero. Nessuna modifica.
- P-115: già nella guida: 15.06 toglie la lama B prima dello sfilamento (15.09). Nessuna modifica.
- P-116: applicato: l'ansa del cavo di coxa si tiene con una fascetta lasca (D11, 6 in tutto); i pettini restano in backlog e le misure si confermano quando si disegnano. File: `guida/passi/07-corpo.yaml` (7.12).
- P-118: confermato com'è (due passi in più in 2.26-2.28). Nessuna modifica.
- P-123: confermato com'è: etichetta SUPPORTO lasciata, i supporti li decide lo slicer. Nessuna modifica.
- P-124: confermato com'è: si lascia finché il catalogo non conosce le occorrenze (F7). Nessuna modifica.

## Gruppo 5: catalogo delle giunzioni e BOM

- P-020: applicato in parte: con il supporto dell'INA260 (X7) le 2 viti delle slitte sono M3 × 10 (M3 × 8 darebbe 3,2 mm di presa, M3 × 10 ne dà 5,2). BOM: riga delle slitte e paragrafo "Viteria in più" con i totali con X7 (M3 × 8: 104, M3 × 10: 20); la riga "Totale viti" resta quella senza X7, quindi i totali di `viteria.yaml` restano uguali. Giunzione per variante non aggiunta: la pipeline non sa disegnarla con il supporto e darebbe un avviso falso (nota in `giunzioni.yaml`); rimandata a F7. File: `docs/BOM.md`, `guida/catalogo/giunzioni.yaml` (solo commento).
- P-068: applicato in parte: nel BOM le viti M2 dei supporti INA260 (2 a supporto), della scheda del carapace (4) e dell'amplificatore (2) sono M2 × 5 [C] fino alla prova sui pezzi veri. Rimandato: fori dell'INA260 nel CAD (2.1.7) e giunzioni `ina260`, `scheda_carapace`, `ampli` nel catalogo, dopo la prova. File: `docs/BOM.md`.
- P-069: applicato in parte: riga 107 del BOM, M3 × 5 "approvate il 9 ottobre 2026, come D6" invece di "da approvare" (D-049); 9.01 dice 1,8° e "se il disco ha davvero quattro fori [C]", con controllo dello scarto con la dima 1 (12.11). Rimandato: guardare vite centrale e disco sulla squadretta di prova (dopo P-004, arrivo dei pezzi) ed eventuale foro centrale più largo nella 2.1.7. File: `docs/BOM.md`, `guida/passi/09-zampa-corpo.yaml`.
- P-073: da decidere: il consiglio (470 µF di X2 in Ø6,3 alto al più 8 mm, "corto se si trova") cambia il componente da ordinare. Nessuna modifica; il riordino dei fili Qwiic prima di CE1 nel passo 13.16 si fa quando si riscrive il passo della scheda.
- P-075: da decidere: il codice della testata 2 × 8 nel BOM dipende dalla scelta su S-01 (P-002, domanda Q-02: spostare la scheda o testata a 90° da comprare). Nessuna modifica.
- P-076: applicato: il filo della batteria verso la basetta è il 26 AWG di B17 con una guaina termorestringente (B19, già in casa) sul tratto lungo la basetta; 4.19 aggiornato (nessun acquisto). File: `docs/BOM.md` (B17), `guida/passi/04-banco.yaml` (4.19).
- P-085: da decidere: il consiglio ("X3 non si compra finché la prova del 3,3 V non lo chiede") toglie un acquisto oggi approvato nel BOM (X3, D24V5F3, 7,76 €). Nessuna modifica; resta lo schema con J1 e il caso "mai J1 e X3 insieme".

## Gruppo 9: provini e misure sul primo esemplare

- P-042: rimandato: servono i fogli Pololu del D42V110F6 e del D24V22F5 (fonte primaria, non letti in questa passata) per scrivere il campo ammesso; le altre soglie vengono dalle prime misure. Fino ad allora la guida dice "annota", come ora.
- P-059: applicato: nota in 1.11, la sede del disco in Femore A e i perni in Femore B si provano sui pezzi veri con Femore B primo del lotto; nessun attrezzo nuovo. File: `guida/passi/01-provini.yaml`.
- P-060: già nella guida (60 mm [C] con prova in 6.25); `cablaggio.md` 3.2 corretto con le tre misure per la fascetta nel blocco (57,4 / 40,5 / 27,2 mm). Rimandato: numero vero dalla prima zampa e giro di `calc/cavi_servo.py` nella 2.1.7. File: `docs/cablaggio.md`.
- P-061: applicato: 14.02 dice di pesare prima di camminare e, oltre 3150 g, di annotare il peso e fermarsi a decidere come alleggerire (guscio della tibia, D-063); soglia d'avviso e alleggerimento restano da decidere con l'utente se succede. File: `guida/passi/14-collaudo.yaml`.
- P-095: applicato: `cablaggio.md` 3.5 dà microfoni circa 8 cm e ToF posteriore circa 20 cm [S], da tagliare a misura sul primo carapace (la guida usa già 8 e 20 cm). File: `docs/cablaggio.md`.
- P-130: già nella guida (1.01 e 1.05: il provino 1 viene per primo). Nessuna modifica.
- P-131: applicato: nota in 1.17, gli incastri del diffusore (luc_dif_gio) e del fondo dell'anello (luc_fondo_gio) si tarano sui pezzi veri alla prima stampa. File: `guida/passi/01-provini.yaml`.
- P-132: già nella guida (nota in 1.01: tappo a rombo, nervature dello sportellino e collare si provano sui pezzi veri). Il collare prima del carapace, con la misura del BX100 (P-066): rimandato a quella misura. Nessuna modifica.
- P-133: già nella guida (provino 3 misura il gioco, nervature "da disegnare" dopo la prova). Rimandato: nervature nella 2.1.7.
- P-136: rimandato: il numero di rondelle di registro dipende dalla squadretta vera (dopo P-004); si misura la luce sul provino del giunto e si scrive nel passo 6.18.
- P-137: già nella guida (13.23: prova a mano, con il ripiego di una linguetta di nastro). Nessuna modifica.

## Scelte finali dell'utente (15 ottobre 2026, D-076)

Dopo le decisioni in blocco l'utente ha risposto alle domande e deciso i bloccanti. Il perché è in `docs/decisioni.md` D-076; le modifiche al CAD in `docs/piano-v2.1.0.md` ("Versione 2.1.7"). Le voci qui sotto sostituiscono le righe "da decidere" delle sezioni precedenti (P-031, P-073, P-075, P-085).

### Bloccanti

- P-001: fessure del tetto aperte verso la coda nella 2.1.7, con il dentino per la fascetta di F1 (modifica 11). Niente caricatore integrato: si carica con il caricatore USB 2S lento dell'utente, alle spine in coda. Sacchetto LiPo da comprare (B20).
- P-002: soluzione A, testata 2 × 8 a 90° con chiave sul bordo posteriore della scheda, comprata con X2 (modifica 12). La guida resta sulle millefori; nota che l'alternativa PCB stampato arriverà in una versione successiva.
- P-003: soluzione e di `bloccanti-arresto2.md` (colonne della base, inserti M2, M2 × 5 svasate). B18 esce dal BOM (modifica 1).
- P-004: squadretta di prova approvata (già nel BOM).
- P-005: interasse 25,4 (S) con prova a secco prima di saldare (modifica 2).

### Voci che erano "da decidere"

- P-031: opzione 2, pulsante provvisorio sui pin A e B della 2813, il secondo B3b. L'utente non ha pulsanti: si comprano due (B3b "1 + 1", già nel BOM). Testi 12.01 e 12.07 dopo la 2.1.7.
- P-073: condensatore da 470 µF basso (Ø6,3, alto al più 8 mm) nell'ordine di X2.
- P-075: testata 2 × 8 a 90° con chiave nell'ordine di X2 (Würth 61201621721, da confermare sul disegno).
- P-085: X3 esce dal BOM; negli schemi resta J1 come ritorno possibile.

### Dalle risposte

- P-004, P-059, P-069, P-136: squadretta di prova approvata (Q-01).
- P-021: 2 FSR 400 Short e un tratto di striscia a 120 LED/m con buffer e resistenze approvati per i provini 6 e 7 (Q-05).
- P-077, P-062, P-063, P-064, P-138: luci delle tibie opzionali, diffusore bianco (Q-06). P-063: gola da 4,5 (modifica 14).
- P-074: condensatore sulle prese delle luci solo se serve, con quelli in casa (Q-07).
- P-027: niente zaino per ora (Q-08); F2 resta da 2 A.
- P-008: ToF posteriore avvitato, ritegno dell'altoparlante, microfoni con colla a caldo (Q-09, modifica 15).
- P-088, P-078: vassoio e lunette in PLA, colore libero (Q-10, Q-11).
- P-066: soglia del cicalino a 3,3 V per cella (Q-12). P-046: 100/45 a coppie (Q-13).
- P-050: prima prova della zampa con la batteria, nessun alimentatore da banco (Q-14).
- P-080: ristampa quando serve (Q-15). P-111: le durate non importano, si toglie il totale delle ore (Q-16).
- P-007, P-029, P-041, P-001: dati misurati della batteria (Q-17): 139,65 mm, cavo 110 mm, T-plug femmina, positivo sul lato verticale; rebbi più lunghi (modifica 16).
- P-057, P-058: inserti del kit, zigrinatura Ø4,2 e invito Ø4,0 per l'M3, Ø3,2 e Ø3,0 per l'M2 (Q-20); il provino resta (Q-21: il resto in autonomia).
- P-010: pulsante non in casa (Q-22): si misura all'arrivo, prima del fondo dell'anello.
- P-028: fili da specifiche, stando larghi (Q-24).
- P-072, P-008: consumabili generici fuori dal BOM (Q-25).
- P-070, P-071, P-117: l'utente ha solo la bilancia (Q-26): la guida non chiede alimentatore da banco né termometro a infrarossi; tester dei servo da comprare (C9).
- P-134: gommini e tubetti di ottone vengono a parte e non si montano (Q-28).
- P-101: intervalli di manutenzione a eventi, numeri dall'uso (Q-29).
- P-012: prese dei piedi e delle luci come da registro, con lo schema dei partitori (Q-04, "non lo so").

### Aperte

Q-18, Q-19, Q-23, Q-27, Q-30 … Q-37: da chiedere quando arrivano i pezzi. P-067 (espansore e presa Qwiic sulla scheda del carapace) si decide con i fori liberi della modifica 12.

### Testi della guida cambiati in questa passata

- 5.02, apertura e controllo della sezione 5, 6.03, 6.04 e 1.08: gommini e tubetti di ottone non si montano.
- 0.20 e attrezzi della sezione 0: niente alimentatore da banco; tester dei servo e sacchetto LiPo nell'inventario.
- 14 (collaudo): niente termometro a infrarossi.
- 9.08 e apertura della sezione 9: tester dei servo per le pose (come lo si alimenta nel corpo resta [C]); 5.01 senza l'alternativa dell'alimentatore da banco; 14.06 con le soglie di batteria in simulazione.
- 0.06, 11.01 e 15.04: carica con il caricatore dell'utente; 0.06 con il T-plug femmina verificato.
- 0.08 e opzioni X (0.15): niente zaino per ora, X3 non si compra.
- 6.22, 02-stampa (diffusore), 0.15 e provino 7 della sezione 1: diffusore bianco, niente PETG fumé.
- 0.23: tolto il totale delle ore.
- Tutto il resto, che dipende dal CAD 2.1.7, è elencato nel piano ("Testi della guida dopo la 2.1.7").
