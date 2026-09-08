# Solder-mask clearance review

**No mask-to-copper violations at 0.09 mm were reported on any of the four
unchanged native boards.** This is a focused rule check, not complete mask or
fabrication acceptance. Source hashes, temporary configuration and full reports
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
findings, so **the 0.10 mm minimum mask-bridge width is not established by this
test**. Do not count that unverified field as a passing manufacturing check.

JLCPCB supports 1:1 pad/mask openings, a 0.09 mm opening-to-neighboring-trace
clearance and 0.10 mm bridges for the selected green mask/1 oz outer copper.
The [separate via-process specification](../via-process/README.md) addresses
holes exposed by overlapping pad openings. Minimum bridge width, final supplier
mask edits and the amplifier's consistent mask treatment still require their
own disposition. [JLCPCB fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities).
