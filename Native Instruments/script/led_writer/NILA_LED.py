import nihia
from nihia import buttons
from nihia.mixer import setTrackSolo, setTrackMute, setTrackArm, setTrackMutedBySolo
from script.device_setup import constants
import device
import channels
import mixer
import transport
import ui

# Constants for button light states
on, off = 1, 0

def set_light(button_name, state):
    """
    Sets the light state of a button.

    Parameters:
    - button_name (str): The name of the button.
    - state (int): The state of the light (0 for off, 1 for on).
    """
    nihia.buttons.setLight(button_name, state)

def OnRefresh(self, flags):
    """
    Handles the refresh event and updates button lights based on the DAW state.

    Parameters:
    - self: The instance of the script.
    - flags: Flags indicating the refresh event details.
    """
    if device.isAssigned():
        # Update transport control lights
        set_light("STOP", on if not transport.isPlaying() else off)
        set_light("REC", on if transport.isRecording() else off)
        set_light("LOOP", on if transport.getLoopMode() == off else off)
        set_light("METRO", on if ui.isMetronomeEnabled() else off)
        set_light("COUNT_IN", on if ui.isPrecountEnabled() else off)
        set_light("QUANTIZE", on if ui.getSnapMode() in [1, 3] else on)
        set_light("AUTO", off)

        # Update PLAY button light when not playing or recording
        if not transport.isPlaying() and transport.isRecording() == False:
            set_light("PLAY", on if transport.isPlaying() else off)
        elif transport.isPlaying() == False and transport.isRecording() == True:
            set_light("PLAY", off)

        # Update mixer lights if Mixer window is focused
        if ui.getFocused(constants.winName["Mixer"]):
            for x in range(8):
                track_number = mixer.trackNumber() + x
                if 0 < track_number <= 125:
                    is_muted = mixer.isTrackMuted(track_number)
                    is_solo = mixer.isTrackSolo(track_number)
                    
                    if is_muted and is_solo:
                        setTrackMute(x, on)
                        setTrackSolo(x, off)
                    else:
                        setTrackSolo(x, is_solo)
                        setTrackMute(x, is_muted)
                        setTrackArm(x, mixer.isTrackArmed(track_number))

        # Update Channel Rack lights if Channel Rack window is focused
        if ui.getFocused(constants.winName["Channel Rack"]):
            if channels.channelCount() >= 2:
                for x in range(8):
                    selected_channel = channels.selectedChannel()
                    if channels.channelCount() > x and selected_channel < (channels.channelCount() - x):
                        setTrackSolo(x, channels.isChannelSolo(selected_channel + x))
                        setTrackMute(x, channels.isChannelMuted(selected_channel + x))
            else:
                setTrackMute(0, on) if channels.isChannelMuted(channels.selectedChannel()) else setTrackMute(0, off)
                setTrackSolo(0, off) if channels.channelCount() == 1 and channels.isChannelSolo(channels.selectedChannel()) else setTrackSolo(0, off)

        # Set lights for the 4D Encoder on S-Series keyboards
        set_light("ENCODER_X_S", 1)
        set_light("ENCODER_X_S", 127)
        set_light("ENCODER_Y_S", 1)
        set_light("ENCODER_Y_S", 127)

def OnUpdateBeatIndicator(self, Value):
    """
    Handles the beat indicator update event and updates PLAY and REC button lights.

    Parameters:
    - self: The instance of the script.
    - Value: The current beat indicator value.
    """
    if transport.isRecording() == 0:
        set_light("PLAY", on if Value in [1, 2] else off)
    elif transport.isRecording() == 1:
        set_light("PLAY", on)
        set_light("REC", on if Value in [1, 2] else off)