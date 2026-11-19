"""Ideal hexagonal honeycomb: identical hex tubes along the freezing direction z."""

import numpy as np

from aerosim.core import ui_text

NAME = "Honeycomb"
LEVEL = "fast"
ORDER = 1
HELP = (
    "Ideal hexagonal tubes along the freezing direction z, all the same size, walls connected "
    "all round. Porosity and density follow from the pore size d and the wall thickness t; "
    "they are never set on their own."
    " ⚠ Accuracy: an idealised shape. Real freeze-cast cells are uneven, partly connected and "
    "cracked, and the measured values are out of reach of any air-filled model (k⊥ 16.9 "
    "mW/m·K in Chan et al. 2022, below the ≈ 26 mW/m·K air floor; anisotropy ≈ 5.8 against "
    "1.58 here). Compare trends, not absolute numbers."
)
EQUATION = "p = d + t,   φ = (d / p)²,   ρ_bulk = (1 − φ) ρ_wall"
SOURCE = "Hexagon geometry (d = inner flat-to-flat width); defaults from Chan et al. 2022"
COST = "instant"
INPUTS = {
    "d": {
        "value": 30.0,
        "unit": "µm",
        "status": "literature",
        "source": "Chan et al. 2022 (Kit's paper), Nat. Commun. 13:5553: pore size ≈ 30 µm",
        "help": "Pore size: the inner flat-to-flat width of one hexagonal channel.",
    },
    "t": {
        "value": 0.27,
        "unit": "µm",
        "status": "derived",
        "source": "chosen so that φ = (d/(d + t))² ≈ 0.982, the porosity in Chan et al. 2022",
        "help": "Wall thickness.",
    },
    "rho_wall": {
        "value": 1122.0,
        "unit": "kg/m³",
        "status": "derived",
        "source": "20.2 kg/m³ / (1 − 0.982): density and porosity from Chan et al. 2022",
        "help": "Density of the wall material itself (not of the aerogel).",
    },
    "T": {
        "value": 300.0,
        "unit": "K",
        "status": "hypothetical",
        "source": "chosen test condition: room temperature",
        "help": "Mean sample temperature. Used by the gas, radiation and convection rows.",
    },
    "pressure": {
        "value": 101.325,
        "unit": "kPa",
        "status": "hypothetical",
        "source": "chosen test condition: one standard atmosphere, sample in air",
        "help": "Air pressure in the pores. Lower it to see how vacuum insulation works.",
    },
}

VIEW_CELLS = 4  # cells per side of the block shown in 3D (and drawn by Honeycomb + defects)


def block(pitch, cells):
    """Centres of a cells × cells hexagon block that repeats periodically, and its size (m).

    Rows of hexagons are √3/2 · p apart; every second row is shifted by p/2.
    `cells` must be even so the block repeats in y as well.
    """
    row_gap = pitch * np.sqrt(3) / 2
    j, i = np.mgrid[0:cells, 0:cells]
    x = (i + 0.5 * (j % 2) + 0.25) * pitch
    y = (j + 0.5) * row_gap
    return np.column_stack([x.ravel(), y.ravel()]), (cells * pitch, cells * row_gap)


def check(inputs):
    """Refuse inputs that have no physical meaning."""
    for key in ("d", "rho_wall", "T", "pressure"):
        if inputs[key] <= 0:
            raise ValueError(f"{key} must be > 0")
    if inputs["t"] < 0:
        raise ValueError("t must be ≥ 0")


def run(structure, inputs, conditions):
    """Porosity and density of the ideal honeycomb (structure and conditions are unused here)."""
    check(inputs)
    d, t = inputs["d"] * 1e-6, inputs["t"] * 1e-6  # µm → m
    pitch = d + t  # centre-to-centre distance of two neighbouring channels
    phi = (d / pitch) ** 2  # pore area / cell area for a hexagon (area ∝ flat-to-flat width²)
    rho_bulk = (1 - phi) * inputs["rho_wall"]  # only the walls have mass
    centres, box = block(pitch, VIEW_CELLS)
    wall_draw = max(t, 0.06 * pitch)  # real walls (t/d ≈ 0.01) would be invisible in 3D
    scale = f"{wall_draw / t:.0f}" if t > 0 else "∞"
    return {
        "phi": phi,
        "rho_bulk": rho_bulk,
        "d": d,
        "t": t,
        "pitch": pitch,
        "T": inputs["T"],
        "pressure": inputs["pressure"] * 1e3,  # kPa → Pa
        "notes": [
            f"pitch p = d + t = {pitch * 1e6:.2f} µm",
            f"porosity φ = (d/p)² = {phi:.4f}",
            f"bulk density ρ = (1 − φ) ρ_wall = {rho_bulk:.1f} kg/m³",
        ],
        "_geometry": {
            "kind": "cells",
            "box": [box[0] * 1e6, box[1] * 1e6],
            "centres": (centres * 1e6).round(3).tolist(),
            "pitch": pitch * 1e6,
            "wall": wall_draw * 1e6,
            "note": ui_text.WALL_NOTE.format(scale=scale),
        },
    }
