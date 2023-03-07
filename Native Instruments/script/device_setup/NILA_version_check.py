from script.device_setup import NILA_detect_device
from script.device_setup import constants

from sys import flags, platform
import general 
import ui

VER_Major = ui.getVersion(0) 
VER_Minor = ui.getVersion(1)
VER_Release = ui.getVersion(2)

def VersionCheck(compatibility):
   """Called to check user's FL Studio version to see if this script can run."""

   NILA_Name = ""
   OS = ""
   
   print(constants.OUTPUT_MESSAGE)

   if platform == "darwin":
      OS = "macOS"
   elif platform == "win32":
      OS = "Windows"


   if constants.MIN_Major <= int(VER_Major): 
      if constants.MAX_Major == int(constants.MAX_Major) and int(VER_Minor) >= constants.MAX_Minor and general.getVersion() >= constants.MIDI_Script_Version:
         print(ui.getProgTitle(), ui.getVersion(), "\nis compatible with this script on", OS,"\n")
         compatibility = True
      
      elif constants.MIN_Major == int(constants.MIN_Major) and int(VER_Minor) >= constants.MIN_Minor >= constants.MIDI_Script_Version:
         print(ui.getProgTitle(), ui.getVersion(), "\nis compatible with this script on", OS,"\n")
         compatibility = True

   else:
      print(ui.getProgTitle(), ui.getVersion(), "\nis not compatible with this script on", OS, "\n\nFRUITY NILA " + constants.VERSION_NUMBER + 
      " will not load on this device. \nPlease update", VER_Major, ui.getVersion(), "to", str(constants.MIN_Major) + "." + str(constants.MIN_Minor) + "." + str(constants.MIN_Release),
      "or higher.\n")
      compatibility = False

   seriesDevice = NILA_detect_device.detectDevice(NILA_Name)

   if (seriesDevice == 'Komplete Kontrol Series A' or seriesDevice =='Komplete Kontrol Series M' or seriesDevice =='Komplete Kontrol Series S') == True:
      print("A", seriesDevice, "has been detected. It is compatible with this script\n\n")
   else:
      print("The", seriesDevice, "is not compatible with this script. Only the Komplete Kontrol Series S, Komplete Kontrol Series A and Komplete Kontrol Series M are comptible with FRUITY NILA\n\n")
   return compatibility



