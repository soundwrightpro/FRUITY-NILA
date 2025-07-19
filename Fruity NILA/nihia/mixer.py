# MIT License

# Copyright (c) 2021 Pablo Peral

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Submodule of flmidi-nihia for mixer manipulation of Komplete Kontrol keyboards.
"""

import nihia
import device
import math

###########################################################################################################################################
# Dictionaries and constants
###########################################################################################################################################

# Knob to knob ID matrix
# Each knob has two possible DATA1 values, one for volume and another for pan adjustment
# The rows specify the knob mode (volume adjustment and shifted/pan adjustment knobs)
# The columns specify the knob
# Example:
#   knobs[0][0] --> First knob without shift. It is meant to adjust volume.
#   knobs[0][1] --> First knob shifted (SHIFT button is being held down while using the knob). It is meant to adjust panning.
knobs = [
    [80, 81, 82, 83, 84, 85, 86, 87],
    [88, 89, 90, 91, 92, 93, 94, 95]
]

# The DATA2 value of a knob turning message specifies the speed the user is turning the knob at
# On S-Series keyboards, the knobs are speed-sensitive and send different DATA2 values to specify the turning speed
# - If turned clockwise, the speed will go from 0 to 63 (slowest to fastest)
# - If turned counterclockwise, the speed will go from 127 to 65 (slowest to fastest, they are inverted)
# On A/M-Series, the knobs aren't speed-sensitive and they will always report the max value for each direction
# - If turned clockwise, the DATA2 value will be 63
# - If turned counterclockwise, the DATA2 value will be 65
KNOB_INCREASE_MIN_SPEED = 0     # DATA2 byte sent by the keyboard on clockwise knob turning messages at minimum speed
KNOB_INCREASE_MAX_SPEED = 63    # DATA2 byte sent by the keyboard on clockwise knob turning messages at maximum speed

KNOB_DECREASE_MIN_SPEED = 127   # DATA2 byte sent by the keyboard on counterclockwise knob turning messages at minimum speed
KNOB_DECREASE_MAX_SPEED = 65    # DATA2 byte sent by the keyboard on counterclockwise knob turning messages at maximum speed

# Dictionary that goes between the different kinds of information that can be sent to the device to specify information about the mixer tracks
# and their corresponding identification bytes
mixerinfo_types = {
    "VOLUME": 70,
    "PAN": 71,
    "IS_MUTE": 67,
    "IS_SOLO": 68,
    "NAME": 72,
    "IS_ARMED": 69,
    "MUTED_BY_SOLO": 74,
    
    "MUTE_SELECTED": 102,
    "SOLO_SELECTED": 103,

    # This one makes more sense on DAWs that create more tracks as the user requests it, as there might be projects (for example) on Ableton Live
    # with only two tracks
    # However, since FL Studio has all playlist and mixer tracks created, it has no use at all (maybe on the channel rack) and all tracks should have
    # their existence reported as 1 (which means the track exists) in order to light on the Mute and Solo buttons on the device
    "EXIST": 64,
    "SELECTED": 66,

    "SELECTED_AVAILABLE": 104,
    "SELECTED_MUTE_BY_SOLO": 105,

    # This one only will make an effect on devices with full feature support, like the S-Series MK2 and it's used to send the peak meter information
    "PEAK": 73,

    # Serves to tell the device if there's a Komplete Kontrol instance added in a certain track or not
    # In case there's one, we would use mixerSendInfo("KOMPLETE_INSTANCE", trackID, info="NIKBxx")
    # In case there's none, we would use mixerSendInfo("KOMPLETE_INSTANCE", trackID, info="")
    # NIKBxx is the name of the first automation parameter of the Komplete Kontrol plugin
    "KOMPLETE_INSTANCE": 65,

    # The S-Series keyboard have two arrows that graphically show the position of the volume fader and the pan on the screen
    # These definitions have the MIDI values that have to be set as the data1 value of a simple MIDI message to tell the device where the volume arrow
    # or the pan arrow should be for the first track
    # For the rest of the tracks, you sum incrementally
    # Example:
    # ----------------------------------------------------
    # BF 50 00  // Moves the volume fader of the first track down to the bottom 
    # BF 50 40  // Moves the volume fader of the first track to the middle
    # 
    # BF 51 00  // Moves the volume fader of the second track down to the bottom 
    # BF 51 40  // Moves the volume fader of the second track to the middle
    # 
    # BF 58 00  // Moves the pan fader of the first track down to the bottom 
    # BF 58 40  // Moves the pan fader of the first track to the middle
    # 
    # BF 59 00  // Moves the pan fader of the second track down to the bottom 
    # BF 59 40  // Moves the pan fader of the second track to the middle    
    
    "VOLUME_GRAPH": 80,
    "PAN_GRAPH": 88,
}

# Track types dictionary
# Used when reporting existence of tracks
track_types = {
    "EMPTY": 0,
    "GENERIC": 1,
    "MIDI": 2,
    "AUDIO": 3,
    "GROUP": 4,
    "RETURN_BUS": 5,
    "MASTER": 6
}

# Methods for reporting information about the mixer tracks, which is done through SysEx
def setTrackExist(trackID: int, value: int or str):
    """ Method to report existence of a track and update its type as well.

    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - value (int or str): Track type from `track_types`.
    """

    if value == str:
        value = track_types.get(track_types)

    # Conforms the kind of message midiOutSysex is waiting for
    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("EXIST"), value, trackID] + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

def setTrackName(trackID: int, name: str):
    """ Method to update the name of a track being displayed on the device.

    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - name (str): Name of the track.
    """
    # Conforms the kind of message midiOutSysex is waiting for
    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("NAME"), 0, trackID] + Str2Bytes(name) + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

def setTrackPan(trackID: int, value: str):
    """ Method to update the pan string of a track being displayed on the device.

    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - value (str): String to show on the display as the pan of the track.
    """
    # Conforms the kind of message midiOutSysex is waiting for
    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("PAN"), 0, trackID] + Str2Bytes(value) + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

def setTrackVol(trackID: int, value: str):
    """ Method to update the volume string of a track being displayed on the device.

    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - value (str): String to show on the display as the volume of the track.
    """
    # Conforms the kind of message midiOutSysex is waiting for
    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("VOLUME"), 0, trackID] + Str2Bytes(value) + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

def setTrackArm(trackID: int, value: bool):
    """ Method to report the arm for recording state state of a track.

    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - value (Bool): Selection status.
    """
    # Conforms the kind of message midiOutSysex is waiting for
    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("IS_ARMED"), value, trackID] + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

def setTrackSel(trackID: int, value: bool):
    """ Method to report selection state of a track.

    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - value (bool): Selection status.
    """
    # Conforms the kind of message midiOutSysex is waiting for
    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("SELECTED"), value, trackID] + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

def setTrackSolo(trackID:int, value: bool):
    """ Method to report solo state of a track.

    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - value (bool): Solo status.
    """
    # Conforms the kind of message midiOutSysex is waiting for
    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("IS_SOLO"), value, trackID] + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

def setTrackMute(trackID:int, value: bool):
    """ Method to report mute state of a track.

    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - value (bool): Mute status.
    """
    # Conforms the kind of message midiOutSysex is waiting for
    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("IS_MUTE"), value, trackID] + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

def setTrackMutedBySolo(trackID:int, value: bool):
    """ Method to report mute by solo state of a track.

    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - value (bool): Mute by solo status.
    """
    # Conforms the kind of message midiOutSysex is waiting for
    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("MUTED_BY_SOLO"), value, trackID] + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

def setTrackKompleteInstance(trackID: int, instanceID: str):
    """ Method to report the Komplete Kontrol instance a mixer track is associated to.
    
    ### Arguments
    - trackID (int): From 0 to 7, the number of the track being represented on the display.
    - instanceID (str): The `NIKBxx` string retrieved from the name of the first automation parameter of the Komplete Kontrol instance.
      If it's left to nothing (`""`), the Komplete Kontrol integration will be disabled for that track.
    """

    msg = nihia.SYSEX_HEADER + [mixerinfo_types.get("KOMPLETE_INSTANCE"), 0, trackID] + Str2Bytes(instanceID) + [247]

    device.midiOutSysex(bytes(msg))

def sendPeakMeterData(peakValues: list):
    """ Send peak meter data to be displayed on the device.

    ### Arguments
     - peakValues (list): A list of 16 integer values representing peak values for each track and stereo channel like ``[peakL_0, peakR_0, peakL_1, peakR_1 ...]``
     in a range of 0 to 127. To convert values coming from FL Studio's ``mixer.getTrackPeaks()`` function, the reccomended range is 0 to 1.1 so that any value
     greater than 1.1 should be set to 1.1 anyway.
    """

    # Conforms the kind of message midiOutSysex is waiting for
    msg = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get("PEAK"), 2, 0] + peakValues + [247]

    # Warps the data and sends it to the device
    device.midiOutSysex(bytes(msg))

# Methods for changing the locations of the pan and volume arrows on the screen of S-Series devices to graphically show where the pan and volume faders are
def setTrackVolGraph(trackID: int, location: float):
    """ Method for changing the location of the volume arrow of a track on the screen of S-Series MK2 devices to graphically show where the volume fader is.
    ### Arguments
     - trackID: From 0 to 7, the track whose the graph you want to update belongs to.
     - location: Can be filled using `mixer.getTrackVolume()`, expecting a `0 <= x <= 1` range.
    """
    # Gets the right data1 value to update the volume graph
    graphValue = mixerinfo_types.get("VOLUME_GRAPH")
    
    # Translates the 0-1 range given by FL Studio to 0-127 range
    location = location * 127
    
    # Truncates the possible decimals and declares the number as an integer to avoid errors in the translation of the data
    location = int(math.trunc(location))

    # Reports the change of the desired graph to the device
    nihia.dataOut(graphValue + trackID, location)

def setTrackPanGraph(trackID: int, location: float):
    """ Method for changing the location of the pan arrow of a track on the screen of S-Series MK2 devices to graphically show where the pan fader is.
    ### Arguments
     - trackID: From 0 to 7, the track whose the graph you want to update belongs to.
     - location: Can be filled using `mixer.getTrackPan()`, expecting a `-1 <= x <= 1` range.
    """
    # Gets the right data1 value to update the pan graph
    graphValue = mixerinfo_types.get("PAN_GRAPH")
    
    # Translates the -1 to 1 range from FL Studio to 0-127 range
    if location < 0:  # If the pan is negative, for hence is set to the left
        location = abs(location)    # Gets the absolute value of the location
        location = 64 - location * 64
    
    elif location == 0: # If the pan is 0, for hence is set to the center
        location = 64
    
    elif location > 0:  # If the pan is positive, for hence is set to the right
        location = 64 + location * 63
    
    # Truncates the possible decimals and declares the number as an integer to avoid errors in the translation of the data
    location = int(math.trunc(location))

    # Reports the change of the desired graph to the device
    nihia.dataOut(graphValue + trackID, location)

# Deprecated due to not having enough knowledge about how this actually works TODO
# -----------------------
# def setSelTrack(info_type: str, info: str):
#     """ Send selection state of a mixer track.
#     ### Parameters
#      - info_type: The data you are going to tell about the selected track.
#          - SELECTED: If there's a track selected on the mixer or not.
#          - MUTE_BY_SOLO: To tell if it's muted by solo.
#      - info: The value of the info you are telling.
#          - `info_type = SELECTED`: The track type as defined on `track_types`.
#          - `info_type = MUTE_BY_SOLO`: Yes or no.
#     """
#     if info_type == "SELECTED":
#         info_type = mixerinfo_types.get("SELECTED_AVAILABLE")

#         info = track_types.get(info)
    
#     # Not implemented yet in FL Studio
#     elif info_type == "MUTE_BY_SOLO":
#         info_type = mixerinfo_types.get("SELECTED_MUTE_BY_SOLO")

#     # Sends the message
#     dataOut(info_type, info)

def setCurrentTrackAvailable(track_type: int or str):
    """ Unknown functionality TODO
    ### Arguments
     - track_type (int or str): Track types as specified on `track_types`.
    """
    if track_type == str:
        track_type = track_types.get(track_type)

    # Sends the message
    nihia.dataOut(mixerinfo_types.get("SELECTED_AVAILABLE"), track_type)

def setCurrentTrackMuted(value: bool):
    """ Sets the mute status of the currently selected track. Used just to highlight change the light of the MUTE button
    between dimmed and highlighted. For this method to take an effect, track existence must have been declared beforehand. 
    
    ### Arguments
     - value (bool): Mute status. 
    """
    # Sends the message
    nihia.dataOut(mixerinfo_types.get("MUTE_SELECTED"), value)

def setCurrentTrackSolo(value: bool):
    """ Sets the solo status of the currently selected track. Used just to highlight change the light of the MUTE button
    between dimmed and highlighted. For this method to take an effect, track existence must have been declared beforehand. 
    
    ### Arguments
     - value (bool): Mute status. 
    """
    # Sends the message
    nihia.dataOut(mixerinfo_types.get("SOLO_SELECTED"), value)

def setCurrentTrackMuteBySolo(value: str):
    """ 
    Unknown functionality TODO
    ### Arguments
     - value (bool):
    """

    # Sends the message
    nihia.dataOut(mixerinfo_types.get("SELECTED_MUTE_BY_SOLO"), value)

def Str2Bytes(string: str) -> list:
    """ Utility function that encodes a given string to a Python list of its corresponding values in the UTF-8 standard.

    ### Args
     - str (str): String to encode

    ### Returns
     - list: List of the corresponding bytes to the string specified on function call in the UTF-8 standard.
    """

    # Tells Python that the additional_info argument is in UTF-8
    string = string.encode("UTF-8")

    # Converts the text string to a list of Unicode values
    string = list(bytes(string))

    return string
