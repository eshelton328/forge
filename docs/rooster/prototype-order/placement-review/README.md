# Manual placement and production review sheet

Prepared September 8, 2026 for native source `090b207` and the current quote
candidates. **Prepared locally; not sent to the supplier and not approved for
production.** It makes the outstanding comparisons concrete without applying
speculative supplier offsets or rotations.

## Exact comparison reference

[Native placement reference](090b207-r1/native-placement-reference.json) contains
all **207 fitted references: 111 main, 5 controls, 3 front, 88 Beacon**. Each entry
includes exact MPN/catalog ID, source footprint/side, native anchor, the reviewed
supplier CPL row, and every numbered native pad's net, center, size, rotation and
drill. Repeated pad numbers are preserved, including U3's thermal-pad geometry.
U5 remains included on both large boards, regardless of the incomplete price
previews. Main R11 remains DNP.

The read-only builder verifies current native hashes against the fabrication
manifest, native MPNs against the upload BOM, complete BOM/CPL reference coverage,
assembly sides and supplier-CPL manifest bindings. It does **not** compare supplier
production data or prove the manufacturer pin mapping of every component.
Reproduce with KiCad Python and
`tools/build_placement_reference.py --output <new-json-path>`; it refuses overwrite.

Coordinates below and `native_center_mm` use **X right, Y down, viewed from the
board top, millimetres**. Bottom-face components are shown through the board in
that same coordinate frame, not as a mirrored bottom photograph. Supplier CPL Y
is upward-positive. Native pad coordinates are inspection targets, **not CPL
centroids**. An intentionally corrected header/body center must not be reset to
the native footprint's pin-one anchor.

## Priority reconciliation

| Item | Exact comparison target | Required resolution |
| --- | --- | --- |
| Main and Beacon U3 | ESP32-S3-WROOM-1-N16 / C2913199; current CPL (133, −76.5), top, 0° | Reconcile supplier package origin against all perimeter pads and the antenna/body envelope; the preview body appears above native pads. Do not derive a 3–4 mm correction from that image alone. |
| Main U6 | MAX98357AETE+T / C910544; current CPL (153, −106), top, 0° | Establish actual numbered pin 1 and all four sides. The displayed corner mark is insufficient evidence for rotating the part. Use the retained T1633+4 package and verified 17-pad map. |
| Front D1 / Beacon D2 | 150141M173100 / C5342281 | Supplier previews lack a useful body model. Match common anode and all RGB cathodes, not just body outline. |
| Beacon J3 | SSW-105-01-F-S / C5930350; corrected CPL (150.08, −108), top, 0° | Confirm the five socket contacts centered on the five holes, pin order and actual socket face/height. Placeholder centering is not a pin-1 sign-off. |
| Main J4 | TSW-104-07-G-S / C3335156; corrected CPL (161, −89.81), top, 270° | Preserve the reviewed center/rotation and four 1.10 mm holes; do not fill the lead holes or substitute a female socket. |
| Controls SW1–SW3 | B3F-1060 / C726010; corrected centers (20, −6), (20, −18), (20, −30), top, 0° | Preserve the corrected body centers and four-hole alignment. Confirm controls rear J1 and power switch SW4 as well. |
| PH/GH headers and Beacon rear controls | Exact entries in the native reference | Compare every keyed connector's signal-pad order and retention pads, bottom-face orientation and switch contact mapping. Main J3 body overhang needs rail/fixture clearance. |

All fitted components,
including the other ICs and polarized parts, remain in the full production review;
the table prioritizes observed ambiguities rather than granting a blanket pass.

### U3 native perimeter landmarks, both large boards

| Pin | Native X, Y (mm) |
| --- | --- |
| 1 | 124.25, 71.24 |
| 14 | 124.25, 87.75 |
| 15 | 126.015, 89 |
| 26 | 139.985, 89 |
| 27 | 141.75, 87.75 |
| 40 | 141.75, 71.24 |

Native F.Fab body bounds are X 124…142 and Y 63.75…89.25, centered at (133, 76.5).
These native landmarks supplement the manufacturer's package drawing; they are
not proof of how JLCPCB defines its library origin.

### U6 and RGB orientation landmarks

U6 pin 1 DIN is (151.5625, 105.25); pin 4 SD_MODE is (151.5625, 106.75); pins 7/8
VDD are (153.25, 107.4375) / (153.75, 107.4375); pin 9 OUTP is
(154.4375, 106.75); pin 10 OUTN is (154.4375, 106.25); pin 16 BCLK is
(152.25, 104.5625). Exposed pad 17 is GND at (153, 106). All perimeter net/size/
position entries match the earlier [ADI drawing review](../assembly-drawing-review.md).

| LED pad / function | Front D1 X, Y | Beacon D2 X, Y |
| --- | --- | --- |
| 1 / common anode, 3v3 | 19.55, 4.3 | 131.55, 120.3 |
| 2 / blue cathode | 19.55, 5.7 | 131.55, 121.7 |
| 3 / red cathode | 16.45, 4.3 | 128.45, 120.3 |
| 4 / green cathode | 16.45, 5.7 | 128.45, 121.7 |

## Manufacturing requirements to carry into the order

- Five fabricated / two assembled **finished functional PCBs per design**;
  supplier rails/fiducials do not redefine that quantity. Main is Standard / Top;
  controls, front and Beacon are Standard / Both Sides, including listed THT.
  Factory rail removal is selected. Preserve native functional outlines.
- Main/Beacon: named JLC041611-7628, nominal 1.6 mm, 1 oz outer/inner, FR4 TG155,
  ENIG 1 µin, minimum via option 0.2 mm, Kelvin/flying-probe tests. This is the
  [prototype stackup disposition](../stackup-review/README.md), not certified
  90 Ω USB routing. Controls/front retain their documented two-layer settings.
- Apply the exact [via attachments](../via-process/README.md): 255 main / 199
  Beacon small plated holes filled with epoxy and copper capped; preserve open
  lead holes, USB slots and NPTH. Controls/front retain tenting.
- Retain the [uniform 1:1 mask disposition](../mask-review/README.md). Review
  supplier changes to mask openings explicitly, including U6.
- Preserve separated U6 thermal paste apertures with 50–80% coverage and adequate
  release, using the selected stencil process. Native rounded-aperture coverage
  is 62.552%; it does not certify the supplier's finished stencil. Review both
  assembly faces, DNP treatment and the other thermal-pad apertures.
- Rails/tooling must clear connector mating/overhang and the ESP32 antenna area,
  permit THT assembly and leave the delivered board undamaged after removal.
  Actual supplier panel/rail geometry is still required for final confirmation.
- U5 must be restored in main/Beacon from the exact approved RTC supply route.
  A quote labeled INCOMPLETE RTC is not a manufacturing instruction to omit it.

## Purchase and production stages

The review reference and requirements can be prepared before purchase. Resolve
supplier-library placement ambiguities using authoritative pin/placement data;
do not declare them fixed simply because this sheet exists. Exact purchase scope,
parts intake, final services/landed cost and Erik's permission remain outstanding.

Actual supplier CAM, panel/rails, stencil and final placement data follow the
order. Both new main/Beacon drafts have manual production-file and placement
review enabled with automatic confirmation disabled. Compare those final files
against this sheet and the bound manufacturing inputs before approval. A supplier
change that alters native electrical/mechanical intent returns for engineering
review; it is not automatically accepted to advance production.

Controls/front may retain their reviewed historical Gerber uploads: their native
source hashes, BOM bytes and corrected/native CPL bytes match the current candidate
exactly, and the existing graphic-layer continuity check establishes matching
manufacturing primitives. Preserve their actual uploaded ZIP hashes in any final
order record; do not claim that a regenerated ZIP was uploaded when it was not.
