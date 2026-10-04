# Cube diagnostic verification — 2026-10-04

The first ROO-011 Cube slice compiled from clean commit
`36b0c3715bcd07e869eb22892a511c2589145204`, on the merged ROO-007 baseline
`01c1450`. This record identifies the tested sources and emitted artifacts;
subsequent documentation commits do not change that tested revision.

## Results

- **Host software:** 181 passed, one optional SciPy-dependent physical-screening
  module skipped, 14 existing Matplotlib/Pyparsing deprecation warnings.
  The 17 new Cube tests are included: startup ordering/polarity/failure,
  real-sketch serial parsing/backpressure/disconnection, input debounce/rollover,
  contract rejection and build-artifact integrity.
- **Source contract:** fresh KiCad 10.0.1 XML export passes the Cube GPIO/net-peer
  checks; every frozen source hash matches. Fontconfig warnings occurred during
  export. No native design was changed.
- **Preservation:** all 15 original sketches and two dependency archives match
  their retained hashes, including comparison with the original source files.
- **ESP32-S3 compilation:** Arduino CLI 1.4.1, Espressif core 3.3.7, 16 MB flash,
  no PSRAM, Hardware CDC. 322,060 bytes of program storage and 25,496 bytes of
  dynamic memory. SDK header missing-field-initializer warnings are retained in
  the compile log; the host sketch builds with warnings treated as errors.
- **Artifact integrity:** emitted file hashes pass verification. Offline esptool
  inspection validates the image checksum/digest, ESP32-S3 target and embedded
  ELF SHA-256 against the saved ELF artifact.
- **Physical execution:** **NOT RUN**. No custom board was powered or flashed.
  Reset-time output behavior, actual rails/current, USB/UART behavior and button
  response still need the identified-unit bench session.

[verification.json](verification.json) records commands and tool versions.
[build-manifest.json](build-manifest.json) preserves the exact build invocation,
source hashes, pin contract and all artifact hashes. Its absolute paths locate
this local run; binaries remain in that ignored run directory. The copied
manifest here is historical evidence, not an upload bundle: use `--verify` on the
original run or a complete downloaded CI bundle with adjacent `artifacts/`.
CI builds and uploads a new identified bundle for each applicable PR run.
Cross-host bit-identical binaries are not claimed.

Source-set image ID: `f18ec0dd306e` (not a binary checksum).

| Artifact | SHA-256 |
| --- | --- |
| Application | `3396b2f20398850e8c76f2a3c090cfd56092a4043f7296572003f06fe5471529` |
| ELF | `6a4752c830570cca9f02bee044d5f4bdcb3cfd42d2f3e3c94e384a07012bd8c9` |

The [build/flash guide](../../../../firmware/rooster/diagnostics/alarm/README.md)
and [first-power run sheet](../../../../firmware/rooster/diagnostics/alarm/RUNSHEET.md)
cover this bounded slice. Sensor diagnostics and Cube RTC/display/audio/ADC,
radio and sleep tests remain open; full ROO-011 and ROO-013 are not complete.
