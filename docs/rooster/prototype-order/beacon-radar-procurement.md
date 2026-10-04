# Beacon radar: purchased module and PCB-mounted socket

The current `alec-sensor` design uses a complete **Hi-Link HLK-LD2410C radar module with its five-pin, 2.54 mm header**, plugged into the PCB's J3 socket. We design and order the host PCB containing the ESP32, power/control circuits and socket. Hi-Link manufactures the radar antenna, RF electronics and detection firmware. Designing a custom radar is outside this prototype order.

This is the existing design, not a new design selection. The recommended prototype approach is to retain it: it matches the preserved LD2410C breadboard software and current mechanical model, and lets a module be replaced without desoldering the host PCB. A surface-mount purchased module remains an option for a future deliberate board/mechanical revision; it would still be a purchased radar, not our own radar design.

## Separate procurement and assembly items

| Item | Required for two assembled Beacon units | Assembly plan and current status |
| --- | --- | --- |
| J3 socket: Samtec SSW-105-01-F-S | 2 fitted sockets, plus supplier-required assembly attrition if any | In the native PCB and review BOM. Request factory through-hole assembly; actual service acceptance/placement remains open. |
| Hi-Link HLK-LD2410C with matching male header | 2 usable modules total | Separate module procurement. Credit any compatible modules already owned only after inventory/revision verification. Proposed final assembly is plugging the module into J3; supplier installation would require explicit inclusion in the quote. Purchase quantity and supplier are not yet fixed. |

The working PCB BOM's J3 value says `LD2410C — INTERNAL`, but its MPN **SSW-105-01-F-S identifies only the socket**. Do not treat that row or eight assembled PCBs as including the two radar modules. The native board has 88 fitted BOM references; adding this external module does not add a new native PCB reference.

## Variant, orientation and mechanical checks

- Retain the five-pin header version matching the current vendor model and 22 × 16 mm radar body. Existing custom J3 footprint uses five through holes at 2.54 mm pitch; nominal socket housing height is 8.51 mm. The enclosure depends on that stack height.
- JLCPCB's catalog distinguishes **HLK-LD2410C** (plug-in, 16 × 22 mm) from **HLK-LD2410C-P** (surface mount, 22 × 16 mm). Do not substitute the `-P` listing for the current socketed assembly based on stock alone. An older vault snapshot mentioning `LD2410C-P` is historical and does not override the current native socket and enclosure.
- The saved current netlist maps **J3 1 = radar TX, 2 = radar RX, 3 = OUT, 4 = GND, 5 = switched 5 V**. TX/RX here name the radar's signals. Confirm the received module's physical pin order, viewing direction and header orientation against the final assembly drawing before insertion; the netlist mapping alone is not a physical fit test.
- The manufacturer product page specifies 5 V power, approximately 79 mA and 3.3 V serial signals. Preserve the existing switched power and signal isolation. Scheduled radar operation and measured battery life remain firmware/bench work; the purchased module does not make continuous detection compatible with an assumed month-long battery life.

## Public sourcing observation — 2026-09-07

The [dated catalog capture](jlc-radar-catalog-20260907.json) records read-only public search results, not reservations, assembly commitments or a quote:

| Exact listing | Catalog ID | Observed stock | Disposition |
| --- | --- | --- | --- |
| [Samtec SSW-105-01-F-S](https://jlcpcb.com/partdetail/Samtec-SSW_105_01_FS/C5930350) | C5930350 | 33 | Exact MPN match; request through-hole assembly and verify final availability. |
| [Hi-Link HLK-LD2410C](https://jlcpcb.com/partdetail/HILINK-HLKLD2410C/C18197927) | C18197927 | 0 | Correct named module family; source compatible header version separately or establish supplier lead time. |
| [Hi-Link HLK-LD2410C-P](https://jlcpcb.com/partdetail/HILINK-HLK_LD2410CP/C19723500) | C19723500 | 355 | Surface-mount variant; not a drop-in replacement for the current J3 socket. |

Manufacturer source: [Hi-Link LD2410C product/download page](https://www.hlktech.com/en/Goods-239.html), checked September 7. It describes a complete 24 GHz presence module, UART/GPIO outputs and header pins as the default package. Some generic dimensions on that page conflict with the C-specific drawing; use the existing reviewed C drawing/model for geometry. The current linked V1.09 manual download returned 404 through the website during this check, and the alternate download host timed out in the web reader. No fresh manual review is claimed; the existing [source review](../../../boards/alec-sensor/SOURCES.md) records its original retrieval and geometric evidence.

Native evidence: [board README](../../../boards/alec-sensor/README.md), [review BOM](../../../boards/alec-sensor/review/bom.csv), [netlist](../../../boards/alec-sensor/review/netlist.xml), [custom socket footprint](../../../boards/alec-sensor/footprints/Sensor.pretty/Samtec_SSW-105-01-F-S.kicad_mod), [mechanical contract](../../../boards/alec-sensor/ENCLOSURE.md). No native source changed in this clarification. ROO-010-AC01/04 and Beacon O03 retain the assembly/supply checks; ROO-013 retains the hardware interface.
