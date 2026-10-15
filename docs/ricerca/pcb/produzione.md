# PCB su misura: produzione e costi (studio preliminare)

Studio del 16 ottobre 2026 per sostituire le tre millefori (basetta dell'ESP32 56 × 35, scheda del carapace 20 × 30 che nella 2.1.7 si allunga, striscia dei partitori 9 × 4 fori). Solo produzione, costi, regole e flusso di lavoro: il disegno vero si fa in una versione successiva. Nessun acquisto: ogni voce è una proposta.

Stati: **V** verificato sulla fonte (pagina letta oggi), **S** stimato (calcolo o fonte di terzi), **C** da confermare (con il preventivo vero, il giorno dell'ordine).

Valuta: i produttori cinesi danno i prezzi in dollari. Dove serve, 1 $ ≈ 0,86 € [S, cambio indicativo di ottobre 2026: da rifare il giorno dell'ordine].

## 0. Cosa c'è da fare (dati del progetto)

| Dato | Valore | Fonte | Stato |
|---|---|---|---|
| Basetta dell'ESP32 | 56 × 35 mm, quattro colonnine Ø 5,8 | `guida/schemi/schemi.md:25`, `:31` | V |
| Scheda del carapace | 20 × 30 mm oggi, da allungare per la testata 2 × 8 a 90° (2.1.7) | `guida/schemi/schemi.md:249`, S-01 | V oggi, C misura nuova |
| Striscia dei partitori | 9 × 4 fori = 22,86 × 10,16 mm | `guida/schemi/schemi.md:439` | V |
| Corrente massima sulle schede | ramo logica protetto da F2 da 2 A; regolatore D24V22F5 da 2,5 A; LED dietro un PTC MF-R075 (0,75 A di tenuta) | `docs/cablaggio.md:27`, `:75`; `docs/BOM.md:43`; `guida/schemi/schemi.md:48` | V |
| Corrente dei partitori | circa 2 mA in tutto | `guida/schemi/schemi.md:444` | S |

Le correnti dei servo (rail da 14 AWG, fino a 13 A per lato, `docs/cablaggio.md:74`) **non passano** su nessuna di queste schede: restano sui fili, sui Wago e sulla SSC-32. Quindi le piste da 2–5 A del capitolo 4 servono solo come margine sul 5 V e sulla massa.

## 1. Produttori per pochi pezzi (5–10 schede)

### 1.1 Prezzi della sola scheda

Aree di riferimento: **50 × 40 mm = 20 cm² = 3,1 pollici²** e **100 × 60 mm = 60 cm² = 9,3 pollici²**. Le formule pubblicate si applicano qui sotto; i numeri senza formula pubblica sono quelli del sito, da rifare nel preventivo vero.

| Produttore | Dove | Formula o prezzo pubblicato | 50 × 40, 2 strati | 100 × 60, 2 strati | 50 × 40, 4 strati | 100 × 60, 4 strati | Pezzi | Stato |
|---|---|---|---|---|---|---|---|---|
| JLCPCB | Cina (Shenzhen) | 1–4 strati, 5 pezzi fino a 100 × 100: "From $2.00" ([confronto JLCPCB](https://jlcpcb.com/ads/pcb-manufacturer-comparison)); 4 strati 10 × 10 "start at just $7" con buono ([pagina prototipi](https://jlcpcb.com/features/prototype-pcb-way)) | 2–5 $ per 5 pezzi | 2–5 $ per 5 pezzi | 2–10 $ per 5 pezzi | 7–20 $ per 5 pezzi | minimo 5 | V prezzo d'ingresso; S i valori per le nostre misure; C buoni |
| PCBWay | Cina (Shenzhen) | 2 strati, 10 pezzi fino a 100 × 100: 5 $ ([PCBWay](https://www.pcbway.com/)) | ~5 $ per 10 | ~5 $ per 10 | 20–40 $ per 5–10 | 30–60 $ per 5–10 | minimo 5 | V 2 strati (prezzo pubblicizzato, non datato); S 4 strati |
| Aisler | Germania (UE) | prezzo = quota d'ordine + area × tariffa × pezzi; 2 strati HASL Budget 12 € + 0,067 €/cm²; 4 strati ENIG Budget 14 € + 0,13 €/cm² ([listino Aisler](https://community.aisler.net/t/our-simple-pricing/102), post del 27 agosto 2023) | 20,04 € per 6; 24,06 € per 9 | 36,12 € per 6; 48,18 € per 9 | 29,60 € per 6; 37,40 € per 9 | 60,80 € per 6; 84,20 € per 9 | multipli di 3 | V formula (ma del 2023, e una versione della stessa pagina dà 10 € + 0,0525 €/cm²); S i totali; C listino di oggi. IVA esclusa |
| Eurocircuits | Belgio (UE), servizio "PCB Proto" | solo dal calcolatore sul sito, nessun listino pubblico ([PCB Proto](https://www.eurocircuits.com/pcb-assembly-proto/)) | 50–90 € per 2–5 | 70–120 € per 2–5 | 90–150 € per 2–5 | 120–200 € per 2–5 | 1–5 | S (ordine di grandezza dei prezzi europei, non letto sul calcolatore); C |
| OSH Park | USA (Oregon) | 2 strati 5 $/pollice², 4 strati 10 $/pollice², a gruppi di 3 ([OSH Park](https://docs.oshpark.com/services/)) | 15,50 $ per 3; 31 $ per 6 | 46,50 $ per 3; 93 $ per 6 | 31 $ per 3; 62 $ per 6 | 93 $ per 3; 186 $ per 6 | multipli di 3 | V formula; S i totali |

Note:
- **JLCPCB e PCBWay** hanno il prezzo a gradino: fino a 100 × 100 costa uguale, quindi due delle nostre schede costano quanto una. Si possono ordinare **separate** (un ordine per scheda: 2 $ l'una) oppure in un **pannello** con più disegni (JLCPCB lo fa pagare di più come "different designs") [S].
- **4 strati**: per queste schede non servono (capitolo 4): poche reti, nessun segnale veloce oltre l'I2C a 400 kHz e la seriale. Il 4 strati dà un piano di massa intero, ma con 2 strati e un riempimento di massa sul retro si arriva al risultato [S].
- **Tutti e cinque** fanno di base 1,6 mm (Eurocircuits 1,55), verde con serigrafia bianca. Rame esterno finito da 1 oz (35 µm) da JLCPCB, PCBWay e OSH Park; Eurocircuits dichiara 18 µm di base sugli strati esterni, prima della metallizzazione [V, pagine delle capacità linkate nel capitolo 3].

### 1.2 Spedizione, dogana e IVA in Italia (ottobre 2026)

Cosa vale oggi per un privato in Italia:

| Voce | Dal 1° luglio 2026 | Fonte | Stato |
|---|---|---|---|
| IVA all'importazione | 22 % sempre, anche sotto i 150 €. Con l'IOSS la paga il venditore alla cassa e il pacco arriva senza altro da pagare per l'IVA | [JLCPCB, regole IVA UE](https://jlcpcb.com/help/article/eu-vat-e-commerce-rules-%26-adjustments) (aggiornata il 22 aprile 2026) | V |
| Soglia IOSS di JLCPCB | ordini di privati fino a **170 $**: IVA alla cassa; oltre, IVA e dazio alla dogana tramite il corriere | stessa pagina; [dogane e tasse](https://jlcpcb.com/help/article/customs,-duties-and-taxes) (9 settembre 2026) | V |
| Dazio UE sotto i 150 € | **3 € per voce doganale** (dazio forfettario temporaneo, fino al 30 giugno 2028). L'IOSS non lo copre: lo paga il destinatario alla consegna, o lo anticipa il corriere | [JLCPCB, riforma doganale UE](https://jlcpcb.com/news/eu-customs-reform-2026) (27 giugno 2026); Reg. (UE) 2026/382 citato da [vatcalc](https://vatcalc.com/eu/eu-clarifies-vat-on-new-e3-customs-duty-on-low-value-imports) | V |
| Dazio sopra i 150 € | tariffa doganale normale (per i circuiti stampati nudi di solito 0 %, ma con sdoganamento formale e spese del corriere) | pagina JLCPCB sulla riforma; aliquota dei PCB: da controllare sulla TARIC (voce 8534) | V regola; C aliquota |
| Contributo italiano di 2 € | sui pacchi extra UE fino a 150 €, legge di bilancio 2026 (L. 199/2025, commi 126–129); rinviato più volte, ora dal **1° dicembre 2026** (DL 17 settembre 2026, n. 162) | [Fiscal Focus, 17 settembre 2026](https://www.fiscal-focus.it/quotidiano/il-quotidiano/articoli-fisco/mini-pacchi-extra-ue-la-tassa-da-2-euro-slitta-al-1deg-dicembre,3,188064); [MySolution, 21 settembre 2026](https://www.mysolution.it/fisco/informazioni/news/2026/09/21/pacchi-extra-ue.-nuova-proroga-per-il-contributo-nazionale-di-2-euro) | V data di oggi; C se slitta ancora |
| Spese del corriere | DHL, UPS e FedEx fanno pagare una commissione quando anticipano dazio o IVA; variano per paese e corriere | pagina JLCPCB sulla riforma | V esistenza; C importo (in Italia di solito 10–20 €, S) |
| Aisler, Eurocircuits | **dentro l'UE**: niente dogana, niente dazio. IVA italiana inclusa alla cassa | [Aisler, spedizioni](https://community.aisler.net/t/a-quick-primer-about-shipping-at-aisler/672) | V |
| OSH Park | dagli USA: dazio di 3 € e IVA 22 % alla consegna, più la commissione del corriere (OSH Park non dichiara l'IOSS) | regola UE sopra | S |

Spedizione:

| Produttore | Spedizione verso l'Italia | Tempo di viaggio | Fonte | Stato |
|---|---|---|---|---|
| JLCPCB | a scelta alla cassa: linee economiche ("Global Standard Direct Line", poche unità di dollari) o DHL/UPS/FedEx Express (circa 20–30 $). Un utente tedesco riceve con la linea diretta e i dazi prepagati, senza pagare alla porta | 7–15 giorni lavorativi la linea economica, 3–5 l'express | [pagina spedizioni JLCPCB](https://JLCPCB.com/help/article/65-Shipping-Info) (2023); [EEVblog](https://www.eevblog.com/forum/manufacture/jlcpcb-shipping/msg5538881/); [PedalPCB](https://forum.pedalpcb.com/threads/jlcpcb-and-tariffs.25071/post-333100) | S costi; C alla cassa |
| PCBWay | simile a JLCPCB, DHL di solito 20–30 $ | 3–7 giorni con DHL | nessuna fonte di oggi | S, C |
| Aisler | **gratis** con Deutsche Post o DHL Warenpost (senza tracciamento); a pagamento DHL Parcel e UPS | Warenpost 4–14 giorni lavorativi; UPS Express 1–5 | [Aisler, spedizioni](https://community.aisler.net/t/a-quick-primer-about-shipping-at-aisler/672) | V |
| Eurocircuits | corriere a pagamento, calcolato all'ordine | 1–3 giorni nell'UE | [Eurocircuits, costi di trasporto](https://www.eurocircuits.com/blog/how-transport-costs-are-calculated/) | C |
| OSH Park | **gratis** in tutto il mondo (posta USPS) | 1–3 settimane, più la dogana | [OSH Park](https://docs.oshpark.com/services/) | V gratis; S tempo |

**Come si legge per noi** [S]: un ordine JLCPCB di sole schede nude da 5–15 $ sta sotto i 150 € e sotto i 170 $. Alla cassa si paga l'IVA; alla consegna restano il dazio di 3 € per voce (le schede nude di disegni diversi possono contare come voci diverse: C) e, dal 1° dicembre 2026, i 2 € italiani. Per tre disegni separati il costo di dogana può superare quello delle schede. **Un solo ordine con le tre schede in un pannello** riduce le voci; oppure si prende Aisler, che costa di più in partenza ma non ha dogana.

### 1.3 Tempi

| Produttore | Fabbricazione 2 strati, 5–10 pezzi | 4 strati | Totale fino a casa (stima) | Fonte | Stato |
|---|---|---|---|---|---|
| JLCPCB | 24 ore per 5 pezzi, 1–2 giorni per 6–10 | 2–5 giorni | 8–15 giorni con la linea economica, 5–7 con l'express | [JLCPCB, tempi di produzione](https://jlcpcb.com/help/article/pcb-fabrication-services-and-production-time) (9 settembre 2026) | V fabbricazione; S totale |
| PCBWay | 24 ore pubblicizzate | 3–5 giorni | 6–12 giorni | [PCBWay](https://www.pcbway.com/) | S |
| Aisler | 1 giorno lavorativo (Beautiful Boards); progetti in generale 2 | n.d. | 5–16 giorni lavorativi con la spedizione gratuita | [aisler.net](https://aisler.net/en) | V fabbricazione; S totale |
| Eurocircuits | 2–3 giorni lavorativi (PCB Proto) | uguale | 4–6 giorni lavorativi | [PCB Proto](https://www.eurocircuits.com/pcb-assembly-proto/) | V fabbricazione; S totale |
| OSH Park | 9–12 giorni di calendario (Prototype); 4–5 lavorativi (Super Swift, doppio prezzo) | 9–14 giorni | 3–5 settimane | [OSH Park](https://docs.oshpark.com/services/) | V fabbricazione; S totale |

## 2. Montaggio

### 2.1 Montaggio fatto dal produttore (PCBA)

**JLCPCB**, listino del montaggio aggiornato al 9 settembre 2026 ([prezzi del montaggio](https://jlcpcb.com/help/article/pcb-assembly-price)) [V]:

| Voce | Economic (fino a 50 schede, una faccia, parti da 0402 in su) | Standard |
|---|---|---|
| Messa in macchina | 8,18 $ | 25,56 $ una faccia, 51,12 $ due facce |
| Stencil (resta a JLCPCB) | 1,53 $ | 8,21 $ / 16,42 $ |
| Pannello con più disegni | 8,21 $ | 8,21 $ |
| SMD | 0,0016 $ a giunto | uguale fino a 50 000 giunti |
| Montaggio a mano (THT) | 0,0164 $ a giunto **più 3,58 $ a ordine** | uguale |
| Caricamento dei componenti | **Basic e Preferred Extended gratis**; 3,07 $ per ogni Extended diverso | 1,53 $ per ogni parte diversa |
| Conferma della posizione dei componenti | 0,45 $ | 0,45 $ |
| Componenti | prezzo LCSC del giorno | uguale |

Altre regole [V, [blog JLCPCB del 13–14 ottobre 2026](https://jlcpcb.com/blog/reduce-pcb-assembly-cost-prototype)]:
- si fabbricano almeno 5 schede, se ne montano anche solo 2;
- Economic copre da 2 a 50 pezzi; tempi 1–3 giorni di montaggio, Standard 4 o più;
- i componenti che JLCPCB non ha in magazzino si comprano con "Global Sourcing", ma con il minimo d'ordine del distributore (nell'esempio del blog 443 pezzi per usarne 10): **da evitare**.

Librerie dei componenti [S, fonti di terzi, conteggi che cambiano ogni giorno: [elenco Basic](https://jlcpcb.com/parts/basic_parts)]:
- **Basic**: circa 700 parti comuni (resistenze e condensatori 0402–1206, diodi, transistor, regolatori e logiche diffuse), sempre caricate;
- **Preferred Extended**: Extended molto usate, senza costo di caricamento in Economic;
- **Extended**: centinaia di migliaia di codici LCSC, 3,07 $ ciascuno;
- tutto si cerca con il codice LCSC (Cxxxx) che va nella distinta.

**Altri produttori**:

| Produttore | Montaggio | Prezzo | Tempo | Fonte | Stato |
|---|---|---|---|---|---|
| PCBWay | SMD e THT, componenti forniti da loro o dal cliente | preventivo fatto da una persona in 1–2 giorni lavorativi, niente listino. Un esempio del 2026: 36 $ di montaggio per 10 schede, 186 $ di componenti | dopo il preventivo, 3–7 giorni | [esempio del 2026](https://strifestreams.com/articles/2026/hdd-synth-prototype-to-product/); [descrizione del servizio](https://skills.sh/aklofas/kicad-happy/pcbway) | S |
| Aisler | "Amazing Assembly", prototipi | dal configuratore, nessun listino pubblico | 6 giorni lavorativi | [aisler.net](https://aisler.net/en) | V tempo; C prezzo |
| Eurocircuits | SMD, THT o misti, una o due facce, 1–5 pezzi; componenti comprati da loro | dal calcolatore | 6 giorni lavorativi (3 + 3) | [PCB Proto](https://www.eurocircuits.com/pcb-assembly-proto/) | V tempo; C prezzo |
| OSH Park | solo schede nude | — | — | [OSH Park](https://docs.oshpark.com/services/) | V |

### 2.2 Stima per la basetta dell'ESP32 (montaggio misto)

Ipotesi [S], da rivedere col disegno: i moduli restano moduli e si saldano a mano (ESP32 su due strip femmina, regolatore Pololu D24V22F5, eventualmente il traslatore KAmod). Le parti sciolte della basetta (`guida/schemi/schemi.md:44–59`: R1, R2, R4, R5, R7, CS1, CS2, D1, PTC1, U3) diventano SMD sul lato componenti.

| Voce | JLCPCB Economic, 5 schede montate | Stato |
|---|---|---|
| 5 schede nude 2 strati | 2–5 $ | S |
| Messa in macchina + stencil + conferma | 8,18 + 1,53 + 0,45 = 10,16 $ | V (voci), S (somma) |
| Giunti SMD (circa 30 a scheda × 5) | 0,24 $ | S |
| Caricamento Extended (stima: 2 codici non Basic, per esempio il buffer in SOIC e il PTC in 1206) | 6,14 $ | S, C se sono Basic o Preferred |
| Componenti (10 codici, quantità minime LCSC) | 2–5 $ | S |
| **Totale prima della spedizione** | **circa 21–27 $ (18–23 €)** | S |
| Montaggio THT anche delle strip (80 giunti a scheda) | + 3,58 $ + 80 × 5 × 0,0164 = + 10,14 $ | S. Non conviene: le strip si saldano a mano in 10 minuti |

Confronto: le stesse parti sciolte comprate su LCSC o Mouser per montarle a mano costano 2–5 € più la spedizione; il montaggio di JLCPCB **costa circa 10–15 $ in più**, e toglie il rischio di saldare a mano un SOIC e dei passivi piccoli [S].

### 2.3 Montaggio a mano

| Tipo di componente | Con un saldatore a punta fine e flussante | Note | Stato |
|---|---|---|---|
| THT (strip, testate, morsetti, moduli, DIP) | facile: è quello che l'utente fa già sulle millefori | i fori metallizzati della PCB riempiono meglio delle millefori | S |
| SMD 1206 e 0805 | facile dopo qualche prova | pinzette, flussante, stagno da 0,5 mm; un pad prima, poi l'altro | S |
| SOIC (passo 1,27) | fattibile | trascinamento col flussante, poi treccia per i ponti | S |
| 0603, SOT-23 | fattibile con lente | | S |
| 0402, QFN, passi 0,5 | sconsigliato senza aria calda e microscopio | lasciarlo al produttore, o non usarlo | S |

### 2.4 Cosa conviene per questo progetto [S]

1. **Tutto a mano, con parti THT o SMD ≥ 0805**, per la prima serie. La PCB toglie già i 37 fili e i 44 incroci della basetta (`guida/schemi/schemi.md:102`), cioè il lavoro lungo e il rischio vero. Costo: solo le schede nude.
2. **Montaggio JLCPCB Economic solo per le parti SMD** se il disegno porta parti piccole (un SOIC, un traslatore a MOSFET, i passivi): 10–15 $ in più per 5 schede, con parti **Basic o Preferred Extended** scelte prima di disegnare.
3. **Mai il montaggio THT del produttore** per strip e testate: costa più del tempo che fa risparmiare e porta la scheda in Standard o nel montaggio a mano a pagamento.
4. Meno componenti (preferenza dell'utente): il modulo traslatore U4 può restare un modulo (meno pezzi da saldare) oppure diventare un MOSFET BSS138 e due resistenze per canale sulla scheda (più pezzi, ma un modulo in meno da comprare). È una scelta del disegno: qui si nota solo che non cambia il costo di produzione in modo apprezzabile.

## 3. Regole di progetto

### 3.1 Capacità dei produttori (2 strati, rame da 1 oz)

| Produttore | Pista / spazio minimi | Foro minimo | Corona minima (foro metallizzato) | Rame esterno | Fonte | Stato |
|---|---|---|---|---|---|---|
| JLCPCB | 0,10 / 0,10 mm (1 oz); 0,16 / 0,16 (2 oz). 4 strati: 0,09 / 0,09 | via 0,15 mm (0,20 consigliato); 0,1 a pagamento | 0,18 mm minimo, **0,25 consigliato** (2 oz: 0,254) | 1, 2, 2,5, 3,5, 4,5 oz su 2 strati; 1 o 2 oz su 4 strati | [capacità JLCPCB](https://jlcpcb.com/capabilities/pcb-capabilities) | V |
| PCBWay | 0,10 / 0,10 mm (servizio standard); 5/6 mil con 1 oz e 7/8 mil con 2 oz (servizio avanzato) | 0,15 mm (sotto 0,2 a pagamento) | 0,15 mm sui via | 1–8 oz | [capacità PCBWay](https://www.pcbway.com/capabilities.html) | V |
| Aisler | n.d. sulle pagine lette | n.d. | n.d. | 35 o 70 µm (Beautiful Boards+) | [annuncio del 17 novembre 2025](https://community.aisler.net/t/announcing-beautiful-boards-bringing-more-accessible-choices-for-pcbs-made-in-europe/5437) | V rame; C regole |
| Eurocircuits (PCB Proto) | 0,15 / 0,15 mm | 0,25 mm metallizzato, 0,35 non metallizzato | piazzola = foro + 0,35 mm | 18 µm di base esterni, 35 interni | [PCB Proto](https://www.eurocircuits.com/pcb-assembly-proto/) | V |
| OSH Park | 6 / 6 mil (0,152 mm); 4 strati 5 / 5 mil | 10 mil (0,254 mm) | 5 mil (0,127 mm) | 1 oz (2 oz nel servizio da 0,8 mm) | [OSH Park](https://docs.oshpark.com/services/) | V |

Il 2 oz costa di più da tutti e allarga le piste minime (JLCPCB: da 0,10 a 0,16 mm) [V, [rame di JLCPCB](https://jlcpcb.com/help/article/jlcpcb-copper-weight)]; il sovrapprezzo per 5 pezzi non è pubblicato [C].

### 3.2 Larghezza delle piste per la corrente

Formula IPC-2221 per gli strati esterni: A = (I / (0,048 · ΔT^0,44))^(1/0,725), con A in mil², poi larghezza = A / (spessore in oz × 1,378 mil) ([formula e limiti](https://www.lcsc.com/tools/conversion-calculator-pcb-trace-width); la stessa calcolatrice è in KiCad, "PCB Calculator", installato con KiCad). L'IPC-2221 è prudente: non conta il calore che portano via i riempimenti di rame vicini; l'IPC-2152 è la norma più recente [V].

Calcolo fatto qui (strato esterno) [S, aritmetica della formula]:

| Corrente | 1 oz, +10 °C | 1 oz, +20 °C | 2 oz, +10 °C | 2 oz, +20 °C |
|---|---|---|---|---|
| 1 A | 0,30 mm | 0,20 mm | 0,15 mm | 0,10 mm |
| 2 A | 0,78 mm | 0,51 mm | 0,39 mm | 0,26 mm |
| 3 A | 1,37 mm | 0,90 mm | 0,68 mm | 0,45 mm |
| 5 A | 2,77 mm | 1,82 mm | 1,38 mm | 0,91 mm |

Per le nostre schede [S]:
- il ramo più carico è il 5 V del D24V22F5 (2,5 A massimi del regolatore, F2 da 2 A a monte sul 7,4 V): con **1 oz e piste da 1,5 mm** sul 5 V e un **riempimento di massa** su tutta la faccia inferiore si sta sotto +10 °C anche a 3 A;
- il 2 oz **non serve**: le correnti dei servo non passano sulle schede (capitolo 0);
- i segnali (I2C, seriale, dato dei LED, partitori) a 0,25 mm.

### 3.3 Regole proposte, valide da qualunque produttore [S]

Scelte larghe apposta, così lo stesso file si manda a JLCPCB, Aisler o Eurocircuits senza ritocchi e il DRC trova i margini veri:

| Voce | Valore proposto | Perché |
|---|---|---|
| Pista / spazio minimi | 0,20 / 0,20 mm | il doppio del minimo di JLCPCB e PCBWay, sopra lo 0,15 di Eurocircuits |
| Pista di segnale | 0,25 mm | |
| Pista di potenza (5 V del regolatore, 5 V dei LED, masse) | 1,0–1,5 mm, oppure riempimento | tabella 3.2 |
| Via | foro 0,3 mm, diametro 0,6 mm | corona 0,15 mm per lato, sopra tutti i minimi; foro sopra lo 0,25 di Eurocircuits e OSH Park |
| Fori dei componenti THT | diametro del reoforo + 0,2–0,3 mm; strip e testate a passo 2,54: foro 1,0 mm, piazzola 1,7 mm | regola delle impronte di libreria di KiCad |
| Fori delle viti M2 / M3 | 2,2 / 3,2 mm, non metallizzati, con un anello senza rame di 1 mm attorno alla testa | la vite non tocca le piste |
| Distanza rame–bordo | 0,5 mm | sopra lo 0,25–0,4 di Eurocircuits |
| Spessore | 1,6 mm | standard e gratis da tutti; la basetta oggi è una millefori da circa 1,6 (C) |
| Finitura | HASL senza piombo, ENIG solo se serve un SMD fine | ENIG costa di più (Aisler: 0,097 contro 0,067 €/cm²) |

## 4. Flusso di lavoro

### 4.1 KiCad

| Dato | Valore | Fonte | Stato |
|---|---|---|---|
| Versione corrente | **KiCad 10.0.7** (7 ottobre 2026); la serie 10 è uscita il 20 marzo 2026 | [10.0.7](https://www.kicad.org/blog/2026/10/KiCad-10.0.7-Release/); [10.0.0](https://www.kicad.org/blog/2026/03/Version-10.0.0-Released/) | V |
| Versione sul Mac dell'utente | **9.0.6** (`/Applications/KiCad/KiCad.app`) | letta oggi dal pacchetto | V |
| Novità della 10 utili qui | librerie ufficiali con i soli modelli STEP (più precisi, 386 modelli nuovi); editor grafico delle regole del DRC, con correzioni suggerite; integrazione con git nel gestore del progetto (nuova, con difetti segnalati nella 10.0.2) | [10.0.0](https://www.kicad.org/blog/2026/03/Version-10.0.0-Released/); [forum KiCad](https://forum.kicad.info/t/git-integration-in-10-0-2-cannot-commit/69118) | V |
| Riga di comando | `kicad-cli sch erc`, `kicad-cli pcb drc --exit-code-violations` (esce con 5 se ci sono violazioni), `pcb export gerbers`, `pcb export drill`, `pcb export pos`, `pcb export step`, `jobset run` | [kicad-cli 10.0](https://docs.kicad.org/10.0/en/cli/cli.html) | V |

Proposta [S]: passare alla 10.0.x prima di iniziare il disegno (gratuito, nessun acquisto); un progetto aperto con la 10 non si riapre più con la 9.

### 4.2 Librerie

- **Librerie ufficiali di KiCad**: resistenze, condensatori, diodi, strip e testate a passo 2,54 (`Connector_PinSocket_2.54mm`, `Connector_PinHeader_2.54mm`, `Connector_IDC`), DIP e SOIC, con modelli STEP [V per l'esistenza delle famiglie; C per i nomi esatti della 10].
- **Impronte da fare a mano** (una per modulo, in una libreria del progetto):
  - ESP32-S3-CAM UICPAL: due file da 20 a 25,4 mm di interasse, ma **la quota è ancora da confermare** (`guida/schemi/schemi.md:44`, S-02);
  - Pololu D24V22F5 e D42V110F6: c'è il modello STEP in `cad/modelli/pololu-d24v22fx/d24v22fx.step` e `cad/modelli/pololu-d42v110fx/` (fuori da git, riscaricabili: `.gitignore`); le quote dei pin dalla pagina Pololu;
  - traslatore KAmod (sigle e passo fra le file da confermare: S-04), testata 2 × 8 della scheda del carapace (S-26);
  - le quote già in `cad/script/rif_componenti.py` sono la fonte da usare, così il CAD e la PCB partono dagli stessi numeri.
- **Codici LCSC** nel campo "LCSC Part #" di ogni simbolo, solo se si usa il montaggio di JLCPCB ([guida JLCPCB per KiCad](https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad), verificata da JLCPCB su KiCad 10.0.3, aggiornata il 9 settembre 2026) [V].

### 4.3 Esportazione verso JLCPCB

| Strumento | Cosa fa | Stato con KiCad 10 | Fonte | Stato |
|---|---|---|---|---|
| **Fabrication Toolkit** (bennymeg), dal gestore dei plugin (PCM) | un clic: zip dei Gerber e dei fori, `bom.csv` e `positions.csv` nel formato di JLCPCB, con la correzione delle rotazioni | consigliato da JLCPCB nella guida per la 10.0.3; un utente segnala che la v5.2.0 ignora le **varianti** della 10 (non ci servono) | [guida JLCPCB](https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad); [forum](https://forum.kicad.info/t/jlcpcb-fabrication-toolkit-and-design-variants-issue/67972); [GitHub](https://github.com/bennymeg/JLC-Plugin-for-KiCad) | V |
| **kicad-jlcpcb-tools** (Bouni) | cerca i codici LCSC dentro KiCad, segna Basic ed Extended, esporta | nessuna dichiarazione sulla 10 trovata; ultimo aggiornamento del repository il 23 aprile 2026 | [gittrend](https://gittrend.io/repo/Bouni/kicad-jlcpcb-tools) | C |
| **Esportazione di KiCad senza plugin** | File → Fabbricazione → Gerber, fori, posizioni; distinta dalla tabella dei campi | sempre disponibile | guida JLCPCB sopra | V |

Per Aisler non serve un esportatore: accetta i file nativi di KiCad 10 trascinati nel sito, oppure il plugin "AISLER Push for KiCad" dal PCM ([annuncio Aisler sulla 10](https://community.aisler.net/t/kicad-10-is-live-and-100-supported-by-aisler/5567)) [V]. Un utente segnala che il caricamento nativo si blocca se un'impronta contiene un'immagine; i Gerber passano sempre ([forum Aisler](https://community.aisler.net/t/kicad-8-0-4-failing-to-import-on-aisler/4456)) [V]. Eurocircuits e OSH Park prendono i Gerber; il caricamento diretto del `.kicad_pcb` su OSH Park non è verificato [C].

### 4.4 Il progetto in git

Proposta [S] per questa repo:
- cartella `pcb/` con un progetto KiCad per scheda (`pcb/basetta/`, `pcb/carapace/`, `pcb/partitori/`) oppure un progetto unico con tre schede, da decidere col disegno;
- si versionano `.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, `.kicad_sym`, `.pretty/`, `fp-lib-table`, `sym-lib-table`, `.kicad_dru` (regole del DRC) e `.kicad_jobset`: sono testo, i diff si leggono;
- **fuori da git** (in `.gitignore`): `*-backups/`, `.history/` (la 10 ci tiene i salvataggi incrementali: [forum KiCad](https://forum.kicad.info/t/git-integration-in-10-0-2-cannot-commit/69118)), `*.kicad_prl` (stato dell'interfaccia), `fp-info-cache`, `*.lck`, e le uscite di produzione, che si rigenerano;
- i Gerber dell'ordine **effettivamente inviato** si salvano con un tag git (per esempio `pcb-basetta-r1`), così si sa sempre cosa è stato fabbricato;
- nella CI esistente (`.github/workflows/ci.yml`) si può aggiungere un passo con `kicad-cli sch erc --exit-code-violations` e `kicad-cli pcb drc --exit-code-violations`: la CI resta verde solo se ERC e DRC sono puliti. Serve l'immagine Docker di KiCad o il pacchetto nel runner [C: tempo di esecuzione].
- git di sistema da riga di comando, come per il resto della repo; l'integrazione git di KiCad 10 è nuova e non serve [S].

### 4.5 Modello 3D (STEP) per Fusion

- KiCad: File → Esporta → STEP, oppure `kicad-cli pcb export step --subst-models -o basetta.step basetta.kicad_pcb` ([kicad-cli](https://docs.kicad.org/10.0/en/cli/cli.html)) [V].
- Opzioni utili: `--board-only` per la sola scheda (verifiche di ingombro leggere), `--no-dnp` per togliere i componenti non montati, `--include-tracks` solo per i render (lento), `--user-origin` per esportare con l'origine che si sceglie [V].
- **Origine comune**: si mette l'origine ausiliaria della PCB nello stesso punto del sistema di riferimento del CAD (per la basetta, x 22 e y 0 della quota `x 22…78, |y| ≤ 17,5`, `guida/schemi/schemi.md:25`): lo STEP entra in Fusion già al suo posto, senza spostarlo a mano [S].
- **Nell'altro verso** (dal CAD alla PCB): il contorno e i fori delle colonnine si esportano da uno schizzo di Fusion in DXF e si importano su `Edge.Cuts` di KiCad; così la scheda nasce dalle quote del corpo [S]. Le quote stanno già in `guida/dati/fori.json` e `cad/script/rif_componenti.py`, quindi si può anche generare il contorno da script.
- In Fusion lo STEP diventa un componente della libreria come i `Rif_*` (D-046), e si prova con le verifiche di interferenza come ogni altra parte. I modelli dei moduli (ESP32, Pololu) dentro lo STEP della PCB vanno controllati contro quelli già in libreria, per non averli due volte [S].

## 5. Rischi per chi fa la prima PCB, e come ridurli

| Rischio | Esempio in questo progetto | Come si riduce | Stato |
|---|---|---|---|
| **Impronta sbagliata** (passo, interasse, ordine dei pin) | interasse delle file dell'ESP32, 25,4 o 24,7 (S-02); ordine dei pin del D24V22F5 (S-03); passo del KAmod (S-04); chiave della testata 2 × 8 (S-26) | impronte disegnate dalle quote misurate sul pezzo vero, non dalle foto; **stampa 1:1** del lato rame su carta, con i moduli veri appoggiati sopra; meglio ancora una **dima stampata in 3D** (placca da 1,6 mm con i fori) su cui infilare i moduli prima di ordinare | S |
| **Specchiatura** | la basetta oggi appoggia sulle colonnine con il lato saldature in basso, la scheda del carapace con il lato saldature verso il dorso (`guida/schemi/schemi.md:31`, `:249`) | decidere prima quale faccia guarda dove e scriverlo sulla serigrafia ("LATO COMPONENTI"); controllo nel 3D di KiCad e poi nello STEP in Fusion | S |
| **Pin del simbolo diversi da quelli dell'impronta** | SOT-23 dei MOSFET, diodi (catodo), PTC, elettrolitico CE1 | usare simboli e impronte della libreria ufficiale in coppia; ERC a zero errori; serigrafia con polarità e pin 1 | S |
| **Regole del produttore non rispettate** | fori troppo piccoli, rame troppo vicino al bordo | impostare le regole del capitolo 3.3 **prima** di disegnare (file `.kicad_dru`); DRC a zero errori e con il controllo di parità con lo schema; nella CI, `kicad-cli pcb drc --exit-code-violations` | V comando; S metodo |
| **Gerber diversi da quello che si vede in KiCad** | strati mancanti, contorno aperto, fori su un file a parte dimenticato | aprire lo zip in GerbView (installato con KiCad) e nell'anteprima del produttore prima di pagare; Aisler mostra un'anteprima 3D | S |
| **Ingombri e collisioni nel corpo** | 3,3 mm sotto la basetta (`guida/schemi/schemi.md:102`), colonnine Ø 5,8, spina della testata sopra l'ESP32 (S-01) | STEP della PCB in Fusion con l'origine comune (4.5) e verifica di interferenza, come per ogni parte | S |
| **Impossibile misurare o correggere** | sulle millefori si misura su ogni foro; sulla PCB le piste sono sotto il solder mask | **punti di prova**: una piazzola nuda (o un foro da 1 mm per un puntale) su 5V_REG, 5V_ESP, 5V_LED, 3V3S, GND, SDA, SCL, TX3, RX3, LED_IN e sui nodi dei partitori; un anello di massa per la pinza del puntale. Le prove della guida (`guida/schemi/schemi.md`, 1.5, 2.6, 6.5) si rifanno sui punti di prova | S |
| **Errore scoperto dopo la fabbricazione** | una rete sbagliata o un pin invertito | piazzole di **ponticelli a saldare** (solder jumper) sulle scelte ancora aperte, come J1 (3V3 dell'ESP32 → 3V3S, che sparisce con X3: `guida/schemi/schemi.md:57`); componenti SMD ≥ 0805 per poter tagliare una pista e mettere un filo; fori in più per le predisposizioni | S |
| **Prima serie inutilizzabile** | tutto il lotto da rifare | **prima serie minima**: 5 schede nude (minimo di JLCPCB) o 3 (Aisler, OSH Park); si monta **una** scheda per gradi: prima solo l'alimentazione e si misura, poi i moduli. La seconda serie dopo la prova sul robot | S |
| **Costi di dogana più alti delle schede** | tre disegni da un produttore extra UE, ciascuno una voce da 3 € | tre schede in **un solo pannello** con ponticelli da staccare (mouse bites), oppure un produttore UE; controllare alla cassa (capitolo 1.2) | S |
| **Revisioni confuse** | due serie con differenze piccole | nome, revisione e data sulla serigrafia (per esempio "HEX2 BASETTA r1 2026-11"); tag git sui Gerber ordinati | S |

## 6. Cosa conviene, in ordine [S]

### 6.1 Stima per la prima serie delle tre schede

Aree: basetta 56 × 35 = 19,6 cm²; scheda del carapace allungata, ipotesi 20 × 40 = 8 cm² (C, la misura viene dalla 2.1.7); partitori 23 × 10 = 2,3 cm².

| Strada | Calcolo | Totale consegnato | Stato |
|---|---|---|---|
| **JLCPCB, tre disegni separati, 5 pezzi l'uno, linea economica** | 3 × 2 $ + spedizione 3–6 $ = 9–12 $; IVA 22 % alla cassa → 11–15 $ (9–13 €); dazio 3 € × 3 voci = 9 €; dal 1° dicembre 2026 più 2 € | **circa 20–24 €**, 2–3 settimane | S; C voci doganali |
| **JLCPCB, un pannello con le tre schede** | 2–10 $ secondo il sovrapprezzo per i disegni diversi; una voce doganale | **circa 8–18 €** | S; C sovrapprezzo |
| **Aisler, tre progetti, 6 pezzi l'uno** | (12 + 19,6 × 0,067 × 6) + (12 + 8 × 0,067 × 6) + (12 + 2,3 × 0,067 × 6) = 48,02 €; IVA 22 % → 58,58 € | **circa 59 €**, spedizione gratuita, 1–3 settimane, niente dogana | S su listino del 2023 |
| **Aisler, un pannello di circa 30 cm², 6 pezzi** | 12 + 30 × 0,067 × 6 = 24,06 €; con IVA 29,35 € | **circa 30 €** | S |
| **JLCPCB con il montaggio Economic degli SMD della basetta** | prima riga + circa 15–20 $ (capitolo 2.2) | **circa 35–45 €** | S |

### 6.2 Proposta

1. **Due strati, 1,6 mm, rame da 1 oz, HASL**: basta per tutte e tre le schede (capitoli 0 e 3.2).
2. **Parti THT o SMD ≥ 0805 montate a mano**, moduli su strip come oggi. Il montaggio del produttore solo se il disegno porta un SOIC o parti piccole, e solo con parti Basic o Preferred Extended.
3. **Produttore**: JLCPCB per il prezzo e la velocità, con un solo ordine (meglio un pannello) per tenere basso il dazio; **Aisler** se si vuole evitare la dogana o se le regole doganali cambiano ancora (contributo italiano dal 1° dicembre 2026, tassa di gestione UE annunciata). La differenza è di 10–40 € sulla prima serie.
4. **KiCad 10.0.x**, progetto in `pcb/` nella repo, ERC e DRC nella CI, STEP in Fusion con l'origine del CAD.
5. **Prima della fabbricazione**: dima stampata in 3D con i moduli veri, Gerber controllati in GerbView, STEP provato in Fusion.

### 6.3 Aperti

- Prezzi veri dal preventivo di JLCPCB e Aisler con i file finali (C): i calcolatori non si leggono senza caricare un progetto.
- Quante voci doganali conta un ordine JLCPCB di tre disegni (C).
- Listino Aisler di oggi: la pagina pubblica è del 2023 e ne esistono due versioni (C).
- Misura della scheda del carapace dopo la 2.1.7 (S-01).
- Quote dei moduli da misurare sul pezzo prima di disegnare le impronte: S-02, S-03, S-04, S-26 (`guida/problemi/schemi.yaml`).
- Aggiornare KiCad dalla 9.0.6 alla 10.0.x: da chiedere all'utente.
