from nihia import mixer as mix

from script.device_setup import constants 

import channels
import playlist
import math
import mixer
import ui
import midi 
import transport 


def VolTodB(value: float):

    if value == 0:
        dB = "- oo"
        str(dB)
    else:
        dB = (math.exp(value * 1.25 * math.log(11)) - 1) * 0.1
        dB = round(math.log10(dB) * 20, 1)
    return dB


def updatePanMix(self,track):

    if mixer.getTrackPan(self) == 0:
        mix.setTrackPan(track, "Centered")
    elif mixer.getTrackPan(self) > 0:
        mix.setTrackPan(track, str(round(mixer.getTrackPan(self) * 100)) + "% " + "Right")
    elif mixer.getTrackPan(self) < 0:
        mix.setTrackPan(track, str(round(mixer.getTrackPan(self) * -100)) + "% " + "Left")

    for x in range(8):
        if mixer.trackNumber() <= constants.currentUtility - x:
            mix.setTrackPanGraph(x, mixer.getTrackPan(mixer.trackNumber() + x))


def updatePanChannel(self,track):

    if channels.getChannelPan(self) == 0:
        mix.setTrackPan(track, "Centered")
    elif channels.getChannelPan(self) > 0:
        mix.setTrackPan(track, str(round(channels.getChannelPan(self) * 100)) + "% " + "Right")
    elif channels.getChannelPan(self) < 0:
        mix.setTrackPan(track, str(round(channels.getChannelPan(self) * -100)) + "% " + "Left")

    mix.setTrackPanGraph(0, channels.getChannelPan(channels.selectedChannel() + 0))     

    for x in range(1,8):
        if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount()-x) :  
            mix.setTrackPanGraph(x, channels.getChannelPan(channels.selectedChannel() + x)) 


def sendPeakInfo():

    TrackPeaks = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if transport.isPlaying() == True:
        
        if ui.getFocused(constants.winName["Mixer"]) == True:
            for x in range(8):   
                if mixer.trackNumber() <= constants.currentUtility - x:
                    TrackPeaks[(x*2) + 0] = mixer.getTrackPeaks((mixer.trackNumber() + x), midi.PEAK_L)
                    TrackPeaks[(x*2) + 1] = mixer.getTrackPeaks((mixer.trackNumber() + x), midi.PEAK_R)

        elif ui.getFocused(constants.winName["Channel Rack"]) == True:
            for x in range(8):
                if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
                    if channels.getTargetFxTrack((channels.selectedChannel() + x)) > 0:
                        TrackPeaks[(x*2) + 0] = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel() + x)), midi.PEAK_L)
                        TrackPeaks[(x*2) + 1]  = mixer.getTrackPeaks(channels.getTargetFxTrack((channels.selectedChannel() + x)), midi.PEAK_R)       
        
        elif ui.getFocused(constants.winName["Playlist"]) == True:
            
            TrackPeaks[0] = mixer.getTrackPeaks(0, midi.PEAK_L)
            TrackPeaks[1] = mixer.getTrackPeaks(0, midi.PEAK_R)
                
        if ui.getFocused(constants.winName["Browser"]) == True or ui.getFocused(constants.winName["Playlist"]) == True:
            
            TrackPeaks[0] = mixer.getTrackPeaks(0, midi.PEAK_L)
            TrackPeaks[1] = mixer.getTrackPeaks(0, midi.PEAK_R)
                
        for x in range(0, 16):
            if TrackPeaks[x] > 1.1:
                TrackPeaks[x] = 1.1

            TrackPeaks[x] = TrackPeaks[x] * (127 / 1.1)
            TrackPeaks[x] = int(math.trunc(TrackPeaks[x]))

        mix.sendPeakMeterData(TrackPeaks)
    else:
        pass


def timeConvert(timeDisp, currentTime):

   currentBar = str(playlist.getVisTimeBar())
   currentStep = str(playlist.getVisTimeStep())
   currentTick = str(playlist.getVisTimeTick())

   zeroStr = str(0)

   if int(currentStep) <= 9 and int(currentStep) >= 0:
      currentTime = str(currentBar+":"+zeroStr+currentStep)
   elif int(currentStep) >= 0:
      currentTime = str(currentBar+":"+currentStep)
   elif int(currentStep) < 0:
      currentTime = str(currentStep)

   if ui.getTimeDispMin() == True and int(currentStep) >= 0:
      timeDisp = "Min:Sec"
   elif ui.getTimeDispMin() == False and int(currentStep) >= 0:
      timeDisp = "Beats:Bar"
   elif int(currentStep) <= 0:
      timeDisp = "REC in..."
   
   return timeDisp, currentTime


def setTrackVolConvert(trackID: int, value: str):
   if value == "-inf dB":
      value = "- oo dB"

   mix.setTrackVol(trackID, value)