# quantum.eval

Evaluation dataset for the quantum many-body harness (`quantum.harness`):
physics papers decomposed into withholdable schema sections, consumed by
`agentic-eval` experiments that measure whether the harness skill set
improves paper reproduction.

The full design — the laws each component obeys, from decomposition to
run composition — lives in [DESIGN.md](DESIGN.md). The per-paper schema
contract lives in [SCHEMA.md](SCHEMA.md).

## Design principles

- **One truth per paper.** Each paper is exactly one `<arxiv_id>.toml`
  (see `SCHEMA.md`), from candidate stub to fully extracted schema. No
  database: selection is a script over the TOML files.
- **Sections mirror the skill map.** A schema section exists iff there is a
  harness skill family to blind or ablate at it (problem ↔ model cards,
  method ↔ `method-*`, software ↔ `using-*`, truth ↔ verification).
- **Blindness is configuration.** A visibility level assigns each section a
  location — `workspace` (worker reads it), `dialogue` (sim-user reveals if
  asked), `judge` (never crosses). `[truth]` is always judge-only.
- **Datasets are named selections** over schema fields (`datasets.toml`),
  pinned by repo commit — never copies.
- **Physics papers only.** Method-oriented papers count as fully numerical
  and are quarantined in `candidates/methods-papers/`.

## Layout

```text
SCHEMA.md            per-paper schema definition (shared by extractor and judge)
visibility.toml      named section→location maps
datasets.toml        named dataset selections
candidates/
  light/             laptop-tier candidates   (CPU, ≤16 GB, minutes–hours)
  medium/            node/GPU-tier candidates (single node, hours–day)
  methods-papers/    quarantined method-oriented papers (kind = methods)
```

## Lifecycle

1. **Candidate** (now): metadata-only TOML from searcher sweeps
   (PR-series 2024–2026, non-experimental, theory + numerics, physics kind).
2. **Rendered**: paper fetched and rendered via the harness `download-ref`
   scripts (`ref.bib` as bib source of truth; `.raw/`/`.figures/` gitignored).
3. **Schema-drafted**: `paper-to-schemas` extracts the schema sections
   (one paper per subagent), truth digitized, human-ratified.
4. **Schema-verified**: `verify-schema` (independent subagent per schema)
   re-reads the paper against the schema; deterministic lint for format.

Skills (`paper-to-schemas`, `verify-schema`, judge criteria) are
deliverables of this repo and land in `skills/` at stage 3.
