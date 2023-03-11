import nihia
from nihia import mixer as mix

from script.device_setup import NILA_core

from script.device_setup import config 
from script.device_setup import constants
from script.device_setup import transform 

import channels
import device 
import ui 

def OnMidiMsg(self, event): 

    if ui.getFocused(constants.winName["Channel Rack"]) == True:

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
                            mix.setTrackName(z,channels.getChannelName(channels.selectedChannel() + z))
                            

                    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (channels.getChannelVolume(channels.selectedChannel() + z))
                        y = round(x,2)
                        channels.setChannelVolume((channels.selectedChannel() + z), (y + config.increment) )
                        mix.setTrackVol(z, str(round(channels.getChannelVolume(channels.selectedChannel()+ z, 1), 1)) + " dB")
                        mix.setTrackName(z, channels.getChannelName(channels.selectedChannel() + z), z)
                        
                
                for x in range(8):
                    if channels.channelCount() >= x and channels.selectedChannel() <= (channels.channelCount()-x) :  
                        mix.setTrackVolGraph(x, (channels.getChannelVolume(channels.selectedChannel() + x)/ 1.0 * 0.86))

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
                        transform.updatePanChannel((channels.selectedChannel() + z), z)

                    elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:  
                        x = (channels.getChannelPan(channels.selectedChannel() + z))
                        channels.setChannelPan((channels.selectedChannel() + z), (x + config.increment) ) 
                        transform.updatePanChannel((channels.selectedChannel() + z), z)

            else:
                event.handled = True 

