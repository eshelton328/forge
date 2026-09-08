# Proposed technical enquiry to JLCPCB

**September 8 decision: Erik chose “Keep the enquiry unsent.”** Retain this draft
locally. No supplier enquiry was sent and no reply is pending.

**Draft only, not sent.** Sending this to supplier support requires Erik's
permission. It requests placement information only: no order, reservation,
purchase, substitution, rework or production approval.

The relevant unsubmitted drafts are named:

- `alec-main 090b207 - INCOMPLETE RTC - REVIEW ONLY`
- `alec-sensor 090b207 - INCOMPLETE RTC - REVIEW ONLY`

Their account-specific links are in private ROO-010. If Erik approves sending,
include those two links and the local placement-review sheet as context. No
address, payment information or unrelated project file is needed.

## Message

We are preparing two assembled copies each of the above boards and need to
resolve two component-placement preview discrepancies before ordering.

**ESP32-S3-WROOM-1-N16 / C2913199, U3 on both boards:** our CPL body center is
X=133 mm, Y=−76.5 mm, top, rotation 0°. In native board coordinates viewed from
the top with Y increasing downward, pad 1 is (124.25, 71.24), pad 15 is
(126.015, 89), pad 26 is (139.985, 89), and pad 40 is (141.75, 71.24). Native
body bounds are X=124…142 and Y=63.75…89.25. The preview module appears shifted
up relative to these pads. Please identify the library origin/offset used for
assembly and show numbered terminal alignment, so we can distinguish a model
display offset from a placement-coordinate correction.

**MAX98357AETE+T / C910544, U6 on main:** CPL X=153 mm, Y=−106 mm, top,
rotation 0°. In the same native top-view/Y-down frame, pin 1 DIN is
(151.5625, 105.25), pin 4 SD_MODE is (151.5625, 106.75), pin 9 OUTP is
(154.4375, 106.75), and pin 16 BCLK is (152.25, 104.5625). The preview corner
mark appears at lower left, while our required pin-1 location is upper left.
Please show the actual numbered pin orientation for this exact T1633+4 package.
We have not applied a rotation based only on the rendered dot.

For each item, please confirm whether an amended CPL is needed before ordering
or whether the correction is mapped in the later manual placement review.
An annotated numbered-pin view or explicit origin/rotation mapping would let us
verify the result. We require manual production-file and placement confirmation;
these incomplete-RTC drafts do not authorize assembly or omission of the RTCs.

Thank you.
