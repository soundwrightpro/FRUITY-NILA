"""Midi Module (included in FL Studio Python lib folder)

Contains useful constants for working with MIDI events, and with FL Studio API
flags.

NOTE: This code is taken from FL Studio's Python lib folder and included in this
package in the hope that it will be useful for script developers. It is not the
creation of the repository authors, and no credit is claimed.
"""

MaxInt = 2147483647

# midi codes
MIDI_NOTEON = 0x90
MIDI_NOTEOFF = 0x80
MIDI_KEYAFTERTOUCH = 0xA0
MIDI_CONTROLCHANGE = 0xB0
MIDI_PROGRAMCHANGE = 0xC0
MIDI_CHANAFTERTOUCH = 0xD0
MIDI_PITCHBEND = 0xE0
MIDI_SYSTEMMESSAGE = 0xF0
MIDI_BEGINSYSEX = 0xF0
MIDI_MTCQUARTERFRAME = 0xF1
MIDI_SONGPOSPTR = 0xF2
MIDI_SONGSELECT = 0xF3
MIDI_ENDSYSEX = 0xF7
MIDI_TIMINGCLOCK = 0xF8
MIDI_START = 0xFA
MIDI_CONTINUE = 0xFB
MIDI_STOP = 0xFC
MIDI_ACTIVESENSING = 0xFE
MIDI_SYSTEMRESET = 0xFF

# processMIDIEvent flags
PME_LiveInput = 1
PME_System = 1 << 1
PME_System_Safe = 1 << 2
PME_PreviewNote = 1 << 3
PME_FromHost = 1 << 4
PME_FromMIDI = 1 << 5
PME_FromScript = 1 << 6

# playlist.triggerLiveClip flags
TLC_MuteOthers = 1
TLC_Fill = 1 << 1
TLC_Queue = 1 << 2
TLC_Release = 1 << 5
TLC_NoPlayCheck = 1 << 6
TLC_NoHardwareUpdate = 1 << 30
TLC_SecondPass = 1 << 31 # system

TLC_ColumnMode = 1 << 7 # scene
TLC_WeakColumnMode = 1 << 8 # +scene
TLC_TriggerCheckColumnMode = 1 << 9 # same press mode

TLC_TrackSnap = 0 << 3
TLC_GlobalSnap = 1 << 3
TLC_NoSnap = 2 << 3

TLC_SubNum_Normal = 0 << 16
TLC_SubNum_ClipPos = 1 << 16
TLC_SubNum_GroupNum = 2 << 16
TLC_SubNum_Read = 3 << 16
TLC_SubNum_Leave = 4 << 16

# playing modes
PM_Stopped = 0
PM_Playing = 1
PM_Precount = 2

# hardware dirty flags
HW_Dirty_Mixer_Sel = 1
HW_Dirty_Mixer_Display = 2
HW_Dirty_Mixer_Controls = 4
HW_Dirty_RemoteLinks = 16 # links have changed
HW_Dirty_FocusedWindow = 32 # needed for controllers that reflect generic links
HW_Dirty_Performance = 64 # performance layout (not playing state!) has changed
HW_Dirty_LEDs = 256
HW_Dirty_RemoteLinkValues = 512

#song time flags
SONGLENGTH_MS = 0
SONGLENGTH_S = 1
SONGLENGTH_ABSTICKS = 2
SONGLENGTH_BARS = 3
SONGLENGTH_STEPS = 4
SONGLENGTH_TICKS = 5

#TEventIDInfo
Event_CantInterpolate = 0x00
Event_Float = 0x02
Event_Centered = 0x04

#rec events
REC_ItemRange = 0x10000
REC_TrackRange = 0x10
REC_EnvRange = 0x100
REC_PluginBase = 0x8000
REC_PluginRange = 0x8000
REC_ItemMask = 0xFFFF

REC_MaxChan = 0x1000
REC_MaxPat = 0x1000
REC_GlobalChan = REC_MaxChan - 1

REC_GlobalPlugTrack = 128 - 1
REC_GlobalPlug = (0x2000 >> 6) + REC_GlobalPlugTrack
REC_MixerMask = 0x3FFFFF

# event ID's     channels (up to 4096)
REC_Chan_First = 0
REC_Chan_Last = REC_MaxChan * REC_ItemRange - 1
REC_Chan_Vol = REC_Chan_First
REC_Chan_Pan = REC_Chan_First + 1
REC_Chan_FCut = REC_Chan_First + 2
REC_Chan_FRes = REC_Chan_First + 3
REC_Chan_Pitch = REC_Chan_First + 4
REC_Chan_FType = REC_Chan_First + 5
REC_Chan_PortaTime = REC_Chan_First + 6
REC_Chan_Mute = REC_Chan_First + 7
REC_Chan_FXTrack = REC_Chan_First + 8
REC_Chan_GateTime = REC_Chan_First + 9
REC_Chan_Crossfade = REC_Chan_First + 10
REC_Chan_TimeOfs = REC_Chan_First + 11
REC_Chan_SwingMix = REC_Chan_First + 12
REC_Chan_SmpOfs = REC_Chan_First + 13
REC_Chan_StretchTime = REC_Chan_First + 14

REC_Chan_OfsPan = REC_Chan_First + 16
REC_Chan_OfsVol = REC_Chan_First + 17
REC_Chan_OfsPitch = REC_Chan_First + 18
REC_Chan_OfsFCut = REC_Chan_First + 19
REC_Chan_OfsFRes = REC_Chan_First + 20

# TS404
REC_Chan_TS404_First = REC_Chan_First + 0x100 # same order as the 404 params
REC_Chan_TS404_FCut = REC_Chan_TS404_First + 18
REC_Chan_TS404_FRes = REC_Chan_TS404_First + 19
REC_Chan_TS404_Env_First = REC_Chan_TS404_First + 31
REC_Chan_TS404_Env_Last = REC_Chan_TS404_Env_First + 4
REC_Chan_TS404_Last = REC_Chan_TS404_First + 0x100 - 1
REC_Chan_TS404_Valid_First = 259
REC_Chan_TS404_Valid_Last = 293

# delay
REC_Chan_Delay_First = REC_Chan_First + 0x200
REC_Chan_Delay_Last = REC_Chan_Delay_First + 0x100 - 1
REC_Chan_Delay_Time = REC_Chan_Delay_First + 4

# arpeggiator
REC_Chan_Arp_First = REC_Chan_First + 0x300
REC_Chan_Arp_Last = REC_Chan_Arp_First + 0x100 - 1
REC_Chan_Arp_Chord = REC_Chan_Arp_First + 2
REC_Chan_Arp_Time = REC_Chan_Arp_First + 3
REC_Chan_Arp_Gate = REC_Chan_Arp_First + 4
REC_Chan_Arp_Repeat = REC_Chan_Arp_First + 5

# misc
REC_Chan_Misc = REC_Chan_First + 0x400

# tracking
REC_Chan_Track_First = REC_Chan_First + 0x500
REC_Chan_Track_PLast = REC_Chan_Track_First + 2
REC_Chan_Track_Last = REC_Chan_Track_First + 0x100 - 1

# automation articulator
REC_Chan_AC_First = REC_Chan_First + 0x600
REC_Chan_AC_Last = REC_Chan_AC_First + 0x100 - 1

# envelope
REC_Chan_Env_First = REC_Chan_First + 0x1000
REC_Chan_Env_LFO_First = REC_Chan_Env_First + 9
REC_Chan_Env_MA = REC_Chan_Env_First + 8
REC_Chan_Env_LFOA = REC_Chan_Env_First + 11
REC_Chan_Env_Hole = REC_Chan_Env_LFOA + 2
REC_Chan_Env_PLast = REC_Chan_Env_Hole + 3
REC_Chan_Env_Last = REC_Chan_Env_First + 0x800 - 1

# note events
REC_Chan_Note_First = REC_Chan_First + 0x4000
REC_Chan_Note_Num = 0x20
REC_Chan_Note_Last = REC_Chan_Note_First + REC_Chan_Note_Num

REC_Chan_NoteOn = REC_Chan_Note_First
REC_Chan_NoteMask = 0xFFFFFFF0
# slides
REC_Chan_NoteSlideMask = 8
REC_Chan_NoteSlide = REC_Chan_NoteOn + REC_Chan_NoteSlideMask
REC_Chan_NoteSlideTo = REC_Chan_NoteSlide
REC_Chan_NoteSlideOfs = REC_Chan_NoteSlide + 1
# misc
REC_Chan_NoteOff = REC_Chan_NoteOn + 0x20
REC_Chan_PianoRoll = REC_Chan_NoteOn

REC_Chan_Clip = REC_Chan_First + 0x5000

# linked plugin (>0x8000)
REC_Chan_Plugin_First = REC_Chan_First + REC_PluginBase
REC_Chan_Plugin_Last = REC_Chan_Plugin_First + REC_PluginRange - 1

# *** effect plugins (up to 128 mixer tracks*64 plugins)
# designed not to overlap with REC_Chan events, so that they can be merged later
REC_Plug_First = 0x2000 * REC_ItemRange
REC_Plug_Last = REC_Plug_First + 0x2000 * REC_ItemRange - 1

# plugin common properties (up to 256)
REC_Plug_General_First = REC_Plug_First + 0x2000 - 0x100
REC_Plug_General_Last = REC_Plug_General_First + 0x40 - 1
REC_Plug_Mute = REC_Plug_General_First # mute
REC_Plug_MixLevel = REC_Plug_General_First + 1 # mix level

# mixer track properties
REC_Mixer_First = REC_Plug_General_First + 0x40
REC_Mixer_Last = REC_Mixer_First + 0x800 - 1
REC_Mixer_Send_First = REC_Mixer_First # sends (up to 128)
REC_Mixer_Send_Last = REC_Mixer_Send_First + 0x80 - 1
REC_Mixer_Vol = REC_Mixer_Send_Last + 1 # volume
REC_Mixer_Pan = REC_Mixer_Vol + 1 # pan
REC_Mixer_SS = REC_Mixer_Vol + 2 # stereo separation

# EQ (up to 8 bands)
REC_Mixer_EQ_First = REC_Mixer_Vol + 0x10
REC_Mixer_EQ_Last = REC_Mixer_EQ_First + 8 * 3 - 1
REC_Mixer_EQ_Gain = REC_Mixer_EQ_First
REC_Mixer_EQ_Freq = REC_Mixer_EQ_First + 8
REC_Mixer_EQ_Q = REC_Mixer_EQ_First + 8 * 2
REC_Mixer_EQ_Type = REC_Mixer_EQ_First + 8 * 3

# linked plugin (>0x8000)
REC_Plug_Plugin_First = REC_Plug_First + REC_PluginBase
REC_Plug_Plugin_Last = REC_Plug_Plugin_First + REC_PluginRange - 1

# global
REC_Global_First = 0x4000 * REC_ItemRange
REC_Global_Last = REC_Global_First + REC_ItemRange
REC_MainVol = REC_Global_First
REC_MainShuffle = REC_Global_First + 1
REC_MainPitch = REC_Global_First + 2
REC_MainFRes = REC_Global_First + 3 # obsolete
REC_MainFCut = REC_Global_First + 4 # obsolete
REC_Tempo = REC_Global_First + 5

REC_TS404Delay_First = REC_Global_First + 0x100 # obsolete
REC_TS404Delay_Feed = REC_TS404Delay_First
REC_TS404Delay_Pan = REC_TS404Delay_First + 1
REC_TS404Delay_Vol = REC_TS404Delay_First + 2
REC_TS404Delay_Time = REC_TS404Delay_First + 3

# playlist
REC_Playlist_First = 0x5000 * REC_ItemRange
REC_Playlist_Last = REC_Playlist_First + 0x2000 * REC_ItemRange - 1

# patterns (up to 4096)
REC_Pat_First = REC_Playlist_First
REC_Pat_Last = REC_Pat_First + 0x1000 * REC_ItemRange - 1
REC_Pat_Clip = REC_Pat_First + 0x5000 # clip item

# all clips
REC_PLClip_First = REC_Chan_First # this is not a typo, it includes channel and pattern clips
REC_PLClip_Last = REC_Pat_Last

# pattern instances at the top of the playlist
REC_Playlist_Old = REC_Playlist_First # obsolete
REC_Pat_Block = REC_Playlist_First + 0x1000 * REC_ItemRange # pattern block, but shouldn't happen anymore?
REC_Playlist = REC_Playlist_Old

# playlist tracks (up to 4096)
REC_PLTrack_First = 0x6000 * REC_ItemRange
REC_PLTrack_Last = REC_PLTrack_First + 0x1000 * REC_ItemRange - 1

# reserved for future use
REC_Reserved = 0x80000000

# special commands
# for remote control by external apps
REC_Special = -1
REC_StartStop = REC_Special # 0=Stop, 1=Start
REC_SongPosition = REC_Special - 1 # get/set song position (in bars)
REC_SongLength = REC_Special - 2 # get song length (in bars)
# last tweaked
REC_LastTweakedFirst = -32
REC_LastTweakedLast = REC_LastTweakedFirst + 1
# for the project browser
REC_Proj_First = REC_Special - 0x100

# process flags
REC_UpdateValue = 1 << 0
REC_GetValue = 1 << 1
REC_ShowHint = 1 << 2
REC_UpdatePlugLabel = 1 << 3
REC_UpdateControl = 1 << 4
REC_FromMIDI = 1 << 5
REC_Store = 1 << 6
REC_SetChanged = 1 << 7
REC_SetTouched = 1 << 8
REC_Init = 1 << 9
REC_NoLink = 1 << 10
REC_InternalCtrl = 1 << 11
REC_PlugReserved = 1 << 12
REC_Smoothed = 1 << 13
REC_NoLastTweaked = 1 << 14
REC_NoSaveUndo = 1 << 15

# combo's
REC_InitStore = REC_Init | REC_Store
REC_Control = REC_UpdateValue | REC_UpdateControl | REC_ShowHint | REC_InitStore | REC_SetChanged | REC_SetTouched # called by a control
REC_MIDIController = REC_Control | REC_FromMIDI # called by a MIDI controller from midi
REC_Controller = REC_Control #for compatibility only, wrong name used

REC_SetAll = REC_UpdateValue | REC_UpdateControl | REC_InitStore | REC_SetChanged | REC_SetTouched # called externally
REC_Control = REC_UpdateValue | REC_ShowHint | REC_InitStore | REC_SetChanged | REC_UpdatePlugLabel | REC_SetTouched # called by the param's control
REC_Visual = REC_GetValue | REC_UpdateControl | REC_UpdatePlugLabel # refresh visually
REC_FromMixThread = REC_UpdateValue # change the value only
REC_PlugCallback = REC_InitStore | REC_SetChanged | REC_SetTouched
REC_FromInternalCtrl = REC_UpdateValue | REC_FromMIDI | REC_InternalCtrl # let's not prevent automation & internal controllers at the same time
REC_AnyInternalCtrl = REC_InternalCtrl | REC_Smoothed

# ProcessRECEvent returns this when the ID is invalid
REC_InvalidID = MaxInt

# used when filtering events that have no ID's
REC_None = MaxInt

# Remote_FindEventID returns this when a generic link could be found, but it's not related to the focused window
REC_SomeGeneric = REC_None - 1

# Default mapping for the wrapper (to support mod wheel and aftertouch in VSTs)
REC_WrapperModWheel = 0x0FFF9001
REC_WrapperAfterTouch = 0x0FFF9080

# recording flags for ProcessMIDIEvent
PME_RECFlagsT = [REC_UpdateValue | REC_UpdateControl | REC_FromMIDI | REC_SetChanged | REC_SetTouched, REC_MIDIController]

# Global transport commnads
FPT_Jog = 0
FPT_Jog2 = 1
FPT_Strip = 2
FPT_StripJog = 3
FPT_StripHold = 4
FPT_Previous = 5
FPT_Next = 6
FPT_PreviousNext = 7
FPT_MoveJog = 8
FPT_Play = 10
FPT_Stop = 11
FPT_Record = 12
FPT_Rewind = 13
FPT_FastForward = 14
FPT_Loop = 15
FPT_Mute = 16
FPT_Mode = 17
FPT_Undo = 20
FPT_UndoUp = 21
FPT_UndoJog = 22
FPT_Punch = 30
FPT_PunchIn = 31
FPT_PunchOut = 32
FPT_AddMarker = 33
FPT_AddAltMarker = 34
FPT_MarkerJumpJog = 35
FPT_MarkerSelJog = 36

FPT_Up = 40
FPT_Down = 41
FPT_Left = 42
FPT_Right = 43
FPT_HZoomJog = 44
FPT_VZoomJog = 45
FPT_Snap = 48
FPT_SnapMode = 49

FPT_Cut = 50
FPT_Copy = 51
FPT_Paste = 52
FPT_Insert = 53
FPT_Delete = 54
FPT_NextWindow = 58
FPT_WindowJog = 59

FPT_F1 = 60
FPT_F2 = 61
FPT_F3 = 62
FPT_F4 = 63
FPT_F5 = 64
FPT_F6 = 65
FPT_F7 = 66
FPT_F8 = 67
FPT_F9 = 68
FPT_F10 = 69
FPT_F11 = 70
FPT_F12 = 71

FPT_Enter = 80
FPT_Escape = 81
FPT_Yes = 82
FPT_No = 83

FPT_Menu = 90
FPT_ItemMenu = 91
FPT_Save = 92
FPT_SaveNew = 93

FPT_PatternJog = 100
FPT_TrackJog = 101
FPT_ChannelJog = 102

FPT_TempoJog = 105
FPT_TapTempo = 106
FPT_NudgeMinus = 107
FPT_NudgePlus = 108

FPT_Metronome = 110
FPT_WaitForInput = 111
FPT_Overdub = 112
FPT_LoopRecord = 113
FPT_StepEdit = 114
FPT_CountDown = 115

FPT_NextMixerWindow = 120
FPT_MixerWindowJog = 121
FPT_ShuffleJog = 122

FPT_ArrangementJog = 123

# Global transport flags
GT_Cannot = -1
GT_None = 0
GT_Plugin = 1
GT_Form = 2
GT_Menu = 4
GT_Global = 8
GT_All = GT_Plugin | GT_Form | GT_Menu | GT_Global

#
TranzPort_OffOnT = [MIDI_NOTEON, MIDI_NOTEON + (0x7F << 16)]
TranzPort_OffBlinkT = [MIDI_NOTEON, MIDI_NOTEON + (1 << 16)]
TranzPort_OffOnBlinkT = [MIDI_NOTEON, MIDI_NOTEON + (0x7F << 16), MIDI_NOTEON + (1 << 16)]

FromMIDI_Max = 1073741824
FromMIDI_Half = FromMIDI_Max >> 1

# resolution of endless knobs is assumed to be 24 ticks per revolution
EKRes = 1 / 24



TrackNum_Master = 0

SM_Pat = 0
SM_Song = 1

# show ui 
widMixer = 0
widChannelRack = 1
widPlaylist = 2
widPianoRoll = 3
widBrowser = 4

curfxScrollToMakeVisible = 1
StartcurfxCancelSmoothing = 1 << 1
curfxNoDeselectAll = 1 << 2
curfxMinimalLatencyUpdate = 1 << 3

fxSoloModeWithSourceTracks = 1
fxSoloModeWithDestTracks = 1 << 1
fxSoloModeIgnorePrevious = 1 << 2

fxSoloSetOff = 0
fxSoloSetOn = 1
fxSoloToggle = 2
fxSoloGetValue = 3

EKRes = 1 / 24

#get peaks mode
PEAK_L = 0
PEAK_R = 1
PEAK_LR = 2
PEAK_LR_INV = 3

# routing mode
ROUTE_ToThis = 0
ROUTE_StartingFromThis = 1

# scales
HARMONICSCALE_MAJOR = 0
HARMONICSCALE_HARMONICMINOR = 1
HARMONICSCALE_MELODICMINOR = 2
HARMONICSCALE_WHOLETONE = 3
HARMONICSCALE_DIMINISHED = 4
HARMONICSCALE_MAJORPENTATONIC = 5
HARMONICSCALE_MINORPENTATONIC = 6
HARMONICSCALE_JAPINSEN = 7
HARMONICSCALE_MAJORBEBOP = 8
HARMONICSCALE_DOMINANTBEBOP = 9
HARMONICSCALE_BLUES = 10
HARMONICSCALE_ARABIC = 11
HARMONICSCALE_ENIGMATIC = 12
HARMONICSCALE_NEAPOLITAN = 13
HARMONICSCALE_NEAPOLITANMINOR = 14
HARMONICSCALE_HUNGARIANMINOR = 15
HARMONICSCALE_DORIAN = 16
HARMONICSCALE_PHRYGIAN = 17
HARMONICSCALE_LYDIAN = 18
HARMONICSCALE_MIXOLYDIAN = 19
HARMONICSCALE_AEOLIAN = 20
HARMONICSCALE_LOCRIAN = 21
HARMONICSCALE_CHROMATIC = 22

HARMONICSCALE_LAST = 22

MiddleNote_Default = 60
FineTune_Default = 0

DotVol_Default = 100
DotPan_Default = 64
DotVol_Max = 128
DotNote_Default = MiddleNote_Default

FFNEP_FindFirst = 0
FFNEP_DontPromptName = 1 << 1

pPitch = 0
pVelocity = 1
pRelease = 2
pFinePitch = 3
pPan = 4
pModX = 5
pModY = 6
pShift = 7

CT_Sampler = 0
CT_TS404 = 1
CT_GenPlug = 2
CT_Layer = 3
CT_AudioClip = 4
CT_AutoClip = 5

CT_ColorT = (0x565148 + 0x141414 , 0x868178, 0x514F61, 0x474440, 0x787168, 0x787168)

# event editor modes
EE_EE = 0
EE_PR = 1
EE_PL = 2

# snap modes
Snap_Default = -2
Snap_Line = 0
Snap_Cell = 1
Snap_None = 3
Snap_SixthStep = 4
Snap_FourthStep = 5
Snap_ThirdStep = 6
Snap_HalfStep = 7
Snap_Step = 8
Snap_SixthBeat = 9
Snap_FourthBeat = 10
Snap_ThirdBeat = 11
Snap_HalfBeat = 12
Snap_Beat = 13

Snap_SixthBar  = 14
Snap_FourthBar = 15
Snap_ThirdBar  = 16
Snap_HalfBar   = 17

Snap_Bar = 14
Snap_Events = 16
Snap_Markers = 17

Snap_ForceCell = 1 << 8
Snap_AltNone = 2 << 8
Snap_FlagsMask = 0xFF

#
TN_Master = 0
TN_FirstIns = 1
TN_LastIns = 2
TN_Sel = 3

#undo 
UF_None = 0

UF_EE = 1
UF_PR = 2
UF_PL = 4
UF_EEPR = UF_EE | UF_PR

UF_Knob = 1 << 5
UF_SS = UF_PR
UF_AudioRec = 1 << 8
UF_AutoClip = 1 << 9
UF_PRMarker = 1 << 10
UF_PLMarker = 1 << 11
UF_Plugin = 1 << 12
UF_SSLooping = 1 << 13

CC_Normal = 0 # standard CC
CC_Special = 128 # non-CC are mapped to CC after 128
CC_PitchBend = 255
CC_KeyAfterTouch = 254
CC_ChanAfterTouch = 253
CC_Note = 256 # when notes are linked to parameters
CC_Free = 256 + 128
CC_PLTrack = CC_Free # playlist track XY control (performance mode)

# song tick options
ST_Int = 0
ST_Beat = 1
ST_PGB = 2

# Live block status
LB_Status_Default = 0
LB_Status_Simple = 1
LB_Status_Simplest = 2

# channel looping settings for a given pattern (see TChannelLoopInfo)
ssLoopOff = 0
ssLoopNextStep = -1
ssLoopNextBeat = -2
ssLoopNextBar = -3

EventNameT = ['Note Off', 'Note On ', 'Key Aftertouch', 'Control Change','Program Change',  'Channel Aftertouch', 'Pitch Bend', 'System Message' ]
ChannelDefaultVolume = 1000 / 1280
TackDefaultVolume = 800 / 1000
    
def EncodeRemoteControlID(PortNum, ChanNum, CCNum):
  return CCNum + (ChanNum << 16) + ((PortNum + 1) << 22)
