import math
import channels
import playlist
import midi
import mixer
import ui

from nihia import mixer as nihia_mixer
from NILA.NILA_engine import constants


CENTERED_PAN_TEXT = "Centered"
RIGHT_PAN_SUFFIX = "% Right"
LEFT_PAN_SUFFIX = "% Left"
FL_DB_FLOOR = -100.0
GRAPH_DB_FLOOR = -60.0
MIXER_DB_MAX = 5.6
CHANNEL_DB_MAX = 0.0
ZERO_DB_ARROW_POSITION = constants.display_vol_bar_scaling
NEGATIVE_DB_ARROW_CURVE = 2.05
POSITIVE_DB_ARROW_CURVE = 1.0
LOW_END_SPLIT = 0.45
LOW_END_CURVE = 0.55


def get_utility_track():
	"""Returns the last track (Utility) dynamically."""
	return mixer.trackCount() - 1

def get_mixer_order():
	"""Get mixer tracks sorted by docked position & order of appearance."""
	track_count = mixer.trackCount() - 1
	tracks = []

	for i in range(track_count):
		dock_side = mixer.getTrackDockSide(i)
		tracks.append((dock_side, i))

	tracks.sort()
	return [t[1] for t in tracks]

def get_correct_tracks():
	"""Determines the correct 8 tracks for knob control while skipping docked tracks."""
	tracks_order = get_mixer_order()
	current_track = mixer.trackNumber()
	utility_track = get_utility_track()

	if current_track in tracks_order:
		start_idx = tracks_order.index(current_track)
	else:
		start_idx = 0

	selected_tracks = [current_track]

	for i in range(start_idx + 1, len(tracks_order)):
		track = tracks_order[i]

		# Skip tracks docked on a different side
		if mixer.getTrackDockSide(track) != mixer.getTrackDockSide(current_track):
			break

		# Stop at utility track
		if track >= utility_track:
			break  

		selected_tracks.append(track)
		if len(selected_tracks) == 8:
			break

	# Fill up the remaining slots if needed
	while len(selected_tracks) < 8 and selected_tracks[-1] != tracks_order[-1]:
		next_idx = tracks_order.index(selected_tracks[-1]) + 1
		if next_idx < len(tracks_order) and tracks_order[next_idx] < utility_track:
			selected_tracks.append(tracks_order[next_idx])
		else:
			break

	return selected_tracks


def _format_db_text(db_value: float) -> str:
	"""Formats a dB value for the display."""
	if db_value <= FL_DB_FLOOR:
		return "- oo"
	return f"{round(db_value, 1)}"


def _curve_normalized_value(value: float, curve: float) -> float:
	"""Apply an adjustable curve to a normalized 0.0..1.0 value.

	curve = 1.0 keeps the mapping linear.
	curve > 1.0 pushes the arrow lower for mid range values.
	curve < 1.0 pushes the arrow higher for mid range values.
	"""
	value = clamp(value, 0.0, 1.0)
	if curve <= 0.0:
		return value
	return value ** curve


def VolTodB(value: float) -> float | str:
	"""Fallback conversion for raw 0..1 style values."""
	if value <= 0:
		return "- oo"
	dB = (math.exp(value * 1.25 * math.log(11)) - 1) * 0.1
	return round(math.log10(dB) * 20, 1)



def getMixerVolumeDb(track: int) -> float:
	"""Returns the exact FL mixer volume in dB."""
	return float(mixer.getTrackVolume(track, 1))



def getChannelVolumeDb(channel: int) -> float:
	"""Returns the exact FL Channel Rack volume in dB."""
	return float(channels.getChannelVolume(channel, 1)) # type: ignore



def getMixerArrowValue(track: int) -> float:
	"""Maps FL mixer dB onto the fixed S-Series graph.

	The negative dB section uses an adjustable curve because the hardware's
	printed scale is visually compressed near the bottom and expanded near 0 dB.
	Set NEGATIVE_DB_ARROW_CURVE to tune the arrow without affecting knob speed.
	"""
	db_value = getMixerVolumeDb(track)
	if db_value <= GRAPH_DB_FLOOR:
		return 0.0
	if db_value <= 0.0:
		normalized = (db_value - GRAPH_DB_FLOOR) / (0.0 - GRAPH_DB_FLOOR)


		if normalized < LOW_END_SPLIT:
			split_value = _curve_normalized_value(LOW_END_SPLIT, NEGATIVE_DB_ARROW_CURVE)
			normalized = split_value * ((normalized / LOW_END_SPLIT) ** LOW_END_CURVE)
		else:
			normalized = _curve_normalized_value(normalized, NEGATIVE_DB_ARROW_CURVE)


		return clamp(normalized * ZERO_DB_ARROW_POSITION, 0.0, ZERO_DB_ARROW_POSITION)

	normalized = db_value / MIXER_DB_MAX
	normalized = _curve_normalized_value(normalized, POSITIVE_DB_ARROW_CURVE)
	return clamp(
		ZERO_DB_ARROW_POSITION + normalized * (1.0 - ZERO_DB_ARROW_POSITION),
		ZERO_DB_ARROW_POSITION,
		1.0,
	)


def getChannelArrowValue(channel: int) -> float:
	"""Maps Channel Rack dB onto the fixed S-Series graph.

	Channel Rack tops out at 0 dB, and the negative section uses the same
	adjustable curve as the mixer so the arrow can be tuned easily.
	"""
	db_value = getChannelVolumeDb(channel)
	if db_value <= GRAPH_DB_FLOOR:
		return 0.0
	normalized = (db_value - GRAPH_DB_FLOOR) / (CHANNEL_DB_MAX - GRAPH_DB_FLOOR)
	normalized = _curve_normalized_value(normalized, NEGATIVE_DB_ARROW_CURVE)
	return clamp(normalized * ZERO_DB_ARROW_POSITION, 0.0, ZERO_DB_ARROW_POSITION)



def setTrackVolFromMixer(slot_index: int, track: int):
	"""Sets mixer volume text from FL's exact dB value."""
	nihia_mixer.setTrackVol(slot_index, f"{_format_db_text(getMixerVolumeDb(track))} dB")



def setTrackVolFromChannel(slot_index: int, channel: int):
	"""Sets Channel Rack volume text from FL's exact dB value."""
	nihia_mixer.setTrackVol(slot_index, f"{_format_db_text(getChannelVolumeDb(channel))} dB")



def setTrackVolGraphFromMixer(slot_index: int, track: int):
	"""Sets mixer arrow from FL's 0.00..1.90 value domain."""
	nihia_mixer.setTrackVolGraph(slot_index, getMixerArrowValue(track))



def setTrackVolGraphFromChannel(slot_index: int, channel: int):
	"""Sets Channel Rack arrow from FL's 0.00..1.00 value domain."""
	nihia_mixer.setTrackVolGraph(slot_index, getChannelArrowValue(channel))



def updatePanMix(track: int, slot_index: int):
    """Updates mixer pan text and graph values for an slot."""
    if track < 0 or track >= mixer.trackCount():
        return

    pan_value = mixer.getTrackPan(track)
    if pan_value == 0:
        nihia_mixer.setTrackPan(slot_index, CENTERED_PAN_TEXT)
    elif pan_value > 0:
        nihia_mixer.setTrackPan(slot_index, f"{round(pan_value * 100)}{RIGHT_PAN_SUFFIX}")
    else:
        nihia_mixer.setTrackPan(slot_index, f"{round(abs(pan_value) * 100)}{LEFT_PAN_SUFFIX}")

    utility_track = get_utility_track()
    for x in range(8):
        track_to_update = mixer.trackNumber() + x
        if track_to_update < utility_track:
            nihia_mixer.setTrackPanGraph(x, mixer.getTrackPan(track_to_update))
        else:
            nihia_mixer.setTrackPanGraph(x, 0)


def updatePanChannel(channel: int, slot_index: int):
    """Updates Channel Rack pan text and graph values for an slot."""
    if channel < 0 or channel >= channels.channelCount():
        return

    pan_value = channels.getChannelPan(channel)
    if pan_value == 0:
        nihia_mixer.setTrackPan(slot_index, CENTERED_PAN_TEXT)
    elif pan_value > 0:
        nihia_mixer.setTrackPan(slot_index, f"{round(pan_value * 100)}{RIGHT_PAN_SUFFIX}")
    else:
        nihia_mixer.setTrackPan(slot_index, f"{round(abs(pan_value) * 100)}{LEFT_PAN_SUFFIX}")

    for x in range(8):
        track_to_update = channels.selectedChannel() + x
        if track_to_update < channels.channelCount():
            nihia_mixer.setTrackPanGraph(x, channels.getChannelPan(track_to_update))
        else:
            nihia_mixer.setTrackPanGraph(x, 0)


def sendPeakInfo():
	"""Sends peak meter data to the mixer."""
	TrackPeaks = [0] * 16

	if ui.getFocused(constants.winName["Mixer"]):
		for x in range(8):
			if mixer.trackNumber() <= get_utility_track() - x:
				TrackPeaks[(x * 2)] = int(mixer.getTrackPeaks(mixer.trackNumber() + x, midi.PEAK_L) * 127)
				TrackPeaks[(x * 2) + 1] = int(mixer.getTrackPeaks(mixer.trackNumber() + x, midi.PEAK_R) * 127)

	elif ui.getFocused(constants.winName["Channel Rack"]):
		for x in range(8):
			if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
				if channels.getTargetFxTrack(channels.selectedChannel() + x) > 0:
					TrackPeaks[(x * 2)] = int(mixer.getTrackPeaks(channels.getTargetFxTrack(channels.selectedChannel() + x), midi.PEAK_L) * 127)
					TrackPeaks[(x * 2) + 1] = int(mixer.getTrackPeaks(channels.getTargetFxTrack(channels.selectedChannel() + x), midi.PEAK_R) * 127)

	# Ensure values are within expected range (0 to 127)
	for x in range(len(TrackPeaks)):
		TrackPeaks[x] = max(0, min(127, TrackPeaks[x]))

	nihia_mixer.sendPeakMeterData(TrackPeaks)


def timeConvert(timeDisp, currentTime):
	"""
	Converts and formats the time display.

	Parameters:
	- timeDisp: The current time display mode.
	- currentTime: The current time.

	Returns:
	- Tuple[str, str]: The formatted time display and current time.
	"""
	currentBar = str(playlist.getVisTimeBar())
	currentStep = str(playlist.getVisTimeStep())

	try:
		step_int = int(currentStep)
	except (ValueError, TypeError):
		step_int = -1

	if 0 <= step_int <= 9:
		currentTime = f"{currentBar}:0{step_int}"
	elif step_int >= 0:
		currentTime = f"{currentBar}:{step_int}"
	else:
		currentTime = str(currentStep)

	if step_int >= 0:
		timeDisp = "Min:Sec" if ui.getTimeDispMin() else "Beats:Bar"
	else:
		timeDisp = "REC in..."

	return timeDisp, currentTime

def setTrackVolConvert(trackID: int, value: str):
	"""
	Sets the volume for a track in the mixer.

	Parameters:
	- trackID (int): The ID of the track.
	- value (str): The volume value to set.
	"""
	if value == "-inf dB":
		value = "- oo dB"
	nihia_mixer.setTrackVol(trackID, value)

def clamp(value, min_value, max_value):
	"""
	Clamps the given value within the specified range.

	Args:
		value: The value to be clamped.
		min_value: The minimum allowed value.
		max_value: The maximum allowed value.

	Returns:
		The clamped value.
	"""
	return max(min(value, max_value), min_value)