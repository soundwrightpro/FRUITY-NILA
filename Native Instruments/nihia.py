# MIT License
# Copyright © 2020 Hobyst

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

# Library for using the NIHIA protocol on FL Studio's MIDI Scripting API

# This script contains all the functions and methods needed to take advantage of the deep integration
# features on Native Instruments' devices
# Any device with this kind of features will make use of this script

import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import midi
import utils

import device_Komplete_Kontrol_DAW as kk

# Method to make talking to the device less annoying
# All the messages the device is expecting have a structure of "BF XX XX"
# The STATUS byte always stays the same and only the DATA1 and DATA2 vary

buttons = {
    "PLAY": 16,
    "RESTART": 17,
    "REC": 18,
    "COUNT_IN": 19,
    "STOP": 20,
    "CLEAR": 21,
    "LOOP": 22,
    "METRO": 23,
    "TEMPO": 24,
    
    "UNDO": 32,
    "REDO": 33,
    "QUANTIZE": 34,
    "AUTO": 35,

    "IS_MUTE": 67,
    "IS_SOLO": 68,

    "MUTE_SELECTED": 102,
    "SOLO_SELECTED": 103,

    # The 4D encoder events use the same data1, but different data2
    # For example, if you want to retrieve the data1 value for ENCODER_PLUS 
    # you would do nihia.buttons.get("ENCODER_PLUS")[0]
    "ENCODER_BUTTON": 96,
    "SHIFT+ENCODER_BUTTON": 97,
    
    "ENCODER_RIGHT": [50, 1],
    "ENCODER_LEFT": [50, 127],
    
    "ENCODER_UP": [48, 127],
    "ENCODER_DOWN": [48, 1],

    "ENCODER_PLUS": [52, 1],
    "ENCODER_MINUS": [52, 127],

    "ENCODER_HORIZONTAL": 50,
    "ENCODER_VERTICAL": 48,   

    "ENCODER_SPIN": 52
}

knobs = {
    "KNOB_0A": 80, 
    "KNOB_1A": 81,
    "KNOB_2A": 82,
    "KNOB_3A": 83,
    "KNOB_4A": 84,
    "KNOB_5A": 85,
    "KNOB_6A": 86,
    "KNOB_7A": 87,

    "KNOB_0B": 88,
    "KNOB_1B": 89,
    "KNOB_2B": 90,
    "KNOB_3B": 91,
    "KNOB_4B": 92,
    "KNOB_5B": 93,
    "KNOB_6B": 94,
    "KNOB_7B": 95,

    "INCREASE": 63,
    "DECREASE": 65
}

touch_strips = {
   "PITCH": 0,
   "MOD": 1
}

message = {
   "EMPTY": " ",
   "CHANNEL_RACK": "C| ",
   "BROWSER": "B| ",
   "WAITING": "Waiting on Input"
}


mixerinfo_types = {
    "VOLUME": 70,
    "PAN": 71,
    "IS_MUTE": 67,
    "IS_SOLO": 68,
    "NAME": 72,
    
    # This one makes more sense on DAWs that create more tracks as the user requests it, as there might be projects (for example) on Ableton Live
    # with only two tracks
    # However, since FL Studio has all playlist and mixer tracks created, it has no use at all (maybe on the channel rack) and all tracks should have
    # their existance reported as 1 (which means the track exists) in order to light on the Mute and Solo buttons on the device
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




#on/off values
on = 1
off = 0
 
def dataOut(data1, data2):
    """ Function that makes communication with the keyboard easier. By just entering the DATA1 and DATA2 of the MIDI message, 
    it composes the full message in forther to satisfy the syntax required by the midiOut functions, as well as the setting 
    the STATUS of the message to BF as expected.""" 
    
    # Composes the MIDI message and sends it
    convertmsg = [240, 191, data1, data2] # takes message and add the header required for communication with device
    msgtom32 = bytearray(convertmsg) #converts message array into bytes, 1 turns into 0x01 but in b/01/ format
    device.midiOutSysex(bytes(msgtom32)) #converts to 0x01 format

def printText(trkn, word):

      """ Function for easing the communication with the device OLED easier. The device has 8 slots 
      that correspond to the 8 knobs. Knobs 0 through 7 on the device. Slot 0 (aka Knob 0 aka the
      first knob from the left) is also use to display temporary messages. """

      lettersh = [] #array where message to screen will be broken down by letter and/or spaces, i.e. hello turns into [h,e,l,l,o] **1
      header = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 72, 0] #required header in message to tell m32 where to place track title

      n = 0
      m = 0

      letters = list(word) #convert word into letters in array

      if len(letters) <= 11: #if the message to screen is less than 11 characters convert to message by letters see -> **1
         while n < len(letters): #convert letters in array to integer representing the Unicode character
            if ord(letters[n]) > 256:
               n +=1
            else:
               lettersh.append(ord(letters[n]))
               n += 1
      else:
         while n < 12: #convert letters in array to integer representing the Unicode character
            if ord(letters[n]) > 256:
               n += 1
            else:   
               lettersh.append(ord(letters[n]))
               n += 1
         
      header.append(trkn) #adding track number to header at the end 

      while m < len(lettersh): #combining header array and unicode value array together; just makes it easier to send to device
         header.append(lettersh[m])
         m += 1 

      header.append(247) #tells m32, that's it that's the whole word
      
      device.midiOutSysex(bytes(header)) #send unicode values as bytes to OLED screen
    
def printVol(trkn, vol):

      """ function that makes sending vol to the OLED screen easier"""
       
      volk = ""
      
      lettersh = [] 
      header = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 70, 0,] 

      p = 0
      n = 0
      m = 0

      vol==(float(vol))

      if vol <= -60.0:
         volk = "- oo dB"
         letters = list(volk) 

         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1
 
      elif vol >= -59.0 and vol <= 6.00:

         volk = '%s dB' % (vol) # volume displayed in dB from here
         letters = list(volk)
         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1 # end of volume in dB
         
      elif vol >= 103:
         volk = "N/A"
         letters = list(volk) 

         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1   

      header.append(trkn)
      
      while m < len(lettersh):
         header.append(lettersh[m])
         m += 1

      header.append(247)

      device.midiOutSysex(bytes(header))

def printPan(trkn, pan): 

      pan = round(pan,0)

      volk = ""

      lettersh = [] 
      header = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 71, 0,]

      p = 0
      n = 0
      m = 0

      header.append(trkn)
      

      if pan == 0:
         volk = "Centered"
         letters = list(volk) 

         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1 

      elif pan < 0:
         
         volk = u'%d%% Left' % round((pan*-1),2)
         letters = list(volk) 
         
         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1

      elif pan > 0 and pan < 101:
         
         volk = u'%d%% Right' % round((pan),2)
         letters = list(volk) 
         
         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1 

      elif pan >= 103:
         volk = "N/A"
         letters = list(volk) 

         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1        

      while m < len(lettersh):
         header.append(lettersh[m])
         m += 1

      header.append(247)

      device.midiOutSysex(bytes(header))

# Method to enable the deep integration features on the device
def initiate():
    """ Acknowledges the device that a compatible host has been launched, wakes it up from MIDI mode and activates the deep
    integration features of the device. TODO: Then waits for the answer of the device in order to confirm if the handshake 
    was successful and returns True if affirmative."""

    # Sends the MIDI message that initiates the handshake: BF 01 01

    dataOut(1,3)
    #turning on group of lights not initialized during the nihia.initiate()
    dataOut(buttons["CLEAR"], on)
    dataOut(buttons["UNDO"], on) 
    dataOut(buttons["REDO"], on) 
    dataOut(buttons["AUTO"], on) 
    dataOut(buttons["QUANTIZE"], on) 
    dataOut(buttons["TEMPO"], on)
    device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 64, 1, 0, 247])) # 'mute' & 'solo' button lights activated

    # TODO: Waits and reads the handshake confirmation message
   
# Method to deactivate the deep integration mode. Intended to be executed on close.
def terminate():
    """ Sends the goodbye message to the device and exits it from deep integration mode. 
    Intended to be executed before FL Studio closes."""

    # Sends the goodbye message: BF 02 01
    dataOut(2, 1)

# Method for restarting the protocol on demand. Intended to be used by the end user in case the keyboard behaves 
# unexpectedly.
def restartProtocol():
    """ Sends the goodbye message to then send the handshake message again. """

    # Turns off the deep integration mode
    terminate()

    # Then activates it again
    initiate()
    

# Method for controlling the lighting on the buttons (for those who have idle/highlighted two state lights)
# Examples of this kind of buttons are the PLAY or REC buttons, where the PLAY button alternates between low and high light and so on.
# SHIFT buttons are also included in this range of buttons, but instead of low/high light they alternate between on/off light states.
def buttonSetLight(buttonName: str, lightMode: int):
    """ Method for controlling the lights on the buttons of the device. 
    
    buttonName -- Name of the button as shown in the device in caps and enclosed in quotes. ("PLAY", "AUTO", "REDO"...)
    EXCEPTION: declare the Count-In button as COUNT_IN
    
    lightMode -- If set to 0, sets the first light mode of the button. If set to 1, sets the second light mode."""

    #Light mode integer to light mode hex dictionary
    lightModes = {
        0: 0,
        1: 1
    }

    # Then sends the MIDI message using dataOut
    dataOut(buttons.get(buttonName), lightModes.get(lightMode))

# Dictionary that goes between the different kinds of information that can be sent to the device to specify information about the mixer tracks
# and their corresponding identification bytes
mixerinfo_types = {
    "VOLUME": 70,
    "PAN": 71,
    "IS_MUTE": 67,
    "IS_SOLO": 68,
    "NAME": 72,
    
    # This one makes more sense on DAWs that create more tracks as the user requests it, as there might be projects (for example) on Ableton Live
    # with only two tracks
    # However, since FL Studio has all playlist and mixer tracks created, it has no use at all (maybe on the channel rack) and all tracks should have
    # their existence reported as 1 (which means the track exists) in order to light on the Mute and Solo buttons on the device
    "EXIST": 64,
    "SELECTED": 66,
}

# Method for reporting information about the mixer tracks, which is done through SysEx
# Couldn't make this one as two different functions under the same name since Python doesn't admit function overloading
def mixerSendInfo(info_type: str, trackID: int, **kwargs):
    """ Sends info about the mixer tracks to the device.
    
    ### Parameters

     - info_type: The kind of information you're going to send as defined on `mixerinfo_types`. ("VOLUME", "PAN"...)
         - Note: If declared as `"EXIST"`, you can also declare the track type on the `value` argument as a string (values are contained in `track_types` dictionary).
    
     - trackID: From 0 to 7. Tells the device which track from the ones that are showing up in the screen you're going to tell info about.

    The third (and last) argument depends on what kind of information you are going to send:

     - value (integer): Can be 0 (no) or 1 (yes). Used for two-state properties like to tell if the track is solo-ed or not (except `"EXIST"`).

     - info: Used for track name, track pan, track volume and the Komplete Kontrol instance ID.

     - peakValues: For peak values. They can be neither integers or floats, and they will get reformated automatically. You can
    also use the `mixer.getTrackPeaks` function directly to fill the argument, but remember you have to specify the left and the right channel separately. You have to 
    report them as a list of values: `peak=[peakL_0, peakR_0, peakL_1, peakR_1 ...]`
    """

    # Gets the inputed values for the optional arguments from **kwargs
    value = kwargs.get("value", 0)
    info = kwargs.get("info", None)

    peakValues = kwargs.get("peakValues", None)

    # Compatibility behaviour for older implementations of the layer before the addition of track_types
    # This will retrieve the correct value in case the developer used the string based declaration
    if type(value) == str:
        value = track_types.get(value, 0)


    # Defines the behaviour for when additional info is reported (for track name, track pan, track volume and peak values)
    if info != None:
        # Tells Python that the additional_info argument is in UTF-8
        info = info.encode("UTF-8")

        # Converts the text string to a list of Unicode values
        info = list(bytes(info))
        
        # Conforms the kind of message midiOutSysex is waiting for
        msg = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type), value, trackID] + info + [247]

        # Warps the data and sends it to the device
        device.midiOutSysex(bytes(msg))

    # For peak values
    # Takes each value from the dictionary and rounds it in order to avoid conflicts with hexadecimals only being "compatible" with integer numbers 
    # in case peak values are specified
    elif peakValues != None:
            
        for x in range(0, 16):
            # Makes the max of the peak meter on the device match the one on FL Studio (values that FL Studio gives seem to be infinite)
            if peakValues[x] >= 1.1:
                peakValues[x] = 1.1
        
            # Translates the 0-1.1 range to 0-127 range
            peakValues[x] = peakValues[x] * (127 / 1.1)
        
            # Truncates the possible decimals and declares the number as an integer to avoid errors in the translation of the data
            peakValues[x] = int(math.trunc(peakValues[x]))

        # Conforms the kind of message midiOutSysex is waiting for
        msg = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type), 2, trackID] + peakValues + [247]

        # Warps the data and sends it to the device
        device.midiOutSysex(bytes(msg))

    # Defines how the method should work normally
    elif info == None:
        
        # Takes the information and wraps it on how it should be sent and sends the message
        device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type), value, trackID, 247]))

def mixerSendInfoSelected(info_type: str, info: str):
    """ Makes the device report MIDI messages for volume and pan adjusting for the selected track when existence of this track is reported as true.
    ### Parameters
     - info_type: The data you are going to tell about the selected track.
         - SELECTED: If there's a track selected on the mixer or not.
         - MUTE_BY_SOLO: To tell if it's muted by solo.
     - info: The value of the info you are telling.
         - `info_type = SELECTED`: The track type as defined on `track_types`.
         - `info_type = MUTE_BY_SOLO`: Yes or no.
    """
    if info_type == "SELECTED":
        info_type = mixerinfo_types.get("SELECTED_AVAILABLE")

        info = track_types.get(info)
    
    # Not implemented yet in FL Studio
    elif info_type == "MUTE_BY_SOLO":
        info_type = mixerinfo_types.get("SELECTED_MUTE_BY_SOLO")
    

    # Sends the message
    dataOut(info_type, info)