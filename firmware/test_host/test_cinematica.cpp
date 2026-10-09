// Cinematica del nucleo contro il CAD (robot/pose_cad.json) e contro tools/descrizione.py (software.md 6.3, test 1-2).
#include "comune.hpp"

using namespace nucleo;

extern "C" void setUp(void) {}
extern "C" void tearDown(void) {}

// Tolleranze di software.md 6.3: diretta uguale al CAD entro 0,05 mm, angoli uguali al Python entro 0,01 gradi.
constexpr float TOLLERANZA_CAD_MM = 0.05f;
constexpr float TOLLERANZA_ANGOLI = 0.01f;
// Diretta float contro diretta double di tools/descrizione.py: l'errore atteso del float su ~300 mm e' circa 1e-4 mm.
constexpr float TOLLERANZA_PYTHON_MM = 0.001f;

static void test_diretta_uguale_al_cad(void) {
    prova::Massimo m;
    for (const auto& p : vettori::pose_cad) {
        m(prova::distanza(piede_robot(p.zampa, prova::angoli(p.angoli)), p.punta));
    }
    std::printf("diretta contro CAD: %d pose, scarto massimo %.5f mm\n", prova::numero(vettori::pose_cad), m.valore);
    TEST_ASSERT_TRUE(m.valore <= TOLLERANZA_CAD_MM);
}

static void test_diretta_uguale_al_python(void) {
    prova::Massimo m;
    for (const auto& p : vettori::griglia) {
        m(prova::distanza(piede_robot(p.zampa, prova::angoli(p.angoli)), p.punta));
    }
    std::printf("diretta contro Python: %d punti, scarto massimo %.6f mm\n", prova::numero(vettori::griglia), m.valore);
    TEST_ASSERT_TRUE(m.valore <= TOLLERANZA_PYTHON_MM);
}

static void test_inversa_andata_e_ritorno(void) {
    prova::Massimo angoli, punte;
    for (const auto& p : vettori::griglia) {
        AngoliZampa a{};
        const Vec3 punta = {p.punta[0], p.punta[1], p.punta[2]};
        TEST_ASSERT_TRUE(ik_robot(p.zampa, punta, a));
        angoli(prova::scarto_angoli(a, p.angoli));
        punte(prova::distanza(piede_robot(p.zampa, a), p.punta));
    }
    std::printf("inversa contro Python: scarto massimo %.5f gradi; diretta(inversa(p)) - p: %.6f mm\n", angoli.valore,
                punte.valore);
    TEST_ASSERT_TRUE(angoli.valore <= TOLLERANZA_ANGOLI);
    TEST_ASSERT_TRUE(punte.valore <= TOLLERANZA_PYTHON_MM);
}

static void test_inversa_delle_pose_del_cad(void) {
    // le pose del CAD dentro il campo della soluzione a ginocchio alto (gamma < 180, piede fuori dall'asse della coxa)
    prova::Massimo m;
    int n = 0;
    for (const auto& p : vettori::pose_cad) {
        const Vec3 punta = {p.punta[0], p.punta[1], p.punta[2]};
        const Vec3 nella_zampa = piede_zampa(prova::angoli(p.angoli));
        if (std::hypot(nella_zampa.x, nella_zampa.y) < 20.0f) {
            continue;
        }
        AngoliZampa a{};
        TEST_ASSERT_TRUE(ik_robot(p.zampa, punta, a));
        m(prova::scarto_angoli(a, p.angoli));
        ++n;
    }
    std::printf("inversa delle punte lette dal CAD: %d pose, scarto massimo %.5f gradi\n", n, m.valore);
    // la punta del CAD e' data a 1e-4 mm: l'angolo che ne risulta ha qualche millesimo di grado d'incertezza
    TEST_ASSERT_TRUE(m.valore <= TOLLERANZA_ANGOLI);
}

static void test_fuori_portata(void) {
    float a = 0.0f, g = 0.0f;
    TEST_ASSERT_FALSE(ik_piano(200.0f, 0.0f, a, g));                         // oltre Lf + Lt
    TEST_ASSERT_FALSE(ik_piano(10.0f, 10.0f, a, g));                         // sotto |Lf - Lt|
    TEST_ASSERT_FALSE(ik_piano(std::nanf(""), 100.0f, a, g));               // non finito
    AngoliZampa z{};
    TEST_ASSERT_FALSE(ik_robot(robot::AS, {400.0f, 300.0f, -100.0f}, z));
}

static void test_corpo_andata_e_ritorno(void) {
    PosaCorpo c;
    c.x = 12.0f;
    c.y = -7.0f;
    c.z = 95.0f;
    c.rollio = 6.0f;
    c.beccheggio = -4.0f;
    c.imbardata = 9.0f;
    Piedi piedi{};
    for (int z = 0; z < N_ZAMPE; ++z) {
        const robot::Coxa& cx = robot::coxe[static_cast<size_t>(z)];
        const float r = robot::Lc + robot::andatura::xf0;
        piedi[static_cast<size_t>(z)] = {cx.x + r * std::cos(rad(cx.direzione)), cx.y + r * std::sin(rad(cx.direzione)),
                                         0.0f};
    }
    Posa posa{};
    TEST_ASSERT_EQUAL_UINT8(0, ik_corpo(c, piedi, posa));
    Piedi ritorno{};
    diretta_corpo(c, posa, ritorno);
    prova::Massimo m;
    for (int z = 0; z < N_ZAMPE; ++z) {
        m(prova::distanza(ritorno[static_cast<size_t>(z)], piedi[static_cast<size_t>(z)]));
        const Vec3 q = appoggio_a_robot(c, robot_a_appoggio(c, piedi[static_cast<size_t>(z)]));
        m(prova::distanza(q, piedi[static_cast<size_t>(z)]));
    }
    std::printf("corpo inclinato e spostato, andata e ritorno: %.6f mm\n", m.valore);
    TEST_ASSERT_TRUE(m.valore <= TOLLERANZA_PYTHON_MM);
}

static void test_corpo_versi(void) {
    // beccheggio positivo: il muso scende; rollio positivo: il fianco sinistro sale
    PosaCorpo c;
    c.z = 100.0f;
    c.beccheggio = 10.0f;
    TEST_ASSERT_TRUE(robot_a_appoggio(c, {100.0f, 0.0f, 0.0f}).z < 100.0f);
    c.beccheggio = 0.0f;
    c.rollio = 10.0f;
    TEST_ASSERT_TRUE(robot_a_appoggio(c, {0.0f, 100.0f, 0.0f}).z > 100.0f);
    c.rollio = 0.0f;
    c.imbardata = 90.0f;
    const Vec3 q = robot_a_appoggio(c, {100.0f, 0.0f, 0.0f});
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 0.0f, q.x);
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 100.0f, q.y);
}

static void test_normalizza(void) {
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, -180.0f, normalizza_180(180.0f));
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, 170.0f, normalizza_180(-190.0f));
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, -10.0f, normalizza_180(350.0f));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_diretta_uguale_al_cad);
    RUN_TEST(test_diretta_uguale_al_python);
    RUN_TEST(test_inversa_andata_e_ritorno);
    RUN_TEST(test_inversa_delle_pose_del_cad);
    RUN_TEST(test_fuori_portata);
    RUN_TEST(test_corpo_andata_e_ritorno);
    RUN_TEST(test_corpo_versi);
    RUN_TEST(test_normalizza);
    return UNITY_END();
}
