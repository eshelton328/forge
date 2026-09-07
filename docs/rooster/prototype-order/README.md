# Rooster Cube + Beacon prototype PCB order

**Goal: place the factory-assembled PCB orders so the Cube and Beacon can be tested while firmware development continues.** The order-placement milestone ends with submitted orders and confirmations for the selected four-board set. Delivery, bring-up and complete firmware acceptance follow under their existing tickets.

## Current state

Order preparation has started on `codex/rooster-prototype-orders`, based on `0d0d8af3b1d2c60616f77a5116eba637098acf98`. No quote, supplier submission, manufacturing release or order exists yet. The existing design reviews supply the starting evidence; this directory is an order workspace, not an upload-ready release.

- [Input audit](input-audit.json): 69 source-map hashes match this checkout; 136 Cube saved bindings match; 214 Sensor bindings match their preserved review inputs. PRs #126/#127 remain merged, with no open PRs at capture. These checks verify evidence continuity, not electrical or physical performance.
- [Sourcing inventory](sourcing.csv): 208 source review BOM rows across the four boards, including one explicit DNP. The Cube main review BOM has 95 populated rows without an explicit MPN. Existing MPNs are candidates pending verification; empty supplier and assembly fields are unresolved.
- Native boards, schematics, models and firmware are unchanged by this kickoff. The CSV is a working sourcing list, not a supplier-upload BOM.

## Board scope

| Device | Board | Layers |
| --- | --- | --- |
| Cube | alec-main | 4 |
| Cube | alec-controls | 2 |
| Cube | alec-front | 2 |
| Beacon | alec-sensor | 4 |

Erik’s selected first quote target is **5 fabricated / 2 assembled copies per design at JLCPCB**. Across four separate designs this means 20 fabricated PCBs, 8 assembled PCBs (two complete Cube + Beacon sets) and 12 spare bare PCBs. Confirm any panel/unit counting in the actual quote. Services, final cost and spending decision remain open.

Equipment confirmed by Erik: **multimeter and oscilloscope**. Instrument models/probes, a current-limited source, programming cables/adapters and soldering capability are unconfirmed, not assumed absent. Review practical first-power and bare-board USB/recovery access before adding equipment to procurement. See [JLCPCB assembly preflight](jlcpcb-preflight.md).

## Remaining order work

| Item | Work and closure evidence | Owner |
| --- | --- | --- |
| Current source/evidence | Source continuity checked in input-audit.json; consume the reviewed board findings at the recorded revision | ROO-009 handoff |
| Exact components | Resolve every fitted reference’s exact MPN/package/ratings/pins; verify capacitor effective values and power-component limits; maintain DNP/excluded-pad treatment | ROO-010; Cube O01, Beacon O02 |
| Supply and assembly | Supplier IDs/availability, substitutions, both-side SMD and through-hole coverage; explicit factory-fitted versus local work | ROO-010; Cube O01, Beacon O03 |
| Battery and external parts | Establish intended cell/load envelope; exact holders/leads, display/socket, speaker, GH/PH mates/harnesses, radar module/socket and ratings/orientation | ROO-013/010; Cube O02/O03, Beacon O02/O03/O05 |
| Hardware and service interfaces | Version pins, power sequencing, board-dependent geometry and service access; use native USB plus accessible reset/boot if it provides a viable bare-board recovery route | ROO-013/011; Cube O04, Beacon O04/O05 |
| Manufacturing packages | Generate four matching Gerber/drill/BOM/placement sets; inspect stackup, holes, rotations/pin 1 and assembly scope; run required checks on the final candidate | ROO-010; Cube O05, Beacon O01 |
| Quote and placement | Concrete quantity/service/landed-cost options and exclusions; Erik’s selection, then exact submitted file hashes and order confirmations | ROO-010 → ROO-014 |

Sourcing/package review can proceed while ROO-013 settles interfaces. Only an actual circuitry, component, geometry, assembly or testability issue returns to PCB correction. Full application protocol/UI, completed enclosures, commercial costing and the month-long Cube runtime trial do not gate ordering dry engineering boards. The Cube monthly target remains a design input.

## Firmware handoff during fabrication

Use ROO-002’s preserved sketches and PCB port matrix, ROO-007’s stable firmware paths, and ROO-013’s electrical/power map for ROO-011 diagnostics and incremental ROO-015 application work. Preserve originals. Hardware measurements wait for identified delivered units in ROO-012. The configuration screen and agreed alarm/fallback behavior remain required for the finished first version.

## Evidence and remaining distinctions

The Cube review is in the existing `the-forge-roo-004/docs/rooster/roo-004` package (local commit `f0b8dca`); the Sensor and source-map review records are in the Obsidian Rooster project. The audit records the files and hashes consumed here. Keep original review packages and source history; order artifacts receive their own final revision and hashes when ready. The detailed Oxx identifiers are local to each device review, not globally unique tickets.
