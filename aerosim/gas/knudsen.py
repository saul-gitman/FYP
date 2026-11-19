"""Gas conduction by the Knudsen formula, with one pore size d."""

from aerosim.core.constants import k_air, knudsen_beta, mean_free_path
from aerosim.gas import ALPHA

NAME = "Knudsen"
LEVEL = "fast"
ORDER = 1
HELP = (
    "Free air conductivity from the standard table, reduced when the pore size d is not much "
    "bigger than the molecules' mean free path λ (≈ 66 nm in air at 300 K, 1 atm). The air "
    "fills a fraction φ of the cross-section, in both directions (thin-wall limit)."
    " ⚠ Accuracy: treats d as a plate gap, but a hexagonal channel behaves like a gap of "
    "about d/2 (see Monte Carlo), so k_gas comes out slightly high at low pressure. At 30 µm "
    "and 1 atm the difference is < 1 %. The accommodation coefficient α = 1 is hypothetical."
)
EQUATION = (
    "λ = k_B T / (√2 π d_g² p),   Kn = λ / d,   k_gas = k_air / (1 + 2 β Kn),   "
    "β = ((2 − α)/α) · (2γ/(γ + 1)) / Pr,   contribution = φ k_gas"
)
SOURCE = "Kaganer 1969; Zeng, Hunt & Greif 1995 (J. Heat Transfer 117:758); Incropera Table A.4"
COST = "instant"
INPUTS = {"alpha": ALPHA}


def knudsen(T, pressure, d, alpha):
    """k_gas (W/m·K) in a pore of size d (m), plus λ, Kn and β."""
    lam = mean_free_path(T, pressure)
    kn = lam / d
    beta = knudsen_beta(alpha)
    return k_air(T) / (1 + 2 * beta * kn), lam, kn, beta


def run(structure, inputs, conditions):
    T, p = conditions["T"], conditions["pressure"]
    k_gas, lam, kn, beta = knudsen(T, p, structure["d"], inputs["alpha"])
    phi = structure["phi"]
    notes = [
        f"k_air({T:.0f} K) = {k_air(T) * 1e3:.2f} mW/m·K (Incropera Table A.4)",
        f"λ = {lam * 1e9:.1f} nm,  Kn = λ/d = {kn:.2e},  β = {beta:.3f}",
        f"k_gas = {k_gas * 1e3:.2f} mW/m·K;  contribution φ k_gas = {phi * k_gas * 1e3:.2f}",
    ]
    if not 250 <= T <= 400:
        notes.append("T is outside the air table (250–400 K): k_air is held at the end value")
    return {
        "k_par": phi * k_gas,
        "k_trans": phi * k_gas,
        "covers": ["gas"],
        "k_gas": k_gas,
        "Kn": kn,
        "notes": notes,
    }
