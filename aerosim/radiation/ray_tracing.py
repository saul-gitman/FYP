"""Ray tracing: photon bundles through slabs of the pixel picture; Beer's law gives extinction."""

import numpy as np
from scipy import ndimage

from aerosim.core.constants import SIGMA
from aerosim.radiation import L_SAMPLE
from aerosim.structure.honeycomb_defects import distance_to_wall, image_of

NAME = "Ray tracing"
LEVEL = "detailed"
ORDER = 3
HELP = (
    "Fires infrared 'photon bundles' into slabs of the structure picture, ¼ to 4 cells thick. "
    "At a wall a bundle is reflected, absorbed inside the wall, or passes through it. The "
    "fraction that gets through falls as e^(−βL) (Beer's law); the fit gives the extinction β "
    "of this structure. Then Rosseland if the sample is optically thick, else a two-flux slab."
)
EQUATION = (
    "at a wall: reflect R, absorb (1 − R)(1 − e^(−κ t)), else pass;   T(L) = e^(−βL) → β;   "
    "βL_s ≥ 3: k_rad = 16σT³/(3β),   else k_rad = 4σT³L_s / (1 + 3βL_s/4)"
)
SOURCE = (
    "Randrianalisoa & Baillis 2014 (C. R. Physique, ray tracing in foams); two-flux "
    "(Schuster–Schwarzschild) slab between black walls. Optional cross-check: pumapy"
)
COST = "≈ 3 s"
INPUTS = {
    "kappa": {
        "value": 1.0e6,
        "unit": "1/m",
        "status": "hypothetical",
        "source": "assumed; the infrared absorption of BN/CNF/MTMS walls is not measured",
        "help": "Absorption coefficient of the wall material. CNT would raise it strongly.",
    },
    "refl": {
        "value": 0.1,
        "unit": "",
        "status": "hypothetical",
        "source": "assumed: 1 − ε with the Opaque method's ε = 0.9",
        "help": "Fraction of bundles reflected when they hit a wall surface.",
    },
    "L": L_SAMPLE,
    "bundles": {
        "value": 20000,
        "unit": "",
        "status": "derived",
        "source": "numerical setting: ≈ 1 % noise on the transmitted fraction",
        "help": "Photon bundles per slab. More = less noise, slower.",
    },
    "seed": {
        "value": 1,
        "unit": "",
        "status": "derived",
        "source": "numerical setting: the same seed gives the same answer",
        "help": "Random seed.",
    },
}


def trace(wall_t, length_px, kappa, refl, n, rng, max_steps=20000):
    """Send n bundles into the left face of a slab length_px thick (the picture repeats in x
    and y). Returns the transmitted, reflected, absorbed and still-flying fractions and an
    absorption map. Still flying after max_steps (bundles running almost parallel to the slab
    face) are counted as absorbed and reported."""
    wall = wall_t > 0
    edt = distance_to_wall(wall)
    ny, nx = wall.shape
    pos = np.column_stack([np.full(n, 1e-9), rng.uniform(0, ny, n)])
    sin_a = rng.uniform(-1, 1, n)  # diffuse entry in 2D: sin(angle to the normal) is uniform
    dirs = np.column_stack([np.sqrt(1 - sin_a**2), sin_a])
    inside = np.zeros(n, bool)  # the bundle has entered a wall and not yet left it
    fate = np.zeros(n, int)  # 0 still flying, 1 transmitted, 2 reflected out, 3 absorbed
    absorbed = np.zeros(wall.shape)
    for _ in range(max_steps):
        a = np.flatnonzero(fate == 0)
        if a.size == 0:
            break
        i = np.floor(pos[a, 0]).astype(int) % nx
        j = np.floor(pos[a, 1]).astype(int) % ny
        # in a pore, step as far as the nearest wall allows; inside a wall, small steps
        step = np.where(inside[a], 0.25, np.maximum(edt[j, i] - 1, 0.25))
        new = pos[a] + step[:, None] * dirs[a]
        fate[a[new[:, 0] >= length_px]] = 1  # left through the far face
        fate[a[new[:, 0] < 0]] = 2  # came back out of the near face
        keep = (new[:, 0] >= 0) & (new[:, 0] < length_px)
        a, new = a[keep], new[keep]
        i = np.floor(new[:, 0]).astype(int) % nx
        j = np.floor(new[:, 1]).astype(int) % ny
        hits = wall[j, i] & ~inside[a]  # bundles arriving at a wall surface
        u = rng.random(a.size)
        # shortcut: absorption uses the normal-incidence path t through the wall, not t/cosθ;
        # upgrade: track the angle between the bundle and the wall normal.
        p_abs = (1 - refl) * (1 - np.exp(-kappa * wall_t[j, i]))
        reflect = hits & (u < refl)
        absorb = hits & ~reflect & (u < refl + p_abs)
        fate[a[absorb]] = 3
        np.add.at(absorbed, (j[absorb], i[absorb]), 1)
        # shortcut: a pixel wall has no well-defined normal, so a reflected bundle leaves in a
        # random direction (diffuse) from where it was; upgrade: normals from the cell geometry.
        r = a[reflect]
        angle = rng.uniform(0, 2 * np.pi, r.size)
        dirs[r] = np.column_stack([np.cos(angle), np.sin(angle)])
        move = ~reflect & ~absorb
        pos[a[move]] = new[move]
        inside[a[move]] = wall[j[move], i[move]]
    lost = np.mean(fate == 0)
    fate[fate == 0] = 3
    return [np.mean(fate == f) for f in (1, 2, 3)] + [lost, absorbed]


def run(structure, inputs, conditions):
    if inputs["kappa"] < 0 or not 0 <= inputs["refl"] < 1 or inputs["L"] <= 0:
        raise ValueError("need kappa ≥ 0, 0 ≤ refl < 1 and L > 0")
    pic = image_of(structure)
    rng = np.random.default_rng(int(inputs["seed"]))
    n = max(100, int(inputs["bundles"]))
    cell_px = structure["pitch"] / pic["_dx"]
    cells = np.array([0.25, 0.5, 1, 2, 4])  # slab thicknesses in cell pitches
    rows = [
        trace(pic["_wall_t"], c * cell_px, inputs["kappa"], inputs["refl"], n, rng) for c in cells
    ]
    trans = np.array([r[0] for r in rows])
    L = cells * structure["pitch"]  # slab thicknesses in m
    ok = trans > 0
    if ok.sum() >= 2:
        beta = -np.polyfit(L[ok], np.log(trans[ok]), 1)[0]  # slope of ln T against L
    else:  # (almost) nothing gets through one cell: a lower bound on β
        beta = np.log(n) / L[0]
    beta = max(beta, 1e-12)
    T, Ls = conditions["T"], inputs["L"] * 1e-3
    if beta * Ls >= 3:  # optically thick: radiation diffuses (Rosseland)
        k_rad, model = 16 * SIGMA * T**3 / (3 * beta), "Rosseland (optically thick)"
    else:  # optically thin: two-flux model of a slab between black walls
        k_rad, model = 4 * SIGMA * T**3 * Ls / (1 + 0.75 * beta * Ls), "two-flux slab (thin)"
    stride = int(np.ceil(max(pic["_s"].shape) / 128))
    field = ndimage.uniform_filter(rows[-1][4], stride)[::stride, ::stride]
    notes = [
        "transmitted fraction for ¼, ½, 1, 2, 4 cells: " + ", ".join(f"{t:.3f}" for t in trans),
        f"Beer's law fit: β = {beta:.3g} 1/m, βL_sample = {beta * Ls:.3g} → {model}",
        f"k_rad = {k_rad * 1e3:.3f} mW/m·K, used along and across the channels",
        "energy check per slab: transmitted + reflected + absorbed = "
        + ", ".join(f"{sum(r[:3]):.3f}" for r in rows),
        f"still flying after the step limit (counted absorbed): {max(r[3] for r in rows):.4f}",
        "2D rays in the cross-section only (a simplification: real rays also travel along z)",
    ]
    return {
        "k_par": k_rad,
        "k_trans": k_rad,
        "covers": ["rad"],
        "beta": beta,
        "slabs": [r[:3] for r in rows],
        "notes": notes,
        "field": {
            "name": "Absorbed bundles (4-cell slab, folded onto one block)",
            "values": field.round(3).tolist(),
            "low": "few",
            "high": "many",
        },
    }
