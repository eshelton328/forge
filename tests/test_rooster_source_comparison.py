"""The independent comparison permits only the recorded main J4 change."""
import copy
import importlib.util
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "compare_native_sources",
    ROOT / "docs/rooster/prototype-order/tools/compare_native_sources.py",
)
comparison = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(comparison)


@pytest.fixture
def geometry_pair():
    before = {
        "pcb_sha256": "before",
        "footprints": {
            "J4": {
                "footprint": "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
                "xy": [161, 86], "angle": 0, "value": "Conn_01x04_Pin",
                "pads": [
                    {"number": str(i), "drill": [1.0, 1.0], "size": [1.7, 1.7],
                     "xy": [161, 86 + (i - 1) * 2.54], "net": net}
                    for i, net in enumerate(["GND", "/OLED_3V3", "/OLED_SCL", "/OLED_SDA"], 1)
                ],
            },
        },
        "tracks": [{"layer": "F.Cu", "net": "/OLED_SCL", "width": .2}],
        "vias": [{"drill": .3, "net": "GND"}],
        "copper": [{"net": "GND", "layer": "B.Cu", "polygons": [1, 2, 3]}],
    }
    after = copy.deepcopy(before)
    after["pcb_sha256"] = "after"
    after["footprints"]["J4"]["footprint"] = "Board:Samtec_TSW-104-07-G-S_Drill1.10mm"
    for pad in after["footprints"]["J4"]["pads"]:
        pad["drill"] = [1.1, 1.1]
    return before, after


def test_accepts_only_the_main_header_correction_without_mutating_inputs(geometry_pair):
    before, after = geometry_pair
    originals = copy.deepcopy(geometry_pair)
    comparison.compare_geometry("alec-main", before, after)
    assert geometry_pair == originals
    comparison.compare_geometry("alec-sensor", before, before)
    with pytest.raises(AssertionError, match="native geometry differs"):
        comparison.compare_geometry("alec-sensor", before, after)


@pytest.mark.parametrize("path,value", [
    (("footprints", "J4", "footprint"), "unreviewed-header"),
    (("footprints", "J4", "xy"), [162, 86]),
    (("footprints", "J4", "pads", 0, "drill"), [1.2, 1.2]),
    (("footprints", "J4", "pads", 0, "net"), "/OLED_SDA"),
    (("footprints", "J4", "pads", 0, "size"), [1.6, 1.6]),
    (("footprints", "J4", "pads", 0, "number"), "2"),
    (("tracks", 0, "layer"), "B.Cu"),
    (("tracks",), []),
    (("vias", 0, "drill"), .4),
    (("copper", 0, "polygons"), [1, 2]),
])
def test_unrelated_geometry_change_is_rejected(geometry_pair, path, value):
    before, after = geometry_pair
    parent = after
    for key in path[:-1]:
        parent = parent[key]
    parent[path[-1]] = value
    with pytest.raises(AssertionError, match="native geometry differs"):
        comparison.compare_geometry("alec-main", before, after)


@pytest.fixture
def circuit_pair():
    before = ET.fromstring('''<export><components>
      <comp ref="J4"><value>Conn_01x04_Pin</value>
        <footprint>Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical</footprint></comp>
      <comp ref="J1"><value>Battery</value><footprint>BatteryHeader</footprint></comp>
      </components><nets><net name="GND"><node ref="J4" pin="1"/>
      <node ref="J1" pin="2"/></net></nets></export>''')
    after = copy.deepcopy(before)
    after.find('./components/comp[@ref="J4"]/footprint').text = "Board:Samtec_TSW-104-07-G-S_Drill1.10mm"
    return before, after


def test_current_netlist_accepts_header_identity_change_only(circuit_pair):
    before, after = circuit_pair
    comparison.compare_circuit("alec-main", before, after)
    comparison.compare_circuit("alec-controls", before, before)
    with pytest.raises(AssertionError, match="exported circuit differs"):
        comparison.compare_circuit("alec-controls", before, after)
    with pytest.raises(AssertionError, match="exported circuit differs"):
        comparison.compare_circuit("alec-main", before, before)


@pytest.mark.parametrize("change", ["footprint", "value", "net", "pin", "dnp", "missing_component"])
def test_unrelated_netlist_change_is_rejected(circuit_pair, change):
    before, after = circuit_pair
    header = after.find('./components/comp[@ref="J4"]')
    if change in ("footprint", "value"):
        header.find(change).text = "unreviewed"
    elif change == "net":
        after.find("./nets/net").set("name", "/OLED_3V3")
    elif change == "pin":
        after.find("./nets/net/node").set("pin", "2")
    elif change == "dnp":
        ET.SubElement(header, "property", name="dnp")
    else:
        after.find("./components").remove(after.find('./components/comp[@ref="J1"]'))
    with pytest.raises(AssertionError, match="exported circuit differs"):
        comparison.compare_circuit("alec-main", before, after)


def test_report_output_cannot_overwrite_historical_evidence(tmp_path):
    report = tmp_path / "native-geometry-comparison.json"
    report.write_text("historical evidence\n")
    with pytest.raises(SystemExit) as error:
        comparison.main(["--output-dir", str(tmp_path)])
    assert error.value.code == 2
    assert report.read_text() == "historical evidence\n"
