# Prototype via fabrication process

Current source: native PCB commit `090b207` and fabrication candidate
`090b207-r1`. The original `4d8e65d-r1` attachments remain historical. **Specify epoxy-filled and copper-capped
vias for main and Beacon.** This supersedes the solder-mask **Plugged** option
used in the earlier cost drafts. Retain tented vias on controls and front.
No native copper, drill, mask or placement geometry changes in this disposition.
The saved assembly drafts still require updated fabrication settings and prices.

The separate, unsubmitted fabrication calculator shows **$99.41 per five-board
large-board batch** at 74 × 70 mm processing size with the matching 4-layer,
1.6 mm, generic FR4 TG155, ENIG 1 µin, 1 oz outer/inner copper, 0.2 mm minimum
drill option, Kelvin test and manual production review. This is **$20.41 above**
the earlier $79.00 fabrication estimate: $17.06 via fill/cap plus $3.35 required
horizontal electroless copper plating. It is not a recalculated assembly draft
or a landed quote. The two large-board batches imply a $40.82 fabrication
adjustment if all other quoted charges stay the same.

## Why the earlier process needs changing

Both large boards have twelve 0.3 mm thermal holes within U3's exposed ground
pad. Main also has a 0.2 mm via at U6's exposed-pad center (153, 106) mm and a
0.3 mm hole intersecting J5.5's mask opening. Beacon has a 0.25 mm via intersecting
U3.31's mask opening. All these intersections are on the same net as their
respective pads. Declaring a via tented does not cover it where an overlapping
pad's mask opening exposes it.

JLCPCB's solder-mask plugging process excludes vias in pad, one-sided openings
and vias close to pad openings. Epoxy fill followed by copper capping supports
these geometries. The native via diameters are within its supported range.
The process specification preserves the plated thermal paths; actual component
temperatures and solder-joint quality still require delivered-board testing and
assembly inspection. [JLCPCB via process, updated August 18, 2026](https://jlcpcb.com/help/article/pcb-via-covering),
[fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities).

## Exact fill scope

Fill and copper-cap **every plated round hole of nominal diameter 0.20, 0.25,
0.30 or 0.40 mm** in each large board, including the twelve thermal holes modeled
as U3 pad 41. No component lead hole uses those diameters in these source files.
Keep the original mask openings: capping a tented via does not authorize exposing
its copper, and filling an exposed thermal hole does not authorize masking the
solderable thermal land. Preserve the selected ENIG finish.

| Board | 0.20 mm | 0.25 mm | 0.30 mm | 0.40 mm | Total fill/cap | Holes/slots left open |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Main | 14 | 192 | 20 | 29 | **255** | 4 J4 lead holes, 4 USB shell slots, 6 NPTH |
| Beacon | 10 | 139 | 33 | 17 | **199** | 5 J3 lead holes, 3 SW1 lead holes, 4 USB shell slots, 6 NPTH |

**Do not fill connector or switch lead holes, USB shell slots, locating holes or
mounting holes.** Controls retains its 11 tented 0.3 mm vias; front retains its
6 tented 0.3 mm vias. Neither small board has a via hole intersecting a native pad
mask opening in this audit. Their component holes remain open.

The proposed quote uses **Epoxy Filled & Capped**. The live quote form requires
Horizontal Electroless Copper Plating for that process. This is a fabrication
selection, not authorization for checkout or payment. Do not substitute copper
paste filling, change copper weight or increase the layer count without recording
the resulting engineering and cost comparison.

## Supplier attachment and verification

The current attachment set was regenerated against `090b207-r1` and its matching
CAM reference. All four fill-coordinate CSVs match the earlier set byte-for-byte.
The inventory now records the four main J4 holes as **1.10 mm / leave open**;
all fill counts and locations remain unchanged. The updated main drill map was
rendered and inspected. No PCB bytes were changed by this process audit.

- [Main exact fill coordinates](090b207-r1/alec-main-fill-holes.csv) and
  [main drill map](090b207-r1/alec-main-via-process.svg).
- [Beacon exact fill coordinates](090b207-r1/alec-sensor-fill-holes.csv) and
  [Beacon drill map](090b207-r1/alec-sensor-via-process.svg).
- [Source-bound inventory](090b207-r1/via-process-review.json), including holes
  excluded from filling, mask-intersection evidence and artifact hashes.

CSV coordinates include both native downward-positive Y and Gerber
upward-positive Y, in millimetres with the verified zero auxiliary origin.
These are process attachments, **not component placement files**. The drill
maps show the native top view; small markers are enlarged for legibility and
slots are marked at their centers. Use the exact Gerbers/drills and CSV for CAM.

Before purchase, include the fill specification and process cost in the final
quote. In manual production review, verify the fill/cap scope, preserved open
component holes, surface finish and mask openings against these attachments.
The supplier's finished CAM files follow the order; automatic confirmation must
remain disabled. No supplier production approval is claimed here.

Reproduce using KiCad Python:

```sh
python tools/review_via_process.py \
  --candidate fabrication-candidates/090b207-r1 \
  --cam-reference cam-review/090b207-r1/native-reference.json \
  --output-dir via-process/090b207-r1-new
```

Run from `docs/rooster/prototype-order`. The audit checks source/manifest hashes,
all native plated-hole counts and each proposed fill location against the earlier
CAM reference. It rejects small component holes outside U3's known thermal
pattern and a nearest intersecting mask pad on a different net. It uses KiCad's
pad polygons with 0.001 mm approximation error and checks both mask faces.
This is not a complete mask-opening-to-trace or mask-bridge DRC, a stackup review,
or physical solder/process qualification.
