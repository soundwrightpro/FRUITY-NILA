import nihia
import nihia.mixer as mix
from nihia import buttons
from script.NILA_engine import constants as c
import device
import mixer
import playlist
import time
import ui

def OnInit(self):
	"""
	Initializes the script, performs a handshake, and sets up the environment.
	"""
	nihia.handShake()

	if not seriesCheck():
		mix.setTrackName(0, c.HELLO_MESSAGE)
		mix.setTrackVol(0, c.GOODBYE_MESSAGE)
		time.sleep(2)

	device.setHasMeters()

	for button in ("UNDO", "REDO", "TEMPO", "CLEAR", "QUANTIZE"):
		nihia.buttons.setLight(button, 1)

	device.midiOutSysex(c.HANDSHAKE_SYSEX)

	for x in range(8):
		mix.setTrackExist(x, 0)

def OnWaitingForInput(status):
	"""
	Handles the waiting-for-input state.
	"""
	mix.setTrackName(0, ". . .")
	time.sleep(c.timedelay)

def seriesCheck():
	"""
	Checks if the current device is in the Komplete Kontrol Series.
	"""
	return device.getName() == "Komplete Kontrol DAW - 1"

def OnProjectLoad(self, status):
	"""
	Handles project loading events.
	"""
	messages = {
		c.PL_Start: "Loading File",
		c.PL_LoadOk: "Load Complete",
		c.PL_LoadError: "Load Error!"
	}
	if status in messages and not seriesCheck():
		mix.setTrackName(0, c.HELLO_MESSAGE)
		mix.setTrackVol(0, messages[status])
		time.sleep(c.timedelay)

def timeConvert(timeDisp, currentTime):
	"""
	Converts the time display format based on the FL Studio settings.
	"""
	currentBar = str(playlist.getVisTimeBar())
	currentStep = str(playlist.getVisTimeStep())

	try:
		step_int = int(currentStep)
	except (ValueError, TypeError):
		step_int = -1  # fallback for any weird values

	if 0 <= step_int <= 9:
		currentTime = f"{currentBar}:0{step_int}"
	elif step_int >= 0:
		currentTime = f"{currentBar}:{step_int}"
	else:
		currentTime = str(currentStep)

	if step_int >= 0:
		timeDisp = "Min:Sec" if ui.getTimeDispMin() else "Beats:Bar"
	else:
		timeDisp = "REC in..."

	return timeDisp, currentTime

def setTrackVolConvert(trackID: int, value: str):
	"""
	Converts the track volume display format and sets the track volume.
	"""
	if value == "-inf dB":
		value = "- oo dB"

