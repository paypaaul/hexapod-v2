# Dossier per la passata estetica dell'esapode (9 ottobre 2026)

Repo: `/Users/paul/hexapod-v2` (leggere `CLAUDE.md`, `docs/progetto-meccanico.md`, `docs/decisioni.md` da D-047 a D-059, `docs/BOM.md`; script CAD in `cad/script/` — `corpo.py`, `zampa.py`, `assieme.py`, `lib_cad.py`). Documenti in italiano.
Immagini del modello attuale (aprire con Read): `vista_iso_anteriore.png`, `vista_fianco_sinistro.png`, `zampa_media_dettaglio.png`, `vista_iso_posteriore.png` in questa cartella. Oggi il robot sembra un assemblaggio di staffe: coperchio piatto con lobi tondi, muso a scatola, servo e cavi a vista.

## Indicazioni dell'utente (vincolanti)

- Carta bianca sul design. Stile futuristico ma minimale, pulito, moderno, bello da vedere: un oggetto "cool", non un assemblaggio di staffe.
- Quando estetica e funzione sono in conflitto vince sempre la funzione.
- Cover delle zampe: placche non strutturali, parti separate da stampare in un altro colore e montare sulle zampe (ed eventualmente sul corpo). Coprono servo e cavi e danno un aspetto più moderno. Non portano carico e non limitano l'escursione dei giunti.
- Camera: l'housing della OV3660 è integrato nel frontale del corpo (non un pezzo aggiunto dopo) e guarda in avanti.
- Pulsante d'accensione da pannello Ø12 (corpo sotto il pannello circa 20 mm) sul coperchio. Cicalino di sottotensione (scatola 40 × 25 × 11 con display) sotto il coperchio in coda sopra il T-plug, display visibile da una finestra del dorso, spinotto di bilanciamento staccabile dal retro accanto al T-plug.
- Acquisti: niente componenti in più se evitabili (le viti M3/M2 e gli inserti del BOM ci sono già).

## Terna e quote principali (mm)

Terna del robot: X avanti, Y a sinistra, Z in alto; z = 0 sul piano degli assi dei femori nella posa di riferimento (femore orizzontale, tibia verticale).

Corpo (struttura in PETG-CF, `corpo.py`):
- `Corpo_Base`: tunnel della batteria x da −85,4 a 81, |y| ≤ 27, tetto a z −9,4; baie laterali |y| da 27 a 50, x ±65,5, ripiano a z −31,95…−29,95, pareti delle baie fino all'orlo z +7; sei gondole dei servo di coxa. Fondo della base z −31,95; chiglia sotto il tunnel fino a z −41,4. Ingombro della base con le gondole 235 × 173.
- Assi delle coxe: d'angolo (±80, ±44) con direzione neutra ±30° e ±150°; medie (0, ±48) a ±90°.
- Coperchio attuale (`Corpo_Coperchio`, non strutturale, PETG): dorso da z 28,4 a 30 sopra tunnel e baie, lobi di raggio 22 sopra gli assi delle coxe, gonne laterali sulle pareti delle baie (a 22 mm dagli assi delle coxe), muso da x 81 a 101 con |y| ≤ 20 che scende fino a z −1, finestra Ø17 per la camera. Fissato con 4 viti M3 su colonnine del tetto a (40, ±22,5) e (−56, ±22,5) (inserti a z 28,4). Si toglie verso l'alto. Ha l'apertura di servizio x −20…28, |y| ≤ 17 con uno sportellino (USB-C e pulsanti dell'ESP32) e feritoie sopra i regolatori (x 18…53, |y| 28,5…31,5).
- Sotto il coperchio: SSC-32 x −50,8…22, |y| ≤ 27,5, spine e cavi fino a z ≈ 25; vassoio dell'ESP32 x 26…98,5, ESP32 fino a z 20,9 con il modulo antenna x 55,6…81,1 (sopra l'antenna niente carbonio né metallo); camera: testa 8,5 × 8,5, lente Ø7 con la faccia a x 98,5, asse ottico a z 22,5, campo 120° in diagonale (circa ±54° in orizzontale, ±46° in verticale), il flat da 75 mm esce in alto dalla testa e torna verso il connettore dell'ESP32 (x 40,8…45,2, z ≈ 18); torretta della camera sul vassoio x 82…92,5.
- Coda: vano di coda sopra il tetto (x −85,4…−50,8, z −9,4…28,4), aperto dietro: F1 sul tetto (x −83,4…−61,4, z fino a 5,6), coppia di T-plug sopra (fino a z 14,1), da staccare dal retro a ogni uso; qui va anche il cicalino (x −85,2…−60,2, |y| ≤ 20, z 17,4…28,4). Sportello della batteria sul retro x −87,4…−85,4, z −41,4…−9,4, due viti M3 in basso.
- Baie anteriori: regolatori in piedi, camino d'aria dal ripiano alle feritoie del coperchio. Baie posteriori: Wago in piedi, anse dei cavi dei servo (circa 1,1 m di cavo in più per lato).

Zampe (`zampa.py`; terna della zampa: X verso l'esterno lungo la zampa, Y lungo l'asse del femore, Z in alto, origine sull'asse della coxa all'altezza dell'asse del femore):
- Lc 55, Lf 65, Lt 110. Larghezza della zampa lungo Y da −30,55 a +30,55.
- Coxa: culla del servo del femore (coda in basso), anima verso il corpo che gira fuori dalla gondola (raggio 39,3…44,55 dall'asse), braccio inferiore sotto la gondola con il perno della coxa (Z −38,35…−33,15, nervatura fino a −41,35). Coxa_Ponte: braccio superiore Z 19,6…23,5, mozzo Ø24 sopra la squadretta del servo di coxa, fascetta dei cavi a X 28.
- Femore: due piastre (Femore_A con le squadrette a Y +24,85…+30,55, Femore_B con i perni a Y −30,55…−24,15), teste tonde attorno ad anca (X 55) e ginocchio (X 120), blocco tra le piastre X 76,5…99, Z −2…+20, unito con 4 viti M3.
- Tibia: culla del servo del ginocchio (coda verso il piede) e stinco 12 × 18,9 con finestre, piedino in TPU; punta a Z −110.
- Escursioni: imbardata della coxa ±35° nel modello (firmware ±30°, somma tra zampe vicine ≤ 60°; vicine a contatto a 34° ciascuna verso l'altra); femore α da −49° a +85°; ginocchio γ da 29° a 180°, minimo in funzione di α: α −45 → 54, −40 → 55, −35 → 45, −30…−20 → 46, 0 → 43, +20 → 37, +40 e oltre → 29 (tabella completa in `progetto-meccanico.md`). Assetti di marcia da 130/25 a 70/70 (altezza / distanza del piede), alzata 30.
- Cavi: quelli di femore e ginocchio escono in alto dalle culle (servo del femore sull'asse dell'anca, servo del ginocchio sull'asse del ginocchio), passano sopra il femore (fascetta attorno al femore vicino all'anca), sopra il servo del femore, lungo il ponte fino al mozzo ed entrano sotto il coperchio. Le anse cambiano con α (11…56 mm) e γ (22…40 mm).
- Servo MG996R: 40,7 × 19,7 × 42,9 mm, alette a 4 fori; quelli di femore e ginocchio hanno la faccia esterna (lato squadretta) e il fondo a vista.

## Produzione e limiti

- FlashForge Creator 5 Pro, 256 × 256 × 256, toolchanger a 4 testine, ugelli da 0,4: PLA, PLA-CF, PETG, PETG-CF. Supporti con interfaccia in altro materiale ammessi ma al minimo. Le cover possono essere in un secondo colore (PLA o PETG); sopra l'antenna dell'ESP32 niente carbonio.
- Massa: circa 2730 g attesi contro 2750 di progetto; ogni 100 g in più costano circa 2 punti di coppia al femore (oggi 48–52 % dello stallo al punto di progetto). Le cover devono essere leggere (pareti 1,2–1,6).
- Fissaggi disponibili: viti M3 e M2 con inserti a caldo (già nel BOM), incastri e denti stampati, fascette.

## Strumenti CAD (tutto via script Python nell'API di Fusion)

- `lib_cad.Parte`: `blocco` (rettangolo su un piano principale estruso), `cilindro`, `blocco_obl` (rettangolo inclinato in una terna locale: serve per tagli e smussi inclinati, cioè sfaccettature), `specchia` (specchiature di lavorazioni), `svuota` (guscio a spessore costante da un pieno), con schizzi completamente vincolati e quote come espressioni dei parametri utente. Nella prima versione il guscio "sfaccettato" del corpo era fatto così: pieno → tagli obliqui → svuotamento.
- Raccordi e smussi dell'API (`filletFeatures`, `chamferFeatures`) si possono usare ma non sono ancora provati negli script; loft e sweep sono sconsigliati (difficili da vincolare e da tenere parametrici).
- Ogni parte è un componente; le cover delle zampe vanno nel componente `Zampa` (sei istanze) e devono seguire la parte a cui sono fissate.
