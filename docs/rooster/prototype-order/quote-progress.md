# JLCPCB quote progress — September 7, 2026

**No complete four-board landed quote, reservation, checkout, payment or order exists.**
All four signed-in drafts now contain Gerbers, BOMs and complete placement files.
Main has **41 of 42 BOM groups confirmed** and Beacon **37 of 38**; the remaining
group in each is the unavailable RTC. Their incomplete price previews exclude it.
Erik must explicitly approve the exact items, quantities and total before any
order or paid parts procurement.

Controls and front have all fitted parts matched. The four price previews and
the controls/header placement corrections are recorded below. No Save to Cart
action was submitted. The estimate including separately listed rail removal is
**$750.25 before RTCs, any related assembly-fee changes, shipping, tax and external
parts**. This is arithmetic from draft pages, not a complete quote or final bill.

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

Initially chose **Select parts** when advancing offered to omit the RTC. Later,
to inspect placements and capture the remaining assembly costs, renamed both
main and Beacon drafts **INCOMPLETE RTC - REVIEW ONLY** and used **Do not place**
for the temporary RTC-excluded preview. **This is an incomplete supplier draft,
not authorization to omit the RTC from the ordered boards.** The full required
native and uploaded BOM/CPL files still include U5; no DNP or source change was
made. Restore/select sourced RTCs and recalculate before purchase approval.

## Beacon draft and main/Beacon price previews

Beacon Gerber ZIP SHA-256:
`0763d0b54402151a925ea1437c293f5484da0f6d5a1f63483d3d5ebcf1df1f85`.
The supplier recognized 4 layers and the native **64 × 56 mm** outline. The
draft requests **5 fabricated / 2 assembled**, Standard, Both Sides, supplier
processing dimensions **74 × 70 mm**, and depaneling. Production-file and
placement reviews were set to Yes with automatic confirmation disabled. It uses
the same four-layer fabrication options as main above. The complete 88-reference
placement file includes rear SW1; J3 purchases the radar socket only.

All available Beacon parts are selected: 37 of 38 BOM groups. J1 PH connector:
5 parts/$1.0985; J3 SSW-105-01-F-S / C5930350: 2/$1.9002; rear SW1
1101M2S3CQE2 / C221538: 2/$20.4006; U3 ESP32: 2/$10.4476. U5 has a two-part
shortfall, matching main's RTC dependency. Catalog matching does not certify
placement or the whole assembly process.

The following were captured again after the header CPL corrections:

| Item | Main | Beacon |
| --- | --- | --- |
| PCB fabrication/options | $79.00 | $79.00 |
| Standard assembly, **excluding U5 RTC** | $157.90 | $215.89 |
| Displayed total | **$236.90** | **$294.89** |
| Rail removal | $2.30 included | $2.30 separately listed; page warns some advanced options are excluded |
| Parts priced | 40 unique items ($55.08); 41 BOM groups share one PH part | 37 items ($71.43) |
| Build-time observation | PCB 3–4 days; assembly 5–6 days plus 1 advanced-option day | PCB 3 days; assembly 5–6 days plus 3 advanced-option days |

No rush option selected. Beacon would be $297.19 if its separately listed $2.30
rail removal is the only adjustment. The four displayed totals sum to $745.65;
adding front and Beacon's separate $2.30 options gives **$750.25**. RTC procurement
and any changed feeder/stencil/assembly costs must be added through a revised
supplier quote, not assumed to be the bare RTC purchase price alone. Shipping,
tax, radar/display modules, cables, holders, cells, speaker and equipment remain
outside these estimates. No combined-cart total or delivery date is claimed.

Main assembly breakdown: setup $25.56, stencil $8.21, components $55.08, feeder
loading $59.67, SMT $2.44, placement review $0.45, hand soldering $3.58, manual
assembly $0.13, packaging $0.49 and depaneling $2.30. Beacon: setup $51.12,
stencil $16.42, components $71.43, feeders $53.55, SMT $2.17, placement review
$0.45, hand soldering $3.58, manual assembly $0.26, fixture $16.42, packaging
$0.49; depaneling separately as above. Four-layer fabrication breakdown on both:
special offer $7.00, ENIG $17.10, inner copper $16.63, material $3.41, Kelvin
test $16.76, minimum drill option $17.06, production review $1.04.

Uploaded [headers r2](supplier-placement-candidates/README.md): main J4 changes
to CPL (161, −89.81), 270°; Beacon J3 to (150.08, −108), 0°. Main J5's exact
C5305068 match and both PH selections were restored after reprocessing. A
fresh DOM check found no unselected available component rows on either board;
the only shortage remains U5. Main J4 now overlays its vertical four-hole row.
Beacon J3's placeholder now lies on the middle hole, but no socket body model
exists in this preview. U3 still appears shifted in both boards' supplier views;
its native body-center coordinates have not been changed speculatively.
Returning to main's BOM tab after restoring both PH rows produced an inconsistent
summary counter (43 confirmed against 42 detected). The actual DOM contains
**41 selected component rows**, plus the U5 shortage row; the price page contains
40 unique priced items because J1/J3 share C160352. Use the reconciled rows and
file references, not that counter, when checking coverage. Both drafts were left
on their full BOM views with U5 still showing two-part shortfalls and cart count 0.

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

## Earlier fabrication-only price observations

The original Economic fabrication/options page showed $78.38 before parts or
assembly. After switching to Standard with 74 × 70 mm processing dimensions,
that amount showed **$79.00**, with component, feeder, SMT and hand-soldering
fields still blank. Country-level shipping showed **$27.50 DHL Express (DDP)**.
Do not add or multiply these incomplete one-board observations into a four-board
landed total. The service-switch dialog mentioned $25 setup per assembly side;
a completed quote must establish actual fees and discounts.

## Controls and front — assembly prices captured

Both drafts retain **5 fabricated / 2 assembled**, one design, Single PCB,
Standard, Both Sides, supplier rails/fiducials, and factory rail removal. Both
production-file and placement review have automatic confirmation disabled.
Two-layer settings: 1.6 mm, TG135, green/white, ENIG 1 µin, 1 oz copper, tented
vias, minimum drill option 0.3 mm, ±0.2 mm outline and flying-probe test. Native
drill reports confirm the 0.3 mm minimum. These are quote settings pending final
manufacturing review.

| Item | Controls | Front |
| --- | --- | --- |
| Native outline / proposed processing size | 27 × 34 / 71 × 70 mm | 24 × 10 / 70 × 70 mm |
| Matched BOM / fitted placements per board | 3 groups / 5 placements; four top THT switches and rear SMD J1 | 3 groups / 3 placements; front D1/SW1 and rear J1 |
| PCB fabrication/options | $22.04 | $22.04 |
| Standard assembly displayed | $93.61 | $76.17 |
| Displayed total | **$115.65** | **$98.21** |
| Rail removal | $2.30 included in the displayed assembly total | $2.30 listed separately; the page says some advanced options are excluded from its total |
| Build-time observation | PCB 24 hours; assembly 4–5 days plus 1 day for advanced options | PCB 24 hours; assembly 3–4 days plus 3 days for advanced options |

These are board/assembly estimates, **excluding shipping and tax**. Front would
be $100.51 if its displayed $2.30 rail-removal charge is the only adjustment;
confirm the actual cart total rather than treating that arithmetic as a final bill.
No rush option was selected. No cart, checkout or order was submitted.

Controls assembly breakdown: setup $51.12, stencil $8.21, parts $8.99, feeder
loading $1.53, SMT $0.03, placement review $0.45, hand soldering $3.58, manual
assembly $0.49, fixture $16.42, packaging $0.49, and rail removal $2.30. Front:
setup $51.12, stencil $16.42, parts $3.05, feeder loading $4.59, SMT $0.05,
placement review $0.45, packaging $0.49; rail removal separately as above.

Controls exact matches: six B3F-1060 / C726010 ($4.6854), two EG1218 / C273394
($3.0520), and two BM07B-GHS-TBT(LF)(SN) / C5305068 ($1.2496). J1 needed exact-ID
search; re-uploading the CPL reset that match, which was restored. Front exact
matches: two 150141M173100 / C5342281 ($1.5164), two BM06B-GHS-TBT(LF)(SN) /
C189892 ($0.6018), and five B3U-1000P / C231329 ($0.9330, including excess over
the two fitted units). All rows were selected; no omission or substitute accepted.

The initial controls preview exposed a B3F centroid mismatch. Replaced only its
CPL with [controls r2](supplier-placement-candidates/README.md), SHA-256
`e9d49c056b6b012c332c8ca27a95382bf7f17ff4d8ce052d39db43d77efc5de9`.
All three button centers now align with their native four-hole patterns in the
supplier preview. J1/SW4, BOM, Gerbers and native geometry remain unchanged.
The front preview shows SW1 and J1 bodies, but D1 has no rendered LED body; it
cannot prove RGB pin orientation. Neither draft is a full placement sign-off.

## Next work

All four archives have been uploaded. Resolve U3's supplier model/placement
origin discrepancy and missing-model orientation checks. Finish amplifier/pad,
stencil/via/stackup, pin/rotation, rail clearance,
external-parts and first-power dispositions. Final quantities, services/exclusions,
shipping/tax and exact totals still precede Erik's purchase approval.
