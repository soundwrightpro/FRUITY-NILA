# FL NI KK v6.0.1 for FL Studio 20.8.2 and higher

#### Written by Duwayne 'Sound' Wright

Providing support for the Native Instruments Komplete Kontrol M32 and the A-Series. Uses the NI Host Integration protocol instead of the limited MIDI Mode NI provides, so the controller acts like as if it was connected to Ableton or Logic Pro X. The Komplete Kontrol App and/or Plugin does not have to be running for this script to function. This script doesn't interfere with the operation of the Komplete Kontrol Plugin. **You must have FL Studio 20.7.1 or higher, Komplete Kontrol v2.3.0, and Firmware 0.3.9 or higher for the A-Series or 0.4.4 or higher for the M32 installed**. 

### Have a question? Want to be a beta tester for S-Series developement? Have a request? Want to say hi? [Join us on Discord!](https://discord.gg/GeTTWBV "FL Studio NI on Discord")

#### What's New since v5.1.0
* dropped older version support. 20.8.2 and higher only!
* Go through presets on the channel rack when a plugin is selected (only for plugins that support selecting presets from FL Studio, not through plugins internal structure)
* speed improvements through multi-threading processing
* switch between multiple instances of Komplete Kontrol Plugin by pressing shift+instance, then scroll through instances with 4D
* mute & solo buttons light up with active in Channel Rack or Mixer
* bug fixes

##### Key Features
* **transport** play, record, stop control
* **count-in** - toggles countdown before recording
* **restart** (**shift + play**)
* **loop** - toggles between pattern and song mode
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
* if the Komplete Control Plugin (not to be confused with the Application) is active, to switch between modes do the following (or vice versa):
  * press **TRACK Instance** and that returns all knobs to FL Studio
  * if FL Studio is active (you can tell if **Scale** & **Arp** buttons are not lit) press in this order, 
    **Instance (Shift+Track)**, **PLUG-IN MIDI**. Knob function has now returned to the Komplete Kontrol Plugin.
  * if you want to assign the eight knobs yourself, go to **MIDI Mode**. To do this hold shift and press **MIDI**. Assign the knobs as you wish. You have four pages of knobs to do so. To return to full control mode, Press **TRACK**
* OLED - shows what module window is open with  **Playlist**, **Piano Roll**, **Browser**, **Channel Rack**
* OLED - **Mute** & **Solo** light up for Channel Rack 
* pushing down on 4D encoder is enter, useful for plugins like Flex when you want to choose a new sound after scrolling       through using 4D encoder
* shift + pushing down on 4D encoder toggles between open windows.
* **clear** (**shift + stop**) functions as the escape key
* **channel and mixer track names** on the OLED. For the Mixer all track names start with "M: " and for the Channel Rack all track names start with "C: ". Tap on a knob to see the name of what it controls.
* Scroll through FLEX settings with the 4-D controller (up, down, left, right; click on the list in FLEX then use controls)
* **play** button flashes to tempo, **record** button flashes to tempo when recording is engaged and **play** button light is engaged 
* **volume** and **pan** values are displayed on the OLED. Tap on a knob to see the value of the track it's controlling.
* interact with something on the keyboard, it displays what it is in the hint bar 
* don't know what a button does? Press it and look at the hint bar. Spells it all out for you.
* **volume** displayed in dB on the OLED (my thanks to Image-Line for the assist)
* **Piano Roll** shown as "PR: " with track name and **Browser** when selected show on OLED
* consolidated into one file for easier updates
* status messages on OLED when corresponding buttons are pushed, eg. **auto** (shift + auto) now shows the snap setting on the OLED
* **shift + 4D knob** activates the plugin picker, use the 4D knob directions (left, right, up, down) to choose the plugin you want to load (macOS, see known issues)
* improvements with track names on OLED
* **shift + 4D button** - switching between mixer, browser, channel rack, playlist and piano roll (when visable) 
* **shift + 4D button** double press opens plugin picker
* when the mixer is the active window
  * able to see what the 8 knobs are linked to when you move the 4D jog wheel
* when playlist is the active window
  * can add auto markers in playlist (double click to add, double click again at same point to remove)
  * time/seconds or beats/bars on OLED when playlist is selected (depending on what you have active in FL Studio)
  * jumping between markers in playlist (left and right on 4d)
* when broswer is the active window
  * double press 4D button when plugin or sound is selected. Right click menu will open.
* when the channel rack is the active window
  * navigating between groups on the channel rack (double click to open menu)



##### Known Issues
* **scale, arp** buttons are exclusive to the Komplete Kontrol and the **ideas** button is exclusive to Machine. 
* **quantize** button goes between off(snap off) and on (snap on) instead of dim and bright when in use. - todo
* Active window on OLED can't go from **Mixer** to **Playlist**, then **Channel Rack** and vice versa.  - Something is wrong with FL Studio, Image-Line is aware of the problem. Awaiting fix
* tempo light flashing while playing with PLAY and REC button sometimes becomes out of sync.
* script slows down when machine is taxed. Currently working on threading/multitreading to overcome this issue.
* **Mute** and **Solo** buttons do not light up when shift isn't pushed. Can't get access to those buttons as NI doesn't allow it.



##### Installation

Native Instruments Host Integration service must be installed and running. It is automatically the case
if you installed Komplete Kontrol on your machine.

1. Download **the zip** and unzip. Place the 'Native Instruments' to the FL Studio User data 
folder under the following location:

   ```... Documents\Image-Line\FL Studio\Settings\Hardware\```  

2. In FL Studio 20.7.1 or higher under the MIDI tab in settings set Komplete Kontrol M DAW as Komplete Kontrol DAW in Input, for your M32 or A-Series. Set Port to 1. Above in Output select "Send Master Sync" once again set Port to 1. See image for clarification.


![Installlation GIF](/images/install.gif)

Enjoy

My thanks to [Hobyst](https://github.com/hobyst) for their documentation, programs, and coding help and my thanks to the developers over at Image-Line for making MIDI scripting available & answering all of my questions.

**DEVELOPMENT OF THIS SCRIPT TAKES PLACE ON A M32**


