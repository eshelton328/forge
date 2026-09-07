# ROO-002 physical prototype ledger

As of September 7, 2026. No new physical tests, uploads, module queries or wiring changes were performed. The source declarations imply S3 alarm/C3 sensor targets, but do not identify Erik's actual module variants or board revisions.

| ID | Physical stage and evidence | Software/source association | Reproduction status and missing evidence |
| --- | --- | --- | --- |
| P01 | Breadboard alarm/sensor: Erik reports building a prototype and rough sketches, and explicitly confirms the existing sketches are old breadboard code | Erik identifies cube_browns/beacon_browns as the most relevant reference pair, with “I believe” qualification; exact last-flashed bytes remain unconfirmed | Host builds in BUILD-REPORT.md; actual boards, wiring, OLED, RTC, amp, radar firmware and demonstrated behavior remain to identify. A source header's “working” claim is not new physical evidence. |
| P02 | Standalone buck-boost PCB: Erik reports a JLCPCB order, delivery and successful test | `boards/tps63070-breakout` is a plausible project lineage, not a verified manufactured revision | Need order/export revision, actual part marking, wiring/load/input and any surviving measurements. |
| P03 | Buck-boost + ESP32-S3 PCB: Erik reports mostly working, with VBAT/header input failure | Strong historical lead: July 18 fix `ad268c04a01746be538a1ff84e6b9e0186a9ef9e` / PR #118 for `esp32s3-devkit` | Commit narrative records a hardware workaround and geometry cause. Erik has not yet connected this exact history to his board/order in this task. Manufactured revision and post-fix retest remain unknown. |
| P04 | Current ALEC main/controls/front: native design inspected at `dc57b550ebe8c1943e7830468d73af3f93c5bb73` | Destination PCB interface, not a flashed prototype | Design/source evidence only. No physical pass established here. Old breadboard mappings should be adapted to these boards. |
| P05 | Current ALEC sensor S1.1: S3-WROOM-1-N16 + LD2410C + RTC and switched radar circuitry at the same commit | Destination S3 sensor interface; old Beacon is C3 reference code | Design/source evidence only. Actual assembly, module firmware, readiness timing, dwell, radio and power/sleep behavior remain unmeasured. |

## Recovered VBAT evidence

The [saved commit record](evidence/vbat-fix-commit.txt) says assembled boards did not power up because Q1 drain on `/VBAT` had no filled copper connection. It reports that injecting battery+ into the downstream `/PFET` net booted the board. These are **historical claims in the repository**, not measurements made in this task.

The [actual PCB diff](evidence/vbat-fix-pcb-diff.txt) adds an explicit 0.8 mm F.Cu `/VBAT` segment between coordinates (128.515, 119.09) and (127.5775, 109.115). The commit identifies this as J1.2→Q1.3 and adds the copper-connectivity guard used in later CI. Its reported pre-fix failure and post-fix pass were not rerun here.

This is substantially stronger evidence than an invented power-path hypothesis, but a repository fix date does not identify an order's Gerber export. Keep these distinct: (a) Erik's reported symptom, (b) the historical fix and reported workaround, (c) his physical board/order revision, and (d) any later measured repair/retest.

## Remaining identification

1. Preferred reference pair identified by Erik: cube_browns/beacon_browns, with “I believe” qualification; see `selected-reference.json` for full hashes. Exact flashed provenance remains open; no need to flash a device merely to identify code.
2. Tie each available physical prototype to module markings, wiring or an existing sketch/photo and order/export revision where available.
3. Confirm whether the July 18 VBAT record describes Erik's board, and whether it was repaired/retested.
4. Record original Arduino/FQBN/upload options and LD2410C module firmware if recoverable. The installed library's support description is not the module's actual firmware version.

Missing historical details limit claims about the old working baseline. They do not change Erik's confirmed decision to implement the new firmware against the current native PCB contracts.
