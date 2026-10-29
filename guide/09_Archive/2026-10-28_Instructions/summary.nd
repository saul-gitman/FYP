# FYP context handover — read this first

Export date: 28 October 2026, Hong Kong. Owner: Sam / samm. Institution: The Hong Kong Polytechnic University, Aviation Engineering. Supervisor: Dr CHAN Kit-Ying. Formal project title: **Thermo-optically functional CFRP laminates for lightweight electrified systems**.

## 1. What the project is about

Develop a lightweight, load-bearing CFRP panel with integrated aerogel-derived functional regions. The panel must manage heat produced inside an electrified system, such as UAV electronics, while reducing heat gained from sunlight outside. Study fabrication, resulting porous structure, thermal/optical properties, and structural integrity together. The aerogel is the functional material under investigation; CFRP is the structural component into which it is integrated. The final deliverable is a multifunctional CFRP system, not simply a free-standing insulation sample.

The formal proposal specifies asymmetric aerogel interleaves made by freeze-casting, integration by vacuum-assisted resin infusion (VARI), and evaluation of through-thickness conductivity, solar reflectance, interlaminar shear strength and infrared temperature fields against ordinary CFRP. Read [the original two-page proposal](01_Project/Project_Proposal_original.pdf).

Sam's immediate purpose for this ZIP is to give another agent enough context to **build an aerogel simulator** and retain memory for the **whole FYP**. More of the user's own context is preferable to a short task-only prompt. The requested recording transcript will be supplied later and must be retained in full, without conversion into a task summary.

## 2. How the CFRP and aerogels are placed

The supplied experiment guide specifies this stack, from the sun-facing outside toward the inside:

| Order | Region | Proposed formulation / role |
|---|---|---|
| 1 | Exposed BN-rich porous surface | CNF + BN + MTMS; reflect sunlight; investigate shielding and its effect on internal heat rejection |
| 2 | Upper carbon-cloth/epoxy layer | Structural CFRP face |
| 3 | Carbon-rich aerogel-derived interlayer | CNF + carboxylated CNT + MTMS; investigate thermal transport and spreading inside the laminate |
| 4 | Lower carbon-cloth/epoxy layer | Structural CFRP face |
| 5 | Back-centre heater during tests | Represents internal electronics heat generation; this is a boundary load, not a permanent material layer |

**The CNT-containing region is between the two carbon-cloth layers. The BN-containing region is on top of the upper carbon-cloth layer.** “Plant” is interpreted here as placement, incorporation and fabrication within/on the laminate.

Read [Experiment_Guide_original.docx](02_Experiment/Experiment_Guide_original.docx), copied byte-for-byte. A machine-readable text extraction is beside it. The guide describes placing the two slurries at their intended positions, freezing, freeze-drying, resin infusion and curing. It also proposes an integrated-fabrication versus separately made/bonded comparison. The precise sequence for screening samples and protection of the BN layer during infusion needs resolution; do not silently replace it with a different manufacturing route.

The proposal's broader “carbon-rich inner / BN-rich outer” architecture and the later Word guide are compatible in purpose but differ in specificity. Older assistant suggestions such as 0.5 mm / 2 mm / 0.5 mm model stacks are exploratory examples, not measured dimensions or supervisor-approved decisions.

## 3. What the aerogels are — do not merge these materials

| Material/system | Status in this project | Intended function / meaning |
|---|---|---|
| TEMPO-oxidised cellulose nanofibrils, CNF | Specified in supplied guide | Porous supporting network; a cellulose component, not the same thing as CNT or carbon fibre |
| Carboxylated carbon nanotubes, CNT | Guide's carbon-rich filler | Modify the network and directional heat paths; actual cured-laminate improvement must be measured |
| Boron nitride, BN | Guide's outer-layer filler | Solar reflection and porous-layer thermal/optical regulation; exact grade and whether exfoliated BN nanosheets must be established |
| Methyltrimethoxysilane, MTMS | Guide additive | Silane chemistry/structural and surface modification; final reaction state, retention and role require confirmation |
| BNNS/WPU aerogel | Chan 2022 reference | Anisotropic cooling aerogel (ACA), a standalone reference aerogel; not the project's CFRP or a CNF recipe |
| BNNS/PVA aerogel | Yang 2022 / Adegun 2023 references | Related aligned, reflective insulation networks; PVA differs from WPU and from CNF/MTMS |
| Epoxy-infused aerogel network | State after integration | Solid skeleton + epoxy + any residual gas pores; must be modelled separately from the dry aerogel |

There is no carbonisation step specified in the supplied guide. Its phrase “carbon aerogel” refers to the CNT-containing CNF/MTMS system in this context; it does not establish a pyrolysed carbon skeleton. Likewise, earlier “BN/C ratio” did not define C consistently. Keep CNT mass, CNF dry mass, carbon fibre, graphene and any carbonised material distinct.

## 4. Functions and the physical question

1. **Internal heat management:** spread or route a local electronics heat load so the source runs cooler under comparable boundary conditions. Measure source temperature, spatial gradients, effective conductivity and system thermal resistance.
2. **External solar management:** reduce absorbed sunlight through the exposed BN-rich layer. Measure spectral reflectance and solar-weighted reflectance on the actual supported/cured surface.
3. **Directional transport:** pore orientation and filler alignment can give different conductivities along different axes. High anisotropy is useful only if the high/low conductivity directions suit the intended heat path.
4. **Lightweight structural integration:** preserve acceptable laminate integrity, quantify added areal mass, assess interfaces, and check whether porosity survives infusion.
5. **Radiation:** sunlight rejection and mid-infrared thermal emission are different properties. Long-wave emission may contribute to cooling, but the guide does not provide measured emissivity for this formulation.

The trade-off is central: a layer that blocks incoming heat can also obstruct internally generated heat from leaving. Lower conductivity alone does not prove better internal cooling. “One-way heat” was an earlier user description of the objective; ordinary constant-property Fourier conduction does not make a thermal diode. Demonstrate directional system performance without claiming validated rectification.

## 5. Preserve Sam's processing–structure–property framework

Keep exactly these three top-level categories when organising the project:

| Category | Items carried forward |
|---|---|
| **1. Processing / Control Parameters** | BN/C ratio, freezing temperature and freezing time; later guide has separate CNT and BN concentration series |
| **2. Resulting Structure** | Shape/morphology, density; also measure porosity, pore dimensions, wall dimensions, alignment, connectivity, shrinkage and resin filling |
| **3. Resulting Properties** | Mechanical/tensile behaviour, heat transfer and reflectance; core formal-proposal metrics include through-thickness k and interlaminar integrity |

**1→3 = experiment. 2→3 = simulation. 1→2 = processing–structure relationship.** Literature/RAG supports these categories; it is not a fourth category. Earlier map requests were editable, self-contained HTML with a white background and black text. The retained maps are in `06_Previous_Work/Maps_and_Demos/`.

For the simulator, this means start by predicting properties from an explicitly defined structure. A freezing-temperature slider cannot legitimately predict pore structure without an experimentally calibrated processing model. An ideal hexagon/honeycomb is a testable geometry hypothesis, not an observed fact for all samples.

## 6. Roadmap through the package

| Order | Read | Purpose |
|---|---|---|
| 1 | This `summary.md` | Scope, placement, materials, functions and navigation |
| 2 | `01_Project/Project_Proposal_original.pdf` | Formal objectives and integration challenge |
| 3 | `02_Experiment/Experiment_Guide_original.docx` and `Experiment_Parameters_and_Issues.md` | Actual supplied recipe, test geometry and unresolved instructions |
| 4 | `03_Context/User_Context_and_Decisions.md` | Recovered user intent, preferences and history, with attribution limits |
| 5 | `04_Simulation/Simulation_Handover.md` | Proposed implementation roadmap, physics, inputs, outputs and validation |
| 6 | `04_Simulation/model_input_template.json` and `parameter_register.csv` | Machine-readable inputs with unknowns kept explicit |
| 7 | `05_References/Reference_Roadmap.md` and `references_catalog.csv` | Which papers support which modelling questions; actual PDF availability |
| 8 | `06_Previous_Work/` | Original research master, 49-record database, 27 supplied-paper records, spreadsheet and demos |
| 9 | `07_Capstone_Requirements/` | Whole-project academic requirements and original forms |
| 10 | `08_Transcripts/` once supplied | Complete, unsummarised recording transcripts |

`summary.nd` is an identical compatibility copy of this Markdown file because the request used that extension. Maintain `summary.md` as the canonical roadmap and keep the alias in sync.

## 7. First simulator milestones — proposed handover plan, not completed work

1. Define coordinates, geometry, material state, formulations and units. Identify which inputs are measured, from literature or hypothetical.
2. Implement an analytical multilayer resistance benchmark and a simple dry-aerogel structure-to-conductivity model. Use Obori's CNF model as a methodological reference, respecting its assumptions.
3. Solve directional conduction on a representative porous geometry, then extract an effective conductivity tensor. Validate against analytic limits and convergence checks.
4. Put the effective properties into the full CFRP/functional-layer panel. Reproduce dark heater, illumination-only and combined cases from the guide.
5. Add optical/radiative detail as data permits. Validate against measured spectra and temperatures. Preserve model and experiment differences.
6. Compare plain CFRP, carbon-only, BN-only and combined constructions on source temperature, shielding, mass and mechanical integrity. Produce reproducible inputs, fields, plots and uncertainty reports.

Python and ANSYS were discussed previously; no installed licence, validated solver, finished solver code, measured material constants or approved software choice is established by this export. The preserved HTML demos are geometry/visualisation aids, not evidence of a validated heat solver.

## 8. Completeness and unresolved sources

- The Word guide, official proposal, eight capstone documents and recovered previous working files are included.
- The original Chan 2022 paper PDF is included. Other references, including Yang 2022 and Obori 2019, have verified publisher/accepted-manuscript links but their PDF bytes could not be downloaded in this run. They are explicitly marked **LINK_ONLY**; the paper corpus is not complete offline.
- Earlier “Kit's two” references most clearly point to Chan 2022 and Yang 2022. The recovered literature set also prioritises Adegun 2023 and Kim 2023, so all four are indexed rather than silently choosing a pair and dropping the others.
- The full recording/transcript is pending. No transcript has been fabricated. See `TRANSCRIPT_PENDING.md`.
- Historical context retrieval returns partial, attributed summaries, not a complete verbatim chat export. Exact currently visible user wording is retained separately. Do not quote reconstructed history as the user's exact speech.
- Guide contradictions are retained in an issue register. Numbers in older spreadsheets are exploration ranges, not measured project results, and some composition entries are internally inconsistent.
