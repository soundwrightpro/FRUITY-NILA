import time
import device

import nihia
import nihia.buttons as buttons
import nihia.mixer as mix

from NILA.NILA_engine import constants as c


SERIES_DEVICE_NAME = "Komplete Kontrol DAW - 1"


def _show_startup_message(name_message, volume_message, delay):
	"""Displays a temporary two line startup style message on non series devices."""
	mix.setTrackName(0, name_message)
	mix.setTrackVol(0, volume_message)
	time.sleep(delay)

def OnInit(self):
	"""Initializes the script, performs a handshake, and sets up the environment."""
	nihia.handShake()

	if not seriesCheck():
		_show_startup_message(c.HELLO_MESSAGE, c.GOODBYE_MESSAGE, 2)

	device.setHasMeters()

	for button in ("UNDO", "REDO", "TEMPO", "CLEAR", "QUANTIZE"):
		buttons.setLight(button, 1)

	device.midiOutSysex(c.HANDSHAKE_SYSEX)

	for track_index in range(8):
		mix.setTrackExist(track_index, 0)

def OnWaitingForInput(status):
	"""Handles the waiting for input state."""
	mix.setTrackName(0, ". . .")
	time.sleep(c.ui_time_delay)

def seriesCheck():
	"""Checks if the current device is in the Komplete Kontrol Series."""
	return device.getName() == SERIES_DEVICE_NAME

def OnProjectLoad(self, status):
	"""Handles project loading events."""
	messages = {
		c.PL_Start: "Loading File",
		c.PL_LoadOk: "Load Complete",
		c.PL_LoadError: "Load Error!"
	}
	if status in messages and not seriesCheck():
		_show_startup_message(c.HELLO_MESSAGE, messages[status], c.ui_time_delay)


def setTrackVolConvert(trackID: int, value: str):
	"""Converts the track volume display format and sets the track volume."""
	if value == "-inf dB":
		value = "- oo dB"