# Physics of the Aerogel k Simulator (v0.1)

Every equation the code uses, in plain words, with its source and its limits. The code in `aerosim/` follows this file line by line. SI units inside the code (W/m·K); mW/m·K only for display.

**What is modelled:** the *dry* freeze-cast aerogel skeleton only: thin solid walls (BN/CNF/MTMS) around hexagonal channels of air along the freezing direction z. No carbon fibre, no resin, no laminate.

**The one rule that holds it together:**

```
k_total = k_solid + k_gas + k_rad + k_conv        (separately along z: k∥, and across: k⊥)
anisotropy = k∥ / k⊥
```

Heat in an aerogel travels by four paths side by side: through the walls, through the air, as infrared radiation, and by moving air. Adding them is the standard decomposition for porous insulation (Hrubesh & Pekala 1994; Lou et al. 2023). Each path is counted **once**. If one method solves two paths together (Pixel FV solves solid and gas in one picture, with their coupling), it says so (`covers = ["solid", "gas"]`) and the Gas row is not added again. The footer then shows the term as `(solid+gas)`.

Sources are listed at the end. Page numbers still need checking in the originals before the final report.

---

## 1. Structure

### 1.1 Honeycomb (fast) — `structure/honeycomb.py`
Identical hexagonal tubes. Inputs: pore size d (inner flat-to-flat width), wall thickness t, wall density ρ_wall, and the test conditions T and p used by every other row.

- pitch (centre to centre): **p = d + t**
- porosity: **φ = (d/p)²**. A hexagon's area grows with the square of its flat-to-flat width, so pore area / cell area = (d/p)².
- bulk density: **ρ_bulk = (1 − φ) ρ_wall**. Only the walls have mass.

Porosity and density always follow from d and t; they are never inputs (meeting constraint, PLAN.md §0a).

Defaults: d = 30 µm (literature, Chan et al. 2022), t = 0.27 µm (derived: gives φ ≈ 0.982 as in Chan 2022), ρ_wall = 20.2/0.018 ≈ 1122 kg/m³ (derived from the density 20.2 kg/m³ at φ = 0.982 in Chan 2022), T = 300 K and p = 101.325 kPa (chosen test conditions).

### 1.2 Honeycomb + defects (detailed) — `structure/honeycomb_defects.py`
The same honeycomb drawn as a pixel picture of a 4 × 4 block of cells that repeats like wallpaper, with seeded random defects:
- **spread**: each cell centre is shifted at random (std. dev. as % of the pitch), so cells come out with different sizes;
- **wall_var**: each wall gets its own thickness, t·(1 + wall_var·N(0,1)), at least 0.1 t;
- **cracks**: every wall gets one gap, cracks × wall length long, at a random place along it.

How a pixel is drawn: it belongs to its nearest cell centre (a); the wall it is closest to is the perpendicular bisector between a and the second-nearest centre (b). The distance from the pixel to that wall is (r_b² − r_a²)/(2|c_b − c_a|). The pixel is wall if that distance is below half the drawn wall thickness.

**Shortcut (documented in the code):** real walls are t/d ≈ 0.009 thin. To draw them 4 pixels wide we would need about 400 pixels per cell. Instead each wall is drawn **4 px wide** (100 px per cell, so 1.2 µm instead of 0.27 µm), and each wall pixel holds the real wall plus the air it displaced *side by side*: its solid fraction is s = t/t_draw. Along the wall the two conduct in parallel, so the wall conductance t·k_wall is kept exactly. Why 4 px and not 2: on a square grid a 2-px wall at ±30° becomes a thin staircase that conducts only about 60 % of what it should (checked: a single 2-px band at 30° carries 0.64 of its true heat; 4 px carries 0.83 alone, and within 3 % in the honeycomb with the periodic solver below).

Porosity is **counted**: φ = 1 − mean(s). The ideal picture gives φ = 0.9825 against the formula's 0.9822.

---

## 2. Solid conduction

### 2.1 Formula (fast) — `solid/formula.py`
- **Along z:** the walls are straight strips parallel to the heat flow, side by side with the air, like resistors in parallel: **k_solid,∥ = (1 − φ) k_wall**.
- **Across:** a hexagonal network of thin walls has walls in three directions, 0°, 60° and 120° to the heat flow. A thin wall at angle θ carries heat only along itself, so it contributes in proportion to cos²θ (one cos for the share of the temperature gradient along the wall, one for the share of its heat flow in the flow direction). The average of cos² over 0°, 60°, 120° is (1 + ¼ + ¼)/3 = ½: **k_solid,⊥ = ½ (1 − φ) k_wall**. This is the 2D version of the ⅓ factor for thin-strut foams (Collishaw & Evans 1994).

k_wall = 4.0 W/m·K, **derived**: back-calculated from Chan et al. 2022 (Kit's paper), Nat. Commun. 13:5553: k_wall = (k_axial − φ k_air)/(1 − φ) with k_axial ≈ 5.8 × 16.9 mW/m·K and φ = 0.982, i.e. (98.0 − 25.8)/0.018 mW/m·K ≈ 4.0 W/m·K.

### 2.2 Pixel FV (detailed) — `solid/pixel_fv.py`
Every pixel is a small resistor. Each pixel's conductivity is k = s·k_wall + (1 − s)·k_gas, where k_gas comes from the Gas row (one number, or the per-pixel map from Local Kn). Between two neighbouring pixels the conductance is the **harmonic mean** 2k_i k_j/(k_i + k_j): two half-pixel resistors in series. Square pixels and unit depth make a face conductance equal to the face conductivity.

**Energy balance at every pixel:** heat in = heat out, Σ_neighbours G_ij (T_j − T_i) = 0. This is one linear equation per pixel, solved with `scipy.sparse.linalg.spsolve` (finite-volume method, Patankar 1980).

**Boundary condition: periodic.** The picture repeats like wallpaper, and the temperature drops by ΔT = 1 K per copy in x: the link from the last column to the first column (of the next copy) carries G (T_last − T_first + 1 K). One extra link from pixel 0 to 0 K only fixes the arbitrary temperature level; it carries no heat. Then k⊥ = Q L / (A ΔT), with Q the heat crossing one vertical cut, L the block length and A its height × unit depth. The same is done along y (the picture transposed); k⊥ is the mean of the two.

*Deviation from the brief, on purpose:* the brief suggested fixed temperatures on two sides and insulated other sides. On a 4 × 4 block that gave k⊥ about 5 % lower (9 % in x) because of the cut cells at the edges, and 2 × 2 cells gave a different answer from 4 × 4. The periodic version gives the same answer for 2 × 2 and 4 × 4 cells, which is the standard way to get the conductivity of a repeating structure (Build_Brief §3 allows periodic or fixed-temperature, if stated).

- **Along z:** k∥ = mean pixel k. Exact for straight channels (all pixels in parallel).
- **Checks (tests):** ideal honeycomb within 5 % of φ k_gas + ½(1 − φ) k_wall (it is 2.4 % low: k_x 57.6, k_y 60.8, mean 59.2 vs 60.6 mW/m·K; the difference in x and y is the ±30° pixel staircase); energy balance |Q_in − Q_out|/Q_in ≈ 1e-12; 2× finer grid changes k⊥ by < 3 %; a uniform picture gives exactly k; two layers in series and in parallel give the textbook values.
- **What it adds:** cracks. 5 % of every wall cut out lowers k⊥ from 59.2 to 45.4 mW/m·K (−23 %) at almost the same porosity, while k∥ barely moves (−4 %). The formula cannot see this.

---

## 3. Gas conduction

### 3.1 Knudsen (fast) — `gas/knudsen.py`
- Free air conductivity k_air(T): linear interpolation in Incropera Table A.4 (250 K 22.3, 300 K 26.3, 350 K 30.0, 400 K 33.8 mW/m·K).
- Mean free path of air molecules (kinetic theory): **λ = k_B T / (√2 π d_g² p)**, d_g = 3.72 × 10⁻¹⁰ m → λ ≈ 66 nm at 300 K, 1 atm.
- Knudsen number **Kn = λ/d**. When the pore is not much bigger than λ, molecules hit the walls more often than each other and the gas conducts less (Kaganer 1969; Zeng, Hunt & Greif 1995):
  **k_gas = k_air / (1 + 2βKn)**, **β = ((2 − α)/α) · (2γ/(γ + 1)) / Pr** = 1.643 for α = 1 (full accommodation, hypothetical), γ = 1.4, Pr = 0.71.
- Contribution φ·k_gas in both directions (thin-wall limit: the air fills a fraction φ of the cross-section and the walls are too thin to block it).

At 30 µm, Kn ≈ 0.002 and the reduction is below 1 %. Lower the pressure in the Structure row to see vacuum insulation (at 1 kPa, Kn ≈ 0.22, k_gas drops by about 40 %).

### 3.2 Local Kn (detailed) — `gas/local_knudsen.py`
The Knudsen formula pixel by pixel, with the **local pore size**: the diameter of the largest circle that fits in the pore and covers the pixel (the "local thickness"). It is found with distance transforms: for a growing radius r, the pixels at least r from a wall can be circle centres, and every pixel within r of such a centre lies inside a circle of diameter 2r. The picture is padded with its neighbouring copies so edge pixels see their real walls. Narrow cracks and corners get a small size and conduct less; the result is a map of k_gas (shown on the 3D top), its area mean is the gas term, and Pixel FV uses the map if this was the last gas run.
- **Check:** wide uniform pores give the fast value within 1 % (25.95 vs 26.11 mW/m·K; the drawn walls are 1.2 µm thick, so the drawn pores are a little narrower); at 1 kPa within 10 % and lower (corners).

### 3.3 Monte Carlo (detailed) — `gas/monte_carlo.py`
Virtual molecules start at random points in the pores and fly in random 3D directions (the channels run along z). Each straight flight is followed both ways to the first wall, giving a chord ℓ. The **mean chord** of the pore space is ℓ̄ = 1/mean(1/ℓ): a random point lies on a long chord more often than on a short one, and the harmonic mean removes that bias, giving Cauchy's ℓ̄ = 4V/S. The wall-collision length of a molecule is ℓ̄ (Zeng et al. 1995 use the same S/(4φ) term). Two parallel plates a gap d apart have ℓ̄ = 2d, so the equivalent plate gap is **d_eff = ℓ̄/2** and **k_gas = k_air / (1 + 2βλ/d_eff)**.

*Deviation from the brief, on purpose:* the brief proposed k_gas = k_air·λ_eff/λ with λ_eff the mean of free paths cut short by walls. Tested on parallel plates this disagrees with the Knudsen formula by +3 % at Kn = 0.01, +26 % at Kn = 0.1 and a factor 5.5 at Kn = 10, because it has no accommodation (temperature-jump) physics. The chord version reproduces the Knudsen formula for parallel plates exactly (test: within 3 % for Kn = 0.01–10, limited by Monte Carlo noise) and, with no walls, gives k_air (λ_eff → λ).
- **Honest note:** a smooth hexagonal channel has ℓ̄ = d (4A/P), so d_eff = d/2: the gas "feels" half the pore size, twice the Knudsen effect of the fast formula, which treats d as a plate gap. On the pixel picture the staircase walls shorten ℓ̄ by about 10 % more (a circle test gives 0.89 of 4V/S). At 30 µm and 1 atm this changes k_gas by < 1 %; it matters only at low pressure or for nanopores.

---

## 4. Radiation

### 4.1 Opaque (fast) — `radiation/opaque_walls.py`
Each pore is a gap of width d between two opaque grey walls. The net exchange between two large grey plates is σ(T₁⁴ − T₂⁴)/(2/ε − 1) (Incropera, radiation exchange). For a small difference, T₁⁴ − T₂⁴ ≈ 4T³ΔT, so per unit gradient: **k_rad = 4σT³ d ε/(2 − ε)**. ε = 0.9 is hypothetical. The same value is used along and across the channels (first approximation).

### 4.2 Rosseland (fast) — `radiation/rosseland.py`
If the material absorbs and scatters infrared strongly, radiation moves in many short steps and behaves like conduction: **k_rad = 16 n²σT³/(3 e ρ_bulk)** (Hrubesh & Pekala 1994), with e the specific extinction (m²/kg, hypothetical: unknown for BN/CNF/MTMS) and n = 1. Only valid if the sample is optically thick: **τ = e ρ_bulk L** must be well above 1; a warning is shown when τ < 3. At the defaults (e = 30 m²/kg, L = 3 mm) τ = 1.8, so Rosseland is *not* valid there; the warning says so.

### 4.3 Ray tracing (detailed) — `radiation/ray_tracing.py`
Photon bundles enter slabs of the pixel picture ¼, ½, 1, 2 and 4 cells thick, with diffuse (Lambertian) directions. In a pore a bundle flies straight. At a wall surface it is reflected with probability R, absorbed inside the wall with probability (1 − R)(1 − e^(−κ t)), or passes through. Each bundle ends transmitted, reflected back out, or absorbed, so **transmitted + reflected + absorbed = 1** for every slab (checked). The transmitted fraction against slab thickness is fitted with Beer's law T(L) = e^(−βL) → extinction β of this structure (Randrianalisoa & Baillis 2014 review ray tracing as the main method for foams). Then:
- βL_s ≥ 3 (optically thick): Rosseland with the computed β, **k_rad = 16σT³/(3β)**;
- otherwise: the two-flux (Schuster–Schwarzschild) slab between black walls, **k_rad = 4σT³ L_s/(1 + ¾ βL_s)**. It tends to 4σT³L_s for an empty gap and to the Rosseland value for a thick slab. (Note: at βL_s = 3 the two formulas differ by ≈ 30 %; the brief's rule is kept as written.)
- **Shortcuts (in the code):** rays stay in the 2D cross-section (real rays also travel along z); absorption uses the normal-incidence path t (not t/cosθ); a reflected bundle leaves in a random direction because a pixel wall has no clean normal; bundles still flying after 20 000 steps (almost parallel to the slab face) are counted as absorbed and reported.
- **Checks:** an empty slab transmits everything; energy is conserved; with opaque walls (κ → ∞, R = 0.1 so ε = 0.9) it gives 0.144 mW/m·K against 0.150 from the Opaque formula. At the defaults (κ = 10⁶ 1/m, hypothetical) β ≈ 1.8 × 10⁴ 1/m and k_rad ≈ 0.46 mW/m·K.

---

## 5. Convection

### 5.1 Rayleigh (fast) — `convection/rayleigh.py`
Buoyancy pushes warm air up; viscosity and heat diffusion hold it still. Their ratio for one pore is the Rayleigh number **Ra = g β_T ΔT d³/(ν α)**, with β_T = 1/T (ideal gas), ΔT = (dT/dx)·d across one pore, and ν = 15.89 × 10⁻⁶, α = 22.5 × 10⁻⁶ m²/s for air at 300 K (Incropera Table A.4; not varied with T: a shortcut). A fluid layer heated from below starts to move only above **Ra ≈ 1708**. At d = 30 µm and dT/dx = 1000 K/m (hypothetical), Ra ≈ 7 × 10⁻⁸, so **k_conv = 0**, with the reason printed. Foam literature agrees: no convection in cells below about 3–4 mm (Skochdopole 1961, via NIST NBSIR 82-1664). Above 1708 the formula cannot give a value: it still returns 0 with a warning to run Lattice Boltzmann.

### 5.2 Lattice Boltzmann (detailed) — `convection/lattice_boltzmann.py`
The air in one pore is simulated as a layer heated from below (T = 1 at the bottom, 0 at the top) at the pore's real Ra and Pr = 0.71. Lattice Boltzmann works with "particle" populations f_k on a grid: each step they **stream** one node along their direction and **collide**, relaxing towards a local equilibrium: f_k ← f_k − (f_k − f_k^eq)/τ. D2Q9 (9 directions) carries the flow, D2Q5 (5 directions) the temperature. The relaxation times follow from viscosity and diffusivity: τ = 3ν + ½, τ_T = 3α + ½. Buoyancy is the Boussinesq force ρ gβ (T − T_mean) upward. Walls use half-way bounce-back (flow) and anti-bounce-back (fixed temperature). The Nusselt number compares the heat carried with pure conduction: **Nu = 1 + ⟨v T⟩ H/(α ΔT)**, and **k_conv = (Nu − 1) φ k_gas**. Lattice speeds are kept below 0.1 (low Mach). Values of Nu − 1 below 10⁻⁹ are round-off and shown as 0.
- **Shortcut:** a layer with periodic sides (width 2H, the classic Rayleigh–Bénard set-up of Shan 1997), not the hexagonal pore. Real side walls only delay the onset, so this is on the safe side.
- **Checks (test marked slow):** Ra = 1000 and 1500 give Nu = 1.0000; Ra = 5000 gives Nu = 2.09 and Ra = 10 000 gives 2.62 (published Rayleigh–Bénard values at Pr ≈ 0.7 are about 2.1 and 2.6). The physical pore (Ra ≈ 7 × 10⁻⁸) gives Nu = 1 and k_conv = 0.

---

## 6. Material (placeholder) — `material/placeholder.py`
Reserved for a future material simulation; not decided yet. It contributes nothing to k_total.

---

## 7. Worked example at the defaults (all fast methods)

Inputs: d = 30 µm, t = 0.27 µm, k_wall = 4.0 W/m·K, T = 300 K, p = 101 325 Pa, α = 1, ε = 0.9, dT/dx = 1000 K/m.

| Step | Calculation | Result |
|---|---|---|
| pitch | p = 30 + 0.27 | 30.27 µm |
| porosity | φ = (30/30.27)² | **0.98224** |
| bulk density | (1 − 0.98224) × 1122 | 19.9 kg/m³ |
| solid ∥ | (1 − φ) k_wall = 0.017760 × 4.0 | **71.0 mW/m·K** |
| solid ⊥ | ½ × 71.04 | **35.5 mW/m·K** |
| k_air(300 K) | Table A.4 | 26.3 mW/m·K |
| mean free path | 1.380649e-23 × 300 / (√2 π (3.72e-10)² × 101 325) | 66.5 nm |
| Knudsen number | 66.5 nm / 30 µm | 0.00222 |
| β | (2 × 1.4/2.4)/0.71 | 1.643 |
| k_gas | 26.3/(1 + 2 × 1.643 × 0.00222) | 26.1 mW/m·K |
| gas term | φ k_gas = 0.98224 × 26.11 | **25.6 mW/m·K** |
| radiation | 4 × 5.670e-8 × 300³ × 30e-6 × 0.9/1.1 | **0.150 mW/m·K** |
| Rayleigh | 9.81 × (1/300) × (1000 × 30e-6) × (30e-6)³ / (15.89e-6 × 22.5e-6) | 7.4 × 10⁻⁸ → **k_conv = 0** |
| **k⊥** | 35.5 + 25.6 + 0.150 + 0 | **61.3 mW/m·K** |
| **k∥** | 71.0 + 25.6 + 0.150 + 0 | **96.8 mW/m·K** |
| **anisotropy** | 96.8/61.3 | **1.58** |

`.agent/tests/test_hand_numbers.py` recomputes this table independently of the code and checks it to 12 digits.

**Pixel FV at the defaults** (ideal picture, Knudsen gas): k⊥ = (solid+gas) 59.2 + 0.150 + 0 = **59.3**, k∥ = 95.8 + 0.150 = **95.9 mW/m·K**, anisotropy **1.62**. With 5 % cracks: k⊥ = **45.6**, k∥ = **92.4**, anisotropy **2.03**.

**Measured, for comparison (trends, not a fit):** Chan et al. 2022 report k⊥ = 16.9 mW/m·K and anisotropy ≈ 5.8. That k⊥ is *below* the air-only floor (≈ 26 mW/m·K at 1 atm), so no model of air-filled micron channels can reach it; candidate causes are the test method on anisotropic samples and nanoporous walls. The tool reports this gap and does not tune inputs to hide it. Cracks raise the anisotropy (1.58 → 2.03 at 5 %), in the direction of the measurement.

## 8. Pore-size sweep (`python -m aerosim sweep` → `results/sweep.csv`, fast methods)
- **A, t fixed (headline):** bigger pores, same walls → φ rises, k falls (k⊥ 222 → 31 mW/m·K from d = 5 to 500 µm).
- **B, pitch fixed (headline):** walls thin out as d grows towards p.
- **C, φ fixed (diagnostic only, it prescribes porosity):** only the Knudsen and radiation terms depend on d, so k⊥ barely changes (60.3 → 63.8 mW/m·K from 5 to 500 µm). Pore size matters through porosity, not through size alone.

## Sources
- Hrubesh, L.W. & Pekala, R.W. (1994) *J. Mater. Res.* 9(3):731–738 — solid/gas/radiative split; Rosseland for aerogels.
- Lou, F. et al. (2023) *Gels* 9(3):220 — review of heat transfer in aerogels.
- Kaganer, M.G. (1969) *Thermal Insulation in Cryogenic Engineering* — Knudsen gas conduction.
- Zeng, S.Q., Hunt, A.J. & Greif, R. (1995) *J. Heat Transfer* 117:758–761 — gas in porous media, wall-collision mean free path.
- Collishaw, P.G. & Evans, J.R.G. (1994) *J. Mater. Sci.* 29:2261 — cellular conduction models, strut factor.
- Skochdopole, R.E. (1961) *Chem. Eng. Prog.* 57(10):55, via NIST NBSIR 82-1664 — convection negligible below ≈ 3–4 mm cells.
- Incropera, F.P. et al. *Fundamentals of Heat and Mass Transfer* — air table A.4, grey-plate exchange, Rayleigh–Bénard onset.
- Chan, K.-Y. et al. (2022) *Nat. Commun.* 13:5553 — 30 µm pores, φ 0.982, 20.2 kg/m³, k⊥ 16.9 mW/m·K, anisotropy ≈ 5.8.
- Randrianalisoa, J. & Baillis, D. (2014) *C. R. Physique* 15:683 — ray tracing for foam radiation.
- Shan, X. (1997) *Phys. Rev. E* 55:2780 — LBM Rayleigh–Bénard.
- Mohamad, A.A. *Lattice Boltzmann Method* (Springer) — student-level LBM codes.
- Patankar, S.V. (1980) *Numerical Heat Transfer and Fluid Flow* — finite-volume method.
