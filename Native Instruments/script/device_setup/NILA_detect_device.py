import device


def detectDevice(NILA_Name):
   """ Gets the MIDI device name from FL Studio and sets `DEVICE_SERIES` to the right value in order for the script to work properly. """
   
   deviceName = device.getName()

   if deviceName == "Komplete Kontrol A DAW":
      NILA_Name = "Komplete Kontrol Series A"

   elif deviceName == "Komplete Kontrol M DAW":
      NILA_Name = "Komplete Kontrol Series M"

   else:
      NILA_Name = device.getName()
 
   return NILA_Name