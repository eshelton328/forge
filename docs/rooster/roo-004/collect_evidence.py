"""Collect ROO-004 static provenance; never modifies native board sources.

Run with KiCad Python, from this worktree root, after exporting the three
native schematics as kicadxml into .cache/roo-004/<board>.xml.
"""
from pathlib import Path
import csv
import hashlib
import json
import platform
import subprocess
import xml.etree.ElementTree as ET

import pcbnew
import wx

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "evidence"
app = wx.App(False)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def netlist(path):
    root = ET.parse(path).getroot()
    components = {
        c.attrib["ref"]: {k: c.findtext(k) for k in ["value", "footprint"]}
        for c in root.findall("./components/comp")
    }
    nets = {
        n.attrib["name"]: sorted(
            (p.attrib["ref"], p.attrib["pin"]) for p in n.findall("node")
        )
        for n in root.findall("./nets/net")
    }
    return components, nets


manifest_path = ROOT / "boards/alec-main/review/qa-manifest.json"
manifest = json.loads(manifest_path.read_text())
bindings = {
    path: {"expected": digest, "actual": sha(ROOT / path)}
    for group in ["files", "evidence"]
    for path, digest in manifest[group].items()
}
assert all(row["expected"] == row["actual"] for row in bindings.values())
boards = {}
for kind in ["main", "controls", "front"]:
    name = "alec-" + kind
    directory = ROOT / "boards" / name
    fresh = ROOT / ".cache/roo-004" / (name + ".xml")
    components, nets = netlist(fresh)
    assert (components, nets) == netlist(directory / "review/netlist.xml"), name
    pcb = pcbnew.LoadBoard(str(directory / (name + ".kicad_pcb")))
    pads = {}
    probe_points = {}
    for footprint in pcb.GetFootprints():
        ref = footprint.GetReference()
        for pad in footprint.Pads():
            key = ref + "." + pad.GetNumber()
            pads.setdefault(key, set()).add(pad.GetNetname())
            if ref.startswith("TP") or ref == "J7":
                probe_points[key] = {
                    "net": pad.GetNetname(),
                    "native_pcb_xy_mm": [
                        pcbnew.ToMM(pad.GetPosition().x),
                        pcbnew.ToMM(pad.GetPosition().y),
                    ],
                    "layer": pcb.GetLayerName(pad.GetLayer()),
                }
    checked = 0
    for net, nodes in nets.items():
        for ref, pin in nodes:
            assert pads.get(ref + "." + pin) == {net}, (name, ref, pin, net)
            checked += 1
    bbox = pcb.GetBoardEdgesBoundingBox()
    with (directory / "review/bom.csv").open() as handle:
        bom = list(csv.DictReader(handle))
    boards[name] = {
        "native_export_matches_saved_components_and_net_topology": True,
        "schematic_nodes_matched_to_native_pcb": checked,
        "copper_layers": pcb.GetCopperLayerCount(),
        "edge_bbox_including_0p05mm_stroke_mm": [pcbnew.ToMM(bbox.GetWidth()), pcbnew.ToMM(bbox.GetHeight())],
        "probe_points": probe_points,
        "components": components,
        "nets": nets,
        "bom_rows": len(bom),
        "blank_mpn_refs": [r["Reference"] for r in bom if not r["MPN"]],
        "dnp_refs": [r["Reference"] for r in bom if r["Assembly"] == "DNP"],
        "fresh_export_sha256": sha(fresh),
    }
sources = [
    manifest_path,
    ROOT / "boards/alec-main/HARNESS.md",
    ROOT / "boards/alec-main/review/TEST-REPORT.md",
    ROOT / "enclosures/alec/pcb-revision/README.md",
    ROOT / "boards/esp32s3-devkit-5v/review/battery-sensing.md",
    ROOT / "boards/esp32s3-devkit-5v/review/gpio-map.csv",
]
result = {
    "review_date": "2026-09-07",
    "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "comparison_revision": "dc57b550ebe8c1943e7830468d73af3f93c5bb73",
    "python": platform.python_version(),
    "kicad": pcbnew.GetBuildVersion(),
    "method": "Fresh schematic export compared with saved net topology/components; every schematic node matched to native PCB pad net. This does not prove complete copper graph continuity or physical operation.",
    "physical_tests_run": False,
    "manufacturing_release": False,
    "saved_qa_bindings": bindings,
    "additional_sources": {str(p.relative_to(ROOT)): sha(p) for p in sources},
    "boards": boards,
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "source-review.json").write_text(json.dumps(result, indent=2) + "\n")
print("Verified", len(bindings), "saved QA bindings")
for name, row in boards.items():
    print(name, row["schematic_nodes_matched_to_native_pcb"], "native schematic/PCB nodes;", row["bom_rows"], "BOM rows;", len(row["blank_mpn_refs"]), "blank MPNs")
