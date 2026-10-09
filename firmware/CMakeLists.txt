# Firmware dell'esapode: progetto ESP-IDF per l'ESP32-S3 (versione dell'IDF in README.md).
cmake_minimum_required(VERSION 3.22)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
# solo main e i componenti che richiede: il resto dell'IDF non si compila
idf_build_set_property(MINIMAL_BUILD ON)
project(hexapod)
