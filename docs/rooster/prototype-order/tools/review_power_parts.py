#!/usr/bin/env python3
"""Source-bound, offline capacitor-bank and inductor selection calculations.

Typical manufacturer curves plus explicit engineering allowances are a selection
screen, not a guarantee of converter stability, temperature or battery endurance.
"""
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts/alarm'))
from order_parts import baseline_source, verify_transition, native_order_fields
CURVES = HERE / "murata-curves-20260908.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def interpolate(data, voltage):
    points = [(x[0], y[0]) for x, y in data]
    assert points[0][0] <= voltage <= points[-1][0]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 <= voltage <= x1:
            return y0 + (y1 - y0) * (voltage - x0) / (x1 - x0)
    raise AssertionError(voltage)


def main():
    rows = list(csv.DictReader((HERE / "sourcing.csv").open()))
    proposed = {(r["board"], r["reference"]): r for r in rows}
    captured = json.loads(CURVES.read_text())
    available = {}
    for item in captured["curves"]:
        if item["status"] != "CURVE_RETRIEVED":
            continue
        curve, = item["response"]["JsonCharaData"][0]["charadata"]
        assert not curve["error"]
        key = item["mpn"], float(curve["ac"]), float(curve["tc"])
        assert key not in available
        assert (curve["x_unit"], curve["y_unit"], curve["y_subunit"]) == ("V", "F", "u")
        available[key] = curve

    # Independent check against SVG coordinates read from the manufacturer UI.
    # Plot rectangle: x=42.8515625..353 for 0..16 V, y=244..10 for 0..30 uF.
    ui_y = [62.82679999999999, 125.79105313355495, 179.0354187126819,
            205.39309228583016, 218.10439173083512]
    ui_curve = available["GRM31CR61C226KE15L", .5, 25]
    ui_checks = []
    for voltage, pixel_y in zip([0, 4, 8, 12, 16], ui_y):
        svg_uf = (244 - pixel_y) * 30 / 234
        api_uf = interpolate(ui_curve["data"], voltage)
        assert abs(svg_uf - api_uf) < 1e-9
        ui_checks.append({"voltage": voltage, "svg_uF": svg_uf, "api_uF": api_uf})

    def cap(ref, board, voltage):
        mpn = proposed[board, ref]["proposed_mpn"]
        samples = {str(t): interpolate(available[mpn, .01, t]["data"], voltage)
                   for t in [-55, 25, 85]}
        # K = +/-10%, M = +/-20%; subtract nominal tolerance, then an extra
        # 20% engineering reserve. This reserve is not a manufacturer bound.
        tolerance = {"K": .1, "M": .2}[mpn[13]]
        return {"reference": ref, "mpn": mpn, "bias_V": voltage,
                "typical_uF_at_sampled_temperatures_C": samples,
                "nominal_tolerance_fraction": tolerance,
                "additional_engineering_reserve_fraction": .2,
                "screen_uF": min(samples.values()) * (1-tolerance) * .8}

    hashes = {str(CURVES.relative_to(ROOT)): sha(CURVES),
              str((HERE / "sourcing.csv").relative_to(ROOT)): sha(HERE / "sourcing.csv"),
              str(Path(__file__).resolve().relative_to(ROOT)): sha(Path(__file__))}
    audit = json.loads((HERE / "assembly-audit.json").read_text())
    hashes.update(verify_transition())
    banks = []
    rails = {}
    for board in ["alec-main", "alec-sensor"]:
        bp = ROOT / "boards" / board
        native = bp / (board + ".kicad_pcb")
        assert hashlib.sha256(baseline_source(native.relative_to(ROOT)).encode()).hexdigest() == audit["boards"][board]["source_sha256"]
        native_order_fields(board)
        netpath = bp / "review/netlist.xml"
        hashes[str(native.relative_to(ROOT))] = sha(native)
        hashes[str(netpath.relative_to(ROOT))] = sha(netpath)
        netlist = ET.parse(netpath).getroot()
        pins = {(n.attrib["ref"], n.attrib["pin"]): net.attrib["name"]
                for net in netlist.findall("./nets/net") for n in net.findall("node")}
        values = {c.attrib["ref"]: c.findtext("value").replace("Ω", "")
                  for c in netlist.findall("./components/comp")}
        for ref in ["L1", "L2"]:
            assert proposed[board, ref]["proposed_mpn"] == "XFL4020-152MEC"
            assert values[ref] == "1.5µH", (board, ref, values[ref])
        for ic, refs, volts, role in [
            ("U1", ["C1", "C2", "C3"], 5.4, "input"),
            ("U2", ["C9", "C10", "C11"], 5.4, "input"),
            ("U1", ["C5", "C6", "C7", "C8"], 3.6, "output"),
            ("U2", ["C13", "C14", "C15", "C16"], 5.4, "output"),
        ]:
            rail = pins[ic, "12" if role == "input" else "7"]
            for ref in refs:
                assert {pins[ref, "1"], pins[ref, "2"]} == {rail, "GND"}
            members = [cap(ref, board, volts) for ref in refs]
            total = sum(c["screen_uF"] for c in members)
            minimum = 4.7 if role == "input" else 18.0  # 10 x 1.8 uH upper tolerance
            assert total >= minimum, (board, ic, role, total)
            banks.append({"board": board, "converter": ic, "role": role,
                          "net": rail, "members": members, "screen_total_uF": total,
                          "TI_minimum_uF": minimum, "ratio_to_minimum": total/minimum})
        for ic, top, bottom, ceiling in [("U1", "R4", "R5", 3.6), ("U2", "R8", "R9", 5.4)]:
            assert pins[top, "2"] == pins[bottom, "1"] == pins[ic, "5"]
            assert pins[bottom, "2"] == "GND"
            assert pins[top, "1"] == pins[ic, "7"]
            assert values[top] in ["470k", "680k"] and values[bottom] in ["150k", "130k"]
            rt, rb = float(values[top][:-1])*1000, float(values[bottom][:-1])*1000
            # +3% PFM accuracy, 1% resistor extremes and worst-direction 100nA
            # FB leakage through Rtop. Excludes ripple/overshoot and resistor TCR.
            static_max = .8*1.03*(1+rt*1.01/(rb*.99)) + 100e-9*rt*1.01
            assert static_max < ceiling
            rails[board + "/" + ic] = {"static_max_V": static_max,
                                          "capacitor_screen_bias_V": ceiling}

    inductor_cases = []
    # Source-case loads retain the earlier 0.25 A digital / 1 W audio proposal.
    # 0.5 A digital, depleted input and 2 A output are explicitly stress cases.
    for name, vin, vout, amps in [
        ("digital_reference", 3, 3.3, .25),
        ("digital_stress", 3, 3.3, .5),
        ("cube_5V_allowance_for_1W_audio", 3, 5, .3),
        ("beacon_5V_200mA_supply_allowance", 3, 5, .2),
        ("depleted_cube_5V_stress", 2, 5, .3),
        ("depleted_digital_stress", 2, 3.3, .5),
        ("not_supported_2A_5V_from_2V", 2, 5, 2),
    ]:
        duty = 1-vin/vout
        # 80% efficiency is a screening assumption. Lmin = -20% tolerance and
        # -10% current drop; Lmax = +20% tolerance. fmin = TI 2.1 MHz.
        peak = amps / (.8*(1-duty)) + vin*duty/(2*2.1e6*1.08e-6)
        rhpz = (1-duty)**2*vout/(2*math.pi*amps*1.8e-6)
        inductor_cases.append({"case": name, "VIN_V": vin, "VOUT_V": vout,
                               "IOUT_A": amps, "estimated_peak_A": peak,
                               "Isat_required_with_TI_20_percent_margin_A": 1.2*peak,
                               "below_4p1A_10_percent_drop_rating": 1.2*peak < 4.1,
                               "RHP_zero_Hz": rhpz,
                               "above_TI_400kHz_recommendation": rhpz > 400e3})
    result = {
        "status": "COMPONENT_SELECTION_SCREEN_COMPLETE_BENCH_VALIDATION_PENDING",
        "scope": "Near-converter capacitor banks and selected inductor under explicit cases. Typical models and arithmetic, not hardware qualification or all BOM electrical approval.",
        "limits": ["Temperature samples -55,25,85 C do not prove every intervening temperature.",
                   "20% reserve is an engineering allowance; no guaranteed age or model-error bound is claimed.",
                   "Input screen is up to 5.4 V at protected VIN; cold start requires at least 3 V there.",
                   "Real low-battery stability, load steps, PFM ripple and temperatures require first-board tests.",
                   "The 4.1 A inductor rating is at 25 C. It is not a hot/short-circuit guarantee.",
                   "Regulator current limit is average input current, not an absolute peak clamp.",
                   "Combined battery/holder/fuse load and audio limits remain a separate system review."],
        "manufacturer_svg_crosscheck": ui_checks,
        "rail_static_bounds": rails,
        "capacitor_banks": banks,
        "inductor": {"mpn": "XFL4020-152MEC", "inductance_nominal_uH": 1.5,
                     "Isat_10_20_30_percent_drop_A_at_25C": [4.1, 4.4, 4.6],
                     "Irms_20_40C_rise_A": [6.7, 9.1], "DCR_max_mOhm_at_25C": 15.8,
                     "cases": inductor_cases},
        "input_sha256": hashes,
    }
    (HERE / "power-component-audit.json").write_text(json.dumps(result, indent=2)+"\n")
    for bank in banks:
        print(bank["board"], bank["converter"], bank["role"],
              round(bank["screen_total_uF"], 3), "uF; minimum", bank["TI_minimum_uF"])


if __name__ == "__main__":
    main()
