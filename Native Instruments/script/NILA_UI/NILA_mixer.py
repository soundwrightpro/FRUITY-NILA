import nihia
from script.device_setup import NILA_core as core
from script.device_setup import config
from script.device_setup import constants as c
import mixer
import ui
import time

# Cache for visually ordered mixer tracks
ordered_tracks_cache = []
last_updated_track = None

def update_mixer_order(force=False):
        """Cache the visually sorted mixer track order.

        Args:
                force: Force recalculation even when cached.

        Returns:
                None.
        """
	global ordered_tracks_cache, last_updated_track
	current_track = mixer.trackNumber()
	
	if not force and ordered_tracks_cache and current_track == last_updated_track:
		return

	last_updated_track = current_track
	track_count = mixer.trackCount() - 1  # Exclude Utility track
	tracks = sorted([(mixer.getTrackDockSide(i), i) for i in range(track_count)])  # Sort by dock position
	ordered_tracks_cache = [t[1] for t in tracks]

def get_adjacent_tracks(current_track):
        """Return mixer tracks adjacent to the current one.

        Args:
                current_track: Track index used as the starting point.

        Returns:
                A list of track indices no longer than ``c.max_knobs``.
        """
	if current_track not in ordered_tracks_cache:
		update_mixer_order()

	start_index = ordered_tracks_cache.index(current_track) if current_track in ordered_tracks_cache else 0
	return ordered_tracks_cache[start_index : start_index + c.max_knobs]  # Uses max_knobs constant

def OnMidiMsg(self, event):
        """Handle mixer knob MIDI messages.

        Args:
                self: Script instance.
                event: MIDI event from the controller.

        Returns:
                None.
        """
	if ui.getFocused(c.winName["Mixer"]):
		last_valid_track = mixer.trackCount() - 2  # Last non-Utility track
		current_track = mixer.trackNumber()

		update_mixer_order()
		adjacent_tracks = get_adjacent_tracks(current_track)

		for z, track_number in enumerate(adjacent_tracks):
			if mixer.getTrackName(track_number) != c.current_track_name:  # Avoid magic string
				event.handled = True

				# Track time difference for knob acceleration
				current_time = time.time()
				last_time_attr = f'last_signal_time_{track_number}'
				time_diff = current_time - getattr(self, last_time_attr, current_time)
				setattr(self, last_time_attr, current_time)

				adjusted_increment = config.increment * c.knob_rotation_speed if time_diff <= c.speed_increase_wait else config.increment

				# Handle volume and pan controls
				if event.data1 == nihia.mixer.knobs[0][z]:  # Volume Control
					adjust_mixer_parameter(track_number, event.data2, adjusted_increment, c.volume_param_type)
				elif event.data1 == nihia.mixer.knobs[1][z]:  # Pan Control
					adjust_mixer_parameter(track_number, event.data2, adjusted_increment, c.pan_param_type)

def adjust_mixer_parameter(track_number, data2, increment, param_type=c.volume_param_type):
        """Modify mixer volume or pan from knob input.

        Args:
                track_number: Index of the mixer track.
                data2: MIDI value representing rotation.
                increment: Increment step size.
                param_type: Parameter type constant.

        Returns:
                None.
        """
	value = 0
	if core.seriesCheck():
		if c.encoder_cc_dec_slow_min <= data2 <= c.encoder_cc_dec_slow_max or c.encoder_cc_dec_fast_min <= data2 <= c.encoder_cc_dec_fast_max:
			value = -increment
		elif c.encoder_cc_inc_fast_min <= data2 <= c.encoder_cc_inc_fast_max or c.encoder_cc_inc_slow_min <= data2 <= c.encoder_cc_inc_slow_max:
			value = increment
	else:
		if data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
			value = -increment
		elif data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
			value = increment

	if value:
		if param_type == c.volume_param_type:
			mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) + value)
		else:
			mixer.setTrackPan(track_number, mixer.getTrackPan(track_number) + value)
