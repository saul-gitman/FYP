AAE4002/AAE4012 CAPSTONE PROJECT INTERIM REPORT — FULL TEXT (plain, for pasting into Word)
Project code: AAE12. Title: Thermo-optically Functional CFRP Laminates for Lightweight Electrified Systems
Students: CHAN Man Ho (23115045D); CHIK Long Tin (23076727D); SIU Ka Shun (23076695D)
Academic supervisor: Prof. CHAN Kit-Ying [proposal form says "Dr" – check title]. Industrial supervisor: N/A. Date of submission: 21 December 2026.

====================================================================
0 REVIEW NOTES (delete before submission)
====================================================================
A. Corrections to the group Word draft
A1 Template text still present: "1.1 Overview Main Context", "1.2 Current Situation / The current situation...", the example paragraph "The final year project is a testament...", "1.32 Objectives", "1.2.1 Objective 14", "7 5 Conclusion", the template reference (Wang et al. 2024, LLM agents), "Suggested to use APA or Vancouver Style", and the margin instructions pasted inside the AI declaration. Remove all.
A2 Heading numbers: use 1.1 Background, 1.2 Problem Statement, 1.3 Proposed Material Concept, 1.4 Aim and Objectives; "3.32" -> 3.3; subsections 3.3.1–3.3.6 consistent.
A3 Figure numbers do not match the text: text says Figure 1 (roadmap) but caption is Figure 2; Figure 2 (six configurations) -> caption Figure 3; Figure 3 (slurry preparation) -> caption Figure 4; Figure 4 (schedule) -> caption Figure 6. Use Word cross-references so numbers update automatically.
A4 Typos/grammar: "thermos-optically" -> thermo-optically; "radical direction" -> radial direction; "As report by" -> As reported by; "solidification-approached technique that fabricate" -> solidification-based technique that fabricates; "the ice will remove by sublimation" -> the ice is removed by sublimation; "Consider freeze-drying, it can alleviate" -> Freeze-drying alleviates; "After calculated the quantities ... we start to mix" -> After the quantities are calculated, the slurry is mixed; "Slurry Formation" (table titles) -> Slurry Formulation; mixed US/UK spelling (behavior/behaviour, fiber/fibre) -> choose British throughout.
A5 Tables 2 and 4: the "CNF (g)" and "CNT (g)" columns hold stock and dispersion masses (12.50 g, 9.62 g), not dry masses (0.50 g CNF, 1.25 g CNT). Rename to "CNF stock, 4 wt% (g)" and "CNT dispersion, 13 wt% (g)" and add a dry-mass note. The arithmetic of the water column is correct.
A6 Future plan: "30 specimen groups in total" -> 30 panels (10 groups x 3 panels). Reference P is described as "two carbon-fabric plies" in Table 3 but Semester 1 uses four plies; make consistent.
A7 2.3.2 is titled "Incorporation and Function of CNF Layer" but 2.3.1 already covers CNF; it should read CNT layer.
A8 1.2 Problem Statement cites a CNT-sheet interleave study and NASA conductive CFRP work without references; add both to the reference list.
A9 Scotti & Dunand relation: write lambda = A v^(-n) (A, n constants); avoid "k" as an exponent because k is used for thermal conductivity elsewhere.
A10 Contribution table: 33% x 3 = 99%; use 33.3% or state equal contribution.
A11 AI declaration: it says AI was used only for grammar and that methodologies and derivations were developed independently. The simulation code and a large part of the simulation text were produced with AI assistance, so the declaration as written would be inaccurate. Revise it to describe the actual use before submission (discussion deferred as requested).
A12 Supervisor title: draft says Prof., the 2026/27 proposal form says Dr. Use the current one.

B. Corrections applied to the earlier simulation report (HTML) after reading the group draft
B1 Team names, SIDs, project code AAE12 added; supervisor title follows the group draft.
B2 Laminates use FOUR carbon-fabric plies, not two; the CNT slurry is applied to the plies ("CNT-treated plies"), not cast as a separate interlayer between two plies. L1–L5 and P now defined as in Table 1 of the group draft.
B3 Freezing set-up (liquid-nitrogen cavity, metal plate, upward ice growth) confirms channels through the laminate thickness: the measured through-thickness value corresponds to the aerogel's high direction k_par, not k_perp.
B4 Added Zhao et al. (2022), cited in the group draft: a CNF/BN/MTMS cryogel (same constituents as B10) with k = 62.1 (axial) and 33.9 (radial) mW/m K, anisotropy 1.83. This changes the discrepancy discussion: the closest-composition measurement lies ABOVE the air-only floor and its anisotropy (1.83) lies inside the model range (1.6–2.2). The sub-air and anisotropy-5.8 discrepancies belong to the BNNS/WPU and BNNS/PVA systems.
B5 Objectives replaced by the group's three objectives; simulation objectives S1–S4 mapped onto them.
B6 Semester-2 screening range is B0–B20 and C0–C7.5 (not B30, C10).

====================================================================
ABSTRACT
====================================================================
Lightweight electrified systems such as UAVs place heat-generating electronics inside carbon-fibre-reinforced polymer (CFRP) structures that conduct heat poorly through their thickness, while the outer skin absorbs solar radiation. This project develops an asymmetric, thermo-optically functional CFRP laminate: carbon-fabric plies treated with a CNF/CNT/MTMS slurry to redistribute internal heat, and a freeze-cast CNF/BN/MTMS porous surface layer to reflect sunlight. Six configurations (L1–L5 and an uncoated reference P), each with four T300 carbon-fabric plies, are fabricated by directional freezing, freeze-drying and vacuum-assisted resin infusion (VARI), and compared under internal heating, simulated solar irradiation and combined loading, together with spectral reflectance, through-thickness thermal resistance and short-beam strength.
A simulation strand predicts the thermal conductivity of the freeze-cast layers from their structure and recipe. A browser-based simulator decomposes conductivity into solid, gas, radiative and convective paths, each with a closed-form method and a pixel-based detailed method that must reproduce the formula in the ideal case; a GPU-ready voxel solver computes the wall conductivity from the recipe and solves the honeycomb at its true wall thickness. At the reference structure (30 um pores, 0.27 um walls, wall conductivity 4 W/m K) the model gives 61.3 and 96.8 mW/m K across and along the channels (anisotropy 1.58), and 5% wall cracks lower the transverse value by 23%. All 53 unit tests, a lattice Boltzmann benchmark and 11 solver checks pass, including an independent finite-element benchmark within 0.35%. The modelled anisotropy agrees with a published CNF/BN/MTMS cryogel (1.83), whereas sub-air values reported for BNNS/polymer aerogels cannot be reproduced by any air-filled micron-channel model. A sensitivity study ranks BN sheet contact resistance, BN conductivity, sheet alignment and wall porosity as the measurements that would most reduce uncertainty. Semester two will vary CNT and BN content and use the model to predict the specimens blind after one calibration on P.
Keywords: freeze-casting; boron nitride; carbon nanotube; CFRP; thermal management; anisotropic thermal conductivity; finite volume; GPU computing

====================================================================
1 INTRODUCTION
====================================================================
1.1 Background
Lightweight electrified systems require structural materials that can perform more than a load-bearing function. In applications such as UAVs, structural components may also form part of the thermal pathway between internally mounted electronics and the surrounding environment. This creates an opportunity to develop multifunctional composites that combine structural performance with thermal management. Related aerospace research has demonstrated this approach by incorporating conductive fillers and graphite-based layers into carbon-fibre-reinforced polymer composites for lightweight heat exchangers and radiators [ref: NASA conductive CFRP].
CFRP is a relevant platform for this development, but its thermal performance requires careful consideration. Heat transfer depends on the laminate architecture, the resin matrix and the interfaces between its constituents; carbon/epoxy laminates conduct well below 1 W/m K through their thickness and several times more along the fibres (Villière et al., 2013). Improving conductivity along the laminate surface therefore does not necessarily produce an equivalent improvement through its thickness. NASA's work on conductive CFRP, for example, specifically addressed through-thickness heat transfer by introducing perforated graphite layers and carbon nanotube (CNT) containing resin, highlighting the importance of continuous thermal pathways across the laminate [ref: NASA].
For the application considered in this project, the thermal challenge involves two distinct loads: heat generated by internal components and heat absorbed from external solar irradiation of up to about 1000 W/m2. A material intended to reduce operating temperature must therefore manage internal heat without unnecessarily increasing solar heat gain. This motivates an asymmetric laminate in which different regions provide different functions, rather than a single homogeneous modification.

1.2 Problem Statement
The design of a thermally functional CFRP laminate involves a potential conflict between heat dissipation and thermal protection. A conductive inner region may help redistribute internally generated heat, while a reflective outer region may reduce the absorption of sunlight. However, a porous outer layer can also act as an insulator and restrict the release of internal heat. The effectiveness of the combined structure must therefore be evaluated under both individual and simultaneous thermal loads.
Previous research demonstrates the importance of this distinction. CNT-sheet interleaves have produced substantial improvements in the in-plane thermal conductivity of carbon-fibre composites without a corresponding improvement in out-of-plane conductivity, a behaviour associated with interfacial thermal resistance within the hybrid laminate [ref: CNT-sheet interleave study]. Consequently, the addition of CNTs cannot be assumed to lower the temperature of an internally heated component unless the complete heat-transfer pathway is considered.
Similarly, cellulose/BN/MTMS cryogels have demonstrated useful thermal insulation and optical functionality, but these properties do not establish their suitability for releasing heat from an enclosed electronic system. Zhao et al. (2022) reported an anisotropic CNF/hydroxylated-BN-nanosheet/MTMS cryogel with thermal conductivities of 0.0621 and 0.0339 W/m K in its axial and radial directions. These results support directionally structured porous layers while showing that the resulting material may remain strongly insulating.
A further challenge arises when these porous materials are incorporated into a structural laminate. Results obtained from standalone aerogels cannot be transferred directly to a resin-infused composite because the finished structure differs from the original dry framework. The project therefore assesses the complete cured laminate rather than treating the properties of its individual layers as sufficient evidence of overall effectiveness.
The experimental chain from slurry to tested laminate is long, and only a few parameters can be varied, yet the conductivity of a porous layer depends on many at once: pore size, wall thickness, channel direction, wall composition and microstructure, and whether resin has entered the pores. The walls are about 0.27 um thick while the pores are about 30 um wide (Chan et al., 2022), the conductivity of a BN/CNF/MTMS wall cannot be looked up, and several published BN aerogels report transverse conductivities below that of still air. A transparent model that predicts conductivity from structure, states the status of every input and reports gaps rather than hiding them is therefore needed to interpret the measurements and to choose the next formulations.

1.3 Proposed Material Concept
This project, titled "Thermo-optically functional CFRP laminates for lightweight electrified systems", investigates an asymmetric material architecture containing two functional regions. CNT-treated carbon-fabric plies investigate heat redistribution and thermal transport, while a BN-containing porous surface layer on the externally exposed side investigates solar shielding.
TEMPO-oxidised cellulose nanofibres (CNF) provide the supporting framework for both formulations, and methyltrimethoxysilane (MTMS) is incorporated as a framework-modifying component. Directional freezing and freeze-drying form the porous structures before integration into CFRP through VARI.
The selection of these constituents is informed by related hybrid-aerogel research. Zhao et al. (2022) demonstrated a CNF/BN/MTMS cryogel fabricated through unidirectional freeze-casting. Zuo et al. (2023) incorporated carboxylated CNTs into an MTMS-treated nanocellulose/MXene aerogel, while Lu et al. (2025) investigated a bacterial-cellulose/CNT/MTMS porous material produced through directed freezing. These studies support the feasibility of related material combinations, but they do not directly validate the exact formulations or the resin-infused architecture proposed here.
T300 carbon fibre is selected for this project. T300 is a standard-modulus reinforcement manufactured by Toray and used in woven fabrics and prepregs. Its nominal fibre properties include a tensile strength of 3,530 MPa, a tensile modulus of 230 GPa, a density of 1.76 g/cm3 and a failure strain of about 1.5% [ref: Toray T300 datasheet]. In the proposed laminate, T300 fabric plies provide the principal structural reinforcement, while the CNT-treated plies and the BN-containing surface layer introduce the thermal and optical functions. Keeping fabric architecture, ply orientation and resin system consistent across reference and modified specimens isolates the effects of the functional layers. The manufacturer's fibre properties are not the properties of the finished laminate; the mechanical performance of the infused composite must be established experimentally.
The central design principle is integration: the thermal and optical functions must remain beneficial when combined within the same component. The project therefore investigates not only whether individual formulations possess useful properties, but whether their combination produces a measurable improvement under representative internal heating and external irradiation.

1.4 Aim and Objectives
The aim of this project is to develop and experimentally evaluate a thermo-optically functional CFRP laminate that combines internal heat-management capability with external solar protection. The specific objectives are to:
(1) design and fabricate CNF/CNT/MTMS and CNF/BN/MTMS layers by freeze-casting and VARI in different laminate configurations;
(2) investigate the influence of CNT and BN aerogel content on the thermal behaviour, spectral reflectance and mechanical strength of the CFRP laminate;
(3) integrate selected formulations into CFRP by VARI and compare them with conventional CFRP under internal heating, simulated solar irradiation and simultaneous loading.
The simulation strand supports objectives (2) and (3) with four sub-objectives: (S1) build a transparent, verified model of the conductivity of a freeze-cast honeycomb layer along and across its channels, decomposed by heat path; (S2) link the slurry recipe to the conductivity of the aerogel wall as a band with the reason for its width; (S3) identify which uncertain inputs dominate, and therefore which measurements to make first; (S4) predict the temperature rise of the six specimens, calibrating once on P only (Semester 2).

====================================================================
2 LITERATURE REVIEW
====================================================================
2.1 Thermal Management in CFRP Laminates
Villière et al. (2013) measured and modelled the full conductivity tensor of a carbon/epoxy composite and showed that the transverse conductivity is governed by the epoxy and the fibre packing, remaining well below 1 W/m K, while the fibre direction conducts several times better. For an electrified airframe this means heat from an internal source spreads poorly through the skin, and any added layer acts in series with an already resistive laminate. Two strategies follow: raise the through-thickness conductivity with conductive networks (fillers, CNT-containing resin, graphite layers [ref: NASA]), or redistribute heat in-plane so that it leaves over a larger area. On the outer surface the relevant literature is that of daytime radiative cooling: surfaces reflecting most of the solar spectrum can stay below ambient temperature in direct sunlight (Raman et al., 2014). The same anisotropy appears again in the freeze-cast layers of this project, so every layer must be described by a conductivity tensor, not a single number, and the laminate must be evaluated as a whole.

2.2 CNT-based Interlayers for Thermal Transport
Individual CNTs conduct heat very well along their axis, but networks of CNTs in a polymer conduct far less because heat must cross tube–tube contacts and tube–matrix interfaces, each with a thermal boundary (Kapitza) resistance (Swartz & Pohl, 1989). Effective-medium models with interfacial resistance show that for slender, high-aspect-ratio fillers this interface term can dominate the composite conductivity (Nan et al., 1997). This explains why CNT interleaves can raise in-plane conductivity strongly while leaving the out-of-plane value almost unchanged [ref: CNT-sheet interleave study from 1.2]: in-plane, heat can travel long distances along well-connected tubes; through the thickness it must cross many interfaces in series with the resin-rich interlaminar region. For the present laminate this means that the CNT-treated plies are expected mainly to spread heat laterally, and that the benefit for an internally heated component depends on whether lateral spreading enlarges the area through which heat leaves the plate. After infusion the CNT/CNF/MTMS framework inside the plies becomes a CNT/epoxy composite rather than a dry aerogel, so its properties must be evaluated in the infused state (Section 2.6).

2.3 Material Selection for Functional Aerogel Layers
2.3.1 Cellulose Nanofibres as Supporting Framework
Nanocellulose-based porous materials offer a framework for incorporating functional fillers into lightweight structures (Apostolopoulou-Kalkavoura et al., 2021). In the present study CNF supports both the CNT-containing and the BN-containing layer. Zhao et al. (2022) fabricated an anisotropic cellulose nanofibre/hydroxylated boron nitride nanosheet/methyltrimethoxysilane composite cryogel (Si-CNF/BNNS) by unidirectional freeze-casting, with thermal conductivities of 0.0621 W/m K axially and 0.0339 W/m K radially. The authors attribute this to hydrogen bonding and silylation cross-linking of CNF with BNNS and MTMS, and to the aligned structure of the cryogel.
2.3.2 Incorporation and Function of the CNT Layer
In the CNT formulation (C2.5) the CNTs are the thermally functional phase and the CNF acts as dispersant and binder. Because the water leaves on drying, the 2.5 wt% CNT slurry produces a dry solid that is about 56 wt% CNT (1.25 g CNT, 0.50 g CNF and about 0.49 g of condensed MTMS per 50 g batch, assuming full condensation of MTMS). The CNTs therefore form a continuous network rather than a dilute filler, and the conductivity of that network is controlled by tube–tube contacts (Section 2.2). Applied to the carbon fabric and frozen from below, the slurry forms a porous network in and around the plies, which is subsequently infused with epoxy.
2.3.3 Incorporation and Function of the BN Layer
Hexagonal BN is white, electrically insulating and highly anisotropic: bulk h-BN conducts about 325 W/m K in-plane with natural isotopes (585 W/m K for isotopically pure 10B) but only about 5 W/m K across its basal planes (Yuan et al., 2019; Jiang et al., 2018). In freeze-cast aerogels BN nanosheets provide solar reflectance (Chan et al., 2022) and stiffen the pore walls. The B10 slurry contains 10 wt% BN of the wet mass but, once the water has left, builds walls that are about 83 wt% (77 vol%) BN. Every BN-containing group (B5–B20) gives walls of at least 62 vol% BN, so BN is the continuous phase and CNF/MTMS act as glue between sheets. Measured BN/cellulose films of similar composition range from 1.2 to 145.7 W/m K in-plane depending on how the sheets touch (Zhu et al., 2014; Kong et al., 2022; Wang et al., 2019), so composition alone does not fix the wall conductivity.
2.3.4 Incorporation and Function of MTMS
MTMS hydrolyses and condenses into a methyl-bearing polysiloxane (polymethylsilsesquioxane, PMSQ). In CNF/BN cryogels it cross-links the network by silylation, which strengthens the aligned structure and makes the walls hydrophobic (Zhao et al., 2022). Hydrophobicity matters for this project in two ways: it limits moisture uptake after freeze-drying, and it may change how readily the epoxy wets and fills the porous layer during infusion. The extent of MTMS condensation in the slurry is not specified by the procedure; full condensation (mass yield 0.493) is assumed in the composition calculations and treated as an uncertain input.

2.4 Freeze-casting and Anisotropic Pore Architecture
2.4.1 Principles of Freeze-casting
Freeze-casting is a solidification-based technique that fabricates porous materials with controlled architectures. The process involves preparing a suspension or solution, freezing the liquid phase and removing the frozen solvent by sublimation. During solidification the growing solvent crystals push the suspended materials into the spaces between the crystals, where they form the solid walls. During freeze-drying the ice is removed by sublimation and pores remain in the spaces previously occupied by the crystals (Scotti & Dunand, 2018).
In this project freeze-casting arranges CNF, CNTs and BN into porous functional layers that are then integrated into CFRP. The purpose is not only to produce lightweight layers but also to control the direction, distribution and connections within their solid framework.
2.4.2 Directional Freezing and Structure Formation
Directional freezing removes heat mainly in one direction so that ice grows along a preferred path. A common arrangement uses a metal base connected to a cold source while the mould walls provide insulation. Ice grows away from the cold base and pushes the suspended materials into the spaces between the growing crystals; after freeze-drying the material contains a vertically aligned lamellar structure (Zhao et al., 2022) (Figure 1, Luo et al., 2026).
The growing ice does not always push all particles aside; some may be trapped within the ice. This depends on the speed of ice growth, particle properties, suspension viscosity and interactions between the materials. The first region to freeze may therefore have a relatively dense structure, followed by a transition region and a more clearly aligned region (Wegst et al., 2010).
2.4.3 Influence of Freezing Conditions
The temperature of the cold source, the cooling rate, the temperature gradient and the freezing-front speed are different quantities. The freezing front is the boundary between frozen and unfrozen material, and its speed describes how quickly freezing moves through the suspension. A liquid-nitrogen-cooled base does not produce one fixed front speed, because heat must pass through the base, the mould and the growing frozen layer; the cold-source temperature alone does not describe the process.
Scotti and Dunand (2018) relate the structural spacing to the front speed as
lambda = A v^(-n)     (Equation 1)
where lambda is the average width of one pore plus its adjacent wall, v is the freezing-front speed, and A and n are constants for a particular material and process. Faster ice growth is generally linked to smaller spacing, but the constants cannot be applied directly to every formulation, and pore width, wall thickness and spacing may respond differently to the freezing conditions.
The structure may also change with distance from the cold base: as the frozen layer thickens, heat must travel further to the cold source, the front slows and pores become larger. Mould size, casting area, wet-layer thickness, contact with the base and sample position should therefore be kept consistent.
2.4.4 Freeze-drying and Preservation of the Structure
After freezing, the ice must be removed without damaging the structure. During ordinary evaporation, capillary forces in small pores can cause shrinkage or collapse; freeze-drying alleviates this by removing the ice through sublimation, and vacuum freeze-drying is essential to avoid collapse and cracking (Sozcu et al., 2023).
Freeze-drying has two stages: primary drying removes most of the frozen water, and secondary drying reduces the moisture that remains bound to the material. Suitable conditions depend on sample temperature, chamber pressure, heat supply and formulation, so a fixed drying time is an initial setting, not proof that every sample has reached the same dry state (Tchessalov et al., 2023). Merivaara et al. (2022) showed the importance of controlling residual moisture when producing nanofibrillated-cellulose aerogels, which supports checking drying progress and final condition rather than relying on time alone. Drying conditions, visible defects and storage conditions are recorded to separate effects of freezing from those of drying or moisture uptake.

2.5 BN-containing Porous Layers for Solar Shielding
BN-nanosheet aerogels combine high solar reflectance with low thermal conductivity. Chan et al. (2022) produced BNNS/waterborne-polyurethane (WPU) panels by additive freeze-casting with in-plane channels of about 30 um, a porosity of 98.2% and a density of 20.2 mg/cm3; the out-of-plane conductivity was 16.9 mW/m K, the anisotropy factor 5.8 and the solar reflectance 97%. Kim et al. (2023) showed that lower freezing temperatures give more anisotropic BNNS/WPU structures (16.2 mW/m K) and proposed a theoretical approach to estimate anisotropic conductivity. BNNS/PVA aerogels reached 23.5 mW/m K with 93.8% reflectance (Yang et al., 2022) and 20.3 mW/m K with 95.0% reflectance (Adegun et al., 2023). Zhao et al. (2022), with the same constituents as this project (CNF/BN/MTMS), reported 33.9 mW/m K radially and 62.1 mW/m K axially, with radiative-cooling capability from the white CNF/BN surface.
Table 2.1 Reported properties of anisotropic freeze-cast insulating aerogels
Material | k_perp (mW/m K) | anisotropy | solar reflectance | source
BNNS/WPU, additive freeze-casting, 30 um pores, porosity 0.982 | 16.9 | 5.8 | 97% | Chan et al. (2022)
BNNS/WPU, low freezing temperature | 16.2 | – | about 97% | Kim et al. (2023)
BNNS/PVA, unidirectional | 20.3 | – | 95.0% | Adegun et al. (2023)
BNNS/PVA, solvent-assisted | 23.5 | – | 93.8% | Yang et al. (2022)
CNF/BNNS/MTMS cryogel, unidirectional | 33.9 | 1.83 | high (white) | Zhao et al. (2022)
Three points matter for this project. First, the BNNS/polymer values lie at or below still air (26.3 mW/m K at 300 K; Bergman et al., 2011); an air-filled honeycomb with 30 um channels and porosity 0.98 should carry about 25.6 mW/m K through its gas alone, so those values imply either pores much smaller than the channels (for example nanoporous walls) or a measurement that underestimates the transverse value. Chan et al. used a transient plane source (Hot Disk) instrument (Gustafsson, 1991), whose result on strongly anisotropic, highly porous samples depends on the analysis model and the assumed heat capacity (Lou et al., 2023). The CNF/BN/MTMS cryogel of Zhao et al., closest to this project, lies above the air floor. Second, Chan et al. define porosity as 1 − rho/rho0 with rho0 the weighted average of the WPU (1.02 g/cm3) and BNNS (2.25 g/cm3) densities; with 20.2 mg/cm3 at 98.2% this gives rho0 = 1.12 g/cm3, i.e. a polymer-rich wall of roughly 8–16 wt% BNNS, very different from the BN-continuous walls of B10 (to be confirmed with the authors). Third, reflectance in these studies is measured from 0.25–2.5 um, while thermal emission at 300 K peaks near 9.7 um; solar reflectance data do not determine the infrared emissivity of the surface.

2.6 Resin Infusion and Preservation of Functionality
A porous layer keeps its insulating function only while its pores stay empty. Bounding analysis of the honeycomb (Hashin & Shtrikman, 1962) shows how strongly infusion changes the layer. For a dry layer (wall 4 W/m K, air 0.026 W/m K, contrast about 150) the transverse conductivity is bracketed between 27.0 and 61.9 mW/m K and depends strongly on the wall: doubling the wall conductivity raises it by 58%. If epoxy (assumed 0.2 W/m K) fills the cells, the contrast falls to about 20, the bracket narrows to 206.5–235.7 mW/m K, and doubling the wall conductivity changes the result by only 15%. A BN surface layer flooded with resin would conduct about 3.8 times more across and 2.8 times more along its channels and would no longer insulate. For the CNT-treated plies infusion is intended: the CNT/CNF/MTMS framework becomes a CNT/epoxy network, and its function is heat spreading. For the BN top layer of L1 and L2, formed before infusion, whether resin enters it is the single most important question for the thermal comparison. The mass gain on infusion and cross-sections of the retained offcuts are therefore recorded for every plate. Post-infusion BN coatings (L3, L4) avoid this risk but replace a porous insulating layer by a thin coating.

2.7 Mechanical Implications of Functional Interleaves
Adding porous or particle-filled layers between or within plies changes the interlaminar region, which governs delamination resistance. Short-beam shear testing (ASTM D2344/D2344M) is the usual screening method for interlaminar shear strength, but its applicability to thin, four-ply laminates with functional layers must be checked: the span-to-thickness ratio, failure mode and the presence of a soft surface layer affect whether the measured value is a true interlaminar shear strength. Well-dispersed CNT networks can toughen the interlaminar region, whereas resin-starved or poorly bonded porous layers can act as weak planes [ref: CNT veil interleaf study, e.g. catalogue item U17]. Failure modes are therefore recorded with every strength value, and the reference P is fabricated with the same fabric, orientation, resin and cure so that differences can be attributed to the functional layers.

2.8 Modelling Heat Transfer in Porous Functional Layers
2.8.1 Heat-transfer paths
Heat flow in aerogels and foams is commonly decomposed into conduction through the solid skeleton, conduction through the gas in the pores, thermal radiation and convection (Hrubesh & Pekala, 1994; Lou et al., 2023; Apostolopoulou-Kalkavoura et al., 2021). Obori et al. (2019) applied this split quantitatively to cellulose-nanofibril aerogels, fitting an open-cell solid model, the Kaganer gas expression and a radiative term to measurements; it is the closest methodological precedent, but it fits the solid term rather than predicting it from composition. Gas conduction is reduced when the pore size approaches the mean free path of the gas (about 66 nm for air at 300 K and 1 atm) (Kaganer, 1969; Zeng et al., 1995), the principle used in vacuum insulation panels (Baetens et al., 2010); for 30 um channels at 1 atm the reduction is below 1%. Radiation in cellular materials is modelled as exchange between opaque walls or, for optically thick materials, by Rosseland diffusion (Glicksman, 1994; Modest, 2013), with Monte Carlo ray tracing on the real geometry as the most general route (Randrianalisoa & Baillis, 2014). Convection is absent in cells smaller than a few millimetres (Skochdopole, 1961; Collishaw & Evans, 1994). The additive split neglects solid–gas coupling, which can be significant in nanoporous materials (Han et al., 2022); for micron-scale channels it is expected to be small.
2.8.2 Conductivity of the walls
For thin-walled cellular solids the solid term scales with the solid fraction and a geometric factor for walls inclined to the heat flow (about one third for thin-strut foams; Collishaw & Evans, 1994; Gibson & Ashby, 1997). Wiener and Hashin–Shtrikman bounds bracket any two-phase arrangement (Hashin & Shtrikman, 1962; Torquato, 2002). Effective-medium theory with interface resistance (Nan et al., 1997) assumes a dilute filler in a continuous matrix; the B-series walls are 62–91 vol% BN, outside that range, where heat must cross sheet-to-sheet contacts. This is why the project models the wall explicitly with voxels and reports a band of wall conductivities rather than one number.
2.8.3 Computing properties from structure
Homogenisation on a periodic representative volume element (RVE), imposing a mean gradient and averaging the flux, is standard (Torquato, 2002) and is used in industry: NASA's PuMA software for heat-shield preforms (Ferguson et al., 2018), TauFactor for battery electrodes and its GPU version TauFactor 2 (Cooper et al., 2016; Kench et al., 2023), and FFT-based homogenisation of composites (Moulinec & Suquet, 1998). The local-thickness transform from bone micro-CT (Hildebrand & Rüegsegger, 1997), implemented in PoreSpy (Gostick et al., 2019), gives pore sizes point by point. Lattice Boltzmann methods reproduce the onset of Rayleigh–Bénard convection (Shan, 1997; Mohamad, 2011), DSMC resolves rarefied gas (Bird, 1994), and SliceGAN generates 3-D structures from 2-D micrographs (Kench & Cooper, 2021). Verification and validation practice (Oberkampf & Roy, 2010; ASME, 2009) requires each numerical model to be shown to solve its equations correctly before it is compared with experiments.
Table 2.2 Concepts borrowed by the simulation tools
Concept | origin | used in practice for | where in this project
Additive heat-path split | Hrubesh & Pekala (1994) | aerogel and foam insulation | simulator rows, k_total
Periodic RVE with imposed gradient | Torquato (2002) | composite design | Pixel FV; K_cond solver
Voxel image-based conductivity | Ferguson et al. (2018); Cooper et al. (2016) | heat shields; battery electrodes | K_cond wall and honeycomb steps
FFT preconditioning of a periodic solve | Moulinec & Suquet (1998) | FFT homogenisation codes | K_cond PCG preconditioner
Local thickness by distance transform | Hildebrand & Rüegsegger (1997) | bone micro-CT; PoreSpy | local-Knudsen gas method
Knudsen gas conduction | Kaganer (1969); Zeng et al. (1995) | vacuum and cryogenic insulation | Knudsen, local Kn, Monte Carlo
Ray tracing, Beer fit, Rosseland | Randrianalisoa & Baillis (2014) | foam radiation | ray-tracing method
Lattice Boltzmann Rayleigh–Bénard | Shan (1997) | industrial LBM CFD | convection check
Interface resistance in series | Swartz & Pohl (1989); Nan et al. (1997) | thermal interface materials | K_cond face conductance
Verify before validating | Oberkampf & Roy (2010) | engineering simulation V&V | test suite; built-in checks
2.8.4 Research gap
Three gaps emerge. (i) Sub-air transverse values reported for BNNS/polymer aerogels are not explained by their stated structures, while the closest-composition CNF/BN/MTMS cryogel lies above the air floor. (ii) No predictive link exists from a BN:CNF:MTMS recipe to wall conductivity; mixture models are used outside their validity range, and films of similar composition differ by two orders of magnitude. (iii) Effective-property tools exist, but not as a transparent chain from recipe to laminate that states the status of every input. This project builds that chain and uses the estimate of Kim et al. (2023) and the component model of Obori et al. (2019) as benchmarks.

====================================================================
3 METHODOLOGY
====================================================================
3.1 Research Approach
The study combines simulation and experiment to evaluate the thermal and optical performance of thermo-optically functional CFRP laminates, within a processing–structure–property framework: processing (recipe, freezing, infusion) produces structure (pore size, wall thickness, channel direction, wall microstructure, resin fill), and structure produces properties (conductivity, reflectance, strength). The experiments span the whole chain; the simulation covers structure to properties, where causes can be separated one at a time. The thermal model uses the specimen geometry, material properties and loading conditions to predict temperature and heat flow. In parallel, the experimental investigation covers material selection, laminate configuration, slurry preparation, freeze-casting, resin infusion and surface coating. Predictions are compared with measurements to assess agreement and explain differences between configurations. Figure 2 shows the research roadmap. The combined findings identify promising layouts and guide simulation and processing optimisation in Semester 2.

3.2 Simulation
3.2.1 Scope, strategy and modelling chain
Following the supervisor's guidance, the first study models the freeze-cast layer on its own before the laminate, with a simple idealised geometry, one fixed composition and varying pore size, computing conductivity both along (par) and across (perp) the channels and comparing trends rather than absolute values; porosity and density follow from the geometry. The conductivity is decomposed into four paths:
k_total = k_solid + k_gas + k_rad + k_conv, separately along and across the channels; anisotropy = k_par / k_perp     (Equation 3)
Two pieces of software are used. The aerosim web tool explains each path with a fast closed-form method and a detailed pixel method and runs on any laptop (Python, NumPy, SciPy). The K_cond solver computes what the web tool cannot derive, the wall conductivity for the real recipe, and solves the honeycomb at its true wall thickness; it is written for GPU execution on Google Colab and also runs on a CPU. Its result feeds back into the web tool (Figure 3.1, modelling chain: recipe and geometry -> wall RVE -> honeycomb -> layer k_par, k_perp -> planned specimen model).
Four rules govern the implementation: (1) each heat path is counted once, and a method that resolves two paths together declares it; (2) every path has a fast and a detailed method; (3) a detailed method is trusted where the formula cannot go (cracks, uneven cells, narrow gaps) only after it reproduces the formula in the ideal case, enforced by automated tests; (4) every input carries a value, unit, source and status (measured, literature, derived or hypothetical), and no input is tuned to match a measurement.
Table 3.1 Methods considered and not adopted
Method | what it would add | reason not adopted
3-D CFD of pore convection | convective term | pore Rayleigh number about 7e-8, eleven orders below onset; a 2-D lattice Boltzmann check suffices
DSMC of the gas (Bird, 1994) | rarefied gas in any geometry | Kn about 0.002 at 1 atm; Knudsen correction below 1%
Molecular dynamics of BN–binder interfaces | interface resistance from first principles | months of work for one number; published orders of magnitude used and swept
Phase-field simulation of ice growth | structure from freezing conditions | most expensive option; SEM of own specimens gives the structure more accurately
Commercial FE package (e.g. ANSYS) | general conduction solver | meshing 0.27 um walls in 30 um cells is costly; a periodic finite-volume solver is simpler, checkable and free

3.2.2 Structure model
The ideal structure is identical hexagonal tubes with inner flat-to-flat width d and wall thickness t. Because a hexagon's area scales with the square of its flat-to-flat width:
p = d + t,  phi = (d/p)^2,  rho_bulk = (1 − phi) rho_wall     (Equation 4)
Defaults follow Chan et al. (2022): d = 30 um and t = 0.27 um (so that phi = 0.982); rho_wall = 20.2/0.018 = 1122 kg/m3 (derived). For the detailed methods the honeycomb is drawn as a periodic pixel image of a 4 x 4 block of cells with seeded defects: random cell-centre spread (10% of pitch), wall-thickness variation t(1 + 0.2 N(0,1)) and one crack per wall of a chosen fraction of its length. A pixel belongs to its nearest cell centre a; its distance to the wall (the bisector between a and the second-nearest centre b) is (r_b^2 − r_a^2)/(2|c_b − c_a|), and it is wall if this is below half the drawn thickness. Shortcut: real walls are only t/d = 0.009 of the cell, so the web tool draws walls 4 px wide at 100 px per cell and gives each wall pixel a solid fraction s = t/t_draw, preserving the wall conductance t·k_wall exactly; 4 px are needed because a 2 px band at ±30° carries only 64% of its true heat. Counted porosity is 0.9825 against 0.9822 analytically. The GPU solver removes this shortcut.
Table 3.2 Main simulation inputs
Input | value | status | source
Pore size d | 30 um | literature | Chan et al. (2022); SEM of own specimens to replace
Wall thickness t | 0.27 um | derived | gives phi = 0.982
Wall density | 1122 kg/m3 | derived | 20.2/(1 − 0.982)
Wall conductivity (web tool) | 4.0 W/m K | derived | back-calculated from Chan et al. (2022); polymer-rich wall (Section 2.5)
Temperature, pressure | 300 K, 101.3 kPa | hypothetical | test conditions
Accommodation coefficient | 1 | hypothetical | full accommodation
Emissivity; IR absorption; reflectance | 0.9; 1e6 1/m; 0.1 | hypothetical | no infrared data for BN/CNF/MTMS walls
Temperature gradient (convection check) | 1000 K/m | hypothetical | result insensitive

3.2.3 Solid conduction: a four-rung fidelity ladder
Rung 1, closed form and bounds. Along the channels the walls are strips in parallel with the air: k_solid,par = (1 − phi) k_wall exactly. Across, a thin wall at angle theta to the gradient sees the component |grad T| cos theta and only the component cos theta of its flux lies in the flow direction, so each wall contributes in proportion to cos^2 theta. A hexagonal network has walls at 0°, 60° and 120°, whose mean cos^2 is (1 + 1/4 + 1/4)/3 = 1/2:
k_solid,par = (1 − phi) k_wall;  k_solid,perp = 1/2 (1 − phi) k_wall     (Equation 5)
the 2-D analogue of the one-third factor for thin-strut foams (Collishaw & Evans, 1994). A 2-D conductivity tensor unchanged by a 120° rotation is isotropic, so the honeycomb has one k_perp in every in-plane direction; any x–y difference in a calculation is discretisation error. The result is bracketed by the 2-D Hashin–Shtrikman bounds:
k_HS = k1 + f2 / [1/(k2 − k1) + f1/(2 k1)], with k1 the larger (upper) or smaller (lower) phase conductivity     (Equation 6)
Rung 2, pixel finite volume (web tool). Each pixel has k = s k_wall + (1 − s) k_gas; face conductance is the harmonic mean of two half-pixels; heat balance holds in every pixel (Patankar, 1980):
sum_j G_ij (T_j − T_i) = 0,  G_ij = 2 k_i k_j/(k_i + k_j),  k_eff = Q L/(A dT)     (Equation 7)
Boundary conditions are periodic with a 1 K drop per period, solved directly with SciPy along x and y; k_perp is their mean. This deliberately replaces fixed-temperature edges, which gave values about 5% low and disagreed between 2 x 2 and 4 x 4 blocks because of cut edge cells. Along the channels k_par is the mean pixel conductivity, exactly. The method resolves solid and gas together and is not added to the gas row again.
Rung 3, honeycomb at true wall thickness (K_cond step 2). One periodic unit of two hexagonal cells is drawn at the real wall thickness with 4 (quick) or 8 (full) pixels across the wall; stratified 4 x 4 sub-sampling gives each pixel face its wall fraction, reducing the x–y split from 5.5% to 0.16%. A plate whose channels are tilted by theta from its normal sees
K = diag(k_perp, k_perp, k_par),  n = (sin theta, 0, cos theta),  k_n = k_par cos^2 theta + k_perp sin^2 theta     (Equation 8)
The freezing set-up of Section 3.3.4 (metal plate on liquid nitrogen, upward ice growth) grows channels through the laminate thickness (theta about 0), so the through-thickness value of the specimens corresponds to the layer's high direction k_par, whereas the published BN aerogels were tested across in-plane channels. theta will be confirmed by SEM of the offcuts.
Rung 4, wall RVE from the recipe (K_cond step 1). The water leaves on drying, so the solids build the walls. Per 50 g batch (BN 0–10 g, 0.50 g dry CNF, 1.00 g MTMS) and assuming full MTMS condensation (yield 0.493, hypothetical), with densities BN 2.1, CNF 1.5 and PMSQ 1.25 g/cm3 (the last a placeholder), the dry walls are:
Table 3.3 Dry wall composition of the B-series
Group | BN wt% | CNF wt% | PMSQ wt% | BN vol% | dense wall density (g/cm3)
B0 | 0 | 50.4 | 49.6 | 0 | 1.37
B5 | 71.6 | 14.3 | 14.1 | 62.1 | 1.82
B10 | 83.4 | 8.3 | 8.2 | 76.6 | 1.93
B20 | 91.0 | 4.5 | 4.5 | 86.7 | 2.00
C2.5 dry solids: about 56 wt% CNT, 22 wt% CNF, 22 wt% PMSQ.
The wall is a periodic 3-D voxel box: true thickness (0.27 um) through z and 1.6–2.5 um in plane. BN sheets are thin discs (default diameter 1 um, thickness 30 nm, hypothetical) at random centres, tilted from the wall plane by |N(0, 10°)| because the ice front flattens platelets, until the BN volume fraction is reached. BN voxels conduct 300 W/m K along their sheet plane and 3 W/m K across (Yuan et al., 2019; Jiang et al., 2018); remaining voxels are CNF, PMSQ or pore in proportion; each voxel carries its sheet identity. Interfaces enter the face conductance between voxels i and j of size h:
k_f = [1/(2k_i) + 1/(2k_j) + R/h]^-1, R = R_K (BN–binder), R_c (two different sheets), 0 otherwise     (Equation 9)
with R_K = 1e-8 m2K/W (order for BN–polymer; Swartz & Pohl, 1989; Nan et al., 1997) and R_c = 1e-8 m2K/W (swept). Percolation and contact effects emerge from the geometry without fitting. Three periodic solves give the wall conductivity tensor; several random walls (2 quick, 8 full) give a low–likely–high band. The C2.5 layer uses the same machinery with rods.

3.2.4 Numerical solution and computing hardware
Rungs 3 and 4 share one solver. T = theta − G x with theta periodic and a 1 K drop per cell along the driven axis; heat balance gives a symmetric positive semi-definite system A theta = b, solved by preconditioned conjugate gradients (Hestenes & Stiefel, 1952) without assembling the matrix (neighbours are array shifts). The preconditioner is the same grid filled with a uniform reference medium, diagonal in Fourier space and inverted exactly by two FFTs (Moulinec & Suquet, 1998), so iteration counts depend on the conductivity contrast, not the grid size (264–284 iterations for the wall, 67–95 for the honeycomb; relative residual 1e-8; every solve checks that equal heat crosses every plane). The code runs on CPU with NumPy or on GPU with CuPy (Okuta et al., 2017) in double precision and needs about 112 bytes per voxel per solve: the full-mode wall (5 nm voxels, 500 x 500 x 54) needs about 1.5 GB, a 2.5 nm convergence check about 12 GB, and 1.25 nm about 97 GB, beyond one 80 GB card. The GPU is therefore needed for throughput (seeds x three drives x sensitivity points) and the convergence study, not for one large solve. Because a stencil-plus-FFT solver is memory-bound, memory bandwidth and double-precision rate decide performance; data-centre GPUs (A100, H100) provide both (NVIDIA, 2020, 2022), whereas consumer GPUs run FP64 at a small fraction of FP32. Colab sessions are time-limited and not guaranteed a GPU type, so runs use fixed seeds, save one result row per solve and log GPU type, library versions and wall time.

3.2.5 Gas conduction
Fast: free-air conductivity from Bergman et al. (2011) (26.3 mW/m K at 300 K), mean free path from kinetic theory (d_g = 3.72e-10 m) and Knudsen reduction (Kaganer, 1969; Zeng et al., 1995):
lambda = k_B T/(sqrt2 pi d_g^2 p),  Kn = lambda/d,  k_gas = k_air/(1 + 2 beta Kn),  beta = [(2 − alpha)/alpha][2 gamma/(gamma + 1)]/Pr     (Equation 10)
beta = 1.643 for alpha = 1, gamma = 1.4, Pr = 0.71; lambda = 66.5 nm and Kn = 0.0022 at 30 um and 1 atm. The gas term is phi k_gas in both directions.
Detailed 1, local Knudsen: the local pore size at each pixel is the diameter of the largest disc that fits in the pore and covers it (local thickness; Hildebrand & Rüegsegger, 1997), computed with distance transforms on a periodically padded picture; the formula applied pixel by pixel gives a k_gas map that Rung 2 can use.
Detailed 2, Monte Carlo chords: molecules start at random pore points and fly in random 3-D directions; the harmonic mean chord 1/<1/l> recovers Cauchy's 4V/S; since parallel plates a gap d apart have mean chord 2d, d_eff = mean chord/2 and k_gas = k_air/(1 + 2 beta lambda/d_eff). This replaces the brief's free-path-ratio model, which disagreed with the plate Knudsen result by 26% at Kn = 0.1 and a factor 5.5 at Kn = 10.
Comparison: at 1 atm the three methods give 26.11, 25.95 and 25.86 mW/m K (within 1%). At 1 kPa they give 15.1, 14.3 and 9.6 mW/m K. A smooth hexagonal channel has mean chord d (4A/P), so it behaves as a plate gap of d/2, not d; the definition of pore size is irrelevant at 1 atm but decisive in vacuum or nanoporous walls (Figure: k_gas vs pressure, three methods).

3.2.6 Radiation
Fast 1, opaque walls: linearising grey-plate exchange gives k_rad = 4 sigma T^3 d eps/(2 − eps)     (Equation 11)
= 0.150 mW/m K at eps = 0.9 (hypothetical), used in both directions.
Fast 2, Rosseland: k_rad = 16 n^2 sigma T^3/(3 e rho_bulk), valid only for optical thickness tau = e rho_bulk L well above 1 (Hrubesh & Pekala, 1994; Modest, 2013). With e = 30 m2/kg and L = 3 mm, tau = 1.8, so the tool flags it as invalid at the defaults.
Detailed, ray tracing: diffuse photon bundles enter slabs 1/4–4 cells thick; at a wall a bundle is reflected (R), absorbed with (1 − R)(1 − exp(−kappa_w t)) or transmitted; transmitted + reflected + absorbed = 1 for every slab. A Beer's-law fit gives the extinction beta of the structure; k_rad follows from Rosseland (beta L >= 3) or the two-flux slab 4 sigma T^3 L/(1 + 3/4 beta L) (Randrianalisoa & Baillis, 2014). Rays stay in the cross-section (2-D). Opaque walls give 0.144 against 0.150 mW/m K; default optics give beta = 1.77e4 1/m and 0.46 mW/m K.
The radiative term is below 1% of the total but has the least certain inputs: reflectance is measured from 300–2500 nm, whereas emission at 300 K peaks near 9.7 um (Wien), so FTIR data or literature optical constants are needed; until then k_rad is an order of magnitude.

3.2.7 Convection
Ra = g beta_T dT d^3/(nu alpha_th), beta_T = 1/T, dT = (dT/dx) d     (Equation 12)
with nu = 15.89e-6 and alpha_th = 22.5e-6 m2/s at 300 K. Onset is at Ra about 1708; at d = 30 um and 1000 K/m, Ra = 7.4e-8, so k_conv = 0. Since Ra scales with d^4, onset would need pores of about 12 mm (3.7 mm at 1e5 K/m), consistent with the millimetre threshold for foams (Skochdopole, 1961). A D2Q9/D2Q5 lattice Boltzmann model with Boussinesq buoyancy (Shan, 1997; Mohamad, 2011) confirms this: Nu = 1 + <vT>H/(alpha_th dT), k_conv = (Nu − 1) phi k_gas; it is benchmarked first (Section 4.1.1) and returns Nu = 1.000000 for the pore.

3.2.8 Implementation
The web tool is organised as rows (heat paths) and methods (one Python file each, declaring name, level, equation, source, cost and inputs, and returning k_par, k_perp, the paths covered and notes). A registry discovers the files, a state object runs them and adds each path once, and a standard-library HTTP server exposes a JSON API to a browser page that holds no physics or labels: all text shown on hover comes from the method files. A 3-D view shows the structure coloured by the last detailed field. The K_cond solver is one file with editable wall, honeycomb and run-option blocks, each input annotated with unit, status and source, running in quick CPU mode (under a minute) or full GPU mode. Both live in the project repository (github.com/saul-gitman/FYP) with plans, physics notes and design records.

3.2.9 Verification strategy
Following Oberkampf & Roy (2010) and ASME (2009), checks are layered: hand numbers (worked example recomputed independently); exact cases (uniform box, layers in series and parallel, layers with interface resistance); limits and bounds (Wiener, Hashin–Shtrikman, empty slab, opaque walls); detailed reproduces fast (each detailed method against its formula in the ideal case); convergence and conservation (grid refinement, plane energy balance, seed scatter); and independent benchmarks (fitted-mesh FE honeycomb; published Rayleigh–Bénard Nusselt numbers).

3.2.10 Planned specimen model (Semester 2)
The specimen model follows the fabrication sequence, one model state per step, each fed by the experiment's own records: recipe -> wall composition; SEM of offcuts -> pore size, wall thickness, channel direction; mass gain on infusion -> resin fill; measured thicknesses -> stack of four T300 plies, CNT-treated plies and BN top layer or coating. A 40 x 40 mm plate with a 20 x 20 mm heater, four low-conductivity supports and still air is solved in 3-D, with solar input absorbed as (1 − R) from measured reflectance. Infused CNT plies and coated layers use closed-form bounds (narrow brackets); dry BN layers use the voxel solver. The surface heat-transfer coefficient and heater contact are calibrated once on P and held fixed while L1–L5 are predicted blind; uncertainty is propagated by Latin-hypercube sampling with Sobol indices.

3.3 Experimental Design
3.3.1 Specimen Configuration and Groups
Laminate layouts are compared in this semester. The CNF, CNT, BN and MTMS concentrations of each formulation remain constant wherever it is used; the variables are the location of the aerogel, the use of a BN aerogel surface layer and the type of coating after infusion. Six configurations are investigated: three aerogel-containing, two conventional CFRP with different coatings, and an uncoated conventional reference. Each contains four T300 carbon-fabric plies (Table 3.4; Figure: schematic of the six configurations).
Table 3.4 Specimen configuration
Group | configuration | surface treatment | purpose
L1 | four CNT-treated plies | BN aerogel layer formed on top before infusion | CNT laminate with freeze-cast BN surface layer
L2 | two CNT-treated and two BN-treated plies | BN aerogel layer formed on top before infusion | effect of replacing two CNT plies with BN plies
L3 | four CNT-treated plies | BN-based coating after infusion and cure | post-infusion BN coating vs pre-infusion BN aerogel
L4 | four conventional plies | BN-based coating after infusion and cure | coating without internal aerogel
L5 | four conventional plies | commercial white reflective coating after infusion and cure | non-BN coating comparison
P | four conventional plies | none | reference
Panels are fabricated at 50 x 50 mm and edge-trimmed by waterjet to 40 x 40 mm for thermal–optical evaluation; edge material is retained for cross-sectional examination (SEM of pore size, wall thickness, channel direction and resin penetration, which feed the specimen model).
3.3.2 Materials and Slurry Formulations
Two fixed formulations are investigated this semester: C2.5 (2.5 wt% CNT) and B10 (10 wt% BN), both with 1 wt% CNF and 2 wt% MTMS, all relative to a 50.00 g wet batch. CNTs are supplied as a dispersion of 13 wt% dry CNT and the CNF stock contains 4 wt% dry CNF. The stock mass is
m_i,stock = M w_i / c_i     (Equation 2)
with M = 50.00 g, w_i the target mass fraction and c_i the stock fraction (c_CNT = 0.13, c_CNF = 0.04). For C2.5, m_CNT = 50.00 x 0.025/0.13 = 9.62 g of dispersion (1.25 g dry CNT); BN is added as powder, m_BN = 50.00 x 0.10 = 5.00 g; m_CNF = 50.00 x 0.01/0.04 = 12.50 g of stock (0.50 g dry); m_MTMS = 1.00 g. Liquid in the stocks is included when calculating added water.
Table 3.5 Slurry formulation (per 50.00 g batch)
Formulation | CNF stock 4 wt% (g) | CNT dispersion 13 wt% (g) | BN powder (g) | MTMS (g) | added water (g)
C2.5 | 12.50 | 9.62 | 0 | 1.00 | 26.88
B10 | 12.50 | 0 | 5.00 | 1.00 | 31.50
The CNF stock is mixed with about 80% of the added water and magnetically stirred for 10 min. CNT dispersion or BN powder is added gradually and stirred at 600–1000 rpm for 10 min, followed by intermittent ultrasonication under cooling (10 min net, 2 s on/2 s off, slurry below 30 °C). MTMS is added slowly and stirred for 20 min, the remaining water brings the batch to 50.00 g, and the slurry stands for 2 h before remixing and degassing prior to application to the fabric and directional freezing (Figure: slurry preparation).
3.3.3 Implementation of Aerogels
(i) Four-ply CNT configuration (L1, L3): C2.5 slurry is applied to each of the four plies, which are stacked in the mould on the freezing plate so that ice grows upward through the stack. (ii) Combined CNT and BN configuration (L2): two plies are treated with C2.5 and two with B10, stacked with the CNT-treated plies nearest the heater side and the BN-treated plies towards the exposed side. (iii) BN top aerogel layer (L1, L2): a controlled wet layer of B10 slurry is cast on top of the stack before freezing, so the surface layer freezes from the same base and is freeze-dried with the plies. Wet-layer thickness, slurry mass per ply and stacking order are recorded for each plate. [Group to confirm stacking order and wet-layer thickness; guide gives about 0.5–1 mm for the BN layer.]
3.3.4 Freeze-casting and Freeze-drying
The directional freezing set-up (Figure: freezing set-up) consists of (a) a styrofoam box with a liquid-nitrogen-filled cavity and (b) a metal plate carrying the slurry-treated plies, with insulated mould walls so that ice grows upward from the plate. Frozen specimens are kept frozen during transfer and freeze-dried with an initial setting of 48 h at a controlled chamber pressure in the 10–30 Pa range; drying progress, visible defects (cracks, powder shedding) and storage conditions are recorded (Section 2.4.4).
3.3.5 Vacuum Assisted Resin Infusion (VARI)
The freeze-dried stack is laid on a release film with peel ply and flow mesh, enclosed in a vacuum bag with inlet and outlet lines, and evacuated; an existing epoxy system (e.g. WEST SYSTEM 105/209, mixing ratio and cure per batch documentation) is drawn through the stack under vacuum, then cured and conditioned for at least 7 days at room temperature before testing. Dry and cured dimensions and masses are recorded; the mass gain on infusion gives the resin fill fraction, and cross-sections show whether resin has entered the BN top layer (Section 2.6). [Group to confirm bagging sequence, vacuum level and cure schedule.]
3.3.6 Implementation of Commercial Coating
For L3 and L4 a BN-based coating, and for L5 a commercial white reflective coating, are applied to the cured top surface after infusion, with coating mass and thickness recorded so that differences in reflectance can be related to coverage. [Group to specify coating products, application method and target thickness.]

3.4 Material Testing
3.4.1 Optical Characterisation
Optical tests quantify how much incident sunlight each top surface reflects, which determines the absorbed solar fraction (1 − R) used in the thermal comparison and the specimen model.
3.4.2 Spectral Reflectance
Total hemispherical reflectance R(lambda) is measured from 300 to 2500 nm with a UV–Vis–NIR spectrometer and integrating sphere against a white reference and dark baseline, at the centre and two further positions per plate, averaged per plate; replicate plates are kept separate from repeated positions.
3.4.3 Solar-weighted Reflectance
R_solar = ∫ R(lambda) I_AM1.5(lambda) dlambda / ∫ I_AM1.5(lambda) dlambda (300–2500 nm)     (Equation 13)
where R(lambda) is the measured spectral reflectance and I_AM1.5(lambda) the reference spectral irradiance (ASTM G173). The infrared emissivity relevant to radiative heat loss (around 8–13 um) is outside this range and is stated as an assumption.
3.4.4 Through-thickness Thermal Characterisation
R''_z = L / k_z     (Equation 14)
where R''_z is the through-thickness thermal resistance in m2K/W and L the measured thickness of the complete laminate in metres, measured near 25 °C with a method compatible with the laminate thickness and with contact resistances corrected and stated.
3.4.5 Combined Thermal–solar Testing
P = V I     (Equation 15)
where P is the heater power, V the voltage and I the current. A 20 x 20 mm heater is attached at the back centre with the same interface for all specimens, each specimen resting on four low-conductivity supports at fixed height in still air at 25 ± 2 °C. Three load cases are run: internal heating (2 W) in the dark; solar-only (1000 W/m2, irradiance mapped at the centre and four corners); and combined. Temperatures are logged every 1–5 s by thermocouples and every 30–60 s by infrared camera; each run lasts at least 60 min until the slope stays below 0.1 °C/min over 10 min.
3.4.6 Performance Evaluation
R_sys = (T_heater − T_ambient) / P     (Equation 16)
where T_heater is the steady heater temperature, T_ambient the ambient temperature and R_sys the system thermal resistance in K/W (distinct from the material resistance R''_z). The temperature reduction relative to the conventional reference is
dT_reduction = dT_P − dT_Li, with dT = T_heater − T_ambient     (Equation 17)
3.4.7 Mechanical Assessment
Interlaminar performance is screened by short-beam shear following ASTM D2344/D2344M where its span-to-thickness requirements can be met for the four-ply laminates, with at least five valid specimens per selected group drawn from different plates; the apparent short-beam strength F_sbs = 0.75 P_max/(b h) and the failure mode are reported, recognising that the result is not automatically a pure interlaminar shear strength.

====================================================================
4 RESULTS AND DISCUSSION
====================================================================
4.1 Simulation Results
All values come from the simulation tools at repository commit 39ba8b0. GPU-solver results were obtained in quick CPU mode and are labelled quick, not converged.
4.1.1 Verification
The 53 unit tests pass in about 25 s, the lattice Boltzmann benchmark in about 10 s, and the 11 built-in solver checks in about 30 s.
Table 4.1 Verification results
Check | expected | obtained
Worked example recomputed independently | identical | agrees to 12 significant digits
Uniform 3-D box | k I | relative error 3.6e-16
Layers in series/parallel; with interface resistance | harmonic/arithmetic mean; + 2R | errors 5.4e-15; 2.8e-14
Honeycomb vs fitted-mesh FE (k_w 200, k_h 0.026 W/m K, t/l 0.1) | 11.17/11.18 W/m K | 11.155/11.141 (−0.13%/−0.35%)
True-thickness honeycomb at defaults within HS bounds | 27.04–61.94 mW/m K | 61.84 (+1.1% on formula); x–y split 0.16%
Pixel FV ideal honeycomb vs formula | 60.6 mW/m K | 59.2 (−2.4%); x, y = 57.6, 60.8
Energy balance | below tolerance | 2.9e-12 (Pixel FV); <= 5.5e-8 (33 CG solves)
Grid refinement | small change | Pixel FV 2x finer < 3%; true-thickness 2 -> 4 px 0.3%
Local Kn wide pores vs Knudsen | 26.11 mW/m K | 25.95 (−0.6%)
Monte Carlo chords, parallel plates vs Knudsen | exact, Kn 0.01–10 | within 3% (sampling noise)
Ray tracing energy closure; opaque walls | 1.000; 0.150 mW/m K | 1.000 every slab; 0.144
Lattice Boltzmann Rayleigh–Bénard, Pr 0.7 | Nu = 1 below 1708; 2.1 at 5000; 2.6 at 10 000 | 1.0000 at 1000, 1500; 2.09; 2.62
The solvers reproduce exact solutions to round-off; the true-thickness solver matches an independent FE solution within 0.35%; detailed methods reproduce their formulas within 0.6–2.4%, the 2.4% (and the 5.5% x–y split) of Pixel FV being the pixel staircase on ±30° walls, which the supersampled faces reduce to 0.16%.
4.1.2 Baseline breakdown
At the defaults the fast methods give k_perp = 35.5 + 25.6 + 0.150 + 0 = 61.3 mW/m K and k_par = 71.0 + 25.6 + 0.150 + 0 = 96.8 mW/m K (anisotropy 1.58); Pixel FV gives 59.3 and 95.9 (1.62). The solid walls carry 58% of the heat across and 73% along the channels, air almost all the rest, radiation 0.2% and convection none. The wall conductivity is the decisive input (Figure: stacked bars by path).
4.1.3 Pore-size sweep
Mode A (t fixed): k_perp falls from 222 mW/m K at 5 um to 31 at 500 um and the anisotropy from 1.90 to 1.07, because porosity rises. Mode B (pitch fixed) shows a steeper version. Mode C (porosity fixed, diagnostic only) changes k_perp only from 60.3 to 63.8 mW/m K over two decades. At atmospheric pressure, pore size matters through porosity, not size itself: a freezing study that changes pore size without changing solids loading should expect a small thermal effect unless the walls change too.
4.1.4 Structural defects
One crack per wall lowers k_perp by 23% at 5% crack length (59.2 -> 45.4) and 34% at 15% (39.1), while k_par drops 4% and 11% and porosity barely changes; anisotropy rises from 1.62 to 2.03 (5%) and 2.18 (15%). The default defects (10% spread, 20% wall variation, 5% cracks) give 45.2 and 91.9 mW/m K.
4.1.5 Wall model: first results
Quick mode for B10 (83 wt% BN, dense wall 1.93 g/cm3; 80 x 80 x 14 voxels of 20 nm, two random walls, 1.35 s per solve on two CPU cores): along-wall 61.4 W/m K (57.1–65.7), through-wall 1.98 W/m K, inside the parallel (229) and series (1.44) bounds. Not converged (20 nm voxels do not resolve 30 nm sheets). In the honeycomb at true thickness this wall gives k_perp = 573 mW/m K (535–612) and k_par = 1115 mW/m K.
Table 4.2 One-at-a-time sensitivity of the B10 wall (baseline 61.4 W/m K)
Input (low–high) | k_wall at low / high (W/m K) | swing % of baseline
Sheet–sheet contact R_c (1e-9–1e-7 m2K/W) | 118.6 / 22.0 | 158
BN in-plane k (100–550 W/m K) | 32.8 / 81.7 | 80
Sheet tilt spread (3–30°) | 76.0 / 41.8 | 56
Sheet diameter (0.5–1.28 um) | 36.3 / 70.2 | 55
Wall porosity (0–0.4) | 61.4 / 27.5 | 55
BN–binder R_K (0.6e-8–5e-8) | 61.8 / 59.8 | 3.4
CNF k (0.5–2.0) | 60.5 / 61.8 | 2.1
PMSQ k (0.1–0.3) | 60.9 / 61.7 | 1.4
In a BN-continuous wall heat crosses from sheet to sheet, so contacts, sheet size and flatness and wall porosity dominate and the binder hardly matters. Measurements to make first: BN grade sheet size and thickness (datasheet or TEM), sheet alignment and wall porosity (SEM, density check), with R_c kept as a swept unknown.
Dry vs infused: for a dry layer the HS bracket spans a factor 2.3 and doubling k_wall raises k_perp by 58%; with epoxy in the cells the bracket narrows to 14% and doubling k_wall changes k_perp by 15%. The voxel solver is therefore needed for dry BN layers only; infused CNT plies can use closed-form bounds.
4.1.6 Model versus measurement
Discrepancy 1, values below the air floor: BNNS/WPU and BNNS/PVA aerogels report 16.2–23.5 mW/m K across their channels, below the 25.6 mW/m K that air in a 98%-porous honeycomb of 30 um channels must carry at 1 atm. No air-filled micron-channel model can reach these values by changing the wall. Possible causes: nanoporous walls (the B10 dense wall would be 1.93 g/cm3 against a reference skeleton density of 1.12 g/cm3), discontinuous channels, or transient-plane-source measurements underestimating the transverse value of anisotropic porous samples (Gustafsson, 1991; Lou et al., 2023). The CNF/BN/MTMS cryogel of Zhao et al. (2022), closest to this project's composition, reports 33.9 mW/m K radially, above the floor and consistent with the model's physics.
Discrepancy 2, anisotropy: the model gives 1.6 (ideal) to 2.2 (heavily cracked) against 5.8 for BNNS/WPU (Chan et al., 2022) but 1.83 for CNF/BNNS/MTMS (Zhao et al., 2022). For the project's own material family the predicted anisotropy is therefore plausible; the high value of Chan et al. may come from 3-D features (bridges, waviness), aligned BN in the walls or an underestimated transverse measurement.
Discrepancy 3, wall conductivity: the ideal B10 wall gives about 61 W/m K, fifteen times the 4.0 W/m K back-calculated from Chan et al. Part of the gap is not a model error: that reference wall is polymer-rich (about 8–16 wt% BNNS) while B10 is 83 wt% BN. The rest lies in hypothetical microstructure inputs and the unconverged grid; the planned analysis reports which input combinations give a given wall value rather than fitting them. A first consistency check: with Zhao et al.'s radial value (33.9 mW/m K) and a gas term of about 25.6 mW/m K, the implied transverse solid term is about 8 mW/m K, i.e. (1 − phi) k_wall of about 16 mW/m K — a modest wall conductivity or a low solid fraction, to be checked against their reported density.
Table 4.3 Discrepancies, causes and resolving evidence
Discrepancy | model | measured | candidate causes | evidence that resolves it
Below air floor | 45–61 mW/m K; floor 25.6 | 16.2–23.5 (BNNS/polymer); 33.9 (CNF/BN/MTMS) | nanoporous walls; discontinuous channels; test method | SEM of walls; porosity; steady-state test of own layers
Anisotropy | 1.6–2.2 | 5.8 (BNNS/WPU); 1.83 (CNF/BN/MTMS) | 3-D bridges; aligned BN; underestimated k_perp | SEM of both sections; 3-D model from SEM
Wall conductivity | about 61 W/m K (B10, quick) | about 4 W/m K (polymer-rich reference) | different wall material; contacts; sheet size, tilt; wall porosity; grid | BN grade data/TEM; SEM; density; GPU convergence
4.1.7 Limitations
Web-tool walls are 4 px with reduced solid fraction (removed by the GPU solver); ray tracing is 2-D and wall optics, specific extinction, emissivity and accommodation are hypothetical; the LBM check uses a periodic layer; air properties in Ra are fixed at 300 K; the wall RVE results are quick, unconverged, with hypothetical sheet geometry, contact resistance and PMSQ properties; solid–gas coupling is neglected except in Pixel FV; the reference geometry is from the literature until SEM of the specimens is available; the model so far describes the dry layer, not the infused laminate.

4.2 Experimental Results
[Group: insert the status of fabrication and any first measurements (panel masses, mass gain on infusion, reflectance spectra, first temperature runs). If none are available by submission, state which specimens have been fabricated, which tests are scheduled, and present the expected comparison: P as calibration case; L4 vs L5 isolates BN vs commercial coating; L3 vs L1 isolates post-infusion coating vs pre-infusion BN aerogel; L1 vs L2 isolates CNT vs BN plies.]

====================================================================
5 FUTURE PLAN
====================================================================
5.1 Formulation Optimisation
Following the layout comparison of Semester 1, the selected layout will be used for formulation optimisation in Semester 2, in which CNT and BN contents are varied systematically. The programme includes 10 specimen groups with three independently fabricated panels per group, 30 panels in total; extra panels are prepared if required for trials and testing (Table 5.1).
Table 5.1 Specimen groups for formulation screening
Stage | groups | variable | fixed conditions | panels
CNT formulation | C0, C2.5, C5, C7.5 | CNT 0/2.5/5/7.5 wt% | CNF 1 wt%; MTMS 2 wt%; no BN surface layer | 12
Reference | P | conventional CFRP without functional layers | four carbon-fabric plies; identical lay-up, resin and cure | 3
BN formulation | B0, B5, B10, B20 | BN 0/5/10/20 wt% | CNF 1 wt%; MTMS 2 wt%; controlled surface-layer thickness | 12
Combined | C* + B* | selected formulations | selected processing conditions | 3
C* and B* denote the selected CNT and BN formulations; the final comparison is among P, C*, B* and C* + B*. Materials and slurry preparation remain unchanged (50.00 g batches, Table 5.2).
Table 5.2 Slurry formulations for screening (per 50.00 g batch)
Formulation | CNF stock (g) | CNT dispersion (g) | BN (g) | MTMS (g) | added water (g)
C0/B0 | 12.50 | 0 | 0 | 1.00 | 36.50
C2.5 | 12.50 | 9.62 | 0 | 1.00 | 26.88
C5 | 12.50 | 19.23 | 0 | 1.00 | 17.27
C7.5 | 12.50 | 28.85 | 0 | 1.00 | 7.65
B5 | 12.50 | 0 | 2.50 | 1.00 | 34.00
B10 | 12.50 | 0 | 5.00 | 1.00 | 31.50
B20 | 12.50 | 0 | 10.00 | 1.00 | 26.50
5.2 Simulation Plan
January: run the K_cond solver in full GPU mode with a voxel-halving convergence study; build the specimen model for L1–L5 and P and calibrate once on P. February: introduce SEM-based inputs (pore size, wall thickness, channel direction, wall porosity) and propagate uncertainty with Latin-hypercube sampling and Sobol indices. March: run the composition sweep matching the screening matrix (B0–B20, C0–C7.5) so that each experimental group has a predicted band, then freeze the code before the final report.

====================================================================
6 PROJECT MANAGEMENT
====================================================================
The team consists of three final-year BEng (Hons) Aviation Engineering students at The Hong Kong Polytechnic University; the academic supervisor is Prof. CHAN Kit-Ying.
6.1 Team Organisation
Table 6.1 Contributions and workload (names alphabetical by surname; not an order of contribution)
Student | SID | workload | contribution
CHAN Man Ho | 23115045D | [fill] | 33.3%
CHIK Long Tin | 23076727D | [fill] | 33.3%
SIU Ka Shun | 23076695D | [fill] | 33.3%
[Group: fill workload with the actual tasks of each student, e.g. literature review, slurry and freeze-casting, VARI and coating, optical and thermal testing, simulation, report sections. Do not assign the simulation to a student unless that is how the work was done.]
6.2 Project Schedule
The project spans one year and requires time management, organisation and close cooperation among the three members; the team follows the schedule in Figure 6 (Semester 1 and proposed Semester 2).
Table 6.2 Simulation work packages and milestones
Work package | main tasks | milestone | date | status
WP1 literature and plan | heat-transfer review, measured data, meeting constraints, build plan | M1 plan agreed | Oct 2026 | done
WP2 aerosim v0.1 | structure, four paths, fast and detailed methods, web UI, 53 tests | M2 tool verified | 15 Nov 2026 | done
WP3 K_cond solver | recipe -> wall RVE; true-thickness honeycomb; PCG/FFT; checks | M3 CPU-verified solver | 24 Nov 2026 | done (GPU runs pending)
– | interim report | M4 | 21 Dec 2026 | in progress
WP4 specimen model | 3-D plate; layer properties; calibrate on P; predict L1–L5 | M5 | Jan 2027 | planned
WP5 GPU, uncertainty, sweep | convergence; SEM inputs; Sobol; composition sweep; code freeze | M6, M7 | Feb–Mar 2027 | planned
– | final report; oral | M8, M9 | 16 Apr; 19–21 Apr 2027 | planned
6.3 Resources
Laptop CPU (web tool, tests, quick solver; all interim results under 3 min); Google Colab GPU (A100/H100 when allocated) for full solver runs, logged and resumable, cost tracked against the HK$1,000 per-student allowance; open-source Python (NumPy, SciPy, CuPy); GitHub repository for version control and reproducibility; laboratory equipment for freeze-casting, freeze-drying, VARI, spectrometry and thermal testing [group to list].
6.4 Risk Register
Risk | L | I | mitigation
SEM images late or unavailable | M | H | literature defaults labelled; procedural 3-D structures; request offcuts early
Wall conductivity uncertain by an order of magnitude | H | M | report bands; prioritise BN sheet data and wall porosity; no tuning
Limited or interrupted GPU access | M | M | interim results CPU-only; resumable jobs; workstation backup
Resin enters the BN surface layer | M | H | model dry and infused states; record mass gain and cross-sections per plate
Sedimentation or poor dispersion at high CNT/BN loading | M | M | pilot C2.5 and B5 first; check castability before C7.5/B20
Temperature rise dominated by boundary conditions | M | M | identical heater interface and supports; calibrate on P; predict L1–L5 blind
Short-beam test not applicable to thin laminates | M | M | check span-to-thickness; report failure mode; treat as apparent strength

====================================================================
7 CONCLUSION
====================================================================
1. Six four-ply laminate configurations (L1–L5, P) and two fixed slurries (C2.5, B10) have been defined, with slurry quantities, freezing set-up and test procedures specified so that the effect of aerogel location, BN surface layer and coating type can be isolated.
2. A verified two-level model of the conductivity of freeze-cast honeycomb layers has been built: exact solutions are reproduced to round-off and an independent FE benchmark within 0.35%.
3. At the reference structure the walls carry 58% of the heat across and 73% along the channels; radiation contributes 0.2% and convection none; at atmospheric pressure pore size acts through porosity. Because the freezing set-up grows channels through the thickness, the specimens' through-thickness value corresponds to the layer's high direction.
4. The predicted anisotropy (1.6–2.2) is consistent with the CNF/BN/MTMS cryogel of Zhao et al. (1.83); sub-air values reported for BNNS/polymer aerogels cannot be reproduced by air-filled micron channels and point to nanoporous walls or test-method effects.
5. B-series walls are BN-continuous (62–91 vol% BN); their conductivity is controlled by sheet contacts, BN conductivity, sheet alignment and wall porosity, and whether resin enters the BN surface layer during infusion is the most important open question for the thermal comparison. These, together with SEM of the specimens and infrared optical data, are the measurements to make first.

====================================================================
REFERENCES (APA 7; items marked [complete] were cited in the group draft without full details)
====================================================================
Adegun, M. H., Chan, K.-Y., Yang, J., Venkatesan, H., Kim, E., Zhang, H., Shen, X., Yang, J., & Kim, J.-K. (2023). Anisotropic thermally superinsulating boron nitride composite aerogel for building thermal management. Composites Part A: Applied Science and Manufacturing, 169, 107522. https://doi.org/10.1016/j.compositesa.2023.107522
Apostolopoulou-Kalkavoura, V., Munier, P., & Bergström, L. (2021). Thermally insulating nanocellulose-based materials. Advanced Materials, 33(28), 2001839. https://doi.org/10.1002/adma.202001839
ASME. (2009). Standard for verification and validation in computational fluid dynamics and heat transfer (ASME V&V 20-2009). American Society of Mechanical Engineers.
ASTM International. (2022). ASTM D2344/D2344M: Standard test method for short-beam strength of polymer matrix composite materials and their laminates. [check edition]
ASTM International. (2020). ASTM G173-03(2020): Standard tables for reference solar spectral irradiances. [check edition]
Baetens, R., Jelle, B. P., Thue, J. V., Tenpierik, M. J., Grynning, S., Uvsløkk, S., & Gustavsen, A. (2010). Vacuum insulation panels for building applications: A review and beyond. Energy and Buildings, 42(2), 147–172. https://doi.org/10.1016/j.enbuild.2009.09.005
Bergman, T. L., Lavine, A. S., Incropera, F. P., & DeWitt, D. P. (2011). Fundamentals of heat and mass transfer (7th ed.). John Wiley & Sons.
Bird, G. A. (1994). Molecular gas dynamics and the direct simulation of gas flows. Clarendon Press.
Chan, K.-Y., Shen, X., Yang, J., Lin, K.-T., Venkatesan, H., Kim, E., Zhang, H., Lee, J.-H., Yu, J., Yang, J., & Kim, J.-K. (2022). Scalable anisotropic cooling aerogels by additive freeze-casting. Nature Communications, 13, 5553. https://doi.org/10.1038/s41467-022-33234-8
Collishaw, P. G., & Evans, J. R. G. (1994). An assessment of expressions for the apparent thermal conductivity of cellular materials. Journal of Materials Science, 29, 2261–2273.
Cooper, S. J., Bertei, A., Shearing, P. R., Kilner, J. A., & Brandon, N. P. (2016). TauFactor: An open-source application for calculating tortuosity factors from tomographic data. SoftwareX, 5, 203–210. https://doi.org/10.1016/j.softx.2016.09.002
Ferguson, J. C., Panerai, F., Borner, A., & Mansour, N. N. (2018). PuMA: The Porous Microstructure Analysis software. SoftwareX, 7, 81–87. https://doi.org/10.1016/j.softx.2018.03.001
Gibson, L. J., & Ashby, M. F. (1997). Cellular solids: Structure and properties (2nd ed.). Cambridge University Press.
Glicksman, L. R. (1994). Heat transfer in foams. In N. C. Hilyard & A. Cunningham (Eds.), Low density cellular plastics: Physical basis of behaviour. Chapman & Hall.
Gostick, J. T., Khan, Z. A., Tranter, T. G., Kok, M. D. R., Agnaou, M., Sadeghi, M., & Jervis, R. (2019). PoreSpy: A Python toolkit for quantitative analysis of porous media images. Journal of Open Source Software, 4(37), 1296. https://doi.org/10.21105/joss.01296
Gustafsson, S. E. (1991). Transient plane source techniques for thermal conductivity and thermal diffusivity measurements of solid materials. Review of Scientific Instruments, 62(3), 797–804. https://doi.org/10.1063/1.1142087
Han, Y., Li, S., Liu, H., & Li, Y. (2022). Lattice Boltzmann simulation of coupling heat transfer between solid and gas phases of nanoporous materials. Nanomaterials, 12(19), 3424. https://doi.org/10.3390/nano12193424
Hashin, Z., & Shtrikman, S. (1962). A variational approach to the theory of the effective magnetic permeability of multiphase materials. Journal of Applied Physics, 33(10), 3125–3131. https://doi.org/10.1063/1.1728579
Hestenes, M. R., & Stiefel, E. (1952). Methods of conjugate gradients for solving linear systems. Journal of Research of the National Bureau of Standards, 49(6), 409–436.
Hildebrand, T., & Rüegsegger, P. (1997). A new method for the model-independent assessment of thickness in three-dimensional images. Journal of Microscopy, 185(1), 67–75. https://doi.org/10.1046/j.1365-2818.1997.1340694.x
Hrubesh, L. W., & Pekala, R. W. (1994). Thermal properties of organic and inorganic aerogels. Journal of Materials Research, 9(3), 731–738. https://doi.org/10.1557/JMR.1994.0731
Jiang, P., Qian, X., Yang, R., & Lindsay, L. (2018). Anisotropic thermal transport in bulk hexagonal boron nitride. Physical Review Materials, 2(6), 064005. https://doi.org/10.1103/PhysRevMaterials.2.064005
Kaganer, M. G. (1969). Thermal insulation in cryogenic engineering. Israel Program for Scientific Translations.
Kench, S., & Cooper, S. J. (2021). Generating three-dimensional structures from a two-dimensional slice with generative adversarial network-based dimensionality expansion. Nature Machine Intelligence, 3(4), 299–305. https://doi.org/10.1038/s42256-021-00322-1
Kench, S., Squires, I., & Cooper, S. J. (2023). TauFactor 2: A GPU accelerated python tool for microstructural analysis. Journal of Open Source Software, 8(88), 5358. https://doi.org/10.21105/joss.05358
Kim, E., Chan, K.-Y., Yang, J., Venkatesan, H., Adegun, M. H., Zhang, H., Lee, J.-H., Shen, X., & Kim, J.-K. (2023). Engineering anisotropic structures of thermally insulating aerogels with high solar reflectance for energy-efficient cooling applications. Journal of Materials Chemistry A, 11(13), 7105–7114. https://doi.org/10.1039/D2TA09983G
Kong, X., Li, L., Li, M., Xia, J., Wang, Y., Wei, X., Xiong, S., Gong, P., Pan, Z., Wu, X., Cai, T., Nishimura, K., Lin, C.-T., Jiang, N., & Yu, J. (2022). Two-dimensional hexagonal boron nitride nanosheets as lateral heat spreader with high thermal conductivity. Frontiers in Materials, 8, 817061. https://doi.org/10.3389/fmats.2021.817061
Lou, F., Dong, S., Zhu, K., Chen, X., & Ma, Y. (2023). Thermal insulation performance of aerogel nano-porous materials: Characterization and test methods. Gels, 9(3), 220. https://doi.org/10.3390/gels9030220
Lu et al. (2025). [complete: bacterial-cellulose/CNT/MTMS porous material by directed freezing]
Luo et al. (2026). [complete: source of Figure 1, freeze-casting directions]
Merivaara et al. (2022). [complete: residual moisture in nanofibrillated-cellulose aerogels]
Modest, M. F. (2013). Radiative heat transfer (3rd ed.). Academic Press.
Mohamad, A. A. (2011). Lattice Boltzmann method: Fundamentals and engineering applications with computer codes. Springer.
Moulinec, H., & Suquet, P. (1998). A numerical method for computing the overall response of nonlinear composites with complex microstructure. Computer Methods in Applied Mechanics and Engineering, 157(1–2), 69–94. https://doi.org/10.1016/S0045-7825(97)00218-1
Nan, C.-W., Birringer, R., Clarke, D. R., & Gleiter, H. (1997). Effective thermal conductivity of particulate composites with interfacial thermal resistance. Journal of Applied Physics, 81(10), 6692–6699. https://doi.org/10.1063/1.365209
[NASA conductive CFRP: complete]
NVIDIA. (2020). NVIDIA A100 Tensor Core GPU architecture [White paper].
NVIDIA. (2022). NVIDIA H100 Tensor Core GPU architecture [White paper].
Oberkampf, W. L., & Roy, C. J. (2010). Verification and validation in scientific computing. Cambridge University Press.
Obori, M., Suh, D., Yamasaki, S., Kodama, T., Saito, T., Isogai, A., & Shiomi, J. (2019). Parametric model to analyze the components of the thermal conductivity of a cellulose-nanofibril aerogel. Physical Review Applied, 11(2), 024044. https://doi.org/10.1103/PhysRevApplied.11.024044
Okuta, R., Unno, Y., Nishino, D., Hido, S., & Loomis, C. (2017). CuPy: A NumPy-compatible library for NVIDIA GPU calculations. Proceedings of the Workshop on Machine Learning Systems (LearningSys) at NIPS 2017.
Patankar, S. V. (1980). Numerical heat transfer and fluid flow. Hemisphere.
Raman, A. P., Anoma, M. A., Zhu, L., Rephaeli, E., & Fan, S. (2014). Passive radiative cooling below ambient air temperature under direct sunlight. Nature, 515(7528), 540–544. https://doi.org/10.1038/nature13883
Randrianalisoa, J., & Baillis, D. (2014). Thermal conductive and radiative properties of solid foams: Traditional and recent advanced modelling approaches. Comptes Rendus Physique, 15(8–9), 683–695. https://doi.org/10.1016/j.crhy.2014.09.002
Scotti, K. L., & Dunand, D. C. (2018). Freeze casting – A review of processing, microstructure and properties via the open data repository, FreezeCasting.net. Progress in Materials Science, 94, 243–305. https://doi.org/10.1016/j.pmatsci.2018.01.001
Shan, X. (1997). Simulation of Rayleigh–Bénard convection using a lattice Boltzmann method. Physical Review E, 55(3), 2780–2788. https://doi.org/10.1103/PhysRevE.55.2780
Skochdopole, R. E. (1961). The thermal conductivity of foamed plastics. Chemical Engineering Progress, 57(10), 55–59.
Sozcu et al. (2023). [complete]
Swartz, E. T., & Pohl, R. O. (1989). Thermal boundary resistance. Reviews of Modern Physics, 61(3), 605–668. https://doi.org/10.1103/RevModPhys.61.605
Tchessalov et al. (2023). [complete]
Torquato, S. (2002). Random heterogeneous materials: Microstructure and macroscopic properties. Springer.
Toray. [complete: T300 technical data sheet]
Villière, M., Lecointe, D., Sobotka, V., Boyard, N., & Delaunay, D. (2013). Experimental determination and modeling of thermal conductivity tensor of carbon/epoxy composite. Composites Part A: Applied Science and Manufacturing, 46, 60–68. https://doi.org/10.1016/j.compositesa.2012.10.012
Wang, X., Yu, Z., Bian, H., Wu, W., Xiao, H., & Dai, H. (2019). Thermally conductive and electrical insulation BNNS/CNF aerogel nano-paper. Polymers, 11(4), 660. https://doi.org/10.3390/polym11040660
Wegst, U. G. K., Schecter, M., Donius, A. E., & Hunger, P. M. (2010). Biomaterials by freeze casting. Philosophical Transactions of the Royal Society A, 368(1917), 2099–2121. [check]
Yang, J., Chan, K.-Y., Venkatesan, H., Kim, E., Adegun, M. H., Lee, J.-H., Shen, X., & Kim, J.-K. (2022). Superinsulating BNNS/PVA composite aerogels with high solar reflectance for energy-efficient buildings. Nano-Micro Letters, 14, 54. https://doi.org/10.1007/s40820-022-00797-6
Yuan, C., Li, J., Lindsay, L., Cherns, D., Pomeroy, J. W., Liu, S., Edgar, J. H., & Kuball, M. (2019). Modulating the thermal conductivity in hexagonal boron nitride via controlled boron isotope concentration. Communications Physics, 2, 43. https://doi.org/10.1038/s42005-019-0145-5
Zeng, S. Q., Hunt, A., & Greif, R. (1995). Mean free path and apparent thermal conductivity of a gas in a porous medium. Journal of Heat Transfer, 117(3), 758–761. https://doi.org/10.1115/1.2822642
Zhao, J., Zhou, J., Li, H., & Xiao, A. (2022). Directional fabricating of flexible and compressible cellulose nanofibril composite cryogel with excellent thermal insulation, flame-retardancy and radiative cooling for efficient thermal management. Cellulose, 29. https://doi.org/10.1007/s10570-022-04861-7
Zhu, H., Li, Y., Fang, Z., Xu, J., Cao, F., Wan, J., Preston, C., Yang, B., & Hu, L. (2014). Highly thermally conductive papers with percolative layered boron nitride nanosheets. ACS Nano, 8(4), 3606–3613. https://doi.org/10.1021/nn500134m
Zuo et al. (2023). [complete: carboxylated CNT in MTMS-treated nanocellulose/MXene aerogel]

====================================================================
APPENDICES
====================================================================
Appendix A Worked example at the defaults (d 30 um, t 0.27 um, k_wall 4.0 W/m K, 300 K, 101 325 Pa, alpha 1, eps 0.9, 1000 K/m)
pitch 30.27 um; porosity (30/30.27)^2 = 0.98224; bulk density 19.9 kg/m3; solid along 0.017760 x 4.0 = 71.0 mW/m K; solid across 35.5; k_air 26.3; mean free path 66.5 nm; Kn 0.00222; beta 1.643; k_gas 26.1; gas term 0.98224 x 26.11 = 25.6; radiation 4 x 5.670e-8 x 300^3 x 30e-6 x 0.9/1.1 = 0.150; Ra 7.4e-8 -> k_conv 0; k_perp 61.3; k_par 96.8; anisotropy 1.58.
Appendix B Input register: see Table 3.2 and the input blocks of the code (every input has value, unit, status, source).
Appendix C Code availability: github.com/saul-gitman/FYP, commit 39ba8b0. Commands: python -m aerosim serve (web UI); python -m aerosim run (breakdown); python -m aerosim sweep (pore-size sweep); python -m pytest (53 tests) and python -m pytest -m slow (LBM benchmark); python K_cond_GPU_solver/colab_k_cond.py (wall and honeycomb solver; RUN_SENSITIVITY = True for Table 4.2). All random processes use fixed seeds.
Appendix D Use of AI declaration: [rewrite to state accurately how AI tools were used, including for the simulation code and simulation text; decision deferred].
