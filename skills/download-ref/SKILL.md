---
name: download-ref
user-invocable: false
description: Use when adding papers to the quantum.eval pool or re-rendering them — an arXiv ID to fetch, "render this paper", "re-fetch metadata". Renders paper PDFs into papers/<id>/ beside their schema.toml via the bundled scripts.
---

# download-ref (quantum.eval)

Origin: [QuantumBFS/sci-brain `skills/download-ref`](https://github.com/QuantumBFS/sci-brain/tree/main/skills/download-ref).
The helpers vendored here are `quantum.harness`'s bib-driven adaptation of
that skill (harness `skills/download-ref` @ `edfb385`: adds
`md_to_bibtex.py` / `append_bibtex.py`, drops `resolve_kb.py`), with this
SKILL.md rewritten for the eval-repo layout. Sync order: sci-brain is the
upstream lineage; the harness copy is the immediate source of the helpers.

Renders papers into Markdown beside their schema TOMLs, one paper one
folder. Raw PDFs and extracted figures stay local (gitignored). The
workflow MUST be run via the bundled scripts — hand-editing rendered
Markdown is not the intended path.

## Layout

```text
ref.bib                       # source of truth (committed); keywords = {tier, family}
papers/<arxiv_id>/            # one paper, one folder; the KB unit for the scripts
  schema.toml                 # the single truth (labels: tier, family, kind, status)
  <arxiv_id>_<slug>.md        # rendered paper, canonical_id = arXiv id
  .manifest.json              # single-entry manifest, derived from ref.bib, gitignored
  .raw/                       # S2 metadata json + PDF, gitignored
  .figures/                   # extracted PDF images, gitignored
```

`ref.bib` is the source of truth for what gets rendered. Each entry's
`keywords` field carries `{tier, family}` (mirroring the schema labels).
Cite keys: `lastname_year_firstword` (lowercase ASCII, stop words
dropped). There are no index files and no tier directories — grouping is
by schema label via `scripts/select.py`.

## Workflow (per paper)

Steps 3–4 are idempotent (existing metadata/PDFs are skipped; rendered
markdown is overwritten from raw). Step 6 is REQUIRED before reporting.

```sh
HELPERS="$(pwd)/skills/download-ref/helpers"
ID=2601.18229                   # the paper being added or re-rendered
KB="papers/$ID"
```

1. **Edit `ref.bib`** — add an `@article` with `eprint` (arXiv id),
   plus `keywords = {<tier>, <family>}`. Journal ref goes in `note`.
   New papers also get a metadata-only `papers/<id>/schema.toml`
   (`[paper]` per `SCHEMA.md`, `status = "candidate"`).
2. **Derive the single-entry manifest**:

   ```sh
   python3 "$HELPERS/bibtex_to_manifest.py" ref.bib | python3 -c "
   import json, pathlib, sys
   e = [x for x in json.load(sys.stdin)['arxiv'] if x['id'] == '$ID']
   assert len(e) == 1, f'{len(e)} bib entries for $ID'
   pathlib.Path('$KB').mkdir(exist_ok=True)
   pathlib.Path('$KB/.manifest.json').write_text(json.dumps({'arxiv': e, 'doi': []}))"
   ```

3. **Fetch metadata + PDF**:
   `python3 "$HELPERS/fetch_metadata.py" --kb "$KB" --manifest "$KB/.manifest.json" --download-arxiv-pdfs`
   Metadata comes from the Semantic Scholar batch endpoint (venue/DOI
   confirmation included) even for arXiv entries; only the PDF comes from
   arXiv. **Rate limits**: unauthenticated S2 429s under load — retry the
   same command with ~75 s outer backoff until `.raw/arxiv/<id>.json`
   exists; the call is idempotent. Do NOT substitute another metadata
   source.
4. **Render**:
   `python3 "$HELPERS/render.py" --kb "$KB" --manifest "$KB/.manifest.json"`
   (uses `pymupdf4llm`, extracts figures into `.figures/`)
5. **Update the schema** — flip `schema.toml` `status` to `"rendered"`
   and record `doi` from the fetched metadata (`externalIds.DOI`). The
   rendered text is the arXiv version; watch for v1-vs-published figure
   differences at truth-digitization time.
6. **Verify**:
   - `git check-ignore "$KB/.raw" "$KB/.figures" "$KB/.manifest.json"` all ignored
   - exactly one `$KB/<id>_*.md` with `full_text: yes` in its frontmatter
   - the entry appears in `ref.bib` with tier + family keywords matching
     `schema.toml`

Bulk re-renders loop the same steps over a dataset:
`for ID in $(python3 scripts/select.py all-physics); do ...; done`.

## Notes

- DO NOT commit `.raw/`, `.figures/`, or `.manifest.json`.
- DO NOT hand-edit `.manifest.json` — change `ref.bib` and re-derive.
- `md_to_bibtex.py --lit-root papers --out ref.bib` rebuilds bib structure
  from rendered frontmatter if it ever drifts, but derives `keywords` from
  the directory name — under this layout that is the arXiv id, so restore
  `keywords = {tier, family}` from each `schema.toml` and review the diff.
