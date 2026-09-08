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

Both patterns' perimeter pads start 1.025 mm from the package center; the native
pad extends 0.025 mm farther outward and is 0.05 mm narrower. This arithmetic
does not establish solder-joint suitability. The manufacturer calls its drawing
a process-dependent recommendation. **Keep the land-pattern disposition open:**
either document suitability of the existing pattern for the exact package and
assembly process, or correct it to 90-0031 and recheck the affected native source,
clearances, copper, stencil and manufacturing exports. No pad change or waiver
has been made in this pass.

The fresh datasheet pin table agrees with native connectivity: 1 DIN, 2 GAIN_SLOT
to GND, 3 GND, 4 SD_MODE, 5/6 NC, 7/8 VDD, 9 OUTP, 10 OUTN, 11 GND, 12/13 NC,
14 LRCLK, 15 GND and 16 BCLK. The exposed pad is native pad 17 on GND. The speaker
uses both active BTL outputs. Final supplier rotation and pin-1 viewing convention
remain separate checks. Four 0.5 × 0.5 mm paste windows provide approximately
66.1% of the exposed copper-pad area; this is an observation, not stencil approval.

Sources: [ADI datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf)
(pages 15 and 37 visually read in the browser),
[90-0031 Rev.C](https://mds.analog.com/api/public/content/90-0031.pdf)
(one-page drawing downloaded and visually read; SHA-256
`5661318725986f79e664adb5fd24d80c2b444c1d48d3aa4c1b0d51ebfa53f4c8`).
A fresh 90-0032 download returned 404; no current review of that drawing is claimed.

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
