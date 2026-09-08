# September 8 — shortest path to the prototype orders

**The complete four-design assembly order is not ready for payment.** The exact
RTC is still unavailable in JLCPCB's assembly matcher. Buying its preorder today
starts sourcing; it does not make main/Beacon assembly orderable tonight.

Scope remains five fabricated / two assembled finished boards for each of main,
controls, front and Beacon: two complete Cube + Beacon sets. Retain native source
`090b207`, fabrication candidate `090b207-r1`, the selected components and the
existing prototype manufacturing dispositions. No order or supplier message was
submitted in this readiness pass.

## Work in dependency order

| Step / ticket | Concrete next action | Evidence needed to close it | Current state |
| --- | --- | --- | --- |
| 1. RTC supply — ROO-010 → ROO-014 | Obtain Erik's decision on the prepared exact-part preorder, then procure only if approved. | Paid sourcing confirmation followed by enough usable received stock allocated across two main and two Beacon assemblies, including actual attrition requirements. | Five C3019759 staged at $10.76 initial total; unpaid, no firm lead time. |
| 2. Placement — ROO-010 | Reconcile U3 on both large boards and main U6 against actual numbered library/placement data. Complete RGB, keyed connector and rear-side checks. | Every affected pad maps correctly; record any justified CPL correction and refreshed preview. | Native reference ready; supplier mapping remains open. Enquiry stays unsent at Erik's request. |
| 3. Prototype power scope — ROO-013/010 | Use the documented dry, current-limited bench evaluation scope with current hardware. | Explicit retained limits, initial disconnected loads and battery-test handoff. | [Disposition recorded](prototype-power-disposition.md); no physical results claimed. |
| 4. Complete order packet — ROO-010 | Restore U5 in both drafts, refresh parts/services and complete-set external inventory, then obtain the actual combined quote. | Required fitted references, actual uploaded hashes, five/two counts, both-side/THT work, fabrication, assembly, component, shipping, tariff and tax amounts stated separately. | RTC supply and placement precede the final purchase proposal; $791.07 remains the earlier incomplete manufacturing estimate. |
| 5. Purchase — ROO-014 | Present the exact four-design order for Erik's explicit spending decision. | Approval tied to that priced scope, then submitted order IDs and file hashes. | Blocked; preparing a quote is not approval. |
| 6. Production confirmation — ROO-014 with ROO-010 | Review the supplier's generated CAM, rails, stencil and final placements. | Manual comparison to the frozen packet before production approval. | Follows order; automatic confirmation remains disabled in the large-board drafts. |

Steps 1 and 2 can progress independently. Step 3 is documented today. ROO-011
bench run sheets and diagnostic firmware can progress while sourcing/fabrication
is underway, alongside external harness preparation and enclosure fit work.
These are parallel work assignments, not newly launched tasks or agents.
Completed application firmware, enclosure finishes, wet-use qualification,
month-long Cube endurance and ROO-008 production cost optimization do not gate
this dry prototype order.

## What the supplier actually supports

JLCPCB's [preorder terms](https://jlcpcb.com/help/article/pre-ordering-parts-terms-conditions),
checked September 8, require preordered parts to arrive at its warehouse before
use in assembly orders. No documented exception allowing this complete assembly
order tonight was established. The [exact RTC](https://jlcpcb.com/partdetail/C3019759)
still shows stock zero, minimum five. The live assembly drafts still show main
41/42 and Beacon 37/38 confirmed BOM groups, each short two U5s.

The existing parts cart and settled review page were rechecked: **five
RV-3028-C7-32.768kHz-1ppm-TA-QC / C3019759, $2.1517 each, $10.76 rounded initial
total**. Only that row is selected; the unrelated converter row remains
unselected. The public product page separately estimates $11.17. Checkout says
price and lead time will be quoted within 48 hours after payment. Its terms make
the estimate adjustable and prohibit cancellation once quotation is finished;
any additional charge needs Erik's further approval. No payment was made.

The prior Global Sourcing offer also requires supplier transit/intake; it is not
an immediate-stock workaround. Ordering only controls/front would leave the
Cube/Beacon set incomplete and may incur another shipment; it is not the default
plan. Omitting U5 for later local rework or substituting a different RTC would
change the assembly scope and requires a separately reviewed decision. Neither
was applied to meet the deadline.

## Today's completed work and limits

- Rechecked live RTC shortage and the staged procurement amount; established the
  warehouse-receipt dependency in the published terms.
- Confirmed all four current native PCB hashes match the existing source-bound
  placement reference, covering 207 fitted references. This is source continuity,
  not a fresh whole-board ERC/DRC run or supplier placement acceptance.
- Attempted the amplifier's linked EasyEDA library viewer. Opening its iframe
  directly returned `ERR_BLOCKED_BY_CLIENT`; no usable numbered supplier map was
  obtained and no rotation/offset was changed.
- Recorded the prototype power disposition and separated before-purchase,
  before-production and before-power responsibilities.
- Erik explicitly chose **“Keep the enquiry unsent.”** The supplier draft remains
  local. No supplier response is expected from this preparation.

The useful near-term purchasing action is the exact RTC sourcing decision. It
can start the supply lead time while placement work continues. Complete-board
payment should follow the closed gates above, without representing an incomplete
quote or parts preorder as the finished PCB-order milestone.
