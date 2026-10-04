# Power-component selection for the prototype order

Reviewed September 7, 2026 local time; public model/catalog captures completed September 8 UTC. **Retain the existing converter layout, 1.5 µH Coilcraft inductors and capacitor-bank values. Replace the proposed 10 µF / 0603 ordering part with Murata GRT188R61A106KE13D, JLCPCB C782172.** The resulting near-converter capacitor banks pass the selection screen below. This closes the missing effective-capacitance evidence for those banks; it does not qualify the real boards or release the full manufacturing package.

## Concrete BOM decision

The nine affected references are main **C3/C5/C11/C13** and Beacon **C3/C5/C11/C13/C35**. The original GRM188R61A106KAALD is a real 10 µF, 10 V, X5R, ±10%, 0603 part, but its model is unavailable in the current SimSurfing service. Its old reference sheet is not a DC-bias curve. The substitute retains those ratings and the same **1.6 × 0.8 × 0.8 mm nominal body, ±0.15 mm dimensions**. Its current manufacturer sheet, dated April 18, 2026 in the actual download, was visually checked on page 2. Its bias models are available. JLCPCB reports **9,799 available** in the saved public query, versus the earlier proposal's very limited stock. Availability is not reserved.

Sources: [original Murata specification](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM188R61A106KAAL-01A.pdf), [replacement Murata specification](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRT188R61A106KE13-01A.pdf), [JLCPCB replacement](https://jlcpcb.com/partdetail/C782172), [dated catalog response](jlc-capacitor-followup-20260908.json).

The native KiCad files, purchasing overlay, source generators and draft BOMs now identify the replacement. [Source integration](source-integration-review.md) confirms that every non-ordering source token and the independent KiCad copper/placement geometry are preserved. No component moved; nominal capacitance and voltage constraints are unchanged.

## Effective capacitance

The [manufacturer capture](murata-curves-20260908.json) contains 28 successful curves and three explicit unavailable-model responses. It covers nine selected Murata capacitor families plus the superseded 0603 proposal. Data came from [Murata SimSurfing](https://ds.murata.com/simsurfing/mlcc.html?lcid=en-us), whose visible dataset date was September 2, 2026. The same public read endpoint used by its graph UI provides the numeric points; the 22 µF reference curve was independently reconciled with five points from the rendered SVG.

Use **10 mVrms AC** for this small-signal screen, rather than assuming capacitance measured at 0.5 or 1 Vrms is available on a quiet DC rail. Curves were requested at **−55, 25 and 85°C**. These are sampled typical models, not guaranteed production limits or proof at every intervening temperature. [Manufacturer measurement conditions](https://ds.murata.com/simsurfing_data/pdf/en-us/mlcc/sim_mlcc_measuringcond_e.pdf) explain the distinction between DC bias, AC voltage and temperature characterization.

For each capacitor, take the lowest of the three temperature samples at the screening voltage, subtract its nominal tolerance, then reserve a further **20%** for engineering margin. The extra reserve is an assumption, not a manufacturer-guaranteed aging or model-error bound. Do not subtract the X5R temperature percentage again: temperature is already represented by the models.

The screen uses **5.4 V at protected battery VIN**, **3.6 V on the 3.3-V output**, and **5.4 V on the 5-V output**. The output ceilings exceed the calculated static maxima of approximately **3.505 V and 5.290 V**, including the actual divider's 1% resistor extremes, TI's +3% PFM reference error and 100 nA feedback leakage. Those static calculations exclude switching ripple/overshoot and resistor temperature drift. The input ceiling is a design-review envelope for the three-AA architecture, not a measurement of Erik's cells.

Both boards have the same local banks:

| Bank per converter | Native references | Screened capacitance, including tolerance and extra reserve | Selection threshold |
| --- | --- | ---: | ---: |
| 3.3-V converter input | C1/C2/C3 | **5.391 µF** | 4.7 µF |
| 5-V converter input | C9/C10/C11 | **5.391 µF** | 4.7 µF |
| 3.3-V converter output | C5/C6/C7/C8 | **24.925 µF** | 18 µF |
| 5-V converter output | C13/C14/C15/C16 | **19.970 µF** | 18 µF |

The output threshold uses the adjustable TPS63070's **Ceffective ≥ 10 × Leffective** criterion with 1.8 µH at the +20% inductance tolerance. Its recommended effective-inductance range is 0.7–2.8 µH. The input bank on the other converter and downstream bulk capacitors receive **no credit** in these local-bank minimum calculations. Actual netlist connectivity is checked before summing. [TI TPS63070 datasheet, sections 7.3 and 9.2.2](https://www.ti.com/lit/ds/symlink/tps63070.pdf).

Some useful typical values at 25°C / 10 mVrms illustrate why nominal values alone were insufficient:

| Selected capacitor | At 3.3 V | At 5 V |
| --- | ---: | ---: |
| 10 µF / 0603 GRT188R61A106KE13D | 4.65 µF | 3.12 µF |
| 10 µF / 0805 GRM21BR61E106KA73L | 5.00 µF | 3.90 µF |
| 22 µF / 1206 GRM31CR61C226KE15L | 14.61 µF | 11.84 µF |
| Main 100 µF / 1206 GRM31CR61A107MEA8L | 48.07 µF | 32.57 µF |

The existing 22 µF / 1206 part appears as **“To be discontinued”** in the manufacturer's current UI. It has a usable model and observed supplier stock; retain it for this small prototype order if final stock remains available. Record the lifecycle issue for the next sourcing revision. A replacement must be compared by effective capacitance and package dimensions, not just nominal value. The Samsung Beacon C21 bulk capacitor is not covered by the Murata models and is not credited to the local-bank minimum.

## Inductor decision and useful load cases

The existing **XFL4020-152MEC** is the 1.5 µH part in TI's own recommended inductor table. [Coilcraft's current specifications](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xfl/xfl4020/xfl4020-152/) give **4.1 / 4.4 / 4.6 A** at 10 / 20 / 30% inductance drop at 25°C. Its **6.7 / 9.1 A** figures describe 20 / 40°C temperature rise; **9.1 A is not the saturation rating**. DCR is 15.8 mΩ maximum at 25°C. These ratings do not establish hot-board or fault performance.

The offline calculation uses TI's boost-mode equations, 80% assumed efficiency, 2.1 MHz minimum switching frequency, 1.08 µH for ripple (−20% tolerance and −10% current drop), and 1.8 µH for the right-half-plane-zero calculation. The saturation requirement includes TI's additional 20% margin.

| Screen case at 3 V protected input | Estimated peak inductor current | Isat needed with margin | Calculated RHP zero |
| --- | ---: | ---: | ---: |
| 3.3 V / 0.25 A digital reference | 0.404 A | 0.485 A | 965 kHz |
| 3.3 V / 0.5 A digital stress | 0.748 A | 0.897 A | 482 kHz |
| Cube 5 V / 0.3 A allowance for 1 W audio | 0.890 A | 1.067 A | 531 kHz |
| Beacon 5 V / 0.2 A supply allowance | 0.681 A | 0.817 A | 796 kHz |

These cases support retaining the inductor. They are **not confirmed firmware averages, simultaneous battery-load approval or guaranteed acoustic performance**. The Cube case reuses the [existing 8-ohm / 1-W speaker-and-load proposal](../../../boards/esp32s3-devkit-5v/review/physical-validation/continuous-alarm.md); exact speaker/holder procurement and the shared battery/fuse envelope still need their own disposition.

At 2 V input, the depleted-battery stress cases fall below TI's recommended 400 kHz RHP-zero target. TI calls for additional output capacitance and observation of stability in such conditions. The existing downstream capacitance helps, but no loop-stability proof is claimed. Cold starting either converter also requires at least 3 V at its input. Do not promise full alarm power or restart on depleted cells. TI's 3.05–4.15 A current-limit range is **average input current under its stated test conditions**, not a hard peak-current clamp. The 2-A / 5-V-from-2-V counterexample deliberately fails this screen.

## Order disposition and first-board evidence

- **Component selection:** accept the four unchanged local bank layouts and selected Coilcraft inductor for the stated prototype evaluation, with the nine-reference 0603 MPN substitution. Source metadata is integrated; supplier assembly review remains.
- **Before payment:** the subsequent [prototype power disposition](prototype-power-disposition.md) retains the current circuitry for supervised, current-limited dry bench evaluation and hands protection/load validation off before battery use. Complete external-item scope and remaining package/pin/assembly checks still precede the full purchase proposal. This review does not clear the complete BOM.
- **After delivery:** start with a current-limited source at ≥3 V protected VIN and modest loads; measure actual startup, radio/radar/audio load steps, PFM ripple, rail overshoot and temperatures. Then test depleted cells and the shared-load cases. Use those measurements to establish operating limits; they are not prerequisites that can be fabricated through more simulation before boards exist.

Reproduce the offline calculations with `python3 docs/rooster/prototype-order/tools/review_power_parts.py`. [Audit JSON](power-component-audit.json) binds the source board/netlist/sourcing/model hashes, bank members, voltage calculations and stress-case results. The query script can make a new dated manufacturer capture when part choices change; no supplier messages, cart changes, reservations or purchases are involved.
