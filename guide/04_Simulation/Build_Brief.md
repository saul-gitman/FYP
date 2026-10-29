# Build brief — aerogel simulation tool

Implement the requirements already extracted in `Requirements_Extracted_From_Transcript.md`. The simulator has not been built by this handover. The implementation sequence below is the editor's practical interpretation of those requirements; choices such as solver, mesh and UI framework remain implementation decisions.

## 1. Reference and physical scope

Main conceptual reference: Lou et al. (2023), DOI **10.3390/gels9030220**. Use its discussion of heat-transfer mechanisms, model families and measurement limitations to choose suitable physics. It is a review of nanoporous insulation, not a ready-made model of the exact CNF/CNT/BN/MTMS formulation. Use the supporting sources in `../05_References/START_HERE.md`, particularly Obori for a CNF network and Kim/Chan for directional geometry. Do not claim that one paper supplies all material inputs.

Maintain three separate states: **dry aerogel**, **resin-infiltrated aerogel-derived region**, and **whole CFRP laminate**. A dry-aerogel conductivity is not automatically a property of a cured interlayer. No validated project conductivity, optical spectrum, wall geometry or contact resistance is included.

## 2. First working version

1. Define a simple representative aligned porous cell or repeated-channel geometry. A homogeneous wall is sufficient initially. Explicitly define channel axis, pitch, pore diameter/width, wall dimension, cell length and boundary treatment.
2. Fix one documented wall composition. Start with a pore-size sweep while holding the declared remaining dimensions constant. Report derived porosity and density. If pitch or specimen size changes instead, state that clearly.
3. Solve steady conduction along and transverse to the alignment. Use a reproducible numerical solver rather than a decorative conductivity slider. A resistor network, finite-volume or finite-element approach is acceptable if its assumptions and convergence are demonstrated.
4. Return directional effective conductivity, temperature and heat-flux fields, porosity/density and an anisotropy ratio. Store the definition of that ratio, e.g. k_parallel/k_transverse.
5. Add composition sweeps after the initial geometry study works. Track CNF, CNT, BN and retained MTMS-derived material separately. Include supporting-network feasibility as a limit or warning, not an invented precise threshold.
6. Add the laminate and experimental load cases only after the aerogel core is verified. Use the original Word guide for that extension.

Do not invent a freezing-temperature-to-pore-size equation. The first tool maps **structure → properties**. Processing → structure needs a literature-supported or experimentally calibrated relation.

## 3. Governing equations and bookkeeping

Use SI units. For steady conduction, ∇·(K∇T) + q_vol = 0, with heat-flux vector q = −K∇T. For transients, ρc_p∂T/∂t = ∇·(K∇T) + q_vol. Introduce heat capacity only when needed and supported.

For a specimen of length L under an imposed ΔT, k_eff = QL/(AΔT), with Q the integrated heat rate in W, A the area in m² and L in m. If using heat flux q_n in W/m², k_eff = q_nL/ΔT. Document area and the sign convention. For general homogenisation use ⟨q_i⟩ = −K_ij G_j and independent loading directions. Specify whether the boundary scheme is periodic or fixed-temperature with insulated sides.

Use local alignment axes and, when needed, transform K_global = R K_local Rᵀ with an orthonormal rotation R. Alignment, global plate thickness and carbon-fibre direction are distinct. Off-diagonal terms can arise from coordinate rotation; they are not extra heat sources.

Compute porosity from the modelled solid/gas volumes. For a dry skeleton under additive-volume assumptions, ρ_solid = 1/(Σ w_i/ρ_i) and ρ_bulk ≈ (1−φ)ρ_solid. These relations need dry retained mass fractions, not slurry percentages. MTMS reaction losses, drying shrinkage and later epoxy uptake require separate treatment. A simple wall mixture model should disclose its assumptions and compare parallel/series mixture bounds; a linear mixture rule alone does not prove actual wall conductivity.

## 4. Gas, solid and radiation

Keep constituent conductivity separate from its effective contribution through a porous structure. Use Lou as the entry point, then select a specific model with its assumptions and parameter definitions from the cited research.

For a supported first approximation, gas conductivity may use a declared Knudsen correction such as k_g = k_g,free/(1 + 2βKn), Kn = λ_mfp/d_pore. β depends on the chosen convention and gas/surface accommodation; it is not a universal fitted number. Distinguish micrometre ice-templated channels from nanopores within cell walls. Use the appropriate pore length and do not automatically suppress gas conduction in every visible channel.

A component view of k_eff can include solid conduction, gas conduction and an equivalent radiative contribution. In a coupled network, these contributions need not be independent additive material constants. Do not add an extra gas–solid coupling term on top of a resolved model that already includes it.

Radiation normally follows a radiative-transfer or surface-exchange equation. An equivalent k_rad is a reduction under specified conditions, not an intrinsic conduction property. Use a Rosseland-type approximation only when its optical-thickness and local-equilibrium assumptions are supported; otherwise leave it disabled or use a separately justified radiation model. Avoid double counting internal radiative transfer and external surface radiation. Neglect pore convection initially only with an explicit scale/flow justification.

## 5. Later laminate extension

Outside to inside: BN-rich surface, upper CFRP, CNT-containing interlayer, lower CFRP; heater at the back. Use measured thickness, actual layer count and material orientation. A finite interface resistance gives ΔT = q_n R″_c. Represent an adhesive explicitly or through an interface resistance, without counting it twice.

Guide cases: dark heating at 2 W (optional 5 W), solar-only at 1000 W/m², and 2 W plus 1000 W/m². The guide specifies a 20 × 20 mm heater. Confirm actual tested/illuminated area, supports, heat split and contact before matching temperatures.

For an opaque surface α_solar = 1−R_solar; with transmission, α_solar = 1−R_solar−τ_solar. Solar absorption is α_solarG. Thermal emission requires separate long-wave emissivity and absolute temperature, e.g. εσ(T_s⁴−T_sur⁴). Reflectance is not emissivity. Use measured reflectance as input first rather than promising to calculate spectra from pore size alone.

Compare plain CFRP, carbon-only, BN-only and combined variants under common conditions. Report source temperature, directional conductivity, temperature fields and thermal resistance. Distinguish R″ = L/k [m² K/W] from dark-state system resistance (T_heater−T_ambient)/P [K/W]. Anisotropy does not establish a passive one-way thermal diode.

## 6. Verification and deliverables

- Verify homogeneous-slab and series-layer/contact solutions, units and flux direction.
- Demonstrate mesh/network refinement and representative-cell size sensitivity; check energy balance and symmetry/positive definiteness where applicable.
- For transient extensions, demonstrate time-step convergence and energy accumulation balance.
- Compare trends under matching materials, composition basis and alignment. Investigate both numerical/model limitations and experimental structure when results differ.
- Label every input as measured, literature-derived, derived or hypothetical. Keep unknowns unresolved rather than silently filling them with attractive values.
- Export machine-readable run inputs/results plus readable plots and a model/assumptions report. Include reproducible run instructions. A UI may help inspection but does not replace numerical verification.

Mechanics and spectral optical modelling are later extensions. Earlier HTML files in `../06_Previous_Work/` are retained illustrations, not validated solvers. Superseded build instructions are in `../09_Archive/`.
