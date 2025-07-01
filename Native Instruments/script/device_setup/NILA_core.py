import nihia
import nihia.mixer as mix
from script.device_setup import constants
import device
import playlist
import time
import ui

def OnInit(self):
	"""
	Initializes the script, performs a handshake, and sets up the environment.
	"""
	nihia.handShake()

	if not seriesCheck():
		mix.setTrackName(0, constants.HELLO_MESSAGE)
		mix.setTrackVol(0, constants.GOODBYE_MESSAGE)
		time.sleep(2)

	device.setHasMeters()

	for button in ("UNDO", "REDO", "TEMPO", "CLEAR", "QUANTIZE"):
		nihia.buttons.setLight(button, 1)

	device.midiOutSysex(constants.HANDSHAKE_SYSEX)

	for x in range(8):
		mix.setTrackExist(x, 0)

def OnWaitingForInput(status):
	"""
	Handles the waiting-for-input state.
	"""
	mix.setTrackName(0, ". . .")
	time.sleep(constants.timedelay)

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
		constants.PL_Start: "Loading File",
		constants.PL_LoadOk: "Load Complete",
		constants.PL_LoadError: "Load Error!"
	}
	if status in messages and not seriesCheck():
		mix.setTrackName(0, constants.HELLO_MESSAGE)
		mix.setTrackVol(0, messages[status])
		time.sleep(constants.timedelay)

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
	mix.setTrackVol(trackID, value)