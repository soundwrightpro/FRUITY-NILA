from nihia import buttons
from nihia.mixer import setTrackVol, setTrackName, setTrackPan
from script.device_setup import constants as c
from script.screen_writer import NILA_OLED
import channels
import device
import general
import midi
import mixer
import transport
import ui

# Constants for on and off states
on, off = 1, 0

def get_utility_track():
	""" Returns the last track (Utility) dynamically. """
	return mixer.trackCount() - 1  

def get_mixer_order():
	""" Get mixer tracks sorted by docked position & order of appearance. """
	tracks = [(mixer.getTrackDockSide(i), i) for i in range(mixer.trackCount() - 1)]
	tracks.sort()
	return [track[1] for track in tracks]  # Return sorted track indices

def set_track_info(track_index, name, vol, pan=None):
	""" Sets name, volume, and optionally pan for a track. """
	if device.getName() != "Komplete Kontrol DAW - 1":
		setTrackName(track_index, name)
		setTrackVol(track_index, vol)
		if pan is not None:
			setTrackPan(track_index, pan)

def handle_mixer_action(event, action_function, track_number, hint_message):
	""" Handles mixer actions while ensuring the track is valid. """
	event.handled = True
	if track_number < get_utility_track():
		action_function(track_number)
		ui.setHintMsg(hint_message)

def get_correct_tracks():
	""" Determines the correct 8 tracks for knob control while skipping docked tracks. """
	tracks_order = get_mixer_order()
	current_track = mixer.trackNumber()

	# Ensure current track exists in order list
	if current_track not in tracks_order:
		return [current_track]  # Fallback to single-track control

	start_idx = tracks_order.index(current_track)
	selected_tracks = [current_track]

	# Expand selection while keeping within the same dock section
	for track in tracks_order[start_idx + 1:]:
		if mixer.getTrackDockSide(track) != mixer.getTrackDockSide(current_track):
			break  
		selected_tracks.append(track)
		if len(selected_tracks) == 8:
			break  

	# Ensure selection always contains 8 valid tracks
	while len(selected_tracks) < 8 and selected_tracks[-1] != tracks_order[-1]:
		selected_tracks.append(tracks_order[tracks_order.index(selected_tracks[-1]) + 1])

	return selected_tracks

def OnMidiMsg(self, event):
	""" Handles incoming MIDI events. """
	event.handled = True
	utility_track = get_utility_track()

	if event.data1 == buttons.button_list.get("PLAY") and not ui.isInPopupMenu():
		transport.start()
		ui.setHintMsg("Play/Pause")

	elif event.data1 == buttons.button_list.get("RESTART"):
		transport.stop()
		transport.start()
		set_track_info(0, "Metronome:", "Enabled")
		ui.setHintMsg("Restart")

	elif event.data1 == buttons.button_list.get("REC"):
		transport.record()
		ui.setHintMsg("Record")

	elif event.data1 == buttons.button_list.get("STOP"):
		transport.stop()
		ui.setHintMsg("Stop")

	elif event.data1 == buttons.button_list.get("LOOP"):
		transport.setLoopMode()
		ui.setHintMsg("Song / pattern mode")
		mode = "Enabled" if transport.getLoopMode() == off else "Disabled"
		set_track_info(0, "Pattern:", mode)

	elif event.data1 == buttons.button_list.get("METRO"):
		transport.globalTransport(midi.FPT_Metronome, 110)
		ui.setHintMsg("Metronome")

	elif event.data1 == buttons.button_list.get("TEMPO"):
		transport.stop()
		transport.globalTransport(midi.FPT_TapTempo, 106)

	elif event.data1 == buttons.button_list.get("QUANTIZE"):
		channels.quickQuantize(channels.channelNumber(), 0)
		ui.setHintMsg("Quick Quantize")
		set_track_info(0, "Piano Roll", "Quick Quantize")

	elif event.data1 == buttons.button_list.get("COUNT_IN"):
		transport.globalTransport(midi.FPT_CountDown, 115)
		ui.setHintMsg("Countdown before recording")

	elif event.data1 == buttons.button_list.get("CLEAR"):
		double_click_status = device.isDoubleClick(buttons.button_list.get("CLEAR"))
		if double_click_status:
			transport.globalTransport(midi.FPT_F12, 2, 15)
			ui.setHintMsg("Clear All Windows")
			set_track_info(0, "Clear All", "")
		else:
			ui.escape()
			ui.setHintMsg("Close")

	elif event.data1 == buttons.button_list.get("UNDO"):
		undo_level = str(general.getUndoHistoryCount() - general.getUndoHistoryLast())
		general.undoUp()
		ui.setHintMsg(ui.getHintMsg())
		set_track_info(0, "History", f"Undo @ {undo_level}")

	elif event.data1 == buttons.button_list.get("REDO"):
		undo_level = str(general.getUndoHistoryCount() - general.getUndoHistoryLast())
		general.undo()
		ui.setHintMsg(ui.getHintMsg())
		set_track_info(0, "History", f"Redo @ {undo_level}")

	if event.data1 == buttons.button_list.get("AUTO"):
		event.handled = True
		ui.snapMode(1)
		snapmode_mapping = {
			0: "Line", 1: "Cell", 3: "(none)", 4: "1/6 step", 5: "1/4 step",
			6: "1/3 step", 7: "1/2 step", 8: "Step", 9: "1/6 beat", 10: "1/4 beat",
			11: "1/3 beat", 12: "1/2 beat", 13: "Beat", 14: "Bar"
		}
		snap_mode_name = snapmode_mapping.get(ui.getSnapMode(), "Unknown")
		ui.setHintMsg(f"Snap: {snap_mode_name}")

	button_id = event.data1
	is_mute_button = button_id == buttons.button_list["MUTE_SELECTED"]
	is_solo_button = button_id == buttons.button_list["SOLO_SELECTED"]

	if is_mute_button or is_solo_button:
		event.handled = True
		if mixer.getTrackName(mixer.trackNumber()) != "Current" and mixer.trackNumber() < utility_track:
			mixer_function = mixer.enableTrack if is_mute_button else mixer.soloTrack
			mixer_function(mixer.trackNumber())
			ui.setHintMsg("Mute" if is_mute_button else "Solo")

	if ui.getFocused(c.winName["Mixer"]):
		button_id = event.data1
		tracks_to_control = get_correct_tracks()

		for knob_number, target_track in enumerate(tracks_to_control):
			if button_id == buttons.button_list["MUTE"] and event.data2 == knob_number:
				handle_mixer_action(event, mixer.enableTrack, target_track, "Mute")
			elif button_id == buttons.button_list["SOLO"] and event.data2 == knob_number:
				handle_mixer_action(event, mixer.soloTrack, target_track, "Solo")
			elif button_id == buttons.button_list["TRACK_SELECT"] and event.data2 == knob_number:
				handle_mixer_action(event, mixer.armTrack, target_track, "Armed Disk Recording")

	if ui.getFocused(c.winName["Effect Plugin"]):
		if event.data1 == buttons.button_list.get("TRACK_SELECT") and event.data2 in range(8):
			event.handled = True 

	win_channel_rack = ui.getFocused(c.winName["Channel Rack"])
	if win_channel_rack:
		button_list = buttons.button_list
		channel_count = channels.channelCount()
		selected_channel = channels.selectedChannel()

		for knob_number in range(8):
			if channel_count > knob_number and selected_channel < (channel_count - knob_number):
				if event.data1 == button_list.get("MUTE") and event.data2 == knob_number:
					event.handled = True
					channels.muteChannel(selected_channel + knob_number)
					ui.setHintMsg("Mute")

				if event.data1 == button_list.get("SOLO") and event.data2 == knob_number:
					event.handled = True
					channels.soloChannel(selected_channel + knob_number)
					ui.setHintMsg("Solo")

				if event.data1 == buttons.button_list["TRACK_SELECT"] and event.data2 == knob_number:
					event.handled = True
					channels.selectOneChannel(selected_channel + knob_number)
					ui.setHintMsg("Track selected")
