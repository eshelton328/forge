# Cube supplier quotes — September 8, 2026

**No complete alternative quote yet meets the exact build and confirmed RTC-sourcing requirement.** Seeed accepted the full RFQ through its manufacturing contact form. The full package was also emailed to MacroFab and PCBWay, with Gmail confirming both messages sent. Manual pricing and sourcing responses are pending. No order, paid procurement or production approval was submitted.

This record supersedes the earlier four-design enquiry scope. Quote **alec-main, alec-controls and alec-front only**, each with **five fabricated / two fully assembled / three bare spares**: two complete Cube PCB sets, six assembled boards and nine bare boards. Beacon manufacture is deferred. Different supplier minimums must be separate alternatives.

## What the current prices actually cover

USD; manufacturing is separated from freight, tariffs/clearance and sales tax. None of these figures is a complete approved order price.

| Supplier | Observed amount | Included scope | Missing or incompatible scope |
| --- | ---: | --- | --- |
| JLCPCB | **$473.47 manufacturing estimate** | Three designs, 5 fabricated / 2 assembled each; current main fill/cap; dated drafts | RTCs and related fee changes; remaining placement review; external hardware; freight, tariffs/clearance and tax |
| PCBWay | **$29 assembly-service calculator** | Main only, quantity 2, 42 unique parts, 110 SMT and 1 THT inputs | Bare PCBs, all components, custom services, controls/front and all delivery charges; not a complete offer |
| MacroFab | **$1,480.22 before tariff**, plus **$87.52 tariff** | Preliminary two-main-board, 30-day platform estimate; displayed total $1,567.74 | Unavailable BOM items, unapproved automatic matches, custom via/stackup acceptance, controls/front, three additional bare mains, freight and sales tax |
| Seeed | **Pending** | Full three-design RFQ submitted | All project-specific prices, RTC sourcing and process acceptance pending |
| OSH Park | **About $64.52 bare fabrication only** | Three copies of each design under published standard area pricing | Main does not fit the standard process; no components or turnkey assembly; quantity differs |

JLCPCB's subtotal is **$143.49 fabrication/options + $67.12 priced components excluding RTCs + $262.86 assembly services**. It comes from the [dated draft record](../quote-progress.md), not a refreshed checkout. External OLED, speaker, battery holders/cells, cables and enclosure are outside every PCB quote here.

PCBWay's current [assembly calculator](https://www.pcbway.com/quotesmt.aspx) offers quantity 2 and displays $29 for its 1–20 quantity band. This is newer evidence than the earlier report's five-assembly-minimum statement; actual two-assembly eligibility for our mixed/both-face scope remains unconfirmed. Its sales agent said a quote normally follows complete online file submission in 1–2 days. That does not establish a response deadline for the email route.

## RTC: production-intent quotation candidate

The quote BOM explicitly selects **Micro Crystal RV-3028-C7 32.768KHZ 1PPM-TA-QA**, manufacturer code **203603-MG01**, LCSC **C3304278**, for main U5. Erik asked to quote what we would use in production. QA is the recommended candidate for these offers, with final temperature/clock-drift qualification still pending. The native schematic/BOM still names QC: no native component, footprint, driver or PCB was changed. No other BOM substitution was authorized.

The shared manufacturer datasheet specifies the package/interface and −40 to +85 °C operating range; the ±1 ppm figure is at 25 °C. This is **not a temperature-compensated RTC**, and automotive qualification does not establish enclosed clock accuracy. [Manufacturer datasheet](https://www.microcrystal.com/fileadmin/Media/Products/RTC/Datasheet/RV-3028-C7.pdf)

Live DigiKey UI showed **6,011 QA units available**, $2.66 at quantity 1, $1.982 at 10 and $1.6239 at 100. Two fitted parts at retail would be $5.32 before attrition, fees and logistics. This is distributor inventory, not reserved factory supply. [Exact DigiKey listing](https://www.digikey.com/en/products/detail/micro-crystal-ag/RV-3028-C7-32-768KHZ-1PPM-TA-QA/10500185)

MacroFab matched the exact QA MPN and displayed:

| RTC row field | Observed value |
| --- | ---: |
| Vendor stock | 25,123 |
| Lead-time field | 28 weeks |
| Fitted requirement | 2 |
| Procurement overage | 2 |
| Parts charge for four units | $12.98 |
| Placement labor | $0.07 |
| Tariff | $1.06 |
| Combined row total | $14.11 |

The vendor identity was not displayed. Stock and a long lead-time field appeared together, so the manual request explicitly asks for the actual authorized/traceable source, immediately available quantity, procurement quantity and factory-ready date. The row tariff is already part of the platform's overall tariff; **do not add it twice**. No supplier has confirmed allocation or procurement.

## MacroFab preliminary main-board estimate

Main Gerbers and the Excel quote BOM were imported into platform PCB **100y2ghx, version 1**. The import covers **111 fitted references / 42 BOM groups**; R11 remains absent/DNP. Quantity was verified as **2**. Navigation without the quantity parameter can default to five; preserve the recorded quantity when revisiting.

The platform recognizes 64 × 56 mm and four layers. Its specifications summary shows **green mask, white silk, ENIG, 1 oz inner and outer copper**. The custom via map and final stackup have **not** been accepted or configured into a qualified platform quote. The default summary's “no custom quote” indication therefore does not approve our RFQ process.

| 30-day economy estimate line | USD |
| --- | ---: |
| NRE | $472.00 |
| Labor | $202.00 |
| PCB fabrication | $405.91 |
| Per-order fee | $250.00 |
| Components, incomplete | $150.32 |
| Tariffs | $87.52 |
| **Displayed total** | **$1,567.74** |
| **Displayed total minus tariffs** | **$1,480.22** |

Individual displayed non-tariff lines sum to $1,480.23; the one-cent difference reflects displayed rounding. Use the platform total when comparing. The 30-day option displayed an estimated October 21 ship date, contingent on parts, data and process readiness; it is not a committed delivery date.

Other displayed two-main-board options were **10 days / $4,812.74**, **16 days / $2,329.46**, and **25 days / $2,076.97**, including their platform tariffs. These share the same incomplete scope and should not be treated as full Cube alternatives.

The BOM view reports **3 errors and 9 unavailable items**; Quote & Order reports **10 components missing availability**. These are separate UI warnings, not resolved quantities. Automatic matches also changed displayed manufacturer/MPN text for some rows, including D1, R34/R35 and R42/R44. Punctuation normalization is not proof of equivalence. The manual RFQ requires exact attached MPNs, an explicit exception list and no silent substitutions.

Support agent Eric directed the request to the quoting team by email and agreed to forward the chat. The full package was sent. Neither the headline estimate nor the RTC stock display establishes an accepted complete build.

## OSH Park process and price check

OSH Park's [standard four-layer service](https://docs.oshpark.com/services/four-layer/) is $10 per square inch for three boards. It specifies **0.254 mm minimum drill**, **0.5 oz internal copper** and no filled/plated vias. Current main has 0.20 and 0.25 mm holes, requires 1 oz internal copper and the specified **255 epoxy-filled, planarized, copper-capped holes**. Its standard service therefore does not meet this main-board specification. Enlarging drills, changing copper or removing fill/cap would require engineering review and new fabrication files.

The [two-layer service](https://docs.oshpark.com/services/two-layer/) is $5 per square inch for three boards. Using finished outlines, before any quote-specific rounding:

| Design | Area | Rate for three boards | Calculated charge |
| --- | ---: | ---: | ---: |
| Main, 64 × 56 mm | 5.5552 in² | $10/in² | $55.55 |
| Controls, 27 × 34 mm | 1.4229 in² | $5/in² | $7.11 |
| Front, 24 × 10 mm | 0.3720 in² | $5/in² | $1.86 |
| **Three copies of each** | | | **About $64.52** |

Six of each would be approximately **$129.05** using unrounded area arithmetic. These are calculations, not uploaded accepted quotes. Three-copy pricing means nine bare boards, not three assembled Cube units. OSH Park's advertised service does not provide the complete turnkey assembly and RTC sourcing requested here. A separate assembler would need to quote parts, attrition, setup, assembly, inspection and inter-supplier transport, after resolving fabrication fit. It is not a like-for-like alternative for the current files.

## Submissions and file identity

| Supplier | Action and observed confirmation | Remaining status |
| --- | --- | --- |
| Seeed | Submitted full ZIP through the [contact form](https://www.seeedstudio.com/contacts), category PCB/PCBA Manufacturing Enquiries; success page said the form was successfully submitted | No visible ticket number; human response and pricing pending |
| MacroFab | Full ZIP emailed to support@macrofab.com, September 8 at 1:58 PM Central; Gmail confirmed sent and the sent message contains one attachment; support chat notified | Full three-design manual quote and sourcing confirmation pending |
| PCBWay | Full ZIP emailed to service@pcbway.com, September 8 at 2:00 PM Central; Gmail confirmed sent and the sent message contains one attachment; sales chat notified | Sales agent confirmed the email route and forwarding to a sales representative; complete quote pending |

PCBWay chat could not accept the files or provide a quote; its attachment attempt did not deliver the ZIP. The email contains the complete file package. The sales agent subsequently confirmed this email route, said the request will be forwarded to an appropriate representative, and explained that PCBWay will create an account from the contact email and submit the inquiry files there so the quote can be viewed in its cart. Supplier account/inquiry creation and the eventual quote were not yet observed. No online order or paid cart was submitted. Route confirmation is distinct from technical acceptance or a priced offer.

The [supplier package](rooster-cube-quote-package.zip) is **405,508 bytes**, SHA-256 **`b7e2f0fa6012e868caf0c8489ba017b125b132429544adb5c8c8317dac1afd77`**. Its 19 members include the detailed [RFQ](RFQ.md), three unchanged Gerber archives, CSV/Excel quote BOMs, native placement references, main via instructions and [manifest](manifest.json). The three boards total 119 fitted parts per Cube / 238 across two assemblies of each design. Only the quote BOM's main U5 changes to QA; the native source remains `090b207` / fabrication candidate `090b207-r1`.

The ZIP is the immutable submitted technical packet. This internal status report was added afterwards and is **not inside it**. Do not rebuild that ZIP with supplier prices, private email links or unrelated project records. Private sent-message links and the contact address are retained in Obsidian.

CSV/Excel quantities and reference coverage were checked; all three Excel BOMs were rendered and visually inspected. File hashes and archive contents were verified. This was documentation, quotation and sourcing work, not a new PCB design or physical test.

## Decision and next steps

Retain JLCPCB as the working baseline. MacroFab's preliminary estimate does not support switching on price, and OSH Park's standard service does not fit the current main board. PCBWay and Seeed may still offer a useful complete alternative; neither has returned one.

For each reply, verify all three designs and delivered board counts; exact available RTC source and attrition; complete exact-MPN BOM or explicit exceptions; fill/cap, stackup, both-face and THT acceptance; workmanship/inspection and rework scope; itemized manufacturing, freight, tariffs/clearance and sales tax; and credible sourcing/production dates. Then compare complete offers and present the exact proposed purchase to Erik.

The existing main U3 datum, U6 pin orientation and remaining controls/front placement checks still need resolution before release. The original JLCPCB placement enquiry remains **unsent**, as requested. The old QC preorder remains unpaid and unapproved. ROO-010 remains Active and ROO-014 remains blocked on a complete reviewed package and explicit spending approval.
