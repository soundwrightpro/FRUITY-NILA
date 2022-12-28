import nihia
from nihia import buttons 

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

        if mixer.trackNumber() <= 125:

            if mixer.isTrackMuted(mixer.trackNumber()) == True:
                nihia.buttons.setLight("MUTE_SELECTED", mixer.isTrackMuted(mixer.trackNumber()))
            else:
                nihia.buttons.setLight("MUTE_SELECTED", mixer.isTrackMuted(mixer.trackNumber()))

            if mixer.isTrackSolo(mixer.trackNumber()) == True:
                nihia.buttons.setLight("SOLO_SELECTED", mixer.isTrackSolo(mixer.trackNumber()))
            else:
                nihia.buttons.setLight("SOLO_SELECTED", mixer.isTrackSolo(mixer.trackNumber()))      

        #channel mute/solo paradox fix (why was this so hard?!?!?!?)
        if channels.channelCount() >= 2: 
            if channels.isChannelSolo(channels.selectedChannel()) == True:
                nihia.buttons.setLight("SOLO_SELECTED", on)
            else:
                nihia.buttons.setLight("SOLO_SELECTED", off)

            if channels.isChannelMuted(channels.selectedChannel()) == True:
                if channels.isChannelSolo(channels.selectedChannel()) == True:
                    nihia.buttons.setLight("MUTE_SELECTED", on)
                    nihia.buttons.setLight("SOLO_SELECTED", off)
                else:
                    nihia.buttons.setLight("MUTE_SELECTED", on)
            else:
                nihia.buttons.setLight("MUTE_SELECTED", off)
        

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