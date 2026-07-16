#!/usr/bin/env python3
"""Verifier for benchmarks/light: compare report.json against ground_truth.json.

Usage: verifier.py <instance_dir> <report.json>

Every target in the instance's ground_truth.json must be present in the
report and match within its tolerance (element-wise for list values).
Prints one PASS/FAIL line per target; exit 0 iff all pass.
"""
import json
import pathlib
import sys

instance = pathlib.Path(sys.argv[1])
report = json.loads(pathlib.Path(sys.argv[2]).read_text())
ground_truth = json.loads((instance / "ground_truth.json").read_text())


def close(got, want, tol):
    if isinstance(want, list):
        return (isinstance(got, list) and len(got) == len(want)
                and all(close(g, w, tol) for g, w in zip(got, want)))
    return (isinstance(got, (int, float)) and not isinstance(got, bool)
            and abs(got - want) <= tol)


ok = True
for target, spec in ground_truth.items():
    if target == "canary":
        continue
    good = close(report.get(target), spec["value"], spec["tol"])
    print(f"{'PASS' if good else 'FAIL'} {target}: "
          f"got {report.get(target)!r}, want {spec['value']!r} ± {spec['tol']}")
    ok &= good
sys.exit(0 if ok else 1)
