import nihia
from nihia import mixer as mix

from script.screen_writer import NILA_OLED as oled
from script.device_setup import config 

import device 
import math
import mixer
import ui 


def OnMidiMsg(self, event):    
    if ui.getFocused(config.winName["Mixer"]) == True: 

        # VOLUME CONTROL

        xy = 1.25 # no idea what this does. don't change it; it's important
                        
        #knob 0
        if mixer.trackNumber() <= config.currentUtility:
            if (event.data1 == nihia.mixer.knobs[0][0]):
                event.handled = True

                if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= config.currentUtility:
                    pass
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                        mixer.setTrackVolume((mixer.trackNumber() + 0), (x - config.increment) ) # volume values go down
                        mix.setTrackVol(0, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 0))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 0), 0)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 0))
                        mixer.setTrackVolume((mixer.trackNumber() + 0), (x + config.increment) ) # volume values go up
                        mix.setTrackVol(0, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 0))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 0), 0)



        #knob 1
        if mixer.trackNumber() <= 125:
            if (event.data1 == nihia.mixer.knobs[0][1]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+1) == "Current" and mixer.trackNumber()+1 >= config.currentUtility:
                    pass
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                        mixer.setTrackVolume((mixer.trackNumber() + 1), (x - config.increment) ) # volume values go down
                        mix.setTrackVol(1, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 1))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 1), 1)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 1))
                        mixer.setTrackVolume((mixer.trackNumber() + 1), (x + config.increment) ) # volume values go up
                        mix.setTrackVol(1, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 1))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 1), 1)

        elif mixer.trackNumber()+1 >= 125:
            pass 
            mix.setTrackName(1, config.blankEvent)
            mix.setTrackVol(1, config.blankEvent) 

        #knob 2
        if mixer.trackNumber() <= 124:
            if (event.data1 == nihia.mixer.knobs[0][2]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+2) == "Current" and mixer.trackNumber()+2 >= config.currentUtility:
                    pass
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 2))
                        mixer.setTrackVolume((mixer.trackNumber() + 2), (x - config.increment) ) # volume values go down
                        mix.setTrackVol(2, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 2))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 2), 2)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 2))
                        mixer.setTrackVolume((mixer.trackNumber() + 2), (x + config.increment) ) # volume values go up
                        mix.setTrackVol(2, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 2))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 2), 2)

        elif mixer.trackNumber()+2 >= 125:
            pass     
            mix.setTrackName(2, config.blankEvent)
            mix.setTrackVol(2, config.blankEvent) 
            
        #knob 3
        if mixer.trackNumber() <= 123:
            if (event.data1 == nihia.mixer.knobs[0][3]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+3) == "Current" and mixer.trackNumber()+3 >= config.currentUtility:
                    pass
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 3))
                        mixer.setTrackVolume((mixer.trackNumber() + 3), (x - config.increment) ) # volume values go down
                        mix.setTrackVol(3, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 3))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 3), 3)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 3))
                        mixer.setTrackVolume((mixer.trackNumber() + 3), (x + config.increment) ) # volume values go up
                        mix.setTrackVol(3, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 3))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 3), 3)

        elif mixer.trackNumber()+3 >= 125:
            pass     
            mix.setTrackName(3, config.blankEvent)
            mix.setTrackVol(3, config.blankEvent) 

        #knob 4
        if mixer.trackNumber() <= 122:
            if (event.data1 == nihia.mixer.knobs[0][4]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+4) == "Current" and mixer.trackNumber()+4 >= config.currentUtility:
                    pass
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 4))
                        mixer.setTrackVolume((mixer.trackNumber() + 4), (x - config.increment) ) # volume values go down
                        mix.setTrackVol(4, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 4))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 4), 4)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 4))
                        mixer.setTrackVolume((mixer.trackNumber() + 4), (x + config.increment) ) # volume values go up
                        mix.setTrackVol(4, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 4))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 4), 4)


        elif mixer.trackNumber()+4 >= 125:
            pass    
            mix.setTrackName(4, config.blankEvent)
            mix.setTrackVol(4, config.blankEvent) 

        #knob 5
        if mixer.trackNumber() <= 121:
            if (event.data1 == nihia.mixer.knobs[0][5]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+5) == "Current" and mixer.trackNumber()+5 >= config.currentUtility:
                    pass
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 5))
                        mixer.setTrackVolume((mixer.trackNumber() + 5), (x - config.increment) ) # volume values go down
                        mix.setTrackVol(5, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 5))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 5), 5)

                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 5))
                        mixer.setTrackVolume((mixer.trackNumber() + 5), (x + config.increment) ) # volume values go up
                        mix.setTrackVol(5, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 5))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 5), 5)

        elif mixer.trackNumber()+5 >= 125:
            pass   
            mix.setTrackName(5, config.blankEvent)
            mix.setTrackVol(5, config.blankEvent)      

        #knob 6
        if mixer.trackNumber() <= 120:
            if (event.data1 == nihia.mixer.knobs[0][6]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+6) == "Current" and mixer.trackNumber()+6 >= config.currentUtility:
                    pass
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 6))
                        mixer.setTrackVolume((mixer.trackNumber() + 6), (x - config.increment) ) # volume values go down
                        mix.setTrackVol(6, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 6))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 6), 6)

                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 6))
                        mixer.setTrackVolume((mixer.trackNumber() + 6), (x + config.increment) ) # volume values go up
                        mix.setTrackVol(6, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 6))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 6), 6)


        elif mixer.trackNumber()+6 >= 125: 
            pass   
            mix.setTrackName(6, config.blankEvent)
            mix.setTrackVol(6, config.blankEvent)      
                        
        #knob 7
        if mixer.trackNumber() <= 119:
            if (event.data1 == nihia.mixer.knobs[0][7]):
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber()+7) == "Current" and mixer.trackNumber()+7 >= config.currentUtility:
                    pass
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 7))
                        mixer.setTrackVolume((mixer.trackNumber() + 7), (x - config.increment) ) # volume values go down
                        mix.setTrackVol(7, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 7))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 7), 7)

                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackVolume(mixer.trackNumber() + 7))
                        mixer.setTrackVolume((mixer.trackNumber() + 7), (x + config.increment) ) # volume values go up
                        mix.setTrackVol(7, str(oled.VolTodB(mixer.getTrackVolume(mixer.trackNumber() + 7))) + " dB")
                        oled.updateText(mixer.getTrackName(mixer.trackNumber() + 7), 7)


        elif mixer.trackNumber()+7 >= 125:
            pass    
            mix.setTrackName(7, config.blankEvent)
            mix.setTrackVol(7, config.blankEvent)     

        # PAN CONTROL

        xy = 1.25
                        
        #knob 0
        if mixer.trackNumber() <= config.currentUtility:
            if (event.data1 == nihia.mixer.knobs[1][0]):
                event.handled = True

                if mixer.trackNumber()+0 >= 125:
                    mix.setTrackPan(0, config.blankEvent)
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                        mixer.setTrackPan((mixer.trackNumber() + 0), (x - config.increment) ) 
                        oled.updatePanMix((mixer.trackNumber() + 0), 0)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 0))
                        mixer.setTrackPan((mixer.trackNumber() + 0), (x + config.increment) )
                        oled.updatePanMix((mixer.trackNumber() + 0), 0)

        elif mixer.trackNumber() >= config.currentUtility:    
            mix.setTrackPan(0, config.blankEvent)                

        #knob 1
        if mixer.trackNumber() <= 125:
            if (event.data1 == nihia.mixer.knobs[1][1]):
                event.handled = True

                if mixer.trackNumber()+1 >= 125:
                    mix.setTrackPan(1, config.blankEvent)
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 1))
                        mixer.setTrackPan((mixer.trackNumber() + 1), (x - config.increment) ) 
                        oled.updatePanMix((mixer.trackNumber() + 1), 1)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 1))
                        mixer.setTrackPan((mixer.trackNumber() + 1), (x + config.increment) )
                        oled.updatePanMix((mixer.trackNumber() + 1), 1)

        elif mixer.trackNumber()+1 >= config.currentUtility: 
            mix.setTrackPan(0, config.blankEvent) 

        #knob 2
        if mixer.trackNumber() <= 124:
            if (event.data1 == nihia.mixer.knobs[1][2]):
                event.handled = True

                if mixer.trackNumber()+2 >= 124:
                    mix.setTrackPan(2, config.blankEvent)
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                        mixer.setTrackPan((mixer.trackNumber() + 2), (x - config.increment) ) 
                        oled.updatePanMix((mixer.trackNumber() + 1), 2)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 2))
                        mixer.setTrackPan((mixer.trackNumber() + 2), (x + config.increment) )
                        oled.updatePanMix((mixer.trackNumber() + 2), 2)
            
        #knob 3
        if mixer.trackNumber() <= 124:
            if (event.data1 == nihia.mixer.knobs[1][3]):
                event.handled = True

                if mixer.trackNumber()+1 >= 124:
                    mix.setTrackPan(3, config.blankEvent)
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                        mixer.setTrackPan((mixer.trackNumber() + 3), (x - config.increment) ) 
                        oled.updatePanMix((mixer.trackNumber() + 3), 3)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 3))
                        mixer.setTrackPan((mixer.trackNumber() + 3), (x + config.increment) )
                        oled.updatePanMix((mixer.trackNumber() + 3), 3)

        #knob 4
        if mixer.trackNumber() <= 124:
            if (event.data1 == nihia.mixer.knobs[1][4]):
                event.handled = True

                if mixer.trackNumber()+4 >= 124:
                    mix.setTrackPan(4, config.blankEvent)
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                        mixer.setTrackPan((mixer.trackNumber() + 4), (x - config.increment) ) 
                        oled.updatePanMix((mixer.trackNumber() + 4), 4)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 4))
                        mixer.setTrackPan((mixer.trackNumber() + 4), (x + config.increment) )
                        oled.updatePanMix((mixer.trackNumber() + 4), 4)

        #knob 5
        if mixer.trackNumber() <= 124:
            if (event.data1 == nihia.mixer.knobs[1][5]):
                event.handled = True

                if mixer.trackNumber()+5 >= 124:
                    mix.setTrackPan(5, config.blankEvent)
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                        mixer.setTrackPan((mixer.trackNumber() + 5), (x - config.increment) ) 
                        oled.updatePanMix((mixer.trackNumber() + 5), 5)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 5))
                        mixer.setTrackPan((mixer.trackNumber() + 5), (x + config.increment) )
                        oled.updatePanMix((mixer.trackNumber() + 5), 5)

        #knob 6
        if mixer.trackNumber() <= 124:
            if (event.data1 == nihia.mixer.knobs[1][6]):
                event.handled = True

                if mixer.trackNumber()+6 >= 124:
                    mix.setTrackPan(6, config.blankEvent)
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                        mixer.setTrackPan((mixer.trackNumber() + 6), (x - config.increment) ) 
                        oled.updatePanMix((mixer.trackNumber() + 6), 6)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 6))
                        mixer.setTrackPan((mixer.trackNumber() + 6), (x + config.increment) )
                        oled.updatePanMix((mixer.trackNumber() + 6), 6)

        #knob 7
        if mixer.trackNumber() <= 124:
            if (event.data1 == nihia.mixer.knobs[1][7]):
                event.handled = True

                if mixer.trackNumber()+7 >= 124:
                    mix.setTrackPan(7, config.blankEvent)
                else:
                    if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 7))
                        mixer.setTrackPan((mixer.trackNumber() + 7), (x - config.increment) ) 
                        oled.updatePanMix((mixer.trackNumber() + 7), 7)
                    
                    elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                        x = (mixer.getTrackPan(mixer.trackNumber() + 7))
                        mixer.setTrackPan((mixer.trackNumber() + 7), (x + config.increment) )
                        oled.updatePanMix((mixer.trackNumber() + 7), 7)

