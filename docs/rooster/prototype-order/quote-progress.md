# JLCPCB quote progress — September 7–8, 2026

**No complete four-board landed quote, paid reservation, payment or submitted order exists.**
All four signed-in drafts now contain Gerbers, BOMs and complete placement files.
Main has **41 of 42 BOM groups confirmed** and Beacon **37 of 38**; the remaining
group in each is the unavailable RTC. Their incomplete price previews exclude it.
Erik must explicitly approve the exact items, quantities and total before any
order or paid parts procurement.

September 8: [stackup/USB requirements](stackup-review/README.md) now recommend
the named JLC041611-7628 construction for the main/Beacon prototype quotes.
The native USB routing is retained as a disclosed functional-test risk; it has
not been certified at 90 Ω. The current via attachments were reproduced exactly
and committed as `b3818f9`; stackup/USB evidence is in `d957338`. Main and Beacon
now both have current uploads and revised prices, recorded below.

## Current four-design estimate

| Design | PCB fabrication/options | Assembly preview | Rail-removal adjustment outside preview | Estimate including rail removal |
| --- | ---: | ---: | ---: | ---: |
| Main | $99.41 | $157.90 | Included | $257.31 |
| Controls | $22.04 | $93.61 | Included | $115.65 |
| Front | $22.04 | $76.17 | $2.30 | $100.51 |
| Beacon | $99.41 | $215.89 | $2.30 | $317.60 |
| **Total** | | | | **$791.07** |

Each design is five fabricated / two assembled. Main/Beacon now use the actual
filled-and-capped draft settings. Controls/front retain the September 7 price
observations. This sum includes the separately listed advanced-option charges;
it is **not a settled cart or landed quote**. RTCs, related assembly-fee changes,
shipping, tax and external modules/harnesses remain excluded. Do not add the
country-only shipping estimate or treat the RTC preorder as already purchased.

## September 8 — current Beacon draft, 090b207-r1

Saved title: **alec-sensor 090b207 - INCOMPLETE RTC - REVIEW ONLY**. Its private
draft URL is recorded in ROO-010. The old Beacon draft is historical.

| Uploaded input | SHA-256 |
| --- | --- |
| `fabrication-candidates/090b207-r1/alec-sensor/alec-sensor-gerbers.zip` | `ec6e25d9eb399ee1a5e95eb94d4714c771c721c467dbd2f87d9307b50056540f` |
| Adjacent `alec-sensor-bom.csv` | `c7a9010b88b9de347d351e8ef81565ee74a5a164eebab3a9e8bcc791b92a947b` |
| `supplier-placement-candidates/090b207-r1-headers/alec-sensor-cpl.csv` | `f0f5540f6d4730df6a70341bc655e5509eb487768cac2a0f7cf5dac1813e9b6c` |

Gerber detection reports four layers / 64 × 56 mm. Selected five fabricated,
two assembled, Standard / **Both Sides**, with 74 × 70 mm supplier processing
dimensions and factory depaneling. Fabrication settings match the new main draft:
1.6 mm, green/white, FR4 TG155, 1 oz outer/inner, ENIG 1 µin, JLC041611-7628,
impedance **No requirement**, Epoxy Filled & Capped, required Horizontal
Electroless Copper Plating, 0.2 mm minimum via option, Kelvin/flying-probe tests,
regular ±0.2 mm outline tolerance. Selected button states and actual input values
were checked before saving. Both manual-review dialogs had **Do not confirm
automatically checked**. The saved PCB tab confirms Standard / Both Sides / 2.

The full BOM/CPL covers 88 fitted placements and matches **38 detected / 37
confirmed / one shortage**. U5 is exact C3019759 with two parts short; there is
no unchecked available BOM row. No substitute was selected. U5 was temporarily
excluded only to reach the incomplete price preview; it remains required by the
uploaded/native BOM and CPL. This does not authorize an RTC-free assembly.

The settled page shows **$315.30 = $99.41 PCB + $215.89 Standard assembly**.
It separately lists $2.30 depaneling and warns that some advanced options are
excluded. Including that charge gives $317.60 for comparison, subject to the
eventual cart. Assembly fees remain setup $51.12; stencil $16.42; components
(37 items) $71.43; feeders $53.55; SMT $2.17; placement review $0.45; hand
soldering $3.58; manual assembly $0.26; fixture $16.42; packaging $0.49.
PCB time is 3 days; assembly 5–6 days plus three advanced-option days, with
no rush selected. These are production estimates, not delivery dates.

This pass verifies file intake, matching and quote settings, not final placement
alignment. Existing U3/model and missing-model questions remain subject to the
native-pad comparison and manual production review. **Save to Cart was not
clicked; no PCB/parts order, payment or production approval was submitted.**

## September 8 — current main draft, 090b207-r1

A new saved supplier draft replaces the superseded main Gerbers. Its title is
**alec-main 090b207 - INCOMPLETE RTC - REVIEW ONLY**. The account-specific URL
is retained in the private Rooster note; it is a draft identifier, not an order.

| Uploaded input | SHA-256 |
| --- | --- |
| `fabrication-candidates/090b207-r1/alec-main/alec-main-gerbers.zip` | `fdf29a45b08e7f7863141c78b3ecf48b4a34069a986c37b83001055218727ae0` |
| Adjacent `alec-main-bom.csv` | `9e2f10a6fd418bff844181ae03c07c44b041786fba7198782cb7e382b9ab5507` |
| `supplier-placement-candidates/090b207-r1-headers/alec-main-cpl.csv` | `b8118c464899128b6c40f13c5f933c3c276592ff2955c50fab9680f62cd7576e` |

The supplier detects **four layers / 64 × 56 mm**. The quote retains five
fabricated and two assembled, Standard / Top Side, Single PCB, with supplier
processing dimensions **74 × 70 mm**. Native outlines are unchanged. Selected:
nominal 1.6 mm, green/white, FR4 TG155, 1 oz outer and inner, ENIG 1 µin,
**JLC041611-7628**, impedance control **No requirement**, **Epoxy Filled & Capped**,
required Horizontal Electroless Copper Plating, 0.2 mm minimum drill option,
Kelvin/flying-probe tests and ±0.2 mm outline tolerance. Named stackup selection
does not certify trace impedance. Both production-file and placement dialogs
were set to Yes with **Do not confirm automatically checked**. Factory rail
removal is Yes. The saved PCB tab confirms Standard / Top Side / quantity 2.

After processing the matching BOM/CPL, restored both PH connector rows and
selected exact J5 C5305068 (4,069 stock shown). The final BOM summary reads
**42 detected / 41 confirmed / 1 inventory shortage**; the DOM contains no
unchecked available component row. U5 still has a two-part shortfall. J4's
matched footprint now explicitly reads **Samtec_TSW-104-07-G-S_Drill1.10mm**.
As in the earlier draft, U5 was temporarily excluded only to inspect placements
and prices. Its native/uploaded BOM/CPL entries remain required. No incomplete
assembly is approved for purchase.

The settled Quote & Order page shows **$257.31 = $99.41 fabrication/options +
$157.90 Standard assembly excluding RTC**. The assembly amount includes $2.30
depaneling; all its other fees match the earlier main breakdown below. The
$20.41 fabrication increase is now confirmed on this actual new assembly draft,
not merely inferred from the separate calculator. It consists of $17.06 fill/cap
and $3.35 horizontal plating. No separate stackup fee appears. The displayed
times are PCB 3 days and assembly 5–6 days plus one advanced-option day; no rush
was selected. Shipping, tax, RTC procurement and related assembly adjustments
remain excluded. No landed total or arrival date is established.

The new 3D preview renders, but U3 still appears vertically displaced relative
to its native land pattern. Switching to 2D does not expose an authoritative
numbered-pin datum. No speculative U3 offset or U6 rotation was applied. These
placement issues remain for reconciliation against native pad coordinates and
supplier production data with manual approval. No Save to Cart, order, paid
reservation, payment, supplier outreach or production approval was submitted.

## Historical four-design comparison before the September 8 uploads

Controls and front have all fitted parts matched. The earlier four price previews and
the controls/header placement corrections are recorded below. No PCB Save to Cart
action was submitted. The estimate including separately listed rail removal is
**$750.25 before RTCs, any related assembly-fee changes, shipping, tax and external
parts**. This is arithmetic from draft pages, not a complete quote or final bill.

**Via-process correction:** the $750.25 draft estimate uses solder-mask plugging
on the large boards, which does not resolve their exposed thermal vias. The
[source-bound fill/cap specification](via-process/README.md) now calls for
Epoxy Filled & Capped on main/Beacon. A separate fabrication calculator shows
$99.41 per large-board batch versus the earlier $79.00: an indicative **$40.82
increase across both**, giving **$791.07 before RTCs, related assembly changes,
shipping, tax and external items**, if all other draft charges hold. This is
comparison arithmetic. The September 8 main/Beacon sections above now replace
this provisional calculation with actual refreshed fabrication-price previews.

Erik supplied a USA shipping destination; the postal code and account-specific
draft URL are in the private Rooster task note. Postal-code-specific shipping/tax
has not been reached. These are live UI observations from September 7; stock,
pricing and lead times may change.

## September 7 — historical main-board draft

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
  ±0.2 mm outline tolerance and flying-probe test. The recorded Plugged setting
  is superseded by the fill/cap specification above and is not release-ready.
  The 0.2 mm option requires
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

## September 8 — same-day order readiness follow-up

The [order checklist](order-readiness-2026-09-08.md) records a fresh live recheck:
main 41/42 and Beacon 37/38 BOM groups confirmed, each short two exact U5 RTCs.
The existing five-RTC cart and settled checkout still show $10.76 initial total;
no order or payment was submitted. Published preorder terms require warehouse
receipt before assembly ordering. This is a timing dependency, not merely an
extra line to add to the current incomplete price previews.

Erik asked to keep the technical enquiry unsent. The amplifier library viewer
did not provide a usable numbered map; placement remains open. The four-board
$791.07 figure above remains its dated incomplete manufacturing estimate; this
follow-up did not refresh every final manufacturing fee, shipping or tax.

## RTC procurement candidates

Four fitted RTCs are required across the two main and two Beacon assemblies,
before confirmed attrition. No alternate QA device was selected; no source
part fields changed.

| Route | Live observation | Remaining qualification |
| --- | --- | --- |
| JLCPCB C3019759 preorder | Stock 0; minimum 5. Product page estimates $11.17; the staged cart and settled checkout show **$10.76 for five** ($2.1517 each, rounded total). | Exact part and two-order quantity calculation verified; no firm date. Initial payment precedes confirmed pricing. Awaiting Erik's explicit approval; no order submitted. |
| Global Sourcing → CoreStaff | MICRO CRYSTAL **RV-3028-C7 32.768kHz 1PPM TA QC**; stock 2,190; MOQ 7; $2.9518 each; **$20.66 for seven**; **10–16 business days** | Candidate for the same QC part, with spacing/case differences in its name. Pkg field says “franchised”; actual packing/assembly intake need confirmation. Displayed attrition 0 is not final four-board allocation approval. |
| Global Sourcing → Verical | QC part; stock 13,000; MOQ 1,000; $1,812.20; 12–20 business days | Unsuitable minimum for this prototype batch; not selected. |

The full hyphenated MPN returned no Global Sourcing results; searching
**RV-3028-C7** exposed the QC offers alongside distinct QA and evaluation boards.
Two reversible **Add** attempts were made for the seven-part CoreStaff QC offer,
with an intervening visit to the Global Sourcing cart confirming it was empty.
The refreshed search still shows **Cart (0)** after the second attempt; neither
attempt produced a confirmed RTC cart line. Browser logs also contain UI errors,
but they do not establish the cause. Do not repeat Add without checking the cart
again. An existing, unselected JLCPCB-parts line for a different regulator was
left untouched. No order, reservation, RFQ, checkout submission or payment
was made. The $20.66 remains a search-page offer, not a checkout total.

The direct JLCPCB **Pre-order** button subsequently added exact C3019759 to the
JLCPCB-parts cart successfully. On September 7 the cart was reopened and still
contained five RTCs, with only that row selected. **Secure Checkout** opens a
review page; its settled merchandise and grand totals both read **$10.76**, with
no separately displayed charge. The Customer Compliance Statement remained
unchecked and **Submit Order was not clicked**. Opening this page did not place
an order. Billing/contact details are not copied into this repository; this is
parts storage at JLCPCB, not a PCB shipping/tax quote.

The exact part's **Order Guide** calculator was run with two separate orders:

| Intended order | Assembly side | Assembled PCBs | RTCs per PCB | Calculated attrition | Recommended parts |
| --- | --- | ---: | ---: | ---: | ---: |
| Main | Single-Sided | 2 | 1 | 0 | 2 |
| Beacon | Double-Sided | 2 | 1 | 0 | 2 |

It reports **Total Rec. Order Qty: 4**, with minimum-assembly fields shown as
`/`. The product's purchase MOQ of five therefore covers this calculation with
one excess part. Retain five in the draft cart. This is current calculator
evidence, not received stock; recheck allocation when parts enter the private
library and U5 is restored in both PCBA drafts. Do not click the calculator's
Add to My Part Lib again: the five-part cart row already exists.

The [RTC page](https://jlcpcb.com/partdetail/C3019759) supplies the preorder
estimate. JLCPCB says the price becomes firm only after initial payment and may
need adjustment. The reviewable proposal is **five exact RTCs at the displayed
$10.76 initial total**, held at JLCPCB for the two assembly orders, with no firm
arrival date. Both order submission and payment require Erik's approval. Any
later price increase requires a further decision, not an automatic top-up.
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

The [J4 hole correction](header-fit/README.md) now changes main's four plated
header holes from 1.00 to 1.10 mm, preserving its lands and placement. The new
[090b207-r1 candidate](fabrication-candidates/README.md) has passed native/CAM
checks and has rebound supplier CPLs. Main's original uploaded archive is
historical only; both large boards now have new drafts with current files,
fill/cap and the named stackup. The via attachments match the current source.
Prices remain incomplete until RTCs and landed charges are resolved.

All four archives have been uploaded. The [amplifier review](assembly-drawing-review.md)
now supports retaining its native copper land pattern and verifies all 17 pad
nets; rounded thermal paste coverage is 62.552%, correcting the earlier 66.1%.
The previously loaded U6 model marking differs from the native pin-1 corner; no CPL
rotation was changed in this pass. Resolve this, U3's supplier model/placement
origin discrepancy and missing-model orientation checks. The source mask decision
is now recorded: retain uniform 1:1 openings, with the actual-Gerber separation
check passing on all eight masks. The via process is specified separately.
The stackup prototype disposition is recorded. Finish
pin/rotation, rail clearance,
external-parts and first-power dispositions. Final quantities, services/exclusions,
shipping/tax and exact totals still precede Erik's purchase approval.

Record stencil constraints before purchase; actual JLCPCB stencil production
data follows the order and belongs to manual production review. The updated
drawing review records this sequencing. No order, paid parts procurement or
production approval was submitted during this review.

The latest drawing pass supports retaining main D1's LED pads and Beacon F1 for
dry prototype evaluation with the recorded current and temperature envelope.
Main J4's nonlocking header variant was distinguished from the catalog's locking
lead option in that earlier pass, which did not change source or manufacturing
files. Its fit question is now resolved by the subsequent 1.10 mm hole correction
above. The supplier viewer remained on **Generating PCB...** during
the follow-up and was returned to the BOM tab; this provides no new placement
verification or basis to change U6's rotation.

## Via-process cost comparison

The native hole audit identified 255 main and 199 Beacon holes for epoxy fill
and copper capping, including each board's twelve U3 thermal holes; all component
lead holes, USB slots and NPTH remain open. Controls/front retain tenting. The
new process attachments are bound to the unchanged r1 fabrication candidate.

Opening the main draft's **Change PCB specifications** link produced a blank
100 × 100 mm calculator, including after one reload. No defaults were saved
over the main draft. Returned to its original assembly URL and used a separate
unsubmitted calculator at 74 × 70 mm, five boards, four layers, 1.6 mm, generic
FR4 TG155, ENIG 1 µin, 1 oz outer/inner copper, 0.2 mm minimum via option,
Kelvin test, regular outline tolerance and production review. Epoxy Filled &
Capped automatically requires Horizontal Electroless Copper Plating. The
Do not confirm automatically checkbox was checked before confirming that
review preference. No Gerbers were uploaded or order/cart submitted in this
comparison. It therefore does not replace the four saved assembly drafts.

Settled fabrication breakdown: special offer $7.00; fill/cap $17.06; ENIG
$17.10; generic TG155 $3.41; inner copper $16.63; minimum via option $17.06;
Kelvin $16.76; horizontal electroless plating $3.35; production review $1.04.
Total **$99.41**. A named S1000H laminate initially added $4.01; it was changed
back to generic FR4 TG155 to match the earlier estimate. Do not carry that
intermediate $102.38 observation into the selected comparison. No assembly,
shipping, tax or RTC-price update is implied.
