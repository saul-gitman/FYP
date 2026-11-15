"""Find every row (a folder with __init__.py) and method (a .py file in it), and check the contract.

A folder = a sidebar row. A file = a segment in that row's selector. Files starting with "_" are
ignored. A file that breaks the contract is refused with a message naming the file and the field.
"""

import importlib
import pkgutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]  # the aerosim/ folder
SKIP = {"core"}  # folders that are not rows

ROW_FIELDS = {"ROW": str, "ORDER": int, "HELP": str, "COLOR": str}
METHOD_FIELDS = {
    "NAME": str,
    "LEVEL": str,
    "ORDER": int,
    "HELP": str,
    "EQUATION": str,
    "SOURCE": str,
    "COST": str,
    "INPUTS": dict,
}
INPUT_FIELDS = {"value": (int, float), "unit": str, "status": str, "source": str, "help": str}
LEVELS = {"fast", "detailed"}
STATUSES = {"measured", "literature", "derived", "hypothetical"}
PATHS = {"solid", "gas", "rad", "conv"}  # the four heat paths of k_total
STRUCTURE_KEYS = ("phi", "rho_bulk", "d", "t", "pitch", "T", "pressure")  # a structure result
HEAT_KEYS = ("k_par", "k_trans", "covers")  # what every other method must return


class ContractError(Exception):
    """A row or method file does not follow the house style in _template.py."""


def _check_fields(obj, fields, where):
    for name, kind in fields.items():
        if not hasattr(obj, name):
            raise ContractError(f"{where}: missing {name}")
        if not isinstance(getattr(obj, name), kind) or isinstance(getattr(obj, name), bool):
            raise ContractError(f"{where}: {name} has the wrong type")


def check_method(mod, where):
    """Raise ContractError unless the module follows the method-file contract."""
    _check_fields(mod, METHOD_FIELDS, where)
    if mod.LEVEL not in LEVELS:
        raise ContractError(f"{where}: LEVEL must be one of {sorted(LEVELS)}")
    for key, spec in mod.INPUTS.items():
        if not isinstance(spec, dict):
            raise ContractError(f"{where}: INPUTS['{key}'] must be a dict")
        for field, kind in INPUT_FIELDS.items():
            if field not in spec:
                raise ContractError(f"{where}: INPUTS['{key}'] has no '{field}'")
            if not isinstance(spec[field], kind) or isinstance(spec[field], bool):
                raise ContractError(f"{where}: INPUTS['{key}']['{field}'] has the wrong type")
        if spec["status"] not in STATUSES:
            raise ContractError(
                f"{where}: INPUTS['{key}'] status must be one of {sorted(STATUSES)}"
            )
    uses = getattr(mod, "USES", [])
    if not (isinstance(uses, list) and all(isinstance(u, str) for u in uses)):
        raise ContractError(f"{where}: USES must be a list of row names")
    if not callable(getattr(mod, "run", None)):
        raise ContractError(f"{where}: missing run(structure, inputs, conditions)")


def check_result(row, result, where):
    """Raise ContractError unless run() returned what the totals and the other rows need."""
    keys = STRUCTURE_KEYS if row == "structure" else HEAT_KEYS
    if not isinstance(result, dict):
        raise ContractError(f"{where}: run() must return a dict")
    for key in keys:
        if key not in result:
            raise ContractError(f"{where}: run() result has no '{key}'")
    if row != "structure" and not set(result["covers"]) <= PATHS:
        raise ContractError(f"{where}: covers must be a subset of {sorted(PATHS)}")


def load():
    """Return every row (sorted by ORDER), each with its methods (sorted by ORDER)."""
    importlib.invalidate_caches()  # so a file added while the server runs is found
    rows = []
    for folder in sorted(PACKAGE.iterdir()):
        if folder.name in SKIP or not (folder / "__init__.py").exists():
            continue
        pkg = importlib.import_module(f"aerosim.{folder.name}")
        _check_fields(pkg, ROW_FIELDS, f"aerosim/{folder.name}/__init__.py")
        methods = []
        for info in pkgutil.iter_modules([str(folder)]):
            if info.name.startswith("_"):
                continue
            mod = importlib.import_module(f"aerosim.{folder.name}.{info.name}")
            check_method(mod, f"aerosim/{folder.name}/{info.name}.py")
            methods.append({"key": info.name, "module": mod})
        if not methods:
            raise ContractError(f"aerosim/{folder.name}/: a row needs at least one method file")
        methods.sort(key=lambda m: m["module"].ORDER)
        rows.append({"key": folder.name, "module": pkg, "methods": methods})
    rows.sort(key=lambda r: r["module"].ORDER)
    if not rows or rows[0]["key"] != "structure":
        raise ContractError("the structure row must exist and come first (ORDER = 1)")
    return rows


def describe(rows):
    """Everything the sidebar needs, as plain JSON (no modules, no functions)."""
    out = []
    for row in rows:
        pkg = row["module"]
        methods = []
        for m in row["methods"]:
            mod = m["module"]
            methods.append({"key": m["key"]} | {f: getattr(mod, f) for f in METHOD_FIELDS})
        out.append(
            {"key": row["key"]} | {f: getattr(pkg, f) for f in ROW_FIELDS} | {"methods": methods}
        )
    return out
