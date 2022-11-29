"""Patterns Module (FL Studio built-in)

Allows you to control and interact with FL Studio Patterns.

NOTES:
 * Patterns are 1-indexed
"""

def patternNumber() -> int:
    """Returns the index for the currently selected pattern.

    Returns:
     * `int`: index of the currently active pattern
    
    Included since API version 1
    """

def patternCount() -> int:
    """Returns the number of patterns in the project

    Returns:
     * `int`: the number of patterns
    
    Included since API version 1
    """

def patternMax() -> int:
    """Returns the maximum number of patterns that can be created.

    Returns:
     * `int`: max number of patterns
    
    Included since API version 1
    """

def getPatternName(index: int) -> str:
    """Returns the name of the pattern at `index`.

    Args:
     * `index` (`int`): pattern index

    Returns:
     * `str`: name of pattern.
        
    Included since API version 1
    """

def setPatternName(index: int, name: str) -> None:
    """Sets the name of pattern at `index`
    
    Setting the name to an empty string will reset the name of the pattern to
    its default.

    Args:
     * index (`int`): index of pattern
     * name (`str`): new name
        
    Included since API version 1
    """

def getPatternColor(index: int) -> int:
    """Returns the colour of the pattern at `index`.

    Args:
     * `index` (`int`): pattern index

    Returns:
     * `int`: colour of pattern (0x--RRGGBB)
        
    Included since API version 1
    """

def setPatternColor(index: int, color: int) -> None:
    """Sets the colour of the pattern at `index`.

    Args:
     * `index` (`int`): pattern index
     * `color` (`int`): colour of pattern (0x--RRGGBB)
        
    Included since API version 1
    """

def getPatternLength(index: int) -> int:
    """Returns the length of the pattern at `index` in beats.

    Args:
     * `index` (`int`): pattern index

    Returns:
     * `int`: length of pattern in beats
    
    Included since API version 1
    """

def getBlockSetStatus(left: int, top: int, right: int, bottom: int) -> int:
    """Returns the status of the live block.
    
    HELP WANTED: What does this do?

    Args:
     * left (`int`): ?
     * top (`int`): ?
     * right (`int`): ?
     * bottom (`int`): ?

    Returns:
     * `int`: live block status
            * `LB_Status_Filled` (`1`): Filled
            * `LB_Status_Scheduled` (`2`): Scheduled
            * `LB_Status_Playing` (`4`): Playing
    
    Included since API version 1
    """

def ensureValidNoteRecord(index: int, playNow:int=0) -> int:
    """Ensures valid note on the pattern at `index`.

    HELP WANTED: What does this do? I haven't managed to get it to return
    anything other than zero.

    Args:
     * `index` (`int`): pattern index
     * `playNow` (`int`, optional): ???. Defaults to 0.

    Returns:
     * `int`: ???
    
    Included since API version 1
    """

def jumpToPattern(index: int) -> None:
    """Scroll the patterns list to the pattern at `index`, and select it.
    
    NOTE: This function seems to cause some extremely buggy behaviour as of FL
    20.8.4, and as such, using it is not recommended.

    Args:
     * index (`int`): pattern index
    
    Included since API version 1
    """

def findFirstNextEmptyPat(flags: int, x:int=-1, y:int=-1) -> None:
    """Selects the first or next empty pattern.

    Args:
     * `flags` (`int`):
            * `FFNEP_FindFirst` (`0`): Find first pattern
            * `FFNEP_DontPromptName` (`1`): Don't prompt pattern name (this 
              doesn't seem to work)
     * `x` (`int`, optional): ???. Defaults to -1.
     * `y` (`int`, optional): ???. Defaults to -1.
    
    Included since API version 1
    """

def isPatternSelected(index: int) -> bool:
    """Returns whether the pattern at `index` is selected.

    Args:
     * `index` (`int`): pattern index

    Returns:
     * `bool`: whether pattern is selected
    
    Included since API version 2
    """

def selectPattern(index: int, value:int=-1, preview:int=0) -> None:
    """Selects the pattern at `index`.

    Args:
     * `index` (`int`): pattern index
     * `value` (`int`, optional): selection mode:
            * `-1`: Toggle (default)
            * `0`: Deselect
            * `1`: Select
     * `preview` (`int`, optional): whether to preview the pattern.
       Defaults to 0.
    
    Included since API version 2
    """

def selectAll() -> None:
    """Selects all patterns
    
    Included since API version 2
    """

def deselectAll() -> None:
    """Deselects all patterns
    
    Included since API version 2
    """

def burnLoop(index: int, storeUndo:int=1, updateUi:int=1) -> None:
    """???
    
    HELP WANTED: The documentation for this doesn't make sense.

    Args:
     * `index` (`int`): ???
     * `storeUndo` (`int`, optional): ???. Defaults to 1.
     * `updateUi` (`int`, optional): ???. Defaults to 1.
    
    Included since API version 9
    """
