# Test del nucleo sul PC (Mac o CI): CMake, ctest e Unity, lo stesso framework dei test sul chip.
#   cmake -S firmware/test_host -B build/test_host -G Ninja && cmake --build build/test_host && ctest --test-dir build/test_host
cmake_minimum_required(VERSION 3.20)
project(nucleo_test_host LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(NUCLEO_SANITIZER "Compila nucleo e test con AddressSanitizer e UndefinedBehaviorSanitizer" ON)
if(NUCLEO_SANITIZER)
    add_compile_options(-fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer)
    add_link_options(-fsanitize=address,undefined)
endif()

# Unity alla stessa revisione che ESP-IDF v6.1 porta in components/unity (v2.6.0_RC1), cosi' i test sul PC e sul chip
# usano lo stesso framework.
include(FetchContent)
FetchContent_Declare(
    unity
    URL https://github.com/ThrowTheSwitch/Unity/archive/bf560290f6020737eafaa8b5cbd2177c3956c03f.tar.gz
    URL_HASH SHA256=441fae1f1e49f545a871508bf096f50c69e602a9df54ef8a8a4972f52389b77e
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE)
FetchContent_MakeAvailable(unity)

add_subdirectory(../components/nucleo nucleo)

enable_testing()
foreach(nome cinematica guardia andatura servo)
    add_executable(test_${nome} test_${nome}.cpp)
    target_link_libraries(test_${nome} PRIVATE nucleo unity)
    target_include_directories(test_${nome} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
    target_compile_options(test_${nome} PRIVATE -Wall -Wextra -Werror)
    add_test(NAME ${nome} COMMAND test_${nome})
endforeach()
