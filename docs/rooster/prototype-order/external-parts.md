# External parts for two Cube + Beacon sets

September 8, 2026. These are outside the four PCBA BOMs and the $791.07 draft
board/assembly comparison. Quantities below are the complete-system requirement
**before subtracting verified existing inventory**, not a purchase authorization.
Ownership is unconfirmed; no external item has been purchased by the agent.

## Reuse the recorded candidates

| Item | Gross quantity | Exact recorded choice or required interface | Remaining procurement work |
| --- | ---: | --- | --- |
| Radar module | 2 | Hi-Link LD2410C, header version mating with Beacon J3 SSW-105-01-F-S | Confirm existing modules or quote the exact header version; inspect shipped orientation. J3's PCBA BOM buys the socket only. |
| OLED | 2 | EastRising ER-OLEDM013-1W-I2C, four-pin, SH1106 | Confirm inventory or quote this variant; seven-pin and bare-glass variants are not substitutes. |
| Speaker | 2 | Visaton FRS 5 X, **8 Ω, article 2235**, existing enclosure candidate | Confirm inventory and exact offer; fit/acoustic testing follows delivery. This is the solder-lug version. |
| Three-AA holder | 4 | MPD **BH3AAW**, existing Cube and Beacon enclosure candidate | Confirm inventory and exact offer; wire leads require the correct PH mating connection. Test contact/load behavior on delivered holders. |
| AA cells | 12 across four holders | Chemistry/brand not frozen | Agree actual cells for battery characterization; a controlled source is used for first power. |
| Cube controls cable | 2 | Main J5 ↔ controls J1; GHR-07V-S at each end, SSHL-002T-P0.2 contacts, AWG28, ≤200 mm, pin 1 ↔ pin 1 | Quote or assemble a verified harness. Two cables require four housings and 28 contacts before spares. Needed for the normal main-board enable route. |
| Cube front cable | 2 | Main J6 ↔ front J1; GHR-06V-S at each end, same contact/wire rules | Two cables require four housings and 24 contacts before spares; verify all six nets. |
| OLED cable | 2 | Four-conductor female-to-female 2.54 mm connection; both main J4 and selected display have male headers | Choose exact cable/contacts accepting the header posts; verify GND, switched supply, SCL, SDA continuity. |
| Battery PH connection | 4 | Two-position PHR-2 mate to each main/Beacon J1; pin 1 VBAT, pin 2 GND | Select correctly terminated leads or contacts compatible with actual holder wire. Do not assume the holder comes with a PH plug. |
| Speaker PH connection | 2 | PHR-2 mate to main J3; pin 1 speaker −, pin 2 speaker +, other end to solder lugs | Select/assemble paired conductors with appropriate termination and strain relief; both BTL leads are active. |

PH requirements above total six two-position mating housings and twelve signal
contacts if building those connections from loose pieces, before spares and any
separate bench-supply lead. Preassembled cables replace, rather than add to, the
equivalent loose housing/contact counts. Exact PH contact/wire selection remains
part of the harness quote; it has not been silently inferred from the GH contact.

The speaker and holder identities come from the existing
[Cube parts register](../../../enclosures/alec/parts/parts-register.json),
[mechanical inventory](../../../enclosures/alec/parts/mechanical-parts.csv) and
[Beacon enclosure](../../../enclosures/alec-sensor/README.md). They were already
recommended candidates, not newly approved parts. Mechanical allocations and
manufacturer models do not prove that physical parts are owned or fit-qualified.

## Manufacturer verification

The current Visaton listing confirms **FRS 5 X / 2235**, nominal 8 Ω, rated 5 W
and solder-lug connections. Preserve that identity when quoting: the related
FRS 5 XTS is article 2239 with different terminals. The supplier's advertised
speaker power rating does not establish our amplifier's delivered sound level
or enclosure response. [Visaton 2235 product data](https://www.visaton.de/de/produkte/chassis/breitband-systeme/frs-5-x-8-ohm),
[Visaton range and terminal variants](https://www.visaton.de/en/products/industry/fullrange-systems).

MPD's current BH3AAW listing confirms a three-AA nylon holder with wire leads.
It does not identify a JST plug as supplied. Its bulk price breaks are not a
four-holder delivered quote, and distributor counters do not reserve stock.
[MPD BH3AAW](https://batteryholders.com/part.php?original=AA&override=AA&pn=BH3AAW).

Retain the existing [radar variant checks](beacon-radar-procurement.md),
[display interface](../../../enclosures/alec/PCB-INTERFACE.md) and
[GH/BTL harness contract](../../../boards/alec-main/HARNESS.md). No PCB footprint
change is indicated merely to replace missing external-item inventory records.

## Ordering sequence

The PCBA order must have complete fitted-part intake and a feasible first-power
route. Completed enclosures, delivered external peripherals, full application
firmware and endurance tests are later work. The controlled source and USB cable
can support initial rail/programming tests while the display, speaker and radar
are disconnected; the Cube still needs its controls enable connection.

After existing inventory is confirmed, quote the net external quantities and
bench equipment separately, with shipping/tax and any assembly work explicit.
These items do not belong in JLCPCB's fitted-component placement file. Obtain
Erik's permission for the concrete external purchase as well as the PCB purchase;
this inventory does not authorize either. See the
[first-power handoff](first-power-access.md) for equipment and test preparation.
