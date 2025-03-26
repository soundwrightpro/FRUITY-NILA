import nihia
from script.device_setup import NILA_core as core
from script.device_setup import config
from script.device_setup import constants
import mixer
import ui
import time

# Cache ordered mixer tracks to reduce unnecessary recalculations
ordered_tracks_cache = []
last_updated_track = None

def update_mixer_order(force=False):
	"""
	Updates and caches the mixer track order, sorted visually.
	Only updates when necessary unless forced.
	"""
	global ordered_tracks_cache, last_updated_track
	current_track = mixer.trackNumber()
	
	# Prevent redundant updates
	if not force and ordered_tracks_cache and current_track == last_updated_track:
		return

	last_updated_track = current_track
	track_count = mixer.trackCount() - 1  # Exclude Utility track
	tracks = sorted([(mixer.getTrackDockSide(i), i) for i in range(track_count)])  # Sort by dock position
	ordered_tracks_cache = [t[1] for t in tracks]

def get_adjacent_tracks(current_track):
	"""
	Returns up to 8 visually adjacent mixer tracks.
	"""
	if current_track not in ordered_tracks_cache:
		update_mixer_order()

	start_index = ordered_tracks_cache.index(current_track) if current_track in ordered_tracks_cache else 0
	return ordered_tracks_cache[start_index : start_index + 8]  # Slice up to 8 tracks

def OnMidiMsg(self, event):
	"""
	Handles MIDI messages in FL Studio for mixer control.
	"""
	if ui.getFocused(constants.winName["Mixer"]):
		last_valid_track = mixer.trackCount() - 2  # Last non-Utility track
		current_track = mixer.trackNumber()

		update_mixer_order()  # Ensure track order is up-to-date
		adjacent_tracks = get_adjacent_tracks(current_track)

		for z, track_number in enumerate(adjacent_tracks):
			if mixer.getTrackName(track_number) != "Current":
				event.handled = True
				
				# Track time difference for responsiveness
				current_time = time.time()
				time_diff = current_time - getattr(self, f'last_signal_time_{track_number}', current_time)
				setattr(self, f'last_signal_time_{track_number}', current_time)

				# Adjust increment speed dynamically
				adjusted_increment = config.increment * constants.knob_rotation_speed if time_diff <= constants.speed_increase_wait else config.increment

				# Handle volume and pan controls
				if event.data1 == nihia.mixer.knobs[0][z]:  # Volume Control
					adjust_mixer_parameter(track_number, event.data2, adjusted_increment, "volume")

				elif event.data1 == nihia.mixer.knobs[1][z]:  # Pan Control
					adjust_mixer_parameter(track_number, event.data2, adjusted_increment, "pan")

def adjust_mixer_parameter(track_number, data2, increment, param_type="volume"):
	"""
	Handles dynamic volume or pan control for a mixer track.
	"""
	value = 0
	if core.seriesCheck():
		if 65 <= data2 < 95 or 96 <= data2 < 128:
			value = -increment
		elif 0 <= data2 < 31 or 32 <= data2 < 64:
			value = increment
	else:
		if data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
			value = -increment
		elif data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
			value = increment

	if value:
		if param_type == "volume":
			mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) + value)
		else:
			mixer.setTrackPan(track_number, mixer.getTrackPan(track_number) + value)