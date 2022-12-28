from nihia import mixer

from script.device_setup import config
from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED

import ui 


def OnIdle():

   timeDisp, currentTime = NILA_core.timeConvert(config.itemDisp, config.itemTime)

   if ui.getFocused(config.winName["Playlist"]) == True: 
      
      NILA_OLED.updateText(str(timeDisp), 0)
      NILA_OLED.updateText(config.blankEvent, 1)
      NILA_OLED.updateText(config.blankEvent, 2)
      NILA_OLED.updateText(config.blankEvent, 3)
      NILA_OLED.updateText(config.blankEvent, 4)
      NILA_OLED.updateText(config.blankEvent, 5)
      NILA_OLED.updateText(config.blankEvent, 6)
      NILA_OLED.updateText(config.blankEvent, 7)

      split_message = ui.getHintMsg()
      split_point1 = ' - '
      split_point2 = ' to '

      if split_point1 in split_message.lower():
         split_hint = split_message.partition(split_point1)[2]
      else:
         split_hint = split_message.partition(split_point2)[2]

      mixer.setTrackVol(0, str(split_hint[:7] + "| " + currentTime))
      mixer.setTrackVol(1, config.blankEvent)
      mixer.setTrackVol(2, config.blankEvent)
      mixer.setTrackVol(3, config.blankEvent)
      mixer.setTrackVol(4, config.blankEvent)
      mixer.setTrackVol(5, config.blankEvent)
      mixer.setTrackVol(6, config.blankEvent)
      mixer.setTrackVol(7, config.blankEvent)

      mixer.setTrackPan(0, config.blankEvent)
      mixer.setTrackPan(1, config.blankEvent)
      mixer.setTrackPan(2, config.blankEvent)
      mixer.setTrackPan(3, config.blankEvent)
      mixer.setTrackPan(4, config.blankEvent)
      mixer.setTrackPan(5, config.blankEvent)
      mixer.setTrackPan(6, config.blankEvent)
      mixer.setTrackPan(7, config.blankEvent)



