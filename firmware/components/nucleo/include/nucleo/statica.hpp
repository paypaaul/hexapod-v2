// Statica dei piedi in appoggio: carichi, coppie stimate e margine di stabilita', come calc/statica_tripode.py.
// Ipotesi del calcolo (le stesse di calc/): suolo piano, corpo orizzontale, niente accelerazioni, forze ai piedi
// verticali, peso proprio delle zampe non sottratto.
#pragma once

#include "nucleo/tipi.hpp"

namespace nucleo {

inline constexpr int MAX_APPOGGI = N_ZAMPE;

// Carico verticale su ciascun piede in appoggio (stessa unita' di peso). Con tre piedi e' la soluzione esatta di
// calc/statica_tripode.py -> carichi_piedi; con piu' di tre il problema e' iperstatico e si prende la ripartizione a
// norma minima (S, ipotesi: la ripartizione vera dipende dalle cedevolezze). false con meno di tre piedi o piedi
// allineati. Un carico negativo vuol dire baricentro fuori dal poligono d'appoggio.
bool carichi_piedi(const Vec2* piedi, int n, Vec2 baricentro, float peso, float* carichi);

// Distanza minima del baricentro dai lati del poligono d'appoggio (inviluppo convesso dei piedi), positiva dentro,
// come calc/statica_tripode.py -> margine_stabilita. -infinito con meno di tre piedi.
float margine_stabilita(const Vec2* piedi, int n, Vec2 baricentro);

// Coppie statiche al femore e al ginocchio di una zampa con il carico verticale dato (kgf -> kgf*cm), come
// calc/statica_tripode.py -> valuta: braccio = distanza orizzontale del piede dall'asse del giunto.
struct CoppieZampa {
    float femore_kgfcm;
    float ginocchio_kgfcm;
};
CoppieZampa coppie_zampa(int zampa, const AngoliZampa& a, const Vec3& piede_robot, float carico_kgf);

}  // namespace nucleo
