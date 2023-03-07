from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED

import channels
import device
import math
import midi
import plugins
import ui 

touch_strips = {
   "PITCH": 0,
   "MOD": 1,
   "EXPRESSION": 11 
}


def OnMidiIn(event):

    if (event.data1 == touch_strips["MOD"]):
        event.handled = True

    if (event.data1 == touch_strips["EXPRESSION"]):
        event.handled = True


    if ui.getFocused(5) == True: #plugin

        if (event.data1 == touch_strips["MOD"]):
            event.handled = True

            if plugins.isValid(channels.selectedChannel()):
                plugins.setParamValue((event.data2/127/10)/0.50/2*10, 4097, channels.selectedChannel(), -1, 2)
                
                ui.setHintMsg("Modulation: %s" % round(event.data2/1.27))
            else:
                ui.setHintMsg("Modulation: %s" % round(event.data2/1.27))


        if (event.data1 == touch_strips["EXPRESSION"]):
            event.handled = True

            if plugins.isValid(channels.selectedChannel()):    
                plugins.setParamValue(event.data2/127, 4096 + event.data1, channels.selectedChannel(), -1, 2) 

                ui.setHintMsg("Expression: %s" % round(event.data2/1.27))
            else:
                ui.setHintMsg("Expression: %s" % round(event.data2/1.27))




