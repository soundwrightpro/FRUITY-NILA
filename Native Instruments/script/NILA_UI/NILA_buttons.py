from nihia import buttons
from nihia.mixer import setTrackVol
from nihia.mixer import setTrackName
from nihia.mixer import setTrackPan

from script.device_setup import constants

import channels
import device
import general
import midi
import mixer 
import playlist
import time
import transport
import ui


on, off = 1, 0
windowCycle = 0
jogMove = True

 
def OnMidiMsg(event): #listens for button or knob activity

    global windowCycle
    global jogMove

    if (event.data1 == buttons.button_list.get("PLAY")):
        event.handled = True
        if ui.isInPopupMenu() == True:
            pass 
        else:
            transport.start() #play
            ui.setHintMsg("Play/Pause")

    if (event.data1 == buttons.button_list.get("RESTART")):
        event.handled = True
        transport.stop() #stop
        transport.start() #restart play at beginning
        setTrackName(0, "Metronome:")
        setTrackVol(0, "Enabled")
        ui.setHintMsg("Restart")
        
    if (event.data1 == buttons.button_list.get("REC")):
        event.handled = True
        transport.record() #record
        ui.setHintMsg("Record")

    if (event.data1 == buttons.button_list.get("STOP")):
        event.handled = True
        transport.stop() #stop
        ui.setHintMsg("Stop")

    if (event.data1 == buttons.button_list.get("LOOP")):
        event.handled = True
        transport.setLoopMode() #loop/pattern mode
        ui.setHintMsg("Song / pattern mode")

        if transport.getLoopMode() == off:
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                setTrackName(0, "Pattern:")
                setTrackVol(0, "Enabled")
                setTrackPan(0, "Enabled")
                time.sleep(constants.timedelay) 

        elif transport.getLoopMode() == on:
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                setTrackName(0, "Song:")
                setTrackVol(0, "Enabled")
                setTrackPan(0, "Enabled")
                time.sleep(constants.timedelay) 

    if (event.data1 == buttons.button_list.get("METRO")): # metronome/button
        event.handled = True
        transport.globalTransport(midi.FPT_Metronome, 110)
        ui.setHintMsg("Metronome")

        if ui.isMetronomeEnabled() == off: 
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                setTrackName(0, "Metronome:")
                setTrackVol(0, "Disabled")
                time.sleep(constants.timedelay) 

        elif ui.isMetronomeEnabled() == on:
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                setTrackName(0, "Metronome:")
                setTrackVol(0, "Enabled")
                time.sleep(constants.timedelay) 

    if (event.data1 == buttons.button_list.get("TEMPO")):
        event.handled = True
        transport.stop() #tap tempo

    if (event.data1 == buttons.button_list.get("QUANTIZE")):
        event.handled = True
        channels.quickQuantize(channels.channelNumber(),0)
        ui.setHintMsg("Quick Quantize")
        if device.getName() == "Komplete Kontrol DAW - 1":
            pass
        else:
            setTrackName(0, "Piano Roll")
            setTrackVol(0, "Quick Quantize")
            time.sleep(constants.timedelay) 

        
    if event.data1 == buttons.button_list.get("AUTO"):
        event.handled = True

        ui.snapMode(1)  # Snap toggle

        snapmode_mapping = {
            0: "Line",
            1: "Cell",
            3: "(none)",
            4: "1/6 step",
            5: "1/4 step",
            6: "1/3 step",
            7: "1/2 step",
            8: "Step",
            9: "1/6 beat",
            10: "1/4 beat",
            11: "1/3 beat",
            12: "1/2 beat",
            13: "Beat",
            14: "Bar"
        }

        snap_mode = ui.getSnapMode()
        snap_mode_name = snapmode_mapping.get(snap_mode, "Unknown")

        ui.setHintMsg(f"Snap: {snap_mode_name}")

        if device.getName() != "Komplete Kontrol DAW - 1":
            setTrackName(0, "Main Snap")
            setTrackPan(0, snap_mode_name)
            time.sleep(constants.timedelay)


    if (event.data1 == buttons.button_list.get("COUNT_IN")):
        event.handled = True
        transport.globalTransport(midi.FPT_CountDown, 115) #countdown before recording
        ui.setHintMsg("Countdown before recording")
        

        if ui.isPrecountEnabled() == 1: 
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                setTrackName(0, "Count In:")
                setTrackPan(0, "Enabled")
                time.sleep(constants.timedelay)   
        else:
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                setTrackName(0, "Count In:")
                setTrackPan(0, "Disabled")
                time.sleep(constants.timedelay) 

    if (event.data1 == buttons.button_list.get("CLEAR")):
        event.handled = True

        doubleclickstatus = device.isDoubleClick(buttons.button_list.get("CLEAR"))

        if doubleclickstatus == True:
            transport.globalTransport(midi.FPT_F12, 2, 15)
            ui.setHintMsg("Clear All Windows")
            if device.getName() == "Komplete Kontrol DAW - 1":
                pass
            else:
                setTrackName(0, "Clear All")
                time.sleep(constants.timedelay) 
        else:
            ui.escape() #escape key
            ui.setHintMsg("Close")


    if (event.data1 == buttons.button_list.get("UNDO")):
        event.handled = True
        undoLevel =  str(general.getUndoHistoryCount()-general.getUndoHistoryLast())

        general.undoUp() #undo 

        ui.setHintMsg(ui.getHintMsg())
        if device.getName() == "Komplete Kontrol DAW - 1":
            pass
        else:
            setTrackName(0, "History")
            setTrackVol(0, "Undo @ "+ undoLevel)
            time.sleep(constants.timedelay) 
        
        

    if (event.data1 == buttons.button_list.get("REDO")):
        event.handled = True
        undoLevel =  str(general.getUndoHistoryCount()-general.getUndoHistoryLast())

        general.undo() #redo

        ui.setHintMsg(ui.getHintMsg())
        setTrackName(0, "History")
        setTrackPan(0, "Redo @ "+ undoLevel)
        time.sleep(constants.timedelay)
        

    if (event.data1 == buttons.button_list.get("TEMPO")):
        event.handled = True
        transport.globalTransport(midi.FPT_TapTempo, 106) #tap tempo

    if (event.data1 == buttons.button_list.get("ENCODER_BUTTON_SHIFTED")):
        event.handled = True
 

        doubleclickstatus = device.isDoubleClick(buttons.button_list.get("ENCODER_BUTTON_SHIFTED"))


        if doubleclickstatus == True:

            if windowCycle == 0:
                windowCycle == 3
            else:
                windowCycle -= 1

            transport.globalTransport(midi.FPT_F8, 67)
            ui.setHintMsg("Plugin Picker")
            
            if " M " in device.getName():
                #setTrackName(0, "Window:")
                #setTrackPan(0, "Plugin Picker")
                time.sleep(constants.timedelay)
            
        else:
            
            if windowCycle == 0:
                ui.showWindow(1)
                windowCycle += 1
                ui.setHintMsg("Channel Rack")
                if " M " in device.getName():
                    #setTrackName(0, "Window:")
                    #setTrackPan(0, "Channel Rack")
                    time.sleep(constants.timedelay)

            elif windowCycle == 1:
                ui.showWindow(0)
                windowCycle += 1
                ui.setHintMsg("Mixer")
                if " M " in device.getName():
                    #setTrackName(0, "Window:")
                    #setTrackPan(0, "Mixer")
                    time.sleep(constants.timedelay)

            elif windowCycle == 2:
                ui.showWindow(2)
                windowCycle += 1
                ui.setHintMsg("Playlist")
                if " M " in device.getName():
                    #setTrackName(0, "Window:")
                    #setTrackPan(0, "Playlist")
                    time.sleep(constants.timedelay)

            elif windowCycle == 3:
                ui.showWindow(4)
                windowCycle = 0
                ui.setHintMsg("Browser")
                if " M " in device.getName():
                    #setTrackName(0, "Window:")
                    #setTrackPan(0, "Browser")
                    time.sleep(constants.timedelay)

                     
    if (event.data1 == buttons.button_list.get("MUTE_SELECTED")):
        if ui.getFocused(0) == True: 
            event.handled = True
            if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= constants.currentUtility:
                pass
            else:
                mixer.enableTrack(mixer.trackNumber()) 
                ui.setHintMsg("Mute")
   
    if (event.data1 ==  buttons.button_list.get("SOLO_SELECTED")): 
        if ui.getFocused(0) == True: 
            event.handled = True
            if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= constants.currentUtility:
                pass
            else:
                mixer.soloTrack(mixer.trackNumber()) 
                ui.setHintMsg("Solo")

    if (event.data1 == buttons.button_list.get("MUTE_SELECTED")):
        if ui.getFocused(1) == True: 
            event.handled = True
            channels.muteChannel(channels.channelNumber()) 
            ui.setHintMsg("Mute")
        
    if (event.data1 ==  buttons.button_list.get("SOLO_SELECTED")): 
        if ui.getFocused(1) == True: 
            event.handled = True
            channels.soloChannel(channels.channelNumber()) 
            ui.setHintMsg("Solo")


    
    if ui.getFocused(constants.winName["Mixer"]) == True:
        
        #s-series mixer mute 
        for x in range(8):
            if event.data1 == buttons.button_list.get("MUTE") and event.data2 == x:
                event.handled = True
                if mixer.trackNumber() + x <= constants.currentUtility - 1:
                    mixer.enableTrack(mixer.trackNumber() + x) 
                    ui.setHintMsg("Mute") 
                else:
                    pass              

        #s-series mixer solo 
        for x in range(8):
            if event.data1 == buttons.button_list.get("SOLO") and event.data2 == x:
                event.handled = True
                if mixer.trackNumber() + x <= constants.currentUtility - 1:
                    mixer.soloTrack(mixer.trackNumber() + x)  
                    ui.setHintMsg("Solo")
                else:
                    pass

        #s-series mixer arm recording
        for x in range(8):
            if event.data1 == constants.select and event.data2 == x:
                event.handled = True
                if mixer.trackNumber() + x <= constants.currentUtility - 1:
                    mixer.armTrack(mixer.trackNumber() + x)
                    ui.setHintMsg("Armed Disk Recording")
                else:
                    pass

    
    if ui.getFocused(constants.winName["Channel Rack"]) == True:
        
        #s-series channel rack mute 
        for x in range(8):
            if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
                if event.data1 == buttons.button_list.get("MUTE") and event.data2 == x:
                    event.handled = True
                    channels.muteChannel(channels.selectedChannel() + x) 
                    ui.setHintMsg("Mute")  

        #s-series channel rack solo
        for x in range(8):
            if channels.channelCount() > x and channels.selectedChannel() < (channels.channelCount() - x):
                if event.data1 == buttons.button_list.get("SOLO") and event.data2 == x: 
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