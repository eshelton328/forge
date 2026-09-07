# Breadboard → ALEC firmware compatibility

**Direction confirmed by Erik, September 7:** adapt firmware to the PCB. Old source constants are historical evidence, not PCB requirements. This matrix is static inspection; no firmware port or electrical test was performed.

Reference: native files at `dc57b550ebe8c1943e7830468d73af3f93c5bb73`; [source hashes](evidence/hardware-inputs.json). The main reference is `boards/alec-main/alec-main.kicad_sch` and `HARNESS.md`; sensor reference is its native schematic, `tools/check_design.py` and `OPERATION.md`. The inherited `boards/esp32s3-devkit-5v/review/gpio-map.csv` and `design-review.md` explain the alarm mapping, which was cross-checked against the ALEC schematic's actual routing notes.

The alarm column describes `cube_browns/cube_browns.ino` unless another variant is named. The sensor column describes `cube_browns/beacon_browns.ino` (identical to `beacon_cursor`). Full individual constants are in [candidate-analysis.json](candidate-analysis.json).

| Interface | Breadboard code | Current PCB contract | Port implication |
| --- | --- | --- | --- |
| MCU | Cube source targets S3; Beacon source targets C3 | Both ALEC main and sensor use ESP32-S3; sensor module is WROOM-1-N16 | Build the destination sensor for S3 with correct flash/module options. C3 compile success does not qualify the S3 sensor. |
| Settings buttons | MODE=4, VOL+=5, VOL−=6, active LOW | MODE=5, VOL+=6, VOL−=4, active LOW; main J5/controls J1 | Remap functions and wake masks; retain deliberate debounce and UI semantics. |
| Battery button/RGB | No implemented battery button or RGB indication in the selected alarm source; sensor uses yellow GPIO4 and green GPIO3, active HIGH | Both boards: battery button GPIO10; common-anode RGB GPIO38/39/40, active LOW | Add board-specific controls/indication. GPIO4 on the sensor is radar presence wake, not a yellow LED output. |
| Sensor UART | RX20/TX21, UART1, 256000 8N1 | S3 RX18/TX17 through U10 TMUX1511, with module TX→MCU RX and module RX←MCU TX | Remap UART and enable signal isolation. GPIO20 is now native USB D+, so retaining RX20 conflicts with the PCB interface. |
| Sensor radar power | Always reads the powered LD2410C; no rail or isolation control | GPIO16 enables 5 V; GPIO11 enables U10; GPIO4 receives OUT | Implement reset-safe sequencing and readiness: I/O isolated → rail on → power-good → I/O connected → valid settled frames. Reverse sequence on shutdown. |
| I²C/RTC | SDA8/SCL9, RV-3028 INT1 on the Cube | SDA8/SCL9, INT1 on both boards | Addresses and pins are useful references; add the sensor RTC implementation and validate time/interrupt behavior. |
| Display controller | U8g2 SSD1306 128×64 constructor (also display test); historical notes include other older modules | Selected ER-OLEDM013-1W-I2C uses SH1106 per main harness | Change driver to the selected physical display and test full-screen alignment. |
| Display power/bus | GPIO7 power gate, 12 s idle timeout; no separate OLED bus-isolation GPIO | GPIO41 power; GPIO11 I²C isolation; J4 = GND/power/SCL/SDA | Remap and add ordered power/bus connection. GPIO7 now monitors USB VBUS. Keep RTC connected while OLED is off. |
| I²S audio | BCLK15/LRCLK16/DATA17 | BCLK47/LRCLK48/DIN14 | Remap all three. GPIO15 is now 3.3 V power-good, so old BCLK output assignment is incompatible. |
| Audio enable | Boost18 and AMP_SD21; fixed delays, deferred audio after ACK, 150 ms soft start | GPIO18 enables TPS63070 5 V; GPIO21 drives amp through isolation; GPIO13 monitors 5 V PG | Pins partly match, but implement PG timeout and settling. Current contract drives I²S low before power removal; the old uninstall path sets pins to INPUT. |
| Battery/PG monitoring | No ADC measurement or converter PG handling | GPIO2 ADC with GPIO12 measurement enable, calibrated ×4.3 divider conversion, 10 ms settling; PG3=15/PG5=13 | Implement diagnostics and chemistry-specific indication. Do not mistake ADC voltage for a validated fuel gauge. |
| Cube sleep/wake | EXT1 wake from buttons4/5/6 and RTC1; one-minute pre-alarm support | New function assignments, battery10, added switched peripherals; main OFF is regulator standby, not full battery disconnection | Review wake eligibility/holds, RTC backup configuration, bus/radio/audio shutdown and cold-start behavior. Old mask includes the same three GPIOs but does not include battery10. |
| Sensor sleep/time | Always-awake radar sampling; no sleep, schedule distribution or RTC use | RTC/timer rendezvous, radar rail/isolation sequencing; sensor hard OFF removes power and loses time | Requires scheduler, time synchronization, wake guard and readiness protocol. This is more than pin remapping. Product policy remains with ROO-001/005/013. |
| ESP-NOW messages | Main family uses packed ROOS v1 CONFIG/ACK/PRESENCE/SUCCESS/STOP, channel9, configured Cube peer MAC and learned Beacon peer; peers set `encrypt=false` | S1 guidance calls for session-specific acknowledged completion, bounded retries, authentication and schedule readiness | Reuse behavior as reference while defining a shared protocol. Current header/sequence checks are not cryptographic authentication; schedule/battery/readiness/failure data are missing. |
| Grace/presence | Sensor pauses accumulation during filtered loss, retains effective presence through 5 s, then resets; can retain stale distance for 1.5 s and treats 3 s without data as no presence | Product D03-GRACE keeps silent/paused for ≤5 s recognized qualifying loss; input freshness/hold qualification remains open | Preserve confirmed user behavior while separating raw radar hold, stale/invalid data and radio unreachability. Sensor OPERATION shorthand requires reconciliation. |
| Missing-sensor behavior | `cube_browns` defers audio until ACK, then ends session after 1200 ms ACK timeout; no user-configurable battery-button override | Confirmed product direction requires fallback alarm behavior and a delayed conditional override | Legacy startup/failure handling is not the new requirement. Preserve source; implement agreed fallback in ROO-015 after remaining D04 choices. |
| VBAT/header history | Source names do not identify the manufactured PCB | July 18 Git fix records a disconnected J1.2→Q1.3 battery path on old `esp32s3-devkit`; added 0.8 mm F.Cu track | See physical ledger. Exact order/revision mapping remains open. This historical fault is distinct from audio brownout comments and from current ALEC validation. |

## Message layouts

Sizes below are static field totals for packed 32-bit ESP32 builds; they are not captured on-device packets. The Cube's `roos_u32` is `unsigned long`, whereas the Beacon uses `uint32_t`. Use explicit fixed-width types and length/layout checks for the shared destination protocol.

| ROOS v1 packet | Ordered fields | Packed bytes |
| --- | --- | --- |
| CONFIG (1) | magic[4], version:u8, msgType:u8, distHalfFt:u8, timeHalfMin:u8, seq:u32 | 12 |
| ACK (2) | magic[4], version:u8, msgType:u8, seq:u32, ok:u8 | 11 |
| PRESENCE (3) | magic[4], version:u8, msgType:u8, seq:u32, present:u8, distCm:u16 | 13 |
| SUCCESS (4) | magic[4], version:u8, msgType:u8, seq:u32 | 10 |
| STOP (5) | magic[4], version:u8, msgType:u8, seq:u32 | 10 |

`cube_connected` and `cube_settings_save` define the first four packets and no STOP struct. `cube_esp_now`, its backup, `cube_merge`, `cube_cursor` and `cube_browns` define all five. The radio-enabled Beacon variants other than `beacon_connected` use the five-message family.

**Filename pairing is unreliable:** `beacon_connected` instead uses channel1, magic `0x52535431`, a 16-bit sequence, TEST_START/TEST_STOP/PING/ROGER/STATUS and 15-second hold units. Its packed `CubeToBeacon` is 11 bytes (u32 magic, u8 version, u8 type, u16 seq, u8 maxDistHalfFt, u16 hold15sUnits); `BeaconToCube` is 12 bytes (u32 magic, u8 version, u8 type, u16 seq, u8 presence, u8 success, u16 held15s). `cube_connected` uses ROOS/channel9 and half-minute hold units, so those similarly named files are not a matching protocol pair. This was found in their constants and struct definitions, not a radio test.
