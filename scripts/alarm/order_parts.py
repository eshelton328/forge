"""Synchronize Rooster ordering fields without rewriting circuit or PCB geometry.

The sourcing CSV is the deliberate purchasing overlay on the preserved design
generators. Component values, footprints, wiring, copper, DNP flags and model
transforms remain native-design authority. This is not an order-release approval.
"""
import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import uuid
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ORDER = ROOT / "docs/rooster/prototype-order"
BOARDS = ("alec-main", "alec-controls", "alec-front", "alec-sensor")
FIELDS = {"MPN", "Manufacturer", "LCSC#", "Datasheet"}
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+')


class Atom(str):
    pass


class Form(list):
    pass


def parse(text):
    stack = []
    root = None
    for match in TOKEN.finditer(text):
        token = match.group()
        if token == "(":
            form = Form()
            form.start = match.start()
            if stack:
                stack[-1].append(form)
            else:
                assert root is None, "Multiple roots"
                root = form
            stack.append(form)
        elif token == ")":
            assert stack, "Unbalanced source"
            stack.pop().end = match.end()
        else:
            assert stack, "Atom outside root"
            atom = Atom(token)
            atom.start, atom.end = match.span()
            stack[-1].append(atom)
    assert not stack and root, "Incomplete source"
    return root


def value(atom):
    return json.loads(atom) if atom.startswith('"') else str(atom)


def children(form, tag):
    return [x for x in form if isinstance(x, Form) and x[0] == tag]


def properties(form):
    result = {}
    for field in children(form, "property"):
        key = value(field[1])
        assert key not in result, "Duplicate property: " + key
        result[key] = field
    return result


def non_ordering_signature(text):
    """Compare every parsed token except ordering properties on real components."""
    root = copy.deepcopy(parse(text))
    for component in children(root, "symbol") + children(root, "footprint"):
        component[:] = [x for x in component if not
                        (isinstance(x, Form) and x[0] == "property" and value(x[1]) in FIELDS)]
    return hashlib.sha256(json.dumps(root, separators=(",", ":")).encode()).hexdigest()


def selection(board):
    assert board in BOARDS, board
    with (ORDER / "sourcing.csv").open() as f:
        rows = [r for r in csv.DictReader(f) if r["board"] == board and r["proposed_mpn"]]
    assert rows and len(rows) == len({r["reference"] for r in rows})
    return {r["reference"]: r for r in rows}


def expected_fields(row):
    result = {"MPN": row["proposed_mpn"], "Manufacturer": row["manufacturer"],
              "LCSC#": row["supplier_part_id"]}
    if row["proposed_datasheet"]:
        result["Datasheet"] = row["proposed_datasheet"]
    assert all(result.values())
    assert re.fullmatch(r"C\d+", result["LCSC#"])
    return result


def baseline_source(relative, commit=None):
    if commit is None:
        commit = json.loads((ORDER / "input-audit.json").read_text())["source_commit"]
    assert re.fullmatch(r"[0-9a-f]{40}", commit), commit
    return subprocess.check_output(["git", "show", commit+":"+str(relative)],
                                   cwd=ROOT, text=True)


def verify_transition(board=None, verify_baseline=True):
    """Check original ordering-only transition plus the explicit J4 fit change."""
    try:
        from .header_fit import historical_source, RECORD
    except ImportError:
        from header_fit import historical_source, RECORD
    path = ORDER / "source-metadata-transition.json"
    report = json.loads(path.read_text())
    assert set(report["ordering_fields"]) == FIELDS
    assert report["baseline_commit"] == json.loads((ORDER / "input-audit.json").read_text())["source_commit"]
    expected_paths = {str(p.relative_to(ROOT)) for b in BOARDS
                      for p in list((ROOT / "boards" / b).glob("*.kicad_sch"))
                      + [ROOT / "boards" / b / (b+".kicad_pcb")]}
    assert len(report["files"]) == len(expected_paths)
    assert {r["path"] for r in report["files"]} == expected_paths
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest(),
              str(RECORD.relative_to(ROOT)): hashlib.sha256(RECORD.read_bytes()).hexdigest()}
    mechanical = json.loads(RECORD.read_text())
    library = ROOT / mechanical['library']['path']
    assert hashlib.sha256(library.read_bytes()).hexdigest() == mechanical['library']['sha256']
    hashes[str(library.relative_to(ROOT))] = mechanical['library']['sha256']
    for record in report["files"]:
        if board and Path(record["path"]).parts[1] != board:
            continue
        native = (ROOT / record["path"]).read_text()
        current = historical_source(native, record['path'])
        assert hashlib.sha256(current.encode()).hexdigest() == record["after_sha256"], record["path"]
        assert non_ordering_signature(current) == record["non_ordering_signature"], record["path"]
        if verify_baseline:
            original = baseline_source(record["path"], report["baseline_commit"])
            assert hashlib.sha256(original.encode()).hexdigest() == record["before_sha256"], record["path"]
            assert non_ordering_signature(original) == record["non_ordering_signature"], record["path"]
        hashes[record["path"]] = hashlib.sha256(native.encode()).hexdigest()
    assert len(hashes) > 1, board
    return hashes


def verify_evidence_pcb(path, expected_sha256):
    """Accept recorded metadata and J4-hole changes for retained-layout evidence.

    Historical geometry/nominal-model evidence retains its original source hash;
    it is not new physical qualification of the enlarged connector holes.
    The stored transition also works in shallow CI checkouts. Full baseline
    reconstruction is separately required by verify_sourcing.py before export.
    """
    path = Path(path)
    if hashlib.sha256(path.read_bytes()).hexdigest() == expected_sha256:
        return
    relative = str(path.relative_to(ROOT))
    record, = [r for r in json.loads((ORDER / "source-metadata-transition.json").read_text())["files"]
               if r["path"] == relative]
    assert record["before_sha256"] == expected_sha256, relative
    verify_transition(path.parent.name, verify_baseline=False)


def native_order_fields(board):
    rows = selection(board)
    path = ROOT / "boards" / board / (board+".kicad_pcb")
    result = {}
    for fp in children(parse(path.read_text()), "footprint"):
        props = properties(fp)
        ref = value(props["Reference"][2])
        if ref not in rows:
            continue
        assert ref not in result, (board, ref, "duplicate PCB reference")
        result[ref] = {key: value(prop[2]) for key, prop in props.items()}
        for key, expected in expected_fields(rows[ref]).items():
            assert result[ref].get(key) == expected, (board, ref, key)
    assert set(result) == set(rows), board
    return result


def export_bom(board):
    """Build the review BOM from native netlist fields, preserving source fit flags."""
    directory = ROOT / "boards" / board
    netlist = ET.parse(directory / "review/netlist.xml")
    components = {c.get("ref"): c for c in netlist.findall("./components/comp")}
    native = native_order_fields(board)
    columns = ["Reference", "Value", "MPN", "Footprint", "Voltage", "Datasheet",
               "Assembly", "Manufacturer", "LCSC#"]
    output = []
    fitted = set()
    for ref, comp in sorted(components.items()):
        flags = {p.get("name") for p in comp.findall("property")}
        if "exclude_from_bom" in flags:
            continue
        fields = {f.get("name"): f.text or "" for f in comp.findall("fields/field")}
        row = dict(Reference=ref, Value=comp.findtext("value"), Footprint=comp.findtext("footprint"),
                   MPN=fields.get("MPN", ""), Datasheet=comp.findtext("datasheet") or "",
                   Manufacturer=fields.get("Manufacturer", ""), Voltage=fields.get("Voltage", ""),
                   Assembly="DNP" if "dnp" in flags else "Selected prototype part; package/assembly release checks remain")
        row["LCSC#"] = fields.get("LCSC#", "")
        if "dnp" not in flags:
            fitted.add(ref)
            assert ref in native, (board, ref, "Missing ordering selection")
            for key in ["MPN", "Manufacturer", "LCSC#"]:
                assert row[key] == native[ref][key], (board, ref, key)
        output.append(row)
    assert fitted == set(native), board
    with (directory / "review/bom.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)


def synchronize_text(text, rows, identity):
    try:
        from .header_fit import expected_footprint
    except ImportError:
        from header_fit import expected_footprint
    root = parse(text)
    pcb = root[0] == "kicad_pcb"
    assert pcb or root[0] == "kicad_sch"
    edits, found = [], []
    for component in children(root, "footprint" if pcb else "symbol"):
        props = properties(component)
        if "Reference" not in props:
            continue
        ref = value(props["Reference"][2])
        if ref not in rows:
            continue
        row = rows[ref]
        assert value(props["Value"][2]) == row["value"], (identity, ref, "value")
        footprint = value(component[1]) if pcb else value(props["Footprint"][2])
        assert footprint == expected_footprint(identity, ref, row["footprint"]), (identity, ref, "footprint")
        found.append(ref)
        additions = []
        for key, val in expected_fields(row).items():
            quoted = json.dumps(val, ensure_ascii=False)
            if key in props:
                old = props[key][2]
                if value(old) != val:
                    edits.append((old.start, old.end, quoted))
            elif pcb:
                layer = value(children(component, "layer")[0][1])
                field_id = uuid.uuid5(uuid.NAMESPACE_URL, "rooster-order/"+identity+"/"+ref+"/"+key)
                additions.append(f'(property "{key}" {quoted} (at 0 0 0) '
                                 f'(layer "{"B.Fab" if layer == "B.Cu" else "F.Fab"}") '
                                 f'(hide yes) (uuid "{field_id}") '
                                 '(effects (font (size 1 1) (thickness 0.15))))')
            else:
                additions.append(f'(property "{key}" {quoted} (at 0 0 0) '
                                 '(effects (font (size 1.27 1.27)) (hide yes)))')
        if additions:
            closing = component.end-1
            line_start = text.rfind("\n", component.start, closing)+1
            indent = text[line_start:closing]
            if not indent.strip():
                # Insert before the closing line's indentation, avoiding a
                # whitespace-only line when the source is pretty-printed.
                edits.append((line_start, line_start,
                              "".join(indent+"\t"+field+"\n" for field in additions)))
            else:
                edits.append((closing, closing, "\n\t"+"\n\t".join(additions)))
    revised = text
    for start, end, replacement in sorted(edits, reverse=True):
        revised = revised[:start]+replacement+revised[end:]
    assert non_ordering_signature(revised) == non_ordering_signature(text), identity
    return revised, found


def synchronize_board(board, schematics=True, pcb=True, write=True):
    rows = selection(board)
    directory = ROOT / "boards" / board
    paths = sorted(directory.glob("*.kicad_sch")) if schematics else []
    if pcb:
        paths.append(directory / (board+".kicad_pcb"))
    staged, sch_refs, pcb_refs = [], set(), set()
    for path in paths:
        before = path.read_text()
        relative = str(path.relative_to(ROOT))
        after, refs = synchronize_text(before, rows, relative)
        (pcb_refs if path.suffix == ".kicad_pcb" else sch_refs).update(refs)
        staged.append((path, before, after, refs))
    if schematics:
        assert sch_refs == set(rows), (board, "schematic refs", set(rows)-sch_refs)
    if pcb:
        assert pcb_refs == set(rows), (board, "PCB refs", set(rows)-pcb_refs)
    for path, before, after, refs in staged:
        assert path.read_text() == before, "Source changed concurrently: " + str(path)
    for path, before, after, refs in staged:
        if write and before != after:
            path.write_text(after)
    return [{"path": str(path.relative_to(ROOT)), "changed": before != after,
             "component_references": refs,
             "before_sha256": hashlib.sha256(before.encode()).hexdigest(),
             "after_sha256": hashlib.sha256(after.encode()).hexdigest(),
             "non_ordering_signature": non_ordering_signature(before)}
            for path, before, after, refs in staged]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", choices=BOARDS, action="append")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.report:
        assert not args.check, "A dry run cannot record an applied transition"
        assert not args.report.exists(), "Refusing to overwrite a transition record"
    records = []
    for board in args.board or BOARDS:
        records.extend(synchronize_board(board, write=not args.check))
    if args.report:
        args.report.write_text(json.dumps({"ordering_fields": sorted(FIELDS),
            "baseline_commit": json.loads((ORDER / "input-audit.json").read_text())["source_commit"],
            "scope": "Only ordering properties changed; every other parsed token preserved.",
            "files": records}, indent=2)+"\n")
    changed = [r["path"] for r in records if r["changed"]]
    print(json.dumps({"changed_or_out_of_sync": changed, "files_checked": len(records)}))
    if args.check and changed:
        raise SystemExit(1)
