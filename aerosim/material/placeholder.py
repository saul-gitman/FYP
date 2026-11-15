"""Placeholder: nothing is simulated yet; adds nothing to k_total."""

NAME = "Placeholder"
LEVEL = "fast"
ORDER = 1
HELP = "Reserved for a future material simulation; not decided yet."
EQUATION = "none yet (contributes nothing to k_total)"
SOURCE = "not decided yet"
COST = "instant"
INPUTS = {}


def run(structure, inputs, conditions):
    return {"k_par": 0.0, "k_trans": 0.0, "covers": [], "notes": ["not decided yet"]}
