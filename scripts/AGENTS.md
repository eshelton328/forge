# Engineering tooling

Read the relevant guide: [alarm](alarm/README.md),
[physics](physics/README.md), [qualification](qualification/README.md),
[SPICE](../sim/README.md) or [EMI](../emi/README.md).

- Determine whether a command reads, exports, rebuilds or overwrites native
  sources. Several generators rebuild the alarm/Sensor from devkit-5v. Keep
  historical inputs until their consumers are deliberately migrated.
- Resolve paths from the repository/script or explicit arguments. Document
  runtime distinctions: host Python, KiCad Python/`pcbnew`, Blender and CadQuery.
- Fail on missing required input, solver/export errors and violated limits.
  Report optional skips separately. Do not let a later successful shell command
  hide an earlier failure.
- Test engineering invariants with independent expectations and failure controls
  when changing a validator: incorrect pins/polarity/layer, disconnected copper,
  stale evidence and wrong part variants as applicable. Rechecking a saved
  `passed: true` field alone does not rerun the underlying engineering analysis.
- Retain units, assumptions, validity ranges and raw outputs in numerical work.
  A behavioral converter model is not a validated switching model. Scenario
  arithmetic does not measure battery life or temperature.
- Keep evidence generation separate from evidence verification. Preserve old
  input bindings; a changed source requires an explained revalidation, not just
  a new hash.

Run relevant `tests/` modules first; run the broader host suite for shared tooling
changes. Numerical tests also need `scripts/physics/requirements.txt`; disclose
missing dependencies and skipped modules. Keep expensive solver runs tied to
an actual changed assumption, design or unresolved engineering question.
