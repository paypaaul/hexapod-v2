// Compiti FreeRTOS del firmware, con core, priorita' e ritmi di software.md 2.2.
#pragma once

// Crea i compiti. Solo ctrl fa gia' qualcosa (il ciclo del nucleo in modo OMBRA, senza SSC-32); gli altri sono
// scheletri che girano a vuoto al loro ritmo.
void avvia_compiti();
