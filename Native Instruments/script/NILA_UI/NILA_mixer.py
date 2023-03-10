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
       
    """
    Final track is the 'current' track, which is a special analysis track that has no
    volume or pan controls. We are not interested in this track as we cannot control it.
    """

    if ui.getFocused(constants.winName["Mixer"]) == True: 

        # VOLUME CONTROL

        for z in range(8):
            if mixer.trackNumber() <= constants.currentUtility - z:
                if (event.data1 == nihia.mixer.knobs[0][z]):
                    event.handled = True
                    if mixer.getTrackName(mixer.trackNumber()+z) == "Current" and mixer.trackNumber()+z >= constants.currentUtility:
                        pass
                    else:
                        if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                            x = (mixer.getTrackVolume(mixer.trackNumber() + z))
                            mixer.setTrackVolume((mixer.trackNumber() + z), (x - config.increment) ) # volume values go down
                            mix.setTrackVol(z, str(transform.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + z))) + " dB")
                            mix.setTrackName(z, mixer.getTrackName(mixer.trackNumber() + z))
                        
                        elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                            x = (mixer.getTrackVolume(mixer.trackNumber() + z))
                            mixer.setTrackVolume((mixer.trackNumber() + z), (x + config.increment) ) # volume values go up
                            mix.setTrackVol(z, str(transform.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + z))) + " dB")
                            mix.setTrackName(z, mixer.getTrackName(mixer.trackNumber() + z))

            elif mixer.trackNumber() + z >= constants.currentUtility:
                pass     
                mix.setTrackName(z, constants.blankEvent)
                mix.setTrackVol(z, constants.blankEvent) 

        # PAN CONTROL

        for z in range(8):
            if mixer.trackNumber() <= constants.currentUtility - z:
                if (event.data1 == nihia.mixer.knobs[1][z]):
                    event.handled = True

                    if mixer.trackNumber() + z >= constants.currentUtility - z:
                        mix.setTrackPan(z, constants.blankEvent)
                    else:
                        if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                            x = (mixer.getTrackPan(mixer.trackNumber() + z))
                            mixer.setTrackPan((mixer.trackNumber() + z), (x - config.increment) ) 
                            transform.updatePanMix((mixer.trackNumber() + z), z)
                        
                        elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                            x = (mixer.getTrackPan(mixer.trackNumber() + z))
                            mixer.setTrackPan((mixer.trackNumber() + z), (x + config.increment) )
                            transform.updatePanMix((mixer.trackNumber() + z), z)


