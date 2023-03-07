import nihia
from nihia import mixer as nihia_mix

from script.device_setup import config
from script.device_setup import constants
from script.device_setup import NILA_core
from script.screen_writer import NILA_OLED as oled

import arrangement as arrange
import channels
import device 
import math
import midi
import mixer
import time
import transport
import plugins
import ui 

mixer_right = 63
mixer_left = 65

xAxis, yAxis = 0, 0,

def encoder(self, event): 

    if event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL") or event.data1 == nihia.buttons.button_list.get("ENCODER_VOLUME_SELECTED") or event.data1 == nihia.buttons.button_list.get("ENCODER_PAN_SELECTED"):
        if event.data2 == nihia.buttons.button_list.get("RIGHT") or event.data2 == mixer_right: # encoder spin right 
            event.handled = True
            if ui.getFocused(constants.winName["Mixer"])== True: 
                if ui.isInPopupMenu() == True:
                    ui.down()
                else:
                    ui.jog(1)
                    ui.miDisplayRect(mixer.trackNumber()+0,mixer.trackNumber() + 7, config.rectMixer)
                    ui.setHintMsg(mixer.getTrackName(mixer.trackNumber()))

            elif ui.getFocused(constants.winName["Channel Rack"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.down()
                else:
                    ui.jog(1)
                    ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel) #red rectangle
                    ui.setHintMsg("Channel Rack selection rectangle")

            elif ui.getFocused(constants.winName["Plugin"]) == True:   
                ui.down(1)   
            
            elif ui.getFocused(constants.winName["Playlist"]) == True: 
                ui.jog(1)

            elif ui.getFocused(constants.winName["Piano Roll"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.down()
                else: 
                    ui.verZoom(-1)

            elif ui.getFocused(constants.winName["Browser"]) == True: 
                if ui.isInPopupMenu() == True:
                    ui.down()
                else:
                    ui.next()
                    oled.updateBrowser()
                    if config.jog_preview_sound == 1:
                        ui.previewBrowserMenuItem()
                    else:
                        pass
                    if device.getName() == "Komplete Kontrol DAW - 1":
                        pass
                    else:
                        oled.updateBrowser()
            else:
                ui.down(1)


        if event.data2 == nihia.buttons.button_list.get("LEFT") or event.data2 == mixer_left: # encoder spin left 
            event.handled = True
            if ui.getFocused(constants.winName["Mixer"])== True: 
                if ui.isInPopupMenu() == True:
                    ui.up()
                else:
                    ui.jog(-1)
                    ui.miDisplayRect(mixer.trackNumber()+0,mixer.trackNumber() + 7,config.rectMixer)
                    ui.setHintMsg(mixer.getTrackName(mixer.trackNumber()))

            elif ui.getFocused(constants.winName["Channel Rack"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.up()
                else:
                    ui.jog(-1)
                    ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel) #red rectangle
                    ui.setHintMsg("Channel Rack selection rectangle")

            elif ui.getFocused(constants.winName["Plugin"]) == True:   
                ui.up(1)

            elif ui.getFocused(constants.winName["Playlist"]) == True: 
                ui.jog(-1) 

            elif ui.getFocused(constants.winName["Piano Roll"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.up()
                else: 
                    ui.verZoom(1)

            elif ui.getFocused(constants.winName["Browser"]) == True: 
                if ui.isInPopupMenu() == True:
                    ui.up()
                else:
                    ui.previous()
                    oled.updateBrowser()
                    if config.jog_preview_sound == 1:
                        ui.previewBrowserMenuItem()
                    else:
                        pass
                    if device.getName() == "Komplete Kontrol DAW - 1":
                        pass
                    else:
                        oled.updateBrowser()
            else:
                ui.up(1)
                

    if (event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON")):
        event.handled = True
        doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("ENCODER_BUTTON"))
        
        if ui.getFocused(constants.winName["Mixer"]) == True or ui.getFocused(constants.winName["Channel Rack"]) == True or ui.getFocused(constants.winName["Plugin"]) == True or ui.getFocused(constants.winName["Piano Roll"]) == True:
        
            if doubleclickstatus == True:
                if ui.isInPopupMenu() == True:
                    ui.enter()
                    ui.setHintMsg("Enter")
                else:  
                    transport.globalTransport(midi.FPT_Menu, 4)
                    ui.setHintMsg("Open Menu")
                    mixer.deselectAll()
                    mixer.selectTrack(mixer.trackNumber())
            else:
                    if ui.isInPopupMenu() == True:
                        ui.enter()
                        ui.setHintMsg("Enter") 

        elif ui.getFocused(constants.winName["Playlist"]) == True: 
            if doubleclickstatus == True:
                if ui.isInPopupMenu() == False:
                    arrange.addAutoTimeMarker(mixer.getSongTickPos(), str("Mark"))
                else:
                    pass
            else:
                pass

        elif ui.getFocused(constants.winName["Browser"]) == True:
            if doubleclickstatus == True: 
                if ui.getFocusedNodeFileType() <= -100:
                    ui.enter()
                    ui.setHintMsg("Enter")
                else:
                    ui.selectBrowserMenuItem()
                    ui.setHintMsg("Open menu")   
            else:
                if ui.isInPopupMenu() == True:
                    ui.enter()
                    ui.setHintMsg("Enter")
                else:
                    pass
        else:
            ui.enter()


    if device.getName() == "Komplete Kontrol DAW - 1":
        yAxis = nihia.buttons.button_list.get("ENCODER_Y_S")
        xAxis = nihia.buttons.button_list.get("ENCODER_X_S")
    else:
        yAxis = nihia.buttons.button_list.get("ENCODER_Y_A")
        xAxis = nihia.buttons.button_list.get("ENCODER_X_A")


    if event.data1 == xAxis:
        if event.data2 == nihia.buttons.button_list.get("RIGHT"):
            event.handled = True
            if ui.getFocused(constants.winName["Mixer"])== True:
                if ui.isInPopupMenu() == True:
                    ui.right(1)
                else:
                    ui.jog(8)
                    ui.miDisplayRect(mixer.trackNumber()+0,mixer.trackNumber() + 7,config.rectMixer)
                    ui.setHintMsg(mixer.getTrackName(mixer.trackNumber()))
                    jogMove = True

            elif ui.getFocused(constants.winName["Channel Rack"]) == True:
                if ui.isInPopupMenu() == False:
                    ui.left(1)
                else:
                    ui.right(1)
                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel) #red rectangle
                ui.setHintMsg("Moving to the start of Channel Rack")

            elif ui.getFocused(constants.winName["Plugin"]) == True:   
                ui.right(1)

            elif ui.getFocused(constants.winName["Playlist"]) == True: 
                arrange.jumpToMarker(1,0)
            
            elif ui.getFocused(constants.winName["Browser"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.right()

            elif ui.getFocused(constants.winName["Piano Roll"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.right()
                else:
                    ui.jog(1)
            else:
                ui.right(1)

    if event.data1 == xAxis:
        if event.data2 == nihia.buttons.button_list.get("LEFT"):
            event.handled = True
            if ui.getFocused(constants.winName["Mixer"])== True:
                if ui.isInPopupMenu() == True:
                    ui.left(1)
                else:
                    ui.jog(-8)
                    ui.miDisplayRect(mixer.trackNumber()+0,mixer.trackNumber() + 7,config.rectMixer)
                    ui.setHintMsg(mixer.getTrackName(mixer.trackNumber()))
                    jogMove = True

            elif ui.getFocused(constants.winName["Channel Rack"]) == True:
                if ui.isInPopupMenu() == False:
                    ui.right(1)
                else:
                    ui.left(1)
                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel) #red rectangle
                ui.setHintMsg("Moving to the end of Channel Rack")

            elif ui.getFocused(constants.winName["Plugin"]) == True:   
                ui.left(1)

            elif ui.getFocused(constants.winName["Playlist"]) == True: 
                arrange.jumpToMarker(-1,0)

            elif ui.getFocused(constants.winName["Browser"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.left()
                    
            elif ui.getFocused(constants.winName["Piano Roll"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.left()
                else:
                    ui.jog(-1)
            else:
                ui.left(1)


    if event.data1 == yAxis:
        if event.data2 == nihia.buttons.button_list.get("UP"):
            event.handled = True
            if ui.getFocused(constants.winName["Mixer"])== True:
                if ui.isInPopupMenu() == True:
                    ui.up(1)
                else:
                    pass

            elif ui.getFocused(constants.winName["Channel Rack"]) == True:
                event.handled = True
                ui.up(1)
                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel) #red rectangle

            elif ui.getFocused(constants.winName["Plugin"]) == True:
                if channels.getChannelName(channels.selectedChannel()) in ui.getFocusedFormCaption():
                    plugins.prevPreset(channels.channelNumber(channels.selectedChannel()))
                else:
                    ui.up()

            elif ui.getFocused(constants.winName["Browser"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.up()
                else:
                    ui.previous()

                    if config.upDown_preview_sound == 1:
                        ui.previewBrowserMenuItem()
                    else:
                        pass
                    if device.getName() == "Komplete Kontrol DAW - 1":
                            pass
                    else:
                        oled.updateBrowser()


            elif ui.getFocused(constants.winName["Piano Roll"]) == True:
                ui.up()

    if event.data1 == yAxis:
        if event.data2 == nihia.buttons.button_list.get("DOWN"):
            event.handled = True
            if ui.getFocused(constants.winName["Mixer"])== True:
                if ui.isInPopupMenu() == True:
                        ui.down(1)
                else:
                    pass

            elif ui.getFocused(constants.winName["Channel Rack"]) == True:
                event.handled = True
                ui.down(1)
                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel) #red rectangle     

            elif ui.getFocused(constants.winName["Plugin"]) == True:
                if channels.getChannelName(channels.selectedChannel()) in ui.getFocusedFormCaption():
                    plugins.nextPreset(channels.channelNumber(channels.selectedChannel()))
                else:
                     ui.up()   

            elif ui.getFocused(constants.winName["Browser"]) == True:
                if ui.isInPopupMenu() == True:
                    ui.down()
                else:
                    ui.next()

                    if config.upDown_preview_sound == 1:
                        ui.previewBrowserMenuItem()
                    else:
                        pass 
                    if device.getName() == "Komplete Kontrol DAW - 1":
                        pass
                    else:
                        
                        oled.updateBrowser()

            elif ui.getFocused(constants.winName["Piano Roll"]) == True:
                ui.down()