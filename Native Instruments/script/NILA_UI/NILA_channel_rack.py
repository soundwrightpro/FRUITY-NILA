import nihia
from nihia import *
from script.device_setup.NILA_core import seriesCheck
from script.device_setup import config
from script.device_setup import constants as c
from script.screen_writer import NILA_OLED as oled
import channels
import ui
import time
from collections import defaultdict

# Store last signal times per knob
last_signal_time = defaultdict(lambda: time.time())

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
	if data2 >= 96:  # Large decrement
		return round(channel_value - increment, 2)
	elif data2 >= 65:  # Small decrement
		return round(channel_value - increment, 2)
	elif data2 >= 32:  # Small increment
		return round(channel_value + increment, 2)
	elif data2 >= 0:   # Large increment
		return round(channel_value + increment, 2)
	elif speed != 0:
		return round(channel_value + speed, 2)
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
		return  # Exit early if Channel Rack is not focused

	knob_speed = 0
	is_s_series = seriesCheck()  # Avoid redundant calls

	for control_type in (0, 1):  # 0 for volume, 1 for pan
		for z in range(8):
			if channels.channelCount() <= z or channels.selectedChannel() >= (channels.channelCount() - z):
				continue  # Skip if out of range

			knob_data = nihia.mixer.knobs[control_type][z]
			current_channel = channels.selectedChannel() + z
			current_value = (
				channels.getChannelVolume(current_channel) if control_type == 0
				else channels.getChannelPan(current_channel)
			)

			if event.data1 == knob_data:
				event.handled = True

				# Time-based adjustment
				current_time = time.time()
				time_difference = current_time - last_signal_time[z]
				last_signal_time[z] = current_time

				adjusted_increment = config.increment * c.knob_rotation_speed if time_difference <= c.speed_increase_wait else config.increment

				new_value = adjust_channel_value(current_value, event.data2, adjusted_increment, knob_speed)

				if control_type == 0:
					channels.setChannelVolume(current_channel, new_value)
				else:
					channels.setChannelPan(current_channel, new_value)

	# Refresh OLED display once per event, not per knob
	oled.OnRefresh(self, event)