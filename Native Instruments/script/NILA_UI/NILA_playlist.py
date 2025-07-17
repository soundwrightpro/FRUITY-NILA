import nihia
from script.device_setup import config, constants as c, NILA_transform
from script.screen_writer import NILA_OLED as oled
import mixer
import ui 

def OnMidiMsg(self, event):
    """Handle MIDI messages for the Playlist window.

    Args:
        self: Script instance.
        event: Incoming MIDI event.

    Returns:
        None.
    """
    if ui.getFocused(c.winName["Playlist"]):
        handle_volume_control(event)

def handle_volume_control(event):
    """Respond to volume control events.

    Args:
        event: MIDI event from the controller.

    Returns:
        None.
    """
    if event.data1 == nihia.mixer.knobs[0][0]:
        event.handled = True
        track_index = c.playlist_track_index

        if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
            adjust_track_volume(track_index, -config.increment)
        elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
            adjust_track_volume(track_index, config.increment)

def adjust_track_volume(track_index, increment):
    """Change the volume of a playlist track.

    Args:
        track_index: Index of the playlist track.
        increment: Amount to adjust by.

    Returns:
        None.
    """
    current_volume = mixer.getTrackVolume(track_index)
    new_volume = NILA_transform.clamp(
        current_volume + increment, 
        c.track_volume_min, 
        c.track_volume_max
    )
    mixer.setTrackVolume(track_index, new_volume)
