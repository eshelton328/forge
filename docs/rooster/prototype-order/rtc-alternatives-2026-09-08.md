# RTC alternatives — September 8, 2026

**Investigate the RV-3028-C7 TA-QA grade first for the current boards; consider
RV-3032-C7 if accepting a PCB/firmware revision.** The present QC selection,
native sources, uploaded BOMs/CPLs and unpaid preorder remain unchanged. This is
a comparison, not substitution or spending approval.

## Actual requirements used for this screen

Both boards need 3.3 V operation, I2C time/calendar access, an alarm interrupt to
wake the ESP32, and low sleep current. Their selected module includes the quartz.
The native pin map, no-backup connection and firmware interface matter as well.
No separately agreed product-wide maximum clock drift across temperature was
found in this screen; distinguish the selected component's rating from a frozen
product acceptance requirement.

## Supply observed in live browser pages

All prices below are USD per part at quantity one, excluding shipping, tariffs,
tax, assembly and any external quartz. Inventory is unreserved and is not a
long-term supply guarantee.

| Exact candidate | Current supply observation | Relevance |
| --- | --- | --- |
| RV-3028-C7 32.768KHZ 1PPM-TA-QA | [DigiKey](https://www.digikey.com/en/products/detail/micro-crystal-ag/RV-3028-C7-32-768KHZ-1PPM-TA-QA/10499248): **6,011**, **$2.66**, $1.6239 at 100. [JLCPCB C3304278](https://jlcpcb.com/partdetail/C3304278): one stocked, preorder minimum three. | Strongest candidate to preserve PCB/driver. Enough distributor stock, but not enough stock already at JLCPCB for four fitted RTCs. |
| RV-3032-C7-32.768KHZ-2.5PPM-TA-QA | [JLCPCB C5366550](https://jlcpcb.com/partdetail/C5366550): 709 total, **284 available to order**, **$3.4603**, $2.4029 at 100. | Meets the screened functional/power needs and improves temperature stability; requires rerouting and driver work. |
| RV-3032-C7-32.768KHZ-2.5PPM-TA-QC | [DigiKey](https://www.digikey.com/en/products/detail/micro-crystal-ag/RV-3032-C7-32-768KHZ-2-5PPM-TA-QC/16273066): **799**, **$3.24**. | Another supply option for the revised design, not JLCPCB warehouse inventory. |
| PCF85063ATL/1,118 | [JLCPCB C404360](https://jlcpcb.com/partdetail/NXPSemicon-PCF85063ATL_1118/C404360): 1,953 total, **1,774 available to order**, **$0.7386**, $0.4442 at 100. | Lower-cost future candidate. Requires an external crystal, different footprint/routing/driver and a new accuracy/calibration budget. |

Live observations supersede search-index snapshots of 8,074/8,081 RV-3028 QA,
1,827 RV-3032 QC and 19,959 PCF85063 parts. Do not present those older counts as
the live checked amounts. RV-8803-C7 QC was also screened, but its
[DigiKey listing](https://www.digikey.com/en/products/detail/micro-crystal-ag/RV-8803-C7-32-768KHZ-3PPM-TA-QC/10499250)
reported zero; no supply advantage was established for it.

## Compatibility and accuracy

Micro Crystal identifies **QC as commercial and QA as automotive AEC-Q200** in
the same [RV-3028 datasheet](https://www.microcrystal.com/fileadmin/Media/Products/RTC/Datasheet/RV-3028-C7.pdf).
TA-QA retains the C7 package, pin functions, 45 nA typical / 60 nA maximum
timekeeping current at 3 V and 25°C, and factory ±1 ppm rating at 25°C. Engineering
assessment: this grade change should preserve our PCB and RV-3028 driver. Exact
manufacturer order code, tape presentation, supplier mapping and placement still
need confirmation before accepting a substitution. It is not an independent
second manufacturer.

The [RV-3032 datasheet](https://www.microcrystal.com/fileadmin/Media/Products/RTC/Datasheet/RV-3032-C7.pdf)
specifies 160 nA typical / 210 nA maximum at 3 V and 25°C, and temperature-compensated
±2.5 ppm from −40 to +85°C. That error rate equals about 6.48 seconds per 30 days,
before separately specified aging and system effects. Its extra typical current
versus RV-3028 is only 0.0828 mAh per 30 days on the RTC supply rail; this is not
a whole-battery runtime calculation. The present RTC's ±1 ppm is a room-temperature
calibration specification, not a guarantee across its temperature range.

Despite the same 3.2 × 1.5 mm body, the RV-3032 is **not pin compatible**:

| Pin | Current RV-3028 / native U5 | RV-3032 |
| --- | --- | --- |
| 1 | CLKOUT, unused | VBACKUP |
| 2 | INT → GPIO1 | SDA |
| 3 | SCL → GPIO9 | INT |
| 4 | SDA → GPIO8 | EVI |
| 5 | GND | GND |
| 6 | VBACKUP, 10 kΩ to GND | VDD |
| 7 | VDD, 3.3 V | CLKOUT |
| 8 | EVI, GND | SCL |

The two boards' source-bound U5 maps were checked. A 3032 conversion needs both
schematics/routes and generated manufacturing files updated, plus driver/register,
alarm-clear/wake and startup/no-backup review. Similar package geometry does not
permit changing only the BOM. Datasheet page 2 ordering, electrical and pin tables
were visually inspected; source PDF SHA-256 values are
`fb5a01874b3e02a088c3043dabe87bf5f0c6760ce2700d33c36ad3c4d02f12fc` (3028) and
`0f42daa62026ca24fb551b2102e28fdc1e8638fcea8bed2fe47b2eb99c8312e2` (3032).

[NXP's PCF85063A](https://www.nxp.com/products/PCF85063A) supports the needed alarm
and I2C functions with low current, but quartz selection, loading, temperature
drift and calibration determine accuracy. It is not a like-for-like replacement
for a factory-calibrated integrated module. Its attractive stock and IC price
alone do not justify revising the present prototypes.

## Recommendation for the order goal

Compare an exact RV-3028 TA-QA sourcing/consignment offer into JLCPCB against the
current QC preorder before spending. Distributor inventory cannot itself fill
the assembly matcher; verify intake, packing, quantity/attrition, total and lead
time. No such transfer was arranged in this comparison. If accepting a design
revision, RV-3032 TA-QA is the strongest alternate architecture identified here
and has directly observed JLCPCB stock. Its change/verification effort must be
weighed against supply lead time; no same-night completion is promised.

For production, qualify both acceptable RV-3028 grades/order presentations and
check distributor breadth, replenishment lead time and lifecycle over time.
Today's stock proves a current sourcing opportunity, not generally superior
future availability. No enquiry, order, cart change or board substitution was made.
