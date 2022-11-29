"""Playlist Module (FL Studio built-in)

Allows you to control and interact with the FL Studio Playlist.

NOTES:
 * Playlist tracks are 1-indexed.

KNOWN ISSUES:
 * When a track index is required, track zero can be accessed, but does not give
   results (as track indexes start at 1)
 * Trying to access track `500` raises an Index out of range `TypeError`

HELP WANTED:
 * Explanations for display zone functions
 * Explanations for live performance related functions
"""

import midi

def trackCount() -> int:
    """Returns the number of tracks on the playlist.
    Includes empty tracks.

    Returns:
     * `int`: track count on playlist

    Included since API version 1
    """

def getTrackName(index: int) -> str:
    """Returns the name of the track at `index`
    For unnamed tracks, returns "Track `n`" where `n` is `index` + 1
    
    Note that playlist track indexes start at 1

    Args:
     * `index` (`int`): track index

    Returns:
     * `str`: track name

    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
    
    Included since API version 1
    """

def setTrackName(index: int, name: str) -> None:
    """Sets the name of the track at `index`
    Setting the name to an empty string ("") will reset the name to "Track n"
    
    Note that playlist track indexes start at 1

    Args:
     * `index` (`int`): track index

    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
    
    Included since API version 1
    """

def getTrackColor(index: int) -> int:
    """Returns the colour of the track at `index`
    
    Note that colours can be split into or built from components using the
    functions provided in the module `utils`
    * `ColorToRGB()`
    * `RGBToColor()`
    
    Note that playlist track indexes start at 1

    Args:
     * `index` (`int`): track index

    Returns:
     * `int`: track colour (0x--RRGGBB)

    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
    
    Included since API version 1
    """

def setTrackColor(index: int, color: int) -> None:
    """Sets the colour of the track at `index`
    
    Note that colours can be split into or built from components using the
    functions provided in the module `utils`
    * `ColorToRGB()`
    * `RGBToColor()`
    
    Note that playlist track indexes start at 1

    Args:
     * `index` (`int`): track index
     * `color` (`int`): track colour (0x--RRGGBB)

    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
    
    Included since API version 1
    """

def isTrackMuted(index: int) -> bool:
    """Returns whether the track at `index` is muted

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether track is muted
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     
    Included since API version 1
    """

def muteTrack(index: int) -> None:
    """Toggle whether the track at `index` is muted. An unmuted track will 
    become muted and a muted track will become unmuted.

    Args:
     * `index` (`int`): track index
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     
    Included since API version 1
    """

def isTrackMuteLock(index: int) -> bool:
    """Returns whether the mute status of the track at `index` is locked (meaning
    that solo/unsolo commands won't affect its mute status).

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether track's mute status is locked
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     
    Included since API version 2
    """

def muteTrackLock(index: int) -> None:
    """Toggle whether the track at `index`'s mute status is locked (meaning that 
    solo/unsolo commands won't affect its mute status).

    Args:
     * `index` (`int`): track index
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     
    Included since API version 2
    """

def isTrackSolo(index: int) -> bool:
    """Returns whether the track at `index` is solo

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether track is muted
            * `1`: True
            * `0`: False
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     
    Included since API version 1
    """

def soloTrack(index: int, value:int = -1) -> None:
    """Toggle whether the track at `index` is solo. An unsolo track will become
    solo and a solo track will become unsolo. If `value` is provided, it will
    control what the new value will be (`1`: solo, `0`: unsolo).

    Args:
     * `index` (`int`): track index
     * `value` (`int`, optional): new solo value
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     
    Included since API version 1
    """

def isTrackSelected(index: int) -> bool:
    """Returns whether the track at `index` is selected

    Args:
     * `index` (`int`): track index

    Returns:
     * `bool`: whether track is selected
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     
    Included since API version 12
    """

def selectTrack(index: int) -> None:
    """Toggle whether the track at `index` is selected. A deselected track will 
    become selected and a selected track will become deselected.

    Args:
     * `index` (`int`): track index
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     
    Included since API version 12
    """

def selectAll() -> None:
    """Select all tracks on the playlist

    Included since API version 12
    """

def deselectAll() -> None:
    """Deselect all tracks on the playlist

    Included since API version 12
    """

def getTrackActivityLevel(index: int) -> float:
    """Returns the activity level of the track at `index`. This value is a float
    in the range of 0.0 - 0.5 representing whether an unmuted playlist clip is 
    active at the playhead. Compare to `playlist.getTrackActivityLevelVis()`.

    Args:
     * `index` (`int`): track index

    Returns:
     * `float`: activity level
            * `0.0`: No clip is active
            * `0.5`: A clip is active at the play head
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     * This function will only return 0.0 or 0.5, and nothing in between. There
       is no documentation for whether this is by design.
     
    Included since API version 1
    """

def getTrackActivityLevelVis(index: int) -> float:
    """Returns the visual activity level of the track at `index`. This value is a
    float in the range of 0.0 - 1.0 representing whether an unmuted playlist 
    clip is active at the playhead and how recently a note-on event was played 
    on this track.

    Args:
     * `index` (`int`): track index

    Returns:
     * float: activity level
            * `0.0`: No clip is active
            * `0.5 - 1.0`: A clip is active at the play head. Higher values 
              represent more recent note-on events.
    
    Raises:
     * `TypeError`: Index out of range
    
    Known Issues:
     * Trying to access track 500 raises an Index out of range `TypeError`
     
    Included since API version 1
    """

def getDisplayZone() -> int:
    """Returns the current display zone in the playlist or zero if none.

    HELP WANTED: Explanation for what a display zone is.

    Returns:
     * `int`: current display zone
    
    Included since API version 1
    """

def lockDisplayZone(index: int, value: int) -> None:
    """Lock display zone at `index`.

    HELP WANTED: Explanation for what a display zone is.
    HELP WANTED: Explanation for parameters.

    Args:
     * `index` (`int`): ???
     * `value` (`int`): ???
    
    Included since API version 1
    """

def liveDisplayZone(left: int, top: int, right: int, bottom: int,
                    duration:int=0) -> None:
    """Set the display zone in the playlist to the specified co-ordinates. Use 
    optional `duration` parameter to make display zone temporary

    HELP WANTED: Explanation for what a display zone is.
    HELP WANTED: Explanation for parameters.

    Args:
     * `left` (`int`): ???
     * `top` (`int`): ???
     * `right` (`int`): ???
     * `bottom` (`int`): ???
     * `duration` (`int`, optional): ???. Defaults to `0`.
    
    Included since API version 1
    """

def getLiveLoopMode(index: int) -> int:
    """Get live loop mode
    
    HELP WANTED: Explanation for parameters.

    Args:
     * `index` (`int`): track index???

    Returns:
     * `int`: live loop mode:
            * `0` (`LiveLoop_Stay`): Stay
            * `1` (`LiveLoop_OneShot`): One shot
            * `2` (`LiveLoop_MarchWrap`): March and wrap
            * `3` (`LiveLoop_MarchStay`): March and stay
            * `4` (`LiveLoop_MarchStop`): March and stop
            * `5` (`LiveLoop_Random`): Random
            * `6` (`LiveLoop_ExRandom`): Random, avoiding previous clip?
    
    Included since API version 1
    """

def getLiveTriggerMode(index: int) -> int:
    """Get live trigger mode
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index???

    Returns:
     * `int`: live trigger mode:
            * `0` (`LiveTrig_Retrigger`): Retrigger
            * `1` (`LiveTrig_Hold`): Hold and stop
            * `2` (`LiveTrig_HMotion`): Hold and motion
            * `3` (`LiveTrig_Latch`): Latch
    
    Included since API version 1
    """

def getLivePosSnap(index: int) -> int:
    """Get live position snap
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index???

    Returns:
     * `int`: live position snap:
            * `0` (`LiveSnap_Off`): No snap
            * `1` (`LiveSnap_Fourth`): 1/4 beat
            * `2` (`LiveSnap_Half`): 1/2 beat
            * `3` (`LiveSnap_One`): 1 beat
            * `4` (`LiveSnap_Two`): 2 beats
            * `5` (`LiveSnap_Four`): 4 beats
            * `6` (`LiveSnap_Auto`): Auto
    
    Included since API version 1
    """

def getLiveTrigSnap(index: int) -> int:
    """Get live trigger snap
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index???

    Returns:
     * `int`: live position snap:
            * `0` (`LiveSnap_Off`): No snap
            * `1` (`LiveSnap_Fourth`): 1/4 beat
            * `2` (`LiveSnap_Half`): 1/2 beat
            * `3` (`LiveSnap_One`): 1 beat
            * `4` (`LiveSnap_Two`): 2 beats
            * `5` (`LiveSnap_Four`): 4 beats
            * `6` (`LiveSnap_Auto`): Auto
    
    Included since API version 1
    """

def getLiveStatus(index: int, mode:int=midi.LB_Status_Default) -> int:
    """Returns the live status for track at `index`
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index
     * `mode` (`int`, optional): live status mode. Defaults to 'LB_Status_Default'.

    Returns:
     * `int`: live status of track:
            Refer to [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#getLiveStatusMode)
    
    Included since API version 1
    """

def getLiveBlockStatus(index: int, blockNum:int, mode:int=midi.LB_Status_Default) -> int:
    """Returns the live block status for track at `index` and for block 
    `blockNum`
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index
     * `blockNum` (`int`): block number
     * `mode` (`int`, optional): live status mode. Defaults to 'LB_Status_Default'.

    Returns:
     * `int`: live status of track:
       Refer to [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#getLiveStatusMode).
    
    Included since API version 1
    """

def getLiveBlockColor(index: int, blockNum: int) -> int:
    """Returns the colour of block on track `index` at position `blockNum`
    
    HELP WANTED: Explanation.

    Note that colours can be split into or built from components using the
    functions provided in the module `utils`
    * `ColorToRGB()`
    * `RGBToColor()`

    Args:
     * `index` (`int`): track index
     * `blockNum` (`int`): block number

    Returns:
     * `int`: block colour (`0x--RRGGBB`)
    
    Included since API version 1
    """

def triggerLiveClip(index: int, subNum:int, flags: int, velocity:int=-1) -> None:
    """Triggers live clip for track at `index` and for block `subNum`
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index
     * `subNum` (`int`): block number (usually `blockNum`)
     * `flags` (`int`): live clip trigger flags.
       refer to [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#triggerLiveClipFlags).
     * `velocity` (`int`, optional): velocity for triggering clip. Defaults to `-1`.

    Included since API version 1
    """

def refreshLiveClip(index: int, value: int) -> None:
    """Triggers live clip for track at `index` and for block `subNum`
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index
     * `value` (`int`): ???

    Included since API version 1
    """

def incLivePosSnap(index: int, value: int) -> None:
    """Increase live position snap for track at `index`
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index
     * `value` (`int`): ???

    Included since API version 1
    """

def incLiveTrigSnap(index: int, value: int) -> None:
    """Increase live trigger snap for track at `index`
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index
     * `value` (`int`): ???

    Included since API version 1
    """

def incLiveLoopMode(index: int, value: int) -> None:
    """Increase live loop mode for track at `index`
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index
     * `value` (`int`): ???

    Included since API version 1
    """

def incLiveTrigMode(index: int, value: int) -> None:
    """Increase live trigger mode for track at `index`
    
    HELP WANTED: Explanation.

    Args:
     * `index` (`int`): track index
     * `value` (`int`): ???

    Included since API version 1
    """

def getVisTimeBar() -> int:
    """Returns the time bar

    HELP WANTED: Explanation. I could only get this function to return `0`.

    Returns:
     * `int`: time bar

    Included since API version 1
    """

def getVisTimeTick() -> int:
    """Returns the time tick

    HELP WANTED: Explanation. I could only get this function to return `0`.

    Returns:
     * `int`: time tick

    Included since API version 1
    """

def getVisTimeStep() -> int:
    """Returns the time bar

    HELP WANTED: Explanation. I could only get this function to return `0`.

    Returns:
     * `int`: time step

    Included since API version 1
    """
