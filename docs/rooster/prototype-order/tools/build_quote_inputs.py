#!/usr/bin/env python3
"""Build review-only BOM/CPL drafts including THT and both board faces.

Uses reconciled native MPN and LCSC fields. It cannot make a fabrication
release: final part review, rotations and supplier coverage remain
open. Run verify_sourcing.py first. No network or supplier action is performed.
"""
import argparse
import collections
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts/alarm'))
from order_parts import native_order_fields


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_csv(path, fields, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kicad-cli', default='/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')
    args = parser.parse_args()
    rows = list(csv.DictReader((HERE / 'sourcing.csv').open()))
    audit = json.loads((HERE / 'selection-audit.json').read_text())
    for relative, digest in audit['input_sha256'].items():
        assert sha(ROOT / relative) == digest, 'Stale selection audit: ' + relative
    dst = HERE / 'draft-quote-inputs'
    dst.mkdir(exist_ok=True)
    cache = ROOT / '.cache/prototype-order/positions'
    cache.mkdir(parents=True, exist_ok=True)
    report = {'status': 'DRAFT_REVIEW_ONLY_NOT_MANUFACTURING_RELEASE',
              'tool_version': subprocess.check_output([args.kicad_cli, 'version'], text=True).strip(),
              'source_mpn_fields_updated': True,
              'placement_basis': 'Native KiCad auxiliary drill/place origin, both faces, no bottom X negation. Native rotation preserved; no supplier-specific rotation or centroid correction has been verified. Fabrication files must use a matching origin.',
              'sourcing_sha256': sha(HERE / 'sourcing.csv'), 'boards': {}}
    for board in sorted({r['board'] for r in rows}):
        fitted = {r['reference']: r for r in rows if r['board'] == board and r['proposed_mpn']}
        native = ROOT / 'boards' / board / (board + '.kicad_pcb')
        native_fields = native_order_fields(board)
        raw = cache / (board + '.csv')
        cmd = [args.kicad_cli, 'pcb', 'export', 'pos', '--format', 'csv', '--units', 'mm',
               '--side', 'both', '--use-drill-file-origin', '--exclude-dnp', '-o', str(raw), str(native)]
        subprocess.run(cmd, text=True, capture_output=True, check=True)
        positions = list(csv.DictReader(raw.open()))
        assert len(positions) == len({x['Ref'] for x in positions}) == len(fitted)
        assert {x['Ref'] for x in positions} == set(fitted), board
        groups = collections.defaultdict(list)
        cpl = []
        for pos in positions:
            r = fitted[pos['Ref']]
            assert pos['Val'] == r['value'] and pos['Package'] == r['footprint'].split(':')[-1], (board, pos['Ref'])
            fields = native_fields[pos['Ref']]
            groups[fields['MPN'], fields['LCSC#'], pos['Package']].append(pos['Ref'])
            assert pos['Side'] in ['top', 'bottom']
            cpl.append({'Designator': pos['Ref'], 'Mid X': pos['PosX'], 'Mid Y': pos['PosY'],
                        'Layer': pos['Side'], 'Rotation': pos['Rot']})
        bom = [{'Comment': mpn, 'Designator': ','.join(refs), 'Footprint': package, 'LCSC Part #': code}
               for (mpn, code, package), refs in sorted(groups.items())]
        bom_file, cpl_file = dst / (board + '-bom.csv'), dst / (board + '-cpl.csv')
        write_csv(bom_file, ['Comment', 'Designator', 'Footprint', 'LCSC Part #'], bom)
        write_csv(cpl_file, ['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'], cpl)
        report['boards'][board] = {'fitted_references': len(fitted), 'bom_rows': len(bom),
                                   'placement_rows_by_side': dict(collections.Counter(x['Layer'] for x in cpl)),
                                   'native_pcb_sha256': sha(native),
                                   'files': {bom_file.name: sha(bom_file), cpl_file.name: sha(cpl_file)}}
    assert sum(b['fitted_references'] for b in report['boards'].values()) == 207
    (dst / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['boards'], indent=2))


if __name__ == '__main__':
    main()
