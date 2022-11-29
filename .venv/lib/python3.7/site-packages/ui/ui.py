"""User Interface Module (FL Studio built-in)

Allows you to control and interact with FL Studio's UI.

HELP WANTED:
 * What do the return values mean?
"""

def jog(value: int) -> int:
    """Jog control. Used to map a jog wheel to selections.

    Args:
     * `value` (`int`): delta value (increment), for example
            * `1`: next
            * `-1`: previous
        
    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def jog2(value: int) -> int:
    """Alternate jog control. Used to map a jog wheel to relocate.

    Args:
     * `value` (`int`): delta value (increment), for example
            * `1`: next
            * `-1`: previous
        
    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def strip(value: int) -> int:
    """Used by touch-sensitive strip controls.
    
    HELP WANTED: What does this apply to?

    Args:
     * `value` (`int`): ???

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def stripJog(value: int) -> int:
    """Touch-sensitive strip in jog mode.

    Args:
     * `value` (`int`): delta value (increment)

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def stripHold(value: int) -> int:
    """Touch-sensitive strip in hold mode

    Args:
     * `value` (`int`):
            * `0`: release
            * `1`: 1-finger centred mode
            * `2`: 2-fingers centred mode
            * `-1`: 1-finger jog mode
            * `-2`: 2-finger jog mode

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def previous() -> int:
    """Select to previous control:
     * in mixer: select previous track
     * in channel rack: select previous channel
     * in browser: scroll to previous item
     * in plugin: switch to previous preset (since API version 9)

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def next() -> int:
    """Select to next control:
     * in mixer: select next track
     * in channel rack: select next channel
     * in browser: scroll to next item
     * in plugin: switch to next preset

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def moveJog(value: int) -> int:
    """Used to relocate items with a jog control.
    
    HELP WANTED: How does this differ from `jog2()`?

    Args:
     * `value` (`int`): delta value (increment)

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def up(value:int=1) -> int:
    """Generic up control.

    WARNING: This function echoes the up arrow key, and thus will affect
    programs outside of FL Studio. Use with caution.
    
    HELP WANTED: What does the `value` variable do?

    Args:
     * `value` (`int`, optional): ???. Defaults to 1.

    Returns:
     * `int`: ?
    
    Included since API version 1, with option parameter since API version 4
    """

def down(value:int=1) -> int:
    """Generic down control.

    WARNING: This function echoes the down arrow key, and thus will affect
    programs outside of FL Studio. Use with caution.
    
    HELP WANTED: What does the `value` variable do?

    Args:
     * `value` (`int`, optional): ???. Defaults to 1.

    Returns:
     * `int`: ?
    
    Included since API version 1, with option parameter since API version 4
    """

def left(value:int=1) -> int:
    """Generic left control.

    WARNING: This function echoes the left arrow key, and thus will affect
    programs outside of FL Studio. Use with caution.
    
    HELP WANTED: What does the `value` variable do?

    Args:
     * `value` (`int`, optional): ???. Defaults to 1.

    Returns:
     * `int`: ?
    
    Included since API version 1, with option parameter since API version 4
    """

def right(value:int=1) -> int:
    """Generic right control.

    WARNING: This function echoes the right arrow key, and thus will affect
    programs outside of FL Studio. Use with caution.
    
    HELP WANTED: What does the `value` variable do?

    Args:
     * `value` (`int`, optional): ???. Defaults to 1.

    Returns:
     * `int`: ?
    
    Included since API version 1, with option parameter since API version 4
    """

def horZoom(value: int) -> int:
    """Zoom horizontally by `value`.

    Args:
     * `value` (`int`): amount to zoom by. Negative zooms out, positive zooms in.
        Larger magnitudes zoom more, but the scale doesn't seem consistent.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def verZoom(value: int) -> int:
    """Zoom vertically by `value`.

    Args:
     * `value` (`int`): amount to zoom by. Negative zooms out, positive zooms in.
        Larger magnitudes zoom more, but the scale doesn't seem consistent.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def snapOnOff() -> int:
    """Toggle whether snapping is enabled globally.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def cut() -> int:
    """Cut the selection.
    
    WARNING: This function echoes the hotkey to cut, and thus will affect
    programs outside of FL Studio. Use with caution.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def copy() -> int:
    """Copy the selection.
    
    WARNING: This function echoes the hotkey to copy, and thus will affect
    programs outside of FL Studio. Use with caution.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def paste() -> int:
    """Paste the selection.
    
    WARNING: This function echoes the hotkey to paste, and thus will affect
    programs outside of FL Studio. Use with caution.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def insert() -> int:
    """Press the insert key.
    
    WARNING: This function echoes the insert key, and thus will affect
    programs outside of FL Studio. Use with caution.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def delete() -> int:
    """Press the delete key.
    
    WARNING: This function echoes the delete key, and thus will affect
    programs outside of FL Studio. Use with caution.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def enter() -> int:
    """Press the enter key.
    
    WARNING: This function echoes the enter key, and thus will affect
    programs outside of FL Studio. Use with caution.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def escape() -> int:
    """Press the escape key.
    
    WARNING: This function echoes the escape key, and thus will affect
    programs outside of FL Studio. Use with caution.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def yes() -> int:
    """Press the y key.
    
    WARNING: This function echoes the y key, and thus will affect
    programs outside of FL Studio. Use with caution.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def no() -> int:
    """Press the n key.
    
    WARNING: This function echoes the n key, and thus will affect
    programs outside of FL Studio. Use with caution.

    NOTE: This function is listed in the official documentation as `not`, 
    however this is incorrect, and will result in a syntax error since
    overriding core keywords (such as `if`, `def` and `not`) is not allowed. The
    function is actually named `no`, which is how this documentation lists it.

    Returns:
     * `int`: ?
    
    Included since API version 1
    """

def getHintMsg() -> str:
    """Returns the current message in FL Studio's hint panel.

    Returns:
     * `str`: hint
    """

def setHintMessage(msg: str) -> None:
    """Sets the current hint message in FL Studio's hint panel to `msg`.

    Args:
     * `msg` (`str`): new message
    
    Included since API version 1
    """

def getHintValue(value: int, max: int) -> str:
    """Returns hint for `value`.
    
    HELP WANTED: What does this do?

    Args:
     * `value` (`int`): ???
     * `max` (`int`): ???

    Returns:
     * `str`: hint for `value`
    
    Included since API version 1
    """

def getTimeDispMin() -> bool:
    """Returns `True` when the song position panel is displaying time, rather
    than bar and beat.

    Returns:
     * `bool`: whether song position is displaying time.
    
    Included since API version 1
    """

def setTimeDispMin() -> None:
    """Toggles whether the song position panel is displaying time or bar and 
    beat.
    
    Included since API version 1
    """

def getVisible(index: int) -> bool:
    """Returns whether an FL Studio window is visible.

    Args:
     * `index` (`int`): window index:
            * `widMixer` (`0`): Mixer
            * `widChannelRack` (`1`): Channel Rack
            * `widPlaylist` (`2`): Playlist
            * `widPianoRoll` (`3`): Piano Roll
            * `widBrowser` (`4`): Browser

    Returns:
     * `bool`: whether it is visible
    
    Included since API version 1
    """

def showWindow(index: int) -> None:
    """Shows an FL Studio window specified by `index`.

    Args:
     * `index` (`int`): window index:
            * `widMixer` (`0`): Mixer
            * `widChannelRack` (`1`): Channel Rack
            * `widPlaylist` (`2`): Playlist
            * `widPianoRoll` (`3`): Piano Roll
            * `widBrowser` (`4`): Browser
    
    Included since API version 1
    """

def hideWindow(index: int) -> None:
    """Hides an FL Studio window specified by `index`.

    Args:
     * `index` (`int`): window index:
            * `widMixer` (`0`): Mixer
            * `widChannelRack` (`1`): Channel Rack
            * `widPlaylist` (`2`): Playlist
            * `widPianoRoll` (`3`): Piano Roll
            * `widBrowser` (`4`): Browser
    
    Included since API version 5
    """

def getFocused(index: int) -> bool:
    """Returns whether an FL Studio window is focused (meaning it is the
    currently selected Window in FL Studio). 
    
    NOTE: this doesn't necessarily mean that it is the currently selected window
    in the host operating system, so functions that rely on keypress emulation 
    (such as `ui.copy()`) may not work as intended, even if this returns `True`.
    
    Args:
     * `index` (`int`): window index:
            * `widMixer` (`0`): Mixer
            * `widChannelRack` (`1`): Channel Rack
            * `widPlaylist` (`2`): Playlist
            * `widPianoRoll` (`3`): Piano Roll
            * `widBrowser` (`4`): Browser
            * `widPlugin` (`5`): Plugin Window (note that this constant is only
              usable in this particular function).

    Returns:
     * `bool`: whether it is visible
    
    Included since API version 1
    """

def setFocused(index: int) -> None:
    """Sets which FL Studio window should be focused (meaning it is the
    currently selected Window in FL Studio). 
    
    NOTE: this doesn't necessarily mean that it will be the currently selected 
    window in the host operating system, so functions that rely on keypress 
    emulation (such as `ui.copy()`) may not work as intended, even after calling
    this function.
    
    Args:
     * `index` (`int`): window index:
            * `widMixer` (`0`): Mixer
            * `widChannelRack` (`1`): Channel Rack
            * `widPlaylist` (`2`): Playlist
            * `widPianoRoll` (`3`): Piano Roll
            * `widBrowser` (`4`): Browser
    
    Included since API version 2
    """

def getFocusedFormCaption() -> str:
    """Returns the caption (title) of the focused FL Studio window. This isn't 
    necessarily the same as the plugin's name.

    Returns:
     * `str`: window title
    
    Included since API version 1
    """

def getFocusedPluginName() -> str:
    """Returns the plugin name for the active window if it is a plugin,
    otherwise an empty string.

    Returns:
     * `str`: plugin name
    
    Included since API version 5
    """

def scrollWindow(index: int, value: int, directionFlag:int=0) -> None:
    """Scrolls on the window specified by `index`. Value is index for whatever
    is contained on that window (eg channels for the Channel Rack or tracks for
    the Mixer).

    Args:
     * `index` (`int`): window index:
            * `widMixer` (`0`): Mixer
            * `widChannelRack` (`1`): Channel Rack
            * `widPlaylist` (`2`): Playlist
            * `widPianoRoll` (`3`): Piano Roll
            * `widBrowser` (`4`): Browser
     * `value` (`int`): index to scroll to:
            * on mixer: track number
            * on channel rack: channel number
            * on playlist: playlist track number
            * on playlist: bar number (when `directionFlag` is set to `1`)
    
    Included since API version 13
    """

def nextWindow() -> int:
    """Switch to the next window

    Returns:
     * `int`: ???
    
    Included since API version 1
    """
    
def selectWindow(shift: int) -> int:
    """Switch to the next window by pressing the `Tab` key. If `shift` is true 
    (`1`), switch to the previous window by pressing `Shift` and `Tab`.

    WARNING: This function echoes the tab key, and thus will affect
    programs outside of FL Studio. Use with caution.

    Args:
     * `shift` (`int`): whether the shift key is pressed.

    Returns:
     * `int`: ???
    
    Included since API version 1
    """

def launchAudioEditor(reuse: int, filename: str, index: int, preset: str,
                      presetGUID: str) -> int:
    """Launches an audio editor for track at `index` and returns the state of 
    the editor. Set `reuse` to true (`1`) to reuse an already loaded audio 
    editor.

    HELP WANTED: How do I get this to work? I can only get it to open an empty
    window.

    Args:
     * `reuse` (`int`): whether to reuse an already open audio editor
     * `filename` (`str`): filename to open?
     * `index` (`int`): mixer track index to open on
     * `preset` (`str`): ???
     * `presetGUID` (`str`): ???

    Returns:
     * `int`: ???
    
    Included since API version 1
    """

def openEventEditor(eventId: int, mode: int, newWindow:int=0) -> int:
    """Launches an event editor for `eventId`.
    
    HELP WANTED: Yuck REC events please help me.

    Args:
     * `eventId` (`int`): ???
     * `mode` (`int`): Refer to [official documentation](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_scripting.htm#openEventEditorMode)
     * `newWindow` (`int`, optional): whether to open in a new window. Defaults 
       to 0.

    Returns:
     * `int`: ???
    
    Included since API version 9
    """

def isInPopupMenu() -> bool:
    """Returns `True` when a popup menu is open (for example a rick-click or
    drop-down menu).

    Returns:
      * `bool`: whether a popup menu is open
    
    Included since API version 1
    """

def closeActivePopupMenu() -> None:
    """Closes a currently-open popup menu (for example a rick-click or
    drop-down menu).
    
    Included since API version 1
    """

def isClosing() -> bool:
    """Returns `True` when FL Studio is closing

    Returns:
     * `bool`: is closing
    
    Included since API version 1
    """

def isMetronomeEnabled() -> bool:
    """Returns whether the metronome is enabled

    Returns:
     * `bool`: whether metronome is enabled
    
    Included since API version 1
    """

def isStartOnInputEnabled() -> bool:
    """Returns whether start on input is enabled

    Returns:
     * `bool`: whether start on input is enabled
    
    Included since API version 1
    """

def isPrecountEnabled() -> bool:
    """Returns whether precount is enabled

    Returns:
     * `bool`: whether precount is enabled
    
    Included since API version 1
    """

def isLoopRecEnabled() -> bool:
    """Returns whether loop recording is enabled

    Returns:
     * `bool`: whether loop recording is enabled
    
    Included since API version 1
    """

def getSnapMode() -> int:
    """Returns the current snap mode.

    NOTE: Although the official documentation states that this takes an 
    argument `value`, it does not. This stub reflects the actual behaviour.

    Returns:
     * `int`: index in the snap mode list:
            * `0`: Line
            * `1`: Cell
            * `2`: Unused (separator)
            * `3`: None
            * `4`: 1/6 step
            * `5`: 1/4 step
            * `6`: 1/3 step
            * `7`: 1/2 step
            * `8`: Step
            * `9`: 1/6 beat
            * `10`: 1/4 beat
            * `11`: 1/3 beat
            * `12`: 1/2 beat
            * `13`: Beat
            * `14`: bar
    
    Included since API version 1
    """

def snapMode(value: int) -> int:
    """Changes the snap mode, by shifting it by `value` in the list of modes.
    Note that `2` (the unused value) is skipped.
    
    Also note that the usage for this function is truly painful. I am sorry.
    
    TODO: Add helper function to provide a better implementation to this 
    documentation, so people can copy it into their code.

    Args:
     * `value` (`int`): increment (`1` for next, `-1` for previous)

    Returns:
     * `int`: ???
    
    Included since API version 1
    """

def getProgTitle() -> str:
    """Returns the title of the FL Studio window

    Returns:
     * `str`: program title
    
    Included since API version 1
    """

def getVersion(mode:int=4) -> 'str | int':
    """Returns the version number of FL Studio
    
    Args:
     * `mode` (`int`, optional):
            * `VER_Major` (`0`): Major version number (as `int`)
              Eg: `20`
            * `VER_Minor` (`1`): Minor version number (as `int`)
              Eg: `8`
            * `VER_Release` (`2`): Release version number (as `int`)
              Eg: `4`
            * `VER_Build` (`3`): Program build number (as `int`)
              Eg: `2553`
            * `VER_VersionAndEdition` (`4`): Program version and edition (as `str`).
              Eg: `"Producer Edition v20.8.4 [build 2553]"`
            * `VER_FillVersionAndEdition` (`5`): Full version and edition (as `str`).
              Eg: `"Producer Edition v20.8.4 [build 2553] - Signature Bundle - 64Bit"`
            * `VER_ArchAndBuild` (`6`): Architecture and build number?
    
    Included since API version 1, with mode parameter since API version 7
    """

def crDisplayRect(left: int, top: int, right: int, bottom: int, duration: int, flags:int=0) -> None:
    """Displays a selection rectangle on the channel rack

    Args:
     * `left` (`int`): left position
     * `top` (`int`): top position
     * `right` (`int`): right border (not inclusive)
     * `bottom` (`int`): bottom index (not inclusive)
     * `duration` (`int`): duration to display for (in ms)
     * `flags` (`int`, optional): a bitwise combination of:
            * `CR_HighlightChannels`: Display on channel list rather than on
              grid
            * `CR_ScrollToView`: Scroll channel rack to specified position
    
    Included since API version 1
    """

def miDisplayRect(start: int, end: int, duration: int, flags:int=0) -> None:
    """Displays a selection rectangle on the mixer

    TODO: Ensure these docs are correct when it gets added

    Args:
     * `start` (`int`): start track index
     * `end` (`int`): end track index
     * `duration` (`int`): duration to display for (in ms)??
     * `flags` (`int`, optional): unknown
    
    Included since API version 13
    """
