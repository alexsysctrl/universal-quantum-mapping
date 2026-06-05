# Modular Clifford Category: Replication Package

**Date:** 2026-06-04
**Purpose:** All simulation code, instructions, dependencies, and expected outputs for reproducing MCC results.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Dependencies](#2-dependencies)
3. [Installation](#3-installation)
4. [Simulation 1: Modular Dirac Operator Spectrum](#4-simulation-1-modular-dirac-operator-spectrum)
5. [Simulation 2: Fisher-Rao Metric and Curvature](#5-simulation-2-fisher-rao-metric-and-curvature)
6. [Simulation 3: q-Deformed Clifford Algebra](#6-simulation-3-q-deformed-clifford-algebra)
7. [Simulation 4: Anyon Braiding from Modular Dirac Operator](#7-simulation-4-anyon-braiding-from-modular-dirac-operator)
8. [Simulation 5: Modular Zeta Function](#8-simulation-5-modular-zeta-function)
9. [Verification Scripts](#9-verification-scripts)
10. [Expected Outputs](#10-expected-outputs)

---

## 1. Overview

This replication package contains 5 simulations that test core predictions of the Modular Clifford Category (MCC) framework. Each simulation is self-contained, with its own Python script, input parameters, and expected output.

### What Each Simulation Tests

| # | Simulation | MCC Result Tested | Confidence Level |
|---|-----------|-------------------|-----------------|
| 1 | Modular Dirac Operator Spectrum | Continuous spectrum for Type III_1 | HIGH |
| 2 | Fisher-Rao Metric and Curvature | Negative curvature of state space | MEDIUM |
| 3 | q-Deformed Clifford Algebra | Hopf algebra structure | MEDIUM |
| 4 | Anyon Braiding from D_ω | Braiding matrix = exp(iπD_ω/Λ) | HIGH |
| 5 | Modular Zeta Function | Zeta function regularization | MEDIUM |

---

## 2. Dependencies

```
Python >= 3.9
numpy >= 1.24
scipy >= 1.10
matplotlib >= 3.7
sympy >= 1.12
```

### Installation

```bash
pip install numpy scipy matplotlib sympy
```

### Verification

```bash
python -c "import numpy; import scipy; import matplotlib; import sympy; print('All dependencies OK')"
```

---

## 3. Installation

```bash
# Clone or copy this directory to your workspace
mkdir -p ./mcc-replication
cp -r replication-package/* ./mcc-replication/
cd ./mcc-replication

# Install dependencies
pip install numpy scipy matplotlib sympy

# Run all simulations
python run_all_simulations.py
```

---

## 4. Simulation 1: Modular Dirac Operator Spectrum

**Tests:** The spectral theory of D_ω for Type III_1 factors (continuous spectrum).

**MCC Reference:** Session 2, Section 1.1; Session 3, Section 3.1

### 4.1 What This Simulates

A finite-dimensional approximation of a Type III_1 factor. We construct a modular operator with continuous spectrum and compute the spectrum of the modular Dirac operator D_ω = I^(-1) log Δ_ω.

### 4.2 Code

See `simulation_1_spectrum.py` in this directory.

### 4.3 Expected Output

- A plot showing the eigenvalues of D_ω distributed continuously on ℝ (not discrete).
- A histogram of eigenvalues showing uniform (Lebesgue) spectral density.
- Confirmation that the spectral TYPE is continuous, consistent with Type III_1.

### 4.4 Verification

Run: `python simulation_1_spectrum.py`

Expected output file: `output/spectrum_plot.png` (eigenvalue distribution plot)

The eigenvalue distribution should show:
- No gaps in the spectrum (continuous)
- Approximately uniform density (Lebesgue measure)
- Symmetric about zero (if I² = -1)

---

## 5. Simulation 2: Fisher-Rao Metric and Curvature

**Tests:** Negative curvature of the state space with respect to the Fisher-Rao metric.

**MCC Reference:** Session 3, Section 3.1-3.3

### 5.1 What This Simulates

We compute the Fisher-Rao metric and sectional curvature for a family of quantum states (qubits and qutrits). We verify that the curvature is negative, consistent with the MCC prediction.

### 5.2 Code

See `simulation_2_curvature.py` in this directory.

### 5.3 Expected Output

- A plot showing the Fisher-Rao metric tensor for various states.
- A plot showing the sectional curvature as a function of the state.
- Confirmation that the curvature is negative for generic states.

### 5.4 Verification

Run: `python simulation_2_curvature.py`

Expected output file: `output/curvature_plot.png` (curvature vs. state plot)

The curvature should be:
- Negative for generic states (non-commuting with K)
- Zero for states that commute with K (modular-invariant states)
- More negative for states farther from equilibrium

---

## 6. Simulation 3: q-Deformed Clifford Algebra

**Tests:** The q-deformed Clifford algebra Cl_q(p,q) as a braided Hopf algebra.

**MCC Reference:** Session 3, Section 2.1-2.6

### 6.1 What This Simulates

We construct the q-deformed Clifford algebra for small p, q and verify:
1. The q-deformed anti-commutation relation: e_i e_j + q^(-1) e_j e_i = 2g_ij
2. The Hopf algebra coproduct: Δ(e_i) = e_i ⊗ 1 + K_i ⊗ e_i
3. The R-matrix and braiding

### 6.2 Code

See `simulation_3_qdeformed.py` in this directory.

### 6.3 Expected Output

- A table showing the multiplication table of Cl_q(p,q) for q ≠ 1.
- A plot showing how the algebra structure changes as q → 1.
- Verification that the coproduct preserves the q-deformed relations (in the braided category).

### 6.4 Verification

Run: `python simulation_3_qdeformed.py`

Expected output file: `output/qdeformed_table.png` (multiplication table visualization)

The output should show:
- For q = 1: Standard Clifford algebra multiplication table.
- For q ≠ 1: Deformed multiplication table with q-dependent coefficients.
- As q → 1: Smooth recovery of the standard Clifford algebra.

---

## 7. Simulation 4: Anyon Braiding from Modular Dirac Operator

**Tests:** The braiding matrix B_ab = exp(iπ D_ω/Λ) for anyon modules.

**MCC Reference:** Session 3, Section 5.1-5.5

### 7.1 What This Simulates

We construct an anyon module for SU(2)_k Chern-Simons theory and compute the braiding matrix from the modular Dirac operator. We verify that the braiding phases match the expected anyonic statistics.

### 7.2 Code

See `simulation_4_anyons.py` in this directory.

### 7.3 Expected Output

- A table showing the braiding matrix B_ab for different anyon types.
- A plot showing the braiding phases as a function of the Chern-Simons level k.
- Verification that the fusion rules match SU(2)_k.

### 7.4 Verification

Run: `python simulation_4_anyons.py`

Expected output file: `output/braiding_plot.png` (braiding phases vs. k plot)

The output should show:
- Braiding phases matching exp(2πi(h_c - h_a - h_b)) for SU(2)_k.
- Fusion rules matching the SU(2)_k fusion rules.
- Topological entropy S_top = log(D) matching the predicted formula.

---

## 8. Simulation 5: Modular Zeta Function

**Tests:** The modular zeta function for continuous spectrum.

**MCC Reference:** Session 2, Section 1.5; Session 2, Addendum E

### 8.1 What This Simulates

We compute the modular zeta function ζ_D(s) = ∫ dμ ρ(μ) |μ|^(-s) for various spectral densities ρ(μ). We verify the analytic continuation and the regularized determinant.

### 8.2 Code

See `simulation_5_zeta.py` in this directory.

### 8.3 Expected Output

- A plot showing ζ_D(s) as a function of s (real part).
- A plot showing the pole structure of ζ_D(s).
- The regularized determinant log det(D_ω) = -ζ_D'(0).

### 8.4 Verification

Run: `python simulation_5_zeta.py`

Expected output file: `output/zeta_plot.png` (zeta function plot)

The output should show:
- ζ_D(s) with poles at s = 1, 2, 3, ... (from the Gamma function).
- The regularized determinant ζ_D'(0) as a finite number.
- Agreement with the analytic formula ζ_D(s) = 2C·(2π)^(s-1)·Γ(1-s) for the thermal weight case.

---

## 9. Verification Scripts

### 9.1 run_all_simulations.py

Runs all 5 simulations in sequence and checks that the outputs match expected results.

```bash
python run_all_simulations.py
```

### 9.2 verify_results.py

Checks that each simulation produced the expected output files and that the numerical results are within tolerance.

```bash
python verify_results.py
```

### 9.3 check_dependencies.py

Verifies that all required Python packages are installed with correct versions.

```bash
python check_dependencies.py
```

---

## 10. Expected Outputs

After running all simulations, you should have the following output files in the `output/` directory:

| File | Description | Size |
|------|-------------|------|
| `spectrum_plot.png` | Eigenvalue distribution of D_ω | ~100 KB |
| `curvature_plot.png` | Sectional curvature vs. state | ~100 KB |
| `qdeformed_table.png` | Multiplication table of Cl_q(p,q) | ~100 KB |
| `braiding_plot.png` | Braiding phases vs. k | ~100 KB |
| `zeta_plot.png` | Zeta function ζ_D(s) | ~100 KB |
| `simulation_log.txt` | Log of all simulation runs | ~10 KB |

### Success Criteria

All simulations pass if:
1. Each simulation completes without errors.
2. Each output file is created and has non-zero size.
3. The numerical results are within tolerance of the expected values (see tolerance settings in each script).
4. The verification script reports all checks as PASSED.

---

## Troubleshooting

### Common Issues

1. **Import errors:** Make sure all dependencies are installed (`pip install numpy scipy matplotlib sympy`).

2. **Memory errors:** If simulations run out of memory, reduce the dimension of the Hilbert space (change `N` in the script parameters).

3. **Numerical instability:** For large k in the anyon simulation, use higher precision (`mpmath` instead of `numpy`).

4. **Plot rendering:** If matplotlib fails to create plots, install a backend: `pip install PyQt5` or `pip install tk`.

---

## References

1. Session 2, Section 1.1-1.5: Spectral theory of D_ω
2. Session 3, Section 3.1-3.3: Fisher-Rao metric and curvature
3. Session 3, Section 2.1-2.6: q-deformed Clifford algebras
4. Session 3, Section 5.1-5.5: Anyon modules
5. Session 2, Addendum E: Modular zeta function

---

*End of replication package.*
