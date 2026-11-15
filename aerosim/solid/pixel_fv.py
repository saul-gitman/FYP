"""Pixel finite-volume conduction: each pixel is a small thermal resistor."""

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

from aerosim.solid import K_WALL
from aerosim.structure.honeycomb_defects import image_of

NAME = "Pixel FV"
LEVEL = "detailed"
ORDER = 2
HELP = (
    "Splits the cross-section into pixels; each one is wall or air. Heat in = heat out at every "
    "pixel gives the temperature field, and the heat that flows gives k⊥. The picture repeats "
    "like wallpaper with a fixed temperature drop per copy, so there are no edge effects. "
    "Sees cracks and irregular cells. Air pixels use the Gas row's result, so solid and gas "
    "are solved together (their coupling included) and the Gas row is not added again."
)
EQUATION = (
    "Σ_neighbours G_ij (T_j − T_i) = 0,   G_ij = 2 k_i k_j / (k_i + k_j);   "
    "periodic, T drops ΔT per period;   k⊥ = Q L / (A ΔT);   k∥ = mean pixel k"
)
SOURCE = "Finite-volume method (Patankar 1980). Optional cross-check: NASA PuMA, TauFactor 2"
COST = "≈ 3 s"
INPUTS = {"k_wall": K_WALL}
USES = ["gas"]  # air pixels take the gas conductivity from the Gas row


def solve(k):
    """Steady conduction on a pixel map k (W/m·K) that repeats like wallpaper in x and y.

    The temperature drops by ΔT = 1 K over one period in x: crossing from the last column to
    the first one (the next copy of the block) costs an extra 1 K. This is the standard way to
    get the conductivity of a repeating structure without edge effects. Square pixels and unit
    depth, so the conductance between two pixel centres is simply the face conductivity.
    Returns k_eff along x, the temperature map and the energy-balance error.
    """
    ny, nx = k.shape
    idx = np.arange(nx * ny).reshape(ny, nx)
    k_right, k_up = np.roll(k, -1, axis=1), np.roll(k, -1, axis=0)  # neighbours (wrapping)
    gx = 2 * k * k_right / (k + k_right)  # harmonic mean: two half-pixel resistors in series
    gy = 2 * k * k_up / (k + k_up)
    rows, cols, vals = [], [], []
    for nb, g in ((np.roll(idx, -1, axis=1), gx), (np.roll(idx, -1, axis=0), gy)):
        i, j, g = idx.ravel(), nb.ravel(), g.ravel()
        rows += [i, j, i, j]  # heat balance: +G on each pixel's own diagonal, −G to the other
        cols += [i, j, j, i]
        vals += [g, g, -g, -g]
    # one link from pixel 0 to 0 K fixes the arbitrary temperature level; it carries no heat
    rows.append([0])
    cols.append([0])
    vals.append([k.mean()])
    A = coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols)))).tocsr()
    b = np.zeros(nx * ny)
    g_jump = gx[:, -1]  # links from the last column to the first column of the next copy
    b[idx[:, -1]] -= g_jump * 1.0  # heat flow over such a link is G (T_last − T_first + 1 K)
    b[idx[:, 0]] += g_jump * 1.0
    T = spsolve(A, b, permc_spec="MMD_AT_PLUS_A").reshape(ny, nx)
    q = np.sum(g_jump * (T[:, -1] - T[:, 0] + 1.0))  # heat crossing the jump
    m = nx // 2
    q_mid = np.sum(gx[:, m - 1] * (T[:, m - 1] - T[:, m]))  # must equal q: heat in = heat out
    k_eff = q * nx / ny  # k = Q L / (A ΔT) with L = nx px, A = ny px × unit depth, ΔT = 1 K
    return k_eff, T - T.min(), abs(q - q_mid) / q


def run(structure, inputs, conditions):
    pic = image_of(structure)
    s = pic["_s"]  # solid fraction of each pixel (0 = air)
    gas = conditions["results"]["gas"]
    k_gas = gas.get("_k_gas_map", gas["k_gas"])  # a per-pixel map (Local Kn) or one number
    if np.shape(k_gas) not in ((), s.shape):  # the map was made on another picture
        k_gas = gas["k_gas"]
    # a pixel holds the real wall and air side by side (parallel), see Honeycomb + defects
    k = s * inputs["k_wall"] + (1 - s) * k_gas
    kx, T, err_x = solve(k)
    ky, _, err_y = solve(k.T)
    k_trans = (kx + ky) / 2
    k_par = k.mean()  # along the straight channels every pixel is a resistor in parallel: exact
    stride = int(np.ceil(max(T.shape) / 128))  # small enough for the 3D view
    return {
        "k_par": k_par,
        "k_trans": k_trans,
        "covers": ["solid", "gas"],
        "k_x": kx,
        "k_y": ky,
        "energy_error": max(err_x, err_y),
        "notes": [
            f"k⊥ along x = {kx * 1e3:.2f}, along y = {ky * 1e3:.2f} mW/m·K (k⊥ = their mean)",
            f"k∥ = mean pixel k = {k_par * 1e3:.2f} mW/m·K (exact for straight channels)",
            f"energy balance: |Q_in − Q_out| / Q_in = {max(err_x, err_y):.1e}",
            f"{s.shape[1]} × {s.shape[0]} px; air pixels use the {gas['method']} gas result",
            "covers solid + gas together: the Gas row is not added again",
        ],
        "field": {
            "name": "Temperature (heat flows along x, left → right)",
            "values": T[::stride, ::stride].round(3).tolist(),
            "low": "cold",
            "high": "hot",
        },
    }
