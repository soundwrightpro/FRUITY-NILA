import device
import channels
import mixer
import transport
import ui

from nihia import buttons
from nihia.mixer import setTrackSolo, setTrackMute, setTrackArm

from NILA.NILA_engine import constants


# Constants for button light states
on, off = True, False

def set_light(button_name, state):
	"""
	Sets the light state of a button.

	Parameters:
	- button_name (str): The name of the button.
	- state (int): The state of the light (0 for off, 1 for on).
	"""
	buttons.setLight(button_name, state)

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
	""" Determines the correct 8 tracks for button control while skipping docked tracks. """
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
		if len(selected_tracks) == 8:
			break

	while len(selected_tracks) < 8 and selected_tracks[-1] != tracks_order[-1]:
		next_idx = tracks_order.index(selected_tracks[-1]) + 1
		if next_idx < len(tracks_order):
			selected_tracks.append(tracks_order[next_idx])
		else:
			break

	return selected_tracks

def update_transport_lights():
	"""Update transport and global control lights."""
	is_playing = transport.isPlaying()
	is_recording = transport.isRecording()

	set_light("STOP", on if not is_playing else off)
	set_light("REC", on if is_recording else off)
	set_light("LOOP", on if transport.getLoopMode() == off else off)
	set_light("METRO", on if ui.isMetronomeEnabled() else off)
	set_light("COUNT_IN", on if ui.isPrecountEnabled() else off)
	set_light("QUANTIZE", on if ui.getSnapMode() in [1, 3] else on)
	set_light("AUTO", off)

	if not is_playing:
		set_light("PLAY", off)


def update_mixer_lights():
	"""Update mixer mute, solo, and arm lights for the controlled tracks."""
	tracks_to_control = get_correct_tracks()
	utility_track = get_utility_track()

	for x, track_number in enumerate(tracks_to_control):
		if 0 <= track_number <= utility_track:
			is_muted = mixer.isTrackMuted(track_number)
			is_solo = mixer.isTrackSolo(track_number)

			if is_muted and is_solo:
				setTrackMute(x, on)
				setTrackSolo(x, off)
			else:
				setTrackSolo(x, is_solo)
				setTrackMute(x, is_muted)
				setTrackArm(x, mixer.isTrackArmed(track_number))


def update_channel_rack_lights():
	"""Update Channel Rack mute and solo lights."""
	channel_count = channels.channelCount()
	selected_channel = channels.selectedChannel()

	if channel_count >= 2:
		for x in range(8):
			if channel_count > x and selected_channel < (channel_count - x):
				setTrackSolo(x, channels.isChannelSolo(selected_channel + x))
				setTrackMute(x, channels.isChannelMuted(selected_channel + x))
	else:
		setTrackMute(0, on) if channels.isChannelMuted(selected_channel) else setTrackMute(0, off)
		setTrackSolo(0, off) if channel_count == 1 and channels.isChannelSolo(selected_channel) else setTrackSolo(0, off)


def update_encoder_lights():
	"""Set lights for the 4D Encoder on S-Series keyboards."""
	set_light("ENCODER_X_S", 1)
	set_light("ENCODER_X_S", 127)
	set_light("ENCODER_Y_S", 1)
	set_light("ENCODER_Y_S", 127)

def OnRefresh(self, flags):
	"""
	Handles the refresh event and updates button lights based on the DAW state.

	Parameters:
	- self: The instance of the NILA.
	- flags: Flags indicating the refresh event details.
	"""
	if not device.isAssigned():
		return

	update_transport_lights()

	if ui.getFocused(constants.winName["Mixer"]):
		update_mixer_lights()

	if ui.getFocused(constants.winName["Channel Rack"]):
		update_channel_rack_lights()

	update_encoder_lights()

def OnUpdateBeatIndicator(self, Value):
	"""
	Handles the beat indicator update event and updates PLAY and REC button lights.

	Parameters:
	- self: The instance of the NILA.
	- Value: The current beat indicator value.
	"""
	if not transport.isRecording():
		set_light("PLAY", on if Value in [1, 2] else off)
	else:
		set_light("PLAY", on)
		set_light("REC", on if Value in [1, 2] else off)