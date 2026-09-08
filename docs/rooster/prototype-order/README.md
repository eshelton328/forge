# Rooster Cube + Beacon prototype PCB order

**Goal: place the factory-assembled PCB orders so the Cube and Beacon can be tested while firmware development continues.** The order-placement milestone ends with submitted orders and confirmations for the selected four-board set. Delivery, bring-up and complete firmware acceptance follow under their existing tickets.

## Order approval

Erik explicitly instructed on September 7: **"Please don't place the order without my permission."** Preparing files, supplier quotes and reviewable order details may continue. Do not submit a PCB order, parts preorder/reservation requiring payment, checkout or payment until Erik explicitly approves the exact items, quantities and total. Quote preparation or sign-in is not permission to purchase. No order has been placed by the agent.

## Current state

The [September 8 order checklist](order-readiness-2026-09-08.md) records the
critical path: RTC warehouse receipt, placement reconciliation, final quote,
Erik's purchase decision, then manual production confirmation. A parts preorder
today does not make the complete assembly order ready tonight. The
[prototype power scope](prototype-power-disposition.md) retains the current
circuitry for supervised current-limited bench evaluation, with battery
protection and real-load testing explicitly handed off before battery use.

Order preparation is on `codex/rooster-prototype-orders`, based on `0d0d8af3b1d2c60616f77a5116eba637098acf98`. All four designs have signed-in Standard-assembly drafts and price previews. Controls/front have all fitted parts matched; main has 41 of 42 BOM groups and Beacon 37 of 38, with only the RTC unavailable. Main/Beacon previews are explicitly **INCOMPLETE RTC - REVIEW ONLY**. Their full BOMs still require U5. The current four draft estimates sum to **$791.07 including separately listed rail removal, before RTCs and related fee changes, shipping, tax and external parts**. Main/Beacon now use the current source and fill/cap process; controls/front retain September 7 observations. No complete landed quote, manufacturing release or order exists.

Separate [supplier CPL candidates](supplier-placement-candidates/README.md) correct the controls buttons and main/Beacon header centers; main J4 also rotates to match its vertical holes. Native geometry is unchanged. U3 model/placement alignment, remaining manufacturing dispositions and missing-model orientation checks remain open. [Quote progress](quote-progress.md) records exact inputs, services, prices and review scope.

The [manual placement review sheet](placement-review/README.md) now supplies a
source-bound reference for all 207 fitted components and exact targets for the
observed supplier-preview ambiguities. It is prepared locally, not a supplier
sign-off. The [external-parts inventory](external-parts.md) reuses the existing
holder, speaker, display and radar candidates and gives gross cable/part counts
before checking owned inventory.

The [via-process review](via-process/README.md) supersedes the large boards'
Plugged quote setting with epoxy fill and copper cap. It specifies 255 main and
199 Beacon holes while keeping component holes open. Both refreshed assembly
drafts now confirm **$99.41 fabrication per batch**, a combined $40.82 increase.
They also select the [named prototype stackup](stackup-review/README.md), with
the recorded USB test/rework risk. The total above is draft arithmetic, not a
landed quote or purchase request.

- [Input audit](input-audit.json): at kickoff, 69 source-map hashes matched the baseline checkout, 136 Cube saved bindings matched, and 214 Sensor bindings matched their preserved review inputs. PRs #126/#127 were merged, with no open PRs at capture. The subsequent native purchasing-field changes are recorded separately below.
- [Sourcing inventory](sourcing.csv): 208 original review BOM rows across the four boards, including one explicit DNP. All 207 fitted rows have exact selected MPNs and manufacturer-specific catalog IDs, including the 95 populated main-board rows missing MPNs in the original review. [Part selection review](part-selection-review.md) records substitutions and remaining checks. Of the 51 selected unique parts, the RTC has no ready catalog stock in the dated capture.
- [Source integration](source-integration-review.md): selected purchasing fields now reconcile across the eleven native files, fresh netlists and review BOMs. Independent source-token and KiCad geometry checks confirm that values, circuits, copper, fit flags and models are preserved. The CSV remains a sourcing record, not a supplier-upload BOM.
- [Draft quote BOM/CPL inputs](draft-quote-inputs/README.md): four BOMs and four placement files cover all 207 fitted references, including both faces and through-hole parts. They now use reconciled native purchasing fields and native positions; remaining component checks, supplier rotations and fabrication outputs still gate release.
- [Power-component review](power-component-review.md): eight local converter capacitor banks pass the source-bound selection calculation using manufacturer bias models and explicit tolerance/reserve assumptions. Nine proposed 0603 capacitor references change to GRT188R61A106KE13D; inductors and layout are retained. Actual startup, transients, depleted-cell operation and temperatures remain first-board measurements.
- [Fabrication candidates and CAM check](fabrication-candidates/README.md): four Gerber/drill/BOM/CPL sets agree with native holes, slots, outlines, copper-layer counts and all 207 fitted references. The [additional drawing review](assembly-drawing-review.md) records JST PH pad agreement and the basis for retaining the amplifier copper pads. Its 17-pin map and rounded paste calculations are verified. The [mask review](mask-review/README.md) supports retaining uniform 1:1 openings; [fill/cap requirements](via-process/README.md) cover exposed vias. Supplier orientation and final production data remain open.

## Board scope

| Device | Board | Layers |
| --- | --- | --- |
| Cube | alec-main | 4 |
| Cube | alec-controls | 2 |
| Cube | alec-front | 2 |
| Beacon | alec-sensor | 4 |

Erik’s selected first quote target is **5 fabricated / 2 assembled copies per design at JLCPCB**. Across four separate designs this means 20 fabricated PCBs, 8 assembled PCBs (two complete Cube + Beacon sets) and 12 spare bare PCBs. Confirm any panel/unit counting in the actual quote. Services, final cost and spending decision remain open.

Equipment confirmed by Erik: **multimeter and oscilloscope**. Instrument models/probes, a current-limited source, programming cables/adapters and soldering capability are unconfirmed, not assumed absent. The [first-power access handoff](first-power-access.md) records feasible connections, required external items and the later run-sheet work; it does not claim equipment availability or completed tests. See [JLCPCB assembly preflight](jlcpcb-preflight.md).

The Beacon uses a **purchased Hi-Link LD2410C radar module plugged into J3**, not a custom radar built into our PCB. J3's BOM MPN identifies the **Samtec socket only**. Two compatible radar modules are required for the two assembled Beacon units, accounting for verified existing inventory; their separate purchase/installation is not included merely by ordering PCB assembly. Retain the current header/socket version for this prototype; the LD2410C-P surface-mount variant is not a drop-in substitution. See [radar procurement and variant checks](beacon-radar-procurement.md).

## Remaining order work

| Item | Work and closure evidence | Owner |
| --- | --- | --- |
| Current source/evidence | Source continuity checked in input-audit.json; consume the reviewed board findings at the recorded revision | ROO-009 handoff |
| Exact components | Native purchasing metadata applied and verified; finish remaining IC/package/pin/ratings checks. Local capacitor-bank and inductor selection has a recorded disposition; maintain DNP/excluded-pad treatment | ROO-010; Cube O01, Beacon O02 |
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
