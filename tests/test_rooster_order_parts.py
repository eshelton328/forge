"""Guard the purchasing update against wiring, fit-status and placement changes."""
import copy

import pytest

from scripts.alarm import order_parts as order


PCB = '''(kicad_pcb (version 20260101)
 (footprint "Capacitor_SMD:C_0603_1608Metric" (layer "B.Cu") (at 17 23 90)
  (property "Reference" "C3") (property "Value" "10µF")
  (property "MPN" "old" (at 1 2 0) (layer "B.Fab") (hide yes))
  (pad "1" smd rect (at 0 0) (size 1 1) (net 2 "5v"))
  (model "part.step" (offset (xyz 0 0 1)))
 )
 (footprint "Resistor_SMD:R_0402_1005Metric" (layer "F.Cu")
  (property "Reference" "R11") (property "Value" "1kΩ") (attr smd dnp)
  (pad "1" smd rect (at 2 2) (size 1 1) (net 1 "GND")))
 (segment (start 17 23) (end 19 23) (width 0.4) (layer "F.Cu") (net 2)))'''

ROW = {"reference": "C3", "value": "10µF", "footprint": "Capacitor_SMD:C_0603_1608Metric",
       "proposed_mpn": "GRT188R61A106KE13D", "manufacturer": "Murata Electronics",
       "supplier_part_id": "C782172", "proposed_datasheet": "https://example.com/cap.pdf"}


def test_update_preserves_non_ordering_data_and_is_idempotent():
    revised, refs = order.synchronize_text(PCB, {"C3": ROW}, "example.kicad_pcb")
    assert refs == ["C3"]
    assert revised != PCB
    assert not any(line.endswith((" ", "\t")) for line in revised.splitlines())
    assert order.non_ordering_signature(PCB) == order.non_ordering_signature(revised)
    # Excluded parts must retain even their metadata byte-for-byte.
    assert revised[revised.index(' (footprint "Resistor'): ] == PCB[PCB.index(' (footprint "Resistor'): ]
    twice, _ = order.synchronize_text(revised, {"C3": ROW}, "example.kicad_pcb")
    assert twice == revised
    fp = order.children(order.parse(revised), "footprint")[0]
    props = order.properties(fp)
    assert order.value(props["LCSC#"][2]) == "C782172"
    assert order.value(order.children(props["LCSC#"], "layer")[0][1]) == "B.Fab"


@pytest.mark.parametrize("old,new", [
    ('(at 17 23 90)', '(at 18 23 90)'),
    ('(layer "B.Cu")', '(layer "F.Cu")'),
    ('(net 2 "5v")', '(net 2 "3v3")'),
    ('(attr smd dnp)', '(attr smd)'),
    ('(width 0.4)', '(width 0.3)'),
    ('(xyz 0 0 1)', '(xyz 0 0 2)'),
    ('"10µF"', '"22µF"'),
])
def test_non_ordering_change_invalidates_equivalence(old, new):
    assert old in PCB
    assert order.non_ordering_signature(PCB.replace(old, new)) != order.non_ordering_signature(PCB)


@pytest.mark.parametrize("key,replacement", [("value", "22µF"), ("footprint", "Capacitor_SMD:C_0402_1005Metric")])
def test_stale_inventory_cannot_write_over_a_changed_design(key, replacement):
    row = copy.deepcopy(ROW)
    row[key] = replacement
    with pytest.raises(AssertionError, match=key):
        order.synchronize_text(PCB, {"C3": row}, "example.kicad_pcb")


def test_library_defaults_are_not_discarded_by_comparison():
    source = '(kicad_sch (lib_symbols (symbol "Device:C" (property "MPN" "library"))))'
    assert order.non_ordering_signature(source) != order.non_ordering_signature(source.replace('"library"', '"changed"'))


def test_schematic_symbol_update_preserves_hidden_fields_and_flags():
    source = '''(kicad_sch (lib_symbols)
      (symbol (lib_id "Device:C") (at 10 20 0) (in_bom yes) (dnp no)
        (property "Reference" "C3") (property "Value" "10µF")
        (property "Footprint" "Capacitor_SMD:C_0603_1608Metric")
        (property "Voltage" "10V minimum") (uuid "component-id")))'''
    revised, refs = order.synchronize_text(source, {"C3": ROW}, "sheet.kicad_sch")
    assert refs == ["C3"]
    assert order.non_ordering_signature(source) == order.non_ordering_signature(revised)
    assert order.synchronize_text(revised, {"C3": ROW}, "sheet.kicad_sch")[0] == revised


def test_rejects_duplicate_ordering_fields():
    with pytest.raises(AssertionError, match="Duplicate property"):
        order.synchronize_text(PCB.replace('(property "MPN" "old"', '(property "MPN" "duplicate") (property "MPN" "old"'), {"C3": ROW}, "duplicate.kicad_pcb")
