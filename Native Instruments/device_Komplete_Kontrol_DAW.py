# name=Komplete Kontrol DAW
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-m32/
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-a25-a49-a61/

# GitHub for this script
# url=https://github.com/soundwrightpro/FLNI_KK

# FL Studio Forum
# https://forum.image-line.com/viewtopic.php?f=1994&t=225473
# script by Duwayne "Sound" Wright additional code from Hobyst (absolute legend)
# find me on the forums as 'soundwrightpro'

# Join the FL Studio NI on Discord if you need help or just want to say hi.
# https://discord.gg/7FYrJEq

# MIT License
# Copyright © 2020 Duwayne Wright

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# This import section is loading the back-end code required to execute the script. 
# The following are the custom FL Studio modules not found outside FL Studio's Python enviorment. 

import channels # This module allows you to control FL Studio Channels

import mixer # This module allows you to control FL Studio Mixer. NOTE: Track number 0 is always the Master.

import device # This module will handle MIDI devices connected to the FL Studio MIDI interface. 
              # You send messages to output interface, retrieve linked control values... etc). 
              # MIDI scripts, assigned to an input interface, can be mapped (linked) to an Output interface via the Port Number. 
              # With mapped (linked) output interfaces, scripts can send midi messages to output interfaces by using one of the midiOut*** messages.

import transport # This module handles FL Studio Transport (Play, Stop, Pause & Record)

import general # This module handles general FL Studio functions

import playlist # This module allows you to control FL Studio Playlist

import ui # This module allows you to control FL Studio User interface (eg. scrolling, moving around, zoom)

import arrangement as arrange # This module allows you to control FL Studio Playlist Arrangements. I've changed it to arrange because I didn't want to 
                              # write out arrangement every time.

import plugins # this module allows for the use of plugis to be control

# The following are the standard Python modules found outside FL Studio's Python enviorment. 

import midi # This module allows for simple sending and receiving of MIDI messages from your device

import utils # Thie module is a collection of small Python functions and classes which make common patterns shorter and easier

import time # This module provides various time-related functions

import sys # This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.

import binascii # This module contains a number of methods to convert between binary and various ASCII-encoded binary representations.

import math #  This module provides access to the mathematical functions.

from sys import platform # This module allows access to the OS version being used. 
                          # As for why it's 'from sys import platform' see https://stackoverflow.com/questions/9439480/from-import-vs-import


# The following is a custom Python modules made for use in FL Studio. Written by Hobyst, modified by Duwayne Wright

import nihia # this module loads the abstraction layer of the Native Instruments' Host Integration Agent API for the FL Studio MIDI Scripting API.
             # more info on this found here: https://github.com/hobyst/flmidi-nihia

if sys.platform == "win32":
    import _thread

if sys.platform == "darwin":
    import lib._dummy_thread as _thread



# For data2, up down right left values for knobs and 4d controller
down = right = 1
up = left = 127

#knob increment value; change this if you want a different feel to the knobs. nothing higher than 1.00
knobinc = 0.01

#on/off values
on = 1
off = 0

winSwitch = 0
jogMove = True

#time delay for messages on screen
timedelay = 0.45 #seconds

#This is a 'utility' track that receives the currently selected Mixer Tracks Output. Settings for this track are hard to see, so the mixer skips over it.
currentUtility = 126



VERSION_NUMBER = "v8.0.5"

VER_Major = ui.getVersion(0) 
VER_Minor = ui.getVersion(1)
VER_Release = ui.getVersion(2)

MIN_Major = 20
MIN_Minor = 9
MIN_Release = 0

HELLO_MESSAGE = "KK " + VERSION_NUMBER 
GOODBYE_MESSAGE = "Ending KK"
OUTPUT_MESSAGE = "\nKomplete Kontrol Script " + VERSION_NUMBER + "\nCopyright © 2021 Duwayne Wright\n"



class KeyKompleteKontrolBase(): #used a class to sheild against crashes
     
     def OnInit(self):
      """ Called when the script has been started.""" 

      #initializing NI Host Integration Agent API for FL Studio by Hobyst
      nihia.initiate() 
      nihia.printText(0, HELLO_MESSAGE)
      time.sleep(timedelay)

     def OnMidiMsg(self, event): #listens for button or knob activity
         """Called first when a MIDI message is received. Set the event's handled property to True if you don't want further processing.
         (only raw data is included here: handled, timestamp, status, data1, data2, port, sysex, pmeflags)"""
         global winSwitch
         global jogMove

         #buttons
         if (event.data1 == nihia.buttons["PLAY"]):
            event.handled = True
            if ui.isInPopupMenu() == True:
               print("Working")
            else:
               transport.start() #play
               self.UpdateLEDs()
               ui.setHintMsg("Play/Pause")

         if (event.data1 == nihia.buttons["RESTART"]):
            event.handled = True
            transport.stop() #stop
            transport.start() #restart play at beginning
            ui.setHintMsg("Restart")
             
         if (event.data1 == nihia.buttons["REC"]):
            event.handled = True
            transport.record() #record
            self.UpdateLEDs()
            ui.setHintMsg("Record")

         if (event.data1 == nihia.buttons["STOP"]):
            event.handled = True
            transport.stop() #stop
            self.UpdateLEDs()
            ui.setHintMsg("Stop")

         if (event.data1 == nihia.buttons["LOOP"]):
            event.handled = True
            transport.setLoopMode() #loop/pattern mode
            self.UpdateLEDs()
            ui.setHintMsg("Song / pattern mode")

            if transport.getLoopMode() == off:
               nihia.printText(0, "Pat. Mode")
               time.sleep(timedelay)

            elif transport.getLoopMode() == on:
               nihia.printText(0, "Song Mode")
               time.sleep(timedelay)
            
         if (event.data1 == nihia.buttons["METRO"]): # metronome/button
            event.handled = True
            transport.globalTransport(midi.FPT_Metronome, 110)
            self.UpdateLEDs()
            ui.setHintMsg("Metronome")

            if ui.isMetronomeEnabled() == off: 
              nihia.printText(0, "Metro Off")
              time.sleep(timedelay)

            elif ui.isMetronomeEnabled() == on: 
              nihia.printText(0, "Metro On")
              time.sleep(timedelay)
            
         if (event.data1 == nihia.buttons["TEMPO"]):
            event.handled = True
            transport.stop() #tap tempo

            #BPMv = str(round(mixer.getCurrentTempo()*0.001))+ " BPM"
            #nihia.printText(0, BPMv)

         if (event.data1 == nihia.buttons["QUANTIZE"]):
            event.handled = True
            self.UpdateLEDs()
            channels.quickQuantize(channels.channelNumber(),0)
            ui.setHintMsg("Quick Quantize")

         if (event.data1 == nihia.buttons["AUTO"]):
            event.handled = True
            ui.snapMode(1) #snap toggle
            self.UpdateLEDs()
            
            snapmodevalue = ["Snap: Line", "Snap: Cell", "Snap: None", 
            "S: 1/6 Step", "S: 1/4 Step", "S: 1/3 Step", "S: 1/2 Step", 
            "Snap: Step", "S: 1/6 Beat", "S: 1/4 Beat", "S: 1/3 Beat", 
            "S: 1/2 Beat", "Snap: Beat", "Snap: Bar"]

            if ui.getSnapMode() == 0: # Line
              ui.setHintMsg("Snap: Line")
              nihia.printText(0, snapmodevalue[0])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 1: # Cell
              ui.setHintMsg("Snap: Cell") 
              nihia.printText(0, snapmodevalue[1])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 3: # (none)
              ui.setHintMsg("Snap: (none)")
              nihia.printText(0, snapmodevalue[2])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 4: # 1/6 step
              ui.setHintMsg("Snap: 1/6 step")
              nihia.printText(0, snapmodevalue[3])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 5: # 1/4 step
              ui.setHintMsg("Snap: 1/4 step")
              nihia.printText(0, snapmodevalue[4])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 6: # 1/3 step
              ui.setHintMsg("Snap: 1/3 step")
              nihia.printText(0, snapmodevalue[5])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 7: # 1/2 step
              ui.setHintMsg("Snap: 1/2 step")
              nihia.printText(0, snapmodevalue[6])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 8: # step
              ui.setHintMsg("Snap: Step")
              nihia.printText(0, snapmodevalue[7])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 9: # 1/6 beat
              ui.setHintMsg("Snap: 1/6 beat")
              nihia.printText(0, snapmodevalue[8])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 10: # 1/4 beat
              ui.setHintMsg("Snap: 1/4 beat")
              nihia.printText(0, snapmodevalue[9])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 11: # 1/3 beat
              ui.setHintMsg("Snap: 1/3 beat")
              nihia.printText(0, snapmodevalue[10])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 12: # 1/2 beat
              ui.setHintMsg("Snap: 1/2 beat")
              nihia.printText(0, snapmodevalue[11])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 13: # beat
              ui.setHintMsg("Snap: Beat")
              nihia.printText(0, snapmodevalue[12])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 14: # bar
              ui.setHintMsg("Snap: Bar")
              nihia.printText(0, snapmodevalue[13])
              time.sleep(timedelay)


         if (event.data1 == nihia.buttons["COUNT_IN"]):
            event.handled = True
            transport.globalTransport(midi.FPT_CountDown, 115) #countdown before recording
            ui.setHintMsg("Countdown before recording")
            self.UpdateLEDs()
            
            if ui.isPrecountEnabled() == 1: 
               nihia.printText(0, "Cnt-in On")
               time.sleep(timedelay)  
            else:
               nihia.printText(0, "Cnt-in Off")
               time.sleep(timedelay)

         if (event.data1 == nihia.buttons["CLEAR"]):
            event.handled = True

            doubleclickstatus = device.isDoubleClick(nihia.buttons["CLEAR"])

            if doubleclickstatus == True:
               transport.globalTransport(midi.FPT_F12, 2, 15)
               ui.setHintMsg("Clear All Windows")
               nihia.printText(0, "Clear All")
               time.sleep(timedelay)
            else:
               ui.escape() #escape key
               ui.setHintMsg("esc")
   

         if (event.data1 == nihia.buttons["UNDO"]):
            event.handled = True
            general.undoUp() #undo 
            ui.setHintMsg(ui.getHintMsg())

         if (event.data1 == nihia.buttons["REDO"]):
            event.handled = True
            general.undo() #redo
            ui.setHintMsg(ui.getHintMsg())

         if (event.data1 == nihia.buttons["TEMPO"]):
            event.handled = True
            transport.globalTransport(midi.FPT_TapTempo, 106) #tap tempo

         if (event.data1 == nihia.buttons["SHIFT+ENCODER_BUTTON"]):
            event.handled = True
            
            doubleclickstatus = device.isDoubleClick(nihia.buttons["SHIFT+ENCODER_BUTTON"])

            if doubleclickstatus == True:
               transport.globalTransport(midi.FPT_F8, 67)
               ui.setHintMsg("Plugin Picker")
               nihia.printText(0, "Plugin Picker")
               #time.sleep(timedelay)
            else:

               if winSwitch == 0:
                  ui.showWindow(1)
                  winSwitch += 1
                  ui.setHintMsg("Switch to Channel Rack") # channel ra

               elif winSwitch == 1:
                  ui.showWindow(0)
                  winSwitch += 1
                  ui.setHintMsg("Switch to Mixer")

               elif winSwitch == 2:
                  ui.showWindow(2)
                  winSwitch += 1
                  ui.setHintMsg("Switch to Playlist")

               elif winSwitch == 3:
                  ui.showWindow(4)
                  ui.setHintMsg("Switch to Browser")
                  if ui.getVisible(3) == True:
                     winSwitch += 1
                  else:
                     winSwitch = 0

               elif winSwitch == 4:
                     ui.showWindow(3)
                     ui.setHintMsg("Switch to Piano Roll")
                     winSwitch = 0
                     
                     
         #mute and solo for mixer and channel rack
         if (event.data1 == nihia.buttons["MUTE_SELECTED"]):
            if ui.getFocused(0) == 1: #mixer volume control
               event.handled = True
               if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= currentUtility:
                  pass
               else:
                  mixer.enableTrack(mixer.trackNumber()) #mute 
                  self.UpdateOLED()
                  ui.setHintMsg("Mute")
               
            elif ui.getFocused(1) == 1: # channel rack
               if channels.channelCount() >= 1: 
                  event.handled = True
                  if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= currentUtility:
                     pass
                  else:
                     channels.muteChannel(channels.channelNumber()) 
                     self.UpdateOLED()
                     ui.setHintMsg("Mute")
                  
         if (event.data1 ==  nihia.buttons["SOLO_SELECTED"]): 
            if ui.getFocused(0) == 1: #mixer volume control
               event.handled = True
               if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= currentUtility:
                  pass
               else:
                  mixer.soloTrack(mixer.trackNumber()) #solo
                  self.UpdateOLED()
                  ui.setHintMsg("Solo")

            elif ui.getFocused(1) == 1: # channel rack
               if channels.channelCount() >= 2: 
                  event.handled = True
                  if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= currentUtility:
                     pass
                  else:
                     channels.soloChannel(channels.channelNumber()) 
                     self.UpdateOLED()
                     ui.setHintMsg("Solo")
                  

         #8 volume knobs for mixer & channel rack, 8 tracks at a time

         if ui.getFocused(0) == 1: #mixer control



            # VOLUME CONTROL

            xy = 1.25
                           

            #knob 0
            if mixer.trackNumber() <= currentUtility:
               if (event.data1 == nihia.knobs["KNOB_0A"]):
                event.handled = True

                if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= currentUtility:
                  pass
                else:
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                     mixer.setTrackVolume((mixer.trackNumber() + 0), (x - knobinc) ) # volume values go down
                     nihia.printVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),3)))
                  
                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                     mixer.setTrackVolume((mixer.trackNumber() + 0), (x + knobinc) ) # volume values go up
                     nihia.printVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),3)))

            #knob 1
            if mixer.trackNumber() <= 125:
               if (event.data1 == nihia.knobs["KNOB_1A"]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+1) == "Current" and mixer.trackNumber()+1 >= currentUtility:
                  pass
                else:
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                     mixer.setTrackVolume((mixer.trackNumber() + 1), (x - knobinc) ) # volume values go down
                     nihia.printVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))
                  
                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                     mixer.setTrackVolume((mixer.trackNumber() + 1), (x + knobinc) ) # volume values go up
                     nihia.printVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))

            elif mixer.trackNumber()+1 >= 125: 
               nihia.printText(1, nihia.message["EMPTY"])
               nihia.printVol(1, 104) 

            #knob 2
            if mixer.trackNumber() <= 124:
               if (event.data1 == nihia.knobs["KNOB_2A"]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+2) == "Current" and mixer.trackNumber()+2 >= currentUtility:
                  pass
                else:
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 2))
                     mixer.setTrackVolume((mixer.trackNumber() + 2), (x - knobinc) ) # volume values go down
                     nihia.printVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))
                  
                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 2))
                     mixer.setTrackVolume((mixer.trackNumber() + 2), (x + knobinc) ) # volume values go up
                     nihia.printVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))

            elif mixer.trackNumber()+2 >= 125:    
               nihia.printText(2, nihia.message["EMPTY"])
               nihia.printVol(2, 104)
               
            #knob 3
            if mixer.trackNumber() <= 123:
               if (event.data1 == nihia.knobs["KNOB_3A"]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+3) == "Current" and mixer.trackNumber()+3 >= currentUtility:
                  pass
                else:
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 3))
                     mixer.setTrackVolume((mixer.trackNumber() + 3), (x - knobinc) ) # volume values go down
                     nihia.printVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))
                  
                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 3))
                     mixer.setTrackVolume((mixer.trackNumber() + 3), (x + knobinc) ) # volume values go up
                     nihia.printVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))

            elif mixer.trackNumber()+3 >= 125:    
               nihia.printText(3, nihia.message["EMPTY"])
               nihia.printVol(3, 104)

            #knob 4
            if mixer.trackNumber() <= 122:
               if (event.data1 == nihia.knobs["KNOB_4A"]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+4) == "Current" and mixer.trackNumber()+4 >= currentUtility:
                  pass
                else:
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 4))
                     mixer.setTrackVolume((mixer.trackNumber() + 4), (x - knobinc) ) # volume values go down
                     nihia.printVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))
                  
                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 4))
                     mixer.setTrackVolume((mixer.trackNumber() + 4), (x + knobinc) ) # volume values go up
                     nihia.printVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))


            elif mixer.trackNumber()+4 >= 125:    
               nihia.printText(4, nihia.message["EMPTY"])
               nihia.printVol(4, 104)

            #knob 5
            if mixer.trackNumber() <= 121:
               if (event.data1 == nihia.knobs["KNOB_5A"]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+5) == "Current" and mixer.trackNumber()+5 >= currentUtility:
                  pass
                else:
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 5))
                     mixer.setTrackVolume((mixer.trackNumber() + 5), (x - knobinc) ) # volume values go down
                     nihia.printVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))

                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 5))
                     mixer.setTrackVolume((mixer.trackNumber() + 5), (x + knobinc) ) # volume values go up
                     nihia.printVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))

            elif mixer.trackNumber()+5 >= 125:    
               nihia.printText(5, nihia.message["EMPTY"])
               nihia.printVol(5, 104)     

            #knob 6
            if mixer.trackNumber() <= 120:
               if (event.data1 == nihia.knobs["KNOB_6A"]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+6) == "Current" and mixer.trackNumber()+6 >= currentUtility:
                  pass
                else:
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 6))
                     mixer.setTrackVolume((mixer.trackNumber() + 6), (x - knobinc) ) # volume values go down
                     nihia.printVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))

                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 6))
                     mixer.setTrackVolume((mixer.trackNumber() + 6), (x + knobinc) ) # volume values go up
                     nihia.printVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))


            elif mixer.trackNumber()+6 >= 125:    
               nihia.printText(6, nihia.message["EMPTY"])
               nihia.printVol(6, 104)     
                          
            #knob 7
            if mixer.trackNumber() <= 119:
               if (event.data1 == nihia.knobs["KNOB_7A"]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+7) == "Current" and mixer.trackNumber()+7 >= currentUtility:
                  pass
                else:
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 7))
                     mixer.setTrackVolume((mixer.trackNumber() + 7), (x - knobinc) ) # volume values go down
                     nihia.printVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))

                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (mixer.getTrackVolume(mixer.trackNumber() + 7))
                     mixer.setTrackVolume((mixer.trackNumber() + 7), (x + knobinc) ) # volume values go up
                     nihia.printVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))


            elif mixer.trackNumber()+7 >= 125:    
               nihia.printText(7, nihia.message["EMPTY"])
               nihia.printVol(7, 104)      

            # MIXER PAN CONTROL 

            #sknob 0
            if mixer.trackNumber() <= currentUtility:
               if (event.data1 == nihia.knobs["KNOB_0B"]):
                  event.handled = True

                  if mixer.trackNumber()+0 >= 125:    
                     nihia.printPan(0, 104)
                  else:
                     if event.data2 == nihia.knobs["DECREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                        mixer.setTrackPan((mixer.trackNumber() + 0), (x - knobinc) ) # volume values go down
                        nihia.printPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)

                     elif event.data2 == nihia.knobs["INCREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                        mixer.setTrackPan((mixer.trackNumber() + 0), (x + knobinc) ) # volume values go up
                        nihia.printPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)


            elif mixer.trackNumber() >= currentUtility:    
               nihia.printVol(0, 104)

            #sknob 1
            if mixer.trackNumber() <= 125:
               if (event.data1 == nihia.knobs["KNOB_1B"]):
                  event.handled = True

                  if mixer.trackNumber()+1 >= currentUtility:    
                     nihia.printPan(1, 104)
                  else:
                     if event.data2 == nihia.knobs["DECREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 1))
                        mixer.setTrackPan((mixer.trackNumber() + 1), (x - knobinc) ) # volume values go down
                        nihia.printPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)

                     elif event.data2 == nihia.knobs["INCREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 1))
                        mixer.setTrackPan((mixer.trackNumber() + 1), (x + knobinc) ) # volume values go up
                        nihia.printPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)
               
            elif mixer.trackNumber()+1 >= currentUtility:    
               nihia.printVol(1, 104)


            #sknob 2
            if mixer.trackNumber() <= 124:
               if (event.data1 == nihia.knobs["KNOB_2B"]):
                  event.handled = True

                  if mixer.trackNumber()+2 >= currentUtility:    
                     nihia.printPan(2, 104)
                  else:
                     if event.data2 == nihia.knobs["DECREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                        mixer.setTrackPan((mixer.trackNumber() + 2), (x - knobinc) ) # volume values go down
                        nihia.printPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)
                  
                     elif event.data2 == nihia.knobs["INCREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                        mixer.setTrackPan((mixer.trackNumber() + 2), (x + knobinc) ) # volume values go up
                        nihia.printPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)

            elif mixer.trackNumber()+2 >= currentUtility:    
               nihia.printVol(2, 104)

            #sknob 3
            if mixer.trackNumber() <= 123:
               if (event.data1 == nihia.knobs["KNOB_3B"]):
                  event.handled = True

                  if mixer.trackNumber()+3 >= currentUtility:    
                     nihia.printPan(3, 104)
                  else:
                     if event.data2 == nihia.knobs["DECREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                        mixer.setTrackPan((mixer.trackNumber() + 3), (x - knobinc) ) # volume values go down
                        nihia.printPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)
                  
                     elif event.data2 == nihia.knobs["INCREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                        mixer.setTrackPan((mixer.trackNumber() + 3), (x + knobinc) ) # volume values go up
                        nihia.printPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)

            elif mixer.trackNumber()+3 >= currentUtility:    
               nihia.printVol(3, 104)

            #sknob 4
            if mixer.trackNumber() <= 122:
               if (event.data1 == nihia.knobs["KNOB_4B"]):
                  event.handled = True

                  if mixer.trackNumber()+4 >= currentUtility:    
                     nihia.printPan(4, 104)
                  else:
                     if event.data2 == nihia.knobs["DECREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                        mixer.setTrackPan((mixer.trackNumber() + 4), (x - knobinc) ) # volume values go down
                        nihia.printPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)
                  
                     elif event.data2 == nihia.knobs["INCREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                        mixer.setTrackPan((mixer.trackNumber() + 4), (x + knobinc) ) # volume values go up
                        nihia.printPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)

            elif mixer.trackNumber()+4 >= currentUtility:    
               nihia.printVol(4, 104)

            #sknob 5
            if mixer.trackNumber() <= 121:
               if (event.data1 == nihia.knobs["KNOB_5B"]):
                  event.handled = True

                  if mixer.trackNumber()+5 >= currentUtility:    
                     nihia.printPan(5, 104)
                  else:
                     if event.data2 == nihia.knobs["DECREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                        mixer.setTrackPan((mixer.trackNumber() + 5), (x - knobinc) ) # volume values go down
                        nihia.printPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)
                  
                     elif event.data2 == nihia.knobs["INCREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                        mixer.setTrackPan((mixer.trackNumber() + 5), (x + knobinc) ) # volume values go up
                        nihia.printPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)

            elif mixer.trackNumber()+5 >= currentUtility:    
               nihia.printVol(5, 104)

            #sknob 6
            if mixer.trackNumber() <= 120:
               if (event.data1 == nihia.knobs["KNOB_6B"]):
                  event.handled = True

                  if mixer.trackNumber()+6 >= currentUtility:    
                     nihia.printPan(6, 104)
                  else:
                     if event.data2 == nihia.knobs["DECREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                        mixer.setTrackPan((mixer.trackNumber() + 6), (x - knobinc) ) # volume values go down
                        nihia.printPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)
                  
                     elif event.data2 == nihia.knobs["INCREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                        mixer.setTrackPan((mixer.trackNumber() + 6), (x + knobinc) ) # volume values go up
                        nihia.printPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)

            elif mixer.trackNumber()+6 >= currentUtility:    
               nihia.printVol(6, 104)

            #sknob 7
            if mixer.trackNumber() <= 119:
               if (event.data1 == nihia.knobs["KNOB_7B"]):
                  event.handled = True

                  if mixer.trackNumber()+7 >= currentUtility:    
                     nihia.printPan(7, 104)
                     
                  else:
                     if event.data2 == nihia.knobs["DECREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 7))
                        mixer.setTrackPan((mixer.trackNumber() + 7), (x - knobinc) ) # volume values go down
                        nihia.printPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)
                  
                     elif event.data2 == nihia.knobs["INCREASE"]:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 7))
                        mixer.setTrackPan((mixer.trackNumber() + 7), (x + knobinc) ) # volume values go up
                        nihia.printPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)



            #4D controller # for mixer
      
            if (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == right): #4d encoder spin right 
               event.handled = True
               ui.jog(1)
               if ui.isInPopupMenu() == True:
                  pass
               else:
                  jogMove = True

            elif (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == left): #4d encoder spin left 
               event.handled = True
               ui.jog(-1)
               if ui.isInPopupMenu() == True:
                  pass
               else:
                  jogMove = True
         
            if (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == right): #4d encoder push right
               event.handled = True
               if ui.isInPopupMenu() == True:
                  ui.right(1)
                  pass
               else:
                  ui.jog(8)
                  jogMove = True

            elif (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == left): #4d encoder push left
               event.handled = True
               if ui.isInPopupMenu() == True:
                  ui.left(1)
                  pass
               else:
                  ui.jog(-8)
                  jogMove = True

            if (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == up): #4d encoder push up
               event.handled = True
               if ui.isInPopupMenu() == True:
                  ui.up(1)
               else:
                  pass
            
            elif (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == down): #4d encoder push down
               event.handled = True
               if ui.isInPopupMenu() == True:
                  ui.down(1)
               else:
                  pass

            if (event.data1 == nihia.buttons["ENCODER_BUTTON"]):
               event.handled = True
               doubleclickstatus = device.isDoubleClick(nihia.buttons["ENCODER_BUTTON"])
               if doubleclickstatus == True:
                  if ui.isInPopupMenu() == True:
                     ui.enter()
                     ui.setHintMsg("Enter")
                  else:  
                     transport.globalTransport(midi.FPT_Menu, 90)
                     ui.setHintMsg("Open Menu")
                     mixer.deselectAll()
                     mixer.selectTrack(mixer.trackNumber())
               else:
                     if ui.isInPopupMenu() == True:
                        ui.enter()
                        ui.setHintMsg("Enter") 
                        
            if jogMove == True:# mixer highlighting when jog wheel is moved
               ui.miDisplayRect(mixer.trackNumber()+0,mixer.trackNumber()+7,1000)

         elif ui.getFocused(5) == True: # Plugin

            # VOLUME CONTROL

            #knob 1
            if channels.getChannelName(channels.selectedChannel()) in ui.getFocusedFormCaption():
               if (event.data1 == nihia.knobs["KNOB_0A"]):
                  event.handled = True  
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                     y = round(x,2)
                     if channels.getChannelVolume(channels.selectedChannel() + 0) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + 0), (y - knobinc) ) # volume values go down
                        nihia.printVol(0, (round(channels.getChannelVolume(channels.selectedChannel() + 0) ,2)))
            
                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                     y = round(x,2)
                     channels.setChannelVolume((channels.selectedChannel() + 0), (y + knobinc) ) # volume values go up
                     nihia.printVol(0, (round(channels.getChannelVolume(channels.selectedChannel() + 0) ,2)))

            # PAN CONTROL

            #sknob 1
            if channels.getChannelName(channels.selectedChannel()) in ui.getFocusedFormCaption():
               if (event.data1 == nihia.knobs["KNOB_0B"]):
                  event.handled = True  
                  if event.data2 == nihia.knobs["DECREASE"]:
                     x = (channels.getChannelPan(channels.selectedChannel() + 0))
                     channels.setChannelPan((channels.selectedChannel() + 0), (x - knobinc) ) # pan values go down
                     nihia.printPan(0, channels.getChannelPan(channels.selectedChannel() + 0) * 100)
   
                  elif event.data2 == nihia.knobs["INCREASE"]:
                     x = (channels.getChannelPan(channels.selectedChannel() + 0))
                     channels.setChannelPan((channels.selectedChannel() + 0), (x + knobinc) ) # pan values go up
                     nihia.printPan(0, channels.getChannelPan(channels.selectedChannel() + 0) * 100)

            if (event.data1 == nihia.knobs["KNOB_1B"] or nihia.knobs["KNOB_2B"] or nihia.knobs["KNOB_3B"] 
            or nihia.knobs["KNOB_4B"] or nihia.knobs["KNOB_5B"] or nihia.knobs["KNOB_6B"] or nihia.knobs["KNOB_7B"] 
            or nihia.knobs["KNOB_1A"] or nihia.knobs["KNOB_2A"] or nihia.knobs["KNOB_3A"] or nihia.knobs["KNOB_4A"] 
            or nihia.knobs["KNOB_5A"] or nihia.knobs["KNOB_6A"] or nihia.knobs["KNOB_7A"] ):
               event.handled = True  

            if (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == right): #4d encoder spin right 
               event.handled = True
               ui.down(1)
               

            elif (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == left): #4d encoder spin left 
               event.handled = True
               ui.up(1)
               
         
            if (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == right): #4d encoder push right
               event.handled = True
               ui.right(1)
               

            elif (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == left): #4d encoder push left
               event.handled = True
               ui.left(1)

            if (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == up): #4d encoder push up
               event.handled = True
               #ui.up()
               plugins.prevPreset(channels.channelNumber(channels.selectedChannel()))
            
            elif (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == down): #4d encoder push down
               event.handled = True
               #ui.down(1)
               plugins.nextPreset(channels.channelNumber(channels.selectedChannel()))

            if (event.data1 == nihia.buttons["ENCODER_BUTTON"]):
               event.handled = True

            if (event.data1 == nihia.buttons["ENCODER_BUTTON"]):
               event.handled = True
               doubleclickstatus = device.isDoubleClick(nihia.buttons["ENCODER_BUTTON"])
               if doubleclickstatus == True:
                  ui.enter()
                  ui.setHintMsg("enter")
               else:
                  pass


         elif ui.getFocused(1) == 1: # channel rack

            # VOLUME CONTROL

            #knob 1
            if (event.data1 == nihia.knobs["KNOB_0A"]):
             event.handled = True  
             if event.data2 == nihia.knobs["DECREASE"]:
                x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                y = round(x,2)
                if channels.getChannelVolume(channels.selectedChannel() + 0) != 0 :
                  channels.setChannelVolume((channels.selectedChannel() + 0), (y - knobinc) ) # volume values go down
                  nihia.printVol(0, (round(channels.getChannelVolume(channels.selectedChannel() + 0) ,2)))
       
             elif event.data2 == nihia.knobs["INCREASE"]:
                x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                y = round(x,2)
                channels.setChannelVolume((channels.selectedChannel() + 0), (y + knobinc) ) # volume values go up
                nihia.printVol(0, (round(channels.getChannelVolume(channels.selectedChannel() + 0) ,2)))

   
            #knob 2
            if (event.data1 == nihia.knobs["KNOB_1A"]):
             event.handled = True  
             if channels.channelCount() > 1 and channels.selectedChannel() < (channels.channelCount()-1) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 1))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.selectedChannel() + 1) != 0 :
                     channels.setChannelVolume((channels.selectedChannel() + 1), (y - knobinc) ) # volume values go down
                     nihia.printVol(1, (round(channels.getChannelVolume(channels.selectedChannel() + 1) ,2)))
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 1))
                  y = round(x,2)
                  channels.setChannelVolume((channels.selectedChannel() + 1), (y + knobinc) ) # volume values go up
                  nihia.printVol(1, (round(channels.getChannelVolume(channels.selectedChannel() + 1) ,2)))

            #knob 3
            if (event.data1 == nihia.knobs["KNOB_2A"]):
             event.handled = True  
             if channels.channelCount() > 2 and channels.selectedChannel() < (channels.channelCount()-2) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 2))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.selectedChannel() + 2) != 0 :
                     channels.setChannelVolume((channels.selectedChannel() + 2), (y - knobinc) ) # volume values go down
                     nihia.printVol(2, (round(channels.getChannelVolume(channels.selectedChannel() + 2) ,2)))
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 2))
                  y = round(x,2)
                  channels.setChannelVolume((channels.selectedChannel() + 2), (y + knobinc) ) # volume values go up
                  nihia.printVol(2, (round(channels.getChannelVolume(channels.selectedChannel() + 2) ,2)))

            #knob 4
            if (event.data1 == nihia.knobs["KNOB_3A"]):
             event.handled = True  
             if channels.channelCount() > 3 and channels.selectedChannel() < (channels.channelCount()-3) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 3))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.selectedChannel() + 3) != 0 :
                     channels.setChannelVolume((channels.selectedChannel() + 3), (y - knobinc) ) # volume values go down
                     nihia.printVol(3, (round(channels.getChannelVolume(channels.selectedChannel() + 3) ,2)))
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 3))
                  y = round(x,2)
                  channels.setChannelVolume((channels.selectedChannel() + 3), (y + knobinc) ) # volume values go up
                  nihia.printVol(3, (round(channels.getChannelVolume(channels.selectedChannel() + 3) ,2)))

            #knob 5
            if (event.data1 == nihia.knobs["KNOB_4A"]):
             event.handled = True  
             if channels.channelCount() > 4 and channels.selectedChannel() < (channels.channelCount()-4) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 4))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.selectedChannel() + 4) != 0 :
                     channels.setChannelVolume((channels.selectedChannel() + 4), (y - knobinc) ) # volume values go down
                     nihia.printVol(4, (round(channels.getChannelVolume(channels.selectedChannel() + 4) ,2)))
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 4))
                  y = round(x,2)
                  channels.setChannelVolume((channels.selectedChannel() + 4), (y + knobinc) ) # volume values go up
                  nihia.printVol(4, (round(channels.getChannelVolume(channels.selectedChannel() + 4) ,2)))

            #knob 6
            if (event.data1 == nihia.knobs["KNOB_5A"]):
             event.handled = True  
             if channels.channelCount() > 5 and channels.selectedChannel() < (channels.channelCount()-5) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 5))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.selectedChannel() + 5) != 0 :
                     channels.setChannelVolume((channels.selectedChannel() + 5), (y - knobinc) ) # volume values go down
                     nihia.printVol(5, (round(channels.getChannelVolume(channels.selectedChannel() + 5) ,2)))
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 5))
                  y = round(x,2)
                  channels.setChannelVolume((channels.selectedChannel() + 5), (y + knobinc) ) # volume values go up
                  nihia.printVol(5, (round(channels.getChannelVolume(channels.selectedChannel() + 5) ,2)))

            #knob 7
            if (event.data1 == nihia.knobs["KNOB_6A"]):
             event.handled = True  
             if channels.channelCount() > 6 and channels.selectedChannel() < (channels.channelCount()-6) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 6))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.selectedChannel() + 6) != 0 :
                     channels.setChannelVolume((channels.selectedChannel() + 6), (y - knobinc) ) # volume values go down
                     nihia.printVol(6, (round(channels.getChannelVolume(channels.selectedChannel() + 6) ,2)))
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 6))
                  y = round(x,2)
                  channels.setChannelVolume((channels.selectedChannel() + 6), (y + knobinc) ) # volume values go up
                  nihia.printVol(6, (round(channels.getChannelVolume(channels.selectedChannel() + 6) ,2)))

            #knob 8
            if (event.data1 == nihia.knobs["KNOB_7A"]):
             event.handled = True  
             if channels.channelCount() > 7 and channels.selectedChannel() < (channels.channelCount()-7) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 7))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.selectedChannel() + 7) != 0 :
                     channels.setChannelVolume((channels.selectedChannel() + 7), (y - knobinc) ) # volume values go down
                     nihia.printVol(7, (round(channels.getChannelVolume(channels.selectedChannel() + 7) ,2)))
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelVolume(channels.selectedChannel() + 7))
                  y = round(x,2)
                  channels.setChannelVolume((channels.selectedChannel() + 7), (y + knobinc) ) # volume values go up
                  nihia.printVol(7, (round(channels.getChannelVolume(channels.selectedChannel() + 7) ,2)))

            # PAN CONTROL

            #sknob 1
            if (event.data1 == nihia.knobs["KNOB_0B"]):
             event.handled = True  
             if event.data2 == nihia.knobs["DECREASE"]:
                x = (channels.getChannelPan(channels.selectedChannel() + 0))
                channels.setChannelPan((channels.selectedChannel() + 0), (x - knobinc) ) # pan values go down
                nihia.printPan(0, channels.getChannelPan(channels.selectedChannel() + 0) * 100)
  
             elif event.data2 == nihia.knobs["INCREASE"]:
                x = (channels.getChannelPan(channels.selectedChannel() + 0))
                channels.setChannelPan((channels.selectedChannel() + 0), (x + knobinc) ) # pan values go up
                nihia.printPan(0, channels.getChannelPan(channels.selectedChannel() + 0) * 100)

            #sknob 2
            if (event.data1 == nihia.knobs["KNOB_1B"]):
             event.handled = True  
             if channels.channelCount() > 1 and channels.selectedChannel() < (channels.channelCount()-1) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 1))
                  channels.setChannelPan((channels.selectedChannel() + 1), (x - knobinc) ) # pan values go down
                  nihia.printPan(1, channels.getChannelPan(channels.selectedChannel() + 1) * 100)
      
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 1))
                  channels.setChannelPan((channels.selectedChannel() + 1), (x + knobinc) ) # pan values go up
                  nihia.printPan(1, channels.getChannelPan(channels.selectedChannel() + 1) * 100)
   

            #sknob 3
            if (event.data1 == nihia.knobs["KNOB_2B"]):
             event.handled = True  
             if channels.channelCount() > 2 and channels.selectedChannel() < (channels.channelCount()-2) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 2))
                  channels.setChannelPan((channels.selectedChannel() + 2), (x - knobinc) ) # pan values go down
                  nihia.printPan(2, channels.getChannelPan(channels.selectedChannel() + 2) * 100)
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 2))
                  channels.setChannelPan((channels.selectedChannel() + 2), (x + knobinc) ) # pan values go up
                  nihia.printPan(2, channels.getChannelPan(channels.selectedChannel() + 2) * 100)   

            #sknob 4
            if (event.data1 == nihia.knobs["KNOB_3B"]):
             event.handled = True  
             if channels.channelCount() > 3 and channels.selectedChannel() < (channels.channelCount()-3) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 3))
                  channels.setChannelPan((channels.selectedChannel() + 3), (x - knobinc) ) # pan values go down
                  nihia.printPan(3, channels.getChannelPan(channels.selectedChannel() + 3) * 100)
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 3))
                  channels.setChannelPan((channels.selectedChannel() + 3), (x + knobinc) ) # pan values go up
                  nihia.printPan(3, channels.getChannelPan(channels.selectedChannel() + 3) * 100)  

            #sknob 5
            if (event.data1 == nihia.knobs["KNOB_4B"]):
             event.handled = True  
             if channels.channelCount() > 4 and channels.selectedChannel() < (channels.channelCount()-4) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 4))
                  channels.setChannelPan((channels.selectedChannel() + 4), (x - knobinc) ) # pan values go down
                  nihia.printPan(4, channels.getChannelPan(channels.selectedChannel() + 4) * 100)
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 4))
                  channels.setChannelPan((channels.selectedChannel() + 4), (x + knobinc) ) # pan values go up
                  nihia.printPan(4, channels.getChannelPan(channels.selectedChannel() + 4) * 100)  

            #sknob 6
            if (event.data1 == nihia.knobs["KNOB_5B"]):
             event.handled = True  
             if channels.channelCount() > 5 and channels.selectedChannel() < (channels.channelCount()-5) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                   x = (channels.getChannelPan(channels.selectedChannel() + 5))
                   channels.setChannelPan((channels.selectedChannel() + 5), (x - knobinc) ) # pan values go down
                   nihia.printPan(5, channels.getChannelPan(channels.selectedChannel() + 5) * 100)
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 5))
                  channels.setChannelPan((channels.selectedChannel() + 5), (x + knobinc) ) # pan values go up
                  nihia.printPan(5, channels.getChannelPan(channels.selectedChannel() + 5) * 100)

            #sknob 7
            if (event.data1 == nihia.knobs["KNOB_6B"]):
             event.handled = True  
             if channels.channelCount() > 6 and channels.selectedChannel() < (channels.channelCount()-6) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 6))
                  channels.setChannelPan((channels.selectedChannel() + 6), (x - knobinc) ) # pan values go down
                  nihia.printPan(6, channels.getChannelPan(channels.selectedChannel() + 6) * 100)
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 6))
                  channels.setChannelPan((channels.selectedChannel() + 6), (x + knobinc) ) # pan values go up
                  nihia.printPan(6, channels.getChannelPan(channels.selectedChannel() + 6) * 100)

            #sknob 8
            if (event.data1 == nihia.knobs["KNOB_7B"]):
             event.handled = True  
             if channels.channelCount() > 7 and channels.selectedChannel() < (channels.channelCount()-7) :  
               if event.data2 == nihia.knobs["DECREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 7))
                  channels.setChannelPan((channels.selectedChannel() + 7), (x - knobinc) ) # pan values go down
                  nihia.printPan(7, channels.getChannelPan(channels.selectedChannel() + 7) * 100)
                
               elif event.data2 == nihia.knobs["INCREASE"]:
                  x = (channels.getChannelPan(channels.selectedChannel() + 7))
                  channels.setChannelPan((channels.selectedChannel() + 7), (x + knobinc) ) # pan values go up
                  nihia.printPan(7, channels.getChannelPan(channels.selectedChannel() + 7) * 100)


            #4D controller # for channel rack

            if (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == right): #4d encoder spin right 
               event.handled = True
               ui.jog(1)
               ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
               ui.setHintMsg("Channel Rack selection rectangle")

            elif (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == left): #4d encoder spin left 
               event.handled = True
               ui.jog(-1)
               ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
               ui.setHintMsg("Channel Rack selection rectangle")
         
            if (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == right): #4d encoder push right
               event.handled = True
               ui.right(1)
               ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
               ui.setHintMsg("Moving to the start of Channel Rack")

            elif (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == left): #4d encoder push left
               event.handled = True
               ui.left(1)
               ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
               ui.setHintMsg("Moving to the end of Channel Rack")

            if (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == up): #4d encoder push up
               event.handled = True
               ui.up(1)
               ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
            
            elif (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == down): #4d encoder push down
               event.handled = True
               ui.down(1)
               ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
               

            if (event.data1 == nihia.buttons["ENCODER_BUTTON"]):
               event.handled = True
               doubleclickstatus = device.isDoubleClick(nihia.buttons["ENCODER_BUTTON"])
               if doubleclickstatus == True:
                  if ui.isInPopupMenu() == False:
                     ui.selectBrowserMenuItem()
                     ui.setHintMsg("Channel display filter")
                  else:
                     pass
               else:
                  if ui.isInPopupMenu() == True:
                     ui.enter()
                     ui.setHintMsg("Enter")
                  else:
                     pass



         elif ui.getFocused(2) == True: # playlist:

      
            if (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == right): #4d encoder spin right 
               event.handled = True
               ui.jog(1)
               
            elif (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == left): #4d encoder spin left 
               event.handled = True
               ui.jog(-1)
         
            if (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == right): #4d encoder push right
               event.handled = True
               arrange.jumpToMarker(1,0)

            elif (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == left): #4d encoder push left
               event.handled = True
               arrange.jumpToMarker(-1,0)

            if (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == up): #4d encoder push up
               event.handled = True
               ui.up(1)
            
            elif (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == down): #4d encoder push down
               event.handled = True
               ui.down(1)

            if (event.data1 == nihia.buttons["ENCODER_BUTTON"]):
               event.handled = True
               doubleclickstatus = device.isDoubleClick(nihia.buttons["ENCODER_BUTTON"])
               if doubleclickstatus == True:
                  if ui.isInPopupMenu() == False:
                     arrange.addAutoTimeMarker(mixer.getSongTickPos(), "Marker")   
                  else:
                     pass
               else:
                  pass
               

         elif ui.getFocused(3) == True: # Piano Roll:

            #knob for volume
            if (event.data1 == nihia.knobs["KNOB_0A"]):
             event.handled = True  
             if event.data2 == nihia.knobs["DECREASE"]:
                x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                y = round(x,2)
                if channels.getChannelVolume(channels.selectedChannel() + 0) != 0 :
                  channels.setChannelVolume((channels.selectedChannel() + 0), (y - knobinc) ) # volume values go down
                  nihia.printVol(0, (round(channels.getChannelVolume(channels.selectedChannel() + 0) ,2)))
       
             elif event.data2 == nihia.knobs["INCREASE"]:
                x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                y = round(x,2)
                channels.setChannelVolume((channels.selectedChannel() + 0), (y + knobinc) ) # volume values go up
                nihia.printVol(0, (round(channels.getChannelVolume(channels.selectedChannel() + 0) ,2)))

            #knob for pan
            if (event.data1 == nihia.knobs["KNOB_0B"]):
             event.handled = True  
             if event.data2 == nihia.knobs["DECREASE"]:
                x = (channels.getChannelPan(channels.selectedChannel() + 0))
                channels.setChannelPan((channels.selectedChannel() + 0), (x - knobinc) ) # pan values go down
                nihia.printPan(0, channels.getChannelPan(channels.selectedChannel() + 0) * 100)
  
             elif event.data2 == nihia.knobs["INCREASE"]:
                x = (channels.getChannelPan(channels.selectedChannel() + 0))
                channels.setChannelPan((channels.selectedChannel() + 0), (x + knobinc) ) # pan values go up
                nihia.printPan(0, channels.getChannelPan(channels.selectedChannel() + 0) * 100)

            
            
            if (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == right): #4d encoder spin right 
               event.handled = True
               ui.jog(1)

            elif (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == left): #4d encoder spin left 
               event.handled = True
               ui.jog(-1)
         
            if (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == right): #4d encoder push right
               event.handled = True
               ui.right(1)
               
            elif (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == left): #4d encoder push left
               event.handled = True
               ui.left(1)
               
            if (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == up): #4d encoder push up
               event.handled = True
               ui.up(1)
            
            elif (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == down): #4d encoder push down
               event.handled = True
               ui.down(1)

            if (event.data1 == nihia.buttons["ENCODER_BUTTON"]):
               event.handled = True
               nodeFileType = ui.getFocusedNodeFileType()
               doubleclickstatus = device.isDoubleClick(nihia.buttons["ENCODER_BUTTON"])
               if doubleclickstatus == True: 
                  ui.selectBrowserMenuItem()
               else:
                  if ui.isInPopupMenu() == True:
                     ui.enter()
                     ui.setHintMsg("Enter")
                  else:
                     pass



         elif ui.getFocused(4) == True: # Browser:
      
            if (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == right): #4d encoder spin right 
               event.handled = True
               fileNameText = ui.navigateBrowserMenu(1,0)
               nihia.printText(0, nihia.message["BROWSER"] + fileNameText)

            elif (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == left): #4d encoder spin left 
               event.handled = True
               fileNameText = ui.navigateBrowserMenu(0,0)
               nihia.printText(0, nihia.message["BROWSER"] + fileNameText)
         
            if (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == right): #4d encoder push right
               event.handled = True
               #ui.right(1)
               ui.next()
               

            elif (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == left): #4d encoder push left
               event.handled = True
               #ui.left(1)
               ui.previous()

            if (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == up): #4d encoder push up
               event.handled = True
               fileNameText = ui.navigateBrowserMenu(0,0)
               nihia.printText(0, nihia.message["BROWSER"] + fileNameText)
            
            elif (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == down): #4d encoder push down
               event.handled = True
               fileNameText = ui.navigateBrowserMenu(1,0)
               nihia.printText(0, nihia.message["BROWSER"] + fileNameText)

            if (event.data1 == nihia.buttons["ENCODER_BUTTON"]):
               event.handled = True
               nodeFileType = ui.getFocusedNodeFileType()
               doubleclickstatus = device.isDoubleClick(nihia.buttons["ENCODER_BUTTON"])
               if doubleclickstatus == True: 
                  if nodeFileType <= -100:
                     ui.enter()
                     ui.setHintMsg("Enter")
                  else:
                     ui.selectBrowserMenuItem()
                     ui.setHintMsg("Open menu")
               else:
                  if ui.isInPopupMenu() == True:
                     ui.enter()
                     ui.setHintMsg("Enter")
                  else:
                     pass


         else:

            #4D controller # for everything else

            if (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == right): #4d encoder spin right 
               event.handled = True
               ui.down(1)

            elif (event.data1 == nihia.buttons["ENCODER_SPIN"]) & (event.data2 == left): #4d encoder spin left 
               event.handled = True
               ui.up(1)
         
            if (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == right): #4d encoder push right
               event.handled = True
               ui.right(1)

            elif (event.data1 == nihia.buttons["ENCODER_HORIZONTAL"]) & (event.data2 == left): #4d encoder push left
               event.handled = True
               ui.left(1)

            if (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == up): #4d encoder push up
               event.handled = True
               ui.up()
            
            elif (event.data1 == nihia.buttons["ENCODER_VERTICAL"]) & (event.data2 == down): #4d encoder push down
               event.handled = True
               ui.down()

            if (event.data1 == nihia.buttons["ENCODER_BUTTON"]):
               event.handled = True
               doubleclickstatus = device.isDoubleClick(nihia.buttons["ENCODER_BUTTON"])
               if doubleclickstatus == True:
                  pass
               else:
                  ui.enter()
                  ui.setHintMsg("enter")

 
 
     def UpdateLEDs(self): #controls all nights located within buttons
         """Function for device light communication (excluding OLED screen)"""

         if device.isAssigned():

            for a in [transport.isPlaying()]:
              if a == off: #not playing
                  nihia.dataOut(nihia.buttons["STOP"], on) #stop on

              elif a == on: #playing
                  nihia.dataOut(nihia.buttons["STOP"], off) #stop off


            if transport.isPlaying() == True:
               pass
            else:
               for b in [transport.isRecording()]:
                  if b == off: #not recording
                     nihia.dataOut(nihia.buttons["REC"], off)

                  elif b == on: #recording
                     nihia.dataOut(nihia.buttons["REC"], on)

            for c in [transport.getLoopMode()]:
               if c == off: #loop mood
                  nihia.dataOut(nihia.buttons["LOOP"], on)

               elif c == on: #playlist mode
                  nihia.dataOut(nihia.buttons["LOOP"], off)

            for d in [ui.isMetronomeEnabled()]:
               if d == off: #metro off
                  nihia.dataOut(nihia.buttons["METRO"], off)

               elif d == on: #metro on
                  nihia.dataOut(nihia.buttons["METRO"], on)

            for e in [ui.isPrecountEnabled()]:
              if e == off: #pre count on
                  nihia.dataOut(nihia.buttons["COUNT_IN"], off)

              elif e == on: #pre count off
                  nihia.dataOut(nihia.buttons["COUNT_IN"], on) 

            for f in [ui.getSnapMode()]:
              if f == 3: #quantize always on
                  nihia.dataOut(nihia.buttons["QUANTIZE"], on)
                  nihia.dataOut(nihia.buttons["AUTO"], on)

              elif f != 1: #quantize alwayns on
                  nihia.dataOut(nihia.buttons["QUANTIZE"], on)
                  nihia.dataOut(nihia.buttons["AUTO"], on)
                  
            for g in [transport.isPlaying()]:
              if transport.isRecording() == 0 & transport.isPlaying() == 1: 
                  if g == off: #play off
                     nihia.dataOut(nihia.buttons["PLAY"], off)
                  elif g != on: #play on
                     nihia.dataOut(nihia.buttons["PLAY"], on)
              elif g == off: #play off: 
                  nihia.dataOut(nihia.buttons["PLAY"], off)



     def UpdateOLED(self): #controls OLED screen messages
        """Function for OLED control"""

        

        if ui.getFocused(0) == True: #mixer volume control

            xy = 1.25

            if mixer.trackNumber() <= currentUtility:
               nihia.printText(0, mixer.getTrackName(mixer.trackNumber() + 0))
               nihia.printVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),2)))
               nihia.printPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)

            if mixer.trackNumber() <= 125:
               nihia.printText(1, mixer.getTrackName(mixer.trackNumber() + 1))
               nihia.printVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))
               nihia.printPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)
               
               if mixer.isTrackMuted(mixer.trackNumber() + 1) == True:
                  nihia.mixerSendInfo("IS_MUTE",1, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",1, value=0)

               if mixer.isTrackSolo(mixer.trackNumber() + 1) == True:
                  nihia.mixerSendInfo("IS_SOLO",1, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",1, value=0)               
                  

            if mixer.trackNumber() <= 124:
               nihia.printText(2, mixer.getTrackName(mixer.trackNumber() + 2))
               nihia.printVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))
               nihia.printPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)

               if mixer.isTrackMuted(mixer.trackNumber() + 2) == True:
                  nihia.mixerSendInfo("IS_MUTE",2, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",2, value=0)

               if mixer.isTrackSolo(mixer.trackNumber() + 2) == True:
                  nihia.mixerSendInfo("IS_SOLO",2, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",2, value=0)  

            if mixer.trackNumber() <= 123:
               nihia.printText(3, mixer.getTrackName(mixer.trackNumber() + 3))
               nihia.printVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))
               nihia.printPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)

               if mixer.isTrackMuted(mixer.trackNumber() + 3) == True:
                  nihia.mixerSendInfo("IS_MUTE",3, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",3, value=0)

               if mixer.isTrackSolo(mixer.trackNumber() + 3) == True:
                  nihia.mixerSendInfo("IS_SOLO",3, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",3, value=0)  

            if mixer.trackNumber() <= 122:
               nihia.printText(4, mixer.getTrackName(mixer.trackNumber() + 4))
               nihia.printVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))
               nihia.printPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)

               if mixer.isTrackMuted(mixer.trackNumber() + 4) == True:
                  nihia.mixerSendInfo("IS_MUTE",4, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",4, value=0)

               if mixer.isTrackSolo(mixer.trackNumber() + 4) == True:
                  nihia.mixerSendInfo("IS_SOLO",4, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",4, value=0)  

            if mixer.trackNumber() <= 121:
               nihia.printText(5, mixer.getTrackName(mixer.trackNumber() + 5))
               nihia.printVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))
               nihia.printPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)

               if mixer.isTrackMuted(mixer.trackNumber() + 5) == True:
                  nihia.mixerSendInfo("IS_MUTE",5, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",5, value=0)

               if mixer.isTrackSolo(mixer.trackNumber() + 5) == True:
                  nihia.mixerSendInfo("IS_SOLO",5, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",5, value=0)  

            if mixer.trackNumber() <= 120:
               nihia.printText(6, mixer.getTrackName(mixer.trackNumber() + 6))
               nihia.printVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))
               nihia.printPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)

               if mixer.isTrackMuted(mixer.trackNumber() + 6) == True:
                  nihia.mixerSendInfo("IS_MUTE",6, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",6, value=0)

               if mixer.isTrackSolo(mixer.trackNumber() + 6) == True:
                  nihia.mixerSendInfo("IS_SOLO",6, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",6, value=0)  

            if mixer.trackNumber() <= 119:
               nihia.printText(7, mixer.getTrackName(mixer.trackNumber() + 7))
               nihia.printVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))
               nihia.printPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)

               if mixer.isTrackMuted(mixer.trackNumber() + 7) == True:
                  nihia.mixerSendInfo("IS_MUTE",7, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",7, value=0)

               if mixer.isTrackSolo(mixer.trackNumber() + 7) == True:
                  nihia.mixerSendInfo("IS_SOLO",7, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",7, value=0)  
               

            if mixer.isTrackEnabled(mixer.trackNumber()) == 1: #mute light off
               
               nihia.dataOut(nihia.buttons["MUTE_SELECTED"], off)
               nihia.mixerSendInfo("IS_MUTE",0, value=0)
               
               
            elif mixer.isTrackEnabled(mixer.trackNumber()) == 0: #mute light on
               
               nihia.dataOut(nihia.buttons["MUTE_SELECTED"], on)
               nihia.mixerSendInfo("IS_MUTE",0, value=1)


            if mixer.isTrackSolo(mixer.trackNumber()) == 0: #solo light off
               
               nihia.dataOut(nihia.buttons["SOLO_SELECTED"], off)
               nihia.mixerSendInfo("IS_SOLO",0, value=0)

            elif mixer.isTrackSolo(mixer.trackNumber()) == 1: #solo light on
               
               if mixer.isTrackMuted(mixer.trackNumber()) == 0:
                  nihia.dataOut(nihia.buttons["SOLO_SELECTED"], on)
                  nihia.mixerSendInfo("IS_SOLO",0, value=1)
               else:
                  nihia.dataOut(nihia.buttons["SOLO_SELECTED"], off)
                  nihia.mixerSendInfo("IS_SOLO",0, value=0)

        if ui.getFocused(1) == True: # channel rack
            
            nihia.printText(0, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 0))

            if channels.channelCount() > 0 and channels.selectedChannel() < (channels.channelCount()-0) :
               nihia.printText(1, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 0))
               nihia.printVol(0, (round(channels.getChannelVolume(channels.selectedChannel() + 0), 2)))
               nihia.printPan(0, channels.getChannelPan(channels.selectedChannel() + 0) * 100)
            else:
               nihia.printText(1, nihia.message["EMPTY"])
               nihia.printVol(0, 104)
               nihia.printPan(0, 104)
               nihia.mixerSendInfo("IS_MUTE",0, value=0)
               nihia.mixerSendInfo("IS_SOLO",0, value=0)


            if channels.channelCount() > 1 and channels.selectedChannel() < (channels.channelCount()-1) :
               nihia.printText(1, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 1))
               nihia.printVol(1, (round(channels.getChannelVolume(channels.selectedChannel() + 1), 2)))
               nihia.printPan(1, channels.getChannelPan(channels.selectedChannel() + 1) * 100)

               if channels.isChannelMuted(channels.selectedChannel() + 1) == True:
                  nihia.mixerSendInfo("IS_MUTE",1, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",1, value=0)

               if channels.isChannelSolo(channels.selectedChannel() + 1) == True:
                  nihia.mixerSendInfo("IS_SOLO",1, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",1, value=0)

            else:
               nihia.printText(1, nihia.message["EMPTY"])
               nihia.printVol(1, 104)
               nihia.printPan(1, 104)
               nihia.mixerSendInfo("IS_MUTE",1, value=0)
               nihia.mixerSendInfo("IS_SOLO",1, value=0)

            if channels.channelCount() > 2 and channels.selectedChannel() < (channels.channelCount()-2) :
               nihia.printText(2, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 2))
               nihia.printVol(2, (round(channels.getChannelVolume(channels.selectedChannel() + 2), 2)))
               nihia.printPan(2, channels.getChannelPan(channels.selectedChannel() + 2) * 100)

               if channels.isChannelMuted(channels.selectedChannel() + 2) == True:
                  nihia.mixerSendInfo("IS_MUTE",2, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",2, value=0)

               if channels.isChannelSolo(channels.selectedChannel() + 2) == True:
                  nihia.mixerSendInfo("IS_SOLO",2, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",2, value=0)

            else:
               nihia.printText(2, nihia.message["EMPTY"])
               nihia.printVol(2, 104)
               nihia.printPan(2, 104)
               nihia.mixerSendInfo("IS_MUTE",2, value=0)
               nihia.mixerSendInfo("IS_SOLO",2, value=0)
               
            if channels.channelCount() > 3 and channels.selectedChannel() < (channels.channelCount()-3) :
               nihia.printText(3, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 3))
               nihia.printVol(3, (round(channels.getChannelVolume(channels.selectedChannel() + 3), 2)))
               nihia.printPan(3, channels.getChannelPan(channels.selectedChannel() + 3) * 100)

               if channels.isChannelMuted(channels.selectedChannel() + 3) == True:
                  nihia.mixerSendInfo("IS_MUTE",3, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",3, value=0)

               if channels.isChannelSolo(channels.selectedChannel() + 3) == True:
                  nihia.mixerSendInfo("IS_SOLO",3, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",3, value=0)
            else:
               nihia.printText(3, nihia.message["EMPTY"])
               nihia.printVol(3, 104)
               nihia.printPan(3, 104)
               nihia.mixerSendInfo("IS_MUTE",3, value=0)
               nihia.mixerSendInfo("IS_SOLO",3, value=0)
               
            if channels.channelCount() > 4 and channels.selectedChannel() < (channels.channelCount()-4) :
               nihia.printText(4, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 4))
               nihia.printVol(4, (round(channels.getChannelVolume(channels.selectedChannel() + 4), 2)))
               nihia.printPan(4, channels.getChannelPan(channels.selectedChannel() + 4) * 100)

               if channels.isChannelMuted(channels.selectedChannel() + 4) == True:
                  nihia.mixerSendInfo("IS_MUTE",4, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",4, value=0)

               if channels.isChannelSolo(channels.selectedChannel() + 4) == True:
                  nihia.mixerSendInfo("IS_SOLO",4, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",4, value=0)
            else:
               nihia.printText(4, nihia.message["EMPTY"])
               nihia.printVol(4, 104)
               nihia.printPan(4, 104)
               nihia.mixerSendInfo("IS_MUTE",4, value=0)
               nihia.mixerSendInfo("IS_SOLO",4, value=0)
               
            if channels.channelCount() > 5 and channels.selectedChannel() < (channels.channelCount()-5) :
               nihia.printText(5, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 5))
               nihia.printVol(5, (round(channels.getChannelVolume(channels.selectedChannel() + 5), 2)))
               nihia.printPan(5, channels.getChannelPan(channels.selectedChannel() + 5) * 100)

               if channels.isChannelMuted(channels.selectedChannel() + 5) == True:
                  nihia.mixerSendInfo("IS_MUTE",5, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",5, value=0)

               if channels.isChannelSolo(channels.selectedChannel() + 5) == True:
                  nihia.mixerSendInfo("IS_SOLO",5, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",5, value=0)

            else:
               nihia.printText(5, nihia.message["EMPTY"])
               nihia.printVol(5, 104)
               nihia.printPan(5, 104)
               nihia.mixerSendInfo("IS_MUTE",5, value=0)
               nihia.mixerSendInfo("IS_SOLO",5, value=0)
               
            if channels.channelCount() > 6 and channels.selectedChannel() < (channels.channelCount()-6) :
               nihia.printText(6, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 6))
               nihia.printVol(6, (round(channels.getChannelVolume(channels.selectedChannel() + 6), 2)))
               nihia.printPan(6, channels.getChannelPan(channels.selectedChannel() + 6) * 100)

               if channels.isChannelMuted(channels.selectedChannel() + 6) == True:
                  nihia.mixerSendInfo("IS_MUTE",6, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",6, value=0)

               if channels.isChannelSolo(channels.selectedChannel() + 6) == True:
                  nihia.mixerSendInfo("IS_SOLO",6, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",6, value=0)
            else:
               nihia.printText(6, nihia.message["EMPTY"])
               nihia.printVol(6, 104)
               nihia.printPan(6, 104)
               nihia.mixerSendInfo("IS_MUTE",6, value=0)
               nihia.mixerSendInfo("IS_SOLO",6, value=0)
               
            if channels.channelCount() > 7 and channels.selectedChannel() < (channels.channelCount()-7) :
               nihia.printText(7, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 7))
               nihia.printVol(7, (round(channels.getChannelVolume(channels.selectedChannel() + 7), 2)))
               nihia.printPan(7, channels.getChannelPan(channels.selectedChannel() + 7) * 100)

               if channels.isChannelMuted(channels.selectedChannel() + 7) == True:
                  nihia.mixerSendInfo("IS_MUTE",7, value=1)
               else:
                  nihia.mixerSendInfo("IS_MUTE",7, value=0)

               if channels.isChannelSolo(channels.selectedChannel() + 7) == True:
                  nihia.mixerSendInfo("IS_SOLO",7, value=1)
               else:
                  nihia.mixerSendInfo("IS_SOLO",7, value=0)
            else:
               nihia.printText(7, nihia.message["EMPTY"])
               nihia.printVol(7, 104)
               nihia.printPan(7, 104)
               nihia.mixerSendInfo("IS_MUTE",7, value=0)
               nihia.mixerSendInfo("IS_SOLO",7, value=0)

            if channels.isChannelMuted(channels.selectedChannel()) == 0: #mute light off
               
               nihia.dataOut(nihia.buttons["MUTE_SELECTED"], off)
               nihia.mixerSendInfo("IS_MUTE",0, value=0)
                
            else: #mute light on
               nihia.dataOut(nihia.buttons["MUTE_SELECTED"], on)
               nihia.mixerSendInfo("IS_MUTE",0, value=1)
               
            if channels.channelCount() >= 2: 
               if channels.isChannelSolo(channels.selectedChannel()) == 0: #solo light off
                  nihia.dataOut(nihia.buttons["SOLO_SELECTED"], off)
                  nihia.mixerSendInfo("IS_SOLO",0, value=0)

               elif channels.isChannelSolo(channels.selectedChannel()) == 1: #solo light on
                  if channels.isChannelMuted(channels.selectedChannel()) == 0:
                     nihia.dataOut(nihia.buttons["SOLO_SELECTED"], on)
                     nihia.mixerSendInfo("IS_SOLO",0, value=1)
                  else:
                     nihia.dataOut(nihia.buttons["SOLO_SELECTED"], off)
                     nihia.mixerSendInfo("IS_SOLO",0, value=0)


        if ui.getFocused(2) == True: # playlist

            #spells out 'Playlist' on tracks 1 through 8 on OLED
            currentBar = str(playlist.getVisTimeBar())
            currentStep = str(playlist.getVisTimeStep())
            currentTick = str(playlist.getVisTimeTick())

            zeroStr = str(0)

            if int(currentStep) <= 9 and int(currentStep) >= 0:
               currentTime = str(currentBar+":"+zeroStr+currentStep)
            elif int(currentStep) >= 0:
               currentTime = str(currentBar+":"+currentStep)
            elif int(currentStep) < 0:
               currentTime = " "

            if ui.getTimeDispMin() == True and int(currentStep) >= 0:
               timeDisp = "M:S | "
            elif ui.getTimeDispMin() == False and int(currentStep) >= 0:
               timeDisp = "B:B | "
            elif int(currentStep) < 0:
               timeDisp = "REC in..."


            nihia.printText(0, (timeDisp+currentTime))
            nihia.printText(1, nihia.message["EMPTY"])
            nihia.printText(2, nihia.message["EMPTY"])
            nihia.printText(3, nihia.message["EMPTY"])
            nihia.printText(4, nihia.message["EMPTY"])
            nihia.printText(5, nihia.message["EMPTY"])
            nihia.printText(6, nihia.message["EMPTY"])
            nihia.printText(7, nihia.message["EMPTY"])
            nihia.printVol(0, 104)
            nihia.printPan(0, 104)

        if ui.getFocused(3) == True: # Piano Roll 
            nihia.printText(0, "PR: " + channels.getChannelName(channels.selectedChannel() + 0))

            if channels.channelCount() > 1 and channels.selectedChannel() < (channels.channelCount()-1) :
               nihia.printText(1, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 1))
               nihia.printVol(1, (round(channels.getChannelVolume(channels.selectedChannel() + 1), 2)))
               nihia.printPan(1, channels.getChannelPan(channels.selectedChannel() + 1) * 100)
            else:
               nihia.printText(1, nihia.message["EMPTY"])
               nihia.printVol(1, 104)
               nihia.printPan(1, 104)

            if channels.channelCount() > 2 and channels.selectedChannel() < (channels.channelCount()-2) :
               nihia.printText(2, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 2))
               nihia.printVol(2, (round(channels.getChannelVolume(channels.selectedChannel() + 2), 2)))
               nihia.printPan(2, channels.getChannelPan(channels.selectedChannel() + 2) * 100)
            else:
               nihia.printText(2, nihia.message["EMPTY"])
               nihia.printVol(2, 104)
               nihia.printPan(2, 104)
               
            if channels.channelCount() > 3 and channels.selectedChannel() < (channels.channelCount()-3) :
               nihia.printText(3, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 3))
               nihia.printVol(3, (round(channels.getChannelVolume(channels.selectedChannel() + 3), 2)))
               nihia.printPan(3, channels.getChannelPan(channels.selectedChannel() + 3) * 100)
            else:
               nihia.printText(3, nihia.message["EMPTY"])
               nihia.printVol(3, 104)
               nihia.printPan(3, 104)
               
            if channels.channelCount() > 4 and channels.selectedChannel() < (channels.channelCount()-4) :
               nihia.printText(4, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 4))
               nihia.printVol(4, (round(channels.getChannelVolume(channels.selectedChannel() + 4), 2)))
               nihia.printPan(4, channels.getChannelPan(channels.selectedChannel() + 4) * 100)
            else:
               nihia.printText(4, nihia.message["EMPTY"])
               nihia.printVol(4, 104)
               nihia.printPan(4, 104)
               
            if channels.channelCount() > 5 and channels.selectedChannel() < (channels.channelCount()-5) :
               nihia.printText(5, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 5))
               nihia.printVol(5, (round(channels.getChannelVolume(channels.selectedChannel() + 5), 2)))
               nihia.printPan(5, channels.getChannelPan(channels.selectedChannel() + 5) * 100)
            else:
               nihia.printText(5, nihia.message["EMPTY"])
               nihia.printVol(5, 104)
               nihia.printPan(5, 104)
               
            if channels.channelCount() > 6 and channels.selectedChannel() < (channels.channelCount()-6) :
               nihia.printText(6, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 6))
               nihia.printVol(6, (round(channels.getChannelVolume(channels.selectedChannel() + 6), 2)))
               nihia.printPan(6, channels.getChannelPan(channels.selectedChannel() + 6) * 100)
            else:
               nihia.printText(6, nihia.message["EMPTY"])
               nihia.printVol(6, 104)
               nihia.printPan(6, 104)
               
            if channels.channelCount() > 7 and channels.selectedChannel() < (channels.channelCount()-7) :
               nihia.printText(7, nihia.message["CHANNEL_RACK"] + channels.getChannelName(channels.selectedChannel() + 7))
               nihia.printVol(7, (round(channels.getChannelVolume(channels.selectedChannel() + 7), 2)))
               nihia.printPan(7, channels.getChannelPan(channels.selectedChannel() + 7) * 100)
            else:
               nihia.printText(7, nihia.message["EMPTY"])
               nihia.printVol(7, 104)
               nihia.printPan(7, 104)

            if channels.getChannelName(channels.selectedChannel()) != channels.getChannelName(0):
               nihia.printVol(0, 104)
               nihia.printPan(0, 104)

            else:
               nihia.printVol(0, (round(channels.getChannelVolume(channels.selectedChannel() + 0), 2)))
               nihia.printPan(0, channels.getChannelPan(channels.selectedChannel() + 0) * 100)


        if ui.getFocused(4) == True: # Browser

            nihia.printText(1, nihia.message["EMPTY"])
            nihia.printText(2, nihia.message["EMPTY"])
            nihia.printText(3, nihia.message["EMPTY"])
            nihia.printText(4, nihia.message["EMPTY"])
            nihia.printText(5, nihia.message["EMPTY"])
            nihia.printText(6, nihia.message["EMPTY"])
            nihia.printText(7, nihia.message["EMPTY"])
            
            nihia.printVol(0, 104)
            nihia.printPan(0, 104)     

            nihia.printVol(1, 104)
            nihia.printPan(1, 104)

            nihia.printVol(2, 104)
            nihia.printPan(2, 104)

            nihia.printVol(3, 104)
            nihia.printPan(3, 104)

            nihia.printVol(4, 104)
            nihia.printPan(4, 104)

            nihia.printVol(5, 104)
            nihia.printPan(5, 104)

            nihia.printVol(6, 104)
            nihia.printPan(6, 104)

            nihia.printVol(7, 104)
            nihia.printPan(7, 104)

        if ui.getFocused(5) == True: # Plugin
            #gets plugin name to display on OLED
            
            if "Fruity Wrapper" in ui.getFocusedPluginName():
               nihia.printText(0, ui.getFocusedFormCaption())
            elif '' == ui.getFocusedPluginName():
               nihia.printText(0, ui.getFocusedFormCaption())
            else:
               nihia.printText(0, ui.getFocusedPluginName())
               

            nihia.printText(1, nihia.message["EMPTY"])
            nihia.printText(2, nihia.message["EMPTY"])
            nihia.printText(3, nihia.message["EMPTY"])
            nihia.printText(4, nihia.message["EMPTY"])
            nihia.printText(5, nihia.message["EMPTY"])
            nihia.printText(6, nihia.message["EMPTY"])
            nihia.printText(7, nihia.message["EMPTY"])

            if channels.getChannelName(channels.selectedChannel()) in ui.getFocusedFormCaption():
               nihia.printVol(0, (round(channels.getChannelVolume(channels.selectedChannel(0)), 2)))
               nihia.printPan(0, channels.getChannelPan(channels.selectedChannel(0)) * 100)
            else:
               nihia.printVol(0, 104)
               nihia.printPan(0, 104)

               nihia.printVol(1, 104)
               nihia.printPan(1, 104)

               nihia.printVol(2, 104)
               nihia.printPan(2, 104)

               nihia.printVol(3, 104)
               nihia.printPan(3, 104)

               nihia.printVol(4, 104)
               nihia.printPan(4, 104)

               nihia.printVol(5, 104)
               nihia.printPan(5, 104)

               nihia.printVol(6, 104)
               nihia.printPan(6, 104)

               nihia.printVol(7, 104)
               nihia.printPan(7, 104)
            

            nihia.printVol(1, 104)
            nihia.printPan(1, 104)

            nihia.printVol(2, 104)
            nihia.printPan(2, 104)

            nihia.printVol(3, 104)
            nihia.printPan(3, 104)

            nihia.printVol(4, 104)
            nihia.printPan(4, 104)

            nihia.printVol(5, 104)
            nihia.printPan(5, 104)

            nihia.printVol(6, 104)
            nihia.printPan(6, 104)

            nihia.printVol(7, 104)
            nihia.printPan(7, 104)
         


     def OnRefresh(self, flags): #when something happens in FL Studio, update the keyboard lights & OLED
        """Function for when something changed that the script might want to respond to."""

        self.UpdateLEDs(), self.UpdateOLED()

     def OnUpdateBeatIndicator(self, Value): #play light flashes to the tempo of the project
       """Function that is called when the beat indicator has changed."""
       

       if ui.getFocused(2) == True: # playlist
          self.UpdateOLED()
       else:
          pass

       if transport.isRecording() == 0:
          if Value == 1:
             nihia.dataOut(nihia.buttons["PLAY"], on) #play light bright
          elif Value == 2:
             nihia.dataOut(nihia.buttons["PLAY"], on) #play light bright
          elif Value == 0:
             nihia.dataOut(nihia.buttons["PLAY"], off) #play light dim

       elif transport.isRecording() == 1:
          nihia.dataOut(nihia.buttons["PLAY"], on)
          if Value == 1:
             nihia.dataOut(nihia.buttons["REC"], on) #play light bright
          elif Value == 2:
             nihia.dataOut(nihia.buttons["REC"], on) #play light bright
          elif Value == 0:
             nihia.dataOut(nihia.buttons["REC"], off) #play light dim  
 

     #def OnMidiMsg(self, event):
     #    _thread.start_new_thread(KeyKompleteKontrolBase.TOnMidiMsg, (self, event)) #Crashes on Windows. Sigh. Can't use for now

     #def UpdateLEDs(self):
     #    _thread.start_new_thread(KeyKompleteKontrolBase.TUpdateLEDs, (self,))

     #def UpdateOLED(self):
     #    _thread.start_new_thread(KeyKompleteKontrolBase.TUpdateOLED, (self,))

     #def OnRefresh(self, flags):
     #    _thread.start_new_thread(KeyKompleteKontrolBase.TOnRefresh, (self, flags))    

     #def OnUpdateBeatIndicator(self, Value):
     #    _thread.start_new_thread(KeyKompleteKontrolBase.TOnUpdateBeatIndicator, (self, Value))






KompleteKontrolBase = KeyKompleteKontrolBase()



def OnInit():
   # command to initialize the protocol handshake
   compatibility = False
   compatibility = VersionCheck(compatibility)
   if compatibility == True:
      KompleteKontrolBase.OnInit()
   else:
      pass

def OnRefresh(flags):
   try:
      KompleteKontrolBase.OnRefresh(flags)
   except:
      pass

def OnUpdateBeatIndicator(Value):
   KompleteKontrolBase.OnUpdateBeatIndicator(Value)

def OnMidiMsg(event):
   try:
      KompleteKontrolBase.OnMidiMsg(event)
   except:
     pass

def OnDeInit():
   if ui.isClosing() == True:
      nihia.printText(0, GOODBYE_MESSAGE)
      time.sleep(timedelay)
      nihia.terminate(), KompleteKontrolBase.OnDeInit() # Command to stop the protocol
   else:
      nihia.terminate()

def detectDevice(kkName):
   """ Gets the MIDI device name from FL Studio and sets `DEVICE_SERIES` to the right value in order for the script to work properly. """
   
   deviceName = device.getName()

   if deviceName == "Komplete Kontrol A DAW":
      kkName = "Komplete Kontrol Series A"

   elif deviceName == "Komplete Kontrol M DAW":
      kkName = "Komplete Kontrol Series M"

   else:
      kkName = device.getName()
 
   return kkName

def VersionCheck(compatibility):
   """Called to check user's FL Studio version to see if this script can run."""

   kkName = ""
   OS = ""
   
   print(OUTPUT_MESSAGE)

   if platform == "darwin":
      OS = "macOS"
   elif platform == "win32":
      OS = "Windows"


   if MIN_Major == int(VER_Major) and int(VER_Minor) >= MIN_Minor: # and int(VER_Release >=  MIN_Release):
      print(ui.getProgTitle(), ui.getVersion(), "\nis compatible with this script on", OS,"\n")
      compatibility = True

   else:
      print(ui.getProgTitle(), ui.getVersion(), "\nis not compatible with this script on", OS, "\n\nKomplete Kontrol Script " + VERSION_NUMBER + 
      " will not load on this device. \nPlease update", VER_Major, ui.getVersion(), "to", str(MIN_Major) + "." + str(MIN_Minor) + "." + str(MIN_Release),
      "or higher.\n")
      compatibility = False

   seriesDevice = detectDevice(kkName)

   if seriesDevice ==  "Komplete Kontrol Series A" or "Komplete Kontrol Series M":
      print("A", seriesDevice, "has been detected. It is compatible with this script\n\n")

   else:
      print("The", seriesDevice, "is not compatible with this script. Only the Komplete Kontrol Series A and Komplete Kontrol Series M are comptible with this script\n\n")

   return compatibility

def TranslateVolume(Value):
   """Function that converts values from device into FL Studio comptable values for volume conversion"""

   return (math.exp(Value * math.log(11)) - 1) * 0.1   

def VolTodB(Value): #works off of the db scale explained here: https://www.image-line.com/support/flstudio_online_manual/html/mixer_dB.htm
   """Function that converts % valume into db"""
   
   Value = TranslateVolume(Value)
   return round(math.log10(Value) * 20, 1)  