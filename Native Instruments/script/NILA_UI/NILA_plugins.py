import nihia
from script.device_setup import NILA_core, constants, config
import channels
import mixer
import midi
import general


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
        handle_mixer_effect(event)


def handle_mixer_effect(event):
    """
    Handles control events for the active mixer effect slot mix level for focused plugin on mixer.

    Args:
        event (object): The event triggered by the user's input.
    """
    track_index, mixer_slot = mixer.getActiveEffectIndex()
    track_plugin_id = mixer.getTrackPluginId(track_index, mixer_slot)
    event_id = midi.REC_Plug_MixLevel + track_plugin_id
    mix_slot_volume = general.processRECEvent(event_id, 0, midi.REC_GetValue)

    # Convert mix_slot_volume to the percentage scale [0, 100]
    converted_volume = round((mix_slot_volume / 12800) * 100)

    if event.data1 == nihia.mixer.knobs[0][0]:
        handle_mixer_effect_mix(event, converted_volume, event_id)


def handle_mixer_effect_mix(event, converted_volume, event_id):
    """
    Handles mix level knob control events.

    Args:
        event (object): The event triggered by the user's input.
        converted_volume (float): Current volume converted to the percentage scale.
        event_id (int): Event ID for the mixer plugin.
    """
    volume_increment = config.increment * 100

    if not NILA_core.seriesCheck():
        handle_non_series_knob_event(event, converted_volume, event_id, volume_increment)
    else:
        handle_series_knob_event(event, converted_volume, event_id, volume_increment)


def handle_non_series_knob_event(event, converted_volume, event_id, volume_increment):
    """
    Handles knob events in non-series s devices.

    Args:
        event (object): The event triggered by the user's input.
        converted_volume (float): Current volume converted to the percentage scale.
        event_id (int): Event ID for the mixer plugin.
        volume_increment (float): Increment value for volume change.
    """
    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED and converted_volume - 1 >= 0:
        converted_volume -= volume_increment
    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED and converted_volume + 1 <= 100:
        converted_volume += volume_increment

    update_and_record_volume(event_id, converted_volume)


def handle_series_knob_event(event, converted_volume, event_id, volume_increment):
    """
    Handles knob events in series s devices.

    Args:
        event (object): The event triggered by the user's input.
        converted_volume (float): Current volume converted to the percentage scale.
        event_id (int): Event ID for the mixer plugin.
        volume_increment (float): Increment value for volume change.
    """
    if 65 <= event.data2 < 95:
        if converted_volume - 1 >= 0:
            converted_volume -= volume_increment

    elif 96 <= event.data2 < 128:
        if converted_volume - 1 >= 0:
            converted_volume -= volume_increment

    elif 0 <= event.data2 < 31:
        if converted_volume + 1 <= 100:
            converted_volume += volume_increment

    elif 32 <= event.data2 < 64:
        if converted_volume + 1 <= 100:
            converted_volume += volume_increment

    update_and_record_volume(event_id, converted_volume)


def update_and_record_volume(event_id, converted_volume):
    """
    Update the volume of the mix level on the focused plugin.

    Args:
        event_id (int): Event ID for the mixer plugin.
        converted_volume (float): Current volume converted to the percentage scale.
    """
    mix_slot_volume = round((converted_volume / 100) * 12800)
    general.processRECEvent(event_id, mix_slot_volume, midi.REC_UpdateValue)


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
    Handles volume control events for series S device on the channel rack .

    Args:
        event (object): The event triggered by the user's input.
    """
    selected_channel = channels.selectedChannel()
    volume_increment = config.increment

    if 65 <= event.data2 < 95 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(
            selected_channel, round(channels.getChannelVolume(selected_channel) - volume_increment * 2.5, 2))
    elif 96 <= event.data2 < 128 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - volume_increment, 2))
    elif 0 <= event.data2 < 31:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + volume_increment, 2))
    elif 32 <= event.data2 < 64:
        channels.setChannelVolume(
            selected_channel, round(channels.getChannelVolume(selected_channel) + volume_increment * 2.5, 2))


def handle_single_volume(event):
    """
    Handles volume control events for single mode.

    Args:
        event (object): The event triggered by the user's input.
    """
    selected_channel = channels.selectedChannel()
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
    selected_channel = channels.selectedChannel()
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