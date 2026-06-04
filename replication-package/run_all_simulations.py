#!/usr/bin/env python3
"""
Run All MCC Simulations

Runs all 5 simulations in sequence, saves output figures, and produces
a combined log of results.

Usage:
    python run_all_simulations.py

Expected output files in output/:
    - spectrum_plot.png
    - curvature_plot.png
    - decoherence_plot.png
    - R_matrix.png
    - yang_baxter.png
    - braiding_phase.png
    - q_limit.png
    - braiding_plot.png
    - fusion_tree.png
    - D_omega_comparison.png
    - zeta_plot.png
    - zeta_grid.png
    - simulation_log.txt
"""

import sys
import os
import time
import traceback
from datetime import datetime

# Add the simulation directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'output')
os.makedirs(output_dir, exist_ok=True)

log_lines = []

def log(msg):
    """Log a message to both stdout and the log file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line)
    log_lines.append(line)

def run_simulation(sim_name, sim_module):
    """
    Run a single simulation and capture results.
    
    Returns:
        success: bool
        results: dict or None
    """
    log(f"\n{'=' * 70}")
    log(f"RUNNING: {sim_name}")
    log(f"{'=' * 70}")
    
    start_time = time.time()
    
    try:
        # Import and run
        results = sim_module.main()
        elapsed = time.time() - start_time
        
        log(f"✓ {sim_name} completed successfully in {elapsed:.2f}s")
        log(f"  Results: {results}")
        
        return True, results, elapsed
    
    except Exception as e:
        elapsed = time.time() - start_time
        log(f"✗ {sim_name} FAILED after {elapsed:.2f}s")
        log(f"  Error: {e}")
        log(f"  Traceback:\n{traceback.format_exc()}")
        
        return False, None, elapsed


def main():
    """Run all 5 simulations in sequence."""
    log("=" * 70)
    log("MCC Replication Package — Run All Simulations")
    log("=" * 70)
    log(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Working directory: {script_dir}")
    log(f"Output directory: {output_dir}")
    
    total_start = time.time()
    
    # Import simulations
    try:
        import simulation_1_spectrum as sim1
        import simulation_2_curvature as sim2
        import simulation_3_qdeformed as sim3
        import simulation_4_anyons as sim4
        import simulation_5_zeta as sim5
        log("✓ All simulation modules imported successfully")
    except ImportError as e:
        log(f"✗ Import error: {e}")
        log("  Make sure all simulation files are in the same directory.")
        log("  Run `pip install numpy scipy matplotlib sympy` if needed.")
        sys.exit(1)
    
    # Run simulations
    simulations = [
        ("Simulation 1: Modular Dirac Operator Spectrum", sim1),
        ("Simulation 2: Fisher-Rao Metric and Curvature", sim2),
        ("Simulation 3: q-Deformed Clifford Algebra", sim3),
        ("Simulation 4: 2+1D Anyon Modules", sim4),
        ("Simulation 5: Modular Zeta Function", sim5),
    ]
    
    results = {}
    successes = []
    failures = []
    
    for sim_name, sim_module in simulations:
        success, result, elapsed = run_simulation(sim_name, sim_module)
        results[sim_name] = {'success': success, 'result': result, 'elapsed': elapsed}
        
        if success:
            successes.append(sim_name)
        else:
            failures.append(sim_name)
    
    # Summary
    total_elapsed = time.time() - total_start
    
    log(f"\n{'=' * 70}")
    log("FINAL SUMMARY")
    log(f"{'=' * 70}")
    log(f"Total time: {total_elapsed:.2f}s")
    log(f"Simulations run: {len(successes) + len(failures)}/{len(simulations)}")
    log(f"Successful: {len(successes)}")
    log(f"Failed: {len(failures)}")
    
    for sim_name in successes:
        log(f"  ✓ {sim_name}")
    
    for sim_name in failures:
        log(f"  ✗ {sim_name}")
    
    if len(failures) == 0:
        log(f"\n✓ ALL SIMULATIONS PASSED")
    else:
        log(f"\n✗ {len(failures)} SIMULATION(S) FAILED")
        log(f"  Check the output above for error details.")
    
    # Save log file
    log_file = os.path.join(output_dir, 'simulation_log.txt')
    with open(log_file, 'w') as f:
        f.write('\n'.join(log_lines))
    log(f"Log saved to: {log_file}")
    
    # Check output files
    log(f"\n{'=' * 70}")
    log("OUTPUT FILES")
    log(f"{'=' * 70}")
    
    expected_files = [
        'spectrum_plot.png',
        'curvature_plot.png',
        'decoherence_plot.png',
        'R_matrix.png',
        'yang_baxter.png',
        'braiding_phase.png',
        'q_limit.png',
        'braiding_plot.png',
        'fusion_tree.png',
        'D_omega_comparison.png',
        'zeta_plot.png',
        'zeta_grid.png',
    ]
    
    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            log(f"  ✓ {fname} ({size:,} bytes)")
        else:
            log(f"  ✗ {fname} (NOT FOUND)")
    
    log(f"\n{'=' * 70}")
    log(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'=' * 70}")
    
    return 0 if len(failures) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
