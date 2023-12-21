import nihia
from nihia import *
from script.device_setup.NILA_core import seriesCheck

from script.device_setup import config
from script.device_setup import constants
from script.screen_writer import NILA_OLED as oled
import channels
import ui
import time

def adjust_channel_value(channel_value, data2, increment, speed=0):
    """
    Adjusts the channel value based on MIDI input.

    Parameters:
    - channel_value (float): The current value of the channel parameter (volume or pan).
    - data2 (int): The MIDI data2 value indicating the direction of adjustment.
    - increment (float): The base increment value for adjustment.
    - speed (float): The speed of adjustment.

    Returns:
    - float: The adjusted channel value.
    """
    if data2 in range(65, 95):
        return round(channel_value - increment, 2)
    elif data2 in range(96, 128):
        return round(channel_value - increment, 2)
    elif data2 in range(0, 31):
        return round(channel_value + increment, 2)
    elif data2 in range(32, 64):
        return round(channel_value + increment, 2)
    elif speed != 0:
        return round(channel_value + speed, 2)
    else:
        return channel_value

def OnMidiMsg(self, event):
    """
    Handles MIDI messages for channel adjustment in the Channel Rack.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event.
    """
    
    knob_speed = 0
    
    if ui.getFocused(constants.winName["Channel Rack"]):
        
        
        # VOLUME AND PAN CONTROL
        #s_series = False
        
        for control_type in (0, 1):  # 0 for volume, 1 for pan
            for z in range(8):
                if channels.channelCount() > z and channels.selectedChannel() < (channels.channelCount() - z):
                    knob_data = nihia.mixer.knobs[control_type][z]
                    knob_speed = (
                        knob_speed if seriesCheck() and event.data2 in (nihia.mixer.KNOB_DECREASE_MAX_SPEED, nihia.mixer.KNOB_INCREASE_MAX_SPEED)
                        or seriesCheck() and event.data2 in (nihia.mixer.KNOB_DECREASE_MIN_SPEED, nihia.mixer.KNOB_INCREASE_MIN_SPEED) else 0
                    )
                    
                    current_channel = channels.selectedChannel() + z
                    current_value = (
                        channels.getChannelVolume(current_channel) if control_type == 0 else
                        channels.getChannelPan(current_channel)
                    )
                    
                    if event.data1 == knob_data:
                        event.handled = True

                        # Check the time between consecutive signals
                        current_time = time.time()  
                        time_difference = current_time - getattr(self, f'last_signal_time_{z}', current_time)
                        setattr(self, f'last_signal_time_{z}', current_time)

                        # Adjust increment value based on the time difference
                        adjusted_increment = config.increment * constants.knob_rotation_speed if time_difference < constants.speed_increase_wait else config.increment

                        new_value = adjust_channel_value(current_value, event.data2, adjusted_increment, knob_speed)
                        
                        if control_type == 0:
                            channels.setChannelVolume(current_channel, new_value)
                            oled.OnRefresh(self, event)
                        else:
                            channels.setChannelPan(current_channel, new_value)
                            
                        
                else:
                    event.handled = True
