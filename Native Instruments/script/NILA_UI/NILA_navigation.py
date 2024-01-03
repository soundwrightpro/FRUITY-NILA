# Import necessary modules and components
import nihia
from script.device_setup import NILA_core, config, constants as c
from script.screen_writer import NILA_OLED
import arrangement as arrange
import channels
import device
import midi
import mixer
import transport
import plugins
import ui
import time
import math



# Initialize variables for encoder movement on X and Y axes
xAxis, yAxis = 0, 0
windowCycle = 0
last_click_time = 0
current_track_plugin_id = None  # Variable to store the current track_plugin_id

def onButtonClick(button):
    global last_click_time

    

    # Get the current time
    current_time = time.time()

    # Check if it's a double-click
    if (current_time - last_click_time) < config.double_click_speed :  # Adjust the time window as needed
        double_click_status = True
    else:
        double_click_status = False

    # Update the last click time
    last_click_time = current_time

    return double_click_status



# Define the encoder function that handles various events
def encoder(self, event):
    global windowCycle

    global current_track_plugin_id  # Declare current_track_plugin_id as a global variable
    global_index = False


    
    """
    Handle encoder events for a specific controller.

    Parameters:
        self: The instance of the controller.
        event: The event triggered by the encoder movement.

    Returns:
        None
    """

    # Define a helper function for jogging in different UI contexts
    def jog(amount):
        """
        Perform jogging in the UI.

        Parameters:
            amount: The amount by which to jog.

        Returns:
            None
        """
        ui.jog(amount)
        if ui.getFocused(c.winName["Mixer"]):
            ui.miDisplayRect(mixer.trackNumber(), mixer.trackNumber() + 7, config.rectMixer)
            ui.setHintMsg(mixer.getTrackName(mixer.trackNumber()))
        elif ui.getFocused(c.winName["Channel Rack"]):
            ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
            ui.setHintMsg("Channel Rack selection rectangle")

    # Define a helper function for browsing through UI elements
    def browse(action):
        """
        Browse through UI elements.

        Parameters:
            action: The action to perform during browsing.

        Returns:
            None
        """
        
        if ui.isInPopupMenu():
            ui.down() if action == "next" else ui.up()
        else:
            ui.next() if action == "next" else ui.previous()
            NILA_OLED.OnIdle(self)
            if config.jog_preview_sound == 1:
                ui.previewBrowserMenuItem()
            elif device.getName() != "Komplete Kontrol DAW - 1":
                NILA_OLED.OnIdle(self)

    # Handle encoder jog wheel events

    if event.data1 in (
        nihia.buttons.button_list.get("ENCODER_GENERAL"),
        nihia.buttons.button_list.get("ENCODER_VOLUME_SELECTED")
    ):
        if not NILA_core.seriesCheck():
            plugin_skip = 1
        else:
            plugin_skip = 1 # normally 7   
        
        if event.data2 in (
            nihia.buttons.button_list.get("RIGHT"),
            c.mixer_right, 
        ):
            event.handled = True
            
            
            if ui.getFocused(c.winName["Mixer"]):
                jog(1)
            elif ui.getFocused(c.winName["Channel Rack"]):
                jog(1)
            elif ui.getFocused(c.winName["Plugin"]):
                
                if ui.getFocused(c.winName["Effect Plugin"]):
                    mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
                    track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
                    
                    if not track_plugin_id == c.last_plugin_name:
                        c.lead_param = 0
                        c.last_plugin_name = track_plugin_id
                                        
                    if plugins.isValid(mix_track_index, mixer_slot):
                        param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
                        
                        if param_count == 4240:
                            param_count = c.actual_param_count
                                                
                        #param_count_adjusted = math.ceil(param_count/c.knobs_available)
                        
                        if plugins.getPluginName(mix_track_index, mixer_slot, 0, global_index) in c.unsupported_plugins:
                            ui.down(1)
                        else:
                            if track_plugin_id != current_track_plugin_id:
                                c.lead_param = 0  # Reset page number
                                current_track_plugin_id = track_plugin_id
                            else:
                                c.lead_param = min(c.lead_param + plugin_skip, param_count)  # Increment and clamp
                                NILA_OLED.OnRefresh(self, event)

                elif ui.getFocused(c.winName["Generator Plugin"]): 
                    chan_track_index = channels.selectedChannel()

                    if channels.getChannelType() in (1, 2): 
                        if plugins.getPluginName(chan_track_index, -plugin_skip, global_index) in c.unsupported_plugins:
                            ui.down(1)
                        else:
                            pass
                    else:
                        pass
 
                
            elif ui.getFocused(c.winName["Playlist"]):
                ui.jog(1)
            elif ui.getFocused(c.winName["Piano Roll"]):
                ui.verZoom(-1)
            elif ui.getFocused(c.winName["Browser"]):
                browse("next")
            else:
                ui.down(1)
                

        elif event.data2 in (
            nihia.buttons.button_list.get("LEFT"),
            c.mixer_left,
        ):
            event.handled = True
            if ui.getFocused(c.winName["Mixer"]):
                jog(-1)
            elif ui.getFocused(c.winName["Channel Rack"]):
                jog(-1)
            elif ui.getFocused(c.winName["Plugin"]):
                 
                if ui.getFocused(c.winName["Effect Plugin"]):
                    mix_track_index, mixer_slot = mixer.getActiveEffectIndex()
                    if plugins.isValid(mix_track_index, mixer_slot):
                        track_plugin_id = mixer.getTrackPluginId(mix_track_index, mixer_slot)
                        param_count = plugins.getParamCount(mix_track_index, mixer_slot, global_index)
                        
                        if plugins.getPluginName(mix_track_index, mixer_slot, 0, global_index) in c.unsupported_plugins:
                            ui.up(1)
                        else:
                            if track_plugin_id != current_track_plugin_id:
                                c.lead_param = 0  # Reset page number
                                current_track_plugin_id = track_plugin_id
                            else:
                                c.lead_param = max(c.lead_param - plugin_skip, 0)  # Decrement and clamp
                                NILA_OLED.OnRefresh(self, event)
                    
                elif ui.getFocused(c.winName["Generator Plugin"]): 
                    chan_track_index = channels.selectedChannel()
                    if channels.getChannelType == 1 or 2:
                        if plugins.getPluginName(chan_track_index, - plugin_skip, global_index) in c.unsupported_plugins:
                            ui.up(1)
                        else:
                            pass
                    else:
                        pass
        
                        
            elif ui.getFocused(c.winName["Playlist"]):
                ui.jog(-1)
            elif ui.getFocused(c.winName["Piano Roll"]):
                ui.verZoom(1)
            elif ui.getFocused(c.winName["Browser"]):
                browse("previous")
            else:
                ui.up(1)

    if event.data1 == nihia.buttons.button_list.get("ENCODER_PAN_SELECTED"):
        
        if event.data2 in (
            nihia.buttons.button_list.get("RIGHT"),
            c.mixer_right, 
        ):
            event.handled = True
            if ui.getFocused(c.winName["Mixer"]):
                mixer.setTrackStereoSep(mixer.trackNumber(), mixer.getTrackStereoSep(mixer.trackNumber()) + c.stereo_sep)
                
            if ui.getFocused(c.winName["Playlist"]) or ui.getFocused(c.winName["Piano Roll"]):
                transport.globalTransport(midi.FPT_HZoomJog, 1, midi.PME_System, midi.GT_All)
    
        if event.data2 in (
            nihia.buttons.button_list.get("LEFT"),
            c.mixer_left, 
        ):
            event.handled = True
            if ui.getFocused(c.winName["Mixer"]):
                mixer.setTrackStereoSep(mixer.trackNumber(), mixer.getTrackStereoSep(mixer.trackNumber()) - c.stereo_sep)
            
            if ui.getFocused(c.winName["Playlist"]) or ui.getFocused(c.winName["Piano Roll"]):
                transport.globalTransport(midi.FPT_HZoomJog, -1, midi.PME_System, midi.GT_All)


    if event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON"):
        event.handled = True
        button_id = nihia.buttons.button_list.get("ENCODER_BUTTON")

        if ui.getFocused(c.winName["Mixer"]) or ui.getFocused(
                c.winName["Plugin"]) or ui.getFocused(c.winName["Piano Roll"]):
            if onButtonClick(button_id):
                if ui.isInPopupMenu():
                    ui.enter()
                    ui.setHintMsg("Enter")
                else:
                    transport.globalTransport(midi.FPT_Menu, midi.GT_Menu)
                    ui.setHintMsg("Open Menu")
                    mixer.deselectAll()
                    mixer.selectTrack(mixer.trackNumber())
                    
        elif ui.getFocused(c.winName["Channel Rack"]):
            if onButtonClick(button_id):
                if ui.isInPopupMenu():
                    ui.enter()
                    ui.setHintMsg("Enter")
                else:
                    transport.globalTransport(midi.FPT_ItemMenu, 4) #'/Applications/FL Studio 21.app/Contents/Libs/../Resources/FL/Shared/Python/Lib/midi.py'>
                    ui.setHintMsg("Open Menu")
                    mixer.deselectAll()
                    mixer.selectTrack(mixer.trackNumber())
                    
        elif ui.getFocused(c.winName["Playlist"]):
            if onButtonClick(button_id) and not ui.isInPopupMenu():
                arrange.addAutoTimeMarker(mixer.getSongTickPos(), str("Mark"))
        elif ui.getFocused(c.winName["Browser"]):
            if onButtonClick(button_id):
                if ui.getFocusedNodeFileType() <= -100:
                    ui.enter()
                    ui.setHintMsg("Enter")
                else:
                    ui.selectBrowserMenuItem()
                    ui.setHintMsg("Open menu")
        else:
            ui.enter()
            
    if event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON_SHIFTED"):
        event.handled = True

        button_id = nihia.buttons.button_list.get("ENCODER_BUTTON_SHIFTED")

        window_mappings = {
            0: (1, "Channel Rack"),
            1: (0, "Mixer"),
            2: (2, "Playlist"),
            3: (4, "Browser")
        }

        if onButtonClick(button_id):
            transport.globalTransport(midi.FPT_F8, 67)
            ui.setHintMsg("Plugin Picker")
        else:
            window, hint_msg = window_mappings[windowCycle]
            ui.showWindow(window)
            windowCycle = (windowCycle + 1) % 4
            ui.setHintMsg(hint_msg)

        

    if device.getName() == "Komplete Kontrol DAW - 1":
        yAxis, xAxis = nihia.buttons.button_list.get("ENCODER_Y_S"), nihia.buttons.button_list.get("ENCODER_X_S")
    else:
        yAxis, xAxis = nihia.buttons.button_list.get("ENCODER_Y_A"), nihia.buttons.button_list.get("ENCODER_X_A")

    if event.data1 == xAxis:
        event.handled = True
        if event.data2 == nihia.buttons.button_list.get("RIGHT"):
            if ui.getFocused(c.winName["Mixer"]):
                ui.right(1) if ui.isInPopupMenu() else jog(8)
                
            elif ui.getFocused(c.winName["Channel Rack"]):
                ui.right(1) if ui.isInPopupMenu() else ui.left(1)
                
            elif ui.getFocused(c.winName["Plugin"]):
                ui.right(1)
                
            elif ui.getFocused(c.winName["Playlist"]):
                arrange.jumpToMarker(1, 0)
                
            elif ui.getFocused(c.winName["Browser"]):
                ui.right()
                
            elif ui.getFocused(c.winName["Piano Roll"]):
                ui.right() if ui.isInPopupMenu() else ui.jog(1)
            else:
                ui.right(1)
                

        elif event.data2 == nihia.buttons.button_list.get("LEFT"):
            if ui.getFocused(c.winName["Mixer"]):
                ui.left(1) if ui.isInPopupMenu() else jog(-8)
                
            elif ui.getFocused(c.winName["Channel Rack"]):
                ui.left(1) if ui.isInPopupMenu() else ui.right(1)
                
            elif ui.getFocused(c.winName["Plugin"]):
                ui.left(1)
                
            elif ui.getFocused(c.winName["Playlist"]):
                arrange.jumpToMarker(-1, 0)
                
            elif ui.getFocused(c.winName["Browser"]):
                ui.left()
                
            elif ui.getFocused(c.winName["Piano Roll"]):
                ui.left() if ui.isInPopupMenu() else ui.jog(-1)
                
            else:
                ui.left(1)

    if event.data1 == yAxis:
        event.handled = True
        if event.data2 == nihia.buttons.button_list.get("UP"):
            if ui.getFocused(c.winName["Mixer"]):
                ui.up(1) if ui.isInPopupMenu() else None
            elif ui.getFocused(c.winName["Channel Rack"]):
                ui.up(1)
                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
            elif ui.getFocused(c.winName["Plugin"]):
                plugins.prevPreset(channels.channelNumber(channels.selectedChannel())) if channels.getChannelName(
                    channels.selectedChannel()
                ) in ui.getFocusedFormCaption() else ui.up()
            elif ui.getFocused(c.winName["Browser"]):
                ui.up() if ui.isInPopupMenu() else ui.previous()
                if config.upDown_preview_sound == 1 and device.getName() != "Komplete Kontrol DAW - 1":
                    ui.previewBrowserMenuItem()
                elif device.getName() != "Komplete Kontrol DAW - 1":
                    NILA_OLED.OnIdle(self)
            elif ui.getFocused(c.winName["Playlist"]):
                ui.up()
            elif ui.getFocused(c.winName["Piano Roll"]):
                ui.up()

        elif event.data2 == nihia.buttons.button_list.get("DOWN"):
            if ui.getFocused(c.winName["Mixer"]):
                ui.down(1) if ui.isInPopupMenu() else None
            elif ui.getFocused(c.winName["Channel Rack"]):
                ui.down(1)
                ui.crDisplayRect(0, channels.selectedChannel(), 256, 8, config.rectChannel)
            elif ui.getFocused(c.winName["Plugin"]):
                plugins.nextPreset(channels.channelNumber(channels.selectedChannel())) if channels.getChannelName(
                    channels.selectedChannel()
                ) in ui.getFocusedFormCaption() else ui.up()
            elif ui.getFocused(c.winName["Browser"]):
                ui.down() if ui.isInPopupMenu() else ui.next()
                if config.upDown_preview_sound == 1 and device.getName() != "Komplete Kontrol DAW - 1":
                    ui.previewBrowserMenuItem()
                elif device.getName() != "Komplete Kontrol DAW - 1":
                    NILA_OLED.OnIdle(self)
            elif ui.getFocused(c.winName["Playlist"]):
                ui.down()
            elif ui.getFocused(c.winName["Piano Roll"]):
                ui.down()

    return