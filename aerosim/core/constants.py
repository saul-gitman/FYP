"""Physical constants and air properties, each with its source. SI units."""

import numpy as np

SIGMA = 5.670374419e-8  # W/m²K⁴, Stefan–Boltzmann constant (CODATA 2018)
K_B = 1.380649e-23  # J/K, Boltzmann constant (exact, SI 2019)
G = 9.81  # m/s², standard gravity

# Air, Incropera et al., Fundamentals of Heat and Mass Transfer, Table A.4 (1 atm)
AIR_T = np.array([250.0, 300.0, 350.0, 400.0])  # K
AIR_K = np.array([22.3e-3, 26.3e-3, 30.0e-3, 33.8e-3])  # W/m·K
AIR_NU_300 = 15.89e-6  # m²/s, kinematic viscosity at 300 K (Table A.4)
AIR_ALPHA_300 = 22.5e-6  # m²/s, thermal diffusivity at 300 K (Table A.4)
AIR_PR = 0.71  # Prandtl number near 300 K (Table A.4: 0.707)
AIR_GAMMA = 1.4  # ratio of specific heats cp/cv for a diatomic gas (kinetic theory)
# Kinetic-theory collision diameter of an air molecule; gives the standard λ ≈ 66 nm at 300 K, 1 atm
AIR_DIAMETER = 3.72e-10  # m


def k_air(T):
    """Free (bulk) air conductivity at temperature T, linear interpolation in Table A.4."""
    return float(np.interp(T, AIR_T, AIR_K))


def mean_free_path(T, pressure):
    """Mean free path of air molecules, kinetic theory: λ = k_B T / (√2 π d_g² p)."""
    return K_B * T / (np.sqrt(2) * np.pi * AIR_DIAMETER**2 * pressure)


def knudsen_beta(alpha=1.0):
    """β = ((2 − α)/α) · (2γ/(γ + 1)) / Pr ≈ 1.64 for air (Kaganer 1969; Zeng et al. 1995)."""
    return (2 - alpha) / alpha * (2 * AIR_GAMMA / (AIR_GAMMA + 1)) / AIR_PR
