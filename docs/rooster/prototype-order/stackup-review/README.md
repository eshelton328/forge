# Prototype stackup and USB disposition

September 8, 2026. Candidate `090b207-r1`; no purchase or production approval.

For the two-set engineering prototype, specify **JLC041611-7628, four layers,
nominal 1.6 mm, 1 oz outer and inner copper** on main and Beacon. Retain the
native USB routing for this prototype, with the explicit functional-test risk
below. This is an engineering recommendation for the purchase proposal, **not
a claim of 90 Ω controlled impedance or Espressif layout compliance**. The
actual supplier quote and subsequent manual production review must retain the
named stackup and existing track geometry. No native PCB bytes changed.

## Fabrication specification

The [JLCPCB stackup page](https://jlcpcb.com/impedance), observed with four layers,
1.6 mm and **1 oz inner** selected, lists:

| Layer or dielectric | Material | Published thickness |
| --- | --- | ---: |
| F.Cu | Copper | 0.035 mm |
| F.Cu to In1.Cu dielectric | 7628 × 1, nominal relative permittivity 4.4 | 0.203 mm |
| In1.Cu | Copper | 0.030 mm |
| In1.Cu to In2.Cu core | Core, nominal relative permittivity 4.6 | 1.030 mm |
| In2.Cu | Copper | 0.030 mm |
| In2.Cu to B.Cu dielectric | 7628 × 1 | 0.203 mm |
| B.Cu | Copper | 0.035 mm |

The supplier labels this a nominal 1.6 mm construction; the listed constituents
sum to 1.566 mm before surface coatings. Do not replace the 1 oz inner selection
with the default 0.5 oz **JLC04161H-7628** construction. The current generic
quote's “No requirement” table corresponds to the selected 7628 construction,
but a generic selection does not establish an agreed exact production stackup.
Record the named requirement in the actual quote and inspect it before release.

Other observed 1 oz alternatives place In1 closer to the top traces: 3313 at
0.092 mm, 1080 at 0.069 mm, and 2116 at 0.109 mm. None was calculated or measured
to meet this board's impedance, so changing to one merely because the plane is
closer is not justified here. The supplier calculator produced no result even
for its default 50 Ω single-ended case on September 8; earlier differential
attempts also produced no result. No calculator pass is claimed.

Keep the independently specified [epoxy fill/cap process](../via-process/README.md),
TG155 eligibility for the 0.2 mm drill option, ENIG and manual production review.
Controls/front retain the existing two-layer, nominal 1.6 mm, 1 oz, TG135 quote
specification and tented vias. Their board-to-board GPIO/LED/control connections
have no USB pair or controlled-impedance requirement in this prototype scope.

## What the USB inspection establishes

[Native evidence](usb-native-routing.json) binds both PCB hashes, all six USB
data nets, individual tracks, component pin maps and 752 centerline samples per
board. The data geometry is identical between main and Beacon:

- Every USB track is 0.15 mm wide on F.Cu; no USB signal vias exist.
- Every sample at intervals no greater than 0.05 mm lies over filled In1 GND.
  This checks sampled centerlines, not the entire return-current corridor.
- Positive-net track segments total 18.280 mm; negative segments total 17.704 mm.
  These totals include the USB-C orientation branches and omit component
  internals. **Their difference is not path skew.**
- R34/R35 are fitted 22 Ω series resistors, approximately 2.74 mm of track from
  their MCU-side pads to U3.13/U3.14. U4 is the existing USBLC6-2SC6 protection.
- The data lines have variable separation and fanout, rather than a uniform
  coupled pair. No numeric differential impedance has been established.

[Espressif's layout guide](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html#usb)
recommends equal-length parallel pairs at 90 Ω ±10%, minimal transitions and a
continuous ground reference. This inventory supports the layer/return findings,
but **does not satisfy the complete recommendation**.

## Why retain the routes for the engineering prototype

ESP32-S3's internal USB PHY is **full-speed, 12 Mbit/s**.
[Espressif peripheral documentation](https://docs.espressif.com/projects/esp-iot-solution/en/release-v2.0/usb/usb_overview/usb_otg.html).
USB 2.0 §7.1.2.1 specifies 4–20 ns full-speed transitions under its specified
test load. That is an edge-rate requirement, not the 83 ns bit period.
[USB specification, p. 130](https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/2656.usb_5F00_20.pdf#page=158).

As a limited length screen, assuming effective permittivity 4.6 gives a
propagation speed of about 140 mm/ns. A deliberately generous 25 mm interconnect
length would then have about 0.179 ns one-way delay, below one tenth of a 4 ns
edge (0.4 ns). The 25 mm includes allowance beyond the native segment totals;
it is not an extracted package model or a measured end-to-end path. Actual
in-system edges and manufacturing tolerances are unknown. TI describes the
one-tenth edge-time criterion as an approximation; reflections never disappear.
[TI transmission-line discussion](https://e2e.ti.com/support/interface-group/interface/f/interface-forum/1305114/considering-pcb-trace-as-a-transmission-line-rise-time-vs-propagation-delay).

NXP also describes short full-speed routes as less dependent on exact 45 Ω
trace impedance in its LPC application note. That is supporting context, **not
an ESP32-S3 waiver**, and its component values are not substituted here.
[NXP AN11392 §3, p. 7](https://www.nxp.com/docs/en/application-note/AN11392.pdf#page=7).

The engineering judgment is that these short routes with no transitions and
sampled ground continuity are reasonable to fabricate for functional testing.
Retaining them avoids an unvalidated geometric change based on an unavailable
calculator. **USB may still require rework or a board revision**; disclose this
in the concrete purchase proposal. This disposition does not promise reliable
USB, USB-IF certification, or suitability for a later high-speed PHY.

Main has the existing six-pad J7 UART/recovery interface. Beacon has **no routed
UART0 service pads**: U3.36/RXD0 and U3.37/TXD0 are marked unconnected. Do not
describe J3's radar UART as a bootloader fallback. Temporary connections to the
module pads would be rework, not a verified ready-to-use programming interface.
Native USB plus accessible RESET/BOOT remains the planned Beacon recovery path.

## Tests after delivery

Run on every assembled main and Beacon after current-limited power-up and rail
checks. USB supplies data only; apply the separate board supply first. Use a
known data cable, both USB-C orientations, and repeat with a second known cable
if behavior is questionable. Verify ROM download entry with BOOT/RESET, ten
cold-start enumerations, repeated flash writes with readback/hash verification,
and a sustained diagnostic connection while enabling representative radio and
peripheral loads. Record board serial, supply, host, cable, firmware hash and
any disconnects. Unreliable enumeration, failed verification or repeatable load
disconnects fail the functional check and trigger signal/power diagnosis before
relying on that board for alarm tests. These are prototype acceptance tests,
not an electrical compliance suite or a pre-order demand for complete firmware.

The earlier physical-screening reports used assumed 0.2 mm copper-center
spacing and 17.5 µm inner copper. This stackup has about 0.2355 mm outer-to-inner
copper-center spacing and published 30 µm inner copper. Those old R/L/thermal
results remain nominal, uncorrelated screening; do not relabel them as a solver
run on the chosen production stackup.

Reproduce the read-only inventory with KiCad Python:

```sh
python tools/review_usb_routing.py --output stackup-review/usb-native-routing-new.json
```

Run from `docs/rooster/prototype-order`. Reproduction on September 8 matched all
prior track and ground-sample evidence exactly. The generator now records its
own hash and relevant USB/RESET/BOOT/UART pads. Neither the script nor its output
is a whole-board or supplier acceptance gate.
