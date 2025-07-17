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
        """Calculate a new channel value from MIDI input.

        Args:
                channel_value: Current value of the parameter.
                data2: MIDI data controlling the adjustment direction.
                increment: Base increment to apply.
                speed: Optional direct speed amount.

        Returns:
                The adjusted channel value.
        """
	if c.encoder_cc_dec_fast_min <= data2 <= c.encoder_cc_dec_fast_max:  # Fast decrement
		return round(channel_value - increment, 2)
	elif c.encoder_cc_dec_slow_min <= data2 <= c.encoder_cc_dec_slow_max:  # Slow decrement
		return round(channel_value - increment, 2)
	elif c.encoder_cc_inc_slow_min <= data2 <= c.encoder_cc_inc_slow_max:  # Slow increment
		return round(channel_value + increment, 2)
	elif c.encoder_cc_inc_fast_min <= data2 <= c.encoder_cc_inc_fast_max:  # Fast increment
		return round(channel_value + increment, 2)
	elif speed != 0:
		return round(channel_value + speed, 2)
	else:
		return channel_value

def OnMidiMsg(self, event):
        """Handle channel rack knob messages.

        Args:
                self: Script instance.
                event: Incoming MIDI event.

        Returns:
                None.
        """
        if not ui.getFocused(c.winName["Channel Rack"]):
                return  # Exit early if Channel Rack is not focused

	knob_speed = 0
	is_s_series = seriesCheck()  # Avoid redundant calls

	for control_type in (0, 1):  # 0 for volume, 1 for pan
		for z in range(c.max_knobs):
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
