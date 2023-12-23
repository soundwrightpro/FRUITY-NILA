"""
Exported Modules List

This section defines the list of modules that are accessible when using the 'from script import *' syntax.
Users can add or remove module names to control which modules are imported and accessible in their script.

- `NILA_buttons`: Module containing functions related to handling buttons.
- `NILA_channel_rack`: Module with functions for interacting with the Channel Rack.
- `NILA_mixer`: Module providing functionality for the Mixer.
- `NILA_navigation`: Module containing navigation-related functions.
- `NILA_piano_roll`: Module with functions related to the Piano Roll.
- `NILA_playlist`: Module for interacting with the Playlist.
- `NILA_plugins`: Module containing functions related to Plugins.
- `NILA_touch_strips`: Module providing functionality for touch strips.

Usage:
    - Add or remove module names within the square brackets to control module imports.
    - For example, to import only 'NILA_buttons' and 'NILA_mixer', modify the list as follows:
        __all__ = ["NILA_buttons", "NILA_mixer"]
    - Ensure that the module names listed here match the actual module filenames in the 'script' package.

Note: Users should update this list based on the specific modules they want to use in their script.

"""
__all__ = ["NILA_buttons", 
           "NILA_channel_rack", 
           "NILA_mixer",
           "NILA_navigation", 
           "NILA_piano_roll", 
           "NILA_playlist",
           "NILA_plugins", 
           "NILA_touch_strips"]