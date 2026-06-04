"""
Simulation 5: Modular Zeta Function for Type III_1 Factors

Tests: The modular zeta function ζ(s) = Tr(|D_ω|^(-s)) for Type III_1 factors,
its analytic continuation, spectral density, and regularized determinant.

Corrected per verification report:
- The spectral density of D_ω for Type III_1 is UNIFORM (Lebesgue measure),
  NOT ρ(μ) ∝ e^(-|μ|/(2π)).
- The exponential factor e^(-|μ|/(2π)) is the THERMAL WEIGHT (Boltzmann factor),
  not the spectral density.
- The zeta function with uniform spectral density diverges; must use thermal
  weight for regularization.

MCC Reference: Session 2, Section 1.5; Session 2, Addendum A
Verification Report: Errors 2.1 and 2.2
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import special


# ============================================================================
# SECTION 1: SPECTRAL DENSITY
# ============================================================================

def uniform_spectral_density(mu, C=1.0):
    """
    Uniform spectral density (Lebesgue measure) for Type III_1 factors.
    
    CORRECTED (per verification report, Error 2.1):
    The spectral density of D_ω for Type III_1 is uniform:
        ρ_D(μ) = C (constant, uniform on ℝ)
    
    NOT ρ_D(μ) ∝ e^(-|μ|/(2π)) — that is the THERMAL WEIGHT.
    
    Parameters:
        mu: Eigenvalue(s) of D_ω
        C: Normalization constant
    
    Returns:
        rho: Spectral density value(s)
    """
    return np.full_like(mu, C, dtype=float)


def thermal_weight(mu, beta=2 * np.pi):
    """
    Thermal weight (Boltzmann factor) for the modular Hamiltonian.
    
    For a thermal state at inverse temperature beta:
        w(μ) = e^(-beta * |μ|)
    
    The expectation value of an observable O is:
        <O> = ∫ dμ ρ_D(μ) w(μ) O(μ)
    
    where ρ_D is the uniform spectral density and w is the thermal weight.
    
    Parameters:
        mu: Eigenvalue(s) of D_ω
        beta: Inverse modular temperature (beta = 2*pi for Unruh)
    
    Returns:
        w: Thermal weight value(s)
    """
    return np.exp(-beta * np.abs(mu))


def combined_measure(mu, C=1.0, beta=2 * np.pi):
    """
    Combined spectral measure: ρ_D(μ) * w(μ) = C * e^(-beta * |μ|).
    
    This is what appears in the zeta function integral when using
    the thermal state expectation.
    
    Parameters:
        mu: Eigenvalue(s) of D_ω
        C: Spectral density normalization
        beta: Inverse temperature
    
    Returns:
        measure: Combined measure value(s)
    """
    return C * thermal_weight(mu, beta)


# ============================================================================
# SECTION 2: ZETA FUNCTION
# ============================================================================

def zeta_function_thermal(s, C=1.0, beta=2 * np.pi, N_modes=10000):
    """
    Compute the modular zeta function with thermal weight regularization.
    
    ζ_D(s) = ∫ dμ ρ_D(μ) w(μ) |μ|^(-s)
           = 2C ∫_0^∞ dμ e^(-beta*μ) μ^(-s)
           = 2C * beta^(s-1) * Γ(1-s)
    
    Valid for Re(s) < 1.
    
    Parameters:
        s: Complex parameter
        C: Spectral density normalization
        beta: Inverse temperature
        N_modes: Number of modes for numerical integration
    
    Returns:
        zeta_value: ζ_D(s) value
        analytical_value: Analytical formula value (for comparison)
    """
    s_real = np.real(s)
    
    if s_real >= 1:
        # Divergent — return NaN
        return np.nan, np.nan
    
    # Numerical integration
    mu = np.logspace(-10, 5, N_modes)
    measure = combined_measure(mu, C=C, beta=beta)
    integrand = measure * (mu ** (-s_real))
    
    # Use log-space integration for better accuracy
    zeta_numerical = np.trapezoid(integrand, np.log(mu)) * beta  # Jacobian from log transform
    
    # Analytical formula: ζ_D(s) = 2C * beta^(s-1) * Γ(1-s)
    zeta_analytical = 2 * C * (beta ** (s_real - 1)) * special.gamma(1 - s_real)
    
    return zeta_numerical, zeta_analytical


def zeta_function_analytic_continuation(s_real):
    """
    Compute ζ_D(s) using the analytical formula with analytic continuation.
    
    ζ_D(s) = 2C * (2π)^(s-1) * Γ(1-s)
    
    This formula is valid for Re(s) < 1. For Re(s) ≥ 1, we use the
    analytic continuation of the Gamma function.
    
    Parameters:
        s_real: Real part of s
    
    Returns:
        zeta: ζ_D(s) value (may be complex due to Gamma function poles)
    """
    C = 1.0
    beta = 2 * np.pi
    
    # The Gamma function has poles at non-positive integers:
    # Γ(z) → ∞ as z → 0, -1, -2, ...
    # So ζ_D(s) has poles at s = 1, 2, 3, ...
    
    z = 1 - s_real
    gamma_val = special.gamma(z)
    
    if np.isinf(gamma_val) or np.isnan(gamma_val):
        return np.nan
    
    zeta = 2 * C * (beta ** (s_real - 1)) * gamma_val
    
    return zeta


def zeta_prime_at_zero(s_grid):
    """
    Compute ζ_D'(0) numerically using finite differences.
    
    ζ_D'(0) is related to the regularized determinant:
        log det(D_ω) = -ζ_D'(0)
    
    Parameters:
        s_grid: Array of s values near 0
    
    Returns:
        zeta_prime_0: ζ_D'(0) value
    """
    zeta_values = []
    for s in s_grid:
        zeta = zeta_function_analytic_continuation(s)
        if not np.isnan(zeta):
            zeta_values.append((s, zeta))
    
    # Finite difference: ζ'(0) ≈ (ζ(ε) - ζ(-ε)) / (2ε)
    if len(zeta_values) >= 2:
        s_pos = zeta_values[-1][0]
        s_neg = zeta_values[0][0]
        zeta_pos = zeta_values[-1][1]
        zeta_neg = zeta_values[0][1]
        
        zeta_prime_0 = (zeta_pos - zeta_neg) / (2 * (s_pos - s_neg))
    else:
        zeta_prime_0 = np.nan
    
    return zeta_prime_0


def compute_regularized_determinant():
    """
    Compute the regularized determinant of D_ω.
    
    log det(D_ω) = -ζ_D'(0)
    
    For ζ_D(s) = 2C * (2π)^(s-1) * Γ(1-s):
    ζ_D'(s) = 2C * (2π)^(s-1) * [log(2π) * Γ(1-s) - Γ'(1-s)]
    
    At s = 0:
    ζ_D'(0) = 2C * (2π)^(-1) * [log(2π) * Γ(1) - Γ'(1)]
            = C/π * [log(2π) + γ]
    
    where γ is the Euler-Mascheroni constant (Γ'(1) = -γ).
    
    So: log det(D_ω) = -C/π * [log(2π) + γ]
    
    Returns:
        log_det: Regularized log determinant
        zeta_prime_0: ζ_D'(0)
    """
    C = 1.0
    gamma_const = 0.5772156649015328606065120900824024310421  # Euler-Mascheroni
    
    zeta_prime_0 = C / np.pi * (np.log(2 * np.pi) + gamma_const)
    log_det = -zeta_prime_0
    
    return log_det, zeta_prime_0


# ============================================================================
# SECTION 3: SPECTRAL ACTION
# ============================================================================

def spectral_action(Lambda, C=1.0, beta=2 * np.pi, N_modes=10000):
    """
    Compute the spectral action S(Λ) = Tr(f(D_ω/Λ)).
    
    For the Rindler vacuum with uniform spectral density and thermal weight:
        S(Λ) = ∫ dμ ρ(μ) w(μ) f(μ/Λ)
             = 2C ∫_0^∞ dμ e^(-beta*μ) f(μ/Λ)
    
    For f(x) = 1 for |x| ≤ 1, f(x) = 0 for |x| > 1 (sharp cutoff):
        S(Λ) = 2C ∫_0^Λ dμ e^(-beta*μ)
             = 2C * (1 - e^(-beta*Λ)) / beta
    
    As Λ → ∞:
        S(Λ) → 2C / beta = C/π
    
    For f(x) = e^(-x^2) (Gaussian cutoff):
        S(Λ) = 2C ∫_0^∞ dμ e^(-beta*μ) e^(-(μ/Λ)^2)
    
    Parameters:
        Lambda: Cutoff scale
        C: Spectral density normalization
        beta: Inverse temperature
        N_modes: Number of modes for numerical integration
    
    Returns:
        S: Spectral action value
    """
    mu = np.logspace(-10, np.log10(Lambda * 10), N_modes)
    measure = combined_measure(mu, C=C, beta=beta)
    
    # Gaussian cutoff function
    cutoff = np.exp(-(mu / Lambda) ** 2)
    integrand = measure * cutoff
    
    S = np.trapezoid(integrand, np.log(mu)) * beta
    
    return S


def spectral_action_asymptotic(Lambda, C=1.0, beta=2 * np.pi):
    """
    Compute the asymptotic expansion of the spectral action.
    
    S(Λ) = (Area/4G) + (Entropy term) + O(Λ^(-1))
    
    For the Rindler vacuum:
        S(Λ) ~ Λ/(2π) + O(1)
    
    The leading term is linear in Λ (the "volume" term).
    
    Parameters:
        Lambda: Cutoff scale
        C: Spectral density normalization
        beta: Inverse temperature
    
    Returns:
        S_asymptotic: Asymptotic spectral action
    """
    # Leading term: linear in Lambda
    S_linear = 2 * C * Lambda / beta
    
    # Subleading term: constant
    S_constant = -2 * C * np.log(Lambda) / beta  # From the exponential integral
    
    return S_linear + S_constant


# ============================================================================
# SECTION 4: PLOTTING
# ============================================================================

def plot_zeta_function(s_range, filename='output/zeta_plot.png'):
    """
    Plot the zeta function ζ_D(s) as a function of s.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    
    # 1. Zeta function real part vs s
    ax = axes[0, 0]
    s_values = np.linspace(-3, 0.9, 200)
    zeta_values = [zeta_function_analytic_continuation(s) for s in s_values]
    
    # Filter out NaN/inf
    valid = [(s, z) for s, z in zip(s_values, zeta_values)
             if not np.isnan(z) and not np.isinf(z) and abs(z) < 1e10]
    
    if valid:
        s_valid, z_valid = zip(*valid)
        ax.plot(s_valid, np.real(z_valid), 'b-', linewidth=2, label='Re(ζ_D(s))')
        ax.plot(s_valid, np.imag(z_valid), 'r--', linewidth=1.5, label='Im(ζ_D(s))')
        ax.set_xlabel('s (real)')
        ax.set_ylabel('ζ_D(s)')
        ax.set_title('Modular Zeta Function ζ_D(s)\n(Analytic continuation)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axvline(x=1, color='red', linestyle=':', alpha=0.5, label='Pole at s=1')
    
    # 2. Spectral density vs eigenvalue
    ax = axes[0, 1]
    mu_values = np.linspace(-20, 20, 1000)
    
    rho_uniform = uniform_spectral_density(mu_values, C=1.0)
    w_thermal = thermal_weight(mu_values, beta=2 * np.pi)
    combined = combined_measure(mu_values, C=1.0, beta=2 * np.pi)
    
    ax.plot(mu_values, rho_uniform, 'b-', linewidth=2, label='ρ_D(μ) = C (uniform)')
    ax.plot(mu_values, w_thermal, 'r-', linewidth=2, label='w(μ) = e^(-β|μ|) (thermal)')
    ax.plot(mu_values, combined, 'g-', linewidth=2, label='ρ(μ) = C·w(μ) (combined)')
    ax.set_xlabel('Eigenvalue μ of D_ω')
    ax.set_ylabel('Density / Weight')
    ax.set_title('Spectral Density vs Thermal Weight\n(CORRECTED: ρ_D is uniform, not exponential)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. Zeta function pole structure
    ax = axes[1, 0]
    s_pole_range = np.linspace(-1, 5, 500)
    zeta_pole = [zeta_function_analytic_continuation(s) for s in s_pole_range]
    
    valid_pole = [(s, z) for s, z in zip(s_pole_range, zeta_pole)
                  if not np.isnan(z) and not np.isinf(z) and abs(z) < 1e10]
    
    if valid_pole:
        s_p, z_p = zip(*valid_pole)
        ax.plot(s_p, np.abs(z_p), 'purple', linewidth=2)
        ax.set_xlabel('s (real)')
        ax.set_ylabel('|ζ_D(s)|')
        ax.set_title('Zeta Function Magnitude (Pole Structure)')
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3)
        
        # Mark poles
        for pole in [1, 2, 3]:
            ax.axvline(x=pole, color='red', linestyle=':', alpha=0.5)
            ax.text(pole, 10, f's={pole}', rotation=90, va='bottom', ha='center')
    
    # 4. Spectral action vs cutoff
    ax = axes[1, 1]
    Lambda_values = np.logspace(-2, 3, 100)
    S_values = [spectral_action(L, C=1.0, beta=2*np.pi) for L in Lambda_values]
    S_asym = [spectral_action_asymptotic(L, C=1.0, beta=2*np.pi) for L in Lambda_values]
    
    ax.plot(Lambda_values, S_values, 'b-', linewidth=2, label='Numerical S(Λ)')
    ax.plot(Lambda_values, S_asym, 'r--', linewidth=2, label='Asymptotic S(Λ)')
    ax.set_xlabel('Cutoff Λ')
    ax.set_ylabel('Spectral Action S(Λ)')
    ax.set_title('Spectral Action vs Cutoff')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✓ Zeta function plot saved to {filename}")


def plot_zeta_values_grid(filename='output/zeta_grid.png'):
    """
    Plot ζ_D(s) for a grid of s values.
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    
    s_real_range = np.linspace(-3, 0.9, 20)
    s_imag_range = np.linspace(-2, 2, 15)
    
    grid_values = np.zeros((len(s_imag_range), len(s_real_range)))
    
    for i, s_imag in enumerate(s_imag_range):
        for j, s_real in enumerate(s_real_range):
            s_complex = s_real + 1j * s_imag
            # Use numerical integration for complex s
            mu = np.logspace(-10, 5, 5000)
            measure = combined_measure(mu, C=1.0, beta=2*np.pi)
            integrand = measure * (mu ** (-s_real)) * np.cos(s_imag * np.log(mu))
            grid_values[i, j] = np.trapezoid(integrand, np.log(mu)) * 2 * np.pi
    
    im = ax.imshow(grid_values, extent=[-3, 0.9, -2, 2],
                   cmap='RdBu_r', origin='lower', aspect='auto')
    ax.set_xlabel('Re(s)')
    ax.set_ylabel('Im(s)')
    ax.set_title('Modular Zeta Function ζ_D(s)\n(Heat map of real part)')
    plt.colorbar(im, ax=ax, label='Re(ζ_D(s))')
    ax.axvline(x=1, color='red', linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✓ Zeta grid plot saved to {filename}")


# ============================================================================
# SECTION 5: MAIN SIMULATION
# ============================================================================

def main():
    """
    Main simulation: Compute modular zeta function, spectral density,
    regularized determinant, and spectral action for Type III_1 factors.
    """
    print("=" * 70)
    print("Simulation 5: Modular Zeta Function for Type III_1 Factors")
    print("Testing: Zeta function regularization, spectral density, determinant")
    print("=" * 70)
    
    # Parameters
    C = 1.0  # Spectral density normalization
    beta = 2 * np.pi  # Inverse modular temperature (Unruh)
    
    print(f"\nSpectral density normalization: C = {C}")
    print(f"Inverse modular temperature: beta = {beta:.4f}")
    
    # 1. Spectral density analysis
    print(f"\n{'=' * 70}")
    print("Spectral Density Analysis")
    print(f"{'=' * 70}")
    print(f"  CORRECTED (per verification report, Error 2.1):")
    print(f"  Spectral density ρ_D(μ) = C (UNIFORM, Lebesgue measure)")
    print(f"  Thermal weight w(μ) = e^(-β|μ|) (Boltzmann factor)")
    print(f"  Combined measure ρ(μ) = C·e^(-β|μ|) (used in zeta function)")
    print(f"")
    print(f"  The exponential factor e^(-|μ|/(2π)) is the THERMAL WEIGHT,")
    print(f"  NOT the spectral density. The spectral density is UNIFORM.")
    
    # 2. Zeta function computation
    print(f"\n{'=' * 70}")
    print("Zeta Function ζ_D(s) = 2C·β^(s-1)·Γ(1-s)")
    print(f"{'=' * 70}")
    
    s_test_values = [-2, -1, -0.5, 0, 0.5]
    
    for s in s_test_values:
        zeta_num, zeta_ana = zeta_function_thermal(s, C=C, beta=beta)
        print(f"\n  s = {s:6.2f}:")
        print(f"    Numerical: {zeta_num:.6f}")
        print(f"    Analytical: {zeta_ana:.6f}")
        if not np.isnan(zeta_num) and not np.isnan(zeta_ana):
            rel_error = abs(zeta_num - zeta_ana) / abs(zeta_ana) if abs(zeta_ana) > 1e-15 else float('inf')
            print(f"    Relative error: {rel_error:.2e}")
    
    # 3. Pole structure
    print(f"\n{'=' * 70}")
    print("Pole Structure")
    print(f"{'=' * 70}")
    print(f"  ζ_D(s) = 2C·(2π)^(s-1)·Γ(1-s)")
    print(f"  Poles at s = 1, 2, 3, ... (from Gamma function)")
    
    for pole in [1, 2, 3]:
        zeta_val = zeta_function_analytic_continuation(pole)
        print(f"  s = {pole}: ζ_D({pole}) = {zeta_val} (pole)")
    
    # 4. Zeta(0)
    print(f"\n{'=' * 70}")
    print("ζ_D(0) — Related to Anomaly")
    print(f"{'=' * 70}")
    
    zeta_0 = zeta_function_analytic_continuation(0)
    print(f"  ζ_D(0) = 2C·(2π)^(-1)·Γ(1) = 2C/(2π) = C/π")
    print(f"  ζ_D(0) = {zeta_0:.6f}")
    print(f"  This is related to the trace anomaly of the modular Dirac operator.")
    
    # 5. Zeta'(0) and regularized determinant
    print(f"\n{'=' * 70}")
    print("ζ_D'(0) and Regularized Determinant")
    print(f"{'=' * 70}")
    
    log_det, zeta_prime_0 = compute_regularized_determinant()
    gamma_const = 0.5772156649015328606065120900824024310421
    
    print(f"  ζ_D'(0) = C/π · [log(2π) + γ]")
    print(f"  ζ_D'(0) = {C/np.pi} · [{np.log(2*np.pi):.6f} + {gamma_const:.6f}")
    print(f"  ζ_D'(0) = {zeta_prime_0:.6f}")
    print(f"  log det(D_ω) = -ζ_D'(0) = {log_det:.6f}")
    
    # 6. Spectral action
    print(f"\n{'=' * 70}")
    print("Spectral Action S(Λ)")
    print(f"{'=' * 70}")
    
    Lambda_values = [0.1, 1.0, 10.0, 100.0, 1000.0]
    for Lambda in Lambda_values:
        S = spectral_action(Lambda, C=C, beta=beta)
        S_asym = spectral_action_asymptotic(Lambda, C=C, beta=beta)
        print(f"  Λ = {Lambda:8.1f}: S(Λ) = {S:.4f} (numerical), {S_asym:.4f} (asymptotic)")
    
    # 7. Plots
    plot_zeta_function(np.linspace(-3, 0.9, 200))
    plot_zeta_values_grid()
    
    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"This simulation tests the MCC prediction for the modular zeta function")
    print(f"ζ_D(s) = Tr(D_ω^(-s)) for Type III_1 factors with continuous spectrum.")
    print(f"")
    print(f"Key results:")
    print(f"  - Spectral density: UNIFORM (Lebesgue measure)")
    print(f"  - Thermal weight: e^(-β|μ|) (separate from spectral density)")
    print(f"  - Zeta function: ζ_D(s) = 2C·β^(s-1)·Γ(1-s)")
    print(f"  - ζ_D(0) = {zeta_0:.6f} (C/π)")
    print(f"  - log det(D_ω) = {log_det:.6f}")
    print(f"  - Poles at s = 1, 2, 3, ...")
    print(f"")
    print(f"CAVEATS (per verification report):")
    print(f"  1. The spectral density is UNIFORM, NOT exponential.")
    print(f"  2. The exponential factor is the THERMAL WEIGHT, not the density.")
    print(f"  3. With uniform density alone, ζ_D(s) diverges for all s.")
    print(f"  4. The thermal weight provides the necessary regularization.")
    print(f"{'=' * 70}")
    
    return {
        'zeta_0': zeta_0,
        'zeta_prime_0': zeta_prime_0,
        'log_det': log_det,
        'spectral_density': 'uniform',
        'thermal_weight': 'exponential',
    }


if __name__ == '__main__':
    results = main()
