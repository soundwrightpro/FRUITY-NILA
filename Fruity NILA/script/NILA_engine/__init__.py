"""
Fruity NILA Script package.

This module collects all Fruity NILA components and utilities for easy access.

Components:
- config: Configuration settings for Fruity NILA.
- constants: Global constants.
- NILA_core: Core event handler and interface.
- NILA_detect_device: Device detection utilities.
- NILA_transform: Data transformation utilities.
- NILA_version_check: Version compatibility checking.

Usage Example:
    from script.NILA_engine import constants, NILA_core

    # Access a constant:
    x = constants.VERSION_NUMBER

    # Instantiate the core handler:
    my_core = NILA_core.Core()
"""

__all__ = [
    "config",
    "constants",
    "NILA_core",
    "NILA_detect_device",
    "NILA_transform",
    "NILA_version_check",
]

# Optional: import all for direct access (optional and not strictly required)
# from . import config, constants, NILA_core, NILA_detect_device, NILA_transform, NILA_version_check
