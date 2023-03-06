import nihia
from nihia import mixer as mix

from script.screen_writer import NILA_OLED as oled
from script.device_setup import config 

import device 
import math
import mixer
import ui 


def OnMidiMsg(self, event): 
       
    """
    Final track is the 'current' track, which is a special analysis track that has no
    volume or pan controls. We are not interested in this track as we cannot control it.
    """

    if ui.getFocused(config.winName["Mixer"]) == True: 

        # VOLUME CONTROL


        for z in range(8):
            if mixer.trackNumber() <= config.currentUtility - z:
                if (event.data1 == nihia.mixer.knobs[0][z]):
                    event.handled = True
                    if mixer.getTrackName(mixer.trackNumber()+z) == "Current" and mixer.trackNumber()+z >= config.currentUtility:
                        pass
                    else:
                        if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                            x = (mixer.getTrackVolume(mixer.trackNumber() + z))
                            mixer.setTrackVolume((mixer.trackNumber() + z), (x - config.increment) ) # volume values go down
                            mix.setTrackVol(z, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + z))) + " dB")
                            oled.updateText(mixer.getTrackName(mixer.trackNumber() + z), z)
                        
                        elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                            x = (mixer.getTrackVolume(mixer.trackNumber() + z))
                            mixer.setTrackVolume((mixer.trackNumber() + z), (x + config.increment) ) # volume values go up
                            mix.setTrackVol(z, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + z))) + " dB")
                            oled.updateText(mixer.getTrackName(mixer.trackNumber() + z), z)

            elif mixer.trackNumber() + z >= config.currentUtility:
                pass     
                mix.setTrackName(z, config.blankEvent)
                mix.setTrackVol(z, config.blankEvent) 

        # PAN CONTROL

        for z in range(8):
            if mixer.trackNumber() <= config.currentUtility - z:
                if (event.data1 == nihia.mixer.knobs[1][z]):
                    event.handled = True

                    if mixer.trackNumber() + z >= config.currentUtility - z:
                        mix.setTrackPan(z, config.blankEvent)
                    else:
                        if nihia.mixer.KNOB_DECREASE_MIN_SPEED >= event.data2 >= nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                            x = (mixer.getTrackPan(mixer.trackNumber() + z))
                            mixer.setTrackPan((mixer.trackNumber() + z), (x - config.increment) ) 
                            oled.updatePanMix((mixer.trackNumber() + z), z)
                        
                        elif nihia.mixer.KNOB_INCREASE_MIN_SPEED <= event.data2 <= nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                            x = (mixer.getTrackPan(mixer.trackNumber() + z))
                            mixer.setTrackPan((mixer.trackNumber() + z), (x + config.increment) )
                            oled.updatePanMix((mixer.trackNumber() + z), z)


