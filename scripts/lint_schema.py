#!/usr/bin/env python3
"""Deterministic lint of one paper folder against the SCHEMA.md contract.

Usage: scripts/lint_schema.py papers/<id>

Identity checks always run; partition mechanics run once the schema
carries extraction content (md_sha256 / blocks / sections). Judgment
(coverage, fidelity, truth correctness) is verify-schema's job, not lint.
"""
import hashlib
import pathlib
import re
import sys
import tomllib

STATUSES = ("candidate", "rendered", "schema-drafted", "schema-verified")
SECTIONS = ("problem", "method", "method_params", "software",
            "software_params", "anchors", "truth")
TIERS = ("light", "medium")
LITERAL_RE = re.compile(r"\bLiteral\s+\S+:(\d+)(?:-(\d+))?")

paper_dir = pathlib.Path(sys.argv[1])
errors = []


def err(msg):
    errors.append(msg)


schema = tomllib.loads((paper_dir / "schema.toml").read_text())
paper = schema["paper"]

# --- identity ---
if paper["id"] != paper_dir.name:
    err(f"id {paper['id']!r} != folder {paper_dir.name!r}")
if paper["status"] not in STATUSES:
    err(f"status {paper['status']!r} not on ladder {STATUSES}")
mds = sorted(paper_dir.glob(f"{paper['id']}_*.md"))
if paper["status"] != "candidate" and len(mds) != 1:
    err(f"{len(mds)} rendered md files, want exactly 1")

extracted = "md_sha256" in paper or "blocks" in schema or any(s in schema for s in SECTIONS)
if paper["status"] in ("schema-drafted", "schema-verified") and not extracted:
    err(f"status {paper['status']} but no extraction content")

if extracted and mds:
    md_text = mds[0].read_text()
    md_lines = md_text.split("\n")
    n_lines = len(md_lines)

    # --- source pin ---
    digest = hashlib.sha256(md_text.encode()).hexdigest()
    if paper.get("md_sha256") != digest:
        err(f"md_sha256 mismatch: schema {paper.get('md_sha256')!r} != file {digest[:12]}…")

    # --- blocks: sections known, ranges valid + disjoint at (line, char)
    # granularity, text verbatim; span blocks carry `chars` on one line ---
    claimed = []  # (line, c_lo, c_hi, tag) — whole-line blocks claim full lines
    for i, b in enumerate(schema.get("blocks", [])):
        tag = f"blocks[{i}]"
        bad = set(b["sections"]) - set(SECTIONS)
        if bad or not b["sections"]:
            err(f"{tag}: bad sections {sorted(bad) or '[]'}")
        m = re.fullmatch(r"(\d+)-(\d+)", b["lines"]) or re.fullmatch(r"(\d+)", b["lines"])
        if not m:
            err(f"{tag}: malformed lines {b['lines']!r}")
            continue
        lo, hi = int(m.group(1)), int(m.group(m.lastindex))
        if not (1 <= lo <= hi <= n_lines):
            err(f"{tag}: range {lo}-{hi} outside file (1-{n_lines})")
            continue
        if "chars" in b:
            cm = re.fullmatch(r"(\d+)-(\d+)", b["chars"]) or re.fullmatch(r"(\d+)", b["chars"])
            if lo != hi or not cm:
                err(f"{tag}: chars requires a single line and 'c0-c1' form")
                continue
            c_lo, c_hi = int(cm.group(1)), int(cm.group(cm.lastindex))
            line_text = md_lines[lo - 1]
            if not (1 <= c_lo <= c_hi <= len(line_text)):
                err(f"{tag}: chars {c_lo}-{c_hi} outside line {lo} (1-{len(line_text)})")
                continue
            if b["text"] != line_text[c_lo - 1:c_hi]:
                err(f"{tag}: text is not verbatim line {lo} chars {c_lo}-{c_hi}")
            claimed.append((lo, c_lo, c_hi, tag))
        else:
            if b["text"] != "\n".join(md_lines[lo - 1:hi]):
                err(f"{tag}: text is not verbatim lines {lo}-{hi}")
            for ln in range(lo, hi + 1):
                claimed.append((ln, 1, max(1, len(md_lines[ln - 1])), tag))
    claimed.sort()
    for (ln_a, _, hi_a, tag_a), (ln_b, lo_b, _, tag_b) in zip(claimed, claimed[1:]):
        if ln_a == ln_b and lo_b <= hi_a and tag_a != tag_b:
            err(f"{tag_a} and {tag_b} overlap on line {ln_a}")

    # --- sections present; targets and truth well-formed ---
    for s in SECTIONS:
        if s not in schema:
            err(f"missing section [{s}]")
    targets = schema.get("problem", {}).get("targets", [])
    if not targets:
        err("no targets in [problem]")
    panels = [t.get("panel") for t in targets]
    if len(set(panels)) != len(panels) or None in panels:
        err(f"target panels not unique/present: {panels}")
    for t in targets:
        if t.get("tier") not in TIERS:
            err(f"target {t.get('panel')}: tier {t.get('tier')!r} not in {TIERS}")
    for panel in panels:
        entry = schema.get("truth", {}).get(panel)
        if entry is None:
            err(f"target {panel}: no [truth.{panel}] entry")
            continue
        has_value = "value" in entry or (paper_dir / f"truth_{panel}.csv").exists()
        if not has_value:
            err(f"truth.{panel}: no value and no truth_{panel}.csv")
        if "tolerance" not in entry:
            err(f"truth.{panel}: no tolerance")

    # --- Literal citations resolve ---
    def walk(node):
        if isinstance(node, dict):
            for v in node.values():
                yield from walk(v)
        elif isinstance(node, list):
            for v in node:
                yield from walk(v)
        elif isinstance(node, str):
            yield node

    for s in walk(schema):
        for m in LITERAL_RE.finditer(s):
            lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
            if not (1 <= lo <= hi <= n_lines):
                err(f"Literal citation {m.group(0)!r} outside file (1-{n_lines})")

if errors:
    print(f"FAIL {paper_dir.name}: {len(errors)} error(s)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print(f"OK {paper_dir.name} [{paper['status']}]")
