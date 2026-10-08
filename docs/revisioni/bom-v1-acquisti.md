# Revisione BOM v1 — lente "acquisti e coerenza interna"

Documento rivisto: `docs/BOM.md` versione 1 (8 ottobre 2026). Revisore indipendente. Data: 8 ottobre 2026.
Severità: **bloccante** = comprando o costruendo come scritto qualcosa non funziona o si danneggia; **importante** = rilavorazione probabile, quantità sbagliata, connettore incompatibile, numero diverso dal valore verificato; **minore** = chiarezza.
Stato: revisione completata. 16 finding: 0 bloccanti, 11 importanti (F1–F8, F13–F15), 5 minori (F9–F12, F16).

## Sintesi

Nessuna riga, comprata così com'è, rompe qualcosa. I problemi sono di tre tipi.

1. **Fonti d'acquisto sbagliate o mancanti.** B2 e B3 sono indicati su pololu.com in dollari ma sono a magazzino in UE (F15). I cuscinetti "a 15 € per 20" partono dalla California (F14). Le spine h8 non hanno una fonte al dettaglio (F8). La camera a flat lungo indicata potrebbe non essere un OV3660 (F3).
2. **Righe che portano a un errore nel CAD o nel cablaggio.** Inserti M2,5 "per le schede" quando i Pololu accettano solo M2 (F2); Hobbywing con uscita su spina servo (F7); possibile ritorno di 5 V verso il PC (F6); nessuna basetta per i componenti sciolti (F5).
3. **Numeri che non reggono al ricalcolo.** Il totale di 400 € non si ricostruisce dalle righe: 24 righe su 38 non hanno prezzo, la stima ricostruita è circa 440 € più 40–70 € di spedizioni, e restano fuori servo, SSC-32, batteria, camera e caricabatterie (F4). Il "circa 14 A" di B1 è un'interpolazione marcata V (F1). L'interruttore B3 è dato "ok" a 17,2 A contro un limite di 16 A (F13).

Carrello Pololu consigliato, da confermare aprendo le pagine: tutti e tre i codici da Exp-Tech (Germania), 118,28 € netti.

## Finding

### F1 — B1: "circa 14 A" marcato V, ma è un'interpolazione (importante)
- Voce: B1, Pololu D42V110F6 (#5673), colonna Dato = V.
- Problema: il BOM dà "corrente continua tipica circa 14 A con ingresso 7–8,4 V (letta dal grafico)" e la marca V. Il grafico Pololu non ha la curva a 6 V: il valore è interpolato fra le curve 5 V e 8,4 V. Il dato del costruttore per questo modello è **11 A** (nome del prodotto: "6V, 11A Step-Down Voltage Regulator", nota "At 42 V in"), famiglia 8–15 A.
- Evidenza: `verifica_alimentazione.md` riga 2: "curve presenti: 3.3 / 5 / 8.4 / 12 / 18 V -> NESSUNA curva a 6 V"; verdetto "il valore '~14 A a 6 V' resta un'interpolazione, non un dato del costruttore"; inoltre "misurata in aria libera ... dentro una scocca stampata va declassata".
- Correzione: scrivere "11 A dichiarati (a 42 V in); circa 13,5–14 A stimati per interpolazione a 7–8,4 V, in aria libera" e marcare quel dato S. Nella tabella "Catena elettrica" la colonna Limite di B1 deve dire "11 A dichiarati / circa 14 A stimati". Il margine sullo stallo per lato (8,5 A) resta comunque positivo.

### F2 — D5 / D9: inserti e viti M2,5 "per le schede", ma tre schede su quattro accettano solo M2 o non hanno fori (importante)
- Voce: D5 "Inserti a caldo M2,5 — 70 — fissaggio delle schede"; D9 "schede (M2,5: i fori del clone sono circa 3,0 mm)".
- Problema: l'unica scheda che si fissa con M2,5 è la SSC-32 (4 fori). Le altre: Pololu B1 ha 4 fori da 0,086" = 2,18 mm e B2 ne ha 2 uguali (passa solo una M2); la scheda ESP32 (A2) e l'interruttore B3 non hanno fori. Scritto così, il CAD rischia di mettere inserti M2,5 sotto i Pololu, dove la vite non entra nella scheda. Inoltre si comprano 70 inserti e un assortimento di viti per 4 punti di fissaggio.
- Evidenza: `verifica_alimentazione.md` riga 1 ("0.086" = 2.18 mm (una vite M2 passa, una M2.5 NO)") e riga 6 ("Two 0.086″ mounting holes for #2 or M2 screws"); "Gap chiusi" (#2815 "NON ha fori di fissaggio"); BOM A2 "nessun foro di fissaggio"; `verifica_ssc32.md` riga 8b (fori del clone 2,9–3,0 mm, "prevedere viti M2.5").
- Correzione: nella colonna uso di D5 scrivere "solo SSC-32 (4 pezzi)"; aggiungere a D4 "Pololu B1 e B2: 6 inserti M2"; in D9 togliere "schede" al plurale. Valutare per la SSC-32 4 viti M2,5 passanti con dado (niente confezione da 70) oppure tenere D5 come scorta consapevole.

### F3 — A3: il dato "V" riguarda il modulo standard da 21 mm, ma la riga manda a comprare la variante "75MM", che non è verificata (importante)
- Voce: A3 Camera OV3660, Dove = "versione a flat lungo 75MM: AliExpress 1005008406404365", Dato = "V (modulo standard)".
- Problema: le quote verificate (21 mm, testa 8 × 8 × 5,35, lente 68°) sono di un altro oggetto. L'esistenza di un OV3660 con flat da 75 mm non è confermata: la ricerca indipendente ha trovato OV3660 da 21 e da 80 mm, e flat da 75 mm solo con sensore OV2640. Rischio concreto: arriva un OV2640.
- Evidenza: `verifica_esp32cam_camera.md`, tabella lacune: "Esistenza del modulo OV3660 con flat da 75 mm ... NON VERIFICABILE ... moduli da 75 mm solo con sensore OV2640 ... aprire il link prima di ordinare e chiedere al venditore la lunghezza totale".
- Correzione: Dato = "V solo per il modulo da 21 mm; variante lunga S, C". Aggiungere nella riga: "prima dell'ordine farsi confermare dal venditore sensore (OV3660) e lunghezza del flat". Aggiungere inoltre alla tabella "Aperto" il problema del DVDD (la scheda dà 1,2 V sul pin 10, il sensore chiede 1,5 V ±5 %): la stessa verifica lo chiama "PROBLEMA APERTO" e nel BOM non compare.

### F4 — Costo "circa 400 €": non ricalcolabile dalle righe, e manca tutto ciò che sta fuori dalle sezioni B–E (importante)
- Voce: sezione "Costo indicativo".
- Problema e calcolo:
  - Righe B–D con stato A: 35 (B1–B16 = 16, C1–C6 = 6, D1–D13 con D3-opz = 13), più 3 righe E. Solo 12 hanno un prezzo in euro e 2 un prezzo in dollari; 24 non hanno alcun prezzo (B4, B5, B6, B7, B9, B10, B14, B16, C1, C2, C3, C6, D2, D3-opz, D7–D13, E1–E3).
  - Somma delle righe con prezzo in euro: 2 × 54,89 (B1) + 4 (B8) + 8,99 (B11) + 9,99 (B12) + 11,99 (B13) + 15,99 (B15) + 10,99 (C4) + 10,99 (C5) + 15 (D1) + 9,90 (D4) + 9,19 (D5) + 9,40 + 8,90 (D6) = **235,11 €**, più 18,95 + 8,49 = **27,44 US$** (B2, B3) senza IVA né spedizione.
  - I quattro gruppi citati nel testo fanno 110 + 60 + 55 + 55 = 280 €. I restanti 120 € non sono scomposti e devono coprire B2–B10, B16, C1–C6, D1, D2, D3-opz, D10–D13: con stime prudenti (B2 20, B3 10, B4–B10 22, B16 7, C1–C3 15, C4–C6 26, D1 15, D2 8, D3-opz 10, D10–D13 27) fanno circa 160 €. Totale ricostruito: circa **440 €**, non 400.
  - "Viteria e inserti circa 60 €": i soli inserti fanno 9,90 + 9,19 + 9,40 + 8,90 = 37,39 €; restano 22,61 € per tre assortimenti di viti inox e i dadi (stima reale 30–40 €).
  - Differenza Pololu/Hobbywing: 109,78 − 55,80 = 53,98 €; il testo dà 400 − 340 = 60 €.
  - **Spedizioni non contate**: l'elenco "Dove" porta ad almeno 6–8 venditori diversi (Kamami, pololu.com, Mouser/RS/TME, cnckitchen.store, 3DJake/ruthex, Amazon.it, eBay.de/AliExpress, Melopero/Farnell): ordine di grandezza 40–70 €.
  - **Fuori dal totale**: componenti A con stato "?" (servo, camera, SSC-32, batteria: da 28,19 + 19,99 + circa 6 + 20 × 4,50 = circa 144 € con servo clone fino a oltre 330 € con 18 Tower Pro a 15,50 €), caricabatterie bilanciato e sacca ignifuga.
- Evidenza: righe del BOM; prezzo servo da `verifica_servo_mg90s.md` riga 33 e punto 11.
- Correzione: aggiungere una colonna "prezzo stimato" a ogni riga, una riga "spedizioni", e due totali separati: "B–E" e "tutto ciò che resta da comprare, A e utensili compresi". Scrivere "circa 440–450 € + spedizioni" finché le righe non hanno un prezzo.

### F5 — Manca il supporto dei componenti sciolti e mancano righe nella tabella connettori (importante)
- Voce: B7 (terzo ceramico), B9, B10, C1; tabella "Connettori".
- Problema: partitore, MOSFET con resistenza, ceramico dell'ADC e traslatore di livello non hanno una basetta su cui montarsi: nel BOM non c'è né una millefori né strip di pin 2,54 mm. Nella tabella connettori mancano inoltre: il percorso B2 → ESP32 (pin 5V o spinotto C3), l'alimentazione dei due lati di C1 (LV 3,3 V da quale pin, HV 5 V da B2 o dal pin 5 V della SSC-32), il filo VL e il collegamento ENA → B10.
- Evidenza: righe B7, B9, B10, C1 del BOM confrontate con la tabella "Connettori: chi si accoppia con chi" (nessuna riga per questi collegamenti).
- Correzione: aggiungere una riga "basetta millefori circa 30 × 40 mm + strip maschio/femmina 2,54 mm" e completare la tabella connettori con le quattro righe mancanti.

### F6 — C3 + porta USB "TTL" accessibile: possibile ritorno di 5 V verso il PC (importante, da confermare sullo schema reale)
- Voce: C3 (spinotto USB-C per alimentare la scheda) e ultima riga della tabella connettori ("PC → porta USB-C TTL ... resta accessibile dall'esterno").
- Problema: secondo lo schema del venditore il regolatore 3,3 V è alimentato dalla rete USB_5V. Se il 5 V di B2 entra da una porta USB-C e il PC viene collegato all'altra con la batteria inserita, l'uscita di B2 e il VBUS del PC finiscono sullo stesso nodo. Il BOM non prevede né un diodo né una regola d'uso.
- Evidenza: `verifica_esp32cam_camera.md` riga 7 ("AMS1117-3.3, pin 3 VIN sulla rete USB_5V"; "portare il 5 V del BEC su una porta USB-C"). Che le due porte condividano il VBUS senza diodi non è scritto nella verifica: va guardato sulla scheda.
- Correzione: aggiungere alla domanda 4 la misura di continuità fra i VBUS delle due porte; mettere a BOM un diodo Schottky da almeno 1 A (es. SS14 / 1N5817) in serie a C3, oppure scrivere la regola "PC collegato solo con il 5 V di B2 staccato".

### F7 — B1-alt: i Hobbywing escono su spinotti servo, non su fili da morsetto, e non hanno protezione da inversione (importante se si sceglie l'alternativa)
- Voce: B1-alt, Dato "V (specifiche)".
- Problema: entrambi i modelli hanno l'uscita su cavetti con spina servo da infilare nel ricevitore (il 30603000 ne ha due in parallelo). Per portare 8,5 A ai morsetti VS bisogna tagliare le spine e giuntare, e la sezione dei cavetti non è dichiarata. Il BOM non lo dice e la riga B13 (16 AWG) presuppone piazzole a saldare. Inoltre: polarità invertita = regolatore distrutto; niente pin di abilitazione, quindi B10 non serve e l'arresto del rail a 6,6 V non si può fare via hardware. Il codice "HW30603003" e il prezzo Robitronic 27,90 € non sono stati verificati; il 30603000 risultava "su richiesta" presso l'unico negozio UE trovato.
- Evidenza: `verifica_alimentazione.md` righe 3 e 4 e punto 6 di "Cose sfuggite"; "Non verificato": "Prezzi e giacenze Robitronic ... non riaperti"; `alimentazione.md` (toemen.nl "Op aanvraag").
- Correzione: aggiungere queste tre limitazioni nella riga B1-alt e nella nota su B1; marcare codice e prezzo della versione Car come S.

### F8 — D2: spine "h8" non verificate e difficili da trovare; quelle comuni sono m6 e non entrano a mano nel cuscinetto (importante)
- Voce: D2, spina Ø3 × 10 mm h8 (ISO 2338), Dove = "ferramenta, Amazon.it".
- Problema: nessuna inserzione concreta; la tolleranza h8 per il nominale 3 mm non è stata confermata su fonte primaria. Le spine più diffuse in commercio (temprate DIN 6325 / ISO 8734, e molte ISO 2338 inox) sono m6 (+0,002/+0,008 mm): nel foro P0 del cuscinetto (−0,008/0) danno sempre interferenza 0,002–0,016 mm. Forzare una spina in un 3 × 7 × 3 lo rovina.
- Evidenza: `verifica_giunti_stampa.md` riga 7 (verdetto "non verificabile"; "farsi dare dal venditore la tolleranza in mm e misurare le spine col micrometro"); `giunti_stampa.md` ("la misura 3 x 10 [m6] è a catalogo da Ludwig Meister e Bossard").
- Correzione: indicare un articolo preciso con tolleranza dichiarata (vedi sezione "Disponibilità" più sotto). Piano B da scrivere nel BOM: asta rettificata o perno ricavato da vite M3 con gambo liscio, oppure spina m6 con sede del cuscinetto verificata su un campione.

### F9 — B10: funzione della resistenza non indicata, rail acceso di default (minore)
- Voce: B10 "MOSFET N a segnale, es. 2N7000 (+ 1 resistenza 10 kΩ)".
- Problema: non è scritto dove va la resistenza. Se finisse fra ENA e massa il rail non si accenderebbe mai (partitore con i due pull-up da 1 MΩ in parallelo: 8,4 V × 10/(500 + 10) = 0,16 V). Come pull-down di gate è corretta, ma allora con l'ESP32 in reset o bloccato il rail resta acceso: lo spegnimento per sottotensione non è a prova di guasto. Il 2N7000 ha soglia massima 3,0 V: con 3,3 V di gate funziona (servono circa 17 µA) ma senza margine; un BSS138 o un 2N7002 è più adatto.
- Evidenza: `verifica_alimentazione.md` riga 1 (ENA con pull-up 1 MΩ a VIN) e punto 5 di "Cose sfuggite" ("il rail servo resta ACCESO ... non è fail-safe").
- Correzione: scrivere "10 kΩ fra gate e massa"; dichiarare nel BOM che il default è acceso e che la protezione indipendente è il cicalino B8.

### F10 — B5: due codici in alternativa nella stessa riga (minore)
- Voce: B5 "0FHM0002ZXJ (12 AWG) o 0FHM0001ZXJ (14 AWG)".
- Problema: una riga d'ordine deve avere un codice solo. Con B12 e B11 a 14 AWG il codice coerente è **0FHM0001ZXJ**. Mancano inoltre due avvertenze della verifica: le code sono in cavo GXL da 94 mm da giuntare (saldatura + termorestringente) e il portafusibile va fissato al telaio, non lasciato appeso.
- Evidenza: `verifica_alimentazione.md` riga 8 ("0FHM0001ZXJ 14 AWG Black 94 94 GXL No"; "Fuse holders should not be placed under tension").
- Correzione: lasciare solo 0FHM0001ZXJ e aggiungere le due note; prevedere una sede con fascetta nel CAD.

### F11 — Piccole incoerenze fra tabelle (minore)
- B15: il BOM dice "puntalini 0,25–2,5 mm²"; l'articolo citato (B0FPDZ8SGR) è "1800 pezzi, 0,25–10 mm²" (`batteria_cablaggio.md`). Servono 6 puntalini in tutto (4 × 16 AWG = 1,5 mm² e 2 × 22 AWG = 0,34 mm² sui morsetti della SSC-32).
- D6: quantità "100" con due articoli diversi (M3 × 5,7 a 9,40 € e M3 × 3 a 8,90 €): scrivere 100 + 100 oppure sceglierne uno.
- D3-opz: l'ASIN noto (B0D6GDBYGS) è di amazon.com, non di Amazon.it; compatibilità, prezzo e disponibilità in Italia "non verificabili" (`verifica_servo_mg90s.md` riga 22). Con stato "A (opzionale)" finisce nel carrello: metterlo a "—" finché la domanda 5 non ha risposta.
- A1: nella colonna Dove mancano le due fonti UE controllate: Botland DNG-24408 (Tower Pro, 15,50 €, non a magazzino l'8/10 e avviso "B2B") e TinyTronics (clone Sky Star con datasheet, 4,50 € da 20 pezzi, "500+ in stock") (`verifica_servo_mg90s.md` riga 33 e punto 11).
- Catena elettrica, riga Batteria "6,4–8,4 V" contro soglia di arresto 6,6 V e contro "ingresso ≥ 6,3 V" di B1: a 11 A la caduta fra batteria e regolatore è circa 0,013 Ω × 11 A (interruttore) + 0,036 V (cavo) + fusibile e spina ≈ 0,2 V, quindi a 6,4 V di batteria il regolatore vede circa 6,2 V e il rail scende sotto 6,0 V. Usare 6,6 V come minimo operativo in tutta la tabella.
- Tabella pin: "Liberi: 2" ma `dimensioni-componenti.md` indica GPIO2 = LED "ON" della scheda; la frase "tutti verificati sul datasheet Espressif" vale per il chip, mentre la mappa della UICPAL poggia sull'inserzione (`verifica_esp32cam_camera.md` riga 1).
- T-plug "25 A (Amass AM-1015E)": dato non ricontrollato (`verifica_batteria_cablaggio.md`, "NON verificate": affermazione 23) e comunque riferito a un connettore diverso da quello che si compra (B11 generico).
- B8: il cicalino sta sulla presa di bilanciamento, a monte dell'interruttore B3: resta alimentato anche a robot spento. Scrivere di staccarlo (o di togliere la batteria) a fine uso.
- B3: nessuna nota su come si collegano i fili da 14 AWG. La verifica riporta che sopra i 5 A vanno usati i fori grandi e che i morsetti inclusi sono dati per 16 A; il diametro dei fori rispetto al 14 AWG non è verificato. A 11 A la scheda dissipa circa 1,5 W: non va a contatto con una parete stampata.

### F12 — Consumabili e utensili che mancano (minore, ma fermano il lavoro)
- Stagno e flussante; una punta per inserti a caldo M2 / M2,5 / M3 (con la punta conica del saldatore gli inserti M2 entrano storti).
- Cavo **micro-USB** dati per la SSC-32 (il BOM elenca solo l'USB-C): serve per leggere versione e baud e per tarare i servo dal PC.
- Cavo di carica con T-plug per il caricabatterie (si può fare con una delle 3 coppie di B11: scriverlo).
- Fusibili MINI di taglia minore (5 A e 10 A) per la prima accensione al banco: B4 dice solo "20 A + scorta".
- Micrometro o almeno calibro centesimale per le spine D2 (lo chiede la verifica).
- Rondelle M2 sotto la testa delle viti delle alette (plastica del servo) e colla per i piedini in TPU, se non sono a incastro.

### F13 — Catena elettrica, riga "Interruttore B3": esito "ok" in contraddizione con il limite scritto nella stessa riga (importante)
- Voce: tabella "Catena elettrica", riga Interruttore B3; riga Fusibile; riga Morsetto VS.
- Problema: la riga dà 17,2 A in stallo totale contro un limite di "16 A a 150 °C" e conclude "ok ... lo stallo totale è sopportato solo per decine di secondi". Il "decine di secondi" non ha alcuna fonte: né `verifica_alimentazione.md` né `alimentazione.md` contengono una durata. Il fusibile da 20 A in quella condizione è all'86 % e non interviene, quindi nulla protegge l'interruttore. Stesso schema per il morsetto VS: 8,5 A di stallo per lato contro "3–5 A continui raccomandati", esito "ok sulla carta".
- Evidenza: `verifica_alimentazione.md` riga 5 ("Continuous current at 150°C 16 A"; "i 16 A portano la scheda a 150 °C"; "Do not use this switch as an emergency cutoff"); calcolo 17,2 / 16 = 108 % del limite; 17,2 / 20 = 86 % del fusibile.
- Correzione: cambiare l'esito in "ok in marcia e sui picchi; NON coperto in stallo totale prolungato" e scrivere la contromisura: tempo massimo di stallo nel firmware (il rail si spegne da B10) oppure fusibile da 15 A (picco realistico 11 A = 73 %; stallo 17,2 A = 115 %). Togliere "decine di secondi" o misurarlo al banco.

### F14 — D1: i "circa 15 € per 20 pezzi" sono un'inserzione che spedisce dagli Stati Uniti (importante)
- Voce: D1, Dove = "eBay.de, AliExpress, Amazon.it: circa 15 € per 20 pezzi".
- Problema: l'unica inserzione da 20 pezzi nota (eBay.de 157288484750) risulta, dal riepilogo di ricerca letto oggi, a 17,70 US$ (circa 15,11 €), spedizione indicata gratuita, venditore a Rancho Cucamonga, California, ultimo aggiornamento settembre 2025. Arriva quindi da fuori UE: IVA 22 % al checkout (15,11 × 1,22 = 18,43 €), tempi lunghi, cuscinetti senza marca. Per Amazon.it la ricerca non ha mai trovato un'inserzione; nessuna confezione da 20 con magazzino UE trovata.
- Evidenza: vedi "Disponibilità" (b); `giunti_stampa.md` ("una ricerca mirata non ha restituito NESSUNA inserzione amazon.it").
- Correzione: togliere "Amazon.it" finché non c'è un link; scrivere "eBay.de 157288484750, spedizione dagli USA, 2–4 settimane" e ordinare per primi i cuscinetti (sono il pezzo con la consegna più lunga). Alternativa in giornata ma costosa: RS PRO SF683ZZ, 18 × 11,72 = 210,96 € (prezzo non ricontrollato).

### F15 — B2 e B3: il BOM manda su pololu.com in dollari, ma ci sono a magazzino in UE; per B1 esiste una seconda fonte (importante)
- Voce: B2 "pololu.com 18,95 US$; disponibilità da Kamami da controllare"; B3 "pololu.com 8,49 US$; rivenditori UE da controllare"; B1 "Kamami, 2 pezzi".
- Problema: ordinando da pololu.com si pagano spedizione dagli USA, IVA 22 % all'importazione e diritti di sdoganamento su due pezzi da 27 US$. I dati letti oggi (sezione "Disponibilità" (a)) mostrano tutti e tre i codici presso rivenditori UE. Per B1 la giacenza Kamami (2 pezzi su 2 necessari) non lascia margine.
- Correzione: riscrivere la colonna Dove così: B1 = Kamami 54,89 € (2 pezzi) oppure Exp-Tech 48,50 € + IVA (5 pezzi); B2 = Botland 14,90 € oppure Exp-Tech 15,69 € + IVA; B3 = Eckstein 8,03 € oppure Exp-Tech 5,59 € + IVA. Carrello unico possibile: **Exp-Tech (Germania)**, 2 × 48,50 + 15,69 + 5,59 = 118,28 € netti, cioè 140,75 € con IVA al 19 % o 144,30 € al 22 %, più una sola spedizione. In alternativa tre carrelli (Kamami 109,78 + Botland 14,90 + Eckstein 8,03 = 132,71 €) con tre spedizioni. I numeri Exp-Tech ed Eckstein vengono da riepiloghi di ricerca: aprire le pagine prima di ordinare.

### F16 — Altre note di coerenza (minore)
- Tabella connettori: "B1 e B2 accettano anche morsetti passo 5 mm". Per B1 è confermato (`verifica_alimentazione.md` riga 1); per B2 la verifica non lo dice (riga 6) e il D24V22F5 è una scheda da 17,8 mm con piazzole a passo 2,54 mm: togliere B2 dalla frase o controllare sulla pagina Pololu.
- B3: il #2815 arriva con due morsetti a 2 poli passo 5 mm inclusi (dati per 16 A): con il puntalino da 2,5 mm² il 14 AWG si collega senza saldare. Scriverlo nella riga, perché la tabella connettori dice solo "saldatura".
- B6: "uno su ciascun morsetto VS" significa stringere nello stesso morsetto il puntalino del 16 AWG e il reoforo del condensatore. Decidere dove si salda davvero (per esempio sulle piazzole d'uscita di B1) e prevedere il fissaggio meccanico di un cilindro Ø12,5 × 20 mm.
- Nota su B1: "gli Hobbywing costano circa la metà" è vero solo per la versione Car a 27,90 € (non verificato); la differenza reale è 53,98 €.

## Disponibilità dall'Italia, letta l'8 ottobre 2026 (10 chiamate web)

Legenda: **(P)** = pagina del negozio letta tramite lo strumento di lettura web; **(R)** = dato preso dal riepilogo di un motore di ricerca, pagina non aperta: da ricontrollare.

### (a) Pololu #5673, #2858, #2815 presso rivenditori UE
| Codice | Negozio | Prezzo | Giacenza | URL | Come letto |
|---|---|---|---|---|---|
| #5673 D42V110F6 | Kamami (PL) | non letto | non letta | https://kamami.pl/en/step-down/1201579-6v-11a-step-down-voltage-regulator-d42v110f6-5902186330856.html | (P) **pagina letta solo in parte**: il testo (127 533 caratteri) è stato troncato a 100 000, prima del blocco prezzo. Resta la lettura del verificatore di oggi: 54,89 € IVA inclusa, 2 pezzi |
| #5673 D42V110F6 | Exp-Tech (DE) | 48,50 € IVA esclusa (SKU 80-5673) | "only 5 units left", InStock | https://exp-tech.de/en/products/6v-11a-step-down-voltage-regulator-d42v110f6 | (R) |
| #2858 D24V22F5 | Botland (PL) | 14,90 € | "Available", "Shipping in 24 hours" (numero di pezzi non indicato) | https://botland.store/converters-step-down/4978-step-down-voltage-converter-d24v22f5-5v-25a-pololu-2858-5904422365769.html | (P) pagina dei risultati di ricerca Botland, codice PLL-04978 |
| #2858 D24V22F5 | Exp-Tech (DE) | 15,69 € IVA esclusa | 8 pezzi | https://exp-tech.de/en/products/pololu-5v-25a-step-down-voltage-regulator-d24v22f5 | (R) |
| #2858 D24V22F5 | Eckstein (DE) | 22,55 € IVA 19 % inclusa | 5 pezzi | https://eckstein-shop.de/Pololu5V2C25AStep-DownSpannungsreglerD24V22F5EN | (R) |
| #2858 D24V22F5 | Kamami (PL) | — | la ricerca interna per "D24V22F5" non restituisce il prodotto | https://kamami.pl/en/search?controller=search&s=D24V22F5 | (P) esito negativo, ma vedi nota |
| #2815 HP | Eckstein (DE) | 8,03 € IVA inclusa (netto 6,75 €) | "disponibile subito" | https://eckstein-shop.de/Pololu-Big-MOSFET-Slide-Switch-with-Reverse-Voltage-Protection-HP-EN | (R) |
| #2815 HP | Exp-Tech (DE) | 5,59 € IVA esclusa (un'altra pagina dello stesso negozio: 6,24 €, 3 pezzi) | "In stock (19 units)" | https://exp-tech.de/en/products/pololu-big-mosfet-slide-switch-with-reverse-voltage-protection-hp | (R) |
| #2815 HP | Kamami (PL) | non letto | non letta | https://kamami.pl/en/digital-switches/561032-pololu-2815-big-mosfet-slide-switch-with-reverse-voltage-protection-hp.html | (R) la pagina esiste; la ricerca interna Kamami per "Big MOSFET Slide Switch" rispondeva "No matching products found" (P) |
| #2815 HP | Botland (PL) | non letto | non letta | https://botland.store/digital-switches/5120-large-switch-slide-mosfet-hp-45-40v16a-with-protection-before-reverse-current-pololu-2815-5903351244886.html | (R) la pagina esiste; la ricerca interna Botland per "Pololu 2815" rispondeva "Found products: 0" (P): probabile articolo non ordinabile |

Nota: le ricerche interne di Kamami e Botland non hanno trovato articoli che hanno comunque una pagina; un esito negativo di quelle ricerche non prova l'assenza a catalogo. Spedizione verso l'Italia: non letta per nessuno dei quattro negozi.

### (b) Cuscinetti F683ZZ, confezione da circa 20
- eBay.de 157288484750, "F683ZZ Flanschkugellager 3x7x3 mm geschirmt Chromstahl Flanschlager 20 Stück": **pagina non leggibile (HTTP 403)**. Dal riepilogo di ricerca (R): 17,70 US$ (circa 15,11 €), prezzo precedente 22,13 US$, spedizione indicata gratuita, venditore a Rancho Cucamonga (California), aggiornata a settembre 2025. Spedizione verso l'Italia: non dichiarata nel riepilogo.
- eBay.de, inserzione multi-misura da Shenzhen con variante F683ZZ: 5,39 € per 10 pezzi (R); spedizione UE non dichiarata. https://www.ebay.de/itm/405019293156 oppure https://www.ebay.de/itm/176296261457 (il riepilogo non dice quale delle due).
- Nessuna confezione da 20 con magazzino in UE trovata. Amazon.it, AliExpress, kugellager-express.de: non controllati.

### (c) Spine Ø3 × 10 mm h8
- SFS (Svizzera), articolo 133670 "Zylinderstifte h8 ISO 2338 - rostfrei A1 3 h8x10": 8,90 CHF per 100 pezzi netti, **ordine minimo 500 pezzi**, 3 400 a magazzino (R). https://www.sfs.ch/CH/en/dl/p/133670 . Fuori UE e per aziende: non praticabile, ma conferma che l'articolo "ISO 2338 h8 A1 3 × 10" esiste a catalogo.
- eBay.de: le inserzioni ISO 2338 comparse dichiarano in più casi la tolleranza m6; nessuna 3 × 10 h8 (R).
- Nessun negozio italiano o UE con piccole quantità trovato in una ricerca: la riga D2 resta senza fonte d'acquisto.

### (d) Inserti a caldo, (e) portafusibile Littelfuse FHM, (f) traslatore BSS138
Non controllati dal vivo: le 10 chiamate sono finite sui punti (a)–(c). Per (d) restano i prezzi letti oggi dal verificatore sul listino di cnckitchen.store (M2 × 3 9,90 €; M2,5 × 4 9,90 €; M3 × 5,7 9,40 €; M3 × 3 8,90 €; spedizione non letta). Suggerimento senza chiamate: lo stesso negozio ha anche l'M2,5 × 4, quindi i tre formati stanno in un solo ordine invece di due (cnckitchen.store + 3DJake/ruthex). Per (e) e (f) non esiste alcuna lettura di prezzo o giacenza, né mia né del verificatore: "Mouser, RS, TME" e "Melopero, Farnell 2301651" sono solo nomi.

## Controllato e trovato corretto
- A1: 13,4 g, 1,8 kgf·cm a 4,8 V, 2,2 a 6,6 V, tensione dichiarata 4,8 V, cavo 25 cm JR: coincidono con `verifica_servo_mg90s.md` righe 1–4 e 26.
- A2: 62,6 × 28,3 mm, circa 67,5 con l'antenna, nessun foro: coincidono con `verifica_esp32cam_camera.md`; etichetta S/C corretta.
- A4: etichetta "S (solo venditore), C" corretta; 72 × 55 mm dentro l'intervallo rimisurato (71,5–74 × 54,5–56,5).
- A5: quote, peso, 12 AWG, JST-XH, 19,99 €: coincidono con `verifica_batteria_cablaggio.md` righe 2–4 e 1+10.
- B1: codice #5673, 6–60 V, 6 V ±3 %, caduta 0,27 V a 8 A, 31,8 × 43,2 × 9 mm, 15 g, fori M2 a 38,9 × 25,4 mm, 59,95 US$, Kamami 54,89 €: confermati (resta F1 sul "14 A").
- B2 (#2858) e B3 (#2815): tutte le specifiche della riga coincidono con `verifica_alimentazione.md` righe 6 e 5, compreso il PCB 20,3 × 22,9 mm senza fori.
- B5: abbinamento codice/sezione dei due FHM confermato (riga 8). B4 MINI e B5 FHM sono compatibili fra loro.
- B9: 8,4 × 47/147 = 2,69 V, dentro 0–2,9 V (campo confermato in `verifica_esp32cam_camera.md` riga 4): l'etichetta V è giusta.
- D1: 3 × 7 × 3, flangia Ø8,1 × 0,8, avviso sulla versione aperta: confermati (`verifica_giunti_stampa.md` righe 4–5).
- D4, D5, D6: lunghezze e prezzi (9,90; 8,99 su ruthex.de; 9,40 / 8,90) confermati; etichetta "S (quote), V (lunghezza)" corretta.
- Aritmetica della catena elettrica: 50 × 5,2 = 260 A; 17,03 × 6 / (0,9 × 6,6) = 17,2 A; 17,2 / 20 = 86 %; 11 / 20 = 55 %; 9 × 0,946 = 8,5 A; 2 × 36 − 2 × 15 = 42 g.
- SSC-32: ordine dei morsetti, ordine dei pin servo, canali 0–15 su VS1 e 16–31 su VS2, ponticelli da togliere: coerenti con `verifica_ssc32.md` righe 4 e 8c.
- Livelli logici (2,64 V contro 3,0 V; massimo 3,6 V) e scelta dei GPIO 21 / 47 / 1 / 42: coerenti con le verifiche e con la mappa pin di `dimensioni-componenti.md`.
- Quantità: 18 cuscinetti e 18 spine per 18 giunti; 36 dadi M2 necessari contro circa 50; 10 prolunghe necessarie contro 20; massa dei regolatori nel bilancio (30 g) uguale al BOM.

## Non controllato
- Dal vivo: inserti (d), portafusibile FHM (e), traslatore BSS138 (f); spese di spedizione di ogni negozio; tutti gli ASIN Amazon.it (B0FVRHF7GW, B075M578PB, B0D9VDPG54, B0FPDZ8SGR, B087289HFS, B0C61PDHDF, B098P5ZBJ6); inserzioni AliExpress di A2, A3, A4; Robitronic; RS PRO SF683ZZ.
- Prezzo e giacenza Kamami del #5673: pagina troncata, non riletti.
- Condensatore EEUFR1C222, bilanciere R13-112, cicalino BX100, 2N7000: nessuna verifica esistente e nessuna mia.
- Correttezza della geometria e delle coppie (`docs/dimensionamento.md`): fuori dalla mia lente.
- Disponibilità e prezzo dei filamenti E1–E3.
