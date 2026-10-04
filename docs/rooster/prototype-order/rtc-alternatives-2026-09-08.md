# RTC supply, temperature and manufacturer comparison — September 8, 2026

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

## Heat in the shower and enclosure

**Temperature was screened, but neither assembled product has passed a physical
thermal test.** The [Beacon report](../../../boards/alec-sensor/TEST-REPORT.md#thermal-screen)
estimates a 45.1–48.5°C lumped surface temperature at 40°C ambient for its example
0.775 W load. Its sustained 3.53 W stress case reaches 63.4–78.9°C under the same
two assumed cooling conditions; that is not an approved operating mode. These
are surface estimates, not temperatures at the RTC, cells or regulator junctions.

The [Cube report](../../../boards/alec-main/review/TEST-REPORT.md#fresh-copperthermal-screening)
also contains a nominal PCB thermal model: approximately 33.61°C peak rise with
its assumed loads and cooling. It does not model enclosure cooling or package
junction temperatures. Neither historical screen validates the current assembled
boards or authorizes prolonged high-load use in a sealed housing.

The present RV-3028 TA grade operates from −40 to +85°C. Its **±1 ppm is specified
at 25°C**, and its quartz has a parabolic temperature characteristic. Using the
datasheet's nominal coefficient −0.035 ppm/°C² and 25°C turnover, a crystal held
at 50°C has approximately −21.9 ppm thermal offset: about 1.89 seconds/day if
held there all day, or 0.039 seconds during a 30-minute exposure. These are
illustrations, not worst-case guarantees; turnover/coefficient tolerances,
initial error, aging and actual crystal temperature also matter. Brief shower
heating does not imply two seconds of added error every day. Changing QC to QA
does not add temperature compensation or raise this TA temperature limit.

Temperature therefore favors considering a compensated clock, rather than
retaining RV-3028 specifically for heat. More urgent system checks are regulator,
radio/radar/audio and cell heating, fuse derating, accessible case temperatures
and moisture/condensation. The Beacon's selected C&K 1101M2S3CQE2 switch belongs
to a family rated only to **65°C** ([manufacturer datasheet](https://www.ckswitches.com/media/1429/1000.pdf),
p. 1); this is a component ceiling, not a safe case-temperature target.

After delivery, instrument both assembled housings at the agreed maximum ambient,
normal duty and longest supported alarm/radar operation. Log RTC, converters,
cells, radar/amplifier and case temperatures, supply stability, elapsed-time
drift and alarm wake behavior. Use measured margins to establish load/duty limits.
Wet/condensation and sealing validation remain part of ROO-017 after the fit work
in ROO-016; these physical tests are not newly imposed prerequisites to purchasing
engineering prototype PCBs.

## Other RTC manufacturers

All candidates below integrate their timing resonator and support 3.3 V, I2C and
alarm interrupts. **All require board and driver changes from RV-3028.** The
accuracy column covers −40 to +85°C; aging and other separately specified effects
must still enter the finished-product error budget. Currents are typical idle
timekeeping values in the stated configurations, not whole-device sleep current
or a guarantee at elevated temperature.

| Manufacturer / candidate | Accuracy across temperature | Typical supply current and conditions | Assessment for Rooster |
| --- | --- | --- | --- |
| [Micro Crystal RV-3032-C7](https://www.microcrystal.com/fileadmin/Media/Products/RTC/Datasheet/RV-3032-C7.pdf) | ±2.5 ppm | 0.160 µA at 3 V, 25°C | Best balance identified here of size, accuracy and already-observed JLCPCB stock; different pinout despite same 3.2 × 1.5 mm body. |
| [Epson RX8901CE XS](https://download.epsondevice.com/td/pdf/brief/RX8901CE_en.pdf) | ±3 ppm; XS is the tighter grade | 0.40 µA from VDD at 3 V, clock output off, 2 s compensation | Credible independent manufacturer. 3.2 × 2.5 mm / 10 pins, requires a VOUT capacitor and new power/initialization review. XS also specifies ±5 ppm above 85 to 105°C; cheaper XB has looser accuracy. |
| [NXP PCF2131TFY](https://www.nxp.com/docs/en/data-sheet/PCF2131.pdf) | ±3 ppm typical, **±8 ppm limits** | 0.070 µA at 3.3 V with compensation on, CLKOUT/hundredths counter/power management off | Strong supply/cost candidate with exceptionally low current. 4.5 × 3.5 mm / 16 pins and a looser worst-case accuracy budget than RV-3032 or Epson XS. |
| [Analog Devices MAX31343ETAY+T](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX31343.pdf) | ±5 ppm | 0.940 µA at 3.3 V, 25°C, clock output off, 32 s compensation | Integrated MEMS timing, two alarms; 3 × 4 mm / 8-pin TDFN. Higher current and observed small-quantity price make it less attractive here. |

The [Epson application manual](https://download.epsondevice.com/td/pdf/app/RX8901CE_en.pdf),
Table 5.4, gives the 0.40 µA VDD figure; the advertised 0.24 µA is **backup** current.
NXP Rev. 2.5, Table 89, gives 70 nA with compensation enabled in the configuration
above; its 64 nA figure disables compensation. NXP's ±3 ppm typical figure must
not be compared as a guaranteed limit against competitors' maximum errors.
Epson's brief and NXP's current table were visually checked. ADI's datasheet
current includes averaged temperature conversions. Its April 2026 PIN 2571D
concerns shipping packaging, not an electrical erratum.

### Additional live distributor observations

Checked September 8, 2026 in the rendered US DigiKey product pages. USD per part,
**cut tape**, with shipping, tariff, tax, reeling, assembly and supplier intake
fees separate. These quantities supersede older search-index results.

| Exact orderable part / source | Stock observed | Each at 1 / 100 | Listed standard manufacturer lead time |
| --- | --- | --- | --- |
| [RX8901CE XS B06](https://www.digikey.com/en/products/detail/epson/RX8901CE-XS-B06/16630058) | 415 | $6.40 / $4.1105 | 30 weeks |
| [PCF2131TFY](https://www.digikey.com/en/products/detail/nxp-usa-inc/PCF2131TFY/15216480) | 2,573 | $3.66 / $2.2761 | 16 weeks |
| [MAX31343ETAY+T](https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX31343ETAY-T/17885235) | 1,499 | $7.32 / $4.7600 | 10 weeks |

Listed standard lead time is not a promised delivery date for stocked material.
Distributor stock is not JLCPCB warehouse stock; JLCPCB intake for these three
has not been established. No conclusion of generally better long-term supply
follows from a brand name or today's count. Exact variant, lifecycle, replenishment,
assembly acceptance and an agreed clock-drift budget still determine selection.
The comparison expands the options; the existing native design remains unchanged.
