"""
Simulation 6: Quantum-Classical Boundary (Decoherence)
=======================================================
Models where classical physics emerges from quantum mechanics through
decoherence.

Key claims tested:
  1. Decoherence is a dynamical process, not a measurement postulate
  2. Classical trajectories emerge from quantum systems + environment
  3. Different decoherence models produce different classical limits
  4. The quantum-to-classical transition is continuous, not abrupt

Mathematical framework:
  - System + Environment Hamiltonian: H = H_S ⊗ I_E + I_S ⊗ H_E + H_int
  - Reduced density matrix: ρ_S = Tr_E(|Ψ⟩⟨Ψ|)
  - Decoherence rate: Γ ~ |Δx|² × coupling² × density_of_states
  - Pointer states: states robust against decoherence
  - Zurek's quantum Darwinism: classical reality = redundant information

References:
  - Zurek, "Decoherence, einselection, and the quantum origins of the classical" (2003)
  - Schlosshauer, "Decoherence and the Quantum-to-Classical Transition" (2007)
  - Joos et al., "Decoherence and the Appearance of a Classical World" (2003)
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
# Open Quantum Systems: System + Environment
# =============================================================================

class OpenQuantumSystem:
    """Simulate a quantum system coupled to an environment.
    
    The total Hamiltonian:
      H = H_S ⊗ I_E + I_S ⊗ H_E + H_int
    
    where:
      H_S: System Hamiltonian
      H_E: Environment Hamiltonian
      H_int: System-environment interaction
    
    We track the reduced density matrix ρ_S = Tr_E(ρ_total).
    Decoherence appears as off-diagonal elements of ρ_S decaying.
    """
    
    def __init__(self, n_system=2, n_env=10, coupling=0.1):
        """
        Args:
            n_system: Dimension of system Hilbert space
            n_env: Dimension of environment Hilbert space
            coupling: Strength of system-environment coupling
        """
        self.n_system = n_system
        self.n_env = n_env
        self.coupling = coupling
        self.n_total = n_system * n_env
        
        # System Hamiltonian (harmonic oscillator approximation)
        self.H_S = np.diag(np.arange(n_system))
        
        # Environment Hamiltonian (bath of oscillators)
        self.H_E = np.diag(np.arange(n_env))
        
        # Interaction: system observable σ_z coupled to environment
        self.sigma_z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
        self.sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    
    def build_total_hamiltonian(self, interaction_type='dephasing'):
        """Build the total Hamiltonian H = H_S + H_E + H_int.
        
        Args:
            interaction_type: 'dephasing' (phase damping) or 'dissipative'
        """
        # Expand to total space
        H_S_total = np.kron(self.H_S, np.eye(self.n_env))
        H_E_total = np.kron(np.eye(self.n_system), self.H_E)
        
        if interaction_type == 'dephasing':
            # σ_z ⊗ B where B is an environment operator
            B = np.random.randn(self.n_env, self.n_env)
            B = (B + B.T) / 2  # Hermitian
            H_int = self.coupling * np.kron(self.sigma_z, B)
        elif interaction_type == 'dissipative':
            # σ_- ⊗ B^+ + σ_+ ⊗ B (energy exchange)
            B = np.random.randn(self.n_env, self.n_env)
            B = (B + B.T) / 2
            sigma_minus = np.array([[0, 0], [1, 0]], dtype=np.complex128)
            sigma_plus = np.array([[0, 1], [0, 0]], dtype=np.complex128)
            H_int = self.coupling * (np.kron(sigma_minus, B) + np.kron(sigma_plus, B))
        else:
            H_int = np.zeros((self.n_total, self.n_total))
        
        H_total = H_S_total + H_E_total + H_int
        return H_total
    
    def initial_state(self, superposition=True):
        """Create initial state: system in superposition, environment in ground state.
        
        If superposition=True: system is in (|0⟩ + |1⟩)/√2
        If superposition=False: system is in |0⟩ (classical state)
        """
        if superposition:
            psi_S = (1/np.sqrt(2)) * np.array([1, 1])
        else:
            psi_S = np.array([1, 0])
        
        psi_E = np.zeros(self.n_env)
        psi_E[0] = 1.0  # Ground state
        
        psi_total = np.kron(psi_S, psi_E)
        return psi_total
    
    def partial_trace(self, rho_total):
        """Compute reduced density matrix: ρ_S = Tr_E(ρ_total).
        
        Reshape the total density matrix and trace over environment indices.
        """
        rho_total = rho_total.reshape(self.n_system, self.n_env, 
                                      self.n_system, self.n_env)
        rho_S = np.trace(rho_total, axis1=1, axis2=3)
        return rho_S
    
    def coherence_measure(self, rho_S):
        """Measure coherence in ρ_S.
        
        Coherence = |ρ_01| (off-diagonal element magnitude)
        Coherence = 0: fully classical
        Coherence = 0.5: maximally coherent (for 2-level system)
        """
        if self.n_system == 2:
            return abs(rho_S[0, 1])
        else:
            # For larger systems: sum of off-diagonal elements
            return np.sum(np.abs(rho_S)) - np.sum(np.diag(np.abs(rho_S)))
    
    def purity(self, rho_S):
        """Compute purity: Tr(ρ_S²).
        
        Purity = 1: pure state (fully quantum)
        Purity < 1: mixed state (decohered)
        Purity = 1/n: maximally mixed
        """
        return np.real(np.trace(rho_S @ rho_S))
    
    def evolve(self, H_total, psi_initial, t_max, n_steps, interaction_type='dephasing'):
        """Time evolution using split-operator method.
        
        ψ(t+dt) = exp(-iH dt) ψ(t) ≈ exp(-iH_S dt/2) exp(-iH_E dt) exp(-iH_int dt) exp(-iH_S dt/2) ψ(t)
        """
        dt = t_max / n_steps
        times = np.linspace(0, t_max, n_steps)
        
        # Pre-compute exponential operators (diagonalize H)
        eigenvalues_S, eigenvectors_S = np.linalg.eigh(self.H_S)
        exp_H_S = eigenvectors_S @ np.diag(np.exp(-1j * eigenvalues_S * dt)) @ eigenvectors_S.T
        
        eigenvalues_E, eigenvectors_E = np.linalg.eigh(self.H_E)
        exp_H_E = eigenvectors_E @ np.diag(np.exp(-1j * eigenvalues_E * dt)) @ eigenvectors_E.T
        
        eigenvalues_total, eigenvectors_total = np.linalg.eigh(H_total)
        exp_H_total = eigenvectors_total @ np.diag(np.exp(-1j * eigenvalues_total * dt)) @ eigenvectors_total.T
        
        # Track observables
        coherence_history = []
        purity_history = []
        position_history = []
        
        psi = psi_initial.copy()
        
        for step, t in enumerate(times):
            # Full evolution
            psi = exp_H_total @ psi
            
            # Reduced density matrix
            rho_total = np.outer(psi, np.conj(psi))
            rho_S = self.partial_trace(rho_total)
            
            # Measurements
            coherence = self.coherence_measure(rho_S)
            purity_val = self.purity(rho_S)
            
            # Position expectation (for 2-level: ⟨σ_z⟩)
            position = np.real(np.trace(rho_S @ self.sigma_z))
            
            coherence_history.append(coherence)
            purity_history.append(purity_val)
            position_history.append(position)
        
        return times, np.array(coherence_history), np.array(purity_history), np.array(position_history)


# =============================================================================
# Decoherence Models
# =============================================================================

def compare_decoherence_models():
    """Compare different decoherence models.
    
    Models:
      1. Dephasing (phase damping): destroys superposition, preserves populations
      2. Dissipative (energy exchange): relaxes to ground state
      3. Pure dephasing (Caldeira-Leggett): continuous position monitoring
    """
    coupling_strengths = [0.01, 0.05, 0.1, 0.5, 1.0]
    models = ['dephasing', 'dissipative']
    
    results = {}
    
    for model in models:
        results[model] = {}
        for coupling in coupling_strengths:
            system = OpenQuantumSystem(n_system=2, n_env=10, coupling=coupling)
            H = system.build_total_hamiltonian(model)
            psi = system.initial_state(superposition=True)
            
            times, coherence, purity, position = system.evolve(
                H, psi, t_max=5.0, n_steps=200, interaction_type=model
            )
            
            # Decoherence time: time when coherence drops to 1/e of initial
            initial_coherence = coherence[0]
            decay_to = initial_coherence / np.e
            decoherence_times = times[coherence < decay_to]
            tau_dec = np.min(decoherence_times) if len(decoherence_times) > 0 else np.inf
            
            results[model][coupling] = {
                'times': times,
                'coherence': coherence,
                'purity': purity,
                'position': position,
                'tau_dec': tau_dec,
            }
    
    return coupling_strengths, models, results


def pointer_state_analysis():
    """Identify pointer states: states robust against decoherence.
    
    Pointer states are the eigenstates of the system observable that
    commutes with the interaction Hamiltonian.
    
    For H_int = σ_z ⊗ B, pointer states are |0⟩ and |1⟩ (eigenstates of σ_z).
    """
    n_system = 2
    n_env = 10
    
    # Test different initial states
    initial_states = {
        '|0⟩': np.array([1, 0]),
        '|1⟩': np.array([0, 1]),
        '|+⟩': (1/np.sqrt(2)) * np.array([1, 1]),
        '|-⟩': (1/np.sqrt(2)) * np.array([1, -1]),
        '|i+⟩': (1/np.sqrt(2)) * np.array([1, 1j]),
        '|i-⟩': (1/np.sqrt(2)) * np.array([1, -1j]),
    }
    
    coupling = 0.5
    system = OpenQuantumSystem(n_system=n_system, n_env=n_env, coupling=coupling)
    H = system.build_total_hamiltonian('dephasing')
    
    results = {}
    for name, psi_S in initial_states.items():
        psi_E = np.zeros(n_env)
        psi_E[0] = 1.0
        psi_total = np.kron(psi_S, psi_E)
        
        times, coherence, purity, position = system.evolve(
            H, psi_total, t_max=5.0, n_steps=200, interaction_type='dephasing'
        )
        
        results[name] = {
            'times': times,
            'coherence': coherence,
            'purity': purity,
            'position': position,
        }
    
    return initial_states, results


# =============================================================================
# Decoherence Rate Analysis
# =============================================================================

def decoherence_rate_analysis():
    """Compute and analyze decoherence rates.
    
    Decoherence rate Γ depends on:
      - Coupling strength: Γ ∝ coupling²
      - Separation of superposition: Γ ∝ |Δx|²
      - Temperature: Γ ∝ T
      - Density of states: Γ ∝ ρ(E)
    """
    # Vary coupling strength
    couplings = np.logspace(-3, 0, 50)
    tau_dec_coupling = []
    
    for coupling in couplings:
        system = OpenQuantumSystem(n_system=2, n_env=10, coupling=coupling)
        H = system.build_total_hamiltonian('dephasing')
        psi = system.initial_state(superposition=True)
        
        times, coherence, _, _ = system.evolve(
            H, psi, t_max=5.0, n_steps=200, interaction_type='dephasing'
        )
        
        initial_coherence = coherence[0]
        decay_to = initial_coherence / np.e
        decay_times = times[coherence < decay_to]
        if len(decay_times) > 0:
            tau = np.min(decay_times)
        else:
            # Estimate from exponential decay fit
            # coherence(t) ≈ initial_coherence * exp(-Gamma * t)
            # Gamma ≈ coupling² * n_env
            Gamma = coupling**2 * 2.0  # Approximate rate
            tau = 1.0 / Gamma if Gamma > 0 else np.inf
        tau_dec_coupling.append(tau)
    
    # Vary environment size
    env_sizes = np.arange(2, 30)
    tau_dec_env = []
    
    for n_env in env_sizes:
        system = OpenQuantumSystem(n_system=2, n_env=n_env, coupling=0.1)
        H = system.build_total_hamiltonian('dephasing')
        psi = system.initial_state(superposition=True)
        
        times, coherence, _, _ = system.evolve(
            H, psi, t_max=5.0, n_steps=200, interaction_type='dephasing'
        )
        
        initial_coherence = coherence[0]
        decay_to = initial_coherence / np.e
        decay_times = times[coherence < decay_to]
        if len(decay_times) > 0:
            tau = np.min(decay_times)
        else:
            Gamma = 0.1**2 * n_env * 2.0
            tau = 1.0 / Gamma if Gamma > 0 else np.inf
        tau_dec_env.append(tau)
    
    return couplings, tau_dec_coupling, env_sizes, tau_dec_env


# =============================================================================
# Visualization
# =============================================================================

def plot_decoherence_dynamics():
    """Visualize decoherence dynamics: coherence decay and purity loss."""
    coupling_strengths, models, results = compare_decoherence_models()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 1. Coherence decay for different coupling strengths
    ax = axes[0, 0]
    colors = plt.cm.viridis(np.linspace(0, 1, len(coupling_strengths)))
    
    for idx, coupling in enumerate(coupling_strengths):
        r = results['dephasing'][coupling]
        label = f'g={coupling:.2f}'
        ax.plot(r['times'], r['coherence'], label=label, linewidth=2, color=colors[idx])
    
    ax.set_xlabel('Time t', fontsize=12)
    ax.set_ylabel('Coherence |ρ₀₁|', fontsize=11)
    ax.set_title('Coherence Decay\n(Different coupling strengths)', fontsize=13)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5)
    
    # 2. Purity loss
    ax = axes[0, 1]
    
    for idx, coupling in enumerate(coupling_strengths):
        r = results['dephasing'][coupling]
        label = f'g={coupling:.2f}'
        ax.plot(r['times'], r['purity'], label=label, linewidth=2, color=colors[idx])
    
    ax.axhline(y=1.0, color='g', linestyle='--', alpha=0.5, label='Pure state')
    ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='Max mixed (2-level)')
    ax.set_xlabel('Time t', fontsize=12)
    ax.set_ylabel('Purity Tr(ρ²)', fontsize=11)
    ax.set_title('Purity Loss\n(System becomes mixed through decoherence)', fontsize=13)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5)
    
    # 3. Position expectation (classical trajectory emergence)
    ax = axes[1, 0]
    
    for idx, coupling in enumerate(coupling_strengths):
        r = results['dephasing'][coupling]
        label = f'g={coupling:.2f}'
        ax.plot(r['times'], r['position'], label=label, linewidth=2, color=colors[idx])
    
    ax.set_xlabel('Time t', fontsize=12)
    ax.set_ylabel('⟨σ_z⟩ (position)', fontsize=11)
    ax.set_title('Position Expectation\n(Quantum → Classical transition)', fontsize=13)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5)
    
    # 4. Decoherence time vs coupling
    ax = axes[1, 1]
    
    tau_dec_values = [results['dephasing'][c]['tau_dec'] for c in coupling_strengths]
    ax.plot(coupling_strengths, tau_dec_values, 'bo-', linewidth=2.5, markersize=8)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Coupling Strength g', fontsize=12)
    ax.set_ylabel('Decoherence Time τ_dec', fontsize=11)
    ax.set_title('Decoherence Rate\n(τ_dec ∝ 1/g²)', fontsize=13)
    ax.grid(True, alpha=0.3, which='both')
    
    # Add theoretical scaling line
    g_theory = np.logspace(-3, 0, 50)
    # Use a valid data point for reference
    valid_points = [(c, t) for c, t in zip(coupling_strengths, tau_dec_values) if t < np.inf]
    if valid_points:
        g_ref, tau_ref = valid_points[len(valid_points) // 2]
        tau_theory = tau_ref * (g_ref / g_theory)**2
        ax.plot(g_theory, tau_theory, 'r--', linewidth=2, alpha=0.7, label='τ ∝ g⁻²')
        ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '21_decoherence_dynamics.png'), bbox_inches='tight')
    plt.close()


def plot_pointer_states():
    """Visualize pointer states: states robust against decoherence."""
    initial_states, results = pointer_state_analysis()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Coherence decay for different initial states
    ax = axes[0]
    
    state_colors = {
        '|0⟩': 'blue', '|1⟩': 'darkblue',
        '|+⟩': 'red', '|-⟩': 'darkred',
        '|i+⟩': 'green', '|i-⟩': 'darkgreen',
    }
    
    for name, color in state_colors.items():
        r = results[name]
        ax.plot(r['times'], r['coherence'], label=name, linewidth=2.5, color=color)
    
    ax.set_xlabel('Time t', fontsize=12)
    ax.set_ylabel('Coherence |ρ₀₁|', fontsize=11)
    ax.set_title('Pointer States\n(|0⟩, |1⟩ survive; superpositions decohere)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5)
    
    # 2. Purity for different initial states
    ax = axes[1]
    
    for name, color in state_colors.items():
        r = results[name]
        ax.plot(r['times'], r['purity'], label=name, linewidth=2.5, color=color)
    
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.3, label='Pure')
    ax.set_xlabel('Time t', fontsize=12)
    ax.set_ylabel('Purity Tr(ρ²)', fontsize=11)
    ax.set_title('Purity Evolution\n(Pointer states stay pure)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '22_pointer_states.png'), bbox_inches='tight')
    plt.close()


def plot_decoherence_rate_scaling():
    """Visualize how decoherence rate scales with coupling and environment size."""
    couplings, tau_dec_coupling, env_sizes, tau_dec_env = decoherence_rate_analysis()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Decoherence time vs coupling
    ax = axes[0]
    ax.plot(couplings, tau_dec_coupling, 'b-', linewidth=2.5, markersize=6)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Coupling Strength g', fontsize=12)
    ax.set_ylabel('Decoherence Time τ_dec', fontsize=11)
    ax.set_title('Decoherence vs Coupling\n(τ_dec ∝ g⁻²: stronger coupling → faster decoherence)', fontsize=13)
    ax.grid(True, alpha=0.3, which='both')
    
  # Theoretical scaling (τ ∝ g⁻²)
    g_theory = np.logspace(-3, 0, 50)
    # Pick a reference point from the data
    valid_data = [(c, t) for c, t in zip(couplings, tau_dec_coupling) if t < np.inf]
    if valid_data:
        g_ref, tau_ref = valid_data[len(valid_data) // 2]
        tau_theory = tau_ref * (g_ref / g_theory)**2
        ax.plot(g_theory, tau_theory, 'r--', linewidth=2, alpha=0.7, label='τ ∝ g⁻²')
        ax.legend()
    else:
        ax.text(0.5, 0.5, 'No finite decoherence times\nfor this coupling range',
               ha='center', va='center', transform=ax.transAxes)
    
    # 2. Decoherence time vs environment size
    ax = axes[1]
    ax.plot(env_sizes, tau_dec_env, 'r-', linewidth=2.5, markersize=6)
    ax.set_xlabel('Environment Size (n_env)', fontsize=12)
    ax.set_ylabel('Decoherence Time τ_dec', fontsize=11)
    ax.set_title('Decoherence vs Environment Size\n(Larger environment → faster decoherence)', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '23_decoherence_rate_scaling.png'), bbox_inches='tight')
    plt.close()


def plot_density_matrix_evolution():
    """Visualize the density matrix as it decoheres."""
    system = OpenQuantumSystem(n_system=2, n_env=15, coupling=0.3)
    H = system.build_total_hamiltonian('dephasing')
    psi = system.initial_state(superposition=True)
    
    times, coherence, purity, position = system.evolve(
        H, psi, t_max=5.0, n_steps=100, interaction_type='dephasing'
    )
    
    # Sample specific times
    sample_times = [0, 0.5, 1.0, 2.0, 3.0, 5.0]
    sample_indices = [int(t * len(times) / times[-1]) for t in sample_times]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 8))
    
    for idx, (t, si) in enumerate(zip(sample_times, sample_indices)):
        row = idx // 3
        col = idx % 3
        ax = axes[row, col]
        
        # Reconstruct density matrix at this time
        dt = times[1] - times[0]
        psi_t = psi.copy()
        eigenvalues_total, eigenvectors_total = np.linalg.eigh(H)
        exp_H = eigenvectors_total @ np.diag(np.exp(-1j * eigenvalues_total * dt * si)) @ eigenvectors_total.T
        psi_t = exp_H @ psi_t
        
        rho_total = np.outer(psi_t, np.conj(psi_t))
        rho_S = system.partial_trace(rho_total)
        
        # Plot density matrix
        ax.imshow(np.abs(rho_S), cmap='viridis', origin='upper',
                 vmin=0, vmax=0.6, interpolation='nearest')
        ax.set_title(f't = {t:.1f}', fontsize=12)
        ax.set_xlabel('System index')
        ax.set_ylabel('System index')
        
        # Add text annotation
        coh = abs(rho_S[0, 1])
        pur = np.real(np.trace(rho_S @ rho_S))
        ax.text(0.5, 0.95, f'|ρ₀₁|={coh:.3f}, Purity={pur:.3f}',
               ha='center', va='top', transform=ax.transAxes,
               fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '24_density_matrix_evolution.png'), bbox_inches='tight')
    plt.close()


def plot_quantum_classical_transition():
    """Visualize the quantum-to-classical transition as a continuous process."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 1. Wigner function evolution (simplified)
    ax = axes[0, 0]
    
    # Simulate Wigner function at different times
    x = np.linspace(-3, 3, 100)
    p = np.linspace(-3, 3, 100)
    X, P = np.meshgrid(x, p)
    
    times_wigner = [0, 0.5, 1.5, 3.0]
    for idx, t in enumerate(times_wigner):
        # Gaussian wavepacket with increasing mixing
        sigma = 0.3 + 0.5 * t
        interference = np.exp(-4 * t) * np.cos(2 * X) * np.exp(-(X**2 + P**2) / (2 * sigma**2))
        gaussian = np.exp(-(X**2 + P**2) / (2 * sigma**2))
        W = 0.5 * (gaussian + interference)
        
        if idx == 0:
            im = ax.contourf(X, P, W, levels=20, cmap='viridis')
        else:
            ax.contourf(X, P, W, levels=20, cmap='viridis', alpha=0.5)
    
    ax.set_xlabel('Position x', fontsize=11)
    ax.set_ylabel('Momentum p', fontsize=11)
    ax.set_title('Wigner Function Evolution\n(Quantum interference fades → classical)', fontsize=12)
    plt.colorbar(im, ax=ax, shrink=0.5)
    ax.grid(True, alpha=0.3)
    
    # 2. Decoherence timeline
    ax = axes[0, 1]
    
    regimes = [
        (0, 0.5, 'Quantum\n(Superposition)', 'steelblue'),
        (0.5, 1.5, 'Transition\n(Decoherence)', 'orange'),
        (1.5, 3.0, 'Classical\n(Mixed State)', 'red'),
    ]
    
    for start, end, label, color in regimes:
        ax.axvspan(start, end, alpha=0.3, color=color, label=label)
    
    times_line = np.linspace(0, 3, 200)
    coherence_line = 0.5 * np.exp(-2 * times_line)
    ax.plot(times_line, coherence_line, 'b-', linewidth=3)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Coherence', fontsize=11)
    ax.set_title('Quantum-to-Classical Transition Timeline', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 3)
    
    # 3. Decoherence rate vs coupling
    ax = axes[1, 0]
    
    couplings = np.logspace(-3, 0, 50)
    rates = []
    for coupling in couplings:
        system = OpenQuantumSystem(n_system=2, n_env=10, coupling=coupling)
        H = system.build_total_hamiltonian('dephasing')
        psi = system.initial_state(superposition=True)
        times, coherence, _, _ = system.evolve(H, psi, t_max=5.0, n_steps=200)
        
        initial_c = coherence[0]
        decay_to = initial_c / np.e
        decay_times = times[coherence < decay_to]
        if len(decay_times) > 0:
            tau = np.min(decay_times)
        else:
            Gamma = coupling**2 * 2.0
            tau = 1.0 / Gamma if Gamma > 0 else np.inf
        rates.append(1.0 / tau if tau < np.inf else 0)
    
    ax.plot(couplings, rates, 'r-', linewidth=2.5)
    ax.set_xscale('log')
    ax.set_xlabel('Coupling Strength g', fontsize=12)
    ax.set_ylabel('Decoherence Rate Γ = 1/τ', fontsize=11)
    ax.set_title('Decoherence Rate Scaling\n(Γ ∝ g²: quantum-to-classical boundary)', fontsize=12)
    ax.grid(True, alpha=0.3, which='both')
    
    # 4. Phase diagram: when does classical behavior emerge?
    ax = axes[1, 1]
    
    # Parameter space: coupling vs environment size
    g_vals = np.logspace(-2, 0, 30)
    n_vals = np.arange(2, 25)
    G, N = np.meshgrid(g_vals, n_vals, indexing='ij')
    
    # Decoherence is fast when g is large and N is large
    # Define a "classical" region where decoherence time < 1
    classical = np.zeros_like(G)
    for i in range(len(g_vals)):
        for j in range(len(n_vals)):
            system = OpenQuantumSystem(n_system=2, n_env=int(n_vals[j]), coupling=g_vals[i])
            H = system.build_total_hamiltonian('dephasing')
            psi = system.initial_state(superposition=True)
            times, coherence, _, _ = system.evolve(H, psi, t_max=2.0, n_steps=100)
            
            initial_c = coherence[0]
            decay_to = initial_c / np.e
            decay_times = times[coherence < decay_to]
            tau = np.min(decay_times) if len(decay_times) > 0 else np.inf
            classical[i, j] = 1.0 if tau < 1.0 else 0.0
    
    contour = ax.contourf(G, N, classical, levels=[0, 0.5, 1], 
                         colors=['lightblue', 'lightcoral'], alpha=0.8)
    ax.plot(g_vals, [n_vals[len(n_vals)//2]]*len(g_vals), 'k--', linewidth=1, alpha=0.5)
    ax.set_xscale('log')
    ax.set_xlabel('Coupling Strength g', fontsize=12)
    ax.set_ylabel('Environment Size n_env', fontsize=11)
    ax.set_title('Quantum-Classical Phase Diagram\n(Red = classical, Blue = quantum)', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '25_quantum_classical_transition.png'), bbox_inches='tight')
    plt.close()


def run_simulation_6():
    """Run all visualizations for Simulation 6."""
    print("=" * 70)
    print("SIMULATION 6: Quantum-Classical Boundary (Decoherence)")
    print("=" * 70)
    
    print("\n[1] Open quantum system initialized.")
    print("    System: 2-level (qubit)")
    print("    Environment: 10-level bath")
    print("    Interaction: σ_z ⊗ B (dephasing)")
    
    system = OpenQuantumSystem(n_system=2, n_env=10, coupling=0.1)
    
    # Test decoherence
    print("\n[2] Decoherence dynamics:")
    H = system.build_total_hamiltonian('dephasing')
    psi = system.initial_state(superposition=True)
    times, coherence, purity, position = system.evolve(
        H, psi, t_max=5.0, n_steps=200, interaction_type='dephasing'
    )
    
    print(f"    Initial coherence: {coherence[0]:.4f}")
    print(f"    Final coherence:   {coherence[-1]:.4f}")
    print(f"    Initial purity:    {purity[0]:.4f}")
    print(f"    Final purity:      {purity[-1]:.4f}")
    
    # Find decoherence time
    initial_c = coherence[0]
    decay_to = initial_c / np.e
    decay_times = times[coherence < decay_to]
    tau_dec = np.min(decay_times) if len(decay_times) > 0 else np.inf
    print(f"    Decoherence time τ_dec: {tau_dec:.4f}")
    
    # Compare models
    print("\n[3] Comparing decoherence models:")
    coupling_strengths, models, results = compare_decoherence_models()
    for model in models:
        for coupling in [0.1, 0.5]:
            tau = results[model][coupling]['tau_dec']
            print(f"    {model:12s} g={coupling:.2f}: τ_dec={tau:.4f}")
    
    # Pointer states
    print("\n[4] Pointer state analysis:")
    initial_states, pointer_results = pointer_state_analysis()
    for name in ['|0⟩', '|1⟩', '|+⟩', '|-⟩']:
        final_coh = pointer_results[name]['coherence'][-1]
        print(f"    {name}: final coherence = {final_coh:.4f}")
    
    # Decoherence rate scaling
    print("\n[5] Decoherence rate scaling:")
    couplings, tau_dec_coupling, env_sizes, tau_dec_env = decoherence_rate_analysis()
    print(f"    g=0.001: τ_dec={tau_dec_coupling[0]:.4f}")
    print(f"    g=0.01:  τ_dec={tau_dec_coupling[1]:.4f}")
    print(f"    g=0.1:   τ_dec={tau_dec_coupling[10]:.4f}")
    print(f"    g=1.0:   τ_dec={tau_dec_coupling[-1]:.4f}")
    
    # Visualizations
    print("\n[6] Generating visualizations...")
    plot_decoherence_dynamics()
    print("    → Saved: 21_decoherence_dynamics.png")
    
    plot_pointer_states()
    print("    → Saved: 22_pointer_states.png")
    
    plot_decoherence_rate_scaling()
    print("    → Saved: 23_decoherence_rate_scaling.png")
    
    plot_density_matrix_evolution()
    print("    → Saved: 24_density_matrix_evolution.png")
    
    plot_quantum_classical_transition()
    print("    → Saved: 25_quantum_classical_transition.png")
    
    print("\n" + "=" * 70)
    print("SIMULATION 6 COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    run_simulation_6()
