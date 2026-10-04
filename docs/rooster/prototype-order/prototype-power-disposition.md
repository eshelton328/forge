# Prototype power scope and protection disposition

September 8, 2026. Native source `090b207`; candidate `090b207-r1`.

**Retain the current power circuitry for supervised, dry bench evaluation using
an adjustable current-limited supply at the battery input.** This is a bounded
engineering disposition for prototype order preparation. It does not establish
consumer battery safety, unattended operation or achieved battery life. Other
order gates, especially RTC supply and placement, remain open.

## Source facts

The [source-bound placement/net reference](placement-review/090b207-r1/native-placement-reference.json)
was reconciled to all four unchanged native PCB hashes on September 8.

| Device | Actual input path | Consequence for prototype testing |
| --- | --- | --- |
| Cube | J1.1 VBAT → Q1 AO3401A → PFET → U1/U2 VIN; no series input fuse. Controls SW4 switches the U1 enable signal. | The controls OFF position does not disconnect the battery from the regulator inputs. Source current limiting and physical source disconnection are required for this initial bench scope. |
| Beacon | J1.1 VBAT → F1 046701.5NRHF → SW1 1101M2S3CQE2 → Q1 → PFET → U1/U2 VIN. | Retain the fuse and rated switch. F1 does not protect the holder or wire before its input, and is not an electronic current clamp. |

Both J1.2 pins are GND. The prior [component review](power-component-review.md)
supports the chosen capacitor banks and inductors within its stated load cases;
it does not establish simultaneous full-system battery loading. The
[fuse review](assembly-drawing-review.md) gives a 1.125 A continuous allowance at
25°C and 0.9 A at its 70°C example, with startup/thermal verification still due.

## Initial evaluation envelope

Use a nominal **4.5 V pack substitute**, output off while connecting, verified
PH polarity and the normal controls/Beacon enable route. Leave the display,
speaker and radar disconnected for initial rail and USB checks. USB provides
data, not target power. Keep accessible BOOT/RESET controls; main additionally
has the J7 service pads. The [first-power handoff](first-power-access.md) defines
these connections and the equipment still to arrange.

ROO-011 must set the actual source current limits, allowed rail ranges, probe
points, step durations and stop conditions in a per-board run sheet before
power is applied. Do not improvise a higher current limit to force a failing
board to start. Completed run sheets/diagnostic code and equipment delivery are
before-power requirements, not reasons to wait for physical test results before
ordering the PCBs needed for those tests.

Keep the existing three-AA architecture and the previous **≤5.4 V input review
ceiling**. This is not a new cell-chemistry selection. Converter cold start needs
at least 3 V at protected VIN; lower running voltage is not a restart guarantee.
The existing 8-ohm speaker proposal and 1 W audio calculation remain later load
cases to measure, not approved simultaneous battery-load limits.

## Before battery-powered or unattended use

ROO-013 owns the protection/harness decision and ROO-011/012 its measurement:

- Establish exact cell, holder, wire, connector and load ratings, including
  low-battery current and faults upstream of Beacon F1.
- Specify and verify suitable source-end protection for battery harness testing,
  including Cube's unfused input; confirm coordination with wiring and load.
  An exact protective device/rating has not been selected in this disposition.
- Measure startup, sustained and transient current, rail behavior and heating
  before progressing to real-cell operation and sustained audio/radar loads.
- Record whether findings require harness changes or a PCB revision. Enclosure,
  wet-use, unattended operation and endurance acceptance follow their later
  tickets. Cube's one-month aspiration remains a design target; Beacon's target
  remains open.

This closes the question of what power setup the present dry engineering-board
purchase is intended to support. It does not close the separate battery-powered
product protection review, authorize a purchase, or report any executed test.
