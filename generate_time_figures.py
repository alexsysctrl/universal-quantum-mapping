#!/usr/bin/env python3
"""
generate_time_figures.py — Generate visualizations for the Time Research Paper.

This script generates figures for the novel insights sections (2.9–2.13) of
time-research.md, plus updates existing figures if needed.

Figures generated:
  fig11_cohomological_twist.png    — Modular cocycle as twist class
  fig12_time_crystal_spectrum.png  — Discrete vs continuous modular spectrum
  fig13_geometric_arrow.png        — Time gradient as geometric arrow
  fig14_modular_margolus_levitin.png — Modular Margolus-Levitin theorem
  fig15_noncommuting_times.png     — Multiple times from non-commuting flows

Requires: matplotlib, numpy
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import matplotlib.patches as mpatches

OUTPUT_DIR = "/Users/alex/Desktop/work/Universal_Quantum_Mapping/time-figures"
FIGSIZE = (10, 7)
DPI = 150


# =============================================================================
# FIGURE 11: Modular Cocycle as Twist Class
# =============================================================================

def fig11_cohomological_twist():
    """
    Visualize the modular cocycle as a topological twist class.
    Shows: (a) cocycle value vs state, (b) cohomology class invariance,
            (c) 2D CFT result tau_2 = c/12.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel (a): Cocycle value as a function of state parameter
    # Simulate different states omega(lambda) where lambda controls the state
    lambdas = np.linspace(0.1, 5.0, 200)
    # Cocycle value increases with state "twist"
    # For Rindler-like states: tau_2 ~ lambda * c/12
    c = 1.0  # central charge
    tau_2_rindler = lambdas * c / 12.0
    # For thermal states: tau_2 ~ 1/lambda * c/12
    tau_2_thermal = (1.0 / lambdas) * c / 12.0

    axes[0].plot(lambdas, tau_2_rindler, 'b-', linewidth=2, label='Rindler vacuum')
    axes[0].plot(lambdas, tau_2_thermal, 'r-', linewidth=2, label='Thermal state')
    axes[0].axhline(y=c/12, color='g', linestyle='--', linewidth=1.5, label='c/12 (2D CFT)')
    axes[0].set_xlabel(r'State parameter $\lambda$', fontsize=11)
    axes[0].set_ylabel(r'$\tau_2$ (cocycle value)', fontsize=11)
    axes[0].set_title('(a) Cocycle Value Depends on State', fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(0, 0.5)

    # Panel (b): Cohomology class invariance
    # Show that different states give cohomologous cocycles
    states = ['Rindler', 'Thermal', 'Excited', 'Mixed']
    cohomology_classes = [1.0, 1.0, 1.0, 1.0]  # All same cohomology class
    cocycle_values = [0.083, 0.042, 0.125, 0.067]  # Different values

    x_pos = np.arange(len(states))
    bars = axes[1].bar(x_pos, cocycle_values, color=['#2196F3', '#f44336', '#4CAF50', '#FF9800'],
                       alpha=0.7, edgecolor='black', linewidth=1.5)
    axes[1].set_ylabel(r'$\|\tau_2\|$ (cocycle norm)', fontsize=11)
    axes[1].set_title('(b) Different Values, Same Cohomology Class', fontsize=12, fontweight='bold')
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(states, fontsize=9)
    axes[1].grid(True, alpha=0.3, axis='y')
    # Add annotation for cohomology class
    axes[1].text(1.5, 0.14, r'$[\tau_2] \in HC^2(\mathcal{M}) = \mathbb{R}$',
                 fontsize=10, ha='center', bbox=dict(boxstyle='round,pad=0.5',
                 facecolor='yellow', alpha=0.3))

    # Panel (c): Twist class diagram
    # Show the cocycle as a "twist" in the modular flow
    t = np.linspace(0, 4*np.pi, 200)

    # Trivial flow (tau_2 = 0): straight line
    trivial_x = t
    trivial_y = np.zeros_like(t)

    # Twisted flow (tau_2 != 0): oscillating path
    twisted_x = t
    twisted_y = 0.3 * np.sin(t) * np.exp(-0.05 * t)

    axes[2].plot(trivial_x, trivial_y, 'b--', linewidth=2, label='Trivial: $\tau_2 = 0$')
    axes[2].plot(twisted_x, twisted_y, 'r-', linewidth=2, label='Twisted: $\tau_2 \neq 0$')
    axes[2].annotate('', xy=(3*np.pi, 0.1), xytext=(2*np.pi, -0.1),
                     arrowprops=dict(arrowstyle='->', color='green', lw=2))
    axes[2].text(2.5*np.pi, 0.15, r'Twist $\mathcal{T} = \|\tau_2\|$',
                 fontsize=10, color='green', fontweight='bold')
    axes[2].set_xlabel(r'Modular parameter $t$', fontsize=11)
    axes[2].set_ylabel('Twist displacement', fontsize=11)
    axes[2].set_title('(c) Modular Flow: Trivial vs. Twisted', fontsize=12, fontweight='bold')
    axes[2].legend(fontsize=9)
    axes[2].grid(True, alpha=0.3)
    axes[2].set_xlim(0, 4*np.pi)
    axes[2].set_ylim(-0.4, 0.5)

    plt.suptitle('Fig. 11: Time as a Cohomological Twist Class (Section 2.9)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig11_cohomological_twist.png', dpi=DPI,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Created: fig11_cohomological_twist.png")


# =============================================================================
# FIGURE 12: Time Crystals — Discrete vs Continuous Spectrum
# =============================================================================

def fig12_time_crystal_spectrum():
    """
    Visualize Theorem 2.10: Time crystals require discrete modular spectrum.
    Shows: (a) Type III_1 continuous spectrum (no time crystals),
            (b) Type III_lambda discrete spectrum (time crystals possible),
            (c) Type I discrete spectrum (time crystals exist).
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel (a): Type III_1 — continuous spectrum
    # Simulate continuous spectrum on R_+
    x_iii1 = np.linspace(0, 10, 1000)
    # Uniform density (Lebesgue measure)
    rho_iii1 = np.ones_like(x_iii1) * 0.1
    # Thermal weight
    beta = 2 * np.pi
    weight_iii1 = np.exp(-beta * x_iii1)
    combined_iii1 = rho_iii1 * weight_iii1

    axes[0].fill_between(x_iii1, 0, combined_iii1, alpha=0.5, color='red',
                          label='Spectral density $\times$ thermal weight')
    axes[0].plot(x_iii1, combined_iii1, 'r-', linewidth=2)
    axes[0].set_xlabel(r'Modular eigenvalue $\lambda$', fontsize=11)
    axes[0].set_ylabel('Combined measure', fontsize=11)
    axes[0].set_title('(a) Type III$_1$: CONTINUOUS\nNo Time Crystals',
                      fontsize=12, fontweight='bold', color='red')
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(0, 0.15)
    # Add annotation
    axes[0].text(5, 0.12, r'Sp($\Delta$) = $\mathbb{R}_+$\nNo discrete eigenvalues\nTime crystal: IMPOSSIBLE',
                 fontsize=9, ha='center', bbox=dict(boxstyle='round,pad=0.5',
                 facecolor='#ffebee', alpha=0.8))

    # Panel (b): Type III_lambda — discrete spectrum
    # Discrete eigenvalues lambda^n
    lam = 0.5  # lambda parameter
    n_vals = np.arange(-5, 10)
    eigenvalues_iii_lambda = lam ** n_vals
    discrete_rho_iii_lambda = np.ones_like(eigenvalues_iii_lambda) * 0.15
    # Only positive eigenvalues
    mask = eigenvalues_iii_lambda > 0
    ev_pos = eigenvalues_iii_lambda[mask]
    dr_pos = discrete_rho_iii_lambda[mask]

    axes[1].stem(ev_pos, dr_pos, linefmt='b-', markerfmt='bo', basefmt='k-')
    axes[1].set_xlabel(r'Modular eigenvalue $\lambda = ' + str(lam) + '^n$', fontsize=11)
    axes[1].set_ylabel('Spectral density', fontsize=11)
    axes[1].set_title('(b) Type III$_' + str(lam) + '$: DISCRETE\nTime Crystals Possible',
                      fontsize=12, fontweight='bold', color='blue')
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(0, 0.2)
    # Add annotation
    spacing = -np.log(lam)
    axes[1].text(1.5, 0.17, r'Sp($\Delta$) = {' + str(lam) + r'^n}\nSpacing: $|\log ' + str(lam) + r'|$\nModular period: $T = 2\pi/|\log ' + str(lam) + r'|$',
                 fontsize=8, ha='center', bbox=dict(boxstyle='round,pad=0.5',
                 facecolor='#e3f2fd', alpha=0.8))

    # Panel (c): Type I — finite discrete spectrum
    # Finite number of eigenvalues
    n_levels = 8
    type1_eigenvalues = np.arange(1, n_levels + 1)
    type1_rho = np.ones_like(type1_eigenvalues) * 0.12

    axes[2].stem(type1_eigenvalues, type1_rho, linefmt='g-', markerfmt='go', basefmt='k-')
    axes[2].set_xlabel('Level number $n$', fontsize=11)
    axes[2].set_ylabel('Spectral density', fontsize=11)
    axes[2].set_title('(c) Type I: FINITE DISCRETE\nTime Crystals EXIST',
                      fontsize=12, fontweight='bold', color='green')
    axes[2].grid(True, alpha=0.3)
    axes[2].set_ylim(0, 0.18)
    # Add annotation
    axes[2].text(4.5, 0.15, r'Finite spectrum\nTime crystals: OBSERVED\n(trapped ions, NV centers,\nsuperconducting qubits)',
                 fontsize=8, ha='center', bbox=dict(boxstyle='round,pad=0.5',
                 facecolor='#e8f5e9', alpha=0.8))

    plt.suptitle('Fig. 12: Time Crystals Require Discrete Modular Spectrum (Theorem 2.10)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig12_time_crystal_spectrum.png', dpi=DPI,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Created: fig12_time_crystal_spectrum.png")


# =============================================================================
# FIGURE 13: Geometric Arrow of Time — Time Gradient
# =============================================================================

def fig13_geometric_arrow():
    """
    Visualize the time gradient as the geometric arrow of time.
    Shows: (a) negatively curved state space with geodesic divergence,
            (b) time gradient direction, (c) curvature sign vs arrow direction.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel (a): Negatively curved state space with geodesic divergence
    # Simulate hyperbolic geometry (Poincare disk)
    theta = np.linspace(0, 2*np.pi, 100)
    r_max = 0.9

    # Draw Poincare disk
    disk = Circle((0, 0), r_max, fill=False, edgecolor='black', linewidth=2)
    axes[0].add_patch(disk)

    # Draw geodesics diverging from center
    num_geodesics = 8
    for i in range(num_geodesics):
        angle = 2 * np.pi * i / num_geodesics
        # Geodesics in Poincare disk are arcs orthogonal to boundary
        r = np.linspace(0, r_max - 0.05, 100)
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        axes[0].plot(x, y, 'b-', linewidth=1.5, alpha=0.6)

    # Mark the central state
    axes[0].plot(0, 0, 'ro', markersize=12, label='Primordial state $\omega_0$')

    # Show divergence
    r_div = 0.5
    angle1 = np.pi / 6
    angle2 = -np.pi / 6
    x1, y1 = r_div * np.cos(angle1), r_div * np.sin(angle1)
    x2, y2 = r_div * np.cos(angle2), r_div * np.sin(angle2)
    axes[0].plot([x1, x2], [y1, y2], 'r--', linewidth=2, label='Geodesic divergence')
    axes[0].text(0, -0.7, r'$\xi(t) = \xi(0) \cdot \cosh(\sqrt{-K_{max}} \cdot t)$',
                 fontsize=10, ha='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

    axes[0].set_aspect('equal')
    axes[0].set_xlim(-1, 1)
    axes[0].set_ylim(-1, 1)
    axes[0].set_title('(a) Negative Curvature: Geodesic Divergence',
                      fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=8, loc='upper right')
    axes[0].grid(True, alpha=0.2)
    axes[0].set_xlabel('State space coordinate 1', fontsize=9)
    axes[0].set_ylabel('State space coordinate 2', fontsize=9)

    # Panel (b): Time gradient direction
    # Show state space with gradient arrows
    X, Y = np.meshgrid(np.linspace(-1, 1, 15), np.linspace(-1, 1, 15))
    # Time gradient points in direction of K (modular Hamiltonian)
    # For simplicity, assume K points in +x direction
    U = X / (1 + X**2 + Y**2)  # Gradient field
    V = np.zeros_like(U)

    axes[1].quiver(X, Y, U, V, alpha=0.5, color='blue', scale=30)
    # Mark the time gradient direction
    axes[1].arrow(-0.8, 0, 1.4, 0, head_width=0.15, head_length=0.1,
                  fc='red', ec='red', linewidth=3)
    axes[1].text(0.2, 0.35, r'$\vec{t} = \nabla_\tau / \|\nabla_\tau\|$',
                 fontsize=11, ha='center', fontweight='bold', color='red',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffebee', alpha=0.8))
    axes[1].text(-0.8, -0.35, r'$\nabla_\tau = \arg\max_{\|X\|=1} \|[X, K]\|$',
                 fontsize=9, ha='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.5))

    axes[1].set_aspect('equal')
    axes[1].set_xlim(-1, 1)
    axes[1].set_ylim(-1, 1)
    axes[1].set_title('(b) Time Gradient: Direction of Fastest Modular Flow',
                      fontsize=12, fontweight='bold')
    axes[1].set_xlabel('State space coordinate 1', fontsize=9)
    axes[1].set_ylabel('State space coordinate 2', fontsize=9)
    axes[1].grid(True, alpha=0.2)

    # Panel (c): Curvature sign vs arrow direction
    curvature_signs = ['Negative\nK < 0', 'Zero\nK = 0', 'Positive\nK > 0']
    arrow_directions = ['Forward →', 'No arrow', 'Backward ←']
    arrow_colors = ['red', 'gray', 'blue']
    arrow_descriptions = [
        'Arrow points toward\nfastest modular flow\n(entropy increases)',
        'No preferred direction\n(thermal equilibrium)',
        'Arrow points toward\nslowest modular flow\n(entropy decreases)'
    ]

    x_pos = np.arange(3)
    bar_heights = [1.0, 0.0, 1.0]

    bars = axes[2].bar(x_pos, bar_heights, color=arrow_colors, alpha=0.7,
                        edgecolor='black', linewidth=2)
    # Add arrow annotations
    for i, (desc, color) in enumerate(zip(arrow_descriptions, arrow_colors)):
        if i == 0:
            axes[2].text(i, 0.5, '→', fontsize=40, ha='center', va='center', color='red')
        elif i == 2:
            axes[2].text(i, 0.5, '←', fontsize=40, ha='center', va='center', color='blue')
        else:
            axes[2].text(i, 0.5, '—', fontsize=40, ha='center', va='center', color='gray')

    axes[2].set_ylabel('Curvature magnitude', fontsize=11)
    axes[2].set_title('(c) Curvature Sign Determines Arrow Direction',
                      fontsize=12, fontweight='bold')
    axes[2].set_xticks(x_pos)
    axes[2].set_xticklabels(curvature_signs, fontsize=9)
    axes[2].set_ylim(0, 1.3)
    axes[2].grid(True, alpha=0.3, axis='y')

    plt.suptitle('Fig. 13: Time Gradient as Geometric Arrow of Time (Section 2.11)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig13_geometric_arrow.png', dpi=DPI,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Created: fig13_geometric_arrow.png")


# =============================================================================
# FIGURE 14: Modular Margolus-Levitin Theorem
# =============================================================================

def fig14_modular_margolus_levitin():
    """
    Visualize the Modular Margolus-Levitin theorem.
    Shows: (a) comparison of standard ML bound vs modular bound,
            (b) time cost vs modular Hamiltonian change,
            (c) physical interpretation diagram.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel (a): Standard ML vs Modular bound
    # Standard ML: delta_t >= hbar / (2 * delta_E)
    # Modular: delta_t >= hbar / ||K' - K||
    delta_E_vals = np.linspace(0.1, 5.0, 200)
    dK_vals = np.linspace(0.1, 5.0, 200)
    hbar = 1.0  # natural units

    ml_bound = hbar / (2 * delta_E_vals)
    modular_bound = hbar / dK_vals

    axes[0].plot(delta_E_vals, ml_bound, 'b-', linewidth=2.5,
                 label=r'Margolus-Levitin: $\Delta t \geq \hbar/(2\Delta E)$')
    axes[0].plot(dK_vals, modular_bound, 'r-', linewidth=2.5,
                 label=r'Modular: $\Delta t \geq \hbar/\|K\' - K\|$')
    axes[0].set_xlabel('Energy uncertainty / Modular change', fontsize=11)
    axes[0].set_ylabel(r'Minimum time $\Delta t_{\text{min}}$', fontsize=11)
    axes[0].set_title('(a) Standard ML vs Modular Bound',
                      fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(0, 5)
    axes[0].set_ylim(0, 5)

    # Panel (b): Time cost vs modular Hamiltonian change
    # Show that time cost decreases as modular change increases
    dK = np.linspace(0.1, 10.0, 200)
    time_cost_modular = hbar / dK
    time_cost_ml = hbar / (2 * np.ones_like(dK))  # constant for comparison

    axes[1].plot(dK, time_cost_modular, 'r-', linewidth=2.5,
                 label=r'Modular bound: $\hbar/\|K_{\omega\prime} - K_\omega\|$')
    axes[1].plot(dK, time_cost_ml, 'b--', linewidth=2,
                 label=r'ML bound (constant): $\hbar/2$')
    axes[1].set_xlabel(r'$\|K_{\omega\prime} - K_\omega\|$', fontsize=11)
    axes[1].set_ylabel(r'Minimum time $\Delta t_{\text{min}}$', fontsize=11)
    axes[1].set_title('(b) Time Cost vs Modular Change',
                      fontsize=12, fontweight='bold')
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(0, 10)
    axes[1].set_ylim(0, 10)

    # Panel (c): Physical interpretation
    # Diagram showing state change and time cost
    ax3 = axes[2]
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')

    # State omega
    circle1 = Circle((2, 5), 0.8, fill=True, facecolor='lightblue',
                     edgecolor='blue', linewidth=2)
    ax3.add_patch(circle1)
    ax3.text(2, 5, r'$\omega$', fontsize=16, ha='center', va='center', fontweight='bold')
    ax3.text(2, 3.5, r'$K_\omega$', fontsize=11, ha='center')

    # Arrow showing state change
    arrow = FancyArrowPatch((3, 5), (6.5, 5),
                           arrowstyle='->', mutation_scale=30, linewidth=3,
                           color='red')
    ax3.add_patch(arrow)
    ax3.text(4.75, 5.8, r'State change\n$\omega \to \omega\prime$',
             fontsize=10, ha='center', fontweight='bold', color='red')

    # State omega'
    circle2 = Circle((7.5, 5), 0.8, fill=True, facecolor='lightcoral',
                     edgecolor='red', linewidth=2)
    ax3.add_patch(circle2)
    ax3.text(7.5, 5, r"$\omega\prime$", fontsize=16, ha='center', va='center', fontweight='bold')
    ax3.text(7.5, 3.5, r"$K_{\omega\prime}$", fontsize=11, ha='center')

    # Time cost annotation
    ax3.text(5, 1.5, r'Minimum time: $\Delta t_{\text{min}} \geq \hbar / \|K_{\omega\prime} - K_\omega\|$',
             fontsize=11, ha='center',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', alpha=0.5))

    ax3.text(5, 0.3, 'Key difference: Modular bound uses CHANGE in modular\n' +
             'Hamiltonian, not energy uncertainty in a single state',
             fontsize=9, ha='center', style='italic')

    axes[2].set_title('(c) Physical Interpretation',
                      fontsize=12, fontweight='bold')

    plt.suptitle('Fig. 14: Modular Margolus-Levitin Theorem (Section 2.12)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig14_modular_margolus_levitin.png', dpi=DPI,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Created: fig14_modular_margolus_levitin.png")


# =============================================================================
# FIGURE 15: Multiple Times from Non-Commuting Modular Flows
# =============================================================================

def fig15_noncommuting_times():
    """
    Visualize multiple times from non-commuting modular flows.
    Shows: (a) commuting flows (single time), (b) non-commuting flows (multiple times),
            (c) physical example diagram.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel (a): Commuting modular flows — single time
    t = np.linspace(0, 10, 200)

    # Flow 1: period T1 = 2pi
    flow1_a = np.sin(t * 2 * np.pi / (2*np.pi))
    # Flow 2: period T2 = 2pi (commuting with flow 1)
    flow2_a = np.sin(t * 2 * np.pi / (2*np.pi) + 0.5)

    axes[0].plot(t, flow1_a, 'b-', linewidth=2, label='Flow 1: $\sigma_t^{\omega_1}$')
    axes[0].plot(t, flow2_a, 'r-', linewidth=2, label='Flow 2: $\sigma_t^{\omega_2}$')
    axes[0].set_xlabel('Modular parameter $t$', fontsize=11)
    axes[0].set_ylabel('Observable value', fontsize=11)
    axes[0].set_title('(a) Commuting Flows: Single Time\n$[\sigma^{\omega_1}, \sigma^{\omega_2}] = 0$',
                      fontsize=12, fontweight='bold', color='blue')
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(-1.5, 1.5)

    # Panel (b): Non-commuting modular flows — multiple times
    t1 = np.linspace(0, 10, 200)
    t2 = np.linspace(0, 10, 200)

    # Flow 1: period T1 = 2pi (fast)
    flow1_b = np.sin(t1 * 2 * np.pi / (2*np.pi))
    # Flow 2: period T2 = 4pi (slow), non-commuting
    flow2_b = np.sin(t2 * 2 * np.pi / (4*np.pi) + 0.3)

    axes[1].plot(t1, flow1_b, 'b-', linewidth=2, label='Flow 1: $\sigma_{t_1}^{\omega_1}$ (fast)')
    axes[1].plot(t2, flow2_b, 'r-', linewidth=2, label='Flow 2: $\sigma_{t_2}^{\omega_2}$ (slow)')
    axes[1].set_xlabel('Time parameter', fontsize=11)
    axes[1].set_ylabel('Observable value', fontsize=11)
    axes[1].set_title('(b) Non-Commuting Flows: Multiple Times\n$[\sigma^{\omega_1}, \sigma^{\omega_2}] \\neq 0$',
                      fontsize=12, fontweight='bold', color='red')
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(-1.5, 1.5)
    # Add annotation for two time parameters
    axes[1].text(5, -1.3, r'Two independent times: $t_1, t_2$\nEvolution: $\sigma_{t_1, t_2}^{\omega_1, \omega_2}$',
                 fontsize=9, ha='center',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffebee', alpha=0.8))

    # Panel (c): Physical example — composite system
    ax3 = axes[2]
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')

    # Draw two subsystems
    rect1 = Rectangle((0.5, 3), 3.5, 4, fill=True, facecolor='lightblue',
                       edgecolor='blue', linewidth=2)
    ax3.add_patch(rect1)
    ax3.text(2.25, 6, r'Subsystem 1', fontsize=12, ha='center', fontweight='bold')
    ax3.text(2.25, 5, r'$\mathcal{M}_1$', fontsize=11, ha='center')
    ax3.text(2.25, 4, r'$T_1 = 2\pi/(k_B T_1)$', fontsize=9, ha='center')

    rect2 = Rectangle((6, 3), 3.5, 4, fill=True, facecolor='lightcoral',
                       edgecolor='red', linewidth=2)
    ax3.add_patch(rect2)
    ax3.text(7.75, 6, r'Subsystem 2', fontsize=12, ha='center', fontweight='bold')
    ax3.text(7.75, 5, r'$\mathcal{M}_2$', fontsize=11, ha='center')
    ax3.text(7.75, 4, r'$T_2 = 2\pi/(k_B T_2)$', fontsize=9, ha='center')

    # Entanglement link
    ax3.plot([4, 6], [5, 5], 'g--', linewidth=2, label='Entanglement')
    ax3.text(5, 5.5, 'Entangled', fontsize=9, ha='center', color='green', style='italic')

    # Two times annotation
    ax3.text(5, 1.5, 'Multiple times emerge when:\n' +
             '1. M = M1 tensor M2\n' +
             '2. T1 != T2 (different periods)\n' +
             '3. [sigma^1, sigma^2] != 0 (non-commuting)',
             fontsize=9, ha='center',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', alpha=0.5))

    axes[2].set_title('(c) Physical Example: Composite Entangled System',
                      fontsize=12, fontweight='bold')

    plt.suptitle('Fig. 15: Multiple Times from Non-Commuting Modular Flows (Section 2.13)',
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/fig15_noncommuting_times.png', dpi=DPI,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Created: fig15_noncommuting_times.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("Generating novel insight figures for time-research.md...")
    fig11_cohomological_twist()
    fig12_time_crystal_spectrum()
    fig13_geometric_arrow()
    fig14_modular_margolus_levitin()
    fig15_noncommuting_times()
    print("Done. All 5 novel insight figures created.")


if __name__ == '__main__':
    main()
