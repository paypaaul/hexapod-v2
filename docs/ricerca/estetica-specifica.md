# Passata estetica: specifica della versione scelta (Kabuto corretto)

Generata il 9 ottobre 2026 dalla sintesi del confronto tra tre concept (giuria di tre giudici). Concept, render e giudizi completi in `estetica.json` e nella cartella `estetica/`. **Da approvare dall'utente prima di modellare.**

## Perché

Tutti e tre i giudici (estetica, funzione, CAD) mettono Kabuto primo, con voto 7. È l'identità più forte e leggibile: un guscio bianco sfaccettato con i lobi perpendicolari alle zampe, la fascia nera sull'asse, la regola "chiaro = armatura, scuro = struttura". È anche il più leggero (+70 g nel concept, +74 g in questa sintesi), quello con meno pezzi (3 per zampa) e il più costruibile con le primitive già provate. I suoi problemi bloccanti sono tutti correggibili.
- Sedi della lama A fuse e teste e rondelle sovrapposte: è un difetto del femore di oggi; si spostano gli inserti del blocco.
- Testa "a scatola": diventa una visiera nera rastremata a 60°.
- Schiniere troppo grande: diventa una ginocchiera a scudo solo sulla culla.
- Fascetta nera sul bianco: va dentro il blocco del femore. Questo risolve anche l'urto, già presente oggi, contro la testa dell'anima da α 74°.
- Retro disordinato: guance e sportello bianco fanno da cornice alla porta.
- Altri: piega dello schiniere che compenetra la tibia (tolta), spina e foro con lo stesso parametro (separati), coda degenere (ora 1 mm oltre il vertice del lobo), massa (ricontrollata con la statica: femore al 49 %).

Gli altri due concept non reggono come base:
- Ciottolo dipende da raccordi API mai provati e pesa +171 g. Ha errori di quota bloccanti: pinne, cicalino nel raccordo, asola e cuffie prigioniere.
- Lamina ha il miglior muso e la miglior coda, ma da lontano resta un robot nero con lamine sparse.

Delle idee di Ciottolo e Lamina ho preso solo quelle che restano nel linguaggio a 60°/45° di Kabuto.

## Innesti dagli altri concept

- Da Ciottolo: lame del femore lunghe da mozzo a mozzo con finestre sui mozzi. Qui le finestre sono esagonali (apotema 11), con le viti delle squadrette a vista e raggiungibili.
- Da Ciottolo: faccia esterna della lama A a filo delle teste M3 (Y 33,55), così la zampa non si allarga. Le zampe vicine toccano a 31,5° invece di 31,7°.
- Da Ciottolo: piedini in TPU arancio come unico accento di colore, senza pezzi in più (voce D9/E3).
- Da Ciottolo: facce in vista stampate sul PEI testurizzato (carapace capovolto, cover a faccia in giù), per avere la stessa grana ovunque.
- Da Ciottolo: teste delle viti M3 modellate come ingombro (Ingombro_Teste_A) prima delle verifiche tra zampe vicine; ingombro del pulsante Rif_Pulsante_12; documento di prova per le funzioni API nuove.
- Da Lamina: valli del carapace a y 56, che nascondono dall'alto le bugne delle slitte dei regolatori (y 50…55,7).
- Da Lamina: coda come pannello di servizio. Due guance bianche ai lati della porta, tettoia del carapace sopra e sportello della batteria bianco sotto chiudono di lato il vano del T-plug e del cicalino.
- Da Lamina: fronte del corpo chiuso dietro la testa da due paratie (|y| 15…28,5), così ai lati del muso non si vede più l'elettronica.
- Da Lamina: casi di controllo dichiarati per ogni verifica e misura della distanza minima con measureMinimumDistance.
- Dai giudici: la fascia nera scende dalla schiena sul viso e diventa una visiera nera che contiene l'occhio; i fianchi della testa sono a 60° fino al mento; ins_blocco_gb spostato; parametri distinti per spina e foro; cicalino aggiunto in pose_corpo; VOLUMI_ATTESI creato (oggi non esiste).

## Come sarà

Il robot avrà un guscio bianco opaco, basso e sfaccettato, con sei lobi esagonali proprio sopra le zampe e uno smusso a 45° tutto intorno. Al centro corre una fascia nera dalla coda alla testa. Contiene lo sportellino dell'USB-C, il pulsante d'accensione e la finestra del display del cicalino. Davanti la fascia scende sul viso e diventa una visiera nera a forma di scudo, larga in alto e stretta al mento, con l'occhio della camera. La incorniciano le due punte bianche del guscio. Sotto il guscio tutto è scuro: scafo, servo, gonne laterali nere. Su ogni lato del femore c'è una lama bianca lunga quanto l'osso, con le punte a esagono e due finestre esagonali sui giunti, da cui si vedono viti e perni. Sul ginocchio c'è uno scudo bianco a punta; lo stinco resta nero e finisce con un piedino arancio, l'unico colore. Dietro, tra due montanti bianchi, si apre la porta di servizio con T-plug, fusibile e spinotto del cicalino, sopra lo sportello bianco della batteria. Il robot pesa circa 75 g in più (circa 2,8 kg) e le zampe si muovono come oggi.

## Specifica

# Specifica: "Kabuto corretto", sintesi della passata estetica (proposta D-060)

Quote in mm. Terna del robot: X avanti, Y a sinistra, Z in alto, z 0 sugli assi dei femori. Terna della zampa: X verso l'esterno, Y verso Femore_A, Z in alto. Posa di riferimento: α 0, γ 90.

Riferimenti:
- conti: `/Users/paul/.claude/jobs/3d86073b/tmp/estetica/sintesi/calc/verifiche.py`, da copiare in `calc/` con D-060;
- render: `/Users/paul/.claude/jobs/3d86073b/tmp/estetica/sintesi/concept.py`.

Le chiamate scritte `p.blocco(...)`, `p.blocco_obl(...)`, `p.cilindro(...)` e `p.specchia(...)` sono quelle di `lib_cad.Parte`, con la firma di oggi.

## 0. Regole comuni

**Colore e funzione.** Una sola regola di colore:
- **bianco** (PETG bianco opaco) = armatura che non porta niente: carapace, guance, lame dei femori, ginocchiere, sportello della batteria;
- **nero** (PETG nero NON caricato) = interfacce: fascia, visiera con l'occhio, gonne, sportellino di servizio;
- **antracite** (PETG-CF) = struttura, invariata: giunti, culle, servo e viti a vista;
- **arancio** (TPU 95A) = solo i piedini.

Sopra l'antenna (x 55,6…81,1) solo PETG non caricato.

**Forma.**
- Due angoli soli: 60° in pianta e nelle sagome (lobi, punte delle lame, finestre dei mozzi, fianchi della testa, punta della ginocchiera) e 45° in sezione (smusso unico del carapace da 6 mm). Nessun raccordo.
- Spessori: pareti del carapace 1,6; cover 1,2; intarsio della fascia 0,6.

**Metodo.**
- Un componente per pezzo. I tagli toccano solo i corpi del componente (`lib_cad`).
- Dopo ogni blocco, in una chiamata a parte: stato, sentinella dei volumi, timeline senza avvisi, nessuna posa pendente.
- Nessuna chiamata oltre i 40 s.

**Acquisti.** Nessuna voce nuova di minuteria. Da approvare solo i colori dei filamenti: E2 in PETG bianco, un PETG nero non caricato, E3 TPU arancio.

## 1. Parametri

### 1.1 Corpo (nuovi, `corpo.py` → PARAMETRI)

| Nome | Espressione | Valore | Commento |
|---|---|---|---|
| car_top | `cor_cop_z + 7.6 mm` | 36 | cima del carapace (6 mm d'aria in più sopra regolatori, cicalino e flat) |
| car_sp | `cor_cop_sp` | 1,6 | pareti del carapace |
| car_smusso | `6 mm` | 6 | smusso unico a 45° del contorno superiore, viso e coda compresi |
| car_lobo_R | `32.3 mm` | 32,3 | lobi esagonali sugli assi delle coxe, raggio ai vertici (vertici a 0°, 60°…) |
| car_lobo_a | `car_lobo_R * cos(30 deg)` | 27,97 | apotema |
| car_valle_y | `56 mm` | 56 | fondo delle valli tra i lobi: copre le bugne delle slitte (y 50…55,7) |
| car_viso_x | `102 mm` | 102 | viso, che sta tra le punte dei lobi anteriori (vertici a x 112,3) |
| car_coda_x | `cor_ang_x + car_lobo_R / 2 + 1 mm` | 97,15 | coda, 1 mm oltre il vertice del lobo posteriore (−96,15): topologia non degenere |
| car_testa_y | `30 mm` | 30 | semilarghezza dei rettangoli di testa e coda nel pieno; gli spigoli stanno 1,9 mm (testa) e 6,1 mm (coda) dentro i lobi |
| car_mento_z | `cor_muso_giu` | −1 | fondo della testa, sotto il vassoio (z 1) |
| car_mento_semi | `9.2 mm` | 9,2 | semilarghezza del mento. A 60° la parete interna resta a \|y\| 7,35, cioè 1,35 mm fuori da mensola e torretta (\|y\| 6) quando il carapace si sfila |
| car_testa_semi | `25.2 mm` | 25,2 | fianchi verticali della testa, 0,96 mm dentro lo spigolo del viso (y 26,16) |
| car_testa_x0 | `cor_vas_x1 + 0.6 mm` | 82,6 | retro della parte bassa della testa (il vassoio arriva a x 82) |
| car_rastr | `60 deg` | 60 | fianchi della testa; la rastremazione arriva a car_testa_semi a z 26,71 |
| car_paratia_y0 | `15 mm` | 15 | paratie dietro la testa, da qui (ESP32 fino a \|y\| 14,15; punta dell'antenna a x 81,1) |
| car_paratia_y1 | `28.5 mm` | 28,5 | fino a qui (fronte del corpo \|y\| ≤ 27; gondola anteriore da \|y\| 30,2 a x 81) |
| car_fascia_semi | `17 mm` | 17 | fascia nera |
| car_fascia_h | `0.6 mm` | 0,6 | intarsio (3 strati da 0,2) |
| car_pozzo_d | `7 mm` | 7 | pozzetti delle viti |
| car_pozzo_D | `9.4 mm` | 9,4 | tubo dei pozzetti |
| car_serv_semi | `16 mm` | 16 | apertura di servizio \|y\| ≤ 16 (prima 17: la fascia resta larga 1 mm ai lati); x da cor_serv_x0 a cor_serv_x1 |
| car_serv_smusso | `6 mm` | 6 | angoli a 45° dell'apertura (ottagono) |
| car_battuta | `1.5 mm` | 1,5 | battuta dello sportellino sotto la pelle |
| car_puls_x | `-40 mm` | −40 | pulsante sull'asse, sopra lo zoccolo XBee della SSC-32 (fino a z 4,7: restano 9,7 mm sotto il corpo da 20) |
| car_puls_d | `12.2 mm` | 12,2 | foro del pulsante Ø12 (B3b) |
| cic_x0, cic_x1 | `-87 mm`, `-62 mm` | | cicalino 25 × 40 × 11 spostato di 1,8 indietro, pin verso la coda |
| cic_semi, cic_z0 | `20 mm`, `17.4 mm` | | |
| car_fin_l, car_fin_semi | `14 mm`, `12 mm` | | finestra del display centrata su (cic_x0 + cic_x1)/2 |
| car_guancia_x0 | `car_coda_x + 3.35 mm` | 100,5 | retro delle guance di coda, 1 mm dentro il lato del lobo posteriore a \|y\| 25,4 |
| car_guancia_x1 | `cor_tun_x0 + cor_sport_sp + 0.2 mm` | 87,6 | fronte delle guance, 0,2 dietro lo sportello della batteria |
| car_guancia_y0, car_guancia_y1 | `25.4 mm`, `cor_tun_semi` | 25,4; 27 | |
| car_guancia_giu | `cor_tetto - 1 mm` | 8,4 (z −8,4) | 1 mm sopra lo sportello, che si sfila sotto |
| car_occhio_x0 | `cor_cam_x + cam_alt + 0.9 mm` | 99,4 | bocca interna dell'occhio, 0,9 davanti alla lente |
| cam_fov_h, cam_fov_v | `54.2 deg`, `46.1 deg` | | semicampo, 120° in diagonale su sensore 4:3 (caso peggiore) |
| car_occhio_marg | `0.8 mm` | 0,8 | margine del campo |
| car_occhio_si | `cam_lente_d / 2 + (car_occhio_x0 - cor_cam_x - cam_alt) * tan(cam_fov_h) + car_occhio_marg` | 5,55 | |
| car_occhio_vi | come sopra con cam_fov_v | 5,24 | |
| car_occhio_se | `cam_lente_d / 2 + (car_viso_x - cor_cam_x - cam_alt) * tan(cam_fov_h) + car_occhio_marg` | 9,15 | |
| car_occhio_ve | come sopra con cam_fov_v | 7,94 | |
| car_bugna_semi, car_bugna_z0 | `11 mm`, `cor_cam_z - 7.5 mm` | 11; 15 | bugna dell'occhio dietro la visiera |

### 1.2 Zampa (nuovi, `zampa.py` → PARAMETRI)

| Nome | Espressione | Valore | Commento |
|---|---|---|---|
| cov_sp | `1.2 mm` | 1,2 | spessore delle cover |
| cov_ap | `14 mm` | 14 | semialtezza delle lame e apotema delle punte esagonali; il femore è ±13 |
| cov_punta | `cov_ap / cos(30 deg)` | 16,17 | raggio delle punte dai centri di anca e ginocchio: lama da X 38,83 a 136,17 |
| cov_fin_ap | `11 mm` | 11 | apotema delle finestre esagonali sui mozzi: teste delle squadrette fino a r 9,75, restano 1,25 mm d'aria |
| cov_yA0 | `zy_A_est + vite_m3_testa_h - cov_sp` | 32,35 | faccia interna della lama A; l'esterna sta a 33,55, a filo delle teste M3 |
| cov_gobba_c | `(fem_blocco_x0 + zam_Lf - fem_blocco_dk) / 2` | 32,75 | centro della gobba dall'anca (X 87,75) |
| cov_gobba_semi | `12.17 mm` | 12,17 | semibase della gobba a Z cov_ap; in cima 8,71 (fianchi a 60°) |
| cov_gobba_z | `fem_blocco_su` | 20 | cima della gobba |
| cov_testa_d | `5.6 mm` | 5,6 | sede sulle teste M3 ISO 4762 (dk 5,32…5,5); da tarare 5,4…5,7 sul provino |
| cov_tubo_D | `7.6 mm` | 7,6 | tubi della lama A attorno alle teste del blocco |
| cov_dist_d, cov_dist_u | `3 mm`, `15.2 mm` | | distanziali della lama A a X 70,2 e 104,8 |
| cov_spina_d, cov_spina_l | `3 mm`, `3 mm` | | spine della lama B |
| cov_foro_spina_d, cov_foro_spina_l | `3.1 mm`, `3.3 mm` | | fori ciechi in Femore_B: gioco nel modello, il forzamento lo dà la stampa (D-056) |
| cov_spina_z | `6 mm` | 6 | |
| gin_punta | `bug_coda` | 38,35 (Z −38,35) | punta della ginocchiera, alla base dello zoccolo |
| gin_lab | `1.8 mm` | 1,8 | labbro sulla cima della parete +X della culla |
| gin_tappo, gin_tappo_p | `cul_fin_lato - 0.4 mm`, `1.6 mm` | 11,6; 1,6 | tappi a rombo nelle finestre della culla |
| vite_m3_testa_d | `5.5 mm` | 5,5 | ingombro delle teste ISO 4762 |
| fem_fascetta_u | `24.5 mm` | 24,5 (X 79,5) | fascetta del femore dentro il blocco |
| fem_fascetta_fondo | `10 mm` | 10 | Z del tunnel della fascetta |

### 1.3 Cambiati
- **`_inserti_blocco`** (difetto di oggi: teste a interasse 5,4 contro dk 5,5, rondelle Ø7 sovrapposte di 1,6):
  - `ins_blocco_gb` da Z 7,5 a 6,0 (`z0 + ' + 1.5 mm'`);
  - `ins_blocco_ga` da 12,9 a 13,4 (`z1 + ' + 0.5 mm'`).
  
  Interasse 7,4: tra le rondelle restano 0,4 mm, tra le teste 1,9. Parete dell'inserto gb dallo smusso basso: 2,3 mm. Inserto ga: 4,5 mm dalla cima del blocco.
- **`cox_fascetta_x`** da 28 a 24 mm: la fascetta del ponte passa sotto il lobo e va montata con la testa di fianco al braccio.
- Restano invariati cor_cop_z (28,4), colonnine, base, vassoio, camera (asse a z 22,5, lente a x 98,5) e la sagoma delle zampe.

## 2. Corpo

### 2.1 Corpo_Carapace: nuovo, sostituisce Corpo_Coperchio. PETG bianco

**Forma.** Pianta: il contorno dell'unione di sei esagoni (R 32,3) sugli assi delle coxe, di un nucleo x −97,15…102 con \|y\| ≤ 30 e di un rettangolo \|x\| ≤ 80 con \|y\| ≤ 56. Semicontorno sinistro, dal centro del viso:

(102; 0), (102; 26,16), (112,30; 44), (96,15; 71,97), (63,85; 71,97), (54,63; 56), (27,68; 56), (16,15; 75,97), (−16,15; 75,97), (−27,68; 56), (−54,63; 56), (−63,85; 71,97), (−96,15; 71,97), (−112,30; 44), (−97,15; 17,76), (−97,15; 0).

Area 27 734 mm², perimetro 786, ingombro 224,6 × 151,9. Viso largo ±26,16, coda ±17,76.

Sezione:
- bordo verticale da z 28,4 a 30, poi smusso 6 × 45° fino alla faccia piana a z 36;
- dopo lo smusso la faccia piana misura 23 143 mm² e ha questi vertici: (96; 27,77), (105,37; 44), (92,69; 65,97), (67,31; 65,97), (58,09; 50), (24,22; 50), …

Testa sotto il carapace (x 82,6…102):
- fianchi verticali a \|y\| 25,2 da z 26,71 a 28,4;
- sotto, fianchi a 60° fino al mento \|y\| ≤ 9,2 a z −1;
- aperta sotto e dietro;
- la parete del viso (x 100,4…102, sotto z 28,4) è la visiera nera (2.3).

**Lavorazioni**, passo `carapace` in due chiamate, con `p = Parte(Corpo_Carapace)`.

*A. Testa (pieno), prima del carapace,* perché i tagli della rastremazione non intacchino i lobi:
1. `p.blocco('z', 'car_mento_z', 'testa', 'car_testa_x0', '-(car_testa_semi)', 'car_viso_x', 'car_testa_semi', 'cor_cop_z - car_mento_z', 1, NUOVO)`.
2. Rastremazione sinistra:
   `p.blocco_obl('x', 'car_testa_x0 - 1 mm', 'rastremazione_s', ('car_mento_semi', 'car_mento_z'), ('car_mento_semi + 10 mm * cos(car_rastr)', 'car_mento_z + 10 mm * sin(car_rastr)'), '-(5 mm)', '50 mm', '-(30 mm)', '0 mm', 'car_viso_x - car_testa_x0 + 2 mm', 1, TAGLIA)`.
   Nel piano 'x' si ha (u, v) = (y, z). b = a ruotato di +90° punta verso l'interno, quindi la parte tagliata è b < 0.
3. `p.specchia([rastremazione_s], 'y', 'rastremazione_d')`.

*B. Carapace pieno (UNISCI), da z cor_cop_z, alto `car_top - cor_cop_z`:*
4. `p.blocco('z', 'cor_cop_z', 'nucleo', '-(car_coda_x)', '-(car_testa_y)', 'car_viso_x', 'car_testa_y', 'car_top - cor_cop_z')`.
5. `p.blocco('z', 'cor_cop_z', 'baie', '-(cor_ang_x)', '-(car_valle_y)', 'cor_ang_x', 'car_valle_y', 'car_top - cor_cop_z')`.
6. Lobo AS, unione di tre rettangoli:
   - `p.blocco('z', 'cor_cop_z', 'lobo_as_0', 'cor_ang_x - car_lobo_R / 2', 'cor_ang_y - car_lobo_a', 'cor_ang_x + car_lobo_R / 2', 'cor_ang_y + car_lobo_a', 'car_top - cor_cop_z')`;
   - `p.blocco_obl('z', 'cor_cop_z', 'lobo_as_60', ('cor_ang_x', 'cor_ang_y'), ('cor_ang_x + 10 mm * cos(60 deg)', 'cor_ang_y + 10 mm * sin(60 deg)'), '-(car_lobo_R / 2)', 'car_lobo_R / 2', '-(car_lobo_a)', 'car_lobo_a', 'car_top - cor_cop_z')`;
   - la stessa a 120°.
7. Lobo MS: le stesse tre lavorazioni centrate su (0; cor_med_y).
8. `p.specchia([lobi AS], 'x', 'lobi_ps')`, poi `p.specchia([lobi AS, MS, PS], 'y', 'lobi_destri')`.

Controllo, in uno script a parte: la faccia a z = car_top ha area 27 734 ± 5 mm² e la pianta misura 224,6 × 151,9.

*C. Smusso:*
9. `p.smussa(spigoli del contorno esterno della faccia z = car_top, 'car_smusso', 'smusso')` (primitiva nuova, B0). È un solo valore: niente punti a due distanze. Controllo: la faccia piana misura 23 143 ± 10 mm².

*D. Svuotamento:*
10. `p.svuota([facce con normale −Z a z = cor_cop_z, faccia con normale −Z a z = car_mento_z, faccia con normale −X a x = car_testa_x0], 'car_sp', 'guscio')`.

Controllo: volume 53 ± 3 cm³. Lo stimo da 216,8 cm³ di pieno e dalle pareti da 1,6.

*E. Unioni (UNISCI), seconda chiamata:*

11. **Parte alta delle gonne (bianca, nascosta dal bordo delle valli).** `p.blocco('z', 'cor_cop_z', 'gonna_alta_as', 'cor_gonna_x0', 'cor_baia_y - cor_gonna_sp', 'cor_gonna_x1', 'cor_baia_y', 'car_top - car_sp - cor_cop_z')`, poi `specchia` su 'x' e su 'y'. La parte nera da z 7 a 28,4 è Corpo_Gonne (2.4).

12. **Paratie dietro la testa.** `p.blocco('z', 'cor_orlo', 'paratia_s', 'cor_tun_x1', 'car_paratia_y0', 'car_testa_x0', 'car_paratia_y1', 'car_top - car_sp - cor_orlo')` e lo specchio su 'y'. Chiudono il fronte del corpo sopra il muro anteriore della base, che arriva a z 7.

13. **Guance di coda.** `p.blocco('z', '-(car_guancia_giu)', 'guancia_s', '-(car_guancia_x0)', 'car_guancia_y0', '-(car_guancia_x1)', 'car_guancia_y1', 'car_top - car_sp + car_guancia_giu')` e lo specchio su 'y'.

14. **Pozzetti.** `p.cilindro('z', 'cor_cop_z', 'pozzo_tubo_a', 'cor_col_xa', 'cor_col_y', 'car_pozzo_D', 'car_top - car_sp - cor_cop_z')`, lo stesso a `-(cor_col_xp)` e gli specchi su 'y'.

15. **Collare del cicalino.**
    - Fianco: `p.blocco('z', 'cic_z0 + 8 mm', 'collare_s', 'cic_x0 - 0.2 mm', 'cic_semi + 0.2 mm', 'cic_x1 + 0.2 mm', 'cic_semi + 1.4 mm', 'car_top - car_sp - cic_z0 - 8 mm')` e il suo specchio.
    - Parete davanti: `p.blocco('z', 'cic_z0 + 8 mm', 'collare_fronte', 'cic_x1 + 0.2 mm', '-(14 mm)', 'cic_x1 + 1.4 mm', '14 mm', stessa altezza)`.
    - Due nervature di schiacciamento da 1 × 0,25 per fianco, a x −80 e −68.
    - Distanze: parete davanti a 0,9 dalle colonnine posteriori, fianchi a 1,1 dai tubi dei pozzetti. Il retro resta aperto per i pin.

16. **Battuta dello sportellino.** `p.blocco('z', 'car_top - 2 * car_sp', 'battuta', 'cor_serv_x0 - 1 mm', '-(car_serv_semi + 1 mm)', 'cor_serv_x1 + 1 mm', 'car_serv_semi + 1 mm', 'car_sp')`, poi il TAGLIA del rettangolo interno x da cor_serv_x0 + car_battuta a cor_serv_x1 − car_battuta, \|y\| ≤ car_serv_semi − car_battuta. Resta un passaggio \|y\| ≤ 14,5 sopra USB-C e pulsanti dell'ESP32.

*F. Tagli (TAGLIA):*

17. **Sede della fascia sul piano.** `p.blocco('z', 'car_top - car_fascia_h', 'sede_fascia', '-(car_coda_x - car_smusso)', '-(car_fascia_semi)', 'car_viso_x - car_smusso', 'car_fascia_semi', 'car_fascia_h', 1, TAGLIA)`.

18. **Sede sullo smusso del viso.** `p.blocco_obl('y', '-(car_fascia_semi)', 'sede_fascia_smusso_viso', ('car_viso_x', 'car_top - car_smusso'), ('car_viso_x - car_smusso', 'car_top'), '-(0.6 mm)', 'car_smusso * sqrt(2) + 0.6 mm', '-(1 mm)', 'car_fascia_h', '2 * car_fascia_semi', 1, TAGLIA)`. b positivo punta dentro il materiale.

19. **Sede sul bordo del viso, a piena parete.** `p.blocco('x', 'car_viso_x - car_sp', 'sede_fascia_bordo_viso', '-(car_fascia_semi)', 'cor_cop_z', 'car_fascia_semi', 'car_top - car_smusso', 'car_sp + 0.1 mm', 1, TAGLIA)`.

20. **Coda.**
    - Sullo smusso: `p.blocco_obl('y', '-(car_fascia_semi)', 'sede_fascia_smusso_coda', ('-(car_coda_x)', 'car_top - car_smusso'), ('-(car_coda_x - car_smusso)', 'car_top'), '-(0.6 mm)', 'car_smusso * sqrt(2) + 0.6 mm', '-(car_fascia_h)', '1 mm', '2 * car_fascia_semi', 1, TAGLIA)`. Qui b positivo punta fuori, quindi la sede è b < 0.
    - Sul bordo: `p.blocco('x', '-(car_coda_x)', 'sede_fascia_bordo_coda', '-(car_fascia_semi)', 'cor_cop_z', 'car_fascia_semi', 'car_top - car_smusso', 'car_fascia_h', 1, TAGLIA)`.

21. **Sede della visiera.** `p.blocco('x', 'car_viso_x - car_sp', 'sede_visiera', '-(car_testa_semi + 1 mm)', 'car_mento_z - 1 mm', 'car_testa_semi + 1 mm', 'cor_cop_z', 'car_sp + 0.1 mm', 1, TAGLIA)`. Toglie la parete del viso e gli ultimi 1,6 mm dei fianchi rastremati: la visiera li sostituisce.

22. **Apertura di servizio (ottagono).**
    - `p.blocco('z', 'car_top - car_sp', 'apertura_a', 'cor_serv_x0', '-(car_serv_semi - car_serv_smusso)', 'cor_serv_x1', 'car_serv_semi - car_serv_smusso', 'car_sp', 1, TAGLIA)`.
    - `p.blocco(… 'apertura_b', 'cor_serv_x0 + car_serv_smusso', '-(car_serv_semi)', 'cor_serv_x1 - car_serv_smusso', 'car_serv_semi', …)`.
    - 4 `blocco_obl` TAGLIA d'angolo. Ognuno ha un lato sulla retta a 45° fra (x1 − 6; 16) e (x1; 10) e va verso l'interno di `car_serv_smusso * sqrt(2) / 2`. Gli angoli del rettangolo così stanno tutti dentro l'ottagono.
    - Vertici dell'ottagono: (−14; ±16), (22; ±16), (28; ±10), (−20; ±10).

23. **Feritoie.** I 10 tagli di oggi (`_x_feritoia(i)`, \|y\| da cor_fer_y − 1,5 a +1,5), solo nella pelle: da `car_top - car_sp`, alti `car_sp`. Stanno fuori dalla fascia.

24. **Pozzetti.** `p.cilindro('z', 'cor_cop_z + cor_cop_sp', 'pozzo_vano_..', x, y, 'car_pozzo_d', 'car_top - cor_cop_z - cor_cop_sp', 1, TAGLIA)` e `p.cilindro('z', 'cor_cop_z', 'pozzo_foro_..', x, y, 'vite_m3_pass', 'cor_cop_sp', 1, TAGLIA)`, nei 4 punti delle colonnine.

25. **Pulsante.** `p.cilindro('z', 'car_top - car_sp', 'foro_pulsante', 'car_puls_x', '0 mm', 'car_puls_d', 'car_sp', 1, TAGLIA)`.

26. **Finestra del display.** `p.blocco('z', 'car_top - car_sp', 'finestra_cicalino', '(cic_x0 + cic_x1) / 2 - car_fin_l / 2', '-(car_fin_semi)', '(cic_x0 + cic_x1) / 2 + car_fin_l / 2', 'car_fin_semi', 'car_sp', 1, TAGLIA)`.

27. **Tacca dell'unghia.** `p.blocco('z', 'car_top', 'tacca', 'cor_serv_x1 + 1 mm', '-(5 mm)', 'cor_serv_x1 + 4 mm', '5 mm', '0.8 mm', -1, TAGLIA)`.

L'occhio si taglia nella visiera e nella fascia (2.2, 2.3). Nel carapace il tronco di piramide non incontra materiale: le sedi 19 e 21 lo hanno già tolto.

**Fissaggio.** Come oggi (D-052): 4 viti M3 × 8 negli inserti delle colonnine. La sede del pozzetto (z 28,4…30) appoggia sulla colonnina: 1,6 di sede più 6,4 nell'inserto. La testa resta da 1,6 a 3 mm sotto la superficie. Le gonne appoggiano sull'orlo delle baie (z 7).

**Togliere il carapace.** Si toglie verso l'alto, come oggi. Prima si staccano lo spinotto di bilanciamento, dal retro, e il Dupont a 2 vie del pulsante (C4). Il cicalino e il pulsante salgono con il carapace.

**Stampa.** Un solo pezzo multimateriale con Fascia, Visiera e Gonne: PETG bianco più PETG nero, sulla Creator 5 Pro.
- Orientamento: capovolto, faccia z 36 sul PEI testurizzato. Ingombro 224,6 × 151,9 × 44,4 (le guance scendono a z −8,4).
- Supporti: nessuno.
  - Ponti: fondo dei pozzetti Ø7 e battuta da 1,5.
  - Occhio: la parete bassa è a 43° dalla verticale.
  - Testa: i fianchi a 60° e lo smusso a 45°, a pezzo capovolto, guardano in alto.
- Cambi di testina: circa 180, negli strati da 1,6 a 37 mm dove ci sono visiera e gonne. Con il toolchanger, da 30 a 60 minuti in più.
- Brim e piatto caldo. Area utile con lo spurgo da confermare (D-050).

### 2.2 Corpo_Fascia: nuovo, PETG nero. Un corpo, intarsio a filo

Corrisponde alle sedi 17–20 del carapace. Lavorazioni:

1. **Piano.** `p.blocco('z', 'car_top - car_fascia_h', 'fascia', '-(car_coda_x - car_smusso)', '-(car_fascia_semi)', 'car_viso_x - car_smusso', 'car_fascia_semi', 'car_fascia_h', 1, NUOVO)`.

2. **Smusso del viso.** `p.blocco_obl('y', '-(car_fascia_semi)', 'fascia_smusso_viso', ('car_viso_x', 'car_top - car_smusso'), ('car_viso_x - car_smusso', 'car_top'), '0 mm', 'car_smusso * sqrt(2)', '0 mm', 'car_fascia_h', '2 * car_fascia_semi')`. Ho verificato in pianta che i tre pezzi coprono la sede senza vuoti.

3. **Bordo del viso, a piena parete.** `p.blocco('x', 'car_viso_x - car_sp', 'fascia_bordo_viso', '-(car_fascia_semi)', 'cor_cop_z', 'car_fascia_semi', 'car_top - car_smusso', 'car_sp')`.

4. **Coda.** `p.blocco_obl` come la sede 20 (a da 0 a `car_smusso * sqrt(2)`, b da `-(car_fascia_h)` a 0) e `p.blocco('x', '-(car_coda_x)', 'fascia_bordo_coda', …, 'car_fascia_h')`.

5. **Fori**, con le stesse espressioni del carapace: apertura ottagonale (22), pulsante (25), finestra (26), tacca (27).

6. **Occhio**, cinque tagli (vedi 2.3, punto 4). Tolgono la parte del tronco fra z 28,4 e 30,44.

In vista: la fascia corre sulla schiena, scende sul viso fino a z 28,4, dove continua nella visiera, e sulla coda fino al bordo sopra la porta.

### 2.3 Corpo_Visiera: nuova, PETG nero. Alloggiamento della camera, integrato nel frontale e stampato insieme al carapace

1. **Lastra.** `p.blocco('x', 'car_viso_x - car_sp', 'visiera', '-(car_testa_semi)', 'car_mento_z', 'car_testa_semi', 'cor_cop_z', 'car_sp', 1, NUOVO)`.

2. **Rastremazione.** Le stesse due lavorazioni del punto A2–A3 del carapace, sul corpo della visiera.

3. **Bugna.** `p.blocco('x', 'car_occhio_x0', 'bugna_occhio', '-(car_bugna_semi)', 'car_bugna_z0', 'car_bugna_semi', 'cor_cop_z', 'car_viso_x - car_sp - car_occhio_x0')`, in UNISCI.

4. **Occhio, tronco di piramide con quattro tagli piani.** È la riserva provata; lo smusso a due distanze non serve.
   - Foro: `p.blocco('x', 'car_occhio_x0', 'occhio_foro', '-(car_occhio_si)', 'cor_cam_z - car_occhio_vi', 'car_occhio_si', 'cor_cam_z + car_occhio_vi', 'car_viso_x - car_occhio_x0 + 1 mm', 1, TAGLIA)`.
   - Pareti laterali: `p.blocco_obl('z', 'cor_cam_z - car_occhio_ve - 1 mm', 'occhio_fianco_s', ('car_occhio_x0', 'car_occhio_si'), ('car_viso_x', 'car_occhio_se'), '-(1 mm)', '6 mm', '-(10 mm)', '0 mm', '2 * car_occhio_ve + 2 mm', 1, TAGLIA)` e lo specchio su 'y'.
   - Pareti alta e bassa: due `blocco_obl` su 'y', con estrusione lungo y da `-(car_occhio_se + 1 mm)` per `2 * car_occhio_se + 2 mm`. Quella alta va da (car_occhio_x0; cor_cam_z + car_occhio_vi) a (car_viso_x; cor_cam_z + car_occhio_ve). Quella bassa è simmetrica rispetto a z = cor_cam_z.

**Geometria dell'occhio.** Bocca interna 11,1 × 10,5 a x 99,4; bocca esterna 18,3 × 15,9 a x 102. Le pareti sono sul campo più 0,8 mm (54,2° e 46,1°).

**Verifica del campo** (verifiche.py, raggi da tutto il bordo della lente Ø7, obiettivo rettilineo 120°):
- margine minimo 0,80 mm;
- lo spigolo fra viso e smusso (102; 30) è a 48,8° in verticale, contro 46,1° di campo;
- le corna (112,3; 44) sono a 71,2°, contro 54,2°;
- la bocca esterna arriva a z 30,44 e intacca lo smusso di 0,44 mm, sopra il campo (accettato);
- le ginocchia anteriori restano al bordo dell'immagine, come in D-057.

**Montaggio della camera.** Invariato: torretta e mensola del vassoio, lente a x 98,5, flat sopra la torretta. La visiera sta a x ≥ 99,4, quindi il carapace si sfila senza toccare la camera. Le pareti dell'occhio, nere, tolgono i riflessi.

### 2.4 Corpo_Gonne: nuovo, PETG nero. 4 corpi

Quattro blocchi NUOVO: `p.blocco('z', 'cor_orlo', 'gonna_as', 'cor_gonna_x0', 'cor_baia_y - cor_gonna_sp', 'cor_gonna_x1', 'cor_baia_y', 'cor_cop_z - cor_orlo', 1, NUOVO)` e gli altri tre (x negative, y negative).

Toccano la parte alta bianca (punto 11) a z 28,4 e appoggiano sull'orlo delle baie. Stanno 6 mm dentro il bordo delle valli, quindi di lato sotto il guscio si vede solo scuro. Volume 3,78 cm³.

### 2.5 Corpo_Sportello_Servizio: rifatto, PETG nero

`fai_sportellino` riscritto:
- lastra a filo, `p.blocco('z', 'car_top - car_sp', 'piastra', 'cor_serv_x0 + 0.2 mm', '-(car_serv_semi - 0.2 mm)', 'cor_serv_x1 - 0.2 mm', 'car_serv_semi - 0.2 mm', 'car_sp', 1, NUOVO)`;
- 4 tagli d'angolo a 45° come il punto 22, spostati di 0,2 verso l'interno;
- 4 nervature di schiacciamento larghe 1 sui lati lunghi, a x 16 e −8, a filo dell'apertura (D-056).

Appoggia sulla battuta e resta su per attrito. Volume circa 2,4 cm³ (4 g). Stampa: faccia in vista sul PEI.

### 2.6 Corpo_Sportello (della batteria): PETG bianco

Geometria e viti invariate (D-054). In più, smusso 1 × 45° sui quattro spigoli esterni della piastra, con `p.smussa`, oppure 4 `blocco_obl` TAGLIA. Insieme alle guance fa la cornice bianca della porta di servizio. Stampa: faccia esterna sul PEI.

### 2.7 Comprati: cicalino e pulsante

**Ingombro del pulsante.** In `rif_componenti.py` si aggiunge l'ingombro `Rif_Pulsante_12`. Origine al centro della faccia superiore del pannello, +Z in alto:
- flangia Ø15 × 2 (z 0…2);
- corpo Ø12 da z −21,6 a 0;
- dado Ø17,3 × 2 da z −3,6 a −1,6.

**Istanze in `assieme.py` → `pose_corpo`:**
- `out['Cicalino'] = ('Rif_Cicalino_BX100', _rz((cic_x0 + cic_x1) / 2, 0, cic_z0, 90.0))`. Il box 40 × 25 × 11 ha il lato da 40 lungo y e i pin verso −X.
- `out['Pulsante'] = ('Rif_Pulsante_12', _rz(car_puls_x, 0, car_top, 0.0))`.

Il cicalino oggi è solo in libreria: va aggiunto. Il pulsante occupa z 14,4…38: a −40 sotto ci sono 9,7 mm sopra lo zoccolo XBee.

## 3. Zampa

### 3.1 Femore_B e Femore_A

**Inserti del blocco.** Nuove posizioni (1.3): Femore_B (inserti) e Femore_A (fori) si rigenerano.

**Fori ciechi per le spine della lama B**, in `fai_femore_b`: `p.cilindro('y', 'zy_B_est', 'foro_spina_a', 'zam_Lc + fem_blocco_x0 + fem_ins_dx', 'cov_spina_z', 'cov_foro_spina_d', 'cov_foro_spina_l', 1, TAGLIA)` e lo stesso a `'zam_Lc + zam_Lf - fem_blocco_dk - fem_ins_dx'`. Sono a X 81 e 94,5, Z 6: nella piastra B e nel blocco, lontani dagli inserti, che stanno sul lato A (Y 20,45…27,15).

**Fascetta del femore dentro il blocco.** D-058 cambia: prima la fascetta da 200 mm girava attorno al femore. Ora è una fascetta corta da 2,5 mm (D11) in due feritoie e un tunnel:
- `p.blocco('z', 'fem_fascetta_fondo', 'feritoia_femore_a', 'zam_Lc + fem_fascetta_u - fascetta_w / 2', 'cox_fascetta_y - fascetta_sp / 2', 'zam_Lc + fem_fascetta_u + fascetta_w / 2', 'cox_fascetta_y + fascetta_sp / 2', 'fem_blocco_su - fem_fascetta_fondo', 1, TAGLIA)`;
- la gemella a \|y\| negative;
- il tunnel: `p.blocco('z', 'fem_fascetta_fondo', 'tunnel_femore', stessi x, '-(cox_fascetta_y + fascetta_sp / 2)', 'cox_fascetta_y + fascetta_sp / 2', 'fascetta_sp', 1, TAGLIA)`.

L'anello sta sullo smusso alto del blocco, fra le piastre: non si vede dai lati e non tocca le cover.

Risolve anche il difetto di oggi (la fascetta a 15 mm dall'anca entra nella testa dell'anima da α 74°). Ad α 85 l'anello sta a X 38,2, Z circa 26: 6 mm sopra la testa dell'anima, 2,5 mm sopra il ponte, fuori dal lobo.

### 3.2 Coxa_Ponte
Si cambia cox_fascetta_x a 24 e si rigenera il ponte. La testa della fascetta va di fianco al braccio. Sotto la pelle del carapace (z 34,4) restano 8 mm.

### 3.3 Ingombro_Teste_A: nuovo, non stampato, 12 corpi

Teste ISO 4762 sul lato A, per verificare le zampe vicine e le sedi della lama. `p.cilindro('y', 'zy_A_est', nome, x, z, 'vite_m3_testa_d', 'vite_m3_testa_h', 1, NUOVO)`:
- 8 sulle squadrette: (xc ± sq_fori_pcd/2; 0) e (xc; ±sq_fori_pcd/2), con xc = zam_Lc e zam_Lc + zam_Lf;
- 4 sul blocco, nelle posizioni di `_inserti_blocco()`.

Volume 855,3 mm³. Va escluso da masse ed esportazioni.

### 3.4 Cover_Femore_A: lama sospesa, PETG bianco

Lastra 1,2 da Y 32,35 a 33,55. La faccia esterna sta a filo delle teste M3, quindi la zampa non si allarga. Sotto resta una fuga d'ombra di 1,8 mm.

Sagoma nel piano X–Z:
- punte esagonali sui mozzi, con vertici a X 38,83 e 136,17;
- lati a Z ±14;
- gobba sopra il blocco, da (75,58; 14) a (79,04; 20), piatta a Z 20 fino a 96,46, poi fino a (99,92; 14).

Due finestre esagonali (apotema 11, vertici lungo X) sui mozzi di anca e ginocchio. Dentro si vedono le 8 teste delle squadrette e il foro d'accesso Ø6.

Lavorazioni, sul piano 'y' a `cov_yA0`, verso +1:
1. Corpo: `p.blocco('y', 'cov_yA0', 'corpo', 'zam_Lc', '-(cov_ap)', 'zam_Lc + zam_Lf', 'cov_ap', 'cov_sp', 1, NUOVO)`.

2. Punte. Per xc in (zam_Lc, zam_Lc + zam_Lf), tre rettangoli:
   - `p.blocco('y', 'cov_yA0', 'punta0_..', xc − cov_punta/2, −cov_ap, xc + cov_punta/2, cov_ap, 'cov_sp')`;
   - `p.blocco_obl('y', 'cov_yA0', 'punta60_..', (xc, '0 mm'), (xc + ' + 10 mm * cos(60 deg)', '10 mm * sin(60 deg)'), '-(cov_punta / 2)', 'cov_punta / 2', '-(cov_ap)', 'cov_ap', 'cov_sp')`;
   - la stessa a 120°.

3. Gobba: `p.blocco('y', 'cov_yA0', 'gobba', 'zam_Lc + cov_gobba_c - cov_gobba_semi', 'cov_ap - 1 mm', 'zam_Lc + cov_gobba_c + cov_gobba_semi', 'cov_gobba_z', 'cov_sp')`.

4. Fianchi della gobba, due `blocco_obl` TAGLIA:
   - fianco verso l'anca: p0 = (zam_Lc + cov_gobba_c − cov_gobba_semi; cov_ap), p1 a +60°, a da 0 a 20, b da 0 a 20;
   - fianco verso il ginocchio: p0 = (… + cov_gobba_semi; cov_ap), p1 a +120°, a da 0 a 20, b da −20 a 0.
   
   Con a0 = 0 i tagli non scendono sotto Z 14.

5. Finestre: per ogni xc, tre TAGLIA come il punto 2, con semiasse `cov_fin_ap / cos(30 deg) / 2` (6,35) e apotema `cov_fin_ap`.

6. Tubi: `p.cilindro('y', 'zy_A_est', 'tubo_..', x, z, 'cov_tubo_D', 'cov_yA0 - zy_A_est')`, nelle 4 posizioni di `_inserti_blocco()`. I due tubi gb e ga si fondono: interasse 7,4 contro Ø7,6.

7. Distanziali: `p.cilindro('y', 'zy_A_est', 'distanziale_anca', 'zam_Lc + cov_dist_u', '0 mm', 'cov_dist_d', 'cov_yA0 - zy_A_est')` e lo stesso a `zam_Lc + zam_Lf - cov_dist_u`.

8. Sedi: `p.cilindro('y', 'zy_A_est', 'sede_..', x, z, 'cov_testa_d', 'cov_yA0 + cov_sp - zy_A_est', 1, TAGLIA)` nelle 4 posizioni.

9. Facoltativo: `p.smussa` 0,6 sul contorno della faccia esterna, se B0 ha provato la primitiva.

Pareti minime:
- dai fianchi della gobba ai tubi: 1,44 mm verso l'anca e 1,19 verso il ginocchio;
- fra i tubi ab e aa: 0,8.

Volume circa 2,20 cm³, 2,8 g.

**Fissaggio.** A pressione sulle 4 teste M3 × 8 del blocco: 3 mm di presa per testa, i tubi poggiano sulla piastra A. Nessuna vite in più. Si toglie tirando. Le viti delle squadrette restano raggiungibili dalle finestre.

**Stampa.** Faccia esterna sul PEI; tubi e distanziali in alto; senza supporti.

### 3.5 Cover_Femore_B: lama appoggiata, PETG bianco

Stessa sagoma, stessa gobba e stesse finestre, sul piano `zy_B_est` verso −1: lastra da Y −30,55 a −31,75, dentro la sporgenza dei perni (−31,95). Nelle finestre si vede la testa del perno, 0,2 mm sopra la lama.

Le spine: `p.cilindro('y', 'zy_B_est', 'spina_..', x, 'cov_spina_z', 'cov_spina_d', 'cov_spina_l', 1)`, a X 81 e 94,5, verso +Y dentro i fori ciechi.

Volume circa 2,19 cm³, 2,8 g. Stampa: faccia esterna sul PEI, spine in alto.

Il lato B ha lo stesso peso visivo del lato A (stessa sagoma bianca, due finestre scure). Le zampe destre e sinistre, che non sono specchiate, da davanti si leggono uguali.

### 3.6 Cover_Tibia: ginocchiera a scudo, PETG bianco

Sostituisce lo schiniere di Kabuto. Sta solo sulla faccia +X della culla del ginocchio, da X 132,45 a 133,65: niente piega sullo stinco, quindi niente compenetrazione.

Sagoma nel piano Y–Z:
- da Y −24,15 a 9,45 e da Z 13,65 in giù;
- lati dritti fino a Z −9,25, poi punta a 60° in (−7,35; −38,35).

Il servo sopra l'orlo resta a vista, come giunto scuro. Area 1258 mm², contro 2280 dello schiniere di Kabuto: la lama del femore torna l'elemento più grande.

Lavorazioni, con xk = `zam_Lc + zam_Lf`:
1. `p.blocco('x', xk + ' + cul_semi', 'piastra', 'zy_fondo_est', '-(gin_punta)', 'zy_orlo', 'cul_corto + cov_sp', 'cov_sp', 1, NUOVO)`.
2. Labbro: `p.blocco('z', 'cul_corto', 'labbro', xk + ' + cul_semi - gin_lab', 'zy_fondo_est', xk + ' + cul_semi + cov_sp', 'zy_orlo', 'cov_sp')`. Sta fuori dalle bugne (X ≤ 128,7) e dalla fessura del cavo.
3. Tappi: `p.blocco_obl('x', xk + ' + cul_semi', 'tappo_1', ('cul_fin_y', '-(cul_fin_z1)'), ('cul_fin_y + 1 mm', '-(cul_fin_z1) + 1 mm'), '-(gin_tappo / 2)', 'gin_tappo / 2', '-(gin_tappo / 2)', 'gin_tappo / 2', 'gin_tappo_p', -1)` e lo stesso con cul_fin_z2. È la stessa chiamata delle finestre di `_alleggerisci_culla`. Dietro il tappo restano 0,6 mm fino al servo.
4. Punta, dopo i tappi (così il taglio rifila anche il tappo basso, 0,25 mm), due `blocco_obl` TAGLIA:
   - piano 'x' a `xk + ' + cul_semi - gin_tappo_p - 0.5 mm'`, alti `gin_tappo_p + cov_sp + 1 mm`;
   - p0 = ('(zy_fondo_est + zy_orlo) / 2', '-(gin_punta)');
   - p1 a 120° per il lato −Y (b da 0 a 30), a 60° per il lato +Y (b da −30 a 0); a da −5 a 40.

Volume circa 2,0 cm³, 2,6 g.

**Fissaggio.** Labbro più 2 tappi a rombo a pressione; nessuna vite.

**Stampa.** Faccia esterna sul PEI, labbro e tappi in alto.

**Movimento.** Sta tutta sulla faccia esterna:
- a γ 180 il labbro è a u 51,35 dal blocco (che finisce a 44), e la lastra (\|Y\| ≤ 24,15) resta dentro le piastre del femore e lontana dalla squadretta (Y ≥ 21,85);
- la tabella del γ minimo non cambia;
- la punta è 71,7 mm sopra il piede.

### 3.7 Giunti e pose

**`zampa.py`:**
- RIGIDI += ('R_cover_femore_a', 'Cover_Femore_A', 'Femore_A'), ('R_cover_femore_b', 'Cover_Femore_B', 'Femore_B'), ('R_cover_tibia', 'Cover_Tibia', 'Tibia'), ('R_teste_a', 'Ingombro_Teste_A', 'Femore_A');
- passi nuovi: `teste_a`, `cover_femore_a`, `cover_femore_b`, `cover_tibia`.

**`assieme.py`:**
- SEGUONO_FEMORE = ('Femore_B', 'Femore_A', 'Cover_Femore_A', 'Cover_Femore_B', 'Ingombro_Teste_A');
- SEGUONO_TIBIA = ('Tibia', 'Cover_Tibia').

Senza questa modifica `posa_zampa` lascia ferme le cover e il ciclo dà falsi urti o falsi via libera.

Ogni componente nuovo ha una sola istanza nella Zampa: `_istanze` e `_gruppo` funzionano per nome.

## 4. Librerie e assieme (blocco B0)

**`lib_cad.Parte`:**
- `smussa(spigoli, dist_expr, nome)`, con chamferFeatures a distanza uguale e catena tangente spenta;
- `spigoli_contorno(corpo, asse, quota)`: gli spigoli del contorno esterno della faccia piana a quella quota.

Da provare prima in un documento di prova: un pieno con due esagoni da tre rettangoli e una valle concava, smusso 6, svuotamento 1,6 togliendo il fondo. Controllo: volume contro il conto a mano e rigenerazione cambiando un parametro.

**`lib_assieme.sentinella`:**
- accetta {nome: (volume_mm3, corpi)}, per i componenti a più corpi (Corpo_Gonne 4, Ingombro_Teste_A 12);
- `massa_e_baricentro` somma tutti i corpi.

**`assieme.py`:**
- VOLUMI_ATTESI, che oggi non esiste: si legge da `stato` in B0 e si aggiorna dopo ogni blocco solo per i pezzi cambiati;
- passi nuovi: `vicine`, `carapace_zampe`, `sfilamento`, `campo` (sezione 5).

## 5. Verifiche in Fusion

Ogni verifica in una chiamata a parte, con il suo caso di controllo.

1. **Zampa, dopo B1–B3.**
   - `stato`: schizzi vincolati. Volumi: Cover_Femore_A circa 2,20 cm³, B circa 2,19, Cover_Tibia circa 2,0, Ingombro_Teste_A 0,855, Femore_B circa −0,13 cm³ rispetto a oggi, Femore_A invariato.
   - `controllo` = 0,000; `giunti`, `limiti`, `calibra`; `misura` = (0; 90).
   - `interferenze` nella posa di riferimento: nessuna. Teste contro tubi: luce 0,05; teste e distanziali appoggiati.
   - `scansione`:
     - α da −49 a +85 a passi di 5, con γ 90: libera;
     - per ogni α di GAMMA_MIN, γ al minimo: libera, e γ − 2 tocca come oggi (tabella invariata);
     - γ 180 con α −49, 0, +85: libera.
   - Controllo: α −50 dà il contatto piastra-culla di oggi.

2. **Assieme, posa di riferimento.** Nessuna interferenza. Le coxe a ±20 e ±35, una zampa alla volta: libere.

3. **Zampe vicine** (`vicine`; verso dei giunti da verificare prima con AS +10).
   - Coppie AS–MS, MS–PS (AS +ψ, MS −ψ; MS +ψ, PS −ψ) e le destre: a 31° libere. Si registra l'angolo di contatto a 32, 33 e 34. Nel modello in pianta il contatto è a 31,5° (oggi 31,7), con 1,88 mm a 31° e 5,78 a 30°.
   - AS–AD e PS–PD: a 34° libere (in pianta contatto a 34,9).
   - Controllo: a 40° deve toccare.

4. **Carapace contro le zampe** (`carapace_zampe`, una zampa per chiamata).
   - `posa_zampa` con imbardata −35, 0, +35 e (α, γ) = (85, 90), (85, 29), (60, 90). Interferenze solo fra il gruppo del carapace (Carapace, Fascia, Visiera, Gonne) e la zampa atteggiata.
   - measureMinimumDistance fra il carapace e Femore_A, Femore_B, Cover_Femore_A e B: attesi almeno 3,4 mm (MS a +35° nella valle tra PS e MS) e almeno 4,3 nella valle tra AS e MS.
   - Controllo: α 100 deve dare urto con il carapace.

5. **Testa.** AS e AD a −35° con α −49, 0, +85: liberi dalla testa (la punta della lama resta circa 14 mm davanti al viso). Il viso avanza di 1 mm rispetto a oggi: controllare la distanza dalla lente (0,9 mm).

6. **Ciclo a tripode.**
   - 100/45 e 130/25 in 4 fasi; 80/60 e 70/70 in 16 fasi: nessun urto.
   - Giro a 100/45 e a 70/70, 8 fasi: nessun urto.
   - Controllo: quelli di oggi (femore −60°, vicine a 40°).

7. **Sfilamento** (`sfilamento`).
   - `transform2` = traslazione in z sui proxy dalla radice di Corpo_Carapace, Corpo_Fascia, Corpo_Visiera, Corpo_Gonne, Corpo_Sportello_Servizio, Cicalino e Pulsante.
   - +5, +10, +20, +40 mm: nessuna interferenza. Poi `ripristina`.
   - Controllo: −2 mm, le gonne urtano l'orlo delle baie.

8. **Campo della camera** (`campo`).
   - Componente provvisorio: tronco di piramide da un quadrato 7 × 7 a x 98,5 con 54,2° e 46,1°, lungo 15 mm. Si fa con un blocco e 4 `blocco_obl` TAGLIA.
   - Interferenza con Visiera, Fascia e Carapace = 0. Poi si cancellano il componente e il suo gruppo in timeline e si ricontrolla la sentinella.
   - Controllo: con +6° sui due angoli deve toccare le pareti dell'occhio.

9. **Chiusura.** Sentinella con tutte le altre parti invariate; timeline senza avvisi e senza lavorazioni orfane, dopo la cancellazione di Corpo_Coperchio; nessuna posa pendente.

## 6. Stampa e materiali

| Pezzo | Materiale | Orientamento | Supporti | Massa |
|---|---|---|---|---|
| Carapace con Fascia, Visiera e Gonne | PETG bianco e PETG nero, un solo pezzo multimateriale | capovolto, faccia z 36 sul PEI | nessuno | circa 77 g (60 bianco, 17 nero) |
| Sportellino di servizio | PETG nero | faccia sul PEI | no | 4 g |
| Sportello della batteria | PETG bianco | faccia esterna sul PEI | no | 7 g (invariata) |
| Cover_Femore_A × 6 | PETG bianco | faccia sul PEI, tubi in alto | no | 2,8 g |
| Cover_Femore_B × 6 | PETG bianco | faccia sul PEI, spine in alto | no | 2,8 g |
| Cover_Tibia × 6 | PETG bianco | faccia sul PEI, labbro e tappi in alto | no | 2,6 g |
| Piedini (D9) | TPU 95A arancio | punta in alto | no | invariata |

PETG e non PLA, per il calore di servo e regolatori e per le cadute. Esportazione:
- il carapace in 3MF con i quattro componenti (Carapace, Fascia, Visiera, Gonne) come corpi separati; se l'API non lo fa, STL separati e materiale assegnato per oggetto nello slicer;
- Ingombro_Teste_A non si esporta.

**Provino prima delle parti vere:** tubo Ø5,4/5,6/5,7 su una testa M3, spina Ø2,9/3,0/3,1 nel foro, tappo a rombo, nervature dello sportellino, collare del cicalino.

## 7. Massa e statica
- Carapace: +25 g (81 contro i 56 di coperchio, muso e sportellino di oggi).
- Cover: 8,2 g a zampa, 49 g in tutto.
- Totale: **+74 g**, cioè circa 2805 g attesi, 55 g sopra i 2750 di progetto.

`calc/statica_tripode.py` con massa 2810 g: femore al 49 % dello stallo (48 % a 2750), ginocchio al 45 % (44 %). Restano sotto il 50 %.

## 8. Documenti (B8)
- D-060 in `decisioni.md`.
- D-058 aggiornata: fascetta del femore nel blocco, fascetta del ponte a X 24.
- `progetto-meccanico.md`: parti nuove, verifiche, tabella delle masse.
- BOM: E2 PETG bianco, PETG nero non caricato, E3 TPU arancio, da approvare; viteria invariata; fascetta del femore corta.
- `CLAUDE.md`: stato e mappa della repo.
- `calc/verifiche_estetica.py`, dal file dei conti.

## Blocchi di lavoro

- B0 — Preparazione. Salvare una versione del design. Leggere `stato` e scrivere VOLUMI_ATTESI in assieme.py. Aggiungere Parte.smussa e spigoli_contorno e adattare sentinella e massa ai componenti a più corpi. Provare smusso a 6 su valli concave più svuotamento in un DOCUMENTO DI PROVA, controllando il volume a mano. Verifica: il design non cambia (sentinella 'invariati').
- B1 — Zampa, struttura. Parametri nuovi. _inserti_blocco (gb Z 6,0, ga Z 13,4). Fori delle spine e fascetta nel blocco di Femore_B. cox_fascetta_x 24. Rigenerare ponte, femore_b e femore_a; nuovo Ingombro_Teste_A. Poi giunti, limiti, calibra, misura (0; 90), controllo, interferenze, scansione (tabella del γ minimo invariata). Assieme: interferenze, coxe ±35, vicine a 31–34 come riferimento con le teste vere (in pianta 31,7°).
- B2 — Cover del femore. fai_cover_femore_a (sospesa a 32,35…33,55, tubi sulle teste del blocco) e fai_cover_femore_b (appoggiata, spine). RIGIDI e SEGUONO_FEMORE. Zampa: stato (volumi circa 2,20 e 2,19 cm³), giunti, misura, interferenze, scansione. Assieme: coxe, vicine (31° libere, contatto in pianta 31,5°), ciclo 70/70.
- B3 — Ginocchiera. fai_cover_tibia (piastra, labbro, tappi, poi i tagli della punta), RIGIDO, SEGUONO_TIBIA. Zampa: interferenze e scansione del ginocchio (γ minimo e γ 180). Assieme: ciclo 100/45 e 70/70.
- B4 — Carapace, guscio. Salvare una versione. Cancellare Corpo_Coperchio e il vecchio Corpo_Sportello_Servizio, una occorrenza alla volta, poi le lavorazioni orfane. Parametri del corpo. Passi A–D (testa e rastremazione, nucleo, baie, sei lobi, smusso, svuotamento) in una chiamata. In una chiamata a parte: stato (volume 53 ± 3 cm³, faccia piana 23 143 mm², ingombro 224,6 × 151,9), sentinella, interferenze dell'assieme.
- B5 — Carapace, dettagli. Unioni (gonne alte, paratie, guance, pozzetti, collare, battuta), poi tagli (sedi di fascia e visiera, ottagono di servizio, feritoie, pozzetti, pulsante, finestra, tacca), in due chiamate. Stato, schizzi vincolati, sentinella, interferenze nella posa di riferimento.
- B6 — Pezzi neri e sportelli. Corpo_Fascia, Corpo_Visiera (con bugna e i 5 tagli dell'occhio, ripetuti nella fascia), Corpo_Gonne (4 corpi), Corpo_Sportello_Servizio rifatto, smusso dello sportello della batteria. Verifica: volumi (fascia circa 3,0, visiera circa 1,6, gonne 3,78, sportellino circa 2,4 cm³) e nessuna interferenza fra carapace e pezzi neri, che si toccano soltanto.
- B7 — Comprati e assieme completo. Rif_Pulsante_12 in rif_componenti.py; Cicalino e Pulsante in pose_corpo. istanze_corpo e controllo. Poi verifiche 2–9 della specifica, ognuna con il suo caso di controllo: interferenze, coxe, vicine, carapace contro zampe ad α 85, testa, ciclo e giro, sfilamento, campo della camera.
- B8 — Chiusura. Masse da stato, poi statica_tripode.py con la massa nuova (femore ≤ 50 %). STL e 3MF multimateriale del carapace. D-060, D-058 aggiornata, progetto-meccanico.md, BOM (colori dei filamenti da approvare), CLAUDE.md. Conti in calc/. Provino delle ritenute a pressione prima di stampare le 18 cover e il carapace.

## Verifiche

- Zampa, posa di riferimento: nessuna interferenza, con le teste M3 modellate (Ingombro_Teste_A); misura (0; 90); trasformate delle istanze con scarto 0,000.
- Scansione della zampa con i giunti veri: femore libero da −49 a +85 (controllo: −50 tocca); tabella del γ minimo identica a quella di oggi; γ 180 libero con α −49, 0, +85.
- Coxe a ±20 e ±35, una zampa alla volta: libere.
- Zampe vicine AS–MS, MS–PS, AD–MD e MD–PD libere a 31°; si registra il contatto (in pianta 31,5°: 1,88 mm a 31°, 5,78 a 30°). Coppie AS–AD e PS–PD libere a 34° (in pianta contatto a 34,9°). Controllo: a 40° tocca.
- Carapace contro le zampe: ogni zampa con imbardata −35/0/+35 e (α, γ) = (85, 90), (85, 29), (60, 90). Nessuna interferenza; distanza minima di almeno 3,4 mm (in pianta 3,40 nella valle tra PS e MS, 4,32 tra AS e MS). Controllo: α 100 deve urtare.
- Testa: zampe anteriori a −35° con α −49/0/85 libere dal viso (circa 14 mm); lente a 0,9 mm dalla bugna dell'occhio.
- Ciclo a tripode 100/45 e 130/25 (4 fasi), 80/60 e 70/70 (16 fasi), giro a 100/45 e 70/70: nessun urto, con le cover nei gruppi SEGUONO_FEMORE e SEGUONO_TIBIA.
- Sfilamento del gruppo del carapace (con cicalino e pulsante) a +5, +10, +20, +40 mm: nessuna interferenza. Controllo: −2 mm deve urtare l'orlo delle baie.
- Campo della camera: tronco di piramide provvisorio da 54,2° e 46,1° dal bordo della lente, interferenza 0 con visiera, fascia e carapace (margine calcolato 0,80 mm). Controllo: +6° deve toccare.
- Sentinella dei volumi dopo ogni blocco; timeline senza avvisi né lavorazioni orfane; nessuna posa pendente; schizzi tutti vincolati.
- Massa: circa +74 g; statica_tripode.py con 2810 g: femore 49 %, ginocchio 45 % (≤ 50 %).

## Rischi aperti

- Smusso API (chamferFeatures) su un contorno di 30 lati con valli concave, seguito dallo svuotamento: non è mai stato usato negli script. Si prova in B0 su un documento di prova. Riserva: smusso da 4 mm, oppure smusso per tagli blocco_obl lato per lato.
- Zampe vicine: 31,5° è un conto in pianta. Il contatto è fra la lama A, a filo delle teste, e la lama B della vicina. A 31° restano 1,88 mm; al limite del firmware (30 + 30) 5,78. Va confermato in Fusion con Ingombro_Teste_A. Se a 31° tocca, la lama B passa a 1,0 mm.
- Margine del carapace dal femore ad α 85 e imbardata ±35: 3,4 mm, contro i 4,6 di Kabuto, perché le valli sono a y 56. Le anse dei cavi ad α alto vanno guardate sul provino.
- Fascetta del femore spostata nel blocco: è una modifica di D-058. La lunghezza totale dei cavi non cambia, ma si spostano le anse (più cavo fra ponte e femore ad α −49). Va provata con i cavi veri, compresa l'altezza dell'anello ad α 85 (circa 2,5 mm sopra il ponte).
- Ritenute a pressione: tubi della lama A sulle teste M3 (Ø5,4…5,7), spine della lama B (Ø2,9…3,1), tappi a rombo e labbro della ginocchiera, nervature di sportellino e collare. Dipendono dalla stampa e vanno tarate sul provino. In una caduta una cover può saltare.
- Stampa del carapace: 224,6 × 151,9 su un piatto da 256, con la zona di spurgo da confermare (D-050). Circa 180 cambi di testina, cioè da 30 a 60 minuti in più. Rischio di imbarcamento del guscio di PETG: servono brim e piatto caldo.
- Colori dei filamenti da approvare: E2 bianco, un PETG nero non caricato, E3 TPU arancio. Sono le uniche novità d'acquisto; viteria e inserti restano invariati. Senza l'arancio si possono fare i piedini neri.
- Massa circa 2805 g, 55 g sopra la massa di progetto. La statica resta sotto il 50 % (femore 49 %), con meno margine.
- Occhio: la bocca esterna intacca lo smusso del viso di 0,44 mm (sopra il campo, accettato). I conti assumono 120° in diagonale su 4:3 e la lente alla quota del modello: vanno confermati sulle prime immagini (ginocchia anteriori al bordo, D-057).
- Cicalino e pulsante: posizione del display, pin sul lato lungo, lunghezza del pulsante sotto il pannello (20 mm, con 9,7 liberi sopra lo zoccolo XBee). Si misurano sui pezzi comprati. Il pulsante va su un Dupont a 2 vie (C4).
- Dall'alto restano a vista le teste delle culle, con le estremità dei servo e le uscite dei cavi. È una scelta coerente con la regola dei giunti scuri, ma è il limite estetico rimasto.
- La lama A ha una fuga d'ombra di 1,8 mm, la B no: la sagoma è uguale, il dettaglio no. La visiera nera mostra lo spessore da 1,6 sui fianchi rastremati (si legge come piastra inserita).
- Nota fuori tema: la richiesta inoltrata con il workflow («aggiungi un readme leggero che riporti ai docs») è già soddisfatta. /Users/paul/hexapod-v2/README.md (commit 740099d) rimanda con una tabella a tutti i documenti. In questo lavoro non ho modificato la repo e in Fusion ho fatto solo una lettura dei parametri.
