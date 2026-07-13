#!/usr/bin/env python3
"""Anchor quoted blocks: agents quote, scripts count.

Usage: scripts/anchor_blocks.py papers/<id>

Reads papers/<id>/blocks.toml, resolves every single-line quoted span to
1-indexed char offsets against the rendered md, and rewrites the file in
canonical form (sorted by position, one shape). Authoring form:

    [[blocks]]
    sections = ["method"]
    lines = "541"          # one line for spans; "A-B" for whole-line blocks
    text = "DMRG"          # verbatim substring (span) or the full lines
    nth = 2                # only when the substring repeats on that line

Never hand-count offsets: quote, run this, then lint. Whole-line blocks
(text equals the full line range) and already-anchored blocks pass
through; ambiguity (0 or several occurrences without `nth`) is an error.
"""
import json
import pathlib
import re
import sys
import tomllib

paper_dir = pathlib.Path(sys.argv[1])
md = next(paper_dir.glob(f"{paper_dir.name}_*.md"))
md_lines = md.read_text().split("\n")
blocks_path = paper_dir / "blocks.toml"
blocks = tomllib.loads(blocks_path.read_text()).get("blocks", [])

errors, out, n_anchored = [], [], 0
for i, b in enumerate(blocks):
    tag = f"blocks[{i}] (lines {b['lines']})"
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", b["lines"])
    if not m:
        errors.append(f"{tag}: malformed lines")
        continue
    lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
    entry = {"sections": b["sections"], "lines": b["lines"], "text": b["text"]}
    if "chars" in b:
        entry["chars"] = b["chars"]          # already anchored; lint verifies
    elif b["text"] == "\n".join(md_lines[lo - 1:hi]):
        pass                                 # whole-line form
    elif lo != hi:
        errors.append(f"{tag}: multi-line text must equal the full lines — "
                      "quote whole lines, or one line's substring")
        continue
    else:
        line = md_lines[lo - 1]
        hits = [mm.start() for mm in re.finditer(re.escape(b["text"]), line)]
        nth = b.get("nth", 1 if len(hits) == 1 else None)
        if not hits:
            errors.append(f"{tag}: quote not found in line {lo}")
            continue
        if nth is None or not (1 <= nth <= len(hits)):
            errors.append(f"{tag}: {len(hits)} occurrences on line {lo} — "
                          "add nth or lengthen the quote")
            continue
        c0 = hits[nth - 1] + 1
        entry["chars"] = f"{c0}-{c0 + len(b['text']) - 1}"
        n_anchored += 1
    out.append(entry)

if errors:
    print(f"FAIL {paper_dir.name}: {len(errors)} unresolved block(s)")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)


def start(e):
    lo = int(re.match(r"\d+", e["lines"]).group(0))
    c = int(e["chars"].split("-")[0]) if "chars" in e else 0
    return (lo, c)


out.sort(key=start)
body = "\n\n".join(
    "[[blocks]]\n"
    f"sections = {json.dumps(e['sections'], ensure_ascii=False)}\n"
    f'lines = "{e["lines"]}"\n'
    + (f'chars = "{e["chars"]}"\n' if "chars" in e else "")
    + f"text = {json.dumps(e['text'], ensure_ascii=False)}"
    for e in out)
blocks_path.write_text(
    f"# Partition layer for papers/{paper_dir.name} — canonical, written by\n"
    "# scripts/anchor_blocks.py. Author blocks as quotes (no chars), then\n"
    "# re-run the anchor; never hand-edit offsets.\n\n" + body + "\n")
print(f"OK {paper_dir.name}: {len(out)} blocks "
      f"({n_anchored} newly anchored) -> {blocks_path}")
