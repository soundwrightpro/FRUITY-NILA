from nihia import mixer as mix
from script.device_setup import constants
import channels
import playlist
import math
import ui
import midi
import transport
import mixer 



def VolTodB(value: float) -> float:
    """
    Converts a linear volume value to decibels.

    Parameters:
    - value (float): The linear volume value.

    Returns:
    - float: The corresponding decibel value.
    """
    if value == 0:
        return "- oo"
    else:
        dB = (math.exp(value * 1.25 * math.log(11)) - 1) * 0.1
        return round(math.log10(dB) * 20, 1)


def updatePanMix(self, track):
    """
    Updates the panning information for a track in the mixer.

    Parameters:
    - track: The track to update.
    """
    pan_value = mixer.getTrackPan(track)
    if pan_value == 0:
        mix.setTrackPan(track, "Centered")
    elif pan_value > 0:
        mix.setTrackPan(track, f"{round(pan_value * 100)}% Right")
    elif pan_value < 0:
        mix.setTrackPan(track, f"{round(pan_value * -100)}% Left")

    for x in range(8):
        if mixer.trackNumber() <= constants.currentUtility - x:
            mix.setTrackPanGraph(x, mixer.getTrackPan(mixer.trackNumber() + x))


def updatePanChannel(self, track):
    """
    Updates the panning information for a track in the Channel Rack.

    Parameters:
    - track: The track to update.
    """
    pan_value = channels.getChannelPan(track)
    if pan_value == 0:
        mix.setTrackPan(track, "Centered")
    elif pan_value > 0:
        mix.setTrackPan(track, f"{round(pan_value * 100)}% Right")
    elif pan_value < 0:
        mix.setTrackPan(track, f"{round(pan_value * -100)}% Left")

    mix.setTrackPanGraph(0, channels.getChannelPan(channels.selectedChannel() + 0))

    for x in range(1, 8):
        if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
            mix.setTrackPanGraph(x, channels.getChannelPan(channels.selectedChannel() + x))


def sendPeakInfo():
    """
    Sends peak meter data to the mixer.
    """
    TrackPeaks = [0] * 16

    if transport.isPlaying():
        if ui.getFocused(constants.winName["Mixer"]):
            for x in range(8):
                if mixer.trackNumber() <= constants.currentUtility - x:
                    TrackPeaks[(x * 2) + 0] = mixer.getTrackPeaks((mixer.trackNumber() + x), midi.PEAK_L)
                    TrackPeaks[(x * 2) + 1] = mixer.getTrackPeaks((mixer.trackNumber() + x), midi.PEAK_R)
        elif ui.getFocused(constants.winName["Channel Rack"]):
            for x in range(8):
                if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
                    if channels.getTargetFxTrack((channels.selectedChannel() + x)) > 0:
                        TrackPeaks[(x * 2) + 0] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel() + x)), midi.PEAK_L)
                        TrackPeaks[(x * 2) + 1] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel() + x)), midi.PEAK_R)
        elif ui.getFocused(constants.winName["Playlist"]):
            TrackPeaks[0] = mixer.getTrackPeaks(0, midi.PEAK_L)
            TrackPeaks[1] = mixer.getTrackPeaks(0, midi.PEAK_R)
        elif ui.getFocused(constants.winName["Browser"]) or ui.getFocused(constants.winName["Playlist"]):
            TrackPeaks[0] = mixer.getTrackPeaks(0, midi.PEAK_L)
            TrackPeaks[1] = mixer.getTrackPeaks(0, midi.PEAK_R)

        for x in range(16):
            TrackPeaks[x] = min(1.1, TrackPeaks[x])
            TrackPeaks[x] = int(TrackPeaks[x] * (127 / 1.1))

        mix.sendPeakMeterData(TrackPeaks)


def timeConvert(timeDisp, currentTime):
    """
    Converts and formats the time display.

    Parameters:
    - timeDisp: The current time display mode.
    - currentTime: The current time.

    Returns:
    - Tuple[str, str]: The formatted time display and current time.
    """
    currentBar = str(playlist.getVisTimeBar())
    currentStep = str(playlist.getVisTimeStep())
    currentTick = str(playlist.getVisTimeTick())

    zeroStr = str(0)

    if 0 <= int(currentStep) <= 9:
        currentTime = f"{currentBar}:{zeroStr}{currentStep}"
    elif int(currentStep) >= 0:
        currentTime = f"{currentBar}:{currentStep}"
    elif int(currentStep) < 0:
        currentTime = str(currentStep)

    if ui.getTimeDispMin() and int(currentStep) >= 0:
        timeDisp = "Min:Sec"
    elif not ui.getTimeDispMin() and int(currentStep) >= 0:
        timeDisp = "Beats:Bar"
    elif int(currentStep) <= 0:
        timeDisp = "REC in..."

    return timeDisp, currentTime


def setTrackVolConvert(trackID: int, value: str):
    """
    Sets the volume for a track in the mixer.

    Parameters:
    - trackID (int): The ID of the track.
    - value (str): The volume value to set.
    """
    if value == "-inf dB":
        value = "- oo dB"
    mix.setTrackVol(trackID, value)


def clamp(value, min_value, max_value):
    """
    Clamps the given value within the specified range.

    Args:
        value: The value to be clamped.
        min_value: The minimum allowed value.
        max_value: The maximum allowed value.

    Returns:
        The clamped value.
    """
    return max(min(value, max_value), min_value)