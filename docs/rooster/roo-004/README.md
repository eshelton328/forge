# ROO-004 — Cube prototype acceptance review

Specification v1, September 7, 2026. **Review draft delivered; order release and all physical tests remain open.** The three-board alarm set is covered. No demonstrated fault from this review calls for changing the routed converter geometry.

The immediate handoff is a bounded order-gap list and an executable bench specification. [BENCH.md](BENCH.md) defines test conditions and dispositions; [SOURCES.md](SOURCES.md) identifies component limits and drawings; [evidence/source-review.json](evidence/source-review.json) records native-source traceability. [bench-results.csv](bench-results.csv) starts every physical case as NOT RUN.

## Revision and actual evidence

- Worktree: `/Users/erik/Workspaces/the-forge-roo-004`, branch `codex/roo-004-cube-acceptance`.
- Freshly fetched `origin/main`: `0d0d8af3b1d2c60616f77a5116eba637098acf98`. Its alarm native boards, harness, review package, scripts and v4.2 enclosure are unchanged from the prior `dc57b550ebe8c1943e7830468d73af3f93c5bb73` review baseline. The intervening alarm changes are generated `docs/` artwork only. The original `/the-forge` checkout at `afede0f` is not this review's source.
- Current native schematics exported with KiCad CLI 10.0.1. All three exports match saved component values/footprints and net topology. Every exported schematic node matches its native PCB pad net: **363 main, 16 controls, 12 front**.
- The repository's filled-copper guard freshly passes **355 main, 16 controls, 12 front** multi-pad nodes. This tests whether pads touch same-net copper; it is not an independent complete copper-network graph proof. Physical end-to-end continuity remains B01/B02.
- **136/136** saved QA source/evidence hash bindings match. The existing focused suite `python3 -m pytest -q tests/test_alarm_pcbs.py` freshly passes **5/5**. Saved zero ERC/DRC/fab violations, 487 interface checks, 145 layout checks, simulations and 52 assembly checks are inherited, hash-bound results. ERC/DRC, simulations, thermal solvers and assembly renders were not rerun.
- Logs `evidence/check-01.txt` through `check-08.txt` record actual commands/exits, including the source collector. Fontconfig and KiCad/wx diagnostics occurred; commands exited zero. The separate native comparison and hash checks succeeded. Python 3.9.13 with KiCad 10.0.1 produced the source review. System Python 3.9.6 / pytest 8.4.2 ran the focused tests; verify the captured environment if reproducing elsewhere.

For reproduction, use the commands in the logs, then run `collect_evidence.py` with KiCad Python from the worktree root. Fresh XML goes into `.cache/roo-004/`; no generator is needed. The collector does not edit schematics, PCBs or inherited reports. Its edge bounding boxes include the 0.05 mm Edge.Cuts stroke; nominal board dimensions below are the outline centerlines.

## Alarm set and dependencies

| Item | Reviewed requirement | Source |
| --- | --- | --- |
| alec-main | 64 × 56 × 1.6 mm, four layers; MCU, battery protection, 3.3/5 V conversion, RTC, display switching/isolation, amplifier, USB and service | `boards/alec-main/alec-main.kicad_sch`, `power-monitor.kicad_sch`, `.kicad_pcb`, `board.yml` |
| alec-controls | 27 × 34 × 1.6 mm, two layers; three B3F-1060 buttons and EG1218 enable switch; J1 on B.Cu | Native controls schematic/PCB and `review/bom.csv` |
| alec-front | 24 × 10 × 1.6 mm, two layers; B3U-1000P button and 150141M173100 common-anode RGB; J1 on B.Cu | Native front schematic/PCB and `review/bom.csv` |
| External electrical parts | Two GH harnesses, battery holder/cells/PH lead, PH speaker lead and speaker, four-pin I2C OLED and exact socket, USB cable and 3.3 V UART adapter/probes | [Harness](../../../boards/alec-main/HARNESS.md), vendor sources S05–S10; exact purchased-part identities are not yet established |
| Mechanical/service | v4.2 enclosure, mounts/fasteners, caps, light pipe, cable bends and 8 × 10 mm probe corridor through 10 × 12 mm opening | `enclosures/alec/pcb-revision/` native assembly and verification |
| System dependencies | Sensor/radio peer and protocol under ROO-005/013; diagnostic firmware ROO-011; product behavior/settings under ROO-001/006/015 | ROO-002 preferred breadboard pair is historical; adapt firmware to PCB assignments |

The sensor is the fourth design in the paired order, outside the three-board Cube electrical review.

## Review matrix

All rows use source revision **R1 = `0d0d8af3b1d2c60616f77a5116eba637098acf98`**, with native/source hashes in the evidence JSON. S-identifiers refer to [SOURCES.md](SOURCES.md). O = gate before the affected prototype fabrication/assembly package; B = physical bench gate or characterization; P = later assembled-product qualification. A pending P gate is not automatically an O gate.

| ID / requirement | Source at R1 / present evidence | Gap and disposition | Gate / owner / cases |
| --- | --- | --- | --- |
| M01 — all three boards and selected parts agree | Native exports/PCB nodes and 136 QA bindings match; nominal dimensions/layers verified; BOMs have 112/5/3 rows | Exact supplier/package/drawing and purchased-item comparison pending. Main CSV has 96 empty MPN fields, including DNP R11; some identities exist in Value, but this is not an orderable sourcing map | O: O01, ROO-010/013; B01 |
| M02 — battery through protection reaches both converters | J1.1 `/VBAT` → Q1.3 drain; Q1.2 source `/PFET` → U1/U2.12/.13; J1.2 GND. Fresh copper guard passes | Measure connector, cable and Q1 drop under load. Historical J1.2→Q1.3 failure used an older numbering/revision; do not apply that pin label to this J1 | B: ROO-002/011/012; B01/B02/B05 |
| M03 — actual battery envelope supports alarm loads | BH3AAW three-AA allocation; ADC protected-node envelope 0–6 V; S01 cold-start requirement is ≥3 V at converter VIN | Chemistry, cell maximum, holder/lead rating, restart margin and useful cutoff not frozen; below-3-V running is not a guaranteed cold start | O: O02, ROO-010/013; B/P: D06, B02/B05/B13 |
| M04 — predictable standby/enable | Controls SW4.2 common → J1.7/main J5.7 → U1 EN; ON throw SW4.1 through R31 10 kΩ to PFET; OFF SW4.3 to GND; R32 100 kΩ holds unplugged EN low. U2 GPIO18 with R19 100 kΩ pulldown | OFF leaves VIN energized, is not charging or hard isolation, and does not retain RTC time after 3.3 V decays. U2 shutdown follows GPIO18/reset behavior and must be measured during power-down | B: ROO-011/012; D05 product consequence to ROO-001/013; B02/B03/B09 |
| M05 — regulated rails, PG and load response | U1 R4/R5 = 470k/150k → 3.307 V nominal; U2 R8/R9 = 680k/130k → 4.985 V; PS/SYNC pulled to PFET selects power save; GPIO15/13 PG pullups both to 3.3 V. S01/S02/S04 | Freeze resistor tolerances/capacitor effective values before final rail bands; measure startup, ripple, dips, PG sequencing and temperature. PG alone does not establish valid MCU voltage | O01 component review; B: ROO-011/012, B03/B05; P: D06 |
| M06 — RTC bus and wake | U5 RV-3028-C7 VDD=3.3 V; GPIO8 SDA/9 SCL; GPIO1 INT with R18 pullup; VBACKUP via R33 10 kΩ to GND. S03 | No backup cell. Verify RTC survives MCU reset/sleep while powered, INT clearing/wake and power-loss invalidity; schedule/resync policy belongs to D05 | B: ROO-011/012, B08/B09; P: ROO-001/006/015 |
| M07 — switched OLED with isolated I2C | GPIO41 → Q3/Q2 supply switch; GPIO11 → both U7 enables, R36 default LOW; RTC-side R16/R17 and OLED-side R37/R38 = 4.7 kΩ, latter to switched rail; J4 order GND/power/SCL/SDA. S05/S06 | Verify exact four-pin module/socket; sequence isolation before power-off, reconnect after power-up, test RTC with display off. Off-state leakage/settling unknown | O03, ROO-010/013; B: ROO-011/012, B07 |
| M08 — amplifier and differential speaker output | GPIO18 enables 5 V; GPIO21 → U8 3.3-to-5-V translation → SD_MODE, R20/R39 default shutdown; I2S GPIO47/48/14; J3.2 OUTP, J3.1 OUTN. S04/S06/S09 | Neither speaker pin is ground. Verify I2S held low when amp rail is off, start/mute sequencing, 8 Ω candidate speaker/harness, rail sag and sound | O02/O03; B: ROO-011/012, B06; P: D06/ROO-017, B13/B14 |
| M09 — controls harness, polarity and bounce | J5 pin order below, two GHR-07V-S, BM07B-GHS-TBT at both boards; R50–52 100 Ω, R24–26 10 kΩ, C22–24 100 nF; full native trace. S07/S08 | Actual crimps, ≤200 mm allocation, insulation, actuator direction and ≥10 ms software debounce must be checked on sample | O03 sourcing; B: ROO-011/012, B01/B10; P: ROO-016 |
| M10 — front button and RGB | J6 order below; two GHR-06V-S, BM06B-GHS-TBT; R53 100 Ω/R27 10 kΩ/C25 100 nF; RGB R28=330 Ω red, R29/R30=150 Ω green/blue; active LOW GPIO38/39/40. S07/S08 | Verify common-anode LED orientation, currents/visibility and actual B3U cap actuation; distinguish battery request from conditionally eligible alarm override in application firmware | O03; B: ROO-011/012, B10/B11; P: ROO-001/006/016 |
| M11 — USB is self-powered data service | J2 VBUS feeds ESD reference/detection only; CC1/CC2 each 5.1 kΩ; data via U4/R34/R35 22 Ω to GPIO19/20; Q4/Q5 produces GPIO7 USB detect | No charger, VBUS-to-system rail supply, USB/UART bridge or RTS/DTR auto-reset circuit. Bench USB with battery-powered target; check USB-only off-state leakage and recovery path | B: ROO-011/012, B04; O04 service plan |
| M12 — accessible, correctly wired programming | J7 pins 1 GND, 2 target 3.3-V sense, 3 TX43, 4 RX44, 5 EN/reset, 6 GPIO0; local RESET/BOOT remain; custom pad fixture allocated but unbuilt | Cross adapter TX/RX, use 3.3-V logic, no power into J7.2. Establish one workable bare-board recovery route before order; fitted enclosure fixture belongs to later service qualification | O04, ROO-010/011/013; B04; P: ROO-016 |
| M13 — battery/rail monitoring reflects actual circuit | GPIO12 enables Q6/Q7 divider; R48 33k/R49 10k, both specified 0.1%; ADC GPIO2 = PFET/4.3; C34 100 nF. ADC settling guidance 10 ms | Calibrate/measure settling, switch drop/leakage and rail-PG thresholds. RGB voltage bands and state-of-charge interpretation need chemistry/policy | B: ROO-011/012, B12; P: ROO-001/015 |
| M14 — PCB-led firmware compatibility | ROO-002 static port map and preferred pair hashes; full native GPIO mapping below | Breadboard control/audio/display pins differ; running old firmware unchanged could drive USB-detect GPIO7. Diagnostic port must initialize correct safe states | B: ROO-011; all powered cases; P: ROO-015 |
| M15 — fit and service tolerances | Hash-bound nominal v4.2 assembly, 0.055 mm front stem gap, mounts/connectors/probe corridor | Clearance is not a printer tolerance. Actual M2 hardware, B3U travel/stop, cable bends, USB access and optics need samples; a board change becomes O only if sample/part review demonstrates one | O03/O04 access disposition; B/P: ROO-013/016, B10/B15 |
| M16 — sound, endurance, RF and temperature | Prior behavioral/PCB thermal screening only; no physical performance data | Keep SPL/latency/endurance/range/use-temperature targets OPEN (D06). Set measurable methods now and return curves to product shaping; do not turn simulation fixtures into product limits | B characterization: B05/B06/B09/B13/B14; P: ROO-001/006/017 |

## Cable and GPIO contract to hand to ROO-013/011

Numbering is connector pin identity, not wire colors or the apparent order of a bottom-view photograph. Both GH cables are one-to-one, AWG28 within the selected contact insulation range, **≤200 mm each**. Unpowered isolated-cable continuity and shorts tests precede mating.

| Main connector | Pin order 1 → last |
| --- | --- |
| J5 → controls J1 | GND, VOL−, MODE, VOL+, GND, SW_ON, EN_3V3 |
| J6 → front J1 | GND, 3.3 V common anode, BAT button, red cathode, green cathode, blue cathode |
| J4 → four-pin OLED | GND, switched OLED_3V3, OLED_SCL, OLED_SDA |
| J1 → battery | **1 positive VBAT, 2 GND** |
| J3 → speaker | **1 OUTN, 2 OUTP**; both active BTL outputs |

| Function | Preferred old Cube reference → current ALEC | Firmware contract |
| --- | --- | --- |
| VOL− / MODE / VOL+ | 6 / 4 / 5 → **4 / 5 / 6** | Active LOW; RC plus software debounce ≥10 ms; verify upper/lower physical labels |
| Battery button | 10 → 10 | Active LOW; application decides request versus eligible single-press override |
| I2S BCLK / LRCLK / DATA | 15 / 16 / 17 → **47 / 48 / 14** | Old GPIO15 is now PG input |
| OLED power / bus enable | 7 / absent → **41 / 11** | Both default LOW; old GPIO7 is now USB-sense input |
| I2C SDA / SCL; RTC INT | 8 / 9; 1 → unchanged | Shared RTC bus remains live with OLED isolated |
| Amp rail / SD command | 18 / 21 → unchanged | LOW during boot/sleep; SD uses U8 translator; no high I2S drive into unpowered amp |
| RGB R / G / B | 38 / 39 / 40 → unchanged pins | Current common-anode channels are active LOW; port polarity explicitly |
| Battery measure enable / ADC | absent → **12 / 2** | HIGH enables; wait 10 ms; calibrated ADC ×4.3; LOW after sample |
| 3.3-V PG / 5-V PG / USB sense | absent → **15 / 13 / 7** | Inputs only; both PG pullups are 3.3 V |
| USB D− / D+; UART TX / RX | **19 / 20; 43 / 44** | Native USB and 3.3-V UART service; select ESP32-S3-WROOM-1-N16 build settings |

## Bounded corrections and order gates

These are required release-package corrections/decisions, **not claims that all listed components require replacement**. ROO-010 owns sourcing/assembly; ROO-013 owns any interface change. Keep the reviewed converter placement and copper unless a specific finding requires correction and revalidation.

| ID | What must be resolved | Concrete closure evidence |
| --- | --- | --- |
| O01 — exact component/assembly map | Convert reviewed BOM into supplier orderable parts. Reconcile the 95 populated main rows with empty MPN fields; use existing Value/datasheet identity where adequate. Select remaining passive tolerances/ratings, verify MLCC capacitance under DC bias (especially converter input/output and 100 µF packages), inductor current margin, exact MCU N16/RTC/amplifier/package variants | Per-reference manufacturer/order code, datasheet revision, supplier code and footprint/pin/rotation check; assembly side/through-hole coverage. R11 remains DNP; J7/TP pads remain unpopulated. No automatic substitute based on name alone |
| O02 — battery and load envelope | Resolve cell chemistry and maximum/minimum intended loaded voltage, cold-start headroom at PFET, holder/PH wiring current capability and peak-load trial plan | Dated parts/envelope sheet. Characterization below cold-start guarantee may proceed, but no guaranteed depleted-cell restart claim. A 2-A converter headline is not a three-AA output-current promise |
| O03 — exact external interfaces | Freeze PH battery/speaker mates, GH housings/contacts/cables, four-pin display/socket, switches/LED and service cable; inspect actual chosen drawings against copper, connector orientation, envelope and assembler coverage | Pin-by-pin drawing-to-PCB checklist, part codes and cable crimp orientation; mechanical/assembly review with ROO-013/016. Purchases are not assumed to have happened |
| O04 — practical bring-up access | Confirm current-limited first-power equipment and at least one bare-board programming/recovery method; provide adapter pin map and temporary contact/retention plan | ROO-011 equipment/procedure disposition and B01–B04 feasibility review. Native USB plus accessible RESET/BOOT can be the bare-board route; final enclosed J7 fixture need not block PCBs if that route is established |
| O05 — freeze/check exact production inputs | ROO-009 reconciles current sources; ROO-010 generates the actual three alarm packages alongside the sensor package and validates native/BOM/placement identity | Versioned predecessor handoff, output hashes, required ERC/DRC/connectivity/fab checks for the exact export, supplier/stackup/assembly review. This draft is not that release |

B01–B12/B15 supply physical bring-up evidence; B05/B09/B12–B14 also collect unknown performance. ROO-001 sets D06 product limits, ROO-016 handles fit/service samples, and ROO-017 runs everyday trials. The front cap, probe fixture, enclosure temperature, sound and endurance remain open without automatically requiring another PCB layout.

## Ticket acceptance and handoff

| Criterion | Draft result | Remaining condition |
| --- | --- | --- |
| ROO-004-AC01 | All three alarm boards, native schematic/PCB interfaces and external dependencies are covered | Exact purchased-part drawing comparison and O01/O03 identities remain open; no actual purchases were located or inferred |
| ROO-004-AC02 | Static specification complete: full power path, standby/RTC/USB behavior, programming and old-to-new pin changes explicit | Historical manufactured revision/retest is still ROO-002; physical regression B02 is NOT RUN |
| ROO-004-AC03 | B01–B15 define conditions, equipment, repetitions, measurement points and either pass rules or explicit characterization | D08 equipment inventory and ROO-011 feasibility review pending; final D06 performance thresholds remain OPEN |
| ROO-004-AC04 | Every matrix finding is assigned an O/B/P gate and owner; bounded O01–O05 list supplied | Owners must disposition actual order gaps; inherited reports do not close physical gates |

Keep ROO-004 **Active** pending the predecessor/part/equipment closure above; the draft can be consumed by ROO-005/010/011/013 now. ROO-009 remains Ready; this review contributes source evidence without marking that predecessor Done or waiving it. Product decisions and the shared decision register remain with the ROO-001 coordinator. No firmware, native board/enclosure source, remote issue, purchase or physical result was changed by this review.
