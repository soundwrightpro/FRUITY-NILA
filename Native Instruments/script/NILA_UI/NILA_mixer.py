import nihia
from script.device_setup import NILA_core as core
from script.device_setup import config
from script.device_setup import constants
import mixer
import ui
import time


def OnMidiMsg(self, event):
    """
    Handles MIDI messages received in FL Studio.

    Parameters:
    - self: The instance of the script.
    - event: The MIDI event object containing information about the received MIDI message.
    """
    if ui.getFocused(constants.winName["Mixer"]):
        for z in range(8):
            if mixer.trackNumber() <= constants.currentUtility - z:
                track_number = mixer.trackNumber() + z
                track_name = mixer.getTrackName(track_number)

                if track_number <= constants.currentUtility - z and track_name != "Current":
                    event.handled = True
                    
                    # Check the time between consecutive signals
                    current_time = time.time()  
                    time_difference = current_time - getattr(self, f'last_signal_time_{z}', current_time)
                    setattr(self, f'last_signal_time_{z}', current_time)
                    
                    adjusted_increment = config.increment * constants.knob_rotation_speed if time_difference <= constants.speed_increase_wait else config.increment
                    
                    if event.data1 == nihia.mixer.knobs[0][z]:  # VOLUME CONTROL
                        handle_volume_control(track_number, event.data2, adjusted_increment)

                    elif event.data1 == nihia.mixer.knobs[1][z]:  # PAN CONTROL
                        handle_pan_control(track_number, event.data2, adjusted_increment)


def handle_volume_control(track_number, data2, volume_increment):
    """
    Handles volume control for a specific mixer track.

    Parameters:
    - track_number: The number of the mixer track to control.
    - data2: The MIDI event data representing the movement of the MIDI knob.
    """
    if core.seriesCheck():
        if 65 <= data2 < 95:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) - volume_increment)
        elif 96 <= data2 < 128:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) - volume_increment)
        elif 0 <= data2 < 31:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) + volume_increment)
        elif 32 <= data2 < 64:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) + volume_increment)
    else:
        if data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) - volume_increment)
        elif data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) + volume_increment)


def handle_pan_control(track_number, data2, pan_increment):
    """
    Handles pan control for a specific mixer track.

    Parameters:
    - track_number: The number of the mixer track to control.
    - data2: The MIDI event data representing the movement of the MIDI knob.
    """
    if core.seriesCheck():
        if nihia.mixer.KNOB_INCREASE_MAX_SPEED <= data2:
            mixer.setTrackPan(track_number, mixer.getTrackPan(track_number) - pan_increment)
        elif nihia.mixer.KNOB_DECREASE_MAX_SPEED >= data2:
            mixer.setTrackPan(track_number, mixer.getTrackPan(track_number) + pan_increment)
    else:
        if data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
            mixer.setTrackPan(track_number, mixer.getTrackPan(track_number) - pan_increment)
        elif data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
            mixer.setTrackPan(track_number, mixer.getTrackPan(track_number) + pan_increment)