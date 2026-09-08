#!/usr/bin/env python3
"""Read-only USB routing inventory; does not certify impedance or USB operation."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import pcbnew as p

ROOT = Path(__file__).resolve().parents[4]
NETS = ('Net-(J2-D+-PadA6)', 'Net-(J2-D--PadA7)', '/USB_MCU_P',
        '/D+', '/USB_MCU_N', '/D-')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xy(point):
    return [p.ToMM(point.x), p.ToMM(point.y)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), 'Refusing to overwrite an existing inventory'
    step = .05
    report = {'scope': __doc__, 'generator_sha256': sha(Path(__file__)),
              'sample_step_mm': step,
              'limitations': ['Centerline samples do not check the whole return-current corridor.',
                  'Segment totals include USB-C orientation branches; they are not path skew.',
                  'No field-solver, impedance coupon or physical USB test is represented.'],
              'boards': {}}
    for name in ('alec-main', 'alec-sensor'):
        source = ROOT / 'boards' / name / (name + '.kicad_pcb')
        digest = sha(source)
        board = p.LoadBoard(str(source))
        ground = [z.GetFilledPolysList(p.In1_Cu) for z in board.Zones()
                  if str(z.GetNetname()) == 'GND' and z.IsOnLayer(p.In1_Cu)]
        assert ground and all(poly.OutlineCount() for poly in ground)
        tracks = [t for t in board.GetTracks() if str(t.GetNetname()) in NETS]
        vias = [t for t in tracks if isinstance(t, p.PCB_VIA)]
        assert not vias and all(t.GetLayer() == p.F_Cu for t in tracks)
        result = {'source_sha256': digest, 'usb_via_count': len(vias),
                  'all_usb_tracks_top': True, 'nets': {}, 'interface_pads': {}}
        for net in NETS:
            rows = []
            for track in tracks:
                if str(track.GetNetname()) != net:
                    continue
                assert type(track) == p.PCB_TRACK, 'Arc needs arc sampling'
                a, b = track.GetStart(), track.GetEnd()
                length = p.ToMM(track.GetLength())
                count = max(1, math.ceil(length / step))
                gaps = []
                for i in range(count + 1):
                    pos = p.VECTOR2I(round(a.x + (b.x - a.x) * i / count),
                                    round(a.y + (b.y - a.y) * i / count))
                    if not any(poly.Contains(pos) for poly in ground):
                        gaps.append(xy(pos))
                rows.append({'start_mm': xy(a), 'end_mm': xy(b), 'length_mm': length,
                             'width_mm': p.ToMM(track.GetWidth()),
                             'ground_sample_count': count + 1 - len(gaps),
                             'samples_without_in1_ground': gaps})
            assert rows, 'Required USB net has no tracks'
            result['nets'][net] = {
                'segment_length_total_mm': sum(r['length_mm'] for r in rows),
                'sample_count': sum(r['ground_sample_count'] + len(r['samples_without_in1_ground']) for r in rows),
                'gap_sample_count': sum(len(r['samples_without_in1_ground']) for r in rows),
                'tracks': rows}
        for fp in board.GetFootprints():
            ref = fp.GetReference()
            if ref not in ('U3', 'U4', 'J2', 'J7', 'R34', 'R35', 'SW2', 'SW3'):
                continue
            pads = []
            for pad in fp.Pads():
                if ref == 'U3' and pad.GetNumber() not in ('3', '13', '14', '27', '36', '37'):
                    continue
                pads.append({'pin': str(pad.GetNumber()), 'net': str(pad.GetNetname()),
                             'position_mm': xy(pad.GetPosition())})
            result['interface_pads'][ref] = {'value': str(fp.GetValue()), 'pads': pads}
        assert sha(source) == digest
        report['boards'][name] = result
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({name: {'native_sha256': b['source_sha256'],
        'segment_total_mm': sum(n['segment_length_total_mm'] for n in b['nets'].values()),
        'samples': sum(n['sample_count'] for n in b['nets'].values()),
        'ground_gap_samples': sum(n['gap_sample_count'] for n in b['nets'].values())}
        for name, b in report['boards'].items()}, indent=2))


if __name__ == '__main__':
    main()
