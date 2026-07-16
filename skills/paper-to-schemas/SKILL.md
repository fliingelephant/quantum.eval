---
name: paper-to-schemas
description: Use to extract one rendered paper into its schema.toml sections — "extract 2311.07683", "draft the schema for this paper". Per-paper procedure, designed to run inside one subagent per paper; a main agent loops it over a dataset.
argument-hint: <arxiv_id>
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
3. **Move content into blocks** (`papers/<id>/blocks.toml`) — **agents
   quote, scripts count**: author every block as a verbatim quote with NO
   char offsets, then anchor. Sub-line spans are the norm (the renderer
   emits one line per paragraph, so whole lines are usually far too much):

   ```toml
   [[blocks]]                     # span form — the norm
   sections = ["method"]          # every section this span reveals
   lines = "541"                  # the line it sits on
   text = "DMRG"                  # verbatim substring — never count chars
   # nth = 2                      # only if the substring repeats on the line

   [[blocks]]                     # whole-line form — only if it ALL reveals
   sections = ["method"]
   lines = "412-431"
   text = """...the full lines, verbatim..."""
   ```

   Then run `python3 scripts/anchor_blocks.py papers/<id>` — it resolves
   quotes to offsets and canonicalizes the file; fix any ambiguity it
   reports (lengthen the quote or add `nth`) and re-run.

   - Verbatim only — never paraphrase. Hidden spans are replaced by a
     fixed marker; whole-line blocks are deleted.
   - Block the minimal revealing content. In result-stating units (title,
     abstract, captions) hide only the outcome — values, exponents, phase
     identifications — and leave the setup half (model, instance, what
     was computed) readable. Whole-line form is for units that reveal in
     full (a method-named section header, an equation image defining the
     algorithm).
   - **Sections are decided by swap tests** (`SCHEMA.md`): would the
     content survive switching to a different valid numerical method?
     Yes → `problem` — the paper's physics analysis (observables and
     their ratios, system sizes, transition-locating criteria, fits and
     error analysis) is never method content, even inside a
     methods-titled section. Survives only a software swap →
     `method_params`. Survives neither → `software_params`. The
     standard failure mode is **over-labeling into `method*`/
     `software*`** — a capable extractor rarely misses content but
     often over-assigns it; when the swap question says `problem`, it
     is `problem`. (Examples: a bond dimension → `method_params`; an
     eigensolver tolerance → `software_params`; a correlation-length
     ratio → `problem`.)
   - A span revealing several sections lists them all; derivation later
     hides a block if ANY of its sections is hidden. Torn between
     sections? Tag the union and flag it in the digest (uncertainty rule,
     `SCHEMA.md`).
   - Ranges must be pairwise disjoint at (line, char) granularity. Blocks
     are visibility-agnostic: capture for every section uniformly,
     including `[problem]`; which blocks get hidden is decided elsewhere.
   - A figure whose image reveals a section: block the image-link line(s);
     within its caption, span-block only the revealing parts. A
     bibliography entry cited only inside blocked text is itself a block.
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
6. **Self-lint**: `python3 scripts/anchor_blocks.py papers/<id>` then
   `python3 scripts/lint_schema.py papers/<id>` — both must pass.
7. **Return a digest** (the subagent's final message): targets found
   (panel id, quantity, tier, truth source), block count per section,
   anything Inferred, anything ambiguous flagged for the human.

## Postconditions

- `schema.toml` gains `md_sha256` and the seven sections
  (`[candidate_notes]` stays); `blocks.toml` holds the anchored partition
  layer. The rendered md is frozen from here on (re-render ⇒ re-extract).
- Status flips to `schema-drafted` after the digest is surfaced to the
  human — who may review per paper, batch-approve, or waive review; the
  independent quality check is `verify-schema`, not this gate.

## Rules

- Extraction is a pure function of (rendered md, `SCHEMA.md`). No
  knowledge of visibility maps, eval tasks, or other papers may enter.
- Nothing paper-specific is special-cased; if the contract fails on a
  real paper, that is a `SCHEMA.md` discussion, not a local workaround.
