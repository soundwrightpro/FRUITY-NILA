import nihia

from script.device_setup import config 
from script.device_setup import constants
from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED as oled

import channels
import ui


def OnMidiMsg(self, event):

    if ui.getFocused(constants.winName["Piano Roll"]) == True:

        #knob 0
        if (event.data1 == nihia.mixer.knobs[0][0]):
            event.handled = True  
            if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                y = round(x,2)

                if channels.getChannelVolume(channels.selectedChannel() + 0) != 0 :
                    channels.setChannelVolume((channels.selectedChannel() + 0), (y - config.increment) ) 
                    NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
                    oled.updateText(channels.getChannelName(channels.selectedChannel() + 0), 0)
                

            elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                y = round(x,2)
                channels.setChannelVolume((channels.selectedChannel() + 0), (y + config.increment) )
                NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
                oled.updateText(channels.getChannelName(channels.selectedChannel() + 0), 0)

        #knob shifted 0
        if (event.data1 == nihia.mixer.knobs[1][0]):
            event.handled = True  
            if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                x = (channels.getChannelPan(channels.selectedChannel() + 0))
                channels.setChannelPan((channels.selectedChannel() + 0), (x - config.increment) )
                oled.updatePanChannel((channels.selectedChannel() + 0), 0)

            elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                
                x = (channels.getChannelPan(channels.selectedChannel() + 0))
                channels.setChannelPan((channels.selectedChannel() + 0), (x + config.increment) ) 
                oled.updatePanChannel((channels.selectedChannel() + 0), 0)


