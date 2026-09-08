# Supplier placement candidates

These files record supplier-specific placement corrections without moving native
footprints, copper, drills, or functional outlines. They are review candidates,
not manufacturing releases. Preserve the original candidate files and their hashes.

## Controls r2 — B3F pushbutton centers

Use [controls-r2/alec-controls-cpl.csv](controls-r2/alec-controls-cpl.csv) with
the unchanged controls Gerber ZIP and BOM from `fabrication-candidates/4d8e65d-r1`.
This CPL supersedes the r1 controls CPL for the active JLCPCB draft.

The initial JLCPCB preview placed B3F-1060 / C726010 bodies on the native corner-pin
origins. Native pads form 6.5 × 4.5 mm rectangles; their centers agree with the
6 × 6 mm F.Fab bodies. Correct only the three CPL centers:

| Reference | Original CPL X, Y (mm) | Corrected CPL X, Y (mm) | Side / rotation |
| --- | --- | --- | --- |
| SW1 | 16.75, −3.75 | 20, −6 | top / 0° |
| SW2 | 16.75, −15.75 | 20, −18 | top / 0° |
| SW3 | 16.75, −27.75 | 20, −30 | top / 0° |

J1 and SW4 rows are unchanged. Negative CPL Y is the established Cartesian export
convention, matching the r1 Gerber/drill origin. The builder checks native and input
CPL hashes, footprint identity, rotation, all four holes, spacing and anchor, and
preserves every other row. It does not infer offsets for unrelated footprints.

Re-uploaded this CPL to the existing controls draft on September 7, 2026. The J1
catalog match had to be restored afterward. All three B3F models were visually
checked again in the supplier preview and now center on their hole patterns.
The preview itself says it is a reference view and requires final DFM placement
review after an order. This limited correction does not certify every pin-1,
rotation, connector origin, process rail, or supplier manufacturing file.

[Manifest](controls-r2/manifest.json) records the before/after rows, native hole
coordinates and hashes. Reproduce into a new, nonexistent directory with KiCad
Python and `tools/build_controls_placement_candidate.py --output <new-directory>`.
The tool emitted the usual KiCad wx diagnostic and exited zero. Native files,
Gerbers and the BOM are unchanged.

Do not apply this B3F-specific correction to other components automatically.

## Headers r2 — main display header and Beacon radar socket

Use [headers-r2/alec-main-cpl.csv](headers-r2/alec-main-cpl.csv) and
[headers-r2/alec-sensor-cpl.csv](headers-r2/alec-sensor-cpl.csv) with their unchanged
r1 Gerber ZIPs and BOMs. These supersede the corresponding r1 CPLs in the JLCPCB
drafts. U5 remains in both files and in the required assembly BOM despite the
temporary RTC-excluded supplier preview.

| Board / reference | Original CPL X, Y / rotation | Corrected CPL X, Y / rotation |
| --- | --- | --- |
| Main J4, TSW-104-07-G-S | 161, −86 / 0° | 161, −89.81 / 270° |
| Beacon J3, SSW-105-01-F-S | 145, −108 / 0° | 150.08, −108 / 0° |

Both native origins are pin 1. Main's four holes run vertically at 2.54 mm pitch;
its supplier model was horizontal and centered on pin 1. A quarter-turn and
the actual body/hole-row center align the model with the four holes. This plain,
unkeyed single-row header is mechanically equivalent under a 180° reversal;
the final display cable/module pin mapping still matters.

Beacon's five holes run horizontally at 2.54 mm pitch. The midpoint is its body
center; the supplier only renders a checkerboard placeholder, now centered on
hole 3 after re-upload. That is coordinate verification, not socket body/pin-1
approval. Native rear SW1 already has a central origin; no change was applied.

The [manifest](headers-r2/manifest.json) binds both native files, unchanged ZIPs
and BOMs, input/output CPL hashes, native holes and exact before/after rows.
All other 110 main and 87 Beacon rows are unchanged. The source-bound builder
checks footprint identity, native orientation, hole count/pitch/plating/drill,
origin, fitted reference coverage and file hashes before writing a new directory.
Reproduce with KiCad Python and
`tools/build_header_placement_candidate.py --output <new-directory>`. Generation,
independent CSV comparison/hash checks and Python compilation passed. No native
geometry or manufacturing archive changed.

## Remaining preview discrepancies

Both U3 ESP32 models appear above their actual board pads. Native F.Fab body
bounds are X=124…142 and board Y=63.75…89.25 mm, centered at **(133, 76.5)**,
which agrees with the unchanged CPL (133, −76.5). The bottom row (pins 15–26)
has board Y=89 mm. This differs from the proven corner-pin header cases:
do not blindly substitute a different center based on the preview image alone.
Reconcile the supplier library/model origin and all perimeter-pad positions
before accepting placement. Both drafts remain review-only.

Front D1 and Beacon D2 RGB LEDs, and Beacon J3 socket, lack useful body models
in the observed previews. Manufacturer pin maps and the final supplier placement
files must establish their orientation. No whole-board placement sign-off is
implied by these corrected centers.
