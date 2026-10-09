# Firmware dell'esapode

Firmware per l'ESP32-S3 (scheda UICPAL ESP32-S3-CAM N16R8) in **C++17 su ESP-IDF, senza Arduino**. Architettura in `docs/software.md` (capitoli 2 e 4); qui c'è la prima parte della fase S0: il nucleo provato sul PC e lo scheletro del firmware che compila.

## Struttura

```
firmware/
  CMakeLists.txt            progetto ESP-IDF (build minima: solo main e i componenti che richiede)
  sdkconfig.defaults        16 MB di flash, PSRAM octal, partizioni, OTA con ritorno, watchdog a 1 s
  partitions.csv            tabella di software.md 2.8, con due slot OTA da 4 MB
  main/                     app_main e compiti FreeRTOS (scheletri, vedi sotto)
  components/nucleo/        C++17 puro, senza dipendenze da ESP-IDF: si compila sul chip e sul PC
    include/nucleo/
      robot_generato.hpp    GENERATO da tools/genera_header.py (non si modifica a mano)
      tipi.hpp              vettori, angoli di una zampa, posa, maschera d'appoggio
      cinematica.hpp        diretta e inversa di zampa e corpo
      statica.hpp           carichi sui piedi, coppie stimate, margine di stabilità
      guardia.hpp           guardia del fotogramma intero (software.md 2.5)
      andatura.hpp          tripode a fase continua, identico a cad/script/assieme.py -> pose_tripode
      servo.hpp             angolo -> impulso, taratura, modello del servo per la posa prevista
  test_host/                test del nucleo sul PC: CMake, ctest, Unity, sanitizer
    vettori_generati.hpp    GENERATO da tools/genera_vettori.py
```

Fuori da `firmware/`: `tools/genera_header.py`, `tools/genera_vettori.py`, `tools/riferimento.py` (andatura di riferimento in Python), `tests/` (pytest), `ruff.toml`, `.github/workflows/ci.yml`.

## Versione di ESP-IDF

**ESP-IDF v6.1** (pubblicata il 27 agosto 2026): l'ultima versione stabile pubblicata da almeno due settimane al 9 ottobre 2026, ed è quella scelta in `docs/software.md` (tabella del capitolo 1). La stessa versione è fissata nel CI (`ESP_IDF_VERSIONE` in `.github/workflows/ci.yml`, immagine Docker `espressif/idf:v6.1`): si cambiano insieme.

Installazione sul Mac (fatta il 9 ottobre 2026, solo per l'esp32s3):

```sh
git clone -b v6.1 --depth 1 --recursive --shallow-submodules https://github.com/espressif/esp-idf.git ~/esp/esp-idf
~/esp/esp-idf/install.sh esp32s3
```

Gli strumenti stanno in `~/.espressif` (compilatore `xtensa-esp-elf` 15.2.0, ambiente Python `idf6.1_py3.12_env`). In `~/esp-idf` resta un'installazione precedente della v6.0: questo progetto usa `~/esp/esp-idf`.

## Compilare il firmware

```sh
. ~/esp/esp-idf/export.sh
cd firmware
idf.py build          # la prima volta crea sdkconfig da sdkconfig.defaults (sdkconfig non va in git)
idf.py size           # occupazione di flash e RAM
```

Risultato al 9 ottobre 2026: compila senza avvisi; `hexapod.bin` 174 KB, il 4 % dello slot OTA da 4 MB.

Non provato sul chip: la scheda non c'è ancora. Quando ci sarà: `idf.py -p <porta> flash monitor` (console sulla CH340).

## Provare il nucleo sul PC

```sh
cmake -S firmware/test_host -B firmware/test_host/build -G Ninja   # sanitizer attivi: -DNUCLEO_SANITIZER=OFF per toglierli
cmake --build firmware/test_host/build
ctest --test-dir firmware/test_host/build --output-on-failure -V    # -V stampa gli scarti misurati
```

Unity si scarica alla prima configurazione (FetchContent), alla stessa revisione che ESP-IDF v6.1 porta in `components/unity` (v2.6.0_RC1), con l'hash dell'archivio controllato. Nucleo e test si compilano con `-Wall -Wextra -Wpedantic -Wshadow -Wdouble-promotion -Werror` e, di default, con AddressSanitizer e UndefinedBehaviorSanitizer.

Cosa controllano (criteri di `docs/software.md` 6.3) e cosa si è misurato il 9 ottobre 2026 con Apple clang 21 (uguale in Debug con i sanitizer e in Release):

| Prova | Criterio | Misurato |
|---|---|---|
| Diretta contro il CAD (`robot/pose_cad.json`, 75 pose) | ≤ 0,05 mm | 0,00009 mm |
| Diretta contro `tools/descrizione.py` (810 punti) | ≤ 0,001 mm | 0,00005 mm |
| Inversa contro il Python, andata e ritorno | ≤ 0,01° | 0,0004° (punta ritrovata a 0,0004 mm) |
| Inversa delle punte lette dal CAD (66 pose) | ≤ 0,01° | 0,002° |
| Andatura contro i cicli del CAD (arrotondati a 0,01°) | ≤ 0,006° | 0,005° |
| Andatura contro `tools/riferimento.py` (240 pose a fasi diverse) | ≤ 0,01° | 0,00003° |
| Pose dei 6 cicli verificati nel CAD | nessun limite geometrico violato | nessuno; a 70/70 rifiuto per la coppia (sotto) |
| Casi d'urto: femore a −60°, vicine a 40° una verso l'altra, ginocchio sotto la tabella | rifiutati | rifiutati con il motivo giusto |
| Statica contro `calc/statica_tripode.py`, riga per riga | carichi ≤ 1e-4 kgf, coppie ≤ 1e-3 kgf·cm | 5e-7 kgf, 5e-6 kgf·cm |
| Regressione a 100/45 | femore al 51 % ± 1, margine 59 mm | 51,38 % (5,651 kgf·cm), 59,21 mm |
| Andatura a 50 Hz, ciclo da 1,2 s, tre cicli per assetto | nessun salto oltre 250°/s; piedi in appoggio fermi ≤ 0,5 mm | salto massimo 4,06° a fotogramma (203°/s); piedi fermi entro 0,0002 mm |
| Partenza, rotazione e arresto con la rampa dei parametri | ogni fotogramma accettato dalla guardia | 360 fotogrammi accettati, salto massimo 3,8° |

**Coppia a 70/70.** Le pose del ciclo a tripode a 70/70 (e della rotazione sul posto a 70/70) passano tutti i limiti geometrici, ma la coppia stimata arriva al 75 % (74 % nella rotazione) dello stallo, oltre il rifiuto al 70 % di `robot.yaml`; la tabella del 4.2 di `software.md` dà lo stesso 75 %. Nel CAD si è verificata l'assenza di urti, non la coppia. La guardia li rifiuta: a 70/70 il firmware dovrà usare un'andatura con più piedi a terra. Il test lo controlla esplicitamente.

## Test Python e file generati

```sh
python3 -m venv .venv && .venv/bin/pip install -r tests/requirements.txt
.venv/bin/python -m pytest tests            # descrizione contro il CAD, statica, file generati aggiornati
.venv/bin/ruff check .
```

`robot_generato.hpp` e `vettori_generati.hpp` si rigenerano dopo ogni modifica di `robot/robot.yaml` o una nuova esportazione dal CAD (prima `python3 tools/descrizione.py --aggiorna-hash`):

```sh
python3 tools/genera_header.py
python3 tools/genera_vettori.py
```

L'uscita è deterministica; il CI la rigenera e fallisce se differisce da quella nel commit, o se `cad_sha256` di `robot.yaml` non è quello di `cad.json`.

## La guardia

Un fotogramma (posa delle 18 articolazioni più i piedi a terra) è accettato solo se rispetta tutti i limiti di `robot.yaml -> guardia`: imbardata ±30°, somma tra vicine entro 56° con i segni di `robot.yaml` (a sinistra imb_A − imb_M e imb_M − imb_P, a destra il contrario), femore da −45° a +82°, ginocchio da γmin(α) + 3° (fra due righe della tabella vale il massimo) a 177°, corsa ±80° attorno al calettamento, 250°/s per giunto rispetto al fotogramma precedente, baricentro ad almeno 20 mm dai lati del poligono d'appoggio, coppia stimata sotto il 70 % dello stallo (oltre il 55 % e il 60 % dà il livello di avviso e di tempo limitato, che userà la macchina a stati). Il singolo giunto non si tronca mai: l'esito dice il primo motivo del rifiuto (zampa, giunto, valore, limite) e tutti i limiti violati; chi comanda tiene il fotogramma precedente o riduce il comando. I limiti morbidi possono solo stringere quelli rigidi (`LimitiGuardia::stringi`).

Ipotesi della statica, le stesse di `calc/`: corpo orizzontale, baricentro al centro del corpo, forze ai piedi verticali. Con più di tre piedi a terra il problema è iperstatico e il nucleo prende la ripartizione a norma minima (S): la ripartizione vera dipende dalle cedevolezze.

## Cosa è uno scheletro

I compiti di `docs/software.md` 2.2 esistono tutti, con il loro core, la priorità e il ritmo; nel codice sono marcati `SCHELETRO`.

| Compito | Core | Priorità | Ritmo | Oggi |
|---|---|---|---|---|
| `ctrl` | 1 | 22 | 50 Hz da un timer hardware, interruzione sul core 1 | **fa il ciclo del nucleo in modo OMBRA**: andatura a tripode a 100/45, IK del corpo, guardia, impulsi, posa prevista; niente alla SSC-32, rail spento. Si iscrive al watchdog. Ogni secondo scrive nel log cicli, rifiutati e durata massima del ciclo |
| `sens` | 1 | 20 | 100 Hz | gira a vuoto |
| `infer` | 1 | 3 | 5 Hz | gira a vuoto |
| `comm` | 0 | 15 | a evento | gira a vuoto |
| `cam` | 0 | 10 | 15 Hz | gira a vuoto |
| `telem` | 0 | 8 | 50 Hz | gira a vuoto |
| `servizio` | 0 | 3 | a evento | gira a vuoto |

All'avvio `app_main` porta GPIO42 (rail dei servo) basso, scrive versione e impronta di `cad.json`, fa un autotest del nucleo (la posa iniziale dell'andatura deve passare la guardia) e solo allora avvia i compiti.

Mancano: macchina a stati e sequenza d'accensione (2.6), driver della SSC-32 (2.4), comandi e rete, sensori, telemetria, taratura in NVS (2.7), OTA con autotest (2.8), andature a coppie e a onda, politica.

## Partizioni

| Partizione | Indirizzo | Dimensione |
|---|---|---|
| `nvs` | 0x9000 | 24 KB |
| `nvs_cal` (taratura) | 0xF000 | 16 KB |
| `otadata` | 0x13000 | 8 KB |
| `phy_init` | 0x15000 | 4 KB |
| `ota_0` | 0x20000 | 4 MB |
| `ota_1` | 0x420000 | 4 MB |
| `coredump` | 0x820000 | 64 KB |
| `storage` (LittleFS) | 0x830000 | 7,8 MB, fino a 16 MB |

Gli indirizzi non vanno cambiati dopo la prima installazione: l'OTA non riscrive la tabella.

## Integrazione continua

`.github/workflows/ci.yml`, quattro job: `python` (ruff e pytest), `nucleo` (CMake e ctest con i sanitizer, con gcc e con clang), `firmware` (azione ufficiale `espressif/esp-idf-ci-action` v1.2.0 con ESP-IDF v6.1 per l'esp32s3, dimensione dell'immagine contro lo slot OTA, binari allegati), `generati` (impronta di `cad.json`, header e vettori rigenerati, `git diff --exit-code`).

**Passo successivo: il job `qemu`** (`software.md` 6.4). Una configurazione dedicata del firmware (per esempio `sdkconfig.qemu` con la console sulla UART0 e senza camera, Wi-Fi e sensori) si avvia nel QEMU di Espressif per l'esp32s3 (`idf.py qemu`, nell'immagine Docker dell'IDF), stampa versione e autotest e, in uno scenario scritto, emette i comandi attesi per la SSC-32; il job confronta l'uscita. Prova la macchina a stati e il nucleo, non lo stack completo: il QEMU dell'S3 non emula Wi-Fi, Bluetooth, USB, I2C, RMT né la matrice dei GPIO. Serve prima il driver della SSC-32 con il backend simulato, e va verificato se la UART1 è emulata; se non lo è, lo scenario usa la console.
