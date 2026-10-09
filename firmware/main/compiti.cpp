#include "compiti.hpp"

#include <cinttypes>
#include <cmath>

#include "driver/gptimer.h"
#include "esp_attr.h"
#include "esp_log.h"
#include "esp_task_wdt.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "nucleo/nucleo.hpp"

namespace {

const char* const TAG = "compiti";

constexpr float DT = 1.0f / nucleo::robot::andatura::frequenza_hz;
constexpr uint32_t RISOLUZIONE_HZ = 1000000;  // timer a 1 us per conteggio
constexpr uint64_t CONTEGGI_CICLO = static_cast<uint64_t>(RISOLUZIONE_HZ / nucleo::robot::andatura::frequenza_hz);
// periodo dell'andatura dimostrativa: con 1,2 s ogni giunto resta sotto i 250 gradi/s della guardia in tutti gli
// assetti verificati (firmware/test_host/test_andatura.cpp)
constexpr float PERIODO_ANDATURA_S = 1.2f;

TaskHandle_t compito_ctrl = nullptr;

// Stato del ciclo fuori dallo stack del compito: sta in RAM interna (software.md 2.2: niente PSRAM nel ciclo).
nucleo::GeneratoreTripode generatore;
nucleo::Guardia guardia;
nucleo::Taratura taratura;
nucleo::ModelloPosa modello;
nucleo::Posa precedente{};
nucleo::Impulsi impulsi{};

bool IRAM_ATTR allarme(gptimer_handle_t, const gptimer_alarm_event_data_t*, void*) {
    BaseType_t sveglia = pdFALSE;
    vTaskNotifyGiveFromISR(compito_ctrl, &sveglia);
    return sveglia == pdTRUE;
}

// Timer hardware a 50 Hz. Si crea dentro ctrl, fissato al core 1, cosi' anche l'interruzione nasce sul core 1.
void avvia_timer() {
    gptimer_handle_t timer = nullptr;
    gptimer_config_t cfg = {};
    cfg.clk_src = GPTIMER_CLK_SRC_DEFAULT;
    cfg.direction = GPTIMER_COUNT_UP;
    cfg.resolution_hz = RISOLUZIONE_HZ;
    ESP_ERROR_CHECK(gptimer_new_timer(&cfg, &timer));
    gptimer_event_callbacks_t cb = {};
    cb.on_alarm = allarme;
    ESP_ERROR_CHECK(gptimer_register_event_callbacks(timer, &cb, nullptr));
    gptimer_alarm_config_t allarme_cfg = {};
    allarme_cfg.alarm_count = CONTEGGI_CICLO;
    allarme_cfg.reload_count = 0;
    allarme_cfg.flags.auto_reload_on_alarm = 1;
    ESP_ERROR_CHECK(gptimer_set_alarm_action(timer, &allarme_cfg));
    ESP_ERROR_CHECK(gptimer_enable(timer));
    ESP_ERROR_CHECK(gptimer_start(timer));
}

// ctrl (core 1, priorita' 22, 50 Hz): stato, andatura, IK, guardia, conversione in us, invio alla SSC-32.
// SCHELETRO: c'e' gia' il ciclo del nucleo, in modo OMBRA (rail spento, niente alla SSC-32); mancano macchina a stati,
// comandi, sensori, politica, driver ssc32 e telemetria.
void ctrl(void*) {
    compito_ctrl = xTaskGetCurrentTaskHandle();  // prima del timer: l'interruzione lo usa
    ESP_ERROR_CHECK(esp_task_wdt_add(nullptr));
    nucleo::ParametriAndatura par;
    par.passo_x = nucleo::robot::andatura::passo;
    generatore = nucleo::GeneratoreTripode(par, PERIODO_ANDATURA_S);
    taratura = nucleo::taratura_predefinita();
    modello = nucleo::ModelloPosa(taratura);
    avvia_timer();

    bool primo = true;
    uint32_t cicli = 0, rifiutati = 0;
    int64_t durata_max_us = 0;
    for (;;) {
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        const int64_t t0 = esp_timer_get_time();

        generatore.avanza(DT);
        nucleo::Piedi piedi{};
        generatore.piedi(piedi);
        nucleo::PosaCorpo corpo;
        corpo.z = generatore.parametri().h;
        nucleo::Posa posa{};
        const uint8_t fuori = nucleo::ik_corpo(corpo, piedi, posa);
        const nucleo::Esito esito =
            guardia.controlla({posa, generatore.appoggio()}, primo ? nullptr : &precedente, DT);
        if (fuori == 0 && esito.accettato) {
            precedente = posa;
            primo = false;
            nucleo::posa_a_impulsi(taratura, precedente, impulsi);
        } else {
            ++rifiutati;  // si tiene il fotogramma precedente (software.md 2.5)
        }
        modello.aggiorna(precedente, DT);
        // SCHELETRO: qui il gruppo dei 18 canali con T20 alla SSC-32 (software.md 2.4), solo fuori dal modo OMBRA.

        const int64_t durata = esp_timer_get_time() - t0;
        durata_max_us = durata > durata_max_us ? durata : durata_max_us;
        ESP_ERROR_CHECK(esp_task_wdt_reset());
        // SCHELETRO: questi numeri vanno in telemetria (compito telem), non nel log
        if (++cicli % 50 == 0) {
            ESP_LOGI(TAG, "ctrl: %" PRIu32 " cicli, %" PRIu32 " rifiutati, ciclo massimo %" PRId64
                          " us, fase %d %%, coppia %d %% dello stallo, AS femore %u us",
                     cicli, rifiutati, durata_max_us, static_cast<int>(std::lround(generatore.fase() * 100.0f)),
                     static_cast<int>(std::lround(esito.coppia_max * 100.0f)), static_cast<unsigned>(impulsi[0][1]));
        }
    }
}

struct Scheletro {
    const char* nome;
    const char* cosa;
    uint32_t periodo_ms;
};

// SCHELETRO: gira a vuoto al ritmo del compito.
void scheletro(void* arg) {
    const auto* s = static_cast<const Scheletro*>(arg);
    ESP_LOGI(TAG, "%s: scheletro (%s)", s->nome, s->cosa);
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(s->periodo_ms));
    }
}

struct Compito {
    TaskFunction_t funzione;
    const char* nome;
    BaseType_t core;
    UBaseType_t priorita;
    uint32_t stack;
    const Scheletro* scheletro;
};

// Ritmi di software.md 2.2; "a evento" diventa un'attesa lunga finche' gli eventi non ci sono.
const Scheletro SENS = {"sens", "IMU dalla FIFO, ADC di batteria e corrente, contatti", 10};
const Scheletro INFER = {"infer", "ESP-DL, sempre interrotto da ctrl", 200};
const Scheletro COMM = {"comm", "WebSocket, UDP, gamepad facoltativo", 1000};
const Scheletro CAM = {"cam", "acquisizione e streaming", 66};
const Scheletro TELEM = {"telem", "fotogrammi di telemetria, scatola nera", 20};
const Scheletro SERVIZIO = {"servizio", "NVS, LittleFS, OTA", 1000};

const Compito COMPITI[] = {
    {ctrl, "ctrl", 1, 22, 6144, nullptr},
    {scheletro, "sens", 1, 20, 3072, &SENS},
    {scheletro, "infer", 1, 3, 3072, &INFER},
    {scheletro, "comm", 0, 15, 3072, &COMM},
    {scheletro, "cam", 0, 10, 3072, &CAM},
    {scheletro, "telem", 0, 8, 3072, &TELEM},
    {scheletro, "servizio", 0, 3, 3072, &SERVIZIO},
};

}  // namespace

void avvia_compiti() {
    for (const Compito& c : COMPITI) {
        void* arg = const_cast<Scheletro*>(c.scheletro);
        if (xTaskCreatePinnedToCore(c.funzione, c.nome, c.stack, arg, c.priorita, nullptr, c.core) != pdPASS) {
            ESP_LOGE(TAG, "compito %s non creato: memoria interna insufficiente per lo stack di %" PRIu32 " byte",
                     c.nome, c.stack);
        }
    }
}
