# Aerogel k Simulator

Predicts the thermal conductivity of a **dry freeze-cast honeycomb aerogel skeleton** (solid walls + air), along (k∥) and across (k⊥) its channels, one heat path at a time. FYP tool, *Thermo-optically functional CFRP laminates for lightweight electrified systems* (PolyU AAE capstone 2026/27, supervisor Dr CHAN Kit-Ying).

> **Reminder**
> - **Scope:** structure = **Honeycomb** and **Honeycomb + defects** only.
> - **`k_total = k_solid + k_gas + k_rad + k_conv`**, for k∥ and k⊥ separately; anisotropy = k∥ / k⊥.
> - Each heat path is counted once. A method that solves several paths together (Pixel FV: solid + gas) says so, and the other row is not added again.
> - The Material row is a placeholder: nothing is simulated there yet.

## Quick start
```bash
pip install -e ".[dev]"          # Python ≥ 3.11; needs only numpy and scipy (+ pytest, ruff to develop)
python -m aerosim serve          # web UI on http://localhost:8000
python -m aerosim run            # k_total breakdown at the defaults, in the terminal
python -m aerosim run structure=honeycomb_defects solid=pixel_fv   # with detailed methods
python -m aerosim sweep          # results/sweep.csv: every k term against pore size (modes A, B, C)
python -m pytest                 # fast test suite (≈ 30 s); python -m pytest -m slow for the LBM onset
```
At the defaults (d = 30 µm, t = 0.27 µm, k_wall = 4 W/m·K, 300 K, 1 atm):
`k⊥ = 35.5 + 25.6 + 0.150 + 0 = 61.3 mW/m·K`, `k∥ = 71.0 + 25.6 + 0.150 + 0 = 96.8 mW/m·K`, anisotropy 1.58. The worked example is in [`docs/PHYSICS.md`](docs/PHYSICS.md) §7.

## Backend
Each heat path (and the structure) is a **row**, and each row offers methods at two levels:
- **fast (simplified):** a closed-form formula from the literature. Instant, checkable by hand, and what the report explains first.
- **detailed (◆):** a small simulation on a pixel picture of the structure (finite volume, Monte Carlo, ray tracing, lattice Boltzmann). Seconds of CPU, but it sees what the formula cannot: cracks, uneven cells, narrow gaps, real optical thickness, the onset of convection.

**Rule:** every detailed method must first reproduce its formula in the ideal case (a test in `.agent/tests/test_detailed.py`) before its answer is trusted where the formula cannot go. More CPU helps only when it is spent on more realistic structure; no CPU fixes unknown inputs (k_wall, wall optics), which are labelled `hypothetical`.

Every input carries `value, unit, status, source, help`, with status ∈ {measured, literature, derived, hypothetical}. Default k_wall = 4.0 W/m·K is **derived**: back-calculated from Chan et al. 2022 (Kit's paper), Nat. Commun. 13:5553. Measured k⊥ = 16.9 mW/m·K in that paper is below the air-only floor (≈ 26 mW/m·K), so compare **trends**; the tool reports the gap instead of tuning inputs to hide it.

## Backend methods
All current method files (one file = one segment in the UI). Physics and checks in [`docs/PHYSICS.md`](docs/PHYSICS.md). **Keep this table in sync with `aerosim/<row>/` (CLAUDE.md rule).**

| Row | File | Level | What it does | Equation | Source | Library used / optional cross-check |
|---|---|---|---|---|---|---|
| Structure | `honeycomb.py` | fast | ideal hexagonal tubes; porosity and density from d and t | p = d + t, φ = (d/p)², ρ = (1 − φ)ρ_wall | hexagon geometry; defaults Chan et al. 2022 | none |
| Structure | `honeycomb_defects.py` | detailed | periodic pixel picture of a 4 × 4 cell block with cell-size spread, wall-thickness variation and cracks; counted φ | wall pixel: distance to bisector of the two nearest centres < t_draw/2; φ = 1 − mean(s) | own code | NumPy, `scipy.spatial.cKDTree` / PoreSpy (optional) |
| Solid conduction | `formula.py` | fast | thin walls in parallel along z; cos² average across | k∥ = (1 − φ)k_w, k⊥ = ½(1 − φ)k_w | Collishaw & Evans 1994 (2D analogue of ⅓) | none |
| Solid conduction | `pixel_fv.py` | detailed | every pixel a resistor, heat balance per pixel, periodic with ΔT per period; solves solid + gas together | Σ G_ij(T_j − T_i) = 0, G = 2k_ik_j/(k_i + k_j), k = QL/(AΔT) | finite volume, Patankar 1980 | `scipy.sparse.linalg.spsolve` / NASA PuMA (pumapy), TauFactor 2 |
| Gas conduction | `knudsen.py` | fast | air table + Knudsen reduction, contribution φ k_gas | λ = k_BT/(√2πd_g²p), k_g = k_air/(1 + 2βKn) | Kaganer 1969; Zeng et al. 1995; Incropera A.4 | none |
| Gas conduction | `local_knudsen.py` | detailed | Knudsen per pixel from the local pore size (local thickness) → k_gas map | k_g(x) = k_air/(1 + 2βλ/d_local(x)) | Kaganer 1969 | `scipy.ndimage.distance_transform_edt` / PoreSpy `local_thickness` |
| Gas conduction | `monte_carlo.py` | detailed | random 3D molecule flights → mean chord 4V/S → equivalent gap | ℓ̄ = 1/mean(1/ℓ), d_eff = ℓ̄/2, k_g = k_air/(1 + 2βλ/d_eff) | Cauchy mean chord; Zeng et al. 1995 | NumPy / pumapy random walk |
| Radiation | `opaque_walls.py` | fast | pore = gap between two grey walls | k_r = 4σT³dε/(2 − ε) | Incropera (grey-plate exchange) | none |
| Radiation | `rosseland.py` | fast | radiative diffusion; warns when τ < 3 | k_r = 16n²σT³/(3eρ), τ = eρL | Hrubesh & Pekala 1994 | none |
| Radiation | `ray_tracing.py` | detailed | 2D photon bundles through slabs → Beer's law β → Rosseland or two-flux | T(L) = e^(−βL); k_r = 16σT³/(3β) or 4σT³L/(1 + ¾βL) | Randrianalisoa & Baillis 2014 | NumPy / pumapy radiation |
| Convection | `rayleigh.py` | fast | Rayleigh number of one pore → k_conv = 0 below 1708 | Ra = gβ_TΔT d³/(να) | Incropera; Skochdopole 1961 | none |
| Convection | `lattice_boltzmann.py` | detailed | D2Q9 flow + D2Q5 heat, Boussinesq, layer heated from below → Nu | Nu = 1 + ⟨vT⟩H/(αΔT), k_c = (Nu − 1)φk_g | Shan 1997; Mohamad (textbook) | NumPy / XLB not recommended (heavy) |
| Material | `placeholder.py` | fast | nothing yet (not decided); adds nothing | none | not decided yet | none |

Optional cross-check libraries (PoreSpy, pumapy, TauFactor 2, XLB) are **not** dependencies; the tool runs on NumPy + SciPy only.

## Frontend
`web/` (plain HTML + one JS module + CSS, three.js `0.160.0` from a pinned CDN). Two parts only:
- **Left sidebar:** a reminder line, then one row per backend folder (Structure, Solid conduction, Gas conduction, Radiation, Convection, Material). Click a row to expand it: a pill selector with one segment per method file (◆ = detailed), the method's inputs next to it (unit and a coloured status dot), and ▶ Start under it. Each row runs on its own; detailed methods show a progress bar. The footer shows `k_total = …` with the current numbers for k⊥ and k∥ and the anisotropy; it greys out with "re-run …" when a row's inputs changed or its structure changed since its last run.
- **3D model:** the ideal hex tubes, or the defects picture extruded along z (walls drawn thicker than real, with a corner note). After a detailed run that returns a field (temperature, gas-k map, absorbed radiation) the top face is coloured with a small colour bar. Drag to rotate.

**Hover:** row title → folder `HELP`; segment → `HELP`, `EQUATION`, `SOURCE`, `COST`; input → `help`, status, `source`; result → its notes. Every word comes from the backend (`GET /api/models`, i.e. the method files and `aerosim/core/ui_text.py`); the front end holds no physics and no labels.

API (the only link): `GET /api/models`, `POST /api/run/<row>/<method>` (body = inputs, returns the result and totals), `GET /api/structure` (geometry for the 3D view).

## File system
```
aerosim/
  __main__.py          CLI: python -m aerosim serve | run | sweep
  core/
    registry.py        finds rows (folders) and methods (files), refuses malformed ones
    state.py           runs methods, remembers last results, adds k_total once per path, "re-run"
    server.py          standard-library http.server: the JSON API + serves web/
    constants.py       σ, k_B, g, air table (Incropera A.4), mean free path, Knudsen β
    ui_text.py         the few UI words not tied to a method (title, reminder, footer, Start)
  structure/           row 1: honeycomb.py, honeycomb_defects.py, _template.py
  solid/               row 2: formula.py, pixel_fv.py, _template.py (K_WALL in __init__.py)
  gas/                 row 3: knudsen.py, local_knudsen.py, monte_carlo.py, _template.py
  radiation/           row 4: opaque_walls.py, rosseland.py, ray_tracing.py, _template.py
  convection/          row 5: rayleigh.py, lattice_boltzmann.py, _template.py
  material/            row 6: placeholder.py, _template.py
web/                   index.html, app.js, style.css: the UI
results/sweep.csv      output of python -m aerosim sweep
.agent/
  tests/               the pytest suite (contract, hand numbers, limits, detailed, API)
  checks/              ui_check.js (Playwright) and its screenshots
  skills/ponytail/     coding-style skill for agents
  SUBAGENT_GUIDE.md    full context pack for build agents
docs/                  PHYSICS.md, DESIGN.md, PLAN.md, ui-mockup.html, COUNCIL_*.md
idea.json              full record of the design dialogue
CLAUDE.md              rules for agents working here
pyproject.toml         dependencies, ruff style, pytest settings
```

## How to add a new simulation method
1. Copy `aerosim/<row>/_template.py` to a new name without a leading `_`, e.g. `aerosim/gas/dsmc.py`.
2. Fill in the variables: `NAME` (segment text), `LEVEL` ("fast" or "detailed"), `ORDER` (position), `HELP`, `EQUATION`, `SOURCE`, `COST`, and `INPUTS` (each with `value, unit, status, source, help`). If `run()` reads another row's result, list it in `USES` (e.g. `["gas"]`).
3. Write `run(structure, inputs, conditions)`: return `k_par` and `k_trans` in W/m·K, `covers` (which of "solid", "gas", "rad", "conv" it accounts for), and `notes`. Optionally a `field` for the 3D top face.
4. Run `python -m pytest`: `test_contract.py` refuses a file that misses a field, has an input without a source/status, or returns the wrong keys.
5. Refresh the page (a running server picks up new files on refresh; restart it after editing an existing file). The new segment appears with all its hover text. No front-end change.
6. Add a row to the **Backend methods** table above.

A **new folder** with an `__init__.py` holding `ROW`, `ORDER`, `HELP`, `COLOR` becomes a **new row**. The structure row must stay first.

## Notes and unfinished issues
Open questions from the v0.1 build check (2026-11-15). **No more backend methods are planned for now.** These are notes, not tasks in progress.

1. **What "pore size" means for gas in a hex channel.**
   - Local Kn treats the pore size d as the gap.
   - Monte Carlo finds that a hex channel behaves like a gap of about d/2, and the pixel staircase lowers it by about 10 % more.
   - At 1 atm the effect on k is under 1 %, but the definition matters at low pressure. It is a fair point to discuss in the report.
2. **Ray tracing (0.46 mW/m·K at the defaults) depends entirely on two hypothetical wall inputs:** IR absorption κ_w and reflectance. Replace them once the reflectance spectra are measured. Until then, read the radiation term as an order of magnitude.
3. **Source page numbers are not verified yet.** Check every citation in `docs/PHYSICS.md` and the method files against the original papers before the interim report. Also check the Collishaw & Evans DOI, which differs between databases, and the author list of the 2021 CNF/BN paper.
4. **Pixel FV on the ideal honeycomb:** k_x and k_y differ by 5.5 % because of the pixel staircase. Only their mean is checked against the formula.
5. **Measured vs model gap:**
   - Chan 2022 measured k⊥ = 16.9 mW/m·K, which is below the air-only floor (≈ 26 mW/m·K) of any air-filled micron-channel model.
   - Cracks raise the model's anisotropy from 1.6 to about 2.0; the measured value is ≈ 5.8.
   - Compare trends, not absolute values (see `docs/PLAN.md` §2).
6. **GitHub housekeeping (repo settings, outside the code):**
   - Set the repository's default branch to `main` (Settings → Branches).
   - The merged branches `claude/quirky-thompson-39y288` and `claude/beautiful-tesla-ro162g` still contain the removed AAE4203 GNSS lab folder and can be deleted.

## Other repo contents
- [`HANDOVER.md`](HANDOVER.md) — handover: original goal, state, change log, sessions
- [`guide/`](guide/) — full contents of the handover zip `FYP_Handover_2026-10-29.zip` (start at `guide/summary.md`; read-only)
- [`docs/COUNCIL_BRIEF.md`](docs/COUNCIL_BRIEF.md), [`docs/COUNCIL_SETUP.md`](docs/COUNCIL_SETUP.md) — council review brief and orchestrator notes (written for the earlier FV-solver plan)
- [`docs/PLAN.md`](docs/PLAN.md), [`docs/DESIGN.md`](docs/DESIGN.md), [`idea.json`](idea.json) — plan, UI/backend design, and the design-session record
- [`docs/FUTURE_WORK.md`](docs/FUTURE_WORK.md) — honeycomb slice model (corrected proof, why it is not a method, bounds) and a report checklist for the code
