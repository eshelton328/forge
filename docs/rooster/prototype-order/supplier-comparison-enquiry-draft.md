# Rooster prototype comparison request - UNSENT

**Local draft only. No supplier contact, purchase, reservation or production authorization.**

Please quote fabrication and assembly of four prototype PCB designs for an alarm system, with delivery to Austin, Texas, USA 78704. The baseline is five fabricated and two fully assembled finished boards per design, delivering eight assembled boards and twelve spare bare boards in one shipment. If two assemblies per design are unavailable, identify your minimum and price it separately.

| Board | Layers | Finished dimensions | Fitted references per assembly |
| --- | ---: | --- | ---: |
| alec-main | 4 | 64 x 56 mm | 111 |
| alec-controls | 2 | 27 x 34 mm | 5 |
| alec-front | 2 | 24 x 10 mm | 3 |
| alec-sensor | 4 | 64 x 56 mm | 88 |

The build includes both-side SMT and through-hole work. Main R11 is DNP; all other fitted references in the supplied manufacturing BOM are required. Please source the exact manufacturer part numbers, identify procurement quantities/attrition and any uncertain availability, and request approval before substituting any component. In particular, include four fitted RV-3028-C7-32.768kHz-1ppm-TA-QC RTCs plus your attrition requirement. A QA-grade sourcing option may be quoted separately for review; it is not an approved substitution.

For main and sensor, quote the supplied four-layer, nominal 1.6 mm, 1 oz outer/inner copper, ENIG and epoxy-fill/copper-cap requirements. Propose the actual stackup and dielectric thicknesses; the current baseline uses JLC041611-7628/TG155. Preserve the finished outline, copper, component-hole sizes and mask intent. Do not replace fill/cap with solder-mask plugging. Use the source-bound fill maps and confirm any deviations. Quote the two-layer boards to their supplied specifications. Please identify rails/panels, fiducials, depaneling method and finished-board quantity explicitly.

Please identify your workmanship class/revision, bare-board electrical tests, assembly optical/manual inspection, hidden-joint X-ray coverage and report/image availability. Provide a manual placement/CAM review path before production, particularly for ESP32 modules, main amplifier, keyed connectors and both-side components. Default to unprogrammed boards with workmanship inspection; quote powered/functional testing separately, subject to an agreed procedure and fixture/firmware scope.

Separate all costs: fabrication/options, component procurement, setup/engineering, stencils, feeders, fixtures, machine/manual/through-hole assembly, depaneling, inspection, packaging, freight, duties/import-clearance fees, sales tax and other charges. State quote validity, any payment-processing surcharge, excess-parts ownership/return and the approval process for additional charges.

Identify fabrication and assembly countries, dispatch location, component-ready date, production milestones, carrier/service and estimated arrival at 78704. Quote a duty-paid option where available and state precisely which charges it covers. Provide warranty/claim periods, remake or repair terms and responsibility for return freight.

Optionally quote compatible family-panel arrangements preserving finished boards and exact quantities, and a five-assembled-set alternative. Keep these separate from the baseline.

External radar modules, OLEDs, speakers, holders, batteries, harnesses, enclosures and full product assembly are excluded unless separately listed. This enquiry is for a reviewable quote only and does not authorize purchases or manufacturing.

## Attachment manifest for preparation, not yet sent

- Current Gerbers/drills and full BOMs: `fabrication-candidates/090b207-r1/`.
- Supplier-neutral placement data derived from native coordinates, including both faces and THT; do not assume JLCPCB-adjusted CPL conventions transfer unchanged.
- Native pad/placement drawings: `placement-review/`.
- Exact via maps: `via-process/090b207-r1/`.
- Stackup/USB prototype disposition: `stackup-review/`.
- The actual exported package and supplier-specific placement file must receive a fresh manifest/hash review before sending.
