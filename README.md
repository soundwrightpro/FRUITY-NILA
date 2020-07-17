# Komplete Kontrol DAW - FL Studio Script - v4.2.5

#### Written by Duwayne 'Sound' Wright

Providing support for the Native Instruments Komplete Kontrol M32 and the A-Series. Uses the NI Host Integration protocol instead of the limited MIDI Mode NI provides, so the controller acts like as if it was connected to Ableton or Logic Pro X. The Komplete Kontrol App and/or Plugin does not have to be running for this script to function. This script doesn't interfere with the operation of the Komplete Kontrol Plugin. **You must have FL Studio 20.7.1 or higher, Komplete Kontrol v2.3.0, and Firmware 0.3.9 for the A-Series or 0.4.4 for the M32 installed**. 

### Have a question? Want to be a beta tester for S-Series development? Have a request? Want to say hi? [Join us on Discord!](https://discord.gg/GeTTWBV "FL Studio NI on Discord")


#### What's new since v3.5.5
* install method
* first stable version - all known bugs that result in a crash have been removed
* Modulation touch strip values now appears in hint bar.
* Display channel rack selection in red rectangle when selcted track moves, so you always know what the knobs control (Only works in ALL group)
* as you browse through the **Browser** file names are displayed on the OLED

##### Key Features
* full transport controls - **PLAY** with tempo flashing feedback, **Restart**, **REC** (when engaged with tempo flashing feedback), **Count-In** - toggles countdown before recording, and **STOP**; all with button light feedback
* **UNDO/Redo** right from the controller, **LOOP** toggles between pattern and song mode, **METRO** toggles the metronome off or on, and you can tap out the tempo with **TEMPO** 
* **QUANTIZE** turns off snap, while **Auto** cycles through global snap options
* **Clear** asks like the **"esc"** button on your keyboard
* **Mute** and **Solo** tracks on both the Mixer and Channel Rack

* **4-directional push encoder** - up, down, left, right and push for enter/accept (works on channel rack, mixer, browser and others)
* **Knobs** All 8 knobs control volume in channel rack or mixer, depending on what windows is active
* **Knobs + shift** controls pan in channel rack or mixer, depending on what windows is active

* full functioning OLED Screen that provides feedback to buttons and some features in FL Studio including volume, pan, track name, quantization status, and more

* Scroll through FLEX settings with the 4-D controller (up, down, left, right; click on the list in FLEX then use controls) & Plugin Picker. Envoke the plugin picker by pressing 
  Shift+Enter on 4D encoder.

* interact with something on the keyboard, it displays what it is in the hint bar on FL Studio
* don't know what a button does? Press it and look at the hint bar. Spells it all out for you.

* Integrated the [NI Host Integration Agent API for FL Studio](https://github.com/hobyst/flmidi-nihia  "NIHIA by Hobyst") by [Hobyst](https://github.com/hobyst  "Hobyst Github") for the best possible experience and stablity.

* #### Easily switch betwen NIHIA mode, Komplete Kontrol Plugin Mode and Midi Mode

  if the Komplete Control Plugin (not to be confused with the Application) is active, to switch between modes do the following:
  * press **TRACK Instance** and that returns all knobs to FL Studio
  * if FL Studio is active (you can tell if **Scale** & **Arp** buttons are not lit) press in this order, 
    **Instance (Shift+Track)**, **PLUG-IN MIDI**. Knob function has now returned to the Komplete Kontrol Plugin.
  * if you want to assign the eight knobs yourself, go to **MIDI Mode**. To do this hold shift and press **MIDI**. Assign the knobs as you wish. You have four pages of knobs to do so. To return to full control mode, Press **TRACK**

##### Limitations
* **scale, arp** buttons are exclusive to the Komplete Kontrol and the **ideas** button is exclusive to Machine. 
* **quantize** button goes between off (snap off) and on (snap on) instead of dim and bright when in use.
* **mixer** pan and volume control only works if the group is set to **"ALL"**

##### Awaiting fix from Image-Line Developers
* Active window on OLED can't go from **Mixer** to **Playlist**, then **Channel Rack** and vice versa.
* 4D plugin picker inserts odd characters in the search field on macOS



### Installation 

Native Instruments Host Integration service must be installed and running. It is automatically the case
if you installed Komplete Kontrol on your machine.

1. Download **the zip** and unzip. Place the 'Native Instruments' to the FL Studio User data 
folder under the following location:

   ```... Documents\Image-Line\FL Studio\Settings\Hardware\```  

2. In FL Studio 20.7.1 or higher under the MIDI tab in settings set Komplete Kontrol M DAW as **Komplete Kontrol DAW** in Input, for your M32 or A-Series and then set Kompolete Kontrol M32 or A-Series to **Komplete Kontrol MIDI**. Set Port to 1. Above in Output select "Send Master Sync" once again set Port to 1. Watch gif for clarification.

![Installlation gif](/images/install.gif)


My thanks to [Hobyst](https://github.com/hobyst) for their documentation, programs, and coding help. Also my thanks to the developers over at Image-Line for making MIDI scripting available & answering all of my questions.

### **DEVELOPMENT OF THIS SCRIPT TAKES PLACE ON A M32**


