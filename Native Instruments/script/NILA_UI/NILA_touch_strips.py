from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED
from script.device_setup import constants

import channels
import plugins
import ui

def handle_modulation_event(event, data2_normalized):
	"""Handles modulation input from the modulation touch strip and sets the plugin modulation parameter."""
	event.handled = True
	channel = channels.selectedChannel()
	if plugins.isValid(channel):
		value = (data2_normalized / 127 / 10) / 0.50 / 2 * 10
		plugins.setParamValue(value, 4097, channel, -1, 2)
		ui.setHintMsg(f"Modulation: {round(data2_normalized / 1.27)}")

def handle_expression_event(event, data2_normalized):
	"""Handles expression input from the expression touch strip and sets the plugin expression parameter."""
	event.handled = True
	channel = channels.selectedChannel()
	if plugins.isValid(channel):
		value = (data2_normalized / 127 / 10) / 0.50 / 2 * 10
		plugins.setParamValue(value, 4096 + constants.touch_strips["EXPRESSION"], channel, -1, 2)
		ui.setHintMsg(f"Expression: {round(data2_normalized / 1.27)}")

def handle_pitch_expression(event):
	"""Handles pitch bend messages and applies pitch changes to the selected channel."""
	lsb = event.data1
	msb = event.data2
	raw = (msb << 7) | lsb         # 0–16383
	normalized = (raw - 8192) / 8192  # -1.0 to +1.0
	channel = channels.selectedChannel()
	if channel >= 0:
		channels.setChannelPitch(channel, normalized)
		ui.setHintMsg(f"Pitch Bend: {round(normalized * 100)}%")
	event.handled = True

def OnMidiIn(event):
	"""Main MIDI input handler. Routes incoming MIDI events to pitch, modulation, or expression handlers."""
	status = event.status & 0xF0
	data1 = event.data1
	data2 = event.data2

	mod_touch_strip = constants.touch_strips["MOD"]
	exp_touch_strip = constants.touch_strips["EXPRESSION"]
	plugin_win_name = constants.winName["Plugin"]

	# Handle pitch bend messages separately
	if status == 0xE0:
		handle_pitch_expression(event)
		return

	# Handle CC messages
	if data1 == mod_touch_strip or data1 == exp_touch_strip:
		event.handled = True

	if ui.getFocused(plugin_win_name):
		if data1 == mod_touch_strip:
			handle_modulation_event(event, data2)
		elif data1 == exp_touch_strip:
			handle_expression_event(event, data2)
