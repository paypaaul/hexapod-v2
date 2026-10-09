// Firmware dell'esapode (software.md 2). Per ora: rail spento, autotest del nucleo, compiti di 2.2 come scheletri.
#include <cmath>

#include "compiti.hpp"
#include "driver/gpio.h"
#include "esp_log.h"
#include "nucleo/nucleo.hpp"

namespace {

const char* const TAG = "hexapod";

// Accensione del rail dei servo: spento con il GPIO basso o flottante (D-019, software.md 2.6).
constexpr gpio_num_t GPIO_RAIL = GPIO_NUM_42;

void rail_spento() {
    ESP_ERROR_CHECK(gpio_set_level(GPIO_RAIL, 0));  // il livello prima della direzione: niente impulsi alti
    gpio_config_t io = {};
    io.pin_bit_mask = 1ULL << GPIO_RAIL;
    io.mode = GPIO_MODE_OUTPUT;
    io.pull_up_en = GPIO_PULLUP_DISABLE;
    io.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io.intr_type = GPIO_INTR_DISABLE;
    ESP_ERROR_CHECK(gpio_config(&io));
    ESP_ERROR_CHECK(gpio_set_level(GPIO_RAIL, 0));
}

// Il nucleo calcola la posa iniziale dell'andatura di riferimento e la guardia la deve accettare.
bool autotest_nucleo() {
    nucleo::ParametriAndatura par;
    par.passo_x = nucleo::robot::andatura::passo;
    nucleo::Posa posa{};
    if (!nucleo::pose_tripode(par, 0.0f, posa)) {
        ESP_LOGE(TAG, "autotest: posa iniziale fuori portata, controllare robot_generato.hpp");
        return false;
    }
    const nucleo::Esito e = nucleo::Guardia().controlla({posa, nucleo::appoggio_tripode(0.0f)}, nullptr, 0.0f);
    if (!e.accettato) {
        ESP_LOGE(TAG, "autotest: la guardia rifiuta la posa iniziale (%s, zampa %d)", nucleo::nome_motivo(e.motivo),
                 e.zampa);
        return false;
    }
    // niente %f nei log: interi, cosi' non serve il printf con la virgola mobile
    ESP_LOGI(TAG, "autotest del nucleo: posa iniziale accettata, coppia stimata %d %% dello stallo, margine %d mm",
             static_cast<int>(std::lround(e.coppia_max * 100.0f)), static_cast<int>(std::lround(e.margine_stabilita_mm)));
    return true;
}

}  // namespace

extern "C" void app_main(void) {
    rail_spento();
    ESP_LOGI(TAG, "esapode %s, CAD \"%s\" (cad.json %.12s)", nucleo::robot::versione, nucleo::robot::documento_cad,
             nucleo::robot::cad_sha256);
    if (!autotest_nucleo()) {
        ESP_LOGE(TAG, "rail spento e compiti non avviati: il firmware non e' coerente con la descrizione del robot");
        return;
    }
    avvia_compiti();
}
