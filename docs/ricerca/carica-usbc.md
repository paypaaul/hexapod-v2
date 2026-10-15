# Carica dal robot: USB-C, porta di carica o fessure allargate

Ricerca del 15 ottobre 2026 sulla domanda dell'utente: "si può integrare già un circuito che permette di caricare il robot direttamente tramite USB-C?". Nasce da P-001 (`guida/problemi.md`, bloccante): le spine del pacco non passano dalle fessure del tetto, quindi il pacco non si sfila per caricarlo.

Stato dei dati: **V** verificato su fonte primaria, **S** stimato, **C** da confermare. Le voci nuove vanno approvate dall'utente: il BOM non è stato modificato.

## 1. Punto di partenza

| Dato | Valore | Fonte | Stato |
|---|---|---|---|
| Batteria | OVONIC 2S 5200 mAh 50C hardcase, T-plug, 12 AWG, bilanciamento JST-XH 3 poli; 137–139 × 46–47 × 24–25 mm; 245–259 g | BOM A5, D-045 | V |
| Energia del pacco | 7,4 V × 5,2 Ah = 38,5 Wh; da vuoto (3,5 V/cella, 7,0 V) a pieno (8,4 V) servono circa 36 Wh nel pacco | calcolo | S |
| Catena di potenza | pacco ─12 AWG─ T-plug ─14 AWG─ F1 30 A ─ Wago + ─ due D42V110F6 (servo) e F2 2 A ─ 2813 ─ D24V22F5 (logica) | `docs/cablaggio.md`, sezione 2 | V (progetto) |
| Bilanciamento oggi | JST-XH del pacco ─ prolunga C7 ─ cicalino BX100, si stacca a fine uso | `docs/cablaggio.md`, riga "Bilanciamento" | V (progetto) |
| Vano di coda | T-plug x −80…−64, F1 x −83…−61, cicalino x −87…−62 z 17…28, ToF posteriore e altoparlante sulle guance a x −100…−88 | `docs/cablaggio.md`, sezione 1 | V (modello) |
| Cavi del pacco | escono dal tunnel e salgono al T-plug dalle due fessure del tetto 13 × 4,5 mm accanto a F1 (\|y\| 20,5…25), chiuse verso la coda da un ponte di 2 mm | D-051, P-001 | V (modello) |
| Sportello | si sfila lungo X, due viti M3 × 8 in basso, linguetta sotto il tetto; T-plug e F1 raggiungibili dal retro senza toglierlo | D-054 | V (modello) |
| Logica accesa | 5 V: circa 0,3–0,6 A tipici (ESP32 con Wi-Fi e camera ~250 mA, LED spenti 40–60 mA, sensori), cioè 2–3 W, circa 0,35 A dal pacco | `docs/piano-elettronica-software.md`, 3.2 | S |
| Servo | rail spenti di default (EN dei D42V110F6, D-019) | D-045 | V (progetto) |

**Oggi come si carica**: la guida (D-054) prevede di sfilare il pacco e caricarlo fuori con un caricatore LiPo. P-001 mostra che non si può: la spina T-plug (circa 30 × 16 × 8,5 la coppia) e la JST-XH (circa 10 × 5,8) non passano da una fessura alta 4,5 mm. Il caricatore usato con la v1 non è noto (domanda Q-17).

## 2. Sicurezza: cosa dicono i produttori

Le regole sono le stesse per tutte e tre le opzioni, ma pesano in modo diverso su ciascuna.

- **Mai caricare il pacco dentro il modello.** ElectriFly / Great Planes, manuale delle LiPo: "NEVER charge a LiPo battery while it's inside the model", "ALWAYS charge a LiPo battery in a fireproof location", "NEVER LEAVE A LIPO BATTERY UNATTENDED AT ANY TIME WHILE BEING CHARGED!" ([manuale GPMP0760-0871](https://www.manualsdir.com/manuals/678115/great-planes-lithium-polymer-batteries-gpmp0760-0871.html)). Lo stesso dicono il manuale Flyzone FLZA6401 e il manuale del DHK 8331 (un pacco caldo può incendiare "wood, foam, plastic"). V
- **Sempre in bilanciamento** e con la spina di bilanciamento collegata al caricatore; corrente non oltre quella indicata sul pacco. V (stessa fonte)
- **Corrente di carica della OVONIC**: le pagine dei rivenditori per i pacchi OVONIC 2S indicano da 0,5 a 1C se il manuale non dice altro ([rcdrone.top, OVONIC 2S 1800](https://rcdrone.top/products/ovonic-2s-7-4v-1800mah-90c-rc-car-lipo-battery)); per la 5200 nessuna fonte dà un valore. Si assume **1C = 5,2 A al massimo, 0,5C = 2,6 A consigliati**. C (da leggere sull'etichetta del pacco)
- **Mai lasciare la carica senza sorveglianza**: OVONIC lo scrive sulle istruzioni dei suoi caricatori Mate2 e D15, e dà un sacchetto LiPo con il caricatore ([rcdrone.top, Mate2](https://rcdrone.top/products/ovonic-mate2-balance-charger)). S (pagina di un rivenditore)
- **Pacco caldo**: lasciarlo raffreddare dopo l'uso prima di caricarlo; pacco gonfio, ammaccato o caldo non si carica.

**Cosa vuol dire per questo robot**
- Il pacco sta in un tunnel chiuso di PETG-CF (base, chiglia, sportello), sotto la SSC-32 e i regolatori. Il PETG non è autoestinguente: un incendio del pacco (38,5 Wh) brucia il corpo e quello che c'è sopra, e il tunnel non lo contiene. Caricare dentro il robot va contro l'indicazione esplicita dei produttori di modelli.
- Il rischio non dipende dal caricatore ma dal pacco: un caricatore integrato non lo rende più sicuro. Lo rende solo più comodo, e quindi più facile da lasciare acceso da solo, magari di notte, che è proprio quello che i produttori vietano.
- Se si carica comunque nel robot (opzioni 1 e 2), servono regole fisse: robot su una superficie che non brucia (piastrella, teglia), lontano da cose infiammabili, con qualcuno presente, corrente al massimo 1C, pacco a temperatura ambiente, carica interrotta se il pacco è caldo al tatto o gonfio. Il sacchetto LiPo non si può usare con il pacco dentro il robot.
- **Raccomandazione di sicurezza**: il pacco **deve** potersi sfilare (P-001 va risolto comunque), per caricarlo nel sacchetto o per sostituirlo. La carica nel robot è una comodità sorvegliata, non il modo normale.

## 3. Opzione 1: caricatore 2S integrato, alimentato da USB-C

**Sì, di base si può fare.** Esistono integrati e moduli da pochi euro che caricano un 2S da una presa USB-C e bilanciano le celle. Il limite è la potenza: con la sola USB-C a 5 V si arriva a 15 W, cioè 3–4 volte meno di quello che il pacco accetta.

### 3.1 Candidati

| Soluzione | Potenza e corrente di carica | Tempo per 5,2 Ah (da 7,0 a 8,4 V) | Bilanciamento | Protezioni e NTC | Ingombro e prezzo | Stato |
|---|---|---|---|---|---|---|
| **Modulo con Injoinic IP2326** (boost da USB-C, "Type-C 2S 15W 8.4V con bilanciamento") | ingresso 4,5–9,5 V, al massimo 15 W in ingresso e 1,5 A in uscita; corrente impostata con ISET da 0,75 a 1,5 A (molti moduli escono a 1–1,2 A) | 1,5 A: circa 4 h; 1,0–1,2 A: 5–6 h | sì, solo 2S, **passivo, 20–40 mA** (pin BM sul punto centrale delle celle) | sovracorrente, sovratensione, corto, timer di carica (4/12/24 h), spegnimento a 135 °C; **NTC da 100 kΩ (B 4100)** sul chip: ferma sopra circa 45 °C, dimezza la corrente a caldo | circa 30 × 20 × 5 mm; 2–4 € | V chip ([datasheet Injoinic su LCSC](https://datasheet.lcsc.com/lcsc/2304062030_INJOINIC-IP2326_C2832094.pdf), [done.land](https://done.land/components/power/powersupplies/battery/chargers/charge/powermanagementics/ip2326/)); S modulo ([Cirkit Designer](https://docs.cirkitdesigner.com/component/0e62f3af-f612-4872-999f-5491813837a4/type-c-usb-2s-bms-15w-84v-126v-15a-battery-charging-boost-module-with-balanced)); efficienza 92–94 % |
| **TI BQ25887** | boost da USB 3,9–6,2 V, fino a 2 A di carica (circa 17 W), I2C | circa 3 h | sì, integrato, fino a 400 mA | sensore di temperatura del pacco, regolazione termica, timer | solo integrato QFN o scheda di valutazione: serve un circuito stampato fatto apposta | V ([TI BQ25887](https://www.ti.com/product/BQ25887)); S corrente di bilanciamento ([LCSC](https://www.lcsc.com/product-detail/C2761614.html)) |
| **Modulo IP2368 / IP2369** (USB-C PD bidirezionale, buck-boost) | fino a 45–100 W da PD 9–20 V, carica fino a 3 A e oltre | 1,5–2 h | **no** | sovra/sottotensione, corto, temperatura del chip; NTC opzionale (IP2369: 0–45 °C) | moduli pensati per 4S; chip che scaldano molto secondo gli acquirenti | S ([done.land IP2369](https://done.land/components/power/powersupplies/battery/chargers/charge-discharge/ip2369/), [inserzione IP2368](https://www.onbuy.com/ro/p/ip2368-bidirectional-100w-fast-charging-module-buck-boost-type-c-interface-4s-lithium-battery-high-power-charging-board~p252223345/)) |
| **Trigger PD (es. 12 V) + buck CC/CV a 8,4 V** (XL4015 e simili) | quanto il buck, 2–5 A | 1–2,5 h | **no** | nessuna: il buck tiene 8,4 V per sempre, non termina la carica, niente NTC né timer | 2 moduli, 5–8 € | S; **scartato**: non è un caricatore LiPo |

Gli IP2368/2369 e il trigger con il buck non bilanciano: servirebbe un bilanciatore 2S sempre collegato alla presa JST-XH, che consuma anche a robot spento. Sono scartati. Restano l'IP2326 (modulo pronto) e il BQ25887 (scheda da progettare, fuori misura per questo progetto).

### 3.2 IP2326 nel robot: cosa comporta

- **Potenza e alimentatore**: basta un qualsiasi caricatore USB-C da **5 V 3 A (15 W)**; il chip può chiedere 9 V a un caricatore PD o QC, ma non serve un profilo particolare. Il pacco riceve al massimo 1,5 A × 8,4 V = 12,6 W: 0,29C, molto sotto il limite.
- **Tempo**: 4 ore a 1,5 A, 5–6 ore con i moduli tarati a 1 A. Con un caricatore esterno a 0,5–1C: 1–2 ore.
- **Bilanciamento**: 20–40 mA contro i 400 mA di un caricatore LiPo. Tiene in equilibrio celle già equilibrate; una differenza di 50 mAh fra le celle richiede ore. Non c'è un programma "storage" (3,8–3,85 V per cella), che i produttori chiedono per i pacchi fermi.
- **Protezioni**: buone per il prezzo (timer, NTC, sovratensione), ma non c'è la sorveglianza delle singole celle che fa un caricatore LiPo (allarme su una cella oltre 4,2 V o con resistenza interna anomala). Molti moduli dichiarano "protezione: BMS esterno richiesto".
- **NTC**: va incollata sul pacco. Il pacco si sfila dal tunnel, quindi la sonda va su un supporto a molla nel tunnel che tocca la custodia rigida: la custodia isola, la lettura arriva in ritardo. Il sensore non può stare sulle NTC X14: l'ADS7830 ha tutti gli 8 canali occupati (6 FSR, 2 NTC dei regolatori).
- **Calore nel corpo**: a 92–94 % il modulo perde circa 1 W; il pacco a 0,3C scalda poco. Il calore non è il problema: il problema è che il pacco carica chiuso in un corpo di plastica (sezione 2).
- **Collegamento**: l'uscita del modulo va sul lato robot del T-plug, con un fusibile suo da 2–3 A (F1 da 30 A non protegge il modulo); il pin BM va sul punto centrale del bilanciamento, che oggi va al cicalino BX100 con la prolunga C7. Serve uno sdoppiatore JST-XH 3 poli. Per caricare il T-plug deve restare inserito: oggi a fine uso si stacca (sezionamento e consumo a riposo dei regolatori e del BX100).
- **Robot acceso durante la carica**: in pratica no.
  - Camminare chiede circa 70–90 W in media (5,2 Ah in 22–27 minuti, D-045, con l'80 % usabile): nessun caricatore USB-C fino a 100 W lo regge, e l'IP2326 ne dà 12,6.
  - Con la sola logica accesa (circa 0,35 A dal pacco) la carica va avanti più lenta, ma l'IP2326 non ha il percorso di potenza separato: la corrente della logica gli impedisce di vedere la fine della carica (soglia di 300 mA), e il pacco resta a 8,4 V fino al timer. È proprio il mantenimento a tensione piena che rovina le LiPo.
  - Regola: durante la carica 2813 spenta e rail spenti; il firmware può leggere la presenza della USB-C (un partitore su un GPIO, se ne resta uno) solo per impedire l'accensione.
- **Ingombro**: modulo 30 × 20 × 5 più la presa USB-C sulla porta di coda. In coda oggi ci sono T-plug, F1, cicalino, ToF posteriore e altoparlante in pochi millimetri d'aria (`cablaggio.md`, sezioni 1 e 4); il modulo andrebbe sul tetto del tunnel o sulla guancia, con la presa sulla porta di servizio.

**Giudizio**: fattibile e poco costoso (meno di 10 € con fusibile, sdoppiatore e NTC), ma lento (4–6 ore), con un bilanciamento debole, senza programma di conservazione e con il pacco che carica dentro il corpo. Non lo consiglio come modo normale di caricare.

## 4. Opzione 2: porta di carica in coda, caricatore LiPo esterno

**Il robot ce l'ha già quasi tutta.** Le due spine che servono a un caricatore LiPo arrivano già in coda, raggiungibili dal retro senza aprire nulla:
- il **T-plug** sta 7 mm dentro la porta di coda, sopra F1 (`cablaggio.md`, sezione 4; D-051, D-054): si stacca il maschio lato robot e si inserisce al suo posto il cavo del caricatore;
- il **bilanciamento** arriva al cicalino BX100 con la prolunga C7, con lo spinotto verso il retro (BOM, domanda 6): si sfila il cicalino e si inserisce la spina di bilanciamento del caricatore.

Il caricatore resta fuori dal robot, sul tavolo. Si carica senza togliere il pacco e senza elettronica nuova nel corpo.

### 4.1 Caricatore con ingresso USB-C: ToolkitRC M4 Pocket

È il modo di avere "la carica da USB-C" senza mettere il caricatore nel robot: un solo alimentatore USB-C PD alimenta un caricatore LiPo vero, con il suo bilanciamento.

| Dato | Valore | Stato |
|---|---|---|
| Ingresso | USB-C 7,0–20,0 V (PD, QC, AFC, FCP) oppure XT60 7–25 V, 5 A | V ([Pyrodrone](https://pyrodrone.com/collections/chargers-1/products/toolkitrc-m4-pocket-80w-5a-1-4s-compact-balance-charger-w-built-in-usb-c-input-output)) |
| Carica | 1,0–5,0 A, al massimo 80 W; LiPo, LiHV, LiFe 2–4S; programma storage (3,85 V per cella) | V (Pyrodrone; [Oscar Liang](https://oscarliang.com/toolkitrc-m4-pocket)) |
| Bilanciamento | 400 mA, precisione migliore di 5 mV a 4,2 V | V (Pyrodrone) |
| Uscite | XT60 e XT30; spina di bilanciamento sul fianco (tipo JST-XH da confermare) | S |
| Ingombro | 80 × 40 × 30 mm, 75 g; display a colori | V |
| Prezzo | circa 30–40 € (Rotorama 35,49 €, Motion RC 29,99 $, Sigmanortec 61,09 €) | V a ottobre 2026, da ricontrollare |
| Attenzione | parte solo se l'alimentatore dà 9 V o più: un lettore ha trovato alimentatori PD che davano solo 5 V e il caricatore non partiva | S (commento alla recensione di Oscar Liang) |

Alternativa più potente: ISDT 608PD (USB-C 5–28 V, 140 W da USB-C, 1–6S, 72,5 × 60 × 26,6 mm, circa 42–68 €; [Oscar Liang](https://oscarliang.com/isdt-608pd-charger/)). Per un 2S da 5,2 Ah non serve.

### 4.2 Alimentatore necessario

Il pacco riceve al massimo 8,4 V × corrente; il caricatore rende circa il 90 % (S).

| Corrente di carica | Potenza al pacco | Potenza dall'alimentatore | Profilo PD minimo | Tempo da vuoto |
|---|---|---|---|---|
| 0,5C = 2,6 A (consigliata) | 22 W | circa 25 W | 9 V 3 A (27 W) o 15 V 2 A | circa 2 h 15 min |
| 1C = 5,2 A (massimo) | 44 W | circa 49 W | 20 V 3 A (60 W) | circa 1 h 15 min |

**Alimentatore consigliato: USB-C PD da 65 W con il profilo 20 V 3,25 A** (anche 15 V 3 A), con cavo USB-C da 3 A (60 W). Va bene il caricatore di un portatile. Un alimentatore da 30 W con 9 V 3 A carica a 0,5C. Un alimentatore che dà solo 5 V non va.

### 4.3 Cosa comporta

- **Bilanciamento e protezioni**: quelle di un caricatore LiPo (400 mA di bilanciamento, tensione di ogni cella sul display, storage, limite di capacità e di tempo secondo il modello).
- **Calore nel corpo**: nessun componente in più; il caricatore scalda fuori.
- **Robot durante la carica**: spento per forza, perché il T-plug lato robot è staccato. È un vantaggio: nessuna corrente verso la logica durante la carica, la fine della carica è pulita.
- **Sicurezza**: il pacco carica comunque dentro il corpo (sezione 2): solo sorvegliato, su una superficie che non brucia, con il robot spento. Il pacco va sfilato per caricarlo nel sacchetto se si vuole lasciarlo senza guardarlo, o per la conservazione lunga.
- **Comodità**: due spine dal retro, come oggi a fine uso. Il T-plug maschio lato robot resta libero mentre si carica: non ha tensione.
- **Da provare**: che la spina del caricatore (adattatore XT60 → T-plug maschio) entri nei 7 mm della porta di coda come il maschio del robot (stesso connettore, quindi sì; S), e che il cavo esca dalla porta senza tirare il pacco. È la stessa prova a mano del T-plug già prevista sul primo carapace (`cablaggio.md`, sezione 4).

**Giudizio**: la soluzione migliore per la carica di tutti i giorni. Costa zero se il caricatore della v1 va bene (domanda Q-17); altrimenti un caricatore da 30–40 € e un alimentatore che probabilmente l'utente ha già.

## 5. Opzione 3: fessure del tetto aperte verso la coda

È la soluzione di P-001: si toglie il ponte da 2 mm che chiude verso la coda le due fessure 13 × 4,5 mm (|y| 20,5…25) accanto a F1. Le fessure diventano due tacche aperte: quando il pacco si sfila, i cavi scorrono fuori dall'estremità aperta e le spine non devono più passare dal foro.

- **Cosa permette**: sfilare il pacco con T-plug e JST-XH attaccati, per caricarlo fuori nel sacchetto, conservarlo a 3,85 V per cella o sostituirlo. È quello che chiedono i produttori.
- **Da verificare nel CAD**: la fascetta di F1 (D-055) passa proprio in queste due fessure, a x ≈ −76, e abbraccia la striscia di tetto fra le due. Tolto il ponte, quella striscia diventa una lingua a sbalzo aperta verso la coda e la fascetta può scivolarne fuori: serve un dentino o una tacca sulla lingua che la tenga, oppure le fessure si aprono verso i fianchi invece che verso la coda. Poi la rigidezza del tetto senza il ponte (tetto da 2 mm); lo spazio dei cavi da 12 AWG (Ø esterno circa 3,5–4 mm) nella tacca, e lo sportello (D-054) che non li pizzichi.
- **Da provare**: con la spina vera, prima di stampare la base (guida, passo 11.03).
- **Costo**: nessuno.

**Giudizio**: necessaria comunque, con qualsiasi scelta di carica. Senza, il pacco non si toglie dal robot: non si può caricare nel sacchetto, non si può sostituire e un pacco gonfio resta nel corpo.

## 6. Confronto

| | 1. IP2326 integrato (USB-C) | 2. Porta di carica + M4 Pocket (USB-C PD) | 3. Fessure aperte |
|---|---|---|---|
| Corrente di carica | 1,0–1,5 A (0,2–0,3C) | 2,6–5,2 A (0,5–1C) | quella del caricatore, fuori |
| Tempo da vuoto | 4–6 h | 1 h 15 – 2 h 15 | come la 2, più sfilare il pacco |
| Bilanciamento | passivo 20–40 mA | 400 mA, tensione di ogni cella a vista | come la 2 |
| Programma storage | no | sì (3,85 V) | sì |
| NTC | sì, ma sulla custodia del pacco sfilabile | dipende dal caricatore (non dichiarata sull'M4) | — |
| Calore nel corpo | circa 1 W del modulo | nessuno | nessuno |
| Pacco carica nel corpo | sì | sì | no (nel sacchetto) |
| Robot usabile durante la carica | no (camminare chiede 70–90 W; la logica disturba la fine della carica) | no (T-plug staccato) | no (pacco fuori) |
| Alimentatore | USB-C 5 V 3 A (15 W) qualsiasi | USB-C PD 65 W, profilo 20 V 3,25 A (30 W con 9 V 3 A per 0,5C) | quello del caricatore |
| Elettronica nuova nel robot | modulo, fusibile, sdoppiatore JST-XH, NTC, presa USB-C | nessuna | nessuna |
| CAD 2.1.7 | sede del modulo, presa USB-C nella porta di coda, supporto della NTC nel tunnel | nessuno (prova a mano) | tacche aperte e fermo della fascetta di F1 |
| Costo | meno di 10 € | 0 € se va il caricatore della v1; altrimenti circa 35 € + alimentatore | 0 € |
| Contro le indicazioni dei produttori | sì, e invita a caricare senza sorveglianza | sì, ma solo con sorveglianza | no |

## 7. Raccomandazione

1. **Opzione 3 nella 2.1.7, comunque**: le fessure aperte verso la coda (o verso i fianchi) risolvono P-001. Il pacco deve potersi sfilare per caricarlo nel sacchetto, conservarlo e sostituirlo; un pacco gonfio non deve restare chiuso nel corpo.
2. **Opzione 2 per la carica di tutti i giorni**: caricatore LiPo esterno collegato in coda al T-plug e al bilanciamento, senza togliere il pacco, solo sorvegliato, robot spento su una superficie che non brucia, a 0,5C (2,6 A). Se l'utente vuole "caricare da USB-C", lo fa con un caricatore LiPo che ha l'ingresso USB-C PD, come il ToolkitRC M4 Pocket, alimentato da un **USB-C PD da 65 W con il profilo 20 V 3,25 A** (basta uno da 30 W con 9 V 3 A per caricare a 0,5C). Prima di comprare, sapere che caricatore usava l'utente con la v1 (Q-17): se bilancia il 2S e ha il programma storage va bene quello.
3. **Opzione 1 sconsigliata**: si può fare, ma un caricatore da 15 W dentro il corpo dà una carica di 4–6 ore con un bilanciamento debole e senza storage, aggiunge pezzi nella coda già piena, cambia il ruolo del T-plug come sezionamento e invoglia a lasciare il robot in carica da solo. Il robot non è comunque usabile mentre carica. Se l'utente la vuole lo stesso, va come predisposizione X (sezione 8), con le regole della sezione 2.

## 8. Voci nuove da approvare

Il BOM non è stato modificato. Prezzi e link indicativi, letti il 15 ottobre 2026 (V se letti sulla pagina, S se stimati).

**Per l'opzione 2 (consigliata)**, solo quello che l'utente non ha già:

| Voce proposta | Quantità | Cosa | Prezzo e link indicativi | Stato |
|---|---|---|---|---|
| Caricatore LiPo con ingresso USB-C PD | 1 | ToolkitRC M4 Pocket, 80 W, 1–4S, bilanciamento 400 mA, storage | [Rotorama](https://www.rotorama.com/product/toolkitrc-m4-pocket) 35,49 € (33,39 € con la scatola rovinata); [Motion RC](https://motionrc.com/products/toolkitrc-m4-pocket-80w-4-cell-4s-lipo-dc-battery-charger-tk11800) 29,99 $; anche su AliExpress | V (prezzi), C (disponibilità) |
| Alimentatore USB-C PD | 1 | 65 W con profilo 20 V 3,25 A (Anker o UGREEN da 65 W), cavo USB-C 3 A | circa 20–30 € su Amazon.it (offerte da 19,94 a meno di 30 €: [telefonino.net](https://www.telefonino.net/notizie/caricatore-usb-anker-65w-3-uscite-soli-19e-offerta-del-giorno/), [Notebookcheck](https://www.notebookcheck.com/Deal-Ugreen-Nexode-GaN-Charger-mit-65-Watt-zum-Tiefstpreis-dank-35-Rabatt.705296.0.html)); va bene quello di un portatile | S |
| Adattatore XT60 femmina → T-plug maschio | 1 | cavo corto in 14 AWG, dall'uscita del caricatore al T-plug femmina del pacco | 3–5 € da AliExpress o eBay ([eBay.it](https://www.ebay.it/itm/224050585331)); 15 $ la versione con cavo Tornado RC ([OzRC](https://ozrc.com.au/products/tornado-rc-10cm-xt-60-female-to-deans-male-adapter-trc-8043b)) | S |
| Sacchetto LiPo | 1 | per caricare e conservare il pacco sfilato | circa 8–12 € | S; Q-17 chiede se c'è già |

Totale: 0 € se il caricatore della v1 è adatto e c'è un alimentatore; altrimenti circa 60–80 €.

**Per l'opzione 1 (sconsigliata)**, come predisposizione X se l'utente la vuole:

| Voce proposta | Quantità | Cosa | Prezzo e link indicativi | Stato |
|---|---|---|---|---|
| Modulo di carica 2S da USB-C | 1 + 1 | IP2326, 15 W, 8,4 V, bilanciamento 2S (pin BM), ISET a 1,5 A | 2–4 € su AliExpress, per esempio [1005005394606799](https://www.aliexpress.com/item/1005005394606799.html) o [1005008676573097](https://www.aliexpress.com/item/1005008676573097.html): chip, bilanciamento e protezioni da guardare sull'inserzione | S, C |
| NTC 100 kΩ B 4100 | 1 | sonda sul pacco (con la 82 kΩ al posto della 51 kΩ del modulo) | circa 1 € | S |
| Fusibile 3 A con portafusibile in linea | 1 | sull'uscita del modulo | circa 2 € | S |
| Sdoppiatore JST-XH 3 poli | 1 | bilanciamento al cicalino e al pin BM | circa 2 € | S |

## 9. Impatto sul CAD della 2.1.7

- **Opzione 3 (da fare)**, in `cad/script/corpo.py` sul tetto della base:
  - togliere il ponte da 2 mm che chiude le due fessure 13 × 4,5 verso la coda, o aprirle verso i fianchi;
  - un dentino o una tacca sulla lingua centrale perché la fascetta di F1 (D-055, x ≈ −76) non scivoli fuori;
  - verifiche: rigidezza del tetto (sezione chiusa o nervata), costole di F1, linguetta dello sportello (D-054, 0,4 mm dal tetto), cavi da 12 AWG che non vengono pizzicati, corsa di sfilamento del pacco con i cavi (la prova di D-051 era senza cavi);
  - nessun pezzo comprato in più; prova con la spina vera prima di stampare la base.
- **Opzione 2**: nessuna modifica. Resta la prova a mano del T-plug già prevista sul primo carapace, estesa all'adattatore del caricatore e allo spinotto di bilanciamento dietro il cicalino.
- **Opzione 1** (solo se approvata): sede del modulo 30 × 20 × 5 sul tetto del tunnel o su una guancia della coda, con la presa USB-C affacciata alla porta di coda (da controllare con ToF posteriore e altoparlante, a x −100…−88); sede del portafusibile da 3 A; supporto a molla della NTC nel tunnel contro la custodia del pacco; passaggio dei fili BM e NTC. Va anche aggiornato `cablaggio.md` (schema di potenza e tabella dei cavi).
- **Guida**: i passi 11.03, 11.04, 15.04 e 15.05 seguono la scelta; va aggiunto un passo "Carica" con le regole della sezione 2.

## 10. Domande per l'utente

- Che caricatore usavi con la v1? Bilancia il 2S e ha il programma storage? Che ingresso ha (rete, XT60, USB-C)? È la domanda Q-17, e decide se le voci dell'opzione 2 servono.
- Hai un alimentatore USB-C PD da 65 W (anche quello di un portatile)?
- Hai un sacchetto LiPo?
- Vuoi comunque il caricatore integrato (opzione 1), sapendo che è sconsigliato?

## Fonti

- Injoinic IP2326, datasheet: [LCSC](https://datasheet.lcsc.com/lcsc/2304062030_INJOINIC-IP2326_C2832094.pdf); riassunto: [done.land](https://done.land/components/power/powersupplies/battery/chargers/charge/powermanagementics/ip2326/); modulo: [Cirkit Designer](https://docs.cirkitdesigner.com/component/0e62f3af-f612-4872-999f-5491813837a4/type-c-usb-2s-bms-15w-84v-126v-15a-battery-charging-boost-module-with-balanced), [Fritzing forum](https://forum.fritzing.org/t/2s-3s-18w-mini-fast-charging-module/32503)
- TI BQ25887: [ti.com](https://www.ti.com/product/BQ25887), [LCSC](https://www.lcsc.com/product-detail/C2761614.html)
- IP2369 / IP2368: [done.land](https://done.land/components/power/powersupplies/battery/chargers/charge-discharge/ip2369/), [inserzione IP2368](https://www.onbuy.com/ro/p/ip2368-bidirectional-100w-fast-charging-module-buck-boost-type-c-interface-4s-lithium-battery-high-power-charging-board~p252223345/)
- ToolkitRC M4 Pocket: [Pyrodrone](https://pyrodrone.com/collections/chargers-1/products/toolkitrc-m4-pocket-80w-5a-1-4s-compact-balance-charger-w-built-in-usb-c-input-output), [Oscar Liang](https://oscarliang.com/toolkitrc-m4-pocket), [Rotorama](https://www.rotorama.com/product/toolkitrc-m4-pocket); ISDT 608PD: [Oscar Liang](https://oscarliang.com/isdt-608pd-charger/)
- Sicurezza LiPo: [ElectriFly / Great Planes, manuale delle LiPo](https://www.manualsdir.com/manuals/678115/great-planes-lithium-polymer-batteries-gpmp0760-0871.html), [Flyzone FLZA6401](https://www.manualsdir.com/manuals/676146/flyzone-flza6401.html), [DHK 8331](https://www.asiatees.com/files/product/Instruction%20Manual%20DHK-8331%20Short%20Course%20Truck_1594960608.pdf); OVONIC: [pacco 2S 1800](https://rcdrone.top/products/ovonic-2s-7-4v-1800mah-90c-rc-car-lipo-battery), [Mate2](https://rcdrone.top/products/ovonic-mate2-balance-charger), [pacchi 5200](https://rcdrone.top/products/ovonic-2s-5200mah-lipo-battery)
- Repo: D-045, D-051, D-054, D-055; `docs/cablaggio.md` sezioni 1, 2 e 4; `docs/BOM.md` A5, B3, B9, B12, C7; `docs/piano-elettronica-software.md` 3.2; `guida/problemi.md` P-001 e Q-17.
