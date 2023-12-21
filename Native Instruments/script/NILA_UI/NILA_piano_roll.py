import nihia
from nihia import mixer as mix
from script.device_setup import config, constants, transform, NILA_core
import channels
import ui

def OnMidiMsg(self, event):
    """
    Handles MIDI messages for the Piano Roll window.

    Args:
        self: The instance of the NILA system.
        event: The MIDI event triggered by the MIDI controller.
    """
    if ui.getFocused(constants.winName["Piano Roll"]):
        handle_knob_0(event)
        handle_knob_1(event)

def handle_knob_0(event):
    """
    Handles events for the first knob.

    Args:
        event: The MIDI event triggered by the first knob.
    """
    if event.data1 == nihia.mixer.knobs[0][0]:
        event.handled = True

        channel_index = 0
        channel_volume = channels.getChannelVolume(channels.selectedChannel() + channel_index)

        if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
            adjust_channel_volume(channel_index, channel_volume, -config.increment)
        elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
            adjust_channel_volume(channel_index, channel_volume, config.increment)

def handle_knob_1(event):
    """
    Handles events for the second knob.

    Args:
        event: The MIDI event triggered by the second knob.
    """
    if event.data1 == nihia.mixer.knobs[1][0]:
        event.handled = True

        channel_index = 0
        channel_pan = channels.getChannelPan(channels.selectedChannel() + channel_index)

        if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
            adjust_channel_pan(channel_index, channel_pan, -config.increment)
        elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
            adjust_channel_pan(channel_index, channel_pan, config.increment)

def adjust_channel_volume(channel_index, current_volume, increment):
    """
    Adjusts the volume of a channel based on the provided increment.

    Args:
        channel_index: Index of the channel to adjust.
        current_volume: Current volume of the channel.
        increment: Amount to adjust the volume.
    """
    updated_volume = round(current_volume + increment, 2)
    channels.setChannelVolume(channels.selectedChannel() + channel_index, updated_volume)
    NILA_core.setTrackVolConvert(channel_index, f"{updated_volume:.1f} dB")
    mix.setTrackName(channel_index, channels.getChannelName(channels.selectedChannel() + channel_index))

def adjust_channel_pan(channel_index, current_pan, increment):
    """
    Adjusts the pan of a channel based on the provided increment.

    Args:
        channel_index: Index of the channel to adjust.
        current_pan: Current pan of the channel.
        increment: Amount to adjust the pan.
    """
    updated_pan = current_pan + increment
    channels.setChannelPan(channels.selectedChannel() + channel_index, updated_pan)
    transform.updatePanChannel(channels.selectedChannel() + channel_index, 0)