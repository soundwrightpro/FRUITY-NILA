from nihia import mixer as nihia_mixer
from script.NILA_engine import constants
import channels
import playlist
import math
import ui
import midi
import transport
import mixer 

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

def VolTodB(value: float) -> float:
	"""
	Converts a linear volume value to decibels.

	Parameters:
	- value (float): The linear volume value.

	Returns:
	- float: The corresponding decibel value.
	"""
	if value == 0:
		return "- oo"
	else:
		dB = (math.exp(value * 1.25 * math.log(11)) - 1) * 0.1
		return round(math.log10(dB) * 20, 1)


def updatePanMix(self, track):
    """
    Updates the panning information for a track in the mixer.

    Parameters:
    - track: The track to update.
    """
    if track < 0 or track >= mixer.trackCount():
        return  # Prevents invalid track access

    pan_value = mixer.getTrackPan(track)
    if pan_value == 0:
        nihia_mixer.setTrackPan(track, "Centered")
    elif pan_value > 0:
        nihia_mixer.setTrackPan(track, f"{round(pan_value * 100)}% Right")
    else:
        nihia_mixer.setTrackPan(track, f"{round(abs(pan_value) * 100)}% Left")

    utility_track = get_utility_track()
    
    for x in range(8):
        track_to_update = mixer.trackNumber() + x
        if track_to_update < utility_track:  # Prevent updating the utility track
            nihia_mixer.setTrackPanGraph(x, mixer.getTrackPan(track_to_update))

def updatePanChannel(self, track):
    """
    Updates the panning information for a track in the Channel Rack.

    Parameters:
    - track: The track to update.
    """
    if track < 0 or track >= channels.channelCount():
        return  # Prevents invalid track access

    pan_value = channels.getChannelPan(track)
    if pan_value == 0:
        nihia_mixer.setTrackPan(track, "Centered")
    elif pan_value > 0:
        nihia_mixer.setTrackPan(track, f"{round(pan_value * 100)}% Right")
    else:
        nihia_mixer.setTrackPan(track, f"{round(abs(pan_value) * 100)}% Left")

    nihia_mixer.setTrackPanGraph(0, channels.getChannelPan(channels.selectedChannel()))

    for x in range(1, 8):
        track_to_update = channels.selectedChannel() + x
        if track_to_update < channels.channelCount():  # Prevent accessing invalid tracks
            nihia_mixer.setTrackPanGraph(x, channels.getChannelPan(track_to_update))


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
