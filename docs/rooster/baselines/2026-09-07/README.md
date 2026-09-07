# ROO-002 — breadboard firmware reference, September 7, 2026

The 15 inventoried sketches are preserved unchanged. Erik confirmed during this task that they are old breadboard firmware and that **the PCB designs in The Forge should determine the new firmware pin mapping**. This capture recovers a software reference and its build evidence. Erik subsequently identified `cube_browns.ino` and `beacon_browns.ino` as the most relevant pair (“I believe”); both compile unchanged as separate targets. [Selection and full hashes](selected-reference.json) preserve that qualified identification. It does not establish the exact last-flashed bytes or prove operation on the current ALEC boards.

Hardware comparison is pinned to `dc57b550ebe8c1943e7830468d73af3f93c5bb73`, the inspected S1.1 worktree revision, on a new local branch `codex/roo-002-firmware-baseline`. It is an inspection reference, not a manufacturing freeze. No board design or original sketch was changed.

## Deliverables

- [Full manifest](manifest.json): full SHA-256 hashes, original paths, includes, source pin definitions, source headers, dependency versions/file hashes and limitations.
- [Candidate inventory](CANDIDATES.md) and [complete derived code index](candidate-analysis.json): individual roles, pins, includes and all struct layouts. The sealed manifest's message-name filter omits `CubeToBeacon`/`BeaconToCube`; the derived index includes them. The original archive remains unchanged.
- [Preserved originals and libraries](originals-2026-09-07.tar.gz) with [archive checksum](originals-2026-09-07.tar.gz.sha256).
- [Build report](BUILD-REPORT.md), [raw logs, commands and properties](build-records/installed-core-3.3.7/results.json).
- [PCB compatibility matrix](COMPATIBILITY.md): old/new assignments and required firmware adaptations.
- [Physical prototype ledger](PHYSICAL-LEDGER.md): user reports, historical evidence and unresolved identification.

## Preservation boundary

Source root: `/Users/erik/Workspaces/Electronics/Arduino`. All 14 original candidate folders, containing 15 files, are captured with their original filenames and folder relationships. All 15 full hashes match both their source files and the earlier inventory prefixes. There are 12 distinct content hashes; all three duplicate pairs retain their separate paths and roles. An additional 16 sketches outside the original inventory are indexed in the manifest, with hashes and explicit disposition; their originals remain in place, but they are not part of this 15-candidate build study.

The archive contains `snapshot/Arduino`, `snapshot/manifest.json`, per-file `snapshot/SHA256SUMS`, and complete copies of the installed **U8g2 2.35.30** and **MyLD2410 1.2.7** libraries as nested tar archives, including their license/source files. These are the versions used for today's build experiment; they are not asserted to be the versions used for the breadboard's last upload. Arduino/ESP32 toolchain packages are identified in the build report and logs, rather than vendored in this archive.

The archive and extracted snapshot have read-only permissions on this machine. Checksums detect changes; these permissions are not a hardware-enforced immutable/WORM store. Treat this capture as append-only: any later evidence or corrections belong outside the archive or in a new dated capture. `capture.py` refuses to replace an existing snapshot.

From this directory, verify archive contents and the retained original sketches:

```sh
python3 verify.py --compare-originals
```

Omit `--compare-originals` on a different machine. To recreate the ignored, extracted snapshot for builds, first verify the archive, then run `tar -xzf originals-2026-09-07.tar.gz` in this directory. The build runner creates its own writable copies and separately extracts the captured libraries under `.work/`. No build modifies the snapshot.

## What can proceed

ROO-013/011/015 can use the native PCB contracts and this explicit port matrix for interface design, diagnostics and application development. Erik's direction does not require making the PCB match the old breadboard, or recovering a particular historical flash before drafting PCB-based firmware. ROO-007 has a verified preservation artifact to consume when source organization is decided; this task has not moved or deleted sources.

The exact historical flashed pair, physical modules/revisions, original upload settings, module firmware and manufactured-order mapping remain open under D02. Keep those facts separate from a newly reproducible host build. Final ROO-002 acceptance still needs the physical identification required by AC02, or an explicit revision of that criterion; no such waiver is assumed.

The Obsidian task is the status record: `/Users/erik/Documents/Obsidian/Projects/Rooster/Tasks/ROO-002 - Identify the working firmware and physical baseline.md`.
