# Batteria OVONIC 2S 5200 mAh 50C hardcase e cablaggio del robot esapode (18x MG90S + SSC-32)

> Versione 3 (definitiva), 8 ottobre 2026. Il primo tentativo (circa 50 chiamate web) era stato interrotto; la versione 2 ne ha riusato i dati con circa 15 chiamate mirate; questa terza ripresa ha ricontrollato il file contro il registro del primo tentativo, ha riletto direttamente le pagine OVONIC / Ampow e le immagini dell'inserzione Amazon.it, ha riguardato i due disegni quotati Pololu e ha aggiunto 15 chiamate (genere del T-plug e uscita dei cavi dalle immagini del produttore, T-plug Amass AM-1015E, cavo in silicone 14 AWG, mappa dei canali Lynxmotion). I calcoli delle tabelle sono stati rifatti e tornano.
>
> **Etichette di ogni numero**: **[primary]** = pagina / datasheet / manuale del produttore; **[secondary]** = inserzione di negozio, blog, tabella di terzi; **[third_party_measurement]** = misura fatta da terzi; **[community]** = forum / opinione; **[computed]** = calcolo mio (formula indicata).
>
> **Come è stato letto il dato**: **(DIR)** = letto da me direttamente nel testo della pagina, nel testo estratto dal PDF o nell'immagine del disegno; **(WF)** = pagina letta tramite WebFetch, cioè riassunta da un modello piccolo (citazioni attendibili ma non viste da me sulla fonte: ricontrollare prima di usarle in un CAD); **(SNIP)** = solo dal riassunto di un motore di ricerca, affidabilità bassa.
>
> Pagine non raggiungibili (blocco anti-bot o errore 403/404, non aggirato): wiki.lynxmotion.com, tme.eu, community.robotshop.com (verifica anti-bot anche dal browser), studica.com, hackster.io.
> Ambito: l'architettura di alimentazione (regolatori, fusibile, interruttore) e la scheda SSC-32 sono trattate nelle note `alimentazione.md` e `ssc32.md` della stessa cartella; qui se ne riprende solo ciò che serve al cablaggio.

## 1. Batteria OVONIC 2S 5200 mAh 50C hardcase con T-plug: dimensioni, peso, cavi, connettori, correnti, varianti, tolleranza del vano

### Takeaway
Le inserzioni ufficiali NON concordano tra loro: lunghezza 137-139 mm, larghezza 46-47,3 mm, altezza 24-25,4 mm, peso 245-259 g, con tolleranza dichiarata dal produttore fino a ±5 mm in lunghezza, ±2 mm in larghezza e in altezza, ±20 g. Il vano va progettato sull'inviluppo massimo (144 × 49,3 × 27,4 mm) con fermo regolabile, spessori e cinghia, e le quote definitive vanno prese col calibro sul pacco reale. Lunghezza dei cavi e genere del T-plug NON sono dichiarati a testo da OVONIC; dalle immagini del produttore il T-plug sulla batteria è femmina, tutti i cavi escono da un solo lato corto e i cavi di potenza (12 AWG) sono lunghi circa 120 mm (stima mia dalla foto, da misurare).

### Cited Findings

**Inserzione Amazon.it (la più probabile per un acquirente italiano)**
- "OVONIC Batteria Lipo 2s 5200mAh 7.4V 50C con Connettore T stile Dean per RC Auto Barca Camion Buggy Team Associato Hobby", ASIN B098P5ZBJ6, variante "5200mAh-2S-Deans", 19,99 €, "Disponibilità immediata", spedito da Amazon, venditore "OVONIC Direct", produttore dichiarato "Emate", 4,0 stelle su 24 recensioni (letto l'8 ottobre 2026) (DIR) [secondary] — [Amazon.it B098P5ZBJ6](https://www.amazon.it/OVONIC-Batteria-LiPo-5200-Plug/dp/B098P5ZBJ6)
- "Specifiche: dimensioni della batteria Lipo (± 3 mm): 137 x 24 x 46 mm (lunghezza x larghezza x altezza), peso approssimativo (± 5 g): 245 g" (DIR) [secondary] — [Amazon.it B098P5ZBJ6](https://www.amazon.it/OVONIC-Batteria-LiPo-5200-Plug/dp/B098P5ZBJ6). L'inserzione scambia larghezza e altezza: il pacco è lungo 137, largo 46, alto 24.
- Nella tabella "Dettagli prodotto" della stessa pagina: "Peso della batteria 254 Grammi" (DIR) [secondary] — [Amazon.it B098P5ZBJ6](https://www.amazon.it/OVONIC-Batteria-LiPo-5200-Plug/dp/B098P5ZBJ6). È in disaccordo con i 245 g ± 5 g dell'elenco puntato della stessa pagina.
- "Parametri – ... tensione: 7,4 V, cella: 2S, capacità: 5200 mAh, scarica: 50 C, spina di ricarica: JST-XHR-3P, spina di scarica: connettore Dean Style T, imballaggio: custodia rigida"; "Contenuto della confezione: 1 batteria OVONIC 2S, 2 adesivi di marca" (DIR) [secondary] — [Amazon.it B098P5ZBJ6](https://www.amazon.it/OVONIC-Batteria-LiPo-5200-Plug/dp/B098P5ZBJ6)
- La pagina NON indica: sezione dei cavi, lunghezza dei cavi, genere del connettore (ricerca nel testo di "AWG", "cavo", "maschio", "femmina": nessun risultato) (DIR) — [Amazon.it B098P5ZBJ6](https://www.amazon.it/OVONIC-Batteria-LiPo-5200-Plug/dp/B098P5ZBJ6)
- **Immagine quotata del produttore nella galleria dell'inserzione** (seconda immagine; letta da me a schermo, terza ripresa): "137 mm (5.39 inches)", "46 mm (1.81 inches)", "24 mm (0.94 inches)", bilancia con "245 g" e didascalia "Peso (0,24 kg)", riquadri "JST-XHR-3P", "Deans T Plug", "Filo di rame massiccio"; in alto "5200mAh / 2S1P / 7.4V / 50C" (DIR, immagine) [secondary, grafica del produttore su Amazon] — [immagine 71zhTyw3kxL](https://m.media-amazon.com/images/I/71zhTyw3kxL._AC_SL1500_.jpg)
- **Genere del T-plug sulla batteria, dalle immagini del produttore**: il riquadro "Deans T Plug" mostra un corpo rosso con due feritoie (una orizzontale e una verticale) e nessuna lamella sporgente, cioè la metà **femmina**; anche nella foto principale il connettore in fondo ai cavi termina piatto, senza lamelle (DIR, osservazione mia su immagini di prodotto, che sono rendering: da confermare sul pezzo) [secondary] — [immagine 71zhTyw3kxL](https://m.media-amazon.com/images/I/71zhTyw3kxL._AC_SL1500_.jpg), [immagine principale 61J9hFl54LL](https://m.media-amazon.com/images/I/61J9hFl54LL._AC_SL1500_.jpg)
- **Uscita dei cavi, dalle stesse immagini**: cavi di potenza (rosso e nero) e cavetto di bilanciamento escono tutti dallo stesso lato corto; i due cavi di potenza escono in alto, da un intaglio del bordo superiore della testata, il cavetto di bilanciamento più in basso sulla stessa testata (DIR, osservazione mia su rendering) [secondary] — [immagine principale 61J9hFl54LL](https://m.media-amazon.com/images/I/61J9hFl54LL._AC_SL1500_.jpg)
- **Lunghezza dei cavi di potenza stimata dalla foto** [computed, bassa affidabilità: scala = 137 mm / 385 px del corpo batteria nell'immagine quotata = 0,356 mm/px; percorso del cavo dall'uscita al T-plug circa 335 px]: circa 120 mm (campo plausibile 100-140 mm), più il connettore (circa 14 mm nell'immagine). Il cavetto di bilanciamento appare molto più corto (ordine di 40-60 mm fuori dalla custodia, stima a occhio). È un rendering pubblicitario: NON è una quota dichiarata — [immagine 71zhTyw3kxL](https://m.media-amazon.com/images/I/71zhTyw3kxL._AC_SL1500_.jpg)
- Altre immagini della galleria: "Micro resistenza interna: < 10 mΩ", "128 Wh/kg", "Ciclo di vita a 350+ volte"; contenuto della confezione: 1 scatola, 1 batteria, 2 adesivi, 1 manuale utente (DIR, immagini; affermazioni pubblicitarie non verificate) [secondary] — [immagine 71ITp31epsL](https://m.media-amazon.com/images/I/71ITp31epsL._AC_SL1500_.jpg), [immagine 81RTdmxGpzL](https://m.media-amazon.com/images/I/81RTdmxGpzL._AC_SL1500_.jpg)
- Codice modello nelle immagini A+ della stessa inserzione (testo alternativo): "O-50C-5200-2S1P-HC-T2P" (DIR) [secondary] — [Amazon.it B098P5ZBJ6](https://www.amazon.it/OVONIC-Batteria-LiPo-5200-Plug/dp/B098P5ZBJ6)
- Altre inserzioni Amazon.it dello stesso pacco, non lette nel dettaglio: [B08C4MM6HD (2 pezzi)](https://www.amazon.it/OVONIC-5200-connettore-elicottero-confezioni/dp/B08C4MM6HD), [B0BM4FMZR5 (2 pezzi)](https://www.amazon.it/OVONIC-Batteria-5200mAh-spina-Camion/dp/B0BM4FMZR5) [secondary]

**Pagine del produttore / negozio ufficiale (us.ovonicshop.com, ampow.com)**
- us.ovonicshop.com, confezione da 2 con T Plug (riletta direttamente nella terza ripresa): "Length (dev.5mm) 137mm/5.39inch", "Width (dev.2mm) 46mm/1.81inch", "Height (dev.2mm) 24mm/0.94inch"; "Net Weight (dev.20g) 245g/0.54lb for one battery"; "Discharge Rate 50C"; "Max Burst Discharge Rate 100C"; "Discharge Plug T Plug"; "Charge Plug JST-XHR-3P"; "Wire Gauge 12 AWG"; lunghezza dei cavi non indicata; "Availability: Out Of Stock" sul negozio USA (DIR) [primary] — [us.ovonicshop.com, 2 pezzi](https://us.ovonicshop.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-2pcs-lipo-battery)
- ampow.com, pacco singolo (riletta direttamente nella terza ripresa, versione italiana della pagina): "Lunghezza (dev.5mm): 138mm", "Larghezza (dev.2mm): 46mm", "Altezza (dev.2mm): 24mm"; "Peso netto (dev.20g): 259g"; "dimensioni di 138x46x24 mm"; prezzo 25,17 € (barrato 32,91 €; "Final Price €22,65" con codice sconto); "Availability: In Stock"; sezione e lunghezza dei cavi non indicate (DIR). 50C continui e 100C burst, connettore Deans (WF) [primary] — [ampow.com, singolo](https://www.ampow.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-lipo-battery)
- ampow.com, confezione da 2: "Length (dev.5mm): 139mm", "Width (dev.2mm): 46mm", "Height (dev.2mm): 24mm"; 512 g (259 g per pacco, dev. 20 g); "Charge Plug: JST-XH"; 50C / 100C burst; 35,17 €, "In Stock" (WF) [primary] — [ampow.com, 2 pezzi](https://www.ampow.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-2pcs-lipo-battery)
- ampow.com, confezione da 2 con voltage checker: "139mm x 47.3mm x 25.4mm L*W*H (5.48in x 1.86in x 1.00in)", nessuna tolleranza; "253g (0.51lb) per pack"; "Balancer Connector Type: JST-XHR-3P"; "12 AWG"; esaurito (WF) [primary] — [ampow.com, 2 pezzi + checker](https://www.ampow.com/products/2-x-ovonic-2s-50c-5200mah-7-4v-hardcase-lipo-battery-with-dean-t-connector-lipo-voltage-checker-for-1-10-scale-car-truck)
- us.ovonicshop.com, confezione da 4: "Size (with ±5mm variance): 137 x 46 x 24mm"; "Net Weight (dev.20g): 259g per unite"; 50C / 100C burst; "Charge Plug: JST-XHR-3P"; "Discharge Plug: Deans(T) Plug"; genere del connettore non indicato (WF) [primary] — [us.ovonicshop.com, 4 pezzi](https://us.ovonicshop.com/products/4-packs-ovonic-hard-case-lipo-2s-5200mah-50c-7-4v-with-deans-for-1-10-1-8-rc-cars)
- L'indirizzo www.ovonicshop.com/products/ovonic-50c-2s-5200mah-lipo-battery-7-4v-hardcase-with-deans-plug-for-rc-car dà errore 404: la scheda esiste solo sul sottodominio us. e su ampow.com — [tentativo](https://www.ovonicshop.com/products/ovonic-50c-2s-5200mah-lipo-battery-7-4v-hardcase-with-deans-plug-for-rc-car)

**Rivenditore terzo (coerente con ampow)**
- rcdrone.top: 2S1P, 7,4 V, 5200 mAh, "Energy 38.48Wh", 50C, burst 100C, Deans, bilanciatore "JST-XHR", "259g (dev.20g)", "138 x 46 x 24 mm (dev.5mm / dev.2mm / dev.2mm)" (WF) [secondary] — [rcdrone.top](https://rcdrone.top/products/ovonic-2s-5200mah-battery)

**Riepilogo delle discrepanze (stesso prodotto nominale: 2S 5200 mAh 50C hardcase, T-plug)**

| Fonte | L (mm) | W (mm) | H (mm) | Peso (g) | Tolleranza dichiarata |
|---|---|---|---|---|---|
| Amazon.it B098P5ZBJ6, elenco puntato [secondary] (DIR) | 137 | 46 | 24 | 245 | ±3 mm, ±5 g |
| Amazon.it B098P5ZBJ6, tabella dettagli [secondary] (DIR) | – | – | – | 254 | – |
| Amazon.it B098P5ZBJ6, immagine quotata [secondary] (DIR) | 137 | 46 | 24 | 245 | – |
| us.ovonicshop, 2 pezzi [primary] (DIR) | 137 | 46 | 24 | 245 | L ±5, W ±2, H ±2 mm; ±20 g |
| us.ovonicshop, 4 pezzi [primary] (WF) | 137 | 46 | 24 | 259 | ±5 mm; ±20 g |
| ampow, singolo [primary] (DIR) | 138 | 46 | 24 | 259 | L ±5, W ±2, H ±2 mm; ±20 g |
| ampow, 2 pezzi [primary] (WF) | 139 | 46 | 24 | 259 | L ±5, W ±2, H ±2 mm; ±20 g |
| ampow, 2 pezzi + checker [primary] (WF) | 139 | 47,3 | 25,4 | 253 | non indicata |

**Formato di riferimento (regolamento gare)**
- Regola ROAR 8.3.2.2.1 per i pacchi LiPo 2S in custodia rigida, dimensioni massime: "Length: 139mm +0mm/-3mm", "Width: 47mm +0mm/-2mm", "Height: 25.1mm +0mm/-3.0mm"; il pacco deve avere cavi che escono dalla custodia oppure punti di connessione esterni marcati (testo riportato in un articolo del 16 gennaio 2008; non verificato sul regolamento attuale) (WF) [secondary] — [Red RC, 16 gennaio 2008](https://www.redrc.net/?p=7371)

**Varianti e prodotti simili da NON confondere**
- Tabella comparativa pubblicata da OVONIC nella pagina Amazon.it (colonne nell'ordine): 2S 5000 mAh 50C Deans T: 137×45×24 mm, 297 g; 3S 5000 mAh 50C XT60+TRX: 155×42×24 mm, 343 g; 2S 5200 mAh 50C EC5: 138×47×24 mm, 251 g; 3S 5000 mAh 50C EC5: 138×41×24 mm, 308 g; 2S 5200 mAh 80C EC5: 138×46×24 mm, 270 g; 2S 5200 mAh 100C Deans T: 131×42×20 mm, 246 g; pesi con "dev.20g" (DIR) [secondary, tabella del produttore su Amazon] — [Amazon.it B098P5ZBJ6](https://www.amazon.it/OVONIC-Batteria-LiPo-5200-Plug/dp/B098P5ZBJ6). Esiste quindi un 5200 mAh "100C" con T-plug sensibilmente più piccolo (131×42×20): controllare il "C" prima dell'ordine.
- OVONIC 2S 5000 mAh 50C hardcase Deans (prodotto diverso): 139 × 46 × 25 mm, 273 g, "Charge Plug JST-XH", "Wire Length(mm): 115mm" (WF, dai prodotti correlati della pagina ampow) [primary] — [ampow.com](https://www.ampow.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-lipo-battery)
- Lo stesso 5000 mAh nella recensione LiveRC: 137 × 45 × 24 mm, 302 g (SNIP) [secondary] — [LiveRC](https://liverc.com/news/thursday-testimonials-ovonic-74v-5000mah-50c-2s-lipo-battery-pack/)
- Il 5200 mAh 2S 50C hardcase è venduto anche con EC5, EC3 e XT60, e in versione "80C" con XT60 (SNIP) [secondary] — [us.ovonicshop EC5](https://us.ovonicshop.com/products/ovonic-2s-5200mah-50c-7-4v-hardcase-lipo-battery-with-ec5-plug-for-1-10-arrma-car), [Amazon.com 80C XT60](https://www.amazon.com/OVONIC-Battery-5200mAh-Vehicles-Airplane/dp/B0FZJNTWC1)
- Esiste un 5200 mAh 2S "shorty" (formato corto) (SNIP) [secondary] — [rcdrone.top shorty](https://rcdrone.top/hi/products/ovonic-2s-5200mah-shorty-battery)
- Codice della confezione da 2 pezzi: "O50C52002S1PHCT2P" (SNIP, titolo eBay) [secondary] — [eBay](https://www.ebay.com/p/7019819982)

**Correnti**
- 50C continui e 100C burst dichiarati (WF) [primary] — [ampow.com, singolo](https://www.ampow.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-lipo-battery)
- Corrente continua di targa = 50 × 5,2 Ah = 260 A; burst = 100 × 5,2 Ah = 520 A [computed: C × capacità]. Sono valori nominali del pacco, non raggiungibili attraverso un T-plug e cavi 12 AWG (41 A in aria libera, vedi sezione 4). Con 15-20 A di picco il pacco lavora a 2,9-3,9 C [computed: I / 5,2 Ah].
- Energia = 7,4 V × 5,2 Ah = 38,48 Wh [computed; coincide con "38.48Wh" di [rcdrone.top](https://rcdrone.top/products/ovonic-2s-5200mah-battery)]

**Connettore di bilanciamento**
- Dichiarato "JST-XHR-3P" (Amazon.it, us.ovonicshop) oppure "JST-XH" (ampow, 2 pezzi): è il connettore di bilanciamento 2S a 3 poli della serie JST XH, passo 2,5 mm (dettagli in sezione 4) [primary] — [ampow.com, 2 pezzi](https://www.ampow.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-2pcs-lipo-battery), [datasheet JST XH](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf)

### Inferences
- Inviluppo massimo secondo il produttore: L = 139 + 5 = 144 mm; W = 47,3 + 2 = 49,3 mm; H = 25,4 + 2 = 27,4 mm [computed: nominale più grande tra le inserzioni + "dev." dichiarata]. Inviluppo minimo: 137 − 5 = 132 mm; 46 − 2 = 44 mm; 24 − 2 = 22 mm [computed].
- I valori nominali stanno tutti dentro (o a 0,3 mm da) il formato ROAR 139 × 47 × 25,1 mm: è molto probabile che il pacco reale misuri circa 137-139 × 46-47 × 24-25 mm, ma OVONIC non dichiara la conformità ROAR per questo pacco, quindi non è una garanzia.
- Tolleranza consigliata per il vano: sezione libera 50 × 28 mm (49,3 + 0,7 e 27,4 + 0,6 di gioco) e lunghezza regolabile da 132 a 144 mm (fermo scorrevole o spessore in schiuma), con il pacco trattenuto da una cinghia in velcro e non da un incastro a misura [computed/progetto]. Un incastro fisso a 138 × 46 × 24 + 0,5 mm rischia di non accettare il pacco reale.
- Se si misura prima il pacco reale: quota misurata + 1 mm in lunghezza e + 0,5 mm per lato in larghezza e altezza, più 1-2 mm di schiuma EVA.
- Il lato corto da cui escono i cavi deve restare aperto: servono lo spazio per la curva di due cavi 12 AWG in silicone (diametro esterno circa 4,5 mm, vedi sezione 4) e per la coppia di T-plug accoppiati (ogni metà Deans: corpo 16,5 mm, 26,2 mm con le linguette, vedi sezione 4). Prevedere almeno 50-60 mm liberi oltre la testata oppure far risalire i cavi sopra il pacco [stima].
- Peso da usare nei calcoli: 260 g nominali, 279 g nel caso peggiore (259 + 20) [computed].
- Lunghezza dei cavi di potenza: due indizi indipendenti concordano su circa 115-120 mm: (a) il 5000 mAh gemello dichiara "Wire Length(mm): 115mm"; (b) la mia misura in scala sull'immagine quotata del 5200 mAh dà circa 120 mm. Nessuno dei due è una quota dichiarata per questo pacco: nel CAD usare 100-140 mm come campo e progettare il percorso del cavo verso il T-plug del robot in modo che funzioni con 100 mm.
- Genere del T-plug: femmina sulla batteria secondo le immagini del produttore, in accordo con la convenzione (sorgente = femmina con i contatti protetti, vedi sezione 4); OVONIC non lo scrive a testo. Lato robot serve quindi un T-plug **maschio**.
- Uscita dei cavi: tutti da un solo lato corto, quelli di potenza in alto sulla testata. Il vano deve quindi avere la testata lato cavi aperta (o un'asola larga almeno quanto la testata nella parte alta) e il pacco può essere infilato dal lato opposto solo se la testata lato cavi resta libera.
- Acquisto: l'inserzione Amazon.it B098P5ZBJ6 (19,99 €, disponibilità immediata l'8 ottobre 2026) è l'opzione più semplice dall'Italia; ampow.com mostra il pacco singolo a 25,17 € "In Stock" con pagina in italiano e prezzi in euro, ma condizioni e tempi di spedizione in Italia non sono stati verificati.

### Gaps
- NON TROVATO: lunghezza dei cavi di potenza e del cavetto di bilanciamento del 5200 mAh con T-plug come dato dichiarato (nessuna pagina la indica, nemmeno dopo una ricerca mirata nella terza ripresa); resta solo la stima di circa 120 mm dalla foto.
- NON TROVATO: genere del T-plug dichiarato a testo dal produttore; l'unica evidenza è l'immagine di prodotto (femmina), che è un rendering.
- NON TROVATO: posizione esatta (quote) dell'intaglio di uscita dei cavi sulla testata.
- NON TROVATO: misure di terzi (calibro / bilancia) su questo pacco.
- NON TROVATO: corrente di carica raccomandata (le pagine indicano solo il limite di 4,2 V per cella).
- Non chiarito quale tolleranza sia quella vera: ±3 mm (Amazon.it) o ±5 / ±2 / ±2 mm (negozio del produttore); progettare per la più larga.
- Non chiarito il peso: 245 g, 253 g, 254 g o 259 g secondo la pagina.

## 2. Lunghezza del cavo dell'MG90S: basta per arrivare all'SSC-32 al centro del corpo? Quanto lasco per giunto?

### Takeaway
Tower Pro dichiara 25 cm e un datasheet di clone 250 ± 5 mm, ma alcuni negozi vendono "MG90S" con cavo da 175 mm o 24 cm: la lunghezza va misurata sui pezzi comprati. Con 250 mm il servo della coxa arriva sempre, quello del femore arriva per le zampe centrali ed è al limite per le quattro d'angolo, quello della tibia in genere NON arriva senza una prolunga da 150 mm.

### Cited Findings
- Tower Pro, pagina MG90S: "Servo wire/cable length: 25 cm"; connettore "JR (Fits JR and Futaba)" (WF) [primary] — [Tower Pro MG90S](https://www.towerpro.com.tw/product/mg90s-3/)
- Datasheet di un clone (Shenzhen Sky Star): "3.9 Connector wire 250mm±5mm"; "Stall current 750mA±10% [4,8 V] 860mA±10% [6,0 V]" (DIR, testo estratto dal PDF) [primary del clone] — [Sky Star, PDF su tinytronics.nl](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)
- 25 cm secondo Cool Components e Makers Electronics (SNIP) [secondary] — [Cool Components](https://coolcomponents.co.uk/products/mg90s-digital-metal-gear-servo), [Makers Electronics](https://makerselectronics.com/product/micro-servo-mg90s-half-metal-180-degree/)
- 24 cm (9,5 pollici) secondo ProtoSupplies (SNIP) [secondary] — [ProtoSupplies](https://protosupplies.com/product/servo-motor-micro-mg90s/)
- 175 mm secondo Domoticx (due inserzioni), take.app e reach.dog (SNIP) [secondary] — [Domoticx](https://domoticx.net/webshop/servo-22-kg-cm-digitaal-180-graden-mg90s), [take.app](https://take.app/uniktek/p/cm7kxqlb600jsgv7gqj5bsw73)
- Colori: marrone = massa, rosso = +V, arancione = segnale (SNIP) [secondary] — [Makers Electronics](https://makerselectronics.com/product/micro-servo-mg90s-half-metal-180-degree/), [ShillehTek](https://shillehtek.com/blogs/shillehtek-product-manuals/mg90s-metal-gear-micro-servo-motor-180-degree-9g-for-rc-plane-manual)
- Scheda SSC-32 / SSC-32U: "PC board size: 3.0" x 2.3"" cioè 76,2 × 58,4 mm; i connettori dei servo sono sui due lati lunghi (DIR, testo estratto dal PDF) [primary] — [scheda RB-LYN-850](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf)
- Il clone "SSC32-V2.5" (la scheda più probabile in mano all'utente secondo `ssc32.md`) è più piccolo: circa 72 × 55 mm, con gli header dei servo lungo i due lati lunghi e il blocco morsetti a 6 poli su un lato corto (misura fatta dal ricercatore di `ssc32.md` su immagini del venditore, incertezza circa ±1 mm) [secondary] — vedi `ssc32.md`, sezioni 1 e 2. Rispetto alla Lynxmotion il percorso interno dei cavetti cambia di circa 2 mm: trascurabile.
- Indicazioni generali sul lasco: "Leave enough slack when the cable is routed around robot joints"; il cavo deve adattarsi a tutto il campo di movimento previsto (WF; guida per robot industriali, senza valori numerici) [secondary] — [Pickit, FAQ robot cable routing](https://docs.pickit3d.com/en/3.3/optimize-your-application/hardware/faq-robot-cable-routing.html)

### Inferences
- Percorso interno al corpo [computed/stima; ipotesi: corpo 200 × 120 mm, SSC-32 da 76 × 58 mm al centro con i lati lunghi paralleli ai lati lunghi del corpo, zampe a x = 0 e x = ±80 mm]: dal connettore sul bordo della scheda al fianco del corpo 60 − 29 = 31 mm; più lo spostamento longitudinale (10-20 mm per le zampe centrali, 60-80 mm per quelle d'angolo); più circa 20 mm per la risalita della spina e le curve. Totale: 60-70 mm per le zampe centrali, 110-130 mm per quelle d'angolo.
- Lunghezza necessaria = percorso interno + distanza esterna del servo + lasco (circa 25 mm per ogni giunto attraversato) [computed]:

| Servo | Zampe centrali | Zampe d'angolo | Cavo da 250 mm | Cavo da 175 mm |
|---|---|---|---|---|
| Coxa (30-60 mm fuori, 0-1 giunti) | 90-155 mm | 140-215 mm | sufficiente | sufficiente al centro, al limite o insufficiente agli angoli |
| Femore (60-90 mm fuori, 1 giunto) | 145-185 mm | 195-245 mm | sufficiente al centro, al limite agli angoli (margine 5-55 mm) | insufficiente quasi ovunque |
| Tibia (110-160 mm fuori, 2 giunti) | 220-280 mm | 270-340 mm | insufficiente (o margine nullo) | insufficiente |

- Lasco per giunto [computed, geometria]: se il cavo attraversa il giunto vicino all'asse di rotazione la lunghezza del percorso quasi non cambia e il cavo lavora a flessione/torsione; se è fissato a distanza r dall'asse sui due lati, la corda tra i due fissaggi vale 2 × r × sin(θ/2) e varia fino a 2 × r su 180° di corsa. Con r = 10 mm servono fino a 20 mm di lasco; da qui la stima di 20-25 mm per giunto, da verificare muovendo a mano ogni giunto su tutta la corsa prima di fissare il cavo.
- La giunzione servo-prolunga (spina + collare, rigida) va tenuta dentro il corpo o lungo un tratto rigido della zampa, mai a cavallo di un giunto: la prolunga conviene quindi montarla dal lato della scheda.

### Gaps
- NON TROVATO: sezione (AWG) del cavetto originale dell'MG90S in una fonte del produttore (confermato anche dalla ricerca parallela in `servo_mg90s.md`). I calcoli della sezione 3 coprono perciò sia 26 sia 28 AWG.
- NON TROVATO: misura di terzi della lunghezza reale del cavo su MG90S recenti (cloni compresi).
- NON TROVATO: una regola quantitativa citabile per il lasco per giunto nei robot a zampe; i 20-25 mm sono una mia stima geometrica.

## 3. Prolunghe servo (JR / Futaba 3 pin): lunghezze, sezione, clip di ritenzione, dove comprarle; caduta di tensione

### Takeaway
Su Amazon.it si trovano prolunghe maschio-femmina 22 AWG "60 fili" da 100, 150, 300 e 500 mm in confezioni da 10-20 pezzi a 10-11 € e clip di blocco in confezioni da 30-40 pezzi a 11-14 €. A 1 A di stallo la caduta su 0,4-0,6 m (andata + ritorno) è 21-32 mV con 22 AWG, 54-80 mV con 26 AWG, 85-128 mV con 28 AWG: trascurabile sul singolo cavetto.

### Cited Findings
- Prolunghe su Amazon.it (risultati di ricerca letti l'8 ottobre 2026; prezzi dell'elenco) (DIR) [secondary]:
  - POFET 20 pezzi 15 cm, "22AWG 60 Fili", maschio-femmina, 10,99 € — [B087289HFS](https://www.amazon.it/dp/B087289HFS)
  - POFET 20 pezzi 10 cm, 22 AWG, 9,99 € — [B08727NKP2](https://www.amazon.it/dp/B08727NKP2)
  - POFET 10 pezzi 50 cm, 22 AWG, 9,99 € — [B08727C78V](https://www.amazon.it/dp/B08727C78V)
  - 10 cavi 30 cm, "22 AWG, 0,32 mm²", 11,98 € — [B078VSNC9D](https://www.amazon.it/dp/B078VSNC9D)
  - GTIWUNG 24 pezzi misti 75 / 150 / 300 / 600 mm, 22 AWG, 13,99 € — [B09B1ZSHKY](https://www.amazon.it/dp/B09B1ZSHKY)
  - RUNCCI-YUN 25 pezzi misti 100 / 150 / 300 / 500 / 600 mm, 10,99 € — [B082Y4QK9J](https://www.amazon.it/dp/B082Y4QK9J)
  - GTIWUNG 5 pezzi 150 mm, 8,99 € — [B07K34JQYT](https://www.amazon.it/dp/B07K34JQYT)
- Clip di ritenzione per la giunzione servo-prolunga su Amazon.it (DIR, titoli e prezzi dell'elenco) [secondary]: GTIWUNG 40 pezzi "Clip per Cavo di Prolunga Anti-Sciolto", 10,99 € — [B0C61PDHDF](https://www.amazon.it/dp/B0C61PDHDF); "Create idea 30 clip ... 30x9x6mm", 13,62 € — [B0C5XHZ1C4](https://www.amazon.it/dp/B0C5XHZ1C4); QUARKZMAN 18 pezzi in ABS nero, 13,49 € — [B0CNP7RMJS](https://www.amazon.it/dp/B0CNP7RMJS)
- Pololu 2165, prolunga intrecciata femmina-femmina da 6 pollici (150 mm): fili 22 AWG, 60 trefoli per conduttore, connettori JR femmina ai due capi; Pololu offre anche 6, 12 e 24 pollici femmina-femmina (779, 780, 785) e 12 pollici maschio-femmina intrecciata (2169) (WF) [primary] — [Pololu 2165](https://www.pololu.com/product/2165/specs)
- Eckstein (DE): "Servo Extension Cable 3Pin length 6"(150mm) Female - Female", SKU PO779, 22 AWG, 3,60 € IVA inclusa; la pagina mostrava "This item is not available in your delivery country" (WF; il paese rilevato era quello del server, disponibilità per l'Italia incerta) [secondary] — [Eckstein PO779](https://eckstein-shop.de/Servo-Extension-Cable-3Pin-length-6150mm-Female-Female_1)
- Esistono anche prolunghe JR da 15 cm in 26 AWG (eBay.de, 4,98 € per 5 pezzi; robu.in 26 AWG, 150 mm): la sezione va letta nell'inserzione, non è sempre 22 AWG (SNIP) [secondary] — [eBay.de, categoria cavi servo](https://www.ebay.de/b/RC-Modellbau-Stecker-Servokabeln-2-5-4/182178/bn_88621346), [robu.in](https://robu.in/?p=4143). Una ricerca di prolunghe Conrad / Reely / Modelcraft con sezione dichiarata in mm² non ha dato risultati.
- I pin a crimpare dei connettori JR sono "designed for 22–26 AWG wires"; passo 0,1 pollici; il JR ha due spigoli smussati e non ha la linguetta del Futaba J, ma i due sono compatibili (DIR) [primary] — [Pololu 1924](https://www.pololu.com/product/1924)
- Resistenza del rame: 22 AWG 52,94 Ω/km; 24 AWG 84,20 Ω/km; 26 AWG 133,86 Ω/km; 28 AWG 212,87 Ω/km (WF) [secondary] — [PowerStream](https://www.powerstream.com/Wire_Size.htm)

**Calcolo della caduta di tensione** [computed: ΔV = I × R; R = (Ω/km) × L / 1000; I = 1 A; L = lunghezza totale andata + ritorno; dati di resistenza da [PowerStream](https://www.powerstream.com/Wire_Size.htm)]

| Sezione | Ω/m | ΔV su 0,4 m a 1 A | ΔV su 0,5 m a 1 A | ΔV su 0,6 m a 1 A |
|---|---|---|---|---|
| 22 AWG | 0,0529 | 21 mV | 26 mV | 32 mV |
| 24 AWG | 0,0842 | 34 mV | 42 mV | 51 mV |
| 26 AWG | 0,1339 | 54 mV | 67 mV | 80 mV |
| 28 AWG | 0,2129 | 85 mV | 106 mV | 128 mV |

- Esempio: 26 AWG, 0,6 m: R = 133,86 × 0,6 / 1000 = 0,0803 Ω; ΔV = 1 A × 0,0803 Ω = 80 mV [computed].
- Caso peggiore 28 AWG, 0,6 m, 1 A: 128 mV = 2,1 % di 6,0 V; potenza nel cavo I² × R = 0,13 W [computed].
- Percorso reale della tibia (cavo originale 250 mm + prolunga 150 mm 22 AWG, cioè 0,5 m + 0,3 m andata e ritorno): R = 0,083 Ω se l'originale è 26 AWG, 0,122 Ω se è 28 AWG; a 0,95 A di stallo ΔV = 79 mV oppure 116 mV [computed; 0,95 A = 860 mA + 10 % dal [datasheet Sky Star](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)].

### Inferences
- La caduta sul singolo cavetto non è il problema; il punto critico è il tratto comune (cavo principale, morsetti e piste dell'SSC-32), dove le correnti di 9 servo per lato si sommano (sezione 4).
- Acquisto consigliato: 1 confezione da 20 prolunghe da 15 cm (6 per le tibie + 4 per i femori d'angolo + 10 di scorta) e 1 confezione di clip; la confezione da 10 cm è facoltativa (femori d'angolo con meno cavo in eccesso).
- Prolunga maschio-femmina: il capo "femmina" (guscio piatto con contatti femmina, uguale a quello del servo) va sui pin dell'SSC-32, il capo "maschio" (collare) riceve la spina del servo. Attenzione: nel modellismo i nomi sono spesso invertiti rispetto a questa definizione (lo segnala la stessa Pololu), guardare le foto.
- I valori di resistenza sono per rame pieno a 20 °C; trefoli e riscaldamento li alzano di qualche percento.

### Gaps
- NON TROVATO: resistenza di contatto dei contatti JR / Dupont da 2,54 mm in una fonte del produttore (ogni giunzione aggiunge due contatti in serie per filo).
- Non verificata la sezione reale delle prolunghe economiche ("22 AWG" è la dichiarazione del venditore).
- Non letta la scheda delle clip: verificare nelle foto che il modello scelto sia per connettori JR standard e non per connettori a Y.
- Disponibilità in Italia dell'articolo Eckstein PO779 incerta; Pololu vende in Europa tramite distributori (non verificato quali abbiano l'articolo a magazzino).

## 4. Portata dei cavi in silicone per AWG (12-22), sezioni consigliate per 15-20 A di picco e 5-8 A medi; puntalini; T-plug contro XT30 / XT60; JST-XH

### Takeaway
Per tratti corti in aria libera la tabella "chassis wiring" dà 41 A a 12 AWG, 32 A a 14 AWG, 22 A a 16 AWG, 16 A a 18 AWG, 11 A a 20 AWG, 7 A a 22 AWG: cavo principale 14 AWG (o 12 AWG come quello della batteria), due coppie 16 AWG verso VS1 e VS2 dell'SSC-32 (limite della scheda: 15 A di picco e 3-5 A continui per lato), 22 AWG per la logica. XT60 Amass: 30 A nominali / 60 A istantanei, 0,55 mΩ; XT30U: 15 A / 30 A, insufficiente; W.S. Deans dichiara per l'Ultra Plug 0,10 mΩ ma nessuna corrente nominale; l'unico T-plug con dati di targa trovato è l'Amass AM-1015E: 25 A massimi (con 16 AWG), 50 A istantanei, 0,45 mΩ, sufficiente per questo robot. Sotto vite: puntalini, non trefoli stagnati.

### Cited Findings

**Portata e resistenza per AWG** (WF) [secondary; la pagina indica come fonte l'"Handbook of Electronic Tables and Formulas"] — [PowerStream](https://www.powerstream.com/Wire_Size.htm)

| AWG | Ø conduttore (mm) | Sezione (mm²) [computed: π × d² / 4] | Ω/km | Max A "chassis wiring" | Max A "power transmission" | 25 A/mm² [computed] |
|---|---|---|---|---|---|---|
| 12 | 2,052 | 3,31 | 5,209 | 41 | 9,3 | 83 A |
| 14 | 1,628 | 2,08 | 8,282 | 32 | 5,9 | 52 A |
| 16 | 1,290 | 1,31 | 13,172 | 22 | 3,7 | 33 A |
| 18 | 1,024 | 0,82 | 20,943 | 16 | 2,3 | 21 A |
| 20 | 0,813 | 0,52 | 33,292 | 11 | 1,5 | 13 A |
| 22 | 0,645 | 0,33 | 52,939 | 7 | 0,92 | 8 A |
| 24 | 0,511 | 0,20 | 84,198 | 3,5 | 0,577 | 5 A |
| 26 | 0,404 | 0,13 | 133,857 | 2,2 | 0,361 | 3 A |
| 28 | 0,320 | 0,08 | 212,872 | 1,4 | 0,226 | 2 A |

- "Chassis wiring" vale per cavi in aria libera, non in fascio ("meant for wiring in air, and not in a bundle"); "power transmission" usa la regola dei 700 circular mils per ampere, "very very conservative" (WF) [secondary] — [PowerStream](https://www.powerstream.com/Wire_Size.htm)
- Regola pratica per il cavo in silicone (isolante da circa 200 °C): circa 25 A per mm²; esempio della pagina 0,5 mm² = 12,5 A; definita dalla pagina stessa "rough rule of thumb" (WF) [community] — [Gogo:Tronics](https://sparks.gogo.co.nz/silicone-wire-current-capacity.html). È una regola da modellismo, aggressiva: usare la colonna "chassis wiring" come limite di progetto.

**Costruzione dei cavi in silicone** [secondary]
- 12 AWG: 680 trefoli da 0,08 mm, Ø esterno 4,5 mm; 14 AWG: 400 × 0,08 mm, Ø 3,5 mm; 16 AWG: 252 × 0,08 mm, Ø 3,0 mm; 18 AWG: 150 × 0,08 mm, Ø 2,3 mm; 22 AWG: 60 × 0,08 mm, Ø 1,7 mm (SNIP: tabella Studica e inserzione Newegg, pagine non lette direttamente) — [Studica](https://www.studica.com/16-awg-redblack-flexible-silicone-bonded-wire-8m)
- 20 AWG: 100 × 0,08 mm, circa 0,5 mm², Ø esterno 1,8 mm (SNIP) — [Gogo:Tronics 20 AWG](https://sparks.gogo.co.nz/catalog/Wire-and-Connectors-37/Wire-169/Red-Silicone-Wire-20AWG-Per-50cm-Super-Flexible-896.html?SuID=1264)
- Conferma dai titoli Amazon.it: "14 Gauge 2.07 mm² ... 400 Fili 0,08 mm di Rame Stagnato"; "16 Gauge 1.27 mm² ... 252 Fili 0,08 mm" (DIR) — [B0C53D343Y](https://www.amazon.it/dp/B0C53D343Y), [B0D9VDPG54](https://www.amazon.it/dp/B0D9VDPG54)
- Cavo in silicone 14 AWG a metraggio (Switch Electronics, venduto da Maplin Pro, codice 403005): "Conductor Cross Section: 2.07mm²", "Conductor Stranding: 400/0.08mm", "Conductor Material: Tinned Copper", "Overall Diameter: 3.5mm", "Voltage Rating: 600V", "Operating Temperature: -60°C to 200°C", "Current Rating: 55.5A" (WF) [secondary] — [Maplin Pro, 14 AWG 400/0.08](https://pro.maplin.co.uk/products/black-silicone-lead-wire-14awg-400-0-08mm-price-per-metre)
- Disaccordo sul diametro esterno del 14 AWG: 3,5 mm (Maplin Pro, Studica) contro 3,7 mm per il Mueller Electric WI-M-14 (420 trefoli da 0,08 mm, 600 V, 200 °C; SNIP, listino RS) [secondary] — [RS, Mueller WI-M-14](https://ch.rs-online.com/web/p/schaltdraht/2431645). Per fori e canaline contare 4 mm.
- Disaccordo sulla portata del 14 AWG in silicone: 55,5 A secondo il venditore (Maplin Pro), 52 A con la regola dei 25 A/mm², 32 A nella colonna "chassis wiring" di PowerStream. I valori alti presuppongono l'isolante a 200 °C e cavo singolo in aria; dentro un corpo stampato in PLA / PETG, che cede al calore molto prima dell'isolante (PLA e PLA-CF a 54-55 °C secondo le schede riportate in `giunti_stampa.md`, sezione sui materiali), il limite di progetto resta la colonna "chassis wiring" [confronto mio tra le fonti citate].
- Rame effettivo = n × π × (0,04 mm)²: 680 → 3,42 mm²; 400 → 2,01 mm²; 252 → 1,27 mm²; 150 → 0,75 mm²; 100 → 0,50 mm²; 60 → 0,30 mm² [computed]. I cavi in silicone "18 AWG" e "22 AWG" hanno quindi circa il 9 % di rame in meno della sezione AWG teorica (0,82 e 0,33 mm²).

**Caduta sul cavo principale** [computed: ΔV = I × (Ω/km) × L / 1000 con L = 0,30 m andata + ritorno; P = I² × R]

| Sezione | R su 0,30 m | ΔV a 20 A | P a 20 A | ΔV a 10 A | ΔV a 8 A |
|---|---|---|---|---|---|
| 12 AWG | 1,56 mΩ | 31 mV | 0,63 W | 16 mV | 13 mV |
| 14 AWG | 2,48 mΩ | 50 mV | 0,99 W | 25 mV | 20 mV |
| 16 AWG | 3,95 mΩ | 79 mV | 1,58 W | 40 mV | 32 mV |
| 18 AWG | 6,28 mΩ | 126 mV | 2,51 W | 63 mV | 50 mV |

**Limite dell'SSC-32**
- "VS peak current: max 15 amps per side"; "VS steady current: max 3-5 amps per side recommended" (DIR, testo estratto dal PDF) [primary] — [scheda RB-LYN-850 (SSC-32U)](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf)
- VS1 alimenta i canali 0-15 e VS2 i canali 16-31; con i due ponticelli VS1 = VS2 inseriti "you can power EITHER VS1 or VS2, but not both"; ci sono due ponticelli "because of the current involved" (DIR, testo estratto dal PDF) [primary] — [guida SSC-32U, pagine 9, 10 e 16](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf)
- SSC-32 originale: "Apply 4.8vdc to 6.0vdc when using micro servos" sui morsetti VS1 e VS2 (DIR, testo estratto dal PDF) [primary] — [manuale SSC-32 Ver 2.0](https://hobbielektronika.hu/forum/getfile.php?id=81561)

**Connettori di potenza**

| Connettore | Corrente nominale | Corrente di picco | Resistenza di contatto | Cavo | Fonte |
|---|---|---|---|---|---|
| Amass XT60 | 30 A | 60 A istantanei | 0,55 mΩ | 12 AWG | [primary] (DIR) |
| Amass XT30U | 15 A | 30 A | NON TROVATO | NON TROVATO | [secondary] (WF) |
| W.S. Deans Ultra Plug | non dichiarata dal produttore; 60 A secondo una fonte hobbistica | "75 Amp & higher" secondo la stessa fonte | 0,10 mΩ | "wide range of wire gauges" | [primary] per resistenza (WF); [community] per le correnti |
| Amass AM-1015E (T-plug di marca, non Deans) | "25A MAX (16AWG / △≤85K)" | 50 A istantanei | 0,45 mΩ | 16 AWG (condizione di prova) | [secondary, dati Amass riportati da un rivenditore] (WF) |
| T-plug clone senza marca | NON TROVATO | NON TROVATO | NON TROVATO | – | – |

- Amass XT60 (scheda tecnica Amass V1.2, XT60-F e XT60-M): corrente nominale 30 A, istantanea 60 A, resistenza di contatto 0,55 mΩ, DC 500 V, ottone dorato, corpo PA UL94 V0, 1000 inserzioni raccomandate, cavo raccomandato 12 AWG, da −20 a 120 °C; uso raccomandato XT60-F = batteria, XT60-M = controller (DIR, testo estratto dal PDF) [primary, copia ospitata da CMU] — [Amass XT60 spec V1.2](https://mrsdprojects.ri.cmu.edu/2025teamb/wp-content/uploads/sites/84/2025/05/xt60.pdf)
- Holybro riporta i dati Amass: XT60 con 12 AWG, 30 A continui (4 ore, aumento di temperatura < 60 °C), 60 A per 1 minuto (WF) [secondary] — [Holybro](https://docs.holybro.com/power-module-and-pdb/power-module/connector-and-wire-rating)
- Disaccordo: un rivenditore indica per l'XT60H "35A MAX (12AWG, ΔT ≤ 85K)" (SNIP) [secondary] — [Thingbits](https://www.thingbits.in/products/amass-xt60h-male-female-connector)
- Amass XT30U (XT30U-M / XT30U-F): corrente continua 15 A, picco 30 A, da −20 a 120 °C (WF) [secondary] — [Pimoroni](https://shop.pimoroni.com/products/amass-xt30-connector); "15A" anche nel titolo Maplin (SNIP) — [Maplin](https://pro.maplin.co.uk/products/black-male-xt30u-gold-plated-connector-15a-amass)
- Deans Ultra Plug originale: peso 4,73 g; corpo lungo 0,650 pollici, lunghezza complessiva 1,030 pollici, altezza 0,650 pollici, larghezza 0,300 pollici; resistenza 0,10 mΩ; "Usable with a wide range of wire gauges"; nessuna corrente nominale; codici 1310-1315 (WF) [primary] — [W.S. Deans, Ultra Plug](https://www.wsdeans.com/collections/ultra-plug). In millimetri: 16,5 / 26,2 / 16,5 / 7,6 mm [computed: × 25,4].
- "rated for 60 Amps of continuous load, up to 75 Amp & higher bursts" (WF) [community] — [RC Helicopter Fun](https://www.rchelicopterfun.com/deans-connector.html)
- Genere: "A Female (source) and Male (device) Deans Ultra Connector Set", cioè femmina sulla batteria e maschio sul carico (WF) [community] — [RC Helicopter Fun](https://www.rchelicopterfun.com/deans-connector.html)
- T-plug Amass AM-1015E (l'unico T-plug con dati di targa di un costruttore che ho trovato): "Rated Current: 25A MAX (16AWG / △≤85K)", "Instantaneous Current: 50A", "Contact Resistance: 0.45mΩ", "Withstand Voltage: 600V DC", "Working Temperature: -20℃ to 120℃", "Service Life: 1000 Mating Cycles", "Material: PA / Brass (Gold-Plated)", "UL94 V-0"; la pagina lo descrive come "skid-proof T-plug design" e non ne dichiara la compatibilità con il Deans (WF) [secondary] — [Thingbits, Amass AM-1015E](https://thingbits.in/products/amass-am-1015e-male-female-connector)
- Disaccordo tra rivenditori sulla corrente dell'Amass AM-1015: 25 A (Thingbits, videotronics), 20 A (Maplin, AM-1015-M), 36 A (campo "specification" di altre pagine Maplin) (SNIP) [secondary] — [Maplin AM1015 20 A](https://pro.maplin.co.uk/products/male-t-plug-connector-20a-amass-am1015), [videotronics 25 A](https://videotronics.com.cy/product/46682), [Maplin 36 A](https://pro.maplin.co.uk/products/female-t-plug-connector-with-cap-36a-amass). Nessuna scheda tecnica Amass originale letta.
- T-plug cloni: qualità variabile, spesso "will not fit well with other copies or even the originals"; il corpo in plastica si deforma se scaldato troppo in saldatura (WF) [community] — [RC Helicopter Fun](https://www.rchelicopterfun.com/deans-connector.html)
- Caduta sui contatti a 20 A: XT60 0,55 mΩ × 20 A = 11 mV per contatto (22 mV sui due poli, 0,44 W); Deans 0,10 mΩ × 20 A = 2 mV per contatto [computed dai valori dei produttori; per i cloni il valore reale è ignoto].

**JST XH (connettore di bilanciamento)** (DIR, testo estratto dal PDF) [primary] — [datasheet JST XH](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf)
- Passo 2,5 mm (non 2,54); corrente 3 A AC/DC con AWG 22; 250 V; da −25 a +85 °C; resistenza di contatto iniziale 10 mΩ max (20 mΩ dopo prove ambientali); fili da AWG 30 a AWG 22; Ø isolante da 0,9 a 1,9 mm; altezza montato su scheda 9,8 mm.
- Guscio a 3 circuiti XHP-3: quota A = 5,0 mm, quota B = 9,8 mm (larghezza del guscio); header corrispondenti B3B-XH-A (verticale) e S3B-XH-A (orizzontale).

**Puntalini**
- Phoenix Contact, "The problems with tinning wires" (2018): quando il morsetto stringe un filo stagnato "the tin can fracture and cause wire strands to pull apart from one another, creating voids"; i cicli termici allentano il serraggio; "Adding tin can make the wire larger than the terminal block is rated for"; conclusione: "tinning wires could be the reason for loose connections in screw terminal blocks ... A great alternative is to use ferrules and ensure the screws are tightened to the proper specification" (DIR, testo estratto dal PDF) [primary] — [Phoenix Contact](https://assets.phoenixcontact.com/file/be20e58a-773f-4be9-a3f9-43ed9b1dc431/media/original)
- Puntalini Phoenix Contact a listino RS: perno Ø 1,4 mm per 18 AWG; perno Ø 1,7 mm (lungo 10 mm) per 16 AWG; perno Ø 2,2 mm per 14 AWG (SNIP) [secondary] — [RS 18 AWG](https://ph.rs-online.com/web/p/bootlace-ferrules/0609911), [RS 16 AWG](https://uk.rs-online.com/web/p/bootlace-ferrules/2544868), [RS 14 AWG](https://uk.rs-online.com/web/p/bootlace-ferrules/0608332)
- Kit con pinza su Amazon.it: "Pinza Crimpatrice, 1800 Pezzi ... Set di Puntalini, 0,25-10mm²", 15,99 € (DIR, titolo e prezzo dell'elenco) [secondary] — [B0FPDZ8SGR](https://www.amazon.it/dp/B0FPDZ8SGR)

### Inferences
- Sezioni consigliate per 15-20 A di picco e 5-8 A medi:
  - batteria → fusibile → interruttore → regolatore: 14 AWG (32 A "chassis"; 50 mV e 1 W a 20 A su 0,3 m); 12 AWG se si vuole la stessa sezione del cavo della batteria; 16 AWG (22 A) è il minimo; 18 AWG (16 A) NON copre 20 A;
  - regolatore → VS1 e regolatore → VS2: 16 AWG per coppia (9 servo per lato: stallo 9 × 0,95 = 8,5 A < 15 A di picco per lato; media 2,5-4 A per lato, dentro i 3-5 A raccomandati) [computed];
  - logica (VL, 5 V dell'ESP32-S3): 22 AWG (7 A "chassis", ampiamente sufficiente).
- Abbinamento filo-puntalino per sezione di rame [computed dalla tabella]: 14 AWG (2,0-2,1 mm²) → 2,5 mm²; 16 AWG (1,27-1,31 mm²) → 1,5 mm²; 18 AWG (0,75-0,82 mm²) → 0,75 o 1,0 mm²; 20 AWG (0,5 mm²) → 0,5 mm²; 22 AWG (0,30-0,33 mm²) → 0,34 mm².
- Il T-plug resta sulla batteria; lato robot serve un T-plug maschio. Se a valle si preferisce l'XT60 (30 A nominali, più robusto dei cloni T): adattatore T-plug maschio → XT60 femmina e XT60 maschio sul robot. L'XT30U (15 A nominali) non copre 15-20 A di picco.
- Il T-plug basta per questo robot: l'unico dato di targa trovato per un T-plug (Amass AM-1015E, 25 A massimi con 16 AWG e 50 A istantanei) copre i 15-20 A di picco e lascia un margine di 3-5 volte sui 5-8 A medi; a 20 A la caduta su un contatto da 0,45 mΩ è 9 mV [computed: 0,45 mΩ × 20 A]. Il T-plug montato da OVONIC sulla batteria è però di marca ignota: se dopo qualche minuto di camminata il connettore è caldo al tatto, è il primo componente da sostituire (o da scavalcare con l'adattatore verso XT60).
- Usare T-plug della stessa marca sui due lati quando possibile: l'accoppiamento tra cloni diversi è il difetto più citato.
- Connettore di bilanciamento XH a 3 poli: va lasciato accessibile per il caricabatterie e per un cicalino LiPo; con passo 2,5 mm su 3 poli lo scarto rispetto a uno strip da 2,54 mm è 0,08 mm sull'ultimo pin [computed: 2 × 0,04].

### Gaps
- NON TROVATO: corrente nominale ufficiale W.S. Deans per l'Ultra Plug.
- NON TROVATO: datasheet Amass dell'XT30U leggibile (tme.eu bloccato; il PDF LCSC contiene solo immagini): resistenza di contatto e cavo raccomandato mancano.
- NON TROVATO: tipo, passo e sezione massima dei morsetti a vite dell'SSC-32 e del clone "V2.5": non è certo che un puntalino da 2,5 mm² (14 AWG) entri, per questo si propone il 16 AWG; va misurata l'apertura del morsetto.
- NON TROVATO: scheda tecnica del produttore dei cavi in silicone (i diametri esterni vengono da inserzioni).
- NON TROVATO: raggio minimo di curvatura dei cavi in silicone 12-14 AWG da una fonte del produttore.

## 5. Gestione dei cavi nei robot a zampe; dimensioni del guscio del connettore servo a 3 pin per dimensionare i fori passacavo

### Takeaway
La spina JR femmina del servo misura 7,9 × 2,75 × 14,0 mm (±0,25) e il collare maschio di una prolunga 10,3 × 4,0 × 18,0 mm (±0,25): per tre cavetti per zampa servono asole da almeno 10 × 6 mm (solo spine femmina) o 12 × 7 mm (se passa anche un collare), oppure asole aperte con coperchio. Sull'instradamento esistono solo principi generali (lasco sufficiente per tutta la corsa, scarico di trazione solidale al pezzo protetto, passaggio vicino all'asse del giunto); non ho trovato una guida quantitativa specifica per esapodi.

### Cited Findings
- Guscio JR femmina (quello sul cavo del servo), dal disegno quotato Pololu: larghezza 7,90 ± 0,25 mm (lato bocca) e 7,70 ± 0,25 mm (lato cavo); spessore 2,75 ± 0,25 mm e 2,65 ± 0,25 mm; lunghezza 14,00 ± 0,25 mm; passo 2,54 ± 0,10 mm; interasse tra i contatti esterni 5,08 ± 0,20 mm (DIR, quote lette dall'immagine del disegno) [primary per il componente Pololu; i gusci di altri produttori possono differire di qualche decimo] — [disegno Pololu, guscio femmina](https://a.pololu-files.com/picture/0J9699.1200.jpg), [Pololu 1925, immagini](https://www.pololu.com/product/1925/pictures)
- Collare JR maschio (estremità "maschio" di una prolunga, dentro cui entra la spina del servo): 10,30 ± 0,25 mm × 4,00 ± 0,25 mm × 18,00 ± 0,25 mm di lunghezza; apertura interna 8,05 × 2,80 mm (DIR, quote lette dall'immagine del disegno) [primary per il componente Pololu] — [disegno Pololu, collare maschio](https://a.pololu-files.com/picture/0J9700.1200.jpg), [Pololu 1925, immagini](https://www.pololu.com/product/1925/pictures)
- I due disegni Pololu sono stati riguardati nella terza ripresa: tutte le quote qui sopra sono confermate. Lo spessore nominale del guscio femmina (2,75 mm lato bocca, 2,65 mm lato cavo) è maggiore del passo di 2,54 mm; il collare maschio (4,00 mm) lo è di molto (DIR) [primary per il componente Pololu] — [disegno Pololu, guscio femmina](https://a.pololu-files.com/picture/0J9699.1200.jpg)
- Nei robot esapodi Lynxmotion la mappa dei canali della SSC-32 lascia un canale libero tra una zampa e l'altra: i servo di coxa ("horizontal hip") sui canali 0, 4 e 8 per il lato destro e 16, (20) e 24 per il sinistro, con femore e tibia sui due canali successivi; quale zampa (anteriore o posteriore) stia sullo 0 e sul 16 cambia tra le fonti (tabella di un utente del forum: RF = 0, RM = 4, RR = 8, LF = 16, LR = 24; file di configurazione Lynxmotion T-Hex del 2010: cRRCoxaPin = P8, cRMCoxaPin = P4) (SNIP: i documenti sono sul forum RobotShop, non raggiungibile, quindi non letti direttamente) [community] — [PDF sul forum RobotShop](https://community.robotshop.com/forum/uploads/default/original/3X/8/a/8ab0b3f5d68a0778d8261b5927100dca789b8e1e.pdf), [configurazione T-Hex](https://community.robotshop.com/forum/uploads/short-url/8W5FB040TSbOckHZ7bkcSjq8QzX.pdf)
- Sulla SSC-32U il pin più esterno (verso il bordo della scheda) è la massa, quello centrale l'alimentazione, quello interno il segnale; VS1 = canali 0-15, VS2 = canali 16-31 (DIR, testo estratto dal PDF) [primary] — [guida SSC-32U](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf)
- Principi generali (robot industriali): "Leave enough slack when the cable is routed around robot joints"; lo scarico di trazione va messo "in a location that moves rigidly with" il dispositivo protetto; tenere i cavi di segnale lontani da attuatori e cavi di potenza (WF) [secondary] — [Pickit, FAQ robot cable routing](https://docs.pickit3d.com/en/3.3/optimize-your-application/hardware/faq-robot-cable-routing.html)
- Letteratura brevettuale: far passare il cavo per il centro di rotazione del giunto fa sì che il giunto torca il cavo invece di piegarlo, a prezzo di più spazio lungo l'asse; pieghe strette, torsione e strisciamento su superfici ruvide accorciano la vita del cavo (SNIP, non letto sul brevetto) [secondary] — [WO2014008662A1](https://patents.google.com/patent/WO2014008662A1/fr), [US 5863010](https://patents.justia.com/patent/5863010)
- Consigli di costruttori di esapodi (forum RobotShop): stendere completamente la zampa prima di fissare i cavi dei servo, così il movimento normale non li tende; guaina a spirale o calza intrecciata tagliata abbastanza lunga da permettere tutta la corsa; fascette per fissare la guaina alla zampa (SNIP: la pagina dà errore 403 e non è stata letta) [community] — [RobotShop forum, cable management for servo cables](https://community.robotshop.com/forum/t/cable-management-for-servo-cables/12664)
- Un robot quadrupede di ricerca usa scarichi di trazione fissati vicino a ogni attuatore, sul busto e sull'accoppiamento anca-ginocchio (SNIP) [secondary] — [arXiv 2503.14255](https://arxiv.org/pdf/2503.14255)
- Guaina a spirale su Amazon.it: GTIWUNG Ø 6 mm, 15 m, 10,99 € — [B07WDRYFXV](https://www.amazon.it/dp/B07WDRYFXV); Ø 8 mm, 12 m, 9,99 € — [B07YFQMGGX](https://www.amazon.it/dp/B07YFQMGGX) (DIR, titoli e prezzi dell'elenco) [secondary]

### Inferences
- Ingombro massimo della spina del servo: 8,15 × 3,00 mm (7,90 + 0,25; 2,75 + 0,25); diagonale 8,7 mm [computed]. Foro per UNA spina: asola ≥ 9 × 4 mm oppure foro tondo ≥ 9,5 mm (gioco 0,4-0,5 mm per lato per la stampa FDM).
- Ingombro massimo del collare maschio: 10,55 × 4,25 mm; diagonale 11,4 mm [computed]. Se dal foro deve passare un collare: asola ≥ 11,5 × 5 mm oppure foro tondo ≥ 12 mm.
- Tre cavetti per zampa nello stesso passaggio, infilati uno alla volta: l'ultima spina passa accanto a due piattine già infilate (piattina a 3 fili: circa 3,9 × 1,3 mm, stima da misurare). Asola consigliata 10 × 6 mm (solo spine femmina) oppure 12 × 7 mm (se passa anche un collare) [computed/stima]. Alternativa migliore: asole aperte a U con coperchio o pettine a scatto, così nessuna spina deve attraversare un foro chiuso e un servo si sostituisce senza sfilare gli altri.
- Sull'header della scheda lo spessore massimo della spina (3,00 mm) supera il passo di 2,54 mm: nove spine adiacenti possono forzare. Conviene lasciare un canale libero tra una zampa e l'altra (0-2, 4-6, 8-10 su VS1 e 16-18, 20-22, 24-26 su VS2), che è anche lo schema usato dagli esapodi Lynxmotion (vedi sopra) [computed dal disegno Pololu; da verificare sulle spine reali: nella pratica le spine dei servo si montano affiancate su header a passo 2,54 mm, quindi i gusci reali stanno probabilmente nella parte bassa della tolleranza, circa 2,5 mm]. Nota di coerenza: `ssc32.md` propone i canali 0-8 e 16-24 (contigui); le due mappe sono equivalenti dal punto di vista elettrico (9 servo per lato), cambia solo l'ingombro delle spine e la tabella dei canali nel firmware.
- Altezza sopra la scheda: la spina è lunga 14 mm e il cavo esce in verticale; prevedere almeno 14 mm + raggio di curva del cavetto (circa 10 mm) = 25 mm liberi sopra il piano dei pin, oppure piegare i cavi verso l'esterno subito sopra la spina [stima].
- Regole pratiche di instradamento proposte [mia sintesi dei principi citati, non una norma]:
  1. un punto di fissaggio (clip stampata o fascetta) su ciascun lato di ogni giunto, sul pezzo rigido, a 10-15 mm dall'asse;
  2. il cavo attraversa il giunto il più vicino possibile all'asse e con un'ansa libera; verificare a mano la posizione più chiusa e la più aperta prima di stringere;
  3. niente fascette strette sull'ansa mobile; fascette ferme solo sui punti di ancoraggio;
  4. primo ancoraggio a 10-20 mm dall'uscita del cavo dal servo: il cavetto esce da una fessura della cassa senza vero pressacavo;
  5. i tre cavetti di una zampa riuniti in guaina a spirale Ø 6 mm solo nei tratti rigidi (femore, interno del corpo);
  6. cavi di potenza 14-16 AWG separati dal cavetto seriale e dal flat della camera.
- Le clip di blocco (sezione 3) servono solo dove c'è una giunzione servo-prolunga; sull'header dell'SSC-32 la ritenzione è data dall'attrito dei contatti: un pettine stampato sopra le spine evita che si sfilino con le vibrazioni.

### Gaps
- NON TROVATO: lunghezza della coppia spina + collare accoppiati (serve per l'alloggiamento della giunzione): stimare 22-28 mm e misurare.
- NON TROVATO: diario di costruzione di un esapode con MG90S che documenti lunghezze dei cavi, anse e fissaggi con misure. Le due fonti più promettenti non sono leggibili: il forum RobotShop (discussioni "Cable management for servo cables" e "Phoenix code my MG90 hexapod") risponde con una verifica anti-bot anche dal browser, e il progetto Hackster "3D printed hexapod" dà errore 403. L'utente può aprirle a mano: [discussione sui cavi](https://community.robotshop.com/forum/t/cable-management-for-servo-cables/12664), [esapode MG90](https://community.robotshop.com/forum/t/phoenix-code-my-mg90-hexapod/25538), [Hackster](https://www.hackster.io/sir-kuhnhero/3d-printed-hexapod-05a60c).
- Non letta direttamente la mappa dei canali Lynxmotion (solo riassunti del motore di ricerca, in disaccordo su quale zampa stia sul canale 0).
- NON TROVATO: numero di cicli di flessione sopportati dal cavetto originale dei servo.
- NON TROVATO: diametro dei singoli fili del cavetto MG90S (stimato 1,0-1,3 mm).

## 6. Lista di cablaggio per un robot con corpo di circa 200 × 120 mm

### Takeaway
Lista coerente con l'architettura di `alimentazione.md` (batteria → T-plug → fusibile 20 A → interruttore → nodo a stella → regolatore servo 6,0 V → VS1 e VS2; 5 V separati per l'ESP32-S3; VL dalla batteria): circa 0,5 m di 14 AWG, 0,6 m di 16 AWG, 18 cavetti servo con 6-10 prolunghe da 100-150 mm, 3 fili per la seriale. Tutte le lunghezze sono stime da confermare sul CAD.

### Cited Findings
- Architettura e componenti di alimentazione: vedi `alimentazione.md` (regolatore servo [Pololu D42V110F6 #5673](https://www.pololu.com/product/5673), 5 V [Pololu D24V22F5 #2858](https://www.pololu.com/product/2858), fusibile a lama mini da 20 A, interruttore).
- Limiti di corrente dell'SSC-32, 15 A di picco e 3-5 A continui per lato (DIR) [primary] — [scheda RB-LYN-850](https://media.digikey.com/pdf/Data%20Sheets/RobotShop%20PDFs/RB-LYN-850-Datasheet.pdf)
- Materiali su Amazon.it (DIR, titoli e prezzi degli elenchi di ricerca dell'8 ottobre 2026) [secondary]:
  - "3 Pairs T-Plug Connettore, Deans T Plug Connettori Maschio e Femmina con Cavo di Silicone 100mm 14 AWG", 8,99 € — [B0FVRHF7GW](https://www.amazon.it/dp/B0FVRHF7GW)
  - "RUIZHI 5 pairs Deans Style T Connettore Femmina e Maschio ... Filo in Silicone 14AWG", 11,99 € — [B098WRZMPQ](https://www.amazon.it/dp/B098WRZMPQ)
  - "Set di 3 paia di connettori a T con filo in silicone da 12 AWG", 10,99 € — [B07QM1WS2J](https://www.amazon.it/dp/B07QM1WS2J)
  - "2 Pezzi Deans T Plug a XT60 Adattatore, XT60 Femmina a T Maschio ... Cavo Silicone 10cm 14AWG", 8,99 € — [B0FGCLCK1R](https://www.amazon.it/dp/B0FGCLCK1R)
  - Cavo silicone 14 AWG, 2,5 m rosso + 2,5 m nero, 400 × 0,08 mm, 13,99 € — [B0C53D343Y](https://www.amazon.it/dp/B0C53D343Y); TUOFENG 14 AWG 1,5 m + 1,5 m, 9,99 € — [B075M578PB](https://www.amazon.it/dp/B075M578PB)
  - Cavo silicone 16 AWG, 2,5 m rosso + 2,5 m nero, 252 × 0,08 mm, 11,99 € — [B0D9VDPG54](https://www.amazon.it/dp/B0D9VDPG54)
  - Prolunghe, clip, puntalini e guaina: vedi sezioni 3, 4 e 5.

### Inferences

**Lista di cablaggio** (lunghezze [computed/stima] per corpo 200 × 120 mm, SSC-32 al centro, batteria sotto o dietro la scheda)

| # | Tratta | Cavo | Lunghezza | Sezione | Terminazioni | Q.tà |
|---|---|---|---|---|---|---|
| 0 | Cavi propri della batteria | rosso/nero, parte del pacco | circa 120 mm (stima dalla foto, da misurare) | 12 AWG (dichiarato) | T-plug femmina (dalle immagini del produttore, da confermare) + JST-XH 3 poli di bilanciamento | – |
| 1 | Batteria → robot | codino precablato rosso/nero in silicone | 100 mm | 14 AWG (o 12 AWG) | T-plug maschio lato robot | 1 |
| 2 | Positivo: codino → portafusibile a lama mini 20 A | silicone rosso | 30-60 mm | 14 AWG | saldato + termorestringente | 1 |
| 3 | Fusibile → interruttore → nodo a stella | silicone rosso | 2 × 60-100 mm | 14 AWG | saldato sulle piazzole (interruttore a MOSFET Pololu #2815, prima scelta di `alimentazione.md`) o faston (bilanciere) | 2 |
| 4 | Negativo: codino → nodo a stella | silicone nero | 80-150 mm | 14 AWG | saldato | 1 |
| 5 | Nodo → ingresso regolatore servo | coppia rosso/nero | 50-100 mm | 14 AWG | saldato o morsetto + puntalino 2,5 mm² | 1 |
| 6 | Uscita regolatore → SSC-32 VS1 | coppia rosso/nero | 80-150 mm | 16 AWG | puntalini 1,5 mm² sul morsetto a vite | 1 |
| 7 | Uscita regolatore → SSC-32 VS2 | coppia rosso/nero | 80-150 mm | 16 AWG | puntalini 1,5 mm² | 1 |
| 7b | Condensatore 2200 µF 16 V su ciascun morsetto VS (scelta di `alimentazione.md`) | reofori del componente | il più corto possibile | – | saldato sulla coppia 16 AWG a ridosso del morsetto, oppure nello stesso puntalino doppio; non due conduttori sciolti sotto la stessa vite | 2 |
| 8 | Nodo → SSC-32 VL (logica) | coppia rosso/nero | 80-150 mm | 22 AWG | puntalini 0,34 mm² | 1 |
| 9 | Nodo → regolatore 5 V → ESP32-S3 (pin 5V e GND) | coppia rosso/nero | 60-120 mm + 60-120 mm | 22 AWG | saldato / Dupont 2,54 mm femmina | 1 |
| 10 | Seriale ESP32-S3 ↔ SSC-32 (TX, RX, GND) | 3 fili | 80-150 mm | 26-28 AWG | Dupont 2,54 mm femmina-femmina | 1 |
| 11 | Misura tensione batteria → ADC (partitore) | 2 fili | 80-150 mm | 26-28 AWG | saldato / Dupont | 1 |
| 12 | Presa di bilanciamento JST-XH 3 poli → cicalino LiPo | cavetto della batteria | – | – | innesto diretto | 1 |
| 13 | Servo coxa → SSC-32 | cavo originale del servo | 250 mm nominali | originale | JR femmina sui pin della scheda | 6 |
| 14 | Servo femore → SSC-32 | cavo originale; + prolunga 100-150 mm sulle 4 zampe d'angolo se il percorso CAD supera 220 mm | 250-400 mm | originale + 22 AWG | JR; prolunga maschio-femmina con clip | 6 (+4 prolunghe) |
| 15 | Servo tibia → SSC-32 | cavo originale + prolunga 150 mm | 400 mm | originale + 22 AWG | JR; prolunga maschio-femmina con clip | 6 (+6 prolunghe) |

**Lista della spesa per il solo cablaggio** (Amazon.it, prezzi dell'8 ottobre 2026)

| Articolo | Q.tà | Prezzo | Link |
|---|---|---|---|
| T-plug maschio/femmina con codini 14 AWG 100 mm (3 coppie) | 1 conf. | 8,99 € | [B0FVRHF7GW](https://www.amazon.it/dp/B0FVRHF7GW) |
| Cavo silicone 14 AWG 2,5 m + 2,5 m | 1 | 13,99 € | [B0C53D343Y](https://www.amazon.it/dp/B0C53D343Y) |
| Cavo silicone 16 AWG 2,5 m + 2,5 m | 1 | 11,99 € | [B0D9VDPG54](https://www.amazon.it/dp/B0D9VDPG54) |
| Prolunghe servo 15 cm, 22 AWG, maschio-femmina (20 pezzi) | 1 conf. | 10,99 € | [B087289HFS](https://www.amazon.it/dp/B087289HFS) |
| Prolunghe servo 10 cm (20 pezzi), facoltative | 1 conf. | 9,99 € | [B08727NKP2](https://www.amazon.it/dp/B08727NKP2) |
| Clip di blocco per prolunghe servo (40 pezzi) | 1 conf. | 10,99 € | [B0C61PDHDF](https://www.amazon.it/dp/B0C61PDHDF) |
| Kit puntalini 0,25-10 mm² con pinza | 1 | 15,99 € | [B0FPDZ8SGR](https://www.amazon.it/dp/B0FPDZ8SGR) |
| Guaina a spirale Ø 6 mm, 15 m | 1 | 10,99 € | [B07WDRYFXV](https://www.amazon.it/dp/B07WDRYFXV) |

- Totale indicativo: 83,93 € senza le prolunghe da 10 cm, 93,92 € con [computed: somma dei prezzi in tabella]. Cavo 22 AWG, cavetti Dupont, termorestringente e fascette non sono stati cercati (materiale generico).
- Consumo stimato di cavo: 14 AWG rosso circa 0,3-0,4 m e nero circa 0,2-0,3 m; 16 AWG 4 × 0,15 = 0,6 m [computed]. Le confezioni da 2,5 m + 2,5 m bastano con ampio margine.
- Assegnazione dei canali suggerita: tre zampe di un lato sui canali 0-15 (VS1), le tre dell'altro lato su 16-31 (VS2), con il lato corrispondente della scheda rivolto verso quelle zampe: 9 servo per morsetto e cavetti senza incroci.
- Ponticelli VS1 = VS2: con UN solo regolatore che alimenta entrambi i morsetti con due coppie di fili i ponticelli possono restare (stesso potenziale); con DUE regolatori separati (uno per lato) vanno tolti, altrimenti le due uscite risultano in parallelo [inferenza dalla guida SSC-32U: con i ponticelli inseriti si alimenta "EITHER VS1 or VS2, but not both"].
- Ordine di montaggio consigliato: cablare e provare l'alimentazione senza servo (misurare 6,0 V su VS1 e VS2), poi collegare i servo una zampa alla volta.

### Gaps
- La lista dipende dalla variante reale della scheda ("SSC-32 V2.5", probabile clone della SSC-32U secondo `ssc32.md`): posizione e tipo dei morsetti e tensione ammessa su VL non sono noti.
- Lunghezze interne non verificabili senza il CAD del corpo e la posizione della batteria.
- Livelli logici della seriale (TX a 5 V dell'SSC-32 verso l'ESP32-S3 a 3,3 V): trattati in `ssc32.md`, qui non verificati.
- Disponibilità: tutti gli articoli Amazon.it erano a catalogo l'8 ottobre 2026; scorte e prezzi cambiano e le inserzioni di marchi generici vengono sostituite spesso.

#### Cose che solo l'utente può verificare
1. Misurare col calibro il pacco reale: lunghezza, larghezza e altezza nel punto più spesso; lunghezza dei cavi di potenza e del cavetto di bilanciamento; lato e posizione di uscita dei cavi; peso sulla bilancia.
2. Fotografare il T-plug della batteria per confermare il genere (attesa: femmina, come nelle immagini del produttore) e leggere la sezione stampata sui cavi (attesa: 12 AWG); fotografare la testata da cui escono i cavi e quotare la posizione dell'intaglio.
3. Confermare l'ASIN o il link esatto della batteria acquistata (B098P5ZBJ6?) e che sia la versione 50C e non la "100C" da 131 × 42 × 20 mm.
4. Misurare la lunghezza del cavo di almeno 3 dei 18 MG90S (250 mm o 175 mm?) e il diametro di un singolo filo.
5. Misurare sulla scheda SSC-32: apertura dei morsetti a vite (entra un puntalino da 1,5 mm²? da 2,5 mm²?), passo dei morsetti, altezza libera sopra i pin dei servo.
6. Misurare una spina JR dei propri servo (larghezza, spessore, lunghezza) e provarne 3 affiancate sui pin della scheda.
7. Misurare la lunghezza della coppia spina + collare di una prolunga accoppiata e chiusa con la clip.
