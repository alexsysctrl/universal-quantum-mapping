# Universal Quantum Mapping Simulations

Six computational simulations testing novel hypotheses about quantum structure. Each simulation implements a different theoretical framework and produces visualizations showing how the theory explains quantum phenomena.

## Overview

| # | Simulation | Core Hypothesis | Key Equation |
|---|-----------|----------------|--------------|
| 1 | Geometric Algebra QD | Spin is geometric, not intrinsic | `∇ψIσ₃ = mψγ₀` (Dirac in GA) |
| 2 | Entanglement Geometry | Entanglement = curvature of state space | `S = -Tr(ρ log ρ)` (entanglement entropy) |
| 3 | Information-Theoretic QM | QM is the unique theory satisfying info principles | `p=2` (fixed point in theory space) |
| 4 | Emergent Spacetime | Spacetime geometry from entanglement | `S_A = Area(γ_A) / 4G_N` (Ryu-Takayanagi) |
| 5 | Thermal Time | Time flow emerges from statistical state | `σ_t(A) = e^{itK} A e^{-itK}` (modular group) |
| 6 | Quantum-Classical Boundary | Classical physics from decoherence | `Γ ∝ g²` (decoherence rate) |

## Files

```
simulations/
├── README.md                          # This file
├── 01_geometric_algebra_quantum.py    # Dirac equation in geometric algebra
├── 02_entanglement_geometry.py        # Entanglement as state space geometry
├── 03_information_theoretic_derivation.py  # QM from information principles
├── 04_emergent_spacetime.py           # Spacetime from tensor networks
├── 05_thermal_time.py                 # Time from modular automorphism
├── 06_quantum_classical_boundary.py   # Decoherence and classical emergence
└── figures/                           # Generated visualizations
    ├── 01_dirac_energy_spectrum.png
    ├── 02_spin_precession.png
    ├── 03_ga_vs_standard_qm.png
    ├── 04_pseudoscalar_imaginary.png
    ├── 05_geometric_spin_ontology.png
    ├── 06_bloch_entanglement.png
    ├── 07_bell_inequality_violation.png
    ├── 08_entanglement_curvature.png
    ├── 09_bell_state_geometry.png
    ├── 10_information_causality.png
    ├── 11_no_cloning_comparison.png
    ├── 12_qm_fixed_point.png
    ├── 13_mps_entanglement.png
    ├── 14_spacetime_tearing.png
    ├── 15_holographic_entanglement.png
    ├── 16_er_epr_relation.png
    ├── 17_thermal_time_evolution.png
    ├── 18_kms_condition.png
    ├── 19_entropy_time_arrow.png
    ├── 20_connes_rovelli_conceptual.png
    ├── 21_decoherence_dynamics.png
    ├── 22_pointer_states.png
    ├── 23_decoherence_rate_scaling.png
    ├── 24_density_matrix_evolution.png
    └── 25_quantum_classical_transition.png
```

## Requirements

```bash
pip install numpy matplotlib scipy
```

## Running

```bash
python 01_geometric_algebra_quantum.py
python 02_entanglement_geometry.py
python 03_information_theoretic_derivation.py
python 04_emergent_spacetime.py
python 05_thermal_time.py
python 06_quantum_classical_boundary.py
```

Each simulation generates 3-5 figure files and prints analysis to stdout.

## Simulation Details

### 1. Geometric Algebra Quantum Dynamics

Tests whether quantum mechanics is more naturally expressed in geometric algebra (Cl(1,3) spacetime algebra) than complex Hilbert space.

**Key findings:**
- The pseudoscalar I = e₀∧e₁∧e₂∧e₃ satisfies I² = -1, playing the role of the imaginary unit
- Spin emerges as a bivector rotation (S = x∧p), not an intrinsic property
- The Dirac equation `∇ψIσ₃ = mψγ₀` gives identical predictions to standard QM
- Spin precession is visualized as geometric rotation in the e₁₂ plane

**Equations implemented:**
- Geometric product: `ab = a·b + a∧b`
- Dirac equation (Hestenes form): `∇ψIσ₃ = mψγ₀`
- Spin bivector: `S = x∧p`
- Larmor precession: `dS/dt = μ[B, S]`

### 2. Entanglement Geometry

Models entanglement as geometric structure in the state space rather than "spooky action."

**Key findings:**
- Bell states are special points in the S⁷ state space
- Entanglement = curvature of the Fubini-Study metric on state space
- Bell inequality violation emerges from spherical geometry (cosine correlations)
- The Bloch sphere interior represents mixed (entangled) reduced states

**Equations implemented:**
- Schmidt decomposition: `|ψ⟩ = cos(θ)|00⟩ + sin(θ)|11⟩`
- Concurrence: `C = |⟨ψ|σ_y⊗σ_y|ψ*⟩|`
- CHSH inequality: `S = |E(a,b) - E(a,b')| + |E(a',b) + E(a',b')| ≤ 2`
- Tsirelson bound: `S ≤ 2√2`
- Fubini-Study metric: `ds² = 4(⟨dψ|dψ⟩ - |⟨ψ|dψ⟩|²)`

### 3. Information-Theoretic Derivation

Tests whether quantum mechanics is the UNIQUE theory consistent with information principles.

**Key findings:**
- Classical theory (p=1): perfect cloning, no entanglement
- Quantum theory (p=2): no-cloning (F=5/6), information causality satisfied
- Box-world (p=∞): violates information causality, allows super-quantum correlations
- Only p=2 satisfies ALL information principles simultaneously → QM is a fixed point

**Principles tested:**
- Information causality: `I ≤ m` (communication bits)
- No-cloning: `F < 1` (no perfect copying)
- Local discriminability: composite states from local measurements
- Purification: mixed states have unique purifications

### 4. Emergent Spacetime from Entanglement

Tests the Van Raamsdonk hypothesis: spacetime geometry emerges from quantum entanglement.

**Key findings:**
- MPS entanglement entropy scales with bond dimension: `S ∝ log(χ)`
- Cutting entanglement bonds "tears" emergent spacetime (entropy drops to 0)
- Holographic entanglement: `S_boundary ≈ S_bulk`
- Ryu-Takayanagi: `S_A ∝ Area(γ_A)` (boundary area ∝ entanglement)
- ER=EPR: `d(i,j) ∝ -log(E(i,j))` (distance from entanglement)

**Frameworks implemented:**
- Matrix Product States (MPS) for 1D
- Projected Entangled Pair States (PEPS) for 2D
- Ryu-Takayanagi formula
- Entanglement-distance relation

### 5. Time from Thermal Time

Tests the Connes-Rovelli thermal time hypothesis: time flow emerges from statistical state.

**Key findings:**
- Modular Hamiltonian `K = -log(ρ)` generates time evolution
- Different states → different time flows (no absolute time)
- KMS condition: `ω(A σ_{iβ}(B)) = ω(BA)` characterizes thermal equilibrium
- Low entropy → fast time flow; high entropy → slow time flow
- Maximum entropy (equilibrium) → no time flow (static)

**Equations implemented:**
- Modular group: `σ_t(A) = e^{itK} A e^{-itK}` where `K = -log(ρ)`
- KMS condition: `ω(A σ_{iβ}(B)) = ω(BA)`
- Thermal time: `τ = βt`
- Von Neumann entropy: `S = -Tr(ρ log ρ)`

### 6. Quantum-Classical Boundary

Models where classical physics emerges from quantum mechanics through decoherence.

**Key findings:**
- Decoherence rate: `Γ ∝ g²` (scales with coupling strength squared)
- Pointer states (|0⟩, |1⟩) survive decoherence; superpositions decay
- Density matrix evolves from pure (coherent) to mixed (classical)
- Wigner function interference fringes fade → classical probability distribution
- Quantum-to-classical transition is continuous, parameterized by `g × √n_env`

**Models implemented:**
- Dephasing (phase damping): `H_int = g σ_z ⊗ B`
- Dissipative (energy exchange): `H_int = g(σ_- ⊗ B^+ + σ_+ ⊗ B)`
- Caldeira-Leggett bath
- Pointer state selection (Zurek's einselection)

## Analysis Summary

### What Each Simulation Reveals

**1. Geometric Algebra:** Quantum mechanics doesn't need complex numbers. The imaginary unit is a geometric object (pseudoscalar). Spin is not mysterious — it's a bivector rotation. This suggests the "weirdness" of QM partly comes from using the wrong mathematical language.

**2. Entanglement Geometry:** "Spooky action" is just geometry. Bell violations come from the spherical structure of state space, not nonlocal causation. Entanglement is curvature — a local property of the state manifold.

**3. Information-Theoretic QM:** Quantum mechanics isn't arbitrary. It's the UNIQUE theory satisfying basic information principles. This suggests QM is forced on us by the nature of information itself.

**4. Emergent Spacetime:** Space and time are not fundamental. They emerge from quantum entanglement patterns. Cutting entanglement "tears" spacetime. This supports the holographic principle and ER=EPR.

**5. Thermal Time:** Time is not a fundamental ingredient of physics. It emerges from the statistical state of the system. Different states experience different time flows. This resolves the "problem of time" in quantum gravity.

**6. Quantum-Classical Boundary:** Classical physics emerges naturally from quantum mechanics through environmental interaction. The boundary is continuous, not sharp. Pointer states are selected by the environment (einselection).

### Common Themes

1. **Geometry is fundamental**: GA spin, entanglement curvature, tensor network geometry, entanglement-distance relation
2. **Emergence**: Spacetime from entanglement, time from state, classical from quantum
3. **Information**: QM as fixed point of information principles, entropy as time driver
4. **No "spooky" action**: All nonlocality explained geometrically or statistically

### Limitations

- Finite-dimensional approximations (true QFT requires infinite dimensions)
- Simplified environments (real environments have many more degrees of freedom)
- Numerical precision limits for large tensor networks
- No experimental verification (these are theoretical investigations)

## References

1. Hestenes, "Space-Time Algebra" (1966)
2. Doran & Lasenby, "Geometric Algebra for Physicists" (2003)
3. Van Raamsdonk, "Building up spacetime with quantum entanglement" (2010)
4. Connes & Rovelli, "Von Neumann algebra automorphisms and time" (1994)
5. Chiribella et al., "Informational derivation of QM" (2011)
6. Zurek, "Decoherence, einselection, and the quantum origins of the classical" (2003)
7. Ryu & Takayanagi, "Holographic derivation of entanglement entropy" (2006)
8. Schlosshauer, "Decoherence and the Quantum-to-Classical Transition" (2007)
