import nihia

from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED
from script.device_setup import config

import channels
import device 
import math
import plugins 
import ui 

def OnMidiMsg(self, event): 

    if ui.getFocused(config.winName["Channel Rack"]) == True:

        # VOLUME CONTROL

        #knob 0
        if (event.data1 == nihia.mixer.knobs[0][0]):
            event.handled = True  
            if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                y = round(x,2)

                if channels.getChannelVolume(channels.selectedChannel() + 0) != 0 :
                    channels.setChannelVolume((channels.selectedChannel() + 0), (y - config.increment) ) 
                    NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
                    NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 0), 0)
                

            elif event.data2 ==  nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                x = (channels.getChannelVolume(channels.selectedChannel() + 0))
                y = round(x,2)
                channels.setChannelVolume((channels.selectedChannel() + 0), (y + config.increment) )
                NILA_core.setTrackVolConvert(0, str(round(channels.getChannelVolume(channels.selectedChannel()+ 0, 1), 1)) + " dB")
                NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 0), 0)

        #knob 1
        if channels.channelCount() > 1 and channels.selectedChannel() < (channels.channelCount()-1) :
            if (event.data1 == nihia.mixer.knobs[0][1]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 1))
                    y = round(x,2)

                    if channels.getChannelVolume(channels.selectedChannel() + 1) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + 1), (y - config.increment) ) 
                        NILA_core.setTrackVolConvert(1, str(round(channels.getChannelVolume(channels.selectedChannel()+ 1, 1), 1)) + " dB")
                        NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 1), 1)
                    

                elif event.data2 ==  nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 1))
                    y = round(x,2)
                    channels.setChannelVolume((channels.selectedChannel() + 1), (y + config.increment) )
                    NILA_core.setTrackVolConvert(1, str(round(channels.getChannelVolume(channels.selectedChannel()+ 1, 1), 1)) + " dB")
                    NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 1), 1)
        else:
            event.handled = True 
                        

        #knob 2
        if channels.channelCount() > 2 and channels.selectedChannel() < (channels.channelCount()-2) :
            if (event.data1 == nihia.mixer.knobs[0][2]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 2))
                    y = round(x,2)

                    if channels.getChannelVolume(channels.selectedChannel() + 2) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + 2), (y - config.increment) ) 
                        NILA_core.setTrackVolConvert(2, str(round(channels.getChannelVolume(channels.selectedChannel()+ 2, 1), 1)) + " dB")
                        NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 2), 2)
                

                elif event.data2 ==  nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 2))
                    y = round(x,2)
                    channels.setChannelVolume((channels.selectedChannel() + 2), (y + config.increment) )
                    NILA_core.setTrackVolConvert(2, str(round(channels.getChannelVolume(channels.selectedChannel()+ 2, 1), 1)) + " dB")
                    NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 2), 2)
        else:
            event.handled = True 
                        

        #knob 3
        if channels.channelCount() > 3 and channels.selectedChannel() < (channels.channelCount()-3) :
            if (event.data1 == nihia.mixer.knobs[0][3]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 3))
                    y = round(x,2)

                    if channels.getChannelVolume(channels.selectedChannel() + 3) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + 3), (y - config.increment) ) 
                        NILA_core.setTrackVolConvert(3, str(round(channels.getChannelVolume(channels.selectedChannel()+ 3, 1), 1)) + " dB")
                        NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 3), 3)
                    

                elif event.data2 ==  nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 3))
                    y = round(x,2)
                    channels.setChannelVolume((channels.selectedChannel() + 3), (y + config.increment) )
                    NILA_core.setTrackVolConvert(3, str(round(channels.getChannelVolume(channels.selectedChannel()+ 3, 1), 1)) + " dB")
                    NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 3), 3)     
        else:
            event.handled = True 
                        

        #knob 4
        if channels.channelCount() > 4 and channels.selectedChannel() < (channels.channelCount()-4) :
            if (event.data1 == nihia.mixer.knobs[0][4]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 4))
                    y = round(x,2)

                    if channels.getChannelVolume(channels.selectedChannel() + 4) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + 4), (y - config.increment) ) 
                        NILA_core.setTrackVolConvert(4, str(round(channels.getChannelVolume(channels.selectedChannel()+ 4, 1), 1)) + " dB")
                        NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 4), 4)
                    

                elif event.data2 ==  nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 4))
                    y = round(x,2)
                    channels.setChannelVolume((channels.selectedChannel() + 4), (y + config.increment) )
                    NILA_core.setTrackVolConvert(4, str(round(channels.getChannelVolume(channels.selectedChannel()+ 4, 1), 1)) + " dB")
                    NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 4), 4)
        else:
            event.handled = True 
                         

        #knob 5
        if channels.channelCount() > 5 and channels.selectedChannel() < (channels.channelCount()-5) :
            if (event.data1 == nihia.mixer.knobs[0][5]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 5))
                    y = round(x,2)

                    if channels.getChannelVolume(channels.selectedChannel() + 5) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + 5), (y - config.increment) ) 
                        NILA_core.setTrackVolConvert(5, str(round(channels.getChannelVolume(channels.selectedChannel()+ 5, 1), 1)) + " dB")
                        NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 5), 5)
                    

                elif event.data2 ==  nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 5))
                    y = round(x,2)
                    channels.setChannelVolume((channels.selectedChannel() + 5), (y + config.increment) )
                    NILA_core.setTrackVolConvert(5, str(round(channels.getChannelVolume(channels.selectedChannel()+ 5, 1), 1)) + " dB")
                    NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 5), 5)
        else:
            event.handled = True 
                       

        #knob 6
        if channels.channelCount() > 6 and channels.selectedChannel() < (channels.channelCount()-6) :
            if (event.data1 == nihia.mixer.knobs[0][6]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 6))
                    y = round(x,2)

                    if channels.getChannelVolume(channels.selectedChannel() + 6) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + 6), (y - config.increment) ) 
                        NILA_core.setTrackVolConvert(6, str(round(channels.getChannelVolume(channels.selectedChannel()+ 6, 1), 1)) + " dB")
                        NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 6), 6)
                    

                elif event.data2 ==  nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 6))
                    y = round(x,2)
                    channels.setChannelVolume((channels.selectedChannel() + 6), (y + config.increment) )
                    NILA_core.setTrackVolConvert(6, str(round(channels.getChannelVolume(channels.selectedChannel()+ 6, 1), 1)) + " dB")
                    NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 6), 6)   
        else:
            event.handled = True 
                      

        #knob 7
        if channels.channelCount() > 7 and channels.selectedChannel() < (channels.channelCount()-7) :
            if (event.data1 == nihia.mixer.knobs[0][7]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 7))
                    y = round(x,2)

                    if channels.getChannelVolume(channels.selectedChannel() + 7) != 0 :
                        channels.setChannelVolume((channels.selectedChannel() + 7), (y - config.increment) ) 
                        NILA_core.setTrackVolConvert(7, str(round(channels.getChannelVolume(channels.selectedChannel()+ 7, 1), 1)) + " dB")
                        NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 7), 7)
                    

                elif event.data2 ==  nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    x = (channels.getChannelVolume(channels.selectedChannel() + 7))
                    y = round(x,2)
                    channels.setChannelVolume((channels.selectedChannel() + 7), (y + config.increment) )
                    NILA_core.setTrackVolConvert(7, str(round(channels.getChannelVolume(channels.selectedChannel()+ 7, 1), 1)) + " dB")
                    NILA_OLED.updateText(channels.getChannelName(channels.selectedChannel() + 7), 7)   
        else:
            event.handled = True 
                       

        # PAN CONTROL

        #knob shifted 0
        if (event.data1 == nihia.mixer.knobs[1][0]):
            event.handled = True  
            if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                x = (channels.getChannelPan(channels.selectedChannel() + 0))
                channels.setChannelPan((channels.selectedChannel() + 0), (x - config.increment) )
                NILA_OLED.updatePanChannel((channels.selectedChannel() + 0), 0)

            elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                
                x = (channels.getChannelPan(channels.selectedChannel() + 0))
                channels.setChannelPan((channels.selectedChannel() + 0), (x + config.increment) ) 
                NILA_OLED.updatePanChannel((channels.selectedChannel() + 0), 0)

        #knob shifted 1
        if channels.channelCount() > 1 and channels.selectedChannel() < (channels.channelCount()-1) :
            if (event.data1 == nihia.mixer.knobs[1][1]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelPan(channels.selectedChannel() + 1))
                    channels.setChannelPan((channels.selectedChannel() + 1), (x - config.increment) )
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 1), 1)

                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    
                    x = (channels.getChannelPan(channels.selectedChannel() + 1))
                    channels.setChannelPan((channels.selectedChannel() + 1), (x + config.increment) ) 
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 1), 1)
        else:
            event.handled = True 
            

        #knob shifted 2
        if channels.channelCount() > 2 and channels.selectedChannel() < (channels.channelCount()-2) :
            if (event.data1 == nihia.mixer.knobs[1][2]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelPan(channels.selectedChannel() + 2))
                    channels.setChannelPan((channels.selectedChannel() + 2), (x - config.increment) )
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 2), 2)

                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    
                    x = (channels.getChannelPan(channels.selectedChannel() + 2))
                    channels.setChannelPan((channels.selectedChannel() + 2), (x + config.increment) ) 
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 2), 2)
        else:
            event.handled = True 
            

        #knob shifted 3
        if channels.channelCount() > 3 and channels.selectedChannel() < (channels.channelCount()-3) :
            if (event.data1 == nihia.mixer.knobs[1][3]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelPan(channels.selectedChannel() + 3))
                    channels.setChannelPan((channels.selectedChannel() + 3), (x - config.increment) )
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 3), 3)

                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    
                    x = (channels.getChannelPan(channels.selectedChannel() + 3))
                    channels.setChannelPan((channels.selectedChannel() + 3), (x + config.increment) ) 
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 3), 3)
        else:
            event.handled = True 
            

        #knob shifted 4
        if channels.channelCount() > 4 and channels.selectedChannel() < (channels.channelCount()-4) :
            if (event.data1 == nihia.mixer.knobs[1][4]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelPan(channels.selectedChannel() + 4))
                    channels.setChannelPan((channels.selectedChannel() + 4), (x - config.increment) )
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 4), 4)

                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    
                    x = (channels.getChannelPan(channels.selectedChannel() + 4))
                    channels.setChannelPan((channels.selectedChannel() + 4), (x + config.increment) ) 
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 4), 4)
        else:
            event.handled = True 
            

        #knob shifted 5
        if channels.channelCount() > 5 and channels.selectedChannel() < (channels.channelCount()-5) :
            if (event.data1 == nihia.mixer.knobs[1][5]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelPan(channels.selectedChannel() + 5))
                    channels.setChannelPan((channels.selectedChannel() + 5), (x - config.increment) )
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 5), 5)

                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    
                    x = (channels.getChannelPan(channels.selectedChannel() + 5))
                    channels.setChannelPan((channels.selectedChannel() + 5), (x + config.increment) ) 
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 5), 5)
        else:
            event.handled = True 
            

        #knob shifted 6
        if channels.channelCount() > 6 and channels.selectedChannel() < (channels.channelCount()-6) :
            if (event.data1 == nihia.mixer.knobs[1][6]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelPan(channels.selectedChannel() + 6))
                    channels.setChannelPan((channels.selectedChannel() + 6), (x - config.increment) )
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 6), 6)

                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    
                    x = (channels.getChannelPan(channels.selectedChannel() + 6))
                    channels.setChannelPan((channels.selectedChannel() + 6), (x + config.increment) ) 
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 6), 6)
        else:
            event.handled = True 
            

        #knob shifted 7
        if channels.channelCount() > 7 and channels.selectedChannel() < (channels.channelCount()-7) :
            if (event.data1 == nihia.mixer.knobs[1][7]):
                event.handled = True  
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    x = (channels.getChannelPan(channels.selectedChannel() + 7))
                    channels.setChannelPan((channels.selectedChannel() + 7), (x - config.increment) )
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 7), 7)

                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    
                    x = (channels.getChannelPan(channels.selectedChannel() + 7))
                    channels.setChannelPan((channels.selectedChannel() + 7), (x + config.increment) ) 
                    NILA_OLED.updatePanChannel((channels.selectedChannel() + 7), 7)
        else:
            event.handled = True 
            
