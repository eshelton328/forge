#!/usr/bin/env python3
"""One-time ROO-002 capture. Refuses to replace an existing snapshot."""
import datetime
import hashlib
import json
import re
import shutil
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/erik/Workspaces/Electronics/Arduino')
EXPECTED = {
    'beacon_connected/beacon_connected.ino': 'fc16b4a53866',
    'beacon_cursor/beacon_cursor.ino': 'c238b9714153',
    'beacon_esp_now/beacon_esp_now.ino': 'cb54c240c9f2',
    'beacon_working_backup/beacon_working_backup.ino': 'cb54c240c9f2',
    'c3_beacon/c3_beacon.ino': 'e2be97701e40',
    'cube_MAX98357/cube_MAX98357.ino': 'fb11439c1997',
    'cube_browns/beacon_browns.ino': 'c238b9714153',
    'cube_browns/cube_browns.ino': '257cadfb2cd4',
    'cube_connected/cube_connected.ino': '183c024daeb4',
    'cube_cursor/cube_cursor.ino': '865692a83865',
    'cube_display_test/cube_display_test.ino': '656b3fa643c1',
    'cube_esp_now/cube_esp_now.ino': '6fefee567c2a',
    'cube_merge/cube_merge.ino': '01ae76b3aede',
    'cube_settings_save/cube_settings_save.ino': 'd23b43684126',
    'cube_working_backup/cube_working_backup.ino': '6fefee567c2a',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    snapshot = HERE / 'snapshot'
    snapshot.mkdir(exist_ok=False)
    original = snapshot / 'Arduino'
    for folder in sorted({Path(p).parts[0] for p in EXPECTED}):
        shutil.copytree(SOURCE / folder, original / folder)
    records = []
    for rel, prefix in EXPECTED.items():
        p = SOURCE / rel
        digest = sha(p)
        assert digest.startswith(prefix), f'Inventory changed: {rel}'
        assert digest == sha(original / rel), f'Copy differs: {rel}'
        source = p.read_text()
        lines = source.splitlines()
        header = []
        for line in lines:
            if line.startswith('//') or not line.strip():
                header.append(line)
            else:
                break
        def selected(pattern):
            return [{'line': i, 'text': line} for i, line in enumerate(lines, 1)
                    if re.search(pattern, line)]
        messages = [{'line': source[:m.start()].count('\n') + 1, 'text': m.group()}
                    for m in re.finditer(r'(?:typedef\s+)?struct\s+\w*\s*\{[^}]*\}\s*\w*\s*;', source)
                    if re.search(r'msg|message|packet', m.group(), re.I)]
        records.append({
            'path': rel, 'source_path': str(p), 'sha256': digest,
            'bytes': p.stat().st_size, 'source_mtime_ns': p.stat().st_mtime_ns,
            'target_inferred': 'ESP32-C3' if 'beacon' in p.stem else 'ESP32-S3',
            'target_evidence': 'Source header/name and pin map; physical board/FQBN unconfirmed',
            'flashed_status': 'unverified',
            'includes': selected(r'^\s*#\s*include'),
            'pins': selected(r'(?:#define\s+\w*(?:PIN|GPIO)\w*|(?:const|constexpr)\s+\w+\s+(?:PIN_|UART_|GPIO_)\w*)'),
            'message_layouts': messages,
            'protocol_constants': selected(r'(?:MSG_\w+\s*=|PROTO_VER|MAGIC_ROOS|ESPNOW_CHANNEL|#pragma pack)'),
            'entry_points': selected(r'^void\s+(?:setup|loop)\s*\('),
            'behavior_header_static_claims_only': '\n'.join(header),
        })
    snapshot_files = []
    for p in sorted(original.rglob('*')):
        if p.is_file():
            rel = p.relative_to(original)
            assert sha(p) == sha(SOURCE / rel)
            snapshot_files.append({'path': str(p.relative_to(snapshot)), 'sha256': sha(p),
                                   'bytes': p.stat().st_size, 'source_path': str(SOURCE / rel)})
    deps = []
    for name in ['U8g2', 'MyLD2410']:
        root = SOURCE / 'libraries' / name
        files = [{'path': str(p.relative_to(root)), 'sha256': sha(p), 'bytes': p.stat().st_size}
                 for p in sorted(root.rglob('*')) if p.is_file()]
        archive = snapshot / f'{name}.tar.gz'
        with tarfile.open(archive, 'w:gz') as out:
            out.add(root, arcname=name)
        with tarfile.open(archive) as saved:
            for f in files:
                data = saved.extractfile(name + '/' + f['path']).read()
                assert hashlib.sha256(data).hexdigest() == f['sha256']
                assert sha(root / f['path']) == f['sha256']
        props = dict(line.split('=', 1) for line in (root / 'library.properties').read_text().splitlines() if '=' in line)
        deps.append({'name': name, 'version': props['version'], 'source_path': str(root),
                     'archive': archive.name, 'sha256': sha(archive), 'files': files})
    supplemental = [{'path': str(p.relative_to(SOURCE)), 'sha256': sha(p),
                     'disposition': 'Outside the original 15; indexed only, original retained; role unverified'}
                    for p in sorted(SOURCE.rglob('*.ino'))
                    if 'libraries' not in p.relative_to(SOURCE).parts and str(p.relative_to(SOURCE)) not in EXPECTED]
    manifest = {'schema': 1, 'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'source_root': str(SOURCE), 'hardware_reference_commit': 'dc57b550ebe8c1943e7830468d73af3f93c5bb73',
                'candidates': records, 'snapshot_files': snapshot_files, 'dependencies': deps,
                'other_sketches_not_in_original_inventory': supplemental,
                'limitations': ['No flashed pair identified; no hardware testing or upload.',
                                'Current installed dependencies, not proven original build versions.',
                                'Toolchain packages are identified in build records, not vendored.',
                                'Read-only permissions and checksums are tamper evidence, not WORM storage.']}
    (snapshot / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    checks = [(sha(p), str(p.relative_to(snapshot))) for p in sorted(snapshot.rglob('*')) if p.is_file()]
    (snapshot / 'SHA256SUMS').write_text(''.join(f'{digest}  {rel}\n' for digest, rel in checks))
    archive = HERE / 'originals-2026-09-07.tar.gz'
    with tarfile.open(archive, 'x:gz') as out:
        out.add(snapshot, arcname='snapshot')
    (HERE / 'originals-2026-09-07.tar.gz.sha256').write_text(f'{sha(archive)}  {archive.name}\n')
    for p in snapshot.rglob('*'):
        p.chmod(0o555 if p.is_dir() else 0o444)
    snapshot.chmod(0o555)
    archive.chmod(0o444)
    print(json.dumps({'candidates': len(records), 'unique_hashes': len({r['sha256'] for r in records}),
                      'preserved_files': len(snapshot_files), 'archive_sha256': sha(archive),
                      'additional_sketches_indexed': len(supplemental)}, indent=2))

if __name__ == '__main__':
    main()
