# Bilancio di massa, geometria delle zampe e dimensionamento della coppia per un esapode con 18 MG90S

Stato del file: **versione 2, completa** (8 ottobre 2026). La versione 1 era stata scritta dalle evidenze del tentativo interrotto; questa integra 15 ulteriori ricerche.

Legenda delle etichette di fonte: **[primary]** datasheet / manuale / pagina o codice del produttore; **[secondary]** inserzione di negozio, blog, wiki, database; **[3rd-meas]** misura di terzi; **[community]** forum / autore di un progetto amatoriale; **[computed]** calcolo mio, con formula.

Avvertenza sulla qualità dell'evidenza:
- "(testo letto)" = ho letto il testo della pagina, del PDF o del file sorgente.
- "(riassunto)" = il numero viene dal riassunto automatico di una pagina scaricata; affidabile per orientarsi, non l'ho visto citato alla lettera.
- "(snippet)" = il numero viene solo dal risultato di un motore di ricerca; la pagina non è stata aperta. **Da ricontrollare prima di metterlo in un ordine o in una quota CAD.**

Unità: coppie in kgf·cm (1 kgf·cm = 0,0981 N·m), masse in g, lunghezze in mm.

---

## 1. Esapodi esistenti con servo classe 9 g (SG90 / MG90S / MG92B): massa, batteria, zampe, affidabilità

### Takeaway
Non ho trovato NESSUN esapode documentato con 18 MG90S e un pacco LiPo da 250 g. I riferimenti a 18 gradi di libertà in questa taglia pesano 0,58 kg (Hiwonder miniHexa, commerciale) o usano servo da 3,5 kgf·cm (SmallpTsai con MG92B), e tutti montano batterie da circa 100 g (2 celle 18650) o un piccolo LiPo 2S. L'unico progetto nato con MG90S (VEB4697) li ha abbandonati per guasti frequenti. Le geometrie lette dal codice sorgente: Freenove coxa 22,75 / femore 55 / tibia 70 mm, passo 42 mm; SmallpTsai coxa 28 / femore 42,6 / tibia 89 mm, passo 50 mm.

### Cited Findings

**Tabella di sintesi** (dettagli e fonti sotto)

| Progetto | Servo | Massa totale | Batteria | Coxa / femore / tibia (mm) | Piede dall'asse femore, in posa (mm) |
|---|---|---|---|---|---|
| Freenove FNK0031 (kit, acrilico) | 18, modello non dichiarato | 820 g secondo un'inserzione (incerto) | 2×18650 | 22,75 / 55 / 70 | 43,3 [computed] |
| Hiwonder miniHexa (commerciale, alluminio) | 18 × HPD-0127 (≥ 1,8 kgf·cm a 7,4 V) | 580 g | 2×18650 2200 mAh | NON TROVATO | NON TROVATO |
| SmallpTsai hexapod-v2-7697 (PLA) | 18 × Tower Pro MG92B (3,5 kgf·cm a 6 V) | NON TROVATO | LiPo 2S | 28 / 42,6 / 89,07 | 59,9 [computed] |
| VEB4697 hexapod v2 (stampato) | 18 × servo da 21 g | NON TROVATO | 2×18650 | NON TROVATO | — |
| Vorpal The Hexapod (stampato) | 12 × MG90 | NON TROVATO | 2×18650, circa 110 g | zampe a 2 giunti | — |
| DYOR UPV (stampato) | 12 × SG90 | circa 500 g | powerbank 5000 mAh | NON TROVATO | — |

**Freenove Hexapod Robot Kit FNK0031 (18 servo, telaio in acrilico)** — geometria letta dal codice sorgente della libreria ufficiale `FNHR` (testo letto)
- Assi coxa nel piano del corpo: zampe d'angolo a (±35, ±50) mm, zampe medie a (±49, 0) mm (x = laterale, y = longitudinale) per la versione V3 (`robotShape.a = 35; b = 50; g = 49`); 32 / 50 / 46 per V1-V2 — [primary] [Freenove_Hexapod_Robot_Kit, ArduinoLibraries/FNHR.zip → src/FNHRBasic.cpp](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)
- Segmenti: `d = 22.75` (distanza orizzontale asse coxa → asse femore), `c = 15.75` (quota dell'asse femore sopra il piano z = 0), `e = 55` (femore), `f = 70` (tibia) — [primary] [FNHRBasic.cpp](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)
- Cinematica del produttore: `u = d + e·sin(β) + f·sin(γ−β)`, `v = c + e·cos(β) − f·cos(γ−β)` — [primary] [FNHRBasic.cpp](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)
- Posizione dei piedi all'avvio (`bootPoints`): (±81, ±99, 0) e (±115, 0, 0) mm — [primary] [FNHRBasic.h](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)
- Andatura: `crawlLength = 42` mm, `turnAngle = 18`°, `legLift = 20` mm, `defaultBodyLift = 15` mm, `crawlSteps` = 2 (tripode), 4 o 6 — [primary] [FNHRBasic.h / .cpp](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)
- Limiti di giunto nel firmware: coxa zampa media 135…225° (90° di finestra), coxa d'angolo 90…200° (110°); femore e tibia 0…180° — [primary] [FNHRBasic.cpp](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)
- Batteria: 2 celle 18650 da 3,7 V (non incluse), tipo "flat-top unprotected" — [primary] [AboutBattery_for_V3.pdf](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit/blob/master/AboutBattery_for_V3.pdf), [Tutorial_for_V3.pdf](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit/blob/master/Tutorial_for_V3.pdf) (testo letto)
- Il firmware accende i gruppi di servo sopra 6,5 V e li spegne sotto 5,5 V (`powerGroupOnVoltage = 6.5`, `powerGroupOffVoltage = 5.5`) — [primary] [FNHRBasic.h](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)
- Massa: un'inserzione di rivenditore riporta 820 g e 26,97 × 16,48 × 5,99 cm per il modello FNK0031 (66 pezzi); non è chiaro se sia il robot montato o il kit imballato — [secondary] [desertcart](https://www.desertcart.sn/products/96948045), [newegg](https://www.newegg.com/global/au-en/p/3C6-02NP-000D1) (snippet)
- Un recensore definisce i servo del kit piccoli e deboli e dice che il robot va male su piastrelle e pendenze — [community] [inserzione desertcart](https://www.desertcart.sn/products/96948045) (snippet)
- Modello e coppia dei 18 servo: **NON TROVATO** (il manuale di 71 pagine elenca solo "Servo Package x18").

**Hiwonder miniHexa (18 servo, telaio in alluminio, ESP32)**
- 0,58 kg; 240 × 234 × 84 mm; struttura in lega di alluminio anodizzata; 2 celle 18650 da 3,7 V 2200 mAh; fino a 60 minuti dichiarati; 18 micro servo "anti-stall" HPD-0127 — [secondary, inserzioni] [robotshop.com](https://www.robotshop.com/products/hiwonder-hiwonder-minihexa-ai-hexapod-robot-with-ai-vision-voice-interaction-support-arduino-programming-sensor-expansion-standard-kit), [openelab.io](https://openelab.io/a/s/products/hiwonder-minihexa-ai-hexapod-robot) (snippet)
- Servo Hiwonder HPD-0127: 23,9 × 12 × 24 mm; 11 g; 7,4-8,4 V; stallo "≥ 1,8 kgf·cm a 7,4 V"; ≤ 0,05 s/60°; stallo ≤ 1 A; corsa 0-280°; ingranaggi in plastica con frizione di protezione; millerighe 40T Ø circa 4,85 mm; cavo senza connettore; 7,65 € IVA inclusa, spedito dalla Cina — [secondary, negozio UE] [openelab.io/it](https://openelab.io/it/products/hiwonder-hpd-0127-dual-axis) (riassunto con citazioni). La pagina non dice che è il servo del miniHexa: l'abbinamento viene dall'inserzione RobotShop.
- Lunghezze delle zampe: **NON TROVATO**.

**SmallpTsai hexapod-v2-7697 (18 servo, PLA, open source GPL)** (testo letto)
- "there are total 18 Servo motors (TowerPro MG92B)"; "2S Lipo battery (7.4v)"; 7 regolatori mini360: uno a 5 V per il microcontrollore, sei per le zampe (uno ogni 3 servo; il README dice 6 V, la distinta elettronica dice "adjust to 5V": disaccordo interno); corpo in PLA su Prusa i3 MK2S — [community, autore] [README](https://github.com/SmallpTsai/hexapod-v2-7697), [electronics/README.md](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/electronics/README.md)
- Geometria: attacchi zampa a (±29,87, 0) e (±22,41, ±55,41) mm; `kLegRootToJoint1 = 20.75`, `kLegJoint1ToJoint2 = 28.0`, `kLegJoint2ToJoint3 = 42.6`, `kLegJoint3ToTip = 89.07` — [community, autore] [software/pathTool/src/config.py](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/software/pathTool/src/config.py), [config.h](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/software/hexapod7697/src/hexapod/config.h)
- Posa di riposo: femore alzato di 30°, tibia a 15° dalla verticale: `STANDBY_Z = kLegJoint3ToTip*COS15 - kLegJoint2ToJoint3*SIN30`; zampe d'angolo a 45° (`defaultAngle = -45, 0, 45, 135, 180, 225`) — [community, autore] [config.py](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/software/pathTool/src/config.py)
- Limiti di giunto: `angleLimitation = ((-45, 45), (-45, 75), (-60, 60))` gradi (coxa, femore, tibia) — [community, autore] [config.py](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/software/pathTool/src/config.py)
- Andatura in avanti: semicerchio con `g_radius = 25` (passo 50 mm, alzata 25 mm), `g_steps = 20`, due terne di zampe sfasate di mezzo ciclo — [community, autore] [path/forward.py](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/software/pathTool/src/path/forward.py), [path/lib.py](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/software/pathTool/src/path/lib.py)
- "The dimension of 3d printed part is highly depended on servo's dimension. Modification is required if you want to use other alternative servo" — [community] [mechanism/BOM.md](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/mechanism/BOM.md)
- Viteria: 54 viti M2×6, 24 M2×10, 36 M2×30, 36 dadi M2, 18 spine inox M4×6 (una per servo, perno opposto all'albero) — [community] [mechanism/BOM.md](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/mechanism/BOM.md)
- Massa totale: **NON TROVATO**.

**VEB4697 hexapod-MG90S (derivato dal precedente)**
- "MG90S servos used in Hexapod v1 frequently fail due to their inherent weaknesses and inconsistencies in quality"; "It is strongly recommended to start with Hexapod v2 rather than building Hexapod v1" — [community, autore] [README](https://github.com/VEB4697/hexapod-MG90S) (riassunto con citazioni)
- La v2 usa 18 servo da 21 g ("DS Power or Miuzei 21G servo"), 2 celle 18650, 18 cuscinetti MR74-2RS, 18 spine M4×6, 36 viti M2×6, 198 viti M2×10, 234 dadi M2 — [community] [README](https://github.com/VEB4697/hexapod-MG90S) (riassunto)

**Vorpal The Hexapod (12 servo MG90, 2 per zampa, stampato in 3D)**
- Servo "Vorpal MG90" (prodotto da Tower Pro, meccanica identica all'MG90S): 13,4 g; 22,8×12,2×28,5 mm; stallo 1,8 kg/cm (4,8 V), 2,2 kg/cm (6,0 V); 4,8-6,6 V — [primary di Vorpal] [Vorpal MG90 Micro Servo](https://vorpalrobotics.com/wiki/index.php/Vorpal_MG90_Micro_Servo) (testo letto)
- Servo alimentati a 5,0 V nominali da un regolatore che richiede almeno 6,5 V in ingresso — [primary] [Battery Recommendations](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations) (testo letto)
- Assorbimento con 12 servo: "typically draws about 2 to 2.5 Amps", "at most about 3 Amps during short surges" — [primary] [stessa pagina](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations)
- **Peso della batteria**: "The weight of the batteries is also critical. The heavier the batteries, the more stress is put on the servos. The maximum weight of batteries should be no more than 200 to 250 grams. Note that the 2x18650 setup that comes with our kits weigh about 110 grams." — [primary] [stessa pagina](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations)
- Carico utile: circa 100 g di accessori ("three to four ounces"); il robot "is not built to carry heavy weight" — [primary] [Vorpal User Guide](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_User_Guide) (snippet)
- Autonomia con 2×18650 da 3000 mAh: 80 minuti fino al primo spegnimento, fino a 110 — [primary] [Battery Recommendations](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations)
- Riposo dei servo: "it is best to let the servos 'rest' after several minutes of vigorous activity, you shouldn't run the robot full-out for two hours" — [primary] [stessa pagina](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations)
- Un MG90S genuino "will typically require rubber washers on the axles to stop 'hunting'" — [primary] [Vorpal MG90](https://vorpalrobotics.com/wiki/index.php/Vorpal_MG90_Micro_Servo)
- Massa totale e lunghezza delle zampe: **NON TROVATO** (due ricerche e quattro pagine wiki).

**Altri riferimenti**
- "Hexapod Mochi" (MakerWorld): 18 gradi di libertà, ESP32, servo MG92B — [community] [makerworld.com/en/models/1822096](https://makerworld.com/en/models/1822096) (snippet; la pagina risponde 403)
- DYOR "Screwless 3D printable hexapod" (Universitat Politècnica de València): 12 SG90 + 1, tripode; "Designed to be light because of the restrictions that the smallest of the comercial microservos, the TowerPro SG90, has, with the battery and the 5000mAh 2A powerbank it weights only half a kilogram" — [secondary] [dyor.webs.upv.es](https://dyor.webs.upv.es/?p=4606) (testo letto)
- ArcBotics Hexy (19 servo 9 g in plastica): "Use either 4xAA Alkalines or 5xAA NiMH. 4xAA NiMH is also okay. 5xAA alkalines can fry servos" — [primary] [user-guide-hexy.pdf](https://cdn.robotshop.com/media/a/arc/rb-arc-02/pdf/user-guide-hexy.pdf) (testo letto). Massa e zampe: NON TROVATO.
- repBug (stampato, micro servo HXT900 da 9 g): stima dell'autore "skeleton ... 10 g per leg" di parti stampate — [community] [RobotShop Community](https://community.robotshop.com/robots/show/repbug-3d-printed-hexapod) (snippet)
- "18 DOF High-Flotation Hexapod" (Hackaday, SG90 / MG90): nessun dato di massa né prova di cammino — [community] [hackaday.io/project/10131](https://hackaday.io/project/10131) (riassunto)

**Casi di insuccesso**
- 18 Tower Pro SG90, LiPo 2S 1000 mAh, regolatore: "the legs are moving properly when I hold it in the air, but when I put it in the ground. The legs just stall and not moving" — [community] [forum SparkFun](https://community.sparkfun.com/t/question-about-the-power-supply-for-hexapod/34538) (testo letto)
- Esapode ANU, 18 servo standard, 1,5 kg, 420 mm: "The servos have insufficient torque to support the weight of the hexapod on 3 legs"; cammina solo con ciclo 5/6 (cinque zampe a terra) — [community, autore] [mso.anu.edu.au](https://www.mso.anu.edu.au/~ian/Hobby/Hexapod) (testo letto)

**Fuori taglia (solo per la posa)**
- Capers II: 18 Hitec HS-645MG, SSC-32U, NiMH 6 V 2800 mAh, cuscinetti flangiati 3×8 mm sulla coxa; posa neutra con femore orizzontale e tibia a 15° dalla perpendicolare verso l'interno — [community] [Instructables](https://www.instructables.com/Capers-II-a-Hexapod-Robot/) (testo letto)

### Inferences
- **Freenove, posa di marcia** [computed dai valori del codice]: piede della zampa media a 115 − 49 = 66 mm dall'asse coxa, cioè a 66 − 22,75 = **43,25 mm** in orizzontale dall'asse del femore; zampa d'angolo √((81−35)² + (99−50)²) = 67,2 mm → 44,5 mm. Asse femore a 15,75 + 15 = **30,75 mm** dal suolo; luce a terra del corpo 15 mm; femore a circa 45° sopra l'orizzontale, angolo interno al ginocchio circa 48°, tibia quasi verticale (braccio al ginocchio 4,6 mm).
- **Freenove, carico** [computed]: nel tripode i piedi d'angolo stanno a 81 mm dalla mezzeria e quello medio a 115 mm → N_medio = W·81/(81+115) = 0,413·W; N_angolo = 0,293·W. Coppia al femore della zampa media a metà appoggio = 0,413·W·4,325 = 1,79·W kgf·cm; massimo sull'intera corsa di 42 mm = **1,91·W** kgf·cm (W in kg). Con W = 0,6 kg → 1,15; con 0,82 kg → 1,57 kgf·cm. Un kit commerciale lavora quindi sopra 1 kgf·cm, cioè **oltre il 50 % dello stallo di un MG90S**: non rispetta il margine che l'utente si è dato (e un recensore lo trova debole).
- **SmallpTsai, posa di riposo** [computed]: braccio orizzontale asse femore → piede = 42,6·cos30° + 89,07·sin15° = 36,9 + 23,1 = **59,9 mm**; asse femore a 89,07·cos15° − 42,6·sin30° = **64,7 mm** dal suolo. Piedi a (±138,6, 0) e (±99,3, ±132,3) mm → N_medio = 0,417·W. Coppia massima al femore sull'intera corsa di 50 mm = **2,62·W** kgf·cm: con MG92B a 6 V (stallo 3,5) resta entro il 50 % solo se W ≤ 0,67 kg; raggiunge lo stallo a 1,34 kg.
- **miniHexa** [computed]: un robot commerciale a 18 servo da ≥ 1,8 kgf·cm pesa 0,58 kg con batteria da circa 90-110 g. Il pacco OVONIC da solo (245-259 g) varrebbe il 42-45 % di quella massa.
- Il vincolo Vorpal "batteria non oltre 200-250 g" vale per un robot con 12 servo a 5 V; il pacco OVONIC è al limite superiore o oltre già per quel robot più semplice.
- I progetti a 18 servo "micro" che funzionano o sono in vendita si dividono in due famiglie: robot leggeri (≈ 0,6 kg) con servo da ≈ 1,8 kgf·cm, oppure servo da ≥ 3 kgf·cm. Nessuno combina servo da 1,8-2,2 kgf·cm con una massa vicina a 1 kg.

### Gaps
- Massa totale di Freenove (valore certo), Vorpal, Hexy, SmallpTsai: non pubblicata nelle fonti lette.
- Adeept, SunFounder, "Aecert", "Markwtech": nessun esapode a 18 servo 9 g individuato con dati tecnici (due ricerche senza esito).
- Segnalazioni quantitative di surriscaldamento di MG90S su esapodi (temperature, tempi): non trovate; solo le frasi qualitative di Vorpal e VEB4697.

---

## 2. Metodo di calcolo: coppia statica al femore in andatura a tripode, ripartizione del carico, fattori dinamici e di sicurezza

### Takeaway
Con tre piedi a terra il problema è staticamente determinato: tre equazioni di equilibrio danno i tre carichi senza altre ipotesi. Su un corpo rettangolare con i sei piedi alla stessa distanza dalla mezzeria la zampa media del tripode porta W/2 e le due d'angolo W/4; se il piede medio sta al doppio della distanza laterale dei piedi d'angolo (piedi su un cerchio) ogni zampa porta W/3 a metà appoggio. La coppia al femore è il carico sul piede per la distanza orizzontale piede-asse femore. La regola "W/2 sulla zampa media" non l'ho trovata enunciata in una fonte citabile: discende dall'equilibrio. Le regole empiriche trovate per la coppia continua (20-30 % dello stallo) sono più severe del 50 % dell'utente.

### Cited Findings
- Il tutorial più citato dai costruttori, RobotShop "Robot Leg Torque Tutorial", tratta una zampa a 3 gradi di libertà di un esapode a due file da tre zampe e pone come condizione di stabilità che il baricentro cada dentro il triangolo dei piedi a terra — [secondary] [community.robotshop.com](https://community.robotshop.com/tutorials/show/robot-leg-torque-tutorial) (snippet: la pagina risponde 403 a WebFetch, curl e browser; web.archive.org non è raggiungibile dallo strumento. **Le equazioni NON sono state lette.**)
- Il carico non è uniforme tra le zampe in appoggio: "the supporting force (against gravity) is not uniformly distributed among all the legs in stance phase"; modello a "toppling table" con zampe elastiche N_i = K·L·ε_i e piano del corpo L_i = [x_i y_i 1]·[e1 e2 d]ᵀ, necessario quando i piedi a terra sono più di tre — [primary, articolo scientifico] [Chong et al. 2022, Supplementary Information](https://crablab.gatech.edu/pages/publications/pdf/Chong_et_al_2022_B&B_SI.pdf) (testo letto)
- Esiste un'analisi statica con verifica sperimentale delle forze normali ai piedi di un esapode in tripode — [primary, articolo] [Chinese Journal of Mechanical Engineering 2018, doi 10.1186/s10033-018-0263-0](https://cjme.springeropen.com/articles/10.1186/s10033-018-0263-0) (snippet: il testo reindirizza a un login e non è stato letto)
- Coppia continua sostenibile: "typically 20–30% of stall torque for standard DC servos, higher for advanced designs"; "Never exceed 25% of stall torque for continuous duty"; allo stallo "for more than a fraction of a second will overheat and damage the servo"; usare lo stallo come coppia continua: "Servo overheats and demagnetizes within minutes". Fattore di sicurezza: "Add a minimum safety factor of 2.5" per uso hobbistico, 4,0 per uso professionale; "Always design to 3–5 times your calculated static torque under ideal conditions" — [secondary: blog di un produttore di servo, articolo del 26-04-2026 senza autore; regola empirica, non una norma] [kpower.com, "Servo Load Capacity Analysis"](https://www.kpower.com/insight_servo/7642.html) (riassunto con citazioni)
- Regola empirica "continuous torque is approximately 1/3 to 1/5 of stall torque" — [community, post del 2005] [archivio CAD_CAM_EDM_DRO](https://buildbotics.com/archive/cad_cam_edm_dro/messages/79264.html) (snippet)
- Un secondo articolo Kpower suggerisce stallo ≥ 1,5 × coppia calcolata (carico ≈ 67 % dello stallo) — [secondary] [kpower.com](https://www.kpower.com/insight_driver/7325.html) (snippet)
- Rapporto dichiarato da un produttore: Feetech FS90MG "Peak stall torque: 2.2 kg.cm @ 6 V; Rated torque: 0.7 kg.cm @ 6 V" → nominale = 32 % dello stallo — [secondary, inserzione] [RobotShop EU](https://eu.robotshop.com/products/feetech-9g-digital-servo-22kg-cm-fs90mg) (snippet)
- Stallo MG90S: "Stall torque: 1.8kg/cm (4.8V); 2.2kg/cm (6.6V)", "Operating voltage: 4.8V" — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/) (testo letto). Vorpal riporta 2,2 kg/cm a 6,0 V — [primary di Vorpal] [Vorpal MG90](https://vorpalrobotics.com/wiki/index.php/Vorpal_MG90_Micro_Servo). Il datasheet di un clone (Sky Star) dà 2,0 kgf·cm a 6,0 V secondo le note `servo_mg90s.md` — [primary del clone, non riletto da me] [tinytronics.nl PDF](https://www.tinytronics.nl/product_files/000263_Data%20Sheet%20of%20MG90S%20Analog%20Servo%20Motor.pdf). **Disaccordo non risolto**: a 6,0 V lo stallo vale 2,0, 2,07 (interpolazione Tower Pro) oppure 2,2 kgf·cm secondo la fonte.

### Inferences (metodo, tutto [computed])
1. **Carichi sui piedi.** Piedi a terra in (x_i, y_i), baricentro in (x_G, y_G), peso W:
   ΣN_i = W;  ΣN_i·x_i = W·x_G;  ΣN_i·y_i = W·y_G.
2. **Tripode su corpo allungato**, baricentro al centro: due piedi dello stesso lato a distanza laterale s dalla mezzeria, il piede medio del lato opposto a distanza s_m:
   N_medio = W·s/(s + s_m);  N_ant + N_post = W·s_m/(s + s_m).
   s_m = s → N_medio = W/2 (corpo rettangolare, piedi allineati); s_m = 1,5·s → 0,40·W; **s_m = 2·s → W/3** (equivale ai piedi su un cerchio a 120°).
3. **Effetto dell'avanzamento.** Se il corpo avanza di d rispetto al centro della corsa e i piedi d'angolo distano ±a in longitudinale: N_ant − N_post = W·d/a; il carico sul piede medio non cambia. Per un triangolo equilatero di raggio R: N_i = W/3·(1 + 2·(p·u_i)/R), con p spostamento del baricentro e u_i versore verso il piede i. Con R = 120 mm e d = 20 mm il piede più carico sale da 0,333·W a 0,43·W: **il vantaggio del layout circolare a fine corsa è minore di quanto suggerisce W/3**.
4. **Coppia al femore (asse orizzontale):** T_femore = N · x_f, con x_f = distanza orizzontale tra asse del femore e punto di contatto del piede, nel piano della zampa. Il peso proprio della zampa la riduce di poco (trascurarlo è prudente). Dipende solo dalla posizione del piede, non dalle lunghezze dei segmenti.
5. **Coppia al ginocchio:** T_tibia = N · (distanza orizzontale ginocchio-piede). Con tibia verticale è zero.
6. **Coppia alla coxa (asse verticale):** nulla per carichi verticali su suolo piano; resta quella di attrito e spinta. Il momento flettente N·(L_coxa + x_f) va portato dal perno o dal cuscinetto della coxa, non dal servo.
7. **Criterio dell'utente:** T ≤ 0,5·T_stallo. MG90S: 0,90 kgf·cm a 4,8 V; a 6,0 V 1,00 (stallo 2,0), 1,03 (2,07) oppure 1,10 (2,2). A 5,0 V, interpolando Tower Pro: stallo 1,8 + 0,4·(5,0−4,8)/(6,6−4,8) = 1,84 → limite 0,92.
8. **Come leggere il 50 %:** è 2 volte la coppia statica (fattore 2,0), più basso del fattore 2,5 minimo citato da Kpower e ben sopra la soglia del 20-30 % per servizio continuo. Va quindi inteso come limite di picco statico in appoggio; una posa tenuta a lungo (robot fermo in piedi) dovrebbe stare sotto il 25-30 % oppure il robot va fatto sedere.
9. **Coppia massima sull'intera corsa** (carico e braccio variano insieme: quando un piede d'angolo è più carico è anche più vicino al corpo). Ho calcolato T_max/W, in kgf·cm per kg di robot, con coxa 28 mm e passo 40 mm:

   | x_f a metà appoggio | Esagonale regolare (assi coxa su raggio 60 mm) | Corpo allungato (angoli a (±70, ±42) orientati a 40°, medie a (0, ±62)) |
   |---|---|---|
   | 15 mm | — | 0,77 |
   | 18 mm | — | 0,88 |
   | 20 mm | 0,86 | 0,96 |
   | 25 mm | 0,99 | 1,14 |
   | 30 mm | 1,13 | 1,33 |
   | 35 mm | 1,27 | — |
   | 40 mm | 1,43 | — |

   Per confronto, stesso calcolo: Freenove 1,91; SmallpTsai 2,62. Massa massima = limite di coppia / (T_max/W).

### Gaps
- Equazioni del tutorial RobotShop: pagina non leggibile con nessuno strumento disponibile.
- Nessuna fonte citabile per "la zampa media porta metà del peso": è un risultato dell'equilibrio (punto 2).
- Fattore dinamico per l'impatto del piede e l'accelerazione del corpo in un esapode piccolo: NON TROVATO.

---

## 3. Massa di ogni componente

### Takeaway
I due blocchi che contano sono i 18 servo (241 g) e la batteria (245-259 g ± 20 g): insieme circa 500 g su un totale stimato di 0,83-0,98 kg. Scheda SSC-32, scheda ESP32-S3-CAM, camera, viteria e telaio non hanno una massa affidabile in letteratura: vanno pesati.

### Cited Findings
| Componente | Massa | Fonte |
|---|---|---|
| Tower Pro MG90S | 13,4 g (×18 = 241,2 g [computed]) | [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/) (testo letto) |
| OVONIC 2S 5200 mAh 50C hardcase, Deans | "245g/0.54lb for one battery" (dev. 20 g); 137×46×24 mm (dev. 5/2/2 mm) | [primary] [us.ovonicshop.com](https://us.ovonicshop.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-2pcs-lipo-battery) (riassunto con citazioni) |
| idem, altra inserzione | 259 g (dev. 20 g); 138×46×24 mm; 25,17 € | [secondary, negozio Ampow] [ampow.com](https://www.ampow.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-lipo-battery) (riassunto) |
| idem, confezione da 2 | "253g (0.51lb) per pack"; 139×47,3×25,4 mm | [secondary] [ampow.com, 2 pack](https://www.ampow.com/products/2-x-ovonic-2s-50c-5200mah-7-4v-hardcase-lipo-battery-with-dean-t-connector-lipo-voltage-checker-for-1-10-scale-car-truck) (riassunto) |
| Lynxmotion SSC-32U (scheda) | massa non indicata nel manuale; dimensioni 3,00" × 2,30" (76,2 × 58,4 mm), fori Ø 0,125" a 0,15" dai bordi | [primary] [SSC-32U user guide](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf) (testo letto) |
| Lynxmotion SSC-32U | "Item weight: 0,08 kg", peso di spedizione 0,20 kg | [secondary] [mybotshop.de](https://www.mybotshop.de/Lynxmotion-SSC-32U-Servocontrollerboard_1) (snippet) |
| Clone "SSC32-V2.5" (Glayent) | "peso articolo 61 grammi", unità di vendita 71 g, 9×7×3 cm | [secondary] [amazon.it B0FM8S6W59](https://www.amazon.it/dp/B0FM8S6W59) (testo letto dal ricercatore SSC-32; articolo non disponibile) |
| Scheda ESP32-S3-WROOM CAM | NON TROVATO un valore affidabile: un'inserzione Freenove FNK0085 dà 0,068 kg (peso di spedizione) | [secondary] [bigamart.com](https://bigamart.com/?p=10540591) (snippet) |
| Modulo OV3660 | NON TROVATO | — |
| Hobbywing UBEC 10A (2-6S), cod. 30603000 | 36 g; 43,1×32,3×12,5 mm; ingresso 6-25,2 V; uscita 5,0/6,0/7,4/8,4 V; 10 A continui, 20 A picco | [primary] [hobbywing.com](https://www.hobbywing.com/en/products/ubec-10a-2-6s152) (snippet) |
| Hobbywing UBEC 10A V2 Car, cod. 30603003 | 34 g cavi inclusi; 45×20×16,2 mm; uscita 6,0/7,4/8,4 V; 10 A continui, 15 A picco | [primary, negozio del produttore] [hobbywingdirect.com](https://www.hobbywingdirect.com/collections/ubec/products/ubec-10a) (snippet) |
| Hobbywing UBEC 10A HV, cod. 30608000 | 35 g; 55×25×12 mm; ingresso 3-14S: **non adatto a un 2S** | [primary] [hobbywing.com](https://www.hobbywing.com/en/products/ubec-10a-hv289.html) (snippet) |
| YPG (ex YEP) 20A HV UBEC 2-12S | 42 g; PCB 57×26 mm; uscita 5/5,5/6/7/9 V | [secondary] [flyingtech.co.uk](https://www.flyingtech.co.uk/product/ypg-20a-hv-2-12s-ubec-with-selectable-voltage-output-5-0v-5-5v-6-0v-7-0v-9-0v/) (snippet) |
| Cuscinetto 623ZZ (3×10×4) | circa 1,66 g | [primary] [NSK](https://www.oss.nsk.com/623zzmc5-apn.html) (snippet) |
| Cuscinetto 693ZZ (3×8×4) | circa 0,83 g (NSK); 0,4 g secondo un'inserzione FBJ: disaccordo | [primary] [NSK](https://www.oss.nsk.com/products/bearings/ball-bearings/deep-groove-ball-bearings/extra-small-ball-bearings-and-miniature-ball-bearings-metric-series/693zzmc3-apn.html); [secondary] [abf.store](https://www.abf.store/s/en/bearings/693ZZ-FBJ/674842) (snippet) |
| Cuscinetto MR105ZZ (5×10×4) | 1,26 g (aperto MR105: 0,91 g) | [secondary, catalogo distributore] [Albeco](https://old.albeco.com.pl/data/catalogueb/miniaturowe.pdf) (snippet) |
| Cuscinetto MR63 aperto (3×6×2) | 0,20 g (MR63ZZ largo 2,5 mm: NON TROVATO) | [secondary] [Albeco](https://old.albeco.com.pl/data/catalogueb/miniaturowe.pdf) (snippet) |
| Cuscinetti F693ZZ flangiato, MR74-2RS | NON TROVATO | — |
| 2×18650 con portabatterie (confronto) | circa 110 g | [primary] [Vorpal](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations) (testo letto) |
| Parti stampate per zampa, micro esapode | circa 10 g per zampa (stima dell'autore di repBug, progetto non finito) | [community] [RobotShop Community](https://community.robotshop.com/robots/show/repbug-3d-printed-hexapod) (snippet) |

### Inferences
- **SSC-32** [computed, stima]: il solo circuito stampato da 76,2 × 58,4 × 1,6 mm in FR4 (1,85 g/cm³) pesa circa 13 g; con circa 100 pin, morsetti e connettori la scheda nuda dovrebbe stare tra 35 e 45 g. I 61-80 g delle inserzioni comprendono con ogni probabilità imballo o cavo. Nel bilancio uso 60 g per prudenza.
- **Viteria** [computed, stima geometrica]: una vite M2×6 a testa cilindrica in acciaio pesa circa 0,3 g (gambo π·1²·6 mm³ × 0,85 + testa Ø3,8×2 mm, 7,85 g/cm³); una M2×10 circa 0,4 g. I progetti di riferimento usano 114 viti + 36 dadi (SmallpTsai) e 234 viti + 234 dadi (VEB4697): 40-120 g.
- **Bilancio di massa preliminare** [computed; le voci "stima" non hanno fonte]:

  | Voce | g |
  |---|---|
  | 18 × MG90S | 241 |
  | Batteria OVONIC (media delle tre inserzioni) | 252 |
  | SSC-32 (stima prudente) | 60 |
  | ESP32-S3-CAM + OV3660 (stima) | 15 |
  | BEC Hobbywing 10 A | 36 |
  | Cablaggio, interruttore, connettori (stima) | 40 |
  | Viteria e perni (stima) | 40 |
  | **Totale senza telaio** | **684** |
  | Con telaio stampato da 150 / 200 / 250 / 300 g | 834 / 884 / 934 / 984 |

  Lo script del progetto `calc/statica_tripode.py` usa 1150 g: è prudente rispetto a questa stima.
- Con un pacco 2S da 2200 mAh (122-136 g) al posto dell'OVONIC il totale scende di 116-130 g: 0,71-0,86 kg.
- Servo + batteria OVONIC = 493 g: più della metà del robot. La batteria da sola pesa quanto i 18 servo.

### Gaps
- Massa reale della scheda "SSC-32 V2.5", della scheda UICPAL ESP32-S3-CAM e del modulo OV3660: da pesare.
- Massa del telaio stampato di un esapode con servo da 9 g: NON TROVATO un valore pubblicato (nessuno dei progetti letti dichiara i grammi di filamento; l'unico dato trovato, 600 g di PLA, riguarda un esapode con servo standard MG996R).
- Non è chiaro se i 13,4 g dichiarati da Tower Pro includano cavo, squadretta e viti.

---

## 4. Con stallo 1,8 kgf·cm a 4,8 V e 2,2 kgf·cm a 6 V e limite al 50 %: che massa e che geometria sono fattibili? Il pacco hardcase da 250-300 g è realistico?

### Takeaway
Sulla carta il vincolo si può rispettare, ma solo con una posa molto raccolta: con il pacco OVONIC (robot da 0,83-0,98 kg stimati) il piede deve stare a 20-29 mm in orizzontale dall'asse del femore a metà appoggio, contro i 43 mm del kit Freenove e i 60 mm del progetto con MG92B. Il pacco hardcase da circa 250 g NON è realistico per questa classe secondo l'evidenza disponibile: l'unico costruttore che dà un numero (Vorpal) pone 200-250 g come massimo su un robot con 12 servo, tutti i riferimenti usano circa 100 g di batteria, e il robot commerciale a 18 servo equivalente pesa in tutto 580 g. Non ho trovato nessuna testimonianza, né positiva né negativa, di un esapode a 18 MG90S con un pacco simile.

### Cited Findings
- Stallo MG90S: 1,8 kg/cm a 4,8 V; 2,2 kg/cm a 6,6 V — [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/) (testo letto)
- Batteria: massimo consigliato 200-250 g, 110 g di serie, su un esapode a 12 MG90 — [primary] [Vorpal](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations) (testo letto)
- Massa OVONIC 5200: 245-259 g ± 20 g — [primary] [us.ovonicshop.com](https://us.ovonicshop.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-2pcs-lipo-battery); [secondary] [ampow.com](https://www.ampow.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-lipo-battery)
- Esapode commerciale a 18 servo da ≥ 1,8 kgf·cm: 0,58 kg con 2×18650 — [secondary] [robotshop.com](https://www.robotshop.com/products/hiwonder-hiwonder-minihexa-ai-hexapod-robot-with-ai-vision-voice-interaction-support-arduino-programming-sensor-expansion-standard-kit) (snippet), [openelab.io/it](https://openelab.io/it/products/hiwonder-hpd-0127-dual-axis) (riassunto)
- Esapode con 12 SG90 e powerbank da 5000 mAh: 0,5 kg, progettato leggero per i limiti del servo — [secondary] [dyor.webs.upv.es](https://dyor.webs.upv.es/?p=4606) (testo letto)
- Kit Freenove a 18 servo: braccio orizzontale femore-piede 43-44 mm, 2×18650 — [primary + computed] [Freenove FNHR](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)
- "MG90S servos used in Hexapod v1 frequently fail" — [community] [VEB4697](https://github.com/VEB4697/hexapod-MG90S)

### Inferences (tutto [computed])
**A. Stima rapida a metà appoggio**: braccio massimo x_f [mm] = 10 · 0,5 · T_stallo / (k · W), con k = quota di peso sul piede più carico e W in kg.

| Massa robot | k = 0,50 (piedi allineati) | k = 0,413 (proporzioni Freenove) | k = 0,333 (piedi su un cerchio) |
|---|---|---|---|
| | 4,8 V (1,8) / 6 V (2,0) / 6 V (2,2) | 4,8 V / 6 V (2,0) / 6 V (2,2) | 4,8 V / 6 V (2,0) / 6 V (2,2) |
| 0,6 kg | 30 / 33 / 37 | 36 / 40 / 44 | 45 / 50 / 55 |
| 0,7 kg | 26 / 29 / 31 | 31 / 35 / 38 | 39 / 43 / 47 |
| 0,8 kg | 22 / 25 / 28 | 27 / 30 / 33 | 34 / 38 / 41 |
| 0,9 kg | 20 / 22 / 24 | 24 / 27 / 30 | 30 / 33 / 37 |
| 1,0 kg | 18 / 20 / 22 | 22 / 24 / 27 | 27 / 30 / 33 |
| 1,1 kg | 16 / 18 / 20 | 20 / 22 / 24 | 25 / 27 / 30 |
| 1,2 kg | 15 / 17 / 18 | 18 / 20 / 22 | 23 / 25 / 28 |

**B. Verifica sull'intera corsa** (più realistica: usa T_max/W della sezione 2, punto 9; coxa 28 mm, passo 40 mm, MG90S a 6 V con stallo 2,0, limite 1,0 kgf·cm): massa massima ammessa = 1000 / (T_max/W) grammi.

| x_f a metà appoggio | Esagonale regolare | Corpo allungato con medie sporgenti |
|---|---|---|
| 18 mm | — | 1140 g |
| 20 mm | 1160 g | 1040 g |
| 25 mm | 1010 g | 880 g |
| 30 mm | 885 g | 750 g |
| 35 mm | 790 g | — |
| 40 mm | 700 g | — |

Con stallo 2,2 kgf·cm le masse aumentano del 10 %; a 5 V (stallo 1,84) diminuiscono dell'8 %; a 4,8 V del 10 %.

- **Con il pacco OVONIC (0,83-0,98 kg)**: esagonale → x_f ≤ 26-32 mm; corpo allungato → x_f ≤ 22-27 mm. Con i 1150 g usati dallo script del progetto: x_f ≤ 20 mm (esagonale) o 18 mm (allungato).
- **Con un pacco da 2200 mAh (0,71-0,86 kg)**: esagonale → x_f ≤ 31-40 mm; allungato → x_f ≤ 26-32 mm.
- **Con la geometria Freenove** (T_max/W = 1,91) il limite del 50 % a 6 V vale solo sotto 1000/1,91 = **520 g**; con quella SmallpTsai (2,62) sotto 380 g con MG90S.
- Una posa con x_f di 18-25 mm tiene il piede quasi sotto l'anca: il poligono d'appoggio si restringe, la coxa lavora su ±23° per un passo di 40 mm (atan(20/(28+20))) e l'effetto del gioco dei riduttori sull'assetto cresce. È una scelta possibile, ma lontana da ciò che fanno i progetti di riferimento.

### Gaps
- Nessuna testimonianza trovata di un esapode a 18 MG90S con pacco hardcase 2S da 5000-5200 mAh.
- La massa reale del robot dell'utente è una stima: telaio non ancora disegnato, tre componenti non pesati.
- Coppia effettiva di un MG90S reale (genuino o clone) rispetto al dichiarato: vedi `servo_mg90s.md`; se è più bassa, tutti i limiti scendono in proporzione.

---

## 5. Opzioni se il margine non si raggiunge (con numeri)

### Takeaway
Tre leve, in ordine di efficacia per euro: (a) batteria più leggera: un 2S da 2200 mAh pesa 122-136 g e ne toglie circa 120; (b) geometria: piede medio più sporgente dei piedi d'angolo, piede vicino alla verticale dell'asse femore, tibia verticale; (c) servo più forti nella stessa classe solo sul femore (6 pezzi). Il Tower Pro MG92B (3,1 / 3,5 kgf·cm a 5 / 6 V, 13,8 g) è la scelta dei progetti che funzionano, ma la sua disponibilità in UE è incerta e NON è dimostrato che entri nella sede di un MG90S. L'EMAX ES09MD (2,6 kgf·cm a 6 V) dà solo il 30 % in più; l'ES08MA II non dà nulla.

### Cited Findings

**(a) Servo alternativi della stessa classe**
| Modello | Stallo (kgf·cm) | Tensione | Dimensioni (mm) | Massa | Millerighe | Fonte |
|---|---|---|---|---|---|---|
| Tower Pro MG90S (riferimento) | 1,8 @4,8 V; 2,2 @6,6 V | "4.8V" | 22,8×12,2×28,5; tabella A 32,5 / B 22,8 / C 28,4 / D 12,4 / E 32,1 / F 18,5 | 13,4 g | 20T o 21T, Ø 4,8-4,9 (controverso, vedi `servo_mg90s.md`) | [primary] [towerpro.com.tw](https://www.towerpro.com.tw/product/mg90s-3/) (testo letto) |
| Tower Pro MG92B | 3,1 @5,0 V; 3,5 @6,0 V | 5,0-6,6 V | 22,8×12×31; tabella A 35 / B 22,6 / C 31 / D 12 / E 31,5 / F 22,8; digitale, doppio cuscinetto, cassa centrale in lega; 0,13 / 0,08 s/60° | 13,8 g | 25T secondo ServoDatabase: **non confermato** da nessun'altra fonte | [primary] [towerpro.com.tw/product/mg92b](https://towerpro.com.tw/product/mg92b/) (testo letto); [secondary] [servodatabase.com](https://servodatabase.com/servo/towerpro/mg92b) (riassunto) |
| Savox SH-0255MGP | 3,1 @4,8 V; 3,9 @6 V | 4,8-6 V | 22,8×12,0×29,4 | 15,8 g | 21T | [secondary] [extremeflightrc.com](https://extremeflightrc.com/products/savox-sh-0255mgp-digital-metal-gear-micro-servo) (snippet) |
| Power HD HD-1810MG | 3,1 @4,8 V; 3,9 @6 V | 4,8-6 V | 22,8×12×29,4 | 16 g | non indicato | [secondary] [pololu.com](https://www.pololu.com/product/1047/specs) (riassunto). Stallo 1400 mA a 6 V. **Fuori produzione presso Pololu.** |
| AGFRC B13DLM V2 | circa 4,5 @8,4 V (valore a 6 V non letto) | 4,8-8,4 V | 22,8×12×29,4 | 16 g | NON TROVATO | [secondary] [rcdrone.top](https://rcdrone.top/products/agfrc-b13dlm-v2-4-servo), [servodatabase.com](https://servodatabase.com/servo/agfrc/b13dlm-v2) (snippet; le due fonti si contraddicono sul tipo di motore) |
| Corona DS-939MG | 2,5 @4,8 V | 4,8-6 V | 22,6×11,4×24,6 | 12,5 g | NON TROVATO | [secondary] [servodatabase.com](https://servodatabase.com/servo/corona/ds-939mg) (snippet) |
| Corona DS939MG-II | 3,6 @4,8 V; 4,0 @6,0 V | — | date uguali alla precedente | 15,1 g | NON TROVATO | [secondary] [servodatabase.com](https://servodatabase.com/servo/corona/ds939mg-ii) (snippet; dati di un database compilato dagli utenti) |
| EMAX ES09MD | 2,3 @4,8 V; 2,6 @6,0 V | 4,8-6 V | 23,0×12,0×24,5 (retailer) o 23,1×11,9×24,4 (database) | 14,8 g | non indicato; la versione HV da 13,5 g è data 21T Ø 4,95 ± 0,05 | [secondary] [servodatabase.com](https://servodatabase.com/servo/emax/es09md), [alofthobbies.com](https://alofthobbies.com/products/emax-es09md-servo-2-6kg-36-11-oz-in-08-sec-14-8-grams) (snippet) |
| EMAX ES08MA II (versione 4,8-6 V) | 1,6 @4,8 V; 2,0 @6,0 V | 4,8-6 V | 23×11,5×24 | 12 g | 15T Ø 3,9 secondo INJORA: non compatibile con le squadrette MG90S | [secondary] [elektronicavoorjou.nl](https://elektronicavoorjou.nl/en/product/emax-es08ma-ii-mini-servo) (snippet); [injora.com](https://www.injora.com/products/emax-es08ma-ii-12g-analog-metal-gear-servo-servo-mount-bracket-for-axial-scx24) (dalle note `servo_mg90s.md`). **Nessun guadagno.** |
| EMAX ES3352 | 2,8 (dal titolo) | — | servo "thin" da ala: forma diversa, non è un ricambio | 12,4 g | — | [secondary] [alofthobbies.com](https://alofthobbies.com/products/emax-es3352-thin-digital-servo-2-8kg-38-88-oz-in-10-sec-12-4-grams) (solo titolo) |
| JX PDI-1109MG | 2,2 @4,8 V; 2,5 @6 V | 4,8-6 V | 23,2×12×25,5 (retailer) o 23,1×11,9×24,9 (database) | circa 10 g | 25T | [secondary] [servodatabase.com](https://servodatabase.com/servo/jx-servo/pdi-1109mg), [rotorama.com](https://www.rotorama.com/product/jx-pdi-1109mg-9g-servo) (snippet) |
| Feetech FS90MG | 2,2 @6 V (picco); nominale 0,7 @6 V | 4,8-6 V | 22,5×12,1×26,7 | 12,5-12,7 g | non indicato; senza cuscinetti | [secondary] [RobotShop EU](https://eu.robotshop.com/products/feetech-9g-digital-servo-22kg-cm-fs90mg), [Maplin](https://pro.maplin.co.uk/products/fs90mg-mini-12-7g-digital-servo-feetech) (snippet). Stallo 800 mA. **Nessun guadagno.** |
| Feetech FT90M / FT90M-FB | 1,8 (dal titolo) | — | — | 13,5 g | — | [secondary] [grobotronics.com](https://grobotronics.com/servo-micro-1.8kg.cm-metal-gears-with-analog-feedback-feetech-ft90m-fb.html?sl=en) (solo titolo). **Nessun guadagno.** |
| Hiwonder HPD-0127 | ≥ 1,8 @7,4 V | 7,4-8,4 V | 23,9×12×24; doppio albero, frizione | 11 g | 40T Ø 4,85 | [secondary] [openelab.io/it](https://openelab.io/it/products/hiwonder-hpd-0127-dual-axis) (riassunto). 7,65 €. Funziona direttamente a 2S ma non dà più coppia. |
| KST, PTK | NON TROVATO (nessun modello di questa taglia nei risultati) | | | | | — |

- **Disponibilità e prezzo MG92B in Europa**: Botland lo segna "discontinued"; Rotorama 13,79 € ma "discontinued"; Hobbyelectronica (NL) 11,95 € ma esaurito; The Pi Hut (Regno Unito, fuori UE) 8 £, disponibile; eBay.de lotto da 5 pezzi a circa 42,93 € da venditore cinese (autenticità non verificabile); l'autore di hexapod-v2-7697 li ha comprati dal venditore eBay "servohorns959", indicato sul sito Tower Pro — [secondary] [botland.com.pl](https://botland.com.pl/en/servos/2976-servo-towerpro-mg-92b-micro.html), [rotorama.com](https://www.rotorama.com/motory/mg92b-digital-servo), [hobbyelectronica.nl](https://www.hobbyelectronica.nl/en/product/mg92b-digital-servo-360-graden/), [thepihut.com](https://thepihut.com/products/towerpro-servo-motor-mg92b-metal-gear), [ebay.de](https://www.ebay.de/itm/284523643205) (snippet, prezzi non verificati alla data); [community] [BOM.md](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/mechanism/BOM.md). Inserzione Amazon.it: **NON TROVATO**. **Disponibilità dell'MG92B genuino in UE a ottobre 2026: incerta.**
- Prezzi e disponibilità in Italia di Savox SH-0255MGP, Corona, AGFRC, EMAX: **NON TROVATO** (non cercati per limite di chiamate).

**(b) Batteria più leggera**
| Pacco | Massa | Dimensioni (mm) | Fonte |
|---|---|---|---|
| OVONIC 2S 5200 mAh hardcase (attuale) | 245-259 g ± 20 g | 137-139 × 46-47 × 24-25 | vedi sezione 3 |
| Gens ace Soaring 2S 2200 mAh 30C, XT60 | 122 g | 104 × 34,5 × 14,5 | [primary, negozio europeo del produttore] [gensace.de](https://www.gensace.de/gens-ace-soaring-2200mah-7-4v-30c-2s1p-lipo-battery-pack-with-xt60-plug-2192.html) (snippet) |
| Gens ace 2S 2200 mAh 45C, connettore T (Deans) | 136 g | 106 × 34 × 19 | [secondary] [racedayquads.com](https://racedayquads.com/products/gea2s220045d-gens-ace-2s-lipo-battery-45c-7-4v-2200mah-w-t-style-connector) (snippet) |
| Gens ace Soaring 2S 1300 mAh 30C | 79 g | 69,5 × 34 × 14,5 | [primary, negozio europeo del produttore] [gensace.de](https://www.gensace.de/gens-ace-soaring-1300mah-7-4v-30c-2s1p-lipo-battery-pack-with-t3-plug.html) (snippet) |
| 2×18650 con portabatterie | circa 110 g | — | [primary] [Vorpal](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations) (testo letto) |
| 2 celle LiFePO4 formato AA | circa 80 g | — | [primary] [Vorpal](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations) (testo letto) |

- Autonomia di riferimento: miniHexa (18 servo, 0,58 kg) dichiara fino a 60 minuti con 2×18650 da 2200 mAh — [secondary] [robotshop.com](https://www.robotshop.com/products/hiwonder-hiwonder-minihexa-ai-hexapod-robot-with-ai-vision-voice-interaction-support-arduino-programming-sensor-expansion-standard-kit) (snippet); Vorpal (12 servo) assorbe 2-2,5 A tipici — [primary] [Vorpal](https://vorpalrobotics.com/wiki/index.php/Vorpal_The_Hexapod_Battery_Recommendations)
- Pacchi Tattu 2S da 1550 mAh: NON TROVATO.

**(c) Andatura**
- Un esapode i cui servo non reggono il corpo su tre zampe può camminare con cinque zampe a terra (ciclo 5/6) — [community] [mso.anu.edu.au](https://www.mso.anu.edu.au/~ian/Hobby/Hexapod) (testo letto)
- Il firmware Freenove prevede 2, 4 o 6 fasi per ciclo (`crawlSteps`): tripode oppure andature con più zampe a terra — [primary] [FNHRBasic.cpp](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)

### Inferences (tutto [computed])
- **Batteria da 2200 mAh (122-136 g) al posto dell'OVONIC (252 g)**: −116…−130 g, cioè −13 % su un robot da 0,9 kg; il braccio ammesso cresce della stessa percentuale (per esempio da 29 a 34 mm nel layout esagonale). Autonomia stimata: miniHexa consuma in media circa 2,2 Ah in un'ora a 7,4 V (2200 mAh / 60 min, dato del venditore); per un robot più pesante assumo 3 A lato batteria → 2200 mAh all'80 % = circa 35 minuti; 5200 mAh = circa 83 minuti; 1300 mAh = circa 21 minuti. Stima grossolana: l'assorbimento reale va misurato.
- **Piede medio più sporgente**: portare il rapporto s_m/s da 1 a 1,5 riduce il carico sulla zampa media da 0,50·W a 0,40·W (−20 %); a 2 lo porta a W/3 (−33 % a metà appoggio, circa −14 % a fine corsa per l'effetto del punto 3 della sezione 2).
- **Tibia verticale / piede sotto il ginocchio**: azzera la coppia al ginocchio; la coppia al femore dipende solo da x_f. Una tibia più lunga alza il corpo senza aumentare la coppia statica, ma aumenta l'effetto delle forze orizzontali (braccio pari all'altezza) e del gioco.
- **Servo da 3,5 kgf·cm solo sul femore (6 pezzi)**: limite 50 % = 1,75 kgf·cm a 6 V. Con T_max/W = 1,33 (allungato, x_f 30 mm) la massa ammessa passa da 750 g a 1315 g; con la posa Freenove (1,91) a 915 g. Costo in massa: +0,4 g per servo con MG92B, +2,4 g con Savox. Il ginocchio resta con MG90S purché la tibia lavori vicino alla verticale.
- **EMAX ES09MD sul femore**: limite 1,3 kgf·cm a 6 V (+30 % sull'MG90S con stallo 2,0); corpo più basso dell'MG90S (24,5 contro 28,5 mm dichiarati): sede diversa.
- **Andatura ripple / wave** (4 o 5 piedi a terra): il carico per piede scende indicativamente verso W/4 - W/5, ma con più di tre appoggi il sistema è iperstatico e la ripartizione dipende dalla cedevolezza delle zampe (modello di Chong et al.); velocità di avanzamento dimezzata o peggio. È un ripiego software a costo zero.
- **Drop-in**: nessun servo più forte è un ricambio diretto verificato. MG92B: quota C 31 contro 28,4 mm e quota A 35 contro 32,5 mm nelle tabelle Tower Pro (lettere non spiegate sulla pagina), millerighe incerto. Savox / Power HD / AGFRC: 22,8×12×29,4 mm, cioè stessa pianta ma circa 1 mm più alti, interasse dei fori delle alette non trovato. Se si vuole tenere aperta l'opzione, la sede del femore va disegnata dopo aver misurato un esemplare reale del servo scelto, con uno spessore per l'MG90S.

### Gaps
- Interasse dei fori delle alette, quota sotto-aletta e millerighe di MG92B, Savox SH-0255MGP, AGFRC B13DLM, Corona DS939MG-II: NON TROVATO in nessuna fonte; serve un esemplare da misurare.
- Prezzi e disponibilità in Italia a ottobre 2026 dei servo alternativi e dei pacchi Gens ace: non verificati sulla pagina del negozio.
- Coppia a 6 V dell'AGFRC B13DLM V2 e dati del JX PDI-933MG: non letti.

---

## 6. Parametri di andatura tipici per esapodi piccoli

### Takeaway
Due riferimenti letti dal codice sorgente. Freenove: passo 42 mm, alzata 20 mm, luce a terra del corpo 15 mm (asse femore a circa 31 mm dal suolo), rotazione 18° per ciclo. SmallpTsai: passo 50 mm, alzata 25 mm, asse femore a circa 65 mm dal suolo. In entrambi la coxa in appoggio lavora su circa ±16-18° e il passo vale 0,34-0,38 volte la lunghezza femore + tibia.

### Cited Findings
- Freenove: `crawlLength = 42` mm, `legLift = 20` mm, `defaultBodyLift = 15` mm, `turnAngle = 18`° — [primary] [FNHRBasic.h](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit) (testo letto)
- Freenove, limiti software: coxa media 135…225° (±45°), coxa d'angolo 90…200° (110°), femore 0…180°, tibia 0…180° — [primary] [FNHRBasic.cpp](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit) (testo letto)
- Freenove, segmenti: coxa 22,75, femore 55, tibia 70 mm — [primary] [FNHRBasic.cpp](https://github.com/Freenove/Freenove_Hexapod_Robot_Kit)
- SmallpTsai: passo 2 × `g_radius` = 50 mm, alzata 25 mm (semicerchio), 20 punti per ciclo; limiti coxa ±45°, femore −45…+75°, tibia −60…+60°; posa di riposo femore +30°, tibia 15° dalla verticale — [community, autore] [forward.py](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/software/pathTool/src/path/forward.py), [config.py](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/software/pathTool/src/config.py) (testo letto)
- SmallpTsai, segmenti: coxa 28, femore 42,6, tibia 89,07 mm — [community, autore] [config.py](https://github.com/SmallpTsai/hexapod-v2-7697/blob/master/software/pathTool/src/config.py)
- Capers II (servo standard): posa neutra con femore orizzontale e tibia a 75° rispetto al femore — [community] [Instructables](https://www.instructables.com/Capers-II-a-Hexapod-Robot/) (testo letto)
- Corsa utile reale di un MG90S spesso inferiore a 180°: limitare a 20-160° — [3rd-meas] [protosupplies.com](https://protosupplies.com/product/servo-motor-micro-mg90s/) (dalle note `servo_mg90s.md`)

### Inferences (tutto [computed])
| Parametro | Freenove FNK0031 | SmallpTsai v2 |
|---|---|---|
| Passo | 42 mm | 50 mm |
| Alzata del piede | 20 mm | 25 mm |
| Asse femore dal suolo | 30,75 mm | 64,7 mm |
| Femore in posa, sopra l'orizzontale | circa +45° | +30° |
| Angolo interno al ginocchio in posa | circa 48° | 75° (tibia a 15° dalla verticale) |
| Piede dall'asse femore (x_f) | 43,25 mm | 59,9 mm |
| Piede dall'asse coxa | 66 mm | 87,9 mm |
| Escursione coxa in appoggio | ±atan(21/66) = ±17,7° | ±atan(25/87,9) = ±15,9° |
| Tibia / femore | 70/55 = 1,27 | 89,07/42,6 = 2,09 |
| Passo / (femore + tibia) | 42/125 = 0,34 | 50/131,7 = 0,38 |

- Per il robot dell'utente, con la posa raccolta imposta dal margine (x_f 18-30 mm, coxa 28 mm), un passo di 40 mm porta la coxa a ±19…±23° in appoggio (atan(20/(28+x_f))).

### Gaps
- Parametri di andatura di Vorpal e miniHexa: non letti.
- Nessuna fonte che dia valori "tipici" in forma di regola.

---

## Cose che solo l'utente può fornire
- **Peso reale** (bilancia con risoluzione 1 g) di: scheda "SSC-32 V2.5"; scheda UICPAL ESP32-S3-CAM con modulo OV3660; pacco OVONIC con cavi e connettore; un MG90S completo di cavo, squadretta e viti; il BEC scelto.
- **Tensione del rail servo** prevista (5,0 V, 6,0 V o altro): cambia lo stallo disponibile dell'8-20 %.
- Se il pacco OVONIC da 5200 mAh è un **vincolo** o se è accettabile un pacco 2S da circa 2200 mAh (122-136 g) per il cammino, tenendo l'OVONIC per le prove al banco.
- Se è accettabile comprare **6 servo più forti** per i femori; in tal caso serve **un esemplare da misurare** (interasse fori alette, quota sotto-aletta, altezza, denti del millerighe) prima di disegnare le sedi.
- **Forma del corpo** preferita: allungata attorno al pacco da 138 mm, oppure esagonale / con zampe medie sporgenti.
- Se è accettabile una **posa raccolta** (piede a 18-30 mm dall'asse del femore) o se si vuole la posa larga dei kit (43-60 mm), che con MG90S richiede un robot sotto circa 0,5 kg.
