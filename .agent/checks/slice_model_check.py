"""Check the honeycomb slice model in docs/FUTURE_WORK.md: closed forms, bounds, repo defaults.

Run from the repo root after `pip install -e .`:  python .agent/checks/slice_model_check.py
Geometry as in the slides: flat-top hexagons, inner side l, wall t, unit cell L × H = √3 p × p.
"""

import numpy as np

from aerosim.core.constants import k_air, knudsen_beta, mean_free_path
from aerosim.solid.pixel_fv import solve

S3 = np.sqrt(3)


def closed_form(side, t, kw, kh):
    """k_eff along the slides' x and y from the slice (isothermal-slice) model, §A.2."""
    D1, D2 = kw * t + S3 * kh * side, (4 * kw - 3 * kh) * t + S3 * kh * side
    E1 = 3 * S3 * kw * t + (3 * kw + 6 * kh) * side
    E2 = S3 * (4 * kw - kh) * t + (3 * kw + 6 * kh) * side

    def lm(a, b):  # logarithmic mean; equal arguments when k_w = k_h
        return a if np.isclose(a, b) else (b - a) / np.log(b / a)

    Rx = 2 * side / D1 + 2 * S3 * t / lm(D1, D2) + (side - S3 * t) / D2
    Ry = 6 * t / lm(E1, E2) + (3 * side - S3 * t) / ((4 * kw - kh) * t + 3 * S3 * kh * side)
    L, H = 3 * side + S3 * t, S3 * side + t
    return L / (H * Rx), H / (L * Ry)


def picture(side, t, kw, kh, px_per_l):
    """Pixel map k[y, x] of one periodic L × H unit (cells at the corners and the centre)."""
    L, H = 3 * side + S3 * t, S3 * side + t
    nx, ny = round(L * px_per_l), round(H * px_per_l)  # shortcut: pixels square to < 0.2 %
    x, y = np.meshgrid((np.arange(nx) + 0.5) * L / nx, (np.arange(ny) + 0.5) * H / ny)
    cell = np.zeros_like(x, dtype=bool)
    for cx, cy in ((0, 0), (L, 0), (0, H), (L, H), (L / 2, H / 2)):
        dx, dy = np.abs(x - cx), np.abs(y - cy)
        cell |= (dy <= S3 * side / 2) & (S3 * dx + dy <= S3 * side)
    return np.where(cell, kh, kw)


def raster_bounds(k):
    """Along x: slices (columns at one T) → upper bound on k; lanes (rows, no cross-flow) → lower.

    Pixel units: square pixels, so lengths cancel."""
    ny, nx = k.shape
    k_slice = nx / np.sum(1 / k.sum(axis=0)) / ny
    k_lane = np.sum(1 / np.sum(1 / k, axis=1)) * nx / ny
    return k_slice, k_lane


def main():
    print("Slice model vs pixel FV (repo solver) vs lanes, l = 1, 200 px per l; k in units of k_h")
    print(" t/l   kw/kh |  slice x  raster  lane x   FV x |  slice y  raster  lane y   FV y")
    for t in (0.1, 0.3):
        for kw, kh in ((1, 1), (10, 1), (1, 10), (200, 0.026)):
            sx, sy = closed_form(1.0, t, kw, kh)
            k = picture(1.0, t, kw, kh, 200)
            row, ratio = [f"{t:4}  {kw / kh:6.4g} |"], []
            for s, kk in ((sx, k), (sy, k.T)):
                rs, lane = raster_bounds(kk)
                fv = solve(kk)[0]
                assert abs(rs / s - 1) < 0.01, "closed form disagrees with the raster slices"
                assert lane <= fv * 1.0001 and fv <= s * 1.01, "FV outside the bounds"
                row.append(f" {s / kh:7.4g} {rs / kh:7.4g} {lane / kh:7.4g} {fv / kh:6.4g} |")
                ratio.append(fv / s)  # = R_slice / R_true
            print("".join(row), f" R_slice/R_FV: x {ratio[0]:.2f}, y {ratio[1]:.2f}")
    uniform = closed_form(1.0, 0.2, 3.0, 3.0)
    assert np.allclose(uniform, 3.0), "uniform material must give back k"

    d, t, kw, T, p = 30e-6, 0.27e-6, 4.0, 300.0, 101325.0  # repo defaults
    kg = k_air(T) / (1 + 2 * knudsen_beta() * mean_free_path(T, p) / d)
    phi = (d / (d + t)) ** 2
    sx, sy = closed_form(d / S3, t, kw, kg)
    k = picture(d / S3, t, kw, kg, 200 / (d / S3))
    lane = raster_bounds(k.T)[1]
    print(f"\nRepo defaults: k_gas = {kg * 1e3:.2f} mW/m·K, φ = {phi:.5f}, t/l = {t * S3 / d:.4f}")
    print(f"formula φ k_gas + ½(1 − φ) k_wall = {(phi * kg + 0.5 * (1 - phi) * kw) * 1e3:.1f}")
    print(f"slice model: slides' x {sx * 1e3:.1f}, slides' y {sy * 1e3:.1f} mW/m·K (upper bounds)")
    print(f"lanes, slides' y: {lane * 1e3:.1f} mW/m·K (lower bound; every lane crosses air)")
    hs_up = kw + phi / (1 / (kg - kw) + (1 - phi) / (2 * kw))  # 2-D Hashin–Shtrikman, isotropic
    hs_lo = kg + (1 - phi) / (1 / (kw - kg) + phi / (2 * kg))
    print(f"Hashin–Shtrikman 2-D: {hs_lo * 1e3:.1f} ≤ k⊥ ≤ {hs_up * 1e3:.1f} mW/m·K")
    assert lane <= hs_lo and hs_up <= min(sx, sy), "HS must be inside slice/lane here"


if __name__ == "__main__":
    main()
