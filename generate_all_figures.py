#!/usr/bin/env python3
"""
generate_all_figures.py — Generate all 15 publication-quality cosmic timeline figures.

Framework: Modular Clifford Category (MCC)
Output: PNG (300 DPI) + PDF for each figure
Directory: .//cosmic-figures/
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Polygon, Wedge, Ellipse
from matplotlib.collections import LineCollection
from matplotlib.gridspec import GridSpec
from scipy import interpolate
import warnings
warnings.filterwarnings('ignore')

# ─── Global styling ───────────────────────────────────────────────────────────
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Computer Modern Roman']
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['axes.labelsize'] = 11
mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.titlesize'] = 14
mpl.rcParams['axes.titleweight'] = 'bold'
mpl.rcParams['legend.fontsize'] = 9
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['figure.figsize'] = (10, 8)
mpl.rcParams['axes.linewidth'] = 1.2
mpl.rcParams['xtick.major.width'] = 1.2
mpl.rcParams['ytick.major.width'] = 1.2
mpl.rcParams['axes.grid'] = True
mpl.rcParams['grid.alpha'] = 0.3

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Color palette (colorblind-friendly) ──────────────────────────────────────
CYAN = '#00BFC4'
MAGENTA = '#F58231'
YELLOW = '#FED976'
GREEN = '#77CC85'
RED = '#EF553B'
BLUE = '#0072B2'
PURPLE = '#9E7CCB'
ORANGE = '#FF9900'
TEAL = '#009988'
PINK = '#CC6699'
DARK_BLUE = '#1B4F72'
DARK_GREEN = '#2D6A4F'
DARK_RED = '#9B2226'
LIGHT_GRAY = '#D4D4D4'
WHITE = '#FFFFFF'
BLACK = '#000000'

ERA_COLORS = {
    'quantum': BLUE,
    'particle': PURPLE,
    'astrophysical': DARK_GREEN,
    'biological': TEAL,
    'future': DARK_RED,
}

# ─── Helper functions ─────────────────────────────────────────────────────────
def save_fig(fig, name, tight=True):
    """Save figure as both PNG and PDF."""
    png_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    pdf_path = os.path.join(OUTPUT_DIR, f"{name}.pdf")
    if tight:
        fig.savefig(png_path, bbox_inches='tight', dpi=300, facecolor='white')
        fig.savefig(pdf_path, bbox_inches='tight', dpi=300, facecolor='white')
    else:
        fig.savefig(png_path, dpi=300, facecolor='white')
        fig.savefig(pdf_path, dpi=300, facecolor='white')
    plt.close(fig)
    print(f"  Saved: {png_path}, {pdf_path}")

def latex_label(text):
    """Wrap text in LaTeX math mode for matplotlib."""
    return f"${text}$"


# =============================================================================
# FIGURE 1: Timeline of the Universe
# =============================================================================
def figure_1_timeline():
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))

    # Epochs: (log_time_seconds, label, era, size_description)
    # log_time_seconds = log10(time in seconds from Planck time onward
    epochs = [
        # (log_t_s, label, era, y_pos, size)
        (0, 'Planck\nEpoch', 'quantum', 0, '10^-35 m'),
        (0.3, 'Inflation\nBegins', 'quantum', 0.5, '10^-26 m'),
        (1.1, 'Inflation\nEnds', 'quantum', 1.0, '10^-10 m'),
        (3.2, 'Reheating', 'quantum', 1.5, '10^-10 m'),
        (6.3, 'Electroweak\nEpoch', 'particle', 2.0, '10^-10 m'),
        (8.3, 'Quark\nEpoch', 'particle', 2.5, '1 fm'),
        (9.3, 'Hadron\nEpoch', 'particle', 3.0, '1 fm'),
        (10.3, 'Lepton\nEpoch', 'particle', 3.5, '10^-10 m'),
        (11, 'Photon\nEpoch', 'particle', 4.0, 'Atomic'),
        (18.6, 'Recombination\n(CMB)', 'astrophysical', 4.5, '10^20 m'),
        (21.3, 'Dark Ages', 'astrophysical', 5.0, '10^21 m'),
        (24.3, 'First Stars', 'astrophysical', 5.5, '10^22 m'),
        (26.3, 'Galaxy\nFormation', 'astrophysical', 6.0, '10^23 m'),
        (28.9, 'Solar System\nForms', 'astrophysical', 6.5, '10^13 m'),
        (29.6, 'Life on\nEarth', 'biological', 7.0, '10^-9 m (DNA)'),
        (30.5, 'Human\nConsciousness', 'biological', 7.5, '10^10 m (brain)'),
        (31.2, 'Present\nDay', 'biological', 8.0, '10^26 m (observable)'),
        (37.5, 'Star Formation\nEnds', 'future', 6.0, '10^27 m'),
        (45, 'Black Hole\nEra', 'future', 5.0, '10^28 m'),
        (55, 'Dark Era', 'future', 4.0, '10^30 m'),
        (75, 'Heat Death', 'future', 3.0, '10^40 m'),
    ]

    # Draw the timeline axis
    ax.axhline(y=4.5, color=BLACK, linewidth=2, zorder=1)

    # Draw epoch bars
    for i, (log_t, label, era, y_pos, size) in enumerate(epochs):
        x = log_t
        color = ERA_COLORS[era]

        # Epoch bar
        bar_height = 0.35
        bar = FancyBboxPatch((x - 0.15, y_pos - bar_height/2), 0.3, bar_height,
                              boxstyle="round,pad=0.02",
                              facecolor=color, edgecolor='black',
                              linewidth=1.2, alpha=0.85, zorder=3)
        ax.add_patch(bar)

        # Vertical line from bar to axis
        ax.plot([x, x], [y_pos, 4.5], color=color, linewidth=1.5, zorder=2, alpha=0.7)

        # Label
        ax.text(x, y_pos + 0.6, label, ha='center', va='bottom',
                fontsize=8, fontweight='bold', rotation=0)

        # Size annotation
        ax.text(x, y_pos - 0.7, size, ha='center', va='top',
                fontsize=7, style='italic', color='gray')

    # Add era legend at top
    era_patches = []
    for era_name, color in ERA_COLORS.items():
        era_patches.append(plt.Rectangle((0, 0), 0.04, 0.04,
                                         facecolor=color, edgecolor='black',
                                         linewidth=1, label=era_name.capitalize()))

    ax.legend(handles=era_patches, loc='upper left', fontsize=9,
              title='Cosmic Era', framealpha=0.9, title_fontsize=11)

    # X-axis
    ax.set_xlabel('log₁₀(Time / seconds)', fontsize=13, fontweight='bold')
    ax.set_xlim(-0.5, 80)
    ax.set_ylim(0, 9)

    # X-axis ticks
    x_ticks = [0, 1, 10, 18.6, 26.3, 31.2, 45, 75]
    x_labels = ['Planck\n(10⁻⁴³s)', '10⁻⁴²', '10⁻³³', 'Recomb.\n(380k yr)',
                 'Galaxies\n(10 Gyr)', 'Present\n(13.8 Gyr)', 'BH Era\n(10⁴⁰ yr)', 'Heat Death']
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, fontsize=7, rotation=30, ha='right')

    # Add annotation for the "before" region
    ax.annotate('Before the Big Bang\n(Timeless Primordial State)',
                xy=(-0.3, 5), xytext=(-0.3, 7),
                arrowprops=dict(arrowstyle='->', color=LIGHT_GRAY, lw=2),
                fontsize=9, ha='center', color=LIGHT_GRAY,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#222222', alpha=0.8, edgecolor=LIGHT_GRAY))

    # Title
    ax.set_title('The Complete Cosmic Timeline\nFrom Planck Epoch to Heat Death',
                 fontsize=15, fontweight='bold', pad=15)

    # Add formula annotation
    ax.text(0.5, 0.02, r'$\sigma_t^\omega(M) = \Delta_\omega^{it} M \Delta_\omega^{-it}$' +
            '  —  Time is the modular automorphism group',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=9, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F0F0', edgecolor=BLUE, linewidth=1.5))

    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    save_fig(fig, 'fig01_cosmic_timeline')


# =============================================================================
# FIGURE 2: Temperature vs Time
# =============================================================================
def figure_2_temperature():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Time in seconds (log scale)
    t = np.logspace(-43, 37.5, 2000)  # Planck time to ~10^37 seconds (~10^100 years)
    # Temperature profile (simplified physics)
    T = np.zeros_like(t)

    for i, ti in enumerate(t):
        if ti < 1e-36:  # Planck to inflation
            T[i] = 1e32 * np.exp(-5 * (ti - 1e-43) / 1e-36)
        elif ti < 1e-32:  # Inflation
            T[i] = 1e28 * (1e-36 / ti)**0.5
        elif ti < 1e-12:  # Reheating
            T[i] = 1e15 * np.exp(-3 * (ti - 1e-32) / 1e-12)
        elif ti < 1e-4:   # Quark/Hadron
            T[i] = 1e12 * (1e-6 / ti)**0.5
        elif ti < 1:      # Lepton
            T[i] = 1e9 * (1 / ti)**0.5
        elif ti < 1e6:    # Photon epoch
            T[i] = 1e8 * (10 / ti)**0.5
        elif ti < 3.8e5 * 365 * 86400:  # Recombination
            T[i] = 3000 * (3.8e5 * 365 * 86400 / ti)**0.5
        elif ti < 1e17:   # Post-recombination, CMB cooling
            T[i] = 2.7 * (3.8e5 * 365 * 86400 / ti)**0.5
        else:             # Far future
            T[i] = 2.7 * np.exp(-0.1 * (ti / 1e17))

    # Plot
    ax.loglog(t, T, color=DARK_BLUE, linewidth=2.5, zorder=5)

    # Shade different eras
    era_shades = [
        (1e-43, 1e-36, 'quantum', 'Quantum Epoch', '#0072B2'),
        (1e-36, 1e-32, 'particle', 'Inflation', '#9E7CCB'),
        (1e-32, 1e-12, 'particle', 'Reheating', '#9E7CCB'),
        (1e-12, 1e-4, 'particle', 'Particle Epoch', '#77CC85'),
        (1e-4, 3.8e5*365*86400, 'astrophysical', 'Astrophysical Epoch', '#2D6A4F'),
        (3.8e5*365*86400, 1e17, 'biological', 'Biological Epoch', '#009988'),
        (1e17, 1e38, 'future', 'Future Epoch', '#9B2226'),
    ]

    for t1, t2, era, label, color in era_shades:
        ax.axvspan(t1, t2, alpha=0.08, color=color, zorder=1)

    # Key temperature markers
    markers = [
        (1e-43, 1e32, 'Planck Temp\n10³² K', 'o', DARK_BLUE),
        (1e-32, 1e15, 'Reheating\n10¹⁵ K', 's', PURPLE),
        (1e-10, 1e12, 'Electroweak\n10¹² K', '^', MAGENTA),
        (1e-4, 1e11, 'Hadron\n10¹¹ K', 'D', ORANGE),
        (3.8e5*365*86400, 3000, 'Recombination\n3000 K', 'v', GREEN),
        (1e17, 2.7, 'CMB Today\n2.7 K', 'p', CYAN),
        (1e37, 1e-30, 'Heat Death\n→ 0 K', 'h', DARK_RED),
    ]

    for ti, Ti, label, marker, color in markers:
        ax.plot(ti, Ti, marker=marker, markersize=10, color=color,
                zorder=6, markeredgecolor='black', markeredgewidth=1)
        ax.annotate(label, xy=(ti, Ti), xytext=(ti * 3, Ti * 3),
                    fontsize=8, color=color, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.2),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor=color, alpha=0.9))

    # Labels
    ax.set_xlabel('Time (seconds)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Temperature (Kelvin)', fontsize=13, fontweight='bold')
    ax.set_title('Cosmic Temperature Evolution\nFrom Planck Temperature to Heat Death',
                 fontsize=15, fontweight='bold', pad=15)

    # Add MCC formula
    ax.text(0.5, 0.02, r'$T = \frac{1}{2\pi\beta} \quad \text{and} \quad K_\omega = -\log\Delta_\omega$',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=10, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F0F0',
                      edgecolor=DARK_BLUE, linewidth=1.5))

    ax.grid(True, which='both', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'fig02_temperature_vs_time')


# =============================================================================
# FIGURE 3: Entropy vs Time
# =============================================================================
def figure_3_entropy():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Time in years (log scale)
    t_yr = np.logspace(-25, 100, 3000)  # From ~10^-25 years to 10^100 years
    t_s = t_yr * 365.25 * 86400

    # Entropy profile (S in units of k_B)
    # S starts low at Big Bang, increases through structure formation,
    # peaks at black hole era, then saturates
    S = np.zeros_like(t_yr)

    for i, ti in enumerate(t_yr):
        if ti < 1e-10:  # Early universe: low entropy
            S[i] = 1e10 * (ti / 1e-43)**0.5
        elif ti < 3.8e5:  # Recombination: entropy jump
            S[i] = 1e10 * (1e-10 / 1e-43)**0.5 * (ti / 1e-10)**0.3
        elif ti < 1e9:  # Structure formation: rapid increase
            S[i] = 1e12 * (ti / 3.8e5)**1.5
        elif ti < 1e12:  # Galaxy era: continued growth
            S[i] = 1e15 * (ti / 1e9)**0.8
        elif ti < 1e14:  # Present: slow growth
            S[i] = 1e16 * (ti / 1e12)**0.3
        elif ti < 1e17:  # Star formation ends
            S[i] = 1e17 * (ti / 1e14)**0.1
        elif ti < 1e40:  # Black hole era: entropy dominated by BH
            S[i] = 1e45 * (1 - np.exp(-(ti - 1e17) / 1e30))
        elif ti < 1e100:  # Heat death: saturation
            S[i] = 1e45 + 1e44 * np.log(1 + (ti - 1e40) / 1e40)
        else:
            S[i] = 2e45

    ax.semilogx(t_yr, S, color=DARK_BLUE, linewidth=2.5, zorder=5)

    # Shade entropy regions
    ax.axvspan(1e-25, 3.8e5, alpha=0.1, color=BLUE, label='Quantum/Particle Era')
    ax.axvspan(3.8e5, 1e12, alpha=0.1, color=GREEN, label='Structure Formation')
    ax.axvspan(1e12, 1e40, alpha=0.1, color=ORANGE, label='Black Hole Era')
    ax.axvspan(1e40, 1e101, alpha=0.1, color=DARK_RED, label='Heat Death')

    # Entropy jump markers
    jumps = [
        (1e-36, 'Inflation Jump', '↑', DARK_BLUE),
        (3.8e5, 'Recombination Jump', '↑', PURPLE),
        (1e8, 'Structure Formation', '↑', GREEN),
        (1e40, 'BH Formation', '↑', ORANGE),
    ]

    for tj, jl, arrow, color in jumps:
        ax.annotate(jl, xy=(tj, S[np.argmin(np.abs(t_yr - tj))]),
                    xytext=(tj * 5, S[np.argmin(np.abs(t_yr - tj))] * 1.5),
                    fontsize=9, color=color, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=color, lw=2),
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                              edgecolor=color, alpha=0.9))

    # Arrow of time
    ax.annotate('', xy=(1e90, 1e44), xytext=(1e5, 1e12),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=3, alpha=0.5))
    ax.text(1e47, 5e13, 'Arrow of Time\n(dS/dt > 0)', fontsize=11,
            fontweight='bold', ha='center', color=BLACK, alpha=0.7)

    ax.set_xlabel('Time (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Entropy (units of k_B)', fontsize=13, fontweight='bold')
    ax.set_title('Cosmic Entropy Evolution\nFrom Minimum (Big Bang) to Maximum (Heat Death)',
                 fontsize=15, fontweight='bold', pad=15)

    ax.text(0.5, 0.02, r'$\frac{dS}{dt} \geq 0 \quad \text{and} \quad S_A = \frac{\text{Area}(\gamma_A)}{4G_N}$',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=10, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F0F0',
                      edgecolor=DARK_BLUE, linewidth=1.5))

    ax.grid(True, which='both', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'fig03_entropy_vs_time')


# =============================================================================
# FIGURE 4: Scale of Observable Universe vs Time
# =============================================================================
def figure_4_scale():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Time in years
    t_yr = np.logspace(-25, 100, 3000)
    t_s = t_yr * 365.25 * 86400

    # Observable universe size (meters)
    R = np.zeros_like(t_yr)

    for i, ti in enumerate(t_yr):
        if ti < 1e-36:  # Planck to inflation start
            R[i] = 1e-35 * (ti / 1e-43)**0.5
        elif ti < 1e-32:  # Inflation
            R[i] = 1e-26 * np.exp(60 * (ti - 1e-36) / 1e-36)
        elif ti < 1e12:  # Post-inflation to present
            R[i] = 1e26 * (ti / 1e12)**0.67  # matter-dominated scaling
        elif ti < 1e17:  # Present to near future
            R[i] = 4.4e26 * (ti / 1.38e10)**0.8
        else:  # Dark energy dominated
            R[i] = 4.4e26 * np.exp(0.05 * (ti - 1e17) / 1e17)

    ax.loglog(t_yr, R, color=DARK_BLUE, linewidth=2.5, zorder=5)

    # Reference scales
    refs = [
        (1e-10, 'Atomic\nscale', CYAN),
        (1e9, 'Stellar\nscale', GREEN),
        (1e19, 'Galactic\nscale', PURPLE),
        (1e24, 'Supercluster\nscale', ORANGE),
        (4.4e26, 'Observable\nUniverse (today)', DARK_BLUE),
    ]

    for ref_r, ref_label, ref_color in refs:
        ax.axhline(y=ref_r, color=ref_color, linestyle='--', linewidth=1, alpha=0.5)
        ax.annotate(ref_label, xy=(1e10, ref_r), xytext=(1e12, ref_r * 1.5),
                    fontsize=8, color=ref_color, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=ref_color, lw=1),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor=ref_color, alpha=0.8))

    # Key events
    events = [
        (1e-43, 'Planck length', 1e-35, DARK_BLUE),
        (1e-32, 'Inflation end', 1e-1, PURPLE),
        (3.8e5, 'Recombination', 1e20, GREEN),
        (1.38e10, 'Today', 4.4e26, DARK_BLUE),
        (1e100, 'Far future', 1e40, DARK_RED),
    ]

    for te, el, er, ec in events:
        ax.plot(te, er, 'o', markersize=8, color=ec, markeredgecolor='black',
                markeredgewidth=1, zorder=6)
        ax.annotate(el, xy=(te, er), xytext=(te * 3, er * 2),
                    fontsize=8, color=ec, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=ec, lw=1.2),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor=ec, alpha=0.9))

    ax.set_xlabel('Time (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Observable Universe Radius (meters)', fontsize=13, fontweight='bold')
    ax.set_title('Scale of the Observable Universe vs Time\nFrom Planck Length to Future Expansion',
                 fontsize=15, fontweight='bold', pad=15)

    ax.text(0.5, 0.02, r'$S_A = \frac{\text{Area}(\gamma_A)}{4G_N} \quad \text{—  Space emerges from entanglement}$',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=10, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F0F0',
                      edgecolor=DARK_BLUE, linewidth=1.5))

    ax.grid(True, which='both', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'fig04_scale_of_universe')


# =============================================================================
# FIGURE 5: Energy Density Components
# =============================================================================
def figure_5_energy_density():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Time in years
    t_yr = np.logspace(-25, 100, 3000)
    t_s = t_yr * 365.25 * 86400

    # Critical density today
    rho_crit_0 = 9.2e-27  # kg/m^3

    # Radiation density: rho_r ~ a^-4 ~ t^-2
    rho_r = rho_crit_0 * 9e-5 * (t_yr / 1.38e10)**(-2)

    # Matter density: rho_m ~ a^-3 ~ t^-2
    rho_m = rho_crit_0 * 0.31 * (t_yr / 1.38e10)**(-1.5)

    # Dark energy density: constant (cosmological constant)
    rho_de = np.full_like(t_yr, rho_crit_0 * 0.69)

    # Plot
    ax.loglog(t_yr, rho_r / rho_crit_0, label='Radiation ($\\rho_r \\propto a^{-4}$)',
              color=RED, linewidth=2.5)
    ax.loglog(t_yr, rho_m / rho_crit_0, label='Matter ($\\rho_m \\propto a^{-3}$)',
              color=GREEN, linewidth=2.5)
    ax.loglog(t_yr, rho_de / rho_crit_0, label='Dark Energy ($\\rho_\\Lambda = \\text{const}$)',
              color=BLUE, linewidth=2.5)

    # Transition markers
    # Radiation-matter equality
    t_rm_eq = 1.38e10 * (9e-5 * 0.31**(-2/3))  # ~47,000 years
    ax.axvline(x=t_rm_eq, color=RED, linestyle='--', linewidth=1.5, alpha=0.6)
    ax.annotate('Radiation-Matter\nEquality', xy=(t_rm_eq, 1),
                xytext=(t_rm_eq * 10, 0.5),
                fontsize=9, color=RED, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                          edgecolor=RED, alpha=0.9))

    # Matter-dark energy equality
    t_md_eq = 1.38e10 * (0.31 / 0.69)**0.667  # ~9.8 billion years
    ax.axvline(x=t_md_eq, color=GREEN, linestyle='--', linewidth=1.5, alpha=0.6)
    ax.annotate('Matter-Dark Energy\nEquality', xy=(t_md_eq, 1),
                xytext=(t_md_eq * 10, 0.3),
                fontsize=9, color=GREEN, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                          edgecolor=GREEN, alpha=0.9))

    # Shade dominance regions
    ax.axvspan(1e-25, t_rm_eq, alpha=0.08, color=RED, label='')
    ax.axvspan(t_rm_eq, t_md_eq, alpha=0.08, color=GREEN, label='')
    ax.axvspan(t_md_eq, 1e101, alpha=0.08, color=BLUE, label='')

    # Add era labels
    ax.text(1e-10, 1e4, 'Radiation-\nDominated', fontsize=10, fontweight='bold',
            color=RED, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=RED, alpha=0.15))
    ax.text(1e9, 1e-1, 'Matter-\nDominated', fontsize=10, fontweight='bold',
            color=GREEN, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=GREEN, alpha=0.15))
    ax.text(1e17, 1, 'Dark Energy-\nDominated', fontsize=10, fontweight='bold',
            color=BLUE, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=BLUE, alpha=0.15))

    ax.set_xlabel('Time (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel(r'$\rho / \rho_{\text{crit},0}$ (Density relative to critical)',
                  fontsize=13, fontweight='bold')
    ax.set_title('Energy Density Components of the Universe\nRadiation → Matter → Dark Energy Dominance',
                 fontsize=15, fontweight='bold', pad=15)

    ax.text(0.5, 0.02, r'$\rho_r \propto a^{-4} \quad \rho_m \propto a^{-3} \quad \rho_\Lambda = \text{const}$' +
            r'  —  $\Lambda_\omega \sim H_0^2$',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=10, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F0F0',
                      edgecolor=DARK_BLUE, linewidth=1.5))

    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    ax.grid(True, which='both', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'fig05_energy_density')


# =============================================================================
# FIGURE 6: Entanglement Entropy vs Time
# =============================================================================
def figure_6_entanglement_entropy():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    t_yr = np.logspace(-25, 100, 3000)

    # Entanglement entropy S(t)
    # High at Big Bang (thermal state), decreases during inflation,
    # increases during structure formation, peaks at present, decreases during heat death
    S_ent = np.zeros_like(t_yr)

    for i, ti in enumerate(t_yr):
        if ti < 1e-43:  # Before Big Bang: S = 0
            S_ent[i] = 0
        elif ti < 1e-36:  # Planck: maximum entanglement
            S_ent[i] = 1.0 * (ti / 1e-43)**0.3
        elif ti < 1e-32:  # Inflation: entanglement decreases
            S_ent[i] = 1.0 - 0.8 * (ti - 1e-43) / (1e-32 - 1e-43)
        elif ti < 1e-12:  # Reheating: entanglement builds up
            S_ent[i] = 0.2 + 0.3 * (ti - 1e-32) / (1e-12 - 1e-32)
        elif ti < 3.8e5:  # Photon epoch: high entanglement
            S_ent[i] = 0.5 + 0.3 * np.log(ti / 1e-12) / np.log(3.8e5 / 1e-12)
        elif ti < 1e9:  # Recombination: sharp drop
            S_ent[i] = 0.8 - 0.4 * (ti - 3.8e5) / (1e9 - 3.8e5)
        elif ti < 1e12:  # Structure formation: gradual increase
            S_ent[i] = 0.4 + 0.25 * np.log(ti / 1e9) / np.log(1e12 / 1e9)
        elif ti < 1.38e10:  # Present: peak
            S_ent[i] = 0.65 + 0.15 * (ti - 1e12) / (1.38e10 - 1e12)
        elif ti < 1e17:  # Post-present: slow decrease
            S_ent[i] = 0.8 - 0.15 * (ti - 1.38e10) / (1e17 - 1.38e10)
        elif ti < 1e40:  # Black hole era
            S_ent[i] = 0.65 - 0.3 * (ti - 1e17) / (1e40 - 1e17)
        elif ti < 1e100:  # Heat death: approaches 0
            S_ent[i] = 0.35 * np.exp(-0.5 * (ti - 1e40) / 1e40)
        else:
            S_ent[i] = 0

    ax.semilogx(t_yr, S_ent, color=DARK_BLUE, linewidth=2.5, zorder=5)

    # Fill under curve
    ax.fill_between(t_yr, 0, S_ent, alpha=0.15, color=DARK_BLUE)

    # MCC interpretation annotations
    ax.annotate('High entanglement\n(thermal state)', xy=(1e-36, 0.95),
                xytext=(1e-30, 0.98), fontsize=9, color=BLUE,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=BLUE, alpha=0.1),
                fontweight='bold')

    ax.annotate('Inflation:\nentanglement drops', xy=(1e-34, 0.5),
                xytext=(1e-33, 0.7), fontsize=9, color=MAGENTA,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=MAGENTA, alpha=0.1),
                fontweight='bold')

    ax.annotate('Structure formation:\nentanglement rebuilds', xy=(1e10, 0.7),
                xytext=(1e11, 0.85), fontsize=9, color=GREEN,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=GREEN, alpha=0.1),
                fontweight='bold')

    ax.annotate('Heat death:\nentanglement vanishes', xy=(1e80, 0.05),
                xytext=(1e60, 0.2), fontsize=9, color=DARK_RED,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=DARK_RED, alpha=0.1),
                fontweight='bold')

    ax.set_xlabel('Time (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Normalized Entanglement Entropy S(t)', fontsize=13, fontweight='bold')
    ax.set_title('Entanglement Entropy Through Cosmic History\nHow Quantum Correlations Evolved from Big Bang to Heat Death',
                 fontsize=15, fontweight='bold', pad=15)
    ax.set_ylim(0, 1.05)

    ax.text(0.5, 0.02,
            'S_A = -Tr(rho_A log rho_A)  and  S_A = Area(gamma_A) / (4G_N)  --  Entropy as property of state omega on algebra M',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=9, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F0F0',
                      edgecolor=DARK_BLUE, linewidth=1.5))

    ax.grid(True, which='both', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'fig06_entanglement_entropy')


# =============================================================================
# FIGURE 7: Modular Flow Strength vs Time
# =============================================================================
def figure_7_modular_flow():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    t_yr = np.logspace(-25, 100, 3000)

    # Modular flow strength ||K_omega||
    # Weak/undefined before "start", emerges at Big Bang, strengthens during inflation,
    # stabilizes during thermal epoch, slows during heat death
    K = np.zeros_like(t_yr)

    for i, ti in enumerate(t_yr):
        if ti < 1e-43:  # Before Big Bang: no modular flow
            K[i] = 0
        elif ti < 1e-36:  # Emergence: rapid increase
            K[i] = 1e-36 * (ti / 1e-43)**2
        elif ti < 1e-32:  # Inflation: peak
            K[i] = 1e-36 + 1e-30 * (ti - 1e-36) / (1e-32 - 1e-36)
        elif ti < 1e-12:  # Reheating: stabilization
            K[i] = 1e-30 + 1e-31 * np.log(ti / 1e-32) / np.log(1e-12 / 1e-32)
        elif ti < 1e12:  # Structure formation: moderate
            K[i] = 1e-29 * (1 + 0.1 * np.log(ti / 1e-12) / np.log(1e12 / 1e-12))
        elif ti < 1.38e10:  # Present
            K[i] = 1e-29 * 1.1 * (ti / 1.38e10)**0.1
        elif ti < 1e40:  # Future: slow decrease
            K[i] = 1e-28 * (1e10 / ti)**0.5
        elif ti < 1e100:  # Heat death: near zero
            K[i] = 1e-38 * (1e40 / ti)**2
        else:
            K[i] = 0

    # Normalize for visualization
    K_norm = K / (K.max() + 1e-50)

    ax.semilogx(t_yr, K_norm, color=DARK_BLUE, linewidth=2.5, zorder=5)
    ax.fill_between(t_yr, 0, K_norm, alpha=0.15, color=DARK_BLUE)

    # Annotations
    ax.annotate('No modular flow\n(timeless)', xy=(1e-44, 0),
                xytext=(1e-40, 0.05), fontsize=9, color=LIGHT_GRAY,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_GRAY, alpha=0.1))

    ax.annotate('Modular flow\nemerges', xy=(1e-38, 0.15),
                xytext=(1e-35, 0.3), fontsize=9, color=BLUE, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor=BLUE, alpha=0.1))

    ax.annotate('Inflation:\npeak strength', xy=(1e-33, 0.95),
                xytext=(1e-31, 0.98), fontsize=9, color=MAGENTA, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=MAGENTA, alpha=0.1))

    ax.annotate('Thermal\nstabilization', xy=(1e-8, 0.3),
                xytext=(1e-5, 0.5), fontsize=9, color=GREEN, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=GREEN, alpha=0.1))

    ax.annotate('Heat death:\nflow vanishes', xy=(1e90, 0.01),
                xytext=(1e70, 0.1), fontsize=9, color=DARK_RED, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=DARK_RED, alpha=0.1))

    ax.set_xlabel('Time (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Normalized Modular Flow Strength $\\|K_\\omega\\|$',
                  fontsize=13, fontweight='bold')
    ax.set_title('Modular Flow Strength Through Cosmic History\nHow $\\sigma_t^\\omega$ Evolved from Timeless to Uniform',
                 fontsize=15, fontweight='bold', pad=15)
    ax.set_ylim(0, 1.05)

    ax.text(0.5, 0.02, r'$\sigma_t^\omega(M) = \Delta_\omega^{it} M \Delta_\omega^{-it} \quad \text{and} \quad K_\omega = -\log\Delta_\omega$',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=10, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F0F0',
                      edgecolor=DARK_BLUE, linewidth=1.5))

    ax.grid(True, which='both', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'fig07_modular_flow_strength')


# =============================================================================
# FIGURE 8: State Space S(M) Geometry
# =============================================================================
def figure_8_state_space():
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(1, 1, figure=fig)
    ax = fig.add_subplot(gs[0, 0], projection='3d')

    # Create a hyperbolic-like surface (negative curvature)
    u = np.linspace(-3, 3, 60)
    v = np.linspace(-3, 3, 60)
    U, V = np.meshgrid(u, v)

    # Saddle surface (negative curvature)
    X = U
    Y = V
    Z = 0.3 * (U**2 - V**2)  # Saddle shape

    # Plot surface
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6,
                           edgecolor='none', rstride=2, cstride=2)

    # Draw geodesics (physical processes)
    t_geo = np.linspace(0, 1, 100)

    # Geodesic 1: Big Bang → Present
    geo1_u = -2.5 + 5 * t_geo
    geo1_v = -2.5 + 5 * t_geo
    geo1_z = 0.3 * (geo1_u**2 - geo1_v**2)
    ax.plot(geo1_u, geo1_v, geo1_z, color=RED, linewidth=3, alpha=0.9, label='Cosmic evolution')

    # Geodesic 2: Structure formation
    geo2_u = -2.5 + 3 * t_geo
    geo2_v = 2.5 - 3 * t_geo
    geo2_z = 0.3 * (geo2_u**2 - geo2_v**2)
    ax.plot(geo2_u, geo2_v, geo2_z, color=GREEN, linewidth=2.5, alpha=0.8, label='Structure formation')

    # Geodesic 3: Heat death
    geo3_u = 2.5 - 2 * t_geo
    geo3_v = 0
    geo3_z = 0.3 * (geo3_u**2 - geo3_v**2)
    ax.plot(geo3_u, geo3_v, geo3_z, color=DARK_RED, linewidth=2, alpha=0.7, label='Heat death')

    # Mark key states
    ax.scatter([-2.5], [-2.5], [0.3*(6.25-6.25)], c=BLUE, s=200, marker='*',
               label='Big Bang\n(non-trivial $\\Delta_\\omega$)', zorder=10)
    ax.scatter([0], [0], [0], c=GREEN, s=150, marker='o',
               label='Present state', zorder=10)
    ax.scatter([2.5], [2.5], [0], c=DARK_RED, s=200, marker='h',
               label='Heat death\n(maximum entropy)', zorder=10)

    # Add diameter arrow (maximum entropy state)
    ax.quiver(0, 0, 0, 2.5, 2.5, 0, color=DARK_RED, arrow_length_ratio=0.1,
              linewidth=2, alpha=0.7)
    ax.text(1.5, 1.5, -0.5, 'Maximum\nEntropy', fontsize=9, color=DARK_RED,
            fontweight='bold')

    # Labels
    ax.set_xlabel(r'Coordinate $u$', fontsize=11, fontweight='bold')
    ax.set_ylabel(r'Coordinate $v$', fontsize=11, fontweight='bold')
    ax.set_zlabel(r'Entropy $S$', fontsize=11, fontweight='bold')
    ax.set_title('Modular State Manifold $\\mathcal{S}(\\mathcal{M})$\nNegative Curvature Geometry — Geodesics = Physical Processes',
                 fontsize=14, fontweight='bold', pad=15)

    # Add curvature annotation
    ax.text2D(0.05, 0.95, r'$K(X,Y) = -\frac{\|[X,K]\|^2}{\text{positive}} < 0$',
              transform=ax.transAxes, fontsize=10, fontweight='bold',
              bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                        edgecolor=BLUE, linewidth=2, alpha=0.9))

    ax.view_init(elev=25, azim=45)
    ax.legend(loc='lower left', fontsize=8, framealpha=0.9)

    save_fig(fig, 'fig08_state_space_geometry', tight=False)


# =============================================================================
# FIGURE 9: Emergent Spacetime from Entanglement
# =============================================================================
def figure_9_emergent_spacetime():
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Subplot 1: Tensor network
    ax1 = fig.add_subplot(gs[0, 0])
    # Draw a simple tensor network (MERA-like)
    levels = 4
    nodes_per_level = []
    for l in range(levels):
        nodes_per_level.append(2**(levels - l))

    for l in range(levels):
        n = nodes_per_level[l]
        y = 1 - l * 0.25
        x_positions = np.linspace(0.1, 0.9, n)
        for x in x_positions:
            ax1.plot(x, y, 'o', markersize=6, color=DARK_BLUE, zorder=3)
        # Connect to next level
        if l < levels - 1:
            n_next = nodes_per_level[l + 1]
            x_next = np.linspace(0.1, 0.9, n_next)
            for i, x in enumerate(x_positions):
                # Connect to nearest nodes below
                idx1 = min(i, n_next - 1)
                idx2 = min(i + 1, n_next - 1)
                ax1.plot([x, x_next[idx1]], [y, 1 - (l+1) * 0.25],
                         color=DARK_BLUE, linewidth=0.8, alpha=0.4)
                ax1.plot([x, x_next[idx2]], [y, 1 - (l+1) * 0.25],
                         color=DARK_BLUE, linewidth=0.8, alpha=0.4)

    ax1.set_xlim(0, 1)
    ax1.set_ylim(-0.05, 1.05)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('Tensor Network (MERA-like)\nEntanglement Pattern', fontsize=11, fontweight='bold')

    # Subplot 2: Discretized spacetime
    ax2 = fig.add_subplot(gs[0, 1])
    # Draw a 3D-like grid of triangles
    np.random.seed(42)
    nx, ny = 8, 6
    x_grid = np.linspace(0.1, 0.9, nx)
    y_grid = np.linspace(0.1, 0.85, ny)
    for i in range(nx - 1):
        for j in range(ny - 1):
            x1, y1 = x_grid[i], y_grid[j]
            x2, y2 = x_grid[i+1], y_grid[j]
            x3, y3 = x_grid[i], y_grid[j+1]
            x4, y4 = x_grid[i+1], y_grid[j+1]
            ax2.plot([x1, x2, x4, x3, x1], [y1, y1, y4, y4, y1],
                     color=DARK_BLUE, linewidth=0.5, alpha=0.5)
            ax2.plot([x1, x4], [y1, y4], color=GREEN, linewidth=0.8, alpha=0.5)
            ax2.plot([x2, x3], [y2, y3], color=GREEN, linewidth=0.8, alpha=0.5)

    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('Discretized Spacetime\nEmergent Geometry', fontsize=11, fontweight='bold')

    # Subplot 3: Ryu-Takayanagi formula visualization
    ax3 = fig.add_subplot(gs[1, :])

    # Draw a 2D space with a region A and minimal surface
    theta = np.linspace(0, 2*np.pi, 100)
    # Large circle (boundary)
    r_outer = 0.4
    x_outer = 0.5 + r_outer * np.cos(theta)
    y_outer = 0.5 + r_outer * np.sin(theta)
    ax3.plot(x_outer, y_outer, color=DARK_BLUE, linewidth=2, label='Boundary')

    # Region A (half circle)
    theta_A = np.linspace(-np.pi/2, np.pi/2, 50)
    r_A = 0.3
    x_A = 0.5 + r_A * np.cos(theta_A)
    y_A = 0.5 + r_A * np.sin(theta_A)
    ax3.fill(x_A, y_A, alpha=0.3, color=BLUE, label='Region A')

    # Minimal surface (geodesic)
    x_geo = np.linspace(0.2, 0.8, 100)
    y_geo = 0.5 + 0.1 * np.sin(np.pi * (x_geo - 0.2) / 0.6)
    ax3.plot(x_geo, y_geo, color=RED, linewidth=3, linestyle='--',
             label='Minimal surface $\\gamma_A$')

    # Area annotation
    ax3.text(0.5, 0.85, r'$S_A = \frac{\text{Area}(\gamma_A)}{4G_N}$',
             fontsize=14, ha='center', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                       edgecolor=RED, linewidth=2))

    ax3.text(0.5, 0.15, 'Ryu-Takayanagi Formula:\nEntanglement Entropy = Geometry',
             fontsize=10, ha='center', style='italic')

    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.set_aspect('equal')
    ax3.axis('off')
    ax3.set_title('Ryu-Takayanagi: Area = Entanglement Entropy',
                  fontsize=11, fontweight='bold')

    fig.suptitle('Emergent Spacetime from Entanglement\nTensor Network → Discretized Spacetime via Ryu-Takayanagi',
                 fontsize=15, fontweight='bold', y=0.98)

    save_fig(fig, 'fig09_emergent_spacetime', tight=False)


# =============================================================================
# FIGURE 10: Life's Emergence in Cosmic Context
# =============================================================================
def figure_10_life_emergence():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Time in years (log scale)
    t_yr = np.logspace(-25, 100, 3000)

    # Temperature curve (same as fig 2)
    T = np.zeros_like(t_yr)
    for i, ti in enumerate(t_yr):
        if ti < 1e-36:
            T[i] = 1e32 * np.exp(-5 * (ti - 1e-43) / 1e-36)
        elif ti < 1e-32:
            T[i] = 1e28 * (1e-36 / ti)**0.5
        elif ti < 1e-12:
            T[i] = 1e15 * np.exp(-3 * (ti - 1e-32) / 1e-12)
        elif ti < 1e-4:
            T[i] = 1e12 * (1e-6 / ti)**0.5
        elif ti < 1:
            T[i] = 1e9 * (1 / ti)**0.5
        elif ti < 1e6:
            T[i] = 1e8 * (10 / ti)**0.5
        elif ti < 3.8e5 * 365 * 86400:
            T[i] = 3000 * (3.8e5 * 365 * 86400 / ti)**0.5
        elif ti < 1e17:
            T[i] = 2.7 * (3.8e5 * 365 * 86400 / ti)**0.5
        else:
            T[i] = 2.7 * np.exp(-0.1 * (ti / 1e17))

    ax.loglog(t_yr, T, color=DARK_BLUE, linewidth=2.5, zorder=5)

    # Life habitable zone
    T_life_min = 200   # Kelvin (minimum for liquid water)
    T_life_max = 600   # Kelvin (maximum for complex molecules)

    # Find time range where temperature is in habitable zone for Earth-like conditions
    # Earth forms ~4.5 Gyr ago, was habitable for ~3-4 billion years
    t_start_life = 1e9 * 365.25 * 86400  # ~1 billion years (first simple life)
    t_end_life = 1e11 * 365.25 * 86400   # ~100 billion years (last complex life, theoretical)

    # Goldilocks zone shading
    ax.axvspan(t_start_life, t_end_life, alpha=0.15, color=TEAL,
               label='Habitable Window')

    # Draw the habitable temperature band
    ax.axhspan(T_life_min, T_life_max, alpha=0.1, color=TEAL,
               label='Life Temperature Range')

    # Earth's habitable period
    t_earth_formation = 4.5e9 * 365.25 * 86400
    t_life_start = 3.8e9 * 365.25 * 86400
    t_life_end = 1e10 * 365.25 * 86400  # ~10 billion years from now (theoretical)

    ax.axvspan(t_life_start, t_life_end, alpha=0.2, color=GREEN,
               label='Life on Earth')

    # Mark key events
    events = [
        (t_earth_formation, 'Earth Forms\n4.5 Gyr ago', GREEN),
        (t_life_start, 'First Life\n3.8 Gyr ago', TEAL),
        (1.38e10 * 365.25 * 86400, 'Present\nDay', DARK_BLUE),
        (t_life_end, 'End of\nComplex Life', DARK_RED),
    ]

    for te, el, ec in events:
        ax.plot(te, T[np.argmin(np.abs(t_yr - te))], 'o', markersize=10,
                color=ec, markeredgecolor='black', markeredgewidth=1, zorder=6)
        ax.annotate(el, xy=(te, T[np.argmin(np.abs(t_yr - te))]),
                    xytext=(te * 3, T[np.argmin(np.abs(t_yr - te))] * 2),
                    fontsize=9, color=ec, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=ec, lw=1.5),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor=ec, alpha=0.9))

    ax.set_xlabel('Time (seconds)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Temperature (Kelvin)', fontsize=13, fontweight='bold')
    ax.set_title('Life\'s Emergence in Cosmic Context\nThe Goldilocks Window — When Conditions Were Right for Life',
                 fontsize=15, fontweight='bold', pad=15)

    ax.text(0.5, 0.02, r'The habitable window: $200\text{ K} < T < 600\text{ K}$' +
            r'  —  Life as a low-entropy correlation pattern in $\mathcal{S}(\mathcal{M})$',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=10, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F0F0',
                      edgecolor=TEAL, linewidth=1.5))

    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax.grid(True, which='both', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    save_fig(fig, 'fig10_life_emergence')


# =============================================================================
# FIGURE 11: Consciousness as Modular Self-Reference
# =============================================================================
def figure_11_consciousness():
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))

    # Draw the self-referential modular flow diagram
    # Central loop: state -> modular operator -> modular flow -> state update

    # Create circular layout
    center = (0.5, 0.5)
    radius = 0.3

    states = [
        ('State\n$\\omega$', 0),
        ('Modular\nOperator\n$\\Delta_\\omega$', np.pi/2),
        ('Modular\nFlow\n$\\sigma_t^\\omega$', np.pi),
        ("State\nUpdate\n$\\omega \\to \\omega'$", 3*np.pi/2),
    ]

    positions = {}
    for name, angle in states:
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        positions[name] = (x, y)

    # Draw nodes
    node_colors = [BLUE, PURPLE, GREEN, ORANGE]
    for idx, (name, angle) in enumerate(states):
        pos = positions[name]
        color = node_colors[idx]
        circle = Circle(pos, 0.06, facecolor=color, edgecolor='black',
                        linewidth=2, alpha=0.8, zorder=5)
        ax.add_patch(circle)
        ax.text(pos[0], pos[1], name, ha='center', va='center',
                fontsize=8, fontweight='bold', color='white', zorder=6)

    # Draw arrows between nodes (feedback loop)
    arrow_props = dict(arrowstyle='->', lw=2.5, color=DARK_BLUE, alpha=0.7)
    connections = [
        (positions["State\n$\\omega$"], positions['Modular\nOperator\n$\\Delta_\\omega$']),
        (positions['Modular\nOperator\n$\\Delta_\\omega$'], positions['Modular\nFlow\n$\\sigma_t^\\omega$']),
        (positions['Modular\nFlow\n$\\sigma_t^\\omega$'], positions["State\nUpdate\n$\\omega \\to \\omega'$"]),
        (positions["State\nUpdate\n$\\omega \\to \\omega'$"], positions["State\n$\\omega$"]),
    ]

    for start, end in connections:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = np.sqrt(dx**2 + dy**2)
        start_adj = (start[0] + 0.06*dx/length, start[1] + 0.06*dy/length)
        end_adj = (end[0] - 0.06*dx/length, end[1] - 0.06*dy/length)
        ax.annotate('', xy=end_adj, xytext=start_adj, arrowprops=arrow_props)

    # Add formula in center
    ax.text(center[0], center[1],
            r'$\sigma_t^\omega \approx \sigma_t^\omega$',
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=DARK_BLUE,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                      edgecolor=DARK_BLUE, linewidth=2, alpha=0.9))

    # Add brain/neural processing annotation
    ax.annotate('Neural Processing\n(Microtubules as MCMs)',
                xy=(0.85, 0.85), xytext=(0.75, 0.75),
                fontsize=9, color=TEAL, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=TEAL, lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor=TEAL, alpha=0.15))

    # Add subjective time annotation
    ax.annotate('Subjective Time\n$\\tau = \\beta t$',
                xy=(0.15, 0.85), xytext=(0.25, 0.75),
                fontsize=9, color=MAGENTA, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=MAGENTA, lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor=MAGENTA, alpha=0.15))

    # Add self-reference annotation
    ax.annotate('Self-Reference:\nObserver observes\nown modular flow',
                xy=(0.5, 0.92), xytext=(0.5, 0.97),
                fontsize=10, color=DARK_RED, fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=DARK_RED, alpha=0.15))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Consciousness as Self-Referential Modular Flow\nA Subsystem Observing Its Own Modular Automorphism Group',
                 fontsize=15, fontweight='bold', pad=15)

    # Add MCC formula at bottom
    ax.text(0.5, 0.02, r'$\sigma_t^\omega(\text{observer}) \approx \sigma_t^\omega(\text{observed})$' +
            '  --  Consciousness = self-referential modular flow',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=10, style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0F0F0',
                      edgecolor=DARK_BLUE, linewidth=1.5))

    save_fig(fig, 'fig11_consciousness')


# =============================================================================
# FIGURE 12: Heat Death Visualization
# =============================================================================
def figure_12_heat_death():
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Subplot 1: Sparse correlations
    ax1 = fig.add_subplot(gs[0, 0])
    np.random.seed(123)
    n_points = 30
    x_corr = np.random.uniform(0.1, 0.9, n_points)
    y_corr = np.random.uniform(0.1, 0.9, n_points)
    sizes = np.random.uniform(20, 80, n_points)
    ax1.scatter(x_corr, y_corr, s=sizes, c=BLUE, alpha=0.3, edgecolors='gray', linewidth=0.5)

    # Draw very few correlations
    for i in range(min(5, n_points-1)):
        ax1.plot([x_corr[i], x_corr[i+1]], [y_corr[i], y_corr[i+1]],
                 color=BLUE, linewidth=0.5, alpha=0.1)

    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('Sparse Correlations\n(Heat Death)', fontsize=11, fontweight='bold')

    # Subplot 2: Uniform modular flow
    ax2 = fig.add_subplot(gs[0, 1])
    # Draw uniform grid with no structure
    x_grid = np.linspace(0.1, 0.9, 10)
    y_grid = np.linspace(0.1, 0.9, 10)
    for x in x_grid:
        for y in y_grid:
            ax2.plot(x, y, 'o', markersize=4, color=LIGHT_GRAY)
    # No connections between points
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('Uniform Modular Flow\nNo Structure Remains', fontsize=11, fontweight='bold')

    # Subplot 3: Entropy saturation
    ax3 = fig.add_subplot(gs[1, 0])
    t_future = np.logspace(40, 100, 500)
    S_final = 2e45 * (1 - np.exp(-(t_future - 1e40) / 1e35))
    ax3.semilogx(t_future, S_final / 2e45, color=DARK_RED, linewidth=2.5)
    ax3.axhline(y=1.0, color=GREEN, linestyle='--', linewidth=1.5, alpha=0.5, label='Maximum Entropy')
    ax3.set_xlabel('Time (years)', fontsize=10, fontweight='bold')
    ax3.set_ylabel('S / S_max', fontsize=10, fontweight='bold')
    ax3.set_title('Entropy Saturation\n(dS/dt → 0)', fontsize=11, fontweight='bold')
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    # Subplot 4: Final state description
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)

    # Draw final state description
    final_text = [
        ('FINAL STATE: HEAT DEATH', 0.9, 'center', 12, DARK_RED, 'bold'),
        ('', 0.85, 'center', 6, BLACK, 'normal'),
        (r'$\Delta_\omega \approx I$', 0.80, 'center', 11, DARK_BLUE, 'bold'),
        (r'$\sigma_t^\omega \approx \text{id}$', 0.73, 'center', 11, DARK_BLUE, 'bold'),
        (r'$K_\omega \approx 0$', 0.66, 'center', 11, DARK_BLUE, 'bold'),
        ('', 0.60, 'center', 6, BLACK, 'normal'),
        ('No structure remains', 0.55, 'center', 10, BLACK, 'normal'),
        ('No correlations', 0.50, 'center', 10, BLACK, 'normal'),
        ('No energy gradients', 0.45, 'center', 10, BLACK, 'normal'),
        ('No change possible', 0.40, 'center', 10, BLACK, 'normal'),
        ('Time exists but nothing happens', 0.33, 'center', 10, DARK_RED, 'normal'),
        ('', 0.27, 'center', 6, BLACK, 'normal'),
        (r'$\frac{dS}{dt} = 0$', 0.22, 'center', 12, DARK_RED, 'bold'),
    ]

    for text, y, ha, fs, fc, fw in final_text:
        ax4.text(0.5, y, text, ha=ha, va='center', fontsize=fs, color=fc,
                 fontweight=fw)

    fig.suptitle('The End of the Universe: Heat Death\nSparse Correlations, Uniform Modular Flow, No Structure',
                 fontsize=15, fontweight='bold', y=0.98)

    save_fig(fig, 'fig12_heat_death', tight=False)


# =============================================================================
# FIGURE 13: Alternative Endings Comparison
# =============================================================================
def figure_13_alternative_endings():
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    scenarios = [
        ('Big Freeze\n(Heat Death)', DARK_BLUE, 'Most likely'),
        ('Big Rip', RED, 'w < -1'),
        ('Big Crunch', PURPLE, 'High density'),
        ('Vacuum Decay', MAGENTA, 'False vacuum'),
        ('Big Bounce', GREEN, 'Quantum gravity'),
        ('Cyclic Universe', TEAL, 'Oscillating'),
    ]

    for idx, (title, color, desc) in enumerate(scenarios):
        ax = axes[idx // 3, idx % 3]

        # Time axis
        t = np.linspace(0, 10, 500)

        # Each scenario: entropy, scale factor, structure
        if title.startswith('Big Freeze'):
            # Entropy increases to max, scale factor expands forever, structure fades
            entropy = 1 - np.exp(-0.5 * t)
            scale = np.exp(0.3 * t)
            structure = np.exp(-0.8 * t)
        elif title.startswith('Big Rip'):
            # Everything tears apart
            entropy = 1 - np.exp(-2 * t)
            scale = np.exp(2 * t)
            structure = np.exp(-5 * t)
        elif title.startswith('Big Crunch'):
            # Reversal: contraction
            entropy = 1 - np.exp(-0.5 * t) * (1 + 0.5 * (t - 5)**2 / 25)
            scale = np.cos(0.3 * (t - 5))
            structure = np.exp(-0.8 * t) * (1 + (t-5)**2 / 25)
        elif title.startswith('Vacuum Decay'):
            # Sudden transition
            entropy = np.where(t < 7, 1 - np.exp(-0.5*t), 1.2)
            scale = np.where(t < 7, np.exp(0.3*t), 0.5)
            structure = np.where(t < 7, np.exp(-0.8*t), 0.1)
        elif title.startswith('Big Bounce'):
            # Bounce at t=5
            entropy = 1 - np.exp(-0.5 * np.abs(t - 5))
            scale = np.abs(np.cos(0.3 * (t - 5))) + 0.1
            structure = np.exp(-0.5 * np.abs(t - 5))
        else:  # Cyclic
            entropy = 0.5 + 0.5 * np.sin(0.5 * t)
            scale = 1 + 0.5 * np.sin(0.5 * t)
            structure = 0.5 + 0.5 * np.cos(0.5 * t)

        if isinstance(entropy, np.ndarray) and entropy.ndim == 0:
            entropy = np.full_like(t, entropy)

        # Plot entropy
        ax.plot(t, entropy, color=color, linewidth=2.5, label='Entropy', alpha=0.8)
        ax.plot(t, scale, color=color, linewidth=1.5, linestyle='--', label='Scale Factor', alpha=0.6)
        ax.plot(t, structure, color=color, linewidth=1.5, linestyle=':', label='Structure', alpha=0.6)

        # Title and description
        ax.set_title(f'{title}\n({desc})', fontsize=11, fontweight='bold', color=color)

        ax.set_xlabel('Time (normalized)', fontsize=9)
        ax.set_ylabel('Normalized', fontsize=9)
        ax.legend(fontsize=7, loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 2)

    # Remove any empty axes
    if len(scenarios) < 6:
        for idx in range(len(scenarios), 6):
            ax = axes[idx // 3, idx % 3]
            ax.axis('off')

    fig.suptitle('Alternative Endings of the Universe\nComparing Five Scenarios for the Fate of Spacetime, Entropy, and Structure',
                 fontsize=15, fontweight='bold', y=0.98)

    save_fig(fig, 'fig13_alternative_endings', tight=False)


# =============================================================================
# FIGURE 14: Energy-Information-Geometry Triangle
# =============================================================================
def figure_14_eig_triangle():
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))

    # Equilateral triangle vertices
    # Center at (0.5, 0.5), radius 0.35
    center = (0.5, 0.5)
    radius = 0.35

    # Vertices: Energy (top), Information (bottom right), Geometry (bottom left)
    angles = [np.pi/2, -np.pi/6, -5*np.pi/6]  # top, bottom-right, bottom-left
    vertices = [(center[0] + radius * np.cos(a), center[1] + radius * np.sin(a))
                for a in angles]

    vertex_labels = ['Energy', 'Information', 'Geometry']
    vertex_colors = [RED, PURPLE, DARK_BLUE]

    # Draw triangle
    triangle = Polygon(vertices, closed=True, fill=False,
                       edgecolor=BLACK, linewidth=2.5)
    ax.add_patch(triangle)

    # Draw the triangle fill with gradient-like effect
    for i, (v1, v2, v3) in enumerate([(vertices[0], vertices[1], vertices[2]),
                                        (vertices[1], vertices[2], vertices[0]),
                                        (vertices[2], vertices[0], vertices[1])]):
        tri = Polygon([v1, v2, v3], closed=True,
                      facecolor=vertex_colors[i], alpha=0.08)
        ax.add_patch(tri)

    # Mark vertices
    for v, label, color in zip(vertices, vertex_labels, vertex_colors):
        ax.plot(v[0], v[1], 'o', markersize=15, color=color,
                markeredgecolor='black', markeredgewidth=2, zorder=5)
        ax.text(v[0], v[1], label, ha='center', va='center',
                fontsize=13, fontweight='bold', color='white', zorder=6)

    # Draw positions through cosmic history
    epochs_triangle = [
        # (position, label, description, color)
        (vertices[2], 'Planck Epoch', 'Geometry dominant\n$\\mathcal{D}_\\omega$ unified', BLUE),
        (np.array(vertices[2]) * 0.7 + np.array([0.15, 0.15]), 'Inflation', 'Geometry + Energy', PURPLE),
        (np.array([0.4, 0.55]), 'Particle Epoch', 'Energy dominant\n$K_\\omega = \\beta H$', RED),
        (np.array([0.55, 0.45]), 'Present Day', 'Balanced\nall three equal', GREEN),
        (np.array([0.6, 0.35]), 'Future', 'Information dominant\nsparse correlations', TEAL),
        (np.array(vertices[1]) * 0.8 + np.array([0.05, 0.05]), 'Heat Death', 'Information only\nS -> S_max', DARK_RED),
    ]

    for pos, label, desc, color in epochs_triangle:
        ax.plot(pos[0], pos[1], 'o', markersize=12, color=color,
                markeredgecolor='black', markeredgewidth=1.5, zorder=5)
        ax.annotate(label, xy=pos, xytext=(pos[0] + 0.08, pos[1] + 0.05),
                    fontsize=9, color=color, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor=color, alpha=0.9))

    # Draw trajectory line through triangle
    trajectory = [np.array(vertices[2]), np.array(vertices[2]) * 0.7 + np.array([0.15, 0.15]),
                  np.array([0.4, 0.55]), np.array([0.55, 0.45]),
                  np.array([0.6, 0.35]), np.array(vertices[1]) * 0.8 + np.array([0.05, 0.05])]
    traj_x = [p[0] for p in trajectory]
    traj_y = [p[1] for p in trajectory]

    # Create color gradient along trajectory
    for i in range(len(traj_x) - 1):
        ax.plot(traj_x[i:i+2], traj_y[i:i+2], color=color,
                linewidth=3, alpha=0.6, zorder=3)

    ax.plot(traj_x, traj_y, color=DARK_BLUE, linewidth=2, alpha=0.4,
            linestyle='--', zorder=2, label='Cosmic evolution')

    # Add time arrow
    ax.annotate('', xy=(trajectory[-1][0] + 0.05, trajectory[-1][1]),
                xytext=(trajectory[0][0], trajectory[0][1]),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=2, alpha=0.5))
    ax.text(0.5, 0.08, 'Time →', fontsize=12, fontweight='bold', ha='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Energy-Information-Geometry Triangle\nThe Balance of Cosmic Components Through History',
                 fontsize=15, fontweight='bold', pad=15)

    # Add MCC formula
    ax.text(0.5, 0.98, r'$\mathcal{D}_\omega = I^{-1}\log\Delta_\omega$  —  Unifies Geometry, Energy, and Information',
            transform=ax.transAxes, ha='center', va='top',
            fontsize=11, style='italic', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#F0F0F0',
                      edgecolor=DARK_BLUE, linewidth=2))

    save_fig(fig, 'fig14_eig_triangle')


# =============================================================================
# FIGURE 15: Modular Dirac Operator Spectrum Through Cosmic History
# =============================================================================
def figure_15_dirac_spectrum():
    fig, axes = plt.subplots(1, 3, figsize=(15, 7))

    # Three panels: Early universe, Present, Future
    panels = [
        ('Early Universe\n(Type III$_1$)', 'Broad continuous spectrum', BLUE),
        ('Present Day\n(Structured)', 'Structured with gaps', GREEN),
        ('Heat Death\n(Nearly trivial)', 'Narrow sparse spectrum', DARK_RED),
    ]

    for idx, (title, desc, color) in enumerate(panels):
        ax = axes[idx]

        # Generate spectrum
        n_levels = 50 if idx == 0 else (20 if idx == 1 else 5)

        if idx == 0:  # Broad continuous
            # Many eigenvalues spread across wide range
            eigenvalues = np.random.uniform(-5, 5, n_levels)
            eigenvalues = np.sort(eigenvalues)
            widths = np.random.uniform(0.3, 0.8, n_levels)
        elif idx == 1:  # Structured with gaps
            # Clusters of eigenvalues with gaps
            groups = [np.random.uniform(-4, -2, 8),
                      np.random.uniform(-1, 1, 6),
                      np.random.uniform(2, 4, 6)]
            eigenvalues = np.concatenate(groups)
            widths = np.random.uniform(0.15, 0.4, n_levels)
        else:  # Narrow sparse
            # Few eigenvalues, narrow spread
            eigenvalues = np.random.uniform(-0.5, 0.5, n_levels)
            widths = np.random.uniform(0.05, 0.15, n_levels)

        # Plot spectrum as vertical bars
        for ev, w in zip(eigenvalues, widths):
            ax.plot([ev, ev], [-w, w], color=color, linewidth=2, alpha=0.7)
            ax.plot(ev, 0, 'o', markersize=6, color=color,
                    markeredgecolor='black', markeredgewidth=1)

        # Add zero line
        ax.axhline(y=0, color=BLACK, linewidth=1, alpha=0.3)
        ax.axvline(x=0, color=BLACK, linewidth=1, alpha=0.3)

        ax.set_xlabel(r'Eigenvalue of D_omega', fontsize=10, fontweight='bold')
        ax.set_ylabel('Density', fontsize=10, fontweight='bold')
        ax.set_title(f'{title}\n{desc}', fontsize=11, fontweight='bold', color=color)

        ax.set_xlim(-6, 6)
        ax.set_ylim(-1, 1)
        ax.grid(True, alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add spectral action annotation
        if idx == 0:
            ax.text(0, -0.85, 'P(omega_1) proportional to exp(-S_modular[omega_1])',
                    ha='center', fontsize=9, style='italic',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor=color, alpha=0.9))

    fig.suptitle('Modular Dirac Operator Spectrum Through Cosmic History\nD_omega = I^-1 log(Delta_omega) — From Broad Continuous to Narrow Sparse',
                 fontsize=14, fontweight='bold', y=0.98)

    save_fig(fig, 'fig15_dirac_spectrum', tight=False)


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    print("=" * 70)
    print("Generating 15 Cosmic Timeline Figures")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 70)

    figures = [
        ("Figure 1: Timeline of the Universe", figure_1_timeline),
        ("Figure 2: Temperature vs Time", figure_2_temperature),
        ("Figure 3: Entropy vs Time", figure_3_entropy),
        ("Figure 4: Scale of Observable Universe", figure_4_scale),
        ("Figure 5: Energy Density Components", figure_5_energy_density),
        ("Figure 6: Entanglement Entropy", figure_6_entanglement_entropy),
        ("Figure 7: Modular Flow Strength", figure_7_modular_flow),
        ("Figure 8: State Space Geometry", figure_8_state_space),
        ("Figure 9: Emergent Spacetime", figure_9_emergent_spacetime),
        ("Figure 10: Life's Emergence", figure_10_life_emergence),
        ("Figure 11: Consciousness Diagram", figure_11_consciousness),
        ("Figure 12: Heat Death", figure_12_heat_death),
        ("Figure 13: Alternative Endings", figure_13_alternative_endings),
        ("Figure 14: EIG Triangle", figure_14_eig_triangle),
        ("Figure 15: Dirac Spectrum", figure_15_dirac_spectrum),
    ]

    for name, func in figures:
        print(f"\n{name}...")
        try:
            func()
            print(f"  ✓ {name} completed")
        except Exception as e:
            print(f"  ✗ {name} failed: {e}")

    print("\n" + "=" * 70)
    print("All figures generated!")
    print("=" * 70)

    # List generated files
    files = sorted(os.listdir(OUTPUT_DIR))
    png_files = [f for f in files if f.endswith('.png')]
    pdf_files = [f for f in files if f.endswith('.pdf')]
    print(f"\nGenerated: {len(png_files)} PNG files, {len(pdf_files)} PDF files")
    print("Files:")
    for f in png_files:
        path = os.path.join(OUTPUT_DIR, f)
        size = os.path.getsize(path)
        print(f"  {f} ({size // 1024} KB)")


if __name__ == '__main__':
    main()
