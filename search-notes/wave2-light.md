# Wave 2 — laptop tier, PR 2024–26 (physics-only correction applied mid-flight)

Four searchers with the laptop bar (CPU, ≤16 GB, minutes–hours). All received
the mid-flight correction: methods papers count as purely numerical → drop.

## MPS-light searcher — 6 candidates, all physics

Selected: 2501.03329 (Bhullar/Xu/Kee, field-induced orders in anisotropic
Kitaev chains, PRB 111 104439; degenerate PT backbone), 2408.07968 (Yang+/
Affleck, LLRR order in Kitaev-Heisenberg chain + c=1 gapless phase, PRB 112
035104; bosonization), 2410.13354 (Miura/Totsuka, emergent spacetime SUSY in
interacting Kitaev chain, PRB 111 075136; c: ½→7/10 tricritical Ising),
2410.21424 (Mögerle+/Büchler, spin-1 Haldane phase in Rydberg chain, PRXQ 6
020332; SPT theory proposal, no experimental data despite experiment-group
authors; long-range MPO sum-of-exponentials caveat), 2501.13059 (Sharma+/
Mila, S(q,ω) of spin-1 J₁–J₂ chain near first-order transition at
J₂≈0.76J₁, PRB 111 064404; tDMRG + SMA/confinement picture), 2601.18229
(Mondal+, breakdown of bosonic Thouless pump in quasiperiodic lattice,
PRB 2026 accepted, DOI 10.1103/6gdw-nmjk — re-verify at render; iTEBD;
heaviest of the light set).

- Kitaev-adjacent weighting in #1–3; #4–6 give orthogonal families.
- Re-rejected: 2509.22773 (still preprint).

## QMC-light searcher — 5 candidates

Selected: 2403.02400 (Weber, anisotropic spin-boson fixed-point annihilation
+ pseudocriticality, PRB 112 235153; wormhole world-line QMC, single-spin
imaginary-time problem — seconds/point, strongest laptop QMC), 2311.07683
(Ribeiro+/Weber, dissipation-induced LRO in 1D Bose-Hubbard, PRB 110 115145),
2506.16424 (Kumar/Pujari/D'Emidio, pseudocriticality in AFM spin chains —
c(N) walking vs complex-CFT, PRL 136 076701), 2405.08688 (Caci+/Uhrig,
anisotropic square-lattice Heisenberg LRO + magnon expansion, PRB 110
054411; moderate-λ targets laptop, small-λ extrapolations NOT), 2509.02044
(Wang+/Zhang, boundary RG flow of EE at (2+1)D O(3) QCP, PRB 113 L161104 —
filed medium: clean γ needs beyond-laptop L; single S₂(L) curve is light).

- Structural finding: laptop fermionic DQMC/AFQMC with real theory content
  effectively absent in PR 2024–26; laptop QMC = spin/boson.
- Near-misses: 2310.11525 spin chains with bond dissipation (physics fit,
  likely SciPost — no PR ref); 2309.02407 fully-frustrated TFIM (needs
  L=96); 2410.13844 post-measurement QMC (methods); 2401.08157 exact
  staggered-dimer 2D magnet (ED + bond-operator MF, not QMC); 2603.07031
  sub-Ohmic three-term criticality (variational, not QMC); event-chain MC
  paper (methods). Watchlist: 2312.13095 AFM order from local dissipation
  (unverified PR status; would be a third Weber-group entry).

## VMC-light searcher — 5 candidates

Selected (light): 2407.03046 (Piccioni+/Becca, 1D Hubbard-SSH phases incl.
doped spin-gapped metal, PRB 111 045125), 2412.05975 (Favata+/Becca, 1D
half-filled BHZ interaction-induced phases, PRB 111 155105; DMRG
cross-check), 2410.18747 (Budaraju+, monopole excitations in triangular U(1)
Dirac SL vs QED₃, PRB 111 125150; per-size targets light, L=28 extrapolation
not). Filed medium: 2503.11834 (Kumar/Kang/Lee, Dirac node pinning from DM
on kagome, PRL 136 146704; D_c≈0.28J, φ_min fit, 216-site + HPC as
published), 2311.02639 (Zhang/Jin/Zhou, SU(4) spin-orbital model on
triangular, PRB 109 125103; decisive ordering needs L=24 tori).

- Excluded: 2407.20629 kagome 1/9 plateau (432–576 sites — later taken as
  medium in wave 3); 2406.13634 iron-pnictide three-orbital VMC (HPC,
  days–weeks); 2408.16453 second-order topological magnet (361k-param GCNN);
  2308.09709 long-range Ising RBM (authors compute-limited); 2502.00130
  YbZn₂GaO₅ (experimental); 2501.00096 (preprint); 2403.07795 fine-tuning
  NQS + 2210.00692 interpreting CNN (methods).

## 2D-TN-light searcher — 4 candidates

Selected: 2505.05194 (Pulloor Kuttanikkad+, J₁-J₂ clock model — emergent Zq
stripe order + Landau-incompatible transitions, PRL 135 256703; CTMRG on
classical partition function, minutes), 2410.01460 (Chatelain, frustrated
2D Ising first-order + Ashkin-Teller marginal criticality, PRE 111 024109;
TRG), 2403.17309 (Homma/Morita/Kawashima, AFM 6-state clock on Union-Jack
lattice — BKT + Z₆ + chiral Ising transitions with CFT data, PRB 111 134427;
caveat: nuclear-norm-regularized TRG is method-forward framing — judged
physics-leaning), 2508.08376 (Zhang/Xu, continuous toric-code↔double-semion
transition, XY* class, PRB 112 L241107; C₄ᵥ iPEPS AD+CTMRG, headline at
D≤6/χ≤100 laptop; D=7 precision exponent beyond).

- Rejected: 2403.11490 spin-1 Kitaev iPEPS (D=8, thin theory); 2503.19027
  Z₂-LGT roughening (iDMRG, not 2D-TN); 2411.01009 FCLS disorder parameter
  (methods); 2506.00114 symmetry-deformed toric codes (QMC+DMRG numerics);
  2401.14830 / 2510.21269 Chatelain classical TN (J. Stat. Mech., non-PR);
  2604.15749 CFT-data extraction (methods); 2311.03353 (primarily analytic).
- Structural finding: the constraint intersection is genuinely narrow —
  laptop 2D-TN physics lives in classical partition-function contraction.
