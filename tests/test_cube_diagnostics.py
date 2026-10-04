"""Independent board assertions and the real Cube sketch on simulated GPIO/serial."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'firmware/rooster/tools'
sys.path.insert(0, str(TOOLS))
from contract import header, load, verify
from build import verify_artifacts


def test_build_profile_matches_n16_without_psram_and_preserves_native_usb():
    profile = json.loads((ROOT / 'firmware/rooster/diagnostics/alarm/cube_diag/sketch.yaml').read_text())
    fqbn = profile['profiles']['cube']['fqbn'].split(':', 3)
    assert fqbn[:3] == ['esp32', 'esp32', 'esp32s3']
    options = dict(item.split('=') for item in fqbn[3].split(','))
    assert {key: options[key] for key in ['USBMode', 'CDCOnBoot', 'FlashMode', 'FlashSize', 'PSRAM']} == {
        'USBMode': 'hwcdc', 'CDCOnBoot': 'cdc', 'FlashMode': 'qio', 'FlashSize': '16M', 'PSRAM': 'disabled'}


def test_contract_matches_native_connectivity_and_off_polarities():
    c = verify()
    # Independent expectations from Cube BENCH.md and the electrical contract.
    assert {(p['gpio'], p['inactive_level']) for p in c['outputs']} == {
        (18, 0), (21, 0), (47, 0), (48, 0), (14, 0), (11, 0),
        (41, 0), (12, 0), (38, 1), (39, 1), (40, 1)}
    assert {p['gpio'] for p in c['inputs']} == {1, 4, 5, 6, 7, 10, 13, 15}
    assert all(p['active_level'] == 0 and p['debounce_ms'] >= 10
               for p in c['inputs'] if p['gpio'] in {4, 5, 6, 10})


@pytest.mark.parametrize('fault', ['legacy_oled', 'duplicate', 'reserved', 'wrong_peer', 'stale_source',
                                  'active_load', 'led_polarity', 'button_polarity', 'debounce', 'mcu'])
def test_contract_rejects_incompatible_mapping(fault):
    c = copy.deepcopy(load())
    if fault == 'legacy_oled': c['outputs'][6]['gpio'] = 7
    if fault == 'duplicate': c['outputs'][1]['gpio'] = 18
    if fault == 'reserved': c['outputs'][0]['gpio'] = 19
    if fault == 'wrong_peer': c['inputs'][0]['peer'] = 'U5.2'
    if fault == 'stale_source': c['source_sha256']['boards/alec-main/alec-main.kicad_sch'] = '0' * 64
    if fault == 'active_load': c['outputs'][0]['inactive_level'] = 1
    if fault == 'led_polarity': c['outputs'][-1]['inactive_level'] = 0
    if fault == 'button_polarity': c['inputs'][0]['active_level'] = 1
    if fault == 'debounce': c['inputs'][0]['debounce_ms'] = 0
    if fault == 'mcu': c['mcu'] = 'ESP32-S3-WROOM-1-N16R8'
    with pytest.raises(ValueError): verify(c)


@pytest.fixture(scope='module')
def host_binary(tmp_path_factory):
    compiler = shutil.which('c++')
    assert compiler, 'A C++17 host compiler is required for Cube firmware tests'
    work = tmp_path_factory.mktemp('cube-host')
    (work / 'board_config.h').write_text(header(verify()))
    (work / 'build_identity.h').write_text('\n'.join([
        '#define CUBE_IMAGE_ID "host-test"', '#define CUBE_SOURCE_REVISION "host-test"',
        '#define CUBE_CORE_VERSION "3.3.7"',
        '#define CUBE_SOURCE_SHA256 "host-test-source"', '#define CUBE_CONTRACT_SHA256 "host-test-contract"']))
    binary = work / 'cube-host-test'
    subprocess.run([compiler, '-std=c++17', '-Wall', '-Wextra', '-Werror',
                    '-I' + str(work), '-I' + str(ROOT / 'tests/firmware/fakes'),
                    '-I' + str(ROOT / 'firmware/rooster/diagnostics/alarm/cube_diag'),
                    str(ROOT / 'tests/firmware/cube_diag_test.cpp'), '-o', str(binary)], check=True)
    return binary


@pytest.mark.parametrize('scenario', ['normal', 'backpressure', 'disconnect', 'fault'])
def test_actual_sketch_startup_serial_sampling_and_failure_controls(host_binary, scenario):
    result = subprocess.run([str(host_binary), scenario], check=True, capture_output=True, text=True, timeout=10)
    lines = [json.loads(line) for line in result.stdout.splitlines()]
    assert lines and all(x['schema'] == 1 and x['image_id'] == 'host-test' for x in lines)
    if scenario in ('normal', 'fault'):
        assert [x['type'] for x in lines] == ['info', 'status', 'help', 'error', 'error']
        info, status = lines[:2]
        assert info['chip_id'] == '112233445566'
        assert len(info['app_elf_sha256']) == 64
        assert lines[2]['commands'] == ['info', 'status', 'help']
        assert lines[3]['error'] == 'unknown_command' and lines[4]['error'] == 'invalid_line'
        assert info['startup_ok'] == status['loads_commanded_off'] == (scenario == 'normal')
        assert status['inputs']['volume_minus']['active'] is (False if scenario == 'normal' else None)
        assert status['inputs']['pg_3v3']['active'] is (True if scenario == 'normal' else None)
        assert status['inputs']['pg_5v']['active'] is (False if scenario == 'normal' else None)
    elif scenario == 'backpressure':
        assert lines[-1]['inputs']['volume_minus']['active'] is True
        assert lines[-1]['inputs']['volume_minus']['transitions'] == 1
    else:
        assert lines[0]['error'] == 'unknown_command' and lines[1]['type'] == 'info'


def test_artifact_verifier_rejects_missing_and_changed_images(tmp_path):
    import hashlib
    artifacts = tmp_path / 'artifacts'
    artifacts.mkdir()
    names = ['cube_diag.ino.bin', 'cube_diag.ino.bootloader.bin', 'cube_diag.ino.partitions.bin', 'cube_diag.ino.elf']
    for name in names: (artifacts / name).write_bytes(b'test image')
    manifest = {'result': 'compile_pass', 'image_id': 'test',
                'artifacts': {n: hashlib.sha256(b'test image').hexdigest() for n in names}}
    path = tmp_path / 'manifest.json'
    path.write_text(json.dumps(manifest))
    verify_artifacts(path)
    (artifacts / names[0]).write_bytes(b'wrong image')
    with pytest.raises(ValueError, match='Artifact mismatch'): verify_artifacts(path)
    del manifest['artifacts'][names[0]]
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match='Not a complete'): verify_artifacts(path)
