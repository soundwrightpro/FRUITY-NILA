import nihia
from nihia import mixer as mix
from script.device_setup import config, constants, transform
from script.screen_writer import NILA_OLED as oled
import mixer
import ui 

def OnMidiMsg(self, event): 
    """
    Handles MIDI messages for the Playlist window.

    Args:
        self: The instance of the NILA system.
        event: The MIDI event triggered by the MIDI controller.
    """
    if ui.getFocused(constants.winName["Playlist"]):
        handle_volume_control(event)

def handle_volume_control(event):
    """
    Handles volume control events.

    Args:
        event: The MIDI event triggered by the volume control knob.
    """
    event.handled = True
    track_index = 0

    if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
        adjust_track_volume(track_index, -config.increment)
    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
        adjust_track_volume(track_index, config.increment)

def adjust_track_volume(track_index, increment):
    """
    Adjusts the volume of a track based on the provided increment.

    Args:
        track_index: Index of the track to adjust.
        increment: Amount to adjust the volume.
    """
    current_volume = mixer.getTrackVolume(track_index)
    new_volume = transform.clamp(current_volume + increment, 0.0, 1.0)
    mixer.setTrackVolume(track_index, new_volume)