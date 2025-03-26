import nihia
from script.device_setup import NILA_core, config, constants as c
from script.screen_writer import NILA_OLED
import arrangement as arrange
import channels
import device
import midi
import mixer
import transport
import plugins
import ui
import time
import math


# Initialize variables for encoder movement on X and Y axes
xAxis, yAxis = 0, 0
windowCycle = 0
last_click_time = 0
current_track_plugin_id = None  # Variable to store the current track_plugin_id

def OnRefresh(self, flags):
	global ordered_tracks

def onButtonClick(button):
	global last_click_time
	
	# Get the current time
	current_time = time.time()

	# Check if it's a double-click
	if (current_time - last_click_time) < config.double_click_speed :  # Adjust the time window as needed
		double_click_status = True
	else:
		double_click_status = False

	# Update the last click time
	last_click_time = current_time

	return double_click_status

# Define the encoder function that handles various events
def encoder(self, event):
	global windowCycle
	global current_track_plugin_id  # Declare current_track_plugin_id as a global variable
	global_index = False
	
	"""
	Handle encoder events for a specific controller.

	Parameters:
		self: The instance of the controller.
		event: The event triggered by the encoder movement.

	Returns:
		None
	"""

	# Define a helper function for jogging in different UI contexts

	def get_mixer_order():
		""" Get mixer tracks sorted by docked position & order of appearance. """
		track_count = mixer.trackCount() - 1  # Exclude Utility
		tracks = []

		for i in range(0, track_count):  # Ignore Utility 
			dock_side = mixer.getTrackDockSide(i)
			tracks.append((dock_side, i))

		# Sort by dock position first, then by track index
		tracks.sort()

		return [t[1] for t in tracks]  # Return only track indices

	def jog(direction):
		""" Scroll through mixer tracks in order of appearance (dock-aware). """

		if ui.getFocused(c.winName["Mixer"]):
			tracks_order = get_mixer_order()  # Get mixer tracks in visual order
			currentTrack = mixer.trackNumber()

			if currentTrack in tracks_order:
				current_idx = tracks_order.index(currentTrack)
			else:
				current_idx = 0  # Default to first track

			# Move left or right in sorted track list
			if direction > 0:  # Right Scroll
				new_idx = (current_idx + 1) % len(tracks_order)  # Wrap around
			else:  # Left Scroll
				new_idx = (current_idx - 1) % len(tracks_order)

			newTrack = tracks_order[new_idx]
			mixer.setTrackNumber(newTrack)

			# **NEW**: Call updated function to ensure proper selection expansion/contraction
			update_mixer_selection(newTrack, tracks_order)
			
		elif ui.getFocused(c.winName["Channel Rack"]):
			ui.jog(direction)
			ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
			ui.setHintMsg("Channel Rack selection rectangle")

	def update_mixer_selection(startTrack, tracks_order):
		""" Dynamically highlights tracks within the same dock section, expanding up to 8, then shrinking. """

		track_count = len(tracks_order)  # Get the total number of mixer tracks
		start_idx = tracks_order.index(startTrack)  # Find the index of the selected track
		start_dock_side = mixer.getTrackDockSide(startTrack)  # Get dock side of the selected track

		selected_tracks = [startTrack]  # Always start with the current track

		# Expand forward (up to 8 tracks) but stop at the end of the dock section
		for i in range(start_idx + 1, track_count):
			track = tracks_order[i]
			if mixer.getTrackDockSide(track) != start_dock_side:  
				break  # Stop when hitting a different dock side
			selected_tracks.append(track)
			if len(selected_tracks) >= 8:  # Stop at max selection
				break

		# If fewer than 8 tracks are available, ensure we expand correctly
		while len(selected_tracks) < 8 and selected_tracks[-1] != tracks_order[-1]:
			next_idx = tracks_order.index(selected_tracks[-1]) + 1
			if next_idx < len(tracks_order) and mixer.getTrackDockSide(tracks_order[next_idx]) == start_dock_side:
				selected_tracks.append(tracks_order[next_idx])
			else:
				break  # Stop expanding if a different dock section starts

		# Apply selection box **only to the selected tracks within the dock section**
		ui.miDisplayRect(selected_tracks[0], selected_tracks[-1], config.rectMixer)

	# Define a helper function for browsing through UI elements
	def browse(action):
		"""
		Browse through UI elements.

		Parameters:
			action: The action to perform during browsing.

		Returns:
			None
		"""
		
		if ui.isInPopupMenu():
			ui.down() if action == "next" else ui.up()
		else:
			ui.next() if action == "next" else ui.previous()
			NILA_OLED.OnIdle(self)
			if config.jog_preview_sound == 1:
				ui.previewBrowserMenuItem()
			elif device.getName() != "Komplete Kontrol DAW - 1":
				NILA_OLED.OnIdle(self)

	# Handle encoder jog wheel events

	if event.data1 in (
		nihia.buttons.button_list.get("ENCODER_GENERAL"),
		nihia.buttons.button_list.get("ENCODER_VOLUME_SELECTED")
	):
		plugin_skip = 1

		if event.data2 in (
			nihia.buttons.button_list.get("RIGHT"),
			c.mixer_right, 
		):
			event.handled = True
			
			if ui.getFocused(c.winName["Mixer"]):
				jog(1)
			elif ui.getFocused(c.winName["Channel Rack"]):
				jog(1)
			elif ui.getFocused(c.winName["Plugin"]):
				if ui.getFocused(c.winName["Effect Plugin"]):
					mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
					track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
					
					if not track_plugin_id == c.last_plugin_name:
						c.lead_param = 0
						c.last_plugin_name = track_plugin_id
										
					if plugins.isValid(mix_track_index, mixer_slot):
						param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
						
						if param_count == 4240:
							param_count = c.actual_param_count
																		
						if plugins.getPluginName(mix_track_index, mixer_slot, 0, global_index) in c.unsupported_plugins:
							ui.down(1)
						else:
							if c.actual_param_count > 7:
								if c.lead_param + 6 != c.actual_param_count:                                        
									c.lead_param = min(c.lead_param + plugin_skip, c.actual_param_count - 7)
									NILA_OLED.OnRefresh(self, event)
								else:
									pass
														
				elif ui.getFocused(c.winName["Generator Plugin"]):
					channel_index = channels.selectedChannel()
					if not plugins.isValid(channel_index, c.gen_plugin):
						return

					if channels.getChannelType(channels.selectedChannel()) in (0, 3, 4, 5):
						if plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index)  in c.unsupported_plugins:
							ui.down(1)
					else:
						channel_index = channels.selectedChannel()
						track_plugin_id = plugins.getPluginName(channel_index, c.gen_plugin)

						if track_plugin_id != c.last_plugin_name:
							c.lead_param = 0
							c.last_plugin_name = track_plugin_id

						if plugins.isValid(channel_index, c.gen_plugin):
							param_count = plugins.getParamCount(channel_index, c.gen_plugin, global_index)

							if param_count == 4240:
								param_count = c.actual_param_count

							if plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index)in c.unsupported_plugins:
								ui.down(1)  # Skip plugin
							else:
								if c.actual_param_count > 7:
									if c.lead_param + 6 != c.actual_param_count:
										c.lead_param = min(c.lead_param + plugin_skip, c.actual_param_count - 7)
										NILA_OLED.OnRefresh(self, event)
									else:
										pass

 
			elif ui.getFocused(c.winName["Playlist"]):
				ui.jog(1)
			elif ui.getFocused(c.winName["Piano Roll"]):
				ui.verZoom(-1)
			elif ui.getFocused(c.winName["Browser"]):
				browse("next")
			else:
				ui.down(1)
				
		elif event.data2 in (
			nihia.buttons.button_list.get("LEFT"),
			c.mixer_left,
		):
			event.handled = True
			if ui.getFocused(c.winName["Mixer"]):
				jog(-1)
			elif ui.getFocused(c.winName["Channel Rack"]):
				jog(-1)
			elif ui.getFocused(c.winName["Plugin"]):
				if ui.getFocused(c.winName["Effect Plugin"]):
					mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
					if plugins.isValid(mix_track_index, mixer_slot):
						track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
						param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
						
						if plugins.getPluginName(mix_track_index, mixer_slot, 0, global_index) in c.unsupported_plugins:
							ui.up(1)
						else:
							if track_plugin_id != current_track_plugin_id:
								c.lead_param = 0  # Reset page number
								current_track_plugin_id = track_plugin_id
							else:
								if c.actual_param_count > 7:
									if c.lead_param >= 0:
										c.lead_param = max(c.lead_param - plugin_skip, 0)
										NILA_OLED.OnRefresh(self, event)
 
				elif ui.getFocused(c.winName["Generator Plugin"]):
					channel_index = channels.selectedChannel()
					if not plugins.isValid(channel_index, c.gen_plugin):
						return
					if channels.getChannelType(channels.selectedChannel()) in (0, 3, 4, 5):
						if plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index) in c.unsupported_plugins:
							ui.up(1)
					else:
						channel_index = channels.selectedChannel()
						track_plugin_id = plugins.getPluginName(channel_index, c.gen_plugin)

						if track_plugin_id != c.last_plugin_name:
							c.lead_param = 0
							c.last_plugin_name = track_plugin_id

						if plugins.isValid(channel_index, c.gen_plugin):
							param_count = plugins.getParamCount(channel_index, c.gen_plugin, global_index)

							if param_count == 4240:
								param_count = c.actual_param_count

							if plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index) in c.unsupported_plugins:
								ui.up(1)  # Skip plugin
							else:
								if c.actual_param_count > 7:
									if c.lead_param >= 0:
										c.lead_param = max(c.lead_param - plugin_skip, 0)
										NILA_OLED.OnRefresh(self, event)
									else:
										pass
				 
			elif ui.getFocused(c.winName["Playlist"]):
				ui.jog(-1)
			elif ui.getFocused(c.winName["Piano Roll"]):
				ui.verZoom(1)
			elif ui.getFocused(c.winName["Browser"]):
				browse("previous")
			else:
				ui.up(1)

	if event.data1 == nihia.buttons.button_list.get("ENCODER_PAN_SELECTED"):
		
		if event.data2 in (
			nihia.buttons.button_list.get("RIGHT"),
			c.mixer_right, 
		):
			event.handled = True
			if ui.getFocused(c.winName["Mixer"]):
				mixer.setTrackStereoSep(mixer.trackNumber(), mixer.getTrackStereoSep(mixer.trackNumber()) + c.stereo_sep)
	
			if ui.getFocused(c.winName["Playlist"]) or ui.getFocused(c.winName["Piano Roll"]):
				transport.globalTransport(midi.FPT_HZoomJog, 1, midi.PME_System, midi.GT_All)
	
		if event.data2 in (
			nihia.buttons.button_list.get("LEFT"),
			c.mixer_left, 
		):
			event.handled = True
			if ui.getFocused(c.winName["Mixer"]):
				mixer.setTrackStereoSep(mixer.trackNumber(), mixer.getTrackStereoSep(mixer.trackNumber()) - c.stereo_sep)
			
			if ui.getFocused(c.winName["Playlist"]) or ui.getFocused(c.winName["Piano Roll"]):
				transport.globalTransport(midi.FPT_HZoomJog, -1, midi.PME_System, midi.GT_All)


	if event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON"):
		event.handled = True
		button_id = nihia.buttons.button_list.get("ENCODER_BUTTON")

		if ui.getFocused(c.winName["Mixer"]) or ui.getFocused(c.winName["Plugin"]) or ui.getFocused(c.winName["Piano Roll"]):
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
					
		elif ui.getFocused(c.winName["Channel Rack"]):
			if onButtonClick(button_id):
				if ui.isInPopupMenu():
					ui.enter()
					ui.setHintMsg("Enter")
				else:
					transport.globalTransport(midi.FPT_ItemMenu, 4) #'/Applications/FL Studio 21.app/Contents/Libs/../Resources/FL/Shared/Python/Lib/midi.py'>
					ui.setHintMsg("Open Menu")
					mixer.deselectAll()
					mixer.selectTrack(mixer.trackNumber())

		elif ui.getFocused(c.winName["Playlist"]):
			if onButtonClick(button_id) and not ui.isInPopupMenu():
				arrange.addAutoTimeMarker(mixer.getSongTickPos(), str("Mark"))

		elif ui.getFocused(c.winName["Browser"]):
			if onButtonClick(button_id):
				if ui.getFocusedNodeFileType() <= -100:
					ui.enter()
					ui.setHintMsg("Enter")
				else:
					ui.selectBrowserMenuItem()
					ui.setHintMsg("Open menu")
		else:
			ui.enter()
			
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

		

	if device.getName() == "Komplete Kontrol DAW - 1":
		yAxis, xAxis = nihia.buttons.button_list.get("ENCODER_Y_S"), nihia.buttons.button_list.get("ENCODER_X_S")
	else:
		yAxis, xAxis = nihia.buttons.button_list.get("ENCODER_Y_A"), nihia.buttons.button_list.get("ENCODER_X_A")

	if event.data1 == xAxis:
		event.handled = True
		if event.data2 == nihia.buttons.button_list.get("RIGHT"):
			if ui.getFocused(c.winName["Mixer"]):
				ui.right(1) if ui.isInPopupMenu() else jog(8)
				
			elif ui.getFocused(c.winName["Channel Rack"]):
				ui.right(1) if ui.isInPopupMenu() else ui.left(1)
				
			elif ui.getFocused(c.winName["Plugin"]):
				if ui.getFocused(c.winName["Effect Plugin"]):
					plugin_skip = 7
					mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
					track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
					
					if not track_plugin_id == c.last_plugin_name:
						c.lead_param = 0
						c.last_plugin_name = track_plugin_id
										
					if plugins.isValid(mix_track_index, mixer_slot):
						param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
						
						if param_count == 4240:
							param_count = c.actual_param_count
																		
						if plugins.getPluginName(mix_track_index, mixer_slot, 0, global_index) in c.unsupported_plugins:
							ui.down(1)
						else:
							if c.actual_param_count > 7:
								if c.lead_param + 6 != c.actual_param_count:                                        
									c.lead_param = min(c.lead_param + plugin_skip, c.actual_param_count - 7)
									NILA_OLED.OnRefresh(self, event)
								else:
									pass

				elif ui.getFocused(c.winName["Generator Plugin"]):
					plugin_skip = 7
					channel_index = channels.selectedChannel()
					if not plugins.isValid(channel_index, c.gen_plugin):
						return
					track_plugin_id = plugins.getPluginName(channel_index, c.gen_plugin)

					if not track_plugin_id == c.last_plugin_name:
						c.lead_param = 0
						c.last_plugin_name = track_plugin_id

					if plugins.isValid(channel_index, c.gen_plugin):
						param_count = plugins.getParamCount(channel_index, c.gen_plugin, global_index)

						if param_count == 4240:
							param_count = c.actual_param_count

						if plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index) in c.unsupported_plugins:
							ui.right(1)
						else:
							if c.actual_param_count > 7:
								if c.lead_param + 6 != c.actual_param_count:
									c.lead_param = min(c.lead_param + plugin_skip, c.actual_param_count - 7)
									NILA_OLED.OnRefresh(self, event)
								else:
									pass


				else:
					ui.right(1)
				
			elif ui.getFocused(c.winName["Playlist"]):
				arrange.jumpToMarker(1, 0)
				
			elif ui.getFocused(c.winName["Browser"]):
				ui.right()
				
			elif ui.getFocused(c.winName["Piano Roll"]):
				ui.right() if ui.isInPopupMenu() else ui.jog(1)
			else:
				ui.right(1)
				

		elif event.data2 == nihia.buttons.button_list.get("LEFT"):
			if ui.getFocused(c.winName["Mixer"]):
				ui.left(1) if ui.isInPopupMenu() else jog(-8)
				
			elif ui.getFocused(c.winName["Channel Rack"]):
				ui.left(1) if ui.isInPopupMenu() else ui.right(1)
				
			elif ui.getFocused(c.winName["Plugin"]):
				if ui.getFocused(c.winName["Effect Plugin"]):
					plugin_skip = 7
					mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
					if plugins.isValid(mix_track_index, mixer_slot):
						track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
						param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
						
						if plugins.getPluginName(mix_track_index, mixer_slot, 0, global_index) in c.unsupported_plugins:
							ui.up(1)
						else:
							if track_plugin_id != current_track_plugin_id:
								c.lead_param = 0  # Reset page number
								current_track_plugin_id = track_plugin_id
							else:
								if c.actual_param_count > 7:
									if c.lead_param >= 0:
										c.lead_param = max(c.lead_param - plugin_skip, 0)
										NILA_OLED.OnRefresh(self, event)

				elif ui.getFocused(c.winName["Generator Plugin"]):
					plugin_skip = 7
					channel_index = channels.selectedChannel()
					if not plugins.isValid(channel_index, c.gen_plugin):
						return

					if plugins.isValid(channel_index, c.gen_plugin):
						track_plugin_id = plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index)
						param_count = plugins.getParamCount(channel_index, c.gen_plugin, global_index)

						if plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index) in c.unsupported_plugins:
							ui.left(1)
						else:
							if track_plugin_id != current_track_plugin_id:
								c.lead_param = 0  # Reset page number
								current_track_plugin_id = track_plugin_id
							else:
								if c.actual_param_count > 7:
									if c.lead_param >= 0:
										c.lead_param = max(c.lead_param - plugin_skip, 0)
										NILA_OLED.OnRefresh(self, event)
				else:
					ui.left(1)
				
			elif ui.getFocused(c.winName["Playlist"]):
				arrange.jumpToMarker(-1, 0)
				
			elif ui.getFocused(c.winName["Browser"]):
				ui.left()
				
			elif ui.getFocused(c.winName["Piano Roll"]):
				ui.left() if ui.isInPopupMenu() else ui.jog(-1)
				
			else:
				ui.left(1)

	if event.data1 == yAxis:
		event.handled = True
		if event.data2 == nihia.buttons.button_list.get("UP"):
			if ui.getFocused(c.winName["Mixer"]):
				ui.up(1) if ui.isInPopupMenu() else None
			elif ui.getFocused(c.winName["Channel Rack"]):
				ui.up(1)
				ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
			elif ui.getFocused(c.winName["Plugin"]):
				if ui.getFocused(c.winName["Effect Plugin"]): 
					mix_track_index, mixer_slot = mixer.getActiveEffectIndex() 
					param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
						
					if param_count != 4240:
						plugins.prevPreset(mix_track_index, mixer_slot, global_index)
						
				elif ui.getFocused(c.winName["Generator Plugin"]): 
					channel_index = channels.selectedChannel()
					if not plugins.isValid(channel_index, c.gen_plugin):
						ui.up()  # Fallback action
						return
					if plugins.getPluginName(channel_index, c.gen_plugin,0 ,global_index) in c.unsupported_plugins:
						
						ui.up(1)
					if channels.getChannelName(channel_index) in ui.getFocusedFormCaption():
						plugins.prevPreset(channel_index)
					else:
						ui.up()

			elif ui.getFocused(c.winName["Browser"]):
				ui.up() if ui.isInPopupMenu() else ui.previous()
				if config.upDown_preview_sound == 1 and device.getName() != "Komplete Kontrol DAW - 1":
					ui.previewBrowserMenuItem()
				elif device.getName() != "Komplete Kontrol DAW - 1":
					NILA_OLED.OnIdle(self)
			elif ui.getFocused(c.winName["Playlist"]):
				ui.up()
			elif ui.getFocused(c.winName["Piano Roll"]):
				ui.up()

		elif event.data2 == nihia.buttons.button_list.get("DOWN"):
			if ui.getFocused(c.winName["Mixer"]):
				ui.down(1) if ui.isInPopupMenu() else None
			elif ui.getFocused(c.winName["Channel Rack"]):
				ui.down(1)
				ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
			elif ui.getFocused(c.winName["Plugin"]):
				if ui.getFocused(c.winName["Effect Plugin"]): 
					mix_track_index, mixer_slot = mixer.getActiveEffectIndex() 
					param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)

					if param_count != 4240:
						plugins.nextPreset(mix_track_index, mixer_slot, global_index)
						
				elif ui.getFocused(c.winName["Generator Plugin"]): 
					channel_index = channels.selectedChannel()
					if not plugins.isValid(channel_index, c.gen_plugin):
						ui.down()  # Fallback action
						return
					if plugins.getPluginName(channel_index, c.gen_plugin, 0, global_index)in c.unsupported_plugins:
						ui.down(1)
					if channels.getChannelName(channel_index) in ui.getFocusedFormCaption():
						plugins.nextPreset(channel_index)
					else:
						ui.down(1)

			elif ui.getFocused(c.winName["Browser"]):
				ui.down() if ui.isInPopupMenu() else ui.next()
				if config.upDown_preview_sound == 1 and device.getName() != "Komplete Kontrol DAW - 1":
					ui.previewBrowserMenuItem()
				elif device.getName() != "Komplete Kontrol DAW - 1":
					NILA_OLED.OnIdle(self)
			elif ui.getFocused(c.winName["Playlist"]):
				ui.down()
			elif ui.getFocused(c.winName["Piano Roll"]):
				ui.down()
	return