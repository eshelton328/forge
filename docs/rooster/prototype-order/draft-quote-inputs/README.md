# Draft quote BOM and placement inputs

**Review only. Do not submit as a manufacturing release.** These eight CSV files combine the proposed manufacturer selections with the current native footprint positions. They provide complete reference coverage for pricing and assembly review; the source MPN fields and final part/rotation/assembly checks remain open.

- Both faces and through-hole parts are included. R11 DNP and unpopulated test pads are excluded by native flags.
- BOM quantities are for one board of each design; request two assembled and five fabricated copies per design in the quote.
- PCB-mounted socket/header parts are included; external radar/display modules, mating cables, holders, cells, speaker and other loose items are separate procurement.
- Position coordinates are in millimeters using KiCad's auxiliary drill/place origin. Rotations are KiCad-native, without confirmed JLCPCB corrections. Review supplier pin-1/placement overlays before release and use matching origins for Gerbers/drills.
- These are not generated from the current `kibot/jlcpcb.kibot.yaml`, whose `only_smd: true` would omit required through-hole references. The dedicated draft builder includes them explicitly and reconciles every exported position with the sourcing inventory.

Reproduce from the repository root:

```sh
python3 docs/rooster/prototype-order/tools/verify_sourcing.py
python3 docs/rooster/prototype-order/tools/build_quote_inputs.py
```

The builder accepts `--kicad-cli` to select the local KiCad executable. [Manifest](manifest.json) records version, source/file hashes, reference coverage and limitations. [Part review](../part-selection-review.md) owns remaining component/source work; [assembly preflight](../jlcpcb-preflight.md) owns service choices. No Gerber archive, supplier upload or order is included in this draft.
