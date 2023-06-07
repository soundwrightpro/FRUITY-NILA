import nihia
from nihia import mixer as mix

from script.device_setup import NILA_core
from script.device_setup import config 
from script.device_setup import constants

import channels
import plugins
import ui 

skip = -1


def plugin(self, event):
    
    if ui.getFocused(constants.winName["Plugin"]) == 1: #plugin control
                     
        if ui.getFocusedPluginName()  == constants.supported_plugins["FL Keys"]:
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["FLEX"] :
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["Sytrus"] :
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["GMS"] :
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["Harmless"] :
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["Harmor"] :
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["Morphine"] :
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["3x Osc"]:
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["Fruity DX10"] :
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["BassDrum"] :
            
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
                    
        elif ui.getFocusedPluginName()  == constants.supported_plugins["MiniSynth"] :
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["PoiZone"] :
            
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

        elif ui.getFocusedPluginName()  == constants.supported_plugins["Sakura"] :
            
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


        for a in range(8):
                if MAPPED_FUNCTION[str(a)] == skip and event.data1 == mix.knobs[0][a]:
                    event.handled = True
                    mix.setTrackVol(a, constants.blankEvent)
                    mix.setTrackName(a, constants.blankEvent)
                    ui.setHintMsg(constants.blankEvent)
                else:
                    if (event.data1 == mix.knobs[0][a]):
                        x = plugins.getParamValue(MAPPED_FUNCTION[str(a)], channels.selectedChannel())
                        y = round(x,2)
                        event.handled = True
                        
                        ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION[str(a)], channels.selectedChannel()))
                        
                        if mix.KNOB_DECREASE_MIN_SPEED >= event.data2 >= mix.KNOB_DECREASE_MAX_SPEED:
                            plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION[str(a)], channels.selectedChannel()) 

                        elif mix.KNOB_INCREASE_MIN_SPEED <= event.data2 <= mix.KNOB_INCREASE_MAX_SPEED:
                            plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION[str(a)], channels.selectedChannel())

                        mix.setTrackVol(a, str(round(100*plugins.getParamValue(MAPPED_FUNCTION[str(a)], channels.selectedChannel())   ), ))
                        mix.setTrackName(a, plugins.getParamName(MAPPED_FUNCTION[str(a)], channels.selectedChannel()))

        for a in range(8):
                b = a + 8
                if MAPPED_FUNCTION[str(b)] == skip and event.data1 == mix.knobs[1][a]:
                    event.handled = True
                    mix.setTrackVol(a, constants.blankEvent)
                    mix.setTrackName(a, constants.blankEvent)
                    
                    mix.setTrackName(a, constants.blankEvent)
                    ui.setHintMsg(constants.blankEvent)
                else:
                    if (event.data1 == mix.knobs[1][a]):
                        x = plugins.getParamValue(MAPPED_FUNCTION[str(b)], channels.selectedChannel())
                        y = round(x,2)
                        event.handled = True
                        
                        ui.setHintMsg(plugins.getParamName(MAPPED_FUNCTION[str(b)], channels.selectedChannel()))
                        
                        if mix.KNOB_DECREASE_MIN_SPEED >= event.data2 >= mix.KNOB_DECREASE_MAX_SPEED:
                            plugins.setParamValue((y - config.increment) , MAPPED_FUNCTION[str(b)], channels.selectedChannel()) 

                        elif mix.KNOB_INCREASE_MIN_SPEED <= event.data2 <= mix.KNOB_INCREASE_MAX_SPEED:
                            plugins.setParamValue((y + config.increment) , MAPPED_FUNCTION[str(b)], channels.selectedChannel())

                        mix.setTrackPan(a, str(round(100*plugins.getParamValue(MAPPED_FUNCTION[str(b)], channels.selectedChannel())   ), ))
                        mix.setTrackName(a, plugins.getParamName(MAPPED_FUNCTION[str(b)], channels.selectedChannel()))