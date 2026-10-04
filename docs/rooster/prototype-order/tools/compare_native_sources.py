#!/usr/bin/env python3
"""Compare original/current KiCad geometry and exported connectivity (KiCad Python)."""
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from scripts.alarm.order_parts import BOARDS, ORDER, baseline_source, verify_transition
from scripts.physics.export_geometry import export


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


def main():
    verify_transition()
    cache = ROOT / ".cache/prototype-order/source-checks"
    cache.mkdir(parents=True, exist_ok=True)
    geometry, netlists = [], []
    for board in BOARDS:
        native = ROOT / "boards" / board / (board+".kicad_pcb")
        old_path = cache / (board+"-baseline.kicad_pcb")
        old_path.write_text(baseline_source(native.relative_to(ROOT)))
        old, new = export(old_path), export(native)
        before_hash, after_hash = old.pop("pcb_sha256"), new.pop("pcb_sha256")
        assert old == new, board+" native geometry differs"
        geometry.append({"board": board, "baseline_sha256": before_hash, "current_sha256": after_hash,
                         "geometry_sha256": digest(json.dumps(new, sort_keys=True, separators=(",", ":")).encode()),
                         "footprints": len(new["footprints"]), "tracks": len(new["tracks"]),
                         "vias": len(new["vias"]), "copper_polygons_records": len(new["copper"]),
                         "result": "EXACT_GEOMETRY_MATCH"})
        path = native.parent / "review/netlist.xml"
        old, new = circuit(ET.fromstring(baseline_source(path.relative_to(ROOT)))), circuit(ET.parse(path).getroot())
        assert old == new, board+" exported circuit differs"
        netlists.append({"board": board, "netlist_sha256": digest(path.read_bytes()),
                         "component_count": len(new["components"]), "net_nodes": len(new["nodes"]),
                         "result": "EXACT_CONNECTIVITY_VALUES_FOOTPRINTS_AND_FIT_FLAGS_MATCH"})
        print(board, "geometry and connectivity match", flush=True)
    for name, scope, results in [
        ("native-geometry-comparison.json", "KiCad-loaded original/current outlines, footprint positions/values/pads, tracks, vias and saved filled copper; exact equality after removing only PCB file hash. Hidden ordering fields and model transforms separately covered by source-token comparison. No physical measurement.", geometry),
        ("native-netlist-comparison.json", "Fresh KiCad XML compared with the original reviewed export: all reference/value/footprint/fit flags and every named-net/reference/pin tuple. Ordering fields are checked separately against sourcing selections.", netlists),
    ]:
        (ORDER / name).write_text(json.dumps({"scope": scope, "verifier_sha256": digest(Path(__file__).read_bytes()),
                                            "boards": results}, indent=2)+"\n")


if __name__ == "__main__":
    main()
