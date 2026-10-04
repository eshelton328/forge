"""Apply and verify the reviewed main J4 finished-hole correction.

The purchasing CSV retains the historical footprint identity. This explicit
mechanical change preserves its selected part, electrical pins and pad copper.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = 'Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical'
NEW = 'Board:Samtec_TSW-104-07-G-S_Drill1.10mm'
OLD_DESCRIPTION = 'Through hole straight pin header, 1x04, 2.54mm pitch, single row'
NEW_DESCRIPTION = 'Samtec TSW-104-07-G-S, four 1.10mm finished holes for JLCPCB tolerance; 1.70mm lands, 2.54mm pitch'
RECORD = ROOT / 'docs/rooster/prototype-order/header-fit/source-transition.json'


def transform(text, forward=True):
    try:
        from .order_parts import parse, children, properties, value
    except ImportError:
        from order_parts import parse, children, properties, value
    root = parse(text)
    pcb = root[0] == 'kicad_pcb'
    assert pcb or root[0] == 'kicad_sch'
    fp, = [f for f in children(root, 'footprint' if pcb else 'symbol')
           if value(properties(f)['Reference'][2]) == 'J4']
    atom = fp[1] if pcb else properties(fp)['Footprint'][2]
    source, target = (OLD, NEW) if forward else (NEW, OLD)
    # Already applied is permitted for generator idempotence, but not mistaken
    # for the reverse transformation's input.
    if forward and value(atom) == NEW:
        return text
    assert value(atom) == source
    edits = [(atom.start, atom.end, json.dumps(target))]
    if pcb:
        desc, = children(fp, 'descr')
        expected, replacement = ((OLD_DESCRIPTION, NEW_DESCRIPTION) if forward
                                 else (NEW_DESCRIPTION, OLD_DESCRIPTION))
        assert value(desc[1]) == expected
        edits.append((desc[1].start, desc[1].end, json.dumps(replacement)))
        pads = children(fp, 'pad')
        assert {value(p[1]) for p in pads} == {'1', '2', '3', '4'} and len(pads) == 4
        for pad in pads:
            assert pad[2] == 'thru_hole'
            drill, = children(pad, 'drill')
            expected, replacement = ('1', '1.1') if forward else ('1.1', '1')
            assert str(drill[1]) == expected
            edits.append((drill[1].start, drill[1].end, replacement))
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def historical_source(text, relative):
    """Reconstruct exact pre-fit bytes; reject any other unrecorded source edit."""
    report = json.loads(RECORD.read_text())
    records = [r for r in report['files'] if r['path'] == str(relative)]
    if not records:
        return text
    record, = records
    assert hashlib.sha256(text.encode()).hexdigest() == record['after_sha256'], relative
    original = transform(text, forward=False)
    assert hashlib.sha256(original.encode()).hexdigest() == record['before_sha256'], relative
    return original


def apply_to_main(suffix):
    path = ROOT / 'boards/alec-main' / ('alec-main.' + suffix)
    before = path.read_text()
    after = transform(before)
    if before != after:
        path.write_text(after)


def expected_footprint(identity, ref, historical):
    if str(identity).startswith('boards/alec-main/') and ref == 'J4':
        assert historical == OLD
        return NEW
    return historical
