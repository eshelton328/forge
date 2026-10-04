#!/usr/bin/env python3
"""Compile unchanged copies only. No upload, port access or core installation."""
import argparse
import datetime
import hashlib
import json
import shlex
import shutil
import subprocess
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cli', default='/Applications/Arduino IDE.app/Contents/Resources/app/lib/backend/resources/arduino-cli')
    parser.add_argument('--run', default='installed-core-3.3.7')
    args = parser.parse_args()
    snapshot = HERE / 'snapshot'
    manifest = json.loads((snapshot / 'manifest.json').read_text())
    run = HERE / 'build-records' / args.run
    run.mkdir(parents=True, exist_ok=False)
    work = HERE / '.work' / args.run
    work.mkdir(parents=True, exist_ok=False)
    libs = work / 'libraries'
    libs.mkdir()
    for dep in manifest['dependencies']:
        archive = snapshot / dep['archive']
        assert sha(archive) == dep['sha256']
        with tarfile.open(archive) as src:
            # This is the hash-verified archive produced from local library trees.
            src.extractall(libs)
        for f in dep['files']:
            assert sha(libs / dep['name'] / f['path']) == f['sha256']
    config = work / 'arduino-cli.yaml'
    config.write_text('directories:\n  data: /Users/erik/Library/Arduino15\n  user: ' + str(work / 'sketchbook') + '\n')
    (work / 'sketchbook').mkdir()
    base = [args.cli, '--config-file', str(config), '--no-color']
    results = []
    for name, command in [('cli-version', ['version']), ('cores', ['core', 'list']),
                          ('config', ['config', 'dump']), ('s3-board', ['board', 'details', '-b', 'esp32:esp32:esp32s3', '--json']),
                          ('c3-board', ['board', 'details', '-b', 'esp32:esp32:esp32c3', '--json'])]:
        p = subprocess.run(base + command, capture_output=True, text=True)
        (run / (name + '.txt')).write_text('$ ' + shlex.join(base + command) + '\n' + p.stdout + p.stderr + f'\nexit={p.returncode}\n')
        if name in ('s3-board', 'c3-board'):
            assert p.returncode == 0, f'{name}: board lookup failed'
            assert json.loads(p.stdout)['version'] == '3.3.7', 'This reproduction requires ESP32 core 3.3.7'
    (run / 'arduino-cli.yaml').write_text(config.read_text())
    targets = [('cube_browns_combined', None)]
    priority = ['cube_browns/cube_browns.ino', 'cube_browns/beacon_browns.ino']
    ordered = sorted(manifest['candidates'], key=lambda c: (c['path'] not in priority, c['path']))
    targets += [(c['path'].replace('/', '__').removesuffix('.ino'), c) for c in ordered]
    for ident, candidate in targets:
        if candidate is None:
            sketch = work / 'targets' / 'combined' / 'cube_browns'
            shutil.copytree(snapshot / 'Arduino' / 'cube_browns', sketch)
            fqbn = 'esp32:esp32:esp32s3'
            hashes = {str(p.relative_to(sketch)): sha(p) for p in sketch.iterdir() if p.is_file()}
        else:
            original = snapshot / 'Arduino' / candidate['path']
            assert sha(original) == candidate['sha256']
            sketch = work / 'targets' / ident / original.stem
            sketch.mkdir(parents=True)
            shutil.copy2(original, sketch / original.name)
            hashes = {original.name: sha(sketch / original.name)}
            fqbn = 'esp32:esp32:esp32c3' if candidate['target_inferred'] == 'ESP32-C3' else 'esp32:esp32:esp32s3'
        common = ['compile', '--fqbn', fqbn, '--libraries', str(libs), '--jobs', '4',
                  '--build-path', str(work / 'build' / ident), '--warnings', 'default']
        props_cmd = base + common + ['--show-properties=expanded', str(sketch)]
        props = subprocess.run(props_cmd, capture_output=True, text=True)
        (run / (ident + '.properties.txt')).write_text('$ ' + shlex.join(props_cmd) + '\n' + props.stdout + props.stderr)
        cmd = base + common + ['--verbose', str(sketch)]
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        start = time.monotonic()
        with (run / (ident + '.log')).open('w') as log:
            log.write('$ ' + shlex.join(cmd) + '\n')
            log.flush()
            try:
                p = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=300)
                code = p.returncode
            except subprocess.TimeoutExpired:
                code = 124
                log.write('\nStopped after 300 seconds.\n')
            log.write(f'\nexit={code}\n')
        assert hashes == {p.name: sha(p) for p in sketch.iterdir() if p.is_file()}
        bins = [{'path': str(p.relative_to(work)), 'sha256': sha(p), 'bytes': p.stat().st_size}
                for p in (work / 'build' / ident).glob('*.bin')]
        row = {'id': ident, 'candidate': candidate['path'] if candidate else 'combined original folder',
               'fqbn': fqbn, 'fqbn_status': 'inferred generic development target; not recovered upload settings',
               'command': cmd, 'started_utc': started, 'elapsed_seconds': round(time.monotonic()-start, 2),
               'exit_code': code, 'source_sha256': hashes, 'binaries': bins,
               'log': ident + '.log', 'properties': ident + '.properties.txt'}
        results.append(row)
        (run / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
        print(f'{ident}: exit {code} ({row["elapsed_seconds"]} s)', flush=True)
    print('No upload or physical test performed.', flush=True)

if __name__ == '__main__':
    main()
