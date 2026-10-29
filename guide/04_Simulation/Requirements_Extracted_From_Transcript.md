# Requirements extracted from the project meeting

Prepared by the handover editor from the supplied transcript. The receiving agent should implement these requirements, not repeat the extraction. Time references point to `../08_Transcripts/transcript_English.md`. This is an extraction of the discussion, with editor recommendations labelled separately; it is not a claim that the supervisor approved every implementation detail below.

## Immediate simulation scope

| ID | Extracted requirement or direction | Meeting time |
|---|---|---|
| S01 | Preserve the processing → structure → properties framework. Simulation initially maps structure to properties; experiments connect processing to observed properties. | 00:00–01:22; 02:43–03:38 |
| S02 | Start with aerogel alone, leaving carbon fibre out of the initial model. This is an expressly accepted first step. | 14:56–17:04; 30:51–31:51 |
| S03 | Use a simple idealised structure first. Perfect hexagons are not mandatory; circular channels/cylinders or a hollow cell with homogeneous walls are acceptable starting representations. | 04:37–05:32; 11:40–12:40; 27:25–29:50 |
| S04 | Start by varying pore size with one fixed composition. Investigate composition next. Do not launch a five-parameter sweep just because five parameters were mentioned. | 10:42–11:40; 30:19–31:21 |
| S05 | Choose the most influential one or two variables from the references before expanding the study. Keep alignment fixed initially. | 11:10–11:40 |
| S06 | Evaluate thermal conductivity in directions along and transverse to the structure; the discussion explicitly mentions vertical and horizontal directions. | 17:04–17:32; 31:21–31:51 |
| S07 | Define pore geometry consistently: pore size, wall dimensions, porosity and density are related. Do not independently prescribe incompatible values. | 11:40–12:40; 29:50–31:21 |
| S08 | Use literature or available microscopy to select plausible pore size, wall thickness and alignment. A single representative size, such as a distribution midpoint, is acceptable initially. | 08:51–11:10; 18:23–22:45 |
| S09 | A homogeneous cell wall with a mixture-based conductivity is an accepted simple option. Explicit BN platelets and fibrils are a possible later refinement, not the first requirement. | 17:57–18:54; 27:25–29:50 |
| S10 | Explore material proportions, but state exactly which materials and fraction basis are being varied. BN:CNF and BN:CNT are both mentioned in different portions of the discussion. | 04:05–04:37; 17:32–17:57; 34:18–35:17 |
| S11 | Distinguish an ideal optimum from a manufacturable composition. A powder-only wall can be mathematically defined but may not hold together without a supporting/binding network. | 17:32–18:54; 24:37–28:25 |
| S12 | Communicate difficulties and progress, including the absence of results. Do the initial model before waiting for every experimental detail. | 31:21–31:51; 34:18–35:17 |

The numbers 20–50, midpoint 35, the uncertain freezing-temperature example, and 0/10/20/50/100 composition values were conversational examples. Their units or percentage bases were not established. They are **not confirmed model inputs**. The later 20% BN suggestion is also incomplete because its partner acronym and mass basis are unresolved.

## Comparison with experiments

| ID | Extracted direction | Meeting time |
|---|---|---|
| V01 | Exact experimental/simulation microstructure matching is not expected within this project. An idealised model is acceptable if limitations are explained. | 03:08–06:26 |
| V02 | Keep known quantities consistent: constituent properties, stated material percentages and intended alignment should match the corresponding experiment. | 06:26–09:17 |
| V03 | Compare trends across formulations and structural changes. Do not judge the work only by absolute agreement of two values. | 03:38–05:04; 06:53–07:24 |
| V04 | If trends or values disagree, investigate the actual manufactured structure and explain the discrepancy. Propose a modification or future remedy if time permits. | 07:24–08:51 |
| V05 | Use microscopy to distinguish overall channel orientation from platelet/fibril structure inside the walls. These are different modelling scales. | 18:23–23:42 |
| V06 | Real channels and platelet arrangements will be imperfect. The common growth/alignment direction matters more initially than perfect regularity. | 08:21–09:17; 20:25–22:45 |

The meeting's suggestion that experiments often cause discrepancies is a speaker's opinion, not proof that the simulation is correct. **Editor implementation requirement:** verify the numerical model and examine both model assumptions and experimental uncertainty before attributing a mismatch.

## Later CFRP integration

| ID | Extracted direction | Meeting time |
|---|---|---|
| L01 | After the aerogel model works, combine simplified regions into a CFRP-containing model. Excessive microstructure detail makes integration harder. | 12:40–14:56; 28:25–29:21 |
| L02 | Match carbon-fibre alignment and layer spacing/thickness to the actual construction. | 12:40–13:30 |
| L03 | Investigate how interfaces are represented: physical contact, interlocking and chemical bonding were raised as possibilities. No interface model or numerical value was selected. | 13:30–14:56 |
| L04 | Thermal and mechanical responses were discussed as useful outputs. Thermal conductivity is the immediate focus; a tensile/mechanical solver is not a prerequisite to the initial thermal model. | 14:56–16:15 |

## Parallel laboratory work retained for whole-project context

These are experimental actions, not tasks assigned to the software build agent.

- Make a plain CFRP reference plate first and refresh resin-infusion and bag-sealing skills through lab booking/training (31:51–34:50).
- Check the carbon cloth and room-temperature-curing resin systems actually available. A resin number sounding like “209” was recalled uncertainly; weave preferences were not reliably transcribed (32:19–33:22).
- Practise on plain material before risking an aerogel sample. Greater independence in the lab depends on demonstrating competence (33:22–34:50).
- Trial BN-containing, CNT-containing and combined constructions are discussed, including checking whether the layers bond firmly. The precise composition/sequence is partially unclear (34:18–36:08).
- The discussion gives four layers as an initial suggestion; the sample dimension is unclear (“two-five cm” in the ASR) (35:43–36:08).
- Prepare at least three samples per composition to allow for failures and calculate a standard deviation. Three initial compositions are mentioned (36:08–36:36).

## Resolve source differences explicitly

The Word guide supplies the detailed experimental plan; the meeting supplies the immediate modelling sequence. The recording date and revision relationship are not established, so do not assume either silently supersedes the other.

| Topic | Meeting | Word guide / action |
|---|---|---|
| Initial scope | Aerogel alone, fixed composition, pore-size sweep | Full laminate is the eventual experimental system; postpone its solver integration |
| Cloth/layers | Four layers mentioned; meaning needs confirmation | Two carbon-cloth layers specified; keep alternatives in the issue register |
| Sample dimensions | Unclear spoken size | 50 × 50 mm fabrication and 40 × 40 mm retained region appear; use actual measured geometry later |
| Fractions | Several ratios and example percentages, often without basis | Wet-slurry CNT/BN series with fixed dry CNF and MTMS feed; do not equate these to final dry volume fractions |
| BN thickness | Not established | About 1 mm in prose and about 0.5 mm in a table; unresolved |
| Supporting network | CNF/binder network clearly discussed, but CNF/CNT acronyms alternate elsewhere | Guide separately specifies CNF, carboxylated CNT, BN and MTMS; keep them distinct |
| Alignment | Match intended experimental direction; keep fixed first | Bottom-cooled freezing does not establish in-plane alignment; declare the actual axis |
| Temperature/pressure | No confirmed numerical boundary set for the first pore model | Freezing and infusion details have documented ambiguities in `../02_Experiment/Experiment_Parameters_and_Issues.md` |

Do not treat the claimed benefit of adding a filler as a required outcome. The tool must be able to show either increasing or decreasing performance, depending on physics and geometry.
