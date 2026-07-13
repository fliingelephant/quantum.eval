# SCHEMA — per-paper `papers/<arxiv_id>/`

One folder per paper is the single source of truth, in two layers plus
data: `schema.toml` (judgment layer — sections, human-ratified),
`blocks.toml` (partition layer — machine-anchored spans), and optional
`truth_<panel>.csv`. `paper_id` = arXiv id (what `download-ref` uses as
canonical id). The extractor (`paper-to-schemas`) and the judge share
this definition and nothing else.

Status ladder: `candidate → rendered → schema-drafted → schema-verified`.
The rendered md is **frozen once extraction content exists** — every
offset points into it (`md_sha256` detects drift); re-render ⇒ re-extract.

## Sections

A section exists iff a harness skill family can be blinded or ablated at it.

### `[paper]` — identity and selection fields (candidate stage)

| field | meaning |
|---|---|
| `id` | arXiv id, the primary key |
| `title`, `authors`, `journal` | citation; journal ref re-verified at render |
| `family` | method family: `mps`, `qmc`, `vmc`, `peps`, `ed`, `thermal-tn`, … |
| `tier` | compute tier of the headline: `light` (laptop) / `medium` (node or one GPU) |
| `kind` | `physics` / `methods` — methods papers are excluded from datasets by default |
| `status` | lifecycle stage (above) |
| `doi`, `arxiv_version` | recorded at render time |

### `[candidate_notes]` — searcher-era free text

`model`, `headline`, `compute`, `verification`. Superseded by the extracted
sections below; kept for provenance.

### Extraction sections (filled at schema-drafted stage — NOT yet)

All method/software/params sections refer to the paper's **numerical**
work — the decision chain the harness skills own. Analytic theory is
content, not a junction (closed-form check values → `[anchors]`).

| section | content | harness skills under test |
|---|---|---|
| `[problem]` | model (card name or explicit Hamiltonian), convention (sign/normalization, pinned), instance (dimension, lattice, BC, couplings, sector/filling, sizes), `targets` = every quantity the paper computes numerically (observable, ensemble, axes, panel id, **per-target tier**) | model/physics cards, confirm-the-setup |
| `[method]` | the paper's **numerical** route — method family AND algorithm within it (the `method-*` cards' *select method* step: e.g. mps → DMRG vs VUMPS) — plus the valid-alternative set: routes that CAN produce the targets, at both family and algorithm level | `method-*` routing |
| `[method_params]` | numerical convergence knobs and criteria — the method card's layer; the quantities survive a software swap even when their spellings differ (χ/maxdim, truncation cutoff, sizes list, time grid, statistics, extrapolation protocol) | `method-*` details, parameter-scan, scaling-fit |
| `[software]` | the paper's numerical software/code if stated, plus the valid tool set (the `method-*` cards' *select software* step → `using-*` targets) | `using-*` |
| `[software_params]` | implementation setup with no method-level meaning — does not survive a software swap (eigensolver choice and its tolerances, e.g. Krylov atol; noise/perturbation tricks; threading; API-specific toggles) | `using-*` |
| `[anchors]` | analytic values usable as cross-checks (exact limits, closed forms) | verification |
| `[truth]` | ground truth: the paper's numerical results as digitized figure/table values + tolerances, keyed by panel id; long curves as csv beside the TOML. The grader ALWAYS consumes this table; a map's `truth` location only decides whether the paper's stated results stay readable to the worker. | outcome grading (`check_truth.py`) |

### `blocks.toml` — verbatim moves (the partition layer)

Every paper passage that reveals a section's content becomes a block —
the same fact usually appears in several places, each its own block.
Blocks live in their own file so the machine can own its format wholesale.

**Agents quote, scripts count.** Author blocks WITHOUT offsets — never
hand-count characters:

```toml
[[blocks]]                   # sub-line span — THE NORM
sections = ["method"]        # every section the span reveals
lines = "541"                # one line, 1-indexed
text = "DMRG"                # verbatim substring
# nth = 2                    # only when the substring repeats on the line

[[blocks]]                   # whole-line form — only when the entire unit reveals
sections = ["method", "software_params"]
lines = "412-431"            # 1-indexed inclusive line range
text = """…the full lines, verbatim…"""
```

then `scripts/anchor_blocks.py papers/<id>` resolves each quote to
1-indexed `chars = "c0-c1"` offsets and canonicalizes the file (0 or
several occurrences without `nth` is an error), and
`scripts/lint_schema.py papers/<id>` verifies the anchored mechanics.
Pipeline: **author quotes → anchor → lint**. `[paper].md_sha256` in
`schema.toml` pins the md all offsets point into.

Blocks are visibility-agnostic (captured uniformly for all sections);
derivation hides a block iff ANY of its sections is hidden: a span is
replaced by the fixed marker `▓` (fixed length — a hidden name must not
leak its length), a whole-line block's lines are deleted. **Fine-grained
spans are the norm**: block the minimal revealing content — in
result-stating units (title, abstract sentences, captions) only the
outcome (values, exponents, phase identifications) hides and the setup
half (model, instance, what was computed) stays readable. Whole-line
blocks are for units that reveal in full (a "DMRG numerics" section
header, an equation image defining the method). Ranges are pairwise
disjoint at (line, char) granularity; text is byte-verbatim. Coverage
(no revealing passage missed) is `verify-schema`'s judgment.

**Blocking is surgical and numerical-scoped.** What gets blocked is what
the sections withhold: the numerical route (method family, convergence
knobs, software, implementation setup) and truth values — the minimal
spans that reveal them. A paper's analytical apparatus (symmetry
analysis, effective field theory, perturbative arguments, dualities) is
not `[method]`: closed-form values/relations usable as cross-checks go
to `[anchors]`; the rest is problem-side physics context and stays
unblocked. That a paper "performed numerics" is not withholdable — every
pool paper did. The derived blinded paper must remain a coherent problem
statement; over-blocking is starvation (`verify-schema` audits both
directions).

## Rules

- **Provenance discipline**: every extracted entry cites the rendered
  paper (`file:line` — Literal) or is marked Inferred. Untagged numbers are
  not trustworthy.
- **Uncertainty rule**: torn between sections for a block or entry — tag
  the union (fail-closed hides more) AND flag it for the human in the
  digest. No agent improvises a tie-break.
- **Method correctness is set-membership**: `wrong` means the route cannot
  produce the target; "same as the paper" is a recorded bit, never a grade.
- **Verdict taxonomy is discovered, not designed**: judges emit free-form,
  evidence-cited findings anchored to sections; categories get frozen only
  after clustering across runs.
- **Partial replication is the norm**: a task selects a *subset* of
  `targets` (e.g. only the laptop-feasible panels/sizes of a heavier paper —
  the Turner pattern). Each target carries its own tier; the paper-level
  `tier` is shorthand for the headline target's tier, not a gate. A target
  is gradeable only if the paper states its value at that instance — truth
  is always paper-stated, never a reduced-size variant the paper doesn't
  report. Task success = all *selected* targets within tolerance.
- **Intent is not a section**: personas and target selections live with the
  eval pack tasks (`intent.md`), one paper minting many tasks.
