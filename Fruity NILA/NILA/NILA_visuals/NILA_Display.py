import os
import time

import device
import channels
import mixer
import plugins
import transport
import midi
import general
import ui

from nihia import mixer as mix

from NILA.NILA_engine import NILA_core, NILA_transform, constants as c

# Persist across refresh calls so we can detect when a slot really changed
last_track_state = {}

focus_overlay_text = None
focus_overlay_started = 0.0
FOCUS_OVERLAY_DURATION = 0.6


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
	if current_track not in tracks_order:
		return []
	start_idx = tracks_order.index(current_track)

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
	"""Inserts spaces for parameter names for display (for series)."""
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
	last_track_state.clear()
	purge_tracks(c.purge_start_index, c.max_knob_number, clear_info=True)
	purge_tracks(c.purge_start_index, c.max_knob_number)


# Helper to clear a display slot

def clear_display_slot(knobNumber, clear_controls=True):
	"""Clear a display slot without changing behavior elsewhere."""
	mix.setTrackExist(knobNumber, 0)
	mix.setTrackName(knobNumber, c.blankEvent)
	mix.setTrackVol(knobNumber, c.blankEvent)
	mix.setTrackVolGraph(knobNumber, 0)
	mix.setTrackPan(knobNumber, c.blankEvent)
	if clear_controls:
		mix.setTrackPanGraph(knobNumber, 0)
		mix.setTrackSel(knobNumber, False)
		mix.setTrackArm(knobNumber, False)
		mix.setTrackSolo(knobNumber, False)
		mix.setTrackMute(knobNumber, False)



# --- Helper functions for S Series Browser path display ---
def truncate_display_text(text, limit=8):
	"""Return text shortened for one S Series display slot."""
	clean_text = str(text or c.blankEvent).strip()
	return clean_text[:limit] if clean_text else c.blankEvent


# --- Smart truncate for S Series 4-slot (32 char) display ---
def smart_truncate_32(text):
	"""Keep start and end with separator to fit 32 chars across 4 slots."""
	s = str(text or c.blankEvent).strip()
	if len(s) <= 32:
		return s
	# 14 + 1 + 17 = 32
	head = s[:14]
	tail = s[-17:]
	return f"{head}/{tail}"


# --- Helper for splitting text into display slots, preserving words where possible ---
def split_text_for_display_slots(text, slot_count=4, slot_width=8):
	"""Split text into display slots while preserving whole words when possible."""
	s = smart_truncate_32(text)
	words = s.split()
	chunks = []
	current = ""

	for word in words:
		while len(word) > slot_width:
			if current:
				chunks.append(current)
				current = ""
			chunks.append(word[:slot_width])
			word = word[slot_width:]

		if not word:
			continue

		if not current:
			current = word
		elif len(current) + 1 + len(word) <= slot_width:
			current = f"{current} {word}"
		else:
			chunks.append(current)
			current = word

	if current:
		chunks.append(current)

	return chunks[:slot_count]


# --- Helper for temporary focus overlay on display ---
def show_temporary_focus_message(text):
	"""Temporarily show focused window text on the display."""
	global focus_overlay_text
	global focus_overlay_started

	focus_overlay_text = str(text or c.blankEvent).strip()
	focus_overlay_started = time.time()


def focus_overlay_is_active():
	"""Return True while the temporary focus overlay should remain visible."""
	global focus_overlay_text
	global focus_overlay_started

	if not focus_overlay_text:
		return False

	if time.time() - focus_overlay_started <= FOCUS_OVERLAY_DURATION:
		return True

	focus_overlay_text = None
	focus_overlay_started = 0.0
	return False


def write_focus_overlay():
	"""Write the temporary focus overlay to the controller display."""
	display_text = str(focus_overlay_text or c.blankEvent)

	if NILA_core.seriesCheck():
		for i in range(c.max_knobs):
			mix.setTrackExist(i, 1 if i < 2 else 0)
			mix.setTrackName(i, c.blankEvent)
			mix.setTrackVol(i, c.blankEvent)
			mix.setTrackVolGraph(i, 0)
			mix.setTrackPan(i, c.blankEvent)
			mix.setTrackPanGraph(i, 0)
			mix.setTrackSel(i, False)
			mix.setTrackArm(i, False)
			mix.setTrackSolo(i, False)
			mix.setTrackMute(i, False)

		mix.setTrackName(0, "Focus:")
		mix.setTrackName(1, display_text)
	else:
		mix.setTrackExist(c.display_track_index, 1)
		mix.setTrackName(c.display_track_index, "Focus")
		mix.setTrackVol(c.display_track_index, display_text)
		mix.setTrackVolGraph(c.display_track_index, 0)


# --- Map file type to DAW-style descriptions ---
def map_file_type(filename, file_type_id):
	"""Return DAW-style descriptive type."""
	name = str(filename or "")
	ext = os.path.splitext(name)[1].lower()

	# Folder
	if file_type_id <= -100 or ext == "":
		return "Folder"

	# Audio
	if ext in (".wav", ".mp3", ".flac", ".aiff", ".ogg", ".wv"):
		return "Audio Clip"

	# MIDI
	if ext in (".mid", ".midi"):
		return "MIDI Sequence"

	# Projects
	if ext in (".flp", ".zip"):
		return "FL Project"

	# Presets
	if "preset" in name.lower():
		return "Plugin Preset"

	return "File"



def write_series_playlist_time(time_disp, current_time, marker_name=None):
	"""Display Playlist time in fixed S Series slots.

	Track 0 = Minutes or Beats
	Track 1 = Seconds or Bars
	Track 2 = current time
	Track 3 = marker name, only while playing and when available
	"""
	if time_disp == "Beats:Bar":
		values = ("Beats|", "Bars:", str(current_time), c.blankEvent)
	elif time_disp == "Min:Sec":
		values = ("Minutes|", "Seconds:", str(current_time), c.blankEvent)
	else:
		values = (str(time_disp)[:8], c.blankEvent, str(current_time), c.blankEvent)

	if transport.isPlaying():
		try:
			bpm = round(mixer.getCurrentTempo() / 1000)
			bpm_text = f"bpm {bpm}"
			values = (values[0], values[1], values[2], truncate_display_text(bpm_text))
		except Exception as e:
			print(f"Playlist BPM display error: {e}")
	elif marker_name:
		values = (values[0], values[1], values[2], truncate_display_text(marker_name))

	for i in range(c.max_knobs):
		mix.setTrackExist(i, 1 if i < 4 else 0)
		mix.setTrackName(i, c.blankEvent)
		mix.setTrackVol(i, c.blankEvent)
		mix.setTrackVolGraph(i, 0)
		mix.setTrackPan(i, c.blankEvent)
		mix.setTrackPanGraph(i, 0)
		mix.setTrackSel(i, False)
		mix.setTrackArm(i, False)
		mix.setTrackSolo(i, False)
		mix.setTrackMute(i, False)

	mix.setTrackName(0, "Playlist:")
	mix.setTrackName(1, f"{values[0]} {values[1]}")
	mix.setTrackName(2, values[2])
	mix.setTrackName(3, values[3])
	mix.setTrackVol(0, c.blankEvent)
	mix.setTrackVol(1, c.blankEvent)
	mix.setTrackVol(2, c.blankEvent)
	mix.setTrackVol(3, c.blankEvent)
	mix.setTrackVolGraph(0, 0)
	mix.setTrackVolGraph(1, 0)
	mix.setTrackVolGraph(2, 0)
	mix.setTrackVolGraph(3, 0)

	for i in range(4, c.max_knobs):
		clear_display_slot(i)



def get_playlist_marker_hint(split_hint):
	"""Extract marker names only from Playlist scrubbing hints."""
	hint = str(split_hint or "").strip()
	if not hint:
		return None

	if " - " in hint:
		marker = hint.partition(" - ")[2].strip()
	elif " to " in hint:
		marker = hint.partition(" to ")[2].strip()
	else:
		return None

	if not marker:
		return None

	lower_marker = marker.lower()
	if lower_marker.startswith("volume"):
		return None
	if lower_marker.startswith("track"):
		return None
	if marker in ("Playlist", c.blankEvent):
		return None
	if marker.replace(":", "").isdigit() and ":" in marker:
		return None

	return marker


# --- Helper to refresh Mixer display slots ---
def refresh_mixer_display():
	"""Refresh Mixer display slots immediately while Mixer is focused."""
	tracks_to_control = get_correct_tracks()
	for i in range(c.max_knobs):
		mix.setTrackSel(i, False)

	for knobNumber, trackNumber in enumerate(tracks_to_control):
		mix.setTrackExist(knobNumber, 1)
		mix.setTrackName(knobNumber, mixer.getTrackName(trackNumber))
		NILA_transform.setTrackVolFromMixer(knobNumber, trackNumber)
		NILA_transform.setTrackVolGraphFromMixer(knobNumber, trackNumber)
		NILA_transform.updatePanMix(trackNumber, knobNumber)
		last_track_state[knobNumber] = f"{trackNumber}_{round(mixer.getTrackVolume(trackNumber, 1), 1)}_{mixer.getTrackPan(trackNumber)}"

	# Blank any remaining slots so old names do not stick at the end.
	for knobNumber in range(len(tracks_to_control), c.max_knobs):
		clear_display_slot(knobNumber)
		if knobNumber in last_track_state:
			del last_track_state[knobNumber]


# --- Helper to refresh Channel Rack display slots ---
def refresh_channel_rack_display():
	"""Refresh Channel Rack display slots immediately while Channel Rack is focused."""
	sel_channel = channels.selectedChannel()
	ch_count = channels.channelCount()

	for knobNumber in range(c.max_knobs):
		selectedChannel = sel_channel + knobNumber
		if ch_count > knobNumber and selectedChannel < ch_count:
			mix.setTrackExist(knobNumber, 1)
			mix.setTrackName(knobNumber, channels.getChannelName(selectedChannel))
			NILA_transform.setTrackVolFromChannel(knobNumber, selectedChannel)
			NILA_transform.setTrackVolGraphFromChannel(knobNumber, selectedChannel)
			NILA_transform.updatePanChannel(selectedChannel, knobNumber)
			mix.setTrackSel(c.display_track_index, False)
		else:
			clear_display_slot(knobNumber, clear_controls=False)


def OnRefresh(self, event):
	"""Handles track updates based on the focused FL Studio window."""
	if focus_overlay_is_active():
		write_focus_overlay()
		return

	useGlobalIndex = False

	form_id = ui.getFocusedFormID()
	if form_id != c.last_form_id:
		purge_all_tracks()
		c.last_form_id = form_id

	if ui.getFocused(c.winName["Mixer"]):
		refresh_mixer_display()

	elif ui.getFocused(c.winName["Channel Rack"]):
		refresh_channel_rack_display()

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
			NILA_transform.setTrackVolFromChannel(c.display_track_index, sel_channel)
			NILA_transform.setTrackVolGraphFromChannel(c.display_track_index, sel_channel)
			NILA_transform.updatePanChannel(sel_channel, c.display_track_index)

			if ui.getFocused(c.winName["Generator Plugin"]):
				knobNumber = 0
				if channels.getChannelType(sel_channel) in (c.CT_Sampler, c.CT_Layer, c.CT_AudioClip, c.CT_AutoClip):
					# Use knob 0 to show and control channel volume
					purge_all_tracks() 
					mix.setTrackExist(knobNumber, 1)
					NILA_transform.setTrackVolFromChannel(knobNumber, sel_channel)
					NILA_transform.setTrackVolGraphFromChannel(knobNumber, sel_channel)
					NILA_transform.updatePanChannel(sel_channel, knobNumber)
					mix.setTrackSel(c.display_track_index, False)
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
								mix.setTrackSel(c.display_track_index, True)
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
			event_id = midi.REC_Plug_MixLevel + track_plugin_id # type: ignore[attr-defined]
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
								mix.setTrackSel(c.display_track_index, True)
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
		refresh_piano_roll_display(sel_channel)

	elif ui.getFocused(c.winName["Playlist"]):
		if NILA_core.seriesCheck():
			timeDisp, currentTime = NILA_core.timeConvert(c.itemDisp, c.itemTime)
			write_series_playlist_time(timeDisp, currentTime)
		else:
			mix.setTrackName(c.display_track_index, "Playlist")
			NILA_transform.setTrackVolGraphFromMixer(c.display_track_index, c.display_track_index)

def OnUpdateBeatIndicator(self, Value):
	"""Updates the beat indicator based on the focused window (e.g., Playlist)."""
	if ui.getFocused(c.winName["Playlist"]):
		timeDisp, currentTime = NILA_core.timeConvert(c.itemDisp, c.itemTime)
		mix.setTrackName(c.display_track_index, "Playlist")
		split_message = ui.getHintMsg()
		split_hint = split_message
		if NILA_core.seriesCheck():
			write_series_playlist_time(timeDisp, currentTime)
		else:
			if timeDisp == "Beats:Bar":
				displayLabel = "B:B" if len(currentTime) >= 5 else "Beats:Bar"
			elif timeDisp == "Min:Sec":
				displayLabel = "M:S" if len(currentTime) > 5 else "Min:Sec"
			else:
				displayLabel = timeDisp
			mix.setTrackExist(c.display_track_index, 1)
			mix.setTrackName(c.display_track_index, "Playlist")
			mix.setTrackVol(c.display_track_index, f"{displayLabel}|{currentTime}")
			mix.setTrackVolGraph(c.display_track_index, 0)

def OnIdle(self):
	"""Performs idle tasks based on the currently focused window."""
	if focus_overlay_is_active():
		write_focus_overlay()
		return

	if ui.getFocused(c.winName["Mixer"]):
		refresh_mixer_display()
	elif ui.getFocused(c.winName["Channel Rack"]):
		refresh_channel_rack_display()

	elif ui.getFocused(c.winName["Playlist"]):
		timeDisp, currentTime = NILA_core.timeConvert(c.itemDisp, c.itemTime)
		split_message = ui.getHintMsg()
		split_hint = split_message

		if NILA_core.seriesCheck():
			marker_name = None if transport.isPlaying() else get_playlist_marker_hint(split_hint)
			write_series_playlist_time(timeDisp, currentTime, marker_name)
		else:
			if timeDisp == "Beats:Bar":
				displayLabel = "B:B" if len(currentTime) >= 5 else "Beats:Bar"
			elif timeDisp == "Min:Sec":
				displayLabel = "M:S" if len(currentTime) > 5 else "Min:Sec"
			else:
				displayLabel = timeDisp
			mix.setTrackExist(c.display_track_index, 1)
			mix.setTrackName(c.display_track_index, "Playlist")
			mix.setTrackVol(c.display_track_index, f"{displayLabel}|{currentTime}")
			mix.setTrackVolGraph(c.display_track_index, 0)

	elif ui.getFocused(c.winName["Browser"]):

		# purge_all_tracks()  # Removed as per instruction

		filename = ui.getFocusedNodeCaption()
		name_no_ext = os.path.splitext(filename)[0]

		if NILA_core.seriesCheck():
			file_ext = os.path.splitext(filename)[1]

			for i in range(c.max_knobs):
				if i < 3:
					mix.setTrackExist(i, 1)
					mix.setTrackName(i, c.blankEvent)
					mix.setTrackVol(i, c.blankEvent)
					mix.setTrackVolGraph(i, 0)
					mix.setTrackPan(i, c.blankEvent)
					mix.setTrackPanGraph(i, 0)
					mix.setTrackSel(i, False)
					mix.setTrackArm(i, False)
					mix.setTrackSolo(i, False)
					mix.setTrackMute(i, False)
				else:
					clear_display_slot(i)

			mix.setTrackName(0, "Browser:")
			mix.setTrackName(1, name_no_ext)
			mix.setTrackName(2, file_ext if file_ext else c.blankEvent)
		else:
			mix.setTrackExist(c.display_track_index, 1)
			mix.setTrackName(c.display_track_index, "Browser:")
			mix.setTrackVol(c.display_track_index, name_no_ext[:15])
			mix.setTrackVolGraph(c.display_track_index, 0)


def purge_tracks(start, end, clear_info=False):
	for track_index in range(start, end + 1):
		if clear_info:
			mix.setTrackPanGraph(track_index, 0)
			mix.setTrackVolGraph(track_index, 0)
			mix.setTrackSel(track_index, False)
			mix.setTrackArm(track_index, False)
			mix.setTrackSolo(track_index, False)
			mix.setTrackMute(track_index, False)
			mix.setTrackName(track_index, c.blankEvent)
			mix.setTrackPan(track_index, c.blankEvent)
			mix.setTrackVol(track_index, c.blankEvent)
		else:
			mix.setTrackExist(track_index, 0)


def refresh_piano_roll_display(channel_index):
	"""Refresh the display for the active Piano Roll channel on slot 0."""
	knobNumber = c.display_track_index
	mix.setTrackExist(knobNumber, 1)
	mix.setTrackName(knobNumber, str(channels.getChannelName(channel_index)))
	NILA_transform.setTrackVolFromChannel(knobNumber, channel_index)
	NILA_transform.setTrackVolGraphFromChannel(knobNumber, channel_index)
	NILA_transform.updatePanChannel(channel_index, knobNumber)