import nihia
from nihia import mixer as mix

from script.device_setup import NILA_core as core
from script.device_setup import config 
from script.device_setup import constants
from script.device_setup import transform 


import mixer
import ui 

        
def OnMidiMsg(self, event): 
       
    """
    Final track is the 'current' track, which is a special analysis track that has no
    volume or pan controls. We are not interested in this track as we cannot control it.
    """

    if ui.getFocused(constants.winName["Mixer"]) == True: 

        # VOLUME CONTROL
        s_series = False
        
        for z in range(8):
            if mixer.trackNumber() <= constants.currentUtility - z:
                if (event.data1 == nihia.mixer.knobs[0][z]):
                    event.handled = True
                    
                    if mixer.getTrackName(mixer.trackNumber()+z) == "Current" and mixer.trackNumber()+z >= constants.currentUtility:
                        pass
                    else:
                        if core.seriesCheck(s_series) == True:
                       
                            if event.data2 in range(65, 95):
                                mixer.setTrackVolume((mixer.trackNumber() + z), (mixer.getTrackVolume(mixer.trackNumber() + z) - config.increment * 2.5)) 
                                
                            elif event.data2 in range(96, 127):
                                mixer.setTrackVolume((mixer.trackNumber() + z), (mixer.getTrackVolume(mixer.trackNumber() + z) - config.increment)) 

                            elif event.data2 in range (0, 31):
                                mixer.setTrackVolume((mixer.trackNumber() + z), (mixer.getTrackVolume(mixer.trackNumber() + z) + config.increment)) 

                            elif event.data2 in range (32, 63):
                                mixer.setTrackVolume((mixer.trackNumber() + z), (mixer.getTrackVolume(mixer.trackNumber() + z) + config.increment * 2.5))
                                   
                        else:
                            if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                                mixer.setTrackVolume((mixer.trackNumber() + z), (mixer.getTrackVolume(mixer.trackNumber() + z) - config.increment)) 

                            elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                                mixer.setTrackVolume((mixer.trackNumber() + z), (mixer.getTrackVolume(mixer.trackNumber() + z) + config.increment))       

                elif mixer.trackNumber() + z >= constants.currentUtility:
                    pass     

            # PAN CONTROL

            for z in range(8):
                if mixer.trackNumber() <= constants.currentUtility - z:
                    if (event.data1 == nihia.mixer.knobs[1][z]):
                        event.handled = True

                        if mixer.trackNumber() + z >= constants.currentUtility - z:
                            pass
                        else:
                            if core.seriesCheck(s_series) == True:
                                if nihia.mixer.KNOB_INCREASE_MAX_SPEED <= event.data2:
                                    mixer.setTrackPan((mixer.trackNumber() + z), (mixer.getTrackPan(mixer.trackNumber() + z) - config.increment)) 
                                
                                elif nihia.mixer.KNOB_DECREASE_MAX_SPEED >= event.data2:
                                    mixer.setTrackPan((mixer.trackNumber() + z), (mixer.getTrackPan(mixer.trackNumber() + z) + config.increment))
                            else:
                                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                                    mixer.setTrackPan((mixer.trackNumber() + z), (mixer.getTrackPan(mixer.trackNumber() + z) - config.increment)) 
                                
                                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                                    mixer.setTrackPan((mixer.trackNumber() + z), (mixer.getTrackPan(mixer.trackNumber() + z) + config.increment))