# Prototype source integration — September 7, 2026

The selected purchasing identities are now in all four native KiCad designs. **207 fitted references reconcile between the sourcing list, freshly exported schematic netlists, native PCBs and review BOMs.** Main R11 stays DNP; main J7 stays fabricated probe pads excluded from BOM/placement. The Beacon J3 remains the Samtec socket only; the purchased radar module remains separate procurement.

Only `MPN`, `Manufacturer`, `LCSC#` and `Datasheet` properties changed in the eleven native PCB/schematic files. This applies the nine GRT188R61A106KE13D capacitor selections, the Royalohm 150-ohm selections, complete connector/device ordering suffixes and previously missing main-board identities. Nominal values, voltage constraints, footprints, pins, nets, fit flags, routing, board outlines and 3D model transforms are preserved.

## Validation

- [Source transition](source-metadata-transition.json): original and current file hashes, baseline commit and signatures covering every parsed token except the four allowed purchasing properties on real component instances. The verifier reconstructs the original sources from Git and rejects any other change.
- [Independent KiCad geometry comparison](native-geometry-comparison.json): all four original/current loaded boards have identical outlines, footprint/pad geometry, tracks, vias and saved filled copper after excluding only the PCB file hash.
- [Fresh netlist comparison](native-netlist-comparison.json): all component values, footprints, fit flags and named-net/reference/pin tuples match the reviewed baseline.
- All four boards pass fresh ERC and DRC with zone refill and schematic parity, filled-copper connectivity, and their selected JLCPCB fabrication-rule profiles. No native board was rewritten by a router or zone-save operation. Cube board-intent checks pass; the Beacon uses its dedicated 47 design checks because it has no generic `checks.yml`.
- Cube: 487 circuit/interface checks and 145 layout guards pass. Beacon: 47 design checks, 8 rear-service checks, all 88 BOM/native metadata matches and 27 capacitor-package checks pass; its layout guard passes.
- Purchasing-update regression cases cover placement, layer, net, copper width, DNP, nominal-value and model-offset changes; stale value/footprint input, duplicate fields and idempotence are checked. The repository suite reports **140 passed, 1 skipped**; 13 tests specifically exercise the purchasing updater. `tests/test_physical_screening.py` is skipped at collection because SciPy is unavailable in this interpreter. The historical numerical solver run was not repeated; geometry and its model assumptions are unchanged.

The historical Cube enclosure exports and nominal physics report retain their original hashes. Their verifier accepts only the explicit metadata transition and checks current structural signatures. The original simulation assumptions and limitations remain in force; the power-component review separately assesses the selected real capacitors. Existing sensor enclosure evidence remains historical: its embedded PCB hash predates this update and is not relabeled as a fresh export. Finished enclosure validation does not gate these bare-board prototype orders.

## Reproduction and remaining work

The schematic/PCB generators apply the shared `scripts/alarm/order_parts.py` purchasing overlay after creating the native design. Apply a purchasing-field update directly with that script, without regenerating routing. `--check` detects drift without writing files. Generate fresh native XML netlists and call `export_bom(board)` to refresh review BOMs. Run `docs/rooster/prototype-order/tools/compare_native_sources.py` with KiCad Python to reproduce both independent comparisons. `verify_sourcing.py` checks agreement before `build_quote_inputs.py` creates the four BOM/CPL pairs from the native purchasing fields and native positions.

Source integration is complete; manufacturing release remains open. Complete the remaining package/pin/rating and external battery/harness checks, prepare matching fabrication archives, then inspect supplier assembly previews and obtain the actual quantity/service/shipping quote. RTC procurement timing remains open. No supplier upload, preorder, reservation, payment or PCB order has occurred.
