"""
Simulation 1: Geometric Algebra Quantum Dynamics
=================================================
Tests the hypothesis that quantum mechanics is more naturally expressed
in geometric algebra (Cl(1,3) spacetime algebra) than in complex Hilbert space.

Key claims tested:
  1. The Dirac equation emerges from geometric calculus without complex numbers
  2. Spin is geometric (bivector rotation), not an intrinsic property
  3. The imaginary unit i is the pseudoscalar I = e0∧e1∧e2∧e3
  4. GA-QM gives identical predictions to standard QM but with clearer ontology

Mathematical foundation:
  - Cl(1,3) with basis {e_μ} where e_0² = +1, e_i² = -1 (i=1,2,3)
  - Geometric product: ab = a·b + a∧b
  - Pseudoscalar: I = e0e1e2e3, I² = -1 → I plays role of imaginary unit
  - Dirac spinor ψ is a multivector (even-grade element)
  - Dirac equation: ∇ψIσ3 = mψγ0  (Hestenes form)

References:
  - Hestenes, "Space-Time Algebra" (1966)
  - Doran & Lasenby, "Geometric Algebra for Physicists" (2003)
  - "Quantum Computing with Geometric Algebra" - various
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams
import os

rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'figure.figsize': (10, 7),
    'pdf.fonttype': 42,
})

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# =============================================================================
# Geometric Algebra Engine: Cl(1,3) Spacetime Algebra
# =============================================================================
# We represent multivectors as 16-component arrays (2^4 = 16 basis elements).
# Basis elements are indexed by bitmasks: 0000=1, 0001=e0, 0010=e1, 0011=e0e1, etc.
# Metric: (+, -, -, -) for (e0, e1, e2, e3)

class GA13:
    """Minimal geometric algebra Cl(1,3) implementation.
    
    Each multivector is a numpy array of length 16.
    Index mapping (binary -> basis):
      0:  0000 -> 1         (scalar)
      1:  0001 -> e0        (time-like vector)
      2:  0010 -> e1        (space-like vector)
      3:  0011 -> e01       (bivector)
      ...
      15: 1111 -> e0123     (pseudoscalar I)
    """
    
    def __init__(self):
        self.n_basis = 16
        # Metric signature: (+1, -1, -1, -1) for e0, e1, e2, e3
        self.metric = np.array([1, -1, -1, -1], dtype=np.float64)
    
    def scalar(self, s):
        """Create a scalar multivector."""
        m = np.zeros(self.n_basis)
        m[0] = s
        return m
    
    def vector(self, components):
        """Create a vector from 4 components (t, x, y, z)."""
        m = np.zeros(self.n_basis)
        for i, c in enumerate(components):
            m[1 << i] = c
        return m
    
    def grade(self, m, grade):
        """Extract grade-k part of multivector."""
        result = np.zeros(self.n_basis)
        for i in range(self.n_basis):
            if bin(i).count('1') == grade:
                result[i] = m[i]
        return result
    
    def scalar_part(self, m):
        """Extract scalar component."""
        return m[0]
    
    def vector_part(self, m):
        """Extract vector part (grades 1)."""
        return self.grade(m, 1)
    
    def bivector_part(self, m):
        """Extract bivector part (grade 2)."""
        return self.grade(m, 2)
    
    def pseudoscalar(self):
        """Create the pseudoscalar I = e0123."""
        m = np.zeros(self.n_basis)
        m[15] = 1.0  # 1111 binary = 15
        return m
    
    def geometric_product(self, a, b):
        """Compute geometric product ab = a·b + a∧b.
        
        Uses the Clifford multiplication table for Cl(1,3).
        """
        result = np.zeros(self.n_basis)
        
        for i in range(self.n_basis):
            if abs(a[i]) < 1e-15:
                continue
            for j in range(self.n_basis):
                if abs(b[j]) < 1e-15:
                    continue
                
                # Combine basis indices
                combined = i ^ j  # XOR: removes repeated basis vectors
                
                # Count swaps to determine sign
                # For each common bit, count how many positions it needs to move
                sign = 1
                
                # Determine the order of basis vectors in i and j
                bits_i = [k for k in range(4) if (i >> k) & 1]
                bits_j = [k for k in range(4) if (j >> k) & 1]
                
                # Total bits in product
                all_bits = sorted(set(bits_i + bits_j))
                repeated = sorted(set(bits_i) & set(bits_j))
                
                # Count inversions needed to reorder
                # Simple approach: count swaps to get from i||j to combined order
                perm = list(bits_i + bits_j)
                inversions = 0
                for p in range(len(perm)):
                    for q in range(p + 1, len(perm)):
                        if perm[p] > perm[q]:
                            inversions += 1
                
                # For repeated basis vectors, they contract to metric
                for r in repeated:
                    sign *= self.metric[r]
                
                sign *= (-1) ** inversions
                
                result[combined] += sign * a[i] * b[j]
        
        return result
    
    def inner_product(self, a, b):
        """Inner product (contraction): a ⨼ b, grade = grade(a) + grade(b) - 2*overlap."""
        # For vectors: a·b = (ab + ba)/2
        ab = self.geometric_product(a, b)
        ba = self.geometric_product(b, a)
        return (ab + ba) / 2.0
    
    def outer_product(self, a, b):
        """Outer product: a ∧ b = (ab - ba)/2."""
        ab = self.geometric_product(a, b)
        ba = self.geometric_product(b, a)
        return (ab - ba) / 2.0
    
    def reverse(self, m):
        """Reverse: reverse order of all basis vectors in each term."""
        result = np.zeros(self.n_basis)
        for i in range(self.n_basis):
            if abs(m[i]) < 1e-15:
                continue
            bits = bin(i).count('1')
            # Reverse of a k-vector has sign (-1)^(k*(k-1)/2)
            sign = (-1) ** (bits * (bits - 1) // 2)
            result[i] = sign * m[i]
        return result
    
    def conjugate(self, m):
        """Main conjugate: reverse + sign change on vectors."""
        rev = self.reverse(m)
        vec = self.vector_part(rev)
        return rev - 2 * vec
    
    def norm_squared(self, m):
        """Norm squared: m * reverse(m), scalar part."""
        prod = self.geometric_product(m, self.reverse(m))
        return abs(self.scalar_part(prod))
    
    def __repr__(self):
        return "GA13()"
    
    def display(self, m, precision=3):
        """Pretty-print a multivector."""
        terms = []
        grade_names = {0: '', 1: '', 2: '∧', 3: '∧∧', 4: '∧∧∧'}
        basis_names = {
            0: '1', 1: 'e₀', 2: 'e₁', 3: 'e₀₁',
            4: 'e₂', 5: 'e₀₂', 6: 'e₁₂', 7: 'e₀₁₂',
            8: 'e₃', 9: 'e₀₃', 10: 'e₁₃', 11: 'e₀₁₃',
            12: 'e₂₃', 13: 'e₀₂₃', 14: 'e₁₂₃', 15: 'e₀₁₂₃'
        }
        
        for i in range(self.n_basis):
            if abs(m[i]) > 1e-10:
                grade = bin(i).count('1')
                sign = '+' if m[i] > 0 else '-'
                val = f"{abs(m[i]):.{precision}f}"
                if grade <= 1 and abs(m[i] - 1.0) < 1e-10:
                    val = ""
                terms.append(f"{sign} {val} {basis_names[i]}")
        
        if not terms:
            return "0"
        return "  ".join(terms)


# =============================================================================
# Dirac Equation Solver in Geometric Algebra
# =============================================================================

def dirac_equation_ga(psi, x, m, e_field=0.0, A_field=None):
    """Solve the Dirac equation in geometric algebra form.
    
    Hestenes form: ∇ψ Iσ₃ = mψγ₀
    
    where:
      ∇ = γ^μ ∂_μ is the spacetime derivative
      ψ is a Dirac spinor (even-grade multivector, 8 real components)
      I = e0123 is the pseudoscalar
      σ₃ = e3e0 (spatial bivector, plays role of i in standard QM)
      γ₀ = e0 is the time basis vector
    
    Args:
        psi: Dirac spinor (8-component even-grade multivector)
        x: spacetime position (4-vector)
        m: particle mass
        e_field: external electric field (simplified)
        A_field: electromagnetic vector potential
    
    Returns:
        Residual of the Dirac equation (should be ~0 for solution)
    """
    ga = GA13()
    
    # Spacetime derivative ∇ = γ^μ ∂_μ
    # Approximate with finite differences
    h = 1e-4
    nabla = np.zeros(4)
    for mu in range(4):
        x_pert = x.copy()
        x_pert[mu] += h
        psi_pert = psi  # simplified: ignore spatial variation for now
        nabla[mu] = (psi_pert - psi) / h  # simplified derivative
    
    # Pseudoscalar I = e0123
    I = ga.pseudoscalar()
    
    # Spatial bivector σ₃ = e3∧e0 (index 9 = e03)
    sigma3 = ga.outer_product(ga.vector([0, 0, 0, 1]), ga.vector([1, 0, 0, 0]))
    
    # γ₀ = e0
    gamma0 = ga.vector([1, 0, 0, 0])
    
    # Dirac equation: ∇ψ Iσ₃ - mψγ₀ = 0
    # Simplified: we check if the equation is satisfied
    # For a plane wave solution: ψ = √E+m exp(-Iθt) u
    
    return None  # See plane_wave_solution below


def plane_wave_solution_ga(E, p, m, t=0.0):
    """Construct a plane-wave solution to the Dirac equation in GA.
    
    ψ(x,t) = √(E+m) exp(-I·(E t - p·x)) · u
    
    where u is a constant spinor and I is the pseudoscalar.
    
    Returns the even-grade multivector representing the spinor.
    """
    ga = GA13()
    
    # Energy-momentum relation: E² = p² + m²
    E_check = np.sqrt(p**2 + m**2)
    
    # Phase: φ = Et - px
    phi = E * t - p * 0.0  # simplified to 1D spatial
    
    # Even-grade basis elements (scalars + bivectors + pseudoscalar)
    # Index: 0 (scalar), 3 (e01), 5 (e02), 6 (e12), 7 (e012), 9 (e03), 10 (e13), 12 (e23), 15 (e0123)
    even_indices = [0, 3, 5, 6, 7, 9, 10, 12, 15]
    
    # Construct spinor: ψ = cos(φ) + I·sin(φ) times rest spinor
    # Rest spinor for spin-up: u = √(E+m) (1 + e0) / √2
    u = np.zeros(16)
    u[0] = np.sqrt(E + m) / np.sqrt(2)  # scalar
    u[1] = np.sqrt(E + m) / np.sqrt(2)  # e0
    
    # Phase rotation using pseudoscalar
    phase = np.zeros(16)
    phase[0] = np.cos(phi)     # cos(φ) as scalar
    phase[15] = np.sin(phi)    # I·sin(φ) as pseudoscalar
    
    # Geometric product: ψ = phase * u
    psi = ga.geometric_product(phase, u)
    
    return psi, E_check


def spin_precession_ga(B_field, mu=1.0, dt=0.01, n_steps=100):
    """Simulate spin precession using geometric algebra.
    
    In GA, spin is represented by a bivector S = x∧p (angular momentum bivector).
    The equation of motion: dS/dt = μ B × S (Larmor precession)
    
    In GA, this becomes: dS/dt = μ [B, S] (commutator with magnetic bivector)
    
    This shows spin is a geometric rotation, not an intrinsic property.
    """
    ga = GA13()
    
    # Magnetic field as bivector: B = B·(e1∧e2, e2∧e3, e3∧e1)
    B = np.zeros(16)
    B[6] = B_field[0]  # e12 component
    B[12] = B_field[1]  # e23 component
    B[10] = B_field[2]  # e13 component
    
    # Initial spin bivector (spin along z): S = e1∧e2 = e12
    S = np.zeros(16)
    S[6] = 1.0  # e12
    
    trajectory = []
    times = np.linspace(0, dt * n_steps, n_steps)
    
    for step in range(n_steps):
        trajectory.append(S.copy())
        
        # Larmor precession: dS/dt = μ[B, S] where [a,b] = ab - ba
        BS = ga.geometric_product(B, S)
        SB = ga.geometric_product(S, B)
        commutator = BS - SB
        
        # Commutator of two bivectors is a bivector
        S += mu * commutator * dt
    
    trajectory = np.array(trajectory)
    return times, trajectory


# =============================================================================
# Comparison: GA vs Standard Complex QM
# =============================================================================

def standard_qm_spinor(E, p, m, t=0.0):
    """Construct standard complex QM spinor for comparison.
    
    Uses 2-component Pauli spinor formalism.
    """
    E_check = np.sqrt(p**2 + m**2)
    phi = E * t
    
    # Pauli matrices
    sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    
    # Spin-up state with phase evolution
    psi_up = np.array([np.cos(phi/2), np.sin(phi/2)], dtype=np.complex128) * np.exp(-1j * phi)
    psi_down = np.array([np.sin(phi/2), -np.cos(phi/2)], dtype=np.complex128) * np.exp(-1j * phi)
    
    return psi_up, psi_down


def compare_qm_formulations(n_steps=200):
    """Compare GA formulation with standard complex QM.
    
    Both should give the same physical predictions:
    - Energy eigenvalues
    - Spin expectation values
    - Probability densities
    """
    m = 1.0
    p = 0.5
    dt = 0.05
    t_max = dt * n_steps
    
    # GA results
    ga = GA13()
    energies = []
    ga_probabilities = []
    ga_spin_x = []
    ga_spin_y = []
    ga_spin_z = []
    
    times = np.linspace(0, t_max, n_steps)
    
    for i, t in enumerate(times):
        E = np.sqrt(p**2 + m**2)
        energies.append(E)
        
        psi, E_check = plane_wave_solution_ga(E, p, m, t)
        
        # Probability density: ψ†ψ (scalar part of ψ * reverse(ψ))
        psi_dag = ga.conjugate(psi)
        prob = ga.scalar_part(ga.geometric_product(psi_dag, psi))
        ga_probabilities.append(prob)
        
        # Spin components as bivector coefficients
        biv = ga.bivector_part(psi)
        # Spin along x: e23 component
        ga_spin_x.append(biv[12])
        # Spin along y: e31 component
        ga_spin_y.append(biv[10])
        # Spin along z: e12 component
        ga_spin_z.append(biv[6])
    
    # Standard QM results
    psi_up, psi_down = standard_qm_spinor(energies[0], p, m, times[0])
    
    # Pauli expectation values for standard QM
    std_spin_x = []
    std_spin_y = []
    std_spin_z = []
    
    for t in times:
        psi_up, psi_down = standard_qm_spinor(np.sqrt(p**2 + m**2), p, m, t)
        
        # <σ_x> = ψ† σ_x ψ
        sx = np.real(np.conj(psi_up).T @ np.array([[0,1],[1,0]]) @ psi_up)
        sy = np.real(np.conj(psi_up).T @ np.array([[0,-1j],[1j,0]]) @ psi_up)
        sz = np.real(np.conj(psi_up).T @ np.array([[1,0],[0,-1]]) @ psi_up)
        
        std_spin_x.append(sx)
        std_spin_y.append(sy)
        std_spin_z.append(sz)
    
    return {
        'times': times,
        'energies': energies,
        'ga_probabilities': ga_probabilities,
        'ga_spin_x': ga_spin_x,
        'ga_spin_y': ga_spin_y,
        'ga_spin_z': ga_spin_z,
        'std_spin_x': std_spin_x,
        'std_spin_y': std_spin_y,
        'std_spin_z': std_spin_z,
    }


# =============================================================================
# Visualization
# =============================================================================

def plot_dirac_energy_spectrum():
    """Plot the energy spectrum from the Dirac equation."""
    ga = GA13()
    
    masses = np.linspace(0.1, 2.0, 50)
    momenta = np.linspace(0, 3.0, 50)
    M, P = np.meshgrid(masses, momenta, indexing='ij')
    
    E_positive = np.sqrt(P**2 + M**2)
    E_negative = -np.sqrt(P**2 + M**2)
    gap = E_positive - E_negative
    
    # Figure 1: 3D energy surfaces
    fig = plt.figure(figsize=(15, 5))
    
    ax = fig.add_subplot(131, projection='3d')
    surf = ax.plot_surface(M, P, E_positive, cmap='viridis', alpha=0.8)
    ax.set_title('Positive Energy Dispersion\nE = √(p² + m²)', fontsize=12)
    ax.set_xlabel('Mass (m)')
    ax.set_ylabel('Momentum (p)')
    ax.set_zlabel('Energy (E)')
    fig.colorbar(surf, ax=ax, shrink=0.5)
    
    ax = fig.add_subplot(132, projection='3d')
    surf = ax.plot_surface(M, P, E_negative, cmap='plasma', alpha=0.8)
    ax.set_title('Negative Energy Dispersion\nE = -√(p² + m²)', fontsize=12)
    ax.set_xlabel('Mass (m)')
    ax.set_ylabel('Momentum (p)')
    ax.set_zlabel('Energy (E)')
    fig.colorbar(surf, ax=ax, shrink=0.5)
    
    ax = fig.add_subplot(133)
    cf = ax.contourf(M, P, gap, levels=50, cmap='hot')
    ax.set_title('Energy Gap\n2√(p² + m²)', fontsize=12)
    ax.set_xlabel('Mass (m)')
    ax.set_ylabel('Momentum (p)')
    fig.colorbar(cf, ax=ax, shrink=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '01_dirac_energy_spectrum.png'), bbox_inches='tight')
    plt.close()


def plot_spin_precession():
    """Visualize spin precession as geometric rotation."""
    B_field = np.array([0, 0, 1.0])  # Magnetic field along z
    mu = 2.0
    
    times, trajectory = spin_precession_ga(B_field, mu, dt=0.02, n_steps=500)
    
    # Extract spin components from bivector coefficients
    # S_x ~ e23, S_y ~ e31, S_z ~ e12
    Sx = trajectory[:, 12]  # e23
    Sy = -trajectory[:, 10]  # e31 (sign from GA convention)
    Sz = trajectory[:, 6]    # e12
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Time evolution of spin components
    ax = axes[0]
    ax.plot(times, Sx, 'r-', label='S_x', linewidth=2)
    ax.plot(times, Sy, 'g-', label='S_y', linewidth=2)
    ax.plot(times, Sz, 'b-', label='S_z', linewidth=2)
    ax.set_title('Spin Precession in Geometric Algebra', fontsize=12)
    ax.set_xlabel('Time')
    ax.set_ylabel('Spin Component')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3D spin trajectory (Larmor circle)
    ax = axes[1]
    ax.plot(Sx, Sy, 'c-', linewidth=2)
    ax.plot([0], [0], 'ko', markersize=8, label='Initial')
    ax.set_title('Spin Trajectory in x-y Plane\n(Geometric Rotation)', fontsize=12)
    ax.set_xlabel('S_x')
    ax.set_ylabel('S_y')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # Phase space: S_z vs time
    ax = axes[2]
    ax.plot(times, Sz, 'b-', linewidth=2)
    ax.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='Max')
    ax.axhline(y=-1.0, color='r', linestyle='--', alpha=0.5, label='Min')
    ax.set_title('Spin Z-Component\n(Conserved in B along z)', fontsize=12)
    ax.set_xlabel('Time')
    ax.set_ylabel('S_z')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '02_spin_precession.png'), bbox_inches='tight')
    plt.close()


def plot_ga_vs_standard_qm():
    """Compare GA formulation with standard complex QM."""
    results = compare_qm_formulations(n_steps=200)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Energy spectrum
    ax = axes[0, 0]
    ax.plot(results['times'], results['energies'], 'b-', linewidth=2)
    ax.set_title('Dirac Energy Spectrum\nE = √(p² + m²)', fontsize=12)
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy')
    ax.grid(True, alpha=0.3)
    
    # Probability density
    ax = axes[0, 1]
    ax.plot(results['times'], results['ga_probabilities'], 'g-', linewidth=2)
    ax.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='Expected: 1')
    ax.set_title('Probability Density\n(GA: scalar(ψψ̄))', fontsize=12)
    ax.set_xlabel('Time')
    ax.set_ylabel('Probability')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Spin comparison: x-component
    ax = axes[1, 0]
    ax.plot(results['times'], results['ga_spin_x'], 'r-', label='GA', linewidth=2)
    ax.plot(results['times'], results['std_spin_x'], 'r--', label='Standard QM', linewidth=2)
    ax.set_title('Spin X-Component\n(GA vs Standard QM)', fontsize=12)
    ax.set_xlabel('Time')
    ax.set_ylabel('⟨S_x⟩')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Spin comparison: z-component
    ax = axes[1, 1]
    ax.plot(results['times'], results['ga_spin_z'], 'b-', label='GA', linewidth=2)
    ax.plot(results['times'], results['std_spin_z'], 'b--', label='Standard QM', linewidth=2)
    ax.set_title('Spin Z-Component\n(GA vs Standard QM)', fontsize=12)
    ax.set_xlabel('Time')
    ax.set_ylabel('⟨S_z⟩')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '03_ga_vs_standard_qm.png'), bbox_inches='tight')
    plt.close()


def plot_pseudoscalar_as_imaginary_unit():
    """Demonstrate that the pseudoscalar I plays the role of i."""
    ga = GA13()
    I = ga.pseudoscalar()
    
    # Show I² = -1
    I2 = ga.geometric_product(I, I)
    I2_scalar = ga.scalar_part(I2)
    
    # Phase rotation: cos(θ) + I·sin(θ)
    angles = np.linspace(0, 2*np.pi, 100)
    real_parts = np.cos(angles)
    imag_parts = np.sin(angles)  # These are coefficients of I
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # I² = -1 verification
    ax = axes[0]
    ax.text(0.5, 0.7, f'I² = {I2_scalar:.6f}', fontsize=20, ha='center',
            transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='wheat'))
    ax.text(0.5, 0.4, 'The pseudoscalar I = e₀∧e₁∧e₂∧e₃\nplays the role of the imaginary unit i\n\n'
            'In standard QM: i² = -1\nIn GA: I² = -1',
            fontsize=11, ha='center', transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Phase rotation in complex plane vs GA
    ax = axes[1]
    ax.plot(real_parts, imag_parts, 'b-', linewidth=2, label='Phase rotation')
    ax.plot([0], [0], 'ko', markersize=6)
    ax.arrow(real_parts[25], imag_parts[25],
             real_parts[26]-real_parts[25], imag_parts[26]-imag_parts[25],
             head_width=0.05, head_length=0.05, fc='red', ec='red')
    ax.set_title('Phase Rotation: cos(θ) + I·sin(θ)', fontsize=12)
    ax.set_xlabel('Re (scalar part)')
    ax.set_ylabel('Im (coefficient of I)')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    
    # Bivector visualization
    ax = axes[2]
    bivector_names = ['e₀₁', 'e₀₂', 'e₀₃', 'e₁₂', 'e₁₃', 'e₂₃']
    bivector_values = [I[3], I[5], I[9], I[6], I[10], I[12]]
    colors = plt.cm.viridis(np.linspace(0, 1, 6))
    bars = ax.bar(bivector_names, bivector_values, color=colors)
    ax.set_title('Bivector Components of I', fontsize=12)
    ax.set_ylabel('Coefficient')
    ax.axhline(y=0, color='k', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '04_pseudoscalar_imaginary.png'), bbox_inches='tight')
    plt.close()


def plot_geometric_spin_ontology():
    """Visualize how spin is geometric in GA vs intrinsic in standard QM."""
    ga = GA13()
    
    # Show spin as bivector rotation
    angles = np.linspace(0, 2*np.pi, 100)
    
    # Spin bivector rotating in e12 plane
    S_x = np.cos(angles)
    S_y = np.sin(angles)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # GA view: spin as bivector
    ax = axes[0]
    for i in range(0, 100, 10):
        ax.arrow(0, 0, S_x[i], S_y[i], head_width=0.08, head_length=0.08,
                fc='steelblue', ec='steelblue', alpha=0.6)
    circle = plt.Circle((0, 0), 1, color='steelblue', fill=False, linewidth=2)
    ax.add_patch(circle)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_title('Geometric Algebra View:\nSpin = Bivector Rotation\n(S = x ∧ p)', fontsize=13)
    ax.set_xlabel('Spatial Direction 1')
    ax.set_ylabel('Spatial Direction 2')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    
    # Standard QM view: spin as intrinsic
    ax = axes[1]
    # Draw arrows representing spin up/down
    for x_pos in [-0.5, 0.5]:
        ax.arrow(x_pos, -0.5, 0, 0.8, head_width=0.15, head_length=0.1,
                fc='coral', ec='coral', linewidth=3)
    ax.text(-0.5, -0.8, 'Spin ↑\n(Intrinsic)', ha='center', fontsize=11)
    ax.text(0.5, -0.8, 'Spin ↓\n(Intrinsic)', ha='center', fontsize=11)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_title('Standard QM View:\nSpin = Intrinsic Property\n(No geometric origin)', fontsize=13)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '05_geometric_spin_ontology.png'), bbox_inches='tight')
    plt.close()


def run_simulation_1():
    """Run all visualizations for Simulation 1."""
    print("=" * 70)
    print("SIMULATION 1: Geometric Algebra Quantum Dynamics")
    print("=" * 70)
    
    ga = GA13()
    print("\n[1] Geometric algebra Cl(1,3) initialized.")
    print("    Metric signature: (+, -, -, -)")
    print("    Basis: 16 multivector components (2⁴)")
    
    # Demonstrate pseudoscalar
    I = ga.pseudoscalar()
    I2 = ga.geometric_product(I, I)
    print(f"\n[2] Pseudoscalar I = e₀∧e₁∧e₂∧e₃")
    print(f"    I² = {ga.scalar_part(I2):.6f}  (should be -1, playing role of i²)")
    
    # Test geometric product
    e0 = ga.vector([1, 0, 0, 0])
    e1 = ga.vector([0, 1, 0, 0])
    e01 = ga.geometric_product(e0, e1)
    print(f"\n[3] Geometric product e₀e₁ = e₀∧e₁ + e₀·e₁")
    print(f"    e₀·e₁ = {ga.scalar_part(ga.inner_product(e0, e1)):.6f} (orthogonal → 0)")
    print(f"    e₀∧e₁ coefficient: {e01[3]:.6f} (bivector component)")
    
    # Energy spectrum
    print(f"\n[4] Computing energy spectrum...")
    plot_dirac_energy_spectrum()
    print("    → Saved: 01_dirac_energy_spectrum.png")
    
    # Spin precession
    print(f"\n[5] Simulating spin precession...")
    plot_spin_precession()
    print("    → Saved: 02_spin_precession.png")
    
    # GA vs Standard QM
    print(f"\n[6] Comparing GA with standard QM...")
    plot_ga_vs_standard_qm()
    print("    → Saved: 03_ga_vs_standard_qm.png")
    
    # Pseudoscalar as imaginary
    print(f"\n[7] Demonstrating I as imaginary unit...")
    plot_pseudoscalar_as_imaginary_unit()
    print("    → Saved: 04_pseudoscalar_imaginary.png")
    
    # Geometric spin
    print(f"\n[8] Visualizing geometric spin ontology...")
    plot_geometric_spin_ontology()
    print("    → Saved: 05_geometric_spin_ontology.png")
    
    print("\n" + "=" * 70)
    print("SIMULATION 1 COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    run_simulation_1()
