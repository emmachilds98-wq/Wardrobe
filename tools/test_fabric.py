"""Checks for the fibre-composition reader (python3 tools/test_fabric.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import sweep_filter as sf  # noqa: E402

CASES = [
    ("Composition: 100% Cotton. Machine wash", "100% cotton"),
    ("60% Cotton, 40% Polyester", "60% cotton, 40% polyester"),
    ("Shell: 100% nylon. Lining: 100% polyester", "100% nylon"),
    ("98% organic cotton 2% elastane", "98% organic cotton, 2% elastane"),
    ("95%cotton 5% Lycra", "95% cotton, 5% elastane"),
    ("50% off this week", ""),
    ("Main: 80% recycled polyester / 20% cotton; Trim: 100% polyester", "80% recycled polyester, 20% cotton"),
    ("100% Cotton twill with a relaxed fit", "100% cotton"),
    ("Made with 70% cotton", ""),
]

bad = [(t, want, sf.fabric_of(t)) for t, want in CASES if sf.fabric_of(t) != want]
for t, want, got in bad:
    print("FAIL", repr(t), "want", repr(want), "got", repr(got))
print("%d of %d fabric cases pass" % (len(CASES) - len(bad), len(CASES)))
sys.exit(1 if bad else 0)
