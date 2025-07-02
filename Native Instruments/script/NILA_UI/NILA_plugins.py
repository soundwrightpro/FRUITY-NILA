import nihia
from script.device_setup import NILA_core, constants as c, config
from script.screen_writer import NILA_OLED
from script.NILA_UI import NILA_channel_rack
import channels
import mixer
import midi
import general
import time
import ui
import plugins
from collections import defaultdict

# Store last signal times per knob
last_signal_time = defaultdict(lambda: time.time())

def plugin(self, event):
	"""Handles plugin-related events and delegates control."""
	if ui.getFocused(c.winName["Plugin"]):
		if ui.getFocused(c.winName["Generator Plugin"]):
			channel_index = channels.selectedChannel() 
			if not plugins.isValid(channel_index, c.gen_plugin):
				return
			else:
				handle_channel_generator(self, event)
				setGenPluginVolumePan(self, event)
		else:
			handle_mixer_effect(self, event)	
		plugin_set_param(self, event)
	
def plugin_set_param(self, event):
	"""Sets parameters for the plugin based on the focused window."""
	use_global_index = False
	effect_info = mixer.getActiveEffectIndex()

	if effect_info is None or effect_info == (0, -1):
		return  # No effect is focused

	track_index, mixer_slot = effect_info
	full_plugin_name = plugins.getPluginName(track_index, mixer_slot)

	if full_plugin_name not in c.unsupported_plugins:
		c.param_offset = max(c.skip_over, 0)

		if c.actual_param_count <= 0:
			return  # No available parameters

		for knob_number in range(1, min(c.actual_param_count, 8 + c.param_offset)):
			param_index = max(min(knob_number - 1 + c.lead_param, c.actual_param_count - 1), 0)
			param_name = plugins.getParamName(param_index, track_index, mixer_slot, use_global_index)

			if not param_name:
				param_name = "Unnamed Param"  # Fallback

			if param_name not in c.unsupported_param:
				knob_number = max(1, min(knob_number - c.skip_over, 7))
				knob_data = nihia.mixer.knobs[0][knob_number]
				volume_increment = config.increment

				if event.data1 == knob_data:
					adjusted_increment = knob_time_check(self, volume_increment)
					handle_param_control(self, event, param_index, track_index, mixer_slot, use_global_index, adjusted_increment, param_name)

		NILA_OLED.OnRefresh(self, event)

def handle_channel_generator(self, event):
	"""Sets parameters for the selected generator plugin in the Channel Rack."""
	use_global_index = False
	channel_index = channels.selectedChannel()
	full_plugin_name = plugins.getPluginName(channel_index, c.gen_plugin)

	if not plugins.isValid(channel_index, c.gen_plugin):
		return  # No valid plugin loaded
	
	if full_plugin_name not in c.unsupported_plugins:
		param_count = plugins.getParamCount(channel_index, c.gen_plugin, use_global_index)

		if param_count <= 0:
			return  # No parameters to map

		c.param_offset = max(c.skip_over, 0)

		for knob_number in range(1, min(param_count + c.knob_offset, 8 + c.param_offset)):
			param_index = max(min(knob_number - 1 + c.lead_param, param_count - 1), 0)
			param_name = plugins.getParamName(param_index, channel_index, c.gen_plugin, use_global_index)

			if not param_name:
				param_name = "Unnamed Param"

			if param_name not in c.unsupported_param:
				knob_number = max(1, min(knob_number - c.skip_over, 7))
				knob_data = nihia.mixer.knobs[0][knob_number]
				volume_increment = config.increment

				if event.data1 == knob_data:
					adjusted_increment = knob_time_check(self, volume_increment)
					handle_param_control(
						self, event,
						param_index=param_index,
						track_index=channel_index,
						mixer_slot=c.gen_plugin,
						use_global_index=use_global_index,
						volume_increment=adjusted_increment,
						param_name=param_name
					)

		NILA_OLED.OnRefresh(self, event)

def send_hint_message(parameter_name):
	"""Formats and sends a hint message."""
	formatted_name = ""
	for i, char in enumerate(parameter_name):
		if i > 0 and char.isupper() and parameter_name[i - 1] != " ":
			formatted_name += " "  # Insert space for readability
		formatted_name += char
	ui.setHintMsg(formatted_name)

def handle_param_control(self, event, param_index, track_index, mixer_slot, use_global_index, volume_increment, param_name):
	"""Handles parameter control events for plugins."""
	pickup_mode = 0
	param_value = plugins.getParamValue(param_index, track_index, mixer_slot, use_global_index)
	new_param_value = param_value

	if NILA_core.seriesCheck():
		if 65 <= event.data2 < 95 or 96 <= event.data2 < 128:
			new_param_value = max(param_value - volume_increment, 0)
		elif 0 <= event.data2 < 31 or 32 <= event.data2 < 64:
			new_param_value = min(param_value + volume_increment, 1)
	else:
		if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
			new_param_value = max(param_value - volume_increment, 0)
		elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
			new_param_value = min(param_value + volume_increment, 1)

	plugins.setParamValue(new_param_value, param_index, track_index, mixer_slot, pickup_mode, use_global_index)
	NILA_OLED.OnRefresh(self, event)

def handle_mixer_effect(self, event):
	"""Handles mixer effect mix level changes."""
	effect_info = mixer.getActiveEffectIndex()
	if effect_info is None:
		return  # No effect focused

	track_index, mixer_slot = effect_info
	track_plugin_id = mixer.getTrackPluginId(track_index, mixer_slot)
	event_id = midi.REC_Plug_MixLevel + track_plugin_id
	mix_slot_volume = general.processRECEvent(event_id, 0, midi.REC_GetValue)
	converted_volume = round((mix_slot_volume / c.midi_CC_max) * 100)

	if event.data1 == nihia.mixer.knobs[0][0]:
		handle_mixer_effect_mix(self, event, converted_volume, event_id)

def handle_mixer_effect_mix(self, event, converted_volume, event_id):
	"""Handles mix level adjustment."""
	volume_increment = config.increment * 100
	adjusted_increment = knob_time_check_mixer(self, volume_increment)

	if not NILA_core.seriesCheck():
		handle_non_series_knob_event(self, event, converted_volume, event_id, adjusted_increment)
	else:
		handle_series_knob_event(self, event, converted_volume, event_id, adjusted_increment)

def handle_non_series_knob_event(self, event, converted_volume, event_id, volume_increment):
	"""Handles mix level changes for non-series controllers."""
	if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED and converted_volume > 0:
		converted_volume -= volume_increment
	elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED and converted_volume < 100:
		converted_volume += volume_increment

	update_and_record_volume(self, event, event_id, converted_volume)

def handle_series_knob_event(self, event, converted_volume, event_id, volume_increment):
	"""Handles mix level changes for series controllers."""
	if 65 <= event.data2 < 95 or 96 <= event.data2 < 128:
		converted_volume = max(0, converted_volume - volume_increment)
	elif 0 <= event.data2 < 31 or 32 <= event.data2 < 64:
		converted_volume = min(100, converted_volume + volume_increment)

	update_and_record_volume(self, event, event_id, converted_volume)

def update_and_record_volume(self, event, event_id, converted_volume):
	"""Updates and records volume adjustments."""
	mix_slot_volume = round((converted_volume / 100) * c.midi_CC_max)
	mix_slot_volume = max(0, min(12800, mix_slot_volume))
	general.processRECEvent(event_id, mix_slot_volume, midi.REC_Control | midi.REC_UpdateValue | midi.REC_UpdateControl)
	NILA_OLED.OnRefresh(self, event)

def knob_time_check(self, adjusted_increment):
	"""Adjusts knob sensitivity based on interaction speed."""
	current_time = time.time()
	time_difference = current_time - getattr(self, 'last_signal_time', current_time)
	setattr(self, 'last_signal_time', current_time)
	return adjusted_increment * 1.5 if time_difference < c.speed_increase_wait else adjusted_increment

def knob_time_check_mixer(self, adjusted_increment):
	"""Adjusts knob sensitivity for mixer controls."""
	current_time = time.time()
	time_difference = current_time - getattr(self, 'last_signal_time_mixer', current_time)
	setattr(self, 'last_signal_time_mixer', current_time)
	return adjusted_increment * 1.5 if time_difference < 0.005 else adjusted_increment

def setGenPluginVolumePan(self, event):
	knob_speed = 0

	for control_type in (0, 1):  # 0 for volume, 1 for pan
		knob_data = nihia.mixer.knobs[control_type][0]
		current_channel = channels.selectedChannel() + 0
		current_value = (
			channels.getChannelVolume(current_channel) if control_type == 0
			else channels.getChannelPan(current_channel)
		)
		if event.data1 == knob_data:
			event.handled = True

			# Time-based adjustment
			current_time = time.time()
			time_difference = current_time - last_signal_time[0]
			last_signal_time[0] = current_time

			adjusted_increment = config.increment * c.knob_rotation_speed if time_difference <= c.speed_increase_wait else config.increment

			new_value = NILA_channel_rack.adjust_channel_value(current_value, event.data2, adjusted_increment, knob_speed)

			if control_type == 0:
				channels.setChannelVolume(current_channel, new_value)
			else:
				channels.setChannelPan(current_channel, new_value)
	
	#NILA_OLED.OnRefresh(self, event)