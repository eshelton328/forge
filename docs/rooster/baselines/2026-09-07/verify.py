#!/usr/bin/env python3
"""Verify the sealed capture; optionally compare original source files as well."""
import argparse
import hashlib
import io
import json
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compare-originals', action='store_true')
    args = parser.parse_args()
    archive = HERE / 'originals-2026-09-07.tar.gz'
    expected = (HERE / (archive.name + '.sha256')).read_text().split()[0]
    assert digest(archive.read_bytes()) == expected, 'Outer archive hash mismatch'
    with tarfile.open(archive) as saved:
        checks = saved.extractfile('snapshot/SHA256SUMS').read().decode().splitlines()
        checked = set()
        for line in checks:
            sha, rel = line.split('  ', 1)
            assert digest(saved.extractfile('snapshot/' + rel).read()) == sha, rel
            checked.add('snapshot/' + rel)
        actual = {x.name for x in saved.getmembers() if x.isfile()}
        assert actual == checked | {'snapshot/SHA256SUMS'}, 'Unlisted/missing archive files'
        manifest_bytes = saved.extractfile('snapshot/manifest.json').read()
        assert manifest_bytes == (HERE / 'manifest.json').read_bytes(), 'Manifest copy mismatch'
        manifest = json.loads(manifest_bytes)
        assert len(manifest['candidates']) == 15
        for f in manifest['snapshot_files']:
            assert digest(saved.extractfile('snapshot/' + f['path']).read()) == f['sha256'], f['path']
            if args.compare_originals:
                assert digest(Path(f['source_path']).read_bytes()) == f['sha256'], f['source_path']
        for dep in manifest['dependencies']:
            data = saved.extractfile('snapshot/' + dep['archive']).read()
            assert digest(data) == dep['sha256']
            with tarfile.open(fileobj=io.BytesIO(data)) as lib:
                for f in dep['files']:
                    assert digest(lib.extractfile(dep['name'] + '/' + f['path']).read()) == f['sha256']
    print(f'PASS: 15 candidates, {len(manifest["snapshot_files"])} original files, 2 dependency archives, all archive hashes.')
    if args.compare_originals:
        print('PASS: source sketches still match the captured originals.')

if __name__ == '__main__':
    main()
