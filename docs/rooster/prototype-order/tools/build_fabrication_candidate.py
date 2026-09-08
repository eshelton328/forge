#!/usr/bin/env python3
"""Export four source-bound fabrication candidates for CAM and quote review.

Does not add rails/panels, change native sources, approve substitutions, submit
files to a supplier or authorize manufacturing. Refuses an existing output path.
"""
import argparse
import csv
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
BOARDS = {"alec-main": 4, "alec-controls": 2, "alec-front": 2, "alec-sensor": 4}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--kicad-cli", default="/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli")
    args = parser.parse_args()
    dst = args.output.resolve()
    assert not dst.exists(), "Refusing to overwrite an existing candidate"
    selection = json.loads((HERE / "selection-audit.json").read_text())
    for relative, digest in selection["input_sha256"].items():
        assert sha(ROOT / relative) == digest, "Stale selection audit: " + relative
    placements = json.loads((HERE / "draft-quote-inputs/manifest.json").read_text())
    assert placements["source_mpn_fields_updated"] is True
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    report = {"status": "FABRICATION_CANDIDATE_FOR_CAM_AND_QUOTE_REVIEW_NOT_ORDER_RELEASE",
              "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "native_source_commit": commit,
              "kicad_version": subprocess.check_output([args.kicad_cli, "version"], text=True).strip(),
              "generator_sha256": sha(Path(__file__)),
              "selection_audit_sha256": sha(HERE / "selection-audit.json"),
              "origin": "Native drill/place origin; all four sources currently use the default (0,0). Gerbers, drills and CPL share this origin; no bottom X reflection or supplier rotation correction applied.",
              "processing": "Single product outlines; no rails or panel arrays generated. Supplier processing rails/fiducials, detachment clearance, counting and shipped format require review.",
              "boards": {}}
    dst.mkdir(parents=True)
    for board, copper_layers in BOARDS.items():
        source_dir = ROOT / "boards" / board
        native = source_dir / (board+".kicad_pcb")
        source_hashes = {}
        for source in sorted(source_dir.glob("*.kicad_*")):
            if source.suffix not in {".kicad_pcb", ".kicad_sch", ".kicad_pro", ".kicad_dru"}:
                continue
            relative = str(source.relative_to(ROOT))
            committed = subprocess.check_output(["git", "show", commit+":"+relative], cwd=ROOT)
            assert committed == source.read_bytes(), "Native source not committed: " + relative
            source_hashes[relative] = sha(source)
        assert placements["boards"][board]["native_pcb_sha256"] == sha(native)
        board_dir = dst / board
        gerbers = board_dir / "gerbers"
        gerbers.mkdir(parents=True)
        layers = ["F.Cu"] + (["In1.Cu", "In2.Cu"] if copper_layers == 4 else [])
        layers += ["B.Cu", "F.Paste", "B.Paste", "F.SilkS", "B.SilkS", "F.Mask", "B.Mask", "Edge.Cuts"]
        commands = [
            [args.kicad_cli, "pcb", "export", "gerbers", "--layers", ",".join(layers),
             "--exclude-value", "--no-x2", "--no-netlist", "--subtract-soldermask",
             "--disable-aperture-macros", "--use-drill-file-origin", "--precision", "6",
             "--check-zones", "-o", str(gerbers)+"/", str(native)],
            [args.kicad_cli, "pcb", "export", "drill", "--format", "excellon",
             "--drill-origin", "plot", "--excellon-units", "mm", "--excellon-zeros-format", "decimal",
             "--excellon-oval-format", "alternate", "--excellon-separate-th",
             "--generate-report", "--report-path", str(board_dir / "drill-report.txt"),
             "-o", str(gerbers)+"/", str(native)],
        ]
        logs = []
        for command in commands:
            result = subprocess.run(command, text=True, capture_output=True)
            assert result.returncode == 0, result.stdout+result.stderr
            logs.append({"command": command, "stdout": result.stdout, "stderr": result.stderr})
        (board_dir / "export-log.json").write_text(json.dumps(logs, indent=2)+"\n")
        expected = {".gtl", ".gbl", ".gtp", ".gbp", ".gto", ".gbo", ".gts", ".gbs", ".gm1"}
        if copper_layers == 4:
            expected.update({".g1", ".g2"})
        files = [p for p in gerbers.iterdir() if p.suffix in expected or p.suffix == ".drl"]
        assert {p.suffix for p in files} == expected | {".drl"}, [p.name for p in gerbers.iterdir()]
        assert {p.name for p in files if p.suffix == ".drl"} == {board+"-PTH.drl", board+"-NPTH.drl"}
        for source in files:
            assert source.stat().st_size > 0
        for filename, digest in placements["boards"][board]["files"].items():
            source = HERE / "draft-quote-inputs" / filename
            assert sha(source) == digest, filename
            shutil.copyfile(source, board_dir / filename)
        archive = board_dir / (board+"-gerbers.zip")
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for path in sorted(files):
                z.write(path, path.name)
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert set(z.namelist()) == {p.name for p in files}
        for relative, digest in source_hashes.items():
            assert sha(ROOT / relative) == digest, "Exporter changed native source: " + relative
        report["boards"][board] = {"copper_layers": copper_layers,
                                    "requested_fabricated": 5, "requested_assembled": 2,
                                    "fitted_references": placements["boards"][board]["fitted_references"],
                                    "source_sha256": source_hashes,
                                    "gerber_layers": layers,
                                    "archive_members": sorted(p.name for p in files),
                                    "file_sha256": {str(p.relative_to(board_dir)): sha(p)
                                                    for p in sorted(board_dir.rglob("*")) if p.is_file()}}
        print(board, "fabrication candidate exported", flush=True)
    (dst / "manifest.json").write_text(json.dumps(report, indent=2)+"\n")


if __name__ == "__main__":
    main()
