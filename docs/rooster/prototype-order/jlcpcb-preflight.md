# JLCPCB prototype assembly preflight

September 7, 2026. Quote target: five fabricated and two assembled copies of each design. All four Gerber/BOM/CPL sets are uploaded with actual Standard-service price previews. Controls/front have all fitted parts matched. Main and Beacon retain their full required BOM/CPLs but remain short of RTCs; their temporary incomplete price previews exclude U5 and are labeled accordingly. No complete four-board landed quote or order exists. [Quote progress](quote-progress.md).

JLCPCB publishes a five-board fabrication minimum and assembly quantities starting at two. [Fabrication FAQ](https://jlcpcb.com/resources/pcb-prototyping), [PCBA capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities).

Its capabilities distinguish Economic single-side placement from Standard single/double-side placement, including through-hole parts. Standard lists 70 × 70 mm minimum processing size and required rails/fiducials. [PCBA capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities). Small-board rail handling must be confirmed in the quotation; the supplier describes adding rails to meet processing dimensions. [After-sales/process-rail explanation](https://jlcpcb.com/help/article/common-pcba-after-sales-issues-and-faq). This last page was available as a search excerpt; a later full-page request returned HTTP 429. It is context, not an approved tooling plan.

## Native board inventory and service implications

The read-only KiCad footprint inventory in [assembly-audit.json](assembly-audit.json) matches all 207 fitted review BOM references exactly. One additional main-board row is DNP. No board bytes changed. KiCad emitted wx/image-handler diagnostics but exited zero; this was a footprint-side/type inventory, not a placement-rotation, pin-map or electrical validation.

| Board | Native fitted placement | Service basis |
| --- | --- | --- |
| alec-main | 110 front SMD, front THT J4; 64 × 56 mm | Standard required by actual JLCPCB eligibility for ESP32-S3-WROOM-1-N16 / C2913199; saved draft is top-side assembly, quantity 2 |
| alec-controls | Back SMD J1; front THT SW1–SW4; 27 × 34 mm | Actual Standard / Both Sides / qty 2 quote includes all five fitted parts, hand soldering and fixture fees; processing proposal 71 × 70 mm |
| alec-front | Front SMD D1/SW1; back SMD J1; 24 × 10 mm | Actual Standard / Both Sides / qty 2 quote includes all three fitted parts; processing proposal 70 × 70 mm |
| alec-sensor | 84 front SMD, front THT J3, back THT SW1, back SMD SW2/SW3; 64 × 56 mm | Actual Standard / Both Sides / qty 2 draft, 74 × 70 mm processing proposal, hand-soldering and fixture charges; U5 RTC is the only shortage |

The main-board service restriction is an actual supplier-matcher result, superseding the earlier Economic candidate. All four drafts have actual assembly-price breakdowns; main/Beacon prices currently exclude the unavailable RTC. None is an accepted manufacturing release. The Sensor front-SMD count is 84; the remaining four fitted references bring its total to 88.

After switching the main quote to Standard, JLCPCB proposed a **74 × 70 mm processing size** with its own rails/fiducials around the native 64 × 56 mm board. The source outline has not changed. Five fabricated / two assembled remained selected. Factory depaneling was added to the draft, and production-file and placement review were confirmed with automatic approval disabled. Actual rail geometry, connector/antenna clearance, finished-board count and detachment still need review.

## Remaining preflight work

Main's [J4 finished-hole correction](header-fit/README.md) is checked in native
source: four 1.10 mm plated holes, with existing pads/placement preserved. Its
previous uploaded Gerber archive is superseded. The new
[090b207-r1 fabrication candidate](fabrication-candidates/README.md) passes the
independent native/CAM checks, with the same supplier placement corrections
rebound to its hashes. Source-bound via attachments now match this candidate, including the enlarged
open J4 holes. Replace/reprice the supplier draft before ordering.

The [via-process specification](via-process/README.md) now calls for epoxy fill
and copper cap on main/Beacon, preserving all component holes. Their draft
Plugged setting is superseded and needs updating/repricing; controls/front retain
tenting. The separate calculator indicates $20.41 extra fabrication per large
board batch. This establishes the process requirement and an indicative cost,
not supplier acceptance of the final CAM files.

The [mask review](mask-review/README.md) found no violations at 0.09 mm
mask-to-copper clearance in isolated copies of all four boards. Its independent
negative control verifies that rule is active. The separate actual-Gerber check
now establishes at least 0.15 mm between distinct mask openings on all eight
layers, above the 0.10 mm requirement. Retain uniform native 1:1 openings for the
prototype, including U6, with supplier mask changes subject to manual production
review. This does not claim NSMD geometry or whole-board fabrication acceptance.

- Available fitted parts are matched on all four designs, including both faces and through-hole parts. Resolve RTC procurement/assembly intake and restore U5 in both incomplete supplier previews, then recheck final eligibility. JLCPCB’s FAQ describes supported through-hole assembly through its assembly-parts library. [Assembly FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs).
- Account for detachable rails/panelization and final board outline/clearance on the small Standard boards. Do not enlarge the functional PCB or move connectors merely to meet a processing-size requirement.
- The dedicated BOM/CPL files include both faces and THT locations, covering 111/5/3/88 fitted references. Use the corrected [controls r2 and headers r2 CPLs](supplier-placement-candidates/README.md), which correct the button/header centers and main J4 rotation. The shared repository exporter uses `only_smd: true` and omits THT locations. U3 model alignment, other origins, rotations and final placement review remain open.
- Confirm actual stock, component attrition/minimums, fabrication versus assembly counts, services and total cost for the selected order options. The published fee table is not a quote for these boards.
- Establish the first-power source and USB/recovery procedure using Erik’s confirmed multimeter and oscilloscope, with remaining equipment/probe capabilities recorded explicitly.

## Purchase versus production approval

Before requesting purchase approval, resolve actual design and testability issues,
identify exact fitted parts and quantities, define mask/via/stackup and stencil
requirements, and present the complete priced scope. The amplifier's copper-pad
disposition and 17-pin map are recorded in the [drawing review](assembly-drawing-review.md).
Its supplier preview orientation still needs reconciliation.

JLCPCB prepares its actual SMT/stencil production data after an order. Review
those files, final placements and rail geometry through the manual confirmation
steps before production; automatic confirmation stays disabled. The finished
supplier stencil is not a pre-purchase prerequisite. [Supplier stencil workflow](https://jlcpcb.com/help/article/smt-stencil-data-prepared-for-smt-orders).

Erik's explicit permission is required before any PCB order, paid parts
procurement or checkout/payment submission. Draft quotes do not grant it.
