# Native Instruments Komplete Kontrol FL Studio Script for M32 & A-Series V3.0.6

Written by Duwayne 'Sound' Wright

Providing support for the Native Instruments Komplete Kontrol M32 and the A-Series. Uses the NI Host Integration protocol instead of the limited MIDI Mode NI provides, so the controller acts like as if it was connected to Ableton or Logic Pro X. **You must have Komplete Kontrol v2.3.0 and Firmware 0.3.9 for the A-Series or 0.4.4 for the M32 installed**. 


# What's new since 2.9.9
* A-Series support
* **play** button flashes to tempo, **record** button flashes to tempo when recording is engaged and **play** button light is engaged 
* **volume** and **pan** values are displayed on the OLED. Tap on a knob to see the value of the track it's controlling.
* interact with something on the keyboard, it displays what it is in the hint bar 
* don't know what a button does? Press it and look at the hint bar. Spells it all out for you.
* bug fixes (undo light)

## Key Features
* **transport** works as expected (play, record, stop)
* **count-in** - toggles countdown before recording
* **loop** - toggles between pattern and loop mode
* **metro** - toggles metro off and on
* **tempo** - tap to set tempo
* **undo/redo** - works as expected, hold shift to redo
* **four-directional push encoder** - up, down, left, right and push for enter/accept (works on channel rack, mixer, browser and others)
* **play**, **rec**, **stop**, **loop**, **metro** light up when engaged from FL Studio or controller
* **quantize** turns off snap, auto (**shift + quantize**) cycles through global snap options
* **knobs** All 8 knobs control volume in channel rack or mixer, depending on what windows is active
* **knobs + shift** controls pan in channel rack or mixer, depending on what windows is active
* **mute and solo** buttons work on selected track in channel rack or mixer when shift is held down, depending on what windows is active
* **quantize** light turns off when snap status is none.
* if the Komplete Control Plugin is active, to switch between modes do the following:
  * press **TRACK Instance** and that returns all knobs to FL Studio
  * if FL Studio is active (you can tell if **Scale** & **Arp** buttons are not lit) press in this order, 
    **Instance (Shift+Track)**, **PLUG-IN MIDI**. Knob function has now returned to the Komplete Kontrol Plugin.
  * if you want to assign the eight knobs yourself, go to **MIDI Mode**. To do this hold shift and press **MIDI**. Assign the knobs as you wish. You have four pages of knobs to do so. To return to full control mode, Press **TRACK**
* OLED - shows what module window is open with  **Playlist**, **Piano Roll**, **Browser**, **Channel Rack**
* OLED - **Mute** & **Solo** light up for Channel Rack 
* pushing down on 4D encoder is enter, useful for plugins like Flex when you want to choose a new sound after scrolling       through using 4D encoder
* shift + pushing down on 4D encoder toggles between open windows.
* **clear** (**shift + stop**) functions as the escape key
* **restart** (**shift + play**) save!
* **channel and mixer track names** on the OLED. For the Mixer all track names start with "M: " and for the Channel Rack all track names start with "C: ". Tap on a knob to see the name of what it controls.

## Known Issues
* **clear** (**shift + stop**) closes all windows has a bug when plugins are opened. temp disabled - todo
* **quantize** button goes between off(snap off) and on (snap on) instead of dim and bright when in use. - todo
* **volume** dB displayed on OLED screen isn't correct - switched to % scale for the time being 
* **mute** and **solo** can be engaged at the same time - todo
* Active window on OLED can't go from **Mixer** to **Playlist**, then **Channel Rack** and vice versa. Something is wrong with FL Studio, Image-Line is aware of the problem. - awaiting fix
* When a track/channel name is longer than 8 characters on the mixer/channel, an automatic shortening is applied to the name. The colon and/or space for "M:" or "C:" may disappear. This is unavoidable.
* **channel rack** doesn't update volume or pan in real-time. Something is wrong with FL Studio, Image-Line is aware of the problem. - awaiting fix


## Installation

Native Instruments Host Integration service must be installed and running. It is automatically the case
if you installed Komplete Kontrol on your machine.

1. Download **the zip** and unzip. Place the 'Native Instruments' to the FL Studio User data 
folder under the following location:

... Documents\Image-Line\FL Studio\Settings\Hardware\

2. In FL Studio 20.7 or higher under the MIDI tab in settings set Komplete Kontrol M DAW as Native Instruments Komplete Kontrol M32 (User) or Native Instruments Komplete Kontrol A-Series (User) in Input, depending on what you own. Set Port to 1. Above in Output select "Send Master Sync" once again set Port to 1. See image for clarification.

![Installlation image](/images/FL%20Studio%20Install.png)

Enjoy

My thanks to Hobyst and their documentation and coding help. You have been the GOAT! 

**DEVELOPEMNT OF THIS SCRIPT TAKES PLACE ON A M32**

Did you make it all the way to the bottom? Good work. I'll share my road map with you.

* 3.5.0 - bugs and refinements - I'm new to python, so I'm learning as I go. There are so many techniques I've learned that           I need to apply to the older things I've done.
* 4.0.0 - Final - There's only so much I can do. If you have any suggestions leave them here in the FL Studio forum:                   https://forum.image-line.com/viewtopic.php?f=1994&t=225473
