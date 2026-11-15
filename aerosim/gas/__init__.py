"""Gas conduction row: heat carried by the air inside the pores."""

ROW = "Gas conduction"
ORDER = 3
HELP = (
    "Heat carried by the air inside the pores. Air conducts less when the pore is not much "
    "bigger than the distance a molecule flies between collisions (the Knudsen effect)."
)
COLOR = "#2f9e8f"

# Shared by every method in this row.
ALPHA = {
    "value": 1.0,
    "unit": "",
    "status": "hypothetical",
    "source": "full accommodation assumed, α = 1 (as in Zeng, Hunt & Greif 1995); not measured",
    "help": "Thermal accommodation coefficient: how fully a molecule takes the wall temperature.",
}
