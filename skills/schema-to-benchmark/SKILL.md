---
name: schema-to-benchmark
description: Use to compose benchmark instances from one labeled paper per a benchmark description — "compose 2410.13354 into benchmarks/light". Per-paper procedure, designed to run inside one subagent per paper; a main agent resolves the spec's selection into a paper list and loops.
argument-hint: <benchmark_spec> <arxiv_id>
---

# schema-to-benchmark — one labeled paper → benchmark instances

Composes instances for the benchmark described by `<benchmark_spec>`
(e.g. `benchmarks/light/SPEC.md`) from the label layers of
`papers/<id>/`. The labels are the map, the paper is the source, the
composer is a problem-setter: **select by schema fields, route by
provenance lines, fence by blocks, state the problem, then answer it.** Safety lives in the
forward pass — read the fence before writing — not in an audit pass.

**Read the spec in full first, and follow it exactly.** The spec owns
everything set-specific: selection predicate, instance format and file
names, worker-input definition, report contract, grading, envelope
defaults, validation rule. This skill owns only the paper-agnostic,
set-agnostic process; where the two seem to conflict, the spec wins.

## Inputs

- The benchmark spec: selection predicate, instance format, worker
  input, report contract, grading, envelope defaults, validation rule.
- `papers/<id>/`: `schema.toml` (judgment layer), `blocks.toml`
  (partition layer), the rendered md and `.figures/`.

## Procedure

1. **Select and group.** Apply the spec's selection predicate to
   `[problem].targets` and `[truth]`. No qualifying target → report
   "no instances" and stop. Grouping: ONE instance per paper, holding
   all qualifying targets. Split only when two targets live on
   different Hamiltonians — never for a different observable, size
   window, sector, or estimated budget.
2. **Route.** For each selected target, follow its provenance lines
   (and the `[problem]` field provenances) into the rendered md; read
   those passages and the equation images they contain. That is the
   reading list — not the whole paper.
3. **Read the fence, then write.** Open `blocks.toml` and read every
   span tagged `method*`, `software*`, or `truth`. Those passages must
   not be echoed in the worker-facing text: no method or algorithm
   names, no convergence knobs, no software, and no truth values **or
   findings** — numbers, exponents, phase or universality-class
   identifications, which side of a transition is which.
4. **Author the worker input fresh** (the spec names the file, e.g.
   `instruction.md`). Model, conventions, and instance from
   `[problem]` — summarized, clean, self-contained prose, never a
   mechanical render of label fields. Label fields and their wording
   are routing pointers only: every physical statement is authored
   from the provenance passages themselves. Then precise target
   definitions and the report contract from the spec. Canary line on
   top. No paper identity anywhere in the worker input. Write as a
   problem-setter, not a redactor: the finished statement must admit
   exactly one correct answer — every convention the number depends on
   is stated, or provably doesn't matter — and nothing worker-visible
   (wording, key names, grids, examples) narrows the answer without
   doing the physics.
5. **Derive the machine side** per the spec's instance format: the
   answer key from `[truth]` (value, tolerance, provenance per
   target — e.g. `ground_truth.json`) and the envelope from the spec's
   defaults with identity fields from `[paper]` (e.g. `task.toml`,
   blocked domains from the paper's hosts). The key must answer the
   written problem, not merely quote the paper: wherever the statement
   itself implies a value (a limit, an exactly known point, a
   symmetry), substitute and confirm the key agrees. Tolerance accepts
   any correct calculation — including the reference value's own
   uncertainty — and rejects a natural wrong one; one line of
   justification per value in the key's provenance.
6. **Validate before shipping — reading and small arithmetic, never
   running the physics.**
   Cross-check each definition, value, and tolerance in the instance
   against its provenance passage — equations symbol by symbol (each
   operator, index, sign); a mistranscribed definition is a wrong
   instance even when every number matches. A target whose statement cannot be
   pinned from the paper's text, or cannot be defined without leaking
   the fence, is dropped and said so.
7. **Digest** (the subagent's final message): instances written,
   targets included/dropped and why, what was validated and how.

## Rules

- Never write an equation or value from memory — read it from the
  source (the provenance passage or its equation image); if the source
  cannot be read, drop the target and say so.
- Safety is in the forward pass: fence read → author. No post-hoc
  audit pass, no second agent.
- Nothing paper-specific lives in this skill or the spec; per-paper
  judgment lives in the instance files it writes.
- The worker input is exactly what the spec defines — nothing else
  reaches the worker; paper identity stays harness-side.
