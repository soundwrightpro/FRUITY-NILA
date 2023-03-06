import nihia
from nihia import buttons 
from nihia import mixer as mix

from script.device_setup import config

import channels
import device
import general
import math
import midi
import mixer
import transport
import time
import ui


on = 1
off = 0

windowCycle = 0
jogMove = True
config.currentUtility


def OnRefresh(self, flags):
    if device.isAssigned():
        for a in [transport.isPlaying()]:
            if a == off: #not playing
                nihia.buttons.setLight("STOP", on) 
            elif a == on: #playing
                nihia.buttons.setLight("STOP", off) 

        if transport.isPlaying() == True:
            pass
        else:
            for b in [transport.isRecording()]:
                if b == off: #not recording
                    nihia.buttons.setLight("REC", off)
                elif b == on: #recording
                    nihia.buttons.setLight("REC", on)

        for c in [transport.getLoopMode()]:
            if c == off: #loop mood
                nihia.buttons.setLight("LOOP", on)

            elif c == on: #playlist mode
                nihia.buttons.setLight("LOOP", off)

        for d in [ui.isMetronomeEnabled()]:
            if d == off: #metro off
                nihia.buttons.setLight("METRO", off)

            elif d == on: #metro on
                nihia.buttons.setLight("METRO", on)

        for e in [ui.isPrecountEnabled()]:
            if e == off: #pre count on
                nihia.buttons.setLight("COUNT_IN", off)

            elif e == on: #pre count off
                nihia.buttons.setLight("COUNT_IN", on)

        for f in [ui.getSnapMode()]:
            if f == 3: #quantize always on
                nihia.buttons.setLight("QUANTIZE", on)
                nihia.buttons.setLight("AUTO", off)

            elif f != 1: #quantize alwayns on
                nihia.buttons.setLight("QUANTIZE", on)
                nihia.buttons.setLight("AUTO", off)

        for g in [transport.isPlaying()]:
            if transport.isRecording() == 0 & transport.isPlaying() == 1: 
                if g == off: #play off
                    nihia.buttons.setLight("PLAY", off)
                elif g != on: #play on
                    nihia.buttons.setLight("PLAY", on)
            elif g == off: #play off: 
                nihia.buttons.setLight("PLAY", off)


        if ui.getFocused(config.winName["Mixer"]) == True:
            #mixer solo
            if mixer.trackNumber() <= 125:
                if mixer.isTrackSolo(mixer.trackNumber() + 0) == True or mixer.isTrackSolo(mixer.trackNumber() + 0) == False:
                    mix.setTrackSolo(0, mixer.isTrackSolo(mixer.trackNumber() + 0))

            if mixer.trackNumber() <= 124:
                if mixer.isTrackSolo(mixer.trackNumber() + 1) == True or mixer.isTrackSolo(mixer.trackNumber() + 1) == False:
                    mix.setTrackSolo(1, mixer.isTrackSolo(mixer.trackNumber() + 1))

            if mixer.trackNumber() <= 123:
                if mixer.isTrackSolo(mixer.trackNumber() + 2) == True or mixer.isTrackSolo(mixer.trackNumber() + 2) == False:
                    mix.setTrackSolo(2, mixer.isTrackSolo(mixer.trackNumber() + 2))

            if mixer.trackNumber() <= 122:
                if mixer.isTrackSolo(mixer.trackNumber() + 3) == True or mixer.isTrackSolo(mixer.trackNumber() + 3) == False:
                    mix.setTrackSolo(3, mixer.isTrackSolo(mixer.trackNumber() + 3))

            if mixer.trackNumber() <= 121:
                if mixer.isTrackSolo(mixer.trackNumber() + 4) == True or mixer.isTrackSolo(mixer.trackNumber() + 4) == False:
                    mix.setTrackSolo(4, mixer.isTrackSolo(mixer.trackNumber() + 4))

            if mixer.trackNumber() <= 120:
                if mixer.isTrackSolo(mixer.trackNumber() + 5) == True or mixer.isTrackSolo(mixer.trackNumber() + 5) == False:
                    mix.setTrackSolo(5, mixer.isTrackSolo(mixer.trackNumber() + 5))

            if mixer.trackNumber() <= 119:
                if mixer.isTrackSolo(mixer.trackNumber() + 6) == True or mixer.isTrackSolo(mixer.trackNumber() + 6) == False:
                    mix.setTrackSolo(6, mixer.isTrackSolo(mixer.trackNumber() + 6))

            if mixer.trackNumber() <= 118:
                if mixer.isTrackSolo(mixer.trackNumber() + 7) == True or mixer.isTrackSolo(mixer.trackNumber() + 7) == False:
                    mix.setTrackSolo(7, mixer.isTrackSolo(mixer.trackNumber() + 7))


            #mixer mute 
            if mixer.trackNumber() <= 125:
                if mixer.isTrackMuted(mixer.trackNumber() + 0) == True or mixer.isTrackMuted(mixer.trackNumber() + 0) == False:
                    mix.setTrackMute(0, mixer.isTrackMuted(mixer.trackNumber() + 0))

            if mixer.trackNumber() <= 124:
                if mixer.isTrackMuted(mixer.trackNumber() + 1) == True or mixer.isTrackMuted(mixer.trackNumber() + 1) == False:
                    mix.setTrackMute(1, mixer.isTrackMuted(mixer.trackNumber() + 1))

            if mixer.trackNumber() <= 123:
                if mixer.isTrackMuted(mixer.trackNumber() + 2) == True or mixer.isTrackMuted(mixer.trackNumber() + 2) == False:
                    mix.setTrackMute(2, mixer.isTrackMuted(mixer.trackNumber() + 2))

            if mixer.trackNumber() <= 122:
                if mixer.isTrackMuted(mixer.trackNumber() + 3) == True or mixer.isTrackMuted(mixer.trackNumber() + 3) == False:
                    mix.setTrackMute(3, mixer.isTrackMuted(mixer.trackNumber() + 3))
                    
            if mixer.trackNumber() <= 121:
                if mixer.isTrackMuted(mixer.trackNumber() + 4) == True or mixer.isTrackMuted(mixer.trackNumber() + 4) == False:
                    mix.setTrackMute(4, mixer.isTrackMuted(mixer.trackNumber() + 4))

            if mixer.trackNumber() <= 120:
                if mixer.isTrackMuted(mixer.trackNumber() + 5) == True or mixer.isTrackMuted(mixer.trackNumber() + 5) == False:
                    mix.setTrackMute(5, mixer.isTrackMuted(mixer.trackNumber() + 5))

            if mixer.trackNumber() <= 119:
                if mixer.isTrackMuted(mixer.trackNumber() + 6) == True or mixer.isTrackMuted(mixer.trackNumber() + 6) == False:
                    mix.setTrackMute(6, mixer.isTrackMuted(mixer.trackNumber() + 6))

            if mixer.trackNumber() <= 118:
                if mixer.isTrackMuted(mixer.trackNumber() + 7) == True or mixer.isTrackMuted(mixer.trackNumber() + 7) == False:
                    mix.setTrackMute(7, mixer.isTrackMuted(mixer.trackNumber() + 7))


            #mixer recording arm
            if mixer.trackNumber() <= 125:
                if mixer.isTrackArmed(mixer.trackNumber() + 0) == True or mixer.isTrackArmed(mixer.trackNumber() + 0) == False:
                    mix.setTrackArm(0, mixer.isTrackArmed(mixer.trackNumber() + 0))       

            if mixer.trackNumber() <= 124:
                if mixer.isTrackArmed(mixer.trackNumber() + 1) == True or mixer.isTrackArmed(mixer.trackNumber() + 1) == False:
                    mix.setTrackArm(1, mixer.isTrackArmed(mixer.trackNumber() + 1))
    
            if mixer.trackNumber() <= 123:
                if mixer.isTrackArmed(mixer.trackNumber() + 2) == True or mixer.isTrackArmed(mixer.trackNumber() + 2) == False:
                    mix.setTrackArm(2, mixer.isTrackArmed(mixer.trackNumber() + 2))           

            if mixer.trackNumber() <= 122:
                if mixer.isTrackArmed(mixer.trackNumber() + 3) == True or mixer.isTrackArmed(mixer.trackNumber() + 3) == False:
                    mix.setTrackArm(3, mixer.isTrackArmed(mixer.trackNumber() + 3))

            if mixer.trackNumber() <= 121:
                if mixer.isTrackArmed(mixer.trackNumber() + 4) == True or mixer.isTrackArmed(mixer.trackNumber() + 4) == False:
                    mix.setTrackArm(4, mixer.isTrackArmed(mixer.trackNumber() + 4))           

            if mixer.trackNumber() <= 120:
                if mixer.isTrackArmed(mixer.trackNumber() + 5) == True or mixer.isTrackArmed(mixer.trackNumber() + 5) == False:
                    mix.setTrackArm(5, mixer.isTrackArmed(mixer.trackNumber() + 5))  

            if mixer.trackNumber() <= 119:
                if mixer.isTrackArmed(mixer.trackNumber() + 6) == True or mixer.isTrackArmed(mixer.trackNumber() + 6) == False:
                    mix.setTrackArm(6, mixer.isTrackArmed(mixer.trackNumber() + 6))           

            if mixer.trackNumber() <= 118:
                if mixer.isTrackArmed(mixer.trackNumber() + 7) == True or mixer.isTrackArmed(mixer.trackNumber() + 7) == False:
                    mix.setTrackArm(7, mixer.isTrackArmed(mixer.trackNumber() + 7))



        if ui.getFocused(config.winName["Channel Rack"]) == True:
   
            #channel mute/solo paradox fix (why was this so hard?!?!?!?)
            if channels.channelCount() >= 2:
                for x in range(8):
                    if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount()-x) :
                        if channels.isChannelSolo(channels.selectedChannel() + x) == True:
                            mix.setTrackSolo(x, 1)
                        else:
                            mix.setTrackSolo(x, 0)

                        if channels.isChannelMuted(channels.selectedChannel() + x) == True:
                            if channels.isChannelSolo(channels.selectedChannel() + x) == True:
                                mix.setTrackMute(x, 1)
                                mix.setTrackSolo(x, 0)
                            else:
                                mix.setTrackMute(x, 1)
                        else:
                            mix.setTrackMute(x, 0)
            else:
                if channels.isChannelMuted(channels.selectedChannel()) == True:
                    mix.setTrackMute(0, 1)
                else:
                    mix.setTrackMute(0, 0)


    

        # Sets the lights of the 4D Encoder on S-Series keyboards on
        nihia.buttons.setLight("ENCODER_X_S", 1)
        nihia.buttons.setLight("ENCODER_X_S", 127)
        nihia.buttons.setLight("ENCODER_Y_S", 1)
        nihia.buttons.setLight("ENCODER_Y_S", 127)

        

def OnUpdateBeatIndicator(self, Value):

    if transport.isRecording() == 0:
        if Value == 1:
            nihia.buttons.setLight("PLAY", on) 
        elif Value == 2:
            nihia.buttons.setLight("PLAY", on) 
        elif Value == 0:
            nihia.buttons.setLight("PLAY", off) 

    elif transport.isRecording() == 1:
        nihia.buttons.setLight("PLAY", on)
        if Value == 1:
            nihia.buttons.setLight("REC", on) 
        elif Value == 2:
            nihia.buttons.setLight("REC", on) 
        elif Value == 0:
            nihia.buttons.setLight("REC", off) 