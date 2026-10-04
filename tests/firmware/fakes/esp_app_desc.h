#pragma once
#include <stdint.h>
struct esp_app_desc_t { uint8_t app_elf_sha256[32]; };
inline const esp_app_desc_t* esp_app_get_description() {
  static esp_app_desc_t app = {};
  return &app;
}
