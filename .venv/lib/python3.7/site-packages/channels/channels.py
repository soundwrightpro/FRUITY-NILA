"""Channels Module (FL Studio built-in)

Allows you to control and interact with the FL Studio Channel Rack, and with
instrument channels.

NOTES:
 * In this documentation, an index respects channel groups, whereas a 
   global index does not.
 * Channels are zero-indexed.
"""

def channelNumber(canBeNone:int=0, offset:int=0) -> int:
    """Returns the global index of the first selected channel, otherwise the nth
    selected channel where n is `offset` + 1. If n is greater than the number of
    selected channels, the global index of the last selected channel will be
    returned.
    
    If `canBeNone` is `1`, no selection will return `-1`. Otherwise, no selection
    will return `0` (representing the first channel).

    Args:
     * `canBeNone` (`int`, optional): Whether the function will return `-1` or `0`
       when there is no selection. Defaults to `0` (returning `0`).
     * `offset` (`int`, optional): return other selected channels after offset. Defaults to 0.

    Returns:
     * `int`: global index of first selected channel
    
    Included since API version 1
    """

def channelCount(mode:int=0) -> int:
    """Returns the number of channels on the channel rack. Respect for groups is
    controlled by the `mode` flag.

    Args:
     * `mode` (`int`, optional): Whether the number of channels respects groups. 
       Defaults to 0.

    Returns:
     * `int`: number of channels
    
    Included since API version 1. (updated with optional parameter in API 
    version 3).
    """

def getChannelName(index: int) -> str:
    """Returns the name of the channel at `index` (respecting groups)

    Args:
     * `index` (`int`): index of channel

    Returns:
     * `str`: channel name
    
    Included since API version 1
    """

def setChannelName(index: int, name: str) -> None:
    """Sets the name of the channel at `index` (respecting groups)

    If a channel's name is set to "", its name will be set to the default name
    of the plugin or sample.

    Args:
     * `index` (`int`): index of channel
     * `name` (`str`): new name for channel
    
    Included since API version 1
    """

def getChannelColor(index: int) -> int:
    """Returns the colour of the channel at `index` (respecting groups)

    Note that colours can be split into or built from components using the
    functions provided in the module `utils`
    * `ColorToRGB()`
    * `RGBToColor()`

    Args:
     * `index` (`int`): index of channel

    Returns:
     * `int`: channel colour (0x--RRGGBB)
    
    Included since API version 1
    """

def setChannelColor(index: int, color: int) -> None:
    """Sets the colour of the channel at `index` (respecting groups)

    Note that colours can be split into or built from components using the
    functions provided in the module `utils`
    * `ColorToRGB()`
    * `RGBToColor()`

    Args:
     * `index` (`int`): index of channel
     * `colour` (`int`): new colour for channel (0x--RRGGBB)
    
    Included since API version 1
    """

def isChannelMuted(index: int) -> bool:
    """Returns whether channel is muted (`1`) or not (`0`)

    Args:
     * `index` (`int`): index of channel

    Returns:
     * `bool`: mute status
    
    Included since API version 1
    """

def muteChannel(index: int) -> None:
    """Toggles the mute state of the channel at `index`

    Args:
        `index` (`int`): index of channel
    """

def isChannelSolo(index: int) -> bool:
    """Returns whether channel is solo (`1`) or not (`0`)

    Args:
     * `index` (`int`): index of channel

    Returns:
     * `bool`: solo status
    
    Included since API version 1
    """

def soloChannel(index: int) -> None:
    """Toggles the solo state of the channel at `index`

    Args:
     * `index` (`int`): index of channel
    
    Included since API version 1
    """

def getChannelVolume(index: int, mode:int=0) -> float:
    """Returns the normalised volume of the channel at `index`, where `0.0` is
    the minimum value, and `1.0` is the maximum value. Note that the default
    volume for channels is `0.78125`. By setting the `mode` flag to `1`, the
    volume is returned in decibels.

    Args:
     * `index` (`int`): index of channel
     * `mode` (`int`, optional): whether to return as a float between 0 and 1
       of a value in dB

    Returns:
     * `float`: channel volume
    
    Included since API version 1
    """

def setChannelVolume(index: int, volume: float, pickupMode:int=0) -> None:
    """Sets the normalised volume of the channel at `index`, where `0.0` is
    the minimum value, and `1.0` is the maximum value. Note that the default
    volume for channels is `0.78125`. Use the pickup mode flag to set pickup
    options.

    Args:
     * `index` (`int`): index of channel
     * `volume` (`float`): channel volume
     * `pickupMode` (`int`, optional): define the pickup behaviour. Refer to
       the [manual](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#pickupModes)
    
    Included since API version 1
    """

def getChannelPan(index: int) -> float:
    """Returns the normalised pan of the channel at `index`, where `-1.0` is 
    100% left, and `1.0` is 100% right. Note that the default pan for channels 
    is `0.0` (centre).

    Args:
     * `index` (`int`): index of channel

    Returns:
     * `float`: channel pan
    
    Included since API version 1
    """

def setChannelPan(index: int, pan: float, pickupMode:int=0) -> None:
    """Sets the normalised pan of the channel at `index`, where `-1.0` is
    100% left, and `1.0` is 100% right. Note that the default
    pan for channels is `0.0` (centre). Use the pickup mode flag to set pickup
    options.

    Args:
     * `index` (`int`): index of channel
     * `pan` (`float`): channel pan
     * `pickupMode` (`int`, optional): define the pickup behaviour. Refer to
       the [manual](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#pickupModes)
    
    Included since API version 1
    """

def getChannelPitch(index: int, mode:int=0) -> 'float | int':
    """Returns the pitch of the channel at `index`. The `mode` parameter is used
    to determine the type of pitch returned. 
    
    HELP WANTED: What do the `mode` parameter options mean?
    
    Args:
     * `index` (`int`): index of channel
     * `mode` (`int`, optional):
            * `1`: return value in semitones
            * `2`: return value pitch range???
    
    Returns:
     * `float`: channel pitch (when `mode` is `1`)
     * `int`: channel pitch range (when `mode` is `2`) ???
    
    Included since API version 8
    """

def setChannelPitch(index: int, value: float, mode:int=0) -> 'float | int':
    """Sets the pitch of the channel at `index` to value. The `mode` parameter is used
    to determine the type of pitch set. Use the pickup mode flag to set pickup
    options.
    
    HELP WANTED: What do the `mode` parameter options mean?
    
    Args:
     * `index` (`int`): index of channel
     * `value` (`float`): value to set
     * `mode` (`int`, optional):
            * `1`: set value in semitones
            * `2`: set value pitch range???
     * `pickupMode` (`int`, optional): define the pickup behaviour. Refer to
       the [manual](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#pickupModes)
    
    
    Included since API version 8
    """

def isChannelSelected(index: int) -> bool:
    """Returns whether the channel at `index` is selected (not respecting 
    channel groups).

    Args:
     * `index` (`int`): channel index

    Returns:
     * `bool`: whether the channel is selected
    
    Included since API version 1
    """

def selectChannel(index: int, value:int=-1) -> None:
    """Select the channel at `index` (respecting groups).

    Args:
     * `index` (`int`): channel index
     * `value` (`int`, optional): Whether to select or deselect the channel. 
            * `-1` (default): Toggle
            * `0` : Deselect
            * `1`: Select
    
    Included since API version 1
    """

def selectOneChannel(index: int) -> None:
    """Exclusively select the channel at `index` (deselecting any other selected
    channels).

    Args:
        `index` (`int`): channel index
    
    Included since API version 8
    """

def selectedChannel(canBeNone:int=0, offset:int=0, indexGlobal:int=0) -> int:
    """Returns the index of the first selected channel, otherwise the nth
    selected channel where n is `offset` + 1. If n is greater than the number of
    selected channels, the global index of the last selected channel will be
    returned. If `indexGlobal` is set to `1`, this will replicate the behaviour
    of `channelNumber()` by returning global indexes.
    
    NOTE: This function replaces the functionality of `channelNumber()` 
    entirely, with the added functionality of providing indexes respecting 
    groups (when `indexGlobal` is not set).
    
    If `canBeNone` is `1`, no selection will return `-1`. Otherwise, no selection
    will return `0` (representing the first channel).

    Args:
     * `canBeNone` (`int`, optional): Whether the function will return `-1` or 
       `0` when there is no selection. Defaults to `0` (returning `0`).
     * `offset` (`int`, optional): return other selected channels after offset. 
       Defaults to 0.
     * `indexGlobal` (`int`, optional): Whether to return the group index (`0`)
       or the global index (`1`).

    Returns:
     * `int`: index of first selected channel
    
    Included since API version 5
    """

def selectAll() -> None:
    """Selects all channels in the current channel group
    
    Included since API version 1
    """

def deselectAll() -> None:
    """Deselects all channels in the current channel group
    
    Included since API version 1
    """

def getChannelMidiInPort(index: int) -> int:
    """Returns the MIDI port associated with the channel at `index`.

    TODO: Write use cases

    Args:
     * `index` (`int`): channel index

    Returns:
     * `int`: MIDI port associated with channel
    
    Included since API version 1
    """

def getChannelIndex(index: int) -> int:
    """Returns the global index of a channel given the group `index`.

    Args:
     * `index` (`int`): index of channel (respecting groups)

    Returns:
     * `int`: global index of channel
    
    Included since API version 1
    """

def getTargetFxTrack(index: int) -> int:
    """Returns the mixer track that the channel at `index` is linked to.

    Args:
     * index (`int`): index of channel

    Returns:
     * `int`: index of targeted mixer track
    
    Included since API version 1
    """

def isHighlighted() -> bool:
    """Returns True when a red highlight rectangle is displayed on the channel
    rack. This rectangle can be displayed using `ui.crDisplayRect()` in the UI
    module. 
    
    These hints can be used to visually indicate on the channel rack where your 
    script is mapping to.

    Returns:
     * `bool`: whether highlight rectangle is visible.
    
    Included since API version 1
    """

def processRECEvent(eventId: int, value: int, flags: int) -> int:
    """Processes a recording event.
    
    WARNING: This function is depreciated here, and moved to the `general`
    module as of API version 7.
    
    HELP WANTED: What does this do?

    Args:
     * `eventId` (`int`): Refer to the [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#RecEventParams)
     * `value` (`int`): value of even within range (0 - midi.FromMIDI_Max)
     * `flags` (`int`): Refer to the [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#RecEventFlags)

    Returns:
     * `int`: Unknown
    
    Included since API version 1
    Depreciated since API version 7
    """

def incEventValue(eventId: int, step: int, res: float) -> int:
    """Increase recording event value
    
    HELP WANTED: I have no idea what any of this does

    Args:
     * `eventId` (`int`): event ID, see the [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#RecEventParams)
     * `step` (`int`): unknown
     * `res` (`float` (double precision)): unknown

    Returns:
     * `int`: unknown
    
    Included since API version 1
    """

def getRecEventId(index: int) -> int:
    """Returns recording event ID for channel at `index`.
    
    HELP WANTED: Honestly REC events are sooooo confusing, and I avoid using 
    them entirely. Can someone else explain them?

    Args:
     * `index` (`int`): channel index

    Returns:
     * `int`: Recording event ID???
    
    Included since API version 1
    """

def getGridBit(index: int, position: int) -> bool:
    """Returns whether the grid bit on channel at `index` in `position` is set.

    Args:
     * `index` (`int`): channel index
     * `position` (`int`): index of grid bit (horizontal axis)

    Returns:
     * `bool`: whether grid bit is set
    
    Included since API version 1
    """

def setGridBit(index: int, position: int, value: int) -> None:
    """Sets the value of the grid bit on channel at `index` in `position`.

    Args:
     * `index` (`int`): channel index
     * `position` (`int`): index of grid bit (horizontal axis)
     * `value` (`int`): whether grid bit is set (`1`) or not (`0`)
    
    Included since API version 1
    """

def getStepParam(step: int, param: int, ofset: int, startPos: int,
                 padsStride:int=16) -> int:
    """Get step parameter for `step`.
    
    HELP WANTED: What does this do?

    Args:
     * `step` (`int`): ?
     * `param` (`int`): ?? at least there's the [offical documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#stepParams)
       (actually, tbh the docs on this looks kinda dodgy for some values)
     * `ofset` (`int`): ??? (this typo is in the official docs too)
     * `startPos` (`int`): ????
     * `padsStride` (`int`, optional): ?????. Defaults to 16.

    Returns:
     * `int`: ??????
    
    Included since API version 1
    """

def getCurrentStepParam(index: int, step: int, param: int) -> None:
    """Get current step parameter for channel at `index` and for step at `step`.
    
    HELP WANTED: What does this do?

    TODO: Official documentation says this returns None, but it shouldn't.
    Check this.

    Args:
     * `index` (`int`): channel index
     * `step` (`int`): ???
     * `param` (`int`): step parameter (refer to [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#stepParams)
       although it looks kinda dodgy for some values)
    
    Included since API version 1
    """

def getGridBitWithLoop(index: int, position: int) -> bool:
    """Get value of grid bit on channel `index` in `position` accounting for 
    loops.
    
    NOTE: Official documentations say this returns None, but it doesn't. This
    documentation reflects the actual behaviour.

    Args:
     * `index` (`int`): channel index`
     * `position` (`int`): position on grid (x axis)
    
    Returns:
     * `bool`: whether grid bit is set
    
    Included since API version 1
    """

def showEditor(index: int, value:int=-1) -> None:
    """Toggle whether the plugin window for the channel at `index` is shown.
    The value parameter chan be used to set to a specific value.

    Args:
     * `index` (`int`): channel index
     * `value` (`int`): whether to hide (`0`) or show (`1`) the plugin window.
       Defaults to `-1` (toggle).
    
    Included since API version 1, with optional parameter added in version 3.
    """

def focusEditor(index: int) -> None:
    """Focus the plugin window for the channel at `index`.

    Args:
     * `index` (`int`): channel index.
    
    Included since API version 1
    """

def showCSForm(index: int, state:int=1) -> None:
    """Show the channel settings window (or plugin window for plugins) for 
    channel at `index`.
    
    TODO: Difference to `showEditor()`??? Check this.

    Args:
     * `index` (int): channel index
     * `state` (`int`, optional): * `value` (`int`): whether to hide (`0`), show 
        (`1`) or toggle (`-1`) the plugin window. Defaults to `1`.
    
    Included since API version 1, with optional parameter added in version 9
    """

def midiNoteOn(indexGlobal: int, note: int, velocity: int, channel:int=-1
               ) -> None:
    """Set a MIDI Note for the channel at `indexGlobal` (not respecting groups)
    
    This can be used to create extra notes (eg mapping one note to a chord).

    Args:
     * `indexGlobal` (`int`): channel index (not respecting groups)
     * `note` (`int`): note number (0-127)
     * `velocity` (`int`): note velocity (1-127, 0 is note off)
     * `channel` (`int`, optional): MIDI channel to use. Defaults to -1.
    
    Included since API version 1
    """

def getActivityLevel(index: int) -> float:
    """Return the note activity level for channel at `index`. Activity level
    refers to how recently a note was played, as well as whether any notes are
    currently playing.

    Args:
     * `index` (`int`): channel index

    Returns:
     * `float`: activity level
    
    Included since API version 9
    """
