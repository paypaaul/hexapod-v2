# Giunti rigidi senza gioco per micro servo MG90S, viteria nelle parti stampate, materiali e stampante FlashForge Creator 5

Data ricerca: 8 ottobre 2026. Tre passate: primo tentativo interrotto (circa 50 chiamate web), prima ripresa (16 chiamate), seconda ripresa di verifica e completamento (16 ricerche/letture web piu' la consultazione delle immagini di montaggio del repository VEB4697). I risultati aggiunti nella seconda ripresa sono marcati **(2a ripresa)**.

Etichette fonte: **[primary]** = produttore (datasheet / catalogo / manuale / pagina prodotto del produttore), **[secondary]** = negozio, blog, wiki, repository di un progetto, **[3rd-meas]** = misura o prova di terzi, **[community]** = forum/opinione, **[computed]** = calcolo mio (formula indicata).

Note di metodo:
- Letti integralmente come PDF (testo visto riga per riga, non riassunto): catalogo cuscinetti miniatura ospitato dal distributore Albeco (16 pagine), schede tecniche Bambu PLA Basic V2.0, PLA-CF V2.0, PETG HF V1.0, PETG-CF V2.0, PET-CF V1.0, articolo sul creep di Dogan (SV-JME 2022, 10 pagine). I numeri presi da questi documenti sono affidabili.
- (2a ripresa) Ho riestratto in locale il testo dei PDF salvati (catalogo cuscinetti, Bambu PLA-CF, PETG-CF, PET-CF) e ricontrollato riga per riga i valori riportati qui sotto: coincidono. Nel testo del catalogo cuscinetti il nome del produttore NON compare: la prima ripresa lo attribuiva a "FBJ", attribuzione che non ho potuto verificare; qui lo cito come "catalogo Albeco". Ho letto allo stesso modo (testo estratto) il PDF "Flashforge Filament guides".
- (2a ripresa) Le immagini di montaggio del repository VEB4697 sono state guardate direttamente: cio' che ne riporto e' una mia osservazione delle immagini, non testo della fonte.
- Tutte le altre pagine sono state lette tramite uno strumento che restituisce un riassunto fatto da un modello piccolo. Dove un numero critico NON e' stato visto citato testualmente lo segnalo con **(da riverificare sulla fonte)**.
- Amazon.it, AliExpress, RobotShop EU, kugellager-express.de, MakerWorld hanno risposto 403 o con verifica anti-bot: prezzi e disponibilita' su quei siti NON sono verificati.
- Le quote del servo usate nei calcoli (cassa 22.6 x 12.2 x 22.55 mm, interasse fori alette 27.5 mm, foro aletta Ø 2.5 mm, asse albero a 5.375 mm dal centro cassa, cima millerighe a 32.25 mm dal fondo) vengono dal modello STEP dell'utente, non da una fonte esterna.
- Su millerighe, squadrette metalliche e viti delle alette esiste gia' il file `servo_mg90s.md` (sezioni 4, 5, 6): qui riporto solo cio' che serve al progetto del giunto e i dati nuovi.

---

## 1. Come costruiscono i giunti i piccoli esapodi/quadrupedi con servo classe 9 g (doppio appoggio, perno posteriore coassiale)

### Takeaway
Nessun progetto trovato sfrutta un rilievo del servo: il perno posteriore coassiale e' sempre ricavato nel pezzo che avvolge il servo. Tre schemi documentati: (a) guscio stampato in due meta' serrato da viti M2 passanti, con perno in acciaio inox M4 x 6 mm, da solo (SmallpTsai, MG92B) o dentro un cuscinetto MR74-2RS 4x7x2.5 (VEB4697); (b) emisfero stampato sul portaservo che fa da perno a scatto per una cerniera a U (Vorpal, servo MG90); (c) cerniera commerciale Lynxmotion PSH-02 per micro servo (dettagli non verificati). Un progetto di riferimento con MG90S e cuscinetto con foro da 3 mm NON e' stato trovato. (2a ripresa) Le immagini di montaggio di VEB4697 confermano lo schema (a): il cuscinetto sta in una sede tonda nel fondo del guscio portaservo, sotto l'albero di uscita, e il perno e' portato dalla piastra inferiore della staffa mobile.

### Cited Findings
Schema (a): guscio a sandwich + perno metallico
- SmallpTsai "hexapod-v2-7697" (18x TowerPro MG92B, stessa famiglia dimensionale dell'MG90S): distinta con 18 x perni in acciaio inox (304) M4 x 6 mm, uno per servo; viti M2x6 x54 (18 per le squadrette dei servo, 24 per i giunti, 12 per le cosce), M2x10 x24 (6 per le cosce, 18 per il bloccaggio dei perni, "pin locks"), M2x30 x36 (2 per servo), dadi M2 x36 (2 per servo); nessun cuscinetto — [secondary] [BOM.md](https://raw.githubusercontent.com/SmallpTsai/hexapod-v2-7697/master/mechanism/BOM.md) (quantita' dal riassunto: da riverificare sulla fonte prima di ordinare)
- Montaggio: "Combine `thigh_top`, `MG92B` and `thigh_bottom`, use M2x30mm screw and nut to secure them together"; "First put 2 x `MG92B`, `leg_top` and `leg_bottom` together with M2x30mm screw and nut" — [secondary] [LEG.md](https://raw.githubusercontent.com/SmallpTsai/hexapod-v2-7697/master/mechanism/LEG.md)
- Parti stampate: joint_top, joint_bottom, joint_cross, thigh_top/bottom, leg_top/bottom, foot_*; corpo in PLA stampato su Prusa i3 MK2S — [secondary] [repo](https://github.com/SmallpTsai/hexapod-v2-7697), [cartella mechanism](https://github.com/SmallpTsai/hexapod-v2-7697/tree/master/mechanism)
- VEB4697 "hexapod-MG90S" (derivato dal precedente): M2 6 mm x36, M2 10 mm x198, dadi M2 x234, "Pin (304) M4 6mm" x18, cuscinetto "MR74-2RS (4mm ID, 7mm OD, 2.5mm Bore)" x18 — [secondary] [github.com/VEB4697/hexapod-MG90S](https://github.com/VEB4697/hexapod-MG90S)
- Stesso autore: "It is strongly recommended to start with Hexapod v2 rather than building Hexapod v1." / "MG90S servos used in Hexapod v1 frequently fail due to their inherent weaknesses and inconsistencies in quality." La v2 usa servo da 21 g ("DS Power or Miuzei 21G servo"). Stampa: "Use the orientations of the thumbnials to print, no support is needed." — [secondary/community] [github.com/VEB4697/hexapod-MG90S](https://github.com/VEB4697/hexapod-MG90S)
- (2a ripresa) OSSERVAZIONE MIA sulle immagini di montaggio VEB4697 (ramo v2, servo da 21 g; non e' testo della fonte, nessuna quota leggibile):
  - Guscio portaservo ([assembly_leg.gif](https://github.com/VEB4697/hexapod-MG90S/raw/v2/images/assembly_leg.gif), [leg_bottom.jpg](https://github.com/VEB4697/hexapod-MG90S/raw/v2/images/leg_bottom.jpg), [leg_top.jpg](https://github.com/VEB4697/hexapod-MG90S/raw/v2/images/leg_top.jpg)): quattro pezzi piatti. `leg_top` e' un telaio con due finestre rettangolari da cui sporgono le teste dei due servo; `leg_bottom` e' un vassoio con un incavo che riceve il fondo dei servo e due fori tondi, uno sotto ciascun albero di uscita; due `leg_side` chiudono i fianchi e hanno tasche per dadi. Sei viti dall'alto e sei dal basso entrano nei dadi dei fianchi. Due anelli (i cuscinetti MR74 della distinta) si infilano dal basso nei fori tondi di `leg_bottom`. Non si vedono viti nelle alette dei servo: il servo e' tenuto dal sandwich.
  - Staffa mobile ([assembly_joint.gif](https://github.com/VEB4697/hexapod-MG90S/raw/v2/images/assembly_joint.gif), [joint_cross.jpg](https://github.com/VEB4697/hexapod-MG90S/raw/v2/images/joint_cross.jpg), [joint_bottom.jpg](https://github.com/VEB4697/hexapod-MG90S/raw/v2/images/joint_bottom.jpg)): un disco a croce (`joint_cross`) con quattro asole e tasche per dadi riceve a incastro quattro piastre, bloccate da viti lunghe e dadi. Due piastre (`joint_top`) portano il disco-squadretta del servo fissato con due viti; le altre due (`joint_bottom`) portano ciascuna un perno cilindrico (i "Pin (304) M4 6mm" della distinta) vicino all'estremita'. Ogni asse ha quindi squadretta sopra e perno-in-cuscinetto sotto, e i due assi del giunto sono a 90° tra loro.
- (2a ripresa) "Mini Quadruped - optimized for 9G servos" (Printables): la distinta comprende otto spalle e otto piccoli "servo buttons" stampati; ogni bottone va nel foro della spalla opposto alla squadretta e fa da appoggio (cuscinetto a strisciamento) per il retro del servo; sono inclusi i sorgenti OpenSCAD per ritoccare i giochi — [secondary, visto SOLO come riassunto di ricerca: la pagina risponde 403] [printables.com/model/211466](https://www.printables.com/model/211466-mini-quadruped-optimized-for-9g-servos)
- (2a ripresa) I robot Spot Micro con servo taglia standard (MG996R) usano cuscinetti flangiati piu' grandi (F625ZZ, F688ZZ 8x16x5): non trasferibili alla taglia 9 g — [secondary, riassunto di ricerca] [github.com/OttPeterR/SpotMicro](https://github.com/OttPeterR/SpotMicro), [github.com/MKme/quadrupedal-robot](https://github.com/MKme/quadrupedal-robot)

Schema (b): emisfero stampato a scatto (Vorpal, servo "Vorpal MG90")
- Il servo dell'anca si preme nel portaservo "until it clicks in under the small tab on one side of the servo holder"; "the sides of the servo compartments need to bend outward while the servos are inserted"; nessuna vite sul corpo servo — [primary del progetto] [Vorpal Assembly Instructions](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Assembly_Instructions)
- Sul lato opposto all'albero ci sono "the hemispheres jutting out of one side of each of the servo holders", che fanno da cuscinetto: la cerniera della zampa si aggancia "over the hemispherical bearing on the other side"; ogni cerniera e' fatta di "two identical U-shaped parts" che, infilate sul servo, "will lock together tightly" — [primary del progetto] [Vorpal Assembly Instructions](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Assembly_Instructions)
- Avvertenze Vorpal sull'attrito: gli emisferi "need to be as low friction as possible"; "If you find you are struggling, that means the hinges are too tight. This may affect walking."; "A tiny bit of silicone lubricant will usually fix that problem" — [primary del progetto] [Vorpal Assembly Instructions](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Assembly_Instructions)

Schema (c): cerniera commerciale
- Esiste il prodotto "Lynxmotion Injection Molded Servo Hinge Two Pack - Micro PSH-02", a catalogo RobotShop EU; un riassunto di ricerca riporta diametro albero 1/8" — [secondary, visto SOLO come titolo/riassunto di ricerca: la pagina risponde con verifica anti-bot] [eu.robotshop.com](https://eu.robotshop.com/products/injection-molded-servo-hinge-psh-02)

Altri progetti consultati (senza dettagli utili sul giunto):
- ZeroBug (CoretechR): 18 servo "EMAX ES08A II", "Anything apart from the electronics and servos is 3D printed"; la pagina non descrive giunti, viti, perni o cuscinetti — [secondary] [hackaday.io/project/180534](https://hackaday.io/project/180534-zerobug-diy-hexapod-robot), [github.com/CoretechR/ZeroBug](https://github.com/CoretechR/ZeroBug)
- Esapode stampato su Hackster: boccole stampate ai giunti al posto dei cuscinetti; consiglio di costruire prima una sola gamba per trovare il gioco giusto (lasco = vibra, stretto = la gamba non si muove) — [secondary, visto solo come riassunto di ricerca] [hackster.io](https://www.hackster.io/sir-kuhnhero/3d-printed-hexapod-05a60c)
- Robot camminatore su Hackaday (servo taglia standard): sei pezzi stampati avvolgono il servo e "The design also requires a bearing at the top to spread the weight and stress to both sides of the joint." — [secondary, visto solo come riassunto di ricerca; attribuzione dell'URL non verificata] [hackaday.io/project/158800](https://hackaday.io/project/158800)
- Una cerniera stampata con boccole al posto dei cuscinetti: in PETG, ripassata con punta da 3 mm e un po' d'olio, "it kind of works, though it's not as efficient as ball bearings" — [community, visto solo come riassunto di ricerca] [printables.com/model/812379](https://www.printables.com/model/812379-hinged-parallelogram-for-gyroman-4)

### Calcoli
- Distanza dell'asse dell'albero dalla faccia corta piu' vicina della cassa (lato cavo) = 22.6 / 2 − 5.375 = 5.925 mm; dalla faccia opposta = 22.6 / 2 + 5.375 = 16.675 mm; dalle facce lunghe = 12.2 / 2 = 6.1 mm — [computed] da quote STEP dell'utente
- Un cuscinetto posto sotto il fondo del servo e coassiale all'albero resta dentro l'impronta della cassa se il raggio esterno e' minore di 5.925 mm: OD 7 mm (raggio 3.5, margine 2.4 mm) e OD 8 mm (raggio 4, margine 1.9 mm) ci stanno; OD 10 mm (raggio 5) lascia 0.9 mm; la flangia Ø 11.5 mm dell'F623ZZ (raggio 5.75) lascia 0.175 mm — [computed] da quote STEP e dimensioni del catalogo Albeco (sezione 2)

### Inferences
- Schema ricorrente (dedotto dalle distinte e, nella 2a ripresa, visto nelle immagini VEB4697; non descritto a parole dalle fonti): guscio che cattura il corpo servo tra un pezzo superiore e uno inferiore; nel pezzo inferiore, sotto il fondo servo, una sede tonda coassiale con l'albero che riceve il cuscinetto; la staffa a U della parte mobile porta da un lato la squadretta e dall'altro un perno corto che entra nel cuscinetto. Nel progetto SmallpTsai (senza cuscinetti) le 18 viti M2x10 "pin locks" indicano che il perno e' bloccato da una vite.
- Conseguenza per il CAD dell'MG90S: il cuscinetto va nel guscio fisso (anello esterno forzato nella plastica, che cosi' lavora su una superficie grande) e il perno nella staffa mobile; non il contrario. Il fondo del guscio deve essere abbastanza spesso da contenere la larghezza del cuscinetto (3 mm per 683ZZ / MR83ZZ) piu' una battuta.
- Per l'MG90S il perno coassiale va quindi creato nella culla stampata, sotto il fondo cassa, a 5.925 mm dalla faccia corta lato cavo. I cuscinetti con foro 3 mm e OD 7-8 mm sono quelli che restano dentro l'impronta della cassa.
- L'emisfero stampato di Vorpal e' la soluzione a costo zero ma e' un cuscinetto a strisciamento plastica su plastica: l'attrito consuma coppia a un servo che ne ha poca e il gioco dipende dalla qualita' di stampa. Per un giunto "senza gioco" lo schema (a) con cuscinetto a sfere e' la scelta coerente.

### Gaps
- Quote della sede perno/cuscinetto nei due progetti GitHub (diametro foro, interferenza, spessori): NON TROVATO; la disposizione e' stata vista nelle immagini (2a ripresa) ma le quote stanno solo nelle STL, che non ho scaricato.
- Le immagini guardate sono del ramo v2 di VEB4697 (servo da 21 g): la versione v1 per MG90S non e' stata vista.
- Progetto di riferimento con MG90S + cuscinetto serie MR63 / 683 / MR83 / 693 / 623: NON TROVATO (quattro ricerche mirate, esito negativo).
- Lynxmotion PSH-02: quote, modo di fissaggio al servo, prezzo e giacenza: NON VERIFICATO (pagina bloccata).

---

## 2. Cuscinetti candidati, carichi, prezzi, accoppiamenti in stampa FDM, cosa usare come asse

### Takeaway
Tutti i candidati con foro 3 mm hanno un carico statico (74-216 N) molto superiore a quello che un esapode da circa 1 kg scarica su un giunto: la scelta si fa per ingombro. I piu' adatti sono 683ZZ / F683ZZ (3x7x3) e MR83ZZ (3x8x3) o 693ZZ / F693ZZ (3x8x4). Come asse, una vite M3 ha gioco nel foro del cuscinetto (fino a 0.126 mm sul diametro): per un giunto senza gioco serve una spina cilindrica da 3 mm oppure bisogna serrare assialmente l'anello interno. (2a ripresa) Il foro di un cuscinetto classe P0 e' 2.992-3.000 mm: una spina m6 vi entra sempre forzata (0.002-0.016 mm), una spina h6 ha al massimo 0.006 mm di gioco; la larghezza del cuscinetto puo' essere fino a 0.12 mm sotto il nominale.

### Cited Findings
Catalogo "Miniature Ball Bearings" ospitato dal distributore Albeco (pagine di catalogo 46-61, lette integralmente; righe ricontrollate nella 2a ripresa), versioni a doppio schermo ZZ — [catalogo di cuscinetti: il nome del produttore non compare nel testo del PDF, quindi lo etichetto secondary; quote d x D x B coerenti con le sigle standard] [miniaturowe.pdf](https://old.albeco.com.pl/data/catalogueb/miniaturowe.pdf):

| Sigla | d x D x B (mm) | Cr dinamico (N) | C0r statico (N) | Peso (g) |
|---|---|---|---|---|
| MR63ZZ | 3 x 6 x 2.5 | 206 | 74 | 0.28 |
| 683ZZ | 3 x 7 x 3.0 | 314 | 108 | 0.45 |
| MR83ZZ | 3 x 8 x 3.0 | 392 | 137 | 0.67 |
| 693ZZ | 3 x 8 x 4.0 | 559 | 177 | 0.80 |
| MR93ZZ | 3 x 9 x 4.0 | 569 | 186 | 1.15 |
| 623ZZ | 3 x 10 x 4 | 628 | 216 | 1.65 |
| MR74ZZ | 4 x 7 x 2.5 | 255 | 108 | 0.33 |
| MR84ZZ | 4 x 8 x 3.0 | 392 | 137 | 0.56 |
| MR85ZZ | 5 x 8 x 2.5 | 216 | 88 | 0.34 |
| MR105ZZ | 5 x 10 x 4.0 | 432 | 167 | 1.26 |

Versioni flangiate a doppio schermo (stesso catalogo; colonne "Flange Dia. D1" e "Flange Width t1"):

| Sigla | d x D x B (mm) | Flangia Ø D1 x spessore t1 (mm) | Cr (N) | C0r (N) | Peso (g) |
|---|---|---|---|---|---|
| MF63ZZ | 3 x 6 x 2.5 | 7.2 x 0.6 | 206 | 74 | 0.34 |
| F683ZZ | 3 x 7 x 3.0 | 8.1 x 0.8 | 314 | 108 | 0.53 |
| F693ZZ | 3 x 8 x 4.0 | 9.5 x 0.9 | 559 | 177 | 0.94 |
| F623ZZ | 3 x 10 x 4 | 11.5 x 1.0 | 628 | 216 | 1.85 |
| MF74ZZ | 4 x 7 x 2.5 | 8.2 x 0.6 | 255 | 108 | 0.40 |
| MF84ZZ | 4 x 8 x 3.0 | 9.2 x 0.6 | 392 | 137 | 0.64 |
| MF85ZZ | 5 x 8 x 2.5 | 9.2 x 0.6 | 216 | 88 | 0.42 |
| MF105ZZ | 5 x 10 x 4.0 | 11.6 x 0.8 | 432 | 167 | 1.38 |

- MF83ZZ (3x8x3 flangiato schermato) NON compare nella tabella "MF Series Flanged, Double Shielded" del catalogo Albeco; c'e' solo l'MF83 aperto (3 x 8 x 2.5, flangia 9.2 x 0.6, Cr 392 / C0r 137 N). Un'inserzione eBay.de usa pero' la sigla "MF83 ZZ" per un 3x8x3 flangiato: esiste presso altri produttori — [catalogo Albeco] [miniaturowe.pdf](https://old.albeco.com.pl/data/catalogueb/miniaturowe.pdf); [secondary, riassunto di ricerca] [ebay.de](https://www.ebay.de/itm/375637480610)
- Nota del catalogo: tenuta in gomma = "-2RS" al posto di "ZZ"; tutti disponibili anche in inox 440C — [catalogo Albeco] [miniaturowe.pdf](https://old.albeco.com.pl/data/catalogueb/miniaturowe.pdf)
- Attenzione alle versioni APERTE della stessa sigla, piu' strette: MR63 aperto 3x6x2.0, 683 aperto 3x7x2.0, MR83 aperto 3x8x2.5, 693 aperto 3x8x3.0 — [catalogo Albeco] [miniaturowe.pdf](https://old.albeco.com.pl/data/catalogueb/miniaturowe.pdf)

Prezzi e reperibilita' (tutti da riassunti di ricerca: da riverificare al momento dell'ordine):
- RS Italia, RS PRO SF683ZZ (inox, flangiato, schermato, 3x7x3): 9,61 € IVA esclusa (11,72 € IVA inclusa) al pezzo, disponibile — [secondary] [it.rs-online.com 2346936](https://it.rs-online.com/web/p/cuscinetti-a-sfera/2346936)
- eBay.de, 10 x 683ZZ 3x7x3 da venditore cinese: 4,84 US$ piu' circa 4,30 € di spedizione — [secondary] [ebay.de 254153213019](https://www.ebay.de/itm/254153213019)
- eBay.de, MR83ZZ 3x8x3 in confezioni da 10-30 pezzi: 12,26 US$ (quantita' a cui si riferisce il prezzo non chiara); un'altra inserzione da Hong Kong 10 pezzi a 8,66 US$ spedizione inclusa (URL non identificato con certezza) — [secondary] [ebay.de 375637480610](https://www.ebay.de/itm/375637480610)
- Negozio tedesco di cuscinetti con pagine per 683 ZZ 3x7x3 e MR83 ZZ 3x8x3 (prezzi non letti: 403) — [secondary] [kugellager-express 683 ZZ](https://www.kugellager-express.de/miniature-deep-groove-ball-bearing-683-zz-3x7x3-mm), [kugellager-express MR83 ZZ](https://www.kugellager-express.de/miniature-deep-groove-ball-bearing-mr83-zz-3x8x3-mm)
- Amazon.it e AliExpress: una ricerca mirata non ha restituito NESSUNA inserzione amazon.it per questi cuscinetti; le pagine dei due siti non sono leggibili dagli strumenti usati — esito negativo, non prova di indisponibilita'
- (2a ripresa) eBay.de, lotti da 10 x 683ZZ 3x7x3 spediti dalla Cina: circa 2,71 € + 8,52 € di spedizione; circa 4,16 € + 4,30 € (dazi inclusi); circa 5,99 € + 4,31 €; circa 13,72 € con spedizione gratuita. Con la spedizione fanno circa 0,85-1,37 € a cuscinetto. Singolo 683.ZZ marca KBS da venditore tedesco: 4,96 € IVA inclusa + 3,90 € — [secondary, riassunto di ricerca; inserzioni aggiornate tra maggio e settembre 2025, prezzi in euro convertiti da dollari: da riverificare] [ebay.de 231172835498](https://www.ebay.de/itm/231172835498), [ebay.de 254153213019](https://www.ebay.de/itm/254153213019), [ebay.de 375520041032](https://www.ebay.de/itm/375520041032), [ebay.de KBS](https://www.ebay.de/p/28006849156)
- (2a ripresa) eBay.de, 20 x F683ZZ flangiati 3x7x3 in acciaio al cromo: circa 15,11 € (17,70 US$), spedizione indicata gratuita, cioe' circa 0,76 € al pezzo — [secondary, riassunto di ricerca; da riverificare] [ebay.de 157288484750](https://www.ebay.de/itm/157288484750)
- (2a ripresa) RS Italia vende anche l'RS PRO S683ZHH (3x7x3) a 11,97 € IVA esclusa (14,60 € IVA inclusa) al pezzo; consegna gratuita da 60 € — [secondary, riassunto di ricerca] [it.rs-online.com 2346984](https://it.rs-online.com/web/p/cuscinetti-a-sfera/2346984)

Accoppiamenti in stampa FDM:
- Gioco di progetto per lato con ugello 0.4 mm e flusso tarato: forzato 0.05-0.15 mm; scorrevole 0.2-0.3 mm (PLA 0.15-0.25, PETG 0.2-0.3); parti mobili stampate assemblate circa 0.3-0.4 mm in totale; i fori interni "tend to print slightly undersized"; tolleranza pratica di una macchina tarata circa ±0.2-0.5 mm; "Don't shave the pin; enlarge the hole" — [secondary] [Sovol](https://www.sovol3d.com/blogs/news/fdm-3d-printing-tolerances-clearances-how-to-design-parts-that-fit)
- Per un accoppiamento forzato su stampanti Ultimaker si parte da circa 0.2 mm; un valore di 0.1 mm per lato aggiunge 0.2 mm al diametro del foro; a gioco zero in FDM il pezzo spesso non entra — [secondary, riassunto di ricerca] [wiki CCI](https://wiki.cci.arts.ac.uk/books/digital-fabrication-lab/page/design-the-clearance-and-tolerance)
- Misura CNC Kitchen su fori da circa 4 mm stampati in PLA: i fori escono circa 0.25 mm piu' piccoli del CAD — [3rd-meas] [cnckitchen.com](https://cnckitchen.com/blog/are-our-heat-set-insert-datasheets-wrong)
- Chi ha rifatto in FDM i pezzi di un robot progettato per altra tecnologia: "we needed to add .3mm to all pockets and holes" — [community, visto solo come titolo di risultato] [circuitlaunch](https://circuitlaunch.notion.site/Tolerance-and-Modifications-2235fea8525c452ba48ba4e825f2f36c)

Tolleranze dei cuscinetti (2a ripresa):
- Classe P0 (normale), tabelle in millesimi di millimetro: anello interno con foro "over 2.5mm to 10mm": scostamento medio del foro +0 / −8, scostamento della larghezza +0 / −120; anello esterno con diametro "over 6mm up to 18mm": scostamento medio +0 / −8. Per confronto P6: 0 / −7; P5: 0 / −5 (larghezza P5: 0 / −40) — [secondary: tabelle di tolleranza riprodotte da un distributore di cuscinetti; l'abbinamento della colonna "larghezza" e' stato fatto per posizione dallo strumento di lettura: da riverificare] [smbbearings.com tolerance tables](https://www.smbbearings.com/technical/bearing-tolerance-tables.html)
- ABEC 1 corrisponde alla classe ISO normale (P0); per ABEC 1 il foro e' +.0000 / −.0003 pollici (circa 0 / −7.6 µm), coerente con 0 / −8 µm — [secondary, riassunto di ricerca] [engineersedge.com](https://engineersedge.com/bearing/ball_bearings_tolerances.htm), [nhbb.com](https://www.nhbb.com/knowledge-center/engineering-reference/miniature-instrument-bearings/coding-classification)

Asse:
- (2a ripresa) ISO 286, alberi con diametro nominale oltre 1 fino a 3 mm: m6 = +0.002 / +0.008 mm; h6 = 0 / −0.006 mm; h8 = 0 / −0.014 mm — [secondary, visto come riassunto di ricerca di tabelle commerciali ISO 286, non sul testo della norma] [ganternorm ISO 286](https://ganternorm.com/fileadmin/user_upload/downloads/technischer%20anhang/286_1.pdf), [simplybearings ISO limits](https://simplybearings.co.uk/shop/Info-Pages-ISO-Limits/c4746_4779/index.html)
- (2a ripresa) Spine cilindriche temprate e rettificate DIN 6325 (norma ritirata, equivalente circa a ISO 8734), tolleranza m6, 60 HRC: la misura 3 x 10 e' a catalogo da Ludwig Meister (Germania) e Bossard; la stessa spina in tolleranza h6 e' a catalogo SFS (Svizzera) — [secondary, riassunto di ricerca; prezzi, quantita' minime e spedizione in Italia NON verificati] [ludwigmeister.de 3x10](https://www.ludwigmeister.de/artikel/zylinderstifte/185618/din-6325-zylinderstifte/501din6325-3x10-2390684), [bossard.com](https://www.bossard.com/eshop/ch-de/spine/spine-cilindriche/spine-cilindriche-temprate-rettificate/p/857), [sfs.ch h6](https://www.sfs.ch/CH/en/dl/p/149079)
- Vite M3x0.5 classe 6g: diametro esterno del filetto 2.980 mm max, 2.874 mm min — [secondary: tabella ISO 965 riprodotta] [Wikipedia ISO 965](https://en.wikipedia.org/wiki/ISO_965), [amesweb](https://amesweb.info/Screws/metric-thread-chart.aspx)
- Spine cilindriche ISO 2338 m6: tolleranza +0.002 / +0.008 mm (vista sulle righe da 1.5 e 2.5 mm; la riga da 3 mm non e' stata trovata); una spina da 3 mm "ISO 2338B h8" ha invece −0.014 / 0 mm — [secondary, riassunto di ricerca] [McMaster ISO 2338 m6](https://www.mcmaster.com/products/dowel-pins/specifications-met~iso-2338-m6/), [Zoro](https://www.zoro.com/i/G1914744/)
- Viti a spallamento con filetto M2 e spallamento Ø 3 mm esistono presso Accu come articolo su ordinazione ("M2 (3mm) x 71mm ... MTO ... Shoulder Screws") — [secondary, visto solo come titolo di risultato; prezzo e tempi non verificati] [accu-components.com](https://accu-components.com/de/massgefertigte-metrische-schulterschrauben-mit-buchse/871096-STR6023LM2-71-00)
- I due progetti di riferimento usano un perno inox 304 M4 x 6 mm (con MR74, foro 4 mm, in VEB4697) — [secondary] [github.com/VEB4697/hexapod-MG90S](https://github.com/VEB4697/hexapod-MG90S)

### Calcoli
- Foro reale di un cuscinetto P0 con foro nominale 3 mm: 3.000 − 0.008 = 2.992 mm (minimo), 3.000 mm (massimo) — [computed] da [smbbearings.com](https://www.smbbearings.com/technical/bearing-tolerance-tables.html)
- Gioco diametrale di una vite M3 6g in quel foro: 2.992 − 2.980 = 0.012 mm (minimo), 3.000 − 2.874 = 0.126 mm (massimo) — [computed] da [Wikipedia ISO 965](https://en.wikipedia.org/wiki/ISO_965) e tolleranza P0. (La prima ripresa indicava 0.020 mm di minimo perche' usava il foro nominale.)
- (2a ripresa) Spina 3 mm m6 (3.002-3.008 mm) nel foro P0: interferenza da 3.002 − 3.000 = 0.002 mm a 3.008 − 2.992 = 0.016 mm: sempre forzata — [computed]
- (2a ripresa) Spina 3 mm h6 (2.994-3.000 mm) nel foro P0: da 0.008 mm di interferenza (spina 3.000, foro 2.992) a 0.006 mm di gioco (spina 2.994, foro 3.000) — [computed]
- (2a ripresa) Spina 3 mm h8 (2.986-3.000 mm) nel foro P0: da 0.008 mm di interferenza a 3.000 − 2.986 = 0.014 mm di gioco — [computed]
- (2a ripresa) Larghezza reale di un cuscinetto P0 con B nominale 3 mm: da 3.000 − 0.120 = 2.880 mm a 3.000 mm; per B = 4 mm da 3.880 a 4.000 mm — [computed]. La battuta assiale non va quindi dimensionata sulla larghezza nominale.
- (2a ripresa) Diametro esterno reale: 683ZZ da 6.992 a 7.000 mm; MR83ZZ / 693ZZ da 7.992 a 8.000 mm — [computed]. La dispersione del cuscinetto (0.008 mm) e' trascurabile rispetto a quella del foro stampato (circa 0.25 mm): la sede si tara sulla stampante, non sul cuscinetto.
- Effetto sul piede se quel gioco resta libero: i due appoggi del giunto (piano squadretta e cuscinetto posteriore) distano circa 35 mm (32.25 mm dalla cima del millerighe al fondo cassa, piu' il fondo della culla: ipotesi mia). Inclinazione = 0.126 / 35 = 0.0036 rad = 0.21°; su un segmento di zampa lungo 100 mm = 0.36 mm al piede — [computed], con interasse appoggi e lunghezza zampa ipotizzati
- Carico sul giunto: massa stimata del robot 0.85-1.0 kg (da `dimensionamento.md`); peso W = 1.0 x 9.81 = 9.8 N; zampa media del tripode W/2 = 4.9 N. Rapporto con il C0r del cuscinetto piu' piccolo: 74 / 4.9 = 15 — [computed] con C0r dal catalogo Albeco. Anche con un fattore d'urto 3 il margine resta 5.
- Sede cuscinetto in CAD: se i fori escono 0.25 mm piu' piccoli (misura CNC Kitchen) un foro disegnato a D + 0.20 mm esce a circa D − 0.05 mm, cioe' leggermente forzato. Punto di partenza: 7.20 mm per 683ZZ, 8.20 mm per MR83ZZ / 693ZZ, 6.20 mm per MR63ZZ — [computed] da [cnckitchen.com](https://cnckitchen.com/blog/are-our-heat-set-insert-datasheets-wrong); da confermare con un provino sulla stampante dell'utente

### Inferences
- Cuscinetto consigliato per il perno posteriore dell'MG90S: F683ZZ (3x7x3 flangiato) se si vuole che la flangia faccia da battuta assiale nel pezzo stampato, altrimenti MR83ZZ (3x8x3) che ha piu' margine di carico e la stessa larghezza. 623ZZ e' inutilmente grande: esce quasi dall'impronta della cassa (vedi calcolo in sezione 1).
- Con vite M3 come asse il gioco radiale sparisce solo se l'anello interno viene serrato assialmente tra una battuta (rondella o colletto stampato) e la testa della vite: l'anello resta bloccato per attrito dove si trova al serraggio e l'errore diventa un disassamento fisso (al massimo 0.063 mm di raggio), non un gioco. In alternativa una spina cilindrica rettificata da 3 mm: in tolleranza m6 entra nel foro del cuscinetto sempre forzata (0.002-0.016 mm di interferenza: va pressata appoggiando l'anello interno, non a mano) e non ha gioco; in tolleranza h6 e' quasi sempre montabile a mano con al massimo 0.006 mm di gioco, cioe' 20 volte meno della vite M3 nel caso peggiore. La spina va poi bloccata nella plastica della staffa (foro stretto piu' una vite di fermo, come le "pin locks" di SmallpTsai, oppure colla).
- Poiche' la larghezza del cuscinetto puo' essere fino a 0.12 mm sotto il nominale, il fermo assiale conviene farlo con la flangia (F683ZZ) o con un coperchietto avvitato, non con una sede profonda esattamente 3.00 mm.
- L'inserzione piu' economica (eBay/AliExpress, cuscinetti cinesi senza marca) va bene per questo uso: carichi e velocita' sono minimi. RS a 11,72 € al pezzo e' sproporzionato per 18 giunti (18 x 11,72 = 211 €).

### Gaps
- Prezzo in confezione su Amazon.it e AliExpress al 8 ottobre 2026: NON TROVATO (pagine non raggiungibili).
- Gioco radiale interno dei cuscinetti (classe C0 / MC3): NON TROVATO; e' un gioco che resta comunque nel giunto, dell'ordine dei centesimi o meno (ordine di grandezza non verificato). La tolleranza del foro trovata nella 2a ripresa vale per la classe P0: i cuscinetti economici senza marca dichiarano spesso ABEC 1 o ABEC 3 ma nessuno lo garantisce.
- Tolleranze ISO 286 a 3 mm (m6, h6, h8): viste nella 2a ripresa solo come riassunto di ricerca di tabelle commerciali, non sul testo della norma ne' su una tabella letta direttamente.
- Negozio che vende spine 3 mm h6 / m6 in piccole quantita' con spedizione in Italia e prezzo: NON TROVATO (Ludwig Meister, Bossard e SFS sono fornitori industriali).
- Un valore di interferenza "consigliato" per sedi cuscinetto in FDM da fonte autorevole: NON TROVATO; esistono solo regole empiriche (0.05-0.2 mm) da provare.

---

## 3. Lato squadretta: squadrette in alluminio per il millerighe MG90S/SG90, cattura della squadretta di serie, gioco

### Takeaway
Non c'e' una squadretta in alluminio verificata per l'MG90S e le fonti non concordano nemmeno sul numero di denti (20, 21, 22 o 25 secondo la fonte); i lotti differiscono tra loro. La via a rischio minimo resta la squadretta di plastica di serie annegata in una sede stampata. Il gioco che ne risulta non e' quantificato da nessuna fonte.

### Cited Findings
- "the output splines can differ between different batches": due lotti di MG90S con squadrette simili ma non intercambiabili (una combinazione troppo lasca, l'altra si e' spaccata forzandola); squadrette SG90 e MG90S non intercambiabili; l'albero MG90S e' metallico e gia' filettato in fabbrica — [3rd-meas] [newscrewdriver.com](https://newscrewdriver.com/2020/12/27/notes-on-micro-servo-output-shaft/)
- Stampare il millerighe in FDM non e' praticabile per la finezza dei denti, e la variabilita' tra lotti sconsiglia anche la stampa a resina: l'autore usa le squadrette fornite — [3rd-meas/opinione] [newscrewdriver.com](https://newscrewdriver.com/2020/12/27/notes-on-micro-servo-output-shaft/)
- Vorpal (servo MG90): "there are only 22 little groves (splines) in each shaft", quindi la squadretta si puo' calettare solo a passi di circa 16° (errore fino a circa 8° dalla posizione ideale, da correggere via software); squadretta a un braccio; "you can insert the M2.5x8 screws into the servo horns to lock them in place"; in distinta 12 viti a testa cilindrica Ø 2.5 x 8 mm — [primary del progetto] [Vorpal Assembly Instructions](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Assembly_Instructions) (da riverificare sulla fonte: letto come riassunto)
- Vorpal: "If your kit includes O-rings or washers, you will need to use those on the shaft of the hip servos only" (solo con servo digitali); "Do not overtighten these screws, as you could possibly crack the servo brackets" — [primary del progetto] [Vorpal Assembly Instructions](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Assembly_Instructions)
- SmallpTsai: 18 viti M2x6 "for servo arms", una per servo (MG92B) — [secondary] [BOM.md](https://raw.githubusercontent.com/SmallpTsai/hexapod-v2-7697/master/mechanism/BOM.md)
- Squadrette in alluminio "21T": RampCrab "RC Servo Horn, Diameter 4.9mm, 21T, Thread M2.0mm, Aluminium Alloy 7075", 3 pezzi, per FCX24 / FCX18 — [secondary] [amazon.com B0D6GDBYGS](https://www.amazon.com/RampCrab-Diameter-Aluminium-Upgrade-Accessory/dp/B0D6GDBYGS); SERVOMY "21T-5mm Metal RC servo arm", 2 pezzi — [secondary] [amazon.com B0DT774531](https://www.amazon.com/SERVOMY-21T-5mm-Crawlers-Models-Electronics/dp/B0DT774531); squadretta CNC 21T dichiarata per servo 12-18 g, circa 14,98 US$ — [secondary] [ebay.de 125626159464](https://www.ebay.de/itm/125626159464). Nessuna dichiara compatibilita' MG90S (dettagli in `servo_mg90s.md`, sezione 5).
- Le squadrette INJORA per EMAX ES08MA II sono a 15 denti: non adatte — [secondary] [ebay.de 134159962214](https://www.ebay.de/itm/134159962214)
- Una guida generalista colloca SG90 e MG90S tra i servo a 25 denti — [secondary, bassa affidabilita': contraddetta da tutte le altre fonti] [zbotic.in](https://zbotic.in/servo-motor-horn-types-propeller-disc-arm-for-robotics/)

### Disaccordi tra fonti (non risolti)
- Denti del millerighe: 20 (ServoDatabase, datasheet clone Sky Star), 21 (Pololu, TinyTronics, venditori di squadrette), 22 (Vorpal, per il proprio MG90), 25 (guida zbotic). Vedi `servo_mg90s.md` sezione 4.
- Vite dell'albero: M2.5 x 8 (Vorpal, per il proprio MG90) contro M2 x 6 (SmallpTsai, per MG92B) contro fonti generiche in conflitto M2 / M2.5 (`servo_mg90s.md`). Nessuna di queste e' una misura sull'MG90S Tower Pro dell'utente.

### Inferences
- Progettare la sede attorno alla squadretta di plastica reale dell'utente (misurata), non attorno a una squadretta metallica comprata alla cieca. Sede a tasca che copia il contorno del braccio, piu' due viti passanti nei fori della squadretta e la vite centrale dell'albero: cosi' la coppia passa per forma e non per attrito.
- Il gioco residuo del giunto e' la somma di: gioco del riduttore del servo, accoppiamento millerighe-squadretta, gioco squadretta-tasca. Solo l'ultimo e' sotto il controllo del progettista (tasca disegnata a misura sulla squadretta reale, chiusa da viti).
- Con 20-22 denti il passo angolare e' 360 / 21 = 17.1° (16.4-18.0° per 22-20 denti): l'azzeramento meccanico e' grossolano e va rifinito via software, come dice Vorpal — [computed]

### Gaps
- Gioco angolare (gradi) lasciato da una squadretta di serie in una tasca stampata: NON TROVATO (nessuna misura pubblicata).
- Metodi documentati e quantificati per eliminare il gioco del millerighe sui micro servo: NON TROVATO; solo il rimedio Vorpal dell'O-ring, che serve a smorzare il tremolio dei servo digitali, non il gioco.
- Squadretta metallica con compatibilita' MG90S confermata e acquistabile da Italia: NON TROVATO.
- Quote delle squadrette di serie: NON TROVATO (vanno misurate).

---

## 4. Tenuta del corpo servo: alette e due viti contro culla / guscio; giochi FDM

### Takeaway
I progetti che funzionano non si affidano alle sole alette: o chiudono la cassa in un guscio a due meta' serrato da viti M2 passanti (SmallpTsai, VEB4697) o la incastrano a scatto in un portaservo che la avvolge (Vorpal). Le quote della cassa cambiano di 0.3-0.5 mm tra produttori, piu' del gioco di stampa: la sede va tarata sui servo reali e deve poter stringere.

### Cited Findings
- Guscio a sandwich: due viti M2x30 passanti + dado per servo tengono insieme meta' superiore, servo e meta' inferiore — [secondary] [LEG.md](https://raw.githubusercontent.com/SmallpTsai/hexapod-v2-7697/master/mechanism/LEG.md)
- VEB4697 usa 198 viti M2x10 e 234 dadi M2 per l'intero robot (gusci e giunti) — [secondary] [github.com/VEB4697/hexapod-MG90S](https://github.com/VEB4697/hexapod-MG90S)
- (2a ripresa) Nelle immagini di montaggio VEB4697 il guscio e' fatto di quattro pezzi piatti (telaio superiore con finestre, vassoio inferiore con incavo, due fianchi con tasche per dadi) chiusi da viti corte dall'alto e dal basso che entrano in dadi alloggiati nei fianchi; non si vedono viti nelle alette dei servo — [osservazione mia delle immagini, ramo v2 con servo da 21 g] [assembly_leg.gif](https://github.com/VEB4697/hexapod-MG90S/raw/v2/images/assembly_leg.gif)
- Vorpal: servo premuto nel portaservo fino allo scatto sotto una linguetta; le pareti del vano devono flettere verso l'esterno; nessuna vite sul corpo — [primary del progetto] [Vorpal Assembly Instructions](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Assembly_Instructions)
- Esapode senza viti (UPV): le zampe sono sagomate in modo che i servo restino in sede senza viti perche' la direzione delle forze li tiene a posto; piccoli difetti di stampa complicano il montaggio — [secondary, visto solo come riassunto di ricerca] [dyor.webs.upv.es](https://dyor.webs.upv.es/screwless-3d-printable-hexapod/)
- Supporti stampati per SG90/MG90S: la versione pesante usa tre punti di fissaggio M3 per stabilita' in tutte le direzioni, quella sottile non e' adatta a carichi elevati — [secondary, visto solo come riassunto di ricerca] [makerworld.com/models/423292](https://makerworld.com/en/models/423292-sg90-mg90s-servo-motor-quick-mounts)
- Giochi FDM: forzato 0.05-0.15 mm per lato, scorrevole 0.2-0.3 mm per lato — [secondary] [Sovol](https://www.sovol3d.com/blogs/news/fdm-3d-printing-tolerances-clearances-how-to-design-parts-that-fit)
- Quote della cassa secondo le fonti (da `servo_mg90s.md`): Tower Pro 22.8 x 12.2 (tabella 12.4) mm; clone Sky Star 22.4 x 12.1 (disegno 12.5) mm; PDF non ufficiale 22.5 x 12 mm; STEP dell'utente 22.6 x 12.2 mm — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/); [primary del clone] [Sky Star PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf)

### Calcoli
- Dispersione delle quote tra fonti: lunghezza 22.8 − 22.4 = 0.4 mm; larghezza 12.5 − 12.0 = 0.5 mm — [computed]. E' maggiore del gioco di progetto (0.1-0.15 mm per lato).
- Sede nominale sulle quote STEP con 0.1-0.15 mm per lato: (22.6 + 0.2...0.3) x (12.2 + 0.2...0.3) = 22.8-22.9 x 12.4-12.5 mm — [computed] da quote STEP e [Sovol](https://www.sovol3d.com/blogs/news/fdm-3d-printing-tolerances-clearances-how-to-design-parts-that-fit); da tarare sui servo reali
- Distanza tra asse del foro dell'aletta e faccia corta della cassa = (27.5 − 22.6) / 2 = 2.45 mm — [computed] da quote STEP dell'utente

### Inferences
- Due viti nelle alette stanno su una sola retta: da sole lasciano il servo libero di oscillare attorno a quella retta, frenato solo da alette di plastica spesse 2.5 mm. La culla che appoggia sulle quattro facce laterali e sul fondo blocca quell'oscillazione; le viti nelle alette servono a tenere il servo premuto nella culla.
- Poiche' la cassa varia di 0.3-0.5 mm tra lotti, una culla rigida a misura fissa o non entra o balla. Meglio una culla in due meta' (o con un taglio) che le viti chiudono sulla cassa, come nei due progetti GitHub.
- Il fondo della culla deve lasciare libero il cavo (esce dal lato corto vicino all'albero, in basso) e non deve appoggiare sulle teste delle viti del fondo cassa.

### Gaps
- Gioco culla-cassa "che funziona" misurato su MG90S in PLA-CF / PETG-CF: NON TROVATO; va ricavato con un provino.
- Confronto misurato di rigidezza tra fissaggio a sole alette e culla: NON TROVATO.

---

## 5. Viteria nelle parti stampate: inserti a caldo M2/M2.5/M3, dadi prigionieri, viti per le alette

### Takeaway
Inserti ruthex e CNC Kitchen hanno la stessa geometria: foro di datasheet 3.2 mm per M2 e 4.0 mm per M2.5 e M3, parete minima 1.3 e 1.6 mm. In CAD il foro va maggiorato di circa 0.2 mm e fatto 1 mm piu' profondo dell'inserto. Su M3 in PETG l'inserto a caldo regge 3 N·m contro 1 N·m della vite avvitata nella plastica e 2 N·m del dado in tasca. Sotto le alette dell'MG90S lo spazio (2.45 mm tra asse vite e cassa) non basta per rispettare la parete minima di un inserto M2: li' conviene vite passante e dado.

### Cited Findings
Tabella CNC Kitchen (colonne: "Length type L", "Insert diameter ⌀ D1", "Centre tip ⌀ D2", "Hole diameter ⌀ D3", "Wall thickness min. W"; unita' non dichiarate, mm) — [secondary: negozio che riporta i dati del produttore] [3djake.com CNC Kitchen M2](https://www.3djake.com/cnc-kitchen/threaded-inserts-m2-standard):

| Filetto | L | D1 inserto | D2 punta | D3 foro | W parete min |
|---|---|---|---|---|---|
| M2 Standard | 3.0 | 3.6 | 3.1 | 3.2 | 1.3 |
| M2.5 Standard | 4.0 | 4.6 | 3.9 | 4.0 | 1.6 |
| M3 Standard | 5.7 | 4.6 | 3.9 | 4.0 | 1.6 |
| M3 Short | 3.0 | 4.6 | 3.9 | 4.0 | 1.6 |
| M3 Voron | 4.0 | 5.0 | 4.25 | 4.4 | 1.3 |

Tabella ruthex (stesse colonne D1 / D2 / D3 / L / W, non spiegate sulla pagina) — [secondary] [3djake.ch assortimento ruthex](https://www.3djake.ch/de-CH/ruthex/m2-m3-m4-m5-gewindeeinsatz-sortimentskasten), [3djake.it ruthex M2.5](https://www.3djake.it/ruthex/inserto-filettato-m25-70-pezzi):

| Filetto (sigla) | D1 | D2 | D3 | L | W min | Confezione |
|---|---|---|---|---|---|---|
| M2 (RX-M2x4) | 3.6 | 3.1 | 3.2 | 4.0 | 1.3 | 70 pezzi |
| M2.5 (RX-M2.5x5.7) | 4.6 | 3.9 | 4.0 | 5.7 | 1.6 | 70 pezzi |
| M3 (RX-M3x5.7) | 4.6 | 3.9 | 4.0 | 5.7 | 1.6 | 100 pezzi |

Prezzi (acquistabili da Italia):
- ruthex M2.5, 70 pezzi: 9,19 € su 3DJake.it, "In Magazzino", consegna indicata 13 ottobre, spedizione gratuita da 49,90 € (altrimenti 5,90 €) — [secondary] [3djake.it](https://www.3djake.it/ruthex/inserto-filettato-m25-70-pezzi); 8,99 € su ruthex.de (art. GE-M25x57-001) — [primary] [ruthex.de](https://www.ruthex.de/products/ruthex-gewindeeinsatz-m2-5-70-stuck-rx-m2-5x5-7-messing-gewindebuchsen)
- CNC Kitchen su 3DJake.it: M2 x 3.0 100 pezzi 12,19 €; M2.5 x 4.0 100 pezzi 12,19 €; M3 x 5.7 100 pezzi 12,19 €; set standard 33,99 € — [secondary] [3djake.it CNC Kitchen](https://www.3djake.it/cnc-kitchen/inserti-filettati-m2-standard)

Regole di progetto e installazione (CNC Kitchen):
- "A blind hole should be slightly deeper than the length of the insert (approx. 1 mm)."; "Holes should be straight (not tapered)."; "Normally, no chamfer is required at the hole edge."; rispettare la parete minima W — [primary: produttore degli inserti] [cnckitchen.com tips](https://cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts)
- Saldatore circa 10-20 °C sopra la temperatura di stampa: circa 225 °C per PLA, 245 °C per PETG, 265 °C per ABS; nessun valore per i caricati carbonio — [primary] [cnckitchen.com tips](https://cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts)
- Fondere l'inserto per circa il 90% con la punta e finire a filo con un attrezzo piano, tenendolo fermo finche' la plastica solidifica — [primary] [cnckitchen.com tips](https://cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts)
- Prova su M3 in PLA (quasi 50 inserti, fori 3.6-4.6 mm): estrazione "around 1400 N" con fori stretti; forte calo tra 4.1 e 4.2 mm su fori alesati; i fori stampati escono circa 0.25 mm piu' piccoli del CAD; foro CAD consigliato 4.2 mm (circa 90% della resistenza massima); per gli inserti piu' piccoli aggiungere 0.2-0.3 mm al diametro in CAD — [3rd-meas, dal produttore] [cnckitchen.com](https://cnckitchen.com/blog/are-our-heat-set-insert-datasheets-wrong)

Confronto dei metodi (CNC Kitchen, vite M3, PETG, 4 perimetri, 100% infill) — [3rd-meas] [cnckitchen.com](https://www.cnckitchen.com/blog/helicoils-threaded-insets-and-embedded-nuts-in-3d-prints-strength-amp-strength-assessment):

| Metodo | Coppia di cedimento | Estrazione media |
|---|---|---|
| Vite avvitata direttamente nel PETG | 1 N·m (filetto tranciato) | 118 kg |
| Inserto a caldo (ruthex) | 3 N·m (l'inserto ruota nella plastica) | 119 kg |
| Helicoil | 1 N·m | 120 kg |
| Dado in tasca laterale | 2 N·m (PETG ceduto a compressione) | 86 kg |
| Dado in tasca dal fondo | circa 2 N·m | circa 166 kg |

- Conclusioni dell'autore: l'Helicoil non aggiunge nulla rispetto alla vite nella plastica; il dado e' un'alternativa economica valida se c'e' accesso dal retro o dal fianco, ma puo' essere scomodo e cadere durante il montaggio; per giunzioni aperte e chiuse spesso l'inserto a caldo e' "still the king for durable connection"; 1 N·m su M3 da' oltre 1500 N di precarico — [3rd-meas] [cnckitchen.com](https://www.cnckitchen.com/blog/helicoils-threaded-insets-and-embedded-nuts-in-3d-prints-strength-amp-strength-assessment)

Dadi (quote di norma, mm):
- Esagonali DIN 934 (ritirata, sostituita da DIN EN ISO 4032): M2 chiave s = 4, altezza m max 1.6 (min 1.35), spigoli e min 4.32; M2.5 s = 5, m max 2 (min 1.75), e min 5.45; M3 s = 5.5, m max 2.4 (min 2.15), e min 6.01 — [secondary: tabella di norma riprodotta] [fasten.it DIN 934](https://fasten.it/en/norms/norm/din_934)
- Quadri bassi DIN 562: M2 s = 4, m = 1.2, diagonale e min 5; M2.5 s = 5, m = 1.6, e min 6.3; M3 s = 5.5, m = 1.8, e min 7 — [secondary] [fasten.it DIN 562](https://fasten.it/en/norms/norm/din_562)

Viti per le alette del servo:
- SmallpTsai: M2x30 passante + dado M2, 2 per servo (MG92B); VEB4697: M2x10 + dado; una staffa commerciale SG90/MG90 e' fornita con viti M2 x 10 mm — [secondary] [BOM.md](https://raw.githubusercontent.com/SmallpTsai/hexapod-v2-7697/master/mechanism/BOM.md), [VEB4697](https://github.com/VEB4697/hexapod-MG90S), [protosupplies](https://protosupplies.com/product/sg90-mg90-servo-bracket/)

Vite M2 avvitata direttamente nella plastica stampata (2a ripresa; tutto visto come riassunto di ricerca, da provare su un provino):
- Tabella Bambu Lab per viti metriche M2: foro verticale (asse lungo Z) 1.84 mm in PLA e 1.70 mm in PETG HF; foro orizzontale 2.10 mm e 1.95 mm; diametro medio del filetto M2 1.740 mm. Bambu avverte che le viti metriche non sono pensate per la plastica e consiglia di fare i fori orizzontali una misura piu' grandi per non aprire gli strati — [secondary/community, riassunto di ricerca] [forum.bambulab.com](https://forum.bambulab.com/t/how-to-design-screw-holes-for-3d-printing/217352)
- Wiki CCI (stampanti Ultimaker): per viti che mordono la plastica, foro da 0 a 0.2 mm sotto il diametro nominale, cioe' 1.8-2.0 mm per M2 — [secondary, riassunto di ricerca] [wiki CCI](https://wiki.cci.arts.ac.uk/books/digital-fabrication-lab/page/design-the-clearance-and-tolerance-readme)
- Hubs: in mancanza di dati del produttore, preforo che dia il 75-80% di presa del filetto — [secondary, riassunto di ricerca] [hubs.com](https://www.hubs.com/blog/knowledge-base/how-assemble-3d-printed-parts-threaded-fasteners)
- Disaccordo: altre guide (MEDesignLab, SelfCAD) consigliano fori 0.1-0.2 mm PIU' GRANDI del nominale per le viti autofilettanti; dipende se la vite deve formare il filetto spostando plastica (foro piu' piccolo) o tagliarlo — [secondary, riassunto di ricerca] [medesignlab.me.wisc.edu](https://medesignlab.me.wisc.edu/?p=165)

### Calcoli
- Foro CAD per inserto = D3 + 0.2 mm: M2 3.4 mm; M2.5 e M3 4.2 mm — [computed] da tabella e regola [cnckitchen.com](https://cnckitchen.com/blog/are-our-heat-set-insert-datasheets-wrong)
- Profondita' foro cieco = L + 1 mm: M2 CNC Kitchen 4.0 mm, M2 ruthex 5.0 mm; M2.5 CNC Kitchen 5.0 mm, M2.5 ruthex 6.7 mm; M3 standard 6.7 mm; M3 short 4.0 mm; M3 Voron 5.0 mm — [computed] da tabelle e regola [cnckitchen.com tips](https://cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts)
- Diametro minimo della borchia = D3 + 2 x W: M2 3.2 + 2.6 = 5.8 mm; M2.5 e M3 4.0 + 3.2 = 7.2 mm; M3 Voron 4.4 + 2.6 = 7.0 mm — [computed] da tabella
- Inserto M2 sotto l'aletta del servo: parete tra foro inserto e vano servo = 2.45 − 3.4 / 2 − 0.15 (gioco del vano) = 0.60 mm, meno della parete minima 1.3 mm (con foro nominale 3.2 mm: 0.70 mm) — [computed] da quote STEP e tabella. L'inserto rischia di gonfiare o sfondare la parete verso il servo.
- Sede per dado con 0.1 mm di gioco per lato: esagonale M2 chiave 4.2 mm, altezza tasca 1.8 mm; M2.5 5.2 e 2.2 mm; M3 5.7 e 2.6 mm; quadro DIN 562 M2 4.2 x 4.2 x 1.4 mm; M2.5 5.2 x 5.2 x 1.8 mm; M3 5.7 x 5.7 x 2.0 mm — [computed] da [fasten.it](https://fasten.it/en/norms/norm/din_934) piu' gioco [Sovol](https://www.sovol3d.com/blogs/news/fdm-3d-printing-tolerances-clearances-how-to-design-parts-that-fit); da tarare con un provino

### Inferences
- Quando preferire cosa: inserto a caldo dove si smonta spesso e si serra a coppia (coperchi, piastra del corpo, vite-asse del giunto): tiene 3 volte la coppia della vite nella plastica. Dado prigioniero dove la vite tira in asse e c'e' accesso dal fondo (estrazione piu' alta, circa 166 kg) o dove manca lo spessore per l'inserto. Dado quadro DIN 562 in asola laterale: non ruota e si infila di fianco, ma in tasca laterale l'estrazione misurata e' la piu' bassa (86 kg).
- Per le alette dell'MG90S: vite M2 passante con dado sul lato opposto del guscio (schema SmallpTsai), cosi' la plastica lavora in compressione e non serve parete attorno a un inserto. Un inserto M2 li' e' fuori dalle regole del produttore (0.6 mm di parete contro 1.3 mm).
- Tra M2.5 e M3 conviene unificare su M3 per il telaio: stessi foro e borchia (4.0 / 7.2 mm), viteria piu' reperibile, e M3 e' anche il foro dei cuscinetti candidati. M2 solo attorno al servo.
- Gli inserti corti (M3 Short 3.0 mm, M2 3.0 mm) permettono pareti da circa 4 mm.

### Gaps
- Coppia di cedimento ed estrazione per inserti M2 e M2.5: NON TROVATO (le prove pubblicate sono su M3; i 1400 N sono su PLA).
- Dati di tenuta degli inserti in PLA-CF / PETG-CF e temperatura del saldatore per i caricati: NON TROVATO.
- Tolleranze min/max su chiave e altezza dei dadi DIN 934 / DIN 562: la pagina consultata da' solo i nominali.
- Diametro del preforo per avvitare una vite M2 direttamente nella plastica: trovato nella 2a ripresa solo come riassunto di ricerca (1.7-1.84 mm secondo Bambu Lab), non letto sulla fonte; nessun dato per PLA-CF / PETG-CF.
- Tabella dimensionale degli inserti sul sito del produttore (cnckitchen.store, ruthex.de): non letta; le quote vengono dalle schede del rivenditore 3DJake, coerenti tra ruthex e CNC Kitchen.
- Scheda tecnica ruthex con forza di estrazione e coppia: NON TROVATO (la pagina ruthex.de parla solo di "hohes Anzugs- und Lösemoment").

---

## 6. Materiali: PLA, PLA-CF, PETG, PETG-CF

### Takeaway
Con dati dello stesso laboratorio (schede Bambu): il PLA-CF e' il piu' rigido (modulo a flessione 3700 MPa, +35% sul PLA) ma e' il piu' debole tra gli strati (trazione Z 26 MPa) e cede al calore a 54-55 °C come il PLA; il PETG-CF ha la rigidezza del PLA normale (2890 contro 2750 MPa) con 68-74 °C di tenuta al calore, la miglior resistenza tra gli strati (38 MPa) e all'urto; il PETG non caricato e' il meno rigido (2050 MPa). Sul creep l'unico dato misurato trovato riguarda i non caricati: il PLA e' il peggiore e peggiora molto gia' a 40 °C.

### Cited Findings
Schede tecniche Bambu Lab, tutte lette integralmente; provini stampati al 100% di infill e condizionati (55 °C 8 h per i PLA, 65 °C 8 h PETG-CF, 75 °C 8 h PETG HF); metodi ISO 527 (trazione), ISO 178 (flessione), ISO 179 (urto), ISO 75 (HDT) — [primary] [PLA Basic V2.0](https://www.additive-x.com/shop/mpattachments/file/viewonline/id/494/product_id/2236), [PLA-CF V2.0](https://www.additive-x.com/shop/mpattachments/file/viewonline/id/817/product_id/2578), [PETG HF V1.0](https://botland.com.pl/img/art/inne/25540_karta_produktu.pdf), [PETG-CF V2.0](https://www.additive-x.com/shop/mpattachments/file/viewonline/id/596/product_id/2346):

| Proprieta' | PLA Basic | PLA-CF | PETG HF | PETG-CF |
|---|---|---|---|---|
| Densita' (g/cm³) | 1.24 | 1.22 | 1.28 | 1.25 |
| Tg (°C) | 60 | 63 | 66 | 68 |
| Vicat (°C) | 57 | 69 | 70 | 85 |
| HDT 1.8 MPa (°C) | 54 | 54 | 62 | 68 |
| HDT 0.45 MPa (°C) | 57 | 55 | 69 | 74 |
| Modulo a flessione X-Y (MPa) | 2750 ± 60 | 3700 ± 220 | 2050 ± 120 | 2890 ± 130 |
| Modulo a flessione Z (MPa) | 2370 ± 50 | 2260 ± 180 | 1810 ± 140 | 1680 ± 90 |
| Resistenza a flessione X-Y (MPa) | 76 ± 3 | 96 ± 3 | 64 ± 3 | 83 ± 4 |
| Resistenza a flessione Z (MPa) | 68 ± 2 | 49 ± 2 | 48 ± 4 | 62 ± 3 |
| Modulo di Young X-Y (MPa) | 2680 ± 130 | 2790 ± 120 | 1810 ± 190 | 2460 ± 230 |
| Modulo di Young Z (MPa) | 2160 ± 90 | 2160 ± 90 | 1540 ± 130 | 1340 ± 150 |
| Trazione X-Y (MPa) | 39 ± 2 | 38 ± 4 | 34 ± 4 | 59 ± 4 |
| Trazione Z, tra gli strati (MPa) | 35 ± 3 | 26 ± 2 | 23 ± 4 | 38 ± 3 |
| Allungamento a rottura X-Y / Z (%) | 12.2 / 7.5 | 12.7 / 3.6 | 8.6 / 5.1 | 10.4 / 4.7 |
| Urto X-Y, senza / con intaglio (kJ/m²) | 26.6 / 7.9 | 23.2 / 7.6 | 31.5 / 6.2 | 41.2 / 15.7 |
| Urto Z (kJ/m²) | 13.8 | 7.8 (riga etichettata "X-Y" nel PDF, verosimilmente Z) | 10.6 | 10.7 |
| Assorbimento d'acqua a saturazione (%) | 0.43 | 0.42 | 0.40 | 0.30 |
| Ugello / piano (°C) | 190-230 / 35-45 | 210-240 / 35-45 | 230-260 / 65-75 | 240-270 / 65-75 |
| Essiccazione | 55 °C 8 h | 55 °C 8 h | 65 °C 8 h | 65 °C 8 h |

- Bambu sconsiglia di ricuocere i pezzi in PETG HF: guadagno minimo e deformazioni — [primary] [PETG HF V1.0](https://botland.com.pl/img/art/inne/25540_karta_produktu.pdf)
- Per confronto, materiale che richiede camera chiusa: Bambu PET-CF V1.0, modulo a flessione X-Y 5080 ± 210 MPa, HDT 182 °C a 1.8 MPa, camera 45-60 °C, ugello 260-290 °C, ugello consigliato 0.6 mm — [primary] [PET-CF V1.0](https://www.additive-x.com/shop/mpattachments/file/viewonline/id/593/product_id/2342)
- Avvertenza comune a tutte le schede: valori "for design reference and comparison only"; le prestazioni del pezzo dipendono da stampante e parametri — [primary] [PLA-CF V2.0](https://www.additive-x.com/shop/mpattachments/file/viewonline/id/817/product_id/2578)

Filamenti Flashforge (2a ripresa). PDF "Flashforge Filament guides", tabella "Filament Technical Parameters" e "Print Setting Parameters", letto come testo estratto; non indica norme di prova ne' direzione di stampa — [primary: documento del produttore] [en.fss.flashforge.com PDF](https://en.fss.flashforge.com/10000/software/9d9a24cd6d47443d428166b4b1e23dfb.pdf):

| Voce | PLA | PETG | PLA CF | PETG CF |
|---|---|---|---|---|
| Resistenza a trazione (MPa) | 45-49 | 40-45 | 40-45 | 40-43 |
| Resistenza a flessione (MPa) | 69-75 | 50-55 | 85-95 | 75-85 |
| Assorbimento d'acqua, equilibrio in acqua a 23 °C (unita' non indicata) | <0.3 | <0.2 | 0.5 | 0.8 |
| Diametro ugello ("Nozzle Size") | All Size | All Size | 0.6/0.8mm | 0.6/0.8mm |
| Temperatura ugello (°C) | 190-220 | 220-240 | 200-230 | 230-250 |
| Temperatura piano (°C) | 25-60 | 70-80 | 25-60 | 60-80 |
| Velocita' di stampa normale (mm/s) | 40-60 | 40-60 | 40-60 | 40-60 |

- La riga "Hardened Nozzle Required" della stessa tabella usa simboli grafici che l'estrazione del testo non restituisce: quali colonne siano spuntate NON e' stato letto.
- Il documento non riporta modulo a flessione, HDT o resistenza tra gli strati per nessun filamento.
- Pagina "enterprise" Flashforge del PETG-CF: HDT 74 °C a 0.455 MPa, resistenza a flessione 75-85 MPa, a trazione 40-43 MPa (X-Y), "Elastic Modulus (X-Y direction) 2100~2400 MPa" senza dire se a trazione o a flessione; ugello 220-270 °C, mentre la pagina consumer dice 200-240 °C. Pagina "enterprise" del PLA-CF: "Modulus of Elasticity (X-Y direction) 1100~1300 MPa" e due righe "Tensile Strength" in conflitto (85-95 e 40-45 MPa) — [primary, ma visto SOLO come riassunto di ricerca: le due pagine hanno risposto 404 alla lettura diretta; il modulo del PLA-CF (1100-1300 MPa) e' circa un terzo di quello Bambu e Polymaker ed e' sospetto] [enterprise.flashforge.com petg-cf](https://enterprise.flashforge.com/products/petg-cf), [enterprise.flashforge.com pla-cf](https://enterprise.flashforge.com/products/pla-cf)
- Controprova da un terzo produttore: Polymaker PolyLite PLA-CF, HDT 54 °C (ISO 75, 0.45 MPa), modulo a flessione X-Y circa 3380 MPa (ISO 178): in linea con Bambu PLA-CF (55 °C, 3700 MPa) — [primary, visto come riassunto di ricerca] [Polymaker PolyLite PLA-CF TDS](https://polymaker.com/wp-content/uploads/lana-downloads/PolyLite_PLA-CF_TDS_US_5.3.pdf)

Creep dei caricati carbonio (2a ripresa; solo indizi da riassunti di ricerca, nessun dato su PLA-CF o PETG-CF in flessione):
- Uno studio su compositi di PETG stampati, provati a COMPRESSIONE, riporta per i campioni rinforzati rilassamento degli sforzi e spostamento a compressione maggiori del PETG non caricato — [3rd-meas, riassunto di ricerca; materiale e condizioni non letti] [estudogeral.uc.pt](https://estudogeral.uc.pt/handle/10316/102830)
- Uno studio del 2024 su PET caricato carbonio trova che la resistenza al creep dipende fortemente dall'orientamento del riempimento — [3rd-meas, riassunto di ricerca] [acris.aalto.fi PDF](https://acris.aalto.fi/ws/portalfiles/portal/164003634/1-s2.0-S2666682024000999-main.pdf)
- Una ricerca mirata sulle prove di creep MyTechFun per PLA-CF e PETG-CF non ha trovato alcun risultato numerico.

Creep (articolo letto integralmente): Dogan, Strojniški vestnik 68 (2022) 451-460; filamenti Ultimaker (PLA, Tough PLA, ABS, CPE, PC, Nylon), provini ASTM D638 tipo IV stampati su Ultimaker 2+ a strato 0.2 mm e poi fresati, prova a trazione costante di 3 ore (10 800 s) a 10 e 20 MPa, a 25, 40 e 60 °C — [3rd-meas, articolo scientifico] [SV-JME PDF](https://www.sv-jme.eu/?ns_articles_pdf=%2Fns_articles%2Ffiles%2Fojs30%2F191%2F63073da9a438a.pdf&id=6869)
- "PLA, which is the most commonly used polymer in 3D printers, is determined as the material with the worst creep resistance. For this reason, it is recommended that the parts produced using PLA with a 3D printer should be used at room temperature with no load or under very low static loads." — [3rd-meas] [SV-JME PDF](https://www.sv-jme.eu/?ns_articles_pdf=%2Fns_articles%2Ffiles%2Fojs30%2F191%2F63073da9a438a.pdf&id=6869)
- "the creep resistance of the CPE materials is better than ABS, PLA, and TPLA"; ABS e CPE adatti a "medium loads and moderate temperatures" — [3rd-meas] [SV-JME PDF](https://www.sv-jme.eu/?ns_articles_pdf=%2Fns_articles%2Ffiles%2Fojs30%2F191%2F63073da9a438a.pdf&id=6869)
- "According to the test results, the load is a more effective parameter on creep than the temperature." A 60 °C tutti i materiali tranne il PC si rompono rapidamente a 20 MPa; PLA e Tough PLA si rompono anche a 10 MPa — [3rd-meas] [SV-JME PDF](https://www.sv-jme.eu/?ns_articles_pdf=%2Fns_articles%2Ffiles%2Fojs30%2F191%2F63073da9a438a.pdf&id=6869)
- Allungamento dopo 3 ore LETTO DA ME SUI GRAFICI (figure 4, 5, 8, 9; valori approssimati, l'articolo non da' tabelle): a 25 °C e 10 MPa PLA circa 70 µm, Tough PLA circa 34, ABS circa 27, CPE circa 11, PC circa 3; a 40 °C e 10 MPa PLA circa 130 µm, Tough PLA circa 85, ABS circa 63, CPE circa 60; a 25 °C e 20 MPa PLA circa 290 µm, CPE circa 85; a 40 °C e 20 MPa PLA circa 1830 µm, CPE circa 250 — [3rd-meas, lettura approssimata di grafici] [SV-JME PDF](https://www.sv-jme.eu/?ns_articles_pdf=%2Fns_articles%2Ffiles%2Fojs30%2F191%2F63073da9a438a.pdf&id=6869)
- Altre prove di creep consultate danno solo risultati qualitativi: MyTechFun (PLA, PETG, ASA, Nylon; tre prove su 6 giorni; i numeri sono nel video e in un file xlsx non letti) — [3rd-meas, numeri non accessibili] [mytechfun.com/video/143](https://www.mytechfun.com/video/143); fermagli in PLA, PETG, ABS, nylon tenuti in tensione oltre 24 ore e poi una settimana: nessuno torna alla forma iniziale, quello in PLA stringe ancora a sufficienza — [community] [thrinter.com](http://thrinter.com/creep-abs-pla-petg-alloy-910/)

Impostazioni di stampa per resistenza e rigidezza (CNC Kitchen; visti come riassunti di ricerca con citazioni):
- Per un gancio caricato a flessione: stampare di piatto e "use more perimeters rather than more infill", perche' le linee di estrusione seguono cosi' il percorso delle forze — [3rd-meas] [cnckitchen.com gancio](https://cnckitchen.com/blog/how-designs-the-strongest-hook-polymaker-competition)
- Carico di rottura dei ganci: 2 perimetri al 100% di larghezza 20 kg; 4 perimetri al 100% 33 kg; 3 perimetri al 133% 37 kg; 2 perimetri al 200% di larghezza 39 kg — [3rd-meas] [cnckitchen.com larghezza estrusione](https://www.cnckitchen.com/blog/the-effect-of-extrusion-width-on-strength-and-quality-of-3d-prints)
- Non sotto-estrudere: la flessione genera sforzi trasversali e di taglio che separano i perimetri — [3rd-meas] [cnckitchen.com gancio](https://cnckitchen.com/blog/how-designs-the-strongest-hook-polymaker-competition)
- Pezzi in PLA pieni al 100% rotti a 131 kg, gli stessi al 30% di infill a 71 kg in media; PLA e PETG stampati sono resistenti ma poco rigidi se infill e perimetri non sono regolati — [3rd-meas] [cnckitchen.com stampe contro legno](https://www.cnckitchen.com/blog/whats-stronger-3d-prints-or-wood)
- Hexana (AranaCorp, esapode per MG90S): ABS o PLA, strato 0.2 mm, 65% di infill — [secondary, visto solo come riassunto di ricerca] [cults3d.com](https://cults3d.com/en/3d-model/gadget/robot-hexapode-hexana-pour-servo-mg90s)

### Calcoli
- Rigidezza relativa a flessione rispetto al PLA Basic (modulo X-Y): PLA-CF 3700 / 2750 = 1.35; PETG-CF 2890 / 2750 = 1.05; PETG HF 2050 / 2750 = 0.75. A pari geometria la freccia e' inversamente proporzionale: PLA-CF 0.74, PETG-CF 0.95, PETG HF 1.34 volte quella del PLA — [computed] dalle schede Bambu
- Resistenza a trazione tra gli strati rispetto a quella nel piano (Z / X-Y): PLA 35 / 39 = 90%; PLA-CF 26 / 38 = 68%; PETG HF 23 / 34 = 68%; PETG-CF 38 / 59 = 64% — [computed]
- Resistenza a flessione Z / X-Y: PLA 68 / 76 = 89%; PLA-CF 49 / 96 = 51%; PETG HF 48 / 64 = 75%; PETG-CF 62 / 83 = 75% — [computed]
- Creep PLA, effetto di 15 °C in piu': a 20 MPa da circa 290 µm (25 °C) a circa 1830 µm (40 °C) = 6.3 volte — [computed] da lettura dei grafici SV-JME

### Inferences
- Scelta per parte (ragionamento mio sui dati sopra):
  - Culle servo, staffe dei giunti e piastre del corpo (plastica sotto precarico di viti, a contatto con servo ed elettronica che scaldano, con inserti a caldo): PETG-CF. Ha 14-19 °C di margine termico in piu' sul PLA-CF (HDT 68 contro 54 °C a 1.8 MPa, 74 contro 55 °C a 0.45 MPa), la miglior tenuta tra gli strati e all'urto, e la rigidezza del PLA normale.
  - Segmenti lunghi e snelli (femore, tibia) dove conta solo la rigidezza a flessione e il pezzo resta a temperatura ambiente: PLA-CF (+35% di rigidezza), a patto di orientare gli strati lungo il segmento.
  - Coperture estetiche e parti non caricate: PLA o PETG normali (PLA per finitura e facilita', PETG se vicino a fonti di calore).
  - Volendo un solo materiale strutturale: PETG-CF ovunque.
- Il carbonio aumenta la rigidezza solo nel piano di stampa: in Z il modulo del PLA-CF (2260 MPa) e del PETG-CF (1680 MPa) e' inferiore a quello del PLA normale (2370 MPa), e la resistenza tra gli strati cala. Con i caricati l'orientamento conta di piu'.
- Regole di orientamento per i giunti:
  - L'asse del foro cuscinetto e dell'albero servo deve essere verticale in stampa (foro stampato come cerchio nel piano X-Y: piu' rotondo e con i perimetri che lo cingono).
  - I bracci della staffa a U lavorano a flessione: vanno stampati coricati, cosi' gli strati corrono lungo il braccio e non lo attraversano. Una U stampata in piedi mette gli strati in trazione proprio alla radice dei bracci.
  - Le viti che tirano perpendicolarmente agli strati (inserto estratto lungo Z) lavorano sulla resistenza Z, la piu' bassa: preferire vite passante e dado che comprimono gli strati.
- Impostazioni di partenza per i pezzi strutturali: 4 o piu' perimetri, infill 40-65%, 5 o piu' strati pieni sopra e sotto; i pezzi piccoli e fitti di fori (culle, staffe) risultano di fatto quasi pieni. Sono un mio punto di partenza derivato dalle prove CNC Kitchen e dal 65% di Hexana, non un valore ottimizzato.
- Il PLA e il PLA-CF non vanno usati dove la plastica resta sotto carico costante e al caldo (un servo in stallo, un'auto al sole): il creep del PLA sale di circa 6 volte gia' a 40 °C.

### Gaps
- Creep misurato di PLA-CF e PETG-CF: NON TROVATO (cercato in tutte e tre le passate). Gli indizi della 2a ripresa dicono solo che la fibra non garantisce da sola un creep minore. Il confronto di creep riguarda solo polimeri non caricati; "CPE" nell'articolo e' il filamento Ultimaker CPE, che l'articolo chiama "chlorinated polyethylene" ma che per quanto mi risulta e' un copoliestere della famiglia del PETG (non verificato in questa ricerca).
- Scheda tecnica dei filamenti che l'utente possiede davvero: i valori sopra sono Bambu Lab e cambiano da marca a marca (percentuale e tipo di fibra non dichiarati).
- Scheda Prusament PETG Carbon Fiber: cercata nel primo tentativo ma non letta.
- Filamenti Flashforge PLA-CF / PETG-CF: il produttore pubblica solo resistenze a trazione e flessione (lette nella 2a ripresa); modulo a flessione, HDT del PLA-CF e resistenza tra gli strati NON TROVATI su un documento leggibile. Non esiste quindi, per i filamenti Flashforge, un confronto di rigidezza da fonte primaria: il +35% del PLA-CF vale per Bambu.
- Dai dati Flashforge (flessione 85-95 MPa PLA CF contro 75-85 MPa PETG CF contro 69-75 MPa PLA) l'ordine di resistenza e' lo stesso delle schede Bambu, ma i valori di PETG non caricato (50-55 MPa) sono molto piu' bassi: i numeri non sono trasferibili da una marca all'altra.
- Prova diretta "perimetri contro infill" sulla rigidezza (non sulla rottura): NON TROVATO in forma scritta (CNC Kitchen rimanda a un video).

---

## 7. La stampante: FlashForge Creator 5

### Takeaway
La "Flashforge Creator 5" esiste (presente sul comparatore europeo geizhals dal 2 luglio 2026): CoreXY a telaio aperto con 4 testine indipendenti, volume 256 x 256 x 256 mm, ugello in acciaio temprato fino a 320 °C, piano fino a 120 °C; PLA, PETG, PLA-CF e PETG-CF sono tutti nella lista dei filamenti consigliati dal produttore. Esiste anche la "Creator 5 Pro", chiusa e con camera riscaldata fino a 65 °C: sono due macchine diverse e la base non si puo' trasformare in Pro. (2a ripresa) Restano due punti aperti che toccano i caricati carbonio: la guida filamenti Flashforge chiede ugello 0.6/0.8 mm per PLA CF e PETG CF mentre la macchina esce con 0.4 mm, e una recensione indica l'ugello di serie come inox anziche' temprato.

### Cited Findings
Creator 5 (pagina ufficiale):
- Volume di stampa 256 x 256 x 256 mm; 4 testine indipendenti; ugello max 320 °C; piano max 120 °C; struttura "Open Frame Design"; nessun kit di chiusura a listino per questo modello — [primary] [flashforge.com Creator 5](https://www.flashforge.com/products/creator-5-multi-color-3d-printer)
- "Its 320°C hardened-steel nozzles support standard and moderately abrasive materials." Ugelli smontabili da 0.4 mm (di serie), 0.25, 0.6 e 0.8 mm — [primary] [flashforge.com](https://www.flashforge.com/products/creator-5-multi-color-3d-printer)
- Filamenti consigliati: PLA, PETG, TPU-90A, TPU-95A, TPU-64D, PLA-CF, PETG-CF, SILK, PVA, BVOH. Filamenti che richiedono camera chiusa: ABS, ASA, HIPS, ABS-GF, PA-CF, ASA-CF, ASA-GF, S-Multi, S-PAHT, PET-CF, PAHT-CF, PPA-CF, PPS-CF — [primary] [flashforge.com](https://www.flashforge.com/products/creator-5-multi-color-3d-printer)
- Velocita' max di spostamento 600 mm/s, di stampa 300 mm/s, accelerazione 30 000 mm/s², portata 32 mm³/s; altezza strato 0.1-0.4 mm — [primary] [flashforge.com](https://www.flashforge.com/products/creator-5-multi-color-3d-printer); [secondary] [shop3duniverse](https://shop3duniverse.com/products/flashforge-creator-5)
- Ingombro 436 x 432 x 480 mm (520 x 443 x 710 mm con tubi e portabobine); 14 kg netti; 700 W; schermo 4 pollici, livellamento automatico, sensore filamento, ripresa dopo blackout, camera 1280x720, Wi-Fi — [primary] [flashforge.com](https://www.flashforge.com/products/creator-5-multi-color-3d-printer)
- Conferma indipendente (comparatore prezzi): Flashforge Creator 5, codice 10001101001, 256 x 256 x 256 mm, 4 testine, 320 °C ugello, 120 °C piano, filamento 1.75 mm, materiali BVOH, PETG, PETG-CF, PLA, PLA-CF, PVA, SILK, TPU; a listino dal 02.07.2026 — [secondary] [geizhals.at](https://geizhals.at/flashforge-creator-5-10001101001-a3861996.html)
- Prezzi: 699 US$ sul sito ufficiale (in offerta) — [primary] [flashforge.com](https://www.flashforge.com/products/creator-5-multi-color-3d-printer); in Europa da 541,57 € (alza.at), 668,99 € (mylemon.at), 669,00 € (galaxus.at), aggiornati all'8.10.2026, tutti con consegna solo in Austria — [secondary] [geizhals.at](https://geizhals.at/flashforge-creator-5-10001101001-a3861996.html)

Ugelli (2a ripresa):
- Ricambio ufficiale "Nozzle Assembly for Creator 5 Series": misure 0.25, 0.4, 0.6 e 0.8 mm, tutte marcate 320 °C; 39,90 US$ (prezzo in offerta); 0.25 mm per "fine details and higher precision", 0.6 mm per "faster printing and functional parts", 0.4 mm per l'uso quotidiano, 0.8 mm per alto flusso. La pagina NON dichiara il materiale dell'ugello e non parla di filamenti caricati — [primary] [flashforge.com nozzle assembly](https://flashforge.com/products/flashforge-nozzle-assembly-for-creator-5-series)
- La guida filamenti Flashforge indica "Nozzle Size 0.6/0.8mm" per PLA CF e PETG CF e "All Size" per tutti gli altri filamenti (documento generale senza data, non specifico per la Creator 5) — [primary] [en.fss.flashforge.com PDF](https://en.fss.flashforge.com/10000/software/9d9a24cd6d47443d428166b4b1e23dfb.pdf)
- FAQ Flashforge riferita all'Adventurer 5M: l'ugello da 0.25 mm "may clog more easily with abrasive or composite materials"; 0.6 e 0.8 mm "Better suited for abrasive materials (e.g., carbon fiber-filled filaments)" — [primary, visto come riassunto di ricerca; URL della FAQ non identificato]
- Materiale dell'ugello di serie: "hardened-steel" secondo la FAQ della pagina prodotto Flashforge e secondo il rivenditore Currys ("hardened steel nozzles - support abrasive materials such as carbon fibre and nylon"); la recensione di Tom's Hardware lo elenca invece come ".4mm stainless steel proprietary" — [primary] [flashforge.com](https://www.flashforge.com/products/creator-5-multi-color-3d-printer); [secondary, riassunto di ricerca] [currys.co.uk](https://www.currys.co.uk/products/flashforge-creator-5-3d-printer-black-10305608.html), [tomshardware.com](https://www.tomshardware.com/3d-printing/flashforge-creator-5-review) (la recensione non e' stata leggibile per intero)
- Un rivenditore canadese elenca ugelli 0.2 / 0.4 / 0.6 / 0.8 mm invece di 0.25: probabile errore della scheda, il ricambio ufficiale e' 0.25 mm — [secondary, riassunto di ricerca] [memoryexpress.com](https://www.memoryexpress.com/Products/MX00137027)

Creator 5 Pro:
- "Fully Enclosed, Rigid Frame"; "Active Heated Chamber up to 65°C" (riscaldamento per ABS, ASA, PC, PA; modalita' raffreddamento per PLA, TPU, PETG, PLA-CF); 4 testine; filtro HEPA H13 e carbone; 749 £ in offerta, 849 £ di listino — [primary] [uk.flashforge.com Creator 5 Pro](https://uk.flashforge.com/products/flashforge-creator-5-pro)
- Il riscaldamento attivo della Pro "is built into the machine itself"; una Creator 5 base non e' aggiornabile a Pro, puo' solo ricevere una chiusura artigianale passiva — [primary] [flashforge.com](https://www.flashforge.com/products/creator-5-multi-color-3d-printer)
- Creator 5 Pro: 256 x 256 x 256 mm, 320 °C estrusore, 120 °C piano (riassunto di ricerca del negozio ufficiale UK); codice 10001103001, 848,99 € (mylemon.at) e 849,00 € (galaxus.at) — [secondary] [geizhals.at](https://geizhals.at/flashforge-creator-5-10001101001-a3861996.html)

### Disaccordi tra fonti
- Velocita' di stampa: 300 mm/s (sito ufficiale) contro 600 mm/s indicati come "Max Print Speed" da un blog — [secondary] [antonmansson.com](https://www.antonmansson.com/3d-printing-blog/flashforge-creator-5-breakdown). 600 mm/s e' la velocita' di spostamento.
- Materiale dell'ugello di serie: acciaio temprato (Flashforge, Currys) contro acciaio inox (tabella di Tom's Hardware). Non risolto: conta per l'usura con i caricati carbonio.
- Diametro dell'ugello per i caricati carbonio: la pagina prodotto mette PLA-CF e PETG-CF tra i filamenti consigliati senza restrizioni di ugello (di serie 0.4 mm), la guida filamenti Flashforge chiede 0.6/0.8 mm. Non risolto.
- Prezzo europeo della Pro: circa 1 030-1 050 € IVA inclusa secondo un riassunto di ricerca del primo tentativo (fonte non identificata) contro 848,99 € su geizhals all'8.10.2026.
- Un negozio ucraino indica la camera della Pro sia "Closed" sia "Open" nella stessa scheda: errore della scheda — [secondary] [3ddevice.com.ua](https://3ddevice.com.ua/en/product/3d-printer-flashforge-creator-5-pro/)

### Inferences
- I quattro materiali dell'utente sono tutti stampabili sulla Creator 5 base senza chiusura; secondo Flashforge gli ugelli di serie sono in acciaio temprato e reggono i caricati carbonio ("moderately abrasive"), ma una recensione li indica in inox (vedi disaccordi).
- (2a ripresa) Per PLA-CF e PETG-CF conviene prevedere un ugello da 0.6 mm sulla testina dedicata ai caricati (ricambio ufficiale a 39,90 US$): e' cio' che chiede la guida filamenti Flashforge e riduce il rischio di intasamento. Con ugello 0.6 mm la larghezza di estrusione sale a circa 0.6-0.7 mm (stima mia, non da fonte): pareti sottili, tasche per dadi M2 e dettagli fini vanno ridisegnati a multipli di quella larghezza, e i giochi dei provini vanno rifatti con quell'ugello.
- 256 mm di lato bastano per stampare in un pezzo solo le piastre del corpo di un esapode a micro servo.
- Le 4 testine permettono di stampare supporti in un materiale diverso (per esempio PLA sotto PETG-CF o viceversa) per sedi e sbalzi puliti, o di tenere caricati insieme PETG-CF, PLA-CF e un materiale per le coperture.
- Macchina aperta: niente PET-CF, PA-CF, ABS, ASA. Se l'utente ha la Pro, la camera va tenuta in modalita' raffreddamento per PLA, PLA-CF e PETG.

### Gaps
- Manuale utente PDF della Creator 5: non letto (non cercato per limite di chiamate); le specifiche vengono dalla pagina prodotto letta come riassunto e sono confermate da geizhals per volume, testine e temperature.
- Diametro dell'ugello ammesso con i caricati carbonio SULLA CREATOR 5: non trovato in forma specifica; la guida filamenti generale Flashforge dice 0.6/0.8 mm (2a ripresa). Il profilo PLA-CF / PETG-CF dello slicer Flashforge per la Creator 5 con ugello 0.4 mm non e' stato controllato.
- Manuale: su manualslib esiste un "Flashforge Creator 5 Pro Quick Start Manual" ([manualslib.com](https://www.manualslib.com/manual/4527394/Flashforge-Creator-5-Pro.html)), non letto.
- Precisione dello scostamento tra le quattro testine (conta se si stampano supporti o pezzi con due materiali): NON TROVATO.
- Prezzo e disponibilita' presso un negozio che spedisce in Italia: NON TROVATO (non rilevante se l'utente possiede gia' la macchina).
- Precisione dimensionale reale della macchina dell'utente: va misurata con un provino.

---

## Cose che solo l'utente puo' fornire

1. Modello esatto della stampante: Creator 5 (telaio aperto) o Creator 5 Pro (chiusa)? Diametro dell'ugello montato sulle testine.
2. Marca e nome commerciale dei filamenti PLA-CF e PETG-CF posseduti (le schede tecniche cambiano da marca a marca: i numeri della sezione 6 sono Bambu Lab).
3. Misure col calibro su almeno 3 servo reali: lunghezza, larghezza e altezza della cassa; diametro del foro delle alette; sporgenza delle teste delle viti sul fondo cassa (servono per il fondo della culla).
4. Squadrette di serie: numero di denti contati sull'albero, lunghezza, spessore, interasse e diametro dei fori del braccio che si intende usare; filetto e lunghezza della vite dell'albero (M2 o M2.5).
5. Un provino di tolleranze stampato sulla propria macchina, in ciascun materiale strutturale: fori da 6.9 a 7.4 mm e da 7.9 a 8.4 mm a passi di 0.05-0.1 mm (sede cuscinetto), fori 3.2-3.5 mm e 4.0-4.4 mm (inserti), una tasca 22.6 x 12.2 mm con gioco 0.05-0.2 mm per lato (culla servo), una sede per dado M2.
6. Se dispone di un saldatore a temperatura regolabile (225-245 °C) e di punte per inserti.
7. Prezzo e disponibilita' al momento dell'ordine di: cuscinetti F683ZZ / MR83ZZ in confezione da 20 su Amazon.it o AliExpress; cerniera Lynxmotion PSH-02 su RobotShop EU (le pagine non erano leggibili dagli strumenti usati).
8. (2a ripresa) Ugelli: cosa c'e' scritto sull'ugello di serie o nel manuale (acciaio temprato o inox?) e se nello slicer Flashforge i profili PLA-CF / PETG-CF per la Creator 5 sono disponibili con ugello 0.4 mm o solo con 0.6 / 0.8 mm. Se possiede gia' un ugello da 0.6 mm.
9. (2a ripresa) Cosa intende usare come asse del giunto: se ha gia' spine rettificate da 3 mm (e in che tolleranza, h6 o m6) o solo viti M3; un calibro centesimale o un micrometro per misurare perni e fori.
