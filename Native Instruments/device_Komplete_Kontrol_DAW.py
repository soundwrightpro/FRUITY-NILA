# name=Komplete Kontrol DAW
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-m32/
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-a25-a49-a61/

# GitHub for this script
# url=https://github.com/soundwrightpro/FLNI_KK

# FL Studio Forum
# https://forum.image-line.com/viewtopic.php?f=1994&t=225473
# script by Duwayne "Sound" Wright www.soundwrightpro.com and additional code from Hobyst

# Have a question? Want to be a beta tester? Have a request? Want to say hi? Join the FL Studio NI on Discord!
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

import channels
import mixer
import device
import transport
import general
import playlist
import ui

import midi
import utils
import time
import sys
import binascii
import math

import nihia

#data2, up down right left values for knobs and 4d controller
down = right = 1
up = left = 127

#knob increment value; change this if you want a different feel to the knobs. nothing higher than 1.00
knobinc = 0.01

#on/off values
on = 1
off = 0

#time delay for messages on screen
timedelay = 0.45

VERSION_NUMBER = "v4.1.1"
HELLO_MESSAGE = "KK " + VERSION_NUMBER 
GOODBYE_MESSAGE = "Goodbye"
OUTPUT_MESSAGE = "Komplete Kontrol DAW " + VERSION_NUMBER + "\n\nMIT License\nCopyright © 2020 Duwayne Wright\n\nJoin the FL Studio NI on Discord!\nhttps://discord.gg/7FYrJEq"

def TranslateVolume(Value):
   """Function that converts values from device into FL Studio comptable values for volume conversion"""

   return (math.exp(Value * math.log(11)) - 1) * 0.1   

def VolTodB(Value): #works off of the db scale explained here: https://www.image-line.com/support/flstudio_online_manual/html/mixer_dB.htm
   """Function that converts % valume into db"""
   
   Value = TranslateVolume(Value)
   return round(math.log10(Value) * 20, 1)

class KeyKompleteKontrolBase(): #used a class to sheild against crashes
     
     def OnInit(self):
      """ Called when the script has been started.""" 

      #initializing NI Host Integration Agent API for FL Studio by Hobyst 
      nihia.initiate() 

      #turning on group of lights not initialized during the nihia.initiate()
      nihia.dataOut(nihia.buttons["CLEAR"], on)
      nihia.dataOut(nihia.buttons["UNDO"], on) 
      nihia.dataOut(nihia.buttons["REDO"], on) 
      nihia.dataOut(nihia.buttons["AUTO"], on) 
      nihia.dataOut(nihia.buttons["QUANTIZE"], on) 
      device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 64, 1, 0, 247])) # 'mute' & 'solo' button lights activated
      print (OUTPUT_MESSAGE)
      nihia.printText(0, HELLO_MESSAGE)
      time.sleep(timedelay)

     def OnMidiMsg(self, event): #listens for button or knob activity
         """Called first when a MIDI message is received. Set the event's handled property to True if you don't want further processing.
         (only raw data is included here: handled, timestamp, status, data1, data2, port, sysex, pmeflags)"""

         #tbuttons
         if (event.data1 == nihia.buttons["PLAY"]):
            event.handled = True
            transport.start() #play
            self.UpdateLEDs()
            ui.setHintMsg("Play/Pause")

         if (event.data1 == nihia.buttons["RESTART"]):
            event.handled = True
            #transport.globalTransport(midi.FPT_Save, 92)
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
            transport.globalTransport(midi.FPT_Snap, 48) #snap toggle
            self.UpdateLEDs()
            ui.setHintMsg("Snap")

            if ui.getSnapMode() == 3: # none
               nihia.printText(0, "Snap Off")
               time.sleep(timedelay)

            else:
               nihia.printText(0, "Snap On")
               time.sleep(timedelay)

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
            ui.escape() #escape key
            ui.setHintMsg("esc")
            nihia.printText(0, "esc")
            time.sleep(timedelay)


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

         if (event.data1 == nihia.buttons["ENCODER_BUTTON"]):
            event.handled = True
            ui.enter()
            ui.setHintMsg("enter")

         if (event.data1 == nihia.buttons["SHIFT+ENCODER_BUTTON"]):
            event.handled = True
            #ui.nextWindow()
            transport.globalTransport(midi.FPT_F8, 67)
            ui.setHintMsg("Plugin Picker")

         #mute and solo for mixer and channel rack
         if (event.data1 == nihia.buttons["MUTE"]):
            if ui.getFocused(0) == 1: #mixer volume control
               event.handled = True
               mixer.enableTrack(mixer.trackNumber()) #mute 
               self.UpdateOLED()
               ui.setHintMsg("Mute")
               
            elif ui.getFocused(1) == 1: # channel rack
               if channels.channelCount() >= 1: 
                  event.handled = True
                  channels.muteChannel(channels.channelNumber()) 
                  self.UpdateOLED()
                  ui.setHintMsg("Mute")
                  
         if (event.data1 ==  nihia.buttons["SOLO"]): 
            if ui.getFocused(0) == 1: #mixer volume control
               event.handled = True
               mixer.soloTrack(mixer.trackNumber()) #solo
               self.UpdateOLED()
               ui.setHintMsg("Solo")

            elif ui.getFocused(1) == 1: # channel rack
               if channels.channelCount() >= 2: 
                  event.handled = True
                  channels.soloChannel(channels.channelNumber()) 
                  self.UpdateOLED()
                  ui.setHintMsg("Solo")
               
         #4D controller
      
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

         #8 volume knobs for mixer & channel rack, 8 tracks at a time

         if ui.getFocused(0) == 1: #mixer volume control

            # VOLUME CONTROL

            xy = 1.25

            #knob 0
            if mixer.trackNumber() <= 126:
               if (event.data1 == nihia.knobs["KNOB_0A"]):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                   mixer.setTrackVolume((mixer.trackNumber() + 0), (x - knobinc) ) # volume values go down
                   nihia.printVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),3)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                   mixer.setTrackVolume((mixer.trackNumber() + 0), (x + knobinc) ) # volume values go up
                   nihia.printVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),3)))

            #knob 1
            if mixer.trackNumber() <= 125:
               if (event.data1 == nihia.knobs["KNOB_1A"]):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                   mixer.setTrackVolume((mixer.trackNumber() + 1), (x - knobinc) ) # volume values go down
                   nihia.printVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                   mixer.setTrackVolume((mixer.trackNumber() + 1), (x + knobinc) ) # volume values go up
                   nihia.printVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))

            #knob 2
            if mixer.trackNumber() <= 124:
               if (event.data1 == nihia.knobs["KNOB_2A"]):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 2))
                   mixer.setTrackVolume((mixer.trackNumber() + 2), (x - knobinc) ) # volume values go down
                   nihia.printVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 2))
                   mixer.setTrackVolume((mixer.trackNumber() + 2), (x + knobinc) ) # volume values go up
                   nihia.printVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))

            elif mixer.trackNumber() <= 127:    
               nihia.printText(3, ' ')
               nihia.printVol(3, 104)
               
            #knob 3
            if mixer.trackNumber() <= 123:
               if (event.data1 == nihia.knobs["KNOB_3A"]):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 3))
                   mixer.setTrackVolume((mixer.trackNumber() + 3), (x - knobinc) ) # volume values go down
                   nihia.printVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 3))
                   mixer.setTrackVolume((mixer.trackNumber() + 3), (x + knobinc) ) # volume values go up
                   nihia.printVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))

            elif mixer.trackNumber() <= 127:    
               nihia.printText(4, ' ')
               nihia.printVol(4, 104)

            #knob 4
            if mixer.trackNumber() <= 122:
               if (event.data1 == nihia.knobs["KNOB_4A"]):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 4))
                   mixer.setTrackVolume((mixer.trackNumber() + 4), (x - knobinc) ) # volume values go down
                   nihia.printVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 4))
                   mixer.setTrackVolume((mixer.trackNumber() + 4), (x + knobinc) ) # volume values go up
                   nihia.printVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))


            elif mixer.trackNumber() <= 127:    
               nihia.printText(5, ' ')
               nihia.printVol(5, 104)

            #knob 5
            if mixer.trackNumber() <= 121:
               if (event.data1 == nihia.knobs["KNOB_5A"]):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 5))
                   mixer.setTrackVolume((mixer.trackNumber() + 5), (x - knobinc) ) # volume values go down
                   nihia.printVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))

                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 5))
                   mixer.setTrackVolume((mixer.trackNumber() + 5), (x + knobinc) ) # volume values go up
                   nihia.printVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))

            elif mixer.trackNumber() <= 127:    
               nihia.printText(6, ' ')
               nihia.printVol(6, 104)     

            #knob 6
            if mixer.trackNumber() <= 120:
               if (event.data1 == nihia.knobs["KNOB_6A"]):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 6))
                   mixer.setTrackVolume((mixer.trackNumber() + 6), (x - knobinc) ) # volume values go down
                   nihia.printVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))

                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 6))
                   mixer.setTrackVolume((mixer.trackNumber() + 6), (x + knobinc) ) # volume values go up
                   nihia.printVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))


            elif mixer.trackNumber() <= 127:    
               nihia.printText(7, ' ')
               nihia.printVol(7, 104)     
                          
            #knob 8
            if mixer.trackNumber() <= 119:
               if (event.data1 == nihia.knobs["KNOB_7A"]):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 7))
                   mixer.setTrackVolume((mixer.trackNumber() + 7), (x - knobinc) ) # volume values go down
                   nihia.printVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))

                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 7))
                   mixer.setTrackVolume((mixer.trackNumber() + 7), (x + knobinc) ) # volume values go up
                   nihia.printVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))


            elif mixer.trackNumber() <= 127:    
               nihia.printText(8, ' ')     

            # MIXER PAN CONTROL 

            #sknob 1
            if mixer.trackNumber() <= 126:
               if (event.data1 == nihia.knobs["KNOB_0B"]):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                     mixer.setTrackPan((mixer.trackNumber() + 0), (x - knobinc) ) # volume values go down
                     nihia.printPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)

                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                     mixer.setTrackPan((mixer.trackNumber() + 0), (x + knobinc) ) # volume values go up
                     nihia.printPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)


            elif mixer.trackNumber() <= 127:    
               nihia.printVol(0, 104)

            #sknob 2
            if mixer.trackNumber() <= 125:
               if (event.data1 == nihia.knobs["KNOB_1B"]):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 1))
                     mixer.setTrackPan((mixer.trackNumber() + 1), (x - knobinc) ) # volume values go down
                     nihia.printPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)

                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 1))
                     mixer.setTrackPan((mixer.trackNumber() + 1), (x + knobinc) ) # volume values go up
                     nihia.printPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)


            elif mixer.trackNumber() <= 127:    
               nihia.printVol(1, 104)

            elif mixer.trackNumber() + 1 == mixer.trackNumber(126):
               mixer.setTrackVolume(126, 1)
               mixer.setTrackPan(126, 0)

            #sknob 3
            if mixer.trackNumber() <= 124:
               if (event.data1 == nihia.knobs["KNOB_2B"]):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                     mixer.setTrackPan((mixer.trackNumber() + 2), (x - knobinc) ) # volume values go down
                     nihia.printPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                     mixer.setTrackPan((mixer.trackNumber() + 2), (x + knobinc) ) # volume values go up
                     nihia.printPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)

            elif mixer.trackNumber() <= 127:    
               nihia.printVol(2, 104)

            #sknob 4
            if mixer.trackNumber() <= 123:
               if (event.data1 == nihia.knobs["KNOB_3B"]):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                     mixer.setTrackPan((mixer.trackNumber() + 3), (x - knobinc) ) # volume values go down
                     nihia.printPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                     mixer.setTrackPan((mixer.trackNumber() + 3), (x + knobinc) ) # volume values go up
                     nihia.printPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)

            elif mixer.trackNumber() <= 127:    
               nihia.printVol(3, 104)

            #sknob 5
            if mixer.trackNumber() <= 122:
               if (event.data1 == nihia.knobs["KNOB_4B"]):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                     mixer.setTrackPan((mixer.trackNumber() + 4), (x - knobinc) ) # volume values go down
                     nihia.printPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                     mixer.setTrackPan((mixer.trackNumber() + 4), (x + knobinc) ) # volume values go up
                     nihia.printPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)

            elif mixer.trackNumber() <= 127:    
               nihia.printVol(4, 104)

            #sknob 6
            if mixer.trackNumber() <= 121:
               if (event.data1 == nihia.knobs["KNOB_5B"]):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                     mixer.setTrackPan((mixer.trackNumber() + 5), (x - knobinc) ) # volume values go down
                     nihia.printPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                     mixer.setTrackPan((mixer.trackNumber() + 5), (x + knobinc) ) # volume values go up
                     nihia.printPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)

            elif mixer.trackNumber() <= 127:    
               nihia.printVol(5, 104)

            #sknob 7
            if mixer.trackNumber() <= 120:
               if (event.data1 == nihia.knobs["KNOB_6B"]):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                     mixer.setTrackPan((mixer.trackNumber() + 6), (x - knobinc) ) # volume values go down
                     nihia.printPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                     mixer.setTrackPan((mixer.trackNumber() + 6), (x + knobinc) ) # volume values go up
                     nihia.printPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)

            elif mixer.trackNumber() <= 127:    
               nihia.printVol(6, 104)

            #sknob 8
            if mixer.trackNumber() <= 119:
               if (event.data1 == nihia.knobs["KNOB_7B"]):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 7))
                     mixer.setTrackPan((mixer.trackNumber() + 7), (x - knobinc) ) # volume values go down
                     nihia.printPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 7))
                     mixer.setTrackPan((mixer.trackNumber() + 7), (x + knobinc) ) # volume values go up
                     nihia.printPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)

            elif mixer.trackNumber() <= 127:    
               nihia.printVol(7, 104)


         elif ui.getFocused(1) == 1: # channel rack

            # VOLUME CONTROL

            #knob 1
            if (event.data1 == nihia.knobs["KNOB_0A"]):
             event.handled = True  
             if event.data2 == left:
                x = (channels.getChannelVolume(channels.channelNumber() + 0))
                y = round(x,2)
                if channels.getChannelVolume(channels.channelNumber() + 0) != 0 :
                  channels.setChannelVolume((channels.channelNumber() + 0), (y - knobinc) ) # volume values go down
                  nihia.printVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0) ,2)))
       
             elif event.data2 == right:
                x = (channels.getChannelVolume(channels.channelNumber() + 0))
                y = round(x,2)
                channels.setChannelVolume((channels.channelNumber() + 0), (y + knobinc) ) # volume values go up
                nihia.printVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0) ,2)))

   
            #knob 2
            if (event.data1 == nihia.knobs["KNOB_1A"]):
             event.handled = True  
             if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 1))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 1) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 1), (y - knobinc) ) # volume values go down
                     nihia.printVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1) ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 1))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 1), (y + knobinc) ) # volume values go up
                  nihia.printVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1) ,2)))

            #knob 3
            if (event.data1 == nihia.knobs["KNOB_2A"]):
             event.handled = True  
             if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 2))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 2) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 2), (y - knobinc) ) # volume values go down
                     nihia.printVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2) ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 2))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 2), (y + knobinc) ) # volume values go up
                  nihia.printVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2) ,2)))

            #knob 4
            if (event.data1 == nihia.knobs["KNOB_3A"]):
             event.handled = True  
             if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 3))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 3) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 3), (y - knobinc) ) # volume values go down
                     nihia.printVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3) ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 3))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 3), (y + knobinc) ) # volume values go up
                  nihia.printVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3) ,2)))

            #knob 5
            if (event.data1 == nihia.knobs["KNOB_4A"]):
             event.handled = True  
             if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 4))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 4) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 4), (y - knobinc) ) # volume values go down
                     nihia.printVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4) ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 4))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 4), (y + knobinc) ) # volume values go up
                  nihia.printVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4) ,2)))

            #knob 6
            if (event.data1 == nihia.knobs["KNOB_5A"]):
             event.handled = True  
             if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 5))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 5) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 5), (y - knobinc) ) # volume values go down
                     nihia.printVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5) ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 5))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 5), (y + knobinc) ) # volume values go up
                  nihia.printVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5) ,2)))

            #knob 7
            if (event.data1 == nihia.knobs["KNOB_6A"]):
             event.handled = True  
             if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 6))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 6) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 6), (y - knobinc) ) # volume values go down
                     nihia.printVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6) ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 6))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 6), (y + knobinc) ) # volume values go up
                  nihia.printVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6) ,2)))

            #knob 8
            if (event.data1 == nihia.knobs["KNOB_7A"]):
             event.handled = True  
             if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 7))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 7) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 7), (y - knobinc) ) # volume values go down
                     nihia.printVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7) ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 7))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 7), (y + knobinc) ) # volume values go up
                  nihia.printVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7) ,2)))

            # PAN CONTROL

            #sknob 1
            if (event.data1 == nihia.knobs["KNOB_0B"]):
             event.handled = True  
             if event.data2 == left:
                x = (channels.getChannelPan(channels.channelNumber() + 0))
                channels.setChannelPan((channels.channelNumber() + 0), (x - knobinc) ) # pan values go down
                nihia.printPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)
  
             elif event.data2 == right:
                x = (channels.getChannelPan(channels.channelNumber() + 0))
                channels.setChannelPan((channels.channelNumber() + 0), (x + knobinc) ) # pan values go up
                nihia.printPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)

            #sknob 2
            if (event.data1 == nihia.knobs["KNOB_1B"]):
             event.handled = True  
             if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 1))
                  channels.setChannelPan((channels.channelNumber() + 1), (x - knobinc) ) # pan values go down
                  nihia.printPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)
      
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 1))
                  channels.setChannelPan((channels.channelNumber() + 1), (x + knobinc) ) # pan values go up
                  nihia.printPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)
   

            #sknob 3
            if (event.data1 == nihia.knobs["KNOB_2B"]):
             event.handled = True  
             if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 2))
                  channels.setChannelPan((channels.channelNumber() + 2), (x - knobinc) ) # pan values go down
                  nihia.printPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 2))
                  channels.setChannelPan((channels.channelNumber() + 2), (x + knobinc) ) # pan values go up
                  nihia.printPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)   

            #sknob 4
            if (event.data1 == nihia.knobs["KNOB_3B"]):
             event.handled = True  
             if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 3))
                  channels.setChannelPan((channels.channelNumber() + 3), (x - knobinc) ) # pan values go down
                  nihia.printPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 3))
                  channels.setChannelPan((channels.channelNumber() + 3), (x + knobinc) ) # pan values go up
                  nihia.printPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)  

            #sknob 5
            if (event.data1 == nihia.knobs["KNOB_4B"]):
             event.handled = True  
             if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 4))
                  channels.setChannelPan((channels.channelNumber() + 4), (x - knobinc) ) # pan values go down
                  nihia.printPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 4))
                  channels.setChannelPan((channels.channelNumber() + 4), (x + knobinc) ) # pan values go up
                  nihia.printPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)  

            #sknob 6
            if (event.data1 == nihia.knobs["KNOB_5B"]):
             event.handled = True  
             if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :  
               if event.data2 == left:
                   x = (channels.getChannelPan(channels.channelNumber() + 5))
                   channels.setChannelPan((channels.channelNumber() + 5), (x - knobinc) ) # pan values go down
                   nihia.printPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 5))
                  channels.setChannelPan((channels.channelNumber() + 5), (x + knobinc) ) # pan values go up
                  nihia.printPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)

            #sknob 7
            if (event.data1 == nihia.knobs["KNOB_6B"]):
             event.handled = True  
             if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 6))
                  channels.setChannelPan((channels.channelNumber() + 6), (x - knobinc) ) # pan values go down
                  nihia.printPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 6))
                  channels.setChannelPan((channels.channelNumber() + 6), (x + knobinc) ) # pan values go up
                  nihia.printPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)

            #sknob 8
            if (event.data1 == nihia.knobs["KNOB_7B"]):
             event.handled = True  
             if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 7))
                  channels.setChannelPan((channels.channelNumber() + 7), (x - knobinc) ) # pan values go down
                  nihia.printPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 7))
                  channels.setChannelPan((channels.channelNumber() + 7), (x + knobinc) ) # pan values go up
                  nihia.printPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)
 
     def UpdateLEDs(self): #controls all nights located within buttons
         """Function for device light communication (excluding OLED screen)"""

         if device.isAssigned():

            for a in [transport.isPlaying()]:
              if a == off: #not playing
                  nihia.dataOut(nihia.buttons["STOP"], on) #stop on

              elif a == on: #playing
                  nihia.dataOut(nihia.buttons["STOP"], off) #stop off

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
              if f == 3: #quantize off
                  nihia.dataOut(nihia.buttons["QUANTIZE"], off)
                  nihia.dataOut(nihia.buttons["AUTO"], off)

              elif f != 1: #quantize on
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

            if mixer.trackNumber() <= 126:
               nihia.printText(0, mixer.getTrackName(mixer.trackNumber() + 0))
               nihia.printVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),2)))
               nihia.printPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)
               

            if mixer.trackNumber() <= 125:
               nihia.printText(1, mixer.getTrackName(mixer.trackNumber() + 1))
               nihia.printVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))
               nihia.printPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)

            if mixer.trackNumber() <= 124:
               nihia.printText(2, mixer.getTrackName(mixer.trackNumber() + 2))
               nihia.printVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))
               nihia.printPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)

            if mixer.trackNumber() <= 123:
               nihia.printText(3, mixer.getTrackName(mixer.trackNumber() + 3))
               nihia.printVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))
               nihia.printPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)

            if mixer.trackNumber() <= 122:
               nihia.printText(4, mixer.getTrackName(mixer.trackNumber() + 4))
               nihia.printVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))
               nihia.printPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)

            if mixer.trackNumber() <= 121:
               nihia.printText(5, mixer.getTrackName(mixer.trackNumber() + 5))
               nihia.printVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))
               nihia.printPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)

            if mixer.trackNumber() <= 120:
               nihia.printText(6, mixer.getTrackName(mixer.trackNumber() + 6))
               nihia.printVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))
               nihia.printPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)

            if mixer.trackNumber() <= 119:
               nihia.printText(7, mixer.getTrackName(mixer.trackNumber() + 7))
               nihia.printVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))
               nihia.printPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)
               

            if mixer.isTrackEnabled(mixer.trackNumber()) == 1: #mute light off
               nihia.oled_mute_solo(nihia.buttons["MUTE"], off)
               nihia.dataOut(102, off)
               
            elif mixer.isTrackEnabled(mixer.trackNumber()) == 0: #mute light on
               nihia.oled_mute_solo(nihia.buttons["MUTE"], on)
               nihia.dataOut(102, on)


            if mixer.isTrackSolo(mixer.trackNumber()) == 0: #solo light off
               nihia.oled_mute_solo(nihia.buttons["SOLO"], off)
               nihia.dataOut(105, off)

            elif mixer.isTrackSolo(mixer.trackNumber()) == 1: #solo light on
               if mixer.isTrackMuted(mixer.trackNumber()) == 0:
                  nihia.oled_mute_solo(nihia.buttons["SOLO"], on)
                  nihia.dataOut(105, on)
               else:
                  nihia.oled_mute_solo(nihia.buttons["SOLO"], off)


        if ui.getFocused(1) == True: # channel rack
            
            nihia.printText(0, "C: " + channels.getChannelName(channels.channelNumber() + 0))

            if channels.channelCount() > 0 and channels.channelNumber() < (channels.channelCount()-0) :
               nihia.printText(1, "C: " + channels.getChannelName(channels.channelNumber() + 0))
               nihia.printVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0), 2)))
               nihia.printPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)
            else:
               nihia.printText(1, " ")
               nihia.printVol(0, 104)
               nihia.printPan(0, 104)

            if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :
               nihia.printText(1, "C: " + channels.getChannelName(channels.channelNumber() + 1))
               nihia.printVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1), 2)))
               nihia.printPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)
            else:
               nihia.printText(1, " ")
               nihia.printVol(1, 104)
               nihia.printPan(1, 104)

            if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :
               nihia.printText(2, "C: " + channels.getChannelName(channels.channelNumber() + 2))
               nihia.printVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2), 2)))
               nihia.printPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)
            else:
               nihia.printText(2, " ")
               nihia.printVol(2, 104)
               nihia.printPan(2, 104)
               
            if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :
               nihia.printText(3, "C: " + channels.getChannelName(channels.channelNumber() + 3))
               nihia.printVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3), 2)))
               nihia.printPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)
            else:
               nihia.printText(3, " ")
               nihia.printVol(3, 104)
               nihia.printPan(3, 104)
               
            if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :
               nihia.printText(4, "C: " + channels.getChannelName(channels.channelNumber() + 4))
               nihia.printVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4), 2)))
               nihia.printPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)
            else:
               nihia.printText(4, " ")
               nihia.printVol(4, 104)
               nihia.printPan(4, 104)
               
            if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :
               nihia.printText(5, "C: " + channels.getChannelName(channels.channelNumber() + 5))
               nihia.printVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5), 2)))
               nihia.printPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)
            else:
               nihia.printText(5, " ")
               nihia.printVol(5, 104)
               nihia.printPan(5, 104)
               
            if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :
               nihia.printText(6, "C: " + channels.getChannelName(channels.channelNumber() + 6))
               nihia.printVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6), 2)))
               nihia.printPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)
            else:
               nihia.printText(6, " ")
               nihia.printVol(6, 104)
               nihia.printPan(6, 104)
               
            if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :
               nihia.printText(7, "C: " + channels.getChannelName(channels.channelNumber() + 7))
               nihia.printVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7), 2)))
               nihia.printPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)
            else:
               nihia.printText(7, " ")
               nihia.printVol(7, 104)
               nihia.printPan(7, 104)


            if channels.isChannelMuted(channels.channelNumber()) == 0: #mute light off
               nihia.oled_mute_solo(nihia.buttons["MUTE"], off)
               nihia.dataOut(102, off)
                
            else: #mute light on
               nihia.oled_mute_solo(nihia.buttons["MUTE"], on)
               nihia.dataOut(102, on)

               
            if channels.channelCount() >= 2: 
               if channels.isChannelSolo(channels.channelNumber()) == 0: #solo light off
                  nihia.oled_mute_solo(nihia.buttons["SOLO"], off)
                  nihia.dataOut(105, off)
                  
               elif channels.isChannelSolo(channels.channelNumber()) == 1: #solo light on
                  if channels.isChannelMuted(channels.channelNumber()) == 0:
                     nihia.oled_mute_solo(nihia.buttons["SOLO"], on)
                     nihia.dataOut(105, on)
                  else:
                     nihia.oled_mute_solo(nihia.buttons["SOLO"], off)
                  

        if ui.getFocused(2) == True: # playlist

            #spells out 'Playlist' on tracks 1 through 8 on OLED
            nihia.printText(0, "Playlist")
            nihia.printText(1, " ")
            nihia.printText(2, " ")
            nihia.printText(3, " ")
            nihia.printText(4, " ")
            nihia.printText(5, " ")
            nihia.printText(6, " ")
            nihia.printText(7, " ")
            nihia.printVol(0, 104)
            nihia.printPan(0, 104)

        if ui.getFocused(3) == True: # Piano Roll - spells out 'Piano Roll' on tracks 1 through 8 on OLED
            nihia.printText(0, "PR: " + channels.getChannelName(channels.channelNumber() + 0))

            if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :
               nihia.printText(1, "C: " + channels.getChannelName(channels.channelNumber() + 1))
               nihia.printVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1), 2)))
               nihia.printPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)
            else:
               nihia.printText(1, " ")
               nihia.printVol(1, 104)
               nihia.printPan(1, 104)

            if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :
               nihia.printText(2, "C: " + channels.getChannelName(channels.channelNumber() + 2))
               nihia.printVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2), 2)))
               nihia.printPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)
            else:
               nihia.printText(2, " ")
               nihia.printVol(2, 104)
               nihia.printPan(2, 104)
               
            if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :
               nihia.printText(3, "C: " + channels.getChannelName(channels.channelNumber() + 3))
               nihia.printVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3), 2)))
               nihia.printPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)
            else:
               nihia.printText(3, " ")
               nihia.printVol(3, 104)
               nihia.printPan(3, 104)
               
            if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :
               nihia.printText(4, "C: " + channels.getChannelName(channels.channelNumber() + 4))
               nihia.printVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4), 2)))
               nihia.printPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)
            else:
               nihia.printText(4, " ")
               nihia.printVol(4, 104)
               nihia.printPan(4, 104)
               
            if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :
               nihia.printText(5, "C: " + channels.getChannelName(channels.channelNumber() + 5))
               nihia.printVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5), 2)))
               nihia.printPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)
            else:
               nihia.printText(5, " ")
               nihia.printVol(5, 104)
               nihia.printPan(5, 104)
               
            if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :
               nihia.printText(6, "C: " + channels.getChannelName(channels.channelNumber() + 6))
               nihia.printVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6), 2)))
               nihia.printPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)
            else:
               nihia.printText(6, " ")
               nihia.printVol(6, 104)
               nihia.printPan(6, 104)
               
            if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :
               nihia.printText(7, "C: " + channels.getChannelName(channels.channelNumber() + 7))
               nihia.printVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7), 2)))
               nihia.printPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)
            else:
               nihia.printText(7, " ")
               nihia.printVol(7, 104)
               nihia.printPan(7, 104)

            if channels.getChannelName(channels.channelNumber()) != channels.getChannelName(0):
               nihia.printVol(0, 104)
               nihia.printPan(0, 104)

            else:
               nihia.printVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0), 2)))
               nihia.printPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)
     
        if ui.getFocused(4) == True: # Browser
            #spells out 'Piano Roll' on tracks 1 through 8 on OLED
            nihia.printText(0, "Browser")
            nihia.printText(1, " ")
            nihia.printText(2, " ")
            nihia.printText(3, " ")
            nihia.printText(4, " ")
            nihia.printText(5, " ")
            nihia.printText(6, " ")
            nihia.printText(7, " ")
            nihia.printVol(0, 104)
            nihia.printPan(0, 104)     

        if ui.getFocused(5) == True: # Plugin
            #spells out 'Plugin' on tracks 1 through 8 on OLED
            nihia.printText(0, ui.getFocusedPluginName())
            nihia.printText(1, " ")
            nihia.printText(2, " ")
            nihia.printText(3, " ")
            nihia.printText(4, " ")
            nihia.printText(5, " ")
            nihia.printText(6, " ")
            nihia.printText(7, " ")
            nihia.printVol(0, 104)
            nihia.printPan(0, 104)     

     def OnRefresh(self, flags): #when something happens in FL Studio, update the keyboard lights & OLED
        """Function for when something changed that the script might want to respond to."""

        self.UpdateLEDs(), self.UpdateOLED()

     def OnUpdateBeatIndicator(Self, Value): #play light flashes to the tempo of the project
       """Function that is called when the beat indicator has changed."""

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

KompleteKontrolBase = KeyKompleteKontrolBase()

def OnInit():
   # command to initialize the protocol handshake
   KompleteKontrolBase.OnInit()


def OnRefresh(Flags):
   try:
      KompleteKontrolBase.OnRefresh(Flags)
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