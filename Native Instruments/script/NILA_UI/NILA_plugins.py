import nihia
from nihia import mixer as mix
from script.device_setup import NILA_core as core, config, constants
from script.screen_writer import NILA_OLED as oled
import channels
import ui

skip = -1
z = 0
s_series = False

def plugin(self, event):
    """
    Handles plugin control events for the NILA system.

    Args:
        self: The instance of the NILA system.
        event: The event triggered by the user's input.
    """
    # Check if the focused window is the Plugin window
    if ui.getFocused(constants.winName["Plugin"]) == 1:
        # Handle knob events for volume and pan control
        if event.data1 == nihia.mixer.knobs[0][0]:
            handle_volume_control(event)
        elif event.data1 == nihia.mixer.knobs[1][0]:
            handle_pan_control(event)
        else:
            handle_other_controls(event)

    # Refresh OLED display
    oled.OnRefresh(self, event)

def handle_volume_control(event):
    """
    Handles volume control events.

    Args:
        event: The event triggered by the user's input.
    """
    event.handled = True

    if core.seriesCheck():
        handle_series_volume(event.data2)
    else:
        handle_single_volume(event.data2)

def handle_series_volume(data2):
    """
    Handles volume control events for series mode.

    Args:
        data2: The value of the event data2.
    """
    selected_channel = channels.selectedChannel() + z

    if 65 <= data2 < 95 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - config.increment * 2.5, 2))
    elif 96 <= data2 < 128 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - config.increment, 2))
    elif 0 <= data2 < 31:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + config.increment, 2))
    elif 32 <= data2 < 64:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + config.increment * 2.5, 2))

def handle_single_volume(data2):
    """
    Handles volume control events for single mode.

    Args:
        data2: The value of the event data2.
    """
    selected_channel = channels.selectedChannel() + z

    if data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - config.increment, 2))
    elif data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + config.increment, 2))

def handle_pan_control(event):
    """
    Handles pan control events.

    Args:
        event: The event triggered by the user's input.
    """
    event.handled = True
    selected_channel = channels.selectedChannel() + z

    if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
        channels.setChannelPan(selected_channel, channels.getChannelPan(selected_channel) - config.increment)
    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
        channels.setChannelPan(selected_channel, channels.getChannelPan(selected_channel) + config.increment)

def handle_other_controls(event):
    """
    Handles other knob control events.

    Args:
        event: The event triggered by the user's input.
    """
    event.handled = any(event.data1 == nihia.mixer.knobs[i][x] for i in range(2) for x in range(8))
