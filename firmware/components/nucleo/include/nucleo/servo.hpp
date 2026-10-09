// Servo: conversione angolo del giunto -> impulso e modello del servo senza retroazione per la posa prevista
// (software.md 2.7 e 4.6).
#pragma once

#include "nucleo/tipi.hpp"

namespace nucleo {

// Taratura di un giunto. I valori di partenza vengono dalla repo (robot.yaml -> canali, servo); quelli veri dalla
// taratura con le dime (due punti, in NVS), che sostituisce centro_us e us_per_grado giunto per giunto.
struct TaraturaGiunto {
    uint8_t canale;      // SSC-32
    int8_t verso;        // segno di d(angolo)/d(impulso)
    float centro_us;     // impulso con il giunto al calettamento
    float us_per_grado;  // guadagno
    float calettamento;  // angolo del giunto a centro_us
};

using Taratura = std::array<std::array<TaraturaGiunto, N_GIUNTI>, N_ZAMPE>;
using Impulsi = std::array<std::array<uint16_t, N_GIUNTI>, N_ZAMPE>;

Taratura taratura_predefinita();

// us = centro_us + verso * us_per_grado * (angolo - calettamento)
float angolo_a_us(const TaraturaGiunto& t, float angolo);
float us_a_angolo(const TaraturaGiunto& t, float us);

// Impulsi interi per la SSC-32 (arrotondati al microsecondo). La posa deve essere gia' passata dalla guardia: con la
// corsa entro +-80 gradi dal calettamento gli impulsi stanno tra 612 e 2388 us.
void posa_a_impulsi(const Taratura& t, const Posa& p, Impulsi& out);

// Modello di un servo senza retroazione: il giunto insegue il comando alla velocita' massima a vuoto e non risponde
// a variazioni dentro la banda morta. Valori di partenza: 0,14 s/60 gradi a 6 V e banda morta 5 us (robot.yaml ->
// servo); l'identificazione dei servo (software.md 4.6) li sostituira'. Niente ritardo ne' gioco, per ora.
class ModelloServo {
   public:
    ModelloServo() = default;
    ModelloServo(float velocita_gradi_s, float banda_morta_gradi);

    void reimposta(float angolo);
    // Nuovo comando, tempo trascorso dal precedente: ritorna l'angolo previsto.
    float aggiorna(float comando, float dt_s);
    float previsto() const { return previsto_; }

   private:
    float velocita_gradi_s_ = 60.0f / robot::servo::velocita_s_60;
    float banda_morta_gradi_ = robot::servo::banda_morta_us / robot::servo::us_per_grado;
    float previsto_ = 0.0f;
};

// I 18 servo: posa prevista dalla posa comandata.
class ModelloPosa {
   public:
    explicit ModelloPosa(const Taratura& t = taratura_predefinita());

    void reimposta(const Posa& p);
    const Posa& aggiorna(const Posa& comando, float dt_s);
    const Posa& prevista() const { return prevista_; }

   private:
    std::array<std::array<ModelloServo, N_GIUNTI>, N_ZAMPE> servo_;
    Posa prevista_{};
};

}  // namespace nucleo
