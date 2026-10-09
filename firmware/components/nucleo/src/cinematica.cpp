#include "nucleo/cinematica.hpp"

#include <cmath>

namespace nucleo {

namespace {

using robot::Lc;
using robot::Lf;
using robot::Lt;

float limita(float x, float lo, float hi) { return x < lo ? lo : (x > hi ? hi : x); }

// Matrice di rotazione Rz(imbardata) Ry(beccheggio) Rx(rollio), per righe.
struct Rotazione {
    float m[3][3];
};

Rotazione rotazione(const PosaCorpo& c) {
    const float cr = std::cos(rad(c.rollio)), sr = std::sin(rad(c.rollio));
    const float cp = std::cos(rad(c.beccheggio)), sp = std::sin(rad(c.beccheggio));
    const float cy = std::cos(rad(c.imbardata)), sy = std::sin(rad(c.imbardata));
    return {{{cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr},
             {sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr},
             {-sp, cp * sr, cp * cr}}};
}

}  // namespace

float normalizza_180(float g) {
    float w = std::fmod(g + 180.0f, 360.0f);
    if (w < 0.0f) {
        w += 360.0f;
    }
    return w - 180.0f;
}

Vec3 piede_zampa(const AngoliZampa& a) {
    const float alpha = rad(a.alpha);
    const float b = alpha - PI + rad(a.gamma);  // direzione della tibia: alpha - (180 - gamma)
    const float r = Lc + Lf * std::cos(alpha) + Lt * std::cos(b);
    const float z = Lf * std::sin(alpha) + Lt * std::sin(b);
    const float y = rad(a.imbardata);
    return {r * std::cos(y), r * std::sin(y), z};
}

Vec3 piede_robot(int zampa, const AngoliZampa& a) {
    const robot::Coxa& cx = robot::coxe[static_cast<size_t>(zampa)];
    const Vec3 p = piede_zampa(a);
    const float c = std::cos(rad(cx.direzione)), s = std::sin(rad(cx.direzione));
    return {cx.x + c * p.x - s * p.y, cx.y + s * p.x + c * p.y, p.z};
}

bool ik_piano(float x_f, float h, float& alpha, float& gamma) {
    const float d = std::hypot(x_f, h);
    // la forma negata respinge anche i NaN
    if (!(d <= Lf + Lt) || d < std::fabs(Lf - Lt) || d == 0.0f) {
        return false;
    }
    const float c = limita((Lf * Lf + d * d - Lt * Lt) / (2.0f * Lf * d), -1.0f, 1.0f);
    alpha = gradi(std::atan2(-h, x_f) + std::acos(c));
    const float cg = limita((Lf * Lf + Lt * Lt - d * d) / (2.0f * Lf * Lt), -1.0f, 1.0f);
    gamma = gradi(std::acos(cg));
    return true;
}

bool ik_robot(int zampa, const Vec3& p, AngoliZampa& out) {
    const robot::Coxa& cx = robot::coxe[static_cast<size_t>(zampa)];
    const float px = p.x - cx.x, py = p.y - cx.y;
    AngoliZampa a{};
    if (!ik_piano(std::hypot(px, py) - Lc, -p.z, a.alpha, a.gamma)) {
        return false;
    }
    a.imbardata = normalizza_180(gradi(std::atan2(py, px)) - cx.direzione);
    out = a;
    return true;
}

Vec3 appoggio_a_robot(const PosaCorpo& c, const Vec3& p) {
    const Rotazione r = rotazione(c);
    const Vec3 d = {p.x - c.x, p.y - c.y, p.z - c.z};
    // R^T d
    return {r.m[0][0] * d.x + r.m[1][0] * d.y + r.m[2][0] * d.z,
            r.m[0][1] * d.x + r.m[1][1] * d.y + r.m[2][1] * d.z,
            r.m[0][2] * d.x + r.m[1][2] * d.y + r.m[2][2] * d.z};
}

Vec3 robot_a_appoggio(const PosaCorpo& c, const Vec3& p) {
    const Rotazione r = rotazione(c);
    return {c.x + r.m[0][0] * p.x + r.m[0][1] * p.y + r.m[0][2] * p.z,
            c.y + r.m[1][0] * p.x + r.m[1][1] * p.y + r.m[1][2] * p.z,
            c.z + r.m[2][0] * p.x + r.m[2][1] * p.y + r.m[2][2] * p.z};
}

uint8_t ik_corpo(const PosaCorpo& c, const Piedi& piedi_appoggio, Posa& out) {
    uint8_t fuori = 0;
    for (int i = 0; i < N_ZAMPE; ++i) {
        const size_t k = static_cast<size_t>(i);
        if (!ik_robot(i, appoggio_a_robot(c, piedi_appoggio[k]), out[k])) {
            fuori = static_cast<uint8_t>(fuori | (1u << i));
        }
    }
    return fuori;
}

void diretta_corpo(const PosaCorpo& c, const Posa& posa, Piedi& piedi_appoggio) {
    for (int i = 0; i < N_ZAMPE; ++i) {
        const size_t k = static_cast<size_t>(i);
        piedi_appoggio[k] = robot_a_appoggio(c, piede_robot(i, posa[k]));
    }
}

}  // namespace nucleo
