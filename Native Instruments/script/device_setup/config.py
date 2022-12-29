"""
Start of User-editable Python file to change script behavior
"""

# Behavior of Browser Jog Wheel 
# 
# If set to 0, will turn off sounds playing while you jog(spinning the right most knob)
# If set to 1, will turn on the sounds while you jog 

jog_preview_sound = 0

# Behavior of Browser Jog Wheel 
# 
# If set to 0, will turn off sounds playing while you jog(spinning the right most knob)
# If set to 1, will turn on the sounds while you jog 

upDown_preview_sound = 1


"""
End of User-editable Python file to change script behavior
"""






















































# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# script_constants

VERSION_NUMBER = "v10.0.0"
HELLO_MESSAGE = "FRUITY NILA"
GOODBYE_MESSAGE = "by: Duwayne"
OUTPUT_MESSAGE = "\nFRUITY NILA " + VERSION_NUMBER + "\nCopyright © 2022 Duwayne\n"
LOAD_MESSAGE = "Project Loaded"


supported_plugins = ['FL Keys','FLEX','Sytrus','GMS','Harmless','Harmor',
                    'Morphine', '3x Osc', 'Fruity DX10', 'BassDrum',
                    'MiniSynth', 'PoiZone', 'Sakura']

widTitle = ["Mixer", "Channel Rack", "Playlist", "Piano Roll",
            "Browser", "Plugin Window", "Effect Plugin", "Generator Plugin"]

winName = {
    "Mixer": 0,
    "Channel Rack": 1,
    "Playlist": 2,
    "Piano Roll": 3,
    "Browser": 4,
    "Plugin": 5
}

MAX_Major = 21
MAX_Minor = 0
MAX_Release = 0

MIN_Major = 21
MIN_Minor = 0
MIN_Release = 0


timedelay = 0.45

increment = 0.01

wait_input_1 = "Waiting"
wait_input_2 = "for input...     "

currentUtility = 126

blankEvent = "   "
nuText = "Not Used"

itemDisp = 0
itemTime = 0

#fl constants

PL_Start = 0 #Called when project loading start
PL_LoadOk = 100	#Called when project was succesfully loaded
PL_LoadError = 101 #Called when project loading stopped because of error