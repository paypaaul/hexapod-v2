#include "nucleo/guardia.hpp"

#include <algorithm>
#include <cmath>
#include <limits>

#include "nucleo/cinematica.hpp"

namespace nucleo {

namespace {

constexpr float NaN = std::numeric_limits<float>::quiet_NaN();

void registra(Esito& e, Motivo m, int zampa, int giunto, float valore, float limite) {
    e.violazioni |= 1u << static_cast<unsigned>(m);
    if (e.accettato) {
        e.accettato = false;
        e.motivo = m;
        e.zampa = static_cast<int8_t>(zampa);
        e.giunto = static_cast<int8_t>(giunto);
        e.valore = valore;
        e.limite = limite;
    }
}

}  // namespace

const char* nome_motivo(Motivo m) {
    switch (m) {
        case Motivo::nessuno: return "nessuno";
        case Motivo::non_finito: return "non_finito";
        case Motivo::imbardata: return "imbardata";
        case Motivo::alpha: return "alpha";
        case Motivo::gamma_min: return "gamma_min";
        case Motivo::gamma_max: return "gamma_max";
        case Motivo::corsa_servo: return "corsa_servo";
        case Motivo::somma_vicine: return "somma_vicine";
        case Motivo::velocita: return "velocita";
        case Motivo::stabilita: return "stabilita";
        case Motivo::coppia: return "coppia";
    }
    return "?";
}

LimitiGuardia LimitiGuardia::rigidi() {
    namespace g = robot::guardia;
    LimitiGuardia l{};
    l.imbardata_min = g::imbardata_min;
    l.imbardata_max = g::imbardata_max;
    l.somma_vicine = g::somma_vicine;
    l.alpha_min = g::alpha_min;
    l.alpha_max = g::alpha_max;
    l.gamma_max = g::gamma_max;
    l.gamma_margine = g::gamma_margine;
    l.corsa_servo = g::corsa_servo;
    l.calettamento = robot::servo::calettamento;
    l.velocita_gradi_s = g::velocita_gradi_s;
    l.coppia_avviso = g::coppia_avviso;
    l.coppia_tempo_limitato = g::coppia_tempo_limitato;
    l.coppia_rifiuto = g::coppia_rifiuto;
    l.stabilita_mm = g::stabilita_mm;
    l.massa_g = robot::masse::attesa_g;
    l.stallo_kgfcm = robot::servo::stallo_kgfcm;
    // baricentro al centro del corpo, come calc/statica_tripode.py -> CONFIG['com_xy'] (robot.yaml non lo da' ancora)
    l.baricentro = {0.0f, 0.0f};
    return l;
}

LimitiGuardia LimitiGuardia::stringi(const LimitiGuardia& m) const {
    LimitiGuardia l = *this;
    l.imbardata_min = std::max(imbardata_min, m.imbardata_min);
    l.imbardata_max = std::min(imbardata_max, m.imbardata_max);
    l.somma_vicine = std::min(somma_vicine, m.somma_vicine);
    l.alpha_min = std::max(alpha_min, m.alpha_min);
    l.alpha_max = std::min(alpha_max, m.alpha_max);
    l.gamma_max = std::min(gamma_max, m.gamma_max);
    l.gamma_margine = std::max(gamma_margine, m.gamma_margine);
    l.corsa_servo = std::min(corsa_servo, m.corsa_servo);
    l.velocita_gradi_s = std::min(velocita_gradi_s, m.velocita_gradi_s);
    l.coppia_avviso = std::min(coppia_avviso, m.coppia_avviso);
    l.coppia_tempo_limitato = std::min(coppia_tempo_limitato, m.coppia_tempo_limitato);
    l.coppia_rifiuto = std::min(coppia_rifiuto, m.coppia_rifiuto);
    l.stabilita_mm = std::max(stabilita_mm, m.stabilita_mm);
    // piu' massa e meno stallo danno coppie stimate piu' alte: piu' prudenti
    l.massa_g = std::max(massa_g, m.massa_g);
    l.stallo_kgfcm = std::min(stallo_kgfcm, m.stallo_kgfcm);
    return l;
}

Guardia::Guardia(const LimitiGuardia& limiti) : limiti_(limiti) {}

float Guardia::gamma_min(float alpha) {
    const auto& t = robot::tabella_gamma_min;
    if (!(alpha >= t.front().alpha && alpha <= t.back().alpha)) {
        return NaN;
    }
    for (size_t i = 0; i + 1 < t.size(); ++i) {
        if (alpha == t[i].alpha) {
            return t[i].gamma;
        }
        if (alpha > t[i].alpha && alpha < t[i + 1].alpha) {
            // la tabella non e' monotona (-40 -> 55, -35 -> 45): fra due righe vale il massimo
            return std::max(t[i].gamma, t[i + 1].gamma);
        }
    }
    return t.back().gamma;
}

Esito Guardia::controlla(const Fotogramma& f, const Posa* precedente, float dt_s) const {
    const LimitiGuardia& l = limiti_;
    Esito e;
    bool finiti = true;

    for (int z = 0; z < N_ZAMPE; ++z) {
        const AngoliZampa& a = f.posa[static_cast<size_t>(z)];
        if (!std::isfinite(a.imbardata) || !std::isfinite(a.alpha) || !std::isfinite(a.gamma)) {
            registra(e, Motivo::non_finito, z, -1, NaN, NaN);
            finiti = false;
            continue;
        }
        if (a.imbardata < l.imbardata_min) {
            registra(e, Motivo::imbardata, z, 0, a.imbardata, l.imbardata_min);
        } else if (a.imbardata > l.imbardata_max) {
            registra(e, Motivo::imbardata, z, 0, a.imbardata, l.imbardata_max);
        }
        if (a.alpha < l.alpha_min) {
            registra(e, Motivo::alpha, z, 1, a.alpha, l.alpha_min);
        } else if (a.alpha > l.alpha_max) {
            registra(e, Motivo::alpha, z, 1, a.alpha, l.alpha_max);
        }
        const float g_min = gamma_min(a.alpha) + l.gamma_margine;
        if (!(a.gamma >= g_min)) {  // NaN fuori tabella: rifiuto
            registra(e, Motivo::gamma_min, z, 2, a.gamma, g_min);
        }
        if (a.gamma > l.gamma_max) {
            registra(e, Motivo::gamma_max, z, 2, a.gamma, l.gamma_max);
        }
        for (int j = 0; j < N_GIUNTI; ++j) {
            const float d = angolo(a, j) - l.calettamento[static_cast<size_t>(j)];
            if (std::fabs(d) > l.corsa_servo) {
                registra(e, Motivo::corsa_servo, z, j, angolo(a, j),
                         l.calettamento[static_cast<size_t>(j)] + (d > 0 ? l.corsa_servo : -l.corsa_servo));
            }
        }
    }
    if (!finiti) {
        return e;  // senza angoli validi i controlli che seguono non hanno senso
    }

    for (const robot::Vicine& v : robot::vicine) {
        const float s = static_cast<float>(v.segno) * (f.posa[v.a].imbardata - f.posa[v.b].imbardata);
        if (s > l.somma_vicine) {
            registra(e, Motivo::somma_vicine, v.a, 0, s, l.somma_vicine);
        }
    }

    if (precedente != nullptr) {
        const float massimo = l.velocita_gradi_s * dt_s;
        for (int z = 0; z < N_ZAMPE; ++z) {
            for (int j = 0; j < N_GIUNTI; ++j) {
                const float d =
                    std::fabs(angolo(f.posa[static_cast<size_t>(z)], j) - angolo((*precedente)[static_cast<size_t>(z)], j));
                if (!(d <= massimo)) {
                    registra(e, Motivo::velocita, z, j, dt_s > 0.0f ? d / dt_s : NaN, l.velocita_gradi_s);
                }
            }
        }
    }

    if (f.appoggio != 0) {
        Vec2 piedi[MAX_APPOGGI];
        Vec3 piedi3[MAX_APPOGGI];
        int indice[MAX_APPOGGI];
        int n = 0;
        for (int z = 0; z < N_ZAMPE; ++z) {
            if (a_terra(f.appoggio, z)) {
                piedi3[n] = piede_robot(z, f.posa[static_cast<size_t>(z)]);
                piedi[n] = {piedi3[n].x, piedi3[n].y};
                indice[n] = z;
                ++n;
            }
        }
        // assunzione di calc/: corpo orizzontale, quindi il piano XY del robot e' quello del suolo
        e.margine_stabilita_mm = margine_stabilita(piedi, n, l.baricentro);
        if (!(e.margine_stabilita_mm >= l.stabilita_mm)) {
            registra(e, Motivo::stabilita, -1, -1, e.margine_stabilita_mm, l.stabilita_mm);
        }
        float carichi[MAX_APPOGGI];
        if (carichi_piedi(piedi, n, l.baricentro, l.massa_g / 1000.0f, carichi)) {
            float massimo = 0.0f;
            for (int k = 0; k < n; ++k) {
                const size_t z = static_cast<size_t>(indice[k]);
                e.carico_kgf[z] = carichi[k];
                e.coppie[z] = coppie_zampa(indice[k], f.posa[z], piedi3[k], carichi[k]);
                massimo = std::max(massimo, std::max(e.coppie[z].femore_kgfcm, e.coppie[z].ginocchio_kgfcm));
            }
            e.coppia_max = massimo / l.stallo_kgfcm;
            if (e.coppia_max > l.coppia_rifiuto) {
                e.livello_coppia = LivelloCoppia::rifiuto;
                registra(e, Motivo::coppia, -1, -1, e.coppia_max, l.coppia_rifiuto);
            } else if (e.coppia_max > l.coppia_tempo_limitato) {
                e.livello_coppia = LivelloCoppia::tempo_limitato;
            } else if (e.coppia_max > l.coppia_avviso) {
                e.livello_coppia = LivelloCoppia::avviso;
            }
        }
    }
    return e;
}

}  // namespace nucleo
