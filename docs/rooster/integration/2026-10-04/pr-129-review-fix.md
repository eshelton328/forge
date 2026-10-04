# PR #129 source-comparison correction

October 4, 2026. Reviewed source: `2a761fdb7dc7eda7f635ae30647fd048f937f7bf`
plus the comparator/runbook correction and regression tests in this commit.
No native designs, saved netlists or historical result hashes changed.

The comparator now applies exactly the recorded main J4 footprint and four
1.00-to-1.10 mm drill changes to its expected baseline before comparing actual
KiCad geometry. The netlist comparison permits only that footprint identity
change. Source-transition verification still precedes both comparisons.
Default execution verifies without writing reports; `--output-dir` writes new
reports only to a previously nonexistent directory.

## Static verification

Host Python 3.9.6, pytest 8.4.2; KiCad CLI 10.0.1 and bundled Python 3.9.13.
Commands ran at the repository root and exited zero:

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_rooster_source_comparison.py tests/test_rooster_header_fit.py tests/test_rooster_order_parts.py -q -ra` | 37 passed, including failure controls for unrelated geometry, copper layer/connectivity, hole, net, pin, value, footprint and DNP changes. Existing output directories are rejected. |
| `python3 -m pytest tests/ -q -ra` | 164 passed, one optional physics module skipped because SciPy is unavailable; 14 dependency deprecation warnings. |
| KiCad Python: `docs/rooster/prototype-order/tools/compare_native_sources.py --output-dir .cache/pr129-source-comparison-fix` | All four boards pass; separate new geometry/netlist reports emitted. |
| KiCad Python: `docs/rooster/prototype-order/tools/compare_native_sources.py` | All four boards pass; historical geometry/netlist reports and both transition records remain byte-identical. |
| `git diff --check` | Passed. |

KiCad emitted its existing wxApp/duplicate-image-handler diagnostics and exited
successfully. These comparisons inspect saved copper and saved netlists; no new
ERC/DRC, netlist export, solver, nominal enclosure fit or physical test was run.

Comparator SHA-256:
`642450f42c490db99752bd46e66cfc9cfd1b1f7a500368f8cc300ac2ca8affb1`.
Regression-test SHA-256:
`0d7c0c9f3a1142a8fb8bae58373719165e1feaeee65f023f27bad3d58922499e`.

The original `source-preservation.json` remains the immutable first-handoff
snapshot. Its comparator and prototype-order README entries now intentionally
differ because of this correction; the remaining 477 imported files still match.
Do not refresh the historical manifest to erase these later changes.
