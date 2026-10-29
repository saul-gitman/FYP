# Aerogel simulator: build plan (v0, for council review)

Status: **plan only, nothing built yet.** Written 2026-10-29 from the handover pack `FYP_Handover_2026-10-29.zip`.
Project: *Thermo-optically functional CFRP laminates for lightweight electrified systems* (PolyU AAE capstone 2026/27, supervisor Dr CHAN Kit-Ying).

## 1. One-paragraph summary

Build a reproducible Python tool that maps **structure → properties** for a freeze-cast directional aerogel: geometry in, directional effective thermal conductivity (k_parallel, k_transverse, anisotropy ratio), porosity, density and temperature/flux fields out. Version 1 covers the aerogel alone, one fixed wall composition and a pore-size sweep. That matches what the supervisor agreed in the meeting (S02–S06). Composition sweeps follow, then the CFRP laminate and the experimental load cases. Every input is labelled *measured / literature / derived / hypothetical*. The tool is judged on **trends**, not on matching absolute numbers (V01–V03).

## 2. Scope by version

| Version | Content | Gate to next version |
|---|---|---|
| **v0.1 core** (target: before the interim report, 21 Dec 2026) | Unit-cell geometry, derived porosity/density, axial + transverse conduction solver, Knudsen gas, wall-mixture bounds, pore-size sweep, plots + JSON/CSV + auto report | Verification suite passes (§6) |
| v0.2 physics options | Switchable radiation (off / opaque-wall cell exchange / Rosseland with optical-thickness check), nanoporous wall option, imperfect/tilted channels (3D FV), tensor rotation | Sensitivity study shows which unknown inputs dominate |
| v0.3 composition | Dry-mass-basis composition of CNF / CNT / BN / MTMS-derived solid; wall k from bounds/EMT; binder-feasibility **warning** (not a threshold); C-series and B-series of the Word guide | Agreement with the experimental *trend* or a written explanation |
| v1.0 laminate | 1D through-thickness stack + 3D plate: BN/CNF/MTMS surface → upper CFRP → CNT/CNF/MTMS interlayer → lower CFRP, heater 20×20 mm; load cases 2 W (5 W), 1000 W/m², combined; interface resistance R″_c; resin-infiltrated state kept separate from the dry state | Energy balance and comparison with P / C* / B* / C*+B* plates |

Out of scope for now: mechanics, spectral optics (reflectance is a measured *input*), processing → structure (no invented freezing-temperature-to-pore-size law).

## 3. Model design

### 3.1 Geometry (representative cell)
- Straight prismatic channels along axis **z** (the freezing/growth direction). Cross-section options: (a) circular pores in square or hex array; (b) **hexagonal or square honeycomb with thin walls** (needed in practice).
- Parameters: pitch *p*, pore size *d* (diameter or flat-to-flat), wall thickness *t*, cell length *L*. Only two of {p, d, t} are independent; porosity follows from them, never prescribed separately (S07).
- **Key limitation:** circular pores in a hex array cannot exceed φ = π/(2√3) ≈ 90.7 %. Literature BN aerogels sit at about 97–98 %. A hex honeycomb with φ = (d/p)² reaches 98.2 % at d = 30 µm only with t ≈ 0.27 µm. So the realistic cell is a thin-walled honeycomb, possibly with **nanoporous walls** (wall-internal porosity φ_w) as a later option.

### 3.2 Three sweep definitions (the user must choose one; the tool supports all three)
| Mode | Held fixed | What changes with d | Physical meaning |
|---|---|---|---|
| A | wall thickness t | φ rises, ρ falls | "bigger holes, same walls" (matches the supervisor's "change hole size → density/porosity follow") |
| B | pitch p | t shrinks, φ rises | fixed cell spacing |
| C | porosity φ (so t ∝ d) | only absolute scale | same slurry, different freezing temperature (closest to the experiment) |

**Expected result to flag early:** in mode C, pure conduction is scale-invariant, so k barely changes with d. Pore-size dependence then comes only from radiation and gas rarefaction. At d ≈ 30 µm and 1 atm, Kn ≈ 68 nm / 30 µm ≈ 0.002, so the Knudsen correction is below 1 %. This is a result to report, not a bug.

### 3.3 Solvers
- **Along the channels (k_par):** for straight uniform channels the axial problem has an exact solution: area-weighted parallel mixing, k_par = φ k_gas,eff + (1−φ) k_wall,z (+ radiation term). Checked numerically by the 3D solver.
- **Across the channels (k_trans):** 2D steady conduction ∇·(k∇T) = 0 on the unit-cell cross-section. Finite-volume on a structured grid, harmonic-mean face conductances, sparse solve (SciPy; AMG if needed). Two boundary schemes: (i) **periodic homogenisation**, giving the full 2×2 tensor from ⟨q⟩ = −K⟨∇T⟩; (ii) fixed ΔT with insulated sides, giving k = qL/ΔT. Both are reported, and they must agree for symmetric cells.
- Thin walls (t/p ≈ 0.01) need resolution: local grid refinement or a wall-aligned subgrid. A thin-wall network check (in-plane honeycomb solid contribution ≈ (1−φ)k_w/2) is used as an independent test.
- **3D FV** (v0.2) for imperfect or tilted channels and for the laminate. K_global = R K_local Rᵀ for rotated alignment.

### 3.4 Constituent physics (each one switchable, with stated assumptions)
- **Gas:** k_g = k_g,free / (1 + 2β Kn), Kn = λ_mfp / d_pore, β taken from a cited convention (accommodation-dependent). It is applied with the correct length scale: macro-channels use d, and nanoporous walls (if enabled) use the wall pore size.
- **Wall solid:** effective wall conductivity from the dry composition, reported as a **band**: series (lower) / parallel (upper) / Maxwell–Eucken / Bruggeman EMT, plus an anisotropic in-wall option for BN platelets aligned in the wall plane. The default single value is labelled *hypothetical* until calibrated.
- **Radiation:** off by default for v0.1. In v0.2 there are two options: opaque-wall exchange across each cell, k_rad ≈ 4σT³d·ε/(2−ε) (order 0.2 mW/m·K at 30 µm, small); or Rosseland k_rad = 16n²σT³/(3β_R), which is allowed **only** if the optical thickness β_R·L ≫ 1. This matters because at ρ ≈ 20 kg/m³ and an unknown specific extinction, a 1 mm aerogel may be optically thin, so Rosseland would be invalid there. CNT strongly changes the extinction. No double counting with external surface radiation.
- **Convection:** neglected, with a Rayleigh-number justification printed in the report.

### 3.5 Composition bookkeeping
- Use **dry retained mass fractions** w_i, never the wet-slurry wt % of the Word guide. ρ_solid = 1/Σ(w_i/ρ_i), ρ_bulk = (1−φ)ρ_solid.
- Converter from the guide recipe (batch 50 g, CNF 0.5 g dry, MTMS feed 1 g, CNT 0–5 g, BN 0–15 g) to dry fractions. The MTMS retention factor is an explicit *hypothetical* input, because the guide does not give it.
- Feasibility: warning when the binder (CNF + MTMS-derived) fraction drops below a user-set level (S11). No invented threshold.

## 4. Inputs and provenance
Every input is stored in a YAML config with fields `value, unit, source, status ∈ {measured, literature, derived, hypothetical}`. A run refuses to label a result "calibrated" if any dominant input is hypothetical.

Literature anchors available offline (Chan et al. 2022, Nat. Commun. 13:5553, BNNS/WPU ACA, *not the project material*):
- pore ≈ 30 µm; density 20.2 mg/cm³; porosity 98.2 %; BNNS 2.25 g/cm³; WPU 1.02 g/cm³
- k_trans = 16.9 mW/m·K (hot disk); anisotropy R = k_align/k_trans ≈ 5.8 (≈ 7 at 50 wt % BNNS)
- the paper's literature range: k_trans 15–37, k_align 44–170 mW/m·K
- other contextual values: Liu 2021 CNF/BN 28.4 (lateral) / 83.3 (axial) mW/m·K; Adegun 2023 20.3; Yang 2022 23.5 mW/m·K

**Validation tension to report honestly:** reported k_trans values below air (≈ 26 mW/m·K) cannot be reproduced by any continuum model of micron channels filled with air at 1 atm. The series lower bound is ≈ k_air/φ ≈ 26.5 mW/m·K, so the result is above it. Lou et al. (2023) discuss how the test method and internal radiation affect inferred conductivity. The tool will therefore compare **trends and anisotropy**, and it documents the absolute gap and its candidate causes (measurement method, nanoporous walls, non-air gas) instead of tuning inputs to hide it.

## 5. Software
- Python 3, NumPy/SciPy, Matplotlib; `pytest`; config in YAML; CLI `aerosim run config.yaml` / `aerosim sweep ...`.
- Outputs per run: `inputs.json`, `results.csv/json`, field plots (T, |q|), sweep plots, `report.md` with assumptions and a provenance table.
- An optional viewer (a static HTML page or Streamlit) comes later. It sits on top of the solver and never replaces the verification suite.
- ANSYS/COMSOL: not required for v0.1. One cross-check case can be exported if the supervisor or the report wants a commercial-code comparison.

Proposed layout:
```
aerosim/
  geometry.py      # cells, porosity, density, masks
  materials.py     # constituent library + provenance
  mixing.py        # wall-mixture bounds/EMT
  gas.py           # Knudsen
  radiation.py     # options + validity checks
  solver_fv2d.py   # transverse homogenisation
  solver_fv3d.py   # v0.2+
  study.py         # sweeps (modes A/B/C), composition
  report.py
  cli.py
tests/
configs/
docs/
```

## 6. Verification (must pass before any study is reported)
1. Homogeneous slab: k_eff = k exactly; flux sign and units.
2. Layered laminate: series/parallel analytic, including contact resistance ΔT = q R″_c.
3. Circular inclusions in square array vs Rayleigh / Maxwell–Garnett at low φ; all results inside Hashin–Shtrikman bounds.
4. Grid convergence (≥ 3 refinements, observed order reported); representative-cell-size check (1×1 vs 2×2 cells).
5. Energy balance (in = out to solver tolerance); K symmetric positive definite; periodic vs fixed-ΔT agreement.
6. Axial 3D FV result = exact parallel formula.

## 7. Studies
1. **Pore-size sweep, fixed composition** (the first deliverable): d over a literature range (about 10–100 µm, to be confirmed from SEM or papers) in modes A/B/C; outputs k_par, k_trans, R, φ, ρ.
2. Sensitivity (tornado): k_wall, φ, d, t, gas, radiation on/off, to find the 1–2 dominant variables (S05).
3. Composition: BN:CNF and CNT:CNF on a declared dry basis, mirroring the C-series (CNT 0–10 wt % wet) and the B-series (BN 0–30 wt % wet).
4. Later: laminate load cases and plain / C* / B* / combined comparisons.

## 8. Timeline (proposed)
| Weeks from start | Milestone |
|---|---|
| 1 | Geometry + materials + 2D FV + verification tests 1–5 |
| 2 | Pore-size sweep (A/B/C), report generator, first results to supervisor (S12: report even weak results) |
| 3–4 | Radiation/nanoporous-wall options, sensitivity, composition converter |
| By 21 Dec 2026 | Interim-report-ready figures and method chapter |
| Jan–Mar 2027 | Laminate model, load cases, comparison with plates |

## 9. Decisions needed from the user (defaults in bold)
1. Sweep mode for the first study: **run all three, headline mode C**.
2. Language/tooling: **Python**, with an optional ANSYS/COMSOL cross-check.
3. Cell shape: **hex thin-wall honeycomb**; circular pores kept as the supervisor's "simple" case and for verification.
4. Whether the B-series substrate includes the carbon-free interlayer (guide issue E09), needed only from v0.3.
