#!/usr/bin/env python3
"""Validate the working proposal against independent source BOMs and catalog captures.

This validates identity/nominal selection and evidence continuity, not DC bias,
component operating margin, placement rotation or manufacturing readiness.
Run from any directory; only selection-audit.json is written.
"""
import collections
import csv
import datetime
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def numeric(value):
    value = value.replace('Ω', '').replace('µF', 'u').replace('uF', 'u')
    m = re.fullmatch(r'(\d+(?:\.\d+)?)([kKMu]?)', value)
    assert m, value
    return float(m[1]) * {'': 1, 'k': 1e3, 'K': 1e3, 'M': 1e6, 'u': 1e-6}[m[2]]


def resistor(mpn):
    if mpn.startswith(('RC0402', 'RT0402')):
        code = re.search(r'07(.+)L$', mpn)[1]
        m = re.fullmatch(r'(\d+)([RKM])(\d*)', code)
        assert m, mpn
        return float(m[1] + '.' + (m[3] or '0')) * {'R': 1, 'K': 1e3, 'M': 1e6}[m[2]]
    if mpn == '0402WGF1500TCE':
        digits = mpn[7:11]
        return int(digits[:3]) * 10 ** int(digits[-1])
    raise AssertionError(mpn)


def capacitor(mpn):
    if mpn.startswith('GRM'):
        m = re.fullmatch(r'GRM(.{3})(R6|R7)(.{2})(\d{3})([KM]).+', mpn)
        assert m, mpn
        size = {'15': '0402', '18': '0603', '21': '0805', '31': '1206'}[m[1][:2]]
        farads = int(m[4][:2]) * 10 ** int(m[4][2]) * 1e-12
        return farads, {'1A': 10, '1C': 16, '1E': 25}[m[3]], size, {'R6': 'X5R', 'R7': 'X7R'}[m[2]]
    if mpn == 'CL31A107MQHNNNE':
        return 100e-6, 6.3, '1206', 'X5R'
    raise AssertionError(mpn)


def main():
    rows = list(csv.DictReader((HERE / 'sourcing.csv').open()))
    assert len(rows) == len({(r['board'], r['reference']) for r in rows}) == 208
    audit = json.loads((HERE / 'assembly-audit.json').read_text())
    sources, fields, hashes = {}, {}, {}
    for board, saved in audit['boards'].items():
        bp = ROOT / 'boards' / board
        native = bp / (board + '.kicad_pcb')
        assert sha(native) == saved['source_sha256'], board
        hashes[str(native.relative_to(ROOT))] = sha(native)
        for r in csv.DictReader((bp / 'review/bom.csv').open()):
            sources[board, r['Reference']] = r
        netlist = bp / 'review/netlist.xml'
        hashes[str(netlist.relative_to(ROOT))] = sha(netlist)
        root = ET.parse(netlist).getroot()
        for comp in root.findall('./components/comp'):
            fields[board, comp.attrib['ref']] = {x.attrib['name']: x.text for x in comp.findall('./fields/field')}
    assert set(sources) == {(r['board'], r['reference']) for r in rows}
    counts = collections.Counter()
    no_stock = []
    for r in rows:
        key = r['board'], r['reference']
        source = sources[key]
        for original, canonical in [('value', 'Value'), ('footprint', 'Footprint'), ('candidate_mpn', 'MPN')]:
            assert r[original] == source[canonical], (key, original)
        if key == ('alec-main', 'R11'):
            assert not r['proposed_mpn'] and not r['supplier_part_id'] and r['order_gate'] == 'DNP'
            counts['source_dnp_retained'] += 1
            continue
        mpn = r['proposed_mpn']
        capture = HERE / r['catalog_capture']
        d = json.loads(capture.read_text())
        hits = [m for q in d['queries'] for m in q.get('matches', []) if m['componentCode'] == r['supplier_part_id']]
        assert hits and all(m['componentModelEn'].casefold() == mpn.casefold() and m['componentBrandEn'] == r['manufacturer'] for m in hits), key
        counts['manufacturer_and_mpn_catalog_matches'] += 1
        if not int(r['observed_stock']): no_stock.append('/'.join(key))
        if r['reference'].startswith('R'):
            assert abs(resistor(mpn) / numeric(r['value']) - 1) < 1e-9, key
            assert 'R_0402' in r['footprint']
            if fields[key].get('Tolerance') == '0.1%': assert mpn.startswith('RT0402BRD'), key
            counts['resistor_nominals_checked'] += 1
        if r['reference'].startswith('C'):
            farads, volts, size, dielectric = capacitor(mpn)
            assert abs(farads / numeric(r['value']) - 1) < 1e-9 and ':C_' + size + '_' in r['footprint'], key
            minimum = fields[key].get('Voltage')
            if minimum: assert volts >= float(re.search(r'[\d.]+', minimum)[0]), (key, minimum, volts)
            requested = fields[key].get('Dielectric')
            if requested: assert dielectric in requested, (key, requested, dielectric)
            counts['capacitor_nominal_size_and_declared_rating_checks'] += 1
    assert counts['manufacturer_and_mpn_catalog_matches'] == 207
    grouped = json.loads((HERE / 'proposed-parts.json').read_text())
    flattened = {}
    for item in grouped['parts']:
        refs = [(b, ref) for b, rs in item['references'].items() for ref in rs]
        assert item['fitted_quantity_two_sets'] == len(refs) * 2
        for key in refs:
            assert key not in flattened
            flattened[key] = (item['proposed_mpn'], item['manufacturer'], item['supplier_part_id'])
    expected = {(r['board'], r['reference']): (r['proposed_mpn'], r['manufacturer'], r['supplier_part_id']) for r in rows if r['proposed_mpn']}
    assert flattened == expected
    assert sum(x['fitted_quantity_two_sets'] for x in grouped['parts']) == 414
    counts['grouped_unique_parts_reconciled'] = len(grouped['parts'])
    counts['source_rows_preserved'] = len(rows)
    for capture in HERE.glob('jlc-*-20260907.json'):
        assert not re.search(r'x-oss-|access_token|signature=', capture.read_text(), re.I), capture
        hashes[str(capture.relative_to(ROOT))] = sha(capture)
    hashes[str((HERE / 'sourcing.csv').relative_to(ROOT))] = sha(HERE / 'sourcing.csv')
    hashes[str((HERE / 'proposed-parts.json').relative_to(ROOT))] = sha(HERE / 'proposed-parts.json')
    result = {'captured_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'command': 'python3 docs/rooster/prototype-order/tools/verify_sourcing.py',
              'result': 'PASS_WITH_OPEN_ENGINEERING_AND_PROCUREMENT_GATES',
              'scope': 'Original source BOM fields, catalog manufacturer/MPN identity, independently decoded passive nominal values, declared voltage/dielectric constraints, native board hash continuity. Does not validate DC-bias curves, current/thermal margin, all component drawings, assembly rotations, supplier commitments or final manufacturing files.',
              'checks': dict(counts), 'no_ready_catalog_stock_references': no_stock, 'input_sha256': hashes}
    (HERE / 'selection-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'checks': dict(counts), 'no_ready_catalog_stock_references': no_stock}))


if __name__ == '__main__':
    main()
