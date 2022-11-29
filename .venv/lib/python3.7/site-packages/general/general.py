"""General Module (FL Studio built-in)

Handles general interactions with FL Studio
"""

def saveUndo(undoName: str, flags: int, update:int=1) -> None:
    """Save an undo point into FL Studio's history.

    Args:
     * `undoName` (`str`): a descriptive name for the undo point
     * `flags` (`int`): Any combination of the following flags, combined using 
       the logical or (`|`) operator:
            * `UF_None` (`0`): No flags
            * `UF_EE` (`1`): Changes in event editor
            * `UF_PR` (`2`): Changes in piano roll
            * `UF_PL` (`4`): Changes in playlist
            * `UF_KNOB` (`32`): Changes to an automated control
            * `UF_AudioRec` (`256`): Audio recording
            * `UF_AutoClip` (`512`): Automation clip
            * `UF_PRMarker` (`1024`): Piano roll (pattern) marker
            * `UF_PLMarker` (`2048`): Playlist marker
            * `UF_Plugin` (`4096`): Plugin
            * `UF_SSLooping` (`8192`): Step sequencer looping
            * `UF_Reset` (`65536`): Reset undo history
     * `update` (`int`, optional): ???. Defaults to 1.
    
    Included since API version 1
    """

def undo() -> int:
    """Perform an undo toggle, much like pressing Ctrl+Z. If the position in the
    undo history is at the most recent, it will undo, otherwise, it will redo.

    Returns:
     * `int`: ???
    
    Included since API version 1
    """

def undoUp() -> int:
    """Move up in the undo history. This is much like undo in most programs

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def undoDown() -> int:
    """Move down in the undo history. This is much like redo in most programs

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def undoUpDown(value: int) -> int:
    """Move in the undo history by delta `value`

    Args:
     * `value` (`int`): amount to undo or redo (positive is redo, negative is
        undo)

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def restoreUndo() -> int:
    """???
    
    This seems to behave in the same way as `undo()`.
    
    HELP WANTED: What does this do?

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def restoreUndoLevel(level: int) -> int:
    """???
    
    This seems to behave in the same way as `undo()`.
    
    HELP WANTED: What does this do? What is the parameter for?

    Args:
     * `level` (`int`): ???

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def getUndoLevelHint() -> str:
    """Returns a fraction-like string that shows the position in the undo
    history as well as the total length of it.

    Returns:
     * `str`: fraction-like string:
            * numerator: position in history (`1` is most recent)
            * denominator: number of elements in history
    
    Included since API version 1
    """

def getUndoHistoryPos() -> int:
    """Returns the length of the undo history

    HELP WANTED: This seems to behave the same as `getUndoHistoryCount()`.
    What's the difference?

    Returns:
     * `int`: number of elements in undo history
    
    Included since API version 1
    """

def getundoHistoryCount() -> int:
    """Returns the length of the undo history

    Returns:
     * `int`: number of elements in undo history
    
    Included since API version 1
    """

def getUndoHistoryLast() -> int:
    """Returns the current position in the undo history. The most recent
    position is `0`, with earlier points in the history having higher indexes.

    Returns:
     * `int`: position in undo history
    
    Included since API version 1
    """

def setUndoHistoryPos(index: int) -> None:
    """Removes recent elements from the undo history, leaving only the first
    `index` elements

    Args:
     * `index` (`int`): number of elements to leave at the start of the history
    
    Included since API version 1
    """

def setUndoHistoryCount(value: int) -> None:
    """Removes old elements from the undo history, leaving only the last
    `index` elements

    Args:
     * `value` (`int`): number of elements to leave at the end of the history
    
    Included since API version 1
    """

def setUndoHistoryLast(index: int) -> None:
    """Sets the position in the undo history, where `index = 0` is the most
    recent element and earlier points have higher indexes.

    Args:
     * `index` (`int`): new position in undo history
    
    Included since API version 1
    """

def getRecPPB() -> int:
    """Returns the current timebase (PPQN) multiplied by the number of beats in
    a bar.
    
    NOTE: This DOES NOT respect time signature markers

    Returns:
     * `int`: timebase * numerator
    
    Included since API version 1
    """

def getRecPPQ() -> int:
    """Returns the current timebase (PPQN)

    Returns:
     * `int`: timebase
    
    Included since API version 8
    """

def getUseMetronome() -> bool:
    """Returns whether the metronome is active

    Returns:
     * `bool`: metronome enabled
    
    Included since API version 1
    """

def getPrecount() -> bool:
    """Returns whether precount before recording is enabled

    Returns:
     * `bool`: precount before recording
    
    Included since API version 1
    """

def getChangedFlag() -> int:
    """Returns whether a project has been changed since the last save

    Returns:
     * `int`: changed flag:
            * `0`: Unchanged since last save
            * `1`: Changed since last save
            * `2`: Changed since last save, but unchanged since last autosave
    
    Included since API version 1
    """

def getVersion() -> int:
    """Returns MIDI Scripting API version number. Note that this is the API
    version, rather than the FL Studio version

    Returns:
     * `int`: version number
    
    Included since API version 1
    """

def processRECEvent(eventId: int, value: int, flags: int) -> int:
    """Processes a recording event.
    
    HELP WANTED: What does this do?

    Args:
     * `eventId` (`int`): Refer to the [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#RecEventParams)
     * `value` (`int`): value of even within range (0 - midi.FromMIDI_Max)
     * `flags` (`int`): Refer to the [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#RecEventFlags)

    Returns:
     * `int`: Unknown
    
    Included since API version 7
    """

def dumpScoreLog(time: int, silent:int=0) -> None:
    """Dump score log
    
    Args:
     * `time` (`int`): ?
     * `silent` (`int`): Whether the empty score message is suppressed (`1`) or
       not (`0`)
    
    Included since API version 15
    """

def clearLog() -> None:
    """Clear log
    """
