# JLCPCB quote progress — September 7, 2026

**No complete assembly quote, reservation, checkout, payment or order exists.**
The signed-in main-board draft contains its Gerbers, BOM and all 111 component
positions: **41 of 42 BOM groups are confirmed**, with the RTC still unavailable.
Erik must explicitly approve the exact items, quantities and total before any
order or paid parts procurement.

Erik supplied a USA shipping destination; the postal code and account-specific
draft URL are in the private Rooster task note. Postal-code-specific shipping/tax
has not been reached. These are live UI observations from September 7; stock,
pricing and lead times may change.

## Main-board draft

- Uploaded `fabrication-candidates/4d8e65d-r1/alec-main/alec-main-gerbers.zip`,
  SHA-256 `abee31e91877f17234b467d81afb02f6149a3f7133e2fabc4cf0385453742ac9`.
  JLCPCB detected **4 layers, 64 × 56 mm**, matching native source and CAM review.
- Uploaded the adjacent `alec-main-bom.csv` and `alec-main-cpl.csv`, including
  through-hole J4 and all **111 fitted positions**. R11 remains DNP.
- The actual matcher marks **ESP32-S3-WROOM-1-N16 / C2913199 Standard Only**.
  Switched from Economic to Standard; the PCB tab confirmed **Standard / Top
  Side / qty 2**. The generic restriction dialog establishes service eligibility,
  not a specific package or temperature defect in the ESP32.
- JLCPCB proposed **74 × 70 mm processing dimensions**, with supplier-added
  rails/fiducials around the unchanged native 64 × 56 mm outline. The form
  retained **5 fabricated / 2 assembled**, Single PCB, one design. After saving,
  the BOM view labels the input Single Piece. Actual rail geometry, final-board
  counts and connector/antenna clearance still need review.
- Set **Depanel boards & edge rail before delivery: Yes**. Production-file and
  placement review are Yes, with **Do not confirm automatically** checked in
  both dialogs. Returned to the saved BOM draft after these changes; recheck
  these settings on the final candidate before purchase.
- Retained candidate fabrication settings: 1.6 mm, green/white, ENIG 1 µin,
  1 oz outer and inner copper, plugged vias, 0.2 mm minimum drill option,
  ±0.2 mm outline tolerance and flying-probe test. The 0.2 mm option requires
  TG155 and extra 4-wire Kelvin testing. Stackup/via/stencil treatment remain
  open engineering decisions; this form is a cost-comparison draft.

## Main BOM matching

The saved draft shows 42 detected / 41 confirmed / 1 inventory-shortage group.
A catalog match is not completed orientation or assembly review.

| Reference | Exact part / supplier ID | Observed disposition |
| --- | --- | --- |
| J1, J3 | B2B-PH-SM4-TB(LF)(SN) / C160352 | Both rows explicitly selected; shared purchase quantity 5, $1.0985. Different native footprint names had left the rows unchecked initially. |
| J4 | TSW-104-07-G-S / C3335156 | THT header selected; 2 parts, $1.3308. Final placement/hand-soldering details remain open. |
| J5 | BM07B-GHS-TBT(LF)(SN) / C5305068 | Exact ID search resolved the unmatched row; 4,069 stock shown. Quote: 2 parts, $1.2496. No substitution. |
| U3 | ESP32-S3-WROOM-1-N16 / C2913199 | Selected after switching to Standard; 2 parts, $10.4476. |
| U5 | RV-3028-C7-32.768kHz-1ppm-TA-QC / C3019759 | **2 shortfall** in this draft. Kept in the required assembly scope. |

Advancing with the RTC unavailable offered to omit unselected parts. Chose
**Select parts**, preserving the requirement. Component Placements and Quote &
Order remain incomplete. No RTC omission was accepted.

## RTC procurement candidates

Four fitted RTCs are required across the two main and two Beacon assemblies,
before confirmed attrition. No alternate QA device was selected; no source
part fields changed.

| Route | Live observation | Remaining qualification |
| --- | --- | --- |
| JLCPCB C3019759 preorder | Stock 0; minimum 5; estimated $2.2337 each; displayed **$11.17 for five** | No firm date shown; price is an estimate. |
| Global Sourcing → CoreStaff | MICRO CRYSTAL **RV-3028-C7 32.768kHz 1PPM TA QC**; stock 2,190; MOQ 7; $2.9518 each; **$20.66 for seven**; **10–16 business days** | Candidate for the same QC part, with spacing/case differences in its name. Pkg field says “franchised”; actual packing/assembly intake need confirmation. Displayed attrition 0 is not final four-board allocation approval. |
| Global Sourcing → Verical | QC part; stock 13,000; MOQ 1,000; $1,812.20; 12–20 business days | Unsuitable minimum for this prototype batch; not selected. |

The full hyphenated MPN returned no Global Sourcing results; searching
**RV-3028-C7** exposed the QC offers alongside distinct QA and evaluation boards.
No Add, preorder, reservation, RFQ, checkout or payment was submitted. The Global
Sourcing cart remained empty.

The [RTC page](https://jlcpcb.com/partdetail/C3019759) supplies the preorder
estimate. JLCPCB says the price becomes firm only after initial payment and may
need adjustment. That payment requires Erik's approval.
[Preorder workflow](https://jlcpcb.com/help/article/how-to-build-your-own-parts-library-in-jlcpcb).

Global Sourcing is not ready JLCPCB warehouse stock. Its parts must arrive at
JLCPCB before they can be selected for assembly; sourcing time precedes assembly
and delivery. Paid global orders cannot be canceled or returned under its terms.
Offers were observed in the [Global Sourcing UI](https://jlcpcb.com/user-center/smtPrivateLibrary/orderParts/?global=1).
[Global Sourcing workflow](https://jlcpcb.com/help/article/how-to-use-jlcpcb-global-sourcing-parts-service).

## Incomplete prices and next quotes

The original Economic fabrication/options page showed $78.38 before parts or
assembly. After switching to Standard with 74 × 70 mm processing dimensions,
that amount showed **$79.00**, with component, feeder, SMT and hand-soldering
fields still blank. Country-level shipping showed **$27.50 DHL Express (DDP)**.
Do not add or multiply these incomplete one-board observations into a four-board
landed total. The service-switch dialog mentioned $25 setup per assembly side;
a completed quote must establish actual fees and discounts.

The other three archives have not been uploaded. Next quote controls and front
independently of RTC procurement, then Beacon with complete both-face and THT
coverage. Finish amplifier/pad, stencil/via/stackup, external-parts and first-power
dispositions alongside quoting. Final review must include supplier rotations,
rail detachment, fitted/bare counts, services/exclusions, shipping/tax and exact
approval-ready totals.
