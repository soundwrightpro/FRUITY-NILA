"""Mixer Module (FL Studio built-in)

Allows you to control and interact with the FL Studio Mixer, and with
effects tracks.

NOTES:
 * Mixer tracks are zero-indexed
"""

import midi

def trackNumber() -> int:
    """Returns the index of the first currently selected mixer track.

    Returns:
     * `int`: selected mixer track
    
    Included since API version 1
    """

def getTrackInfo(mode: int) -> int:
    """Returns the index of a special mixer track depending on `mode`.
    
    This function can serve to help potentially future-proof scripts by ensuring
    that they continue to use the correct indexes for mixer tracks

    Args:
     * `mode` (`int`): Determined the type of information provided:
            * `TN_Master` (`0`): Index of master track
            * `TN_FirstIns` (`1`): Index of first insert track
            * `TN_LastIns` (`2`): Index of last insert track
            * `TN_Sel` (`3`): Index of the "current" track (the one with the
              large peak meter docked to the left).

    Returns:
     * `int`: requested track index
    
    Included since API version 1
    """

def setTrackNumber(trackNumber: int, flags:int=0) -> None:
    """Selects the mixer track at `trackNumber`.
    
    NOTE: All functionality except for scrolling flag can be replicated more
    easily using `mixer.selectTrack()`.

    Args:
     * `trackNumber` (`int`): the track index to select
     * `flags` (`int`, optional): Options to do with new track selection.
            * `curfxScrollToMakeVisible` (`1`): Scroll to make the 
              newly-selected track visible.
            * `curfxCancelSmoothing` (`2`): Effect unknown
            * `curfxNoDeselectAll` (`4`): Prevent the deselection of other
              selected tracks??? Doesn't seem to work.
            * `curfxMinimalLatencyUpdate` (`8`): Effect unknown
            Defaults to `0`.
    
    Included since API version 1
    """

def trackCount() -> int:
    """Returns the number of tracks available on the mixer.
    Tracks range = `0 - (trackCount()-1)`. Includes master and "current track"
    tracks.

    Returns:
     * `int`: number of tracks
        
    Included since API version 1
    """

def getTrackName(index: int) -> str:
    """Returns the name of the track at `index`.

    Args:
     * `index` (`int`): track index

    Returns:
     * `str`: name of track.
        
    Included since API version 1
    """

def setTrackName(index: int, name: str) -> None:
    """Sets the name of track at `index`
    
    Setting the name to an empty string will reset the name of the track to
    its default.

    Args:
     * index (`int`): index of mixer track
     * name (`str`): new name
        
    Included since API version 1
    """

def getTrackColor(index: int) -> int:
    """Returns the colour of the track at `index`.

    Args:
     * `index` (`int`): track index

    Returns:
     * `int`: colour of track (0x--RRGGBB)
        
    Included since API version 1
    """

def setTrackColor(index: int, color: int) -> None:
    """Sets the colour of the track at `index`.

    Args:
     * `index` (`int`): track index
     * `color` (`int`): colour of track (0x--RRGGBB)
        
    Included since API version 1
    """

def isTrackArmed(index: int) -> bool:
    """Returns whether the track at `index` is armed for recording

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether track is armed
        
    Included since API version 1
    """

def armTrack(index: int) -> None:
    """Toggles whether the track at index is armed for recording

    Args:
     * `index` (`int`): track index
        
    Included since API version 1
    """

def isTrackSolo(index: int) -> bool:
    """Returns whether the track at `index` is solo

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether track is solo
        
    Included since API version 1
    """

def soloTrack(index: int) -> None:
    """Toggles whether the track at index is solo

    Args:
     * `index` (`int`): track index
        
    Included since API version 1
    """

def isTrackEnabled(index: int) -> bool:
    """Returns whether the track at `index` is enabled

    NOTE: This seems to be functionally identical to `not isTrackMuted()`.

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether track is enabled
        
    Included since API version 1
    """

def isTrackAutomationEnabled(index: int, plugIndex: int) -> bool:
    """Returns whether the plugin at `plugIndex` on track at `index` has 
    automation enabled.

    Args:
     * `index` (`int`): track index
     * `plugIndex` (`int`): index of plugin

    Returns:
     * `bool`: whether automation is enabled for the track
        
    Included since API version 1
    """

def enableTrack(index: int) -> None:
    """Toggles whether the track at `index` is enabled.
    
    NOTE: This seems to be functionally identical to `muteTrack()`.

    Args:
     * index (`int`): track index
        
    Included since API version 1
    """

def isTrackMuted(index: int) -> bool:
    """Returns whether the track at `index` is muted

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether track is solo
        
    Included since API version 2
    """

def muteTrack(index: int) -> None:
    """Toggles whether the track at index is muted

    Args:
     * `index` (`int`): track index
        
    Included since API version 2
    """

def isTrackMuteLock(index: int) -> bool:
    """Returns whether the mute state of the track at `index` is locked.
    
    If this is true, the mute status of this track won't change when other 
    tracks are solo'd or unsolo'd.

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether track is mute locked
        
    Included since API version 13
    """

def getTrackPluginId(index: int, plugIndex: int) -> int:
    """Returns the plugin ID of the plugin on track `index` in slot `plugIndex`

    HELP WANTED: what is a plugin ID?

    Args:
     * index (`int`): track index
     * plugIndex (`int`): plugin index

    Returns:
     * `int`: plugin ID
        
    Included since API version 1
    """

def isTrackPluginValid(index: int, plugIndex: int) -> bool:
    """Returns whether a plugin on track `index` in slot `plugIndex` is valid
    (has been loaded, so the slot isn't empty)

    Args:
     * `index` (`int`): track index
     * `plugIndex` (`int`): plugin index

    Returns:
     * `bool`: whether track is mute locked
        
    Included since API version 1
    """

def getTrackVolume(index: int, mode:int=0) -> float:
    """Returns the volume of the track at `index`. Volume lies within the range
    `0.0` - `1.0`. Note that the default value is `0.8`. Use the `mode` flag to
    get the volume in decibels.

    Args:
     * `index` (`int`): track index
     * `mode` (`int`, optional): whether to return the volume as a value between
       0 and 1, or in decibels.

    Returns:
     * `float`: volume of track
    
    Included since API version 1
    """

def setTrackVolume(index: int, volume: float,  pickupMode:int=0) -> None:
    """Sets the volume of the track at `index`. Volume lies within the range
    `0.0` - `1.0`. Note that the default value is `0.8`. Use the pickup mode
    flag to set pickup options.

    Args:
     * `index` (`int`): track index
     * `volume` (`float`): volume of track
     * `pickupMode` (`int`, optional): define the pickup behaviour. Refer to
       the [manual](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#pickupModes)
    
    
    Included since API version 1
    """

def getTrackPan(index: int) -> float:
    """Returns the pan of the track at `index`. Pan lies within the range
    100% left (`-1.0`) - 100% right (`1.0`). Note that the default value is 
    `0.0`.

    Args:
     * `index` (`int`): track index

    Returns:
     * `float`: pan of track
    
    Included since API version 1
    """

def setTrackPan(index: int, pan: float, pickupMode:int=0) -> None:
    """Sets the pan of the track at `index`. Pan lies within the range
    100% left (`-1.0`) - 100% right (`1.0`). Note that the default value is 
    `0.0`. Use the pickup mode flag to set pickup options.

    Args:
     * `index` (`int`): track index
     * `pan` (`float`): pan of track
     * `pickupMode` (`int`, optional): define the pickup behaviour. Refer to
       the [manual](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#pickupModes)
    
    
    Included since API version 1
    """

def getTrackStereoSep(index: int) -> float:
    """Returns the stereo separation of the track at `index`. Stereo separation 
    lies within the range 100% centred (`-1.0`) - 100% separated (`1.0`). Note 
    that the default value is `0.0`.

    Args:
     * `index` (`int`): track index

    Returns:
     * `float`: stereo separation of track
    
    Included since API version 12
    """

def setTrackStereoSep(index: int, pan: float, pickupMode:int=0) -> None:
    """Sets the stereo separation of the track at `index`. Stereo separation 
    lies within the range 100% centred (`-1.0`) - 100% separated (`1.0`). Note 
    that the default value is `0.0`. Use the pickup mode flag to set pickup
    options.

    Args:
     * `index` (`int`): track index
     * `sep` (`float`): stereo separation of track
     * `pickupMode` (`int`, optional): define the pickup behaviour. Refer to
       the [manual](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#pickupModes)
    
    Included since API version 12
    """

def isTrackSelected(index: int) -> bool:
    """Returns whether the track at `index` is selected

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether the track is selected
    
    Included since API version 1
    """

def selectTrack(index: int) -> None:
    """Toggles whether the track at `index` is selected.

    Args:
     * `index` (`int`): track index
    
    Included since API version 1
    """

def selectAll() -> None:
    """Selects all tracks
    
    Included since API version 1
    """

def deselectAll() -> None:
    """Deselects all tracks
    
    Included since API version 1
    """

def setRouteTo(index: int, destIndex: int, value: int) -> None:
    """Route the track at `index` to the track at `destIndex`.
    
    Ensure that after all routing changes are made, the `afterRoutingChanged()`
    function is called to allow the UI to update correctly.

    Args:
     * `index` (`int`): source track index
     * `destIndex` (`int`): destination track index
     * `value` (`int`): whether to enable the route (`1`) or disable it (`0`)
    
    Included since API version 1
    """

def getRouteSendActive(index: int, destIndex: int) -> bool:
    """Return whether the track at `index` is routed to the track at `destIndex`

    Args:
     * `index` (`int`): source track
     * `destIndex` (`int`): destination track

    Returns:
     * `bool`: whether the tracks are routed
    
    Included since API version 1
    """

def afterRoutingChanged() -> None:
    """Notify FL Studio that channel routings have changed.
    
    Included since API version 1
    """

def getEventValue(index: int, value:int=midi.MaxInt, smoothTarget:int=1) -> int:
    """Returns event value from MIDI
    
    HELP WANTED: What does this do?

    Args:
     * `index` (`int`): ???
     * `value` (`int`, optional): ???. Defaults to 'MaxInt'.
     * `smoothTarget` (`int`, optional): ???. Defaults to 1.

    Returns:
     * `int`: ???
    
    Included since API version 1
    """

def remoteFindEventValue(index: int, flags:int=0) -> float:
    """Returns event value
    
    HELP WANTED: What does this do?

    Args:
     * `index` (`int`): ???
     * `flags` (`int`, optional): ???. Defaults to 0.

    Returns:
     * `float`: ???
    
    Included since API version 1
    """

def getEventIDName(index: int, shortname:int=0) -> str:
    """Returns event name for event at `index`
    
    HELP WANTED: What does this do?

    NOTE: The official documentation states that this function returns `None`,
    but it actually returns a `str`. These stubs document the actual behaviour.

    Args:
     * `index` (`int`): ???
     * `shortname` (`int`, optional): ???. Defaults to 0.

    Returns:
     * `str`: name of event?
    
    Included since API version 1
    """

def getEventIDValueString(index: int, value: int) -> str:
    """Returns event value as a string
    
    HELP WANTED: What does this do?

    Args:
     * `index` (`int`): ???
     * `value` (`int`): ???.

    Returns:
     * `str`: ???
    
    Included since API version 1
    """

def getAutoSmoothEventValue(index: int, locked:int=1) -> int:
    """Returns auto smooth event value
    
    HELP WANTED: What does this do?

    Args:
     * `index` (`int`): ???
     * `locked` (`int`, optional): ???. Defaults to 1.

    Returns:
     * `int`: ???
    
    Included since API version 1
    """

def automateEvent(index: int, value: int, flags: int, speed:int=0, 
                  isIncrement:int=0, res:float=midi.EKRes) -> int:
    """Automate event
    
    HELP WANTED: What does this do?

    Args:
     * `index` (`int`): ???
     * `value` (`int`): ???
     * `flags` (`int`): refer to the [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#RecEventFlags).
     * `speed` (`int`, optional): ???. Defaults to 0.
     * `isIncrement` (`int`, optional): ???. Defaults to 0.
     * `res` (`float`, optional): ???. Defaults to midi.EKRes.

    Returns:
     * `long`: ???
    
    Included since API version 1
    """

def getTrackPeaks(index: int, mode: int) -> float:
    """Returns the current audio peak value for the track at `index`.

    Args:
     * `index` (`int`): track index
     * `mode` (`int`): track peaks mode (see the [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#TrackPeakMode))

    Returns:
     * `float`: track peak values:
            * `0.0`: silence
            * `1.0`: 0 dB
            * `>1.0`: clipping
    
    Included since API version 1
    """

def getTrackRecordingFileName(index: int) -> str:
    """Returns the file name for audio being recorded on the track at `index`.

    NOTE: Files can't be opened in FL Studio's Python interpreter due to disk 
    access being disabled for security reasons.

    Args:
     * `index` (`int`): track index

    Returns:
     * `str`: filename
    
    Included since API version 1
    """
    
def linkTrackToChannel(mode: int) -> None:
    """Link a mixer track to a channel.
    
    HELP WANTED: How does this function call work?

    Args:
     * `mode` (`int`): link mode
            * `ROUTE_ToThis` (`0`)
            * `ROUTE_StartingFromThis` (`1`)
    
    Included since API version 1
    """

def getSongStepPos() -> int:
    """Returns the current position in the song, measured in steps.

    Returns:
     * `int`: song position
    
    Included since API version 1
    """

def getCurrentTempo(asInt:int=0) -> 'int | float':
    """Returns the current tempo of the song
    
    Args:
     * `asInt` (`int`, optional): whether to return the tempo as an `int` (`1`)
       or not (`0`). Defaults to `0`.
    
    Returns:
     * `int` or `float`: Current tempo
    
    Included since API version 1
    """

def getRecPPS() -> int:
    """Returns the recording PPS
    
    HELP WANTED: What is PPS?

    Returns:
     * `int`: recording PPS
    
    Included since API version 1
    """

def getSongTickPos(mode:int=midi.ST_Int) -> 'int | float':
    """Returns the current position in the song, measured in ticks.

    Returns:
     * `int` or `float`: song position in ticks
    
    Included since API version 1
    """

def getLastPeakVol(section: int) -> float:
    """Returns last peak volume.

    Args:
     * `section` (`int`): audio channel
            * `0`: left channel
            * `1`: right channel

    Returns:
     * `float`: last peak volume (`0.0` for silence, `1.0` for 0 dB, `>1.0` for 
       clipping)
    
    Included since API version 9
    """

def getTrackDockSide(index: int) -> int:
    """Returns the dock side of the mixer for track at `index`

    Args:
     * `index` (`int`): track index

    Returns:
     * `int`: docking side:
            * `0`: Left
            * `1`: Centre (default)
            * `2`: Right 
    
    Included since API version 13
    """
