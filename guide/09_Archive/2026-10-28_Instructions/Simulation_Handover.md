# Simulator handover specification

Status: proposed implementation plan prepared for the receiving agent. No numerical simulation has been run for this handover. This is not an approved laboratory protocol or evidence of measured material properties. Read `../summary.md`, the original proposal, guide, issue register and references before implementation.

## A. Questions the simulator should answer

1. Given an aerogel structure and constituent states, what are its directional conductivities and temperature/heat-flux fields?
2. How do porosity, alignment, pore/wall geometry, filler connectivity and resin infiltration affect those properties?
3. In the actual CFRP panel, how do functional-layer placement and properties change the heater temperature under dark, solar-only and combined loads?
4. What is the trade-off between internal heat removal, incoming-solar shielding, mass and structural integrity?

Primary map is **2 Resulting Structure → 3 Resulting Properties**. Predicting structure from freezing temperature/time requires a separate calibrated processing–structure relationship; do not claim that capability from a visually adjustable geometry.

## B. Model hierarchy and scope

| Level | What to represent | Why |
|---|---|---|
| 0: analytical benchmark | Homogeneous slabs, multilayer series resistance and simple heat-source balance | Check units, signs, contacts and limiting cases |
| 1: dry porous structure | CNF-based skeleton, filler, gas, pore/wall dimensions and orientation | Predict structure-dependent thermal properties |
| 2: infused structure | Skeleton + epoxy + residual gas, cure-related shape changes and interfaces | Bridge dry-aerogel literature to the material actually tested |
| 3: complete panel | Measured CFRP layup, functional layers, local heater, illumination, convection, supports and radiation | Match the experiment and system objective |
| 4: extensions | Spectral optical model; thermoelastic/interface mechanics; calibrated process model | Add only with needed data and verification |

Begin with a transparent resistance/finite-volume/finite-element model. Python and ANSYS were discussed; choose a reproducible route compatible with the available environment. ACP/Mechanical/Fluent and PyANSYS were earlier suggestions, not verified installed dependencies. Resolve the solver choice with the actual receiving agent's capabilities. Airflow CFD is only needed if the boundary-flow problem requires it; a heat-transfer coefficient is a simpler stated boundary model.

## C. Coordinate and state conventions

Proposed global convention: x and y lie in the plate, +z points from inside/heater side toward outside/BN face. Store the complete local material basis for each region. Freezing direction, pore-channel axis, carbon-fibre direction and global thickness direction are separate vectors. Transform material tensors into global coordinates.

For a local conductivity tensor Klocal = diag(k1,k2,k3), Kglobal = Q Klocal Qᵀ, with orthonormal Q whose columns are material axes in global coordinates. Do not assume that the guide's bottom-cooled sample has in-plane aligned channels; the actual freezing geometry could produce a different orientation.

Maintain separate material records for (i) dense skeleton constituents, (ii) dry porous aerogel, (iii) resin-filled aerogel-derived region, (iv) CFRP ply/cloth-epoxy and (v) assembled laminate. Effective properties must carry their length scale and measurement method. Carbon fibre, CNF, CNT and graphene are not synonyms.

## D. Governing thermal equations (standard continuum model)

For each homogenised region, using SI units:

ρ cp ∂T/∂t = ∇·(K ∇T) + qvol;  heat-flux vector q = −K∇T.

T in K; ρ in kg/m³; cp in J/(kg K); K in W/(m K); qvol in W/m³; q in W/m². A steady solve removes the time derivative. Temperature-dependent properties need explicit functions and supported ranges.

At an interface with finite area-normalised contact resistance R''c [m² K/W], normal heat flux is continuous and T1−T2 = qn R''c with a consistent normal/sign convention. A perfect interface is the R''c→0 limit. Model a finite adhesive layer either explicitly or as resistance, without double counting.

For a one-dimensional slab stack, R''total = Σ Li/kz,i + Σ R''c,i. Under fixed ΔT, qn = ΔT/R''total and keq,z = Ltotal/R''total. For a fully insulated one-dimensional specimen with measured total heat rate Qheat [W], k = Qheat L/(A ΔT); if qn is already heat flux [W/m²], k = qn L/ΔT. Keep these notations distinct: earlier discussion mixed q meanings.

The analytical stack is a benchmark, not an adequate full model of a 20 mm heater on a 50 mm panel where lateral spreading and edge losses matter.

## E. Aerogel microstructure and homogenisation

Represent an experimentally defensible RVE: aligned cells/channels or a reconstructed network. Hexagonal channels are one exploratory geometry. Preserve connected solid paths; specify wall/strut thickness, channel diameter distribution, orientation dispersion, bridges, filler distribution and boundary treatment. Map geometric solid and gas volumes to porosity, not just a slider label.

For each loading direction j, impose a known mean gradient, solve for heat flow and average the flux to obtain the corresponding K column: ⟨qi⟩ = −Kij Gj. State whether using periodic boundaries or fixed temperatures with insulated lateral faces; compare finite-size effects. Repeat for three independent directions if necessary. Verify K is symmetric/positive-definite for the reciprocal conduction model and that coordinate rotation works.

Density/porosity/composition are coupled. If constituent mass fractions wi and additive constituent volumes are assumed, ρsolid = 1/(Σ wi/ρi); then ρbulk = (1−φ)ρsolid for a dry, gas-mass-negligible skeleton. Treat the relationship as an assumption and allow measured shrinkage/volume changes to override it. For infused material, volume fractions must satisfy fskeleton + fresin + fgas = 1 and bulk density follows the phase-volume mass balance. Do not independently choose inconsistent density, porosity, wall thickness and composition.

CNT/BN fractions in the guide are wet-slurry mass fractions. Convert to dry retained skeleton and final composite fractions only with the dry masses, chemical retention, density and epoxy uptake data. A BN:C ratio must name the C species and basis (mass or volume; wet feed, dry skeleton or total composite).

## F. Microscopic gas/solid/radiation model and references

**Obori et al. 2019, U25**, is the identified mathematical-method reference. It uses a simple open-cell thermal network, pressure-dependent gas conduction and radiative transfer, fitted to CNF-aerogel experiments under atmospheric and vacuum conditions. Read the linked accepted manuscript before reproducing its network equation, fitting or constants. Its CNF preparation and network differ from the directional CNT/BN/MTMS system here; adaptation needs justification. See `../05_References/Reference_Roadmap.md`.

As a standard small-pore starting approximation, gas conductivity can be written kg = kg,free/(1 + 2β Kn), Kn = ℓmfp/dpore, with gas, temperature, pressure, accommodation convention and characteristic pore definition stated. A hierarchical freeze-cast material may have micrometre channels and nanometre wall pores: choose the physically relevant scales rather than applying a strong Knudsen suppression to every visible channel.

The bookkeeping expression keff ≈ ksolid,contribution + kgas,contribution + kradiative is an approximation. The phase contributions are homogenised paths, not simply the bulk conductivities of each phase added together. A thermal network or coupled numerical phase solve determines their interaction. CNT contacts, BN orientation and contact/phonon resistance require data or labelled effective parameters.

If the medium is optically thick and a diffusion approximation is justified, an equivalent radiative term can use the Rosseland form krad = 16 n² σ T³/(3 βR), with extinction convention and assumptions checked. This cannot automatically describe a thin, partially transparent coating or a boundary solar load. If K is already experimentally effective and includes pore radiation, adding the same radiative term again would double count it. External surface radiation is a separate boundary exchange.

**Lou et al. 2023** is an additional review on modelling/testing porous aerogel heat transport; it was mentioned in the recovered history. **Chan 2022** contains an optical FDTD calculation, which is an electromagnetic solver distinct from time-stepping a heat equation. These are complementary references, not one interchangeable “aerogel model.”

## G. Surface loads, optical model and experiment matching

Guide-based cases: dark heater P = 2 W, optional 5 W; solar-only G = 1000 W/m²; combined 2 W + 1000 W/m². Use the actual illuminated area, heater footprint and any shade/fixture geometry. A 2 W heater over 20 × 20 mm corresponds to 5000 W/m² at that footprint if all electrical power enters the specimen: this is a derived idealisation, not a measured heat split. Account separately for heater losses/contact in validation.

For a simple opaque-surface model, αsolar = 1−Rsolar; if transmission matters, αsolar = 1−Rsolar−τsolar. Absorbed solar surface input is αsolar G. Compute Rsolar = ∫R(λ)I(λ)dλ/∫I(λ)dλ with the stated spectrum and exactly the measured 300–2500 nm range. Do not call limited-band measurements full-spectrum without qualification.

A proposed external surface balance uses outward conduction q·n = h(Ts−Ta) + εσ(Ts⁴−Tsur⁴) − αsolar G, adjusted for other incoming loads. The grey-enclosure radiation approximation is distinct from outdoor spectral sky exchange; use view factors and spectral/atmospheric data for a detailed radiative-cooling model. Solar reflectance does not determine long-wave emissivity. Temperatures in fourth-power radiation terms must be absolute.

Represent supports and side/back heat losses, or explicitly state and test the neglected paths. Calibrate boundary parameters on appropriate baseline data; do not refit them arbitrarily per formulation to force cooling improvements.

## H. Data needed before quantitative validation

Geometry: actual test size, each cured layer thickness, fibre orientation/layup, heater dimensions/position, exposed area, supports and contact area. Material: directional K, density, cp, temperature dependence, dry/cured porosity, epoxy uptake, filler dimensions/grade and distribution. Interfaces: adhesive thickness/properties or R''c. Optical: actual cured-surface R(λ), transmission if relevant, long-wave emissivity and surface state. Environment: ambient/surrounding temperature, airflow or h, irradiance map/spectrum, heater electrical input, heat split and timing.

Microstructure inputs: SEM/micro-CT orientation, channel/wall distributions, shrinkage, density and residual voids. Mechanics extension: orthotropic stiffness, expansion, interface/failure properties and suitable test geometry. No validated table of these values is included. Null inputs are intentional; hypothetical values must be labelled as such and kept separate from calibration data.

## I. Outputs

- kx, ky, kz or full K, local axes, anisotropy ratio and extraction boundary conditions.
- T(x,y,z,t), heat flux, centreline profiles, source/upper/back temperatures, temperature uniformity, heating/cooling curves and time to steady state.
- R'' for material/stack versus Rsys for the heated assembly. Rsys = (Th−Ta)/P is meaningful as the guide's dark-state comparative metric; solar input adds energy in illuminated cases.
- Added areal mass, actual thickness and construction; comparisons P, C*, B*, C*+B* under identical load/environment assumptions.
- Parameter provenance, run identifier, solver/version, mesh, time step, model equations/assumptions, warnings, convergence and residual energy balance.

Keep different replicates and uncertainty separate. Export machine-readable input/output plus human-readable plots/report. Do not fabricate experiments to populate an attractive dashboard.

## J. Verification and validation milestones

1. Reproduce homogeneous slab and two-layer/contact analytic solutions with correct flux sign and units.
2. Show zero gradient for an equilibrated no-load problem and rotate an anisotropic case to demonstrate axis handling.
3. Demonstrate mesh refinement, RVE-size sensitivity and time-step refinement for reported outputs. Set and disclose tolerances before judging convergence.
4. Check transient energy accumulation plus net boundary losses against inputs; for steady state, inputs must balance outputs within the reported numerical error.
5. Compare dry-network results only to comparable dry-network literature conditions. Compare resin-filled region and laminate separately to measurements or relevant infused-composite data.
6. Validate baseline panel before modified panels, preserving identical fixture/environment conditions. Compare transient histories and fields as well as one final temperature.
7. Perform sensitivity/identifiability checks on h, R''c, K and emissivity; one temperature curve may not uniquely determine them all.

Older spreadsheet “targets” (low k roughly 0.017–0.052 W/mK, anisotropy 2–6, porosity 95–99%, channel sizes 20–200 µm) are exploration/context, not code-verification tests or universal success criteria for a cured CFRP laminate. The baseline contains BN fraction 25% and BN:C = 1:1 without a shared basis; do not apply both without resolving it.

## K. Practical order of work

First implement and verify the simplest thermal core and data/provenance schema. Then build an explicit dry-network model and homogenisation, followed by infused-network and whole-panel cases. Keep optical reflectance as measured input initially; add a separately validated optical model when the intended question requires it. Carry mechanical integrity alongside thermal trade-offs through experiments or a supported mechanics extension. Add process-to-structure prediction only after calibration. Record assumptions and unresolved conflicts as part of every model version.
