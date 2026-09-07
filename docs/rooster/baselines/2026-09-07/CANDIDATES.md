# Candidate inventory

All entries are historical breadboard candidates. Erik identified cube_browns/beacon_browns as the most relevant reference pair, with “I believe” qualification (see `selected-reference.json`). Roles describe static source contents; no entry has been identified as the exact flashed baseline. Each source remains at the full original path in `manifest.json`. Includes, pin definitions, all struct declarations and protocol constants are preserved with line numbers in `candidate-analysis.json`.

| Candidate under original Arduino root | Target inferred from source | Full SHA-256 | Static role |
| --- | --- | --- | --- |
| `beacon_connected/beacon_connected.ino` | ESP32-C3 | `fc16b4a53866a6b9307d038a7cfccba7f2389acca839138b89d17fafbcf30fa9` | Separate RST1/channel1 test protocol; 15 s hold units. |
| `beacon_cursor/beacon_cursor.ino` | ESP32-C3 | `c238b971415345d635cb00615c7123737c712b885b03462250e32f94d4cb9918` | ROOS session sensor; delays initial presence 80 ms after ACK. |
| `beacon_esp_now/beacon_esp_now.ino` | ESP32-C3 | `cb54c240c9f2121be82c9e22fa479d3094b2a6da75e1c6908167b27e83688028` | ROOS session sensor before the 80 ms initial-presence delay. |
| `beacon_working_backup/beacon_working_backup.ino` | ESP32-C3 | `cb54c240c9f2121be82c9e22fa479d3094b2a6da75e1c6908167b27e83688028` | Exact content duplicate of beacon_esp_now; backup path retained. |
| `c3_beacon/c3_beacon.ino` | ESP32-C3 | `e2be97701e40f2399c9dabd2278ef0dd17cf79f2aa9bc4e940397b920f194e3a` | Standalone radar filtering/dwell/LED/serial experiment; no radio protocol. |
| `cube_MAX98357/cube_MAX98357.ino` | ESP32-S3 | `fb11439c199725b9465059ad57810d5f5676530e611389d89577c8cd6b1c313c` | Audio-only tone/power-control experiment with MAX98357A and boost. |
| `cube_browns/beacon_browns.ino` | ESP32-C3 | `c238b971415345d635cb00615c7123737c712b885b03462250e32f94d4cb9918` | Exact content duplicate of beacon_cursor; co-located reference retained. |
| `cube_browns/cube_browns.ino` | ESP32-S3 | `257cadfb2cd4fb6482ef522c25d042808a340deacc0eeebddcf10605e8958bb5` | Clock/UI/NVS/sessions/RTC sleep/display gating; deferred audio, soft start; amplitude 15000. |
| `cube_connected/cube_connected.ino` | ESP32-S3 | `183c024daeb41500b673cccb5440ca62323f2b2a6ec0bdd286ff3196873a5912` | ROOS/channel9 four-message test UI; not the protocol of beacon_connected. |
| `cube_cursor/cube_cursor.ino` | ESP32-S3 | `865692a83865cab7f1c61a0bbe12b902387472f5ca3003840b8cd915ddf90b55` | Same code as cube_browns except MAX_AMPL=22000 instead of 15000. |
| `cube_display_test/cube_display_test.ino` | ESP32-S3 | `656b3fa643c13c98734632dd199d98ead355113b250005e8a304413c8f7b0850` | SSD1306 OLED gate/button/I2C test; no radio or audio. |
| `cube_esp_now/cube_esp_now.ino` | ESP32-S3 | `6fefee567c2a54232b3b5e5dc72e2302235393c623aabfc6bbb68b7e2dd43f33` | Clock/UI/NVS/RTC wake plus five-message session/STOP handling. |
| `cube_merge/cube_merge.ino` | ESP32-S3 | `01ae76b3aedee5bdc2d755bdf7ef349cfa568cb7a3b7f1a0bc24b3e353dbc1e6` | Integrated gated-display/audio version before deferred-start/soft-start changes. |
| `cube_settings_save/cube_settings_save.ino` | ESP32-S3 | `d23b436841262388a6f5c538ec2e0c74ddd54a7e5e8dbdc37566d81a6c9c920c` | Clock/UI/NVS settings plus four-message radio structures. |
| `cube_working_backup/cube_working_backup.ino` | ESP32-S3 | `6fefee567c2a54232b3b5e5dc72e2302235393c623aabfc6bbb68b7e2dd43f33` | Exact content duplicate of cube_esp_now; backup path retained. |

## Libraries and message coverage

Cube display/UI candidates include U8g2; Beacon candidates include MyLD2410. Arduino.h, Wire, WiFi, ESP-NOW, NVS, RTC/sleep and legacy I²S headers come from the pinned ESP32 platform/toolchain when present; math/stddef/string are toolchain standard headers. Audio-only and display-only experiments have no message structures. The standalone `c3_beacon` has no radio messages.

The full original includes are in the manifest; the derived index deliberately retains settings and UI structs as well as radio structs so naming heuristics do not hide layouts. The compatibility report gives the packed radio fields and distinguishes the incompatible RST1 and ROOS families.

Duplicate content is preserved at all original paths: beacon_cursor ↔ cube_browns/beacon_browns, beacon_esp_now ↔ beacon_working_backup, cube_esp_now ↔ cube_working_backup. No deduplication or source move was performed.

The 16 additional .ino paths found outside the recorded 15 are explicitly indexed as unverified/outside this capture in the manifest. This ticket does not claim a whole-computer firmware inventory.
