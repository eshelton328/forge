"""The connector-hole correction cannot authorize unrelated native changes."""
import hashlib
import json
import pytest
from scripts.alarm import header_fit as fit


@pytest.mark.parametrize('record', json.loads(fit.RECORD.read_text())['files'])
def test_only_recorded_header_change_is_reversible(record):
    current = (fit.ROOT / record['path']).read_text()
    before = fit.historical_source(current, record['path'])
    assert hashlib.sha256(before.encode()).hexdigest() == record['before_sha256']
    assert fit.transform(before) == current
    assert fit.transform(current) == current


@pytest.mark.parametrize('old,new', [
    ('(at 161 86)', '(at 162 86)'),
    ('(drill 1.1)', '(drill 1.2)'),
    ('(net "/OLED_SCL")', '(net "/OLED_SDA")'),
])
def test_unrecorded_placement_hole_or_net_change_fails(old, new):
    relative = 'boards/alec-main/alec-main.kicad_pcb'
    current = (fit.ROOT / relative).read_text()
    assert old in current
    with pytest.raises(AssertionError):
        fit.historical_source(current.replace(old, new, 1), relative)
