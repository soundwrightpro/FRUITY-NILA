import nihia
import nihia.mixer as mix

from script.device_setup import config
from script.device_setup import NILA_detect_device
from script.NILA_UI import NILA_buttons

import device
import midi
import mixer
import general  
import playlist
import time
import transport
import ui


def OnInit(self):
   nihia.handShake()
   mix.setTrackName(0, config.HELLO_MESSAGE)
   mix.setTrackVol(0, config.GOODBYE_MESSAGE)
   time.sleep(2.00)
   nihia.buttons.setLight("UNDO", 1)
   nihia.buttons.setLight("REDO", 1)
   nihia.buttons.setLight("TEMPO", 1)
   nihia.buttons.setLight("CLEAR", 1)
   device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 64, 1, 0, 247])) # 'mute' & 'solo' button lights activated  


def OnWaitingForInput():
   mix.setTrackName(0, ". . .")
   time.sleep(config.timedelay)
   

def OnProjectLoad(self):
   mix.setTrackName(0, config.HELLO_MESSAGE)
   mix.setTrackVol(0, config.LOAD_MESSAGE)
   time.sleep(config.timedelay)


def timeConvert(timeDisp, currentTime):

   currentBar = str(playlist.getVisTimeBar())
   currentStep = str(playlist.getVisTimeStep())
   currentTick = str(playlist.getVisTimeTick())

   zeroStr = str(0)

   if int(currentStep) <= 9 and int(currentStep) >= 0:
      currentTime = str(currentBar+":"+zeroStr+currentStep)
   elif int(currentStep) >= 0:
      currentTime = str(currentBar+":"+currentStep)
   elif int(currentStep) < 0:
      currentTime = str(currentStep)

   if ui.getTimeDispMin() == True and int(currentStep) >= 0:
      timeDisp = "Min:Sec"
   elif ui.getTimeDispMin() == False and int(currentStep) >= 0:
      timeDisp = "Beats:Bar"
   elif int(currentStep) <= 0:
      timeDisp = "REC in..."
   
   return timeDisp, currentTime


def setTrackVolConvert(trackID: int, value: str):
   if value == "-inf dB":
      value = "- oo dB"

   mix.setTrackVol(trackID, value)