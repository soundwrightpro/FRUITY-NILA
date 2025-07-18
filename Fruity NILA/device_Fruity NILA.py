# name=Fruity NILA
# url=https://forum.image-line.com/viewtopic.php?p=1497550#p1497550
# supportedDevices=Komplete Kontrol DAW - 1,Komplete Kontrol A DAW,Komplete Kontrol M DAW,Komplete Kontrol S DAW,Komplete Kontrol S49 MK2,Komplete Kontrol S61 MK2,Komplete Kontrol S88 MK2,KOMPLETE KONTROL S49 MK2 Port 1,KOMPLETE KONTROL S61 MK2 Port 1,KOMPLETE KONTROL S88 MK2 Port 1,KOMPLETE KONTROL - 1,KOMPLETE KONTROL A25,KOMPLETE KONTROL A49,KOMPLETE KONTROL A61,KOMPLETE KONTROL M32,KOMPLETE KONTROL A25 MIDI,KOMPLETE KONTROL A49 MIDI,KOMPLETE KONTROL A61 MIDI,KOMPLETE KONTROL M32 MIDI
# receiveFrom=Forward Device
# supportedHardwareIds=00 33 09 96 24 32, 00 21 09 60 18 20

import nihia
from script.NILA_UI import *
from script.device_setup import *
from script.led_writer import NILA_LED
from script.screen_writer import NILA_OLED
import device
from nihia.mixer import setTrackVol, setTrackName
import ui
import sys
from script.device_setup import constants as c

class Core:
	"""
	Core class to manage MIDI interactions with FL Studio.
	Handles device initialization, MIDI events, UI updates, and error handling.
	"""

	def OnInit(self):
		"""Initializes the script and verifies device compatibility."""
		try:
			if NILA_version_check.VersionCheck(False):
				NILA_core.OnInit(self)
		except Exception as e:
			self.handle_exception("OnInit", e)

	def OnMidiMsg(self, event):
		"""
		Processes incoming MIDI messages and delegates them to the appropriate handler.
		FL Studio will call this function when a MIDI event is received.
		Parameters:
			event (MidiEvent): The incoming MIDI event.
		"""
		try:
			if event.midiChan == c.controls:
				for handler in (
					NILA_navigation.encoder,
					NILA_buttons.OnMidiMsg,
					NILA_mixer.OnMidiMsg,
					NILA_playlist.OnMidiMsg,
					NILA_channel_rack.OnMidiMsg,
					NILA_piano_roll.OnMidiMsg,
					NILA_plugins.plugin,
				):
					handler(self, event)
			else:
				NILA_touch_strips.OnMidiIn(event)
		except Exception as e:
			self.handle_exception("OnMidiMsg", e)

	def OnRefresh(self, flags):
		"""
		Refreshes the LED and OLED displays based on FL Studio's state.
		FL Studio calls this function to update the hardware UI.
		Parameters:
			flags (int): Flags indicating what needs to be refreshed.
		"""
		try:
			# Cache handlers list, avoid redundant tuple creation
			handlers = (NILA_LED.OnRefresh, NILA_OLED.OnRefresh, NILA_navigation.OnRefresh)
			for handler in handlers:
				handler(self, flags)
		except Exception as e:
			self.handle_exception("OnRefresh", e)

	def OnUpdateBeatIndicator(self, value):
		"""
		Updates beat indicators for LED and OLED displays.
		FL Studio calls this function to sync beat indicators with the DAW.
		Parameters:
			value (int): The current beat indicator value.
		"""
		try:
			for handler in (NILA_LED.OnUpdateBeatIndicator, NILA_OLED.OnUpdateBeatIndicator):
				handler(self, value)
		except Exception as e:
			self.handle_exception("OnUpdateBeatIndicator", e)

	def OnWaitingForInput(self):
		"""
		Handles UI feedback while waiting for user input.
		Used by FL Studio to indicate a waiting state.
		"""
		try:
			# Use display_track_index from constants for clarity/consistency
			setTrackName(c.display_track_index, c.wait_input_1)
			setTrackVol(c.display_track_index, c.wait_input_2)
		except Exception as e:
			self.handle_exception("OnWaitingForInput", e)

	def OnProjectLoad(self, status):
		"""
		Handles project loading events.
		Called when an FL Studio project is opened.
		Parameters:
			status (int): Status of the project load event.
		"""
		try:
			NILA_core.OnProjectLoad(self, status)
		except Exception as e:
			self.handle_exception("OnProjectLoad", e)

	def OnIdle(self):
		"""
		Handles idle state updates for the OLED display.
		Ensures UI feedback remains responsive during inactivity.
		"""
		try:
			NILA_OLED.OnIdle(self)
		except Exception as e:
			self.handle_exception("OnIdle", e)

	def OnUpdateMeters(self):
		"""
		Sends peak meter information for real-time visual feedback.
		FL Studio calls this function to update level meters.
		"""
		try:
			NILA_transform.sendPeakInfo()
		except Exception as e:
			self.handle_exception("OnUpdateMeters", e)

	def handle_exception(self, method_name, exception):
		"""
		Handles and logs exceptions, ensuring stability of the script.
		This prevents crashes and provides debugging information.
		Parameters:
			method_name (str): Name of the method where the exception occurred.
			exception (Exception): The exception object.
		"""
		print(f"{method_name} error: {exception}\nException Type: {type(exception).__name__}\n")

# Instantiate Core object
n_Core = Core()

# Entry point functions for FL Studio MIDI scripting engine
def OnInit(): n_Core.OnInit()
def OnMidiMsg(event): n_Core.OnMidiMsg(event)
def OnRefresh(flags): n_Core.OnRefresh(flags)
def OnUpdateBeatIndicator(value): n_Core.OnUpdateBeatIndicator(value)
def OnWaitingForInput(): n_Core.OnWaitingForInput()
def OnProjectLoad(status): n_Core.OnProjectLoad(status)
def OnIdle(): n_Core.OnIdle()
def OnUpdateMeters(): n_Core.OnUpdateMeters()

def OnDeInit():
	"""
	Handles cleanup and UI closure events.
	Ensures a smooth shutdown of the script.
	FL Studio calls this function when closing the script.
	"""
	try:
		if ui.isClosing():
			n_Core.handle_exception("OnDeInit", "Closing UI")
			nihia.goodBye()
	except Exception as e:
		n_Core.handle_exception("OnDeInit", e)
