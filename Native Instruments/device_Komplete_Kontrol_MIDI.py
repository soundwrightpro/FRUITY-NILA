# name=Komplete Kontrol MIDI
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-m32/
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-a25-a49-a61/

# GitHub for this script
# url=https://github.com/soundwrightpro/FLNI_KK

# FL Studio Forum
# https://forum.image-line.com/viewtopic.php?f=1994&t=225473
# script by Duwayne "Sound" Wright www.soundwrightpro.com and additional code from Hobyst

# Have a question? Want to be a beta tester? Have a request? Want to say hi? Join the FL Studio NI on Discord!
# https://discord.gg/7FYrJEq

# MIT License
# Copyright © 2020 Duwayne Wright

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

import device
import ui
import plugins
import channels
import math

import device_Komplete_Kontrol_DAW as kkDAW
import nihia


class KeyKompleteKontrolMIDI(): # Used a class to shield against crashes
     
    def OnInit(self):
        kkDAW.OnInit()

    def OnMidiIn(self, event):
        # Pitch Bend
        # For the A-Series, the return value is always 0. However when the pitch bend wheel is all the way up, it returns 127.
        #if (event.data1 == nihia.touch_strips["PITCH"] or event.data1 == 127):
        #    channels.setChannelPitch(channels.channelNumber(),(127/64)*event.data2-127,1)
        #    event.handled = True

        # Modulation
        if (event.data1 == nihia.touch_strips["MOD"]):
            # The plugin in the current selected channel will be the one that receives the modulation value
            if plugins.isValid(channels.selectedChannel()):
                # Value 4097 is the default CC parameter for the modulation in most Plugins
                # Value 0.50 is a magic number to get a more precise modulation output value
                plugins.setParamValue( (event.data2/127/10)/0.50/2*10, 4097,channels.selectedChannel())
            else:
                ui.setHintMsg("Modulation: %s" % round(event.data2/1.27))
            event.handled = True

KompleteKontrolMIDI = KeyKompleteKontrolMIDI()

def OnInit():
   # command to initialize the protocol handshake
   KompleteKontrolMIDI.OnInit()

def OnMidiIn(event):
    KompleteKontrolMIDI.OnMidiIn(event)