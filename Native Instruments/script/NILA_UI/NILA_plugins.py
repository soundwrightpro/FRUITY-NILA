import nihia
from script.device_setup import NILA_core, constants as c, config
from script.screen_writer import NILA_OLED
import channels
import mixer
import midi
import general
import time
import ui
import plugins

def plugin(self, event):
    """
    Handles plugin-related events and delegates control to the appropriate function.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.

    Returns:
    None
    """
    if ui.getFocused(c.winName["Plugin"]):
        if ui.getFocused(c.winName["Generator Plugin"]):
            handle_channel_rack_controls(self, event)
        else:
            handle_mixer_effect(self, event)
        plugin_set_param(self, event)

def plugin_set_param(self, event, mixer_slot=-1):
    """
    Sets parameters for the plugin based on the focused window.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.
    - mixer_slot: The mixer slot to set parameters for.

    Returns:
    None
    """
    use_global_index = False

    if ui.getFocused(c.winName["Effect Plugin"]):
        track_index, mixer_slot = mixer.getActiveEffectIndex()
        full_plugin_name = plugins.getPluginName(track_index, mixer_slot)

    if full_plugin_name not in c.unsupported_plugins:
        mix_track_index, mixer_slot = mixer.getActiveEffectIndex()

        c.param_offset = max(c.skip_over, 0)

        if c.actual_param_count > 0:
            for knob_number in range(1, min(c.actual_param_count, 8 + c.param_offset)):
                param_index = max(min(knob_number - 1 + c.lead_param, c.actual_param_count - 1), 0)
                param_name = plugins.getParamName(param_index, mix_track_index, mixer_slot, use_global_index)

                if param_name not in c.unsupported_param:
                    knob_number = max(1, min(knob_number - c.skip_over, 7))
                    knob_data = nihia.mixer.knobs[0][knob_number]
                    volume_increment = config.increment

                    if event.data1 == knob_data:
                        adjusted_increment = knob_time_check(self, volume_increment)
                        handle_param_control(self, event, param_index, mix_track_index, mixer_slot,
                                            use_global_index, adjusted_increment, param_name)


    elif ui.getFocused(c.winName["Generator Plugin"]):
        chan_track_index = channels.selectedChannel()
        plugins.getParamCount(chan_track_index, mixer_slot, use_global_index)

def send_hint_message(parameter_name):
    """
    Sends a hint message with a formatted parameter name.

    Parameters:
    - parameter_name: The parameter name to be formatted.

    Returns:
    None
    """
    result = parameter_name[0]
    for i in range(1, len(parameter_name)):
        if parameter_name[i].isupper() and parameter_name[i - 1] != ' ':
            result += ' ' + parameter_name[i]
        elif parameter_name[i] == '/' and i < len(parameter_name) - 1 and parameter_name[i + 1] != ' ':
            result += ' /'
        else:
            result += parameter_name[i]

    ui.setHintMsg(result)

def handle_param_control(self, event, param_index, mix_track_index, mixer_slot, use_global_index, volume_increment, param_name):
    """
    Handles parameter control events for plugins.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.
    - param_index: The index of the parameter to be controlled.
    - mix_track_index: The mixer track index.
    - mixer_slot: The mixer slot.
    - use_global_index: Indicates whether to use the global index.
    - volume_increment: The increment for parameter control.
    - param_name: The name of the parameter.

    Returns:
    None
    """
    pickup_mode = 0
    param_value = plugins.getParamValue(param_index, mix_track_index, mixer_slot, use_global_index)
    percentage = param_value * 100
    new_param_value = 0

    if NILA_core.seriesCheck():
        if 65 <= event.data2 < 95 or 96 <= event.data2 < 128:
            new_param_value = max(param_value - volume_increment, 0)
        elif 0 <= event.data2 < 31 or 32 <= event.data2 < 64:
            new_param_value = min(param_value + volume_increment, 1)
    else:
        if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
            new_param_value = max(param_value - volume_increment, 0)
        elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
            new_param_value = min(param_value + volume_increment, 1)

    send_hint_message(param_name)
    plugins.setParamValue(new_param_value, param_index, mix_track_index, mixer_slot, pickup_mode, use_global_index)
    NILA_OLED.OnRefresh(self, event)

def handle_mixer_effect(self, event):
    """
    Handles events related to mixer effects.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.

    Returns:
    None
    """
    track_index, mixer_slot = mixer.getActiveEffectIndex()
    track_plugin_id = mixer.getTrackPluginId(track_index, mixer_slot)
    event_id = midi.REC_Plug_MixLevel + track_plugin_id
    mix_slot_volume = general.processRECEvent(event_id, 0, midi.REC_GetValue)
    converted_volume = round((mix_slot_volume / c.midi_CC_max) * 100)

    if event.data1 == nihia.mixer.knobs[0][0]:
        handle_mixer_effect_mix(self, event, converted_volume, event_id)

def handle_mixer_effect_mix(self, event, converted_volume, event_id):
    """
    Handles mixer effect events for adjusting mix level.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.
    - converted_volume: The converted volume level.
    - event_id: The MIDI event ID.

    Returns:
    None
    """
    volume_increment = config.increment * 100
    adjusted_increment = knob_time_check_mixer(self, volume_increment)

    if not NILA_core.seriesCheck():
        handle_non_series_knob_event(self, event, converted_volume, event_id, adjusted_increment)
    else:
        handle_series_knob_event(self, event, converted_volume, event_id, adjusted_increment)

def handle_non_series_knob_event(self, event, converted_volume, event_id, volume_increment):
    """
    Handles non-series knob events for mixer effect control.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.
    - converted_volume: The converted volume level.
    - event_id: The MIDI event ID.
    - volume_increment: The increment for volume control.

    Returns:
    None
    """
    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED and converted_volume - 1 >= 0:
        converted_volume -= volume_increment
    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED and converted_volume + 1 <= 100:
        converted_volume += volume_increment

    update_and_record_volume(self, event, event_id, converted_volume)

def handle_series_knob_event(self, event, converted_volume, event_id, volume_increment):
    """
    Handles series knob events for mixer effect control.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.
    - converted_volume: The converted volume level.
    - event_id: The MIDI event ID.
    - volume_increment: The increment for volume control.

    Returns:
    None
    """
    if 65 <= event.data2 < 95 or 96 <= event.data2 < 128:
        if converted_volume - 1 >= 0:
            converted_volume -= volume_increment
    elif 0 <= event.data2 < 31 or 32 <= event.data2 < 64:
        if converted_volume + 1 <= 100:
            converted_volume += volume_increment

    update_and_record_volume(self, event, event_id, converted_volume)

def update_and_record_volume(self, event, event_id, converted_volume):
    """
    Updates and records the volume based on the converted volume level.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.
    - event_id: The MIDI event ID.
    - converted_volume: The converted volume level.

    Returns:
    None
    """
    mix_slot_volume = round((converted_volume / 100) * c.midi_CC_max)
    mix_slot_volume = max(0, min(12800, mix_slot_volume))
    general.processRECEvent(event_id, mix_slot_volume, midi.REC_Control | midi.REC_UpdateValue | midi.REC_UpdateControl)
    NILA_OLED.OnRefresh(self, event)

def handle_channel_rack_controls(self, event):
    """
    Handles events related to the channel rack controls.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.

    Returns:
    None
    """
    if event.data1 == nihia.mixer.knobs[0][0]:
        handle_volume_control(self, event)
    elif event.data1 == nihia.mixer.knobs[1][0]:
        handle_pan_control(self, event)

def handle_volume_control(self, event):
    """
    Handles volume control events for the channel.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.

    Returns:
    None
    """
    if NILA_core.seriesCheck():
        handle_series_volume(self, event)
    else:
        handle_single_volume(self, event)

def handle_series_volume(self, event):
    """
    Handles series volume control events for the channel.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.

    Returns:
    None
    """
    selected_channel = channels.selectedChannel()
    volume_increment = config.increment
    new_value = knob_time_check(self, volume_increment)

    if 65 <= event.data2 < 95 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - new_value * 2.5, 2))
    elif 96 <= event.data2 < 128 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - new_value, 2))
    elif 0 <= event.data2 < 31:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + new_value, 2))
    elif 32 <= event.data2 < 64:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + new_value * 2.5, 2))

def handle_single_volume(self, event):
    """
    Handles single volume control events for the channel.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.

    Returns:
    None
    """
    selected_channel = channels.selectedChannel()
    volume_increment = config.increment
    new_value = knob_time_check(self, volume_increment)

    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - new_value, 2))
    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + new_value, 2))

def handle_pan_control(self, event):
    """
    Handles pan control events for the channel.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.

    Returns:
    None
    """
    selected_channel = channels.selectedChannel()
    pan_increment = config.increment
    new_value = knob_time_check(self, pan_increment)

    if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
        channels.setChannelPan(selected_channel, channels.getChannelPan(selected_channel) - new_value)
    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
        channels.setChannelPan(selected_channel, channels.getChannelPan(selected_channel) + new_value)

def knob_time_check(self, adjusted_increment):
    """
    Checks the time difference to adjust the knob rotation speed.

    Parameters:
    - self: The instance of the script.
    - adjusted_increment: The adjusted increment value.

    Returns:
    The adjusted increment value.
    """
    current_time = time.time()
    time_difference = current_time - getattr(self, f'last_signal_time_', current_time)
    setattr(self, f'last_signal_time_', current_time)
    adjusted_increment = config.increment * c.knob_rotation_speed if time_difference <= c.speed_increase_wait else config.increment
    return adjusted_increment

def knob_time_check_mixer(self, adjusted_increment):
    """
    Checks the time difference to adjust the knob rotation speed for mixer controls.

    Parameters:
    - self: The instance of the script.
    - adjusted_increment: The adjusted increment value.

    Returns:
    The adjusted increment value.
    """
    current_time = time.time()
    time_difference = current_time - getattr(self, 'last_signal_time', current_time)
    setattr(self, 'last_signal_time', current_time)

    if time_difference <= 0.005:
        adjusted_increment *= 14

    return adjusted_increment