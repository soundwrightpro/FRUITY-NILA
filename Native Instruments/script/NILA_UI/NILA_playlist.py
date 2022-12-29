from nihia import mixer

from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED
from script.device_setup import config

import ui 


def OnIdle():

   timeDisp, currentTime = NILA_core.timeConvert(config.itemDisp, config.itemTime)


