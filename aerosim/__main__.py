"""Command line:  python -m aerosim serve | run [row=method ...] | sweep

serve   start the web UI on http://localhost:8000
run     print the k_total breakdown at the defaults (fast methods), e.g.
        python -m aerosim run structure=honeycomb_defects solid=pixel_fv
sweep   write results/sweep.csv: every k term against pore size d (fast methods)
"""

import argparse
import csv
from pathlib import Path

from aerosim.core.state import State

RESULTS = Path(__file__).resolve().parents[1] / "results"


def run(pairs):
    state = State()
    for pair in pairs:  # each "row=method" runs with its default inputs, in the order given
        row, method = pair.split("=")
        state.run(row, method)
    for row in state.order:
        r = state.results[row]
        title = state.rows[row]["module"].ROW
        print(f"{title:18} {r['method']:18} {r['summary']}  ({r['seconds']} s)")
        for note in r["notes"]:
            print(f"{'':20}{note}")
    t = state.totals()
    lines = ["", t["formula"], t["k_trans_text"], t["k_par_text"], t["anisotropy_text"]]
    print("\n".join(lines + t["notes"] + [t["stale_text"]]).rstrip())


def sweep():
    """Pore-size sweep with the fast methods. Porosity and density follow from the geometry.
    A: wall thickness t fixed (headline).  B: pitch p = d + t fixed (headline).
    C: porosity φ fixed (diagnostic only: it prescribes porosity, see PLAN.md §0a)."""
    t0, p0, phi0 = 0.27, 30.27, (30 / 30.27) ** 2  # µm, µm, - : the defaults
    cases = [("A", d, t0) for d in (5, 10, 20, 30, 50, 100, 200, 500)]
    cases += [("B", d, p0 - d) for d in (20, 25, 28, 29, 30, 30.2)]
    cases += [("C", d, d * (phi0**-0.5 - 1)) for d in (5, 10, 20, 30, 50, 100, 200, 500)]
    state = State()
    RESULTS.mkdir(exist_ok=True)
    path = RESULTS / "sweep.csv"
    with open(path, "w", newline="") as fh:
        out = csv.writer(fh)
        out.writerow(["mode", "d_um", "t_um", "phi", "rho_bulk_kg_m3"]
                     + [f"{k}_{x}_mW_mK" for k in ("solid", "gas", "rad", "conv", "total")
                        for x in ("trans", "par")] + ["anisotropy"])  # fmt: skip
        for mode, d, t in cases:
            s = state.run("structure", "honeycomb", {"d": d, "t": t})
            terms = [state.run(row, state.rows[row]["methods"][0]["key"])
                     for row in ("solid", "gas", "radiation", "convection")]  # fmt: skip
            tot = state.totals()
            ks = [r[x] * 1e3 for r in terms for x in ("k_trans", "k_par")]
            ks += [tot["k_trans"] * 1e3, tot["k_par"] * 1e3]
            out.writerow([mode, d, round(t, 4), round(s["phi"], 5), round(s["rho_bulk"], 2)]
                         + [round(k, 4) for k in ks] + [round(tot["anisotropy"], 4)])  # fmt: skip
    print(f"wrote {path} ({len(cases)} rows)")


def main():
    parser = argparse.ArgumentParser(prog="python -m aerosim", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_serve = sub.add_parser("serve", help="start the web UI")
    p_serve.add_argument("--port", type=int, default=8000)
    p_run = sub.add_parser("run", help="print the k_total breakdown")
    p_run.add_argument("pairs", nargs="*", help="row=method to run after the fast defaults")
    sub.add_parser("sweep", help="write results/sweep.csv")
    args = parser.parse_args()
    if args.cmd == "serve":
        from aerosim.core.server import serve

        serve(args.port)
    elif args.cmd == "run":
        run(args.pairs)
    else:
        sweep()


if __name__ == "__main__":
    main()
