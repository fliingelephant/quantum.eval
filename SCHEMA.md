# SCHEMA — per-paper `papers/<arxiv_id>/schema.toml`

One TOML file per paper is the single source of truth. `paper_id` = arXiv id
(what `download-ref` uses as canonical id for arXiv-sourced entries). The
extractor (`paper-to-schemas`) and the judge share this definition and
nothing else.

Status ladder: `candidate → rendered → schema-drafted → schema-verified`.

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
| `[method]` | the paper's **numerical** route — method family/algorithm in the harness `method-*` sense (ed, mps, qmc, vmc, peps, …) — plus the valid-alternative set: methods that CAN produce the targets | `method-*` routing |
| `[method_params]` | numerical convergence knobs — survive a software swap (χ, sizes list, time grid, statistics) | `method-*` details, parameter-scan, scaling-fit |
| `[software]` | the paper's numerical software/code if stated, plus valid tool set (maps to harness `using-*`) | `using-*` |
| `[software_params]` | numerical implementation knobs — do not survive a software swap | `using-*` |
| `[anchors]` | analytic values usable as cross-checks (exact limits, closed forms) | verification |
| `[truth]` | ground truth: the paper's numerical results as digitized figure/table values + tolerances, keyed by panel id; long curves as csv beside the TOML. **Always judge-only.** | outcome grading (`check_truth.py`) |

### `[[blocks]]` — verbatim moves (the partition layer)

Every paper passage that reveals a section's content becomes a block —
the same fact usually appears in several places, each its own block:

```toml
[paper]
md_sha256 = "…"              # pins the rendered md at extraction

[[blocks]]
sections = ["method", "software_params"]  # every section the span reveals
lines = "412-431"                         # 1-indexed inclusive, in the md
text = """…verbatim copy…"""
```

Blocks are visibility-agnostic (captured uniformly for all sections);
derivation deletes a block iff ANY of its sections is hidden. Ranges are
pairwise disjoint; text is byte-verbatim. `scripts/lint_schema.py`
enforces these mechanics; coverage (no revealing passage missed) is
`verify-schema`'s judgment.

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
