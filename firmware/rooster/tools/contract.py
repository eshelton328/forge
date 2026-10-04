"""Check the frozen Cube pin contract against source hashes and net connectivity."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / 'firmware/rooster/diagnostics/alarm'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load():
    return json.loads((TARGET / 'board-contract.json').read_text())


def verify(contract=None, netlist=None):
    c = load() if contract is None else contract
    low_outputs = {'amp_enable', 'amp_shutdown', 'i2s_bclk', 'i2s_lrclk', 'i2s_data',
                   'display_bus_enable', 'display_power', 'battery_measure_enable'}
    high_outputs = {'led_red', 'led_green', 'led_blue'}
    if {p['name'] for p in c['outputs']} != low_outputs | high_outputs:
        raise ValueError('Only the reviewed inactive output set is allowed')
    for pin in c['outputs']:
        if pin['inactive_level'] != int(pin['name'] in high_outputs):
            raise ValueError(f'Unsafe inactive polarity: {pin["name"]}')
    buttons = {'volume_minus', 'mode', 'volume_plus', 'battery_button'}
    if {p['name'] for p in c['inputs']} != buttons | {'pg_3v3', 'pg_5v', 'usb_present', 'rtc_interrupt'}:
        raise ValueError('Unexpected monitored input set')
    for pin in c['inputs']:
        if pin['active_level'] != int(pin['name'] in {'pg_3v3', 'pg_5v', 'usb_present'}):
            raise ValueError(f'Wrong input polarity: {pin["name"]}')
        if pin['debounce_ms'] != (10 if pin['name'] in buttons else 0):
            raise ValueError(f'Wrong debounce contract: {pin["name"]}')
    if c['reserved_gpio'] != [0, 19, 20, 43, 44]:
        raise ValueError('Boot, USB and UART pins must remain reserved')
    for path, expected in c['source_sha256'].items():
        if sha(ROOT / path) != expected:
            raise ValueError(f'Hardware contract is stale: {path}; review before updating its binding')
    tree = ET.parse(netlist or ROOT / 'boards/alec-main/review/netlist.xml')
    mcu = tree.find('./components/comp[@ref="U3"]/fields/field[@name="MPN"]')
    if mcu is None or mcu.text != c['mcu']:
        raise ValueError('MCU part does not match the native BOM')
    nets = tree.findall('./nets/net')
    seen = set()
    for signal in c['outputs'] + c['inputs'] + c['quiet_inputs']:
        gpio = signal['gpio']
        if gpio in seen or gpio in c['reserved_gpio']:
            raise ValueError(f'Duplicate/reserved GPIO: {gpio}')
        seen.add(gpio)
        ref, pin = signal['peer'].split('.')
        found = [n for n in nets if any(x.get('ref') == ref and x.get('pin') == pin for x in n)]
        if len(found) != 1 or not any(
            x.get('ref') == 'U3' and re.fullmatch(rf'IO{gpio}_\d+', x.get('pinfunction', ''))
            for x in found[0]
        ):
            raise ValueError(f'GPIO{gpio} does not reach {signal["peer"]}: {signal["name"]}')
        if not re.fullmatch('[a-z][a-z0-9_]*', signal['name']):
            raise ValueError('Invalid signal name')
    return c


def header(c):
    """Generate the one pin table consumed by both native and ESP32 builds."""
    lines = ['#pragma once', '#include <stdint.h>', 'namespace cube {',
             'struct OutputPin { const char* name; uint8_t gpio; bool inactive; };',
             'struct InputPin { const char* name; uint8_t gpio; bool active; uint32_t debounce_ms; };',
             'constexpr OutputPin kOutputs[] = {']
    lines += [f'  {{"{x["name"]}", {x["gpio"]}, {str(bool(x["inactive_level"])).lower()}}},' for x in c['outputs']]
    lines += ['};', 'constexpr InputPin kInputs[] = {']
    lines += [f'  {{"{x["name"]}", {x["gpio"]}, {str(bool(x["active_level"])).lower()}, {x["debounce_ms"]}}},' for x in c['inputs']]
    lines += ['};', 'constexpr uint8_t kQuietInputs[] = {' + ', '.join(str(x['gpio']) for x in c['quiet_inputs']) + '};',
              'constexpr unsigned kInputCount = sizeof(kInputs) / sizeof(kInputs[0]);',
              '}  // namespace cube', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', type=Path, help='Optional freshly exported KiCad XML')
    args = parser.parse_args()
    c = verify(netlist=args.netlist)
    print(f'PASS: {c["id"]}; {len(c["outputs"])} inactive outputs, {len(c["inputs"])} monitored inputs')
