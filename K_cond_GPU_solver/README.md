# K_cond GPU solver

Separate from the aerosim web tool (`aerosim_html/` after the folder split). It works out how well the aerogel layer conducts heat, from the recipe and the measured structure, using GPU simulations on Google Colab where formulas are not good enough.

**Status:** first version: [`colab_k_cond.py`](colab_k_cond.py), one file to paste into a Colab cell (GPU runtime). Tested in quick CPU mode, all built-in checks pass; not yet run on a GPU. Full plan: [PLAN.md](PLAN.md).

## What it solves

Two steps, one after the other:

1. **Wall:** how well one cell wall conducts, from what it is made of and how the BN sheets lie in it.
2. **Honeycomb:** how well the whole layer conducts, from the wall result, the cell geometry and what fills the cells (air, or epoxy after infusion).

Note on names: in the slide-10 maths, "k hexagon" is whatever fills the cells (air or epoxy). It is an input, not something to solve. The honeycomb step is what gives the layer's conductivity.

## Step 1: wall

| Input | Example | Where it comes from |
| --- | --- | --- |
| Recipe grams: BN, CNF, MTMS (CNT instead of BN for C2.5) | B10: 5 / 0.5 / 1.0 g | Table 2 of the report |
| BN sheet size and thickness | — | BN datasheet or TEM |
| How flat the sheets lie in the wall | mostly flat | SEM |
| Empty space inside the wall | 0–40 % | density check (PLAN.md) |
| Epoxy inside the wall, and how much | — | mass gain after infusion |
| Conductivity of BN, CNF, MTMS solid, epoxy | — | literature (PLAN.md) |
| Contact resistance sheet-to-sheet and sheet-to-glue | a range | literature, swept |

| Output | Note |
| --- | --- |
| Wall conductivity along the wall | the one that matters |
| Wall conductivity through the wall | small effect |
| Low, likely and high values | from many random walls |
| Which input moved the answer most | tells you what to measure next |

## Step 2: honeycomb layer

| Input | Example | Where it comes from |
| --- | --- | --- |
| Pore size and wall thickness | 30 µm and 0.27 µm today | SEM |
| Wall conductivity | — | step 1 |
| What fills the cells | air (dry) or epoxy (infused) | process |
| Temperature and air pressure | room temperature, 1 atm | test conditions |
| Channel direction relative to the plate | through the thickness or in-plane | SEM of the edge offcuts |
| Measured layer mass and size | — | check on density and porosity |

| Output | Note |
| --- | --- |
| Conductivity along the channels | simple formula is exact; no GPU |
| Conductivity across the channels | same in every sideways direction; GPU gives the exact value for dry layers |
| Conductivity through the plate thickness | combines the two using the channel direction; this goes into the laminate model |
| Porosity and density | compared with the measured mass |
| Low, likely and high values | — |

With air in the cells the result is walls plus air together. For the walls alone, run it with empty cells.

## Where the GPU is used

- **Wall step:** always. Thousands of thin BN sheets, many random copies.
- **Honeycomb step:** dry layers only. With epoxy in the cells the formulas are within about 12 %, so no GPU.

## Files

- `colab_k_cond.py` — the whole solver in one file: wall inputs, honeycomb inputs, run options, engine, output tables, built-in checks
- `PLAN.md` — the full plan
