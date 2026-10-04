#pragma once
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "board_config.h"

namespace cube {

// GPIO adapter is deliberately narrow: there is no runtime "enable load" API.
template <class IO> bool initialize(IO& io) {
  bool ok = true;
  for (const auto& pin : kOutputs) {
    // Set the latch before exposing the pin as an output, including HIGH/off RGB.
    const bool latched = io.latch(pin.gpio, pin.inactive);
    ok = latched && ok;
    if (latched) ok = io.output(pin.gpio) && ok;
  }
  for (const auto& pin : kInputs) ok = io.input(pin.gpio) && ok;
  for (const auto pin : kQuietInputs) ok = io.input(pin) && ok;
  return ok;
}

struct InputState {
  bool raw = false;
  bool stable = false;
  bool seeded = false;
  bool valid = false;
  uint32_t since = 0;
  uint32_t transitions = 0;

  void sample(bool level, uint32_t now, uint32_t debounce) {
    if (!seeded || level != raw) {
      raw = level;
      since = now;
      seeded = true;
    }
    // Unsigned subtraction handles millis() rollover. No startup press inferred.
    if (static_cast<uint32_t>(now - since) >= debounce) {
      if (valid && stable != raw) ++transitions;
      stable = raw;
      valid = true;
    }
  }
};

enum class Command { none, info, status, help, unknown, invalid_line };

class LineParser {
 public:
  Command feed(char ch) {
    if (ch == '\r' || ch == '\n') {
      if (invalid_) { reset(); return Command::invalid_line; }
      buffer_[length_] = '\0';
      Command cmd = Command::none;
      if (length_) {
        cmd = !strcmp(buffer_, "info") ? Command::info :
              !strcmp(buffer_, "status") ? Command::status :
              !strcmp(buffer_, "help") ? Command::help : Command::unknown;
      }
      reset();
      return cmd;
    }
    if (static_cast<unsigned char>(ch) < 32 || static_cast<unsigned char>(ch) > 126 || length_ == sizeof(buffer_) - 1) {
      invalid_ = true;
    } else if (!invalid_) {
      buffer_[length_++] = ch;
    }
    return Command::none;
  }
  void reset() { length_ = 0; invalid_ = false; }

 private:
  char buffer_[32] = {};
  unsigned length_ = 0;
  bool invalid_ = false;
};

template <class IO> class Diagnostics {
 public:
  explicit Diagnostics(IO& io) : io_(io) {}
  bool begin() { startup_ok_ = initialize(io_); return startup_ok_; }
  void sample(uint32_t now) {
    if (!startup_ok_) return;
    for (unsigned i = 0; i < kInputCount; ++i)
      inputs_[i].sample(io_.read(kInputs[i].gpio), now, kInputs[i].debounce_ms);
  }
  bool startup_ok() const { return startup_ok_; }
  const InputState& input(unsigned i) const { return inputs_[i]; }

 private:
  IO& io_;
  bool startup_ok_ = false;
  InputState inputs_[kInputCount];
};

}  // namespace cube
