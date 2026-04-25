import time
from collections import defaultdict

import channels
import ui

import nihia.mixer as mix

from NILA.NILA_engine import config, constants as c
from NILA.NILA_visuals import NILA_Display as display


# Store last signal times per knob
last_signal_time = defaultdict(lambda: time.time())


def get_adaptive_channel_volume_increment(channel_index, base_increment):
	"""Use FL's Channel Rack dB getter to smooth normalized volume steps.

	FL still expects normalized 0.0..1.0 values on write, but using the dB getter
	here lets us reduce skipped dB values at lower levels.
	"""
	current_db = channels.getChannelVolume(channel_index, True)
	if current_db <= -48.0:
		return base_increment * 0.08
	if current_db <= -36.0:
		return base_increment * 0.12
	if current_db <= -24.0:
		return base_increment * 0.20
	if current_db <= -12.0:
		return base_increment * 0.35
	if current_db <= -6.0:
		return base_increment * 0.50
	return base_increment


def adjust_channel_value(channel_value, data2, increment, speed=0):
	"""
	Adjusts the channel value based on MIDI input.

	Parameters:
	- channel_value (float): The current value of the channel parameter (volume or pan).
	- data2 (int): The MIDI data2 value indicating the direction of adjustment.
	- increment (float): The base increment value for adjustment.
	- speed (float): The speed of adjustment.

	Returns:
	- float: The adjusted channel value.
	"""
	if c.encoder_cc_dec_fast_min <= data2 <= c.encoder_cc_dec_fast_max:
		return channel_value - increment
	elif c.encoder_cc_dec_slow_min <= data2 <= c.encoder_cc_dec_slow_max:
		return channel_value - increment
	elif c.encoder_cc_inc_slow_min <= data2 <= c.encoder_cc_inc_slow_max:
		return channel_value + increment
	elif c.encoder_cc_inc_fast_min <= data2 <= c.encoder_cc_inc_fast_max:
		return channel_value + increment
	elif speed != 0:
		return channel_value + speed
	else:
		return channel_value


def OnMidiMsg(self, event):
	"""
	Handles MIDI messages for channel adjustment in the Channel Rack.

	Parameters:
	- self: The instance of the script.
	- event: The MIDI event.
	"""
	if not ui.getFocused(c.winName["Channel Rack"]):
		return

	knob_speed = 0

	for control_type in (0, 1):  # 0 for volume, 1 for pan
		for z in range(c.max_knobs):
			if channels.channelCount() <= z or channels.selectedChannel() >= (channels.channelCount() - z):
				continue

			knob_data = mix.knobs[control_type][z]
			current_channel = channels.selectedChannel() + z
			current_value = (
				channels.getChannelVolume(current_channel) if control_type == 0
				else channels.getChannelPan(current_channel)
			)

			if event.data1 == knob_data:
				event.handled = True

				current_time = time.time()
				time_difference = current_time - last_signal_time[z]
				last_signal_time[z] = current_time

				base_increment = config.channel_increment * c.knob_rotation_speed if time_difference <= c.speed_increase_wait else config.channel_increment
				adjusted_increment = get_adaptive_channel_volume_increment(current_channel, base_increment) if control_type == 0 else base_increment

				new_value = adjust_channel_value(current_value, event.data2, adjusted_increment, knob_speed)

				if control_type == 0:
					new_value = max(0.0, min(1.0, new_value))
					channels.setChannelVolume(current_channel, new_value)
				else:
					new_value = max(-1.0, min(1.0, new_value))
					channels.setChannelPan(current_channel, new_value)

	# Refresh display once per event, not per knob
	display.OnRefresh(self, event)