"""
Fruity NILA Visuals package.

This module provides all visual feedback components for Fruity NILA, including 
LED and display rendering for Native Instruments controllers.

Components:
- NILA_LED: LED color and flashing logic.
- NILA_Display: text display and rendering functions.

Usage Example:
    from nila.NILA_visuals import NILA_LED, NILA_Display

    # Update LEDs:
    NILA_LED.update_leds(track_index)

    # Display text:
    NILA_Display.update_text("Hello from NILA")
"""
from . import NILA_LED
from . import NILA_Display

__all__ = [
    "NILA_LED",
    "NILA_Display",
]