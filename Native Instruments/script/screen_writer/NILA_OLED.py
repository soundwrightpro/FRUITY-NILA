"""
This script defines functions related to the behavior of the FL Studio script in response to various events.

Functions:
- OnRefresh(self, event): Handles the refreshing of the script's state, updating tracks and parameters.
- OnUpdateBeatIndicator(self, Value): Updates the beat indicator based on the focused window (e.g., Playlist).
- OnIdle(self): Performs idle tasks based on the currently focused window.

Supporting Functions:
- remove_part(): Removes tracks 1 to 7.
- remove_all(): Removes all tracks (0 to 7).
- clear_part(): Clears information from tracks 1 to 7.
- clear_all(): Clears information from all tracks (0 to 7).

Dependencies:
- nihia.mixer as mix: Provides access to mixer-related functions.
- script.device_setup.NILA_core, constants, NILA_transform: Handles device setup and constants.
- channels, mixer, plugins, transport, ui, device: FL Studio API modules for channel, mixer, plugin, transport, UI, and device interactions.
- math: Python math module for mathematical operations.
"""

from nihia import mixer as mix

from script.device_setup import NILA_core, constants, NILA_transform

import channels
import mixer
import plugins
import transport
import ui
import device
import math

def OnRefresh(self, event):
    """
    Handles the refreshing of the script's state, updating tracks and parameters based on the currently focused window.

    Parameters:
    - self: The instance of the script.
    - event: The event triggering the refresh.
    """
    self.kompleteInstance = None

    if plugins.isValid(channels.selectedChannel()) and plugins.getPluginName(channels.selectedChannel()) == "Komplete Kontrol":
        if self.kompleteInstance != plugins.getParamName(0, channels.selectedChannel()):
            self.kompleteInstance = plugins.getParamName(0, channels.selectedChannel())
            mix.setTrackKompleteInstance(0, self.kompleteInstance)
    else:
        if self.kompleteInstance:
            self.kompleteInstance = ""
            mix.setTrackKompleteInstance(0, "")

    if ui.getFocused(constants.winName["Mixer"]) == True:
        for x in range(8):
            trackNumber = mixer.trackNumber() + x
            if mixer.trackNumber() <= constants.currentUtility - x and trackNumber != constants.currentUtility:
                mix.setTrackExist(x, 1)
                mix.setTrackName(x, mixer.getTrackName(trackNumber))
                mix.setTrackVol(x, str(NILA_transform.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + x))) + " dB")
                mix.setTrackVolGraph(x, mixer.getTrackVolume(trackNumber))
                NILA_transform.updatePanMix(trackNumber, x)
                mix.setTrackSel(0, 1 if trackNumber == constants.currentUtility else 0)
            else:
                mix.setTrackExist(x, 0)

    if ui.getFocused(constants.winName["Channel Rack"]) == True:
        for x in range(8):
            selectedChannel = channels.selectedChannel() + x
            if channels.channelCount() > x and selectedChannel < channels.channelCount():
                mix.setTrackExist(x, 1)
                mix.setTrackName(x, channels.getChannelName(selectedChannel))
                mix.setTrackVol(x, f"{round(channels.getChannelVolume(selectedChannel, 1), 1)} dB")
                mix.setTrackVolGraph(x, channels.getChannelVolume(selectedChannel) / 1.0 * 0.86)
                NILA_transform.updatePanChannel(selectedChannel, x)
                mix.setTrackSel(0, 0)
            else:
                mix.setTrackExist(x, 0)

    if ui.getFocused(constants.winName["Plugin"]) == True:
            if not mixer.getActiveEffectIndex(): 
                clear_part()
                remove_part()
                mix.setTrackExist(0, 1)
                mix.setTrackName(0, f"P| {channels.getChannelName(channels.selectedChannel())}")
                mix.setTrackVol(0, f"{round(channels.getChannelVolume(channels.selectedChannel(), 1), 1)} dB")
                mix.setTrackVolGraph(0, channels.getChannelVolume(channels.selectedChannel()) / 1.0 * 0.86)
                NILA_transform.updatePanChannel(channels.selectedChannel(), 0)
                mix.setTrackSel(0, 0)
            else:
                if device.getName() == "Komplete Kontrol DAW - 1":
                    track_index, mixer_slot = mixer.getActiveEffectIndex()
                    full_plugin_name = plugins.getPluginName(track_index, mixer_slot)
                    shortened_plugin_name = full_plugin_name[:9]
                    clear_all()
                    remove_all()
                    mix.setTrackExist(0, 1)
                    mix.setTrackName(0, shortened_plugin_name)
                else:
                    track_index, mixer_slot = mixer.getActiveEffectIndex()
                    full_plugin_name = plugins.getPluginName(track_index, mixer_slot)
                    clear_part()
                    remove_part()
                    mix.setTrackExist(0, 1)
                    mix.setTrackName(0, f"P| Insert: {track_index}")
                    mix.setTrackVol(0,full_plugin_name)
                    

    if ui.getFocused(constants.winName["Piano Roll"]) == True:
        remove_part()
        clear_part()
        mix.setTrackName(0, str(channels.getChannelName(channels.selectedChannel())))
        NILA_core.setTrackVolConvert(0, f"{round(channels.getChannelVolume(channels.selectedChannel(), 1), 1)} dB")
        NILA_transform.updatePanChannel(channels.selectedChannel(), 0)

    if ui.getFocused(constants.winName["Playlist"]) == True:
        mix.setTrackName(0, "Playlist")
        mix.setTrackVolGraph(0, mixer.getTrackVolume(0))

def OnUpdateBeatIndicator(self, Value):
    """
    Updates the beat indicator based on the focused window (e.g., Playlist).

    Parameters:
    - self: The instance of the script.
    - Value: The value associated with the beat indicator event.
    """
    if ui.getFocused(constants.winName["Playlist"]) == True:
        timeDisp, currentTime = NILA_core.timeConvert(constants.itemDisp, constants.itemTime)
        mix.setTrackName(0, "Playlist")
        split_message = ui.getHintMsg()
        split_point1 = ' - '
        split_point2 = ' to '
        split_hint = split_message.partition(split_point1)[2] if split_point1 in split_message.lower() else split_message.partition(split_point2)[2]

        if device.getName() == "Komplete Kontrol DAW - 1":
            mix.setTrackVol(0, f"|{currentTime}")
        else:
            if transport.isPlaying():
                timeDisp = "B:B" if timeDisp == "Beats:Bar" and len(currentTime) >= 5 else timeDisp
                timeDisp = "M:S" if timeDisp == "Min:Sec" and len(currentTime) > 5 else timeDisp
                mix.setTrackVol(0, f"{timeDisp}|{currentTime}")
            else:
                mix.setTrackVol(0, f"{split_hint[:7]}|{currentTime}")
                mix.setTrackVolGraph(0, mixer.getTrackVolume(0))

def OnIdle(self):
    """
    Performs idle tasks based on the currently focused window.
    
    Parameters:
    - self: The instance of the script.
    """
    if ui.getFocused(constants.winName["Playlist"]) == True:
        remove_part()
        clear_part()
        mix.setTrackVolGraph(0, mixer.getTrackVolume(0))
        timeDisp, currentTime = NILA_core.timeConvert(constants.itemDisp, constants.itemTime)
        split_message = ui.getHintMsg()
        split_point1 = ' - '
        split_point2 = ' to '
        split_hint = split_message.partition(split_point1)[2] if split_point1 in split_message.lower() else split_message.partition(split_point2)[2]

        mix.setTrackName(0, "Playlist")
        if not transport.isPlaying() and "Volume" not in split_hint[:7]:
            mix.setTrackVol(0, f"{split_hint[:7]}|{currentTime}")

    if ui.getFocused(constants.winName["Browser"]) == True:
        fileType = ui.getFocusedNodeFileType()
        remove_part()

        if ui.getFocusedNodeFileType() <= -100:
            fileType = "Browser"
        else:
            for key, value in constants.FL_node.items():
                fileType = key if ui.getFocusedNodeFileType() == value else fileType

        mix.setTrackName(0, str(fileType))
        mix.setTrackVol(0, ui.getFocusedNodeCaption()[:15])

def remove_part():
    """
    Removes tracks 1 to 7, excluding Track 0
    """
    for y in range(1, 8):
        mix.setTrackExist(y, 0)
    mix.setTrackSel(0, 0)

def remove_all():
    """
    Removes all tracks (0 to 7).
    """
    for y in range(8):
        mix.setTrackExist(y, 0)
    mix.setTrackSel(0, 0)

def clear_part():
    """
    Clears information from tracks 1 to 7, excluding Track 0
    """
    for y in range(1, 8):
        mix.setTrackPanGraph(y, 0)
        mix.setTrackVolGraph(y, 0)
        mix.setTrackSel(0, 0)
        mix.setTrackArm(y, 0)
        mix.setTrackSolo(y, 0)
        mix.setTrackMute(y, 0)
        mix.setTrackName(y, constants.blankEvent)
        mix.setTrackPan(y, constants.blankEvent)
        mix.setTrackVol(y, constants.blankEvent)

def clear_all():
    """
    Clears information from all tracks 0 to 7.
    """
    for y in range(8):
        mix.setTrackPanGraph(y, 0)
        mix.setTrackVolGraph(y, 0)
        mix.setTrackSel(0, 0)
        mix.setTrackArm(y, 0)
        mix.setTrackSolo(y, 0)
        mix.setTrackMute(y, 0)
        mix.setTrackName(y, constants.blankEvent)
        mix.setTrackPan(y, constants.blankEvent)
        mix.setTrackVol(y, constants.blankEvent)