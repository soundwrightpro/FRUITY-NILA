"""
Fruity NILA Script

This module provides a collection of components and utilities for the Fruity NILA script.

Components:
- NILA_core: Core class for Fruity NILA script, handling various events and interactions.
- NILA_detect_device: Module for detecting and setting up devices for Fruity NILA.
- NILA_transform: Module for transforming data or handling transformations in Fruity NILA.
- NILA_version_check: Module for checking the version compatibility of Fruity NILA.
- config: Configuration module for Fruity NILA.
- constants: Module containing constants used throughout Fruity NILA.

Usage:
The '__all__' list is used to specify the components that are intended to be publicly
accessible when someone imports this module using the '*' wildcard import statement.

Example:
    from script import *

    # Now, you can access the components listed in '__all__' directly.

    # Accessing the NILA_core class:
    my_core_instance = NILA_core.Core()

    # Accessing the constants module:
    my_constant_value = constants.some_constant_value
"""

__all__ = [
    "config",
    "constants",
    "NILA_core",
    "NILA_detect_device",
    "NILA_transform",
    "NILA_version_check",
]