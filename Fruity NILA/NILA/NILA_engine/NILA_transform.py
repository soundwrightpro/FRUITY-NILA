import math
import channels
import playlist
import midi
import mixer
import ui

from nihia import mixer as nihia_mixer
from NILA.NILA_engine import constants as c


CENTERED_PAN_TEXT = c.mixer_centered_pan_text
RIGHT_PAN_SUFFIX = c.mixer_pan_right_suffix
LEFT_PAN_SUFFIX = c.mixer_pan_left_suffix
FL_DB_FLOOR = -100.0
GRAPH_DB_FLOOR = -60.0
MIXER_DB_MAX = 5.6
CHANNEL_DB_MAX = 0.0
ZERO_DB_ARROW_POSITION = c.display_vol_bar_scaling
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
	tracks = [(mixer.getTrackDockSide(i), i) for i in range(track_count)]
	tracks.sort()
	return [t[1] for t in tracks]

def get_correct_tracks():
	"""Return the shared visible mixer slots.

	This is the single source of truth for the 8 mixer slots shown on the
	controller. Display text, knob control, pan graphs, and peak meters should all
	use this function so random mixer ordering does not make those systems drift
	apart.
	"""
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

    tracks_to_control = get_correct_tracks()
    for x in range(c.max_knobs):
        if x < len(tracks_to_control):
            nihia_mixer.setTrackPanGraph(x, mixer.getTrackPan(tracks_to_control[x]))
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

    for x in range(c.max_knobs):
        track_to_update = channels.selectedChannel() + x
        if track_to_update < channels.channelCount():
            nihia_mixer.setTrackPanGraph(x, channels.getChannelPan(track_to_update))
        else:
            nihia_mixer.setTrackPanGraph(x, 0)


def sendPeakInfo():
	"""Send live peak meter data to the hardware display.

	For Mixer focus, peak data follows get_correct_tracks() so the meters match
	the same random order used by the display and knobs. For Channel Rack focus,
	peak data follows each channel's target mixer insert.
	"""
	TrackPeaks = [0] * c.peak_meter_data_length

	if ui.getFocused(c.winName["Mixer"]):
		tracks_to_control = get_correct_tracks()
		for x, track_number in enumerate(tracks_to_control[:c.max_knobs]):
			TrackPeaks[(x * 2)] = int(mixer.getTrackPeaks(track_number, midi.PEAK_L) * c.peak_meter_max_value)
			TrackPeaks[(x * 2) + 1] = int(mixer.getTrackPeaks(track_number, midi.PEAK_R) * c.peak_meter_max_value)

	elif ui.getFocused(c.winName["Channel Rack"]):
		for x in range(8):
			if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
				if channels.getTargetFxTrack(channels.selectedChannel() + x) > 0:
					TrackPeaks[(x * 2)] = int(mixer.getTrackPeaks(channels.getTargetFxTrack(channels.selectedChannel() + x), midi.PEAK_L) * c.peak_meter_max_value)
					TrackPeaks[(x * 2) + 1] = int(mixer.getTrackPeaks(channels.getTargetFxTrack(channels.selectedChannel() + x), midi.PEAK_R) * c.peak_meter_max_value)

	# Ensure values are within expected range.
	for x in range(len(TrackPeaks)):
		TrackPeaks[x] = max(0, min(c.peak_meter_max_value, TrackPeaks[x]))

	nihia_mixer.sendPeakMeterData(TrackPeaks)


# --- Clear live peak meter data on the hardware display ---
def clearPeakInfo():
	"""Actively clear live peak meter data on the hardware display.

	Stopping normal meter updates is not enough because the hardware keeps the
	last peak frame. During the temporary focus overlay, this sends a zero peak
	packet so the meter area is actually blank.
	"""
	nihia_mixer.sendPeakMeterData([0] * c.peak_meter_data_length)


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