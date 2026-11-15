"""Solid conduction by formula: thin walls in parallel along z, cos² average across."""

from aerosim.solid import K_WALL

NAME = "Formula"
LEVEL = "fast"
ORDER = 1
HELP = (
    "Along the channels the walls are straight strips beside the air, like resistors in "
    "parallel. Across a honeycomb the walls point in three directions (0°, 60°, 120°) and only "
    "their part along the heat flow carries heat; the cos² average of the three is one half."
)
EQUATION = "k_solid,∥ = (1 − φ) k_wall,   k_solid,⊥ = ½ (1 − φ) k_wall"
SOURCE = (
    "Thin-wall cellular model: 2D analogue of the ⅓ foam strut factor "
    "(Collishaw & Evans 1994, J. Mater. Sci. 29:2261)"
)
COST = "instant"
INPUTS = {"k_wall": K_WALL}


def run(structure, inputs, conditions):
    solid = 1 - structure["phi"]  # area fraction of wall in the cross-section
    k_par = solid * inputs["k_wall"]  # walls in parallel with the heat flow along z
    k_trans = 0.5 * solid * inputs["k_wall"]  # mean of cos²(0°), cos²(60°), cos²(120°) = ½
    return {
        "k_par": k_par,
        "k_trans": k_trans,
        "covers": ["solid"],
        "notes": [
            f"1 − φ = {solid:.4f}",
            f"k_solid,∥ = {k_par * 1e3:.2f} mW/m·K,  k_solid,⊥ = {k_trans * 1e3:.2f} mW/m·K",
        ],
    }
