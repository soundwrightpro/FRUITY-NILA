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
Python package for the FL Studio MIDI API to take advantage of the MIDI mode of the Native Instruments Host 
Integration Agent protocol and use the DAW integration mode of Komplete Kontrol keyboards.
"""

# List of submodules
__all__ = ["buttons", "mixer"]

import device
import transport
import ui 
import channels
import general
import device 
import midi
import mixer

###########################################################################################################################################
# Dictionaries and constants
###########################################################################################################################################

# List of bytes that every SysEx message for the keyboard begins with
SYSEX_HEADER = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0]

###########################################################################################################################################
# Methods and functions
###########################################################################################################################################

# Method to make talking to the device less annoying
# All the messages the device is expecting have a structure of "BF XX XX"
# The STATUS byte always stays the same and only the DATA1 and DATA2 vary
def dataOut(data1: int or hex, data2: int or hex):
    """ Function for easing the communication with the device. By just entering the DATA1 and DATA2 bytes of the MIDI message that has to be sent to the device, it 
    composes the full message in order to satisfy the syntax required by the midiOutSysex method, 
    as well as setting the STATUS of the message to BF as expected and sends the message. 
    
    data1, data2 -- Corresponding bytes of the MIDI message."""
    
    # Composes the MIDI message and sends it
    device.midiOutSysex(bytes([240, 191, data1, data2, 247]))

# Method to enable the deep integration features on the device
def handShake():
    """ Acknowledges the device that a compatible host has been launched, wakes it up from MIDI mode and activates the deep
    integration features of the device. TODO: Then waits for the answer of the device in order to confirm if the handshake 
    was successful and returns True if affirmative."""

    # Sends the MIDI message that initiates the handshake: BF 01 01
    dataOut(1, 3)

    # TODO: Waits and reads the handshake confirmation message
   

# Method to deactivate the deep integration mode. Intended to be executed on close.
def goodBye():
    """ Sends the goodbye message to the device and exits it from deep integration mode. 
    Intended to be executed before FL Studio closes."""

    # Sends the goodbye message: BF 02 01
    dataOut(2, 1)
