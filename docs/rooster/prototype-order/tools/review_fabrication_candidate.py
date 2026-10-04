#!/usr/bin/env python3
"""Compare actual Gerber/drill archives with native KiCad hole/outline geometry.

Run --native with KiCad Python, then --cam with Gerbonara/CairoSVG Python.
This checks exported geometry, layer coverage and placement counts, not supplier
acceptance, component suitability, copper connectivity or manufacturing release.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import warnings
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def native(candidate, output, manifest):
    import pcbnew as p
    result = {"candidate_manifest_sha256": sha(candidate / "manifest.json"), "boards": {}}
    for name, entry in manifest["boards"].items():
        path = ROOT / "boards" / name / (name + ".kicad_pcb")
        assert sha(path) == entry["source_sha256"][str(path.relative_to(ROOT))]
        board = p.LoadBoard(str(path))
        origin = board.GetDesignSettings().GetAuxOrigin()

        def point(v):
            return [(v.x - origin.x) / 1e6, -(v.y - origin.y) / 1e6]

        holes = {"pth": [], "npth": []}
        for fp in board.GetFootprints():
            for pad in fp.Pads():
                if not pad.GetDrillSize().x:
                    continue
                shape = pad.GetEffectiveHoleShape()
                group = "npth" if pad.GetAttribute() == p.PAD_ATTRIB_NPTH else "pth"
                holes[group].append({"start": point(shape.GetStart()), "end": point(shape.GetEnd()),
                                     "diameter": shape.GetWidth() / 1e6})
        for via in board.GetTracks():
            if not isinstance(via, p.PCB_VIA):
                continue
            assert via.GetViaType() == p.VIATYPE_THROUGH, "Blind/buried via needs explicit review"
            pos = point(via.GetPosition())
            holes["pth"].append({"start": pos, "end": pos, "diameter": via.GetDrillValue() / 1e6})
        outline = []
        for drawing in board.GetDrawings():
            if drawing.GetLayer() != p.Edge_Cuts:
                continue
            assert drawing.GetShapeStr() == "Line", "Extend comparator before accepting curved outlines"
            outline.append({"start": point(drawing.GetStart()), "end": point(drawing.GetEnd())})
        result["boards"][name] = {"native_pcb_sha256": sha(path), "holes": holes, "outline": outline,
                                  "copper_layers": board.GetCopperLayerCount()}
    write(output / "native-reference.json", result)


def matching(a, b, tolerance):
    def close(x, y):
        return all(abs(i - j) <= tolerance for i, j in zip(x, y))
    ends = (close(a["start"], b["start"]) and close(a["end"], b["end"])) or (
        close(a["start"], b["end"]) and close(a["end"], b["start"]))
    return ends and ("diameter" not in a or abs(a["diameter"] - b["diameter"]) <= tolerance)


def compare(expected, actual, tolerance, label):
    remaining = list(actual)
    for feature in expected:
        for index, value in enumerate(remaining):
            if matching(feature, value, tolerance):
                remaining.pop(index)
                break
        else:
            raise AssertionError((label, "missing native feature", feature))
    assert not remaining, (label, "extra exported features", remaining)


def cam(candidate, output, manifest):
    from gerbonara import LayerStack
    from gerbonara.graphic_objects import Flash, Line
    from gerbonara.utils import MM
    import cairosvg
    reference = json.loads((output / "native-reference.json").read_text())
    assert reference["candidate_manifest_sha256"] == sha(candidate / "manifest.json")
    report = {"status": "EXPORT_GEOMETRY_CHECK_PASSED_NOT_ORDER_RELEASE",
              "scope": "All exported drill centers/slot endpoints/diameters and plating classes, outline centerlines, layer presence, file hashes, BOM/CPL reference counts. Rendered from the actual ZIP. No electrical or supplier placement acceptance implied.",
              "drill_tolerance_mm": 0.00051, "outline_tolerance_mm": 0.0000011,
              "candidate_manifest_sha256": sha(candidate / "manifest.json"),
              "native_reference_sha256": sha(output / "native-reference.json"),
              "reviewer_script_sha256": sha(Path(__file__)), "boards": {}}
    for name, entry in manifest["boards"].items():
        folder = candidate / name
        for relative, digest in entry["file_sha256"].items():
            assert sha(folder / relative) == digest, (name, relative)
        ref = reference["boards"][name]
        pcb = ROOT / "boards" / name / (name + ".kicad_pcb")
        assert sha(pcb) == ref["native_pcb_sha256"]
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            stack = LayerStack.open(folder / (name + "-gerbers.zip"))
        required = {(side, layer) for side in ("top", "bottom") for layer in ("copper", "mask", "silk", "paste")}
        required.add(("mechanical", "outline"))
        if entry["copper_layers"] == 4:
            required.update({("inner_1", "copper"), ("inner_2", "copper")})
        assert set(stack.graphic_layers) == required
        assert sum(layer == "copper" for side, layer in required) == ref["copper_layers"]
        counts = {}
        for group, layer in (("pth", stack.drill_pth), ("npth", stack.drill_npth)):
            assert layer is not None
            actual = []
            for obj in layer.objects:
                assert obj.unit == MM
                if isinstance(obj, Flash):
                    start = end = [obj.x, obj.y]
                else:
                    assert isinstance(obj, Line), type(obj)
                    start, end = [obj.x1, obj.y1], [obj.x2, obj.y2]
                actual.append({"start": start, "end": end, "diameter": obj.aperture.diameter})
            compare(ref["holes"][group], actual, 0.00051, name + " " + group)
            counts[group] = {"holes_including_slots": len(actual),
                             "slots": sum(f["start"] != f["end"] for f in actual)}
        actual = []
        for obj in stack.graphic_layers[("mechanical", "outline")].objects:
            assert isinstance(obj, Line) and obj.unit == MM
            actual.append({"start": [obj.x1, obj.y1], "end": [obj.x2, obj.y2]})
        compare(ref["outline"], actual, 0.0000011, name + " outline")
        points = [point for f in actual for point in (f["start"], f["end"])]
        bounds = [[min(p[i] for p in points), max(p[i] for p in points)] for i in range(2)]
        with (folder / (name + "-cpl.csv")).open() as f:
            cpl = list(csv.DictReader(f))
        with (folder / (name + "-bom.csv")).open() as f:
            bom = list(csv.DictReader(f))
        bom_refs = [r.strip() for row in bom for r in row["Designator"].split(",")]
        cpl_refs = [row["Designator"] for row in cpl]
        assert len(bom_refs) == len(set(bom_refs)) == entry["fitted_references"]
        assert sorted(bom_refs) == sorted(cpl_refs)
        renders = {}
        render_bounds = ((bounds[0][0], bounds[1][0]), (bounds[0][1], bounds[1][1]))
        for side in ("top", "bottom"):
            # Plain SVG avoids unsupported filter effects in CairoSVG. Keep
            # mask/paste separate: an opaque mask preview can hide copper.
            colors = {side + " copper": "#b7791f", "mechanical outline": "#111111",
                      "drill pth": "#ffffff", "drill npth": "#111111"}
            svg = str(stack.to_svg(side_re=side + "|mechanical", margin=2, colors=colors,
                                   force_bounds=render_bounds))
            if side == "bottom":
                tree = ET.fromstring(svg)
                group = ET.Element("{http://www.w3.org/2000/svg}g", {
                    "transform": "translate(%s 0) scale(-1 1)" % sum(bounds[0])})
                for child in list(tree):
                    tree.remove(child)
                    group.append(child)
                tree.append(group)
                svg = ET.tostring(tree, encoding="unicode")
            dest = output / (name + "-" + side + ".png")
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(dest), output_width=1600,
                            background_color="white")
            renders[dest.name] = sha(dest)
            for use in ("mask", "paste", "silk"):
                svg = str(stack.to_svg(side_re=side + "|mechanical", drills=False, margin=2,
                                      force_bounds=render_bounds,
                                      colors={side + " " + use: "#111111", "mechanical outline": "#888888"}))
                # Layer SVGs stay in the top-view coordinate convention used
                # by Gerber data; only the board bottom overview is mirrored.
                dest = output / (name + "-" + side + "-" + use + ".svg")
                dest.write_text(svg)
                renders[dest.name] = sha(dest)
        report["boards"][name] = {"archive_sha256": sha(folder / (name + "-gerbers.zip")),
                                  "copper_layers": entry["copper_layers"], "drills": counts,
                                  "outline_segments": len(actual),
                                  "outline_width_height_mm": [hi - lo for lo, hi in bounds],
                                  "fitted_references": len(cpl_refs), "render_sha256": renders,
                                  "parser_warnings": sorted(set(str(w.message) for w in caught))}
        print(name, counts, "outline/layers/BOM/CPL pass", flush=True)
    write(output / "cam-check.json", report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("native", "cam"))
    parser.add_argument("candidate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    data = json.loads((args.candidate / "manifest.json").read_text())
    (native if args.mode == "native" else cam)(args.candidate, args.output, data)
