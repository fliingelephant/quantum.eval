---
name: paper-to-schemas
description: Use to extract one rendered paper into its schema.toml sections — "extract 2201.01234", "draft the schema for this paper". The unit of work is one paper.
argument-hint: <arxiv_id>
---

# paper-to-schemas — one paper → one schema

Fills the extraction sections of `papers/<id>/schema.toml` from the
rendered paper, per the contract in `SCHEMA.md` (sections) and
`DESIGN.md` §4 (partition law). The unit of work is ONE paper.

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
   - Redaction is per-occurrence. A revealing term or fact that appears
     N times needs N blocks — fencing some occurrences while leaving
     others readable is a leak. After drafting, search the md for every
     revealing term already blocked (method and software names, key
     values, finding phrases) and block each remaining hit — including
     front matter, repeated headings, and the bibliography. Context
     does not exempt an occurrence: a method named while surveying
     prior work reveals the route the same as in the methods section.
   - Block the minimal revealing content. Result-stating units — title,
     abstract, figure-embedded text, captions, conclusions — routinely
     state outcomes; check each of them and hide only the outcome —
     values, exponents, phase identifications — leaving the setup half
     (model, instance, what was computed) readable. The outcome half is
     `truth`: a title that states the finding gets its outcome phrase
     blocked as `truth`, not the whole line as `problem`. Whole-line
     form is for units that reveal in full: a method-named section
     header, an equation image defining the algorithm, an
     algorithm-walkthrough paragraph. Do not fragment such a passage
     into spans — that leaves connective method vocabulary readable
     between the fenced pieces.
   - **Sections are decided by swap tests** (`SCHEMA.md`): would the
     content survive switching to a different valid numerical method?
     Yes → `problem` — the paper's physics analysis (observables and
     their ratios, system sizes, transition-locating criteria, fits and
     error analysis) is never method content, even inside a
     methods-titled section. Tied to the chosen method: what the method
     *is* — formalism, update moves, data structures, estimator
     constructions — is `method`; only the tunable values an operator
     sets (an expansion cutoff, a sweep count, a discretization step, a
     bond dimension) are `method_params`. Tied to one implementation:
     which code is `software`; its knobs (a solver tolerance, a
     threading setting) are `software_params`. The standard failure
     mode is **over-labeling out of `problem` and out of `method` into
     the narrower sections** — a capable extractor rarely misses
     content but often over-assigns it; when the swap question says
     `problem`, it is `problem`, and when nothing is tuned, it is not a
     `*_params` section. (Examples: a bond dimension → `method_params`;
     an eigensolver tolerance → `software_params`; a correlation-length
     ratio → `problem`; an update move's description → `method`, not
     `method_params`.)
   - Value-carrying spans split by origin: a value the paper computed —
     a located boundary, a fitted exponent, an identified phase — is
     `truth`; a value knowable without this paper's computation (an
     exact limit, a closed form) is `anchors`. Computed results are
     never `problem` or `anchors`, whatever unit they appear in. Judge
     a span by what it reveals, not its rhetorical mode: a prediction,
     expectation, or schematic the paper goes on to confirm reveals
     the finding all the same.
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
7. **End by reporting a digest**: targets found
   (panel id, quantity, tier, truth source), block count per section,
   anything Inferred, anything ambiguous flagged for the human.

## Postconditions

- `schema.toml` gains `md_sha256` and the seven sections
  (`[candidate_notes]` stays); `blocks.toml` holds the anchored partition
  layer. The rendered md is frozen from here on (re-render ⇒ re-extract).
- The **human** flips status to `schema-drafted` at ratification — the
  extractor never edits `status` (its only `[paper]` write is
  `md_sha256`). The human may review per paper, batch-approve, or waive
  review; the independent quality check is `verify-schema`, not this
  gate.

## Rules

- Extraction is a pure function of (rendered md, `SCHEMA.md`). No
  knowledge of visibility maps, eval tasks, or other papers may enter.
- Nothing paper-specific is special-cased; if the contract fails on a
  real paper, that is a `SCHEMA.md` discussion, not a local workaround.
