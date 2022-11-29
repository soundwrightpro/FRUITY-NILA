"""Transport Module (FL Studio built-in)

Handles transport in FL Studio (for example play/pause or record)
"""

import midi

def globalTransport(command: int, value: int, pmeflags:int=midi.PME_System,
                    flags=midi.GT_ALL) -> int:
    """Used as a generic way to run transport commands if a specific function
    doesn't exist for it.
    
    WARNING: It is not recommended to use this function if a dedicated 
    function is available for it. Its usage can make code difficult to read and
    comprehend. Almost all functionality provided by this function can be done
    more easily and cleanly by using the dedicated functions.
    
    WARNING: Some commands will echo keypresses (such as `FPT_F1`), meaning they
    can affect windows outside FL Studio. Make sure you test your code 
    thoroughly if you decide to use this function.

    Args:
     * `command` (`int`): command to execute, refer to 
       [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#globalTransportCommands)
     * `value` (`int`): ???
     * `pmeflags` (`int`, optional): current PME Flags. Defaults to 
       `midi.PME_System`.
     * `flags` (`int`, optional): ??? Refer to 
       [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#globalTransportFlags)

    Returns:
     * `int`: ???
    
    Included since API version 1
    """

def start() -> None:
    """Start or pause playback (play/pause)
    
    Included since API version 1
    """

def stop() -> None:
    """Stop playback
    
    Included since API version 1
    """

def record() -> None:
    """Toggles recording
    
    Included since API version 1
    """

def isRecording() -> bool:
    """Returns whether recording is enabled

    Returns:
     * `bool`: whether recording is enabled
    
    Included since API version 1
    """

def getLoopMode() -> int:
    """Returns the current looping mode

    Returns:
     * `int`: looping mode:
            * `0`: Pattern
            * `1`: Song
    
    Included since API version 1
    """

def setLoopMode() -> None:
    """Toggles the looping mode between pattern and song
    
    Included since API version 1
    """
    
def getSongPos(mode:int=-1) -> 'float | int':
    """Returns the playback position
    
    NOTE: This will set the position in the song in song mode, or the position
    in the pattern

    Args:
     * `mode` (`int`, optional): mode for return:
            * [default] (`-1`): as a fraction of the total length between `0` 
              and `1` (eg `0.5` would indicate we were half-way through the 
              song). Returns as `float`.
            * `SONGLENGTH_MS` (`0`): milliseconds (as `int`)
            * `SONGLENGTH_S` (`1`): seconds (as `int`)
            * `SONGLENGTH_ABSTICKS` (`2`): ticks (as `int`)
            * `SONGLENGTH_BARS` (`3`): bars-steps-ticks format, bars component
              (as `int`)
            * `SONGLENGTH_STEPS` (`4`): bars-steps-ticks format, steps component
              (as `int`)
            * `SONGLENGTH_TICKS` (`5`): bars-steps-ticks format, ticks component
              (as `int`)

    NOTE: An overall bars-steps-ticks position can be gathered through making
    three calls to the function as follows:
    ```py
    bars = transport.getSongPosition(3)
    steps = transport.getSongPosition(4)
    ticks = transport.getSongPosition(5)
    overall_str = f"{bars}:{steps}:{ticks}"
    ```

    Returns:
     * `float` or `int`: song position
    
    Included since API version 1, with optional parameter added in API version 3
    """

def setSongPos(position:'float | int', mode:int=-1) -> None:
    """Sets the playback position
    
    NOTE: This will set the position in the song in song mode, or the position
    in the pattern

    Args:
     * `position` (`float` or `int`): new song position (type depends on `mode`).
     * `mode` (`int`, optional): mode for `position`:
            * [default] (`-1`): as a fraction of the total length between `0` 
              and `1` (eg `0.5` would indicate we were half-way through the 
              song). Returns as `float`.
            * `SONGLENGTH_MS` (`0`): milliseconds (as `int`)
            * `SONGLENGTH_S` (`1`): seconds (as `int`)
            * `SONGLENGTH_ABSTICKS` (`2`): ticks (as `int`)
            * `SONGLENGTH_BARS` (`3`): bars-steps-ticks format, bars component
              (as `int`)
            * `SONGLENGTH_STEPS` (`4`): bars-steps-ticks format, steps component
              (as `int`)
            * `SONGLENGTH_TICKS` (`5`): bars-steps-ticks format, ticks component
              (as `int`)
    
    WARNING: Positions currently won't work when using bars (`mode = 3`), 
    steps (`mode = 4`) or ticks (`mode = 5`).
    
    Included since API version 1, with optional parameter added in API version 4
    """

def getSongLength(mode: int) -> int:
    """Returns the total length of the song
    
    NOTE: This only applies to the full song, not to the currently selected
    pattern when in pattern mode. It will NOT return the length of the current 
    pattern. For that, use `patterns.getPatternLength()` with the index of the
    current pattern.

    Args:
     * `mode` (`int`): mode for length:
            * `SONGLENGTH_MS` (`0`): milliseconds
            * `SONGLENGTH_S` (`1`): seconds
            * `SONGLENGTH_ABSTICKS` (`2`): ticks
            * `SONGLENGTH_BARS` (`3`): bars-steps-ticks format, bars component
            * `SONGLENGTH_STEPS` (`4`): bars-steps-ticks format, steps component
            * `SONGLENGTH_TICKS` (`5`): bars-steps-ticks format, ticks component

    NOTE: The official documentation states that this function has no return,
    but in practice, it returns an `int`. The actual behaviour is used by this
    documentation.

    Returns:
     * `int`: song length
    
    Included since API version 3
    """

def getSongPosHint() -> str:
    """Returns a hint for the current playback position as `"bars:steps:ticks"`.
    
    NOTE: This applies to both pattern mode and song mode

    Returns:
     * `str`: song position
    
    Included since API version 1
    """

def isPlaying() -> bool:
    """Returns `True` if playback is currently occurring.

    Returns:
     * `bool`: whether playback is active
    
    Included since API version 1
    """

def markerJumpJog(value: int, flags:int=midi.GT_All) -> None:
    """Jump to a marker position, where `value` is an delta (increment) value.

    Args:
     * `value` (`int`): delta
     * `flags` (`int`, optional): ??? Refer to 
       [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#globalTransportFlags)
    
    Included since API version 1
    """

def markerSelJog(value: int, flags:int=midi.GT_All) -> None:
    """Select a marker, where `value` is an delta (increment) value.

    Args:
     * `value` (`int`): delta
     * `flags` (`int`, optional): ??? Refer to 
       [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#globalTransportFlags)
    
    Included since API version 1
    """

def getHWBeatLEDState() -> int:
    """Returns the state of the beat indicator.

    HELP WANTED: I couldn't get this to return anything other than zero

    Returns:
     * `int`: beat indicator state
    
    Included since API version 1
    """

def rewind(startStop: int, flags:int=midi.GT_All) -> None:
    """Rewinds the playback position.

    NOTE: Rewinding should be considered as a toggle. All calls to this function
    beginning rewinding with the `SS_Start` or `SS_StartStep` should have a pair 
    call where rewinding is stopped using the `SS_Stop` option, otherwise FL 
    Studio will rewind forever.

    Args:
     * `startStop` (`int`): start-stop option
            * `SS_Stop` (`0`): Stop movement
            * `SS_StartStep` (`1`): Start movement, but only if FL Studio is in
              step editing mode
            * `SS_Start` (`2`); Start movement
     * `flags` (`int`, optional): ??? Refer to 
       [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#globalTransportFlags)
    
    Included since API version 1
    """

def fastForward(startStop: int, flags:int=midi.GT_All) -> None:
    """Fast-fowards the playback position.

    NOTE: Fast-forwarding should be considered as a toggle. All calls to this 
    function beginning fast-forwarding with the `SS_Start` or `SS_StartStep` 
    should have a pair call where fast-forwarding is stopped using the `SS_Stop` 
    option, otherwise FL Studio will fast-forward forever.

    Args:
     * `startStop` (`int`): start-stop option
            * `SS_Stop` (`0`): Stop movement
            * `SS_StartStep` (`1`): Start movement, but only if FL Studio is in
              step editing mode
            * `SS_Start` (`2`); Start movement
     * `flags` (`int`, optional): ??? Refer to 
       [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#globalTransportFlags)
    
    Included since API version 1
    """

def continuousMove(speed: int, startStop: int) -> None:
    """Sets playback speed, allowing a scrub-like functionality

    NOTE: scrubbing should be considered as a toggle. All calls to this 
    function beginning scrubbing with the `SS_Start` or `SS_StartStep` 
    should have a pair call where scrubbing is stopped using the `SS_Stop` 
    option, otherwise FL Studio will scrub forever.

    Args:
     * `speed` (`int`): speed multiplier. Negative means reverse, `0` is 
       stopped, and `1` is normal playback speed.
     * `startStop` (`int`): start-stop option
            * `SS_Stop` (`0`): Stop movement
            * `SS_StartStep` (`1`): Start movement, but only if FL Studio is in
              step editing mode
            * `SS_Start` (`2`); Start movement
    
    Included since API version 1
    """

def continuousMovePos(speed: int, startStop:int) -> None:
    """Sets playback speed, allowing a scrub-like functionality

    HELP WANTED: How is this different to `continuousMove()`?

    NOTE: scrubbing should be considered as a toggle. All calls to this 
    function beginning scrubbing with the `SS_Start` or `SS_StartStep` 
    should have a pair call where scrubbing is stopped using the `SS_Stop` 
    option, otherwise FL Studio will scrub forever.

    Args:
     * `speed` (`int`): speed multiplier. Negative means reverse, `0` is 
       stopped, and `1` is normal playback speed.
     * `startStop` (`int`): start-stop option
            * `SS_Stop` (`0`): Stop movement
            * `SS_StartStep` (`1`): Start movement, but only if FL Studio is in
              step editing mode
            * `SS_Start` (`2`); Start movement
    
    Included since API version 2
    """

def setPlaybackSpeed(speedMultiplier: float) -> None:
    """Sets a playback speed multiplier.

    NOTE: This differs from the `continuousMove` function as it only controls
    speed when playback is active, rather than scrubbing through song or
    pattern regardless of whether playback is active.

    Args:
     * `speedMultiplier` (`float`): speed:
            * `1.0`: Normal speed
            * `0.25`: Minimum speed
            * `4.0`: Maximum speed
    
    Included since API version 1
    """
