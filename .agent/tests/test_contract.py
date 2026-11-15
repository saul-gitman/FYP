"""Every method file follows the contract in _template.py, and a new file shows up by itself."""

import shutil
import types
from pathlib import Path

import pytest

from aerosim.core import registry
from aerosim.core.state import State

EXPECTED = {
    "structure": ["honeycomb", "honeycomb_defects"],
    "solid": ["formula", "pixel_fv"],
    "gas": ["knudsen", "local_knudsen", "monte_carlo"],
    "radiation": ["opaque_walls", "rosseland", "ray_tracing"],
    "convection": ["rayleigh", "lattice_boltzmann"],
    "material": ["placeholder"],
}
ALL = [(row, m) for row, methods in EXPECTED.items() for m in methods]


def test_rows_and_methods_in_order():
    rows = registry.load()
    assert [r["key"] for r in rows] == list(EXPECTED)
    for r in rows:
        assert [m["key"] for m in r["methods"]] == EXPECTED[r["key"]]  # sorted by ORDER
        assert all(not m["key"].startswith("_") for m in r["methods"])  # _template.py ignored


def test_every_input_has_value_unit_status_source_help():
    for r in registry.load():
        for m in r["methods"]:
            for key, spec in m["module"].INPUTS.items():
                assert set(registry.INPUT_FIELDS) <= set(spec), (m["key"], key)
                assert spec["status"] in registry.STATUSES
                assert spec["source"].strip() and spec["help"].strip()


@pytest.mark.parametrize("row,method", ALL)
def test_every_method_runs_and_returns_the_contract(state, row, method):
    result = state.run(row, method)  # check_result raises if a key is missing
    keys = registry.STRUCTURE_KEYS if row == "structure" else registry.HEAT_KEYS
    assert all(k in result for k in keys)
    assert isinstance(result["notes"], list) and result["summary"]


def test_k_wall_label_is_kept():
    from aerosim.solid import K_WALL

    assert K_WALL["value"] == 4.0 and K_WALL["status"] == "derived"
    assert "Chan et al. 2022 (Kit's paper)" in K_WALL["source"]


def test_material_placeholder_adds_nothing(state):
    r = state.results["material"]
    assert r["covers"] == [] and r["k_par"] == 0 and r["k_trans"] == 0
    assert "not decided yet" in state.rows["material"]["module"].HELP


def good_module():
    return types.SimpleNamespace(
        NAME="x", LEVEL="fast", ORDER=1, HELP="h", EQUATION="e", SOURCE="s", COST="c",
        INPUTS={"a": {"value": 1.0, "unit": "", "status": "derived", "source": "s", "help": "h"}},
        run=lambda structure, inputs, conditions: {},
    )  # fmt: skip


def test_good_module_passes():
    registry.check_method(good_module(), "good.py")


@pytest.mark.parametrize(
    "breakage,message",
    [
        (lambda m: delattr(m, "HELP"), "missing HELP"),
        (lambda m: setattr(m, "LEVEL", "medium"), "LEVEL"),
        (lambda m: m.INPUTS["a"].pop("source"), "has no 'source'"),
        (lambda m: m.INPUTS["a"].update(status="guess"), "status"),
        (lambda m: delattr(m, "run"), "missing run"),
    ],
)
def test_malformed_module_is_refused_with_a_clear_message(breakage, message):
    mod = good_module()
    breakage(mod)
    with pytest.raises(registry.ContractError, match=message):
        registry.check_method(mod, "bad.py")


def test_result_without_k_is_refused():
    with pytest.raises(registry.ContractError, match="no 'k_trans'"):
        registry.check_result("solid", {"k_par": 1, "covers": ["solid"]}, "bad.py")
    with pytest.raises(registry.ContractError, match="covers"):
        registry.check_result("solid", {"k_par": 1, "k_trans": 1, "covers": ["heat"]}, "bad.py")


def test_new_file_from_template_appears_without_frontend_change():
    folder = Path(registry.PACKAGE) / "material"
    probe = folder / "zz_contract_probe.py"
    shutil.copy(folder / "_template.py", probe)
    try:
        state = State()
        keys = [m["key"] for m in state.rows["material"]["methods"]]
        assert "zz_contract_probe" in keys
        described = registry.describe([state.rows["material"]])[0]["methods"]
        assert "My method" in [m["NAME"] for m in described]  # what GET /api/models sends
    finally:
        probe.unlink()
