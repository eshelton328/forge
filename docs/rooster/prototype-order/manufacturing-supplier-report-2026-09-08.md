# Rooster manufacturing supplier report

**Cube + Beacon prototypes | September 8, 2026 | Austin, Texas 78704**

## Recommendation

**Keep JLCPCB as the current baseline. Obtain comparable PCBWay and MacroFab offers before deciding to move.** PCBWay is the most relevant alternative to investigate for flexible turnkey sourcing; MacroFab is the most relevant North American comparison. Seeed Fusion and Screaming Circuits provide useful additional benchmarks. This is an engineering assessment, not a finding that one supplier has lower measured defect rates.

The scope is PCB fabrication, component procurement, assembly, inspection and delivery. The separate [RTC comparison](rtc-alternatives-2026-09-08.md) covers component manufacturers. Full product assembly, enclosures, batteries and certification are outside the PCB price comparison.

| Supplier | Why consider it for Rooster | Main decision uncertainty |
| --- | --- | --- |
| JLCPCB | Four actual draft builds already prepared; exact five-fabricated/two-assembled scope demonstrated | RTC sourcing, placement reconciliation and complete delivered price |
| PCBWay | Turnkey, consigned and mixed sourcing; both-side SMT and through-hole work | Exact two-assembly quantity, complete BOM quote and process acceptance |
| MacroFab | North American manufacturing network, distributor sourcing, first-article images and order tracking | Assigned factory, actual price, schedule and country of origin |
| Seeed Fusion | Turnkey sourcing beyond its local library; very small assembly runs | Non-library sourcing time and acceptance of our via-fill specification |
| Screaming Circuits | US prototype assembly from one board; bare boards can be sourced through ASC Sunstone | Custom fabrication fit, complete turnkey cost and optional testing scope |

Supplier capabilities are documented in [PCBWay's assembly specification](https://www.pcbway.com/assembly-capabilities.html), [MacroFab's capabilities](https://www.macrofab.com/capabilities), [Seeed's service page](https://www.seeedstudio.com/pcb-assembly.html) and [Screaming Circuits' FAQ](https://www.screamingcircuits.com/faq). Capabilities do not constitute acceptance of our files.

**What we know financially:** JLCPCB's dated incomplete manufacturing estimate is **$791.07**: $242.90 fabrication, $138.55 priced components, and $409.62 assembly services. RTCs and associated fee changes, shipping, import charges, sales tax and external hardware remain excluded. There is no comparable project-specific offer from the other suppliers, so a defensible cheapest-supplier ranking is not yet possible. [Recorded draft evidence](quote-progress.md)

Research used current official supplier pages and project records. Public claims are identified as such; no factory audit, delivered Rooster sample comparison or independent yield dataset was available. No supplier messages, RFQs, new design uploads, orders or payments were submitted for this report.

<!-- pagebreak -->

## 1. The build every supplier must quote

The baseline is **five fabricated and two assembled finished boards per design**: 20 fabricated PCBs, of which eight are assembled, plus 12 spare bare PCBs. The eight assemblies provide two complete Cube + Beacon PCB sets. Board counts must refer to finished boards, not manufacturing panels. [Source inventory and service audit](jlcpcb-preflight.md)

| Board | Layers / finished size | Fitted parts per board | Required assembly |
| --- | --- | ---: | --- |
| Cube main | 4 / 64 x 56 mm | 111 | Top SMT plus through-hole J4 |
| Cube controls | 2 / 27 x 34 mm | 5 | Rear SMT connector, front through-hole switches |
| Cube front | 2 / 24 x 10 mm | 3 | SMT on both sides |
| Beacon | 4 / 64 x 56 mm | 88 | Both-side SMT and through-hole parts on both sides |

This is **207 fitted references per set, 414 placements across two sets**, before procurement attrition. Main R11 remains DNP. A quote for a single flat board with top-side SMT alone is not equivalent.

The large boards require the reviewed 1.6 mm four-layer construction, 1 oz outer and inner copper, ENIG and the specified epoxy-filled, copper-capped vias. The current JLCPCB construction is JLC041611-7628 with TG155. Other suppliers must propose and document their actual equivalent stackup; the JLCPCB stackup identifier is not portable. Native USB routing remains a disclosed prototype test risk, not certified 90-ohm routing. [Stackup disposition](stackup-review/README.md)

The fill specification covers **255 main and 199 Beacon holes** while preserving component and mounting holes. It is more specific than a generic "plugged vias" checkbox. Tiny-board rails, panelization and depaneling must preserve finished outlines, antenna clearance, connector access and mechanical fit. [Via specification and maps](via-process/README.md)

The full BOM must retain both RTCs per set. The exact QC RTC is missing from current JLCPCB warehouse matching; an approved alternative grade or different clock is a separate engineering/sourcing decision. The purchased LD2410C radar module, OLED, speaker, holders, cells and harnesses are separate from the fitted PCB BOM. J3 on the Beacon orders the radar socket, not the radar module. [External inventory](external-parts.md)

**Transfer caution:** use manufacturer part numbers, native pin maps and complete drawings. JLCPCB-specific placement corrections are not automatically correct in another supplier's coordinate/rotation convention. Require a new placement review; do not alter native geometry merely to match a rendered model.

<!-- pagebreak -->

## 2. What the current JLCPCB cost actually contains

The figures below come from the September 7-8 draft observations, not a new settled checkout. Large-board previews omit unavailable U5 RTCs. [Full quote record](quote-progress.md)

| Design | Fabrication / options | Priced components | Assembly services* | Manufacturing subtotal |
| --- | ---: | ---: | ---: | ---: |
| Main | $99.41 | $55.08 | $102.82 | $257.31 |
| Controls | $22.04 | $8.99 | $84.62 | $115.65 |
| Front | $22.04 | $3.05 | $75.42 | $100.51 |
| Beacon | $99.41 | $71.43 | $146.76 | $317.60 |
| **Total** | **$242.90** | **$138.55** | **$409.62** | **$791.07** |

*Assembly services exclude components and include the recorded rail-removal adjustments. Component charges can include supplier minimums/attrition; they are not an exact installed-parts retail BOM valuation.*

<!-- cost-chart -->

The services subtotal contains **$178.92 setup, $49.26 stencils, $119.34 feeders, $32.84 fixtures and $29.26 other services**. These sum to $409.62. Setup, stencils, feeders and fixtures alone are $380.36, or approximately 48% of the total. This explains why a very small run can cost far more per usable set than a future volume order. JLCPCB's [current fee schedule](https://jlcpcb.com/help/article/pcb-assembly-price) confirms that Standard service charges separately for these operations; advertised entry prices do not describe this build.

The two small Cube boards together cost **$216.16**, despite only **$12.04** in priced components. Their fabrication and assembly processing dominate. Requesting a supplier-designed family panel is worth pricing, if it preserves the design and finished quantities. The four-layer main/Beacon and two-layer controls/front are different fabrication families; putting everything on one panel is not an equivalent no-change quote. No panel savings are assumed or implemented here.

Dividing $791.07 by two yields **$395.54 per assembled PCB set with spare bare boards allocated**. That is neither the price of parts alone nor a production unit cost. It excludes external modules, enclosure work and delivery costs.

For each alternative, compare **manufacturing subtotal + freight + import/clearance charges + sales tax**, with each line shown separately. Compare total cash outlay for the same scope; do not compare a five-set quote's per-unit figure to this two-set prototype run. No competitor dollar estimate has been invented from a promotional assembly price.

<!-- pagebreak -->

## 3. JLCPCB and PCBWay

### JLCPCB: strongest evidence of current build fit

Our real drafts establish Standard-service intake of both-side and through-hole work, the five/two quantities, processing rails and the large-board fill/cap option. Most fitted parts already match. Staying preserves useful preparation, but the remaining RTC and placement issues still need resolution. These are not evidence of defective delivered boards; none has been built. [Preflight](jlcpcb-preflight.md)

Its published inspection flow includes solder-paste inspection, optical inspection, visual inspection and X-ray. **Assembled-board flying-probe tests and functional tests are customized services.** Our bare-board Kelvin/flying-probe selections must not be described as a passed powered PCBA test. The final order should identify X-ray coverage and charges for hidden joints. [Inspection scope](https://jlcpcb.com/help/article/smt-inspection-and-testing-capabilities)

Preordered components must arrive at JLCPCB before assembly ordering. Its customer-supplied-parts policy covers soldering workmanship but excludes intrinsic component quality; procurement-agent sourcing also does not transfer responsibility for our part selection. These details matter if using distributor RTCs. [Preorder terms](https://jlcpcb.com/help/article/pre-ordering-parts-terms-conditions), [after-sales scope](https://jlcpcb.com/help/article/common-pcba-after-sales-issues-and-faq)

**Assessment:** retain as baseline, without treating its incomplete subtotal as the lowest delivered offer or its catalog match as engineering approval.

### PCBWay: first alternative to investigate

PCBWay advertises complete turnkey sourcing, partial turnkey and consigned parts, plus mixed SMT/through-hole and double-sided assembly. Its sourcing page names authorized distributors including DigiKey and Mouser. That is relevant to the RTC bottleneck, but availability, intake time and exact MPN acceptance need a real offer. [Service and sourcing](https://www.pcbway.com/pcb-assembly.html)

Its assembly capability page lists a five-piece minimum, while broader OEM marketing advertises no minimum. **Two assembled boards per design are unconfirmed.** Request the baseline and separately identify any mandatory five-assembly offer. The published assembly clock starts after parts and data are ready; the fastest advertised turn does not include an unresolved component purchase. [Assembly requirements](https://www.pcbway.com/assembly-capabilities.html), [broader OEM offer](https://www.pcbway.com/oem/rapid-production.html)

Published quality capabilities include AOI, X-ray, ICT and customer-procedure functional testing. Specify the applicable workmanship class/revision and actual inspection scope in the offer; do not rely on the site's self-reported yield percentages as comparable independent evidence. [Testing capabilities](https://www.pcbway.com/assembly-capabilities.html)

**Assessment:** a credible sourcing/process alternative, not yet proven cheaper, faster or higher quality for Rooster. Switching requires a fresh BOM/placement/process review.

<!-- pagebreak -->

## 4. North American and additional alternatives

### MacroFab: strongest North American comparison

MacroFab publishes support for small orders, mixed and double-sided assembly, epoxy-filled/capped vias and component consignment. It describes Class 2 inspection, Class 3 availability, first-article images, AOI and hidden-joint X-ray, with a one-year workmanship guarantee. Its stated one-square-inch minimum billable area is relevant to the 24 x 10 mm front board; confirm actual billing. [Capabilities](https://www.macrofab.com/capabilities)

Its platform connects distributor stock, pricing and inventory across builds. This could make RTC procurement and repeat revisions easier to manage. [Platform](https://www.macrofab.com/platform)

The factory network includes US and Mexican operations; Houston headquarters does not establish where our boards will be fabricated, assembled or shipped. Request those locations and import terms explicitly. [Manufacturing footprint](https://www.macrofab.net/)

**Assessment:** worth a complete quote for supply-chain handling, support and production continuity. Neither a lower delivered price nor a faster Rooster delivery is established. Older rapid-turn announcements and staging-site pages are not accepted as a current project schedule.

### Seeed Fusion: useful third turnkey offer

Seeed advertises no assembly minimum, both-side/mixed assembly, engineering DFA review, DigiKey/Mouser-linked sourcing, IPC Class 2/3 capability and free PCBA shipping. The service page's seven-working-day claim depends on local OPL sourcing. Its support guidance describes roughly 20 business days for non-OPL builds, subject to component and fabrication needs. Treat that as published guidance, not a committed Rooster arrival date. [Service](https://www.seeedstudio.com/pcb-assembly.html), [lead-time guidance](https://support.seeedstudio.com/knowledgebase/articles/925059-how-long-do-fusion-pcb-pcba-orders-take)

**Assessment:** useful if it can quote the exact BOM and filled/capped-via process competitively. Confirm inspection inclusions, Austin freight eligibility, customs charges and claim terms. The broad free-shipping statement does not establish zero import cost.

### Screaming Circuits: US prototype assembly benchmark

Screaming Circuits accepts one-board prototypes and can source bare boards through ASC Sunstone. Its stated standalone minimum dimension is 0.75 inch per side, so our 10 mm front-board width needs a handling/panel solution. Its standard process includes hidden-joint X-ray and Class 2 inspection; bespoke functional testing is outside standard services. It ships via UPS by default. [FAQ](https://www.screamingcircuits.com/faq)

**Assessment:** useful when direct US assembly support is valuable. Confirm the bare-board partner's exact fill/cap, drill and stackup acceptance. Its standard online quote may require custom review for this scope; custom quotes are advertised within three business days. [Quoting options](https://www.screamingcircuits.com/capabilities/sourcing-solutions)

<!-- pagebreak -->

## 5. Manufacturing time and shipping to Austin

**Earliest usable arrival depends on parts readiness and engineering approval, then fabrication/assembly/inspection and transport.** Different suppliers start their clocks at different points. Simultaneous procurement and fabrication can overlap; a "24-hour assembly" claim is not a 24-hour order-to-door promise.

| Supplier | Schedule evidence | Shipping comparison |
| --- | --- | --- |
| JLCPCB | Current large-board drafts: PCB 3 days; assembly 5-6 days, plus 1 advanced-option day for main / 3 for Beacon | Austin-specific freight and delivered quote not completed; RTC receipt still precedes assembly ordering |
| PCBWay | Assembly from 24 hours to weeks, after all parts/files are ready | Published DHL/UPS guidance 3-7 business days; FedEx 4-7; slower global lines 8-13. Global guidance, not a 78704 commitment |
| MacroFab | No project-specific accepted schedule | Confirm factory, dispatch location, service and border leg; North American does not automatically mean US domestic |
| Seeed Fusion | Local-library builds advertised from 7 working days; non-library guidance around 20 business days | Free-PCBA-shipping claim requires confirmation for this order; duties and delivery date remain separate |
| Screaming Circuits | Assembly starts only after required materials arrive; noon receiving cutoff | Default UPS; selected service and actual origin determine Austin transit; no rate quoted |

Sources: [JLCPCB draft record](quote-progress.md), [PCBWay assembly](https://www.pcbway.com/assembly-capabilities.html) and [shipping guide](https://www.pcbway.com/shipping_method_guide.aspx), [Seeed timing](https://support.seeedstudio.com/knowledgebase/articles/925059-how-long-do-fusion-pcb-pcba-orders-take), [Screaming Circuits timing](https://www.screamingcircuits.com/faq). Unconfirmed rows deliberately contain no invented arrival dates.

For this run, request one tracked shipment containing all four completed designs and the spare bare boards. Splitting deliveries can increase freight and leave an unusable partial system. PCBWay explicitly links combined orders to a shared dispatch after the last order finishes. [Order combination policy](https://www.pcbway.com/shipping_method_guide.aspx)

JLCPCB's August 27 policy says US individual-customer shipments use DDP with import charges collected in advance. PCBWay's terms generally exclude import charges unless a duty-paid service is selected. Ask both to state freight, duties, clearance and sales tax separately even if checkout groups them. No percentage from a generic tariff table has been applied to Rooster. [JLCPCB collection policy](https://jlcpcb.com/help/article/us-tariff-policy-faq), [PCBWay shipping terms](https://www.pcbway.com/terms_service.html)

Do not assume an under-$800 exemption or tax-free Mexican origin. CBP's guidance documents changes to low-value treatment and origin requirements; classification, actual origin and the entry-date rules still matter. A US assembler can also incur imported-component costs upstream. [CBP low-value guidance](https://www.help.cbp.gov/s/article/Article-1050?language=en_US), [USMCA origin documentation](https://www.help.cbp.gov/s/article/Article-1736)

<!-- pagebreak -->

## 6. What "quality" should mean for these boards

**No evidence here supports an objective best-to-worst defect-rate ranking.** Certification logos, consumer reviews and different suppliers' self-reported yields are not a controlled comparison. The useful comparison is whether the assigned factory agrees to measurable requirements and returns evidence for our build.

The following is a recommended supplier acceptance scope, not newly claimed test results or an already agreed purchase specification. A suitable starting point is IPC-A-610 Class 2 workmanship with the applicable revision identified, plus our explicit component/process requirements. Class 3 is not automatically required for a consumer prototype; it also does not validate its firmware, battery life or shower sealing.

| Item to specify | Evidence useful for Rooster |
| --- | --- |
| Fabrication and via treatment | Approved stackup, finish and fill/cap maps; component holes remain open; bare-board electrical test scope recorded |
| Exact fitted BOM | Manufacturer part numbers, DNP list, substitutions requiring approval, attrition quantities and lot/traceability availability |
| Assembly orientation | Numbered-pin placement review of both ESP32 modules and main amplifier; keyed connectors, RGB LED and rear-side parts checked |
| Hidden solder joints | X-ray coverage and acceptance criteria for applicable ICs/thermal pads; images or report availability and extra charges identified |
| Optical/manual inspection | Both faces, through-hole workmanship, polarity and critical mechanical features; per-board identifier and inspection record |
| Material handling | Moisture-sensitive-part handling and a compatible reflow/cleaning process; no cleaning or coating that damages selected components |
| Packing and depaneling | Finished dimensions, intact antenna/connector areas, ESD packaging and protection from bending or loose hardware |
| Functional test option | Separate price, firmware/fixture responsibilities, exact procedure, voltage/current limits and per-board results |

JLCPCB explicitly distinguishes custom PCBA electrical/functional tests from process inspections. Screaming Circuits includes hidden-joint X-ray but identifies functional/mechanical testing as a separate service discussion. MacroFab publishes first-article images and Class 2 inspection. These are meaningful differences in advertised scope, but final inclusion still belongs in the quote. [JLCPCB](https://jlcpcb.com/help/article/smt-inspection-and-testing-capabilities), [Screaming Circuits](https://www.screamingcircuits.com/faq), [MacroFab](https://www.macrofab.com/capabilities)

The firmware is still being developed. For this engineering run, supplier workmanship inspection plus our planned current-limited bring-up can be appropriate; a finished production test fixture must not become an unnecessary PCB-order blocker. Basic supplier programming or power testing is an optional priced scope only when we can provide a safe, executable procedure.

Neither a better factory nor a clean AOI report resolves our unmeasured enclosed temperatures, RF performance through wet plastic, battery endurance or condensation resistance. Those remain the post-delivery ROO-012/016/017 work. Conformal coating, if later selected, needs its own material and masking review and is not a substitute for enclosure validation. [Current thermal assessment](rtc-alternatives-2026-09-08.md)

<!-- pagebreak -->

## 7. Support, rework and commercial risk

Workmanship coverage is narrower than a promise that the designed product works. Record the claim window, remedy, who pays return freight, and the treatment of customer modifications before paying. Photograph and inspect delivered boards before rework.

| Supplier | Published evidence and implication |
| --- | --- |
| JLCPCB | Customer-supplied component quality is excluded; assembly-process responsibility remains. Quote-specific claim/remedy terms still need confirmation. |
| PCBWay | Return policy states 14 days to apply for return and one month to object to quality. Treat these as distinct provisions; document issues promptly rather than assuming a longer generic warranty. |
| MacroFab | Advertises one-year workmanship coverage. Its agreement also allocates component minimum-buy/excess-inventory liability to the customer; obtain the applicable order terms. |
| Seeed Fusion | No sufficiently specific current Fusion PCBA workmanship/remedy clause was established in this screen; request it with the quote. Retail return or membership policies are not substitutes. |
| Screaming Circuits | FAQ states 30 days after delivery for workmanship, repair or assembly-labor refund at its discretion; customer modifications void the stated warranty. |

Sources: [JLCPCB after-sales](https://jlcpcb.com/help/article/common-pcba-after-sales-issues-and-faq), [PCBWay return policy](https://www.pcbway.com/return_policy.html), [MacroFab guarantee](https://www.macrofab.com/capabilities) and [service agreement](https://www.macrofab.com/legal/msa), [Screaming Circuits warranty](https://www.screamingcircuits.com/faq). This records published scope, not a negotiated remedy.

A short shipping route can make physical returns easier, but build location and responsibility for repair freight matter more than headquarters. Likewise, a longer warranty has limited value if it covers only labor and we have already modified the board. No monetary value has been assigned to these differences without actual terms.

## 8. Supplier selection and next steps

Use a **quote priority**, not a fabricated numerical supplier score:

1. **JLCPCB:** close the existing RTC and placement questions; retain the complete manufacturing packet as the baseline.
2. **PCBWay:** request the same four-design scope, exact sourced RTC, via process, inspection and duty-paid delivery. Verify whether two assemblies per design are accepted.
3. **MacroFab:** price the same scope with the actual North American factory/origin disclosed and first-article/inspection deliverables stated.
4. **Seeed or Screaming Circuits:** pursue if the first comparisons expose poor sourcing, schedule or support value; both are credible options, not prerequisites to deciding.

Choose among suppliers that accept the exact build using **complete delivered cost, parts-ready date, credible ship date and inspection evidence**. Existing JLCPCB preparation reduces remaining effort; a final price winner still requires comparable quotes.

<!-- pagebreak -->

## 9. Reviewable quote request and completion criteria

The companion [unsent comparison request](supplier-comparison-enquiry-draft.md) translates this report into a consistent request. It authorizes neither purchases nor substitutions and has not been sent. The original placement enquiry also remains unsent as Erik requested.

| Required quote field | Completion criterion |
| --- | --- |
| Scope | Five fabricated/two assembled finished boards for each of four designs; eight assemblies plus 12 spare bare boards |
| Manufacturing | Every fabrication option and manual/both-side operation accepted, with deviations explicitly listed |
| Parts | Full BOM priced, four fitted RTCs plus required attrition included, source/arrival dates and substitution policy stated |
| Quality | Workmanship class/revision, optical/X-ray scope, manual placement review and any optional powered test identified |
| Cost | Separate fabrication, parts, setup, stencil, feeders/fixtures, assembly, inspection, freight, import/clearance and sales-tax amounts |
| Timing | Procurement-ready, fabrication, assembly, review and dispatch milestones; carrier/service and Austin delivery estimate |
| Commercial | Quote validity, unapproved extras, claim window, remake/repair scope, return freight and excess-parts ownership |
| Release | Exact accepted file hashes; manual CAM/placement approval before production; explicit purchase approval from Erik |

Optional alternatives must be separate: supplier-designed family panels without changing finished boards; five assembled sets if required or economically attractive; and basic programming/functional testing. An alternate must not silently replace the baseline quantity or quality scope.

### Work that can proceed independently

- ROO-010 supplier/BOM/placement review can proceed alongside ROO-011 diagnostic firmware and test run sheets.
- Component sourcing and manufacturing acceptance can progress in parallel, but purchasing remains subject to Erik's approval.
- External harness preparation and enclosure fit work can continue during sourcing/fabrication.
- Month-long Cube endurance, wet-use qualification and production cost optimization remain later milestones.

### Evidence limits and records

Official web sources were checked September 8, 2026. Alternative suppliers have not quoted or accepted Rooster files. Delivered prices, dates and measured quality remain unresolved. See [quote progress](quote-progress.md), [assembly preflight](jlcpcb-preflight.md), [placement reference](placement-review/README.md) and [order readiness](order-readiness-2026-09-08.md) for the supporting project records.

The report retains native revision `090b207` / fabrication candidate `090b207-r1`. Documentation changed; PCB sources, component selection and purchase status did not.
