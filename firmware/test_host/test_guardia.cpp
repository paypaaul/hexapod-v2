// Guardia (software.md 2.5; test 3-6 di software.md 6.3): pose verificate nel CAD, casi d'urto, regole, statica.
#include "comune.hpp"

using namespace nucleo;

extern "C" void setUp(void) {}
extern "C" void tearDown(void) {}

namespace {

constexpr float DT = 1.0f / robot::andatura::frequenza_hz;
constexpr uint32_t STATICA = (1u << static_cast<unsigned>(Motivo::coppia)) | (1u << static_cast<unsigned>(Motivo::stabilita));

Esito controlla(const Posa& p, Appoggio appoggio = 0, const Posa* prec = nullptr) {
    return Guardia().controlla({p, appoggio}, prec, DT);
}

void accettato(const Esito& e) {
    if (!e.accettato) {
        std::printf("rifiutato: %s zampa %d giunto %d valore %.3f limite %.3f\n", nome_motivo(e.motivo), e.zampa,
                    e.giunto, static_cast<double>(e.valore), static_cast<double>(e.limite));
    }
    TEST_ASSERT_TRUE(e.accettato);
}

void rifiutato(const Esito& e, Motivo m) {
    TEST_ASSERT_FALSE(e.accettato);
    TEST_ASSERT_EQUAL_STRING(nome_motivo(m), nome_motivo(e.motivo));
}

}  // namespace

// Test 3: le pose dei cicli verificati nel CAD rispettano tutti i limiti geometrici. Le coppie stimate superano il
// rifiuto (70 % dello stallo) solo a 70/70: 75 % in tripode e 74 % nella rotazione sul posto (calcolo con
// calc/statica_tripode.py; software.md 4.2: 70/70 a tripode 75 %). Nel CAD si e' verificata l'assenza di urti, non
// la coppia: a 70/70 il firmware deve passare a un'andatura con piu' piedi a terra.
static void test_cicli_verificati(void) {
    for (const auto& c : vettori::cicli) {
        prova::Massimo coppia;
        float margine = 1e9f;
        bool tutti_accettati = true;
        uint32_t violazioni = 0;
        for (int i = c.prima; i < c.prima + c.fasi; ++i) {
            const auto& pc = vettori::pose_cicli[i];
            const Esito e = controlla(prova::posa(pc.angoli), appoggio_tripode(pc.fase));
            TEST_ASSERT_EQUAL_UINT32(0, e.violazioni & ~STATICA);
            coppia(e.coppia_max);
            margine = std::fmin(margine, e.margine_stabilita_mm);
            tutti_accettati = tutti_accettati && e.accettato;
            violazioni |= e.violazioni;
        }
        std::printf("ciclo %3.0f/%2.0f giro %2.0f: coppia massima %.3f dello stallo, margine minimo %.1f mm, %s\n",
                    static_cast<double>(c.h), static_cast<double>(c.xf0), static_cast<double>(c.giro),
                    static_cast<double>(coppia.valore), static_cast<double>(margine),
                    tutti_accettati ? "accettato" : "rifiutato per la coppia");
        TEST_ASSERT_TRUE(margine >= robot::guardia::stabilita_mm);
        const bool atteso_rifiuto_coppia = c.h <= 70.0f;
        TEST_ASSERT_EQUAL(atteso_rifiuto_coppia, !tutti_accettati);
        if (!tutti_accettati) {
            TEST_ASSERT_EQUAL_UINT32(1u << static_cast<unsigned>(Motivo::coppia), violazioni);
        }
    }
}

// Test 4: casi d'urto del CAD.
static void test_casi_d_urto(void) {
    Posa p = prova::in_piedi();
    accettato(controlla(p, 0x3F));

    Posa femore = p;
    femore[robot::AS].alpha = -60.0f;
    rifiutato(controlla(femore), Motivo::alpha);

    Posa vicine = p;  // AS e MS a 40 gradi una verso l'altra
    vicine[robot::AS].imbardata = 40.0f;
    vicine[robot::MS].imbardata = -40.0f;
    const Esito e = controlla(vicine);
    rifiutato(e, Motivo::imbardata);
    TEST_ASSERT_TRUE(e.viola(Motivo::somma_vicine));

    Posa ginocchio = p;  // sotto la tabella: a femore 0 il minimo meccanico e' 43
    ginocchio[robot::MD].alpha = 0.0f;
    ginocchio[robot::MD].gamma = 40.0f;
    rifiutato(controlla(ginocchio), Motivo::gamma_min);
}

// Test 5: le regole una per una (robot sospeso, cosi' contano solo i limiti dei giunti).
static void test_imbardata(void) {
    Posa p = prova::in_piedi();
    p[robot::PS].imbardata = 30.0f;
    accettato(controlla(p));
    p[robot::PS].imbardata = 30.01f;
    rifiutato(controlla(p), Motivo::imbardata);
    p[robot::PS].imbardata = -30.01f;
    rifiutato(controlla(p), Motivo::imbardata);
}

static void test_somma_vicine(void) {
    Posa p = prova::in_piedi();
    p[robot::AS].imbardata = 28.0f;  // a sinistra: imb_A - imb_M
    p[robot::MS].imbardata = -28.0f;
    accettato(controlla(p));
    p[robot::AS].imbardata = 29.0f;
    p[robot::MS].imbardata = -29.0f;
    rifiutato(controlla(p), Motivo::somma_vicine);

    Posa q = prova::in_piedi();  // a destra il contrario: imb_M - imb_A
    q[robot::AD].imbardata = -29.0f;
    q[robot::MD].imbardata = 29.0f;
    rifiutato(controlla(q), Motivo::somma_vicine);
    q[robot::AD].imbardata = 29.0f;  // si allontanano
    q[robot::MD].imbardata = -29.0f;
    accettato(controlla(q));

    Posa r = prova::in_piedi();  // MS e PS: imb_M - imb_P
    r[robot::MS].imbardata = 29.0f;
    r[robot::PS].imbardata = -29.0f;
    rifiutato(controlla(r), Motivo::somma_vicine);
}

static void test_alpha(void) {
    Posa p = prova::in_piedi();
    p[robot::MS] = {0.0f, 82.0f, 120.0f};
    accettato(controlla(p));
    p[robot::MS].alpha = 82.1f;
    rifiutato(controlla(p), Motivo::alpha);
    p[robot::MS] = {0.0f, -45.0f, 60.0f};
    accettato(controlla(p));
    p[robot::MS].alpha = -45.1f;
    rifiutato(controlla(p), Motivo::alpha);
}

static void test_gamma_min_interpolazione_massimo(void) {
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 55.0f, Guardia::gamma_min(-37.5f));  // max(55, 45), non 50
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 45.0f, Guardia::gamma_min(-35.0f));  // sulla riga
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 43.0f, Guardia::gamma_min(2.5f));    // max(43, 41)
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 29.0f, Guardia::gamma_min(60.0f));
    TEST_ASSERT_TRUE(std::isnan(Guardia::gamma_min(-45.5f)));
    TEST_ASSERT_TRUE(std::isnan(Guardia::gamma_min(85.5f)));

    Posa p = prova::in_piedi();
    p[robot::PD] = {0.0f, -37.5f, 58.0f};  // 55 + 3
    accettato(controlla(p));
    p[robot::PD].gamma = 57.9f;
    rifiutato(controlla(p), Motivo::gamma_min);
}

static void test_gamma_max(void) {
    Posa p = prova::in_piedi();
    p[robot::AD] = {0.0f, 20.0f, 177.0f};
    accettato(controlla(p));
    p[robot::AD].gamma = 177.1f;
    rifiutato(controlla(p), Motivo::gamma_max);
}

static void test_non_finito(void) {
    Posa p = prova::in_piedi();
    p[robot::MD].alpha = std::nanf("");
    rifiutato(controlla(p, 0x3F), Motivo::non_finito);
    p[robot::MD].alpha = INFINITY;
    rifiutato(controlla(p), Motivo::non_finito);
}

static void test_corsa_servo(void) {
    // con i calettamenti di robot.yaml la corsa (+-80) contiene gia' tutti gli altri limiti: si prova con un
    // calettamento del femore a 0
    LimitiGuardia l = LimitiGuardia::rigidi();
    l.calettamento[1] = 0.0f;
    Posa p = prova::in_piedi();
    p[robot::AS] = {0.0f, 81.0f, 120.0f};
    const Esito e = Guardia(l).controlla({p, 0}, nullptr, DT);
    rifiutato(e, Motivo::corsa_servo);
    TEST_ASSERT_EQUAL_INT8(1, e.giunto);
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 80.0f, e.limite);
}

static void test_velocita(void) {
    const Posa prec = prova::in_piedi();
    Posa p = prec;
    p[robot::MS].gamma += 4.9f;  // 245 gradi/s a 50 Hz
    accettato(controlla(p, 0, &prec));
    p[robot::MS].gamma = prec[robot::MS].gamma + 5.1f;  // 255 gradi/s
    const Esito e = controlla(p, 0, &prec);
    rifiutato(e, Motivo::velocita);
    TEST_ASSERT_EQUAL_INT8(robot::MS, e.zampa);
    TEST_ASSERT_EQUAL_INT8(2, e.giunto);
}

static void test_limiti_morbidi_solo_piu_stretti(void) {
    LimitiGuardia morbidi = LimitiGuardia::rigidi();
    morbidi.imbardata_min = -20.0f;
    morbidi.imbardata_max = 40.0f;  // piu' largo del rigido: non conta
    const LimitiGuardia l = LimitiGuardia::rigidi().stringi(morbidi);
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, -20.0f, l.imbardata_min);
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 30.0f, l.imbardata_max);
    Posa p = prova::in_piedi();
    p[robot::MD].imbardata = -25.0f;
    rifiutato(Guardia(l).controlla({p, 0}, nullptr, DT), Motivo::imbardata);
}

// Test 6: carichi, coppie e margine come calc/statica_tripode.py -> valuta(CONFIG), riga per riga, e regressione:
// femore al 51 % +- 1 dello stallo a 100/45 (5,65 kgf*cm) e margine 59 mm (robot.yaml -> regressione_statica).
static void test_statica_come_calc(void) {
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, vettori::statica_massa_g, robot::masse::attesa_g);
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, vettori::statica_stallo_kgfcm, robot::servo::stallo_kgfcm);
    const int n = prova::numero(vettori::statica);
    TEST_ASSERT_EQUAL_INT(0, n % 3);
    prova::Massimo carichi, coppie, angoli;
    float coppia_max = 0.0f, margine = 1e9f;
    for (int i = 0; i < n; i += 3) {
        Posa p = prova::in_piedi(vettori::statica_h, vettori::statica_xf0);
        Appoggio app = 0;
        Vec2 piedi[3];
        for (int k = 0; k < 3; ++k) {
            const auto& r = vettori::statica[i + k];
            piedi[k] = {r.piede[0], r.piede[1]};
            AngoliZampa a{};
            TEST_ASSERT_TRUE(ik_robot(r.zampa, {r.piede[0], r.piede[1], -vettori::statica_h}, a));
            p[r.zampa] = a;
            app = static_cast<Appoggio>(app | (1u << r.zampa));
            const float riga[3] = {r.imbardata, r.alpha, r.gamma};
            angoli(prova::scarto_angoli(a, riga));
        }
        float f[3];
        TEST_ASSERT_TRUE(carichi_piedi(piedi, 3, {0.0f, 0.0f}, vettori::statica_massa_g / 1000.0f, f));
        for (int k = 0; k < 3; ++k) {
            const auto& r = vettori::statica[i + k];
            carichi(std::fabs(f[k] - r.carico_kgf));
            const CoppieZampa c = coppie_zampa(r.zampa, p[r.zampa], piede_robot(r.zampa, p[r.zampa]), f[k]);
            coppie(std::fabs(c.femore_kgfcm - r.t_femore));
            coppie(std::fabs(c.ginocchio_kgfcm - r.t_ginocchio));
        }
        // la guardia sul fotogramma intero: le zampe in volo restano nella posa in piedi
        const Esito e = controlla(p, app);
        accettato(e);
        coppia_max = std::fmax(coppia_max, e.coppia_max);
        margine = std::fmin(margine, e.margine_stabilita_mm);
    }
    std::printf("statica contro calc/: carichi %.2e kgf, coppie %.2e kgf*cm, angoli %.2e gradi\n",
                static_cast<double>(carichi.valore), static_cast<double>(coppie.valore),
                static_cast<double>(angoli.valore));
    std::printf("guardia a 100/45: femore %.4f dello stallo (%.3f kgf*cm), margine minimo %.2f mm\n",
                static_cast<double>(coppia_max), static_cast<double>(coppia_max * robot::servo::stallo_kgfcm),
                static_cast<double>(margine));
    TEST_ASSERT_TRUE(carichi.valore <= 1e-4f);
    TEST_ASSERT_TRUE(coppie.valore <= 1e-3f);
    TEST_ASSERT_TRUE(angoli.valore <= 0.01f);
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, vettori::statica_t_femore, coppia_max * robot::servo::stallo_kgfcm);
    TEST_ASSERT_TRUE(coppia_max >= 0.50f && coppia_max <= 0.52f);
    TEST_ASSERT_FLOAT_WITHIN(0.01f, vettori::statica_margine_mm, margine);
    TEST_ASSERT_FLOAT_WITHIN(0.5f, 59.0f, margine);
}

static void test_stabilita(void) {
    // tre piedi con il baricentro a 15 mm da un lato: sotto i 20 della guardia
    const Vec2 piedi[3] = {{-100.0f, 15.0f}, {100.0f, 15.0f}, {0.0f, -150.0f}};
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, 15.0f, margine_stabilita(piedi, 3, {0.0f, 0.0f}));
    const Vec2 fuori[3] = {{-100.0f, -15.0f}, {100.0f, -15.0f}, {0.0f, -150.0f}};
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, -15.0f, margine_stabilita(fuori, 3, {0.0f, 0.0f}));
    // con piu' piedi conta l'inviluppo convesso: un piede interno non cambia il margine
    const Vec2 sei[5] = {{-100.0f, 15.0f}, {100.0f, 15.0f}, {0.0f, -150.0f}, {0.0f, -50.0f}, {10.0f, 0.0f}};
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, 15.0f, margine_stabilita(sei, 5, {0.0f, 0.0f}));

    // in piedi su due zampe: rifiuto
    const Posa p = prova::in_piedi();
    const Appoggio due = static_cast<Appoggio>((1u << robot::AS) | (1u << robot::PD));
    rifiutato(controlla(p, due), Motivo::stabilita);

    // tripode A in appoggio nella posa neutra, baricentro spostato verso il lato AS-MD (a 84 mm dal centro, calcolo):
    // il margine scende sotto i 20 mm
    Posa q{};
    TEST_ASSERT_TRUE(pose_tripode(ParametriAndatura{}, 0.25f, q));
    TEST_ASSERT_TRUE(controlla(q, appoggio_tripode(0.25f)).accettato);
    LimitiGuardia l = LimitiGuardia::rigidi();
    l.baricentro = {61.0f, -42.0f};
    const Esito e = Guardia(l).controlla({q, appoggio_tripode(0.25f)}, nullptr, DT);
    std::printf("tripode con il baricentro spostato: margine %.1f mm\n", static_cast<double>(e.margine_stabilita_mm));
    TEST_ASSERT_TRUE(e.margine_stabilita_mm > 0.0f && e.margine_stabilita_mm < robot::guardia::stabilita_mm);
    rifiutato(e, Motivo::stabilita);
}

static void test_carichi_iperstatici(void) {
    // piu' di tre piedi: equilibrio rispettato (somma = peso, momenti nulli)
    const Vec2 piedi[6] = {{184.0f, 104.0f}, {0.0f, 148.0f}, {-184.0f, 104.0f},
                           {184.0f, -104.0f}, {0.0f, -148.0f}, {-184.0f, -104.0f}};
    const Vec2 g = {10.0f, -5.0f};
    float f[6];
    TEST_ASSERT_TRUE(carichi_piedi(piedi, 6, g, 2.945f, f));
    float s = 0.0f, mx = 0.0f, my = 0.0f;
    for (int k = 0; k < 6; ++k) {
        s += f[k];
        mx += f[k] * (piedi[k].x - g.x);
        my += f[k] * (piedi[k].y - g.y);
        TEST_ASSERT_TRUE(f[k] > 0.0f);
    }
    TEST_ASSERT_FLOAT_WITHIN(1e-5f, 2.945f, s);
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 0.0f, mx);
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 0.0f, my);
    // piedi allineati: nessuna soluzione
    const Vec2 allineati[3] = {{0.0f, 0.0f}, {100.0f, 0.0f}, {200.0f, 0.0f}};
    TEST_ASSERT_FALSE(carichi_piedi(allineati, 3, g, 2.945f, f));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_cicli_verificati);
    RUN_TEST(test_casi_d_urto);
    RUN_TEST(test_imbardata);
    RUN_TEST(test_somma_vicine);
    RUN_TEST(test_alpha);
    RUN_TEST(test_gamma_min_interpolazione_massimo);
    RUN_TEST(test_gamma_max);
    RUN_TEST(test_non_finito);
    RUN_TEST(test_corsa_servo);
    RUN_TEST(test_velocita);
    RUN_TEST(test_limiti_morbidi_solo_piu_stretti);
    RUN_TEST(test_statica_come_calc);
    RUN_TEST(test_stabilita);
    RUN_TEST(test_carichi_iperstatici);
    return UNITY_END();
}
