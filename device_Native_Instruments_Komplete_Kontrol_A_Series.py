# name=Native Instruments KOMPLETE KONTROL A-Series
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-m32/

# github for this script
# url=https://github.com/soundwrightpro/FLIN 

# FL Studio Forum
# https://forum.image-line.com/viewtopic.php?f=1994&t=225473
# script by Duwayne "Sound" Wright www.soundwrightpro.com and additional code from Hobyst


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
knobsp = 52 # knob spin left 127 and spint right = 1
knoblr = 50 # knob left data 2 = 127 and right data 2 = 1
knobud = 48 # knob up data 2 = 127 and down data 2 = 1
knobp = 96 # knob push
sknobp = 97 # knob shift+push

#data2 right left values
right = 1
up = 127
left = 127
down = 1

#knob increment value
knobinc = 0.01

#on/off values
on = 1
off = 0



#function to make talking to the keyboard less annoying
def KDataOut(data11, data12):
   
      """ Funtion that makes commmuication with the keyboard easier. By just entering the DATA1 and DATA2 of the MIDI message, 
          it composes the full message in forther to satisfy the syntax required by the midiOut functions, as well as the setting 
            the STATUS of the message to BF as expected.""" 

      convertmsg = [240, 191, data11, data12] 
      msgtom32 = bytearray(convertmsg)
      device.midiOutSysex(bytes(msgtom32))
      device.midiOutSysex(bytes([240, 191, 31, 1]))
      
      

def KPrntScrn(trkn, word):

      """ funtion that makes sendinig track titles to the OLED screen easier"""

      lettersh = [] 
      header = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, 72, 0] #required header in message to tell m32 where to place track title

      n = 0
      m = 0

      letters = list(word) #convert word into letters in array

      if len(letters) <= 11:
         while n < len(letters): #convert letters in array to integer representing the Unicode character
            lettersh.append(ord(letters[n]))
            n += 1
      else:
         while n < 12: #convert letters in array to integer representing the Unicode character
            lettersh.append(ord(letters[n]))
            n += 1
         
      header.append(trkn) #adding track number to header at the end 

      while m < len(lettersh): #combining header array and unicode value array together; just makes it easier to send to device
         header.append(lettersh[m])
         m += 1 

      header.append(247) #tells m32, that's it that's the whole word
      
      device.midiOutSysex(bytes(header)) #send unicode values as bytes to OLED screen


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
         
         
         
         volk == '%d%%' % round((vol*100),2))

         
         #vol =  math.log(vol/1)
         #print("step A: ", vol)

         #vol = vol*20
         #print("step B: ", vol)

         #volk = '%s dB' % round(vol,1)
         #print("final: ", vol)

         letters = list(volk)
         print(letters)

         
         while n < len(volk):
            lettersh.append(ord(letters[n]))
            n += 1

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


class TKompleteBase():

     def OnInit(self):

         KDataOut(21, 1) #clear light on
         KDataOut(32, 1) #undo light on
         KDataOut(33, 1) #redo light on

         device.midiOutSysex(bytes([0xF0, 0xBF, 0x23, 0x00, 0x00, 0x0C, 1, 0xF7])) # auto button light fix
         device.midiOutSysex(bytes([0xBF, 0x22, 0x01])) #quantize light fix
         device.midiOutSysex(bytes([0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, 0x40, 0x01, 0x00, 0xF7])) # mute and solo light bug fix

         print("Join the DISCORD https://discord.gg/GeTTWBV to report issues in the bug channel")    
         print("Komplete Kontrol A-Series Script - V3.0.5  by Duwayne 'Sound' Wright.")


     def OnMidiIn(self, event):

         #tbuttons
         if (event.data1 == playb):
            transport.start() #play
            self.UpdateLEDs()
            ui.setHintMsg("Play/Pause")

         if (event.data1 == splayb):
            transport.globalTransport(midi.FPT_Save, 92)
            ui.setHintMsg("Save")
             
         if (event.data1 == recb):
            transport.record() #record
            self.UpdateLEDs()
            ui.setHintMsg("Record")

         if (event.data1 == stopb):
            transport.stop() #stop
            self.UpdateLEDs()
            ui.setHintMsg("Stop")

         if (event.data1 == loopb):
            transport.setLoopMode() #loop/pattern mode
            self.UpdateLEDs()
            ui.setHintMsg("Song / pattern mode")
            

         if (event.data1 == metrob): # metronome/button
            transport.globalTransport(midi.FPT_Metronome, 110)
            self.UpdateLEDs()
            ui.setHintMsg("Metronome")
            
         if (event.data1 == tempob):
            transport.stop() #tap tempo

         if (event.data1 == quantizeb):
            transport.globalTransport(midi.FPT_Snap, 48) #snap toggle
            ui.setHintMsg("Quantize")

         if (event.data1 == squantizeb):
            ui.snapMode(1) #snap toggle
            ui.setHintMsg("Snap Type")  

         if (event.data1 == srecb):
            transport.globalTransport(midi.FPT_CountDown, 115) #countdown before recording
            ui.setHintMsg("Countdown before recording") 

         if (event.data1 == sstopb):
            ui.escape() #escape key
            ui.setHintMsg("esc")

         if (event.data1 == undob):
            general.undoUp() #undo 
            ui.setHintMsg(ui.getHintMsg())

         if (event.data1 == sundob):
            general.undo() #redo
            ui.setHintMsg(ui.getHintMsg())

         if (event.data1 == squantizeb):
            transport.globalTransport(midi.FPT_SnapMode, 49, event.pmeFlags) #snap toggle
            self.UpdateLEDs()

         if (event.data1 == tempob):
            transport.globalTransport(midi.FPT_TapTempo, 106) #tap tempo

         if (event.data1 == knobp):
            ui.enter()
            ui.setHintMsg("enter")

         if (event.data1 == sknobp):
            ui.nextWindow()
            ui.setHintMsg("Next Window")

         #mute and solo for playlist, mixer and channel rack
         if (event.data1 == muteb):
            if ui.getFocused(0) == 1: #mixer volume control
               mixer.enableTrack(mixer.trackNumber()) #mute 
               self.UpdateOLED()
               ui.setHintMsg("Mute")

            elif (ui.getFocused(0) == 0) == True: # channel rack
               if channels.channelCount() >= 2: 
                  channels.muteChannel(channels.channelNumber()) 
                  self.UpdateOLED()
                  ui.setHintMsg("Mute")
               
            elif ui.getFocused(0) == 2: # playlist
               #playlist.muteTrack() disabled, doesn't work as expected
               self.UpdateOLED()

         if (event.data1 == solob): 
            if ui.getFocused(0) == 1: #mixer volume control
               mixer.soloTrack(mixer.trackNumber()) #solo
               self.UpdateOLED()
               ui.setHintMsg("Solo")

            elif (ui.getFocused(0) == 0) == True: # channel rack
               if channels.channelCount() >= 2: 
                  channels.soloChannel(channels.channelNumber()) 
                  self.UpdateOLED()
                  ui.setHintMsg("Solo")
               
            elif ui.getFocused(0) == 2: # playlist
               #playlist.soloTrack() need a way to track what playlist tracks
               self.UpdateOLED()



         #4D controller
         if (event.data1 == knobsp) & (event.data2 == right): #4d encoder spin right 
            ui.jog(1)
         elif (event.data1 == knobsp) & (event.data2 == left): #4d encoder spin left
            ui.jog(-1)
         
         if (event.data1 == knoblr) & (event.data2 == right): #4d encoder push right
            transport.globalTransport(midi.FPT_Right, 1)
         elif (event.data1 == knoblr) & (event.data2 == left): #4d encoder push left
            transport.globalTransport(midi.FPT_Left, 1)

         if (event.data1 == knobud) & (event.data2 == up): #4d encoder push up
            transport.globalTransport(midi.FPT_Up, 1)
         elif (event.data1 == knobud) & (event.data2 == down): #4d encoder push down
            transport.globalTransport(midi.FPT_Down, 1)

         #8 volume knobs for mixer & channel rack, 8 tracks at a time


         if ui.getFocused(0) == 1: #mixer volume control

            # VOLUME CONTROL

            xy = 1.25

            #knob 1
            if mixer.trackNumber() <= 126:
               if (event.data1 == knob1):
                if event.data2 == 127:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 0), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),3)))
                
                elif event.data2 == 1:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 0), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(0, (round((mixer.getTrackVolume(mixer.trackNumber() + 0) * xy ),3)))


            #knob 2
            if mixer.trackNumber() <= 125:
               if (event.data1 == knob2):
                if event.data2 == 127:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 1), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))
                
                elif event.data2 == 1:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 1), (x + knobinc) ) # volume values go up
                   KPrntScrnVol(1, (round((mixer.getTrackVolume(mixer.trackNumber() + 1) * xy ),2)))


            #knob 3
            if mixer.trackNumber() <= 124:
               if (event.data1 == knob3):
                if event.data2 == 127:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 2))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 2), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(2, (round((mixer.getTrackVolume(mixer.trackNumber() + 2) * xy ),2)))
                
                elif event.data2 == 1:
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
                if event.data2 == 127:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 3))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 3), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(3, (round((mixer.getTrackVolume(mixer.trackNumber() + 3) * xy ),2)))
                
                elif event.data2 == 1:
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
                if event.data2 == 127:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 4))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 4), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(4, (round((mixer.getTrackVolume(mixer.trackNumber() + 4) * xy ),2)))
                
                elif event.data2 == 1:
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
                if event.data2 == 127:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 5))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 5), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(5, (round((mixer.getTrackVolume(mixer.trackNumber() + 5) * xy ),2)))
                
                elif event.data2 == 1:
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
                if event.data2 == 127:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 6))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 6), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(6, (round((mixer.getTrackVolume(mixer.trackNumber() + 6) * xy ),2)))
                
                elif event.data2 == 1:
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
                if event.data2 == 127:
                   x = (mixer.getTrackVolume(mixer.trackNumber() + 7))
                   round(x,2)
                   mixer.setTrackVolume((mixer.trackNumber() + 7), (x - knobinc) ) # volume values go down
                   KPrntScrnVol(7, (round((mixer.getTrackVolume(mixer.trackNumber() + 7) * xy ),2)))
                
                elif event.data2 == 1:
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
                  if event.data2 == 127:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 0), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)
                
                  elif event.data2 == 1:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 0), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(0, mixer.getTrackPan(mixer.trackNumber() + 0) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(0, 104)

            #sknob 2
            if mixer.trackNumber() <= 125:
               if (event.data1 == sknob2):
                  if event.data2 == 127:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 1))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 1), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(1, mixer.getTrackPan(mixer.trackNumber() + 1) * 100)
                
                  elif event.data2 == 1:
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
                  if event.data2 == 127:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 2), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)
                
                  elif event.data2 == 1:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 2), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(2, mixer.getTrackPan(mixer.trackNumber() + 2) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(2, 104)

            #sknob 4
            if mixer.trackNumber() <= 123:
               if (event.data1 == sknob4):
                  if event.data2 == 127:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 3), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)
                
                  elif event.data2 == 1:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 3), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(3, mixer.getTrackPan(mixer.trackNumber() + 3) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(3, 104)

            #sknob 5
            if mixer.trackNumber() <= 122:
               if (event.data1 == sknob5):
                  if event.data2 == 127:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 4), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)
                
                  elif event.data2 == 1:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 4), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(4, mixer.getTrackPan(mixer.trackNumber() + 4) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(4, 104)

            #sknob 6
            if mixer.trackNumber() <= 121:
               if (event.data1 == sknob6):
                  if event.data2 == 127:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 5), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)
                
                  elif event.data2 == 1:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 5), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(5, mixer.getTrackPan(mixer.trackNumber() + 5) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(5, 104)

            #sknob 7
            if mixer.trackNumber() <= 120:
               if (event.data1 == sknob7):
                  if event.data2 == 127:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 6), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)
                
                  elif event.data2 == 1:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 6), (x + knobinc) ) # volume values go up
                     KPrntScrnPan(6, mixer.getTrackPan(mixer.trackNumber() + 6) * 100)

            elif mixer.trackNumber() <= 127:    
               KPrntScrnVol(6, 104)

            #sknob 8
            if mixer.trackNumber() <= 119:
               if (event.data1 == sknob8):
                  if event.data2 == 127:
                     x = (mixer.getTrackPan(mixer.trackNumber() + 7))
                     round(x,2)
                     mixer.setTrackPan((mixer.trackNumber() + 7), (x - knobinc) ) # volume values go down
                     KPrntScrnPan(7, mixer.getTrackPan(mixer.trackNumber() + 7) * 100)
                
                  elif event.data2 == 1:
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
             if event.data2 == 127:
                x = (channels.getChannelVolume(channels.channelNumber() + 0))
                y = round(x,2)
                if channels.getChannelVolume(channels.channelNumber() + 0) != 0 :
                  channels.setChannelVolume((channels.channelNumber() + 0), (y - knobinc) ) # volume values go down
                  KPrntScrnVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0) / xy ,2)))
       
             elif event.data2 == 1:
                x = (channels.getChannelVolume(channels.channelNumber() + 0))
                y = round(x,2)
                channels.setChannelVolume((channels.channelNumber() + 0), (y + knobinc) ) # volume values go up
                KPrntScrnVol(0, (round(channels.getChannelVolume(channels.channelNumber() + 0) / xy ,2)))

   
            #knob 2
            if (event.data1 == knob2):
             if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :  
               if event.data2 == 127:
                  x = (channels.getChannelVolume(channels.channelNumber() + 1))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 1) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 1), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1) / xy ,2)))
                
               elif event.data2 == 1:
                  x = (channels.getChannelVolume(channels.channelNumber() + 1))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 1), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(1, (round(channels.getChannelVolume(channels.channelNumber() + 1) / xy ,2)))

            #knob 3
            if (event.data1 == knob3):
             if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :  
               if event.data2 == 127:
                  x = (channels.getChannelVolume(channels.channelNumber() + 2))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 2) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 2), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2) / xy ,2)))
                
               elif event.data2 == 1:
                  x = (channels.getChannelVolume(channels.channelNumber() + 2))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 2), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(2, (round(channels.getChannelVolume(channels.channelNumber() + 2) / xy ,2)))

            #knob 4
            if (event.data1 == knob4):
             if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :  
               if event.data2 == 127:
                  x = (channels.getChannelVolume(channels.channelNumber() + 3))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 3) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 3), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3) / xy ,2)))
                
               elif event.data2 == 1:
                  x = (channels.getChannelVolume(channels.channelNumber() + 3))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 3), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(3, (round(channels.getChannelVolume(channels.channelNumber() + 3) / xy ,2)))

            #knob 5
            if (event.data1 == knob5):
             if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :  
               if event.data2 == 127:
                  x = (channels.getChannelVolume(channels.channelNumber() + 4))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 4) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 4), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4) / xy ,2)))
                
               elif event.data2 == 1:
                  x = (channels.getChannelVolume(channels.channelNumber() + 4))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 4), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(4, (round(channels.getChannelVolume(channels.channelNumber() + 4) / xy ,2)))

            #knob 6
            if (event.data1 == knob6):
             if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :  
               if event.data2 == 127:
                  x = (channels.getChannelVolume(channels.channelNumber() + 5))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 5) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 5), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5) / xy ,2)))
                
               elif event.data2 == 1:
                  x = (channels.getChannelVolume(channels.channelNumber() + 5))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 5), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(5, (round(channels.getChannelVolume(channels.channelNumber() + 5) / xy ,2)))

            #knob 7
            if (event.data1 == knob7):
             if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :  
               if event.data2 == 127:
                  x = (channels.getChannelVolume(channels.channelNumber() + 6))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 6) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 6), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6) / xy ,2)))
                
               elif event.data2 == 1:
                  x = (channels.getChannelVolume(channels.channelNumber() + 6))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 6), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(6, (round(channels.getChannelVolume(channels.channelNumber() + 6) / xy ,2)))

            #knob 8
            if (event.data1 == knob8):
             if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :  
               if event.data2 == 127:
                  x = (channels.getChannelVolume(channels.channelNumber() + 7))
                  y = round(x,2)
                  if channels.getChannelVolume(channels.channelNumber() + 7) != 0 :
                     channels.setChannelVolume((channels.channelNumber() + 7), (y - knobinc) ) # volume values go down
                     KPrntScrnVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7) / xy ,2)))
                
               elif event.data2 == 1:
                  x = (channels.getChannelVolume(channels.channelNumber() + 7))
                  y = round(x,2)
                  channels.setChannelVolume((channels.channelNumber() + 7), (y + knobinc) ) # volume values go up
                  KPrntScrnVol(7, (round(channels.getChannelVolume(channels.channelNumber() + 7) / xy ,2)))

            # PAN CONTROL

            #sknob 1
            if (event.data1 == sknob1):
             if event.data2 == 127:
                x = (channels.getChannelPan(channels.channelNumber() + 0))
                #round(x,2)
                channels.setChannelPan((channels.channelNumber() + 0), (x - knobinc) ) # pan values go down
                KPrntScrnPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)
  
             elif event.data2 == 1:
                x = (channels.getChannelPan(channels.channelNumber() + 0))
                #round(x,2)
                channels.setChannelPan((channels.channelNumber() + 0), (x + knobinc) ) # pan values go up
                KPrntScrnPan(0, channels.getChannelPan(channels.channelNumber() + 0) * 100)

            #sknob 2
            if (event.data1 == sknob2):
             if channels.channelCount() > 1 and channels.channelNumber() < (channels.channelCount()-1) :  
               if event.data2 == 127:
                  x = (channels.getChannelPan(channels.channelNumber() + 1))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 1), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)
                
               elif event.data2 == 1:
                  x = (channels.getChannelPan(channels.channelNumber() + 1))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 1), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(1, channels.getChannelPan(channels.channelNumber() + 1) * 100)     

            #sknob 3
            if (event.data1 == sknob3):
             if channels.channelCount() > 2 and channels.channelNumber() < (channels.channelCount()-2) :  
               if event.data2 == 127:
                  x = (channels.getChannelPan(channels.channelNumber() + 2))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 2), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)
                
               elif event.data2 == 1:
                  x = (channels.getChannelPan(channels.channelNumber() + 2))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 2), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(2, channels.getChannelPan(channels.channelNumber() + 2) * 100)     

            #sknob 4
            if (event.data1 == sknob4):
             if channels.channelCount() > 3 and channels.channelNumber() < (channels.channelCount()-3) :  
               if event.data2 == 127:
                  x = (channels.getChannelPan(channels.channelNumber() + 3))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 3), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)
                
               elif event.data2 == 1:
                  x = (channels.getChannelPan(channels.channelNumber() + 3))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 3), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(3, channels.getChannelPan(channels.channelNumber() + 3) * 100)     

            #sknob 5
            if (event.data1 == sknob5):
             if channels.channelCount() > 4 and channels.channelNumber() < (channels.channelCount()-4) :  
               if event.data2 == 127:
                  x = (channels.getChannelPan(channels.channelNumber() + 4))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 4), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)
                
               elif event.data2 == 1:
                  x = (channels.getChannelPan(channels.channelNumber() + 4))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 4), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(4, channels.getChannelPan(channels.channelNumber() + 4) * 100)     

            #sknob 6
            if (event.data1 == sknob6):
             if channels.channelCount() > 5 and channels.channelNumber() < (channels.channelCount()-5) :  
               if event.data2 == 127:
                   x = (channels.getChannelPan(channels.channelNumber() + 5))
                  #round(x,2)
                   channels.setChannelPan((channels.channelNumber() + 5), (x - knobinc) ) # pan values go down
                   KPrntScrnPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)
                
               elif event.data2 == 1:
                  x = (channels.getChannelPan(channels.channelNumber() + 5))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 5), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(5, channels.getChannelPan(channels.channelNumber() + 5) * 100)    

            #sknob 7
            if (event.data1 == sknob7):
             if channels.channelCount() > 6 and channels.channelNumber() < (channels.channelCount()-6) :  
               if event.data2 == 127:
                  x = (channels.getChannelPan(channels.channelNumber() + 6))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 6), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)
                
               elif event.data2 == 1:
                  x = (channels.getChannelPan(channels.channelNumber() + 6))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 6), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(6, channels.getChannelPan(channels.channelNumber() + 6) * 100)    

            #sknob 8
            if (event.data1 == sknob8):
             if channels.channelCount() > 7 and channels.channelNumber() < (channels.channelCount()-7) :  
               if event.data2 == 127:
                  x = (channels.getChannelPan(channels.channelNumber() + 7))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 7), (x - knobinc) ) # pan values go down
                  KPrntScrnPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)
                
               elif event.data2 == 1:
                  x = (channels.getChannelPan(channels.channelNumber() + 7))
                  #round(x,2)
                  channels.setChannelPan((channels.channelNumber() + 7), (x + knobinc) ) # pan values go up
                  KPrntScrnPan(7, channels.getChannelPan(channels.channelNumber() + 7) * 100)     


     def UpdateLEDs(self):

        if device.isAssigned():
            playstatus = [transport.isPlaying()]
            recstatus = [transport.isRecording()]
            loopstatus = [transport.getLoopMode()]
            metrostatus = [ui.isMetronomeEnabled()]
            prestatus = [ui.isPrecountEnabled()]
            quanstatus = [ui.getSnapMode()]
            mutestatusc = [channels.isChannelMuted(0)]
            solostatusc = [channels.isChannelSolo(0)]
            mutestatusm = [mixer.isTrackEnabled(mixer.trackNumber())]
            solostatusm = [mixer.isTrackSolo(mixer.trackNumber())]

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


     def UpdateOLED(self):

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
               device.midiOutSysex(bytes([0x00, 0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, 0x43, 0x00, 0x00, 0xF7]))
               KDataOut(102, off)
               
            elif mixer.isTrackEnabled(mixer.trackNumber()) == 0: #mute light on
               device.midiOutSysex(bytes([0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, 0x43, 0x01, 0x00, 0xF7]))
               KDataOut(102, on)

            if (mixer.isTrackSolo(mixer.trackNumber()) == 0) == True: #solo light off
               device.midiOutSysex(bytes([0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, 0x44, 0x00, 0x00, 0xF7]))
               KDataOut(105, off)

            elif (mixer.isTrackSolo(mixer.trackNumber()) == 1) == True: #solo light on
               device.midiOutSysex(bytes([0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, 0x44, 0x01, 0x00, 0xF7]))
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
               device.midiOutSysex(bytes([0x00, 0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, 0x43, 0x00, 0x00, 0xF7]))
               KDataOut(102, off)
               
            else: #mute light on
               device.midiOutSysex(bytes([0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, 0x43, 0x01, 0x00, 0xF7]))
               KDataOut(102, on)
            
            if channels.channelCount() >= 2: 
               if (channels.isChannelSolo(channels.channelNumber()) == 0) == True: #solo light off
                  device.midiOutSysex(bytes([0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, 0x44, 0x00, 0x00, 0xF7]))
                  KDataOut(105, off)

               else: #solo light on
                  device.midiOutSysex(bytes([0xF0, 0x00, 0x21, 0x09, 0x00, 0x00, 0x44, 0x43, 0x01, 0x00, 0x44, 0x01, 0x00, 0xF7]))
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


     def OnRefresh(self, flags): #when something happens in FL Studio, update the keyboard lights & OLED
        self.UpdateLEDs(), self.UpdateOLED()

     def OnDoFullRefresh(self, flags): #when something happens in FL Studio, update the keyboard lights & OLED
        self.UpdateLEDs(), self.UpdateOLED()

     def OnUpdateBeatIndicator(Self, Value): #play light flashes to the tempo of project
         if Value == 1:
            KDataOut(playb, on) #play light bright
         elif Value == 2:
            KDataOut(playb, on) #play light bright
         elif Value == 0:
            KDataOut(playb, off) #play light dim

     def OnIdle():
         self.UpdateLEDs(), self.UpdateOLED()




KompleteBase = TKompleteBase()

def OnInit():
   # command to initialize the protocol handshake
   KDataOut(1, 1), KompleteBase.OnInit()

def OnRefresh(Flags):
   KompleteBase.OnRefresh(Flags)

def OnDoFullRefresh(Flags):
   KompleteBase.OnDoFullRefresh(Flags)

def OnIdle():
   KompleteBase.OnIdle

def OnUpdateBeatIndicator(Value):
	KompleteBase.OnUpdateBeatIndicator(Value)

def OnMidiIn(event):
	KompleteBase.OnMidiIn(event)

def OnDeInit():
   if ui.isClosing():
      # Command to stop the protocol
      KDataOut(2, 1), KompleteBase.OnDeInit()	
