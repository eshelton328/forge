# First-power access and equipment handoff

September 8, 2026; native PCB source `090b207`. This is the ROO-010 access and
equipment handoff to ROO-011, not an executed test or a complete powered run sheet.
Use the existing Obsidian ROO-005 bench plan B01–B06 and ROO-011 acceptance criteria;
the detailed test program does not need to finish before PCB purchase.

## Equipment and external work

Erik has a multimeter and oscilloscope. Instrument/probe models and other equipment
remain unconfirmed. Plan to borrow or separately procure an adjustable,
current-limited DC source and insulated leads terminating in a correctly wired
two-position JST PH mating cable. It must support the nominal 4.5 V pack-substitute
test and the staged loads defined by ROO-011; its current range, startup behavior,
set limit and stop conditions must be documented before power is applied. A fuse
is not a substitute for a controlled source. This does not select or purchase
bench equipment, and its delivery is not a PCB fabrication gate.

A known USB **data** cable and a usable computer USB port are required for the
primary programming route. A second cable supports failure diagnosis. Magnification
for assembly inspection and suitable clips/probes must be arranged before testing.
Do not infer switch-node, sleep-current or inrush measurement capability merely
from owning an oscilloscope and multimeter; record their actual limits in ROO-011.

For two complete units of each device, account separately for two controls GH
cables, two front GH cables, four battery PH leads/holders, two compatible displays,
two speakers with PH leads, and two header-version LD2410C radar modules, less
verified existing inventory. None is automatically included in the PCBA BOM.
Initial rail/USB checks leave display, speaker and radar disconnected. The Cube
controls cable is needed for the normal power-enable route; the front cable is
needed for later front-button/RGB tests.

Exact harness requirements and signal order remain in
[main HARNESS.md](../../../boards/alec-main/HARNESS.md). The selected display is
the four-pin ER-OLEDM013-1W-I2C; the Beacon module variant is described in the
[radar procurement note](beacon-radar-procurement.md). Battery holder and speaker
procurement still need exact item/inventory confirmation. Firmware can develop
while these external items are being arranged.

## Physical connection and programming access

| Item | Main | Beacon |
| --- | --- | --- |
| Pack-substitute entry | J1 pin 1 VBAT, pin 2 GND | J1 pin 1 VBAT, pin 2 GND |
| Normal enable | Controls cable J5 ↔ controls J1; controls power switch ON | Rear SW1 ON |
| Primary programming | Native USB, separate target power, SW3 BOOT and SW2 RESET | Native USB, separate target power, rear SW3 BOOT and SW2 RESET |
| Alternative ROM UART | J7 exposed service pads; 3.3 V logic fixture required | No routed UART0 service pads; radar J3 is not the ROM UART |
| Initially disconnected loads | OLED and speaker; front board optional | LD2410C module |

The native power/header assignments are also recorded in the current source and
prior interface review. Main J7 native coordinates use KiCad's downward-positive
Y convention and are **not** the transformed enclosure coordinates in HARNESS.md:

| J7 pad | Net | Native X, Y (mm) |
| --- | --- | --- |
| 1 | GND | 125, 121 |
| 2 | Target 3v3 reference | 127, 121 |
| 3 | UART_TX | 125, 123 |
| 4 | UART_RX | 127, 123 |
| 5 | EN | 125, 125 |
| 6 | GPIO0 | 127, 125 |

Cross UART TX/RX at the adapter, share ground and use 3.3 V logic. J7.2 is a
voltage reference, not an external power input. The fixture must release EN and
GPIO0 rather than drive them high from an incompatible source. USB alone is not
the target power source. Verify PH polarity and GH pin-to-pin continuity on the
actual cable before attaching it; a connector's key does not establish wiring.
The main speaker is BTL: neither J3 speaker conductor is ground.

## Sequence after delivery

1. Identify board/revision and fitted/reworked parts. Inspect package alignment,
   soldering, holes and connector polarity; perform unpowered continuity/short
   checks against the run sheet. Keep the source output off during connection.
2. Follow B01 using a nominal 4.5 V current-limited pack substitute and the
   documented initial limit. Keep optional loads disconnected and verify the
   protected input, nominal 3.3 V rail and disabled switched rails. Stop for
   unexpected sustained current limiting, abnormal heating or out-of-range rails.
   Freeze numerical limits and accessible probe locations in the per-board run
   sheet before this step; no custom-board result is claimed here.
3. Use BOOT/RESET to enter the ROM loader with independent target power. Apply the
   [USB test sequence](stackup-review/README.md), including both cable orientations,
   cold enumeration and repeated flash/readback verification. Retained USB routes
   are a disclosed prototype test/rework risk, not certified 90 Ω routing.
4. Add peripheral diagnostics and external loads in stages under ROO-011/012.
   Measure startup, transient and low-battery boundaries after basic operation.
   Battery endurance, complete alarm behavior and wet/enclosure tests retain
   their existing later tickets.

No equipment, external part or PCB was purchased through this handoff. Availability
questions remain explicit; the feasible connections above do not certify a board
as safe to energize before its inspection and run-sheet limits are complete.
