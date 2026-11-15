"""Radiation row: infrared thermal radiation crossing the pores."""

ROW = "Radiation"
ORDER = 4
HELP = (
    "Infrared thermal radiation crossing the pores and passing (or not) through the walls. "
    "Written as an equivalent conductivity k_rad; it grows with T³. Its inputs (wall "
    "emissivity, extinction, absorption) are the least certain of the whole model."
)
COLOR = "#c2417a"

# Shared by every method in this row that needs the sample thickness.
L_SAMPLE = {
    "value": 3.0,
    "unit": "mm",
    "status": "hypothetical",
    "source": "assumed sample thickness; replace with the measured sample",
    "help": "Sample thickness, used to check whether the sample is optically thick.",
}
