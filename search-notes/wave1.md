# Wave 1 — PR 2025–26, feasibility unrestricted (pre physics-only correction)

Five searchers, one per family. Candidates marked ▸quarantined were later
moved to `candidates/methods-papers/` under the physics-only rule.

## MPS searcher — 5 candidates

Selected: 2503.11413 (Pronk/Chepiga, DQCP frustrated Haldane chain, PRB 111
L220412), 2504.02157 (D'Elia/Paiva, Haldane phase in two-leg Hubbard ladder,
PRB 112 035169), 2408.14474 (Nigam+, dimerized XXZ chain, PRB 111 195131),
2410.18913 (Kerschbaumer+, scars beyond PXP, PRL 134 160401), 2602.23187
(La Rivière/Chepiga, extended Ashkin-Teller in coupled Haldane chains, PRB
113 205107).

- Overlap note: 2503.11413 and 2602.23187 are both Chepiga-group frustrated
  spin-1 Haldane systems — distinct universality classes (WZW SU(2)₂ +
  eight-vertex DQCP vs Ashkin-Teller), keep one if maximal source diversity
  is wanted.
- Rejected: 2502.15463 "Mesons in a quantum Ising ladder" (JHEP, not PR;
  truncated free-fermion space, not MPS); 2509.22773 shallow global quenches
  (preprint, no journal ref); iDMRG-on-cylinder 2D spin-liquid papers
  (χ up to ~2000, fails modest compute); square-hexagon-octagon Heisenberg
  (PRB 2026) — SSE-primary, not MPS.
- Verification: APS DOI pages resolve with journal named (new-style DOIs
  s53y-qmr4, rspn-4cyr, yfwf-vxwb); direct APS fetches 403, so citations
  cross-checked across independent search results.

## QMC searcher — 5 candidates

Selected: 2409.10273 ▸quarantined (Ding+, Rényi negativity via
reweight-annealing; c=0.51(3), 2D TFIM h/J=3.04438(2), β_c=1.0874(1)),
2503.13247 (Jiang+, GNY boundary criticality, PRL 135 141602, 4−ε RG matched
to DQMC), 2501.12146 ▸quarantined (Ding+, stabilizer Rényi entropy sampling,
PRXQ 6 030328), 2406.02681 (Zhao+, disorder operator at easy-plane DQC, PRB
112 094416), 2412.15168 (Yang/Schumm/Sandvik, S(k,ω) of long-range
Heisenberg chain, PRB 111 224404; α≈2.23 boundary, z(α)).

- Excluded/watchlist (fail only the PR-published gate at check time):
  2602.03656 honeycomb-Hubbard GNH exponents (also 10,368-site projector
  DQMC — too heavy anyway); 2510.25840 disorder operator at (3+1)D O(3);
  2506.16111 Rényi thermal-entropy scaling theory; 2505.17411
  condensate-fraction BKT (attractive-Hubbard AFQMC, 64×64).
- 2412.11382 angle-tuned GN criticality in TBG: strong but Nature
  Communications (non-PR).
- Set leans SSE; 2409.10273/2501.12146 share the Yan group.

## VMC searcher — 6 candidates (5 later quarantined)

Selected: 2412.04544 (Bose/Paramekanti, easy-plane Dirac SL in honeycomb
J₁–J₃ XY, parton VMC + RPA — the one physics keep), 2505.20406 ▸quarantined
(RNN NQS triangular), 2505.03466 ▸quarantined (deep translationally-symmetric
NQS design principles), 2510.11710 ▸quarantined (symmetrized determinant NQS
Hubbard), 2411.07144 ▸quarantined (autoregressive NQS Fermi-Hubbard),
2405.17541 ▸quarantined (approximately-symmetric NQS for QSLs).

- Excluded: 2509.02663 trellis semi-Dirac SLs (PRR 2026 — parton mean-field
  primary, VMC not the tool; DMRG/PFFRG validate); 2501.00096 SS Z₂ Dirac SL
  and 2503.20122 SS deconfined gapless phases (both strong VMC+PSG fits,
  still preprints — revisit when published); 2602.12998 kagome ViT plateaus
  (Feb 2026 preprint).

## iPEPS searcher — 6 candidates

Selected: 2502.14091 (Corboz+, SS QSL window 0.785(5)≤J'/J≤0.82(1), PRL 136
186701), 2503.07689 (Jahromi/Iqbal, square-kagome VBC phases, PRB 113
L140402), 2412.17495 (Samimi+, bilayer Kitaev-Heisenberg + analytic pCUT
cross-check, PRB 113 245133), 2403.12141 (Wang+, Kitaev-in-field
fractionalization, PRB 111 L100402 — static boundaries cheap, dynamics NOT
modest), 2406.10689 (Nyckees+, weakly-first-order 1/3-plateau melting,
T_c ≈ 4.8 K, PRB 111 014428), 2503.18413 (Han+, finite-T Rydberg arrays,
2D-Ising exponents, PRB 111 235133).

- Redundancy: Shastry-Sutherland ×2 (T=0 QSL vs finite-T melting), Kitaev ×2
  (ground state vs dynamics) — graded difficulty, or drop one each for
  lattice spread.
- Bond dimensions generally not stated in abstracts — not fabricated;
  D/χ live in methods sections.

## Other-methods searcher — 6 candidates (5 later quarantined)

Selected: 2410.21812 ▸quarantined (Yao/Zhang, correlation-matrix scar
diagnostic, PRB 112 125165), 2506.10806 (Yang/Magoni/Pichler, scars from
weak fragmentation, PRB 113 174307 — the physics keep), 2511.07303
▸quarantined (Li+, tanTRG fixed filling, PRB 113 085150), 2408.06414
▸quarantined (Segall+, RG-improved actions for 3D XY, PRB 111 184413),
2507.03137 ▸quarantined (Jansen+, SDP phase-diagram mapping, PRL 136
050401), 2404.05784 ▸quarantined (Schuhmacher+, hybrid tree tensor networks,
PRXQ 6 010320).

- **No genuine block-spin MCRG in PR 2025–26**: Swendsen-style two-lattice
  matching MCRG in PR venues is all 2017–2021 (Wu–Car variational MCRG,
  neural MCRG). 2408.06414 is the honest closest proxy (deterministic
  tensor-RG builds the action, MC only measures).
- tanTRG chosen deliberately over the thermal-PEPS paper (PRB 111 075146)
  to stay MPO-based; certifying-ground-state-properties seminal paper is
  PRX 2024 (out of window) — 2507.03137 is its 2026 PRL successor.
