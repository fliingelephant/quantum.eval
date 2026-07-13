#!/usr/bin/env python3
"""Resolve a named dataset (datasets.toml predicate) over papers/*/schema.toml.

Usage:
    scripts/select.py <dataset>                 # ids, one per line
    scripts/select.py <dataset> --fields tier,family,title
    scripts/select.py --where "tier == 'light'" # ad-hoc predicate
    scripts/select.py --list                    # named datasets
"""
import argparse
import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent

parser = argparse.ArgumentParser()
parser.add_argument("dataset", nargs="?")
parser.add_argument("--where", help="ad-hoc predicate over [paper] fields")
parser.add_argument("--fields", help="comma-separated [paper] fields to print after the id")
parser.add_argument("--list", action="store_true", help="list named datasets")
args = parser.parse_args()

datasets = tomllib.loads((ROOT / "datasets.toml").read_text())
if args.list:
    for name, spec in datasets.items():
        print(f"{name}\t{spec['where']}")
    sys.exit(0)

where = args.where or datasets[args.dataset]["where"]
fields = args.fields.split(",") if args.fields else []

for schema in sorted(ROOT.glob("papers/*/schema.toml")):
    paper = tomllib.loads(schema.read_text())["paper"]
    if eval(where, {}, dict(paper)):
        print("\t".join([paper["id"], *(str(paper.get(f, "")) for f in fields)]))
