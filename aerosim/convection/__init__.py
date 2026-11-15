"""Convection row: air moving inside the pores (buoyancy-driven)."""

ROW = "Convection"
ORDER = 5
HELP = (
    "Air moving inside the pores, driven by buoyancy. It needs a Rayleigh number above about "
    "1708; in micron-size pores it is many orders of magnitude smaller, so k_conv = 0. "
    "Foam literature finds convection only in cells above about 3–4 mm."
)
COLOR = "#7a6fd6"

# Shared by every method in this row.
DTDX = {
    "value": 1000.0,
    "unit": "K/m",
    "status": "hypothetical",
    "source": "assumed temperature gradient across the sample (e.g. 3 K over 3 mm)",
    "help": "Temperature gradient across the sample; one pore sees ΔT = (dT/dx) · d.",
}
