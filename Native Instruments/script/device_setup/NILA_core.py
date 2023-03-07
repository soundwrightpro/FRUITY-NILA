import nihia
import nihia.mixer as NILA_mix

from script.NILA_UI import NILA_buttons
from script.device_setup import NILA_detect_device
from script.device_setup import constants

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

   if device.getName() == "Komplete Kontrol DAW - 1":
      pass
   else:
      NILA_mix.setTrackName(0, constants.HELLO_MESSAGE)
      NILA_mix.setTrackVol(0, constants.GOODBYE_MESSAGE)
      time.sleep(2.00)

   nihia.buttons.setLight("UNDO", 1)
   nihia.buttons.setLight("REDO", 1)
   nihia.buttons.setLight("TEMPO", 1)
   nihia.buttons.setLight("CLEAR", 1)
   device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 64, 1, 0, 247])) # 'mute' & 'solo' button lights activated  


   for x in range(8):
      nihia.mixer.setTrackExist(x,0)


def OnWaitingForInput(status):
   NILA_mix.setTrackName(0, ". . .")
   time.sleep(constants.timedelay)
   

def OnProjectLoad(self, status):

   if status == constants.PL_Start:
      if device.getName() == "Komplete Kontrol DAW - 1":
         pass
      else:
         NILA_mix.setTrackName(0, constants.HELLO_MESSAGE)
         NILA_mix.setTrackVol(0, "Loading File")
         time.sleep(constants.timedelay)

   elif status == constants.PL_LoadOk:
      if device.getName() == "Komplete Kontrol DAW - 1":
         pass
      else:
         NILA_mix.setTrackName(0, constants.HELLO_MESSAGE)
         NILA_mix.setTrackVol(0, "Load Complete")
         time.sleep(constants.timedelay)

   elif status == constants.PL_LoadError:
      if device.getName() == "Komplete Kontrol DAW - 1":
         pass
      else:
         NILA_mix.setTrackName(0, constants.HELLO_MESSAGE)
         NILA_mix.setTrackVol(0, "Load Error!")
         time.sleep(constants.timedelay)


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

   NILA_mix.setTrackVol(trackID, value)