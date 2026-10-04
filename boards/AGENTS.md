# Board work

Read the board README, `board.yml`, native schematic/PCB and applicable interface
contract before editing. For Cube interfaces use
[alec-main/HARNESS.md](alec-main/HARNESS.md); for Sensor power and sequencing use
[alec-sensor/OPERATION.md](alec-sensor/OPERATION.md), reconciled with current
Rooster product decisions.

## Sources and changes

- Native `.kicad_sch`, hierarchical sheets, `.kicad_pcb`, `.kicad_pro`, library
  tables and custom libraries are design sources. Netlists, BOMs, renders and
  Gerbers are derived artifacts; establish which source revision produced them.
- Inspect [the Cube generator guide](../scripts/alarm/README.md) or
  [the Sensor guide](alec-sensor/tools/README.md) before running generators.
  The devkit-5v board remains an active generator input.
- A substitution requires exact MPN, package/pin mapping, ratings and mechanical
  review. For power parts include effective capacitance, saturation/thermal
  limits, startup and actual load cases. Match sourcing metadata to native files.
- Changes to pins, polarity, power sequencing, outlines, holes or connector
  positions require checking firmware, harnesses, enclosure and assembly outputs.
  Historical breadboard mappings do not override the PCB contract.
- USB is data/service on the current Cube and Sensor; it is not their battery
  charger or ordinary power source. Cube controls OFF disables a rail rather
  than disconnecting battery VIN. Follow the selected revision's bring-up plan.

## Check the selected revision

Use `make check BOARD=<name>` for ERC, refilled DRC/parity, copper guard and declared
fab rules; use `make validate BOARD=<name>` for declarative intent. Sensor has no
`checks.yml`: its design/BOM/layout/service tools supply specialized checks.
Read their runbook rather than treating a skipped validator as a pass.

Export a fresh netlist before connectivity assertions. Run affected host tests
and simulation cases, including relevant failure controls. Inspect schematic,
PCB and assembly views for the actual change. The custom copper guard supplements
DRC; it is not a proof of every net's complete physical connectivity.

For manufacturing, reconcile fitted/DNP/probe references, both assembly sides,
through-hole work, pin 1, CPL datum/rotation, drill/slot/mask/paste and selected
stackup/process. Preserve the exact reviewed package and its checksums. A generic
KiBot export is not automatically the reviewed Rooster supplier package.
