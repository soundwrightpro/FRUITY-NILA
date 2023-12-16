import nihia
from nihia import mixer as mix
from script.device_setup import NILA_core as core
from script.device_setup import config 
from script.device_setup import constants
import mixer
import ui 

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

                    if event.data1 == nihia.mixer.knobs[0][z]:  # VOLUME CONTROL
                        handle_volume_control(track_number, event.data2)

                    elif event.data1 == nihia.mixer.knobs[1][z]:  # PAN CONTROL
                        handle_pan_control(track_number, event.data2)

def handle_volume_control(track_number, data2):
    """
    Handles volume control for a specific mixer track.

    Parameters:
    - track_number: The number of the mixer track to control.
    - data2: The MIDI event data representing the movement of the MIDI knob.
    """
    volume_increment = config.increment

    if core.seriesCheck():
        if 65 <= data2 < 95:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) - volume_increment * 2.5)
        elif 96 <= data2 < 128:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) - volume_increment)
        elif 0 <= data2 < 31:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) + volume_increment)
        elif 32 <= data2 < 64:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) + volume_increment * 2.5)
    else:
        if data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) - volume_increment)
        elif data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
            mixer.setTrackVolume(track_number, mixer.getTrackVolume(track_number) + volume_increment)

def handle_pan_control(track_number, data2):
    """
    Handles pan control for a specific mixer track.

    Parameters:
    - track_number: The number of the mixer track to control.
    - data2: The MIDI event data representing the movement of the MIDI knob.
    """
    pan_increment = config.increment

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
