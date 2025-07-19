import nihia
from NILA.NILA_engine import config, constants as c, NILA_transform
from NILA.NILA_visuals import NILA_OLED as oled
import mixer
import ui 

def OnMidiMsg(self, event): 
    """
    Handles MIDI messages for the Playlist window.
    """
    if ui.getFocused(c.winName["Playlist"]):
        handle_volume_control(event)

def handle_volume_control(event):
    """
    Handles volume control events.
    """
    if event.data1 == nihia.mixer.knobs[0][0]:
        event.handled = True
        track_index = c.playlist_track_index

        if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
            adjust_track_volume(track_index, -config.mixer_increment)
        elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
            adjust_track_volume(track_index, config.mixer_increment)

def adjust_track_volume(track_index, increment):
    """
    Adjusts the volume of a track based on the provided increment.
    """
    current_volume = mixer.getTrackVolume(track_index)
    new_volume = NILA_transform.clamp(
        current_volume + increment, 
        c.track_volume_min, 
        c.track_volume_max
    )
    mixer.setTrackVolume(track_index, new_volume)
