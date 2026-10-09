#include "nucleo/servo.hpp"

#include <cmath>

namespace nucleo {

Taratura taratura_predefinita() {
    Taratura t{};
    for (size_t z = 0; z < N_ZAMPE; ++z) {
        for (size_t j = 0; j < N_GIUNTI; ++j) {
            t[z][j] = {robot::servo::canali[z][j], robot::servo::verso[j], robot::servo::centro_us,
                       robot::servo::us_per_grado, robot::servo::calettamento[j]};
        }
    }
    return t;
}

float angolo_a_us(const TaraturaGiunto& t, float angolo) {
    return t.centro_us + static_cast<float>(t.verso) * t.us_per_grado * (angolo - t.calettamento);
}

float us_a_angolo(const TaraturaGiunto& t, float us) {
    return t.calettamento + (us - t.centro_us) / (static_cast<float>(t.verso) * t.us_per_grado);
}

void posa_a_impulsi(const Taratura& t, const Posa& p, Impulsi& out) {
    for (size_t z = 0; z < N_ZAMPE; ++z) {
        for (size_t j = 0; j < N_GIUNTI; ++j) {
            const float us = angolo_a_us(t[z][j], angolo(p[z], static_cast<int>(j)));
            out[z][j] = static_cast<uint16_t>(std::lround(us));
        }
    }
}

ModelloServo::ModelloServo(float velocita_gradi_s, float banda_morta_gradi)
    : velocita_gradi_s_(velocita_gradi_s), banda_morta_gradi_(banda_morta_gradi) {}

void ModelloServo::reimposta(float angolo) { previsto_ = angolo; }

float ModelloServo::aggiorna(float comando, float dt_s) {
    const float errore = comando - previsto_;
    if (std::fabs(errore) <= banda_morta_gradi_) {
        return previsto_;
    }
    const float passo = velocita_gradi_s_ * dt_s;
    previsto_ += errore > passo ? passo : (errore < -passo ? -passo : errore);
    return previsto_;
}

ModelloPosa::ModelloPosa(const Taratura& t) {
    const float velocita = 60.0f / robot::servo::velocita_s_60;
    for (size_t z = 0; z < N_ZAMPE; ++z) {
        for (size_t j = 0; j < N_GIUNTI; ++j) {
            servo_[z][j] = ModelloServo(velocita, robot::servo::banda_morta_us / t[z][j].us_per_grado);
        }
    }
}

void ModelloPosa::reimposta(const Posa& p) {
    prevista_ = p;
    for (size_t z = 0; z < N_ZAMPE; ++z) {
        for (size_t j = 0; j < N_GIUNTI; ++j) {
            servo_[z][j].reimposta(angolo(p[z], static_cast<int>(j)));
        }
    }
}

const Posa& ModelloPosa::aggiorna(const Posa& comando, float dt_s) {
    for (size_t z = 0; z < N_ZAMPE; ++z) {
        for (size_t j = 0; j < N_GIUNTI; ++j) {
            angolo(prevista_[z], static_cast<int>(j)) =
                servo_[z][j].aggiorna(angolo(comando[z], static_cast<int>(j)), dt_s);
        }
    }
    return prevista_;
}

}  // namespace nucleo
