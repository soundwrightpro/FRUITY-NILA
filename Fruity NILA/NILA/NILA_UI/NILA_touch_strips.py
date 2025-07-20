import channels
import plugins
import ui

from NILA.NILA_engine import NILA_core, constants as c
from NILA.NILA_visuals import NILA_OLED


def handle_modulation_event(event, data2_normalized: int):
	event.handled = True
	channel = channels.selectedChannel()
	if plugins.isValid(channel):
		value = data2_normalized / c.midi_cc_max
		plugins.setParamValue(
			value,
			c.plugin_param_modulation,
			channel,
			c.global_plugin_slot,  # <-- uses constant, not -1
			c.plugin_param_mode
		)
		ui.setHintMsg(f"Modulation: {round(value * 100)}%")

def handle_expression_event(event, data2_normalized: int):
	event.handled = True
	channel = channels.selectedChannel()
	if plugins.isValid(channel):
		value = data2_normalized / c.midi_cc_max
		param_index = c.plugin_param_expression_base + c.touch_strips["EXPRESSION"]
		plugins.setParamValue(
			value,
			param_index,
			channel,
			c.global_plugin_slot,  # <-- uses constant, not -1
			c.plugin_param_mode
		)
		ui.setHintMsg(f"Expression: {round(value * 100)}%")

def handle_pitch_expression(event):
	lsb = event.data1
	msb = event.data2
	raw = (msb << 7) | lsb
	normalized = (raw - c.midi_pitch_bend_center) / c.midi_pitch_bend_center  # -1.0 to +1.0
	channel = channels.selectedChannel()
	if channel >= 0:
		channels.setChannelPitch(channel, normalized)
		ui.setHintMsg(f"Pitch Bend: {round(normalized * 100)}%")
	event.handled = True

def OnMidiIn(event):
	status = event.status & c.midi_status_mask
	data1 = event.data1
	data2 = event.data2
	mod_touch = c.touch_strips["MOD"]
	exp_touch = c.touch_strips["EXPRESSION"]
	plugin_win = c.winName["Plugin"]

	if status == c.midi_status_pitch_bend:
		handle_pitch_expression(event)
		return

	if ui.getFocused(plugin_win):
		if data1 == mod_touch:
			handle_modulation_event(event, data2)
		elif data1 == exp_touch:
			handle_expression_event(event, data2)
