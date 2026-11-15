"""Radiation with opaque walls: each pore is a gap between two grey walls."""

from aerosim.core.constants import SIGMA

NAME = "Opaque"
LEVEL = "fast"
ORDER = 1
HELP = (
    "Treats each pore as a gap of width d between two opaque grey walls that exchange "
    "radiation, like two large parallel plates. Bigger pores and hotter samples give more "
    "radiation. Used for both directions as a first approximation."
)
EQUATION = "k_rad = 4 σ T³ d · ε / (2 − ε)"
SOURCE = "Incropera, radiation exchange between parallel grey surfaces, linearised in ΔT"
COST = "instant"
INPUTS = {
    "eps": {
        "value": 0.9,
        "unit": "",
        "status": "hypothetical",
        "source": "assumed; the infrared emissivity of BN/CNF/MTMS walls is not measured",
        "help": "Infrared emissivity of the wall surface (0 = mirror, 1 = black).",
    },
}


def run(structure, inputs, conditions):
    eps = inputs["eps"]
    if not 0 < eps <= 1:
        raise ValueError("eps must be in (0, 1]")
    T = conditions["T"]
    # net exchange between two grey plates: σ(T1⁴ − T2⁴)/(2/ε − 1) ≈ 4σT³ ΔT · ε/(2 − ε)
    k_rad = 4 * SIGMA * T**3 * structure["d"] * eps / (2 - eps)
    return {
        "k_par": k_rad,
        "k_trans": k_rad,
        "covers": ["rad"],
        "notes": [
            f"k_rad = {k_rad * 1e3:.3f} mW/m·K at T = {T:.0f} K, d = {structure['d'] * 1e6:.1f} µm",
            "same value used along and across the channels (first approximation)",
        ],
    }
