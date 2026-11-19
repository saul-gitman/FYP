"""Lattice Boltzmann: simulate the buoyant air flow in one pore and measure the Nusselt number."""

import numpy as np

from aerosim.convection import DTDX
from aerosim.convection.rayleigh import rayleigh_number
from aerosim.core.constants import AIR_PR

NAME = "Lattice Boltzmann"
LEVEL = "detailed"
ORDER = 2
HELP = (
    "Simulates the air in one pore as a layer heated from below, at the pore's real Rayleigh "
    "number. Fluid 'particles' stream to neighbouring lattice nodes and collide; warm air is "
    "pushed up by buoyancy. The Nusselt number Nu compares the heat carried with pure "
    "conduction: Nu = 1 means the air stays still."
    " ⚠ Accuracy: a flat layer with periodic sides, not the hexagonal pore; real side walls "
    "only delay the onset, so this is on the safe side. It reproduces published "
    "Rayleigh–Bénard values (Nu 2.09 and 2.62 against ≈ 2.1 and 2.6 at Ra 5000 and 10 000)."
)
EQUATION = (
    "f_k(x + c_k, t + 1) = f_k − (f_k − f_k^eq)/τ (D2Q9 flow, D2Q5 heat, Boussinesq force);   "
    "Nu = 1 + ⟨v T⟩ H / (α ΔT);   k_conv = (Nu − 1) φ k_gas"
)
SOURCE = (
    "Shan 1997 (Phys. Rev. E 55:2780, Rayleigh–Bénard onset with LBM); "
    "Mohamad, Lattice Boltzmann Method (textbook codes)"
)
COST = "≈ 1 s"
INPUTS = {
    "dTdx": DTDX,
    "nodes": {
        "value": 21,
        "unit": "nodes",
        "status": "derived",
        "source": "numerical setting: lattice nodes across the layer height",
        "help": "Lattice nodes across the pore. More = more accurate, slower.",
    },
    "steps": {
        "value": 3000,
        "unit": "steps",
        "status": "derived",
        "source": "numerical setting: about one heat-diffusion time H²/α at small Ra",
        "help": "Time steps. Near the onset (Ra ≈ 1708–10⁴) use ≥ 40 000.",
    },
}
USES = ["gas"]  # k_conv is scaled with the gas conductivity

# D2Q9 lattice for the flow: rest, 4 axis and 4 diagonal directions, weights, opposites
C = np.array([(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)])
W = np.array([4 / 9] + [1 / 9] * 4 + [1 / 36] * 4)
OPP = [0, 3, 4, 1, 2, 7, 8, 5, 6]
W5 = np.array([1 / 3] + [1 / 6] * 4)  # D2Q5 for temperature: the first 5 directions of C


def nusselt(ra, pr=AIR_PR, height=21, steps=3000):
    """Nu of a fluid layer heated from below (T = 1 at the bottom, 0 at the top), periodic in x
    with width 2H (the most unstable wavelength ≈ 2.016 H). Lattice units: ΔT = 1, H = height."""
    ny, nx = height, 2 * height
    nu = min(0.1, 0.1 * ny / np.sqrt(ra / pr))  # keeps the flow speed below ~0.1 (low Mach)
    alpha = nu / pr
    g_beta = ra * nu * alpha / ny**3  # buoyancy per unit temperature, from the target Ra
    tau_f, tau_g = 3 * nu + 0.5, 3 * alpha + 0.5  # relaxation times from ν and α (c_s² = 1/3)
    y = (np.arange(ny) + 0.5)[:, None]  # walls sit half a node outside the first/last row
    x = np.arange(nx)[None, :]
    T = 1 - y / ny + 0.01 * np.sin(2 * np.pi * x / nx) * np.sin(np.pi * y / ny)  # + a nudge
    rho, ux, uy = np.ones((ny, nx)), np.zeros((ny, nx)), np.zeros((ny, nx))
    f = W[:, None, None] * rho
    g = W5[:, None, None] * T
    for _ in range(int(steps)):
        force = rho * g_beta * (T - 0.5)  # Boussinesq: warm air (T > mean) pushed up
        uy_eq = uy + tau_f * force / rho  # the force shifts the equilibrium velocity
        cu = 3 * (C[:, 0, None, None] * ux + C[:, 1, None, None] * uy_eq)
        feq = W[:, None, None] * rho * (1 + cu + 0.5 * cu**2 - 1.5 * (ux**2 + uy_eq**2))
        f_post = f - (f - feq) / tau_f  # collide
        geq = (
            W5[:, None, None]
            * T
            * (1 + 3 * (C[:5, 0, None, None] * ux + C[:5, 1, None, None] * uy))
        )
        g_post = g - (g - geq) / tau_g
        for k in range(9):  # stream: every population moves one node along its direction
            f[k] = np.roll(f_post[k], (C[k, 1], C[k, 0]), axis=(0, 1))
        for k in range(5):
            g[k] = np.roll(g_post[k], (C[k, 1], C[k, 0]), axis=(0, 1))
        # walls (half-way bounce-back): what went into a wall comes back the opposite way
        for k in (2, 5, 6):  # moving up: refill the bottom row from what moved down there
            f[k, 0] = f_post[OPP[k], 0]
        for k in (4, 7, 8):  # moving down: refill the top row
            f[k, -1] = f_post[OPP[k], -1]
        g[2, 0] = -g_post[4, 0] + 2 * W5[2] * 1.0  # hot bottom wall, T = 1 (anti-bounce-back)
        g[4, -1] = -g_post[2, -1] + 2 * W5[4] * 0.0  # cold top wall, T = 0
        rho = f.sum(axis=0)
        ux = (f * C[:, 0, None, None]).sum(axis=0) / rho
        uy = (f * C[:, 1, None, None]).sum(axis=0) / rho
        T = g.sum(axis=0)
    uy_real = uy + 0.5 * force / rho  # fluid velocity halfway through the force step
    return 1 + (uy_real * T).mean() * ny / alpha  # convective heat flux / conductive heat flux


def run(structure, inputs, conditions):
    ra = rayleigh_number(structure["d"], conditions["T"], inputs["dTdx"])
    height, steps = int(inputs["nodes"]), int(inputs["steps"])
    if height < 5 or steps < 1:
        raise ValueError("need nodes ≥ 5 and steps ≥ 1")
    nu_number = nusselt(ra, AIR_PR, height, steps)
    gas = conditions["results"]["gas"]
    excess = nu_number - 1 if abs(nu_number - 1) > 1e-9 else 0.0  # below 1e-9: round-off
    k_conv = excess * structure["phi"] * gas["k_gas"]
    notes = [
        f"Ra = {ra:.2e} (pore size d, ΔT = (dT/dx) d), Pr = {AIR_PR}",
        f"Nu = {nu_number:.6f} after {steps} steps on a {2 * height} × {height} lattice",
        f"k_conv = (Nu − 1) φ k_gas = {k_conv * 1e3:.3g} mW/m·K",
        "shortcut: a layer heated from below with periodic sides, not the hexagonal pore; "
        + "side walls only delay the onset",
    ]
    if ra > 1e5:
        notes.append("warning: Ra > 1e5, this small lattice is too coarse; results unreliable")
    return {"k_par": k_conv, "k_trans": k_conv, "covers": ["conv"], "Nu": nu_number, "notes": notes}
