---
name: verify-schema
description: Use to independently verify one drafted schema against its paper — "verify 2311.07683", "check the schemas". Per-schema procedure, designed to run inside one fresh subagent per schema (never the extractor's context); a main agent loops it over a dataset.
argument-hint: <arxiv_id>
---

# verify-schema — one schema → findings

Independent re-read of one paper against its drafted `schema.toml`
(extractor–verifier separation, `DESIGN.md` §8). The unit of work is ONE
schema; run many by dispatching one fresh subagent per schema, pointed at
this file + `SCHEMA.md` + the paper folder, with no extractor context.

## Inputs

- `papers/<id>/` with `schema.toml` at status `schema-drafted`,
  `blocks.toml` (anchored partition layer), the rendered md, and any
  `truth_*.csv`.

## Procedure

1. **Mechanical lint first**: `python3 scripts/lint_schema.py papers/<id>`.
   A lint failure is already a finding; still continue to the judgment
   checks.
2. **Partition audit — both directions.** The block set must equal the
   set of revealing spans, tag for tag:
   - *Under-blocked (leak)*: derive the maximally blinded view (mask
     every span, delete every whole-line block) and read what remains as
     an adversary — any surviving passage that still reveals a section's
     content is a finding with its line range and the section revealed.
   - *Over-blocked (starvation)*: every block, and every section tag on
     it, must be justified by the span's own text; a block (or tag) whose
     span reveals none of what it claims removes content from the blinded
     view without cause — a finding citing the unjustified tag.
3. **Section fidelity.** For each block and structured entry, re-read the
   cited passage fresh: is the content in the right section(s), per the
   `SCHEMA.md` definitions? Is every `Literal` citation actually literal?
   Is every `Inferred` basis sound?
4. **Truth audit.** Re-derive each `[truth]` value from the paper
   independently (table/text, linked repository, or the figure image).
   Flag value or tolerance disagreements; flag targets whose truth the
   paper does not actually state at that instance.
5. **Identity check.** Confirm venue/DOI/`arxiv_version` in `[paper]`
   against the fetched metadata and the paper itself (this closes the
   papers whose DOI was missing at render time).

## Output

Findings only — this skill NEVER edits the schema. Each finding:
`{severity: blocker|minor, where: <section or lines>, what, evidence}`,
in the subagent's final message. Empty findings = pass.

- Pass → the dispatching agent flips status to `schema-verified`.
- Blockers → status stays; fixes go through `paper-to-schemas` (or a
  human), then re-verify with a fresh subagent.

## Rules

- Judgment findings are free-form and evidence-cited; no fixed verdict
  vocabulary (taxonomy is discovered later by clustering, `DESIGN.md` §7).
- Verification is per-schema and paper-agnostic: no per-family checklists;
  if a check only makes sense for one paper, it does not belong here.
