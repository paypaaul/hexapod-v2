// Strumenti comuni dei test del nucleo.
#pragma once

#include <cmath>
#include <cstddef>
#include <cstdio>

#include "nucleo/nucleo.hpp"
#include "unity.h"
#include "vettori_generati.hpp"

namespace prova {

template <typename T, std::size_t N>
constexpr int numero(const T (&)[N]) {
    return static_cast<int>(N);
}

inline nucleo::AngoliZampa angoli(const float a[3]) { return {a[0], a[1], a[2]}; }

inline nucleo::Posa posa(const float a[nucleo::N_ZAMPE][3]) {
    nucleo::Posa p{};
    for (int z = 0; z < nucleo::N_ZAMPE; ++z) {
        p[static_cast<std::size_t>(z)] = angoli(a[z]);
    }
    return p;
}

inline float distanza(const nucleo::Vec3& a, const float b[3]) {
    return std::sqrt((a.x - b[0]) * (a.x - b[0]) + (a.y - b[1]) * (a.y - b[1]) + (a.z - b[2]) * (a.z - b[2]));
}

inline float distanza(const nucleo::Vec3& a, const nucleo::Vec3& b) {
    const float v[3] = {b.x, b.y, b.z};
    return distanza(a, v);
}

// Scarto massimo tra due angoli dei tre giunti (l'imbardata a meno di giri interi).
inline float scarto_angoli(const nucleo::AngoliZampa& a, const float b[3]) {
    const float di = std::fabs(nucleo::normalizza_180(a.imbardata - b[0]));
    const float da = std::fabs(a.alpha - b[1]);
    const float dg = std::fabs(a.gamma - b[2]);
    return std::fmax(di, std::fmax(da, dg));
}

inline float scarto_angoli(const nucleo::AngoliZampa& a, const nucleo::AngoliZampa& b) {
    const float v[3] = {b.imbardata, b.alpha, b.gamma};
    return scarto_angoli(a, v);
}

struct Massimo {
    float valore = 0.0f;
    void operator()(float x) {
        if (!(x <= valore)) {
            valore = x;  // anche NaN, cosi' il test fallisce
        }
    }
};

// Posa in piedi a quota h con i piedi neutri a xf0 (tutte le zampe a terra), dentro tutti i limiti a 100/45.
inline nucleo::Posa in_piedi(float h = nucleo::robot::andatura::h, float xf0 = nucleo::robot::andatura::xf0) {
    nucleo::Posa p{};
    for (int z = 0; z < nucleo::N_ZAMPE; ++z) {
        float a = 0.0f, g = 0.0f;
        nucleo::ik_piano(xf0, h, a, g);
        p[static_cast<std::size_t>(z)] = {0.0f, a, g};
    }
    return p;
}

}  // namespace prova
