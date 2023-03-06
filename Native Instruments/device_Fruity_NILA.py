# name=Fruity NILA
# url=https://forum.image-line.com/viewtopic.php?p=1497550#p1497550
# supportedDevices=Komplete Kontrol M DAW, Komplete Kontrol A DAW, KOMPLETE KONTROL M32, Komplete Kontrol DAW 1
# receiveFrom=Forward Device

"""
[[
	Surface:	Komplete Kontrol S-Series , Komplete Kontrol M-Series , Komplete Kontrol A-Series, 
	Developer:	Duwayne WRIGHT
	Version:	11.0 

    Copyright (c) 2023 Duwayne WRIGHT
]]
"""


import nihia
from nihia import *
import nihia.mixer as NILA_mixer
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
		if event.midiChan == config.controls:
			NILA_navigation.encoder(self, event)
			NILA_buttons.OnMidiMsg(event)
			NILA_mixer.OnMidiMsg(self, event)
			NILA_channel_rack.OnMidiMsg(self, event)
			NILA_piano_roll.OnMidiMsg(self, event)
			NILA_plugins.plugin(self,event)

		else:
			NILA_touch_strips.OnMidiIn(event)

	def OnRefresh(self, flags):
		NILA_LED.OnRefresh(self, flags)
		NILA_OLED.OnRefresh(self, flags)

	def OnUpdateBeatIndicator(self, Value):
		NILA_LED.OnUpdateBeatIndicator(self, Value)
		NILA_OLED.OnUpdateBeatIndicator(self,Value)

	def OnWaitingForInput(self):
		NILA_mixer.setTrackName(0, config.wait_input_1)
		NILA_mixer.setTrackVol(0, config.wait_input_2)

	def OnProjectLoad(self, status):
		NILA_core.OnProjectLoad(self, status)
	
	def OnIdle(self):
		NILA_OLED.OnIdle(self)
	
	def OnUpdateMeters(self):
		NILA_OLED.sendPeakInfo()

	

n_Core = Core()


def OnInit():
	#try:
		compatibility = False
		if NILA_version_check.VersionCheck(compatibility) == True:
			n_Core.OnInit()
		else:
			pass
	#except:
		#pass

def OnMidiMsg(event):
	#try:
		n_Core.OnMidiMsg(event)
	#except:
		#pass

def OnRefresh(flags):
	#try:
		n_Core.OnRefresh(flags)
	#except:
		#pass

def OnUpdateBeatIndicator(Value):
	#try:
		n_Core.OnUpdateBeatIndicator(Value)
	#except:
		#pass
	
def OnWaitingForInput():
	#try:
		n_Core.OnWaitingForInput()
	#except:
		#pass
	
def OnProjectLoad(status):
	#try:
		n_Core.OnProjectLoad(status)
	#except:
		#pass

def OnIdle():
	#try:
		n_Core.OnIdle()
	#except:
		#pass
	
def OnUpdateMeters():
	n_Core.OnUpdateMeters()

def OnDeInit():
	#try:
		if ui.isClosing() == True:
			nihia.goodBye()
		else:
			nihia.goodBye()
	#except:
		#pass


