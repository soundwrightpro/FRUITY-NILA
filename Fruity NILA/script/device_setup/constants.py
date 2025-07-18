"""
constants.py - Core constants for the Fruity NILA FL Studio MIDI scripting system.

This file contains all shared constants for device identification, plugin support, 
window and UI mapping, MIDI handling, knob/encoder behaviors, and generic fallback values.

- All plugin, parameter, window, and device mappings should be defined here.
- If you update any feature with new hard-coded numbers or settings, add them here with a comment.

Sections:
- Version and general info
- Plugin support lists
- Window/UI mappings
- MIDI and controller values
- Track/knob/pan/volume logic
- Miscellaneous UI values
- FL Studio/NI integration specifics

Last updated: July 2025
"""

import midi

# ===== VERSION & GENERAL INFO =====
VERSION_NUMBER = "v2025.0.4"
HELLO_MESSAGE = "FRUITY NILA"
GOODBYE_MESSAGE = "by: sound"
OUTPUT_MESSAGE = f"\nFRUITY NILA {VERSION_NUMBER}\n"
LOAD_MESSAGE = "Project Loaded"
DISCORD = "https://discord.com/invite/GeTTWBV"

# ===== MIDI ALIASES (redirect to midi module) =====
PL_Start = midi.PL_Start
PL_LoadOk = midi.PL_LoadOk
PL_LoadError = midi.PL_LoadError

CT_Sampler = midi.CT_Sampler
CT_Hybrid = midi.CT_Hybrid
CT_GenPlug = midi.CT_GenPlug
CT_Layer = midi.CT_Layer
CT_AudioClip = midi.CT_AudioClip
CT_AutoClip = midi.CT_AutoClip

REC_Control = midi.REC_Control
REC_Smoothed = midi.REC_Smoothed
REC_InternalCtrl = midi.REC_InternalCtrl
REC_NoSaveUndo = midi.REC_NoSaveUndo
REC_GetValue = midi.REC_GetValue

FPT_Play = midi.FPT_Play
FPT_Stop = midi.FPT_Stop
FPT_Record = midi.FPT_Record
FPT_Enter = midi.FPT_Enter
FPT_Escape = midi.FPT_Escape
FPT_NextWindow = midi.FPT_NextWindow

Snap_Line = midi.Snap_Line
Snap_Bar = midi.Snap_Bar

widMixer = midi.widMixer
widChannelRack = midi.widChannelRack
widPlaylist = midi.widPlaylist
widPianoRoll = midi.widPianoRoll
widBrowser = midi.widBrowser
widPlugin = midi.widPlugin
widPluginEffect = midi.widPluginEffect
widPluginGenerator = midi.widPluginGenerator

# Encoder CC thresholds for speed-based knob behavior
encoder_cc_inc_fast_min = 0
encoder_cc_inc_fast_max = 31
encoder_cc_inc_slow_min = 32
encoder_cc_inc_slow_max = 64
encoder_cc_dec_slow_min = 65
encoder_cc_dec_slow_max = 95
encoder_cc_dec_fast_min = 96
encoder_cc_dec_fast_max = 127

# Version range required by Fruity NILA
MIN_Major = 25
MIN_Minor = 1
MIN_Release = 0
MAX_Major = 25
MAX_Minor = 99
MAX_Release = 999
MIDI_Script_Version = 38

itemDisp = 0
itemTime = 0

# ===== PLUGIN SUPPORT =====
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
	"FLEX", "Edison", "Patcher", "Wave Candy", "ZGameEditor Visualizer",
	"Distructor", "Flatter", "Fruity Squeeze", "Chorus DEMENSION-D",
	"HalfTime", "iZotope Trash 2", "Insight", "Insight 2", "FabFilter Pro-G",
	"Effector", "Freezr", "Fruity Scratcher", "Gatelab", "Grossbeat",
	"Ohmygod!", "Retronaut", "SNESVerb", "Bitjuggler", "Unfilterted Audio's G8",
	"Lo-Fi-Af", "Silo", "Izotope's Vinyl", "Plogue's Chipcrusher2",
	"Graindad", "Stutter Edit", "Hardcore", "Glitch2", "QuadFrohmage",
	"BYOME", "Guitar Rig 6", "Ampcraft 1992", "Archetype Gojira"
]
unsupported_param = ["Bypass", "", "On/Off", "System Bypass", None]

# ===== PLUGIN PARAMETER POSITIONING =====
lead_param = 0
param_skip = 0
param_offset = 0
skip_over = 0
gen_plugin = -1

last_plugin_name = None
actual_param_count = 0
unused_param = 4240
unused_midi_cc = 144
knob_offset = 1
knobs_available = 7

# ===== WINDOW AND UI MAPPINGS =====
widTitle = [
	"Mixer", "Channel Rack", "Playlist", "Piano Roll", "Browser", 
	"Plugin Window", "Effect Plugin", "Generator Plugin"
]
winName = {
	"Mixer": 0, "Channel Rack": 1, "Playlist": 2, "Piano Roll": 3, "Browser": 4,
	"Plugin": 5, "Effect Plugin": 6, "Generator Plugin": 7
}

# ===== TOUCH STRIP / MIDI MAPPING =====
touch_strips = {"PITCH": 0, "MOD": 1, "EXPRESSION": 11}

# ===== ON/OFF, GENERIC, AND UI MESSAGES =====
off = 0
on = 1
wait_input_1 = "Waiting"
wait_input_2 = "for input...     "
blankEvent = "   "
nuText = "Not Used"
unnamed_param = "Unnamed Param"
timedelay = 0.35
select = 66
controls = 15

# ===== MIXER / CHANNEL / KNOB / VOLUME HANDLING =====
max_knobs = 8
min_knob_number = 1
max_knob_number = 7
first_knob_index = 1
purge_start_index = 1
current_track_name = "Current"
currentUtility = -1

# used as a target track for playlist-linked controls
playlist_track_index = 0
display_track_index = 0
mixer_knob_count = 8

# ==== Value Ranges and Scaling ====
track_volume_min = 0.0
track_volume_max = 1.0
plugin_param_min = 0
plugin_param_max = 1
volume_percent_min = 0
volume_percent_max = 100

volume_param_type = "volume"
pan_param_type = "pan"
stereo_sep = 0.25
oled_vol_bar_scaling = 0.86

# ==== KNOB SPEEDUP HANDLING ====
knob_rotation_speed = 3.5
speed_increase_wait = 0.05
knob_sensitivity_speedup = 1.5
knob_sensitivity_wait = 0.05

# ==== MISC NAVIGATION ====
jog_step_small = 1
jog_step_large = 8
piano_roll_rect_width = 256
piano_roll_rect_height = 8
menu_item_value = 4
plugin_picker_value = 67
plugin_skip_value = 1
plugin_nav_forward = 1

# ==== MIXER PLUGIN HANDLING ====
mix_slot_volume_min = 0
mix_slot_volume_max = 12800
global_plugin_slot = -1
plugin_effect_none = -1

# ==== MIXER ENCODER BUTTONS ====
mixer_right = 63
mixer_left = 65

# ==== DEVICE INTEGRATION ====
HANDSHAKE_SYSEX = bytes([
	240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 64, 1, 0, 247
])

last_form_id = -999  # Init to impossible value
