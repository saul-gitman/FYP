# Subagent guide: build the Aerogel k Simulator (v0.1)

Read this whole file before doing anything. **Part A is the complete context. Part B is the task.** The main assistant only checks your work, and the user wants to be minimally involved, so make sensible decisions yourself and record them.

---

# PART A: WHOLE CONTEXT

## A1. The project and the user
- **FYP:** *Thermo-optically functional CFRP laminates for lightweight electrified systems*, PolyU Aviation Engineering capstone 2026/27. Supervisor **Dr CHAN Kit-Ying** ("Kit"). Interim report **21 Dec 2026**, final report April 2027.
- **Final product:** a CFRP panel that spreads internal heat and reflects solar heat. Outside → inside stack: BN/CNF/MTMS freeze-cast aerogel surface → CFRP → CNT/CNF/MTMS aerogel interlayer → CFRP, heater on the back. (BN = boron nitride nanosheets, CNF = cellulose nanofibrils, CNT = carbon nanotubes, MTMS = methyltrimethoxysilane.)
- **Made by:** unidirectional freeze-casting (aligned channels along the freezing direction z), freeze-drying, then vacuum resin infusion.
- **Framework:** processing → structure → properties. **The simulator covers structure → properties only.**
- **The user:** a 4th-year aviation/mechanical student. Strong in thermodynamics (A grade; knows conduction/convection/radiation, Carnot), fluid dynamics and mechanics; little chemistry. **They must be able to read and defend every line of code.** Keep code short, plain and commented with the physics, not clever.

## A2. What is simulated (decided)
- **Only the dry aerogel skeleton:** solid walls + air in the pores. No carbon fibre, no resin, no laminate in v0.1.
- **Structure:** hexagonal honeycomb channels along z (the supervisor accepted "hollow cell with a homogeneous wall"). **Only two structures exist: `Honeycomb` (ideal) and `Honeycomb + defects`** (cell-size spread, wall-thickness variation, cracks). No lamellar, Voronoi or SEM in v0.1.
- **Material:** enters only as wall properties. Default `k_wall = 4.0 W/m·K`, status **derived**, source "back-calculated from Chan et al. 2022 (Kit's paper), Nat. Commun. 13:5553: k_wall = (k_axial − φ k_air)/(1 − φ) with k_axial ≈ 5.8 × 16.9 mW/m·K, φ = 0.982". Keep this label wording. Do not add a "BN only / not general aerogel" qualifier (the user withdrew that).
- **Heat paths, counted once each, for both directions:**
  `k_total = k_solid + k_gas + k_rad + k_conv`, `anisotropy = k∥ / k⊥`.
  If one method resolves several paths at once (pixel FV resolves solid **and** gas, coupling included), it declares that, and the other path is **not added again** (no double counting; required by `guide/04_Simulation/Build_Brief.md` §4).
- **Material row:** a placeholder row **under Convection** with one method `placeholder.py` that does nothing ("not decided yet"), contributes nothing to k_total, and exists so the user can add something later.

## A3. Meeting constraints (from the transcript, `docs/PLAN.md` §0a)
- Pore size is varied first, with composition fixed. **Porosity and density follow from geometry and are never set independently.**
- Alignment is fixed. One representative pore size per model (the defects structure adds a spread around it, as a sensitivity study, not as the baseline).
- Compare **trends**, not absolute numbers. Measured k⊥ = 16.9 mW/m·K (Chan 2022) is below the air-only floor (≈ 26), so no air-filled micron-channel model can reach it. Report this gap; never tune inputs to hide it.
- Do not invent a freezing-temperature → pore-size law. Do not invent material constants: every input has `status ∈ {measured, literature, derived, hypothetical}` plus a source.

## A4. Physics: fast methods (formulas). Hand-checkable; full detail in `docs/PLAN.md` §4
Defaults: d = 30 µm (literature, Chan 2022), t = 0.27 µm (derived: gives φ ≈ 98.2 %), T = 300 K, p = 101.325 kPa.
- **Geometry (honeycomb):** p = d + t, φ = (d/p)² (d = inner flat-to-flat), ρ_bulk = (1 − φ) ρ_wall. ρ_wall default = 20.2 / 0.018 ≈ 1122 kg/m³ (derived from Chan 2022: ρ = 20.2 kg/m³ at φ = 0.982).
- **Solid (formula):** k_solid,∥ = (1 − φ) k_wall; k_solid,⊥ = ½ (1 − φ) k_wall (thin-wall hex network, cos² average over 0°/60°/120°; 2D analogue of the ⅓ foam strut factor, Collishaw & Evans 1994).
- **Gas (Knudsen):** k_air(T) by linear interpolation in Incropera Table A.4 (250 K 22.3, 300 K 26.3, 350 K 30.0, 400 K 33.8 mW/m·K). λ = k_B T / (√2 π d_g² p), d_g = 3.72e-10 m (≈ 66 nm at 300 K, 1 atm). Kn = λ/d. β = ((2 − α)/α)·(2γ/(γ + 1))/Pr with α = 1, γ = 1.4, Pr = 0.71 → ≈ 1.64 (Kaganer 1969; Zeng, Hunt & Greif 1995). k_gas = k_air / (1 + 2βKn). Contribution φ·k_gas in both directions (thin-wall limit).
- **Radiation, opaque walls:** k_rad = 4σT³ d ε/(2 − ε), ε = 0.9 hypothetical (Incropera radiation exchange between parallel grey surfaces). Same value in both directions as a first approximation (state this).
- **Radiation, Rosseland:** k_rad = 16 n² σ T³ / (3 e ρ_bulk), n = 1, e = specific extinction (m²/kg, hypothetical). Compute the optical thickness τ = e ρ_bulk L (L = sample thickness, hypothetical, default 3 mm) and add a warning note when τ < 3 (Hrubesh & Pekala 1994).
- **Convection, Rayleigh:** Ra = g β_T ΔT_pore d³ / (ν α_th), β_T = 1/T, ΔT_pore = (dT/dx)·d, dT/dx hypothetical (default 1000 K/m); ν, α_th of air at 300 K from Incropera (15.89e-6, 22.5e-6 m²/s). k_conv = 0 while Ra < 1708, with a note giving Ra and the reason (Skochdopole 1961: cells below about 3–4 mm). Above 1708, return k_conv = 0 still, with a warning that the formula level cannot estimate it and the user should run LBM.
- **Expected hand numbers at defaults** (use as test anchors, recompute exactly in tests): φ ≈ 0.9822; k_gas ≈ 26.1 mW/m·K; solid ⊥ ≈ 35.5, ∥ ≈ 71.0; φ·k_gas ≈ 25.6; k_rad opaque ≈ 0.15; total ⊥ ≈ 61.3, ∥ ≈ 96.8 mW/m·K; anisotropy ≈ 1.58.

## A5. Physics: detailed methods (more CPU, more realistic). `docs/PLAN.md` §4b
**Rule: each detailed method must reproduce its fast formula in the ideal case (a test) before being trusted.**
- **Structure `honeycomb_defects`:** rasterise a hex honeycomb onto a pixel grid (a few cells, e.g. 3×3 or 4×4 periodic-ish block), plus seeded random defects: cell-size spread (%), wall-thickness variation (%), crack fraction (% of wall length removed in short gaps). Report the *counted* porosity. Real walls are t/d ≈ 0.009, so ≥ 2 px per wall needs very large grids. Allowed shortcut, documented with a `shortcut:` comment and in PHYSICS.md: draw walls thicker in pixels and scale the wall pixel conductivity so that wall conductance (t·k_wall) is preserved, then check against the formula. Pick whichever keeps a default run under ~10–20 s on a laptop, and say what you chose.
- **Solid `pixel_fv`:** every pixel is a resistor; energy balance per pixel; harmonic-mean face conductance; fixed ΔT on two opposite sides, insulated on the others; `scipy.sparse.linalg.spsolve` (or CG). Wall pixels = k_wall, pore pixels = gas conductivity from the gas row (a scalar, or the per-pixel map from local_knudsen if that was the last gas run). Gives k⊥ (x and y; report both or their mean), k∥ = area-weighted mean of pixel k (exact for straight channels), and the temperature field (downsampled for the 3D view). Declares `covers = ["solid", "gas"]`. Verify: ideal honeycomb vs φk_gas + ½(1 − φ)k_wall within ~5 %, energy balance, grid refinement. A scratch prototype (square honeycomb) matched the formula to 1 % in 0.5 s at 300×300 px, and a 1-px crack per wall cut k⊥ by 21 %.
- **Gas `local_knudsen`:** local pore size per pore pixel from `scipy.ndimage.distance_transform_edt` (≈ 2 × distance to the nearest wall, or a local-thickness estimate), Kn per pixel, k_gas map. The scalar contribution is the area average. Verify: uniform wide pores give the fast Knudsen value.
- **Gas `monte_carlo`:** NumPy-vectorised virtual molecules in the pore pixels: random start, random direction, exponential free path with mean λ, truncated at the first wall pixel → λ_eff; k_gas = k_air · λ_eff/λ. Seeded. Verify: a parallel-plate gap vs the Knudsen formula over Kn ≈ 0.01–10 (within a stated tolerance), and the free-space limit λ_eff → λ.
- **Radiation `ray_tracing`:** NumPy-vectorised photon bundles through slabs of the structure image of increasing thickness. At a wall pixel a bundle is absorbed with probability from the wall absorption κ_w·t (semi-transparent walls) or ε, otherwise reflected/transmitted. Fit Beer's law T(L) = exp(−βL) → β. If βL ≥ 3: k_rad = 16σT³/(3β); else the two-flux (Schuster–Schwarzschild) slab estimate. 2D rays in the cross-section are a simplification (shortcut comment). Verify: opaque walls approach the opaque-wall formula order of magnitude; energy conservation (absorbed + reflected + transmitted = 1); empty slab transmits everything. Source: Randrianalisoa & Baillis 2014.
- **Convection `lattice_boltzmann`:** short NumPy D2Q9 flow + D2Q5 (or D2Q9) temperature lattice, Boussinesq buoyancy, square cavity heated from below, lattice parameters chosen to match the physical Ra and Pr. Returns Nu, k_conv = (Nu − 1)·φ·k_gas. Default run: the physical Ra at the current d (tiny → Nu = 1, fast). Verify (a test marked `slow`): Nu ≈ 1 below Ra ≈ 1708 and Nu > 1 clearly above it (e.g. Ra = 5000). Sources: Shan 1997; Mohamad, *Lattice Boltzmann Method* (textbook codes).
- **Reuse policy** (Ponytail): standard library / NumPy / SciPy first. **Do not add PoreSpy, pumapy, TauFactor or XLB as dependencies.** Mention them in the README table as optional cross-checks only.

## A6. UI (approved; build it from `docs/ui-mockup.html`)
- **Two parts only:** a left sidebar + a three.js 3D model. Light/dark theme as in the mockup. three.js pinned to `three@0.160.0` via the same importmap.
- **Sidebar rows, one per backend folder in ORDER:** Structure, Solid conduction, Gas conduction, Radiation, Convection, Material. Each row:
  - collapsed: title · chosen method · last result
  - expanded, horizontally: the pill/capsule selector (one segment per method file, ◆ marks detailed), input boxes next to it (with a unit and a coloured status dot), and ▶ Start under the selector
  - each row runs on its own, with a progress state for detailed methods
- **Hover tooltips:** row title → folder `HELP`; method segment → `HELP`, `EQUATION`, `SOURCE`, `COST`; input → `help`, `status`, `source`; result → its notes. **Every word comes from backend variables** (`GET /api/models`) or `aerosim/core/ui_text.py`. The front end hard-codes no labels or physics.
- **Reminder line** in the sidebar (text from `ui_text.py`): "Scope: Honeycomb and Honeycomb + defects only · k_total = k_solid + k_gas + k_rad + k_conv".
- **Footer:** the k_total formula with the current numbers for k⊥ and k∥ (e.g. `k⊥ = 35.5 + 25.6 + 0.15 + 0 = 61.3 mW/m·K`; a coupled term shown as `(solid+gas) 61.2`), and the anisotropy. Grey out the footer with "re-run X" when a row's inputs changed since its last run. Changing the structure invalidates the rows that depend on it.
- **3D view:** ideal honeycomb tubes (as in the mockup), or for `Honeycomb + defects` the pixel map extruded along z (downsampled/merged meshes so it stays fast). Walls drawn thicker than real, with a corner note. After a detailed run that returns a `field`, colour the top face with it and show the small colour bar. Drag to rotate.
- **Material row:** shows its single "Placeholder" segment, no inputs (or a disabled note), and hover text "Reserved for a future material simulation; not decided yet."
- **API (the only link):** `GET /api/models`, `POST /api/run/<row>/<method>` (body = inputs, returns the result), `GET /api/structure` (geometry for the 3D view). Served by the standard-library `http.server`: `python -m aerosim serve` → http://localhost:8000.

## A7. Folder structure and contract (`docs/DESIGN.md` §3)
```
aerosim/
  __init__.py  __main__.py         python -m aerosim serve | run | sweep
  core/  registry.py  server.py  constants.py (σ, k_B, air table with sources)  ui_text.py  state.py (if needed)
  structure/   __init__.py (ROW, ORDER, HELP)  honeycomb.py  honeycomb_defects.py  _template.py
  solid/       __init__.py  formula.py  pixel_fv.py  _template.py
  gas/         __init__.py  knudsen.py  local_knudsen.py  monte_carlo.py  _template.py
  radiation/   __init__.py  opaque_walls.py  rosseland.py  ray_tracing.py  _template.py
  convection/  __init__.py  rayleigh.py  lattice_boltzmann.py  _template.py
  material/    __init__.py  placeholder.py  _template.py
web/  index.html  app.js  style.css
.agent/tests/   all pytest tests       .agent/checks/  checker scripts + screenshots
docs/PHYSICS.md  every equation in plain words + source + one fully worked example at the defaults
README.md  CLAUDE.md  idea.json  pyproject.toml (deps, ruff config, pytest testpaths = [".agent/tests"], marker "slow")
```
- **A folder with `__init__.py` = a row; a file = a method segment; files starting with `_` are ignored.** Adding a new file in the house style must make it appear in the UI with no front-end change.
- Method file contract (the exact house style; `_template.py` in every folder shows it):
```python
"""One-line summary."""

NAME = "Pixel FV"                  # capsule text
LEVEL = "detailed"                 # "fast" | "detailed"
ORDER = 2                          # left → right
HELP = "Plain-words explanation, 2–4 sentences."
EQUATION = "…"
SOURCE = "…"
COST = "≈ 1 s"
INPUTS = {
    "k_wall": {"value": 4.0, "unit": "W/m·K", "status": "derived",
               "source": "back-calculated from Chan et al. 2022 (Kit's paper) axial k",
               "help": "Conductivity of the wall material itself (not the aerogel)."},
}


def run(structure, inputs, conditions):
    ...
    return {"k_par": ..., "k_trans": ..., "covers": ["solid"], "notes": [...], "field": None}
```
  You may refine the contract (e.g. structure methods return `phi`, `rho_bulk`, `geometry` instead of k; `conditions` carries T, p and earlier rows' results). If you do, update `_template.py`, the README and DESIGN.md to match. The registry must reject malformed files with a clear message, and `test_contract.py` must enforce the same rules.
- Style: `ruff format` + `ruff check`, 4-space indent, snake_case, SI units internally (W/m·K), with mW/m·K only for display.

## A8. Sources (cite in HELP/SOURCE/PHYSICS.md; verify page numbers before final report)
Hrubesh & Pekala 1994 (J. Mater. Res. 9:731) · Lou et al. 2023 (Gels 9:220) · Zeng, Hunt & Greif 1995 (J. Heat Transfer 117:758) · Kaganer 1969 · Collishaw & Evans 1994 (J. Mater. Sci. 29:2261) · Skochdopole 1961 (via NIST NBSIR 82-1664) · Incropera, *Fundamentals of Heat and Mass Transfer* · Chan et al. 2022 (Nat. Commun. 13:5553, Kit's paper; PDF at `guide/05_References/PDFs/U02_Chan_2022_Additive_Freeze_Casting.pdf`) · Randrianalisoa & Baillis 2014 (C. R. Physique) · Shan 1997 (Phys. Rev. E 55:2780) · Mohamad, *Lattice Boltzmann Method* · Patankar 1980 (finite volume).

## A9. Files you must read before coding (all, in full)
`idea.json` · `CLAUDE.md` · `docs/PLAN.md` · `docs/DESIGN.md` · `docs/ui-mockup.html` · `HANDOVER.md` · `guide/04_Simulation/Build_Brief.md` · `guide/04_Simulation/Requirements_Extracted_From_Transcript.md` · `guide/04_Simulation/Previous_Work_Cautions.md` · `.agent/skills/ponytail/SKILL.md` (follow it at level *full*).

---

# PART B: THE TASK

Build v0.1 completely, on branch `main`, in `/home/user/FYP`.

1. **Setup:** `pyproject.toml` (Python ≥ 3.11; deps: numpy, scipy; dev: pytest, ruff; pytest `testpaths = [".agent/tests"]`, marker `slow`). Install with pip.
2. **Backend:**
   - core (registry, server, constants, ui_text)
   - all 13 method files in A7, plus `__init__.py` and `_template.py` per folder
   - CLI `python -m aerosim serve | run | sweep`. `sweep` writes a CSV of the k terms vs pore size for sweep modes A (fixed t) and B (fixed pitch), plus C (fixed φ) as a diagnostic, using the fast methods, to `results/`. Keep it small.
3. **Frontend:** `web/` per A6, built from the mockup's look. No physics or hard-coded labels in JS.
4. **Tests in `.agent/tests/`:**
   - contract test for every method file
   - hand-number test at the defaults (A4)
   - limits (φ → 0 gives k_wall along z; φ → 1 gives gas)
   - each detailed method vs its formula (A5)
   - energy balance
   - API smoke test (start the server on a free port, GET models, POST each fast method)
   - LBM onset (marked `slow`)
   The fast suite must run in under ~60 s. All must pass.
5. **UI check:** a script in `.agent/checks/` that starts the server, opens the page with Playwright (preinstalled: `require('playwright')`, use `NODE_PATH=$(npm root -g)`, launch chromium with `--use-gl=swiftshader --enable-unsafe-swiftshader`), clicks Start on a fast and a detailed method, hovers a segment, and saves screenshots into `.agent/checks/`. It must report zero console errors.
6. **Docs:**
   - **`docs/PHYSICS.md`:** plain-words physics per method + the worked example.
   - **`README.md`**, rewritten with these sections, in this order:
     1. one-line intro + **Reminder** (scope = Honeycomb and Honeycomb + defects only; `k_total = k_solid + k_gas + k_rad + k_conv`)
     2. Quick start
     3. **Backend**: the idea of simplified (fast) vs detailed methods
     4. **Backend methods**: a table of ALL current method files (row, file, level, what it does, equation, source, reused library / optional cross-check)
     5. **Frontend**
     6. **File system**: tree with one-line descriptions
     7. **How to add a new simulation method**: copy `_template.py`, fill the variables, run tests, refresh the page; a new folder = a new row
     8. Other repo contents: keep the existing links to `HANDOVER.md`, `guide/`, `AAE4203_GNSS_Lab1/`, `docs/COUNCIL_*`
   - Update `docs/DESIGN.md` if you changed the contract.
7. **Commits:** small logical commits on `main`. End each message with:
   ```
   Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
   Claude-Session: https://claude.ai/code/session_0143oVsGXh4V8fwmnWfhskgN
   ```
   No model identifiers anywhere else. At the end: `git push -u origin main`, retrying network errors up to 4 times with backoff. Do not touch `guide/` or `AAE4203_GNSS_Lab1/`.
8. **Final report back** (your last message), short:
   - what was built
   - test results (paste the pytest summary line)
   - the numbers at the defaults: φ, each k term, totals, anisotropy, for the fast methods and for pixel FV
   - pixel FV with cracks vs without
   - LBM onset check
   - runtimes of each detailed method
   - every shortcut you took and why
   - anything not done or uncertain

Ask no questions. Where something is ambiguous, choose the simplest option consistent with Part A, and record it in the final report.
