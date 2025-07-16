from nihia import mixer as mix
from script.device_setup import NILA_core, constants as c, NILA_transform
import channels
import mixer
import plugins
import transport
import ui
import device
import math
import midi
import general



def get_utility_track():
	"""Returns the last track (Utility) dynamically."""
	return mixer.trackCount() - 1

def get_mixer_order():
	"""Get mixer tracks sorted by docked position & order of appearance."""
	track_count = mixer.trackCount() - 1
	tracks = [(mixer.getTrackDockSide(i), i) for i in range(track_count)]
	tracks.sort()
	return [t[1] for t in tracks]

def get_correct_tracks():
	"""Determines the correct tracks for knob control while skipping docked tracks."""
	tracks_order = get_mixer_order()
	current_track = mixer.trackNumber()
	start_idx = tracks_order.index(current_track) if current_track in tracks_order else 0

	selected_tracks = [current_track]
	for i in range(start_idx + 1, len(tracks_order)):
		track = tracks_order[i]
		if mixer.getTrackDockSide(track) != mixer.getTrackDockSide(current_track):
			break
		selected_tracks.append(track)
		if len(selected_tracks) == c.max_knobs:
			break

	while len(selected_tracks) < c.max_knobs and selected_tracks[-1] != tracks_order[-1]:
		next_idx = tracks_order.index(selected_tracks[-1]) + 1
		if next_idx < len(tracks_order):
			selected_tracks.append(tracks_order[next_idx])
		else:
			break

	return selected_tracks

def format_param_name(param_name):
	"""Inserts spaces for parameter names for OLED display (for series)."""
	formatted = ""
	for i, char in enumerate(param_name):
		if i > 0 and (
			(char.isnumeric() and param_name[i - 1].islower()) or
			(char.isupper() and param_name[i - 1].islower()) or
			(char.isupper() and param_name[i - 1].isnumeric())
		):
			formatted += " "
		formatted += char
	return formatted

def purge_all_tracks():
	purge_tracks(c.purge_start_index, c.max_knob_number, clear_info=True)
	purge_tracks(c.purge_start_index, c.max_knob_number)

def OnRefresh(self, event):
	"""Handles track updates based on the focused FL Studio window."""
	useGlobalIndex = False

	last_track_state = {}

	form_id = ui.getFocusedFormID()
	if form_id != c.last_form_id:
		purge_all_tracks()
		c.last_form_id = form_id



	if ui.getFocused(c.winName["Mixer"]):
		tracks_to_control = get_correct_tracks()
		for i in range(c.max_knobs):
			mix.setTrackSel(i, 0)

		for knobNumber, trackNumber in enumerate(tracks_to_control):
			track_id = f"{trackNumber}_{mixer.getTrackVolume(trackNumber)}"
			if last_track_state.get(knobNumber) != track_id:
				mix.setTrackExist(knobNumber, 1)
				mix.setTrackName(knobNumber, mixer.getTrackName(trackNumber))
				mix.setTrackVol(knobNumber, f"{NILA_transform.VolTodB(mixer.getTrackVolume(trackNumber))} dB")
				mix.setTrackVolGraph(knobNumber, mixer.getTrackVolume(trackNumber))
				NILA_transform.updatePanMix(trackNumber, knobNumber)
				last_track_state[knobNumber] = track_id


	elif ui.getFocused(c.winName["Channel Rack"]):
		sel_channel = channels.selectedChannel()
		ch_count = channels.channelCount()
		for knobNumber in range(c.max_knobs):
			selectedChannel = sel_channel + knobNumber
			if ch_count > knobNumber and selectedChannel < ch_count:
				mix.setTrackExist(knobNumber, 1)
				mix.setTrackName(knobNumber, channels.getChannelName(selectedChannel))
				mix.setTrackVol(knobNumber, f"{round(channels.getChannelVolume(selectedChannel, 1), 1)} dB")
				mix.setTrackVolGraph(knobNumber, channels.getChannelVolume(selectedChannel) / 1.0 * c.oled_vol_bar_scaling)
				NILA_transform.updatePanChannel(selectedChannel, knobNumber)
				mix.setTrackSel(c.display_track_index, 0)
			else:
				# clear/blank this knob!
				mix.setTrackExist(knobNumber, 0)
				mix.setTrackName(knobNumber, c.blankEvent)
				mix.setTrackVol(knobNumber, c.blankEvent)
				mix.setTrackVolGraph(knobNumber, 0)
				mix.setTrackPan(knobNumber, c.blankEvent)

	elif ui.getFocused(c.winName["Plugin"]):
		mix.setTrackVolGraph(c.display_track_index, 0)
		active_fx = mixer.getActiveEffectIndex()
		sel_channel = channels.selectedChannel()
		if not active_fx:
			mix.setTrackExist(c.display_track_index, 1)
			channel_type = channels.getChannelType(sel_channel)
			name_map = {
				c.CT_Sampler: "S",
				c.CT_Hybrid: "P",
				c.CT_GenPlug: "P",
				c.CT_Layer: "L",
				c.CT_AudioClip: "AC",
				c.CT_AutoClip: "Auto",
			}
			prefix = name_map.get(channel_type, "S")
			short_form_type = f"{prefix}| {channels.getChannelName(sel_channel)}"
			if not NILA_core.seriesCheck():
				short_form_type = short_form_type[:9]
			mix.setTrackName(c.display_track_index, short_form_type)
			mix.setTrackVol(c.display_track_index, f"{round(channels.getChannelVolume(sel_channel, 1), 1)} dB")
			mix.setTrackVolGraph(c.display_track_index, channels.getChannelVolume(sel_channel) / 1.0 * c.oled_vol_bar_scaling)
			NILA_transform.updatePanChannel(sel_channel, c.display_track_index)

			if ui.getFocused(c.winName["Generator Plugin"]):
				knobNumber = 0
				if channels.getChannelType(sel_channel) in (c.CT_Sampler, c.CT_Layer, c.CT_AudioClip, c.CT_AutoClip):
					# Use knob 0 to show and control channel volume
					purge_all_tracks() 
					mix.setTrackExist(knobNumber, 1)
					mix.setTrackVol(knobNumber, f"{round(channels.getChannelVolume(sel_channel, 1), 1)} dB")
					mix.setTrackVolGraph(knobNumber, channels.getChannelVolume(sel_channel) / 1.0 * c.oled_vol_bar_scaling)
					NILA_transform.updatePanChannel(sel_channel, knobNumber)
					mix.setTrackSel(c.display_track_index, 0)
					return

				if not plugins.isValid(sel_channel, c.gen_plugin):
					purge_all_tracks()
					return

				c.skip_over = 0
				plugin_id = plugins.getPluginName(sel_channel, c.gen_plugin)

				if plugin_id not in c.unsupported_plugins:
					param_count = plugins.getParamCount(sel_channel, c.gen_plugin, useGlobalIndex)
					if plugin_id != c.last_plugin_name:
						c.lead_param = 0
						c.last_plugin_name = plugin_id
					if param_count > 0:
						for knob_index in range(c.first_knob_index, min(param_count + c.knob_offset, c.max_knob_number)):
							param_index = max(min(knob_index - c.knob_offset + c.lead_param, param_count - 1), 0)
							param_name = plugins.getParamName(param_index, sel_channel, c.gen_plugin, useGlobalIndex)
							if param_name in c.unsupported_param:
								c.skip_over += 1
						actual_non_blank_param_count = 0
						if param_count == c.unused_param:
							for param_index in range(param_count):
								param_name = plugins.getParamName(param_index, sel_channel, c.gen_plugin, useGlobalIndex)
								if param_name:
									actual_non_blank_param_count += 1
							c.actual_param_count = actual_non_blank_param_count - c.unused_midi_cc
						else:
							c.actual_param_count = param_count


					c.param_offset = c.skip_over if c.skip_over > 0 else 0
					if c.actual_param_count > 0:
						for knob_index in range(c.first_knob_index, min(c.actual_param_count + c.knob_offset, c.max_knobs + c.param_offset)):
							param_index = max(min(knob_index - c.knob_offset + c.lead_param, c.actual_param_count - 1), 0)
							param_name = plugins.getParamName(param_index, sel_channel, c.gen_plugin, useGlobalIndex)
							if param_name not in c.unsupported_param:
								param_value = plugins.getParamValue(param_index, sel_channel, c.gen_plugin, useGlobalIndex)
								percentage = param_value * 100
								formatted_param_name = format_param_name(param_name) if NILA_core.seriesCheck() else param_name
								knob_display_idx = max(c.first_knob_index, knob_index - c.skip_over)
								mix.setTrackExist(knob_display_idx, 2)
								mix.setTrackSel(c.display_track_index, 1)
								mix.setTrackName(knob_display_idx, formatted_param_name)
								mix.setTrackVol(knob_display_idx, "{}%".format(int(percentage)))
								mix.setTrackVolGraph(knob_display_idx, 0)
					else:
						purge_all_tracks()
				else:
					purge_all_tracks()
		else:
			track_index, mixer_slot = active_fx
			full_plugin_name = plugins.getPluginName(track_index, mixer_slot)
			if "Fruity" in full_plugin_name:
				full_plugin_name = full_plugin_name.replace("Fruity ", "")
			plugin_name = (full_plugin_name[:9] if not NILA_core.seriesCheck() else full_plugin_name + "\n\n|Mix Level") \
				if device.getName() == "Komplete Kontrol DAW - 1" else f"P| Insert: {track_index}"
			track_plugin_id = mixer.getTrackPluginId(track_index, mixer_slot)
			event_id = midi.REC_Plug_MixLevel + track_plugin_id
			effect_mix_level = general.processRECEvent(event_id, 0, midi.REC_Chan_FXTrack | midi.REC_GetValue)
			converted_mix_level = round((effect_mix_level / c.mix_slot_volume_max) * 100)
			mix.setTrackExist(c.display_track_index, 1)
			mix.setTrackName(c.display_track_index, plugin_name)
			mix.setTrackVol(c.display_track_index, "{}%".format(int(converted_mix_level)))
			
			if ui.getFocused(c.winName["Effect Plugin"]):
				c.skip_over = 0
				if full_plugin_name not in c.unsupported_plugins:
					param_count = plugins.getParamCount(track_index, mixer_slot, useGlobalIndex)
					track_plugin_id = mixer.getTrackPluginId(track_index, mixer_slot)
					if track_plugin_id != c.last_plugin_name:
						c.lead_param = 0
						c.last_plugin_name = track_plugin_id
					if param_count > 0:
						for knob_index in range(c.first_knob_index, min(param_count + c.knob_offset, c.max_knob_number)):
							param_index = max(min(knob_index - c.knob_offset + c.lead_param, param_count - 1), 0)
							param_name = plugins.getParamName(param_index, track_index, mixer_slot, useGlobalIndex)
							if param_name in c.unsupported_param:
								c.skip_over += 1
						actual_non_blank_param_count = 0
						if param_count == c.unused_param:
							for param_index in range(param_count):
								param_name = plugins.getParamName(param_index, track_index, mixer_slot, useGlobalIndex)
								if param_name:
									actual_non_blank_param_count += 1
							c.actual_param_count = actual_non_blank_param_count - c.unused_midi_cc
						else:
							c.actual_param_count = param_count
					for knob_index in range(c.actual_param_count, c.max_knobs):
						if c.actual_param_count < c.max_knob_number:
							purge_all_tracks()
					c.param_offset = c.skip_over if c.skip_over > 0 else 0
					if c.actual_param_count > 0:
						for knob_index in range(c.first_knob_index, min(c.actual_param_count + c.knob_offset, c.max_knobs + c.param_offset)):
							param_index = max(min(knob_index - c.knob_offset + c.lead_param, c.actual_param_count - 1), 0)
							param_name = plugins.getParamName(param_index, track_index, mixer_slot, useGlobalIndex)
							if param_name not in c.unsupported_param:
								param_value = plugins.getParamValue(param_index, track_index, mixer_slot, useGlobalIndex)
								percentage = param_value * 100
								formatted_param_name = format_param_name(param_name) if NILA_core.seriesCheck() else param_name
								knob_display_idx = max(c.first_knob_index, knob_index - c.skip_over)
								mix.setTrackExist(knob_display_idx, 2)
								mix.setTrackSel(c.display_track_index, 1)
								mix.setTrackName(knob_display_idx, formatted_param_name)
								mix.setTrackVol(knob_display_idx, "{}%".format(int(percentage)))
								mix.setTrackVolGraph(knob_display_idx, 0)
					else:
						purge_all_tracks()
				else:
					purge_all_tracks()

	elif ui.getFocused(c.winName["Piano Roll"]):
		purge_all_tracks()
		sel_channel = channels.selectedChannel()
		mix.setTrackName(c.display_track_index, str(channels.getChannelName(sel_channel)))
		NILA_core.setTrackVolConvert(c.display_track_index, f"{round(channels.getChannelVolume(sel_channel, 1), 1)} dB")
		NILA_transform.updatePanChannel(sel_channel, c.display_track_index)

	elif ui.getFocused(c.winName["Playlist"]):
		mix.setTrackName(c.display_track_index, "Playlist")
		mix.setTrackVolGraph(c.display_track_index, mixer.getTrackVolume(c.display_track_index))

def OnUpdateBeatIndicator(self, Value):
	"""Updates the beat indicator based on the focused window (e.g., Playlist)."""
	if ui.getFocused(c.winName["Playlist"]):
		timeDisp, currentTime = NILA_core.timeConvert(c.itemDisp, c.itemTime)
		mix.setTrackName(c.display_track_index, "Playlist")
		split_message = ui.getHintMsg()
		split_point1 = ' - '
		split_point2 = ' to '
		split_hint = split_message.partition(split_point1)[2] if split_point1 in split_message.lower() else split_message.partition(split_point2)[2]
		if device.getName() == "Komplete Kontrol DAW - 1":
			mix.setTrackVol(c.display_track_index, f"|{currentTime}")
		else:
			if transport.isPlaying():
				if timeDisp == "Beats:Bar":
					displayLabel = "B:B" if len(currentTime) >= 5 else "Beats:Bar"
				elif timeDisp == "Min:Sec":
					displayLabel = "M:S" if len(currentTime) > 5 else "Min:Sec"
				else:
					displayLabel = timeDisp
				mix.setTrackVol(c.display_track_index, f"{displayLabel}|{currentTime}")
			else:
				mix.setTrackVol(c.display_track_index, f"{split_hint[:7]}|{currentTime}")
				mix.setTrackVolGraph(c.display_track_index, mixer.getTrackVolume(c.display_track_index))

def OnIdle(self):
	"""Performs idle tasks based on the currently focused window."""
	if ui.getFocused(c.winName["Playlist"]):
		purge_all_tracks()
		mix.setTrackVolGraph(c.display_track_index, mixer.getTrackVolume(c.display_track_index))
		timeDisp, currentTime = NILA_core.timeConvert(c.itemDisp, c.itemTime)
		split_message = ui.getHintMsg()
		split_hint = split_message.partition(' - ')[2] if ' - ' in split_message else split_message.partition(' to ')[2]
		mix.setTrackName(c.display_track_index, "Playlist")
		if not transport.isPlaying() and "Volume" not in split_hint[:7]:
			mix.setTrackVol(c.display_track_index, f"{split_hint[:7]}|{currentTime}")

	elif ui.getFocused(c.winName["Browser"]):
		file_type = ui.getFocusedNodeFileType()
		purge_all_tracks()
		if file_type <= -100:
			file_type = "Browser"
		else:
			for key, value in c.FL_node.items():
				file_type = key if ui.getFocusedNodeFileType() == value else file_type
		mix.setTrackName(c.display_track_index, str(file_type))
		mix.setTrackVol(c.display_track_index, ui.getFocusedNodeCaption()[:15])

def purge_tracks(start, end, clear_info=False):
	for track_index in range(start, end + 1):
		if clear_info:
			mix.setTrackPanGraph(track_index, 0)
			mix.setTrackVolGraph(track_index, 0)
			mix.setTrackSel(track_index, 0)
			mix.setTrackArm(track_index, 0)
			mix.setTrackSolo(track_index, 0)
			mix.setTrackMute(track_index, 0)
			mix.setTrackName(track_index, c.blankEvent)
			mix.setTrackPan(track_index, c.blankEvent)
			mix.setTrackVol(track_index, c.blankEvent)
		else:
			mix.setTrackExist(track_index, 0)
