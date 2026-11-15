"""Rayleigh check: can buoyancy start the air moving inside one pore?"""

from aerosim.convection import DTDX
from aerosim.core.constants import AIR_ALPHA_300, AIR_NU_300, G

NAME = "Rayleigh"
LEVEL = "fast"
ORDER = 1
HELP = (
    "Computes the Rayleigh number of one pore: buoyancy pushing warm air up against viscosity "
    "and heat diffusion holding it still. Below Ra ≈ 1708 (a layer heated from below) the air "
    "stays still and k_conv = 0."
)
EQUATION = "Ra = g β_T ΔT d³ / (ν α),   β_T = 1/T,   ΔT = (dT/dx) d;   Ra < 1708 → k_conv = 0"
SOURCE = (
    "Incropera (Rayleigh–Bénard onset 1708; air ν, α at 300 K, Table A.4); "
    "Skochdopole 1961 via NIST NBSIR 82-1664 (no convection in cells below ≈ 3–4 mm)"
)
COST = "instant"
INPUTS = {"dTdx": DTDX}
RA_CRITICAL = 1708  # onset for a fluid layer heated from below between rigid plates


def rayleigh_number(d, T, dTdx):
    """Ra of one pore of size d (m). ν and α are air at 300 K (shortcut: not varied with T)."""
    return G * (1 / T) * (dTdx * d) * d**3 / (AIR_NU_300 * AIR_ALPHA_300)


def run(structure, inputs, conditions):
    ra = rayleigh_number(structure["d"], conditions["T"], inputs["dTdx"])
    if ra < RA_CRITICAL:
        note = f"Ra = {ra:.2e} < {RA_CRITICAL}: the air cannot start moving, k_conv = 0"
    else:
        note = (
            f"warning: Ra = {ra:.2e} ≥ {RA_CRITICAL}: convection may start; the formula cannot "
            + "estimate it, so k_conv = 0 is shown. Run Lattice Boltzmann."
        )
    return {"k_par": 0.0, "k_trans": 0.0, "covers": ["conv"], "Ra": ra, "notes": [note]}
