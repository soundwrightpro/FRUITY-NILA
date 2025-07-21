import time
import arrangement as arrange
import channels
import device
import midi
import mixer
import plugins
import transport
import ui

import nihia

from NILA.NILA_engine import NILA_core, config, constants as c
from NILA.NILA_visuals import NILA_OLED


xAxis, yAxis = 0, 0
windowCycle = 0
last_click_time = 0
current_track_plugin_id = None

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
				mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
				plugin_valid = plugins.isValid(mix_track_index, mixer_slot)
				if not plugin_valid:
					return
				plugin_name_cache = plugins.getPluginName(mix_track_index, mixer_slot, 0, global_index)
				track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
				if track_plugin_id != c.last_plugin_name:
					c.lead_param = 0
					c.last_plugin_name = track_plugin_id
				param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
				param_count = c.actual_param_count if param_count == 4240 else param_count
				if plugin_name_cache in c.unsupported_plugins:
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
				plugin_name_cache = plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index)
				if channels.getChannelType(channel_index) in (0, 3, 4, 5):
					if plugin_name_cache in c.unsupported_plugins:
						ui.down(1) if direction > 0 else ui.up(1)
				else:
					track_plugin_id = plugins.getPluginName(channel_index, c.gen_plugin)
					if track_plugin_id != c.last_plugin_name:
						c.lead_param = 0
						c.last_plugin_name = track_plugin_id
					param_count = plugins.getParamCount(channel_index, c.gen_plugin, global_index)
					param_count = c.actual_param_count if param_count == 4240 else param_count
					if plugin_name_cache in c.unsupported_plugins:
						ui.down(1) if direction > 0 else ui.up(1)
					elif c.actual_param_count > 7:
						target = min if direction > 0 else max
						value = c.lead_param + skip if direction > 0 else c.lead_param - skip
						bound = c.actual_param_count - 7 if direction > 0 else 0
						c.lead_param = target(value, bound)
						NILA_OLED.OnRefresh(self, event)

		def handle_encoder_button(button_id):
			if winFocused["Mixer"]:
				# Only respond to double-click
				if onButtonClick(button_id):
					if ui.isInPopupMenu():
						ui.enter()
						ui.setHintMsg("Enter")
					else:
						transport.globalTransport(midi.FPT_Menu, midi.GT_Menu)
						ui.setHintMsg("Open Menu")
						mixer.deselectAll()
						mixer.selectTrack(mixer.trackNumber())
				return
			elif winFocused["Plugin"] or winFocused["Piano Roll"]:
				ui.enter()
				if onButtonClick(button_id):
					if ui.isInPopupMenu():
						ui.enter()
						ui.setHintMsg("Enter")
					else:
						transport.globalTransport(midi.FPT_Menu, midi.GT_Menu)
						ui.setHintMsg("Open Menu")
						mixer.deselectAll()
						mixer.selectTrack(mixer.trackNumber())
			elif winFocused["Channel Rack"]:
				if onButtonClick(button_id):
					if ui.isInPopupMenu():
						ui.enter()
						ui.setHintMsg("Enter")
					else:
						transport.globalTransport(midi.FPT_ItemMenu, 4)
						ui.setHintMsg("Open Menu")
						mixer.deselectAll()
						mixer.selectTrack(mixer.trackNumber())
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
			nihia.buttons.button_list.get("ENCODER_GENERAL"),
			nihia.buttons.button_list.get("ENCODER_VOLUME_SELECTED")
		):
			plugin_skip = 1
			if event.data2 in (nihia.buttons.button_list.get("RIGHT"), c.mixer_right):
				event.handled = True
				if winFocused["Mixer"]: 
					if ui.isInPopupMenu():
						ui.down(1)
					else:			
						jog(1)
				elif winFocused["Channel Rack"]: jog(1)
				elif winFocused["Plugin"]: handle_plugin_nav(1, plugin_skip)
				elif winFocused["Playlist"]: ui.jog(1)
				elif winFocused["Piano Roll"]: ui.verZoom(-1)
				elif winFocused["Browser"]: browse("next")
				else: ui.down(1)
			elif event.data2 in (nihia.buttons.button_list.get("LEFT"), c.mixer_left):
				event.handled = True
				if winFocused["Mixer"]: 
					if ui.isInPopupMenu():
						ui.up(1)
					else:			
						jog(-1)
				elif winFocused["Channel Rack"]: jog(-1)
				elif winFocused["Plugin"]: handle_plugin_nav(-1, plugin_skip)
				elif winFocused["Playlist"]: ui.jog(-1)
				elif winFocused["Piano Roll"]: ui.verZoom(1)
				elif winFocused["Browser"]: browse("previous")
				else: ui.up(1)

		if event.data1 == nihia.buttons.button_list.get("ENCODER_PAN_SELECTED"):
			if event.data2 in (nihia.buttons.button_list.get("RIGHT"), c.mixer_right):
				event.handled = True
				if winFocused["Mixer"]:
					t = mixer.trackNumber()
					mixer.setTrackStereoSep(t, mixer.getTrackStereoSep(t) + c.stereo_sep)
				if winFocused["Playlist"] or winFocused["Piano Roll"]:
					transport.globalTransport(midi.FPT_HZoomJog, 1, midi.PME_System, midi.GT_All)
			if event.data2 in (nihia.buttons.button_list.get("LEFT"), c.mixer_left):
				event.handled = True
				if winFocused["Mixer"]:
					t = mixer.trackNumber()
					mixer.setTrackStereoSep(t, mixer.getTrackStereoSep(t) - c.stereo_sep)
				if winFocused["Playlist"] or winFocused["Piano Roll"]:
					transport.globalTransport(midi.FPT_HZoomJog, -1, midi.PME_System, midi.GT_All)

		if event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON"):
			event.handled = True
			handle_encoder_button(nihia.buttons.button_list.get("ENCODER_BUTTON"))

		if event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON_SHIFTED"):
			event.handled = True
			button_id = nihia.buttons.button_list.get("ENCODER_BUTTON_SHIFTED")
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
			(nihia.buttons.button_list.get("ENCODER_Y_S"), nihia.buttons.button_list.get("ENCODER_X_S"))
			if device.getName() == "Komplete Kontrol DAW - 1"
			else (nihia.buttons.button_list.get("ENCODER_Y_A"), nihia.buttons.button_list.get("ENCODER_X_A"))
		)

		if event.data1 == xAxisBtn:
			event.handled = True
			if winFocused["Mixer"]:
				if ui.isInPopupMenu():
					if event.data2 == nihia.buttons.button_list.get("RIGHT"):
						ui.right(1)
					elif event.data2 == nihia.buttons.button_list.get("LEFT"):
						ui.left(1)
				else:
					if event.data2 == nihia.buttons.button_list.get("RIGHT"):
						jog(8)
					elif event.data2 == nihia.buttons.button_list.get("LEFT"):
						jog(-8)
			elif winFocused["Channel Rack"]:
				if ui.isInPopupMenu():
					if event.data2 == nihia.buttons.button_list.get("RIGHT"):
						ui.right(1)
					elif event.data2 == nihia.buttons.button_list.get("LEFT"):
						ui.left(1)
				else:
					if event.data2 == nihia.buttons.button_list.get("RIGHT"):
						ui.left(1)
					elif event.data2 == nihia.buttons.button_list.get("LEFT"):
						ui.right(1)
			elif winFocused["Plugin"]:
				if event.data2 == nihia.buttons.button_list.get("RIGHT"):
					handle_plugin_nav(1, 7)
				elif event.data2 == nihia.buttons.button_list.get("LEFT"):
					handle_plugin_nav(-1, 7)
			elif winFocused["Playlist"]:
				if event.data2 == nihia.buttons.button_list.get("RIGHT"):
					arrange.jumpToMarker(1, 0)
				elif event.data2 == nihia.buttons.button_list.get("LEFT"):
					arrange.jumpToMarker(-1, 0)
			elif winFocused["Browser"]:
				if event.data2 == nihia.buttons.button_list.get("RIGHT"):
					ui.right()
				elif event.data2 == nihia.buttons.button_list.get("LEFT"):
					ui.left()
			elif winFocused["Piano Roll"]:
				if ui.isInPopupMenu():
					if event.data2 == nihia.buttons.button_list.get("RIGHT"):
						ui.right()
					elif event.data2 == nihia.buttons.button_list.get("LEFT"):
						ui.left()
				else:
					if event.data2 == nihia.buttons.button_list.get("RIGHT"):
						ui.jog(1)
					elif event.data2 == nihia.buttons.button_list.get("LEFT"):
						ui.jog(-1)
			else:
				if event.data2 == nihia.buttons.button_list.get("RIGHT"):
					ui.right(1)
				elif event.data2 == nihia.buttons.button_list.get("LEFT"):
					ui.left(1)

		if event.data1 == yAxisBtn:
			event.handled = True
			if event.data2 == nihia.buttons.button_list.get("UP"):
				if winFocused["Mixer"]:
					if ui.isInPopupMenu(): ui.up(1)
				elif winFocused["Channel Rack"]:
					ui.up(1)
					ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
				elif winFocused["Plugin"]:
					if winFocused["Effect Plugin"]:
						mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
						param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
						if param_count != 4240:
							plugins.prevPreset(mix_track_index, mixer_slot, global_index)
					elif winFocused["Generator Plugin"]:
						channel_index = channels.selectedChannel()
						if not plugins.isValid(channel_index, c.gen_plugin):
							ui.up()
							return
						if plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index) in c.unsupported_plugins:
							ui.up(1)
						if channels.getChannelName(channel_index) in ui.getFocusedFormCaption():
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
			elif event.data2 == nihia.buttons.button_list.get("DOWN"):
				if winFocused["Mixer"]:
					if ui.isInPopupMenu(): ui.down(1)
				elif winFocused["Channel Rack"]:
					ui.down(1)
					ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
				elif winFocused["Plugin"]:
					if winFocused["Effect Plugin"]:
						mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
						param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
						if param_count != 4240:
							plugins.nextPreset(mix_track_index, mixer_slot, global_index)
					elif winFocused["Generator Plugin"]:
						channel_index = channels.selectedChannel()
						if not plugins.isValid(channel_index, c.gen_plugin):
							ui.down()
							return
						if plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index) in c.unsupported_plugins:
							ui.down(1)
						if channels.getChannelName(channel_index) in ui.getFocusedFormCaption():
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