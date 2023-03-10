import nihia
from nihia import buttons 
from nihia import mixer as mix

from script.device_setup import constants

import channels
import device
import general
import math
import midi
import mixer
import playlist
import time
import transport
import ui


on = 1
off = 0
windowCycle = 0
jogMove = True

 
def OnMidiMsg(event): #listens for button or knob activity

    global windowCycle
    global jogMove

    if (event.data1 == nihia.buttons.button_list.get("PLAY")):
        event.handled = True
        if ui.isInPopupMenu() == True:
            pass 
        else:
            transport.start() #play
            ui.setHintMsg("Play/Pause")

    if (event.data1 == nihia.buttons.button_list.get("RESTART")):
        event.handled = True
        transport.stop() #stop
        transport.start() #restart play at beginning
        ui.setHintMsg("Restart")
        
    if (event.data1 == nihia.buttons.button_list.get("REC")):
        event.handled = True
        transport.record() #record
        ui.setHintMsg("Record")

    if (event.data1 == nihia.buttons.button_list.get("STOP")):
        event.handled = True
        transport.stop() #stop
        ui.setHintMsg("Stop")

    if (event.data1 == nihia.buttons.button_list.get("LOOP")):
        event.handled = True
        transport.setLoopMode() #loop/pattern mode
        ui.setHintMsg("Song / pattern mode")

        if transport.getLoopMode() == off:
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Pattern:")
                mix.setTrackVol(0, "Enabled")
                mix.setTrackPan(0, "Enabled")
                time.sleep(constants.timedelay) 

        elif transport.getLoopMode() == on:
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Song:")
                mix.setTrackVol(0, "Enabled")
                mix.setTrackPan(0, "Enabled")
                time.sleep(constants.timedelay) 

    if (event.data1 == nihia.buttons.button_list.get("METRO")): # metronome/button
        event.handled = True
        transport.globalTransport(midi.FPT_Metronome, 110)
        ui.setHintMsg("Metronome")

        if ui.isMetronomeEnabled() == off: 
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Metronome:")
                mix.setTrackVol(0, "Disabled")
                time.sleep(constants.timedelay) 

        elif ui.isMetronomeEnabled() == on:
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Metronome:")
                mix.setTrackVol(0, "Enabled")
                time.sleep(constants.timedelay) 

    if (event.data1 == nihia.buttons.button_list.get("TEMPO")):
        event.handled = True
        transport.stop() #tap tempo

    if (event.data1 == nihia.buttons.button_list.get("QUANTIZE")):
        event.handled = True
        channels.quickQuantize(channels.channelNumber(),0)
        ui.setHintMsg("Quick Quantize")
        if device.getName() == "Komplete Kontrol DAW - 1":
            pass
        else:
            mix.setTrackName(0, "Piano Roll")
            mix.setTrackVol(0, "Quick Quantize")
            time.sleep(constants.timedelay) 

        

    if (event.data1 == nihia.buttons.button_list.get("AUTO")):
        event.handled = True

        
        ui.snapMode(1) #snap toggle
        

        snapmodevalue = ["Line", "Cell", "None", 
        "1/6 Step", "1/4 Step", "1/3 Step", "1/2 Step", 
        "Step", "1/6 Beat", "1/4 Beat", "1/3 Beat", 
        " 1/2 Beat", "Beat", "Bar"]

        if ui.getSnapMode() == 0: 
            ui.setHintMsg("Snap: Line")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[0])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 1:
            ui.setHintMsg("Snap: Cell") 
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[1])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 3: 
            ui.setHintMsg("Snap: (none)")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[2])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 4:
            ui.setHintMsg("Snap: 1/6 step")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[3])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 5: 
            ui.setHintMsg("Snap: 1/4 step")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[4])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 6: 
            ui.setHintMsg("Snap: 1/3 step")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[5])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 7: 
            ui.setHintMsg("Snap: 1/2 step")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[6])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 8: 
            ui.setHintMsg("Snap: Step")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[7])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 9: 
            ui.setHintMsg("Snap: 1/6 beat")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[8])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 10: 
            ui.setHintMsg("Snap: 1/4 beat")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[9])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 11: 
            ui.setHintMsg("Snap: 1/3 beat")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[10])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 12: 
            ui.setHintMsg("Snap: 1/2 beat")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[11])
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 13:
            ui.setHintMsg("Snap: Beat")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[12])         
                time.sleep(constants.timedelay) 

        elif ui.getSnapMode() == 14: 
            ui.setHintMsg("Snap: Bar")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Main Snap")
                mix.setTrackPan(0, snapmodevalue[13])           
                time.sleep(constants.timedelay) 


    if (event.data1 == nihia.buttons.button_list.get("COUNT_IN")):
        event.handled = True
        transport.globalTransport(midi.FPT_CountDown, 115) #countdown before recording
        ui.setHintMsg("Countdown before recording")
        

        if ui.isPrecountEnabled() == 1: 
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Count In:")
                mix.setTrackPan(0, "Enabled")
                time.sleep(constants.timedelay)   
        else:
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Count In:")
                mix.setTrackPan(0, "Disabled")
                time.sleep(constants.timedelay) 

    if (event.data1 == nihia.buttons.button_list.get("CLEAR")):
        event.handled = True

        doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("CLEAR"))

        if doubleclickstatus == True:
            transport.globalTransport(midi.FPT_F12, 2, 15)
            ui.setHintMsg("Clear All Windows")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Clear All")
                time.sleep(constants.timedelay) 
        else:
            ui.escape() #escape key
            ui.setHintMsg("Close")


    if (event.data1 == nihia.buttons.button_list.get("UNDO")):
        event.handled = True
        undoLevel =  str(general.getUndoHistoryCount()-general.getUndoHistoryLast())

        general.undoUp() #undo 

        ui.setHintMsg(ui.getHintMsg())
        if device.getName() == "Komplete Kontrol DAW - 1":
            pass
        else:
            mix.setTrackName(0, "History")
            mix.setTrackVol(0, "Undo @ "+ undoLevel)
            time.sleep(constants.timedelay) 
        
        

    if (event.data1 == nihia.buttons.button_list.get("REDO")):
        event.handled = True
        undoLevel =  str(general.getUndoHistoryCount()-general.getUndoHistoryLast())

        general.undo() #redo

        ui.setHintMsg(ui.getHintMsg())
        mix.setTrackName(0, "History")
        mix.setTrackPan(0, "Redo @ "+ undoLevel)
        time.sleep(constants.timedelay)
        

    if (event.data1 == nihia.buttons.button_list.get("TEMPO")):
        event.handled = True
        transport.globalTransport(midi.FPT_TapTempo, 106) #tap tempo

    if (event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON_SHIFTED")):
        event.handled = True
 

        doubleclickstatus = device.isDoubleClick(nihia.buttons.button_list.get("ENCODER_BUTTON_SHIFTED"))


        if doubleclickstatus == True:

            if windowCycle == 0:
                windowCycle == 3
            else:
                windowCycle -= 1

            transport.globalTransport(midi.FPT_F8, 67)
            ui.setHintMsg("Plugin Picker")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                mix.setTrackName(0, "Window:")
                mix.setTrackPan(0, "Plugin Picker")
                time.sleep(constants.timedelay)
        else:

            if windowCycle == 0:
                ui.showWindow(1)
                windowCycle += 1
                ui.setHintMsg("Channel Rack")
                if device.getName() == "Komplete Kontrol DAW - 1":
                    pass
                else:
                    mix.setTrackName(0, "Window:")
                    mix.setTrackPan(0, "Channel Rack")
                    time.sleep(constants.timedelay)

            elif windowCycle == 1:
                ui.showWindow(0)
                windowCycle += 1
                ui.setHintMsg("Mixer")
                if device.getName() == "Komplete Kontrol DAW - 1":
                    pass
                else:
                    mix.setTrackName(0, "Window:")
                    mix.setTrackPan(0, "Mixer")
                    time.sleep(constants.timedelay)

            elif windowCycle == 2:
                ui.showWindow(2)
                windowCycle += 1
                ui.setHintMsg("Playlist")
                if device.getName() == "Komplete Kontrol DAW - 1":
                    pass
                else:
                    mix.setTrackName(0, "Window:")
                    mix.setTrackPan(0, "Playlist")
                    time.sleep(constants.timedelay)

            elif windowCycle == 3:
                ui.showWindow(4)
                ui.setHintMsg("Browser")
                if device.getName() == "Komplete Kontrol DAW - 1":
                    pass
                else:
                    mix.setTrackName(0, "Window:")
                    mix.setTrackPan(0, "Browser")
                    time.sleep(constants.timedelay)

                if ui.getVisible(3) == True:
                    windowCycle += 1
                else:
                    windowCycle = 0

            elif windowCycle == 4:
                    ui.showWindow(3)
                    ui.setHintMsg("Piano Roll")
                    if device.getName() == "Komplete Kontrol DAW - 1":
                        pass
                    else:
                            mix.setTrackName(0, "Window:")
                            mix.setTrackPan(0, "Piano Roll")
                            time.sleep(constants.timedelay)
                    windowCycle = 0
                    
                     
    if (event.data1 == nihia.buttons.button_list.get("MUTE_SELECTED")):
        if ui.getFocused(0) == True: 
            event.handled = True
            if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= constants.currentUtility:
                pass
            else:
                mixer.enableTrack(mixer.trackNumber()) 
                ui.setHintMsg("Mute")
   
    if (event.data1 ==  nihia.buttons.button_list.get("SOLO_SELECTED")): 
        if ui.getFocused(0) == True: 
            event.handled = True
            if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= constants.currentUtility:
                pass
            else:
                mixer.soloTrack(mixer.trackNumber()) 
                ui.setHintMsg("Solo")

    if (event.data1 == nihia.buttons.button_list.get("MUTE_SELECTED")):
        if ui.getFocused(1) == True: 
            event.handled = True
            channels.muteChannel(channels.channelNumber()) 
            ui.setHintMsg("Mute")
        
    if (event.data1 ==  nihia.buttons.button_list.get("SOLO_SELECTED")): 
        if ui.getFocused(1) == True: 
            event.handled = True
            channels.soloChannel(channels.channelNumber()) 
            ui.setHintMsg("Solo")


    
    if ui.getFocused(constants.winName["Mixer"]) == True:
        
        #s-series mixer mute 
        for x in range(8):
            if event.data1 == nihia.buttons.button_list.get("MUTE") and event.data2 == x:
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber() + x) == "Current" and (mixer.trackNumber() + x) >= constants.currentUtility:
                    pass
                else:
                    mixer.enableTrack(mixer.trackNumber() + x) 
                    ui.setHintMsg("Mute")                

        #s-series mixer solo 
        for x in range(8):
            if event.data1 == nihia.buttons.button_list.get("SOLO") and event.data2 == x:
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber() + x) == "Current" and (mixer.trackNumber() + x) >= constants.currentUtility:
                    pass
                else:
                    mixer.soloTrack(mixer.trackNumber() + x)  
                    ui.setHintMsg("Solo")

        #s-series mixer arm recording
        for x in range(8):
            if event.data1 == constants.select and event.data2 == x:
                event.handled = True
                if mixer.getTrackName(mixer.trackNumber() + x) == "Current" and (mixer.trackNumber() + x) >= constants.currentUtility:
                    pass
                else:
                    mixer.armTrack(mixer.trackNumber() + x) 
                    ui.setHintMsg("Armed Disk Recording")

    
    if ui.getFocused(constants.winName["Channel Rack"]) == True:

        #s-series channel rack mute 
        for x in range(8):
            if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
                if event.data1 == nihia.buttons.button_list.get("MUTE") and event.data2 == x:
                    event.handled = True
                    channels.muteChannel(channels.selectedChannel() + x) 
                    ui.setHintMsg("Mute")  

        #s-series channel rack solo
        for x in range(8):
            if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
                if event.data1 == nihia.buttons.button_list.get("SOLO") and event.data2 == x: 
                    event.handled = True
                    if channels.isChannelMuted(channels.selectedChannel() + x) == True and channels.channelCount() == 1:
                        pass
                    else:
                        channels.soloChannel(channels.selectedChannel() + x)  
                        ui.setHintMsg("Solo")

        #s-series channel rack select 
        for x in range(8):
            if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
                if event.data1 == constants.select and event.data2 == x: 
                    event.handled = True
                    channels.selectOneChannel(channels.selectedChannel() + x)  
                    ui.setHintMsg("Track selected")
                    
    if ui.getFocused(constants.winName["Playlist"]) == True:
        
        #s-series playlist select 
        for x in range(8):
            if event.data1 == constants.select and event.data2 == x: 
                event.handled = True
                playlist.selectTrack()
                ui.setHintMsg("")
                    