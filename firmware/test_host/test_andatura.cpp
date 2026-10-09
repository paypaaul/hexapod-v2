// Generatore d'andatura (software.md 6.3, test 7): uguale alle pose del CAD e al Python, senza salti, piedi in
// appoggio fermi.
#include "comune.hpp"

using namespace nucleo;

extern "C" void setUp(void) {}
extern "C" void tearDown(void) {}

namespace {

constexpr float DT = 1.0f / robot::andatura::frequenza_hz;
// Periodo del ciclo per le prove a 50 Hz: il piu' lento dei cicli verificati (130/25) arriva a 249 gradi per ciclo
// sul giunto piu' veloce (calcolo con tools/riferimento.py), quindi con 1,2 s resta sotto i 250 gradi/s della guardia.
constexpr float PERIODO = 1.2f;
// Tolleranze di software.md 6.3: angoli uguali al Python entro 0,01 gradi, piedi in appoggio fermi entro 0,5 mm.
constexpr float TOLLERANZA_ANGOLI = 0.01f;
constexpr float TOLLERANZA_PIEDI_MM = 0.5f;
// Le pose del CAD sono arrotondate a 0,01 gradi: lo scarto atteso arriva a 0,005 piu' l'errore del float.
constexpr float TOLLERANZA_CAD = 0.006f;
constexpr uint32_t COPPIA = 1u << static_cast<unsigned>(Motivo::coppia);

// assieme.py -> pose_tripode ignora il passo quando c'e' il giro; il nucleo li somma.
ParametriAndatura parametri(const vettori::Ciclo& c) {
    ParametriAndatura p;
    p.h = c.h;
    p.xf0 = c.xf0;
    p.passo_x = c.giro != 0.0f ? 0.0f : c.passo;
    p.giro = c.giro;
    p.alzata = c.alzata;
    return p;
}

}  // namespace

static void test_uguale_ai_cicli_del_cad(void) {
    prova::Massimo m;
    for (const auto& c : vettori::cicli) {
        for (int i = c.prima; i < c.prima + c.fasi; ++i) {
            const auto& pc = vettori::pose_cicli[i];
            Posa p{};
            TEST_ASSERT_TRUE(pose_tripode(parametri(c), pc.fase, p));
            for (int z = 0; z < N_ZAMPE; ++z) {
                m(prova::scarto_angoli(p[static_cast<size_t>(z)], pc.angoli[z]));
            }
        }
    }
    std::printf("andatura contro i cicli del CAD (arrotondati a 0,01): scarto massimo %.5f gradi\n",
                static_cast<double>(m.valore));
    TEST_ASSERT_TRUE(m.valore <= TOLLERANZA_CAD);
}

static void test_uguale_al_python(void) {
    prova::Massimo m;
    for (const auto& r : vettori::andatura) {
        Posa p{};
        TEST_ASSERT_TRUE(pose_tripode(parametri(vettori::cicli[r.ciclo]), r.fase, p));
        for (int z = 0; z < N_ZAMPE; ++z) {
            m(prova::scarto_angoli(p[static_cast<size_t>(z)], r.angoli[z]));
        }
    }
    std::printf("andatura contro tools/riferimento.py: %d pose, scarto massimo %.5f gradi\n",
                prova::numero(vettori::andatura), static_cast<double>(m.valore));
    TEST_ASSERT_TRUE(m.valore <= TOLLERANZA_ANGOLI);
}

// A 50 Hz, tre cicli a parametri costanti: ogni fotogramma passa la guardia con il controllo di velocita' (a 70/70
// conta solo il rifiuto per la coppia, vedi test_guardia), e i piedi in appoggio, riportati a terra con
// l'odometria del corpo, restano fermi.
static void test_senza_salti_e_piedi_fermi(void) {
    const Guardia guardia;
    for (const auto& c : vettori::cicli) {
        GeneratoreTripode gen(parametri(c), PERIODO);
        const Vec3 v = gen.velocita_corpo();
        float xb = 0.0f, yb = 0.0f, th = 0.0f;  // posa del corpo a terra
        Posa prec{};
        bool primo = true;
        Vec3 inizio[N_ZAMPE] = {};
        bool in_corso[N_ZAMPE] = {};
        prova::Massimo salto, piedi;
        const int passi = static_cast<int>(3.0f * PERIODO / DT);
        for (int k = 0; k <= passi; ++k) {
            Piedi pa{};
            gen.piedi(pa);
            Posa p{};
            PosaCorpo corpo;
            corpo.z = gen.parametri().h;
            TEST_ASSERT_EQUAL_UINT8(0, ik_corpo(corpo, pa, p));
            const Esito e = guardia.controlla({p, gen.appoggio()}, primo ? nullptr : &prec, DT);
            TEST_ASSERT_EQUAL_UINT32(0, e.violazioni & ~COPPIA);
            for (int z = 0; z < N_ZAMPE && !primo; ++z) {
                salto(prova::scarto_angoli(p[static_cast<size_t>(z)], prec[static_cast<size_t>(z)]));
            }
            // piedi a terra: dalla posa dei giunti (cinematica diretta) alla terna del suolo
            const float ct = std::cos(rad(th)), st = std::sin(rad(th));
            for (int z = 0; z < N_ZAMPE; ++z) {
                const Vec3 q = robot_a_appoggio(corpo, piede_robot(z, p[static_cast<size_t>(z)]));
                const Vec3 suolo = {xb + ct * q.x - st * q.y, yb + st * q.x + ct * q.y, q.z};
                if (a_terra(gen.appoggio(), z)) {
                    if (!in_corso[z]) {
                        inizio[z] = suolo;
                        in_corso[z] = true;
                    }
                    piedi(prova::distanza(suolo, inizio[z]));
                } else {
                    in_corso[z] = false;
                }
            }
            prec = p;
            primo = false;
            gen.avanza(DT);
            th += v.z * DT;
            const float c2 = std::cos(rad(th)), s2 = std::sin(rad(th));
            xb += (c2 * v.x - s2 * v.y) * DT;
            yb += (s2 * v.x + c2 * v.y) * DT;
        }
        std::printf("ciclo %3.0f/%2.0f giro %2.0f a %.1f s: salto massimo %.2f gradi a fotogramma, piedi in appoggio "
                    "fermi entro %.4f mm\n",
                    static_cast<double>(c.h), static_cast<double>(c.xf0), static_cast<double>(c.giro),
                    static_cast<double>(PERIODO), static_cast<double>(salto.valore), static_cast<double>(piedi.valore));
        TEST_ASSERT_TRUE(salto.valore <= robot::guardia::velocita_gradi_s * DT);
        TEST_ASSERT_TRUE(piedi.valore <= TOLLERANZA_PIEDI_MM);
    }
}

// Partenza da fermo e arresto: i parametri cambiano in un ciclo e nessun fotogramma salta.
static void test_partenza_e_arresto(void) {
    const Guardia guardia;
    GeneratoreTripode gen(ParametriAndatura{}, PERIODO);
    ParametriAndatura avanti;
    avanti.passo_x = robot::andatura::passo;
    ParametriAndatura gira;
    gira.giro = robot::andatura::giro_max;
    Posa prec{};
    bool primo = true;
    prova::Massimo salto;
    int k = 0;
    const int per_comando = static_cast<int>(2.0f * PERIODO / DT);
    const ParametriAndatura comandi[] = {avanti, gira, ParametriAndatura{}};
    for (const auto& comando : comandi) {
        gen.comanda(comando, PERIODO);
        for (int i = 0; i < per_comando; ++i, ++k) {
            Posa p{};
            TEST_ASSERT_TRUE(pose_tripode(gen.parametri(), gen.fase(), p));
            const Esito e = guardia.controlla({p, gen.appoggio()}, primo ? nullptr : &prec, DT);
            if (!e.accettato) {
                std::printf("fotogramma %d rifiutato: %s\n", k, nome_motivo(e.motivo));
            }
            TEST_ASSERT_TRUE(e.accettato);
            for (int z = 0; z < N_ZAMPE && !primo; ++z) {
                salto(prova::scarto_angoli(p[static_cast<size_t>(z)], prec[static_cast<size_t>(z)]));
            }
            prec = p;
            primo = false;
            gen.avanza(DT);
        }
        TEST_ASSERT_FLOAT_WITHIN(1e-6f, comando.passo_x, gen.parametri().passo_x);
        TEST_ASSERT_FLOAT_WITHIN(1e-6f, comando.giro, gen.parametri().giro);
    }
    std::printf("avanti, rotazione, arresto a 100/45: %d fotogrammi, salto massimo %.2f gradi\n", k,
                static_cast<double>(salto.valore));
    TEST_ASSERT_TRUE(salto.valore <= robot::guardia::velocita_gradi_s * DT);
}

static void test_fase_continua(void) {
    GeneratoreTripode gen(ParametriAndatura{}, 1.0f, 0.95f);
    for (int i = 0; i < 10; ++i) {
        gen.avanza(DT);
        TEST_ASSERT_TRUE(gen.fase() >= 0.0f && gen.fase() < 1.0f);
    }
    TEST_ASSERT_FLOAT_WITHIN(1e-5f, 0.15f, gen.fase());
    gen.comanda(ParametriAndatura{}, 2.0f);  // il periodo cambia la velocita' della fase, non la fase
    TEST_ASSERT_FLOAT_WITHIN(1e-5f, 0.15f, gen.fase());
    gen.avanza(0.2f);
    TEST_ASSERT_FLOAT_WITHIN(1e-5f, 0.25f, gen.fase());
    gen.comanda(ParametriAndatura{}, -1.0f);  // periodo non valido: resta 2 s
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 2.0f, gen.periodo());
}

static void test_tripodi(void) {
    const Appoggio a = static_cast<Appoggio>((1u << robot::AS) | (1u << robot::PS) | (1u << robot::MD));
    TEST_ASSERT_EQUAL_UINT8(a, appoggio_tripode(0.1f));
    TEST_ASSERT_EQUAL_UINT8(static_cast<Appoggio>(0x3F & ~a), appoggio_tripode(0.6f));
    TEST_ASSERT_EQUAL_UINT8(a, appoggio_tripode(1.1f));
    TEST_ASSERT_EQUAL_UINT8(a, appoggio_tripode(-0.9f));
    // a fase 0,25 il tripode in appoggio e' nella posa neutra e l'altro e' alla massima alzata
    const ParametriAndatura p;
    const Vec3 giu = piede_tripode(robot::AS, p, 0.25f);
    const Vec3 su = piede_tripode(robot::AD, p, 0.25f);
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, 0.0f, giu.z);
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, p.alzata, su.z);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_uguale_ai_cicli_del_cad);
    RUN_TEST(test_uguale_al_python);
    RUN_TEST(test_senza_salti_e_piedi_fermi);
    RUN_TEST(test_partenza_e_arresto);
    RUN_TEST(test_fase_continua);
    RUN_TEST(test_tripodi);
    return UNITY_END();
}
