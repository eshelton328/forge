#!/usr/bin/env python3
"""Correct the observed B3F anchor/centroid mismatch for JLCPCB quote review.

Run with KiCad's Python. Preserve the immutable r1 candidate and all native
sources; emit a separate CPL plus source/geometry evidence. This does not certify
other parts, rotations, supplier tooling, or a manufacturing release.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import pcbnew

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    dst = args.output.resolve()
    assert not dst.exists(), 'Refusing to overwrite a placement candidate'
    base = HERE / 'fabrication-candidates/4d8e65d-r1'
    board = 'alec-controls'
    candidate = json.loads((base / 'manifest.json').read_text())['boards'][board]
    native = ROOT / 'boards' / board / (board + '.kicad_pcb')
    native_hash = sha(native)
    assert native_hash == candidate['source_sha256'][str(native.relative_to(ROOT))]
    cpl = base / board / (board + '-cpl.csv')
    assert sha(cpl) == candidate['file_sha256'][cpl.name]
    rows = list(csv.DictReader(cpl.open()))
    originals = {r['Designator']: dict(r) for r in rows}
    pcb = pcbnew.LoadBoard(str(native))
    assert pcb.GetDesignSettings().GetAuxOrigin() == pcbnew.VECTOR2I(0, 0)
    footprints = {f.GetReference(): f for f in pcb.GetFootprints()}
    corrections = []
    for row in rows:
        ref = row['Designator']
        if ref not in {'SW1', 'SW2', 'SW3'}:
            continue
        f = footprints[ref]
        assert f.GetFPID().GetLibNickname() == 'Button_Switch_THT'
        assert f.GetFPID().GetLibItemName() == 'SW_TH_Tactile_Omron_B3F-106x'
        assert f.GetLayer() == pcbnew.F_Cu and f.GetOrientationDegrees() == 0
        pads = sorted((pcbnew.ToMM(p.GetPosition().x), pcbnew.ToMM(p.GetPosition().y)) for p in f.Pads())
        assert len(pads) == 4
        xs, ys = sorted({p[0] for p in pads}), sorted({p[1] for p in pads})
        assert len(xs) == len(ys) == 2
        assert abs(xs[1] - xs[0] - 6.5) < 1e-6 and abs(ys[1] - ys[0] - 4.5) < 1e-6
        assert pads == sorted((x, y) for x in xs for y in ys)
        anchor = [pcbnew.ToMM(f.GetPosition().x), pcbnew.ToMM(f.GetPosition().y)]
        assert row['Layer'] == 'top' and float(row['Rotation']) == 0
        assert [float(row['Mid X']), -float(row['Mid Y'])] == anchor
        center = [sum(xs) / 2, sum(ys) / 2]
        row['Mid X'], row['Mid Y'] = f'{center[0]:.6f}', f'{-center[1]:.6f}'
        corrections.append({'reference': ref, 'part': 'B3F-1060', 'jlcpcb_part': 'C726010',
                            'native_anchor_mm': anchor, 'native_holes_mm': pads,
                            'body_center_board_mm': center, 'before': originals[ref], 'after': dict(row)})
    assert {x['reference'] for x in corrections} == {'SW1', 'SW2', 'SW3'}
    assert len(rows) == 5 and {r['Designator'] for r in rows} == set(originals)
    assert all(r == originals[r['Designator']] for r in rows if r['Designator'] not in {'SW1', 'SW2', 'SW3'})
    assert sha(native) == native_hash
    dst.mkdir(parents=True)
    output = dst / cpl.name
    with output.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    report = {'status': 'SUPPLIER_PLACEMENT_CANDIDATE_NOT_ORDER_RELEASE',
              'reason': 'JLCPCB preview centers each B3F model on the native pin-1 anchor; use the actual four-hole/body center.',
              'native_pcb_sha256': native_hash, 'input_cpl_sha256': sha(cpl),
              'gerber_zip_sha256': candidate['file_sha256'][board + '-gerbers.zip'],
              'bom_sha256': candidate['file_sha256'][board + '-bom.csv'],
              'generator_sha256': sha(Path(__file__)), 'output_cpl_sha256': sha(output),
              'unchanged_references': ['J1', 'SW4'], 'corrections': corrections,
              'remaining': 'Re-upload and inspect supplier preview. Other part origins/pin-1/rotations, rails, and final supplier DFM remain open.'}
    (dst / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
