# Working in Forge

Forge is the electronics workspace. Rooster is the alarm product; ALEC is the
existing hardware family. Start with [the product map](projects/rooster/README.md)
for Rooster work. Keep native board names stable unless a task explicitly needs
a migration.

## Read only the guidance for your task

Before changing files below, read that directory's `AGENTS.md` and the relevant
component README. A task started at the repository root must explicitly open
the applicable nested guidance; do not assume every nested file was loaded.

| Work | Guidance and entry point |
| --- | --- |
| Schematics, layouts, footprints, component selection | [boards/AGENTS.md](boards/AGENTS.md), then the board README and interface contract |
| Enclosures, purchased geometry, physical fit | [enclosures/AGENTS.md](enclosures/AGENTS.md), then the enclosure README |
| Generators, validators, simulation | [scripts/AGENTS.md](scripts/AGENTS.md), then the relevant scripts/sim/physics README |
| CI, fabrication exports, generated documentation | [.github/AGENTS.md](.github/AGENTS.md), the workflow and referenced scripts/configs |
| Application/diagnostic firmware and protocol | [firmware/AGENTS.md](firmware/AGENTS.md), then the target README and native board contract |

## Establish the actual baseline

- Read `git status --short`, the current commit and `git worktree list` before
  editing. Worktree names are locations, not evidence that their work is merged.
- Obsidian `Projects/Rooster` owns product decisions, ROO task specifications and
  task status. Git owns native designs, code and versioned engineering evidence.
  Use the task and its current linked deliverables; dated audits are snapshots.
- Preserve historical firmware, source manifests and supplier packages. Treat
  missing firmware or a planned path as missing, never as implemented.
- Inspect generators before executing them. Several rebuild designs from older
  boards and overwrite native files. Rebuild in a disposable copy when auditing.
- Routine edits and checks should proceed within the requested scope. Purchases,
  supplier messages and production approval require the user's applicable explicit
  authorization. An export or green CI run does not grant it.

## Verification and reporting

Run checks appropriate to changed files. `python3 -m pytest tests/ -q -ra` is the
host suite. For board work use an explicit board: `make check BOARD=alec-main`
and `make validate BOARD=alec-main`, plus the board's specialized checks.
`make check` defaults to a development board, not the Rooster product.

Record the command, source revision, tools, result and skips. Distinguish
**static check**, **simulation**, **nominal CAD fit**, **bench measurement** and
**product-use result**. A preserved result stays bound to its original inputs;
do not refresh hashes merely to make a stale result pass.

Hardware changes need review of affected electrical, firmware, mechanical and
manufacturing interfaces. A passing ERC/DRC or model is evidence only for its
stated scope. Physical acceptance needs identified units and actual observations.

Keep instructions short. Put detailed procedures in linked runbooks and enforce
repeatable constraints in code. Change the current summary when a decision
changes, and preserve its history in dated records rather than appending another
competing current summary.
