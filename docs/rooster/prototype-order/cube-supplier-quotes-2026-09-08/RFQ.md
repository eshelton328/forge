# Rooster Cube prototype — request for quotation

September 8, 2026. Quotation only. No purchase, component procurement, fabrication or assembly is authorized by this request.

Please quote three PCB designs to supply two complete Cube PCB sets. Preferred quantity is five fabricated boards per design, with two fully assembled and the remaining three supplied bare. If your service uses another minimum, identify it and price the smallest complete alternative separately. Ship to Austin, Texas 78704, USA.

| Design | Product outline | Layers | Fitted components per board | Assembly |
| --- | --- | ---: | ---: | --- |
| alec-main | 64 × 56 mm | 4 | 111 | 110 top SMT placements plus J4 through-hole header; R11 DNP |
| alec-controls | 27 × 34 mm | 2 | 5 | Rear SMT J1 plus front through-hole SW1–SW4 |
| alec-front | 24 × 10 mm | 2 | 3 | Top SMT D1/SW1 and rear SMT J1 |

## Required RTC and sourcing

Main U5 must be **Micro Crystal RV-3028-C7 32.768KHZ 1PPM-TA-QA**, manufacturer ordering code **203603-MG01**. This is the production-intent candidate for quotation; final product clock-drift qualification is pending. Use the exact QA part shown in the quote BOM. No QC/QA substitution ambiguity, omitted RTC, or unconfirmed backorder is acceptable in the complete offer.

Please identify the authorized distributor or your traceable inventory, available quantity, required procurement quantity including attrition, price, packaging/handling fees and lead time. Two fitted RTCs are needed. DigiKey's exact QA listing showed 6,011 available on September 8, 2026; this is a sourcing lead, not a reservation or evidence of your factory allocation:

https://www.digikey.com/en/products/detail/micro-crystal-ag/RV-3028-C7-32-768KHZ-1PPM-TA-QA/10500185

The native source revision still names QC. This quote-only BOM explicitly selects QA for U5; circuit, footprint and other components are unchanged. Quote every other fitted BOM item at the specified MPN. Flag unavailable parts or proposed alternates for review instead of silently substituting or omitting them.

## Fabrication and assembly scope

All boards: nominal 1.6 mm FR4, green solder mask, white silkscreen, ENIG and 1 oz copper. Main requires **1 oz inner as well as outer copper**, Tg at least 155 °C, and **epoxy-filled, planarized, copper-capped vias**. Small boards retain tented vias and Tg at least 135 °C. Identify your actual stackup, copper thickness, ENIG thickness and tolerances. The prior main reference has approximately 0.203 mm outer-to-inner dielectric and a 1.030 mm center core. An alternate construction requires engineering review. This prototype does not claim controlled USB impedance.

Main fill/cap scope is all 255 plated round holes of nominal diameter 0.20, 0.25, 0.30 and 0.40 mm, including the twelve U3 thermal-pad holes. Use the attached exact fill-coordinate list and drill map. Preserve original mask openings and solderable thermal lands. **Leave component lead holes, USB shell slots, locating holes and mounting holes open.** Solder-mask plugging or tenting does not meet the main-board fill/cap requirement.

The attached Gerbers are single product outlines, without supplier rails or panelization. Price any required panelization, fiducials, fixture support, stencil, both-face assembly, through-hole soldering and depaneling. Identify delivered board format and rail removal. Overhanging components, including main J3 and U3, need adequate fixture and detachment clearance.

Placement CSVs are unmodified native KiCad exports: millimetres, common zero auxiliary origin, Y upward, top-view coordinate frame, no bottom-X mirroring or supplier rotation corrections. They are **reference input for quotation, not approved machine placement data**. Reconcile component body origins, all numbered pads and pin orientation before production. Supplier-specific placement review and customer approval remain required.

## Requested price and lead-time breakdown

Please separate bare PCB fabrication/options, fitted parts, procurement excess/attrition, setup/stencils, assembly/THT/both-face work, inspection/testing and other services. State fabrication, sourcing and assembly lead times and quote validity. Provide shipping to 78704 separately from manufacturing; itemize tariffs/import clearance and sales tax separately, or mark them excluded/unconfirmed.

Identify electrical bare-board testing, AOI, hidden-joint/X-ray coverage, workmanship standard and defect/rework terms. Firmware programming and functional testing are not specified in this RFQ and should not be represented as included or completed. Display, speaker, battery holders/cells, cables and enclosure are outside this PCB assembly request.

Please flag every exception before presenting the offer as complete. Final CAM, stackup, stencil and placement approval must remain manual. This RFQ is not a production release.
