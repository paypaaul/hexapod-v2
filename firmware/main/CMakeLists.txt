idf_component_register(SRCS "main.cpp" "compiti.cpp"
                       INCLUDE_DIRS "."
                       PRIV_REQUIRES nucleo esp_driver_gpio esp_driver_gptimer esp_timer esp_system freertos log)
