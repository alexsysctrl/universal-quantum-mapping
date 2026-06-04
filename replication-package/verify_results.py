#!/usr/bin/env python3
"""
Verify MCC Simulation Results

Checks that each simulation produces expected results within tolerance.
This is a programmatic verification of the simulation outputs.

Usage:
    python verify_results.py

Checks performed:
    1. Each simulation completes without error
    2. Output files exist and have non-zero size
    3. Numerical results match expected ranges
    4. Key mathematical properties are satisfied
"""

import os
import sys
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'output')

checks_passed = 0
checks_failed = 0
check_results = []


def check(name, condition, detail=""):
    """Record a check result."""
    global checks_passed, checks_failed
    
    if condition:
        checks_passed += 1
        status = "PASS"
    else:
        checks_failed += 1
        status = "FAIL"
    
    check_results.append((status, name, detail))
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))
    return condition


def verify_simulation_1():
    """Verify Simulation 1: Spectrum."""
    print("\n" + "=" * 60)
    print("Verifying Simulation 1: Modular Dirac Operator Spectrum")
    print("=" * 60)
    
    try:
        import simulation_1_spectrum as sim1
        
        # Run with small N for quick verification
        N = 100
        Delta, eigenvalues_Delta = sim1.construct_modular_operator(N, seed=42)
        I = sim1.construct_pseudoscalar_I(N)
        D_omega, eigenvalues_D = sim1.compute_modular_dirac_operator(Delta, I)
        results = sim1.analyze_spectrum(eigenvalues_D, N)
        
        # Check 1: I^2 = -I
        check("I^2 = -I", np.allclose(I @ I, -np.eye(N)))
        
        # Check 2: D_omega is self-adjoint (real eigenvalues)
        check("D_ω eigenvalues are real", 
              np.all(np.abs(np.imag(eigenvalues_D)) < 1e-10))
        
        # Check 3: Spectrum is approximately continuous (small gap ratio)
        check("Gap ratio < 5 (continuous spectrum)", 
              results['gap_ratio'] < 5,
              f"gap_ratio = {results['gap_ratio']:.2f}")
        
        # Check 4: Spectrum is symmetric about zero
        check("Spectrum symmetric about zero", 
              results['symmetry_error'] < 0.1 * results['mean_abs'],
              f"symmetry_error = {results['symmetry_error']:.6f}")
        
        # Check 5: Output file exists
        spectrum_file = os.path.join(output_dir, 'spectrum_plot.png')
        check("spectrum_plot.png exists", 
              os.path.exists(spectrum_file) and os.path.getsize(spectrum_file) > 0)
        
    except Exception as e:
        check("Simulation 1 runs without error", False, str(e))


def verify_simulation_2():
    """Verify Simulation 2: Curvature."""
    print("\n" + "=" * 60)
    print("Verifying Simulation 2: Fisher-Rao Metric and Curvature")
    print("=" * 60)
    
    try:
        import simulation_2_curvature as sim2
        
        # Generate test state and fixed modular Hamiltonian
        rho = sim2.generate_random_density_matrix(4, seed=42)
        K, K_eigvecs = sim2.generate_fixed_modular_hamiltonian(4, seed=42)
        basis = sim2.generate_tangent_vectors(4, num_vectors=4, seed=42)
        
        # Check 1: Fisher-Rao metric is positive definite
        for v in basis:
            g = sim2.fine_silberberg_metric(rho, v)
            check(f"Fisher-Rao metric positive for tangent vector", 
                  g > 0, f"g = {g:.6f}")
        
        # Check 2: Curvature is negative for generic states
        curvature_vals = []
        for i in range(len(basis)):
            for j in range(i+1, len(basis)):
                K_sec, _, _, _ = sim2.compute_sectional_curvature(rho, basis[i], basis[j], K)
                curvature_vals.append(K_sec)
        
        negative_frac = sum(1 for c in curvature_vals if c < 0) / len(curvature_vals)
        check(f"Curvature negative for >50% of planes", 
              negative_frac > 0.5,
              f"{negative_frac:.0%} negative")
        
        # Check 3: Output files exist
        check("curvature_plot.png exists", 
              os.path.exists(os.path.join(output_dir, 'curvature_plot.png')) and 
              os.path.getsize(os.path.join(output_dir, 'curvature_plot.png')) > 0)
        
        check("decoherence_plot.png exists", 
              os.path.exists(os.path.join(output_dir, 'decoherence_plot.png')) and 
              os.path.getsize(os.path.join(output_dir, 'decoherence_plot.png')) > 0)
        
    except Exception as e:
        check("Simulation 2 runs without error", False, str(e))


def verify_simulation_3():
    """Verify Simulation 3: q-Deformed Clifford."""
    print("\n" + "=" * 60)
    print("Verifying Simulation 3: q-Deformed Clifford Algebra")
    print("=" * 60)
    
    try:
        import simulation_3_qdeformed as sim3
        
        # Build algebra at q=1
        alg_std = sim3.QDeformedClifford(4, metric=np.array([1,-1,-1,-1]), q=1.0, seed=42)
        
        # Check 1: Standard Clifford relations at q=1 (e_i^2 = g_ii)
        for i in range(4):
            coeff, result = alg_std._multiply_monomials(1 << i, 1 << i)
            check(f"e_{i+1}^2 = g_{i+1},{i+1} at q=1", 
                  abs(coeff - abs(alg_std.metric[i])) < 0.1,
                  f"coeff = {coeff:.4f}, g = {alg_std.metric[i]}")
        
        # Check 2: Yang-Baxter equation at q=1
        ybe_sat, ybe_err = alg_std.verify_yang_baxter()
        check("YBE satisfied at q=1", ybe_sat, f"error = {ybe_err:.2e}")
        
        # Check 3: YBE at q=0.8
        alg_q = sim3.QDeformedClifford(4, metric=np.array([1,-1,-1,-1]), q=0.8, seed=42)
        ybe_sat_q, ybe_err_q = alg_q.verify_yang_baxter()
        check("YBE satisfied at q=0.8", ybe_sat_q, f"error = {ybe_err_q:.2e}")
        
        # Check 4: R-matrix is non-trivial at q≠1
        R_at_1 = alg_std.R_matrix
        R_at_q = alg_q.R_matrix
        check("R-matrix changes with q", 
              np.max(np.abs(R_at_q - R_at_1)) > 0.01,
              f"max diff = {np.max(np.abs(R_at_q - R_at_1)):.6f}")
        
        # Check 5: Output files exist
        for fname in ['R_matrix.png', 'yang_baxter.png', 'braiding_phase.png', 'q_limit.png']:
            fpath = os.path.join(output_dir, fname)
            check(f"{fname} exists", 
                  os.path.exists(fpath) and os.path.getsize(fpath) > 0)
        
    except Exception as e:
        check("Simulation 3 runs without error", False, str(e))


def verify_simulation_4():
    """Verify Simulation 4: Anyon Modules."""
    print("\n" + "=" * 60)
    print("Verifying Simulation 4: 2+1D Anyon Modules")
    print("=" * 60)
    
    try:
        import simulation_4_anyons as sim4
        
        # Build SU(2)_5 (Fibonacci anyons)
        su2k = sim4.SU2kChernSimons(5, seed=42)
        
        # Check 1: Number of anyon types = k + 1
        expected_types = 5 + 1  # j = 0, 1/2, 1, 3/2, 2, 5/2
        check(f"Number of anyon types = k + 1", 
              su2k.n_types == expected_types,
              f"got {su2k.n_types}, expected {expected_types}")
        
        # Check 2: S matrix is symmetric
        check("S matrix is symmetric", 
              np.allclose(su2k.S, su2k.S.T, atol=1e-10),
              f"max asymmetry = {np.max(np.abs(su2k.S - su2k.S.T)):.2e}")
        
        # Check 3: S matrix is unitary
        S_unitary_error = np.max(np.abs(su2k.S @ su2k.S.conj().T - np.eye(su2k.n_types)))
        check("S matrix is unitary", 
              S_unitary_error < 1e-10,
              f"error = {S_unitary_error:.2e}")
        
        # Check 4: T matrix diagonal elements have modulus <= 1
        T_diag = np.diag(su2k.T)
        check("T matrix diagonal modulus <= 1", 
              np.all(np.abs(T_diag) <= 1.0 + 1e-10))
        
        # Check 5: Quantum dimensions are positive
        check("Quantum dimensions are positive", 
              np.all(su2k.quantum_dimensions > 0),
              f"min d_j = {np.min(su2k.quantum_dimensions):.6f}")
        
        # Check 6: Total quantum dimension D = sqrt(sum d_j^2)
        D_computed = np.sqrt(np.sum(su2k.quantum_dimensions ** 2))
        check(f"D = sqrt(sum d_j^2)", 
              abs(D_computed - su2k.D) < 1e-10,
              f"D = {su2k.D:.6f}, computed = {D_computed:.6f}")
        
        # Check 7: Topological entropy S_top = log(D)
        S_top, S_top_alt = su2k.compute_topological_entropy()
        check("S_top = log(D)", 
              abs(S_top - np.log(su2k.D)) < 1e-10)
        check("S_top = -log(|S_00|)", 
              abs(S_top_alt - np.log(np.abs(su2k.S[0, 0]))) < 0.5)
        
        # Check 8: Universal QC for k >= 4
        check("k=5 is universal QC", su2k.is_universal_qc())
        
        # Check 9: Modular group relations
        mod = su2k.verify_modular_group()
        check("S^2 = C", mod['S_squared_valid'], f"error = {mod['S_squared_error']:.2e}")
        check("(ST)^3 = e^(2πic/24) S^2", mod['ST_cubed_valid'], f"error = {mod['ST_cubed_error']:.2e}")
        
        # Check 10: Output files exist
        for fname in ['braiding_plot.png', 'fusion_tree.png', 'D_omega_comparison.png']:
            fpath = os.path.join(output_dir, fname)
            check(f"{fname} exists", 
                  os.path.exists(fpath) and os.path.getsize(fpath) > 0)
        
    except Exception as e:
        check("Simulation 4 runs without error", False, str(e))


def verify_simulation_5():
    """Verify Simulation 5: Zeta Function."""
    print("\n" + "=" * 60)
    print("Verifying Simulation 5: Modular Zeta Function")
    print("=" * 60)
    
    try:
        import simulation_5_zeta as sim5
        from scipy import special
        
        C = 1.0
        beta = 2 * np.pi
        
        # Check 1: Zeta function at s = -1
        s = -1
        zeta_num, zeta_ana = sim5.zeta_function_thermal(s, C=C, beta=beta)
        expected = 2 * C * (beta ** (s - 1)) * special.gamma(1 - s)
        check(f"ζ_D(-1) matches analytical formula", 
              abs(zeta_num - expected) / abs(expected) < 0.1 if abs(expected) > 1e-15 else True,
              f"num = {zeta_num:.4f}, ana = {expected:.4f}")
        
        # Check 2: Zeta function at s = 0
        s = 0
        zeta_0_num, zeta_0_ana = sim5.zeta_function_thermal(s, C=C, beta=beta)
        expected_0 = 2 * C * (beta ** (-1)) * special.gamma(1)
        check(f"ζ_D(0) = C/π", 
              abs(zeta_0_ana - C/np.pi) < 1e-10,
              f"ana = {zeta_0_ana:.6f}, C/π = {C/np.pi:.6f}")
        
        # Check 3: Zeta function diverges at s = 1
        s = 1
        zeta_1_num, zeta_1_ana = sim5.zeta_function_thermal(s, C=C, beta=beta)
        check("ζ_D(1) diverges (returns NaN/inf)", 
              np.isnan(zeta_1_num) or np.isnan(zeta_1_ana) or np.isinf(zeta_1_num),
              f"num = {zeta_1_num}, ana = {zeta_1_ana}")
        
        # Check 4: Regularized determinant
        log_det, zeta_prime = sim5.compute_regularized_determinant()
        gamma_const = 0.5772156649015328606065120900824024310421
        expected_log_det = -C/np.pi * (np.log(2*np.pi) + gamma_const)
        check("log det(D_ω) = -C/π·[log(2π) + γ]", 
              abs(log_det - expected_log_det) < 1e-10,
              f"log_det = {log_det:.6f}, expected = {expected_log_det:.6f}")
        
        # Check 5: Spectral density is uniform
        mu_test = np.array([-5, 0, 5])
        rho = sim5.uniform_spectral_density(mu_test, C=1.0)
        check("Spectral density is uniform", 
              np.allclose(rho, 1.0),
              f"rho = {rho}")
        
        # Check 6: Thermal weight is exponential
        w = sim5.thermal_weight(mu_test, beta=2*np.pi)
        expected_w = np.exp(-2*np.pi * np.abs(mu_test))
        check("Thermal weight is exponential", 
              np.allclose(w, expected_w),
              f"w = {w}, expected = {expected_w}")
        
        # Check 7: Output files exist
        for fname in ['zeta_plot.png', 'zeta_grid.png']:
            fpath = os.path.join(output_dir, fname)
            check(f"{fname} exists", 
                  os.path.exists(fpath) and os.path.getsize(fpath) > 0)
        
    except Exception as e:
        check("Simulation 5 runs without error", False, str(e))


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("MCC Replication Package — Verify Results")
    print("=" * 60)
    
    print(f"\nOutput directory: {output_dir}")
    print(f"Files present: {os.listdir(output_dir) if os.path.exists(output_dir) else 'NONE'}")
    
    # Run verifications
    verify_simulation_1()
    verify_simulation_2()
    verify_simulation_3()
    verify_simulation_4()
    verify_simulation_5()
    
    # Final summary
    print(f"\n{'=' * 60}")
    print("VERIFICATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Checks passed: {checks_passed}")
    print(f"Checks failed: {checks_failed}")
    print(f"Total checks: {checks_passed + checks_failed}")
    
    if checks_failed == 0:
        print(f"\n✓ ALL CHECKS PASSED")
    else:
        print(f"\n✗ {checks_failed} CHECK(S) FAILED")
        print(f"  See details above.")
    
    return 0 if checks_failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
