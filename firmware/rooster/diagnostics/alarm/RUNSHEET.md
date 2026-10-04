# Cube first diagnostic session — NOT RUN

This adapts ROO-004 **B01–B04 and the input-only part of B10** to the read-only
Cube image. Keep the original [bench plan and limits](../../../../docs/rooster/roo-004/BENCH.md),
[prototype power disposition](../../../../docs/rooster/prototype-order/prototype-power-disposition.md)
and [first-power access](../../../../docs/rooster/prototype-order/first-power-access.md)
alongside this procedure. B05–B09 and B11–B15 remain unrun; reading RTC INT/PG does
not complete their peripheral/analog cases.

## Session identity and readiness

Copy [bench-template.csv](bench-template.csv) into a dated per-unit evidence
folder outside immutable historical reports. Record unit/lot and three PCB revisions,
release/native commit, fitted substitutions/rework, firmware manifest/application/
ELF hashes; supply/DMM/scope/probe models, calibration, ranges and uncertainty;
cable/module identities and continuity results; ambient temperature, actual
conditions/readings, raw logs/waveforms/photos, stops and retest history.

Erik reported a DMM and oscilloscope. Current-limited source, leads, instrument
capabilities and programmer/cable availability remain unconfirmed. Resolve them
before power. Settings below reproduce the existing B01/B02 bench proposal;
verify applicability to actual fitted parts/wiring. They do not approve battery
use or full-load operation.

## 1. Unpowered inspection — B01

Disconnect supply, batteries and USB/UART. Inspect assembly, MPN/orientation,
shorts and solder faults. Verify isolated cables pin-to-pin with no shorts;
PH keying alone is insufficient. Main J1.1 is positive VBAT; J1.2 is GND.
Controls J5↔J1 enables the normal 3.3 V supply; OFF leaves regulator VIN energized.
Check J4 header/finished-hole fit and polarity against its recorded correction
before fitting a display. Leave OLED/speaker disconnected and front board optional.

Record continuity/resistance with capacitors considered. Investigate unexplained
shorts before proceeding; firmware cannot screen them.

## 2. Controlled first power — B02/B03

Use a regulated **4.5 V** pack substitute at J1, initially off. Set the existing
**50 mA initial limit**, controls OFF/unplugged, optional loads disconnected.
This is the short-screen setting, not the running-current allowance. Apply power;
record J1/TP2 and current. Persistent current limiting, abnormal heating or
polarity/rail mismatch means power off and investigate.

Hold RESET low, connect the verified controls cable and enable its switch as in
B02. Measure TP3/U3.2 against GND and record uncertainty. The MCU operating guard
is **3.0–3.6 V**, including transients; tighter regulator-accuracy acceptance
still depends on selected parts and L04. Do not increase limits to overcome
unexplained current draw.

After inspection/rail checks pass, B02 proposes **0.75 A at 4.5 V for the no-audio
boot trial**, only with suitably rated leads/connectors. Record startup demand
and droop; a trip is inconclusive until investigated. Keep optional loads off.
Check TP4/TP8 and default shutdown. Firmware defaults apply only after execution;
separately record pre-execution/reset transients. No full-load ceiling is selected.

## 3. Program and recover — B04

Keep separate target power. Enter ROM loader with BOOT/RESET. Verify artifacts,
identify the actual port and follow the exact [flash instructions](README.md).
Retain upload/verification logs. Reset and request `info`; record chip ID, source,
contract and ELF identity alongside physical unit/PCB identity. Stop if
`startup_ok` is false or the image/board differs from the intended session.

If USB fails, record symptoms and use documented J7 3.3 V UART recovery. J7.2 is
reference, not power. Never ground either BTL speaker output with a scope clip.
USB enumeration, both cable orientations, repeat upload and recovery remain
physical B04 checks to execute.

## 4. Digital observations — input slice of B03/B10

After startup settles, request `status` and record all eight raw/active inputs.
Investigate unexpected PG3V3 against measured TP3. With amplifier enable off,
record PG5V and TP4; PG is not a voltmeter. Via UART, compare USB detection with
the data cable attached/removed. RTC INT says nothing about clock validity.

With verified controls/front wiring, press/release VOL−, MODE, VOL+ and battery
button individually. Check physical labels against reported inputs; each settled
press/release should add one transition and return inactive. Repeat ten times
per button as B10's input subset, recording missing/double edges. LEDs stay off.
Disconnect/reconnect USB and use UART status to check sampling continuity;
record resets/enumeration faults separately. Host substitutes do not count.

## Disposition

Use PASS/FAIL only against explicit rules and measured uncertainty from the bench
plan. Use BLOCKED for absent equipment/limits, INCONCLUSIVE for ambiguous current
limiting, CHARACTERIZED without frozen performance limits, and NOT RUN when
unexecuted. This session cannot establish battery runtime, audio/display/RTC
functionality, radio/presence, enclosure fit or finished alarm behavior.
