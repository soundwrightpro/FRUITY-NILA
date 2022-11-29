"""Device Module (FL Studio built-in)

Handles the way that devices connect to FL Studio's MIDI interface, and how
scripts communicate with each other.
"""

def isAssigned() -> bool:
    """Returns `True` if an output interface is linked to the script, meaning
    that the script can send MIDI messages to that device.

    Returns:
     * `bool`: whether the device is assigned
    
    Included since API version 1
    """

def getPortNumber() -> int:
    """Returns the port number for the input device that the script is attached
    to. If the device requires two-way communication, the output port (where 
    functions like `midiOutMsg()` send their data to) should be set to the value
    of the input port, which is returned by this function.

    Returns:
     * `int`: port number of the input device
    
    Included since API version 1
    """

def getName() -> str:
    """Returns the name of the device.

    Returns:
     * `str`: device name
    
    Included since API version 7
    """

def midiOutMsg(message: int, channel:int=None, data1:int=None, data2:int=None)\
    -> None:
    """Sends a MIDI message to the linked output device.
    
    This can be done either through a single combined message, or in its 
    distinct components.

    Args:
     * `message` (`int`): 
            * the MIDI message to send (if sending a complete message):
                * Lowest byte: `status`
                * Middle byte: `data 1`
                * Upper byte: `data 2`
            * OR the message type (if sending a partial MIDI message, 
              eg `0xB` for a CC message)
     * `channel` (`int`, optional): the channel to send the message to (if 
       sending a partial MIDI message)
     * `data1` (`int`, optional): the note data value for the message (if
       sending a partial MIDI message)
     * `data2` (`int`, optional): the velocity data value for the message (if
       sending a partial MIDI message)
    
    Included since API version 1, with the component options added in API 
    version 2
    """

def midiOutNewMsg(slotIndex: int, message: int) -> None:
    """Sends a MIDI message to the linked output device, but only if the message
    being sent has changed compared to the last message sent with the same 
    `slotIndex`.

    Args:
     * `slotIndex` (`int`): index for MIDI message comparison
     * `message` (`int`): message to potentially send
    
    Included since API version 1
    """

def midiOutSysex(message: str) -> None:
    """Send a SysEx message to the (linked) output device.

    Args:
     * `message` (`str`): SysEx message to send
    
    Included since API version 1
    """

def sendMsgGeneric(id: int, message: str, lastMsg: str, offset:int=0) -> str:
    """Send a text string as a SysEx message to the linked output device.
    
    WARNING: This function is depreciated

    Args:
     * `id` (`int`): the first 6 bytes of the message (the end value `0xF7` is 
       added automatically)
     * `message` (`str`): the text to send
     * `lastMsg` (`str`): the string returned by the previous call to this
       function.
     * `offset` (`int`, optional): ???. Defaults to 0.

    Returns:
     * `str`: value to use in the next call of this function
    
    Included since API version 1
    """

def processMIDICC(eventData) -> None:
    """Lets FL Studio process a MIDI CC message.

    Args:
     * `eventData` (`eventData`): FL MIDI Event to process.
    
    Included since API version 1
    """

def forwardMIDICC(message: int, mode:int=1) -> None:
    """Forwards a MIDI CC message to the currently focused plugin.

    Args:
     * `message` (`int`): MIDI message to forward
     * `mode` (`int`, optional): Where to send the message:
            * `0`: Send the message to all plugins
            * `1` (default): ???
            * `2`: Send the message to the selected channels
    
    Included since API version 7
    """

def directFeedback(eventData) -> None:
    """Send a received message to the linked output device

    Args:
     * `eventData` (`eventData`): event to send
    
    Included since API version 1
    """

def repeatMidiEvent(eventData, delay:int=300, rate:int=300) -> None:
    """Start repeatedly sending out the message in `eventData` every `rate`
    ms after `delay` ms.

    Args:
     * `eventData` (`eventData`): event to repeat
     * `delay` (`int`, optional): initial delay before sending in ms. Defaults to 300.
     * `rate` (`int`, optional): time between each send in ms. Defaults to 300.
    
    Included since API version 1
    """

def stopRepeatMidiEvent() -> None:
    """Stop sending a currently repeating MIDI event.
    
    Refer to `repeatMidiEvent()`.
    
    Included since API version 1
    """

def findEventID(controlId: int, flags:int=0) -> int:
    """Returns eventID for controlId.

    HELP WANTED: What does this do?

    Args:
     * `controlId` (`int`): ???
     * `flags` (`int`, optional): ???. Defaults to 0.

    Returns:
     * `int`: event ID
    
    Included since API version 1
    """

def getLinkedValue(eventID: int) -> float:
    """Returns normalised value of the linked control via eventID. Returns `-1`
    if there is no linked control.

    HELP WANTED: What does this do?

    Args:
     * `eventID` (`int`): eventID

    Returns:
     * `float`: Linked value
    
    Included since API version 1
    """

def getLinkedValueString(eventID: int) -> str:
    """Returns text value of a linked control via eventID

    HELP WANTED: What does this do?

    Args:
     * `eventID` (`int`): eventID

    Returns:
     * `str`: Parameter value string
    
    Included since API version 10
    """

def getLinkedParamName(eventID: int) -> str:
    """Returns the parameter name of the control linked via `eventID`.

    HELP WANTED: What does this do?

    Args:
     * `eventID` (`int`): eventID

    Returns:
     * `str`: Parameter name
    
    Included since API version 10
    """

def getLinkedInfo(eventID: int) -> int:
    """Returns information about a linked control via `eventID`.

    Args:
     * `eventID` (`int`): eventID

    Returns:
     * `int`: linked control info:
            * `-1`: no linked control
            * `Event_CantInterpolate` (`1`): ???
            * `Event_Float` (`2`): ???
            * `Event_Centered` (`4`): ???
    
    Included since API version 1
    """

def createRefreshThread() -> None:
    """Start a threaded refresh of the entire MIDI device.
    
    HELP WANTED: What do refresh threads do?
    
    Included since API version 1
    """

def destroyRefreshThread() -> None:
    """Stop a previously started threaded refresh.
    
    HELP WANTED: What do refresh threads do?
    
    Included since API version 1
    """

def fullRefresh() -> None:
    """Trigger a previously started threaded refresh. If there is none, the
    refresh is triggered immediately.
    
    HELP WANTED: What do refresh threads do?
    
    Included since API version 1
    """

def isDoubleClick(index: int) -> bool:
    """Returns whether the function was called with the same index shortly 
    before, indicating a double click.

    Args:
     * `index` (`int`): a unique value representing the current control

    Returns:
     * `bool`: whether the event was a double click
    
    Included since API version 1
    """

def setHasMeters() -> None:
    """Registers the controller as having peak meters, meaning that the 
    `OnUpdateMeters()` function will be called. This function should be called 
    within `OnInit()`.
    
    Included since API version 1
    """

def baseTrackSelect(index: int, step: int) -> None:
    """Base track selection (for control surfaces). Set `step` to `MaxInt` to
    reset.
    
    HELP WANTED: What does this do?

    Args:
     * `index` (`int`): ???
     * `step` (`int`): ???
    
    Included since API version 1
    """

def hardwareRefreshMixerTrack(index: int) -> None:
    """Hardware refresh mixer track at `index`.
    
    HELP WANTED: What does this mean?

    Args:
     * `index` (`int`): track index. `-1` refreshes all tracks.
    
    Included since API version 1
    """

def dispatch(ctrlIndex: int, message: int, sysex:bytes=None) -> None:
    """Dispatch a MIDI message (either via a standard MIDI Message or through a 
    system exclusive (SysEx) message) that is sent to another controller script.
    This allows communication between different devices provided that they have
    a stardardised communication method.
    
    MIDI messages sent through this method are received in the same way as all
    other messages, so it should be ensured that they can be differentiated
    by the receiving controller.
    
    In order to allow a device to receive MIDI messages via a dispatch command,
    it must have a `receiveFrom` pre-processor comment for FL Studio to detect
    when the script is loaded. This comment should be at the top of the
    `device_MyController.py` file along with the name and URL, for example:
    
    ```py
    # name=My Controller
    # receiveFrom=My Other Controller
    ```
    After this declaration, the script named "My Other Controller" will be able
    to dispatch MIDI messages to the script named "My Controler".

    Args:
     * `ctrlIndex` (`int`): index of the controller to dispatch to
     * `message` (`int`): MIDI message to send (or header of a SysEx message)
     * `sysex` (`bytes`, optional): SysEx data to send, if applicable
    
    Included since API version 1
    """

def dispatchReceiverCount() -> int:
    """Returns the number of device scripts that this script can dispatch to.

    Returns:
     * `int`: number of available receiver devices.
    
    Included since API version 1
    """

def dispatchGetReceiverPortNumber(ctrlIndex: int) -> int:
    """Returns the port of the receiver device specified by `ctrlIndex`.

    Args:
     * `ctrlIndex` (`int`): device script to check

    Returns:
     * `int`: MIDI port associated with the reciever device
    
    Included since API version 5
    """
