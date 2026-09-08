# Assembly drawing review — September 7, 2026

This records additional manufacturer drawing checks against native source commit
`4d8e65d327e1dd0e45adc906855b9b2ccb610a91`. It supplements the earlier component
and electrical reviews; it is not whole-board assembly approval.

## Main U6: MAX98357AETE+T

The current ADI MAX98357A/B datasheet, Rev.16 February 2026, identifies the selected
16-pin TQFN part as T1633+4 and points to land pattern 90-0031. The native footprint
is `TQFN-16-1EP_3x3mm_P0.5mm_EP1.23x1.23mm`; its description references T1633-5
and drawing 90-0032. The package family/body/pitch match, but the recommended pad
dimensions are not identical.

| Dimension | Native footprint | ADI 90-0031 Rev.C |
| --- | --- | --- |
| Perimeter pad length × width | 0.825 × 0.25 mm | 0.80 × 0.30 mm |
| Opposing pad center separation | 2.875 mm | 2.85 mm |
| Adjacent pin pitch | 0.50 mm | 0.50 mm |
| Exposed copper pad | 1.23 × 1.23 mm | 1.23 × 1.23 mm |

**Disposition: retain the native copper land pattern for prototype order
preparation.** ADI package drawing 21-0136 Rev.V identifies the T1633-4 terminals
as 0.20/0.25/0.30 mm minimum/nominal/maximum width, at 0.50 mm pitch. ADI's QFN
assembly guide recommends matching terminal width at this pitch. The native
0.25 mm width matches that nominal dimension. This is an engineering disposition
using the package and assembly guidance, not a literal copy of 90-0031 or supplier
process approval.

Both patterns' perimeter pads start 1.025 mm from the package center. The native
outer edge is 1.85 mm from center: 0.35 mm beyond the nominal 3 mm body, within
ADI's 0.20–0.50 mm outward-extension guidance. Nominal inward extension is
0.075 mm with the selected package's 0.40 mm terminal length. Adjacent copper
pads have a 0.25 mm gap. The exposed copper land matches 90-0031. The native
description's T1633-5 reference therefore does not, by itself, require changing
these pads; use the exact selected T1633+4 package for production review.

The fresh datasheet pin table agrees with native connectivity: 1 DIN, 2 GAIN_SLOT
to GND, 3 GND, 4 SD_MODE, 5/6 NC, 7/8 VDD, 9 OUTP, 10 OUTN, 11 GND, 12/13 NC,
14 LRCLK, 15 GND and 16 BCLK. The exposed pad is native pad 17 on GND. The speaker
uses both active BTL outputs. The read-only
[measurement report](amplifier-assembly-review.json) binds this result to the
unchanged native PCB hash and verifies all 17 pad nets, sizes and positions.
Reproduce it using KiCad Python with
`tools/review_amplifier_assembly.py --output amplifier-assembly-review.json`.

Four rounded 0.5 × 0.5 mm paste windows, each with a 0.125 mm corner radius,
provide **62.552%** of the exposed copper area. The earlier 66.1% figure used
bounding squares and was incorrect for the actual apertures. This measured
coverage falls within ADI's 50–80% guidance. The report also calculates native
aperture area ratios at assumed 0.100, 0.120 and 0.127 mm stencil thicknesses;
all exceed 0.66. These are geometric examples, not selected production-stencil
specifications. ADI's thicker-stencil guidance changes aperture sizes, so passing
these examples does not approve an unmodified 0.127 mm stencil.

**Placement remains open.** In the September 7 signed-in JLCPCB 2D/3D preview,
the model's marked corner appears at lower left while the native silkscreen
triangle identifies the upper-left pad. No supplier rotation change was made
in this review. The required native pin 1 (DIN) is at board coordinate
**(151.5625, 105.25) mm**, with package center **(153, 106) mm** in KiCad's
top-view, downward-positive Y convention. Reconcile the model orientation with
the numbered package pins and final supplier placement data; the preview dot
alone is not a numbered pin map. [JLCPCB's placement conventions](https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2).

The default native mask opening is 1:1 with copper. JLCPCB's current capabilities
allow 1:1 openings and require at least 0.09 mm clearance to neighboring traces;
the green, 1 oz mask-bridge minimum is 0.10 mm. This establishes supplier
capability, not complete local mask clearance or compliance with ADI's preference
for NSMD pads. Verify the final mask treatment consistently across U6, along with
the thermal-via treatment and solder process. [JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities).

Sources: [ADI datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf)
(pages 15 and 37 visually read in the browser),
[21-0136 Rev.V](https://mds.analog.com/api/public/content/tqfn_21-0136.pdf)
(page 2 visually read; SHA-256
`8d5551d518227724b29191e4f4c884115ba9d4540bf09d4cdcccfb31da13f52d`),
[90-0031 Rev.C](https://mds.analog.com/api/public/content/90-0031.pdf)
(one-page drawing downloaded and visually read; SHA-256
`5661318725986f79e664adb5fd24d80c2b444c1d48d3aa4c1b0d51ebfa53f4c8`),
and [ADI QFN assembly guidance](https://www.analog.com/en/resources/app-notes/smt-assembly-and-pcb-design-guidelines-for-maxims-standard-wirebonded-quad-flatpack.html).
A fresh 90-0032 download returned 404; no current review of that drawing is claimed.

## Stencil review sequencing

JLCPCB generates its production stencil after PCB/SMT production-data preparation,
using its own aperture rules rather than directly manufacturing the uploaded
F.Paste Gerber. Before purchase, record the required separated thermal apertures,
coverage/release constraints, assembly sides and DNP treatment. Actual production
stencil and placement approval follow the order and must remain manual. The
finished supplier stencil is therefore not a prerequisite for requesting Erik's
spending approval. This does not authorize an order or release an unresolved
design issue. [JLCPCB stencil workflow](https://jlcpcb.com/help/article/smt-stencil-data-prepared-for-smt-orders).

## JST PH: main J1/J3 and Beacon J1

The exact selected part is **B2B-PH-SM4-TB(LF)(SN)**, the two-circuit, 2 mm pitch
top-entry SMT header. The current JST PH catalog pages 2 and 4 were visually
read. The top-entry PCB pattern specifies at least 1 mm signal-pad width, 2 mm
pitch, and 1.6 × 3.0 mm retention pads. Native signal pads are 1 × 5.5 mm, with
matching pitch and retention-pad dimensions. The signal-pad ends and retention
offsets meet the drawing's 7.5 mm minimum overall reach and 2 mm maximum rear
setback. The standard battery footprints and custom speaker-overhang footprint
retain this same pad geometry.

The top-entry body is distinct from the side-entry S2B variant. Native source and
the manufacturer mounting-surface view must still be reconciled in the supplier's
placement preview. The custom speaker overhang also requires rail/fixture
clearance confirmation. External PHR-2 housings/contact and wire choices remain
in the harness scope; main J3 carries the two active BTL speaker signals.

Source: [JST PH catalog](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf), SHA-256
`447624f4f2f7d37c58c1eaa7ee314ad757fe7aff48f6186491ef6f69fbc00b96`.
