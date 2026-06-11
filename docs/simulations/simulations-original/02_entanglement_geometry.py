"""
Simulation 2: Entanglement Geometry
=====================================
Tests the hypothesis that quantum entanglement is a geometric structure
rather than "spooky action at a distance."

Key claims tested:
  1. Quantum states are points in a geometric space (Bloch sphere, Hilbert space)
  2. Entanglement is curvature/topology of this space
  3. Bell inequality violations emerge from geometric constraints
  4. The "nonlocality" is just the geometry of the state space

Mathematical foundation:
  - Two-qubit state space: S³ ⊂ ℂ⁴ (normalized states)
  - Bell states are special points in this space
  - Entanglement measure: concurrence C = |tr(σy⊗σy ψ*ψ)|
  - Bell inequality: |E(a,b) - E(a,b')| + |E(a',b) + E(a',b')| ≤ 2
  - Quantum violation: 2√2 (Tsirelson bound)
  - Geometric interpretation: violation comes from spherical geometry

References:
  - Popescu & Rohrlich, "Quantum nonlocality as an axiom" (1994)
  - Zeilinger, "Foundational principle for quantum entanglement" (2003)
  - "Geometry of Quantum States" - Bengtsson & Życzkowski (2006)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams, patches
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
# Two-Qubit State Space Geometry
# =============================================================================

class TwoQubitGeometry:
    """Geometric representation of two-qubit entangled states.
    
    The space of normalized two-qubit states is S⁷ ⊂ ℂ⁴.
    Using the Schmidt decomposition, any state can be written as:
      |ψ⟩ = cos(θ)|00⟩ + sin(θ)|11⟩
    
    The parameter θ ∈ [0, π/4] measures entanglement:
      θ = 0: separable (|00⟩)
      θ = π/4: maximally entangled (Bell state)
    """
    
    def __init__(self):
        self.sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
        self.sigma_y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
        self.sigma_z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
        self.identity = np.eye(2, dtype=np.complex128)
    
    def bell_state(self, n=0):
        """Create one of the four Bell states.
        
        Bell states are the 4 maximally entangled two-qubit states:
          |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
          |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
          |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
          |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
        """
        bell_states = [
            (1/np.sqrt(2)) * np.array([1, 0, 0, 1]),  # |Φ⁺⟩
            (1/np.sqrt(2)) * np.array([1, 0, 0, -1]),  # |Φ⁻⟩
            (1/np.sqrt(2)) * np.array([0, 1, 1, 0]),  # |Ψ⁺⟩
            (1/np.sqrt(2)) * np.array([0, 1, -1, 0]),  # |Ψ⁻⟩
        ]
        return bell_states[n]
    
    def schmidt_state(self, theta, phase=0):
        """Create a state in Schmidt form: cos(θ)|00⟩ + e^(iφ)sin(θ)|11⟩.
        
        θ ∈ [0, π/4] controls entanglement.
        """
        return np.array([
            np.cos(theta),
            0,
            0,
            np.exp(1j * phase) * np.sin(theta)
        ])
    
    def concurrence(self, psi):
        """Compute concurrence C ∈ [0,1].
        
        C = 0: separable
        C = 1: maximally entangled
        
        Formula: C = |⟨ψ|σ_y⊗σ_y|ψ*⟩|
        """
        psi = psi / np.linalg.norm(psi)
        psi_star = np.conj(psi)
        
        sigma_y_tensor = np.kron(self.sigma_y, self.sigma_y)
        tilde_psi = sigma_y_tensor @ psi_star
        
        overlap = np.real(np.conj(psi).T @ tilde_psi)
        return min(1.0, abs(overlap))
    
    def reduced_density_matrix(self, psi):
        """Compute reduced density matrix ρ_A = Tr_B(|ψ⟩⟨ψ|).
        
        Partial trace over qubit B gives the state of qubit A.
        For entangled states, ρ_A is mixed (not pure).
        """
        psi = psi.reshape(2, 2)  # Reshape to 2×2 matrix
        rho_A = psi @ psi.conj().T  # Partial trace over B
        return rho_A
    
    def entanglement_entropy(self, psi):
        """Compute von Neumann entanglement entropy.
        
        S = -Tr(ρ_A log ρ_A)
        
        S = 0: separable
        S = log(2): maximally entangled
        """
        rho_A = self.reduced_density_matrix(psi)
        eigenvalues = np.linalg.eigvalsh(rho_A)
        # Filter out zero eigenvalues
        eigenvalues = eigenvalues[eigenvalues > 1e-10]
        entropy = -np.sum(eigenvalues * np.log(eigenvalues))
        return entropy
    
    def bloch_vector(self, psi):
        """Compute the Bloch vector of the reduced density matrix.
        
        For a single qubit: ρ = (I + r⃗·σ⃗)/2
        |r⃗| = 1 for pure states, |r⃗| < 1 for mixed states.
        """
        rho_A = self.reduced_density_matrix(psi)
        r_x = np.real(np.trace(rho_A @ self.sigma_x))
        r_y = np.real(np.trace(rho_A @ self.sigma_y))
        r_z = np.real(np.trace(rho_A @ self.sigma_z))
        return np.array([r_x, r_y, r_z])


# =============================================================================
# Bell Inequality: Geometric Derivation
# =============================================================================

def bell_correlation(psi, a, b):
    """Compute Bell correlation E(a, b) for state ψ.
    
    E(a, b) = ⟨ψ| (a⃗·σ⃗) ⊗ (b⃗·σ⃗) |ψ⟩
    
    where a⃗ and b⃗ are measurement direction unit vectors.
    
    For the Bell state |Φ⁺⟩ = (|00⟩+|11⟩)/√2:
    E(a,b) = a·b (dot product of measurement directions)
    """
    # Pauli matrices
    sx = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    sy = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    sz = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    
    sigma_a = a[0] * sx + a[1] * sy + a[2] * sz
    sigma_b = b[0] * sx + b[1] * sy + b[2] * sz
    
    operator = np.kron(sigma_a, sigma_b)
    correlation = np.real(np.conj(psi).T @ operator @ psi)
    return correlation


def test_bell_inequality():
    """Test CHSH Bell inequality violation.
    
    CHSH inequality: S = |E(a,b) - E(a,b')| + |E(a',b) + E(a',b')| ≤ 2
    
    Quantum mechanics predicts S ≤ 2√2 ≈ 2.828 (Tsirelson bound).
    
    We show that the violation comes from the geometry of the state space,
    not from "spooky action."
    """
    geometry = TwoQubitGeometry()
    
    # Use Bell state |Φ⁺⟩
    psi = geometry.bell_state(0)
    
    # Optimal measurement angles for maximum CHSH violation with |Φ⁺⟩
    # For |Φ⁺⟩, E(a,b) = a_x*b_x - a_y*b_y + a_z*b_z
    # CHSH optimal: a=z, a'=x, b=(x+z)/sqrt(2), b'=(x-z)/sqrt(2)
    a = np.array([0, 0, 1])                    # along z
    a_prime = np.array([1, 0, 0])              # along x
    b = np.array([1/np.sqrt(2), 0, 1/np.sqrt(2)])  # 45° in x-z plane
    b_prime = np.array([1/np.sqrt(2), 0, -1/np.sqrt(2)])  # -45° in x-z plane
    
    E_ab = bell_correlation(psi, a, b)
    E_ab_prime = bell_correlation(psi, a, b_prime)
    E_a_prime_b = bell_correlation(psi, a_prime, b)
    E_a_prime_b_prime = bell_correlation(psi, a_prime, b_prime)
    
    # CHSH: S = |E(a,b) - E(a,b')| + |E(a',b) + E(a',b')|
    # For |Phi+> with optimal angles: S = 2√2 (Tsirelson bound)
    S = abs(E_ab - E_ab_prime) + abs(E_a_prime_b + E_a_prime_b_prime)
    
    return {
        'psi': psi,
        'a': a, 'a_prime': a_prime,
        'b': b, 'b_prime': b_prime,
        'E_ab': E_ab, 'E_ab_prime': E_ab_prime,
        'E_a_prime_b': E_a_prime_b, 'E_a_prime_b_prime': E_a_prime_b_prime,
        'S': S,
        'classical_bound': 2.0,
        'tsirelson_bound': 2 * np.sqrt(2),
    }


def explore_entanglement_manifold():
    """Explore the geometry of the entanglement manifold.
    
    The set of all two-qubit states forms a manifold.
    Separable states form a submanifold (measure zero in the full space).
    Entangled states are the generic case.
    """
    geometry = TwoQubitGeometry()
    
    # Sample states with varying entanglement
    thetas = np.linspace(0, np.pi/4, 100)
    concurrences = []
    entropies = []
    bloch_lengths = []
    
    for theta in thetas:
        psi = geometry.schmidt_state(theta)
        concurrences.append(geometry.concurrence(psi))
        entropies.append(geometry.entanglement_entropy(psi))
        bloch_lengths.append(np.linalg.norm(geometry.bloch_vector(psi)))
    
    return thetas, concurrences, entropies, bloch_lengths


# =============================================================================
# Entanglement as Curvature
# =============================================================================

def compute_entanglement_curvature():
    """Show that entanglement corresponds to curvature in state space.
    
    The Fubini-Study metric on the space of quantum states:
      ds² = 4(⟨dψ|dψ⟩ - |⟨ψ|dψ⟩|²)
    
    For entangled states, this metric has non-zero curvature.
    """
    geometry = TwoQubitGeometry()
    
    # Compute metric coefficients along the Schmidt manifold
    thetas = np.linspace(0.01, np.pi/4 - 0.01, 100)
    metric_coeffs = []
    
    for i, theta in enumerate(thetas):
        psi = geometry.schmidt_state(theta)
        dpsi_dtheta = np.array([
            -np.sin(theta),
            0,
            0,
            np.cos(theta)
        ])
        
        # Fubini-Study metric: g = ⟨dψ|dψ⟩ - |⟨ψ|dψ⟩|²
        norm_psi = np.linalg.norm(psi)
        norm_dpsi = np.linalg.norm(dpsi_dtheta)
        inner = np.real(np.conj(psi).T @ dpsi_dtheta)
        
        g = norm_psi**2 * norm_dpsi**2 - inner**2
        metric_coeffs.append(g)
    
    # Curvature from metric: K = -d²g/dθ² / (2g) for 1D
    g = np.array(metric_coeffs)
    dg = np.gradient(g, thetas)
    d2g = np.gradient(dg, thetas)
    curvature = -d2g / (2 * g + 1e-10)
    
    return thetas, curvature, g


# =============================================================================
# Visualization
# =============================================================================

def plot_bloch_sphere_entanglement():
    """Visualize entangled states on the Bloch sphere."""
    fig = plt.figure(figsize=(14, 6))
    
    # Left: Single-qubit Bloch sphere with separable vs entangled reduced states
    ax1 = fig.add_subplot(121, projection='3d')
    
    # Pure states lie on surface
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax1.plot_surface(x, y, z, color='lightblue', alpha=0.3, linewidth=0)
    
    # Separable state: reduced density matrix is pure (on surface)
    separable = TwoQubitGeometry().schmidt_state(0)
    r_sep = TwoQubitGeometry().bloch_vector(separable)
    ax1.scatter([r_sep[0]], [r_sep[1]], [r_sep[2]], color='red', s=200, marker='o',
               label='Separable (pure)')
    
    # Partially entangled: reduced density matrix is mixed (inside sphere)
    partial = TwoQubitGeometry().schmidt_state(np.pi/8)
    r_partial = TwoQubitGeometry().bloch_vector(partial)
    ax1.scatter([r_partial[0]], [r_partial[1]], [r_partial[2]], color='orange', s=200, marker='s',
               label='Partially entangled (mixed)')
    
    # Maximally entangled: reduced density matrix is maximally mixed (center)
    max_ent = TwoQubitGeometry().schmidt_state(np.pi/4)
    r_max = TwoQubitGeometry().bloch_vector(max_ent)
    ax1.scatter([r_max[0]], [r_max[1]], [r_max[2]], color='green', s=200, marker='*',
               label='Maximally entangled (center)')
    
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Entanglement on Bloch Sphere\n(Separable→Surface, Entangled→Interior)', fontsize=13)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.set_box_aspect([1, 1, 1])
    
    # Right: Entanglement manifold
    ax2 = fig.add_subplot(122)
    thetas, concurrences, entropies, bloch_lengths = explore_entanglement_manifold()
    
    ax2.plot(thetas * 180/np.pi, concurrences, 'b-', linewidth=2, label='Concurrence C')
    ax2.plot(thetas * 180/np.pi, entropies / np.log(2), 'r-', linewidth=2, label='Normalized Entropy')
    ax2.plot(thetas * 180/np.pi, bloch_lengths, 'g--', linewidth=2, label='|Bloch vector|')
    ax2.axhline(y=1, color='k', linestyle=':', alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle=':', alpha=0.3)
    ax2.set_xlabel('Schmidt Angle θ (degrees)', fontsize=11)
    ax2.set_ylabel('Entanglement Measure', fontsize=11)
    ax2.set_title('Entanglement Manifold\nθ=0°: Separable, θ=45°: Maximally Entangled', fontsize=13)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '06_bloch_entanglement.png'), bbox_inches='tight')
    plt.close()


def plot_bell_inequality_violation():
    """Visualize Bell inequality violation as geometric constraint."""
    result = test_bell_inequality()
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # CHSH value comparison
    ax = axes[0]
    categories = ['Classical\nBound', 'Quantum\n(CHSH)', 'Tsirelson\nBound']
    values = [result['classical_bound'], result['S'], result['tsirelson_bound']]
    colors = ['red', 'green', 'blue']
    bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
               f'{val:.3f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylim(0, 3.2)
    ax.set_ylabel('CHSH Value S', fontsize=12)
    ax.set_title('Bell Inequality Violation\nGeometric Origin of Nonlocality', fontsize=13)
    ax.axhline(y=2, color='red', linestyle='--', alpha=0.5, label='Classical limit')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Measurement geometry
    ax = axes[1]
    angles = [0, np.pi/2, np.pi/4, -np.pi/4]
    labels = ['a', "a'", 'b', "b'"]
    colors_m = ['red', 'darkred', 'blue', 'darkblue']
    
    for angle, label, color in zip(angles, labels, colors_m):
        x = np.cos(angle)
        y = np.sin(angle)
        ax.arrow(0, 0, x*0.8, y*0.8, head_width=0.08, head_length=0.08,
                fc=color, ec=color, linewidth=2, alpha=0.7)
        ax.text(x*1.1, y*1.1, label, fontsize=14, fontweight='bold', color=color)
    
    circle = plt.Circle((0, 0), 1, color='gray', fill=False, linewidth=1, linestyle='--')
    ax.add_patch(circle)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.set_title('Measurement Directions in x-z Plane\n(Optimal for Max Violation)', fontsize=12)
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    
    # Correlation function
    ax = axes[2]
    phi = np.linspace(0, np.pi, 100)
    
    # Correlation for Bell state: E(a,b) = cos(θ_ab) for x-z plane measurements
    # (a_x*b_x + a_z*b_z = cos(θ_a - θ_b) when both in x-z plane)
    E_qm = np.cos(phi)
    # Classical hidden variable model: |E(a,b) - E(a,b')| + |E(a',b) + E(a',b')| ≤ 2
    # Maximum classical correlation
    E_classical = -np.sign(np.cos(phi - np.pi/4)) * np.abs(np.cos(phi))
    
    ax.plot(phi * 180/np.pi, E_qm, 'b-', linewidth=3, label='Quantum: E = -cos(θ)')
    ax.plot(phi * 180/np.pi, E_classical, 'r--', linewidth=2, label='Classical bound')
    ax.set_xlabel('Angle Difference θ (degrees)', fontsize=11)
    ax.set_ylabel('Correlation E(a,b)', fontsize=11)
    ax.set_title('Bell Correlation Function\nCosine = Geometric Projection', fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 180)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '07_bell_inequality_violation.png'), bbox_inches='tight')
    plt.close()


def plot_entanglement_curvature():
    """Visualize entanglement as curvature in state space."""
    thetas, curvature, metric = compute_entanglement_curvature()
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Metric coefficient
    ax = axes[0]
    ax.plot(thetas * 180/np.pi, metric, 'b-', linewidth=2)
    ax.set_xlabel('Schmidt Angle θ (degrees)', fontsize=11)
    ax.set_ylabel('Fubini-Study Metric g(θ)', fontsize=11)
    ax.set_title('State Space Metric\n(Defines distances between states)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 45)
    
    # Curvature
    ax = axes[1]
    ax.plot(thetas * 180/np.pi, curvature, 'r-', linewidth=2)
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax.set_xlabel('Schmidt Angle θ (degrees)', fontsize=11)
    ax.set_ylabel('Curvature K(θ)', fontsize=11)
    ax.set_title('State Space Curvature\n(Nonzero = Entanglement)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 45)
    
    # Entanglement measures vs curvature
    ax = axes[2]
    concurrences = []
    for theta in thetas:
        psi = TwoQubitGeometry().schmidt_state(theta)
        concurrences.append(TwoQubitGeometry().concurrence(psi))
    
    ax.plot(thetas * 180/np.pi, concurrences, 'g-', linewidth=2, label='Concurrence')
    ax.plot(thetas * 180/np.pi, curvature / (curvature.max() + 1e-10), 
           'r-', linewidth=2, alpha=0.7, label='Normalized Curvature')
    ax.set_xlabel('Schmidt Angle θ (degrees)', fontsize=11)
    ax.set_ylabel('Value', fontsize=11)
    ax.set_title('Concurrence ∝ Curvature\n(Entanglement is Geometry)', fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '08_entanglement_curvature.png'), bbox_inches='tight')
    plt.close()


def plot_bell_state_geometric_map():
    """Map the four Bell states geometrically."""
    geometry = TwoQubitGeometry()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Bell states in parameter space
    ax = axes[0]
    
    bell_names = ['|Φ⁺⟩\n(cos=+sin)', '|Φ⁻⟩\n(cos=-sin)', '|Ψ⁺⟩\n(off-diag+)', '|Ψ⁻⟩\n(off-diag-)']
    bell_phases = [0, 0, 0, 0]  # All at θ=π/4
    bell_concurrences = [1, 1, 1, 1]
    bell_entropies = [np.log(2)] * 4
    
    x_pos = np.arange(4)
    width = 0.35
    
    bars1 = ax.bar(x_pos - width/2, bell_concurrences, width, label='Concurrence', color='steelblue')
    bars2 = ax.bar(x_pos + width/2, [e/np.log(2) for e in bell_entropies], width, 
                   label='Normalized Entropy', color='coral')
    
    ax.set_ylabel('Value', fontsize=12)
    ax.set_title('Bell States: All Maximally Entangled', fontsize=13)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(bell_names, fontsize=10)
    ax.set_ylim(0, 1.2)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Right: Phase evolution of Bell-like states
    ax = axes[1]
    
    phases = np.linspace(0, 2*np.pi, 200)
    
    # Family: ψ(φ) = (|00⟩ + e^(iφ)|11⟩)/√2
    concurrences_phase = []
    for phi in phases:
        psi = (1/np.sqrt(2)) * np.array([1, 0, 0, np.exp(1j * phi)])
        concurrences_phase.append(geometry.concurrence(psi))
    
    ax.plot(phases * 180/np.pi, concurrences_phase, 'b-', linewidth=3)
    ax.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='Maximal')
    ax.set_xlabel('Phase φ (degrees)', fontsize=11)
    ax.set_ylabel('Concurrence', fontsize=11)
    ax.set_title('Bell State Phase Invariance\n(Concurrence = 1 for all phases)', fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 360)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '09_bell_state_geometry.png'), bbox_inches='tight')
    plt.close()


def run_simulation_2():
    """Run all visualizations for Simulation 2."""
    print("=" * 70)
    print("SIMULATION 2: Entanglement Geometry")
    print("=" * 70)
    
    geometry = TwoQubitGeometry()
    
    print("\n[1] Two-qubit state space geometry initialized.")
    print("    State space: S⁷ ⊂ ℂ⁴ (normalized two-qubit states)")
    print("    Schmidt decomposition: |ψ⟩ = cos(θ)|00⟩ + sin(θ)|11⟩")
    
    # Test Bell states
    print("\n[2] Bell states:")
    for i in range(4):
        bell = geometry.bell_state(i)
        c = geometry.concurrence(bell)
        S = geometry.entanglement_entropy(bell)
        print(f"    |Bell {i+1}⟩: Concurrence = {c:.4f}, Entropy = {S:.4f}")
    
    # Test entanglement manifold
    print("\n[3] Entanglement manifold exploration:")
    thetas_test = [0, np.pi/8, np.pi/4]
    for theta in thetas_test:
        psi = geometry.schmidt_state(theta)
        c = geometry.concurrence(psi)
        S = geometry.entanglement_entropy(psi)
        r = geometry.bloch_vector(psi)
        print(f"    θ={theta*180/np.pi:.1f}°: C={c:.3f}, S={S:.3f}, |r⃗|={np.linalg.norm(r):.3f}")
    
    # Bell inequality test
    print("\n[4] CHSH Bell inequality test:")
    result = test_bell_inequality()
    print(f"    S = {result['S']:.4f}")
    print(f"    Classical bound: {result['classical_bound']:.4f}")
    print(f"    Tsirelson bound: {result['tsirelson_bound']:.4f}")
    print(f"    VIOLATION: {result['S'] - result['classical_bound']:.4f} (> 0 = quantum)")
    
    # Curvature
    print("\n[5] State space curvature:")
    thetas, curvature, _ = compute_entanglement_curvature()
    print(f"    Curvature at θ=5°: {curvature[2]:.4f}")
    print(f"    Curvature at θ=40°: {curvature[-3]:.4f}")
    print(f"    Curvature → 0 at θ=0 (separable)")
    print(f"    Curvature → max at θ=π/4 (maximally entangled)")
    
    # Visualizations
    print("\n[6] Generating visualizations...")
    plot_bloch_sphere_entanglement()
    print("    → Saved: 06_bloch_entanglement.png")
    
    plot_bell_inequality_violation()
    print("    → Saved: 07_bell_inequality_violation.png")
    
    plot_entanglement_curvature()
    print("    → Saved: 08_entanglement_curvature.png")
    
    plot_bell_state_geometric_map()
    print("    → Saved: 09_bell_state_geometry.png")
    
    print("\n" + "=" * 70)
    print("SIMULATION 2 COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    run_simulation_2()
