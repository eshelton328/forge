# JLCPCB prototype assembly preflight

September 7, 2026. Quote target: five fabricated and two assembled copies of each design. The main-board candidate has been uploaded for quotation; sign-in is required to reach assembly pricing. No complete quote or order exists. [Quote progress](quote-progress.md).

JLCPCB publishes a five-board fabrication minimum and assembly quantities starting at two. [Fabrication FAQ](https://jlcpcb.com/resources/pcb-prototyping), [PCBA capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities).

Its capabilities distinguish Economic single-side placement from Standard single/double-side placement, including through-hole parts. Standard lists 70 × 70 mm minimum processing size and required rails/fiducials. [PCBA capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities). Small-board rail handling must be confirmed in the quotation; the supplier describes adding rails to meet processing dimensions. [After-sales/process-rail explanation](https://jlcpcb.com/help/article/common-pcba-after-sales-issues-and-faq). This last page was available as a search excerpt; a later full-page request returned HTTP 429. It is context, not an approved tooling plan.

## Native board inventory and service implications

The read-only KiCad footprint inventory in [assembly-audit.json](assembly-audit.json) matches all 207 fitted review BOM references exactly. One additional main-board row is DNP. No board bytes changed. KiCad emitted wx/image-handler diagnostics but exited zero; this was a footprint-side/type inventory, not a placement-rotation, pin-map or electrical validation.

| Board | Native fitted placement | Initial service inference |
| --- | --- | --- |
| alec-main | 110 front SMD, front THT J4; 64 × 56 mm | Economic is a candidate for single-side placement, subject to actual parts/geometry/service qualification |
| alec-controls | Back SMD J1; front THT SW1–SW4; 27 × 34 mm | Plan Standard for complete factory assembly across both sides; verify manual/through-hole service details |
| alec-front | Front SMD D1/SW1; back SMD J1; 24 × 10 mm | Complete factory assembly uses both sides; plan Standard |
| alec-sensor | 84 front SMD, front THT J3, back THT SW1, back SMD SW2/SW3; 64 × 56 mm | Complete factory assembly uses both sides; plan Standard |

Service choices above are inferences from the actual placement inventory and published capabilities, not accepted supplier quotes. The Sensor front-SMD count is 84; the remaining four fitted references bring its total to 88.

## Remaining preflight work

- Confirm the complete fitted-part list for both sides, through-hole service and exact part eligibility. JLCPCB’s FAQ describes supported through-hole assembly through its assembly-parts library. [Assembly FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs).
- Account for detachable rails/panelization and final board outline/clearance on the small Standard boards. Do not enlarge the functional PCB or move connectors merely to meet a processing-size requirement.
- Ensure BOM/CPL includes the intended service parts. The current repository exporter uses `only_smd: true`, which omits THT locations; it cannot by itself describe all the requested factory assembly.
- Confirm actual stock, component attrition/minimums, fabrication versus assembly counts, services and total cost for the selected order options. The published fee table is not a quote for these boards.
- Establish the first-power source and USB/recovery procedure using Erik’s confirmed multimeter and oscilloscope, with remaining equipment/probe capabilities recorded explicitly.
