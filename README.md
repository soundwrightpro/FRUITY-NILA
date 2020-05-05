# Native Instruments Komplete Kontrol M32 V2.9.4
Written by Duwayne 'Sound' Wright

Providing support for Native Instruments Komplete Kontrol M32. Uses the NI Host Integration protocol instead of the limited MIDI Mode NI provides, so the controller acts like as if it was connected to Ableton or Logic Pro X. **You must have must have  Komplete Kontrol v2.3.0 and Firmware 0.4.4 installed**.

# What's new in 2.9.4
* bug fixes

## Key Features
* **transport** works as expected (play, record, stop)
* **count-in** - toggles countdown before recording
* **loop** - toggles between pattern and loop mode
* **metro** - toggles metro off and on
* **tempo** - tap to set tempo
* **undo/redo** - works as expected, hold shift to redo
* **four-directional push encoder** - up, down, left, right and push for enter/accept (works on channel rack, mixer, browser and others)
* **play** flashes in sync with the tempo of the project
* **play**, **rec**, **stop**, **loop**, **metro** light up when engaged from FL Studio or controller
* **quantize** turns off snap, auto (**shift + quantize**) cycles through global snap options
* **knobs** All 8 knobs controls volume in channel rack or mixer, depending on what windows is active
* **knobs + shift** controls pan in channel rack or mixer, depending on what windows is active
* **mute and solo** buttons work on selected track in channel rack or mixer when shift is held down, depending on what windows is active
* **quantize** light turns off when snap status is none.
* if the Komplete Control Plugin is active, to switch between modes do the following:
  * press **TRACK Instance** and that returns all knobs to FL Studio
  * if FL Studio is active (you can tell if **Scale** & **Arp** buttons are not lit) press in this order, 
    **Instance (Shift+Track)**, **PLUG-IN MIDI**. Knob function has now returned to the Komplete Kontrol Plugin.

## Known Issues
* **clear** (**shift + stop**) closes all window has a bug when plugins are openned. temp disabled - todo
* OLED doesn't change status at all - todo
* **quantize** button goes between off(snap off) and on (snap on) instead of dim and bright when in use. - todo


## Installation

Native Instruments Host Integration service must be installed and running. It is automatically the case
if you installed Komplete Kontrol on your machine.

1. Download **device_Native_Instruments_KOMPLETE_KONTROL_M32.py** and place int to the FL Studio User data 
folder under the following location:

... Documents\Image-Line\FL Studio\Settings\Hardware\Native Instruments

Create a **'Native Instruments' folder if one doesn't exist.**

2. In FL Studio 20.7 or higher under the MIDI tab in settings set Komplete Kontrol M DAW as Native Instruments Komplete Kontrol M32 (User).

Enjoy

My thanks to Hobyst and their documentation and coding help. You have been the GOAT!

Did you make it all the way to the bottom? Good work. I'll share my road map with you.

* 2.9.9 - will have the LED screen working - major progress has been made in this area.
* 3.0.0 - will be full-featured
* 3.5.0 - bugs and refinements - I'm new to python, so I'm learning as I go. There are so many techniques I've learned that           I need to apply to older things I've done.
* 4.0.0 - Final - There's only so much I can do. If you have any suggestions leave them here in the FL Studio forum:                   https://forum.image-line.com/viewtopic.php?f=1994&t=225473


