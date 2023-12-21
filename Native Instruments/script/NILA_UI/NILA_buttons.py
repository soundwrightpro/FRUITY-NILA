from nihia import buttons
from nihia.mixer import setTrackVol, setTrackName, setTrackPan
from script.device_setup import constants
import channels
import device
import general
import midi
import time
import transport
import ui

# Constants for on and off states
on, off = 1, 0

# Global variables
windowCycle = 0
jogMove = True


def set_track_info(track_index, name, vol, pan=None):
    """
    Set track information such as name, volume, and pan.

    Args:
        track_index (int): Index of the track.
        name (str): Name to set for the track.
        vol (str): Volume information to set for the track.
        pan (str, optional): Pan information to set for the track. Defaults to None.
    """
    if device.getName() != "Komplete Kontrol DAW - 1":
        setTrackName(track_index, name)
        setTrackVol(track_index, vol)
        if pan is not None:
            setTrackPan(track_index, pan)


def handle_metronome_enabled():
    """
    Handle metronome enabled state and update track information.
    """
    if ui.isMetronomeEnabled() == off:
        set_track_info(0, "Metronome:", "Disabled")
    elif ui.isMetronomeEnabled() == on:
        set_track_info(0, "Metronome:", "Enabled")


def handle_precount_enabled():
    """
    Handle precount enabled state and update track information.
    """
    set_track_info(0, "Count In:", "Enabled" if ui.isPrecountEnabled() == 1 else "Disabled")


def handle_mixer_action(event, action_function, track_number, hint_message):
    """
    Handle mixer actions.

    Args:
        event (MIDIEvent): MIDI event to handle.
        action_function (function): Mixer action function.
        track_number (int): Track number for the action.
        hint_message (str): Hint message for UI.
    """
    event.handled = True
    if track_number <= constants.currentUtility - 1:
        action_function(track_number)
        ui.setHintMsg(hint_message)
    else:
        pass


def OnMidiMsg(event):
    """
    Handle MIDI messages.

    Args:
        event (MIDIEvent): MIDI event to handle.
    """
    global windowCycle, jogMove

    # Mark the event as handled
    event.handled = True

    if event.data1 == buttons.button_list.get("PLAY") and not ui.isInPopupMenu():
        transport.start()  # play
        ui.setHintMsg("Play/Pause")

    elif event.data1 == buttons.button_list.get("RESTART"):
        transport.stop()  # stop
        transport.start()  # restart play at the beginning
        set_track_info(0, "Metronome:", "Enabled")
        ui.setHintMsg("Restart")

    elif event.data1 == buttons.button_list.get("REC"):
        transport.record()  # record
        ui.setHintMsg("Record")

    elif event.data1 == buttons.button_list.get("STOP"):
        transport.stop()  # stop
        ui.setHintMsg("Stop")

    elif event.data1 == buttons.button_list.get("LOOP"):
        transport.setLoopMode()  # loop/pattern mode
        ui.setHintMsg("Song / pattern mode")
        if transport.getLoopMode() == off:
            set_track_info(0, "Pattern:", "Enabled")
        elif transport.getLoopMode() == on:
            set_track_info(0, "Song:", "Enabled")

    elif event.data1 == buttons.button_list.get("METRO"):
        transport.globalTransport(midi.FPT_Metronome, 110)
        ui.setHintMsg("Metronome")
        handle_metronome_enabled()

    elif event.data1 == buttons.button_list.get("TEMPO"):
        transport.stop()  # tap tempo

    elif event.data1 == buttons.button_list.get("QUANTIZE"):
        channels.quickQuantize(channels.channelNumber(), 0)
        ui.setHintMsg("Quick Quantize")
        set_track_info(0, "Piano Roll", "Quick Quantize")

    elif event.data1 == buttons.button_list.get("COUNT_IN"):
        transport.globalTransport(midi.FPT_CountDown, 115)  # countdown before recording
        ui.setHintMsg("Countdown before recording")
        handle_precount_enabled()

    elif event.data1 == buttons.button_list.get("CLEAR"):
        double_click_status = device.isDoubleClick(buttons.button_list.get("CLEAR"))
        if double_click_status:
            transport.globalTransport(midi.FPT_F12, 2, 15)
            ui.setHintMsg("Clear All Windows")
            set_track_info(0, "Clear All")
        else:
            ui.escape()  # escape key
            ui.setHintMsg("Close")

    elif event.data1 == buttons.button_list.get("UNDO"):
        undo_level = str(general.getUndoHistoryCount() - general.getUndoHistoryLast())
        general.undoUp()  # undo
        ui.setHintMsg(ui.getHintMsg())
        set_track_info(0, "History", "Undo @ " + undo_level)

    elif event.data1 == buttons.button_list.get("REDO"):
        undo_level = str(general.getUndoHistoryCount() - general.getUndoHistoryLast())
        general.undo()  # redo
        ui.setHintMsg(ui.getHintMsg())
        set_track_info(0, "History", "Redo @ " + undo_level)

    elif event.data1 == buttons.button_list.get("TEMPO"):
        transport.globalTransport(midi.FPT_TapTempo, 106)  # tap tempo

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
            set_track_info(0, "Main Snap", snap_mode_name)
            time.sleep(constants.timedelay)

    if event.data1 == buttons.button_list.get("ENCODER_BUTTON_SHIFTED"):
        event.handled = True

        doubleclickstatus = device.isDoubleClick(buttons.button_list.get("ENCODER_BUTTON_SHIFTED"))

        window_mappings = {
            0: (1, "Channel Rack"),
            1: (0, "Mixer"),
            2: (2, "Playlist"),
            3: (4, "Browser")
        }

        if doubleclickstatus:
            windowCycle = (windowCycle - 1) % 4
            transport.globalTransport(midi.FPT_F8, 67)
            ui.setHintMsg("Plugin Picker")
        else:
            window, hint_msg = window_mappings[windowCycle]
            ui.showWindow(window)
            windowCycle = (windowCycle + 1) % 4
            ui.setHintMsg(hint_msg)
            if " M " in device.getName():
                time.sleep(constants.timedelay)

    button_id = event.data1
    is_mute_button = button_id == buttons.button_list["MUTE_SELECTED"]
    is_solo_button = button_id == buttons.button_list["SOLO_SELECTED"]

    if is_mute_button or is_solo_button:
        focused_index = 0 if ui.getFocused(0) else 1
        event.handled = True

        if focused_index == 0:
            if mixer.getTrackName(mixer.trackNumber()) == "Current" and mixer.trackNumber() >= constants.currentUtility:
                pass
            else:
                mixer_function = mixer.enableTrack if is_mute_button else mixer.soloTrack
                mixer_function(mixer.trackNumber())
                ui.setHintMsg("Mute" if is_mute_button else "Solo")
        elif focused_index == 1:
            channel_function = channels.muteChannel if is_mute_button else channels.soloChannel
            channel_function(channels.channelNumber())
            ui.setHintMsg("Mute" if is_mute_button else "Solo")

    if ui.getFocused(constants.winName["Mixer"]):
        button_id = event.data1

        # s-series mixer actions
        for x in range(8):
            target_track = mixer.trackNumber() + x
            if button_id == buttons.button_list["MUTE"] and event.data2 == x:
                handle_mixer_action(event, mixer.enableTrack, target_track, "Mute")
            elif button_id == buttons.button_list["SOLO"] and event.data2 == x:
                handle_mixer_action(event, mixer.soloTrack, target_track, "Solo")
            elif button_id == constants.select and event.data2 == x:
                handle_mixer_action(event, mixer.armTrack, target_track, "Armed Disk Recording")

    win_channel_rack = ui.getFocused(constants.winName["Channel Rack"])

    if win_channel_rack:
        button_list = buttons.button_list
        channel_count = channels.channelCount()
        selected_channel = channels.selectedChannel()

        for x in range(8):
            if channel_count > x and selected_channel < (channel_count - x):
                if event.data1 == button_list.get("MUTE") and event.data2 == x:
                    event.handled = True
                    channels.muteChannel(selected_channel + x)
                    ui.setHintMsg("Mute")

                if event.data1 == button_list.get("SOLO") and event.data2 == x and not (
                        channels.isChannelMuted(selected_channel + x) and channel_count == 1):
                    event.handled = True
                    channels.soloChannel(selected_channel + x)
                    ui.setHintMsg("Solo")

                if event.data1 == constants.select and event.data2 == x:
                    event.handled = True
                    channels.selectOneChannel(selected_channel + x)
                    ui.setHintMsg("Track selected")

    win_playlist = ui.getFocused(constants.winName["Playlist"])

    if win_playlist:
        for x in range(8):
            if event.data1 == constants.select and event.data2 == x:
                event.handled = True
                playlist.selectTrack()
                ui.setHintMsg("")
                break  # Exit the loop since the track has been selected
