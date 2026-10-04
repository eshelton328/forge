# Rooster release conventions

No product firmware or manufacturing release has been declared.
The [product map](../../projects/rooster/README.md) locates the current engineering
sources. Existing [fabrication candidates](../../docs/rooster/prototype-order/fabrication-candidates/README.md),
[placement candidates](../../docs/rooster/prototype-order/supplier-placement-candidates/README.md)
and [supplier RFQ package](../../docs/rooster/prototype-order/cube-supplier-quotes-2026-09-08/README.md)
remain at their original paths with their original manifests and hashes.

ROO-010/013 should assign a release identifier only to a concrete reviewed bundle.
Record exact native commit, board revisions, fitted/DNP BOM, placement files,
Gerber/drill files, stackup/via/assembly scope, source and output hashes, tool
versions, actual checks and the approval/order record. Firmware releases also
need targets, toolchain, binaries/hashes and upload settings. Keep released
bundles immutable; corrections receive a new identified bundle.

The existing manual CI export is an artifact generator. Producing files or
passing static checks does not establish an order, physical acceptance or
Erik's purchase approval.
