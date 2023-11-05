import nihia
from nihia import mixer as mix

from script.device_setup import NILA_core as core
from script.device_setup import config 
from script.device_setup import constants
from script.screen_writer import NILA_OLED as oled

import channels
import plugins
import ui 

skip = -1
z = 0
s_series = False

def plugin(self, event):
    
    if ui.getFocused(constants.winName["Plugin"]) == 1: #plugin control
        
        if (event.data1 == nihia.mixer.knobs[0][0]):
            event.handled = True
            
            if core.seriesCheck(s_series) == True: 
        
                if event.data2 in range(65, 95):
                    if channels.getChannelVolume(channels.selectedChannel() + z) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) - config.increment * 2.5)) 
                        
                elif event.data2 in range(96, 128):
                    if channels.getChannelVolume(channels.selectedChannel() + z) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) - config.increment))
                        
                elif event.data2 in range (0, 31):
                    channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) + config.increment))
                
                elif event.data2 in range (32, 64):
                    channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) + config.increment * 2.5))
            else:
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    if channels.getChannelVolume(channels.selectedChannel() + z) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) - config.increment)) 

                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    channels.setChannelVolume((channels.selectedChannel() + z), (round((channels.getChannelVolume(channels.selectedChannel() + z)), 2) + config.increment))
        
        
        if (event.data1 == nihia.mixer.knobs[1][0]):
            event.handled = True  
            if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                x = (channels.getChannelPan(channels.selectedChannel() + z))
                channels.setChannelPan((channels.selectedChannel() + z), (x - config.increment) )

            elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:  
                x = (channels.getChannelPan(channels.selectedChannel() + z))
                channels.setChannelPan((channels.selectedChannel() + z), (x + config.increment) )     
                        
        for x in range(1, 8):
            if (event.data1 == nihia.mixer.knobs[0][x]) or (event.data1 == nihia.mixer.knobs[1][x]):
                event.handled = True 
                        
                        
    oled.OnRefresh(self, event)        



