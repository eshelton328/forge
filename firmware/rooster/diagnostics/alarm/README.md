# Cube diagnostics — next implementation

ROO-011 owns this target. This is a reserved path; no firmware or build exists.

Use the [current main-board contract](../../../../boards/alec-main/HARNESS.md),
[Browns port matrix](../../../../docs/rooster/baselines/2026-09-07/COMPATIBILITY.md),
[Cube bench plan](../../../../docs/rooster/roo-004/BENCH.md) and
[first-power access plan](../../../../docs/rooster/prototype-order/first-power-access.md).
Reconcile the bench review's original revision with the integrated native board
and purchasing/header transitions before assigning exact part limits.

The first slice should establish reproducible builds, serial identification and
recovery, safe output defaults and input inspection. Then add explicit tests for
rail/PG monitoring, RTC/alarm wake, switched display, audio, buttons and RGB.
Bind each physical result to the board revision, firmware hash, instruments and
conditions. See [the firmware map](../../README.md) for shared conventions.
