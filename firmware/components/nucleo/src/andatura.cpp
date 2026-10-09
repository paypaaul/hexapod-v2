#include "nucleo/andatura.hpp"

#include <cmath>

namespace nucleo {

namespace {

float in_ciclo(float fase) {
    float f = std::fmod(fase, 1.0f);
    if (f < 0.0f) {
        f += 1.0f;
    }
    return f;
}

bool nel_primo_tripode(int zampa) {
    for (uint8_t z : robot::tripodi[0]) {
        if (z == zampa) {
            return true;
        }
    }
    return false;
}

float verso(float da, float a, float s) { return da + (a - da) * s; }

}  // namespace

float fase_zampa(int zampa, float fase) {
    return nel_primo_tripode(zampa) ? in_ciclo(fase) : in_ciclo(fase + 0.5f);
}

bool in_appoggio(int zampa, float fase) { return fase_zampa(zampa, fase) < 0.5f; }

Appoggio appoggio_tripode(float fase) {
    Appoggio m = 0;
    for (int z = 0; z < N_ZAMPE; ++z) {
        if (in_appoggio(z, fase)) {
            m = static_cast<Appoggio>(m | (1u << z));
        }
    }
    return m;
}

Vec3 piede_tripode(int zampa, const ParametriAndatura& p, float fase) {
    const robot::Coxa& c = robot::coxe[static_cast<size_t>(zampa)];
    const float r = robot::Lc + p.xf0;
    float fx = c.x + r * std::cos(rad(c.direzione));
    float fy = c.y + r * std::sin(rad(c.direzione));
    const float u = fase_zampa(zampa, fase);
    float k, dz;
    if (u < 0.5f) {  // appoggio: da +passo/2 a -passo/2
        k = 0.5f - u / 0.5f;
        dz = 0.0f;
    } else {  // volo: torna avanti alzandosi
        const float v = (u - 0.5f) / 0.5f;
        k = -0.5f + v;
        dz = p.alzata * std::sin(PI * v);
    }
    if (p.giro != 0.0f) {  // nella terna del corpo il piede in appoggio gira in senso opposto al corpo
        const float g = rad(p.giro * k);
        const float cg = std::cos(g), sg = std::sin(g);
        const float x = fx * cg - fy * sg;
        fy = fx * sg + fy * cg;
        fx = x;
    }
    return {fx + p.passo_x * k, fy + p.passo_y * k, dz};
}

bool pose_tripode(const ParametriAndatura& p, float fase, Posa& out) {
    bool ok = true;
    for (int z = 0; z < N_ZAMPE; ++z) {
        const Vec3 q = piede_tripode(z, p, fase);
        ok = ik_robot(z, {q.x, q.y, q.z - p.h}, out[static_cast<size_t>(z)]) && ok;
    }
    return ok;
}

GeneratoreTripode::GeneratoreTripode(const ParametriAndatura& p, float periodo_s, float fase)
    : attuali_(p),
      partenza_(p),
      obiettivo_(p),
      periodo_(periodo_s > 0.0f ? periodo_s : 1.0f),
      fase_(in_ciclo(fase)),
      durata_rampa_(0.0f),
      t_rampa_(0.0f) {}

void GeneratoreTripode::comanda(const ParametriAndatura& obiettivo, float periodo_s) {
    if (periodo_s > 0.0f) {
        periodo_ = periodo_s;
    }
    partenza_ = attuali_;
    obiettivo_ = obiettivo;
    durata_rampa_ = periodo_;
    t_rampa_ = 0.0f;
}

void GeneratoreTripode::avanza(float dt_s) {
    fase_ = in_ciclo(fase_ + dt_s / periodo_);
    if (t_rampa_ < durata_rampa_) {
        t_rampa_ += dt_s;
        const float s = t_rampa_ >= durata_rampa_ ? 1.0f : t_rampa_ / durata_rampa_;
        attuali_.h = verso(partenza_.h, obiettivo_.h, s);
        attuali_.xf0 = verso(partenza_.xf0, obiettivo_.xf0, s);
        attuali_.passo_x = verso(partenza_.passo_x, obiettivo_.passo_x, s);
        attuali_.passo_y = verso(partenza_.passo_y, obiettivo_.passo_y, s);
        attuali_.giro = verso(partenza_.giro, obiettivo_.giro, s);
        attuali_.alzata = verso(partenza_.alzata, obiettivo_.alzata, s);
        if (s >= 1.0f) {
            attuali_ = obiettivo_;  // esatto, senza residui dell'interpolazione
        }
    }
}

void GeneratoreTripode::piedi(Piedi& out) const {
    for (int z = 0; z < N_ZAMPE; ++z) {
        out[static_cast<size_t>(z)] = piede_tripode(z, attuali_, fase_);
    }
}

Vec3 GeneratoreTripode::velocita_corpo() const {
    // in appoggio il piede percorre il passo (o il giro) in mezzo ciclo
    const float f = 2.0f / periodo_;
    return {attuali_.passo_x * f, attuali_.passo_y * f, attuali_.giro * f};
}

}  // namespace nucleo
