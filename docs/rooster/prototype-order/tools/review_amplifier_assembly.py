#!/usr/bin/env python3
"""Measure U6's retained prototype land pattern against ADI package guidance.

Run with KiCad Python. Read native source only; this does not certify the final
supplier stencil, placement, process or solder joints.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import pcbnew as p

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
PIN_NETS = {
    '1': '/GPIO14', '2': 'GND', '3': 'GND', '4': '/AMP_SD',
    '5': 'unconnected-(U6-NC-Pad5)', '6': 'unconnected-(U6-NC-Pad6)',
    '7': '/5v', '8': '/5v', '9': '/speaker +', '10': '/speaker -',
    '11': 'GND', '12': 'unconnected-(U6-NC-Pad12)',
    '13': 'unconnected-(U6-NC-Pad13)', '14': '/GPIO48',
    '15': 'GND', '16': '/GPIO47', '17': 'GND',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mm(v):
    return [p.ToMM(v.x), p.ToMM(v.y)]


def rounded_rectangle(width, height, radius):
    return {'area_mm2': width * height - (4 - math.pi) * radius ** 2,
            'perimeter_mm': 2 * (width + height) - 8 * radius + 2 * math.pi * radius}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    output = parser.parse_args().output
    native = ROOT / 'boards/alec-main/alec-main.kicad_pcb'
    native_hash = sha(native)
    candidate = json.loads((HERE / 'fabrication-candidates/4d8e65d-r1/manifest.json').read_text())
    assert native_hash == candidate['boards']['alec-main']['source_sha256'][str(native.relative_to(ROOT))]
    pcb = p.LoadBoard(str(native))
    fp = next(f for f in pcb.GetFootprints() if f.GetReference() == 'U6')
    assert fp.GetValue() == 'MAX98357A'
    assert next(field.GetText() for field in fp.GetFields() if field.GetName() == 'MPN') == 'MAX98357AETE+T'
    assert fp.GetLayer() == p.F_Cu and fp.GetOrientationDegrees() == 0
    anchor = mm(fp.GetPosition())
    numbered = [pad for pad in fp.Pads() if pad.GetNumber()]
    pads = {pad.GetNumber(): pad for pad in numbered}
    assert len(numbered) == len(pads) == 17
    assert set(pads) == set(PIN_NETS)
    assert {n: pad.GetNetname() for n, pad in pads.items()} == PIN_NETS
    signal = []
    for n in range(1, 17):
        pad = pads[str(n)]
        position = [round(a - b, 6) for a, b in zip(mm(pad.GetPosition()), anchor)]
        size = mm(pad.GetSize())
        horizontal = n <= 4 or 9 <= n <= 12
        assert size == ([0.825, 0.25] if horizontal else [0.25, 0.825])
        assert pad.GetShape() == p.PAD_SHAPE_ROUNDRECT
        assert abs(pad.GetRoundRectRadiusRatio() - 0.25) < 1e-9
        assert pad.IsOnLayer(p.F_Cu) and pad.IsOnLayer(p.F_Mask) and pad.IsOnLayer(p.F_Paste)
        radial, tangential = position if horizontal else position[::-1]
        assert abs(radial) == 1.4375 and abs(tangential) in {0.25, 0.75}
        signal.append({'pin': n, 'net': pad.GetNetname(), 'center_board_mm': mm(pad.GetPosition()),
                       'local_mm': position, 'size_mm': size})
    assert len({tuple(s['local_mm']) for s in signal}) == 16
    assert mm(pads['17'].GetPosition()) == anchor and mm(pads['17'].GetSize()) == [1.23, 1.23]
    assert pads['17'].GetShape() == p.PAD_SHAPE_RECT and not pads['17'].IsOnLayer(p.F_Paste)
    assert pads['17'].IsOnLayer(p.F_Cu) and pads['17'].IsOnLayer(p.F_Mask)
    windows = [pad for pad in fp.Pads() if not pad.GetNumber() and pad.IsOnLayer(p.F_Paste)]
    assert len(windows) == 4
    for pad in windows:
        assert mm(pad.GetSize()) == [0.5, 0.5] and pad.GetShape() == p.PAD_SHAPE_ROUNDRECT
        assert pad.GetRoundRectRadiusRatio() == 0.25 and not pad.IsOnLayer(p.F_Cu)
    window_centers = sorted([[round(a - b, 6) for a, b in zip(mm(pad.GetPosition()), anchor)] for pad in windows])
    assert window_centers == [[x, y] for x in [-0.31, 0.31] for y in [-0.31, 0.31]]
    window = rounded_rectangle(0.5, 0.5, 0.125)
    peripheral = rounded_rectangle(0.825, 0.25, 0.0625)
    coverage = 4 * window['area_mm2'] / 1.23 ** 2
    assert 0.5 <= coverage <= 0.8
    stencil_cases = []
    for thickness in [0.100, 0.120, 0.127]:
        ratios = {name: shape['area_mm2'] / (shape['perimeter_mm'] * thickness)
                  for name, shape in [('peripheral', peripheral), ('thermal_window', window)]}
        assert min(ratios.values()) > 0.66
        stencil_cases.append({'assumed_thickness_mm': thickness, 'area_ratios': ratios})
    inner, outer = 1.4375 - 0.825 / 2, 1.4375 + 0.825 / 2
    assert abs(inner - 1.025) < 1e-9 and 0.2 <= outer - 1.5 <= 0.5
    assert sha(native) == native_hash
    report = {
        'status': 'RETAIN_FOR_PROTOTYPE_ORDER_PREPARATION',
        'scope': 'Engineering disposition from package dimensions and assembly guidance; no supplier approval or solder-joint qualification.',
        'native_pcb_sha256': native_hash, 'generator_sha256': sha(Path(__file__)),
        'sources': {
            'package': {'url': 'https://mds.analog.com/api/public/content/tqfn_21-0136.pdf',
                        'revision': 'V', 'page_visually_read': 2,
                        'sha256': '8d5551d518227724b29191e4f4c884115ba9d4540bf09d4cdcccfb31da13f52d'},
            'land_pattern': {'url': 'https://mds.analog.com/api/public/content/90-0031.pdf',
                             'revision': 'C', 'sha256': '5661318725986f79e664adb5fd24d80c2b444c1d48d3aa4c1b0d51ebfa53f4c8'},
            'assembly_guidance': 'https://www.analog.com/en/resources/app-notes/smt-assembly-and-pcb-design-guidelines-for-maxims-standard-wirebonded-quad-flatpack.html',
        },
        'selected_package': {'code': 'T1633+4', 'body_mm': [3, 3], 'pitch_mm': 0.5,
                             'terminal_width_min_nom_max_mm': [0.2, 0.25, 0.3],
                             'terminal_length_min_nom_max_mm': [0.3, 0.4, 0.5]},
        'native_anchor_board_mm': anchor, 'peripheral_pads': signal,
        'land_pattern': {'native_width_mm': 0.25, 'drawing_90_0031_width_mm': 0.3,
                         'native_length_mm': 0.825, 'drawing_90_0031_length_mm': 0.8,
                         'inner_edge_from_center_mm': inner, 'outer_edge_from_center_mm': outer,
                         'nominal_outward_extension_mm': outer - 1.5,
                         'nominal_heel_extension_mm': 1.5 - 0.4 - inner,
                         'adjacent_pad_gap_mm': 0.5 - 0.25,
                         'thermal_copper_mm': [1.23, 1.23]},
        'paste': {'window_centers_local_mm': window_centers, 'rounded_window': window,
                  'thermal_coverage_fraction': coverage, 'peripheral_aperture': peripheral,
                  'native_aperture_stencil_examples_not_supplier_specification': stencil_cases},
        'disposition': 'Retain the native land pattern. Its 0.25 mm width matches nominal package terminals at 0.5 mm pitch, consistent with ADI fine-pitch guidance. The 0.35 mm toe extension lies in ADI guidance; the inner edge and exposed land match 90-0031. It is not a literal copy of 90-0031.',
        'production_requirements': ['Verify all pins and orientation on supplier production data.',
                                    'Use separated thermal apertures with 50-80% coverage and adequate release area ratio.',
                                    'Resolve consistent solder-mask and thermal-via treatment; this report does not verify local mask clearance.',
                                    'Supplier determines actual stencil thickness/apertures and reflow process; native F.Paste is not proof of the production stencil.'],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'pins_checked': len(pads),
                      'thermal_coverage_percent': 100 * coverage,
                      'stencil_examples': stencil_cases, 'native_unchanged': True}, indent=2))


if __name__ == '__main__':
    main()
