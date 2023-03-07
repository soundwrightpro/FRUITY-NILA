from nihia import mixer as nihia_mix

from script.device_setup import NILA_core
from script.device_setup import constants 

from script.NILA_UI import NILA_plugins


import channels
import math
import mixer
import time
import transport
import ui
import device 
import midi 



def updatePanMix(self,track):

    if mixer.getTrackPan(self) == 0:
        nihia_mix.setTrackPan(track, "Centered")
    elif mixer.getTrackPan(self) > 0:
        nihia_mix.setTrackPan(track, str(round(mixer.getTrackPan(self) * 100)) + "% " + "Right")
    elif mixer.getTrackPan(self) < 0:
        nihia_mix.setTrackPan(track, str(round(mixer.getTrackPan(self) * -100)) + "% " + "Left")

    for x in range(8):
        if mixer.trackNumber() <= constants.currentUtility - x:
            nihia_mix.setTrackPanGraph(x, mixer.getTrackPan(mixer.trackNumber() + x))


def updatePanChannel(self,track):

    if channels.getChannelPan(self) == 0:
        nihia_mix.setTrackPan(track, "Centered")
    elif channels.getChannelPan(self) > 0:
        nihia_mix.setTrackPan(track, str(round(channels.getChannelPan(self) * 100)) + "% " + "Right")
    elif channels.getChannelPan(self) < 0:
        nihia_mix.setTrackPan(track, str(round(channels.getChannelPan(self) * -100)) + "% " + "Left")

    nihia_mix.setTrackPanGraph(0, channels.getChannelPan(channels.selectedChannel() + 0))     

    for x in range(1,8):
        if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount()-x) :  
            nihia_mix.setTrackPanGraph(x, channels.getChannelPan(channels.selectedChannel() + x)) 


def updateText(self,track):

    nihia_mix.setTrackName(track, self)


def sendPeakInfo():

    TrackPeaks = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for x in range(8):
        if ui.getFocused(constants.winName["Mixer"]) == True:
            if mixer.trackNumber() <= constants.currentUtility - x:
                TrackPeaks[(x*2) + 0] = mixer.getTrackPeaks((mixer.trackNumber() + x), midi.PEAK_L)
                TrackPeaks[(x*2) + 1] = mixer.getTrackPeaks((mixer.trackNumber() + x), midi.PEAK_R)

        elif ui.getFocused(constants.winName["Channel Rack"]) == True:

            if channels.getTargetFxTrack((channels.selectedChannel()+0)) > 0:
                TrackPeaks[0] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+0)), midi.PEAK_L)
                TrackPeaks[1]  = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+0)), midi.PEAK_R) 

            if channels.channelCount() > 1 and channels.selectedChannel() < (channels.channelCount() - 1):
                if channels.getTargetFxTrack((channels.selectedChannel()+1)) > 0:
                    TrackPeaks[2] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+1)), midi.PEAK_L)
                    TrackPeaks[3]  = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+1)), midi.PEAK_R) 

            if channels.channelCount() > 2 and channels.selectedChannel() < (channels.channelCount() - 2):
                if channels.getTargetFxTrack((channels.selectedChannel()+2)) > 0:
                    TrackPeaks[4] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+2)), midi.PEAK_L)
                    TrackPeaks[5]  = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+2)), midi.PEAK_R) 

            if channels.channelCount() > 3 and channels.selectedChannel() < (channels.channelCount() - 3):
                if channels.getTargetFxTrack((channels.selectedChannel()+3)) > 0:
                    TrackPeaks[6] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+3)), midi.PEAK_L)
                    TrackPeaks[7]  = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+3)), midi.PEAK_R) 

            if channels.channelCount() > 4 and channels.selectedChannel() < (channels.channelCount() - 4):
                if channels.getTargetFxTrack((channels.selectedChannel()+4)) > 0:
                    TrackPeaks[8] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+4)), midi.PEAK_L)
                    TrackPeaks[9]  = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+4)), midi.PEAK_R) 

            if channels.channelCount() > 5 and channels.selectedChannel() < (channels.channelCount() - 5):
                if channels.getTargetFxTrack((channels.selectedChannel()+5)) > 0:
                    TrackPeaks[10] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+5)), midi.PEAK_L)
                    TrackPeaks[11]  = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+5)), midi.PEAK_R) 

            if channels.channelCount() > 6 and channels.selectedChannel() < (channels.channelCount() - 6):
                if channels.getTargetFxTrack((channels.selectedChannel()+6)) > 0:
                    TrackPeaks[12] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+6)), midi.PEAK_L)
                    TrackPeaks[13]  = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+6)), midi.PEAK_R) 

            if channels.channelCount() > 7 and channels.selectedChannel() < (channels.channelCount() - 7):
                if channels.getTargetFxTrack((channels.selectedChannel()+7)) > 0:
                    TrackPeaks[14] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+7)), midi.PEAK_L)
                    TrackPeaks[15]  = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel()+7)), midi.PEAK_R) 

      
    if ui.getFocused(constants.winName["Browser"]) == True or ui.getFocused(constants.winName["Playlist"]) == True:
        TrackPeaks[0] = mixer.getTrackPeaks((mixer.trackNumber() + 0), midi.PEAK_L)
        TrackPeaks[1] = mixer.getTrackPeaks((mixer.trackNumber() + 0), midi.PEAK_R)
            

    for x in range(0, 16):
        if TrackPeaks[x] > 1.1:
            TrackPeaks[x] = 1.1

        TrackPeaks[x] = TrackPeaks[x] * (127 / 1.1)
        TrackPeaks[x] = int(math.trunc(TrackPeaks[x]))

    nihia_mix.sendPeakMeterData(TrackPeaks)


def OnRefresh(self, event):
 
    if ui.getFocused(constants.winName["Mixer"]) == True: 

        for x in range(8):
            if mixer.trackNumber() <= (125 - x):
                nihia_mix.setTrackExist(x,1)
                nihia_mix.setTrackName(x, mixer.getTrackName(mixer.trackNumber() + x))
                nihia_mix.setTrackVol(x, str(VolTodB(mixer.getTrackVolume(mixer.trackNumber() + x))) + " dB")
                nihia_mix.setTrackVolGraph(x, mixer.getTrackVolume(mixer.trackNumber() + x))
                updatePanMix((mixer.trackNumber() + x), x)
            else:
                nihia_mix.setTrackExist(x,0)

    elif ui.getFocused(constants.winName["Channel Rack"]) == True:

        for x in range(8):
            if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x) :
                nihia_mix.setTrackExist(x, 1)
                nihia_mix.setTrackName(x, channels.getChannelName(channels.selectedChannel() + x))
                nihia_mix.setTrackVol(x, str(round(channels.getChannelVolume(channels.selectedChannel() + x, 1), 1)) + " dB")
                nihia_mix.setTrackVolGraph(x, (channels.getChannelVolume(channels.selectedChannel() + x)/ 1.0 * 0.86))
                updatePanChannel((channels.selectedChannel() + x), x)

            else:
                nihia_mix.setTrackExist(x, 0)
                nihia_mix.setTrackName(x, (constants.blankEvent))
                NILA_core.setTrackVolConvert(x, constants.blankEvent)
                nihia_mix.setTrackPan(x, constants.blankEvent)



    elif ui.getFocused(constants.winName["Plugin"]) == True: 

        clear()

        if ui.getFocusedPluginName() in constants.supported_plugins:
            updateText(ui.getFocusedPluginName(), 0)
            updateText("supported plugin", 1)

            for y in range(8):
                nihia_mix.setTrackExist(y,2)
        else:
            clear()
            updateText(ui.getFocusedPluginName(), 0)

            for y in range(1,8):
                nihia_mix.setTrackExist(y,0)           


    if ui.getFocused(constants.winName["Piano Roll"]) == True: #piano roll:

        for x in range(1,8):
            nihia_mix.setTrackExist(x,0)

        nihia_mix.setTrackName(0, (str(channels.getChannelName(channels.selectedChannel()))))
        nihia_mix.setTrackName(1, constants.blankEvent)
        nihia_mix.setTrackName(2, constants.blankEvent)
        nihia_mix.setTrackName(3, constants.blankEvent)
        nihia_mix.setTrackName(4, constants.blankEvent)
        nihia_mix.setTrackName(5, constants.blankEvent)
        nihia_mix.setTrackName(6, constants.blankEvent)
        nihia_mix.setTrackName(7, constants.blankEvent)
        
        NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
        nihia_mix.setTrackVol(1, constants.blankEvent)
        nihia_mix.setTrackVol(2, constants.blankEvent)
        nihia_mix.setTrackVol(3, constants.blankEvent)
        nihia_mix.setTrackVol(4, constants.blankEvent)
        nihia_mix.setTrackVol(5, constants.blankEvent)
        nihia_mix.setTrackVol(6, constants.blankEvent)
        nihia_mix.setTrackVol(7, constants.blankEvent)

        updatePanChannel((channels.selectedChannel() + 0), 0)
        nihia_mix.setTrackPan(1, constants.blankEvent)
        nihia_mix.setTrackPan(2, constants.blankEvent)
        nihia_mix.setTrackPan(3, constants.blankEvent)
        nihia_mix.setTrackPan(4, constants.blankEvent)
        nihia_mix.setTrackPan(5, constants.blankEvent)
        nihia_mix.setTrackPan(6, constants.blankEvent)
        nihia_mix.setTrackPan(7, constants.blankEvent)

    if ui.getFocused(constants.winName["Playlist"]) == True: #playlist

        for x in range(1,8):
            nihia_mix.setTrackExist(x,0)

        nihia_mix.setTrackName(0, "Playlist")
        nihia_mix.setTrackName(1, constants.blankEvent)
        nihia_mix.setTrackName(2, constants.blankEvent)
        nihia_mix.setTrackName(3, constants.blankEvent)
        nihia_mix.setTrackName(4, constants.blankEvent)
        nihia_mix.setTrackName(5, constants.blankEvent)
        nihia_mix.setTrackName(6, constants.blankEvent)
        nihia_mix.setTrackName(7, constants.blankEvent)
        
        #nihia_mix.setTrackVol(1, constants.blankEvent)
        nihia_mix.setTrackVol(1, constants.blankEvent)
        nihia_mix.setTrackVol(2, constants.blankEvent)
        nihia_mix.setTrackVol(3, constants.blankEvent)
        nihia_mix.setTrackVol(4, constants.blankEvent)
        nihia_mix.setTrackVol(5, constants.blankEvent)
        nihia_mix.setTrackVol(6, constants.blankEvent)
        nihia_mix.setTrackVol(7, constants.blankEvent)

        nihia_mix.setTrackPan(0, constants.blankEvent)
        nihia_mix.setTrackPan(1, constants.blankEvent)
        nihia_mix.setTrackPan(2, constants.blankEvent)
        nihia_mix.setTrackPan(3, constants.blankEvent)
        nihia_mix.setTrackPan(4, constants.blankEvent)
        nihia_mix.setTrackPan(5, constants.blankEvent)
        nihia_mix.setTrackPan(6, constants.blankEvent)
        nihia_mix.setTrackPan(7, constants.blankEvent)

def clear():

    for y in range(1,8):
        nihia_mix.setTrackExist(y,0)

    for y in range(8):
        nihia_mix.setTrackPanGraph(y, 0)
        nihia_mix.setTrackArm(y, 0)
        nihia_mix.setTrackSolo(y, 0)
        nihia_mix.setTrackMute(y, 0)
        updateText(constants.blankEvent, y)
        nihia_mix.setTrackName(y, constants.blankEvent)
        nihia_mix.setTrackPan(y, constants.blankEvent)
        nihia_mix.setTrackVol(y, constants.blankEvent)



def OnUpdateBeatIndicator(self, Value):

    if ui.getFocused(constants.winName["Playlist"]) == True:

        timeDisp, currentTime = NILA_core.timeConvert(constants.itemDisp, constants.itemTime)

        #if transport.isPlaying() == True:
        #    nihia_mix.setTrackName(0, str("P| "+ ))
        #else:

        for x in range(1,8):
            nihia_mix.setTrackExist(x,0)

        nihia_mix.setTrackName(0, str("Playlist"))
        nihia_mix.setTrackName(1, constants.blankEvent)
        nihia_mix.setTrackName(2, constants.blankEvent)
        nihia_mix.setTrackName(3, constants.blankEvent)
        nihia_mix.setTrackName(4, constants.blankEvent)
        nihia_mix.setTrackName(5, constants.blankEvent)
        nihia_mix.setTrackName(6, constants.blankEvent)
        nihia_mix.setTrackName(7, constants.blankEvent)

        split_message = ui.getHintMsg()
        split_point1 = ' - '
        split_point2 = ' to '

        if split_point1 in split_message.lower():
            split_hint = split_message.partition(split_point1)[2]
        else:
            split_hint = split_message.partition(split_point2)[2]

        if device.getName() == "Komplete Kontrol DAW - 1":
            nihia_mix.setTrackVol(0, str("|" + currentTime))

        else:
            if transport.isPlaying() == True:    
                if timeDisp == "Beats:Bar" and len(currentTime) >= 5:
                    timeDisp = "B:B"
                    nihia_mix.setTrackVol(0, str(timeDisp + "|" + currentTime))
                else:
                    nihia_mix.setTrackVol(0, str(timeDisp + "|" + currentTime))

                if timeDisp == "Min:Sec" and len(currentTime) > 5:
                    timeDisp = "M:S"
                    nihia_mix.setTrackVol(0, str(timeDisp + "|" + currentTime))
                else:
                    nihia_mix.setTrackVol(0, str(timeDisp + "|" + currentTime))

            else:    
                nihia_mix.setTrackVol(0, str(split_hint[:7] + "|" + currentTime))

        nihia_mix.setTrackVol(1, constants.blankEvent)
        nihia_mix.setTrackVol(2, constants.blankEvent)
        nihia_mix.setTrackVol(3, constants.blankEvent)
        nihia_mix.setTrackVol(4, constants.blankEvent)
        nihia_mix.setTrackVol(5, constants.blankEvent)
        nihia_mix.setTrackVol(6, constants.blankEvent)
        nihia_mix.setTrackVol(7, constants.blankEvent)

        nihia_mix.setTrackPan(0, constants.blankEvent)
        nihia_mix.setTrackPan(1, constants.blankEvent)
        nihia_mix.setTrackPan(2, constants.blankEvent)
        nihia_mix.setTrackPan(3, constants.blankEvent)
        nihia_mix.setTrackPan(4, constants.blankEvent)
        nihia_mix.setTrackPan(5, constants.blankEvent)
        nihia_mix.setTrackPan(6, constants.blankEvent)
        nihia_mix.setTrackPan(7, constants.blankEvent)

    else:
        pass


def VolTodB(value: float):

    if value == 0:
        dB = "- oo"
        str(dB)
    else:
        dB = (math.exp(value * 1.25 * math.log(11)) - 1) * 0.1
        dB = round(math.log10(dB) * 20, 1)
    return dB


def OnIdle(self):

    if ui.getFocused(constants.winName["Playlist"]) == True:

        timeDisp, currentTime = NILA_core.timeConvert(constants.itemDisp, constants.itemTime)
        updatePlaylist()

        split_message = ui.getHintMsg()
        split_point1 = ' - '
        split_point2 = ' to '

        if split_point1 in split_message.lower():
            split_hint = split_message.partition(split_point1)[2]
        else:
            split_hint = split_message.partition(split_point2)[2]


        nihia_mix.setTrackName(0, "Playlist")
        if transport.isPlaying() == False:
            nihia_mix.setTrackVol(0, str(split_hint[:7] + "|" + currentTime))
  
    elif ui.getFocused(constants.winName["Browser"]) == True: 
        updateBrowser()

def updatePlaylist():

    if ui.getFocused(constants.winName["Playlist"]) == True:

        if device.getName() == "Komplete Kontrol DAW - 1":
            for x in range(1,8):
                nihia_mix.setTrackExist(x,0)


            updatePanMix((mixer.trackNumber() + 0), 0)
            sendPeakInfo()

            if transport.isPlaying() == False:
                nihia_mix.setTrackVolGraph(0, 0)
                sendPeakInfo()
            else:
                pass

def updateBrowser():

    if ui.getFocused(constants.winName["Browser"]) == True:

        fileType = ui.getFocusedNodeFileType()

        if device.getName() == "Komplete Kontrol DAW - 1":
            for x in range(1,8):
                nihia_mix.setTrackExist(x,0)

            nihia_mix.setTrackName(0, "Browser")
            nihia_mix.setTrackVol(0, "   ")
            updatePanMix((mixer.trackNumber() + 0), 1)

            if transport.isPlaying() == False:
                nihia_mix.setTrackVolGraph(0, 0)
                sendPeakInfo()
            else:
                pass

        else:
            
            for x in range(1,8):
                nihia_mix.setTrackExist(x,0)

            if ui.getFocusedNodeFileType() == -100:
                fileType = "Browser"

            else:

                if ui.getFocusedNodeFileType() == -100:
                    fileType = "Browser"

                else:           

                    if ui.getFocusedNodeFileType() == constants.SBN_FLP:
                        fileType = "B| FLP File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_ZIP:
                        fileType = "B| ZIP File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_FLM:
                        fileType = "B| FLP File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_FST:
                        fileType = "B| Preset"
                        
                    elif ui.getFocusedNodeFileType() == constants.SBN_WAV:
                        fileType = "B| WAV File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_MP3:
                        fileType = "B| MP3 File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_OGG:
                        fileType = "B| OGG File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_FLAC:
                        fileType = "B| FLAC File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_AIFF:
                        fileType = "B| AIFF File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_TXT:
                        fileType = "B| TEXT File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_BMP:
                        fileType = "B| IMAGE File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_MID:
                        fileType = "B| MIDI File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_M4A:
                        fileType = "B| MP4 File"

                    elif ui.getFocusedNodeFileType() == constants.SBN_FSC:
                        fileType = "B| FSC File"
                    else:
                        fileType = "B| File"

                nihia_mix.setTrackName(0, str(fileType))
                nihia_mix.setTrackVol(0, ui.getFocusedNodeCaption()[:15])
