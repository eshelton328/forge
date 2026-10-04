#!/usr/bin/env python3
"""Export native pad identities alongside the reviewed supplier CPL, without edits.

Run with KiCad Python. This is a comparison reference for manual production
review, not a verifier of supplier library origins, rotations or assembly data.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import pcbnew as pcb

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
CANDIDATE = HERE / 'fabrication-candidates/090b207-r1'
CPLS = {
    'alec-main': HERE / 'supplier-placement-candidates/090b207-r1-headers/alec-main-cpl.csv',
    'alec-controls': HERE / 'supplier-placement-candidates/090b207-r1-controls/alec-controls-cpl.csv',
    'alec-front': CANDIDATE / 'alec-front/alec-front-cpl.csv',
    'alec-sensor': HERE / 'supplier-placement-candidates/090b207-r1-headers/alec-sensor-cpl.csv',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mm(point):
    return [round(pcb.ToMM(point.x), 6), round(pcb.ToMM(point.y), 6)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    output = parser.parse_args().output
    if output.exists():
        raise SystemExit('Refusing to overwrite an existing reference.')
    manifest_path = CANDIDATE / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    report = {
        'status': 'NATIVE_COMPARISON_REFERENCE_NOT_SUPPLIER_PLACEMENT_APPROVAL',
        'source_commit': manifest['native_source_commit'],
        'candidate_manifest_sha256': sha(manifest_path),
        'generator_sha256': sha(Path(__file__)),
        'kicad_version': pcb.GetBuildVersion(),
        'coordinates': 'Native X right, Y down in mm, viewed from board top; bottom footprints are not reflected. Supplier CPL uses X right, Y up. Native footprint anchor and supplier body center may intentionally differ. Never copy pad centers into CPL Mid X/Y.',
        'scope': 'All fitted references from the current candidate BOM/CPL, including required U5 on main/Beacon. Numbered native pads are listed individually, preserving repeated pad numbers. No supplier production data has been compared.',
        'boards': {},
    }
    for board_name, cpl_path in CPLS.items():
        expected = manifest['boards'][board_name]
        native = ROOT / f'boards/{board_name}/{board_name}.kicad_pcb'
        native_hash = sha(native)
        assert native_hash == expected['source_sha256'][str(native.relative_to(ROOT))]
        bom_path = CANDIDATE / board_name / f'{board_name}-bom.csv'
        assert sha(bom_path) == expected['file_sha256'][bom_path.name]
        with bom_path.open(newline='') as handle:
            bom_rows = list(csv.DictReader(handle))
        bom = {ref.strip(): row for row in bom_rows for ref in row['Designator'].split(',')}
        assert sum(len(row['Designator'].split(',')) for row in bom_rows) == len(bom)
        with cpl_path.open(newline='') as handle:
            cpl_rows = list(csv.DictReader(handle))
        placements = {row['Designator']: row for row in cpl_rows}
        assert len(placements) == len(cpl_rows) == expected['fitted_references']
        assert set(bom) == set(placements)
        if board_name == 'alec-front':
            assert sha(cpl_path) == expected['file_sha256'][cpl_path.name]
        else:
            cpl_manifest = json.loads((cpl_path.parent / 'manifest.json').read_text())
            binding = cpl_manifest if board_name == 'alec-controls' else cpl_manifest['boards'][board_name]
            assert sha(cpl_path) == binding['output_cpl_sha256']
            assert binding['native_pcb_sha256'] == native_hash
            assert binding['bom_sha256'] == sha(bom_path)
            assert binding['gerber_zip_sha256'] == expected['file_sha256'][f'{board_name}-gerbers.zip']
        board = pcb.LoadBoard(str(native))
        footprints = {fp.GetReference(): fp for fp in board.GetFootprints()}
        items = []
        for ref in sorted(bom):
            fp = footprints[ref]
            fields = {field.GetName(): field.GetText() for field in fp.GetFields()}
            assert fields['MPN'] == bom[ref]['Comment'], (board_name, ref)
            side = 'bottom' if fp.GetLayer() == pcb.B_Cu else 'top'
            assert placements[ref]['Layer'] == side
            items.append({
                'reference': ref, 'mpn': fields['MPN'], 'catalog_id': bom[ref]['LCSC Part #'],
                'footprint': str(fp.GetFPID().GetLibItemName()), 'side': side,
                'native_anchor_mm': mm(fp.GetPosition()),
                'native_rotation_degrees': fp.GetOrientationDegrees(),
                'supplier_cpl': placements[ref],
                'numbered_pads': sorted([{
                    'number': pad.GetNumber(), 'net': pad.GetNetname(),
                    'native_center_mm': mm(pad.GetPosition()), 'size_mm': mm(pad.GetSize()),
                    'rotation_degrees': pad.GetOrientationDegrees(),
                    'drill_mm': mm(pad.GetDrillSize()),
                    'front_copper': pad.IsOnLayer(pcb.F_Cu), 'back_copper': pad.IsOnLayer(pcb.B_Cu),
                } for pad in fp.Pads() if pad.GetNumber()],
                    key=lambda pad: (pad['number'], pad['native_center_mm'])),
            })
        assert sha(native) == native_hash
        report['boards'][board_name] = {
            'native_pcb_sha256': native_hash, 'bom_sha256': sha(bom_path),
            'cpl_path': str(cpl_path.relative_to(ROOT)), 'cpl_sha256': sha(cpl_path),
            'fitted_references': len(items), 'components': items,
        }
    assert sum(item['fitted_references'] for item in report['boards'].values()) == 207
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print('Exported 207 fitted native references with source-bound BOM/CPL and numbered pads.')


if __name__ == '__main__':
    main()
