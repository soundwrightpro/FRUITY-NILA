"""
script_constants.py

These constants are used in various parts of the FRUITY NILA code base to maintain version information,
define supported plugins, specify window names and IDs, set touch strip mappings, and establish various
other constants for MIDI script functionality.

Author: Duwayne
Copyright © 2023 Duwayne

"""

# Version information
VERSION_NUMBER = "v12.0.2"
HELLO_MESSAGE = "FRUITY NILA"
GOODBYE_MESSAGE = "by: Duwayne"
OUTPUT_MESSAGE = f"\nFRUITY NILA {VERSION_NUMBER}\nCopyright © 2023 Duwayne\n"
LOAD_MESSAGE = "Project Loaded"

# Supported plugins dictionary
supported_plugins = {
    "FL Keys": 0,
    "FLEX": 1,
    "Sytrus": 2,
    "GMS": 3,
    "Harmless": 4,
    "Harmor": 5,
    "Morphine": 6,
    "3x Osc": 7,
    "Fruity DX10": 8,
    "BassDrum": 9,
    "MiniSynth": 10,
    "PoiZone": 11,
    "Sakura": 12
}

# Window names and IDs
widTitle = ["Mixer", "Channel Rack", "Playlist", "Piano Roll", "Browser", "Plugin Window", "Effect Plugin", "Generator Plugin"]
winName = {"Mixer": 0, "Channel Rack": 1, "Playlist": 2, "Piano Roll": 3, "Browser": 4, "Plugin": 5}

# Touch strips
touch_strips = {"PITCH": 0, "MOD": 1, "EXPRESSION": 11}

# Constants for MAX and MIN
MAX_Major, MAX_Minor, MAX_Release = 21, 0, 0
MIN_Major, MIN_Minor, MIN_Release = 21, 0, 0

# On and Off constants
off, on = 0, 1

# MIDI Script Version
MIDI_Script_Version = 23

# Time delay
timedelay = 0.35

# Select constant
select = 66

# Controls constant
controls = 15

# Waiting input messages
wait_input_1, wait_input_2 = "Waiting", "for input...     "

# Current utility constant
currentUtility = 126

# Blank and not used events
blankEvent, nuText = "   ", "Not Used"

# Item display and time
itemDisp, itemTime = 0, 0

# Mixer right and left constants
mixer_right, mixer_left = 63, 65

# Knob speed and delay time before increment is doubled
knob_rotation_speed = 3.5
speed_increase_wait = 0.05  # in milliseconds

# FL Constants
# FL project file types and their associated constants
PL_Start, PL_LoadOk, PL_LoadError = 0, 100, 101
SBN_FLP, SBN_ZIP, SBN_FLM, SBN_FST, SBN_DS, SBN_SS, SBN_WAV, SBN_XI, SBN_FPR, SBN_FSC, SBN_SF2, SBN_Speech, \
SBN_MP3, SBN_OGG, SBN_FLAC, SBN_OSM, SBN_REX, SBN_DWP, SBN_FNV, SBN_FXB, SBN_AIFF, SBN_TXT, SBN_BMP, SBN_WV, \
SBN_TS, SBN_RBS, SBN_MID, SBN_FLEXPack, SBN_NEWS, SBN_SHOP, SBN_LIB, SBN_LIBOWNED, SBN_NOTIFICATION, SBN_DOWNLOAD, \
SBN_M4A = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35

# Dictionary mapping file extensions to FL node constants
FL_node = {'B| .FLP': 1, 'B| .ZIP': 2, 'B| FL Proj.': 3, 'B| FL Preset': 4, 'B| .WAV': 7, 'B| .SF2': 11, 'B| .SPEECH': 12,
           'B| .MP3': 13, 'B| .OGG': 14, 'B| .FLAC': 15, 'B| .FNV': 19, 'B| .AIFF': 21, 'B| .TXT': 22,
           'B| IMAGE File': 23, 'B| .WV': 24, 'B| .MIDI': 27, 'B| FLEX PACK': 28, 'B| .MP4': 35, 'B| .INI': 37,
           'B| .FSC': 10}