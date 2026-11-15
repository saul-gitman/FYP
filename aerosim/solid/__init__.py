"""Solid conduction row: heat carried through the solid walls."""

ROW = "Solid conduction"
ORDER = 2
HELP = (
    "Heat carried through the solid walls of the skeleton (BN/CNF/MTMS surface aerogel). "
    "The wall material enters only through its own conductivity k_wall."
)
COLOR = "#d9822b"

# Shared by every method in this row, so the label wording lives in one place.
K_WALL = {
    "value": 4.0,
    "unit": "W/m·K",
    "status": "derived",
    "source": (
        "back-calculated from Chan et al. 2022 (Kit's paper), Nat. Commun. 13:5553: "
        "k_wall = (k_axial − φ k_air)/(1 − φ) with k_axial ≈ 5.8 × 16.9 mW/m·K, φ = 0.982"
    ),
    "help": "Conductivity of the wall material itself (not the aerogel).",
}
