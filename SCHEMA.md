# SCHEMA — per-paper `<arxiv_id>.toml`

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

| section | content | harness skills under test |
|---|---|---|
| `[problem]` | model (card name or explicit Hamiltonian), convention (sign/normalization, pinned), instance (dimension, lattice, BC, couplings, sector/filling, sizes), `targets` = every quantity the paper computes (observable, ensemble, axes, panel id) | model/physics cards, confirm-the-setup |
| `[method]` | the paper's route, plus the valid-alternative set: methods that CAN produce the targets | `method-*` routing |
| `[method_params]` | physical convergence knobs — survive a software swap (χ, sizes list, time grid, statistics) | `method-*` details, parameter-scan, scaling-fit |
| `[software]` | paper's code if stated, plus valid tool set (maps to harness `using-*`) | `using-*` |
| `[software_params]` | implementation knobs — do not survive a software swap | `using-*` |
| `[anchors]` | analytic values usable as cross-checks (exact limits, closed forms) | verification |
| `[truth]` | ground truth: digitized figure/table values + tolerances, keyed by panel id; long curves as csv beside the TOML. **Always judge-only.** | outcome grading (`check_truth.py`) |

## Rules

- **Provenance discipline**: every extracted entry cites the rendered
  paper (`file:line` — Literal) or is marked Inferred. Untagged numbers are
  not trustworthy.
- **Method correctness is set-membership**: `wrong` means the route cannot
  produce the target; "same as the paper" is a recorded bit, never a grade.
- **Verdict taxonomy is discovered, not designed**: judges emit free-form,
  evidence-cited findings anchored to sections; categories get frozen only
  after clustering across runs.
- **Intent is not a section**: personas and target selections live with the
  eval pack tasks (`intent.md`), one paper minting many tasks.
