"""
User editable Fruity NILA configuration.

Only change values in this file if you want to customize how Fruity NILA feels.
These settings are intentionally separated from constants.py:

- config.py = user adjustable behavior
- constants.py = fixed internal values, labels, MIDI values, and shared names

Recommended editing rule:
Change one setting at a time, reload the script in FL Studio, and test before
changing another setting.
"""

# ==== Browser preview behavior ====

# Controls preview sound when using the large jog encoder in the Browser.
#
# 0 = do not trigger FL Studio's Browser preview sound while jogging
# 1 = trigger Browser preview sound while jogging
#
# Recommended: 0
# Use 0 if jogging through folders or large libraries becomes noisy.
jog_preview_sound = 0

# Controls preview sound when using Up and Down navigation in the Browser.
#
# 0 = do not trigger FL Studio's Browser preview sound while moving up or down
# 1 = trigger Browser preview sound while moving up or down
#
# Recommended: 1
# This lets Up and Down preview samples while keeping jog wheel browsing quiet.
upDown_preview_sound = 1


# ==== Red selection rectangle timing ====

# How long the red selection rectangle remains visible in the Channel Rack.
# Value is in milliseconds.
#
# 0 = do not show the rectangle
# 500 = half a second
# 2000 = two seconds
#
# Recommended: 2000
rectChannel = 2000

# How long the red selection rectangle remains visible in the Mixer.
# Value is in milliseconds.
#
# 0 = do not show the rectangle
# 500 = half a second
# 2000 = two seconds
#
# Recommended: 2000
rectMixer = 2000


# ==== Mixer knob feel ====

# Mixer volume and pan increment per knob movement.
#
# Lower values = finer control, slower movement
# Higher values = faster movement, less precision
#
# Recommended: 0.005
# Safe range: 0.001 to 0.02
# Avoid very high values unless you want large jumps.
mixer_increment = 0.005

# Speed multiplier used when the mixer knob is turned quickly.
#
# Lower values = less acceleration
# Higher values = more acceleration
#
# Recommended: 3.5
# Safe range: 1.0 to 6.0
mixer_knob_rotation_speed = 3.5

# Time window used to detect fast repeated mixer knob movement.
# Value is in seconds.
#
# Lower values = acceleration triggers only with very fast movement
# Higher values = acceleration triggers more easily
#
# Recommended: 0.05
# Safe range: 0.02 to 0.12
mixer_speed_increase_wait = 0.05


# ==== Mixer 0 dB snap feel ====

# Enables or disables the mixer only 0 dB snap.
#
# 0 = off
# 1 = on
#
# Recommended: 1
# This affects Mixer volume only. It does not affect Channel Rack volume.
mixer_zero_db_snap_enabled = 1

# Snap range around 0 dB for Mixer volume.
# Value is in dB, not normalized volume.
#
# Lower values = subtle snap
# Higher values = stronger, stickier snap
#
# Recommended: 1.0
# Suggested range: 0.2 to 1.0
mixer_zero_db_snap_range = 1.0

# Short hold after the mixer fader snaps to 0 dB.
# Value is in seconds.
#
# This creates a small detent feel so 0 dB is easier to land on. After the hold
# expires, the next knob movement is allowed through so the fader does not stay
# trapped at 0 dB.
#
# Recommended: 0.15
# Suggested range: 0.05 to 0.25
mixer_zero_db_hold_time = 0.15


# ==== Channel Rack knob feel ====

# Channel Rack volume and pan increment per knob movement.
#
# Channel Rack controls are more sensitive than Mixer controls.
#
# Lower values = finer control, slower movement
# Higher values = faster movement, less precision
#
# Recommended: 0.01
# Safe range: 0.005 to 0.03
channel_increment = 0.01


# ==== Button timing ====

# Maximum time between two presses for Fruity NILA to treat them as a double click.
# Value is in seconds.
#
# Lower values = double click must be faster
# Higher values = double click can be slower
#
# Recommended: 0.500
double_click_speed = 0.500