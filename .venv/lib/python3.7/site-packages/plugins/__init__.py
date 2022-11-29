"""Plugins Module (FL Studio built-in)

Handles the way that scripts communicate with and control FL Studio plugins,
including 3rd-party VST/AU plugins. The module allows scripts to get and set 
parameter values for plugins on the mixer and the channel rack.

Module added in API version 8.

NOTES:
 * `index` either refers to the index of the plugin on the channel rack, or the
   index of the mixer track containing the plugin on the mixer.
 * `slotIndex` refers the the mixer slot of the plugin if it is on the mixer.
   Leave this parameter empty if the plugin is on the channel rack.
"""

from .plugins import *
