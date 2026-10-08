# Progetto meccanico

Stato all'8 ottobre 2026. La **zampa v0** è modellata e verificata in Fusion; il **corpo** è progettato sulla carta (sezione in fondo) ma non ancora modellato.

Terne:

- **robot**: X in avanti, Y a sinistra, Z in alto; z = 0 all'altezza degli assi dei femori; suolo a z = −72 mm in marcia;
- **zampa** (componente `Zampa`): origine sull'asse della coxa a z = 0; X radiale verso l'esterno, Z in alto, Y lungo gli assi di femore e ginocchio;
- posa di riferimento del modello: femore orizzontale (α = 0), tibia verticale verso il basso (γ = 90°).

## Zampa v0 (modellata)

Script: `cad/script/zampa.py` (parti, istanze, giunti), `cad/script/lib_cad.py` (schizzi vincolati), `cad/script/verifica_zampa.py`.

### Architettura

| Parte | Cosa fa | Come si stampa |
|---|---|---|
| `Coxa` | forcella a C attorno al servo della coxa (braccio superiore sulla squadretta, braccio inferiore sul perno) + anima verticale + culla del servo del femore | faccia −Y sul piano |
| `Femore_B` | piastra lato perni con i due perni, più l'anima che la unisce all'altra piastra | piastra sul piano, anima in piedi |
| `Femore_A` | piastra lato squadrette: porta tutta la coppia tra i due giunti, avvitata all'anima con 2 viti M2 in inserti | in piano |
| `Tibia` | culla del servo del ginocchio, coda verso il piede, più stinco e piede | faccia −Y sul piano |

Dentro `Zampa`: 2 servo, 2 cuscinetti F683ZZ, 3 perni Ø3 × 10 (anca, ginocchio, coxa). Il servo della coxa e il suo cuscinetto appartengono al corpo.

Scelte e perché:

- **Servo della coxa** nel corpo, albero in alto, **coda verso l'esterno**: il cavo esce verso l'interno del corpo. Costa una coxa più lunga: l'anima deve stare oltre le alette del servo (raggio 22,9 mm), quindi a x = 24,2 mm.
- **Servo del femore** con lato lungo verticale e **coda in alto**: con la coda in basso o in orizzontale l'anima del femore lo urterebbe.
- **Femore in due pezzi**: una forcella in un pezzo solo non si infilerebbe sull'albero senza tagliare la piastra. Le due squadrette puntano verso il centro del femore; le viti dell'anima stanno a ±4,5 mm dalla mezzeria per non cadere nelle sedi delle squadrette.
- **Coxa in un pezzo**: si infila di lato sulla gondola; la sede della squadretta sul braccio superiore è una scanalatura aperta verso l'estremità libera, da cui entra la squadretta già montata sull'albero.
- **Giunto**: cuscinetto nel fondo della culla (sede profonda 2,2 mm, flangia fuori a battuta); perno forzato nel braccio, infilato per ultimo dall'esterno, sporgente 1,5 mm per poterlo estrarre; un rialzo Ø4,2 × 0,4 tocca solo l'anello interno.
- **Carico assiale**: la spinta del suolo passa dal rialzo del braccio all'anello interno del cuscinetto e al fondo della culla, non all'albero del servo.
- **Cavo del servo**: cavo e vite dell'aletta stanno sulla stessa mezzeria, quindi il cavo non può scendere lungo la parete. Sotto la bugna c'è una **finestra** larga 9 mm: prima si infila la spina JR, poi si cala il servo.
- **Servo nel modello**: posizionato con le alette appoggiate sull'orlo della culla (nello STEP il sotto-aletta è a 18,4 mm, la quota ufficiale è 18,5).
- Nel modello i fori di perni e cuscinetti sono **nominali**: il forzamento si tara con un provino (`perno_foro`, `cus_sede_d`).

### Quote principali (parametri utente)

| Grandezza | Valore | Parametro |
|---|---|---|
| Semilarghezza della zampa lungo Y | 21,8 mm | `zam_semi_larg` |
| Piastra lato squadrette | y da 18,6 a 21,8 | `zy_sq_int`, `arm_sp_sq` |
| Fondo dei servo di femore e ginocchio | y = −12,4 | `zy_srv` |
| Orlo della culla / fondo esterno della culla | y = 6,1 / −15,8 | `zy_orlo`, `zy_fondo` |
| Piastra lato perni | y da −21,8 a −17,0 | `zy_pn_est`, `zy_pn_int` |
| Culla: semilarghezza, lato corto, lato coda | 8,35 / 8,15 / 18,95 mm | `cul_semi`, `cul_corto`, `cul_lungo` |
| Fondo del servo della coxa | z = −7 | `cox_z0` |
| Braccio inferiore della coxa | z da −16,4 a −11,6 | `cz_inf_giu`, `cz_inf_su` |
| Braccio superiore della coxa | z da 24,0 a 27,2 | `cz_sup_giu`, `cz_sup_su` |
| Anima del femore | da 14 a 20 mm dall'asse dell'anca, alta ±7,5 | `fem_web_x0`, `fem_web_sp`, `fem_web_semi` |

Volumi pieni: Coxa 11,8 cm³, Femore_B 6,7, Femore_A 1,9, Tibia 8,0: 28,4 cm³ per zampa. Con PETG-CF e riempimento parziale sono circa 22 g a zampa (stima).

### Verifica con i giunti veri

`G_femore` e `G_ginocchio` sono giunti di rivoluzione "come costruito" dentro `Zampa`. Misurato: α = −(valore di G_femore); γ = 90° − (valore di G_ginocchio).

- Posa di riferimento: nessuna interferenza; piede a (70, 0, −50).
- Scansione α ∈ {−75 … +25}, γ ∈ {55 … 165}: libera ovunque tranne γ = 55° (la tibia tocca l'anima del femore; limite reale circa 62°) e α = −75° con γ ≤ 62° (la tibia arriva sotto la coxa).
- Campo usato in marcia: α da −52° a −4°, γ da 74° a 134° → almeno 12° di margine su ogni lato.
- Limiti impostati nei giunti: α da −70° a +25°, γ da 65° a 160°.

### Da rifinire nella zampa

- Tasche per i dadi quadri M2 sotto le alette (ora ci sono solo i fori passanti).
- Sede della squadretta: ora è una scanalatura a larghezza costante più la sede del mozzo; diventa trapezoidale quando arrivano le misure della squadretta (parametri `sq_*`, tutti da confermare).
- Coxa: è la parte più pesante, va alleggerita; raccordi alla base dei bracci.
- Nervature di schiacciamento nelle culle per stringere il servo senza gioco.
- Guide e ancoraggi dei cavi (il cavo del servo del femore corre sotto la culla verso l'anima; quello del ginocchio risale lungo il femore).
- Piedino in TPU o silicone; forma dello stinco.
- Fermo assiale del perno affidato alla cover (ora solo forzamento).

## Corpo (progettato, non modellato)

### Vincoli

- Assi delle coxe: (±72, ±40) con direzione neutra a 40° dall'asse longitudinale; (0, ±58) a 90°. Provvisori: dopo la disposizione definitiva si rilancia `calc/statica_tripode.py`.
- Attorno a ogni asse di coxa, entro 9 mm di raggio, lo scafo non può esserci alle quote dei bracci (z da −16,9 a −11,2 e da 23,5 a 27,7).
- Batteria bassa e centrale, estraibile senza attrezzi; USB e interruttore raggiungibili da fuori; camera frontale; passaggi ordinati per 18 cavi.

### Disposizione proposta

- **Scafo**: prisma con pianta a ottagono allungato, vertici (±68, ±24) e (±30, ±48), da z = −17 a z ≈ +39. Gli assi delle coxe d'angolo distano 15,7 mm dallo scafo, quelli medi 10 mm.
- **Gondole** (6): la culla del servo della coxa, integrata nello scafo. In terna zampa: x da −8,15 a 18,95, y ±8,35, z da −10,4 a 11,5. Cuscinetto nel fondo, da sotto; finestra del cavo verso l'interno; bugne delle alette a x = −8,4 e 19,2. Sotto la gondola passa il braccio inferiore della coxa: è uno sbalzo, si stampa con supporti (ammessi, D-032).
- **Pila verticale**: fondo da −17 a −15; vano batteria da −15 a 3 (112 × 37 × 18 mm, x da −66 a 46, aperto sul retro); ponte da 3 a 5; SSC-32 con PCB a z ≈ 9–10,6, lato lungo lungo X, così gli header dei due bus guardano uno a sinistra e uno a destra; zona delle spine fino a z ≈ 35,6; coperchio da 37 a 39.
- **ESP32** sopra la striscia centrale della SSC-32 (|y| ≤ 17, libera dalle spine), antenna in avanti sotto un coperchio non caricato, PCB a z ≈ 24.
- **Camera** al centro del frontale, in alto: il flat arriva diritto dal connettore dell'ESP32 (circa 50 mm sui 61,5 disponibili).
- **Regolatori servo** in piedi nei due rigonfiamenti laterali (x ±22, |y| da 32 a 45, z da 5 a 37), uno per lato, vicino a feritoie e lontani dalla batteria.
- **Retro**: pannello di servizio con apertura della batteria, presa USB-C, pulsante dell'interruttore, cicalino.
- **Stampa in tre pezzi**: base (fondo, pareti fino all'orlo delle gondole, vano batteria), ponte, coperchio.

### Punto da approvare: la porta USB

Con la camera davanti e il flat da 75 mm, la scheda ESP32 deve stare entro circa 60 mm dal frontale con l'antenna in avanti: le sue USB-C finiscono a metà corpo, rivolte indietro. Le alternative provate sulla carta (USB sul frontale sotto la camera con il flat a U; scheda di traverso) allungano il frontale di 6–8 mm in altezza o richiedono pieghe del flat. Proposta: **prolunga USB-C da pannello** (maschio–femmina, 15–20 cm, dati) dalla porta "TTL" dell'ESP32 al pannello posteriore. È una voce in più nel BOM (circa 8 €, circa 10 g) e va approvata (D-034).

### Campo visivo della camera

Camera a circa (63, 0, 31). Il ginocchio anteriore, a fine passo in avanti, sta a 42–55° in orizzontale e a circa −33° in verticale: al bordo di un'inquadratura da 120°. Va verificato in fase 6; le leve sono alzare o avanzare la camera.

### Come modellarlo

- Scafo: rettangolo più smussi come lavorazioni, oppure poligono (vedi sotto); svuotamento con `Parte.svuota`.
- Gondole: servono schizzi ruotati di 40° e 140°. Due strade: sistemare `Parte.sk_poligono` (ora dà "schizzo ipervincolato", vedi `CLAUDE.md`), oppure modellare la gondola come componente a sé nella terna della zampa e istanziarla sei volte.
- Assieme: corpo fissato alla radice; sei istanze di `Zampa`, ciascuna con un giunto di rivoluzione al livello radice tra corpo e `Coxa`. I giunti interni alla zampa sono condivisi dalle istanze: per le pose diverse delle sei zampe si usano trasformate per istanza, validate contro i giunti sulla prima.
