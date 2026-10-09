// GENERATO da tools/genera_header.py a partire da robot/robot.yaml e robot/cad.json: non modificare a mano.
// Si cambia robot.yaml (o si riesporta cad.json dal CAD) e si rigenera con: python3 tools/genera_header.py
// Unita': mm, g, gradi, microsecondi, secondi. Terne e angoli come in robot.yaml.
#pragma once

#include <array>
#include <cstdint>

namespace nucleo::robot {

// Origine dei dati
inline constexpr const char* versione = "2.1.0";
inline constexpr const char* documento_cad = "Hexapod v2.1.0 v3";
inline constexpr const char* cad_sha256 = "517ba75e95b7332a822525c9f4cc09a8edbf8832d8a00245b01660a489a66f30";

// Zampe nell'ordine di robot.yaml -> zampe
inline constexpr int N_ZAMPE = 6;
inline constexpr int N_GIUNTI = 3;  // coxa (imbardata), femore (alpha), ginocchio (gamma)
enum IndiceZampa : uint8_t { AS = 0, MS = 1, PS = 2, AD = 3, MD = 4, PD = 5 };
inline constexpr std::array<const char*, N_ZAMPE> nomi_zampe = {"AS", "MS", "PS", "AD", "MD", "PD"};

// Geometria della zampa (cad.json -> zampa)
inline constexpr float Lc = 55.0f;  // asse della coxa -> asse del femore
inline constexpr float Lf = 65.0f;  // asse del femore -> asse del ginocchio
inline constexpr float Lt = 110.0f;  // asse del ginocchio -> punta del piede

// Assi delle coxe nella terna del robot (cad.json -> coxe): x, y e direzione neutra in gradi da +X
struct Coxa {
    float x;
    float y;
    float direzione;
};
inline constexpr std::array<Coxa, N_ZAMPE> coxe = {{
    {80.0f, 44.0f, 30.0f},  // AS
    {0.0f, 48.0f, 90.0f},  // MS
    {-80.0f, 44.0f, 150.0f},  // PS
    {80.0f, -44.0f, -30.0f},  // AD
    {0.0f, -48.0f, -90.0f},  // MD
    {-80.0f, -44.0f, -150.0f},  // PD
}};

// Limiti meccanici (cad.json -> limiti_meccanici): campo libero misurato nel CAD, a gioco zero
namespace meccanici {
inline constexpr float imbardata_min = -35.0f;
inline constexpr float imbardata_max = 35.0f;
inline constexpr float alpha_min = -49.0f;
inline constexpr float alpha_max = 85.0f;
inline constexpr float gamma_min = 29.0f;
inline constexpr float gamma_max = 180.0f;
}  // namespace meccanici

// Ginocchio minimo meccanico in funzione del femore (cad.json -> limiti_meccanici.gamma_min), per alpha
// crescente. Fra due righe vale il massimo dei due valori (robot.yaml -> guardia.gamma_min_interpolazione).
struct RigaGammaMin {
    float alpha;
    float gamma;
};
inline constexpr std::array<RigaGammaMin, 19> tabella_gamma_min = {{
    {-45.0f, 54.0f},
    {-40.0f, 55.0f},
    {-35.0f, 45.0f},
    {-30.0f, 46.0f},
    {-25.0f, 46.0f},
    {-20.0f, 46.0f},
    {-15.0f, 45.0f},
    {-10.0f, 44.0f},
    {-5.0f, 43.0f},
    {0.0f, 43.0f},
    {5.0f, 41.0f},
    {10.0f, 39.0f},
    {15.0f, 39.0f},
    {20.0f, 37.0f},
    {25.0f, 35.0f},
    {30.0f, 33.0f},
    {35.0f, 31.0f},
    {40.0f, 29.0f},
    {85.0f, 29.0f},
}};

// Limiti della guardia del firmware (robot.yaml -> guardia, software.md 2.5)
namespace guardia {
inline constexpr float imbardata_min = -30.0f;
inline constexpr float imbardata_max = 30.0f;
inline constexpr float somma_vicine = 56.0f;  // massimo avvicinamento tra due vicine
inline constexpr float alpha_min = -45.0f;
inline constexpr float alpha_max = 82.0f;
inline constexpr float gamma_max = 177.0f;
inline constexpr float gamma_margine = 3.0f;  // sopra tabella_gamma_min
inline constexpr float corsa_servo = 80.0f;  // +- attorno al calettamento
inline constexpr float velocita_gradi_s = 250.0f;  // per giunto
inline constexpr float coppia_avviso = 0.55f;  // frazioni dello stallo
inline constexpr float coppia_tempo_limitato = 0.6f;
inline constexpr float coppia_rifiuto = 0.7f;
inline constexpr float stabilita_mm = 20.0f;  // baricentro dai lati del poligono d'appoggio
}  // namespace guardia

// Zampe vicine (robot.yaml -> vicine). avvicinamento = segno * (imbardata_a - imbardata_b): positivo quando le
// due zampe ruotano una verso l'altra; segno = +1 se a, ruotando in verso antiorario, va verso b.
struct Vicine {
    uint8_t a;
    uint8_t b;
    int8_t segno;
};
inline constexpr std::array<Vicine, 4> vicine = {{
    {AS, MS, 1},
    {MS, PS, 1},
    {AD, MD, -1},
    {MD, PD, -1},
}};

// Tripodi (robot.yaml -> tripodi): il primo e' in appoggio nella prima meta' del ciclo
inline constexpr std::array<std::array<uint8_t, 3>, 2> tripodi = {{
    {AS, PS, MD},
    {AD, PD, MS},
}};

// Servo (robot.yaml -> servo). Angolo del giunto -> impulso:
//     us = centro_us + verso[giunto] * us_per_grado * (angolo - calettamento[giunto])
namespace servo {
inline constexpr const char* modello = "MG996R AZDelivery";
// canali della SSC-32 per zampa: coxa, femore, ginocchio
inline constexpr std::array<std::array<uint8_t, N_GIUNTI>, N_ZAMPE> canali = {{
    {0, 1, 2},  // AS
    {6, 7, 8},  // MS
    {13, 14, 15},  // PS
    {16, 17, 18},  // AD
    {22, 23, 24},  // MD
    {29, 30, 31},  // PD
}};
inline constexpr std::array<int8_t, N_GIUNTI> verso = {1, -1, 1};
inline constexpr std::array<float, N_GIUNTI> calettamento = {0.0f, 20.0f, 100.0f};
inline constexpr float centro_us = 1500.0f;
inline constexpr float us_per_grado = 11.1f;
inline constexpr float banda_morta_us = 5.0f;
inline constexpr float periodo_ms = 20.0f;
inline constexpr float corsa_gradi = 160.0f;
inline constexpr float tensione_rail = 6.0f;
// a tensione_rail
inline constexpr float stallo_kgfcm = 11.0f;
inline constexpr float velocita_s_60 = 0.14f;  // secondi per 60 gradi, a vuoto
}  // namespace servo

// Andatura (robot.yaml -> andatura)
namespace andatura {
inline constexpr float frequenza_hz = 50.0f;  // ciclo di controllo
inline constexpr float h = 100.0f;  // altezza dell'asse dei femori dal suolo
inline constexpr float xf0 = 45.0f;  // piede neutro dall'asse del femore
inline constexpr float passo = 60.0f;
inline constexpr float alzata = 30.0f;
inline constexpr float giro_max = 30.0f;  // gradi a passo nella rotazione sul posto
struct Assetto {
    float h;
    float xf0;
};
inline constexpr std::array<Assetto, 4> assetti_verificati = {{{130.0f, 25.0f}, {100.0f, 45.0f}, {80.0f, 60.0f}, {70.0f, 70.0f}}};
}  // namespace andatura

// Masse (robot.yaml -> massa, cad.json -> masse)
namespace masse {
inline constexpr float attesa_g = 2945.0f;  // usata per le coppie stimate, come calc/statica_tripode.py
inline constexpr float modellato_g = 2624.6f;
inline constexpr float non_modellato_g = 360.0f;
inline constexpr float corpo_g = 1063.2f;
inline constexpr float coxa_g = 94.1f;
inline constexpr float femore_g = 54.4f;
inline constexpr float tibia_g = 111.7f;
}  // namespace masse

}  // namespace nucleo::robot
