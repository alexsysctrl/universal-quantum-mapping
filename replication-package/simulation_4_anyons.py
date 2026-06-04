"""
Simulation 4: 2+1D Anyon Modules from Modular Dirac Operator

Tests: Modular Clifford modules in 2+1 dimensions, braiding matrices,
fusion rules matching SU(2)_k, topological entropy, and universal QC.

MCC Reference: Session 3, Section 5.1-5.5; Session 2, Section 8
Verification Report: Confidence HIGH for 2+1D anyon modules
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# ============================================================================
# SECTION 1: SU(2)_k CHERN-SIMONS THEORY
# ============================================================================

class SU2kChernSimons:
    """
    Implement SU(2)_k Chern-Simons theory anyon module.
    
    Anyon types: j = 0, 1/2, 1, ..., k/2  (k+1 types)
    Fusion rules: j1 × j2 = Σ_c N_{j1,j2}^c c  where |j1-j2| ≤ c ≤ min(j1+j2, k-j1-j2)
    and j1+j2+c is even.
    
    Modular S and T matrices, braiding phases, topological entropy.
    """
    
    def __init__(self, k, seed=42):
        """
        Initialize SU(2)_k Chern-Simons theory.
        
        Parameters:
            k: Chern-Simons level (positive integer)
            seed: Random seed
        """
        self.k = k
        # For SU(2)_k: anyon types are j = 0, 1/2, 1, ..., k/2
        # Count: (k/2 - 0) / (1/2) + 1 = k + 1
        self.n_types = k + 1
        # Generate types: j = 0, 1/2, 1, ..., k/2
        self.anyon_types = np.array([j * 0.5 for j in range(0, k + 1)])
        
        # Conformal weights: h_j = j(j+1) / (k+2)
        self.conformal_weights = self._compute_conformal_weights()
        
        # Quantum dimensions: d_j = sin(π(2j+1)/(k+2)) / sin(π/(k+2))
        self.quantum_dimensions = self._compute_quantum_dimensions()
        
        # Total quantum dimension: D = sqrt(sum d_j^2)
        self.D = np.sqrt(np.sum(self.quantum_dimensions ** 2))
        
        # Modular S matrix
        self.S = self._compute_S_matrix()
        
        # Modular T matrix
        self.T = self._compute_T_matrix()
        
        # Fusion rules
        self.fusion_rules = self._compute_fusion_rules()
        
        # Braiding matrices
        self.braiding_matrices = {}
        
        np.random.seed(seed)
    
    def _compute_conformal_weights(self):
        """Compute conformal weights h_j = j(j+1)/(k+2)."""
        return {j: j * (j + 1) / (self.k + 2) for j in self.anyon_types}
    
    def _compute_quantum_dimensions(self):
        """
        Compute quantum dimensions d_j = sin(π(2j+1)/(k+2)) / sin(π/(k+2)).
        """
        denom = np.sin(np.pi / (self.k + 2))
        if abs(denom) < 1e-15:
            return np.ones(self.n_types)
        
        dims = []
        for j in self.anyon_types:
            d_j = np.sin(np.pi * (2 * j + 1) / (self.k + 2)) / denom
            dims.append(d_j)
        
        return np.array(dims)
    
    def _compute_S_matrix(self):
        """
        Compute the modular S matrix.
        
        S_{ab} = sqrt(2/(k+2)) * sin(π(2a+1)(2b+1)/(k+2))
        
        The S matrix is symmetric and unitary.
        """
        S = np.zeros((self.n_types, self.n_types))
        prefactor = np.sqrt(2.0 / (self.k + 2))
        
        for i, a in enumerate(self.anyon_types):
            for j, b in enumerate(self.anyon_types):
                S[i, j] = prefactor * np.sin(np.pi * (2 * a + 1) * (2 * b + 1) / (self.k + 2))
        
        return S
    
    def _compute_T_matrix(self):
        """
        Compute the modular T matrix.
        
        T_{ab} = exp(2πi(h_a - c/24)) * delta_{ab}
        
        where c = 3k/(k+2) is the central charge.
        """
        c = 3 * self.k / (self.k + 2)  # Central charge of SU(2)_k
        
        T = np.zeros((self.n_types, self.n_types))
        for i, j in enumerate(self.anyon_types):
            h_j = self.conformal_weights[j]
            T[i, i] = np.exp(2j * np.pi * 1j * (h_j - c / 24))
        
        return T
    
    def _compute_fusion_rules(self):
        """
        Compute fusion rules N_{ab}^c.
        
        a × b = Σ_c N_{ab}^c c
        
        where N_{ab}^c = 1 if |a-b| ≤ c ≤ min(a+b, k-a-b) and a+b+c is even,
        and 0 otherwise.
        """
        fusion = {}
        
        for i, a in enumerate(self.anyon_types):
            for j, b in enumerate(self.anyon_types):
                fusion[(i, j)] = []
                for l, c in enumerate(self.anyon_types):
                    if (abs(a - b) <= c <= min(a + b, self.k - a - b) and
                        abs(a + b + c - round(2 * (a + b + c)) / 2) < 0.01):
                        # Check parity: a + b + c must be integer and even
                        if abs((a + b + c) - round(a + b + c)) < 0.01:
                            if round(a + b + c) % 2 == 0:
                                fusion[(i, j)].append(l)
        
        return fusion
    
    def compute_braiding_matrix(self, a, b):
        """
        Compute the braiding matrix B_ab for two anyons of types a, b.
        
        B_ab = exp(iπ D_ω / Λ) = exp(2πi(h_c - h_a - h_b))
        
        where c is the fusion channel.
        
        Parameters:
            a: Anyon type index
            b: Anyon type index
        
        Returns:
            braiding: Dict mapping fusion channel c to braiding phase
        """
        braiding = {}
        
        for c_idx in self.fusion_rules.get((a, b), []):
            c = self.anyon_types[c_idx]
            h_a = self.conformal_weights[self.anyon_types[a]]
            h_b = self.conformal_weights[self.anyon_types[b]]
            h_c = self.conformal_weights[c]
            
            # Braiding phase
            phase_angle = 2 * np.pi * (h_c - h_a - h_b)
            phase = np.exp(1j * phase_angle)
            
            braiding[c_idx] = {
                'phase': phase,
                'angle': phase_angle,
                'h_a': h_a,
                'h_b': h_b,
                'h_c': h_c,
            }
        
        return braiding
    
    def compute_topological_entropy(self):
        """
        Compute the topological entanglement entropy.
        
        S_top = log(D) = -log(|S_00|)
        
        Returns:
            S_top: Topological entropy
        """
        S_top = np.log(self.D)
        S_top_alt = -np.log(np.abs(self.S[0, 0]))
        
        return S_top, S_top_alt
    
    def is_universal_qc(self):
        """
        Check if the anyon model supports universal quantum computation.
        
        By the Freedman-Larsen-Wang theorem:
        - k = 2 (Ising): NOT universal (Clifford gates only)
        - k ≥ 4: Universal (braid group representation is dense in SU(2))
        
        Returns:
            universal: bool
        """
        return self.k >= 4
    
    def verify_modular_group(self):
        """
        Verify that S^2 = C (charge conjugation) and (ST)^3 = e^{2πic/24} S^2.
        
        Returns:
            results: Dict with verification results
        """
        # S^2 = C (charge conjugation matrix)
        S_squared = self.S @ self.S
        C = np.eye(self.n_types)  # For SU(2)_k, all anyons are self-conjugate
        
        S2_error = np.max(np.abs(S_squared - C))
        
        # (ST)^3 = e^{2πic/24} S^2
        ST = self.S @ self.T
        ST3 = ST @ ST @ ST
        c = 3 * self.k / (self.k + 2)
        phase_factor = np.exp(2j * np.pi * 1j * c / 24) * self.S @ self.S
        
        ST3_error = np.max(np.abs(ST3 - phase_factor))
        
        return {
            'S_squared_error': S2_error,
            'ST_cubed_error': ST3_error,
            'S_squared_valid': S2_error < 1e-10,
            'ST_cubed_valid': ST3_error < 1e-10,
        }


# ============================================================================
# SECTION 2: MODULAR DIRAC OPERATOR CONNECTION
# ============================================================================

def compute_D_omega_braiding(k, num_modes=100, cutoff=10.0):
    """
    Compute the braiding matrix from the modular Dirac operator D_ω.
    
    B = exp(iπ D_ω / Λ)
    
    where Λ is a cutoff scale related to the Chern-Simons level k.
    
    Parameters:
        k: Chern-Simons level
        num_modes: Number of D_ω modes to include
        cutoff: Cutoff scale Λ
    
    Returns:
        braiding_from_D: Braiding phases computed from D_ω
    """
    # D_ω spectrum for SU(2)_k: discrete modes proportional to conformal weights
    # D_ω eigenvalues: μ_j ∝ h_j = j(j+1)/(k+2)
    
    anyon_types = np.array([j / 2 for j in range(0, k + 1, 1)])
    conformal_weights = anyon_types * (anyon_types + 1) / (k + 2)
    
    # D_ω eigenvalues (proportional to conformal weights)
    D_eigenvalues = conformal_weights * cutoff  # Scale by cutoff
    
    # Braiding: B = exp(iπ D_ω / Λ) = exp(iπ * D_eigenvalue / cutoff)
    braiding_phases = np.exp(1j * np.pi * D_eigenvalues / cutoff)
    
    # Compare with standard anyonic braiding
    standard_phases = np.exp(2j * np.pi * 1j * conformal_weights)
    
    # The MCC prediction: B_ab = exp(iπ D_ω / Λ) should match
    # exp(2πi(h_c - h_a - h_b)) for appropriate choice of Λ
    # Here we use Λ = cutoff and check the correspondence
    
    return {
        'D_phases': braiding_phases,
        'standard_phases': standard_phases,
        'conformal_weights': conformal_weights,
        'anyon_types': anyon_types,
    }


# ============================================================================
# SECTION 3: PLOTTING
# ============================================================================

def plot_braiding_phases(su2k_list, filename='output/braiding_plot.png'):
    """
    Plot braiding phases as a function of Chern-Simons level k.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    
    k_values = [2, 3, 4, 5, 6, 8, 10]
    
    # 1. Braiding phases for 1/2 × 1/2 → 0
    ax = axes[0, 0]
    phases_k = []
    for k in k_values:
        su2k = SU2kChernSimons(k, seed=42)
        if 0 in su2k.anyon_types and 1 in su2k.anyon_types:
            braiding = su2k.compute_braiding_matrix(1, 1)  # j=1/2 is index 1
            if 0 in braiding:
                phases_k.append(np.real(braiding[0]['phase']))
            else:
                phases_k.append(np.nan)
        else:
            phases_k.append(np.nan)
    
    ax.plot(k_values, phases_k, 'bo-', linewidth=2, markersize=8)
    ax.set_xlabel('Chern-Simons Level k')
    ax.set_ylabel('Re(B_{1/2,1/2→0})')
    ax.set_title('Braiding Phase: 1/2 × 1/2 → 0')
    ax.grid(True, alpha=0.3)
    
    # 2. Braiding phases for 1/2 × 1/2 → 1
    ax = axes[0, 1]
    phases_k = []
    for k in k_values:
        su2k = SU2kChernSimons(k, seed=42)
        if 0 in su2k.anyon_types and 1 in su2k.anyon_types and 2 in su2k.anyon_types:
            braiding = su2k.compute_braiding_matrix(1, 1)
            if 2 in braiding:
                phases_k.append(np.real(braiding[2]['phase']))
            else:
                phases_k.append(np.nan)
        else:
            phases_k.append(np.nan)
    
    ax.plot(k_values, phases_k, 'rs-', linewidth=2, markersize=8)
    ax.set_xlabel('Chern-Simons Level k')
    ax.set_ylabel('Re(B_{1/2,1/2→1})')
    ax.set_title('Braiding Phase: 1/2 × 1/2 → 1')
    ax.grid(True, alpha=0.3)
    
    # 3. Quantum dimensions vs k
    ax = axes[1, 0]
    j_max = [0, 0.5, 1]  # j = 0, 1/2, 1
    for j in j_max:
        idx = int(2 * j)
        dims = []
        for k in k_values:
            su2k = SU2kChernSimons(k, seed=42)
            if idx < su2k.n_types:
                dims.append(su2k.quantum_dimensions[idx])
            else:
                dims.append(np.nan)
        ax.plot(k_values, dims, 'g^-', linewidth=2, markersize=8, label=f'j={j}')
    
    ax.set_xlabel('Chern-Simons Level k')
    ax.set_ylabel('Quantum Dimension d_j')
    ax.set_title('Quantum Dimensions vs k')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. Topological entropy vs k
    ax = axes[1, 1]
    S_top_values = []
    for k in k_values:
        su2k = SU2kChernSimons(k, seed=42)
        S_top, _ = su2k.compute_topological_entropy()
        S_top_values.append(S_top)
    
    ax.plot(k_values, S_top_values, 'md-', linewidth=2, markersize=8)
    ax.set_xlabel('Chern-Simons Level k')
    ax.set_ylabel('Topological Entropy S_top = log(D)')
    ax.set_title('Topological Entropy vs k')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✓ Braiding plot saved to {filename}")


def plot_fusion_tree(su2k, filename='output/fusion_tree.png'):
    """
    Visualize the fusion rules as a tree/heatmap.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Fusion rule heatmap
    n = su2k.n_types
    fusion_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            fusion_matrix[i, j] = len(su2k.fusion_rules.get((i, j), []))
    
    im1 = axes[0].imshow(fusion_matrix, cmap='YlOrRd')
    axes[0].set_xlabel('Anyon Type b')
    axes[0].set_ylabel('Anyon Type a')
    axes[0].set_title(f'Fusion Rule Count N_ab^c\n(SU(2)_{su2k.k})')
    axes[0].set_xticks(range(n))
    axes[0].set_yticks(range(n))
    axes[0].set_xticklabels([f'{j:.1f}' for j in su2k.anyon_types], rotation=45)
    axes[0].set_yticklabels([f'{j:.1f}' for j in su2k.anyon_types])
    plt.colorbar(im1, ax=axes[0], label='Number of fusion channels')
    
    # 2. S-matrix heatmap
    im2 = axes[1].imshow(np.abs(su2k.S), cmap='viridis')
    axes[1].set_xlabel('Anyon Type b')
    axes[1].set_ylabel('Anyon Type a')
    axes[1].set_title(f'Modular S-Matrix |S_ab|\n(SU(2)_{su2k.k})')
    axes[1].set_xticks(range(n))
    axes[1].set_yticks(range(n))
    axes[1].set_xticklabels([f'{j:.1f}' for j in su2k.anyon_types], rotation=45)
    axes[1].set_yticklabels([f'{j:.1f}' for j in su2k.anyon_types])
    plt.colorbar(im2, ax=axes[1], label='|S_ab|')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✓ Fusion tree plot saved to {filename}")


def plot_d_omega_braiding_comparison(k, filename='output/D_omega_comparison.png'):
    """
    Compare braiding from D_ω with standard anyonic braiding.
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    result = compute_D_omega_braiding(k, num_modes=100, cutoff=10.0)
    
    x = np.arange(len(result['anyon_types']))
    width = 0.35
    
    ax.bar(x - width/2, np.real(result['D_phases']), width,
           label='B = exp(iπD_ω/Λ)', color='steelblue', alpha=0.8)
    ax.bar(x + width/2, np.real(result['standard_phases']), width,
           label='Standard: exp(2πih)', color='coral', alpha=0.8)
    
    ax.set_xlabel('Anyon Type j')
    ax.set_ylabel('Real Part of Braiding Phase')
    ax.set_title(f'Braiding Comparison: D_ω vs Standard (k={k})')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{j:.1f}' for j in result['anyon_types']])
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✓ D_ω comparison plot saved to {filename}")


# ============================================================================
# SECTION 4: MAIN SIMULATION
# ============================================================================

def main():
    """
    Main simulation: Construct anyon modules for SU(2)_k, compute braiding,
    fusion rules, topological entropy, and verify universal QC.
    """
    print("=" * 70)
    print("Simulation 4: 2+1D Anyon Modules from Modular Dirac Operator")
    print("Testing: Braiding, fusion rules, topological entropy, universal QC")
    print("=" * 70)
    
    # Parameters
    k_values = [2, 3, 4, 5, 6, 8, 10]
    
    print(f"\nChern-Simons levels tested: {k_values}")
    
    all_results = {}
    
    for k in k_values:
        print(f"\n{'=' * 70}")
        print(f"SU(2)_{k} Chern-Simons Theory")
        print(f"{'=' * 70}")
        
        su2k = SU2kChernSimons(k, seed=42)
        
        print(f"  Anyon types: {len(su2k.anyon_types)} (j = 0 to {k/2:.1f})")
        print(f"  Anyon types: {[f'{j:.1f}' for j in su2k.anyon_types]}")
        print(f"  Central charge: c = {3*k/(k+2):.4f}")
        print(f"  Total quantum dimension: D = {su2k.D:.4f}")
        print(f"  Topological entropy: S_top = log(D) = {np.log(su2k.D):.4f}")
        print(f"  Universal QC: {su2k.is_universal_qc()} (k >= 4: yes)")
        
        # Verify modular group relations
        mod_results = su2k.verify_modular_group()
        print(f"  S^2 = C: {'✓' if mod_results['S_squared_valid'] else '✗'} (error: {mod_results['S_squared_error']:.2e})")
        print(f"  (ST)^3: {'✓' if mod_results['ST_cubed_valid'] else '✗'} (error: {mod_results['ST_cubed_error']:.2e})")
        
        # Compute braiding for key anyon pairs
        print(f"\n  Braiding phases:")
        for j_a in [0, 0.5, 1]:
            for j_b in [0, 0.5, 1]:
                if j_a <= k/2 and j_b <= k/2:
                    idx_a = int(2 * j_a)
                    idx_b = int(2 * j_b)
                    braiding = su2k.compute_braiding_matrix(idx_a, idx_b)
                    for c_idx, info in braiding.items():
                        c = su2k.anyon_types[c_idx]
                        print(f"    {j_a:.1f} × {j_b:.1f} → {c:.1f}: "
                              f"phase = {info['phase']:.6f}, angle = {info['angle']:.4f} rad")
        
        # Fusion rules for j=1/2 × j=1/2
        print(f"\n  Fusion rules (j=1/2 × j=1/2):")
        idx_half = 1
        fusion_channels = su2k.fusion_rules.get((idx_half, idx_half), [])
        fusion_types = [su2k.anyon_types[c] for c in fusion_channels]
        print(f"    1/2 × 1/2 = {', '.join([f'{j:.1f}' for j in fusion_types])}")
        
        all_results[k] = su2k
    
    # D_ω braiding comparison
    print(f"\n{'=' * 70}")
    print("Braiding from Modular Dirac Operator D_ω")
    print(f"{'=' * 70}")
    
    for k in [4, 5, 6]:
        result = compute_D_omega_braiding(k, num_modes=100, cutoff=10.0)
        print(f"\n  k = {k}:")
        for i, j in enumerate(result['anyon_types']):
            print(f"    j = {j:.1f}: D_ω phase = {result['D_phases'][i]:.6f}, "
                  f"standard = {result['standard_phases'][i]:.6f}")
    
    # Plots
    plot_braiding_phases(k_values)
    plot_fusion_tree(all_results[5])
    plot_d_omega_braiding_comparison(5)
    
    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"This simulation tests the MCC prediction that anyon braiding")
    print(f"can be expressed as B = exp(iπ D_ω / Λ) from the modular Dirac operator.")
    print(f"")
    print(f"Key results:")
    for k in k_values:
        su2k = all_results[k]
        S_top, _ = su2k.compute_topological_entropy()
        print(f"  k={k}: D={su2k.D:.4f}, S_top={S_top:.4f}, universal QC={su2k.is_universal_qc()}")
    print(f"")
    print(f"Universal QC threshold:")
    print(f"  k=2 (Ising): NOT universal (Clifford gates only)")
    print(f"  k>=4: Universal (braid group dense in SU(2))")
    print(f"")
    print(f"CAVEATS:")
    print(f"  1. The identification B = exp(iπ D_ω/Λ) is an MCC conjecture.")
    print(f"  2. The cutoff Λ must be chosen to match the Chern-Simons level.")
    print(f"  3. The modular Dirac operator D_ω must be independently measurable.")
    print(f"{'=' * 70}")
    
    return {
        'k_values': k_values,
        'universal_qc_threshold': 4,
        'topological_entropies': {k: np.log(all_results[k].D) for k in k_values},
    }


if __name__ == '__main__':
    results = main()
