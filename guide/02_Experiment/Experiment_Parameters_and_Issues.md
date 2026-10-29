# Supplied experiment guide: parameters and open issues

Source: `Experiment_Guide_original.docx`, preserved unchanged. All settings below are **planned guide values**, not completed experiments or an independently approved laboratory protocol. The extraction beside the guide preserves its original text and tables in document order.

## Placement and fabrication

Outside to inside: BN/CNF/MTMS surface → upper carbon-cloth/epoxy → CNT/CNF/MTMS interlayer → lower carbon-cloth/epoxy. Place a 20 × 20 mm heater on the back centre during thermal tests. The guide calls for putting CNT slurry between 50 × 50 mm cloth samples and BN slurry on top, then freezing on a cold metal base, freeze-drying, and controlled resin infusion/cure. Record dry and cured dimensions, mass gain, skeleton retention, resin filling and residual pores. A later integrated-fabrication comparison mentions −80 °C freezing, versus liquid nitrogen in the earlier process.

## Planned screening matrix

| Series | Groups | Fixed formulation / construction | Independent plates |
|---|---|---|---|
| Carbon | C0, C2.5, C5, C7.5, C10 | CNT = 0, 2.5, 5, 7.5, 10 wt% of wet slurry; CNF dry = 1 wt%; MTMS feed = 2 wt%; no BN surface | 5 × 3 = 15 |
| Plain baseline P | Ordinary CFRP | Same two cloth layers, orientation, epoxy and cure; no added functional layers | 3 |
| BN | B0, B5, B10, B20, B30 | BN = 0, 5, 10, 20, 30 wt% wet slurry; CNF dry = 1 wt%; MTMS feed = 2 wt% | 5 × 3 = 15 |
| Combined | C* + B* | Selected carbon and BN formulations | 3 |

Total: 12 groups and 36 independently made plates. Pilot and destructive mechanical specimens are extra. C* and B* are not specified final compositions; they are selected after screening. The guide does not fully define whether each B-series substrate contains the carbon-free support/interlayer or no interlayer: resolve that before interpreting contrasts.

## Slurry and processing values retained from the guide

- Batch total 50.00 g; CNF stock 4.00 wt% solids; stock mass 12.50 g gives 0.50 g dry CNF. MTMS feed 1.00 g per batch.
- For stock solids fraction c (decimal), CNF stock = 0.50/c g; make-up water = 50 − stock − filler − MTMS.
- First mix stock and ~80% of added water for 10 min. Add filler and stir 600–1000 rpm for 10 min.
- Intermittent cooled ultrasound: pilot starting point 10 min net ultrasound, 2 s on / 2 s off; slurry below 30 °C. BN receives the same dispersion programme.
- Add MTMS slowly; stir 20 min; make up batch mass; stand 2 h; remix and degas. Hydrolysis/condensation conditions and final silane retention are not specified.
- Pilot C2.5 and B5, checking high-load C7.5/C10/B20/B30 for sedimentation, agglomeration, castability, cracks and powder shedding.
- Freeze on the metal cold base, insulate top/sides. Liquid nitrogen is mentioned. Freeze-dry initial setting 48 h, pressure chosen in controllable 10–30 Pa range; keep specimen frozen during primary drying.
- Epoxy is an existing formulation; WEST SYSTEM 105/209 is an example. Actual mixing ratio, cure and post-cure must follow the batch documentation. At least 7 d at room temperature is mentioned before testing, together with meeting required cure conditions.

The separate `recipe_mass_balance_derived.csv` fills the guide's blank make-up-water column by arithmetic. It is an added calculation, not a change to the original guide. Wet-slurry mass fraction is not final dry-skeleton or cured-laminate mass fraction; MTMS loses volatile species and infusion adds epoxy.

## Geometry and measurements

- Plate fabrication size: 50 × 50 mm. A 40 × 40 mm region is retained for thermal/optical tests after trimming; a later thermal section again calls the specimen 50 × 50 mm. Record the physical tested size and illuminated area.
- BN thickness: about 1 mm in body/matrix, but about 0.5 mm in a separate table. Carbon layer, cloth/epoxy layers and total cured thickness must be measured.
- Reflectance: integrating-sphere UV–Vis–NIR, total hemispherical R from 300–2500 nm; white reference and dark baseline; centre + two positions averaged per independent plate. AM1.5G weighting over that measured band. Compare standalone and supported/bonded surfaces.
- Through-thickness effective k near 25 °C: use a method compatible with actual laminate thickness; state contact resistance corrections. Multilayer laser-flash analysis needs appropriate density and heat capacity, not an automatic homogeneous-material conversion.
- R''z = L/kz for whole-laminate thickness L, unit m² K/W. Dark system Rsys = (Theater − Tambient)/P, unit K/W. These are different quantities.
- Ambient 25 ± 2 °C; no strong forced flow; record wind and humidity. Temperature every 1–5 s; IR frames every 30–60 s; thermocouples check IR emissivity differences.
- At least 60 min per run. Steady criterion: absolute slope below 0.1 °C/min over last 10 min; extend if needed. Reset near ambient before the next run.
- Same heater interface/pressure, four low-k supports, specimen height and illuminated area; calibrated irradiation map at centre and four corners.

| Load case | Internal heater | Irradiation |
|---|---|---|
| Dark internal heating | 2 W; optional extension 5 W | Off |
| Solar-only | Off | 1000 W/m² |
| Combined | 2 W, matched to dark comparison | 1000 W/m² |

C series: k and dark heating; B series: reflectance and solar-only; final P/C*/B*/C*+B*: all three cases. Keep replicate plates separate from repeated positions on one plate. For mechanical validation, the guide asks to check applicability of ASTM D2344/D2344M to the actual thin two-cloth structure, at least five valid specimens per selected group from different plates if applicable, and record failure modes. Short-beam strength is not automatically pure interlaminar shear strength.

## Issues that must remain visible

| ID | Original conflict / omission | Consequence for the next agent |
|---|---|---|
| E01 | BN about 1 mm versus table about 0.5 mm | Retain both as candidate geometry cases; use measured final value for validation |
| E02 | Liquid-nitrogen base freezing versus later −80 °C “same” process | Actual base temperature, cooling history and freezing duration are unresolved |
| E03 | “about 0.3 Pa gauge pressure” for compaction/infusion | Unit/reference is ambiguous; do not reinterpret as MPa, bar, absolute pressure or vacuum level |
| E04 | Bottom cooling with top/side insulation vs earlier desire for in-plane pores | Freezing direction may be through thickness; measure alignment and rotate K accordingly |
| E05 | In-place fabrication versus separately made/bonded comparison | Integration sequence and resin protection of BN surface are not final |
| E06 | 50 mm sample vs 40 mm retained test region | Model actual tested geometry and footprint; solar power depends on area |
| E07 | All make-up-water table cells blank | Derived arithmetic supplied separately; confirm material stock solids |
| E08 | Final porosity/resin fraction, CNT/BN grade and MTMS reaction not specified | Dry-aerogel literature k cannot be assigned to the cured interlayer |
| E09 | B-series substrate/interlayer control not fully described | Establish a comparable construction before attributing changes only to BN |
| E10 | No measured conductivity, Cp, optical spectra, interface resistance or mechanics included | Use explicit assumptions/sensitivity cases; do not report calibrated predictions |
| E11 | Schedule lists months 1–4 then month 6 | Preserve the source; calendar alignment and month 5 activities are unconfirmed |

The guide is included as the requested Word file, not silently corrected. These notes distinguish an experimental plan from completed findings.
