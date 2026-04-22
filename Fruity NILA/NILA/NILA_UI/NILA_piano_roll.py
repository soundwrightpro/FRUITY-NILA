import channels
import ui

from nihia import mixer as mix
from NILA.NILA_engine import config, constants as c, NILA_transform
from NILA.NILA_visuals import NILA_OLED

PIANO_ROLL_KNOB_VOLUME = getattr(c, "piano_roll_knob_volume", 0)
PIANO_ROLL_KNOB_PAN = getattr(c, "piano_roll_knob_pan", 1)


def OnMidiMsg(self, event):
	"""
	Handles MIDI messages for the Piano Roll window.

	Args:
		self: The instance of the NILA system.
		event: The MIDI event triggered by the MIDI controller.
	"""
	if not ui.getFocused(c.winName["Piano Roll"]):
		return

	# Map knob numbers to actions using constants
	knob_actions = {
		mix.knobs[0][PIANO_ROLL_KNOB_VOLUME]: handle_volume_knob,
		mix.knobs[1][PIANO_ROLL_KNOB_PAN]: handle_pan_knob,
	}

	action = knob_actions.get(event.data1)
	if action:
		event.handled = True
		action(event)

def refresh_piano_roll_display(channel_index):
	"""Delegate Piano Roll display refresh to the OLED module."""
	if hasattr(NILA_OLED, "refresh_piano_roll_display"):
		NILA_OLED.refresh_piano_roll_display(channel_index)

def handle_volume_knob(event):
	channel_index = channels.selectedChannel()
	current_volume = channels.getChannelVolume(channel_index)
	increment = get_knob_increment(event)
	if increment is not None:
		updated_volume = NILA_transform.clamp(
			current_volume + increment, 
			c.track_volume_min, 
			c.track_volume_max
		)
		channels.setChannelVolume(channel_index, updated_volume)
		refresh_piano_roll_display(channel_index)

def handle_pan_knob(event):
	channel_index = channels.selectedChannel()
	current_pan = channels.getChannelPan(channel_index)
	increment = get_knob_increment(event)
	if increment is not None:
		updated_pan = NILA_transform.clamp(
			current_pan + increment,
			c.plugin_param_min,
			c.plugin_param_max
		)
		channels.setChannelPan(channel_index, updated_pan)
		refresh_piano_roll_display(channel_index)

def get_knob_increment(event):
	"""
	Determines the increment value based on MIDI data.
	"""
	if mix.KNOB_DECREASE_MAX_SPEED <= event.data2 <= mix.KNOB_DECREASE_MIN_SPEED:
		return -config.channel_increment
	elif mix.KNOB_INCREASE_MIN_SPEED <= event.data2 <= mix.KNOB_INCREASE_MAX_SPEED:
		return config.channel_increment
	return None