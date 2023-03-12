import nihia
from nihia import *

from script.device_setup import NILA_core as core

from script.device_setup import config 
from script.device_setup import constants
from script.device_setup import transform 
from script.screen_writer import NILA_OLED as oled

import channels
import device 
import ui 

def OnMidiMsg(self, event): 

    if ui.getFocused(constants.winName["Channel Rack"]) == True:

        # VOLUME CONTROL
        s_series = False

        for z in range(8):
            if channels.channelCount() > z and channels.selectedChannel() < (channels.channelCount() - z) :
                if (event.data1 == nihia.mixer.knobs[0][z]):
                    event.handled = True 
                    
                    if core.seriesCheck(s_series) == True: 
                         
                        if nihia.mixer.KNOB_INCREASE_MAX_SPEED <= event.data2:
                            if channels.getChannelVolume(channels.selectedChannel() + z) != 0 :
                                channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) - config.increment)) 
                       
                        elif nihia.mixer.KNOB_DECREASE_MAX_SPEED >= event.data2:
                            channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) + config.increment))

                    else:
                        if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                            if channels.getChannelVolume(channels.selectedChannel() + z) != 0 :
                                channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) - config.increment)) 

                        elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                            channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) + config.increment))
                            
                oled.OnRefresh(self, event)

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

                    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:  
                        x = (channels.getChannelPan(channels.selectedChannel() + z))
                        channels.setChannelPan((channels.selectedChannel() + z), (x + config.increment) ) 
            else:
                event.handled = True 

