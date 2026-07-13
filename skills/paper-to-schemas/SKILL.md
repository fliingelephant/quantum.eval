---
name: paper-to-schemas
description: Use to extract one rendered paper into its schema.toml sections — "extract 2311.07683", "draft the schema for this paper". Per-paper procedure, designed to run inside one subagent per paper; a main agent loops it over a dataset.
---

# paper-to-schemas — one paper → one schema

Fills the extraction sections of `papers/<id>/schema.toml` from the
rendered paper, per the contract in `SCHEMA.md` (sections) and
`DESIGN.md` §4 (partition law). The unit of work is ONE paper; run many
papers by dispatching one subagent per paper, each pointed at this file +
`SCHEMA.md` + the paper folder, with no other context.

## Inputs

- `papers/<id>/` containing `schema.toml` (status `rendered`) and the
  rendered `<id>_<slug>.md`; figure images under `.figures/` (local-only).

## Procedure

1. **Pin the source.** Compute `md_sha256` of the rendered md and record
   it in `[paper]`. All line references below are 1-indexed lines of this
   exact file.
2. **Read the whole paper** (text and figure images). Identify, for each
   schema section, every passage that reveals it — the same fact usually
   appears in several places (abstract, intro, body, captions,
   bibliography); all of them count.
3. **Move content into blocks.** For each revealing passage add a block:

   ```toml
   [[blocks]]
   sections = ["method"]          # every section this span reveals
   lines = "412-431"              # 1-indexed inclusive range in the md
   text = """...verbatim copy..."""
   ```

   - Verbatim only — never paraphrase, never trim inside a line.
   - A span revealing several sections lists them all; derivation later
     deletes a block if ANY of its sections is hidden.
   - Ranges must be pairwise disjoint. Blocks are visibility-agnostic:
     capture for every section uniformly, including `[problem]`; which
     blocks get deleted is decided elsewhere, later.
   - A figure whose image reveals a section: block the image-link line(s)
     and its caption. A bibliography entry cited only inside blocked text
     is itself a block.
4. **Fill the structured sections** (`[problem]`, `[method]`,
   `[method_params]`, `[software]`, `[software_params]`, `[anchors]`,
   `[truth]`) as defined in `SCHEMA.md`. Every entry carries provenance:
   `Literal <md-file>:<lines>` or `Inferred <one-line basis>`. Cite the
   cleanest passage (a problem-only statement, not a mixed sentence);
   blocks cover all occurrences, fields cite one.
5. **Digitize truth.** Source order: stated table/text value (Literal) →
   paper-linked data repository → figure digitization (Inferred; tolerance
   must cover digitization uncertainty). Key by panel id; long curves go
   to `papers/<id>/truth_<panel>.csv` beside the TOML. Each target in
   `[problem].targets` carries its own compute tier. A quantity the paper
   never states at that instance is not a target.
6. **Self-lint**: `python3 scripts/lint_schema.py papers/<id>` must pass.
7. **Return a digest** (the subagent's final message): targets found
   (panel id, quantity, tier, truth source), block count per section,
   anything Inferred, anything ambiguous flagged for the human.

## Postconditions

- `schema.toml` gains `md_sha256`, `[[blocks]]`, and the seven sections;
  `[candidate_notes]` stays (provenance).
- Status flips to `schema-drafted` after the digest is surfaced to the
  human — who may review per paper, batch-approve, or waive review; the
  independent quality check is `verify-schema`, not this gate.

## Rules

- Extraction is a pure function of (rendered md, `SCHEMA.md`). No
  knowledge of visibility maps, eval tasks, or other papers may enter.
- Nothing paper-specific is special-cased; if the contract fails on a
  real paper, that is a `SCHEMA.md` discussion, not a local workaround.
