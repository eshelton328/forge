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

**Prototype mask disposition: retain the uniform native 1:1 openings, including
all U6 pads.** JLCPCB supports 1:1 openings. The [mask review](mask-review/README.md)
reports no violations at 0.09 mm mask-to-copper clearance, with an independent
negative control establishing that the rule is active. Actual Gerber geometry
also has at least 0.15 mm between distinct openings across all eight mask layers,
above the green, 1 oz requirement of 0.10 mm. This supplier-supported prototype
choice differs from ADI's preferred NSMD expansion; it does not relabel 1:1
openings as NSMD or claim solder-joint qualification. Supplier mask alterations
must preserve consistent treatment of U6 and be reviewed before production.
[JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities).

The [via-process specification](via-process/README.md) includes epoxy filling and
copper capping of U6's central 0.2 mm hole and the other small plated holes; the
earlier Plugged quote option is superseded. Together these close the source mask
and exposed-hole process decisions for this prototype. Final placement and
supplier stencil/process data still require their recorded manual reviews.

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


## Main D1: LTST-C190KGKT

The exact Lite-On manufacturer PDF was opened successfully in the browser after
command-line retrieval failed. Pages 2 and 7 were visually read. The package is
1.6 × 0.8 mm; its cathode marking agrees with native pad 1 on GND at
(117.2125, 92) mm. Pad 2 at (118.7875, 92) mm is the anode. R11 remains DNP,
so the fitted optional LED has no normal current path.

Retain the native copper pads: the recommended 0.8 × 0.8 mm pads have a 0.7 mm
inner gap; native 0.875 × 0.95 mm pads retain that same gap and add 0.075 mm
outward reach and lateral margin. Supplier assembly must put the marked cathode
on the native GND side. The manufacturer specifies 30 mA maximum DC current,
75 mW maximum dissipation and lead-free reflow constraints; these are limits,
not a proposed LED operating current. The initial BOM's R11 omission remains
part of the release requirements. Final lot/process and placement review remain
manual. [Lite-On DS22-2000-074](https://optoelectronics.liteon.com/upload/download/DS22-2000-074/LTST-C190KGKT.PDF).

## Beacon F1: 046701.5NRHF

The manufacturer’s 467-series sheet (February 27, 2023 revision) was visually read
in the browser, pages 1–3. The selected 1.5 A fast fuse has marking **K**,
nominal cold resistance 0.0385 Ω and nominal melting I²t 0.0766 A²s. Use the
sheet's conservative 32 V rating for this ≤5.4 V battery circuit; catalog wording
about a 65 V interrupt test is not needed to establish the voltage margin.
The specified opening times are at most 5 s at 3 A and 0.2 s at 4.5 A.
[Littelfuse 467 datasheet](https://www.littelfuse.com/assetdocs/fuse-467-datasheet?assetguid=4a59f034-1cca-460e-a5ba-e1e66247c76d).

**Retain F1 for the dry prototype evaluation, with a measured current envelope.**
The manufacturer's 25% continuous-current derating gives **1.125 A at 25°C**;
its 70°C example gives **0.9 A** after additional temperature derating. This
is a fuse-selection allowance, not a fast electronic current limit or proof that
all downstream faults will be cleared. Start on a current-limited bench source;
verify startup inrush and temperatures before battery operation or sustained
high-load testing. Do not infer pulse endurance merely from the melting-I²t value.
The fuse does not protect the holder/wire upstream of F1 against a harness short.

Native F1 is nonpolar, between VBAT and VBAT_FUSED. Its 0.875 × 0.95 mm pads
have 1.575 mm center spacing and a 0.7 mm gap. The example reflow lands in the
sheet are 0.762 × 1.09 mm, with a 1.02 mm gap and 2.54 mm overall reach. Native
lands are therefore not a literal copy. They extend to ±1.225 mm around the
1.60 ±0.102 mm body; their 0.95 mm width exceeds the 0.813 ±0.076 mm maximum
body width. Both native lands cover the terminal areas without joining. This
supports retaining the generic 0603 pattern for the prototype; final paste and
solder-joint inspection remain the assembler's process work. Reflow must respect
the fuse's 250°C target peak (245–250°C range) and other limits in the sheet.

## Main J4: TSW-104-07-G-S

The exact selected part is a straight, single-row, four-position Samtec header,
without the **-LL** locking-lead option. The catalog's 1.02 ±0.03 mm recommendation
is explicitly in the -LL section; do not apply that tolerance as if a locking
lead had been selected. The separate general footprint nevertheless recommends
1.02 mm nominal holes, so native 1.00 mm holes still merit an assembly-fit
review rather than a claim of exact drawing agreement.

The source has four 1.00 mm plated holes on 2.54 mm pitch and 1.70 mm lands.
The nominal 0.635 mm square pin diagonal is 0.898 mm, leaving about 0.102 mm
nominal diametral clearance. JLCPCB's standard negative hole tolerance can reduce
that clearance; nominal arithmetic is not a worst-case fit guarantee. Preserve
the selected part and source while finishing the finished-hole/process disposition.
No locking lead, alternate socket, hole enlargement or purchasing substitution
was silently applied. The **-07** drawing specifies a 5.84 mm mating post; the
external display cable still needs a female contact that accepts this post.

**Resolved by the subsequent [finished-hole correction](header-fit/README.md):**
main J4 now has four 1.10 mm plated holes in a dedicated local footprint. All
copper lands, coordinates, nets and the selected nonlocking MPN are preserved.
The stated supplier tolerance gives a 1.02 mm lower bound, matching Samtec's
recommended nominal hole. This supersedes the preceding instruction to retain
the 1.00 mm source while reviewing fit. A new main fabrication candidate is
required; the original uploaded archive must not be ordered.

Sources visually read: [Samtec footprint Rev.A](https://suddendocs.samtec.com/prints/tsw-xxx-xx-x-x-xx-xxx-footprint.pdf),
[series print Rev.DS, page 6](https://suddendocs.samtec.com/prints/tsw-xxx-xx-xxx-x-xx-xxx-mkt.pdf),
and [catalog, page 2](https://suddendocs.samtec.com/catalog_english/tsw_th.pdf).
Downloaded drawing SHA-256 values are respectively
`264658121ff2dad25ebd6259e726b123bf1ea31f9145bc695607999181af028f`,
`047ecedcc921fb0aed7127f08b9ba0fc1200d92d33fb7ded1b311d0ed8f42063`,
and `3a5770b11668f4e5a11ba9ceeb4817a23f467b8507e3592f55fb6bd8f96e71bc`.
