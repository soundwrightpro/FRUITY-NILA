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
	""" Returns the last track (Utility) dynamically. """
	return mixer.trackCount() - 1

def get_mixer_order():
	""" Get mixer tracks sorted by docked position & order of appearance. """
	track_count = mixer.trackCount() - 1
	tracks = []

	for i in range(0, track_count):
		dock_side = mixer.getTrackDockSide(i)
		tracks.append((dock_side, i))

	tracks.sort()
	return [t[1] for t in tracks]

def get_correct_tracks():
	""" Determines the correct 8 tracks for knob control while skipping docked tracks. """
	tracks_order = get_mixer_order()
	current_track = mixer.trackNumber()

	if current_track in tracks_order:
		start_idx = tracks_order.index(current_track)
	else:
		start_idx = 0

	selected_tracks = [current_track]
	for i in range(start_idx + 1, len(tracks_order)):
		track = tracks_order[i]
		if mixer.getTrackDockSide(track) != mixer.getTrackDockSide(current_track):
			break
		selected_tracks.append(track)
		if len(selected_tracks) == 8:
			break

	while len(selected_tracks) < 8 and selected_tracks[-1] != tracks_order[-1]:
		next_idx = tracks_order.index(selected_tracks[-1]) + 1
		if next_idx < len(tracks_order):
			selected_tracks.append(tracks_order[next_idx])
		else:
			break

	return selected_tracks

def OnRefresh(self, event):
	""" Handles track updates based on the focused FL Studio window. """
	useGlobalIndex = False

	if ui.getFocused(c.winName["Mixer"]):
		tracks_to_control = get_correct_tracks()

		# First, deselect ALL tracks before setting Track 0
		for i in range(8):
			mix.setTrackSel(i, 0)  # Ensures previous selections are cleared

		for knobNumber, trackNumber in enumerate(tracks_to_control):
			mix.setTrackExist(knobNumber, 1)
			mix.setTrackName(knobNumber, mixer.getTrackName(trackNumber))
			mix.setTrackVol(knobNumber, f"{NILA_transform.VolTodB(mixer.getTrackVolume(trackNumber))} dB")
			mix.setTrackVolGraph(knobNumber, mixer.getTrackVolume(trackNumber))
			NILA_transform.updatePanMix(trackNumber, knobNumber)

			# Ensure ONLY Track 0 is highlighted
			if trackNumber == 0:
				mix.setTrackSel(knobNumber, 1)
			else:
				mix.setTrackSel(knobNumber, 0)  # Explicitly clear others

		purge_tracks(len(tracks_to_control), 7)

	if ui.getFocused(c.winName["Channel Rack"]):
		for knobNumber in range(8):
			selectedChannel = channels.selectedChannel() + knobNumber
			if channels.channelCount() > knobNumber and selectedChannel < channels.channelCount():
				mix.setTrackExist(knobNumber, 1)
				mix.setTrackName(knobNumber, channels.getChannelName(selectedChannel))
				mix.setTrackVol(knobNumber, f"{round(channels.getChannelVolume(selectedChannel, 1), 1)} dB")
				mix.setTrackVolGraph(knobNumber, channels.getChannelVolume(selectedChannel) / 1.0 * 0.86)
				NILA_transform.updatePanChannel(selectedChannel, knobNumber)
				mix.setTrackSel(0, 0)
			else:
				mix.setTrackExist(knobNumber, 0)  
	
	if ui.getFocused(c.winName["Plugin"]):
		mix.setTrackVolGraph(0, 0)

		if not mixer.getActiveEffectIndex():
			purge_tracks(1, 7, clear_info=True)
			purge_tracks(1, 7)
			mix.setTrackExist(0, 1)
						
			# Get the channel type
			channel_type = channels.getChannelType(channels.selectedChannel())

			# Print the channel type detected
			if channel_type == c.CT_Sampler:
				short_form_type = f"S| {channels.getChannelName(channels.selectedChannel())}"
			elif channel_type == c.CT_Hybrid:
				short_form_type = f"P| {channels.getChannelName(channels.selectedChannel())}"
			elif channel_type == c.CT_GenPlug:
				short_form_type = f"P| {channels.getChannelName(channels.selectedChannel())}"
			elif channel_type == c.CT_Layer:
				short_form_type = f"L| {channels.getChannelName(channels.selectedChannel())}"
			elif channel_type == c.CT_AudioClip:
				short_form_type = f"AC| {channels.getChannelName(channels.selectedChannel())}"
			elif channel_type == c.CT_AutoClip:
				short_form_type = f"Auto| {channels.getChannelName(channels.selectedChannel())}"
			else:
				short_form_type = f"S| {channels.getChannelName(channels.selectedChannel())}"
				
			if not NILA_core.seriesCheck():    
				short_form_type = short_form_type[:9]
			else:
				short_form_type = short_form_type

			mix.setTrackName(0, f"{short_form_type}")
			mix.setTrackVol(0, f"{round(channels.getChannelVolume(channels.selectedChannel(), 1), 1)} dB")
			mix.setTrackVolGraph(0, channels.getChannelVolume(channels.selectedChannel()) / 1.0 * 0.86)
			NILA_transform.updatePanChannel(channels.selectedChannel(), 0)
			mix.setTrackSel(0, 0)


			if ui.getFocused(c.winName["Generator Plugin"]):
				selected_channel = channels.selectedChannel()
				if channels.getChannelType(channels.selectedChannel()) in (0, 3, 4, 5):
					return

				if not plugins.isValid(selected_channel, c.gen_plugin):
					purge_tracks(1, 7)
					purge_tracks(1, 7, clear_info=True)
					return

				c.skip_over = 0
				
				plugin_id = plugins.getPluginName(selected_channel, c.gen_plugin)

				if plugin_id not in c.unsupported_plugins:
					param_count = plugins.getParamCount(selected_channel, c.gen_plugin, useGlobalIndex)

					if plugin_id != c.last_plugin_name:
						c.lead_param = 0
						c.last_plugin_name = plugin_id

					if param_count > 0:
						for knob_index in range(1, min(param_count + c.knob_offset, 7)):
							param_index = max(min(knob_index - c.knob_offset + c.lead_param, param_count - 1), 0)
							param_name = plugins.getParamName(param_index, selected_channel, c.gen_plugin, useGlobalIndex)

							if param_name in c.unsupported_param:
								c.skip_over += 1

						actual_non_blank_param_count = 0

						if param_count == c.unused_param:
							for param_index in range(param_count):
								param_name = plugins.getParamName(param_index, selected_channel, c.gen_plugin, useGlobalIndex)

								if param_name != "":
									actual_non_blank_param_count += 1

							c.actual_param_count = actual_non_blank_param_count - c.unused_midi_cc
						else:
							c.actual_param_count = param_count

					# If there are fewer parameters than knobs, set remaining knobs to non-existent
					for knob_index in range(c.actual_param_count, 8):
						if c.actual_param_count < 7:
							purge_tracks(c.actual_param_count, 7)
							purge_tracks(c.actual_param_count, 7, clear_info=True)

					c.param_offset = c.skip_over if c.skip_over > 0 else 0

					if c.actual_param_count > 0:
						for knob_index in range(1, min(c.actual_param_count + c.knob_offset, 8 + c.param_offset)):
							param_index = max(min(knob_index - c.knob_offset + c.lead_param, c.actual_param_count - 1), 0)
							param_name = plugins.getParamName(param_index, selected_channel, c.gen_plugin, useGlobalIndex)

							if param_name not in c.unsupported_param:
								param_value = plugins.getParamValue(param_index, selected_channel, c.gen_plugin, useGlobalIndex)
								percentage = param_value * 100

								if not NILA_core.seriesCheck():
									formatted_param_name = param_name
								else:
									formatted_param_name = ""

									for i, char in enumerate(param_name):
										if i > 0 and (
											(char.isnumeric() and param_name[i - 1].islower()) or
											(char.isupper() and param_name[i - 1].islower()) or
											(char.isupper() and param_name[i - 1].isnumeric())
										):
											formatted_param_name += " "
										formatted_param_name += char

								knob_index = max(1, knob_index - c.skip_over)

								mix.setTrackExist(knob_index, 2)
								mix.setTrackSel(0, 1)
								mix.setTrackName(knob_index, formatted_param_name)
								mix.setTrackVol(knob_index, "{}%".format(int(percentage)))
								mix.setTrackVolGraph(knob_index, 0)
					else:
						purge_tracks(1, 7)
						purge_tracks(1, 7, clear_info=True)
				else:
					purge_tracks(1, 7)
					purge_tracks(1, 7, clear_info=True)

					
		else:
			if device.getName() == "Komplete Kontrol DAW - 1":
				track_index, mixer_slot = mixer.getActiveEffectIndex()
				full_plugin_name = plugins.getPluginName(track_index, mixer_slot)
				
				if "Fruity" in full_plugin_name:
					# Remove the word "Fruity"
					full_plugin_name = full_plugin_name.replace("Fruity ", "")
				 
				if not NILA_core.seriesCheck():    
					plugin_name = full_plugin_name[:9]
				else:
					plugin_name = full_plugin_name + "\n\n|Mix Level"
					
				track_index, mixer_slot = mixer.getActiveEffectIndex()
				track_plugin_id = mixer.getTrackPluginId(track_index, mixer_slot)
				event_id = midi.REC_Plug_MixLevel + track_plugin_id
				
				
				effect_mix_level = general.processRECEvent(event_id, 0, midi.REC_Chan_FXTrack | midi.REC_GetValue)
				converted_mix_level = round((effect_mix_level / c.midi_CC_max) * 100)
					
				mix.setTrackExist(0, 1)
				mix.setTrackName(0, plugin_name)
				mix.setTrackVol(0, "{}%".format(int(converted_mix_level)))
				
			else:
				track_index, mixer_slot = mixer.getActiveEffectIndex()
				full_plugin_name = plugins.getPluginName(track_index, mixer_slot)
				
				if "Fruity" in full_plugin_name:
					# Remove the word "Fruity"
					full_plugin_name = full_plugin_name.replace("Fruity ", "")
					
				mix.setTrackExist(0, 1)
				mix.setTrackName(0, f"P| Insert: {track_index}")
				mix.setTrackVol(0, full_plugin_name)
				
					
			if ui.getFocused(c.winName["Effect Plugin"]):
				c.skip_over = 0
				full_plugin_name = plugins.getPluginName(track_index, mixer_slot)

				if full_plugin_name not in c.unsupported_plugins:
					mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
					track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
					param_count = plugins.getParamCount(mix_track_index, mixer_slot, useGlobalIndex)

					if track_plugin_id != c.last_plugin_name:
						c.lead_param = 0
						c.last_plugin_name = track_plugin_id

					if param_count > 0:
						for knob_index in range(1, min(param_count + c.knob_offset, 7)):
							param_index = max(min(knob_index - c.knob_offset + c.lead_param, param_count - 1), 0)
							param_name = plugins.getParamName(param_index, mix_track_index, mixer_slot, useGlobalIndex)

							if param_name in c.unsupported_param:
								c.skip_over += 1
								
						actual_non_blank_param_count = 0

						if param_count == c.unused_param:
							for param_index in range(param_count):
								param_name = plugins.getParamName(param_index, mix_track_index, mixer_slot, useGlobalIndex)

								if param_name != "":
									actual_non_blank_param_count += 1

							c.actual_param_count = actual_non_blank_param_count - c.unused_midi_cc
						else:
							c.actual_param_count = param_count

					# If there are fewer parameters than knobs, set remaining knobs to non-existent
					for knob_index in range(c.actual_param_count, 8):
						if c.actual_param_count < 7:
							purge_tracks(c.actual_param_count, 7)
							purge_tracks(c.actual_param_count, 7, clear_info=True)

					c.param_offset = c.skip_over if c.skip_over > 0 else 0

					if c.actual_param_count  > 0:
						for knob_index in range(1, min(c.actual_param_count + c.knob_offset, 8 + c.param_offset)):
							
							param_index = max(min(knob_index - c.knob_offset + c.lead_param, c.actual_param_count  - 1), 0)
							param_name = plugins.getParamName(param_index, mix_track_index, mixer_slot, useGlobalIndex)

							if param_name not in c.unsupported_param:
								param_value = plugins.getParamValue(param_index, mix_track_index, mixer_slot, useGlobalIndex)
								percentage = param_value * 100

								if not NILA_core.seriesCheck():
									formatted_param_name = param_name
								else:
									formatted_param_name = ""

									for i, char in enumerate(param_name):
										if i > 0 and (
											(char.isnumeric() and param_name[i - 1].islower()) or
											(char.isupper() and param_name[i - 1].islower()) or
											(char.isupper() and param_name[i - 1].isnumeric())
										):
											formatted_param_name += " "  # Insert space
										formatted_param_name += char

								knob_index = max(1, knob_index - c.skip_over)

								mix.setTrackExist(knob_index, 2)
								mix.setTrackSel(0, 1)
								mix.setTrackName(knob_index, formatted_param_name)
								mix.setTrackVol(knob_index, "{}%".format(int(percentage)))
								mix.setTrackVolGraph(knob_index, 0)

					else:
						purge_tracks(1, 7)
						purge_tracks(1, 7, clear_info=True)
				else:
					purge_tracks(1, 7)
					purge_tracks(1, 7, clear_info=True)
			

	if ui.getFocused(c.winName["Piano Roll"]):
		purge_tracks(1, 7)
		purge_tracks(1, 7, clear_info=True)
		mix.setTrackName(0, str(channels.getChannelName(channels.selectedChannel())))
		NILA_core.setTrackVolConvert(0, f"{round(channels.getChannelVolume(channels.selectedChannel(), 1), 1)} dB")
		NILA_transform.updatePanChannel(channels.selectedChannel(), 0)

	if ui.getFocused(c.winName["Playlist"]):
		mix.setTrackName(0, "Playlist")
		mix.setTrackVolGraph(0, mixer.getTrackVolume(0))

def OnUpdateBeatIndicator(self, Value):
	"""
	Updates the beat indicator based on the focused window (e.g., Playlist).
	"""
	if ui.getFocused(c.winName["Playlist"]):
		timeDisp, currentTime = NILA_core.timeConvert(c.itemDisp, c.itemTime)
		mix.setTrackName(0, "Playlist")

		split_message = ui.getHintMsg()
		split_point1 = ' - '
		split_point2 = ' to '
		split_hint = split_message.partition(split_point1)[2] if split_point1 in split_message.lower() else split_message.partition(split_point2)[2]

		if device.getName() == "Komplete Kontrol DAW - 1":
			mix.setTrackVol(0, f"|{currentTime}")
		else:
			if transport.isPlaying():
				if timeDisp == "Beats:Bar":
					displayLabel = "B:B" if len(currentTime) >= 5 else "Beats:Bar"
				elif timeDisp == "Min:Sec":
					displayLabel = "M:S" if len(currentTime) > 5 else "Min:Sec"
				else:
					displayLabel = timeDisp  # fallback for other formats

				mix.setTrackVol(0, f"{displayLabel}|{currentTime}")
			else:
				mix.setTrackVol(0, f"{split_hint[:7]}|{currentTime}")
				mix.setTrackVolGraph(0, mixer.getTrackVolume(0))

			
def OnIdle(self):
	""" Performs idle tasks based on the currently focused window. """
	if ui.getFocused(c.winName["Playlist"]):
		purge_tracks(1, 7, clear_info=True)
		purge_tracks(1, 7)
		mix.setTrackVolGraph(0, mixer.getTrackVolume(0))
		timeDisp, currentTime = NILA_core.timeConvert(c.itemDisp, c.itemTime)
		split_message = ui.getHintMsg()
		split_hint = split_message.partition(' - ')[2] if ' - ' in split_message else split_message.partition(' to ')[2]

		mix.setTrackName(0, "Playlist")
		if not transport.isPlaying() and "Volume" not in split_hint[:7]:
			mix.setTrackVol(0, f"{split_hint[:7]}|{currentTime}")

	if ui.getFocused(c.winName["Browser"]):
		file_type = ui.getFocusedNodeFileType()
		purge_tracks(1, 7)

		if file_type <= -100:
			file_type = "Browser"
		else:
			for key, value in c.FL_node.items():
				file_type = key if ui.getFocusedNodeFileType() == value else file_type

		mix.setTrackName(0, str(file_type))
		mix.setTrackVol(0, ui.getFocusedNodeCaption()[:15])

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