from nihia import mixer as nihia_mix

from script.device_setup import NILA_core
from script.device_setup import config 
from script.NILA_UI import NILA_touch_strips

import channels
import general
import math
import mixer
import playlist
import ui


def updatePanMix(self,track):

    if mixer.getTrackPan(self) == 0:
        nihia_mix.setTrackPan(track, "Centered")
    elif mixer.getTrackPan(self) > 0:
        nihia_mix.setTrackPan(track, str(round(mixer.getTrackPan(self) * 100)) + "% " + "Right")
    elif mixer.getTrackPan(self) < 0:
        nihia_mix.setTrackPan(track, str(round(mixer.getTrackPan(self) * -100)) + "% " + "Left")


def updatePanChannel(self,track):

    if channels.getChannelPan(self) == 0:
        nihia_mix.setTrackPan(track, "Centered")
    elif channels.getChannelPan(self) > 0:
        nihia_mix.setTrackPan(track, str(round(channels.getChannelPan(self) * 100)) + "% " + "Right")
    elif channels.getChannelPan(self) < 0:
        nihia_mix.setTrackPan(track, str(round(channels.getChannelPan(self) * -100)) + "% " + "Left")


def updateText(self,track):
    nihia_mix.setTrackName(track, self)


def namingTrack(self, event):

    if ui.getFocused(config.winName["Mixer"]) == True: 

        xy = 1.25

        if mixer.trackNumber() <= config.currentUtility:
            nihia_mix.setTrackName(0, mixer.getTrackName(mixer.trackNumber() + 0))
            nihia_mix.setTrackVol(0, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 0))) + " dB")
            updatePanMix((mixer.trackNumber() + 0), 0)

        if mixer.trackNumber() <= 125:
            nihia_mix.setTrackName(1, mixer.getTrackName(mixer.trackNumber() + 1))
            nihia_mix.setTrackVol(1, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 1))) + " dB")
            updatePanMix((mixer.trackNumber() + 1), 1)
        
        if mixer.trackNumber() <= 124:
            nihia_mix.setTrackName(2, mixer.getTrackName(mixer.trackNumber() + 2))
            nihia_mix.setTrackVol(2, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 2))) + " dB")
            updatePanMix((mixer.trackNumber() + 2), 2)

        if mixer.trackNumber() <= 123:
            nihia_mix.setTrackName(3, mixer.getTrackName(mixer.trackNumber() + 3))
            nihia_mix.setTrackVol(3, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 3))) + " dB")
            updatePanMix((mixer.trackNumber() + 3), 3)

        if mixer.trackNumber() <= 122:
            nihia_mix.setTrackName(4, mixer.getTrackName(mixer.trackNumber() + 4))
            nihia_mix.setTrackVol(4, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 4))) + " dB")
            updatePanMix((mixer.trackNumber() + 4), 4)

        if mixer.trackNumber() <= 121:
            nihia_mix.setTrackName(5, mixer.getTrackName(mixer.trackNumber() + 5))
            nihia_mix.setTrackVol(5, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 5))) + " dB")
            updatePanMix((mixer.trackNumber() + 5), 5)

        if mixer.trackNumber() <= 120:
            nihia_mix.setTrackName(6, mixer.getTrackName(mixer.trackNumber() + 6))
            nihia_mix.setTrackVol(6, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 6))) + " dB")
            updatePanMix((mixer.trackNumber() + 6), 6)

        if mixer.trackNumber() <= 119:
            nihia_mix.setTrackName(7, mixer.getTrackName(mixer.trackNumber() + 7))
            nihia_mix.setTrackVol(7, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 7))) + " dB")
            updatePanMix((mixer.trackNumber() + 7), 7)

    elif ui.getFocused(config.winName["Channel Rack"]) == True:

        #knob 0
        NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+0, 1), 1)) + " dB")
        nihia_mix.setTrackName(0, channels.getChannelName(channels.selectedChannel() + 0))
        updatePanChannel((channels.selectedChannel() + 0), 0)

        if channels.channelCount() > 0 and channels.selectedChannel() < (channels.channelCount()-0) :
            NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
            nihia_mix.setTrackName(0, channels.getChannelName(channels.selectedChannel() + 0))
            updatePanChannel((channels.selectedChannel() + 0), 0)
        else:
            nihia_mix.setTrackName(0, (config.blankEvent))
            NILA_core.setTrackVolConvert(0, config.blankEvent)
            nihia_mix.setTrackPan(0, config.blankEvent)

        #knob 1
        if channels.channelCount() > 1 and channels.selectedChannel() < (channels.channelCount()-1) :
            NILA_core.setTrackVolConvert(1, str(round(channels.getChannelVolume(channels.selectedChannel()+ 1, 1), 1)) + " dB")
            nihia_mix.setTrackName(1, channels.getChannelName(channels.selectedChannel() + 1))
            updatePanChannel((channels.selectedChannel() + 1), 1)
        else:
            nihia_mix.setTrackName(1, (config.blankEvent ))
            NILA_core.setTrackVolConvert(1, config.blankEvent)
            nihia_mix.setTrackPan(1, config.blankEvent)

        #knob 2
        if channels.channelCount() > 2 and channels.selectedChannel() < (channels.channelCount()-2) :
            NILA_core.setTrackVolConvert(2, str(round(channels.getChannelVolume(channels.selectedChannel()+ 2, 1), 1)) + " dB")
            nihia_mix.setTrackName(2, channels.getChannelName(channels.selectedChannel() + 2))
            updatePanChannel((channels.selectedChannel() + 2), 2)
        else:
            nihia_mix.setTrackName(2, (config.blankEvent ))
            NILA_core.setTrackVolConvert(2, config.blankEvent)
            nihia_mix.setTrackPan(2, config.blankEvent)

        #knob 3
        if channels.channelCount() > 3 and channels.selectedChannel() < (channels.channelCount()-3) :
            NILA_core.setTrackVolConvert(3, str(round(channels.getChannelVolume(channels.selectedChannel()+ 3, 1), 1)) + " dB")
            nihia_mix.setTrackName(3, channels.getChannelName(channels.selectedChannel() + 3))
            updatePanChannel((channels.selectedChannel() + 3), 3)
        else:
            nihia_mix.setTrackName(3, (config.blankEvent ))
            NILA_core.setTrackVolConvert(3, config.blankEvent)
            nihia_mix.setTrackPan(3, config.blankEvent)

        #knob 4
        if channels.channelCount() > 4 and channels.selectedChannel() < (channels.channelCount()-4) :
            NILA_core.setTrackVolConvert(4, str(round(channels.getChannelVolume(channels.selectedChannel()+ 4, 1), 1)) + " dB")
            nihia_mix.setTrackName(4, channels.getChannelName(channels.selectedChannel() + 4))
            updatePanChannel((channels.selectedChannel() + 4), 4)
        else:
            nihia_mix.setTrackName(4, (config.blankEvent ))
            NILA_core.setTrackVolConvert(4, config.blankEvent)
            nihia_mix.setTrackPan(4, config.blankEvent)

        #knob 5
        if channels.channelCount() > 5 and channels.selectedChannel() < (channels.channelCount()-5) :
            NILA_core.setTrackVolConvert(5, str(round(channels.getChannelVolume(channels.selectedChannel()+ 5, 1), 1)) + " dB")
            nihia_mix.setTrackName(5, channels.getChannelName(channels.selectedChannel() + 5))
            updatePanChannel((channels.selectedChannel() + 5), 5)
        else:
            nihia_mix.setTrackName(5, (config.blankEvent ))
            NILA_core.setTrackVolConvert(5, config.blankEvent)
            nihia_mix.setTrackPan(5, config.blankEvent)

        #knob 6
        if channels.channelCount() > 6 and channels.selectedChannel() < (channels.channelCount()-6) :
            NILA_core.setTrackVolConvert(6, str(round(channels.getChannelVolume(channels.selectedChannel()+ 6, 1), 1)) + " dB")
            nihia_mix.setTrackName(6, channels.getChannelName(channels.selectedChannel() + 6))
            updatePanChannel((channels.selectedChannel() + 6), 6)
        else:
            nihia_mix.setTrackName(6, (config.blankEvent ))
            NILA_core.setTrackVolConvert(6, config.blankEvent)
            nihia_mix.setTrackPan(6, config.blankEvent)

        #knob 7
        if channels.channelCount() > 7 and channels.selectedChannel() < (channels.channelCount()-7) :
            NILA_core.setTrackVolConvert(7, str(round(channels.getChannelVolume(channels.selectedChannel()+ 7, 1), 1)) + " dB")
            nihia_mix.setTrackName(7, channels.getChannelName(channels.selectedChannel() + 7))
            updatePanChannel((channels.selectedChannel() + 7), 7)
        else:
            nihia_mix.setTrackName(7, (config.blankEvent))
            NILA_core.setTrackVolConvert(7, config.blankEvent)
            nihia_mix.setTrackPan(7, config.blankEvent)


    elif ui.getFocused(config.winName["Plugin"]) == True: 

        updateText(ui.getFocusedPluginName(), 0)
        updateText(config.blankEvent, 1)
        updateText(config.blankEvent, 2)
        updateText(config.blankEvent, 3)
        updateText(config.blankEvent, 4)
        updateText(config.blankEvent, 5)
        updateText(config.blankEvent, 6)
        updateText(config.blankEvent, 7)

        NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
        nihia_mix.setTrackVol(1, config.blankEvent)
        nihia_mix.setTrackVol(2, config.blankEvent)
        nihia_mix.setTrackVol(3, config.blankEvent)
        nihia_mix.setTrackVol(4, config.blankEvent)
        nihia_mix.setTrackVol(5, config.blankEvent)
        nihia_mix.setTrackVol(6, config.blankEvent)
        nihia_mix.setTrackVol(7, config.blankEvent)

        updatePanChannel((channels.selectedChannel() + 0), 0)
        nihia_mix.setTrackPan(1, config.blankEvent)
        nihia_mix.setTrackPan(2, config.blankEvent)
        nihia_mix.setTrackPan(3, config.blankEvent)
        nihia_mix.setTrackPan(4, config.blankEvent)
        nihia_mix.setTrackPan(5, config.blankEvent)
        nihia_mix.setTrackPan(6, config.blankEvent)
        nihia_mix.setTrackPan(7, config.blankEvent)
        
    elif ui.getFocused(config.winName["Browser"]) == True: 

        # widTitle[4] = Browser
        nihia_mix.setTrackName(0, config.widTitle[4])
        nihia_mix.setTrackName(1, config.widTitle[4])
        nihia_mix.setTrackName(2, config.widTitle[4])
        nihia_mix.setTrackName(3, config.widTitle[4])
        nihia_mix.setTrackName(4, config.widTitle[4])
        nihia_mix.setTrackName(5, config.widTitle[4])
        nihia_mix.setTrackName(6, config.widTitle[4])
        nihia_mix.setTrackName(7, config.widTitle[4])
        
        nihia_mix.setTrackVol(0, config.blankEvent)
        nihia_mix.setTrackVol(1, config.blankEvent)
        nihia_mix.setTrackVol(2, config.blankEvent)
        nihia_mix.setTrackVol(3, config.blankEvent)
        nihia_mix.setTrackVol(4, config.blankEvent)
        nihia_mix.setTrackVol(5, config.blankEvent)
        nihia_mix.setTrackVol(6, config.blankEvent)
        nihia_mix.setTrackVol(7, config.blankEvent)

        nihia_mix.setTrackPan(0, config.blankEvent)
        nihia_mix.setTrackPan(1, config.blankEvent)
        nihia_mix.setTrackPan(2, config.blankEvent)
        nihia_mix.setTrackPan(3, config.blankEvent)
        nihia_mix.setTrackPan(4, config.blankEvent)
        nihia_mix.setTrackPan(5, config.blankEvent)
        nihia_mix.setTrackPan(6, config.blankEvent)
        nihia_mix.setTrackPan(7, config.blankEvent)
    
    if ui.getFocused(config.winName["Piano Roll"]) == True: #piano roll:

        nihia_mix.setTrackName(0, (str(channels.getChannelName(channels.selectedChannel()))))
        nihia_mix.setTrackName(1, config.blankEvent)
        nihia_mix.setTrackName(2, config.blankEvent)
        nihia_mix.setTrackName(3, config.blankEvent)
        nihia_mix.setTrackName(4, config.blankEvent)
        nihia_mix.setTrackName(5, config.blankEvent)
        nihia_mix.setTrackName(6, config.blankEvent)
        nihia_mix.setTrackName(7, config.blankEvent)
        
        NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
        nihia_mix.setTrackVol(1, config.blankEvent)
        nihia_mix.setTrackVol(2, config.blankEvent)
        nihia_mix.setTrackVol(3, config.blankEvent)
        nihia_mix.setTrackVol(4, config.blankEvent)
        nihia_mix.setTrackVol(5, config.blankEvent)
        nihia_mix.setTrackVol(6, config.blankEvent)
        nihia_mix.setTrackVol(7, config.blankEvent)

        updatePanChannel((channels.selectedChannel() + 0), 0)
        nihia_mix.setTrackPan(1, config.blankEvent)
        nihia_mix.setTrackPan(2, config.blankEvent)
        nihia_mix.setTrackPan(3, config.blankEvent)
        nihia_mix.setTrackPan(4, config.blankEvent)
        nihia_mix.setTrackPan(5, config.blankEvent)
        nihia_mix.setTrackPan(6, config.blankEvent)
        nihia_mix.setTrackPan(7, config.blankEvent)


def OnUpdateBeatIndicator(self, Value):

    if ui.getFocused(config.winName["Playlist"]) == True:

        timeDisp, currentTime = NILA_core.timeConvert(config.itemDisp, config.itemTime)

        updateText(str(timeDisp), 0)
        updateText(config.blankEvent, 1)
        updateText(config.blankEvent, 2)
        updateText(config.blankEvent, 3)
        updateText(config.blankEvent, 4)
        updateText(config.blankEvent, 5)
        updateText(config.blankEvent, 6)
        updateText(config.blankEvent, 7)

        split_message = ui.getHintMsg()
        split_point1 = ' - '
        split_point2 = ' to '

        if split_point1 in split_message.lower():
            split_hint = split_message.partition(split_point1)[2]
        else:
            split_hint = split_message.partition(split_point2)[2]

        nihia_mix.setTrackVol(0, str(split_hint[:7] + "| " + currentTime))
        nihia_mix.setTrackVol(1, config.blankEvent)
        nihia_mix.setTrackVol(2, config.blankEvent)
        nihia_mix.setTrackVol(3, config.blankEvent)
        nihia_mix.setTrackVol(4, config.blankEvent)
        nihia_mix.setTrackVol(5, config.blankEvent)
        nihia_mix.setTrackVol(6, config.blankEvent)
        nihia_mix.setTrackVol(7, config.blankEvent)

        nihia_mix.setTrackPan(0, config.blankEvent)
        nihia_mix.setTrackPan(1, config.blankEvent)
        nihia_mix.setTrackPan(2, config.blankEvent)
        nihia_mix.setTrackPan(3, config.blankEvent)
        nihia_mix.setTrackPan(4, config.blankEvent)
        nihia_mix.setTrackPan(5, config.blankEvent)
        nihia_mix.setTrackPan(6, config.blankEvent)
        nihia_mix.setTrackPan(7, config.blankEvent)

    else:
        pass


def OnIdle():

    print()

    if ui.getFocused(config.winName["Browser"]) == True:

        if ui.getFocusedNodeFileType() == -100:
            nihia_mix.setTrackName(0, config.widTitle[4])
        else:
            if ui.getFocusedNodeFileType() == 7 or ui.getFocusedNodeFileType() == 13 or ui.getFocusedNodeFileType() == 14 or ui.getFocusedNodeFileType() == 15:
                nihia_mix.setTrackName(0, "B| sound:")
            else:
                nihia_mix.setTrackName(0, "B| file:")

        nihia_mix.setTrackName(1, config.widTitle[4])
        nihia_mix.setTrackName(2, config.widTitle[4])
        nihia_mix.setTrackName(3, config.widTitle[4])
        nihia_mix.setTrackName(4, config.widTitle[4])
        nihia_mix.setTrackName(5, config.widTitle[4])
        nihia_mix.setTrackName(6, config.widTitle[4])
        nihia_mix.setTrackName(7, config.widTitle[4])
        
        nihia_mix.setTrackVol(0, ui.getFocusedNodeCaption()[:15])
        nihia_mix.setTrackVol(1, config.blankEvent)
        nihia_mix.setTrackVol(2, config.blankEvent)
        nihia_mix.setTrackVol(3, config.blankEvent)
        nihia_mix.setTrackVol(4, config.blankEvent)
        nihia_mix.setTrackVol(5, config.blankEvent)
        nihia_mix.setTrackVol(6, config.blankEvent)
        nihia_mix.setTrackVol(7, config.blankEvent)

        nihia_mix.setTrackPan(0, config.blankEvent)
        nihia_mix.setTrackPan(1, config.blankEvent)
        nihia_mix.setTrackPan(2, config.blankEvent)
        nihia_mix.setTrackPan(3, config.blankEvent)
        nihia_mix.setTrackPan(4, config.blankEvent)
        nihia_mix.setTrackPan(5, config.blankEvent)
        nihia_mix.setTrackPan(6, config.blankEvent)
        nihia_mix.setTrackPan(7, config.blankEvent)


    elif ui.getFocused(config.winName["Piano Roll"]) == True: 

        nihia_mix.setTrackName(0, (str(channels.getChannelName(channels.selectedChannel()))))
        nihia_mix.setTrackName(1, config.blankEvent)
        nihia_mix.setTrackName(2, config.blankEvent)
        nihia_mix.setTrackName(3, config.blankEvent)
        nihia_mix.setTrackName(4, config.blankEvent)
        nihia_mix.setTrackName(5, config.blankEvent)
        nihia_mix.setTrackName(6, config.blankEvent)
        nihia_mix.setTrackName(7, config.blankEvent)
        
        NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
        nihia_mix.setTrackVol(1, config.blankEvent)
        nihia_mix.setTrackVol(2, config.blankEvent)
        nihia_mix.setTrackVol(3, config.blankEvent)
        nihia_mix.setTrackVol(4, config.blankEvent)
        nihia_mix.setTrackVol(5, config.blankEvent)
        nihia_mix.setTrackVol(6, config.blankEvent)
        nihia_mix.setTrackVol(7, config.blankEvent)

        updatePanChannel((channels.selectedChannel() + 0), 0)
        nihia_mix.setTrackPan(1, config.blankEvent)
        nihia_mix.setTrackPan(2, config.blankEvent)
        nihia_mix.setTrackPan(3, config.blankEvent)
        nihia_mix.setTrackPan(4, config.blankEvent)
        nihia_mix.setTrackPan(5, config.blankEvent)
        nihia_mix.setTrackPan(6, config.blankEvent)
        nihia_mix.setTrackPan(7, config.blankEvent)

    elif ui.getFocused(config.winName["Mixer"]) == True:

        xy = 1.25

        if mixer.trackNumber() <= config.currentUtility:
            nihia_mix.setTrackName(0, mixer.getTrackName(mixer.trackNumber() + 0))
            nihia_mix.setTrackVol(0, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 0))) + " dB")
            updatePanMix((mixer.trackNumber() + 0), 0)

        if mixer.trackNumber() <= 125:
            nihia_mix.setTrackName(1, mixer.getTrackName(mixer.trackNumber() + 1))
            nihia_mix.setTrackVol(1, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 1))) + " dB")
            updatePanMix((mixer.trackNumber() + 1), 1)
        
        if mixer.trackNumber() <= 124:
            nihia_mix.setTrackName(2, mixer.getTrackName(mixer.trackNumber() + 2))
            nihia_mix.setTrackVol(2, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 2))) + " dB")
            updatePanMix((mixer.trackNumber() + 2), 2)

        if mixer.trackNumber() <= 123:
            nihia_mix.setTrackName(3, mixer.getTrackName(mixer.trackNumber() + 3))
            nihia_mix.setTrackVol(3, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 3))) + " dB")
            updatePanMix((mixer.trackNumber() + 3), 3)

        if mixer.trackNumber() <= 122:
            nihia_mix.setTrackName(4, mixer.getTrackName(mixer.trackNumber() + 4))
            nihia_mix.setTrackVol(4, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 4))) + " dB")
            updatePanMix((mixer.trackNumber() + 4), 4)

        if mixer.trackNumber() <= 121:
            nihia_mix.setTrackName(5, mixer.getTrackName(mixer.trackNumber() + 5))
            nihia_mix.setTrackVol(5, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 5))) + " dB")
            updatePanMix((mixer.trackNumber() + 5), 5)

        if mixer.trackNumber() <= 120:
            nihia_mix.setTrackName(6, mixer.getTrackName(mixer.trackNumber() + 6))
            nihia_mix.setTrackVol(6, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 6))) + " dB")
            updatePanMix((mixer.trackNumber() + 6), 6)

        if mixer.trackNumber() <= 119:
            nihia_mix.setTrackName(7, mixer.getTrackName(mixer.trackNumber() + 7))
            nihia_mix.setTrackVol(7, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 7))) + " dB")
            updatePanMix((mixer.trackNumber() + 7), 7)

    elif ui.getFocused(config.winName["Plugin"]) == True: 
        if ui.getFocusedPluginName() in config.supported_plugins:
            pass
            #nihia_mix.setTrackName(0, (str(channels.getChannelName(channels.selectedChannel()))))
            #NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
            #updatePanChannel((channels.selectedChannel() + 0), 0)


def VolTodB(value: float):
    if value == 0:
        dB = "- oo"
        str(dB)
    else:
        dB = (math.exp(value * 1.25 * math.log(11)) - 1) * 0.1
        dB = round(math.log10(dB) * 20, 1)
    return dB