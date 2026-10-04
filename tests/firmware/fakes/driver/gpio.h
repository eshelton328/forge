#pragma once
#include <stdint.h>
#include <string>
#include <vector>
#include "Arduino.h"

using gpio_num_t = int;
using gpio_mode_t = int;
constexpr int ESP_OK = 0;
constexpr int GPIO_MODE_INPUT = 1;
constexpr int GPIO_MODE_OUTPUT = 2;
constexpr int GPIO_PULLUP_DISABLE = 0;
constexpr int GPIO_PULLDOWN_DISABLE = 0;
constexpr int GPIO_INTR_DISABLE = 0;
struct gpio_config_t {
  uint64_t pin_bit_mask;
  int mode, pull_up_en, pull_down_en, intr_type;
};
struct GPIOEvent { int pin; int mode; int level; };
inline int fake_levels[64] = {};
inline int fake_modes[64] = {};
inline int fail_latch = -1;
inline std::vector<GPIOEvent> gpio_events;
inline int gpio_set_level(int pin, uint32_t level) {
  gpio_events.push_back({pin, 0, static_cast<int>(level)});
  lifecycle.push_back("gpio");
  if (pin == fail_latch) return -1;
  fake_levels[pin] = level;
  return ESP_OK;
}
inline int gpio_config(const gpio_config_t* c) {
  int pin = __builtin_ctzll(c->pin_bit_mask);
  if (c->pin_bit_mask != (1ULL << pin) || c->pull_up_en || c->pull_down_en || c->intr_type) return -1;
  gpio_events.push_back({pin, c->mode, fake_levels[pin]});
  lifecycle.push_back("gpio");
  fake_modes[pin] = c->mode;
  return ESP_OK;
}
inline int gpio_get_level(int pin) { return fake_levels[pin]; }
