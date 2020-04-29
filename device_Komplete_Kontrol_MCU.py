# name=Komplete Kontrol MCU
# url=https://www.native-instruments.com/en/products/komplete/keyboards/komplete-kontrol-m32/
# script by Duwayne "Sound" Wright www.soundwrightpro.com

import fl
import patterns
import channels
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import ui
import screen
import midi
import utils
import time

def OnInit():
		# command to initialize the protocol handshake
		device.midiOutSysex(bytes([0xF0, 0xBF, 0x01, 0x01, 0x14, 0x0C, 1, 0xF7]))

def OnDeInit():
		if ui.isClosing():
				# Command to stop the protocol
				device.midiOutSysex(bytes([0xF0, 0xBF, 0x02, 0x01, 0x14, 0x0C, 1, 0xF7]))





