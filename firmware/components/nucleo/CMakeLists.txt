# Nucleo: C++17 puro. Dentro ESP-IDF e' un componente; fuori (test sul Mac, firmware/test_host) una libreria statica.
set(NUCLEO_SORGENTI
    src/andatura.cpp
    src/cinematica.cpp
    src/guardia.cpp
    src/servo.cpp
    src/statica.cpp)

# -Wdouble-promotion: sull'S3 il double e' emulato in software (software.md 2.1), quindi niente promozioni nascoste
set(NUCLEO_AVVISI -Wall -Wextra -Wshadow -Wdouble-promotion -Wfloat-conversion)

if(ESP_PLATFORM)
    idf_component_register(SRCS ${NUCLEO_SORGENTI} INCLUDE_DIRS include)
    target_compile_options(${COMPONENT_LIB} PRIVATE ${NUCLEO_AVVISI})
else()
    add_library(nucleo STATIC ${NUCLEO_SORGENTI})
    target_include_directories(nucleo PUBLIC include)
    target_compile_features(nucleo PUBLIC cxx_std_17)
    set_target_properties(nucleo PROPERTIES CXX_EXTENSIONS OFF)
    target_compile_options(nucleo PRIVATE ${NUCLEO_AVVISI} -Wpedantic -Werror)
endif()
