# Rooster firmware

Stable paths for ROO-011 diagnostics and ROO-015 applications. The first
[Cube diagnostic image](diagnostics/alarm/README.md) now has a pinned build,
read-only digital commands and a first-power run sheet. It is compiled and
host-tested; custom-board operation remains unverified. Application, shared
protocol and Sensor diagnostic paths remain documentation placeholders.

| Path | Intended responsibility |
| --- | --- |
| [alarm](alarm/README.md) | Cube application, UI and alarm behavior |
| [sensor](sensor/README.md) | Beacon presence application |
| [shared](shared/README.md) | Explicit protocol types and shared behavior |
| [diagnostics/alarm](diagnostics/alarm/README.md) | Initial Cube startup/input diagnostics; physical tests pending |
| [diagnostics/sensor](diagnostics/sensor/README.md) | Beacon programming and bench firmware |

Start from the [product map](../../projects/rooster/README.md), native board
contracts and relevant Obsidian task. The [Browns reference](../../docs/rooster/baselines/2026-09-07/README.md)
is preserved with its dependencies and hashes. Keep its archive unchanged and
port behavior deliberately; the historical pins are not the current PCB map.

Record source revision, toolchain, target, binary hash and upload settings for
each new build. Distinguish host tests, compile success, flashing and observed
hardware behavior. Attach physical observations to identified boards and parts.
