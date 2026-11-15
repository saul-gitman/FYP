"""One-line summary of the structure. Copy this file to a new name (no leading "_") to add it.

The file then appears as a new segment in the Structure row after a page refresh.
Run `python -m pytest` first: the contract test refuses a file that misses a field.
"""

from aerosim.structure.honeycomb import INPUTS as HONEYCOMB_INPUTS

NAME = "My structure"  # text on the selector segment
LEVEL = "fast"  # "fast" or "detailed" (marked ◆)
ORDER = 9  # position in the selector, left → right
HELP = "Plain-words explanation, 2–4 sentences. Shown when the mouse is on the segment."
EQUATION = "φ = ..."
SOURCE = "Author year (journal volume:page)"
COST = "instant"
INPUTS = HONEYCOMB_INPUTS  # d, t, rho_wall, T, pressure; add more as {name: {value, unit, ...}}


def run(structure, inputs, conditions):
    """structure and conditions are unused for this row. Return the geometry in SI units.
    T (K) and pressure (Pa) are passed on to every other row. A pixel picture may be added as
    "_s" (solid fraction per pixel), "_wall_t" (wall thickness per pixel, m) and "_dx" (m),
    and "_geometry" for the 3D view (see honeycomb.py / honeycomb_defects.py)."""
    d, t = inputs["d"] * 1e-6, inputs["t"] * 1e-6
    phi = (d / (d + t)) ** 2
    return {
        "phi": phi,
        "rho_bulk": (1 - phi) * inputs["rho_wall"],
        "d": d,
        "t": t,
        "pitch": d + t,
        "T": inputs["T"],
        "pressure": inputs["pressure"] * 1e3,
        "notes": [],
    }
