# name=Fruity NILA
# url=https://forum.image-line.com/viewtopic.php?p=1497550#p1497550
# supportedDevices=Komplete Kontrol M DAW, Komplete Kontrol A DAW, KOMPLETE KONTROL M32, Komplete Kontrol DAW 1
# receiveFrom=Forward Device

"""
Fruity NILA is a script designed for FL Studio.

For more information, visit: https://forum.image-line.com/viewtopic.php?p=1497550#p1497550

Compatibility Notes:
- Surface: Komplete Kontrol S-Series mkII, Komplete Kontrol A-Series, and Komplete Kontrol M-Series
- Developer: Duwayne 

- Copyright (c) 2023  
"""

import nihia
from nihia import *
from script.NILA_UI import *
from script.device_setup import *
from script.device_setup import transform
from script.led_writer import NILA_LED
from script.screen_writer import NILA_OLED as oled

from nihia.mixer import setTrackVol
from nihia.mixer import setTrackName

import sys
exc_type, exc_value, exc_traceback = sys.exc_info()

import ui


class Core(): 
    """
    Core class for Fruity NILA script. Handles various events and interactions.
    """
    def OnInit(self):
        """
        Initialization method. Checks compatibility and initializes the core.
        """
        try:
            compatibility = False
            if NILA_version_check.VersionCheck(compatibility):
                NILA_core.OnInit(self)
        except Exception as e:
            print(f"OnInit error: {e}\n")
            print(f"Line number: {exc_traceback.tb_lineno}\n\n")  

            

    def OnMidiMsg(self, event): 
        """
        MIDI message handling method. Routes MIDI events to corresponding functions.
        """
        try:
            if event.midiChan == constants.controls:
                NILA_navigation.encoder(self, event)
                NILA_buttons.OnMidiMsg(event)
                NILA_mixer.OnMidiMsg(self, event)
                NILA_playlist.OnMidiMsg(self, event)
                NILA_channel_rack.OnMidiMsg(self, event)
                NILA_piano_roll.OnMidiMsg(self, event)
                NILA_plugins.plugin(self, event)
            else:
                NILA_touch_strips.OnMidiIn(event)
        except Exception as e:
            print(f"OnMidiMsg error: {e}\n")
            print(f"Line number: {exc_traceback.tb_lineno}\n\n") 

            

    def OnRefresh(self, flags):
        """
        Refresh method for updating UI components.
        """
        try:
            NILA_LED.OnRefresh(self, flags)
            oled.OnRefresh(self, flags)
        except Exception as e:
            print(f"OnRefresh error: {e}\n")
            print(f"Line number: {exc_traceback.tb_lineno}\n\n")       

    def OnUpdateBeatIndicator(self, Value):
        """
        Update method for beat indicator.
        """
        try:
            NILA_LED.OnUpdateBeatIndicator(self, Value)
            oled.OnUpdateBeatIndicator(self, Value)
        except Exception as e:
            print(f"OnUpdateBeatIndicator error: {e}\n")
            print(f"Line number: {exc_traceback.tb_lineno}\n\n")  

    def OnWaitingForInput(self):
        """
        Method for handling waiting input state.
        """
        try:
            setTrackName(0, constants.wait_input_1)
            setTrackVol(0, constants.wait_input_2)
        except Exception as e:
            print(f"OnWaitingForInput error: {e}\n")
            print(f"Line number: {exc_traceback.tb_lineno}\n\n")

    def OnProjectLoad(self, status):
        """
        Method called on project load.
        """
        try:
            NILA_core.OnProjectLoad(self, status)
        except Exception as e:
            print(f"OnProjectLoad error: {e}\n")
            print(f"Line number: {exc_traceback.tb_lineno}\n\n")

    def OnIdle(self):
        """
        Idle method for handling idle state.
        """
        try:
            oled.OnIdle(self)
        except Exception as e:
            print(f"OnIdle error: {e}\n")
            print(f"Line number: {exc_traceback.tb_lineno}\n\n")

    def OnUpdateMeters(self):
        """
        Method for updating volume meters.
        """
        try:
            transform.sendPeakInfo()
        except Exception as e:
            print(f"OnUpdateMeters error: {e}\n")
            print(f"Line number: {exc_traceback.tb_lineno}\n\n")

n_Core = Core()

def OnInit():
    n_Core.OnInit()

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

def OnUpdateMeters():
    n_Core.OnUpdateMeters()

def OnDeInit():
    try:
        if ui.isClosing() == True:
            nihia.goodBye()
        else:
            nihia.goodBye()
    except Exception as e:
        print(f"OnDeInit error: {e}\n")
        print(f"Line number: {exc_traceback.tb_lineno}\n\n")