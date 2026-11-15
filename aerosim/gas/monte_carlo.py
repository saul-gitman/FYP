"""Monte Carlo gas conduction: virtual molecule flights measure the pore size the gas feels."""

import numpy as np

from aerosim.core.constants import k_air, knudsen_beta, mean_free_path
from aerosim.gas import ALPHA
from aerosim.structure.honeycomb_defects import distance_to_wall, image_of

NAME = "Monte Carlo"
LEVEL = "detailed"
ORDER = 3
HELP = (
    "Starts many virtual molecules at random points in the pores, flying in random 3D "
    "directions, and measures how far each straight flight goes from wall to wall. The mean "
    "flight (mean chord) is the pore size the gas really feels in this shape, cracks and "
    "corners included. Half of it is the equivalent plate gap, which goes into the Knudsen "
    "formula; for two parallel plates this gives exactly the Knudsen formula."
)
EQUATION = (
    "ℓ̄ = 1 / mean(1/ℓ_i) = 4V/S (mean chord),   d_eff = ℓ̄ / 2,   "
    "k_gas = k_air / (1 + 2 β λ / d_eff)"
)
SOURCE = "Mean chord 4V/S (Cauchy); wall-collision length S/(4φ) as in Zeng, Hunt & Greif 1995"
COST = "≈ 1 s"
INPUTS = {
    "alpha": ALPHA,
    "molecules": {
        "value": 20000,
        "unit": "",
        "status": "derived",
        "source": "numerical setting: about 1 % noise on the mean chord",
        "help": "Number of virtual molecules. More = less noise, slower.",
    },
    "seed": {
        "value": 1,
        "unit": "",
        "status": "derived",
        "source": "numerical setting: the same seed gives the same answer",
        "help": "Random seed.",
    },
}


def march(wall, start, step_dir, max_px):
    """Distance (px) from each start point to the first wall pixel along its direction.

    Each step is as long as the distance to the nearest wall (it cannot jump over one), and at
    least 0.25 px. The picture repeats periodically. Returns inf beyond max_px (no wall hit).
    """
    edt = distance_to_wall(wall)
    ny, nx = wall.shape
    pos, dist = start.copy(), np.zeros(len(start))
    alive = np.ones(len(start), bool)
    while alive.any():
        i = np.floor(pos[alive, 0]).astype(int) % nx
        j = np.floor(pos[alive, 1]).astype(int) % ny
        hit = wall[j, i]
        idx = np.flatnonzero(alive)
        alive[idx[hit]] = False
        idx = idx[~hit]
        step = np.maximum(edt[j[~hit], i[~hit]] - 1.0, 0.25)
        pos[idx] += step[:, None] * step_dir[idx]
        dist[idx] += step
        far = idx[dist[idx] > max_px]
        dist[far], alive[far] = np.inf, False
    return dist


def mean_chord(wall, n, rng):
    """Mean chord (px) of the pore space for 3D-isotropic straight lines; channels along z.

    A random point lies on a long chord more often than on a short one, so the plain mean of the
    sampled chords is biased; the harmonic mean removes that bias and equals Cauchy's 4V/S.
    """
    nx = wall.shape[1]
    pores = np.flatnonzero(~wall.ravel())
    pick = rng.choice(pores, n)
    start = np.column_stack([pick % nx, pick // nx]) + rng.random((n, 2))  # uniform in a pixel
    cos_z = rng.uniform(-1, 1, n)  # 3D isotropic: cos of the angle to z is uniform
    sin_z = np.sqrt(1 - cos_z**2)
    psi = rng.uniform(0, 2 * np.pi, n)
    plane = np.column_stack([np.cos(psi), np.sin(psi)])  # direction within the cross-section
    far = 20 * max(wall.shape)  # longer lines count as never hitting a wall (adds < 1/far)
    chord_in_plane = march(wall, start, plane, far) + march(wall, start, -plane, far)
    inv = sin_z / chord_in_plane  # 1/(3D chord); 0 for a line that never meets a wall
    return 1 / inv.mean() if inv.mean() > 0 else np.inf


def run(structure, inputs, conditions):
    pic = image_of(structure)
    rng = np.random.default_rng(int(inputs["seed"]))
    n = max(100, int(inputs["molecules"]))
    chord = mean_chord(pic["_s"] > 0, n, rng) * pic["_dx"]  # px → m
    d_eff = chord / 2  # two parallel plates a gap d apart have a mean chord 2d
    T, p = conditions["T"], conditions["pressure"]
    lam, beta = mean_free_path(T, p), knudsen_beta(inputs["alpha"])
    k_gas = k_air(T) / (1 + 2 * beta * lam / d_eff)
    phi = structure["phi"]
    return {
        "k_par": phi * k_gas,
        "k_trans": phi * k_gas,
        "covers": ["gas"],
        "k_gas": k_gas,
        "d_eff": d_eff,
        "notes": [
            f"mean chord ℓ̄ = {chord * 1e6:.2f} µm from {n} molecules → equivalent gap "
            + f"d_eff = {d_eff * 1e6:.2f} µm (input d = {structure['d'] * 1e6:.2f} µm)",
            f"Kn_eff = λ/d_eff = {lam / d_eff:.2e},  k_gas = {k_gas * 1e3:.2f} mW/m·K",
            f"contribution φ k_gas = {phi * k_gas * 1e3:.2f} mW/m·K",
            "a smooth hexagonal channel has ℓ̄ = d, so d_eff = d/2: twice the Knudsen effect "
            + "of the fast formula, which treats d as a plate gap; pixel staircase walls "
            + "shorten ℓ̄ by a further ≈ 10 % (a circle test gives 0.89 of 4V/S)",
        ],
    }
