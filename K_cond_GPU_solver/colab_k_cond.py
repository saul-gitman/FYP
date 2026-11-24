"""Thermal conductivity of a freeze-cast aerogel layer by conduction, in two steps.

  1. WALL       A periodic 3-D voxel patch of one cell wall: BN sheets (B10 recipe) or CNT rods
                (C2.5 recipe) glued by CNF and PMSQ, with optional pores (air or epoxy).
                Gives the wall conductivity along the wall (what the honeycomb needs) and
                through it, with a low / likely / high band from several random walls.
  2. HONEYCOMB  A periodic 2-D pixel picture of the hexagonal channels at true wall thickness,
                cells filled with air or epoxy. Gives the layer conductivity along the channels,
                across them, and through the plate thickness for a given channel tilt.

Heat paths: conduction only (solid + whatever fills the pores and cells). Radiation and
convection are handled elsewhere and are not added here.

How to run
  Google Colab: Runtime > Change runtime type > GPU (H100 or A100). Paste this whole file into
  one cell and run it. CuPy comes with Colab GPU runtimes; without it the script uses NumPy.
  Elsewhere: python colab_k_cond.py   (NumPy needed; pandas and CuPy optional)

Modes (RUN OPTIONS block)
  "quick"  small grids and 2 random walls; for a CPU (under a minute on 2 cores). The quick wall
           grid does not resolve the sheets, so its tables say "QUICK, NOT CONVERGED".
  "full"   5 nm voxels, 8 random walls, 8 px across the honeycomb wall, sensitivity study.
           Meant for the GPU.
  "auto"   full on a GPU, quick otherwise.

Edit only the WALL and HONEYCOMB input blocks (and RUN OPTIONS if needed).
Units: wall values in W/m·K, layer values in mW/m·K. After the run, RESULTS holds every number.
Each input comment reads: unit | status | source or reason.
"""

# ============================== WALL ==============================
# ------------------------ all input variables ---------------------
# Recipe (grams per 50 g batch; the water leaves, only the solids build the walls)
FILLER = "BN"                # "BN" (B10, platelets) or "CNT" (C2.5, rods) | choice | experiment guide
M_FILLER_G = 5.00            # g | measured recipe | report Table 2: B10 = 5.00 g BN (10 wt%); C2.5 = 1.25 g dry CNT (9.62 g of 13 wt% dispersion)
M_CNF_DRY_G = 0.50           # g | measured recipe | report Table 2: 12.50 g CNF stock = 0.50 g dry (1 wt%)
M_MTMS_FEED_G = 1.00         # g | measured recipe | report Table 2: MTMS feed (2 wt%)
MTMS_TO_PMSQ_YIELD = 0.493   # g PMSQ per g MTMS | hypothetical | full condensation CH3Si(OCH3)3 (136.22 g/mol) -> CH3SiO1.5 (67.12 g/mol); retention not given in the guide
# Densities
RHO_BN = 2.1                 # g/cm³ | literature | h-BN 2.1–2.28
RHO_CNT = 1.8                # g/cm³ | hypothetical | multiwall CNT ~1.6–2.0
RHO_CNF = 1.5                # g/cm³ | literature | cellulose 1.5–1.6
RHO_PMSQ = 1.25              # g/cm³ | hypothetical | placeholder, no value found for MTMS-derived solid
RHO_EPOXY = 1.15             # g/cm³ | hypothetical | typical cured epoxy; check the resin datasheet
# Pores inside the wall. Range 0–0.40. About 0.41 would follow if Chan 2022's derived wall density
# (1.12 g/cm³ vs ~1.89 for a dense wall) is taken at face value.
WALL_POROSITY = 0.0          # volume fraction | hypothetical | see the line above
WALL_PORE_FILL = "air"       # "air" or "epoxy" (resin got into the wall pores at infusion) | choice | process
WALL_PORE_SIZE_NM = 50       # nm | hypothetical | used only for the Knudsen-reduced air in wall pores
# Microstructure
WALL_THICKNESS_UM = 0.27     # µm | derived | gives porosity 0.982 at 30 µm pores (Chan et al. 2022); ALSO the honeycomb wall t
SHEET_DIAMETER_UM = 1.0      # µm | hypothetical | BN grade datasheet / TEM to replace
SHEET_THICKNESS_NM = 30      # nm | hypothetical | BN grade datasheet / TEM to replace
SHEET_TILT_STD_DEG = 10      # deg | hypothetical | tilt from the wall plane = |Normal(0, std)|, azimuth uniform; ice front pushes sheets flat; SEM to replace
ROD_DIAMETER_NM = 15         # nm | hypothetical | CNT only
ROD_LENGTH_UM = 1.0          # µm | hypothetical | CNT only; rods lie in the wall plane (random direction), tilted out of it like the sheets
# Conductivities. BN in-plane: ~325 measured for natural-isotope bulk h-BN (pure 10B, 585, is
# ~80 % higher; Yuan et al. 2019 Commun. Phys.); ~550 predicted; defective sheets lower. Range 100–550.
K_BN_INPLANE = 300           # W/m·K | literature | see the line above
K_BN_THROUGH = 3             # W/m·K | literature | 2–5 (Jaffe et al. 2021; Jiang et al. 2018)
K_CNT_AXIAL = 100            # W/m·K | hypothetical | very uncertain for real multiwall CNT in networks; range 10–1000
K_CNT_RADIAL = 2             # W/m·K | hypothetical | across the tube
K_CNF = 1.3                  # W/m·K | literature | CNF film in-plane ~1.34 (Xu et al., OSTI 1892395); CNC intrinsic ~2.0 (Li et al. 2021); range 0.5–2.0
K_PMSQ = 0.2                 # W/m·K | hypothetical | no bulk value found; polymer-like 0.1–0.3
K_EPOXY = 0.2                # W/m·K | hypothetical | typical cured epoxy ~0.2; check the resin datasheet (used in wall pores and cells)
# (air in the wall pores: Incropera table + Knudsen with gap = WALL_PORE_SIZE_NM, at T_K and
#  PRESSURE_PA set in the HONEYCOMB block)
# Interfaces. Filler-binder: ~1e-8 typical for BN/polymer; 0.6e-8 reported as exceptionally low
# (Mater. Horiz. 2025); MD exists for h-BN/cellulose (Li et al. 2021, IJHMT 171:121043). Applies on
# faces between a filler voxel and a non-filler SOLID voxel (CNF, PMSQ or epoxy). No resistance on
# faces touching air pores, inside one sheet, or between binder voxels.
R_FILLER_BINDER = 1e-8       # m²K/W | literature (order) | see the lines above
R_FILLER_FILLER = 1e-8       # m²K/W | hypothetical | contact between two DIFFERENT sheets/rods; likely controls k at high loading; swept
# Grid (periodic box: PATCH × PATCH in the wall plane, wall thickness through it)
VOXEL_NM_FULL = 5            # nm | numerical | full (GPU) mode voxel edge
PATCH_UM_FULL = 2.5          # µm | numerical | full mode in-plane box edge
VOXEL_NM_QUICK = 20          # nm | numerical | quick (CPU) mode voxel edge; does not resolve 30 nm sheets
PATCH_UM_QUICK = 1.6         # µm | numerical | quick mode box edge (> sheet diameter / 0.8, so sheets do not overlap themselves)
# ------------------------------------------------------------------

# ============================ HONEYCOMB ===========================
# ------------------------ all input variables ---------------------
PORE_SIZE_UM = 30            # µm, inner flat-to-flat width d | literature | Chan et al. 2022
# wall thickness t: WALL_THICKNESS_UM in the WALL block (one value for both steps)
K_WALL_SOURCE = "wall"       # "wall" (the wall step's along-wall value) or a number in W/m·K | choice | e.g. 4.0 = derived (back-calculated) from Chan 2022, BNNS/WPU
CELL_FILL = "air"            # "air" (dry; Knudsen with gap = d) or "epoxy" (infused; K_EPOXY) | choice | process
T_K = 300                    # K | chosen test condition | room temperature; used by both steps
PRESSURE_PA = 101325         # Pa | chosen test condition | 1 atm; used by both steps
CHANNEL_TILT_DEG = 0         # deg | hypothetical until SEM of the edge offcuts | angle channels-to-plate-normal: 0 = through the thickness (cold base below, likely here), 90 = in-plane (as in Chan 2022)
RHO_WALL = None              # g/cm³ or None | derived | None = dense wall density from the WALL composition × (1 − WALL_POROSITY), plus epoxy in wall pores
# Pixel picture
WALL_PIXELS_FULL = 8         # pixels across the wall thickness, full mode | numerical
WALL_PIXELS_QUICK = 4        # pixels across the wall thickness, quick mode | numerical (4, so that the 1/2 resolution study still has 2 px)
SUPERSAMPLE = 4              # sub-samples per pixel edge (stratified random) for the wall area fraction around each pixel face | numerical
RES_STUDY = True             # also solve at 1/2 and 1/4 of the resolution (where >= 2 px across the wall)
# ------------------------------------------------------------------

# ============================ RUN OPTIONS =========================
MODE = "auto"                # "auto" (full on GPU, quick on CPU), "quick" or "full"
N_SEEDS_FULL = 8             # random walls per run, full mode
N_SEEDS_QUICK = 2            # random walls per run, quick mode
SEED0 = 0                    # first random seed (seeds SEED0, SEED0+1, ...)
RUN_CHECKS = True            # built-in verification table
RUN_SENSITIVITY = "auto"     # True, False or "auto" (= True on a GPU): one-at-a-time wall sensitivity
N_SEEDS_SENS = 2             # random walls per sensitivity point (same seeds for every point)
CG_TOL = 1e-8                # stop when |residual| / |right-hand side| < CG_TOL
CG_MAXITER = 20000           # hard stop for the conjugate-gradient solver
PRECONDITIONER = "fft"       # "fft" (periodic Laplacian of a uniform reference medium, solved by FFT) or "jacobi"
BENCH_WALL_PIXELS_QUICK = 10  # pixels across the wall in the finite-element benchmark (check 4), quick mode
BENCH_WALL_PIXELS_FULL = 40   # same, full mode
# ------------------------------------------------------------------

# ======================= ENGINE (no need to edit) =================
import math
import time

import numpy as np

try:
    import cupy as cp
    GPU = cp.cuda.runtime.getDeviceCount() > 0
except Exception:  # no CuPy, or no CUDA device
    cp, GPU = None, False
xp = cp if GPU else np  # the same solver code runs on both

try:
    import pandas as pd
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.width", 250)
except Exception:
    pd = None
try:
    from IPython import get_ipython
    from IPython.display import display
    IN_NOTEBOOK = get_ipython() is not None
except Exception:
    IN_NOTEBOOK = False

S3 = math.sqrt(3.0)
RUN_MODE = ("full" if GPU else "quick") if MODE == "auto" else MODE
FULL = RUN_MODE == "full"
SOLVES = []   # every solve, for check 6
CHECKS = []   # rows of the checks table
RESULTS = {}  # every number, for use after the run


def to_host(a):
    return cp.asnumpy(a) if GPU and isinstance(a, cp.ndarray) else np.asarray(a)


def free_gpu():
    if GPU:
        cp.get_default_memory_pool().free_all_blocks()


def g4(x, sig=4):
    """Compact number for tables."""
    if x is None or isinstance(x, str):
        return "—" if x is None else x
    x = float(x)
    if math.isnan(x):
        return "—"
    if x == 0 or 1e-3 <= abs(x) < 1e5:
        return f"{x:.{sig}g}"
    return f"{x:.2e}"


def show(title, columns, rows, note=None):
    """Table: pandas display() in a notebook, plain text otherwise."""
    print("\n" + title)
    rows = [[g4(v) if not isinstance(v, str) else v for v in r] for r in rows]
    if pd is not None:
        df = pd.DataFrame(rows, columns=columns)
        if IN_NOTEBOOK:
            display(df)
        else:
            print(df.to_string(index=False))
    else:
        w = [max([len(str(c))] + [len(str(r[i])) for r in rows]) for i, c in enumerate(columns)]
        print("  ".join(str(c).ljust(n) for c, n in zip(columns, w)))
        for r in rows:
            print("  ".join(str(v).ljust(n) for v, n in zip(r, w)))
    if note:
        print(note)


# ---------- air (copied from aerosim/core/constants.py; sources as there) ----------
K_BOLTZMANN = 1.380649e-23  # J/K, exact (SI 2019)
AIR_T = np.array([250.0, 300.0, 350.0, 400.0])  # K, Incropera Table A.4 (1 atm)
AIR_K = np.array([22.3e-3, 26.3e-3, 30.0e-3, 33.8e-3])  # W/m·K, Incropera Table A.4
AIR_PR = 0.71  # Prandtl number near 300 K (Table A.4: 0.707)
AIR_GAMMA = 1.4  # cp/cv for a diatomic gas
AIR_DIAMETER = 3.72e-10  # m, kinetic collision diameter (gives λ ≈ 66 nm at 300 K, 1 atm)


def k_air(T):
    """Free air conductivity, linear interpolation in Incropera Table A.4 (clamped to 250–400 K)."""
    return float(np.interp(T, AIR_T, AIR_K))


def mean_free_path(T, p):
    """λ = k_B T / (√2 π d_g² p), kinetic theory."""
    return K_BOLTZMANN * T / (math.sqrt(2) * math.pi * AIR_DIAMETER**2 * p)


def knudsen_beta(alpha=1.0):
    """β = ((2 − α)/α)·(2γ/(γ + 1))/Pr ≈ 1.64 for air, α = 1 (Kaganer 1969; Zeng et al. 1995)."""
    return (2 - alpha) / alpha * (2 * AIR_GAMMA / (AIR_GAMMA + 1)) / AIR_PR


def k_gas(gap, T, p):
    """Knudsen-reduced air in a gap (m): k_air / (1 + 2 β λ / gap)."""
    return k_air(T) / (1 + 2 * knudsen_beta() * mean_free_path(T, p) / gap)


# ---------- the solver (shared by the 3-D wall and the 2-D honeycomb) ----------
def face_k(kd, d, R=None, h=1.0):
    """Face conductivity (W/m·K) between every cell and its +d neighbour (periodic).

    Two half cells in series plus an interface resistance R (m²K/W):
    kf = h·g = 1 / (1/(2 k_i) + 1/(2 k_j) + R/h). With R = 0 this is the harmonic mean of
    pixel_fv.py. kf times a temperature difference between cell centres is h times the flux.
    """
    inv = 0.5 / kd + 0.5 / xp.roll(kd, -1, axis=d)
    if R is not None:
        inv += R / h
    return 1.0 / inv


def est_bytes(cells, ndim):
    """Rough memory need of one solve: face arrays + CG vectors + temporaries + FFT."""
    return cells * 8 * (ndim + 6 + 3 + 2)


class PeriodicConduction:
    """Steady conduction on a periodic grid of cubic cells (finite volume, matrix-free CG).

    The temperature is T = θ − G·x with θ periodic and a drop of 1 K per cell along the driven
    axis d. Flux across the +e face of cell i (to its neighbour j) per unit area, times h:
    kf_e (θ_i − θ_j + δ_ed). Heat balance in every cell gives A θ = b, with A symmetric positive
    semi-definite (constants are its null space) and b_i = kf_d[i − d] − kf_d[i]. Since the
    imposed gradient is 1 K per h, the effective conductivity is k_eff[e, d] = mean over all
    e-faces of kf_e (θ_i − θ_j + δ_ed). Driving each axis in turn gives the full tensor.
    """

    def __init__(self, kf, precond=PRECONDITIONER):
        self.kf, self.n, self.shape, self.precond = kf, len(kf), kf[0].shape, precond
        if precond == "fft":
            # Preconditioner: the same periodic grid filled with a uniform reference medium,
            # one conductivity per axis (geometric mean of the parallel and series face values,
            # close to the effective one). Its matrix is diagonal in Fourier space, so it is
            # inverted exactly by two FFTs. CG converges in a number of iterations that depends
            # on the contrast, not on the grid size (Jacobi grows with the grid size).
            kref = [math.sqrt(float(g.mean()) / float((1.0 / g).mean())) for g in kf]
            lam = 0.0
            for d, N in enumerate(self.shape):
                m = xp.arange(N // 2 + 1 if d == self.n - 1 else N, dtype=xp.float64)
                shp = [1] * self.n
                shp[d] = m.size
                lam = lam + (4.0 * kref[d] * xp.sin(xp.pi * m / N) ** 2).reshape(shp)
            lam[(0,) * self.n] = xp.inf  # the constant mode is the null space: send it to zero
            self.inv_lam = 1.0 / lam
        else:
            diag = sum(g + xp.roll(g, 1, axis=d) for d, g in enumerate(kf))
            self.inv_diag = 1.0 / diag

    def M(self, r):
        """Apply the preconditioner. The result is mean-free, so the iterate stays mean-free."""
        if self.precond == "fft":
            ax = tuple(range(self.n))
            return xp.fft.irfftn(xp.fft.rfftn(r, axes=ax) * self.inv_lam, s=self.shape, axes=ax)
        z = r * self.inv_diag
        return z - z.mean()

    def A(self, v):
        """Net heat leaving every cell for a periodic field v (matrix-free, rolls = neighbours)."""
        out = xp.zeros_like(v)
        for d, g in enumerate(self.kf):
            f = g * (v - xp.roll(v, -1, axis=d))  # flux out through each cell's +d face
            out += f
            out -= xp.roll(f, 1, axis=d)  # the same flux enters the +d neighbour
        return out

    def solve(self, d, tol=CG_TOL, maxiter=CG_MAXITER):
        """Preconditioned CG for the drive along axis d. Returns θ (mean zero) and solver info."""
        t0 = time.time()
        g = self.kf[d]
        b = xp.roll(g, 1, axis=d) - g
        bnorm = float(xp.sqrt(xp.vdot(b, b)))
        x = xp.zeros(self.shape)
        it, res = 0, 0.0
        if bnorm > 0:  # b = 0 (e.g. a uniform grid): θ = 0 is exact
            r = b
            z = self.M(r)
            p = z.copy()
            rz = float(xp.vdot(r, z))
            for it in range(1, maxiter + 1):
                Ap = self.A(p)
                alpha = rz / float(xp.vdot(p, Ap))
                x += alpha * p
                r -= alpha * Ap
                res = float(xp.sqrt(xp.vdot(r, r))) / bnorm
                if res < tol:
                    break
                z = self.M(r)
                rz, rz_old = float(xp.vdot(r, z)), rz
                p *= rz / rz_old
                p += z
            x -= x.mean()
        return x, {"iters": it, "res": res, "converged": res < tol, "time": time.time() - t0}

    def tensor(self, axes, label, tol=CG_TOL, maxiter=CG_MAXITER, verbose=True):
        """Drive each axis in `axes`; returns K (n × n, NaN where not driven) and solver infos."""
        K = np.full((self.n, self.n), np.nan)
        infos = []
        for d in axes:
            theta, info = self.solve(d, tol, maxiter)
            for e in range(self.n):
                q = self.kf[e] * (theta - xp.roll(theta, -1, axis=e) + (1.0 if e == d else 0.0))
                K[e, d] = float(q.mean())
                if e == d:  # energy check: the same heat must cross every plane normal to d
                    planes = to_host(q.sum(axis=tuple(a for a in range(self.n) if a != d)))
                    info["energy"] = float((planes.max() - planes.min()) / abs(planes.mean()))
            info["label"], info["axis"] = f"{label}, drive {'xyz'[d]}", d
            if not info["converged"]:
                print(f"  !!! WARNING: CG NOT CONVERGED ({info['label']}): residual {info['res']:.2e} "
                      f"after {info['iters']} iterations. Raise CG_MAXITER or check the inputs.")
            if verbose:
                print(f"    {info['label']}: {info['iters']} it, residual {info['res']:.1e}, "
                      f"energy {info['energy']:.1e}, {info['time']:.2f} s")
            SOLVES.append(info)
            infos.append(info)
            del theta
        return K, infos


# ---------- step 1: wall ----------
WALL_NAMES = [
    "FILLER", "M_FILLER_G", "M_CNF_DRY_G", "M_MTMS_FEED_G", "MTMS_TO_PMSQ_YIELD", "RHO_BN", "RHO_CNT",
    "RHO_CNF", "RHO_PMSQ", "RHO_EPOXY", "WALL_POROSITY", "WALL_PORE_FILL", "WALL_PORE_SIZE_NM",
    "WALL_THICKNESS_UM", "SHEET_DIAMETER_UM", "SHEET_THICKNESS_NM", "SHEET_TILT_STD_DEG",
    "ROD_DIAMETER_NM", "ROD_LENGTH_UM", "K_BN_INPLANE", "K_BN_THROUGH", "K_CNT_AXIAL", "K_CNT_RADIAL",
    "K_CNF", "K_PMSQ", "K_EPOXY", "R_FILLER_BINDER", "R_FILLER_FILLER",
]


def wall_inputs():
    P = {n: globals()[n] for n in WALL_NAMES}
    P["FILLER"] = str(P["FILLER"]).upper()
    P["VOXEL_NM"] = VOXEL_NM_FULL if FULL else VOXEL_NM_QUICK
    P["PATCH_UM"] = PATCH_UM_FULL if FULL else PATCH_UM_QUICK
    return P


def wall_composition(P):
    """Recipe grams -> mass and volume fractions of the dense wall, then with wall porosity."""
    rho_f = P["RHO_BN"] if P["FILLER"] == "BN" else P["RHO_CNT"]
    mass = {"filler": P["M_FILLER_G"], "CNF": P["M_CNF_DRY_G"],
            "PMSQ": P["M_MTMS_FEED_G"] * P["MTMS_TO_PMSQ_YIELD"]}
    rho = {"filler": rho_f, "CNF": P["RHO_CNF"], "PMSQ": P["RHO_PMSQ"]}
    m_tot = sum(mass.values())
    vol = {k: mass[k] / rho[k] for k in mass}
    v_tot = sum(vol.values())
    por = P["WALL_POROSITY"]
    c = {"mass_g": mass, "wt": {k: mass[k] / m_tot for k in mass},
         "v_dense": {k: vol[k] / v_tot for k in vol}, "rho_dense": m_tot / v_tot}
    c["v"] = {k: (1 - por) * c["v_dense"][k] for k in vol}
    c["v"]["pore"] = por
    c["rho_wall"] = (1 - por) * c["rho_dense"] + (por * P["RHO_EPOXY"] if P["WALL_PORE_FILL"] == "epoxy" else 0.0)
    return c


def wall_grid(P):
    h = P["VOXEL_NM"] * 1e-9
    n_in = max(1, round(P["PATCH_UM"] * 1e-6 / h))
    nz = max(1, round(P["WALL_THICKNESS_UM"] * 1e-6 / h))
    rods = P["FILLER"] == "CNT"
    small = (P["ROD_DIAMETER_NM"] if rods else P["SHEET_THICKNESS_NM"]) * 1e-9
    big = (P["ROD_LENGTH_UM"] if rods else P["SHEET_DIAMETER_UM"]) * 1e-6
    return {"h": h, "shape": (n_in, n_in, nz), "under_resolved": small < 2 * h,
            "self_overlap": big > 0.8 * n_in * h, "small_vox": small / h}


def build_wall(P, seed):
    """One random periodic wall patch -> per-voxel conductivities, phases and sheet ids.

    Phases: 0 air pore, 1 CNF, 2 PMSQ, 3 filler, 4 epoxy in a pore. Sheets (discs) or rods
    (cylinders) get uniform random centres; overlaps are allowed and the later object overwrites
    (new id). Objects are added until the filler voxel fraction reaches the target (the first
    object that reaches or passes it is the last). Each object is evaluated on its own bounding
    box with periodic wrap; an object longer than the box in some direction (a steep sheet in a
    thin wall) is cut to one period there, so it never overlaps itself.
    Remaining voxels: "randomly mixed binder" assumption: each one is CNF, PMSQ or pore at random,
    in proportion to their target volume fractions within the remaining volume.
    Filler voxel conductivity along axis d: the diagonal of the rotated tensor (off-diagonal
    terms dropped): sheets k_d = K_IN (1 − n_d²) + K_THROUGH n_d² (n = sheet normal); rods
    k_d = K_AXIAL a_d² + K_RADIAL (1 − a_d²) (a = rod axis). Other phases are isotropic.
    """
    comp = wall_composition(P)
    G = wall_grid(P)
    h, shape = G["h"], G["shape"]
    box = [n * h for n in shape]
    rng = np.random.default_rng(seed)
    rods = P["FILLER"] == "CNT"
    D = (P["ROD_LENGTH_UM"] if rods else P["SHEET_DIAMETER_UM"]) * 1e-6  # length / diameter
    w = (P["ROD_DIAMETER_NM"] if rods else P["SHEET_THICKNESS_NM"]) * 1e-9  # diameter / thickness
    k_hi, k_lo = (P["K_CNT_AXIAL"], P["K_CNT_RADIAL"]) if rods else (P["K_BN_INPLANE"], P["K_BN_THROUGH"])
    std = math.radians(P["SHEET_TILT_STD_DEG"])
    total = shape[0] * shape[1] * shape[2]
    target = comp["v"]["filler"] * total
    obj_vox = math.pi / 4 * (w * w * D if rods else D * D * w) / h**3
    max_objects = int(200 * target / max(obj_vox, 1e-9)) + 1000
    sid = xp.full(shape, -1, dtype=xp.int32)
    kv = [xp.zeros(shape) for _ in range(3)]
    n_fill, count, cut = 0, 0, 0
    while n_fill < target and count < max_objects:
        c = rng.random(3) * np.array(box)
        tilt, az = abs(rng.normal(0.0, std)), rng.uniform(0.0, 2 * math.pi)
        if rods:  # axis in the wall plane, tilted out of it
            u = np.array([math.cos(tilt) * math.cos(az), math.cos(tilt) * math.sin(az), math.sin(tilt)])
            half = 0.5 * D * np.abs(u) + 0.5 * w * np.sqrt(1 - u * u)
            kdir = k_hi * u * u + k_lo * (1 - u * u)
        else:  # normal tilted from z
            u = np.array([math.sin(tilt) * math.cos(az), math.sin(tilt) * math.sin(az), math.cos(tilt)])
            half = 0.5 * D * np.sqrt(np.clip(1 - u * u, 0, 1)) + 0.5 * w * np.abs(u)
            kdir = k_hi * (1 - u * u) + k_lo * u * u
        idx, disp = [], []
        for a in range(3):
            N, L = shape[a], box[a]
            i = np.arange(math.floor((c[a] - half[a]) / h - 0.5), math.ceil((c[a] + half[a]) / h - 0.5) + 1)
            if i.size >= N:
                i = np.arange(N)
                cut += a == 2 and 2 * half[2] > L
            x = (i + 0.5) * h - c[a]
            x -= L * np.round(x / L)  # nearest periodic image of the centre
            idx.append(xp.asarray(i % N))
            disp.append(xp.asarray(x))
        X, Y, Z = disp[0][:, None, None], disp[1][None, :, None], disp[2][None, None, :]
        s = X * u[0] + Y * u[1] + Z * u[2]  # along the rod axis / along the sheet normal
        r2 = X * X + Y * Y + Z * Z - s * s  # squared distance from the axis / normal line
        if rods:
            m = (xp.abs(s) <= D / 2) & (r2 <= (w / 2) ** 2)
        else:
            m = (xp.abs(s) <= w / 2) & (r2 <= (D / 2) ** 2)
        li, lj, lk = xp.nonzero(m)
        gi = (idx[0][li], idx[1][lj], idx[2][lk])
        n_fill += int((sid[gi] < 0).sum())
        sid[gi] = count
        for d in range(3):
            kv[d][gi] = kdir[d]
        count += 1
    if n_fill < target:
        print(f"  !!! WARNING: stopped at {count} objects before reaching the filler fraction")
    # binder and pores in the rest, voxel by voxel at random
    v = comp["v"]
    rest_tot = v["CNF"] + v["PMSQ"] + v["pore"]
    pore_phase = 4 if P["WALL_PORE_FILL"] == "epoxy" else 0
    rnd = xp.asarray(rng.random(shape, dtype=np.float32))
    if rest_tot > 0:
        c1, c2 = v["CNF"] / rest_tot, (v["CNF"] + v["PMSQ"]) / rest_tot
        binder = xp.where(rnd < c1, 1, xp.where(rnd < c2, 2, pore_phase)).astype(xp.uint8)
    else:  # recipe without binder or pores: leftover voxels (if any) become CNF; warned below
        binder = xp.full(shape, 1, dtype=xp.uint8)
        print("  !!! WARNING: no binder and no pores in the recipe; leftover voxels set to CNF")
    del rnd
    filler = sid >= 0
    phase = xp.where(filler, 3, binder).astype(xp.uint8)
    del binder
    k_pore = k_gas(P["WALL_PORE_SIZE_NM"] * 1e-9, T_K, PRESSURE_PA)
    k_iso = xp.where(phase == 1, P["K_CNF"], xp.where(phase == 2, P["K_PMSQ"],
                     xp.where(phase == 4, P["K_EPOXY"], k_pore)))
    for d in range(3):
        kv[d] = xp.where(filler, kv[d], k_iso)
    del k_iso
    fractions = {name: float((phase == ph).sum()) / total for name, ph in
                 (("filler", 3), ("CNF", 1), ("PMSQ", 2), ("pore", pore_phase))}
    return {"kv": kv, "phase": phase, "sid": sid, "objects": count, "cut": cut,
            "fractions": fractions, "h": h, "shape": shape}


def wall_face_k(W, P):
    """Face conductivities with interface resistances: filler-binder R_FB (binder = CNF, PMSQ or
    epoxy), filler-filler R_FF between different object ids, nothing else."""
    phase, sid, h = W["phase"], W["sid"], W["h"]
    filler = phase == 3
    solid_binder = (phase == 1) | (phase == 2) | (phase == 4)
    kf = []
    for d in range(3):
        fj, bj = xp.roll(filler, -1, axis=d), xp.roll(solid_binder, -1, axis=d)
        R = xp.where(filler & fj & (sid != xp.roll(sid, -1, axis=d)), P["R_FILLER_FILLER"], 0.0)
        R += xp.where((filler & bj) | (solid_binder & fj), P["R_FILLER_BINDER"], 0.0)
        kf.append(face_k(W["kv"][d], d, R, h))
        del R, fj, bj
    return kf


def run_wall(P, seed, axes=(0, 1, 2), label="wall", verbose=True):
    """Build one random wall, solve the driven axes, return the tensor, bounds and diagnostics."""
    t0 = time.time()
    W = build_wall(P, seed)
    t_build = time.time() - t0
    par = [float(W["kv"][d].mean()) for d in range(3)]  # perfect contacts, arithmetic mean
    ser = [1.0 / float((1.0 / W["kv"][d]).mean()) for d in range(3)]  # perfect contacts, harmonic
    kf = wall_face_k(W, P)
    del W["kv"], W["phase"], W["sid"]
    free_gpu()
    ser_R = [1.0 / float((1.0 / g).mean()) for g in kf]  # with contacts: a strict lower bound
    solver = PeriodicConduction(kf)
    K, infos = solver.tensor(axes, f"{label} seed {seed}", verbose=verbose)
    del solver, kf
    free_gpu()
    out = {"K": K, "par": par, "ser": ser, "ser_R": ser_R, "infos": infos, "objects": W["objects"],
           "cut": W["cut"], "fractions": W["fractions"], "time": time.time() - t0, "t_build": t_build}
    for d in axes:  # bounds of the discrete problem: series with contacts <= k_dd <= parallel
        ok = ser_R[d] * (1 - 1e-6) <= K[d, d] <= par[d] * (1 + 1e-6)
        infos[list(axes).index(d)]["bounds_ok"] = ok
    return out


def along(K):
    return 0.5 * (K[0, 0] + K[1, 1])


def max_offdiag(K):
    n = K.shape[0]
    vals = [abs(K[i, j]) / math.sqrt(abs(K[i, i] * K[j, j])) for i in range(n) for j in range(n)
            if i != j and not (math.isnan(K[i, j]) or math.isnan(K[i, i]) or math.isnan(K[j, j]))]
    return max(vals) if vals else float("nan")


# ---------- step 2: honeycomb ----------
def honeycomb_dims(d, t):
    l = d / S3  # inner side of a flat-top hexagon with flat-to-flat width d
    return l, 3 * l + S3 * t, S3 * l + t  # side, unit cell width L (x), height H (y)


def honeycomb_grid(d, t, wall_px):
    """Square pixels of size L/nx; ny chosen so that ny·px matches H. Among nx within ±3 % of the
    requested resolution, take the one with the smallest mismatch. The picture is then the true
    geometry sampled with a y step of H/ny, i.e. stretched in y by the reported tiny amount."""
    l, L, H = honeycomb_dims(d, t)
    nx0 = L / (t / wall_px)
    best = None
    for nx in range(max(4, int(nx0 * 0.97)), int(nx0 * 1.03) + 2):
        ny = max(2, round(nx * H / L))
        key = (abs(ny * L / nx / H - 1), abs(nx - nx0))
        if best is None or key < best[0]:
            best = (key, nx, ny)
    _, nx, ny = best
    px = L / nx
    return {"nx": nx, "ny": ny, "px": px, "stretch_y": ny * px / H - 1, "wall_px": t / px,
            "l": l, "L": L, "H": H}


def honeycomb_picture(d, t, wall_px, S=SUPERSAMPLE, seed=12345):
    """Wall area fractions on the faces of the pixel grid (array axis 0 = x along L, 1 = y).

    Two flat-top hexagonal cells per periodic L × H unit, centred at (0, 0) and (L/2, H/2).
    A point is inside a cell iff |dy| <= (√3/2) l and √3|dx| + |dy| <= √3 l, with (dx, dy) the
    nearest-image offset to the cell centre. Everything else is wall (thickness t everywhere).
    s[0][i, j]: wall area fraction of the pixel-sized square centred on the face between pixel
    (i, j) and (i + 1, j); s[1] the same for the face towards (i, j + 1). Each fraction uses S × S
    stratified random sub-samples (one random point in each sub-square), so that wall edges
    parallel to the grid are not snapped to fixed sub-sample rows (a regular sub-sample grid
    moved k_xx by up to ±2 % on the benchmark, depending on where the edges fell).
    """
    Gd = honeycomb_grid(d, t, wall_px)
    nx, ny, l, L, H = Gd["nx"], Gd["ny"], Gd["l"], Gd["L"], Gd["H"]
    sx, sy = L / nx, H / ny
    rng = np.random.default_rng(seed)
    Gd["s"] = []
    for ox, oy in ((1.0, 0.5), (0.5, 1.0)):  # x-face centres, y-face centres (in pixels)
        x0, y0 = (xp.arange(nx) + ox) * sx, (xp.arange(ny) + oy) * sy
        s = xp.zeros((nx, ny))
        for a in range(S):
            for b in range(S):
                X = x0[:, None] + ((a + xp.asarray(rng.random((nx, ny)))) / S - 0.5) * sx
                Y = y0[None, :] + ((b + xp.asarray(rng.random((nx, ny)))) / S - 0.5) * sy
                inside = xp.zeros((nx, ny), dtype=bool)
                for cx, cy in ((0.0, 0.0), (L / 2, H / 2)):
                    dx, dy = X - cx, Y - cy
                    dx = xp.abs(dx - L * xp.round(dx / L))
                    dy = xp.abs(dy - H * xp.round(dy / H))
                    inside |= (dy <= S3 / 2 * l) & (S3 * dx + dy <= S3 * l)
                s += (~inside).astype(xp.float64)
                del X, Y, inside
        Gd["s"].append(s / (S * S))
    Gd["phi_counted"] = 1.0 - 0.5 * float(Gd["s"][0].mean() + Gd["s"][1].mean())
    return Gd


def closed_form(side, t, kw, kh):
    """k_eff along x (along L) and y from the slice (isothermal-slice) model: an upper bound.
    Copied from aerosim_html/.agent/checks/slice_model_check.py (docs/FUTURE_WORK.md §A.2)."""
    D1, D2 = kw * t + S3 * kh * side, (4 * kw - 3 * kh) * t + S3 * kh * side
    E1 = 3 * S3 * kw * t + (3 * kw + 6 * kh) * side
    E2 = S3 * (4 * kw - kh) * t + (3 * kw + 6 * kh) * side

    def lm(a, b):  # logarithmic mean; equal arguments when k_w = k_h
        return a if np.isclose(a, b) else (b - a) / np.log(b / a)

    Rx = 2 * side / D1 + 2 * S3 * t / lm(D1, D2) + (side - S3 * t) / D2
    Ry = 6 * t / lm(E1, E2) + (3 * side - S3 * t) / ((4 * kw - kh) * t + 3 * S3 * kh * side)
    L, H = 3 * side + S3 * t, S3 * side + t
    return L / (H * Rx), H / (L * Ry)


def hashin_shtrikman_2d(kw, fw, kh, fh):
    """2-D Hashin–Shtrikman bounds for two isotropic phases (k, area fraction)."""
    if math.isclose(kw, kh):
        return kw, kw
    (k1, f1), (k2, f2) = sorted([(kw, fw), (kh, fh)], reverse=True)  # k1 = more conductive
    up = k1 + f2 / (1 / (k2 - k1) + f1 / (2 * k1))
    lo = k2 + f1 / (1 / (k1 - k2) + f2 / (2 * k2))
    return lo, up


def honeycomb_formulas(d, t, kw, kh):
    phi = (d / (d + t)) ** 2
    lo, up = hashin_shtrikman_2d(kw, 1 - phi, kh, phi)
    sx, sy = closed_form(d / S3, t, kw, kh)
    return {"phi": phi, "along": phi * kh + (1 - phi) * kw, "thin": phi * kh + 0.5 * (1 - phi) * kw,
            "hs_lo": lo, "hs_up": up, "slice_x": sx, "slice_y": sy}


def honeycomb_solve(pic, kw, kh, label, verbose=True):
    """Face conductivity = s k_wall + (1 − s) k_fill, with s the wall area fraction of the
    pixel-sized square centred on that face (wall and fill side by side, area-weighted).
    Why not the repo's Pixel FV rule (area-weighted pixels, harmonic mean between pixels): on
    the FE benchmark it was −1.5 % / −4.1 % off at 10 px across the wall and its x/y split at the
    defaults was 5 %, because the harmonic mean puts the partly filled pixels of a slanted wall
    in series. Face-centred fractions keep the full conductance along slanted walls: within
    0.35 % of the FE values from 5 to 40 px, x/y split < 0.1 %. Cost: arithmetic mixing across a
    wall edge drops about half a pixel of fill per edge, i.e. about px/d of the fill path.
    Walls are isotropic with the along-wall value (shortcut: a thin wall's through-wall
    conduction barely matters for the layer). Returns the 2 × 2 tensor."""
    kf = [s * kw + (1 - s) * kh for s in pic["s"]]
    K, infos = PeriodicConduction(kf).tensor((0, 1), label, verbose=verbose)
    del kf
    free_gpu()
    return K, infos


def through_plate(k_along, k_across, tilt_deg):
    """A wide plate sees the conductivity tensor along its normal: k_n = k∥ cos²θ + k⊥ sin²θ."""
    c2 = math.cos(math.radians(tilt_deg)) ** 2
    return k_along * c2 + k_across * (1 - c2)


# ============================ OUTPUT ==============================
def header():
    print("=" * 78)
    print("Aerogel layer conductivity (conduction only): WALL then HONEYCOMB")
    if GPU:
        name = cp.cuda.runtime.getDeviceProperties(0)["name"]
        name = name.decode() if isinstance(name, bytes) else name
        free, tot = cp.cuda.runtime.memGetInfo()
        print(f"backend: GPU (CuPy {cp.__version__}), device: {name}, memory {tot / 1e9:.0f} GB")
    else:
        print(f"backend: CPU (NumPy {np.__version__}); no CUDA device found")
    print(f"mode: {RUN_MODE}   preconditioner: {PRECONDITIONER}   CG tolerance: {CG_TOL:g}")
    if FULL and not GPU:
        print("!!! WARNING: full mode on a CPU will take a very long time")
    print("=" * 78)


def step_wall():
    print("\n" + "=" * 30 + " STEP 1: WALL " + "=" * 30)
    P = wall_inputs()
    if P["FILLER"] not in ("BN", "CNT"):
        raise ValueError("FILLER must be 'BN' or 'CNT'")
    if P["FILLER"] == "CNT" and math.isclose(P["M_FILLER_G"], 5.0):
        print("!!! NOTE: FILLER = CNT with 5.00 g filler. The C2.5 recipe has 1.25 g dry CNT.")
    comp = wall_composition(P)
    G = wall_grid(P)
    fname = "BN" if P["FILLER"] == "BN" else "CNT"
    seeds = list(range(SEED0, SEED0 + (N_SEEDS_FULL if FULL else N_SEEDS_QUICK)))
    nx, ny, nz = G["shape"]
    cells = nx * ny * nz
    print(f"grid {nx} × {ny} × {nz} = {cells:.3g} voxels of {P['VOXEL_NM']} nm "
          f"(wall {nz * P['VOXEL_NM']:.0f} nm thick in the model vs {P['WALL_THICKNESS_UM'] * 1e3:.0f} nm input), "
          f"est. memory {est_bytes(cells, 3) / 1e9:.2f} GB per solve, {len(seeds)} seeds")
    tag = ""
    what = "rod diameter" if fname == "CNT" else "sheet thickness"
    if G["under_resolved"]:
        print(f"!!! WARNING: {what} is only {G['small_vox']:.2f} voxels (< 2): objects under-resolved")
        tag = " [QUICK, NOT CONVERGED]" if not FULL else " [UNDER-RESOLVED]"
    if G["self_overlap"]:
        print(f"!!! WARNING: {'rod length' if fname == 'CNT' else 'sheet diameter'} > 0.8 × patch: "
              "objects may overlap their own periodic images")
        tag = tag or " [PATCH TOO SMALL]"
    k_pore = k_gas(P["WALL_PORE_SIZE_NM"] * 1e-9, T_K, PRESSURE_PA)
    if not 250 <= T_K <= 400:
        print("!!! WARNING: T_K outside the air table (250–400 K); air conductivity clamped")
    if P["WALL_POROSITY"] > 0:
        print(f"wall pores: {P['WALL_PORE_FILL']}, k = "
              f"{(k_pore if P['WALL_PORE_FILL'] == 'air' else P['K_EPOXY']):.4g} W/m·K"
              + (f" (air, Knudsen gap {P['WALL_PORE_SIZE_NM']} nm)" if P["WALL_PORE_FILL"] == "air" else ""))
    runs = []
    for s in seeds:
        r = run_wall(P, s)
        K = r["K"]
        print(f"  seed {s}: {r['objects']} {'rods' if fname == 'CNT' else 'sheets'} "
              f"({r['cut']} cut to the wall thickness), filler {100 * r['fractions']['filler']:.1f} % of voxels; "
              f"k_xx {K[0, 0]:.4g}, k_yy {K[1, 1]:.4g}, k_zz {K[2, 2]:.4g} W/m·K; "
              f"build {r['t_build']:.1f} s, total {r['time']:.1f} s")
        runs.append(r)
    if GPU:
        print(f"  GPU memory pool now: {cp.get_default_memory_pool().total_bytes() / 1e9:.2f} GB")

    names = {"filler": fname, "CNF": "CNF", "PMSQ": "PMSQ (from MTMS)", "pore": f"pore ({P['WALL_PORE_FILL']})"}
    rows = []
    for k in ("filler", "CNF", "PMSQ", "pore"):
        rows.append([names[k], 100 * comp["wt"][k] if k in comp["wt"] else None,
                     100 * comp["v_dense"][k] if k in comp["v_dense"] else None, 100 * comp["v"][k],
                     100 * np.mean([r["fractions"][k] for r in runs])])
    show(f"Wall composition{tag}",
         ["phase", "mass % (dense wall)", "volume % (dense)", "volume % (with porosity)", "achieved voxel %"],
         rows, f"dense wall density {comp['rho_dense']:.3f} g/cm³; with porosity {comp['rho_wall']:.3f} g/cm³; "
               f"dry solids {sum(comp['mass_g'].values()):.3f} g per batch")

    Ks = np.array([r["K"] for r in runs])
    rows = []
    for lab, f in (("along wall x", lambda K: K[0, 0]), ("along wall y", lambda K: K[1, 1]),
                   ("along wall (mean of x, y)", along), ("through wall z", lambda K: K[2, 2])):
        vals = np.array([f(K) for K in Ks])
        if lab.startswith("along wall ("):
            par = np.mean([0.5 * (r["par"][0] + r["par"][1]) for r in runs])
            ser = np.mean([0.5 * (r["ser"][0] + r["ser"][1]) for r in runs])
        else:
            a = {"x": 0, "y": 1, "z": 2}[lab[-1]]
            par, ser = np.mean([r["par"][a] for r in runs]), np.mean([r["ser"][a] for r in runs])
        rows.append([lab, par, ser, vals.mean(), vals.min(), vals.max()])
    iters = [i["iters"] for r in runs for i in r["infos"]]
    t_solve = [i["time"] for r in runs for i in r["infos"]]
    show(f"Wall conductivity (W/m·K){tag}",
         ["direction", "parallel bound, perfect contacts", "series (perfect contacts)",
          "simulation mean", "min", "max"], rows,
         f"  largest off-diagonal |k_ij| / √(k_ii k_jj): {max(max_offdiag(K) for K in Ks):.2e}\n"
         f"  CG iterations {min(iters)}–{max(iters)}, worst residual {max(i['res'] for r in runs for i in r['infos']):.1e}, "
         f"worst energy check {max(i['energy'] for r in runs for i in r['infos']):.1e}\n"
         f"  grid {nx} × {ny} × {nz}, voxel {P['VOXEL_NM']} nm, patch {nx * P['VOXEL_NM'] / 1e3:.2f} µm, "
         f"{len(seeds)} seeds; time per solve {np.mean(t_solve):.2f} s, whole wall step "
         f"{sum(r['time'] for r in runs):.1f} s\n"
         "  The z value is that of a periodic stack of walls (the intrinsic through-wall value).\n"
         "  Low/high = spread over random walls only, not the input uncertainty (see sensitivity).")
    k_al = np.array([along(K) for K in Ks])
    wall = {"likely": float(k_al.mean()), "low": float(k_al.min()), "high": float(k_al.max()),
            "through_mean": float(Ks[:, 2, 2].mean()), "tag": tag, "composition": comp,
            "tensors": Ks.tolist(), "rho_wall": comp["rho_wall"]}
    print(f"\n-> wall conductivity along the wall passed on: likely {wall['likely']:.4g}, low {wall['low']:.4g}, "
          f"high {wall['high']:.4g} W/m·K (through wall {wall['through_mean']:.4g}, informative only){tag}")

    sens = RUN_SENSITIVITY if RUN_SENSITIVITY != "auto" else GPU
    if sens:
        wall["sensitivity"] = step_sensitivity(P, G, runs, tag)
    return wall, runs


def step_sensitivity(P, G, runs, tag):
    """One input at a time to a low and a high value; the same random seeds for every point."""
    patch_um = G["shape"][0] * P["VOXEL_NM"] / 1e3
    cap = round(0.8 * patch_um, 3)
    if P["FILLER"] == "BN":
        items = [("K_BN_INPLANE", 100, 550), ("SHEET_DIAMETER_UM", 0.5, 3.0), ("SHEET_THICKNESS_NM", 10, 100)]
    else:  # rod ranges: hypothetical sweep ranges for hypothetical inputs
        items = [("K_CNT_AXIAL", 10, 1000), ("ROD_LENGTH_UM", 0.5, 3.0), ("ROD_DIAMETER_NM", 10, 30)]
    items += [("SHEET_TILT_STD_DEG", 3, 30), ("R_FILLER_BINDER", 0.6e-8, 5e-8), ("R_FILLER_FILLER", 1e-9, 1e-7),
              ("WALL_POROSITY", 0.0, 0.4), ("K_CNF", 0.5, 2.0), ("K_PMSQ", 0.1, 0.3)]
    seeds = list(range(SEED0, SEED0 + N_SEEDS_SENS))
    base_runs = [r for r in runs[:N_SEEDS_SENS]]
    while len(base_runs) < len(seeds):
        base_runs.append(run_wall(P, seeds[len(base_runs)], axes=(0, 1), label="sens base", verbose=False))
    base = float(np.mean([along(r["K"]) for r in base_runs]))
    n_pts = 2 * len(items) * len(seeds)
    print(f"\nSensitivity: {len(items)} inputs × 2 values × {len(seeds)} seeds × 2 solves = {2 * n_pts} solves "
          f"(baseline k_along {base:.4g} W/m·K from seeds {seeds})")
    rows = []
    for name, lo, hi in items:
        vals, notes = [], []
        for v in (lo, hi):
            if name in ("SHEET_DIAMETER_UM", "ROD_LENGTH_UM") and v > cap:
                notes.append(f"{v} capped at {cap} (0.8 × patch)")
                v = cap
            Q = dict(P, **{name: v})
            if wall_grid(Q)["under_resolved"] and name in ("SHEET_THICKNESS_NM", "ROD_DIAMETER_NM"):
                notes.append(f"{v} skipped (< 2 voxels)")
                vals.append((v, None))
                continue
            t0 = time.time()
            k = float(np.mean([along(run_wall(Q, s, axes=(0, 1), label=f"sens {name}={v}", verbose=False)["K"])
                               for s in seeds]))
            print(f"  {name} = {v:g}: k_along {k:.4g} W/m·K ({time.time() - t0:.1f} s)")
            vals.append((v, k))
        (vlo, klo), (vhi, khi) = vals
        swing = 100 * abs(khi - klo) / base if klo is not None and khi is not None else float("nan")
        rows.append([name, vlo, vhi, klo, khi, swing, "; ".join(notes)])
    rows.sort(key=lambda r: -1 if math.isnan(r[5]) else r[5], reverse=True)
    show(f"Wall sensitivity, one input at a time (k along the wall, W/m·K){tag}",
         ["input", "low", "high", "k_along at low", "k_along at high", "swing % of baseline", "note"], rows,
         f"  baseline {base:.4g} W/m·K; swing = |k(high) − k(low)| / baseline; {len(seeds)} seeds per point")
    return {"baseline": base, "rows": rows}


def step_honeycomb(wall):
    print("\n" + "=" * 28 + " STEP 2: HONEYCOMB " + "=" * 27)
    d, t = PORE_SIZE_UM * 1e-6, WALL_THICKNESS_UM * 1e-6
    fill = str(CELL_FILL).lower()
    kh = k_gas(d, T_K, PRESSURE_PA) if fill == "air" else K_EPOXY
    if K_WALL_SOURCE == "wall":
        kws = [("likely", wall["likely"]), ("low", wall["low"]), ("high", wall["high"])]
        src = f"wall step{wall['tag']}"
    else:
        kws = [("given", float(K_WALL_SOURCE))]
        src = "K_WALL_SOURCE (number)"
    wall_px = WALL_PIXELS_FULL if FULL else WALL_PIXELS_QUICK
    pic = honeycomb_picture(d, t, wall_px)
    cells = pic["nx"] * pic["ny"]
    print(f"cell fill: {fill}, k_fill = {kh * 1e3:.3f} mW/m·K"
          + (f" (air, Knudsen gap d = {PORE_SIZE_UM} µm)" if fill == "air" else " (K_EPOXY)"))
    print(f"k_wall from {src}: " + ", ".join(f"{n} {v:.4g}" for n, v in kws) + " W/m·K")
    print(f"pixel grid {pic['nx']} × {pic['ny']} = {cells:.3g} px of {pic['px'] * 1e9:.1f} nm, "
          f"{pic['wall_px']:.2f} px across the wall, y stretch {100 * pic['stretch_y']:+.4f} %, "
          f"est. memory {est_bytes(cells, 2) / 1e9:.2f} GB per solve")
    out = {"pic": {k: v for k, v in pic.items() if k != "s"}, "cases": {}}
    rho_w = RHO_WALL if RHO_WALL is not None else wall["rho_wall"]
    flag = wall["tag"] if K_WALL_SOURCE == "wall" else ""
    for case, kfill_of in (("A", lambda kw: kh), ("B", lambda kw: 1e-6 * kw)):
        title = (f"walls + {fill}" if case == "A" else "walls only (empty cells, fill = 1e-6 × k_wall: pure k_solid)")
        print(f"\n  case {case}: {title}")
        cols = ["quantity (mW/m·K unless stated)"] + [f"{n} (k_wall {v:.4g} W/m·K)" for n, v in kws]
        res = []
        for n, kw in kws:
            kf_ = kfill_of(kw)
            F = honeycomb_formulas(d, t, kw, kf_)
            K, infos = honeycomb_solve(pic, kw, kf_, f"honeycomb {case} {n}")
            sim = 0.5 * (K[0, 0] + K[1, 1])
            res.append({"kw": kw, "kfill": kf_, "F": F, "K": K, "sim": sim, "infos": infos,
                        "split": abs(K[0, 0] - K[1, 1]) / sim, "off": max_offdiag(K),
                        "n_sim": through_plate(F["along"], sim, CHANNEL_TILT_DEG),
                        "n_formula": through_plate(F["along"], F["thin"], CHANNEL_TILT_DEG)})
            for i in infos:
                i["bounds_ok"] = F["hs_lo"] * (1 - 1e-9) <= K[i["axis"], i["axis"]] <= F["hs_up"] * (1 + 1e-9)
        m = 1e3
        spec = [
            ("along channels, exact: φ k_fill + (1 − φ) k_wall", lambda r: m * r["F"]["along"]),
            ("across, thin-wall formula: φ k_fill + ½(1 − φ) k_wall", lambda r: m * r["F"]["thin"]),
            ("across, Hashin–Shtrikman 2-D lower bound", lambda r: m * r["F"]["hs_lo"]),
            ("across, Hashin–Shtrikman 2-D upper bound", lambda r: m * r["F"]["hs_up"]),
            ("across, slice model upper bound, x (along L)", lambda r: m * r["F"]["slice_x"]),
            ("across, slice model upper bound, y", lambda r: m * r["F"]["slice_y"]),
            ("across, simulation k_xx", lambda r: m * r["K"][0, 0]),
            ("across, simulation k_yy", lambda r: m * r["K"][1, 1]),
            ("across, simulation mean (k⊥)", lambda r: m * r["sim"]),
            ("|k_xx − k_yy| / mean, % (must be 0 by symmetry: discretisation error)", lambda r: 100 * r["split"]),
            ("off-diagonal |k_xy| / k⊥", lambda r: r["off"]),
            (f"through plate, tilt {CHANNEL_TILT_DEG}°: k∥ cos²θ + k⊥ sin²θ, k⊥ simulated", lambda r: m * r["n_sim"]),
            (f"through plate, tilt {CHANNEL_TILT_DEG}°, k⊥ from the thin-wall formula", lambda r: m * r["n_formula"]),
            ("CG iterations x / y", lambda r: f"{r['infos'][0]['iters']} / {r['infos'][1]['iters']}"),
            ("energy check, worst plane deviation", lambda r: max(i["energy"] for i in r["infos"])),
            ("k_fill used", lambda r: m * r["kfill"]),
        ]
        show(f"Honeycomb layer conductivity (mW/m·K), case {case}: {title}{flag}", cols,
             [[lab] + [f(r) for r in res] for lab, f in spec],
             "  A wide plate sees the layer's conductivity tensor along its normal; with the channels tilted\n"
             "  by θ from the normal that is k∥ cos²θ + k⊥ sin²θ (θ = CHANNEL_TILT_DEG).")
        out["cases"][case] = [{"k_wall": r["kw"], "k_fill": r["kfill"], "formulas": r["F"], "K": r["K"].tolist(),
                               "k_across": r["sim"], "k_through_plate": r["n_sim"], "split": r["split"]} for r in res]
    phi = (d / (d + t)) ** 2
    rho_bulk = (1 - phi) * rho_w + (phi * RHO_EPOXY if fill == "epoxy" else 0.0)
    show("Honeycomb geometry",
         ["quantity", "value"],
         [["pore size d (flat to flat), µm", PORE_SIZE_UM], ["wall thickness t, µm", WALL_THICKNESS_UM],
          ["hexagon inner side l = d/√3, µm", pic["l"] * 1e6],
          ["periodic unit L × H (2 cells), µm", f"{pic['L'] * 1e6:.4g} × {pic['H'] * 1e6:.4g}"],
          ["pixels nx × ny", f"{pic['nx']} × {pic['ny']}"], ["pixel size, nm", pic["px"] * 1e9],
          ["pixels across the wall", pic["wall_px"]], ["y stretch of the picture, %", 100 * pic["stretch_y"]],
          ["porosity φ, analytic (d/(d + t))²", phi], ["porosity, counted from the picture", pic["phi_counted"]],
          ["wall density, g/cm³", rho_w], ["bulk layer density, g/cm³ (+ epoxy in cells if infused)", rho_bulk]])
    out.update(phi=phi, phi_counted=pic["phi_counted"], rho_wall=rho_w, rho_bulk=rho_bulk, k_fill=kh)

    if RES_STUDY:
        kw = kws[0][1]
        rows = []
        for f in (1, 2, 4):
            wp = wall_px / f
            if wp < 2:
                continue
            p2 = pic if f == 1 else honeycomb_picture(d, t, wp)
            K = out["cases"]["A"][0]["K"] if f == 1 else honeycomb_solve(p2, kw, kh, f"res study {wp:g} px")[0]
            K = np.asarray(K)
            mean = 0.5 * (K[0, 0] + K[1, 1])
            rows.append([p2["wall_px"], f"{p2['nx']} × {p2['ny']}", 1e3 * K[0, 0], 1e3 * K[1, 1], 1e3 * mean,
                         100 * abs(K[0, 0] - K[1, 1]) / mean])
        show(f"Resolution study, case A, k_wall {kw:.4g} W/m·K (mW/m·K)",
             ["px across wall", "grid", "k_xx", "k_yy", "mean", "x–y split %"], rows)
        out["res_study"] = rows
    return out


def run_checks():
    print("\n" + "=" * 31 + " CHECKS " + "=" * 39)

    def add(name, expected, got, ok):
        CHECKS.append([name, expected, got, "PASS" if ok else "FAIL"])

    # 1. uniform box
    k0 = 3.7
    kf = [face_k(xp.full((12, 10, 8), k0), d) for d in range(3)]
    K, _ = PeriodicConduction(kf).tensor((0, 1, 2), "check 1 uniform", verbose=False)
    err = np.abs(K - k0 * np.eye(3)).max() / k0
    add("1. uniform 3-D box -> k·I", f"k = {k0}, rel. error < 1e-10", f"{err:.1e}", err < 1e-10)
    # 2. layered box (layers normal to z), and 3. the same with an interface resistance
    nz, h = 10, 5e-9
    k1, k2 = 2.0, 50.0
    kz = np.where(np.arange(nz) < 4, k1, k2)  # 4 cells of k1, 6 of k2
    kmap = xp.asarray(np.broadcast_to(kz, (6, 7, nz)).copy())
    ar, hm = float(kz.mean()), 1.0 / float((1.0 / kz).mean())
    for R in (0.0, 2e-9):
        Rz = xp.zeros_like(kmap)
        if R:
            Rz[:, :, 3] = R  # face between cell 3 (k1) and cell 4 (k2)
            Rz[:, :, nz - 1] = R  # periodic face between the last cell (k2) and the first (k1)
        kf = [face_k(kmap, 0), face_k(kmap, 1), face_k(kmap, 2, Rz if R else None, h)]
        K, _ = PeriodicConduction(kf).tensor((0, 1, 2), f"check layered R={R}", verbose=False)
        zz = 1.0 / ((1.0 / kz).mean() + 2 * R / (nz * h))  # 1/k = (Σ h/k_i + 2R) / (nz h)
        e_xy = max(abs(K[0, 0] / ar - 1), abs(K[1, 1] / ar - 1))
        e_z = abs(K[2, 2] / zz - 1)
        if not R:
            add("2. layered box: x, y = arithmetic mean", f"{ar:.6g}", f"{K[0, 0]:.10g}, {K[1, 1]:.10g}", e_xy < 1e-8)
            add("2. layered box: z = harmonic mean", f"{hm:.10g}", f"{K[2, 2]:.10g} (err {e_z:.1e})", e_z < 1e-8)
        else:
            add(f"3. layered + R = {R:g} m²K/W: 1/k_z = mean(h/k)/h + 2R/(nz h)", f"{zz:.10g}",
                f"{K[2, 2]:.10g} (err {e_z:.1e})", e_z < 1e-8 and e_xy < 1e-8)
    # 4. honeycomb benchmark against an independent fitted-mesh finite-element solve
    kw, kh, l = 200.0, 0.026, 1e-6
    t = 0.10 * l
    d = S3 * l
    sx, sy = closed_form(l, t, kw, kh)
    add("4a. slice closed form, t/l = 0.1, 200 / 0.026 (W/m·K)", "14.67 / 15.99", f"{sx:.4f} / {sy:.4f}",
        abs(sx / 14.67 - 1) < 5e-4 and abs(sy / 15.99 - 1) < 5e-4)
    bp = BENCH_WALL_PIXELS_FULL if FULL else BENCH_WALL_PIXELS_QUICK
    pic = honeycomb_picture(d, t, bp)
    print(f"  check 4: benchmark grid {pic['nx']} × {pic['ny']}, {pic['wall_px']:.2f} px across the wall")
    K, _ = honeycomb_solve(pic, kw, kh, "check 4 benchmark", verbose=True)
    ex, ey = K[0, 0] / 11.17 - 1, K[1, 1] / 11.18 - 1
    lim = 0.005 if FULL else 0.02
    add(f"4b. honeycomb vs FE, {pic['wall_px']:.1f} px across wall (W/m·K)", f"11.17 / 11.18 (±{100 * lim:g} %)",
        f"{K[0, 0]:.4f} / {K[1, 1]:.4f} (err {100 * ex:+.2f} % / {100 * ey:+.2f} %)", max(abs(ex), abs(ey)) < lim)
    # 5. honeycomb at the repo defaults, k_wall = 4.0, air
    d, t, kw = 30e-6, 0.27e-6, 4.0
    kh = k_gas(d, 300.0, 101325.0)
    F = honeycomb_formulas(d, t, kw, kh)
    pic = honeycomb_picture(d, t, WALL_PIXELS_FULL if FULL else WALL_PIXELS_QUICK)
    K, _ = honeycomb_solve(pic, kw, kh, "check 5 defaults", verbose=True)
    sim = 0.5 * (K[0, 0] + K[1, 1])
    split = abs(K[0, 0] - K[1, 1]) / sim
    add("5a. defaults, k_wall 4, air: HS lower <= k⊥ <= HS upper (mW/m·K)",
        f"{1e3 * F['hs_lo']:.2f} … {1e3 * F['hs_up']:.2f}", f"{1e3 * sim:.2f}", F["hs_lo"] <= sim <= F["hs_up"])
    dev = sim / F["thin"] - 1
    add("5b. defaults: k⊥ vs thin-wall formula (within 3 %)", f"{1e3 * F['thin']:.2f}",
        f"{1e3 * sim:.2f} ({100 * dev:+.2f} %); x/y split {100 * split:.2f} %", abs(dev) < 0.03)
    # 6. every solve of the run
    tol_e = max(1e-6, 100 * CG_TOL)
    bad = [i["label"] for i in SOLVES if not i["converged"]]
    add("6a. CG converged, every solve", f"{len(SOLVES)} solves, residual < {CG_TOL:g}",
        f"{len(SOLVES) - len(bad)} converged; worst residual {max(i['res'] for i in SOLVES):.1e}"
        + (f"; NOT: {', '.join(bad[:4])}" if bad else ""), not bad)
    worst = max(SOLVES, key=lambda i: i.get("energy", 0.0))
    add("6b. energy balance, every solve", f"plane fluxes equal to < {tol_e:g}",
        f"worst {worst['energy']:.1e} ({worst['label']})", worst["energy"] < tol_e)
    nb = [i["label"] for i in SOLVES if i.get("bounds_ok") is False]
    nck = sum(1 for i in SOLVES if "bounds_ok" in i)
    add("6c. bounds, every wall / layer solve", "wall: series with contacts ≤ k ≤ parallel; layer: HS",
        f"{nck - len(nb)} of {nck} inside" + (f"; outside: {', '.join(nb[:4])}" if nb else ""), not nb)
    show("Checks", ["check", "expected", "got", "result"], CHECKS)
    n_fail = sum(r[3] == "FAIL" for r in CHECKS)
    print(f"\n{'ALL CHECKS PASS' if not n_fail else f'!!! {n_fail} CHECK(S) FAILED: see the table above'}")


T_START = time.time()
header()
WALL_RESULT, _wall_runs = step_wall()
RESULTS["wall"] = {k: v for k, v in WALL_RESULT.items() if k != "composition"}
RESULTS["wall"]["composition"] = WALL_RESULT["composition"]
RESULTS["honeycomb"] = step_honeycomb(WALL_RESULT)
if RUN_CHECKS:
    run_checks()
    RESULTS["checks"] = CHECKS
print(f"\nTotal run time {time.time() - T_START:.1f} s ({RUN_MODE} mode, {'GPU' if GPU else 'CPU'})")
