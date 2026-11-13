> Current reading order: **START_HERE.md**. The user selected Lou 2023 (A01) as the main reference on 29 October. The roadmap below is retained historical context.

# Reference roadmap and offline availability

The original 8 October database has **49 records**, including **27 user-supplied papers**, Chan coauthored journal/review and conference records, and four wider references. It is preserved unchanged in `../06_Previous_Work/`. Four additional historically mentioned modelling/material leads are indexed here: Lou, Guo, Villière and Wang. The current catalog therefore has **53 records**, not 53 paper PDFs. Some historical records are conference presentations or broader background.

**Offline full text included: U02, Chan 2022, as the original uploaded PDF. All other paper records are LINK_ONLY.** Direct external PDF downloads returned HTTP 403 in this run. Publisher/accepted-manuscript links were checked where indicated, but readable web retrieval is not a saved file. The package is not a complete offline paper corpus. No abstract was expanded into a fake full paper.

## Read first for this simulator

| Order | Record | Contribution / guardrail |
|---|---|---|
| 1 | [U25 — Obori 2019](Records/U25.md) | Mathematical CNF-aerogel model lead; open-cell network, gas/solid/radiation; adapt and validate |
| 2 | [U02 — Chan 2022](Records/U02.md) | Kit's additive freeze-casting, aligned BNNS/WPU and optical simulation; PDF included |
| 3 | [C08 — Yang 2022](Records/C08.md) | Likely second historical Kit paper; BNNS/PVA solvent-assisted structure and insulation/reflection |
| 4 | [C07 — Kim 2023](Records/C07.md) | Freezing-temperature control and anisotropic BNNS/WPU network |
| 5 | [C06 — Adegun 2023](Records/C06.md) | Additional aligned BNNS/PVA thermo-optical benchmark |
| 6 | [U06](Records/U06.md), [U07](Records/U07.md), [U12](Records/U12.md), [U15](Records/U15.md), [U17](Records/U17.md) | Epoxy-infiltrated networks/CFRP integration, heat paths and interface mechanics |
| 7 | [U26](Records/U26.md), [U27](Records/U27.md), [U23](Records/U23.md) | Process–structure relationships and aligned-network mechanics |
| 8 | [A01 — Lou 2023](Records/A01.md), [A03 — Villière 2013](Records/A03.md), [A04 — Wang](Records/A04.md) | Heat-transfer/testing overview; CFRP tensor; closer CNF/CNT structure–property lead |
| 9 | [W02](Records/W02.md), [W03](Records/W03.md), [W04](Records/W04.md) | Spectral boundary/radiative-cooling background |

“Kit's two” is not uniquely labelled in the original list. September retrieved context named Chan 2022 plus Yang 2022; October files also foreground Adegun 2023 and Kim 2023. Preserve all four references and their material distinctions.

## Core sources and what can be carried into modelling

### U02 — Chan et al., Nature Communications 13, 5553 (2022)

*Scalable anisotropic cooling aerogels by additive freeze-casting.* DOI: [10.1038/s41467-022-33234-8](https://doi.org/10.1038/s41467-022-33234-8).

Reference system: BN nanosheets in waterborne polyurethane, with pore channels aligned in the panel plane. It reports transverse/out-of-plane k = 0.0169 W/(m K) and solar reflectance 97% for its reference aerogel. These are not values for the project's CNF/CNT/MTMS system or for resin-filled CFRP.

Useful modelling distinction: the paper's optical calculation uses FDTD, with ideal longitudinal air channels in a hexagonal arrangement, pore diameter 20 µm, model thickness 110 µm and simulated wavelength range 0.3–0.8 µm. These are optical model settings, not the complete measured solar band, a thermal mesh prescription or the required project-panel geometry.

The paper's [supplementary information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-022-33234-8/MediaObjects/41467_2022_33234_MOESM1_ESM.pdf) and [source-data spreadsheet](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-022-33234-8/MediaObjects/41467_2022_33234_MOESM8_ESM.xlsx) are linked but not included offline. Supplementary Fig. 12 is particularly relevant to optical geometry. Keep its nanostructure, optical structure and whole-panel scales separate.

### C08 — Yang et al., Nano-Micro Letters 14, 54 (2022)

*Superinsulating BNNS/PVA Composite Aerogels with High Solar Reflectance for Energy-Efficient Buildings.* DOI: [10.1007/s40820-022-00797-6](https://doi.org/10.1007/s40820-022-00797-6).

Reference system: BNNS/PVA, solvent-assisted directional freezing. The paper links altered cell walls/ligaments to insulation and reports transverse k = 0.0235 W/(m K), with solar reflectance 93.8%. It is a useful mechanism comparison, not the same binder, freezing recipe or wet-loading basis as the supplied experiment. [Supplementary PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1007%2Fs40820-022-00797-6/MediaObjects/40820_2022_797_MOESM1_ESM.pdf). Main PDF and supplement are link-only.

### C07 — Kim et al., Journal of Materials Chemistry A 11, 7105–7114 (2023)

*Engineering anisotropic structures of thermally insulating aerogels with high solar reflectance for energy-efficient cooling applications.* DOI: [10.1039/D2TA09983G](https://doi.org/10.1039/D2TA09983G).

Use for evidence connecting controlled freezing conditions and morphology/anisotropy in WPU/BNNS aerogels. It helps frame the process–structure relationship; it does not supply a universal temperature-to-pore mapping for CNF/CNT/MTMS. [Institutional manuscript](https://ira.lib.polyu.edu.hk/bitstream/10397/99470/1/Kim_Engineering_Antisotropic_Structures.pdf), link-only.

### C06 — Adegun et al., Composites Part A 169, 107522 (2023)

*Anisotropic thermally superinsulating boron nitride composite aerogel for building thermal management.* DOI: [10.1016/j.compositesa.2023.107522](https://doi.org/10.1016/j.compositesa.2023.107522).

BNNS/PVA reference with reported transverse/through-thickness k = 0.0203 W/(m K), solar reflectance 95.0%, and atmospheric-window emittance above 93%. Check orientation and measurement details in full text before use; these values do not characterise the guide's resin-infiltrated laminate. [Institutional manuscript](https://ira.lib.polyu.edu.hk/bitstream/10397/99475/1/Adegun_Antiotropic_Thermally_Superinsulating.pdf), link-only.

### U25 — Obori et al., Physical Review Applied 11, 024044 (2019)

*Parametric Model to Analyze the Components of the Thermal Conductivity of a Cellulose-Nanofibril Aerogel.* DOI: [10.1103/PhysRevApplied.11.024044](https://doi.org/10.1103/PhysRevApplied.11.024044). [Accepted manuscript](https://link.aps.org/accepted/10.1103/PhysRevApplied.11.024044), link-only.

The mathematical-method lead separates gas, solid-network and radiative effects using an open-cell representation and atmosphere/vacuum measurements. It motivates a calibratable structure-to-property model. Read Section III and its figures/equations directly before implementation; the current handover does not claim an exact reproduction or transfer its fitted constants to a different material.

### A01 — Lou et al., Gels 9(3), 220 (2023)

*Thermal Insulation Performance of Aerogel Nano-Porous Materials: Characterization and Test Methods.* DOI: [10.3390/gels9030220](https://doi.org/10.3390/gels9030220). A review of porous-aerogel heat-transfer modelling and characterisation/test methods. Useful for assumptions and method selection; not a measured parameter set for this FYP. [PMC full-text page](https://pmc.ncbi.nlm.nih.gov/articles/PMC10048302/), link-only.

## How to use the complete catalog

`references_catalog.csv` and `.json` map every original paper/presentation to its project purpose and current availability. Individual `Records/ID.md` files give navigable links. Original priorities and verification wording are retained as historical metadata, separate from checks made on 28 October.

Many records outside the core group were not freshly read. Their stated relevance is a reading direction inferred from title/theme, not a claim about findings. Keep publication version, composition, filler basis, gas/resin state, direction, density, pore scale, temperature, pressure and measurement method with any extracted number. Separate dry-aerogel conductivity from cured composite conductivity and measured spectra from model spectra.

See `PDF_Acquisition_Manifest.json` for candidate full-text URLs and `download_reference_pdfs.py` for an optional standard-library downloader for the receiving agent's environment. It downloads only supplied candidate URLs, validates PDF signatures and records failures; it neither authenticates nor bypasses publisher restrictions. Acquire remaining PDFs through lawful open versions or the user's institutional access, then update the manifest rather than relabelling a link as a local paper.
