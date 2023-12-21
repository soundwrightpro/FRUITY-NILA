from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED
from script.device_setup import constants

import channels
import plugins
import ui 

def handle_modulation_event(event, data2_normalized):
    """
    Handles modulation events for a MIDI controller.

    Args:
        event: The event triggered by the modulation input.
        data2_normalized: The normalized value of the modulation input (0 to 1).
    """
    event.handled = True
    channel = channels.selectedChannel()

    # Check if the channel is valid for modulation
    if plugins.isValid(channel):
        # Calculate the value based on the normalized input and set the plugin parameter
        value = (data2_normalized / 127 / 10) / 0.50 / 2 * 10
        plugins.setParamValue(value, 4097, channel, -1, 2)
        ui.setHintMsg(f"Modulation: {round(data2_normalized / 1.27)}")

def handle_expression_event(event, data2_normalized):
    """
    Handles expression events for a MIDI controller.

    Args:
        event: The event triggered by the expression input.
        data2_normalized: The normalized value of the expression input (0 to 1).
    """
    event.handled = True
    channel = channels.selectedChannel()

    # Check if the channel is valid for expression control
    if plugins.isValid(channel):
        # Set the plugin parameter based on the normalized input
        plugins.setParamValue(data2_normalized, 4096 + constants.touch_strips["EXPRESSION"], channel, -1, 2)
        ui.setHintMsg(f"Expression: {round(data2_normalized / 1.27)}")

def OnMidiIn(event):
    """
    Handles MIDI input events for the NILA system.

    Args:
        event: The MIDI input event triggered by the MIDI controller.
    """
    data1 = event.data1
    data2_normalized = event.data2 

    mod_touch_strip = constants.touch_strips["MOD"]
    exp_touch_strip = constants.touch_strips["EXPRESSION"]
    plugin_win_name = constants.winName["Plugin"]

    # Check if the MIDI input is related to modulation or expression
    if data1 == mod_touch_strip or data1 == exp_touch_strip:
        event.handled = True

    # Check if the Plugin window is in focus
    if ui.getFocused(plugin_win_name):
        # Route the MIDI input to the appropriate handling function
        if data1 == mod_touch_strip:
            handle_modulation_event(event, data2_normalized)
        elif data1 == exp_touch_strip:
            handle_expression_event(event, data2_normalized)