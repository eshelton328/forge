#!/usr/bin/env python3
"""Verify source continuity, allowing only the recorded main J4 fit correction.

Run with KiCad Python. Historical reports are never overwritten; --output-dir
optionally saves new comparison reports in a directory that does not yet exist.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from scripts.alarm.order_parts import BOARDS, baseline_source, verify_transition
from scripts.alarm.header_fit import OLD, NEW


def digest(data):
    return hashlib.sha256(data).hexdigest()


def circuit(tree):
    return {
        "nodes": sorted((n.get("name"), p.get("ref"), p.get("pin"))
                        for n in tree.findall("./nets/net") for p in n.findall("node")),
        "components": sorted((c.get("ref"), c.findtext("value"), c.findtext("footprint"),
                              sorted(p.get("name") for p in c.findall("property")
                                     if p.get("name") in {"dnp", "exclude_from_bom", "exclude_from_pos_files"}))
                             for c in tree.findall("./components/comp")),
    }


def compare_geometry(board, before, after):
    expected, actual = copy.deepcopy(before), copy.deepcopy(after)
    expected.pop("pcb_sha256")
    actual.pop("pcb_sha256")
    if board == "alec-main":
        header = expected["footprints"]["J4"]
        assert header["footprint"] == OLD, "Unexpected baseline J4 footprint"
        assert len(header["pads"]) == 4
        assert {p["number"] for p in header["pads"]} == {"1", "2", "3", "4"}
        header["footprint"] = NEW
        for pad in header["pads"]:
            assert pad["drill"] == [1.0, 1.0], "Unexpected baseline J4 drill"
            pad["drill"] = [1.1, 1.1]
    assert expected == actual, board + " native geometry differs"
    return actual


def compare_circuit(board, before, after):
    expected, actual = circuit(before), circuit(after)
    if board == "alec-main":
        header, = [c for c in expected["components"] if c[0] == "J4"]
        assert header[2] == OLD, "Unexpected baseline J4 footprint"
        expected["components"] = [
            (ref, value, NEW if ref == "J4" else footprint, flags)
            for ref, value, footprint, flags in expected["components"]
        ]
    assert expected == actual, board + " exported circuit differs"
    return actual


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        help="Save new reports here; refuse an existing directory")
    args = parser.parse_args(argv)
    if args.output_dir is not None and args.output_dir.exists():
        parser.error("Refusing to overwrite an existing comparison directory")
    from scripts.physics.export_geometry import export

    source_hashes = verify_transition()
    geometry, netlists = [], []
    for board in BOARDS:
        native = ROOT / "boards" / board / (board+".kicad_pcb")
        with tempfile.TemporaryDirectory(prefix="rooster-source-comparison-") as tmp:
            old_path = Path(tmp) / native.name
            old_path.write_text(baseline_source(native.relative_to(ROOT)))
            old, current = export(old_path), export(native)
        before_hash, after_hash = old["pcb_sha256"], current["pcb_sha256"]
        new = compare_geometry(board, old, current)
        allowance = "main J4 footprint and four 1.00-to-1.10 mm drills" if board == "alec-main" else "none"
        geometry.append({"board": board, "baseline_sha256": before_hash, "current_sha256": after_hash,
                         "geometry_sha256": digest(json.dumps(new, sort_keys=True, separators=(",", ":")).encode()),
                         "footprints": len(new["footprints"]), "tracks": len(new["tracks"]),
                         "vias": len(new["vias"]), "copper_polygons_records": len(new["copper"]),
                         "allowed_change": allowance,
                         "result": "MATCH_WITH_RECORDED_J4_CHANGE" if board == "alec-main" else "EXACT_GEOMETRY_MATCH"})
        path = native.parent / "review/netlist.xml"
        original = baseline_source(path.relative_to(ROOT))
        new = compare_circuit(board, ET.fromstring(original), ET.parse(path).getroot())
        netlists.append({"board": board, "netlist_sha256": digest(path.read_bytes()),
                         "baseline_netlist_sha256": digest(original.encode()),
                         "component_count": len(new["components"]), "net_nodes": len(new["nodes"]),
                         "allowed_change": "main J4 footprint" if board == "alec-main" else "none",
                         "result": "MATCH_WITH_RECORDED_J4_CHANGE" if board == "alec-main" else "EXACT_CONNECTIVITY_VALUES_FOOTPRINTS_AND_FIT_FLAGS_MATCH"})
        print(board, "geometry and connectivity match", flush=True)
    if args.output_dir is None:
        return
    args.output_dir.mkdir(parents=True, exist_ok=False)
    for name, scope, results in [
        ("native-geometry-comparison.json", "KiCad-loaded baseline/current geometry matches except the recorded main J4 footprint and four 1.00-to-1.10 mm drills. All other exported geometry and connectivity must match exactly. Ordering fields and model transforms are separately covered by source-token comparison. No physical measurement.", geometry),
        ("native-netlist-comparison.json", "Saved KiCad XML compared with the original reviewed export: all reference/value/footprint/fit flags and every named-net/reference/pin tuple, allowing only the recorded main J4 footprint change. This command does not regenerate netlists. Ordering fields are checked separately against sourcing selections.", netlists),
    ]:
        (args.output_dir / name).write_text(json.dumps({"scope": scope, "verifier_sha256": digest(Path(__file__).read_bytes()),
                                            "source_transition_sha256": source_hashes,
                                            "boards": results}, indent=2)+"\n")


if __name__ == "__main__":
    main()
