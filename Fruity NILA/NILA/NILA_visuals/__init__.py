"""
Fruity NILA Visuals package.

This module provides all visual feedback components for Fruity NILA, including 
LED and OLED display rendering for Native Instruments controllers.

Components:
- NILA_LED: LED color and flashing logic.
- NILA_OLED: OLED text display and rendering functions.

Usage Example:
    from nila.NILA_visuals import NILA_LED, NILA_OLED

    # Update LEDs:
    NILA_LED.update_leds(track_index)

    # Display text on OLED:
    NILA_OLED.update_oled_text("Hello from NILA")
"""

__all__ = [
    "NILA_LED",
    "NILA_OLED",
]

# Optional: import all for direct access (optional and not strictly required)
# from . import NILA_LED, NILA_OLED