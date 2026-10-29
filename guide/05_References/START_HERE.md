# Simulator reference roadmap

**Main reference selected by the user:** Lou et al. (2023), *Thermal Insulation Performance of Aerogel Nano-Porous Materials: Characterization and Test Methods*, Gels 9(3), 220. DOI: [10.3390/gels9030220](https://doi.org/10.3390/gels9030220).

Build using this reference **including but not limited to it**. It provides a mechanism/model/test-method overview; it does not establish material constants for the project's final laminate. Use the research below to make the model structure and adaptations concrete.

| Read | ID and paper | Role in building the tool | Offline status |
|---|---|---|---|
| 1 | A01 — Lou et al. 2023, main review | Organise solid, gas, coupling and radiation mechanisms; select models and test comparisons | Reference note + verified full-text links; no PDF |
| 2 | U25 — Obori et al. 2019, *Parametric Model to Analyze the Components of the Thermal Conductivity of a Cellulose-Nanofibril Aerogel* | CNF-specific open-cell mathematical model; pressure-dependent comparison | Existing reference record + accepted-manuscript link; no PDF |
| 3 | U02 — Chan et al. 2022, *Scalable anisotropic cooling aerogels by additive freeze-casting* | Directional BNNS/polymer architecture, thermal/optical behaviour | **Original PDF included** in `PDFs/` |
| 4 | C07 — Kim et al. 2023, *Engineering anisotropic structures of thermally insulating aerogels with high solar reflectance for energy-efficient cooling applications* | Directional conductivity model and freezing-temperature/morphology comparison | Existing record + verified institutional manuscript link; no PDF |
| 5 | N01 — Han et al. 2022, *Lattice Boltzmann Simulation of Coupling Heat Transfer between Solid and Gas Phases of Nanoporous Materials* | Research example of resolved solid–gas transport and scale effects | Added note + full-text links; no PDF |
| 6 | N03 — Liu et al. 2021, *Ice-Templated Anisotropic Flame-Resistant Boron Nitride Aerogels Enhanced through Surface Modification and Cellulose Nanofibrils* | A closer CNF/BN directional-material comparison | Added note + publisher link; no PDF |
| 7 | N02 — Wang et al. 2019, *Aerogel Perfusion-Prepared h-BN/CNF Composite Film with Multiple Thermally Conductive Pathways and High Thermal Conductivity* | Show why a processed/filled CNF–BN film needs a different material state from dry insulation | Added note + full-text links; no PDF |

Also retain C08 (Yang 2022), C06 (Adegun 2023) and all earlier reference records for broader project context. See `Records/`, `references_catalog.csv` and `references_catalog.json`. Historical records are not all freshly verified and are not substitutes for full papers. The N-series reading notes were added during the 29 October update.

## What is actually available

The ZIP includes the original Chan U02 paper PDF and locally readable notes for the main review and added sources. Other full texts are linked, not silently represented as downloaded papers. Direct PDF requests for Lou, Han, Wang, Kim and Adegun returned HTTP 403 on 29 October 2026; Library did not contain an exact matching additional paper. Some full texts were accessible for online inspection, which does not supply original PDF bytes to this package.

Use `Reference_Availability_2026-10-29.json` for current core-source availability. The older acquisition manifest and download script are retained as historical context, with a note identifying this current status. A link-only source requires full-text retrieval before reproducing detailed equations or constants.
