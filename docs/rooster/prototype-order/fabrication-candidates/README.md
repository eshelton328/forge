# Fabrication candidates for quote review

**Main r1 is now historical only:** the [J4 finished-hole correction](../header-fit/README.md)
changes its four connector drills to 1.10 mm. A newly named main fabrication
candidate and placement binding are required before order release. The three
other boards' native geometry remains unchanged. The r1 inventory below describes
the preserved original files, not the corrected main board.

`4d8e65d-r1` contains four Gerber/drill archives plus matching BOM/CPL pairs,
exported from committed native sources at `4d8e65d327e1dd0e45adc906855b9b2ccb610a91`.
These are quote candidates, not an approved manufacturing release. **The r1
controls CPL is superseded for JLCPCB quotation by the [controls r2 placement
candidate](../supplier-placement-candidates/README.md)**, which corrects the three
B3F button centers. **Main and sensor CPLs are superseded by headers r2** at that
same link, correcting main J4's center/rotation and Beacon J3's center. All ZIPs
and BOMs remain unchanged. The manifest
binds the native inputs, exporter, layer list and every output file by SHA-256.
Archives contain fabrication layers and separate plated/unplated drill files;
the export logs, drill reports and job metadata remain outside the uploaded ZIP.

The [independent CAM check](../cam-review/4d8e65d-r1/cam-check.json) compares every
exported round hole and slot with KiCad-loaded native geometry, preserving
plating classes and multiplicities. All outline segments, layer counts and
207 fitted BOM/CPL references agree. No source geometry changed during export.

| Board | Outline (mm) | Copper layers | Plated holes, including slots | Unplated holes | Fitted references |
| --- | --- | --- | --- | --- | --- |
| alec-main | 64 × 56 | 4 | 263 (4 slots) | 6 | 111 |
| alec-controls | 27 × 34 | 2 | 26 | 4 | 5 |
| alec-front | 24 × 10 | 2 | 6 | 2 | 3 |
| alec-sensor | 64 × 56 | 4 | 211 (4 slots) | 6 | 88 |

The comparator allows 0.00051 mm drill rounding and 0.0000011 mm outline rounding.
Gerbonara 1.6.3 reports KiCad's `G90` position after the Excellon header as a syntax
warning; the parsed absolute coordinates and all hole geometries match the native
reference. This is not a supplier acceptance claim. Temporary-directory cleanup
warnings are also retained verbatim in the report.

Top/bottom PNGs in the CAM directory show copper and drills from the actual ZIP;
bottom overviews are mirrored into the viewing convention of a flipped board.
Separate mask, paste and silkscreen SVGs use the Gerber top-view coordinate
convention. Plain SVG rendering avoids filter-dependent solder-mask effects and
uses explicit board bounds so empty layers cannot expand the viewport to zero.
The copper overviews were visually inspected for gross truncation, outline/hole
alignment and recognizable placement. The per-layer SVGs support the remaining
stencil, mask and assembly review; their existence does not close that review.

The [amplifier copper-pad review](../assembly-drawing-review.md) now records a
prototype disposition retaining the native pattern and verifies its 17-pin map.
Its supplier orientation and final production data remain open. Source mask and
via-process decisions are now recorded in the separate reviews.

Still required before order release: remaining component dispositions, supplier
pin-1/rotation review, stackup and via treatment, Standard-board rails/fiducials
and detachment, complete THT/both-face assembly coverage, RTC supply, external
parts and first-power readiness, final checks and an accepted complete quote.
No rails or panels have been added to the functional board outlines.

Specify stencil requirements before purchase; JLCPCB creates actual production
stencil data after the order. Preserve manual production/placement review for
those later files rather than requiring a finished supplier stencil to request
spending approval. See the drawing review for the supplier's documented workflow.

All four ZIPs have been uploaded to JLCPCB for quoting. See
[quote progress](../quote-progress.md) for matching, placement findings and prices.
Candidate files must not be replaced in place when sources or supplier placements
change; preserve the original hashes and name the replacement explicitly.

Reproduce with `tools/build_fabrication_candidate.py`; run
`tools/review_fabrication_candidate.py native <candidate> <review-dir>` using
KiCad Python, followed by `cam` using Python 3.12 with Gerbonara 1.6.3 and
CairoSVG 2.9.1. The current macOS runtime requires KiCad's Frameworks directory
in `DYLD_FALLBACK_LIBRARY_PATH` for CairoSVG.
