# Mechanical work

Read the relevant README and input manifests first:
[Cube v4.2](alec/pcb-revision/README.md) or
[Sensor S1.1](alec-sensor/README.md).

The Cube assembly currently depends on the v4.1 Blender source and staged PCB
GLBs. Sensor solids are generated with CadQuery from its interface parameters;
Blender carries the assembled visualization. These are different workflows.
Preserve the actual editable sources and vendor originals when reorganizing.

- Identify the exact board revision and export before evaluating fit. A newer
  gallery GLB is not automatically the input used by a saved assembly.
- Treat simplified models, wire paths and connector envelopes as allocations.
  Use exact purchased-part drawings for mating dimensions; retain provenance.
- Review tolerance stacks, fasteners, switch travel/overtravel, cable bends,
  battery replacement and programming access. Nominal nonintersection alone
  does not establish manufacturable fit.
- Coordinate board outlines, mounting holes, antenna/radar clearances and
  connector changes with electronics before modifying either side of the
  interface.
- After source changes, rebuild affected geometry and run the corresponding
  verifier before recording new evidence. Preserve raw physical observations.
  State when CAD tooling or a physical sample was unavailable.
- Printed fit samples, acoustic/thermal/radio measurements, sealing and mounting
  tests establish different results. Renders and solid checks do not establish
  waterproofing, print tolerances or everyday usability.

Prefer a small fit coupon for an uncertain button, connector or mount before
committing to another complete housing. Keep the accepted product shape and
requirements distinct from manufacturing experiments.
