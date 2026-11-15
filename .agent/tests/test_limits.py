"""Physical limits and trends of the fast methods, and the no-double-counting rule."""

import numpy as np
import pytest

from aerosim.solid.pixel_fv import solve


def test_no_pores_gives_the_wall_conductivity_along_z(state):
    state.run("structure", "honeycomb", {"d": 1e-4, "t": 10})  # φ ≈ 1e-10
    for row in ("solid", "gas", "radiation", "convection"):
        state.run(row, state.rows[row]["methods"][0]["key"])
    assert state.totals()["k_par"] == pytest.approx(4.0, rel=1e-6)


def test_no_walls_gives_the_gas(state):
    state.run("structure", "honeycomb", {"t": 0})  # φ = 1
    for row in ("solid", "gas", "radiation", "convection"):
        state.run(row, state.rows[row]["methods"][0]["key"])
    r, t = state.results, state.totals()
    assert r["solid"]["k_trans"] == 0 and r["solid"]["k_par"] == 0
    assert r["gas"]["k_trans"] == pytest.approx(r["gas"]["k_gas"])
    assert t["k_trans"] == pytest.approx(r["gas"]["k_gas"] + r["radiation"]["k_trans"])


def test_lower_pressure_lowers_gas_conduction(state):
    k = []
    for p in (101.325, 10, 1, 0.1):
        state.run("structure", "honeycomb", {"pressure": p})
        k.append(state.run("gas", "knudsen")["k_gas"])
    assert k == sorted(k, reverse=True) and k[-1] < 0.5 * k[0]


def test_radiation_grows_with_t_cubed(state):
    k = []
    for T in (300, 600):
        state.run("structure", "honeycomb", {"T": T})
        k.append(state.run("radiation", "opaque_walls")["k_trans"])
    assert k[1] / k[0] == pytest.approx(8, rel=1e-9)


def test_pixel_solver_uniform_and_series_layers():
    assert solve(np.full((20, 30), 2.5))[0] == pytest.approx(2.5, rel=1e-9)
    layers = np.ones((20, 40))
    layers[:, 20:] = 4.0  # two layers in series across x: k = 2/(1/1 + 1/4)
    assert solve(layers)[0] == pytest.approx(1.6, rel=1e-9)
    assert solve(layers.T)[0] == pytest.approx(2.5, rel=1e-9)  # the same layers in parallel


def test_coupled_result_is_not_added_twice(state):
    state.run("solid", "pixel_fv")
    t = state.totals()
    assert t["k_trans"] == pytest.approx(
        state.results["solid"]["k_trans"] + state.results["radiation"]["k_trans"]
    )
    assert "(solid+gas)" in t["k_trans_text"]
    assert any("Gas conduction not added" in n for n in t["notes"])


def test_structure_change_asks_to_rerun(state):
    state.run("structure", "honeycomb", {"d": 40})
    assert set(state.stale()) == {"Solid conduction", "Gas conduction", "Radiation", "Convection"}
    state.run("gas", "knudsen")
    assert "Gas conduction" not in state.stale()
