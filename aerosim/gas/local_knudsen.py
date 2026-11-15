"""Local Knudsen: the Knudsen formula applied pixel by pixel with the local pore size."""

import numpy as np
from scipy.ndimage import distance_transform_edt

from aerosim.core.constants import k_air, knudsen_beta, mean_free_path
from aerosim.gas import ALPHA
from aerosim.structure.honeycomb_defects import image_of

NAME = "Local Kn"
LEVEL = "detailed"
ORDER = 2
HELP = (
    "Finds the local pore size at every air pixel of the picture: the diameter of the largest "
    "circle that fits in the pore and covers that pixel. Narrow cracks and corners get a small "
    "size, so the air there conducts less. The result is a map of gas conductivity."
)
EQUATION = "d_local(x) = local thickness of the pore,   k_gas(x) = k_air / (1 + 2 β λ / d_local(x))"
SOURCE = "Local thickness from scipy.ndimage distance transform (cf. PoreSpy local_thickness)"
COST = "≈ 0.5 s"
INPUTS = {"alpha": ALPHA}


def local_thickness(pore, dx, steps=40):
    """Diameter (m) of the largest circle inside the pore that covers each pixel.

    For a growing radius r: the pixels at least r from a wall can be circle centres; every
    pixel within r of such a centre lies inside a circle of diameter 2r.
    """
    edt = distance_transform_edt(pore) - 0.5  # px from a pixel centre to the wall surface
    size = np.zeros(pore.shape)
    for r in np.linspace(0.5, edt.max(), steps):
        centres = edt >= r
        if not centres.any():
            break
        covered = distance_transform_edt(~centres) <= r
        size[covered & pore] = 2 * r * dx
    return size


def run(structure, inputs, conditions):
    pic = image_of(structure)
    pore = pic["_s"] == 0
    n = round(structure["pitch"] / pic["_dx"])  # one cell of padding: the picture repeats
    size = local_thickness(np.pad(pore, n, mode="wrap"), pic["_dx"])[n:-n, n:-n]
    T, p = conditions["T"], conditions["pressure"]
    lam, beta = mean_free_path(T, p), knudsen_beta(inputs["alpha"])
    k_map = k_air(T) / (1 + 2 * beta * lam / np.where(pore, size, np.inf))
    k_gas = k_map[pore].mean()  # area average over the air pixels
    k_map[~pore] = k_gas  # wall pixels: their air part takes the mean (used by Pixel FV)
    phi = structure["phi"]
    stride = int(np.ceil(max(pore.shape) / 128))
    return {
        "k_par": phi * k_gas,
        "k_trans": phi * k_gas,
        "covers": ["gas"],
        "k_gas": k_gas,
        "notes": [
            f"mean local pore size = {size[pore].mean() * 1e6:.2f} µm "
            + f"(input d = {structure['d'] * 1e6:.2f} µm), λ = {lam * 1e9:.1f} nm",
            f"k_gas: area mean {k_gas * 1e3:.2f}, lowest {k_map[pore].min() * 1e3:.2f} mW/m·K",
            f"contribution φ k_gas = {phi * k_gas * 1e3:.2f} mW/m·K",
        ],
        "field": {
            "name": "Local gas conductivity (mW/m·K)",
            "values": (k_map[::stride, ::stride] * 1e3).round(3).tolist(),
            "low": "low",
            "high": "high",
        },
        "_k_gas_map": k_map,
    }
