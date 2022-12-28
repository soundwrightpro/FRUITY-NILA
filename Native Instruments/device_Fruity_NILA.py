# name=Fruity NILA
# url=https://forum.image-line.com/viewtopic.php?p=1497550#p1497550
# supportedDevices=Komplete Kontrol M DAW,Komplete Kontrol A DAW


"""
[[
	Surface:	Komplete Kontrol M DAW and/or Komplete Kontrol A DAW
	Developer:	Duwayne WRIGHT
	Version:	10.0.0

    Copyright (c) 2022 Duwayne WRIGHT
]]
"""


import nihia
from nihia import mixer as nihia_mixer

from script.NILA_UI import *
from script.device_setup import *
from script.led_writer import NILA_LED
from script.screen_writer import NILA_OLED

import general
import time
import ui


class Core(): 

	def OnInit(self):
		NILA_core.OnInit(self)

	def OnMidiMsg(self, event): 
		NILA_buttons.OnMidiMsg(event)
		NILA_mixer.OnMidiMsg(self, event)
		NILA_channel_rack.OnMidiMsg(self, event)
		NILA_piano_roll.OnMidiMsg(self, event)
		NILA_navigation.encoder(self, event)
		NILA_plugins.plugin(self,event)
		NILA_touch_strips.OnMidiMsg(event)

	def OnRefresh(self, flags): 
		NILA_LED.OnRefresh(self, flags)
		NILA_OLED.namingTrack(self, flags)

	def OnUpdateBeatIndicator(self, Value):
		NILA_LED.OnUpdateBeatIndicator(self, Value)
		NILA_OLED.OnUpdateBeatIndicator(self,Value)

	def OnWaitingForInput(self):
		nihia_mixer.setTrackName(0, config.wait_input_1)
		nihia_mixer.setTrackVol(0, config.wait_input_2)

	def OnProjectLoad(self,status):
		NILA_core.OnProjectLoad(self, status)
	
	def OnIdle(self):
		NILA_playlist.OnIdle()
		NILA_OLED.OnIdle()


n_Core = Core()


def OnInit():
	compatibility = False
	if NILA_version_check.VersionCheck(compatibility) == True:
		n_Core.OnInit()
	else:
		pass

def OnMidiMsg(event):
    n_Core.OnMidiMsg(event)

def OnRefresh(flags):
	n_Core.OnRefresh(flags)

def OnUpdateBeatIndicator(Value):
	n_Core.OnUpdateBeatIndicator(Value)

def OnWaitingForInput():
	n_Core.OnWaitingForInput()

def OnProjectLoad(status):
   n_Core.OnProjectLoad(status)

def OnIdle():
	n_Core.OnIdle()

def OnDeInit():
	if ui.isClosing() == True:
		nihia.goodBye()