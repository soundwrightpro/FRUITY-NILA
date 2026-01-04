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


# Cache constants locally to reduce attribute lookups on hot paths
CONTROLS_CHAN = c.controls
DISPLAY_TRACK_INDEX = c.display_track_index
WAIT_INPUT_1 = c.wait_input_1
WAIT_INPUT_2 = c.wait_input_2


class Core:
	"""
	Core class to manage MIDI interactions with FL Studio.
	Handles device initialization, MIDI events, UI updates, and error handling.
	"""

	def __init__(self):
		# Prebind handler tuples so they are looked up only once
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

		# Prebind frequently used functions to avoid repeated module lookups
		self._on_idle_oled = NILA_OLED.OnIdle
		self._send_peak_info = NILA_transform.sendPeakInfo

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
		"""
		chan = event.midiChan
		try:
			if chan == CONTROLS_CHAN:
				handlers = self._control_handlers
				for handler in handlers:
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
		"""
		try:
			handlers = self._refresh_handlers
			for handler in handlers:
				handler(self, flags)
		except Exception as e:
			self.handle_exception("OnRefresh", e)

	def OnUpdateBeatIndicator(self, value):
		"""
		Updates beat indicators for LED and OLED displays.

		Parameters:
			value (int): The current beat indicator value.
		"""
		try:
			handlers = self._beat_handlers
			for handler in handlers:
				handler(self, value)
		except Exception as e:
			self.handle_exception("OnUpdateBeatIndicator", e)

	def OnWaitingForInput(self):
		"""Handles UI feedback while waiting for user input."""
		try:
			setTrackName(DISPLAY_TRACK_INDEX, WAIT_INPUT_1)
			setTrackVol(DISPLAY_TRACK_INDEX, WAIT_INPUT_2)
		except Exception as e:
			self.handle_exception("OnWaitingForInput", e)

	def OnProjectLoad(self, status):
		"""
		Handles project loading events.

		Parameters:
			status (int): Status of the project load event.
		"""
		try:
			NILA_core.OnProjectLoad(self, status)
		except Exception as e:
			self.handle_exception("OnProjectLoad", e)

	def OnIdle(self):
		"""Handles idle state updates for the OLED display."""
		try:
			self._on_idle_oled(self)
		except Exception as e:
			self.handle_exception("OnIdle", e)

	def OnUpdateMeters(self):
		"""Sends peak meter information for real-time visual feedback."""
		try:
			self._send_peak_info()
		except Exception as e:
			self.handle_exception("OnUpdateMeters", e)

	def handle_exception(self, method_name, exception):
		"""
		Handles and logs exceptions, ensuring stability of the NILA.

		Parameters:
			method_name (str): Name of the method where the exception occurred.
			exception (Exception): The exception object.
		"""
		# Keep logging simple and fast to avoid stalling time critical callbacks
		print(f"{method_name} error: {exception} ({type(exception).__name__})")


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
	"""
	try:
		if ui.isClosing():
			NILA_LED.clearAll()
			NILA_OLED.clearAll()
			n_Core.handle_exception("OnDeInit", "Closing UI")
			nihia.goodBye()
	except Exception as e:
		n_Core.handle_exception("OnDeInit", e)