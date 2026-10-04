#!/usr/bin/env python3
"""Build a pinned Cube diagnostic image and record its identity; never flash hardware."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from contract import ROOT, TARGET, header, sha, verify


def source_files():
    paths = list((TARGET / 'cube_diag').glob('*'))
    paths += list((ROOT / 'firmware/rooster/tools').glob('*.py'))
    paths += [TARGET / 'board-contract.json', ROOT / 'firmware/rooster/toolchain.json']
    return sorted(p for p in paths if p.is_file())


def source_identity():
    files = {str(p.relative_to(ROOT)): sha(p) for p in source_files()}
    digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    return digest, files


def verify_artifacts(path):
    path = Path(path).resolve()
    manifest = json.loads(path.read_text())
    required = {'cube_diag.ino.bin', 'cube_diag.ino.bootloader.bin',
                'cube_diag.ino.partitions.bin', 'cube_diag.ino.elf'}
    if manifest.get('result') != 'compile_pass' or not required <= set(manifest['artifacts']):
        raise ValueError('Not a complete successful Cube build manifest')
    for name, expected in manifest['artifacts'].items():
        if Path(name).name != name or sha(path.parent / 'artifacts' / name) != expected:
            raise ValueError(f'Artifact mismatch: {name}')
    print(f'PASS: artifact hashes for image {manifest["image_id"]}; this is not a physical test')
    return manifest


def build(cli, output):
    contract = verify()
    lock = json.loads((ROOT / 'firmware/rooster/toolchain.json').read_text())
    profile = json.loads((TARGET / 'cube_diag/sketch.yaml').read_text())
    selected = profile['profiles'][lock['profile']]
    if selected['platforms'][0]['platform'] != f'esp32:esp32 ({lock["esp32_core"]})':
        raise ValueError('Core/profile lock mismatch')
    version = subprocess.check_output([cli, 'version'], text=True).strip()
    match = re.search(r'Version:\s*(\S+)', version)
    if not match or match.group(1) != lock['arduino_cli']:
        raise ValueError(f'Use Arduino CLI {lock["arduino_cli"]}; found {version}')
    source_sha, sources = source_identity()
    revision = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = bool(subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain'], text=True).strip())
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix=source_sha[:12] + '-', dir=output))
    sketch = run / 'sketch/cube_diag'
    shutil.copytree(TARGET / 'cube_diag', sketch)
    (sketch / 'board_config.h').write_text(header(contract))
    identity = {'CUBE_IMAGE_ID': source_sha[:12], 'CUBE_SOURCE_SHA256': source_sha,
                'CUBE_SOURCE_REVISION': revision + ('-dirty' if dirty else ''),
                'CUBE_CONTRACT_SHA256': sha(TARGET / 'board-contract.json'),
                'CUBE_CORE_VERSION': lock['esp32_core']}
    (sketch / 'build_identity.h').write_text('#pragma once\n' + ''.join(
        f'#define {key} "{value}"\n' for key, value in identity.items()))
    command = [cli, 'compile', '--profile', lock['profile'], '--clean', '--warnings', 'all',
               '--build-path', str(run / 'build'), '--output-dir', str(run / 'artifacts'), str(sketch)]
    print(f'Compiling {identity["CUBE_IMAGE_ID"]}; log: {run / "compile.log"}', flush=True)
    with (run / 'compile.log').open('w') as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'Compile failed ({result.returncode}); see {run / "compile.log"}')
    artifacts = {p.name: sha(p) for p in sorted((run / 'artifacts').iterdir()) if p.is_file()}
    manifest = {'schema_version': 1, 'result': 'compile_pass', 'created_at': datetime.now(timezone.utc).isoformat(),
                'target': 'cube-diagnostics', 'image_id': source_sha[:12], 'source_sha256': source_sha,
                'source_revision': identity['CUBE_SOURCE_REVISION'], 'source_files': sources,
                'hardware_contract': contract, 'contract_sha256': identity['CUBE_CONTRACT_SHA256'],
                'toolchain': lock, 'cli_version': version, 'fqbn': selected['fqbn'], 'command': command,
                'artifacts': artifacts, 'physical_test': 'NOT_RUN'}
    path = run / 'manifest.json'
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    verify_artifacts(path)
    print(f'Manifest: {path}')
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', default=os.environ.get('ARDUINO_CLI', 'arduino-cli'))
    parser.add_argument('--output', type=Path, default=ROOT / '.cache/rooster-cube')
    parser.add_argument('--verify', type=Path, metavar='MANIFEST', help='Verify existing build files without compiling')
    args = parser.parse_args()
    if args.verify:
        verify_artifacts(args.verify)
    else:
        build(args.cli, args.output)


if __name__ == '__main__':
    main()
