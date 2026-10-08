# Dimensionamento: massa, geometria delle zampe, coppie ai giunti

Calcolo riproducibile: `python3 calc/statica_tripode.py` (punto di progetto) e `--scan` (esplorazione).
Ricontrollato in modo indipendente dal verificatore (`research_notes/.../verifica_dimensionamento.md`, sezione "Ricalcolo indipendente": stessi risultati sui casi di riferimento).

## Risultato in breve

Aggiornato l'8 ottobre 2026 dopo la scelta della batteria (D-027).

- Batteria: **OVONIC 2S 2200 mAh 50C, 120 g**, al posto della 5200 mAh da 260 g. Il robot scende da 1,17 a circa 1,01 kg.
- Punto di progetto: **coxa 36 mm, femore 34 mm, tibia 50 mm**, asse del femore a 72 mm da terra, passo 40 mm. A 1,05 kg la coppia massima è 0,89 kgf·cm al ginocchio (44 % dello stallo) e 0,67 kgf·cm al femore (34 %).
- Il vincolo "coppia statica a tripode ≤ 50 % dello stallo" è rispettato con rail servo a 6,0 V da 68 mm di altezza in su. Resta un assetto alto e raccolto: piede a circa 12 mm in orizzontale dall'asse del femore.
- Il margine dipende ancora da massa reale e coppia reale dei servo (i cloni possono dare meno del dichiarato).
- Il femore non si può allungare: a 38 mm la coppia al ginocchio sale di 8–9 punti.

## Scelta della batteria

| | OVONIC 2S 5200 mAh hardcase | **OVONIC 2S 2200 mAh 50C** |
|---|---|---|
| Massa | 245–259 g ± 20 | 120 g ± 20 |
| Ingombro | 137–139 × 46–47 × 24–25 mm | 105 × 33 × 14 mm (tolleranza ±5 / ±2 / ±2) |
| Connettori | T-plug, JST-XH 3 poli | T-plug, JST-XH 3 poli: gli stessi |
| Corrente continua ammessa | 260 A | 110 A, contro 18,7 A di stallo totale |
| Coppia al ginocchio, stesso assetto (h 72, passo 40) | 51 % a 1,20 kg | 44 % a 1,05 kg |
| Autonomia stimata in marcia | 58–125 min | 25–53 min per pacco |

Ragionamento:

- Il vincolo che stringe è la coppia, non l'autonomia: 140 g in meno valgono 6–7 punti percentuali e permettono un assetto meno estremo, con più riserva di estensione della zampa.
- Autonomia: consumo medio lato batteria stimato 2,0–4,3 A (servo 2–4,5 A a 6 V, più logica); con l'80 % della capacità utile sono 25–53 minuti. La batteria si sfila senza attrezzi e il produttore la vende in coppia: con il cambio sono 50–105 minuti.
- Una taglia intermedia (3000–3300 mAh, circa 185 g) darebbe il 50 % di autonomia in più ma riporterebbe la coppia al 47 %: non conviene.
- Stesso marchio e stessi connettori della batteria che hai già: caricabatterie e cavi restano quelli. La 5200 mAh resta utile al banco.
- Il vano si disegna su 112 × 37 × 18 mm con schiuma, così entrano anche pacchi equivalenti di altre marche (Gens ace 2200 mAh: 104 × 34,5 × 14,5 mm, 126 g).

Dati del pacco da 2200 mAh letti sulla pagina del produttore (us.ovonicshop.com) l'8 ottobre 2026; sezione e lunghezza dei cavi non dichiarate.

## Dati di partenza

| Dato | Valore | Stato |
|---|---|---|
| Coppia di stallo MG90S | 1,8 kgf·cm a 4,8 V; 2,0 kgf·cm a 6,0 V (di progetto) | Tower Pro dichiara 2,2 a **6,6 V** (verificato); 2,0 a 6,0 V è il dato del clone Sky Star (verificato sul suo datasheet) |
| Limite 50 % | 1,0 kgf·cm a 6,0 V; 0,92 a 5,0 V | calcolato |
| Massa di progetto | 1,05 kg (bilancio 1,01 kg) | stimata, vedi sotto |

## Bilancio di massa

Rivisto dopo la revisione indipendente (`docs/revisioni/bom-v1-meccanico.md`, rilievo M-07): la prima versione sommava male e mancavano alcune voci.

| Voce | Massa (g) | Stato |
|---|---|---|
| 18 × MG90S | 241 | verificato (13,4 g l'uno, Tower Pro) |
| Batteria OVONIC 2S 2200 mAh | 120 | verificato sulla pagina del produttore (± 20 g) |
| SSC-32 "V2.5" | 45 | stimato: da pesare |
| ESP32-S3-CAM + OV3660 | 14 | stimato: da pesare |
| 2 regolatori servo Pololu D42V110F6 | 30 | verificato (15 g l'uno) |
| Regolatore 5 V logica | 3 | stimato |
| Interruttore | 3 | stimato |
| 2 fusibili con portafusibile | 20 | stimato |
| 2 derivazioni a leva | 6 | stimato |
| 2 condensatori 2200 µF | 8 | stimato |
| Cablaggio di potenza e T-plug | 35 | stimato |
| Prolunghe servo, cavetti logica, traslatore | 30 | stimato |
| Basetta di supporto e strip | 15 | stimato |
| Cicalino di sottotensione | 8 | fonte secondaria |
| 18 cuscinetti e perni | 12 | stimato |
| Viteria, inserti, distanziali | 60 | stimato: si chiude in fase 5 dal modello |
| Cinghie, schiuma, guaina | 12 | stimato |
| Parti stampate strutturali (corpo + 6 zampe) | 300 | stimato: si chiude dal CAD (corpo più corto con la batteria piccola) |
| Cover non strutturali | 45 | stimato: si chiude dal CAD |
| **Totale** | **1007** | |

Servo e batteria fanno 361 g. Le voci stimate valgono 646 g.
Massa di progetto: 1,05 kg. Obiettivo per il CAD: parti stampate ≤ 345 g in tutto. Ogni 50 g in più valgono circa 2 punti percentuali di coppia.

## Metodo

1. Tre piedi a terra: tre equazioni di equilibrio (somma delle forze verticali, momenti attorno ai due assi orizzontali) danno i tre carichi senza altre ipotesi.
2. Il piede in appoggio resta fermo a terra mentre il corpo avanza di ± passo/2: per ogni posizione si calcola la cinematica inversa della zampa nel suo piano.
3. Coppia al femore = carico sul piede × distanza orizzontale piede–asse femore. Coppia al ginocchio = carico × distanza orizzontale piede–asse ginocchio. La coppia statica alla coxa è nulla (asse verticale, forza verticale).
4. Si verifica anche la fase di volo (piede sollevato di 20 mm): raggiungibilità, angolo minimo al ginocchio, corsa dei servo.

Ipotesi: suolo piano, corpo orizzontale, baricentro al centro, nessuna accelerazione; il peso proprio dei segmenti in appoggio non viene sottratto (prudente). Il margine del 50 % copre la dinamica.

## Punto di progetto

| Parametro | Valore |
|---|---|
| Assi coxa (x avanti, y a sinistra) | angoli (±72, ±40) mm; medie (0, ±58) mm |
| Direzione neutra delle zampe d'angolo | 40° dall'asse longitudinale |
| Coxa `Lc` (asse coxa → asse femore) | 36 mm |
| Femore `Lf` (asse femore → asse ginocchio) | 34 mm |
| Tibia `Lt` (asse ginocchio → punta del piede) | 50 mm |
| Piede neutro: distanza orizzontale dall'asse femore | 12 mm |
| Altezza asse femore da terra (assetto di marcia) | 72 mm |
| Passo / alzata | 40 mm / 20 mm |

Le posizioni degli assi coxa sono **provvisorie**: vanno fissate con la disposizione del corpo (vedi sotto) e poi si rilancia il calcolo.

Risultati a 1,05 kg, 6,0 V:

| Grandezza | Valore |
|---|---|
| Carico massimo su un piede | 421 gf (40 % del peso) |
| Coppia massima al femore | 0,67 kgf·cm (34 % dello stallo) |
| Coppia massima al ginocchio | 0,89 kgf·cm (44 % dello stallo) |
| Momento flettente sul perno della coxa | fino a 2,7 kgf·cm: lo portano squadretta e cuscinetto, non il servo |
| Escursioni usate: coxa / femore / ginocchio | ±23° / da −52° a −4° / da 74° a 134° (angolo interno) |
| Margine di stabilità (baricentro–lato del triangolo d'appoggio) | 38 mm |
| Riserva di estensione della zampa in appoggio | circa 6,5 mm |

Sensibilità (coppia massima in % dello stallo a 6,0 V; ultima colonna a 5,0 V):

| Massa | h = 65, passo 40 | h = 68, passo 40 | h = 72, passo 40 | h = 72, passo 30 | h = 75, passo 40 | h = 72, passo 40, 5,0 V |
|---|---|---|---|---|---|---|
| 0,95 kg | 49 % | 46 % | 40 % | 35 % | 35 % | 44 % |
| 1,00 kg | 52 % | 48 % | 42 % | 37 % | 37 % | 46 % |
| 1,05 kg | 54 % | 50 % | 44 % | 39 % | 39 % | 49 % |
| 1,10 kg | 57 % | 53 % | 47 % | 40 % | 41 % | 51 % |

## Dove sta ogni servo (da confermare con uno schizzo 2D come primo passo del CAD)

Con le quote ufficiali del servo la geometria entra in una sola disposizione (rilievo M-05 della revisione):

- **servo della coxa** nel corpo, albero in alto, cuscinetto in basso;
- **servo del femore** nel pezzo "coxa", con il lato lungo verticale e la coda in alto;
- **femore** passivo: due piastre unite da un'anima di circa 6 mm, senza servo;
- **servo del ginocchio** nella tibia, con la coda verso il piede: servo più culla occupano 23,6 mm dei 50 della tibia, ne restano 26,4 per il piedino.

Lo schizzo va controllato nelle quattro pose estreme: femore a −52° e −4°, ginocchio a 74° e 134°.

Controllo preliminare fatto a mano nel piano della zampa (culla = cassa del servo più 2 mm di parete): lo spigolo della culla più vicino all'asse sta a 11,5 mm, sia all'anca sia al ginocchio. L'anima del femore deve quindi stare fra 12,5 e 21,5 mm dall'asse del femore: con 34 mm ci sta un'anima da 6 mm con circa 1,5 mm di gioco per parte. È stretto ma fattibile; ogni millimetro in più di femore costa circa 2 punti di coppia.

Disposizione del corpo: con la batteria da 2200 mAh il vano scende a 112 × 37 × 18 mm e il conflitto con i servo di coxa segnalato dalla revisione (rilievo M-06, pacco da 144 mm lungo quanto la distanza fra le coxe d'angolo) non c'è più. Restano da fissare nel CAD il lato di uscita dei cavi e il verso di estrazione.

## Perché questa geometria

- La coppia non dipende dalla lunghezza dei segmenti in sé ma da quanto il piede e il ginocchio stanno lontani, in orizzontale, dall'asse che li regge. Per questo la zampa lavora quasi "in colonna": femore inclinato verso il basso e l'esterno, tibia che rientra, piede poco fuori dalla verticale dell'anca.
- La larghezza d'appoggio la dà la coxa (36 mm), che non costa coppia al servo.
- Segmenti corti significano anche meno gioco in punta: il gioco angolare del servo si moltiplica per la distanza dal giunto al piede.
- Gli esapodi di riferimento con zampe larghe (Freenove: piede a 43 mm dall'asse femore; SmallpTsai: 60 mm) richiedono, con questa massa, 1,9–2,6 kgf·cm: per questo usano batterie da circa 100 g o servo da 3,5 kgf·cm.

## Limiti e rischi

- **Coppia reale dei servo**: nessuna misura rigorosa pubblicata; i contraffatti possono dare molto meno del dichiarato. Va misurata su uno dei 18 pezzi.
- **Massa**: le voci stimate valgono 646 g su 1007. Si chiude pesando schede e una zampa di prova e leggendo le masse dal CAD.
- **Assetto**: il firmware deve tenere l'asse del femore a 72 mm in marcia (minimo 68). Accucciarsi è possibile da fermi con sei zampe a terra (carico per zampa dimezzato).
- **Corrente**: una zampa caricata al 44 % dello stallo assorbe circa metà della corrente di stallo; tre zampe in appoggio con due giunti caricati ciascuna valgono circa 2,5–3 A continui in marcia, coerenti con la stima di 2–4,5 A della ricerca.

## Leve disponibili se il margine non basta

| Leva | Effetto | Costo |
|---|---|---|
| Servo più forti solo sui 6 ginocchi (Savox SH-0255MG+, 3,9 kgf·cm a 6 V, verificato) | coppia al ginocchio dal 44 % al 23 % | 6 × 22,95 €; corsa 145°; stallo 1,4 A; spessore 2,4 mm sotto le alette e fori a 28,4 mm |
| Passo 30 mm invece di 40 | circa −5 punti | velocità minore |
| Assetto a 75 mm | circa −5 punti | meno riserva di estensione |

La sede dei servo di ginocchio verrà disegnata in modo da poter accogliere anche il Savox (asole da 27,5 a 28,4 mm e spessore removibile), così la prima leva resta aperta senza ridisegnare la zampa.
