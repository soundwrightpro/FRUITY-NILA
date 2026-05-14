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

Last updated: April 2026
"""

import midi

# ===== VERSION & GENERAL INFO =====
VERSION_NUMBER = "v2026.0.3"
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
widPlugin = midi.widPlugin # type: ignore[attr-defined]
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

# Generator plugins that need direct FL UI navigation instead of parameter or preset navigation.
direct_navigation_plugins = [
	"FLEX"
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

# ===== BROWSER FILE TYPE NODES =====
FL_node = {
	'B| .FLP': 1, 'B| .ZIP': 2, 'B| FL Proj.': 3, 'B| FL Preset': 4, 'B| .WAV': 7, 
	'B| .SF2': 11, 'B| .SPEECH': 12, 'B| .MP3': 13, 'B| .OGG': 14, 'B| .FLAC': 15, 'B| .FNV': 19, 
	'B| .AIFF': 21, 'B| .TXT': 22, 'B| IMAGE File': 23, 'B| .WV': 24, 'B| .MIDI': 27, 'B| FLEX PACK': 28, 
	'B| .MP4': 35, 'B| .INI': 37, 'B| .FSC': 10
}

# ===== FL PROJECT / NODE CONSTANTS =====
SBN_FLP, SBN_ZIP, SBN_FLM, SBN_FST, SBN_DS, SBN_SS, SBN_WAV, SBN_XI, SBN_FPR, SBN_FSC, SBN_SF2, SBN_Speech, \
SBN_MP3, SBN_OGG, SBN_FLAC, SBN_OSM, SBN_REX, SBN_DWP, SBN_FNV, SBN_FXB, SBN_AIFF, SBN_TXT, SBN_BMP, SBN_WV, \
SBN_TS, SBN_RBS, SBN_MID, SBN_FLEXPack, SBN_NEWS, SBN_SHOP, SBN_LIB, SBN_LIBOWNED, SBN_NOTIFICATION, SBN_DOWNLOAD, \
SBN_M4A = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35


# ===== TOUCH STRIP / MIDI MAPPING =====
touch_strips = {"PITCH": 0, "MOD": 1, "EXPRESSION": 11}

# ===== GENERIC, AND UI MESSAGES =====
wait_input_1 = "Waiting"
wait_input_2 = "for input...     "
blankEvent = "   "
nuText = "Not Used"
unnamed_param = "Unnamed Param"

# Generic UI timing
ui_time_delay = 0.35
focus_overlay_refresh_interval = 0.05

# MIDI channels
select = 66
controls = 15

# Display labels
focus_display_name = "Focus"
playlist_display_name = "Playlist"

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
display_vol_bar_scaling = 0.86

# Mixer 0 dB snap behavior
mixer_zero_db_value = 0.8
mixer_zero_db_snap_range = 1.0
mixer_zero_db_hold_time = 0.15

# NI peak meter data
peak_meter_data_length = 16
peak_meter_max_value = 127

# Mixer display strings
mixer_centered_pan_text = "Centered"
mixer_pan_right_suffix = "% Right"
mixer_pan_left_suffix = "% Left"

# ==== KNOB SPEEDUP HANDLING ====
knob_rotation_speed = 3.5
speed_increase_wait = 0.05
knob_sensitivity_speedup = 1.5
knob_sensitivity_wait = 0.05

# ==== MISC NAVIGATION ====
jog_step_small = 1
jog_step_large = 8
mixer_x_axis_step = jog_step_large
piano_roll_rect_width = 256
piano_roll_rect_height = 8
menu_item_value = 4
plugin_picker_value = 67
plugin_skip_value = 1
plugin_nav_forward = 1
plugin_nav_page = 7

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

# ===== MIDI CONSTANTS (NOT EXPOSED BY FL API) =====
midi_cc_max = 127
midi_pitch_bend_center = 8192
midi_pitch_bend_max = 16383
midi_status_pitch_bend = 0xE0
midi_status_mask = 0xF0

# ===== PLUGIN PARAMETER OFFSETS =====
plugin_param_expression_base = 4096
plugin_param_modulation = 4097
plugin_param_mode = 2

# ===== BROWSER AND JOGGING THRESHOLDS =====
marker_jump_forward = 1
browser_menu_threshold = -100

# ===== VIEWPORT / ZOOM =====
zoom_step_small = 1

# ===== S SERIES DISPLAY LAYOUT =====
s_series_slot_count = 8
s_series_primary_slots = 4
s_series_browser_slots = 3
s_series_display_slot_width = 8
s_series_text_total_width = 32
s_series_focus_overlay_duration = 0.6
s_series_focus_label = "Focus:"
s_series_playlist_label = "Playlist:"
s_series_browser_label = "Browser:"

# ===== PLAYLIST DISPLAY LABELS =====
playlist_beats_label = "Beats|"
playlist_bars_label = "Bars:"
playlist_minutes_label = "Minutes|"
playlist_seconds_label = "Seconds:"
playlist_bpm_prefix = "bpm"

# ===== MIXER INERTIA SCROLLING =====
mixer_inertia_acceleration = 1.75
mixer_inertia_decay = 0.76
mixer_inertia_stop_threshold = 0.25
mixer_inertia_step_interval = 0.035
mixer_inertia_max_velocity = 8.0
mixer_inertia_trigger_interval = 0.055
mixer_inertia_trigger_count = 2

# ===== COMMON UI HINTS =====
hint_no_channel_generators = "No Channel Rack generators"
hint_generator_plugin_window = "Generator plugin window"
hint_channel_rack_rect = "Channel Rack selection rectangle"
hint_playlist_tool_prefix = "Playlist Tool:"
hint_open_menu = "Open Menu"
hint_enter = "Enter"
hint_select_menu_item = "Select menu item"
hint_toggle_browser_node = "Toggle browser node"
hint_plugin_picker = "Plugin Picker"
hint_reverse_polarity = "Reverse polarity"
hint_swap_lr_channels = "Swap L/R channels"
hint_previous_preset = "Previous preset"
hint_next_preset = "Next preset"
hint_right = "Right"
hint_left = "Left"
hint_up = "Up"
hint_down = "Down"