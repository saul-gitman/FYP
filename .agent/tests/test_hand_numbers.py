"""The fast methods at the defaults reproduce the hand calculation (docs/PHYSICS.md §7)."""

import math

import pytest

# Hand calculation, written out independently of the code
D, T_WALL, K_WALL, TEMP, P = 30e-6, 0.27e-6, 4.0, 300.0, 101325.0
PHI = (D / (D + T_WALL)) ** 2
LAM = 1.380649e-23 * TEMP / (math.sqrt(2) * math.pi * (3.72e-10) ** 2 * P)
BETA = (2 * 1.4 / 2.4) / 0.71
K_GAS = 26.3e-3 / (1 + 2 * BETA * LAM / D)
K_RAD = 4 * 5.670374419e-8 * TEMP**3 * D * 0.9 / (2 - 0.9)
K_TRANS = 0.5 * (1 - PHI) * K_WALL + PHI * K_GAS + K_RAD
K_PAR = (1 - PHI) * K_WALL + PHI * K_GAS + K_RAD


def test_exact_match_with_the_hand_calculation(state):
    r = state.results
    assert r["structure"]["phi"] == pytest.approx(PHI, rel=1e-12)
    assert r["gas"]["k_gas"] == pytest.approx(K_GAS, rel=1e-12)
    assert r["radiation"]["k_trans"] == pytest.approx(K_RAD, rel=1e-12)
    t = state.totals()
    assert t["k_trans"] == pytest.approx(K_TRANS, rel=1e-12)
    assert t["k_par"] == pytest.approx(K_PAR, rel=1e-12)


def test_rounded_anchor_numbers(state):
    """The numbers quoted in SUBAGENT_GUIDE A4 (mW/m·K)."""
    r, t = state.results, state.totals()
    assert r["structure"]["phi"] == pytest.approx(0.9822, abs=5e-5)
    assert LAM == pytest.approx(66e-9, rel=0.02)
    assert BETA == pytest.approx(1.64, abs=0.01)
    assert r["gas"]["k_gas"] * 1e3 == pytest.approx(26.1, abs=0.05)
    assert r["solid"]["k_trans"] * 1e3 == pytest.approx(35.5, abs=0.05)
    assert r["solid"]["k_par"] * 1e3 == pytest.approx(71.0, abs=0.05)
    assert r["gas"]["k_trans"] * 1e3 == pytest.approx(25.6, abs=0.05)
    assert r["radiation"]["k_trans"] * 1e3 == pytest.approx(0.15, abs=0.005)
    assert r["convection"]["k_trans"] == 0
    assert t["k_trans"] * 1e3 == pytest.approx(61.3, abs=0.05)
    assert t["k_par"] * 1e3 == pytest.approx(96.8, abs=0.05)
    assert t["anisotropy"] == pytest.approx(1.58, abs=0.005)


def test_footer_formula_text(state):
    t = state.totals()
    assert t["k_trans_text"] == "k⊥ = 35.5 + 25.6 + 0.150 + 0.00 = 61.3 mW/m·K"
    assert t["k_par_text"] == "k∥ = 71.0 + 25.6 + 0.150 + 0.00 = 96.8 mW/m·K"
    assert t["formula"] == "k_total = k_solid + k_gas + k_rad + k_conv"


def test_rosseland_warns_when_optically_thin(state):
    r = state.run("radiation", "rosseland")
    assert r["tau"] < 3 and any("not optically thick" in n for n in r["notes"])


def test_rayleigh_number_is_tiny_and_warns_above_onset(state):
    r = state.run("convection", "rayleigh")
    assert r["Ra"] < 1e-6 and r["k_trans"] == 0
    state.run("structure", "honeycomb", {"d": 20000})  # a 20 mm pore
    r = state.run("convection", "rayleigh")
    assert r["Ra"] > 1708 and r["k_trans"] == 0 and "Lattice Boltzmann" in r["notes"][0]
