#!/usr/bin/env python3
"""Emit source-bound JLCPCB header centroids; preserve native geometry and r1.

Run with KiCad Python. Main J4's supplier model also needs a quarter-turn.
This is a placement review candidate, not approval of other parts or fabrication.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import pcbnew

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
SPECS = {
    'alec-main': ('J4', 'PinHeader_1x04_P2.54mm_Vertical', 4, [161.0, 86.0], 270),
    'alec-sensor': ('J3', 'Samtec_SSW-105-01-F-S', 5, [145.0, 108.0], 0),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    dst = parser.parse_args().output.resolve()
    assert not dst.exists(), 'Refusing to overwrite a placement candidate'
    base = HERE / 'fabrication-candidates/4d8e65d-r1'
    manifest = json.loads((base / 'manifest.json').read_text())
    report = {'status': 'SUPPLIER_PLACEMENT_CANDIDATE_NOT_ORDER_RELEASE',
              'generator_sha256': sha(Path(__file__)), 'boards': {}}
    outputs = {}
    for board, (ref, footprint, count, anchor, rotation) in SPECS.items():
        candidate = manifest['boards'][board]
        native = ROOT / 'boards' / board / (board + '.kicad_pcb')
        native_hash = sha(native)
        assert native_hash == candidate['source_sha256'][str(native.relative_to(ROOT))]
        cpl = base / board / (board + '-cpl.csv')
        assert sha(cpl) == candidate['file_sha256'][cpl.name]
        rows = list(csv.DictReader(cpl.open()))
        originals = {r['Designator']: dict(r) for r in rows}
        assert len(rows) == len(originals) == candidate['fitted_references']
        pcb = pcbnew.LoadBoard(str(native))
        assert pcb.GetDesignSettings().GetAuxOrigin() == pcbnew.VECTOR2I(0, 0)
        f = next(f for f in pcb.GetFootprints() if f.GetReference() == ref)
        assert f.GetFPID().GetLibItemName() == footprint
        assert f.GetLayer() == pcbnew.F_Cu and f.GetOrientationDegrees() == 0
        assert [pcbnew.ToMM(f.GetPosition().x), pcbnew.ToMM(f.GetPosition().y)] == anchor
        pads = sorted(f.Pads(), key=lambda p: int(p.GetNumber()))
        assert [p.GetNumber() for p in pads] == [str(n) for n in range(1, count + 1)]
        xy = [[pcbnew.ToMM(p.GetPosition().x), pcbnew.ToMM(p.GetPosition().y)] for p in pads]
        for i, (p, point) in enumerate(zip(pads, xy)):
            expected = [anchor[0], anchor[1] + i * 2.54] if board == 'alec-main' else [anchor[0] + i * 2.54, anchor[1]]
            assert all(abs(a - b) < 1e-6 for a, b in zip(point, expected))
            assert p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH
            assert p.GetDrillSize() == pcbnew.VECTOR2I(pcbnew.FromMM(1), pcbnew.FromMM(1))
        center = [(xy[0][axis] + xy[-1][axis]) / 2 for axis in (0, 1)]
        row = next(r for r in rows if r['Designator'] == ref)
        assert [float(row['Mid X']), -float(row['Mid Y'])] == anchor
        assert row['Layer'] == 'top' and float(row['Rotation']) == 0
        row.update({'Mid X': f'{center[0]:.6f}', 'Mid Y': f'{-center[1]:.6f}',
                    'Rotation': f'{rotation:.6f}'})
        assert all(r == originals[r['Designator']] for r in rows if r['Designator'] != ref)
        assert sha(native) == native_hash
        outputs[cpl.name] = rows
        report['boards'][board] = {
            'native_pcb_sha256': native_hash, 'input_cpl_sha256': sha(cpl),
            'gerber_zip_sha256': candidate['file_sha256'][board + '-gerbers.zip'],
            'bom_sha256': candidate['file_sha256'][board + '-bom.csv'],
            'changed_reference': ref, 'native_holes_mm': xy,
            'body_center_board_mm': center, 'before': originals[ref], 'after': dict(row),
            'unchanged_reference_count': len(rows) - 1,
            'reason': ('Native pin-one origin differs from body center. Main supplier model is horizontal '
                       'at 0 degrees; use 270 degrees for the vertical, unkeyed four-pin header.'
                       if board == 'alec-main' else
                       'Native pin-one origin differs from socket body center. Supplier has only a placeholder; '
                       'do not infer socket pin orientation from it.'),
        }
    dst.mkdir(parents=True)
    for name, rows in outputs.items():
        output = dst / name
        with output.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
        report['boards'][name.removesuffix('-cpl.csv')]['output_cpl_sha256'] = sha(output)
    report['remaining'] = ('Re-upload and inspect. U3 supplier model alignment, other component origins/rotations, '
                           'missing models, rails and final supplier DFM remain open. Full BOM still requires U5 RTC.')
    (dst / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
