// Guardia unica (software.md 2.5): ogni fotogramma, da qualunque sorgente (andatura, PC, politica), si controlla
// intero prima dell'invio alla SSC-32. Il singolo giunto non si tronca mai, perche' il piede striscerebbe: se il
// fotogramma viola un limite la guardia lo rifiuta con il motivo; chi comanda riduce il comando e ricalcola, oppure
// tiene il fotogramma precedente e registra l'evento.
#pragma once

#include <limits>

#include "nucleo/statica.hpp"
#include "nucleo/tipi.hpp"

namespace nucleo {

enum class Motivo : uint8_t {
    nessuno = 0,
    non_finito,    // angolo NaN o infinito
    imbardata,     // fuori da imbardata_min..max
    alpha,         // femore fuori da alpha_min..max
    gamma_min,     // ginocchio sotto tabella_gamma_min(alpha) + margine
    gamma_max,     // ginocchio oltre gamma_max
    corsa_servo,   // oltre +-corsa_servo dal calettamento
    somma_vicine,  // due vicine ruotate una verso l'altra oltre somma_vicine
    velocita,      // giunto piu' veloce di velocita_gradi_s rispetto al fotogramma precedente
    stabilita,     // baricentro a meno di stabilita_mm dai lati del poligono d'appoggio (o meno di tre piedi)
    coppia,        // coppia stimata oltre coppia_rifiuto dello stallo
};

const char* nome_motivo(Motivo m);

enum class LivelloCoppia : uint8_t { normale = 0, avviso, tempo_limitato, rifiuto };

// Limiti della guardia. rigidi() viene dalla repo (header generato) e non si cambia dalla rete; i limiti morbidi
// (in NVS) possono solo stringerli: stringi().
struct LimitiGuardia {
    float imbardata_min;
    float imbardata_max;
    float somma_vicine;
    float alpha_min;
    float alpha_max;
    float gamma_max;
    float gamma_margine;
    float corsa_servo;
    std::array<float, N_GIUNTI> calettamento;  // centro della corsa di ciascun servo, in angolo del giunto
    float velocita_gradi_s;
    float coppia_avviso;  // frazioni dello stallo
    float coppia_tempo_limitato;
    float coppia_rifiuto;
    float stabilita_mm;
    float massa_g;       // per i carichi sui piedi
    float stallo_kgfcm;  // alla tensione del rail
    Vec2 baricentro;     // nel piano, terna del robot

    static LimitiGuardia rigidi();
    // Il piu' stretto tra questi limiti e i morbidi, voce per voce (calettamento e baricentro restano questi).
    LimitiGuardia stringi(const LimitiGuardia& morbidi) const;
};

struct Fotogramma {
    Posa posa;
    Appoggio appoggio;  // piedi a terra; 0 = robot sospeso (cavalletto): niente coppie ne' stabilita'
};

struct Esito {
    bool accettato = true;
    // prima violazione trovata (ordine dei controlli: per zampa, poi vicine, velocita', stabilita', coppia)
    Motivo motivo = Motivo::nessuno;
    int8_t zampa = -1;   // -1 se non riguarda una zampa
    int8_t giunto = -1;  // 0 coxa, 1 femore, 2 ginocchio; -1 se non riguarda un giunto
    float valore = 0.0f;
    float limite = 0.0f;
    uint32_t violazioni = 0;  // bit (1 << Motivo) di tutte le violazioni trovate
    // statica, solo con piedi a terra
    LivelloCoppia livello_coppia = LivelloCoppia::normale;
    float coppia_max = 0.0f;  // frazione dello stallo sul giunto piu' caricato
    float margine_stabilita_mm = std::numeric_limits<float>::quiet_NaN();  // NaN se nessun piede e' a terra
    std::array<float, N_ZAMPE> carico_kgf{};
    std::array<CoppieZampa, N_ZAMPE> coppie{};

    bool viola(Motivo m) const { return (violazioni >> static_cast<unsigned>(m)) & 1u; }
};

class Guardia {
   public:
    explicit Guardia(const LimitiGuardia& limiti = LimitiGuardia::rigidi());

    // precedente: l'ultimo fotogramma accettato, oppure nullptr (niente controllo di velocita'); dt_s: tempo tra i due.
    Esito controlla(const Fotogramma& f, const Posa* precedente, float dt_s) const;

    const LimitiGuardia& limiti() const { return limiti_; }

    // Ginocchio minimo meccanico per il femore ad alpha (tabella_gamma_min, fra due righe il massimo dei due valori);
    // NaN fuori dalla tabella. Il limite della guardia e' questo piu' gamma_margine.
    static float gamma_min(float alpha);

   private:
    LimitiGuardia limiti_;
};

}  // namespace nucleo
