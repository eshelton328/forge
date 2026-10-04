#!/usr/bin/env python3
"""Inventory native holes and pad-mask exposure for the prototype via process.

Run with KiCad Python. Geometry is read-only. This is a fabrication-process
specification aid, not complete solder-mask DRC or supplier production approval.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

import pcbnew as p

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'docs/rooster/prototype-order'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def point(v):
    return [p.ToMM(v.x), p.ToMM(v.y)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, default=BASE / 'fabrication-candidates/4d8e65d-r1')
    parser.add_argument('--cam-reference', type=Path, default=BASE / 'cam-review/4d8e65d-r1/native-reference.json')
    args = parser.parse_args()
    out = args.output_dir
    assert not out.exists(), 'Refusing to overwrite an existing process attachment set'
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = args.candidate / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    cam_reference = json.loads(args.cam_reference.read_text())
    assert cam_reference['candidate_manifest_sha256'] == sha(manifest_path)
    report = {'scope': __doc__, 'generator_sha256': sha(Path(__file__)),
              'candidate_manifest_sha256': sha(manifest_path),
              'cam_reference_sha256': sha(args.cam_reference),
              'mask_polygon_max_error_mm': 0.001, 'boards': {}}
    for name, entry in manifest['boards'].items():
        source = ROOT / 'boards' / name / (name + '.kicad_pcb')
        digest = sha(source)
        assert digest == entry['source_sha256'][str(source.relative_to(ROOT))]
        board = p.LoadBoard(str(source))
        mask_polys = []
        for fp in board.GetFootprints():
            for pad in fp.Pads():
                for layer in (p.F_Mask, p.B_Mask):
                    if not pad.IsOnLayer(layer):
                        continue
                    poly = p.SHAPE_POLY_SET()
                    pad.TransformShapeToPolygon(poly, layer,
                        pad.GetSolderMaskExpansion(layer), p.FromMM(.001), p.ERROR_OUTSIDE)
                    assert poly.OutlineCount() > 0
                    mask_polys.append((fp.GetReference() + '.' + pad.GetNumber(), layer, poly, pad.GetNetname()))
        holes = []
        for via in board.GetTracks():
            if not isinstance(via, p.PCB_VIA):
                continue
            assert via.GetViaType() == p.VIATYPE_THROUGH
            holes.append({'kind': 'via', 'reference': '', 'pin': '',
                          'position_mm': point(via.GetPosition()),
                          'drill_mm': p.ToMM(via.GetDrillValue()),
                          'net': via.GetNetname(),
                          'plated': True, 'round': True,
                          'tented_front': via.IsTented(p.F_Mask),
                          'tented_back': via.IsTented(p.B_Mask)})
        for fp in board.GetFootprints():
            for pad in fp.Pads():
                drill = pad.GetDrillSize()
                if not drill.x:
                    continue
                holes.append({'kind': 'pad', 'reference': fp.GetReference(),
                              'pin': pad.GetNumber(), 'position_mm': point(pad.GetPosition()),
                              'drill_mm': p.ToMM(drill.x), 'drill_y_mm': p.ToMM(drill.y),
                              'net': pad.GetNetname(),
                              'plated': pad.GetAttribute() != p.PAD_ATTRIB_NPTH,
                              'round': drill.x == drill.y})
        holes.sort(key=lambda h: (*h['position_mm'], h['kind'], h['reference'], h['pin']))
        large_board = name in ('alec-main', 'alec-sensor')
        for h in holes:
            small = h['plated'] and h['round'] and h['drill_mm'] <= .5
            if small and h['kind'] == 'pad':
                # A component lead hole must never be silently filled.
                assert h['reference'] == 'U3' and h['pin'] == '41' and h['drill_mm'] == .3
            if h['kind'] == 'via':
                assert h['drill_mm'] <= .5
            h['specified_process'] = ('epoxy_fill_and_copper_cap' if large_board and small
                                      else 'retain_tenting' if h['kind'] == 'via'
                                      else 'leave_open')
            if small:
                pos = p.VECTOR2I(*(p.FromMM(v) for v in h['position_mm']))
                nearest = min(mask_polys, key=lambda row: row[2].Distance(pos))
                clearance = p.ToMM(nearest[2].Distance(pos)) - h['drill_mm'] / 2
                h['nearest_pad_mask'] = {'pad': nearest[0], 'layer': board.GetLayerName(nearest[1]),
                                        'net': nearest[3],
                                        'hole_edge_clearance_mm': round(clearance, 6)}
                if clearance < 0:
                    assert h['net'] == nearest[3], 'Hole intersects a different-net pad opening'
        counts = Counter(h['specified_process'] for h in holes)
        fill = [h for h in holes if h['specified_process'] == 'epoxy_fill_and_copper_cap']
        plated = [h for h in holes if h['plated']]
        cam_board = cam_reference['boards'][name]
        assert digest == cam_board['native_pcb_sha256']
        assert len(plated) == len(cam_board['holes']['pth'])
        for h in fill:
            x, y = h['position_mm']
            assert sum(abs(c['start'][0] - x) < 1e-6 and abs(c['start'][1] + y) < 1e-6
                       and c['start'] == c['end'] and abs(c['diameter'] - h['drill_mm']) < 1e-6
                       for c in cam_board['holes']['pth']) == 1
        if large_board:
            assert {h['drill_mm'] for h in fill} == {.2, .25, .3, .4}
            assert sum(h['kind'] == 'pad' for h in fill) == 12
        csv_path = out / (name + '-fill-holes.csv')
        with csv_path.open('w', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Kind', 'Reference', 'Pin', 'Native_X_mm', 'Native_Y_down_mm',
                             'Gerber_X_mm', 'Gerber_Y_up_mm', 'Drill_mm', 'Process'])
            origin = board.GetDesignSettings().GetAuxOrigin()
            assert origin.x == origin.y == 0
            for h in fill:
                x, y = h['position_mm']
                writer.writerow([h['kind'], h['reference'], h['pin'], x, y, x, -y,
                                 h['drill_mm'], h['specified_process']])
        edges = [d for d in board.GetDrawings() if d.GetLayer() == p.Edge_Cuts]
        assert all(d.GetShapeStr() == 'Line' for d in edges)
        coords = [point(v) for d in edges for v in (d.GetStart(), d.GetEnd())]
        xmin, xmax = min(v[0] for v in coords), max(v[0] for v in coords)
        ymin, ymax = min(v[1] for v in coords), max(v[1] for v in coords)
        scale = min(700 / (xmax - xmin), 590 / (ymax - ymin))
        xy = lambda v: (50 + (v[0] - xmin) * scale, 100 + (v[1] - ymin) * scale)
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="790" viewBox="0 0 800 790">',
               '<rect width="800" height="790" fill="white"/>',
               f'<text x="35" y="35" font-family="sans-serif" font-size="22">{name}: via process — native top view</text>',
               f'<text x="35" y="63" font-family="sans-serif" font-size="15">Blue: fill and cap ({len(fill)}). Orange: leave open. Gray: retain tenting.</text>']
        for d in edges:
            a, b = xy(point(d.GetStart())), xy(point(d.GetEnd()))
            svg.append(f'<path d="M {a[0]} {a[1]} L {b[0]} {b[1]}" stroke="#111827" fill="none" stroke-width="2"/>')
        for h in holes:
            x, y = xy(h['position_mm'])
            color = {'epoxy_fill_and_copper_cap': '#2563eb', 'leave_open': '#c2410c',
                     'retain_tenting': '#64748b'}[h['specified_process']]
            radius = max(2, scale * h['drill_mm'] / 2)
            svg.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}"/>')
        svg.extend([f'<text x="35" y="740" font-family="monospace" font-size="13">PCB SHA-256: {digest[:32]}…</text>',
                    '<text x="35" y="765" font-family="sans-serif" font-size="14">Drill locations only; marker sizes exaggerated. Slots shown at centers. See exact CSV.</text>', '</svg>'])
        svg_path = out / (name + '-via-process.svg')
        svg_path.write_text('\n'.join(svg) + '\n')
        report['boards'][name] = {'native_pcb_sha256': digest, 'process_counts': dict(counts),
            'fill_drill_counts': dict(Counter(str(h['drill_mm']) for h in fill)),
            'small_holes_intersecting_pad_mask': sum(h.get('nearest_pad_mask', {}).get('hole_edge_clearance_mm', 1) < 0 for h in holes),
            'mask_graphics_count': sum(d.GetLayer() in (p.F_Mask, p.B_Mask) for d in board.GetDrawings()),
            'holes': holes, 'csv_sha256': sha(csv_path), 'svg_sha256': sha(svg_path)}
        assert sha(source) == digest
    (out / 'via-process-review.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({name: {k: v for k, v in b.items() if k in ('process_counts', 'fill_drill_counts', 'small_holes_intersecting_pad_mask', 'mask_graphics_count')}
                      for name, b in report['boards'].items()}, indent=2))


if __name__ == '__main__':
    main()
