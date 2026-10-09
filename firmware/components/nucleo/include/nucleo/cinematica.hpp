// Cinematica della zampa e del corpo (software.md 4.1). Formule di calc/statica_tripode.py -> ik_piano (soluzione a
// ginocchio alto) e di tools/descrizione.py; i test le confrontano 1:1 con il Python e con le pose lette dal CAD.
#pragma once

#include "nucleo/tipi.hpp"

namespace nucleo {

// Riporta un angolo in gradi in [-180, 180), come (x + 180) % 360 - 180 in Python.
float normalizza_180(float gradi);

// Punta del piede nella terna della zampa: origine sull'asse della coxa all'altezza del femore, X lungo la direzione
// neutra, ruotata dell'imbardata attorno a Z.
Vec3 piede_zampa(const AngoliZampa& a);

// Cinematica diretta: punta del piede nella terna del robot.
Vec3 piede_robot(int zampa, const AngoliZampa& a);

// Cinematica inversa nel piano della zampa: alpha e gamma con il piede a x_f dall'asse del femore e h sotto.
// false fuori portata (o con ingressi non finiti).
bool ik_piano(float x_f, float h, float& alpha, float& gamma);

// Cinematica inversa: angoli che portano la punta in p (terna del robot). false fuori portata.
bool ik_robot(int zampa, const Vec3& p, AngoliZampa& out);

// Posa del corpo rispetto alla terna d'appoggio: origine sul suolo sotto il centro del corpo nella posa neutra, X
// avanti, Y a sinistra, Z in alto. z e' l'altezza degli assi dei femori (l'origine della terna del robot) dal suolo;
// rotazioni in gradi, positive antiorarie attorno agli assi, applicate come Rz(imbardata) Ry(beccheggio) Rx(rollio).
// Con il beccheggio positivo il muso scende.
struct PosaCorpo {
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
    float rollio = 0.0f;
    float beccheggio = 0.0f;
    float imbardata = 0.0f;
};

// p_appoggio = t + R p_robot e il suo inverso.
Vec3 appoggio_a_robot(const PosaCorpo& c, const Vec3& p);
Vec3 robot_a_appoggio(const PosaCorpo& c, const Vec3& p);

// Cinematica inversa del corpo: angoli delle sei zampe con i piedi dati nella terna d'appoggio e il corpo in c.
// Ritorna la maschera delle zampe fuori portata (0 = tutte raggiunte); per quelle la posa resta invariata.
uint8_t ik_corpo(const PosaCorpo& c, const Piedi& piedi_appoggio, Posa& out);

// Cinematica diretta del corpo: piedi nella terna d'appoggio.
void diretta_corpo(const PosaCorpo& c, const Posa& posa, Piedi& piedi_appoggio);

}  // namespace nucleo
