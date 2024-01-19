# name=Fruity NILA
# url=https://forum.image-line.com/viewtopic.php?p=1497550#p1497550
# supportedDevices=Komplete Kontrol M DAW, Komplete Kontrol A DAW, KOMPLETE KONTROL M32, Komplete Kontrol DAW 1
# receiveFrom=Forward Device
# supportedHardwareIds= 00 33 09 96 24 32, 00 21 09 60 18 20
"""
FRUITY NILA is a robust MIDI script tailored to provide comprehensive support for Native Instruments controllers, 
including the M-Series, A-Series, and S-Series within FL STUDIO. Harnessing the Native Instruments Host Integration protocol, 
FRUITY NILA elevates your controller's functionality, simulating a seamless connection like with Ableton or Logic Pro X. 
Crucially, this script operates independently of the Komplete Kontrol App or Plugin, 
ensuring it doesn't disrupt their regular operation..

For more information, visit: https://github.com/soundwrightpro/FRUITY-NILA

Compatibility Notes:
- Surface: Komplete Kontrol S-Series MKII, Komplete Kontrol A-Series, and Komplete Kontrol M-Series

Developer: Duwayne 
Copyright (c) 2023 
"""

import nihia
from script.NILA_UI import *
from script.device_setup import *
from script.led_writer import NILA_LED
from script.screen_writer import NILA_OLED
import device 

from nihia.mixer import setTrackVol, setTrackName

import ui
import sys

exc_type, exc_value, exc_traceback = sys.exc_info()

class Core():
    def OnInit(self):
        try:
            device.getDeviceID()
            compatibility = False
            if NILA_version_check.VersionCheck(compatibility):
                NILA_core.OnInit(self)
        except Exception as e:
            self.handle_exception("OnInit", e)

    def OnMidiMsg(self, event):
        if event.midiChan == constants.controls:
            NILA_navigation.encoder(self, event)
            NILA_buttons.OnMidiMsg(self, event)
            NILA_mixer.OnMidiMsg(self, event)
            NILA_playlist.OnMidiMsg(self, event)
            NILA_channel_rack.OnMidiMsg(self, event)
            NILA_piano_roll.OnMidiMsg(self, event)
            NILA_plugins.plugin(self, event)
        else:
            NILA_touch_strips.OnMidiIn(event)

    def OnRefresh(self, flags):
        try:
            device.getDeviceID()
            NILA_LED.OnRefresh(self, flags)
            NILA_OLED.OnRefresh(self, flags)
        except Exception as e:
            self.handle_exception("OnRefresh", e)

    def OnUpdateBeatIndicator(self, Value):
        try:
            NILA_LED.OnUpdateBeatIndicator(self, Value)
            NILA_OLED.OnUpdateBeatIndicator(self, Value)
        except Exception as e:
            self.handle_exception("OnUpdateBeatIndicator", e)

    def OnWaitingForInput(self):
        try:
            setTrackName(0, constants.wait_input_1)
            setTrackVol(0, constants.wait_input_2)
        except Exception as e:
            self.handle_exception("OnWaitingForInput", e)

    def OnProjectLoad(self, status):
        try:
            NILA_core.OnProjectLoad(self, status)
        except Exception as e:
            self.handle_exception("OnProjectLoad", e)

    def OnIdle(self):
        try:
            device.getDeviceID()
            NILA_OLED.OnIdle(self)
        except Exception as e:
            self.handle_exception("OnIdle", e)

    def OnUpdateMeters(self):
        try:
            NILA_transform.sendPeakInfo()
        except Exception as e:
            self.handle_exception("OnUpdateMeters", e)

    def handle_exception(self, method_name, exception):
        """
        Handles exceptions and prints detailed error information.
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()

        formatted_exception = f"{method_name} error: {exception}"
        formatted_exception += f"\nException Type: {type(exception).__name__}"
        formatted_exception += f"\nException Value: {exception}"
        formatted_exception += f"\nLine number: {getattr(exception, 'tb_lineno', 'N/A')}\n\n"

        print(formatted_exception)

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
        if ui.isClosing():
            n_Core.handle_exception("OnDeInit", "Closing UI")
            nihia.goodBye()
    except Exception as e:
        n_Core.handle_exception("OnDeInit", e)