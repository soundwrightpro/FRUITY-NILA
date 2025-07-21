# name=Fruity NILA
# url=https://forum.image-line.com/viewtopic.php?p=1497550#p1497550
# supportedDevices=Komplete Kontrol DAW - 1,Komplete Kontrol A DAW,Komplete Kontrol M DAW,Komplete Kontrol S DAW,Komplete Kontrol S49 MK2,Komplete Kontrol S61 MK2,Komplete Kontrol S88 MK2,KOMPLETE KONTROL S49 MK2 Port 1,KOMPLETE KONTROL S61 MK2 Port 1,KOMPLETE KONTROL S88 MK2 Port 1,KOMPLETE KONTROL - 1,KOMPLETE KONTROL A25,KOMPLETE KONTROL A49,KOMPLETE KONTROL A61,KOMPLETE KONTROL M32,KOMPLETE KONTROL A25 MIDI,KOMPLETE KONTROL A49 MIDI,KOMPLETE KONTROL A61 MIDI,KOMPLETE KONTROL M32 MIDI,Komplete Kontrol S49 MK3,Komplete Kontrol S61 MK3,Komplete Kontrol S88 MK3,KOMPLETE KONTROL S49 MK3 Port 1,KOMPLETE KONTROL S61 MK3 Port 1,KOMPLETE KONTROL S88 MK3 Port 1
# receiveFrom=Forward Device

import nihia
import device
import ui
from nihia.mixer import setTrackVol, setTrackName

from NILA.NILA_engine import *
from NILA.NILA_engine import constants as c

from NILA.NILA_UI import *
from NILA.NILA_visuals import *


class Core:
	"""
	Core class to manage MIDI interactions with FL Studio.
	Handles device initialization, MIDI events, UI updates, and error handling.
	"""

	def __init__(self):
		self._control_handlers = (
			NILA_navigation.encoder,
			NILA_buttons.OnMidiMsg,
			NILA_mixer.OnMidiMsg,
			NILA_playlist.OnMidiMsg,
			NILA_channel_rack.OnMidiMsg,
			NILA_piano_roll.OnMidiMsg,
			NILA_plugins.plugin,
		)
		self._refresh_handlers = (
			NILA_LED.OnRefresh,
			NILA_OLED.OnRefresh,
			NILA_navigation.OnRefresh,
		)
		self._beat_handlers = (
			NILA_LED.OnUpdateBeatIndicator,
			NILA_OLED.OnUpdateBeatIndicator,
		)

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
		
		Parameters:
			event (MidiEvent): The incoming MIDI event.
		
		Returns:
			None
		"""
		try:
			if event.midiChan == c.controls:
				for handler in self._control_handlers:
					handler(self, event)
			else:
				NILA_touch_strips.OnMidiIn(event)
		except Exception as e:
			self.handle_exception("OnMidiMsg", e)

	def OnRefresh(self, flags):
		"""
		Refreshes the LED and OLED displays based on FL Studio's state.
		
		Parameters:
			flags (int): Flags indicating what needs to be refreshed.
		
		Returns:
			None
		"""
		try:
			for handler in self._refresh_handlers:
				handler(self, flags)
		except Exception as e:
			self.handle_exception("OnRefresh", e)

	def OnUpdateBeatIndicator(self, value):
		"""
		Updates beat indicators for LED and OLED displays.
		
		Parameters:
			value (int): The current beat indicator value.
		
		Returns:
			None
		"""
		try:
			for handler in self._beat_handlers:
				handler(self, value)
		except Exception as e:
			self.handle_exception("OnUpdateBeatIndicator", e)

	def OnWaitingForInput(self):
		"""
		Handles UI feedback while waiting for user input.
		
		Returns:
			None
		"""
		try:
			setTrackName(c.display_track_index, c.wait_input_1)
			setTrackVol(c.display_track_index, c.wait_input_2)
		except Exception as e:
			self.handle_exception("OnWaitingForInput", e)

	def OnProjectLoad(self, status):
		"""
		Handles project loading events.
		
		Parameters:
			status (int): Status of the project load event.
		
		Returns:
			None
		"""
		try:
			NILA_core.OnProjectLoad(self, status)
		except Exception as e:
			self.handle_exception("OnProjectLoad", e)

	def OnIdle(self):
		"""
		Handles idle state updates for the OLED display.
		
		Returns:
			None
		"""
		try:
			NILA_OLED.OnIdle(self)
		except Exception as e:
			self.handle_exception("OnIdle", e)

	def OnUpdateMeters(self):
		"""
		Sends peak meter information for real-time visual feedback.
		
		Returns:
			None
		"""
		try:
			NILA_transform.sendPeakInfo()
		except Exception as e:
			self.handle_exception("OnUpdateMeters", e)

	def handle_exception(self, method_name, exception):
		"""
		Handles and logs exceptions, ensuring stability of the NILA.
		
		Parameters:
			method_name (str): Name of the method where the exception occurred.
			exception (Exception): The exception object.
		
		Returns:
			None
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
	Ensures a smooth shutdown of the NILA.
	
	Returns:
		None
	"""
	try:
		if ui.isClosing():
			NILA_LED.clearAll()
			NILA_OLED.clearAll()
			n_Core.handle_exception("OnDeInit", "Closing UI")
			nihia.goodBye()
	except Exception as e:
		n_Core.handle_exception("OnDeInit", e)