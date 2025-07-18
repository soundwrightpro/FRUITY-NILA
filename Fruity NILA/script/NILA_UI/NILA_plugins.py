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

last_volume_sent_time = {}
last_volume_sent_value = {}

def plugin(self, event):
	"""Handles plugin-related events and delegates control."""
	if ui.getFocused(c.winName["Plugin"]):
		if ui.getFocused(c.winName["Generator Plugin"]):
			channel_index = channels.selectedChannel() 
			if not plugins.isValid(channel_index, c.gen_plugin):
				setGenPluginVolumePan(self, event)
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

	if effect_info is None or effect_info == (c.plugin_effect_none, c.plugin_effect_none):
		return  # No effect is focused

	track_index, mixer_slot = effect_info
	full_plugin_name = plugins.getPluginName(track_index, mixer_slot)

	if full_plugin_name not in c.unsupported_plugins:
		c.param_offset = max(c.skip_over, 0)

		if c.actual_param_count <= 0:
			return  # No available parameters

		for knob_number in range(c.knob_offset, min(c.actual_param_count + c.knob_offset, c.max_knobs + c.param_offset)):
			param_index = max(min(knob_number - c.knob_offset + c.lead_param, c.actual_param_count - 1), 0)
			param_name = plugins.getParamName(param_index, track_index, mixer_slot, use_global_index)

			if not param_name:
				param_name = c.unnamed_param  # Fallback

			if param_name not in c.unsupported_param:
				knob_number_display = max(c.knob_offset, min(knob_number - c.skip_over, c.max_knob_number))
				knob_data = nihia.mixer.knobs[0][knob_number_display]
				volume_increment = config.mixer_increment

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

		for knob_number in range(c.knob_offset, min(param_count + c.knob_offset, c.max_knobs + c.param_offset)):
			param_index = max(min(knob_number - c.knob_offset + c.lead_param, param_count - 1), 0)
			param_name = plugins.getParamName(param_index, channel_index, c.gen_plugin, use_global_index)

			if not param_name:
				param_name = c.unnamed_param

			if param_name not in c.unsupported_param:
				knob_number_display = max(c.knob_offset, min(knob_number - c.skip_over, c.max_knob_number))
				knob_data = nihia.mixer.knobs[0][knob_number_display]
				volume_increment = config.channel_increment

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
		if c.encoder_cc_dec_slow_min <= event.data2 < c.encoder_cc_dec_fast_max:  # All decrement values
			new_param_value = max(param_value - volume_increment, c.plugin_param_min)
		elif c.encoder_cc_inc_fast_min <= event.data2 < c.encoder_cc_inc_slow_max:  # All increment values
			new_param_value = min(param_value + volume_increment, c.plugin_param_max)
	else:
		if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
			new_param_value = max(param_value - volume_increment, c.plugin_param_min)
		elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
			new_param_value = min(param_value + volume_increment, c.plugin_param_max)

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
	converted_volume = round((mix_slot_volume / c.mix_slot_volume_max) * c.volume_percent_max)

	if event.data1 == nihia.mixer.knobs[0][0]:
		handle_mixer_effect_mix(self, event, converted_volume, event_id)

def handle_mixer_effect_mix(self, event, converted_volume, event_id):
	"""Handles mix level adjustment."""
	volume_increment = config.mixer_increment * c.volume_percent_max
	adjusted_increment = knob_time_check_mixer(self, volume_increment)

	if not NILA_core.seriesCheck():
		handle_non_series_knob_event(self, event, converted_volume, event_id, adjusted_increment)
	else:
		handle_series_knob_event(self, event, converted_volume, event_id, adjusted_increment)

def handle_non_series_knob_event(self, event, converted_volume, event_id, volume_increment):
	"""Handles mix level changes for non-series controllers."""
	if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED and converted_volume > c.volume_percent_min:
		converted_volume -= volume_increment
	elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED and converted_volume < c.volume_percent_max:
		converted_volume += volume_increment

	update_and_record_volume(self, event, event_id, converted_volume)

def handle_series_knob_event(self, event, converted_volume, event_id, volume_increment):
	"""Handles mix level changes for series controllers."""
	if c.encoder_cc_dec_slow_min <= event.data2 < c.encoder_cc_dec_fast_max:
		converted_volume = max(c.volume_percent_min, converted_volume - volume_increment)
	elif c.encoder_cc_inc_fast_min <= event.data2 < c.encoder_cc_inc_slow_max:
		converted_volume = min(c.volume_percent_max, converted_volume + volume_increment)

	update_and_record_volume(self, event, event_id, converted_volume)

def update_and_record_volume(self, event, event_id, converted_volume):
	"""Smoothly updates and records volume adjustments with minimal UI overhead."""
	mix_slot_volume = round((converted_volume / c.volume_percent_max) * c.mix_slot_volume_max)
	mix_slot_volume = max(c.mix_slot_volume_min, min(c.mix_slot_volume_max, mix_slot_volume))

	now = time.time()
	last_time = last_volume_sent_time.get(event_id, 0)
	last_value = last_volume_sent_value.get(event_id, -1)

	if (now - last_time >= 0.015) or (mix_slot_volume != last_value):
		flags = (
			midi.REC_Control |
			midi.REC_Smoothed |
			midi.REC_InternalCtrl |
			midi.REC_NoSaveUndo
		)
		general.processRECEvent(event_id, mix_slot_volume, flags)
		last_volume_sent_time[event_id] = now
		last_volume_sent_value[event_id] = mix_slot_volume

		NILA_OLED.OnRefresh(self, event)

def knob_time_check(self, adjusted_increment):
	"""Gradually scales knob sensitivity based on how fast the knob is moved."""
	current_time = time.time()
	last_time = getattr(self, 'last_signal_time', current_time)
	setattr(self, 'last_signal_time', current_time)

	time_diff = current_time - last_time
	speed_factor = max(1.0, min(c.knob_sensitivity_speedup, 1.5 / (time_diff + 0.001)))

	return adjusted_increment * speed_factor

def knob_time_check_mixer(self, adjusted_increment):
	"""Gradually scales mixer knob sensitivity based on how fast the knob is moved."""
	current_time = time.time()
	last_time = getattr(self, 'last_signal_time_mixer', current_time)
	setattr(self, 'last_signal_time_mixer', current_time)

	time_diff = current_time - last_time
	speed_factor = max(1.0, min(c.knob_sensitivity_speedup, 1.5 / (time_diff + 0.001)))

	return adjusted_increment * speed_factor

def setGenPluginVolumePan(self, event):
	knob_speed = 0

	for control_type in (0, 1):  # 0 for volume, 1 for pan
		knob_data = nihia.mixer.knobs[control_type][0]
		current_channel = channels.selectedChannel()
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

			adjusted_increment = config.channel_increment * c.knob_rotation_speed if time_difference <= c.speed_increase_wait else config.channel_increment

			new_value = NILA_channel_rack.adjust_channel_value(current_value, event.data2, adjusted_increment, knob_speed)

			if control_type == 0:
				channels.setChannelVolume(current_channel, new_value)
			else:
				channels.setChannelPan(current_channel, new_value)
