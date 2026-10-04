#pragma once
#include <algorithm>
#include <deque>
#include <stdint.h>
#include <string>
#include <vector>

#define CONFIG_IDF_TARGET_ESP32S3 1
#define ARDUINO_USB_MODE 1
#define ARDUINO_USB_CDC_ON_BOOT 1
#define SERIAL_8N1 0

inline uint32_t fake_now = 0;
inline std::vector<std::string> lifecycle;
inline uint32_t millis() { return fake_now; }
inline void delay(uint32_t ms) { fake_now += ms; }
struct FakeESP { uint64_t getEfuseMac() { return 0x112233445566ULL; } };
inline FakeESP ESP;

struct FakePort {
  bool connected = true;
  int room = 8;
  std::deque<char> incoming;
  std::string outgoing;
  void begin(int, int = 0, int = -1, int = -1) { lifecycle.push_back("serial"); }
  void setTxTimeoutMs(unsigned ms) { if (ms != 0) __builtin_trap(); }
  int availableForWrite() { return room; }
  int available() { return static_cast<int>(incoming.size()); }
  int read() { char ch = incoming.front(); incoming.pop_front(); return ch; }
  size_t write(const uint8_t* data, size_t count) {
    count = std::min(count, static_cast<size_t>(room));
    outgoing.append(reinterpret_cast<const char*>(data), count);
    return count;
  }
  explicit operator bool() const { return connected; }
  void feed(const std::string& value) { for (char ch : value) incoming.push_back(ch); }
};
inline FakePort Serial;
inline FakePort Serial0;
