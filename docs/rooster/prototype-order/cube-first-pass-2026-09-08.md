# Cube-first prototype order plan - September 8, 2026

Erik prefers ordering the Cube first, testing it and continuing firmware before buying the Beacon boards. The immediate purchasing scope is **alec-main, alec-controls and alec-front**. Beacon preparation and the earlier four-design comparison remain useful records; Beacon manufacture is deferred to a later decision. No supplier draft, PCB source, order or payment changed with this planning update.

## Supplier recommendation

**Use JLCPCB for the first Cube run if the remaining sourcing and placement questions can be closed.** Existing drafts cover the required quantity, fabrication options, through-hole work and both-side assembly. The [supplier report](manufacturing-supplier-report-2026-09-08.md) found no demonstrated quality advantage that warrants transferring this build, and no equivalent competitor quote establishes a lower delivered cost. This is a practical recommendation, not a claim that JLCPCB is universally best or cheapest, and not a purchase authorization.

JLCPCB publishes solder-paste, optical, visual and hidden-joint X-ray inspection; confirm the applicable coverage in the order. These are suitable process controls to investigate for an engineering prototype, not proof that the designed Cube works. [Inspection scope](https://jlcpcb.com/help/article/smt-inspection-and-testing-capabilities)

PCBWay is the first fallback if RTC procurement, manufacturing acceptance or the final price becomes unacceptable. It supports turnkey/partial/consigned sourcing, but its published assembly minimum is five, so a two-assembly offer still needs confirmation. [PCBWay capabilities](https://www.pcbway.com/assembly-capabilities.html) MacroFab remains an option for a North American workflow and inspection records, without evidence yet that its price or schedule improves this first pass. [MacroFab capabilities](https://www.macrofab.com/capabilities)

## Cube-only estimate

Retain the previously selected planning quantity: **five fabricated / two assembled finished boards per design**. For three Cube designs that is 15 fabricated, six assembled and nine spare bare boards, supplying **two Cube PCB sets**. This is not a quote for one assembled Cube.

| Board | Dated manufacturing estimate |
| --- | ---: |
| Main | $257.31 |
| Controls | $115.65 |
| Front | $100.51 |
| **Cube-only subtotal** | **$473.47** |

The subtotal separates **$143.49 fabrication/options, $67.12 priced components and $262.86 assembly services**. It excludes both required RTCs, resulting fee changes, display/speaker/holders/cells/harnesses/enclosure, freight, tariffs/clearance and sales tax. Costs are derived from existing draft observations in [quote progress](quote-progress.md); they are not a refreshed Cube-only checkout. Removing Beacon defers $317.60 of the earlier manufacturing estimate. A later Beacon shipment may add freight, so that is not a lifetime project saving.

## Remaining order work

1. Resolve and price **two fitted main-board RTCs plus the supplier's procurement/attrition requirement**. The existing five-part QC preorder is historical, unpaid and unapproved; its quantity/terms must be re-evaluated for the Cube-only proposal. Do not assume sourcing minimums disappear. QA-grade intake remains an investigation, not an applied substitution.
2. Resolve main U3 ESP32 placement datum and U6 amplifier pin orientation; finish the controls/front and connector/polarity reviews. The existing technical enquiry stays unsent. A smaller scope does not close main-board findings.
3. Refresh complete BOM matching, manufacturing services and Cube-only external-item scope. Obtain freight, import fees and tax separately, retaining manual CAM/placement approval.
4. Present the exact three-design scope and total for Erik's purchase approval. Further supplier research is optional unless the current supplier fails a concrete requirement.

Cube diagnostics can exercise programming, supply rails, RTC/alarm wake, audio, buttons, LED and the separately connected display. Any simulated Beacon messages or development-board peer are test aids to implement, not existing verification. Physical Beacon sensing, paired radio performance and complete alarm/presence behavior remain later tests. Keep current-limited bench bring-up and the existing battery-use limits; no power or functional test has been executed by this planning decision.
