"""Honeycomb + defects: the honeycomb drawn as a pixel picture, with seeded random defects."""

import numpy as np
from scipy import ndimage
from scipy.ndimage import distance_transform_edt
from scipy.spatial import cKDTree

from aerosim.core import ui_text
from aerosim.structure import honeycomb

NAME = "Honeycomb + defects"
LEVEL = "detailed"
ORDER = 2
HELP = (
    "The same honeycomb drawn as a pixel picture, with seeded random defects: cells of different "
    "sizes, walls of different thickness, and cracks (short gaps cut into the walls). Porosity "
    "is counted from the picture. The detailed methods of the other rows work on this picture. "
    "Set the three defect inputs to 0 for the ideal honeycomb."
    " ⚠ Accuracy: walls are drawn 1.2 µm (4 px) thick instead of 0.27 µm, keeping the real "
    "amount of wall in each pixel, and the ±30° walls become pixel staircases: k⊥ along x and "
    "y then differ by ≈ 5 %, though a honeycomb must give equal values. The defects are "
    "random draws, not measured."
)
EQUATION = (
    "wall pixel: distance to the boundary between its two nearest cell centres < t_draw/2;   "
    "φ = 1 − mean(solid fraction of each pixel)"
)
SOURCE = "Own code (NumPy, scipy.spatial). Defect sizes are hypothetical until measured from SEM"
COST = "≈ 0.2 s"
INPUTS = honeycomb.INPUTS | {
    "cells": {
        "value": 4,
        "unit": "cells",
        "status": "derived",
        "source": "numerical setting: an even number, so the block repeats periodically",
        "help": "Number of cells per side of the simulated block.",
    },
    "px_per_cell": {
        "value": 100,
        "unit": "px",
        "status": "derived",
        "source": "numerical setting: walls 4 px wide; Pixel FV within 3 % of the formula (tests)",
        "help": "Pixels per cell pitch. More = finer picture, slower runs.",
    },
    "spread": {
        "value": 10.0,
        "unit": "%",
        "status": "hypothetical",
        "source": "no SEM statistics yet; sensitivity value (0 = identical cells)",
        "help": "Random shift of each cell centre (std. dev., % of pitch): uneven cell sizes.",
    },
    "wall_var": {
        "value": 20.0,
        "unit": "%",
        "status": "hypothetical",
        "source": "no SEM statistics yet; sensitivity value (0 = all walls t thick)",
        "help": "Random change of each wall's thickness (std. dev., % of t).",
    },
    "cracks": {
        "value": 5.0,
        "unit": "%",
        "status": "hypothetical",
        "source": "no SEM statistics yet; sensitivity value (0 = no cracks)",
        "help": "Length of one gap cut into every wall, as % of the wall length.",
    },
    "seed": {
        "value": 1,
        "unit": "",
        "status": "derived",
        "source": "numerical setting: the same seed always gives the same picture",
        "help": "Random seed for the defects.",
    },
}


WALL_PX = 4  # drawn walls are at least this many pixels wide (see the shortcut in picture())


def picture(d, t, cells=4, px_per_cell=100, spread=0.0, wall_var=0.0, cracks=0.0, seed=1):
    """Pixel picture of a periodic hexagon block (lengths in m, defect sizes as fractions).

    Returns s (solid fraction of every pixel, 0 in the pores), wall_t (real thickness of the
    wall a pixel belongs to), dx (pixel size), the block size and the fraction of wall removed.
    """
    rng = np.random.default_rng(int(seed))
    pitch = d + t
    centres, (lx, ly) = honeycomb.block(pitch, cells)
    dx = pitch / px_per_cell
    nx, ny = round(lx / dx), round(ly / dx)
    centres[:, 1] *= ny * dx / ly  # stretch y by < 1 % so the block is a whole number of pixels
    ly = ny * dx
    n = len(centres)
    centres += rng.normal(0, spread * pitch, centres.shape)  # cell-size spread
    # 3 × 3 periodic copies of the centres, so cells at the block edge see their real neighbours
    shifts = np.array([(a * lx, b * ly) for a in (-1, 0, 1) for b in (-1, 0, 1)])
    seeds = (centres[None, :, :] + shifts[:, None, :]).reshape(-1, 2)
    ids = np.tile(np.arange(n), 9)
    yy, xx = np.mgrid[0:ny, 0:nx]
    pts = np.column_stack([(xx.ravel() + 0.5) * dx, (yy.ravel() + 0.5) * dx])  # pixel centres

    # Each pixel belongs to its nearest cell centre (a). The wall it is closest to is the one
    # shared with the second-nearest centre (b): the perpendicular bisector of a-b.
    dist, k = cKDTree(seeds).query(pts, k=2)
    a, b = ids[k[:, 0]], ids[k[:, 1]]
    ca, cb = seeds[k[:, 0]], seeds[k[:, 1]]
    sep = np.linalg.norm(cb - ca, axis=1)
    gap = (dist[:, 1] ** 2 - dist[:, 0] ** 2) / (2 * sep)  # distance from pixel to that wall

    def per_wall(values):
        """One random number per wall, the same seen from both cells (a symmetric matrix)."""
        return np.triu(values) + np.triu(values, 1).T

    t_wall = t * np.clip(1 + wall_var * per_wall(rng.normal(0, 1, (n, n)))[a, b], 0.1, None)
    # shortcut: walls are drawn WALL_PX pixels wide (real t/d ≈ 0.01 would need ~400 px per cell
    # for 4 px per wall). Each drawn pixel holds the real wall plus the air it displaced, side by
    # side (solid fraction s = t/t_draw), so the wall conductance t·k_wall is kept. Thinner drawn
    # walls conduct badly as pixel staircases at ±30°. Upgrade: px_per_cell ≥ 400 so t_draw = t.
    t_draw = np.maximum(t_wall, WALL_PX * dx)
    wall = gap < t_draw / 2

    # Cracks: one gap per wall, length = cracks × wall length, at a random place along the wall.
    side = pitch / np.sqrt(3)  # wall length of a regular hexagon
    tangent = np.column_stack([-(cb - ca)[:, 1], (cb - ca)[:, 0]]) / sep[:, None]
    tangent *= np.where(a < b, 1, -1)[:, None]  # same direction seen from both cells
    along = ((pts - (ca + cb) / 2) * tangent).sum(axis=1)  # position along the wall
    centre = per_wall(rng.uniform(-0.5, 0.5, (n, n)))[a, b] * side * (1 - cracks)
    crack = wall & (np.abs(along - centre) < cracks * side / 2)
    removed = crack.sum() / max(wall.sum(), 1)
    wall &= ~crack

    s = np.where(wall, t_wall / t_draw, 0.0).reshape(ny, nx)
    wall_t = np.where(wall, t_wall, 0.0).reshape(ny, nx)
    return {"s": s, "wall_t": wall_t, "dx": dx, "box": (lx, ly), "removed": removed}


def run(structure, inputs, conditions):
    """Draw the picture, count its porosity (structure and conditions are unused here)."""
    honeycomb.check(inputs)
    cells = max(2, 2 * round(inputs["cells"] / 2))  # even, so the block is periodic
    px = int(inputs["px_per_cell"])
    if px < 10:
        raise ValueError("px_per_cell must be ≥ 10")
    d, t = inputs["d"] * 1e-6, inputs["t"] * 1e-6
    pic = picture(
        d, t, cells, px, inputs["spread"] / 100, inputs["wall_var"] / 100,
        inputs["cracks"] / 100, inputs["seed"],
    )  # fmt: skip
    phi = 1 - pic["s"].mean()  # counted porosity: pore area + the air inside drawn wall pixels
    rho_bulk = (1 - phi) * inputs["rho_wall"]
    wall = pic["s"] > 0
    stride = int(np.ceil(max(wall.shape) / 256))  # keep the 3D view small and fast
    view = ndimage.maximum_filter(wall, size=stride)[::stride, ::stride]
    scale = f"{max(WALL_PX, stride) * pic['dx'] / t:.0f}" if t > 0 else "∞"
    ny, nx = wall.shape
    return {
        "phi": phi,
        "rho_bulk": rho_bulk,
        "d": d,
        "t": t,
        "pitch": d + t,
        "T": inputs["T"],
        "pressure": inputs["pressure"] * 1e3,
        "notes": [
            f"counted porosity φ = {phi:.4f} (ideal formula (d/p)² = {(d / (d + t)) ** 2:.4f})",
            f"bulk density ρ = {rho_bulk:.1f} kg/m³",
            f"picture {nx} × {ny} px, pixel = {pic['dx'] * 1e6:.3f} µm, {cells} × {cells} cells",
            f"cracks remove {100 * pic['removed']:.1f} % of the wall pixels",
            f"walls drawn ≥ {WALL_PX} px wide; each wall pixel holds the real wall + displaced air",
        ],
        "_s": pic["s"],
        "_wall_t": pic["wall_t"],
        "_dx": pic["dx"],
        "_geometry": {
            "kind": "pixels",
            "box": [pic["box"][0] * 1e6, pic["box"][1] * 1e6],
            "wall": ["".join("1" if v else "0" for v in line) for line in view],
            "note": ui_text.WALL_NOTE.format(scale=scale),
        },
    }


def image_of(structure):
    """The pixel picture of a structure; the ideal honeycomb is drawn when it has none."""
    if "_s" in structure:
        return structure
    ideal = {k: v["value"] for k, v in INPUTS.items()}
    ideal |= {"d": structure["d"] * 1e6, "t": structure["t"] * 1e6}
    ideal |= {"spread": 0, "wall_var": 0, "cracks": 0}
    return run(None, ideal, {})


def distance_to_wall(wall):
    """Distance (px) from each pixel centre to the nearest wall pixel, in the repeating picture."""
    if not wall.any():
        return np.full(wall.shape, np.inf)
    n = max(wall.shape) // 2  # pad with the neighbouring copies so edge pixels see their walls
    return distance_transform_edt(~np.pad(wall, n, mode="wrap"))[n:-n, n:-n]
