# Aerogel simulator: UI + backend design (v1, 2026-11-15)

Status: **design only, nothing built.** This file replaces §5 (UI) and §7 (layout) of `PLAN.md`. Physics, sources and the timeline stay in `PLAN.md`.

Principles from the user:
- The UI is minimal: **left sidebar + 3D model**, nothing else.
- **No global presets.** Each heat path picks its own method.
- Every label and every hover explanation comes from a **variable in the backend file** that implements it.
- Front end and back end are **fully separable**: they only talk through a small JSON API.
- **Adding a new Python file in the right folder, in the house style, makes it appear in the UI automatically.**
- Reuse existing libraries where they are better than writing our own.

---

## 1. UI design

### 1.1 Layout
```
┌──────────────────────────────────────┬───────────────────────────────────────┐
│  AEROGEL k SIMULATOR            (i)  │                                       │
├──────────────────────────────────────┤                                       │
│ ▼ Structure                     (i)  │                                       │
│   ╭─────────┬─────────┬────────╮     │   d [ 30 ] µm      t [ 0.27 ] µm      │
│   │Honeycomb│ Voronoi │  SEM   │     │   cracks [ 0 ] %                      │
│   ╰─────────┴─────────┴────────╯     │                                       │
│   [ ▶ Start ]           φ 98.2 %     │         3D MODEL (three.js)           │
├──────────────────────────────────────┤      block of channels along z,       │
│ ▼ Solid conduction              (i)  │      built from the chosen structure; │
│   ╭──────────┬───────────╮           │      after a detailed run the top     │
│   │ Formula  │ Pixel FV  │  k_wall [4.0] W/m·K                               │
│   ╰──────────┴───────────╯           │      face shows its result field      │
│   [ ▶ Start ]   k⊥ 36.0  k∥ 72.0     │      (temperature / gas-k map)        │
├──────────────────────────────────────┤                                       │
│ ▶ Gas conduction      Knudsen  25.7  │      drag = rotate, scroll = zoom     │
│ ▶ Radiation           Opaque    0.2  │                                       │
│ ▶ Convection          Rayleigh  0.0  │                                       │
├──────────────────────────────────────┤                                       │
│  k⊥ = 61.9   k∥ = 97.9   ratio 1.58  │                                       │
│  mW/m·K       (sum of the rows above)│                                       │
└──────────────────────────────────────┴───────────────────────────────────────┘
```

### 1.2 The sidebar rows
- **One row per backend folder** (Structure, Solid, Gas, Radiation, Convection), top to bottom. The row title, order and info text come from the folder's `__init__.py`.
- **Collapsed row:** title · chosen method · its last result. Click it to expand.
- **Expanded row:** grows *horizontally*:
  - left: the **capsule selector**, a pill shape (half-circle, rectangles, half-circle), one segment per method file in that folder. Two files give two segments; adding a third file gives three segments.
  - right, next to the selector: **input boxes** for the chosen method, each with its unit and a small coloured dot for its status (measured / literature / derived / hypothetical).
  - under the selector: **▶ Start**. A fast method finishes instantly. A detailed one shows a thin progress bar in the row. Each row runs on its own.
- **Footer:** total k⊥, k∥ and anisotropy = the sum of the four heat-path rows. If a row has changed since it last ran, the footer greys out with "re-run Solid".

### 1.3 Hover explanations
- Hover over a **row title** → what this heat path is (folder text).
- Hover over a **capsule segment** → what this method does, its equation, its source, roughly how long it takes (file variables `HELP`, `EQUATION`, `SOURCE`, `COST`).
- Hover over an **input** → what the value means and where the default comes from (`INPUTS[...]["help"]`, `["source"]`).
- Hover over a **result** → which numbers it came from (returned by the method).
- The tooltip is plain text with an optional equation line. No hard-coded words in the front end except "Start".

### 1.4 The 3D model
- It shows the **current structure**: hex tubes, lamellar sheets, a Voronoi/cracked pattern, or an SEM image extruded along z.
- Walls are drawn thicker than real (true t/d ≈ 0.01 would be invisible). A small note in the corner says "walls ×10".
- After a detailed run the **top face is coloured by that run's field**: temperature for solid, local gas-k for gas, absorbed radiation for radiation. There is a tiny colour bar, and nothing else.
- **No other panels.** Charts and sweeps go to `results/` files and the report, not the UI (minimal on purpose).

### 1.5 Look
- Light and dark themes. One accent colour, plus four fixed colours for the four heat paths, used for the row dot and the 3D field.
- Font: system UI. Numbers in tabular figures.
- The mockup is in `docs/ui-mockup.html` (static, fake numbers, to agree on the look before building).

---

## 2. Backend: methods and what can be reused

"Own" means written by us, short and readable; it is what the report explains. "Reuse" means an existing, published library. Where a library exists, the recommended pattern is **own code as the main method, library as an independent cross-check**. The report can then say "our solver agrees with NASA PuMA within x %", which is strong academic support.

### 2.1 Structure (shared input for every path)
| Method file | Level | What it does | Reuse from an existing repo | Own code |
|---|---|---|---|---|
| `honeycomb.py` | fast | ideal hex tubes; φ = (d/p)² | none needed | ~20 lines |
| `lamellar.py` | fast | parallel sheets; φ = d/p | none needed | ~20 lines |
| `voronoi.py` | detailed | irregular cells, size spread, wall-thickness variation, **cracks** | **PoreSpy** `generators.voronoi_edges` (MIT) or `scipy.spatial.Voronoi` | crack-cutting + scale bar, ~60 lines |
| `sem_image.py` | detailed | thresholded SEM cross-section → pixel map | **scikit-image** (`io`, `threshold_otsu`); **PoreSpy** `local_thickness`, porosity metrics | scale input + cleaning, ~40 lines |

### 2.2 Solid conduction
| Method file | Level | What it does | Reuse from an existing repo | Own code |
|---|---|---|---|---|
| `formula.py` | fast | k∥ = (1−φ)k_w; k⊥ = ½(1−φ)k_w (honeycomb) or series (lamellar) | none | ~30 lines |
| `pixel_fv.py` | detailed | **every pixel is a resistor**; energy balance per pixel; sparse solve; temperature field | **SciPy** `sparse.linalg` (solver). Cross-check: **NASA PuMA / pumapy** `compute_thermal_conductivity` (finite volume on 3D images) or **TauFactor 2** (MIT, PyTorch, multi-phase conductivity) | ~60 lines (prototype already exists and matched the formula to 1 %) |

### 2.3 Gas conduction
| Method file | Level | What it does | Reuse from an existing repo | Own code |
|---|---|---|---|---|
| `knudsen.py` | fast | k_g = k_air/(1+2βKn), with Kn from mean pore size | none | ~30 lines |
| `local_knudsen.py` | detailed (cheap) | Kn **per pixel** from the local pore size → map of gas k (narrow cracks conduct less) | **PoreSpy** `filters.local_thickness`, or `scipy.ndimage.distance_transform_edt` | ~30 lines |
| `monte_carlo.py` | detailed | random molecule flights cut short by walls → real λ_eff in this geometry | possible cross-check: **pumapy** particle-random-walk tortuosity *(exact function to confirm in the docs)* | ~70 lines, NumPy-vectorised |

### 2.4 Radiation
| Method file | Level | What it does | Reuse from an existing repo | Own code |
|---|---|---|---|---|
| `opaque_walls.py` | fast | k_r = 4σT³d·ε/(2−ε) | none | ~20 lines |
| `rosseland.py` | fast | k_r = 16n²σT³/(3eρ), with an optical-thickness warning | none | ~25 lines |
| `ray_tracing.py` | detailed | photon bundles through the structure → extinction β → Rosseland or two-flux | **pumapy** `compute_radiation` (ray tracing → β; in `puma.experimental` in recent versions) | own two-flux slab model ~40 lines; own simple 2D ray tracer ~80 lines if pumapy is unsuitable |

### 2.5 Convection
| Method file | Level | What it does | Reuse from an existing repo | Own code |
|---|---|---|---|---|
| `rayleigh.py` | fast | Ra of one pore → k_c = 0, with the reason | none | ~25 lines |
| `lattice_boltzmann.py` | detailed | thermal LBM in one pore → Nu; sweep d to find the onset size | **XLB** (Apache-2.0, JAX) exists but is heavy and its thermal support is unconfirmed: **not recommended**. Use the student-level codes in Mohamad's LBM textbook as the reference. | ~80–100 lines NumPy |

### 2.6 Shared pieces
| Piece | Reuse | Note |
|---|---|---|
| Linear solver, image tools | SciPy, scikit-image | standard |
| Porous-image metrics | PoreSpy (MIT) | widely cited (Gostick et al. 2019, JOSS) |
| Independent cross-checks | pumapy (NASA), TauFactor 2 (MIT, JOSS 2023) | **optional install**; the tool runs without them. Check the PuMA licence before redistributing. |
| Web server | Python standard library `http.server` | no framework needed |
| 3D view | three.js (pinned CDN version) | only front-end dependency |

---

## 3. Folder structure: "drop in a file → it appears in the UI"

```
aerosim/
  core/
    registry.py        finds every method file and checks it follows the contract
    server.py          JSON API (below) + serves web/
    units.py           shared constants (σ, k_B) with sources
    ui_text.py         the few UI words not tied to a method (title, "Start", footer labels)
  structure/           ← sidebar row 1
    __init__.py        ROW = "Structure", ORDER = 1, HELP = "…"
    honeycomb.py
    lamellar.py
    voronoi.py
    sem_image.py
    _template.py       copy this to add a new structure
  solid/               ← sidebar row 2
    __init__.py
    formula.py
    pixel_fv.py
    _template.py
  gas/                 ← row 3
    __init__.py  knudsen.py  local_knudsen.py  monte_carlo.py  _template.py
  radiation/           ← row 4
    __init__.py  opaque_walls.py  rosseland.py  ray_tracing.py  _template.py
  convection/          ← row 5
    __init__.py  rayleigh.py  lattice_boltzmann.py  _template.py
web/
  index.html  app.js  style.css      builds every row from GET /api/models (no physics, no hard-coded labels)
tests/
  test_contract.py     every method file follows the contract (so it shows in the UI)
  test_limits.py       each detailed method reproduces its fast formula in the ideal case
docs/  PLAN.md  DESIGN.md  PHYSICS.md  ADDING_A_METHOD.md  ui-mockup.html
pyproject.toml         ruff format/lint settings = the house style
```

- **A new folder** (with `__init__.py`) = a new sidebar row.
- **A new file** in a folder = a new segment in that row's capsule selector.
- Files starting with `_` are ignored.

### 3.1 The method-file contract (house style)
Every method file looks like this. Same order, same names, 4-space indent, snake_case, every number carries its unit and source:

```python
"""Pixel finite-volume conduction: each pixel is a small thermal resistor."""

NAME = "Pixel FV"                    # text on the capsule segment
LEVEL = "detailed"                   # "fast" or "detailed"
ORDER = 2                            # position in the capsule (left → right)
HELP = (                             # hover text: plain words, 2–4 sentences
    "Splits the cross-section into pixels. Each pixel is wall or air. "
    "Heat in = heat out at every pixel, which gives the temperature field "
    "and the effective conductivity across the channels."
)
EQUATION = "Σ_neighbours G_ij (T_j − T_i) = 0,   G_ij = 2 k_i k_j / (k_i + k_j)"
SOURCE = "Finite-volume method, e.g. Patankar (1980); cross-check: NASA PuMA"
COST = "≈ 1 s for 300×300 px"        # shown in the tooltip

INPUTS = {
    "k_wall": {
        "value": 4.0,
        "unit": "W/m·K",
        "status": "derived",         # measured | literature | derived | hypothetical
        "source": "back-calculated from Chan et al. 2022 axial k",
        "help": "Conductivity of the wall material itself (not the aerogel).",
    },
}


def run(structure, inputs, conditions):
    """Return k contributions in W/m·K plus anything worth showing."""
    ...
    return {
        "k_par": k_par,
        "k_trans": k_trans,
        "field": temperature_map,    # optional: coloured onto the 3D top face
        "notes": ["energy balance error 1e-9"],
    }
```

- `conditions` = shared values set once in the Structure row: T, pressure, and the structure image/parameters.
- `registry.py` refuses (with a clear message) any file that is missing a field, has an input without `unit` / `help` / `status`, or whose `run()` does not return `k_par` and `k_trans`. `test_contract.py` runs the same check, so a badly written file never reaches the UI half-broken.
- `ruff format` keeps the indentation and layout identical across files.
- `docs/ADDING_A_METHOD.md`: a one-page walkthrough of copying `_template.py`, filling it in, running the tests and refreshing the page.

### 3.2 The API (the only link between front end and back end)
| Call | Returns |
|---|---|
| `GET /api/models` | every row and method with NAME, HELP, EQUATION, SOURCE, COST, INPUTS: everything the sidebar needs |
| `POST /api/run/<row>/<method>` | body = inputs; returns the method's result (k values, notes, optional field) |
| `GET /api/structure` | geometry for the 3D view (cell outlines or a downsampled pixel map) |

The front end never computes physics, and the back end never knows about buttons. Either side can be replaced on its own, e.g. a Jupyter notebook can call the same `run()` functions directly.

---

## 4. What changed from the earlier plan
- **Removed:** the global "Run detailed" preset and the extra UI panels (sweep chart, equations panel, bar chart). Equations now live in the hover text; sweeps go to the CLI/report.
- **Added:** per-row method choice, auto-discovered method files, a contract test, and the reuse table.
