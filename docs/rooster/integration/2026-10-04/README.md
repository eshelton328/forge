# ROO-007 first integration handoff — October 4, 2026

The local branch `codex/rooster-integrated-baseline` combines current main,
preserved breadboard firmware, the Cube acceptance/bench package, and the latest
prototype ordering work. Start at the [Rooster product map](../../../../projects/rooster/README.md)
or [machine-readable manifest](../../../../projects/rooster/project.json).
Native board, enclosure, library and generator paths are unchanged.

This completes the bounded **first handoff** in ROO-007. Broad historical issue
reconciliation and optional worktree retirement remain later work. Obsidian owns
ROO task specifications and statuses; no GitHub issue was assigned, closed or
inferred from a ROO number. No product firmware or manufacturing release exists.

## Applied integration and recovery ledger

| Input | Applied action and recovery reference |
| --- | --- |
| Main `a56d8900c386f5e4f612d92436ebecb11c258c24` | New isolated branch from this commit; all 18 non-README rename changes retained byte for byte. Root README receives navigation additions. |
| ROO-002 `ffd6919b25867d8c8ac212e057060805acadf475`, `59e0e42ede19a06d63609b489e1fb50a523c7e49` | Cherry-picked only the preservation/selection commits as `55d0914ac6622ab8c5dc0aae05e873ed019e5ec7` and `c60d876f2c7a0563a317e5f6b79920fdf1cb2ae2`; 58 package files match the original source. Old Sensor branch history was not replayed. |
| ROO-004 `f0b8dca2c0223e456426645712087c3667b4a6c1` | Cherry-picked as `cbf10f071828e851d8beab42f8a29ca1a52301da`; all 14 review/bench files preserved unchanged. |
| Ordering `1e8ee9512929b6ccc40a2d7a813928b0d3307015` | Merged with history at `c53fc800316b509785961fa476465852356e178d`; all 407 changed/added files since `0d0d8af` match the ordering branch. Includes capacitor/purchasing overlays and main J4 drill correction. |
| Earlier October 4 audit/navigation work in the main working tree | Copied the dated audit/evidence and scoped agent guidance. Updated the integration product index and added firmware guidance. The audit remains a pre-integration snapshot. |
| Product and firmware paths | Added `projects/rooster/project.json`, separate application/shared/diagnostic READMEs under `firmware/rooster`, and `releases/rooster/README.md`. Firmware implementation remains planned. |
| Existing boards, libraries, mechanical sources, source worktrees, original Arduino sketches and older clone | Retained in place. No native-source moves, worktree removals or original-sketch edits. Existing main audit edits and user logs remain in the original checkout. |

[source-preservation.json](source-preservation.json) records all 479 imported
file hashes, original and reachable Git refs, and frozen-package checks.
The preserved firmware archive SHA-256 remains
`f281711b3b2c08c187c220e718618285ba8e4165403789cf4ee905dfc42791d5`.
Its verifier also compared retained originals and both dependency archives.
The integration's engineering source revision is `c53fc800316b509785961fa476465852356e178d`;
subsequent changes in this handoff are documentation and recorded evidence.

To recover the combined native baseline, create a checkout at that merge commit.
To recover one package, the reachable firmware/acceptance commits above remain
ancestors of this branch; their preserved files match the original source refs.
To check this handoff's recorded hashes from the repository root:

```sh
python3 - <<'PY'
import hashlib, json
from pathlib import Path
p = Path('docs/rooster/integration/2026-10-04/source-preservation.json')
for item in json.loads(p.read_text())['files']:
    actual = hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()
    assert actual == item['sha256'], item['path']
print('All 479 imported files match the dated handoff.')
PY
```

A later intentional source change should differ from this historical capture;
record its own review instead of editing these hashes.

## Verification performed

[Commands and exits](commands.json), [specialized commands](specialized-commands.json)
and adjacent logs record this run. Main runtime: host Python 3.9.6 / pytest 8.4.2,
KiCad CLI 10.0.1 and its bundled Python/pcbnew. Git inputs were combined before
these checks; no tracked source or historical report was changed by validation.

| Check | Result and scope |
| --- | --- |
| `python3 -m pytest tests/ -q -ra` | 145 passed, 1 optional physics module skipped because SciPy is missing, 14 dependency deprecation warnings. No full numerical-stack/solver rerun claimed. |
| Baseline `verify.py --compare-originals` | 15 candidates, 15 original files, two dependency archives and archive contents match; originals still match. Historical build records preserved, sketches not recompiled. |
| `python3 scripts/alarm/order_parts.py --check` | Native purchasing-field overlay and source-transition checks pass. |
| `make check-all` | All seven boards: fresh ERC, refilled DRC/schematic parity, copper guard and all eight named board/fab combinations pass. Each configured fab appears in the passing log. |
| `make validate-all` | Six declared board-intent configurations pass; Sensor has no `checks.yml` and is handled by its specialized checks below. |
| Fresh netlists and Cube checks | Five fresh exports (three Cube, Sensor, retained devkit input); 487 Cube circuit/interface checks and 153 layout guards pass. |
| Fresh Sensor checks | 47 schematic-interface checks, BOM metadata/packages, eight service checks and layout/CAD interface guards pass. |
| Original imports / frozen package bindings | 58 firmware + 14 acceptance + 407 ordering files preserved; 87 fabrication-candidate and 17 supplier-RFQ hash bindings match. |
| Navigation / discovery | Product manifest paths and added local documentation links resolve. CI's existing shared-script/library changes select all boards; retained paths need no discovery rewrite. |

Specialized scripts write reports into their input tree, so they ran in a
temporary archive checkout of `c53fc80`, with freshly exported netlists. Their
new outputs are in [fresh-reports](fresh-reports); [fresh-netlists.json](fresh-netlists.json)
records export hashes. Original saved evidence was not replaced. Export hashes
can differ because of absolute source paths/timestamps; the fresh circuit
assertions and DRC parity establish the checked connectivity scope.

The macOS fab wrapper emitted spurious missing `-` rule warnings from its list
parser; every actual configured fab ran and passed. KiCad/pcbnew emitted wxApp
diagnostics and exited successfully. The copper guard retains the known
wrong-layer limitation documented in the [audit](../../../audits/2026-10-04-forge-rooster.md);
it does not prove complete physical connectivity. Full CAD rebuild, physics
solvers, remote GitHub Actions and physical/functional tests were not run.
Integration preserves historical evidence without expanding its validity.

## Consumer handoff and remaining work

- **ROO-011:** implement Cube diagnostics at `firmware/rooster/diagnostics/alarm`;
  begin with pinned builds, programming/recovery, safe defaults and input checks.
  Use current native contracts, the preserved port matrix and Cube bench cases.
- **ROO-015/013:** consume the separate alarm/sensor/shared paths. Define protocol
  and application behavior from Obsidian; historical sketches remain references.
- **ROO-010:** use current native sources and existing immutable candidates.
  Reconcile QA RFQ versus QC native RTC, remaining placement/orientation,
  stackup/fill-cap/assembly scope, external parts and the complete Cube quote.
- **ROO-016:** enclosure paths and generator inputs are unchanged. Reconcile the
  exact integrated board/export when new fit evidence is produced.

The source worktrees were clean before integration and remain available. This
task owns the integration checkout; no other active Forge editor was observed.
The Obsidian hub, source inventory and ROO-007 execution record receive this
branch/path and its final documentation commit. No purchase or supplier action
is part of this handoff.

ROO-007 AC01/AC02 and the affected AC03 checks are covered for this bounded
integration; AC04 retains Obsidian authority with no new mapped issue; AC05 is
the published consumer handoff. The ticket remains **Active**, because broad
historical issue reconciliation is outside this first handoff. No predecessor's
unrun physical acceptance is silently marked complete.
