"""Each detailed method reproduces its fast formula in the ideal case before it is trusted."""

import numpy as np
import pytest

from aerosim.convection.lattice_boltzmann import nusselt
from aerosim.core.constants import k_air, knudsen_beta, mean_free_path
from aerosim.gas.monte_carlo import mean_chord
from aerosim.radiation.ray_tracing import trace

IDEAL = {"spread": 0, "wall_var": 0, "cracks": 0}


def formula_trans(state):
    """φ k_gas + ½ (1 − φ) k_wall with the counted porosity of the current picture."""
    phi, k_gas = state.results["structure"]["phi"], state.results["gas"]["k_gas"]
    return phi * k_gas + 0.5 * (1 - phi) * 4.0


# ---------------- solid: pixel finite volume ----------------
def test_pixel_fv_ideal_honeycomb_matches_formula(state):
    state.run("structure", "honeycomb_defects", IDEAL)
    state.run("gas", "knudsen")
    r = state.run("solid", "pixel_fv")
    assert r["k_trans"] == pytest.approx(formula_trans(state), rel=0.05)
    assert r["k_x"] == pytest.approx(r["k_y"], rel=0.07)  # in-plane isotropy (pixel staircase)
    phi, k_gas = state.results["structure"]["phi"], state.results["gas"]["k_gas"]
    assert r["k_par"] == pytest.approx(phi * k_gas + (1 - phi) * 4.0, rel=1e-9)  # exact
    assert r["energy_error"] < 1e-8  # heat in = heat out


def test_pixel_fv_on_fast_honeycomb_draws_the_ideal_picture(state):
    r = state.run("solid", "pixel_fv")  # structure row is the fast Honeycomb here
    assert r["k_trans"] == pytest.approx(formula_trans(state), rel=0.05)


def test_pixel_fv_grid_refinement(state):
    k = []
    for px in (100, 200):
        state.run("structure", "honeycomb_defects", IDEAL | {"cells": 2, "px_per_cell": px})
        k.append(state.run("solid", "pixel_fv")["k_trans"])
    assert k[1] == pytest.approx(k[0], rel=0.03)


def test_cracks_cut_transverse_conduction_but_not_axial(state):
    state.run("structure", "honeycomb_defects", IDEAL)
    ideal = state.run("solid", "pixel_fv")
    state.run("structure", "honeycomb_defects", IDEAL | {"cracks": 5})
    cracked = state.run("solid", "pixel_fv")
    assert cracked["k_trans"] < 0.9 * ideal["k_trans"]
    assert cracked["k_par"] == pytest.approx(ideal["k_par"], rel=0.05)


# ---------------- gas: local Knudsen and Monte Carlo ----------------
def test_local_knudsen_wide_pores_give_the_fast_value(state):
    fast = state.results["gas"]["k_gas"]
    assert state.run("gas", "local_knudsen")["k_gas"] == pytest.approx(fast, rel=0.01)


def test_local_knudsen_follows_the_formula_at_low_pressure(state):
    state.run("structure", "honeycomb", {"pressure": 1.0})  # Kn ≈ 0.2
    fast = state.run("gas", "knudsen")["k_gas"]
    local = state.run("gas", "local_knudsen")["k_gas"]
    assert local == pytest.approx(fast, rel=0.10) and local < fast  # corners conduct less


def test_monte_carlo_parallel_plates_match_knudsen():
    gap = 100  # px between two wall rows
    wall = np.zeros((gap + 2, 50), bool)
    wall[0], wall[-1] = True, True
    d_eff = mean_chord(wall, 20000, np.random.default_rng(1)) / 2 / gap  # in units of the gap
    beta = knudsen_beta(1.0)
    for kn in (0.01, 0.1, 1.0, 10.0):
        mc = 1 / (1 + 2 * beta * kn / d_eff)  # k_gas / k_air with the Monte Carlo gap
        formula = 1 / (1 + 2 * beta * kn)
        assert mc == pytest.approx(formula, rel=0.03), kn


def test_monte_carlo_free_space_limit():
    wall = np.zeros((40, 40), bool)  # no walls: molecules never hit anything
    chord = mean_chord(wall, 1000, np.random.default_rng(1))
    assert chord == np.inf  # so k_gas → k_air (λ_eff → λ)


def test_monte_carlo_runs_on_the_honeycomb(state):
    r = state.run("gas", "monte_carlo")
    assert 0.9 * k_air(300) < r["k_gas"] < k_air(300)
    lam = mean_free_path(300, 101325)
    assert lam / r["d_eff"] > lam / 30e-6  # a hexagonal channel feels a smaller gap than d


# ---------------- radiation: ray tracing ----------------
def test_ray_tracing_energy_is_conserved_and_empty_slab_transmits_all():
    rng = np.random.default_rng(1)
    wall_t = np.zeros((50, 50))
    wall_t[:, 20:24] = 0.3e-6  # one semi-transparent wall
    for kappa, refl in ((1e6, 0.1), (1e12, 0.5)):
        t, r, a, lost, _ = trace(wall_t, 80, kappa, refl, 5000, rng)
        assert t + r + a == pytest.approx(1.0, abs=1e-12) and lost < 1e-3
    t, r, a, lost, _ = trace(np.zeros((50, 50)), 200, 1e6, 0.1, 5000, rng)
    assert t == 1.0


def test_ray_tracing_opaque_walls_close_to_the_opaque_formula(state):
    opaque = state.run("radiation", "opaque_walls")["k_trans"]
    traced = state.run("radiation", "ray_tracing", {"kappa": 1e12})["k_trans"]
    assert 0.1 < traced / opaque < 10  # same order of magnitude (here within ~5 %)


# ---------------- convection: lattice Boltzmann ----------------
def test_lattice_boltzmann_physical_pore_has_no_convection(state):
    r = state.run("convection", "lattice_boltzmann")
    assert r["Nu"] == pytest.approx(1.0, abs=1e-6) and abs(r["k_trans"]) < 1e-9


@pytest.mark.slow
def test_lattice_boltzmann_onset_near_1708():
    assert nusselt(1500, steps=20000) == pytest.approx(1.0, abs=0.01)  # below onset
    assert nusselt(5000, steps=20000) > 1.5  # clearly above onset (literature Nu ≈ 2.1)
