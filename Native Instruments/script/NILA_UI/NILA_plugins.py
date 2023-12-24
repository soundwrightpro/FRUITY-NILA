import nihia
from script.device_setup import NILA_core, config, constants
from script.screen_writer import NILA_OLED
import channels
import mixer
import ui
import plugins

skip = -1
z = 0
s_series = False

def plugin(self, event):
    """
    Handles plugin control events for the NILA system.

    Args:
        self (object): The instance of the NILA system.
        event (object): The event triggered by the user's input.
    """
    event.handled = True
    if not mixer.getActiveEffectIndex():
        handle_channel_rack_controls(event)
    else:
        track_index, mixer_slot = mixer.getActiveEffectIndex()
 
    # Refresh OLED display
    NILA_OLED.OnRefresh(self, event)

def handle_channel_rack_controls(event):
    """
    Handles controls specific to the Channel Rack.

    Args:
        event (object): The event triggered by the user's input.
    """
    if event.data1 == nihia.mixer.knobs[0][0]:
        handle_volume_control(event)
    elif event.data1 == nihia.mixer.knobs[1][0]:
        handle_pan_control(event)
    else:
        handle_other_controls(event)

def handle_volume_control(event):
    """
    Handles volume control events.

    Args:
        event (object): The event triggered by the user's input.
    """
    if NILA_core.seriesCheck():
        handle_series_volume(event)
    else:
        handle_single_volume(event)

def handle_series_volume(event):
    """
    Handles volume control events for series mode.

    Args:
        event (object): The event triggered by the user's input.
    """
    selected_channel = channels.selectedChannel() + z
    volume_increment = config.increment

    if 65 <= event.data2 < 95 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - volume_increment * 2.5, 2))
    elif 96 <= event.data2 < 128 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - volume_increment, 2))
    elif 0 <= event.data2 < 31:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + volume_increment, 2))
    elif 32 <= event.data2 < 64:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + volume_increment * 2.5, 2))

def handle_single_volume(event):
    """
    Handles volume control events for single mode.

    Args:
        event (object): The event triggered by the user's input.
    """
    selected_channel = channels.selectedChannel() + z
    volume_increment = config.increment

    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - volume_increment, 2))
    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + volume_increment, 2))

def handle_pan_control(event):
    """
    Handles pan control events.

    Args:
        event (object): The event triggered by the user's input.
    """
    selected_channel = channels.selectedChannel() + z
    pan_increment = config.increment

    if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
        channels.setChannelPan(selected_channel, channels.getChannelPan(selected_channel) - pan_increment)
    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
        channels.setChannelPan(selected_channel, channels.getChannelPan(selected_channel) + pan_increment)

def handle_other_controls(event):
    """
    Handles other knob control events.

    Args:
        event (object): The event triggered by the user's input.
    """
    event.handled = any(event.data1 == nihia.mixer.knobs[i][x] for i in range(2) for x in range(8))
