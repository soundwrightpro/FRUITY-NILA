import time
import arrangement as arrange
import channels
import device
import midi
import playlist
import mixer
import plugins
import transport
import ui

import nihia.buttons as buttons

from NILA.NILA_engine import config, constants as c
from NILA.NILA_visuals import NILA_Display


xAxis, yAxis = 0, 0
windowCycle = 0
last_click_time = 0
current_track_plugin_id = None
current_generator_cycle_index = None
current_playlist_tool_index = 0

pending_encoder_button_single = None
mixer_x_axis_step = 8

mixer_inertia_velocity = 0.0
mixer_inertia_last_step_time = 0.0
mixer_inertia_last_spin_time = 0.0
mixer_inertia_last_spin_direction = 0
mixer_inertia_fast_spin_count = 0

MIXER_INERTIA_ACCELERATION = 1.75
MIXER_INERTIA_DECAY = 0.76
MIXER_INERTIA_STOP_THRESHOLD = 0.25
MIXER_INERTIA_STEP_INTERVAL = 0.035
MIXER_INERTIA_MAX_VELOCITY = 8.0
MIXER_INERTIA_TRIGGER_INTERVAL = 0.055
MIXER_INERTIA_TRIGGER_COUNT = 2

BUTTONS = buttons.button_list

UNSUPPORTED_PLUGINS = tuple(c.unsupported_plugins or ())
DIRECT_NAVIGATION_PLUGINS = tuple(c.direct_navigation_plugins or ())


def _button(name):
	return BUTTONS[name]

ENCODER_GENERAL = _button("ENCODER_GENERAL")
ENCODER_VOLUME_SELECTED = _button("ENCODER_VOLUME_SELECTED")
ENCODER_SELECTED_PLUS = _button("ENCODER_SELECTED_PLUS")
ENCODER_SELECTED_MINUS = _button("ENCODER_SELECTED_MINUS")
ENCODER_PAN_SELECTED = _button("ENCODER_PAN_SELECTED")
ENCODER_BUTTON = _button("ENCODER_BUTTON")
ENCODER_BUTTON_SHIFTED = _button("ENCODER_BUTTON_SHIFTED")
RIGHT_BUTTON = _button("RIGHT")
LEFT_BUTTON = _button("LEFT")
UP_BUTTON = _button("UP")
DOWN_BUTTON = _button("DOWN")
ENCODER_Y_S = _button("ENCODER_Y_S")
ENCODER_X_S = _button("ENCODER_X_S")
ENCODER_Y_A = _button("ENCODER_Y_A")
ENCODER_X_A = _button("ENCODER_X_A")

PLAYLIST_TOOLS = (
	("Pencil", midi.EETool_Pencil), # type: ignore
	("Brush", midi.EETool_Brush),	# type: ignore
	("Delete", midi.EETool_Del),	# type: ignore
	("Mute", midi.EETool_Mute),		# type: ignore
	("Slip", midi.EETool_Slip),		# type: ignore
	("Slice", midi.EETool_Cut),		# type: ignore
	("Select", midi.EETool_Sel),	# type: ignore
	("Zoom", midi.EETool_Zoom),		# type: ignore
	("Playback", midi.EETool_Play), # type: ignore
)


def _popup_enter_or_open_menu(menu_transport, menu_hint):
	if ui.isInPopupMenu():
		ui.enter()
		ui.setHintMsg("Enter")
	else:
		transport.globalTransport(menu_transport, menu_hint)
		ui.setHintMsg("Open Menu")
		mixer.deselectAll()
		mixer.selectTrack(mixer.trackNumber())


def _flush_pending_encoder_button_single():
	global pending_encoder_button_single

	if pending_encoder_button_single is not None:
		now = time.time()
		if (now - pending_encoder_button_single["time"]) >= config.double_click_speed:
			action = pending_encoder_button_single["action"]
			pending_encoder_button_single = None
			action()


# --- Mixer inertia and jog helpers ---

def _get_mixer_order():
	tc = mixer.trackCount() - 1
	return [i for _, i in sorted((mixer.getTrackDockSide(i), i) for i in range(tc))]


def _update_mixer_selection(startTrack, tracks_order):
	track_count = len(tracks_order)
	start_idx = tracks_order.index(startTrack)
	start_dock_side = mixer.getTrackDockSide(startTrack)
	selected_tracks = [startTrack]

	for i in range(start_idx + 1, track_count):
		track = tracks_order[i]
		if mixer.getTrackDockSide(track) != start_dock_side:
			break
		selected_tracks.append(track)
		if len(selected_tracks) >= 8:
			break

	while len(selected_tracks) < 8 and selected_tracks[-1] != tracks_order[-1]:
		next_idx = tracks_order.index(selected_tracks[-1]) + 1
		if next_idx < len(tracks_order) and mixer.getTrackDockSide(tracks_order[next_idx]) == start_dock_side:
			selected_tracks.append(tracks_order[next_idx])
		else:
			break

	ui.miDisplayRect(selected_tracks[0], selected_tracks[-1], config.rectMixer)


def _jog_mixer_track(direction):
	tracks_order = _get_mixer_order()
	if not tracks_order:
		return

	currentTrack = mixer.trackNumber()
	try:
		current_idx = tracks_order.index(currentTrack)
	except ValueError:
		current_idx = 0

	new_idx = (current_idx + direction) % len(tracks_order)
	newTrack = tracks_order[new_idx]
	mixer.setTrackNumber(newTrack)

	# Attempt to force mixer viewport scroll, then restore the intended track.
	if direction > 0:
		ui.right(1)
	else:
		ui.left(1)
	mixer.setTrackNumber(newTrack)

	_update_mixer_selection(newTrack, tracks_order)


def _start_mixer_inertia(direction):
	global mixer_inertia_velocity
	global mixer_inertia_last_spin_time
	global mixer_inertia_last_spin_direction
	global mixer_inertia_fast_spin_count

	now = time.time()
	fast_repeat = (
		mixer_inertia_last_spin_direction == direction
		and (now - mixer_inertia_last_spin_time) <= MIXER_INERTIA_TRIGGER_INTERVAL
	)

	# Always perform the normal one-step mixer jog first.
	# This preserves the original slow-spin behavior.
	_jog_mixer_track(direction)

	if fast_repeat:
		mixer_inertia_fast_spin_count += 1
	else:
		mixer_inertia_fast_spin_count = 1
		mixer_inertia_velocity = 0.0

	if mixer_inertia_fast_spin_count >= MIXER_INERTIA_TRIGGER_COUNT:
		mixer_inertia_velocity += direction * MIXER_INERTIA_ACCELERATION
		mixer_inertia_velocity = max(
			-MIXER_INERTIA_MAX_VELOCITY,
			min(MIXER_INERTIA_MAX_VELOCITY, mixer_inertia_velocity)
		)

	mixer_inertia_last_spin_time = now
	mixer_inertia_last_spin_direction = direction


def _apply_mixer_inertia():
	global mixer_inertia_velocity
	global mixer_inertia_last_step_time
	global mixer_inertia_fast_spin_count

	if abs(mixer_inertia_velocity) < MIXER_INERTIA_STOP_THRESHOLD:
		mixer_inertia_velocity = 0.0
		mixer_inertia_fast_spin_count = 0
		return

	if not ui.getFocused(c.winName["Mixer"]):
		mixer_inertia_velocity = 0.0
		mixer_inertia_fast_spin_count = 0
		return

	if ui.isInPopupMenu():
		mixer_inertia_velocity = 0.0
		mixer_inertia_fast_spin_count = 0
		return

	now = time.time()
	if (now - mixer_inertia_last_step_time) < MIXER_INERTIA_STEP_INTERVAL:
		return

	mixer_inertia_last_step_time = now
	direction = 1 if mixer_inertia_velocity > 0 else -1
	_jog_mixer_track(direction)
	mixer_inertia_velocity *= MIXER_INERTIA_DECAY

def OnRefresh(self, flags):
	global ordered_tracks
	_flush_pending_encoder_button_single()


def OnIdle(self):
	_flush_pending_encoder_button_single()
	_apply_mixer_inertia()

def onButtonClick(button):
	global last_click_time
	now = time.time()
	double_click_status = (now - last_click_time) < config.double_click_speed
	last_click_time = now
	return double_click_status

def encoder(self, event):
	try: 
		global windowCycle
		global current_track_plugin_id
		global current_generator_cycle_index
		global current_playlist_tool_index
		global_index = False
		global mixer_x_axis_step
		def cycle_channel_rack_generators(direction):
			"""Cycle through valid Channel Rack generator plugin windows only."""
			global current_generator_cycle_index
			generator_targets = []

			for channel_index in range(channels.channelCount()):
				try:
					if plugins.isValid(channel_index, c.gen_plugin):
						generator_targets.append(channel_index)
				except Exception:
					pass

			if not generator_targets:
				ui.setHintMsg("No Channel Rack generators")
				return

			selected_channel = channels.selectedChannel()
			if selected_channel in generator_targets:
				current_index = generator_targets.index(selected_channel)
			elif current_generator_cycle_index in generator_targets:
				current_index = generator_targets.index(current_generator_cycle_index)
			else:
				current_index = -1 if direction > 0 else 0

			next_index = (current_index + direction) % len(generator_targets)
			target_channel = generator_targets[next_index]
			current_generator_cycle_index = target_channel
			channels.selectChannel(target_channel, 1)
			channels.showCSForm(target_channel, 1)
			channels.focusEditor(target_channel)
			ui.setHintMsg("Generator plugin window")

		def get_current_playlist_tool_index():
			"""Return FL Studio's current Playlist tool index when available."""
			try:
				current_tool_id = playlist.getTool() # type: ignore
			except Exception:
				return current_playlist_tool_index

			for index, (_, tool_id) in enumerate(PLAYLIST_TOOLS):
				if tool_id == current_tool_id:
					return index

			return current_playlist_tool_index

		def cycle_playlist_tools(direction):
			"""Cycle through Playlist tools when the Playlist is focused."""
			global current_playlist_tool_index

			current_playlist_tool_index = (get_current_playlist_tool_index() + direction) % len(PLAYLIST_TOOLS)
			tool_name, tool_id = PLAYLIST_TOOLS[current_playlist_tool_index]
			playlist.selectTool(tool_id) # type: ignore
			ui.setHintMsg(f"Playlist Tool: {tool_name}")

		def jog(direction):
			winMixer = ui.getFocused(c.winName["Mixer"])
			winChan = ui.getFocused(c.winName["Channel Rack"])
			if winMixer:
				_jog_mixer_track(direction)
			elif winChan:
				ui.jog(direction)
				ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
				ui.setHintMsg("Channel Rack selection rectangle")

		def browse(action):
			if ui.isInPopupMenu():
				if action == "next":
					ui.down(1)
				else:
					ui.up(1)
			else:
				if action == "next":
					ui.navigateBrowser(midi.FPT_Down, False)
				else:
					ui.navigateBrowser(midi.FPT_Up, False)
				NILA_Display.OnIdle(self)
				if config.jog_preview_sound == 1:
					ui.previewBrowserMenuItem()


		# --- Begin event handling ---
		winFocused = {name: ui.getFocused(c.winName[name]) for name in (
			"Mixer", "Channel Rack", "Plugin", "Effect Plugin", "Generator Plugin", "Playlist", "Browser", "Piano Roll"
		)}

		def get_focused_generator_plugin_name():
			"""Return the focused generator plugin name, or None when unavailable."""
			if not winFocused["Generator Plugin"]:
				return None

			channel_index = channels.selectedChannel()
			try:
				if not plugins.isValid(channel_index, c.gen_plugin):
					return None
				return plugins.getPluginName(channel_index, c.gen_plugin, False, global_index)
			except Exception:
				return None

		def focused_generator_uses_direct_navigation():
			"""Return True when the focused generator plugin needs raw FL UI navigation."""
			return get_focused_generator_plugin_name() in DIRECT_NAVIGATION_PLUGINS

		def get_window_cycle_order():
			"""Return the main window cycle order.

			Clockwise order:
			Channel Rack -> Piano Roll (if visible) -> Mixer -> Playlist -> Browser
			"""
			order = ["Channel Rack"]
			if ui.getVisible(c.winName["Piano Roll"]):
				order.append("Piano Roll")
			order.extend(["Mixer", "Playlist", "Browser"])
			return order

		def cycle_main_windows(direction):
			"""Cycle main FL windows without disturbing existing spin behavior."""
			order = get_window_cycle_order()
			current_index = None
			for idx, name in enumerate(order):
				if ui.getFocused(c.winName[name]):
					current_index = idx
					break

			if current_index is None:
				current_index = 0 if direction > 0 else len(order) - 1
			else:
				current_index = (current_index + direction) % len(order)

			target_name = order[current_index]
			ui.showWindow(c.winName[target_name])
			ui.setHintMsg(target_name)
			NILA_Display.show_temporary_focus_message(target_name)

		def is_s_series_device():
			"""Return True when running on the S-Series DAW port."""
			return device.getName() == "Komplete Kontrol DAW - 1"

		def is_shifted_selected_encoder_spin():
			"""Return True for the S-Series shifted selected-encoder spin event.

			Uses the named button constants, but also accepts the known raw values so
			it still works if the button mapping file was reverted or not reloaded yet.
			"""
			return (
				event.data1 == ENCODER_VOLUME_SELECTED
				and event.data2 in (
					ENCODER_SELECTED_PLUS,
					ENCODER_SELECTED_MINUS,
					12,
					116,
				)
			)

		def plugin_has_named_presets(index, slot_index=-1):
			"""Return True only when the focused plugin exposes usable named presets."""
			try:
				if not plugins.isValid(index, slot_index, global_index):
					return False
				preset_count = plugins.getPresetCount(index, slot_index, global_index)
				return preset_count > 1
			except Exception:
				return False

		def change_plugin_preset(index, slot_index, direction):
			"""Change plugin preset only when a usable preset list is available."""
			if not plugin_has_named_presets(index, slot_index):
				return False
			if direction > 0:
				plugins.nextPreset(index, slot_index, global_index)
			else:
				plugins.prevPreset(index, slot_index, global_index)
			return True

		def scroll_plugin_parameters(direction, skip, plugin_id):
			"""Scroll the displayed plugin parameter bank when enough parameters are available."""
			if plugin_id != c.last_plugin_name:
				c.lead_param = 0
				c.last_plugin_name = plugin_id

			if c.actual_param_count <= 7:
				return

			target = min if direction > 0 else max
			value = c.lead_param + skip if direction > 0 else c.lead_param - skip
			bound = c.actual_param_count - 7 if direction > 0 else 0
			c.lead_param = target(value, bound)
			NILA_Display.OnRefresh(self, event)

		def handle_plugin_nav(direction, skip):
			if winFocused["Effect Plugin"]:
				idx = mixer.getActiveEffectIndex()
				if not idx:
					return

				mix_track_index, mixer_slot = idx
				if not plugins.isValid(mix_track_index, mixer_slot):
					return

				plugin_name = plugins.getPluginName(mix_track_index, mixer_slot, False, global_index)
				if plugin_name in UNSUPPORTED_PLUGINS:
					ui.down(1) if direction > 0 else ui.up(1)
					return

				track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
				scroll_plugin_parameters(direction, skip, track_plugin_id)
				return

			if winFocused["Generator Plugin"]:
				channel_index = channels.selectedChannel()
				plugin_name = get_focused_generator_plugin_name()
				if plugin_name is None:
					return

				if plugin_name in DIRECT_NAVIGATION_PLUGINS:
					ui.down(1) if direction > 0 else ui.up(1)
					return

				if plugin_name in UNSUPPORTED_PLUGINS:
					ui.down(1) if direction > 0 else ui.up(1)
					return

				if channels.getChannelType(channel_index) not in (0, 3, 4, 5):
					plugin_id = plugins.getPluginName(channel_index, c.gen_plugin)
					scroll_plugin_parameters(direction, skip, plugin_id)

		def handle_encoder_button(button_id):
			global pending_encoder_button_single
			if focused_generator_uses_direct_navigation():
				ui.enter()
				ui.setHintMsg("Enter")
				return
			if winFocused["Mixer"]:
				if onButtonClick(button_id):
					_popup_enter_or_open_menu(midi.FPT_Menu, midi.GT_Menu)
				return
			elif winFocused["Plugin"] or winFocused["Piano Roll"]:
				ui.enter()
				if onButtonClick(button_id):
					_popup_enter_or_open_menu(midi.FPT_Menu, midi.GT_Menu)
			elif winFocused["Channel Rack"]:
				if is_s_series_device() and button_id == ENCODER_BUTTON:
					now = time.time()
					if (
						pending_encoder_button_single is not None
						and pending_encoder_button_single.get("kind") == "s_series_channel_wrapper"
						and (now - pending_encoder_button_single["time"]) < config.double_click_speed
					):
						pending_encoder_button_single = None
						_popup_enter_or_open_menu(midi.FPT_ItemMenu, 4)
					else:
						channel_index = channels.selectedChannel()
						pending_encoder_button_single = {
							"kind": "s_series_channel_wrapper",
							"time": now,
							"action": lambda idx=channel_index: channels.showCSForm(idx, 1)
						}
				elif onButtonClick(button_id):
					_popup_enter_or_open_menu(midi.FPT_ItemMenu, 4)
			elif winFocused["Playlist"]:
				if onButtonClick(button_id) and not ui.isInPopupMenu():
					arrange.addAutoTimeMarker(mixer.getSongTickPos(), str("Mark"))
			elif winFocused["Browser"]:
				if ui.isInPopupMenu():
					pending_encoder_button_single = None
					ui.enter()
					ui.setHintMsg("Select menu item")
					return

				now = time.time()
				if (
					pending_encoder_button_single is not None
					and pending_encoder_button_single.get("kind") == "browser_toggle_node"
					and (now - pending_encoder_button_single["time"]) < config.double_click_speed
				):
					pending_encoder_button_single = None
					_popup_enter_or_open_menu(midi.FPT_ItemMenu, 4)
				else:
					pending_encoder_button_single = {
						"kind": "browser_toggle_node",
						"time": now,
						"action": lambda: (ui.toggleBrowserNode(), ui.setHintMsg("Toggle browser node"))
					}
			else:
				ui.enter()

		# --- SHIFT + SELECTED ENCODER SPIN WINDOW CYCLE ---
		# S-Series only: shifted selected encoder spin cycles the main windows.
		if is_s_series_device() and is_shifted_selected_encoder_spin():
			event.handled = True
			if event.data2 in (ENCODER_SELECTED_PLUS, 12):
				cycle_main_windows(1)
			else:
				cycle_main_windows(-1)
			return

		# --- ENCODER HANDLING ---
		if event.data1 in (
			ENCODER_GENERAL,
			ENCODER_VOLUME_SELECTED
		):
			plugin_skip = 1
			if event.data1 == ENCODER_VOLUME_SELECTED:
				mixer_x_axis_step = 8
			if event.data2 in (RIGHT_BUTTON, c.mixer_right):
				event.handled = True
				if winFocused["Mixer"]: 
					if ui.isInPopupMenu():
						ui.down(1)
					else:			
						_start_mixer_inertia(1)
				elif winFocused["Channel Rack"]: 
					jog(1)
				elif winFocused["Plugin"]: 
					handle_plugin_nav(1, plugin_skip)
				elif winFocused["Playlist"]: 
					ui.jog(1)
				elif winFocused["Piano Roll"]: 
					ui.verZoom(-1)
				elif winFocused["Browser"]: 
					browse("next")
				else: 
					ui.down(1)
			elif event.data2 in (LEFT_BUTTON, c.mixer_left):
				event.handled = True
				if winFocused["Mixer"]: 
					if ui.isInPopupMenu():
						ui.up(1)
					else:			
						_start_mixer_inertia(-1)
				elif winFocused["Channel Rack"]: 
					jog(-1)
				elif winFocused["Plugin"]: 
					handle_plugin_nav(-1, plugin_skip)
				elif winFocused["Playlist"]: 
					ui.jog(-1)
				elif winFocused["Piano Roll"]: 
					ui.verZoom(1)
				elif winFocused["Browser"]: 
					browse("previous")
				else: 
					ui.up(1)

		if event.data1 == ENCODER_PAN_SELECTED:
			mixer_x_axis_step = 1
			if event.data2 in (ENCODER_SELECTED_PLUS, ENCODER_SELECTED_MINUS, 12, 116):
				event.handled = True
				direction = 1 if event.data2 in (ENCODER_SELECTED_PLUS, 12) else -1
				if winFocused["Playlist"]:
					transport.globalTransport(midi.FPT_HZoomJog, direction, midi.PME_System, midi.GT_All)
				else:
					cycle_channel_rack_generators(direction)
				return

			if event.data2 in (RIGHT_BUTTON, c.mixer_right):
				event.handled = True
				if winFocused["Mixer"]:
					t = mixer.trackNumber()
					mixer.setTrackStereoSep(t, mixer.getTrackStereoSep(t) + c.stereo_sep)
				if winFocused["Playlist"]:
					cycle_playlist_tools(1)
				elif winFocused["Piano Roll"]:
					transport.globalTransport(midi.FPT_HZoomJog, 1, midi.PME_System, midi.GT_All)
			if event.data2 in (LEFT_BUTTON, c.mixer_left):
				event.handled = True
				if winFocused["Mixer"]:
					t = mixer.trackNumber()
					mixer.setTrackStereoSep(t, mixer.getTrackStereoSep(t) - c.stereo_sep)
				if winFocused["Playlist"]:
					cycle_playlist_tools(-1)
				elif winFocused["Piano Roll"]:
					transport.globalTransport(midi.FPT_HZoomJog, -1, midi.PME_System, midi.GT_All)

		if event.data1 == ENCODER_BUTTON:
			event.handled = True
			handle_encoder_button(ENCODER_BUTTON)

		if event.data1 == ENCODER_BUTTON_SHIFTED:
			event.handled = True
			button_id = ENCODER_BUTTON_SHIFTED
			if onButtonClick(button_id):
				transport.globalTransport(midi.FPT_F8, 67)
				ui.setHintMsg("Plugin Picker")
			elif not is_s_series_device():
				cycle_main_windows(1)
			else:
				# S-Series no longer cycles windows on Shift + Press.
				return

		yAxisBtn, xAxisBtn = (
			(ENCODER_Y_S, ENCODER_X_S)
			if device.getName() == "Komplete Kontrol DAW - 1"
			else (ENCODER_Y_A, ENCODER_X_A)
		)

		if event.data1 == xAxisBtn:
			event.handled = True
			if winFocused["Mixer"]:
				if ui.isInPopupMenu():
					if event.data2 == RIGHT_BUTTON:
						ui.right(1)
					elif event.data2 == LEFT_BUTTON:
						ui.left(1)
				else:
					if event.data2 == RIGHT_BUTTON:
						jog(mixer_x_axis_step)
					elif event.data2 == LEFT_BUTTON:
						jog(-mixer_x_axis_step)
			elif winFocused["Channel Rack"]:
				if ui.isInPopupMenu():
					if event.data2 == RIGHT_BUTTON:
						ui.right(1)
					elif event.data2 == LEFT_BUTTON:
						ui.left(1)
				else:
					if event.data2 == RIGHT_BUTTON:
						ui.left(1)
					elif event.data2 == LEFT_BUTTON:
						ui.right(1)
			elif winFocused["Plugin"]:
				if focused_generator_uses_direct_navigation():
					if event.data2 == RIGHT_BUTTON:
						ui.right(1)
						ui.setHintMsg("Right")
					elif event.data2 == LEFT_BUTTON:
						ui.left(1)
						ui.setHintMsg("Left")
				elif event.data2 == RIGHT_BUTTON:
					handle_plugin_nav(1, 7)
				elif event.data2 == LEFT_BUTTON:
					handle_plugin_nav(-1, 7)
			elif winFocused["Playlist"]:
				if event.data2 == RIGHT_BUTTON:
					arrange.jumpToMarker(1, False)
				elif event.data2 == LEFT_BUTTON:
					arrange.jumpToMarker(-1, False)
			elif winFocused["Browser"]:
				if ui.isInPopupMenu():
					if event.data2 == RIGHT_BUTTON:
						ui.right(1)
					elif event.data2 == LEFT_BUTTON:
						ui.left(1)
				else:
					if event.data2 == RIGHT_BUTTON:
						ui.navigateBrowserTabs(midi.FPT_Right)
					elif event.data2 == LEFT_BUTTON:
						ui.navigateBrowserTabs(midi.FPT_Left)
			elif winFocused["Piano Roll"]:
				if ui.isInPopupMenu():
					if event.data2 == RIGHT_BUTTON:
						ui.right()
					elif event.data2 == LEFT_BUTTON:
						ui.left()
				else:
					if event.data2 == RIGHT_BUTTON:
						ui.jog(1)
					elif event.data2 == LEFT_BUTTON:
						ui.jog(-1)
			else:
				if event.data2 == RIGHT_BUTTON:
					ui.right(1)
				elif event.data2 == LEFT_BUTTON:
					ui.left(1)

		if event.data1 == yAxisBtn:
			event.handled = True
			if event.data2 == UP_BUTTON:
				if winFocused["Mixer"]:
					if ui.isInPopupMenu(): 
						ui.up(1)
					else:
						track_index = mixer.trackNumber()
						mixer.revTrackPolarity(track_index)
						ui.setHintMsg("Reverse polarity")
				elif winFocused["Channel Rack"]:
					ui.up(1)
					ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
				elif winFocused["Plugin"]:
					if focused_generator_uses_direct_navigation():
						ui.up(1)
						ui.setHintMsg("Up")
					elif winFocused["Effect Plugin"]:
						idx = mixer.getActiveEffectIndex()
						if not idx:
							return
						mix_track_index, mixer_slot = idx
						if change_plugin_preset(mix_track_index, mixer_slot, -1):
							ui.setHintMsg("Previous preset")
					elif winFocused["Generator Plugin"]:
						channel_index = channels.selectedChannel()
						if change_plugin_preset(channel_index, c.gen_plugin, -1):
							ui.setHintMsg("Previous preset")
						else:
							ui.up()
				elif winFocused["Browser"]:
					if ui.isInPopupMenu():
						ui.up(1)
					else:
						ui.navigateBrowser(midi.FPT_Up, False)
						if config.upDown_preview_sound == 1:
							ui.previewBrowserMenuItem()
						else:
							NILA_Display.OnIdle(self)
				elif winFocused["Playlist"]:
					ui.up()
				elif winFocused["Piano Roll"]:
					ui.up()
			elif event.data2 == DOWN_BUTTON:
				if winFocused["Mixer"]:
					if ui.isInPopupMenu(): 
						ui.down(1)
					else:
						track_index = mixer.trackNumber()
						mixer.swapTrackChannels(track_index)
						ui.setHintMsg("Swap L/R channels")
				elif winFocused["Channel Rack"]:
					ui.down(1)
					ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
				elif winFocused["Plugin"]:
					if focused_generator_uses_direct_navigation():
						ui.down(1)
						ui.setHintMsg("Down")
					elif winFocused["Effect Plugin"]:
						idx = mixer.getActiveEffectIndex()
						if not idx:
							return
						mix_track_index, mixer_slot = idx
						if change_plugin_preset(mix_track_index, mixer_slot, 1):
							ui.setHintMsg("Next preset")
					elif winFocused["Generator Plugin"]:
						channel_index = channels.selectedChannel()
						if change_plugin_preset(channel_index, c.gen_plugin, 1):
							ui.setHintMsg("Next preset")
						else:
							ui.down(1)
				elif winFocused["Browser"]:
					if ui.isInPopupMenu():
						ui.down(1)
					else:
						ui.navigateBrowser(midi.FPT_Down, False)
						if config.upDown_preview_sound == 1:
							ui.previewBrowserMenuItem()
						else:
							NILA_Display.OnIdle(self)
				elif winFocused["Playlist"]:
					ui.down()
				elif winFocused["Piano Roll"]:
					ui.down()
		return
	except RuntimeError:
		return