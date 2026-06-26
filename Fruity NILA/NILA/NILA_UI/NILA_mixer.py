import time
import mixer
import ui

from nihia import mixer as nihia_mixer

from NILA.NILA_engine import NILA_core as core, NILA_transform, config, constants as c
MIXER_MIN_VALUE = c.track_volume_min
MIXER_MAX_VALUE = c.track_volume_max
MIXER_ZERO_DB_VALUE = c.mixer_zero_db_value


# Cache for visually ordered mixer tracks
ordered_tracks_cache = []
last_updated_track = None

# Cache mixer volume writes because some assigned mixer tracks can report
# stale values immediately after mixer.setTrackVolume().
#
# Why this exists:
# FL can return the previous mixer volume for assigned tracks immediately after
# a script write. If every knob tick trusts mixer.getTrackVolume(), the next
# target value can be calculated from stale data, which makes assigned tracks
# move slowly, freeze, or jump. During knob movement, this cache is the source
# of truth. It is resynced only when the visible mixer bank changes.
mixer_volume_cache = {}

# Tracks that have just snapped to 0 dB. Used only to create a short detent.
mixer_zero_db_snap_state = {}


def reset_mixer_state_cache():
	"""Reset cached mixer control state after project changes.

	Project loads can leave cached track numbers and volume values pointing at
	old project data. Resetting here prevents the first mixer knob touch from
	jumping to a stale value.
	"""
	global ordered_tracks_cache, last_updated_track
	ordered_tracks_cache = []
	last_updated_track = None
	mixer_volume_cache.clear()
	mixer_zero_db_snap_state.clear()


def sync_visible_mixer_volume_cache():
	"""Sync cached mixer volumes when the visible mixer bank changes.

	This must not run on every knob tick. It runs only when the selected mixer
	track changes and the visible 8 slot bank is recalculated. That gives each
	newly visible track a safe starting value without reintroducing stale FL
	readback during active knob movement.
	"""
	for track_number in ordered_tracks_cache:
		try:
			mixer_volume_cache[track_number] = mixer.getTrackVolume(track_number)
		except Exception:
			mixer_volume_cache.pop(track_number, None)


def update_mixer_order(force=False):
	"""
	Updates and caches the same mixer track slots shown on the display.

	The slot order comes from NILA_transform.get_correct_tracks(), which is the
	shared source of truth for display, knob control, pan graphs, and peak meters.
	Keeping this shared prevents random mixer order from breaking knob targeting.
	"""
	global ordered_tracks_cache, last_updated_track
	current_track = mixer.trackNumber()

	if not force and ordered_tracks_cache and current_track == last_updated_track:
		return

	last_updated_track = current_track
	ordered_tracks_cache = NILA_transform.get_correct_tracks()
	sync_visible_mixer_volume_cache()



def get_adjacent_tracks(current_track):
	"""
	Returns the cached mixer slots shown on the display.
	"""
	if current_track != last_updated_track or not ordered_tracks_cache:
		update_mixer_order()

	return ordered_tracks_cache[:c.max_knobs]


def get_mixer_raw_step(data2, increment):
	"""Returns a raw mixer step for an encoder movement."""
	value = 0.0
	if core.seriesCheck():
		if c.encoder_cc_dec_slow_min <= data2 <= c.encoder_cc_dec_slow_max or c.encoder_cc_dec_fast_min <= data2 <= c.encoder_cc_dec_fast_max:
			value = -increment
		elif c.encoder_cc_inc_fast_min <= data2 <= c.encoder_cc_inc_fast_max or c.encoder_cc_inc_slow_min <= data2 <= c.encoder_cc_inc_slow_max:
			value = increment
	else:
		if data2 == nihia_mixer.KNOB_DECREASE_MAX_SPEED:
			value = -increment
		elif data2 == nihia_mixer.KNOB_INCREASE_MAX_SPEED:
			value = increment
	return value



def get_adaptive_volume_increment(track_number, base_increment):
	"""Uses FL's dB getter for smoother mixer movement.

	Only the mixer uses dB here. Channel Rack remains unchanged elsewhere.
	"""
	return base_increment


# --- Mixer 0 dB snap logic ---
def apply_mixer_zero_db_snap(track_number, current_value, target_value):
	"""Snap mixer volume to 0 dB with a short timed detent.

	This is mixer only. Channel Rack volume is not affected.

	The snap is based on FL's dB readout, not a raw normalized value. When a knob
	movement lands near 0 dB, the mixer fader is written to FL's normalized 0 dB
	point. A short hold creates the detent feel. After the hold expires, the next
	movement is allowed through so the fader does not get trapped at 0 dB.
	"""
	now = time.time()
	state = mixer_zero_db_snap_state.get(track_number)
	current_is_zero_db = abs(current_value - MIXER_ZERO_DB_VALUE) < 0.000001

	if state and current_is_zero_db:
		snap_time, _snap_direction = state
		if now - snap_time < config.mixer_zero_db_hold_time:
			return MIXER_ZERO_DB_VALUE

		# Hold expired. Clear state and let this movement pass through so the
		# fader can continue past 0 dB instead of snapping again immediately.
		del mixer_zero_db_snap_state[track_number]
		return target_value

	if state:
		del mixer_zero_db_snap_state[track_number]

	current_distance = abs(current_value - MIXER_ZERO_DB_VALUE)
	target_distance = abs(target_value - MIXER_ZERO_DB_VALUE)
	moving_toward_zero_db = target_distance < current_distance
	crossed_zero_db = (
		current_value < MIXER_ZERO_DB_VALUE <= target_value or
		current_value > MIXER_ZERO_DB_VALUE >= target_value
	)

	if not moving_toward_zero_db and not crossed_zero_db:
		return target_value

	mixer.setTrackVolume(track_number, target_value)
	target_db = mixer.getTrackVolume(track_number, 1)

	if config.mixer_zero_db_snap_enabled and abs(target_db) <= config.mixer_zero_db_snap_range:
		mixer_zero_db_snap_state[track_number] = (now, 1 if target_value > current_value else -1)
		return MIXER_ZERO_DB_VALUE

	return target_value



def OnMidiMsg(self, event):
	"""
	Handles MIDI messages in FL Studio for mixer control.
	"""
	if ui.getFocused(c.winName["Mixer"]):
		current_track = mixer.trackNumber()

		update_mixer_order()
		adjacent_tracks = get_adjacent_tracks(current_track)
		if not adjacent_tracks:
			event.handled = True
			return

		for z, track_number in enumerate(adjacent_tracks):
			if mixer.getTrackName(track_number) == c.current_track_name:  # Avoid magic string
				continue

			is_volume_control = event.data1 == nihia_mixer.knobs[0][z]
			is_pan_control = event.data1 == nihia_mixer.knobs[1][z]

			if not is_volume_control and not is_pan_control:
				continue

			event.handled = True

			# Track time difference for knob acceleration only after a matching knob is found.
			current_time = time.time()
			last_time_attr = f'last_signal_time_{track_number}_{event.data1}'
			time_diff = current_time - getattr(self, last_time_attr, current_time)
			setattr(self, last_time_attr, current_time)

			if time_diff <= config.mixer_speed_increase_wait:
				base_volume_increment = config.mixer_increment * config.mixer_knob_rotation_speed
				adjusted_pan_increment = config.mixer_increment * config.mixer_knob_rotation_speed
			else:
				base_volume_increment = config.mixer_increment
				adjusted_pan_increment = config.mixer_increment

			adjusted_volume_increment = get_adaptive_volume_increment(track_number, base_volume_increment)

			# Handle volume and pan controls
			if is_volume_control:  # Volume Control
				adjust_mixer_parameter(self, track_number, event.data2, adjusted_volume_increment, c.volume_param_type)
			elif is_pan_control:  # Pan Control
				adjust_mixer_parameter(self, track_number, event.data2, adjusted_pan_increment, c.pan_param_type)

			break

def adjust_mixer_parameter(self, track_number, data2, increment, param_type=c.volume_param_type):
	"""
	Handles dynamic volume or pan control for a mixer track.

	Mixer movement still writes FL's normalized 0.0..1.0 value, but the step
	size is chosen from FL's exact dB getter so movement tracks the dB display
	more closely.
	"""
	value = get_mixer_raw_step(data2, increment)
	if not value:
		return

	if param_type == c.volume_param_type:
		current_value = mixer_volume_cache.get(track_number, mixer.getTrackVolume(track_number))
		target_value = max(MIXER_MIN_VALUE, min(MIXER_MAX_VALUE, current_value + value))
		target_value = apply_mixer_zero_db_snap(track_number, current_value, target_value)
		mixer.setTrackVolume(track_number, target_value)
		mixer_volume_cache[track_number] = target_value
	else:
		mixer.setTrackPan(track_number, mixer.getTrackPan(track_number) + value)