# Firmware work

Read [Rooster's firmware map](rooster/README.md), the applicable Obsidian ROO
task and the selected native board contract before implementing a target.

- Keep application, diagnostic and shared protocol code in their declared paths.
- Preserve the Browns archive. Adapt its behavior to the PCB; do not flash old
  breadboard pin assignments onto the new boards unchanged.
- Derive startup defaults, rail/display isolation, audio mute and input polarity
  from the current schematic and harness/power contract. USB is data/service;
  establish the documented power and recovery route before bench flashing.
- Pick a reproducible, pinned build setup when the first target is implemented.
  Capture target/toolchain and binary identity. Do not invent build commands or
  treat documentation placeholders as working firmware.
- Test meaningful protocol, timing and state-machine behavior on the host where
  feasible; keep physical rail, wake, audio and power measurements separate.
