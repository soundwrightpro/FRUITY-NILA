# name=Fruity NILA for MIDI
# url=https://forum.image-line.com/viewtopic.php?p=1497550#p1497550
# supportedDevices=Komplete Kontrol M DAW,Komplete Kontrol A DAW


"""
[[
	Surface:	Komplete Kontrol M DAW and/or Komplete Kontrol A DAW
	Developer:	Duwayne WRIGHT
	Version:	21.0 

    Copyright (c) 2022 Duwayne WRIGHT
]]
"""

import device_Fruity_NILA as NILA

import channels
import device
import math
import plugins
import ui 

touch_strips = {
   "PITCH": 0,
   "MOD": 1
}


class MIDI_Core(): 

    def OnInit(self):
        NILA.OnInit()

    def OnMidiMsg(self, event):

        if (event.data1 == touch_strips["MOD"]):
            event.handled = True

            if plugins.isValid(channels.selectedChannel()):
                plugins.setParamValue((event.data2/127/10)/0.50/2*10, 4097, channels.selectedChannel())
                ui.setHintMsg("Modulation: %s" % round(event.data2/1.27))
            else:
                ui.setHintMsg("Modulation: %s" % round(event.data2/1.27))


MIDI_Core = MIDI_Core()

def OnInit():
   MIDI_Core.OnInit()

def OnMidiMsg(event):
    MIDI_Core.OnMidiMsg(event)