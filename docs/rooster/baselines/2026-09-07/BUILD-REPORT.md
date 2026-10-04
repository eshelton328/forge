# ROO-002 build reproduction report

September 7, 2026. **15/15 separately built, unchanged candidate sketches compiled successfully.** The original combined `cube_browns` folder failed with duplicate definitions. There was no upload or hardware test.

## Environment used

- Arduino CLI 1.4.1, commit `e39419312`, bundled in `/Applications/Arduino IDE.app`.
- Espressif Arduino platform `esp32:esp32` **3.3.7**, locally installed under `/Users/erik/Library/Arduino15`. Other installed Arduino platforms were recorded but not used.
- S3 compiler: `xtensa-esp32s3-elf-g++`, GCC 14.2.0, crosstool-NG `esp-14.2.0_20251107`, tool package `esp-x32/2511`.
- C3 compiler: `riscv32-esp-elf-g++`, same GCC/crosstool version, tool package `esp-rv32/2511`.
- External dependencies: captured U8g2 **2.35.30** and MyLD2410 **1.2.7**, extracted from the verified archive, not resolved from a changing global sketchbook. ESP32 core libraries and standard headers came from the installed platform/toolchain. ESP32 library archives/tool packages and resolved paths are in the verbose logs/properties; executable/platform hashes are in `tool-identities.json`.
- Test FQBNs: `esp32:esp32:esp32s3` and `esp32:esp32:esp32c3`, inferred generic development targets from source comments and pins. These are **today's compile targets**, not recovered historical upload settings or selected new-PCB release targets.

Both targets used the installed platform's defaults: 4 MB QIO/80 MHz flash, default 4 MB SPIFFS partition layout, USB CDC on boot disabled, upload speed default 921600, erase disabled. S3 CPU 240 MHz, PSRAM disabled, hardware CDC/JTAG mode; C3 CPU 160 MHz. Complete options, including defaults not listed here, are saved in `s3-board.txt`, `c3-board.txt` and each target's expanded properties. No upload options were exercised. ALEC sensor's N16 module needs a separately selected release profile; these generic 4 MB test builds do not establish its final flash configuration.

Original build environment and actual LD2410C module firmware are unknown. MyLD2410's declared support for a firmware revision does not identify the connected radar. No device connection was attempted to fill that gap.

## Results

| Original candidate/folder | Compile target | Result | Evidence |
| --- | --- | --- | --- |
| `combined original folder` | `esp32:esp32:esp32s3` | EXPECTED FAILURE: duplicate programs | [log](build-records/installed-core-3.3.7/cube_browns_combined.log) |
| `cube_browns/beacon_browns.ino` | `esp32:esp32:esp32c3` | PASS | [log](build-records/installed-core-3.3.7/cube_browns__beacon_browns.log) |
| `cube_browns/cube_browns.ino` | `esp32:esp32:esp32s3` | PASS | [log](build-records/installed-core-3.3.7/cube_browns__cube_browns.log) |
| `beacon_connected/beacon_connected.ino` | `esp32:esp32:esp32c3` | PASS | [log](build-records/installed-core-3.3.7/beacon_connected__beacon_connected.log) |
| `beacon_cursor/beacon_cursor.ino` | `esp32:esp32:esp32c3` | PASS | [log](build-records/installed-core-3.3.7/beacon_cursor__beacon_cursor.log) |
| `beacon_esp_now/beacon_esp_now.ino` | `esp32:esp32:esp32c3` | PASS | [log](build-records/installed-core-3.3.7/beacon_esp_now__beacon_esp_now.log) |
| `beacon_working_backup/beacon_working_backup.ino` | `esp32:esp32:esp32c3` | PASS | [log](build-records/installed-core-3.3.7/beacon_working_backup__beacon_working_backup.log) |
| `c3_beacon/c3_beacon.ino` | `esp32:esp32:esp32c3` | PASS | [log](build-records/installed-core-3.3.7/c3_beacon__c3_beacon.log) |
| `cube_MAX98357/cube_MAX98357.ino` | `esp32:esp32:esp32s3` | PASS | [log](build-records/installed-core-3.3.7/cube_MAX98357__cube_MAX98357.log) |
| `cube_connected/cube_connected.ino` | `esp32:esp32:esp32s3` | PASS | [log](build-records/installed-core-3.3.7/cube_connected__cube_connected.log) |
| `cube_cursor/cube_cursor.ino` | `esp32:esp32:esp32s3` | PASS | [log](build-records/installed-core-3.3.7/cube_cursor__cube_cursor.log) |
| `cube_display_test/cube_display_test.ino` | `esp32:esp32:esp32s3` | PASS | [log](build-records/installed-core-3.3.7/cube_display_test__cube_display_test.log) |
| `cube_esp_now/cube_esp_now.ino` | `esp32:esp32:esp32s3` | PASS | [log](build-records/installed-core-3.3.7/cube_esp_now__cube_esp_now.log) |
| `cube_merge/cube_merge.ino` | `esp32:esp32:esp32s3` | PASS | [log](build-records/installed-core-3.3.7/cube_merge__cube_merge.log) |
| `cube_settings_save/cube_settings_save.ino` | `esp32:esp32:esp32s3` | PASS | [log](build-records/installed-core-3.3.7/cube_settings_save__cube_settings_save.log) |
| `cube_working_backup/cube_working_backup.ino` | `esp32:esp32:esp32s3` | PASS | [log](build-records/installed-core-3.3.7/cube_working_backup__cube_working_backup.log) |

All duplicate-content candidates were built at separate paths. All build-copy hashes matched their preserved originals before and after compilation. Full commands, exit codes, elapsed times and generated binary hashes are in [results.json](build-records/installed-core-3.3.7/results.json). Generated binaries/build caches remain local under ignored `.work/`; they are breadboard-target experiments, not board-ready releases.

The combined-folder failure names duplicate `ESPNOW_CHANNEL`, message types/structs, callbacks, `setup()` and `loop()`. Original layout is preserved in the archive. The working build layout has two separate Arduino sketch folders, each containing the unchanged matching .ino filename. This establishes distinct build targets without editing any source.

## Repeat the experiment

From this directory with Python 3.9+ and the recorded ESP32 platform/tool packages installed:

```sh
python3 verify.py
# Only if the ignored snapshot folder has not already been extracted:
tar -xzf originals-2026-09-07.tar.gz
python3 build_candidates.py --run reproduction-02
```

Use a new run name; the runner refuses to overwrite existing logs or working copies. `--cli` can select the recorded CLI executable on another machine. The runner uses `/Users/erik/Library/Arduino15` as the local data path; adjust that explicit path when reproducing elsewhere and record the change. It checks the reported board core version is 3.3.7. It does not install/upgrade cores or upload firmware. The version guard was added after this run; the saved board-detail evidence independently records 3.3.7 for the executed builds.

Each command is recorded exactly in the corresponding log. General form:

```text
arduino-cli --config-file <isolated-config> --no-color compile
  --fqbn esp32:esp32:esp32s3
  --libraries <captured-library-copies> --jobs 4
  --build-path <isolated-target-build> --warnings default --verbose <sketch-folder>
```

Use the C3 FQBN for old Beacon sketches. No source pin remapping is applied in this experiment.

## Warnings and limits

Successful compile/link establishes compatibility with this host toolchain, not timing, radio delivery, RTC operation, correct UI, wiring, supply behavior, physical fit or old/new PCB compatibility. Legacy I²S deprecation warnings are retained in full in the logs; success does not imply a warning-free or production-qualified implementation. Raw tool output retains its original whitespace, with a scoped Git attribute excluding those evidence files from whitespace lint. No physical criterion is promoted to passed by these build results.

The PCB matrix records required changes to I²S, OLED driver/power/isolation, button roles, C3→S3 sensor target, UART, radar sequencing, battery monitoring, sleep and protocol behavior. Firmware work should follow those PCB contracts, as Erik directed. The archive is a reference, not the future release source tree.
