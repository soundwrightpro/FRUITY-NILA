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

# Function to handle plugin control events for the NILA system
def plugin(self, event):
    """
    Handles plugin control events for the NILA system.

    Args:
        self (object): The instance of the NILA system.
        event (object): The event triggered by the user's input.
    """
    if ui.getFocused(c.winName["Plugin"]):
        event.handled = True
        if ui.getFocused(c.winName["Generator Plugin"]):
            handle_channel_rack_controls(self, event)
        else:
            handle_mixer_effect(self, event)
            
        plugin_set_param(self, event)


def plugin_set_param(self, event, mixer_slot=-1):
    """
    Sets plugin parameters based on the received event.

    Args:
        self (object): The instance of the NILA system.
        event (object): The event triggered by the user's input.
        mixer_slot (int, optional): Mixer slot index (default is -1).
    """
    useGlobalIndex = False

    if ui.getFocused(c.winName["Effect Plugin"]):
        mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
        track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
        event_id = midi.REC_Plug_MixLevel + track_plugin_id
        param_count = plugins.getParamCount(mix_track_index, mixer_slot, useGlobalIndex)

        if param_count > 0:
            for knob_number in range(1, min(param_count + 1, 8)):
                param_index = min(max(knob_number - 1 + c.lead_param, 0), param_count - 1)
                knob_data = nihia.mixer.knobs[0][knob_number]
                volume_increment = config.increment

                if event.data1 == knob_data:
                    adjusted_increment = knob_time_check(self, volume_increment)
                    handle_param_control(self, event, param_index, mix_track_index, mixer_slot, useGlobalIndex, event.data2, adjusted_increment)


    elif ui.getFocused(c.winName["Generator Plugin"]):
        chan_track_index = channels.selectedChannel()
        plugins.getParamCount(chan_track_index, mixer_slot, useGlobalIndex)


def handle_param_control(self, event, param_index, mix_track_index, mixer_slot, useGlobalIndex, data2, volume_increment):
    """
    Handles the adjustment of a specific parameter of a plugin based on the user's input event.

    Args:
        self (object): The instance of the NILA system.
        event (object): The event triggered by the user's input.
        param_index (int): Index of the parameter to be controlled.
        mix_track_index (int): Mixer track index.
        mixer_slot (int): Mixer slot index.
        useGlobalIndex (bool): Flag indicating whether to use a global index.
        data2 (int): Data value from the event.
        volume_increment (float): Increment value for parameter change.
    """
    pickupMode = 0
    param_value = plugins.getParamValue(param_index, mix_track_index, mixer_slot, useGlobalIndex)
    percentage = param_value * 100

    if NILA_core.seriesCheck():
        if 65 <= data2 < 95 or 96 <= data2 < 128:
            new_param_value = max(param_value - volume_increment, 0)
        elif 0 <= data2 < 31 or 32 <= data2 < 64:
            new_param_value = min(param_value + volume_increment, 1)
    else:
        if data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
            new_param_value = max(param_value - volume_increment, 0)
        elif data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
            new_param_value = min(param_value + volume_increment, 1)

        plugins.setParamValue(new_param_value, param_index, mix_track_index, mixer_slot, pickupMode, useGlobalIndex)


    NILA_OLED.OnRefresh(self, event)

            
# Function to handle control events for the active mixer effect slot mix level for focused plugin on the mixer
def handle_mixer_effect(self, event):
    """
    Handles control events for the active mixer effect slot mix level for focused plugin on the mixer.

    Args:
        event (object): The event triggered by the user's input.
    """
    track_index, mixer_slot = mixer.getActiveEffectIndex()
    track_plugin_id = mixer.getTrackPluginId(track_index, mixer_slot)
    event_id = midi.REC_Plug_MixLevel + track_plugin_id
    mix_slot_volume = general.processRECEvent(event_id, 0, midi.REC_GetValue)

    # Convert mix_slot_volume to the percentage scale [0, 100]
    converted_volume = round((mix_slot_volume / c.midi_CC_max) * 100)

    if event.data1 == nihia.mixer.knobs[0][0]:
        handle_mixer_effect_mix(self, event, converted_volume, event_id)


# Function to handle mix level knob control events
def handle_mixer_effect_mix(self, event, converted_volume, event_id):
    """
    Handles mix level knob control events.

    Args:
        event (object): The event triggered by the user's input.
        converted_volume (float): Current volume converted to the percentage scale.
        event_id (int): Event ID for the mixer plugin.
    """
    volume_increment = config.increment * 100
    
    adjusted_increment = knob_time_check_mixer(self, volume_increment)

    if not NILA_core.seriesCheck():
        handle_non_series_knob_event(self, event, converted_volume, event_id, adjusted_increment)
    else:
        handle_series_knob_event(self, event, converted_volume, event_id, adjusted_increment)


# Function to handle knob events in non-series S devices
def handle_non_series_knob_event(self, event, converted_volume, event_id, volume_increment):
    """
    Handles knob events in non-series S devices.

    Args:
        event (object): The event triggered by the user's input.
        converted_volume (float): Current volume converted to the percentage scale.
        event_id (int): Event ID for the mixer plugin.
        volume_increment (float): Increment value for volume change.
    """

    # Adjust volume increment based on knob rotation speed

    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED and converted_volume - 1 >= 0:
        converted_volume -= volume_increment
    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED and converted_volume + 1 <= 100:
        converted_volume += volume_increment

    update_and_record_volume(self, event_id, converted_volume)


# Function to handle knob events in series devices
def handle_series_knob_event(self, event, converted_volume, event_id, volume_increment):
    """
    Handles knob events in series devices.

    Args:
        event (object): The event triggered by the user's input.
        converted_volume (float): Current volume converted to the percentage scale.
        event_id (int): Event ID for the mixer plugin.
        volume_increment (float): Increment value for volume change.
    """

    if 65 <= event.data2 < 95 or 96 <= event.data2 < 128:
        if converted_volume - 1 >= 0:
            converted_volume -= volume_increment

    elif 0 <= event.data2 < 31 or 32 <= event.data2 < 64:
        if converted_volume + 1 <= 100:
            converted_volume += volume_increment

    update_and_record_volume(self, event_id, converted_volume)


# Function to update the volume of the mix level on the focused plugin
def update_and_record_volume(self, event_id, converted_volume):
    """
    Update the volume of the mix level on the focused plugin.

    Args:
        event_id (int): Event ID for the mixer plugin.
        converted_volume (float): Current volume converted to the percentage scale.
    """

    # Calculate mix_slot_volume based on the converted_volume
    mix_slot_volume = round((converted_volume / 100) * c.midi_CC_max)

    # Ensure mix_slot_volume is within the desired range [0, 12800]
    mix_slot_volume = max(0, min(12800, mix_slot_volume))
    
    general.processRECEvent(event_id, mix_slot_volume, midi.REC_Control | midi.REC_UpdateValue | midi.REC_UpdateControl)
    

# Function to handle controls specific to the Channel Rack
def handle_channel_rack_controls(self, event):
    """
    Handles controls specific to the Channel Rack.

    Args:
        event (object): The event triggered by the user's input.
    """
    if event.data1 == nihia.mixer.knobs[0][0]:
        handle_volume_control(self, event)
    elif event.data1 == nihia.mixer.knobs[1][0]:
        handle_pan_control(self, event)


# Function to handle volume control events
def handle_volume_control(self, event):
    """
    Handles volume control events.

    Args:
        event (object): The event triggered by the user's input.
    """
    if NILA_core.seriesCheck():
        handle_series_volume(self, event)
    else:
        handle_single_volume(self, event)


# Function to handle volume control events for series S device on the channel rack
def handle_series_volume(self, event):
    """
    Handles volume control events for series S device on the channel rack.

    Args:
        event (object): The event triggered by the user's input.
    """
    selected_channel = channels.selectedChannel()
    volume_increment = config.increment
    
    new_value = knob_time_check(self, volume_increment)

    if 65 <= event.data2 < 95 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(
            selected_channel, round(channels.getChannelVolume(selected_channel) - new_value * 2.5, 2))
    elif 96 <= event.data2 < 128 and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - new_value, 2))
    elif 0 <= event.data2 < 31:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + new_value, 2))
    elif 32 <= event.data2 < 64:
        channels.setChannelVolume(
            selected_channel, round(channels.getChannelVolume(selected_channel) + new_value * 2.5, 2))


# Function to handle volume control events for single mode
def handle_single_volume(self, event):
    """
    Handles volume control events for single mode.

    Args:
        event (object): The event triggered by the user's input.
    """
    selected_channel = channels.selectedChannel()
    volume_increment = config.increment
    
    new_value = knob_time_check(self, volume_increment)
    
    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED and channels.getChannelVolume(selected_channel) != 0:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) - new_value, 2))
    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
        channels.setChannelVolume(selected_channel, round(channels.getChannelVolume(selected_channel) + new_value, 2))


# Function to handle pan control events
def handle_pan_control(self, event):
    """
    Handles pan control events.

    Args:
        event (object): The event triggered by the user's input.
    """
    selected_channel = channels.selectedChannel()
    pan_increment = config.increment
    
    new_value = knob_time_check(self, pan_increment)

    if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
        channels.setChannelPan(selected_channel, channels.getChannelPan(selected_channel) - new_value)
    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
        channels.setChannelPan(selected_channel, channels.getChannelPan(selected_channel) + new_value)


# Function to handle other knob control events
def handle_other_controls(event):
    """
    Handles other knob control events.

    Args:
        event (object): The event triggered by the user's input.
    """
    event.handled = any(event.data1 == nihia.mixer.knobs[i][x] for i in range(2) for x in range(8))


# Function to check the time between consecutive signals and adjust the knob increment accordingly
def knob_time_check(self, adjusted_increment):
    """
    Check the time between consecutive signals and adjust the knob increment accordingly.

    Args:
        self (object): The instance of the NILA system.
        adjusted_increment (float): Adjusted increment value for volume change.

    Returns:
        float: Adjusted knob increment.
    """
    # Check the time between consecutive signals
    current_time = time.time() 
     
    
    time_difference = current_time - getattr(self, f'last_signal_time_', current_time)
    setattr(self, f'last_signal_time_', current_time)
    
    adjusted_increment = config.increment * c.knob_rotation_speed if time_difference <= c.speed_increase_wait else config.increment
        
    return adjusted_increment


def knob_time_check_mixer(self, adjusted_increment):
    """
    Check the time between consecutive signals and adjust the knob increment accordingly.

    Args:
        self (object): The instance of the NILA system.
        adjusted_increment (float): Adjusted increment value for volume change.

    Returns:
        float: Adjusted knob increment.
    """
    # Check the time between consecutive signals
    current_time = time.time()
    time_difference = current_time - getattr(self, 'last_signal_time', current_time)
    
    # Update last signal time
    setattr(self, 'last_signal_time', current_time)

    # Adjust volume increment based on the time difference
    
    if time_difference <= 0.005:
        adjusted_increment *= 14
    # Add additional conditions for different time thresholds if needed

    return adjusted_increment