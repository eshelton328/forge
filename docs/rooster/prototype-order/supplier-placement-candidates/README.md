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

Other native footprint anchors, especially main J4 and Beacon J3 through-hole
headers, still need supplier-centroid review. Front D1 had no rendered LED body
in the observed preview, so that image cannot establish RGB pin orientation.
Do not apply this B3F-specific correction to other components automatically.
