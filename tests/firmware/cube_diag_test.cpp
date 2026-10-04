// Runs the actual sketch with GPIO/serial substitutes. This is a host test, not
// evidence for ESP32 timing, electrical transients, USB enumeration or real pins.
#include <assert.h>
#include <iostream>
#include <set>
#include "cube_diag.ino"

void ticks(unsigned n) { while (n--) loop(); }

void check_debounce() {
  cube::InputState s;
  s.sample(true, 100, 10);
  assert(!s.valid);
  s.sample(true, 110, 10);
  assert(s.valid && s.stable && !s.transitions);
  s.sample(false, 111, 10);
  s.sample(true, 116, 10);
  s.sample(false, 119, 10);
  s.sample(false, 128, 10);
  assert(s.stable && !s.transitions);
  s.sample(false, 129, 10);
  assert(!s.stable && s.transitions == 1);
  s.sample(true, 130, 10);
  s.sample(true, 140, 10);
  assert(s.stable && s.transitions == 2);
  cube::InputState wrap;
  wrap.sample(false, UINT32_MAX - 5, 10);
  wrap.sample(false, 3, 10);
  assert(!wrap.valid);
  wrap.sample(false, 4, 10);
  assert(wrap.valid && !wrap.stable && !wrap.transitions);
}

cube::Command line(cube::LineParser& parser, const std::string& text) {
  auto last = cube::Command::none;
  for (char ch : text) { auto cmd = parser.feed(ch); if (cmd != cube::Command::none) last = cmd; }
  return last;
}

void check_parser() {
  cube::LineParser p;
  assert(line(p, "info\r\n") == cube::Command::info);
  assert(line(p, "\n") == cube::Command::none);
  assert(line(p, "enable amp\n") == cube::Command::unknown);
  assert(line(p, std::string(40, 'x') + "status\n") == cube::Command::invalid_line);
  assert(line(p, "status\n") == cube::Command::status);
  assert(line(p, std::string("st\0atus\n", 8)) == cube::Command::invalid_line);
  assert(line(p, "he") == cube::Command::none);
  assert(line(p, "lp\n") == cube::Command::help);
}

void check_gpio(bool fault) {
  const std::set<int> low = {11, 12, 14, 18, 21, 41, 47, 48};
  const std::set<int> high = {38, 39, 40};
  const std::set<int> inputs = {1, 2, 4, 5, 6, 7, 8, 9, 10, 13, 15};
  for (size_t i = 0; i < gpio_events.size(); ++i) {
    const auto& e = gpio_events[i];
    assert(low.count(e.pin) || high.count(e.pin) || inputs.count(e.pin));
    if (e.mode == GPIO_MODE_OUTPUT) {
      assert(i > 0 && gpio_events[i - 1].pin == e.pin && gpio_events[i - 1].mode == 0);
      assert((low.count(e.pin) && e.level == 0) || (high.count(e.pin) && e.level == 1));
    }
  }
  for (int pin : low) assert(fake_modes[pin] == ((fault && pin == 18) ? 0 : GPIO_MODE_OUTPUT));
  for (int pin : high) assert(fake_modes[pin] == GPIO_MODE_OUTPUT && fake_levels[pin] == 1);
  for (int pin : inputs) assert(fake_modes[pin] == GPIO_MODE_INPUT);
  for (int pin : {0, 19, 20, 43, 44}) assert(fake_modes[pin] == 0);
  assert(lifecycle.size() > gpio_events.size());
  assert(lifecycle[gpio_events.size()] == "serial");
}

int main(int argc, char** argv) {
  assert(argc == 2);
  check_debounce();
  check_parser();
  std::string scenario(argv[1]);
  for (int pin : {1, 4, 5, 6, 10, 15}) fake_levels[pin] = 1;
  Serial.connected = false;
  const bool fault = scenario == "fault";
  if (fault) fail_latch = 18;
  setup();
  check_gpio(fault);
  const size_t writes = gpio_events.size();
  assert(diagnostics.startup_ok() == !fault);
  ticks(250);  // An absent USB host must not hold setup or sampling.
  assert(fake_now == 250 && !Serial0.outgoing.empty());
  Serial.connected = true;
  if (scenario == "backpressure") {
    Serial.room = 0;
    Serial.feed("status\n");
    ticks(20);
    fake_levels[4] = 0;
    ticks(20);
    assert(!diagnostics.input(0).stable && Serial.outgoing.empty());
    Serial.room = 7;
    ticks(400);
    Serial.feed("status\n");
  } else if (scenario == "disconnect") {
    Serial.feed("st");
    ticks(2);
    Serial.connected = false;
    ticks(1);
    Serial.connected = true;
    Serial.feed("atus\ninfo\n");
  } else {
    Serial.feed("info\r\nstatus\nhelp\nenable amp\n" + std::string(40, 'x') + "\n");
  }
  ticks(2000);
  assert(gpio_events.size() == writes);  // Commands, errors and congestion cannot drive outputs.
  assert(!Serial.outgoing.empty() && Serial.outgoing.back() == '\n');
  std::cout << Serial.outgoing;
}
