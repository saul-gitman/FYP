# Aerogel simulator: build plan (v1, revised 2026-11-15)

Status: **plan only, nothing built yet.** This replaces the v0 plan (2026-10-29). The v0 plan made a finite-volume (FV) solver the core. This version swaps that for a set of short, readable formulas, one heat-transfer path per file. It also adds a 3D web UI.
Project: *Thermo-optically functional CFRP laminates for lightweight electrified systems* (PolyU AAE capstone 2026/27, supervisor Dr CHAN Kit-Ying).

## 0. What changed from v0, and why

| v0 plan | v1 plan | Reason |
|---|---|---|
| 2D finite-volume solver as the core | **Closed-form formulas**, one file per heat path | A 4th-year mechanical student must be able to read and defend every line. The formulas are the ones aerogel papers actually use. |
| Periodic homogenisation, 2×2 tensor, grid refinement, Hashin–Shtrikman bounds | Dropped from v0.1 | Too heavy for the interim report, and they add nothing to the *trends* the supervisor wants |
| One cell type (thin-wall hex honeycomb) | **Two cell types that bracket reality:** honeycomb (walls connected across) and lamellar (parallel sheets) | Freeze-cast walls are partly connected. The two shapes give an upper and a lower case for k_transverse. |
| No UI until later | **Simple HTML page with a three.js 3D cell**, sliders, bar chart, live equations | Required: the UI must show *what is changing* |
| Wall k from an EMT band | **One wall-k input**, default back-calculated from a published axial value and labelled as such | Simple, honest, and replaceable once there is project data |

## 1. One-paragraph summary

The tool predicts how well a freeze-cast aerogel conducts heat **along** its channels (k_par) and **across** them (k_trans) from its structure: pore size, wall thickness, cell type, temperature and gas pressure. It treats heat transfer as **separate paths that add up**, the standard approach in the aerogel literature (Hrubesh & Pekala 1994; Lou et al. 2023):

```
k_eff = k_solid   (conduction through the walls)
      + k_gas     (conduction through the air in the pores)
      + k_rad     (thermal radiation across the pores)
      + k_conv    (convection of the air: shown to be ≈ 0, with a printed reason)
```

This is your "simulate the three modes separately" idea. Conduction is split into solid and gas because they behave very differently in an aerogel. A 3D web page shows the cell changing shape as you move the sliders, and a bar chart shows how much each path contributes.

## 2. Is this a solid plan for an FYP? (honest assessment)

**Yes.** Splitting heat transfer into solid, gas, radiation and convection terms is the main framework in aerogel thermal research, not a student shortcut:
- Hrubesh & Pekala (1994) split heat transport in porous materials into solid, gaseous and radiative parts.
- The *Gels* reviews (Lou et al. 2023; a 2023 thermal-protection review) describe the same three modes.
- Collishaw & Evans (1994) note that most foam models neglect convection.

So the plan is defensible to examiners, and each term can be checked by hand.

**Known weaknesses (write them in the report, don't hide them):**
1. **The terms are not perfectly independent.** Gas next to a solid contact can bridge it ("coupling"). Simple addition ignores this. It matters most for nano-scale pores and little for 30 µm channels.
2. **Convection isn't really simulated.** It is calculated (Rayleigh number) and shown to be negligible. That is a correct and standard result, but say it plainly.
3. **Radiation has the least certain input.** The infrared extinction of BN/CNF walls is unknown, so it is a hypothetical input you sweep.
4. **The model cannot reach sub-air values.** Measured k_trans values below air (e.g. 16.9 mW/m·K in Chan et al. 2022) are below what *any* model of 30 µm air-filled channels at 1 atm can give, because the gas term alone is ≈ 26 mW/m·K. The tool compares **trends and anisotropy** and reports this gap with its candidate causes (test method on anisotropic samples, nanoporous walls). It does not tune inputs to hide it.

## 3. Scope by version

| Version | Content | Target |
|---|---|---|
| **v0.1 core** | Four heat-path modules, two cell types, two directions, pore-size sweep (modes A/B/C), web UI with 3D cell, CSV/JSON + figures for the report | **Interim report, 21 Dec 2026** |
| v0.2 | Composition → wall k and density (rule of mixtures, dry mass basis), sensitivity ("which input matters most") chart | Jan 2027 |
| v1.0 | Through-thickness laminate stack as thermal resistances in series (aerogel / CFRP / interlayer / CFRP), heater and solar load cases | Feb–Mar 2027 |

Out of scope: mechanics, spectral optics (reflectance is a measured *input*), processing → structure (no invented freezing-temperature-to-pore-size law), CFD/FV solvers.

## 4. Backend: the physics, one file per path

Every module is a few short functions. Each has a docstring with (1) the equation, (2) what it means in plain words, (3) the source. All of this is also written up in `docs/PHYSICS.md`.

### 4.1 `geometry.py`: what the structure looks like
Inputs: pore size **d**, wall thickness **t**, cell type. Pitch p = d + t.

| Cell type | Picture | Porosity φ | Meaning |
|---|---|---|---|
| Honeycomb (hexagonal) | hollow hex tubes along z | φ = (d/p)² | walls are connected across the channels (supervisor's "hollow cell with homogeneous wall") |
| Lamellar | parallel sheets along z | φ = d/p | walls are *not* connected across (the extreme case; freeze-casting often gives sheets) |

Density follows from porosity and is never set separately: ρ_bulk = (1 − φ) ρ_wall.
Check: d = 30 µm and t = 0.27 µm give honeycomb φ ≈ 98.2 %, which matches the literature anchor.

### 4.2 `solid.py`: conduction through the walls
- **Along z (both cell types):** the walls are straight rods/sheets parallel to the heat flow, so they act like resistors in parallel:
  `k_solid,par = (1 − φ) · k_wall`
- **Across, honeycomb:** a hexagonal network of thin walls is isotropic in-plane, and only the wall component along the heat flow carries heat. Averaging cos² over the wall directions (0°, 60°, 120°) gives ½:
  `k_solid,trans = ½ (1 − φ) · k_wall`
  This is the 2D version of the well-known thin-strut foam result (⅓ in 3D, Lemlich/Glicksman; see Collishaw & Evans 1994). The derivation is short and goes in PHYSICS.md.
- **Across, lamellar:** heat must cross sheet → air → sheet in series, so the solid gives no separate parallel path. The gas and the sheets form a series resistance:
  `k_trans = 1 / ( φ/k_gas + (1−φ)/k_wall )`. This is the classic series model, used for freeze-cast lamellar ceramics with series/parallel resistance models.
- `k_wall` is the conductivity of the wall material itself. Default: back-calculated from Chan et al. 2022: `k_wall = (k_axial − φ k_air)/(1 − φ) ≈ (98 − 25.8)/0.018 mW/m·K ≈ 4 W/m·K`, where k_axial ≈ 5.8 × 16.9 mW/m·K. It is labelled **derived (from a different material, BNNS/WPU)** and is a slider in the UI.

### 4.3 `gas.py`: conduction through the air in the pores
- Free air conductivity at temperature T: interpolated from the standard air property table (Incropera, *Fundamentals of Heat and Mass Transfer*, Table A.4), ≈ 26.3 mW/m·K at 300 K.
- Mean free path of air molecules: `λ = k_B T / (√2 π d_g² p)` ≈ 66 nm at 300 K, 1 atm (kinetic theory).
- Knudsen number `Kn = λ / d`. When the pore is not much bigger than λ, molecules hit the walls more often than each other, and gas conduction drops (Kaganer 1969; Zeng, Hunt & Greif 1995):
  `k_gas = k_air / (1 + 2 β Kn)`, with β ≈ 1.6–2 for air (a cited value, set in the config).
- Contribution: along z the gas is in parallel, `φ · k_gas`. Across the honeycomb it is ≈ `φ · k_gas` (thin-wall limit). Across the lamellar cell it is inside the series formula above.
- **Expected result:** at d = 30 µm, Kn ≈ 0.002, so the reduction is below 1 %. The **pressure slider** makes the effect visible: at low pressure λ grows and k_gas falls. This is how vacuum insulation works, and it is a good teaching point for the report.

### 4.4 `radiation.py`: thermal radiation across the pores
Two options, chosen in the config/UI, both standard:
1. **Opaque walls (default):** each pore is a gap between two grey surfaces, like parallel plates (Incropera radiation-exchange chapter):
   `k_rad = 4 σ T³ d · ε / (2 − ε)`. Bigger pores and hotter samples give more radiation. At 30 µm and 300 K this is ≈ 0.2 mW/m·K, i.e. small.
2. **Semi-transparent walls (Rosseland diffusion):** used for aerogels in Hrubesh & Pekala 1994 and in the Lou et al. 2023 review:
   `k_rad = 16 n² σ T³ / (3 e ρ_bulk)`, where e is the *specific extinction* (m²/kg).
   **Valid only if the sample is optically thick:** τ = e ρ_bulk L ≫ 1. The tool computes τ and shows a warning when τ < ~3. e for BN/CNF is unknown, so it is a hypothetical slider. CNT would raise e strongly (v0.2 comment only).
- No double counting with radiation from the outer surfaces of the panel (that belongs to the laminate model).

### 4.5 `convection.py`: why convection is ≈ 0
- Compute the Rayleigh number of one pore: `Ra = g β_T ΔT_pore d³ / (ν α)`, with ΔT_pore = (temperature gradient) × d.
- Natural convection in an enclosure needs Ra above about 10³ (≈ 1708 for a heated horizontal layer, Incropera). For a 30 µm pore Ra is many orders of magnitude smaller.
- Supporting literature: convection in foams is negligible for cells below about 3–4 mm (Skochdopole 1961, as cited by NIST NBSIR 82-1664 and Collishaw & Evans 1994).
- Output: `k_conv = 0`, plus the printed Ra value and the reason. The UI shows the convection bar at zero with a tooltip giving the Ra value.

### 4.6 `model.py`: add it up
```
k_par   = (1−φ)k_wall + φ k_gas + k_rad (+0)
k_trans = honeycomb: ½(1−φ)k_wall + φ k_gas + k_rad
          lamellar : 1/(φ/k_gas + (1−φ)/k_wall) + k_rad
anisotropy = k_par / k_trans
```
It returns every term separately (that is what the bar chart shows), plus φ, ρ, Kn, Ra, τ and the warnings.

**Expected first result (worth reporting early):**
- At the Chan-like defaults, honeycomb gives k_trans ≈ 60 mW/m·K and anisotropy ≈ 1.6.
- Lamellar gives k_trans ≈ 27 mW/m·K and anisotropy ≈ 3.7.
- Measured anisotropy is ≈ 5.8.

So the measured aerogel insulates across the channels better than even the "no connection" lamellar case. This points to poorly connected walls in the transverse direction, which matches reports that radial walls are less interconnected than axial ones, *and* to the measurement issue in §2. This is a real finding to show the supervisor, not a bug.

### 4.7 `sweep.py`: pore-size study (the first deliverable)
Three ways to change d (the user picks; the UI has a toggle):

| Mode | Held fixed | What happens as d grows | Physical meaning |
|---|---|---|---|
| A | wall thickness t | φ rises, ρ falls, k falls | "bigger holes, same walls" (the supervisor's wording) |
| B | pitch p | walls thin out | fixed cell spacing |
| C | porosity φ | only the scale changes | same slurry, different freezing speed (closest to the experiment) |

Key insight to explain: **in mode C only radiation and Knudsen depend on d**, so k barely changes in air at 1 atm. Pore size matters through porosity (mode A), not through size alone. Recommendation: show **A and C side by side** in the interim report.

### 4.8 Inputs and provenance
One YAML config (`configs/default.yaml`). Every input has `value, unit, source, status` with status ∈ {measured, literature, derived, hypothetical}. The UI shows the status as a coloured tag next to each slider. The report lists every input in a table. A result is never called "calibrated" while a dominant input is hypothetical.

### 4.9 Code size and dependencies
- Level 1: Python 3, NumPy + Matplotlib (figures) + PyYAML. Runs in milliseconds.
- Level 2 adds SciPy (sparse solve, `ndimage`), Pillow (SEM images) and, optionally, Numba (faster Monte Carlo).
- Target: about 400–600 lines for Level 1, and about 150–250 lines per detailed method. Every function is short enough to read in one sitting.

## 4b. Level 2: detailed simulations (more CPU, more realistic)

**Idea:** each of the four heat-path files has two functions:
- `fast_...()`: the Level 1 formula above. Instant, and drives the live UI sliders.
- `detailed_...()`: a real simulation on a picture of the structure. Seconds to minutes, started with a "Run detailed" button or `python -m aerosim detailed`.

**Rule:** every detailed method must first **reproduce its Level 1 formula in the ideal case** (a test), and only then be used where the formula cannot go (cracks, irregular cells, thin samples, real SEM images). That makes each one academically defensible: "verified against the textbook limit, then extended".

**Check already done (2026-11-15, scratch prototype, solid file):**
- On ideal thin-walled cells, the pixel solver matched the ½ formula to 1 %, and a grid twice as fine changed nothing.
- A crack only ~1 % of the wall length wide cut k_trans by 21 % at the same porosity, which the formula cannot see.
- So the extra CPU pays off only when it is spent on **realistic structure**, not on finer grids of the ideal cell.

### 4b.0 `structure.py`: the picture every detailed method uses (new, shared)
Makes a 2D cross-section image (and a 3D voxel block by extruding it), where each pixel is *wall* or *pore*:
- **Synthetic, realistic:**
  - Voronoi cells with a pore-size *distribution* (mean d, spread σ_d) instead of identical hexagons
  - wall-thickness variation
  - **crack/gap fraction**: walls broken in the transverse direction, the key unknown found above
  - optional bridges and channel tilt in 3D (dendritic bridges are typical of freeze-casting)
- **Real:** load a thresholded **SEM cross-section** (black = wall, white = pore) with a µm-per-pixel scale. This becomes the main input once the lab has images.
- **Outputs:** porosity (counted, not assumed), pore-size histogram (distance transform, `scipy.ndimage`), wall connectivity.
- **Provenance:** synthetic parameters (σ_d, crack fraction) are *hypothetical* until measured from SEM.

### 4b.1 `solid.py` → `detailed_conduction()`: pixel finite-volume conduction
- **Method:** every pixel is a small resistor. Energy balance at each pixel (heat in = heat out), harmonic-mean conductance between neighbours, fixed ΔT on two sides, insulated on the others. Sparse linear solve (`scipy.sparse`). The same finite-difference idea as heat-conduction coursework.
- **Pore pixels** use the *local* gas conductivity from 4b.2, so **gas–solid coupling is included**: air in a 0.3 µm crack still carries heat, but less than free air. Simple addition misses exactly this effect, which the literature says can be about 30 % for some silica aerogels.
- **Directions:** k_trans in x and y from the 2D image (also tests in-plane isotropy). k_par from a 3D voxel run when tilt or bridges are on; otherwise the exact parallel formula holds.
- **Gives:** k_trans for real/irregular/cracked walls, the temperature field and heat-flux map (shown in the UI), and the anisotropy.
- **Verified by:**
  - ideal honeycomb vs the ½ formula (done, 1 %)
  - lamellar vs the series formula
  - grid refinement
  - energy balance (heat in = heat out)
- **CPU (estimates except the first):** 300×300 px ≈ 0.5 s (measured); 1000×1000 ≈ tens of s; 3D 200³ voxels with an iterative solver ≈ minutes.
- **Limit:** thin walls need ≥ 2–3 px across, so resolution is set by the SEM image. Hexagons on a square grid have small staircase errors (quantified by the refinement test).

### 4b.2 `gas.py` → `detailed_gas()`: Monte Carlo molecule paths
- **Method:** release many virtual air molecules at random points in the pore image. Each flies a random free path (exponential distribution with the free-air λ) in a random direction, and the path is cut short if it hits a wall first. The average gives the **effective mean free path in this geometry**, λ_eff. Kinetic theory gives k ∝ λ, so `k_gas,local = k_air · λ_eff/λ`. This is the idea behind Zeng, Hunt & Greif (1995), done numerically on the real shape.
- **Gives:**
  - a *map* of local gas conductivity: lower in narrow cracks and corners, ≈ free air in the 30 µm channels
  - a pore-size-distribution-averaged k_gas
  - a pressure sweep (vacuum behaviour)
  - **nanoporous walls**: run the same code on a wall-scale image to get the gas contribution *inside* the walls, where Kn is large and the effect is real
- **Verified by:** parallel-plate gap vs the Kaganer/Zeng formula over Kn = 0.01–10, and the free-space limit λ_eff → λ.
- **CPU (estimate):** 10⁶ molecules, NumPy-vectorised, ≈ seconds to a minute.
- **Not done:** full DSMC (molecule–molecule collisions, Bird's method). It is the "gold standard" but needless at Kn ≈ 0.002 in the channels, and it is research-level code.

### 4b.3 `radiation.py` → `detailed_radiation()`: Monte Carlo ray tracing
- **Method:** fire many "photon bundles" into a slab of the structure image. In a pore a ray goes straight. At a wall it is absorbed (probability from wall emissivity/absorption), reflected, or passes through a semi-transparent thin wall with probability exp(−κ_w t / cos θ). Count what gets through slabs of several thicknesses. Fit Beer's law, T(L) = exp(−βL), to get the **real extinction coefficient β** of the structure, plus the reflected fraction.
- **Then:**
  - if optically thick (βL ≳ 3): `k_rad = 16 n² σ T³ / (3β)` (Rosseland, now with a *computed* β instead of a guessed one)
  - if thin: solve the **two-flux (Schuster–Schwarzschild) slab model**, a simple 1D model of forward/backward radiation. The sample thickness then matters, as it does in the real test.
- **Why it is better:** it removes the biggest guess in Level 1 (the extinction e) and the "is Rosseland valid?" question, and it shows how pore size, wall thickness and CNT (higher wall absorption κ_w) change radiation. Ray tracing on foam geometry is the standard method for radiative properties of foams (Randrianalisoa & Baillis 2014 review; tomography-based foam studies).
- **Inputs still needed:** wall absorption κ_w and reflectance (hypothetical, swept; later from the measured reflectance spectra).
- **Verified by:** opaque walls vs the parallel-plate formula `4σT³dε/(2−ε)`; empty slab gives full transmission; energy conservation (absorbed + reflected + transmitted = 1).
- **CPU (estimate):** 10⁶ rays × tens of wall hits, vectorised ≈ minutes (optional Numba for speed).

### 4b.4 `convection.py` → `detailed_convection()`: lattice Boltzmann flow in one pore
- **Method:** a 2D lattice Boltzmann (LBM) solver: D2Q9 for the air flow plus a temperature lattice, with buoyancy from the Boussinesq approximation. It runs in one pore cross-section heated on one side. LBM is short (~80 lines of NumPy), and each step is "particles stream, then collide", easy to explain with a fluid-dynamics background.
- **Gives:** the Nusselt number Nu (Nu = 1 means pure conduction, i.e. no convection), so `k_conv = (Nu − 1)·φ·k_gas`. Then **sweep pore size from 30 µm up to ~10 mm** to find where convection starts. This turns the Level 1 "trust me, Ra is small" into your **own simulation** reproducing the literature onset (cells of about 3–4 mm, Skochdopole 1961).
- **Verified by:** the classic Rayleigh–Bénard onset at Ra ≈ 1708, the standard LBM benchmark.
- **CPU (estimate):** 200×200 lattice, 10⁴–10⁵ steps ≈ minutes per point.
- **Honest note:** the answer at 30 µm will be k_conv = 0. Its value is the *proof* and the onset curve, not a new number. The convection that really matters for the project is on the **outside** of the panel (heater and solar tests), in the v1.0 laminate model.

### 4b.5 How the detailed results combine
```
k_trans,detailed = FV conduction on the image (solid + local gas, coupling included)
                 + k_rad from ray tracing
                 + k_conv from LBM (≈ 0)
```
Radiation is still *added* to conduction, which assumes they don't interact much. Valid when k_rad is small; stated as a limitation.

### 4b.6 Does the extra CPU give better results? (expected, honest)
| File | Better than Level 1? | Why / why not |
|---|---|---|
| solid | **Yes, the biggest gain** | captures cracks, irregular cells, real SEM shape, and gas–solid coupling: the likely cause of the anisotropy gap (model 1.6 vs measured 5.8) |
| radiation | **Yes, a large gain** | replaces a guessed extinction with one computed from the structure; handles thin samples correctly |
| gas | Small in the channels, **large for nanoporous walls or reduced pressure** | Kn ≈ 0.002 at 30 µm in air |
| convection | No new number | gives a self-made proof and onset curve instead of a citation |

**What no amount of CPU fixes:** wall material k (BN-sheet contact resistance), wall optical properties, and measured values below the air floor. Those need lab data (SEM, reflectance, a measured k on project samples).

## 5. Front end: what the UI shows

**Goal: show which parameters change and what that does to heat flow.** No framework, no build step.

- **Files:** `web/index.html`, `web/app.js`, `web/style.css`. three.js is loaded from a pinned CDN version.
- **Data flow:** `python -m aerosim serve` starts a tiny standard-library HTTP server. When a slider moves, the page sends the inputs to `/api/compute` and draws what Python returns. **The physics lives only in Python**, so the UI can never disagree with the backend.

Layout (one screen):

```
┌───────────────┬──────────────────────────────┬────────────────────────┐
│ Inputs        │   3D cell (three.js)         │ Results                │
│ ─ cell type   │   block of channels along z  │ k_par, k_trans, ratio  │
│ ─ pore size d │   walls resize live          │ φ, ρ, Kn, Ra, τ        │
│ ─ wall t      │   arrows: heat along / across│ stacked bars:          │
│ ─ k_wall      │   arrow thickness ∝ k        │ solid|gas|rad|conv     │
│ ─ T, pressure │   toggle: show air / walls   │ for both directions    │
│ ─ radiation   │                              │                        │
│ ─ sweep mode  │                              │                        │
│ [status tags] ├──────────────────────────────┴────────────────────────┤
│               │ Sweep chart: k vs d (modes A/B/C), current d marked   │
│               │ Live equations: each formula with today's numbers in  │
└───────────────┴───────────────────────────────────────────────────────┘
```

- **3D cell:** a small 3×3 block of hex tubes (or stacked sheets for lamellar), extruded along z. Walls are drawn **thicker than real** (real t/d ≈ 0.01 would be invisible), with a note saying so. The block is coloured by solid vs air, can be rotated, and has two arrows (along / across) whose thickness scales with k.
- **Bars:** the four heat paths in fixed colours, used the same way across the UI, so the user sees at once that gas dominates across, solid dominates along, and radiation and convection are tiny.
- **Live equations:** each formula with the current numbers substituted. This links the UI directly to PHYSICS.md and the report.
- **"Run detailed" button (Level 2):** starts the slow simulations in the background with a progress bar. When done:
  - the 3D block is rebuilt from the *actual generated (or SEM) structure*, showing cracks and irregular cells
  - the top face shows the **temperature field** from the pixel solver as a colour map
  - each bar gets a second "detailed" bar next to the "formula" bar, so you see where the two disagree
  - small extra plots: Beer's-law fit (radiation), local gas-conductivity map (gas), Nu vs pore size (convection)
- Not included: user accounts, saving sessions, animation of individual molecules.

## 6. Verification (simple, hand-checkable)
1. **Limits:** φ → 0 gives k → k_wall (along); φ → 1 gives k → k_gas. Honeycomb k_trans always lies between the lamellar series value and the parallel value.
2. **Hand calculation:** one fully worked example in PHYSICS.md (d = 30 µm, t = 0.27 µm, 300 K, 1 atm), matched to the code by a test to 3 significant figures.
3. **Known numbers:** air mean free path ≈ 66–68 nm at 300 K/1 atm; k_air(300 K) from the table; Ra ≪ 1000 at 30 µm.
4. **Trend checks:** k_gas falls when pressure falls; k_rad rises with T³ and with d; in mode C only k_rad and k_gas change.
5. **Literature comparison table:** model vs Chan 2022 and Liu 2021 for k_par, k_trans and anisotropy, with the gap explained (§2, §4.6).
6. *(Optional, only if an examiner asks)* a small numerical grid check of the ½ honeycomb factor. Not in v0.1.

## 7. Proposed layout
```
aerosim/
  geometry.py    porosity, density, pitch
  structure.py   Level 2: synthetic Voronoi/cracked cells, or SEM image → pixel/voxel map
  solid.py       fast: wall conduction formulas   | detailed: pixel finite-volume (gas–solid coupled)
  gas.py         fast: air table, Knudsen         | detailed: Monte Carlo molecule free paths
  radiation.py   fast: opaque-wall + Rosseland    | detailed: Monte Carlo ray tracing → β → Rosseland / two-flux
  convection.py  fast: Rayleigh number            | detailed: lattice Boltzmann pore flow → Nu, onset size
  model.py       adds the paths, both directions
  sweep.py       modes A/B/C
  report.py      CSV/JSON + Matplotlib figures + report.md
  server.py      tiny HTTP server for the UI
  __main__.py    `python -m aerosim run|sweep|serve`
web/  index.html  app.js  style.css
configs/default.yaml
tests/
docs/PLAN.md  docs/PHYSICS.md  docs/COUNCIL_BRIEF.md
```

## 8. Timeline (about 5 weeks to the interim report)
| Week of | Milestone |
|---|---|
| 16 Nov | Backend modules + tests + PHYSICS.md with the worked example |
| 23 Nov | Web UI: sliders, 3D cell, bars, equations |
| 30 Nov | Sweeps A/B/C, report figures; **send first results to the supervisor** (S12: report even weak results) |
| 7–21 Dec | `structure.py` + detailed solid (pixel FV, crack sweep): the highest-value Level 2 item. Literature comparison, interim-report method chapter and figures |
| Jan 2027 | Detailed radiation (ray tracing) + detailed gas (Monte Carlo); first SEM images through the pixel solver if available; v0.2 composition |
| Feb 2027 | Detailed convection (LBM onset curve): lowest priority, cut first if time runs short |
| Feb–Mar 2027 | v1.0 laminate stack |

## 9. References (verify page numbers in the originals before citing)
- Hrubesh, L.W. & Pekala, R.W. (1994). Thermal properties of organic and inorganic aerogels. *J. Mater. Res.* 9(3), 731–738. doi:10.1557/JMR.1994.0731 (split into solid / gas / radiative parts)
- Lou, F. et al. (2023). Review of nanoscale heat transfer in aerogels. *Gels* 9(3), 220. doi:10.3390/gels9030220 (heat-transfer modes, test methods)
- Zeng, S.Q., Hunt, A.J. & Greif, R. (1995). Mean free path and apparent thermal conductivity of a gas in a porous medium. *J. Heat Transfer* 117(3), 758–761. doi:10.1115/1.2822642 (gas in pores)
- Kaganer, M.G. (1969). *Thermal Insulation in Cryogenic Engineering.* Israel Program for Scientific Translations (Knudsen gas formula)
- Collishaw, P.G. & Evans, J.R.G. (1994). An assessment of expressions for the apparent thermal conductivity of cellular materials. *J. Mater. Sci.* 29, 2261–2273. doi:10.1007/BF00363413 (foam conduction models, ⅓ strut factor, convection neglected) *(DOI/pages differ between databases: check)*
- Skochdopole, R.E. (1961). The thermal conductivity of foamed plastics. *Chem. Eng. Prog.* 57(10), 55 (convection negligible below about 3–4 mm cells; cited via NIST NBSIR 82-1664)
- Glicksman, L.R. (1994). Heat transfer in foams. In *Low Density Cellular Plastics*, Chapman & Hall (radiation in cellular materials) *(not yet checked)*
- Incropera, F.P. et al. *Fundamentals of Heat and Mass Transfer* (air property table A.4; enclosure convection; radiation exchange between surfaces)
- Chan, K.-Y. et al. (2022). Anisotropic thermally superinsulating boron nitride composite aerogel. *Nat. Commun.* 13, 5553. doi:10.1038/s41467-022-33234-8 (literature anchor: 30 µm pores, φ 98.2 %, 16.9 mW/m·K, anisotropy ≈ 5.8)
- Randrianalisoa, J. & Baillis, D. (2014). Thermal conductive and radiative properties of solid foams. *C. R. Physique* 15, 683–695. doi:10.1016/j.crhy.2014.09.002 (ray-tracing Monte Carlo as the main method for foam radiation; 3D image-based models) *(volume/pages to confirm)*
- Shan, X. (1997). Simulation of Rayleigh–Bénard convection using a lattice Boltzmann method. *Phys. Rev. E* 55, 2780 (arXiv:comp-gas/9612001) (LBM reproduces the onset Ra ≈ 1708)
- Mohamad, A.A. *Lattice Boltzmann Method: Fundamentals and Engineering Applications with Computer Codes.* Springer (student-level LBM codes) *(edition to confirm)*
- Bird, G.A. (1994). *Molecular Gas Dynamics and the Direct Simulation of Gas Flows.* Oxford (DSMC: referenced as the method *not* used, and why)
- Ice-templated anisotropic flame-resistant BN aerogels with CNF (2021). *ACS Appl. Polym. Mater.* (28.4 lateral / 83.3 axial mW/m·K) *(author list to confirm; previously cited as "Liu 2021")*

## 10. Decisions needed from the user (defaults in bold)
1. Headline sweep for the interim report: **A and C side by side**.
2. Default cell type in the UI: **honeycomb**, with lamellar as the comparison case.
3. Default radiation option: **opaque walls**, with Rosseland behind a toggle and an optical-thickness warning.
4. UI served by **a tiny local Python server** (physics stays in Python). The alternative is a static page with the formulas copied into JavaScript, which is easier to share but duplicates the physics.
5. Which Level 2 methods go before the interim report: **only detailed solid + `structure.py`**, the others in Jan–Feb.
6. Whether you can get SEM cross-section images of the lab samples (or the Chan 2022 figures) to feed the pixel solver. **This matters more than any extra CPU.**
