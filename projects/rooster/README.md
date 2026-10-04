# Rooster engineering map

Rooster is the alarm-clock product in Forge. The current hardware uses ALEC
names. This index connects the sources without renaming them or duplicating
product requirements. The **2026-10-04 integration** combines main `a56d890`,
the Browns preservation package, Cube acceptance review and ordering branch.
Use [project.json](project.json) for repository-relative paths and source refs;
the [integration record](../../docs/rooster/integration/2026-10-04/README.md)
records provenance, checks and the handoff. This is a local integration branch,
not a manufacturing release.

## Names

| Name | Meaning |
| --- | --- |
| Forge / historical The Forge | Electronics repository and shared tooling |
| Rooster / ROO | Product and its Obsidian task IDs |
| Cube / alarm | Bedside device: main, controls and front PCBs |
| Beacon / Sensor | Remote presence device |
| ALEC / `alec-*` | Existing board/enclosure family and stable source paths |
| `bedroom-alarm-*` | Historical Cube source names |

## Sources in this checkout

| Area | Read first |
| --- | --- |
| Cube electronics | [Main](../../boards/alec-main/README.md), [controls](../../boards/alec-controls/README.md), [front](../../boards/alec-front/README.md), [harness and service contract](../../boards/alec-main/HARNESS.md) |
| Sensor electronics | [Sensor](../../boards/alec-sensor/README.md), [power and behavior](../../boards/alec-sensor/OPERATION.md) |
| Cube mechanics | [v4.2 assembly](../../enclosures/alec/pcb-revision/README.md); [v4.1 retained input](../../enclosures/alec/README.md) |
| Sensor mechanics | [S1.1 enclosure](../../enclosures/alec-sensor/README.md) |
| Design generation | [Cube runbook](../../scripts/alarm/README.md), [Sensor runbook](../../boards/alec-sensor/tools/README.md) |
| Validation | [Root commands](../../README.md), [tests](../../tests/), [simulation](../../sim/README.md) |

`boards/esp32s3-devkit-5v` remains a generator/reference input. The development
boards and breakout are supporting projects, not additional components in a
finished Rooster set.

## Integrated reference and ordering packages

| Branch and observed commit | Deliverable |
| --- | --- |
| `codex/roo-002-firmware-baseline` at `59e0e42` | [Preserved sketches, dependencies and builds](../../docs/rooster/baselines/2026-09-07/README.md), [Browns selection](../../docs/rooster/baselines/2026-09-07/selected-reference.json), [PCB port matrix](../../docs/rooster/baselines/2026-09-07/COMPATIBILITY.md) |
| `codex/roo-004-cube-acceptance` at `f0b8dca` | [Cube acceptance review](../../docs/rooster/roo-004/README.md), [bench plan](../../docs/rooster/roo-004/BENCH.md) |
| `codex/rooster-prototype-orders` at `1e8ee95` | [Cube-first plan](../../docs/rooster/prototype-order/cube-first-pass-2026-09-08.md), [sourcing and native transitions](../../docs/rooster/prototype-order/README.md), [first-power access](../../docs/rooster/prototype-order/first-power-access.md) |

The latest saved purchasing direction is **Cube first**, from September 8:
main, controls and front, five fabricated/two assembled per design. It remains
an incomplete proposal. Sensor manufacture is deferred. Read the
[supplier-quote record](../../docs/rooster/prototype-order/cube-supplier-quotes-2026-09-08/README.md)
before older four-board summaries. Integration did not refresh supplier stock,
replies or prices. Frozen packages remain at their existing paths; see
[release conventions](../../releases/rooster/README.md).

The Browns sketches are historical references, not firmware validated on the
ALEC PCBs. [Firmware paths](../../firmware/rooster/README.md) now exist as
documentation: separate alarm, sensor, shared and diagnostic locations. There
is no implemented application or diagnostic target yet. The two Browns programs
must be built separately; their old pin definitions do not override the PCB.

## Immediate order blockers

- Reconcile the RFQ's QA RTC selection with the native QC part and actual supply.
- Close main U3 placement datum/U6 amplifier orientation and the remaining
  controls/front, connector and polarity reviews using the
  [placement sheet](../../docs/rooster/prototype-order/placement-review/README.md).
- Confirm fill/cap process, stackup, assembly scope and exact external parts;
  [order readiness](../../docs/rooster/prototype-order/order-readiness-2026-09-08.md)
  and [external inventory](../../docs/rooster/prototype-order/external-parts.md)
  retain the details.
- Obtain a complete Cube quote and Erik's approval for its exact scope and total.

The native sources include the ordering metadata/capacitor selections and main
J4 1.10 mm finished-hole correction. Historical acceptance, simulation, gallery
and CAD files retain their producing revisions; do not infer new physical
validation from their presence in this checkout.

## Product decisions and next evidence

In Obsidian, open `Projects/Rooster/Rooster.md`, then the relevant task and linked
decision/specification. Obsidian currently owns all 17 ROO task statuses. Current
summary text and historical appended notes sometimes conflict; follow the latest
explicit decision and record the reconciliation.

The personal-use product comes first. Cube's minimum monthly battery target is
a requirement; actual runtime, new-board bring-up, assembled fit, radio/presence
behavior and everyday use still need physical evidence in the inspected records.

The next implementation is ROO-011 Cube diagnostics at
[`firmware/rooster/diagnostics/alarm`](../../firmware/rooster/diagnostics/alarm/README.md),
using the current harness/power contracts and bench plan. Close the remaining
order/first-power inputs alongside that work, then measure before selecting a
cost-reduction revision. The [audit](../../docs/audits/2026-10-04-forge-rooster.md)
is the preserved pre-integration snapshot, not the current task-status record.
