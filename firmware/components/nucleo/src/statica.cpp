#include "nucleo/statica.hpp"

#include <cmath>
#include <limits>

#include "nucleo/cinematica.hpp"

namespace nucleo {

namespace {

// Le equazioni dei momenti si scrivono in decimetri: con i millimetri le righe di A valgono 1 e circa 200, e in
// float il sistema a norma minima (A A^T) perderebbe cifre. I carichi non dipendono dalla scala.
constexpr float SCALA_MM = 100.0f;
// Determinante sotto cui i piedi si considerano allineati, con le coordinate in decimetri: per tre piedi vale il
// doppio dell'area del triangolo, e un triangolo alto 1 mm su 200 mm di base da' 0,02 (calcolo); 1e-6 scarta solo i
// casi degeneri.
constexpr float DET_MIN = 1e-6f;

float det3(const float m[3][3]) {
    return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
           m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
}

// Regola di Cramer, come calc/statica_tripode.py -> risolvi3.
bool risolvi3(const float a[3][3], const float b[3], float x[3]) {
    const float d = det3(a);
    if (!(std::fabs(d) >= DET_MIN)) {
        return false;
    }
    for (int k = 0; k < 3; ++k) {
        float m[3][3];
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                m[i][j] = (j == k) ? b[i] : a[i][j];
            }
        }
        x[k] = det3(m) / d;
    }
    return true;
}

float croce(Vec2 o, Vec2 a, Vec2 b) { return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x); }

}  // namespace

bool carichi_piedi(const Vec2* piedi, int n, Vec2 baricentro, float peso, float* carichi) {
    if (n < 3 || n > MAX_APPOGGI) {
        return false;
    }
    float r[3][MAX_APPOGGI];
    for (int i = 0; i < n; ++i) {
        r[0][i] = 1.0f;
        r[1][i] = (piedi[i].x - baricentro.x) / SCALA_MM;
        r[2][i] = (piedi[i].y - baricentro.y) / SCALA_MM;
    }
    const float b[3] = {peso, 0.0f, 0.0f};
    if (n == 3) {
        const float a[3][3] = {{r[0][0], r[0][1], r[0][2]}, {r[1][0], r[1][1], r[1][2]}, {r[2][0], r[2][1], r[2][2]}};
        return risolvi3(a, b, carichi);
    }
    // norma minima: f = A^T (A A^T)^-1 b
    float m[3][3];
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            float s = 0.0f;
            for (int k = 0; k < n; ++k) {
                s += r[i][k] * r[j][k];
            }
            m[i][j] = s;
        }
    }
    float lambda[3];
    if (!risolvi3(m, b, lambda)) {
        return false;
    }
    for (int k = 0; k < n; ++k) {
        carichi[k] = r[0][k] * lambda[0] + r[1][k] * lambda[1] + r[2][k] * lambda[2];
    }
    return true;
}

float margine_stabilita(const Vec2* piedi, int n, Vec2 baricentro) {
    if (n < 3 || n > MAX_APPOGGI) {
        return -std::numeric_limits<float>::infinity();
    }
    // inviluppo convesso in senso antiorario (catena monotona) su al piu' sei punti
    Vec2 p[MAX_APPOGGI];
    for (int i = 0; i < n; ++i) {
        p[i] = piedi[i];
    }
    for (int i = 1; i < n; ++i) {
        const Vec2 v = p[i];
        int j = i - 1;
        while (j >= 0 && (p[j].x > v.x || (p[j].x == v.x && p[j].y > v.y))) {
            p[j + 1] = p[j];
            --j;
        }
        p[j + 1] = v;
    }
    Vec2 h[2 * MAX_APPOGGI];
    int k = 0;
    for (int i = 0; i < n; ++i) {
        while (k >= 2 && croce(h[k - 2], h[k - 1], p[i]) <= 0.0f) {
            --k;
        }
        h[k++] = p[i];
    }
    for (int i = n - 2, t = k + 1; i >= 0; --i) {
        while (k >= t && croce(h[k - 2], h[k - 1], p[i]) <= 0.0f) {
            --k;
        }
        h[k++] = p[i];
    }
    const int m = k - 1;  // l'ultimo punto ripete il primo
    if (m < 3) {
        return -std::numeric_limits<float>::infinity();
    }
    float minimo = std::numeric_limits<float>::infinity();
    for (int i = 0; i < m; ++i) {
        const Vec2 a = h[i], b = h[i + 1];
        const float l = std::hypot(b.x - a.x, b.y - a.y);
        const float s = croce(a, b, baricentro) / l;  // positiva a sinistra del lato, cioe' dentro
        minimo = s < minimo ? s : minimo;
    }
    return minimo;
}

CoppieZampa coppie_zampa(int zampa, const AngoliZampa& a, const Vec3& piede, float carico_kgf) {
    const robot::Coxa& cx = robot::coxe[static_cast<size_t>(zampa)];
    const float x_f = std::hypot(piede.x - cx.x, piede.y - cx.y) - robot::Lc;
    const float x_k = robot::Lf * std::cos(rad(a.alpha));
    // kgf * mm / 10 = kgf * cm
    return {std::fabs(carico_kgf * x_f) / 10.0f, std::fabs(carico_kgf * (x_f - x_k)) / 10.0f};
}

}  // namespace nucleo
