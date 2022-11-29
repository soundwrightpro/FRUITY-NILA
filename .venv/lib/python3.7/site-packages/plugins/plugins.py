"""Plugins Module (FL Studio built-in)

Handles the way that scripts communicate with and control FL Studio plugins,
including 3rd-party VST/AU plugins. The module allows scripts to get and set 
parameter values for plugins on the mixer and the channel rack.

Module added in API version 8.

NOTES:
 * `index` either refers to the index of the plugin on the channel rack, or the
   index of the mixer track containing the plugin on the mixer.
 * `slotIndex` refers the the mixer slot of the plugin if it is on the mixer.
   Leave this parameter empty if the plugin is on the channel rack.
"""

import midi

def isValid(index: int, slotIndex:int=-1) -> bool:
    """Returns whether there is a valid plugin at `index`/`slotIndex`.
    
    NOTE: Audio samples are not considered to be plugins in FL Studio.

    Args:
        `index` (`int`): index on channel rack or mixer
        `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.

    Returns:
        `bool`: whether there is a valid plugin at `index`.
    
    Included since API version 8
    """

def getPluginName(index: int, slotIndex:int=-1, userName:int=0) -> str:
    """Returns the name of the plugin at `index`/slotIndex`. This returns the
    original plugin name if `userName` is `False`, otherwise the name of the
    plugin as set by the user.

    Args:
        `index` (`int`): index on channel rack or mixer
        `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.

    Returns:
        `str`: plugin name
    
    Included since API version 8, with `userName` parameter added in API version
    12
    """

def getParamCount(index: int, slotIndex:int=-1) -> int:
    """Returns the number of parameters that the plugin at `index`/`slotIndex`
    has.

    NOTE: VST plugins are listed as having `4240` parameters, but not all of
    these are necessarily used by the plugin. The first `4096` are for
    parameters, then the next `128` are used for MIDI CC sends `0` to `127`. 
    The final `16` are used for aftertouch for each MIDI channel.

    Args:
        `index` (`int`): index on channel rack or mixer
        `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.

    Returns:
        `int`: number of parameters
    
    Included since API version 8
    """

def getParamName(paramIndex: int, index: int, slotIndex:int=-1) -> str:
    """Returns the name of the parameter at `paramIndex` for the plugin at
    `index`/`slotIndex`.

    Args:
     * `paramIndex` (`int`): index of parameter
     * `index` (`int`): index of plugin on channel rack or mixer
     * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.

    Returns:
     * `str`: name of parameter
    
    Included since API version 8
    """

def getParamValue(paramIndex: int, index: int, slotIndex:int=-1) -> float:
    """Returns the value of the parameter at `paramIndex` for the plugin at
    `index`/`slotIndex`.
    
    KNOWN ISSUE: The return values of this function for VST plugins seem to be 
    very broken, often being incorrect by orders of magnitude

    Args:
     * `paramIndex` (`int`): index of parameter
     * `index` (`int`): index of plugin on channel rack or mixer
     * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.

    Returns:
     * `float`: parameter value, between `0.0` and `1.0`
    
    Included since API version 8
    """

def setParamValue(value: float, paramIndex: int, index: int, slotIndex:int=-1)\
    -> None:
    """Sets the value of the parameter at `paramIndex` for the plugin at
    `index`/`slotIndex`.
    
    NOTE: Although there are issues with the return values of `getParamValue()`,
    these issues don't appear to be present for setting the values of paramters.

    Args:
     * `value` (`float`): new value of parameter (between `0.0` and `1.0`)
     * `paramIndex` (`int`): index of parameter
     * `index` (`int`): index of plugin on channel rack or mixer
     * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.
    
    Included since API version 8
    """

def getParamValueString(paramIndex: int, index: int, slotIndex:int=-1) -> str:
    """Returns a string value of the parameter at `paramIndex` for the plugin at
    `index`/`slotIndex`. This function is only supported by some FL Studio
    plugins.

    Args:
     * `paramIndex` (`int`): index of parameter
     * `index` (`int`): index of plugin on channel rack or mixer
     * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.

    Returns:
     * `str`: string parameter value
    
    Included since API version 8
    """

def getColor(index: int, slotIndex:int=-1, flag:int=midi.GC_BackgroundColor)\
    -> int:
    """Returns various plugin colour parameter values for the plugin at 
    `index`/`slotIndex`.

    Args:
     * `index` (`int`): index of plugin on channel rack or mixer
     * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.
     * `flag` (`int`, optional): colour type to return:
            * `GC_BackgroundColor` (`0`, default): The darkest background colour
            of the plugin.
            * `GC_Semitone` (`1`): Retrieves semitone colour (in FPC, returns
              colour of drum pads).

    Returns:
     * `int`: colour (`0x--RRGGBB`)
    
    Included since API version 12
    """

def getName(index: int, slotIndex:int=-1, flag:int=midi.FPN_Param,
            paramIndex:int=0) -> str:
    """Returns various names for parts of plugins for the plugin at
    `index`/`slotIndex`.

    TODO: Verify this all works on release of API version 13.

    Args:
     * `index` (`int`): index of plugin on channel rack or mixer
     * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.
     * `flag` (`int`, optional): name type to return:
            * `FPN_Param` (`0`, default): Name of plugin parameter (requires 
              `paramIndex`)
            * `FPN_ParamValue` (`1`): Text value of plugin parameter (requires
              `paramIndex`)
            * `FPN_Semitone` (`2`): Name of note as defined by plugin (for 
              example the name of the sample linked to a note in FPC), (requires
              `paramIndex` as note)
            * `FPN_Patch` (`3`): Name of the patch defined by plugin (requires
              `paramIndex`)
            * `FPN_VoiceLevel` (`4`): Name of per-voice parameter defined by
              plugin (requires `paramIndex`)
            * `FPN_VoiceLevelHint` (`5`): Hint for per-voice parameter defined 
              byplugin (requires `paramIndex`)
            * `FPN_Preset` (`6`): For plugins that support internal presets,
              mainly VST plugins, the name of the current preset?
            * `FPN_OutCtrl` (`7`): For plugins that output controllers, the name
              of the output controller?
            * `FPN_VoiceColor` (`8`): Name of per-voice colour (requires 
              `paramIndex` as MIDI channel)?
            * `FPN_VoiceColor` (`9`): For plugins that output voices, the name
              of output voice (requires `paramIndex` as voice number)?
     * `paramIndex` (`int`, optional): index required by requested flag (if 
       necessary)

    Returns:
     * `str`: name of requested parameter
    
    Included since API version 13
    """

def getPresetCount(index: int, slotIndex:int=-1) -> int:
    """Returns the number of presets available for the selected plugin.

    Args:
     * `index` (`int`): index of plugin on channel rack or mixer
     * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.
    
    Included since API version 15
    """
  
def nextPreset(index: int, slotIndex:int=-1) -> None:
    """Navigate to the next preset for plugin at `index`/`slotIndex`.

    Args:
     * `index` (`int`): index of plugin on channel rack or mixer
     * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.
    
    Included since API version 10
    """

def prevPreset(index: int, slotIndex:int=-1) -> None:
    """Navigate to the previous preset for plugin at `index`/`slotIndex`.

    Args:
     * `index` (`int`): index of plugin on channel rack or mixer
     * `slotIndex` (`int`, optional): mixer slot if on mixer. Defaults to -1.
    
    Included since API version 10
    """
