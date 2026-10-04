# Forge and Rooster repository audit

**2026-10-04 · local source and workflow audit · main `a56d890`**

Forge has a substantial engineering foundation, but the current product is
difficult to reconstruct. Useful work is split between main, unintegrated
branches, historical firmware and a large Obsidian project. The highest-value
next step is a coherent Cube prototype baseline with runnable diagnostics and
measured results. More planning documents, another wholesale rename or more
general simulation infrastructure would do less to advance that milestone.

This audit covers the local repository, registered worktrees, the older clone
referenced by the project, Rooster notes, key generation/validation/CI code,
hardware/mechanical interfaces, preserved firmware, manufacturing preparation
and dated costs. It includes fresh checks and online research. It is not a
component-by-component electrical sign-off, supplier CAM acceptance or physical
test of a product. No supplier prices, replies, stock or orders were refreshed.

## What exists and what works

Before this audit's documentation additions, main contained **794 tracked files**,
seven boards, nine workflows and 24 Python test files. The local main checkout
uses about 314 MB for Git, 228 MB for boards, 90 MB for enclosures and 140 MB for
ignored output. These are filesystem sizes, not download sizes or a reason to
rewrite Git history. The Obsidian project has **64 Markdown notes, about 89,462
whitespace-delimited words, 17 tasks and five epics**. None of the scanned
explicit vault-path wikilinks was broken.

Strengths worth keeping:

- KiCad ERC/DRC, schematic parity, declared fab rules, circuit-intent checks and
  negative controls already exist. Main Cube evidence is bound to source hashes.
- There are real native schematics/layouts and reproducible enclosure assets,
  not just renders. Source provenance and limitations are usually documented.
- Historical breadboard firmware was preserved with dependencies, checksums,
  build records and a PCB port matrix. The originals still match the archive.
- The order branch does detailed MPN, DC-bias, package, placement, via-process,
  mask and fabrication review. That work should be integrated, not recreated.
- Most reports explicitly distinguish simulations and nominal geometry from
  physical qualification. Preserve that discipline.

Fresh verification performed during this audit:

| Check | Result and scope |
| --- | --- |
| Main `python3 -m pytest tests/ -q -ra` | **127 passed, one module skipped**, 14 dependency deprecation warnings; host Python 3.9, not CI's 3.12 |
| Order branch at `1e8ee95`, same host command | **145 passed, one module skipped**, same warnings |
| KiCad 10.0.1 ERC on all seven main boards | **Seven passed**, zero reported violations |
| KiCad 10.0.1 DRC with refill and schematic parity on all seven main boards | **Seven passed**, zero reported violations; reports written outside native sources |
| Existing copper guard on all seven main boards | Passed; its wrong-layer false positive is separately reproduced below. KiCad Python emitted a wxApp diagnostic |
| `make validate-all` | Six passed; Sensor explicitly skipped because it has no `checks.yml`. The final “all boards passed” message overstates that command's coverage |
| ROO-002 `verify.py --compare-originals` | 15 candidates, 15 original files, two dependency archives and archive hashes passed |
| Sensor source manifest | 214 bindings inspected; seven mismatches, all in generated `docs/` gallery exports. No native-source mismatch in that manifest |
| ROO-006 v0.1 bindings | 11 of 14 reconciled inputs changed; two of five artifact bindings changed. The three standalone acceptance/observability/run-sheet artifacts still match |

The skipped module is `tests/test_physical_screening.py`, because SciPy is absent
from the host environment. It is a module-level skip, not evidence that only one
individual numerical case was omitted. The dedicated numerical CI job installs
its own dependencies. No fresh full physics, EMI, Blender or CadQuery rebuild,
multi-fab DRC run, application-firmware build, order-branch ERC/DRC run or physical
measurement was performed. Existing reports were inspected within that boundary.
See [audit evidence](2026-10-04/evidence.json) for revisions, inputs and results.

## Findings in priority order

### P1 The latest engineering baseline is outside main

There are eight registered checkouts, plus the older separate clone under
`Electronics/the-forge`. All secondary worktrees were tracked-clean. Main had
three untracked historical enclosure logs. A clean worktree can still contain
valuable ignored data, so this is not deletion clearance.

| Checkout or branch | Observed HEAD | Disposition |
| --- | --- | --- |
| `forge` / main | `a56d890` | Current integration source; `the-forge` is a symlink to it |
| `forge-rename` | `a56d890` | Same tracked state as main; first retirement candidate after ignored-file and active-task checks |
| `the-forge-alec` | `12e2b10` | Historical rename work; content is represented by later main history. Verify patch/content equivalence before retirement |
| `the-forge-alec-sensor` | `dc57b55` | Historical Sensor work; current Sensor native inputs are represented on main, with later gallery/rename differences |
| `the-forge-enclosure-pcbs` | `c402b2b` | Historical pre-ALEC enclosure/PCB work; migration-aware comparison required |
| `the-forge-roo-002` | `59e0e42` | Preserve and integrate the firmware archive/port matrix; two baseline commits sit above the historical Sensor branch |
| `the-forge-roo-004` | `f0b8dca` | Preserve and integrate Cube acceptance/bench deliverables |
| `the-forge-rooster-orders` | `1e8ee95` | **28 commits beyond its shared base with main**; native sourcing/header-fit corrections plus 407 changed paths in the branch diff |
| Separate `Electronics/the-forge` clone | `466de9c`, May 24 | Clean historical main, old remote name; inspect all refs, ignored files and consumers before retiring |

The ordering work changes real native files, including the display header's
finished-hole allowance, exact purchasing fields and selected capacitors. Starting
the next design from main alone misses those changes. Conversely, copying the
whole order branch over main would reintroduce pre-rename workflow references.
Raw “ahead” counts on squash-merged historical branches do not identify unique
unintegrated engineering work.

**Action:** use ROO-007's existing source/destination plan. Integrate baseline and
acceptance packages, then review the order branch against current main with a
native-source and generated-evidence diff. Preserve old package hashes. Validate
the combined result before retiring any checkout. Record which source each
physical unit actually uses. No branch was merged or deleted in this audit.

### P1 Current product direction is buried beneath historical summaries

The latest September 8 direction is **Cube first**, with Beacon manufacture
deferred. It is recorded in the order branch's
`docs/rooster/prototype-order/cube-first-pass-2026-09-08.md` and the vault's
`Reference/2026-09-08 - Cube first pass and supplier recommendation.md`.
However, `Product brief.md`, the beginning of `Execution plan.md`, ROO-010's
description and `order-target.json` still lead with four designs/two complete
Cube+Beacon sets. Later appendices partly supersede earlier prose without making
the current state easy to find. `Execution plan.md` says ROO-009 is Done in its
table while older retained sections still call it unfinished.

ROO-006's pinned draft also predates later decisions; its changed hashes are a
reason to reconcile specific behavior, not to delete the draft or invent new
requirements. For example, Sensor `OPERATION.md` says to reset dwell on confirmed
absence, while the later product decision permits a five-second silent pause and
resumption. Firmware must implement the accepted product behavior, with invalid
or stale input handled separately.

**Action:** maintain one short current-state section: milestone, scope, exact
source, blocking decisions, next test and owner. Move superseded operational text
under clearly dated history. Preserve ROO IDs and task ownership. Do not introduce
a new ticket system or migrate the vault to Incubator merely for this cleanup.
Task metadata currently shows five Active, two Review, five Shaping, three
Blocked, one Done and one Deferred; reduce active work to a small deliverable
batch. The new [product map](../../projects/rooster/README.md) supplies navigation
without changing ticket statuses or pretending the integration is complete.

### P1 The custom connectivity guard accepts a wrong-layer connection

In [check_copper_connectivity.py](../../scripts/ci/check_copper_connectivity.py),
`pad_has_copper` checks layers for zones, but track endpoint/body and via tests
use XY overlap without checking the pad/track layer intersection or via span.
An in-memory **F.Cu-only SMD pad with a B.Cu same-net track at the same position
and no via returns `True`**. That false positive was reproduced with the installed
KiCad Python. See [the reproducible fixture](2026-10-04/copper-layer-repro.py).

This establishes a validator defect; it does not establish that the current
boards contain this defect. The existing guard also checks local copper contact,
not complete connected components across an entire net. Keep DRC and actual
continuity/bring-up measurements alongside it.

**Action:** make track and via checks layer-aware and add independent failure
fixtures for opposite-layer copper, a via that does not span the pad layer and
isolated same-net islands. Retain valid through-hole/through-via and trace-body
positive controls. This is a focused harness repair, not a PCB redesign.

### P1 Manufacturing preparation has outgrown the generic release workflow

[release.yml](../../.github/workflows/release.yml) is manual-dispatch only, has
no dependency on a fresh product acceptance gate and retains an unreachable
two-development-board fallback list. [The JLC config](../../kibot/jlcpcb.kibot.yaml)
exports only SMD positions and expects `LCSC#` metadata. The order branch has
separate all-fitted-reference files and supplier placement corrections precisely
because generic exports are insufficient for these boards. That mature work is
not the main workflow's canonical release path.

Main also contains a README claim that release tags generate files; this audit
corrected that claim to match the workflow. The workflow still replaces a rolling
Gerber ZIP and makes a PR; that is not an immutable record of an actual order.
Supplier-facing RTC QA selection and native QC selection also remain different
in the saved RFQ versus native design. Treat it as an unresolved source/quote
contract, not an interchangeable string.

**Action:** one product release command should select the intended board set,
verify current sources, export full BOM/CPL/fab files, bind approved supplier
offsets, account for both-side/THT work, and freeze checksums/tool versions and
manufacturing process in a candidate manifest. A separate order record binds
the actually submitted bytes. Adapt the existing order tooling first. Required
checks should fail on missing output; publication or an order remains separate.

### P1 The path from breadboard behavior to PCB firmware is still missing

Main has no integrated firmware tree or pinned build for the actual Cube/Sensor.
The preserved Browns pair compiles according to its September build record and
its archive still verifies today. That does not prove current PCB operation.
The 68 logical alarm cases and eight physical scenarios are valuable definitions,
but remain unrun in the inspected specification.

**Action:** integrate the preservation package, then build ROO-011 diagnostics
for the current Cube pins: supply/readback, USB or UART recovery, RTC wake,
buttons/LED, display sequencing and audio. Implement a small ROO-015 slice with
an injected clock and simulated peer: scheduled alarm → presence silence → grace
pause/reset → completion, plus the accepted unreachable-sensor fallback. Keep
the core transition logic testable on a host and hardware drivers behind a small
interface. A legacy/dev-board peer can exercise protocol development before
Beacon manufacture, with that limitation stated. Do not wait for every historic
flash-identification detail before writing PCB-based diagnostics.

### P1 Whole-system energy and mechanical fit remain product risks

Cube's confirmed minimum is roughly one month between battery changes. There
is no measured complete-Cube power budget in the inspected evidence. Beacon's
illustrative model yields about 12 hours continuous or 22 days at 30 active
minutes/day, under unmeasured assumptions; the Beacon endurance target remains
open. A schedule/wake/radio contract is necessary to make duty cycling useful.
These estimates cannot be transferred to Cube.

The current power architecture includes four buck-boost stages per eventual
Cube+Beacon pair. TI specifies a 3 V input startup minimum when output is below
3 V; its lower running-input range is not a depleted-cell restart guarantee.
This supports measuring startup and load pulses, not immediately substituting
another regulator. [TI TPS63070 datasheet](https://www.ti.com/lit/ds/symlink/tps63070.pdf)

Mechanically, Cube documents a **0.055 mm nominal button stem gap** and a service
probe corridor without a completed registering fixture. Sensor records close
carrier/screw clearances and a proposed seal, with physical fit and wet-use
validation pending. The Cube source mixes Blender-derived solids/assembly and
Sensor's CadQuery workflow. Both are legitimate editable assets, but a render
is not a manufacturing tolerance model.

**Action:** measure pack current by state and actual audible duration; determine
the allowable average power from measured usable energy divided by 720 hours.
Use the existing dry, current-limited first-power disposition. Print a button/
connector/service coupon before a whole polished enclosure. Record actual parts,
process tolerances and fit results. Keep the next manufacturing revision driven
by those findings. The earlier Cube prototype scope does not establish protected
battery or unattended-use qualification.

### P2 Evidence, dependencies and generated artifacts need clearer boundaries

The Sensor manifest's seven gallery mismatches show that a live preview and a
frozen evidence bundle currently share paths. Sensor CI regenerates evidence,
while its host tests do not verify the complete source-hash manifest. Cube tests
do verify its saved manifest. This is an inconsistent freshness contract, not
evidence that all old Sensor results are invalid.

The numerical job targets the older devkit-5v path. Main's global dependencies
are lower-bound requirements; the numerical requirements are separate pinned
dependencies. Local Python and CI Python differ, and `make validate-all` describes
a skipped board as part of an all-passed result. There is no single product
command that explains which checks cover which boards and which were skipped.
Documentation generation may commit even when optional SPICE generation fails;
a freshly dated gallery must not imply a fresh complete engineering pass.

**Action:** separate live exports, immutable review inputs and physical run data.
Keep small useful previews; move large regenerable releases to checksum-bound
artifacts only after consumers are updated. Do not blanket-delete generated
files: several are build inputs or preserved supplier evidence. Add explicit
test environments and a required-check inventory with PASS/FAIL/SKIP/NOT_RUN.
Keep physics runs tied to relevant source/assumption changes. Extend a single
product entry point rather than creating another overlapping orchestration layer.

## Cost and manufacturability

All figures below are **September 7–8 USD observations**, not current quotes.
Sources are the vault's `Cost and commercial feasibility.md` and the order
branch's `cube-first-pass-2026-09-08.md` and `quote-progress.md`.

| Cost view | Recorded value | What it means |
| --- | ---: | --- |
| Cube-first manufacturing draft | **$473.47** | Five fabricated/two assembled of each of three designs; two Cube PCB sets plus nine bare spares |
| Its fabrication/options | $143.49 | Prototype batch charges |
| Its priced component purchases | $67.12 | Batch purchases; excludes required RTCs |
| Its assembly services | **$262.86** | About 56% of that incomplete Cube draft |
| Earlier four-design manufacturing draft | $791.07 | Two Cube+Beacon PCB sets plus bare spares; superseded near-term purchasing scope |
| Fitted PCB components per full Cube+Beacon set | **about $63.85** | About $30.73 Cube and $33.12 Beacon, using historical RTC pricing |

These totals exclude significant external parts and/or fabrication/assembly,
depending on the row. The fitted-component figure excludes boards, assembly,
display, radar, speaker, holders, cells, harnesses and enclosures. The manufacturing
draft excludes RTC procurement/related fee changes, external hardware, freight,
tariffs and tax. Do not add component procurement again to a manufacturing total
that already includes it. None establishes a profitable sub-$100 product.

The full-pair fitted-cost concentration is approximately $12.72 for four Coilcraft
inductors, $10.45 for two ESP32-S3 modules, $10.20 for the Beacon switch, $5.31
for four regulators and $4.47 for two RTCs. The switch is a future review target;
the user had already accepted retaining it for the current prototype. Changing
only the RTC would address a relatively small part of recurring cost.

Recommended cost investigations, in order:

1. **Assembly structure:** quote a shared daughterboard panel or deliberate
   consolidation, balanced against access and harness labor. Controls/front alone
   are $216.16 of the current batch draft. They cannot simply be removed while
   keeping the same UX/mechanics; savings must come from a quoted alternative.
2. **Manufacturing process:** the order branch calls for filled/capped vias,
   advanced four-layer geometry and explicit stackup requirements. Examine
   whether the next layout can use less costly geometry/process without losing
   electrical/thermal performance. DRC for an advanced tier does not establish
   low-cost manufacturability. Do not waive the existing process on unchanged files.
3. **Power-stage requirements:** measure state/current peaks, then compare rails,
   load envelopes, inductors and converters. Four shared high-capability stages
   are a plausible cost/area optimization target; a cheaper inductor with only
   matching nominal inductance is not a qualified replacement.
4. **Beacon switch and module size:** review exact electrical/mechanical needs
   and real memory/radio usage. A smaller module or different switch is a new
   compatibility assessment, not a promised drop-in saving.
5. **Complete-set procurement:** maintain one fitted/externally assembled BOM
   with exact variant and quantity. Distinguish prototype sunk/setup spending
   from repeated per-unit cost. Compare 1/10/100-unit scenarios only with dated
   assumptions and real supplier coverage.

The current request reopens cost investigation. It does not itself change the
previously deferred commercial ticket or select a cost-down PCB. A bounded
manufacturability/cost comparison now can prevent another expensive revision
while the broader sales/business assessment remains optional later.

## A development harness suited to electronics

Use progressive disclosure for **navigation and constraints**, and executable
tools for enforcement. The root agent file should identify the product, source
ownership, verification language and where to read next. Board guidance owns
electrical/source/fab contracts; enclosure guidance owns geometry/tolerances;
scripts own reproducibility and independent controls; CI owns selection,
failures and artifacts. Detailed pin maps belong in their existing contracts.

Codex loads instructions along the root-to-working-directory chain at startup;
it does not promise to load every descendant just because a file is edited.
The added root file explicitly routes root-started work to nested guidance.
Keep the files short and avoid copying all the vault into them.
[Official AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

For each engineering change, use this evidence sequence:

| Stage | Evidence required | What it establishes |
| --- | --- | --- |
| Intent and interfaces | Accepted behavior, revision, pins/power/mechanical contract | The question the change must answer |
| Host and CAD checks | Fresh ERC/DRC/netlist checks, meaningful failure fixtures, firmware build, nominal fit | Machine-checkable design constraints |
| Reviewable candidate | Visual diff, BOM/CPL/fab review, exact part/process, source and tool hashes | A reproducible candidate for manufacture |
| Identified bench unit | Unit/PCB revision, firmware hash, instruments, conditions, raw readings and limits | Actual behavior of those specimens |
| Everyday prototype | Assembled operation, measured energy, real presence/fault trials and usability | Progress toward the finished personal product |

The minimal bench record can be a small JSON/CSV plus attachments: unit ID,
hardware revision/rework, firmware hash, test-case ID, instrument, input conditions,
measurement with units, acceptance limit, PASS/FAIL/NOT_RUN and timestamp. Reuse
ROO-006's observability/run-sheet design. A self-hosted board runner should come
after the first repeatable manual/serial test, with exclusive device ownership.

### Relevant practices found online

| Primary source | Useful practice | Recommendation for Forge |
| --- | --- | --- |
| [KiBot documentation](https://kibot.readthedocs.io/en/master/) | Scripted fabrication/documentation outputs | Keep the existing investment; unify the reviewed product exporter |
| [KiCad 10 CLI](https://docs.kicad.org/10.0/en/cli/cli.html) | ERC/DRC with violation exit codes, parity/refill options and jobsets | Reuse native checks; jobsets are an optional simplification, not another parallel required pipeline |
| [Espressif pytest-embedded](https://docs.espressif.com/projects/pytest-embedded/en/latest/) | pytest services for serial devices, flashing and Arduino/IDF targets | Best near-term extension once Cube diagnostics can emit/assert real observations |
| [OpenHTF](https://github.com/google/openhtf) | Test phases, device IDs, measurements, attachments and instrument plugs | Borrow its record structure; adopt a station framework only when repeated fixture testing warrants it |
| [atopile](https://github.com/atopile/atopile) | Circuit modules, interfaces, units/tolerances/assertions and KiCad-oriented builds | Interesting future experiment for a small reusable circuit. Migrating the current clock would add risk before it answers the bench questions |

These are examples of maintained project approaches, not a survey proving an
industry-standard AI harness. The recommendation is to combine focused agent
instructions, established KiCad checks and an actual firmware/bench loop. Adding
more autonomous design tools does not supply missing measurements.

## Prioritized execution plan

These are proposed work packages mapped to existing tasks, not new registered
tickets or claims that their prerequisites are complete.

| Order | Existing scope | Concrete deliverable and completion check |
| --- | --- | --- |
| 1 — P1 | ROO-003/007/009 | Reconcile current Cube-first summary and integrate preserved firmware, acceptance and order sources. Check native changes and current-main rename compatibility; all links/build inputs resolve |
| 2 — P1 | Harness repair alongside ROO-007 | Fix the wrong-layer copper false positive; add failure fixtures, explicit skip reporting and required environment/check inventory. Recheck affected boards |
| 3 — P1 | ROO-010/013 | One exact Cube candidate: reconcile RTC variant/supply, U3/U6/connector placements, via/stackup, external parts and first-power access; refresh the actual quote only when resuming ordering |
| 4 — P1 | ROO-011 plus initial ROO-015/006 | Pinned diagnostic build and runnable host alarm slice with current behavior. Per-board first-power procedure has actual limits, probe points and stop conditions before energizing hardware |
| 5 — P1 | ROO-014/012/016 | After a separate concrete purchase decision if still needed, identify received units, bring up rails/peripherals, measure pack load/startup and test a small mechanical coupon |
| 6 — P2 | ROO-015/016/017 | Complete Cube experience and measured battery/fit reliability; then integrate/qualify Beacon presence and the paired system |
| 7 — P2 | Cost review, ROO-008 if resumed | Use measured requirements and complete BOM to compare a manufacturing/cost revision and any later commercial proposition |

Integration comes first because it prevents work on the wrong revision. Firmware
and bench preparation can advance while sourcing or fabrication proceeds; a
month-long endurance trial is not a prerequisite to ordering engineering PCBs.
Historical flashed-revision identification remains useful but need not block
new diagnostics against known PCB contracts. Keep one owner for shared source
moves, product status and release manifests. Independent electrical, firmware
and mechanical work needs frozen interfaces and a combined integration check.

The next useful milestone is **an identified Cube running diagnostic and alarm
firmware, with measured power and physically demonstrated control/service fit**.
The next useful spending decision compares the exact current prototype packet
against the cost of a deliberate manufacturability revision; another general
planning pass is not required to make that comparison concrete.

## Changes delivered by this audit

Added a small root/nested `AGENTS.md` layer for boards, mechanics, scripts and CI,
the Rooster engineering map, this dated audit, source/check evidence and the
connectivity reproducer. Corrected the root README's tag-release claim. Existing
native hardware, firmware archives, supplier packages, Obsidian decisions/task
statuses, check implementations and worktrees were preserved. No commit, push,
purchase, supplier contact or hardware qualification was performed.
