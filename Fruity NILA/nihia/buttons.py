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
Subfile of flmidi-nihia used to manipulate the state of buttons of Komplete Kontrol keyboards.
"""

import nihia

# Button name to button ID dictionary
# The button ID is the number in hex that is used as the DATA1 parameter when a MIDI message related to that button is
# sent or received from the device
button_list = {
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
    
    "TRACK_SELECT": 66,
    "MUTE": 67,
    "SOLO": 68,

    "MUTE_SELECTED": 102,
    "SOLO_SELECTED": 103,

    "ENCODER_BUTTON": 96,
    "ENCODER_BUTTON_SHIFTED": 97,
    
    # The 4D encoder events use the same data1, but different data2
    # For example, if you want to retrieve the data1 value for ENCODER_PLUS you would do nihia.buttons.get("ENCODER_PLUS")[0]
    # 
    # data1 values are inverted for the axis of the 4D Encoder between A/M devices and S devices
    # The values represented here correspond to A/M-Series
    # D-pad
    "ENCODER_X_A": 50,
    "ENCODER_X_S": 48,
    "RIGHT": 1,
    "LEFT": 127,
    
    "ENCODER_Y_A": 48,
    "ENCODER_Y_S": 50,
    "UP": 127,
    "DOWN": 1,

    # Jog / knob
    "ENCODER_GENERAL": 52,
    "ENCODER_VOLUME_SELECTED": 100,
    "ENCODER_PAN_SELECTED": 101,

    "PLUS": 1,
    "MINUS": 127
}

# Method for controlling the lighting on the buttons (for those who have idle/highlighted two state lights)
# Examples of this kind of buttons are the PLAY or REC buttons, where the PLAY button alternates between low and high light and so on.
# SHIFT buttons are also included in this range of buttons, but instead of low/high light they alternate between on/off light states.
def setLight(buttonName: str, lightMode: int):
    """ Method for controlling the lights on the buttons of the device. 
    
    ### Parameters

     - buttonName: Name of the button as shown in the device in caps and enclosed in quotes. ("PLAY", "AUTO", "REDO"...)
        - EXCEPTION: declare the Count-In button as COUNT_IN
    
     - lightMode: If set to 0, sets the first light mode of the button. If set to 1, sets the second light mode."""

    #Light mode integer to light mode hex dictionary
    lightModes = {
        0: 0,
        1: 1,

        # For setting lights on of the right and down dot lights of the 4D Encoder on S-Series devices
        127: 127
    }

    # Then sends the MIDI message using dataOut
    nihia.dataOut(button_list.get(buttonName), lightModes.get(lightMode))