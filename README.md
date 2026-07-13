# quantum.eval

Evaluation dataset for the quantum many-body harness (`quantum.harness`):
physics papers decomposed into withholdable schema sections, consumed by
`agentic-eval` experiments that measure whether the harness skill set
improves paper reproduction.

The full design — the laws each component obeys, from decomposition to
run composition — lives in [DESIGN.md](DESIGN.md). The per-paper schema
contract lives in [SCHEMA.md](SCHEMA.md).

## Design principles

- **One truth per paper.** Each paper is one folder `papers/<arxiv_id>/`
  whose `schema.toml` (see `SCHEMA.md`) is the single truth, from
  candidate stub to fully extracted schema. No database: selection is a
  script over the TOML files.
- **Sections mirror the skill map.** A schema section exists iff there is a
  harness skill family to blind or ablate at it (problem ↔ model cards,
  method ↔ `method-*`, software ↔ `using-*`, truth ↔ verification).
- **Blindness is configuration.** A visibility level assigns each section a
  location — `workspace` (worker reads it), `dialogue` (sim-user reveals if
  asked), `judge` (never crosses). `[truth]` is always judge-only.
- **Grouping is by label, never by path.** `tier` (`light` = laptop,
  `medium` = single node/GPU), `family`, and `kind` are schema fields; a
  dataset is a named predicate over them (`datasets.toml`), resolved by
  `scripts/select.py` at a pinned commit — never copies.
- **Physics papers only.** Method-oriented papers count as fully numerical
  and carry `kind = "methods"`; default datasets exclude them.

## Layout

```text
SCHEMA.md            per-paper schema definition (shared by extractor and judge)
DESIGN.md            the laws each component obeys
visibility.toml      named section→location maps
datasets.toml        named dataset selections
scripts/select.py    dataset resolver (ids from a named or ad-hoc predicate)
papers/<arxiv_id>/   one paper, one folder:
  schema.toml          judgment layer (labels, sections, provenance; human-ratified)
  blocks.toml          partition layer (verbatim spans, machine-anchored)
  <arxiv_id>_<slug>.md rendered paper (arXiv version; frozen once extracted)
  .raw/ .figures/      local-only fetch artifacts (gitignored)
skills/download-ref/ vendored render workflow (bundled scripts, per paper)
search-notes/        preserved searcher intelligence from the collection sweeps
```

## Lifecycle

1. **Candidate** (now): metadata-only TOML from searcher sweeps
   (PR-series 2024–2026, non-experimental, theory + numerics, physics kind).
2. **Rendered**: paper fetched and rendered via the vendored
   `skills/download-ref` scripts (`ref.bib` as bib source of truth;
   `.raw/`/`.figures/` gitignored).
3. **Schema-drafted**: `paper-to-schemas` extracts the schema sections
   (one paper per subagent), truth digitized, human-ratified.
4. **Schema-verified**: `verify-schema` (independent subagent per schema)
   re-reads the paper against the schema; deterministic lint for format.

`skills/paper-to-schemas` and `skills/verify-schema` are per-paper
procedures (one subagent per paper invokes the skill; orchestration is
plain main-agent work); `scripts/lint_schema.py` is the deterministic
partition check both rely on. Judge criteria land with the eval pack.
