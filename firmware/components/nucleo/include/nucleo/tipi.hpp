// Tipi comuni del nucleo: vettori, angoli di una zampa, posa del robot.
// Float a precisione singola ovunque: l'FPU dell'ESP32-S3 non fa il double (software.md 2.1).
#pragma once

#include <array>
#include <cstdint>

#include "nucleo/robot_generato.hpp"

namespace nucleo {

inline constexpr float PI = 3.14159265358979323846f;

constexpr float rad(float gradi) { return gradi * (PI / 180.0f); }
constexpr float gradi(float radianti) { return radianti * (180.0f / PI); }

struct Vec2 {
    float x;
    float y;
};

struct Vec3 {
    float x;
    float y;
    float z;
};

inline Vec3 operator+(const Vec3& a, const Vec3& b) { return {a.x + b.x, a.y + b.y, a.z + b.z}; }
inline Vec3 operator-(const Vec3& a, const Vec3& b) { return {a.x - b.x, a.y - b.y, a.z - b.z}; }

// Angoli di una zampa in gradi, come robot.yaml: imbardata dalla direzione neutra attorno a +Z, alpha del femore
// sopra l'orizzontale, gamma angolo interno al ginocchio (180 = distesa).
struct AngoliZampa {
    float imbardata;
    float alpha;
    float gamma;
};

inline constexpr int N_ZAMPE = robot::N_ZAMPE;
inline constexpr int N_GIUNTI = robot::N_GIUNTI;

using Posa = std::array<AngoliZampa, N_ZAMPE>;
using Piedi = std::array<Vec3, N_ZAMPE>;

// Zampe con il piede a terra: bit i = zampa i (ordine di robot.yaml -> zampe).
using Appoggio = uint8_t;

inline constexpr bool a_terra(Appoggio m, int zampa) { return (m >> zampa) & 1u; }

// Angolo del giunto j (0 coxa, 1 femore, 2 ginocchio) di una zampa.
inline float angolo(const AngoliZampa& a, int giunto) {
    return giunto == 0 ? a.imbardata : (giunto == 1 ? a.alpha : a.gamma);
}

inline float& angolo(AngoliZampa& a, int giunto) {
    return giunto == 0 ? a.imbardata : (giunto == 1 ? a.alpha : a.gamma);
}

}  // namespace nucleo
