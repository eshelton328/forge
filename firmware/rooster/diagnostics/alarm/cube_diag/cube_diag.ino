#include <Arduino.h>
#include <driver/gpio.h>
#include <esp_app_desc.h>
#include <esp_system.h>
#include <stdarg.h>
#include "build_identity.h"
#include "diagnostics.h"

#if !CONFIG_IDF_TARGET_ESP32S3 || !ARDUINO_USB_MODE || !ARDUINO_USB_CDC_ON_BOOT
#error "Use the locked Cube ESP32-S3 hardware CDC profile."
#endif

struct BoardIO {
  bool latch(uint8_t pin, bool high) {
    return gpio_set_level(static_cast<gpio_num_t>(pin), high) == ESP_OK;
  }
  bool configure(uint8_t pin, gpio_mode_t mode) {
    gpio_config_t config = {};
    config.pin_bit_mask = 1ULL << pin;
    config.mode = mode;
    config.pull_up_en = GPIO_PULLUP_DISABLE;
    config.pull_down_en = GPIO_PULLDOWN_DISABLE;
    config.intr_type = GPIO_INTR_DISABLE;
    return gpio_config(&config) == ESP_OK;
  }
  bool output(uint8_t pin) { return configure(pin, GPIO_MODE_OUTPUT); }
  bool input(uint8_t pin) { return configure(pin, GPIO_MODE_INPUT); }
  bool read(uint8_t pin) { return gpio_get_level(static_cast<gpio_num_t>(pin)); }
};

BoardIO board;
cube::Diagnostics<BoardIO> diagnostics(board);
char chip_id[17];
char elf_hash[65];

// One bounded response per port; drain it in available chunks without waiting for
// a host. Input sampling continues even when USB is absent or the terminal stalls.
struct Console {
  cube::LineParser parser;
  char response[1536] = {};
  size_t length = 0;
  size_t sent = 0;
  bool overflow = false;

  void append(const char* format, ...) {
    if (overflow) return;
    va_list args;
    va_start(args, format);
    int count = vsnprintf(response + length, sizeof(response) - length, format, args);
    va_end(args);
    if (count < 0 || static_cast<size_t>(count) >= sizeof(response) - length) {
      overflow = true;
      return;
    }
    length += static_cast<size_t>(count);
  }
  void reply(cube::Command command, uint32_t now) {
    length = sent = 0;
    overflow = false;
    append("{\"schema\":1,\"uptime_ms\":%lu,\"image_id\":\"%s\",\"chip_id\":\"%s\",", static_cast<unsigned long>(now), CUBE_IMAGE_ID, chip_id);
    if (command == cube::Command::info) {
      append("\"type\":\"info\",\"target\":\"cube-diagnostics\",\"contract\":\"cube-bringup-v1\",\"source_revision\":\"%s\",\"source_sha256\":\"%s\",\"contract_sha256\":\"%s\",\"app_elf_sha256\":\"%s\",\"core\":\"%s\",\"reset_reason\":%d,\"startup_ok\":%s", CUBE_SOURCE_REVISION, CUBE_SOURCE_SHA256, CUBE_CONTRACT_SHA256, elf_hash, CUBE_CORE_VERSION, static_cast<int>(esp_reset_reason()), diagnostics.startup_ok() ? "true" : "false");
    } else if (command == cube::Command::status) {
      append("\"type\":\"status\",\"startup_ok\":%s,\"inputs\":{", diagnostics.startup_ok() ? "true" : "false");
      for (unsigned i = 0; i < cube::kInputCount; ++i) {
        const auto& state = diagnostics.input(i);
        const auto& pin = cube::kInputs[i];
        const bool valid = diagnostics.startup_ok() && state.valid;
        append("%s\"%s\":{\"raw\":%s,\"active\":%s,\"transitions\":%lu}", i ? "," : "", pin.name,
               diagnostics.startup_ok() ? (state.raw ? "1" : "0") : "null",
               valid ? (state.stable == pin.active ? "true" : "false") : "null",
               static_cast<unsigned long>(state.transitions));
      }
      append("},\"loads_commanded_off\":%s", diagnostics.startup_ok() ? "true" : "false");
    } else if (command == cube::Command::help) {
      append("\"type\":\"help\",\"commands\":[\"info\",\"status\",\"help\"],\"mode\":\"read-only\"");
    } else {
      append("\"type\":\"error\",\"error\":\"%s\"", command == cube::Command::invalid_line ? "invalid_line" : "unknown_command");
    }
    append("}\n");
    if (overflow) {
      strcpy(response, "{\"schema\":1,\"type\":\"error\",\"error\":\"response_overflow\"}\n");
      length = strlen(response);
    }
  }

  template <class Port> void poll(Port& port, uint32_t now) {
    if (sent < length) {
      int room = port.availableForWrite();
      if (room > 0) {
        size_t count = length - sent;
        if (count > static_cast<size_t>(room)) count = room;
        sent += port.write(reinterpret_cast<const uint8_t*>(response + sent), count);
      }
      return;
    }
    for (unsigned budget = 0; budget < 32 && port.available(); ++budget) {
      auto command = parser.feed(static_cast<char>(port.read()));
      if (command != cube::Command::none) { reply(command, now); return; }
    }
  }
  void disconnected() { sent = length = 0; parser.reset(); }
};

Console usb_console;
Console uart_console;

void setup() {
  diagnostics.begin();  // Must precede serial setup, allocation and any wait.
  snprintf(chip_id, sizeof(chip_id), "%012llx", static_cast<unsigned long long>(ESP.getEfuseMac()));
  const auto* app = esp_app_get_description();
  for (unsigned i = 0; i < 32; ++i) snprintf(elf_hash + i * 2, 3, "%02x", app->app_elf_sha256[i]);
  Serial0.begin(115200, SERIAL_8N1, 44, 43);
  Serial.begin(115200);
  Serial.setTxTimeoutMs(0);
  diagnostics.sample(millis());
  uart_console.reply(cube::Command::info, millis());
  // USB hosts request "info" after opening; never wait for CDC to attach.
}

void loop() {
  uint32_t now = millis();
  diagnostics.sample(now);
  if (Serial) usb_console.poll(Serial, now);
  else usb_console.disconnected();
  uart_console.poll(Serial0, now);
  delay(1);
}
