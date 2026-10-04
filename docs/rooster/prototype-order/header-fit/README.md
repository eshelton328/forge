# Main J4 finished-hole correction

**Use four 1.10 mm plated holes for the selected TSW-104-07-G-S header.**
The native board and schematic now use the local
`Board:Samtec_TSW-104-07-G-S_Drill1.10mm` footprint. Its 1.70 mm lands, 2.54 mm
pitch, pin order, position, model and mask openings are preserved. The MPN and
supplier part remain TSW-104-07-G-S / C3335156; this is the nonlocking variant.

Samtec's general footprint recommends 1.02 mm holes. JLCPCB publishes finished
through-hole tolerance of +0.13 / −0.08 mm, so a nominal 1.10 mm gives a stated
range of 1.02–1.23 mm. This replaces the old 1.00 mm choice, whose lower bound
was 0.92 mm. It is a prototype fit decision based on the recommended footprint,
not a fabricated worst-case tolerance for Samtec's nominal square post.
[Samtec footprint Rev.A](https://suddendocs.samtec.com/prints/tsw-xxx-xx-x-x-xx-xxx-footprint.pdf),
[JLCPCB drilling capabilities](https://jlcpcb.com/capabilities/pcb-capabilities).

The nominal annular ring remains 0.30 mm. At the maximum stated hole diameter,
subtracting a further 0.05 mm for hole-position offset leaves 0.185 mm of ring.
That is above JLCPCB's 0.15 mm absolute minimum for multilayer 1 oz boards.
This arithmetic is not a complete fabrication process-capability study. Actual
finished-hole inspection and sound solder joints remain assembler responsibilities.

The [source transition](source-transition.json) reconstructs the exact prior
native files by reversing only J4's footprint identifier/description and four
drills (plus the schematic footprint identifier). Every other source byte is
preserved. The [independent KiCad geometry check](geometry-review.json) also
confirms that all 492 copper records, 3,572 tracks, 243 vias, all placements,
pad nets/sizes and board bounds match before/after. Only J4's four drill records
and footprint name differ in that export. Both schematic and local library
agree with the placed board; full DRC/parity found no violations.

The current physical-screening solver consumes copper polygons, tracks, vias
and selected power-pad positions/values. Those inputs are unchanged; its code
does not use J4's footprint name or pad-drill records. Historical nominal solver
results can therefore be retained with this explicit limitation. No new solver
run, connector-hole thermal model, enclosure rebuild or physical qualification
is claimed. The original hashes remain in those historical records.

Reproduce the geometry check with KiCad Python:

```sh
python docs/rooster/prototype-order/tools/review_header_fit.py
```

Creation scripts now apply this bounded fit correction before purchasing fields.
The purchasing CSV retains its historical footprint column; exporters explicitly
resolve J4 to the new native footprint while retaining the exact selected MPN.
Regression checks reject unrecorded pin/net/position/hole edits. The layout guard
checks the minimum finished-hole allowance and annular ring on all four pads.

Validation at this source: main ERC, all-severity/all-track-error DRC with
schematic parity, JLCPCB four-layer advanced-rule DRC and board-content validation
pass. All 355 checked pad nodes have same-net copper. The interface checks pass
487 assertions and layout checks pass 153. Purchasing reconciliation covers all
207 fitted references; the only stock shortages remain main/Beacon U5. Repository
tests pass **145, with one skipped** because the optional SciPy-dependent test
runtime is unavailable. The unchanged solver run was not rerun. Source and
documentation whitespace checks pass.

**The uploaded main r1 Gerber archive is superseded by this source correction.**
Keep it as historical quote evidence. Generate a newly named fabrication
candidate and rebind the corrected J4 placement to it before a new supplier
upload. The other three boards' native geometry and archives are unchanged.
No order or supplier production approval is authorized by this correction.
