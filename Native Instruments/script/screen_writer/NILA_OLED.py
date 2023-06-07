from nihia import mixer as mix

from script.device_setup import NILA_core
from script.device_setup import constants 
from script.device_setup import transform

import channels
import mixer
import plugins
import transport
import ui
import device
import math



def OnRefresh(self, event):
    
    self.kompleteInstance = None
    
    if plugins.isValid(channels.selectedChannel()) == True:                                   # Checks if plugin exists
        if plugins.getPluginName(channels.selectedChannel()) == "Komplete Kontrol":           # Checks if plugin is Komplete Kontrol
            if self.kompleteInstance != plugins.getParamName(0, channels.selectedChannel()):  # Checks against cache and updates if necessary
                self.kompleteInstance = plugins.getParamName(0, channels.selectedChannel())
                mix.setTrackKompleteInstance(0, plugins.getParamName(0, channels.selectedChannel()))
        
        else:
            if self.kompleteInstance != "":  # Checks against cache and updates if necessary
                self.kompleteInstance = ""
                mix.setTrackKompleteInstance(0, "")

    else:
        if self.kompleteInstance != "":  # Checks against cache and updates if necessary
            self.kompleteInstance = ""
            mix.setTrackKompleteInstance(0, "")


    if ui.getFocused(constants.winName["Mixer"]) == True: 

        for x in range(8):
            if mixer.trackNumber() <= constants.currentUtility - x:
                if mixer.trackNumber() + x == constants.currentUtility:
                     mix.setTrackExist(x,0)
                     if mixer.trackNumber() == constants.currentUtility:
                         clear_all()
                else:
                    mix.setTrackExist(x,1)
                    mix.setTrackName(x, mixer.getTrackName(mixer.trackNumber() + x))
                    mix.setTrackVol(x, str(transform.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + x))) + " dB")
                    mix.setTrackVolGraph(x, (mixer.getTrackVolume(mixer.trackNumber() + x)))
                    transform.updatePanMix((mixer.trackNumber() + x), x)
                    mix.setTrackSel(0,1)

            else:
                mix.setTrackExist(x,0)

    if ui.getFocused(constants.winName["Channel Rack"]) == True:

        for x in range(8):
            if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
                mix.setTrackExist(x, 1)
                mix.setTrackName(x, channels.getChannelName(channels.selectedChannel() + x))
                mix.setTrackVol(x, str(round(channels.getChannelVolume(channels.selectedChannel() + x, 1), 1)) + " dB")
                mix.setTrackVolGraph(x, (channels.getChannelVolume(channels.selectedChannel() + x)/ 1.0 * 0.86))
                transform.updatePanChannel((channels.selectedChannel() + x), x)
                mix.setTrackSel(0,0)

            else:
                mix.setTrackExist(x, 0)
           

    if ui.getFocused(constants.winName["Plugin"]) == True: 

        clear_all()
        remove_part()

        if ui.getFocusedPluginName() in constants.supported_plugins:
            
            mix.setTrackName(1, "supported plugin")
            
            for y in range(8):
                mix.setTrackExist(y,2)
        else:
            clear_all()
            mix.setTrackName(0, ui.getFocusedPluginName())


            for y in range(1,8):
                mix.setTrackExist(y,0)           

    if ui.getFocused(constants.winName["Piano Roll"]) == True: #piano roll:

        remove_part()
        clear_part()

        mix.setTrackName(0, (str(channels.getChannelName(channels.selectedChannel()))))
        NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
        transform.updatePanChannel((channels.selectedChannel() + 0), 0)


    if ui.getFocused(constants.winName["Playlist"]) == True: #playlist

        mix.setTrackName(0, "Playlist")
        mix.setTrackVolGraph(0, mixer.getTrackVolume(0))
        
        
def OnUpdateBeatIndicator(self, Value):

    if ui.getFocused(constants.winName["Playlist"]) == True:
        
        timeDisp, currentTime = NILA_core.timeConvert(constants.itemDisp, constants.itemTime)

        mix.setTrackName(0, str("Playlist"))

        split_message = ui.getHintMsg()
        split_point1 = ' - '
        split_point2 = ' to '

        if split_point1 in split_message.lower():
            split_hint = split_message.partition(split_point1)[2]
        else:
            split_hint = split_message.partition(split_point2)[2]

        if device.getName() == "Komplete Kontrol DAW - 1":
            mix.setTrackVol(0, str("|" + currentTime))

        else:
            if transport.isPlaying() == True:    
                if timeDisp == "Beats:Bar" and len(currentTime) >= 5:
                    timeDisp = "B:B"
                    mix.setTrackVol(0, str(timeDisp + "|" + currentTime))
                else:
                    mix.setTrackVol(0, str(timeDisp + "|" + currentTime))

                if timeDisp == "Min:Sec" and len(currentTime) > 5:
                    timeDisp = "M:S"
                    mix.setTrackVol(0, str(timeDisp + "|" + currentTime))
                else:
                    mix.setTrackVol(0, str(timeDisp + "|" + currentTime))

            else:    
                mix.setTrackVol(0, str(split_hint[:7] + "|" + currentTime))
                mix.setTrackVolGraph(0, mixer.getTrackVolume(0))

    else:
        pass


def OnIdle(self):
    
    #print(plugins.getParamName(0, channels.selectedChannel()))


    if ui.getFocused(constants.winName["Playlist"]) == True:
        
        remove_part()
        clear_part()
        
        mix.setTrackVolGraph(0, mixer.getTrackVolume(0))
        
        timeDisp, currentTime = NILA_core.timeConvert(constants.itemDisp, constants.itemTime)

        split_message = ui.getHintMsg()
        split_point1 = ' - '
        split_point2 = ' to '

        if split_point1 in split_message.lower():
            split_hint = split_message.partition(split_point1)[2]
        else:
            split_hint = split_message.partition(split_point2)[2]


        mix.setTrackName(0, "Playlist")
        if transport.isPlaying() == False:
            if "Volume" in split_hint[:7]:
                pass
            else:
                mix.setTrackVol(0, str(split_hint[:7] + "|" + currentTime))
  
    if ui.getFocused(constants.winName["Browser"]) == True: 

        fileType = ui.getFocusedNodeFileType()

        if device.getName() == "Komplete Kontrol DAW - 1":
            remove_part()

            mix.setTrackName(0, "Browser")
            mix.setTrackVol(0, "   ")
            transform.updatePanMix((mixer.trackNumber() + 0), 1)
            mix.setTrackVolGraph(0, 0)

            if transport.isPlaying() == False:
                mix.setTrackVolGraph(0, 0)
                transform.sendPeakInfo()
            else:
                pass

        else:
            
            remove_part()

            if ui.getFocusedNodeFileType() <= -100:
                fileType = "Browser"
            else: 
                for key, value in constants.FL_node.items():
                    if ui.getFocusedNodeFileType() == value:
                        fileType = key

            mix.setTrackName(0, str(fileType))
            mix.setTrackVol(0, ui.getFocusedNodeCaption()[:15])
          
                       
def remove_part(): # remove tracks 1 to 7

    for y in range(1,8):
        mix.setTrackExist(y,0)
    mix.setTrackSel(0,0)


def remove_all(): #remove tracks 0 to 7
    
    for y in range(8):
        mix.setTrackExist(y,0)
    mix.setTrackSel(0,0)

      
def clear_part():
    
    for y in range(1,8):
        mix.setTrackPanGraph(y, 0)
        mix.setTrackVolGraph(y, 0)
        mix.setTrackSel(0,0)
        mix.setTrackArm(y, 0)
        mix.setTrackSolo(y, 0)
        mix.setTrackMute(y, 0)
        mix.setTrackName(y, constants.blankEvent)
        mix.setTrackPan(y, constants.blankEvent)
        mix.setTrackVol(y, constants.blankEvent)        

        
def clear_all():
    
    for y in range(8):
        mix.setTrackPanGraph(y, 0)
        mix.setTrackVolGraph(y, 0)
        mix.setTrackSel(0,0)
        mix.setTrackArm(y, 0)
        mix.setTrackSolo(y, 0)
        mix.setTrackMute(y, 0)
        mix.setTrackName(y, constants.blankEvent)
        mix.setTrackPan(y, constants.blankEvent)
        mix.setTrackVol(y, constants.blankEvent)