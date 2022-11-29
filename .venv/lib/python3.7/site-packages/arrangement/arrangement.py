"""Arrangement Module (FL Studio built-in)

Allows you to control and interact with FL Studio Arrangements, inlcuding 
markers, selections and timestamps.
"""

def jumpToMarker(index: int, select: int) -> None:
    """Jumps to the marker at index.

    Args:
     * index (`int`): marker index
     * select (`int`): whether to select the marker
    
    Included since API version 1
    """

def getMarkerName(index: int) -> str:
    """Returns the name of the marker at `index`

    Args:
     * index (`int`): marker index

    Returns:
     * `str`: name of the marker
    
    Included since API version 1
    """

def addAutoTimeMarker(time: int, name: str) -> None:
    """Add an automatic time marker at `time`.

    Args:
     * `time` (`int`): time (TODO: What are the units?)
     * `name` (`str`): name of new marker
    
    Included since API version 1
    """

def liveSelection(time: int, stop: int) -> None:
    """Set a live selection point at `time`.
    set `stop` to True, to use end point of the selection (instead of start).
    
    HELP WANTED: A better explanation would be good

    Args:
     * `time` (`int`): ???
     * `stop` (`int`): ???
    
    Included since API version 1
    """

def liveSelectionStart() -> int:
    """Returns the start time of the current live selection

    Returns:
     * `int`: start of selection time
    
    Included since API version 1
    """

def currentTime(snap: int) -> int:
    """Returns the current time in the current arrangement.

    Args:
     * `snap` (`int`): whether to get time snapped to grid

    Returns:
     * `int`: current time
    
    Included since API version 1
    """

def currentTimeHint(mode: int, time: int, setRecPPB:int=0, isLength:int=0)\
    -> str:
    """Returns a hint string for the given time
    
    HELP WANTED: What does this do?
    
    Args:
     * `mode` (`int`): pattern mode (`0`) or song mode (`1`)
     * `time` (`int`): time
     * `setRecPPB` (`int`, optional): ???. Defaults to ?
     * `isLength` (`int`, optional): ???. Defaults to 0

    Returns:
     * `str`: current time as string hint
    
    Included since API version 1
    """

def selectionStart() -> int:
    """Returns the returns the start time of the current selection.

    Returns:
        `int`: start time
    
    Included since API version 1
    """

def selectionEnd() -> int:
    """Returns the returns the end time of the current selection.

    Returns:
        `int`: end time
    
    Included since API version 1
    """
