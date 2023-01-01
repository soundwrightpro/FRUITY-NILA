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

VERSION_NUMBER = "v10.0.1"
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

off = 0
on = 1

MIDI_Script_Version = 23

timedelay = 0.35

increment = 0.01

controls = 15

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

SBN_FLP = 1	            #FL studio project
SBN_ZIP = 2	            #Zipped archive
SBN_FLM	= 3	            #FL studio project
SBN_FST	= 4	            #FL Studio state preset
SBN_DS	= 5	            #Ds file
SBN_SS	= 6	            #SS file
SBN_WAV	= 7	            #Wav file
SBN_XI	= 8	            #XI file
SBN_FPR	= 9	            #Fpr file
SBN_FSC	= 10	        #FSC file
SBN_SF2	= 11	        #SF2 file
SBN_Speech = 12	        #Speech file
SBN_MP3	= 13	        #MP3 file
SBN_OGG	= 14	        #Ogg file
SBN_FLAC = 15	        #Flac file
SBN_OSM	= 16	        #OSM file
SBN_REX	= 17	        #REX file
SBN_DWP	= 18	        #DirectWave preset
SBN_FNV	= 19	        #FNV file
SBN_FXB	= 20	        #FXB file
SBN_AIFF = 21	        #AIFF file
SBN_TXT	= 22	        #Text file
SBN_BMP	= 23	        #Image
SBN_WV	= 24	        #WV file
SBN_TS	= 25	        #TS file
SBN_RBS	= 26	        #RBS file
SBN_MID	= 27	        #Midi file
SBN_FLEXPack = 28	    #Flex pack
SBN_NEWS = 29	        #News item
SBN_SHOP = 30           #Shop item(unused)
SBN_LIB = 31	        #Library item
SBN_LIBOWNED = 32	    #Library item(owned)
SBN_NOTIFICATION = 33	#Notification item
SBN_DOWNLOAD = 34	    #Download item
SBN_M4A	= 35	        #M4A file