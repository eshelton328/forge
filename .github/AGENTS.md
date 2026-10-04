# CI and export work

Read the changed workflow and every script/config it calls. The normal host
suite runs for all PRs; electrical, simulation and mechanical work also has path
selection. Check shared-source changes and empty-board selections explicitly.

- Keep KiCad/image versions consistent across Makefile, workflows and simulation
  containers. Prefer pinned actions and toolchains with an explicit update path.
- Required checks must fail when a command fails, an input/report is missing or
  a required test is skipped. Optional galleries and exploratory jobs should
  communicate their weaker result rather than imply release approval.
- Keep generated previews separate from source-bound review evidence. Do not
  rewrite historical evidence when the documentation bot updates a gallery.
  Source/tool identity should accompany new engineering results.
- `release.yml` currently generates files on manual dispatch. It is not a tag
  release pipeline or an approval gate. Do not claim a product release until
  the selected boards, BOM/CPL, fabrication process and immutable manifest agree.
- Manufacturing bundles must account for both-side and through-hole assembly,
  fitted/DNP/service pads, supplier rotation/offset corrections and the actual
  quoted stackup/via process. Keep old ordered bundles immutable.
- Avoid embedding free-text inputs directly into shell code; use environment
  variables and validate board names against actual known projects.

For CI edits, verify change selection and failure propagation as well as the
happy path. Use artifacts for build output where possible. Any change to the
existing bot-commit/gallery contract must update its consumers and documentation.
