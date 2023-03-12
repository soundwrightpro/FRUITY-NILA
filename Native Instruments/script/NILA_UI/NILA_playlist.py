import nihia
from nihia import mixer as mix

from script.device_setup import config 
from script.device_setup import constants 
from script.device_setup import transform
from script.screen_writer import NILA_OLED as oled


import mixer
import ui 


def OnMidiMsg(self, event): 

    if ui.getFocused(constants.winName["Playlist"]) == True:
        
        #oled.OnRefresh(self, event) 

        # VOLUME CONTROL

        if (event.data1 == nihia.mixer.knobs[0][0]):
            event.handled = True

            if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                x = mixer.getTrackVolume(0)
                mixer.setTrackVolume((0), (x - config.increment) ) # volume values go down

            elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                x = mixer.getTrackVolume(0)
                mixer.setTrackVolume((0), (x + config.increment) ) # volume values go up

