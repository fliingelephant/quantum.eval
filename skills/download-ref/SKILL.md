---
name: download-ref
user-invocable: false
description: Use when adding papers to the quantum.eval candidate pool or re-rendering them — an arXiv ID or DOI to fetch, "render the candidates", "re-fetch metadata", "rebuild the INDEX". Renders paper PDFs into per-tier markdown beside their schema TOMLs via the bundled scripts.
---

# download-ref (quantum.eval)

Adapted from `quantum.harness` `skills/download-ref` @ `edfb385` — same
bundled helpers, paths rewritten for this repo's layout. Helpers are
upstream-verbatim; sync from the harness when it updates.

Renders candidate papers into Markdown beside their schema TOMLs and
indexes them. Raw PDFs and extracted figures stay local (gitignored). The
workflow MUST be run via the bundled scripts — manual editing of `INDEX.md`
or rendered Markdown is not the intended path.

## Layout

```text
ref.bib                       # source of truth (committed); keywords = {tier, family}
candidates/<tier>/            # tier ∈ {light, medium, methods-papers}
  <arxiv_id>.toml             # per-paper schema (the single truth)
  <arxiv_id>_<slug>.md        # rendered paper, canonical_id = arXiv id
  INDEX.md
  .raw/                       # S2 metadata json + PDFs, gitignored
  .figures/                   # extracted PDF images, gitignored
.manifest-<tier>.json         # derived from ref.bib, gitignored — never hand-edit
```

`ref.bib` is the source of truth. Each entry's `keywords` field carries
`{tier, family}`; the tier keyword selects the render manifest and target
dir. Cite keys: `lastname_year_firstword` (lowercase ASCII, stop words
dropped).

## Workflow

Run all steps in order via the bundled scripts. Steps 3–6 are idempotent
(existing metadata/PDFs are skipped; rendered markdown is overwritten from
raw). Step 7 is REQUIRED before reporting.

```sh
HELPERS="$(pwd)/skills/download-ref/helpers"
TIER=light                      # or medium
KB="$(pwd)/candidates/$TIER"
BIB="$(pwd)/ref.bib"
```

1. **Edit `ref.bib`** — add an `@article` with `eprint` (arXiv) or `doi`,
   plus `keywords = {<tier>, <family>}`. Journal ref goes in `note`.
2. **Derive the manifest**:
   `python3 "$HELPERS/bibtex_to_manifest.py" "$BIB" --method "$TIER" > .manifest-$TIER.json`
3. **Fetch metadata + PDFs**:
   `python3 "$HELPERS/fetch_metadata.py" --kb "$KB" --manifest .manifest-$TIER.json --download-arxiv-pdfs`
   Metadata comes from the Semantic Scholar batch endpoint (venue/DOI
   confirmation included) even for arXiv entries; only PDFs come from
   arXiv. **Rate limits**: unauthenticated S2 429s under load — retry the
   same command with ~75 s outer backoff until every manifest entry has its
   `.raw/arxiv/<id>.json`; the call is idempotent. Do NOT substitute
   another metadata source.
4. **Render**:
   `python3 "$HELPERS/render.py" --kb "$KB" --manifest .manifest-$TIER.json`
   (uses `pymupdf4llm`, extracts figures into `.figures/`)
5. **Index**:
   `python3 "$HELPERS/index.py" --kb "$KB" --title "quantum.eval $TIER-tier candidate papers" --source-note "Rendered candidate papers for the quantum.eval reproduction dataset. Raw PDFs and extracted figures are local-only and gitignored."`
   Keep title/source-note stable across runs.
6. **Update schema status** — flip the paper's TOML `status` to
   `"rendered"` and record `doi` from the fetched metadata
   (`externalIds.DOI`). The rendered text is the arXiv version; watch for
   v1-vs-published figure differences at truth-digitization time.
7. **Verify**:
   - `git check-ignore "$KB/.raw" "$KB/.figures"` both ignored
   - `INDEX.md` exists; every manifest entry has a matching `.md`
   - `full_text: yes` in each rendered file's frontmatter
   - the entry appears in `ref.bib` with tier + family keywords

## Notes

- DO NOT commit `.raw/` or `.figures/`.
- DO NOT hand-edit `.manifest-*.json` — change `ref.bib` and re-derive.
- `md_to_bibtex.py --lit-root candidates --out ref.bib` rebuilds the bib
  from rendered frontmatter if it ever drifts (review the diff).
