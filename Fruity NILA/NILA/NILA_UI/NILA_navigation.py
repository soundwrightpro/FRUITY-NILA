import time
import arrangement as arrange
import channels
import device
import midi
import mixer
import plugins
import transport
import ui

import nihia.buttons as buttons

from NILA.NILA_engine import config, constants as c
from NILA.NILA_visuals import NILA_OLED


xAxis, yAxis = 0, 0
windowCycle = 0
last_click_time = 0
current_track_plugin_id = None

BUTTONS = buttons.button_list
UNSUPPORTED_PLUGINS = tuple(c.unsupported_plugins or ())


def _button(name):
	return BUTTONS[name]


ENCODER_GENERAL = _button("ENCODER_GENERAL")
ENCODER_VOLUME_SELECTED = _button("ENCODER_VOLUME_SELECTED")
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


def _popup_enter_or_open_menu(menu_transport, menu_hint):
	if ui.isInPopupMenu():
		ui.enter()
		ui.setHintMsg("Enter")
	else:
		transport.globalTransport(menu_transport, menu_hint)
		ui.setHintMsg("Open Menu")
		mixer.deselectAll()
		mixer.selectTrack(mixer.trackNumber())

def OnRefresh(self, flags):
	global ordered_tracks

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
		global_index = False

		def get_mixer_order():
			tc = mixer.trackCount() - 1
			return [i for _, i in sorted((mixer.getTrackDockSide(i), i) for i in range(tc))]

		def jog(direction):
			winMixer = ui.getFocused(c.winName["Mixer"])
			winChan = ui.getFocused(c.winName["Channel Rack"])
			if winMixer:
				tracks_order = get_mixer_order()
				currentTrack = mixer.trackNumber()
				try:
					current_idx = tracks_order.index(currentTrack)
				except ValueError:
					current_idx = 0
				new_idx = (current_idx + direction) % len(tracks_order)
				newTrack = tracks_order[new_idx]
				mixer.setTrackNumber(newTrack)
				update_mixer_selection(newTrack, tracks_order)
			elif winChan:
				ui.jog(direction)
				ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
				ui.setHintMsg("Channel Rack selection rectangle")

		def update_mixer_selection(startTrack, tracks_order):
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

		def browse(action):
			if ui.isInPopupMenu():
				if action == "next":
					ui.down()
				else:
					ui.up()
			else:
				if action == "next":
					ui.next()
				else:
					ui.previous()
				NILA_OLED.OnIdle(self)
				if config.jog_preview_sound == 1:
					ui.previewBrowserMenuItem()
				elif device.getName() != "Komplete Kontrol DAW - 1":
					NILA_OLED.OnIdle(self)

		# --- Begin event handling ---
		winFocused = {name: ui.getFocused(c.winName[name]) for name in (
			"Mixer", "Channel Rack", "Plugin", "Effect Plugin", "Generator Plugin", "Playlist", "Browser", "Piano Roll"
		)}

		def handle_plugin_nav(direction, skip):
			global current_track_plugin_id
			plugin_name_cache = None
			if winFocused["Effect Plugin"]:
				idx = mixer.getActiveEffectIndex()
				if not idx:
					return
				mix_track_index, mixer_slot = idx
				plugin_valid = plugins.isValid(mix_track_index, mixer_slot)
				if not plugin_valid:
					return
				plugin_name_cache = plugins.getPluginName(mix_track_index, mixer_slot, False, global_index)
				track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
				if track_plugin_id != c.last_plugin_name:
					c.lead_param = 0
					c.last_plugin_name = track_plugin_id
				param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
				param_count = c.actual_param_count if param_count == 4240 else param_count
				if plugin_name_cache in UNSUPPORTED_PLUGINS:
					ui.down(1) if direction > 0 else ui.up(1)
				elif c.actual_param_count > 7:
					target = min if direction > 0 else max
					value = c.lead_param + skip if direction > 0 else c.lead_param - skip
					bound = c.actual_param_count - 7 if direction > 0 else 0
					c.lead_param = target(value, bound)
					NILA_OLED.OnRefresh(self, event)
			elif winFocused["Generator Plugin"]:
				channel_index = channels.selectedChannel()
				if not plugins.isValid(channel_index, c.gen_plugin):
					return
				plugin_name_cache = plugins.getPluginName(channel_index, c.gen_plugin, False, global_index)
				if channels.getChannelType(channel_index) in (0, 3, 4, 5):
					if plugin_name_cache in UNSUPPORTED_PLUGINS:
						ui.down(1) if direction > 0 else ui.up(1)
				else:
					track_plugin_id = plugins.getPluginName(channel_index, c.gen_plugin)
					if track_plugin_id != c.last_plugin_name:
						c.lead_param = 0
						c.last_plugin_name = track_plugin_id
					param_count = plugins.getParamCount(channel_index, c.gen_plugin, global_index)
					param_count = c.actual_param_count if param_count == 4240 else param_count
					if plugin_name_cache in UNSUPPORTED_PLUGINS:
						ui.down(1) if direction > 0 else ui.up(1)
					elif c.actual_param_count > 7:
						target = min if direction > 0 else max
						value = c.lead_param + skip if direction > 0 else c.lead_param - skip
						bound = c.actual_param_count - 7 if direction > 0 else 0
						c.lead_param = target(value, bound)
						NILA_OLED.OnRefresh(self, event)

		def handle_encoder_button(button_id):
			if winFocused["Mixer"]:
				if onButtonClick(button_id):
					_popup_enter_or_open_menu(midi.FPT_Menu, midi.GT_Menu)
				return
			elif winFocused["Plugin"] or winFocused["Piano Roll"]:
				ui.enter()
				if onButtonClick(button_id):
					_popup_enter_or_open_menu(midi.FPT_Menu, midi.GT_Menu)
			elif winFocused["Channel Rack"]:
				if onButtonClick(button_id):
					_popup_enter_or_open_menu(midi.FPT_ItemMenu, 4)
			elif winFocused["Playlist"]:
				if onButtonClick(button_id) and not ui.isInPopupMenu():
					arrange.addAutoTimeMarker(mixer.getSongTickPos(), str("Mark"))
			elif winFocused["Browser"]:
				if onButtonClick(button_id):
					if ui.getFocusedNodeFileType() <= -100:
						ui.enter()
						ui.setHintMsg("Enter")
					else:
						ui.selectBrowserMenuItem()
						ui.setHintMsg("Open menu")
			else:
				ui.enter()

		# --- ENCODER HANDLING ---
		if event.data1 in (
			ENCODER_GENERAL,
			ENCODER_VOLUME_SELECTED
		):
			plugin_skip = 1
			if event.data2 in (RIGHT_BUTTON, c.mixer_right):
				event.handled = True
				if winFocused["Mixer"]: 
					if ui.isInPopupMenu():
						ui.down(1)
					else:			
						jog(1)
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
						jog(-1)
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
			if event.data2 in (RIGHT_BUTTON, c.mixer_right):
				event.handled = True
				if winFocused["Mixer"]:
					t = mixer.trackNumber()
					mixer.setTrackStereoSep(t, mixer.getTrackStereoSep(t) + c.stereo_sep)
				if winFocused["Playlist"] or winFocused["Piano Roll"]:
					transport.globalTransport(midi.FPT_HZoomJog, 1, midi.PME_System, midi.GT_All)
			if event.data2 in (LEFT_BUTTON, c.mixer_left):
				event.handled = True
				if winFocused["Mixer"]:
					t = mixer.trackNumber()
					mixer.setTrackStereoSep(t, mixer.getTrackStereoSep(t) - c.stereo_sep)
				if winFocused["Playlist"] or winFocused["Piano Roll"]:
					transport.globalTransport(midi.FPT_HZoomJog, -1, midi.PME_System, midi.GT_All)

		if event.data1 == ENCODER_BUTTON:
			event.handled = True
			handle_encoder_button(ENCODER_BUTTON)

		if event.data1 == ENCODER_BUTTON_SHIFTED:
			event.handled = True
			button_id = ENCODER_BUTTON_SHIFTED
			window_mappings = {
				0: (1, "Channel Rack"),
				1: (0, "Mixer"),
				2: (2, "Playlist"),
				3: (4, "Browser")
			}
			if onButtonClick(button_id):
				transport.globalTransport(midi.FPT_F8, 67)
				ui.setHintMsg("Plugin Picker")
			else:
				window, hint_msg = window_mappings[windowCycle]
				ui.showWindow(window)
				windowCycle = (windowCycle + 1) % 4
				ui.setHintMsg(hint_msg)

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
						jog(8)
					elif event.data2 == LEFT_BUTTON:
						jog(-8)
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
				if event.data2 == RIGHT_BUTTON:
					handle_plugin_nav(1, 7)
				elif event.data2 == LEFT_BUTTON:
					handle_plugin_nav(-1, 7)
			elif winFocused["Playlist"]:
				if event.data2 == RIGHT_BUTTON:
					arrange.jumpToMarker(1, False)
				elif event.data2 == LEFT_BUTTON:
					arrange.jumpToMarker(-1, False)
			elif winFocused["Browser"]:
				if event.data2 == RIGHT_BUTTON:
					ui.right()
				elif event.data2 == LEFT_BUTTON:
					ui.left()
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
				elif winFocused["Channel Rack"]:
					ui.up(1)
					ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
				elif winFocused["Plugin"]:
					if winFocused["Effect Plugin"]:
						idx = mixer.getActiveEffectIndex()
						if not idx:
							return
						mix_track_index, mixer_slot = idx
						param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
						if param_count != 4240:
							plugins.prevPreset(mix_track_index, mixer_slot, global_index)
					elif winFocused["Generator Plugin"]:
						channel_index = channels.selectedChannel()
						if not plugins.isValid(channel_index, c.gen_plugin):
							ui.up()
							return
						if plugins.getPluginName(channel_index, c.gen_plugin, False, global_index) in UNSUPPORTED_PLUGINS:
							ui.up(1)
						focused_caption = str(ui.getFocusedFormCaption() or "")
						channel_name = str(channels.getChannelName(channel_index) or "")
						if channel_name in focused_caption:
							plugins.prevPreset(channel_index)
						else:
							ui.up()
				elif winFocused["Browser"]:
					ui.up() if ui.isInPopupMenu() else ui.previous()
					if config.upDown_preview_sound == 1 and device.getName() != "Komplete Kontrol DAW - 1":
						ui.previewBrowserMenuItem()
					elif device.getName() != "Komplete Kontrol DAW - 1":
						NILA_OLED.OnIdle(self)
				elif winFocused["Playlist"]:
					ui.up()
				elif winFocused["Piano Roll"]:
					ui.up()
			elif event.data2 == DOWN_BUTTON:
				if winFocused["Mixer"]:
					if ui.isInPopupMenu(): 
						ui.down(1)
				elif winFocused["Channel Rack"]:
					ui.down(1)
					ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
				elif winFocused["Plugin"]:
					if winFocused["Effect Plugin"]:
						idx = mixer.getActiveEffectIndex()
						if not idx:
							return
						mix_track_index, mixer_slot = idx
						param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
						if param_count != 4240:
							plugins.nextPreset(mix_track_index, mixer_slot, global_index)
					elif winFocused["Generator Plugin"]:
						channel_index = channels.selectedChannel()
						if not plugins.isValid(channel_index, c.gen_plugin):
							ui.down()
							return
						if plugins.getPluginName(channel_index, c.gen_plugin, False, global_index) in UNSUPPORTED_PLUGINS:
							ui.down(1)
						focused_caption = str(ui.getFocusedFormCaption() or "")
						channel_name = str(channels.getChannelName(channel_index) or "")
						if channel_name in focused_caption:
							plugins.nextPreset(channel_index)
						else:
							ui.down(1)
				elif winFocused["Browser"]:
					ui.down() if ui.isInPopupMenu() else ui.next()
					if config.upDown_preview_sound == 1 and device.getName() != "Komplete Kontrol DAW - 1":
						ui.previewBrowserMenuItem()
					elif device.getName() != "Komplete Kontrol DAW - 1":
						NILA_OLED.OnIdle(self)
				elif winFocused["Playlist"]:
					ui.down()
				elif winFocused["Piano Roll"]:
					ui.down()
		return
	except RuntimeError:
		return