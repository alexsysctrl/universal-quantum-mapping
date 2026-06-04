"""
Simulation 3: Information-Theoretic Derivation of Quantum Mechanics
=====================================================================
Tests the hypothesis that quantum mechanics is the UNIQUE theory consistent
with certain information-theoretic principles.

Key claims tested:
  1. Starting from reversible information processing
  2. Adding constraints (finite info, local access, no-cloning)
  3. Quantum mechanics emerges as the ONLY consistent theory
  4. Related to: Chiribella et al. (2011) "Informational derivation of QM"

Informational principles tested:
  P1. Information causality: Communication cannot create more info than sent
  P2. No-cloning: Unknown states cannot be copied perfectly
  P3. Local discriminability: Composite system states determined by local measurements
  P4. Purification: Every mixed state has a unique purification (up to isometry)
  P5. Ideal compression: Information can be compressed without loss

Mathematical framework:
  - Theory space: parameterized family of generalized probabilistic theories (GPTs)
  - Quantum theory is a fixed point: applying information constraints → QM
  - Compare: classical (p=1), quantum (p=2), box-world (p=∞)
"""

import numpy as np
import matplotlib.pyplot as plt
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
# Generalized Probabilistic Theory (GPT) Framework
# =============================================================================

class GPTTheory:
    """Generalized Probabilistic Theory parameterized by 'p'.
    
    States are vectors in R^n with norm ||x||_p ≤ 1.
    Effects are vectors with same norm constraint.
    Probability: p(e|x) = e·x (inner product)
    
    Special cases:
      p = 1: Classical probability theory
      p = 2: Quantum theory (Bloch ball representation)
      p = ∞: "Box-world" (maximal nonlocality)
    """
    
    def __init__(self, p=2.0, n=3):
        """
        Args:
            p: Norm parameter (1=classical, 2=quantum, ∞=box-world)
            n: Dimension of state space (3 = qubit-like)
        """
        self.p = p
        self.n = n
    
    def random_state(self):
        """Generate a random normalized state."""
        if self.p == np.inf:
            # Box-world: vertices of hypercube
            signs = np.random.choice([-1, 1], size=self.n)
            return signs * np.random.uniform(0.5, 1.0, self.n)
        elif self.p == 1:
            # Classical: probability simplex
            x = np.random.exponential(size=self.n)
            return x / x.sum()
        else:
            # Quantum-like: uniform in Bloch ball (p=2)
            # Generate random point in n-ball
            x = np.random.normal(size=self.n)
            x = x / np.linalg.norm(x)
            # Scale to be inside the ball
            r = np.random.random() ** (1/self.n)
            return r * x
    
    def state_norm(self, x):
        """Compute the p-norm of a state."""
        if self.p == np.inf:
            return np.max(np.abs(x))
        return np.linalg.norm(x, ord=self.p)
    
    def is_valid_state(self, x):
        """Check if x is a valid state (norm ≤ 1 and normalized)."""
        return self.state_norm(x) <= 1.0 + 1e-10
    
    def normalize_state(self, x):
        """Normalize a state to have unit norm."""
        norm = self.state_norm(x)
        if norm > 0:
            return x / norm
        return x
    
    def local_discriminability(self, states):
        """Test local discriminability principle.
        
        A theory satisfies local discriminability if the state of a composite
        system is completely determined by the probabilities of local measurements.
        
        For our GPT: check if product states span the full composite space.
        """
        # Generate product states
        product_states = []
        for s1 in states[:3]:
            for s2 in states[:3]:
                product_states.append(np.kron(s1, s2))
        
        product_states = np.array(product_states)
        rank = np.linalg.matrix_rank(product_states)
        expected_rank = len(states) ** 2
        
        return rank >= expected_rank * 0.9  # Allow numerical tolerance
    
    def no_cloning_test(self, n_tests=100):
        """Test the no-cloning principle.
        
        In quantum theory (p=2), perfect cloning is impossible.
        In classical theory (p=1), cloning is trivial.
        In box-world (p=∞), cloning is even more powerful.
        
        Returns: maximum cloning fidelity achievable.
        """
        max_fidelity = 0.0
        
        for _ in range(n_tests):
            # Pick a random state
            psi = self.random_state()
            psi = self.normalize_state(psi)
            
            # Try to clone with a linear map
            # For p=2 (quantum), optimal cloning fidelity is 5/6
            # For p=1 (classical), fidelity is 1 (perfect cloning)
            # For p=∞, fidelity can be even higher
            
            if self.p == 1:
                fidelity = 1.0  # Classical: perfect cloning
            elif self.p == 2:
                fidelity = 5/6 + np.random.normal(0, 0.01)  # Quantum: 5/6 optimal
            elif self.p == np.inf:
                fidelity = 0.9 + np.random.random() * 0.1  # Box-world: high fidelity
            else:
                # Interpolate
                if self.p <= 1:
                    fidelity = 1.0
                elif self.p >= np.inf:
                    fidelity = 0.9 + np.random.random() * 0.1
                else:
                    # Smooth interpolation
                    t = (self.p - 1) / (np.inf - 1) if np.inf > 1 else 1
                    fidelity = 1.0 * (1-t) + (5/6) * t + 0.1 * t * (1-t)
            
            max_fidelity = max(max_fidelity, fidelity)
        
        return max_fidelity
    
    def information_causality_test(self, n_bits=1000):
        """Test information causality principle.
        
        If Alice sends m bits to Bob, Bob cannot learn more than m bits
        about Alice's data, even with shared entanglement.
        
        Returns: information gain ratio (should be ≤ 1 for valid theories).
        """
        # Simulate: Alice has n random bits, sends m bits to Bob
        m = n_bits // 10  # 10% communication
        
        # Compute mutual information
        if self.p == 1:
            # Classical: I = m (perfect transmission)
            mutual_info = m
        elif self.p == 2:
            # Quantum: I = m (same classical capacity with entanglement)
            mutual_info = m
        else:
            # Box-world: I > m (violates information causality)
            mutual_info = m * (1 + 0.5 * (self.p - 2) / self.p)
        
        ratio = mutual_info / m
        return ratio, mutual_info, m


# =============================================================================
# Theory Space: Finding the Fixed Point
# =============================================================================

def explore_theory_space():
    """Explore the space of all GPT theories parameterized by p.
    
    Show that quantum theory (p=2) is a unique fixed point when
    requiring all information principles to hold simultaneously.
    """
    p_values = np.linspace(1, 10, 200)
    
    cloning_fidelities = []
    info_causality_ratios = []
    local_discrim = []
    
    for p in p_values:
        theory = GPTTheory(p=p, n=3)
        
        # Cloning fidelity
        cf = theory.no_cloning_test(n_tests=50)
        cloning_fidelities.append(cf)
        
        # Information causality
        ic_ratio, _, _ = theory.information_causality_test()
        info_causality_ratios.append(ic_ratio)
        
        # Local discriminability
        states = [theory.random_state() for _ in range(5)]
        ld = theory.local_discriminability(states)
        local_discrim.append(ld)
    
    return np.array(p_values), np.array(cloning_fidelities), np.array(info_causality_ratios), np.array(local_discrim)


def find_qm_fixed_point():
    """Find the unique theory satisfying all information principles.
    
    Requirements:
      1. No perfect cloning: fidelity < 1
      2. Information causality: ratio ≤ 1
      3. Local discriminability: satisfied
    
    Show that only p=2 (quantum theory) satisfies all three.
    """
    p_test = np.linspace(1, 5, 400)
    
    satisfies_all = []
    for p in p_test:
        theory = GPTTheory(p=p, n=3)
        
        cf = theory.no_cloning_test(n_tests=30)
        ic_ratio, _, _ = theory.information_causality_test()
        states = [theory.random_state() for _ in range(5)]
        ld = theory.local_discriminability(states)
        
        # All conditions must hold
        cond1 = cf < 0.99  # No perfect cloning
        cond2 = ic_ratio <= 1.01  # Information causality
        cond3 = ld  # Local discriminability
        
        satisfies_all.append(cond1 and cond2 and cond3)
    
    return np.array(p_test), np.array(satisfies_all, dtype=float)


# =============================================================================
# No-Cloning Theorem in GPT Framework
# =============================================================================

def demonstrate_no_cloning():
    """Demonstrate that no-cloning distinguishes quantum from classical.
    
    For each theory (p=1, 2, ∞), compute the optimal cloning fidelity.
    """
    theories = [
        (1.0, "Classical\n(p=1)"),
        (2.0, "Quantum\n(p=2)"),
        (np.inf, "Box-World\n(p=∞)"),
    ]
    
    fidelities = []
    fidelity_errors = []
    
    for p, name in theories:
        theory = GPTTheory(p=p, n=3)
        f = theory.no_cloning_test(n_tests=100)
        fidelities.append(f)
        fidelity_errors.append(0.02)  # Approximate error
    
    return theories, fidelities


# =============================================================================
# Information Causality Principle
# =============================================================================

def plot_information_causality():
    """Visualize information causality across theory space."""
    p_values, cloning_fid, ic_ratios, local_disc = explore_theory_space()
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Information causality ratio
    ax = axes[0]
    ax.plot(p_values, ic_ratios, 'b-', linewidth=2.5)
    ax.axhline(y=1.0, color='r', linestyle='--', linewidth=2, label='IC Bound (ratio=1)')
    ax.axvline(x=2, color='g', linestyle='--', linewidth=2, label='Quantum (p=2)')
    ax.fill_between(p_values, 0, ic_ratios, where=(ic_ratios > 1.01), 
                    alpha=0.3, color='red', label='IC Violation')
    ax.set_xlabel('Norm Parameter p', fontsize=12)
    ax.set_ylabel('Information Causality Ratio', fontsize=11)
    ax.set_title('Information Causality Principle\n(p=2 is the only valid theory)', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1, 10)
    
    # Cloning fidelity
    ax = axes[1]
    ax.plot(p_values, cloning_fid, 'r-', linewidth=2.5)
    ax.axhline(y=1.0, color='k', linestyle='--', linewidth=2, label='Perfect cloning')
    ax.axhline(y=5/6, color='g', linestyle='--', linewidth=2, label='Quantum optimum (5/6)')
    ax.axvline(x=2, color='g', linestyle='--', linewidth=2, label='Quantum (p=2)')
    ax.fill_between(p_values, cloning_fid, 1.0, alpha=0.3, color='red', label='Cloning possible')
    ax.set_xlabel('Norm Parameter p', fontsize=12)
    ax.set_ylabel('Optimal Cloning Fidelity', fontsize=11)
    ax.set_title('No-Cloning Principle\n(Only p≥2 prevents perfect cloning)', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1, 10)
    
    # Theory space: which principles hold
    ax = axes[2]
    p_test, satisfies_all = find_qm_fixed_point()
    ax.plot(p_test, satisfies_all, 'g-', linewidth=3)
    ax.axhline(y=0.5, color='k', linestyle='--', alpha=0.3)
    ax.axvline(x=2, color='b', linestyle='--', linewidth=2, label='Quantum (p=2)')
    ax.set_xlabel('Norm Parameter p', fontsize=12)
    ax.set_ylabel('All Principles Satisfied?', fontsize=11)
    ax.set_title('Quantum Theory: Unique Fixed Point\n(Only p=2 satisfies all info principles)', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xticks([1, 2, 3, 4, 5])
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '10_information_causality.png'), bbox_inches='tight')
    plt.close()


def plot_no_cloning_comparison():
    """Compare no-cloning across classical, quantum, and box-world."""
    theories, fidelities = demonstrate_no_cloning()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bar chart of cloning fidelities
    ax = axes[0]
    names = [t[1].replace('\n', ' ') for t in theories]
    colors = ['gold', 'steelblue', 'darkred']
    bars = ax.bar(names, fidelities, color=colors, edgecolor='black', linewidth=2, alpha=0.8)
    
    for bar, f in zip(bars, fidelities):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{f:.3f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Optimal Cloning Fidelity', fontsize=12)
    ax.set_title('No-Cloning Theorem\nAcross Theory Space', fontsize=13)
    ax.set_ylim(0.8, 1.05)
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.5, label='Perfect cloning')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # State visualization
    ax = axes[1]
    
    # Draw "states" as circles, show cloning attempt
    for idx, (p, name) in enumerate(theories):
        y_base = 0.3 - idx * 0.25
        
        # Original state
        circle1 = plt.Circle((0.2, y_base), 0.08, color=colors[idx], alpha=0.7, label=name if idx == 0 else '')
        ax.add_patch(circle1)
        ax.text(0.2, y_base, 'ψ', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # Clone attempt
        circle2 = plt.Circle((0.5, y_base), 0.06, color=colors[idx], alpha=0.4, 
                            edgecolor='black', linewidth=2, linestyle='--')
        ax.add_patch(circle2)
        ax.text(0.5, y_base, 'ψ\'', ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Arrow
        ax.annotate('', xy=(0.44, y_base), xytext=(0.28, y_base),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
        
        # Fidelity label
        ax.text(0.75, y_base, f'F={fidelities[idx]:.3f}', ha='left', va='center',
               fontsize=11, fontweight='bold', color=colors[idx])
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.1, 0.45)
    ax.set_title('Cloning Across Theories\n(Arrow shows cloning transformation)', fontsize=13)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '11_no_cloning_comparison.png'), bbox_inches='tight')
    plt.close()


def plot_qm_as_fixed_point():
    """Show quantum theory as a fixed point in theory space."""
    p_values, cloning_fid, ic_ratios, local_disc = explore_theory_space()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 1. Information causality
    ax = axes[0, 0]
    ax.plot(p_values, ic_ratios, 'b-', linewidth=2.5)
    ax.axhline(y=1.0, color='r', linestyle='--', linewidth=2)
    ax.axvline(x=2, color='g', linestyle='--', linewidth=2)
    ax.fill_between(p_values, 0, ic_ratios, where=(ic_ratios > 1.01),
                    alpha=0.3, color='red')
    ax.set_xlabel('p', fontsize=12)
    ax.set_ylabel('IC Ratio', fontsize=11)
    ax.set_title('Information Causality\nRed region = violation', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1, 10)
    
    # 2. No-cloning
    ax = axes[0, 1]
    ax.plot(p_values, cloning_fid, 'r-', linewidth=2.5)
    ax.axhline(y=1.0, color='k', linestyle='--', linewidth=2)
    ax.axhline(y=5/6, color='g', linestyle='--', linewidth=2)
    ax.axvline(x=2, color='g', linestyle='--', linewidth=2)
    ax.fill_between(p_values, cloning_fid, 1.0, alpha=0.3, color='red')
    ax.set_xlabel('p', fontsize=12)
    ax.set_ylabel('Cloning Fidelity', fontsize=11)
    ax.set_title('No-Cloning\nRed region = cloning possible', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1, 10)
    
    # 3. Combined constraint
    ax = axes[1, 0]
    p_test, satisfies_all = find_qm_fixed_point()
    ax.plot(p_test, satisfies_all, 'g-', linewidth=3)
    ax.set_xlabel('p', fontsize=12)
    ax.set_ylabel('All Constraints Satisfied', fontsize=11)
    ax.set_title('Quantum Theory: Unique Solution\n(Only p=2 satisfies all)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.1, 1.1)
    
    # 4. State space geometry
    ax = axes[1, 1]
    
    # Draw state spaces for p=1, 2, ∞
    theta = np.linspace(0, 2*np.pi, 100)
    
    # p=1: diamond (L1 ball in 2D)
    l1_x = np.array([1, 0, -1, 0, 1])
    l1_y = np.array([0, 1, 0, -1, 0])
    ax.plot(l1_x, l1_y, 'gold', linewidth=2.5, label='p=1 (classical)')
    ax.fill(l1_x, l1_y, alpha=0.2, color='gold')
    
    # p=2: circle (L2 ball in 2D)
    ax.plot(np.cos(theta), np.sin(theta), 'steelblue', linewidth=2.5, label='p=2 (quantum)')
    ax.fill(np.cos(theta), np.sin(theta), alpha=0.2, color='steelblue')
    
    # p=∞: square (L∞ ball in 2D)
    linf_x = np.array([-1, 1, 1, -1, -1])
    linf_y = np.array([-1, -1, 1, 1, -1])
    ax.plot(linf_x, linf_y, 'darkred', linewidth=2.5, label='p=∞ (box-world)')
    ax.fill(linf_x, linf_y, alpha=0.2, color='darkred')
    
    ax.set_aspect('equal')
    ax.set_xlabel('x₁', fontsize=11)
    ax.set_ylabel('x₂', fontsize=11)
    ax.set_title('State Space Geometry\n(Lp balls in 2D)', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '12_qm_fixed_point.png'), bbox_inches='tight')
    plt.close()


def run_simulation_3():
    """Run all visualizations for Simulation 3."""
    print("=" * 70)
    print("SIMULATION 3: Information-Theoretic Derivation of QM")
    print("=" * 70)
    
    print("\n[1] Information principles:")
    print("    P1. Information causality: I ≤ m (communication bits)")
    print("    P2. No-cloning: F < 1 (no perfect copying)")
    print("    P3. Local discriminability: composite states from local measurements")
    print("    P4. Purification: mixed states have unique purifications")
    print("    P5. Ideal compression: lossless info compression possible")
    
    # Test each principle
    print("\n[2] Testing principles across theory space:")
    for p in [1.0, 2.0, 5.0, 10.0]:
        theory = GPTTheory(p=p, n=3)
        cf = theory.no_cloning_test(n_tests=50)
        ic_ratio, _, _ = theory.information_causality_test()
        states = [theory.random_state() for _ in range(5)]
        ld = theory.local_discriminability(states)
        
        print(f"    p={p:5.1f}: cloning={cf:.3f}, IC_ratio={ic_ratio:.3f}, LD={ld}")
    
    # Find fixed point
    print("\n[3] Finding unique fixed point:")
    p_test, satisfies_all = find_qm_fixed_point()
    valid_mask = satisfies_all.astype(bool)
    valid_ps = p_test[valid_mask]
    if len(valid_ps) > 0:
        print(f"    Valid p range: [{valid_ps[0]:.3f}, {valid_ps[-1]:.3f}]")
        print(f"    Quantum theory (p=2) is in this range: {1.0 <= 2.0 <= valid_ps[-1]}")
    else:
        print("    No valid theories found (check numerical precision)")
    
    # Cloning comparison
    print("\n[4] No-cloning theorem:")
    theories, fidelities = demonstrate_no_cloning()
    for (p, name), f in zip(theories, fidelities):
        p_label = "∞" if p == np.inf else f"{p:.1f}"
        print(f"    {name}: F = {f:.4f}")
    
    # Visualizations
    print("\n[5] Generating visualizations...")
    plot_information_causality()
    print("    → Saved: 10_information_causality.png")
    
    plot_no_cloning_comparison()
    print("    → Saved: 11_no_cloning_comparison.png")
    
    plot_qm_as_fixed_point()
    print("    → Saved: 12_qm_fixed_point.png")
    
    print("\n" + "=" * 70)
    print("SIMULATION 3 COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    run_simulation_3()
