"""Rosseland radiation: radiation diffuses through an optically thick medium like heat."""

from aerosim.core.constants import SIGMA
from aerosim.radiation import L_SAMPLE

NAME = "Rosseland"
LEVEL = "fast"
ORDER = 2
HELP = (
    "If the aerogel absorbs and scatters infrared strongly, radiation moves through it in many "
    "short steps and behaves like heat conduction. Only valid if the sample is optically "
    "thick (τ = e ρ L well above 1); a warning is shown when τ < 3."
)
EQUATION = "k_rad = 16 n² σ T³ / (3 e ρ_bulk),   τ = e ρ_bulk L"
SOURCE = "Hrubesh & Pekala 1994 (J. Mater. Res. 9:731); Lou et al. 2023 (Gels 9:220)"
COST = "instant"
INPUTS = {
    "e": {
        "value": 30.0,
        "unit": "m²/kg",
        "status": "hypothetical",
        "source": "assumed order of magnitude; unknown for BN/CNF/MTMS walls (needs IR spectra)",
        "help": "Specific extinction: how strongly 1 kg of material per m² blocks infrared.",
    },
    "n": {
        "value": 1.0,
        "unit": "",
        "status": "literature",
        "source": "refractive index of air ≈ 1 (the medium is ≈ 98 % air)",
        "help": "Effective refractive index of the medium.",
    },
    "L": L_SAMPLE,
}


def run(structure, inputs, conditions):
    if inputs["e"] <= 0 or inputs["L"] <= 0:
        raise ValueError("e and L must be > 0")
    T, rho = conditions["T"], structure["rho_bulk"]
    beta = inputs["e"] * rho  # extinction coefficient, 1/m
    k_rad = 16 * inputs["n"] ** 2 * SIGMA * T**3 / (3 * beta)
    tau = beta * inputs["L"] * 1e-3  # optical thickness of the sample (mm → m)
    notes = [
        f"β = e ρ = {beta:.0f} 1/m,  optical thickness τ = {tau:.2f}",
        f"k_rad = {k_rad * 1e3:.3f} mW/m·K, used along and across the channels",
    ]
    if tau < 3:
        notes.append(f"warning: τ = {tau:.2f} < 3, the sample is not optically thick; "
                     "Rosseland is not valid here")  # fmt: skip
    return {"k_par": k_rad, "k_trans": k_rad, "covers": ["rad"], "tau": tau, "notes": notes}
