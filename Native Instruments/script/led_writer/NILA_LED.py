import nihia
from nihia import buttons 
from nihia import mixer as mix

from script.device_setup import constants

import channels
import device
import mixer
import transport
import ui


on = 1
off = 0

windowCycle = 0
jogMove = True
constants.currentUtility


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

        if ui.getFocused(constants.winName["Mixer"]) == True:
            
            for x in range (8):
                #mixer solo
                if mixer.trackNumber() <= 125 - x:
                    if mixer.isTrackSolo(mixer.trackNumber() + x) == True or mixer.isTrackSolo(mixer.trackNumber() + x) == False:
                        mix.setTrackSolo(x, mixer.isTrackSolo(mixer.trackNumber() + x))

                #mixer mute 
                if mixer.trackNumber() <= 125 - x:
                    if mixer.isTrackMuted(mixer.trackNumber() + x) == True or mixer.isTrackMuted(mixer.trackNumber() + x) == False:
                        mix.setTrackMute(x, mixer.isTrackMuted(mixer.trackNumber() + x))

                #mixer recording arm          
                if mixer.trackNumber() <= 125 - x:
                    if mixer.isTrackArmed(mixer.trackNumber() +x) == True or mixer.isTrackArmed(mixer.trackNumber() + x) == False:
                        mix.setTrackArm(x, mixer.isTrackArmed(mixer.trackNumber() + x))

        if ui.getFocused(constants.winName["Channel Rack"]) == True:
   
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
                    
                if channels.channelCount() == 1 and channels.isChannelSolo(channels.selectedChannel()) == True:
                    mix.setTrackSolo(0, 0)
   
                
                    

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