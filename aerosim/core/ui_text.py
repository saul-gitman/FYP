"""The few UI words that do not belong to a method file. The front end hard-codes none."""

TITLE = "Aerogel k Simulator"
BADGE = "v0.1"
REMINDER = (
    "Scope: Honeycomb and Honeycomb + defects only · k_total = k_solid + k_gas + k_rad + k_conv"
)
START = "▶ Start"
RUNNING = "Running…"
DETAILED_MARK = "◆"
NO_INPUTS = "No inputs: nothing is simulated in this row yet."

# Row summaries (numbers in mW/m·K for display; the backend works in W/m·K)
SUMMARY_HEAT = "k⊥ {k_trans} · k∥ {k_par} mW/m·K"
SUMMARY_STRUCTURE = "φ {phi} %"
SUMMARY_NONE = "adds nothing"

# Footer
FORMULA = "k_total = k_solid + k_gas + k_rad + k_conv"
TRANS = "k⊥"
PAR = "k∥"
UNIT = "mW/m·K"
ANISOTROPY = "anisotropy k∥/k⊥"
STALE = "re-run {rows}"
SKIPPED = "{row} not added: already counted in {by}"

# 3D view
WALL_NOTE = "walls drawn ×{scale} thicker than real · drag to rotate"
AXIS_PAR = "z · along the channels (k∥)"
AXIS_TRANS = "x · across the channels (k⊥)"

# Input status dots
STATUS = {
    "measured": "measured on the project samples",
    "literature": "taken from a published source",
    "derived": "calculated from other values (see source)",
    "hypothetical": "assumed; no data yet, replace when measured",
}
