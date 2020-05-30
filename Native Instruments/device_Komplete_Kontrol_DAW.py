# name=Komplete Kontrol DAW
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-m32/
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-a25-a49-a61/

# github for this script
# url=https://github.com/soundwrightpro/FLIN 

# FL Studio Forum
# https://forum.image-line.com/viewtopic.php?f=1994&t=225473
# script by Duwayne "Sound" Wright www.soundwrightpro.com and additional code from Hobyst

# MIT License

# Copyright (c) Duwayne Wright

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


#custom fl script modules
import patterns
import channels
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import ui
import screen
import midi
import utils
import time
import sys
import binascii
import math


#button values
playb = 16 # play button 
splayb = 17 # shift play button
recb = 18 # record button
srecb = 19 # shift record button
stopb = 20 # stop button
sstopb = 21 # shift stop button
loopb = 22 # loop button
metrob = 23 # metronome button
tempob = 24 # tempo button
undob = 32 # undo button
sundob = 33 # shift undo/redo button
quantizeb = 34 # quantize button
squantizeb = 35 # shift quantize button
muteb = 67 # mute button
solob = 68 # solo button

#knobs, spin to the left 127 and spin to the right 1
knob1 = 80
knob2 = 81
knob3 = 82
knob4 = 83
knob5 = 84
knob6 = 85
knob7 = 86
knob8 = 87
sknob1 = 88
sknob2 = 89
sknob3 = 90
sknob4 = 91
sknob5 = 92
sknob6 = 93
sknob7 = 94
sknob8 = 95

#multiknob
knobud = 48 # knob up data 2 = 127 and down data 2 = 1
knoblr = 50 # knob left data 2 = 127 and right data 2 = 1
knobsp = 52 # knob spin left 127 and spint right = 1
knobp = 96 # knob push
sknobp = 97 # knob shift+push

#data2 up down right left values
down = right = 1
up = left = 127

#knob increment value
knobinc = 0.01

#on/off values
on = 1
off = 0


#time delay for messages on screen
timedelay = 0.5


def KDataOut(data11, data12):
   
      """ Funtion that makes commmuication with the keyboard easier. By just entering the DATA1 and DATA2 of the MIDI message, 
          it composes the full message in forther to satisfy the syntax required by the midiOut functions, as well as the setting 
            the STATUS of the message to BF as expected.""" 

      convertmsg = [240, 191, data11, data12] 
      msgtom32 = bytearray(convertmsg)
      device.midiOutSysex(bytes(msgtom32))

def KPrntScrn(trkn, word):

      """ funtion that makes sendinig track titles to the OLED screen easier"""

      lettersh = [] 
      header = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 72, 0] #required header in message to tell m32 where to place track title

      n = 0
      m = 0

      letters = list(word) #convert word into letters in array

      if len(letters) <= 10:
         while n < len(letters): #convert letters in array to integer representing the Unicode character
            lettersh.append(ord(letters[n]))
            n += 1
      else:
         while n < 11: #convert letters in array to integer representing the Unicode character
            lettersh.append(ord(letters[n]))
            n += 1
         
      header.append(trkn) #adding track number to header at the end 

      while m < len(lettersh): #combining header array and unicode value array together; just makes it easier to send to device
         header.append(lettersh[m])
         m += 1 

      header.append(247) #tells m32, that's it that's the whole word
      
      device.midiOutSysex(bytes(header)) #send unicode values as bytes to OLED screen

def TranslateVolume(Value):

	return (math.exp(Value * math.log(11)) - 1) * 0.1   

def VolTodB(Value):

	Value = TranslateVolume(Value)
	return round(math.log10(Value) * 20, 1)

def KPrntScrnVol(trkn, vol):

      """ funtion that makes sendinig vol to the OLED screen easier"""
       
      volk = ""
      
      lettersh = [] 
      header = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 70, 0,] 

      p = 0
      n = 0
      m = 0

      vol==(float(vol))

      if vol == 0:
         volk = "- oo dB"
         letters = list(volk) 

         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1
 
      elif vol >= 0.01 and vol <= 2.00:
         
         #volj = u'%d%%  ' % round((vol*100),2) # returns volume display to percentage
         #lettersj = list(volj)
         #while m < len(volj):
         #   lettersh.append(ord(lettersj[m]))
         #   m += 1 #end of volume in percentage 

         volk = '%s dB' % VolTodB(vol) # volume displayed in dB from here
         letters = list(volk)
         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1 # end of volume in dB
         
      elif vol >= 103:
         volk = "N/A"
         letters = list(volk) 

         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1   

      header.append(trkn)
      
      while m < len(lettersh):
         header.append(lettersh[m])
         m += 1

      header.append(247)

      device.midiOutSysex(bytes(header))

def KPrntScrnPan(trkn, pan): 

      pan = round(pan,0)

      volk = ""

      lettersh = [] 
      header = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 71, 0,]

      p = 0
      n = 0
      m = 0

      header.append(trkn)
      

      if pan == 0:
         volk = "Centered"
         letters = list(volk) 

         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1 

      elif pan < 0:
         
         volk = u'%d%% Left' % round((pan),2)
         letters = list(volk) 
         
         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1

      elif pan > 0 and pan < 101:
         
         volk = u'%d%% Right' % round((pan),2)
         letters = list(volk) 
         
         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1 

      elif pan >= 103:
         volk = "N/A"
         letters = list(volk) 

         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1        

      while m < len(lettersh):
         header.append(lettersh[m])
         m += 1

      header.append(247)

      device.midiOutSysex(bytes(header))

def K_MS_OLED(lighttype, state): 

   header = [0, 240, 0, 33, 9, 0, 0, 68, 67, 1, 0]

   omute = [lighttype, state, 0]
   osolo = [lighttype, state, 0]

   n = 0

   if lighttype == muteb:
      while n < len(omute):
         header.append(omute[n])
         n += 1

   elif lighttype == solob:
      while n < len(osolo):
         header.append(osolo[n])
         n += 1

   header.append(247)
   device.midiOutSysex(bytes(header))


class TKompleteBase():

     def OnInit(self): #initializing 

      KDataOut(21, 1) # 'clear' light on
      KDataOut(32, 1) # 'undo' light on
      KDataOut(33, 1) # 'redo' light on

      device.midiOutSysex(bytes([240, 191, 35, 0, 0, 12, 1, 247])) # 'auto' light on
      device.midiOutSysex(bytes([191, 34, 1])) # 'quantize' light on
      device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 64, 1, 0, 247])) # 'mute' & 'solo' light on

      print ("Komplete Kontrol DAQ v3.3.7 by DUWAYNE 'SOUND' WRIGHT")

     def OnMidiIn(self, event): #listens for button or knob activity

         #tbuttons
         if (event.data1 == playb):
            event.handled = True
            transport.start() #play
            self.UpdateLEDs()
            ui.setHintMsg("Play/Pause")

         if (event.data1 == splayb):
            event.handled = True
            #transport.globalTransport(midi.FPT_Save, 92)
            transport.stop() #stop
            transport.start() #restart play at beginning
            ui.setHintMsg("Restart")
             
         if (event.data1 == recb):
            event.handled = True
            transport.record() #record
            self.UpdateLEDs()
            ui.setHintMsg("Record")

         if (event.data1 == stopb):
            event.handled = True
            transport.stop() #stop
            self.UpdateLEDs()
            ui.setHintMsg("Stop")

         if (event.data1 == loopb):
            event.handled = True
            transport.setLoopMode() #loop/pattern mode
            self.UpdateLEDs()
            ui.setHintMsg("Song / pattern mode")

            if transport.getLoopMode() == 0:
               KPrntScrn(0, "Pat. Mode")
               time.sleep(timedelay)

            elif transport.getLoopMode() == 1:
               KPrntScrn(0, "Song Mode")
               time.sleep(timedelay)
            

         if (event.data1 == metrob): # metronome/button
            event.handled = True
            transport.globalTransport(midi.FPT_Metronome, 110)
            self.UpdateLEDs()
            ui.setHintMsg("Metronome")

            if ui.isMetronomeEnabled() == 0: 
              KPrntScrn(0, "Metro Off")
              time.sleep(timedelay)

            elif ui.isMetronomeEnabled() == 1: 
              KPrntScrn(0, "Metro On")
              time.sleep(timedelay)
            
         if (event.data1 == tempob):
            event.handled = True
            transport.stop() #tap tempo
            #BPMv = str(round(mixer.getCurrentTempo()*0.001))+ " BPM"
            #KPrntScrn(0, BPMv)

         if (event.data1 == quantizeb):
            event.handled = True
            transport.globalTransport(midi.FPT_Snap, 48) #snap toggle
            self.UpdateLEDs()
            ui.setHintMsg("Snap")

            if ui.getSnapMode() == 3: # none
               KPrntScrn(0, "Snap Off")
               time.sleep(timedelay)

            else:
               KPrntScrn(0, "Snap On")
               time.sleep(timedelay)


         if (event.data1 == squantizeb):
            event.handled = True
            ui.snapMode(1) #snap toggle
            ui.setHintMsg("Snap Type")
            self.UpdateLEDs()
            
            snapmodevalue = ["Snap: Line", "Snap: Cell", "Snap: None", "S: 1/6 Step", "S: 1/4 Step", "S: 1/3 Step", "S: 1/2 Step", "Snap: Step", "S: 1/6 Beat", "S: 1/4 Beat", "S: 1/3 Beat", "S: 1/2 Beat", "Snap: Beat", "Snap: Bar"]

            if ui.getSnapMode() == 0: # line
              KPrntScrn(0, snapmodevalue[0])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 1: # cell
              KPrntScrn(0, snapmodevalue[1])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 3: # none
              KPrntScrn(0, snapmodevalue[2])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 4: # 1/6 step
              KPrntScrn(0, snapmodevalue[3])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 5: # 1/4 step
              KPrntScrn(0, snapmodevalue[4])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 6: # 1/3 step
              KPrntScrn(0, snapmodevalue[5])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 7: # 1/2 step
              KPrntScrn(0, snapmodevalue[6])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 8: # step
              KPrntScrn(0, snapmodevalue[7])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 9: # 1/6 beat
              KPrntScrn(0, snapmodevalue[8])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 10: # 1/4 beat
              KPrntScrn(0, snapmodevalue[9])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 11: # 1/3 beat
              KPrntScrn(0, snapmodevalue[10])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 12: # 1/2 beat
              KPrntScrn(0, snapmodevalue[11])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 13: # beat
              KPrntScrn(0, snapmodevalue[12])
              time.sleep(timedelay)

            elif ui.getSnapMode() == 14: # bar
              KPrntScrn(0, snapmodevalue[13])
              time.sleep(timedelay)


         if (event.data1 == srecb):
            event.handled = True
            transport.globalTransport(midi.FPT_CountDown, 115) #countdown before recording
            ui.setHintMsg("Countdown before recording")
            
            if ui.isPrecountEnabled() == 1: 
               KPrntScrn(0, "Cnt-in On")
               time.sleep(timedelay)
            else:
               KPrntScrn(0, "Cnt-in Off")
               time.sleep(timedelay)

         if (event.data1 == sstopb):
            event.handled = True
            ui.escape() #escape key
            ui.setHintMsg("esc")

         if (event.data1 == undob):
            event.handled = True
            general.undoUp() #undo 
            ui.setHintMsg(ui.getHintMsg())

         if (event.data1 == sundob):
            event.handled = True
            general.undo() #redo
            ui.setHintMsg(ui.getHintMsg())

         if (event.data1 == tempob):
            event.handled = True
            transport.globalTransport(midi.FPT_TapTempo, 106) #tap tempo

         if (event.data1 == knobp):
            event.handled = True
            ui.enter()
            ui.setHintMsg("enter")

         if (event.data1 == sknobp):
            event.handled = True
            ui.nextWindow()
            ui.setHintMsg("Next Window")

         #mute and solo for mixer and channel rack
         if (event.data1 == muteb):
            if ui.getFocused(0) == 1: #mixer volume control
               event.handled = True
               mixer.enableTrack(mixer.trackNumber()) #mute 
               self.UpdateOLED()
               ui.setHintMsg("Mute")
               

            elif (ui.getFocused(0) == 0) == True: # channel rack
               if channels.channelCount() >= 1: 
                  event.handled = True
                  channels.muteChannel(channels.channelNumber()) 
                  self.UpdateOLED()
                  ui.setHintMsg("Mute")
                  
               

         if (event.data1 == solob): 
            if ui.getFocused(0) == 1: #mixer volume control
               event.handled = True
               mixer.soloTrack(mixer.trackNumber()) #solo
               self.UpdateOLED()
               ui.setHintMsg("Solo")

            elif (ui.getFocused(0) == 0) == True: # channel rack
               if channels.channelCount() >= 2: 
                  event.handled = True
                  channels.soloChannel(channels.channelNumber()) 
                  self.UpdateOLED()
                  ui.setHintMsg("Solo")
               



         #4D controller
         if (event.data1 == knobsp) & (event.data2 == right): #4d encoder spin right 
            event.handled = True
            ui.jog(1)
         elif (event.data1 == knobsp) & (event.data2 == left): #4d encoder spin left
            event.handled = True
            ui.jog(-1)
         
         if (event.data1 == knoblr) & (event.data2 == right): #4d encoder push right
            event.handled = True
            transport.globalTransport(midi.FPT_Right, 1)
         elif (event.data1 == knoblr) & (event.data2 == left): #4d encoder push left
            event.handled = True
            transport.globalTransport(midi.FPT_Left, 1)

         if (event.data1 == knobud) & (event.data2 == up): #4d encoder push up
            event.handled = True
            transport.globalTransport(midi.FPT_Up, 1)
         elif (event.data1 == knobud) & (event.data2 == down): #4d encoder push down
            event.handled = True
            transport.globalTransport(midi.FPT_Down, 1)

         #8 volume knobs for mixer & channel rack, 8 tracks at a time


         if ui.getFocused(0) == 1: #mixer volume control

            # VOLUME CONTROL

            xy = 1.25

            #knob 1
            if mixer.trackNumber() <= 126:
               if (event.data1 == knob1):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 0), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),3)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 0), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),3)))


            #knob 2
            if mixer.trackNumber() <= 125:
               if (event.data1 == knob2):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 1), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 1), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))


            #knob 3
            if mixer.trackNumber() <= 124:
               if (event.data1 == knob3):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 2))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 2), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 2))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 2), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))

            elif mixer.trackNumber() <= 127:    
               KPrntScrn(3, ' ')
               KPrntScrnVol(3, 104)
               

            #knob 4
            if mixer.trackNumber() <= 123:
               if (event.data1 == knob4):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 3))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 3), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 3))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 3), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))

            elif mixer.trackNumber() <= 127:    
               KPrntScrn(4, ' ')
               KPrntScrnVol(4, 104)

            #knob5
            if mixer.trackNumber() <= 122:
               if (event.data1 == knob5):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 4))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 4), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))
                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 4))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 4), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))


            elif mixer.trackNumber() <= 127:    
               KPrntScrn(5, ' ')
               KPrntScrnVol(5, 104)

            #knob 6
            if mixer.trackNumber() <= 121:
               if (event.data1 == knob6):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 5))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 5), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))

                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 5))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 5), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))

            elif mixer.trackNumber() <= 127:    
               KPrntScrn(6, ' ')
               KPrntScrnVol(6, 104)     

            #knob 7
            if mixer.trackNumber() <= 120:
               if (event.data1 == knob7):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 6))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 6), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))

                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 6))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 6), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))


            elif mixer.trackNumber() <= 127:    
               KPrntScrn(7, ' ')
               KPrntScrnVol(7, 104)     
                          
            #knob 8
            if mixer.trackNumber() <= 119:
               if (event.data1 == knob8):
                event.handled = True
                if event.data2 == left:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 7))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 7), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))

                
                elif event.data2 == right:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 7))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 7), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))


            elif mixer.trackNumber() <= 127:    
               KPrntScrn(8, ' ')     
                          
               
            # MIXER PAN CONTROL 

            #sknob 1
            if mixer.trackNumber() <= 126:
               if (event.data1 == sknob1):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 0), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)

                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 0), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)


            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(0, 104)

            #sknob 2
            if mixer.trackNumber() <= 125:
               if (event.data1 == sknob2):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 1))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 1), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)

                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 1))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 1), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)


            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(1, 104)

            elif mixer.trackNumber() + 1 == mixer.trackNumber(126):
               mixer.setTrackVolume(126, 1)
               mixer.setTrackPan(126, 0)

            #sknob 3
            if mixer.trackNumber() <= 124:
               if (event.data1 == sknob3):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 2), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 2), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(2, 104)

            #sknob 4
            if mixer.trackNumber() <= 123:
               if (event.data1 == sknob4):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 3), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 3), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(3, 104)

            #sknob 5
            if mixer.trackNumber() <= 122:
               if (event.data1 == sknob5):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 4), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 4), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(4, 104)

            #sknob 6
            if mixer.trackNumber() <= 121:
               if (event.data1 == sknob6):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 5), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 5), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(5, 104)

            #sknob 7
            if mixer.trackNumber() <= 120:
               if (event.data1 == sknob7):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 6), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 6), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(6, 104)

            #sknob 8
            if mixer.trackNumber() <= 119:
               if (event.data1 == sknob8):
                  event.handled = True
                  if event.data2 == left:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 7))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 7), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)
                
                  elif event.data2 == right:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 7))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 7), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(7, 104)


         elif ui.getFocused(0) == 0: # channel rack

            # VOLUME CONTROL

            xy = 1

            #knob 1
            if (event.data1 == knob1):
             event.handled = True  
             if event.data2 == left:
                x = (channels.getChannelVolume(channels.channelNumber() + 0))
                y = round(x,2)
                if channels.getChannelVolume(channels.channelNumber() + 0) != 0 :
                  channels.setChannelVolume((channels.channelNumber() + 0), (y - knobinc) ) # volume values go down
                  KPrntScrnVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0) / xy ,2)))
       
             elif event.data2 == right:
                x = (channels.getChannelVolume(channels.channelNumber() + 0))
                y = round(x,2)
                channels.setChannelVolume((channels.channelNumber() + 0), (y + knobinc) ) # volume values go up
                KPrntScrnVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0) / xy ,2)))

   
            #knob 2
            if (event.data1 == knob2):
             event.handled = True  
             if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 1))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 1) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 1), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1) / xy ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 1))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 1), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1) / xy ,2)))

            #knob 3
            if (event.data1 == knob3):
             event.handled = True  
             if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 2))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 2) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 2), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2) / xy ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 2))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 2), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2) / xy ,2)))

            #knob 4
            if (event.data1 == knob4):
             event.handled = True  
             if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 3))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 3) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 3), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3) / xy ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 3))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 3), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3) / xy ,2)))

            #knob 5
            if (event.data1 == knob5):
             event.handled = True  
             if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 4))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 4) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 4), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4) / xy ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 4))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 4), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4) / xy ,2)))

            #knob 6
            if (event.data1 == knob6):
             event.handled = True  
             if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 5))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 5) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 5), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5) / xy ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 5))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 5), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5) / xy ,2)))

            #knob 7
            if (event.data1 == knob7):
             event.handled = True  
             if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 6))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 6) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 6), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6) / xy ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 6))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 6), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6) / xy ,2)))

            #knob 8
            if (event.data1 == knob8):
             event.handled = True  
             if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :  
               if event.data2 == left:
                  x = (channels.getChannelVolume(channels.channelNumber() + 7))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 7) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 7), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7) / xy ,2)))
                
               elif event.data2 == right:
                  x = (channels.getChannelVolume(channels.channelNumber() + 7))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 7), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7) / xy ,2)))

            # PAN CONTROL

            #sknob 1
            if (event.data1 == sknob1):
             event.handled = True  
             if event.data2 == left:
                x = (channels.getChannelPan(channels.channelNumber() + 0))
                #round(x,2)
                channels.setChannelPan((channels.channelNumber() + 0), (x - knobinc) ) # pan values go down
                KPrntScrnPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)
  
             elif event.data2 == right:
                x = (channels.getChannelPan(channels.channelNumber() + 0))
                #round(x,2)
                channels.setChannelPan((channels.channelNumber() + 0), (x + knobinc) ) # pan values go up
                KPrntScrnPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)

            #sknob 2
            if (event.data1 == sknob2):
             event.handled = True  
             if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 1))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 1), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)
      
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 1))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 1), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)
   

            #sknob 3
            if (event.data1 == sknob3):
             event.handled = True  
             if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 2))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 2), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 2))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 2), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)   

            #sknob 4
            if (event.data1 == sknob4):
             event.handled = True  
             if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 3))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 3), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 3))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 3), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)  

            #sknob 5
            if (event.data1 == sknob5):
             event.handled = True  
             if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 4))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 4), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 4))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 4), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)  

            #sknob 6
            if (event.data1 == sknob6):
             event.handled = True  
             if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :  
               if event.data2 == left:
                   x = (channels.getChannelPan(channels.channelNumber() + 5))
                  #round(x,2)
                   channels.setChannelPan((channels.channelNumber() + 5), (x - knobinc) ) # pan values go down
                   KPrntScrnPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 5))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 5), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)

            #sknob 7
            if (event.data1 == sknob7):
             event.handled = True  
             if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 6))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 6), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 6))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 6), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)

            #sknob 8
            if (event.data1 == sknob8):
             event.handled = True  
             if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :  
               if event.data2 == left:
                  x = (channels.getChannelPan(channels.channelNumber() + 7))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 7), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)
                
               elif event.data2 == right:
                  x = (channels.getChannelPan(channels.channelNumber() + 7))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 7), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)
 
     def UpdateLEDs(self): #controls all nights located within buttons

         playstatus = [transport.isPlaying()]
         recstatus = [transport.isRecording()]
         loopstatus = [transport.getLoopMode()]
         metrostatus = [ui.isMetronomeEnabled()]
         prestatus = [ui.isPrecountEnabled()]
         quanstatus = [ui.getSnapMode()]

         if device.isAssigned():

            for a in playstatus:
              if a == 0: #not playing
                  KDataOut(stopb, on) #stop on

              elif a == 1: #playing
                  KDataOut(stopb, off) #stop off

            for b in recstatus:
               if b == 0: #not recording
                  KDataOut(recb, off)

               elif b == 1: #recording
                  KDataOut(recb, on)

            for c in loopstatus:
               if c == 0: #loop mood
                  KDataOut(loopb, on)

               elif c == 1: #playlist mode
                  KDataOut(loopb, off)

            for d in metrostatus:
               if d == 0: #metro off
                  KDataOut(metrob, off)

               elif d == 1: #metro on
                  KDataOut(metrob, on)

            for e in prestatus:
              if e == 0: #pre count on
                  KDataOut(srecb, off)

              elif e == 1: #pre count off
                  KDataOut(srecb, on) 

            for f in quanstatus:
              if f == 3: #quantize off
                  KDataOut(quantizeb, off)

              elif f != 1: #quantize on
                  KDataOut(quantizeb, on)

            for g in playstatus:
              if transport.isRecording() == 0 & transport.isPlaying() == 1: 
                  if g == 0: #play off
                     KDataOut(playb, off)
                  elif g != 1: #play on
                     KDataOut(playb, on)
              elif g == 0: #play off: 
                  KDataOut(playb, off)

     def UpdateOLED(self): #controls OLED screen messages

        if ui.getFocused(0) == 1: #mixer volume control

            xy = 1.25

            if mixer.trackNumber() <= 126:
               KPrntScrn(0, "M: " + mixer.getTrackName(mixer.trackNumber() + 0))
               KPrntScrnVol(channels.channelNumber() + 0, (round(channels.getChannelVolume(channels.channelNumber() + 0) / xy ,2)))
               KPrntScrnVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),2)))
               KPrntScrnPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)

            if mixer.trackNumber() <= 125:
               KPrntScrn(1, "M: " + mixer.getTrackName(mixer.trackNumber() + 1))
               KPrntScrnVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))
               KPrntScrnPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)

            if mixer.trackNumber() <= 124:
               KPrntScrn(2, "M: " + mixer.getTrackName(mixer.trackNumber() + 2))
               KPrntScrnVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))
               KPrntScrnPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)

            if mixer.trackNumber() <= 123:
               KPrntScrn(3, "M: " + mixer.getTrackName(mixer.trackNumber() + 3))
               KPrntScrnVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))
               KPrntScrnPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)

            if mixer.trackNumber() <= 122:
               KPrntScrn(4, "M: " + mixer.getTrackName(mixer.trackNumber() + 4))
               KPrntScrnVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))
               KPrntScrnPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)

            if mixer.trackNumber() <= 121:
               KPrntScrn(5, "M: " + mixer.getTrackName(mixer.trackNumber() + 5))
               KPrntScrnVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))
               KPrntScrnPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)

            if mixer.trackNumber() <= 120:
               KPrntScrn(6, "M: " + mixer.getTrackName(mixer.trackNumber() + 6))
               KPrntScrnVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))
               KPrntScrnPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)

            if mixer.trackNumber() <= 119:
               KPrntScrn(7, "M: " + mixer.getTrackName(mixer.trackNumber() + 7))
               KPrntScrnVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))
               KPrntScrnPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)
               

            if mixer.isTrackEnabled(mixer.trackNumber()) == 1: #mute light off
               K_MS_OLED(muteb, off)
               KDataOut(102, off)
               
            elif mixer.isTrackEnabled(mixer.trackNumber()) == 0: #mute light on
               K_MS_OLED(muteb, on)
               KDataOut(102, on)

            if (mixer.isTrackSolo(mixer.trackNumber()) == 0) == True: #solo light off
               K_MS_OLED(solob, off)
               KDataOut(105, off)

            elif (mixer.isTrackSolo(mixer.trackNumber()) == 1) == True: #solo light on
               K_MS_OLED(solob, on)
               KDataOut(105, on)

        if ui.getFocused(1) == 1: # channel rack

            xy = 1
            
            KPrntScrn(0, "C: " + channels.getChannelName(channels.channelNumber() + 0))

            if channels.channelCount() > 0 and channels.channelNumber() < (channels.channelCount()-0) :
               KPrntScrn(1, "C: " + channels.getChannelName(channels.channelNumber() + 0))
               KPrntScrnVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0) / xy ,2)))
               KPrntScrnPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)
            else:
               KPrntScrn(1, " ")
               KPrntScrnVol(0, 104)
               KPrntScrnPan(0, 104)

            if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :
               KPrntScrn(1, "C: " + channels.getChannelName(channels.channelNumber() + 1))
               KPrntScrnVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1) / xy ,2)))
               KPrntScrnPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)
            else:
               KPrntScrn(1, " ")
               KPrntScrnVol(1, 104)
               KPrntScrnPan(1, 104)

            if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :
               KPrntScrn(2, "C: " + channels.getChannelName(channels.channelNumber() + 2))
               KPrntScrnVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2) / xy ,2)))
               KPrntScrnPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)
            else:
               KPrntScrn(2, " ")
               KPrntScrnVol(2, 104)
               KPrntScrnPan(2, 104)
               
            if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :
               KPrntScrn(3, "C: " + channels.getChannelName(channels.channelNumber() + 3))
               KPrntScrnVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3) / xy ,2)))
               KPrntScrnPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)
            else:
               KPrntScrn(3, " ")
               KPrntScrnVol(3, 104)
               KPrntScrnPan(3, 104)
               
            if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :
               KPrntScrn(4, "C: " + channels.getChannelName(channels.channelNumber() + 4))
               KPrntScrnVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4) / xy ,2)))
               KPrntScrnPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)
            else:
               KPrntScrn(4, " ")
               KPrntScrnVol(4, 104)
               KPrntScrnPan(4, 104)
               
            if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :
               KPrntScrn(5, "C: " + channels.getChannelName(channels.channelNumber() + 5))
               KPrntScrnVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5) / xy ,2)))
               KPrntScrnPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)
            else:
               KPrntScrn(5, " ")
               KPrntScrnVol(5, 104)
               KPrntScrnPan(5, 104)
               
            if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :
               KPrntScrn(6, "C: " + channels.getChannelName(channels.channelNumber() + 6))
               KPrntScrnVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6) / xy ,2)))
               KPrntScrnPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)
            else:
               KPrntScrn(6, " ")
               KPrntScrnVol(6, 104)
               KPrntScrnPan(6, 104)
               
            if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :
               KPrntScrn(7, "C: " + channels.getChannelName(channels.channelNumber() + 7))
               KPrntScrnVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7) / xy ,2)))
               KPrntScrnPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)
            else:
               KPrntScrn(7, " ")
               KPrntScrnVol(7, 104)
               KPrntScrnPan(7, 104)


            if (channels.isChannelMuted(channels.channelNumber()) == 0) == True: #mute light off
               K_MS_OLED(muteb, off)
               KDataOut(102, off)
                
            else: #mute light on
               K_MS_OLED(muteb, on)
               KDataOut(102, on)

               
            if channels.channelCount() >= 2: 
               if channels.isChannelSolo(channels.channelNumber()) == 0: #solo light off
                  K_MS_OLED(solob, off)
                  KDataOut(105, off)
                  
               elif channels.isChannelSolo(channels.channelNumber()) == 1: #solo light on
                  K_MS_OLED(solob, on)
                  KDataOut(105, on)
                  

        if ui.getFocused(2) == 1: # playlist
            #spells out 'Playlist' on tracks 1 through 8 on OLED
            KPrntScrn(0, "Playlist")
            KPrntScrn(1, "Playlist")
            KPrntScrn(2, "Playlist")
            KPrntScrn(3, "Playlist")
            KPrntScrn(4, "Playlist")
            KPrntScrn(5, "Playlist")
            KPrntScrn(6, "Playlist")
            KPrntScrn(7, "Playlist")
            KPrntScrnVol(0, 104)
            KPrntScrnPan(0, 104)

        if ui.getFocused(3) == 1: # Piano Roll
            #spells out 'Piano Roll' on tracks 1 through 8 on OLED

            xy = 1
            
            KPrntScrn(0, "PR: " + channels.getChannelName(channels.channelNumber() + 0))

            if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :
               KPrntScrn(1, "C: " + channels.getChannelName(channels.channelNumber() + 1))
               KPrntScrnVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1) / xy ,2)))
               KPrntScrnPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)
            else:
               KPrntScrn(1, " ")
               KPrntScrnVol(1, 104)
               KPrntScrnPan(1, 104)

            if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :
               KPrntScrn(2, "C: " + channels.getChannelName(channels.channelNumber() + 2))
               KPrntScrnVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2) / xy ,2)))
               KPrntScrnPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)
            else:
               KPrntScrn(2, " ")
               KPrntScrnVol(2, 104)
               KPrntScrnPan(2, 104)
               
            if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :
               KPrntScrn(3, "C: " + channels.getChannelName(channels.channelNumber() + 3))
               KPrntScrnVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3) / xy ,2)))
               KPrntScrnPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)
            else:
               KPrntScrn(3, " ")
               KPrntScrnVol(3, 104)
               KPrntScrnPan(3, 104)
               
            if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :
               KPrntScrn(4, "C: " + channels.getChannelName(channels.channelNumber() + 4))
               KPrntScrnVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4) / xy ,2)))
               KPrntScrnPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)
            else:
               KPrntScrn(4, " ")
               KPrntScrnVol(4, 104)
               KPrntScrnPan(4, 104)
               
            if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :
               KPrntScrn(5, "C: " + channels.getChannelName(channels.channelNumber() + 5))
               KPrntScrnVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5) / xy ,2)))
               KPrntScrnPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)
            else:
               KPrntScrn(5, " ")
               KPrntScrnVol(5, 104)
               KPrntScrnPan(5, 104)
               
            if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :
               KPrntScrn(6, "C: " + channels.getChannelName(channels.channelNumber() + 6))
               KPrntScrnVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6) / xy ,2)))
               KPrntScrnPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)
            else:
               KPrntScrn(6, " ")
               KPrntScrnVol(6, 104)
               KPrntScrnPan(6, 104)
               
            if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :
               KPrntScrn(7, "C: " + channels.getChannelName(channels.channelNumber() + 7))
               KPrntScrnVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7) / xy ,2)))
               KPrntScrnPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)
            else:
               KPrntScrn(7, " ")
               KPrntScrnVol(7, 104)
               KPrntScrnPan(7, 104)

            if channels.getChannelName(channels.channelNumber()) != channels.getChannelName(0):
               KPrntScrnVol(0, 104)
               KPrntScrnPan(0, 104)

            else:
               KPrntScrnVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0) / xy ,2)))
               KPrntScrnPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)
     
        if ui.getFocused(4) == 1: # Browser
            #spells out 'Piano Roll' on tracks 1 through 8 on OLED
            KPrntScrn(0, "Browser")
            KPrntScrn(1, "Browser")
            KPrntScrn(2, "Browser")
            KPrntScrn(3, "Browser")
            KPrntScrn(4, "Browser")
            KPrntScrn(5, "Browser")
            KPrntScrn(6, "Browser")
            KPrntScrn(7, "Browser")
            KPrntScrnVol(0, 104)
            KPrntScrnPan(0, 104)     

     def OnRefresh(self, flags): #when something happens in FL Studio, update the keyboard lights & OLED

        self.UpdateLEDs(), self.UpdateOLED()

     def OnUpdateBeatIndicator(Self, Value): #play light flashes to the tempo of the project

       if transport.isRecording() == 0:
      	 if Value == 1:
      	    KDataOut(playb, on) #play light bright
      	 elif Value == 2:
      	    KDataOut(playb, on) #play light bright
      	 elif Value == 0:
      	    KDataOut(playb, off) #play light dim

       elif transport.isRecording() == 1:
            KDataOut(playb, on)
            if Value == 1:
               KDataOut(recb, on) #play light bright
            elif Value == 2:
               KDataOut(recb, on) #play light bright
            elif Value == 0:
               KDataOut(recb, off) #play light dim  


KompleteBase = TKompleteBase()

def OnInit():
   # command to initialize the protocol handshake
   KDataOut(1, 1), KompleteBase.OnInit()

def OnRefresh(Flags):
   KompleteBase.OnRefresh(Flags)

def OnUpdateBeatIndicator(Value):
	KompleteBase.OnUpdateBeatIndicator(Value)

def OnMidiIn(event):
	KompleteBase.OnMidiIn(event)

def OnDeInit():
   if ui.isClosing():
      # Command to stop the protocol
      KDataOut(2, 1), KompleteBase.OnDeInit()	