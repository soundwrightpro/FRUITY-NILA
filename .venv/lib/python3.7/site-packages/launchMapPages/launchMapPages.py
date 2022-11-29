"""Launchmap Pages Module (FL Studio built-in)

Handles custom controller layouts for certain controllers

Refer to [reference](https://forum.image-line.com/viewtopic.php?f=1914&t=92193)

HELP WANTED: More detailed explanations would be good, since it's not very well
explained by the manual.
"""

def init(deviceName: str, width: int, height: int) -> None:
    """Initialise launchmap pages

    Args:
     * `deviceName` (`str`): ???
     * `width` (`int`): ???
     * `height` (`int`): ???
    
    Included since API version 1
    """

def createOverlayMap(offColor: int, onColor: int, width: int, height: int) -> None:
    """Creates an overlay map

    Args:
     * `offColor` (`int`): ?
     * `onColor` (`int`): ?
     * `width` (`int`): ?
     * `height` (`int`): ?
    
    Included since API version 1
    """

def length() -> int:
    """Returns launchmap pages length

    Returns:
     * `int`: length
    
    Included since API version 1
    """

def updateMap(index: int) -> None:
    """Updates launchmap page at `index`

    Args:
     * `index` (`int`): index of page to update
    
    Included since API version 1
    """

def getMapItemColor(index: int, itemIndex: int) -> int:
    """Returns item colour of `itemIndex` in map `index`

    Args:
     * `index` (`int`): map index
     * `itemIndex` (`int`): item index

    Returns:
     * `int`: colour
    
    Included since API version 1
    """

def getMapCount(index: int) -> int:
    """Returns the number of items in page at `index`

    Args:
     * `index` (`int`): page index

    Returns:
     * `int`: number of items
    
    Included since API version 1
    """

def getMapItemChannel(index: int, itemIndex: int) -> int:
    """Returns the channel for item at `itemIndex` on page at `index`

    Args:
     * `index` (`int`): page index
     * `itemIndex` (`int`): item index

    Returns:
     * `int`: channel number
    
    Included since API version 1
    """

def getMapItemAftertouch(index: int, itemIndex: int) -> int:
    """Returns the aftertouch for item at `itemIndex` on page at `index`

    Args:
     * `index` (`int`): page index
     * `itemIndex` (`int`): item index

    Returns:
     * `int`: aftertouch value
    
    Included since API version 1
    """

def processMapItem(eventData, index: int, itemIndex: int, velocity: int) -> None:
    """Process map item at `itemIndex` of page at `index`

    Args:
     * eventData (`eventData`): event data
     * index (`int`): page index
     * itemIndex (`int`): item index
     * velocity (`int`): velocity
    
    Included since API version 1
    """

def releaseMapItem(eventData, index: int) -> None:
    """Release map item at `itemIndex` of page at `index`

    HELP WANTED: This doesn't seem quite right, there is no `itemIndex` argument

    Args:
     * `eventData` (`eventData`): event data
     * `index` (`int`): page index
    
    Included since API version 1
    """

def checkMapForHiddenItem() -> None:
    """Checks for launchpad hidden item???
    
    Included since API version 1
    """

def setMapItemTarget(index: int, itemIndex: int, target: int) -> int:
    """Set target for item at `itemIndex` of page at `index`.

    Args:
     * `index` (`int`): page index
     * `itemIndex` (`int`): item index
     * `target` (`int`): ????

    Returns:
        `int`: ????
    
    Included since API version 1
    """
