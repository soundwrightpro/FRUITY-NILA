import nihia
from nihia import mixer as mix

from script.device_setup import config
from script.device_setup import NILA_core

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


jogMove = True


def encoder(self, event): 
    
    global jogMove
    if ui.getFocused(config.winName["Mixer"]) == True: #mixer control
        if (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.right): # encoder spin config.right 
            event.handled = True
            ui.jog(1)
            if ui.isInPopupMenu() == True:
                pass
            else:
                ui.setHintMsg(mixer.getTrackName(mixer.trackNumber()))
                jogMove = True

        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.left): # encoder spin config.left 
            event.handled = True
            ui.jog(-1)
            if ui.isInPopupMenu() == True:
                pass
            else:
                ui.setHintMsg(mixer.getTrackName(mixer.trackNumber()))
                jogMove = True

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.right): # encoder push config.right
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.right(1)
                pass
            else:
                ui.jog(8)
                ui.setHintMsg(mixer.getTrackName(mixer.trackNumber()))
                jogMove = True

        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.left): # encoder push config.left
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.left(1)
                pass
            else:
                ui.jog(-8)
                ui.setHintMsg(mixer.getTrackName(mixer.trackNumber()))
                jogMove = True


        if (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.up): # encoder push config.up
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.up(1)
            else:
                #pass
                mixer.armTrack(mixer.trackNumber())
                if mixer.isTrackArmed(mixer.trackNumber()) == True:
                    ui.setHintMsg("Armed Disk Recording")
                    mix.setTrackName(0, "Disk REC off")
                    time.sleep(config.timedelay)
                else:
                    ui.setHintMsg("Disarmed Disk Recording")
                    mix.setTrackName(0, "Disk REC on")
                    time.sleep(config.timedelay)

        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.down): # encoder push config.down
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.down(1)
            else:
                #pass
                if mixer.isTrackSlotsEnabled(mixer.trackNumber()) == True:
                    mixer.enableTrackSlots(mixer.trackNumber(),0)
                    mix.setTrackName(0, "Disable FX")
                    time.sleep(config.timedelay)
                else:
                    mixer.enableTrackSlots(mixer.trackNumber(),1)
                    mix.setTrackName(0, "Enable FX")
                    time.sleep(config.timedelay)


        if (event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON")):
            event.handled = True
            doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("ENCODER_BUTTON"))
            if doubleclickstatus == True:
                if ui.isInPopupMenu() == True:
                    ui.enter()
                    ui.setHintMsg("Enter")
                else:  
                    transport.globalTransport(midi.FPT_Menu, 90)
                    ui.setHintMsg("Open Menu")
                    mixer.deselectAll()
                    mixer.selectTrack(mixer.trackNumber())
            else:
                    if ui.isInPopupMenu() == True:
                        ui.enter()
                        ui.setHintMsg("Enter") 

        if ui.isInPopupMenu() == True:
            pass
        else:          
            if jogMove == True:# mixer highlighting when jog wheel is moved
                ui.miDisplayRect(mixer.trackNumber()+0,mixer.trackNumber()+7,1000)

    elif ui.getFocused(config.winName["Channel Rack"]) == True: 

        if ui.isInPopupMenu() == True:
            pass
        else:
            if (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.right): # encoder spin config.right 
                event.handled = True
                ui.jog(1)
                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
                ui.setHintMsg("Channel Rack selection rectangle")

            elif (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.left): # encoder spin config.left 
                event.handled = True
                ui.jog(-1)
                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
                ui.setHintMsg("Channel Rack selection rectangle")
            
            if (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.right): # encoder push config.right
                event.handled = True
                if ui.isInPopupMenu() == False:
                    ui.left(1)
                else:
                    ui.right(1)

                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
                ui.setHintMsg("Moving to the start of Channel Rack")

            elif (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.left): # encoder push config.left
                event.handled = True
                if ui.isInPopupMenu() == False:
                    ui.right(1)
                else:
                    ui.left(1)
                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
                ui.setHintMsg("Moving to the end of Channel Rack")

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.up): # encoder push config.up
            event.handled = True
            ui.up(1)
            ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
        
        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.down): # encoder push config.down
            event.handled = True
            ui.down(1)
            ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, 2000) #red rectangle
            

        if  (event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON")):
            event.handled = True
            doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("ENCODER_BUTTON"))
            if doubleclickstatus == True:
                if ui.isInPopupMenu() == False:
                    ui.selectBrowserMenuItem()
                    ui.setHintMsg("Channel display filter")
                else:
                    pass
            else:
                if ui.isInPopupMenu() == True:
                    ui.enter()
                    ui.setHintMsg("Enter")
                else:
                    pass
    elif ui.getFocused(config.winName["Plugin"]) == True: 

        if  (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.right): # encoder spin config.right 
            event.handled = True
            ui.down(1)
            

        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.left): # encoder spin config.left 
            event.handled = True
            ui.up(1)
        
        if (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.right): # encoder push config.right
            event.handled = True
            ui.right(1)

        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.left): # encoder push config.left
            event.handled = True
            ui.left(1)

        if channels.getChannelName(channels.selectedChannel()) in ui.getFocusedFormCaption():
            if (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.up): # encoder push config.up
                event.handled = True
                plugins.prevPreset(channels.channelNumber(channels.selectedChannel()))
            
            elif (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.down): # encoder push config.down
                event.handled = True
                plugins.nextPreset(channels.channelNumber(channels.selectedChannel()))
        else:
            if (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.up): # encoder push config.up
                event.handled = True
                ui.up()

            elif (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.down): # encoder push config.down
                event.handled = True
                ui.down()

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON")):
            event.handled = True
            doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("ENCODER_BUTTON"))
            if doubleclickstatus == True:
                pass
            else:
                ui.enter()
                ui.setHintMsg("enter")

    elif ui.getFocused(config.winName["Playlist"]) == True: 

        config.itemDisp = 0
        config.itemTime= 0

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.right): #4d encoder spin config.right 
            event.handled = True
            ui.jog(1)
            
        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.left): #4d encoder spin config.left 
            event.handled = True
            ui.jog(-1)
        
        if (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A"))  & (event.data2 == config.right): #4d encoder push config.right
            event.handled = True
            arrange.jumpToMarker(1,0)

        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A"))  & (event.data2 == config.left): #4d encoder push config.left
            event.handled = True
            arrange.jumpToMarker(-1,0)

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.up): #4d encoder push config.up
            event.handled = True
            ui.up(1)
        
        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.down): #4d encoder push config.down
            event.handled = True
            ui.down(1)

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON")):
            event.handled = True
            doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("ENCODER_BUTTON"))
            if doubleclickstatus == True:
                if ui.isInPopupMenu() == False:
                    timeDisp, currentTime = NILA_core.timeConvert(config.itemDisp, config.itemTime)

                    if ui.getTimeDispMin() == True:
                        #arrange.addAutoTimeMarker(mixer.getSongTickPos(), str("Time: " + currentTime))
                        arrange.addAutoTimeMarker(mixer.getSongTickPos(), str("Mark"))
                    else:
                        timeDisp == "Bar: "
                        #arrange.addAutoTimeMarker(mixer.getSongTickPos(), str("Beat: " + currentTime))
                        arrange.addAutoTimeMarker(mixer.getSongTickPos(), str("Mark"))
                        
                    

                else:
                    pass
            else:
                pass

    elif ui.getFocused(config.winName["Browser"]) == True: 

        if ui.getFocusedNodeFileType() == -100:
            mix.setTrackName(0, "Browser")
        else:
            if ui.getFocusedNodeFileType() == 7 or ui.getFocusedNodeFileType() == 13 or ui.getFocusedNodeFileType() == 14 or ui.getFocusedNodeFileType() == 15:
                mix.setTrackName(0, "B| sound:")
            else:
                mix.setTrackName(0, "B| file:")

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.right): # encoder spin config.right 
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.down()
            else:
                ui.next()
                mix.setTrackVol(0, ui.getFocusedNodeCaption()[:15])
            
        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.left): # encoder spin config.left 
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.up()
            else:
                ui.previous()
                mix.setTrackVol(0, ui.getFocusedNodeCaption()[:15])
            
        if (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.right): # encoder push config.right
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.right()
            else:
                ui.next()
            
        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.left): # encoder push config.left
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.left()
            else:
                ui.previous()

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.up): # encoder push config.up
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.up()
            else:
                ui.previous()
                mix.setTrackVol(0, ui.getFocusedNodeCaption()[:15])
                ui.previewBrowserMenuItem()
        
        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.down): # encoder push config.down
            event.handled = True
            if ui.isInPopupMenu() == True:
                ui.down()
            else:
                ui.next()
                mix.setTrackVol(0, ui.getFocusedNodeCaption()[:15])
                ui.previewBrowserMenuItem()

        if (event.data1 ==  nihia.buttons.button_list.get("ENCODER_BUTTON")):
            event.handled = True
            doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("ENCODER_BUTTON"))
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

    elif ui.getFocused(config.winName["Piano Roll"]) == True:
        if  (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.right): # encoder spin config.right 
            event.handled = True
            #ui.down(1)
            ui.jog(1)
            
        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.left): # encoder spin config.left 
            event.handled = True
            #ui.up(1)
            ui.jog(-1)
        
        if (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.right): # encoder push config.right
            event.handled = True
            ui.right(1)

        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.left): # encoder push config.left
            event.handled = True
            ui.left(1)

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.up): # encoder push config.up
            event.handled = True
            ui.up()
        
        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.down): # encoder push config.down
            event.handled = True
            ui.down()

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON")):
            event.handled = True
            doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("ENCODER_BUTTON"))
            if doubleclickstatus == True: 
                ui.selectBrowserMenuItem()
            else:
                if ui.isInPopupMenu() == True:
                    ui.enter()
                    ui.setHintMsg("Enter")
                else:
                    pass

    else:
        if  (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.right): # encoder spin config.right 
            event.handled = True
            ui.down(1)
            

        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL")) & (event.data2 == config.left): # encoder spin config.left 
            event.handled = True
            ui.up(1)
        
        if (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.right): # encoder push config.right
            event.handled = True
            ui.right(1)

        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_X_A")) & (event.data2 == config.left): # encoder push config.left
            event.handled = True
            ui.left(1)

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.up): # encoder push config.up
            event.handled = True
            ui.up()
        
        elif (event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A")) & (event.data2 == config.down): # encoder push config.down
            event.handled = True
            ui.down()

        if (event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON")):
            event.handled = True
            doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("ENCODER_BUTTON"))
            if doubleclickstatus == True:
                pass
            else:
                ui.enter()
                ui.setHintMsg("enter")