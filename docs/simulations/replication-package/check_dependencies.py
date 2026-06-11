#!/usr/bin/env python3
"""
Check Dependencies for MCC Replication Package

Verifies that all required Python packages are installed with correct versions.

Usage:
    python check_dependencies.py
"""

import sys
import importlib

REQUIRED_PACKAGES = {
    'numpy': '1.24',
    'scipy': '1.10',
    'matplotlib': '3.7',
    'sympy': '1.12',
}

def check_package(name, min_version):
    """Check if a package is installed with sufficient version."""
    try:
        mod = importlib.import_module(name)
        version = getattr(mod, '__version__', 'unknown')
        
        # Parse version
        try:
            installed = tuple(int(x) for x in version.split('.')[:2])
            required = tuple(int(x) for x in min_version.split('.')[:2])
            meets = installed >= required
        except (ValueError, AttributeError):
            meets = True  # Can't parse version, assume OK
        
        return True, version, meets
    
    except ImportError:
        return False, 'NOT INSTALLED', False


def main():
    """Check all required dependencies."""
    print("=" * 60)
    print("MCC Replication Package — Dependency Check")
    print("=" * 60)
    
    all_ok = True
    
    for name, min_version in REQUIRED_PACKAGES.items():
        installed, version, meets = check_package(name, min_version)
        
        if installed and meets:
            status = "✓"
        elif installed and not meets:
            status = "⚠"
            all_ok = False
        else:
            status = "✗"
            all_ok = False
        
        print(f"  [{status}] {name} {version} (required >= {min_version})")
    
    print(f"\n{'=' * 60}")
    
    if all_ok:
        print("✓ ALL DEPENDENCIES OK")
        print(f"\nYou can now run the simulations:")
        print(f"  python run_all_simulations.py")
    else:
        print("✗ SOME DEPENDENCIES MISSING OR OUT OF DATE")
        print(f"\nInstall/update with:")
        print(f"  pip install {' '.join(REQUIRED_PACKAGES.keys())}")
    
    print(f"{'=' * 60}")
    
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
