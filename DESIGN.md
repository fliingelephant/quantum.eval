# DESIGN — paper-reproduction evaluation dataset

The framework is generic: it evaluates whether a **skill set** improves an
agent's ability to reproduce published results, for any system under test
(SUT) whose workflow decomposes into decision junctions. The quantum
instance parameterizes it (harness = `quantum.harness`, engine =
`agentic-eval`); nothing below depends on the domain except where marked
*instance*.

Every component owns exactly one law. If a proposed feature does not
follow from one of these laws, it does not enter the design.

## 1. The claim, and what it forces

The claim under test: *the skill set causes better reproduction*.
Causation needs attribution; attribution forces three structures:

- **Decomposition** — the paper must be split into parts so failures
  localize ("wrong method" vs "wrong convention" vs "wrong knobs").
- **Isolation** — parts must be withholdable, so a junction is exercised
  rather than read off the page.
- **Ablation** — the skill claimed to own a junction must be removable,
  so its contribution is a measured delta, not a story.

Everything else in this document is machinery serving those three.

## 2. Decomposition law

> A schema section exists **iff** the SUT has a skill family that can be
> blinded or ablated at it.

The decomposition mirrors the SUT's decision chain, not the paper's
anatomy. *Instance*: `problem` ↔ model/knowledge cards, `method` ↔
`method-*` skills, `method_params` ↔ convergence-judgment skills,
`software`/`software_params` ↔ `using-*` skills, `anchors`/`truth` ↔
verification. Full section contract: `SCHEMA.md`.

Consequences:
- Paper anatomy (result DAGs, figure roles, compute cost) is *record-level
  detail inside sections*, never a new section.
- **Intent is not a section.** What a user wants (persona, target subset,
  budget) belongs to the eval task, not the paper. One paper mints many
  tasks.

## 3. One-truth law

> Each paper is exactly one folder `papers/<id>/` whose `schema.toml` is
> the single source of truth; every other representation is derived and
> disposable.

- `<id>` = arXiv id (the render pipeline's canonical id).
- No databases, no index files, no tier directories: **grouping is by
  label, never by path**. `tier`, `family`, `kind` are schema fields; a
  *dataset* is a named predicate over them (`datasets.toml`), resolved by
  script at a pinned commit. Copies are forbidden; the commit is the pin.
- `kind` law (*instance of the generic inclusion rule*): the pool holds
  **physics papers** — established methods answering a question about a
  model. A paper whose contribution is the method itself counts as fully
  numerical and is excluded from datasets by default (`kind = "methods"`).

## 4. Partition law (isolation mechanics)

> Extraction **moves** paper content into schema sections verbatim —
> never paraphrases — and records where it came from. Blinded documents
> are derived, never stored.

Each moved passage is a block: `{section, lines, verbatim text}`, plus a
pinned `md_sha256` of the rendered paper. Then:

- **Derivation is a pure function** `(paper.md, schema, visibility) →
  blinded.md`: delete the line ranges of every block whose section is not
  workspace-visible. No model in the loop.
- **Fail closed.** Any anchor/hash mismatch aborts derivation. A unit of
  text mixing sections goes whole to the *more restricted* section.
  Composition can re-add information; it can never un-leak it.
- **Auditable faithfulness.** verify checks: hash pinned, every block's
  text matches its lines verbatim, ranges disjoint. Paraphrase is banned
  twice over: it cannot be audited, and it would make the eval measure
  the extractor's rewording instead of the SUT.
- Figures split by nature: panel *semantics* (what is plotted) →
  `targets`; *values* (digitized) → `truth`; the image itself is a block.
  Captions and bibliography entries partition under the same rule (a
  citation used only inside moved text moves with it).
- The isolation bar is **no raw simple leaks** — not adversarial
  anti-memorization. Post-cutoff papers are the memorization control.

## 5. Visibility law

> A blindness level is one map: section → location ∈ {workspace,
> dialogue, judge}. `truth` is always judge.

- `workspace`: materialized where the worker can read it.
- `dialogue`: known to the simulated user; revealed only if asked — this
  is where elicitation quality becomes measurable.
- `judge`: never crosses the seam.

Named maps live in `visibility.toml`; any new kind or degree of blindness
— including a combination of existing ones — is a new named map, nothing
else. Visibility is a *value on an axis*, not an experiment: the engine's
law — vary exactly one axis (content / task / worker), freeze the rest,
N trials — composes conditions from (paper, visibility, intent,
SUT-content, model).

**Coherence constraint.** A map must be monotone along the decision
chain: a section may not be more visible than the choice it presupposes
(`method_params` ≤ `method`; `software_params` ≤ `software` ≤ `method`,
with workspace > dialogue > judge). Revealing the knobs while hiding the
method would leak the method through its knobs; such maps are rejected
by lint at materialization, not left to judgment.

## 6. Target law

> `targets` lists every quantity the paper computes; each carries its own
> compute tier; a task selects a subset; truth is always paper-stated.

Partial replication is the norm (reproduce the laptop-feasible panels of
a heavier paper). A reduced instance the paper never reports is not
gradeable and cannot be a target. Paper-level `tier` is shorthand for the
headline target's tier — a browsing label, not a gate.

## 7. Grading law

> Deterministic checks are code; judgment is an agent; taxonomy is
> discovered, not designed.

- **Outcome bit** (code, `check_truth.py`): selected targets within
  `truth` tolerances, computed from run artifacts.
- **Findings** (judge subagent, one per run — a run is one narrative):
  free-form, evidence-cited (journal/run record), anchored to schema
  sections. No fixed verdict vocabulary; after enough runs, cluster
  findings and freeze the empirically stable categories — those become
  the failure-reason breakdown.
- **Method correctness is set-membership**: `wrong` = the route cannot
  produce the target. "Same as the paper" is a recorded bit, never a
  grade; several routes may be valid simultaneously (method choice is
  often fuzzy, and obviousness is capability-relative — never pre-label
  papers as instruments; where skill deltas concentrate is a *finding*,
  read per-paper from the results).

## 8. Pipeline law

> Deterministic steps run via committed scripts; judgment steps are
> skills run by subagents; each paper advances a status ladder.

`candidate → rendered → schema-drafted → schema-verified`

- **candidate**: metadata-only `schema.toml` (searcher-verified citation).
- **rendered**: `skills/download-ref` (vendored; bundled scripts are
  mandatory — rate limits are retried, never worked around by
  substituting sources).
- **schema-drafted**: `paper-to-schemas` — one paper per subagent
  (extraction parallelizes along independence: papers are independent,
  layers within a paper are not), verbatim blocks + provenance, truth
  digitization human-ratified.
- **schema-verified**: `verify-schema` — an independent subagent re-reads
  the paper against the schema (extractor–verifier separation), plus the
  mechanical partition checks of §4. Format uniformity across papers is
  deterministic lint, not agent judgment.

The skills are deliverables of this repo, held to the same quality bar as
the dataset.

## 9. Run composition (how an evaluation consumes this repo)

For one trial of condition (paper, visibility, intent, content, model):

1. **Materialize**: worktree of the SUT + derived `blinded.md` planted as
   the user-provided file; SUT-internal copies of papers stripped;
   content-axis ablation applied if the condition says so.
2. **Secrets**: task `intent.md` (persona × target subset × budgets ×
   DONE) beside the dialogue-tier schema sections.
3. **Run**: the engine's seam (real AskUserQuestion crossings, turn
   gating, kill-safe record).
4. **Judge**: outcome bit vs `truth` (never left this repo); findings
   anchored to sections.
5. **Read out**: per-paper deltas across conditions; aggregate bar chart.

A baseline arm (everything visible, skills on) is just one condition —
if it fails, that shows up in the table like anything else.

## 10. Genericity

To retarget the framework: swap the SUT, rewrite the junction map (§2)
for its skill families, re-author truth checkers for its artifact types.
The laws (§1, §3–§9), the engine, and the file shapes do not change.
