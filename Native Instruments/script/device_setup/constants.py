"""

These constants are used in various parts of the FRUITY NILA code base to maintain version information,
define supported plugins, specify window names and IDs, set touch strip mappings, and establish various
other constants for MIDI script functionality.

"""

# Version information
VERSION_NUMBER = "v14.0.6"
HELLO_MESSAGE = "FRUITY NILA"
GOODBYE_MESSAGE = "by: Duwayne"
OUTPUT_MESSAGE = f"\nFRUITY NILA {VERSION_NUMBER}\nCopyright © 2024 Duwayne\n"
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

unsupported_plugins = [
    "FLEX",
    "Edison",
    "Patcher",
    "Wave Candy",
    "ZGameEditor Visualizer",
    "Distructor",
    "Flatter",
    "Fruity Squeeze",
    "Chorus DEMENSION-D",
    "HalfTime",
    "iZotope Trash 2",
    "Insight",
    "Insight 2",
    "FabFilter Pro-G",
    "Effector",
    "Freezr",
    "Fruity Scratcher",
    "Gatelab",
    "Grossbeat",
    "Ohmygod!",
    "Retronaut",
    "SNESVerb",
    "Bitjuggler",
    "Unfilterted Audio's G8",
    "Lo-Fi-Af",
    "Silo",
    "Izotope's Vinyl",
    "Plogue's Chipcrusher2",
    "Graindad",
    "Stutter Edit",
    "Hardcore",
    "Glitch2",
    "QuadFrohmage",
    "BYOME",
    "Guitar Rig 6",
    "Ampcraft 1992",
    "Archetype Gojira"
]


unsupported_param = [
    "Bypass",
    "",
    "On/Off",
    "System Bypass",
    None
]


#plugin parameter position 
lead_param = 0 
param_skip = 0
param_offset = 0
skip_over = 0

knobs_available = 7
last_plugin_name = None
unused_midi_cc = 144
actual_param_count = 0
knob_offset = 1
unused_param = 4240 #4096 VST parameters, 128 CCs and 16 channels of aftertouch not in use

# Window names and IDs
widTitle = ["Mixer", "Channel Rack", "Playlist", "Piano Roll", "Browser", "Plugin Window", "Effect Plugin", "Generator Plugin"]
winName = {"Mixer": 0, "Channel Rack": 1, "Playlist": 2, "Piano Roll": 3, "Browser": 4, "Plugin": 5, "Effect Plugin": 6, "Generator Plugin": 7}

# Touch strips
touch_strips = {"PITCH": 0, "MOD": 1, "EXPRESSION": 11}

# Constants for MAX and MIN
MAX_Major, MAX_Minor, MAX_Release = 24, 1, 0
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

#stereo separation constant
stereo_sep = 0.25

# Current utility constant
currentUtility = 126

# Blank and not used events
blankEvent, nuText = "   ", "Not Used"

# Item display and time
itemDisp, itemTime = 0, 0

midi_CC_max = 12800

# Mixer right and left constants from the S-Series that aren't included in NIHIA
mixer_right, mixer_left = 63, 65

# Knob speed and delay time before increment is doubled
knob_rotation_speed = 3.5
speed_increase_wait = 0.05  # in milliseconds


# FL Constants

CT_Sampler = 0  # Internal sampler
CT_Hybrid = 1   # Generator plugin feeding internal sampler
CT_GenPlug = 2  # Generator plugin
CT_Layer = 3    # Layer
CT_AudioClip = 4  # Audio clip
CT_AutoClip = 5   # Automation clip

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