// Conversione angolo -> impulso e modello del servo (software.md 2.7, 4.6).
#include "comune.hpp"

using namespace nucleo;

extern "C" void setUp(void) {}
extern "C" void tearDown(void) {}

static void test_centro_al_calettamento(void) {
    const Taratura t = taratura_predefinita();
    Posa p{};
    for (auto& a : p) {
        a = {robot::servo::calettamento[0], robot::servo::calettamento[1], robot::servo::calettamento[2]};
    }
    Impulsi us{};
    posa_a_impulsi(t, p, us);
    for (const auto& z : us) {
        for (uint16_t v : z) {
            TEST_ASSERT_EQUAL_UINT16(1500, v);
        }
    }
}

static void test_verso_e_guadagno(void) {
    const Taratura t = taratura_predefinita();
    // femore: verso -1, calettamento 20 -> alpha 30 vale 1500 - 11,1 * 10
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 1389.0f, angolo_a_us(t[robot::AS][1], 30.0f));
    // ginocchio: verso +1, calettamento 100 -> gamma 120 vale 1500 + 11,1 * 20
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 1722.0f, angolo_a_us(t[robot::AS][2], 120.0f));
    // coxa: verso +1, calettamento 0
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 1167.0f, angolo_a_us(t[robot::PD][0], -30.0f));
    // canali di robot.yaml
    TEST_ASSERT_EQUAL_UINT8(29, t[robot::PD][0].canale);
    TEST_ASSERT_EQUAL_UINT8(8, t[robot::MS][2].canale);
}

static void test_andata_e_ritorno(void) {
    const Taratura t = taratura_predefinita();
    for (int j = 0; j < N_GIUNTI; ++j) {
        for (float a = -80.0f; a <= 180.0f; a += 7.5f) {
            const TaraturaGiunto& g = t[robot::MD][static_cast<size_t>(j)];
            TEST_ASSERT_FLOAT_WITHIN(1e-4f, a, us_a_angolo(g, angolo_a_us(g, a)));
        }
    }
}

static void test_estremi_della_corsa(void) {
    // corsa +-80 dal calettamento: impulsi tra 1500 -+ 888 us, dentro i 500-2500 del servo
    const Taratura t = taratura_predefinita();
    const float c = robot::guardia::corsa_servo;
    for (int j = 0; j < N_GIUNTI; ++j) {
        const TaraturaGiunto& g = t[0][static_cast<size_t>(j)];
        const float a = angolo_a_us(g, g.calettamento + c), b = angolo_a_us(g, g.calettamento - c);
        TEST_ASSERT_FLOAT_WITHIN(0.01f, 888.0f, std::fabs(a - 1500.0f));
        TEST_ASSERT_FLOAT_WITHIN(0.01f, 888.0f, std::fabs(b - 1500.0f));
    }
}

static void test_modello_velocita(void) {
    // 0,14 s per 60 gradi a 6 V (robot.yaml -> servo.velocita_s_60)
    ModelloServo s;
    s.reimposta(0.0f);
    for (int i = 0; i < 7; ++i) {
        s.aggiorna(60.0f, 0.01f);
    }
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 30.0f, s.previsto());
    for (int i = 0; i < 7; ++i) {
        s.aggiorna(60.0f, 0.01f);
    }
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 60.0f, s.previsto());
    // arrivato: il residuo del float sta dentro la banda morta e il servo non si muove piu'
    const float arrivato = s.previsto();
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, arrivato, s.aggiorna(60.0f, 0.01f));
}

static void test_modello_banda_morta(void) {
    // 5 us a 11,1 us/grado = 0,45 gradi: un comando piu' vicino non muove il servo
    ModelloServo s;
    s.reimposta(10.0f);
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 10.0f, s.aggiorna(10.4f, 0.02f));
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 10.0f, s.aggiorna(9.6f, 0.02f));
    TEST_ASSERT_FLOAT_WITHIN(1e-5f, 10.5f, s.aggiorna(10.5f, 0.02f));
}

static void test_posa_prevista(void) {
    ModelloPosa m;
    const Posa partenza = prova::in_piedi();
    m.reimposta(partenza);
    Posa comando = partenza;
    comando[robot::AS].alpha += 20.0f;
    // in un fotogramma da 20 ms il femore fa al piu' 0,02 * 428,6 = 8,6 gradi
    const Posa& p = m.aggiorna(comando, 0.02f);
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, partenza[robot::AS].alpha + 0.02f * 60.0f / 0.14f, p[robot::AS].alpha);
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, partenza[robot::AS].gamma, p[robot::AS].gamma);
    for (int i = 0; i < 3; ++i) {
        m.aggiorna(comando, 0.02f);
    }
    TEST_ASSERT_FLOAT_WITHIN(1e-5f, comando[robot::AS].alpha, m.prevista()[robot::AS].alpha);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_centro_al_calettamento);
    RUN_TEST(test_verso_e_guadagno);
    RUN_TEST(test_andata_e_ritorno);
    RUN_TEST(test_estremi_della_corsa);
    RUN_TEST(test_modello_velocita);
    RUN_TEST(test_modello_banda_morta);
    RUN_TEST(test_posa_prevista);
    return UNITY_END();
}
