import nihia
from nihia import mixer

from script.device_setup import config
from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED

import channels
import device
import midi
import plugins
import ui 


skip = -1


def plugin(self, event):

    if ui.getFocused(config.winName["Plugin"]) == 1: #plugin control
        plugin_name = ui.getFocusedPluginName()   

        if plugin_name == config.supported_plugins[0]:
            
            MAPPED_FUNCTION = {
            '0':0, 
            '1':1,
            '2':14,
            '3':13,
            '4':5,
            '5':4,
            '6':skip,
            '7':8,
            '8':12,  # 0
            '9':7,   # 1
            '10':11, # 2
            '11':10, # 3 
            '12': 3, # 4
            '13':2,  # 5
            '14':6,  # 6
            '15':9,  # 7      
            }

        elif plugin_name == config.supported_plugins[1] :
            
            MAPPED_FUNCTION = {
                    '0':10,
                    '1':11,
                    '2':12,
                    '3':13,
                    '4':14,
                    '5':15,
                    '6':16,
                    '7':17,
                    '8':skip,  #0
                    '9':skip,  #1
                    '10':skip, #2
                    '11':skip, #3 
                    '12':skip, #4
                    '13':skip, #5
                    '14':skip, #6
                    '15':skip, #7      
                    }   

        elif plugin_name == config.supported_plugins[2] :
            
            MAPPED_FUNCTION = {
                    '0':18,
                    '1':19,
                    '2':1,
                    '3':11,
                    '4':12,
                    '5':13,
                    '6':3,
                    '7':4,
                    '8':6,   #0
                    '9':7,   #1
                    '10':8,  #2
                    '11':10, #3
                    '12':17, #4
                    '13':2,  #5
                    '14':2,  #6                
                    '15':2,  #7
                    }

        elif plugin_name == config.supported_plugins[3] :
            
            MAPPED_FUNCTION = {
                    '0':18,
                    '1':19,
                    '2':1,
                    '3':11,
                    '4':12,
                    '5':13,
                    '6':3,
                    '7':4,
                    '8':6,   #0
                    '9':7,   #1
                    '10':8,  #2
                    '11':10, #3
                    '12':17, #4 
                    '13':2,  #5 
                    '14':2,  #6              
                    '15':2   #7
                    }

        elif plugin_name == config.supported_plugins[4] :
            
            MAPPED_FUNCTION = {
                    '0':0,
                    '1':1,
                    '2':2,
                    '3':3,
                    '4':4,
                    '5':5,
                    '6':6,
                    '7':7, 
                    '8':8,   #0
                    '9':9,   #1
                    '10':10, #2
                    '11':11, #3
                    '12':12, #4
                    '13':13, #5
                    '14':14, #6
                    '15':15  #7
                    }

        elif plugin_name == config.supported_plugins[5] :
            
            MAPPED_FUNCTION = {
                    '0':0,
                    '1':1,
                    '2':2,
                    '3':3,
                    '4':4,
                    '5':5,
                    '6':6,
                    '7':7, 
                    '8':8,   #0
                    '9':9,   #1
                    '10':10, #2
                    '11':11, #3
                    '12':12, #4
                    '13':13, #5
                    '14':14, #6
                    '15':15  #7
                    }

        elif plugin_name == config.supported_plugins[6] :
            
            MAPPED_FUNCTION = {
                    '0':0,
                    '1':1,
                    '2':2,
                    '3':3,
                    '4':4,
                    '5':5,
                    '6':6,
                    '7':7, 
                    '8':8,   #0
                    '9':9,   #1
                    '10':10, #2
                    '11':11, #3
                    '12':12, #4
                    '13':13, #5
                    '14':14, #6
                    '15':15  #7
                    }

        elif plugin_name == config.supported_plugins[7]:
            
            MAPPED_FUNCTION = {
                    '0':0,
                    '1':1,
                    '2':2,
                    '3':3,
                    '4':4,
                    '5':5,
                    '6':6,
                    '7':7, 
                    '8':8,   #0
                    '9':9,   #1
                    '10':10, #2
                    '11':11, #3
                    '12':12, #4
                    '13':13, #5
                    '14':14, #6
                    '15':15  #7
                    }

        elif plugin_name == config.supported_plugins[8] :
            
            MAPPED_FUNCTION = {
                    '0':0,
                    '1':1,
                    '2':2,
                    '3':3,
                    '4':4,
                    '5':5,
                    '6':6,
                    '7':7, 
                    '8':8,   #0
                    '9':9,   #1
                    '10':10, #2
                    '11':11, #3
                    '12':12, #4
                    '13':13, #5
                    '14':14, #6
                    '15':15  #7
                    }

        elif plugin_name == config.supported_plugins[9] :
            
            MAPPED_FUNCTION = {
                    '0':0,
                    '1':1,
                    '2':2,
                    '3':3,
                    '4':4,
                    '5':5,
                    '6':6,
                    '7':7, 
                    '8':8,   #0
                    '9':9,   #1
                    '10':10, #2
                    '11':11, #3
                    '12':12, #4
                    '13':13, #5
                    '14':14, #6
                    '15':15  #7
                    }
                    
        elif plugin_name == config.supported_plugins[10] :
            
            MAPPED_FUNCTION = {
                    '0':8,
                    '1':9,
                    '2':5,
                    '3':2,
                    '4':25,
                    '5':26,
                    '6':12, 
                    '7':13,
                    '8':15,    #0
                    '9':21,    #1
                    '10':22,   #2
                    '11':24,   #3
                    '12':4,    #4
                    '13':skip, #5
                    '14':skip, #6
                    '15':skip  #7   
                    }

        elif plugin_name == config.supported_plugins[11] :
            
            MAPPED_FUNCTION = {
                    '0':8,
                    '1':9,
                    '2':1,
                    '3':5,
                    '4':6,
                    '5':7,
                    '6':46, 
                    '7':15,
                    '8':18,  #0
                    '9':19,  #1
                    '10':20, #2
                    '11':21, #3
                    '12':29, #4
                    '13':30, #5
                    '14':17, #6
                    '15':16  #7   
                    }

        elif plugin_name == config.supported_plugins[13] :
            
            MAPPED_FUNCTION = {
                    '0':0,
                    '1':1,
                    '2':2,
                    '3':3,
                    '4':4,
                    '5':5,
                    '6':6,
                    '7':16, 
                    '8':8,   #0
                    '9':9,   #1
                    '10':10, #2
                    '11':17, #3
                    '12':12, #4
                    '13':13, #5
                    '14':14, #6
                    '15':15  #7
                    }
        else:

            MAPPED_FUNCTION = {
                    '0':skip,
                    '1':skip,
                    '2':skip,
                    '3':skip,
                    '4':skip,
                    '5':skip,
                    '6':skip,
                    '7':skip, 
                    '8':skip,  #0
                    '9':skip,  #1
                    '10':skip, #2
                    '11':skip, #3
                    '12':skip, #4
                    '13':skip, #5
                    '14':skip, #6
                    '15':skip  #7
                    }


        if MAPPED_FUNCTION["0"] == skip and event.data1 == nihia.mixer.knobs[0][0]:
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

        else:
            if (event.data1 == nihia.mixer.knobs[0][0]):
                x = plugins.getParamValue(MAPPED_FUNCTION["0"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True

                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["0"], channels.selectedChannel()))
            
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["0"], channels.selectedChannel()) 

                    #mixer.setTrackVol(0, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["0"], channels.channelNumber()))))
                    

                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["0"], channels.selectedChannel())

                    #mixer.setTrackVol(0, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["0"], channels.channelNumber()))))
                    
                mixer.setTrackVol(0, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["0"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["0"], channels.selectedChannel()), 0)

            
        if MAPPED_FUNCTION["1"]  == skip and event.data1 == nihia.mixer.knobs[0][1]:
            event.handled = True
            mixer.setTrackVol(1, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 1)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[0][1]):
                x = plugins.getParamValue(MAPPED_FUNCTION["1"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["1"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["1"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["1"], channels.selectedChannel())

                mixer.setTrackVol(1, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["1"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["1"], channels.selectedChannel()), 1)

        if MAPPED_FUNCTION["2"]  == skip and event.data1 == nihia.mixer.knobs[0][2]:
            event.handled = True
            mixer.setTrackVol(2, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 2)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[0][2]):
                x = plugins.getParamValue(MAPPED_FUNCTION["2"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["2"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["2"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["2"], channels.selectedChannel())

                mixer.setTrackVol(2, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["2"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["2"], channels.selectedChannel()), 2)                             

        if MAPPED_FUNCTION["3"]  == skip and event.data1 == nihia.mixer.knobs[0][3]:
            event.handled = True
            mixer.setTrackVol(3, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 3)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[0][3]):
                x = plugins.getParamValue(MAPPED_FUNCTION["3"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["3"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["3"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["3"], channels.selectedChannel())

                mixer.setTrackVol(3, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["3"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["3"], channels.selectedChannel()), 3)

        if  MAPPED_FUNCTION["4"] == skip and event.data1 == nihia.mixer.knobs[0][4]:
            event.handled = True
            mixer.setTrackVol(4, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 4)
            ui.setHintMsg(config.nuText)
        else:        
            if (event.data1 == nihia.mixer.knobs[0][4]):
                x = plugins.getParamValue(MAPPED_FUNCTION["4"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["4"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["4"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["4"], channels.selectedChannel())

                mixer.setTrackVol(4, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["4"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["4"], channels.selectedChannel()), 4)

        if  MAPPED_FUNCTION["5"] == skip and event.data1 == nihia.mixer.knobs[0][5]:
            event.handled = True
            mixer.setTrackVol(5, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 5)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[0][5]):
                x = plugins.getParamValue(MAPPED_FUNCTION["5"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["5"], channels.selectedChannel()))   
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["5"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["5"], channels.selectedChannel())

                mixer.setTrackVol(5, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["5"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["5"], channels.selectedChannel()), 5)

        if  MAPPED_FUNCTION["6"] == skip and event.data1 == nihia.mixer.knobs[0][6]:
            event.handled = True
            mixer.setTrackVol(6, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 6)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[0][6]):
                x = plugins.getParamValue(MAPPED_FUNCTION["6"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["6"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["6"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["6"], channels.selectedChannel())

                mixer.setTrackVol(6, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["6"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["6"], channels.selectedChannel()), 6)

        if  MAPPED_FUNCTION["7"] == skip and event.data1 == nihia.mixer.knobs[0][7]:
            event.handled = True
            mixer.setTrackVol(7, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 7)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[0][7]):
                x = plugins.getParamValue(MAPPED_FUNCTION["7"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["7"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["7"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["7"], channels.selectedChannel())

                mixer.setTrackVol(7, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["7"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["7"], channels.selectedChannel()), 7)


            #shifted knobs

        if  MAPPED_FUNCTION["8"] == skip and event.data1 == nihia.mixer.knobs[1][0]:
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
        else:
            if (event.data1 == nihia.mixer.knobs[1][0]):
                x = plugins.getParamValue(MAPPED_FUNCTION["8"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True

                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["8"], channels.selectedChannel()))
            
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["8"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["8"], channels.selectedChannel())

                mixer.setTrackPan(0, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["8"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["8"], channels.selectedChannel()), 0)
                
        if  MAPPED_FUNCTION["9"] == skip and event.data1 == nihia.mixer.knobs[1][1]:
            event.handled = True
            mixer.setTrackPan(1, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 1)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[1][1]):
                x = plugins.getParamValue(MAPPED_FUNCTION["9"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["9"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["9"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["9"], channels.selectedChannel())

                mixer.setTrackPan(1, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["9"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["9"], channels.selectedChannel()), 1)

        if  MAPPED_FUNCTION["10"] == skip and event.data1 == nihia.mixer.knobs[1][2]:
            event.handled = True
            mixer.setTrackPan(2, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 2)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[1][2]):
                x = plugins.getParamValue(MAPPED_FUNCTION["10"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["10"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["10"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["10"], channels.selectedChannel())

                mixer.setTrackPan(2, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["10"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["10"], channels.selectedChannel()), 2)                              

        if  MAPPED_FUNCTION["11"] == skip and event.data1 == nihia.mixer.knobs[1][3]:
            event.handled = True
            mixer.setTrackPan(3, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 3)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[1][3]):
                x = plugins.getParamValue(MAPPED_FUNCTION["11"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["11"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["11"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["11"], channels.selectedChannel())

                mixer.setTrackPan(3, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["11"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["11"], channels.selectedChannel()), 3)

        if  MAPPED_FUNCTION["12"] == skip and event.data1 == nihia.mixer.knobs[1][4]:
            event.handled = True
            mixer.setTrackPan(4, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 4)
            ui.setHintMsg(config.nuText)
        else:        
            if (event.data1 == nihia.mixer.knobs[1][4]):
                x = plugins.getParamValue(MAPPED_FUNCTION["12"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["12"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["12"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["12"], channels.selectedChannel())

                mixer.setTrackPan(4, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["12"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["12"], channels.selectedChannel()), 4)

        if  MAPPED_FUNCTION["13"] == skip and event.data1 == nihia.mixer.knobs[1][5]:
            event.handled = True
            mixer.setTrackPan(5, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 5)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[1][5]):
                x = plugins.getParamValue(MAPPED_FUNCTION["13"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["13"], channels.selectedChannel()))   
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["13"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["13"], channels.selectedChannel())

                mixer.setTrackPan(5, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["13"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["13"], channels.selectedChannel()), 5)

        if  MAPPED_FUNCTION["14"] == skip and event.data1 == nihia.mixer.knobs[1][6]:
            event.handled = True
            mixer.setTrackPan(6, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 6)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[1][6]):
                x = plugins.getParamValue(MAPPED_FUNCTION["14"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["14"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["14"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["14"], channels.selectedChannel())

                mixer.setTrackPan(6, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["14"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["14"], channels.selectedChannel()), 6)

        if  MAPPED_FUNCTION["15"] == skip and event.data1 == nihia.mixer.knobs[1][7]:
            event.handled = True
            mixer.setTrackPan(7, config.blankEvent)
            NILA_OLED.updateText(config.blankEvent, 7)
            ui.setHintMsg(config.nuText)
        else:
            if (event.data1 == nihia.mixer.knobs[1][7]):
                x = plugins.getParamValue(MAPPED_FUNCTION["15"], channels.selectedChannel())
                y = round(x,2)
                event.handled = True
                
                ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION["15"], channels.selectedChannel()))
                
                if event.data2 == nihia.mixer.KNOB_DECREASE_MAX_SPEED:
                    plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION["15"], channels.selectedChannel()) 
                elif event.data2 == nihia.mixer.KNOB_INCREASE_MAX_SPEED:
                    plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION["15"], channels.selectedChannel())

                mixer.setTrackPan(7, str(round(100*plugins.getParamValue(MAPPED_FUNCTION["15"], channels.selectedChannel())   ), ))
                NILA_OLED.updateText(plugins.getParamName(MAPPED_FUNCTION["15"], channels.selectedChannel()), 7)