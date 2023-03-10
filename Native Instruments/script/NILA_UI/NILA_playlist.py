import nihia
from nihia import mixer as mix

from script.device_setup import config 
from script.device_setup import constants 
from script.device_setup import transform


import device 
import math
import mixer
import ui 


def OnMidiMsg(self, event): 

    if ui.getFocused(constants.winName["Playlist"]) == True: 

        # VOLUME CONTROL

        if (event.data1 == nihia.mixer.knobs[0][0]):
            event.handled = True

            if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                x = mixer.getTrackVolume(0)
                mixer.setTrackVolume((0), (x - config.increment) ) # volume values go down
                mix.setTrackVol(0, str(transform.VolTodB(mixer.getTrackVolume(0))) + " dB")
                mix.setTrackName(0, mixer.getTrackName(0))
            
            elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                x = mixer.getTrackVolume(0)
                mixer.setTrackVolume((0), (x + config.increment) ) # volume values go up
                mix.setTrackVol(0, str(transform.VolTodB(mixer.getTrackVolume(0))) + " dB")
                mix.setTrackName(0, mixer.getTrackName(0))


        # PAN CONTROL

        if (event.data1 == nihia.mixer.knobs[1][0]):
            event.handled = True

            if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                x = mixer.getTrackPan(0)
                mixer.setTrackPan((0), (x - config.increment) ) 
                transform.updatePanMix((0), 0)
            
            elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                x = mixer.getTrackPan(0)
                mixer.setTrackPan((0), (x + config.increment) )
                transform.updatePanMix((0), 0)
