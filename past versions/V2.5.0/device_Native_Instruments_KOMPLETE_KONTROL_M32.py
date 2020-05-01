# name=Native Instruments KOMPLETE KONTROL M32
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-m32/

# github for this script
# url=https://github.com/soundwrightpro/FLIN 
# FL Studio Forum
# https://forum.image-line.com/viewtopic.php?f=1994&t=225473
# script by Duwayne "Sound" Wright www.soundwrightpro.com and additional code from Hobyst


#custom fl script modules
import fl
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
knobe = 96 # knob enter

#data2 right left values
right = 1
up = 127
left = 127
down = 1

#function to make talking to the keyboard less annoying
def KompleteDataOut(data11, data12):
      """ Funtion that makes commmuication with the keyboard easier. By just entering the DATA1 and DATA2 of the MIDI message, 
          it composes the full message in forther to satisfy the syntax required by the midiOut functions, as well as the setting 
            the STATUS of the message to BF as expected.""" 
      device.midiOutSysex(bytes([0xF0, 0xBF, data11, data12, 0x14, 0x0C, 1, 0xF7]))

class TKompleteBase():
     def OnInit(self):
         print("Active")

     def OnMidiIn(self, event):
         
         print("Output from M32: data 1 =", event.data1, ", data 2 =",event.data2, ", handled ", event.handled)
         u = 0
         #tbuttons
         if (event.data1 == playb):
            transport.start() #play
            
         if (event.data1 == recb):
            transport.record() #record

         if (event.data1 == stopb):
            transport.stop() #stop

         if (event.data1 == loopb):
            transport.setLoopMode() #loop/pattern mode

         if (event.data1 == metrob): # metronome/button self.Clicking 
            transport.globalTransport(midi.FPT_Metronome, 110)
            
         if (event.data1 == tempob):
            transport.stop() #tap tempo

         if (event.data1 == quantizeb):
            transport.globalTransport(midi.FPT_Snap, 48) #snap toggle

         if (event.data1 == squantizeb):
            transport.globalTransport(midi.FPT_Snap, 48) #snap toggle     

         if (event.data1 == srecb):
            transport.globalTransport(midi.FPT_CountDown, 115) #countdown before recordin

         if (event.data1 == sstopb):
            transport.globalTransport(midi.FPT_F12, 71) #clear all windows

         if (event.data1 == sstopb):
            transport.globalTransport(midi.FPT_F12, 71) #clear all windows

         if (event.data1 == undob):
            general.undoUp() #undo

         if (event.data1 == sundob):
            general.undo() #redo

         if (event.data1 == squantizeb):
            transport.globalTransport(midi.FPT_SnapMode, 49, event.pmeFlags) #snap toggle

         if (event.data1 == tempob):
            transport.globalTransport(midi.FPT_TapTempo, 106) #tap tempo


         #knobs
         if (event.data1 == knobe):
            transport.globalTransport(midi.FPT_Enter, 80) #enter
         
         if (event.data1 == knobsp) & (event.data2 == right): #4d encoder spin right 
            transport.globalTransport(midi.FPT_Jog, 1)
            
         elif (event.data1 == knobsp) & (event.data2 == left): #4d encoder spin left
            transport.globalTransport(midi.FPT_Jog, -1)
         
         if (event.data1 == knoblr) & (event.data2 == right): #4d encoder push right
            transport.globalTransport(midi.FPT_Right, 1)
            
         elif (event.data1 == knoblr) & (event.data2 == left): #4d encoder push left
            transport.globalTransport(midi.FPT_Left, 1)

         if (event.data1 == knobud) & (event.data2 == up): #4d encoder push up
            transport.globalTransport(midi.FPT_Up, 1)
         elif (event.data1 == knobud) & (event.data2 == down): #4d encoder push down
            transport.globalTransport(midi.FPT_Down, 1)

         

       

KompleteBase = TKompleteBase()


def OnInit():
      # command to initialize the protocol handshake
      KompleteDataOut(0x01, 0x01), KompleteBase.OnInit()

def OnMidiIn(event):
	KompleteBase.OnMidiIn(event)

def OnDeInit():
      if ui.isClosing():
                  # Command to stop the protocol
                  KompleteDataOut(0x02, 0x01), KompleteBase.OnDeInit()	
