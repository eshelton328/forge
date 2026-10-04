# Cube diagnostics — first bring-up image

ROO-011's first Cube target uses **ESP32-S3-WROOM-1-N16**, 16 MB QIO flash,
no PSRAM, Arduino CLI **1.4.1** and Espressif Arduino core **3.3.7**. No external
Arduino libraries are used. It initializes inactive outputs and reports digital
inputs over native USB CDC and J7 UART at 115200 baud.
**Compiled and host-tested; custom-board flashing and physical tests are NOT RUN.**

Sensor diagnostics, RTC transactions/wake, display, audio, ADC calibration,
radio and the finished alarm remain future work. Full ROO-011 is incomplete.

## Build from a clean checkout

Install [Arduino CLI 1.4.1](https://github.com/arduino/arduino-cli/releases/tag/v1.4.1)
and Python 3.9 or later. The first build needs internet/disk space for the pinned
Espressif platform/compiler. From the repository root:

```sh
python3 firmware/rooster/tools/build.py
```

Use `--cli /path/to/arduino-cli` or `ARDUINO_CLI` if it is not on PATH. On this
Mac the existing executable is inside Arduino IDE:

```sh
python3 firmware/rooster/tools/build.py \
  --cli '/Applications/Arduino IDE.app/Contents/Resources/app/lib/backend/resources/arduino-cli'
```

The builder checks the CLI version, source-bound hardware contract and profile,
stages independent pin/identity headers, and uses a clean build directory.
It prints a new run directory under `.cache/rooster-cube/` containing:

- `artifacts/`: application, bootloader, partition binaries and ELF/map files.
- `manifest.json`: source/contract hashes, Git revision (including dirty state),
  FQBN, versions, exact command and SHA-256 for every emitted artifact.
- `compile.log` and `sketch/cube_diag/`: captured transcript and build inputs.

[sketch.yaml](cube_diag/sketch.yaml) uses JSON syntax, which is valid YAML and
readable by Python's standard library. [Arduino build profiles](https://docs.arduino.cc/arduino-cli/sketch-project-file/)
resolve versioned platforms in isolated storage. The Browns archive and installed
user libraries are not build inputs. Generated headers belong in the staged copy;
compiling the source `.ino` directly is intentionally incomplete.

## Hardware contract and startup

[board-contract.json](board-contract.json) binds native source bytes at merged
baseline `01c1450` to named signals and netlist peers. Builds fail on changed
sources; review electrical/firmware impact before making a new binding. This is
ROO-013's scoped diagnostic contract, not its complete application protocol.

| Signal | GPIO | This image after setup |
| --- | --- | --- |
| Amplifier 5 V enable / SD command | 18 / 21 | LOW / LOW |
| I2S BCLK / LRCLK / data | 47 / 48 / 14 | LOW |
| Display bus enable / power | 11 / 41 | LOW / LOW |
| Battery-divider enable | 12 | LOW; no ADC conversion |
| RGB R / G / B | 38 / 39 / 40 | HIGH, common-anode LEDs off |
| VOL− / MODE / VOL+ / battery button | 4 / 5 / 6 / 10 | Inputs, active LOW, 10 ms debounce |
| 3.3 V PG / 5 V PG / USB detection | 15 / 13 / 7 | Inputs, active HIGH, raw digital status |
| RTC interrupt | 1 | Input, active LOW; no time-validity assertion |
| ADC / I2C SDA / SCL | 2 / 8 / 9 | Inputs; no peripheral traffic |

Output latches receive inactive levels before enabling output mode, using the
[ESP-IDF GPIO API](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/gpio.html).
External pulls are retained; internal pulls stay disabled. Startup failures report
`startup_ok:false`. Firmware cannot control ROM/reset/pre-setup transients, which
need measurement. GPIO0 and USB 19/20 are not repurposed; UART owns 43/44. Setup
never waits for a USB host. No command enables a load.

## Flash and recover — after bench prerequisites pass

Follow [RUNSHEET.md](RUNSHEET.md) first. USB is data only: the target needs its
separate reviewed power source. This task did not flash hardware.
Set `CUBE_RUN` to the exact successful directory printed by the builder, and
`CUBE_PORT` to the actual device identified by `arduino-cli board list`.

```sh
python3 firmware/rooster/tools/build.py --verify "$CUBE_RUN/manifest.json"
arduino-cli upload --profile cube --port "$CUBE_PORT" \
  --input-dir "$CUBE_RUN/artifacts" "$CUBE_RUN/sketch/cube_diag"
arduino-cli monitor --port "$CUBE_PORT" --config baudrate=115200
```

For first upload/recovery, hold BOOT, press/release RESET, then release BOOT to
enter the ROM loader. Recheck the port before upload; reset afterward if needed,
reopen the application port and request `info`. The [Espressif USB guide](https://docs.espressif.com/projects/arduino-esp32/en/latest/tutorials/cdc_dfu_flash.html)
describes CDC/recovery. This profile uses Hardware CDC/JTAG with CDC on boot.

J7 provides ROM UART0 recovery and the same application console. Use 3.3 V logic,
adapter TX→J7.4/RX44, adapter RX←J7.3/TX43, GND→J7.1. J7.2 senses target voltage;
it must not power the target. Enter the ROM loader manually. Follow
[HARNESS.md](../../../../boards/alec-main/HARNESS.md) for fixture access; do not
use 5 V logic or assume an automatic RTS/DTR circuit exists.

## Commands and logs

Send lowercase commands terminated by LF or CRLF:

| Command | JSON-lines reply |
| --- | --- |
| `info` | Target, source/contract identity, chip ID, embedded ELF hash, reset reason and startup result |
| `status` | Raw input levels, debounced active states, transition counts and commanded-off state |
| `help` | Supported commands and read-only mode |

`image_id` is the first 12 characters of the source-set SHA-256, not the application
binary hash. Match full source/contract identities to the manifest and retain its
application/ELF hashes. `chip_id` identifies the MCU, not the physical PCB/unit;
record those separately. Preserve the manifest, `info`, raw status lines and reset
observations with each session. USB requires an `info` request after opening;
UART also sends startup info. ROM/CLI messages can appear outside the JSON stream.

Each input's `raw` is 0/1; `active` uses the table's polarity. Buttons start with
`active:null` until stable for 10 ms. A button held at boot becomes active without
inventing a transition. `transitions` counts both debounced edges. PG/USB/RTC are
undebounced digital observations, not rail voltage, RTC time validity or acceptance.
On startup failure input values are null and `loads_commanded_off:false` means
inactive output initialization was not established.

Lines over 31 characters or containing nonprintable bytes are discarded through
the terminator and return `invalid_line`; unknown commands return `unknown_command`.
Send one command and await the reply. Bounded responses drain in available chunks;
congestion never waits in the sampling loop. USB disconnect discards partial
commands/replies. No command changes power, LEDs, I2C, audio, radio or flash.

## Verify and extend

```sh
python3 firmware/rooster/tools/contract.py
python3 -m pytest tests/test_cube_diagnostics.py -q
```

Host tests compile the actual sketch with GPIO/serial substitutes using C++17.
They check latch-before-output ordering, inactive levels, reserved pins, startup
failure, bounce/rollover, malformed commands, absent/stalled/disconnected USB,
source/MCU/polarity mistakes and altered/incomplete artifacts. They do not model
ESP32 electrical behavior or USB hardware. CI repeats these checks and compiles
the pinned target. The [Browns originals](../../../../docs/rooster/baselines/2026-09-07/README.md)
remain unchanged. Add one reviewed peripheral diagnostic at a time using the
existing ROO-004 bench cases and identified physical samples.
