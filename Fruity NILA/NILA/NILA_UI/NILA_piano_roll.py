import channels
import ui

import nihia
from nihia import mixer as mix

from NILA.NILA_engine import config, constants as c, NILA_transform, NILA_core


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
		nihia.mixer.knobs[0][c.piano_roll_knob_volume]: handle_volume_knob,
		nihia.mixer.knobs[1][c.piano_roll_knob_pan]: handle_pan_knob,
	}

	action = knob_actions.get(event.data1)
	if action:
		event.handled = True
		action(event)

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
		NILA_core.setTrackVolConvert(channel_index, f"{updated_volume:.1f} dB")
		mix.setTrackName(channel_index, channels.getChannelName(channel_index))

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
		NILA_transform.updatePanChannel(channel_index, 0)

def get_knob_increment(event):
	"""
	Determines the increment value based on MIDI data.
	"""
	if nihia.mixer.KNOB_DECREASE_MAX_SPEED <= event.data2 <= nihia.mixer.KNOB_DECREASE_MIN_SPEED:
		return -config.channel_increment
	elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
		return config.channel_increment
	return None