import nihia
from nihia import mixer as mix
from script.device_setup import config, constants, NILA_transform, NILA_core
import channels
import ui

def OnMidiMsg(self, event):
	"""
	Handles MIDI messages for the Piano Roll window.

	Args:
		self: The instance of the NILA system.
		event: The MIDI event triggered by the MIDI controller.
	"""
	if ui.getFocused(constants.winName["Piano Roll"]):
		if event.data1 in (nihia.mixer.knobs[0][0], nihia.mixer.knobs[1][0]):
			event.handled = True
			handle_knob(event)

def handle_knob(event):
	"""
	Handles knob events for adjusting volume or pan in the Piano Roll.

	Args:
		event: The MIDI event triggered by a knob.
	"""
	channel_index = 0
	selected_channel = channels.selectedChannel() + channel_index
	
	# Determine whether the event is for volume (knob 0) or pan (knob 1)
	if event.data1 == nihia.mixer.knobs[0][0]:  # Volume control
		current_value = channels.getChannelVolume(selected_channel)
		update_function = adjust_channel_volume
	elif event.data1 == nihia.mixer.knobs[1][0]:  # Pan control
		current_value = channels.getChannelPan(selected_channel)
		update_function = adjust_channel_pan
	else:
		return  # Ignore other events

	# Adjust value based on MIDI input
	increment = get_knob_increment(event)
	if increment is not None:
		update_function(selected_channel, current_value, increment)

def get_knob_increment(event):
	"""
	Determines the increment value based on MIDI data.

	Args:
		event: The MIDI event.

	Returns:
		float: The calculated increment value, or None if the event is not valid.
	"""
	if nihia.mixer.KNOB_DECREASE_MAX_SPEED <= event.data2 <= nihia.mixer.KNOB_DECREASE_MIN_SPEED:
		return -config.increment
	elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
		return config.increment
	return None  # Ignore if outside valid range

def adjust_channel_volume(channel_index, current_volume, increment):
	"""
	Adjusts the volume of a channel.

	Args:
		channel_index: Index of the channel.
		current_volume: Current volume level.
		increment: Amount to adjust.
	"""
	updated_volume = round(current_volume + increment, 2)
	channels.setChannelVolume(channel_index, updated_volume)
	NILA_core.setTrackVolConvert(channel_index, f"{updated_volume:.1f} dB")
	mix.setTrackName(channel_index, channels.getChannelName(channel_index))

def adjust_channel_pan(channel_index, current_pan, increment):
	"""
	Adjusts the pan of a channel.

	Args:
		channel_index: Index of the channel.
		current_pan: Current pan value.
		increment: Amount to adjust.
	"""
	updated_pan = round(current_pan + increment, 2)
	channels.setChannelPan(channel_index, updated_pan)
	NILA_transform.updatePanChannel(channel_index, 0)
