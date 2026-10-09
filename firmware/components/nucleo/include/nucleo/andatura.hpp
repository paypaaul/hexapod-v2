// Andatura a tripode (software.md 4.2), identica a cad/script/assieme.py -> pose_tripode: il piede in appoggio va
// in linea retta da +passo/2 a -passo/2 (o su un arco attorno al centro del corpo nella rotazione sul posto), in volo
// torna avanti alzandosi di alzata * sin(pi v). La fase e' continua (0..1), non a passi: la pose_tripode del CAD e'
// la stessa funzione valutata a 8 o 16 fasi.
#pragma once

#include "nucleo/cinematica.hpp"
#include "nucleo/tipi.hpp"

namespace nucleo {

struct ParametriAndatura {
    float h = robot::andatura::h;      // altezza degli assi dei femori dal suolo
    float xf0 = robot::andatura::xf0;  // piede neutro dall'asse del femore, lungo la direzione neutra
    float passo_x = 0.0f;              // mm a passo, avanti
    float passo_y = 0.0f;              // mm a passo, a sinistra
    float giro = 0.0f;                 // gradi a passo, antiorario
    float alzata = robot::andatura::alzata;
};

// Fase propria della zampa: il primo tripode di robot.yaml ha la fase del ciclo, l'altro e' sfasato di mezzo ciclo.
float fase_zampa(int zampa, float fase);
// In appoggio nella prima meta' della propria fase.
bool in_appoggio(int zampa, float fase);
Appoggio appoggio_tripode(float fase);

// Punta del piede nella terna d'appoggio (z = quota dal suolo). Il piede in appoggio si sposta di k * passo e ruota
// di k * giro attorno al centro del corpo, con k da +0,5 a -0,5. pose_tripode del CAD ignora il passo quando c'e' il
// giro: qui si sommano, e i cicli di rotazione del CAD si riproducono con passo 0.
Vec3 piede_tripode(int zampa, const ParametriAndatura& p, float fase);

// Pose come assieme.py -> pose_tripode: corpo orizzontale con gli assi dei femori a quota h. false se un piede e'
// fuori portata (out resta invariato per quella zampa).
bool pose_tripode(const ParametriAndatura& p, float fase, Posa& out);

// Generatore a fase continua. I parametri nuovi si raggiungono in linea retta in un ciclo, cosi' ogni zampa fa un
// appoggio e un volo durante il cambio e i piedi non saltano; il periodo cambia subito (cambia solo la velocita'
// della fase, non la posizione). Il periodo e' sempre positivo: un periodo <= 0 non viene accettato e resta il
// precedente. Per stare fermi si comandano passo e giro nulli (le zampe continuano ad alzarsi a turno): stare in piedi
// senza passi e' uno stato della macchina a stati, non dell'andatura.
class GeneratoreTripode {
   public:
    explicit GeneratoreTripode(const ParametriAndatura& p = {}, float periodo_s = 1.0f, float fase = 0.0f);

    void comanda(const ParametriAndatura& obiettivo, float periodo_s);
    void avanza(float dt_s);

    float fase() const { return fase_; }
    float periodo() const { return periodo_; }
    const ParametriAndatura& parametri() const { return attuali_; }

    // Piedi nella terna d'appoggio e zampe in appoggio alla fase attuale.
    void piedi(Piedi& out) const;
    Appoggio appoggio() const { return appoggio_tripode(fase_); }

    // Velocita' del corpo che tiene fermi i piedi in appoggio, a parametri costanti: x e y in mm/s nella terna del
    // corpo, z = velocita' d'imbardata in gradi/s.
    Vec3 velocita_corpo() const;

   private:
    ParametriAndatura attuali_;
    ParametriAndatura partenza_;
    ParametriAndatura obiettivo_;
    float periodo_;
    float fase_;
    float durata_rampa_;
    float t_rampa_;
};

}  // namespace nucleo
