import device

def detectDevice(NILA_Name):
   """ Gets the MIDI device name from FL Studio and sets `DEVICE_SERIES` to the right value in order for the script to work properly. """
   
   deviceName = device.getName()

   if deviceName == "Komplete Kontrol A DAW":
      NILA_Name = "Komplete Kontrol Series A"
      

   elif deviceName == "Komplete Kontrol M DAW":
      NILA_Name = "Komplete Kontrol Series M"

   elif deviceName == "Komplete Kontrol DAW - 1":
      NILA_Name = "Komplete Kontrol Series S"

   elif deviceName == "KOMPLETE KONTROL M32":
      NILA_Name = "Komplete Kontrol Series M"  

   elif deviceName == "KOMPLETE KONTROL S88 MK2 Port 1":
      NILA_Name = "Komplete Kontrol Series S"   

   elif deviceName == "KOMPLETE KONTROL - 1":
      NILA_Name = "Komplete Kontrol Series S" 
      

   else:
      NILA_Name = device.getName()
 
   return NILA_Name
