#!/usr/bin/env python3
"""Read public SimSurfing characteristics for the proposed Murata capacitors.

Uses the same unauthenticated read endpoint and parameter schema as Murata's
public SimSurfing graph UI. No account, credentials, uploads or purchasing.
The returned curves are typical manufacturer models, not guaranteed limits.
"""
import argparse
import concurrent.futures
import csv
import datetime
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

BASE = Path(__file__).resolve().parents[1]
ENDPOINT = "https://ds.murata.com/simserve/characteristics"


def query(mpn, ac, temperature):
    # SimSurfing omits the final tape/reel code from the electrical part number.
    request = {
        "partnumber": mpn[:-1],
        "chara_type": "c_dcbias_capacitance",
        "parameter": {"tc": str(temperature), "ac": str(ac)},
        "WorkInfo": {},
    }
    params = {
        "callback": "nothing", "ReqType": "Characteristics",
        "ReqChara": json.dumps([request]), "CallBack": "mycallback",
        "WorkInfo": "prototype-order-review", "ModeType": "",
    }
    url = ENDPOINT + "?" + urllib.parse.urlencode(params)
    raw = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
        timeout=30,
    ).read()
    response = json.loads(raw)
    curves = response["JsonCharaData"]
    assert len(curves) == 1 and curves[0]["partnumber"] == mpn[:-1]
    assert curves[0]["chara_type"] == request["chara_type"]
    errors = []
    for curve in curves[0]["charadata"]:
        if curve.get("error"):
            errors.append(curve["error"])
            continue
        assert float(curve["tc"]) == temperature
        assert float(curve["ac"]) == ac
        assert (curve["x_unit"], curve["y_unit"], curve["y_subunit"]) == ("V", "F", "u")
        assert len(curve["data"]) >= 2
    return {"mpn": mpn, "request": request,
            "status": "MODEL_UNAVAILABLE" if errors else "CURVE_RETRIEVED",
            "errors": errors,
            "response_sha256": hashlib.sha256(raw).hexdigest(),
            "response": response}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Refusing to overwrite a dated manufacturer capture")
    source = BASE / "sourcing.csv"
    rows = list(csv.DictReader(source.open()))
    mpns = sorted({r["proposed_mpn"] for r in rows
                   if r["reference"].startswith("C") and r["proposed_mpn"].startswith(("GRM", "GRT"))})
    cases = [(mpn, .01, t) for mpn in mpns for t in (-55, 25, 85)]
    # Reference curve also inspected in the rendered manufacturer UI.
    cases.append(("GRM31CR61C226KE15L", .5, 25))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda case: query(*case), cases))
    out = {
        "captured_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_ui": "https://ds.murata.com/simsurfing/mlcc.html?lcid=en-us",
        "source_endpoint": ENDPOINT,
        "ui_dataset_date_observed": "2026-09-02",
        "scope": "Typical capacitance models at 10 mVrms and -55/25/85 C; not guaranteed production limits or physical board tests.",
        "sourcing_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "curves": results,
    }
    args.output.write_text(json.dumps(out, separators=(",", ":")) + "\n")
    print(f"Saved {len(results)} curves for {len(mpns)} proposed capacitor MPNs to {args.output}")


if __name__ == "__main__":
    main()
