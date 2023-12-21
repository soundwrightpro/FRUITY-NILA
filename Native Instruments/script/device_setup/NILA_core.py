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

    This function is called when the script is initialized.
    """
    nihia.handShake()

    if not seriesCheck():
        mix.setTrackName(0, constants.HELLO_MESSAGE)
        mix.setTrackVol(0, constants.GOODBYE_MESSAGE)
        time.sleep(2.00)

    device.setHasMeters()

    for button in ["UNDO", "REDO", "TEMPO", "CLEAR", "QUANTIZE"]:
        nihia.buttons.setLight(button, 1)

    device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 64, 1, 0, 247]))  # 'mute' & 'solo' button lights activated

    for x in range(8):
        mix.setTrackExist(x, 0)

def OnWaitingForInput(status):
    """
    Handles the waiting-for-input state.

    This function is called when the script is waiting for user input.
    """
    mix.setTrackName(0, ". . .")
    time.sleep(constants.timedelay)

def seriesCheck():
    """
    Checks if the current device is in the Komplete Kontrol Series.

    Returns:
        bool: True if the device is in the Komplete Kontrol Series, False otherwise.
    """
    return device.getName() == "Komplete Kontrol DAW - 1"

def OnProjectLoad(self, status):
    """
    Handles project loading events.

    Args:
        status (int): The status of the project loading event.

    This function is called when the project is loaded.
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

    Args:
        timeDisp (str): Current time display format.
        currentTime (str): Current time.

    Returns:
        tuple: A tuple containing the updated time display format and current time.
    """
    currentBar = str(playlist.getVisTimeBar())
    currentStep = str(playlist.getVisTimeStep())
    zeroStr = "0"

    if 0 <= int(currentStep) <= 9:
        currentTime = f"{currentBar}:{zeroStr}{currentStep}"
    elif int(currentStep) >= 0:
        currentTime = f"{currentBar}:{currentStep}"
    elif int(currentStep) < 0:
        currentTime = str(currentStep)

    if ui.getTimeDispMin() and int(currentStep) >= 0:
        timeDisp = "Min:Sec"
    elif not ui.getTimeDispMin() and int(currentStep) >= 0:
        timeDisp = "Beats:Bar"
    elif int(currentStep) <= 0:
        timeDisp = "REC in..."

    return timeDisp, currentTime

def setTrackVolConvert(trackID: int, value: str):
    """
    Converts the track volume display format and sets the track volume.

    Args:
        trackID (int): The ID of the track.
        value (str): The track volume value.

    This function sets the track volume after converting the display format.
    """
    if value == "-inf dB":
        value = "- oo dB"
    mix.setTrackVol(trackID, value)
