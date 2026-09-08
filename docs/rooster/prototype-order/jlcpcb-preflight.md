# JLCPCB prototype assembly preflight

September 7, 2026. Quote target: five fabricated and two assembled copies of each design. The main-board candidate, BOM and all 111 component positions are uploaded in a signed-in quote. Its RTC is the remaining BOM shortage. The main draft now uses Standard assembly because the selected ESP32 module is Standard-only in JLCPCB's matcher. No complete quote or order exists. [Quote progress](quote-progress.md).

JLCPCB publishes a five-board fabrication minimum and assembly quantities starting at two. [Fabrication FAQ](https://jlcpcb.com/resources/pcb-prototyping), [PCBA capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities).

Its capabilities distinguish Economic single-side placement from Standard single/double-side placement, including through-hole parts. Standard lists 70 × 70 mm minimum processing size and required rails/fiducials. [PCBA capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities). Small-board rail handling must be confirmed in the quotation; the supplier describes adding rails to meet processing dimensions. [After-sales/process-rail explanation](https://jlcpcb.com/help/article/common-pcba-after-sales-issues-and-faq). This last page was available as a search excerpt; a later full-page request returned HTTP 429. It is context, not an approved tooling plan.

## Native board inventory and service implications

The read-only KiCad footprint inventory in [assembly-audit.json](assembly-audit.json) matches all 207 fitted review BOM references exactly. One additional main-board row is DNP. No board bytes changed. KiCad emitted wx/image-handler diagnostics but exited zero; this was a footprint-side/type inventory, not a placement-rotation, pin-map or electrical validation.

| Board | Native fitted placement | Service basis |
| --- | --- | --- |
| alec-main | 110 front SMD, front THT J4; 64 × 56 mm | Standard required by actual JLCPCB eligibility for ESP32-S3-WROOM-1-N16 / C2913199; saved draft is top-side assembly, quantity 2 |
| alec-controls | Back SMD J1; front THT SW1–SW4; 27 × 34 mm | Plan Standard for complete factory assembly across both sides; verify manual/through-hole service details |
| alec-front | Front SMD D1/SW1; back SMD J1; 24 × 10 mm | Complete factory assembly uses both sides; plan Standard |
| alec-sensor | 84 front SMD, front THT J3, back THT SW1, back SMD SW2/SW3; 64 × 56 mm | Complete factory assembly uses both sides; plan Standard |

The main-board service restriction is an actual supplier-matcher result, superseding the earlier Economic candidate. The other three choices remain inferences from the placement inventory and published capabilities. None is an accepted manufacturing release. The Sensor front-SMD count is 84; the remaining four fitted references bring its total to 88.

After switching the main quote to Standard, JLCPCB proposed a **74 × 70 mm processing size** with its own rails/fiducials around the native 64 × 56 mm board. The source outline has not changed. Five fabricated / two assembled remained selected. Factory depaneling was added to the draft, and production-file and placement review were confirmed with automatic approval disabled. Actual rail geometry, connector/antenna clearance, finished-board count and detachment still need review.

## Remaining preflight work

- Confirm the complete fitted-part list for both sides, through-hole service and exact part eligibility. JLCPCB’s FAQ describes supported through-hole assembly through its assembly-parts library. [Assembly FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs).
- Account for detachable rails/panelization and final board outline/clearance on the small Standard boards. Do not enlarge the functional PCB or move connectors merely to meet a processing-size requirement.
- The four dedicated candidate BOM/CPL pairs include both faces and THT locations, covering 111/5/3/88 fitted references. Continue using those reconciled files: the shared repository exporter uses `only_smd: true` and omits THT locations. Supplier rotations and placement review remain open.
- Confirm actual stock, component attrition/minimums, fabrication versus assembly counts, services and total cost for the selected order options. The published fee table is not a quote for these boards.
- Establish the first-power source and USB/recovery procedure using Erik’s confirmed multimeter and oscilloscope, with remaining equipment/probe capabilities recorded explicitly.
