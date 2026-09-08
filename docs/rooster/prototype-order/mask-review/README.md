# Solder-mask clearance and bridge review

**All four unchanged boards pass the focused mask-to-copper and distinct-opening
spacing checks.** No mask-to-copper violations at 0.09 mm were reported. Actual
Gerber opening separation is at least 0.15 mm, exceeding the selected green-mask
0.10 mm requirement. These checks are not complete fabrication acceptance.
Source hashes, temporary configuration and full DRC reports
are in [the measurement record](4d8e65d-r1/mask-review.json).

The native main/Beacon projects had `solder_mask_to_copper_clearance` set to
0.0 mm; controls/front had empty project files. Temporary copies set that rule
to JLCPCB's current 0.09 mm requirement and requested all DRC severities and all
track errors. No native board or project file was edited. The temporary projects
are retained next to the reports for reproduction; copy each next to an unchanged
board using its normal matching basename before running the recorded command.

| Board | Mask-related violations | Other reported findings |
| --- | ---: | --- |
| Main | 0 | 8 missing local footprint-library references in the isolated copy |
| Controls | 0 | 1 missing local footprint-library reference in the isolated copy |
| Front | 0 | 0 |
| Beacon | 0 | 8 missing local footprint-library references in the isolated copy |

These isolated-copy library findings are retained in the full reports; they do
not represent mask violations or a clean whole-project DRC run. Native project
validation already exists at the unchanged revision. No new zone fill or
schematic-parity test was requested in this check.

An independent negative control increased only mask-to-copper clearance to an
intentionally excessive 1.0 mm and produced **210 solder-mask bridge violations**
on main. This confirms that the selected KiCad rule was active. Increasing only
the legacy `solder_mask_min_width` project field to 1.0 mm produced no additional
findings, so the project field does not establish minimum bridge width. The
separate Gerber measurement below supplies that evidence instead.

## Actual Gerber opening separation

[The measurement record](4d8e65d-r1/gerber-mask-bridges.json) uses the immutable
r1 fabrication archives, with archive and native-board hashes checked against
their manifest. It merges overlapping/duplicate dark mask primitives before
measuring every pair of distinct openings on each side. Circular arcs are
approximated with 0.0001 mm maximum error; subtracting twice that amount from
each minimum still leaves every result above 0.10 mm.

| Board | Minimum top separation (mm) | Minimum bottom separation (mm) |
| --- | ---: | ---: |
| Main | 0.150000 | 0.605025 |
| Controls | 0.800050 | 0.650000 |
| Front | 0.500000 | 0.650000 |
| Beacon | 0.200000 | 0.605025 |

No merged opening encloses a separate mask island. Main and Beacon each have
four nonconvex openings at the two converters' stepped pads. The rendered
[U1 detail](4d8e65d-r1/converter-mask-detail.svg) was visually inspected: the
notches remain connected to the surrounding mask. This calculation establishes
separation between distinct openings; it does not measure every local neck in
the mask or approve supplier modifications.

Reproduce from the worktree root with Gerbonara and Shapely 2 installed:

```sh
python docs/rooster/prototype-order/tools/review_mask_bridges.py \
  --output-dir docs/rooster/prototype-order/mask-review/4d8e65d-r1
```

The report records the generator and library versions. The helper rejects clear
polarity primitives, invalid polygons and enclosed mask islands rather than
silently interpreting unsupported geometry. No native files are changed.

JLCPCB supports 1:1 pad/mask openings, a 0.09 mm opening-to-neighboring-trace
clearance and 0.10 mm bridges for the selected green mask/1 oz outer copper.
The [separate via-process specification](../via-process/README.md) addresses
holes exposed by overlapping pad openings. Retain the source's uniform 1:1 mask
openings for this prototype, including U6; this is not NSMD geometry or a claim
to follow ADI's preferred mask expansion. See the [amplifier disposition](../assembly-drawing-review.md).
Final supplier mask edits remain subject to manual production review.
[JLCPCB fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities).
