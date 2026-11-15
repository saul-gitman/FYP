"""One-line summary of the method. Copy this file to a new name (no leading "_") to add it.

The file then appears as a new segment in this row's selector after a page refresh.
Run `python -m pytest` first: the contract test refuses a file that misses a field.
"""

NAME = "My method"  # text on the selector segment
LEVEL = "fast"  # "fast" (a formula) or "detailed" (a simulation, marked ◆)
ORDER = 9  # position in the selector, left → right
HELP = "Plain-words explanation, 2–4 sentences. Shown when the mouse is on the segment."
EQUATION = "k = ..."  # shown in the tooltip
SOURCE = "Author year (journal volume:page)"
COST = "instant"  # rough run time, shown in the tooltip
INPUTS = {
    "x": {
        "value": 1.0,  # default, in the unit below
        "unit": "",
        "status": "hypothetical",  # measured | literature | derived | hypothetical
        "source": "where the default comes from",
        "help": "What this value means.",
    },
}
USES = []  # optional: other rows whose results run() reads, e.g. ["gas"] (for "re-run")


def run(structure, inputs, conditions):
    """structure: the Structure row's result (phi, rho_bulk, d, t, pitch in SI units).
    inputs: {name: number} in the units of INPUTS.
    conditions: {"T": K, "pressure": Pa, "results": {row: last result}}.
    Return k_par and k_trans in W/m·K, and which heat paths they cover:
    any of "solid", "gas", "rad", "conv" (several = solved together, counted once)."""
    k = 0.0
    return {"k_par": k, "k_trans": k, "covers": [], "notes": ["shown when hovering the result"]}
