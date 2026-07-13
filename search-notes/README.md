# search-notes — searcher-subagent first-glance intelligence

Raw findings from the candidate-search subagents (Opus 4.8, web search,
2026-07-13). **Unverified first-glance material**: journal refs were
cross-checked via search results (APS blocks direct fetch), feasibility is
estimated, and physics/methods judgments are the searchers' calls. The
curated truth per paper lives in `candidates/**/*.toml`; these notes keep
what the TOMLs drop — near-miss watchlists (preprints to revisit when
published), rejection rationales, and family-level structural findings.

- `wave1.md` — 2025–26, feasibility unrestricted, one searcher per family
  (ran before the physics-only correction; several picks later quarantined
  to `candidates/methods-papers/`)
- `wave2-light.md` — laptop tier, 2024–26, physics-only correction applied
  mid-flight
- `wave3-fill.md` — fill-to-20 wave: ED-light, VMC-medium, finite-T,
  medium-diversity

Family-level findings worth remembering:

- **No genuine block-spin MCRG paper exists in PR 2024–2026** (closest:
  RG-improved actions, 2408.06414 — quarantined as methods).
- **Laptop-scale fermionic DQMC/AFQMC physics papers effectively don't
  exist** in PR 2024–26 (O(N³) determinants + sign problem); laptop QMC is
  spin/boson SSE/world-line territory.
- **Laptop 2D-TN physics lives in classical partition functions** (clock /
  frustrated-Ising TRG-CTMRG); quantum iPEPS headlines almost always need
  D ≥ 8 or cluster-scale extrapolation.
- **NQS literature 2024–26 is dominated by architecture (methods) papers**;
  VMC physics papers are mostly Gutzwiller-projected parton studies, and
  the laptop-feasible ones are 1D classic VMC (Becca-school).
