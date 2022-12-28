from script.device_setup import config
from script.device_setup import NILA_detect_device

from sys import flags, platform
import ui

VER_Major = ui.getVersion(0) 
VER_Minor = ui.getVersion(1)
VER_Release = ui.getVersion(2)


def VersionCheck(compatibility):
   """Called to check user's FL Studio version to see if this script can run."""

   NILA_Name = ""
   OS = ""
   
   print(config.OUTPUT_MESSAGE)

   if platform == "darwin":
      OS = "macOS"

   elif platform == "win32":
      OS = "Windows"


   if config.MIN_Major <= int(VER_Major): 
      if config.MAX_Major == int(config.MAX_Major) and int(VER_Minor) >= config.MAX_Minor:
         print(ui.getProgTitle(), ui.getVersion(), "\nis compatible with this script on", OS,"\n")
         compatibility = True
      
      elif config.MIN_Major == int(config.MIN_Major) and int(VER_Minor) >= config.MIN_Minor:
         print(ui.getProgTitle(), ui.getVersion(), "\nis compatible with this script on", OS,"\n")
         compatibility = True

   else:
      print(ui.getProgTitle(), ui.getVersion(), "\nis not compatible with this script on", OS, "\n\nFRUITY NILA " + config.VERSION_NUMBER + 
      " will not load on this device. \nPlease update", VER_Major, ui.getVersion(), "to", str(config.MIN_Major) + "." + str(config.MIN_Minor) + "." + str(config.MIN_Release),
      "or higher.\n")
      compatibility = False

   seriesDevice = NILA_detect_device.detectDevice(NILA_Name)

   if seriesDevice ==  "Komplete Kontrol Series A" or "Komplete Kontrol Series M":
      print("A", seriesDevice, "has been detected. It is compatible with this script\n\n")

   else:
      print("The", seriesDevice, "is not compatible with this script. Only the Komplete Kontrol Series A and Komplete Kontrol Series M are comptible with FRUITY NILA\n\n")
   return compatibility