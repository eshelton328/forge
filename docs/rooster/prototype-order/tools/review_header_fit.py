#!/usr/bin/env python3
"""Check J4 fit and prove the bounded change using KiCad-loaded geometry."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts/alarm'))
from header_fit import historical_source, RECORD, NEW, OLD
from scripts.physics.export_geometry import export


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = ROOT / 'boards/alec-main/alec-main.kicad_pcb'
    old_text = historical_source(source.read_text(), source.relative_to(ROOT))
    with tempfile.TemporaryDirectory() as tmp:
        old_path = Path(tmp) / source.name
        old_path.write_text(old_text)
        before, after = export(old_path), export(source)
    normalized = copy.deepcopy(after)
    before_hash = before.pop('pcb_sha256')
    after_hash = normalized.pop('pcb_sha256')
    j4 = normalized['footprints']['J4']
    assert j4['footprint'] == NEW
    assert before['footprints']['J4']['footprint'] == OLD
    j4['footprint'] = OLD
    pads = []
    for pad in j4['pads']:
        assert pad['drill'] == [1.1, 1.1] and pad['size'] == [1.7, 1.7]
        pads.append(copy.deepcopy(pad))
        pad['drill'] = [1.0, 1.0]
    assert len(pads) == 4
    assert before == normalized, 'An additional KiCad geometry or connectivity change exists'
    record = json.loads(RECORD.read_text())
    library = ROOT / record['library']['path']
    assert sha(library) == record['library']['sha256']
    result = {
        'status': 'PASS_BOUNDED_J4_FINISHED_HOLE_CHANGE',
        'scope': 'Exactly four J4 hole diameters and its footprint identity differ in the KiCad geometry export. All pad copper polygons, saved filled copper, tracks, vias, placements, nets and board bounds match. This is not physical fit or solder-joint qualification.',
        'before_pcb_sha256': before_hash, 'after_pcb_sha256': after_hash,
        'transition_sha256': sha(RECORD), 'library_sha256': sha(library),
        'generator_sha256': sha(Path(__file__)),
        'geometry_exporter_sha256': sha(ROOT / 'scripts/physics/export_geometry.py'),
        'unchanged_copper_records': len(after['copper']),
        'unchanged_tracks': len(after['tracks']), 'unchanged_vias': len(after['vias']),
        'header_pads': pads,
        'nominal_finished_hole_mm': 1.10,
        'supplier_finished_hole_range_mm': [1.02, 1.23],
        'samtec_recommended_hole_mm': 1.02,
        'nominal_annular_ring_mm': .30,
        'annular_ring_at_max_hole_minus_0_05mm_position_offset_mm': .185,
        'supplier_multilayer_1oz_absolute_minimum_annular_ring_mm': .15,
        'retained_physical_screening': 'The present solver uses copper polygons, tracks, vias and selected power-pad positions/values; these inputs are unchanged. The J4 footprint name and pad.drill records are not consumed by that solver. Retaining its historical nominal results does not claim a new run, a model of the connector holes or physical qualification.',
    }
    (RECORD.parent / 'geometry-review.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'unchanged_copper_records', 'unchanged_tracks', 'unchanged_vias']}, indent=2))


if __name__ == '__main__':
    main()
