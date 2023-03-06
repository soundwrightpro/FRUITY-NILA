import nihia
from nihia import mixer as mix

from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED as oled
from script.device_setup import config

import channels
import device 
import math
import plugins 
import ui 

def OnMidiMsg(self, event): 

    if ui.getFocused(config.winName["Channel Rack"]) == True:

        # VOLUME CONTROL

        for z in range(8):
            if channels.channelCount() > z and channels.selectedChannel() < (channels.channelCount() - z) :
                if (event.data1 == nihia.mixer.knobs[0][z]):
                    event.handled = True  
                    if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (channels.getChannelVolume(channels.selectedChannel() + z))
                        y = round(x,2)

                        if channels.getChannelVolume(channels.selectedChannel() + z) != 0 :
                            channels.setChannelVolume((channels.selectedChannel() + z), (y - config.increment) ) 
                            mix.setTrackVol(z, str(round(channels.getChannelVolume(channels.selectedChannel()+ z, 1), 1)) + " dB")
                            oled.updateText(channels.getChannelName(channels.selectedChannel() + z), z)


                    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (channels.getChannelVolume(channels.selectedChannel() + z))
                        y = round(x,2)
                        channels.setChannelVolume((channels.selectedChannel() + z), (y + config.increment) )
                        mix.setTrackVol(z, str(round(channels.getChannelVolume(channels.selectedChannel()+ z, 1), 1)) + " dB")
                        oled.updateText(channels.getChannelName(channels.selectedChannel() + z), z)
                
                mix.setTrackVolGraph(0, (channels.getChannelVolume(channels.selectedChannel() + 0)/ 1.0 * 0.86))
                
                if channels.channelCount() > 1 and channels.selectedChannel() < (channels.channelCount()-1) :
                    mix.setTrackVolGraph(1, (channels.getChannelVolume(channels.selectedChannel() + 1)/ 1.0 * 0.86))

                if channels.channelCount() > 2 and channels.selectedChannel() < (channels.channelCount()-2) :    
                    mix.setTrackVolGraph(2, (channels.getChannelVolume(channels.selectedChannel() + 2)/ 1.0 * 0.86))

                if channels.channelCount() > 3 and channels.selectedChannel() < (channels.channelCount()-3) :    
                    mix.setTrackVolGraph(3, (channels.getChannelVolume(channels.selectedChannel() + 3)/ 1.0 * 0.86))

                if channels.channelCount() > 4 and channels.selectedChannel() < (channels.channelCount()-4) :  
                    mix.setTrackVolGraph(4, (channels.getChannelVolume(channels.selectedChannel() + 4)/ 1.0 * 0.86))

                if channels.channelCount() > 5 and channels.selectedChannel() < (channels.channelCount()-5) :  
                    mix.setTrackVolGraph(5, (channels.getChannelVolume(channels.selectedChannel() + 5)/ 1.0 * 0.86))

                if channels.channelCount() > 6 and channels.selectedChannel() < (channels.channelCount()-6) :  
                    mix.setTrackVolGraph(6, (channels.getChannelVolume(channels.selectedChannel() + 6)/ 1.0 * 0.86))

                if channels.channelCount() > 7 and channels.selectedChannel() < (channels.channelCount()-7) :  
                    mix.setTrackVolGraph(7, (channels.getChannelVolume(channels.selectedChannel() + 7)/ 1.0 * 0.86))

            else:
                event.handled = True 

        # PAN CONTROL

        for z in range(8):
            if channels.channelCount() > z and channels.selectedChannel() < (channels.channelCount()-z) :
                if (event.data1 == nihia.mixer.knobs[1][z]):
                    event.handled = True  
                    if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (channels.getChannelPan(channels.selectedChannel() + z))
                        channels.setChannelPan((channels.selectedChannel() + z), (x - config.increment) )
                        oled.updatePanChannel((channels.selectedChannel() + z), z)

                    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:  
                        x = (channels.getChannelPan(channels.selectedChannel() + z))
                        channels.setChannelPan((channels.selectedChannel() + z), (x + config.increment) ) 
                        oled.updatePanChannel((channels.selectedChannel() + z), z)

                #mix.setTrackPanGraph(z, channels.getChannelPan(channels.selectedChannel() + z)) 

            else:
                event.handled = True 

