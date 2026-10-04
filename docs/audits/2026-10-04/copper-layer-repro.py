"""Audit reproducer: a bottom track must not connect a top-only SMD pad.

Run with KiCad's Python from any directory. Exit 1 demonstrates the finding;
exit 0 means the checker rejects this fixture. No design file is modified.
"""
import json
from pathlib import Path
import sys

import pcbnew as p

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/ci"))
from check_copper_connectivity import pad_has_copper

board = p.BOARD()
net = p.NETINFO_ITEM(board, "AUDIT_TEST")
board.Add(net)
footprint = p.FOOTPRINT(board)
footprint.SetReference("U_AUDIT")
board.Add(footprint)
pad = p.PAD(footprint)
pad.SetNumber("1")
pad.SetAttribute(p.PAD_ATTRIB_SMD)
layers = p.LSET()
layers.AddLayer(p.F_Cu)
pad.SetLayerSet(layers)
pad.SetSize(p.VECTOR2I(p.FromMM(1), p.FromMM(1)))
pad.SetPosition(p.VECTOR2I(0, 0))
pad.SetNet(net)
footprint.Add(pad)
track = p.PCB_TRACK(board)
track.SetLayer(p.B_Cu)
track.SetStart(p.VECTOR2I(0, 0))
track.SetEnd(p.VECTOR2I(p.FromMM(2), 0))
track.SetWidth(p.FromMM(0.25))
track.SetNet(net)
board.Add(track)
observed = pad_has_copper(board, pad)
print(json.dumps({
    "fixture": "F.Cu-only SMD pad, B.Cu same-net track at same XY, no via",
    "expected": False,
    "observed": observed,
    "false_positive_reproduced": observed is True,
}, indent=2))
raise SystemExit(1 if observed else 0)
