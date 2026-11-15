"""Run state: the last result of every row, which results are out of date, and k_total.

Used by the server, the CLI and the tests, so all three add up the heat paths the same way.
"""

import math
import time

from aerosim.core import registry, ui_text

PATH_ORDER = ["solid", "gas", "rad", "conv"]  # the order of the terms in k_total


def fmt(x):
    """Three significant figures for display (61.3, 71.0, 0.150); whole numbers above 1000."""
    return f"{x:#.3g}".rstrip(".") if abs(x) < 1000 else f"{x:.0f}"


def public(result):
    """The part of a result the browser sees: keys starting with '_' stay in Python."""
    return {k: v for k, v in result.items() if not k.startswith("_")}


class State:
    def __init__(self):
        self.results = {}  # row key -> last result
        self.runs = {}  # row key -> number of runs so far (a version counter)
        self.refresh()

    def refresh(self):
        """Re-scan the folders; give any row without a result its first (fast) method's result."""
        rows = registry.load()
        self.order = [r["key"] for r in rows]
        self.rows = {r["key"]: r for r in rows}
        for key in self.order:
            if key not in self.results:
                self.run(key, self.rows[key]["methods"][0]["key"])

    def module(self, row, method):
        for m in self.rows.get(row, {"methods": []})["methods"]:
            if m["key"] == method:
                return m["module"]
        raise KeyError(f"no method '{method}' in row '{row}'")

    def run(self, row, method, inputs=None):
        """Run one method with its default inputs, overridden by `inputs`; store and return it."""
        mod = self.module(row, method)
        values = {k: float(v["value"]) for k, v in mod.INPUTS.items()}
        for k, v in (inputs or {}).items():
            if k not in values:
                raise ValueError(f"unknown input '{k}' for {row}/{method}")
            values[k] = float(v)
            if not math.isfinite(values[k]):
                raise ValueError(f"input '{k}' must be a finite number")
        if row == "structure":
            structure, conditions = None, {}
        else:
            structure = self.results["structure"]
            conditions = {"T": structure["T"], "pressure": structure["pressure"]}
            conditions["results"] = self.results
        start = time.perf_counter()
        result = mod.run(structure, values, conditions)
        registry.check_result(row, result, f"aerosim/{row}/{method}.py")
        result["seconds"] = round(time.perf_counter() - start, 3)
        result["method"] = method
        result.setdefault("notes", [])
        self.runs[row] = self.runs.get(row, 0) + 1
        # remember which version of each row this result was computed from (for "re-run")
        uses = [] if row == "structure" else ["structure"] + getattr(mod, "USES", [])
        result["_seen"] = {u: self.runs.get(u, 0) for u in uses}
        result["summary"] = self.summary(row, result)
        self.results[row] = result
        return public(result)

    def summary(self, row, r):
        if row == "structure":
            return ui_text.SUMMARY_STRUCTURE.format(phi=fmt(100 * r["phi"]))
        if not r["covers"]:
            return ui_text.SUMMARY_NONE
        return ui_text.SUMMARY_HEAT.format(
            k_trans=fmt(1e3 * r["k_trans"]), k_par=fmt(1e3 * r["k_par"])
        )

    def stale(self):
        """Rows whose last result was computed from an older structure (or older row in USES)."""
        out = []
        for row in self.order:
            r = self.results[row]
            if any(self.runs.get(u, 0) != n for u, n in r["_seen"].items()) and r.get("covers"):
                out.append(self.rows[row]["module"].ROW)
        return out

    def totals(self):
        """k_total = k_solid + k_gas + k_rad + k_conv, each path counted once, both directions."""
        heat = [r for r in self.order if r != "structure" and self.results[r]["covers"]]
        # a result that resolves several paths together goes first, so they are not added twice
        heat.sort(key=lambda r: -len(self.results[r]["covers"]))
        claimed, notes = {}, []
        for row in heat:
            covers = self.results[row]["covers"]
            taken = [p for p in covers if p in claimed]
            if taken:
                by = self.rows[claimed[taken[0]]]["module"].ROW
                notes.append(ui_text.SKIPPED.format(row=self.rows[row]["module"].ROW, by=by))
                continue
            for p in covers:
                claimed[p] = row
        used = list(dict.fromkeys(claimed[p] for p in PATH_ORDER if p in claimed))
        out = {"formula": ui_text.FORMULA, "notes": notes, "stale": self.stale()}
        for key, label in (("k_trans", ui_text.TRANS), ("k_par", ui_text.PAR)):
            terms = []
            for row in used:
                r = self.results[row]
                value = fmt(1e3 * r[key])
                terms.append(
                    value if len(r["covers"]) == 1 else f"({'+'.join(r['covers'])}) {value}"
                )
            total = sum(self.results[row][key] for row in used)
            out[key] = total
            out[key + "_text"] = (
                f"{label} = {' + '.join(terms)} = {fmt(1e3 * total)} {ui_text.UNIT}"
            )
        out["anisotropy"] = out["k_par"] / out["k_trans"] if out["k_trans"] else float("nan")
        out["anisotropy_text"] = f"{ui_text.ANISOTROPY} = {fmt(out['anisotropy'])}"
        out["stale_text"] = (
            ui_text.STALE.format(rows=", ".join(out["stale"])) if out["stale"] else ""
        )
        return out

    def snapshot(self):
        return {
            "results": {row: public(r) for row, r in self.results.items()},
            "totals": self.totals(),
        }
