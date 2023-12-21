import nihia
from nihia import mixer as mix
from script.device_setup import NILA_core as core
from script.device_setup import config
from script.device_setup import constants
import mixer
import ui
import time

# Constants for tracking knob values per second
KNOB_HISTORY_DURATION = 1.0  # seconds
KNOB_VALUE_THRESHOLD = 3

# Dictionary to store knob values and timestamps
knob_history = {}

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

                    knob_key = nihia.mixer.knobs[0][z] if event.data1 == nihia.mixer.knobs[0][z] else nihia.mixer.knobs[1][z]
                    
                    if knob_key in knob_history:
                        knob_history[knob_key].append(time.time())
                    else:
                        knob_history[knob_key] = [time.time()]

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
    global knob_history

    volume_increment = config.increment
    
    # Check if the knob has sent enough values in the last second to increase volume_increment
    knob_key = nihia.mixer.KNOB_DECREASE_MAX_SPEED if data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED else nihia.mixer.KNOB_INCREASE_MAX_SPEED
    if knob_key in knob_history and len(knob_history[knob_key]) >= KNOB_VALUE_THRESHOLD:
        volume_increment = volume_increment * 6

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


        # Clear the knob history after checking
        knob_history[knob_key] = []

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
