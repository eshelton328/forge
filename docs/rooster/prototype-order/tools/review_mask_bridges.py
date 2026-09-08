#!/usr/bin/env python3
"""Measure separation of actual Gerber mask openings after merging overlaps.

Requires Gerbonara and Shapely 2. Uses the immutable fabrication ZIPs, not a
project rule whose application has not been established. No native files change.
"""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
from itertools import combinations
import json
from pathlib import Path
import warnings

from gerbonara import LayerStack
from gerbonara.utils import MM
from shapely.geometry import Polygon, box
from shapely.ops import nearest_points, unary_union

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'docs/rooster/prototype-order'
ARC_ERROR_MM = .0001
REQUIRED_BRIDGE_MM = .10


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def detail_svg(regions, output):
    bounds = (110.5, -103.5, 115.5, -99.0)
    selected = [r for r in regions if r.intersects(box(*bounds))]
    scale = 125
    xy = lambda c: (50 + (c[0] - bounds[0]) * scale, 80 + (bounds[3] - c[1]) * scale)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="740" height="725" viewBox="0 0 740 725">',
           '<rect width="740" height="725" fill="white"/>',
           '<text x="30" y="32" font-family="sans-serif" font-size="22">U1: actual top mask openings</text>',
           '<text x="30" y="58" font-family="sans-serif" font-size="14">White = mask opening; green = solder mask. Native top view.</text>',
           '<rect x="35" y="70" width="670" height="590" fill="#14532d"/>']
    for r in selected:
        coords = [xy(c) for c in r.exterior.coords]
        path = 'M ' + ' L '.join(f'{x:.3f} {y:.3f}' for x, y in coords) + ' Z'
        svg.append(f'<path d="{path}" fill="white"/>')
    svg.extend(['<text x="30" y="692" font-family="sans-serif" font-size="14">Stepped pad openings contain no separate mask islands.</text>', '</svg>'])
    output.write_text('\n'.join(svg) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    out = parser.parse_args().output_dir
    out.mkdir(parents=True, exist_ok=True)
    candidate = BASE / 'fabrication-candidates/4d8e65d-r1'
    manifest = json.loads((candidate / 'manifest.json').read_text())
    result = {'status': 'PASS_SEPARATION_BETWEEN_DISTINCT_GERBER_MASK_OPENINGS',
              'scope': __doc__, 'required_separation_mm': REQUIRED_BRIDGE_MM,
              'arc_max_error_mm': ARC_ERROR_MM,
              'distance_error_allowance_mm': 2 * ARC_ERROR_MM,
              'manifest_sha256': sha(candidate / 'manifest.json'),
              'generator_sha256': sha(Path(__file__)),
              'libraries': {n: importlib.metadata.version(n) for n in ('gerbonara', 'shapely')},
              'boards': {}}
    for name, entry in manifest['boards'].items():
        native = ROOT / 'boards' / name / (name + '.kicad_pcb')
        assert sha(native) == entry['source_sha256'][str(native.relative_to(ROOT))]
        archive = candidate / name / (name + '-gerbers.zip')
        assert sha(archive) == entry['file_sha256'][archive.name]
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            stack = LayerStack.open(archive)
        board_result = {'native_sha256': sha(native), 'archive_sha256': sha(archive),
                        'parser_warnings': [str(w.message) for w in caught], 'sides': {}}
        for side in ('top', 'bottom'):
            primitives = [p for obj in stack.graphic_layers[(side, 'mask')].objects
                          for p in obj.to_primitives(unit=MM)]
            assert primitives and all(p.polarity_dark for p in primitives), 'Extend polarity handling before accepting clear primitives'
            polys = [Polygon(p.to_arc_poly().approximate_arcs(max_error=ARC_ERROR_MM).outline)
                     for p in primitives]
            assert all(p.is_valid and not p.is_empty for p in polys)
            joined = unary_union(polys)
            regions = list(joined.geoms) if joined.geom_type == 'MultiPolygon' else [joined]
            assert len(regions) > 1 and all(r.geom_type == 'Polygon' and not r.interiors for r in regions)
            distance, a, b = min(((a.distance(b), a, b) for a, b in combinations(regions, 2)), key=lambda r: r[0])
            lower_bound = distance - 2 * ARC_ERROR_MM
            assert lower_bound >= REQUIRED_BRIDGE_MM, (name, side, distance)
            positions = [list(p.coords)[0] for p in nearest_points(a, b)]
            nonconvex = [list(r.bounds) for r in regions if r.convex_hull.area - r.area > 1e-5]
            board_result['sides'][side] = {
                'primitive_count': len(primitives), 'primitive_types': dict(Counter(type(p).__name__ for p in primitives)),
                'merged_opening_count': len(regions), 'minimum_separation_mm': distance,
                'conservative_lower_bound_mm': lower_bound,
                'nearest_points_gerber_mm': positions,
                'nearest_points_native_mm': [[x, -y] for x, y in positions],
                'nonconvex_opening_bounds_gerber_mm': nonconvex,
                'enclosed_mask_islands': 0,
            }
            if name == 'alec-main' and side == 'top':
                detail_svg(regions, out / 'converter-mask-detail.svg')
        result['boards'][name] = board_result
        assert sha(native) == board_result['native_sha256']
    result['converter_detail_sha256'] = sha(out / 'converter-mask-detail.svg')
    (out / 'gerber-mask-bridges.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({name: {side: round(d['minimum_separation_mm'], 6) for side, d in b['sides'].items()}
                      for name, b in result['boards'].items()}, indent=2))


if __name__ == '__main__':
    main()
